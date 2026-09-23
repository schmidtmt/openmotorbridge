# 09 - Firmware Architecture, FreeRTOS Tasks & Rollback-OTA

This document specifies the system-wide firmware architecture of OpenMotorBridge v8.0: the multi-core allocation of the ESP32-S3 host MCU, the coprocessors (ESP32-C3 in Rear Pod 3 and ESP32-S3 in the Front Node), the **ESP-NOW low-latency protocol (< 1.8 ms)**, the LittleFS profile engine, and the **Dual-Bank Rollback-OTA architecture** guaranteeing zero bricking during power interruptions.

---

## 1. Multi-Core & Multi-MCU System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 3 FIRMWARE CONTROLLERS IN CONCERT                           │
├──────────────────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. CENTRAL BOX (ESP32-S3 Dual-Core)  │ 2. REAR POD 3 (ESP32-C3)│ 3. FRONT NODE (ESP32-S3)│
├──────────────────────────────────────┼─────────────────────────┼───────────────────────┤
│ • Core 0: BLE, WebDAV, SDIO, ESP-NOW │ • NMEA/UBX & I2C-Sensor │ • Core 0: BLE/ESP-NOW │
│ • Core 1: Realtime 48kHz Audio DSP   │ • 2.4G OMM & SX1262 LoRa│ • Core 1: Vector-DSP  │
│ • LittleFS Cartridge Profile Engine  │ • 1-PPS Timecode Sync   │ • TWAI CAN-Bus / USB  │
└──────────────────────────────────────┴─────────────────────────┴───────────────────────┘
```

### 1.1 ESP32-S3 Core Allocation (240 MHz)

#### CORE 0 (Communication, Telemetry & System):
- **BLE GATT Server:** Web-Bluetooth connection for the PWA dashboard (`0x180D`, `0x180A`).
- **ESP-NOW Front Node Client (`esp_now_front_node_client.cpp`):** Handles zero-latency handlebar PTT events ($< 1{,}8\,\text{ms}$) and Knowles MEMS dB(A) noise telemetry.
- **Dual 1-Wire Cartridge Manager (`cartridge_onewire.cpp`):** Polls 64-bit ROM IDs (emulated by Cartridge MCU or physical DS2401) on Ports 1 & 2 to dynamically mount LittleFS JSON profiles.
- **Smart Cartridge Dispatcher & Opto-Pulse Sequencer (`opto_pulse_sequencer.cpp`):** Detects Smart Cartridges (PCBA 03 Rev 2.0) and dispatches 1-byte opcodes via single-wire UART on Pin 5 (19,200 baud) to drive the 4 mechatronic actuators; switches to TLP222A relay keying for analog PMR446 radios.
- **WebDAV TLS 1.3 Client:** Asynchronous upload of GPX rides to Nextcloud/Synology on home Wi-Fi.
- **SDIO Logging Task:** 4-bit high-speed SD card logger with rolling BGH privacy auto-purge.

#### CORE 1 (Realtime Audio DSP Engine @ Highest Priority):
- **I2S Audio DMA Receiver & Transmitter:** Ultra-low-latency streaming via ES8388 Codec ($f_s = 48\,\text{kHz}, 24\,\text{bit}$, 128-sample double buffers = $2{,}67\,\text{ms}$).
- **Raised-Cosine Ducking Engine:** Click-free, mathematically continuous attenuation during announcements.
- **Dynamic AGC Volume Boost:** Automatic helmet volume scaling driven by Front Node wind noise.
- **Lookahead Brickwall Limiter:** Prevents digital clipping above $0\,\text{dBFS}$.

---

## 2. Ultra-Low-Latency ESP-NOW Protocol (`esp_now_front_node_client`)

Direct communication between Front Node and Central Box utilizes unencrypted IEEE 802.11 Vendor-Specific Action Frames:

```cpp
enum FrontNodePktType : uint8_t {
    PKT_TYPE_HEARTBEAT       = 0x01,  // Status, Uptime, VBUS Voltage
    PKT_TYPE_PTT_EVENT       = 0x02,  // Handlebar PTT pressed/released (< 1.8 ms)
    PKT_TYPE_AUDIO_RMS       = 0x03,  // Knowles MEMS wind noise dB(A) (50 Hz)
    PKT_TYPE_OTTOCAST_STATUS = 0x04,  // Status, Current, Auto-Café Timer
    PKT_TYPE_CAN_TELEMETRY   = 0x05,  // Cockpit CAN telemetry
    PKT_TYPE_CMD_POWER_CYCLE = 0x10,  // Central Box -> Front Node: 2.5s Hard Reboot
    PKT_TYPE_CMD_CONFIG      = 0x11   // Central Box -> Front Node: Ignition Sync
};
```

### 2.1 Handlebar PTT Latency Budget
1. **Handlebar Switch Closure:** $12\,\mu\text{s}$ hardware debouncing.
2. **ESP32-S3 GPIO Interrupt:** $25\,\mu\text{s}$ ISR execution time.
3. **ESP-NOW Radio Transmission (2.4 GHz):** $0{,}90\,\text{ms}$ over-the-air flight time (99.8% PDR).
4. **Central Box ESP32-S3 Core 0 ISR:** $45\,\mu\text{s}$ frame decode & opcode dispatch.
5. **Cartridge Controller & N-MOSFETs (`AO3400`):** $< 0{,}10\,\text{ms}$ actuator gate trigger.
* **Total Glass-to-Glass Latency:** **$1{,}70\,\text{ms}$** (far below the human perceptual threshold of 10 ms).

### 2.2 Front-Node Binding, Proximity-Pairing & Zero-Touch Re-Pairing

To completely prevent cross-talk, accidental triggering, or packet interference during group rides and at red lights (where multiple OpenMotorBridge-equipped motorcycles are clustered together), the system implements a strict **1:1 hardware binding** stored in NVS flash:

```
                  FRONT-NODE BINDING- & RE-PAIRING STATE MACHINE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. INITIAL FACTORY STATE:                                                   │
│    • No Front Node MAC in NVS (Status: UNPAIRED)                            │
│    • Central Box opens 60s pairing window upon first boot                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 2. PROXIMITY-PAIRING & RSSI-GATING:                                         │
│    • Front Node broadcasts pairing beacon at reduced TX power (-12 dBm)     │
│    • Central Box accepts pairing ONLY if RSSI > -45 dBm (< 30 cm distance)  │
│    • Rider holds Front Node directly against Central Box                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 3. PAIRING HANDSHAKE & NVS PERSISTENCE:                                     │
│    • Central Box acknowledges with vendor action frame (pairing token)      │
│    • Both nodes store peer MAC & token in encrypted NVS                     │
│    • State transitions to PAIRED & LOCKED                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                    │
│ 4. ZERO-TOUCH AUTOMATIC RE-CONNECT:                                         │
│    • On every ignition ON (KL15), Front Node sends heartbeat frame          │
│    • Central Box verifies MAC & token in < 5 ms -> Instant PTT readiness   │
│    • Zero manual button presses or pairing required for daily rides         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 CAN Dual-Ingress Architecture & Auto-Sensing / Deactivation

OpenMotorBridge supports vehicle CAN bus telemetry ingress from two redundant hardware locations:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAN DUAL-INGRESS & AUTO-SENSING MATRIX                   │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ Scenario 1: Touring Fairing       │ Scenario 2: Naked / Road King / Adv     │
│ (Street Glide / Road Glide)       │ (Road King Special, BMW R1250/R1300 GS) │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ • CAN connector at FRONT NODE     │ • No CAN present in headlight nacelle   │
│   Port J2 (4-Pin JST-PH)          │ • CAN connector at CENTRAL BOX          │
│ • Front Node detects bus frames   │   HD26 header pins 17/18 at BCM / OBD2  │
│ • 120R relay CPC1017N CLOSES      │ • Front Node J2 remains UNCONNECTED     │
│ • Telemetry streamed via ESP-NOW  │ • Front Node deactivates J2 after 2.5s: │
│   (PKT_TYPE_CAN_TELEMETRY) to     │   - 120R relay remains OPEN             │
│   Central Box                     │   - TCAN334G enters Silent High-Z mode  │
│ • Central Box switches to         │   - TWAI controller halted (twai_stop)  │
│   `CAN_SOURCE_REMOTE_FRONT_NODE`  │ • Central Box utilizes local HD26 CAN   │
│                                   │   as `CAN_SOURCE_LOCAL_CENTRAL_BOX`     │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

1. **Front Node Auto-Sensing & Deactivation (`cockpit_can_manager.cpp`):**
   - Boots in safe **Listen-Only Mode** (`TWAI_MODE_LISTEN_ONLY`) with the termination relay opened (`PIN_CAN_TERM_EN = 0`).
   - Senses bus activity within a $2.5\,\text{s}$ boot-time window.
   - **Bus Detected:** State transitions to `CAN_STATE_CONNECTED`, the Solid-State OptoMOS relay `CPC1017N` closes the local $120\,\Omega$ termination resistor, the transceiver switches to normal mode (`PIN_CAN_SILENT = 0`), and streams received frames over ESP-NOW to the Central Box.
   - **No Bus Detected (e.g., Road King / BMW GS):** State transitions to `CAN_STATE_DEACTIVATED`. The relay remains open, `PIN_CAN_SILENT` is pulled HIGH (standby/high-Z), and the TWAI controller is halted (`twai_stop()`). This guarantees 0 bus-off errors, 0 spurious interrupts, and negligible quiescent current.

2. **Central Box Source Arbitration (`can_bus_manager.cpp`):**
   - Central Box continuously monitors both its local HD26 CAN receiver and incoming ESP-NOW CAN telemetry packets.
   - When local CAN frames are received (Road King / BMW under seat), `CAN_SOURCE_LOCAL_CENTRAL_BOX` is active.
   - If the local HD26 CAN port is unconnected (Fairing touring bikes), the manager seamlessly designates `CAN_SOURCE_REMOTE_FRONT_NODE` as the primary source upon receiving ESP-NOW telemetry.
   - Wheel speed (`adr_ekf_update_can_wheel_speed`), handlebar joystick events, and telemetry are fed to downstream subsystems (ADR Dead Reckoning, Radar TTC, Helmet AGC, WebApp) in an identical, fully transparent manner.

---

## 3. BLE GATT Server Architecture (`ble_service_server.cpp`)

The system exposes standardized Bluetooth SIG services and vendor-specific characteristics for the PWA dashboard:

| Service UUID | Characteristic UUID | Properties | Function & Data Payload |
| :--- | :--- | :--- | :--- |
| **`0x180D`** (Heart Rate / Audio RMS) | **`0x2A37`** | Notify | Knowles MEMS wind noise level (50 Hz, 8-bit dB(A) + Peak). |
| **`0x180A`** (Device Information)   | **`0x2A24`** | Read   | Hardware revision (`OMB-V8-2026.1`), Serial, Firmware build. |
| **`0xFFE0`** (Proprietary Control)   | **`0xFFE1`** | Write  | Control commands: `0x01` Profile switch, `0x02` Reset, `0x09` Smart Cartridge Opcode. |
| **`0xFFE0`** (Proprietary Telemetry) | **`0xFFE2`** | Notify | 10 Hz Telemetry stream: Lean-Angle (Roll/Pitch), Speed, TTC, Battery status. |
| **`0xFFE0`** (1-Wire & DLE Gateway)  | **`0xFFE3`** | Notify/Read | Cartridge status Ports 1 & 2: 64-bit UID, detected class, DLE score. |

---

## 4. OMM In-System UART-Push-Flasher (`omm_flasher.cpp`)

For zero-disassembly firmware updates of rear Pod 3:
* The Central Box reads the binary image `omm_rear.bin` and triggers the hardware ROM bootloader on the ESP32-C3 via dedicated GPIO reset/boot lines using the SLIP protocol (`omm_flasher.cpp`).
* Flashing completes over $460{,}800\,\text{baud}$ UART in 1024-byte chunks in $< 6\,\text{s}$.
* The Front Node (PCBA 05) is updated via dual-partition OTA rollback partitions over ESP-NOW or through the WebApp dashboard.

---

## 5. Cartridge Key Automation: Mechatronic Smart Cartridge (PCBA 03 Rev 2.0) & Legacy Mode

OpenMotorBridge actuates intercoms and two-way radios via two optimized modes:

### 5.1 Smart Cartridge Mechatronic Mode (PCBA 03 Rev 2.0 – Default for Intercoms)
The Central Box communicates over Pin 5 (`TRIGGER_PPS`) via 19,200-baud single-wire UART with the Cartridge MCU (WCH CH32V003). The MCU independently drives 4 N-MOSFETs (`AO3400`):

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

### 5.2 TLP222A Legacy Mode (PMR446 Radios / K7)
For analog radios (e.g. Midland G9 / SA818S), Pin 5/6 provides isolated solid-state relay keying (PhotoMOS TLP222A) synchronized with the handlebar PTT.

---

## 6. FreeRTOS Task Architecture & Scheduling Matrix (All 3 MCUs)

The overall system orchestrates 13 specialized tasks across 3 physically separated microcontrollers with deterministic priorities and core affinities:

| Task Name | MCU / Core | Priority | Stack | Trigger / Rate | IPC / Interface | Responsibility & Function |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | ESP32-S3 (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Zero-latency I2S audio mix, Raised-Cosine ducking & AGC. |
| **`esp_now_rx_task`** | ESP32-S3 (Core 0) | **22** | 4 KB | Event-Queue | Direct-to-Task Notify | Handles Front Node PTT events ($< 1{,}8\,\text{ms}$) & noise RMS. |
| **`smart_act_task`** | ESP32-S3 (Core 0) | **18** | 2 KB | Event-Queue | FreeRTOS Queue | Dispatches 1-byte opcodes via single-wire UART or triggers TLP222A relays. |
| **`radar_proc_task`** | ESP32-S3 (Core 0) | **16** | 4 KB | 20 Hz UART2 ISR | FreeRTOS Queue / UART | Garmin Varia / mmWave parsing, TTC calculation & Prio-1 ducking. |
| **`adr_ekf_task`** | ESP32-S3 (Core 0) | **15** | 4 KB | 50 Hz Timer | I2C / CAN Buffer | 15-State Kalman filter (GNSS + IMU + wheel speed). |
| **`ble_server_task`** | ESP32-S3 (Core 0) | **10** | 4 KB | Event-Driven | NimBLE Stack | Web-Bluetooth PWA dashboard (GATT services `0x180D`/`0x180A`). |
| **`sdio_log_task`** | ESP32-S3 (Core 0) | **8** | 8 KB | 10 Hz Ringbuffer | FreeRTOS RingBuffer | 4-Bit SDIO blackbox telemetry logging with ECDSA SHA-256. |
| **`onewire_task`** | ESP32-S3 (Core 0) | **5** | 2 KB | 0.5 Hz cyclic | Bit-Banging Driver | Polls 1-Wire UIDs on Pods 1 & 2 (CH32V003 emulation or physical DS2401). |
| **`webdav_sync_task`**| ESP32-S3 (Core 0) | **3** | 8 KB | Graceful Shutdown | LwIP TLS 1.3 | Automatic GPX tour upload via home Wi-Fi upon ignition OFF. |
| **`rear_nmea_task`** | ESP32-C3 (RISC-V) | **High**| 2 KB | 10 Hz DMA | UART0 (460.8k Baud) | High-speed UBX/NMEA parsing, 1-PPS timecode capture & I2C SHT40. |
| **`rear_lora_task`** | ESP32-C3 (RISC-V) | **High**| 2 KB | SX1262 IRQ | SPI0 / ESP-NOW | 868 MHz LoRa mesh packet scheduling & 2.4 GHz OMM voice. |
| **`front_ptt_task`** | ESP32-S3 (Core 0)| **24** | 2 KB | GPIO 0 Edge ISR | ESP-NOW TX Queue | Transmits handlebar PTT: 1x short = radio PTT via ESP-NOW in $< 0{,}9\,\text{ms}$; 2x short = Action Cam Toggle; 1x long = HiLight Tag. |
| **`front_mems_task`** | ESP32-S3 (Core 1)| **18** | 4 KB | 48 kHz DMA | Biquad Vector-DSP| Knowles SPH0645 MEMS acoustic A-weighting & RMS tracking with SIMD acceleration. |
| **`front_can_task`**  | ESP32-S3 (Core 0)| **14** | 4 KB | TWAI CAN ISR | FreeRTOS Queue | Automotive CAN-Bus gateway (Harley/BMW/KTM/Ducati) with CPC1017N dynamic termination sensing. |
| **`front_cam_ble_task`**| ESP32-S3 (Core 0)| **12**| 4 KB | Event / KL15 ISR | NimBLE Client | Controls GoPro / Insta360 / DJI over BLE; triggers instant auto-stop (fuel-stop filter) upon ignition off with $C_{\text{BUF}}$ power reserve. |
| **`front_pwr_task`** | ESP32-S3 (Core 0)| **10** | 2 KB | 10 Hz Timer | GPIO Load Switch | TPS2051B 1-click cold restart (2.5s) & Auto-Café 60s timer for CP2AA dongle. |

---

## 7. LittleFS Cartridge Profile Engine & JSON Storage Schema

Upon cartridge insertion, the 1-Wire driver queries the 64-bit UID and loads the matching profile from `/storage/profiles/<UID>.json`:

```json
{
  "profile_schema": 2,
  "uid": "01:A4:7B:3F:00:00:00:1E",
  "device_name": "Sena 50S Mesh 2.0 Inlay",
  "hardware_class": "K1",
  "power": {
    "vcc_enabled": true,
    "vcc_voltage_mv": 5000,
    "max_current_ma": 300,
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
    "mode": "sena_mesh_button",
    "pulse_click_ms": 200,
    "pulse_channel_ms": 1000
  },
  "mesh_routing": {
    "dle_bonus_points": 60,
    "protocol_family": "sena_wave_3"
  }
}
```

* **Zero-Trust Fallback (`disabled.json`):** On unrecognized UIDs, electrical shorts, or empty bays, the 5V MOSFET remains off (`vcc_enabled: false`), codec gain drops to `-96 dB`, and DLE score is clamped to `0`.

---

## 8. Modular Hardware Topology & Graceful Degradation (Operation without Pod 3 or Front Node)

OpenMotorBridge is designed from the ground up as a **resilient, fault-tolerant modular architecture**. No subsystem blocks Central Box boot or crashes if optional modules are omitted or unplugged:

| Configuration | Installed Hardware | System Behavior & Graceful Degradation |
| :--- | :--- | :--- |
| **Tier 1: Minimal Core** | Central Box only<br>*(No Pod 3, no Front Node)* | • **Audio Bridge & Intercoms fully operational:** Pod 1 & 2 mix with zero latency.<br>• **CAN-Bus active:** Speed, RPM & BCM telemetry via HD26 pins 17/18 under seat.<br>• **IMU active:** Bosch BMI270 provides lean angle, pitch & vibration sensing.<br>• **UART1 (Pod 3):** Polls with 100 ms timeout without error; reports `has_3d_fix = false`.<br>• **ESP-NOW (Front Node):** Waits in discovery mode; AGC operates at nominal gain.<br>• **DLE Score:** LoRa, GNSS, and Front-Mic capability bits are dynamically omitted. |
| **Tier 2: Cockpit Extension** | Central Box + Front Node<br>*(No Pod 3)* | • All Tier 1 features + 4-Port USB Hub & 20W PD Charger.<br>• Ottocast Watchdog & automatic ignition power-gating enabled.<br>• Handlebar PTT (< 1.8 ms) and dynamic acoustic wind AGC via Knowles MEMS.<br>• CAN-Bus can be tapped at Front Node `J2` or under the seat.<br>• Blind spot mirror LEDs (`J9`) remain dark (no radar attached). |
| **Tier 3: Tail & Radar Extension** | Central Box + Pod 3<br>*(No Front Node)* | • All Tier 1 features + u-blox MAX-M10S GNSS & SX1262 LoRa Mesh.<br>• Garmin Varia / mmWave radar active: Audible warning pings in helmet & WebApp.<br>• Because Front Node is omitted, only mirror LEDs and USB cockpit are absent.<br>• Handlebar control is performed wirelessly via BLE Handlebar Remote (CR2032). |
| **Tier 4: Full System** | Central Box + Front Node + Pod 3 | • 100% of all features: 3-Node mesh, mirror LEDs (8 Hz strobe on TTC hazard), automatic action cam bookmarking on critical radar threats (< 2.5s), and 1-PPS timecode master. |

### 8.1 Zero-Crash Resiliency Mechanisms
1. **Asynchronous Non-Blocking UARTs:** Communications to Pod 3 (UART1) and Radar (UART2) use FreeRTOS timeouts (`pdMS_TO_TICKS(50)` / `100`). There are **zero blocking `while(1)` polling loops** awaiting serial bytes.
2. **Dynamic DLE Capabilities (`omm_get_capabilities_vector`):** Central Box advertises only those hardware flags to the mesh that physically acknowledge presence (`gnss_bridge_is_pod3_connected()`, `is_linked`, `can_bus_is_connected()`).
3. **Sensor-Fusion Autarky (`adr_ekf_filter.cpp`):** If GNSS is absent (or Pod 3 missing), the EKF immediately falls back to **Dead Reckoning** supported by IMU and CAN wheel speed.
4. **Fault-Tolerant Audio Mixer (`audio_dsp_pipeline.cpp`):** If the Front Node Knowles MEMS microphone is absent, the brickwall limiter and AGC level run at a fixed nominal baseline (Unity Gain `1.0f`).
