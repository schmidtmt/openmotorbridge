# OpenMotorBridge (OMB) – KI-Systemkontext & Architektur-DNA

## 1. Projekt-Identität & Ziel
OpenMotorBridge v8.0 ist ein universelles, modulares Kfz-Gateway für Motorräder, das proprietäre Intercom-Netze (Sena Mesh 3.0/2.0, Cardo DMC Gen2/Gen1, PMR446) herstellerübergreifend mit Bord-Infotainment-Systemen (z. B. Harley-Davidson Boom! Box GTS / Skyline OS) und Weitbereichs-LoRa (OpenMotorMesh 868 MHz) latenzfrei und isoliert verbindet.

## 2. Unverrückbare Hardware- & Architektur-Entscheidungen (v8.0)
* **Topologie:** 4-Punkte-Satellitensystem zur 100%igen Vermeidung von HF-De-Sensing:
  - **Zentralbox (Unter Sitzbank):** ESP32-S3 Dual-Core, ES8388 24-Bit I2S Audio Codec, TCAN334G CAN-FD Transceiver, LM5164-Q1 Buck (65V), BQ24075 USV (LiPo mit JEITA NTC-Schutz), I2S DSP, SDIO MicroSD (4-Bit). Keine HF-Sender im Inneren.
  - **Pod 1 (Links am Rahmen/Seitendeckel):** Kassette für Sena Intercom.
  - **Pod 2 (Rechts am Rahmen/Seitendeckel):** Kassette für Cardo Intercom / PMR446.
  - **Pod 3 (Heckbürzel/Gepäckträger):** u-blox MAX-M10S GNSS + Semtech SX1262 LoRa (868 MHz) + ESP32-C3 Co-Prozessor (UART @ 460.800 Baud zur Zentralbox).
  - **Cockpit/Front:** 100 % drahtlos über BLE 5.0 (Lenkertaster mit CR2032-Spannungsüberwachung via Service 0x180F) und autarken USB-Hub.
* **Gehäuseschnittstelle Zentralbox:** HD26 IP67 Flanschbuchse in der Gehäusewand. Intern via 26-poligem Flachbandkabel auf 2x13 Wannenstecker auf der Hauptplatine geführt.
* **Kabelbaum & Pinbelegung (26 Pins, 0 NC):**
  - **Pod 1 (Pins 1–6):** VCC, GND, NF_P, NF_N, OPTO, 1WIRE_ID ($1 \times 6$-Ader geschirmt).
  - **Pod 2 (Pins 7–12):** VCC, GND, NF_P, NF_N, OPTO, 1WIRE_ID ($1 \times 6$-Ader geschirmt).
  - **Pod 3 (Pins 13–18):** VCC, GND, UART_TX, UART_RX, GNSS_PPS, 1WIRE_ID ($1 \times 6$-Ader geschirmt).
  - **Bordnetz & Busse (Pins 19–24):** KL30, KL15, GND_PWR, GND_SHIELD, CAN_H, CAN_L.
  - **Reserve-Schnittstellen (Pins 25–26):** RESERVE_GPIO_A (Input/PTT), RESERVE_GPIO_B (Output/Relais).
* **Kassetten-Erkennung & Steuerung:**
  - Standard-Pogo-Leiste (6 Pins: VCC, GND, 2x Signal/NF, Opto/PPS, 1-Wire ID).
  - Kassetten-Identifikation über integrierte DS2401 Silicon Serial Number an port-spezifischen 1-Wire-Leitungen (sofortige, verwechslungssichere Steckplatzerkennung).
  - Tasten-Simulation prellfrei über Toshiba TLP222A PhotoMOS-Halbleiterrelais.
* **EMV- & Batterieschutz:**
  - Mehrstufiger Schutz: SMBJ33CA TVS (53.3V Clamping) + Bourns PPTC-Sicherung (500mA/1A) vor LM5164.
  - JEITA NTC-Temperaturüberwachung: Automatischer Lade-Stopp des LiPo bei < 0 °C (Lithium-Plating-Schutz) und > 45 °C (Sitzbank-Hitzeschutz).
  - Unterstützung aller 5 Bordnetz-Batterietypen (Nass, AGM, Gel, LiFePO4, NMC) mit adaptivem Unterspannungsschutz.

## 3. Firmware- & Software-Prinzipien
* **ESP-IDF v5.x / FreeRTOS:**
  - **Core 0:** Kommunikation (BLE Server, BLE Client Lenkertaster, 1-Wire Scan, WebDAV TLS Upload, SDIO Logging).
  - **Core 1:** Echtzeit-Audio DSP mit Raised-Cosine-Ducking ($< 8\,\text{ms}$ Latenz).
* **BGH-Konformität (BGH VI ZR 233/17 / DSGVO):** Anlassbezogenes Loggen im rollierenden Ringspeicher. Automatisches Überschreiben ältester ungeschützter Tracks bei $< 200\,\text{MB}$ freiem Speicher.
* **Frontend:** 100 % autarke PWA (HTML5, Vanilla ES6, Web Bluetooth API) ohne Cloud-Abhängigkeiten.

## 4. Verworfene Alt-Konzepte (Nicht wieder aufgreifen!)
- *Monolithisches Gehäuse / Tetraeder-Anordnung:* Verworfen wegen HF-Übersteuerung (De-Sensing) und Bauraumrestriktionen.
- *Interne LoRa/GNSS-Mezzanine-Steckkarte in der Zentralbox:* Verworfen zugunsten der Auslagerung in Heck-Pod 3.
- *Kabellose analoge Audio-Verbindung zu den Pods:* Verworfen wegen Latenzen; bleibt fest verdrahtet über Bourns-Übertrager.