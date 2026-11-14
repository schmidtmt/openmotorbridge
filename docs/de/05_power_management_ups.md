# 05 - Energie-Management, USV & Kfz-Bordnetzschutz

Dieses Dokument spezifiziert das dynamische Energie- und Schutzmanagement der OpenMotorBridge v10.0 Standardized Node Architecture: die primären Schaltregler (Zentralbox `LM5164-Q1` & Front-Knoten `TPS54302` + `SW3526`), die unterbrechungsfreie Stromversorgung (USV-Pufferschnittstelle `J5` für 2.200 mAh Pufferzelle; aktiver `BQ24075` PMIC auf PCBA 09/10), die **Dual-Power Input Architektur (12V Bordnetz `J1` / 5V USB-C Service-Input `J3`)**, den automobilen Transienten- und Verpolschutz (ISO 7637-2 via `SMBJ33CA` und `LM66100` Ideal-Diode), das intelligente **Dongle-Powermanagement (1-Klick Kaltstart & Auto-Café Mode)**, das **Apple Find My & Google Find My Device Dual-Beaconing** sowie die mehrstufige Winterschlaf-Kaskade (< 16,5 µA).

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
| * Versorgt: S31, Hub, Audio, LoRa    | * Versorgt: ESP32-P4/E22, Hub, OLEDs |
+--------------------------------------+--------------------------------------+
```

### 1.1 Induktivitäts- & Filter-Dimensionierung (`PCBA 01` & `PCBA 05`)
Die Speicherinduktivität $L$ der Abwärtswandler ist für lückenlosen Betrieb (CCM) und minimalen Ausgangs-Ripple auf den Audio- und HF-Schienen ausgelegt:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Zentralbox (`PCBA 01`, `U1 LM5164-Q1`):** Geschirmte $47\,\mu\text{H} / 68\,\mu\text{H}$ Power-Induktivität ($I_{\text{sat}} \ge 1{,}8\,\text{A}$), kombiniert mit dem rauscharmen Ultra-Low-IQ LDO `U11 TPS7A0533` (für `VCC_3V3` Digital/MCU/Hub und Audio-DSP).
* **Front-Knoten (`PCBA 05`, `U1 TPS54302` & `U4 SW3526`):** `TPS54302` ($400\,\text{kHz}$ synchroner Buck, $3{,}0\,\text{A}$) für Logik, `USB2514Bi` Hub und Dual-OLEDs sowie ein dedizierter **`SW3526` 65W Synchronous Buck-Boost PD-Source Controller (`U4`)** für die USB-PD Fast-Charge Versorgung zum Handschuhfach-Hub (`PCBA 05B`).
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
+----------------------------+        +---> [U12 TPS25921 Quad eFuse] ---> J6 Satelliten (12V)
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
  * **1. Fahrzeug- & Prüfstands-Vollbetrieb (`J1` DTM06-6S an 12V Bordnetz):** Liegt 12V-Bordnetzspannung an `J1` an, wandelt der 100V-Synchron-Schaltregler **`U1` (`LM5164-Q1`)** die Bordspannung hocheffizient in `VCC_5V` und über den Ultra-Low-IQ-LDO **`U11` (`TPS7A0533`)** in `VCC_3V3` um. Gleichzeitig schaltet die **`TPS25921` Quad Automotive eFuse (`U12`)** die 12V-Bordspannung überwacht auf die vier Peripheriezweige an `J6` (`VBUS_FRONT`, `VBUS_POD1`, `VBUS_POD2`, `VBUS_RADAR`). In dieser Betriebsart sind alle Satelliten (`PCBA 05` Front Node, `PCBA 03` Pod 1/2, `PCBA 08` Heckradar) aktiv und können von der Zentralbox über den 4-Draht USB-Backbone per **Central Bus-DFU** geflasht und betrieben werden.
  * **2. Werkbank- & Schreibtisch-Servicebetrieb über 5V USB-C (`J3`):** Wird die Zentralbox am PC oder USB-Netzteil angeschlossen, speist die **`LM66100` Ideal-Diode (`D3`)** direkt die interne `VCC_5V`-Schiene und über `U11` die 3.3V-Logik der **Zentralbox (`PCBA 01`)** (`ESP32-S31`, `USB2517I` 7-Port Hub, Audio-DSP, LoRa und IMU). Dadurch lässt sich die Zentralbox autark ohne 12V-Labornetzteil flashen, kalibrieren und diagnostizieren.
  * **Hardware-Klarstellung zur Satellitenversorgung im Werkbankbetrieb (P01):** Auf der Platine `PCBA 01` speist der USB-C Eingang `J3` ausschließlich die interne 5V-Systemschiene der Zentralbox (`VCC_5V`). Die vier Satellitenzweige auf `J6` werden hardwareseitig direkt aus `KL30_IN` (12V) über `U12` gespeist; es existiert auf der Hauptplatine bewusst keine ungesicherte 5V-Querverbindung auf die 12V-Busleitung, um eine Überlastung des Host-PCs oder unzulässige Rückspeisungen zu verhindern. Sollen angeschlossene Satelliten an der Zentralbox auf der Werkbank betrieben oder geflasht werden, ist daher an `J1` eine 12V-Versorgung (z. B. ein einfaches 12V-Steckernetzteil am DTM-6 Gegenstecker) erforderlich, ODER der jeweilige Satellit wird an seinem eigenen lokalen Port separat mit Energie versorgt.
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

- **Eingangssicherung & Strombegrenzung:** 4-Kanal Automotive-eFuses (**`U12 TPS25921`**) mit programmierbarer Strombegrenzung für alle externen Zweige auf `J6`.
- **Überspannungs- & Spikeschutz:** Littelfuse **`SMBJ33CA`** bidirektionale TVS-Diode (**`D2`**, $33\,\text{V}$ Standoff-Spannung) zum Clamping von Load-Dump-Impulsen nach ISO 16750-2 / ISO 7637-2.
- **High-Voltage Schutz:** Der zentrale Buck-Converter **`U1 LM5164-Q1`** ist für Eingangsspannungen bis $100\,\text{V}$ spezifiziert und bietet $> 45\,\text{V}$ Sicherheitsreserve über die geclampte Überspannung hinaus.
- **Filterung:** $10\,\mu\text{F}$ 100V X7R Eingangskondensator (`C1`) am KL30-Eingang und LC-Dämpfungsnetzwerk (`L1` $47\,\mu\text{H}$ + `C2` $22\,\mu\text{F}$) für minimale Restwelligkeit auf der 5V-Schiene.

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
