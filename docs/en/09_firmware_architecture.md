# 09 - Firmware Architecture, FreeRTOS Tasks & Rollback-OTA

*Note: All CAD, electronic, and block diagrams reflect the standardized v10.0 node architecture (PCBA 01 through 10).*

This document specifies the system-wide firmware architecture of OpenMotorBridge v10.0 (Native USB-PD & Edge-AI Generation): the multi-core allocation of the **ESP32-S31 AI RISC-V** host MCU on the Central Box (`PCBA 01`) featuring a 128-bit SIMD AI vector accelerator, the ESP32-S3 Front Node (`PCBA 05`), the deterministic **4-Wire Automotive USB-PD & USB 2.0 Backbone (`VBUS`, `GND`, `D+`, `D-`, latency < 0.2 ms)** to all satellite nodes, the **Dual-Power Input Engine** (12V DTM & USB-PD Sink 5V–20V via LM5050 ideal-diode OR-ing), the **5-Gesture Trigger Engine** for symmetrical under-perch mirror pods (`PCBA 05B`), the LittleFS profile engine, and the **Dual-Bank Rollback-OTA architecture** guaranteeing zero bricking during power interruptions.

---

## 1. Multi-Core & Multi-MCU System Architecture

In v10.0, the overall system is standardized onto a ruggedized, shielded **4-wire Automotive USB-PD & USB 2.0 bus**. All data, audio, and control links between Central Box and external nodes operate over wire with deterministic latency ($< 0.2\,	ext{ms}$) and massive power delivery (up to 60 W per branch):

```
+----------------------------------------------------------------------------------------+
|                        FIRMWARE CONTROLLERS IN CONCERT (v10.0)                         |
+------------------------------------------------------+---------------------------------+
| 1. CENTRAL BOX (ESP32-S31 AI RISC-V, PCBA 01)         | 2. FRONT NODE (ESP32-S3, PCBA 05)|
+------------------------------------------------------+---------------------------------+
| * Core 0: 4-Wire USB-PD Host Engine, SX1262 LoRa     | * Core 0: USB Backbone Client,  |
|   868 MHz, Dual-Power OR-ing, BLE, Pod Dispatcher    |   SAM-M10Q GNSS, CAN, USB-PD    |
| * Core 1: 48 kHz SIMD AI Audio-DSP, Raised-Cosine    | * Core 1: Knowles Wind-DSP,     |
|   Ducking, AGC, Qualcomm QCC3084 BT 5.4 Hub          |   5-Gesture Mirror-Pod Engine   |
+------------------------------------------------------+---------------------------------+
| 3. SATELLITE PODS (ESP32-C6, PCBA 03 in Pod 1 & 2)   | 4. REAR RADAR (ESP32-C5 Sub-MCU, PCBA 08)|
+------------------------------------------------------+---------------------------------+
| * USB 2.0 Device & USB-PD Sink Controller (up to 30W)| * Wheeltec MR20 77-GHz mmWave   |
| * ES8388 Audio Codec / USB Audio Class Streamer      | * 20 Hz Tracking Vectors via    |
| * OptoMOS PTT Keying & Direct Headset Interface      |   CAN / High-Speed Serial       |
+------------------------------------------------------+---------------------------------+
```

### 1.1 Central Box ESP32-S31 AI Host Controller Core Allocation (320 MHz RISC-V)

#### CORE 0 (Communication, Telemetry, 4-Wire USB Backbone & Power Management):
- **Automotive USB Backbone Host Engine (`usb_vehicle_backbone.cpp`):** Manages the USB 2.0 High-Speed connection across the onboard USB2514B hub to Front Node and saddlebag pods. Receives handlebar PTT and gesture events ($< 0.15\,	ext{ms}$), Knowles MEMS acoustic noise readings, 10 Hz Multi-GNSS packets, and pod telemetry.
- **Dual-Power Input Manager (`dual_power_mgr.cpp`):** Overviews the TI LM5050-Q1 ideal-diode OR-ing between 12V vehicle power (Deutsch DTM-6 / Cable 1) and USB-PD Sink (5V–20V USB-C). Enables seamless switching and zero-disassembly flashing, benchtop calibration, and testing without a 12V laboratory power supply.
- **Staggered Power Sequencing (`power_sequencer.cpp`):** Controls the automotive eFuses `TI TPS25982` on PCBA 01 to eliminate inrush current spikes:
  - $T = 0\,	ext{ms}$: Central Box (PCBA 01) and Front Node (PCBA 05) boot synchronously upon ignition ON (KL15).
  - $T = 200\,	ext{ms}$: Pod 1 (VBUS via eFuse with soft-start ramp).
  - $T = 350\,	ext{ms}$: Pod 2 (VBUS via eFuse with soft-start ramp).
  - $T = 500\,	ext{ms}$: Rear Radar (+12V switched on Whip 3).
- **LoRa 868 MHz Mesh Engine (`lora_mesh_engine.cpp`):** Direct SPI link to the onboard Semtech SX1262 transceiver on PCBA 01 (24/7 UPS-buffered for theft sentry and group telemetry).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth connection for the PWA dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatic state machine bridging radio shadows between Sena Mesh, Cardo DMC, OMM 2.4 GHz, and LoRa 868 MHz emergency beacon.
- **WebDAV TLS 1.3 Client:** Asynchronous upload of GPX tour recordings to Nextcloud/Synology on home Wi-Fi upon ignition OFF.
- **SDIO Logging Task:** 4-bit high-speed SD card logger with rolling BGH privacy auto-purge.
- **ADR-EKF Filter:** 15-State sensor fusion fusing 10 Hz Multi-GNSS telemetry (from Front Node via USB) and onboard Bosch BMI270 6-axis IMU for uninterrupted navigation through tunnels.

#### CORE 1 (Realtime Edge-AI Audio DSP & Qualcomm QCC3084 Hub @ Highest Priority):
- **128-bit SIMD AI Vector Accelerator:** Real-time filtering of wind noise, acoustic transients, and engine rumble, plus acoustic scene classification directly on silicon.
- **Qualcomm QCC3084 Dual-Helmet Audio Hub (`bluetooth_audio_manager.cpp`):** Controls the dedicated QCC3084 BT 5.4 Audio SoC (`U9` on PCBA 01) via UART (GAIA/AT) for hardware-accelerated Dual-A2DP (aptX HD / Adaptive) to rider and pillion helmets, LE Audio Auracast, and synchronous HFP 1.8 Wideband voice channel.
- **I2S Audio DMA Receiver & Transmitter:** Ultra-low-latency streaming via ES8388 Audio Codec and Qualcomm QCC3084 ($f_s = 48\,	ext{kHz}, 24\,	ext{bit}$, double-buffer of 128 samples = $2.67\,	ext{ms}$).
- **Raised-Cosine Ducking Engine:** Click-free, continuously differentiable audio attenuation during intercom announcements or radar alerts.
- **Dynamic AGC Volume Scaling:** Smooth automatic scaling of helmet output volume based on Front Node aerodynamic wind noise.
- **Lookahead Brickwall Limiter:** Prevents digital clipping exceeding $0\,	ext{dBFS}$.

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
- **TI LM5050-Q1 Ideal-Diode OR-ing:** Decouples the 12V vehicle power (Deutsch DTM-6) and the USB-PD Sink input (5V–20V via the native USB-C port) with zero forward voltage drop compared to conventional Schottky diodes.
- **Seamless Switching:** If the motorcycle is started with a USB-C charger connected, the 12V rail takes over the load without interruption.
- **Zero-Disassembly Benchtop Flashing:** On the workbench, the entire system can be operated, flashed, and calibrated with any standard USB-C PD phone or laptop charger—eliminating the need for a heavy 12V lab bench supply!

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
| **`power_mgmt_task`** | Central Box (Core 0) | **14** | 2 KB | Boot-Event / Timer  | GPIO / I2C Power      | Automotive eFuses, Dual-Power LM5050 monitoring, staggered power start. |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA dashboard (GATT services `0x180D`/`0x180A`/`0xFFE0`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringbuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO blackbox logging with ECDSA SHA-256 signature. |
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
