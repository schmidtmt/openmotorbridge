# 09 - Firmware Architecture, FreeRTOS Tasks & Rollback-OTA

This document specifies the system-wide firmware architecture of OpenMotorBridge v8.0: the multi-core allocation of the ESP32-S3 host MCU on the Central Box (`PCBA 01`), the ESP32-S3 Front Node (`PCBA 05`), the deterministic **UWB Backbone (Qorvo DW3110 / 6.489 GHz Ch. 5, latency < 0.4 ms)**, the **Group Split Fallback Engine**, the LittleFS profile engine, and the **Dual-Bank Rollback-OTA architecture** guaranteeing zero bricking during power interruptions.

---

## 1. Multi-Core & Multi-MCU System Architecture

In v8.0, the system is strictly consolidated to two primary main nodes (Rear Pod 3 and PCBA 04 have been retired without replacement):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         THE FIRMWARE CONTROLLERS IN CONCERT                            │
├──────────────────────────────────────────────────────┬─────────────────────────────────┤
│ 1. CENTRAL BOX (ESP32-S3 Dual-Core, PCBA 01)          │ 2. FRONT NODE (ESP32-S3, PCBA 05)│
├──────────────────────────────────────────────────────┼─────────────────────────────────┤
│ • Core 0: UWB Backbone, SX1262 LoRa 868, BLE, WebDAV  │ • Core 0: UWB Backbone, SAM-M10Q│
│ • Core 1: Realtime 48 kHz Audio DSP, Ducking, AGC    │   Multi-GNSS, CAN, USB-PD, PTT  │
│ • Co-MCUs: CH32V003 on PCBA 03 (Smart Cartridges)    │ • Core 1: Knowles Vector-DSP    │
└──────────────────────────────────────────────────────┴─────────────────────────────────┘
```

### 1.1 Central Box ESP32-S3 Core Allocation (240 MHz)

#### CORE 0 (Communication, Telemetry & System):
- **UWB Backbone Driver (`uwb_vehicle_backbone.cpp`):** Deterministic SPI communication with the Qorvo DW3110 transceiver on `B.Cu`. Receives handlebar PTT events ($< 0.4\,\text{ms}$), Knowles MEMS dB(A) acoustic noise readings, and 10 Hz Multi-GNSS packets from the Front Node.
- **LoRa 868 MHz Mesh Engine (`lora_mesh_engine.cpp`):** Direct SPI link to the onboard Semtech SX1262 transceiver on PCBA 01 (24/7 UPS-buffered for theft sentry and group telemetry).
- **BLE GATT Server (`ble_service_server.cpp`):** Web-Bluetooth connection for the PWA dashboard (`0x180D`, `0x180A`, `0xFFE0`).
- **Dual 1-Wire Cartridge Manager (`cartridge_onewire.cpp`):** Cyclically polls Ports 1 & 2 for cartridge IDs (emulated by CH32V003 MCU or DS2401) and dynamically mounts LittleFS JSON profiles.
- **Smart Cartridge Dispatcher & Opto-Pulse Sequencer (`opto_pulse_sequencer.cpp`):** Detects Smart Cartridges (PCBA 03) and dispatches 1-byte opcodes via single-wire UART on Pin 5 (19,200 baud) to drive the 4 mechatronic actuators; switches to TLP222A relay keying for analog PMR446 two-way radios.
- **Group Split Fallback Engine (`group_split_rescue_engine.cpp`):** Automatic state machine bridging radio shadows between Sena Mesh, Cardo DMC, OMM 2.4 GHz, and LoRa 868 MHz emergency beacon.
- **WebDAV TLS 1.3 Client:** Asynchronous upload of GPX tour recordings to Nextcloud/Synology on home Wi-Fi upon ignition OFF.
- **SDIO Logging Task:** 4-bit high-speed SD card logger with rolling BGH privacy auto-purge.
- **ADR-EKF Filter:** 15-State sensor fusion fusing 10 Hz Multi-GNSS telemetry (from Front Node via UWB) and onboard Bosch BMI270 6-axis IMU for uninterrupted navigation through tunnels.

#### CORE 1 (Realtime Audio DSP Engine @ Highest Priority):
- **I2S Audio DMA Receiver & Transmitter:** Ultra-low-latency streaming via ES8388 Audio Codec ($f_s = 48\,\text{kHz}, 24\,\text{bit}$, double-buffer of 128 samples = $2.67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Click-free, continuously differentiable audio attenuation during intercom announcements or radar alerts.
- **Dynamic AGC Volume Scaling:** Smooth automatic scaling of helmet output volume based on Front Node aerodynamic wind noise.
- **Lookahead Brickwall Limiter:** Prevents digital clipping exceeding $0\,\text{dBFS}$.

---

## 2. Deterministic UWB Vehicle Backbone (`uwb_vehicle_backbone.cpp`)

The wireless backbone between Front Node and Central Box employs IEEE 802.15.4z Ultra-Wideband (Qorvo DW3110, Channel 5 @ 6.489 GHz, 499.2 MHz bandwidth, BPRF mode):
- **Regulatory Compliance:** ETSI EN 302 065-1, EN 302 065-3, and EU Decision 2019/785 ($-41.3\,\text{dBm/MHz}$, continuous legal transmission without duty-cycle capping).
- **Zero-Interference:** Operates far above 2.4 GHz (Wi-Fi, Bluetooth, Sena Mesh, Cardo DMC) and 5.8 GHz.
- **Deterministic Latency:** Flight and processing time $< 0.4\,\text{ms}$.

```cpp
enum UwbBackbonePktType : uint8_t {
    UWB_PKT_HEARTBEAT       = 0x01,  // Status, Uptime, VBUS Voltage, Ranging Distance
    UWB_PKT_PTT_EVENT       = 0x02,  // Handlebar PTT pressed/released (< 0.4 ms)
    UWB_PKT_AUDIO_RMS       = 0x03,  // Knowles MEMS wind noise dB(A) level (50 Hz)
    UWB_PKT_GNSS_PVT        = 0x04,  // u-blox SAM-M10Q 10 Hz PVT telemetry block
    UWB_PKT_ENV_SENSORS     = 0x05,  // TI TMP117 (Temp) & TI OPT3001 (Lux)
    UWB_PKT_CAN_TELEMETRY   = 0x06,  // Cockpit CAN telemetry data (when J2 active)
    UWB_PKT_OTTOCAST_STATUS = 0x07,  // Status, Current, Auto-Café Timer
    UWB_PKT_CMD_POWER_CYCLE = 0x10,  // Central Box -> Front Node: 2.5s Hard Reboot
    UWB_PKT_CMD_CONFIG      = 0x11   // Central Box -> Front Node: Ignition Sync
};
```

### 2.1 Handlebar PTT Latency Budget
1. **Handlebar Switch Closure:** $12\,\mu\text{s}$ hardware debouncing.
2. **Front Node ESP32-S3 GPIO Interrupt:** $25\,\mu\text{s}$ ISR execution time.
3. **UWB SPI TX & RF Transmission (6.5 GHz):** $180\,\mu\text{s}$ (6.8 Mbps data rate).
4. **Central Box DW3110 SPI RX & Core 0 ISR:** $45\,\mu\text{s}$ frame decode & opcode dispatch.
5. **Cartridge Controller & N-MOSFETs (`AO3400`):** $< 100\,\mu\text{s}$ switching time of mechatronic actuators.
* **Total Glass-to-Glass Latency:** **$\approx 0.36\,\text{ms}$** (more than 25 times faster than the human perceptual threshold of $10\,\text{ms}$).

### 2.2 UWB Cryptographic Binding & Distance Gating
- **PAN-ID & Session Key:** A 128-bit AES-GCM session key stored in encrypted NVS flash prevents cross-talk between adjacent motorcycles.
- **Two-Way Ranging Gating:** The Central Box continuously verifies the physical distance to the Front Node. If distance falls outside the motorcycle envelope ($0.5\,\text{m}\dots 2.5\,\text{m}$), frames are rejected (protection against spoofing and relay attacks).

### 2.3 CAN Dual-Ingress Architecture & Auto-Sensing / Deactivation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAN DUAL-INGRESS & AUTO-SENSING MATRIX                   │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ Scenario 1: Touring Fairing       │ Scenario 2: Naked / Road King / Adv     │
│ (Street Glide / Road Glide)       │ (Road King Special, BMW R1250/R1300 GS) │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ • CAN connector at FRONT NODE     │ • No CAN present in headlight nacelle   │
│   Port J2 (3-Pin JST-GH)          │ • CAN connector at CENTRAL BOX          │
│ • Front Node detects bus frames   │   HD26 header pins 17/18 at BCM / OBD2  │
│ • 120R relay CPC1017N CLOSES      │ • Front Node J2 remains UNCONNECTED     │
│ • Telemetry streamed via UWB      │ • Front Node deactivates J2 after 2.5s: │
│   (UWB_PKT_CAN_TELEMETRY) to      │   - 120R relay remains OPEN             │
│   Central Box                     │   - TCAN334G enters Silent High-Z mode  │
│ • Central Box switches to         │   - TWAI controller halted (twai_stop)  │
│   `CAN_SOURCE_REMOTE_FRONT_NODE`  │ • Central Box utilizes local HD26 CAN   │
│                                   │   as `CAN_SOURCE_LOCAL_CENTRAL_BOX`     │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

1. **Front Node Auto-Sensing & Deactivation (`cockpit_can_manager.cpp`):**
   - Boots in safe **Listen-Only Mode** (`TWAI_MODE_LISTEN_ONLY`) with the termination relay open (`PIN_CAN_TERM_EN = 0`).
   - Senses bus activity within a $2.5\,\text{s}$ boot-time window.
   - **Bus Detected:** State transitions to `CAN_STATE_CONNECTED`, the Solid-State OptoMOS relay `CPC1017N` closes the local $120\,\Omega$ termination resistor, the transceiver switches to normal mode (`PIN_CAN_SILENT = 0`), and streams received frames over UWB to the Central Box.
   - **No Bus Detected (e.g., Road King / BMW GS):** State transitions to `CAN_STATE_DEACTIVATED`. The relay remains open, `PIN_CAN_SILENT` is pulled HIGH (standby/high-Z), and the TWAI controller is halted (`twai_stop()`). This guarantees 0 bus-off errors, 0 spurious interrupts, and negligible quiescent current.
2. **Central Box Source Arbitration (`can_bus_manager.cpp`):**
   - When local CAN frames are received on HD26 pins 17/18, `CAN_SOURCE_LOCAL_CENTRAL_BOX` is active.
   - If the local HD26 CAN port remains unconnected, the manager seamlessly switches to `CAN_SOURCE_REMOTE_FRONT_NODE`.

---

## 3. BLE GATT Server Architecture (`ble_service_server.cpp`)

The system exposes standardized Bluetooth SIG services as well as vendor-specific characteristics for the PWA dashboard:

| Service UUID | Characteristic UUID | Properties | Function & Data Payload |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Audio RMS & Env)       | **`0x2A37`** | Notify | Knowles MEMS wind noise level (50 Hz, dB(A)) & TMP117 temperature. |
| **`0x180A`** (Device Information)    | **`0x2A24`** | Read   | Hardware revision (`OMB-V8-2026.1`), Serial, Firmware build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Control commands: `0x01` Profile switch, `0x02` Reset, `0x09` Smart Cartridge Opcode. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetry stream: Lean-Angle (Roll/Pitch), Speed, TTC, Radar warning. |
| **`0xFFE0`** (1-Wire & Cartridge ID) | **`0xFFE3`** | Notify/Read | Cartridge status Ports 1 & 2: 64-bit UID, hardware class, DLE score. |

---

## 4. Universal Group Split Fallback Engine (`group_split_rescue_engine.cpp`)

During tours across mountainous terrain or dense forests, 2.4 GHz intercom connections (Sena Mesh / Cardo DMC) drop beyond approximately $800\dots 1200\,\text{m}$ once line-of-sight is obstructed. The integrated **Group Split Fallback Engine** in v8.0 prevents groups from fragmenting:

```
               GROUP SPLIT FALLBACK ENGINE STATE MACHINE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. NORMAL STATUS: LINE-OF-SIGHT CONNECTED                                   │
│    • Pod 1 (Sena Mesh) & Pod 2 (Cardo DMC) fully active                     │
│    • HD-Audio stream in helmet; LoRa transmits periodic heartbeats (0.2 Hz) │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Connection loss > 15 s)              │
│ 2. RESCUE LEVEL 1: OMM 2.4 GHz CHANNEL-HOPPING MESH                         │
│    • If OMM cartridge installed: Boosts TX power to +20 dBm                 │
│    • Searches for relay nodes among adjacent group members                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Connection loss > 45 s)              │
│ 3. RESCUE LEVEL 2: 868 MHz LoRa MESH (SX1262) TELEMETRY & TEXT              │
│    • Range up to 15 km (LOS) or 3-5 km in mountains                         │
│    • Automatically transmits GPS position, bearing, distance & arrow vector │
│    • Displays "Group ahead: 2.4 km NW" on CarPlay / PWA Dashboard           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                     ▼ (Connection loss > 120 s)             │
│ 4. RESCUE LEVEL 3: PMR446 ANALOG VOICE FALLBACK (OPTIONAL)                  │
│    • Triggers automated voice broadcast ping on Midland radio cartridge     │
│    • Broadcasts synthesized TTS location announcement over PMR446 channel   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Cartridge Control: Mechatronic Smart Cartridge (PCBA 03) & Hardware IDs

### 5.1 CH32V003 Hardware IDs & 1-Wire Emulation
Every plug-in cartridge reports its hardware class upon insertion via single-wire UART / 1-Wire ID:
* **`0x01`**: Sena SPIDER X Slim (Mechatronic 4-actuator control)
* **`0x02`**: Cardo Packtalk Edge (Mechatronic 4-actuator control)
* **`0x03`**: OMM 2.4 GHz Swap Cartridge (ESP32-C3 Digital Transceiver)
* **`0x04`**: Midland PMR446 / Two-Way Radio (Relay keying via TLP222A)

### 5.2 Smart Cartridge Mechatronic Mode (PCBA 03)
The Central Box dispatches 1-byte opcodes via single-wire UART on Pin 5 (19,200 baud) to the CH32V003:

| Opcode | Function / Gesture | Active Actuators | Pulse Duration / Sequence | Headset Response (Sena SPIDER X Slim) |
| :---: | :--- | :--- | :--- | :--- |
| **`0x01`** | **Power Boot (Cold Start)**| **ACT_CENTER + PLUS** | $1000\,\text{ms}$ synchronous | Automatically boots headset on ignition ON |
| **`0x02`** | **Power Off** | **ACT_CENTER + PLUS** | $200\,\text{ms}$ synchronous | Clean graceful shutdown prior to power cut |
| **`0x03`** | **Volume Up (+)** | **ACT_PLUS** (solo) | $100\,\text{ms}$ single pulse | Volume +1 step |
| **`0x04`** | **Volume Down (-)** | **ACT_MINUS** (solo) | $100\,\text{ms}$ single pulse | Volume -1 step |
| **`0x05`** | **Mesh Intercom On/Off**| **ACT_MESH** (solo) | $200\,\text{ms}$ single pulse | Mesh toggle voice prompt ("Mesh On/Off") |
| **`0x06`** | **Open ↔ Group Mesh** | **ACT_MESH** (solo) | $3000\,\text{ms}$ hold pulse | Toggles between Open Mesh and private Group Mesh |
| **`0x07`** | **Channel +1 (Macro)** | **ACT_MESH (2x) + PLUS (1x)** | 2x $150\,\text{ms}$, pause $200\,\text{ms}$, 1x $150\,\text{ms}$ | Enters channel menu and advances channel autonomously |
| **`0x08`** | **Channel -1 (Macro)** | **ACT_MESH (2x) + MINUS (1x)**| 2x $150\,\text{ms}$, pause $200\,\text{ms}$, 1x $150\,\text{ms}$ | Enters channel menu and decrements channel autonomously |

---

## 6. FreeRTOS Task Architecture & Scheduling Matrix (Central Box & Front Node)

The overall system orchestrates 15 specialized tasks across 2 ESP32-S3 host microcontrollers:

| Task Name | MCU / Core | Priority | Stack | Trigger / Rate | IPC / Interface | Responsibility & Function |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | Central Box (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Zero-latency I2S audio mix, Raised-Cosine ducking & AGC. |
| **`uwb_backbone_task`**| Central Box (Core 0) | **22** | 4 KB | DW3110 IRQ / Event | Direct-to-Task Notify | Processes Front Node PTT events ($< 0.4\,\text{ms}$), GNSS & wind noise. |
| **`lora_mesh_task`**  | Central Box (Core 0) | **20** | 4 KB | SX1262 IRQ / Timer  | FreeRTOS Queue        | 868 MHz LoRa mesh protocol, theft sentry & Group Split Rescue. |
| **`smart_act_task`**  | Central Box (Core 0) | **18** | 2 KB | Event-Queue         | FreeRTOS Queue        | Dispatches 1-byte opcodes via single-wire UART / TLP222A relays. |
| **`radar_proc_task`** | Central Box (Core 0) | **16** | 4 KB | 20 Hz UART2 ISR     | FreeRTOS Queue / UART | Wheeltec MR20 / Garmin Varia parsing, TTC calculation & Prio-1 ducking. |
| **`adr_ekf_task`**    | Central Box (Core 0) | **15** | 4 KB | 50 Hz Timer         | I2C / CAN Buffer      | 15-State Kalman filter (SAM-M10Q GNSS + BMI270 IMU + CAN speed). |
| **`ble_server_task`** | Central Box (Core 0) | **10** | 4 KB | Event-Driven        | NimBLE Stack          | Web-Bluetooth PWA dashboard (GATT services `0x180D`/`0x180A`). |
| **`sdio_log_task`**   | Central Box (Core 0) | **8**  | 8 KB | 10 Hz Ringbuffer    | FreeRTOS RingBuffer   | 4-Bit SDIO blackbox logging with ECDSA SHA-256 signature. |
| **`onewire_task`**    | Central Box (Core 0) | **5**  | 2 KB | 0.5 Hz cyclic       | Bit-Banging Driver    | Polls cartridge IDs on Pods 1 & 2 (CH32V003 emulation or DS2401). |
| **`webdav_sync_task`**| Central Box (Core 0) | **3**  | 8 KB | Graceful Shutdown   | LwIP TLS 1.3          | Automatic GPX tour upload via home Wi-Fi upon ignition OFF. |
| **`front_ptt_task`**  | Front Node (Core 0)  | **24** | 2 KB | GPIO Edge ISR       | UWB TX Queue          | Transmits handlebar PTT via UWB in $< 0.2\,\text{ms}$; Cam toggle; HiLight tag. |
| **`front_gnss_task`** | Front Node (Core 0)  | **20** | 4 KB | 10 Hz I2C DMA       | J12 Qwiic / UWB TX    | u-blox SAM-M10Q UBX-NAV-PVT parsing, TMP117 Temp & OPT3001 Lux. |
| **`front_mems_task`** | Front Node (Core 1)  | **18** | 4 KB | 48 kHz DMA          | Vector-DSP Filter     | Knowles SPH0645 digital microphone A-weighting & RMS tracking via Xtensa DSP. |
| **`front_can_task`**  | Front Node (Core 0)  | **16** | 4 KB | TWAI Interrupt      | CAN Message Queue     | Reads cockpit CAN (if J2 connected), CPC1017N auto-termination. |
| **`front_pwr_task`**  | Front Node (Core 0)  | **10** | 2 KB | 10 Hz Timer         | GPIO Load Switch      | SW3526 USB-PD monitoring, TPS2051B cold restart (2.5s), auto-off. |

---

## 7. LittleFS Cartridge Profile Engine & JSON Storage Schema

Upon cartridge insertion, the cartridge manager loads the configuration from `/storage/profiles/<UID>.json`:

```json
{
  "profile_schema": 2,
  "uid": "01:A4:7B:3F:00:00:00:1E",
  "device_name": "Sena SPIDER X Slim Inlay",
  "hardware_class": "0x01",
  "power": {
    "vcc_enabled": true,
    "vcc_voltage_mv": 5000,
    "max_current_ma": 350,
    "soft_start_ms": 120
  },
  "audio": {
    "input_gain_db": 6.0,
    "output_gain_db": 0.0,
    "ducking_priority": 3,
    "auto_agc_enabled": true,
    "clip_limit_dbfs": -0.5
  },
  "opto_trigger": {
    "enabled": true,
    "mode": "sena_spider_mesh",
    "pulse_click_ms": 150,
    "pulse_channel_ms": 1000
  },
  "mesh_routing": {
    "dle_bonus_points": 60,
    "protocol_family": "sena_mesh_3"
  }
}
```

* **Zero-Trust Fallback (`disabled.json`):** On unrecognized UIDs, electrical shorts, or empty bays, the 5V MOSFET remains off (`vcc_enabled: false`), codec gain drops to `-96 dB`, and DLE score is clamped to `0`.

---

## 8. Modular Hardware Topology & Graceful Degradation

OpenMotorBridge is designed from the ground up as a **resilient, fault-tolerant modular architecture**. No subsystem blocks Central Box boot or crashes if optional modules are omitted or unplugged:

| Configuration | Installed Hardware | System Behavior & Graceful Degradation |
| :--- | :--- | :--- |
| **Tier 1: Minimal Core** | Central Box only<br>*(No Front Node)* | • **Audio Bridge & Intercoms fully operational:** Pod 1 & 2 mix with zero latency.<br>• **LoRa 868 MHz Mesh active:** Direct UPS-buffered 24/7 theft sentry & tracking.<br>• **CAN-Bus active:** Speed, RPM & BCM telemetry via HD26 pins 17/18 under seat.<br>• **IMU active:** Bosch BMI270 provides lean angle, pitch & vibration sensing.<br>• **ADR-EKF:** Operates in pure Dead Reckoning mode supported by IMU & wheel speed.<br>• **UWB driver:** Waits passively in scan mode; AGC operates at nominal gain. |
| **Tier 2: Full System with Front Node** | Central Box + Front Node | • All Tier 1 features + deterministic UWB backbone (< 0.4 ms).<br>• u-blox SAM-M10Q Multi-GNSS with 10 Hz PVT fix & precision time synchronization.<br>• TI TMP117 black ice warning ($\pm 0.1\,^\circ\text{C}$) & TI OPT3001 ambient light sensor.<br>• 4-Port USB Hub & Dual 20W USB-PD fast charger in cockpit.<br>• Ottocast Watchdog & automatic ignition power-gating.<br>• Handlebar PTT (< 0.4 ms) and dynamic acoustic wind AGC via Knowles MEMS. |
| **Tier 3: Rear Radar Option** | Central Box + Front Node + Radar | • All Tier 2 features + Wheeltec MR20 77 GHz or Garmin Varia on Whip 5.<br>• Audible warning pings in helmet, visual alert wings & mirror LEDs (Port `J9`).<br>• Automatic action cam bookmarks upon critical radar TTC hazard (< 2.5s). |

### 8.1 Zero-Crash Resiliency Mechanisms
1. **Asynchronous Non-Blocking Interfaces:** Communications via UWB, LoRa (SPI), and Radar (UART2) use FreeRTOS timeouts (`pdMS_TO_TICKS(50)`). There are **zero blocking `while(1)` polling loops** awaiting serial bytes.
2. **Dynamic DLE Capabilities (`omm_get_capabilities_vector`):** Central Box advertises only those hardware flags to the mesh that physically acknowledge presence (`gnss_is_connected()`, `is_linked`, `can_bus_is_connected()`).
3. **Sensor-Fusion Autarky (`adr_ekf_filter.cpp`):** If GNSS is absent (e.g. tunnel or Front Node offline), the EKF immediately falls back to **Dead Reckoning** supported by IMU and CAN wheel speed.
4. **Fault-Tolerant Audio Mixer (`audio_dsp_pipeline.cpp`):** If the Front Node Knowles MEMS microphone is absent, the brickwall limiter and AGC level run at a fixed nominal baseline (Unity Gain `1.0f`).
