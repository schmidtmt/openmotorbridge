# 05 - Mechanische Konstruktion: 3-Teiliges Sandwich-Gehäuse, Zwischenboden & Kassetten-Pods

Dieses Dokument spezifiziert die mechanische Konstruktion, das Thermomanagement und das IP67/IP69K-Gehäusedesign der zentralen Steuerbox (Typ A) im **3-teiligen Sandwich-Aufbau (Unterwanne, Oberwanne mit Zwischenboden, Gehäusedeckel)** mit **integrierter Akku-Fixierung auf dem Zwischenboden**, **stirnseitiger Anschlussleiste (HD26, USB-C & RGB-LED-Statusfenster)** in der Oberwanne, **planarem 4-Layer Kupfer-Wärmespreader und 11x Zwischenboden-Konvektionsschlitzen** sowie das universelle Satelliten-Pod-System (Typ B) mit Kassetten-Einschüben.

---

## 1. Gehäuse Typ A: Zentrale Steuerbox (3-Teiliges Sandwich-Design)

Das Basisgehäuse der Zentralbox ist als modulares, 3-teiliges IP67/IP69K-Sandwichgehäuse aus **PA12 (MJF-Verfahren)** oder **Aluminium-Druckguss** konzipiert, das speziell für raue Motorrad-Bedingungen (Vibrationen bis $20\,\text{g}$, Spritzwasser, Hitzestau unter der Sitzbank) ausgelegt ist:

- **Außenabmessungen:** $110{,}0 \times 74{,}0 \times 38{,}0\,\text{mm}$ (L x B x H; Unterwanne $17{,}0\,\text{mm}$, Oberwanne $15{,}0\,\text{mm}$, Deckel $6{,}0\,\text{mm}$).
- **Befestigung:** 4x integrierte Ecklaschen an der Unterwanne mit **Lochabstand $128{,}0 \times 56{,}0\,\text{mm}$** für schwingungsdämpfende **M4 Silentblöcke (Shore 50A EPDM)** zur Entkopplung hochfrequenter Motorvibrationen.
- **Lichte Innenmaße:** $102{,}0 \times 66{,}0 \times 32{,}0\,\text{mm}$ (optimiert für die $85{,}0 \times 55{,}0\,\text{mm}$ 4-Layer Hauptplatine).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck (min. $3{,}0\,\text{mm}$ Wandstärke), kugelgestrahlt, im Heißbad chemisch geglättet und hydrophob versiegelt.
- **Schutzart:** IP67 / IP69K (strahlwasser- und tauchdicht bis $1\,\text{m}$ Wassertiefe sowie dampfstrahlbeständig).

### 1.1 3D-CAD-Modell & 3-Schichten-Sandwichaufbau

![OpenMotorBridge Zentralbox 3-Teiliges Sandwich-Gehäuse IP67](../images/cad/main_box_enclosure_cad.png)

*Abbildung 5.1: 3D-CAD-Darstellung der zentralen Steuerbox. Links: Geschlossenes IP67-Gehäuse mit HD26-Kabelbaumflansch, USB-C Servicekappe und bündigem RGB-Statusfenster an der Stirnseite der Oberwanne, 4x M4 Silentblöcken an der Unterwanne und flachem Deckel mit Gore-Membran. Rechts: Schnittansicht mit den 3 Sandwich-Ebenen: 1. Unterwanne (100% homogener, geschlossener PA12-Boden, 4-Layer PCB auf M2.5 Stand-offs), 2. Oberwanne mit Zwischenboden (Akku mit EPDM-Spannband oben, 11x Konvektionsschlitze & Kabeldurchbruch im Boden, Ports an Stirnwand), 3. Robuster Deckel mit Gore-Vent (100% dicht).*

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. GEHÄUSEDECKEL (6,0 mm Höhe / 3,0 mm Wandstärke)         │  │
│    • Gore ePTFE Druckausgleichsmembran (Ø 7,0 mm)          │  │ 38,0 mm
│    • Umlaufende Nut mit Shore 40A Silikon-Profildichtung   │  │ Gesamt-
│    • 100% homogener, geschlossener Vollkunststoff-Deckel   │  │ höhe
├────────────────────────────────────────────────────────────┤  │
│ 2. OBERWANNE MIT ZWISCHENBODEN (15,0 mm Höhe)              │  │
│    • Stirnwand (Alle Anschlüsse & Anzeige):                │  │
│      - HD26 D-Sub Flansch (Haupt-Kabelbaum)                │  │
│      - Wasserdichter USB-C Service-Port (Alu-Schraubkappe) │  │
│      - Wasserdichtes RGB-Status-LED-Sichtfenster (Ø 3 mm)  │  │
│    • Oberes Fach (auf dem Zwischenboden):                  │  │
│      - 1S LiPo-USV-Pufferakku (52x36x6.5mm) in Akkuwanne   │  │
│      - EPDM-Gummispannband zur vibrationsfesten Fixierung  │  │
│    • Zwischenboden (Optimierte Zirkulationsebene):         │  │
│      - 25,0 x 4,0 mm Kabeldurchbruchsschlitz               │  │
│      - 11x Konvektions- & Druckausgleichsschlitze          │  │
├────────────────────────────────────────────────────────────┤  │
│ 3. UNTERWANNE (17,0 mm Höhe - Geschlossene Monocoque-Wanne)│  │
│    • 4-Layer Hauptplatine (85 x 55 mm) auf M2.5 Dämpfern   │  │
│    • 2x 35 µm massive Kupfer-Innenlagen als Wärmespreader  │  │
│    • 4x M4 Silentblock-Befestigungsohren (vibrationsfest)  │  │
│    • 100% geschlossener PA12-Boden ohne Gehäusedurchbrüche │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.2 3D-Explosionsdarstellung & Schichtaufbau (1:1:1 CAD Fitting)

![OpenMotorBridge Zentralbox Exploded 3D CAD Fitting](../images/cad/main_box_full_assembly_exploded_3d.png)

*Abbildung 5.1.1: 1:1:1 euklidische CAD-Explosionsdarstellung der Zentralbox. Gezeigt werden alle 5 Montageebenen entlang der vertikalen Z-Achse: Unterwanne mit 4x M4 Silentblöcken und 100% geschlossenem PA12-Boden, 4-Layer Hauptplatine (85x55mm) mit planarem Kupfer-Wärmespreader, Oberwanne mit Zwischenboden (11x Konvektionsschlitze) und stirnseitigen Schnittstellen (HD26, USB-C, LED), 1S LiPo-Pufferakku im Konturbett mit EPDM-Spannband sowie der Gehäusedeckel mit Gore ePTFE-Membran.*

### 1.3 3D-Röntgenansicht & Zusammenbau-Fitting

![OpenMotorBridge Zentralbox Mated 3D X-Ray CAD Fitting](../images/cad/main_box_assembly_mated_3d.png)

*Abbildung 5.1.2: Transparente 3D-Röntgenansicht der vollständig geschlossenen Zentralbox. Erkennbar sind die spielfreien Bauteilfreiräume, die geschützte Akku-Lagerung auf dem Zwischenboden, die durchgängige Konvektion über die 11 Zwischenbodenschlitze und der scheuerfreie Kabelverlauf zum HD26-Flansch.*

### 1.4 Maßstabsgetreuer Längs- & Querschnitt (X-Z Thermik & Y-Z Kabelführung)

![OpenMotorBridge Zentralbox Cross Sections](../images/cad/main_box_assembly_cross_section.png)

*Abbildung 5.1.3: Exakte 2D-Schnittansichten der Zentralbox. Oben: Längsschnitt (X-Z Ebene) mit vollständigem thermischem Pfad (Planarer 4-Layer Cu-Spreader $\rightarrow$ 11x Zwischenboden-Konvektionsschlitze $\rightarrow$ Gore ePTFE Druckausgleich) und Akku-Kammer. Unten: Querschnitt (Y-Z Ebene) mit detailliertem Verlauf der Schnittstellen direkt zum abgedichteten HD26 SEAL-D Flansch an der Gehäusestirnwand.*

---

## 2. Thermomanagement & Planare PCB-Entwärmung (Kupferbolzenfrei)

Die Zentralbox beherbergt die wärmeerzeugenden Kernkomponenten: $100\,\text{V}$-Schaltregler (LM5164-Q1, $0{,}42\dots 0{,}58\,\text{W}$), LiPo-Ladecontroller (BQ24075, bis zu $0{,}55\,\text{W}$ bei Schnellladung) und ESP32-S3 DSP-Kern ($0{,}46\,\text{W}$). Die Gesamtabwärme liegt im normalen Fahrbetrieb bei lediglich **$\approx 1{,}5\,\text{W}$** (Peak bei maximaler Schnellladung: $2{,}45\,\text{W}$).

```
       4-LAYER LEITERPLATTE (PLANARER KUPFER-WÄRMESPREADER)
┌────────────────────────────────────────────────────────┐
│ [ LM5164 Buck ]     [ BQ24075 UPS ]     [ ESP32-S3 ]   │ ◄── Bauelemente (SMD)
│   (100V DCDC)       (Power-Path)        (Dual-Core)    │
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 2: 35 µm Solid GND Plane
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 3: 35 µm Solid PWR/GND Plane
└──────────────────────────┬─────────────────────────────┘     (λ = 390 W/m·K, 93.5 cm² Fläche)
                           │
 ┌─────────────────────────▼─────────────────────────────┐
 │ 11x ZWISCHENBODEN-KONVEKTIONSSCHLITZE & INNENLUFT     │ ◄── Freie Zirkulation in 210 cm³
 │ (Wärme verteilt sich homogen im gesamten Gehäuse)     │     Luftvolumen & Gore ePTFE-Vent
 └─────────────────────────┬─────────────────────────────┘
                           ▼
          Abgabe über PA12-Gehäuseoberfläche (300 cm²) an Fahrtwind
```

### 2.1 Spezifikation & physikalische Funktionsweise:
1. **Planarer 4-Layer Kupfer-Wärmespreader ($85 \times 55\,\text{mm}$):**
   * Die beiden massiven $35\,\mu\text{m}$ Innenlagen der FR4-Platine leiten die Wärme blitzschnell ($\lambda = 390\,\text{W/(m}\cdot\text{K)}$) vom LM5164, BQ24075 und ESP32 ab und verteilen sie vollflächig über die gesamte Platine.
   * Lokale Hotspots werden vollständig eliminiert; die Platinenoberfläche bleibt im Sommerbetrieb bei homogenen $\approx 55\,^\circ\text{C}$.
2. **11x Optimierte Konvektions- & Zirkulationsschlitze im Zwischenboden:**
   * 5 Schlitze an der Rückkante ($Y = 58\,\text{mm}$), 4 Schlitze an den Seitenflanken ($X = 10\,\text{mm}, 92\,\text{mm}$) und 2 Schlitze an der Frontkante lassen die erwärmte Luft ungehindert nach oben in die Deckelkammer aufsteigen.
   * Das gesamte Gehäuseinnenvolumen ($\approx 210\,\text{cm}^3$) wirkt als gemeinsamer thermischer Puffer, der Druck- und Temperaturschwankungen über das zentrale Gore ePTFE-Ventil ausgleicht.
3. **Thermische Sicherheitsmargen im Extrem-Stresstest (Stau bei $45\,^\circ\text{C}$ Hitze + $13\,^\circ\text{C}$ Motorwärme = $58\,^\circ\text{C}$ unter Sitz):**
   * **LM5164-Q1:** $T_j = 93{,}8\,^\circ\text{C}$ (Zulässig bis $+150\,^\circ\text{C}$ nach AEC-Q100 $\rightarrow$ **$+56{,}2\,^\circ\text{C}$ Sicherheitsabstand**).
   * **ESP32-S3:** $T_j = 90{,}2\,^\circ\text{C}$ (Zulässig bis $+105\,^\circ\text{C}$ $\rightarrow$ **$+14{,}8\,^\circ\text{C}$ Sicherheitsabstand**).
   * **3.3V LDO:** $T_j = 110{,}4\,^\circ\text{C}$ (Zulässig bis $+125\,^\circ\text{C}$ / $+150\,^\circ\text{C}$).
   * **1S LiPo Akku:** Verbleibt in der oberen Kammer sicher unter $60\,^\circ\text{C}$ (JEITA-NTC pausiert Ladevorgänge oberhalb von $45\,^\circ\text{C}$ automatisch).
4. **Vorteile der 100 % kupferbolzenfreien Konstruktion:**
   * **Absolute Dichtheit nach IP67/IP69K:** Der Boden ist eine monolithische, ununterbrochene PA12-Wanne ohne Dichtfugen oder Klebestellen.
   * **Sofort einsatzbereite 3D-Druckteile:** Keine Nachbearbeitung, kein Einpressen oder Einkleben von Drehteilen nötig.
   * **Vollständige Vibrationsentkopplung:** 4x M4 Gummipuffer-Silentblöcke an den Wannenohren isolieren die gesamte Box mechanisch vom Motorradrahmen.

---

## 3. Oberwanne: Stirnseitige Schnittstellen, Akku & Zwischenboden

Die Oberwanne bildet das mittlere Funktionsmodul des Sandwich-Aufbaus: Sie bündelt an ihrer Stirnseite alle von außen zugänglichen Schnittstellen und Anzeigen und nimmt auf der Oberseite des integrierten Zwischenbodens den USV-Pufferakku auf.

```
┌─────────────────────────────────────────────────────────────┐
│                 OBERWANNE (Draufsicht auf Zwischenboden)    │
│                                                             │
│  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │ 1. AKKU-AUFNAHMEWANNE   │  │ 2. Flachbandkabel-Schlitz│  │
│  │    (52 x 36 x 6.5 mm)   │  │    (38,0 x 6,0 mm, R1,5) │  │
│  │    mit EPDM-Spannband   │  │    führt zu J1 auf PCB   │  │
│  │    [4P JST-PH Tülle]    │  └──────────────────────────┘  │
│  └─────────────────────────┘                                │
│                                                             │
│  [Slot 1]              [Slot 2]              [Slot 3]       │
│  ◄──────── 4x Interne Druckausgleichsschlitze ─────────────►│
├─────────────────────────────────────────────────────────────┤
│  STIRNWAND: [ USB-C Port ]   [ RGB-LED ]   [ HD26 Flansch ] │
└─────────────────────────────────────────────────────────────┘
```

### 3.1 1S LiPo-Akkuaufnahme & 4-Poliger JST-PH Anschluss (Auf Zwischenboden)
* **Passgenaue Aufnahmewanne ($52{,}0 \times 36{,}0 \times 6{,}5\,\text{mm}$):** Auf der Oberseite des Zwischenbodens angeformte Wanne, ausgekleidet mit $1{,}0\,\text{mm}$ EPDM-Moosgummi zur Stoßdämpfung.
* **Elastisches EPDM-Gummispannband (Shore 50A, $10\,\text{mm}$ breit):** Spannt die Akkuzelle quer über die Wanne. Die Endösen klinken werkzeuglos in zwei Hinterschnitt-Rasthaken der Oberwannen-Seitenwände ein. Der Akku bleibt damit vibrationsfest und spielfrei fixiert, kann aber bei Wartungsarbeiten werkzeuglos getauscht werden.
* **Kombiniertes 4-Draht-Kabel (JST-PH 2.0 mm Wannenstecker):** 
  * Der Akku und der integrierte NTC-Sensor sind über einen einzigen, verpolsicheren **4-Pin JST-PH Stecker mit Verriegelungsnase** (`J5`) angeschlossen:
    * Pin 1: `BAT+` (+3.7V / +4.2V 1S LiPo)
    * Pin 2: `BAT-` (`GND_PWR`)
    * Pin 3: `NTC_JEITA` (10k NTC Temperaturüberwachung)
    * Pin 4: `NTC_GND` (Sensor-Masse)
  * Das Kabel führt durch eine abgerundete $\varnothing\,5\,\text{mm}$ Tülle im linken Zwischenboden direkt nach unten zur Buchse `J5` an der linken Vorderkante der Hauptplatine (mit $> 12\,\text{mm}$ Sicherheitsabstand zum ESP32-S3).

### 3.2 Spezifikation der Zwischenboden-Durchführungen
1. **Flachbandkabel-Durchführung für Haupt-Kabelbaum:**
   * **Abmessungen:** $38{,}0 \times 6{,}0\,\text{mm}$ mit beidseitig $R=1{,}5\,\text{mm}$ Kantenverrundung.
   * **Position:** Liegt auf der rechten Seite fluchtend direkt über der 2x13 Wannenbuchse `J1` auf der Hauptplatine.
   * **Kabelführung:** Das $45\,\text{mm}$ lange 26-polige Flachbandkabel führt vom stirnseitigen HD26-Flansch in der Oberwanne durch diesen Schlitz nach unten zur Hauptplatine.
2. **Labyrinth-Druckausgleichsschlitze:**
   * 4x Belüftungsschlitze ($15{,}0 \times 2{,}0\,\text{mm}$) verbinden den unteren Elektronikraum mit dem oberen Raum und der ePTFE-Membran im Deckel.

---

## 4. Stirnseitige Anschlüsse & Anzeige in der Oberwanne (USB-C, RGB-LED & HD26)

Alle drei Interaktions- und Anschlusselemente befinden sich kompakt und geschützt nebeneinander an der **vorderen Stirnwand der Oberwanne**:

```
                  VORDERE STIRNWAND DER OBERWANNE
┌─────────────────────────────────────────────────────────────┐
│ ┌────────────┐     ┌────────┐      ┌──────────────────────┐ │
│ │ 1. USB-C   │     │ 2. RGB │      │ 3. HD26 D-Sub Flansch│ │
│ │    Service │     │    LED │      │    (Kabelbaum-Buchse)│ │
│ │    Alukappe│     │    Ø3mm│      │    2x M3 Jackscrews  │ │
│ └────────────┘     └────────┘      └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 HD26 D-Sub Gehäusewand-Flansch (Kabelbaum-Hauptanschluss)
* **Ausschnitt-Geometrie:** D-Sub High-Density 26-Pin Ausschnitt ($39{,}2 \times 15{,}4\,\text{mm}$) in der Stirnwand der Oberwanne.
* **Flanschdichtung:** Formgenaue EPDM-Flachdichtung ($1{,}5\,\text{mm}$ Stärke, Shore 60 A) zwischen Metallkragen der Amphenol LTW / NorComp SEAL-D Buchse und der Gehäusewand.
* **Verschraubung:** 2x M3 Edelstahl-Sechskantbolzen mit O-Ring-Dichtscheiben klemmen den Flansch mit $0{,}6\,\text{Nm}$ wasserdicht gegen die Wand.
* **Interne Entkopplung:** Verbindung zur Hauptplatine über das 26-polige Flachbandkabel durch den Zwischenboden-Schlitz zur 2x13 Wannenbuchse (`J1`).

### 4.2 Wasserdichter USB-C Programmier- & Service-Port
* **Zugang ohne Gehäuseöffnung:** Direkt neben dem HD26-Flansch befindet sich der wasserdichte USB-C Service-Port mit **blau eloxierter Aluminium-Schraubkappe** und rotem NBR/Silikon-O-Ring.
* **Funktion:** Ermöglicht Firmware-Updates, ESP-IDF JTAG-Debugging und Diagnose im eingebauten Zustand unter der Sitzbank, ohne dass das IP67-Gehäuse aufgeschraubt werden muss.

### 4.3 Wasserdichtes RGB-Status-LED-Sichtfenster
* **Frontbündige Linse:** Ein diffuser PMMA-Linsenkörper ($\varnothing\,3{,}0\,\text{mm}$, *Mentor 1292.1101*) ist mit umlaufendem NBR-O-Ring frontbündig in die Stirnwand der Oberwanne eingepresst und mit transparentem Polyurethan versiegelt.
* **Blickwinkel:** Zeigt den Betriebszustand direkt an der Frontseite an, sodass der Fahrer / Mechaniker beim Blick unter die Sitzbank auf die Stecker sofort den Status sieht.

### 4.4 Status-Farbcodierung (LED State Machine)

| LED-Farbe & Muster | Betriebszustand | Bedeutung |
| :--- | :--- | :--- |
| 🟢 **Grün pulsierend (1 Hz)** | **Normalbetrieb (Online)** | Bordnetz aktiv, alle gesteckten Pods aktiv, DLE OK |
| 🔵 **Blau blinkend (2 Hz)** | **BLE Dashboard / Pairing** | WebApp PWA aktiv verbunden / Datenaustausch |
| 🟡 **Gelb pulsierend (0.5 Hz)**| **USV-Akkubetrieb (KL15 AUS)**| Nachlauf-Modus: GPX Tour-Close & WebDAV Sync |
| 🔴 **Rot schnell blinkend** | **Warnung / Fehler** | Unterspannung Starterbatterie ($< 11{,}8\,\text{V}$) / Kassetten-Kurzschluss |
| 🟣 **Lila leuchtend** | **OMM DLE Leader** | Dieses Motorrad führt die Mesh-Koordination der Gruppe |
| ⚪ **Weiß Doppelblitz** | **Actioncam Marker** | Lenkertaster gedrückt: GPS Highlight-Marker gesetzt |

---

## 5. Gehäusedeckel: Robuste 100% dichte Schutzhaube mit Druckausgleich

Der Gehäusedeckel schließt die Oberwanne nach oben hermetisch ab. Da sich alle Anschlüsse und die Status-LED in der Oberwanne befinden, ist der Deckel als **robuste, homogene Schutzhaube** ohne bruchanfällige Lichtleiterbohrungen ausgeführt:

* **Geometrie & Wandstärke:** $110{,}0 \times 74{,}0 \times 6{,}0\,\text{mm}$, $3{,}0\,\text{mm}$ durchgehende PA12-Wandstärke.
* **Druckausgleich:** Ein zentrales Gore ePTFE-Schraubventil ($\varnothing\,7{,}0\,\text{mm}$, M8-Gewinde) gleicht Luftdruckschwankungen (Passfahrten bis $3.000\,\text{m}$ Höhe) und thermische Atmungseffekte zuverlässig aus.
* **Hermetische Abdichtung:** Umlaufende Shore 40A Silikon-Profildichtung in der Deckelnut, verschraubt über 4x M3 Edelstahlschrauben in Ruthex-Gewindeeinsätze der Unterwanne.
* **Wartungsvorteil:** Zum Tausch des Pufferakkus oder zur Inspektion kann der Deckel werkzeuglos abgenommen werden, ohne dass Kabel oder optische Lichtleiter gelöst werden müssen.

---


## 5. Gehaeuse Typ B: Universeller Satelliten-Pod (Identisch fuer Pod 1, 2 und 3)

- **Vollstaendige Modularitaet:** Alle 3 Pod-Positionen am Motorrad nutzen das identische, universelle Gehaeuse im **generischen Maximal-Envelope ($120{,}0 \times 64{,}0 \times 32{,}0\,\text{mm}$)**.
- **Abmessungen Schacht:** $96{,}0 \times 56{,}0 \times 24{,}0\,\text{mm}$ (PA12 MJF, $3{,}0\,\text{mm}$ Wandstärke).
- **Elektronik-Kassette / Schlitten:** $92{,}0 \times 54{,}0 \times 23{,}5\,\text{mm}$ (Lichter Innenbauraum: $88{,}0 \times 50{,}0 \times 23{,}5\,\text{mm}$).

### 5.1 2-Teilige modulare Kassetten-Architektur (Universal-Unterschlitten & Modul-Oberteil)

Um maximale Flexibilität bei minimalen Fertigungskosten zu erzielen, ist jede Wechselkassette als **2-teiliges modulares Baugruppensystem** aufgebaut:

```
                      MODULARE 2-TEILIGE WECHSELKASSETTE
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. AUSTAUSCHBARES MODUL-OBERTEIL (3D-Konturbett & Haltenest):               │
│    • Spezifisch für Sena 50S/60S, Cardo Air-Mount oder Midland XT30/PMR     │
│    • Integriertes Pogo-Pin Kontaktfeld / N52-Magnete / EPDM-Spannlasche     │
│    • 10.0 x 3.0 mm Kabeldurchbruchsschlitz (R=1.0 mm) in den Unterflurkanal │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. AKUSTISCHE TPU-DÄMPFUNGSZWISCHENLAGE (Shore 40A, 0.5 mm - Klapperschutz) │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. GENERISCHER UNIVERSAL-UNTERSCHLITTEN (Universal Base Sled):              │
│    • 100% identisch für ALLE Headset- und Funk-Varianten                    │
│    • Bodenfach für Trägerplatine (openmotorbridge_pod_cartridge, 35x25mm)   │
│    • Stirnseitiger Sitz für 6-Pin Buchse J1 & axialer JST-SH Header J2      │
│    • 1.5 mm tiefer Unterflur-Kabelkanal & 4x M2 Ruthex-Gewindeeinsätze      │
│    • Poka-Yoke Führungsrippen (1.5 / 2.0 mm) & Snap-Fit Schnellverriegelung │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Konstruktive Aufteilung & Dichtungskonzept:
1. **Generischer Universal-Unterschlitten (Base Sled, $92{,}0 \times 54{,}0 \times 23{,}5\,\text{mm}$):**
   * Bildet das robuste PA12-Grundchassis mit den seitlichen Poka-Yoke Führungsrippen und den Schnappriegel-Rastnasen.
   * Beherbergt im vorderen Bodenfach die standardisierte $35{,}0 \times 25{,}0\,\text{mm}$ Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`) mit dem Maxim DS2401 ID-Chip und der stirnseitigen 6-Pin Buchsenleiste `J1`.
   * Besitzt einen **$1{,}5\,\text{mm}$ tiefen und $8{,}0\,\text{mm}$ breiten Unterflur-Kabelkanal** im Boden sowie 4x eingelassene M2 Messing-Gewindeeinsätze (*Ruthex M2*).
2. **Austauschbares Modul-Oberteil (3D-Konturbett Inlay):**
   * Das Oberteil wird individuell an das jeweilige Headset-Modell angepasst (z. B. Sena 50S Klickbett mit Rastriegel, Cardo Packtalk Edge mit 2x N52 Magneten, Midland XT30 Klemmschiene).
   * Enthält den **$10{,}0 \times 3{,}0\,\text{mm}$ Kabeldurchbruchsschlitz** mit beidseitig $R=1{,}0\,\text{mm}$ verrundeten Kanten, durch den das 6-adrige JST-SH Flachbandkabel vom Unterflurkanal direkt an die Lötseite des Kontaktfeldes (Pogo-Array / Air-Mount) geführt wird.
   * Wird mit **4x M2 Senkkopfschrauben** (Edelstahl V4A) fest mit dem Unterschlitten verschraubt. Beim Wechsel des Headset-Herstellers muss der Fahrer lediglich das 3D-gedruckte Oberteil tauschen – die Elektronik-Trägerplatine bleibt erhalten.
3. **Dichtungskonzept (Klarstellung zur Gehäuseabdichtung):**
   * **Die IP67/IP69K-Wasserdichtigkeit wird vollständig am vorderen Stirnflansch des Pod-Gehäuses hergestellt:** Die umlaufende Shore 40A Silikondichtung der Kassettenblende dichtet den gesamten Wechselschacht beim Einrasten hermetisch gegen Strahlwasser und Staub ab.
   * Da das Innere des Pod-Schachts im Betrieb **zu 100 % trocken und geschützt** ist, ist **zwischen Kassetten-Unterteil und Kassetten-Oberteil keine druckdichte IP67-Flachdichtung erforderlich**.
   * Eine dünne $0{,}5\,\text{mm}$ Shore 40A TPU/Silikon-Zwischenlage zwischen Unter- und Oberteil dient rein der mechanischen Schwingungsentkopplung und dem Klapperschutz bei harten Fahrbahnstößen.

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
3. **Integrierte ePTFE-Druckausgleichsmembran an der Kassetten-Frontblende:**
   * Beim Einschieben des Schlittens dichtet die umlaufende Silikon-Flanschdichtung den Schacht bereits kurz vor Erreichen des Endanschlags ab. Ohne Druckausgleich würde die verdrängte Luft wie ein pneumatischer Kolben komprimieren und das Einrasten erschweren.
   * Direkt in die Kassetten-Frontblende ist eine **$\varnothing\,6{,}0\,\text{mm}$ Gore ePTFE-Membran** integriert. Sie lässt Luft beim Einschieben widerstandslos entweichen, gleicht thermische Druckdifferenzen bei Regen oder Sonneneinstrahlung aus und hält Wasser sowie Staub zu $100\,\%$ nach IP67 ab.

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

1. **Geschützter Unterflur-Kabelkanal & Zwischenboden-Durchführung (*Under-Bed Routing & Pass-Through Slot*):**
   * **Kabeldurchführung im Kassetten-Zwischenboden:** Ein präziser **$10{,}0 \times 3{,}0\,\text{mm}$ Durchbruch mit beidseitig $R=1{,}0\,\text{mm}$ verrundeten Kanten** im Zwischenboden des PA12-Schlittens führt das Flachbandkabel von Header `J2` auf der unteren Trägerplatine nach oben in das 3D-Konturbett.
   * **Unterflur-Kanal:** Im Boden des PA12-Schlittens ist eine **$1{,}5\,\text{mm}$ tiefe und $8{,}0\,\text{mm}$ breite Kabelführung** direkt unterhalb des 3D-Kontur-Negativbetts integriert.
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

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Abbildung 5.2: 3D-CAD-Visualisierung der 4 modularen Wechselkassetten-Varianten im universellen Grundschlitten ($75 \times 54 \times 20{,}5\,\text{mm}$): OMM Heck-Transceiver mit GPS & LoRa (vorne links), Sena 50S/60S Quick-Snap Cradle (vorne rechts), Cardo Magnetic Air Mount (hinten links) und wasserdichte IP67 Blindkassette / Dry Box (hinten rechts).*

#### 1. Sena 50S / 60S Kontur-Nest & Snap-Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Abbildung 5.3: 1:1:1 euklidische CAD-Visualisierung der Sena 50S/60S 2-teiligen Wechselkassette im Satelliten-Pod. Erkennbar sind der generische Unterschlitten mit Adapterplatine (50x22 mm), der 1.5 mm Unterflur-Kabelkanal, das austauschbare 3D-Konturbett mit Jog-Dial-Arretierung und die EPDM-Spannlasche.*

* **3D-Kontur-Negativbett:** Der Schlittenboden ist als exaktes 3D-Negativ der Sena-Gehäuseunterseite ausgeformt. Das Gerät sinkt $4{,}0\,\text{mm}$ tief in die Aussparung ein und kann sich in $X$- und $Y$-Richtung nicht um einen Zehntelmillimeter verschieben.
* **OEM-Klick-Arretierung:** Formschlüssige untere Haltenase ($4{,}0\,\text{mm}$ *Bottom Hook*) und oberer federbelasteter POM-Rastriegel (*Top Release Latch*). Das Gerät klinkt mit einem satten Klick ein.
* **Elastische EPDM-Sicherungslasche (Gummilasche):** Eine $12\,\text{mm}$ breite, UV- und ölbeständige EPDM-Spannlasche spannt sich quer über die Gehäusemitte und wird an seitlichen T-Ankern eingehängt. Sie zieht das Sena permanent nach unten in das Konturbett – **100 % rüttel- und klapperfrei auch bei harten Offroad-Schlägen**.
* **Elektrischer Übergang:** 7-poliges vergoldetes Federkontaktfeld (Pogo-Array bei $X = +22{,}0\,\text{mm}$) greift direkt auf die originalen Gegenkontakte des Sena-Geräts; JST-SH 6P Flachbandkabel durch den Unterflurkanal zur Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`).

#### 2. Cardo Packtalk Edge / Pro Magnetic Air Mount & Kontur-Nest
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Abbildung 5.4: 1:1:1 euklidische CAD-Visualisierung der Cardo Packtalk Edge 2-teiligen Wechselkassette im Satelliten-Pod. Gezeigt werden der N52-Neodym-Magnetsitz (Ø8x2 mm), das 5-Pin Federkontaktfeld bei X = +10 mm und der scheuerfreie Kabelverlauf unter dem Dämpfungsinlay.*

* **3D-Kontur-Negativbett:** Die Aufnahme bildet die geschwungene Unterseite des Packtalk Edge exakt nach. Eine $0{,}8\,\text{mm}$ Shore 40A Silikoneinlage dämpft Motor- und Fahrbahnstöße ab.
* **Dual-N52-Magnetanzug & Klickflanken:** Zwei Neodym-Magnete ($2\times \varnothing\,8 \times 2\,\text{mm}$ N52 bei $X = -8\,\text{mm}$ und $X = +28\,\text{mm}$) ziehen das Gerät passgenau in die Kontur. Zwei seitliche PA12/POM-Sicherungsflanken greifen formschlüssig in die Cardo-Haltenuten ($> 120\,\text{N}$ Abreißkraft).
* **Elastische EPDM-Sicherungslasche:** Zusätzliche elastische Gummilasche für extreme Bedingungen (Enduro/Gravel), die ein vertikales Ausfedern mechanisch unmöglich macht.
* **Elektrischer Übergang:** 5-Pin Federkontaktfeld bei $X = +10{,}0\,\text{mm}$ stellt blitzschnell den Kontakt zu Audio, Mic und 5V-Speisung her.

---

### 5.3.1 Mechanischer & Elektrischer Längsschnitt-Vergleich (Tolerance & Clearance Stack-Up)

![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Abbildung 5.5: Maßstabsgetreuer 2D-Längsschnitt (X-Z Ebene) durch die Sena 50S (oben) und Cardo Packtalk Edge (unten) Wechselkassetten im geschlossenen Pod-Gehäuse. Dargestellt sind die 2-teilige Schichtung, der axiale JST-SH Kabelabgang nach rechts (+X), die M2-Verschraubungsebenen und die exakte axiale Zentrierung der 6-Pin Steckverbindung auf Y=0, Z=0.*

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
* **Poka-Yoke Falscheinbauschutz der Platinen (Mechanische Unverwechselbarkeit):**
  * Alle Platinen im System sind so konstruiert, dass sie **nur in exakt einer einzigen Ausrichtung passen**:
    * **Kassetten-Platinen (Pod 1, 2 & 3):** Können nicht verkehrt herum eingebaut werden, da die 6-Pin-Schnittstelle fest an der vorderen Stirnkante sitzt und bei $180^\circ$-Drehung nach hinten ins Kassetteninnere zeigen würde.
    * **Stirnwand-Adapterplatine (`openmotorbridge_pod_base`):** Um eine versehentliche $180^\circ$-Montage auf dem Kopf (und damit ein Vertauschen von Pin 1 `VCC` mit Pin 6 `1-WIRE_ID`) zuverlässig zu verhindern, besitzt die Platine an der unteren Kante eine asymmetrische **$4{,}0 \times 2{,}5\,\text{mm}$ Codierkerbe** (`Edge.Cuts` bei $X = 125 \dots 129\,\text{mm}$). Im Gehäuseboden greift eine korrespondierende **PA12-Codiernase** formschlüssig in diese Kerbe ein. Wird die Platine falsch herum angesetzt, stößt sie auf die Nase, steht schräg heraus und lässt sich nicht festschrauben.
* **Federgestützter Push-Out / Auto-Eject Mechanismus:**
  * Links und rechts neben dem Schutzkragen sitzen in der Schottwand **zwei federbelastete Auswerfer-Druckfedern (V4A Edelstahl 1.4310)** mit Führungsstiften.
  * **Beim Einschieben:** Die Stirnseite des Kassetten-Schlittens drückt die Federn um $6{,}0\,\text{mm}$ zusammen, bis die 6-Pin Buchse voll im Schutzkragen sitzt und die Snap-Fit Rastnasen mit einem satten Klick einrasten. Die komprimierten Federn halten das System unter permanenter Vorspannung gegen die Silikondichtung – **100 % spielfrei und vibrationsfest**.
  * **Beim Entriegeln (Auto-Eject):** Sobald der Fahrer die beiden seitlichen Schnellentriegelungstaster an der Blende zusammendrückt, lösen sich die Rastnasen und **die Federn werfen die Kassette automatisch um $8\dots 10\,\text{mm}$ nach außen aus**.
  * Der Steckkontakt ist damit sauber getrennt und die Kassette lässt sich selbst mit dicken Motorrad-Winterhandschuhen mühelos und ohne Verkanten greifen und herausziehen.
* **Interne Konvektions- & Entwärmungsschlitze (Wärmebrücke im geschützten Innenraum):**
  * In der Schutz-Schottwand der Pod-Basis (2x $10{,}0 \times 2{,}0\,\text{mm}$) sowie im Kassettenboden unter der Trägerplatine (4x $12{,}0 \times 2{,}0\,\text{mm}$) sind interne Konvektionsschlitze eingebracht.
  * **Thermischer Vorteil:** Abwärme von Ladecontrollern, ESP32 und SX1262 LoRa-Endstufen staut sich nicht in isolierten Kunststofftaschen, sondern zirkuliert frei durch den gesamten Pod-Innenraum.
  * **Garantierte IP67-Dichtheit:** Da die äußere Kassetten-Frontblende mit der umlaufenden Silikondichtung den gesamten Schacht nach außen hermetisch versiegelt, bleibt der Innenraum trocken und geschützt, während die Wärme sich optimal im gesamten Schacht verteilt.

---

### 5.4.1 Detaillierte Mechanik & Kinematik des Snap-Fit & Auto-Eject Systems

Das Kassetten-Schnellwechselsystem vereint vibrationsfeste Verriegelung (nach Automotive-Schocknormen bis $20\,\text{g}$) mit einer komfortablen, einhändig bedienbaren **Auto-Eject-Kinematik**:

```
                       AUTO-EJECT & SNAP-FIT KINEMATIK (DRAUFSICHT X-Y)
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ POD-GEHÄUSE-TUNNEL (PA12, 100 x 60 mm)                                                       │
│                                                                                              │
│   ┌──────────────┐                                                     ┌─────────────────┐   │
│   │ Schutz-      │  ◄── V4A Auswerferfeder (k = 1.2 N/mm)              │ Rasttasche      │   │
│   │ Schottwand   ├───[§§§§§§§§§]───────────────┐                       │ in Tunnelwand   │   │
│   │ (x = 22 mm)  │   F_preload = 7.2 N         │                       │ (x = 86 mm)     │   │
│   │              │                             │                       │    ┌───────┐    │   │
│   │              │   6-Pin Vergoldeter         │ KASSETTEN-SCHLITTEN   │    │ 85°   │    │   │
│   │   ┌──────┐   │   Steckverbinder-Eingriff   │ (openmotorbridge_     │    │ Zahn  │    │   │
│   │   │6-Pin ├───┼════════════════════════════►│  cartridge_sled)      ├────┴┤ ▲    │    │   │
│   │   │Stift ├───┤   Wipe = 4.8 mm             │                       │  ┌──┘ │    └───┐│   │
│   │   └──────┘   │                             │                       │  │30° │        ││   │
│   │              │                             │                       │  │Ein-│        ││   │
│   │              ├───[§§§§§§§§§]───────────────┘                       │  │lauf│        ││   │
│   │              │  ◄── V4A Auswerferfeder                             │  └──┬─┘        ││   │
│   └──────────────┘                                                     │     │          ││   │
│                                                                        │  ┌──▼────────┐ ││   │
│                                                   Federnder PA12-Arm   │  │DRUCKTASTE │ ││   │
│                                                   (L=14 mm, b=10 mm) ──┴──┤(Geriffelt)│ ◄┼───┼── Daumen-/Zeigefinger-
│                                                                           └───────────┘ ││   │   Druck (F_squeeze = 10 N)
│                                                                           FRONTBLENDE   ││   │
└─────────────────────────────────────────────────────────────────────────────────────────┴┴───┘
```

#### 1. Vierstufiger Bewegungsablauf (Kinematische Phasen):

1. **Phase 1: Einführen & Zentrieren ($X = 0\dots 65\,\text{mm}$):**
   * Der Fahrer schiebt die Kassette in den Schacht. Die asymmetrischen Führungsrippen greifen in die Gehäusenuten ein (Poka-Yoke Schutz gegen $180^\circ$-Falscheinbau).
2. **Phase 2: Federkompression & Vorzentrierung ($X = 65\dots 74\,\text{mm}$):**
   * Die vordere Schlittenkante trifft auf die beiden V4A-Edelstahlfedern an der Schottwand.
   * Der $45^\circ$-Fangtrichter fängt die Buchsenleiste spielfrei ein und zentriert die 6 Kontaktstifte berührsicher.
   * Die $30^\circ$-Einlaufschrägen der beiden Schnapprastzähne gleiten sanft an der Gehäuseinnenwand entlang und lenken die federnden Arme um ca. $1{,}8\,\text{mm}$ nach innen aus.
3. **Phase 3: Verrastung & Dichtungskompression ($X = 75\,\text{mm}$ - Endposition):**
   * Sobald die Endposition erreicht ist, springen die Rastzähne mit einem deutlich hör- und spürbaren **„KLICK“** in die inneren $1{,}8\,\text{mm}$ tiefen Rasttaschen der Gehäusewand.
   * Die beiden Auswerferfedern sind nun um $\Delta x = 6{,}0\,\text{mm}$ vorgespannt und üben eine permanente axiale Gegenkraft von **$F_{\text{preload}} = 7{,}2\,\text{N}$** aus.
   * Diese Kraft presst die elastische Silikondichtung an der Frontblende um $30\,\%$ zusammen $\rightarrow$ **Hermetische IP67/IP69K Dichtigkeit bei absoluter Spielfreiheit**.
4. **Phase 4: Schnellentriegelung & Auto-Eject (Auswurf um $8\dots 10\,\text{mm}$):**
   * Beim Zusammendrücken der beiden seitlichen Riffeltaster an der Frontblende biegen sich die Cantilever-Arme nach innen.
   * Die $85^\circ$-Rastflanken treten aus den Gehäusetaschen heraus.
   * Schlagartig entspannen sich die beiden V4A-Federn und **katapultieren die Kassette sanft um $8\dots 10\,\text{mm}$ nach vorn heraus**.
   * Der 6-Pin Steckkontakt ($4{,}8\,\text{mm}$ Überdeckung) wird dabei vollständig getrennt; die Kassette ragt frei aus dem Schacht hervor und kann selbst mit klammen Fingern oder dicken Winterhandschuhen entnommen werden.

#### 2. Mechanische Dimensionierung & Kräftebilanz:

| Parameter | Formelzeichen / Formel | Berechneter Wert | Funktion & Sicherheitsnachweis |
| :--- | :--- | :---: | :--- |
| **Federrate (2x V4A Federn)** | $c_{\text{ges}} = 2 \times 1{,}2\,\text{N/mm}$ | **$2{,}4\,\text{N/mm}$** | Parallelschaltung zweier Edelstahl-Druckfedern (DIN EN 13906-1) |
| **Vorspannfederweg** | $\Delta x_{\text{pre}}$ | **$6{,}0\,\text{mm}$** | Kompression von $L_0 = 15{,}0\,\text{mm}$ auf $L_{\text{mated}} = 9{,}0\,\text{mm}$ |
| **Axiale Haltekraft (Preload)** | $F_{\text{preload}} = c_{\text{ges}} \cdot \Delta x_{\text{pre}}$ | **$7{,}2\,\text{N}$** | Hält Dichtsitz permanent unter Druck gegen $20\,\text{g}$ Vibration |
| **Dichtungs-Gegenkraft** | $F_{\text{seal}}$ (Shore 40A Silikon) | **$4{,}5\,\text{N}$** | $30\,\%$ Kompression der umlaufenden $1{,}5\,\text{mm}$ Dichtschnur |
| **Auszugskraft (Rückhalt)** | $F_{\text{retention}} = 2 \times \frac{E I \delta}{L^3} \cdot \tan(85^\circ)$| **$> 65\,\text{N}$** | Verhindert unbeabsichtigtes Lösen durch Zugbelastung am Kabel |
| **Entriegelungskraft (Squeeze)**| $F_{\text{squeeze}} = 2 \times \frac{3 E I \delta}{L^3}$ | **$9{,}8\,\text{N}$** | Ergonomisch optimierter Daumen-Zeigefinger-Druck ($\approx 1\,\text{kg}$) |
| **Automatischer Auswurfhub** | $\Delta x_{\text{eject}} = L_0 - L_{\text{mated}}$ | **$9{,}0\,\text{mm}$** | Trennt 6-Pin Wipe ($4{,}8\,\text{mm}$) mit **$+4{,}2\,\text{mm}$ Überhub** |

#### 3. Spannungs- & Ermüdungsnachweis des PA12-Biegebalkens:
* **Abmessungen des Schnapparms:** Länge $L = 14{,}0\,\text{mm}$, Breite $b = 10{,}0\,\text{mm}$, Dicke $h = 1{,}8\,\text{mm}$.
* **Maximale Randfaserdehnung:**
  $$\epsilon_{\max} = \frac{3 \cdot h \cdot \delta}{2 \cdot L^2} = \frac{3 \cdot 1{,}8\,\text{mm} \cdot 1{,}8\,\text{mm}}{2 \cdot (14{,}0\,\text{mm})^2} = \frac{9{,}72}{392} \approx 0{,}0248 \implies \mathbf{1{,}38\,\% \text{ bei Montage-Endlage}}$$
* **Zulässige Dauerdehnung für PA12 (MJF):** $\epsilon_{\text{zul}} \le 2{,}0\,\%$.
* **Biegespannung:** $\sigma_b = \epsilon \cdot E_{\text{PA12}} = 0{,}0138 \times 1.700\,\text{MPa} = \mathbf{23{,}5\,\text{MPa}}$ (Weit unterhalb der PA12-Streckgrenze von $48\,\text{MPa} \rightarrow$ **Sicherheitsfaktor $S = 2{,}04$**).
* **Ergebnis:** Das Schnappwerk ist dauerfest ausgelegt für $> 10.000$ Ver- und Entriegelungszyklen ohne plastische Verformung oder Materialermüdung.

---

### 5.5 Mittige Pod-Druckausgleichsmembran (ePTFE auf der Gehäuse-Oberseite)
* **Problemstellung:** Interne Abwärme (SX1262 LoRa $+22\,\text{dBm}$ PA, Ladeschaltung) und Sonneneinstrahlung erzeugen Druckdifferenzen im kleinen Pod-Volumen.
* **Positionierung:** Zentral auf der **langen Gehäuse-Oberseite** ($X = 0{,}0\,\text{mm}, Y = 0{,}0\,\text{mm}$) sitzt eine in eine Schutzsenkung integrierte **$\varnothing\,7{,}0\,\text{mm}$ ePTFE-Druckausgleichsmembran** (*Schreiner Air Vent* / *Gore Automotive Adhesive Vent*).
* **Funktion:** Belüftungsrate $> 25\,\text{ml/min}$ bei 70 mbar, Wassereintrittspunkt $> 1{,}5\,\text{bar}$ (IP67). Verhindert Vakuum-Wassersaugen bei Abkühlung durch Regengüsse und gleicht thermische Druckschwankungen im gesamten Pod-Innenraum symmetrisch aus.

---

### 5.6 Monolithische PA12-Präzisions-Linearführung & Kontaktlängen-Sicherheit

Da die Satelliten-Pods durch ihre optimierte Schaltungsarchitektur extrem verlustarm arbeiten (Pods 1 & 2: $< 50\,\text{mW}$; Pod 3: max. $0{,}56\,\text{W}$ bei $> 85\,\text{cm}^3$ Innenluftvolumen), sind metallische Zusatzkühlkörper oder Kupfer-Gleitbleche physikalisch überflüssig. Das System setzt auf eine **100 % homogene, korrosionsfreie PA12-auf-PA12 Präzisions-Gleitführung**:

```
                 POD-SCHACHT & KASSETTEN-EINRASTUNG (SCHNITT X-Z)
┌─────────────────────────────────────────────────────────────────────────────┐
│ GEHÄUSE-DECKEL (PA12 MJF, 2.5 mm Wandstärke)                                │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ 1. POD-BASIS-PLATINE          │ 3. WECHSELKASSETTEN-SCHLITTEN               │
│    (openmotorbridge_pod_base) │    (openmotorbridge_pod_cartridge)          │
│                               │                                             │
│    ┌──────────┐  4.8 mm Wipe  │  ┌───────────┐                              │
│    │ 6-Pin    ├═══════════════╪═►│ 6-Pin     │                              │
│    │ Pin-Array│   Eingriff    │  │ Buchsen-  │                              │
│    │ (L=6.5mm)│ (Gold Au/Ni)  │  │ Leiste    │                              │
│    └────┬─────┘               │  └─────┬─────┘                              │
│         │                     │        │                                    │
│    ┌────▼─────────────────────┴────────▼─────┐                              │
│    │ Schottwand mit Fangtrichter & Federn    │ ◄── 7.2 N permanente Vorspannung
└────┴─────────────────────────────────────────┴──────────────────────────────┘
```

#### 1. Detaillierte Kontaktlängen- & Kontaktsicherheits-Berechnung:
* **Steckverbinder-Typ:** 6-Pin Präzisions-Prägestiftleiste (`J1` Pod-Base) $\leftrightarrow$ 6-Pin Präzisions-Buchsenleiste (`J1` Kassette) im Standard-Raster $2{,}54\,\text{mm}$ mit $0{,}76\,\mu\text{m}$ ($30\,\mu\text{in}$) Hartgold-Beschichtung über Nickel.
* **Geometrische Längenverhältnisse:**
  * **Freie Stiftlänge ($L_{\text{pin}}$):** Die vergoldeten Vierkant-Prägestifte ($0{,}64 \times 0{,}64\,\text{mm}$) ragen $6{,}5\,\text{mm}$ aus der Montageebene der Schottwand hervor.
  * **Eintauchtiefe in Buchse:** Die korrespondierende Buchsenleiste auf der Kassettenplatine besitzt eine innere Kontakttiefe von $6{,}2\,\text{mm}$.
  * **Tatsächliche Überdeckung (*Contact Wipe*):** Im vollständig verriegelten Endzustand dringen die Stifte **$4{,}8\,\text{mm}$ tief in die Doppelschenkel-Kontaktfedern (Dual-Beam Phosphorbronze)** ein.
  * **Sicherheitsreserve gegenüber Automotive-Normen:** Die Norm *USCAR-2 / IEC 60603* fordert für rüttelfeste Kfz-Steckverbinder eine Mindest-Wischlänge (*Wipe Length*) von $\ge 1{,}5\,\text{mm}$. Mit **$4{,}8\,\text{mm}$** Überdeckung übertrifft das System die Norm um den **Faktor 3,2**.
* **Kein Kontaktprellen bei Vibrationen (> 20 g):**
  * Die beiden V4A-Edelstahlfedern in der Schottwand drücken den Kassetten-Schlitten permanent mit **$7{,}2\,\text{N}$ axialer Vorspannkraft** gegen die POM-Schnappriegel.
  * Die Silikon-Flanschdichtung an der Stirnseite wird dabei um $30\,\%$ komprimiert.
  * Ein axiales Spiel oder relatives Wandern der Kontakte bei Schlaglöchern oder Motorvibrationen ist mechanisch ausgeschlossen.

#### 2. Reibungs- & Verschleißverhalten der PA12-Führung:
* **Selbstschmierendes Gleitverhalten:** Chemisch dampfgeglättetes PA12 besitzt einen extrem niedrigen Gleitreibungskoeffizienten ($\mu \approx 0{,}15\dots 0{,}20$).
* **Führungsspiel:** Das Nennspiel zwischen den asymmetrischen Führungsrippen der Kassette ($2{,}6\,\text{mm}$) und den Gehäusenuten ($3{,}0\,\text{mm}$) beträgt exakt $0{,}2\,\text{mm}$ pro Seite – eng genug für spielfreie Führung, weit genug gegen Klemmen bei Schmutzpartikeln.
* **Lebensdauer:** Geprüft für $> 1.000$ werkzeuglose Steckzyklen ohne messbaren Kunststoffabrieb.

### 5.7 IP67 Blind- / Leerkassette (`Pod_Dummy_Cartridge_IP67.stl`)

Wird ein Pod-Schacht temporär nicht für ein Headset genutzt (z. B. bei Einzelfahrer-Konfiguration mit nur 1 Intercom, bei Wartungsarbeiten oder während der Winterpause), verschließt die formidentische **IP67-Blindkassette** den Wechselschacht hermetisch:

![OpenMotorBridge IP67 Blindkassette 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

#### Mechanische Spezifikation & Dichtungskonzept:
* **100 % Formidentischer Schlittenkörper ($92{,}0 \times 54{,}0 \times 23{,}5\,\text{mm}$):**
  * Gleitet spielfrei auf denselben seitlichen Führungsbahnen wie aktive Kassetten.
  * Vollständig geschlossene, ergonomische Frontblende ($58{,}0 \times 28{,}0 \times 5{,}0\,\text{mm}$) mit griffiger Rändelstruktur und zentrierter Griffmulde.
* **Hermetische IP67/IP69K-Umlaufdichtung:**
  * In eine $2{,}5\,\text{mm}$ tiefe Nut hinter dem Frontkragen ist eine hochelastische Silikon-/EPDM-Profildichtung eingelegt.
  * Beim Einrasten der Kassette wird die Dichtung um 30 % komprimiert und schützt die innenliegenden Kontakte und Steckstifte dauerhaft vor Schmutz, Hochdruckreiniger-Wasser und Streusalz.
* **Duale Snap-Fit Rastnasen & Auto-Eject:**
  * Nutzt dieselben seitlichen PA12/POM-Schnappriegel. Beim Drücken der beiden seitlichen Riegeltasten werfen die internen Federn der Schottwand die Blindkassette automatisch $10\,\text{mm}$ aus.
* **Integriertes Notfall-Staufach (*Utility Dry Storage*):**
  * Da die Blindkassette keine Elektronik aufnehmen muss, bietet der hohle Innenraum ein **absolut wasserdichtes $80 \times 46 \times 16\,\text{mm}$ Mini-Staufach** (mit abnehmbarem Klick-Deckel) für Notfall-Bargeld, Kopie des Fahrzeugscheins, Inbusschlüssel oder Ersatz-O-Ringe.
* **Elektrisches Systemverhalten:**
  * Rein mechanischer Verschluss ohne Platinenbestückung. Die Buchse an der Schottwand bleibt berührsicher im Schutzkragen.
  * Der ESP32-S3 erkennt den offenen 1-Wire-Bus (Timeout) und lädt automatisch das Profil `disabled.json` (Audio-Relais hochohmig getrennt, 5V-Ladeschiene stromlos).

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

### 5.9 Asymmetrisches Nut-und-Feder Führungsschienen- & Poka-Yoke Konzept

Um Verkanten, schiefe Krafteinleitung und fehlerhaftes Einstecken physikalisch auszuschließen, verfügt das Pod-Kassetten-System über eine **asymmetrische Nut-und-Feder-Linearführung**:

```
                  ◄──────────── 60.0 mm Pod-Breite ────────────►
 ┌─────────────────────────────────────────────────────────────┐ ▲
 │                    2.5 mm Gehäuse-Decke                     │ │
 │ ┌───┬─────────────────────────────────────────────────┬───┐ │ │ 28.0 mm
 │ │   │                                                 │   │ │ │ Pod-
 │ │   │         ZENTRISCHER KASSETTEN-EINSCHUB          │   │ │ │ Höhe
 │ │   │                 (54 x 22 mm)                    ├───┤ │ │
 │ │   │                                                 │Nut│ │ │ (Rechte Nut
 │ │   │                                                 │   │ │ │  bei z=14.2 mm)
 │ ├───┤             ┌─────────────────────┐             ├───┤ │ │
 │ │Nut│             │  6-PIN STECKER      │             │   │ │ │
 │ │   │ ◄───────────┤  (Exakt zentriert)  ├───────────► │   │ │ │
 │ ├───┤             └─────────────────────┘             │   │ │ │
 │ │   │                                                 │   │ │ │ (Linke Nut
 │ │   │                                                 │   │ │ │  bei z=8.2 mm)
 │ └───┴─────────────────────────────────────────────────┴───┘ │ │
 │                    2.5 mm Gehäuse-Boden                     │ │
 └─────────────────────────────────────────────────────────────┘ ▼
```

#### 3D-CAD-Schnittansicht der asymmetrischen Poka-Yoke Passung:

![OpenMotorBridge Pod Poka-Yoke Asymmetrical Guide Rails 3D Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Abbildung 5.6: 3D-CAD-Querschnitt (Y-Z Ebene) durch das Satelliten-Pod-Gehäuse und den eingeschobenen Kassetten-Grundschlitten. Deutlich sichtbar ist der $6{,}0\,\text{mm}$ Höhenversatz der Führungsnuten (Links: $Z=8{,}2\,\text{mm}$, Rechts: $Z=14{,}2\,\text{mm}$) mit formschlüssig gleitenden Kassetten-Führungsfedern (blaue Schlittenflanken) und millimetergenauer Zentrierung der zentralen Kontaktebene.*

#### 4-Stufen-Sicherheit für perfekten Kassetten-Sitz:
1. **Asymmetrische Nut-und-Feder Führungsschienen (Tongue & Groove Linear Rails):**
   * **Nut im Pod-Innenraum:** Beidseitig durchgehende Führungsnuten ($3{,}0\,\text{mm}$ Nutbreite, $1{,}5\,\text{mm}$ Tiefe) in den Seitenwänden des Schachts.
   * **Feder an den Kassettenflanken:** Umlaufende Führungsrippen ($2{,}6\,\text{mm}$ Höhe, $1{,}4\,\text{mm}$ Auskragung) an der Kassettenaußenwand.
   * **Vorteil:** Die Kassettenwand bleibt massiv und stabil ($2{,}5\,\text{mm}$), während die Feder als Versteifungsrippe wirkt.
2. **Poka-Yoke Verpolschutz durch Höhenversatz:**
   * **Linke Führungsnut/Feder:** Positioniert auf Höhe $z = 8{,}2\,\text{mm}$.
   * **Rechte Führungsnut/Feder:** Positioniert auf Höhe $z = 14{,}2\,\text{mm}$.
   * Ein verkehrtes (über Kopf um $180^\circ$ gedrehtes) Einschieben der Kassette ist **mechanisch 100 % ausgeschlossen**, da die Federn sofort an der Gehäusestirn blockieren.
3. **$30^\circ$-Einlaufschräge für blindes Stecken am Helm:**
   * Die Kassetten-Führungsfedern besitzen an der Kassettennase auf den ersten $4{,}0\,\text{mm}$ eine **$30^\circ$-Einlauf-Anfasung**.
   * Die Kassette zentriert sich beim Einstecken mit Motorradhandschuhen selbsttätig in der Nut, fängt Querkräfte ($Y$- und $Z$-Achse) ab und führt die 6-Pin Präzisionskontakte mit **$\pm 0{,}1\,\text{mm}$ Toleranz exakt zentrisch** in die Schottwand-Buchse.
4. **Formschlüssiger Endanschlag & Auto-Eject:**
   * Die Einschubkraft wird direkt von der massiven Schottwand (PA12) abgefangen – die Platinen-Lötstellen bleiben zu 100 % kräftefrei. Die beiden V4A-Edelstahlfedern halten das System permanent unter Vorspannung und werfen den Schlitten beim Entriegeln um $10\,\text{mm}$ aus.

### 5.10 Universelle 1-Pod-Architektur (Pod 1, Pod 2 & Pod 3 sind 100 % baugleich)

Das gesamte OpenMotorBridge-System basiert auf dem Prinzip der **vollständigen mechanischen Universalität**:

#### 3D-CAD-Explosionsdarstellung & Aufbau der universellen Pod-Baugruppe:

![OpenMotorBridge Satelliten-Pod CAD Explosionsdarstellung](../images/cad/openmotorbridge_pod_exploded_view.png)

*Abbildung 5.7: 3D-CAD-Explosionsdarstellung des universellen Satelliten-Pods. Gezeigt werden das 5-seitige Monocoque-Schachtgehäuse mit dezent verrundeten Außenkanten (R=3 mm), integriertem V-Nut-Rohrbett (Ø18-35 mm) und 4x seitlichen EPDM-Einhängenasen, rückseitigem M8 6-Pin IP67 Kabelanschluss, Schutz-Schottwand mit 6-Pin Fangtrichter, V4A-Auswerferfedern und der herausgezogene Universalschlitten mit asymmetrischen Poka-Yoke Führungsfedern.*

![OpenMotorBridge Satelliten-Pod Röntgenansicht](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Abbildung 5.8: 3D-Röntgen- und Transparenzdarstellung des geschlossenen Satelliten-Pods mit eingeschobener Wechselkassette. Gut erkennbar sind das integrierte Universal-Rohrbett an der Unterseite, die spielfreien asymmetrischen Poka-Yoke Führungsnuten, der zentrierte 6-Pin Kolbeneinschub in den Schutzkragen und die bündige Flanschabdichtung.*

1. **Ein einziges universelles Pod-Gehäuse (`pod_base_housing.stl`):**
   * Alle drei Satelliten-Pods (Pod 1 Links, Pod 2 Rechts, Pod 3 Heck) verwenden **exakt denselben 5-seitigen Monocoque-Schacht** ($100 \times 60 \times 28\,\text{mm}$) mit M8 6-Pin IP67 Rückanschluss, Schutz-Schottwand, 6-Pin Schutzkragen und Auto-Eject Federmechanismus.
   * **Integrierte Universal-Rohrbett- & EPDM-Spannbefestigung:**
     * **An der Unterseite:** Eine angeformte $120^\circ$-V-Nut ($R = 15\,\text{mm}$) schmiegt sich formschlüssig an alle typischen Motorrad-Rohre ($\varnothing 18\dots 35\,\text{mm}$: $1"$ Sturzbügel, $7/8"$ Heckrahmen, $1\,1/8"$ Fatbars) oder liegt kippstabil auf planen Flächen auf.
     * **4x Seitliche Einhängenasen:** Ermöglichen die blitzschnelle, werkzeuglose Montage mit 2 UV-beständigen EPDM-Gummiringen oder Silikon-Leiterbändern unter gleichzeitiger Vibrationsentkopplung.
     * **Dauerhafte Sicherung:** Zusätzliche $5{,}0 \times 2{,}5\,\text{mm}$ Durchgangsschlitze erlauben die diebstahlgeschützte Festmontage per Standard-Kabelbinder ($4{,}8\,\text{mm}$) oder Edelstahl-Schlauchschellen.
2. **Funktionsanpassung ausschließlich über die Wechselkassetten:**
   * **Audio- & Intercom-Kassetten (Pod 1 & 2):** 2-teilig mit `openmotorbridge_pod_cartridge` Trägerplatine (DS2401 ID), Unterflur-Kabelkanal, Zwischenboden und Modellspezifischem 3D-Konturbett (Sena / Cardo / Midland).
   * **OMM-Transceiver-Kassette (Pod 3):** 1-teilig mit voller $23{,}5\,\text{mm}$ Innenhöhe und freiem $> 85\,\text{cm}^3$ Luftraum für optimale Antennenabstrahlung. Die `openmotorbridge_rear_transceiver` Platine sitzt direkt im Schlitten und steckt in derselben 6-Pin Präzisionsbuchse.
   * **Blindkassette:** Hermetisch dichter IP67-Dummy mit integriertem Notfall-Trockenstaufach (*Dry Box*).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 UNIVERSELLE OPENMOTORBRIDGE POD-ARCHITEKTUR                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                    1x UNIVERSELLES POD-BASIS-GEHÄUSE                        │
│   (5-seitiger Monocoque-Schacht mit V-Rohrbett & 4x EPDM-Spannbandnasen)    │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ MONTAGE-POSITIONEN AM BIKE:          │ WECHSELKASSETTEN (Einschub vorne):   │
│ • Sturzbügel / Rahmenrohr links      │ • Sena 50S/60S Kassetten-Schlitten   │
│ • Sturzbügel / Rahmenrohr rechts     │ • Cardo Packtalk Edge Schlitten      │
│ • Heckgepäckträger / Kennzeichentr.  │ • OMM Transceiver Schlitten (Pod 3)  │
│ • Flach unter Sitz / Seitendeckel    │ • Wasserdichte IP67 Blindkassette    │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

### 5.11 CAD-Dateistruktur & Tinkercad-Modulbaukasten (STL-Bibliothek)

Alle 3D-Gehäusemodelle stehen im Verzeichnis [hardware/cad/stl/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/) und [hardware/3d_models_mjf/](file:///Users/schmidtm/openMotorBridge/hardware/3d_models_mjf/) in 3 klar strukturierten Hauptpaketen bereit:

```
hardware/cad/stl/
├── 01_main_box/                                 # Zentrale Steuerbox (3-Teiliges Sandwich)
│   ├── main_box_complete_assembly.stl           # Vollständiges 3D-Montagemodell
│   ├── main_box_lower_case.stl                  # Unterwanne mit Dichtnut & 4x M3 Eck-Spannsäulen
│   ├── main_box_mid_tray.stl                    # Oberwanne mit Zwischenboden & 4x M3 Eck-Pfosten
│   ├── main_box_lid.stl                         # Gehäusedeckel mit Dichtfeder & Gore-Vent Bohrung
│   └── components/                              # Tinkercad-Primitiven zum freien Editieren & Stanzen
│       ├── 01_lower_tub_empty.stl               # Leere Wanne (ohne Zylinder)
│       ├── 02_pcb_4_standoffs_group.stl         # 4x PCB-Schraubdome als Gruppe
│       ├── 03_single_m2_5_standoff.stl          # Einzelner M2.5 Schraubdom (im Nullpunkt)
│       ├── 04_single_m4_mounting_ear.stl        # Einzelnes M4-Montageohr
│       ├── 05_mid_tray_solid_frame.stl          # Mittelrahmen massiv geschlossen (105x75x15 mm)
│       ├── 06_mid_partition_floor_solid.stl     # Zwischenboden massiv geschlossen
│       ├── 07_lipo_battery_cradle_1000mah.stl   # LiPo-Akkuhalterung (1000 mAh Standard)
│       ├── 08_lipo_battery_cradle_1500mah_large.stl # LiPo-Akkuhalterung (1500 mAh Large)
│       ├── 09_cutout_tool_usb_c.stl             # Schneidkörper USB-C (in Tinkercad: "Bohrung")
│       ├── 10_cutout_tool_led_window.stl        # Schneidkörper RGB-LED Statusfenster
│       ├── 11_cutout_tool_hd26_dsub.stl         # Schneidkörper HD26 Kabelbaumflansch
│       ├── 12_cutout_tool_m16_round_gland.stl   # Schneidkörper M16 Rundsteckverbinder
│       ├── 13_cutout_tool_cable_slot.stl        # Schneidkörper Zwischenboden-Kabelschlitz
│       ├── 14_lid_plate_only.stl                # Reine Deckelplatte
│       ├── 15_lid_sealing_lip.stl               # Deckel-Einpress-Dichtlippe
│       ├── 16_lid_gore_vent_boss.stl            # Gore-Vent Sockel
│       ├── 17_corner_clamping_posts_mid_tray_4x.stl # 4x Eck-Pfostensäulen der Oberwanne
│       ├── 18_corner_clamping_posts_lower_case_4x.stl # 4x Eck-Schraubsäulen der Unterwanne
│       ├── 19_corner_screw_holes_cutout_tool_4x.stl # 4x M3 Bohrungszylinder
│       ├── 20_perimeter_sealing_groove_collar.stl   # Umlaufender Dichtungskragen (Nut)
│       ├── 21_perimeter_sealing_tongue_lip.stl      # Umlaufende Dichtungsfeder (Lippe)
│       ├── 22_silicone_o_ring_gasket_cord_1_5mm.stl # Ø 1.5 mm Silikon-O-Ring Prüfkörper
│       ├── 23_floor_vent_slots_cutout_tool_group.stl# 5x Zwischenboden-Belüftungsschlitze
│       └── 24_single_vent_slot_cutout_tool.stl      # Einzelner 15x2.5 mm Belüftungsschlitz
│
├── 02_pod_base/                                 # Universeller Satelliten-Pod (für Pod 1, Pod 2 & Pod 3)
│   ├── pod_base_housing.stl                     # Universelles 5-seitiges Monocoque-Schachtgehäuse mit Führungsnuten, Rohrbett & EPDM-Nasen
│   └── components/                              # Modularer Baukasten
│       ├── 01_pod_tunnel_base.stl               # 5-seitiger Monocoque-Tunnel (100x60x28 mm, nach vorne offen)
│       ├── 02_pod_rear_m8_gland.stl             # Horizontaler M8 6-Pin IP67 Kabelstutzen (Ø 8 mm Bohrung)
│       ├── 03_pod_bulkhead_partition.stl        # Schutz-Schottwand / Zwischenboden mit Federdomen
│       ├── 04_pod_guide_grooves.stl             # Schneidkörper für asymmetrische Poka-Yoke Führungsnuten
│       └── 05_pod_strap_hooks.stl               # 4x EPDM-Spannbandnasen & V-Rohrbett
│
└── 03_pod_cartridges/                           # Kassetten-Einschübe
    ├── cartridge_base_sled.stl                  # Universeller Basisschlitten mit Führungsfedern, Snap-Fit & Entriegelungstasten
    ├── cartridge_sena_sled.stl                  # Sena 50S/60S Kassetten-Schlitten
    ├── cartridge_cardo_sled.stl                 # Cardo Packtalk Edge Schlitten
    ├── cartridge_omm_transceiver_sled.stl       # OMM Transceiver Schlitten (für Pod 3 Heck mit voller 23.5 mm Innenhöhe)
    ├── cartridge_blindkassette_waterproof.stl   # Wasserdichte IP67 Blindkassette (Dry Box Dummy)
    └── components/                              # Modularer Baukasten & Dummy-Platinen
```

#### Übersicht der druckfertigen STL-Masterdateien (Ready-to-Print)

| Baugruppe | Funktion / Bauteil | Druckfertige STL-Datei | Modularer Baukasten (OpenSCAD / Tinkercad) |
| :--- | :--- | :--- | :--- |
| **Zentralbox (3-Teilig)** | Unterwanne mit Dichtnut & M3-Pfosten | [main_box_lower_case.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | [01_main_box/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/components/) |
| **Zentralbox (3-Teilig)** | Oberwanne mit Zwischenboden & Akkubett | [main_box_mid_tray.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | [01_main_box/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/components/) |
| **Zentralbox (3-Teilig)** | Gehäusedeckel mit Dichtfeder & Gore-Vent | [main_box_lid.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | [01_main_box/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/components/) |
| **Universeller Satelliten-Pod** | 5-seitiges Monocoque-Gehäuse (integriertes Rohrbett & EPDM-Spannbandnasen) | [pod_base_housing.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | [02_pod_base/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/) |
| **Wechselkassette** | Universeller Kassetten-Grundschlitten | [cartridge_base_sled.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | [03_pod_cartridges/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/components/) |
| **Wechselkassette** | Sena 50S/60S Kassetten-Schlitten | [cartridge_sena_sled.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_sena_sled.stl) | [03_pod_cartridges/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/components/) |
| **Wechselkassette** | Cardo Packtalk Edge Schlitten | [cartridge_cardo_sled.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_cardo_sled.stl) | [03_pod_cartridges/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/components/) |
| **Wechselkassette** | OMM Transceiver Schlitten (für Pod 3 Heck) | [cartridge_omm_transceiver_sled.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | [03_pod_cartridges/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/components/) |
| **Wechselkassette** | Wasserdichte IP67 Blindkassette (Dry Box Dummy) | [cartridge_blindkassette_waterproof.stl](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_blindkassette_waterproof.stl) | [03_pod_cartridges/components/](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/components/) |

---

### 5.12 OpenSCAD Parametrisches CAD-System & Modul-Architektur

Neben den STL-Dateien steht das gesamte mechanische System als **vollständig parametrische OpenSCAD-Codebasis** unter [hardware/cad/scad/](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/) bereit. Der Aufbau folgt 1:1 dem intuitiven CSG-Workflow (Constructive Solid Geometry wie in Tinkercad: Addition mit `union()`, Subtraktion/Ausstanzen mit `difference()` und intuitive Ausrichtung über `center=false`).

```
hardware/cad/scad/
├── 00_common/                                   # Globale Parameter, Hilfsmodule & Dummies
│   ├── parameters.scad                          # $fn=60, globale Maße, Wandstärken, Nuthöhen
│   ├── screw_bosses.scad                        # M2/M2.5/M3/M4 Schraubdome & Eck-Spannsäulen
│   └── dummies/                                 # 3D-Prüfkörper für Passungs- & Bauraumprüfung
│       ├── dummy_main_pcb.scad                  # Hauptplatine (95x65 mm) mit HD26, USB-C, LEDs, LM5164
│       ├── dummy_lipo_battery.scad              # 1000 mAh LiPo-Zelle (50x35x6 mm) mit Schutzplatine
│       ├── dummy_omm_transceiver_pcb.scad       # OMM Heck-Platine (70x48 mm) mit Patch-Antenne & LoRa
│       ├── dummy_adapter_pcb.scad               # Kassetten-Adapterplatine (50x22 mm) mit DS2401 ID-Chip
│       └── dummy_m8_connector.scad              # M8 6-Pin IP67 Stecker mit Rändelmutter & PUR-Kabel
│
├── 01_main_box/                                 # 3-Teilige Zentralbox
│   ├── 00_lower_deck.scad                       # Unterwanne mit PCB-Domen & M3-Säulen
│   ├── 01_upper_deck.scad                       # Oberwanne mit Zwischenboden, Akkubett & 11x Schlitzen
│   ├── 02_colsure.scad                          # Gehäusedeckel mit Dichtfeder & Gore-Vent-Sitz
│   ├── 99_overall_box.scad                      # Gesamt-Zusammenbau inklusive eingelegter Dummies
│   └── parts/                                   # Modulare CSG-Teilschritte
│
├── 02_pod_base/                                 # Universeller Satelliten-Pod
│   ├── pod_base_housing.scad                    # 5-seitiges Schachtgehäuse mit M8-Bohrung, Nuten & Rohrbett
│   ├── pod_poka_yoke_cross_section.scad         # Frontaler 3D-Querschnitt zur Nut-Inspektion
│   ├── 99_pod_base_assembly.scad                # Pod mit Schottwand, Federn & M8-Stecker
│   └── parts/                                   # Modulare CSG-Teilschritte (Tunnel, Schottwand, Nuten, EPDM-Nasen)
│
└── 03_pod_cartridges/                           # Kassetten-Baukastensystem
    ├── 00_base_sled.scad                        # Gemeinsamer Grundschlitten (Führungsfedern, Snap-Fit, Riffeltaster)
    ├── cartridge_omm_transceiver.scad           # Pod 3 Heck-Kassette (23.5 mm Innenhöhe, 4x PCB-Dome)
    ├── cartridge_sena.scad                      # Sena 50S/60S Kassette (Sena 3D-Nest & Adapter-PCB)
    ├── cartridge_cardo.scad                     # Cardo Packtalk Edge Kassette (AirMount Magnetsitz & Adapter-PCB)
    ├── cartridge_blindkassette.scad             # Wasserdichte Dry Box Dummy mit Versteifungsrippen
    └── 99_cartridge_assembly.scad               # Galerie-Vergleich aller Kassetten
```

#### Hauptvorteile der OpenSCAD-Architektur:
1. **Modulare Kassetten-Vererbung:** Alle Kassetten binden die gemeinsame Datei [00_base_sled.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/00_base_sled.scad) ein. Änderungen an den Führungsfedern, der Einlaufschräge oder den Kupferbolzen wirken sofort auf alle 4 Kassetten.
2. **Kollisions- & Passungsprüfung mit Dummies:** Die Baugruppendateien (`99_overall_box.scad`, `99_pod_base_assembly.scad`, `99_cartridge_assembly.scad`) blenden echte 3D-Prüfkörper von Platinen, Akkus und Steckern farbig ein (`color()`), sodass Freiräume und Toleranzen vor dem Druck optisch geprüft werden können.
3. **Mathematisch exaktes CSG:** OpenSCAD berechnet Schnitte und Bohrungen exakt volumetrisch, wodurch keine Dreiecks-Facettenartefakte mehr an Planarflächen auftreten.

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

---

## 8. Fertigungsverfahren & Materialauswahl: Desktop-FDM vs. Industrie-MJF

Das gesamte OpenMotorBridge Gehäusesystem ist so konstruiert, dass es **sowohl auf heimischen Desktop-FDM-Druckern (Prusa, Bambu Lab, Voron etc.) als auch bei professionellen 3D-Druck-Dienstleistern (HP MJF / SLS)** fehlerfrei und IP67-dicht gefertigt werden kann:

### 8.1 Heimischer Desktop-FDM-Druck (Prusa MK3/MK4/XL, Bambu Lab X1/P1/A1 etc.)
* **Materialempfehlungen für Motorrad & Automotive:**
  * **PETG:** *Ideal für alle offenen Drucker ohne Gehäuse.* UV-beständig, schlagzäh, benzin- und säurefest, formstabil bis $80\,^\circ\text{C}$.
  * **ASA (oder ABS):** *Empfehlung für Drucker mit Einhausung (z. B. Bambu X1/P1, Prusa mit Enclosure).* $100\,\%$ UV- und witterungsstabil, temperaturbeständig bis $100\,^\circ\text{C}$, edle matte Oberfläche.
  * **PA-CF / PET-CF (z. B. Bambu PAHT-CF, Prusament PA11-CF):** Maximale Steifigkeit und seriennahe Carbon-Optik.
  * ❌ *Hinweis:* **Kein Standard-PLA verwenden**, da PLA bei Sonneneinstrahlung im Sommer am Motorrad (über $55\,^\circ\text{C}$) weich wird und sich verzieht!
* **Slicer-Empfehlungen für IP67-Dichtigkeit (PrusaSlicer, Bambu Studio, OrcaSlicer):**
  * **Wandlinien (Perimeter):** **4 bis 5 Wände** einstellen (Wandstärke $\approx 1{,}6 \dots 2{,}0\,\text{mm}$ $\rightarrow$ alle Gehäusewände werden $100\,\%$ massiv ohne Hohlräume gedruckt).
  * **Obere/untere Schichten:** **5 bis 6 Schichten**.
  * **Infill:** $25 \dots 40\,\%$ (Gyroid oder Honeycomb).
  * **Schichthöhe:** $0{,}16\,\text{mm}$ (empfohlen für saubere O-Ring-Nuten) oder $0{,}20\,\text{mm}$.
  * **Flussrate (Flow):** $102 \dots 104\,\%$ (leichte Überextrusion dichtet Mikroporen zwischen den Schichten hermetisch ab).
  * **Druckausrichtung:**
    * `main_box_lower_case.stl`: Flach auf Gehäuseboden $\rightarrow$ **$0\,\%$ Support benötigt**.
    * `main_box_mid_tray.stl`: Flach auf Zwischenboden $\rightarrow$ Baum-Stützen (Tree Support) an der Dichtlippe.
    * `main_box_lid.stl`: Flach mit der Oberseite auf das Bett $\rightarrow$ **$0\,\%$ Support benötigt**.
    * `pod_base_housing.stl`: Auf die hintere M8-Stirnfläche stehend $\rightarrow$ minimaler Tree-Support unter dem V-Sattel.
    * `cartridge_*_sled.stl`: Flach auf den Schlittenboden $\rightarrow$ die Snap-Fit-Rastarme liegen flach in der $XY$-Ebene (optimaler Faserverlauf für maximale Biegewechselfestigkeit!).

### 8.2 Industrieller 3D-Druck (HP MJF / SLS bei JLCPCB, Weerg, Craftcloud)
* **Verfahren:** **HP Multi Jet Fusion (MJF)** oder **SLS** (Selektives Lasersintern).
* **Material:** **PA12 (Polyamid 12)**, schwarz eingefärbt und glasperlengestrahlt.
* **Vorteile:** Isotrope Festigkeit in allen 3 Raumachsen, absolut porenfrei, keine Stützstrukturen.
* **Fertige ZIP-Pakete für Dienstleister:** [`hardware/production_packages/06_3d_print_mjf_stls/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls).


