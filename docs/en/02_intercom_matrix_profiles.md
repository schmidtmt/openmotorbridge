# 02 - Intercom Matrix, PTT Control & Dynamic Cartridge Profiles

This document specifies the universal **Intercom Routing Matrix**, the ultra-low-latency **Handlebar PTT Control** (< 0.5 ms), and the class-based **Hardware Profile System** of OpenMotorBridge v8.5 / v9.0 Clean Architecture based on All-UWB Cartridge Identification (`UWB_PKT_CARTRIDGE_ANNOUNCE`), staggered power sequencing, and the LittleFS profile engine.

---

## 1. Intercom Routing Matrix & Bridge Architecture

OpenMotorBridge operates as an active audio crossbar and bridge gateway between two physical intercom units (Bay 1 and Bay 2), external audio sources (Navigation / Boom! Box), and the rider and passenger Bluetooth helmets:

```
                                INTERCOM ROUTING MATRIX (ALL-UWB)
+----------------------------------------------------------------------------------------+
|                                                                                        |
|   SATELLITE BAY 1 (Gateway A * Sena)          SATELLITE BAY 2 (Gateway B * Cardo/OMM)  |
|   +--------------------------+                +--------------------------+             |
|   | * Sena SPIDER X / 50S/60S|                | * Cardo Edge / Pro / OMM |             |
|   | * UWB Transceiver DW3110 |                | * UWB Transceiver DW3110 |             |
|   | * 4x Mechatronic MOSFETs |                | * 4x Mechatronic MOSFETs |             |
|   +------------+-------------+                +------------+-------------+             |
|                |                                           |                           |
|                | 2-Wire DC Power (+5V / GND) from DTM-12   |                           |
|                | Staggered: T=200ms                        | Staggered: T=350ms        |
|                |                                           |                           |
|                +-------------+-----------------------------+                           |
|                              | Wireless UWB Audio & Control Streams                    |
|                              | (Qorvo DW3110 / 6.489 GHz Ch. 5 / Latency < 0.4 ms)     |
|                              v                                                         |
|       +------------------------------------------------------------+                   |
|       |     ESP32-S3 CORE 1 DSP & ES8388 24-BIT / 48 kHz AUDIO     |                   |
|       |  * Raised-Cosine Ducking (Prio: Radar > Nav > Intercom)    |                   |
|       |  * Symmetrical Intercom Cross-Mix (Bay 1 <-> Bay 2)        |                   |
|       |  * Knowles MEMS Wind Noise Adaptive Gain Control (AGC)     |                   |
|       +-----------------------------+------------------------------+                   |
|                                     | Synchronous I2S Digital Bus (48 kHz / 24-Bit PCM)|
|                                     v                                                  |
|       +------------------------------------------------------------+                   |
|       |        QUALCOMM QCC3084 BLUETOOTH 5.4 AUDIO SOC (U9)       |                   |
|       |  * Dual-A2DP Hardware Encoder (aptX HD & aptX Adaptive)    |                   |
|       |  * LE Audio Auracast Broadcast Engine                      |                   |
|       |  * HFP 1.8 Wideband Speech Telephony & Mic Uplink          |                   |
|       |  * Onboard Ceramic Chip Antenna (Zero Coax Cable Overhead) |                   |
|       +-----------------------------+------------------------------+                   |
|                                     |                                                  |
|              +----------------------+----------------------+                           |
|              | RF Stream 1 (aptX HD)                       | RF Stream 2 (aptX / LC3)  |
|              v                                             v                           |
|   +----------------------------+              +----------------------------+           |
|   | RIDER HELMET (Bluetooth)   |              | PASSENGER HELMET (BT)      |           |
|   | * Sena/Cardo/OEM Headset   |              | * Sena/Cardo/OEM Headset   |           |
|   | * aptX Adaptive (< 20 ms)  |              | * Synchronous Dual-A2DP Mix|           |
|   | * HFP 1.8 Microphone Uplink|              | * Independent AVRCP Volume |           |
|   +----------------------------+              +----------------------------+           |
+----------------------------------------------------------------------------------------+
```

### 1.1 The 3 Standard Operating Modes
1. **Mode 0: Standard Mode (Full Mesh Bridge):**  
   Bay 1 (e.g., Sena Mesh 3.0) and Bay 2 (e.g., Cardo DMC Gen2) are simultaneously active. Voice traffic from Sena riders is translated within milliseconds into the Cardo mesh and vice versa. Rider and passenger hear both conversation groups symmetrically mixed inside their Bluetooth helmets.
2. **Mode 1: Single Rider Mode (Focus Mode):**  
   Bay 2 is software-muted (`-96 dB`). Full DSP and routing focus shifts to the primary gateway (Bay 1), GPS navigation directions, and smartphone A2DP streaming.
3. **Mode 2: Cruise Mode (Onboard Speaker Output):**  
   Intercom signals are attenuated by $-6\,\text{dB}$ and routed to vehicle speakers (Harley-Davidson Boom! Box GTS / BMW Sound System).

### 1.2 Cross-Intercom Bridge (Bay 1 ↔ Bay 2) with Anti-Feedback Loopback Gate
* **Bidirectional Bridging:** Provides a seamless audio bridge between incompatible brands (e.g., Sena Spider X Slim Mesh 3.0 in Bay 1 and Cardo DMC Gen2 in Bay 2).
* **Adjustable Bleed Level:** Bleed attenuation continuously configurable from $-18\,\text{dB}$ to $0\,\text{dB}$ (default: $-6\,\text{dB}$) in the WebApp.
* **Anti-Feedback Loopback Gate ($-24\,\text{dB}$ Protection Circuit):**  
  As soon as voice activity is detected on Bay 1 (VOX active or PTT pressed), the DSP instantly clamps the return path from Bay 2 to Bay 1 by $-24\,\text{dB}$. This prevents the rider's voice exiting passenger helmet speakers from looping back into the opposite microphone (eliminating acoustic howl and flutter echoes).

### 1.3 Sidetone Voice Feedback
* **Natural Voice Sensation:** Inside sealed, noise-isolated full-face helmets, riders instinctively raise their voices at highway speeds.
* **Zero-Latency Monitoring:** The DSP feeds the filtered microphone signal back into helmet speakers with $< 2.7\,\text{ms}$ delay and configurable attenuation ($-40\,\text{dB}$ to $0\,\text{dB}$, default: $-12\,\text{dB}$, $< -35\,\text{dB} = \text{Mute}$).
* **VOX Coupling:** Sidetone engages only when VOX or PTT is active.

### 1.4 Intelligent GPS Auto-Sensing (Level-Controlled Ducking)
* **Hardware-Agnostic Ducking:** Operates seamlessly with analog line-level navigation units (e.g., Garmin Zūmo XT2 or BMW Motorrad Navigator) without requiring discrete trigger leads.
* **Threshold Detection:** When incoming GPS audio exceeds $-36\,\text{dBFS}$ for longer than $50\,\text{ms}$, the ducking engine executes smooth raised-cosine ducking ($-12\,\text{dB}$) across music and intercom channels.
* **Hold & Release:** Following the prompt (signal $< -42\,\text{dBFS}$), ducking holds for $800\,\text{ms}$ before executing a smooth $250\,\text{ms}$ release ramp.

### 1.5 Physical Dual-Helmet Connectivity via Qualcomm QCC3084 & aptX HD / Adaptive

Unlike compromised software-emulated A2DP stacks, OpenMotorBridge offloads helmet Bluetooth to a **dedicated Qualcomm QCC3084 Bluetooth 5.4 Audio SoC (`U9` on PCBA 01)** in dedicated hardware:

1. **Complete RF & CPU Decoupling:**
   * The ESP32-S3 internal radio shares a single 2.4-GHz RF path between Wi-Fi (PWA Webserver, WebDAV uploads) and BLE (telemetry dashboard). Computing and streaming dual Hi-Res A2DP streams on the host MCU would lead to buffer under-runs, crackling, and latency spikes $> 150\,\text{ms}$.
   * The Qualcomm QCC3084 operates autonomously on an independent dual-core 32-bit processor ($80\,\text{MHz}$) with a $240\,\text{MHz}$ Kalimba hardware audio DSP.
2. **True Dual-A2DP & aptX HD / Adaptive:**
   * **Rider Helmet (Stream 1):** Dynamic switching between **aptX HD** ($24\,\text{Bit} / 48\,\text{kHz}$, Studio-HiFi for media) and **aptX Adaptive Low-Latency Mode** ($< 20\,\text{ms}$ latency for lip-sync intercom clarity).
   * **Passenger Helmet (Stream 2):** Phase-locked secondary A2DP stream (aptX / LC3) with independent AVRCP volume control.
3. **LE Audio Auracast Broadcast:**
   * Enables sharing the entire vehicle mix (intercom, GPS, music) with unlimited Auracast-enabled companion devices without pairing limits.
4. **HFP 1.8 Wideband Speech & Rider Microphone Uplink:**
   * Decodes HFP 1.8 Wideband Speech ($16\,\text{kHz}$ mSBC / aptX Voice) and feeds the rider's voice into the host ESP32-S3 DSP pipeline over the synchronous `I2S_DIN` line.
5. **Onboard Ceramic Chip Antenna (Zero Coaxial Cable Overhead):**
   * The QCC3084 module integrates an omnidirectional $2.4\,\text{GHz}$ high-performance ceramic antenna directly on its $13 \times 18\,\text{mm}$ substrate, radiating cleanly through the enclosure toward rider and pillion.

---

### 1.6 Strategic Guide: The "Bridge-the-Gap" Principle & Helmet Battery Conservation

> [!IMPORTANT]
> **Defeating the €2,000 Hardware Trap:**
> OpenMotorBridge never forces riders to duplicate expensive hardware. If you already own a premium helmet with an integrated OEM system (e.g., Schuberth C5 + SC2 or Shoei Neotec 3 + SRL3 costing 800–1200 €), you continue to use it. On the motorcycle, you equip **only the missing counterpart brand (Bridge-the-Gap)**. This cuts equipment acquisition costs by more than 50%!

#### The Two Clear User Profiles:
1. **Profile A: "Bridge-the-Gap" (Rider Already Owns a Premium OEM Helmet):**
   * *Helmet features Sena (e.g., SC2 / SRL3):* Install **only Cardo (Packtalk Edge/Neo)** into Bay 1. Bay 2 remains available for **OMM 446 (PMR446 two-way radio)** or a waterproof storage dry-box.
   * *Helmet features Cardo (e.g., Beyond GTS / Edge):* Install **only Sena (Spider X Slim)** into Bay 1.
   * *Universal Bridging:* Through the Central Box DSP, the rider speaks to both worlds; OMB bridges seamlessly between Sena and Cardo mesh groups on demand.
2. **Profile B: "Helmet-Agnostic" (Dumb Helmet / Universal Helmet):**
   * The rider uses a budget standard helmet or ECE 22.06 UCS unit with OMM 2.4.
   * Both bike bays are populated (Sena + Cardo).
   * *Benefit:* Changing helmets anytime is 100% cost-free and brand-independent.

#### Massive Battery Savings: Standard Bluetooth on Helmet:
* Operating an active Mesh transceiver on the helmet (Sena Mesh or Cardo DMC) draws **$80\dots 130\,\text{mA}$**, depleting the 1,000 mAh helmet battery within **7 to 9 hours** (often before the tour ends!).
* When the helmet connects **strictly via low-power Bluetooth (HFP/A2DP)** to the OMB Central Box (while Mesh traffic is handled by the 12V bike-fed cartridge), current draw drops to **$15\dots 22\,\text{mA}$**.
* **Result:** Helmet battery runtime increases to **18 to 24+ hours** -- easily lasting an entire weekend tour without intermediate charging!

#### Mechatronic Advantage: Dedicated Pushbuttons vs. Jog Dials:
* For linear solenoids and micro-plungers, **flat, clearly defined discrete pushbuttons** (as on the Sena Spider X Slim, Spider RT1, 50R, or Cardo Packtalk Edge) are mechanically ideal with crisp tactile snap domes.
* Large rotary dials (jog dials as on the Sena 50S, 60S, or Spider ST1) feature angular play, soft stops, and require rotational torque -- making them poison for mechatronic actuation reliability.

---

## 2. Zero-Latency PTT Control & Mechatronic UWB Trigger (< 0.5 ms)

Classic handlebar Bluetooth remotes suffer from high latency ($80 \dots 250\,\text{ms}$) and connection dropouts. OpenMotorBridge resolves this with an ultra-low-latency **All-UWB PTT Signal Chain**:

```
               HANDLEBAR PTT SIGNAL CHAIN (GLASS-TO-GLASS < 0.54 ms)
+----------------------------------------------------------------------------------------+
| 1. HANDLEBAR SWITCH (Wired to Front Node PCBA 05):                                     |
|    * Mechanical gold-contact pushbutton on handlebar (IP67, 100% battery-free)         |
|    * Hardware Schmitt-trigger debouncing (12 µs latency)                               |
|    * GPIO level interrupt on ESP32-S3 host controller                                  |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 2. ULTRA-LOW-LATENCY WIRELESS BRIDGE 1: FRONT NODE -> CENTRAL BOX                      |
|    * IEEE 802.15.4z UWB Frame UWB_PKT_PTT_EVENT (6.8 Mbps PHY, < 180 µs flight time)   |
|    * 100% compliant with ETSI EN 302 065-1/3 & EU Decision 2019/785 (Zero duty cycle)  |
|    * Zero collision with 2.4 GHz Bluetooth, Wi-Fi, or Sena/Cardo Mesh (PDR: 99.99%)    |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 3. CENTRAL BOX DISPATCHER & WIRELESS BRIDGE 2: CENTRAL BOX -> CARTRIDGE                |
|    * ESP32-S3 Core 0 ISR decodes PTT event (< 35 µs) & generates opcode (< 10 µs)      |
|    * Dispatches UWB_PKT_CARTRIDGE_OPCODE wirelessly to Bay 1 or Bay 2 (< 180 µs)       |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 4. CARTRIDGE ACTUATOR TRIGGER (PCBA 03 Rev 3.0 All-UWB):                               |
|    * Host MCU on PCBA 03 switches AO3400A N-MOSFET (< 1 µs)                            |
|    * Solenoid depresses PTT/Mesh rubber pushbutton on headset (< 100 µs)               |
|    * Total glass-to-glass latency from switch press to physical button actuation: ~0.54|
+----------------------------------------------------------------------------------------+
```

### 2.1 Mechatronic Smart Cartridge & 4-Channel MOSFET Drivers (PCBA 03 Rev 3.0)

* **Physically Infinite Galvanic Isolation:** Mechatronic plungers actuate original rubber buttons from the outside without electrical connection to motorcycle power. Optocouplers on the mainboard are completely eliminated!
* **Ultra-Low Loss N-Channel MOSFETs (`AO3400A`):** Four power MOSFETs ($R_{\text{ON}} < 28\,\text{m}\Omega$) on `B.Cu` drive miniature solenoids bounce-free with $< 1\,\mu\text{s}$ response time.
* **100% Preservation of Factory Warranty & IPX Rating:** Headsets remain brand-new and sealed. Factory seals and rubber gaskets are untouched.
* **Form-Fit Retention Resisting $20\,\text{g}$ Vibration:** The 3D-printed PA12-MJF cradle nests the intercom with damping EPDM liners with zero play, ensuring plungers consistently strike buttons on-center with calibrated $1.0\dots 1.2\,\text{mm}$ travel.

### 2.2 Independent 4-Channel Actuator Matrix via UWB Opcodes

```
+----------------------------------------------------------------------------------------+
|        SENA SPIDER X SLIM - SMART CARTRIDGE ACTUATOR MATRIX (PCBA 03 Rev 3.0)          |
+----------------------+-----------------------+-----------------+-----------------------+
| Function / Opcode    | Active Actuators      | Pulse / Timing  | Sena Reaction         |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x01` Power Boot**| **ACT_CENTER + PLUS** | **1,000 ms**    | Cold boot from sleep  |
|                      |                       |                 | ("Hello")             |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x02` Power Off** | **ACT_CENTER + PLUS** | **200 ms**      | Clean power down      |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x03` Volume Up** | **ACT_PLUS** (solo)   | **100 ms**      | Volume step +1        |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x04` Vol Down**  | **ACT_MINUS** (solo)  | **100 ms**      | Volume step -1        |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x05` Mesh Toggle** **ACT_MESH** (solo)   | **200 ms**      | Mesh Intercom Toggle  |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x06` Group Mesh**| **ACT_MESH** (solo)   | **3,000 ms**    | Open ↔ Group Mesh     |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x07` Channel +1**| **1. ACT_MESH (2x)**  | **2x 150 ms**   | "Channel settings, #" |
| *(Autonomous Macro)* | **2. Pause 200 ms**   |                 |                       |
|                      | **3. ACT_PLUS (1x)**  | **150 ms**      | Next channel (1..6)   |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x08` Channel -1**| **1. ACT_MESH (2x)**  | **2x 150 ms**   | "Channel settings, #" |
| *(Autonomous Macro)* | **2. Pause 200 ms**   |                 |                       |
|                      | **3. ACT_MINUS (1x)** | **150 ms**      | Previous channel      |
+----------------------+-----------------------+-----------------+-----------------------+
```

---

## 3. Class-Based Hardware Profile Matrix & Device Hierarchy

All supported intercom and two-way radio cartridges are categorized into clearly segregated hardware classes:

```
+-----------------------------------------------------------------------------------------+
|                  CLASS-BASED HARDWARE PROFILE MATRIX (v9.6 REVISED)                     |
+----------+-------------------------------------+-----------------------+----------------+
| Class    | Device Families                     | Radio Protocol        | DLE Score Bonus|
+----------+-------------------------------------+-----------------------+----------------+
| **K1a**  | Sena 60S, 60R, 60X, Spider X Slim,  | Sena Mesh 3.0 & Wave  | **+60 Points** |
|          | Sena MeshON (Adapter, 800 m)        | (Next-Gen Dual Mesh)  |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1b**  | Sena 50S, 50R, 50C, Spider ST1/RT1, | Sena Mesh 2.0         | **+40 Points** |
|          | Sena +Mesh Adapter, SRL-Mesh, SC2   | (Preceding Standard)  |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1c**  | Sena 30K, +Mesh 1.0 (Legacy / EOL)  | Sena Mesh 1.0         | **+20 Points** |
+----------+-------------------------------------+-----------------------+----------------+
| **K1d**  | Cardo Packtalk Edge, Pro, Neo,      | Cardo DMC Gen2        | **+60 Points** |
|          | Cardo Packtalk Custom               | (Dynamic Mesh 2.0)    |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1e**  | Cardo Packtalk Bold, Black, Slim    | Cardo DMC Gen1 Legacy | **+30 Points** |
+----------+-------------------------------------+-----------------------+----------------+
| **K2**   | Sena Apex, Apex Plus (BT 6.0),      | Bluetooth Intercom    | **+30 Points** |
|          | Sena Vertex, 10R, 20S EVO, 5R,      | (Point-to-Point &     |                |
|          | Cardo Freecom 4x/2x, Spirit HD      | Daisy-Chain Multi-Hop)|                |
+----------+-------------------------------------+-----------------------+----------------+
| **K3a**  | Midland G7 Pro to G18 Pro, XT Series| PMR446 Analog (FM)    | **+15 Points** |
+----------+-------------------------------------+-----------------------+----------------+
| **K3b**  | OMM 446 (PCBA 10), Midland D-10,    | Digital DMR Tier I    | **+45 Points** |
|          | NiceRF SA818-DMR Transceiver        | & PMR446 Dual-Mode    |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K4**   | OMM 2.4 GHz Universal (PCBA 09 UCS) | OMM TDMA / IPv6 Mesh  | **+55 Points** |
+----------+-------------------------------------+-----------------------+----------------+
| **K0**   | Disabled / Empty Cartridge Slot     | None (eFuse OFF)      | **0 Points**   |
+----------+-------------------------------------+-----------------------+----------------+
```

### 3.1 Detailed Device Classification & Filesystem Profiles (`/data/profiles/`)

#### Class 1a: Sena Mesh 3.0 & Wave (`sena_60_series.json`, `sena_spider_x.json`, `sena_meshon.json`):
* **Sena 60 Series (60S, 60R, 60X):** Next-Gen flagships featuring Mesh 3.0 and Wave cellular fallback. While the 60S relies on a bulky jog dial, the **Sena 60X** is designed as a modular, flat pushbutton system.
* **Sena SPIDER X Slim (`sena_spider_x.json` - Top Reference Recommendation):**
  * *100% Battery-Free from Factory:* Powered directly via 2-wire battery leads at $3.85\,\text{V}$ regulated DC from PCBA 03. Zero fire hazard, zero LiPo swelling in hot pods, zero battery degradation.
  * *Full Mesh 3.0 & Wave Parity:* Full $2.0\,\text{km}$ range in an ultra-compact package ($74.5 \times 31 \times 16\,\text{mm}$, $23.2\,\text{g}$).
  * *Mechatronic Advantage:* Flat, clearly defined discrete buttons (Center, Plus, Minus, Mesh) -- ideal for linear plungers. DLE Score: **+60 pts.**
* **Sena MeshON (`sena_meshon.json`):**
  * Ultra-lightweight ($22.5\,\text{g}$) Mesh 3.0 adapter (with Mesh 2.0 fallback).
  * *Limitation:* Range is approx. $800\,\text{m}$ (half that of full units) and contains an internal battery. DLE Score: **+45 pts.**

#### Class 1b: Sena Mesh 2.0 (`sena_50_series.json`, `sena_spider.json`):
* *Sena 50S, 50R, 50C, SRL-Mesh, Schuberth SC2:* Standard Mesh 2.0 (24–32 nodes).
* *Sena Spider ST1 vs. Spider RT1:*
  * *Spider ST1:* Utilizes a large rotary jog dial (mechatronic hazard).
  * *Spider RT1:* Utilizes 3 ergonomic pushbuttons (far more reliable for linear actuation). DLE Score: **+40 pts.**

#### Class 1d: Cardo Dynamic Mesh Communications Gen2 (`cardo_packtalk_edge.json`):
* *Cardo Packtalk Edge / Pro:* DMC Gen2 reference unit with magnetic Air-Mount, continuous USB-C fast charging ("Charge while Riding"), and 4-actuator control. DLE Score: **+60 pts.**
* *Cardo Packtalk Neo:* Same DMC Gen2 chip, but fixed clamp cradle and lacks continuous ride charging support.

#### Class 2: Bluetooth Intercoms & Bluetooth 6.0 (`sena_apex.json`, `cardo_freecom_live.json`):
* **Sena Apex & Apex Plus (`sena_apex.json`):**
  * **Clarification:** The Sena Apex is **NOT a mesh system**, but a modern **Bluetooth 6.0 Intercom** (2-way for Apex, 4-way for Apex Plus).
  * Leverages BT 6.0 Core for long range and HD voice. Configuration via Sena App uses BLE GATT.

#### Class 3: PMR446 Two-Way Radio & Digital DMR Tier I (`pmr446_gateway.json` / `omm_446.json`):
* **Class 3a (Analog FM):** 16 channels (446.0–446.2 MHz, CTCSS/DCS) for 100% interoperability with handheld units (Midland G7 Pro, G9 Pro, G11, G13, G15, G18).
* **Class 3b (Digital DMR Tier I & OMM 446 `PCBA 10`):**
  * **OMM 446 ECE 22.06 UCS Module:** Digital DMR Tier I + Analog FM transceiver based on NiceRF SA818-DMR.
  * 100% compatible with digital units like the **Midland D-10** (crystal clear, crackle-free digital voice up to range limits).
  * Form-fit integrated 446-MHz helical antenna.

#### Class 4: OpenMotorMesh 2.4 GHz Universal Module (UCS) (`omm_2_4ghz.json`):
* Open-source TDMA / IPv6 multicast mesh module based on the **ESP32-C6 (`PCBA 09`)**.
* Native Bluetooth 5.3 LE Audio (LC3 Codec) with $< 30\,\text{ms}$ latency. DLE Score: **+55 pts.**

### 3.2 JSON Profile Schema Specification
Each hardware profile is stored as an independent JSON file in the ESP32-S3 internal LittleFS flash filesystem (`/data/profiles/*.json`), defining audio gain levels, ducking curves, mechatronic pulse mappings, and BLE remote control parameters:

```json
{
  "id": "sena_spider_x",
  "name": "Sena Spider X Slim (Smart Cartridge 4-Actuator)",
  "vendor": "Sena Technologies",
  "hardware_tier": 1,
  "vcc_enabled": true,
  "direct_dc_supported": true,
  "direct_dc_voltage_v": 3.85,
  "soft_start_ms": 80,
  "input_gain_db": 1.5,
  "output_gain_db": 0.0,
  "noise_gate_threshold_db": -44,
  "control_mode": "smart_cartridge_mechatronic",
  "smart_cartridge": {
    "controller_type": "CH32V003_RISCV",
    "onewire_emulation": true,
    "protocol": "single_wire_uart_19200",
    "num_actuators": 4,
    "command_table": {
      "0x01": { "name": "POWER_BOOT", "actuators": [1, 3], "duration_ms": 1000 },
      "0x02": { "name": "POWER_OFF", "actuators": [1, 3], "duration_ms": 200 },
      "0x03": { "name": "VOL_PLUS", "actuators": [1], "duration_ms": 100 },
      "0x04": { "name": "VOL_MINUS", "actuators": [2], "duration_ms": 100 },
      "0x05": { "name": "MESH_TOGGLE", "actuators": [4], "duration_ms": 200 },
      "0x06": { "name": "GROUP_MESH_TOGGLE", "actuators": [4], "duration_ms": 3000 }
    }
  },
  "ble_control": {
    "supported": true,
    "flavor": "sena_rc_gatt",
    "service_uuid": "0xFFE0",
    "device_name_prefix": "SPIDER-X",
    "capabilities": {
      "power_boot": false,
      "power_off": true,
      "mesh_toggle": true,
      "group_toggle": true,
      "volume_control": true,
      "channel_select": true,
      "mic_mute": true,
      "telemetry": true,
      "le_audio_lc3": false
    },
    "command_mapping": {
      "0x03": { "name": "VOL_PLUS", "ble_cmd": "0xAA550301" },
      "0x04": { "name": "VOL_MINUS", "ble_cmd": "0xAA550302" },
      "0x05": { "name": "MESH_TOGGLE", "ble_cmd": "0xAA550501" },
      "0x06": { "name": "GROUP_MESH_TOGGLE", "ble_cmd": "0xAA550601" }
    },
    "fallback_to_mechatronics_on_disconnect": true
  },
  "mesh_capabilities": {
    "protocol": "Sena_Mesh_3.0_Wave",
    "generation": 3,
    "max_nodes": 32,
    "open_mesh": true,
    "preconfig_channels": 6,
    "dle_bonus_score": 60
  }
}
```

#### The 5 BLE Flavors (`flavor`) in the Profile Schema:
1. **`omm_native` (`0x00MB`):**  
   Native OpenMotorMesh BLE 5.3 GATT Server (for `omm_ucs.json` / `PCBA 09` and Gateway Pods). Provides discrete 16-bit characteristics (`0x0001` PTT, `0x0002` Mesh Mode, `0x0003` Channel, `0x0004` Volume, `0x0005` Telemetry, `0x0006` LE Audio LC3 Configuration). Full bi-directional stereo with $< 25\,\text{ms}$ latency.
2. **`sena_rc_gatt` (`0xFFE0`):**  
   Sena Remote Control GATT protocol (compatible with Sena RC3, RC4, Handlebar Remote). Commands Mesh On/Off, Group Mesh, Volume, and Channel changes without physical actuator movements.
3. **`cardo_ble_v2` (`0xFE59`):**  
   Cardo Connect / Packtalk Edge/Pro Remote BLE API. Supports DMC Mute/Unmute, volume increments, and group reconnects.
4. **`hid_consumer_control` (`0x0C`):**  
   Standard Bluetooth Human Interface Device Consumer Control for legacy headsets and Midland BTR1 (Volume, Play/Pause).
5. **`none`:**  
   No BLE interface available (pure analog radios like Midland G9 Pro PMR446, `omm_pmr446.json`, or disabled cartridges). All commands are dispatched directly via hardware PTT lines or mechatronic actuators.

> [!NOTE]
> **Architectural Rule:** In the `ble_control` object, `power_boot` is by principle **always `false`**, because unpowered intercom devices in cold-off state cannot receive Bluetooth packets. Powering on is handled exclusively via the initial physical mechatronic plunger pulse (`0x01`). Once booted, runtime operation is 100% wear-free digital BLE. If the BLE link drops or desynchronizes, `fallback_to_mechatronics_on_disconnect` immediately engages.

---

## 4. All-UWB Cartridge Recognition, Staggered Power Sequencing & Plug-and-Play

Every cartridge carrier board (`PCBA 03 Rev 3.0 All-UWB`) incorporates an onboard Qorvo DW3110 UWB transceiver, broadcasting its unique 64-bit chip UID and hardware class wirelessly over UWB. Physical 1-Wire data lines and discrete DS2401 chips are retired:

```
+-------------------------------------------------------------+
|        ALL-UWB PLUG-AND-PLAY & POWER-SEQUENCING FLOW        |
+-------------------------------------------------------------+
| 1. STAGGERED POWER-UP (Sequencer via DTM-12):               |
|    * T=0ms: Central Box & Front Node boot on KL15 ignition  |
|    * T=200ms: Bay 1 eFuse closes (+5V rail active)          |
|    * T=350ms: Bay 2 eFuse closes (+5V rail active)          |
|    * Avoids battery voltage drops during starter cranking   |
+-------------------------------------------------------------+
|                                v                            |
| 2. WIRELESS DISCOVERY VIA UWB (Airgap < 0.4 ms):            |
|    * Cartridge boots; transmits UWB_PKT_CARTRIDGE_ANNOUNCE  |
|    * Payload: 64-bit UID, hardware class, battery status    |
|    * Central Box loads /data/profiles/<profile_id>.json     |
+-------------------------------------------------------------+
```

### 4.1 Control Hierarchy: Digital BLE Primary Path vs. Mechatronic Fallback

To maximize component lifespan and eliminate mechanical wear, OpenMotorBridge enforces a strict two-tier control hierarchy:

1. **Digital BLE GATT Primary Path (Zero-Wear):**
   * Once the intercom device is powered on and connected via Bluetooth Low Energy, all **runtime commands** (Mesh activation, group toggles, volume +/-, channel selection, mic mute) are dispatched **strictly digitally via BLE GATT**.
   * Latency: **$< 5\,\text{ms}$** (compared to $100\dots 300\,\text{ms}$ mechanical actuator travel).
   * For `PCBA 09` (OMM 2.4 GHz), the native service `0x00MB` manages all parameters directly. For Sena and Cardo, the cartridge BLE client commands the corresponding vendor GATT characteristics.

2. **Physical Mechatronics (Plungers / MOSFETs) for Cold-Boot & Fallback Only:**
   * **Power ON (Cold-Boot):** Essential because when an intercom is powered off, its Bluetooth radio is completely unpowered. Only a physical mechatronic press (e.g., Center + Plus for $1.0\,\text{s}$ on Sena Spider X Slim) can boot the unit.
   * **Power OFF (Shutdown):** Reliable mechatronic power-down upon vehicle ignition cut (KL15).
   * **Failsafe Fallback:** If the BLE link drops or a vendor changes their proprietary BLE handshake via firmware update, the cartridge firmware immediately falls back to the physical 4x AO3400A MOSFET actuator gates.

---

## 5. Cartridge Interface Pinout (`J_AUDIO_PWR` / 8-Pin JST-SH 1.0mm)

### 5.1 Detailed Pinout of Cartridge Header (`J_AUDIO_PWR`) with Kelvin Grounding

To physically eliminate **common-impedance ground coupling (charging ripple & Mesh TDMA transmit buzzing)**, the `J_AUDIO_PWR` header on `PCBA 03` is designed as an **8-pin JST-SH connector** with complete Kelvin ground isolation:

| Pin | Signal | Class 1a/1b (Sena SPIDER X Slim) | Class 1d (Cardo Packtalk Edge) | Class 3a (Midland PMR446) | Class 4 (OMM 2.4/446 UCS) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `PGND` | 2-Pin DC Return (Power Ground) | USB-C Charge Ground (Return) | DC Battery Dummy GND | USB-C Power Return |
| **2** | `VCC_HEADSET` | +3.85V Regulated Direct-DC | +5V VBUS Fast Charging | +5V VBUS Battery Dummy | +5V VBUS Power-Path |
| **3** | `AGND_SPK` | 3.5mm Spk Sleeve (Audio GND, $I=0$) | 3.5mm Spk Sleeve (Audio GND, $I=0$) | 3.5mm Spk Sleeve (Audio GND, $I=0$) | Clean Audio GND (DAC/ADC, $I=0$)|
| **4** | `AUDIO_L_IN` | 3.5mm Jack Tip (Spk In L $\leftarrow$) | 3.5mm Jack Tip (Spk In L $\leftarrow$) | 3.5mm Jack Mono Tip ($\leftarrow$) | I2S / Line-In Left ($\leftarrow$) |
| **5** | `AUDIO_R_IN` | 3.5mm Jack Ring (Spk In R $\leftarrow$)| 3.5mm Jack Ring (Spk In R $\leftarrow$)| 3.5mm Jack Bridged ($\leftarrow$) | I2S / Line-In Right ($\leftarrow$) |
| **6** | `AGND_MIC` | 2.5mm Mic Sleeve (Audio GND, $I=0$) | Cardo 2-Pin Mic- (Audio GND, $I=0$) | 2.5mm Mic Sleeve (Audio GND, $I=0$) | Mic Ground ($I=0$) |
| **7** | `MIC_OUT` | 2.5mm Mic Tip (Voice Out $\rightarrow$) | Cardo 2-Pin Mic+ (Voice Out $\rightarrow$) | 2.5mm Mic Tip (Voice Out $\rightarrow$) | Mic Signal (Voice Out $\rightarrow$)|
| **8** | `PTT_IO` | N/C (Mechatronics active) | N/C (Mechatronics active) | PTT Keying to GND (MOSFET `Q4`) | Digital PTT / Config IO |

> [!IMPORTANT]
> **Complete Ground-Hum Elimination via Kelvin Grounding:**
> Dedicated audio ground pins 3 (`AGND_SPK`) and 6 (`AGND_MIC`) carry **zero DC supply or charging current** ($I = 0\,\text{A} \implies \Delta V = 0\,\text{mV}$). The heavy $300\dots 600\,\text{mA}$ charging and Mesh RF transmit current returns exclusively over Pin 1 (`PGND`) directly to the carrier PCB power filter. This keeps the microvolt-level microphone line ($5\dots 15\,\text{mV}$) 100% immune to TDMA buzz and charger whine!

---

## 6. Safety Fallback: `disabled.json` & Zero-Trust Quarantine

When a cartridge bay is empty, contains a blank dummy cartridge, or is shut down via the WebApp, the system loads `disabled.json`:
* `vcc_enabled`: `false` (eFuse isolated, zero parasitic power draw).
* `input_gain_db` & `output_gain_db`: `-96.0 dB` (hermetic digital mute).
* `control_mode`: `"disabled"` (all actuator MOSFETs de-energized).

---

## 7. Recommended Pod Configuration Scenarios

```
+-----------------------------------------------------------------------------+
|                   RECOMMENDED POD CONFIGURATION SCENARIOS                   |
+-----------------------+-------------------------+---------------------------+
| Setup Category        | Pod 1 (Left Frame)      | Pod 2 (Right Frame)       |
+-----------------------+-------------------------+---------------------------+
| ⭐ **OMB Reference**   | **Sena SPIDER X Slim**  | **Cardo Packtalk Edge**   |
|   (Price-Performance  | (Mesh 3.0 Direct-DC,K1a)| (DMC Gen2 Air-Mount, K1d) |
|    Leader & Standard) | (DLE +60 pts, ~210 €)   | (DLE +60 pts, ~260 €)     |
+-----------------------+-------------------------+---------------------------+
| 🌐 **Universal Mesh** | **Sena SPIDER X Slim**  | **OMM 446 UCS (PCBA 10)** |
|   (Dual-World Bridge) | (Mesh 3.0 Wave, K1a)    | (DMR Tier I + PMR, K3b)   |
+-----------------------+-------------------------+---------------------------+
| 🛡️ **Autonomous Open**| **OMM 2.4 GHz (PCBA 09)**| **OMM 446 UCS (PCBA 10)** |
|   (100% Open Source)  | (Open TDMA Mesh, K4)    | (DMR Tier I + PMR, K3b)   |
+-----------------------+-------------------------+---------------------------+
| 💰 **Budget Entry**   | **Sena SPIDER X Slim**  | **IP67 Blank Dry-Box**    |
|   (Lean & Reliable)   | (Direct-DC, K1a)        | (Storage Bay, Slot OFF)   |
+-----------------------+-------------------------+---------------------------+
```

### 7.1 Why the Sena SPIDER X Slim is Our Official Reference Recommendation for Pod 1
1. **Full Mesh 3.0 & Wave Parity:** Delivers identical mesh performance to the €500 flagship Sena 60S (+60 DLE points).
2. **Lean Transceiver Form Factor:** Zero useless helmet bloat (no jog dials, no helmet spotlights, no integrated bulky wire looms).
3. **Direct-DC & Factory 3-Port Cable Whip:** Powered directly via 2-wire battery leads from PCBA 03 ($3.85\,\text{V}$) without an internal LiPo battery. Connects directly to `J_AUDIO_PWR` over the 8-pin Kelvin harness -- zero pogo pins, zero warranty loss!
4. **Dedicated Tactile Pushbuttons:** Crisp snap domes provide 100% reliable mechatronic actuation compared to rotary dials.
