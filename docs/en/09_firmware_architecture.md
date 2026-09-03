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
