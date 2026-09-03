# 07 - Hardware-Architektur & Platinen-Pinouts (PCBA 01 bis 05)

Dieses Dokument bildet die **zentrale, autoritative Hardware-Spezifikation aller 5 Platinen-Baugruppen (PCBA 01 bis PCBA 05)** des OpenMotorBridge Gesamtsystems, einschließlich Lagenaufbau, Impedanzkontrolle, Net-Klassen, Funktionszonen und vollständigen Pinout-Tabellen.

---

## 1. Systemübersicht der 5 Platinen-Baugruppen

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   DIE 5 HARDWARE-BAUGRUPPEN (PCBAs) DER OPENMOTORBRIDGE                │
├───────┬───────────────────────────────┬───────────────┬─────────┬──────────────────────┤
│ Baugruppe │ Name & Funktion           │ Abmessungen   │ Lagen   │ Kern-ICs / Controller│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 01**│ **Zentralbox Main Controller** │ 85 x 55 mm    │ 4 Lagen │ ESP32-S3, LM5164,    │
│       │ (Unter der Sitzbank, Audio/USV)│               │ (ENIG)  │ BQ24075, ES8388, IMU │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 02**│ **Satelliten Pod Base Carrier**│ 52 x 32 mm    │ 2 Lagen │ SP3012 TVS, M8 6-Pin,│
│       │ (Sockel für Pod 1 & 2)        │               │         │ Kassetten-Aufnahme   │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 03**│ **Universalschlitten Cartridge**│ 105 x 48 mm   │ 2 Lagen │ DS2401 1-Wire ID,    │
│       │ (Inlay für Sena, Cardo, Funk) │               │         │ TLP222A PhotoMOS Opto│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 04**│ **Rear Pod 3 Transceiver Hub** │ 92 x 44 mm    │ 4 Lagen │ RP2040 Coprozessor,  │
│       │ (Heckbürzel: LoRa & GNSS)     │               │ (ENIG)  │ SX1262 LoRa, NEO-M9N │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 05**│ **Universal Front-Knoten**    │ 72 x 48 mm    │ 4 Lagen │ ESP32-C3 RISC-V,     │
│       │ (Smart Fairing Hub & Ottocast)│               │ (ENIG)  │ USB2512B, TPS2051B   │
└───────┴───────────────────────────────┴───────────────┴─────────┴──────────────────────┘
```

---

## 2. Fertigungsstandard & JLCPCB 4-Lagen Stackup (JLC04161H-7628)

Für alle 4-Lagen-Platinen (PCBA 01, PCBA 04 und PCBA 05) wird der identische, streng impedanzkontrollierte Lagenaufbau verwendet:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1 (F.Cu - Top): High-Speed Signale, USB-Diff, Bauteile│  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielektrikum, Er = 4.4, Dicke 0.2 mm) ──   │
├─────────────────────────────────────────────────────────────┤
│ Layer 2 (In1.Cu): Durchgängige Massefläche (GND_PWR / AGND) │  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── FR4 Core (Isolationskern, Dicke 1.0 mm) ──────────────   │
├─────────────────────────────────────────────────────────────┤
│ Layer 3 (In2.Cu): Power-Planes (VCC_3V3, VCC_5V Polygone)   │  (35 µm Cu)
├─────────────────────────────────────────────────────────────┤
│ ── Prepreg 7628 (Dielektrikum, Er = 4.4, Dicke 0.2 mm) ──   │
├─────────────────────────────────────────────────────────────┤
│ Layer 4 (B.Cu - Bottom): Sekundär-Routing & SMD-Sensorik    │  (35 µm Cu)
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Standardisierte Net-Klassen & Leiterbahn-Geometrien
* **`Default`:** Leiterbahnbreite $0{,}20\,\text{mm}$, Mindestabstand $0{,}20\,\text{mm}$ (Logiksignale, GPIOs).
* **`Power_5V_12V`:** Leiterbahnbreite $0{,}60\,\text{mm}$ (Stromtragfähigkeit bis $2{,}2\,\text{A}$ bei $\Delta T < 10\,^\circ\text{C}$).
* **`RF_50R`:** Leiterbahnbreite $0{,}35\,\text{mm}$, Koplanarabstand $0{,}20\,\text{mm}$ zur Massefläche (50 Ohm Wellenwiderstand für 868 MHz LoRa und GNSS).
* **`USB_90R_DIFF`:** Leiterbahnbreite $0{,}20\,\text{mm}$, differentieller Leiterbahnabstand $0{,}15\,\text{mm}$ ($90\,\Omega \pm 10\,\%$ Differenzimpedanz für USB 2.0 High-Speed 480 Mbps).
* **`Audio_Sensitive`:** Leiterbahnbreite $0{,}25\,\text{mm}$, Abstand $0{,}30\,\text{mm}$ (abgeschirmt durch flankierende GND-Leiterbahnen).

---

## 3. PCBA 01: Zentralbox Main Controller (`openmotorbridge_central_box`)

![PCBA 01 Zentralbox Main Controller](../images/pcba/pcba01_central_box_3d.png)

*Abbildung 7.1: Präzises KiCad 3D-Raytracing-Render der Zentralbox-Hauptplatine (PCBA 01, 85 x 55 mm, 4 Lagen) mit ESP32-S3 WROOM-1, LM5164-Q1 72V Buck, Bourns 1500V Audio-Übertragern, Box-Headers und ENIG-Goldpads.*

### 3.1 Pinbelegung des zentralen 26-poligen Flansch-Steckverbinders (`J1` / HD26)

| Pin (HD26/J1) | Signalname | Signalart / Spannungsbereich | Funktion & Schutzbeschaltung |
| :--- | :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 300 mA) | Stromversorgung Lenker-Pod 1 (High-Side Switch) |
| **Pin 2** | `POD1_NF_P` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T1` (Positiv) |
| **Pin 3** | `POD1_NF_N` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T1` (Negativ) |
| **Pin 4** | `POD1_OPTO_KEY` | Optokoppler PTT-Keying | PhotoMOS `U7` Open-Collector / Schließer |
| **Pin 5** | `POD2_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 300 mA) | Stromversorgung Helm-Pod 2 (High-Side Switch) |
| **Pin 6** | `POD2_NF_P` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T2` (Positiv) |
| **Pin 7** | `POD2_NF_N` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T2` (Negativ) |
| **Pin 8** | `POD2_OPTO_KEY` | Optokoppler Mute/Keying | PhotoMOS `U8` Open-Collector / Schließer |
| **Pin 9** | `POD3_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 500 mA) | Stromversorgung Heck-Transceiver Pod 3 |
| **Pin 10** | `POD3_UART_TX` | UART TX ($3{,}3\,\text{V}$, 115200 Baud) | Datenleitung zu Pod 3 (GNSS/Telemetrie) |
| **Pin 11** | `POD3_UART_RX` | UART RX ($3{,}3\,\text{V}$, 115200 Baud) | Datenleitung von Pod 3 (GNSS/Telemetrie) |
| **Pin 12** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Hauptmasse für Pod-Stromversorgungen |
| **Pin 13** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Paralleler Massepfad für geringen Widerstand |
| **Pin 14** | `KL30_IN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Dauerplus) | Batterie-Haupteingang (LM5164 Buck, TVS-geschützt) |
| **Pin 15** | `KL15_IGN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Zündungsplus) | Zündungssignal mit Spannungsteiler & Schmitt-Trigger |
| **Pin 16** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Fahrzeug-Bordnetz-Masse |
| **Pin 17** | `CAN_H` | CAN High (ISO 11898-2) | CAN-FD Busleitung High ($120\,\Omega$ Terminierung) |
| **Pin 18** | `CAN_L` | CAN Low (ISO 11898-2) | CAN-FD Busleitung Low ($120\,\Omega$ Terminierung) |
| **Pin 19** | `ONEWIRE_ID` | 1-Wire Datenbus ($3{,}3\,\text{V}$) | Automatische Pod- & Zubehörerkennung (DS2431) |
| **Pin 20** | `GND_SHIELD` | Gehäuse- & Schirmmasse | Direkte Verbindung zum Alugehäuse / Schirmgeflecht |
| **Pin 21** | `AGND` | Analoge Audiomasse | Ruhige Audiomasse für Codec-Referenz |
| **Pin 22** | `RESERVE_GPIO_A`| GPIO Digital I/O ($3{,}3\,\text{V}$) | Frei programmierbarer GPIO / PWM-Ausgang |
| **Pin 23** | `RESERVE_GPIO_B`| GPIO Digital I/O ($3{,}3\,\text{V}$) | Frei programmierbarer GPIO / ADC-Eingang |
| **Pin 24** | `I2S_DOUT` | I2S Data Out ($3{,}3\,\text{V}$) | Digitaler Audio-Stream zu externem DSP/Verstärker |
| **Pin 25** | `I2S_BCLK` | I2S Bit Clock ($3{,}3\,\text{V}$) | Digitaler I2S Takt |
| **Pin 26** | `GND_SHIELD` | Gehäuse- & Schirmmasse | Zweiter Schirmkontakt für 360°-Rundumschirmung |

---

## 4. PCBA 02: Satelliten Pod Base Carrier (`openmotorbridge_pod_base`)

![PCBA 02 Satelliten Pod Base Carrier](../images/pcba/pcba02_pod_base_3d.png)

*Abbildung 7.2: KiCad 3D-Render der Pod-Basisplatine (PCBA 02, 52 x 32 mm, 2 Lagen) mit 6-poliger Präzisions-Stiftleiste, M8 6-Pin IP67 Buchsenanschluss und SP3012 TVS-Schutzarray.*

Die Pod-Base-Platine bildet die fest im Gehäusesockel verschraubte Übergabeschnittstelle zwischen dem M8-Zuleitungskabel und der auswechselbaren Kassette:

### 4.1 M8 6-Pin Steckerbelegung (Eingangsseite)
* **Pin 1:** `+5V_VBUS` (Speisung vom Main Controller, geschützt über PolySwitch PPTC 500mA)
* **Pin 2:** `NF_AUDIO_P` (Positives differenzielles NF-Audiosignal)
* **Pin 3:** `NF_AUDIO_N` (Negatives differenzielles NF-Audiosignal)
* **Pin 4:** `OPTO_TRIGGER` (Optokoppler-Tastleitung zum Intercom)
* **Pin 5:** `ONEWIRE_DATA` (1-Wire Datenleitung zum DS2401 ID-Chip)
* **Pin 6:** `GND` (Gemeinsame Masse)

---

## 5. PCBA 03: Universalschlitten Cartridge (`openmotorbridge_pod_cartridge`)

![PCBA 03 Universalschlitten Cartridge](../images/pcba/pcba03_pod_cartridge_3d.png)

*Abbildung 7.3: KiCad 3D-Render des Universalschlitten-Kassettenträgers (PCBA 03, 105 x 48 mm, 2 Lagen) mit DS2401 1-Wire ID-Chip, horizontaler Mating-Buchse und Headset-JST-SH Schnittstelle.*

Nimmt die eigentliche Headset-Elektronik oder das Adapter-Cradle auf:
* **DS2401 ID-Chip:** Auf `B.Cu` verlötet; sendet beim Einstecken die eindeutige Hardware-UID.
* **Toshiba TLP222A:** PhotoMOS-Relais für PTT-Tastung (< 1 ms prellfrei).
* **6-Pin JST-SH Header `J2`:** Führt `GND`, `5V_VBUS`, `AUDIO_R+`, `AUDIO_R-`, `MIC_IN+` und `OPTO_PTT`.
* **CTIA 3.5mm Buchse:** Ermöglicht den direkten Anschluss kabelgebundener Headsets oder Handfunkgeräte.

---

## 6. PCBA 04: Rear Pod 3 Transceiver & Coprozessor (`openmotorbridge_rear_pod3`)

![PCBA 04 Rear Pod 3 Transceiver Hub](../images/pcba/pcba04_rear_pod3_3d.png)

*Abbildung 7.4: KiCad 3D-Render der Heck-Pod 3 Transceiverplatine (PCBA 04, 110 x 52 mm, 4 Lagen) mit RP2040 Coprozessor, Semtech SX1262 LoRa, u-blox Multi-GNSS und U.FL/Murata MM8030 HF-Umschaltports.*

Sitzt im strömungsgünstigen Heckbürzel und vereint die Weitbereichs-Funkinfrastruktur:

```
┌────────────────────────────────────────────────────────────────────────┐
│               PCBA 04: REAR POD 3 COPROZESSOR & HF-ARCHITEKTUR         │
├──────────────────────────────────────┬─────────────────────────────────┤
│ u-blox NEO-M9N Multi-Konstellation   │ Semtech SX1262 LoRa Transceiver │
│ • GPS, Galileo, Glonass, BeiDou      │ • 868 MHz EU ISM (+22 dBm PA)   │
│ • 10 Hz Dead-Reckoning Engine        │ • 50 Ohm koplanarer HF-Pfad     │
│ • Aktive 3.3V LNA Phantom-Speisung   │ • SMA- / Draht-Monopol Antenne  │
├──────────────────────────────────────┴─────────────────────────────────┤
│ Raspberry Pi RP2040 Dual-Cortex-M0+ Coprozessor (133 MHz, 2MB Flash)   │
│ • NMEA & UBX High-Speed Parsing (460.800 Baud UART)                    │
│ • OMM LoRa Paketierung & 1-PPS Framegenaue Zeitsynchronisation         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`)

![PCBA 05 Universal Front-Knoten](../images/pcba/pcba05_front_node_3d.png)

*Abbildung 7.5: KiCad 3D-Render des Universal Front-Knotens (PCBA 05, 68 x 44 mm, 4 Lagen) mit ESP32-C3 RISC-V, Microchip USB2512B High-Speed Hub, TI TPS2051B Power-Gate und Knowles I2S MEMS Mikrofon.*

Die neu entwickelte Verkleidungs- und Cockpit-Platine für Motorräder mit Frontverkleidung (Harley Touring, BMW GS/RT, etc.):

```
┌────────────────────────────────────────────────────────────────────────┐
│               PCBA 05: UNIVERSAL FRONT-KNOTEN ARCHITEKTUR              │
├────────────────────────────────────────────────────────────────────────┤
│ 1. KONTROLLER & HF:                                                    │
│    • ESP32-C3-WROOM-02U (160 MHz RISC-V, 4MB Flash, ext. U.FL Antenne) │
│    • ESP-NOW 2.4 GHz Ultra-Low-Latency Funkbrücke (< 0.9 ms Flugzeit)  │
├────────────────────────────────────────────────────────────────────────┤
│ 2. USB 2.0 HIGH-SPEED HUB:                                             │
│    • Microchip USB2512B-AEZG Hub Controller (480 Mbps)                 │
│    • 90 Ohm symmetrisch geroutete Differenzpaare (USB_90R_DIFF)        │
├────────────────────────────────────────────────────────────────────────┤
│ 3. OTTOCAST POWER-GATE:                                                │
│    • TI LMR36015 Synchroner Buck (5.00V / 2.0A, 91.8% Wirkungsgrad)    │
│    • TI TPS2051B High-Side Lastschalter (1.05A Current Clamp, Soft-St.)│
│    • 1-Klick Kaltstart (2.5s Puls) & Auto-Café 60s WLAN-Freigabe       │
├────────────────────────────────────────────────────────────────────────┤
│ 4. DIGITALES MEMS FAHRTWIND-MIKROFON:                                  │
│    • Knowles SPH0645LM4H I2S Digitalmikrofon (65.4 dB SNR, 120 dBA AOP)│
│    • Biquad A-Weighting Filter zur dynamischen Helm-Lautstärkeregelung │
└────────────────────────────────────────────────────────────────────────┘
```

### 7.1 Steckverbinder & Schnittstellen der Front-Knoten-Platine
* **`J7` (12V Bordnetz-Eingang):** 2-Pin Schraubklemme / JST-GH ($9\dots 36\,\text{V}$ KL15 Zündungsplus & Fahrzeugmasse).
* **`J1` (Ottocast CarPlay USB-A Port 1):** Geschalteter VBUS über TPS2051B.
* **`J2` (Handschuhfach / Smartphone USB-C Port 2):** Dauerhafter 5V VBUS für Handyladung.
* **`J3` (Lenker-PTT Schnittstelle):** 2-Pin JST-GH zum batteriefreien mechanischen Lenkertaster (GPIO 0 Interrupt).
* **`J4` (Cockpit-CAN Bus):** 3-Pin JST-GH (`CAN_H`, `CAN_L`, `GND`) für Motorräder mit Verkleidungs-CAN.
