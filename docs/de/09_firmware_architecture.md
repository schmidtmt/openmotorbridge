# 09 - Firmware-Architektur (C++ / FreeRTOS)

Die Firmware basiert auf ESP-IDF v5.x und FreeRTOS mit strikter Core-Trennung:

## 1. Core-Aufteilung (ESP32-S3 Dual Core @ 240 MHz)

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      ESP32-S3 FREE RTOS MULTITASKING                   │
 ├────────────────────────────────────┬───────────────────────────────────┤
 │ CORE 0: Kommunikation & System     │ CORE 1: Audio DSP & Echtzeit      │
 ├────────────────────────────────────┼───────────────────────────────────┤
 │ ├─ BLE Server (PWA Dashboard)      │ ├─ I2S Audio DMA Receiver         │
 │ ├─ BLE Client (Lenkertaster 0x180F)│ ├─ Raised-Cosine Ducking Engine   │
 │ ├─ 1-Wire Kassetten-Manager        │ ├─ I2S Audio DMA Transmitter      │
 │ ├─ Opto-Puls-Sequenzer (TLP222A)   │ └─ ADC Peak Level Detector        │
 │ ├─ WebDAV TLS Client (Nextcloud)   │                                   │
 │ └─ SDIO Logging & BGH Purge        │                                   │
 └────────────────────────────────────┴───────────────────────────────────┘

 ```

 ## TLP222A Puls-Synthese
 Tastendrücke werden exakt getaktet:
 - Single Click (Mesh On/Off): $200\,\text{ms} \pm 5\,\text{ms}$ aktiv, $> 300\,\text{ms}$ Pause.
 - Channel Next Pulse: $1000\,\text{ms} \pm 10\,\text{ms}$ aktiv, $> 500\,\text{ms}$ Pause.