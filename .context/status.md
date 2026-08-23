# OpenMotorBridge - Current System Context

## Hardware & Architecture (v8.0)
- Topology: 4-Point Satellite (Main Box under seat, Pod 1 Left Sena, Pod 2 Right Cardo, Pod 3 Rear OMM/GNSS)
- Connector: HD26 Flange (IP67) -> Internal 2x13 Ribbon to ESP32-S3 PCB (26 Pins, 0 NC)
- Pod Connection: Symmetrical 6-wire shielded PUR cable (VCC, GND, Audio/UART, Opto/PPS, 1-Wire ID)
- Front/Cockpit: 100% wireless via BLE 5.0 handlebar remote (CR2032 monitored via Service 0x180F)
- BOM: ESP32-S3, ES8388 24-Bit Codec, TCAN334G CAN-FD, LM5164 Buck, BQ24075 UPS with JEITA NTC

## Current Work in Progress
- [x] Docs 01-17 exported to docs/de/ and verified (100% clean formatting)
- [x] Full Firmware Modules (Main ESP32-S3 + Rear ESP32-C3 Pod 3)
  - [x] ESP-IDF v5 I2S DMA Audio DSP with Raised-Cosine Ducking
  - [x] ESP-IDF v5 Oneshot ADC & 3-stage Power Supervisor (KL15/KL30/UPS)
  - [x] Dual-Channel 1-Wire DS2401 Scanner & Profile Loader
  - [x] NimBLE GATT Server (WebBLE PWA) & Central Client (Handlebar SIG 0x180F)
  - [x] 4-Bit SDIO FAT32 BGH Ring Buffer & TLS 1.3 WebDAV Auto-Sync
  - [x] Heck-Pod 3 Co-Processor (MAX-M10S 10Hz, 1-PPS Sync, SX1262 LoRa SPI)
- [x] WebBLE PWA Dashboard v8.0 Fully Implemented
  - [x] Glassmorphism Dark Mode UI (Google Fonts Outfit/Inter, Responsive Grid)
  - [x] Live Fahrdynamik & Schräglagen-Visualisierung (BMI270 15-State EKF)
  - [x] 5-Chemie Starterbatterie-Wahl (AGM, Gel, Nass, LiFePO4, NMC)
  - [x] Audio-Matrix Betriebsmodi, Gain-Slider & Ducking-Control
  - [x] Kassetten-Manager, DLE Leader Score Breakdown & Onboarding Wizard
  - [x] Tour-Manager mit GPX 2.0 Export, Actioncam Marker & WebDAV Sync
  - [x] Reserve I/O Steuerung (Pins 25/26) & Demo-/Simulations-Modus
- [ ] Next: KiCad schematic routing for HD26 pin header & PCBs