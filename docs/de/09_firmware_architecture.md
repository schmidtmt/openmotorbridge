# 09 - Firmware-Architektur (C++ / FreeRTOS)

Die Firmware basiert auf ESP-IDF v5.x und FreeRTOS mit strikter CPU-Core-Trennung auf dem ESP32-S3:

## 1. Core-Aufteilung (Dual Core @ 240 MHz)
- **CORE 0 (Kommunikation & System):**
  - BLE Server (PWA Dashboard Verbindung)
  - BLE Client (Lenkertaster mit Batterie-Service 0x180F)
  - 1-Wire Kassetten-Manager (DS2401 ROM Search)
  - Opto-Puls-Sequenzer (TLP222A)
  - WebDAV TLS 1.3 Client (Nextcloud / Synology)
  - SDIO Logging & BGH Purge Manager
- **CORE 1 (Audio DSP & Echtzeit):**
  - I2S Audio DMA Receiver & Transmitter
  - Raised-Cosine Ducking Engine
  - ADC Peak Level Detector

## 2. TLP222A Puls-Synthese
Tastendruecke werden exakt getaktet:
- **Single Click (Mesh On/Off):** 200 ms aktiv, > 300 ms Pause.
- **Channel Next Pulse:** 1000 ms aktiv, > 500 ms Pause.
