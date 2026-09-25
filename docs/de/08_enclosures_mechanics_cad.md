# 08 - Mechanische Gehäuse, CAD-Konstruktion & Dichtungssystem (Alle Baugruppen)

Dieses Dokument spezifiziert die mechanische Konstruktion, das Thermomanagement, das IP67/IP69K-Gehäusedesign, die Kinematik des Auto-Eject-Schnellwechselsystems sowie alle CAD- und STL-Modelle aller Gehäuse-Baugruppen der OpenMotorBridge v8.0:
1. **Zentrale Steuerbox (Typ A):** 3-teiliges Sandwich-Gehäuse mit Zwischenboden, integrierter Akku-Wanne, stirnseitiger Schnittstellenleiste (HD26, USB-C, RGB-LED) und planarem 4-Layer Kupfer-Wärmespreader.
2. **Modulares Satelliten-Pod- & Wechselsystem (Typ B):** Baugleiches 5-seitiges Monocoque-Schachtgehäuse für alle 3 Satellitenpositionen (Pod 1 & 2 Audio/Intercom, Pod 3 Telemetrie/Backbone) mit modularen Wechselkassetten (OMM-Transceiver, Sena, Cardo, Midland, PMR446, Dry Box), $120^\circ$-V-Nut Rohrbett, Dual-Port M8/USB-C, Poka-Yoke Nut-und-Feder-Führung, federbelastetem Auto-Eject und unsichtbarem Neodym-Magnet-Diebstahlschutz.
3. **Universal Front-Knoten (Typ C):** Ultrakompakter Cockpit- & Sensor-Hub ($98{,}0 \times 68{,}0 \times 25{,}0\,\text{mm}$) für die vergrößerte $82 \times 50\,\text{mm}$ 4-Lagen PCBA 05 mit **4-in-1 Universal-Befestigungssystem** (AMPS, Rohrbügel-Prisma, Silentblöcke, 3M Dual-Lock), getrennten EPDM-Kabelkämmen für USB (Süd) und Fahrzeugleitungen (Nord), Dual-SW3526 20W USB-PD und Knowles MEMS Akustikkanal.
4. **2-in-1 LoRa Smart-Keyfob & Pager (Typ D):** Ultrakompakter Taschenbegleiter ($58{,}0 \times 34{,}0 \times 13{,}0\,\text{mm}$) aus PA12-MJF mit umlaufendem TPU-Kantenschutz, integriertem N52-Neodym-Auswerferschlüssel, $0{,}5\,\text{mm}$ Mu-Metall-Flussschirmung, MagSafe/Qi-Induktionsladeaufnahme, LRA-Haptikmotor und drahtlosem SX1262 LoRa/BLE Alarm-Pager.
5. **Fahrzeugspezifische Referenz-Montagekits (Zero-Drill):** Vollständig konstruierte, zerstörungsfreie Bolt-On Montagekits für CVO Road Glide ST (Kit 1), Road King Special (Kit 2), Classic Bagger & Cruiser (Kit 3) sowie Adventure & Touring Enduros (BMW GS, KTM Adventure, Africa Twin – Kit 4).

---

## 1. Gehäuse Typ A: Zentrale Steuerbox (3-Teiliges Sandwich-Design)

Das Basisgehäuse der Zentralbox ist als modulares, 3-teiliges IP67/IP69K-Sandwichgehäuse aus **PA12 (MJF-Verfahren)** oder **Aluminium-Druckguss** konzipiert, das speziell für raue Motorrad-Bedingungen (Vibrationen bis $20\,\text{g}$, Spritzwasser, Hitzestau unter der Sitzbank) ausgelegt ist:

- **Außenabmessungen:** $110{,}0 \times 74{,}0 \times 38{,}0\,\text{mm}$ (L x B x H; Unterwanne $17{,}0\,\text{mm}$, Oberwanne $15{,}0\,\text{mm}$, Deckel $6{,}0\,\text{mm}$).
- **Befestigung:** 4x integrierte Ecklaschen an der Unterwanne mit **Lochabstand $128{,}0 \times 56{,}0\,\text{mm}$** für schwingungsdämpfende **M4 Silentblöcke (Shore 50A EPDM)** zur Entkopplung hochfrequenter Motorvibrationen.
- **Lichte Innenmaße:** $102{,}0 \times 66{,}0 \times 32{,}0\,\text{mm}$ (optimiert für die $85{,}0 \times 55{,}0\,\text{mm}$ 4-Layer Hauptplatine).
- **Material & Fertigung:** PA12 im HP Multi Jet Fusion (MJF) 3D-Druck (min. $3{,}0\,\text{mm}$ Wandstärke), kugelgestrahlt, im Heißbad chemisch geglättet und hydrophob versiegelt.
- **Schutzart:** IP67 / IP69K (strahlwasser- und tauchdicht bis $1\,\text{m}$ Wassertiefe sowie dampfstrahlbeständig).

### 1.1 3D-CAD-Modell & 3-Schichten-Sandwichaufbau

![OpenMotorBridge Zentralbox 3D Anschnitt CAD](../images/cad/main_box_cutaway_3d.png)

*Abbildung 8.1: Photorealistischer 3D-CAD-Schräganschnitt der zentralen Steuerbox. Sichtbar sind die 3 Schichten im geschlossenen Verbund: Unterwanne mit 4-Layer-Platine (ENIG) auf M2.5 Dämpfern, Zwischenboden mit 11 Konvektionsschlitzen, oberes Akku-Fach mit 1S LiPo-USV-Batterie und EPDM-Spannband, HD26-Flansch, USB-C Servicekappe sowie Deckel mit Gore-Membran.*

![OpenMotorBridge Zentralbox 3-Teiliges Sandwich-Gehäuse IP67](../images/cad/main_box_enclosure_cad.png)

*Abbildung 8.2: 3D-CAD-Konstruktionsübersicht der zentralen Steuerbox (Typ A).*

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
│      - 1S LiPo-Pufferakku (68x39x5.0mm, 2.200 mAh)         │  │
│      - EPDM-Gummispannband zur vibrationsfesten Fixierung  │  │
│    • Zwischenboden (Optimierte Zirkulationsebene):         │  │
│      - 25,0 x 4,0 mm Kabeldurchbruchsschlitz               │  │
│      - 11x Konvektions- & Druckausgleichsschlitze          │  │
├────────────────────────────────────────────────────────────┤  │
│ 3. UNTERWANNE (17,0 mm Höhe - Geschlossene Monocoque-Wanne)│  │
│    • 4-Layer Hauptplatine (85 x 55 mm) auf M2.5 Dämpfern   │  │
│    • Integrierte M3 Sechskant-Nut-Pockets (IKEA-Prinzip)   │  │
│    • 4x M4 Silentblock-Befestigungsohren (vibrationsfest)  │  │
│    • 100% geschlossener PA12-Boden ohne Gehäusedurchbrüche │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.2 3D-Explosionsdarstellung & Schichtaufbau (1:1:1 CAD Fitting)

![OpenMotorBridge Zentralbox Exploded 3D CAD Fitting](../images/cad/main_box_full_assembly_exploded_3d.png)

*Abbildung 8.3: 1:1:1 euklidische CAD-Explosionsdarstellung der Zentralbox entlang der vertikalen Z-Achse.*

### 1.3 3D-Röntgenansicht & Zusammenbau-Fitting

![OpenMotorBridge Zentralbox Mated 3D X-Ray CAD Fitting](../images/cad/main_box_assembly_mated_3d.png)

*Abbildung 8.4: Transparente 3D-Röntgenansicht der vollständig geschlossenen Zentralbox. Erkennbar sind die spielfreien Bauteilfreiräume, die geschützte Akku-Lagerung auf dem Zwischenboden, die durchgängige Konvektion über die 11 Zwischenbodenschlitze und der scheuerfreie Kabelverlauf zum HD26-Flansch.*

### 1.4 Maßstabsgetreuer Längs- & Querschnitt (X-Z Thermik & Y-Z Kabelführung)

![OpenMotorBridge Zentralbox Cross Sections](../images/cad/main_box_assembly_cross_section.png)

*Abbildung 8.5: Exakte 2D-Schnittansichten der Zentralbox (X-Z und Y-Z Ebenen).*

---

## 2. Thermomanagement & Planare PCB-Entwärmung (Kupferbolzenfrei)

Die Gesamtabwärme der Zentralbox liegt im normalen Fahrbetrieb bei lediglich **$\approx 1{,}5\,\text{W}$** (Peak bei maximaler Schnellladung: $2{,}45\,\text{W}$).

```
       4-LAYER LEITERPLATTE (PLANARER KUPFER-WÄRMESPREADER)
┌────────────────────────────────────────────────────────┐
│ [ LM5164 Buck ]     [ BQ24075 UPS ]     [ ESP32-S3 ]   │ ◄── Bauelemente (SMD)
│   (100V DCDC)       (Power-Path)        (Dual-Core)    │
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 2: Durchgehende Solid GND Plane
├────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ ◄── Layer 3: Split Power / GND Planes
└──────────────────────────┬─────────────────────────────┘     (JLC04161H-7628 Standard, 93.5 cm² Fläche)
                           │
 ┌─────────────────────────▼─────────────────────────────┐
 │ 11x ZWISCHENBODEN-KONVEKTIONSSCHLITZE & INNENLUFT     │ ◄── Freie Zirkulation in 210 cm³
 │ (Wärme verteilt sich homogen im gesamten Gehäuse)     │     Luftvolumen & Gore ePTFE-Vent
 └─────────────────────────┬─────────────────────────────┘
                           ▼
          Abgabe über PA12-Gehäuseoberfläche (300 cm²) an Fahrtwind
```

1. **Planare 4-Layer PCB-Entwärmung ($85 \times 55\,\text{mm}$):** Die durchgehenden Kupfer-Innenlagen der FR4-Platine (JLC04161H-7628 Standard mit $17{,}5\,\mu\text{m}$ bzw. optional $35\,\mu\text{m}$) leiten die geringe Abwärme von $\approx 1{,}5\,\text{W}$ blitzschnell ab ($\lambda = 390\,\text{W/(m}\cdot\text{K)}$) und verteilen sie homogen über die gesamte Platinenfläche – ganz ohne mechanische Kühlkörper oder Kupferbolzen.
2. **11x Optimierte Konvektionsschlitze im Zwischenboden:** 5 Schlitze an der Rückkante ($Y = 58\,\text{mm}$), 4 an den Flanken und 2 an der Front lassen die Luft ungehindert in die Deckelkammer aufsteigen.
3. **Thermische Sicherheitsmargen im Extrem-Stresstest (Stau bei $45\,^\circ\text{C}$ Hitze + $13\,^\circ\text{C}$ Motorwärme = $58\,^\circ\text{C}$ unter Sitz):**
   * **LM5164-Q1:** $T_j = 93{,}8\,^\circ\text{C}$ (Zulässig bis $+150\,^\circ\text{C}$ $\rightarrow$ $+56{,}2\,^\circ\text{C}$ Reserve).
   * **ESP32-S3:** $T_j = 90{,}2\,^\circ\text{C}$ (Zulässig bis $+105\,^\circ\text{C}$ $\rightarrow$ $+14{,}8\,^\circ\text{C}$ Reserve).
   * **3.3V LDO:** $T_j = 110{,}4\,^\circ\text{C}$ (Zulässig bis $+125\,^\circ\text{C}$).
   * **1S LiPo Akku:** Verbleibt in der oberen Kammer sicher unter $60\,^\circ\text{C}$ (JEITA-NTC pausiert Ladevorgang bei $> 45\,^\circ\text{C}$).

### 2.2 Oberwanne: 1S LiPo-Akkuaufnahme & Zwischenboden-Durchführungen
* **Integrierte LiPo-Akkutasche:** Auf der Oberseite des Zwischenbodens sitzt eine formschlüssige Aussparung ($68{,}0 \times 39{,}0 \times 5{,}0\,\text{mm}$) für eine ultra-flache **2.200 mAh 1S LiPo-Pufferzelle** (Typ 504068 oder 503870). Durch die gezielte Vergrößerung der horizontalen Grundfläche statt der Bauhöhe bleibt die gesamte Gehäusehöhe der Zentralbox strikt bei **$38{,}0\,\text{mm}$**, sodass unter der Motorradsitzbank kein einziger Millimeter Freigang verloren geht.
* **100 % freier Querschnitt aller 11 Konvektionsschlitze:** Das Akkubett ist zentral bei $X = 17{,}0\dots 88{,}0\,\text{mm}$ und $Y = 13{,}0\dots 55{,}0\,\text{mm}$ platziert. Dadurch halten alle 11 Lüftungsschlitze (5 an der Rückwand, 4 an den Flanken, 2 an der Front) mindestens $2{,}5\dots 4{,}5\,\text{mm}$ Randabstand ein. Die Kaminwirkung und Innenluft-Zirkulation für die Abwärme von LM5164-Q1 und BQ24075 im Unterdeck bleibt uneingeschränkt erhalten.
* **Vibrationssicherung:** Eine $1{,}0\,\text{mm}$ dämpfende EPDM-Schaumstoffmatte an der Unterseite und ein quer verlaufendes EPDM-Gummispannband ($40 \times 12\,\text{mm}$) über seitliche Einhängenocken halten die Zelle auch bei $20\,\text{g}$ Stößen absolut spielfrei.
* **Molex Micro-Fit 3.0 Akkuanschluss (`J_BAT`):**
  * Pin 1: `VBAT+` ($+3{,}7\,\text{V}$ LiPo Pluspol über BQ24075)
  * Pin 2: `GND` (LiPo Masse mit integriertem Murata 10k NTC Temperaturfühler für JEITA-Ladeüberwachung)
* **Kabeldurchbruch & Zwischenboden-Führung:**
  * Großzügiger Front-Kabeldurchbruch ($25{,}0 \times 4{,}0\,\text{mm}$ bei $Y = 4\dots 8\,\text{mm}$) mit beidseitig verrundeten Kanten ($R = 1{,}5\,\text{mm}$) liegt $5{,}0\,\text{mm}$ vor der Akkutasche.
  * Führt die Akku-Silikonleitungen knickfrei nach unten auf den `J_BAT`-Header sowie das interne 2x13 Flachbandkabel von der Hauptplatine zum HD26-Flansch in der Stirnwand.

---

## 3. Stirnseitige Anschlüsse & Anzeige in der Oberwanne

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

1. **HD26 D-Sub Flansch:** Amphenol LTW / NorComp SEAL-D mit EPDM-Flachdichtung ($1{,}5\,\text{mm}$, Shore 60A).
2. **USB-C Service-Port:** Wasserdichte Buchse mit blau eloxierter Aluminium-Schraubkappe und O-Ring.
3. **RGB-Status-LED Sichtfenster:** Diffuser PMMA-Linsenkörper ($\varnothing\,3{,}0\,\text{mm}$) mit umlaufendem O-Ring.

---

## 4. Gehäusesystem Typ B: Universeller Satelliten-Pod & Modulare Wechselkassetten

OpenMotorBridge trennt das mechanische Gehäuse der Satelliten in zwei untrennbar aufeinander abgestimmte Systemkomponenten:
1. **Typ B (Pod-Basisschacht):** Ein zu 100 % baugleiches 5-seitiges Monocoque-Gehäuse ($135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$), das dauerhaft am Motorrad verbleibt (an Rahmenrohren, im Kofferdeckel oder am Heckbürzel).
2. **Typ C (Modulare Wechselkassette):** Ein universeller 2-teiliger Basisschlitten ($116{,}0 \times 58{,}0 \times 28{,}0\,\text{mm}$), der systemspezifische OEM-Funkgeräte (Sena 50S/60S, Cardo Packtalk Edge, Midland, PMR446) oder eine wasserdichte Dry Box aufnimmt und werkzeuglos eingeschoben wird.

![OpenMotorBridge Satelliten-Pod & Kassetten 3D Anschnitt CAD](../images/cad/pod_cartridge_cutaway_3d.png)

*Abbildung 8.6: Photorealistischer 3D-CAD-Schräganschnitt des Satelliten-Pods mit eingeschobener Wechselkassette. Gut zu erkennen sind die 120°-V-Nut mit EPDM-Spannringen um das Motorrad-Rahmenrohr, die M8 6-Pin-Buchse, die innere Schottwand mit den beiden komprimierten V4A-Edelstahlfedern, die asymmetrischen Poka-Yoke Gleitschienen mit 8 mm Höhenversatz, der 6-polige Goldkontakt-Eingriff (4,8 mm Wipe-Weg) und die formbündige Dichtung an der Frontblende.*

---

### 4.1 Gesamtsystem-Kinematik: Poka-Yoke, Auto-Eject & Unsichtbarer Magnet-Diebstahlschutz

Das Zusammenspiel von Pod-Schacht (Typ B) und Wechselkassette (Typ C) wird durch ein vollkommen gekapseltes, werkzeugloses und diebstahlgeschütztes Führungs- und Verriegelungssystem bestimmt:

#### 4.1.1 Asymmetrisches Poka-Yoke Nut-und-Feder Führungskonzept

![OpenMotorBridge Pod Poka-Yoke Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Abbildung 8.7: 3D-CAD-Querschnitt (Y-Z Ebene) durch das Satelliten-Pod-Gehäuse und den Kassetten-Grundschlitten. Sichtbar ist der $8{,}0\,\text{mm}$ Höhenversatz der Führungsnuten (Links: $Z=10{,}0\,\text{mm}$, Rechts: $Z=18{,}0\,\text{mm}$). Ein $180^\circ$-Falscheinbau ist mechanisch ausgeschlossen.*

* **Führungsgeometrie:** Die Führungsnuten an den Innenwänden des Pods und die Gegenfedern am Kassetten-Schlitten sind um $8{,}0\,\text{mm}$ vertikal versetzt. Ein versehentliches Einschieben auf dem Kopf ($180^\circ$-Verdrehung) ist physisch blockiert, bevor elektrische Kontakte berührt werden können.
* **Vorzentrierungs-Fase:** $30^\circ$-Einlaufschrägen verengen das seitliche Führungsspiel auf den ersten $80\,\text{mm}$ auf präzise $\pm 0{,}2\,\text{mm}$.

#### 4.1.2 Serienmäßiger Unsichtbarer Magnet-Diebstahlschutz (2-Arm-Wippe)

Um Wechselkassetten auf allen Motorrädern (von frei zugänglichen Reiseenduro-Sturzbügeln über Naked-Bikes bis zu Cruisern) wirksam gegen unbefugtes Herausziehen und Gelegenheitsdiebstahl zu sichern, verfügen **alle Pods und Kassetten serienmäßig** über einen unsichtbaren, magnetisch entsperrbaren Verriegelungsmechanismus (`parts/05_magnetic_lock_latch.scad`):

```
        MAGNETISCHER DIEBSTAHL-SCHUTZ: 2-ARM-WIPPE (KINEMATIK-SCHNITT)
═════════════════════════════════════════════════════════════════════════════════

                 POD-GEHÄUSEWAND (PA12-MJF, NICHT-MAGNETISCH)
 ─────────────────────────┬───────────────────────┬──────────────────────────────
  [EXTERNER NEODYM-KEY]   │                       │ [GEHÄUSE-FÜHRUNGSNUT]
   (Zielkreis bei X=64)   │                       │  (Rastkerbe bei X=88 mm)
            ▼             │                       │            ▲
      ┌───────────┐       │                       │            │ 90° Sperrflanke:
      │ NEODYM-   │       │                       │            │ blockiert Auszug!
      │ MAGNET N52│       │                       │            │
      └─────┬─────┘       │                       │            │
 ═══════════╪═════════════╪═══════════════════════╪════════════╪═════════════════
  KASSETTE  │             │                       │            │
            ▼ Zieht nach  │   M2 SCHWENKACHSE     │            ▼
      ┌───────────┐ außen!│    (DREHPUNKT)        │   ┌─────────────────┐
      │STAHLANKER ├───────┴─────────⊙─────────────┴───┤ SÄGEZAHN-KRALLE │
      │(Ø 6.2 mm) │   Hinterarm     │     Vorderarm   │ (30° Ein / 90°)|
      └─────┬─────┘   (X = 46 mm)   │    (X = 70 mm)  └─────────────────┘
            ▲                       │                          ▲
     [V4A-FEDER] █ Drückt           │                          │ Schwenkt nach
     (Normalst.)   nach innen       │                          │ innen frei!
```

![OpenMotorBridge Magnetischer Diebstahlschutz 3D CAD Kinematik](../images/cad/magnetic_anti_theft_lock_cad.png)

*Abbildung 8.8: Kinematische 3D-Schnittansicht des magnetischen Kassetten-Diebstahlschutzes (`98_magnetic_anti_theft_inspection.scad`). Erkennbar sind das transparente Pod-Gehäuse, der Schlitten mit 1. Klasse Wipphebel (grün), die 90°-Sägezahnkralle im Gehäuserasteingriff ($X = 88\,\text{mm}$), der $\varnothing\,6{,}2 \times 8\,\text{mm}$ Stahlanker mit V4A Rückstellfeder ($X = 46\,\text{mm}$), die M2 Edelstahl-Drehachse ($X = 58\,\text{mm}$) sowie die stirnseitigen V4A Auswerffedern.*

1. **Glatte, diebstahlsichere Kassettenfront:**
   * Äußere Squeeze-Tasten entfallen vollständig. Die Frontblende der Kassette schließt absolut glatt und spaltbündig mit dem Pod-Gehäuse ab. Ein manuelles Aushebeln per Hand oder mit Werkzeug ist ohne Zerstörung des Gehäuses unmöglich.
2. **Kinetische 2-Arm-Wippe (`parts/05_magnetic_lock_latch.scad`):**
   * Arbeitet als Hebel 1. Ordnung um eine rostfreie M2-Schwenkachse bei $X = 58\,\text{mm}$.
   * **Vorderer Arm ($X = 70\,\text{mm}$):** Trägt die $90^\circ$-Sägezahn-Rastkralle mit $30^\circ$-Einlaufschräge. Sie gleitet beim Einschieben federnd über die Schiene und rastet am Endanschlag formschlüssig in die Gehäusetasche bei $X = 88\,\text{mm}$ ein.
   * **Hinterer Arm ($X = 46\,\text{mm}$):** Trägt den eingepressten ferromagnetischen Stahlanker ($\varnothing\,6{,}2 \times 8\,\text{mm}$). Eine V4A-Druckfeder stützt sich gegen die innere Schlittenwand ab und hält die Sperrkralle im Ruhezustand permanent unter Verriegelung.
3. **Kontaktlose Neodym-Entriegelung & Taktiler Zielkreis:**
   * Auf der linken Gehäuseaußenwand von `pod_base_housing.scad` ist bei $X = 64\,\text{mm}$ ein taktiler Zielkreis ($\varnothing\,18\,\text{mm} \times 0{,}6\,\text{mm}$) eingelassen.
   * Nähert der Fahrer den [Smart-Keyfob](../../hardware/cad/scad/05_accessories/smart_keyfob_pager.scad) (oder einen N52-Magnetschlüssel) an diesen Zielkreis an, zieht das Magnetfeld den innenliegenden Stahlanker nach außen. Die Wippe schwenkt um die M2-Achse, zieht die Sperrkralle nach innen in den Schlitten und gibt die Rastung frei.
4. **Automatischer Federauswurf (Auto-Eject):**
   * Im selben Moment stoßen die beiden in der Schottwand sitzenden V4A-Druckfedern die Kassette definiert um **$15\dots 20\,\text{mm}$ nach vorne aus**, sodass sie bequem gegriffen und entnommen werden kann.
5. **Hermetischer Offroad- & Allwetterschutz:**
   * Keine offenen Gehäuseschlitze, Schieber oder Tastenöffnungen nach außen. Vollkommen resistent gegen Schlamm, Staub, Regen und winterlichen Frost.

| Parameter | Berechneter Wert | Funktion & Sicherheitsnachweis |
| :--- | :---: | :--- |
| **Federrate (2x V4A Auswerffedern)** | **$2{,}4\,\text{N/mm}$** | Parallelschaltung zweier Edelstahl-Druckfedern (DIN EN 13906-1) |
| **Vorspannfederweg** | **$6{,}0\,\text{mm}$** | Kompression von $L_0 = 15\,\text{mm}$ auf $L_{\text{mated}} = 9\,\text{mm}$ |
| **Axiale Haltekraft (Preload)** | **$7{,}2\,\text{N}$** | Hält Dichtsitz permanent unter Druck gegen $20\,\text{g}$ Vibration |
| **Dichtungs-Gegenkraft** | **$4{,}5\,\text{N}$** | $30\,\%$ Kompression der umlaufenden $1{,}5\,\text{mm}$ Silikon-Dichtschnur |
| **Auszugskraft (Verriegelung)** | **$> 120\,\text{N}$** | $90^\circ$-Formschluss sperrt Auszug zuverlässig gegen unbefugtes Ziehen |
| **Entriegelungsmagnetfeld** | **$B_r \ge 1{,}2\,\text{T}$ (N52)** | Kontaktlose Schwenkauslenkung der 2-Arm-Wippe am Zielkreis $X = 64\,\text{mm}$ |
| **Automatischer Auswurfhub** | **$15\dots 20\,\text{mm}$** | Trennt den $4{,}8\,\text{mm}$ 6-Pin Wipe mit großem Sicherheits-Überhub |

#### 4.1.3 Die 4 kinematischen Bewegungsphasen des Kassetteneinschubs

1. **Phase 1 - Vorzentrierung ($x = 0\dots 80\,\text{mm}$):** Die asymmetrischen Poka-Yoke Führungsrippen greifen in die Gehäusenuten ein. Das seitliche Spiel wird auf $\pm 0{,}2\,\text{mm}$ begrenzt.
2. **Phase 2 - Feder-Kompression ($x = 80\dots 86\,\text{mm}$):** Die Stirnseite des Schlittens trifft auf die beiden V4A-Auswerferfedern in der Schottwand und baut die $7{,}2\,\text{N}$ Vorspannkraft auf.
3. **Phase 3 - 6-Pin Kontakt-Eingriff & Schnapp-Rastung ($x = 86\dots 91\,\text{mm}$):** Die 6 Hartgold-Stifte dringen $4{,}8\,\text{mm}$ tief in die Doppelschenkel-Buchsenleiste ein (Wipe). Die $30^\circ$-Einlaufschräge der Sägezahnkralle drückt die Wippe federnd nach innen, bis sie bei $X = 88\,\text{mm}$ in die Gehäusekerbe schnappt.
4. **Phase 4 - Formbündige Verriegelung ($x = 91\,\text{mm}$):** Die $90^\circ$-Sperrkante verriegelt formschlüssig. Die umlaufende Silikon-Dichtung wird um $30\,\%$ komprimiert (IP67 Dichtsitz).

#### 4.1.4 Kontaktsicherheit & Wipe-Länge
* **Freie Stiftlänge:** $6{,}5\,\text{mm}$ Vierkant-Prägestifte ($0{,}64 \times 0{,}64\,\text{mm}$, $0{,}76\,\mu\text{m}$ Hartgold über Nickel).
* **Effektiver Wipe-Weg:** **$4{,}8\,\text{mm}$** Eingriff in die Buchsenleiste (übertrifft die USCAR-2 Kfz-Norm von $\ge 1{,}5\,\text{mm}$ um den **Faktor 3,2**).
* **Prellfreiheit:** $7{,}2\,\text{N}$ permanente Vorspannung verhindert Kontaktprellen selbst bei Vibrationen bis $20\,\text{g}$.

---

### 4.2 Gehäuse Typ B: Der universelle Satelliten-Pod (Pod 1, 2 und 3)

Alle 3 Pod-Positionen nutzen dasselbe 5-seitige Monocoque-Schachtgehäuse im standardisierten Envelope ($135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$):

![OpenMotorBridge Satelliten-Pod CAD Explosionsdarstellung](../images/cad/openmotorbridge_pod_exploded_view.png)

*Abbildung 8.9: 3D-CAD-Explosionsdarstellung des universellen Satelliten-Pods.*

![OpenMotorBridge Satelliten-Pod Röntgenansicht](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Abbildung 8.10: 3D-Röntgen- und Transparenzdarstellung des geschlossenen Satelliten-Pods.*

#### 4.2.1 Rohrbett-Prisma ($120^\circ$) & EPDM-Spannbefestigung
* **An der Unterseite:** $120^\circ$-V-Nut ($R = 15\,\text{mm}$) schmiegt sich formschlüssig an alle Rohre von $\varnothing 18\dots 35\,\text{mm}$ an ($1"$ Sturzbügel, $7/8"$ Heckrahmen).
* **4x Einhängenasen:** Blitzschnelle Montage mit 2 UV-beständigen EPDM-Gummiringen bei gleichzeitiger Schwingungsdämpfung.

#### 4.2.2 Dual-Port Anschluss-Architektur der Pod-Basis (Entflechtung & Koffer-Integration)

Um sowohl exponierte Outdoor-Einsätze (z. B. Sturzbügel-Montage bei Adventure-Bikes oder Heckradar Pod 3) als auch geschützte Koffer-Innenmontagen ohne selbstgelötete Adapterkabel abzudecken, verfügt die Pod-Bodenplatine ([`openmotorbridge_pod_base.kicad_pcb`](../../hardware/kicad_pod_base/openmotorbridge_pod_base.kicad_pcb)) über eine **Dual-Port-Architektur**:

```
                       POD-BASISPLATINE (DRAUFSICHT / LAYOUT)
 ┌────────────────────────────────────────────────────────────────────────┐
 │                                                                        │
 │   [ PORT A: M8 6-Pin ]                   [ PORT B: USB-C Slim ]        │
 │   (Outdoor / Heckradar)                  (Koffer / Innenmontage)       │
 │   Robuste Schraubbuchse                  Hinter TPU-Schutzstopfen      │
 │            │                                         │                 │
 │            └───► [ AUTOMATISCHER POWER-MUX / ] ◄─────┘                 │
 │                  [ IDEAL-DIODEN (LM66100)    ]                         │
 │                                │                                       │
 │                                ▼                                       │
 │                    [ SP3012 ESD-Array ]                                │
 │                                │                                       │
 │                                ▼                                       │
 │                    [ J1: Mill-Max 6-Pin Pogo ]                         │
 │                    (Zentriert zum Kassetten-Eingriff)                  │
 │                                                                        │
 └────────────────────────────────────────────────────────────────────────┘
```

1. **Mechanische Entflechtung von `J1` und `J2`:**
   * Aufteilung in **Port A (M8, links)** und **Port B (Slim-Port, rechts)** lässt die mittige Pogo-Pin-Leiste `J1` frei zugänglich.
2. **100 % Erhalt der Gehäuse- & Platinenabmessungen (Null Längenzuwachs):**
   * Die Pod-Basisplatine behält ihre kompakten Abmessungen von **$36{,}0 \times 20{,}0\,\text{mm}$** bei.
   * Das äußere 5-seitige Monocoque-Gehäuse verbleibt exakt im Envelope von **$135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$**.
   * **Port A Quadratischer Durchbruch ($11{,}5 \times 11{,}5\,\text{mm}$):** Die quadratische Buchsenbasis taucht vollständig durch die $3{,}5\,\text{mm}$ Wand nach außen; das M8-Messinggewinde liegt für die Überwurfmutter frei zugänglich außen.
   * **Planare Platinenabstützung (2x M2-Verschraubung an H1 & H2):** An der Schottwand bei $X = 18{,}0\,\text{mm}$ angeformte M2-Dome sichern die Platine absolut plan gegen Verkippen.
3. **Hardware-Arbitrierung (Prioritäts- & Rückspeiseschutz):**
   * Integrierter LM66100 Ideal-Dioden-Power-Multiplexer schaltet automatisch die aktive Versorgungsspannung durch.
4. **Axiale Ausrichtung & Eingelassene Stecktasche (Tiefenkompensation):**
   * Senkrechte USB-C-Buchse auf `B.Cu` taucht in eine **$7{,}0\,\text{mm}$ tiefe Stecktasche** ($14{,}0 \times 8{,}5\,\text{mm}$) mit $45^\circ$ Einlaufschräge und Dichtkragen ein.
   * Mechanischer Schlagschutz: Die Gehäusewand fängt sämtliche Biege- und Querkräfte des Kabels ab.
   * Bei Nichtnutzung von Port B versiegelt der formangepasste TPU-Stopfen ([`008_pod_base_usbc_cap_tpu.scad`](../../hardware/cad/scad/02_pod_base/parts/008_pod_base_usbc_cap_tpu.scad)) die Tasche hermetisch (IP67).
5. **Universelle Multi-Plattform-Nutzung (Begleitfahrzeug / Pkw-Cockpit / Werkbank):**
   * Über Port B kann derselbe Pod mit einem Standard-Slim-USB-C-Kabel im Begleitfahrzeug oder am PC-Prüfplatz betrieben werden.

---

### 4.3 Gehäuse Typ C: Modulare Wechselkassetten

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Abbildung 8.11: Die modularen Wechselkassetten-Varianten im Überblick: OMM Heck-Transceiver (vorne links), Sena 50S/60S Quick-Snap Cradle (vorne rechts), Cardo Magnetic Air Mount (hinten links) und wasserdichte IP67 Blindkassette (hinten rechts).*

#### 4.3.1 Benutzerzentrierte Plug & Play Docking-Architektur (0 Lötaufwand)
Um Signale vom 90°-abgewinkelten **JST-SH 1.0 mm 6-Pin SMD-Steckverbinder (`J2`)** sowie dem **8-Pin Mechatronik-Header (`J_ACT`)** auf der Kassetten-Trägerplatine (PCBA 03 Rev 2.0) verwechslungs- und knickfrei zu den Kontaktpunkten des jeweiligen Adapters zu führen, besitzt der Kassetten-Schlitten:
* **Geschützten Unterflur-Kabelkanal:** Im Boden des PA12-Schlittens ist eine **$1{,}5\,\text{mm}$ tiefe und $8{,}0\,\text{mm}$ breite Kabelführung** direkt unterhalb des Konturbetts integriert.
* **Zwischenboden-Durchführung:** Ein präziser **$10{,}0 \times 3{,}0\,\text{mm}$ Durchbruch mit beidseitig $R=1{,}0\,\text{mm}$ verrundeten Kanten** führt die Kabelstränge von Header `J2` und `J_ACT` auf der unteren Platine nach oben ins Nest.
* **Standardisierte Pin-Belegung am JST-SH 6P Header (`J2`) für Audio & Direct-DC:**

| Pin | Signal-Name | Funktion am Headset-Adapter | Sena SPIDER X Slim | Sena 50S/60S Pad | Cardo Edge Pad | Midland XT / PMR |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `VCC_DIRECT_DC` | Direct-DC Speisung (3.85V / 5V) | Akkustecker ⑧ (DC In) | Pin 2 (USB-5V) | Pin 2 (5V Charge)| 5V DC In |
| **2** | `GND` | Gemeinsamer Massebezug | Akkustecker ⑧ (GND) | Pin 1 (GND) | Pin 1 (GND) | Masse / Shield |
| **3** | `AUDIO_R+` | Audio Diff-Out + (zum Lautsprecher-In) | Lautsprecher ⑩ (Spk +) | Pin 4 (Spk R+) | Pin 3 (Spk +) | Speaker In + |
| **4** | `AUDIO_R-` | Audio Diff-Out - (Lautsprecher-Rückleiter)| Lautsprecher ⑩ (Spk -) | Pin 5 (Spk R-) | Pin 4 (Spk -) | Speaker In - |
| **5** | `MIC_IN+` | Audio Diff-In + (vom Mikrofon-Out) | Mikrofon ⑨ (Mic +) | Pin 6 (Mic +) | Pin 5 (Mic +) | Mic Out + |
| **6** | `RESERVE_IO` | Diagnose / Auxiliary / PTT | N/C | Pin 7 (Mesh-Btn)| N/C (Aux) | PTT Switch |

#### 4.3.2 OMM-Transceiver-Kassette & Telemetrie-Backbone (Pod 3)

Die OMM-Transceiver-Wechselkassette ([`cartridge_antenna_bracket_omm.scad`](../../hardware/cad/scad/03_pod_cartridges/parts/04_antenna_bracket_omm.scad) / [`cartridge_omm_transceiver.scad`](../../hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad)) bildet das datentechnische Rückgrat des OpenMotorBridge-Mesh-Netzwerks. Sie vereint den OMM-Transceiver, 868 MHz LoRa, 5.9 GHz V2X und Multi-GNSS (`PCBA 04`, ESP32-C3 32-Bit RISC-V Co-Prozessor, SX1262 LoRa, u-blox MAX-M10S mit $25 \times 25\,\text{mm}$ Groundplane und Bosch Sensortec BMI270 6-Achs-IMU) in geschützter Heckposition.

##### Mechatronische Neuerungen (Feedback-Optimierungen):
1. **Sensirion SHT40 Fahrtwind-Führung (Stauwärme-Schutz):**
   * Unter der Forged-Carbon-Hutze der Road Glide ST entsteht durch Motor- und Auspuffabwärme massive Stauwärme, die interne Temperatursensoren um bis zu $+8\dots 15\,^\circ\text{C}$ verfälschen würde.
   * `cartridge_antenna_bracket_omm.scad` integriert einen **abgedichteten rückwärtigen Kabelkanal**, durch den der Sensirion SHT40 Präzisionssensor zusammen mit dem Antennenkabel **nach außen in den echten Fahrtwind** (unter den Kennzeichenträger / Heckbalkon) geführt wird.
2. **5.9 GHz V2X Keramik-Patchantennenaufnahme (OpenTrafficMap):**
   * Neben LoRa und GNSS besitzt das dielektrische Radom eine formschlüssige $20 \times 20\,\text{mm}$ Schnappaufnahme für eine 5.9 GHz V2X Keramik-Patchantenne zum legalen, passiven Empfang von SPAT- und DENM-Sicherheitsmeldungen.

> [!IMPORTANT]
> **Architektonische Modularität (Typ-B-Unantastbarkeit):**
> Auch für den Heck-Transceiver bleibt das universelle Monocoque-Schachtgehäuse (Typ B, $135 \times 70 \times 38{,}0\,\text{mm}$) **zu 100 % baugleich und unverändert**. Der Heck-Pod 3 unterscheidet sich mechanisch nicht von den Intercom-Pods 1 und 2; er wird lediglich durch das Einschieben dieser OMM-Transceiver-Kassette mit integriertem dielektrischem Antennenradom konfiguriert. Die fahrzeugspezifische Adaption an Kotflügel, Gepäckbrücken oder Heckrahmen erfolgt ausschließlich über externe Montagekonsolen (siehe [Kapitel 6](#6-fahrzeugspezifische-referenz-montagekits-zero-drill--bolt-on)).

![Pod 3 Full Assembly Exploded 3D](../images/cad/pod3_full_assembly_exploded_3d.png)

*Abbildung 8.12: CAD-Explosionsdarstellung des Heck-Pods 3 mit Antennen-Radom, Platine und M8-Bajonettsockel.*

![Pod 3 Assembly Cross Section](../images/cad/pod3_assembly_cross_section.png)

*Abbildung 8.13: Längsschnitt durch den Heck-Pod 3 mit koaxial geschirmter Antennenkammer und $25 \times 25\,\text{mm}$ GNSS-Groundplane.*

---

#### 4.3.3 Sena 50S / 60S Kontur-Nest & Snap-Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Abbildung 8.14: CAD-Visualisierung der Sena 50S/60S Wechselkassette mit federnder 7-Pin Pogo-Kontaktleiste.*

#### 4.3.4 Mechatronische Smart Cartridge: Formschlüssige Arretierung & 4-Kanal Aktuator-Führung (Sena SPIDER X Slim & Cardo Packtalk Edge)
Für moderne Intercom-Kassetten wie das Sena SPIDER X Slim und das Cardo Packtalk Edge löst die Kassettenmechanik die doppelte Kernherausforderung: **Absolute Schwingungsfestigkeit des OEM-Adapters** und **präzise, dauerhafte Ausrichtung von 4 diskreten, unabhängig platzierten Aktuatoren auf die Tastenfelder**.

##### Universelle Aktuatoren-Architektur (`cartridge_universal_actuator_rails.scad`):
Um auch Headsets mit asymmetrischen, mittigen oder beidseitig gegenüberliegenden Tasten ohne Neukonstruktion mechanisch vollautomatisiert steuern zu können, wurde das universelle Schienen- und Rastersystem konstruiert:
1. **Top-Face 2D-Langloch-Rasterplatte ($3\,\text{mm}$ Raster):**
   * Die Deckelplatte besitzt eine 2D-Matrix aus verschiebbaren Langlöchern. Zylindrische Miniatur-Hubmagnete ($\varnothing 6{,}0\,\text{mm}$) können stufenlos exakt über der Taste positioniert und mit einer M2-Kontermutter fixiert werden.
2. **Unabhängige seitliche Ausleger-Arme (Lateral Brackets links & rechts):**
   * Bei Headsets mit Tasten auf beiden Seitenwänden (oder mittigen Wippen) greifen zwei separate, voneinander mechanisch entkoppelte Auslegerarme ein. Ein Arm bedient die linke Flanke, der andere die rechte Flanke.

```
     MECHATRONISCHE SMART CARTRIDGE – UNIVERSELLE RASTER- & AUSLEGER-FÜHRUNG
┌──────────────────────────────────────────────────────────────────────────────────┐
│ KASSETTEN-OBERDECKEL (cartridge_universal_actuator_rails.scad):                  │
│                                                                                  │
│   TOP-RASTER (2D-Langlochplatte):                 SEITLICHE AUSLEGER-ARME:       │
│   [ Aktuator 1 ]   [ Aktuator 2 ]   [ Aktuator 3 ]    [ Linker Arm ] [ Rechter Arm]│
│   (Verschiebbar     (Verschiebbar    (Verschiebbar    (Flanke links   (Flanke rechts│
│    in X- & Y-       in X- & Y-        in X- & Y-       unabhängig)     unabhängig)  │
│    3mm-Raster)      3mm-Raster)       3mm-Raster)                                   │
│         │                │                │                 │               │       │
│   ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐     ┌─────┴─────┐   ┌─────┴─────┐ │
│   │Feder 0,15N│    │Feder 0,15N│    │Feder 0,15N│     │Feder 0,15N│   │Feder 0,15N│ │
│   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘     └─────┬─────┘   └─────┬─────┘ │
│         ▼                ▼                ▼                 ▼               ▼       │
│   ┌───────────┐    ┌───────────┐    ┌───────────┐     ┌───────────┐   ┌───────────┐ │
│   │Vertikal-  │    │Vertikal-  │    │Vertikal-  │     │Seiten-    │   │Seiten-    │ │
│   │Führung H8 │    │Führung H8 │    │Führung H8 │     │Führung H8 │   │Führung H8 │ │
│   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘             └─────┬─────┘      │
│         │ (TPU)          │ (TPU)          │ (TPU)                   │ (TPU)      │
│         ▼ (0,4mm)        ▼ (0,4mm)        ▼ (0,4mm)                 ▼ (0,4mm)    │
├─────────┼────────────────┼────────────────┼─────────────────────────┼────────────┤
│ OEM INTERCOM GEHÄUSE (Im vibrationsdämpfenden EPDM-Konturbett):                  │
│         ▼                ▼                ▼                         ▼            │
│   [ Taste 1 ]      [ Taste 2 ]      [ Taste 3 ]               [ Taste 4 / Wheel ]│
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 3-Punkt EPDM-Dämpfungseinlagen (60° Shore A, 1,5 mm) gegen 20g Vibration     │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│ KASSETTEN-UNTERTEIL MIT MONOCOQUE-VERRIEGELUNG (PA12-MJF Negativkontur)          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

* **1. Diskrete, flexible Aktuator-Architektur:**
  * Anstelle eines starren 4er-Kammblocks setzt OpenMotorBridge auf **4 miniaturisierte Einzel-Aktuatoren** (Hubmagnete mit Federrückstellung und dämpfender TPU-Druckspitze), die jeweils über ein flexibles 2-poliges AWG30-Silikonkabel an den 8-Pin Header `J_ACT` von PCBA 03 angeschlossen werden.
  * Dadurch kann das Inlay des Kassettenoberteils für jedes Intercom-Modell maßgeschneidert werden:
    * **Sena SPIDER X Slim:** 3 Aktuatoren axial von oben auf die Tastenreihe (Plus, Center, Minus) sowie 1 Aktuator in einem $45^\circ$-Winkelturm auf der Seitenflanke zur Betätigung der exponierten Mesh-Intercom-Taste.
    * **Cardo Packtalk Edge:** 3 Aktuatoren auf die drei Haupttasten (Media, Mobile, Intercom) sowie 1 Aktuator zur axialen Betätigung des integrierten Tasters im Control Wheel (Center-Press). Ein mechanisches Drehen des Rades im Fahrbetrieb entfällt, da Lautstärke und Gain volldigital über den ES8388 DSP in der Zentralbox geregelt werden.
  * **Mechanische Befestigung via Niederhalteplatte:** Die Aktuatoren werden von innen in die monolithischen Führungsdome geschoben und durch eine gemeinsame, mit 4x M2-Senkkopfschrauben verschraubte PA12-CF-Halteplatte mit $1{,}0\,\text{mm}$ EPDM-Dämpfungsunterlage vibrationsfest und spielfrei auf ihren Bund gepresst.
  * **Anti-Pinch-Kabelführung:** Entlang der Schlitteninnenwand sind vertiefte $1{,}8 \times 2{,}0\,\text{mm}$ Führungskanäle mit angeformten Halteclips integriert. Die hochflexiblen AWG30-Silikonlitzen des 8-Pin Y-Kabelbaums werden darin vollkommen knickfrei und quetschgeschützt von `J_ACT` zu den 4 Aktuatoren geführt.

* **2. Formschlüssiges Negativbett & Vibrationssicherung gegen $20\,\text{g}$ Shock:**
  * **Präzisions-Passung:** Die Aufnahmeschale bildet das OEM-Gehäuse des SPIDER X Slim ($74{,}5 \times 31{,}0 \times 16{,}0\,\text{mm}$) mit einer Passungstoleranz von $0{,}2\,\text{mm}$ im SLS/MJF-Verfahren ab.
  * **3-Punkt EPDM-Schwingungsentkopplung:** Drei profilierte EPDM-Dämpfungspolster ($60^\circ$ Shore A, Dicke $1{,}5\,\text{mm}$) am Boden und an den Stirnflanken absorbieren hochfrequente Motorvibrationen ($50\dots 500\,\text{Hz}$) sowie Stoßbelastungen bis $20\,\text{g}$ (nach ISO 16750-3).
  * **Formschlüssige Schnellspann-Klammer (Quick-Clamp):** Ein schwenkbarer Niederhaltebügel mit unverlierbarer M3-Rändelschraube presst den OEM-Adapter mit definierter Haltekraft ($15\dots 20\,\text{N}$) spielfrei und unbeweglich in das Nest. Ein Verrutschen oder Klappern während der Fahrt ist physikalisch ausgeschlossen.

* **3. Präzisions-Führungsbrücke & Zuverlässiges Treffen der Gegenstelle:**
  * **Monolithische Führungsbuchsen:** Im Kassetten-Deckel sind vier hochpräzise Führungszylinder ($\varnothing\,3{,}2\,\text{mm}$, Passung H8) direkt eingesintert.
  * **Fluchtende Achsausrichtung:** Jeder Zylinder fluchtet exakt zentrisch über der entsprechenden OEM-Gummitaste (`ACT_PLUS`, `ACT_MINUS`, `ACT_CENTER`, `ACT_MESH`) mit einer Achsabweichung von $< \pm 0{,}15\,\text{mm}$.
  * **TPU-/Silikon-Druckkappen (Shore 70A):** Die Stößelspitzen tragen elastische Kappen mit leicht balliger Stirnfläche. Sie verhindern Abrutschen auf der gewölbten Gummitaste, gleichen Bauteiltoleranzen aus und schützen die Original-Tastenbeschichtung vor Reibverschleiß.
  * **Integrierte Rückstellfedern (Edelstahl 1.4310):** Jede Stößelachse wird durch eine Spiralfeder ($c \approx 0{,}15\,\text{N/mm}$) in Ruhelage gehalten. Ein definierter Freihub von $0{,}4\,\text{mm}$ ("Luftspalt") stellt sicher, dass selbst extreme Fahrbahnstöße niemals zu einem ungewollten Berühren oder Drücken der Taste führen.
  * **Mechanischer Endanschlag ($1{,}1 \pm 0{,}1\,\text{mm}$):** Die Betätigungstiefe ist mechanisch begrenzt. Der interne Mikrotaster schaltet sicher durch, eine Überlastung oder Quetschung der internen SMD-Taster auf der Headset-Platine wird zuverlässig verhindert.

* **4. Knickfreie Zugentlastung der Kabelpeitsche:**
  * Im Kassettenboden führen drei separate Führungskanäle die werkseitige Kabelpeitsche des SPIDER X Slim (DC-Power ⑧, Mikrofon ⑨, Lautsprecher ⑩) über großzügig gerundete Radien ($R \ge 5\,\text{mm}$) direkt zu den Buchsen `J2` und `J_ACT` auf PCBA 03 Rev 2.0.

![OpenMotorBridge Mechatronische Smart Cartridge Sena SPIDER X Slim 3D CAD Fitting](../images/cad/smart_cartridge_spider_x_cad.png)

*Abbildung 8.14b: CAD-Visualisierung der mechatronischen Smart Cartridge Rev 2.0 für Sena SPIDER X Slim: Formschlüssiges PA12-MJF Konturbett, 3-Punkt EPDM-Schwingungsdämpfung gegen 20g Vibration, Niederhaltebügel und monolithische Führungsbrücke mit 4 unabhängigen Tauchanker-Aktuatoren auf PCBA 03.*

#### 4.3.5 Sena +Mesh & Universal Slide-Inlay (Klasse A mit externem Antennenanschluss)
Für das Sena +Mesh (oder andere OEM-Adapter mit Antennen- und Ladeanschluss) bietet die Kassetten-Frontblende (`00_base_sled.scad` & `01_insert_sena.scad`):
* **100 % zerstörungsfreie Nutzung des ungeöffneten OEM-Geräts:** Das Sena +Mesh wird im Originalgehäuse belassen.
* **Formschlüssiges Schlitten-Inlay:** Bildet exakt die OEM-Rahmenbefestigungsplatte mit 2x Quer-Schiebestegen (Hakenabstand $30\,\text{mm}$) und federnder Rastzunge ab.
* **Integrierte SMA-Flansch-Bohrung ($\varnothing\,6{,}5\,\text{mm}$):** Mit zylindrischer O-Ring-Dichtsenkung ($\varnothing\,9{,}5 \times 1{,}2\,\text{mm}$) an der Deckelstirnseite für eine IP67 SMA-Flansch-Doppelbuchse (Female-to-Female).
* **Interner Koax-Kabelkanal:** Ausgesparter Durchbruch im Schlittenboden für die biege- und knickfreie Führung des internen $8\,\text{cm}$ RG-178 Pigtails (mit 90°-SMA-Winkelstecker zum Sena +Mesh).
* **EPDM-Spannband-Aufnahme:** Einhängehaken für ein elastisches EPDM-Gummiband ($35 \times 10\,\text{mm}$), das den Adapter vibrationsfest im Negativbett sichert.
* **Elektrische Speisung:** Flaches 90° Micro-USB / USB-C Pigtail von Pin 1 (`GND`) und Pin 2 (`5V_VBUS`) des JST-SH Headers `J2`.

#### 4.3.6 Cardo Packtalk Edge / Pro Magnetic Air Mount
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Abbildung 8.15: CAD-Visualisierung der Cardo Packtalk Edge Wechselkassette mit N52-Neodym-Magnetsitz und 5 gefederten Kontaktpads.*

#### 4.3.7 Cardo Packtalk Bold / Black Edition
Nutzt die formschlüssigen Schiebe-Gegenkontakte der originalen Cardo-Audiokit-Basisplatte. Das Gerät wird von oben in die mechanische Führung geschoben und federnd arretiert.

#### 4.3.8 Midland BT Mini / BTR1 Advanced & XT30 Slide
* **Midland Intercom Edition (BTR1 / Rush / BT Mini):** Kontur-Aufnahme für Midland Bluetooth- und Wave-Mesh-Intercoms ($70\dots 85\,\text{mm}$ Baubreite).
* **Midland XT Bare-Board Edition:** Nimmt die entkernte Platine eines kompakten Handfunkgeräts (XT10/XT30/G5, $\approx 68 \times 42 \times 10\,\text{mm}$) direkt auf.

#### 4.3.9 PMR446 Transceiver & Bare-Board Modul (SA818S / RDA1846)
Vollständig integriertes 500 mW PMR446-Analogfunkmodul ($38 \times 20\,\text{mm}$) direkt auf der Kassetten-Trägerplatine – wahlweise mit interner 446-MHz-Helix oder robuster SMA-Frontbuchse für große Distanzen.

#### 4.3.10 Längsschnitt-Vergleich Sena & Cardo
![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Abbildung 8.16: 2D-Längsschnitt (X-Z Ebene) durch die Sena 50S (oben) und Cardo Packtalk Edge (unten) Kassetten im geschlossenen Pod.*

#### 4.3.11 IP67 Blind- / Leerkassette (Dry Box Dummy)
![OpenMotorBridge IP67 Blindkassette 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

*Abbildung 8.17: Formidentische IP67 Blindkassette mit integriertem $80 \times 46 \times 16\,\text{mm}$ Notfall-Trockenstaufach.*

Die IP67 Blindkassette (`cartridge_blindkassette.scad`) schützt den Pod-Schacht zuverlässig, wenn kein Intercom montiert ist:
* **Identischer Verriegelungs- & Auswurfmechanismus:** Auch die Blindkassette verfügt über die standardisierte 2-Arm-Magnetwippe (`parts/05_magnetic_lock_latch.scad`), Poka-Yoke-Führungsschienen und Federtaschen für die V4A-Auswerferfedern. Sie verriegelt mit demselben satten Klick und wird kontaktlos über den N52-Magnetschlüssel ausgeworfen.
* **Hermetischer Steckerschutz (EPDM-Dichtblock):** An der Rückseite dichtet ein integrierter EPDM-Formblock die 6-Pin Kontaktleiste auf PCBA 02 absolut wasser- und staubdicht ab.
* **Notfall-Trockenstaufach:** Der $80 \times 46 \times 16\,\text{mm}$ große Innenraum dient als wasserdichte Mini-Dry-Box für Fahrzeugschein, Bargeld, Notfallschlüssel oder Ersatz-O-Ringe.

---

### 4.4 Belegung der 6-Pin M8 / Pogo-Schnittstelle & PUR-Kabelbaum-Farbcodierung

| M8 / Pogo-Pin | Leitungsfarbe (PUR-Kabel) | Querschnitt | Signal Pod 1 & 2 (Audio & Intercom) | Signal Pod 3 (Heck-Transceiver) | Schirmung & Verdrillung |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Pin 1** | **Rot (RD)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`VCC`** (5V geschaltete Speisung via MOSFET) | **`VCC`** (5V Versorgung) | Einzelader (Power) |
| **Pin 2** | **Schwarz (BK)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) | Einzelader (Power Ground) |
| **Pin 3** | **Weiß (WH)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_P`** (Symmetrisches Audio + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Box) | **Paar 1 verdrillt** (mit Pin 4) |
| **Pin 4** | **Blau (BU)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_N`** (Symmetrisches Audio - via Bourns) | **`UART_RX`** (Box $\rightarrow$ Heck-Co-Prozessor) | **Paar 1 verdrillt** (mit Pin 3) |
| **Pin 5** | **Gelb (YE)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`TRIGGER_PPS`** (Single-Wire UART / Opto-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal) | Einzelader (Steuersignal) |
| **Pin 6** | **Grün (GN)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`1-WIRE_ID`** (Native Emulation / DS2401 ID) | **`1-WIRE_ID`** (Heck-Kassetten-ID) | Einzelader (1-Wire Bus) |
| **M8-Gehäuse**| **Kupfergeflecht (BL)**| $> 85\,\%$ Geflecht | **`GND_SHIELD`** (360° Gehäuseschirmung) | **`GND_SHIELD`** (360° Gehäuseschirmung) | Gesamtschirm über M8-Metallkragen |


---

## 5. Gehäuse Typ C: Universal Front-Knoten (Cockpit- & Sensor-Hub)

Das Gehäuse des Front-Knotens wurde speziell für die geschützte Montage in Motorrad-Frontverkleidungen (Batwing, Sharknose, BMW GS/RT Schnabel) oder an Sturzbügeln entwickelt:

- **Außenabmessungen:** Kompakte **$98{,}0 \times 68{,}0 \times 25{,}0\,\text{mm}$** (L x B x H, passend für die $82 \times 50\,\text{mm}$ 4-Lagen PCBA 05).
- **Material:** HP Multi Jet Fusion (MJF) PA12, schwarz kugelgestrahlt und chemisch geglättet.
- **Schutzart:** IP67 (tauch- und strahlwasserdicht) mit integrierter Gore-Tex Druckausgleichsmembran (ePTFE Vent) gegen Kondenswasserbildung.

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Abbildung 8.18: Geschlossenes Front-Node IP67-Gehäuse.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Abbildung 8.19: 3D-Explosionsdarstellung des Front-Knotens entlang der Z-Achse.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Abbildung 8.20: Transparente 3D-Schnittansicht des Front-Knotens mit Knowles MEMS Schallkanal und VBUS-Lastschalter.*

### 5.1 Das 4-in-1 Universal-Befestigungssystem des Front-Knotens

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Abbildung 8.21: Gehäuseunterseite des Front-Knotens mit AMPS-Bohrbild, $120^\circ$ V-Nut Rohrbett, EPDM-Spannnasen, Silentblock-Lochungen und 3M Dual-Lock Klettnuten.*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   DAS 4-IN-1 UNIVERSAL-BEFESTIGUNGSSYSTEM (BODENANSICHT)               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. AMPS-LOCHBILD (30 x 38 mm):                                                         │
│    • 4x formschlüssige DIN 934 M4 Nut-Pockets im AMPS-Raster (100 % lötkolbenfrei!)   │
│    • Kompatibel mit allen RAM-Mount Kugeladaptern, Garmin-Haltern & Cockpitstreben     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. ROHRBÜGEL-PRISMA (120° V-Nut):                                                      │
│    • Integrierte Hohlkehle passend für Rohrdurchmesser von Ø 22 mm bis Ø 32 mm         │
│    • 4x Einhängenasen für 2x wetterfeste EPDM-Spannringe (BMW GS / Sturzbügel)         │
│    • 100 % werkzeuglose Schnellmontage ohne Lackkratzer                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. SILENTBLOCK-SCHWINGUNGSENTKOPPLUNG:                                                 │
│    • Eckbohrungen für M4 Silentblöcke (Shore 50A EPDM)                                 │
│    • Isoliert hochfrequente Vibrationen im Verkleidungsschnabel von Einzylinder- / V2  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. 3M DUAL-LOCK KLETTNUTEN:                                                            │
│    • 2x eingefräste 20 mm Nuten für selbstklebendes 3M Dual-Lock Pilzkopfband          │
│    • Perfekt für ebene Kunststoff-Innenflächen in Batwing- oder Sharknose-Verkleidungen │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Schnittstellen- & Flankenlayout des Front-Knotens

Die Anordnung der Steckverbinder und Durchführungen an den Gehäuseflanken ist exakt auf das vergrößerte 4-Layer-Platinenlayout der PCBA 05 ($82 \times 50\,\text{mm}$, `openmotorbridge_front_node.kicad_pcb`) und die Cockpit-Kabelführung abgestimmt:

```
                               FRONT-KNOTEN FLANKEN- & SCHNITTSTELLENLAYOUT
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                 HINTERSEITE / NORDKANTE (Y = 68 mm)                                         │
│                      (6-fach EPDM-Dichtkamm für Bordnetz, Sensorik & Antenne: north_epdm_cable_comb)                         │
│   U.FL Antenne     J9: Spiegel-BSD     J3: Lenker-PTT     J1: 12V KL15     J10: Qi-Lader     J11: Aux-Licht     J2: CAN-Bus │
│   (2.4 GHz ESP)    (3-Pin Radar LED)   (4-Pin Taster)     (2-Pin Zündung)  (2-Pin 12V Sw)    (2-Pin Scheinw)    (3-Pin CAN) │
├──────────────────────────────────────┬─────────────────────────────────────────────────┬────────────────────────────────────┤
│ LINKE SCHMALSEITE / WEST (X = 0 mm)  │              INNENRAUM (PCBA 05, 82 x 50 mm)    │ RECHTE SCHMALSEITE / OST (X = 98)  │
│                                      │                                                 │                                    │
│ • Vollwandiges MJF PA12 Monocoque-   │ • ESP32-S3-WROOM-1-N16R8 Dual-Core MC           │ • J7: Wasserdichte USB-C Service-  │
│   Gehäuse (0 Durchbrüche)            │ • USB2514B Automotive 4-Port USB 2.0 Hub        │   Buchse mit TPU-Dichtstopfen      │
│ • Schirmt interne Leistungsschaltung:│ • Dual SW3526 Synchron-Buck USB-PD (2x 20W)     │ • J12: Qwiic / Stemma QT I2C Port  │
│   - D4: SMCJ24CA 24V TVS-Diode       │ • 2x L2 & L3 geschirmte Speicherdrosseln        │ • SW1 (Boot) & SW2 (Reset) Taster  │
│   - U3 / L1: TPS54302 5V/3A Buck     │ • U3: TPS54302 5V System-Buck-Converter         │ • LED1: WS2812B RGB-Status-LED     │
│   - U6: TCAN334G CAN-Transceiver     │ • MIC1: Knowles SPH0645 I2S MEMS-Mikrofon       │   (Polycarbonat-Lichtleiter-Dom)   │
│   - K1: CPC1017N CAN Auto-Sensing    │ • K1: CPC1017N 120 Ohm Bus-Terminierungs-Relais │                                    │
│   - Q2: DMP3017SFG Verpolschutz      │ • Q1: DMN63D8LDW Spiegel-BSD Treiber-Stufe      │ • M4/M5 Silentblock-Flanschohr     │
│ • M4/M5 Silentblock-Flanschohr       │ • U4: TPS2051B USB-Power-Gate für Port 2        │   (Mitte Y = 34.0 mm, Z = 0..5 mm) │
│   (Mitte Y = 34.0 mm, Z = 0..5 mm)   │ • U7: TLV75533P 3.3V Ultra-Low-Noise LDO        │                                    │
├──────────────────────────────────────┴─────────────────────────────────────────────────┴────────────────────────────────────┤
│                                                 VORDERSEITE / SÜDKANTE (Y = 0 mm)                                           │
│                         (6-fach EPDM-Dichtkamm für Cockpit- & USB-Kabel: south_epdm_cable_comb)                             │
│   J4: USB Host       J5: Phone 20W PD    J6: CP2AA Dongle   J5_MP3: 20W PD + MP3     J6_AUX: Dashcam    J8: Action-Cam 5V   │
│   (Upstream Skyline) (Downstream 1, 5P)  (Downstream 2, 4P) (Downstream 3, 5P Data)  (Downstream 4, 4P) (2-Pin Switched 5V) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Vorderseite / Südflanke ($Y = 0\,\text{mm}$):**
   - **6-fach EPDM-Dichtkamm (`south_epdm_cable_comb`):** Führt USB- und Ladeleitungen vibrations- und zugentlastet durch eine 70 mm breite Dichtkammer nach vorne zum Cockpit:
     - `J4` ($X_{\text{tub}} = 23{,}25\,\text{mm}$): JST-GH 4-Pin Upstream USB 2.0 Verbindung zum Motorrad-Infotainment (Harley Skyline OS / Boom! Box GTS).
     - `J5` ($X_{\text{tub}} = 37{,}00\,\text{mm}$): JST-GH 5-Pin Downstream Port 1 zum Smartphone am Lenker mit **20W USB-PD Fast Charging (5V/3A, 9V/2.22A, 12V/1.67A)** via Synchron-Buck-Controller `U5` (SW3526) und Hochstrom-Speicherdrossel `L2`. Unterstützt USB-PD 3.0, QC 3.0/4.0+, AFC und FCP für unterbrechungsfreies Schnellladen auch bei Navigation unter voller Sommersonne.
     - `J6` ($X_{\text{tub}} = 48{,}50\,\text{mm}$): JST-GH 4-Pin Downstream Port 2 mit 25–30 cm Fairing-Pigtail zum thermisch entkoppelten CP2AA Wireless CarPlay / Android Auto Dongle (Ottocast / Carlinkit, befestigt per 3M Dual-Lock im Verkleidungshohlraum).
     - `J5_MP3` ($X_{\text{tub}} = 61{,}75\,\text{mm}$): JST-GH 5-Pin Downstream Port 3 ins Handschuhfach / Media-Bay. **Dual-Rolle:** Vollwertiges **20W USB-PD Fast Charging** via `U8` (SW3526) und Speicherdrossel `L3` für Powerbanks, Zweithandy oder Kamera-Akkus PLUS **High-Speed USB 2.0 Datenverbindung** zum USB2514B Hub für lokale MP3/FLAC Musik-USB-Sticks und offizielle Firmware-Updates.
     - `J6_AUX` ($X_{\text{tub}} = 73{,}25\,\text{mm}$): JST-GH 4-Pin Downstream Port 4 als freier Cockpit-Datenport für Dashcam, Chigee AIO-5 Display, Garmin Zūmo oder Reifendruck-Sensorempfänger.
     - `J8` ($X_{\text{tub}} = 80{,}75\,\text{mm}$): JST-GH 2-Pin geschaltete 5V/1.5A Spannungsversorgung für Helm- oder Verkleidungs-Action-Cam (GoPro / Insta360).
2. **Hinterseite / Nordflanke ($Y = 68{,}0\,\text{mm}$):**
   - **6-fach EPDM-Dichtkamm (`north_epdm_cable_comb`):** Führt Fahrzeug- und Sensorleitungen durch eine 58 mm breite Dichtkammer nach hinten zum Rahmentunnel:
     - `J9` ($X_{\text{tub}} = 33{,}50\,\text{mm}$): JST-GH 3-Pin Totwinkel-Spiegelwarnleuchten (Radar BSD links / rechts getrennt geschaltet über Dual-MOSFET `Q1` DMN63D8LDW).
     - `J3` ($X_{\text{tub}} = 43{,}25\,\text{mm}$): JST-GH 4-Pin digitaler Lenkertaster (PTT Gruppenfunk, Cam-Bookmark, Media-Voice-Taste, Masse).
     - `J1` ($X_{\text{tub}} = 54{,}75\,\text{mm}$): JST-GH 2-Pin 12V Zündungsplus (KL15) Speisung mit Verpolschutz-PMOS `Q2` (DMP3017SFG) und 24V SMCJ24CA TVS-Diode `D4`.
     - `J10` ($X_{\text{tub}} = 61{,}75\,\text{mm}$): JST-GH 2-Pin 12V geschaltete Speisung für induktive Handy-Ladehalterungen (SP Connect / QuadLock Wireless Charging Head, Ruhestrom 0.0 µA im Standby).
     - `J11` ($X_{\text{tub}} = 68{,}75\,\text{mm}$): JST-GH 2-Pin 12V geschalteter Hilfsausgang für Adventure-Zusatzscheinwerfer oder Notbrems-Stroboskop.
     - `J2` ($X_{\text{tub}} = 75{,}75\,\text{mm}$): JST-GH 3-Pin Automotive CAN-Bus (CAN_H, CAN_L, GND) mit TCAN334G Transceiver `U6` und elektronischem $120\,\Omega$ Bus-Terminierungs-Relais `K1` (`CPC1017N`).
   - **U.FL 2.4 GHz Antennenauslass:** Koaxialer U.FL Anschluss auf PCBA 05 führt zur externen 2.4 GHz Dipol- oder Patchantenne für störungsfreie ESP-NOW / BLE Funkverbindung zur Zentralbox unter der Sitzbank (vollkommen unbeeinflusst von der Fairing-Elektronik).
3. **Rechte Schmalseite / Ostflanke ($X = 98{,}0\,\text{mm}$):**
   - **Service & Diagnose:** IP67 wasserdichte USB-C Service-Buchse (`J7`, $Y_{\text{tub}} = 24{,}1\,\text{mm}$) mit formschlüssigem TPU-Schutzstopfen (`front_node_usbc_cap_tpu.stl`) zum direkten Flashen, Debuggen und Protokoll-Auslesen ohne Gehäuseöffnung.
   - **Sensor-Bus:** 4-Pin JST-SH Qwiic / Stemma QT $I^2C$-Erweiterungsport (`J12`, $Y_{\text{tub}} = 34{,}05\,\text{mm}$) für BME280 Umweltsensorik oder Cockpit-IMU.
   - **Taster:** Taktile Miniaturtaster `SW1` (Boot) und `SW2` (Reset) für MCU-Wartungsarbeiten.
   - **Visuelle Statusanzeige:** Polycarbonat-Lichtleiter im Gehäusedeckel für die **WS2812B RGB-Status-LED** (`LED1`, $Y_{\text{tub}} = 40{,}05\,\text{mm}$): Grün = OK / Normalbetrieb, Blau = BLE/ESP-NOW Link aktiv, Gelb = USB-Enumeration / CP2AA Dongle Boot, Rot = CAN-Fehler / Failsafe.
   - **Flanschbefestigung:** M4/M5 Silentblock-Flanschbefestigungslasche in der Flankenmitte ($Y_{\text{tub}} = 34{,}0\,\text{mm}$, $Z = 0\dots 5\,\text{mm}$).
4. **Linke Schmalseite / Westflanke ($X = 0\,\text{mm}$):**
   - **Monocoque-Schutzwand:** Vollwandiges MJF PA12 Monocoque ohne Gehäusedurchbrüche. Bietet maximalen mechanischen Schutz und Spritzwasserschutz für die direkt dahinter liegende Leistungsschaltung (TVS-Diode `D4`, 12V-Haupt-Buck-Converter `U3` TPS54302 mit Induktivität `L1`, CAN-Transceiver `U6`, Optorelais `K1`, PMOS-Verpolschutz `Q2`).
   - **Flanschbefestigung:** Symmetrische M4/M5 Silentblock-Flanschbefestigungslasche in der Flankenmitte ($Y_{\text{tub}} = 34{,}0\,\text{mm}$, $Z = 0\dots 5\,\text{mm}$).
5. **Gehäuseunterseite ($Z = 0\,\text{mm}$):**
   - Knowles SPH0645LM4H-B $I^2S$ MEMS-Mikrofon (`MIC1`) mit durchgehendem Schallkanal ($\varnothing\,2{,}5\,\text{mm}$) und wasserdichter, ölabweisender Gore ePTFE-Schutzmembran ($\varnothing\,6{,}0 \times 0{,}8\,\text{mm}$) zur Echtzeit-Windgeräusch- und Staudruckanalyse für dynamische Geschwindigkeits-/Geräusch-Lautstärkeanpassung (Speed-Volume-Control).

---

---

## 6. Fahrzeugspezifische Referenz-Montagekits (Zero-Drill / Bolt-On)

Während die 5 Hardware-Gehäuse (Typ A bis E) zu **100 % universell und einheitlich standardisiert** sind, liefert OpenMotorBridge für ausgewählte Motorradplattformen komplett durchentwickelte, schraub- und klebefreie Referenz-Montagekits. Diese nutzen originale Werksbefestigungspunkte oder elastische Spannsysteme, um das Gesamtsystem ohne Lackschäden oder irreversible Karosseriebohrungen perfekt ins Fahrzeug zu integrieren.

---

### 6.1 Referenz-Kit 1: Harley-Davidson CVO Road Glide ST (2024+) & New Touring Platform

Für High-Performance Bagger mit werkseitiger Einzelsitzbank und Forged-Carbon-Hutze (FLTRXSTSE):
Aufgrund der werkseitigen Showa Inverted-Remote-Reservoir-Stoßdämpfer mit dicken Hydraulikleitungen und des neuen 2024er Heckabschlusses scheiden externe Strut-Konsolen mechanisch aus. Das ST-Referenzkit integriert die 5 Knoten daher zu 100 % unsichtbar und zerstörungsfrei:

```
          CVO ROAD GLIDE ST (2024+) GESAMTSYSTEM-INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Vorne, unsichtbar hinter Außenhaut):                            │
│    • Front-Node (PCBA 05) + Ottocast am Alu-Geweihträger montiert           │
│    • 12V Zündungsplus direkt vom internen Fairing-Zubehörstecker            │
│    • Funkverbindung (ESP-NOW) zur Zentralbox -> 0 Kabel über den Lenkkopf   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MITTE (Unter Sitzbank):                                                  │
│    • Zentralbox mittig im Batteriefach                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. HECK (Unter Forged Carbon Hutze & Kennzeichen):                          │
│    • Pod 3 aufrecht im Skeleton Dock (cvo_st_undercowl_skeleton_dock.scad)  │
│      Gegen Fahrbahnschläge nach oben verspannt, 0 Bohrungen, 0 Lackkleber   │
│    • Externe 2.4 GHz Telemetrie-Finne (cvo_st_telemetry_fin.scad) am Tab    │
│    • Radar mittig unter dem Kennzeichen (radar_license_plate_bracket.scad)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. KOFFER (Gruppenfunk-Brücke Sena & Cardo):                                │
│    • Pod 1 (Sena Mesh) im linken Kofferdeckel                               │
│    • Pod 2 (Cardo DMC) im rechten Kofferdeckel                              │
│    • Montage an originalen Scharnier-/Fangbandschrauben (Zero-Drill)        │
│    • Kabelführung am Fangband, wetterfeste Schnellkupplung außen am Spalt   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### A. Heck-Integration: Das Under-Cowl Skeleton Dock & Telemetrie-Finne
* **Skeleton Dock (`cvo_st_undercowl_skeleton_dock.scad`):** Nimmt das Standard-Pod-3-Gehäuse ($135 \times 70 \times 38{,}5\,\text{mm}$) aufrecht auf. Zwei nach oben gewölbte Federbögen stützen sich an der Innendecke der Carbonhutze ab und verhindern jedes Aufbäumen oder Klappern über Schlaglöchern und Kopfsteinpflaster.
* **Telemetrie-Finne (`cvo_st_telemetry_fin.scad`):** Sitzt auf der originalen hinteren Schraublasche der Hutze. Sie führt die 2,4-GHz-Mesh-Antenne des Heck-Pod-3-Transceivers nach draußen an die frische Luft und leitet das Koaxialkabel unsichtbar unter der Lasche in die Hutze.

![CVO ST Under-Cowl Skeleton Dock CAD](../images/cad/cvo_st_undercowl_skeleton_dock_cad.png)

*Abbildung 8.22: 3D-CAD-Ansicht des Under-Cowl Skeleton Docks (`cvo_st_undercowl_skeleton_dock.scad`). Monolithische Halbschale mit nach oben gewölbten Federbögen zur Abstützung an der Innendecke der Carbonhutze, seitlichen Dämpfungsflügeln und formschlüssigem Einschubschacht für Pod 3.*

![CVO ST Telemetry Fin CAD](../images/cad/cvo_st_telemetry_fin_cad.png)

*Abbildung 8.23: 3D-CAD-Modell der externen 2,4-GHz-Telemetrie-Finne (`cvo_st_telemetry_fin.scad`). Aerodynamisch geformte Finne zur Montage auf der werksseitigen Hecklasche der Forged-Carbon-Hutze mit geschützter Koaxialkabel-Durchführung und Knickschutz.*

![Pod 3 Fender Assembly ST 3D](../images/cad/pod3_fender_assembly_st_3d.png)

*Abbildung 8.24: Fotorealistische Gesamtheck-Montage an der CVO Road Glide ST: Unsichtbare, rüttelfeste Integration von Pod 3 im Skeleton Dock unter der Forged-Carbon-Hutze, strömungsgünstige Telemetrie-Finne auf der Hecklasche und vollständige Freigängigkeit zu den Showa Inverted-Remote-Reservoirs.*

#### B. Kofferdeckel-Integration: Pod 1 (Links) & Pod 2 (Rechts)
* **Top-Lid Montage:** Beide Pods sitzen im vorderen Drittel der Kofferdeckel, verschraubt an den originalen Torx-Punkten der Scharnier- bzw. Fangbandhalterung (siehe [Abschnitt 6.5](#65-universal-kofferdeckel-dock-saddlebag_lid_dockscad)).
* **Gepäck- und Getränke-Sicherheit:** Liegen ca. $30\,\text{cm}$ über dem Kofferboden. Schwere Kaltgetränke, Werkzeug oder feuchte Kleidung am Boden liegen vollständig unterhalb der Funk-Fresnel-Zone.
* **Maximale HF-Isolation ($> 40\,\text{dB}$):** Sena (links) und Cardo (rechts) sind über $60\,\text{cm}$ voneinander getrennt, mit Heckfender und Rahmen als HF-Schild.

---

### 6.2 Referenz-Kit 2: Harley-Davidson Touring, Bagger & Cruiser (Road King Special, Street Glide, Electra Glide)

Für klassische Touring- und Bagger-Modelle mit 2-Up-Komfortsitzbank oder freiem Heckkotflügel bietet OpenMotorBridge eine universelle, formvollendete Kotflügel-Integration:

```
        HARLEY-DAVIDSON TOURING & BAGGER GESAMTSYSTEM-INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Nacelle / Batwing / Sharknose):                                 │
│    • Front-Node (PCBA 05) im Hohlraum der Headlight-Nacelle oder Verkleidung │
│    • Speist Garmin Navi / Smartphone-Halterung & Action-Cam am Lenker       │
│    • PTT-Lenkertaster & Knowles Windgeräusch-Mikrofon                       │
│    • 100 % drahtlos via ESP-NOW zur Zentralbox -> 0 Kabel am Tank nach hinten│
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MITTE (Unter Sitzbank):                                                  │
│    • Zentralbox mittig im Batteriefach                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. HECK (Kotflügel-Konsole & Kennzeichen):                                  │
│    • Pod 3 in der Touring Fender Console oder Touring Stealth Console       │
│      Formvollendet auf Kotflügel geschraubt an 1/4"-20 Soziussitz-Mutter    │
│    • Radar mittig unter dem Kennzeichen                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. KOFFER:                                                                  │
│    • Pod 1 (Sena) & Pod 2 (Cardo) in den Kofferdeckeln                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

Die Kotflügel-Integration ist in zwei aerodynamisch optimierten Ausführungen verfügbar, die beide die originale $1/4"-20$ Rändelmutter der Soziussitz-Befestigung im Kotflügel nutzen und das M8-Signalkabel unsichtbar nach vorne unter die Sitzbank leiten:

#### Option A: Touring Fender Console (`pod3_touring_fender_console.scad` / RKS & Naked Touring)
Organische Tropfenform ($R = 6\dots 7\,\text{mm}$), die das Pod 3 formschlüssig aufnimmt und speziell auf den freiliegenden Heckfender der Road King Special (FLHRXS) und Bagger abgestimmt ist:

##### Geometrische Überarbeitung (Feedback-Optimierungen):
* **Längserstreckung & Wandhöhe:** Die hintere Spitze wurde von $X = +160\,\text{mm}$ auf **$X = +205\,\text{mm}$ gestreckt** und **durchgehend auf die volle Seitenwandhöhe ($Z = 34\,\text{mm}$)** gezogen.
* **Spaltschluss:** Der zuvor vorhandene Montagespalt zwischen den langen Flankenwänden und der hinteren Spitze wurde vollständig geschlossen. Die Konsole bildet einen monolithischen, nahtlosen Karosseriekörper.
* **Geschützte 2.4 GHz Antennenkammer:** Die echte externe 2.4 GHz Dipolantenne sitzt formschlüssig in einer strömungsgünstigen, dielektrischen Schutzkammer in der verlängerten Spitze.
* **Konsolen-Vereinheitlichung (Ein einziger Grundkörper):** Die überarbeitete Fender-Konsole fungiert als **universeller Standard-Grundkörper** für alle Touring-Bikes. Sie kann wahlweise offen (für maximale Kassetten-Zugänglichkeit) oder mit formschlüssigem Deckel gefahren werden. Eine separate, verkürzte Stealth-Variante ist somit obsolet.

![Pod 3 Touring Fender Console CAD](../images/cad/pod3_touring_fender_console.png)

*Abbildung 8.25: Isolierte 3D-CAD-Ansicht der Touring Fender Console (`pod3_touring_fender_console.scad`) für Road King Special. Organisch fließende Tropfenform mit gestreckter Heckspitze ($X = +205\,\text{mm}$), geschlossenen Spalten und Heck-Einschuböffnung für Pod 3.*

![Pod 3 Touring Fender Console CAD Underside](../images/cad/pod3_touring_fender_console_cad.png)

*Abbildung 8.26: Unterseite der Touring Fender Console CAD: Konkav gewölbter 195-mm-Kotflügel-Sattel, vordere $1/4"-20$-Schraublasche für die Soziussitz-Mutter und vertiefter Kabelkanal zur scheuerfreien Durchführung des M8-Kabels unter die Sitzbank.*

---

### 6.3 Referenz-Kit 3: Adventure & Touring Enduros (BMW GS / GSA, KTM Adventure, Africa Twin)

Für großvolumige Reiseenduros und Offroad-Tourer mit offenem Gitterrohr-Heckrahmen, Rohrgepäckbrücke und optionalem Aluminium-3-Koffersystem (z. B. Touratech Zega Pro/Evo, BMW Adventure oder Wunderlich):

![OpenMotorBridge Adventure-Kit Master Assembly 3D Studio](../images/cad/adventure_kit_master_assembly_3d.png)
*Abbildung 8.29: Photorealistisches 3D-CAD-Studio des modularen Adventure-Kits (`99_adventure_kit_assembly.scad`). Links: GSA Rohrträger-Klemmschelle im geschützten Rahmendreieck (Pod 1 & Sena). Mitte: Standard-GS Transition Dock in der Sitzbank-Bügelfalte (Pod 2 & Cardo). Rechts: Gepäckbrücken-Ausleger "Heck-Balkon" hinter Alutopcase mit 45°-Astabweiser-Finne für die 2.4 GHz Dipolantenne, Pod 3 Transceiver und Garmin Varia Radar mit 36-Zahn Hirth-Formschluss-Gelenk.*

```
            ADVENTURE BIKE (BMW GS / KTM / AFRICA TWIN) INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Windschild / Navigationsstrebe / Schnabel):                     │
│    • Front-Node (PCBA 05) via AMPS-Bohrbild (30 x 38 mm) an Navigationsstrebe│
│      oder vibrationsentkoppelt mit M4 Silentblöcken im Schnabel             │
│    • Direkte Speisung von Garmin Navi / Smartphone & Action Cam am Lenker   │
│    • Knowles MEMS Mikrofon misst turbulenten Windpegel hinter der Scheibe    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MITTE (Unter Fahrersitz / Batteriefach):                                 │
│    • Zentralbox spritzwassergeschützt im Batteriefach / Werkzeugraum        │
│    • Abgriff Bordnetz-Dauerplus (Kl. 30), Zündungsplus (Kl. 15) und CAN-Bus │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. VORDERER HECKRAHMEN / SEITENBEREICH (Kassetten-Pods 1 & 2):             │
│    • Variante A (GSA & Heavy Duty): An der Innenseite der Rundrohr-         │
│      Kofferträger (Ø 18 mm) im geschützten Rahmendreieck ("Überrollkäfig")  │
│    • Variante B (Standard-GS ohne Koffer): Im "Transition Dock" unter der   │
│      Sitzbank in der optischen "Bügelfalte" am Fahrer-/Sozius-Übergang       │
│    • Raumdiversität > 45 cm; 100 % frei von Koffer-Abschattung nach oben/vorn│
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. HECK (Gepäckbrücken-Ausleger "Heck-Balkon" hinter Alu-Topcase):          │
│    • Universeller "Rack-Tail Mount" an Gepäckbrücke hinter Topcase-Rückwand │
│    • Pod 3 horizontal mit freiem 140°-Zenit-Blick (u-blox MAX-M10S GNSS)   │
│    • Integrierter 2.4 GHz Antennen-Astabweiser (+5 dBi Stabantenne geschützt│
│      in PA12-CF Gleitrippe mit 45°-Abweiser gegen Ast-Abriss im Unterholz)  │
│    • Schwenkbarer M5-GoPro-Radarausleger unten für Garmin Varia mmWave      │
│      (in 90..95 cm Höhe optimal vor Steinschlag/Roost und Wasser geschützt) │
│    • Topcase bleibt in 5 Sekunden per Original-Schnellverschluss abnehmbar  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 6.4.1 Kassetten-Pods 1 & 2 (Seitenmodule) – Die zwei Montage-Varianten

Auf Reiseenduros existieren je nach Einsatzzweck und Koffersystem zwei grundverschiedene Fahrzeughecks. OpenMotorBridge bietet dafür zwei perfekt abgestimmte Montagevarianten:

* **Variante A: BMW F850 GSA / R 1200 / R 1250 / R 1300 GS Adventure & Heavy-Duty Rohrträger (Touratech, Givi Outback, Hepco&Becker): Das "GSA Cage Dock"**
  * **Montage:** An den Innenseiten der massiven $\varnothing 18\,\text{mm}$ Edelstahl-Kofferträger im geschützten Rahmendreieck über das hochbelastbare **GSA Cage Dock** ([`adventure_gsa_cage_dock.scad`](../../hardware/cad/scad/02_pod_base/adventure_gsa_cage_dock.scad)).
  * **Design-Philosophie (Expedition Armor + Stealth Niche):**
    Kombiniert die unzerstörbare Optik professioneller Rallye- & Expeditions-Ausrüstung (analog zu den bekannten Touratech GSA-Werkzeugboxen) mit einer vollständigen Nischen-Integration: Der Pod wandert tief in den ca. $45\,\text{mm}$ breiten, sonst ungenutzten Totraum zwischen Alukoffer-Wand und Heckrahmen/Radkasten.

![OpenMotorBridge GSA Cage Dock Detailansicht](../images/cad/gsa_cage_dock_cad.png)

*Abbildung 8.29-A: CAD-Detailansicht des Heavy-Duty GSA Cage Docks (`adventure_gsa_cage_dock.scad`). Zu sehen sind der tief eingelassene Sena 50S Pod 1 im schützenden PA12-CF-Panzerkäfig, die breite 85 mm Doppel-Rohrsattelbasis für Ø 18 mm Edelstahlrohre mit 4x M5 V4A-Verschraubung und DIN 985 Stoppmuttertaschen, die 45°-Schotter-Abweiserkeile gegen Steinschlag vom Hinterrad sowie die verdeckte M8-Kabelrinne im Rohrschatten.*

  * **Konstruktionsmerkmale & Vorteile:**
    1. **Doppel-Halbschalen-Klemmung mit 85 mm Stützbasis:** Statt einer einfachen Einzelschelle greift das Cage Dock mit zwei getrennten $\varnothing 18\,\text{mm}$ Rohrsätteln über eine Spannweite von $85\,\text{mm}$ am Trägerrohr an. Dadurch werden Dreh- und Kippmomente durch Hebelkräfte selbst bei extremen Pisten-Vibrationen (> 120 Nm Torsionssteifigkeit) zuverlässig eliminiert.
    2. **4x M5 V4A-Verschraubung mit verdeckten Sicherungsmuttern:** 4x M5 DIN 912 Zylinderschrauben spannen die Kappe ([`adventure_gsa_clamp_cap.stl`](../../hardware/cad/stl/02_pod_base/adventure_gsa_clamp_cap.stl)) fest an den Korpus. Auf der Rückseite arretieren integrierte Sechskanttaschen DIN 985 Stoppmuttern verliersicher gegen Rütteln.
    3. **Stealth-Integration im Alukoffer-Totraum (100 % unsichtbar von außen):** Bei eingehängtem Aluminiumkoffer ist der Pod von außen zu 100 % verdeckt. Es existiert keinerlei Kollision mit Verriegelungsmechanismen, Kofferpilzen oder Deckelspannern.
    4. **Integrierter Steinschlag-Gleitkeil (Roost Protection):** Zur Radseite hin schützt eine $45^\circ$ geneigte, $3{,}5\,\text{mm}$ dicke Panzerfront aus kohlefaserverstärktem Polyamid (PA12-CF) den Pod und die Antenne vor aufgewirbeltem Grobschotter, Schlamm und Spritzwasser.
    5. **Verdeckter M8-Kabelkanal:** Das M8-Kabel verlässt die Rückseite der Docking-Wanne geschützt im Schatten des Trägerrohrs und führt ohne Schlaufenbildung direkt unter die Sitzbank.
    6. **HF-Sichtfeld:** Die Antenne strahlt ungehindert durch das offene Rahmendreieck nach vorn-oben zur Fahrerposition ab.
    7. *(Minimalistische Alternative:)* Für besonders beengte Rohrrahmenverläufe stehen weiterhin die kompakten Halbschellen ([`adventure_pannier_rack_clamp_base.stl`](../../hardware/cad/stl/02_pod_base/adventure_pannier_rack_clamp_base.stl) / `cap.stl`) zur Verfügung.

* **Variante B: Standard-BMW GS und nackte Reiseenduros (ohne Rohr-Kofferträger)**
  * **Montage:** Über ein zweiteiliges, aerodynamisch skulpturiertes **Transition Dock** ([`adventure_transition_dock.scad`](../../hardware/cad/scad/02_pod_base/adventure_transition_dock.scad)) in Kombination mit einer verdeckten **Unter-Sitzbank-Sattelbrücke** ([`adventure_underseat_cross_rail.scad`](../../hardware/cad/scad/02_pod_base/adventure_underseat_cross_rail.scad)).
  * **Positionierung:** Exakt in der optischen "Bügelfalte" am Übergang von der Fahrer- zur Soziussitzbank entlang des $\varnothing 28\,\text{mm}$ Heckrahmenrohrs.

![OpenMotorBridge GS Transition Dock & Unter-Sitzbank-Sattelbrücke](../images/cad/adventure_transition_dock_cad.png)

*Abbildung 8.29-B: CAD-Detailansicht des GS Transition Docks mit Unter-Sitzbank-Sattelbrücke. Zu sehen sind das zweitteilige Konsolengehäuse (Unterteil mit Rohrsattel und Oberteil mit formbündigem Karosserie-Deckel entlang der Bügelfalten-Lichtkante), der eingelassene Cardo Packtalk Edge Pod 2 sowie die flache, U-verrippte Sattelbrücke (`adventure_underseat_cross_rail.scad`), die links und rechts unter der Sitzbank durch verbindet, Hebelkräfte als starres U-Portal neutralisiert und das M8-Kabel unsichtbar ins Batteriefach leitet.*

  * **Vorteile & Konstruktionsmerkmale:**
    1. **100 % Verdrehsicherheit durch Unter-Sitzbank-Sattelbrücke:** Statt ein Gehäuse wackelig an einem einzelnen Rundrohr zu klemmen, verbindet eine flache PA12-CF-Traverse ($7{,}5\,\text{mm}$ flaches U-Profil) die linke und rechte Flanke unter der Sitzbankschale zu einem verwindungssteifen U-Portal.
    2. **Zero-Drill & 100 % unsichtbare Befestigung von außen:** Keine Schellen, Kabelbinder oder Schraubenköpfe am sichtbaren Rahmenrohr. Die Verschraubung erfolgt an vorhandenen OEM-Befestigungspunkten (Batteriefach / Quersteg) geschützt im Trockenen unter der Sitzbank.
    3. **Formschlüssige Bügelfalten-Integration & Karosserie-Deckel:** Wie bei der Touring Fender Console bildet das Dock keinen offenen Kasten, sondern eine geschlossene, aerodynamische Rahmenblende. Die Trennfuge liegt exakt in der scharfen Bügelfalten-Lichtkante; der $22^\circ$-Einlaufkeil vorn schließt bündig an den Fahrersitz an (kein Hängenbleiben beim Aufsteigen oder bei Knieschluss).
    4. **Integrierte Stecker-Servicebucht & verdeckte Unter-Sitzbank-Kabeldurchführung:**
       * **Hohlraum im 22°-Einlaufkeil:** Vor der Pod-Stirnwand ($X = 0$) befindet sich im vorderen aerodynamischen Keil eine $24 \times 50 \times 26\,\text{mm}$ große, hohle **Stecker- und Service-Bucht**. Hier finden der M8-Industrie-Schraubstecker (oder 90°-Winkelstecker) und eine spannungsfreie Kabelschlaufe vollständig Platz.
       * **Formschlüssiger Inboard-Kabelkanal:** An der fahrzeuginneren Flanke der Service-Bucht sitzt eine ovale Durchgangsöffnung (Ø 10 mm), die direkt unter dem überhängenden Schaumstoff der Sitzbank ins Innere des Rahmens / Batteriekastens mündet. Alternativ kann das Kabel durch die Unterseiten-Rinne der Sattelbrücke geführt werden.
       * **Bequeme "Top-Access"-Montage:** Bei abgenommenem Karosserie-Deckel wird das M8-Kabel von innen durchgeschoben und bei voller Bewegungsfreiheit von oben auf Port A des Pods geschraubt. Anschließend wird der Pod einfach in die Wanne gelegt und der Deckel mit 4x M3 Torx verschraubt – **100 % unsichtbar, scheuerfrei und ohne Gefummel im Verborgenen**.
    5. **100 % unabhängig von Koffersystemen:** Funktioniert auch dann perfekt, wenn das Motorrad komplett "nackt" ohne Träger, mit Vario-Koffern oder mit leichten Soft-Bags / Hufeisen-Taschen gefahren wird.
    6. **Freie Abstrahlcharakteristik:** Ungestörte $180^\circ$-HF-Sichtachse zur Seite und schräg nach oben zum Fahrer- und Soziushelm.

---

#### 6.4.2 Heck-Pod 3 (Transceiver) – Das universelle "Rack-Tail Mount" & Rallye-Aero-Balkon-Konzept

Wird eine Reiseenduro mit einem Aluminium-Topcase (z. B. Touratech Zega Evo 38L oder BMW Adventure Topcase) bestückt, schirmt das massive $1{,}5\,\text{mm}$ Aluminiumblech Funkwellen nach oben ab (Faraday-Käfig). Das universelle "Rack-Tail Mount" ([`adventure_rack_tail_mount.scad`](../../hardware/cad/scad/02_pod_base/adventure_rack_tail_mount.scad)) löst diesen Konflikt als hochfester **Rallye-Aero-Balkon** im edlen Zwei-Teil-Design, der fest an der Gepäckbrücke verschraubt wird und ca. $68\,\text{mm}$ hinter die senkrechte Rückwand des Topcases kragt:

![OpenMotorBridge Heck-Pod 3 Rallye-Aero-Balkon CAD-Detailansicht](../images/cad/rack_tail_mount_cad.png)

*Abbildung 8.29-Aero: CAD-Detailansicht des neu gestalteten, zweiteiligen Heck-Balkons (`adventure_rack_tail_mount.scad`). Zu sehen sind die dynamisch ansteigende Keilform, das 15°-Tumblehome mit 45°-Unterzug gegen Steinschlag, der formschlüssige Karosserie-Deckel (`adventure_rack_tail_cowl.stl`) mit integrierter Shark-Finne für die 2.4-GHz-Dipolantenne, das 140°-Zenitfenster für GNSS/LoRa sowie der bionische Tropfen-Ausleger für das Garmin Varia Radar auf der Unterseite.*

![OpenMotorBridge Heck-Pod 3 Rack-Tail Mount & Heck-Balkon Seiten-Schnittansicht](../images/cad/rack_tail_mount_side_cross_section.png)

*Abbildung 8.29a: Technische CAD-Schnittansicht des Heck-Pod 3 Rack-Tail Mounts ("Heck-Balkon") am BMW GS Gepäckträger. Dargestellt sind die Abstützung an den Ø 18 mm Edelstahlrohren, die vollständige Deckelfreigängigkeit des 38L Alu-Topcases, der 65..68 mm Ausleger für ungestörten 140°-Zenit-Empfang (MAX-M10S GNSS / LoRa), der 45°-Astabweiser-Keil mit vertiefter 2.4-GHz-Dipolantenne (+5 dBi) sowie die geschützte Unterseiten-Montage des Garmin Varia Radars in 90..95 cm Höhe über der Fahrbahn.*

![OpenMotorBridge Heck-Pod 3 Rack-Tail Mount Draufsicht](../images/cad/rack_tail_mount_top_view.png)

*Abbildung 8.29b: Technische CAD-Draufsicht des Heck-Balkons (X-Y-Ebene) mit 110-mm-Montageflansch, 2x M6 Langlöchern für Rohrschellen, formbündiger Pod-3-Wanne (136,5 x 71,5 mm), unterer M8-Kabeldurchführung, innenliegendem RG178-Koaxialkanal und 45°-Astabweiser-Finne aus PA12-CF mit Einklipsnut für die 2.4-GHz-Antenne.*

##### Die mechanischen & funktechnischen Kernvorteile:
1. **100 % Erhalt des Topcase-Schnellverschlusses (5-Sekunden-Klick):**
   * Der Ausleger stützt sich an den tragenden Edelstahlrohren ($\varnothing 18\,\text{mm}$) der Gepäckbrücke oder den hinteren M6-Verschraubungen der Adapterplatte ab – **nicht am Koffer selbst**.
   * Das Topcase kann jederzeit sekundenschnell verriegelt und abgenommen werden. Pod 3, Antenne und Radar verbleiben einsatzbereit am Motorrad (Schutz und Tracking auch bei Solofahrten ohne Gepäck).
2. **Kollisionsfreie Deckelöffnung:**
   * Da der Ausleger direkt unterhalb der Koffer-Bodenfuge auskragt und die Rückwand des Koffers starr bleibt, lässt sich der Topcase-Deckel uneingeschränkt nach oben oder nach vorne schwenken sowie vollständig aushängen.
3. **Plattformübergreifende Schnittstelle:**
   * Identische Geometrie für Standard-GS, GS Adventure, Africa Twin und KTM 1290 Super Adventure.
4. **Offroad-Schutz der Sensoren (90..95 cm Höhe über Grund) & Dualer Lock-Mechanismus:**
   * Anders als bei Cruisern liegt das Garmin Varia mmWave-Radar weit außerhalb der Wurfparabel von Grobstollenreifen (Tire Roost).
   * Bei tiefen Fluss- und Schlammdurchfahrten taucht das Heck nicht ins Wasser ein.
   * Keine Gefahr des Aufsetzens oder Abreißens an Felskanten bei steilen Bergab-Stufen.
   * **Dualer Lock-Mechanismus (Neigungssicherung + Diebstahlschutz):**
     Standardmäßige GoPro-Reibgelenke und Garmin-Vierteldreh-Halterungen sind auf extremen Rüttelstrecken (Wellblech/Waschbrett auf TET-Tracks) oder bei Raststätten-Zwischenstopps unzureichend. OpenMotorBridge implementiert daher ein doppeltes Verriegelungssystem:

![OpenMotorBridge Dualer Radar-Lock: Hirth-Verzahnung & Diebstahlsicheres Dock](../images/cad/radar_hirth_lock_dock_cad.png)

*Abbildung 8.29c: Dualer Radar-Lock mit formschlüssiger 36-Zahn-Hirth-Rosette (10°-Rastung gegen Neigungsabsacken auf Wellblechpisten) und diebstahlsicherem Garmin-Bajonettdock mit verdeckter M3-Sicherheits-Madenschraube (Verhinderung von Entwendung bei Zwischenstopps).*

     - **Schwingungs- & Neigungsschutz (Radiale Hirth-Verzahnung):**
       Anstelle reiner Reibung besitzen die Gabelwangen und die zentrale GoPro-Zunge eine formschlüssige 36-Zahn-Hirth-Rosette ([`011_gopro_hirth_lock.scad`](../../hardware/cad/scad/02_pod_base/parts/011_gopro_hirth_lock.scad)). Durch Lösen der M5-Sicherheitsschraube um 1–2 Umdrehungen kann die Radar-Neigung in feinen $10^\circ$-Schritten präzise nivelliert werden (Ausgleich von Sozius- und Gepäckzuladung). Nach Festziehen der Schraube ist ein Absacken des Radars selbst bei härtestem Offroad-Pistenrütteln physikalisch unmöglich.
     - **Garmin Varia Diebstahlschutz-Dock ([`radar_varia_gopro_lock_dock.scad`](../../hardware/cad/scad/02_pod_base/radar_varia_gopro_lock_dock.scad)):**
       Das Garmin Radar wird mit seinem originalen Quarter-Turn Bajonett um $90^\circ$ in das Dock eingedreht. Eine integrierte Sperrklinke rastet formschlüssig ein. Zusätzlich wird eine verdeckte M3-Sicherheits-Madenschraube (Inbus oder Torx-TR mit Innenstift) tangential hinter die Bajonettflanke gedreht. Das Radar kann ohne Spezialbit nicht mehr entriegelt oder entwendet werden. Die M5-Drehachse wird ebenfalls durch eine Torx-TR-Schraube oder M5-Sicherungsmutter geschützt.
5. **Astabweiser-Schutz der externen 2.4 GHz Antenne:**
   * Keine ungeschützte SMA-Stabantenne, die im dichten Unterholz von Zweigen abgeschert wird.
   * Die Antenne liegt geschützt in einer formschlüssigen Klemmnut hinter einem $45^\circ$-Gleitkeil aus zähem PA12-CF. Äste und Packgurte gleiten rückstandsfrei ab.
   * Die Koaxialzuleitung (RG178/U.FL) verläuft zu $100\,\%$ verdeckt im Bauteilinneren mit O-Ring-Dichtung.

---

#### 6.4.3 Unsichtbarer Magnet-Diebstahlschutz im Fernreise-Einsatz

Auf frei zugänglichen Reiseenduros und bei Zwischenstopps auf Fernreisen (z. B. auf TET-Pisten, Pässen oder unbewachten Rastplätzen) schützt der in [Abschnitt 4.1](#41-gesamtsystem-kinematik-poka-yoke-auto-eject--unsichtbarer-magnet-diebstahlschutz) als plattformweiter Standard spezifizierte, vollkommen unsichtbare Magnetverschluss die modularen Einschubkassetten (Sena, Cardo, Transceiver) zuverlässig gegen schnellen Gelegenheitsdiebstahl:

* **100 % Schlamm-, Staub- & Eissicherheit:** Da der Mechanismus hermetisch im Inneren des Gehäuses gekapselt ist und ohne Schlüsselloch oder Außenschieber auskommt, ist er absolut resistent gegen eindringenden Offroad-Schlamm, Pistenstaub, Hochdruckreiniger oder Frost auf winterlichen Pässen.
* **Verdeckte Entriegelung:** Das Entriegeln erfolgt kontaktlos in Sekundenbruchteilen durch Anhalten des N52-Magnetschlüssels an den Zielkreis ($X = 64\,\text{mm}$), woraufhin die V4A-Federn die Kassette formschön um $15\dots 20\,\text{mm}$ auswerfen.

#### 6.4.4 Kontaktlose Kassetten-Entriegelung & Diebstahlschutz
* Die magnetische Notentriegelung und der stumme Taschenalarm sind hersteller- und fahrzeugunabhängig im universellen [2-in-1 LoRa Smart-Keyfob (Gehäuse Typ D)](#7-gehäuse-typ-d-2-in-1-lora-smart-keyfob--pager-smart_keyfob_pagerscad) realisiert.

---

### 6.5 Universal Kofferdeckel-Dock (`saddlebag_lid_dock.scad`)

Das universelle Kofferdeckel-Dock ([`saddlebag_lid_dock.scad`](../../hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad)) wurde speziell für die geschützte, vibrationsfeste und 100 % zerstörungsfreie Innenmontage der Satelliten-Pods 1 (Sena Mesh) und 2 (Cardo DMC) in Motorrad-Seitenkoffern entwickelt (Referenz: Harley-Davidson One-Touch Hartschalenkoffer 2014–2024+):

![Universal Saddlebag Lid Dock CAD](../images/cad/saddlebag_lid_dock_iso.png)

*Abbildung 8.30: 3D-CAD-Visualisierung des Kofferdeckel-Docks (`saddlebag_lid_dock.scad`). Sichtbar sind der inboard gerichtete Torx-Montageflansch für die originalen Scharnierschrauben, die frontale Dual-Port-Kabelschnauze mit Zugentlastung (Port B USB-C Durchgang & Port A M8 Freisparung), die umlaufende Halbschale mit EPDM-Spannbandschlitzen und die obere Tropfkante über dem Kassetteneinschub.*

#### 6.5.1 Zero-Drill-Befestigung & Mechanisches Konzept
1. **Nutzung originaler Befestigungspunkte (Zero-Drill):**
   * Der $4\,\text{mm}$ dicke Montageflansch greift die beiden werksseitigen M5 / Torx T20-Schrauben des Scharnier- bzw. Fangbandbeschlags ab (Lochabstand $52\,\text{mm}$).
   * Großzügige Langlöcher ($\varnothing 5{,}6 \times 9{,}0\,\text{mm}$) ermöglichen den Ausgleich von Fertigungstoleranzen der ABS-Koffer.
   * **Keine Bohrungen im Koffer:** Das Motorrad und die Koffer bleiben zu 100 % im unversehrten Originalzustand (Werterhalt & Dichtigkeit garantiert).
2. **Alternative / Zusätzliche Klebemontage (3M VHB):**
   * Auf der Unterseite sind vier definierte Taschen ($18 \times 12 \times 0{,}8\,\text{mm}$) für 3M VHB Hochleistungs-Acrylatschaum-Klebebänder eingelassen, um eine optionale Montage an glatten Kofferinnenwänden anderer Hersteller (z. B. BMW Vario- oder Alukoffer) zu ermöglichen.
3. **Halbschalen-Architektur ($H = 26\,\text{mm}$):**
   * Die $3\,\text{mm}$ dicke PA12-Wanne umschließt das Pod 3-Gehäuse ($135 \times 70 \times 38\,\text{mm}$) formschlüssig bis auf halbe Höhe.
   * Die modulare Wechselkassette bleibt von hinten voll zugänglich und kann mit Daumen und Zeigefinger in Sekunden entriegelt und gewechselt werden, ohne das Dock zu demontieren.
4. **Schutz vor Tropfwasser (Overhead Drip Lip):**
   * Über dem Kassetteneingang kragt eine integrierte **Tropfkante ($16 \times 2\,\text{mm}$ mit $30^\circ$-Dachschräge)** aus. Sie leitet Kondenswasser oder herablaufende Regentropfen beim Öffnen des Kofferdeckels zuverlässig seitlich an der Kassetten-Dichtfuge vorbei.
5. **Vibrationsfeste EPDM-Sicherung:**
   * Zwei seitliche Durchbrüche ($25 \times 3\,\text{mm}$) nehmen ein elastisches Spannband auf, das den Pod bei harten Fahrbahnschlägen spielfrei in der Wanne arretiert.

#### 6.5.2 Kabelführung, Zündungsplus & Werkstattsichere MagSafe-Abreißkupplung

Die Verkabelung der Kofferdeckel-Pods löst das fundamentale Praxiskriterium des Alltags- und Werkstattbetriebs: **Zündungsgesteuerter Dauerstrom ohne Akku-Sorgen bei gleichzeitiger 100 % zerstörungsfreier Kofferdemontage („Mechaniker-Sicherheit“)**.

![OpenMotorBridge Koffer-Verkabelung & MagSafe-Abreiß-Schnittstelle](../images/cad/saddlebag_magsafe_wiring_cad.png)

*Abbildung 8.30b: CAD-Systemarchitektur der Koffer-Verkabelung mit selbstzentrierender MagSafe-Abreißkupplung (IP67). Dargestellt sind die zündungsgesteuerte 5V-Versorgung über die Zentralbox (KL15/BQ24075-USV), das rahmenfeste MagSafe-Dock (`009_magsafe_frame_dock.scad`) mit PCBA 06 TVS-Schutz, die zerstörungsfreie magnetische Abreißtrennung (~10–15 N) bei Kofferabnahme durch Werkstattmechaniker, die seitliche Durchführung an der Koffer-Vorderwand (oberhalb des Schwingenlagers) mit geteilter TPU-Dichtung (`010_saddlebag_hole_grommet_split.scad`) und Stufe-1-Klemmturm (Kofferboden bleibt zu 100 % intakt und lochfrei), die lastfreie Flachkabelführung parallel zum Deckel-Fangband sowie die Stufe-2-Zugentlastung am Kofferdeckel-Dock mit 0 Newton Zugkraft am USB-C Port B.*

1. **Intelligente Stromversorgung & USV-Pufferung über die Zentralbox (Klemme 15 / BQ24075):**
   * Die Koffer-Pods werden **nicht direkt unreguliert** aus dem Bordnetz gespeist, sondern zentral und konditioniert von der **Zentralbox** unter der Sitzbank versorgt.
   * **Zündungsgesteuerter Wake-Up & USV-Pufferung:** Die Zentralbox erfasst das Zündungsplus (Klemme 15, z. B. am Harley P&A-Zubehörstecker). Bei Zündung EIN regelt der LM5164-Q1 Step-Down auf saubere $5{,}0\,\text{V}$ herunter und der integrierte **LiPo-USV-Pufferakku (BQ24075)** fängt selbst härteste Startspannungseinbrüche (Cold Crank bis $6{,}5\,\text{V}$) unterbrechungsfrei in $8{,}5\,\mu\text{s}$ ab – die Koffer-Pods und Funkmodule rebooten niemals beim Anlassen des Motors.
   * **Automatisierter OEM-Boot per Optokoppler:** Sobald die Versorgungsspannung steht, triggert die Zentralbox über galvanisch getrennte **Toshiba TLP222A Optokoppler** die Tasten-/Power-Einschaltsequenz der OEM-Headset-Adapter (Sena Mesh / Cardo DMC) in den Kassetten.
   * **Null Akku-Wartung & automatischer Shutdown:** Die Intercom-Module schalten vollautomatisch mit der Fahrzeugzündung ein und aus. Das Risiko, vor der Fahrt das Laden zu vergessen oder mit leerem Headset-Akku dazustehen, ist zu 100 % eliminiert.
2. **Werkstattsichere 6-Pin MagSafe-Abreißkupplung (IP67):**
   * In Vertragswerkstätten lösen Mechaniker bei Inspektionen, Reifen- oder Bremsenwechseln die Kofferbefestigungen und heben den Koffer in Sekunden ab, ohne nach nachgerüsteten Kabeln zu suchen. Eine feste Schraub- oder Klickverbindung würde hier unweigerlich abreißen.
   * Die **6-polige IP67-Magnetkupplung mit N52-Neodym-Magneten und vergoldeten Pogo-Pins** trennt sich bei ca. $10\dots 15\,\text{N}$ axialer Zugkraft **völlig verschleiß- und zerstörungsfrei**.
   * Beim Wiedereinsetzen des Koffers zieht sich die Kupplung durch die magnetische Polung vollautomatisch zentrierend zusammen (*Klack*) – Zündungsplus und Signale stehen sofort wieder zur Verfügung.
3. **Zwei-Zonen-Kabelarchitektur:**
   * **Zone 1 (Außen am Bike):** Vollwertiger Automotive-Standard (M8-PUR-Kabel) von der Central Box zum Rahmenadapter.
   * **Zone 2 (Im Koffer):** Da der Kofferinnenraum trocken, sauber und witterungsgeschützt ist, kommt ein schlankes, leichtes Consumer-Silikon- oder Flachbandkabel ($< 2\,\text{mm}$ Außendurchmesser) zum Einsatz. Es trägt nicht auf, nimmt kein Koffervolumen weg und beansprucht die Dichtkanten nicht.
4. **Adapterfreier Direktanschluss an Port B des Pods:**
   * Das schlanke Koffer-Kabel läuft parallel zum textilen Deckel-Fangband in den Kofferdeckel und wird **direkt in den Slim-Port B der Pod-Basis** eingesteckt.
   * Port A (M8-Stutzen) wird im Koffer mit einer Schutzkappe verschlossen. Im Kofferinneren befinden sich **keinerlei zusätzliche Adapterplatinen oder Lötstellen**.
5. **2-Stufen-Zugentlastung & Seitliche Durchführung oberhalb des Schwingenlagers ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad)):**
   * **Montageort (Feedback-Entscheidung):** Der Kabelausgang liegt **nicht im Kofferboden**, sondern **seitlich-innen an der Koffer-Vorderwand (oberhalb des Schwingenlagers, zum Fahrzeugrahmen hin gewandt)**.
   * **Vorteile:**
     - **100 % Spritzwasser- & Dreckschutz:** Am Kofferboden sammelt sich Regenwasser und Straßengischt vom Hinterrad. Die seitliche Vorderwand liegt im absoluten Wind- und Gischt-Schatten des Rahmens.
     - **Kein Scheuern bei Bodenkontakt:** Beim Abstellen des Koffers im Hotel oder in der Werkstatt berührt die Durchführung niemals den Boden.
   * **Stufe 1 (Koffer-Vorderwand):** Die geteilte EPDM/TPU-Dichtung (`010_saddlebag_hole_grommet_split.scad`) mit angeformtem Klemmturm fixiert das Kabel per Mini-Kabelbinder formschlüssig. Externe MagSafe-Abreißkräfte ($10\dots 15\,\text{N}$) werden vollständig in die Kofferwand eingeleitet.
   * **Stufe 2 (Kofferdeckel):** Im Schnauz des Kofferdeckel-Docks ([`saddlebag_lid_dock.scad`](../../hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad)) wird das Kabel formschlüssig abgefangen.
   * **Ergebnis an Port B:** Der USB-C-Stecker im Pod ist vollständig mechanisch entkoppelt und unterliegt **0 Newton dynamischer oder statischer Zugkraft**.

#### 6.5.3 HF-Physik: Warum Kofferdeckel statt Kofferboden?

Die Platzierung der Intercom-Pods im Kofferdeckel ($\approx 70\dots 75\,\text{cm}$ über Fahrbahnniveau) löst fundamentale hochfrequenztechnische Probleme:

| Kriterium | Montage am Kofferboden / Seitenwand | Montage im Kofferdeckel (OpenMotorBridge) | Physikalische Begründung |
| :--- | :--- | :--- | :--- |
| **Flüssigkeitsdämpfung** | **Massive Dämpfung ($> 20\,\text{dB}$)** | **Keine Dämpfung ($0\,\text{dB}$)** | 2,4 GHz ist die Resonanzfrequenz von Wasser ($2\dots 4\,\text{dB/cm}$ Verlust). Kalte Getränkedosen / Wasserflaschen liegen am Boden und blockieren die Line-of-Sight (LOS). Im Deckel liegt der Pod weit über dem Gepäck. |
| **Fresnel-Zonen-Höhe** | Bodennah ($30\,\text{cm}$), starke Reflexion an Asphalt | Optimal ($70\dots 75\,\text{cm}$ über Asphalt) | Die erste Fresnel-Zone zu Gruppenmitgliedern (Helme auf $1{,}2\dots 1{,}5\,\text{m}$) bleibt frei von Bodenhindernissen und Fahrbahninterferenzen. |
| **Gehäuse-Dämpfung** | ABS-Kofferwand ($< 0{,}2\,\text{dB}$) | ABS-Kofferdeckel ($< 0{,}2\,\text{dB}$) | ABS-Kunststoff ist für 2,4 GHz dielektrisch nahezu transparent ($\epsilon_r \approx 2{,}6$, $\tan\delta \approx 0{,}005$). |
| **Schließgestänge** | Im Schwenkbereich | $> 15\,\text{cm}$ Abstand zum Gestänge | Die metallische One-Touch Striker Bar reflektiert nur lokal und verursacht bei $\lambda = 12{,}5\,\text{cm}$ keinerlei Abschattung nach vorne/oben. |
| **HF-Entkopplung** | $< 20\,\text{dB}$ bei benachbarter Montage | **$> 40\,\text{dB}$ Raumdiversität** | Sena (linker Koffer) und Cardo (rechter Koffer) sind $> 60\,\text{cm}$ getrennt; Heckfender und Rahmen dienen als HF-Schirm $\implies$ 0 De-Sensing. |

#### 6.5.4 Stationäres MagSafe-Rahmendock (`009_magsafe_frame_dock.scad`) & Horizontale Clamshell-Architektur

Das stationäre MagSafe-Rahmendock ([`009_magsafe_frame_dock.scad`](../../hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad)) wird fahrzeugfest am Rahmenrohr unter dem Sitzüberhang montiert (passend für Harley Touring / Softail / CVO ST Rahmenrohre mit $\varnothing 25{,}4\dots 28{,}6\,\text{mm}$ bzw. $1"\dots 1{,}125"$):

![MagSafe Frame Dock CAD](../images/cad/magsafe_frame_dock_cad.png)

*Abbildung 8.31: 3D-CAD-Explosionsansicht des MagSafe-Rahmendocks (`009_magsafe_frame_dock.scad`). Sichtbar sind das Obergehäuse mit integrierter Ø 26 mm Rahmensattelwiege und DIN 934 M3 Mutternaschen, die mittige PCBA 06 Schutzplatine, das Untergehäuse mit Halbschalen-Cradles für M8 und MagSafe, der obere Halbschellen-Rohrbügel (`009_magsafe_frame_clamp.stl`) sowie die zentrale M2.5 Zylinderkopf-Klemmschraube.*

1. **Horizontale Clamshell-Teilung & Zugfreie Drop-In Montage:**
   * **Horizontale Teilungsebene ($Z = 8{,}5\,\text{mm}$):** Das Gehäuse ist entlang der Stecker- und Platinen-Mittelebene in zwei formschlüssige Halbschalen getrennt:
     - **Obergehäuse (`009_magsafe_frame_dock.stl`):** Beinhaltet die obere Halbschale für den M8-Kabelkonus und das MagSafe-Kupplungsnest, die $\varnothing 26\,\text{mm}$ Rohrwiege mit M3-Klemmflügeln (mit DIN 934 M3 Sechskant-Nut-Pockets) sowie den oberen massiven Schraubdom mit integrierter DIN 934 M2.5 Sechskant-Nut-Pocket (100 % lötkolbenfrei).
     - **Untergehäuse (`009_magsafe_frame_lid.stl`):** Beinhaltet die untere Halbschale für M8 und MagSafe, die umlaufende PCB-Auflagekante ($Z = 7{,}7\,\text{mm}$) sowie den unteren Schraubdom mit M2.5 Durchgangsbohrung ($\varnothing 2{,}8\,\text{mm}$) und DIN 912 Innensechskant-Senkung ($\varnothing 5{,}2 \times 2{,}8\,\text{mm}$).
   * **Stressfreie Montage:** Die vorkonfektionierte und verlötete Baugruppe (M8-Kabel + PCBA 06 + MagSafe-Kupplung) wird von oben spannungsfrei in die untere Halbschale eingelegt. Kein axiales Hineinschieben, kein Biegedruck auf Adern oder Lötpads!
2. **Schlanke Monocoque-Bauform OHNE seitliche Schraublaschen ($B = 16{,}0\,\text{mm}$):**
   * Statt auftragender seitlicher Schraubohren, die das Dock unnötig verbreitern würden, wird das Gehäuse über **eine einzige zentrale M2.5 Edelstahlschraube (DIN 912 M2.5x12)** im PCB-Zentrum verklemmt.
   * Das Gehäuse bleibt mit exakt $16{,}0\,\text{mm}$ Außenbreite extrem filigran und verschwindet optisch nahtlos unter dem Sitzrahmenrohr.
3. **Zentrale M2.5 Klemmsäule durch PCB-Bohrung:**
   * Die beiden Halbschalen treffen sich in einem inneren $\varnothing 4{,}4\,\text{mm}$ Dom direkt durch die $\varnothing 2{,}7\,\text{mm}$ Zentralbohrung (`H1`) der PCBA 06.
   * Der obere Dom ist mit einer $3{,}2\,\text{mm}$ Entformungsschräge massiv in die Gehäusedecke ($Z \le 16\,\text{mm}$) angebunden.
   * Das Anziehen der Schraube spannt Untergehäuse, PCBA 06 und Obergehäuse vibrationsfest, spielfrei und formschlüssig zusammen.
4. **Labyrinth-Dichtfalz & IP67-Verguss:**
   * Entlang der $Z = 8{,}5\,\text{mm}$ Teilungsebene greift eine $0{,}8\,\text{mm}$ umlaufende Feder des Oberteils in eine korrespondierende Nut des Unterteils ein.
   * Vor dem Fügen eingebrachte elastische Dichtmasse (z. B. neutralvernetzendes Silikon) oder abschließender Verguss dichten den Innenraum zuverlässig gegen Hochdruck-Wasserstrahlen und Straßengischt nach IP67 ab.
5. **Rahmen-Klemmung & Kabelbinder-Option:**
   * **Halbschelle:** Der obere Bügel (`009_magsafe_frame_clamp.stl`) fixiert das Dock über 4x M3 Schrauben bombenfest am Rahmenrohr. Vier $0{,}6\,\text{mm}$ Reibungsrippen verhindern jedes Verdrehen.
   * **Kabelbinder-Slots:** Zwei integrierte $5{,}2 \times 2{,}8\,\text{mm}$ Kanäle ermöglichen zusätzlich oder alternativ die Sicherung mit Schwerlast-Kabelbindern.

---

### 6.6 Entkoppeltes Kennzeichen-Radar-Bracket & Dual-Radar-Optionen

Auf Cruisern und Baggern wird das Heckradar von Pod 3 **entkoppelt** und mittig unter dem Kennzeichen an der Kennzeichen-Radarhalterung ([`radar_license_plate_bracket.scad`](../../hardware/cad/scad/02_pod_base/radar_license_plate_bracket.scad)) montiert:

![Radar License Plate Bracket CAD](../images/cad/radar_license_plate_bracket_cad.png)

*Abbildung 8.32: 3D-CAD-Modell des entkoppelten Kennzeichen-Radarhalters mit M6-Klemmung, M5-Schwenkscharnier, bionischer 36-Zahn Hirth-Verzahnung und verdecktem rückseitigem M8/M5-Kabelkanal.*

* **Rechtliche Vorschrift (§ 10 Abs. 6 FZV / ECE R138):**
  Das Kennzeichen muss von oben in einem vertikalen Winkel von **mindestens $+30^\circ$ vollständig und ohne Verdeckung** einsehbar sein.
* **Vermeidung des Dachüberstand-Problems:**
  Durch die Platzierung des Radars **unter** dem Kennzeichen muss die obere Pod-Konsole nicht weit nach hinten auskragen. Der $+30^\circ$-Sichtbereich auf die Zulassungs- und TÜV-Plaketten bleibt zu $100\,\%$ frei.
* **Schwingungs- und Vibrationsfestigkeit (Formschluss-Hirth-Gelenk):**
  Das Radar sitzt direkt an der massiven Grundplatte ohne langen Hebelarm. Die Gabelwangen besitzen eine integrierte formschlüssige 36-Zahn Hirth-Rosette ([`011_gopro_hirth_lock.scad`](../../hardware/cad/scad/02_pod_base/parts/011_gopro_hirth_lock.scad)).

#### Option 1: Legacy Garmin Varia mmWave-Radar (24 GHz)
* Verwendet das diebstahlhemmende Garmin Varia Dock ([`radar_varia_gopro_lock_dock.scad`](../../hardware/cad/scad/02_pod_base/radar_varia_gopro_lock_dock.scad)) mit Bajonettverschluss und verdeckter M3-Sicherheitsmadenschraube.

#### Option 2: Radar 2.0 – 77 GHz mmWave (Wheeltec MR20) & 36-LED Warnflügel (`radar_mr20_housing.scad`)
Für maximale Reichweite ($90\,\text{m}$), weite $\pm 60^\circ$ ($120^\circ$) Winkelerfassung, autarke optische Warnung und 5.9 GHz ITS-G5 (V2X) Car-to-X Vernetzung steht das dedizierte Radar 2.0 Flügel-Gehäuse zur Verfügung:
1. **Formschlüssiges PA12-MJF Flügel-Gehäuse:**
   * Außenmaße: $121{,}0 \times 71{,}0 \times 34{,}0\,\text{mm}$ (Breite x Höhe x Tiefe).
   * Rückseitige Aufnahme: Monolithisch angeformter Garmin Quarter-Turn Bajonett-Zapfen (kompatibel mit `radar_varia_gopro_lock_dock.scad` und Standard-Varia-Haltern) sowie untere 6-mm-Hirth-Gelenklasche und symmetrische M4-Gewindebuchsen ($40\,\text{mm}$ Stichmaß).
2. **Glattes dielektrisches Polycarbonat-Radom-Sichtfenster:**
   * Vor dem Horn-Array des MR20, den beiden 18-LED Neopixel-Warnflügeln und der 5.9 GHz V2X-Patchantenne sitzt ein transparentes, planes $116 \times 66 \times 1{,}6\,\text{mm}$ PC-Sichtfenster mit 4x M2.5 Torx-Eckverschraubung.
   * Absolut ruß-, graphit- und metallfrei zur Gewährleistung von 100 % HF-Transparenz bei 77 GHz und 5.9 GHz.
3. **Interner Splitter- & Kabelbaum-Hohlraum:**
   * Der originale Kabelstrang des MR20 und das Signal-/Strom-Adaptermodul finden **vollständig im inneren Gehäusehohlraum ($108 \times 58 \times 20\,\text{mm}$)** hinter der PCBA 08 Platz.
   * Keine unschönen externen Kabelpeitschen oder DC-Hohlstecker außerhalb des Gehäuses!
4. **Mechanisch entkoppelte Binder Serie 707 M5 Flanschbuchse:**
   * Am Gehäuseboden ist eine 4-polige Binder Serie 707 M5 Buchse (IP67, $\varnothing 5{,}2\,\text{mm}$ mit Verdrehschutz-Fläche) mit O-Ring fest verschraubt.
   * Elektrische Anbindung an PCBA 08 über ein flexibles 4-adriges JST-SH Kabel. Schläge und Zugkräfte vom Kabelbaum wirken niemals auf die Lötstellen der Platine.
5. **Autarke 5.9 GHz V2X-Keramik-Patchantennenkammer:**
   * In der linken Gehäusekammer sitzt eine monolithische Snap-Fit-Aufnahme für eine $20 \times 20\,\text{mm}$ (oder $25 \times 25\,\text{mm}$) Keramik-Patchantenne mit U.FL-Mikrokoaxialkabel-Führung direkt zum ESP32-C5 Sub-MCU.

---

### 6.7 Custom-Bikes & Bobber: Stealth Center-Underfender Mount vs. Seitlicher Kennzeichenhalter

Auf vielen Custom-Bikes, Bobbern, Choppern und modifizierten Softails (z. B. Breakout, Fat Boy, Sportster S, Indian Scout) montieren Besitzer einen **seitlichen Kennzeichenhalter**, um den breiten Hinterreifen ($180\dots 260\,\text{mm}$) optisch vollständig freizulegen und den Heckfender extrem kurz („Short-Cut“) zu halten. 

Obwohl diese Lösung ästhetisch oft kritisiert wird (asymmetrische Störung der Linienführung), stellt sich in der Praxis die entscheidende Frage: **Wo wird bei solchen Maschinen das Garmin Varia mmWave-Radar platziert?**

#### 6.7.1 Warum Radar am seitlichen Kennzeichenhalter lebensgefährlich ist (Die 3 K.O.-Kriterien)

Das mmWave-Radar darf **unter keinen Umständen** an den seitlichen Kennzeichenhalter montiert werden:

1. **Tödliche RF-Abschattung (Blind Spot im rechten Hecksektor):**
   * Das mmWave-Radar (24 GHz / 77 GHz) sendet in einem horizontalen Fächer von ca. $\pm 20^\circ$ bis $\pm 22{,}5^\circ$ ($40^\circ\dots 45^\circ$ Gesamtkegel).
   * Bei einer linken Achsmontage ($25\dots 35\,\text{cm}$ Versatz zur Fahrzeuglängsachse) verdeckt der breite Hinterreifen ($200\dots 260\,\text{mm}$ Karkasse + Felge) den gesamten Signalpfad nach rechts-hinten.
   * **Konsequenz:** Fahrzeuge, die auf mehrspurigen Straßen oder Autobahnen von rechts hinten auflaufen, rechts überholen oder im toten Winkel mitschwimmen, werden vom Radar **vollständig übersehen**.
2. **100 % ungefederte Massen ($20\dots 30\,g$ Schockbelastung):**
   * Seitliche Halter sind starr an der Schwinge oder direkt auf der Radachse verschraubt.
   * Jeder Schlaglochstoß hämmert mit $20\dots 30\,g$ ungedämpft in den Ausleger. Durch den langen Hebelarm entstehen immense dynamische Biegemomente (Kuhschwanz-Vibrationen), die Bajonettverschlüsse und Leiterplatten-Lötstellen in kürzester Zeit zerstören.
3. **Schräglagen-Asymmetrie & Boden-Clutter:**
   * In Linkskurven sinkt das Radar durch den $30\,\text{cm}$-Hebelarm extrem nah an den Asphalt ab (führt zu Multipath-Bodenreflexionen und Falschalarmen), während es in Rechtskurven steil in den Himmel gerichtet ist.

#### 6.7.2 Die OpenMotorBridge-Architektur: Striktes Entkopplungsprinzip & Stealth Center-Underfender Mount

Für OpenMotorBridge gilt das fundamentale Sicherheitsprinzip: **Das Radar sitzt IMMER zentriert in der Fahrzeug-Symmetrieachse und an der gefederten Masse.**

Hierfür wurde der **Stealth Center Under-Fender Mount** ([`02_pod_base/radar_center_underfender_mount.scad`](../../hardware/cad/scad/02_pod_base/radar_center_underfender_mount.scad)) entwickelt:

![Stealth Center Under-Fender Mount CAD](../images/cad/radar_center_underfender_mount_cad.png)

*Abbildung 8.33: 3D-CAD-Modell des Stealth Center Under-Fender Mounts (`radar_center_underfender_mount.scad`). Sichtbar sind die gewölbte Basisflansch-Sattelplatte ($R = 210\,\text{mm}$) für Schraub- oder 3M-VHB-Klebemontage, die ultrakompakte Clevis-Gabel mit radialer 36-Zahn Hirth-Formschluss-Rastung ($10^\circ$-Ausrichtung) und der verdeckte M8-Kabelschacht zur Kotflügel-Innenseite.*

* **Nahtlose Stealth-Ästhetik für Custom-Hecks:**
  Der Halter sitzt direkt mittig unter der Abschlusskante des Heckkotflügels oder an den inneren Fender-Struts. Von hinten ist das Radar im Schatten des Kotflügels kaum wahrnehmbar und wirkt wie eine winzige, edle Designer-Rückleuchte. Der breite Hinterreifen bleibt optisch zu $100\,\%$ frei.
* **Gefederte Masse & Schwingungsschutz:**
  Da die Montage am Fender / Rahmen (gefederte Masse) erfolgt, reduzieren sich Fahrbahnschläge von $25\,g$ auf unkritische $2\dots 4\,g$.
* **Formschluss-Hirth-Gelenk ($10^\circ$-Schritte):**
  Die Clevis-Gabel nimmt das diebstahlhemmende Garmin Varia Dock ([`radar_varia_gopro_lock_dock.scad`](../../hardware/cad/scad/02_pod_base/radar_varia_gopro_lock_dock.scad)) auf. Die formschlüssige 36-Zahn Hirth-Verzahnung arretiert den Neigungswinkel absolut rutschfest horizontal zur Fahrbahn.
* **Flexible Montage (Kleben oder Schrauben):**
  - **3M VHB 5952:** Breite plane Auflagefläche für bohrungsfreie Montage auf makellosen Custom-Lackierungen.
  - **2x M4/M5 Senkkopfschrauben:** Zentraler Bohrungsabstand von $26\,\text{mm}$ für formschlüssige Verschraubung an vorhandenen Fender-Bohrungen.
* **Verdeckte M8-Kabelführung:**
  Das M8-Kabel verschwindet sofort nach oben durch einen integrierten $\varnothing 5{,}5\,\text{mm}$ Schacht an die Kotflügelinnenseite und läuft dort geschützt im serienmäßigen Kabelkanal nach vorne zur Zentralbox.

---

### 6.8 Begleitfahrzeug-, Support-Van- & Rallye-Kit (Referenz-Kit 5: Car Support Kit)

Für den professionellen Einsatz in Begleitfahrzeugen (Support-Vans bei geführten Motorrad-Touren, Besenfahrzeugen, Orga-Transportern bei Alpentouren) sowie in Pkw-Kolonnen (z. B. Sportwagen-Rallyes) bildet das **Referenz-Kit 5** ein autarkes Gesamtsystem. Es ermöglicht die lückenlose Überwachung aller Teilnehmer-Bikes über das 868-MHz-LoRa-Mesh ohne jede Mobilfunk- oder Cloud-Abhängigkeit.

Mechanisch und fahrzeugintegrativ basiert das Car Support Kit auf zwei speziell entwickelten CAD-Komponenten:
1. Dem **Universal Sonnenblenden-Clip für Pod 3** ([`car_sun_visor_pod3_clip.scad`](../../hardware/cad/scad/05_accessories/car_sun_visor_pod3_clip.scad) / [`car_sun_visor_pod3_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod3_clip.stl))
2. Der **Armaturenbrett-Keilaufnahme für die Zentralbox** ([`car_dashboard_wedge_dock.scad`](../../hardware/cad/scad/05_accessories/car_dashboard_wedge_dock.scad) / [`car_dashboard_wedge_dock.stl`](../../hardware/cad/stl/05_accessories/car_dashboard_wedge_dock.stl))

---

#### 6.8.1 Universal Sonnenblenden-Clip für Pod 3 (`car_sun_visor_pod3_clip.scad`)

Moderne Automobile (Kombis, SUVs, Limousinen, Kastenwagen) besitzen selten feste Heck-Hutablagen, und die geschlossene Blechkarosserie dämpft Funkwellen wie ein Faradayscher Käfig. Zudem sitzt mittig hinter dem Rückspiegel an der Windschutzscheibe fast ausnahmslos ein massiver Sensor- und Kamerakasten (ADAS für Notbremsassistent, Spurhalteradar, Regensensor), der eine mittige Scheibenmontage verhindert.

Der universelle Sonnenblenden-Clip löst diese Probleme elegant durch eine asymmetrische Klemmung an der **Beifahrer-Sonnenblende**:

![Universal Sonnenblenden-Clip für Pod 3 Dual-Ansicht](../images/cad/car_sun_visor_pod3_clip_cad.png)

*Abbildung 8.33b: 3D-CAD-Ansicht des Universal Sonnenblenden-Clips für Pod 3 (`car_sun_visor_pod3_clip_cad.png`) in synchroner Doppelperspektive. Rechts: Obere Pod 3 Aufnahmewanne mit seitlichen Haltebacken ($139 \times 73\,\text{mm}$), Eck-Kugelrastungen für vibrationsfesten Formschluss und stirnseitigem Kabelauslass. Links: Ansicht der Gehäuseunterseite mit solidem U-Kanal-Verbindungssteg, flexibler Federspange (14,5 mm Ruheschlitz für 14–22 mm Sonnenblendendicke), transversalen Anti-Rutsch-Rippen und 30°-Einführschräge.*

* **Strikte Trennung von Aufnahmewanne und Klemmfeder (100 % freier Bauraum):**
  * In der finalen Geometrie sitzt die elastische Federspange strikt auf der **Außen-Unterseite** ($Z \le 0$). 
  * Das obere Aufnahmefach für Pod 3 ist zu $100\,\%$ frei und ungehindert zugänglich. Pod 3 wird flach von oben eingedrückt und rastet an den seitlichen Gehäuselippen formschlüssig ein.
* **Universelle Passform für alle Kfz-Sonnenblenden ($14\dots 22\,\text{mm}$):**
  * Der Federbügel aus PETG oder zähem PA12-MJF besitzt eine Tiefe von $58\,\text{mm}$ und eine Breite von $42\,\text{mm}$.
  * Eine aufgewölbte $30^\circ$-Einführlippe erlaubt das einhändige Aufschieben auf die Blende ohne Kraftaufwand oder Werkzeug.
  * Drei abgerundete Rippen verhindern zuverlässig ein Verrutschen bei Fahrzeugerschütterungen, ohne das empfindliche Leder oder Textil der Sonnenblende zu beschädigen.
* **Hemisphärische HF-Freisicht ($180^\circ$ zum Himmel):**
  * An der oberen Windschutzscheibenkante platziert, strahlen die Antennen von Pod 3 (u-blox MAX-M10S Multi-GNSS, 868 MHz LoRa SX1262 und 5,9 GHz V2X) ungedämpft durch das Glas nach vorne und oben ab.
  * Keine Reflexionen an metallischen Karosserieblechen oder Dachträgern.
* **Diebstahlschutz durch Tarnoptik:**
  * Von außen durch die getönte Frontscheibe betrachtet, wirkt der Clip wie eine unauffällige Maut-Box (Telepass / Bip&Go / Toll Collect) oder ein werkseitiger Garagentor-Transponder.

---

#### 6.8.2 Armaturenbrett-Keilaufnahme für die Zentralbox (`car_dashboard_wedge_dock.scad`)

Für die Zentralbox (Main Control Box, $110 \times 74 \times 32\,\text{mm}$) im Pkw-Innenraum wurde eine formschlüssige, rutschfeste Keilaufnahme konstruiert:

![Dashboard Wedge Dock CAD](../images/cad/car_dashboard_wedge_dock_cad.png)

*Abbildung 8.33c: 3D-CAD-Ansicht der Armaturenbrett-Keilaufnahme für die Zentralbox (`car_dashboard_wedge_dock_cad.png`). Sichtbar sind der ergonomische 15°-Neigungswinkel für blendfreie LED-Ablesbarkeit, die passgenaue Einschubtasche ($111 \times 75\,\text{mm}$), seitliche Finger-Entnahmemulden, die rückseitige Kabeldurchführung für die 12V-Stromversorgung sowie Aussparungen für rutschfeste Silikon-Klebepads an der Unterseite.*

* **Ergonomischer $15^\circ$-Neigungswinkel:**
  * Auf horizontalen Armaturenbrettern oder in Mittelkonsolen-Ablagen richtet der $15^\circ$-Keil die Status-LEDs und Anschlüsse blendfrei zum Fahrer/Beifahrer aus.
* **Sekundenschnelle Entnahme (Dual-Finger-Notches):**
  * Zwei seitliche Griffmulden ($40 \times 12\,\text{mm}$) erlauben das einhändige Greifen und Herausheben der Zentralbox – ideal für den schnellen Wechsel zwischen Motorrad und Begleitfahrzeug.
* **Verdeckte Kabeldurchführung & Kühlung:**
  * Die Rückwand besitzt eine $44\,\text{mm}$ breite Kabelaussparung für den 12V-Kfz-Zigarettenanzünder-PD-Adapter und die HD26-Diagnose-Kabelpeitsche.
  * Zwei kreisförmige Bodenöffnungen ($\varnothing 28\,\text{mm}$) ermöglichen passive Konvektionskühlung des Aluminium-/PETG-Kühlkörpers der Zentralbox.
* **Vibrationsgedämpfte, kratzfreie Auflage:**
  * Die Unterseite verfügt über 4 zylindrische Vertiefungen ($\varnothing 12 \times 1{,}5\,\text{mm}$) zur Aufnahme handelsüblicher 3M-Bumpon-Silikonfüße oder 3M-VHB-Klebepads für absolut rutschfesten Stand auf jeder Cockpit-Oberfläche.

#### 6.8.3 Satelliten-Pods 1 & 2: Befestigungskonzept (Dashboard & Sitzkonsole via 3M Dual-Lock)

Während Pod 3 (GNSS, LoRa-Mesh, 5.9 GHz V2X) wegen der Satelliten-Sicht zwingend an die obere Windschutzscheibenkante gehört, dienen die Satelliten-Pods 1 und 2 im Begleitfahrzeug oder in der Autokolonne primär der Funk- und Audio-Kommunikation:
* **Pod 1:** Intercom-Kassette Gruppe A (z. B. Sena Spider ST1 / 50S Mesh)
* **Pod 2:** Intercom-Kassette Gruppe B (z. B. Cardo Packtalk Edge DMC) oder Midland CB-/PMR-Funk

Da moderne Pkw, Vans, Kombis und SUVs **keine starren Heck-Hutablagen** mehr besitzen und Funkgeräte im Kofferraum unter massiver Blechdämpfung leiden, wurde das Konzept der Hutablage bereits frühzeitig verworfen. Stattdessen nutzt OpenMotorBridge die **100 % identische Gehäusegeometrie** aller Pods ($135 \times 70 \times 26\,\text{mm}$):

1. **Armaturenbrett / Cockpit (Primärempfehlung via 3M Dual-Lock SJ3550):**
   * Die Pods werden mit 3M Dual-Lock Pilzkopf-Klett direkt auf dem Armaturenbrett (z. B. im Bereich der Beifahrer-A-Säule oder nahe der Mittelkonsole) fixiert.
   * **HF-Freisicht durch die Frontscheibe:** Die 2.4-GHz-Mesh- und Bluetooth-Antennen von Sena und Cardo strahlen ungehindert durch das Frontglas nach vorn zu den vorausfahrenden Motorrädern ab (im geschlossenen Blechraum würde das Signal um $20\dots 30\,\text{dB}$ einbrechen).
   * **Kompakte Verkabelung:** Die Distanz zur Zentralbox beträgt nur wenige Dezimeter.
2. **Verdeckte Montage an den Vordersitz-Konsolen (Stealth-Option):**
   * Sollen die Pods im Innenraum völlig unsichtbar sein, werden sie per Klett seitlich unten an den Sitzschienen-Verkleidungen oder an der Teppichwand des Mitteltunnels befestigt.
   * Ideal bei festen Setups, bei denen keine manuellen Tasten bedient werden müssen (Bedienung erfolgt komplett über PWA-Touchscreen oder Pkw-Lenkradtaste).
3. **Flexibler Kassetten- & Sonnenblenden-Wechsel bei Multipurpose-Fahrzeugen:**
   * Jeder Pod (auch Pod 1 oder 2) rastet formschlüssig in den Universal-Sonnenblenden-Clip ([`car_sun_visor_pod3_clip.scad`](../../hardware/cad/scad/05_accessories/car_sun_visor_pod3_clip.scad)) ein.
   * Bei wechselnden Einsatzszenarien kann der Biker den Pod mit der aktuell wichtigsten Funkkassette (z. B. Midland CB-Funk bei einer Rallye) mit einem Klick an die Sonnenblende hängen und danach wieder auf das Motorrad übernehmen.

---

#### 6.8.4 Drahtlose Pkw-Telemetrie: Autarke Bluetooth-OBD2-Kopplung via Zentralbox

Im Pkw oder Support-Van ist ein langes, fest verlegtes CAN-Kabel von der Mittelkonsole quer durch den Fahrerfußraum zur Diagnosebuchse unpraktisch und birgt Stolpergefahren an den Pedalen. OpenMotorBridge löst dies über eine **drahtlose Bluetooth-OBD2-Anbindung**:

1. **Direkte Kopplung mit der Zentralbox (ESP32-S3):**
   * Die Kopplung erfolgt **nicht** über den Browser des Tablets (WebBLE im Browser bricht ab, wenn der Bildschirm sperrt oder die App in den Hintergrund wechselt), sondern **direkt und autark über den Bluetooth-5.0-Controller der Zentralbox**.
   * Die Zentralbox fungiert als BLE-Master (SPP-Client) und verbindet sich beim Einschalten der Zündung vollautomatisch mit handelsüblichen COTS-OBD2-Dongles (z. B. *vGate iCar Pro BLE 4.0*, *OBDLink CX* oder Standard *ELM327 BLE*), die unsichtbar in der OBD2-Buchse unter dem Lenkrad stecken.
2. **Autarkes Polling & LoRa-Mesh-Broadcast:**
   * Die Zentralbox fragt per AT-Kommandos zyklisch die Standard-PIDs nach ISO 15765-4 ab:
     * `010D`: Fahrzeuggeschwindigkeit (km/h)
     * `010C`: Motordrehzahl (RPM)
     * `012F`: Tankfüllstand (%)
     * `0105`: Kühlmitteltemperatur (°C)
   * Diese Daten werden autark in das 868-MHz-LoRa-Mesh (OMM) eingespeist. Die gesamte Motorradgruppe sieht auf ihren Dashboards in Echtzeit Geschwindigkeit, Tankstand und Status des Begleitwagens – selbst wenn im Van gar kein Tablet eingeschaltet ist.

---

#### 6.8.5 Gesamtsystem & Werkzeuglose 5-Minuten-Fahrzeugintegration

Das Zusammenspiel aller Komponenten des Referenz-Kits 5 garantiert einen werkzeuglosen, vollkommen zerstörungsfreien Einbau in jeden Pkw oder Van:

```text
       OPENMOTORBRIDGE REFERENZ-KIT 5 (PKW- & SUPPORT-VAN-TOPOLOGIE)
 ┌────────────────────────────────────────────────────────────────────────┐
 │ Windschutzscheibe oben:                                                │
 │ [Beifahrer-Sonnenblende] ──> [car_sun_visor_pod3_clip] ──> [Pod 3 PCBA]│
 │                               (100% Freisicht nach vorn/oben)          │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │ Ultraflaches USB-C Flachbandkabel
                                     ▼ (in Dachhimmel & A-Säule verdeckt)
 ┌────────────────────────────────────────────────────────────────────────┐
 │ Armaturenbrett / Mittelkonsole:                                        │
 │ [car_dashboard_wedge_dock (15°)] ──> [Zentralbox (ESP32-S3)]           │
 │       ▲           ▲                       │        ▲                   │
 │       │ 12V PD    │ M8 / USB-C            │        │ Bluetooth LE      │
 │ [Zigaretten-      ▼                       │        ▼                   │
 │  anzünder]   [Pods 1 & 2 per 3M Klett]    │   [OBD2 BLE-Dongle]        │
 │              (Dashboard / Sitzkonsole)    │   (ELM327 / vGate unter    │
 │                                           │    dem Lenkrad)            │
 │                                           ├─► USB-C / BLE Offline PWA  │
 │                                           │   (iPad / Android Tablet)  │
 │                                           ▼                            │
 │                                      [CarPlay / Android Auto Audio]    │
 └────────────────────────────────────────────────────────────────────────┘
```

1. **Unsichtbare Flachband-Kabelverlegung (Zero-Damage):**
   * Das dünne, 3 m lange USB-C-Flachbandkabel wird mit den Fingerspitzen in die elastische Fuge zwischen Dachhimmel (**Headliner Seam**) und Windschutzscheibe gedrückt.
   * Der weitere Verlauf erfolgt verdeckt hinter der Gummidichtung der rechten A-Säule und hinter dem Handschuhfach direkt zur Mittelkonsole.
   * **Ergebnis:** Null sichtbare Kabel, null Bohrlöcher, in unter 3 Minuten spurlos demontierbar (z. B. bei Miet- oder Leasingfahrzeugen).
2. **Autarke Stromversorgung:**
   * Die Zentralbox wird über einen kompakten 12V/24V-Kfz-Zigarettenanzünder-Adapter (30W USB-PD Schnelllader) direkt mit Zündungs- oder Dauerplus versorgt.
3. **Flotten-Live-Tracking ohne Mobilfunk (PWA Fleet Dashboard):**
   * Auf einem im Begleitfahrzeug montierten Tablet (iPad oder Android) läuft das OpenMotorBridge PWA-Dashboard im Offline-Kartenmodus.
   * Über das 868-MHz-LoRa-Mesh empfängt das Support-Team Positionsdaten, Geschwindigkeiten, Reifendrücke und Sturz-/SOS-Alarme aller Fahrer im Umkreis von bis zu $15\,\text{km}$.
4. **Infotainment- & Audio-Integration:**
   * Durch Anschluss der Zentralbox an die USB-Media-Buchse des Fahrzeugs startet kabelgebundenes Apple CarPlay / Android Auto. Alarmtöne und Funkdurchsagen der Motorradgruppe werden glasklar über das Pkw-Soundsystem ausgegeben.

---

## 7. Gehäuse Typ D: 2-in-1 LoRa Smart-Keyfob & Pager (`smart_keyfob_pager.scad`)

Der **OpenMotorBridge 2-in-1 Smart-Keyfob** ([`smart_keyfob_pager.scad`](../../hardware/cad/scad/05_accessories/smart_keyfob_pager.scad)) löst die gravierenden Schwächen herkömmlicher Motorrad-Schlüsseltransponder (schwache Knopfzellen, Kälteempfindlichkeit, fehlender Rückkanal und Notwendigkeit separater Kassettenwerkzeuge). Er vereint einen ultrastarken N52-Neodym-Entriegelungsschlüssel und einen autarken 868-MHz-LoRa-Alarmpager in einem ergonomischen, taschentauglichen Gehäuse:

![OpenMotorBridge 2-in-1 Smart-Keyfob 3D CAD Assembly](../images/cad/smart_keyfob_pager_assembly.png)

*Abbildung 8.34: 3D-CAD-Gesamtansicht des 2-in-1 LoRa Smart-Keyfobs (`smart_keyfob_pager.scad`). Sichtbar sind das ergonomisch gerundete PA12-MJF Gehäuse ($58 \times 34 \times 13\,\text{mm}$), der umlaufende orangefarbene TPU-Kantenschutz, die 316L-Edelstahl-Schlüsselringöse sowie der seitlich eingelassene N52-Neodym-Auswerferschlüssel mit taktilem Ausrichtungssteg.*

![OpenMotorBridge 2-in-1 Smart-Keyfob Exploded 3D CAD Fitting](../images/cad/smart_keyfob_pager_exploded.png)

*Abbildung 8.35: 3D-CAD-Explosionsdarstellung des Smart-Keyfobs. Von unten nach oben: PA12-MJF Unterschale mit rückseitiger MagSafe-Zentrierringtasche, 180–200 mAh LiPo-Pouch-Zelle ($25 \times 18 \times 3{,}8\,\text{mm}$), PCBA 07 Trägerplatine ($38 \times 19\,\text{mm}$), Semtech SX1262 LoRa Transceiver, LRA-Haptikmotor, Mu-Metall-Flussleitblech ($0{,}5\,\text{mm}$), N52-Neodym-Schlüsselblock ($20 \times 10 \times 5\,\text{mm}$) und Oberschale mit Diffusor-Bohrung für die RGB-Statusanzeige.*

### 7.1 Mechanischer Aufbau & Gehäuseparameter
* **Außenabmessungen:** $58{,}0 \times 34{,}0 \times 13{,}0\,\text{mm}$ (Länge x Breite x Dicke; Unterschale $6{,}5\,\text{mm}$, Oberschale $6{,}5\,\text{mm}$).
* **Materialien & Fertigung:** Hochfestes PA12 im HP Multi Jet Fusion (MJF) Verfahren, kugelgestrahlt, chemisch geglättet und hydrophob versiegelt.
* **Stoßabsorbierender TPU-Kantenschutz:** Umlaufender $0{,}8\,\text{mm}$ TPU-95A Schutzrahmen (Orange `#ff9f0a`) mit Freisparung für die seitliche Magnetkontaktfläche. Schützt Gehäuse und Elektronik zuverlässig bei Stürzen auf Asphalt aus bis zu $2\,\text{m}$ Höhe.
* **316L Edelstahl-Öse:** Massive Schlüsselloch-Durchführung ($\varnothing 4{,}5\,\text{mm}$ innen, $3{,}5\,\text{mm}$ Wandstärke) für Standard-Motorrad-Schlüsselringe und Karabiner.
* **Integrierter N52 Neodym-Schlüsselblock ($20 \times 10 \times 5\,\text{mm}$):**
  * Auf der schmalen Längsseite formschlüssig eingepresst mit korrosionsfester Ni-Cu-Ni Dreifachbeschichtung (silbern-metallisch glänzend, in den CAD-Renderings deutlich sichtbar) und mit einem taktilen Nordpol-Ausrichtungssteg versehen.
  * Tritt der Keyfob an den $X = 64\,\text{mm}$ Zielkreis des Pod-Gehäuses heran, zieht das konzentrierte B-Feld ($B_r \approx 1{,}48\,\text{T}$) den innenliegenden Stahlanker an und entriegelt die Auswerferfedern.
* **0,5 mm Weicheisen- / Mu-Metall-Abschirmblech (Flux Shield):**
  * Direkt hinter dem N52-Magneten platziert. Schirmt die interne Elektronik (SX1262 LoRa-Transceiver, Nordic BLE-SoC, 180 mAh LiPo-Pouch-Akku) hermetisch gegen magnetische Sättigung ab und lenkt den magnetischen Fluss zu 100 % nach außen auf die Gehäusewand.
* **Stummer Alarm-Pager mit LRA-Vibrationsmotor:**
  * Ein $\varnothing 10 \times 3{,}6\,\text{mm}$ Linear Resonant Actuator (LRA) warnt den Fahrer bei Erschütterung, unbefugtem Aufbocken oder Kassettenhebeln lautlos über haptische Vibrationsmuster in der Jackentasche.
* **MagSafe / Qi Induktiv-Ladeaufnahme:**
  * Auf der Rückseite ist ein magnetischer Ausrichtungsring ($\varnothing 28\,\text{mm}$ außen, $\varnothing 22\,\text{mm}$ innen) integriert. Der Keyfob rastet während der Fahrt auf dem Cockpit-Dock (PCBA 06) magnetisch ein und wird induktiv nachgeladen.
* **Zero-False-Alarm & Präsenz-Token:**
  * Durch den Nahfeld-BLE-Beacon des Keyfobs erkennt OpenMotorBridge, dass der rechtmäßige Besitzer die Kassette entnimmt. Ein Diebstahlalarm wird nur ausgelöst, wenn ein Hebelversuch am Kassettenverschluss ohne anwesenden Keyfob registriert wird.

### 7.2 Architekturentscheidung: Warum N52-Permanentmagnet + LoRa + MagSafe statt UWB / aktiver Servos?

| Kriterium | Aktive Bluetooth / UWB Verriegelung | N52-Permanentmagnet + LoRa Pager (OpenMotorBridge) |
| :--- | :--- | :--- |
| **Notentriegelung bei leerer Batterie** | **Unmöglich** (Kassette bleibt im Motorrad gefangen) | **100 % Zuverlässig** (Permanentmagnet funktioniert rein physikalisch ohne Strom) |
| **Ruhestromverbrauch am Schlüsselbund** | 15–45 mA (UWB-Transceiver leert Knopfzelle in Wochen) | **< 50 nA Standby** (Monatelange Standzeit, lädt induktiv am Cockpit-Dock) |
| **Mechanische Robustheit & Bauraum** | Miniatur-Servomotor blockiert bei Schmutz/Vibration | **Formschlüssiger N52-Neodymblock** (Unverwüstlich, keine beweglichen Teile im Key) |
| **Reichweite für Diebstahl-Pager** | 10–30 m (Bluetooth LE bricht hinter Wänden ab) | **Bis zu 4,5 km** (Semtech SX1262 LoRa 868 MHz durchdringt Hotelwände & Garagen) |
| **Falschalarm-Unterdrückung** | Oft Fehlalarme durch reine Erschütterungssensoren | **Zero-False-Alarm:** Entriegelung durch rechtmäßigen Besitzer via BLE-Präsenz erkannt |

---

## 8. Cockpit-Zubehör & Ergonomie-Bedienelemente (`05_accessories/`)

### 8.1 Under-Perch Tasterhalter (`under_perch_switch_bracket.scad`)

Der **Under-Perch Tasterhalter** ([`under_perch_switch_bracket.scad`](../../hardware/cad/scad/05_accessories/under_perch_switch_bracket.scad)) löst das fundamentale Bauraum- und Ergonomie-Dilemma am linken Lenkergriff von Cruisern und Touring-Maschinen:

![Under-Perch Tactile Switch Bracket 3D CAD](../images/cad/under_perch_switch_bracket_cad.png)

*Abbildung 8.36: 3D-CAD-Ansicht des Under-Perch Tasterhalters (`under_perch_switch_bracket_cad.png`). Dargestellt sind der M4-Befestigungsflansch mit Antirotations-Führung zur Harley-Schalterarmatur, der bionische Absenksteg, das um 28° zum Fahrerdaumen geneigte Schalterrohr mit Schutzblende, der rote IP67-Mikrotaster sowie die rückwärtige PUR-Kabeldurchführung.*

* **Mechanische Vorteile:**
  * **0 mm Lenkerrohr-Bedarf:** Verbraucht keinen Millimeter auf dem geraden Lenkerrohr. Die obere Klemmschelle der Armatur bleibt zu **100 % frei für die Steuereinheit eines Klappenauspuffs** (Dr. Jekill & Mr. Hyde / KessTech).
  * **2-Finger-Hebelüberdeckung:** Zeige- und Mittelfinger bleiben unterbrechungsfrei auf dem Kupplungshebel. Der Taster sitzt exakt 15 mm unterhalb des Blinkerschalters in der natürlichen Daumenabsenkzone.
  * **Universelle Befestigung:** Verschraubung entweder über die originale M4-Gehäuse-Torxschraube der Harley-Armatur oder über den M8/M10-Spiegelschaftadapter ([`under_perch_mirror_plate.stl`](../../hardware/cad/stl/05_accessories/under_perch_mirror_plate.stl)).

### 8.2 Spiegel-Totwinkel-LED Gehäuse (`bsd_mirror_indicator_pod.scad`)

Das **Spiegel-Totwinkel-LED Gehäuse** ([`bsd_mirror_indicator_pod.scad`](../../hardware/cad/scad/05_accessories/bsd_mirror_indicator_pod.scad)) integriert die Radarwarnung (Port `J9` am Front-Node) aerodynamisch und blendfrei in das Cockpit:

![Blind Spot Detection Mirror Indicator Pod 3D CAD](../images/cad/bsd_mirror_indicator_pod_cad.png)

*Abbildung 8.37: 3D-CAD-Ansicht des aerodynamischen Spiegel-Totwinkel-Pods (`bsd_mirror_indicator_pod_cad.png`). Sichtbar sind die strömungsgünstige Tropfenform auf dem Ø 10 mm Spiegelarm, die 2-Punkt M3-Edelstahl-Klemmschelle, die 38° nach innen zum Fahrerhelm gerichtete Blendschutzhaube sowie die bernsteinfarbene Diffusorlinse.*

* **Optische & Gesetzliche Sicherheit (StVZO / ECE R50):**
  * **Gezielte Fahrer-Projektion:** Der um 38° nach innen geneigte Lichttunnel projiziert das gelb/rote Radar-Stroboskoplicht exakt in das periphere Sichtfeld des Fahrerhelms.
  * **100 % Blendfreiheit:** Ein 3,8 mm tiefer Visier-Überhang und die blickdichte Vorderwand schirmen das Licht vollständig nach vorne und zur Seite ab. Kein Blenden des Gegenverkehrs, kein Irritieren anderer Verkehrsteilnehmer – voll TÜV-konform.
  * **Universalklemmung:** Zweiteilige Halbschale für Ø 10 mm (Harley, BMW, KTM) und Ø 12 mm Spiegelarme mit verdeckter Kabelführung zu Port `J9`.

### 8.3 Radar 2.0 mmWave Flügel-Gehäuse & Garmin-Bajonett (`radar_mr20_housing.scad`)

Das **Radar 2.0 Flügel-Gehäuse** ([`radar_mr20_housing.scad`](../../hardware/cad/scad/05_accessories/radar_mr20_housing.scad)) integriert das 77-GHz-mmWave-Sensormodul Wheeltec MR20, die geroutete Trägerplatine PCBA 08 (mit 36-LED Warnflügeln und ESP32-C5 Dual-Band Sub-MCU), den Garmin Quarter-Turn Bajonettverschluss sowie die autarke 5.9 GHz ITS-G5 (V2X) Keramik-Patchantenne:

![Radar 2.0 Flügel-Gehäuse 3D CAD](../images/cad/radar_mr20_housing_cad.png)

*Abbildung 8.38: 3D-CAD-Frontansicht des Radar 2.0 Flügel-Gehäuses (`radar_mr20_housing_cad.png`). Sichtbar sind das symmetrische $121 \times 71 \times 34\,\text{mm}$ PA12-MJF Monocoque-Gehäuse, der plane PC-Radom-Fensterrahmen ($116 \times 66 \times 1{,}6\,\text{mm}$) mit 4x M2.5 Torx-Eckverschraubung, der zentrierte $61 \times 51\,\text{mm}$ Radarausschnitt für das MR20 77-GHz-Horn-Array, die beidseitigen LED-Warnflügel-Kammern sowie die linke Antennenkammer für die 5.9 GHz V2X-Keramik-Patchantenne.*

![Radar 2.0 Garmin-Bajonett & Diebstahlsicherung](../images/cad/radar_mr20_housing_bayonet_cad.png)

*Abbildung 8.38b: 3D-CAD-Rückansicht des Radar 2.0 Gehäuses (`radar_mr20_housing_bayonet_cad.png`). Dargestellt sind der monolithische Garmin Quarter-Turn Bajonett-Zapfen (kompatibel mit `radar_varia_gopro_lock_dock.scad` und allen Standard-Varia-Haltern), die federnde Rastklinken-Diebstahlsicherung, das symmetrische M4-Gewindebuchsen-Lochbild ($40\,\text{mm}$ Stichmaß) sowie die zentrierte Binder Serie 707 M5 Flanschbuchsenbohrung am Gehäuseboden.*

* **Konstruktionsmerkmale & HF-Architektur:**
  * **Symmetrisches Flügel-Rechteck ($121{,}0 \times 71{,}0 \times 34{,}0\,\text{mm}$):** Optimale aerodynamische Schaufelform, die sich harmonisch an Kennzeichenträger und Heckfender anschmiegt.
  * **Garmin Quarter-Turn Bajonett mit Diebstahlsicherung:** Werkzeugloses Aufsetzen und Verriegeln durch 90°-Drehung. Eine federnde Rastklinke verhindert versehentliches Lösen durch Fahrbahnstöße und erschwert Gelegenheitsdiebstahl.
  * **Integrierte 5.9 GHz V2X Keramik-Patchantennen-Kammerturm:** Auf der linken Gehäuseflanke ist eine Rastkammer für $20 \times 20\,\text{mm}$ oder $25 \times 25\,\text{mm}$ Keramik-Patchantennen monolithisch eingeformt. Dies garantiert maximale Antennenreichweite ohne Gehäusedämpfung und ohne interne PCB-Antennen-Verluste.
  * **Großzügiger Adapter- & Verkabelungsraum ($112 \times 62 \times 17\,\text{mm}$):** Nimmt den originalen MR20-Zwischenadapter und Kabelbaum-Schlaufen knickfrei im Gehäuseinneren auf.
  * **Optisches PC-Radom & IP67-Dichtung:** Glattes, unstrukturiertes Polycarbonat ($116 \times 66 \times 1{,}6\,\text{mm}$) mit umlaufender EPDM-Schnurnut garantiert 0 dB RF-Dämpfung bei 77 GHz und Schlagfestigkeit nach IK08.

### 8.4 Road Glide ST Sharknose: Induktives Durch-die-Verkleidung Cam-Dock (`road_glide_inductive_cam_dock.scad`)

Das **induktive Cam-Dock** ([`road_glide_inductive_cam_dock.scad`](../../hardware/cad/scad/05_accessories/road_glide_inductive_cam_dock.scad)) löst das Problem der Dauerstromversorgung von Action- und 360°-Kameras (Insta360 X3/X4, GoPro Hero, DJI Osmo Action) auf der Nase der Sharknose-Verkleidung **ohne ein einziges Loch zu bohren und ohne sichtbare Außenkabel**:

![Road Glide Induktives Cam-Dock](../images/cad/road_glide_inductive_cam_dock_cad.png)

*Abbildung 8.39: 3D-CAD-Gesamtansicht des Durch-die-Verkleidung Induktiv-Docks (`road_glide_inductive_cam_dock_cad.png`). Sichtbar sind die 15W Qi-Transmitter-Wanne (Unterseite, verdeckt im Verkleidungsinneren), das dielektrische ABS-Verkleidungsdeck der Harley Road Glide (mittig dargestellt) sowie das aerodynamische Tropfenform-Außendock mit 3M Dual-Lock-Boden, integriertem TI BQ51013B Qi-Empfänger und 3-Finger-Gelenk für Actioncams.*

#### 8.4.1 Zweiteilige Systemarchitektur & Schnittstellen zur Action-Cam

```text
 ┌────────────────────────────────────────────────────────┐
 │ Action-Cam (Insta360 X3/X4 / GoPro Hero / DJI Action)  │
 │ [USB-C Ladeport] ◄─────────────────────────────────┐   │
 └────────┬───────────────────────────────────────────│───┘
          │ Standard 2-Finger-Lasche                  │
          ▼                                           │ 30 mm USB-C
 ┌────────────────────────────────────────────────────│───┐
 │ ROAD GLIDE INDUKTIV-CAM-DOCK (AUSSEN)              │   │
 │ • Integriertes 3-Finger-Gelenk (M5-Klemmschraube)  │   │
 │ • TI BQ51013B Abwärtswandler (5V / 2A) ────────────┘   │
 │ • Qi-Empfängerspule (RX) mit Ferritschild              │
 └────────────────────────┬───────────────────────────────┘
                          │ 3M Dual-Lock SJ3550 Pilzkopfklett
                          ▼ (sekundenschnell abziehbar)
 ══════════════════════════════════════════════════════════
  Harley-Davidson ABS-Verkleidungsdeck (2.8 mm, 100% ohne Bohrung!)
   ~ ~ ~ Magnetisches Wechselfeld (15W Qi Induktion) ~ ~ ~
 ══════════════════════════════════════════════════════════
                          ▲ (3M VHB 5952 Verklebung innen)
 ┌────────────────────────┴───────────────────────────────┐
 │ INNEN-CRADLE (Unter der Haube / hinter Scheinwerfer)   │
 │ • 15W Qi-Senderspule (TX)                              │
 │ • Anschlusskabel zu Front-Knoten Port 1 (12V PD)       │
 └────────────────────────────────────────────────────────┘
```

1. **Mechanische Anbindung an die Kamera:**
   * **Monolithisches 3-Finger-Gelenk (Universal GoPro-Mount):** Direkt auf der Oberseite des Außendocks sitzt die standardisierte 3-Finger-Aufnahme. Jede gängige Actioncam (GoPro Hero 10–13, DJI Osmo) oder jeder 360°-Kamerarahmen (z. B. Insta360 X3/X4 Haltekäfig) wird direkt mit einer handelsüblichen M5-Rändelschraube aufgesteckt.
   * **Integrierte M5-Hutmutter-Tasche:** Auf der linken Flanke ist eine formschlüssige Sechskant-Aussparung eingelassen, die eine M5-Mutter unverlierbar hält – die Klemmschraube kann somit einhändig festgezogen werden.
   * **Optionales 1/4"-20 Stativgewinde:** Alternativ ist im Zentrum eine Bohrung für eine zöllige Messing-Gewindebuchse (1/4"-20 UNC) vorgesehen, um Kameras oder Kugelköpfe direkt aufzuschrauben.
2. **Elektrische Verbindung (Dauerstrom-Versorgung):**
   * **Induktive Energiewandlung:** Die im Dockboden eingelassene Qi-Empfängerspule wandelt das durch die $2{,}8\,\text{mm}$ dicke ABS-Verkleidung übertragene Wechselfeld über einen TI BQ51013B Controller in stabile $5\,\text{V} / 2\,\text{A} = 10\,\text{W}$ Gleichspannung um.
   * **Ultrakurzer USB-C Pigtail ($30\dots 50\,\text{mm}$):** Aus einer schräg nach vorn/oben gerichteten Kabelöffnung des Docks führt ein hochflexibles, kurzes USB-C-Flachbandkabel mit $90^\circ$-Winkelstecker direkt in die Ladebuchse der Kamera.
   * **Kein Fahrtwind-Flattern:** Da das Kabel nur wenige Zentimeter lang ist und unmittelbar unter dem Kamera-Ladeport austritt, liegt es eng am Gehäuse an – es flattert nicht im Fahrtwind, schlägt nicht gegen den Lack und erzeugt keine Windgeräusche im Mikrofon.
3. **Praxis-Vorteile auf Tour:**
   * **100 % Originalzustand:** Absolut bohrungsfrei, null Lackbeschädigung, 100 % wetterfest nach IP67.
   * **Unendliche Aufnahmezeit:** Hält den Kamera-Akku auch bei rechenintensiver 5.7K/60fps 360°-Daueraufnahme dauerhaft auf 100 % (z. B. als Dashcam im Endlos-Loop).
   * **Sekundenschnelle Demontage beim Parken:** USB-C-Winkelstecker abziehen, Dock mit einem Handgriff vom 3M Dual-Lock trennen und samt Kamera in der Jackentasche oder dem Koffer verstauen.

---

## 9. CAD-Dateistruktur & OpenSCAD-Modulbaukasten (STL-Bibliothek)

Die CAD-Dateistruktur von OpenMotorBridge folgt einer strengen hierarchischen CSG-Architektur (Constructive Solid Geometry):
- **Hauptverzeichnisse (`01_main_box/`, `02_pod_base/`, `03_pod_cartridges/`, `04_front_node/`, `05_accessories/`)**: Enthalten **ausschließlich monolithische, direkt 3D-druckbare Produktions-STLs** (100 % single-manifold, wasserdicht, 0 frei schwebende Körper).
- **Unterordner (`components/`)**: Enthalten die parametrischen CSG-Einzelkomponenten (z. B. unbeschnittene Basiskörper, Flansche, Schraubdome, Dichtkämme und PCB-/Akku-Dummies) für Baugruppenmontagen und modulare Adaptionen.

### 9.1 Druckfertige Produktions-STLs (Hauptverzeichnisse)

| Baugruppe | Funktion / Bauteil | Druckfertige STL-Datei | Parametrischer OpenSCAD Code |
| :--- | :--- | :--- | :--- |
| **Zentralbox** | Unterwanne mit Dichtnut & Halteohren | `01_main_box/main_box_lower_case.stl` | `01_main_box/00_lower_deck.scad` |
| **Zentralbox** | Oberwanne mit Zwischenboden | `01_main_box/main_box_mid_tray.stl` | `01_main_box/01_upper_deck.scad` |
| **Zentralbox** | Gehäusedeckel mit Gore-Vent | `01_main_box/main_box_lid.stl` | `01_main_box/02_colsure.scad` |
| **Satelliten-Pod**| 5-seitiges Monocoque-Gehäuse (Tunnel) | `02_pod_base/pod_base_housing.stl` | `02_pod_base/pod_base_housing.scad` |
| **Satelliten-Pod**| CVO ST Under-Cowl Skeleton Dock | `02_pod_base/cvo_st_undercowl_skeleton_dock.stl` | `02_pod_base/cvo_st_undercowl_skeleton_dock.scad` |
| **Satelliten-Pod**| CVO ST Telemetrie-Finne (2.4 GHz Mesh) | `02_pod_base/cvo_st_telemetry_fin.stl` | `02_pod_base/cvo_st_telemetry_fin.scad` |
| **Satelliten-Pod**| Road King Special Touring Fender Console | `02_pod_base/pod3_touring_fender_console.stl` | `02_pod_base/pod3_touring_fender_console.scad` |
| **Satelliten-Pod**| Touring Kofferdeckel-Halter (Pod 1 & 2) | `02_pod_base/saddlebag_lid_dock.stl` | `02_pod_base/saddlebag_lid_dock.scad` |
| **Adventure Pod 3**| Rallye-Aero-Balkon Basis-Wanne (Heckbrücken-Ausleger) | `02_pod_base/adventure_rack_tail_mount_base.stl` | `02_pod_base/adventure_rack_tail_mount.scad` |
| **Adventure Pod 3**| Rallye-Aero-Balkon Karosserie-Deckel (mit Shark-Finne) | `02_pod_base/adventure_rack_tail_cowl.stl` | `02_pod_base/adventure_rack_tail_mount.scad` |
| **Adventure Pods 1/2**| GS Transition Dock Basis-Wanne (Bügelfalten-Unterteil) | `02_pod_base/adventure_transition_dock_base.stl` | `02_pod_base/adventure_transition_dock.scad` |
| **Adventure Pods 1/2**| GS Transition Dock Karosserie-Deckel (Bügelfalten-Cowl) | `02_pod_base/adventure_transition_dock_lid.stl` | `02_pod_base/adventure_transition_dock.scad` |
| **Adventure-Kit** | Unter-Sitzbank-Sattelbrücke (Traverse links-rechts) | `02_pod_base/adventure_underseat_cross_rail.stl` | `02_pod_base/adventure_underseat_cross_rail.scad` |
| **Adventure Pods 1/2**| GSA Heavy-Duty Cage Dock Gehäusekorpus (Ø 18 mm Rohr) | `02_pod_base/adventure_gsa_cage_dock_body.stl` | `02_pod_base/adventure_gsa_cage_dock.scad` |
| **Adventure Pods 1/2**| GSA Heavy-Duty Klemmschelle Kappe (Ø 18 mm Rohr) | `02_pod_base/adventure_gsa_clamp_cap.stl` | `02_pod_base/adventure_gsa_cage_dock.scad` |
| **Adventure Pods 1/2**| GSA Rohrträger-Klemmschelle Basis (Minimal-Option) | `02_pod_base/adventure_pannier_rack_clamp_base.stl` | `02_pod_base/adventure_pannier_rack_clamp.scad` |
| **Adventure Pods 1/2**| GSA Rohrträger-Klemmschelle Kappe (Minimal-Option) | `02_pod_base/adventure_pannier_rack_clamp_cap.stl` | `02_pod_base/adventure_pannier_rack_clamp.scad` |
| **Rahmendock** | MagSafe Rahmen-Dock Gehäuseoberteil (Rohrsattel, Flügel & M2.5 Nut-Pocket) | `02_pod_base/components/009_magsafe_frame_dock.stl` | `02_pod_base/parts/009_magsafe_frame_dock.scad` |
| **Rahmendock** | MagSafe Rohrschellen-Bügel (Ø 26 mm) | `02_pod_base/components/009_magsafe_frame_clamp.stl` | `02_pod_base/parts/009_magsafe_frame_dock.scad` |
| **Rahmendock** | MagSafe Rahmen-Dock Gehäuseunterteil (PCB-Ledge & M2.5 Senkung) | `02_pod_base/components/009_magsafe_frame_lid.stl` | `02_pod_base/parts/009_magsafe_frame_dock.scad` |
| **Radarhalter** | Entkoppelte Kennzeichen-Radarhalterung | `02_pod_base/radar_license_plate_bracket.stl` | `02_pod_base/radar_license_plate_bracket.scad` |
| **Radarhalter** | Stealth Center Under-Fender Radar-Mount (Custom / Bobber) | `02_pod_base/radar_center_underfender_mount.stl` | `02_pod_base/radar_center_underfender_mount.scad` |
| **Radar-Zubehör** | Garmin Varia Quarter-Turn Anti-Theft Lock Dock | `02_pod_base/radar_varia_gopro_lock_dock.stl` | `02_pod_base/radar_varia_gopro_lock_dock.scad` |
| **Kassette** | Universeller Basisschlitten mit Dichtung | `03_pod_cartridges/cartridge_base_sled.stl` | `03_pod_cartridges/00_base_sled.scad` |
| **Kassette** | Magnetischer Diebstahlschutz-Rastbolzen (Sägezahn-Mechanik) | `03_pod_cartridges/cartridge_magnetic_lock_latch.stl` | `03_pod_cartridges/parts/05_magnetic_lock_latch.scad` |
| **Kassette** | Sena 50S/60S Adapterkassette | `03_pod_cartridges/cartridge_insert_sena.stl` | `03_pod_cartridges/parts/01_insert_sena.scad` |
| **Kassette** | Cardo Packtalk Edge Adapterkassette | `03_pod_cartridges/cartridge_insert_cardo.stl` | `03_pod_cartridges/parts/02_insert_cardo.scad` |
| **Kassette** | IP67 Blindkassette (wasserdichte Dry Box)| `03_pod_cartridges/cartridge_insert_blindkassette.stl` | `03_pod_cartridges/parts/03_insert_blindkassette.scad` |
| **Kassette** | OMM Dipol-Antennenhalterung | `03_pod_cartridges/cartridge_antenna_bracket_omm.stl` | `03_pod_cartridges/parts/04_antenna_bracket_omm.scad` |
| **Front-Knoten** | Unterwanne mit 4-in-1 Boden & Ohren | `04_front_node/front_node_lower_tub.stl` | `04_front_node/00_front_node_tub.scad` |
| **Front-Knoten** | Gehäusedeckel mit LED & FPC-Tasche | `04_front_node/front_node_upper_lid.stl` | `04_front_node/01_front_node_lid.scad` |
| **Front-Knoten** | EPDM/TPU Dichtkamm-Paar mit Steg | `04_front_node/front_node_cable_glands_tpu.stl` | `04_front_node/02_front_node_cable_glands.scad` |
| **Front-Knoten** | TPU USB-C Staubschutzstopfen | `04_front_node/front_node_usbc_cap_tpu.stl` | `04_front_node/03_front_node_usbc_plug.scad` |
| **Smart-Keyfob** | PA12-MJF Unterschale mit MagSafe-Tasche | `05_accessories/smart_keyfob_lower_shell.stl` | `05_accessories/smart_keyfob_pager.scad` |
| **Smart-Keyfob** | PA12-MJF Oberschale mit Diffusor-Bohrung | `05_accessories/smart_keyfob_upper_shell.stl` | `05_accessories/smart_keyfob_pager.scad` |
| **Smart-Keyfob** | TPU Stoßdämpfer-Kantenband (Orange) | `05_accessories/smart_keyfob_tpu_rim.stl` | `05_accessories/smart_keyfob_pager.scad` |
| **Tasterhalter** | Under-Perch Tasterhalter für M4 Harley-Armatur | `05_accessories/under_perch_switch_bracket.stl` | `05_accessories/under_perch_switch_bracket.scad` |
| **Tasterhalter** | Spiegelschaft-Adapterplatte für M8/M10 | `05_accessories/under_perch_mirror_plate.stl` | `05_accessories/under_perch_switch_bracket.scad` |
| **Spiegel-Radar** | BSD Spiegel-Totwinkel-Pod Oberteil (38° Trichter) | `05_accessories/bsd_mirror_upper_pod.stl` | `05_accessories/bsd_mirror_indicator_pod.scad` |
| **Spiegel-Radar** | BSD Spiegel-Klemmschelle Unterteil (Ø 10 mm) | `05_accessories/bsd_mirror_lower_clamp.stl` | `05_accessories/bsd_mirror_indicator_pod.scad` |
| **Spiegel-Radar** | BSD Diffusorlinse (Bernstein / transluzent) | `05_accessories/bsd_mirror_lens.stl` | `05_accessories/bsd_mirror_indicator_pod.scad` |
| **Radar 2.0** | Wheeltec MR20 77GHz Gehäuse mit Binder M5 Flansch & Radome | `05_accessories/radar_mr20_housing.stl` | `05_accessories/radar_mr20_housing.scad` |
| **Kamera-Dock** | Road Glide ST Sharknose 15W Qi Induktives Cam-Dock (3M Dual Lock) | `05_accessories/road_glide_inductive_cam_dock.stl` | `05_accessories/road_glide_inductive_cam_dock.scad` |
| **Auto-Zubehör** | Begleitfahrzeug / Auto Universal Sonnenblenden-Clip für Pod 3 | `05_accessories/car_sun_visor_pod3_clip.stl` | `05_accessories/car_sun_visor_pod3_clip.scad` |
| **Kassette** | Universelle 2D-Langloch-Rasterplatte & seitliche Aktuator-Ausleger | `03_pod_cartridges/cartridge_universal_actuator_rails.stl` | `03_pod_cartridges/cartridge_universal_actuator_rails.scad` |

### 9.2 Baukasten-Komponenten & Dummies (`components/`-Verzeichnisse)

In den `components/`-Verzeichnissen liegen die isolierten Basiskörper (vor Differenzoperationen) und Zubehörteile:
- **`01_main_box/components/`**: `01_lower_tub_empty.stl`, `02_corner_screws_enclosure.stl`, `03_pcb_standoffs.stl`, `04_mounting_ears.stl`, `05_sealing_groove.stl`, `06_mid_tray_frame.stl`, `07_mid_partition_floor.stl`, `08_lid_plate.stl`, `dummy_main_pcb.stl`, `dummy_lipo_battery.stl`.
- **`02_pod_base/components/`**: `01_pod_tunnel_base.stl`, `02_pod_rear_m8_gland.stl`, `03_pod_bulkhead_partition.stl`, `04_pod_guide_grooves.stl`, `05_pod_strap_hooks.stl`, `06_fender_curved_saddle.stl`, `07_pod_slide_dock_core.stl`, `011_gopro_hirth_lock.stl` (Radiale Formschluss-Verzahnung), `dummy_m8_connector.stl`.
- **`03_pod_cartridges/components/`**: `dummy_adapter_pcb.stl`, `dummy_omm_transceiver_pcb.stl`.
- **`04_front_node/components/`**:
  - `01_front_node_base_tub.stl`: Monolithischer, abgerundeter Basiskörper mit ausgehöhlter Innenkammer (Grundquader im CSG-Verfahren).
  - `02_pcb_standoffs.stl`: 4x M2.5 Schraubdome für PCBA05.
  - `03_mounting_ears.stl`: 2x M4/M5 Schwingungsdämpfer-Flanschohren.
  - `dummy_front_node_pcb.stl`: 3D-Prüfdummy der PCBA05 mit Steckverbinder-Höhenprofilen.

---

## 10. Fertigungsspezifikation & 3D-Druck Parameter (HP MJF vs. FDM)

### 10.1 Industrieller 3D-Druck (HP MJF PA12)
* **Verfahren:** HP Multi Jet Fusion (MJF), schwarz eingefärbt, kugelgestrahlt und chemisch dampfgeglättet.
* **Toleranzen:** $\pm 0{,}15\,\text{mm}$ (DIN ISO 2768-m).
* **Eigenschaften:** Isotrope Zugfestigkeit $48\,\text{MPa}$, temperaturbeständig bis $+95\,^\circ\text{C}$, $100\,\%$ porenfrei.

### 9.2 Heimischer FDM-Druck (Bambu Lab / Prusa / Voron)
* **Materialien:** ASA oder PETG (niemals Standard-PLA!).
* **Wandlinien:** 4 bis 5 Perimeter ($1{,}6\dots 2{,}0\,\text{mm}$ massiv).
* **Infill:** $25\dots 40\,\%$ Gyroid.
* **Flow:** $102\dots 104\,\%$ zur Mikroporenabdichtung.
