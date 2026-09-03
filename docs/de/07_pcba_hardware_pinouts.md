# 07 - Hardware-Architektur & Platinen-Pinouts (PCBA 01 bis 05)

Dieses Dokument bildet die **zentrale, autoritative Hardware-Spezifikation aller 5 Platinen-Baugruppen (PCBA 01 bis PCBA 05)** des OpenMotorBridge Gesamtsystems, einschließlich Lagenaufbau, Impedanzkontrolle, Net-Klassen, Funktionszonen und vollständigen Pinout-Tabellen.

---

## 1. Systemübersicht der 5 Platinen-Baugruppen

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   DIE 5 HARDWARE-BAUGRUPPEN (PCBAs) DER OPENMOTORBRIDGE                │
├───────┬───────────────────────────────┬───────────────┬─────────┬──────────────────────┤
│ Baugruppe │ Name & Funktion           │ Platinenmaße  │ Lagen   │ Kern-ICs / Controller│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 01**│ **Zentralbox Main Controller** │ 85 x 55 mm    │ 4 Lagen │ ESP32-S3, LM5164,    │
│       │ (Unter der Sitzbank, Audio/USV)│ (77x47 mm M3) │ (ENIG)  │ BQ24075, ES8388, IMU │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 02**│ **Satelliten Pod Base Carrier**│ 36 x 20 mm    │ 2 Lagen │ SP3012 TVS, M8 6-Pin,│
│       │ (Sockel für Pod 1 & 2)        │ (30 mm M2)    │         │ Kassetten-Aufnahme   │
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 03**│ **Universalschlitten Cartridge**│ 35 x 25 mm    │ 2 Lagen │ DS2401 1-Wire ID,    │
│       │ (Trägerplatine im 116x58 Sled)│ (29x19 mm M2) │         │ TLP222A PhotoMOS Opto│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 04**│ **Rear Pod 3 Transceiver Hub** │ 55 x 48 mm    │ 4 Lagen │ RP2040 Coprozessor,  │
│       │ (Heckbürzel: LoRa & GNSS)     │ (46x19 mm M2) │ (ENIG)  │ SX1262 LoRa, MAX-M10S│
├───────┼───────────────────────────────┼───────────────┼─────────┼──────────────────────┤
│ **PCBA 05**│ **Universal Front-Knoten**    │ 68 x 44 mm    │ 4 Lagen │ ESP32-C3 RISC-V,     │
│       │ (Smart Fairing Hub & Ottocast)│ (62x38 mm M2.5│ (ENIG)  │ USB2512B, TPS2051B   │
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

### 3.1 Technische Platinen-Kenndaten
* **Abmessungen:** $85{,}0 \times 55{,}0\,\text{mm}$ (Außenkontur mit 4x M2.5 Montagebohrungen, $77{,}0 \times 47{,}0\,\text{mm}$ Lochabstand).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Gesamtdicke, $35\,\mu\text{m}$ Cu auf allen 4 Lagen).
  * Layer 1 (Top): Bauelemente, HF-Leiterbahnen und differentielle Audiopaare.
  * Layer 2 (Inner 1): Durchgehende, ununterbrochene GND-Bezugsebene.
  * Layer 3 (Inner 2): Split Power Planes ($+3{,}3\,\text{V}$, $+5{,}0\,\text{V}$, `VBUS`, `VBAT_LIPO`) und Audio-GND.
  * Layer 4 (Bottom): Sekundäre Signale, Schirmflächen und thermische Vias.
* **Oberflächenveredelung:** ENIG (Electroless Nickel Immersion Gold, $0{,}05\dots 0{,}1\,\mu\text{m}$ Au über $3\dots 5\,\mu\text{m}$ Ni).
* **Isolationsbarriere:** $4{,}0\,\text{mm}$ galvanischer Kriech- und Luftabstand unter den Audio-Übertragern `T1` und `T2`.

### 3.2 Pinbelegung des zentralen 26-poligen Flansch-Steckverbinders (`J1` / HD26)

| Pin (HD26/J1) | Signalname | Signalart / Spannungsbereich | Funktion & Schutzbeschaltung |
| :--- | :--- | :--- | :--- |
| **Pin 1** | `POD1_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 300 mA) | Stromversorgung Lenker-Pod 1 (High-Side Switch, PPTC 500mA) |
| **Pin 2** | `POD1_NF_P` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T1` (Positiv) |
| **Pin 3** | `POD1_NF_N` | Audio Line-Out ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T1` (Negativ) |
| **Pin 4** | `POD1_OPTO_KEY` | Optokoppler PTT-Keying | PhotoMOS `U7` Open-Collector / Schließer (< 1 ms prellfrei) |
| **Pin 5** | `POD2_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 300 mA) | Stromversorgung Helm-Pod 2 (High-Side Switch, PPTC 500mA) |
| **Pin 6** | `POD2_NF_P` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T2` (Positiv) |
| **Pin 7** | `POD2_NF_N` | Audio Line-In ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Galvanisch getrennt via Trafo `T2` (Negativ) |
| **Pin 8** | `POD2_OPTO_KEY` | Optokoppler Mute/Keying | PhotoMOS `U8` Open-Collector / Schließer (< 1 ms prellfrei) |
| **Pin 9** | `POD3_VCC` | $+5{,}0\,\text{V}$ geschaltet (max. 500 mA) | Stromversorgung Heck-Transceiver Pod 3 |
| **Pin 10** | `POD3_UART_TX` | UART TX ($3{,}3\,\text{V}$, 460.800 Baud) | Datenleitung zu Pod 3 (GNSS/Telemetrie/LoRa) |
| **Pin 11** | `POD3_UART_RX` | UART RX ($3{,}3\,\text{V}$, 460.800 Baud) | Datenleitung von Pod 3 (GNSS/Telemetrie/LoRa) |
| **Pin 12** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Hauptmasse für Pod-Stromversorgungen |
| **Pin 13** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Paralleler Massepfad für minimalen Schleifenwiderstand |
| **Pin 14** | `KL30_IN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Dauerplus) | Batterie-Haupteingang (LM5164 Buck, SMBJ33CA TVS-Schutz) |
| **Pin 15** | `KL15_IGN` | $+9\,\text{V} \dots +72\,\text{V}$ DC (Zündungsplus) | Zündungssignal mit Spannungsteiler & Schmitt-Trigger |
| **Pin 16** | `GND_PWR` | Power-Masse ($0\,\text{V}$) | Fahrzeug-Bordnetz-Masse |
| **Pin 17** | `CAN_H` | CAN High (ISO 11898-2) | CAN-FD Busleitung High ($120\,\Omega$ Terminierung schaltbar) |
| **Pin 18** | `CAN_L` | CAN Low (ISO 11898-2) | CAN-FD Busleitung Low ($120\,\Omega$ Terminierung schaltbar) |
| **Pin 19** | `ONEWIRE_ID` | 1-Wire Datenbus ($3{,}3\,\text{V}$) | Automatische Pod- & Kassetten-Erkennung (DS2431 / DS2401) |
| **Pin 20** | `GND_SHIELD` | Gehäuse- & Schirmmasse | Direkte Verbindung zum Alugehäuse / Schirmgeflecht |
| **Pin 21** | `AGND` | Analoge Audiomasse | Ruhige Audiomasse für ES8388 Codec-Referenz |
| **Pin 22** | `RESERVE_GPIO_A`| GPIO Digital I/O ($3{,}3\,\text{V}$) | Frei programmierbarer GPIO / PWM-Ausgang (ESP32-S3) |
| **Pin 23** | `RESERVE_GPIO_B`| GPIO Digital I/O ($3{,}3\,\text{V}$) | Frei programmierbarer GPIO / ADC-Eingang (ESP32-S3) |
| **Pin 24** | `I2S_DOUT` | I2S Data Out ($3{,}3\,\text{V}$) | Digitaler Audio-Stream zu externem DSP/Verstärker |
| **Pin 25** | `I2S_BCLK` | I2S Bit Clock ($3{,}3\,\text{V}$) | Digitaler I2S Takt |
| **Pin 26** | `GND_SHIELD` | Gehäuse- & Schirmmasse | Zweiter Schirmkontakt für 360°-Rundumschirmung |

### 3.3 Interne Platinen-Steckverbinder & Service-Schnittstellen

| Stecker | Typ / Bauform | Polzahl | Funktion & Signalbelegung |
| :--- | :--- | :---: | :--- |
| **`J2`** | MicroSD Push-Push | 9-Pin | 4-Bit SDIO High-Speed Bus (`CLK`, `CMD`, `DAT0`-`DAT3`, `CD`, `3V3`, `GND`) für die gerichtsfeste Ringspeicher-Blackbox. |
| **`J3`** | IDC Wannenstecker ($2{,}54\,\text{mm}$) | 10-Pin | Service-, Programmier- und Debug-Header: Pin 1: `3V3`, Pin 2: `TXD0`, Pin 3: `RXD0`, Pin 4: `GND`, Pin 5: `USB_D-`, Pin 6: `USB_D+`, Pin 7: `EN`, Pin 8: `IO0`, Pin 9: `CAN_H`, Pin 10: `CAN_L`. |
| **`J_BAT`**| Molex Micro-Fit 3.0 | 2-Pin | USV-Pufferakku: Pin 1: `VBAT_LIPO` ($+3{,}7\dots 4{,}2\,\text{V}$), Pin 2: `GND` (überwacht via BQ24075 TS NTC). |
| **`J_AUD`**| JST-XH ($2{,}50\,\text{mm}$) | 4-Pin | Optionaler interner Audio-Messport: `LINE_L+`, `LINE_L-`, `LINE_R+`, `LINE_R-`. |

---

## 4. PCBA 02: Satelliten Pod Base Carrier (`openmotorbridge_pod_base`)

![PCBA 02 Satelliten Pod Base Carrier](../images/pcba/pcba02_pod_base_3d.png)

*Abbildung 7.2: KiCad 3D-Render der Pod-Basisplatine (PCBA 02, 36 x 20 mm, 2 Lagen) mit 6-poliger Präzisions-Stiftleiste, M8 6-Pin IP67 Buchsenanschluss und SP3012 TVS-Schutzarray.*

### 4.1 Technische Platinen-Kenndaten
* **Abmessungen:** $36{,}0 \times 20{,}0\,\text{mm}$ (Rechteckkontur mit 2x M2 Befestigungsbohrungen im Abstand $30{,}0\,\text{mm}$, passgenau für die Schottkammer des Pod-Gehäuses).
* **Lagenaufbau:** 2 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Dicke, $35\,\mu\text{m}$ Kupfer beidseitig).
  * Layer 1 (Top): Präzisionskontaktleiste `J1`, TVS-Array `U1` und SMD-Entkoppelkondensatoren.
  * Layer 2 (Bottom): Vollflächige Masseebene (`GND`) zur HF- und Störunterdrückung.
* **Oberflächenveredelung:** ENIG (Goldauflage $0{,}05\,\mu\text{m}$ für langlebige Korrosionsbeständigkeit).

### 4.2 Pinbelegung der M8 6-Pin Rundbuchse (`J2` / Kabelbaum-Eingang)

Die M8-Rundbuchse (A-kodiert, IP67) stellt die wasserdichte Verbindung zum Hauptkabelbaum her:

| Pin (M8/J2) | Signalname | Signalart / Spannungsbereich | Funktion & ESD-Schutz |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `1_VCC` | $+5{,}0\,\text{V}$ DC (max. 300 mA) | Speisespannung von Zentralbox (abgesichert über 500mA PPTC, TVS Ch 1) |
| **Pin 2** | `2_GND` | Power-Masse ($0\,\text{V}$) | Zentraler Massepfad für Rückströme und HF-Referenz |
| **Pin 3** | `3_SIG_P` | Audio Line Positiv ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Differenzieller NF-Audiopfad Positiv (TVS Ch 2, $< 0{,}5\,\text{pF}$) |
| **Pin 4** | `4_SIG_N` | Audio Line Negativ ($1{,}0\,\text{V}_{\text{RMS}}$ diff.) | Differenzieller NF-Audiopfad Negativ (TVS Ch 3, $< 0{,}5\,\text{pF}$) |
| **Pin 5** | `5_TRIGGER_PPS`| Trigger / Timecode ($3{,}3\,\text{V}$ Logic) | Optokoppler-PTT-Tastung oder 1-PPS Timepulse (TVS Ch 4) |
| **Pin 6** | `6_1WIRE_ID` | 1-Wire Datenbus ($3{,}3\,\text{V}$) | Datenleitung zur automatischen Kassetten-Erkennung (TVS Ch 5) |
| **Kragen** | `SHIELD` | Schirm- und Gehäusemasse | $360^\circ$-Rundumkontakt zum M8 Metallgewinde und Rohrbett |

### 4.3 Pinbelegung der 6-poligen Präzisions-Stiftleiste (`J1` / Kassetten-Übergabe)

Vertikale, hochpräzise SMD-Stiftleiste ($2{,}54\,\text{mm}$ Raster, vergoldet, mechanischer Wipe-Weg $4{,}8\,\text{mm}$):

| Pin (J1) | Signalname | Richtung | Beschreibung |
| :---: | :--- | :---: | :--- |
| **Pin 1** | `1_VCC` | Ausgang $\rightarrow$ Kassette | $+5{,}0\,\text{V}$ DC Speisung für Headset-Ladeschaltung und Elektronik |
| **Pin 2** | `2_GND` | Bidirektional | Massebezug für Signal und Versorgung |
| **Pin 3** | `3_SIG_P` | Bidirektional | Differenzielles NF-Audiosignal Positiv |
| **Pin 4** | `4_SIG_N` | Bidirektional | Differenzielles NF-Audiosignal Negativ |
| **Pin 5** | `5_TRIGGER_PPS`| Bidirektional | Prellfreie PTT-Schaltleitung zum Headset-Taster |
| **Pin 6** | `6_1WIRE_ID` | Bidirektional | 1-Wire ROM-ID Abfrageleitung zum DS2401-Chip der Kassette |

* **ESD-Schutzarray:** Littelfuse `SP3012-06UTG` schützt alle 5 Signalleitungen gegen elektrostatische Entladungen nach IEC 61000-4-2 ($\pm 15\,\text{kV}$ Luftentladung, $\pm 8\,\text{kV}$ Kontaktentladung) bei vernachlässigbarer Kapazität von nur $0{,}5\,\text{pF}$.

---

## 5. PCBA 03: Universalschlitten Cartridge (`openmotorbridge_pod_cartridge`)

![PCBA 03 Universalschlitten Cartridge](../images/pcba/pcba03_pod_cartridge_3d.png)

*Abbildung 7.3: KiCad 3D-Render des Universalschlitten-Kassettenträgers (PCBA 03, 35 x 25 mm, 2 Lagen) mit DS2401 1-Wire ID-Chip, horizontaler Mating-Buchse und Headset-JST-SH Schnittstelle.*

### 5.1 Technische Platinen-Kenndaten
* **Abmessungen:** $35{,}0 \times 25{,}0\,\text{mm}$ (kompakte Trägerplatine mit 4x M2 Befestigungsbohrungen im Raster $29{,}0 \times 19{,}0\,\text{mm}$, formschlüssig integriert in den $116 \times 58\,\text{mm}$ Wechselschlitten mit $105 \times 48\,\text{mm}$ Adapter-Konturbett).
* **Lagenaufbau:** 2 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Dicke, $35\,\mu\text{m}$ Kupfer).
* **Ausstattung:** DS2401 1-Wire Chip (`U1`), Toshiba TLP222A PhotoMOS Relais (`U2`), PPTC 500mA Sicherung (`F1`), Grüne Status-LED (`D1`).

### 5.2 Pinbelegung der horizontalen Docking-Buchse (`J1` / Verbindung zur Pod-Base)

| Pin (J1) | Signalname | Signalart | Funktion & Schutz |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `1_VCC` | $+5{,}0\,\text{V}$ Eingang | Versorgungsspannung über rückstellbare PPTC-Sicherung `F1` (500mA) |
| **Pin 2** | `2_GND` | Power-Masse | Masseverbindung zum Pod-Sockel |
| **Pin 3** | `3_NF_P` | Audio Line In/Out | Differenzielles Audio Positiv zum Übertrager |
| **Pin 4** | `4_NF_N` | Audio Line In/Out | Differenzielles Audio Negativ zum Übertrager |
| **Pin 5** | `5_OPTO` | PTT-Tastsignal | Steuert das Toshiba TLP222A PhotoMOS Relais an |
| **Pin 6** | `6_1WIRE` | 1-Wire Datenbus | Liest die weltweit eindeutige UID aus Chip `U1` (DS2401) aus |

### 5.3 Pinbelegung des internen 6-poligen JST-SH Headers (`J2` / Headset-Cradle Anbindung)

Der $1{,}0\,\text{mm}$ JST-SH Winkelstecker verbindet die Kassettenplatine mit dem modellspezifischen Pogo-Pin-Feld:

| Pin (J2) | Signalname | Richtung | Belegung nach OEM-Headset-Klasse |
| :---: | :--- | :---: | :--- |
| **Pin 1** | `VCC_5V` | Ausgang $\rightarrow$ Cradle | 5V Ladespeisung (Sena 50S Pogo 2, Cardo Edge Pad 2, USB 5V) |
| **Pin 2** | `GND` | Masse | Systemmasse (Sena 50S Pogo 1, Cardo Edge Pad 1, USB GND) |
| **Pin 3** | `AUDIO_R+` | Ausgang $\rightarrow$ Headset | Lautsprecher/Line-In Signal Positiv (Sena Pogo 4, Cardo Pad 3) |
| **Pin 4** | `AUDIO_R-` | Ausgang $\rightarrow$ Headset | Lautsprecher/Line-In Signal Negativ (Sena Pogo 5, Cardo Pad 4) |
| **Pin 5** | `MIC_IN+` | Eingang $\leftarrow$ Headset | Headset-Mikrofonsignal zum Codec (Sena Pogo 6, Cardo Pad 5) |
| **Pin 6** | `OPTO_PTT` | Schaltausgang | TLP222A Schließerkontakt gegen Masse (Sena Mesh-Taste Pogo 7) |

### 5.4 On-Board Elektronik & Hardware-ID
* **1-Wire ROM-ID Chip (`U1`):** Maxim/Analog Devices `DS2401Z+` im SOT-23 Gehäuse. Sendet eine 64-Bit-UID (`Family-Code 0x01 + 48-Bit Seriennummer + 8-Bit CRC`) zur lückenlosen Profil-Identifikation in LittleFS.
* **PhotoMOS Halbleiterrelais (`U2`):** Toshiba `TLP222A` (Schaltzeit $t_{\text{ON}} < 0{,}5\,\text{ms}$, galvanische Trennung $1500\,\text{V}_{\text{RMS}}$, prellfreies Tasten ohne Kontaktfunken).
* **Selbstrückstellende Sicherung (`F1`):** Bourns `MF-MSMF050-2` (1812 SMD, $I_{\text{hold}} = 500\,\text{mA}$, $I_{\text{trip}} = 1{,}0\,\text{A}$).

---

## 6. PCBA 04: Rear Pod 3 Transceiver & Coprozessor (`openmotorbridge_rear_pod3`)

![PCBA 04 Rear Pod 3 Transceiver Hub](../images/pcba/pcba04_rear_pod3_3d.png)

*Abbildung 7.4: KiCad 3D-Render der Heck-Pod 3 Transceiverplatine (PCBA 04, 55 x 48 mm, 4 Lagen) mit RP2040 Coprozessor, Semtech SX1262 LoRa, u-blox Multi-GNSS und U.FL/Murata MM8030 HF-Umschaltports.*

### 6.1 Technische Platinen-Kenndaten
* **Abmessungen:** $55{,}0 \times 48{,}0\,\text{mm}$ (4 Lagen FR-4 High-TG150, 4x M2 Montagebohrungen im Raster $46{,}0 \times 19{,}0\,\text{mm}$, formbündig im aerodynamischen Heck-Pod 3 Gehäuse montiert).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$, $35\,\mu\text{m}$ Cu) mit kontrollierter $50\,\Omega$ Impedanz für alle HF-Pfade.
  * Layer 1 (Top): HF-Transceiver, GNSS-Modul, Murata MM8030 Buchsen, koplanare $50\,\Omega$ Wellenleiter.
  * Layer 2 (Inner 1): Durchgehende, unsegmentierte HF-Massebezugsebene.
  * Layer 3 (Inner 2): Split Power ($+3{,}3\,\text{V}_{\text{RF}}$, $+3{,}3\,\text{V}_{\text{DIG}}$, $+5{,}0\,\text{V}$).
  * Layer 4 (Bottom): RP2040 Coprozessor, Flash-Speicher, Entkopplung und sekundäres Signalrouting.

### 6.2 Pinbelegung der 6-poligen Schnittstelle zur Zentralbox (`J1`)

| Pin (J1) | Signalname | Signalart / Pegel | Funktion & Beschreibung |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `1_VCC_5V` | $+5{,}0\,\text{V}$ DC geschaltet (max. 500 mA) | Hauptversorgung von der Zentralbox |
| **Pin 2** | `2_GND` | Power- & HF-Masse ($0\,\text{V}$) | Massebezug für Logik und Hochfrequenz |
| **Pin 3** | `3_UART_TX` | UART TX ($3{,}3\,\text{V}$, 460.800 Baud) | High-Speed Telemetrie- und NMEA-Daten zur Zentralbox |
| **Pin 4** | `4_UART_RX` | UART RX ($3{,}3\,\text{V}$, 460.800 Baud) | Steuerbefehle und LoRa-Payloads von der Zentralbox |
| **Pin 5** | `5_1PPS` | Digitaler Impuls ($3{,}3\,\text{V}$, active-high) | Sub-Mikrosekunden Zeitcode-Impuls vom NEO-M9N GNSS |
| **Pin 6** | `6_1WIRE_ID` | 1-Wire Datenbus ($3{,}3\,\text{V}$) | Kassetten- und Pod-Erkennung via DS2401 |

### 6.3 HF-Koaxialports mit Murata MM8030 Umschaltbuchsen

Die Platine verfügt über 3 automatische Koaxial-Umschaltbuchsen (`Murata MM8030-2610`), die beim Einstecken eines Steckers verlustarm auf externe Antennen umschalten ($< 0{,}15\,\text{dB}$ Einfügedämpfung, $> 25\,\text{dB}$ Isolation bis 6 GHz):

| HF-Port | Frequenzband | Interne Standardantenne | Externer Bypass-Pfad (MM8030) |
| :---: | :--- | :--- | :--- |
| **`J3`** | $2{,}4\,\text{GHz}$ ISM | Interne Inverted-F PCB-Antenne (IFA, $0\,\text{dBi}$) | Externe $+5\,\text{dBi}$ Stab- oder Haifischflossenantenne |
| **`J4`** | $868\,\text{MHz}$ LoRa | Interne Wendelspulenantenne ($+1{,}5\,\text{dBi}$) | Externe $\lambda/4$-Monopolantenne für extreme Reichweiten |
| **`J5`** | $1{,}575\,\text{GHz}$ GNSS | Interne $25 \times 25\,\text{mm}$ Keramik-Patchantenne | Externe Aktiv-Patchantenne mit $+3{,}3\,\text{V}$ Phantomspeisung |

### 6.4 RP2040 Dual-Cortex-M0+ Pinbelegung & Funktions-Mapping

| RP2040 Pin | Netzknoten | Funktion & Peripherie |
| :--- | :--- | :--- |
| **GPIO 0 / 1** | `UART0_TX` / `RX` | High-Speed UART-Verbindung zur Zentralbox (460.800 Baud, DMA-gepuffert) |
| **GPIO 4 / 5** | `UART1_TX` / `RX` | High-Speed UBX/NMEA Datenverbindung zum u-blox NEO-M9N GNSS-Modul |
| **GPIO 6** | `TIMEPULSE_1PPS` | Hardware-Capture Timer-Eingang für framegenaue Actioncam-Synchronisation |
| **GPIO 8** | `SPI0_SCK` | SPI Serial Clock zum Semtech SX1262 LoRa-Transceiver |
| **GPIO 9** | `SPI0_MISO` | SPI Master-In Slave-Out vom SX1262 |
| **GPIO 10** | `SPI0_MOSI` | SPI Master-Out Slave-In zum SX1262 |
| **GPIO 11** | `SPI0_NSS` | SPI Chip Select (Active-Low) zum SX1262 |
| **GPIO 2** | `LORA_BUSY` | SX1262 State-Flag (Hardware-Wartebedingung für SPI-Befehle) |
| **GPIO 3** | `LORA_DIO1` | SX1262 IRQ (Packet Received / Packet Sent Interrupt) |
| **GPIO 16** | `WS2812B_LED` | Digitaler Datenausgang für die mehrfarbige Gehäuse-Status-LED |

---

## 7. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`)

![PCBA 05 Universal Front-Knoten](../images/pcba/pcba05_front_node_3d.png)

*Abbildung 7.5: KiCad 3D-Render des Universal Front-Knotens (PCBA 05, 68 x 44 mm, 4 Lagen) mit ESP32-C3 RISC-V, Microchip USB2512B High-Speed Hub, TI TPS2051B Power-Gate und Knowles I2S MEMS Mikrofon.*

### 7.1 Technische Platinen-Kenndaten
* **Abmessungen:** $68{,}0 \times 44{,}0\,\text{mm}$ (Gehäuseinnenmaß $84 \times 60 \times 23\,\text{mm}$ mit 4-in-1 Befestigung).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$, $35\,\mu\text{m}$ Kupfer).
  * Layer 1 (Top): ESP32-C3 Controller, USB2512B Hub, Knowles MEMS, $90\,\Omega$ USB-Differenzpaare.
  * Layer 2 (Inner 1): Durchgehende, niederohmige GND-Masseebene.
  * Layer 3 (Inner 2): Split Power ($+5{,}0\,\text{V}_{\text{MAIN}}$, $+5{,}0\,\text{V}_{\text{OTTOCAST}}$, $+3{,}3\,\text{V}$).
  * Layer 4 (Bottom): LMR36015 Buck-Wandler, TPS2051B Lastschalter, TVS-Dioden und Filter.

### 7.2 Fahrzeug- & Peripherie-Schnittstellen (JST-PH Header)

| Stecker | Steckertyp | Polzahl | Signalbelegung & Funktion |
| :--- | :--- | :---: | :--- |
| **`J1`** | JST-PH / 2-Pin Schraubklemme | 2-Pin | **12V Bordnetz-Eingang:** Pin 1: `KL15_12V_SW` ($+9\dots 36\,\text{V}$ DC Zündungsplus), Pin 2: `GND` (Fahrzeugmasse). Gespeist über LMR36015 Buck-Regler. |
| **`J2`** | JST-PH ($2{,}00\,\text{mm}$) | 3-Pin | **Cockpit CAN-Bus:** Pin 1: `CAN_H`, Pin 2: `CAN_L`, Pin 3: `GND` (ISO 11898-2 mit $120\,\Omega$ Abschlusswiderstand für Cockpit-Instrumente). |
| **`J3`** | JST-PH ($2{,}00\,\text{mm}$) | 2-Pin | **Lenker-PTT Schnittstelle:** Pin 1: `PTT_INPUT_N` (Active-Low Interrupt auf ESP32-C3 GPIO 0, interner Pull-up, 100nF RC-Tiefpass), Pin 2: `GND`. 100% batteriefreier Anschluss. |

### 7.3 Automotive USB 2.0 High-Speed Subsystem (`Microchip USB2512B`)

| Port | Steckertyp | Funktion & Leistungsdaten |
| :--- | :--- | :--- |
| **`J4`** | JST-PH (4-Pin) | **Upstream Host Port:** Führt `USB_UP_VBUS` ($+5{,}0\,\text{V}$), `USB_UP_DM`, `USB_UP_DP`, `GND` zur Verbindung mit dem Hauptsystem. |
| **`J5`** | JST-PH (4-Pin) | **Downstream Port 1 (Handschuhfach / Phone):** Dauerhafter $+5{,}0\,\text{V}$ VBUS (bis $2{,}0\,\text{A}$) für unterbrechungsfreies Laden von Smartphones oder Navi-Geräten. |
| **`J6`** | JST-PH (4-Pin) | **Downstream Port 2 (Ottocast CarPlay / Android Auto):** Geschalteter $+5{,}0\,\text{V}$ VBUS über `TI TPS2051B` Lastschalter mit **1-Klick Kaltstart-Funktion** (2,5s Reset) und **Auto-Café 60s Timer**. |
| **`J7`** | USB-C 16-Pin Receptacle | **Service- & Flash-Port:** Nativer ESP32-C3 USB-JTAG / CDC-Serial Port für Firmware-Updates, Kalibrierung und Echtzeit-Akkustikanalyse. |

### 7.4 ESP32-C3 RISC-V Controller Pinbelegung & Funktions-Mapping

| ESP32-C3 Pin | Signalname | Richtung | Funktion & Peripherie |
| :--- | :--- | :---: | :--- |
| **GPIO 0** | `PTT_INPUT_N` | Eingang | Mechanischer Lenkertaster Interrupt (Active-Low, $12\,\mu\text{s}$ Schmitt-Trigger-Latenz) |
| **GPIO 1** | `OTTOCAST_PWR_EN` | Ausgang | Enable-Steuersignal für den TPS2051B VBUS-Lastschalter (High = Aktiv) |
| **GPIO 3** | `OTTOCAST_FAULT_N`| Eingang | Überstrom- & Thermoflag vom TPS2051B (Active-Low Interrupt) |
| **GPIO 4** | `KL15_SENSE` | Eingang | Bordnetz-Zündungsüberwachung über 10:1 Spannungsteiler & Schmitt-Trigger |
| **GPIO 6** | `MIC_I2S_WS` | Ausgang | I2S Word Select (LRCLK, 48 kHz) für Knowles SPH0645LM4H Digitalmikrofon |
| **GPIO 7** | `MIC_I2S_BCLK` | Ausgang | I2S Bit Clock ($3{,}072\,\text{MHz}$) für Knowles SPH0645LM4H Digitalmikrofon |
| **GPIO 8** | `MIC_I2S_DATA` | Eingang | I2S Serial Audio Data vom Knowles MEMS Mikrofon (Fahrtwind-Erfassung) |
| **GPIO 20** | `TWAI_RX` | Eingang | CAN-Bus Empfangsleitung vom TI SN65HVD230 Transceiver |
| **GPIO 21** | `TWAI_TX` | Ausgang | CAN-Bus Sendeleitung zum TI SN65HVD230 Transceiver |
