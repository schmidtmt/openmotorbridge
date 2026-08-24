# 09 - Firmware-Architektur (C++ / FreeRTOS)

Die Firmware basiert auf ESP-IDF v5.x und FreeRTOS mit strikter CPU-Core-Trennung auf dem ESP32-S3 der Zentralbox sowie dem ESP32-C3 Co-Prozessor des Heck-Pods:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ESP32-S3 DUAL-CORE MCU                          │
├───────────────────────────────────┬────────────────────────────────────┤
│ CORE 0 (Kommunikation & Sensorik) │ CORE 1 (Echtzeit Audio-DSP Engine) │
├───────────────────────────────────┼────────────────────────────────────┤
│ • BLE GATT Server (PWA Dashboard) │ • I2S DMA Codec Receiver & Transm. │
│ • BLE Handlebar Remote Client     │ • Raised-Cosine Ducking Engine     │
│ • Dual 1-Wire Kassetten-Manager   │ • Fast Peak Level Detector         │
│ • OMM High-Speed UART Bridge      │ • Dual-Port Cross-Matrix Routing   │
│ • OMM In-System Flasher Engine    │                                    │
│ • ADR-EKF Dead-Reckoning Filter   │                                    │
│ • SDIO BGH Ringbuffer & WebDAV    │                                    │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 1. Core-Aufteilung (Dual Core @ 240 MHz)

### CORE 0 (Kommunikation & System):
- **BLE Server:** Web-Bluetooth Anbindung für das progressive WebApp-Dashboard (`0x180D`, `0x180A`).
- **BLE Client:** Automatische Koppelung und Batteriestandsüberwachung des Funk-Lenkertasters.
- **1-Wire Kassetten-Manager:** Scannt Port 1 & Port 2 auf DS2401 Silicon Serial ROM IDs und lädt dynamische LittleFS JSON-Profile.
- **Opto-Puls-Sequenzer:** TLP222A Tastensimulation für OEM Sena- / Cardo-Inlays.
- **WebDAV TLS 1.3 Client:** Asynchroner Upload von GPX- und BGH-Tourdateien zu Nextcloud/Synology im Heim-WLAN.
- **SDIO Logging:** 4-Bit High-Speed SD-Karten-Logger mit Ringpuffer und automatischem BGH-Datenschutz-Purge.
- **ADR-EKF Filter:** Sensorfusion aus 10 Hz GNSS-Telemetrie und BMI270 6-Achs IMU für unterbrechungsfreie Navigation in Tunnels.
- **OMM Flasher Engine (`omm_flasher.cpp`):** Synchrones High-Speed UART Push-Flashen des Heck-Pods bei Systemupdates.

### CORE 1 (Audio DSP & Echtzeit):
- **I2S Audio DMA Receiver & Transmitter:** Latenzarmes Streaming über ES8388 Audio-Codec ($f_s = 48\,\text{kHz}, 24\,\text{Bit}$).
- **Raised-Cosine Ducking Engine:** Knackfreie, stetig differenzierbare Audio-Absenkung bei Durchsagen.
- **ADC Peak Level Detector:** Kontinuierliche Überwachung der Mikrofonschwellen und Pegel.

---

## 2. OMM In-System UART-Push-Flasher (`omm_flasher.cpp`)

Um Firmware-Updates für das gesamte Motorradsystem mit einem Klick über das Smartphone durchzuführen, besitzt die Zentralbox eine integrierte SLIP-Loader Engine:

```
┌─────────────────────────┐                ┌─────────────────────────┐
│ ZENTRALBOX (ESP32-S3)   │ 460.800 Baud   │ HECK-POD 3 (ESP32-C3)   │
│                         ├───────────────►│                         │
│ • Liest 'omm_rear.bin'  │ UART TX / RX   │ • Empfängt SLIP Chunks  │
│ • Power-Cycle / Boot-Cmd│                │ • Schreibt Flash        │
│ • MD5 Checksummen-Prüf. │◄───────────────┤ • Reboot ins neue Image │
└─────────────────────────┘ ACK / Status   └─────────────────────────┘
```

### Ablauf des Push-Flashens:
1. **Trigger:** WebApp lädt kombiniertes Firmware-Bundle (`omb_main.bin` + `omm_rear.bin`) auf die Zentralbox.
2. **Bootloader-Einstieg:** Die Zentralbox sendet den Befehl `0xAA 0x55 0xFE 0x01 "BOOT"` über die UART-Leitung und führt einen synchronen Power-Cycle über `POD3_PWR_EN` aus.
3. **ROM-Synchronisation:** 0x08 SLIP-Synchronisations-Frame versetzt den ESP32-C3 in den Download-Modus.
4. **Streaming:** Übertragung in 1024-Byte Blöcken mit 460.800 Baud ($< 6\,\text{Sekunden}$ Gesamtdauer).
5. **Integritätsprüfung:** MD5-Hash-Verifikation und anschließender Warmstart ins neue Image.

---

## 3. TLP222A Puls-Synthese
Tastendrücke werden exakt getaktet:
- **Single Click (Mesh On/Off):** 200 ms aktiv, > 300 ms Pause.
- **Channel Next Pulse:** 1000 ms aktiv, > 500 ms Pause.
