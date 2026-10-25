# 05 - Energie-Management, USV & Kfz-Bordnetzschutz

Dieses Dokument spezifiziert das dynamische Energie- und Schutzmanagement der OpenMotorBridge v10.0 Standardized Node Architecture: die primären Schaltregler (Zentralbox LM5164-Q1 & Front-Knoten LMR36015), die unterbrechungsfreie Stromversorgung (USV mit BQ24075 und **2.200 mAh Flat-LiPo**), die **Dual-Power Input Architektur (12V Bordnetz / USB-PD)**, den automobilen Transienten- und Verpolschutz (ISO 7637-2), das intelligente **Dongle-Powermanagement (1-Klick Kaltstart & Auto-Café Mode)**, das **Apple Find My & Google Find My Device Dual-Beaconing** sowie die mehrstufige Winterschlaf-Kaskade (< 16,5 µA).

---

## 1. Primär-Schaltregler der Baugruppen

Um hohe Wirkungsgrade bei minimaler Eigenerwärmung im geschlossenen IP67-Gehäuse zu erzielen, arbeiten Zentralbox und Front-Knoten mit hochintegrierten synchronen Abwärtswandlern:

```
+-----------------------------------------------------------------------------+
|                    DCDC WANDLER-ARCHITEKTUR IM SYSTEM                       |
+--------------------------------------+--------------------------------------+
| 1. ZENTRALBOX (PCBA 01): LM5164-Q1   | 2. FRONT-KNOTEN (PCBA 05): LMR36015  |
+--------------------------------------+--------------------------------------+
| * Weitbereichseingang: 6.0 V - 65 V  | * Eingangsspannung: 4.2 V - 36 V     |
| * Ausgang: 5.0 V DC / 1.0 A Dauer    | * Ausgang: 5.0 V DC / 2.0 A Dauer    |
| * Wirkungsgrad: > 88 % bei Volllast  | * Wirkungsgrad: 91.8 % bei 2.0 A     |
| * Transientenschutz bis 100 V        | * Restwelligkeit: 5.3 mVpp           |
| * Versorgt: MCU, Audio, USV, Pod 1 & 2| * Versorgt: ESP32-S3, USB2514B, VBUS |
+--------------------------------------+--------------------------------------+
```

### 1.1 LM5164-Q1 Induktivitäts- & Filter-Dimensionierung
Die Speicherinduktivität $L$ des synchronen Abwärtswandlers ist für lückenlosen Betrieb (CCM) und minimalen Ausgangs-Ripple berechnet:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Berechnungsparameter:** $V_{\text{IN,max}} = 65\,\text{V}$, $V_{\text{OUT}} = 5{,}0\,\text{V}$, $f_{\text{sw}} = 400\,\text{kHz}$, Ripplestromverhältnis $\Delta I_L = 0{,}30 \times I_{\text{OUT}} = 300\,\text{mA}$.
* **Ergebnis:** $L = \frac{5{,}0 \cdot (65 - 5)}{65 \cdot 0{,}30 \cdot 400 \times 10^3} \approx 38{,}4\,\mu\text{H} \rightarrow$ **Gewählt: $47\,\mu\text{H}$** (Würth WE-PD 744770147 / Coilcraft XAL5030-473, $I_{\text{sat}} = 2{,}1\,\text{A}$, $R_{\text{DC}} = 115\,\text{m}\Omega$).
* **Eingangskapazität:** $2 \times 10\,\mu\text{F}$ 100V X7R Vielschichtkeramik (MLCC) dämpfen Leitungsinduktivitäten des Motorrad-Kabelbaums zuverlässig.

### 1.2 Labor-Messwerte des Systemstroms (INA226 Präzisionsmessung @ 12.0 V Bordnetz)
* **Normalbetrieb (Volllast):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ bei aktiver Sena- & Cardo-Audiobrücke, LoRa 868MHz RX und 10 Hz Multi-GNSS).
* **USV-Nachlauf (WLAN WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ bei aktiver Übertragung mit Zündung AUS).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wacht in $< 5\,\text{ms}$ bei Zündung AN auf).
* **ULP-Winter-Hibernate (> 72 h Stillstand):** **$14{,}8\,\mu\text{A}$** (Gemessen mit INA226; schützt Starterbatterie selbst nach 12 Monaten Standzeit vor Tiefentladung).

### 1.3 Dual-Power Input Architektur (12V Bordnetz vs. USB-PD Sink für Werkbank & Labor)

Ein häufiges Hindernis bei der Inbetriebnahme, Firmware-Entwicklung und Diagnose von Fahrzeugelektronik ist die Notwendigkeit eines 12V-Labornetzgeräts mit maßgefertigtem Prüfkabelbaum. OpenMotorBridge v10.0 integriert daher eine **Dual-Input Power-Path Architektur**:

```
                  DUAL-INPUT POWER-ORING ARCHITEKTUR (ZENTRALBOX)
+----------------------------+
| 12V BORDNETZ (6-PIN DTM)   |---+
| KL30 (Dauer) / KL15 (Zünd.)|   |   +-----------------------+
+----------------------------+   +-->| TI LM5050 / P-FET     |
                                     | Ideal-Diode OR-ing 1  |---+
+----------------------------+   +-->| (Priorität: 12V Kfz)  |   |   +-------------------+
| USB-C PD SINK PORT         |---|   +-----------------------+   +-->| SYSTEM-POWER BUS  |
| 5V, 9V, 12V, 15V, 20V      |   |   +-----------------------+   |   | * LM5164-Q1 Buck  |
| (CH224K PD-Controller)    |   +-->| TI LM5050 / P-FET     |---+   | * BQ24075 USV-Lad.|
+----------------------------+       | Ideal-Diode OR-ing 2  |       | * 4-Draht Bus VBUS|
                                     | (Rückstromsperre 100%)|       +-------------------+
                                     +-----------------------+
```

* **Prioritäts- & Schutzlogik:**
  * **Fahrzeugbetrieb (On-Bike):** Liegt 12V-Bordnetzspannung über den 6-Pin Deutsch DTM Stecker an, versorgt das Bordnetz das Gesamtsystem und lädt den USV-Akku.
  * **Werkbank- & Diagnosebetrieb (Bench/Desk):** Für Firmware-Updates (USB-DFU), PWA-Tests, Funk-Messungen und Kalibrierung wird die Zentralbox einfach über ein handelsübliches USB-C Smartphone- oder Laptop-Netzteil (oder Powerbank) versorgt.
  * **Vollständige galvanische Entkopplung (Zero Back-Feed):** Der Ideal-Dioden-Controller (TI LM5050-1 oder duale P-FETs mit $< 15\,\text{m}\Omega$) garantiert, dass 12V niemals in den USB-C Port / Host-PC rückspeisen können, und umgekehrt keine USB-Spannung in den Fahrzeugkabelbaum dringt.
  * **Satelliten-Speisung am Schreibtisch:** Der USB-PD Sink liefert genügend Leistung ($15\dots 60\,\text{W}$ je nach Netzteil), um auch angeschlossene Front-Nodes und Koffer-Pods am Labortisch vollständig mitzubetreiben!

---

## 2. Dynamisches Power-Path Management & Integrierte USV

- **Power-Path Controller:** Texas Instruments **BQ24075** mit automatischer Last- und Ladestromaufteilung.
- **USV-Akkuzelle:** 2.200 mAh Wide-Temperature Single-Cell Flat-LiPo ($3{,}7\,\text{V}$ Nennspannung, $4{,}2\,\text{V}$ Ladeschluss, Entladebereich $-20\,^\circ\text{C}$ bis $+60\,^\circ\text{C}$, Typ 504068 / 503870, $68 \times 39 \times 5{,}0\,\text{mm}$).
- **JEITA NTC-Thermomanagement (Murata 10k NTC an BQ24075 TS-Pin):**
  - **Kältestopp ($T < 0\,^\circ\text{C}$):** Ladestrom wird in Hardware auf $0\,\text{mA}$ gestoppt (verhindert Lithium-Plating / Dendritenbildung im Winter). Das System wird normal über das Bordnetz versorgt.
  - **Hitzestopp ($T > 45\,^\circ\text{C}$):** Ladestrom wird auf $0\,\text{mA}$ gestoppt (Schutz vor Akkublähen durch Motorabwärme unter der Sitzbank).
- **Unterbrechungsfreies Umschalten bei Kaltstart (Cranking):**  
  Bricht die Bordnetzspannung beim Anlassen schwerer V2-Motoren kurzzeitig auf $6{,}5\,\text{V}$ ein, schaltet der BQ24075 in $< 5\,\mu\text{s}$ ohne jeglichen Spannungseinbruch auf den internen Pufferakku um. Audio-Streams, Funk-Mesh und GNSS-Tracking laufen unterbrechungsfrei weiter!
- **Nachlauf-Phase (Graceful Shutdown):** Ermöglicht einen Weiterbetrieb nach Zündung AUS für:
  - Finalisierung und Flush des GPX-Dateisystems auf die MicroSD-Karte.
  - Suche nach bekannten Heim-WLAN-SSIDs und Durchführung des WebDAV-Uploads.
  - Geordnetes Senden von BLE-Disconnect-Events.

### 2.1 Autonome Schwarmortung & Diebstahl-Laufzeit (Apple & Google Dual-Beacon)
Wird das Motorrad abgestellt oder trennen Diebe die 12V-Starterbatterie ab, schaltet die Zentralbox auf die interne 2.200 mAh Zelle um:
* **Interleaved Dual-Beaconing:** Der ESP32-S3 sendet alle 2,0 Sekunden abwechselnd ein Apple Find My (FMNP) und ein Google Find My Device (FMDN) BLE-Paket ($2{,}5\,\text{ms}$ Sendedauer, mittlerer Stromverbrauch ca. $15\,\mu\text{A}$).
* **Erschütterungserkennung (Wake-on-Motion):** Die 6-Achs-IMU (LIS3DH / ICM-42688) überwacht Erschütterungen mit nur $6\,\mu\text{A}$.
* **Laufzeitbilanz:** Bei einem Gesamtwachstrom von ca. $31\,\mu\text{A}$ ($0{,}031\,\text{mA}$) bietet die 2.200 mAh Zelle eine theoretische Standby-Dauer von über **70.000 Stunden (~8 Jahre)** bzw. real unter Berücksichtigung von Selbstentladung und Frostverlusten ($-15\,^\circ\text{C}$) eine **autarke Ortungs- und Alarmbereitschaft von 3 bis 4 Jahren** ohne jegliche externe 12V-Versorgung.

---

## 3. Kfz-Transienten-, EMV- & Verpolschutz (ISO 7637-2 & ISO 16750-2)

- **Eingangssicherung:** Bourns MF-MSMF050-2 Rückstellbare PPTC-Sicherung (1812 SMD, $500\,\text{mA}$ Hold / $1{,}0\,\text{A}$ Trip).
- **Überspannungs- & Spikeschutz:** Littelfuse SMBJ33CA Bidirektionale TVS-Diode ($33\,\text{V}$ Standoff, $53{,}3\,\text{V}$ max Clamping). Bietet dem 65V-LM5164-Regler komfortable $> 11{,}7\,\text{V}$ Sicherheits-Headroom bei Load-Dump-Impulsen nach ISO 16750-2 (Impuls 5b bis $87\,\text{V}$).
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET mit extrem niedrigem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **Filterung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

### 3.1 Zwei-Kabel-Architektur & Leistungsverteilung mit TI TPS25921 eFuse-Schutz
Sämtliche Peripherie-Anbindungen der Zentralbox (`PCBA 01`) werden über die **Zwei-Kabel-Architektur** (Kabel 1: 6-Pin Deutsch DTM für Bordnetz/CAN; Kabel 2: 16-Pin Automotive Connector für den Peripheriebus) geführt. Jeder externe Zweig ist auf `PCBA 01` hardwareseitig durch eine eigene **TI TPS25921 eFuse** (elektronische Sicherung) geschützt:
* **Strang 1 (Front-Node & Cockpit):** **60W USB-PD Budget** (Southchip SC8721/SC8102 Synchronous Buck-Boost, 20V/3A). Versorgt Driver Smartphone Fast-Charging (27W USB-PD/QC), dediziertes Motorrad-Navi (15W für Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), Action-Cam Dauerstrom (10W wetterfest USB-C), Dual OLED Cockpit-Displays (2W in Speaker Corner Pods) sowie Host-MCU, Sensor-Puck & USB-Hub-Logik (3,5W) – Peak-Gesamtlast 57,5W.
* **Strang 2 (Koffer-Pod Links):** **30W USB-PD Budget** für interne Koffer-Ladedose (`J_USB_CHARGE`), ESP32-C6 Host, Audio-Codec und mechatronischen Kaltstart-Impuls.
* **Strang 3 (Koffer-Pod Rechts):** **30W USB-PD Budget** für Bucht 2, identisch zu Strang 2.
* **Strang 4 (Heck-Radar MR20):** **12V geschaltet** (1,0A Max) für 77-GHz Radarsensor und Strobe-Warn-LEDs.
* **Mechatronischer Kaltstart-Impuls:**
  * Jeder Koffer-Pod besitzt zwei mechatronische Drücker (Mini-Hubmagnete auf `012_universal_actuator_slide_bracket.scad`), die auf `PCBA 03` über duale AO3400A MOSFETs geschaltet werden.
  * Bei Zündung-AN (KL15) feuern beide Magnete für exakt 2,0 Sekunden simultan ($\sim 4\,\text{N}$ Betätigungskraft mit Shore A50 Silikon-Stößeln auf OEM-Tasten wie Intercom + Media).
  * **Vorteil:** Headsets bleiben nach Touren vollständig spannungsfrei (kein Marketing-Standby-Batteriefraß nach 1-2 Wochen Standzeit!). Beim Einschalten der Zündung booten sie verlässlich und sofort, ohne dass der Kofferpod ausgebaut oder zerlegt werden muss.
* **5-Port Handschuhfach Hub (`glovebox_power_injection_hub.scad`) & Harley Headset-Emulation via USB:**
  * Wird vom Front-Node (`PCBA 05`) über ein kombiniertes High-Power & USB 2.0 High-Speed Kabel gespeist.
  * Tappt den OEM-USB-C Port im rechten Medienfach von Harley Touring-Baggern und schleift ihn an Port 5 durch.
  * Speist geregelte **30W USB-PD** (thermisch sicher im geschlossenen Fach gegen Smartphone-Überhitzung) und **10W geschaltete Dongle-Power** mit Überhitzungs-Notabschaltung ein.
  * **Harley Headset-Emulation via USB:** Das integrierte USB 2.0 Datenpaar verbindet den Front-Node direkt mit der Headunit an Port 5; OpenMotorBridge emuliert ein digitales MFi / USB Audio Class Headset, schaltet Apple CarPlay frei und überträgt Intercom-/Sprachmikrofone verlustfrei ohne analoge Einstreuungen.
  * Einstellbare Strombegrenzung mit Überstromabschaltung in $< 1\,\mu\text{s}$ bei Kurzschluss (z. B. durch Scheuerstellen am Rahmen oder Wassereintritt in offenen Steckern).
  * Automatischer Thermoschutz ($150\,^\circ\text{C}$ Junction Shutdown) und kontrollierter Sanftanlauf (Soft-Start zur Vermeidung kapazitiver Einschaltstromspitzen).
  * Status-Rückmeldung jedes Zweigs (`FLT`) an den ESP32-S31 für proaktive Fehlermeldungen in der WebApp.

---

## 4. Front-Knoten VBUS Lastschalter & Headless CP/AA Bridge Power-Management

Der Universal Front-Knoten verfügt über ein intelligentes Energiemanagement für externe Wireless CarPlay / Android Auto Headless-Dongle:

```
               FRONT-KNOTEN HEADLESS CP/AA POWER-GATE
+----------------------------+              +----------------------------+
| 12V Bordnetz (KL15 Zündung)|              | ESP32-S3 Firmware          |
| * Scheinwerfer / Zubehör   |              | * 1-Click Reboot Listener  |
+-------------+--------------+              | * Auto-Café 60s Countdown  |
              |                             +-------------+--------------+
              v                                           | GPIO 1 (EN)
+----------------------------+                            |
| TI LMR36015 Buck (5.00V)   |                            v
| * 91.8 % Wirkungsgrad      +------------->+----------------------------+
| * 5.3 mVpp Restwelligkeit  |              | TI TPS2051B Load Switch    |
+----------------------------+              | * 1.05A Current Clamp      |
                                            | * 6.5 µs Fault Trip        |
                                            | * 0.42A Soft-Start Inrush  |
                                            +-------------+--------------+
                                                          | 5.0V VBUS
                                                          v
                                            +----------------------------+
                                            | Headless CP/AA Adapter     |
                                            | * USB-Hub Port 2 (Pigtail) |
                                            +----------------------------+
```

### 4.1 1-Klick Dongle Kaltstart (Hard Reset via PWA)
Hängt sich der drahtlose CarPlay-Adapter auf, muss der Fahrer nicht mehr anhalten und den USB-Stecker ziehen:
* Ein Klick auf den Button **"CarPlay 1-Klick Kaltstart"** im WebApp-Dashboard sendet den Befehl `PKT_TYPE_CMD_POWER_CYCLE` über UWB an den Front-Knoten.
* Der ESP32-S3 zieht den Enable-Pin des TPS2051B für exakt $2{,}5\,\text{Sekunden}$ auf LOW.
* Der Dongle wird vollständig spannungsfrei geschaltet ($0{,}00\,\text{V}$) und startet anschließend frisch durch.

### 4.2 Auto-Café Modus: 60s WLAN-Freigabe bei Zündung AUS
* **Problem:** Wireless-CarPlay-Dongles spannen ein 5-GHz-WLAN auf, mit dem das Smartphone dauerhaft gekoppelt bleibt. Schaltet der Fahrer die Zündung ab und betritt ein Café, versucht das Telefon weiterhin Daten über das Dongle-WLAN zu routen $\rightarrow$ kein Internetzugriff im Café!
* **OpenMotorBridge Lösung:** 
  * Erkennt der Controller das Abfallen von KL15 (Zündung AUS), startet ein interner $60\,\text{s}$ Countdown.
  * Nach Ablauf trennt der TPS2051B die VBUS-Versorgung des Dongles komplett ab.
  * Das Smartphone verbindet sich sofort reibungslos mit dem Café-WLAN oder Mobilfunknetz.
  * Bei Wiedereinschalten der Zündung schaltet der Port in $< 10\,\text{ms}$ wieder ein.

---

## 5. Bordbatterie-Überwachung & 3-Stufen Winterschlaf-Kaskade

Die Bordnetzspannung an KL15 und KL30 wird über hochpräzise Spannungsteiler ($100\,\text{k}\Omega / 10\,\text{k}\Omega$, $0{,}1\,\%$ Toleranz) an `PIN_ADC_VIGN` erfasst:

### 5.1 Starterbatterie-Schutzschwellen

| Batterietyp | Nennspannung | Ladeschluss (Motor AN) | Warnschwelle (Low-Bat) | Hard Cut-Off (Schutz) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Blei-Säure (Nass)** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel-Batterie** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium-Eisenphosphat)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starterbatterie)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 5.2 3-Stufen Abschaltkaskade mit 60-Minuten Kaffeepausen-Persistenz

```
+-------------------------------------------------------------+
|          3-STUFIGE POWER-DOWN KASKADE BEI ZÜNDUNG AUS       |
+-------------------------------------------------------------+
| 1. KAFFEEPAUSE (0..60 Min): Mesh-State & Keep-Alive (15 mA) |
| 2. DEEP SLEEP (60 Min..72 h): Ext-Interrupt KL15 (< 100 µA) |
| 3. WINTER-HIBERNATE (> 72 h): ULP-Tiefschlaf (< 16.5 µA)    |
+-------------------------------------------------------------+
```

* **Stufe 1 - Kaffeepausen-Standby (0..60 Min):**
  * Bei Zündung AUS (Abfallen von KL15) sichert der ESP32-S3 den aktuellen Gruppen-Mesh-Status, die Link-State-Routingtabellen und symmetrische Verschlüsselungsschlüssel im NVRAM und RTC-Fast-SRAM.
  * Der Controller verbleibt in einem energiesparenden Standby ($< 15\,\text{mA}$ Ruhestrom), während im Hintergrund der WebDAV-Upload und GPX-Flush abgeschlossen werden.
  * Schaltet der Fahrer innerhalb von 60 Minuten die Zündung wieder ein, steht die gesamte Gruppenkommunikation in **$< 1{,}5\,\text{s}$** ohne erneute Discovery- oder Aushandlungsphase sofort wieder zur Verfügung.
* **Stufe 2 - Deep Sleep (60 Min..72 h):**
  * Überschreitet der Halt 60 Minuten, geht das System in den Tiefschlaf ($< 100\,\mu\text{A}$), aus dem es per Hardware-Interrupt an KL15 in $< 5\,\text{ms}$ aufwacht. Das Find-My-Beaconing läuft im Hintergrund weiter.
* **Stufe 3 - ULP-Hibernate (> 72 h Stillstand):**
  * Schützt die Starterbatterie über 6 bis 12 Monate Winterpause vor Tiefentladung ($< 14{,}8\,\mu\text{A}$ Stromaufnahme, Verlust $< 1{,}5\,\%$ der Nennkapazität pro Jahr), selbst wenn kein Erhaltungsladegerät angeschlossen ist.

---

## 6. Dezentrale Spannungsüberwachung: Smart-Keyfob LiPo & Front-Node

Das OpenMotorBridge-Ökosystem überwacht dezentrale Peripherie-Knoten kontinuierlich:

### 6.1 Front-Node (PCBA 05): Bordnetzüberwachung
Der im Cockpit montierte Front-Node ist fest über das 12V-Bordnetz versorgt (mit eigenem TI LM5164-Q1 Step-Down). Ein hochohmiger Präzisions-Spannungsteiler speist den internen ADC, um lokale Spannungsabfälle an Lenkerarmaturen und Bordsteckdosen in Echtzeit an die Zentralbox zu melden.

### 6.2 Smart-Keyfob & Pager (PCBA 07): LiPo Fuel Gauge (BLE Service 0x180F & LoRa)
Der tragbare Smart-Keyfob wird von einem internen 3,7V LiPo-Akku (350-500 mAh) versorgt, der über USB-C geladen wird. Ein **Maxim MAX17048 I2C Fuel Gauge** misst Ladezustand (SoC in %), Zellspannung und Entladerate präzise ohne Shunt-Widerstand. Der Keyfob sendet diesen Status zyklisch über den standardisierten **Bluetooth SIG Battery Service (`UUID 0x180F`)** sowie im periodischen LoRa-Health-Paket:

```
+--------------+---------------+----------------------------------------------+
| SoC (LiPo)   | Zellspannung  | System-Reaktion & Warnstufe                  |
+--------------+---------------+----------------------------------------------+
| **> 20 %**   | 3.7 V - 4.2 V | Normalbetrieb (Grüne Anzeige im WebApp Dash) |
| **≤ 15 %**   | ≤ 3.6 V       | **Gelbe Frühwarnung:** Status-LED Wechsel-   |
|              |               | blitz Gelb * Push: "Keyfob per USB-C laden"  |
|              |               | * Pager-Display zeigt Low-Bat-Symbol         |
| **≤ 5 %**    | ≤ 3.3 V       | **Kritischer Alarm:** Rote LED, automatischer|
|              |               | ULP-Deep-Sleep zum Schutz vor Tiefentladung  |
+--------------+---------------+----------------------------------------------+
```
