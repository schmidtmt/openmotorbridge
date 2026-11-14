# 05 - Energie-Management, USV & Kfz-Bordnetzschutz

Dieses Dokument spezifiziert das dynamische Energie- und Schutzmanagement der OpenMotorBridge v10.0 Standardized Node Architecture: die primären Schaltregler (Zentralbox `LM2596S-5.0` & Front-Knoten `TPS54302` + `SW3526`), die unterbrechungsfreie Stromversorgung (USV mit `BQ24075`, `TPS2115A` und **2.200 mAh Flat-LiPo**), die **Dual-Power Input Architektur (12V Bordnetz `J1` / 5V USB-C Service-Input `J3`)**, den automobilen Transienten- und Verpolschutz (ISO 7637-2 via `LM74700-Q1`), das intelligente **Dongle-Powermanagement (1-Klick Kaltstart & Auto-Café Mode)**, das **Apple Find My & Google Find My Device Dual-Beaconing** sowie die mehrstufige Winterschlaf-Kaskade (< 16,5 µA).

---

## 1. Primär-Schaltregler der Baugruppen

Um hohe Wirkungsgrade und thermische Reserven im geschlossenen IP67-Gehäuse zu erzielen, ist die Wandler-Topologie exakt mit den Stücklisten aus [`07_pcba_hardware_pinouts.md`](file:///Users/schmidtm/openMotorBridge/docs/de/07_pcba_hardware_pinouts.md) synchronisiert:

```
+-----------------------------------------------------------------------------+
|                    DCDC WANDLER-ARCHITEKTUR IM SYSTEM                       |
+--------------------------------------+--------------------------------------+
| 1. ZENTRALBOX (PCBA 01): LM2596S-5.0 | 2. FRONT-KNOTEN (PCBA 05): TPS54302  |
+--------------------------------------+--------------------------------------+
| * Eingang (via LM74700): 6.0 - 40 V  | * Eingangsspannung: 4.5 V - 28 V     |
| * Ausgang: 5.0 V DC / 3.0 A Dauer    | * Ausgang: 5.0 V DC / 3.0 A Dauer    |
| * nachgeschaltet: 2x AMS1117-3.3 LDO | * Zusatz-PD: SW3526 (65W Buck-Boost) |
| * USV-Mux: BQ24075 + TPS2115A OR-ing | * USV-Schutz: SMBJ24A + AO3401A P-FET|
| * Versorgt: S31, Hub, Audio, USV     | * Versorgt: ESP32-P4/E22, Hub, OLEDs |
+--------------------------------------+--------------------------------------+
```

### 1.1 Induktivitäts- & Filter-Dimensionierung (`PCBA 01` & `PCBA 05`)
Die Speicherinduktivität $L$ der Abwärtswandler ist für lückenlosen Betrieb (CCM) und minimalen Ausgangs-Ripple auf den Audio- und HF-Schienen ausgelegt:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Zentralbox (`PCBA 01`, `U7 LM2596S-5.0`):** Geschirmte $33\,\mu\text{H} / 47\,\mu\text{H}$ Power-Induktivität ($I_{\text{sat}} \ge 3{,}5\,\text{A}$), kombiniert mit zwei getrennten `AMS1117-3.3` LDO-Schienen (`U3` für Digital/MCU/Hub und `U15` exklusiv rauscharm für `QCC3084`/`ES8388` Audio-DSP).
* **Front-Knoten (`PCBA 05`, `U1 TPS54302` & `U4 SW3526`):** `TPS54302` ($400\,\text{kHz}$ synchroner Buck, $3{,}0\,\text{A}$) für Logik, `USB2514Bi` Hub und Dual-OLEDs sowie ein dedizierter **`SW3526` 65W Synchronous Buck-Boost PD-Source Controller (`U4`)** für die USB-PD Fast-Charge Versorgung zum Handschuhfach-Hub (`PCBA 05B`).
* **Eingangskapazität:** Mehrstufige 100V X7R Vielschichtkeramik (MLCC) und Elektrolyt-Puffer dämpfen Leitungsinduktivitäten des Motorrad-Kabelbaums zuverlässig.

### 1.2 Labor-Messwerte des Systemstroms (INA226 Präzisionsmessung @ 12.0 V Bordnetz)
* **Normalbetrieb (Logik + Audio/Mesh ohne PD-Schnellladung):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ bei aktiver Sena- & Cardo-Audiobrücke, LoRa 868MHz RX und 10 Hz Multi-GNSS).
* **USV-Nachlauf (Garage Wi-Fi WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ bei aktiver Übertragung mit Zündung AUS).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wacht in $< 5\,\text{ms}$ bei Zündung AN auf).
* **ULP-Winter-Hibernate (> 72 h Stillstand):** **$14{,}8\,\mu\text{A}$** (Schützt Starterbatterie selbst nach 12 Monaten Standzeit vor Tiefentladung).

### 1.3 Dual-Power Input Architektur (12V Bordnetz `J1` vs. 5V USB-C Service-Input `J3`)

Für Firmware-Entwicklung, **Central Bus-DFU Flashing**, PWA-Tests und Diagnose am Schreibtisch benötigt die Zentralbox (`PCBA 01`) kein externes 12V-Labornetzteil, sondern verfügt über einen rückstromgesicherten **5V USB-C Service-/Bench-Eingang (`J3`)**:

```
             DUAL-INPUT POWER-ORING ARCHITEKTUR (ZENTRALBOX PCBA 01)
+----------------------------+
| 12V BORDNETZ (J1 DTM06-6S) |---> [F1 PPTC + D1 SMBJ33A + U1 LM74700 Ideal-Diode]
| KL30 (Dauer) / KL15 (Zünd.)|         |
+----------------------------+         +---> 12V_SYS ---> [U12 TPS25921 Quad eFuse] (Pods/Front/Radar)
                                       |
                                       v
                                [U7 LM2596S-5.0 Buck] ---> 5V_BUCK ---+
                                                                      |
+----------------------------+                                        v
| 5V USB-C SERVICE PORT (J3) |---> [D3 LM66100 Ideal-Diode] -----> [U5 TPS2115A / 5V_SYS Rail]
| (PC / Standard 5V Netzteil)|     (Zero Back-Feed Block)             * ESP32-S31 + USB2517I Hub
+----------------------------+                                        * BQ24075 USV-Lader (U2)
```

* **Klare Trennung zwischen 5V Service-Input (`J3`) und 12V Hochlast-Speisung (`J1`):**
  * **Fahrzeug- & 12V-Prüfstandsbetrieb (`J1` DTM06-6S):** Liegt 12V-Bordnetzspannung an `J1` an, versorgt `12V_SYS` über die vier `TPS25921` eFuses (`U12`) alle 12V-Hochleistungszweige (Front-Node 60W USB-PD Source via `SW3526`, Koffer-Pods 30W USB-PD Source via `SW3516H`, 12V Mechatronik-Aktuatoren und 12V Heck-Radar) sowie über `U7` (`LM2596S-5.0`) die 5V-Systemschiene und den `BQ24075` USV-Lader.
  * **Werkbank- & Diagnosebetrieb über 5V USB-C (`J3`):** Wird die Zentralbox am Schreibtisch nur per USB-C (`J3`, 5V) mit einem PC oder Netzteil verbunden, speist die **`LM66100` Ideal-Diode (`D3`)** direkt die `5V_SYS`-Schiene (`ESP32-S31`, `USB2517I` 7-Port Hub, Audio-DSP, LoRa und USV-Lader). Dadurch lassen sich die Zentralbox sowie per USB-Bus angebundene Satelliten-Logikplatinen über das **Central Bus-DFU Gateway** flashen und diagnostizieren, ohne 12V anlegen zu müssen. (Hinweis: Die 12V-Schiene `12V_SYS` sowie die nachgeschalteten 30W/60W USB-PD Ladeausgänge `SW3516H`/`SW3526` und die 12V-Hubmagnete bleiben im reinen 5V-USB-Servicebetrieb inaktiv.)
  * **Vollständige galvanische Rückstromsperre (Zero Back-Feed):** `LM74700-Q1` (`U1`, 12V-Pfad), `LM66100` (`D3`, 5V-USB-Pfad) und der `TPS2115A` Auto-Switch (`U5`) verhindern zuverlässig, dass 12V-Bordnetzspannung in den angeschlossenen Diagnose-Laptop rückspeist oder 5V-USB-Spannung rückwärts in den Fahrzeugkabelbaum gelangt.

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

- **Eingangssicherung:** Rückstellbare Automotive PPTC-Sicherung (`F1`) am `J1` KL30-Eingang plus dedizierte 4-Kanal-eFuses (`U12 TPS25921`) für alle externen Zweige.
- **Überspannungs- & Spikeschutz:** Littelfuse `SMBJ33A` / `SMBJ33CA` TVS-Diode (`D1`, $33\,\text{V}$ Standoff) zum Clamping von Load-Dump-Impulsen nach ISO 16750-2.
- **Aktiver Verpolschutz:** Texas Instruments **`LM74700-Q1`** (`U1`) Ideal-Dioden-Controller mit externem N-Kanal-MOSFET (`Q1`, $R_{\text{DS(on)}} < 10\,\text{m}\Omega$) für verlustfreien Verpol- und Rückstromschutz.
- **Filterung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor + $2 \times 10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

### 3.1 Zwei-Kabel-Architektur & Leistungsverteilung mit TI TPS25921 eFuse-Schutz
Sämtliche Peripherie-Anbindungen der Zentralbox (`PCBA 01`) werden über die **Zwei-Kabel-Architektur** (Kabel 1: 6-Pin Deutsch DTM `J1` für Bordnetz/CAN; Kabel 2: 16-Pin Automotive Connector `J4` für den Peripheriebus) geführt. Jeder externe Zweig ist auf `PCBA 01` hardwareseitig durch eine eigene **TI TPS25921 eFuse (`U12`, `GPIO 13..16`)** geschützt:
* **Strang 1 (Front-Node & Cockpit):** **60W Budget** (lokal auf `PCBA 05` über den **`SW3526` Synchronous Buck-Boost PD-Source Controller `U4`** und `TPS54302` `U1` geregelt). Versorgt Driver Smartphone Fast-Charging (27–30W USB-PD/QC über den Handschuhfach-Hub), dediziertes Motorrad-Navi (15W für Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), Action-Cam Dauerstrom (10W wetterfest USB-C), Dual OLED Cockpit-Displays (`PCBA 05C`, 2W in Speaker Corner Pods) sowie Host-MCU (`ESP32-P4` + `ESP32-E22`), Sensor-Puck (`PCBA 05D`) & `USB2514Bi` Hub-Logik (3,5W).
* **Strang 2 (Koffer-Pod Links):** **30W USB-PD Budget** (lokal auf `PCBA 03` über **`SW3516H` `U5`** geregelt) für interne Koffer-Ladedose (`J2`), `ESP32-C6-MINI-1U` Host, `PCM2912A` Audio-Codec und mechatronischen Kaltstart-Impuls.
* **Strang 3 (Koffer-Pod Rechts):** **30W USB-PD Budget** für Bucht 2, identisch zu Strang 2.
* **Strang 4 (Heck-Radar MR20):** **12V geschaltet** (1,0A Max) für 77-GHz Radarsensor und Strobe-Warn-LEDs.
* **Mechatronischer Kaltstart-Impuls:**
  * Jeder Koffer-Pod besitzt zwei mechatronische Drücker (Mini-Hubmagnete auf `012_universal_actuator_slide_bracket.scad`), die auf `PCBA 03` über duale AO3400A MOSFETs geschaltet werden.
  * Bei Zündung-AN (KL15) feuern die Magnete für exakt 2,0 Sekunden ($\sim 4\,\text{N}$ Betätigungskraft mit Shore A50 Silikon-Stößeln auf die Ein-/Ausschalttasten von Cardo oder Sena), um komplett ausgeschaltete Headsets aus dem Null-Watt-Zustand zu wecken; die laufende Steuerung im Fahrbetrieb erfolgt anschließend verschleißfrei digital per BLE GATT bzw. Audio-Bus.
  * **Vorteil:** Headsets bleiben nach Touren vollständig spannungsfrei (kein Marketing-Standby-Batteriefraß nach 1-2 Wochen Standzeit!). Beim Einschalten der Zündung booten sie verlässlich und sofort, ohne dass der Kofferpod geöffnet werden muss.
* **5-Port Handschuhfach Hub (`PCBA 05B`, `glovebox_power_injection_hub.scad`, `55 × 25 × 15 mm`, Bauhülle `55 × 25 × 17 mm`, Platine `50 × 20 mm`) & Harley Headset-Emulation via USB:**
  * Besitzt **5× USB-C Buchsen**: Nordseite mit **`J2` (`FRONT`)** vom Front-Node (`PCBA 05`) und **`J1` (`HOST`)** zum OEM-Medienfach-Port der Harley-Headunit (Skyline OS / Boom! Box GTS); Südseite mit **`J3` (`PHONE`, 15W/30W)**, **`J4` (`DONGLE`, 10W geschaltet via `TPS2051B`)** und **`J5` (`MEDIA`, USB 2.0 Passthrough)**.
  * **Harley Headset-Emulation via USB:** Verbindet den Front-Node direkt mit der Headunit an `J1` (`HOST`); OpenMotorBridge emuliert ein digitales MFi / USB Audio Class Headset, schaltet Apple CarPlay frei und überträgt Intercom-/Sprachmikrofone verlustfrei ohne analoge Einstreuungen.
  * Einstellbare Strombegrenzung mit Überstromabschaltung in $< 1\,\mu\text{s}$ bei Kurzschluss, automatischer Thermoschutz ($150\,^\circ\text{C}$ Junction Shutdown) und Status-Rückmeldung jedes Zweigs (`FLT`) an den `ESP32-S31`.
* **Cockpit Power-Only Ausgänge (Direkt am Front-Node PCBA 05):**
  * **15W Motorrad-Navi (`J10`):** 12V/1.25A bzw. 5V/3A DC-Speisung für Garmin Zūmo XT2 / Tread / Chigee AIO-5. **Reine Stromversorgung (Power-Only):** Vollständig ohne USB-Host Datenleitungen (`D+`, `D-`), damit das Navigationssystem bei Zündung-AN sofort in die Routenführung startet und nicht in den PC-Massenspeicher-Modus schaltet.
  * **10W Action-Cam (`J8`):** Wetterfeste 5V/2A DC USB-C Zuleitung für GoPro Hero / Insta360 direkt am Cockpit. **USB BC 1.2 DCP Spezifikation:** `D+` und `D-` sind im Stecker mit $R < 200\,\Omega$ gebrückt und besitzen null Verbindung zum `USB2514B` Host-Controller. Die Action-Cam erkennt sofort ein dediziertes Bordnetz-Ladegerät und verharrt niemals in einem blockierenden PC-Verbindungs- oder Webcam-Modus. Die direkte Front-Node-Anbindung vermeidet unnötige Kabelführung durch das Handschuhfach.

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
Der im Cockpit montierte Front-Node wird über den 4-Draht-Zweig (12V + USB 2.0) der Zentralbox versorgt und regelt lokal über seinen `TPS54302` Buck-Converter (`U1`) sowie den `SW3526` 65W USB-PD Controller (`U4`). Ein hochohmiger Präzisions-Spannungsteiler speist den internen ADC des `ESP32-P4`, um lokale Spannungsabfälle an Lenkerarmaturen und Bordsteckdosen in Echtzeit an die Zentralbox zu melden.

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
