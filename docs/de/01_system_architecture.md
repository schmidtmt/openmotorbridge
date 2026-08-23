# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

## 1. Problemstellung & Architekturphilosophie
Klassische Motorrad-Intercom-Systeme sind stark fragmentiert (Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, PMR446, proprietäre Infotainment-Systeme). Frühere Versuche einer Integration scheiterten an massiven Kabelbäumen, ungelösten EMV-/HF-Interferenzen bei multiplen 2,4-GHz-Sendern und fahrzeugspezifischen Monolith-Gehäusen.

OpenMotorBridge v8.0 setzt verbindlich auf eine **universelle 4-Punkte-Satelliten-Topologie**:
* **Zentrale Steuerbox (Unter Sitzbank):** Reine Audio-Routing-, Verarbeitungs- und Versorgungseinheit (ESP32-S3, Dual-BT Audio, DSP, USV, SDIO-Speicher).
* **Satelliten-Pod 1 (Linke Fahrzeugseite):** Kassetten-Einschub für Primär-Intercom (z. B. Sena Apex / Spider).
* **Satelliten-Pod 2 (Rechte Fahrzeugseite):** Kassetten-Einschub für Sekundär-Intercom (z. B. Cardo DMC Gen2 / Midland PMR).
* **Satelliten-Pod 3 (Heckträger / Kennzeichenhalter):** GNSS-Patchantenne (360°-Sicht) und OpenMotorMesh (SX1262 LoRa 868 MHz) mit integriertem Co-Prozessor.
* **Cockpit / Front:** 100 % drahtlos über BLE 5.0 (Lenkertaster mit CR2032-Monitoring) und autarker USB-Hub in der Frontverkleidung.

## 2. HF-Koexistenz & Raumdiversität
Durch die Montage von Pod 1 links und Pod 2 rechts wird ein physischer Abstand von mindestens $40\text{--}50\,\text{cm}$ gewährleistet. Der Fahrzeugrahmen, die Starterbatterie und der Heckfender fungieren als massive HF-Schirmwand, was eine Entkopplung von $> 35\,\text{dB}$ zwischen den 2,4-GHz-Mesh-Sendern garantiert.

| Knotenpunkt | Position | Bestückung / Funk | Verbindung zur Zentralbox |
| :--- | :--- | :--- | :--- |
| **Zentralbox** | Unter Sitzbank | ESP32-S3 (BLE/WLAN), Dual BT-Audio, DSP, USV | Zentraler Sternpunkt |
| **Pod 1** | Links (Seitendeckel / Rahmen) | Kassette Sena Apex / Spider (2,4 GHz Mesh) | Geschirmtes 4-Ader-Kabel (NF + Power + Control) |
| **Pod 2** | Rechts (Seitendeckel / Rahmen) | Kassette Cardo DMC Gen2 (2,4 GHz DMC) | Geschirmtes 4-Ader-Kabel (NF + Power + Control) |
| **Pod 3** | Heck (Gepäckbrücke / Kennzeichen) | u-blox MAX-M10S GNSS + OMM (868 MHz LoRa) | Geschirmtes 4-Ader-Kabel (UART + Power) |