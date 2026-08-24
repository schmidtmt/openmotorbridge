# 05 - Mechanische Konstruktion: Zentralbox, Dichtungskonzept, HD26-Wandflansch & Status-LED

Dieses Dokument spezifiziert das IP67-Gehaeusedesign der zentralen Steuerbox (Typ A) mit integriertem **HD26-Wandflansch in der Oberwanne**, **Zwischenboden-Kabeldurchfuehrung** und **wasserdichtem RGB-Lichtleiter**, sowie das universelle Satelliten-Pod-System (Typ B) mit Kassetten-Einschueben.

---

## 1. Gehaeuse Typ A: Zentrale Steuerbox (Unter Sitzbank)
- **Aussenabmessungen:** 96.0 x 66.0 x 43.5 mm (L x B x H).
- **Lichte Innenmasse:** 88.0 x 58.0 mm (Platinen-Ebene 85.0 x 55.0 mm).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck (oder UV-/kraftstoffbestaendiges ASA im FDM-Verfahren mit min. 6 Perimetern / 2.4 mm Vollwand), kugelgestrahlt, im Heissbad schwarz chemisch geglaettet und hydrophob versiegelt.
- **Schutzart:** IP67 (strahlwasser- und tauchdicht bis 1 m Wassertiefe).

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. DECKEL (3,0 mm Wandstärke + M8 ePTFE Vent + LED-Optik)  │  │
├────────────────────────────────────────────────────────────┤  │ 43,5 mm
│ 2. OBERWANNE: HD26-Wandflansch (Stirnseite) + Baffle-Boden │  │ Gesamt-
│    • Flachbandkabel-Durchführung (38 x 6 mm verrundet)     │  │ höhe
│    • LED-Lichtschacht (Ø 5,0 mm) & 4x Druckausgleich-Slots │  │
├────────────────────────────────────────────────────────────┤  │
│ 3. UNTERWANNE: Geschlossene Tauchwanne (20 mm Innenhöhe)   │  │
│    • 4x M2,5 PCB-Dome + vertiefte LiPo-Akkutasche im Boden │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.1 Sandwich-Aufbau & Schichtaufteilung
1. **Unterwanne (20,0 mm Innenhöhe - Geschlossene Tauchwanne):**
   * Vollstaendig geschlossene, durchbruchsfreie Wanne (kein Wassereintritt bei stehender Feuchtigkeit).
   * Vertiefte Akkutasche (52.0 x 36.0 x 6.5 mm) fuer den LiPo-Pufferakku (mit *3M VHB 4910* Schaumklebeband vibrationsgedaempft) und NTC-Temperatursensor.
   * Vier Ruthex M3 x 5.7 mm Messing-Schmelzeinsaetze im Wannenboden fuer die Gehaeusedurchgangsschrauben.
   * 4-Lagen-Platine (85.0 x 55.0 mm) auf vier 4.0-mm-Zylinderdomen mit M2.5 x 5 mm Schrauben und NBR-O-Ringen schwingungsentkoppelt gelagert.
2. **Oberwanne / Zwischenrahmen (15,0 mm Innenhöhe):**
   * Beherbergt den verschraubten **HD26-D-Sub-Wandflansch** an der vorderen Stirnseite.
   * Bietet $12\,\text{mm}$ freie Einbautiefe fuer die Steckerbuchse und eine sanfte Biegeschlaufe fuer das Flachbandkabel.
3. **Gehaeusedeckel (3,0 mm Wandstärke):**
   * Integriert das M8 x 1.25 ePTFE Druckausgleichsventil und den $\varnothing\,3{,}0\,\text{mm}$ PMMA-Lichtleiter fuer die WS2812B RGB-LED.
   * Verschraubt ueber vier durchgehende M3 x 40/45 mm Edelstahl-Zylinderschrauben (DIN 912 / ISO 4762) mit $0{,}8\,\text{Nm}$ Anzugsmoment (gesichert mit *Loctite 243*).

---

## 2. Zwischenboden-Durchfuehrung & Kabelmanagement

Der Zwischenboden der Oberwanne trennt die empfindliche Leiterplatten- und Akkuebene mechanisch vom Steckeranschlussraum, besitzt jedoch praezise Durchbrueche:

```
┌─────────────────────────────────────────────────────────────┐
│              ZWISCHENBODEN DER OBERWANNE (Draufsicht)       │
│                                                             │
│   ┌─────────────────────────────┐     ┌─────────────────┐   │
│   │ 1. Flachbandkabel-Schlitz   │     │ 2. LED-Schacht  │   │
│   │    (38,0 x 6,0 mm)          │     │    (Ø 5,0 mm)   │   │
│   │    Rundum-Fase R1.5 mm      │     │    Freistellung │   │
│   └─────────────────────────────┘     └─────────────────┘   │
│                                                             │
│   [Slot 1]                 [Slot 2]                 [Slot 3]│
│   (15 x 2 mm)              (15 x 2 mm)              (15 x 2)│
│   ◄────────── 4x Innere Druckausgleichs-Schlitze ──────────►│
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Spezifikation der Durchbrueche
1. **Flachbandkabel-Durchfuehrung:**
   * **Abmessungen:** $38{,}0 \times 6{,}0\,\text{mm}$ mit $R=1{,}5\,\text{mm}$ Rundum-Fase an Ober- und Unterkante (verhindert Scheuern oder Kantenabrieb des 26-poligen AWG28 Flachbandkabels bei Fahrzeugvibrationen).
   * **Position:** Direkt vertikal ueber dem 2x13 Wannenstecker `J1` der Hauptplatine angeordnet.
2. **Optischer LED-Lichtschacht:**
   * **Geometrie:** Durchgangsbohrung $\varnothing\,5{,}0\,\text{mm}$, koaxial ueber der SMD-LED `LED1` (WS2812B, GPIO 48) platziert.
   * **Funktion:** Ermoeglicht das ungehinderte Heranfuehren des im Deckel sitzenden PMMA-Lichtleiters bis auf $0{,}8\,\text{mm}$ an die LED-Oberflaeche.
3. **Druckausgleichs- & Belueftungsschlitze:**
   * 4x Labyrinth-Lueftungsschlitze ($15{,}0 \times 2{,}0\,\text{mm}$) ermoeglichen den freien Luftaustausch zwischen Unterwanne und dem M8 ePTFE-Ventil im Deckel, ohne dass lose Kabel nach unten rutschen koennen.

---

## 3. HD26 D-Sub Gehaeusewand-Flansch (In der Oberwanne)

```
    AUSSENSEITE (IP67)                        OBERWANNE (Zentralbox)
┌─────────────────────────┐               ┌─────────────────────────────────┐
│ IP67 HD26 Stecker       │  Flansch-     │ 26-pol. Flachbandkabel (45 mm)  │
│ (Haupt-Kabelbaum)       ├── Dichtung ───┤ mit 2x13 Buchsenleiste (J1)     │
│ 2x M3 Jackscrews O-Ring │  (EPDM 1.5mm) │ ──► Durch Zwischenboden-Schlitz │
└─────────────────────────┘               │ ──► Steckt auf Hauptplatine     │
                                          └─────────────────────────────────┘
```

### 3.1 Mechanische Spezifikation des Flanschausschnitts
* **Ausschnitt-Geometrie:** D-Sub High-Density 26-Pin Ausschnitt ($31{,}0 \times 13{,}0\,\text{mm}$) mit $2{,}0\,\text{mm}$ Radien in der Stirnwand der **Oberwanne**.
* **Flanschdichtung:** Formgenaue EPDM-Flachdichtung ($1{,}5\,\text{mm}$ Staerke, Shore 60 A) zwischen Metallkragen der Amphenol LTW / NorComp SEAL-D Buchse und Gehaeusewand.
* **Verschraubung:** 2x Edelstahl-Sechskantbolzen (UNC 4-40 oder M3 mit O-Ring-Dichtscheiben) klemmen den Flansch mit $0{,}6\,\text{Nm}$ wasserdicht gegen die Wand.
* **Spannungsfreie Entkopplung:** Ein $45\,\text{mm}$ langes, hochflexibles 26-poliges Flachbandkabel (AWG28, Raster 1.27 mm) fuehrt durch den Zwischenboden-Schlitz zur 2x13 Wannenbuchse (J1) auf dem PCB.

---

## 4. Wasserdichter Lichtleiter fuer die WS2812B RGB Status-LED

```
┌─────────────────────────────────────────────────────────────┐
│ GEHAEUSEDECKEL (Wandstaerke 3,0 mm)                         │
│                  ┌──────────────────┐                       │
│                  │  PMMA Lichtleiter│ ◄── O-Ring Dichtung   │
│                  │  (Ø 3,0 mm Matt) │     (IP67 Versiegelung│
│                  └────────┬─────────┘                       │
├───────────────────────────┼─────────────────────────────────┤
│ ZWISCHENBODEN             │ Durchtritt durch Ø 5,0 mm Schacht
├───────────────────────────┼─────────────────────────────────┤
│                           │ Optischer Luftspalt 0,8 mm      │
│                           ▼                                 │
│                  ┌──────────────────┐                       │
│                  │ WS2812B RGB-LED  │                       │
│  HAUPTPLATINE    │ (ESP32 GPIO 48)  │                       │
│  (UNTERWANNE)    └──────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 Optische & Mechanische Spezifikation
* **Lichtleiter-Typ:** PMMA-Praezisions-Lichtleiter mit diffuser, matter Linse (*Bivar PLPC3-3MM* oder *Mentor 1292.1101*), Durchmesser $\varnothing\,3{,}0\,\text{mm}$.
* **Dichtung:** Umlaufender NBR-O-Ring ($\varnothing\,3{,}0\,\text{mm}$ ID, $1{,}0\,\text{mm}$ Schnurstaerke) in Stufenbohrung des Deckels, frontbuendig eingepresst und mit transparentem Polyurethan versiegelt.
* **Sichtbarkeit:** 120°-Abstrahlwinkel, auch bei direkter Sonneneinstrahlung unter der Sitzbank / im Rahmendeckel deutlich sichtbar.

### 4.2 Status-Farbcodierung (LED State Machine)

| LED-Farbe & Muster | Betriebszustand | Bedeutung |
| :--- | :--- | :--- |
| 🟢 **Gruen pulsierend (1 Hz)** | **Normalbetrieb (Online)** | Bordnetz aktiv, alle gesteckten Pods aktiv, DLE OK |
| 🔵 **Blau blinkend (2 Hz)** | **BLE Dashboard / Pairing** | WebApp PWA aktiv verbunden / Datenaustausch |
| 🟡 **Gelb pulsierend (0.5 Hz)**| **USV-Akkubetrieb (KL15 AUS)**| Nachlauf-Modus: GPX Tour-Close & WebDAV Sync |
| 🔴 **Rot schnell blinkend** | **Warnung / Fehler** | Unterspannung Starterbatterie ($< 11{,}8\,\text{V}$) / Kassetten-Kurzschluss |
| 🟣 **Lila leuchtend** | **OMM DLE Leader** | Dieses Motorrad fuehrt die Mesh-Koordination der Gruppe |
| ⚪ **Weiss Doppelblitz** | **Actioncam Marker** | Lenkertaster gedrueckt: GPS Highlight-Marker gesetzt |

---

## 5. Gehaeuse Typ B: Universeller Satelliten-Pod (Identisch fuer Pod 1, 2 und 3)

- **Vollstaendige Modularitaet:** Alle 3 Pod-Positionen am Motorrad nutzen das identische, universelle Gehaeuse.
- **Abmessungen Schacht:** 64.0 x 46.0 x 23.5 mm.
- **Elektronik-Kassette:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).

### 5.1 Kassetten-Trägerplatine & 3D-Board-Render

Die Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`) adaptiert die internen Sena- oder Cardo-OEM-Inlays über einen abgewinkelten Low-Profile JST-SH Stecker auf die 6 vergoldeten Pogo-Kontaktpads:

![OpenMotorBridge Universal Pod Cartridge 3D PCB Render](../../hardware/kicad_pod_cartridge/kicad_3d_render.png)

*Abbildung 5.1: Photorealistisches 3D-Raytracing-Render der Kassetten-Trägerplatine (KiCad 8.0, 35.0 x 25.0 mm, ENIG Gold mit abgewinkeltem JST-SH 1.0 mm Stecker, 6 Pogo-Zielkontaktpads und Maxim DS2401 ID-Chip).*

- **Kontaktblock:** 6-poliges Mill-Max Pogo-Pin-Array (Serie 824-22-006-00-001101, Raster 2.54 mm, 1.4 mm Arbeitshub) mit Silikon-Formschuhdichtung gegen vergoldete ENIG-Pads auf der Kassettenunterseite.
- **Flache Bauhöhe (Low-Profile):** 
  * Interner OEM-Inlay-Anschluss ueber **abgewinkelten Low-Profile SMD-Steckverbinder (JST-SH 1.0 mm, Bauhoehe 1.8 mm)** – verhindert vertikales Auftragen und ermoeglicht ultraflache Kassettengehaeuse ($17.0\,\text{mm}$ Gesamtdicke inkl. OEM-Inlay).
- **Schwingungsdaempfung & Vibrationsentkopplung (Vibration Damping):**
  * **Schwimmende Kassettenlagerung:** Die Kassettenplatine ist im PA12-Gehaeuse ueber eine umlaufende **Shore 40A Silikon-Formschuhdichtung** und zwei **M2-Silikon-Daempfungshuelsen** mechanisch schwingungsentkoppelt gelagert.
  * **Vibrationsfestigkeit:** Daempft hochfrequente Motorvibrationen (Einzylinder, V2, Dreizylinder) bis $20\,\text{g}$ bei $50\dots 500\,\text{Hz}$.
  * **Kontaktstabilitaet:** Der 1.4 mm Pogo-Pin-Arbeitshub mit $60\,\text{g}$ Federkraft pro Pin garantiert unterbrechungsfreien Kontakt ($\Delta R < 5\,\text{m}\Omega$) ohne Audio-Knacken bei harten Schlagloechern.
- **3-Stufen-Sicherheitsarretierung:** Snap-Lock POM-C Klinken mit akustischem Klick, 90°-Cam-Lock Drehriegel gegen Stoesse $> 20\,\text{g}$, Push-to-Eject Wippe.
- **Universelle Montage:** Integrierte M5-Rueckenplatte fuer Flachmontage oder CNC-Aluminium-Rohrschellen (22.0 mm, 28.6 mm, 1.0 Zoll, 25–32 mm Sturzbuegel).

### 5.1 Pod-Druckausgleichsmembran (ePTFE)
* **Problemstellung:** Interne Abwaerme (SX1262 LoRa $+22\,\text{dBm}$ PA, Ladeschaltung) und Sonneneinstrahlung erzeugen Druckdifferenzen im kleinen Pod-Volumen.
* **Spezifikation:** Auf der Rueckseite des Pod-Gehaeuses (geschuetzt in einer Senkung unter der M5-Rueckenplatte) sitzt eine **selbstklebende $\varnothing\,7{,}0\,\text{mm}$ ePTFE-Druckausgleichsmembran** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Funktion:** Belueftungsrate $> 25\,\text{ml/min}$ bei 70 mbar, Wassereintrittspunkt $> 1{,}5\,\text{bar}$ (IP67). Verhindert Vakuum-Wassersaugen bei Abkuehlung durch Regenguesse.

### 5.2 Kabelbaum-Knickschutz & Zugentlastung
* **Schnittstelle:** Kabeleinfuehrung an der Gehaeuseunterseite ueber **M12 x 1.5 IP67-Kabelverschraubung mit integrierter Spiral-Knickschutztuelle** aus UV- und oelbestaendigem Polyamid (PA6) mit NBR-Dichteinsatz.
* **Schutzwirkung:** Garantiert Biegeradius $> 30\,\text{mm}$ und zuverlaessige Zugentlastung ($> 100\,\text{N}$) bei Lenkereinschlaegen und harten Fahrbahnstoessen.

### 5.3 IP67 Blind- / Leerkassette (Dummy Cartridge)
* **Verwendung bei Teilbestueckung:** Wird ein Pod-Schacht temporaer nicht bestueckt (z. B. wenn nur Sena genutzt wird oder ein Pod stillgelegt ist), verschliesst die formidentische **IP67-Leerkassette (`Pod_Dummy_Cartridge_IP67.stl`)** den Schacht vollstaendig.
* **Dichtungskonzept:** Doppelte Silikon-Umlaufdichtung schuetzt die innenliegenden Mill-Max Pogo-Pins vor Schmutz, Spritzwasser und Streusalz.
* **Verriegelung:** Nutzt denselben POM-C Snap-Lock und 90°-Cam-Lock Drehriegel wie aktive Kassetten.
* **Hardware-Zustand:** Die Zentralbox erkennt offene/leere Kontakte und haelt den Slot ueber `disabled.json` strom- und rauschfrei isoliert.

---

## 6. Belegung der universellen 6-Pin Pogo-Kontaktleiste

| Pogo-Pin | Pod 1 & 2 (Links / Rechts: Audio & Intercom-Kassetten) | Pod 3 (Heck: GNSS & Dual-PHY OpenMotorMesh) |
| :---: | :--- | :--- |
| **Pin 1** | **`VCC`** (5V geschaltete Speisespannung via MOSFET) | **`VCC`** (5V Dauer-Versorgung) |
| **Pin 2** | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) |
| **Pin 3** | **`NF_P`** (Symmetrisches Audiosignal + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Zentralbox) |
| **Pin 4** | **`NF_N`** (Symmetrisches Audiosignal - via Bourns) | **`UART_RX`** (Zentralbox $\rightarrow$ Heck-Co-Prozessor) |
| **Pin 5** | **`OPTO`** (TLP222A Tastensimulations-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal Sync) |
| **Pin 6** | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Heck-Kassetten-Erkennung) |
