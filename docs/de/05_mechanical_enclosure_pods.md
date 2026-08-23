# 05 - Mechanische Konstruktion: Zentralbox, Dichtungskonzept & Universal-Kassetten-Pods

Dieses Dokument spezifiziert das IP67-Gehaeusedesign der zentralen Steuerbox (Typ A) sowie das hersteller- und fahrzeugunabhaengige, universelle Satelliten-Pod-System (Typ B) mit modularen Kassetten-Einschueben und Pogo-Pin-Schnittstelle.

---

## 1. Gehaeuse Typ A: Zentrale Steuerbox (Unter Sitzbank)
- **Aussenabmessungen:** 96.0 x 66.0 x 43.5 mm (L x B x H).
- **Lichte Innenmasse:** 88.0 x 58.0 mm (Platinen-Ebene 85.0 x 55.0 mm).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck (oder UV-/kraftstoffbestaendiges ASA im FDM-Verfahren mit min. 6 Perimetern / 2.4 mm Vollwand), kugelgestrahlt, im Heissbad schwarz chemisch geglaettet und hydrophob versiegelt.
- **Schutzart:** IP67 (strahlwasser- und tauchdicht bis 1 m Wassertiefe).

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. DECKEL (3,0 mm Wandstärke + M8 ePTFE Vent + Zentriersteg│  │
├────────────────────────────────────────────────────────────┤  │ 43,5 mm
│ 2. OBERWANNE / ZWISCHENBODEN (15,0 mm lichte Innenhöhe)    │  │ Gesamt-
├────────────────────────────────────────────────────────────┤  │ höhe
│ 3. UNTERWANNE (20,0 mm lichte Innenhöhe + PCB-Dome)        │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.1 Sandwich-Aufbau & Platinenbefestigung
1. **Unterwanne:** Vertiefte Akkutasche (52.0 x 36.0 x 6.5 mm) fuer den LiPo-Pufferakku (mit 3M VHB 4910 Schaumklebeband vibrationsgedaempft) und NTC-Temperatursensor. Vier Ruthex M3 x 5.7 mm Messing-Schmelzeinsaetze.
2. **Elektronik-Ebene:** 4-Lagen-Platine (85.0 x 55.0 mm) auf vier 4.0-mm-Zylinderdomen mit M2.5 x 5 mm Schrauben (Bohrung 3.6 mm fuer Ruthex M2.5 Schmelzeinsaetze) und NBR-O-Ringen schwingungsentkoppelt gelagert.
3. **Zwischenboden / Oberwanne:** Schirmt Leistungselektronik und Akku ab; 6x Lueftungsschlitze (18.0 x 2.5 mm) ermoeglichen inneren Druckausgleich.
4. **Gehaeusedeckel:** Durchgehend ueber vier M3 x 40/45 mm Edelstahl-Zylinderschrauben (DIN 912 / ISO 4762) in die Ruthex M3 Messingbuchsen des Bodens verschraubt ($0{,}8\,\text{Nm}$ Anzugsmoment, gesichert mit *Loctite 243*).

### 1.2 Dichtungskonzept & Druckausgleich
- **Umlaufende Nut-Feder-Dichtung:** 2x NBR- bzw. Silikon-Rundschnuere (Durchmesser 2.0 mm, Shore-Haerte 50–60 A) in 2.5 x 1.5 mm Nuten (25 % definierte Vorkompression).
- **Druckausgleichselement:** M8 x 1.25 Schraubventil mit wasserdichter ePTFE-Membran (Gore Automotive Vent AVS 41 / Schreiner). Luftdurchsatz $> 120\,\text{ml/min}$ bei 70 mbar, Wassereintrittspunkt $> 1{,}5\,\text{bar}$.
- **HD26-Wandflansch:** Wasserdichte IP67 D-Sub HD26 Flanschbuchse mit Silikondichtung in der Gehaeusewand, intern ueber 26-poliges Flachbandkabel auf 2x13 Wannenstecker (J1) spannungsfrei entkoppelt.

---

## 2. Gehaeuse Typ B: Universeller Satelliten-Pod (Identisch fuer Pod 1, 2 und 3)
- **Vollstaendige Modularitaet:** Alle 3 Pod-Positionen am Motorrad nutzen das identische, vollstaendig universelle Gehaeuse.
- **Abmessungen Schacht:** 64.0 x 46.0 x 23.5 mm.
- **Elektronik-Kassette:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).
- **Kontaktblock:** 6-poliges Mill-Max Pogo-Pin-Array (Serie 824-22-006-00-001101, Raster 2.54 mm, 1.4 mm Arbeitshub) mit Silikon-Formschuhdichtung gegen vergoldete ENIG-Pads.
- **3-Stufen-Sicherheitsarretierung:**
  1. *Snap-Lock:* POM-C Federklinken mit akustischem Klick beim Einschieben.
  2. *Cam-Lock:* Stirnseitiger 90-Grad-Edelstahl-Drehriegel blockiert Klinken formschluessig gegen Stoesse $> 20\,\text{g}$.
  3. *Push-to-Eject:* Gummierte Hebelwippe wirft Kassette nach Entriegelung um 8.0 mm aus.
- **Universelle Montage:** Integrierte M5-Rueckenplatte fuer universelle Flachmontage, 3M Dual-Lock oder CNC-Aluminium-Rohrschellen (kompatibel mit allen Standard-Rohrdurchmessern: 22.0 mm, 28.6 mm, 1.0 Zoll sowie Sturzbuegeln von 25 bis 32 mm).

---

## 3. Belegung der universellen 6-Pin Pogo-Kontaktleiste

| Pogo-Pin | Pod 1 & 2 (Links / Rechts: Audio & Intercom-Kassetten) | Pod 3 (Heck: GNSS & OpenMotorMesh LoRa) |
| :---: | :--- | :--- |
| **Pin 1** | **`VCC`** (5V geschaltete Speisespannung via MOSFET) | **`VCC`** (5V Dauer-Versorgung) |
| **Pin 2** | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) |
| **Pin 3** | **`NF_P`** (Symmetrisches Audiosignal + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Zentralbox) |
| **Pin 4** | **`NF_N`** (Symmetrisches Audiosignal - via Bourns) | **`UART_RX`** (Zentralbox $\rightarrow$ Heck-Co-Prozessor) |
| **Pin 5** | **`OPTO`** (TLP222A Tastensimulations-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal Sync) |
| **Pin 6** | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Heck-Kassetten-Erkennung) |

---

## 4. Universeller Kabelbaum (Zentralbox zu Pods)
- **Kabeltyp:** Hochflexibles, oel- und UV-bestaendiges PUR-Kabel mit Geflechtschirm aus verzinntem Kupfer.
- **Adernaufbau:** $2 \times 0.25\,\text{mm}^2$ (VCC / GND fuer bis zu 1 A Ladestrom) + $4 \times 0.14\,\text{mm}^2$ verdrillte Paare (Audio/UART, Opto/PPS, 1-Wire ID).
- **Schirmanschluss:** Der Gesamtschirm ist einseitig an der Zentralbox auf `GND_SHIELD` (Pin 22) niederinduktiv aufgelegt.
- **Fahrzeug-Freiheit:** Dank der identischen Pod-Bauform koennen Pod 1, Pod 2 und Pod 3 an jedem beliebigen Motorradtyp (Harley-Davidson, BMW GS, KTM, Yamaha, Honda, Ducati, Triumph) frei an Rahmenrohren, Sturzbuegeln, Cockpithaltern oder Gepaecktraegern montiert werden.
