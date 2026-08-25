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

- **Vollstaendige Modularitaet:** Alle 3 Pod-Positionen am Motorrad nutzen das identische, universelle Gehaeuse im **generischen Maximal-Envelope ($120{,}0 \times 64{,}0 \times 32{,}0\,\text{mm}$)**.
- **Abmessungen Schacht:** $96{,}0 \times 56{,}0 \times 24{,}0\,\text{mm}$ (PA12 MJF, $3{,}0\,\text{mm}$ Wandstärke).
- **Elektronik-Kassette / Schlitten:** $92{,}0 \times 54{,}0 \times 23{,}5\,\text{mm}$ (Lichter Innenbauraum: $88{,}0 \times 50{,}0 \times 23{,}5\,\text{mm}$).

### 5.1 Offener Kassetten-Einschubschlitten (Open Sled Architecture) & Trägerplatine

Die Wechselkassette ist als **offener U-förmiger Einschubschlitten (Open Carrier Sled)** konstruiert:

```
                  ◄──────────── 64.0 mm Pod-Breite ────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                    3.0 mm Gehäuse-Deckel                    │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 32.0 mm
 │ │   │                                                 │   │ │ │ Pod-
 │ │3.0│      OFFENER SCHLITTEN-BAURAUM (KEIN DECKEL!)   │3.0│ │ │ Höhe
 │ │mm │      Volle 23.5 mm lichte Bauhöhe für Antennen  │mm │ │ │
 │ │   │      Headset-Inlays & OMM-Transceiver-Module    │   │ │ │
 │ │Nut├───────────► ┌─────────────────────┐ ◄───────────┤Nut│ │ │
 │ │1.5│             │  6-PIN BUCHSE       │             │2.0│ │ │
 │ │mm │             │  (Piston-Einschub)  │             │mm │ │ │
 │ │   │             └─────────────────────┘             │   │ │ │
 │ └───┴─────────────────────────────────────────────────┴───┘ │ │
 │                    3.0 mm Gehäuse-Boden                     │ │
 └─────────────────────────────────────────────────────────────┘ ▼
```

#### Vorteile des offenen Großraum-Schlittens:
1. **100% generische Kompatibilität:** Passt für alle gängigen Headset-Formfaktoren (Sena 50S/60S, Cardo Packtalk Edge/Pro/Bold, Midland) sowie für das eigenständige OpenMotorMesh-Transceiver-Modul mit GNSS & LoRa.
2. **Keine Doppelwandung:** Es wird kein separater Kassetten-Deckel benötigt. Das spart Materialstärke und eliminiert eine dämpfende Luftschicht.
3. **Volle Innenraumhöhe ($23{,}5\,\text{mm}$):** GNSS-Keramik-Patchantennen ($25 \times 25 \times 4\,\text{mm}$), LoRa-Helical-Spulen, Akkus und Headset-Module haben uneingeschränkten Freiraum nach oben.
4. **Schutz durch Pod-Hülle:** Nach dem Einschieben übernimmt die geschlossene, wetterfeste PA12-Decke des Pod-Gehäuses ($3{,}0\,\text{mm}$) den robusten mechanischen und hermetischen Schutz nach oben.

---

### 5.2 IP67-Seitendichtung (Stirnflansch) & Snap-Fit Click-Verriegelung

```
    AUSSENSEITE (IP67)                        POD-EINSCHUB-SCHACHT
┌─────────────────────────┐               ┌─────────────────────────────────┐
│ PA12-Abschlussblende    │  Umlaufende   │ Offener U-Einschubschlitten     │
│ mit Griffleiste          ├── Flansch- ───┤ mit Kassettenplatine & Modul    │
│ Duale Snap-Fit Rasten   │  Dichtung     │ ──► Gleitet über Poka-Yoke Nut  │
│ (Taktiles "Klick")      │  (Shore 40A)  │ ──► Buchse gleitet in Shroud    │
└─────────────────────────┘               └─────────────────────────────────┘
```

1. **Umlaufende Stirnflansch-Dichtung (IP67 Seal):**
   * Die äußere Abschlussblende des Schlittens besitzt eine integrierte Nut mit einer **Shore 40A Silikon-Profildichtung** ($1{,}5\,\text{mm}$ Schnurstärke).
   * Beim vollständigen Einschieben presst die Stirnblende die Dichtung gegen den Gehäusekragen des Pods und dichtet den gesamten Schacht **zu 100% wasser- und staubdicht nach IP67** ab.
2. **Duale Snap-Fit Schnellverriegelung (Click-Lock):**
   * Integrierte POM/PA12-Rastnasen an den Seitenwänden des Schlittens rasten beim Erreichen des Endanschlags formschlüssig in die Rastkerben des Pod-Gehäuses ein.
   * Die elastische Kompression der Silikondichtung sorgt für ständige Zugspannung – **absolut vibrationsfest, rüttelsicher (> 20 g) und spielfrei**.
   * **Werkzeuglose Entriegelung:** Zwei seitliche ergonomische Entriegelungstaster an der Blende lösen die Rastung durch einfaches Zusammendrücken mit Daumen und Zeigefinger.

---

### 5.3 Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`)

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
│  │ DOCKING-SCHACHT & 3D-KONTUR-NEGATIVBETT               │  │
│  │ (Fahrer klickt sein Original-Headset hier ein)        │  │
│  │                                                       │  │
│  │  [ Originale Gegen-Federkontakte / Pogo-Pins ]        │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │ Geschützter JST-SH Kabelkanal │
│                             │ (1.5mm Schacht unter Bettung) │
│                             ▼                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ KASSETTEN-TRÄGERPLATINE (Carrier PCB, 60x36mm)        │  │
│  │  - J2: JST-SH 6P Header (Oberseite F.Cu)              │  │
│  │  - U1: DS2401 ID-Chip (Meldet Gerätetyp an ESP32)     │  │
│  │  - J1: 6-Pin Buchse (Unterseite B.Cu)                 │  │
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

#### 5.2.1 Geschützter interner JST-SH Kabelkanal & Anschlusspunkte an den Adaptern

Um die Signale vom 90°-abgewinkelten **JST-SH 1.0 mm 6-Pin SMD-Steckverbinder (`J2`)** auf der Kassetten-Trägerplatine absolut verwechslungs- und knickfrei zu den Kontaktpunkten des jeweiligen Adapters zu führen, besitzt der Kassetten-Schlitten folgende Struktur:

1. **Geschützter Unterflur-Kabelkanal (*Under-Bed Routing Channel*):**
   * Im Boden des PA12-Schlittens ist eine **$1{,}5\,\text{mm}$ tiefe und $8{,}0\,\text{mm}$ breite Kabelführung** direkt unterhalb des 3D-Kontur-Negativbetts eingefräst/eingedruckt.
   * Das hochflexible, silikonisolierte 6-adrige JST-SH Flachbandkabel liegt vollständig verdeckt unter dem Dämpfungsinlay. Beim Einsetzen oder Entnehmen des Intercoms besteht keinerlei Kontakt oder Quetschgefahr.
2. **Standardisierte Pin-Belegung am JST-SH 6P Header (`J2`):**

| Pin | Signal-Name | Funktion am Headset-Adapter | Sena 50S/60S Pad | Cardo Edge Pad | Midland XT / PMR |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Gemeinsamer Massebezug | Pin 1 (GND) | Pin 1 (GND) | Masse / Shield |
| **2** | `5V_VBUS` | Gefilterte Ladespeisung (500mA PTC) | Pin 2 (USB-5V) | Pin 2 (5V Charge)| 5V DC In |
| **3** | `AUDIO_R+` | Audio Diff-Out + (zum Lautsprecher-In) | Pin 4 (Spk R+) | Pin 3 (Spk +) | Speaker In + |
| **4** | `AUDIO_R-` | Audio Diff-Out - (Lautsprecher-Rückleiter)| Pin 5 (Spk R-) | Pin 4 (Spk -) | Speaker In - |
| **5** | `MIC_IN+` | Audio Diff-In + (vom Mikrofon-Out) | Pin 6 (Mic +) | Pin 5 (Mic +) | Mic Out + |
| **6** | `OPTO_PTT` | Optokoppler PTT / Button Synthesis | Pin 7 (Mesh-Btn)| N/C (Aux) | PTT Switch |

3. **Verbindungspunkte an den drei Ziel-Adaptern:**
   * **Sena 50S / 60S:** Das JST-SH Kabel mündet an der Lötseite der 7-Pin Federkontaktleiste (Pogo Pins) im Konturbett. Die Pins drücken federnd direkt auf die vergoldeten Sena-Außenkontakte.
   * **Cardo Packtalk Edge / Pro:** Das JST-SH Kabel kontaktiert die 5 Federpads des magnetischen Air Mounts von unten.
   * **Midland XT / PMR446:** Das JST-SH Kabel wird wahlweise mit einer 4-Pin Stiftleiste auf die entkernte Platine gesteckt oder direkt an die 2-Pin Doppelklinkenbuchse ($2{,}5\,\text{mm} + 3{,}5\,\text{mm}$) der Frontblende gelötet.

#### Modulare Kassetten-Varianten (Community- & 3D-Druck-Vorlagen):
1. **Sena 50S / 60S / 30K / 20S EVO Edition:** Nutzt die originale Federkontakt-Leiste des Helm-Klemmsatzes. Das Gerät wird einfach von oben eingerastet.
2. **Cardo Packtalk Edge / Pro Edition:** Integriert das magnetische *Air Mount*-Kontaktfeld für werkzeugloses Andocken.
3. **Cardo Packtalk Bold / Black Edition:** Nutzt die Schiebe-Gegenkontakte der Cardo-Audiokit-Basis.
4. **Midland Intercom Edition (BT Mini / BTR1 Advanced / Rush / Wave):** Docking-Aufnahme für Midland Bluetooth- und Wave-Mesh-Intercoms ($70\dots 85\,\text{mm}$ Baubreite).
5. **Midland XT / Compact PMR446 Bare-Board Edition:** Nimmt die entkernte Platine eines kompakten Midland-Handfunkgeräts (z. B. XT10/XT30/G5, $\approx 68 \times 42 \times 10\,\text{mm}$ ohne Batteriefach) direkt im Schlitten auf. Stromversorgung direkt über 5V-Bordnetz, PTT-Steuerung über PhotoMOS-Relais.
6. **Integrierte PMR446 Transceiver-Edition (SA818S / RDA1846):** Vollständig integriertes 500mW PMR446-Analogfunkmodul ($38 \times 20\,\text{mm}$) direkt auf der Kassetten-Trägerplatine – wahlweise mit interner 446-MHz-Helix oder robuster SMA-Frontbuchse.
7. **PMR446 Doppelklinken-Adapter Edition:** Spritzwassergeschützter Midland/Kenwood 2-Pin Anschluss ($2{,}5\,\text{mm} + 3{,}5\,\text{mm}$) an der Kassettenblende zum Anstecken externer Großgeräte (Midland G9 Pro / G13).

---

### 5.3 Detaillierte Fixiermechanismen: 3D-Kontur-Negativbett & EPDM-Spannlasche

Zur vibrationsfesten, spielfreien und werkzeuglosen Arretierung der Intercoms und Funkmodule kombiniert jede Kassette ein **dreistufiges Haltesystem**:

```
 ┌─────────────────────────────────────────────────────────────┐
 │       ELASTISCHE EPDM-SPANNLASCHE MIT SCHNELL-PULLTAB       │ ◄─── Zieht Gerät nach unten
 └──────────────────────────────┬──────────────────────────────┘
                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │        ORIGINAL-HEADSET (SENA 50S / CARDO EDGE / MIDLAND)   │
 └──────────────────────────────┬──────────────────────────────┘
                                ▼ (Form- & Kraftschluss)
 ┌─────────────────────────────────────────────────────────────┐
 │ 3D-KONTUR-NEGATIVBETT (Exaktes Negativ der Geräte-Rückseite)│ ◄─── 100% spielfrei & zentriert
 │  • Schwingungsdämpfende TPU/NBR-Bettung (Shore 40A, 0.8 mm) │
 │  • Integrierte OEM-Schnappriegel / Neodym-Magnete           │
 └─────────────────────────────────────────────────────────────┘
```

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../../hardware/cad/cartridge_variants_trio.png)

*Abbildung 5.2: 3D-CAD-Visualisierung der drei Referenz-Kassettenaufnahmen mit formschlüssigem 3D-Kontur-Negativbett und elastischer EPDM-Spannlasche im offenen Großraum-Schlitten ($92 \times 54 \times 23{,}5\,\text{mm}$): Sena Quick-Snap Cradle (links), Cardo Magnetic Air Mount (Mitte) und Midland Dovetail Slide / Bare-PCB Inlay (rechts).*

#### 1. Sena 50S / 60S Kontur-Nest & Snap-Cradle
* **3D-Kontur-Negativbett:** Der Schlittenboden ist als exaktes 3D-Negativ der Sena-Gehäuseunterseite ausgeformt. Das Gerät sinkt $4{,}0\,\text{mm}$ tief in die Aussparung ein und kann sich in $X$- und $Y$-Richtung nicht um einen Zehntelmillimeter verschieben.
* **OEM-Klick-Arretierung:** Formschlüssige untere Haltenase ($4{,}0\,\text{mm}$ *Bottom Hook*) und oberer federbelasteter POM-Rastriegel (*Top Release Latch*). Das Gerät klinkt mit einem satten Klick ein.
* **Elastische EPDM-Sicherungslasche (Gummilasche):** Eine $12\,\text{mm}$ breite, UV- und ölbeständige EPDM-Spannlasche spannt sich quer über die Gehäusemitte und wird an seitlichen T-Ankern eingehängt. Sie zieht das Sena permanent nach unten in das Konturbett – **100 % rüttel- und klapperfrei auch bei harten Offroad-Schlägen**.
* **Elektrischer Übergang:** 7-poliges vergoldetes Federkontaktfeld (Pogo-Array) greift direkt auf die originalen Gegenkontakte des Sena-Geräts; JST-SH 6P Flachbandkabel zur Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`).

#### 2. Cardo Packtalk Edge / Pro Magnetic Air Mount & Kontur-Nest
* **3D-Kontur-Negativbett:** Die Aufnahme bildet die geschwungene Unterseite des Packtalk Edge exakt nach. Eine $0{,}8\,\text{mm}$ Shore 40A Silikoneinlage dämpft Motor- und Fahrbahnstöße ab.
* **Dual-N52-Magnetanzug & Klickflanken:** Zwei Neodym-Magnete ($2\times \varnothing\,8 \times 2\,\text{mm}$ N52) ziehen das Gerät passgenau in die Kontur. Zwei seitliche PA12/POM-Sicherungsflanken greifen formschlüssig in die Cardo-Haltenuten ($> 120\,\text{N}$ Abreißkraft).
* **Elastische EPDM-Sicherungslasche:** Zusätzliche elastische Gummilasche für extreme Bedingungen (Enduro/Gravel), die ein vertikales Ausfedern mechanisch unmöglich macht.
* **Elektrischer Übergang:** 5-Pin Federkontaktfeld stellt blitzschnell den Kontakt zu Audio, Mic und 5V-Speisung her.

#### 3. Midland BTR1 Advanced & XT30 Slide / Kontur-Klemme
* **Für Midland Intercoms (BTR1 Advanced / Rush / Wave):**
  * **Schwalbenschwanz-Führung (*Dovetail Slide*):** Das Gerät wird von oben auf die $72\,\text{mm}$ lange Führungsschiene aufgeschoben.
  * **Rastzahn & Gummilasche:** Ein federnder Rastzahn klinkt unten ein; die EPDM-Spannlasche sichert das Gerät zusätzlich gegen Vibrationen.
* **Für Midland XT-Serie & Bare-Board PMR446 (XT10 / XT30 / G5 entkernt):**
  * **4-Punkt-Silikondämpfung & Konturbett:** Das entkernte Board ($\approx 68 \times 42 \times 10\,\text{mm}$) liegt passgenau in einem gefrästen/gedruckten Konturnest auf 4 Silikonzapfen und wird von 2x M2 Schrauben sowie der Gummilasche vibrationsfrei fixiert.
  * **Integrierte Antenne / SMA-Port:** $32\,\text{mm}$ Helical-Wendelspule im Schlitten oder SMA-Buchse an der Blende. Direct-Wire Lötung oder JST-Verbinder auf die Kassettenplatine.

---

### 5.4 Einschraubbare Schutz-Schottwand mit integriertem Feder-Auswurf (Auto-Eject)
* **Mechanischer Berührungsschutz:** Nach dem Einsetzen der Pod-Base-Platine und dem Anziehen der M8-Rändelmutter wird eine **$2{,}0\,\text{mm}$ starke PA12-Schutz-Schottwand** mit zwei M2-Senkkopfschrauben fest mit dem Gehäuse verschraubt.
* **Vollständige Kapselung:** Die Schottwand riegelt die Platinenkammer der Pod-Basis (M8-Lötstellen, Littelfuse SP3012 TVS-Array, SMD-Filter) hermetisch gegen den Wechselschacht ab. Beim Hineinschieben oder Herausziehen der Kassette können weder Bauteile noch Leiterbahnen berührt, zerkratzt oder beschädigt werden.
* **Integrierter Schutzkragen:** Die Schottwand trägt den zentrischen PA12-Schutzkragen mit $45^\circ$-Fangtrichter, in dem die 6-Pin Präzisions-Stiftleiste sicher geschützt liegt.
* **Federgestützter Push-Out / Auto-Eject Mechanismus:**
  * Links und rechts neben dem Schutzkragen sitzen in der Schottwand **zwei federbelastete Auswerfer-Druckfedern (V4A Edelstahl 1.4310)** mit Führungsstiften.
  * **Beim Einschieben:** Die Stirnseite des Kassetten-Schlittens drückt die Federn um $5\dots 6\,\text{mm}$ zusammen, bis die 6-Pin Buchse voll im Schutzkragen sitzt und die Snap-Fit Rastnasen mit einem satten Klick einrasten. Die komprimierten Federn halten das System unter permanenter Vorspannung gegen die Silikondichtung – **100 % spielfrei und vibrationsfest**.
  * **Beim Entriegeln (Auto-Eject):** Sobald der Fahrer die beiden seitlichen Schnellentriegelungstaster an der Blende zusammendrückt, lösen sich die Rastnasen und **die Federn werfen die Kassette automatisch um $8\dots 10\,\text{mm}$ nach außen aus**.
  * Der Steckkontakt ist damit sauber getrennt und die Kassette lässt sich selbst mit dicken Motorrad-Winterhandschuhen mühelos und ohne Verkanten greifen und herausziehen.

---

### 5.5 Mittige Pod-Druckausgleichsmembran (ePTFE auf der Gehäuse-Oberseite)
* **Problemstellung:** Interne Abwärme (SX1262 LoRa $+22\,\text{dBm}$ PA, Ladeschaltung) und Sonneneinstrahlung erzeugen Druckdifferenzen im kleinen Pod-Volumen.
* **Positionierung:** Zentral auf der **langen Gehäuse-Oberseite** ($X = 0{,}0\,\text{mm}, Y = 0{,}0\,\text{mm}$) sitzt eine in eine Schutzsenkung integrierte **$\varnothing\,7{,}0\,\text{mm}$ ePTFE-Druckausgleichsmembran** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Funktion:** Belüftungsrate $> 25\,\text{ml/min}$ bei 70 mbar, Wassereintrittspunkt $> 1{,}5\,\text{bar}$ (IP67). Verhindert Vakuum-Wassersaugen bei Abkühlung durch Regengüsse und gleicht thermische Druckschwankungen im gesamten Pod-Innenraum symmetrisch aus.

---

### 5.6 Monolithisches Wärmemanagement: Seitliche Kühl-Gleitschienen & Kupfer-Gleitkontakte

Um die Wärmeübertragungsfläche drastisch zu vergrößern und gleichzeitig den mechanischen Verschleiß der 3D-Druck-Führungsnuten auf Null zu reduzieren, kombiniert das System ein **seitliches metallisches Kühl- und Führungsschienen-System (*Lateral Thermal Slide Rails*)**:

```
                    HERAUSNEHMBARER KASSETTEN-SCHLITTEN (PA12)
 ┌───────────────────────────────────────────────────────────────────────────┐
 │   PLATINE / HEADSET-AKKU (Ladeverluste 5V, SX1262 LoRa PA, ESP32)        │
 ├───────────────────────────────────────────────────────────────────────────┤
 │   FLEXIBLES SILIKON-GAP-PAD (Shore 00 35, 1.5 mm, λ = 3.0 W/m·K)          │ ◄── Schwingungsdämpfung & Heat-Flow
 ├─────────────────────────┬───────────────────────┬─────────────────────────┤
 │ KASSETTEN-FLANKENBLECH  │                       │ KASSETTEN-FLANKENBLECH  │ ◄── 0.8 mm Kupfer/Alu-Federblech
 └────────────┬────────────┴───────────────────────┴────────────┬────────────┘     (75 x 14 mm = 1050 mm² Fläche)
              │                                                 │
              ▼ (Großflächiger metallischer Gleitkontakt)       ▼
 ┌────────────┴────────────┬───────────────────────┬────────────┴────────────┐
 │ POD-KÜHL-FÜHRUNGSSCHIENE│                       │ POD-KÜHL-FÜHRUNGSSCHIENE│ ◄── In Pod-Seitenwand eingelassen
 ├─────────────────────────┴───────────────────────┴─────────────────────────┤
 │                  MONOCOQUE-POD-AUSSENGEHÄUSE (PA12)                       │
 └─────────────────────────┬───────────────────────┬─────────────────────────┘
                           │                       │
                           ▼                       ▼
              ═══════════════════════════════════════════════════
                 DIREKTER FAHRTWIND AN DER GEHÄUSE-AUSSENSEITE
              ═══════════════════════════════════════════════════
```

#### Konstruktive Vorteile der seitlichen Kühl- und Gleitschiene:

1. **Riesige Wärmeübertragungsfläche ($> 1.050\,\text{mm}^2$ pro Flanke):**
   * Statt nur punktueller kleiner Bolzen schiebt sich das $75 \times 14\,\text{mm}$ große **Kupfer-/Aluminium-Flankenblech** des Schlittens vollflächig in die korrespondierende Kühl-Gleitschiene der Pod-Seitenwand.
   * Der thermische Widerstand sinkt um mehr als das 5-Fache gegenüber reinen Punktkontakten.
2. **Verschleißfreie Metall-auf-Metall Führung:**
   * Bei wiederholtem Kassettenwechsel (Sena $\leftrightarrow$ Cardo $\leftrightarrow$ OMM) reibt kein 3D-Druck-Kunststoff auf Kunststoff. Die beiden metallischen Führungsschienen gleiten satt, präzise und dauerhaft spielfrei.
3. **Leichte Federvorspannung für satten Kontakt:**
   * Das Flankenblech an der Kassettenwange ist mit einer minimalen konvexen Wölbung ($0{,}3\,\text{mm}$ Federweg) ausgeführt und wird von innen durch das elastische Silikon-Wärmeleitpad gestützt. Beim Einschieben presst es sich mit konstantem Anpressdruck an die Pod-Schiene.
4. **Fahrtwind-Anbindung an der Pod-Außenseite:**
   * Die Pod-Kühlschiene ist an der Außenseite der Pod-Flanke dezent in den Strömungsbereich geführt (oder thermisch an den M5-Montagehalter angebunden) und gibt die Wärme direkt an den Fahrtwind ab.
5. **100 % Funk-Neutralität:**
   * Da die Schienen rein seitlich und unterhalb des oberen $180^\circ$-Halbraums liegen, bleibt das Antennenfeld für GNSS, LoRa und Wi-Fi nach oben und horizontal völlig frei. Gleichzeitig schirmen die Seitenbleche die Audio- und Digital-Signale gegen seitliche Zünd- und Generator-Störfelder ab.

---

### 5.7 IP67 Blind- / Leerkassette (Dummy Cartridge)
* **Verwendung bei Teilbestückung:** Wird ein Pod-Schacht temporär nicht bestückt (z. B. wenn nur Sena genutzt wird oder ein Pod stillgelegt ist), verschließt die formidentische **IP67-Leerkassette (`Pod_Dummy_Cartridge_IP67.stl`)** den Schacht vollständig.
* **Dichtungskonzept:** Stirnseitige Silikon-Umlaufdichtung schützt die innenliegenden Kontakte vor Schmutz, Spritzwasser und Streusalz.
* **Verriegelung:** Nutzt denselben dualen Snap-Fit Klick-Verschluss wie aktive Einschubschlitten.
* **Hardware-Zustand:** Die Zentralbox erkennt offene/leere Kontakte und hält den Slot über `disabled.json` strom- und rauschfrei isoliert.

---

### 5.8 Pod-Basisplatine (`openmotorbridge_pod_base`) & Zentrische Kassetten-Führung

Der mechanische und elektrische Übergang von der Wechselkassette auf die M8-Kabelverbindung zum Motorradkabelbaum erfolgt über die zentrierte **Pod-Basisplatine (`openmotorbridge_pod_base`)**:

#### Oberansicht (Senkrechte/Horizontale 6-Pin Stiftleiste & SP3012 TVS-Schutzstufe):
![OpenMotorBridge Pod-Basisplatine Oberansicht 3D-Render](../../hardware/kicad_pod_base/pod_base_3d_render_top.png)

#### Unteransicht (Zentrierte M8 6-Pin IP67-Buchse & GND-Schirmfläche):
![OpenMotorBridge Pod-Basisplatine Unteransicht 3D-Render](../../hardware/kicad_pod_base/pod_base_3d_render_bottom.png)

* **Abmessungen:** $48{,}0 \times 24{,}0\,\text{mm}$ (Kompakte 2-Layer FR4-Basisplatine mit großzügigen Leiterbahn- und Schutzabständen).
* **Zentrierte 6-Pin Stiftleiste (`J1`) mit PA12-Schutzkragen:** 6-poliges Präzisions-Pin-Array ($2{,}54\,\text{mm}$ Raster, vergoldet) exakt auf der horizontalen Mittelachse ($Y=0, Z=0$).
* **Integrierte PA12-Schutzwandung & Fangtrichter:** Die Schottwand bildet um die Stiftleiste `J1` eine **4-seitige, $1{,}2\,\text{mm}$ starke Schutzwand mit $45^\circ$-Einlaufschrägen**. Die Buchsenleiste der Wechselkassette gleitet formschlüssig und saugend wie ein Kolben in diese Wanne ein – die Stifte sind fingersicher gekapselt und können niemals verbogen oder verkantet werden.
* **Integrierte ESD-Schutzmatrix (`U1`):** **Littelfuse SP3012-06UTG** (6-Kanal TVS-Array mit $< 0{,}5\,\text{pF}$ parasitärer Kapazität) leitet elektrostatische Entladungen beim Berühren der Kontakte blitzschnell gegen Masse ab.
* **Zentrierte M8-Rundsteckverbinder-Buchse (`J2`):** Metallgekapselte **M8 6-Pin A-Coded IP67 Einbaubuchse** (IEC 61076-2-104) mit massivem Montagesockel und Gewindekragen exakt im geometrischen Zentrum der Platinenunterseite (`B.Cu`) verlötet.
* **Mechanische Entkopplung & Montage (`H1`, `H2`):** 2x M2 Montagebohrungen mit Shore 40A Silikondämpfung gegen Fahrbahnvibrationen. Steckkräfte werden zu 100% vom Gehäuseendanschlag aufgenommen.

---

### 5.8 Zentrischer Kassetteneinschub & Poka-Yoke Führungskonzept

Um Verkanten, schiefe Krafteinleitung und fehlerhaftes Einstecken physikalisch auszuschließen, ist der Kassetteneinschub **in allen Raumachsen exakt zentriert**:

```
                  ◄──────────── 64.0 mm Pod-Breite ────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                    3.0 mm Gehäuse-Deckel                    │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 32.0 mm
 │ │   │                                                 │   │ │ │ Pod-
 │ │3.0│         ZENTRISCHER KASSETTEN-EINSCHUB          │3.0│ │ │ Höhe
 │ │mm │                 (56 x 24 mm)                    │mm │ │ │
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
   * **Breite ($Y$):** Bei $64{,}0\,\text{mm}$ Pod-Außenbreite und $56{,}0\,\text{mm}$ Schachtbreite ergeben sich beidseitig symmetrische **$3{,}0\,\text{mm}$ Wandstärken**.
   * **Höhe ($Z$):** Bei $32{,}0\,\text{mm}$ Pod-Außenhöhe und $24{,}0\,\text{mm}$ Schachthöhe ergeben sich symmetrische **$3{,}0\,\text{mm}$ Decken- und Bodenstärken**.
   * Die Steckverbindung liegt exakt im Schnittpunkt der Symmetrieachsen $\rightarrow$ **Null Hebelwirkung oder Kippmomente**.
2. **Poka-Yoke Verpolschutz (Asymmetrische Führungsnuten):**
   * Linke Führungsnut: $1{,}5\,\text{mm}$ Breite.
   * Rechte Führungsnut: $2{,}0\,\text{mm}$ Breite.
   * Ein verkehrtes (über Kopf) Einschieben der Kassette ist mechanisch unmöglich.
3. **$45^\circ$-Zentriertrichter am Kassettenkopf:**
   * Die Kassettennase besitzt um den Steckerausschnitt eine umlaufende $45^\circ$-Einführschräge mit $\pm 1{,}5\,\text{mm}$ Fangbereich. Die Kontakte werden vor dem elektrischen Schluss perfekt zentriert.
4. **Formschlüssiger Endanschlag & Auto-Eject:**
   * Die Einschubkraft wird direkt von der massiven Schottwand (PA12) abgefangen – die Platinen-Lötstellen bleiben zu 100 % kräftefrei. Die beiden V4A-Edelstahlfedern halten das System permanent unter Vorspannung und werfen den Schlitten beim Entriegeln um $10\,\text{mm}$ aus.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              SCHNITTSTELLEN-ÜBERGANG POD-BASIS & KASSETTE               │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. DOCKING-AUFNAHME KASSETTEN-SCHLITTEN:                                │
│    • Original-Headset (Sena 50S/60S / Cardo Edge) werkzeuglos eingeklinkt│
│    • Internes JST-SH 6P Flachbandkabel zur Kassetten-Trägerplatine       │
│                               ▼                                         │
│ 2. KASSETTEN-TRÄGERPLATINE (openmotorbridge_pod_cartridge, 60x36mm):    │
│    • DS2401 1-Wire ID ROM (Meldet Headset-Typ an ESP32)                 │
│    • 500mA PTC-Sicherung + grüne 5V Power-Status-LED                    │
│    • 6-Pin Präzisionsbuchsenleiste (zentriert am Schlittenkopf)         │
│                               ▼ (Horizontaler Kassetteneinschub)        │
│ 3. POD-BASISPLATINE (openmotorbridge_pod_base, 48x24mm):                │
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

### 5.9 3D-Röntgen-Architektur (X-Ray CAD) & Baugruppen-Explosionsansicht

Zur ganzheitlichen Verifikation der Passungen, Dichtebenen und elektrischen Übergänge wurde die mechanische Gesamtanordnung des **Satelliten-Pods** und der **Wechselkassette** in einer transluzenten Röntgen-Darstellung (*Ghosted X-Ray*) sowie einer Explosionsansicht modelliert:

#### Transluzente 3D-Röntgenansicht (120 x 64 x 32 mm, Generic Max Envelope):
![OpenMotorBridge 3D X-Ray CAD Architektur](../../hardware/cad/openmotorbridge_pod_assembly_render_xray.png)

#### Baugruppen-Explosionsdarstellung (Hierarchie entlang der Einschubachse):
![OpenMotorBridge 3D Explosionsansicht](../../hardware/cad/openmotorbridge_pod_exploded_view.png)

#### Mechanische Spezifikationen & Passungen:
* **Pod-Außengehäuse:** Makrolon 2805 Polycarbonat / PA12 MJF ($120{,}0 \times 64{,}0 \times 32{,}0\,\text{mm}$, Schacht-Innenmaß $96{,}0 \times 56{,}0 \times 24{,}0\,\text{mm}$).
* **Pod-Basisplatine (`openmotorbridge_pod_base`):** $48{,}0 \times 24{,}0 \times 1{,}6\,\text{mm}$ Adapterplatine mit zentrierter M8 6-Pin IP67 Vollmetallbuchse (B.Cu) und senkrechter 6-Pin Stiftleiste (F.Cu).
* **Einschraubbare Schottwand:** $56{,}0 \times 24{,}0 \times 2{,}0\,\text{mm}$ PA12 mit 2x M2 Senkkopfschrauben, Schutzkragen und 2x Edelstahl-Auswerferfedern ($10\,\text{mm}$ Auswurfhub).
* **Offener Kassetten-Schlitten:** $92{,}0 \times 54{,}0 \times 23{,}5\,\text{mm}$ U-Chassis ohne Deckel ($88{,}0 \times 50{,}0 \times 23{,}5\,\text{mm}$ nutzbarer Innenbauraum).
* **Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`):** $60{,}0 \times 36{,}0 \times 1{,}2\,\text{mm}$ FR4-Adapter mit DS2401 1-Wire ID, abgewinkeltem JST-SH 1.0mm 6P Flex-Verbinder (F.Cu) und 6-Pin Buchsenleiste (B.Cu).
* **IP67-Dichtebene:** Der umlaufende $58{,}0 \times 28{,}0\,\text{mm}$ Shore 40A Silikon-Stirnflansch wird beim Einschieben um $0{,}8\,\text{mm}$ vorkomprimiert und dichtet die Kassettenkammer hermetisch gegen Strahlwasser und Staub ab.

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


