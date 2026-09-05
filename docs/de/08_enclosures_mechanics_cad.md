# 08 - Mechanische Gehäuse, CAD-Konstruktion & Dichtungssystem (Alle Baugruppen)

Dieses Dokument spezifiziert die mechanische Konstruktion, das Thermomanagement, das IP67/IP69K-Gehäusedesign, die Kinematik des Auto-Eject-Schnellwechselsystems sowie alle CAD- und STL-Modelle aller Gehäuse-Baugruppen der OpenMotorBridge v8.0:
1. **Zentrale Steuerbox (Typ A):** 3-teiliges Sandwich-Gehäuse mit Zwischenboden, integrierter Akku-Wanne, stirnseitiger Schnittstellenleiste (HD26, USB-C, RGB-LED) und planarem 4-Layer Kupfer-Wärmespreader.
2. **Universelle Satelliten-Pods (Typ B):** Baugleiches 5-seitiges Monocoque-Schachtgehäuse für Pod 1, 2 und 3 mit $120^\circ$-V-Nut Rohrbett, M8 6-Pin IP67-Rückanschluss, Schutz-Schottwand und federbelastetem Auto-Eject.
3. **Modulare Wechselkassetten (Typ C):** Generischer 2-teiliger Universal-Basisschlitten mit asymmetrischer Poka-Yoke Nut-und-Feder-Führung für Sena 50S/60S, Cardo Packtalk Edge/Bold, OMM-Transceiver und hermetische IP67 Blindkassette (Dry Box).
4. **Heck-Pod 3 & Radar-Ausleger (Typ D):** Strömungsgünstiger Heckbürzel-Transceiver mit dielektrischem Antennenradom für 868 MHz LoRa und Multi-GNSS sowie winkelverstellbarem Halter für Totwinkel-Radar (Garmin Varia).
5. **Universal Front-Knoten (Typ E):** Ultrakompakter Cockpit- & Sensor-Hub ($84 \times 60 \times 23\,\text{mm}$) mit **4-in-1 Universal-Befestigungssystem** (AMPS, Rohrbügel-Prisma, Silentblöcke, 3M Dual-Lock), EPDM-Kabelkämmen und Knowles MEMS Akustikkanal.
6. **Fahrzeugspezifische Referenz-Montagekits (Zero-Drill):** Vollständig konstruierte, zerstörungsfreie Bolt-On Montagekits für CVO Road Glide ST (Kit 1), Road King Special (Kit 2), Classic Bagger & Cruiser (Kit 3) sowie Adventure & Touring Enduros (BMW GS, KTM Adventure, Africa Twin – Kit 4).

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

*Abbildung 8.2: 1:1:1 euklidische CAD-Explosionsdarstellung der Zentralbox entlang der vertikalen Z-Achse.*

### 1.3 3D-Röntgenansicht & Zusammenbau-Fitting

![OpenMotorBridge Zentralbox Mated 3D X-Ray CAD Fitting](../images/cad/main_box_assembly_mated_3d.png)

*Abbildung 8.3: Transparente 3D-Röntgenansicht der vollständig geschlossenen Zentralbox. Erkennbar sind die spielfreien Bauteilfreiräume, die geschützte Akku-Lagerung auf dem Zwischenboden, die durchgängige Konvektion über die 11 Zwischenbodenschlitze und der scheuerfreie Kabelverlauf zum HD26-Flansch.*

### 1.4 Maßstabsgetreuer Längs- & Querschnitt (X-Z Thermik & Y-Z Kabelführung)

![OpenMotorBridge Zentralbox Cross Sections](../images/cad/main_box_assembly_cross_section.png)

*Abbildung 8.4: Exakte 2D-Schnittansichten der Zentralbox (X-Z und Y-Z Ebenen).*

---

## 2. Thermomanagement & Planare PCB-Entwärmung (Kupferbolzenfrei)

Die Gesamtabwärme der Zentralbox liegt im normalen Fahrbetrieb bei lediglich **$\approx 1{,}5\,\text{W}$** (Peak bei maximaler Schnellladung: $2{,}45\,\text{W}$).

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

1. **Planarer 4-Layer Kupfer-Wärmespreader ($85 \times 55\,\text{mm}$):** Die beiden massiven $35\,\mu\text{m}$ Innenlagen der FR4-Platine leiten die Wärme blitzschnell ab ($\lambda = 390\,\text{W/(m}\cdot\text{K)}$).
2. **11x Optimierte Konvektionsschlitze im Zwischenboden:** 5 Schlitze an der Rückkante ($Y = 58\,\text{mm}$), 4 an den Flanken und 2 an der Front lassen die Luft ungehindert in die Deckelkammer aufsteigen.
3. **Thermische Sicherheitsmargen im Extrem-Stresstest (Stau bei $45\,^\circ\text{C}$ Hitze + $13\,^\circ\text{C}$ Motorwärme = $58\,^\circ\text{C}$ unter Sitz):**
   * **LM5164-Q1:** $T_j = 93{,}8\,^\circ\text{C}$ (Zulässig bis $+150\,^\circ\text{C}$ $\rightarrow$ $+56{,}2\,^\circ\text{C}$ Reserve).
   * **ESP32-S3:** $T_j = 90{,}2\,^\circ\text{C}$ (Zulässig bis $+105\,^\circ\text{C}$ $\rightarrow$ $+14{,}8\,^\circ\text{C}$ Reserve).
   * **3.3V LDO:** $T_j = 110{,}4\,^\circ\text{C}$ (Zulässig bis $+125\,^\circ\text{C}$).
   * **1S LiPo Akku:** Verbleibt in der oberen Kammer sicher unter $60\,^\circ\text{C}$ (JEITA-NTC pausiert Ladevorgang bei $> 45\,^\circ\text{C}$).

### 2.2 Oberwanne: 1S LiPo-Akkuaufnahme & Zwischenboden-Durchführungen
* **Integrierte LiPo-Akkutasche:** Auf der Oberseite des Zwischenbodens sitzt eine formschlüssige Aussparung ($55{,}0 \times 32{,}0 \times 8{,}5\,\text{mm}$) für eine 1000 mAh 1S LiPo-Pufferzelle (Typ 103040 oder 803048).
* **Vibrationssicherung:** Eine $1{,}0\,\text{mm}$ dämpfende EPDM-Schaumstoffmatte an der Unterseite und ein quer verlaufendes EPDM-Gummispannband ($35 \times 10\,\text{mm}$) über seitliche Einhängenocken halten die Zelle auch bei $20\,\text{g}$ Stößen absolut spielfrei.
* **4-Poliger JST-PH Akkuanschluss (`J3`):**
  * Pin 1: `VBAT+` ($+3{,}7\,\text{V}$ LiPo Pluspol über BQ24075)
  * Pin 2: `NTC_10K` (Murata 10k NTC Temperaturfühler für JEITA-Ladeüberwachung)
  * Pin 3: `GND` (LiPo Masse)
  * Pin 4: `NC` / Schirmung
* **Zwischenboden-Durchführungen:**
  * Zentraler Kabeldurchbruch ($14{,}0 \times 4{,}0\,\text{mm}$) mit beidseitig verrundeten Kanten ($R = 1{,}5\,\text{mm}$) zur knickfreien Führung des internen 2x13 Flachbandkabels von der Hauptplatine zum HD26-Flansch in der Stirnwand.
  * 2x Montagefenster für den Zugriff auf die M2.5 Befestigungsschrauben der Hauptplatine.

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

## 4. Gehäuse Typ B: Universeller Satelliten-Pod (Pod 1, 2 und 3)

Alle 3 Pod-Positionen nutzen dasselbe 5-seitige Monocoque-Schachtgehäuse im erweiterten Envelope ($135{,}0 \times 70{,}0 \times 38{,}0\,\text{mm}$):

![OpenMotorBridge Satelliten-Pod & Kassetten 3D Anschnitt CAD](../images/cad/pod_cartridge_cutaway_3d.png)

*Abbildung 8.5: Photorealistischer 3D-CAD-Schräganschnitt des Satelliten-Pods mit eingeschobener Wechselkassette. Gut zu erkennen sind die 120°-V-Nut mit EPDM-Spannringen um das Motorrad-Rahmenrohr, die M8 6-Pin-Buchse, die innere Schottwand mit den beiden komprimierten V4A-Edelstahlfedern, die asymmetrischen Poka-Yoke Gleitschienen mit 8 mm Höhenversatz, der 6-polige Goldkontakt-Eingriff (4,8 mm Wipe-Weg) und die formbündige Dichtung an der Frontblende.*

![OpenMotorBridge Satelliten-Pod CAD Explosionsdarstellung](../images/cad/openmotorbridge_pod_exploded_view.png)

*Abbildung 8.6: 3D-CAD-Explosionsdarstellung des universellen Satelliten-Pods.*

![OpenMotorBridge Satelliten-Pod Röntgenansicht](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Abbildung 8.7: 3D-Röntgen- und Transparenzdarstellung des geschlossenen Satelliten-Pods.*

### 4.1 Rohrbett-Prisma ($120^\circ$) & EPDM-Spannbefestigung
* **An der Unterseite:** $120^\circ$-V-Nut ($R = 15\,\text{mm}$) schmiegt sich formschlüssig an alle Rohre von $\varnothing 18\dots 35\,\text{mm}$ an ($1"$ Sturzbügel, $7/8"$ Heckrahmen).
* **4x Einhängenasen:** Blitzschnelle Montage mit 2 UV-beständigen EPDM-Gummiringen bei gleichzeitiger Schwingungsdämpfung.

### 4.2 Kinematik des Auto-Eject & Snap-Fit Systems

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

| Parameter | Berechneter Wert | Funktion & Sicherheitsnachweis |
| :--- | :---: | :--- |
| **Federrate (2x V4A Federn)** | **$2{,}4\,\text{N/mm}$** | Parallelschaltung zweier Edelstahl-Druckfedern (DIN EN 13906-1) |
| **Vorspannfederweg** | **$6{,}0\,\text{mm}$** | Kompression von $L_0 = 15\,\text{mm}$ auf $L_{\text{mated}} = 9\,\text{mm}$ |
| **Axiale Haltekraft (Preload)** | **$7{,}2\,\text{N}$** | Hält Dichtsitz permanent unter Druck gegen $20\,\text{g}$ Vibration |
| **Dichtungs-Gegenkraft** | **$4{,}5\,\text{N}$** | $30\,\%$ Kompression der umlaufenden $1{,}5\,\text{mm}$ Silikon-Dichtschnur |
| **Auszugskraft (Rückhalt)** | **$> 65\,\text{N}$** | Verhindert unbeabsichtigtes Lösen durch Zugbelastung am Kabel |
| **Entriegelungskraft (Squeeze)**| **$9{,}8\,\text{N}$** | Ergonomisch optimierter Daumen-Zeigefinger-Druck ($\approx 1\,\text{kg}$) |
| **Automatischer Auswurfhub** | **$9{,}0\,\text{mm}$** | Trennt 6-Pin Wipe ($4{,}8\,\text{mm}$) mit **$+4{,}2\,\text{mm}$ Überhub** |

#### 4.2.1 Die 4 kinematischen Bewegungsphasen des Kassetteneinschubs
1. **Phase 1 - Vorzentrierung ($x = 0\dots 80\,\text{mm}$):** Asymmetrische Führungsrippen greifen in die Gehäusenuten ein. Seitliches Spiel wird auf $\pm 0{,}2\,\text{mm}$ eingeengt.
2. **Phase 2 - Feder-Kompression ($x = 80\dots 86\,\text{mm}$):** Die Stirnseite des Schlittens trifft auf die beiden V4A-Auswerferfedern in der Schottwand. Die Federn bauen die $7{,}2\,\text{N}$ Vorspannkraft auf.
3. **Phase 3 - 6-Pin Kontakt-Eingriff & Schnapp-Rastung ($x = 86\dots 91\,\text{mm}$):** Die 6 Hartgold-Stifte dringen $4{,}8\,\text{mm}$ tief in die Doppelschenkel-Buchsenleiste ein (Wipe). Die $30^\circ$-Einlaufschrägen der Rastnasen spreizen die federnden PA12-Arme nach innen.
4. **Phase 4 - Formbündige Verriegelung ($x = 91\,\text{mm}$):** Die $85^\circ$-Sperrkanten der Rastarme schnappen mit hörbarem Klick in die Rasttaschen der Gehäusewand. Die Silikon-Dichtung wird um $30\,\%$ komprimiert.

#### 4.2.2 Spannungs- & Ermüdungsnachweis des PA12-Biegebalkens
* **Abmessungen:** Länge $L = 14{,}0\,\text{mm}$, Breite $b = 10{,}0\,\text{mm}$, Dicke $h = 1{,}8\,\text{mm}$, Auslenkung $\delta = 1{,}8\,\text{mm}$.
* **Maximale Randfaserdehnung:**
  $$\epsilon_{\max} = \frac{3 \cdot h \cdot \delta}{2 \cdot L^2} = \frac{3 \cdot 1{,}8\,\text{mm} \cdot 1{,}8\,\text{mm}}{2 \cdot (14{,}0\,\text{mm})^2} = \mathbf{1{,}38\,\%}$$
* **Zulässige Dauerdehnung für MJF PA12:** $\epsilon_{\text{zul}} \le 2{,}0\,\%$.
* **Biegespannung:** $\sigma_b = \epsilon_{\max} \cdot E_{\text{PA12}} = 0{,}0138 \times 1.700\,\text{MPa} = \mathbf{23{,}5\,\text{MPa}}$ (Weit unterhalb der PA12-Streckgrenze von $48\,\text{MPa} \rightarrow$ **Sicherheitsfaktor $S = 2{,}04$**).
* **Dauerfestigkeit:** Ausgelegt für $> 10.000$ Ver- und Entriegelungszyklen ohne plastische Verformung.

#### 4.2.3 Kontaktsicherheit & Wipe-Länge
* **Freie Stiftlänge:** $6{,}5\,\text{mm}$ Vierkant-Prägestifte ($0{,}64 \times 0{,}64\,\text{mm}$, $0{,}76\,\mu\text{m}$ Hartgold über Nickel).
* **Effektiver Wipe-Weg:** **$4{,}8\,\text{mm}$** Eingriff in die Buchsenleiste (übertrifft die USCAR-2 Kfz-Norm von $\ge 1{,}5\,\text{mm}$ um den **Faktor 3,2**).
* **Prellfreiheit:** $7{,}2\,\text{N}$ permanente Vorspannung verhindert Kontaktprellen selbst bei Vibrationen bis $20\,\text{g}$.

### 4.3 Asymmetrisches Poka-Yoke Nut-und-Feder Führungskonzept

![OpenMotorBridge Pod Poka-Yoke Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Abbildung 8.7: 3D-CAD-Querschnitt (Y-Z Ebene) durch das Satelliten-Pod-Gehäuse und den Kassetten-Grundschlitten. Sichtbar ist der $8{,}0\,\text{mm}$ Höhenversatz der Führungsnuten (Links: $Z=10{,}0\,\text{mm}$, Rechts: $Z=18{,}0\,\text{mm}$). Ein $180^\circ$-Falscheinbau ist mechanisch ausgeschlossen.*

---

## 5. Gehäuse Typ C: Modulare Wechselkassetten

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Abbildung 8.8: Die modularen Wechselkassetten-Varianten im Überblick: OMM Heck-Transceiver (vorne links), Sena 50S/60S Quick-Snap Cradle (vorne rechts), Cardo Magnetic Air Mount (hinten links) und wasserdichte IP67 Blindkassette (hinten rechts).*

### 5.1 Benutzerzentrierte Plug & Play Docking-Architektur (0 Lötaufwand)
Um Signale vom 90°-abgewinkelten **JST-SH 1.0 mm 6-Pin SMD-Steckverbinder (`J2`)** auf der Kassetten-Trägerplatine verwechslungs- und knickfrei zu den Kontaktpunkten des jeweiligen Adapters zu führen, besitzt der Kassetten-Schlitten:
* **Geschützten Unterflur-Kabelkanal:** Im Boden des PA12-Schlittens ist eine **$1{,}5\,\text{mm}$ tiefe und $8{,}0\,\text{mm}$ breite Kabelführung** direkt unterhalb des Konturbetts integriert.
* **Zwischenboden-Durchführung:** Ein präziser **$10{,}0 \times 3{,}0\,\text{mm}$ Durchbruch mit beidseitig $R=1{,}0\,\text{mm}$ verrundeten Kanten** führt das Flachbandkabel von Header `J2` auf der unteren Platine nach oben ins Nest.
* **Standardisierte Pin-Belegung am JST-SH 6P Header (`J2`):**

| Pin | Signal-Name | Funktion am Headset-Adapter | Sena 50S/60S Pad | Cardo Edge Pad | Midland XT / PMR |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Gemeinsamer Massebezug | Pin 1 (GND) | Pin 1 (GND) | Masse / Shield |
| **2** | `5V_VBUS` | Gefilterte Ladespeisung (500mA PTC) | Pin 2 (USB-5V) | Pin 2 (5V Charge)| 5V DC In |
| **3** | `AUDIO_R+` | Audio Diff-Out + (zum Lautsprecher-In) | Pin 4 (Spk R+) | Pin 3 (Spk +) | Speaker In + |
| **4** | `AUDIO_R-` | Audio Diff-Out - (Lautsprecher-Rückleiter)| Pin 5 (Spk R-) | Pin 4 (Spk -) | Speaker In - |
| **5** | `MIC_IN+` | Audio Diff-In + (vom Mikrofon-Out) | Pin 6 (Mic +) | Pin 5 (Mic +) | Mic Out + |
| **6** | `OPTO_PTT` | Optokoppler PTT / Button Synthesis | Pin 7 (Mesh-Btn)| N/C (Aux) | PTT Switch |

### 5.2 Sena 50S / 60S Kontur-Nest & Snap-Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Abbildung 8.9: CAD-Visualisierung der Sena 50S/60S Wechselkassette mit federnder 7-Pin Pogo-Kontaktleiste.*

### 5.3 Sena +Mesh & Universal Slide-Inlay (Klasse A mit externem Antennenanschluss)
Für das Sena +Mesh (oder andere OEM-Adapter mit Antennen- und Ladeanschluss) bietet die Kassetten-Frontblende (`00_base_sled.scad` & `01_insert_sena.scad`):
* **100 % zerstörungsfreie Nutzung des ungeöffneten OEM-Geräts:** Das Sena +Mesh wird im Originalgehäuse belassen.
* **Formschlüssiges Schlitten-Inlay:** Bildet exakt die OEM-Rahmenbefestigungsplatte mit 2x Quer-Schiebestegen (Hakenabstand $30\,\text{mm}$) und federnder Rastzunge ab.
* **Integrierte SMA-Flansch-Bohrung ($\varnothing\,6{,}5\,\text{mm}$):** Mit zylindrischer O-Ring-Dichtsenkung ($\varnothing\,9{,}5 \times 1{,}2\,\text{mm}$) an der Deckelstirnseite für eine IP67 SMA-Flansch-Doppelbuchse (Female-to-Female).
* **Interner Koax-Kabelkanal:** Ausgesparter Durchbruch im Schlittenboden für die biege- und knickfreie Führung des internen $8\,\text{cm}$ RG-178 Pigtails (mit 90°-SMA-Winkelstecker zum Sena +Mesh).
* **EPDM-Spannband-Aufnahme:** Einhängehaken für ein elastisches EPDM-Gummiband ($35 \times 10\,\text{mm}$), das den Adapter vibrationsfest im Negativbett sichert.
* **Elektrische Speisung:** Flaches 90° Micro-USB / USB-C Pigtail von Pin 1 (`GND`) und Pin 2 (`5V_VBUS`) des JST-SH Headers `J2`.

### 5.4 Cardo Packtalk Edge / Pro Magnetic Air Mount
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Abbildung 8.10: CAD-Visualisierung der Cardo Packtalk Edge Wechselkassette mit N52-Neodym-Magnetsitz und 5 gefederten Kontaktpads.*

### 5.5 Cardo Packtalk Bold / Black Edition
Nutzt die formschlüssigen Schiebe-Gegenkontakte der originalen Cardo-Audiokit-Basisplatte. Das Gerät wird von oben in die mechanische Führung geschoben und federnd arretiert.

### 5.6 Midland BT Mini / BTR1 Advanced & XT30 Slide
* **Midland Intercom Edition (BTR1 / Rush / BT Mini):** Kontur-Aufnahme für Midland Bluetooth- und Wave-Mesh-Intercoms ($70\dots 85\,\text{mm}$ Baubreite).
* **Midland XT Bare-Board Edition:** Nimmt die entkernte Platine eines kompakten Handfunkgeräts (XT10/XT30/G5, $\approx 68 \times 42 \times 10\,\text{mm}$) direkt auf.

### 5.7 PMR446 Transceiver & Bare-Board Modul (SA818S / RDA1846)
Vollständig integriertes 500 mW PMR446-Analogfunkmodul ($38 \times 20\,\text{mm}$) direkt auf der Kassetten-Trägerplatine – wahlweise mit interner 446-MHz-Helix oder robuster SMA-Frontbuchse für große Distanzen.

### 5.8 Längsschnitt-Vergleich Sena & Cardo
![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Abbildung 8.11: 2D-Längsschnitt (X-Z Ebene) durch die Sena 50S (oben) und Cardo Packtalk Edge (unten) Kassetten im geschlossenen Pod.*

### 5.9 IP67 Blind- / Leerkassette (Dry Box Dummy)
![OpenMotorBridge IP67 Blindkassette 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

*Abbildung 8.12: Formidentische IP67 Blindkassette mit integriertem $80 \times 46 \times 16\,\text{mm}$ Notfall-Trockenstaufach.*

---

## 6. Belegung der 6-Pin M8 / Pogo-Schnittstelle & PUR-Kabelbaum-Farbcodierung

| M8 / Pogo-Pin | Leitungsfarbe (PUR-Kabel) | Querschnitt | Signal Pod 1 & 2 (Audio & Intercom) | Signal Pod 3 (Heck-Transceiver) | Schirmung & Verdrillung |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **Pin 1** | **Rot (RD)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`VCC`** (5V geschaltete Speisung via MOSFET) | **`VCC`** (5V Versorgung) | Einzelader (Power) |
| **Pin 2** | **Schwarz (BK)** | $0{,}34\,\text{mm}^2$ (AWG22) | **`GND`** (Dedizierte Power- & Signalmasse) | **`GND`** (Dedizierte Power- & Signalmasse) | Einzelader (Power Ground) |
| **Pin 3** | **Weiß (WH)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_P`** (Symmetrisches Audio + via Bourns) | **`UART_TX`** (Heck-Co-Prozessor $\rightarrow$ Box) | **Paar 1 verdrillt** (mit Pin 4) |
| **Pin 4** | **Blau (BU)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`NF_N`** (Symmetrisches Audio - via Bourns) | **`UART_RX`** (Box $\rightarrow$ Heck-Co-Prozessor) | **Paar 1 verdrillt** (mit Pin 3) |
| **Pin 5** | **Gelb (YE)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`OPTO`** (TLP222A Tastensimulations-Trigger) | **`GNSS_PPS`** (1-PPS Hardware-Zeitnormal) | Einzelader (Steuersignal) |
| **Pin 6** | **Grün (GN)** | $0{,}14\,\text{mm}^2$ (AWG26) | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Heck-Kassetten-ID) | Einzelader (1-Wire Bus) |
| **M8-Gehäuse**| **Kupfergeflecht (BL)**| $> 85\,\%$ Geflecht | **`GND_SHIELD`** (360° Gehäuseschirmung) | **`GND_SHIELD`** (360° Gehäuseschirmung) | Gesamtschirm über M8-Metallkragen |

---

## 7. Gehäuse Typ D: Heck-Pod 3 Transceiver (Backbone & Telemetrie)

Der Heck-Pod 3 vereint den OMM-Transceiver, 868 MHz LoRa und Multi-GNSS (`PCBA 04`, RP2040) in geschützter Heckposition. 

> [!IMPORTANT]
> **Architektonische Modularität (Typ-B-Unantastbarkeit):**
> Das universelle Schachtgehäuse von Pod 3 (Typ B, $135 	imes 70 	imes 38{,}5\,	ext{mm}$ Außenmaße, $100 	imes 60 	imes 28\,	ext{mm}$ Innenraum) bleibt über alle Motorradtypen hinweg **zu 100 % baugleich und unverändert**. Die Aufnahme der Telemetrie- und Funkhardware erfolgt über die standardisierte OMM-Transceiver-Wechselkassette (`cartridge_antenna_bracket_omm.stl` / `04_antenna_bracket_omm.scad`). Die fahrzeugspezifische Adaption an Kotflügel, Gepäckbrücken oder Heckrahmen erfolgt ausschließlich über externe Montagekonsolen oder Haltesysteme.

![Pod 3 Transceiver & Radar 3D Anschnitt CAD](../images/cad/pod3_radar_cutaway_3d.png)

*Abbildung 8.13: Photorealistischer 3D-CAD-Schräganschnitt des Heck-Pods 3 mit montiertem Blind-Spot Radarsensor. Sichtbar sind das dielektrische Radom mit Gore-Membran, die 25x25 mm Keramik-Patchantenne, die 868 MHz LoRa-Wendelantenne, die 4-Layer-Platine mit RP2040 und SX1262, der M8 6-Pin-Anschluss sowie der integrierte M5-GoPro-Ausleger mit verstellbarem Garmin Varia Radarkopf.*

![Pod 3 Full Assembly Exploded 3D](../images/cad/pod3_full_assembly_exploded_3d.png)

*Abbildung 8.14: CAD-Explosionsdarstellung des Heck-Pods 3 mit Antennen-Radom, Platine und M8-Bajonettsockel.*

![Pod 3 Assembly Cross Section](../images/cad/pod3_assembly_cross_section.png)

*Abbildung 8.15: Längsschnitt durch den Heck-Pod 3 mit koaxial geschirmter Antennenkammer und $25 	imes 25\,	ext{mm}$ GNSS-Groundplane.*

---

## 8. Gehäuse Typ E: Universal Front-Knoten (Cockpit- & Sensor-Hub)

Das Gehäuse des Front-Knotens wurde speziell für die geschützte Montage in Motorrad-Frontverkleidungen (Batwing, Sharknose, BMW GS/RT Schnabel) oder an Sturzbügeln entwickelt:

- **Außenabmessungen:** Ultrakompakte **$84{,}0 	imes 60{,}0 	imes 23{,}0\,	ext{mm}$** (L x B x H).
- **Material:** HP Multi Jet Fusion (MJF) PA12, schwarz kugelgestrahlt und chemisch geglättet.
- **Schutzart:** IP67 (tauch- und strahlwasserdicht).

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Abbildung 8.16: Geschlossenes Front-Node IP67-Gehäuse.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Abbildung 8.17: 3D-Explosionsdarstellung des Front-Knotens entlang der Z-Achse.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Abbildung 8.18: Transparente 3D-Schnittansicht des Front-Knotens mit Knowles MEMS Schallkanal und VBUS-Lastschalter.*

### 8.1 Das 4-in-1 Universal-Befestigungssystem des Front-Knotens

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Abbildung 8.19: Gehäuseunterseite des Front-Knotens mit AMPS-Bohrbild, $120^\circ$ V-Nut Rohrbett, EPDM-Spannnasen, Silentblock-Lochungen und 3M Dual-Lock Klettnuten.*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   DAS 4-IN-1 UNIVERSAL-BEFESTIGUNGSSYSTEM (BODENANSICHT)               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. AMPS-LOCHBILD (30 x 38 mm):                                                         │
│    • 4x M4 Messing-Gewindeeinsätze (Ruthex) im Standard-AMPS-Raster                    │
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

---

## 9. Fahrzeugspezifische Referenz-Montagekits (Zero-Drill / Bolt-On)

Während die 5 Hardware-Gehäuse (Typ A bis E) zu **100 % universell und einheitlich standardisiert** sind, liefert OpenMotorBridge für ausgewählte Motorradplattformen komplett durchentwickelte, schraub- und klebefreie Referenz-Montagekits. Diese nutzen originale Werksbefestigungspunkte oder elastische Spannsysteme, um das Gesamtsystem ohne Lackschäden oder irreversible Karosseriebohrungen perfekt ins Fahrzeug zu integrieren.

---

### 9.1 Referenz-Kit 1: Harley-Davidson CVO Road Glide ST (2024+) & New Touring Platform

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
* **Skeleton Dock (`cvo_st_undercowl_skeleton_dock.scad`):** Nimmt das Standard-Pod-3-Gehäuse ($135 	imes 70 	imes 38{,}5\,	ext{mm}$) aufrecht auf. Zwei nach oben gewölbte Federbögen stützen sich an der Innendecke der Carbonhutze ab und verhindern jedes Aufbäumen oder Klappern über Schlaglöchern und Kopfsteinpflaster.
* **Telemetrie-Finne (`cvo_st_telemetry_fin.scad`):** Sitzt auf der originalen hinteren Schraublasche der Hutze. Sie führt die 2,4-GHz-Mesh-Antenne des ESP32-C3 nach draußen an die frische Luft und leitet das Koaxialkabel unsichtbar unter der Lasche in die Hutze.

#### B. Kofferdeckel-Integration: Pod 1 (Links) & Pod 2 (Rechts)
* **Top-Lid Montage:** Beide Pods sitzen im vorderen Drittel der Kofferdeckel, verschraubt an den originalen Torx-Punkten der Scharnier- bzw. Fangbandhalterung (siehe [Abschnitt 9.5](#95-universal-kofferdeckel-dock-saddlebag_lid_dockscad)).
* **Gepäck- und Getränke-Sicherheit:** Liegen ca. $30\,	ext{cm}$ über dem Kofferboden. Schwere Kaltgetränke, Werkzeug oder feuchte Kleidung am Boden liegen vollständig unterhalb der Funk-Fresnel-Zone.
* **Maximale HF-Isolation ($> 40\,	ext{dB}$):** Sena (links) und Cardo (rechts) sind über $60\,	ext{cm}$ voneinander getrennt, mit Heckfender und Rahmen als HF-Schild.

---

### 9.2 Referenz-Kit 2: Harley-Davidson Road King Special (FLHRXS / Classic Naked Touring)

Für klassische Touring-Modelle ohne Frontverkleidung und mit 2-Up-Komfortsitzbank oder klassischem Heckfender:

```
             ROAD KING SPECIAL (RKS) GESAMTSYSTEM-INTEGRATION
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT (Nacelle, unsichtbar hinter 7" LED-Scheinwerfer):                │
│    • Front-Node (PCBA 05) im Hohlraum der Aluminium-Headlight-Nacelle       │
│    • Speist Garmin Navi / Smartphone-Halterung & Action-Cam am Lenker       │
│    • PTT-Lenkertaster & Knowles Windgeräusch-Mikrofon                       │
│    • 100 % drahtlos via ESP-NOW zur Zentralbox -> 0 Kabel am Tank nach hinten│
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. MITTE (Unter Sitzbank):                                                  │
│    • Zentralbox mittig im Batteriefach                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. HECK (Kotflügel-Konsole & Kennzeichen):                                  │
│    • Pod 3 in der Touring Fender Console (pod3_touring_fender_console.scad)  │
│      Formvollendet auf Kotflügel geschraubt an 1/4"-20 Soziussitz-Mutter    │
│    • Radar mittig unter dem Kennzeichen                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. KOFFER:                                                                  │
│    • Pod 1 (Sena) & Pod 2 (Cardo) in den Kofferdeckeln (analog ST)          │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Touring Fender Console (`pod3_touring_fender_console.scad`):** Organische Tropfenform ($R = 6\dots 7\,	ext{mm}$), die das Pod 3 formschlüssig aufnimmt. Nutzt die originale $1/4"-20$ Rändelmutter im Kotflügel. M8-Kabel taucht unsichtbar nach vorne unter die Sitzbank ab.
* **Headlight Nacelle Front-Knoten:** Nutzt den gigantischen Raum hinter dem 7"-LED-Scheinwerfer. Stromversorgung über den dort liegenden Harley-Zubehörstecker.

---

### 9.3 Referenz-Kit 3: Classic Bagger & Cruiser (Touring Stealth Console)

Für Harley-Davidson Street Glide, Electra Glide und Ultra Limited mit 2-Up-Komfortsitzbank:

![Pod 3 Touring Stealth Console CAD](../images/cad/pod3_touring_stealth_cad.png)

*Abbildung 8.20: Isolierte 3D-CAD-Ansicht der Touring Stealth Console (`pod3_touring_stealth_console.scad`). Vollständig organisch verrundete Konturen ($R = 6\dots 7\,	ext{mm}$) ohne harte Boxkanten. Vordere Montagelasche für die originale $1/4"-20$ Soziussitz-Schraube im Schutzblech, anschmiegende Sitzbankkontur mit M8-Kabelkanal nach vorne unter die Bank, Anbindung der Frontschräge auf halber Einschubhöhe ($Z = 22\,	ext{mm}$), offenes zentrales Dock und sanft abfallender Teardrop-Heckbürzel mit integrierter Einklips-Nut für die Heckantenne.*

![Pod 3 Fender Assembly Touring 3D](../images/cad/pod3_fender_assembly_touring_3d.png)

*Abbildung 8.21: Fotorealistische Gesamtheck-Montage an der Classic Touring-Maschine: Nahtlose Anschmiegung an die Beifahrersitzbank, M8-Kabel unsichtbar nach vorne geführt, freiliegendes Pod-Dach für ungestörten GNSS-Empfang, Kassetteneinschub von hinten und entkoppeltes Garmin Varia Radar unter dem Kennzeichen.*

---

### 9.4 Referenz-Kit 4: Adventure & Touring Enduros (BMW GS, KTM Adventure, Africa Twin)

Für großvolumige Reiseenduros und Naked Bikes mit offenem Gitterrohrrahmen, Rohrheck oder Aluminium-Gepäckbrücke:

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
│    • Zentralbox spritzwassergeschützt im Batteriefach                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. HECK (Gepäckbrücke / Rohrheck):                                          │
│    • Pod 3 mit integrierter 120°-V-Nut direkt auf Heckträger / Rohrrahmen   │
│    • Befestigung mit 2x wetterfesten EPDM-Spannringen oder Kabelbindern     │
│    • Blind-Spot Radar direkt am integrierten M5-GoPro-Ausleger des Pod 3    │
│      (optimale Bodenfreiheit, keine Hecküberstände)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. STURZBÜGEL (Links & Rechts):                                             │
│    • Pod 1 (Sena) links am Sturzbügel (120°-V-Nut für Ø 22..32 mm Rohre)    │
│    • Pod 2 (Cardo) rechts am Sturzbügel (EPDM-Spannringe)                   │
│    • Höchste HF-Isolation (> 40 dB) durch massiven Tank & Motorblock       │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **V-Nut Rohrbett ($120^\circ$-Prisma):**
  Die Gehäuseunterseite von Pod 1, 2 und 3 besitzt eine integrierte Hohlkehle ($R=15\,	ext{mm}$), die sich spielfrei an alle gängigen Sturzbügel- und Gepäckträgerrohre ($arnothing 18\dots 35\,	ext{mm}$, z. B. $22\,	ext{mm}$ oder $25{,}4\,	ext{mm} / 1"$) anschmiegt.
* **Integrierter M5-GoPro-Radarausleger an Pod 3:**
  Anders als bei tiefen Cruisern und Baggern erfordern Reiseenduros keine Entkopplung des Radars unter das Kennzeichen: Durch die hohe Sitzposition und die steile Heckgeometrie sitzt das Radar am schwenkbaren M5-GoPro-Arm direkt an der Pod-3-Basisplatte in optimaler Erfassungshöhe ($80\dots 100\,	ext{cm}$) mit freiem Radar-Öffnungswinkel über dem Hinterrad.

---

### 9.5 Universal Kofferdeckel-Dock (`saddlebag_lid_dock.scad`)

Das universelle Kofferdeckel-Dock ([`saddlebag_lid_dock.scad`](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad)) wurde speziell für die geschützte, vibrationsfeste und 100 % zerstörungsfreie Innenmontage der Satelliten-Pods 1 (Sena Mesh) und 2 (Cardo DMC) in Motorrad-Seitenkoffern entwickelt (Referenz: Harley-Davidson One-Touch Hartschalenkoffer 2014–2024+):

![Universal Saddlebag Lid Dock CAD](../images/cad/saddlebag_lid_dock_iso.png)

*Abbildung 8.22: 3D-CAD-Visualisierung des Kofferdeckel-Docks (`saddlebag_lid_dock.scad`). Sichtbar sind der inboard gerichtete Torx-Montageflansch für die originalen Scharnierschrauben, die frontale M8-Kabelschnauze mit Zugentlastung, die umlaufende Halbschale mit EPDM-Spannbandschlitzen und die obere Tropfkante über dem Kassetteneinschub.*

#### 9.5.1 Zero-Drill-Befestigung & Mechanisches Konzept
1. **Nutzung originaler Befestigungspunkte (Zero-Drill):**
   * Der $4\,	ext{mm}$ dicke Montageflansch greift die beiden werksseitigen M5 / Torx T20-Schrauben des Scharnier- bzw. Fangbandbeschlags ab (Lochabstand $52\,	ext{mm}$).
   * Großzügige Langlöcher ($arnothing 5{,}6 	imes 9{,}0\,	ext{mm}$) ermöglichen den Ausgleich von Fertigungstoleranzen der ABS-Koffer.
   * **Keine Bohrungen im Koffer:** Das Motorrad und die Koffer bleiben zu 100 % im unversehrten Originalzustand (Werterhalt & Dichtigkeit garantiert).
2. **Alternative / Zusätzliche Klebemontage (3M VHB):**
   * Auf der Unterseite sind vier definierte Taschen ($18 	imes 12 	imes 0{,}8\,	ext{mm}$) für 3M VHB Hochleistungs-Acrylatschaum-Klebebänder eingelassen, um eine optionale Montage an glatten Kofferinnenwänden anderer Hersteller (z. B. BMW Vario- oder Alukoffer) zu ermöglichen.
3. **Halbschalen-Architektur ($H = 26\,	ext{mm}$):**
   * Die $3\,	ext{mm}$ dicke PA12-Wanne umschließt das Pod 3-Gehäuse ($135 	imes 70 	imes 38\,	ext{mm}$) formschlüssig bis auf halbe Höhe.
   * Die modulare Wechselkassette bleibt von hinten voll zugänglich und kann mit Daumen und Zeigefinger in Sekunden entriegelt und gewechselt werden, ohne das Dock zu demontieren.
4. **Schutz vor Tropfwasser (Overhead Drip Lip):**
   * Über dem Kassetteneingang kragt eine integrierte **Tropfkante ($16 	imes 2\,	ext{mm}$ mit $30^\circ$-Dachschräge)** aus. Sie leitet Kondenswasser oder herablaufende Regentropfen beim Öffnen des Kofferdeckels zuverlässig seitlich an der Kassetten-Dichtfuge vorbei.
5. **Vibrationsfeste EPDM-Sicherung:**
   * Zwei seitliche Durchbrüche ($25 	imes 3\,	ext{mm}$) nehmen ein elastisches Spannband auf, das den Pod bei harten Fahrbahnschlägen spielfrei in der Wanne arretiert.

#### 9.5.2 Kabelführung & Schnelle Kofferdemontage
* **Integrierte M8-Zugentlastung:** An der Vorderseite führt eine trichterförmige Schnauze das M8-PUR-Kabel verwechslungssicher ab. Zwei Kabelbinderkanäle sichern den Kabelmantel gegen Zugbelastung.
* **Führung am Fangband:** Das Kabel verläuft parallel zum textilen Deckel-Fangband nach unten in das Kofferinnere. Es wird beim Öffnen und Schließen des Deckels weder gequetscht noch auf Torsion beansprucht.
* **Wasserdichte M8-Schnellkupplung:** Im oberen Kofferspalt (unterhalb der Sitzbankkante) ist eine M8-Trennstelle integriert. Die Koffer können somit bei Servicearbeiten oder zum Waschen mit einem einzigen Handgriff elektrisch getrennt und wie gewohnt abgenommen werden.

#### 9.5.3 HF-Physik: Warum Kofferdeckel statt Kofferboden?

Die Platzierung der Intercom-Pods im Kofferdeckel ($pprox 70\dots 75\,	ext{cm}$ über Fahrbahnniveau) löst fundamentale hochfrequenztechnische Probleme:

| Kriterium | Montage am Kofferboden / Seitenwand | Montage im Kofferdeckel (OpenMotorBridge) | Physikalische Begründung |
| :--- | :--- | :--- | :--- |
| **Flüssigkeitsdämpfung** | **Massive Dämpfung ($> 20\,	ext{dB}$)** | **Keine Dämpfung ($0\,	ext{dB}$)** | 2,4 GHz ist die Resonanzfrequenz von Wasser ($2\dots 4\,	ext{dB/cm}$ Verlust). Kalte Getränkedosen / Wasserflaschen liegen am Boden und blockieren die Line-of-Sight (LOS). Im Deckel liegt der Pod weit über dem Gepäck. |
| **Fresnel-Zonen-Höhe** | Bodennah ($30\,	ext{cm}$), starke Reflexion an Asphalt | Optimal ($70\dots 75\,	ext{cm}$ über Asphalt) | Die erste Fresnel-Zone zu Gruppenmitgliedern (Helme auf $1{,}2\dots 1{,}5\,	ext{m}$) bleibt frei von Bodenhindernissen und Fahrbahninterferenzen. |
| **Gehäuse-Dämpfung** | ABS-Kofferwand ($< 0{,}2\,	ext{dB}$) | ABS-Kofferdeckel ($< 0{,}2\,	ext{dB}$) | ABS-Kunststoff ist für 2,4 GHz dielektrisch nahezu transparent ($\epsilon_r pprox 2{,}6$, $	an\delta pprox 0{,}005$). |
| **Schließgestänge** | Im Schwenkbereich | $> 15\,	ext{cm}$ Abstand zum Gestänge | Die metallische One-Touch Striker Bar reflektiert nur lokal und verursacht bei $\lambda = 12{,}5\,	ext{cm}$ keinerlei Abschattung nach vorne/oben. |
| **HF-Entkopplung** | $< 20\,	ext{dB}$ bei benachbarter Montage | **$> 40\,	ext{dB}$ Raumdiversität** | Sena (linker Koffer) und Cardo (rechter Koffer) sind $> 60\,	ext{cm}$ getrennt; Heckfender und Rahmen dienen als HF-Schirm $\implies$ 0 De-Sensing. |

---

### 9.6 Entkoppeltes Kennzeichen-Radar-Bracket & Rechtliche Konformität

Auf Cruisern und Baggern wird das Garmin Varia mmWave-Radar von Pod 3 **entkoppelt** und mittig unter dem Kennzeichen montiert:

![Radar License Plate Bracket CAD](../images/cad/radar_license_plate_bracket_cad.png)

*Abbildung 8.23: 3D-CAD-Modell des entkoppelten Kennzeichen-Radarhalters mit M6-Klemmung, M5-Schwenkscharnier und verdecktem rückseitigem M8-Kabelkanal.*

* **Rechtliche Vorschrift (§ 10 Abs. 6 FZV / ECE R138):**
  Das Kennzeichen muss von oben in einem vertikalen Winkel von **mindestens $+30^\circ$ vollständig und ohne Verdeckung** einsehbar sein.
* **Vermeidung des Dachüberstand-Problems:**
  Durch die Platzierung des Radars **unter** dem Kennzeichen muss die obere Pod-Konsole nicht weit nach hinten auskragen. Der $+30^\circ$-Sichtbereich auf die Zulassungs- und TÜV-Plaketten bleibt zu $100\,\%$ frei.
* **Schwingungs- und Vibrationsfestigkeit:**
  Das Radar sitzt direkt an der massiven Grundplatte ohne langen Hebelarm – vollkommen vibrationsfest gegen die Vibrationen des Milwaukee-Eight 117 cui Motors.
* **Verdeckte Kabelführung:**
  Das M8-Signalkabel des Radars verläuft unsichtbar in einem rückseitig eingeformten Schacht hinter dem Kennzeichen nach oben und vereinigt sich hinter der Blinkerbrücke mit dem Heckkabelbaum.

---

## 10. CAD-Dateistruktur & OpenSCAD-Modulbaukasten (STL-Bibliothek)

Die CAD-Dateistruktur von OpenMotorBridge folgt einer strengen hierarchischen CSG-Architektur (Constructive Solid Geometry):
- **Hauptverzeichnisse (`01_main_box/`, `02_pod_base/`, `03_pod_cartridges/`, `04_front_node/`)**: Enthalten **ausschließlich monolithische, direkt 3D-druckbare Produktions-STLs** (100 % single-manifold, wasserdicht, 0 frei schwebende Körper).
- **Unterordner (`components/`)**: Enthalten die parametrischen CSG-Einzelkomponenten (z. B. unbeschnittene Basiskörper, Flansche, Schraubdome, Dichtkämme und PCB-/Akku-Dummies) für Baugruppenmontagen und modulare Adaptionen.

### 10.1 Druckfertige Produktions-STLs (Hauptverzeichnisse)

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
| **Radarhalter** | Entkoppelte Kennzeichen-Radarhalterung | `02_pod_base/radar_license_plate_bracket.stl` | `02_pod_base/radar_license_plate_bracket.scad` |
| **Kassette** | Universeller Basisschlitten mit Dichtung | `03_pod_cartridges/cartridge_base_sled.stl` | `03_pod_cartridges/00_base_sled.scad` |
| **Kassette** | Sena 50S/60S Adapterkassette | `03_pod_cartridges/cartridge_insert_sena.stl` | `03_pod_cartridges/parts/01_insert_sena.scad` |
| **Kassette** | Cardo Packtalk Edge Adapterkassette | `03_pod_cartridges/cartridge_insert_cardo.stl` | `03_pod_cartridges/parts/02_insert_cardo.scad` |
| **Kassette** | IP67 Blindkassette (wasserdichte Dry Box)| `03_pod_cartridges/cartridge_insert_blindkassette.stl` | `03_pod_cartridges/parts/03_insert_blindkassette.scad` |
| **Kassette** | OMM Dipol-Antennenhalterung | `03_pod_cartridges/cartridge_antenna_bracket_omm.stl` | `03_pod_cartridges/parts/04_antenna_bracket_omm.scad` |
| **Front-Knoten** | Unterwanne mit 4-in-1 Boden & Ohren | `04_front_node/front_node_lower_tub.stl` | `04_front_node/00_front_node_tub.scad` |
| **Front-Knoten** | Gehäusedeckel mit LED & FPC-Tasche | `04_front_node/front_node_upper_lid.stl` | `04_front_node/01_front_node_lid.scad` |
| **Front-Knoten** | EPDM/TPU Dichtkamm-Paar mit Steg | `04_front_node/front_node_cable_glands_tpu.stl` | `04_front_node/02_front_node_cable_glands.scad` |
| **Front-Knoten** | TPU USB-C Staubschutzstopfen | `04_front_node/front_node_usbc_cap_tpu.stl` | `04_front_node/03_front_node_usbc_plug.scad` |

### 10.2 Baukasten-Komponenten & Dummies (`components/`-Verzeichnisse)

In den `components/`-Verzeichnissen liegen die isolierten Basiskörper (vor Differenzoperationen) und Zubehörteile:
- **`01_main_box/components/`**: `01_lower_tub_empty.stl`, `02_corner_screws_enclosure.stl`, `03_pcb_standoffs.stl`, `04_mounting_ears.stl`, `05_sealing_groove.stl`, `06_mid_tray_frame.stl`, `07_mid_partition_floor.stl`, `08_lid_plate.stl`, `dummy_main_pcb.stl`, `dummy_lipo_battery.stl`.
- **`02_pod_base/components/`**: `01_pod_tunnel_base.stl`, `02_pod_rear_m8_gland.stl`, `03_pod_bulkhead_partition.stl`, `04_pod_guide_grooves.stl`, `05_pod_strap_hooks.stl`, `06_fender_curved_saddle.stl`, `07_pod_slide_dock_core.stl`, `dummy_m8_connector.stl`.
- **`03_pod_cartridges/components/`**: `dummy_adapter_pcb.stl`, `dummy_omm_transceiver_pcb.stl`.
- **`04_front_node/components/`**:
  - `01_front_node_base_tub.stl`: Monolithischer, abgerundeter Basiskörper mit ausgehöhlter Innenkammer (Grundquader im CSG-Verfahren).
  - `02_pcb_standoffs.stl`: 4x M2.5 Schraubdome für PCBA05.
  - `03_mounting_ears.stl`: 2x M4/M5 Schwingungsdämpfer-Flanschohren.
  - `dummy_front_node_pcb.stl`: 3D-Prüfdummy der PCBA05 mit Steckverbinder-Höhenprofilen.

---

## 11. Fertigungsspezifikation & 3D-Druck Parameter (HP MJF vs. FDM)

### 11.1 Industrieller 3D-Druck (HP MJF PA12)
* **Verfahren:** HP Multi Jet Fusion (MJF), schwarz eingefärbt, kugelgestrahlt und chemisch dampfgeglättet.
* **Toleranzen:** $\pm 0{,}15\,\text{mm}$ (DIN ISO 2768-m).
* **Eigenschaften:** Isotrope Zugfestigkeit $48\,\text{MPa}$, temperaturbeständig bis $+95\,^\circ\text{C}$, $100\,\%$ porenfrei.

### 11.2 Heimischer FDM-Druck (Bambu Lab / Prusa / Voron)
* **Materialien:** ASA oder PETG (niemals Standard-PLA!).
* **Wandlinien:** 4 bis 5 Perimeter ($1{,}6\dots 2{,}0\,\text{mm}$ massiv).
* **Infill:** $25\dots 40\,\%$ Gyroid.
* **Flow:** $102\dots 104\,\%$ zur Mikroporenabdichtung.
