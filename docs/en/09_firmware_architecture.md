# 09 - Firmware Architecture, FreeRTOS Tasks & Rollback-OTA

This document specifies the system-wide firmware architecture of OpenMotorBridge v8.0: the multi-core allocation of the ESP32-S3 host MCU, the coprocessors (RP2040 in Rear Pod 3 and ESP32-C3 in the Front Node), the **ESP-NOW low-latency protocol (< 1.8 ms)**, the LittleFS profile engine, and the **Dual-Bank Rollback-OTA architecture** guaranteeing zero bricking during power interruptions.

---

## 1. Multi-Core & Multi-MCU System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 3 FIRMWARE CONTROLLERS IN CONCERT                           │
├──────────────────────────────────────┬─────────────────────────┬───────────────────────┤
│ 1. CENTRAL BOX (ESP32-S3 Dual-Core)  │ 2. REAR POD 3 (RP2040)  │ 3. FRONT NODE (ESP-C3)│
├──────────────────────────────────────┼─────────────────────────┼───────────────────────┤
│ • Core 0: BLE, WebDAV, SDIO, ESP-NOW │ • Core 0: NMEA/UBX 10Hz │ • FreeRTOS Single-Core│
│ • Core 1: Realtime 48kHz Audio DSP   │ • Core 1: LoRa SX1262   │ • I2S MEMS Filter     │
│ • LittleFS Cartridge Profile Engine  │ • 1-PPS Timecode Sync   │ • VBUS Power Switch   │
└──────────────────────────────────────┴─────────────────────────┴───────────────────────┘
```

### 1.1 ESP32-S3 Core Allocation (240 MHz)

#### CORE 0 (Communication, Telemetry & System):
- **BLE GATT Server:** Web-Bluetooth connection for the PWA dashboard (`0x180D`, `0x180A`).
- **ESP-NOW Front Node Client (`esp_now_front_node_client.cpp`):** Handles zero-latency handlebar PTT events ($< 1{,}8\,\text{ms}$) and Knowles MEMS dB(A) noise telemetry.
- **Dual 1-Wire Cartridge Manager:** Polls DS2401 ROM IDs on Ports 1 & 2 to dynamically mount LittleFS JSON profiles.
- **Opto-Pulse Sequencer:** Toshiba TLP222A button synthesis for OEM Sena/Cardo inlays.
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
2. **ESP32-C3 GPIO Interrupt:** $35\,\mu\text{s}$ ISR execution time.
3. **ESP-NOW Radio Transmission (2.4 GHz):** $0{,}90\,\text{ms}$ over-the-air flight time (99.8% PDR).
4. **Central Box ESP32-S3 Core 0 ISR:** $45\,\mu\text{s}$ frame decode & pin toggle.
5. **Toshiba TLP222A Optocoupler:** $0{,}50\,\text{ms}$ turn-on time $t_{\text{ON}}$.
* **Total Glass-to-Glass Latency:** **$1{,}74\,\text{ms}$** (far below the human perceptual threshold of 10 ms).

---

## 3. Dual-Bank Rollback-OTA Partitioning

To completely eliminate the risk of bricking when the vehicle ignition is turned off during an update:

```csv
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x4000,
otadata,  data, ota,     0xd000,  0x2000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x180000,
ota_0,    app,  ota_0,   0x190000,0x140000,
ota_1,    app,  ota_1,   0x2d0000,0x140000,
storage,  data, littlefs,0x410000,0x3f0000,
```

* **Automatic Rollback:** The bootloader verifies firmware image integrity via SHA-256 before committing. If power cuts out mid-flash, the bootloader automatically reverts to the previous working slot (`ota_0`) $\rightarrow$ **0.0% brick risk**.

---

## 4. In-System UART Push-Flasher (`omm_flasher.cpp`)

For firmware updates of Rear Pod 3 without dismantling the vehicle cowl:
* The Central Box reads `omm_rear.bin` from the storage partition and commands the RP2040 coprocessor via UART sequence `0xAA 0x55 0xFE 0x01 "BOOT"` into bootloader mode.
* The flash transfer runs at $460,800\,\text{Baud}$ in 1024-byte chunks with CRC-16 error checking (< 6 seconds duration).

---

## 5. TLP222A Optocoupler Pulse Synthesis & Button Simulation

Button presses are synthesized with sub-millisecond precision to trigger OEM headsets according to exact manufacturer specifications:

| Command / Gesture | Pulse Duration ($t_{\text{ON}}$) | Release Time ($t_{\text{OFF}}$) | Function & Headset Response |
| :--- | :---: | :---: | :--- |
| **Single Click (Mesh On/Off)** | $200\,\text{ms}$ | $> 300\,\text{ms}$ | Toggles Open Mesh or DMC group talk (Sena Mesh button, Cardo Intercom). |
| **Double Click (Radio / Pair)** | 2x $150\,\text{ms}$ | $150\,\text{ms}$ | Activates FM radio or switches between music and intercom. |
| **Channel Next (Channel Cycle)**| $1000\,\text{ms}$ | $> 500\,\text{ms}$ | Advances to the next channel in Sena Open Mesh (Channels 1 through 9). |
| **Long Press (Power Toggle)** | $3500\,\text{ms}$ | $> 1000\,\text{ms}$ | Powers the headset fully ON or OFF. |
| **Mute Toggle (Mute Mic)** | $500\,\text{ms}$ | $> 300\,\text{ms}$ | Temporarily mutes the rider microphone. |

---

## 6. FreeRTOS Task Architecture & Scheduling Matrix (All 3 MCUs)

The overall system orchestrates 13 specialized tasks across 3 physically separated microcontrollers with deterministic priorities and core affinities:

| Task Name | MCU / Core | Priority | Stack | Trigger / Rate | IPC / Interface | Responsibility & Function |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **`audio_dsp_task`** | ESP32-S3 (Core 1) | **24** | 8 KB | 48 kHz DMA ISR | FreeRTOS StreamBuffer | Zero-latency I2S audio mix, Raised-Cosine ducking & AGC. |
| **`esp_now_rx_task`** | ESP32-S3 (Core 0) | **22** | 4 KB | Event-Queue | Direct-to-Task Notify | Handles Front Node PTT events ($< 1{,}8\,\text{ms}$) & noise RMS. |
| **`opto_seq_task`** | ESP32-S3 (Core 0) | **18** | 2 KB | Event-Queue | FreeRTOS Queue | Synthesizes bounce-free pulses to TLP222A PhotoMOS relays. |
| **`adr_ekf_task`** | ESP32-S3 (Core 0) | **15** | 4 KB | 50 Hz Timer | I2C / CAN Buffer | 15-State Kalman filter (GNSS + IMU + wheel speed). |
| **`ble_server_task`** | ESP32-S3 (Core 0) | **10** | 4 KB | Event-Driven | NimBLE Stack | Web-Bluetooth PWA dashboard (GATT services `0x180D`/`0x180A`). |
| **`sdio_log_task`** | ESP32-S3 (Core 0) | **8** | 8 KB | 10 Hz Ringbuffer | FreeRTOS RingBuffer | 4-Bit SDIO blackbox telemetry logging with ECDSA SHA-256. |
| **`onewire_task`** | ESP32-S3 (Core 0) | **5** | 2 KB | 0.5 Hz cyclic | Bit-Banging Driver | Polls DS2401 Silicon Serial ROM IDs on Pods 1 & 2. |
| **`webdav_sync_task`**| ESP32-S3 (Core 0) | **3** | 8 KB | Graceful Shutdown | LwIP TLS 1.3 | Automatic GPX tour upload via home Wi-Fi upon ignition OFF. |
| **`rear_nmea_task`** | RP2040 (Core 0) | **High**| 2 KB | 10 Hz DMA | UART0 (460.8k Baud) | High-speed UBX/NMEA parsing & 1-PPS timecode capture. |
| **`rear_lora_task`** | RP2040 (Core 1) | **High**| 2 KB | SX1262 IRQ | SPI0 Bus | 868 MHz LoRa mesh packet scheduling & emergency voice. |
| **`front_ptt_task`** | ESP32-C3 | **24** | 2 KB | GPIO 0 Edge ISR | ESP-NOW TX Queue | Transmits handlebar PTT transitions in under $0{,}9\,\text{ms}$. |
| **`front_mems_task`** | ESP32-C3 | **18** | 4 KB | 48 kHz DMA | Biquad Filter | Knowles SPH0645 MEMS acoustic A-weighting & RMS tracking. |
| **`front_pwr_task`** | ESP32-C3 | **10** | 2 KB | 10 Hz Timer | GPIO Load Switch | TPS2051B 1-click cold restart (2.5s) & Auto-Café 60s timer. |

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
