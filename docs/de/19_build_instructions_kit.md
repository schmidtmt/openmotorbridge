# 19 - Bauanleitung & Kit-Stückliste (Build Instructions & Hardware Kit)

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Eigenbau eines kompletten **OpenMotorBridge (v8.0)** Gesamtsystems für ein Motorrad. Es enthält eine exakte Bedarfsaufstellung aller 3D-Druckteile, bestückten Leiterplatten (PCBAs), mechanischen Normteile, Dichtungen, Kabelbaumkomponenten sowie das Inbetriebnahmeprotokoll.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit besteht aus folgenden Baugruppen:

```
                      ┌─────────────────────────────────────────┐
                      │    1x ZENTRALE MAIN BOX (IP67)          │
                      │    (Unter der Sitzbank / im Heck)       │
                      │    • Unterwanne + Zwischenboden + Deckel│
                      │    • Hauptplatine (ESP32-S3, Codec, USV)│
                      │    • Integrierter Pufferakku (LiPo)     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x ZENTRALER KABELBAUM (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LINKS) │             │ 1x POD 2 (RECHTS)│              │ 1x POD 3 (HECK)  │
│ (Lenkerarmatur)  │             │ (Lenkerarmatur)  │              │ (Heckbürzel)     │
│ • Pod-Gehäuse    │             │ • Pod-Gehäuse    │              │ • Pod-Gehäuse    │
│ • Basisplatine   │             │ • Basisplatine   │              │ • Basisplatine   │
│ • KASSETTE 1     │             │ • KASSETTE 2     │              │ • KASSETTE 3     │
│   (z. B. Sena/   │             │   (z. B. Cardo/  │              │   (OMM Long-Range│
│    Cardo)        │             │    Blindkassette)│              │    Mesh + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
```

---

## 2. Vollständige Teile- und Einkaufsliste (BOM für 1 Fahrzeug-Kit)

### 2.1 Kategorie A: 3D-Druckteile & Fertigungsoptionen (FDM vs. MJF)

Alle Gehäuse und Kassetten wurden so konstruiert, dass sie **sowohl auf handelsüblichen Desktop-FDM-Druckern (Bambu Lab, Prusa, Voron, Creality) als auch bei industriellen Pulverbett-Dienstleistern (HP MJF / SLS)** gefertigt werden können.

#### Option 1: Heimischer Desktop-FDM-Druck (Bambu Lab X1/P1/A1, Prusa MK3/MK4/XL etc.)
* **Empfohlene Filamente für Motorrad & Outdoor:**
  * **PETG:** *Ideal für alle Drucker ohne Einhausung.* UV-stabil, benzin-/ölbeständig, schlagzäh bis $80\,^\circ\text{C}$ Dauertemperatur.
  * **ASA (oder ABS):** *Beste Wahl für Drucker mit geschlossenem Bauraum (z. B. Bambu X1/P1, Prusa Enclosure).* $100\,\%$ UV- und witterungsbeständig, hitzebeständig bis $100\,^\circ\text{C}$.
  * **PA-CF / PET-CF (z. B. Bambu PAHT-CF, Prusament PA11-CF):** Exzellente Steifigkeit, seriennahe matte Carbon-Haptik.
  * ❌ *Wichtig:* **Kein Standard-PLA verwenden**, da PLA am Motorrad in der prallen Sonne (über $55\,^\circ\text{C}$) erweicht und verzieht!
* **Optimale Slicer-Einstellungen für IP67-Wasserdichtigkeit & Elastizität:**
  * **Wandlinien (Perimeter):** **4 bis 5 Wände** einstellen (Wandstärke $\approx 1{,}6 \dots 2{,}0\,\text{mm}$ $\rightarrow$ Wände werden $100\,\%$ massiv ohne Hohlräume gedruckt).
  * **Obere/untere Schichten:** **5 bis 6 Schichten**.
  * **Infill:** $25 \dots 40\,\%$ (Gyroid oder Honeycomb).
  * **Schichthöhe:** $0{,}16\,\text{mm}$ (empfohlen für saubere O-Ring-Nuten) oder $0{,}20\,\text{mm}$.
  * **Flussrate (Flow):** $102 \dots 104\,\%$ (leichte Überextrusion dichtet eventuelle Schicht-Mikroporen hermetisch ab).
  * **Druckausrichtung & Support-Hinweise:**
    * `main_box_lower_case.stl`: Flach auf Gehäuseboden ausrichten $\rightarrow$ **$0\,\%$ Support benötigt**.
    * `main_box_mid_tray.stl`: Flach auf Zwischenboden ausrichten $\rightarrow$ Baum-Stützen (Tree Support) an der Dichtlippe aktivieren.
    * `main_box_lid.stl`: Flach mit der Oberseite auf das Druckbett legen $\rightarrow$ **$0\,\%$ Support benötigt**.
    * `pod_base_housing.stl`: Auf die hintere M8-Stirnfläche stehend drucken $\rightarrow$ minimaler Tree-Support unter dem V-Rohrsattel.
    * `cartridge_*_sled.stl`: Flach auf den Schlittenboden legen $\rightarrow$ die Snap-Fit-Rastarme liegen flach in der $XY$-Ebene (optimaler Faserverlauf für maximale Biegewechselfestigkeit!).

#### Option 2: Industrieller 3D-Druck (JLCPCB 3D Print, Weerg, Craftcloud, Shapeways)
* **Verfahren:** **HP Multi Jet Fusion (MJF)** oder **SLS** (Selektives Lasersintern).
* **Material:** **PA12 (Polyamid 12)**, schwarz eingefärbt und glasperlengestrahlt.
* **Vorteil:** Isotrope Festigkeit in allen 3 Raumachsen, absolut porenfrei, keine Stützstrukturen.
* **Fertige ZIP-Pakete für Dienstleister:** [`hardware/production_packages/06_3d_print_mjf_stls/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/06_3d_print_mjf_stls).

#### Stückliste der 3D-Druckteile:

| Baugruppe | Dateiname / STL | Stück | Funktion & Beschreibung |
| :--- | :--- | :---: | :--- |
| **Main Box Unterteil** | [`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl) | **1** | Monocoque-Unterwanne mit 4x M4 Silentblock-Ohren, 4x PCB-Domen und O-Ring-Dichtnut |
| **Main Box Zwischenboden**| [`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl) | **1** | Akku-Wanne, 10x Konvektionsschlitze, HD26-/USB-C-/LED-Ausschnitte & Dichtlippe |
| **Main Box Deckel** | [`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl) | **1** | Robuster Abschlussdeckel mit Gore ePTFE-Ventildom & 4x M3-Schraubenlöchern |
| **Pod-Basisgehäuse** | [`pod_base_housing.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/pod_base_housing.stl) | **3** | Universelles Schachtgehäuse für Pod 1, 2 und 3 mit V-Rohrbett, 4x EPDM-Nasen & M8-Stutzen |
| **Universal-Kassettenschlitten**| [`cartridge_base_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_base_sled.stl) | **2** | Schlitten für Pod 1 & 2 mit $360^\circ$-Dichtsitz, Poka-Yoke-Schienen, Rastarmen & M2-Domen |
| **Sena Adapter-Einsatz** | [`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) | **1** | Modularer Deckeleinsatz mit Sena 50S/60S Konturbett, Pogo-Ausschnitt (wird mit 4x M2 verschraubt) |
| **Cardo Adapter-Einsatz** | [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl) | *(opt)* | Modularer Deckeleinsatz mit Cardo AirMount Konturbett & Magnet-Taschen (alternativ zu Sena) |
| **Blindkassetten-Deckel** | [`cartridge_insert_blindkassette.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_blindkassette.stl) | **1** | Hermetischer IP67-Verschlussdeckel für ungenutzten Pod 2 (wird mit 4x M2 verschraubt) |
| **OMM Heck-Kassette** | [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) | **1** | Monocoque-Schlitten für Pod 3 (beherbergt direkt die $70 \times 48\,\text{mm}$ Rear Pod 3 PCBA) |
| **Summe 3D-Druckteile** | | **9** | **Fertig gepackt in den 3D-Druck ZIPs in `hardware/production_packages/`** |

---

### 2.2 Kategorie B: Bestückte Leiterplatten (PCBAs bei JLCPCB / Eurocircuits)
*Alle Produktionsdateien (Gerber ZIP, CPL Pick & Place, BOM CSV) sind vorvalidiert in [`hardware/production_packages/`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages).*

| Leiterplatte | Fertigungspaket | Stück | Lagen / Spezifikation |
| :--- | :--- | :---: | :--- |
| **1. Zentralbox Hauptplatine** | [`01_main_box_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/01_main_box_pcba/01_main_box_pcba_gerbers_jlcpcb.zip) | **1** | 4-Layer FR4 TG150, ENIG, $110 \times 60\,\text{mm}$, ESP32-S3, LM5164, BQ24075 |
| **2. Pod-Basis-Trägerplatine** | [`02_pod_base_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/02_pod_base_pcba/02_pod_base_pcba_gerbers_jlcpcb.zip) | **3** | 2-Layer FR4, ENIG, M8 6-Pin Buchse, SP3012 ESD-Schutzarray |
| **3. Universal-Kassettenplatine**| [`03_pod_cartridge_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/03_pod_cartridge_pcba/03_pod_cartridge_pcba_gerbers_jlcpcb.zip) | **2** | 2-Layer FR4, 6-Pin Buchse, DS2401 1-Wire ID, JST-SH Buchse |
| **4. Heck-Pod 3 Transceiver** | [`04_rear_pod3_pcba_gerbers_jlcpcb.zip`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/04_rear_pod3_pcba/04_rear_pod3_pcba_gerbers_jlcpcb.zip) | **1** | 4-Layer FR4 TG150, ESP32-C3, u-blox MAX-M10S GNSS, SX1262 LoRa, Patchantenne |

---

### 2.3 Kategorie C: Mechanische Normteile, Schrauben & Federn (V4A / Messing)

| Bauteil | Spezifikation / Norm | Stück | Zweck |
| :--- | :--- | :---: | :--- |
| **Gewindeeinsätze** | Messing M3 $\times 5{,}7\,\text{mm}$ (Ruthex RX-M3x5.7 / Tappex) | **4** | Werden mit dem Lötkolben in die Ecken der Unterwanne eingeschmolzen |
| **Gehäuseschrauben** | Zylinderschraube DIN 912 Edelstahl V4A M3 $\times 40\,\text{mm}$ | **4** | Durchgehende 4-Eck-Verschraubung (Deckel $\rightarrow$ Zwischenboden $\rightarrow$ Unterwanne) |
| **Platinenschrauben Main** | Zylinderschraube DIN 912 Edelstahl V4A M2.5 $\times 6\,\text{mm}$ | **4** | Fixierung der Hauptplatine auf den Unterwannen-Domen |
| **Kassettendeckelschrauben**| Senkkopfschraube DIN 7991 Edelstahl V4A M2 $\times 6\,\text{mm}$ | **12** | Je 4x Schrauben zur Befestigung der Adaptereinsätze/Deckel im Kassetten-Basisschlitten (3 Kassetten: 2x Intercom-Pods + 1x Heck-Transceiver) |
| **Kassettenplatinenschrauben**| Zylinderschraube DIN 912 Edelstahl V4A M2 $\times 4\,\text{mm}$ | **12** | Je 4x Schrauben zur Befestigung der Kassetten-Carrier-PCBs / Transceiver-PCBs im Schlittenboden (3 Kassetten) |
| **Schottwandschrauben Pod** | Senkkopfschraube DIN 7991 V4A M2 $\times 8\,\text{mm}$ | **6** | Je 2x Schrauben zur Schottwandfixierung pro Pod-Gehäuse |
| **Auswerfer-Druckfedern** | Edelstahl V4A, $\varnothing_{\text{außen}} = 4{,}5\,\text{mm}$, $L_0 = 15\,\text{mm}$, $d = 0{,}4\,\text{mm}$ | **6** | Auto-Eject Mechanismus (je 2 Federn pro Pod-Schottwand) |
| **Silentblöcke / Gummipuffer** | Gummipuffer Typ A (Außengewinde/Innengewinde M4, $\varnothing 15 \times 10\,\text{mm}$) | **4** | Schwingungsentkoppelte Montage der Zentralbox am Motorradrahmen |
| **Sicherungsmuttern / Scheiben**| DIN 985 M4 Stoppmuttern + DIN 125 Unterlegscheiben V4A | **4** | Befestigung der Silentblöcke |

---

### 2.4 Kategorie D: Dichtungen, Druckausgleich & Lichtleiter (IP67)

| Bauteil | Spezifikation | Stück | Zweck |
| :--- | :--- | :---: | :--- |
| **Gehäusedichtung Main Box** | Silikon-Rundschnur $\varnothing 1{,}5\,\text{mm}$ Shore 40A / 50A ($40\,\text{cm}$ Länge) | **1** | Hermetische Nut-Feder-Abdichtung zwischen Unterwanne und Zwischenboden |
| **Kassetten-Flanschdichtungen**| Silikon Formdichtung Shore 40A ($54 \times 18\,\text{mm}$, $1{,}5\,\text{mm}$ Stärke) | **3** | Stirnseitige IP67-Abdichtung der Kassettenblende am Pod-Mundloch |
| **Druckausgleichselement** | Gore Automotive AVS 41 (M8 Schraubventil) oder AVS 4 | **1** | Druckausgleich & Kondensatvermeidung im Main Box Deckel (optional) |
| **ePTFE-Klebemembranen** | Gore / Porex IP67 Membranpad $\varnothing 7{,}0\,\text{mm}$ (selbstklebend) | **4** | 3x für die oberen Entlüftungsdome der 3 Pod-Gehäuse + 1x für Main Box Deckel (oder 1x Reserve) |
| **Lichtleiter (LED)** | Bivar PLPC3-3MM oder Mentor 1292.1101 (PMMA $\varnothing 3{,}0\,\text{mm}$) | **1** | Wasserdichte Einkopplung der WS2812B RGB-LED durch den Deckel |

---

### 2.5 Kategorie E: Kabelbaum, Steckverbinder & Pufferakku

| Bauteil | Spezifikation / MPN | Stück | Zweck |
| :--- | :--- | :---: | :--- |
| **HD26 Flanschbuchse** | Amphenol LTW HD26 Buchse IP67 (Frontmontage mit Dichtung) | **1** | Zentrale Gehäuseschnittstelle an der Main Box |
| **HD26 Kabelstecker** | HD26 Steckergehäuse IP67 mit Zugentlastung & Rändelschrauben | **1** | Gegenstecker am fahrzeugseitigen Kabelbaum |
| **M8 6-Pin Kabelstecker** | M8 Rundsteckverbinder 6-Pin A-kodiert IP67 (männlich, Schraubanschluss) | **3** | Steckverbindung vom Kabelbaum zu den 3 Pods |
| **Pufferakku** | 3.7V LiPo $1000\,\text{mAh}$ (Abmessungen max. $52 \times 36 \times 6\,\text{mm}$) mit 10k NTC | **1** | USV-Notstromversorgung bei Zündung-Aus / Anlasser-Spannungseinbruch |
| **Akkustecker** | Molex Micro-Fit 3.0 2-Pin Buchsengehäuse mit Crimpkontakten | **1** | Anschluss des Akkus an die Hauptplatine (`J_BAT`) |
| **KFZ-Sicherungshalter** | Wasserdichter Mini-Flachsicherungshalter IP67 mit **2A Sicherung** | **1** | Absicherung der Kl. 30/15 Zuleitung direkt an der Motorradbatterie |
| **Automotive-Leitungen** | FLRY-B $0{,}35\,\text{mm}^2$ (Signal/Audio) und $0{,}5\,\text{mm}^2$ (12V Power/Masse) | *nach Bedarf* | Fahrzeugkabelbaum nach Spezifikation in [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv) |
| **EPDM-Spannbänder** | UV- und ozonbeständige EPDM-Leiterbänder oder robuste O-Ringe | **6** | Werkzeuglose Montage der 3 Pods an Lenkerrohren ($\varnothing 22 \dots 28\,\text{mm}$) |

---

### 2.6 Kategorie F: Werkzeuge & Verbrauchsmaterialien

* **Lötkolben / Lötstation** mit feiner Spitze (für Kabelbaum & Einpressen der Gewindeeinsätze bei ca. $220\,^\circ\text{C}$).
* **Sechskantschlüssel (Inbus):** $1{,}5\,\text{mm}$ (M2), $2{,}0\,\text{mm}$ (M2.5), $2{,}5\,\text{mm}$ (M3), $3{,}0\,\text{mm}$ (M4).
* **Schraubensicherung:** *Loctite 243* (blau, mittelfest) für alle mechanischen Schrauben.
* **Silikonfett / Dichtungsfett:** Dünner Film für die O-Ring-Dichtschnur und die Kassetten-Lippen.
* **Schutzlack:** *Peters Elpeguard SL 1307* oder *Electrolube UR5041* Polyurethan-Schutzlack nach IPC-CC-830B.
* **USB-C Datenkabel:** Zum Flashen der Firmware und für den WebBLE-Selbsttest.

---

## 3. Schritt-für-Schritt Bau- und Montageanleitung

### Schritt 1: Vorbereitung der 3D-Druckteile
1. **Inspektion:** Alle 3D-Druckteile auf Maßhaltigkeit und Pulverfreiheit (MJF-Restpulver in Hohlräumen) prüfen. Führungsnuten und Dichtungsrillen mit Druckluft ausblasen.
2. **Messing-Gewindeeinsätze einpressen:**
   * Lötstation auf $220\,^\circ\text{C}$ einstellen.
   * Die 4x M3 Messingeinsätze vorsichtig und senkrecht in die 4 Ecksäulen der Unterwanne ([`main_box_lower_case.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lower_case.stl)) einschmelzen, bis sie bündig mit der Oberkante der Ecksäule abschließen.
3. **Lichtleiter montieren:** Den PMMA-Lichtleiter mit einem Tropfen transparentem Silikon von innen in die Bohrung des Gehäusedeckels ([`main_box_lid.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_lid.stl)) eindrücken.

---

### Schritt 2: Platinenvorbereitung & Schutzlackierung (Conformal Coating)
1. **Visuelle Kontrolle:** Lötstellen der 4 PCBAs unter der Lupe prüfen. Insbesondere die Anschlüsse des ESP32-S3, LM5164, BQ24075 und der Audioübertrager auf Kurzschlussfreiheit prüfen.
2. **Maskierung:** Vor dem Lackieren folgende Bereiche mit hitzebeständigem Kapton-Tape abkleben:
   * MicroSD-Kartenslot (`J2`),
   * 6-Pin Präzisionsbuchsen / Stecker (`J1`),
   * M8-Steckverbinder-Kontakte,
   * Gore ePTFE-Membran-Sitz.
3. **Schutzlack auftragen:** Beide Seiten der Platinen gleichmäßig mit PU-Schutzlack (*Peters Elpeguard*) lackieren ($40 \dots 60\,\mu\text{m}$) und 24 Stunden aushärten lassen.

---

### Schritt 3: Montage der Zentralbox (Main Box)
1. **Hauptplatine einsetzen:**
   * 4x kleine NBR-O-Ringe ($\varnothing 3\,\text{mm} \times 1\,\text{mm}$) als Schwingungsdämpfer auf die 4 M2.5-Dome der Unterwanne legen.
   * Hauptplatine einsetzen und mit 4x M2.5 $\times 6\,\text{mm}$ V4A-Schrauben (mit einem Tropfen *Loctite 243*) handfest anziehen ($0{,}35\,\text{Nm}$).
2. **HD26 Flanschbuchse montieren:**
   * Die HD26-Gehäusebuchse mit ihrer Silikondichtung in den Flanschausschnitt der Oberwanne einsetzen und mit dem internen Pfostenstecker der Hauptplatine verbinden.
3. **Pufferakku einsetzen:**
   * Den $1000\,\text{mAh}$ LiPo-Akku mit einem $1\,\text{mm}$ EPDM-Klebepad in die Wanne des Zwischenbodens ([`main_box_mid_tray.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) einlegen.
   * Akkukabel durch den vorderen Kabelschlitz zur Hauptplatine führen und an `J_BAT` anstecken.
4. **Sandwich-Gehäuse verschließen:**
   * Silikon-Dichtschnur ($\varnothing 1{,}5\,\text{mm}$) mit etwas Silikonfett in die umlaufende Nut der Unterwanne einlegen.
   * Den Zwischenboden aufsetzen (Dichtfeder greift in die Nut).
   * Gehäusedeckel aufsetzen und die 4x M3 $\times 40\,\text{mm}$ V4A-Schrauben über Kreuz gleichmäßig mit $0{,}8\,\text{Nm}$ anziehen.
   * Gore ePTFE-Ventil (AVS 41) in das Deckelgewinde einschrauben.

---

### Schritt 4: Montage der 3 Satelliten-Pods
*Für alle 3 Pods (Pod 1 Links, Pod 2 Rechts, Pod 3 Heck) identisch durchführen:*
1. **Pod-Basisplatine einschieben:** Die Platine mit der M8-Buchse voran von vorne in den Schacht schieben, bis der M8-Gewindestutzen hinten aus dem Gehäusehals herausragt.
2. **M8-Verschraubung sichern:** Die M8-Rändelmutter mit O-Ring am Heckstutzen handfest anziehen.
3. **Auswerferfedern einsetzen:** 2x Edelstahlfedern ($\varnothing 4{,}5 \times 15\,\text{mm}$) auf die beiden Führungsdome an der Schottwand aufstecken.
4. **Schottwand verschrauben:** Die Schottwand ([`03_pod_bulkhead_partition.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/02_pod_base/components/03_pod_bulkhead_partition.stl)) mit 2x M2 $\times 8\,\text{mm}$ V4A-Senkkopfschrauben im Tunnel fixieren.
5. **Druckausgleichsmembran:** Selbstklebendes Gore ePTFE-Pad ($\varnothing 7\,\text{mm}$) auf den oberen Entlüftungsdom kleben.

---

### Schritt 5: Bestückung der Wechselkassetten
1. **Heck-Kassette (Pod 3):** Die `04_rear_pod3_pcba` Platine mit der stirnseitigen 6-Pin Präzisionsbuchse in den Schlitten [`cartridge_omm_transceiver_sled.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_omm_transceiver_sled.stl) einsetzen und mit **4x M2/M2.5 Schrauben** in den 4 Eckdomen vibrationsfest verschrauben.
2. **Audio- & Intercom-Kassetten (Pod 1 & 2):**
   * Die `03_pod_cartridge_pcba` Trägerplatine ($35 \times 25\,\text{mm}$) in den vorderen Bereich des Basisschlittens einsetzen und mit **4x M2 Schrauben** (mind. 2 Schrauben diagonal) auf den 4 Boden-Dömchen fixieren.
   * Headset-Anschlusskabel (JST-SH 1.0 mm) anstecken und durch die Bodendurchführung nach oben leiten.
   * Den gewünschten Zwischenboden ([`cartridge_insert_sena.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_sena.stl) oder [`cartridge_insert_cardo.stl`](file:///Users/schmidtm/openMotorBridge/hardware/cad/stl/03_pod_cartridges/cartridge_insert_cardo.stl)) aufsetzen und mit **4x M2 Senkkopfschrauben** in die 4 hohen Eckpfosten verschrauben.
   * OEM-Helmaufnahme (Sena Klemmsatz / Cardo Air-Mount) einsetzen und mit einem elastischen EPDM-Spannband an den seitlichen Haken sichern.
3. **Flanschdichtung anbringen:** Die Silikon-Flanschdichtung über den Dichtkragen der Kassettenblende ziehen.
4. **Funktionstest Verriegelung:** Kassette in das Pod-Gehäuse einschieben $\rightarrow$ muss mit einem hörbaren "Klick" satt einrasten. Beim Zusammendrücken der beiden seitlichen Taster muss die Kassette ca. $8 \dots 10\,\text{mm}$ selbstständig herausschnappen.

---

### Schritt 6: Konfektionierung des Fahrzeugkabelbaums
1. **Kabelquerschnitte:** Für die 12V-Versorgung (`PIN 1: KL_30`, `PIN 2: KL_15`, `PIN 3: GND`) FLRY-B $0{,}5\,\text{mm}^2$ verwenden; für alle Audio- und Signalleitungen FLRY-B $0{,}35\,\text{mm}^2$.
2. **Fahrzeugspezifische Längenanpassung:** Die 3 M8-Abzweige passend zu deinem Motorrad und den gewählten Pod-Montageorten zuschneiden (vor dem Schneiden probeweise mit Schnur oder Kabelbinder am Rahmen verlegen!):
   * **Lenker / Cockpit (Standard):** ca. $150 \dots 190\,\text{cm}$ (entlang Rahmenrohr / Lenkkopf).
   * **Sturzbügel (Reise-Enduro wie BMW GS, T7, Africa Twin):** ca. $110 \dots 140\,\text{cm}$ (direkt am vorderen/mittleren Sturzbügelrohr).
   * **Batterie- / Seitendeckel (Harley-Davidson Tourer, Cruiser, Softail):** ca. $25 \dots 50\,\text{cm}$ (sehr kurzer Weg von der Zentralbox unter der Sitzbank).
   * **Kofferträger / Gepäckaufnahme:** ca. $60 \dots 100\,\text{cm}$.
   * **Heckbürzel / Kennzeichenträger (Pod 3):** ca. $40 \dots 80\,\text{cm}$.
3. **Pinbelegung:** Exakt nach der Fertigungstabelle in [`central_breakout_harness_wirelist.csv`](file:///Users/schmidtm/openMotorBridge/hardware/production_packages/05_wiring_harness_spec/central_breakout_harness_wirelist.csv) löten/crimpen.
4. **Schutz:** Den gesamten Kabelbaum mit elastischem Schirmgeflechtschlauch und wasserdichtem Schrumpfschlauch (mit Innenkleber) überziehen.
5. **Sicherung:** Den Mini-Flachsicherungshalter mit **2A Sicherung** in die rote 12V-Dauerplus-Leitung (Kl. 30) direkt am Batteriepol einbinden.

---

## 4. Erstinbetriebnahme & Software-Flash (Schritt-für-Schritt)

```bash
# 1. Firmware-Repository klonen & in Zentralcontroller-Verzeichnis wechseln
cd openMotorBridge/firmware/main_controller

# 2. Zentralcontroller via USB-C flashen (ESP32-S3)
pio run --target upload

# 3. Kassetten-Profile auf das LittleFS-Dateisystem hochladen
pio run --target uploadfs

# 4. Heck-Co-Prozessor flashen (ESP32-C3 in Pod 3)
cd ../rear_coprocessor
pio run --target upload
```

### Selbsttest-Checkliste:
1. [ ] **Labornetzteil:** $12{,}0\,\text{V}$ anlegen (Strombegrenzung $150\,\text{mA}$). Ruhestrom messen: Sollwert $= 45 \dots 75\,\text{mA}$.
2. [ ] **Status-LED:** Blinkt nach dem Start grün (System bereit, Pufferakku lädt).
3. [ ] **Web-Dashboard:** Im Browser (Chrome/Edge auf Smartphone oder PC) [`https://schmidtmt.github.io/openmotorbridge/`](https://schmidtmt.github.io/openmotorbridge/) oder direkt lokal [`webapp_pwa/index.html`](file:///Users/schmidtm/openMotorBridge/webapp_pwa/index.html) öffnen, auf "⚡ BLE Verbinden" klicken und mit `OpenMotorBridge_v8` koppeln.
4. [ ] **Kassettenerkennung:** Kassetten in Pod 1, 2 und 3 einstecken. Im Dashboard muss sofort das entsprechende Profil (z. B. "Sena 50S Mesh", "Cardo Packtalk", "OMM Transceiver") mit Seriennummer angezeigt werden.
5. [ ] **Audio-Check:** Headset koppeln, Musik abspielen $\rightarrow$ sauberes, glasklares Signal ohne Lichtmaschinen-Pfeifen oder Masseschleifen (dank 1500V Bourns Übertrager-Trennung).

---

## 5. Wartung & Pflege

* **Dichtungsinspektion:** 1x pro Saison die O-Ring-Dichtschnur der Main Box und die Kassetten-Flanschdichtungen mit einem Hauch Silikonfett pflegen.
* **Druckausgleich:** Sicherstellen, dass die ePTFE-Gore-Membranen nicht durch Schlamm oder dicke Wachsschichten verdeckt sind.
* **Firmware-Updates:** Drahtlos und ohne Ausbau direkt über die WebBLE-PWA-Oberfläche durchführbar.
