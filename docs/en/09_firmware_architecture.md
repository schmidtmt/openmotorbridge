# 09 - Firmware Architecture, FreeRTOS Tasks & Rollback-OTA

*Note: All CAD, electronic, and block diagrams reflect the standardized v10.0 node architecture (PCBA 01 through 10).*

This document specifies the system-wide firmware architecture of OpenMotorBridge v10.0 (Native USB-PD & Edge-AI Generation): the multi-core allocation of the **`ESP32-S31-WROOM-1U`** host MCU on the Central Box (`PCBA 01`), the **`ESP32-S31-WROOM-1U` + `ESP32-E22`** Front Node (`PCBA 05`), the deterministic **4-Wire Automotive USB 2.0 & 12V Backbone (`+12V_BUS`, `GND`, `D+`, `D-`, latency < 0.2 ms)** across the `USB2517I` 7-port hub to all satellite nodes, the **Dual-Power Input Engine** (12V DTM `J1` via `LM5164-Q1` & 5V USB-C Service Input `J3` via `LM66100` ideal-diode OR-ing), the **5-Gesture Trigger Engine** for symmetrical under-perch mirror pods (`PCBA 05C`), the SPIFFS/LittleFS profile engine, and the **Dual-Bank Rollback-OTA & Central Bus-DFU architecture**.

---

## 1. Multi-Core & Multi-MCU System Architecture

In v10.0, the overall system is standardized onto a ruggedized, shielded **4-wire Automotive 12V & USB 2.0 bus**. All data, audio, and control links between Central Box and external nodes operate over wire with deterministic latency ($< 0.2\,\text{ms}$) and local USB-PD regulation (up to 60 W at Front Node via `SW3526`, 30 W in Pods via `SW3516H`):

```
+----------------------------------------------------------------------------------------+
|                        FIRMWARE CONTROLLERS IN CONCERT (v10.0)                         |
+------------------------------------------------------+---------------------------------+
| 1. CENTRAL BOX (ESP32-S31-WROOM-1U, PCBA 01)          | 2. FRONT NODE (ESP32-S31+E22, PCBA 05)|
+------------------------------------------------------+---------------------------------+
| * Core 0: USB2517I 7-Port Host Engine, SX1262 LoRa   | * Core 0: USB Backbone Client,  |
|   868 MHz, Quad eFuse, BLE, Pod & Bus-DFU Dispatcher |   SAM-M10Q GNSS, CAN, SW3526 PD |
| * Core 1: 48 kHz SIMD Audio-DSP, Raised-Cosine       | * Core 1: Knowles Wind-DSP,     |
|   Ducking, AGC, Qualcomm QCC3084 BT 5.4 Hub          |   OLED UI, 5.9 GHz V2X Co-Proc  |
+------------------------------------------------------+---------------------------------+
| 3. SATELLITE PODS (ESP32-C6-MINI-1U, PCBA 03)         | 4. REAR RADAR (ESP32-C6-MINI-1U, PCBA 08)|
+------------------------------------------------------+---------------------------------+
| * USB 2.0 Device & SW3516H 30W USB-PD Controller     | * Wheeltec MR20 77-GHz mmWave   |
| * PCM2912A USB Audio Codec / OMM_DETECT Auto-Sense   | * 20 Hz Tracking Vectors via    |
| * OptoMOS PTT Keying & Dual AO3400A Cold-Start Pulse |   USB-CDC / WS2812B Strobe LED  |
+------------------------------------------------------+---------------------------------+
```

### 1.1 Central Box `ESP32-S31-WROOM-1U` Host Controller Core Allocation (`PCBA 01`)

#### CORE 0 (Communication, Telemetry, 4-Wire USB Backbone & Power Management):
- **Automotive USB Backbone Host Engine (`uwb_vehicle_backbone.cpp`):** Manages the USB 2.0 High-Speed connection across the onboard `USB2517I-JZX` 7-port hub to Front Node (`PCBA 05`), saddlebag pods (`PCBA 03`), and Rear Radar (`PCBA 08`). Receives handlebar PTT and gesture events ($< 0.15\,\text{ms}$), Knowles MEMS acoustic noise readings, 10 Hz Multi-GNSS packets, and pod telemetry.
- **Dual-Power Input Monitoring:** Monitors generation of the 5V system rail (12V vehicle net `J1` Deutsch DTM06-6S via `LM5164-Q1` buck converter and 5V USB-C Service Input `J3` via `LM66100` ideal diode). Enables benchtop diagnostics and flashing of the Central Box over a single USB-C cable (note: flashing satellite nodes via Central Bus-DFU requires 12V at `J1` or local satellite power because `U12` is powered from `KL30_IN`).
- **Staggered Power Sequencing (`power_sequencer.cpp`):** Controls the 4-channel automotive smart switch **`TI TPS4H160-Q1` (`U12`, `GPIO 13..16`)** on `PCBA 01` to eliminate inrush current spikes:
  - $T = 0\,\text{ms}$: Central Box (`PCBA 01`) and Front Node (`PCBA 05`, `GPIO 15`) boot synchronously upon ignition ON (`KL15`).
  - $T = 200\,\text{ms}$: Pod 1 (`GPIO 13`, +12V via eFuse with soft-start ramp).
  - $T = 350\,\text{ms}$: Pod 2 (`GPIO 14`, +12V via eFuse with soft-start ramp).
  - $T = 500\,\text{ms}$: Rear Radar (`GPIO 16`, +12V switched on Branch 4).
- **LoRa 868 MHz Mesh Engine (`sx1262_lora_engine.cpp`):** Direct SPI link (`GPIO 10..12`, `CS=9`, `BUSY=3`, `DIO1=8`) to the onboard Semtech SX1262 transceiver on `PCBA 01` (24/7 UPS-buffered for theft sentry and group telemetry).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth connection for the PWA dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatic state machine bridging radio shadows between Sena Mesh, Cardo DMC, OMM 2.4 GHz, 5.9 GHz V2X, and LoRa 868 MHz emergency beacon.
- **WebDAV TLS 1.3 Client (`webdav_uploader.cpp`):** Asynchronous upload of GPX tour recordings to Nextcloud/Synology in **Garage Post-Ride Sync Mode** upon ignition OFF (`KL15 = LOW`).
- **SDIO Logging Task (`sdio_ring_buffer.cpp`):** 4-bit high-speed SD card logger (`GPIO 33..39`) with rolling BGH privacy auto-purge (`esp_vfs_fat_info`) and SHA-256 chain + hardware eFuse signature.
- **ADR-EKF Filter (`adr_ekf_filter.cpp`):** 15-State sensor fusion fusing 10 Hz Multi-GNSS telemetry (from Front Node via USB) and onboard Bosch BMI270 6-axis IMU (`I2C 0x68`) for uninterrupted navigation through tunnels.

#### CORE 1 (Realtime Edge-AI Audio DSP & Qualcomm QCC3084 Hub @ Highest Priority):
- **128-bit SIMD Vector Accelerator:** Real-time filtering of wind noise, acoustic transients, and engine rumble, plus acoustic scene classification directly on silicon.
- **Qualcomm QCC3084 Dual-Helmet Audio Hub (`bluetooth_audio_manager.cpp`):** Controls the dedicated QCC3084 BT 5.4 Audio SoC (`U9` on `PCBA 01`) via UART (GAIA/AT) for hardware-accelerated Dual-A2DP (aptX HD / Adaptive) to rider and pillion helmets, LE Audio Auracast, and synchronous HFP 1.8 Wideband voice channel.
- **I2S Audio DMA Receiver & Transmitter:** Ultra-low-latency streaming via ES8388 Audio Codec (`I2C 0x10`) and Qualcomm QCC3084 ($f_s = 48\,\text{kHz}, 24\,\text{bit}$, double-buffer of 128 samples = $2.67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Click-free, continuously differentiable audio attenuation during intercom announcements or radar alerts.
- **Dynamic AGC Volume Scaling:** Smooth automatic scaling of helmet output volume based on Front Node aerodynamic wind noise.
- **Lookahead Brickwall Limiter:** Prevents digital clipping exceeding $0\,\text{dBFS}$.

---

## 2. Deterministic 4-Wire Automotive Bus (`usb_vehicle_backbone.cpp`)

All data, control, and audio links in the vehicle network employ the shielded 4-wire Automotive USB-PD & USB 2.0 bus (`VBUS`, `GND`, `D+`, `D-`):
- **Zero RF Congestion & Zero De-Sensing:** The physical wired bus completely eliminates UWB or RF backbone cross-talk in the cockpit or saddlebag flanks.
- **Deterministic Latency:** Bus transfer times $< 0.2\,	ext{ms}$ over native USB 2.0 interrupt and bulk endpoints.
- **Automotive USB-PD:** Up to 60 W charging power per branch with dynamic power balancing.

```cpp
enum UsbBackbonePktType : uint8_t {
    // --- Node Management & System Heartbeat ---
    USB_DESC_NODE_ANNOUNCE     = 0x01,  // Boot Handshake: Node Type (Front, Pod 1/2, Radar), UID, FW Version
    USB_PKT_NODE_HEARTBEAT     = 0x02,  // 1 Hz Heartbeat: Uptime, VBUS Voltage, Current Draw, Bus Status
    USB_PKT_GESTURE_EVENT      = 0x03,  // 5-Gesture Handlebar Trigger (< 0.15 ms Latency): Short, Double, Triple, Long, Hold

    // --- Consolidated Telemetry (10 Hz Frame) & Peripherals ---
    USB_PKT_FRONT_TELEMETRY    = 0x04,  // Consolidated 10 Hz Frame: GNSS PVT + Wind-RMS + TMP117 + Lux + CAN
    USB_PKT_WIRELESS_CP_AA_STAT= 0x05,  // COTS CarPlay / Android Auto Bridge Status, Current Draw, Auto-Café Timer

    // --- Control Commands & System Synchronization ---
    USB_CMD_POWER_CYCLE        = 0x10,  // Central Box -> Front Node / Pods: Cold Boot & Power Gating
    USB_CMD_CONFIG             = 0x11,  // Central Box -> Satellites: Ignition Sync & Sleep State
    USB_CMD_PAIRING_REQUEST    = 0x12,  // Pairing routine upon SW1 button press (60s window)

    // --- Pod Control & Interface Protocol (Pods 1 & 2) ---
    USB_DESC_POD_ANNOUNCE      = 0x20,  // Handshake: Hardware Class, Model ID, UID, Status, USB-PD Profile
    USB_CMD_POD_CONTROL        = 0x21,  // Central Box -> Pod: PTT Trigger, BLE Command, Audio Routing
    USB_PKT_POD_ACK            = 0x22,  // Pod -> Central Box: Execution Acknowledgment & Status

    // --- Digital USB Audio Class Backbone (Bidirectional, 48 kHz / 24-Bit PCM) ---
    USB_PKT_AUDIO_STREAM_DOWN  = 0x24,  // Central Box -> Pods: Master Mix to Headsets (Mic + Navigation + TTS)
    USB_PKT_AUDIO_STREAM_UP    = 0x25,  // Pods -> Central Box: Intercom Spk-Out / Helmet Audio to Central Box
    USB_PKT_AUDIO_MEDIA_UP     = 0x26,  // Front Node -> Central Box: Music / Navigation Prompts

    // --- Radar 2.0 (PCBA 08 via CAN/UART): Pre-filtering & LED Macro Control ---
    USB_PKT_RADAR_TARGETS      = 0x30,  // 20 Hz Pre-filtered Target List (TTC, Distance, Azimuth) + URGENT Flag
    USB_PKT_RADAR_LED_CMD      = 0x31,  // Central Box -> Radar: Macro Command (Idle, Warning, Prio-1 Strobe)

    // --- Zero-Disassembly WebUSB DFU Flashing ---
    USB_PKT_FW_UPDATE_PUSH     = 0x50,  // Host -> Nodes: Block-wise Firmware Update via USB 2.0
    USB_PKT_FW_UPDATE_DONE     = 0x51   // Nodes -> Host: Flash Acknowledgment / Reboot Ready
};
```

### 2.1 Handlebar PTT Latency Budget
1. **Handlebar Switch Closure:** $12\,\mu	ext{s}$ hardware Schmitt-trigger debouncing at Front Node.
2. **Front Node ESP32-S3 GPIO Interrupt:** $15\,\mu	ext{s}$ ISR execution time & gesture detector.
3. **USB 2.0 Interrupt Transfer (Front -> Central Box):** $60\,\mu	ext{s}$ transit time across shielded 4-wire bus.
4. **Central Box ESP32-S31 Core 0 Dispatcher:** $20\,\mu	ext{s}$ event parsing & PTT routing.
5. **Pod Interface OptoMOS / Digital Audio:** $< 10\,\mu	ext{s}$ switching time of OptoMOS relay `CPC1017N` or digital USB audio stream.
* **Total Glass-to-Glass Latency:** **$pprox 0.12\,	ext{ms}$** (over 80 times faster than the human perceptual threshold of $10\,	ext{ms}$).

### 2.2 Dual-Power Input Management & Benchtop Testing
- **Active Reverse-Polarity & Back-Feed Protection (Zero Back-Feed):**
  - **12V Vehicle Net Path (`J1` Deutsch DTM-6):** A **TI `LM5164-Q1`** (`U1`) 100V synchronous step-down buck converter efficiently generates `VCC_5V` from the 12V vehicle supply. Transients are clamped primarily by an `SMBJ33CA` TVS diode (`D2`).
  - **5V Service & Diagnostic Path (`J3` USB-C):** A **TI `LM66100`** (`D3`) ideal-diode completely isolates the 5V USB feed (`USBC_VBUS`) from the internal `VCC_5V` rail, preventing any back-feed into the diagnostic laptop or programmer.
  - **3.3V Logic Rail:** Generated downstream by the ultra-low-IQ LDO **`U11` (`TPS7A0533`)**.
- **Two Distinct Operating Modes:**
  - **1. Vehicle & Full Testbench Mode (12V at `J1`):** Full operational power. All four `TPS4H160-Q1` Smart Switch branches (`U12` on `J6`: Front Node 60W USB-PD via `SW3526`, Saddlebag Pods 30W USB-PD via `SW3516H`, Rear Radar, 12V solenoids) as well as the `BQ24075` UPS charger and internal logic are fully powered. In this mode, all satellite nodes can be flashed and operated synchronously via **Zero-Disassembly Bus-DFU**.
  - **2. Workbench & Diagnostic Mode (5V via `J3` USB-C):** Powers the 5V and 3.3V logic of the Central Box (`ESP32-S31`, `USB2517I` 7-port hub, DSP, LoRa, IMU) directly. Allows host MCU flashing, sensor calibration, and system diagnostics on the desk from standard 5V USB power or PC USB ports without a 12V bench power supply. **Important P01 Restriction:** Because the quad smart switch `U12` is connected directly to `KL30_IN` (12V), peripheral branches on `J6` are not energized in pure USB-C mode. To flash or test satellites on the workbench via Bus-DFU, either 12V must be supplied to `J1` or the satellite must be powered via its local USB-C port.

---

## 3. BLE GATT Server Architecture (`ble_service_server.cpp`)

The system exposes standardized Bluetooth SIG services as well as vendor-specific characteristics for the PWA dashboard:

| Service UUID | Characteristic UUID | Properties | Function & Data Payload |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Audio RMS & Env)       | **`0x2A37`** | Notify | Knowles MEMS wind noise level (50 Hz, dB(A)) & TMP117 temperature. |
| **`0x180A`** (Device Information)    | **`0x2A24`** | Read   | Hardware revision (`OMB-v10.0`), Serial, Firmware build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Control commands: `0x01` Profile switch, `0x02` Reset, `0x09` Pod Control Opcode. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetry stream: Lean-Angle (Roll/Pitch), Speed, TTC, Radar warning. |
| **`0xFFE0`** (Pod Status)            | **`0xFFE3`** | Notify/Read | Pod status 1 & 2: 64-bit UID, hardware class, USB-PD profile, status. |

---

## 4. Universal Group Split Fallback Engine (`group_split_rescue_engine.cpp`)

During tours across mountainous terrain or dense forests, 2.4 GHz intercom connections (Sena Mesh / Cardo DMC) drop beyond approximately $800\dots 1200\,	ext{m}$ once line-of-sight is obstructed. The integrated **Group Split Fallback Engine** in v10.0 prevents groups from fragmenting:

```
               GROUP SPLIT FALLBACK ENGINE STATE MACHINE
+-----------------------------------------------------------------------------+
| 1. NORMAL STATUS: LINE-OF-SIGHT CONNECTED                                   |
|    * Pod 1 (Sena Mesh) & Pod 2 (Cardo DMC) fully active                     |
|    * HD-Audio stream in helmet; LoRa transmits periodic heartbeats (0.2 Hz) |
+-----------------------------------------------------------------------------+
|                                     v (Connection loss > 15 s)              |
| 2. RESCUE LEVEL 1: OMM 2.4 GHz CHANNEL-HOPPING MESH                         |
|    * If OMM module installed: Boosts TX power to +20 dBm                    |
|    * Searches for relay nodes among adjacent group members                  |
+-----------------------------------------------------------------------------+
|                                     v (Connection loss > 45 s)              |
| 3. RESCUE LEVEL 2: 868 MHz LoRa MESH (SX1262) TELEMETRY & TEXT              |
|    * Range up to 15 km (LOS) or 3-5 km in mountains                         |
|    * Automatically transmits GPS position, bearing, distance & arrow vector |
|    * Displays "Group ahead: 2.4 km NW" on CarPlay / PWA Dashboard           |
+-----------------------------------------------------------------------------+
|                                     v (Connection loss > 120 s)             |
| 4. RESCUE LEVEL 3: PMR446 ANALOG VOICE FALLBACK (OPTIONAL)                  |
|    * Triggers automated voice broadcast ping on Midland radio pod           |
|    * Broadcasts synthesized TTS location announcement over PMR446 channel   |
+-----------------------------------------------------------------------------+
```

---

## 5. Pod Control (PCBA 03) & Symmetrical 5-Gesture Mirror-Pod Engine

### 5.1 Dynamic Pod & Model Identification (Hardware Descriptors & Profile Matrix)
To flexibly interface modern OEM communicators without brittle mechatronic solenoids, `PCBA 03` uses a pure digital and electrical identification scheme:
1. **USB 2.0 Descriptor Handshake:** On boot, the carrier board reports its 16-bit model ID, hardware class, and 64-bit UID natively over USB 2.0 to the Central Box.
2. **Harness Auto-Sense:** Automatically identifies whether a Sena SPIDER X Slim (micro-cable whip at `J_AUDIO_PWR`), Cardo Packtalk Edge (Air-Mount & USB-C port), OMM UCS 2.4 GHz module (USB Audio Class), analog radio (Midland PMR446), or hermetic dry-box is installed.

| Model ID | Base Class | Model Name | Physical Interface | Control & Audio Characteristics |
| :---: | :---: | :--- | :--- | :--- |
| **`0x0101`** | Class A | **Sena SPIDER X Slim** | Micro-cable whip at `J_AUDIO_PWR` | 3.85V Direct-DC, ES8388 Line-In/Out, BLE GATT |
| **`0x0102`** | Class A | **Sena +Mesh Adapter** | Internal USB-C charging port | Pure Bluetooth/Audio gateway; USB-PD charging |
| **`0x0201`** | Class B | **Cardo Packtalk Edge / Pro**| Air-Mount & USB-C charging port | DMC Gen2, USB-PD charging ("Charge while Riding") |
| **`0x0301`** | Class C | **OMM UCS 2.4 GHz Module** | Native USB 2.0 Port | Full-digital USB Audio Class 2.0, IPv6-Mesh |
| **`0x0401`** | Class D | **Midland PMR446 (G9 Pro)** | 2-Pin dual jack pigtail | OptoMOS PTT keying (`CPC1017N`), galvanically isolated |
| **`0x0000`** | Class 0 | **Dry-Box / Luggage Bay** | Zero audio peripherals | Pure 30W/60W USB-PD charge port for phone/powerbank |

### 5.2 Symmetrical Dual Under-Perch Mirror Pods & 5-Gesture Engine (`PCBA 05B`)
The two identical mirror pods (`PCBA 05B`) mounted under the mirror perches provide tactile thumb control and bilateral Blind Spot Detection (BSD):
* **5 Gesture Triggers:** Each switch autonomously detects `SHORT_CLICK`, `DOUBLE_CLICK`, `TRIPLE_CLICK`, `LONG_PRESS`, and `HOLD_GATE`.
* **100% Free Button Mapping:** Via the PWA dashboard, each gesture is freely assignable to any action in the OMB Action Catalog (e.g. Push-to-Talk, Voice Assistant Siri/Google, Waze 1-Click Hazard Pin, Action-Cam Tags for Insta360/GoPro/DJI, Radar Mute, Garage Door via BLE).

---

## 6. FreeRTOS Task Architecture & Scheduling Matrix (Central Box & Front Node)

The overall system orchestrates specialized tasks across the two host microcontrollers:

| Task Name | MCU / Core | Priority | Stack | Trigger / Rate | IPC / Interface | Responsibility & Function |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | Central Box (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Zero-latency I2S audio mix, SIMD AI noise filter, ducking & AGC. |
| **`usb_backbone_task`**| Central Box (Core 0) | **22** | 6 KB | USB Host IRQ / Event | FreeRTOS StreamBuffer | 4-Wire Automotive USB 2.0 host engine for Front Node & Pods (< 0.2 ms). |
| **`qcc3084_hub_task`**| Central Box (Core 1) | **21** | 4 KB | UART DMA ISR / Queue | FreeRTOS Queue / UART1| QCC3084 Supervisor: aptX HD Dual-A2DP, Auracast & HFP Call Handling. |
| **`lora_mesh_task`**  | Central Box (Core 0) | **20** | 4 KB | SX1262 IRQ / Timer  | FreeRTOS Queue        | 868 MHz LoRa mesh protocol, theft sentry & Group Split Rescue. |
| **`gesture_engine_task`**| Front Node (Core 0)| **24** | 2 KB | GPIO Edge ISR       | USB TX Queue          | Processes mirror pod switches Left/Right, generates 5 gestures (< 0.15 ms). |
| **`radar_task`**      | Central Box (Core 0) | **16** | 4 KB | CAN / UART DMA ISR  | FreeRTOS Queue        | 20 Hz Radar target vectors from Wheeltec MR20; TTC computation & Prio-1 ducking. |
| **`adr_ekf_task`**    | Central Box (Core 0) | **15** | 4 KB | 50 Hz Timer         | I2C / CAN Buffer      | 15-State Kalman filter (SAM-M10Q GNSS + BMI270 IMU + CAN speed). |
| **`power_mgmt_task`** | Central Box (Core 0) | **14** | 2 KB | Boot-Event / Timer  | GPIO / I2C Power      | Automotive Smart Switch (U12 TPS4H160-Q1), LM5164-Q1 / LM66100 monitoring, staggered power start. |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA dashboard (GATT services `0x180D`/`0x180A`/`0xFFE0`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringbuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO blackbox logging with HMAC-SHA-256 integrity seal. |
| **`webdav_sync_task`**| Central Box (Core 0) | **3**  | 8 KB | Graceful Shutdown   | LwIP TLS 1.3          | Automatic GPX tour upload via home Wi-Fi upon ignition OFF. |
| **`front_gnss_task`** | Front Node (Core 0)  | **20** | 4 KB | 10 Hz I2C DMA       | J12 Qwiic / USB TX    | u-blox SAM-M10Q UBX-NAV-PVT parsing, TMP117 Temp & OPT3001 Lux. |
| **`front_mems_task`** | Front Node (Core 1)  | **18** | 4 KB | 48 kHz DMA          | Vector-DSP Filter     | Knowles I2S digital microphone A-weighting & RMS tracking via Xtensa DSP. |
| **`front_can_task`**  | Front Node (Core 0)  | **16** | 4 KB | TWAI Interrupt      | CAN Message Queue     | Reads cockpit CAN (if J2 connected), CPC1017N auto-termination. |
| **`front_pwr_task`**  | Front Node (Core 0)  | **10** | 2 KB | 10 Hz Timer         | GPIO Load Switch      | SW3526 USB-PD monitoring, TPS2051B cold restart (2.5s), auto-off. |

---

## 7. LittleFS Pod Profile Engine & JSON Storage Schema

Upon pod connection and USB descriptor announcement (`USB_DESC_POD_ANNOUNCE`), the pod manager loads the configuration from `/storage/profiles/<UID>.json`:

```json
{
  "profile_schema": 3,
  "uid": "01:A4:7B:3F:00:00:00:1E",
  "device_name": "Sena SPIDER X Slim Direct Cradle",
  "hardware_class": "0x01",
  "power": {
    "vcc_enabled": true,
    "usb_pd_profile": "9V_3A",
    "direct_dc_mv": 3850,
    "max_current_ma": 600,
    "soft_start_ms": 50
  },
  "audio": {
    "input_gain_db": 6.0,
    "output_gain_db": 0.0,
    "ducking_priority": 3,
    "auto_agc_enabled": true,
    "clip_limit_dbfs": -0.5
  },
  "direct_interface": {
    "enabled": true,
    "opto_key_mode": "sena_spider_mesh",
    "ble_gatt_control": true
  },
  "mesh_routing": {
    "dle_bonus_points": 60,
    "protocol_family": "sena_mesh_3"
  }
}
```

* **Zero-Trust Fallback (`disabled.json`):** On unknown UID, short-circuit, or empty bay, the VBUS MOSFET remains disabled (`vcc_enabled: false`), the audio codec is muted to `-96 dB`, and DLE score falls to `0`.

---

## 8. Modular Hardware Topology & Graceful Degradation

OpenMotorBridge is designed as a **decoupled, fault-tolerant modular building block**. No subsystem can prevent the Central Box from operating:

| Configuration | Installed Components | System Behavior & Graceful Degradation |
| :--- | :--- | :--- |
| **Tier 1: Minimal Core** | Central Box only<br>*(No Front Node)* | * **Audio Bridge & Intercoms fully operational:** Pod 1 & 2 mix with zero latency via 4-wire bus.<br>* **LoRa 868 MHz Mesh active:** Direct UPS-buffered 24/7 theft sentry & tracking.<br>* **CAN-Bus active:** Speed, RPM & BCM telemetry via Cable 1 (DTM-6 pins 4/5) under seat.<br>* **IMU active:** Bosch BMI270 provides lean angle, pitch & vibration sensing.<br>* **ADR-EKF:** Operates in pure Dead Reckoning mode supported by IMU & wheel speed.<br>* **USB Host:** Passively monitors ports for hotplug events. |
| **Tier 2: Full System with Front Node** | Central Box + Front Node | * All Tier 1 features + deterministic 4-wire USB backbone (< 0.2 ms).<br>* u-blox SAM-M10Q Multi-GNSS with 10 Hz PVT fix & precision time synchronization.<br>* TI TMP117 black ice warning ($\pm 0.1\,^\circ	ext{C}$) & TI OPT3001 ambient light sensor.<br>* 4-Port USB Hub & Dual 20W USB-PD fast charger in cockpit.<br>* Ottocast Watchdog & automatic ignition power-gating.<br>* Symmetrical Under-Perch Mirror Pods (< 0.15 ms) with 5-gesture engine and Knowles dynamic acoustic wind AGC. |
| **Tier 3: Rear Radar Option** | Central Box + Front Node + Radar | * All Tier 2 features + Wheeltec MR20 77 GHz (PCBA 08).<br>* 4-wire power & high-speed data from 16-Pin Periphery Header (Branch 4).<br>* Acoustic alert pings in helmet, optical alert wings & mirror BSD LEDs.<br>* Automatic action-cam bookmarks upon critical radar TTC (< 2.5 s). |

### 8.1 Protection Mechanisms Against Missing Data (Zero-Crash Policy)
1. **Asynchronous Non-Blocking Interfaces:** Communications via USB, LoRa (SPI), and Radar use FreeRTOS timeouts (`pdMS_TO_TICKS(50)`). There are **zero blocking `while(1)` polling loops**.
2. **Dynamic DLE Capabilities (`omm_get_capabilities_vector`):** The Central Box advertises only those hardware flags in mesh packets that physically respond.
3. **Sensor-Fusion Autonomy (`adr_ekf_filter.cpp`):** If GNSS is lost, the EKF transitions immediately to **Dead Reckoning** supported by IMU and wheel speed.
4. **Fault-Tolerant Audio Mixer (`audio_dsp_pipeline.cpp`):** If the Front Node Knowles MEMS is missing, AGC defaults to nominal unity gain (`1.0f`).

---

## 9. Build, Flash & HIL Verification Guide

For step-by-step ESP-IDF v5.5+ toolchain setup (`esp32s3`, `esp32p4`, `esp32c6`), building all six firmware targets (`main_controller`, `front_node`, `pod_gateway`, `radar_submcu`, `omm_module`, `omm446_module`), generating SPIFFS filesystem images (`build/storage.bin` @ `0x5E0000`), and **Central Bus-DFU flashing** via the `USB2517I`/`USB2514Bi` hub backbone, see [`firmware/README.md`](../../firmware/README.md):

```bash
# Build all 6 firmware targets with their verified SoC targets:
./firmware/build.sh all

# Run the system-wide v10.0 Hardware-in-the-Loop (HIL) integration test:
python3 tools/simulators/firmware_hil_system_sim.py
```
