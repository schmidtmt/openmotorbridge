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

### 5.1 Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`) & 3D-Board-Renders

Die universelle Kassetten-Trägerplatine bildet das Herzstück jeder Wechselkassette. Sie dient als mechanische und elektrische Brücke zwischen der fahrzeugseitigen Pod-Basis und den internen Docking-Kontakten der jeweiligen Headset-Schale:

#### Oberansicht (Inlay-Header, 1-Wire ID & Entkopplung):
![OpenMotorBridge Kassetten-Trägerplatine Oberansicht 3D-Render](../../hardware/kicad_pod_cartridge/cartridge_3d_render_top.png)

#### Unteransicht (6-Pin Buchsenleiste zum direkten Aufstecken auf die Pod-Basis):
![OpenMotorBridge Kassetten-Trägerplatine Unteransicht 3D-Render](../../hardware/kicad_pod_cartridge/cartridge_3d_render_bottom.png)

*Abbildung 5.1: Photorealistisches 3D-Raytracing-Render der Kassetten-Trägerplatine (KiCad 8.0, 35.0 x 25.0 mm, ENIG Gold mit nach unten öffnender 6-Pin Buchsenleiste auf B.Cu, Low-Profile JST-SH 1.0 mm Header auf F.Cu und Maxim DS2401 ID-Chip).*

#### Platinenaufbau im Detail:
* **Unterseite (`B.Cu` – Gegenstelle zur Pod-Basis):**
  * **6-Pin Buchsenleiste (`J1` / PinSocket 2.54 mm):** Sitzt zentriert auf der Unterseite und öffnet senkrecht nach unten. Beim Einschieben der Kassette gleiten die nach oben ragenden Pins der Pod-Basis direkt und formschlüssig in diese Buchse.
  * **Massefläche (`GND Shield Plane`):** Großflächige Kupferanbindung zur Abschirmung und Stabilisierung.
* **Oberseite (`F.Cu` – Docking-Schnittstelle & ID):**
  * **Low-Profile Inlay-Header (`J2`):** Um 90° gekippter **JST-SH 1.0 mm 6-Pin SMD-Steckverbinder** (Bauhöhe nur $1{,}8\,\text{mm}$). Ein kurzes internes Kabel verbindet diesen Header werkzeuglos mit dem im Kassetten-Deckel integrierten Docking-Schacht des Nutzers.
  * **Digitaler Kassetten-ID-Chip (`U1`):** **Maxim DS2401Z+** Silicon Serial ROM (SOT-23) speichert eine weltweit eindeutige 64-Bit ROM-ID. Die Zentralbox erkennt beim Einstecken in Millisekunden, welches Headset-Profil geladen werden muss (z. B. `sena_50_series.json`, `cardo_dmc_gen2.json`).
  * **Entkopplungskondensator (`C1`):** 100nF 0603 Keramikkondensator zur Filterung der 1-Wire-Busleitung.
* **Mechanische Schwingungsdämpfung (`H1`, `H2`):**
  * 2x M2-Befestigungsbohrungen mit Shore 40A Silikonhülsen lagern die Platine schwimmend im PA12-Kassettengehäuse gegen Fahrbahnstöße bis zu $20\,\text{g}$.

---

### 5.2 Benutzerzentrierte Plug & Play Docking-Architektur (0 Lötaufwand)

Ein zentrales Entwicklungsziel von OpenMotorBridge ist die **100 % zerstörungsfreie und löt-freie Nutzung** durch jeden Motorradfahrer:

```
┌─────────────────────────────────────────────────────────────┐
│ WECHSELKASSETTE (z. B. "Sena 50S" oder "Cardo Edge Edition")│
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ DOCKING-SCHACHT IM KASSETTENDECKEL                    │  │
│  │ (Fahrer klickt sein Original-Headset hier ein)        │  │
│  │                                                       │  │
│  │  [ Originale Gegen-Federkontakte / Pogo-Pins ]        │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │ Kurzes internes JST-SH Kabel  │
│                             ▼                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ KASSETTEN-TRÄGERPLATINE (Carrier PCB, 35x25mm)        │  │
│  │  - J2: JST-SH 6P Header (Oberseite)                   │  │
│  │  - U1: DS2401 ID-Chip (Meldet Gerätetyp an ESP32)     │  │
│  │  - J1: 6-Pin Buchse (Unterseite)                      │  │
│  └──────────────────────────┬────────────────────────────┘  │
└─────────────────────────────┼───────────────────────────────┘
                              ▼ (Steckt beim Kassetteneinschub)
┌─────────────────────────────┼───────────────────────────────┐
│ POD-BASISPLATINE            │                               │
│  - J1: 6-Pin PinHeader ◄────┘ (Oberseite)                   │
│  - U1: SP3012 TVS-Schutzmatrix                              │
│  - J2: Zentrierte M8 6-Pin IP67 Buchse (Unterseite)         │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
        M8-Kabelbaum zum Motorrad / Zentralbox
```

#### Modulare Kassetten-Varianten (Community- & 3D-Druck-Vorlagen):
1. **Sena 50S / 30K / 20S EVO Edition:** Nutzt die originale Federkontakt-Leiste des Helm-Klemmsatzes. Das Gerät wird einfach von oben eingerastet.
2. **Cardo Packtalk Edge / Pro Edition:** Integriert das magnetische *Air Mount*-Kontaktfeld für werkzeugloses Andocken.
3. **Cardo Packtalk Bold / Black Edition:** Nutzt die Schiebe-Gegenkontakte der Cardo-Audiokit-Basis.
4. **Sena Spider / Apex / OEM-Inlay Edition:** Für Bastler, die eine ausgebaute Bare-Board-Platine fest im Kassettenkörper montieren wollen.
5. **PMR446 Funkgeräte-Edition:** Integriert einen Midland G9 / Kenwood-Doppelklinken-Anschluss für analoge PMR-Handfunkgeräte.

---

### 5.3 Pod-Druckausgleichsmembran (ePTFE)
* **Problemstellung:** Interne Abwaerme (SX1262 LoRa $+22\,\text{dBm}$ PA, Ladeschaltung) und Sonneneinstrahlung erzeugen Druckdifferenzen im kleinen Pod-Volumen.
* **Spezifikation:** Auf der Rueckseite des Pod-Gehaeuses (geschuetzt in einer Senkung unter der M5-Rueckenplatte) sitzt eine **selbstklebende $\varnothing\,7{,}0\,\text{mm}$ ePTFE-Druckausgleichsmembran** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Funktion:** Belueftungsrate $> 25\,\text{ml/min}$ bei 70 mbar, Wassereintrittspunkt $> 1{,}5\,\text{bar}$ (IP67). Verhindert Vakuum-Wassersaugen bei Abkuehlung durch Regenguesse.

---

### 5.4 IP67 Blind- / Leerkassette (Dummy Cartridge)
* **Verwendung bei Teilbestueckung:** Wird ein Pod-Schacht temporaer nicht bestueckt (z. B. wenn nur Sena genutzt wird oder ein Pod stillgelegt ist), verschliesst die formidentische **IP67-Leerkassette (`Pod_Dummy_Cartridge_IP67.stl`)** den Schacht vollstaendig.
* **Dichtungskonzept:** Doppelte Silikon-Umlaufdichtung schuetzt die innenliegenden Kontakte vor Schmutz, Spritzwasser und Streusalz.
* **Verriegelung:** Nutzt denselben POM-C Snap-Lock und 90°-Cam-Lock Drehriegel wie aktive Kassetten.
* **Hardware-Zustand:** Die Zentralbox erkennt offene/leere Kontakte und haelt den Slot ueber `disabled.json` strom- und rauschfrei isoliert.

---

### 5.5 Pod-Basisplatine (`openmotorbridge_pod_base`) & Zentrische Kassetten-Führung

Der mechanische und elektrische Übergang von der Wechselkassette auf die M8-Kabelverbindung zum Motorradkabelbaum erfolgt über die zentrierte **Pod-Basisplatine (`openmotorbridge_pod_base`)**:

#### Oberansicht (Senkrechte/Horizontale 6-Pin Stiftleiste & SP3012 TVS-Schutzstufe):
![OpenMotorBridge Pod-Basisplatine Oberansicht 3D-Render](../../hardware/kicad_pod_base/pod_base_3d_render_top.png)

#### Unteransicht (Zentrierte M8 6-Pin IP67-Buchse & GND-Schirmfläche):
![OpenMotorBridge Pod-Basisplatine Unteransicht 3D-Render](../../hardware/kicad_pod_base/pod_base_3d_render_bottom.png)

* **Abmessungen:** $36{,}0 \times 20{,}0\,\text{mm}$ (Kompakte 2-Layer FR4-Basisplatine mit großzügigen Leiterbahn- und Schutzabständen).
* **Zentrierte 6-Pin Stiftleiste (`J1`) mit PA12-Schutzkragen:** 6-poliges Präzisions-Pin-Array ($2{,}54\,\text{mm}$ Raster, vergoldet) exakt auf der horizontalen Mittelachse ($Y=0, Z=0$).
* **Integrierte PA12-Schutzwandung & Fangtrichter:** Das Gehäuse bildet um die Stiftleiste `J1` eine **4-seitige, $1{,}2\,\text{mm}$ starke Schutzwand mit $45^\circ$-Einlaufschrägen**. Die Buchsenleiste der Wechselkassette gleitet formschlüssig und saugend wie ein Kolben in diese Wanne ein – die Stifte sind fingersicher gekapselt und können niemals verbogen oder verkantet werden.
* **Integrierte ESD-Schutzmatrix (`U1`):** **Littelfuse SP3012-06UTG** (6-Kanal TVS-Array mit $< 0{,}5\,\text{pF}$ parasitärer Kapazität) leitet elektrostatische Entladungen beim Berühren der Kontakte blitzschnell gegen Masse ab.
* **Zentrierte M8-Rundsteckverbinder-Buchse (`J2`):** Metallgekapselte **M8 6-Pin A-Coded IP67 Einbaubuchse** (IEC 61076-2-104) mit massivem Montagesockel und Gewindekragen exakt im geometrischen Zentrum der Platinenunterseite (`B.Cu`) verlötet.
* **Mechanische Entkopplung & Montage (`H1`, `H2`):** 2x M2 Montagebohrungen mit Shore 40A Silikondämpfung gegen Fahrbahnvibrationen. Steckkräfte werden zu 100% vom Gehäuseendanschlag aufgenommen.

---

### 5.6 Zentrischer Kassetteneinschub & Poka-Yoke Führungskonzept

Um Verkanten, schiefe Krafteinleitung und fehlerhaftes Einstecken physikalisch auszuschließen, ist der Kassetteneinschub **in allen Raumachsen exakt zentriert**:

```
                  ◄──────────── 44.0 mm Pod-Breite ────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                    3.0 mm Gehäuse-Deckel                    │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 24.0 mm
 │ │   │                                                 │   │ │ │ Pod-
 │ │3.0│         ZENTRISCHER KASSETTEN-EINSCHUB          │3.0│ │ │ Höhe
 │ │mm │                 (38 x 18 mm)                    │mm │ │ │
 │ │   │                                                 │   │ │ │
 │ │Nut├───────────► ┌─────────────────────┐ ◄───────────┤Nut│ │ │
 │ │1.5│             │  6-PIN STECKER      │             │2.0│ │ │
 │ │mm │             │  (Exakt zentriert)  │             │mm │ │ │
 │ │   │             └─────────────────────┘             │   │ │ │
 │ └───┴─────────────────────────────────────────────────┴───┘ │ │
 │                    3.0 mm Gehäuse-Boden                     │ │
 └─────────────────────────────────────────────────────────────┘ ▼
```

#### 4-Stufen-Sicherheit für perfekten Kassetten-Sitz:
1. **Vollkommen zentrische Geometrie:**
   * **Breite ($Y$):** Bei $44{,}0\,\text{mm}$ Pod-Außenbreite und $38{,}0\,\text{mm}$ Schachtbreite ergeben sich beidseitig symmetrische **$3{,}0\,\text{mm}$ Wandstärken**.
   * **Höhe ($Z$):** Bei $24{,}0\,\text{mm}$ Pod-Außenhöhe und $18{,}0\,\text{mm}$ Schachthöhe ergeben sich symmetrische **$3{,}0\,\text{mm}$ Decken- und Bodenstärken**.
   * Die Steckverbindung liegt exakt im Schnittpunkt der Symmetrieachsen $\rightarrow$ **Null Hebelwirkung oder Kippmomente**.
2. **Poka-Yoke Verpolschutz (Asymmetrische Führungsnuten):**
   * Linke Führungsnut: $1{,}5\,\text{mm}$ Breite.
   * Rechte Führungsnut: $2{,}0\,\text{mm}$ Breite.
   * Ein verkehrtes (über Kopf) Einschieben der Kassette ist mechanisch unmöglich.
3. **$45^\circ$-Zentriertrichter am Kassettenkopf:**
   * Die Kassettennase besitzt um den Steckerausschnitt eine umlaufende $45^\circ$-Einführschräge mit $\pm 1{,}2\,\text{mm}$ Fangbereich. Die Kontakte werden vor dem elektrischen Schluss perfekt zentriert.
4. **Formschlüssiger Endanschlag:**
   * Die Einschubkraft wird nach $4{,}5\,\text{mm}$ Kontakttiefe direkt vom massiven Gehäusekörper (PA12) abgefangen – die Platinen-Lötstellen bleiben zu 100 % kräftefrei.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              SCHNITTSTELLEN-ÜBERGANG POD-BASIS & KASSETTE               │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. DOCKING-SCHACHT KASSETTENDECKEL:                                     │
│    • Original-Headset (Sena 50S / Cardo Edge) werkzeuglos eingeklinkt   │
│    • Internes JST-SH 6P Flachbandkabel zur Kassetten-Trägerplatine       │
│                               ▼                                         │
│ 2. KASSETTEN-TRÄGERPLATINE (openmotorbridge_pod_cartridge, 35x25mm):     │
│    • DS2401 1-Wire ID ROM (Meldet Headset-Typ an ESP32)                 │
│    • 500mA PTC-Sicherung + grüne 5V Power-Status-LED                    │
│    • 6-Pin Präzisionsbuchsenleiste (zentriert)                          │
│                               ▼ (Horizontaler Kassetteneinschub)        │
│ 3. POD-BASISPLATINE (openmotorbridge_pod_base, 36x20mm):                │
│    • 6-Pin Stiftleiste an der inneren Stirnwand (zentriert)             │
│    • Integrierte ESD-Schutzmatrix (Littelfuse SP3012, 6x TVS < 0.5pF)   │
│    • Zentrierte M8 6-Pin A-Coded IP67 Einbaubuchse auf Unterseite (B.Cu)│
│                               ▼ (M8-Außengewinde ragt nach unten)       │
│ 4. MODULARE M8-EINBAUBUCHSE (Gehäuseunterseite):                        │
│    • M8 6-Pin A-Coded IP67-Buchse mit Führungsnut (Poka-Yoke)           │
│    • Vollmetall-Schirmkragen für 360° EMV-Schirmung                     │
│                               ▼                                         │
│ 5. MODULARES M8-ZU-M8 PUR-VERBINDUNGSKABEL (0.5m .. 2.0m):              │
│    • Geschirmtes 6-adriges PUR-Kabel (Halogenfrei, Öl- & UV-beständig)  │
│    • 2x Power (0.34 mm²) + 2x Audio/UART verdrillt (0.14 mm²) + 2x Sign.│
│    • Beidseitig M8 6-Pin IP67 Stecker mit Rüttelsicherung               │
│                               ▼                                         │
│ 6. ZENTRALBOX HD26-KABELBAUMPEITSCHE (Unter der Sitzbank):              │
│    • 3x M8 6-Pin Buchsen (Pod 1 Links, Pod 2 Rechts, Pod 3 Heck)        │
│    • 1x M8 4-Pin / Superseal (Bordnetz KL30/KL15/GND/Schirm)            │
│    • 1x M8 4-Pin (CAN-Bus Telemetrie & Front-Umgebungsmikrofon)         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.6 3D-Röntgen-Architektur (X-Ray CAD) & Baugruppen-Explosionsansicht

Zur ganzheitlichen Verifikation der Passungen, Dichtebenen und elektrischen Übergänge wurde die mechanische Gesamtanordnung des **Satelliten-Pods** und der **Wechselkassette** in einer transluzenten Röntgen-Darstellung (*Ghosted X-Ray*) sowie einer Explosionsansicht modelliert:

#### Transluzente 3D-Röntgenansicht (Stirnwand-Adapter & Sena Apex Inlay):
![OpenMotorBridge 3D X-Ray CAD Architektur](../../hardware/cad/openmotorbridge_pod_assembly_render_xray.png)

#### Baugruppen-Explosionsdarstellung (Hierarchie entlang der Einschubachse):
![OpenMotorBridge 3D Explosionsansicht](../../hardware/cad/openmotorbridge_pod_exploded_view.png)

#### Mechanische Spezifikationen & Passungen:
* **Pod-Außengehäuse:** Makrolon 2805 Polycarbonat / PA12 MJF ($68{,}0 \times 44{,}0 \times 24{,}0\,\text{mm}$, Schacht-Innenmaß $54{,}0 \times 38{,}0 \times 18{,}0\,\text{mm}$, ultraflache Bauhöhe von nur $24\,\text{mm}$).
* **Pod-Basisplatine (`openmotorbridge_pod_base`):** $36{,}0 \times 20{,}0 \times 1{,}6\,\text{mm}$ Adapterplatine mit zentrierter M8 6-Pin IP67 Vollmetallbuchse (B.Cu) und senkrechter 6-Pin Stiftleiste (F.Cu).
* **Wechselkassette:** $52{,}0 \times 36{,}0 \times 16{,}5\,\text{mm}$ Gehäuseschale mit POM-C Schnappriegel ($> 85\,\text{N}$ Haltekraft), Grifffläche für Motorradhandschuhe und PMMA-Statuslichtleiter.
* **Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`):** $35{,}0 \times 25{,}0 \times 1{,}2\,\text{mm}$ FR4-Adapter mit DS2401 1-Wire ID, abgewinkeltem JST-SH 1.0mm 6P Flex-Verbinder (F.Cu) und 6-Pin Buchsenleiste (B.Cu).
* **IP67-Dichtebene:** Der umlaufende $37{,}0 \times 17{,}0\,\text{mm}$ Shore 40A Silikon-Stirnflansch wird beim Einschieben um $0{,}6\,\text{mm}$ vorkomprimiert und dichtet die Kassettenkammer hermetisch gegen Strahlwasser und Staub ab.

---

## 6. Belegung der 6-Pin M8 / Pogo-Schnittstelle & PUR-Kabelbaum-Farbcodierung

| M8 / Pogo-Pin | Leitungsfarbe (PUR-Kabel) | Querschnitt | Signal Pod 1 & 2 (Audio & Intercom) | Signal Pod 3 (Heck-Transceiver) | Schirmung & Verdrillung |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Pin 1** | **Rot (RD)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`VCC`** (5V geschaltete Speisespannung via MOSFET) | **`VCC`** (5V Dauer-Versorgung) | Einzelader (Power) |
| **Pin 2** | **Schwarz (BK)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) | Einzelader (Power Ground) |
| **Pin 3** | **Weiß (WH)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_P`** (Symmetrisches Audiosignal + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Box) | **Paar 1 verdrillt** (mit Pin 4) |
| **Pin 4** | **Blau (BU)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_N`** (Symmetrisches Audiosignal - via Bourns) | **`UART_RX`** (Box $\rightarrow$ Heck-Co-Prozessor) | **Paar 1 verdrillt** (mit Pin 3) |
| **Pin 5** | **Gelb (YE)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`OPTO`** (TLP222A Tastensimulations-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal) | Einzelader (Steuersignal) |
| **Pin 6** | **Grün (GN)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Heck-Kassetten-Erkennung)| Einzelader (1-Wire Bus) |
| **M8-Gehäuse**| **Kupfergeflecht (BL)**| $> 85\,\%$ Geflecht | **`GND_SHIELD`** (360° Gehäuseschirmung) | **`GND_SHIELD`** (360° Gehäuseschirmung) | Gesamtschirm über M8-Metallkragen |


