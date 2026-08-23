# OpenMotorBridge v8.0 – KiCad Hardware-Projekte & Blockschaltbilder

Dieses Verzeichnis enthält die vollständigen **KiCad 7/8 Schaltplan- und Projektdateien** für das universelle 4-Punkte-Satellitensystem von OpenMotorBridge v8.0.

---

## 📂 Projektübersicht

```
hardware/
├── 3d_models_mjf/                  # PA12 MJF CAD Gehäusedaten (Zentralbox Typ A, Satelliten-Pods Typ B)
├── kicad_main_box/                 # Hauptplatine Zentralbox (Unter Sitzbank)
│   ├── openmotorbridge_main.kicad_pro       # KiCad Projektdatei
│   ├── openmotorbridge_main.kicad_sch       # Top-Level hierarchisches Blockschaltbild
│   ├── power_supply_ups.kicad_sch           # Sheet 1: LM5164-Q1, SMBJ33CA, PPTC, BQ24075, JEITA NTC
│   ├── mcu_codec_can.kicad_sch              # Sheet 2: ESP32-S3, ES8388 24-Bit Codec, TCAN334G CAN-FD, BMI270
│   ├── audio_frontend_isolated.kicad_sch    # Sheet 3: Bourns LM-NP-1001-B1L Übertrager, TLP222A Opto
│   └── hd26_interface.kicad_sch             # Sheet 4: HD26 26-Pin Flansch, 2x13 Wannenstecker, SDIO Slot
├── kicad_rear_pod3/                # Heck-Pod 3 (Heckbürzel / Gepäckträger)
│   ├── openmotorbridge_rear_pod3.kicad_pro  # KiCad Projektdatei
│   └── openmotorbridge_rear_pod3.kicad_sch  # MAX-M10S GNSS, SX1262 LoRa, ESP32-C3 Co-Prozessor
└── kicad_pod_cartridge/            # Universal-Kassette (Pod 1 & Pod 2 Kassetteneinschub)
    ├── openmotorbridge_pod_cartridge.kicad_pro # KiCad Projektdatei
    └── openmotorbridge_pod_cartridge.kicad_sch # 6-Pin Mill-Max Pogo, DS2401 1-Wire ID, TLP222A Interface
```

---

## 🛠️ Platinen-Spezifikation & Fertigungsparameter (JLCPCB / Eurocircuits)

* **Lagenanzahl:** 4 Lagen (Layer 1: High-Speed Signals & RF / Layer 2: Solid GND / Layer 3: Power 3.3V & 5V / Layer 4: Signals & Analog Audio)
* **Basismaterial:** FR4 TG150 (hohe thermische Belastbarkeit für Motorrad-Sitzbankbereich)
* **Oberflächenfinish:** ENIG (Electroless Nickel Immersion Gold) für korrosionsfreie Pogo-Pads und QFN/LGA-Lötungen
* **Platinenstärke:** 1.6 mm ± 10 %
* **Kupferauflage:** 1 oz (35 µm) Außenlagen, 0.5 oz (18 µm) Innenlagen
* **Min. Leiterbahnbreite / Abstand:** 0.127 mm (5 mil) / 0.127 mm (5 mil)
* **Min. Bohrdurchmesser:** 0.3 mm (Via 0.3 mm / 0.6 mm Pad)

---

## 🔌 Schnittstellen-Übersicht (HD26 26-Pin Flansch)

| Pin-Bereich | Zuordnung | Beschreibung |
| :--- | :--- | :--- |
| **Pins 1–6** | **Pod 1 (Links)** | `POD1_VCC`, `POD1_GND`, `POD1_NF_P`, `POD1_NF_N`, `POD1_OPTO`, `POD1_1WIRE_ID` |
| **Pins 7–12** | **Pod 2 (Rechts)** | `POD2_VCC`, `POD2_GND`, `POD2_NF_P`, `POD2_NF_N`, `POD2_OPTO`, `POD2_1WIRE_ID` |
| **Pins 13–18**| **Pod 3 (Heck)** | `POD3_VCC`, `POD3_GND`, `POD3_UART_TX`, `POD3_UART_RX`, `POD3_GNSS_PPS`, `POD3_1WIRE_ID` |
| **Pins 19–24**| **Bordnetz & CAN** | `KL30`, `KL15`, `GND_PWR`, `GND_SHIELD`, `CAN_H`, `CAN_L` |
| **Pins 25–26**| **Dedizierte Reserve** | `RESERVE_GPIO_A` (Multifunktions-Input / PTT), `RESERVE_GPIO_B` (Schaltausgang) |
