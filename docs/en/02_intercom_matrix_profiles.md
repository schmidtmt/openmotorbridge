# 02 - Intercom Matrix, Hardware Profiles & Dynamic Routing

This document defines the 5 OEM adapter classes (A through E), the dynamic LittleFS profile engine, the opto-isolated PTT keying architecture (< 1.8 ms latency), and the audio routing cross-matrix of OpenMotorBridge v8.0.

---

## 1. The 5 OEM Adapter Classes (A through E)

To support every intercom and radio standard on the market without proprietary lock-in, OpenMotorBridge categorizes all headsets into 5 distinct hardware classes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 5 OEM ADAPTER CLASSES (A THROUGH E)                         │
├───────┬───────────────────────────────┬───────────────────────────────┬────────────────┤
│ Class │ Intercom / Radio System       │ Interface / Cradle            │ Audio / PTT    │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **A** │ **Sena 50S / 60S / 30K / 20S**│ OEM Spring-Loaded Pogo Array  │ Galvanic Audio,│
│       │ (Mesh 2.0 / 3.0 & Wave)       │ Form-fit Snap-In with POM Lock│ Opto-PTT Keying│
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **B** │ **Cardo Packtalk Edge / Pro** │ Magnetic Air-Mount Cradle     │ Galvanic Audio,│
│       │ (Dynamic Mesh Comm. Gen 2)    │ Dual N52 Magnets + EPDM Strap │ Opto-PTT Keying│
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **C** │ **Midland BTR1 / XT Series**  │ Dovetail Slide / Bare-Board   │ Galvanic Audio,│
│       │ (Wave Mesh & Analog PMR446)   │ 2-Pin 2.5/3.5mm Double Jack   │ PhotoMOS PTT   │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **D** │ **OpenMotorMesh Transceiver** │ Direct Pod 3 Integration      │ LoRa 868 MHz,  │
│       │ (Long-Range LoRa & Multi-GNSS)│ RP2040 Coprocessor + SX1262   │ 10 Hz DGPS     │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **E** │ **Hermetic Dry-Box Blind Pod**│ Closed Front Bezel with       │ Mute (-96 dB), │
│       │ (Weatherproof Blank Cartridge)│ Internal 80x46x16mm Storage   │ 5V Rail OFF    │
└───────┴───────────────────────────────┴───────────────────────────────┴────────────────┘
```

---

## 2. Dynamic 1-Wire Profile Loading (LittleFS JSON Engine)

Each interchangeable cartridge integrates a **Maxim DS2401 64-Bit Silicon Serial ROM** on its carrier board (`PCBA 03`). Upon sliding a cartridge into Pod 1 or Pod 2:

1. **Hardware Detection:** The 1-Wire manager task on Core 0 reads the unique 64-bit ROM-ID within 25 ms.
2. **Profile Resolution:** The ROM-ID maps to a configuration file on the internal flash filesystem:
   * `0x01...` $\rightarrow$ `/profiles/sena_50s.json`
   * `0x02...` $\rightarrow$ `/profiles/cardo_edge.json`
   * `0x03...` $\rightarrow$ `/profiles/midland_pmr.json`
   * `0x04...` $\rightarrow$ `/profiles/omm_transceiver.json`
   * Unknown / Timeout $\rightarrow$ `/profiles/disabled.json` (Mute to prevent open noise).
3. **Dynamic DSP Parameterization:** The ES8388 Audio Codec automatically loads specific input sensitivities, Ducking curves, AGC thresholds, and optocoupler pulse timings without requiring a system reboot.

---

## 3. Opto-Isolated Zero-Latency PTT Keying (< 1.8 ms)

To trigger headset transmission (Push-to-Talk or Mesh Channel Toggle) cleanly without switch bouncing or voltage feedback into sensitive intercom inputs:

```
HANDLEBAR PTT PUSHBUTTON (COCKPIT)
┌─────────────────────────────────────────────────────────────┐
│ 1. Mechanical Handlebar Switch closes (Direct GPIO Interrupt)│
│ 2. ESP32-S3 builds IEEE 802.11 Vendor Action Frame (ESP-NOW)│
│ 3. Over-the-Air Transmission to Central Box: 0.90 ms        │
│ 4. ESP32-S3 Core 0 ISR decodes frame in 45 µs               │
│ 5. Toshiba TLP222A PhotoMOS switches in 0.50 ms             │
│ 6. Headset enters Transmit Mode: TOTAL LATENCY = 1.74 ms!   │
└─────────────────────────────────────────────────────────────┘
```

* **Galvanic Isolation:** The Toshiba TLP222A solid-state PhotoMOS relay isolates up to $1500\,\text{V}_{\text{RMS}}$ between motorcycle logic and the headset mic/key lines.
* **Bounce-Free:** Clean optical switching eliminates contact bounce and audio clicks.
* **Firmware Pulse Sequencer:** Supports configurable click patterns (Single-Click 200 ms, Double-Click $2 \times 150\,\text{ms}$, Long-Press $3000\,\text{ms}$).

### 3.1 Hardware Characteristics of Toshiba TLP222A Optocoupler
* **Galvanic Isolation:** $1500\,\text{V}_{\text{RMS}}$ dielectric breakdown voltage between control and load circuits.
* **Switching Time:** Turn-on time $t_{\text{ON}} \le 0.5\,\text{ms}$, turn-off time $t_{\text{OFF}} \le 0.2\,\text{ms}$.
* **Bounce-Free:** Purely photo-electronic semiconductor MOSFET switch prevents contact chatter, arcing, and audible clicks.
* **Headset Circuit Protection:** Switches directly to ground or signal bias, exactly matching OEM button circuitry (e.g. Sena Mesh button or Cardo Phone button).

### 3.2 Specific Key Controls & Pulse Sequences for Sena SPIDER X Slim (User Guide v1.0.0)

The Sena SPIDER X Slim operating logic differs fundamentally from classic jog-dial headsets (such as Sena 20S/50S). For reliable automation via the Toshiba TLP222A optocoupler on Pin 6 (`OPTO_PTT`), the following pulse sequences derived from the official user guide apply:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│        SENA SPIDER X SLIM – OPTO-PULSE & BUTTON AUTOMATION (User Guide v1.0.0)         │
├─────────────────────────┬──────────────────────┬───────────────────────────────────────┤
│ Function                │ TLP222A Opto-Pulse   │ Sena Reaction & Voice Prompt          │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Mesh Intercom On/Off**│ **1x 200 ms** (short)│ On: "Mesh Intercom On"                │
│ (User Guide page 25)    │                      │ Off: "Mesh Intercom Off"              │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Channel Select Menu** │ **2x 150 ms**        │ Enter: "Channel settings, 1"          │
│ (User Guide page 26)    │ (Pause 150 ms)       │ Save: Automatic after 10s inactivity  │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Microphone Mute/Unmute**│ **1x 1000 ms** (1 s)│ Mute: "Mic off"                       │
│ (User Guide page 26)    │                      │ Active: "Mic on"                      │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Open ↔ Group Mesh**   │ **1x 3000 ms** (3 s) │ Toggle: "Open Mesh" /                 │
│ (User Guide page 29)    │                      │         "Group Mesh"                  │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Mesh Grouping**       │ **1x 5000 ms** (5 s) │ Starts private pairing:               │
│ (User Guide page 27/28) │                      │         "Mesh Grouping"               │
├─────────────────────────┼──────────────────────┼───────────────────────────────────────┤
│ **Mesh Reset**          │ **1x 8000 ms** (8 s) │ Factory reset to Channel 1:           │
│ (User Guide page 30)    │                      │         "Reset Mesh"                  │
└─────────────────────────┴──────────────────────┴───────────────────────────────────────┘
```

#### Key Implementation Insights for Firmware & Automation:
1. **Channel Selection (`opto_port1_channel_next()`):**
   * *Critical Distinction:* On older Sena headsets, channel switching was triggered by a 1000 ms long press. On the SPIDER X Slim, a 1000 ms press **toggles microphone mute**!
   * Accessing channel selection requires a **double click ($2 \times 150\,\text{ms}$ with $150\,\text{ms}$ inter-pulse gap)**.
   * Saving the selected channel is handled autonomously by the headset after a 10-second inactivity timeout.
2. **Switching Between Open Mesh and Group Mesh (`opto_port1_toggle_group_mesh()`):**
   * An exact **3000 ms hold pulse** toggles seamlessly between public Open Mesh (Channels 1–6) and private Group Mesh. In the OpenMotorBridge WebApp, this is triggered via BLE GATT command `0x08`.
3. **Power Management & Vibration Sensor Auto-Wakeup (User Guide page 17):**
   * *Manual Button Combo:* Power ON requires Center (`C`) + `+` held for 1s; Power OFF requires Center (`C`) + `+` tapped once.
   * *Direct-DC Automation via G-Sensor:* The SPIDER X Slim features a built-in accelerometer/motion sensor. When *"Auto Power On/Off"* is enabled in the Sena app, the device enters ultra-low power sleep ($< 1\,\text{mA}$) after 2 minutes without motion.
   * **Automatic Wakeup on Ride Start:** If the motorcycle is moved within 3 days (lifting off side stand, ignition on, engine vibration), the SPIDER X Slim wakes up **completely automatically without pressing any button**! Operating on the $3.85\,\text{V}$ regulated DC rail from OpenMotorBridge, daily rides require zero physical button presses.

---

## 4. Cross-Matrix Audio Routing & Priority Levels

The DSP mixer core routes audio signals dynamically across all connected endpoints:

| **Priority** | **Audio Source** | **Ducking Behavior** | **Target Endpoints** |
| :---: | :--- | :--- | :--- |
| **1 (Highest)** | **Emergency Intercom / Warning** | Ducks all other audio to $-24\,\text{dB}$ | Driver & Passenger Helmets |
| **2** | **Navigation Prompts (GPS/CarPlay)** | Smooth Raised-Cosine Ducking ($-18\,\text{dB}$) | Driver Helmet |
| **3** | **Mesh Intercom (Sena / Cardo / OMM)** | Low latency, Full-Duplex mixing | Group Broadcast |
| **4 (Lowest)** | **Media Audio (Music / FM Radio)** | Background music stream | Helmets (Muted during voice) |

---

## 5. 3-Phase Plug-and-Play Detection Sequence

To protect active headsets against electrical shorts and hot-plug transients, OpenMotorBridge executes a strict 3-phase hardware handshake:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CLASS-BASED HARDWARE PROFILE MATRIX                         │
├─────────┬───────────────────────────────┬─────────────────┬─────────────────┤
│ Class   │ Device Families               │ Mesh Protocol   │ DLE Score Bonus │
├─────────┼───────────────────────────────┼─────────────────┼─────────────────┤
│ **K1**  │ Sena 60S, Apex, 50S/R/C, SRL3 │ Sena Mesh 3.0/2 │ **+60 Points**  │
│ **K2a** │ Sena SPIDER X Slim            │ Mesh 3.0 & Wave │ **+60 Points**  │
│ **K2b** │ Sena Spider RT1/ST1           │ Mesh 2.0 Basic  │ **+40 Points**  │
│ **K3**  │ Sena Vortex, 20S, 10S, SF, 5S │ Bluetooth 5.1/4 │ **+20 Points**  │
│ **K4**  │ Cardo Edge, Pro, Custom, Neo  │ Cardo DMC Gen2  │ **+60 Points**  │
│ **K5**  │ Cardo Freecom 4x/2x, Spirit HD│ Live Intercom   │ **+40 Points**  │
│ **K6**  │ Cardo Bold, Black, Slim       │ Cardo DMC Gen1  │ **+30 Points**  │
│ **K7**  │ Midland G9 Pro, Baofeng/UHF   │ PMR446 Analog   │ **+10 Points**  │
│ **K8**  │ Midland BTR1, Rush RCF, Wave  │ Midland Wave    │ **+30 Points**  │
│ **K0**  │ Disabled / Empty Slot         │ None            │ **0 Points**    │
└─────────┴───────────────────────────────┴─────────────────┴─────────────────┘
```

### 3.1 Detailed Device Classification & Profiles in Filesystem (`/data/profiles/`)
* **Class 1: Sena Next-Gen & High-Tier Mesh (`sena_60s.json`, `sena_apex.json`, `sena_50_series.json`):**
  * *Sena 60S:* Wave Mesh Intercom, up to 64 participants, dual-chip RF hardening, DLE +60 pts.
  * *Sena Apex / Apex Plus:* Mesh 3.0 reference cartridge, 32 nodes, DLE +60 pts.
  * *Sena 50S, 50R, 50C, SRL3, MeshPort Blue/Red:* Mesh 2.0/3.0, 24–32 nodes.
* **Class 2: Sena Spider & Lean Mesh-Only (`sena_spider_x.json`, `sena_spider.json`):**
  * *Sena SPIDER X Slim (K2a - `sena_spider_x.json`):* The ideal lean mesh transceiver module for OpenMotorBridge. Delivers native **Mesh 3.0 & 2.0** as well as Wave Intercom with Bluetooth 5.3 and Sound by BOSE, completely eliminating helmet flagship bloat (no jog dial, no ambient helmet lights, no internal battery).
    * *Factory 3-Port Cable Whip (Manual p. 6):* The main unit ($74.5 \times 31 \times 16\,\text{mm}$, only $23.2\,\text{g}$) exposes all interfaces via molded OEM micro-connectors on a single flexible harness: **Port ⑧ Battery Pack** (Direct-DC $3.85\,\text{V}$), **Port ⑨ Microphone** (direct injection from ES8388 DAC), and **Port ⑩ Speakers** (analog audio tap into ES8388 ADC).
    * *Direct-DC & Zero Pogo Pins:* Requires no fragile pogo-pin cradle. Powered via the 2-wire battery harness at $3.85\,\text{V}$ DC directly from the Carrier PCB – **zero LiPo swelling/aging, zero opening of enclosures, zero soldering, and zero voided warranties!** DLE Score: **+60 pts** (full parity with 60S/Apex at half the price and zero helmet overhead).
  * *Sena Spider RT1 / ST1 (K2b - `sena_spider.json`):* Pure Mesh 2.0 devices with integrated battery and zero Bluetooth intercom overhead, DLE +40 pts.
* **Class 3: Sena Bluetooth & 2-Way Intercom (`sena_vortex.json`, `sena_legacy_bt.json`):**
  * *Sena Vortex:* Bluetooth 5.1 2-way intercom (1:1 up to 1.2 km), quick-pair button trigger, DLE +20 pts.
  * *Sena 20S EVO, 30K, 10S, 10R, SF4/SF2, 5S, SMH10:* Jog-dial pulse sequence for BT multi-hop, DLE +20 pts.
* **Class 4: Cardo Dynamic Mesh Communications Gen2 (`cardo_dmc_gen2.json`):**
  * *Cardo Packtalk Pro, Edge, Custom, Neo:* DMC Gen2 with Open DMC, ultra-fast auto-reconnect, and DLE +60 pts.
* **Class 5: Cardo Live Intercom & Freecom Series (`cardo_freecom_live.json`):**
  * *Cardo Freecom 4x, Freecom 2x, Spirit HD:* Bluetooth 5.2 Live Intercom with automatic reconnect, DLE +40 pts.
* **Class 6: Cardo Legacy DMC Gen1 (`cardo_dmc_legacy.json`):**
  * *Cardo Packtalk Bold, Black, Slim, Smartpack:* DMC 1.0 with up to 15 participants, DLE +30 pts.
* **Class 7: Universal Analog & PMR446 Two-Way Radio Cartridges (`pmr446_gateway.json`):**
  * *Midland XT Series (XT10/XT30/XT50 Bare-Board) & Integrated SA818S Transceivers:* Compact PMR446 cartridge modules (500 mW ERP, 446.0–446.2 MHz, 16 channels, CTCSS/DCS) for analog group communications.
  * *Midland G9 Pro / Baofeng / Kenwood 2-Pin K-Type:* External handheld radios docked via weatherproof dual-jack faceplate.
  * *Hardware PTT:* Seamless keying via photoMOS relay (Toshiba TLP222A on Pin 6 `OPTO_PTT`) synchronized with handlebar PTT or automatic DSP threshold VOX.
  * *Audio Decoupling:* Galvanic isolation through studio-grade audio transformers (Bourns LM-NP-1001) completely suppresses alternator whine and ground loops.
* **Class 8: Midland Intercom & Wave Series (`midland_wave.json` / `midland_bt.json`):**
  * *Midland BTR1 Advanced, Rush RCF, BTX2 PRO S, Midland Wave, BT Mini:* Bluetooth 5.0/5.2 Intercom & Wave Mesh with digital audio pass-through and DLE +30 pts.

### 3.2 JSON Profile Schema Specification
Each hardware profile resides as an autonomous JSON file in the ESP32-S3 internal Flash filesystem (`/data/profiles/*.json`), specifying all gain, routing, and optocoupler timing parameters:

```json
{
  "id": "sena_60s",
  "name": "Sena 60S Wave Mesh 3.0",
  "vendor": "Sena Technologies",
  "hardware_tier": 1,
  "vcc_enabled": true,
  "vcc_current_limit_ma": 850,
  "soft_start_ms": 120,
  "input_gain_db": 0.0,
  "output_gain_db": -2.5,
  "ducking_attenuation_db": -12.0,
  "ducking_attack_ms": 35,
  "ducking_release_ms": 650,
  "noise_gate_threshold_db": -54,
  "control_mode": "pogo_pulse",
  "opto_trigger_duration_ms": 120,
  "opto_trigger_hold_ms": 1500,
  "mesh_capabilities": {
    "protocol": "Sena Wave Mesh 3.0",
    "max_group_nodes": 64,
    "dle_bonus_score": 60
  },
  "audio_routing": {
    "intercom_bridge": true,
    "rider_headset": true,
    "pillion_headset": true,
    "boombox_lineout": false
  }
}
```

---

## 4. 1-Wire DS2401 Cartridge Recognition & 3-Phase Plug-and-Play

Each cartridge carrier PCB (`openmotorbridge_pod_cartridge`) features a factory-soldered **Maxim/Analog Devices DS2401** silicon serial number chip, reporting a globally unique 64-bit UID (`Family Code 0x01 + 48-bit Serial + 8-bit CRC`) over a single data line.

```
┌─────────────────────────────────────────────────────────────┐
│          3-PHASE PLUG-AND-PLAY DETECTION SEQUENCE           │
├─────────────────────────────────────────────────────────────┤
│ 1. DETECTION: 1-Wire ID query (current-limited < 20 mA)     │
│ 2. VALIDATION: Family Code & 64-bit UID checked vs database │
│ 3. RELEASE: Only on match -> 5V MOSFET ON & Audio/UART live │
└─────────────────────────────────────────────────────────────┘
```

1. **Current-Limited Interrogation:** Upon cartridge insertion, the 5V high-side switch remains OFF. The 1-Wire driver polls with a current-limited sense voltage ($< 20\,\text{mA}$) to read the DS2401 UID.
2. **Dynamic Routing Assignment:**
   * **Rear Pod 3 UID detected:** Central Box switches pins 15/16 to high-speed UART (460,800 Baud) and initializes the NMEA/LoRa parser.
   * **Audio Cartridge (Sena/Cardo) detected:** Pins are routed to the Bourns audio path and ES8388 I2S DSP; the matching JSON profile is loaded.
   * **Blank Cartridge or Unassigned UID:** Bay remains unpowered (`disabled.json`).
3. **Controlled Soft-Start:** Once validated, the P-channel MOSFET energizes the cartridge via a soft-start ramp ($100-150\,\text{ms}$) preventing inrush dips.

---

## 5. OEM Adapter Connection System: Classes & Pinouts

OpenMotorBridge supports all standard commercial intercom units intact without opening their housings:

### 5.1 Cartridge Pinout Specification (`J2` / JST-SH 1.0 mm)

The 6-pin **JST-SH 1.0 mm header (`J2`)** on `PCBA 03` connects to the OEM headset cradle:

| Pin | Signal | Class A (+Mesh) | Class B (Sena 50S) | Class C (Cardo Edge)| Class E (PMR446) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Micro-USB Pin 5 (GND) | Pogo-Pin 1 (GND) | Air-Mount Pad 1 (GND) | Plug Shield / Chassis |
| **2** | `5V_VBUS` | Micro-USB Pin 1 (+5V) | Pogo-Pin 2 (5V Charge)| Air-Mount Pad 2 (5V Charge)| Battery Dummy 5V In |
| **3** | `AUDIO_R+` | *N/C (Pure BT Audio)* | Pogo-Pin 4 (Spk R+) | Air-Mount Pad 3 (Spk +)| Plug Speaker + |
| **4** | `AUDIO_R-` | *N/C (Pure BT Audio)* | Pogo-Pin 5 (Spk R-) | Air-Mount Pad 4 (Spk -)| Plug Speaker - |
| **5** | `MIC_IN+` | *N/C (Pure BT Audio)* | Pogo-Pin 6 (Mic +) | Air-Mount Pad 5 (Mic +)| Plug Microphone + |
| **6** | `OPTO_PTT` | *N/C* | Pogo-Pin 7 (Mesh-Btn)| *N/C* (Aux) | PTT Switch to Ground |

---

## 6. Safety Fallback: `disabled.json` & Zero-Trust Quarantine

If a bay is empty, a blank cartridge is inserted, or an unknown UID is read, ESP32-S3 immediately loads `disabled.json`:

```json
{
  "id": "disabled",
  "name": "Deaktiviert / Unbelegt (Disabled Slot)",
  "vendor": "OpenMotorBridge System",
  "hardware_tier": 0,
  "vcc_enabled": false,
  "soft_start_ms": 0,
  "input_gain_db": -96.0,
  "output_gain_db": -96.0,
  "ducking_attenuation_db": 0.0,
  "ducking_attack_ms": 0,
  "ducking_release_ms": 0,
  "noise_gate_threshold_db": -96,
  "control_mode": "disabled",
  "opto_trigger_duration_ms": 0,
  "opto_trigger_hold_ms": 0,
  "mesh_capabilities": {
    "protocol": "None",
    "max_group_nodes": 0,
    "dle_bonus_score": 0
  },
  "audio_routing": {
    "intercom_bridge": false,
    "rider_headset": false,
    "pillion_headset": false,
    "boombox_lineout": false
  }
}
```

### 6.1 Protective Actions of `disabled.json`
1. **Power Isolation (`vcc_enabled: false`):** The P-channel MOSFET disconnects power immediately $\rightarrow 0{,}0\,\text{mA}$ current draw.
2. **Audio Mute:** Codec input and output gains are locked to $-96\,\text{dB}$ eliminating open-line noise or crosstalk.
3. **High-Z Optocoupler:** TLP222A relays remain open.
4. **DLE Score = 0:** Prevents unverified hardware from affecting mesh leader election.

### 6.2 Zero-Trust Hardware Quarantine
Until newly inserted cartridge hardware (DS2401 UID) is assigned to a verified profile by the rider, the bay is **strictly treated as unpopulated**:
* **5V VCC Power Gate OFF (0.0 mA):** Prevents feeding incorrect voltage or current to an unknown device.
* **Audio DSP Mute (-96 dB):** Prevents audio popping or squeal.
* **Optocouplers High-Z (OFF):** Inhibits unintended button presses.
* **DLE Bonus = 0:** Zero weight in group election.
* **Controlled Soft-Release:** Only once confirmed in the WebApp (or matched in local flash), the controller executes a 50 ms soft-start ramp to power the module.

---

## 7. WebApp Workflow: Automatic Recognition & Profile Assignment

When new cartridge hardware is plugged in, the PWA launches an automated onboarding dialog:

```
┌─────────────────────────────────────────────────────────────┐
│ 🧩 NEW CARTRIDGE DETECTED!                                  │
├─────────────────────────────────────────────────────────────┤
│ Detected Bay:           Pod 1 (Left Frame)                  │
│ 1-Wire Silicon UID:     01:A2:3B:4C:5D:6E:7F:8A             │
├─────────────────────────────────────────────────────────────┤
│ This cartridge hardware is not yet linked to a profile.     │
│ Which intercom or radio is installed in this sled?          │
│                                                             │
│ Hardware Profile:  [ 🔵 Sena 50S / 50R / SRL3 (K1)      ▼ ] │
├─────────────────────────────────────────────────────────────┤
│ [ Assign Later ]            [ Assign & Save Profile ]       │
└─────────────────────────────────────────────────────────────┘
```

1. **Automatic Scan:** ESP32-S3 polls both 1-Wire ports every 2 seconds (`task_cartridge_manager`). Valid CRC8 and Family Code `0x01` triggers a BLE telemetry packet with the 64-bit UID to the WebApp.
2. **Assignment Modal:** The WebApp checks the UID against `/profiles/mapping.json` (or PWA `localStorage`). If unmapped, `#uuid-detect-modal` pops up automatically.
3. **Model Selection:** The rider selects their headset model from the dropdown list.
4. **Persistent Mapping:** The configuration `{"<UID>": "<profile_id>"}` is permanently saved to LittleFS and browser IndexedDB.
5. **Zero-Touch Reconnection:** Subsequent insertions into either pod bay automatically re-apply all gains and pulse timings without prompting.

### 7.1 Dynamic Profile Updates & JSON Merge Pipeline
When a manufacturer updates firmware (e.g. Sena upgrading from Mesh 2.0 to Mesh 3.0 or Cardo DMC Gen2 enhancements), OpenMotorBridge adapts via an automated **JSON merge pipeline**:

```
┌─────────────────────────────────────────────────────────────┐
│                 JSON PROFILE MERGE PIPELINE                 │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Base Vendor Profile       │ 2. Custom Rider Offsets      │
│    (e.g., sena_apex_v3.json) │    (Gains, Ducking Levels)   │
├──────────────────────────────┴──────────────────────────────┤
│                             ▼                               │
│ 3. Merged Live Profile in LittleFS Flash                    │
│    (Updated Opto Timings + Preserved Personal Settings)     │
└─────────────────────────────────────────────────────────────┘
```

* **Phase 1 (Base Parameters):** New optocoupler pulse durations, button timings, and DLE bonus ratings are loaded from the vendor release.
* **Phase 2 (User Settings Preservation):** Rider customizations (e.g. $+2{,}0\,\text{dB}$ mic gain, $-12\,\text{dB}$ nav ducking) override default values.
* **Phase 3 (Hot Reload):** The Central Box applies merged settings dynamically to the ES8388 codec and TLP222A pulse engine without requiring a reboot.

### 7.2 Hardware Upgrades (Replacing Headset in Existing Sled)
When upgrading an intercom inside an existing sled (e.g. replacing a Sena 20S with a Sena 60S Mesh 3.0 Wave):
1. **Persistent Silicon UID:** The DS2401 chip on `PCBA 03` retains its unique 64-bit ID.
2. **Dashboard Re-assignment:** In the **"🧩 Cartridges & DLE"** tab, the rider selects the new model from the dropdown.
3. **Automatic Overwrite:** The mapping `{"<UID>": "sena_60s"}` updates immediately in flash and browser storage.
4. **Instant Recognition:** Subsequent boot cycles immediately load the new profile with updated timings and higher DLE bonus (+60 pts).
5. **Ground-Truth Re-Sync (`🔄 Sync`):** The rider can verify flash mappings at any time with a single click.

---

## 8. Recommended Pod Configuration Scenarios

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   RECOMMENDED POD CONFIGURATION SCENARIOS                   │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ Setup Category        │ Pod 1 (Left)            │ Pod 2 (Right)             │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⭐ **OMB Recommendation**│ **Sena SPIDER X Slim**│ **Cardo Packtalk Edge**   │
│   (Price-Performance  │ (Mesh 3.0 Direct-DC,K2a)│ (DMC Gen2 Air-Mount, K4)  │
│    Leader & Reference)│ (DLE +60 pts, ~210 €)   │ (DLE +60 pts, ~320 €)     │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💎 **High-End Leader**│ **Sena 60S / Apex**     │ **Cardo Packtalk Edge**   │
│    (350 – 550 €)      │ (Mesh 3.0 Wave, K1)     │ (DMC Gen2 Air-Mount, K4)  │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⚖️ **Lean & Modern**  │ **Sena SPIDER X Slim**  │ **Cardo Freecom 4x / Bold**│
│    (180 – 260 €)      │ (Mesh 3.0 Direct-DC,K2a)│ (Live Intercom/DMC, K5/K6)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💰 **Budget Entry**   │ **Sena MeshPort Blue**  │ **IP67 Blank Cartridge**  │
│    (80 – 140 €)       │ (or Sena 20S/SF, K3)    │ (Slot unpowered/disabled) │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 🏔️ **Adventure/Offroad**│ **Sena Apex / 50S**   │ **Midland G9 Pro PMR446** │
│    (220 – 320 €)      │ (Mesh 3.0, K1)          │ (Analog Radio Gateway, K7)│
└───────────────────────┴─────────────────────────┴───────────────────────────┘
```

### 8.1 Why the Sena SPIDER X Slim is Our Official Reference Recommendation for Pod 1

The **Sena SPIDER X Slim** (Class 2a – `sena_spider_x.json`) is the **official primary recommendation** of the OpenMotorBridge project for Satellite Pod 1. It combines all required next-generation wireless capabilities with ideal mechanical and electrical characteristics for motorcycle pod cartridge operation:

1. **Full Mesh 3.0 & Wave Parity (Future-Proof Without Compromise):**
   * Delivers the exact same state-of-the-art mesh architecture as Sena's costly flagships (Sena 60S / Apex), featuring native **Mesh 3.0 & 2.0**, Wave Intercom, and Bluetooth 5.3.
   * Supports up to 32 participants in mesh (Multi-Channel Open Mesh Channels 1–6) and receives the **full DLE Score Bonus of +60 points**.

2. **Free from Useless Helmet Overhead (Lean Transceiver Design):**
   * Traditional flagship helmet headsets (like the 60S or 50S) are burdened with costly rotary dials (jog dials), helmet LED spotlights, LCD status panels, and permanently integrated speaker/mic wiring looms — components that are completely useless inside an enclosed pod on a motorcycle, consume unnecessary space, and introduce mechanical failure points.
   * The SPIDER X Slim is radically streamlined to pure core essentials: With ultra-compact dimensions of $74.5 \times 31 \times 16\,\text{mm}$ and a featherweight of just **$23.2\,\text{g}$**, it fits perfectly inside the cartridge bay.

3. **Direct-DC & Integrated 3-Port Cable Whip (No Pogo-Pin Cradle Needed!):**
   * **The Greatest Design & Practical Breakthrough:** According to the official Sena documentation (*SPIDER X Slim User Guide v1.0.0*, page 6), the main unit routes all three fundamental interfaces through rugged factory micro-connectors on a flexible cable whip:
     * **Port ⑧: Battery Pack Connector (Direct-DC):** 2-wire line for permanent $3.85\,\text{V}$ regulated DC directly from the carrier PCB (no LiPo battery inside the pod, zero fire hazard, zero aging!).
     * **Port ⑨: Microphone Jack:** Direct injection of audio signals from the ES8388 Audio Codec / DAC on the carrier PCB (no external mic capsule needed).
     * **Port ⑩: Speaker Jacks:** Direct line-level audio capture of incoming mesh chatter into the Line-In / ADC of the ES8388 Codec.
     * *(Additionally: Port ⑦ USB-C on the front face for optional service / OTA maintenance).*
   * **Mechanical Milestone (Zero Pogo Pins):** It requires **no bulky, failure-prone clamp cradle with spring-loaded pogo pins** (unlike Sena 50S/60S or Cardo Packtalk)! Pogo pins suffer from contact bounce, contact resistance, and corrosion under motorcycle vibrations ($> 20\,\text{g}$) and moisture. With the SPIDER X Slim, all three connectors plug directly and securely via a passive adapter harness into the 6-pin JST-SH header `J2` of the OMB cartridge carrier board (PCBA 03).
   * **100% Plug & Play, Zero Soldering, Full Warranty Retention:** The OEM enclosure remains completely unopened and undamaged. The module is simply taken out of the retail packaging, placed into the 3D-printed sled, and plugged in.
   * **Clean Automatic Power Cycling:** Boots reliably with motorcycle ignition (KL15) and powers down cleanly when switched OFF.

4. **Unbeatable Price-to-Performance Ratio:**
   * At a typical retail street price of **~180 – 240 €**, the SPIDER X Slim delivers identical DLE network performance (+60 pts) to the €450 – €550 flagship Sena 60S — offering over 50% cost savings for builders!

---

## 9. Proximity & Standstill Privacy Mute (Local Conversation Mode at Intermediate Stops)

### Problem in Group Mesh Riding
When two group riders pull up next to each other at a red traffic light, a toll booth, or a roadside turnout and flip open their modular helmet visors to talk face-to-face:
1. **Acoustic Echoes & Feedback Loops:** Rider A's microphone captures Rider B's voice with a $15\dots 30\,\text{ms}$ latency, creating a jarring, disorienting echo inside their helmet speakers.
2. **Channel Congestion for the Entire Group:** The other 6–10 riders in the group (who may be 500 meters ahead or trailing behind) are forced to listen to the private side conversation over the mesh.

### Intelligent Near-Field Privacy Mute
OpenMotorBridge solves this challenge through a fully automated **Proximity Mute Logic**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   PROXIMITY & STANDSTILL PRIVACY MUTE LOGIC                            │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [1. REAL-TIME SENSOR EVALUATION]
  ├── Condition 1: Motorcycle is stationary (CAN vehicle speed v = 0.0 km/h)
  └── Condition 2: Companion motorcycle in immediate proximity (< 3.0 m)
                   Detected via 2.4 GHz ESP-NOW mesh signal strength (RSSI > -45 dBm)

  [2. ACOUSTIC TRANSITION (Automatic)]
  ├── OpenMotorBridge MUTES the microphone uplink to the wide-area group mesh
  ├── Discreet acoustic confirmation tone in helmet (dual-tone "Local Mode Active")
  └── Riders communicate naturally through open visors face-to-face!

  [3. AUTOMATIC GROUP MESH RE-ENGAGEMENT]
  ├── Option A: Motorcycle accelerates away (v > 8.0 km/h)
  └── Option B: Rider taps handlebar PTT button (< 400 ms) ➔ Mesh immediately live!
```

