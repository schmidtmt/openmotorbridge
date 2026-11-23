# 05 - Energie-Management, USV & Kfz-Bordnetzschutz

Dieses Dokument spezifiziert das dynamische Energie- und Schutzmanagement der OpenMotorBridge v10.0 Standardized Node Architecture: die primären Schaltregler (Zentralbox `LM5164-Q1` & Front-Knoten `TPS54302` + `SW3526`), die unterbrechungsfreie Stromversorgung (unterbrechungsfreie Stromversorgung mit aktivem `BQ24075` Lade- & Power-Path-PMIC und **2.200 mAh Flat-LiPo** an `J5` auf PCBA 01 sowie `BQ24075` mit 1.000 mAh LiPo auf PCBA 09/10), die **Dual-Power Input Architektur (12V Bordnetz `J1` / 5V USB-C Service-Input `J3`)**, den automobilen Transienten- und Verpolschutz (ISO 7637-2 via `SMBJ33CA` und `LM66100` Ideal-Diode), das intelligente **Dongle-Powermanagement (1-Klick Kaltstart & Auto-Café Mode)**, das **Apple Find My & Google Find My Device Dual-Beaconing** sowie die mehrstufige Winterschlaf-Kaskade (< 16,5 µA).

---

## 1. Primär-Schaltregler der Baugruppen

Um hohe Wirkungsgrade und thermische Reserven im geschlossenen IP67-Gehäuse zu erzielen, ist die Wandler-Topologie exakt mit den Stücklisten aus [`07_pcba_hardware_pinouts.md`](07_pcba_hardware_pinouts.md) synchronisiert:

```
+-----------------------------------------------------------------------------+
|                    DCDC WANDLER-ARCHITEKTUR IM SYSTEM                       |
+--------------------------------------+--------------------------------------+
| 1. ZENTRALBOX (PCBA 01): LM5164-Q1   | 2. FRONT-KNOTEN (PCBA 05): TPS54302  |
+--------------------------------------+--------------------------------------+
| * Eingang (via J1 DTM): 6.0 - 100 V  | * Eingangsspannung: 4.5 V - 28 V     |
| * Ausgang: 5.0 V DC / 1.0 A Dauer    | * Ausgang: 5.0 V DC / 3.0 A Dauer    |
| * nachgeschaltet: TPS7A0533 LDO      | * Zusatz-PD: SW3526 (65W Buck-Boost) |
| * Dual-Input: LM66100 Ideal-Diode    | * USV-Schutz: SMBJ24A + AO3401A P-FET|
| * Versorgt: S31, Hub, Audio, LoRa    | * Versorgt: ESP32-S31/E22, Hub, OLEDs |
+--------------------------------------+--------------------------------------+
```

### 1.1 Induktivitäts- & Filter-Dimensionierung (`PCBA 01` & `PCBA 05`)
Die Speicherinduktivität $L$ der Abwärtswandler ist für lückenlosen Betrieb (CCM) und minimalen Ausgangs-Ripple auf den Audio- und HF-Schienen ausgelegt:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Zentralbox (`PCBA 01`, `U1 LM5164-Q1`):** Geschirmte $47\,\mu\text{H} / 68\,\mu\text{H}$ Power-Induktivität ($I_{\text{sat}} \ge 1{,}8\,\text{A}$), kombiniert mit dem rauscharmen Ultra-Low-IQ LDO `U11 TPS7A0533` (für `VCC_3V3` Digital/MCU/Hub und Audio-DSP).
* **Front-Knoten (`PCBA 05`, `U1 TPS54302` & `U4 SW3526`):** `TPS54302` ($400\,\text{kHz}$ synchroner Buck, $3{,}0\,\text{A}$) für Logik, `USB2514Bi` Hub, Dual-OLEDs und FSC-BT802 sowie ein dedizierter **`SW3526` 65W Synchronous Buck-Boost PD-Source Controller (`U4`)** für die 30W USB-PD Fast-Charge Versorgung zum Handschuhfach (magnetischer Qi-Ladepuck 15W induktiv + companion USB-C PD Fast-Charge Buchse).
* **Eingangskapazität:** Mehrstufige 100V X7R Vielschichtkeramik (MLCC) und Elektrolyt-Puffer dämpfen Leitungsinduktivitäten des Motorrad-Kabelbaums zuverlässig.

### 1.2 Labor-Messwerte des Systemstroms (INA226 Präzisionsmessung @ 12.0 V Bordnetz)
* **Normalbetrieb (Logik + Audio/Mesh ohne PD-Schnellladung):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ bei aktiver Sena- & Cardo-Audiobrücke, LoRa 868MHz RX und 10 Hz Multi-GNSS).
* **USV-Nachlauf (Garage Wi-Fi WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ bei aktiver Übertragung mit Zündung AUS).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wacht in $< 5\,\text{ms}$ bei Zündung AN auf).
* **ULP-Winter-Hibernate (> 72 h Stillstand):** **$14{,}8\,\mu\text{A}$** (Schützt Starterbatterie selbst nach 12 Monaten Standzeit vor Tiefentladung).

### 1.3 Dual-Power Input Architektur (12V Bordnetz `J1` vs. 5V USB-C Service-Input `J3`)

Für Firmware-Entwicklung, Konfiguration und Diagnose der Zentralbox (`PCBA 01`) am Schreibtisch benötigt die Zentralbox kein externes 12V-Labornetzteil, sondern verfügt über einen rückstromgesicherten **5V USB-C Service-/Bench-Eingang (`J3`)**:

```
             DUAL-INPUT POWER-ORING ARCHITEKTUR (ZENTRALBOX PCBA 01)
+----------------------------+
| 12V BORDNETZ (J1 DTM06-6S) |---> KL30_IN ---> [D2 SMBJ33CA TVS (33V Clamping)]
| KL30 (Dauer) / KL15 (Zünd.)|        |
+----------------------------+        +---> [U12 TPS4H160-Q1 Quad Switch] ---> J6 Satelliten (12V)
                                       |     (VBUS_FRONT, VBUS_POD1, VBUS_POD2, VBUS_RADAR)
                                       v
                                [U1 LM5164-Q1 Buck] (100V Wide-VIN Step-Down)
                                       |
                                       v
+----------------------------+   VCC_5V Rail <------------------------------+
| 5V USB-C SERVICE PORT (J3) |        |                                     |
| (PC / Standard 5V Netzteil)|        +---> [U11 TPS7A0533 3.3V LDO]        |
+-------------+--------------+                 |                            |
              |                                v                            |
              +---> USBC_VBUS ---> [D3 LM66100 Ideal-Diode] ----------------+
                                   (Reverse Current Blocking / Zero Back-Feed)
```

* **Klare Trennung der beiden Betriebsarten:**
  * **1. Fahrzeug- & Prüfstands-Vollbetrieb (`J1` DTM06-6S an 12V Bordnetz):** Liegt 12V-Bordnetzspannung an `J1` an, wandelt der 100V-Synchron-Schaltregler **`U1` (`LM5164-Q1`)** die Bordspannung hocheffizient in `VCC_5V` und über den Ultra-Low-IQ-LDO **`U11` (`TPS7A0533`)** in `VCC_3V3` um. Gleichzeitig schaltet der **`TPS4H160-Q1` Quad Automotive High-Side Smart Switch (`U12`)** die 12V-Bordspannung überwacht auf die vier Peripheriezweige an `J6` (`VBUS_FRONT`, `VBUS_POD1`, `VBUS_POD2`, `VBUS_RADAR`). In dieser Betriebsart sind alle Satelliten (`PCBA 05` Front Node, `PCBA 03` Pod 1/2, `PCBA 08` Heckradar) aktiv und können von der Zentralbox über den 4-Draht USB-Backbone per **Central Bus-DFU** geflasht und betrieben werden.
  * **2. Werkbank- & Werkstatt-Servicebetrieb über 5V USB-C (`J3`):** Wird die Zentralbox am PC oder USB-Netzteil angeschlossen, speist die **`LM66100` Ideal-Diode (`D3`)** direkt die interne `VCC_5V`-Schiene und über `U11` die 3.3V-Logik der **Zentralbox (`PCBA 01`)** (`ESP32-S31`, `USB2517I` 7-Port Hub, Audio-DSP, LoRa und IMU).
  * **Bus-weites Flashen & Werkstatt-Power-Budget:** Über den 7-Port Hub `USB2517I` der Zentralbox sind alle Peripheriestränge (Strang 1 Front Node, Strang 2 Pod 1, Strang 3 Pod 2, Strang 4 Heckradar) im USB-Verbund angebunden, sodass das gesamte Motorrad von diesem einzigen USB-C Service-Port aus per WebUSB / DFU geflasht und diagnostiziert werden kann.
    * **Power-Budget-Rechnung (ohne externe Lenker-/Handschuhfach-Lasten):**
      * Zentralbox (`PCBA 01`): $\approx 1{,}6\,\text{W}$ ($320\,\text{mA}$)
      * Front-Node & Sensor-Puck (`PCBA 05` + `05D`): $\approx 1{,}4\,\text{W}$ ($280\,\text{mA}$)
      * Heck-Radar (`PCBA 08` inkl. MR20 Standby): $\approx 2{,}1\,\text{W}$ ($420\,\text{mA}$)
      * 2x Koffer-Pods (`PCBA 02` + `03` inkl. beider OEM-Intercoms im Standby-Audiobetrieb): $\approx 2{,}2\,\text{W}$ ($440\,\text{mA}$)
      * Leitungs- und Schaltverluste: $\approx 0{,}3\,\text{W}$
      * **Gesamtleistungsaufnahme im Werkstatt-Vollbetrieb:** **$\approx 7{,}6\,\text{W}$ ($5{,}0\,\text{V} / 1{,}52\,\text{A}$)**.
      * *(Reiner Flash-/Programmierbetrieb bei ruhender Radar-HF und inaktiven Intercoms: nur $\approx 4{,}5\,\text{W}$ bzw. $0{,}9\,\text{A}$, voll kompatibel zu Standard USB 3.0).*
    * **Schlussfolgerung:** An jedem modernen Standard-USB-C-Port ($5\,\text{V} / 3{,}0\,\text{A} = 15\,\text{W}$) verbraucht das vollständig bestückte System gerade einmal $\approx 51\,\%$ des Budgets. Weder Radar noch Intercoms müssen im Werkstattbetrieb zwangsweise abgeschaltet werden. Softwareseitig wird lediglich der LiPo-Ladestrom des internen USV-Akkus (`BQ24075`) auf $500\,\text{mA}$ gedrosselt und externe 30W-Schnellladungen für Smartphones gesperrt.
  * **Vollständige galvanische Rückstromsperre (Zero Back-Feed):** Die Ideal-Diode **`D3` (`LM66100`)** sperrt den Rückstrompfad von `VCC_5V` zum USB-C Service-Port `J3` hermetisch ab. Liegt am Fahrzeug gleichzeitig 12V an, während ein Diagnose-Laptop an `J3` angeschlossen ist, verhindert `D3` zuverlässig jede Rückspeisung in das Programmiergerät.

---

## 2. Dynamisches Power-Management & Spannungsüberwachung

- **Interne Spannungsregelung:** Texas Instruments **LM5164-Q1** (100V Synchronous Step-Down DC/DC Buck) für 5V und **TPS7A0533** (Ultra-Low Quiescent Current LDO) für 3.3V.
- **Batterie- und Temperatur-Sensing (`J5`):** 4-poliger Anschluss für externe Pufferbatterie und NTC-Temperatursensor:
  - **Spannungsteiler `R12`/`R13` (100k/100k):** Führt die Batteriespannung hochohmig an `BAT_SENSE` (`ADC1_CHANNEL_0` des ESP32-S31).
  - **NTC-Spannungsteiler `R14` (10k):** Erfasst die Zellentemperatur an `BAT_NTC` (`ADC1_CHANNEL_2`) für thermischen Ladeschutz und Frostüberwachung.
- **Unterbrechungsfreies Verhalten bei Kaltstart (Cranking):**
  Bricht die Bordnetzspannung beim Anlassen schwerer V2-Motoren kurzzeitig auf $6{,}5\,\text{V}$ ein, hält der weite Eingangsspannungsbereich des LM5164-Q1 (Betrieb ab $6{,}0\,\text{V}$) zusammen mit den Pufferkondensatoren die 5V- und 3.3V-Systemschienen stabil.
- **Nachlauf-Phase (Graceful Shutdown):** Ermöglicht einen geordneten Weiterbetrieb nach Zündung AUS für:
  - Finalisierung und Flush des GPX-Dateisystems auf die MicroSD-Karte (`sdio_track_finalize()`).
  - WebDAV-Upload über das Heim-WLAN oder PWA-Relay.
  - Geordnetes Senden von BLE-Disconnect-Events vor dem Deep Sleep.

---

## 3. Kfz-Transienten-, EMV- & Verpolschutz (ISO 7637-2 & ISO 16750-2)

- **Eingangssicherung & Strombegrenzung:** 4-Kanal Automotive Smart Switch (**`U12 TPS4H160-Q1`**) mit programmierbarer Strombegrenzung und Diagnose für alle externen Zweige auf `J6`.
- **Überspannungs- & Spikeschutz:** Littelfuse **`SMBJ33CA`** bidirektionale TVS-Diode (**`D2`**, $33\,\text{V}$ Standoff-Spannung) zum Clamping von Load-Dump-Impulsen nach ISO 16750-2 / ISO 7637-2.
- **High-Voltage Schutz:** Der zentrale Buck-Converter **`U1 LM5164-Q1`** ist für Eingangsspannungen bis $100\,\text{V}$ spezifiziert und bietet $> 45\,\text{V}$ Sicherheitsreserve über die geclampte Überspannung hinaus.
- **Filterung:** $10\,\mu\text{F}$ 100V X7R Eingangskondensator (`C1`) am KL30-Eingang und LC-Dämpfungsnetzwerk (`L1` $47\,\mu\text{H}$ + `C2` $22\,\mu\text{F}$) für minimale Restwelligkeit auf der 5V-Schiene.

### 3.1 Zwei-Kabel-Architektur & Leistungsverteilung mit TI TPS4H160-Q1 Smart Switch
Sämtliche Peripherie-Anbindungen der Zentralbox (`PCBA 01`) werden über die **Zwei-Kabel-Architektur** (Kabel 1: 6-Pin Deutsch DTM `J1` für Bordnetz/CAN; Kabel 2: 16-Pin Automotive Connector `J4` für den Peripheriebus) geführt. Jeder externe Zweig ist auf `PCBA 01` hardwareseitig durch einen eigenen Kanal des **TI TPS4H160-Q1 Smart Switch (`U12`, `GPIO 13..16`)** geschützt:
* **Strang 1 (Front-Node & Cockpit):** **60W Budget** (lokal auf `PCBA 05` über den **`SW3526` Synchronous Buck-Boost PD-Source Controller `U4`** und `TPS54302` `U1` geregelt). Versorgt Driver Smartphone Fast-Charging (27–30W USB-PD/QC über den Handschuhfach-Hub), dediziertes Motorrad-Navi (15W für Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), Action-Cam Dauerstrom (10W wetterfest USB-C), Dual OLED Cockpit-Displays (`PCBA 05C`, 2W in Speaker Corner Pods) sowie Host-MCU (`ESP32-S31` + `ESP32-E22`), Sensor-Puck (`PCBA 05D`) & `USB2514Bi` Hub-Logik (3,5W).
* **Strang 2 (Koffer-Pod Links):** **30W USB-PD Budget** (lokal auf `PCBA 03` über **`SW3516H` `U5`** geregelt) für interne Koffer-Ladedose (`J2`), `ESP32-C6-MINI-1U` Host, `PCM2912A` Audio-Codec und mechatronischen Kaltstart-Impuls.
* **Strang 3 (Koffer-Pod Rechts):** **30W USB-PD Budget** für Bucht 2, identisch zu Strang 2.
* **Strang 4 (Heck-Radar MR20):** **12V geschaltet** (1,0A Max) für 77-GHz Radarsensor und Strobe-Warn-LEDs.
* **Mechatronischer Kaltstart-Impuls:**
  * Jeder Koffer-Pod besitzt zwei mechatronische Drücker (Mini-Hubmagnete auf `012_universal_actuator_slide_bracket.scad`), die auf `PCBA 03` über duale AO3400A MOSFETs geschaltet werden.
  * Bei Zündung-AN (KL15) feuern die Magnete für exakt 2,0 Sekunden ($\sim 4\,\text{N}$ Betätigungskraft mit Shore A50 Silikon-Stößeln auf die Ein-/Ausschalttasten von Cardo oder Sena), um komplett ausgeschaltete Headsets aus dem Null-Watt-Zustand zu wecken; die laufende Steuerung im Fahrbetrieb erfolgt anschließend verschleißfrei digital per BLE GATT bzw. Audio-Bus.
  * **Vorteil:** Headsets bleiben nach Touren vollständig spannungsfrei (kein Marketing-Standby-Batteriefraß nach 1-2 Wochen Standzeit!). Beim Einschalten der Zündung booten sie verlässlich und sofort, ohne dass der Kofferpod geöffnet werden muss.
* **Handschuhfach Schnelllade-Architektur (Ersatz von PCBA 05B):**
  * Das historische 5-Port Hub `PCBA 05B` und externe Wireless-CarPlay-Dongles sind ersatzlos entfallen.
  * Stattdessen wird das Handschuhfach (z. B. Harley Touring) über eine robuste 2-Ader DC-Versorgung von Front-Knoten `J7` mit bis zu 30–36W USB-PD / QC 4.0 gespeist.
  * Dort sitzt ein **magnetischer Qi-Ladepuck** (15W induktiv Qi/Qi2 MagSafe, ca. 20–22W DC-Eingangsleistung) plus eine zusätzliche **USB-C PD Fast-Charge Buchse** für kabelgebundenes Laden mit voller Geschwindigkeit (z. B. Zweithandy oder Tablet).
  * Einstellbare Strombegrenzung mit Überstromabschaltung in $< 1\,\mu\text{s}$ bei Kurzschluss, automatischer Thermoschutz ($150\,^\circ\text{C}$ Junction Shutdown) und Überwachung durch den `SW3526` Controller.
* **Cockpit Power-Only Ausgänge (Direkt am Front-Node PCBA 05):**
  * **15W Motorrad-Navi (`J10`):** 12V/1.25A bzw. 5V/3A DC-Speisung für Garmin Zūmo XT2 / Tread / Chigee AIO-5. **Reine Stromversorgung (Power-Only):** Vollständig ohne USB-Host Datenleitungen (`D+`, `D-`), damit das Navigationssystem bei Zündung-AN sofort in die Routenführung startet und nicht in den PC-Massenspeicher-Modus schaltet.
  * **10W Action-Cam (`J8`):** Wetterfeste 5V/2A DC USB-C Zuleitung für GoPro Hero / Insta360 direkt am Cockpit. **USB BC 1.2 DCP Spezifikation:** `D+` und `D-` sind im Stecker mit $R < 200\,\Omega$ gebrückt und besitzen null Verbindung zum `USB2514B` Host-Controller. Die Action-Cam erkennt sofort ein dediziertes Bordnetz-Ladegerät und verharrt niemals in einem blockierenden PC-Verbindungs- oder Webcam-Modus. Die direkte Front-Node-Anbindung vermeidet unnötige Kabelführung durch das Handschuhfach.

---

## 4. Handschuhfach Lade- & Thermomanagement (Qi-Puck & USB-PD Fast-Charge)

Durch den Entfall des CarPlay/Android Auto Video-Streaming-Stacks (kein WLAN-Direct, kein dauerhafter H.264/H.265 Hardware-Decoder) sinkt die thermische Last des Smartphones im geschlossenen Handschuhfach dramatisch ab:

```
               HANDSCHUHACH LADE- & POWER-GATEWAY (30W USB-PD)
+----------------------------+              +----------------------------+
| 12V Bordnetz (KL15 Zündung)|              | Front-Knoten PCBA 05       |
| * Scheinwerfer / Zubehör   |              | * SW3526 PD-Controller     |
+-------------+--------------+              | * I2C Telemetrie & Protect |
              |                             +-------------+--------------+
              v                                           |
+----------------------------+                            | 2-Ader DC Speisung
| SW3526 Buck-Boost (J7)     +----------------------------+ (bis zu 36W PD 3.0)
| * Bis zu 36W USB-PD / QC   |                            |
+----------------------------+                            v
                                            +----------------------------+
                                            | Handschuhfach Ladebucht    |
                                            | * 15W Qi-Puck (MagSafe)    |
                                            | * Zusatz USB-C PD Buchse   |
                                            +----------------------------+
```

### 4.1 Automatisches Thermomanagement & Überstromschutz
* Der `SW3526` PD-Controller auf `PCBA 05` überwacht Strom, Spannung und Die-Temperatur kontinuierlich per I2C.
* Bei Überhitzung im Handschuhfach oder Fehlausrichtung des Smartphones auf dem Qi-Puck drosselt der Controller den Ladestrom dynamisch (Thermal Throttling) oder schaltet bei thermischer Überlastung ($> 120\,^\circ\text{C}$) sicher ab.
* Sobald KL15 abfällt (Zündung AUS), trennt die Power-Management-Engine die Ladeversorgung verzögert ab, um die Starterbatterie des Motorrads zu schonen.

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
Der im Cockpit montierte Front-Node wird über den 4-Draht-Zweig (12V + USB 2.0) der Zentralbox versorgt und regelt lokal über seinen `TPS54302` Buck-Converter (`U1`) sowie den `SW3526` 65W USB-PD Controller (`U4`). Ein hochohmiger Präzisions-Spannungsteiler speist den internen ADC des `ESP32-S31`, um lokale Spannungsabfälle an Lenkerarmaturen und Bordsteckdosen in Echtzeit an die Zentralbox zu melden.

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

### 6.3 Zentralbox USV-LiPo (PCBA 01): BQ24075 & BAT_SENSE
Die Zentralbox verfügt über eine interne 1S LiPo-Zelle (2.200 mAh) an `J5`, gesteuert durch den Power-Path PMIC Texas Instruments `BQ24075RGTR` (`U4`):
* **Onboard-Ladung & USV-Power-Path:** Die Zelle wird automatisch aus der 5V-Systemschiene (`VCC_5V` aus LM5164-Q1 Kfz-Buck oder USB-C `J3`) geladen ($I_{\mathrm{CHG}} = 1{,}0\,\text{A}$, $I_{\mathrm{IN\_MAX}} = 1{,}5\,\text{A}$). Bei Ausfall oder Einbruch der Bordspannung (z. B. Startvorgang) schaltet `U4` in $< 10\,\mu\text{s}$ unterbrechungsfrei auf den LiPo um.
* **Spannungsüberwachung (`BAT_SENSE`):** Ein hochohmiger Spannungsteiler `R12/R13` ($100\,\text{k}\Omega / 100\,\text{k}\Omega$) führt die Zellspannung an `ADC1_CH9` (GPIO 10) des ESP32-S31.
* **Thermoschutz (`BAT_NTC`):** Der integrierte $10\,\text{k}\Omega$ NTC-Thermistor an `J5` Pin 3 wird durch den `TS`-Pin des `BQ24075` überwacht (JEITA-Ladestopp unter 0 °C und über 45 °C zum Schutz vor Lithium-Plating im Winter).
* **Warn- & Abschaltschwellen:**
  * **$> 3{,}8\,\text{V}$ (> 60 % SoC):** Vollständige Pufferbereitschaft (Cranking-Kompensation, GPX-Blackbox-Abschluss, WebDAV-Uploads).
  * **$\le 3{,}6\,\text{V}$ (ca. 15 % SoC):** Gelbe Vorwarnung in der Telemetrie; Deaktivierung von stromhungrigen Hintergrundaufgaben.
  * **$\le 3{,}3\,\text{V}$ (ca. 3 % SoC):** Notabschaltung des Systems in den ULP-Tiefschlaf ($< 15\,\mu\text{A}$), um die LiPo-Zelle zuverlässig vor irreversibler Tiefentladung zu schützen.

### 6.4 OMM UCS Intercom-Modul (PCBA 09 / 10): LiPo & Autonome Akustik-Ansagen
Das universelle ECE 22.06 Intercom-Modul (`PCBA 09` / `PCBA 10`) nutzt eine interne 1S LiPo-Zelle (1.000 mAh `Typ 603040 / 602840`) an `BAT1` (JST-SH auf der Platinenunterseite):
* **Betriebsarten-Umschaltung:**
  * *Im Koffer-Pod (Bucht 1 / Bucht 2):* Kontinuierliche Ladung über den Kassetten-Schlitten (`VCC_5V_PROT` via `U4` TS5A3159 / `J1` USB-C).
  * *Im Helm (autark):* Autarker Akkubetrieb für 13–18 Stunden kontinuierlichen Vollduplex-Betrieb.
* **Akustische Sprachansagen (Voice Prompts) direkt im Helm:**
  Da das OMM-Modul im Helm autark am Stereo-Codec `ES8388` (`U4`) und den Helmlautsprechern (`J_HELMET`) arbeitet, werden Batteriewarnungen prioritär und ablenkungsfrei akustisch direkt ins Ohr des Fahrers eingespielt:
  * **20 % SoC:** Sanfter Doppelton (Chime) + Sprachansage: *„Battery low – 20 percent remaining“*.
  * **10 % SoC:** Dringlicher Doppelton + Sprachansage: *„Battery critical – please recharge“*.
  * **5 % SoC:** Sprachansage: *„Battery empty – shutting down“* mit anschließendem geordneten Abschalten (Power-Down in den ULP-Schlaf zum Schutz der LiPo-Zelle).
* **Begleitende Anzeige:** Befindet sich der Helm in Funkreichweite des Motorrads (2.4 GHz OMM-Mesh / BLE), meldet das Modul seinen Ladezustand an den Front-Node: Auf den Cockpit-OLEDs erscheint kurz ein Pop-Up `OMM BATT: 18% [!]`, und das WebApp-Dashboard aktualisiert den Füllstand in Echtzeit.

---

## 7. Multi-Batterie Alert-Infrastruktur: LoRa-Sentry, HomeSphere & Fallbacks

Zur lückenlosen Absicherung gegen unbemerkte Entladung – insbesondere bei monatelanger Standzeit im Winterlager oder in fensterlosen Tiefgaragen – implementiert OpenMotorBridge eine mehrstufige Alarmierungs- und Meldekette:

### 7.1 Die Standzeit- & Winterpause-Problematik
In kalten Garagen und Tiefgaragen droht der Starterbatterie schleichende Sulfatierung (bei Standard Blei-Säure/AGM unter $11{,}8\,\text{V}$ bzw. Zellschädigung bei LiFePO4 unter $12{,}8\,\text{V}$). Gleichzeitig versagen 2,4-GHz-Funkstandards (WLAN, Bluetooth) durch die starke Dämpfung von Stahlbetondecken und Brandschutztoren vollständig.

```
+-----------------------------------------------------------------------------+
|              MULTI-BATTERIE STANDBY- & WINTER-ALERT PIPELINE                |
+-----------------------------------------------------------------------------+
| 1. MOTORRAD (Tiefgarage): ESP32-S31 RTC-Wakeup alle 12h (40 ms Airtime)     |
|    -> Misst KL30 (Starterbatt), BAT_SENSE (USV-LiPo) & NTC (Temp)           |
|    -> Sendet 16-Byte LoRa-Health-Paket (0xFD) @ 868 MHz (+14..+22 dBm)      |
+-----------------------------------------------------------------------------+
                                      |
         +----------------------------+----------------------------+
         | (Primär: 868 MHz)                                       | (Fallback: WLAN/IP)
         v                                                         v
+-------------------------------+                         +-------------------+
| HOMESPHERE USB-LoRa-Dongle    |                         | Heim-WLAN Garage  |
| * Empfang durch Stahlbeton    |                         | * MQTT / Webhook  |
| * HomeSphere Alert-Engine     |                         | * Home Assistant  |
| * Push-Notification aufs Handy|                         | * ntfy / Telegram |
+-------------------------------+                         +-------------------+
```

### 7.2 Primärpfad: 868 MHz Semtech SX1262 LoRa an HomeSphere (mit USB-LoRa-Dongle)
* **Ultra-Low-Power Wake-up & Burst:** Im Winterlager / Stillstand verharrt die Zentralbox im Deep Sleep ($< 15\,\mu\text{A}$ Gesamtstromaufnahme).
* Der interne RTC-Timer weckt den ESP32-S31 in konfigurierbaren Intervallen (Standard: alle 12 Stunden) für lediglich **$pprox 40\,\text{ms}$** auf.
* Der Controller misst über den ADC die Starterbatterie-Spannung (`KL30`), die USV-Akkuspannung (`BAT_SENSE`), fragt per Ultra-Short-BLE den letzten Keyfob-Status ab und erfasst die Umgebungstemperatur (`TMP117`/NTC).
* Anschließend sendet der Onboard-Transceiver `SX1262` ein kompaktes **16-Byte LoRa-Health-Paket (`0xFD`)** mit maximaler Reichweite (+14 bis +22 dBm) im 868-MHz-SRD-Band.
* **HomeSphere-Integration:** An der zentralen HomeSphere-Station im Wohnhaus empfängt ein **USB-LoRa-Dongle** (z. B. auf Basis des SX1262 / ESP32-C6) das Paket auch durch dicke Stahlbetondecken und Tiefgaragentore hindurch. HomeSphere speist die Telemetriedaten nahtlos in die bestehende Alert-Infrastruktur ein:
  * Sofortige Push-Benachrichtigung ans Smartphone: *„⚠️ Motorrad-Starterbatterie bei 11.8 V – Ladegerät anschließen!“*
  * Grafische Anzeige der Batteriespannungen im HomeSphere-Dashboard.
  * Automatisierte Schaltung von smarten Garagensteckdosen (z. B. Aktivierung des Ctek/Optimate-Erhaltungsladegeräts bei Unterschreiten der Warnschwelle).

### 7.3 Fallback 1: Lokales Heim-WLAN (Garage / Carport)
Für Nutzer ohne LoRa-Dongle, deren Motorrad in Reichweite des heimischen WLANs steht:
* Beim periodischen Aufwachen prüft der ESP32-S31, ob das hinterlegte Heim-WLAN erreichbar ist.
* Ist dies der Fall, wird der Alert direkt über das IP-Netzwerk abgesetzt:
  * **Smart-Home-Nutzer:** Senden per MQTT oder REST-Webhook an **Home Assistant**, **ioBroker** oder **openHAB**.
  * **Standalone (ohne Heimserver):** Direkter HTTPS-Aufruf via `esp_http_client` an freie Push-Dienste wie **ntfy.sh**, **Pushover**, **Pushsafer** oder als direkte Chat-Nachricht über einen **Telegram-Bot** auf das Mobiltelefon des Besitzers.

### 7.4 Fallback 2: Öffentliches LoRaWAN / The Things Network (TTN)
* Da der onboard Semtech `SX1262` standardkonformes LoRaWAN (Class A Uplink) beherrscht, kann das 16-Byte Winter-Health-Paket über frei zugängliche **The Things Network (TTN)**-Gateways gefunkt werden.
* In vielen städtischen und suburbanen Regionen existiert bereits eine flächendeckende TTN-Abdeckung.
* Ein kostenloser TTN-Webhook leitet das empfangene Datenpaket als Push-Benachrichtigung an das Smartphone des Fahrers weiter – **vollkommen ohne eigene Empfängerhardware oder Dongles zu Hause**.

### 7.5 Fallback 3: Lokaler Nahfeld- & Fahrtantritts-Schutz (Laternenparker ohne Funkempfang)
Steht das Motorrad an der Straße ohne jegliche Funkabdeckung (kein LoRa-Dongle, kein TTN, kein WLAN):
* **BLE Proximity Beacon:** Sobald der Fahrer sich mit Smartphone oder Fob dem abgestellten Motorrad nähert, erkennt die Smartphone-App / WebApp die periodischen BLE-Werbepakete und signalisiert: *„Achtung: Batteriespannung niedrig (11.6 V)!“*.
* **Cockpit-Vollbildwarnung bei Zündung EIN (KL15):** Schaltet der Fahrer die Zündung ein, evaluiert der Controller die Starterbatterie sofort. Fällt die Leerlaufspannung unter die Warnschwelle, schalten die beiden **Dual Under-Perch Cockpit-OLEDs** augenblicklich auf eine dominante Warnanzeige:
  ```
  +-----------------------------+
  |  ⚠️ 12V BATT LOW: 11.5 V    |
  |  START MOTOR IMMEDIATELY!   |
  +-----------------------------+
  ```
  Gleichzeitig ertönt ein dringlicher Signalton im Headset, **bevor** der Anlasser betätigt wird. So wird verhindert, dass der Fahrer durch langes Stehenlassen mit Zündung AN die Batterie restlos entlädt.
