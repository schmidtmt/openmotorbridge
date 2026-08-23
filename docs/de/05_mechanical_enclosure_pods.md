# 05 - Mechanische Konstruktion: Zentralbox, Dichtungskonzept & Universal-Kassetten-Pods

## 1. Gehaeuse Typ A: Zentrale Steuerbox (Unter Sitzbank)
- **Aussenabmessungen:** 95.0 x 65.0 x 24.0 mm (ohne Befestigungslaschen).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck, kugelgestrahlt, im Heissbad schwarz chemisch geglaettet und hydrophob versiegelt.
- **Schutzart:** IP67.

### 1.1 Sandwich-Aufbau & Platinenbefestigung
1. **Bodenwanne:** Vertiefte Akkutasche (52.0 x 36.0 x 6.5 mm) fuer den 1000 mAh LiPo-Akku mit NTC-Temperatursensor, gedaempft durch 2.0 mm EPDM-Moosgummi. Vier Ruthex M3 x 5.7 mm Messing-Gewindeeinsaetze.
2. **Elektronik-Ebene:** 4-Lagen-Platine (85.0 x 55.0 mm) auf vier 4.0-mm-Domen mit M3 x 6 mm Torx-Schrauben (ISO 14581, Edelstahl A2, Loctite 243) fixiert.
3. **Gehaeusedeckel:** Verschraubt ueber sechs M3 x 12 mm Zylinderschrauben (ISO 4762) mit 0.8 Nm Anzugsmoment.

### 1.2 Dichtungskonzept & Druckausgleich
- **Umlaufende Nut-Feder-Dichtung:** Silikon-Rundschnur (Shore 45-50 A, D = 1.8 mm), definiert um 30 % auf 1.25 mm vorkomprimiert.
- **Druckausgleich:** Gore Automotive Vent AVS 41 mit ePTFE-Membran (M8 x 1.25).
- **HD26-Wandbuchse:** IP67 Flansch mit EPDM-Flachdichtung, intern ueber 26-poliges Flachbandkabel auf 2x13 Wannenstecker entkoppelt.

## 2. Gehaeuse Typ B: Universeller Satelliten-Pod (Identisch fuer Pod 1, 2 und 3)
- **Abmessungen Schacht:** 64.0 x 46.0 x 23.5 mm.
- **Elektronik-Kassette:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).
- **Kontaktblock:** 6-poliges Mill-Max Pogo-Pin-Array (Serie 824-22-006-00-001101, Raster 2.54 mm, 1.4 mm Arbeitshub) mit Silikon-Formschuhdichtung gegen vergoldete ENIG-Pads.
- **3-Stufen-Sicherheitsarretierung:**
  1. *Snap-Lock:* POM-C Federklinken mit akustischem Klick.
  2. *Cam-Lock:* Stirnseitiger 90-Grad-Edelstahl-Drehriegel blockiert Klinken formschluessig gegen Stoesse > 20 g.
  3. *Push-to-Eject:* Gummierte Hebelwippe wirft Kassette nach Entriegelung um 8.0 mm aus.
- **Befestigung:** M5-Rueckenplatte fuer Flachmontage oder CNC-Rohrschellen (22.0 mm, 28.6 mm, 1 Zoll).

## 3. Belegung der 6-Pin Pogo-Kontaktleiste

| Pogo-Pin | Pod 1 & 2 (Links / Rechts: Audio & Intercom) | Pod 3 (Heck: GNSS & OpenMotorMesh LoRa) |
| :---: | :--- | :--- |
| **Pin 1** | **`VCC`** (5V geschaltete Speisespannung via MOSFET) | **`VCC`** (5V Dauer-Versorgung) |
| **Pin 2** | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) |
| **Pin 3** | **`NF_P`** (Symmetrisches Audiosignal + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Zentralbox) |
| **Pin 4** | **`NF_N`** (Symmetrisches Audiosignal - via Bourns) | **`UART_RX`** (Zentralbox $\rightarrow$ Heck-Co-Prozessor) |
| **Pin 5** | **`OPTO`** (TLP222A Tastensimulations-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal Sync) |
| **Pin 6** | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Heck-Kassetten-Erkennung) |

## 4. Kabelbaum-Spezifikation (Zentralbox zu Pods)
- **Kabeltyp:** Hochflexibles, oel- und UV-bestaendiges PUR-Kabel mit Geflechtschirm aus verzinntem Kupfer.
- **Adernaufbau:** $2 \times 0.25\,\text{mm}^2$ (VCC / GND fuer bis zu 1 A Ladestrom) + $4 \times 0.14\,\text{mm}^2$ verdrillte Paare (Audio/UART, Opto/PPS, 1-Wire ID).
- **Schirmanschluss:** Der Gesamtschirm ist einseitig an der Zentralbox auf `GND_SHIELD` (Pin 22) niederinduktiv aufgelegt.
