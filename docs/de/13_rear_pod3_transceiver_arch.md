# 13 - Heck-Pod 3 & Digitale OMM-Transceiver-Architektur

Der Heck-Pod 3 bündelt Positionsbestimmung (GNSS) und digitalen Weitbereichsfunk (OpenMotorMesh) in einem aerodynamisch optimierten Gehäuse am Heckbürzel oder Gepäckträger.

## 1. Hardware-Architektur

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                       HECK-POD 3 ELEKTRONIK-KASSETTE                       │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │  ┌───────────────────────────────────┐    ┌──────────────────────────────┐  │
 │  │ 25 x 25 mm Keramik-Patchantenne   │    │ 868 MHz Wendel-/Drahtantenne │  │
 │  └─────────────────┬─────────────────┘    └──────────────┬───────────────┘  │
 │                    ▼                                     ▼                  │
 │  ┌───────────────────────────────────┐    ┌──────────────────────────────┐  │
 │  │ u-blox MAX-M10S GNSS Engine       │    │ Semtech SX1262 LoRa          │  │
 │  │ (GPS, GLONASS, Galileo, BeiDou)   │    │ (+22 dBm PA, 868 MHz OMM)    │  │
 │  └─────────────────┬─────────────────┘    └──────────────┬───────────────┘  │
 │                    │ I2C / UART                          │ SPI              │
 │                    ▼                                     ▼                  │
 │  ┌───────────────────────────────────────────────────────────────────────┐  │
 │  │ ESP32-C3 Co-Prozessor (32-Bit RISC-V @ 160 MHz)                       │  │
 │  │ ├─ Lokales NMEA/UBX-Parsing & 10 Hz Filterung                         │  │
 │  │ ├─ OMM Mesh Routing & LoRa Frame En-/Decodierung                      │  │
 │  │ └─ 1-Wire ID Emulation                                                │  │
 │  └───────────────────────────────────┬───────────────────────────────────┘  │
 └──────────────────────────────────────┼──────────────────────────────────────┘
                                        ▼
                   [ 4-Ader-Interface zur Zentralbox ]
                   Pins: VCC (5V) | UART TX | UART RX | GND
```

## 2. Vorteile der Auslagerung
- Störungsfreie 360°-GNSS-Sicht: Keine Dämpfung durch Fahrer, Beifahrer oder Verkleidungsteile.

- Frequenztrennung: Der 868-MHz-Sender strahlt mit +22 dBm am Heck ab – ohne Beeinflussung der 2,4-GHz-Mesh-Systeme in den vorderen Pods.

- Entlastung der Zentralbox: Die serielle Verbindung (UART @ 460.800 Baud) überträgt vorverarbeitete Binärframes, wodurch die Haupt-MCU von Interrupt-Spitzen entlastet wird.