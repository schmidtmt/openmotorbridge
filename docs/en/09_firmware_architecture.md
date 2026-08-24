# 09 - Firmware Architecture (C++ / FreeRTOS / ESP-IDF v5.x)

The firmware is built on ESP-IDF v5.x and FreeRTOS with strict CPU core isolation between the ESP32-S3 (Central Box) and ESP32-C3 (Rear Pod Coprocessor):

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ESP32-S3 DUAL-CORE MCU                          │
├───────────────────────────────────┬────────────────────────────────────┤
│ CORE 0 (Communication & Sensors)  │ CORE 1 (Real-Time Audio DSP)       │
├───────────────────────────────────┼────────────────────────────────────┤
│ • BLE GATT Server (PWA Dashboard) │ • I2S DMA Codec Receiver & Transm. │
│ • BLE Handlebar Remote Client     │ • Raised-Cosine Ducking Engine     │
│ • Dual 1-Wire Cartridge Manager   │ • Fast Peak Level Detector         │
│ • OMM High-Speed UART Bridge      │ • Dual-Port Cross-Matrix Routing   │
│ • OMM In-System Flasher Engine    │                                    │
│ • ADR-EKF Dead-Reckoning Filter   │                                    │
│ • SDIO BGH Ringbuffer & WebDAV    │                                    │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 1. Dual-Core Task Distribution (@ 240 MHz)

### CORE 0 (Communication & System Management):
- **BLE Server:** Web-Bluetooth interface for the progressive WebApp dashboard (`0x180D`, `0x180A`).
- **BLE Client:** Automated pairing and battery telemetry monitoring for handlebar remotes.
- **1-Wire Cartridge Manager:** Scans Port 1 & Port 2 for DS2401 Silicon Serial ROM IDs and applies LittleFS JSON profiles.
- **Opto-Pulse Sequencer:** TLP222A button synthesis for OEM Sena / Cardo inlays.
- **WebDAV TLS 1.3 Client:** Asynchronous background upload of GPX / BGH tour logs to Nextcloud / Synology over home Wi-Fi.
- **SDIO Logger:** 4-bit high-speed SD card logger with circular ring buffer and automated BGH privacy purge.
- **ADR-EKF Filter:** 15-state sensor fusion combining 10 Hz GNSS telemetry with Bosch BMI270 6-axis IMU for dead reckoning in tunnels.
- **OMM Flasher Engine (`omm_flasher.cpp`):** Synchronous high-speed UART push-flashing for the Rear Pod during one-click system updates.

### CORE 1 (Real-Time Audio DSP Engine):
- **I2S Audio DMA Receiver & Transmitter:** Ultra-low-latency streaming via ES8388 audio codec ($f_s = 48\,\text{kHz}, 24\,\text{bit}$).
- **Raised-Cosine Ducking Engine:** Click-free, smooth continuously-differentiable audio attenuation for navigation voice prompts.
- **ADC Peak Level Detector:** Continuous monitoring of microphone thresholds and speech presence.

---

## 2. OMM In-System UART-Push-Flasher (`omm_flasher.cpp`)

To enable one-click firmware updates for the entire motorcycle system directly from the smartphone, the Central Box integrates an automated SLIP-loader engine:

```
┌─────────────────────────┐                ┌─────────────────────────┐
│ CENTRAL BOX (ESP32-S3)  │ 460,800 Baud   │ REAR POD 3 (ESP32-C3)   │
│                         ├───────────────►│                         │
│ • Reads 'omm_rear.bin'  │ UART TX / RX   │ • Receives SLIP Chunks  │
│ • Power-Cycle / Boot-Cmd│                │ • Flashes NOR storage   │
│ • MD5 Hash Verification │◄───────────────┤ • Reboots into new app  │
└─────────────────────────┘ ACK / Status   └─────────────────────────┘
```

### Push-Flashing Workflow:
1. **Trigger:** WebApp transfers combined firmware package (`omb_main.bin` + `omm_rear.bin`) to the Central Box.
2. **Bootloader Entry:** Central Box transmits command `0xAA 0x55 0xFE 0x01 "BOOT"` over UART and executes a synchronous 100 ms power-cycle via `POD3_PWR_EN`.
3. **ROM Synchronization:** 0x08 SLIP synchronization frame locks the ESP32-C3 into ROM download mode.
4. **Streaming:** 1024-byte block streaming at 460,800 baud ($< 6\,\text{seconds}$ total duration).
5. **Integrity Check:** MD5 hash validation and automatic warm reboot into the active application.

---

## 3. TLP222A Pulse Synthesis
Button pulses are precisely synthesized:
- **Single Click (Mesh On/Off):** 200 ms active, > 300 ms idle.
- **Channel Next Pulse:** 1000 ms active, > 500 ms idle.
