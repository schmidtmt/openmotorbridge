# 02 - PCB Hardware, Layout & Pinout-Spezifikation

Dieses Dokument spezifiziert das 4-Lagen-Platinenlayout der zentralen Steuerbox (`openmotorbridge_main_box`), die EMV-Zonierung, den barrierefreien Steckkorridor, die Schwingungsentkopplung sowie die vollständigen Pin- und GPIO-Belegungen.

---

## 1. 3D-Board-Visualisierung & Photorealistisches Render

Die Hauptplatine vereint auf kompakten **$85{,}0 \times 55{,}0\,\text{mm}$** die komplette Automotive-Stromversorgung, die unterbrechungsfreie LiPo-USV, den digitalen DSP-Host-Core sowie das galvanisch getrennte Audio-Frontend:

![OpenMotorBridge Main Box 3D PCB Render](../../hardware/kicad_main_box/kicad_3d_render.png)

*Abbildung 2.1: Photorealistisches 3D-Raytracing-Render der OpenMotorBridge Zentralbox-Platine (KiCad 9.0, 4-Lagen FR4 TG150 ENIG, 874 Leiterbahnen, 114 Vias, 0 DRC-Fehler).*

---

## 2. Platinenabmessungen, Lagenaufbau & Fertigungsspezifikation

| Parameter | Spezifikation | Norm / Fertigungsstandard |
| :--- | :--- | :--- |
| **Abmessungen** | $85{,}0\,\text{mm} \times 55{,}0\,\text{mm} \times 1{,}6\,\text{mm}$ | DIN ISO 2768-m (Toleranz $\pm 0{,}1\,\text{mm}$) |
| **Lagenanzahl** | **4 Kupferlagen** | Symmetrischer Lagenaufbau |
| **Basismaterial** | FR4 High-TG ($T_g \ge 150\,^\circ\text{C}$) | Automotive-Grade Temperaturbeständigkeit |
| **Oberflächenfinish** | **ENIG (Electroless Nickel Immersion Gold)** | Korrosionsbeständig, planare SMD-Pads |
| **Kupferstärke** | $35\,\mu\text{m}$ (1.0 oz) Außen / $35\,\mu\text{m}$ Innen | Hohe Stromtragfähigkeit für Buck & Power-Path |
| **Lötstoppmaske** | Mattschwarz (Matte Black) | Reflexionsarm, UV-beständig |
| **Bestückungsdruck** | Weiß (Crisp White High-Res) | Eindeutige Bauteil- & Steckerbeschriftung |
| **Min. Leiterbahn / Abstand** | $0{,}127\,\text{mm}$ (5 mil) / $0{,}127\,\text{mm}$ (5 mil) | JLCPCB Standard / Prototypen-kompatibel |
| **Min. Bohrung (Via)** | $0{,}30\,\text{mm}$ Bohrung / $0{,}60\,\text{mm}$ Pad | Tenting auf allen Durchkontaktierungen |

### 2.1 4-Lagen Stackup-Architektur
```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1 (F.Cu - Top): High-Speed Signale, I2S, Bauteile    │  (35 µm Cu)
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

---

## 3. Zonierungs-Architektur (Zero-Cross-Talk & Zero-Collision Topologie)

![OpenMotorBridge Zentralplatine Top-Down Bestückungsplan](../../hardware/cad/main_board_pcb_top_down.png)

*Abbildung 2.2: Kollisionsfreier 2D-Top-Down-Bestückungsplan der Zentralplatine ($85 \times 55\,\text{mm}$). Farbcodierte Zonen mit $100\,\%$ Überschneidungsfreiheit (geprüfte Bounding-Boxes).*

Um gegenseitige Störungen zwischen der Schaltnetzteil-HF ($2{,}1\,\text{MHz}$), dem 2,4-GHz-Bluetooth-Funk und den hochempfindlichen analogen Audioleitungen vollständig zu eliminieren, ist die Platine in **5 strikt voneinander getrennte Funktionszonen** unterteilt:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ZONE 1: RF & ESP32-S3 CORE                      │
│                • ESP32-S3-WROOM-1 (Oben mittig, Y in [73, 86])         │
│                • Freie 2.4 GHz PCB-Antennenzone (>21mm zu H1/H2)       │
├─────────────────────────┬──────────────────┬───────────────────────────┤
│ ZONE 2: 72V BUCK POWER  │ ZONE 5: SENSORIK │ ZONE 3: GALV. AUDIO & CAN │
│ • LM5164 Buck (U1)      │ • MicroSD (J2)   │ • Bourns Trafo 1 (T1)     │
│ • 47µH Induktor (L1)    │ • ES8388 (U3)    │ • Bourns Trafo 2 (T2)     │
│ • SMBJ33CA TVS (D2 B.Cu)│ • BMI270 (U5)    │ • 2x TLP222A Opto (U7/U8) │
│ • TPS7A0533 LDO (U9)    │ (Unterseite B.Cu)│ • TCAN334G CAN (U6)       │
├─────────────────────────┴──────────────────┴───────────────────────────┤
│ ZONE 4: UNTERE FLANSCH-STECKVERBINDER (Zwischen Bohrungen H3 & H4)     │
│ [J3: 10-Pin USB/UART IDC-10]            [J1: 26-Pin System-Bus IDC-26] │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Zone 1 (Obere Kante Mitte – RF & Digital Core):**
   * Beherbergt das **ESP32-S3-WROOM-1** Modul (240 MHz Dual-Core) bei $X = 149{,}50\,\text{mm}, Y = 86{,}00\,\text{mm}$.
   * Die PCB-Mäanderantenne zeigt **vertikal nach oben** ($Y \in [73{,}25, 79{,}75\,\text{mm}]$) mit großzügigem Freiraum:
     * $> 21{,}2\,\text{mm}$ Abstand zur Montagebohrung `H1` (oben links)
     * $> 37{,}0\,\text{mm}$ Abstand zur Montagebohrung `H2` (oben rechts)
   * Der gesamte obere Platinenstreifen ($Y \le 84{,}0\,\text{mm}$) ist auf allen Lagen frei von Kupferflächen, Leitungen und hohen Bauteilen.

2. **Zone 2 (Linke Flanke – Automotive Power & USV):**
   * Enthält den TI LM5164-Q1 Step-Down-Schaltregler `U1` ($X = 124{,}00, Y = 88{,}00$), den Sunlord $47\,\mu\text{H}$ Induktor `L1` ($X = 124{,}00, Y = 103{,}00$) und den ultra-low-noise 3.3V LDO `U9` ($X = 134{,}00, Y = 84{,}00$).
   * Direkt auf der Unterseite (`B.Cu`) unter dem Spannungseingang sitzen die SMBJ33CA TVS-Diode `D2` ($X = 123{,}00, Y = 84{,}00$) und der $10\,\mu\text{F}$ 100V Keramikkondensator `C1` ($X = 130{,}00, Y = 84{,}00$) für minimale Leitungsinduktivität.

3. **Zone 3 (Rechte Flanke – Galvanische Trennung, Audio & CAN):**
   * **Galvanische Trennbarriere ($4{,}0\,\text{mm}$ Kriechstrecke):** Vertikaler Isolationsgraben bei $X = 162\,\text{mm}$ trennt Primär- und Sekundärseite.
   * **Audio-Trennübertrager:** 2x Bourns LM-NP-1001 `T1` ($X = 174{,}00, Y = 90{,}00$) und `T2` ($X = 174{,}00, Y = 107{,}00$) mit $17\,\text{mm}$ Rasterabstand für getrennte Bestückungs-Courtyards.
   * **Optokoppler:** 2x Toshiba TLP222A PhotoMOS `U7` ($X = 186{,}00, Y = 90{,}00$) und `U8` ($X = 186{,}00, Y = 107{,}00$).
   * **CAN-FD:** TI TCAN334G Transceiver `U6` ($X = 185{,}00, Y = 78{,}00$) mit 120-Ohm Abschlusswiderstand `R9`.
   * **Zusatzstecker:** `J5` (4-Pin JST-PH Akku+NTC, $X = 195{,}00, Y = 92{,}00$) und `J4` (3-Pin JST-PH RGB-LED, $X = 195{,}00, Y = 108{,}00$).

4. **Zone 4 (Untere Flansch-Kante – Haupt-Steckverbinder):**
   * **`J3` (10-Pin USB & UART Service-IDC-10):** Positioniert bei $X = 128{,}00\,\text{mm}, Y = 121{,}50\,\text{mm}$ (Höhe bündig mit Montagebohrungen $H3/H4$).
   * **`J1` (26-Pin Automotive System-Bus IDC-26):** Positioniert bei $X = 157{,}00\,\text{mm}, Y = 121{,}50\,\text{mm}$.
   * **Ergonomie:** Beide Stecker sitzen nebeneinander mit $1{,}0\,\text{mm}$ Spalt an der Unterkante und führen über das Flachbandkabel direkt zum wasserdichten HD26-Gehäuseflansch.

5. **Zone 5 (Unterseite `B.Cu` / Zentrum – Sensorik & Audio-DSP):**
   * **MicroSD-Kartenslot `J2`:** Zentral bei $X = 158{,}00\,\text{mm}, Y = 98{,}00\,\text{mm}$.
   * **Everest ES8388 Audio-Codec `U3`:** Bei $X = 158{,}00\,\text{mm}, Y = 84{,}00\,\text{mm}$ auf `B.Cu` für ultrakurze Leitungswege zu ESP32 und Transformatoren.
   * **Bosch BMI270 6-Achsen-IMU `U5`:** Bei $X = 149{,}50\,\text{mm}, Y = 108{,}00\,\text{mm}$ im Schwerpunkt der Platine.

---

## 4. Pinbelegung des zentralen HD26/IDC-26 Steckverbinders (`J1`)

![OpenMotorBridge Zentraler Automotive-Kabelbaum](../../hardware/cad/wiring_harness_cad.png)

*Abbildung 2.3: Automotive-Kabelbaum der 26-poligen Flansch-Schnittstelle.*

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
| **Pin 26** | `GND_SHIELD` | Gehäuse- & Schirmmasse | Zweiter Schirmkontakt für vollumfängliche 360°-Schirmung |

---

## 5. Pinbelegung des Service-IDC-10 Steckverbinders (`J3`)

| Pin (`J3`) | Signalname | Beschreibung |
| :--- | :--- | :--- |
| **Pin 1** | `VCC_5V_USB` | +5V USB-VBUS Versorgung / Ladeeingang |
| **Pin 2** | `USB_D_N` | USB 2.0 Full-Speed Datenleitung Negativ (ESP32-S3 USB-OTG) |
| **Pin 3** | `USB_D_P` | USB 2.0 Full-Speed Datenleitung Positiv (ESP32-S3 USB-OTG) |
| **Pin 4** | `GND_PWR` | USB-Masse |
| **Pin 5** | `UART_TXD0` | ESP32 Hardware UART0 TX (Debug & Flash-Konsole) |
| **Pin 6** | `UART_RXD0` | ESP32 Hardware UART0 RX (Debug & Flash-Konsole) |
| **Pin 7** | `ESP_EN` | Reset / Enable Steuersignal |
| **Pin 8** | `ESP_BOOT` | Boot-Modus Wahlsignal (GPIO0) |
| **Pin 9** | `GND_PWR` | Debug-Masse |
| **Pin 10** | `GND_SHIELD` | USB-Kabel-Schirmung |
