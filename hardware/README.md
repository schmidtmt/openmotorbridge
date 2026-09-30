# OpenMotorBridge v8.5 / v9.0 - KiCad Hardware-Baukasten (Clean All-UWB Architecture)

Dieses Verzeichnis enthält die vollständigen **KiCad 10 Schaltplan-, PCB- und Produktionsdateien** für die drahtlose **All-UWB & Pure-DC Architektur** von OpenMotorBridge.

---

## 📂 Das bereinigte 6-Platinen-Lineup

Durch den konsequenten Einsatz von Ultra-Wideband (Qorvo DW3110 6.5 GHz Ch. 5, $< 0{,}4\,\text{ms}$) und Bluetooth entfällt jegliche Signal- und NF-Audioverdrahtung über den Rahmen. Der Kabelbaum besteht ausschließlich aus robusten **2-Draht-DC-Power-Peitschen** (+5V/GND bzw. +12V/GND). 

Die Pod-Platine (`PCBA 02`) und der Heck-Pod (`PCBA 04`) sind ersatzlos entfallen - der Baukasten besteht aus **exakt 6 aktiven PCBAs**:

| PCBA | Baugruppe & Funktion | Maße / Lagen | Kern-Komponenten / RF |
| :--- | :--- | :--- | :--- |
| **PCBA 01** | **Zentralbox Main Controller**<br>*(Unter Sitzbank, Audio-DSP, USV)* | 85 x 55 mm<br>4 Lagen (ENIG) | ESP32-S3, ES8388 24-Bit Codec, TCAN334G CAN-FD, LM5164-Q1, SX1262 LoRa (Top), DW3110 UWB (Bottom), SW1 Taster |
| **PCBA 03** | **Universal Smart Cartridge Rev 3.0**<br>*(Autarker UWB-Funkschlitten)* | 35 x 25 mm<br>2 Lagen (ENIG, 2-seitig SMT) | Qorvo DW3110 UWB, SPI Host-MCU, 4x AO3400A MOSFETs, 2P Frontkontakt (+5V/GND), DNP-Codec |
| **PCBA 05** | **Universal Front-Knoten**<br>*(Cockpit Hub, Sensorik, Audio, USB-PD)* | 82 x 50 mm<br>4 Lagen (ENIG) | ESP32-S3, DW3110 UWB, SAM-M10Q, USB2514B Hub, Dual SW3526 PD20W, Qi 12V, BSD LEDs |
| **PCBA 06** | **MagSafe Frame Dock Adapter**<br>*(Rahmendock M8 auf 2-Pin MagSafe)* | 28 x 11.5 mm<br>2 Lagen (1 oz) | 2 Pogo-Pins (+5V / GND), TVS Diode, 16V PPTC Polyfuse |
| **PCBA 07** | **2-in-1 LoRa Smart-Keyfob & Pager**<br>*(Taschen-Pager, N52 Key & Qi)* | 38 x 19 mm<br>2 Lagen (ENIG) | Nordic nRF52840 SoC, Semtech SX1262 LoRa, DRV2605L Haptik, BQ51003 Qi RX |
| **PCBA 08** | **Radar 2.0 Sub-MCU & Wings**<br>*(Wheeltec 77GHz MR20 + Halo LED)* | 115 x 65 mm<br>2 Lagen (ENIG) | ESP32 Sub-MCU (UWB DW3110), 36x WS2812B LEDs, 2-Pin 12V Power |

---

## 🔌 Zentraler Bordnetz-Stecker (Deutsch DTM-12 Automotive)

Die Zentralbox nutzt einen robusten, wasserdichten **Deutsch DTM-12 Industriestecker** (11 aktive Kontakte):

| Pin | Signalname | Funktion | Querschnitt / Ziel |
| :---: | :--- | :--- | :--- |
| **1** | `KL30_IN` | 12V Dauerplus | AWG20 (0.50 mm²) / Bordnetz |
| **2** | `KL15_IGN` | 12V Zündungsplus | AWG22 (0.34 mm²) / Zündung |
| **3** | `VEHICLE_GND`| Hauptmasse (KL31) | AWG20 (0.50 mm²) / Rahmen |
| **4** | `CAN_H` | Fahrzeug-CAN High | AWG24 (0.22 mm²) / Twisted Pair |
| **5** | `CAN_L` | Fahrzeug-CAN Low | AWG24 (0.22 mm²) / Twisted Pair |
| **6** | `POD1_VCC` | 5V Switched Power Bucht 1 (Links) | AWG22 (0.34 mm²) / JWPF 2P |
| **7** | `POD1_GND` | Masse Bucht 1 (Links) | AWG22 (0.34 mm²) / JWPF 2P |
| **8** | `POD2_VCC` | 5V Switched Power Bucht 2 (Rechts) | AWG22 (0.34 mm²) / JWPF 2P |
| **9** | `POD2_GND` | Masse Bucht 2 (Rechts) | AWG22 (0.34 mm²) / JWPF 2P |
| **10**| `RADAR_PWR` | 12V Switched Power Radar Heck | AWG22 (0.34 mm²) / JWPF 2P |
| **11**| `RADAR_GND` | Masse Radar | AWG22 (0.34 mm²) / JWPF 2P |
| **12**| `CHASSIS_EARTH` | Gehäuseschirm / Rahmenerde | AWG20 (0.50 mm²) |

---

## 🛠️ Fertigung & Validierung (JLCPCB / Eurocircuits)

* **Produktionspakete generieren:**
  ```bash
  python3 hardware/scripts/export_manufacturing_packages.py
  ```
* **JLCPCB DFM & Netlist-Verifikation:**
  ```bash
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 hardware/scripts/verify_pcb_designs_jlcpcb.py
  ```

