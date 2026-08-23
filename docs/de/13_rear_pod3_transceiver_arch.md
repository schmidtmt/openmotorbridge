# 13 - Heck-Pod 3 & Digitale OMM-Transceiver-Architektur

Der Heck-Pod 3 buendelt Positionsbestimmung (GNSS) und digitalen Weitbereichsfunk (OpenMotorMesh) in einem aerodynamischen Gehaeuse am Heckbuerzel oder Gepaecktraeger.

## 1. Hardware-Architektur im Heck-Pod
- **GNSS Engine:** u-blox MAX-M10S mit 25 x 25 mm Keramik-Patchantenne fuer gleichzeitigen 4-System-Empfang (GPS, GLONASS, Galileo, BeiDou).
- **LoRa Transceiver:** Semtech SX1262 (+22 dBm PA, 868 MHz) fuer OpenMotorMesh Weitbereichs-Routing.
- **Co-Prozessor:** ESP32-C3 (32-Bit RISC-V @ 160 MHz) uebernimmt lokales NMEA/UBX-Parsing bei 10 Hz und LoRa Frame En-/Decodierung.
- **Schnittstelle zur Zentralbox:** Geschirmtes 6-Ader-Kabel (VCC 5V, GND, High-Speed UART TX/RX @ 460.800 Baud, 1-PPS Zeit-Sync, 1-Wire ID).

## 2. Vorteile der Auslagerung
- Stoerungsfreie 360-Grad-GNSS-Sicht ohne Daempfung durch Fahrer oder Verkleidung.
- 868-MHz-Sender strahlt am Heck ab - ohne Beeinflussung der 2.4-GHz-Mesh-Systeme an den Seiten.
- Entlastung der Haupt-MCU (ESP32-S3) von Interrupt-Spitzen beim NMEA-Parsing.
