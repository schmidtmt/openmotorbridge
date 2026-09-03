# 08 - Mechanische Gehäuse, CAD-Konstruktion & Dichtungssystem (Alle Baugruppen)

Dieses Dokument spezifiziert die mechanische Konstruktion, das Thermomanagement, das IP67/IP69K-Gehäusedesign, die Kinematik des Auto-Eject-Schnellwechselsystems sowie alle CAD- und STL-Modelle aller Gehäuse-Baugruppen der OpenMotorBridge v8.0:
1. **Zentrale Steuerbox (Typ A):** 3-teiliges Sandwich-Gehäuse mit Zwischenboden, integrierter Akku-Wanne, stirnseitiger Schnittstellenleiste (HD26, USB-C, RGB-LED) und planarem 4-Layer Kupfer-Wärmespreader.
2. **Universelle Satelliten-Pods (Typ B):** Baugleiches 5-seitiges Monocoque-Schachtgehäuse für Pod 1, 2 und 3 mit $120^\circ$-V-Nut Rohrbett, M8 6-Pin IP67-Rückanschluss, Schutz-Schottwand und federbelastetem Auto-Eject.
3. **Modulare Wechselkassetten (Typ C):** Generischer 2-teiliger Universal-Basisschlitten mit asymmetrischer Poka-Yoke Nut-und-Feder-Führung für Sena 50S/60S, Cardo Packtalk Edge/Bold, OMM-Transceiver und hermetische IP67 Blindkassette (Dry Box).
4. **Heck-Pod 3 & Radar-Ausleger (Typ D):** Strömungsgünstiger Heckbürzel-Transceiver mit dielektrischem Antennenradom für 868 MHz LoRa und Multi-GNSS sowie winkelverstellbarem Halter für Totwinkel-Radar (Garmin Varia).
5. **Universal Front-Knoten (Typ E):** Ultrakompakter Smart Fairing Hub ($84 \times 60 \times 23\,\text{mm}$) mit **4-in-1 Universal-Befestigungssystem** (AMPS, Rohrbügel-Prisma, Silentblöcke, 3M Dual-Lock), EPDM-Kabelkämmen und Knowles MEMS Akustikkanal.

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

*Abbildung 8.1: 3D-CAD-Darstellung der zentralen Steuerbox. Links: Geschlossenes IP67-Gehäuse mit HD26-Kabelbaumflansch, USB-C Servicekappe und bündigem RGB-Statusfenster an der Stirnseite der Oberwanne, 4x M4 Silentblöcken an der Unterwanne und flachem Deckel mit Gore-Membran. Rechts: Schnittansicht mit den 3 Sandwich-Ebenen.*

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

![OpenMotorBridge Satelliten-Pod CAD Explosionsdarstellung](../images/cad/openmotorbridge_pod_exploded_view.png)

*Abbildung 8.5: 3D-CAD-Explosionsdarstellung des universellen Satelliten-Pods.*

![OpenMotorBridge Satelliten-Pod Röntgenansicht](../images/cad/openmotorbridge_pod_assembly_render_xray.png)

*Abbildung 8.6: 3D-Röntgen- und Transparenzdarstellung des geschlossenen Satelliten-Pods.*

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
| **Federrate (2x V4A Federn)** | **$2{,}4\,\text{N/mm}$** | Parallelschaltung zweier Edelstahl-Druckfedern |
| **Vorspannfederweg** | **$6{,}0\,\text{mm}$** | Kompression von $L_0 = 15\,\text{mm}$ auf $L_{\text{mated}} = 9\,\text{mm}$ |
| **Axiale Haltekraft (Preload)** | **$7{,}2\,\text{N}$** | Hält Dichtsitz permanent unter Druck gegen $20\,\text{g}$ Vibration |
| **Dichtungs-Gegenkraft** | **$4{,}5\,\text{N}$** | $30\,\%$ Kompression der umlaufenden $1{,}5\,\text{mm}$ Dichtschnur |
| **Auszugskraft (Rückhalt)** | **$> 65\,\text{N}$** | Verhindert unbeabsichtigtes Lösen durch Zugbelastung |
| **Entriegelungskraft (Squeeze)**| **$9{,}8\,\text{N}$** | Ergonomisch optimierter Daumen-Zeigefinger-Druck ($\approx 1\,\text{kg}$) |
| **Automatischer Auswurfhub** | **$9{,}0\,\text{mm}$** | Trennt 6-Pin Wipe ($4{,}8\,\text{mm}$) mit **$+4{,}2\,\text{mm}$ Überhub** |

### 4.3 Asymmetrisches Poka-Yoke Nut-und-Feder Führungskonzept

![OpenMotorBridge Pod Poka-Yoke Cross Section](../images/cad/pod_poka_yoke_cross_section_cad.png)

*Abbildung 8.7: 3D-CAD-Querschnitt (Y-Z Ebene) durch das Satelliten-Pod-Gehäuse und den Kassetten-Grundschlitten. Sichtbar ist der $6{,}0\,\text{mm}$ Höhenversatz der Führungsnuten (Links: $Z=8{,}2\,\text{mm}$, Rechts: $Z=14{,}2\,\text{mm}$). Ein $180^\circ$-Falscheinbau ist mechanisch ausgeschlossen.*

---

## 5. Gehäuse Typ C: Modulare Wechselkassetten

![OpenMotorBridge Modular Cartridge Variants CAD Trio](../images/cad/cartridge_variants_trio.png)

*Abbildung 8.8: Die 4 modularen Wechselkassetten-Varianten im Überblick: OMM Heck-Transceiver (vorne links), Sena 50S/60S Quick-Snap Cradle (vorne rechts), Cardo Magnetic Air Mount (hinten links) und wasserdichte IP67 Blindkassette (hinten rechts).*

### 5.1 Sena 50S / 60S Kontur-Nest & Snap-Cradle
![OpenMotorBridge Sena 50S Cartridge Assembly 3D CAD Fitting](../images/cad/sena_cartridge_assembly_cad.png)

*Abbildung 8.9: CAD-Visualisierung der Sena 50S/60S Wechselkassette.*

### 5.2 Cardo Packtalk Edge / Pro Magnetic Air Mount
![OpenMotorBridge Cardo Packtalk Edge Cartridge Assembly 3D CAD Fitting](../images/cad/cardo_cartridge_assembly_cad.png)

*Abbildung 8.10: CAD-Visualisierung der Cardo Packtalk Edge Wechselkassette mit N52-Neodym-Magnetsitz.*

### 5.3 Längsschnitt-Vergleich Sena & Cardo
![OpenMotorBridge Sena & Cardo Cartridges Longitudinal Cross Section](../images/cad/sena_cardo_cartridge_cross_section.png)

*Abbildung 8.11: 2D-Längsschnitt (X-Z Ebene) durch die Sena 50S (oben) und Cardo Packtalk Edge (unten) Kassetten im geschlossenen Pod.*

### 5.4 IP67 Blind- / Leerkassette (Dry Box Dummy)
![OpenMotorBridge IP67 Blindkassette 3D CAD Render](../images/cad/dummy_cartridge_cad.png)

*Abbildung 8.12: Formidentische IP67 Blindkassette mit integriertem $80 \times 46 \times 16\,\text{mm}$ Notfall-Trockenstaufach.*

---

## 6. Gehäuse Typ D: Heck-Pod 3 Transceiver & Radar-Ausleger

Der Heck-Pod 3 vereint den OMM-Transceiver, 868 MHz LoRa und Multi-GNSS in aerodynamischer Heckposition:

![Pod 3 Full Assembly Exploded 3D](../images/cad/pod3_full_assembly_exploded_3d.png)

*Abbildung 8.13: CAD-Explosionsdarstellung des Heck-Pods 3 mit Antennen-Radom, Platine und M8-Bajonettsockel.*

![Pod 3 Assembly Cross Section](../images/cad/pod3_assembly_cross_section.png)

*Abbildung 8.14: Längsschnitt durch den Heck-Pod 3 mit koaxial geschirmter Antennenkammer und $25 \times 25\,\text{mm}$ GNSS-Groundplane.*

* **Winkelverstellbarer Radar-Ausleger:** GoPro-kompatibles M5-Scharnier zur horizontalen Ausrichtung von Garmin Varia Radarsensoren ($\pm 5^\circ$).

---

## 7. Gehäuse Typ E: Universal Front-Knoten (Smart Fairing Controller)

Das Gehäuse des Front-Knotens wurde speziell für die geschützte Montage in Motorrad-Frontverkleidungen (Batwing, Sharknose, BMW GS/RT Schnabel) oder an Sturzbügeln entwickelt:

- **Außenabmessungen:** Ultrakompakte **$84{,}0 \times 60{,}0 \times 23{,}0\,\text{mm}$** (L x B x H).
- **Material:** HP Multi Jet Fusion (MJF) PA12, schwarz kugelgestrahlt und chemisch geglättet.
- **Schutzart:** IP67 (tauch- und strahlwasserdicht).

![Universal Front Node Closed CAD](../images/cad/front_node_closed_cad.png)

*Abbildung 8.15: Geschlossenes Front-Node IP67-Gehäuse.*

![Universal Front Node Exploded 3D](../images/cad/front_node_exploded_3d.png)

*Abbildung 8.16: 3D-Explosionsdarstellung des Front-Knotens entlang der Z-Achse.*

![Universal Front Node Cutaway 3D](../images/cad/front_node_cutaway_3d.png)

*Abbildung 8.17: Transparente 3D-Schnittansicht des Front-Knotens mit Knowles MEMS Schallkanal und VBUS-Lastschalter.*

### 7.1 Das 4-in-1 Universal-Befestigungssystem des Front-Knotens

![Universal Front Node Bottom CAD 4-in-1](../images/cad/front_node_bottom_cad.png)

*Abbildung 8.18: Gehäuseunterseite des Front-Knotens mit AMPS-Bohrbild, $120^\circ$ V-Nut Rohrbett, EPDM-Spannnasen, Silentblock-Lochungen und 3M Dual-Lock Klettnuten.*

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

## 8. CAD-Dateistruktur & OpenSCAD-Modulbaukasten (STL-Bibliothek)

Alle 3D-Gehäusemodelle stehen unter `hardware/cad/stl/` und `hardware/cad/scad/` bereit:

| Baugruppe | Funktion / Bauteil | Druckfertige STL-Datei | Parametrischer OpenSCAD Code |
| :--- | :--- | :--- | :--- |
| **Zentralbox** | Unterwanne mit Dichtnut | `main_box_lower_case.stl` | `01_main_box/00_lower_deck.scad` |
| **Zentralbox** | Oberwanne mit Zwischenboden | `main_box_mid_tray.stl` | `01_main_box/01_upper_deck.scad` |
| **Zentralbox** | Gehäusedeckel mit Gore-Vent | `main_box_lid.stl` | `01_main_box/02_colsure.scad` |
| **Satelliten-Pod**| 5-seitiges Monocoque-Gehäuse | `pod_base_housing.stl` | `02_pod_base/pod_base_housing.scad` |
| **Schottwand** | Schutzwand mit Federsitzen | `03_pod_bulkhead_partition.stl` | `02_pod_base/parts/bulkhead.scad`|
| **Kassette** | Universeller Basisschlitten | `cartridge_base_sled.stl` | `03_pod_cartridges/00_base_sled.scad`|
| **Kassette** | Sena 50S/60S Schlitten | `cartridge_sena_sled.stl` | `03_pod_cartridges/cartridge_sena.scad`|
| **Kassette** | Cardo Packtalk Edge Schlitten | `cartridge_cardo_sled.stl`| `03_pod_cartridges/cartridge_cardo.scad`|
| **Kassette** | OMM Transceiver Schlitten | `cartridge_omm_transceiver_sled.stl`| `03_pod_cartridges/cartridge_omm.scad`|
| **Kassette** | IP67 Blindkassette (Dry Box)| `cartridge_blindkassette_waterproof.stl`| `03_pod_cartridges/cartridge_blind.scad`|
| **Front-Knoten** | Unterwanne mit 4-in-1 Boden | `front_node_lower_case.stl`| `04_front_node/front_node_lower.scad`|
| **Front-Knoten** | Oberwanne mit Dichtkämmen | `front_node_upper_case.stl`| `04_front_node/front_node_upper.scad`|

---

## 9. Fertigungsspezifikation & 3D-Druck Parameter (HP MJF vs. FDM)

### 9.1 Industrieller 3D-Druck (HP MJF PA12)
* **Verfahren:** HP Multi Jet Fusion (MJF), schwarz eingefärbt, kugelgestrahlt und chemisch dampfgeglättet.
* **Toleranzen:** $\pm 0{,}15\,\text{mm}$ (DIN ISO 2768-m).
* **Eigenschaften:** Isotrope Zugfestigkeit $48\,\text{MPa}$, temperaturbeständig bis $+95\,^\circ\text{C}$, $100\,\%$ porenfrei.

### 9.2 Heimischer FDM-Druck (Bambu Lab / Prusa / Voron)
* **Materialien:** ASA oder PETG (niemals Standard-PLA!).
* **Wandlinien:** 4 bis 5 Perimeter ($1{,}6\dots 2{,}0\,\text{mm}$ massiv).
* **Infill:** $25\dots 40\,\%$ Gyroid.
* **Flow:** $102\dots 104\,\%$ zur Mikroporenabdichtung.
