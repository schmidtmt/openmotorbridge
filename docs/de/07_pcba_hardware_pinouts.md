# 07 - Hardware-Architektur & Platinen-Pinouts (Das standardisierte v10.0 Lineup)

Dieses Dokument bildet die **zentrale, autoritative Hardware-Spezifikation aller aktiven Platinen-Baugruppen (`PCBA 01`, `03`, `05`, `05B`, `07`, `08`, `09`, `10`)** des OpenMotorBridge Gesamtsystems (v10.0 Standardized Node Architecture), einschließlich Lagenaufbau, Impedanzkontrolle, Net-Klassen, Funktionszonen und vollständigen Pinout-Tabellen.

---

## 1. Systemübersicht des v10.0 Hardware-Lineups

OpenMotorBridge v10.0 ersetzt das frühere experimentelle UWB-Funkbackbone durch einen hochrobusten, geschirmten **4-Ader Automotive-Bus** (`VCC_BUS` 12V/PD, `USB_D-`, `USB_D+`, `GND`). Damit stehen an allen Knoten (Koffer-Pods und Front-Node) zeitgleich **massive Ladeleistung (bis zu 60W USB-PD)** und **hochgeschwindigkeits-stabile native USB 2.0 Datenverbindungen** zur Verfügung – vollkommen immun gegen Funkschatten durch nasses Gepäck, Regenkombis oder Aluminiumkoffer.

```
+----------------------------------------------------------------------------------------+
|                   DAS 7-PLATINEN-LINEUP DER OPENMOTORBRIDGE v10.0                      |
+-------+-------------------------------+---------------+---------+----------------------+
| Baugruppe | Name & Funktion           | Platinenmaße  | Lagen   | Kern-ICs / Bauteile  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 01**| **Zentralbox Main Controller** | 85 x 55 mm    | 4 Lagen | ESP32-S31-WROOM-1U, USB2517I, |
|       | (Unter Sitzbank, Audio/USV/PD)| (77x47 mm M2.5)| (ENIG)  | QCC3084 BT 5.4, LM5164, BQ24075,|
|       | Dual-Power: 12V & USB-C Service|               |         | LM66100 Ideal-Diode, Quad eFuse,|
|       | Vertikal-SMD (MicroLock/Picoflex)|              |         | SX1262 LoRa, ES8388, BMI270, CAN|
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 03**| **Satelliten-Pod Interface**  | 42 x 48 mm    | 4 Lagen | ESP32-C6, ES8388,    |
|       | (Koffer-Pod 1 & 2 Bodenwanne) | (36x42 mm M2.5| (ENIG)  | 4-Draht Bus, SW3516  |
|       | In-Bag 30W USB-PD Ladebuchse  | 2-seitig SMT  |         | 30W PD, J_AUDIO_PWR  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 05**| **Universal Front-Knoten**    | 82 x 50 mm    | 4 Lagen | ESP32-S3, SAM-M10Q,  |
|       | (Cockpit Riser Hub, GNSS/Sens)| (4x M2.5)     | (ENIG)  | Knowles MEMS Mic,    |
|       | 4-Draht Bus (Zero Tank-Heben!)|               |         | SC8102 PD, TMP117    |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 05B**| **Symmetrischer Spiegel-Pod** | 32 x 14 mm    | 2 Lagen | Bernstein BSD LED,   |
|       | (2x identisch für Links/Rechts| (M8/M10 Flansch)| (ENIG) | IP67 Taktiltaster,   |
|       | 100% Software-Defined Gesten) | 100% SMT      |         | TVS ESD, JST-GH 4P   |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 07**| **2-in-1 LoRa Smart-Keyfob**  | 38 x 19 mm    | 2 Lagen | Nordic nRF52840 SoC, |
|       | (Silent Pager, N52 Key & Qi)  | (Tasche M2)   | (ENIG)  | SX1262 LoRa, DRV2605L|
|       | Öffnet Pod-Slide-in Deckel    |               |         | BQ51003 Qi, JST-ACH  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 08**| **Radar 2.0 Sub-MCU & Wings** | 115 x 65 mm   | 2 Lagen | ESP32-C5 Dual-Band,  |
|       | (Wheeltec 77GHz & V2X Patch)  | (Flügel M2.5) | (ENIG)  | Wheeltec MR20 (AoP), |
|       | 12V & UART Kabelanbindung     |               |         | 36x WS2812B, JWPF 12V|
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 09**| **OMM 2.4 GHz UCS Intercom**  | 60 x 30 mm    | 2 Lagen | ESP32-C6 RISC-V,     |
|       | (ECE 22.06 Autonom & Pod)     | (UCS M2)      | (ENIG)  | TI BQ24075, ES8388,  |
|       | Nativ Digitales USB-Audio UAC |               |         | 600mAh LiPo, FXP73   |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 10**| **OMM 446 MHz UCS Intercom**  | 60 x 30 mm    | 4 Lagen | NiceRF SA818-DMR,    |
|       | (DMR Tier I & Analog PMR446)  | (UCS M2)      | (ENIG)  | ESP32-C6, BQ24075,   |
|       | Dual-Mode PMR/DMR via USB-Audio| (UCS M2)     | (ENIG)  | ES8388, Helix-Antenne|
+-------+-------------------------------+---------------+---------+----------------------+
```

### 1.1 Gliederung nach Systemkomponenten
1. **Kern-Baugruppen (Standard-Ausstattung jedes Bikes):**
   * **`PCBA 01` (Zentralbox Main Controller):** Zentrale Recheneinheit unter der Sitzbank für Energie-Management, USV, DSP-Mischung, Dual-Bluetooth-Headsets, LoRa-Schwarm und USB-Hub Koordination. Ausgestattet mit **Dual-Power Input** (12V Bordnetz via Molex Micro-Lock Plus `J1` / Gehäuseflansch Deutsch DTM-6 oder 5V USB-C Service-Port `J3` via TI LM66100 Ideal-Dioden-OR-ing für schreibtischbasiertes Flashen ohne 12V-Labornetzteil) und **vertikalen SMD-Steckverbindern (Pointing UP)** (Bordnetz `J1`, 4-Kanal Peripherie-Bus `J6` Picoflex 16-Pin, USV-Akku `J5`, Status-LED `J4`, Reserve-USB `J7`, USB-C `J3`).
   * **`PCBA 03` (Satelliten-Pod Interface Board):** Universelle Schnittstellenplatine am Boden beider Seitenkoffer-Pods (Pod 1 & Pod 2). Bietet einen integrierten USB-C Schnellladeport (bis 30W/60W) direkt im Koffer und bindet Sena, Cardo oder OMM verlustfrei an den 4-Draht-Bus an.
   * **`PCBA 05` (Universal Front-Knoten):** Cockpit-Einheit am Riser für Multi-GNSS (SAM-M10Q), Kaltluft-Sensorik, Ambient-Mikrofon und Qi-Zusatzspeisung. Verbunden über den 4-Draht-Kabelbaum durch den Harley-Kabelkanal (**ZERO Tank-Demontage!**).
   * **`PCBA 05B` (Symmetrische Under-Perch Spiegel-Pods):** Zwei baugleiche Platinen unter den Spiegelschrauben (Links & Rechts) für bilaterale Totwinkelwarnung (BSD bernsteinfarbene LEDs) und softwaredefinierte Daumentaster (PTT, Voice Assistant, 1-Klick Hazard Pin Drop für Waze, Cam-Tags, SOS).
2. **Empfohlene Erweiterungen & Peripherie:**
   * **`PCBA 07` (2-in-1 LoRa Smart-Keyfob & Silent Pager):** Tragbarer Schlüsselanhänger für 4,5 km Weitbereichs-Alarmierung, N52-Magnetschlüssel zum kontaktlosen Entriegeln des Pod-Slide-in Deckels und induktive Qi-Ladung.
   * **`PCBA 08` (Radar 2.0 Sub-MCU & Warnflügel):** Heckmodul mit 77-GHz-mmWave-Sensorik (AoP), autonomem Brems- und Kollisionsstrobe sowie 5.9 GHz V2X-Uplink, fest über 12V und UART angebunden.
   * **`PCBA 09` / `PCBA 10` (OMM UCS Intercom-Module):** Autarke ECE 22.06 Module für den Helm oder als Plug-in Audio-Engines im Koffer-Pod via USB Audio Class 2.0.
3. **Ersatzlos entfallene Baugruppen (Architektur-Bereinigung v10.0):**
   * **`PCBA 02` (Frühere Pod-Basisplatine):** Vollständig entfallen. Das Pod-Gehäuse ist ein Monocoque mit Slide-in Deckel und Dry-Flap; `PCBA 03` ruht direkt auf Dämpfern am Gehäuseboden.
   * **`PCBA 04` (Heck-Pod 3):** Vollständig gestrichen; LoRa sitzt auf `PCBA 01`, GNSS auf `PCBA 05`.
   * **`PCBA 06` (MagSafe Frame Dock Platine):** Ersetzt durch handelsübliche 4-Pin IP67 Magnet-Abrissschnittstellen (COTS).
   * **Qorvo DW3110 UWB Transceiver:** Auf allen Platinen ersatzlos gestrichen zugunsten des robusten 4-Draht Automotive-Backbones mit nativer USB 2.0 Datenübertragung und WebUSB.

---

## 2. Fertigungsstandard & JLCPCB 4-Lagen Stackup (JLC04161H-7628)

Für alle 4-Lagen-Platinen (`PCBA 01` und `PCBA 05`) wird der identische, streng impedanzkontrollierte Lagenaufbau verwendet:

```
+-------------------------------------------------------------+
| Layer 1 (F.Cu - Top): High-Speed Signale, USB-Diff, Bauteile|  (35 µm / 1 oz Cu)
+-------------------------------------------------------------+
| -- Prepreg 7628 (Dielektrikum, Er = 4.4, Dicke 0.2 mm) --   |
+-------------------------------------------------------------+
| Layer 2 (In1.Cu): Durchgängige Massefläche (GND_PWR / AGND) |  (17.5 µm Standard)
+-------------------------------------------------------------+
| -- FR4 Core (Isolationskern, Dicke 1.0 mm) --------------   |
+-------------------------------------------------------------+
| Layer 3 (In2.Cu): Power-Planes (VCC_3V3, VCC_5V, VBUS)      |  (17.5 µm Standard)
+-------------------------------------------------------------+
| -- Prepreg 7628 (Dielektrikum, Er = 4.4, Dicke 0.2 mm) --   |
+-------------------------------------------------------------+
| Layer 4 (B.Cu - Bottom): Sekundär-Routing, Masse-Shield     |  (35 µm / 1 oz Cu)
+-------------------------------------------------------------+
```

### 2.1 Standardisierte Net-Klassen & Leiterbahn-Geometrien
* **`Default`:** Leiterbahnbreite $0{,}20\,	ext{mm}$, Mindestabstand $0{,}20\,	ext{mm}$ (Logiksignale, GPIOs).
* **`Power_5V_12V`:** Leiterbahnbreite $0{,}60\,	ext{mm}$ (Stromtragfähigkeit bis $2{,}2\,	ext{A}$ bei $\Delta T < 10\,^\circ	ext{C}$).
* **`RF_50R`:** Leiterbahnbreite $0{,}35\,	ext{mm}$, Koplanarabstand $0{,}20\,	ext{mm}$ zur Massefläche (50 Ohm Wellenwiderstand für 868 MHz LoRa und 5.9 GHz V2X).
* **`USB_90R_DIFF`:** Leiterbahnbreite $0{,}20\,	ext{mm}$, differentieller Leiterbahnabstand $0{,}15\,	ext{mm}$ ($90\,\Omega \pm 10\,\%$ Differenzimpedanz für USB 2.0 High-Speed 480 Mbps).
* **`Audio_Sensitive`:** Leiterbahnbreite $0{,}25\,	ext{mm}$, Abstand $0{,}30\,	ext{mm}$ (abgeschirmt durch flankierende GND-Leiterbahnen).

---

## 3. PCBA 01: Zentralbox Main Controller (`openmotorbridge_central_box`)

![PCBA 01 Zentralbox Main Controller Top 3D](../images/pcba/pcba01_central_box_3d.png)
*Abbildung 7.1a: KiCad 3D-Render der Zentralbox-Hauptplatine Top (PCBA 01, 85 x 55 mm, 4 Lagen) mit ESP32-S31-WROOM-1U, Microchip USB2517I 7-Port Hub, Qualcomm QCC3084 BT 5.4 Audio SoC, LM5164-Q1 72V Buck, BQ24075 USV-Lader, Quad-eFuse U12, SX1262 LoRa 868 MHz und vertikal nach oben ragenden SMD-Steckverbindern (J1, J6, J5, J4, J7, J3).*

![PCBA 01 Zentralbox Main Controller Bottom 3D](../images/pcba/pcba01_central_box_bottom_3d.png)
*Abbildung 7.1b: KiCad 3D-Render der Zentralbox-Hauptplatine Bottom mit DM3D MicroSD-Push-Pull-Slot, TI LM66100 Ideal-Dioden-OR-ing Schaltung für Dual-Power (12V Bordnetz vs. USB-C Service), BMI270 6-Achs-IMU, ES8388 Audio-Codec und TCAN334G CAN-FD Transceiver.*

![PCBA 01 Zentralbox Layout Übersicht](../images/pcba/pcba01_layout_v10.svg)
*Abbildung 7.1c: Vektorbasiertes Bestückungs- und Routing-Layout der PCBA 01 (v10.0 Dual-Rail Monocoque Slide-In Standard).*

### 3.1 Technische Platinen-Kenndaten & Top/Bottom-Aufteilung
* **Abmessungen:** $85{,}0 \times 55{,}0\,\text{mm}$ (Außenkontur mit 4x M2.5 Montagebohrungen, $77{,}0 \times 47{,}0\,\text{mm}$ Lochabstand, kompatibel zum Dual-Rail Slide-In Trägerrahmen).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Gesamtdicke, $35\,\mu\text{m}$ Cu auf L1/L4, $17{,}5\,\mu\text{m}$ auf L2/L3, ENIG-Goldfinish, Lagenaufbau nach JLCPCB JLC04161H-7628).
* **Dual-Power Input Schaltung:**
  * **12V Bordnetz (Hauptversorgung):** Molex Micro-Lock Plus 1.25mm 6-Pin Vertikal-Header `J1` (interne Silikon-Kabelpeitsche zum Gehäuse-Flansch Deutsch DTM-6), eingangsseitig gegen Verpolung und Transienten geschützt und über Automotive-eFuse abgesichert.
  * **USB-C Service & Flash-Port (`J3`):** 16-Pin USB-C Buchse mit Texas Instruments `LM66100` Ideal-Diode (`D3`) für verlustarmes Ideal-Dioden-OR-ing (Bordnetz vs. USB-VBUS). Ermöglicht den autarken Werkbank-Betrieb, Firmware-Updates via WebUSB/DFU und Sensortests direkt am Schreibtisch über jedes Standard-USB-C-Netzteil (5V) ohne Labornetzteil.
* **Kompakte Vertikal-Steckverbinder (Pointing UP):**
  * Sämtliche internen Anschlüsse sind als ultrakompakte, vertikal nach oben weisende SMT-Stecker ausgeführt. Dadurch werden Biegeschleifen an den Platinenkanten vollständig vermieden und die Kabelpeitschen laufen parallel nach oben in den Kabelkanal des Monocoque-Gehäuses ab.
* **Bestückung Top-Layer (F.Cu):**
  * **Hauptcontroller (`U2`):** Espressif `ESP32-S31-WROOM-1U` (Dual-Core RISC-V @ 320 MHz mit 128-Bit SIMD AI Engine für On-Device Audio-Signalverarbeitung und Sprachfilterung, 16 MB Flash, 8 MB Octal-PSRAM, externe U.FL Buchse) für Systemsteuerung, FreeRTOS DSP-Pipeline, zentralen geometrischen BLE-Master (Lenkertaster, OEM-Adapter, Action-Cam, Keyfob, TPMS) und CAN-FD Management.
  * **Industrial USB 2.0 Hub Controller (`U8`):** Microchip `USB2517I-JZX` (QFN-64, $-40\,^\circ\text{C}\dots+85\,^\circ\text{C}$ Automotive-Grade) 7-Port High-Speed 480 Mbps Hub mit 24.000 MHz Quarz `Y2`. Bindet alle Peripherieknoten (Front, Pod 1, Pod 2, Radar, Helm-Audio, ESP32 und Service-Port) transparent und synchron an.
  * **Dedizierter Helm-Audio-SoC (`U9`):** **Qualcomm QCC3084** Bluetooth 5.4 Audio SoC Modul ($13 \times 18\,\text{mm}$ mit integrierter Keramik-Chipantenne) für Dual-A2DP (aptX HD, Low Latency), LE Audio Auracast Broadcast, HFP 1.8 Wideband Telefonie und nativen USB Audio Class 2.0 Uplink zu Hub `U8`.
  * **Automotive Power Stage (`U1`):** Texas Instruments `LM5164-Q1` synchroner 72V-Buck-Converter (erzeugt `VCC_BUCK` / 5V aus dem 12V–72V Bordnetz) und TI `BQ24075` Power-Path-Controller mit Ladeelektronik für den internen USV-Akku.
  * **Quad Automotive eFuse Smart Switch (`U12`):** QFN-20 4-Kanal-Lastschalter zur getrennten Absicherung, Strommessung und thermischen Abschaltung der 4 Peripheriestränge (Front, Pod 1, Pod 2, Radar).
  * **Weitbereichsfunk (`U10`):** Semtech `SX1262` LoRa Transceiver (+22 dBm PA) mit U.FL Buchse `ANT1` zur FXP895 Antenne in der Gehäusedeckeltasche.
  * **Status-Anzeige & Bedienelemente:** WS2812B RGB Smart-LED `D1`, Pairing-Hardwaretaster `SW1` sowie Vertikalstecker `J1` (Bordnetz 6P), `J6` (Peripherie 16P), `J5` (USV-Akku 4P), `J4` (RGB-LED 3P), `J7` (Reserve USB 4P) und `J3` (USB-C 16P).
* **Bestückung Bottom-Layer (B.Cu):**
  * **MicroSD-Kartenslot (`J2`):** Hirose `DM3D-SF` Push-Pull MicroSD-Kartenhalter (4-Bit High-Speed SDIO), bündig an der Stirnkante platziert für werkzeugfreien Service-Zugang.
  * **Audio-Codec (`U3`):** Everest Semi `ES8388` 24-Bit / 48 kHz Low-Power Stereo-Audio-Codec (QFN-28).
  * **6-Achs-IMU (`U5`):** Bosch `BMI270` Ultra-Low-Power IMU (I2C) für Wake-on-Motion Diebstahlüberwachung, Schräglagenmessung und Sturzerkennung.
  * **CAN-FD Transceiver (`U6`):** Texas Instruments `TCAN334G` 5 Mbps CAN-FD Transceiver (SOIC-8).
  * **Ideal-Diode Schaltung (`D3`):** Texas Instruments `LM66100` (SOT-23-6) für rückspeisefreien Dual-Power Betrieb.
  * **Analog-LDO (`U11`):** Texas Instruments `TPS7A0533` 3.3V Ultra-Low-Noise LDO für analoge Rails.

---

### 3.2 Platinen-Steckverbinder & Exakte Pinbelegung

#### 3.2.1 Header J1: Fahrzeug-Bordnetz & CAN-Bus (Molex Micro-Lock Plus 1.25mm 6-Pin SMD Vertikal)
Verbindet die Zentralbox über eine interne geschirmte Kabelpeitsche mit dem fahrzeugseitigen Deutsch DTM04-6P Gehäuseflansch:

```
+---------------------------------------------------------------------------------------------------------------+
| HEADER J1: MOLEX MICRO-LOCK PLUS 6-PIN VERTIKAL (505568-0671) - BORDNETZ & CAN-BUS                            |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Kabelbaum-Zweig     | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | KL30_IN        | +9V...+72V DC Dauerplus  | AWG20 0.50² | DTM Pin 1 (Batterie)| Bordnetz Dauerplus (eFuse)|
|  2  | KL15_IN        | +9V...+72V DC Zündung    | AWG22 0.34² | DTM Pin 2 (Zündung) | Zündungs-Sense & Wake-Up|
|  3  | GND_PWR        | Power-Masse (0V)         | AWG20 0.50² | DTM Pin 3 (Batterie)| Zentrale Systemmasse    |
|  4  | CAN_H          | CAN-FD High (ISO 11898-2)| AWG24 0.22² | DTM Pin 4 (Fahrzeug)| Fahrzeug-CAN Bus High   |
|  5  | CAN_L          | CAN-FD Low (ISO 11898-2) | AWG24 0.22² | DTM Pin 5 (Fahrzeug)| Fahrzeug-CAN Bus Low    |
|  6  | GND_SHIELD     | Schirmmasse / Chassis    | AWG20 0.50² | DTM Pin 6 (Rahmen)  | Gehäuse- & Schirmschutz |
| MP1 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 1  |
| MP2 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 2  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

#### 3.2.2 Header J6: OMB 4-Kanal Peripherie-Bus (Molex Picoflex 16-Pin 2x08 Vertikal)
Zentraler Schnittstellen-Header (Molex Picoflex `90814-0016`, 1.27mm Raster, vertikal nach oben) zur Speisung und nativer USB 2.0 High-Speed Datenanbindung aller 4 Peripheriestränge (Front, Pod 1, Pod 2, Radar). Jeder Strang besitzt eine eigene eFuse-Strombegrenzung:

```
+---------------------------------------------------------------------------------------------------------------+
| HEADER J6: MOLEX PICOFLEX 16-PIN (2x08) VERTIKAL (90814-0016) - 4 AUTARKE OMB-SYSTEMSTRÄNGE                  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Zielkomponente      | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | VBUS_FRONT     | +12V DC (bis 60W / 5.0A) | AWG18 0.75² | Strang 1 (Front)    | Speisung Front-Knoten   |
|  2  | GND_PWR        | Power-Masse (0V)         | AWG18 0.75² | Strang 1 (Front)    | Leistungs-Rückleiter    |
|  3  | BUS1_DM        | USB 2.0 High-Speed D-    | AWG26 0.14² | Strang 1 (Front)    | Hub Port 2 Daten-Uplink |
|  4  | BUS1_DP        | USB 2.0 High-Speed D+    | AWG26 0.14² | Strang 1 (Front)    | Hub Port 2 Daten-Uplink |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  5  | VBUS_POD1      | +12V DC (bis 30W / 2.5A) | AWG20 0.50² | Strang 2 (Pod 1 L)  | Speisung Pod 1 & Lader  |
|  6  | GND_PWR        | Power-Masse (0V)         | AWG20 0.50² | Strang 2 (Pod 1 L)  | Leistungs-Rückleiter    |
|  7  | BUS2_DM        | USB 2.0 High-Speed D-    | AWG28 0.08² | Strang 2 (Pod 1 L)  | Hub Port 3 Audio/Daten  |
|  8  | BUS2_DP        | USB 2.0 High-Speed D+    | AWG28 0.08² | Strang 2 (Pod 1 L)  | Hub Port 3 Audio/Daten  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  9  | VBUS_POD2      | +12V DC (bis 30W / 2.5A) | AWG20 0.50² | Strang 3 (Pod 2 R)  | Speisung Pod 2 & Lader  |
| 10  | GND_PWR        | Power-Masse (0V)         | AWG20 0.50² | Strang 3 (Pod 2 R)  | Leistungs-Rückleiter    |
| 11  | BUS3_DM        | USB 2.0 High-Speed D-    | AWG28 0.08² | Strang 3 (Pod 2 R)  | Hub Port 4 Audio/Daten  |
| 12  | BUS3_DP        | USB 2.0 High-Speed D+    | AWG28 0.08² | Strang 3 (Pod 2 R)  | Hub Port 4 Audio/Daten  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| 13  | VBUS_RADAR     | +12V geschaltet (1.5A)   | AWG22 0.34² | Strang 4 (Heck-Rad.)| Speisung Radar Wheeltec |
| 14  | GND_PWR        | Power-Masse (0V)         | AWG22 0.34² | Strang 4 (Heck-Rad.)| Masse Heck-Radar        |
| 15  | BUS4_DM        | USB 2.0 High-Speed D-    | AWG24 0.22² | Strang 4 (Heck-Rad.)| Hub Port 5 Telemetrie   |
| 16  | BUS4_DP        | USB 2.0 High-Speed D+    | AWG24 0.22² | Strang 4 (Heck-Rad.)| Hub Port 5 Telemetrie   |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| MP1 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 1  |
| MP2 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 2  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

#### 3.2.3 Header J5: USV-Akku & NTC-Temperaturfühler (Molex Micro-Lock Plus 1.25mm 4-Pin Vertikal)
Verbindet den internen 2.200-mAh-USV-Pouch-Akku (LiFePO4 oder LiPo) mit dem BQ24075 Power-Path-Controller und ESP32 ADC:

```
+---------------------------------------------------------------------------------------------------------------+
| HEADER J5: MOLEX MICRO-LOCK PLUS 4-PIN VERTIKAL (505568-0471) - USV-BATTERIE & THERMISTOR                     |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Verbunden mit       | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | BAT_PLUS       | +3.2V...+4.2V DC (Akku +)| AWG22 0.34² | BQ24075 BAT-Pin     | Akku-Lade- & Entladestrom|
|  2  | GND_PWR        | Power-Masse (Akku -)     | AWG22 0.34² | GND_PWR Masseplane  | Batterie-Masse          |
|  3  | BAT_NTC        | Analog In (0...3.3V)     | AWG26 0.14² | ESP32-S31 (Pin 25)  | 10k NTC Temperaturfühler|
|  4  | GND_PWR        | Sensor-Masse (0V)        | AWG26 0.14² | GND_PWR Masseplane  | NTC-Rückleitung         |
| MP1 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 1  |
| MP2 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 2  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

#### 3.2.4 Header J4: Externe Gehäuse-RGB-Status-LED (Molex Micro-Lock Plus 1.25mm 3-Pin Vertikal)
Ermöglicht den Anschluss einer extern sichtbaren Gehäuse-Status-LED (z.B. im Gehäusedeckel oder am Cockpit):

```
+---------------------------------------------------------------------------------------------------------------+
| HEADER J4: MOLEX MICRO-LOCK PLUS 3-PIN VERTIKAL (505568-0371) - EXTERNE STATUS-LED                            |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Verbunden mit       | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | VCC_5V         | +5.0V DC (Power Out)     | AWG24 0.22² | 5V Power Plane      | LED-Betriebsspannung    |
|  2  | RGB_LED_DATA   | Digital Out (WS2812B DIN)| AWG26 0.14² | ESP32-S31 (Pin 28)  | Serielles LED-Datensignal|
|  3  | GND_PWR        | Power-Masse (0V)         | AWG24 0.22² | GND_PWR Masseplane  | LED-Masse               |
| MP1 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 1  |
| MP2 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 2  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

#### 3.2.5 Header J7: Reserve USB Port 7 (Molex Micro-Lock Plus 1.25mm 4-Pin Vertikal)
Führt den 7. Downstream-Port des Microchip USB2517I Hubs für künftige Funktionserweiterungen (z.B. LTE/5G-Modem oder Dashcam) heraus:

```
+---------------------------------------------------------------------------------------------------------------+
| HEADER J7: MOLEX MICRO-LOCK PLUS 4-PIN VERTIKAL (505568-0471) - RESERVE USB 2.0 PORT 7                        |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Verbunden mit       | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | VCC_5V         | +5.0V DC (Power Out)     | AWG22 0.34² | 5V Power Plane      | USB VBUS 5V Speisung    |
|  2  | RES_USB_DM     | USB 2.0 D- (Differential)| AWG28 0.08² | USB2517I (Pin 60)   | USB Port 7 Data Minus   |
|  3  | RES_USB_DP     | USB 2.0 D+ (Differential)| AWG28 0.08² | USB2517I (Pin 61)   | USB Port 7 Data Plus    |
|  4  | GND_PWR        | Power-Masse (0V)         | AWG22 0.34² | GND_PWR Masseplane  | USB Masse               |
| MP1 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 1  |
| MP2 | GND_PWR        | Mechanische Halterung    | SMT Pad     | PCB Massefläche     | Solder Retention Pad 2  |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

#### 3.2.6 Buchse J3: USB Type-C Service & Flash-Port (16-Pin SMD Receptacle)
Sitzt an der Gehäusefront für schnellen Werkbank-Zugriff, DFU-Flashen und Diagnose:

```
+---------------------------------------------------------------------------------------------------------------+
| BUCHSE J3: USB TYPE-C 16-PIN RECEPTACLE (HRO TYPE-C-31-M-12) - SERVICE & DFU-PORT                             |
+-----+----------------+--------------------------+---------------------+---------------------------------------+
| Pin | Signalname     | Signalart / Pegel        | Verbunden mit       | Funktion & Spezifikation              |
+-----+----------------+--------------------------+---------------------+---------------------------------------+
| A1  | GND_PWR        | Power-Masse (0V)         | GND_PWR Masseplane  | USB-C Systemmasse                     |
| A4  | USBC_VBUS      | +5.0V DC (Power In)      | LM66100 Diode (D3)  | 5V USB Busspannung (Dual-Power Sink)  |
| A5  | CC1            | Konfigurations-Kanal 1   | 5.1 kΩ Pull-Down    | UFP-Erkennung & 5V/3A Aushandlung     |
| A6  | USBC_DP        | USB 2.0 High-Speed D+    | USB2517I Hub Pin 9  | Upstream USB Datenleitung Plus        |
| A7  | USBC_DM        | USB 2.0 High-Speed D-    | USB2517I Hub Pin 8  | Upstream USB Datenleitung Minus       |
| A8  | CC2            | Konfigurations-Kanal 2   | 5.1 kΩ Pull-Down    | UFP-Erkennung & 5V/3A Aushandlung     |
| A9  | USBC_VBUS      | +5.0V DC (Power In)      | LM66100 Diode (D3)  | 5V USB Busspannung (Dual-Power Sink)  |
| A12 | GND_PWR        | Power-Masse (0V)         | GND_PWR Masseplane  | USB-C Systemmasse                     |
| SH1 | GND_SHIELD     | Schirmmasse              | Gehäuseschirmung    | EMV-Schirmgehäuse Lötlasche Links     |
| SH2 | GND_SHIELD     | Schirmmasse              | Gehäuseschirmung    | EMV-Schirmgehäuse Lötlasche Rechts    |
+-----+----------------+--------------------------+---------------------+---------------------------------------+
```

#### 3.2.7 Slot J2: MicroSD-Kartenleser (Hirose DM3D-SF 9-Pin Push-Pull)
Bietet 4-Bit High-Speed SDIO Anbindung an den ESP32-S31 für unterbrechungsfreie Blackbox-Telemetrie und Offline-Karten:

```
+---------------------------------------------------------------------------------------------------------------+
| KARTENSLOT J2: HIROSE DM3D-SF PUSH-PULL MICROSD-HALTER (4-BIT SDIO)                                           |
+-----+----------------+--------------------------+---------------------+---------------------------------------+
| Pin | Signalname     | Signalart / Pegel        | Verbunden mit       | Funktion & Spezifikation              |
+-----+----------------+--------------------------+---------------------+---------------------------------------+
|  1  | SD_DAT2        | Digital I/O (3.3V SDIO)  | ESP32-S31 (Pin 34)  | SDIO Datenleitung 2 (Pull-Up 10k)     |
|  2  | SD_DAT3        | Digital I/O (3.3V SDIO)  | ESP32-S31 (Pin 38)  | SDIO Datenleitung 3 / Card Select     |
|  3  | SD_CMD         | Digital I/O (3.3V SDIO)  | ESP32-S31 (Pin 36)  | SDIO Command / Response Leitung       |
|  4  | VCC_3V3        | Power In (+3.3V DC)      | 3.3V LDO Rail       | MicroSD Betriebsspannung (100nF+10µF) |
|  5  | SD_CLK         | Digital Out (Clock)      | ESP32-S31 (Pin 35)  | SDIO Bus-Takt (bis 40 MHz)            |
|  6  | GND_PWR        | Masse (0V)               | GND_PWR Masseplane  | Versorgungsmasse                      |
|  7  | SD_DAT0        | Digital I/O (3.3V SDIO)  | ESP32-S31 (Pin 37)  | SDIO Datenleitung 0                   |
|  8  | SD_DAT1        | Digital I/O (3.3V SDIO)  | ESP32-S31 (Pin 33)  | SDIO Datenleitung 1                   |
|  9  | SD_CD          | Digital In (Active Low)  | ESP32-S31 (Pin 39)  | Card Detect Schalter (Karte gesteckt) |
| SH  | GND_PWR        | Gehäuseschirmung         | GND_PWR Masseplane  | 3x Schirm- und Halte-Lötpads (SH1-SH3)|
+-----+----------------+--------------------------+---------------------+---------------------------------------+
```

---

### 3.3 Microchip USB2517I-JZX 7-Port Hub Architektur (`U8`)

Der industrielle 7-Port Hub-Controller bildet das digitale Nervenzentrum der Zentralbox. Er verbindet den Service-Port transparent mit allen Subknoten:

```
+---------------------------------------------------------------------------------------------------------------+
| MICROCHIP USB2517I-JZX (QFN-64): 7-PORT HIGH-SPEED USB 2.0 HUB PORTBELEGUNG                                   |
+----------+--------------------+-----------------------+---------------------+---------------------------------+
| Port     | Signal-Pins (D-/D+)| Netze                 | Ziel-Komponente     | Funktion & Datenstrom           |
+----------+--------------------+-----------------------+---------------------+---------------------------------+
| Upstream | Pin 8 / Pin 9      | USBC_DM / USBC_DP     | Service-Port J3     | Host-Verbindung Laptop / Tablet |
+----------+--------------------+-----------------------+---------------------+---------------------------------+
| Port 1   | Pin 16 / Pin 17    | ESP_USB_DM / ESP_USB_DP| ESP32-S31 (Pin 13/14)| Nativer USB-CDC, DFU & WebUSB  |
| Port 2   | Pin 24 / Pin 25    | BUS1_DM / BUS1_DP     | Header J6 (Pin 3/4) | Front-Knoten PCBA 05            |
| Port 3   | Pin 32 / Pin 33    | BUS2_DM / BUS2_DP     | Header J6 (Pin 7/8) | Koffer-Pod 1 PCBA 03 (Links)    |
| Port 4   | Pin 40 / Pin 41    | BUS3_DM / BUS3_DP     | Header J6 (Pin 11/12)| Koffer-Pod 2 PCBA 03 (Rechts)   |
| Port 5   | Pin 48 / Pin 49    | BUS4_DM / BUS4_DP     | Header J6 (Pin 15/16)| Heck-Radar PCBA 08 (MR20 UART)  |
| Port 6   | Pin 56 / Pin 57    | BT_USB_DM / BT_USB_DP | QCC3084 (Pin 13/14) | USB Audio Class 2.0 Helm-Audio  |
| Port 7   | Pin 60 / Pin 61    | RES_USB_DM / RES_USB_DP| Header J7 (Pin 2/3) | Reserve USB Port für Add-ons    |
+----------+--------------------+-----------------------+---------------------+---------------------------------+
| Takt/RST | Pin 2: RESET_N (Pull-Up 100k) | Pin 4/5: XTALIN/XTALOUT an 24.000 MHz Quarz Y2 (18pF Kondensatoren) |
+----------+----------------------------------------------------------------------------------------------------+
```

---

### 3.4 Qualcomm QCC3084 Bluetooth 5.4 Audio SoC Modul (`U9`)

Der auf der Oberseite platzierte **Qualcomm QCC3084** verbindet Helme drahtlos über hardware-beschleunigtes Dual-A2DP (aptX HD / Adaptive) und HFP 1.8 und kommuniziert zeitgleich über I2S und nativen USB-Audio-Stream:

```
+---------------------------------------------------------------------------------------------------------------+
| QUALCOMM QCC3084 (14-PIN MODUL MIT INTEGRIERTER HF-ANTENNE) - SCHNITTSTELLENBELEGUNG                          |
+-----+----------------+--------------------+-------------------+-----------------------------------------------+
| Pin | Signalname     | Signalart          | Verbunden mit     | Funktion & Protokoll                          |
+-----+----------------+--------------------+-------------------+-----------------------------------------------+
|  1  | VCC_3V3        | Power In (+3.3V)   | 3.3V Power Plane  | Modul-Betriebsspannung                        |
|  2  | GND_PWR        | Masse (0V)         | GND_PWR Plane     | HF- und Systemmasse                           |
|  3  | I2S_MCLK       | Digital In (Clock) | ESP32-S31 (Pin 12)| I2S Master-Clock (12.288 MHz)                 |
|  4  | I2S_BCLK       | Digital In (BitClk)| ESP32-S31 (Pin 30)| I2S Bit-Clock (3.072 MHz)                     |
|  5  | I2S_WS         | Digital In (LRCK)  | ESP32-S31 (Pin 32)| I2S Word-Select / Frame-Sync (48 kHz)         |
|  6  | I2S_DOUT       | Digital In (Audio) | ESP32-S31 (Pin 15)| Stereo-PCM Audiodaten zum QCC3084             |
|  7  | I2S_DIN        | Digital Out (Mic)  | ESP32-S31 (Pin 16)| HFP-Mikrofonaudio zum ESP32 DSP               |
|  8  | GND_PWR        | Masse (0V)         | GND_PWR Plane     | HF-Schirmmasse                                |
|  9  | BT_UART_TX     | Digital Out (UART) | ESP32-S31 (Pin 11)| QCC3084 Telemetrie- und Statusmeldungen       |
| 10  | BT_UART_RX     | Digital In (UART)  | ESP32-S31 (Pin 10)| ESP32 AT-Steuerbefehle                        |
| 11  | BT_EN          | Digital In (Reset) | ESP32-S31 (Pin 9) | Power-Down & Hardware-Reset                   |
| 12  | GND_PWR        | Masse (0V)         | GND_PWR Plane     | HF-Schirmmasse                                |
| 13  | BT_USB_DM      | USB 2.0 D- (Data)  | USB2517I (Pin 56) | USB Audio Class 2.0 High-Res Stream Minus     |
| 14  | BT_USB_DP      | USB 2.0 D+ (Data)  | USB2517I (Pin 57) | USB Audio Class 2.0 High-Res Stream Plus      |
+-----+----------------+--------------------+-------------------+-----------------------------------------------+
```

---

### 3.5 Quad Automotive eFuse Smart Switch (`U12`)

Die integrierte 4-Kanal-eFuse schützt die Peripherieleitungen vor Kabelkurzschlüssen und Überlastung:

```
+---------------------------------------------------------------------------------------------------------------+
| QUAD AUTOMOTIVE EFUSE (QFN-20): LASTKANAL-BELEGUNG                                                            |
+-------+--------------------+--------------------+--------------------+----------------------------------------+
| Kanal | Eingangs-Pin       | Ausgangs-Pin       | Netzknoten         | Absicherung & Funktion                 |
+-------+--------------------+--------------------+--------------------+----------------------------------------+
| In    | Pin 1, 2           | -                  | KL30_IN            | Bordnetz-Zuleitung 12V DC              |
| CH 1  | -                  | Pin 5              | VBUS_FRONT         | Front-Knoten Speisung (Limit: 5.0A)    |
| CH 2  | -                  | Pin 6              | VBUS_POD1          | Koffer-Pod 1 Speisung (Limit: 2.5A)    |
| CH 3  | -                  | Pin 7              | VBUS_POD2          | Koffer-Pod 2 Speisung (Limit: 2.5A)    |
| CH 4  | -                  | Pin 8              | VBUS_RADAR         | Heck-Radar Speisung (Limit: 1.5A)      |
| GND   | Pin 10, EP         | -                  | GND_PWR            | Thermisches Massepad                   |
+-------+--------------------+--------------------+--------------------+----------------------------------------+
```

---

### 3.6 ESP32-S31-WROOM-1U (`U2`) Vollständige Pinout-Matrix

```
+---------------------------------------------------------------------------------------------------------------+
| ESP32-S31-WROOM-1U (41-PIN MODUL) PINOUT & GPIO-ZUORDNUNG AUF PCBA 01                                         |
+-----+----------------+----------------------+--------------------+--------------------------------------------+
| Pin | Signalname     | ESP32 GPIO           | Peripherie / IC    | Funktion & Beschreibung                    |
+-----+----------------+----------------------+--------------------+--------------------------------------------+
|  1  | GND_PWR        | GND                  | Systemmasse        | Power Ground                               |
|  2  | VCC_3V3        | 3V3                  | 3.3V Power Rail    | Betriebsspannung ESP32-S31                 |
|  3  | ESP_EN         | CHIP_PU              | RC-Glied / Taster  | Hardware Enable / Reset                    |
|  4  | SPI_SCK        | GPIO 12 (FSPI CLK)   | SX1262 LoRa (Pin20)| LoRa SPI Bus Takt                          |
|  5  | KL15_SENSE     | GPIO 4               | Spannungsteiler    | Zündungsplus-Erkennung (Wake-Up)           |
|  6  | SPI_MISO       | GPIO 13 (FSPI MISO)  | SX1262 LoRa (Pin18)| LoRa SPI Daten vom Transceiver             |
|  7  | SPI_MOSI       | GPIO 11 (FSPI MOSI)  | SX1262 LoRa (Pin19)| LoRa SPI Daten zum Transceiver             |
|  8  | UART_TXD0      | U0TXD                | Debug Header       | Serielle Konsole TX (115200 Baud)         |
|  9  | BT_EN          | GPIO 1               | QCC3084 (Pin 11)   | Bluetooth Modul Reset / Power-Down         |
| 10  | BT_UART_RX     | GPIO 2               | QCC3084 (Pin 10)   | Bluetooth AT Steuerbefehle RX              |
| 11  | BT_UART_TX     | GPIO 3               | QCC3084 (Pin 9)    | Bluetooth Telemetrie / Status TX           |
| 12  | I2S_MCLK       | GPIO 0               | QCC3084 & ES8388   | I2S Audio Master Clock (12.288 MHz)        |
| 13  | ESP_USB_DM     | GPIO 19 (USB D-)     | USB2517I (Pin 16)  | Nativer USB CDC / WebUSB D-                |
| 14  | ESP_USB_DP     | GPIO 20 (USB D+)     | USB2517I (Pin 17)  | Nativer USB CDC / WebUSB D+                |
| 15  | I2S_DOUT       | GPIO 17 (I2S DOUT)   | QCC3084 & ES8388   | I2S PCM Audio Out (DSP Mix an Headsets)    |
| 16  | I2S_DIN        | GPIO 18 (I2S DIN)    | QCC3084 & ES8388   | I2S PCM Audio In (Mikrofon-Streams)        |
| 17  | I2C_SDA        | GPIO 8 (I2C SDA)     | BMI270 & ES8388    | I2C Datenleitung Sensorik & Codec          |
| 18  | I2C_SCL        | GPIO 9 (I2C SCL)     | BMI270 & ES8388    | I2C Taktleitung Sensorik & Codec           |
| 19  | LORA_DIO1      | GPIO 14              | SX1262 LoRa (Pin15)| LoRa Packet Rx/Tx Interrupt                |
| 20  | LORA_BUSY      | GPIO 21              | SX1262 LoRa (Pin14)| LoRa Transceiver Busy-Signal               |
| 21  | CAN_TX         | GPIO 5               | TCAN334G (Pin 1)   | CAN-FD Transmit Data                       |
| 22  | CAN_RX         | GPIO 6               | TCAN334G (Pin 4)   | CAN-FD Receive Data                        |
| 23  | LORA_RST       | GPIO 7               | SX1262 LoRa (Pin 1)| LoRa Transceiver Hardware Reset            |
| 24  | LORA_NSS       | GPIO 10 (FSPI CS)    | SX1262 LoRa (Pin21)| LoRa SPI Chip Select                       |
| 25  | BAT_NTC        | GPIO 15 (ADC2_CH4)   | Header J5 (Pin 3)   | USV Akku NTC Temperaturüberwachung         |
| 26  | GND_PWR        | GND                  | Systemmasse        | Power Ground                               |
| 27  | ESP_BOOT       | GPIO 0 (Boot Mode)   | Taster SW1         | Bootloader-Aktivierung bei Reset           |
| 28  | RGB_LED_DATA   | GPIO 48              | Header J4 & D1     | WS2812B RGB Smart-LED Datenleitung         |
| 29  | UART_RXD0      | U0RXD                | Debug Header       | Serielle Konsole RX                        |
| 30  | I2S_BCLK       | GPIO 16 (I2S BCLK)   | QCC3084 & ES8388   | I2S Bit-Clock (3.072 MHz)                  |
| 31  | BAT_SENSE      | GPIO 10 (ADC1_CH9)   | BQ24075 BAT-Pin    | Analoge USV Akkuspannungsmessung           |
| 32  | I2S_WS         | GPIO 47 (I2S WS)     | QCC3084 & ES8388   | I2S Word Select / Frame Sync (48 kHz)      |
| 33  | SD_DAT1        | GPIO 33 (SDIO D1)    | MicroSD J2 (Pin 8)  | MicroSD 4-Bit Datenleitung 1               |
| 34  | SD_DAT2        | GPIO 34 (SDIO D2)    | MicroSD J2 (Pin 1)  | MicroSD 4-Bit Datenleitung 2               |
| 35  | SD_CLK         | GPIO 35 (SDIO CLK)   | MicroSD J2 (Pin 5)  | MicroSD Bus-Takt                           |
| 36  | SD_CMD         | GPIO 36 (SDIO CMD)   | MicroSD J2 (Pin 3)  | MicroSD Command / Response                 |
| 37  | SD_DAT0        | GPIO 37 (SDIO D0)    | MicroSD J2 (Pin 7)  | MicroSD 4-Bit Datenleitung 0               |
| 38  | SD_DAT3        | GPIO 38 (SDIO D3)    | MicroSD J2 (Pin 2)  | MicroSD 4-Bit Datenleitung 3               |
| 39  | SD_CD          | GPIO 39              | MicroSD J2 (Pin 9)  | Card Detect (MicroSD Karte gesteckt)       |
| 40  | GND_PWR        | GND                  | Systemmasse        | Power Ground                               |
| 41  | GND_PWR        | Thermal EP (13 Vias) | GND_PWR Plane      | Zentrales Massepads & Kühlung              |
+-----+----------------+----------------------+--------------------+--------------------------------------------+
```

---

### 3.7 Systemweite Funk-Architektur, Frequenztrennung & Geometrischer BLE-Master

In OpenMotorBridge v10.0 ist die drahtlose Kommunikation strikt nach **HF-Physik, geometrischem Schwerpunkt und Frequenztrennung** strukturiert:

```
+---------------------------------------------------------------------------------------------------------------+
|                            GEOMETRISCHE FUNK-TOPOLOGIE DES MOTORRADS (v10.0)                                  |
+---------------------------------------------------------------------------------------------------------------+
|                                    [ LENKER / COCKPIT: FRONT NODE ]                                           |
|                                       • 5 GHz / 6 GHz Wi-Fi (C5 / E22)                                        |
|                                       • Wireless Android Auto / Apple CarPlay (10 cm)                         |
|                                       • High-Speed Dashcam Video-Sync & PWA Webserver                         |
|                                       • Befreit von BLE (keine Kanalüberlastung!)                             |
|                                                       ▲                                                       |
|                                                       │  Kabel 2 Strang 1: USB 2.0 High-Speed                 |
|                                                       │  (480 Mbps) + 12V 60W (Picoflex 16P)                  |
|                                                       ▼                                                       |
|     [ POD 1 LINKS: 50 cm ]             [ ZENTRALBOX: GEOMETRISCHER SCHWERPUNKT ]        [ POD 2 RECHTS: 50 cm ]|
|  • OEM-Adapter (Sena Mesh)           • ESP32-S31 BLE-Master (U.FL Gehäuseantenne)    • OEM-Adapter (Cardo Edge)|
|  • In-Bag Ladeelektronik             • Bündelt BLE: Taster, Cams, Keyfob, TPMS       • In-Bag Ladeelektronik  |
|                                      • Qualcomm QCC3084: Dual-Helm Audio (BT 5.4)                            |
|                                      • SX1262 LoRa: 868 MHz Schwarm-Telemetrie & SOS                         |
|                                      • S31 Wi-Fi: IM NORMALBETRIEB AUS (Null Störung)                         |
|                                                       ▲                                                       |
|                                                       │  Kabel 2 Strang 4: USB 2.0 High-Speed                 |
|                                                       │  (480 Mbps) + 12V 1.5A (Picoflex 16P)                 |
|                                                       ▼                                                       |
|                                           [ HECK: RADAR NODE ]                                                |
|                                       • ESP32-C5 Sub-MCU mit 5 GHz V2X                                        |
|                                       • Wheeltec MR20 Radar & 36-LED Halo                                     |
|                                       • 100% kabelgebundene Datenübertragung                                  |
+---------------------------------------------------------------------------------------------------------------+
```

1. **Zentralbox (PCBA 01) als geometrischer BLE-Master:**
   * **Symmetrische Abstände:** Die Zentralbox sitzt mittig auf der Batteriebrücke unter der Sitzbank und hat zu beiden Koffer-Pods links und rechts exakt denselben kurzen Abstand von nur ca. $50\,\text{cm}$, zum Lenker ca. $90\,\text{cm}$ und zum Fahrer ca. $30\,\text{cm}$.
   * **Dedizierte U.FL-Antenne:** Der `ESP32-S31` nutzt eine externe U.FL-Antenne im Monocoque-Gehäuse für ein verlustfreies 360°-Rundstrahlfeld über das gesamte Motorrad.
   * **Zentrale Event-Verarbeitung:** Sämtliche Steuer- und Sensordaten (OEM-Adapter PTT-Status in beiden Koffer-Pods, BMW WonderWheel / Lenkertaster, Action-Cam Trigger, Smart Keyfob und Reifendruck TPMS) laufen direkt per BLE im `ESP32-S31` ein. Dadurch entfällt jede Bus-Latenz über USB.
   * **Wi-Fi-Deaktivierung im Normalbetrieb:** Das interne 2,4-GHz-WLAN des `ESP32-S31` bleibt im Fahrbetrieb deaktiviert, um jegliche HF-Interferenzen mit dem direkt benachbarten Qualcomm `QCC3084` (Helm-Audio) auszuschließen.
2. **Front Node (PCBA 05 v10) als Cockpit-WLAN-Spezialist:**
   * **Strikte Frequenztrennung (5 GHz / 6 GHz):** Der Front-Knoten spannt das Cockpit-WLAN auf 5 GHz (bzw. 6 GHz Wi-Fi 6E via `ESP32-E22` / `ESP32-C5`) auf. Da dieses Band physikalisch weit vom 2,4-GHz-Band der Zentralbox entfernt ist, arbeiten Helm-Bluetooth und Cockpit-WLAN völlig störungsfrei parallel.
   * **Line-of-Sight zum Smartphone:** 10 bis 20 cm Abstand zum Smartphone im Lenkerhalter ermöglichen Gigabit-Throughput für Dashcam-Downloads und verzögerungsfreies Wireless CarPlay / Android Auto Streaming.
   * **Kein BLE-Overhead:** Der Front Node benötigt keinen eigenen BLE-Master-Stack.
3. **Radar Node (PCBA 08 v10) mit 5 GHz V2X:**
   * Der `ESP32-C5` nutzt seinen 5-GHz-Transceiver im Raw-Packet-Injection-Modus (802.11p OCB) für fahrzeugübergreifende **V2X-Warnmeldungen** (CAM / DENM).
   * Die Radardaten des Wheeltec MR20 und die Trigger für den 36-LED-Halo werden zu 100 % kabelgebunden über das geschirmte Picoflex-USB-Kabel (Strang 4) mit der Zentralbox synchronisiert.

---

---

## 4. Koffer-Pod Gehäusedesign & Entfall von PCBA 02

In OpenMotorBridge v10.0 ist das Kassetten-Schachtsystem vollständig abgelöst:
1. **Monolithisches Pod-Gehäuse mit Slide-in Deckel:** Das Gehäuse verbleibt fest im Koffer. Der Slide-in Deckel verriegelt selbsttätig und öffnet kontaktlos über den N52-Magneten im Smart-Keyfob (`PCBA 07`).
2. **Zwischendeckel (Dry-Flap):** Eine schützende EPDM-Blende schirmt die unten liegende Platine `PCBA 03` hermetisch gegen Tropfwasser beim Kofferöffnen ab.
3. **4-Draht-Backbone & Magnet-Abrissschnittstelle:** Die Zuleitung führt über ein 4-adriges geschirmtes Kabel (12V Bordnetz, GND, USB 2.0 D+/D-) und trennt sich an der Koffer-Teilungskante zerstörungsfrei über eine 4-Pin IP67 Magnetkupplung.

---

## 5. PCBA 03: Satelliten-Pod Interface Board (`openmotorbridge_pod_interface`)

![PCBA 03 Satelliten-Pod Platine Top 3D](../images/pcba/pcba03_pod_cartridge_3d.png)
*Abbildung 7.3a: KiCad 3D-Render der Satelliten-Pod Platine (PCBA 03, 42 x 48 mm) mit ESP32-C6 Host MCU, SW3516 30W USB-PD Ladecontroller, ES8388 Audio-Codec, getrenntem Stirnseiten-Bus & USB-C Abgang sowie rückwärtigen Intercom- und Mechatronik-Headern.*

### 5.1 Technische Platinen-Kenndaten & Architektur
* **Abmessungen:** $42{,}0 \times 48{,}0\,\text{mm}$ (4x M2.5 Befestigungsbohrungen auf $36{,}0 \times 42{,}0\,\text{mm}$ mit Schwingungsdämpfern direkt am Boden der Koffer-Pod Wanne).
  * **Länge in X ($42{,}0\,\text{mm}$):** Strikt nach vorne begrenzt (nur der Raumgewinn durch den Entfall der Kassetten-Frontblende). Der gesamte Raum hinter der Platine bleibt zu 100 % für die OEM-Cradles (Cardo Air-Mount, Sena SPIDER-Schale, OMM) und die 15–85 mm Aktuatorschiene reserviert.
  * **Breite in Y ($48{,}0\,\text{mm}$):** Nutzt die lichte Weite der Pod-Wanne ($63\,\text{mm}$) und der Aktuatorschiene ($54\,\text{mm}$) voll aus. Verdoppelt die Platinenfläche ($2016\,\text{mm}^2$ statt bisher $875\,\text{mm}^2$), schafft massive durchgehende GND-Planes und entzerrt das 4-Lagen-Routing.
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Dicke, L2 durchgehende GND-Plane, L3 Power-Plane, ENIG-Goldfinish).
* **Entfallene Altlasten (Flächenbereinigung):**
  * **DW3110 UWB Subsystem:** IC `U2`, 38.4 MHz Quarz `Y1`, U.FL Buchse `ANT_UWB` und HF-Keepouts ersatzlos gestrichen.
  * **4-Pin SWD Header (`J_PROG`):** Entfällt vollständig, da der ESP32-C6 über integrierte USB-Serial/JTAG Peripherie verfügt (Flashen & DFU direkt über USB).
  * **Blade-Slot Kontakte (`J_DC_IN` / `PAD1`, `PAD2`):** Die alten 10mm Kassetten-Messerkontakte entfallen.
* **4-Pin Bus-Eingang (`J_BUS` / 4-Pin JST-GH 1.25mm SMD):**
  * Sitzt an der **linken Stirnkante unten** (exakt an der Position des früheren Blade-Slots).
  * Direkter, geradliniger Leitungsweg (< 15 mm) zur Kofferwandtülle ohne Biegeschleifen.
  * Führt die 4 Adern des Strangs von der Zentralbox: `VCC_BUS` (+12V...+20V Bordnetz/PD, abgesichert 30W), `GND`, `USB_D+`, `USB_D-`.
* **Integrierte 30W USB-PD Ladezone & Gehäusebuchsen-Abgang (`J_USB_OUT` / 4-Pin JST-GH 1.25mm SMD):**
  * **Controller:** Ismartware `SW3516` oder Injoinic `IP6538` (QFN-32, $5 \times 5\,\text{mm}$) synchroner Step-Down Konverter mit integriertem USB-PD 3.0 / PPS / QC4+ Protokollcontroller und $7 \times 7\,\text{mm}$ geschirmter Speicherinduktivität ($10\,\mu\text{H}$).
  * **Header `J_USB_OUT`:** Sitzt an der **linken Stirnkante oben**.
* **Stirnseitige interne Anschlüsse & Gehäuse-Buchsenanordnung:**
  * **Anordnung an der kurzen Gehäusestirnwand (Port A & Port B):** Beide Buchsen sitzen horizontal exakt mittig ($Y = 35{,}0\,\text{mm}$) und sind vertikal übereinander gestapelt:
    * **Port A (Bus-Buchse):** Oberhalb der Mitte bei $Z = 26{,}5\,\text{mm}$ (mit M8-Schutzkragen bzw. dichter Kabelverschraubung zur Zentralbox).
    * **Port B (USB-C Ladedose):** Unterhalb der Mitte bei $Z = 11{,}5\,\text{mm}$ (mit $7\,\text{mm}$ tief eingelassener Steckertasche für bündige wasserdichte TPU-Schutzkappe).
  * **Interne Silikon-Kabelpeitschen:** Die Verbindung von der Platine zu den Gehäusebuchsen erfolgt über kurze, hochflexible Silikonkabel von den stirnseitigen Headern `J_BUS` bzw. `J_USB_OUT`. Sämtliche Einsteck-, Rüttel- und Hebelkräfte werden zu 100 % vom stabilen PA12-Monocoque abgefangen – die Platine bleibt völlig zug- und schwingungsfrei!
  * **100 % Symmetriegarantie (Links = Rechts):** Da beide Koffer-Pods an der Stirnseite identisch orientiert sind, bleibt die USB-C Ladedose an beiden Fahrzeugseiten ergonomisch gleich zugänglich.
* **Rückwärtige Schnittstellen (Geräteseite, nach rechts in die Gerätekammer):**
  * **`J_AUDIO_PWR` (8-Pin JST-SH 1.0mm, oben rechts):** Direkte Verbindung zur OEM-Kabelpeitsche des Intercoms (Sena, Cardo, OMM, Midland).
  * **`J_ACT` (8-Pin JST-SH 1.0mm, unten rechts):** Direkte Verbindung zu bis zu 4 Aktuatorkanälen (Hubmagnete / Servos auf der universellen Aktuatorschiene `012_universal_actuator_slide_bracket.scad`).
  * **Vorteil:** Durch den räumlichen Abstand zwischen Audio (oben) und Aktorik (unten) streuen Schaltimpulse der Magnete nicht in die analogen Audioleitungen ein. Beide Kabelstränge laufen parallel nach hinten ab – null Kabelkreuzungen über der Platine!
* **Kommunikations-, Leistungs- & Audio-ICs:**
  * `U1`: Espressif `ESP32-C6-MINI-1U` RISC-V MCU zur Ladeüberwachung, Codec-Steuerung, Aktorik und USB-Audio-Brücke.
  * `U_PD`: Ismartware `SW3516` (QFN-32, $5 \times 5\,\text{mm}$) synchroner 30W USB-PD 3.0 / PPS / QC4+ Step-Down Wandler mit $7 \times 7\,\text{mm}$ geschirmter Speicherinduktivität `L_PD` ($10\,\mu\text{H}$) und 1210er Festpolymer-Filterkondensatoren.
  * `U3`: Everest Semi `ES8388` 24-Bit / 48 kHz Low-Noise Audio-Codec.
  * `U4`: TI `TS5A3159DBVR` Analog/Digital-Audio-Umschalter für automatische Erkennung analoger OEM-Headsets vs. digitaler OMM-Module via Pin 6 (`OMM_DETECT`).
  * `Q1..Q4`: 4x N-Kanal Power-MOSFETs (`AO3400A`, 30V/4A) mit 4x Freilaufdioden (`1N4148WS`, D1..D4) für 4 unabhängige Schaltkanäle.
  * `F1`: 1812 SMD Polyfuse (PPTC) zur Absicherung der 5V Aktorik- und Peripherieversorgung (`VCC_5V_PROT`).

### 5.2 Pinbelegung des 4-Pin Bus-Eingangs (`J_BUS` / 4-Pin JST-GH 1.25mm)

| Pin | Signalname | Signalart | Funktion & Spezifikation (internes Kabel zu Port A) |
| :---: | :--- | :---: | :--- |
| **1** | **`VCC_BUS`** | Power In (+12V...+20V) | Bordnetz- / PD-Speisung von Zentralbox (AWG20, abgesichert 30W) |
| **2** | **`GND`** | Power Return | Leistungs- und Signalmasse |
| **3** | **`USB_DP`** | High-Speed Data | USB 2.0 Datenleitung D+ zur Zentralbox (ESP32-S3 Host) |
| **4** | **`USB_DM`** | High-Speed Data | USB 2.0 Datenleitung D- zur Zentralbox (ESP32-S3 Host) |
| **MP** | **`GND`** | Schirmung | Rastlaschen des JST-GH Steckers auf GND-Plane gelegt |

### 5.3 Pinbelegung des internen 30W USB-C Gehäuseabgangs (`J_USB_OUT` / 4-Pin JST-GH 1.25mm)

| Pin | Signalname | Signalart | Funktion: Internes Silikonkabel zur Gehäusewand (Port B) |
| :---: | :--- | :---: | :--- |
| **1** | **`VBUS_30W`** | Power Out | Geregelte 5V/9V/12V/15V/20V USB-PD Ladespannung (bis 30W) |
| **2** | **`GND`** | Power Return | Rückstrom Ladeleistung (AWG20 Silikonader) |
| **3** | **`CC1`** | PD Config In/Out | Configuration Channel 1 für USB-PD 3.0 / PPS Aushandlung |
| **4** | **`CC2`** | PD Config In/Out | Configuration Channel 2 für USB-PD 3.0 / PPS Aushandlung |
| **MP** | **`GND`** | Schirmung | Rastlaschen des JST-GH Steckers auf GND-Plane |

### 5.4 Pinbelegung des Audio-Power-Headers (`J_AUDIO_PWR` / 8-Pin JST-SH 1.0mm)

| Pin | Signalname | Richtung | Funktion: Analog-Intercom (Sena / Cardo / Midland) | Funktion: Digital-OMM (PCBA 09 / PCBA 10) |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **`GND`** | Power Return | **Leistungs- und Audiorückstrom:** Gemeinsame niederohmige Masse ($0{,}2\dots 0{,}6\,\text{A}$) | **Leistungs- und HF-Masse:** Rückstrom Lader & HF-Endstufe |
| **2** | **`VCC_5V_PROT`** | Power Out | Geregelte, polyfuse-geschützte +5V Speisung für Headset-Akku/Lader | Geregelte, geschützte +5V Speisung für OMM BQ24075 PMIC |
| **3** | **`GND`** | System GND | Referenz- und Schirmmasse | Referenz- und Koax-Schirmung |
| **4** | **`AUDIO_IN_L`** | Audio In $\leftarrow$ | Line-Out Lautsprecher Links vom Headset zum ES8388 ADC | Nicht belegt (N/C) |
| **5** | **`AUDIO_IN_R`** | Audio In $\leftarrow$ | Line-Out Lautsprecher Rechts vom Headset zum ES8388 ADC | Nicht belegt (N/C) |
| **6** | **`OMM_DETECT`** | Control In $\leftarrow$ | **GND-Brücke im Kabelbaum (0V):** Hält `U4` in Ruhestellung (NC) | **Offen / N/C:** `R9` zieht auf HIGH ($3{,}3\,\text{V}$) $\rightarrow$ schaltet `U4` auf Digital-USB (NO) |
| **7** | **`AUDIO_IO_P`** | Dual-Mode I/O | **Analog `VOICE_OUT` (via U4 NC):** Sprache vom ES8388 DAC $\rightarrow$ OEM Mic | **Digital `USB_DP` (via U4 NO):** Nativer digitaler USB-Audio-Datenstrom D+ |
| **8** | **`PTT_BTN`** | Digital In $\leftarrow$ | **Physische PTT-Taste:** Tastereingang direkt auf ESP32-C6 GPIO Pin 7 | **PTT-Steuerung / Digital-Status:** Tastung gegen GND |
| **MP** | **`GND`** | Schirmung | Beidseitige SMD-Montagelaschen des JST-SH Steckers auf GND-Plane | Beidseitige SMD-Montagelaschen des JST-SH Steckers auf GND-Plane |

### 5.5 Pinbelegung des Mechatronik-Aktuator-Headers (`J_ACT` / 8-Pin JST-SH 1.0mm)

| Pin | Signalname | Signalart | Funktion & Schutz |
| :---: | :--- | :---: | :--- |
| **1** | **`GND`** | Power Return | Leistungs-Masse für Aktorikstufe |
| **2** | **`GND`** | Power Return | Leistungs-Masse für Aktorikstufe |
| **3** | **`ACT_4`** | Open-Drain Out | Geschaltete Spulenmasse Aktuator 4 (via AO3400A Q4 / Freilaufdiode D4) |
| **4** | **`ACT_3`** | Open-Drain Out | Geschaltete Spulenmasse Aktuator 3 (via AO3400A Q3 / Freilaufdiode D3) |
| **5** | **`ACT_2`** | Open-Drain Out | Geschaltete Spulenmasse Aktuator 2 (via AO3400A Q2 / Freilaufdiode D2) |
| **6** | **`ACT_1`** | Open-Drain Out | Geschaltete Spulenmasse Aktuator 1 (via AO3400A Q1 / Freilaufdiode D1) |
| **7** | **`VCC_5V_PROT`** | Power Out (+5V) | Speisung für Aktuatorspulen (polyfuse-abgesichert via F1) |
| **8** | **`VCC_5V_PROT`** | Power Out (+5V) | Speisung für Aktuatorspulen (polyfuse-abgesichert via F1) |
| **MP** | **`GND`** | Schirmung | SMD-Montagelaschen auf GND-Plane |

---

## 6. PCBA 04: Heck-Pod 3 (Ersatzlos entfallen)

Die Heckplatine `PCBA 04` und das zugehörige Heckgehäuse Pod 3 sind vollständig gestrichen:
* Der Semtech SX1262 LoRa-Transceiver arbeitet direkt auf der Zentralbox (`PCBA 01`).
* Das u-blox SAM-M10Q GNSS-Modul arbeitet im modularen Sensor-Puck des Front-Knotens (`PCBA 05`).

---

## 7. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`)

![PCBA 05 Universal Front-Knoten Top 3D](../images/pcba/pcba05_front_node_3d.png)
*Abbildung 7.5a: KiCad 3D-Render des Universal Front-Knotens Top (PCBA 05, 82 x 50 mm) mit ESP32-S3-WROOM-1U, modularer Sensor-Puck Schnittstelle, Knowles MEMS Akustiksensor, Southchip SC8721/SC8102 60W USB-PD und Anschlüssen für symmetrische Spiegel-Pods & Cockpit Speaker Corner Displays.*

### 7.1 Technische Platinen-Kenndaten & 60W Power Engine
* **Abmessungen:** $82{,}0 \times 50{,}0\,\text{mm}$ (Gehäuseaußenmaß $98 \times 68 \times 25\,\text{mm}$ im geschlossenen IP68-Monocoque-Gehäuse am Lenker-Riser).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$, ENIG-Goldfinish).
* **Automotive-Backbone Anbindung (Strang 1):** Geschirmtes 4-Ader-Kabel von der Zentralbox (12V-20V Bordnetz, GND, USB 2.0 D+/D-), verlegt durch den Harley-Kabelkanal unter der Tankkonsole (**ZERO Tank-Demontage!**).
* **60W USB-PD Power-Engine (`U8`, Southchip SC8721 / SC8102 Synchronous Buck-Boost):**
  * Versorgt das Gesamtsystem an der Front verlässlich ohne Brownouts:
    * Driver Smartphone Fast-Charging: bis 27W USB-PD (9V/3A) am Lenker oder über den Handschuhfach-Hub.
    * Dediziertes Motorrad-Navi (Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride): 15W (12V/1.25A bzw. 5V/3A) direkt an `J10`. **Power-Only:** Reine Stromversorgung ohne USB-Host Datenleitungen (`D+`, `D-`), damit das Navi sofort in den Routenbetrieb startet und nicht in den PC-Massenspeicher-Modus schaltet.
    * Action-Cam Dauerstrom: 10W (5V/2A) wetterfeste USB-C Zuleitung direkt am Front-Node (`J8`) für GoPro / Insta360. **Power-Only / BC 1.2 DCP:** D+/D- kurzgeschlossen ($R < 200\,\Omega$), null USB2514B Host-Verbindung, verhindert PC-/Webcam-Modus und vermeidet Kabelumwege ins Handschuhfach.
    * Dual Cockpit OLED Displays: 2W für die beiden Speaker Corner Pods in den Lautsprechergittern.
    * ESP32-S3 Host-MCU, Sensorik & Audio-AGC: 3,5W.
    * Gesamt-Peaklast ca. 57,5W – perfekt, verlustarm und thermisch dauerlauffest aus dem 60W-Standardbudget bedient (20V / 3A).
* **Modularer Sensor-Puck ("Körbchen") Schnittstelle (`J_SENSOR_EXT` / 6-Pin JST-GH):**
  * Führt I2C (`SCL`, `SDA`, `3V3`, `GND`) und I2S (`I2S_SD`, `I2S_WS`) zum schnappbaren Sensor-Puck ([`sensor_puck_environmental.scad`](../../hardware/cad/scad/04_front_node/parts/sensor_puck_environmental.scad)).
  * Beherbergt u-blox SAM-M10Q Multi-GNSS, TI TMP117 Präzisionsthermometer, OPT3001 Umgebungslichtsensor und Knowles I2S MEMS.
  * Am Motorrad direkt oben auf den Front-Node gerastet; im Auto/Van per 1,5m Verlängerungskabel absetzbar an der Windschutzscheibe.
* **Peripherie-Ausgänge:**
  * 2x 4-polige JST-GH Buchsen (`J_POD_L` und `J_POD_R`) zu den symmetrischen Under-Perch Spiegel-Pods (`PCBA 05B`).
  * 2x 4-polige JST-SH Buchsen (`J_DISP_L` und `J_DISP_R`) zu den beiden Cockpit Speaker Corner Pod Displays (`cockpit_speaker_corner_pod.scad`).
  * SP Connect / QuadLock Ladeanschluss am Lenker (bis 27W) & Garmin Zūmo XT2 Power-Only Navi-Abgriff (`J10`, 15W).
  * Direkter 10W Action-Cam Power-Only Port (`J8`, 2-Pin JST-PH / BC 1.2 DCP pigtail lead für GoPro/Insta360 am Cockpit).
  * 4-Port Handschuhfach Media & Power-Injection Hub Anbindung ([`glovebox_power_injection_hub.scad`](../../hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad)): Kombiniertes Power- & High-Speed-USB-Kabel. Liefert saubere Power-Injection (30W Phone, 10W Dongle, freier Media-Port) und verbindet den USB-Controller mit Port 4 zur OEM-Headunit für die **Harley Headset-Emulation via USB** (MFi-Headset / USB Audio Class composite accessory, native Apple CarPlay Freischaltung und verlustfreies Helmmikrofon-Audio).

---

### 7.2 PCBA 05B: Symmetrische Under-Perch Spiegel-Pod Platine (`openmotorbridge_under_perch_pod`)

![PCBA 05B Spiegel-Pod Platine 3D](../images/pcba/pcba05b_cockpit_breakout_3d.png)
*Abbildung 7.5c: KiCad 3D-Render der symmetrischen Under-Perch Spiegel-Pod Platine (PCBA 05B, 32 x 14 mm). Zwei baugleiche Platinen arbeiten links und rechts unter den Spiegelschrauben.*

#### 7.2.1 Technische Platinen-Kenndaten & Bestückung
* **Abmessungen:** $32{,}0 	imes 14{,}0\,	ext{mm}$, 2 Lagen FR4 High-TG150 ($1{,}6\,	ext{mm}$, ENIG-Goldfinish).
* **Bauform:** 100 % SMD, Formfaktor passgenau für [`under_perch_mirror_pod.scad`](../../hardware/cad/scad/05_accessories/under_perch_mirror_pod.scad).
* **Bestückung:**
  * **`LED1` (Bernstein BSD Totwinkel-Warn-LED):** Hochleistungs-SMD-LED (590 nm Amber, 120° Abstrahlwinkel), strahlt durch einen optischen Diffusortrichter im 38°-Winkel blendfrei in das jeweilige Spiegelglas.
  * **`SW1` (Taktiler Daumen-Mikrotaster):** IP67-versiegelter Kurzhub-Mikrotaster mit spürbarem 300g Druckpunkt für zuverlässige Bedienung mit Winterhandschuhen.
  * **Entprellung & ESD-Schutz:** 100 nF RC-Glied zur Hardware-Entprellung und bidirektionale TVS-Diode (`D1`, PESD5V0S1BL) gegen elektrostatische Entladungen.
  * **Steckverbinder (`J1`):** 4-polige JST-GH SMD Buchse (`SM04B-GHS-TB`, 1.25 mm Raster) mit formschlüssiger Rastverriegelung.

#### 7.2.2 Pinbelegung des Spiegel-Pod Headers (`J1` / 4-Pin JST-GH)

| Pin | Signalname | Signalart | Funktion & Pegel |
| :---: | :--- | :---: | :--- |
| **1** | **`VCC_LED`** | Power In (+5V / +12V) | Geschützte Anodenspeisung für Totwinkel-LED |
| **2** | **`BSD_LED_N`** | Kathode (Low-Side) | Geschaltete Masse vom Front-Node MOSFET (Radar-Warnung) |
| **3** | **`BTN_SIG_N`** | Digital In (Active-Low)| Tastersignal gegen Masse, entprellt mit 100 nF RC-Glied |
| **4** | **`GND`** | Masse (0V) | Gemeinsame Signal- und Rückmasse |

#### 7.2.3 100 % Software-Defined Tasterbelegung via PWA-Dashboard
Beide Taster sind hardwareseitig identisch und können über das PWA-Dashboard völlig frei auf 5 Gesten-Events gemappt werden (`SHORT_CLICK`, `DOUBLE_CLICK`, `TRIPLE_CLICK`, `LONG_PRESS`, `HOLD_GATE`):
* **Werks-Default Links:** `HOLD_GATE` $ightarrow$ PTT Intercom; `TRIPLE_CLICK` $ightarrow$ Siri/Google Assistant; `DOUBLE_CLICK` $ightarrow$ Mesh-Kanalwechsel.
* **Werks-Default Rechts:** `SHORT_CLICK` $ightarrow$ Action-Cam Highlight-Tag (Insta360/GoPro BLE); `LONG_PRESS` $ightarrow$ Videoaufnahme Start/Stop; 3s Halten $ightarrow$ 868 MHz LoRa Notfall-SOS.
* **Frei belegbare Aktionen:** 1-Klick Hazard Pin Drop (Waze/OpenTrafficMap), Radar-Stummschaltung 30s, Garagentoröffner (Shelly/Home Assistant), Zusatzscheinwerfer, Heizgriffe.

---

## 8. PCBA 06: MagSafe Frame Dock (Ersatzlos entfallen)

Die separate Platine `PCBA 06` ist in v9.6 **vollständig und ersatzlos entfallen**:
* Da über die fahrzeugseitige Koffer-Trennstelle ausschließlich 2-Draht DC-Gleichspannung geführt wird, kommt anstelle einer proprietären Leiterplatte ein **industrieller 2-Pin Magnet-Pogo-Steckverbinder (IP68 COTS)** zum Einsatz.
* Kurzschlussschutz und Überlastbegrenzung erfolgen zentral auf `PCBA 01` durch die jeweiligen **TI TPS25921 eFuses**.

---

## 9. PCBA 07: 2-in-1 LoRa Smart-Keyfob (`openmotorbridge_smart_keyfob`)

![PCBA 07 2-in-1 LoRa Smart-Keyfob](../images/pcba/pcba07_smart_keyfob_3d.png)

*Abbildung 7.7: 3D-Render der ultrakompakten PCBA 07 Trägerplatine (38,0 x 19,0 mm, 2 Lagen) mit Nordic nRF52840 SoC, Semtech SX1262 LoRa Transceiver, TI DRV2605L Haptik-Treiber, BQ51003 Qi-Ladecontroller und 2-Pin JST-ACH Induktions-Spulenanschluss.*

### 9.1 Technische Platinen-Kenndaten & Lötfreie Qi-Montage
* **Abmessungen:** $38{,}0 \times 19{,}0 \times 1{,}0\,\text{mm}$ (2-Lagen FR-4, ENIG-Goldfinish).
* **Kern-Chips:**
  * Nordic `nRF52840` SoC (Bluetooth Low Energy 5.4, ARM Cortex-M4F @ 64 MHz, Hardware-Crypto).  
    *(BLE gewährleistet einen extrem sparsamen Ruhestrom von $< 25\,\mu\text{A}$, sodass die 200-mAh-Zelle monatelang betriebsbereit bleibt).*
  * Semtech `SX1262` LoRa Transceiver (868.5 MHz Kanal 3, empfängt Alarme bis zu 4,5 km Reichweite).
  * Texas Instruments `DRV2605L` Haptiktreiber für Vybronics 10x3.6mm LRA Linearmotor.
  * Texas Instruments `BQ51003` Qi Wireless Power Receiver Controller.
* **100 % Lötfreie Induktionsspulen- & Akku-Montage (`J_QI` & `J_BAT`):**
  * Die 24–28 mm Qi-Empfängerspule wird über einen ultrakompakten **2-poligen JST-ACH SMD-Header (`J_QI`)** vibrationsfest angesteckt.
  * Der 180–200 mAh LiPo-Pouch-Akku (mit integrierter PCM-Schutzschaltung) wird über einen baugleichen **2-poligen JST-ACH SMD-Header (`J_BAT`)** angesteckt (1,2 mm Raster, nur 1,4 mm Bauhöhe).
  * Beim Zusammenbau des Smart-Keyfobs sind somit keinerlei manuelle Lötarbeiten erforderlich (100 % lötfreies IKEA-Montageprinzip).

### 9.2 Vollständige Pinbelegung des Nordic nRF52840 SoC (PCBA 07 `U1`)

| SoC-Pad | Signalname | Signal-Typ | Funktion / Hardware-Verbindung |
| :---: | :--- | :---: | :--- |
| **A8** | `BLE_ANT_50R` | RF 2.4G | 50 Ohm Leitung zur Johanson 2450AT Keramik-Chipantenne (`ANT1`) |
| **A12 / A14** | `XTAL1` / `XTAL2` | Analog | 32.000 MHz HF-Präzisionsquarz |
| **F23 / H23** | `RTC1` / `RTC2` | Analog | 32.768 kHz Uhrenquarz (Sleep-Timer & Real-Time Clock) |
| **H2 / AC24** | `SWDCLK` / `SWDIO` | Digital In/Out | 4-Pin SWD Programmier-Header `J_SWD` |
| **B1** | `VCC_3V3` | Power | +3.3V Systemspannung (BQ25100 / LDO) |
| **B9, B11, EP** | `GND` | Power | System- und HF-Masse |
| **C1** | `LORA_SCK` | Digital Out | SPI Serial Clock zu Semtech SX1262 (`U2`) |
| **R1** | `LORA_NSS` | Digital Out | SPI Chip-Select (Active-Low) zu SX1262 (`U2`) |
| **T2** | `LORA_MOSI` | Digital Out | SPI Master-Out Slave-In zu SX1262 (`U2`) |
| **U1** | `LORA_MISO` | Digital In | SPI Master-In Slave-Out von SX1262 (`U2`) |
| **W1** | `LORA_BUSY` | Digital In | Busy-Statusleitung von SX1262 (`U2`) |
| **D2** | `LORA_DIO1` | Digital In | IRQ-Leitung von SX1262 (Empfang 0xFE Alarmpaket) |
| **Y2** | `LORA_RESET` | Digital Out | Hardware-Reset zu SX1262 (`U2`) |
| **F2** | `BUZZER_PWM` | Digital Out | PWM-Ansteuerung (2.7 kHz / 4.0 kHz) für Murata SMD Piezo-Buzzer (`BZ1`) |
| **G1** | `BTN_ARM_N` | Digital In | Scharfschalt-Taster `SW1` (Arm/Disarm, Active-Low) |
| **J1** | `BTN_SOS_N` | Digital In | Notfall-Paniktaster `SW2` (SOS/Alarm, Active-Low) |
| **K2** | `CHG_STAT` | Digital In | Ladezustandsanzeige von TI BQ25100 (Low = Lädt, High = Voll) |
| **L1** | `LED_DATA` | Digital Out | Datenleitung für WS2812B-2020 RGB Status-LED (`D1`) |
| **M2** | `DRV_EN` | Digital Out | Hardware-Enable für TI DRV2605L Haptiktreiber (`U3`) |
| **N1** | `I2C_SDA` | Open-Drain | I2C Datenleitung zu DRV2605L Haptiktreiber (`U3`) |
| **P2** | `I2C_SCL` | Open-Drain | I2C Taktleitung zu DRV2605L Haptiktreiber (`U3`) |

---

## 10. PCBA 08: 77 GHz mmWave Radar Sub-MCU & Warnflügel (`openmotorbridge_radar_submcu`)

![PCBA 08 Radar 2.0 Sub-MCU & Warnflügel 3D](../images/pcba/pcba08_radar_submcu_3d.png)
*Abbildung 7.8: 3D CAD-Ansicht der gerouteten PCBA 08 (115 x 65 mm) mit mittigem 61 x 51 mm Radarausschnitt für das Wheeltec MR20 Horn-Array, 36x WS2812B Warnflügel-LEDs, ESP32-C5 Dual-Band Sub-MCU und 5.9 GHz V2X Keramik-Patchantenne.*

### 10.1 Technische Platinen-Kenndaten & Kabel-Anbindung
* **Abmessungen:** $115{,}0 	imes 65{,}0 	imes 1{,}6\,	ext{mm}$ (2 Lagen FR-4 High-TG150, ENIG-Goldfinish).
* **Zentraler Radarausschnitt:** $61{,}0 	imes 51{,}0\,	ext{mm}$ für das Wheeltec MR20 77-GHz-Sensormodul.
* **Kabelanbindung:** Die Verbindung zur Zentralbox erfolgt über Strang 4 des 16-Pin Automotive Kabelbaums (12V geschaltete Bordnetzspeisung) und eine geschirmte 2-Draht UART-Verbindung zur direkten Ziel- und Telemetrieübertragung (115.200 Baud).
* **5.9 GHz V2X Keramik-Patchantenne:** Autarke Antennenkammer auf der linken Gehäuseflanke für direkte C-V2X / ITS-G5 Kommunikation.

---

## 11. PCBA 09: OMM 2.4 GHz Autonomes Intercom-Modul (`openmotorbridge_omm_ucs`)

Die Platine **`PCBA 09`** ist die universelle Open-Source-Hardware für das OpenMotorMesh (OMM) 2.4 GHz Intercom-System. Sie erfüllt die mechanischen und elektrischen Spezifikationen für den autonomen Betrieb in standardisierten ECE 22.06 UCS-Helmmulden sowie als HF-Einsatz im Kassetten-Schlitten (`PCBA 03`).

![PCBA 09 OMM 2.4 GHz Intercom & UCS Modul Top 3D](../images/pcba/pcba09_omm_intercom_top_3d.png)
*Abbildung 7.9a: PCBA 09 Top 3D (Aktuelles Routing & Placement) – ESP32-C6 Host-MCU (U1), ES8388 Audio-Codec (U4), BQ24075 PMIC (U2), ME6211 3.3V LDO (U3), IP67 USB-C (J1) und 4-Tasten-Reihe.*

![PCBA 09 OMM 2.4 GHz Intercom & UCS Modul Bottom 3D (Dual-Engine)](../images/pcba/pcba09_omm_intercom_bottom_3d.png)
*Abbildung 7.9b: PCBA 09 Bottom 3D (Dual-Engine OMB Lite) – Dedizierter ESP32-PICO-V3-02 Bluetooth Classic/BLE Co-Prozessor (U5) und Johanson 2450AT Chipantenne (ANT1) zur CoEx-freien Funkentkopplung.*

### 11.1 Technische Platinen-Kenndaten & Lagenaufbau
* **Abmessungen:** $60{,}0 \times 30{,}0 \times 1{,}0\,\text{mm}$ ($R = 2{,}5\,\text{mm}$ Kantenradius).
* **Lagenaufbau:** 2-Lagen FR-4 High-TG150, $1{,}0\,\text{mm}$ Materialstärke, $35\,\mu\text{m}$ Cu (1 oz), ENIG-Goldfinish (Electroless Nickel Immersion Gold).
* **Befestigung:** 4x M2-Montagelöcher ($\varnothing 2{,}2\,\text{mm}$) mit $52{,}0 \times 22{,}0\,\text{mm}$ Rastermaß für formschlüssige DIN 934 M2 Mutterntaschen im Gehäuse.

### 11.2 Bestückung & Schaltkreis-Architektur

1. **Host-Mikrocontroller (`U1`):**
   * **Espressif ESP32-C6-MINI-1U** (32-Bit RISC-V Single-Core @ 160 MHz, 512 kB SRAM, 4 MB Quad-SPI Flash, integrierte U.FL-Goldbuchse).
   * Unterstützt 2.4 GHz Wi-Fi 6 ($802.11\text{ax}$), IEEE 802.15.4 (deterministischer TDMA Mesh-Stack) und Bluetooth 5.3 LE / LE Audio LC3.
2. **Power-Management & Lade-IC (`U2`):**
   * **Texas Instruments BQ24075RGTR** (QFN-16 3x3mm) mit Dynamic Power Path Management (DPPM).
   * Unterbrechungsfreie Umschaltung zwischen USB-C 5V-Speisung (Bordnetz über Kassetten-Schlitten oder Powerbank) und dem internen 600-mAh-LiPo-Akku in $< 10\,\mu\text{s}$ ohne MCU-Reboot. Der interne Akku dient im Kassettenbetrieb als unterbrechungsfreie Stromversorgung (USV).
   * Einstellbarer Ladestrom ($500\,\text{mA}$), JEITA-konforme Temperaturüberwachung über NTC-Thermistor ($10\,\text{k}\Omega$).
3. **Audio-Frontend Stereo Codec (`U4`):**
   * **Everest Semi ES8388** (QFN-28 4x4mm): Ultra-Low-Power Stereo Audio Codec mit 24-Bit / 96 kHz I2S-Interface.
   * Getrennte linke und rechte Kopfhörer-Treiber ($2\times 45\,\text{mW}$ @ $16\,\Omega$ / $25\,\text{mW}$ @ $32\,\Omega$) für echten Stereo-Klang (A2DP-Musik, räumliche Navigationshinweise, LE Audio).
   * Rauscharmer Differenz-Mikrofon-Vorverstärker ($+0\dots +30\,\text{dB}$ Gain) mit programmierbarer interner `MICBIAS`-Erzeugung ($2{,}0\dots 2{,}8\,\text{V}$) für Schwanenhals- und Klebemikrofone.
4. **2.4-GHz-HF-Antennensystem & Dual-Engine:**
   * **Host MCU (`U1`):** Nutzt direkt den werkseitig integrierten U.FL-Goldport auf dem `ESP32-C6-MINI-1U` Modul. Über ein kurzes $50\,\text{mm}$ RG-178/1.13mm Mikro-Koaxialpigtail wird das Signal zur wasserdichten IP67 SMA-Bulkhead-Durchführung an der Gehäusestirnseite geführt. (Die frühere redundante Zweitbuchse auf der Leiterplatte wurde ersatzlos gelöscht).
   * **Helm-Default:** Im Helmbetrieb wird direkt die ultrakompakte $38\,\text{mm}$ kurze 2.4 GHz Rubber-Duck Stummelantenne aufgeschraubt (Rundstrahl-Helix, $+2{,}0\dots +2{,}5\,\text{dBi}$, null Helmbüffeln). Im Kassetten-Betrieb am Motorrad verbindet ein Koaxialkabel die SMA-Buchse mit einer fahrzeugfesten Außenantenne.
   * **Bluetooth Co-Prozessor (`U5`):** Der `ESP32-PICO-V3-02` arbeitet auf eine eigene Johanson 2450AT Keramik-Chipantenne (`ANT1`, SMD 3216) für Nahfeld-Kopplungen zum Smartphone oder Cockpit-Display.
5. **Bedienung & Sensorik:**
   * 4x taktile IP67-Mikrotaster (`SW1` bis `SW4`, C&K KMT0 / Alps SKRK) auf `F.Cu`.
   * 1x RGB Status-LED (`D1`, WS2812B-2020) zur Einkopplung in den Gehäuse-Lichtleiter.
6. **Schnittstellen & Steckverbinder:**
   * `J1`: Wasserdichte IP67 USB-C Buchse (16-Pin) bündig an der Stirnkante mit USBLC6-2SC6 TVS-ESD-Schutzarray (Laden unterwegs via Powerbank/Front-Node, WebUSB DFU Flashing, Kassetten-Einschubkontakt).
   * `J_HELMET`: 6-Pin JST-SH 1.0mm SMD Vertikal-Header (`BM06B-SRSS-TB`) auf `B.Cu` ($X=127{,}05, Y=99{,}70\,\text{mm}$ in KiCad, vertikaler Steckanschluss für zugentlastete Kabelführung direkt in die Helmmulde) im hinteren Gehäuseabteil gegenüber USB-C. Führt reines, brummfreies Audio ins Helminnere.
   * `BAT1`: 2-polige JST-SH Micro-Buchse (`BM02B-SRSS-TB` Vertikal) auf `B.Cu` ($X=79{,}40, Y=112{,}00\,\text{mm}$) zum 1S LiPo Pouch-Akku (600 mAh mit integriertem PCM).

### 11.3 Vollständige GPIO-Pinbelegung (ESP32-C6-MINI-1U)

| Modul-Pad | ESP32-C6 GPIO | Netzname | Signal-Typ | Funktion / Hardware-Verbindung |
| :---: | :---: | :--- | :--- | :--- |
| **Pad 8** | **`GPIO 2`** | `BTN_PWR` | Digital In (Pullup) | SW1 (Power / MFB Taster, Low-aktiv, Boot-Pin) |
| **Pad 9** | **`GPIO 3`** | `BTN_MESH` | Digital In (Pullup) | SW2 (Mesh / Group Umschaltung, Low-aktiv) |
| **Pad 4** | **`GPIO 4`** | `BTN_VOL_UP` | Digital In (Pullup) | SW3 (Lautstärke +, Kanalwahl +, Low-aktiv) |
| **Pad 5** | **`GPIO 5`** | `BTN_VOL_DOWN` | Digital In (Pullup) | SW4 (Lautstärke -, Kanalwahl -, Low-aktiv) |
| **Pad 6** | **`GPIO 6`** | `WS2812_DATA` | Digital Out | D1 (WS2812B-2020 RGB Statusanzeige & Lichtleiter) |
| **Pad 7** | **`GPIO 7`** | `CHG_STAT` | Digital In (Pullup) | BQ24075 /STAT Ladezustandsanzeige (Low-aktiv) |
| **Pad 10** | **`GPIO 8`** | `I2C_SDA` | Open-Drain | ES8388 Register Control SDA (4.7k Pullup) |
| **Pad 11** | **`GPIO 9`** | `I2C_SCL` | Open-Drain | ES8388 Register Control SCL (4.7k Pullup) |
| **Pad 3** | **`GPIO 2 / PTT`**| `PTT_IO` | Digital In (Pullup) | Hardware-PTT-Eingang von J_HELMET Pin 6 / Lenkertaster |
| **Pad 21** | **`GPIO 19`** | `I2S_MCLK` | Digital Out | ES8388 Master Clock (12.288 MHz) |
| **Pad 22** | **`GPIO 20`** | `I2S_BCLK` | Digital Out | ES8388 Bit Clock (1.536 MHz) |
| **Pad 23** | **`GPIO 21`** | `I2S_WS` | Digital Out | ES8388 Frame Sync / Word Select (48 kHz) |
| **Pad 24** | **`GPIO 22`** | `I2S_DOUT` | Digital Out | ES8388 DAC Data Out (Stereo-Lautsprecher L/R) |
| **Pad 25** | **`GPIO 23`** | `I2S_DIN` | Digital In | ES8388 ADC Data In (Mikrofon) |
| **U.FL** | **RF 2.4G** | `RF_ANT` | 50 Ohm Koaxial | ESP32-C6 integrierte U.FL-Buchse -> Koax-Pigtail -> SMA-Durchführung |

### 11.4 Belegung des 16-Pin Multi-Use USB-C Steckverbinders (`J1`)

Der stirnseitige USB-C Port `J1` (`TYPE-C-31-M-12_IP67`) dient als universelle Schnittstelle für **Laden (5V Bordnetz / Powerbank)**, **WebUSB/DFU-Flashing** und die **digitale USB-Audio-Anbindung** im Kassetten-Schlitten (`PCBA 03`):

| USB-C Pins | Netzname | Signal-Typ | Funktion & Kassetten-Verbindung (`J_AUDIO_PWR`) |
| :---: | :--- | :--- | :--- |
| **A1, B12, A12, B1, SH** | `GND` / `PGND` | Power Ground | Pin 1 Kassetten-Header `J_AUDIO_PWR` & Schirmung: Führt Lade- & Betriebs-Rückstrom |
| **A4, B9, A9, B4** | `VBUS_5V` | Power In (+5V) | Pin 2 Kassetten-Header `VCC_5V_PROT` & USB-Ladekabel: 5V Speisung & BQ24075 USV-Ladung |
| **A6, B6 (`DP1`, `DP2`)** | `USB_DP` | USB 2.0 PHY | Pin 7 Kassetten-Header `AUDIO_IO_P` $\rightarrow$ ESP32-C6 GPIO 13 (via TVS `D2`): **Digital-Audio USB D+ & WebUSB** |
| **A7, B7 (`DN1`, `DN2`)** | `USB_DN` | USB 2.0 PHY | Pin 8 Kassetten-Header `PTT_USB_N` $\rightarrow$ ESP32-C6 GPIO 12 (via TVS `D2`): **Digital-Audio USB D- & WebUSB** |
| **A5 (`CC1`)** | `CC1` | USB-C UFP | $5{,}1\,\text{k}\Omega$ Pull-Down nach GND (UFP Sink-Erkennung für Standard 5V Speisung) |
| **B5 (`CC2`)** | `CC2` | USB-C UFP | $5{,}1\,\text{k}\Omega$ Pull-Down nach GND (UFP Sink-Erkennung für Standard 5V Speisung) |
| **A8, B8 (`SBU1`, `SBU2`)** | `NC` | Nicht belegt | Frei / Nicht beschaltet (Analogaudio verbleibt 100 % auf `J_HELMET` auf B.Cu) |

> [!NOTE]
> **Digitales USB-Audio statt analoger Wandlung:**
> Im Kassettenbetrieb am Bike wird das Audiosignal zwischen der Host-MCU auf `PCBA 03` und dem OMM-Modul (`PCBA 09`) rein digital als USB-Audiostream (UAC / ESP-USB-Serial) über `USB_DP` und `USB_DN` übertragen. Es finden im Kassetten-Einschub keinerlei verlustbehaftete D/A- oder A/D-Wandlungen statt; Common-Impedance-Brummschleifen sind physikalisch ausgeschlossen. Analoges Audio für Helmlautsprecher und Mikrofon wird ausschließlich über den separaten Header `J_HELMET` (Platinenunterseite) geführt.

### 11.5 Belegung des 6-Pin Internen Helm-Audio & PTT Steckverbinders (`J_HELMET`)

Der auf der Platinenunterseite (`B.Cu`) platzierte 6-polige Header `J_HELMET` (JST-SH 1.0 mm, LCSC `C136657`) führt alle analogen Audio- und Steuersignale für den Helmeinsatz heraus. Durch die strikte Trennung von 5V Ladespannung (verbleibt ausschließlich auf USB-C `J1`) ist die Verbindung zu 100 % brumm- und störungsfrei:

| Pin # | Netzname | Signal-Typ | Ziel / Helm-Headset Peripherie | Elektrische Spezifikation |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `HP_OUT_L` | Audio Out | Linker Helmlautsprecher (Tip 3.5mm Klinke) | ES8388 `LOUT1`, $45\,\text{mW}$ @ $16\,\Omega$, AC-gekoppelt |
| **2** | `HP_OUT_R` | Audio Out | Rechter Helmlautsprecher (Ring 3.5mm Klinke) | ES8388 `ROUT1`, $45\,\text{mW}$ @ $16\,\Omega$, AC-gekoppelt |
| **3** | `AGND_SPK` | Audio Ground | Lautsprecher-Masse (Sleeve 3.5mm Klinke) | Stromlose Analogmasse ($I = 0\,\text{mA}$), kein Ladestrom |
| **4** | `MIC_IN+` | Audio In | Mikrofon-Kapsel (2-Pin Micro-JST Pin 1) | ES8388 `MIC1P` mit programmierbarem `MICBIAS` (2.2V) |
| **5** | `AGND_MIC` | Mic Ground | Mikrofon-Rückleitung (2-Pin Micro-JST Pin 2) | Getrennte, rauscharme Vorverstärker-Masse |
| **6** | `BTN_PTT` | Digital In | Helm-PTT-Taster / Kinn-Klicker | ESP32-C6 GPIO 2, interner $45\,\text{k}\Omega$ Pullup, schaltet gegen GND |

---

## 12. PCBA 10: OMM 446 Analog & Digital PMR446 Intercom-Modul (`openmotorbridge_omm446_ucs`)

Die Platine **`PCBA 10`** ist das universelle Open-Source-Hardwaremodul für den lizenzfreien Jedermannfunk im 446-MHz-Band. Es löst das Dilemma unhandlicher Handfunkgeräte (Midland G9 Pro etc. passen physisch in keine $100 \times 50 \times 30\,\text{mm}$ Kassette) und teurer, unwirtschaftlicher Teardowns (z. B. Midland D-10 DMR) vollständig:
* **Formfaktor-Gleichheit:** Exakt identische Außenmaße ($60{,}0 \times 30{,}0 \times 1{,}0\,\text{mm}$) und Montagepunkte wie das 2.4-GHz-Modul `PCBA 09`.
* **Universal-Einsatz:** Passt mechanisch und elektrisch sowohl in standardisierte ECE 22.06 UCS-Helmmulden als auch in den Kassetten-Schlitten (`PCBA 03`) am Motorrad.
* **Dual-Mode HF-Funk:** Vollwertiges Analog-FM (16 PMR446 Kanäle, CTCSS/DCS) und Digital-DMR Tier I (16 digitale Kanäle, TDMA 4FSK, glasklare Sprache ohne Rauschen).

![PCBA 10 OMM 446 PMR446 Intercom Modul Top 3D](../images/pcba/pcba10_omm446_intercom_top_3d.png)
*Abbildung 7.10a: PCBA 10 Top 3D (Aktuelles Routing & Placement) – ESP32-C6 Host-MCU (U1), ES8388 Audio-Codec (U4), BQ24075 PMIC (U2), ME6211 3.3V LDO (U5), IP67 USB-C (J1) und 4-Tasten-Reihe.*

![PCBA 10 OMM 446 PMR446 Intercom Modul Bottom 3D](../images/pcba/pcba10_omm446_intercom_bottom_3d.png)
*Abbildung 7.10b: PCBA 10 Bottom 3D (NiceRF SA818 & Dual-Engine) – NiceRF SA818-DMR Transceiver (U3), ESP32-PICO-V3-02 Bluetooth Co-Prozessor (U6) und Johanson 2450AT Chipantenne (ANT1).*

### 12.1 Technische Platinen-Kenndaten & Lagenaufbau
* **Abmessungen:** $60{,}0 \times 30{,}0 \times 1{,}0\,\text{mm}$ ($R = 2{,}5\,\text{mm}$ Kantenradius).
* **Lagenaufbau:** 4-Lagen FR-4 High-TG150, $1{,}0\,\text{mm}$ Materialstärke, $35\,\mu\text{m}$ Cu (Außenlagen) / $17{,}5\,\mu\text{m}$ Cu (Innenlagen für GND-Shielding und Power-Planes), ENIG-Goldfinish.
* **Befestigung:** 4x M2-Montagelöcher ($\varnothing 2{,}2\,\text{mm}$) mit $52{,}0 \times 22{,}0\,\text{mm}$ Rastermaß für formschlüssige DIN 934 M2 Mutterntaschen im 3D-Druck-Gehäuse.

### 12.2 Bestückung & Schaltkreis-Architektur

1. **Dual-Mode Funktransceiver-Modul (`U3`):**
   * **NiceRF SA818-DMR** (Ultrakompaktes $446\,\text{MHz}$ Transceiver-Modul mit integriertem DSP, CMX7141 Baseband und PA):
     * **Analog PMR446:** 16 Kanäle ($446{,}00625\dots 446{,}19375\,\text{MHz}$), $12{,}5\,\text{kHz}$ Kanalraster, 38 CTCSS-Subtöne und 83 DCS-Digitalcodes.
     * **Digital DMR Tier I:** ETSI TS 102 361-1 konform, 2-Slot TDMA 4FSK Modulation, Color Code 1–16, Direktmodus (DMO) ohne Repeater.
   * **Dual-Power Umschaltung (Software- & Hardware-gesteuert):**
     * **0,2 W ERP (Helm-Modus / SAR-Safe):** Aktiv bei Standalone-Betrieb in der Helmmulde. Minimiert HF-Absorption am Kopf und thermische Verlustleistung (Reichweite ca. 1,5–2,5 km).
     * **0,5 W ERP (Bike-Modus / High-Power):** Aktiv bei Erkennung des Kassetten-Schlittens via I2C/GPIO. Schöpft das gesetzliche PMR446-Limit voll aus (Reichweite ca. 3–6 km im Freifeld).
2. **Host-Mikrocontroller & Steuer-MCU (`U1`):**
   * **Espressif ESP32-C6-MINI-1U** (32-Bit RISC-V Single-Core @ 160 MHz):
     * Steuert das SA818-DMR per High-Speed UART über AT-Kommandos (Frequenz, CTCSS, DMR Color Code, Squelch, RF Power).
     * Stellt Bluetooth 5.3 LE zur Verfügung für drahtlose Konfiguration via Smartphone-App und WebBluetooth.
     * Unterstützt WebUSB DFU Flashing über den USB-C Port.
3. **Power-Management mit unterbrechungsfreier USV (`U2`):**
   * **Texas Instruments BQ24075RGTR** mit Dynamic Power Path Management (DPPM).
   * Ermöglicht das **Laden während des Betriebs** über USB-C (5V Bordnetz / Powerbank) bei gleichzeitig stabiler 3.3V- und PA-Speisung.
   * Fällt die externe 5V-Versorgung ab (z. B. Zündung aus oder Kassettenwechsel), übernimmt der interne 600-mAh-LiPo-Akku unterbrechungsfrei in $< 10\,\mu\text{s}$ als USV (Pufferzeit ca. 6–8 Stunden reiner Funkempfang).
4. **Audio-Frontend Stereo Codec (`U4`):**
   * **Everest Semi ES8388**: Verarbeitet das Audio-Signal des SA818-DMR analog und digital.
   * Stereo Headphone-Verstärker für Helm-Lautsprecher.
   * Differenzieller Mikrofon-Eingang mit zuschaltbarem Windgeräuschfilter und integriertem Noise-Gate.
5. **Antennensystem (Kompakte Wendel-Stummelantenne & externer Koax):**
   * **Dual-Engine HF-Entkopplung:**
     - **PMR/DMR HF-Pfad:** Der HF-Ausgang des NiceRF SA818-DMR speist über ein Tiefpass-/Bandpassfilter die U.FL-Buchse `J_RF` (`B.Cu`, $X = 110{,}5, Y = 87{,}0\,\text{mm}$). Ein paralleles Lötpad entfällt zugunsten des 100 % lötfreien Stecksystems.
     - Ein kurzes $50\,\text{mm}$ Mikro-Koaxialpigtail (RG-178 / 1.13mm) führt von `J_RF` zur wasserdichten SMA-Bulkhead-Buchse (IP67 mit EPDM O-Ring) an der Gehäusestirnseite.
     - **Helm-Default:** Im Helmbetrieb wird die $48\,\text{mm}$ kurze 446 MHz Wendel-Stummelantenne aufgeschraubt (ca. $0\dots +1{,}5\,\text{dBi}$, $1{,}5\dots 2{,}5\,\text{km}$ Reichweite). Im Kassettenbetrieb im Pod führt ein Koaxialkabel zur Außenantenne am Motorrad ($3\dots 6\,\text{km}$).
     - **Bluetooth Co-Prozessor (`U6`):** Der `ESP32-PICO-V3-02` arbeitet auf seine eigene Johanson 2450AT Keramik-Chipantenne (`ANT1`) für Nahfeld-Kopplungen.
6. **Bedienelemente & Steckverbinder:**
   * 4x taktile Mikrotaster (`SW1` bis `SW4`): PTT (Push-to-Talk / MFB), Mode (Analog/DMR Toggle), Ch+, Ch-.
   * 1x WS2812B-2020 RGB Status-LED (`D1`, RX Grün, TX Rot, DMR Blau, Chg Gelb).
   * `J1`: Wasserdichte IP67 USB-C Buchse (16-Pin) für 5V Laden, WebUSB DFU und Kassetten-Einschub.
   * `J_HELMET`: 6-Pin JST-SH 1.0mm SMD Vertikal-Header (`BM06B-SRSS-TB`) auf `B.Cu` ($X=127{,}05, Y=99{,}70\,\text{mm}$ in KiCad, vertikaler Steckanschluss für zugentlastete Kabelführung direkt in die Helmmulde) – identische Belegung und Platzierung wie PCBA 09.
   * `BAT1`: 2-polige JST-SH Micro-Buchse (`BM02B-SRSS-TB` Vertikal) auf `B.Cu` ($X=79{,}40, Y=112{,}00\,\text{mm}$) zum 1S LiPo Pouch-Akku (600 mAh mit integriertem PCM).

### 12.3 Vollständige GPIO-Pinbelegung (ESP32-C6 zu SA818-DMR & Peripherie)

| Modul-Pad | ESP32-C6 GPIO | Netzname | Signal-Typ | Funktion / Hardware-Verbindung |
| :---: | :---: | :--- | :--- | :--- |
| **Pad 8** | **`GPIO 2`** | `BTN_PTT` | Digital In (Pullup) | Taster SW1: Push-To-Talk / MFB (Low-aktiv, Boot-Pin) |
| **Pad 9** | **`GPIO 3`** | `BTN_MODE` | Digital In (Pullup) | Taster SW2: Analog FM / Digital DMR Toggle |
| **Pad 4** | **`GPIO 4`** | `BTN_CH_UP` | Digital In (Pullup) | Taster SW3: Kanalwahl Aufwärts (CH 1–16) |
| **Pad 5** | **`GPIO 5`** | `BTN_CH_DOWN` | Digital In (Pullup) | Taster SW4: Kanalwahl Abwärts (CH 16–1) |
| **Pad 6** | **`GPIO 6`** | `WS2812_DATA` | Digital Out | D1 (WS2812B RGB Statusanzeige RX/TX/DMR) |
| **Pad 7** | **`GPIO 7`** | `CHG_STAT` | Digital In (Pullup) | BQ24075 /STAT Ladezustand (Low-aktiv) |
| **Pad 10** | **`GPIO 8`** | `I2C_SDA` | Open-Drain | ES8388 Register SDA (4.7k Pullup) |
| **Pad 11** | **`GPIO 9`** | `I2C_SCL` | Open-Drain | ES8388 Register SCL (4.7k Pullup) |
| **Pad 14** | **`GPIO 12`** | `USB_DN` | USB 2.0 PHY | USB-C D- (WebUSB Firmware-Flashing & DFU via D2) |
| **Pad 15** | **`GPIO 13`** | `USB_DP` | USB 2.0 PHY | USB-C D+ (WebUSB Firmware-Flashing & DFU via D2) |
| **Pad 16** | **`GPIO 14`** | `SA818_TXD` | Digital Out (UART) | ESP32 TX -> SA818-DMR RXD (AT-Steuerbefehle @ 9600 Bd) |
| **Pad 17** | **`GPIO 15`** | `SA818_RXD` | Digital In (UART) | ESP32 RX <- SA818-DMR TXD (Status & Telemetrie) |
| **Pad 18** | **`GPIO 16`** | `SA818_PTT` | Digital Out | SA818 PTT Steuerung (Low = Sendebetrieb aktiv) |
| **Pad 19** | **`GPIO 17`** | `SA818_SQL` | Digital In | SA818 Squelch-Ausgang (Low = Träger erkannt / Empfang) |
| **Pad 20** | **`GPIO 18`** | `SA818_PWR_HL` | Digital Out | SA818 RF Power Select: Low = 0.2W (Helm), High = 0.5W (Bike) |
| **Pad 21** | **`GPIO 19`** | `I2S_MCLK` | Digital Out | ES8388 Master Clock (12.288 MHz) |
| **Pad 22** | **`GPIO 20`** | `I2S_BCLK` | Digital Out | ES8388 Bit Clock (1.536 MHz) |
| **Pad 23** | **`GPIO 21`** | `I2S_WS` | Digital Out | ES8388 Frame Sync (48 kHz) |
| **Pad 24** | **`GPIO 22`** | `I2S_DOUT` | Digital Out | ES8388 DAC Out (Lautsprecher / Audio zu Zentralbox) |
| **Pad 25** | **`GPIO 23`** | `I2S_DIN` | Digital In | ES8388 ADC In (Mikrofon von Helm / Central DSP) |
| **J_RF** | **RF 446M** | `RF_ANT` | 50 Ohm Koaxial | U.FL Buchse (`B.Cu`) -> Koax-Pigtail -> IP67 SMA-Durchführung |

### 12.4 Belegung des 16-Pin Multi-Use USB-C Steckverbinders (`J1`)

Identisch beschaltet wie bei PCBA 09: Dient als universelle Schnittstelle für **Laden (5V Bordnetz / Powerbank)**, **WebUSB/DFU-Flashing** und den **Kassetten-Einschubkontakt** im Smart Cartridge (`PCBA 03`).

### 12.5 Belegung des 6-Pin Internen Helm-Audio & PTT Steckverbinders (`J_HELMET`)

Der Header `J_HELMET` auf `B.Cu` ist **100 % anschlusskompatibel zu PCBA 09**:

| Pin # | Netzname | Signal-Typ | Ziel / Helm-Headset Peripherie | Elektrische Spezifikation |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `HP_OUT_L` | Audio Out | Linker Helmlautsprecher (Tip 3.5mm Klinke) | ES8388 `LOUT1`, $45\,\text{mW}$ @ $16\,\Omega$, AC-gekoppelt |
| **2** | `HP_OUT_R` | Audio Out | Rechter Helmlautsprecher (Ring 3.5mm Klinke) | ES8388 `ROUT1`, $45\,\text{mW}$ @ $16\,\Omega$, AC-gekoppelt |
| **3** | `AGND_SPK` | Audio Ground | Lautsprecher-Masse (Sleeve 3.5mm Klinke) | Stromlose Analogmasse ($I = 0\,\text{mA}$), kein Ladestrom |
| **4** | `MIC_IN+` | Audio In | Mikrofon-Kapsel (2-Pin Micro-JST Pin 1) | ES8388 `MIC1P` mit programmierbarem `MICBIAS` (2.2V) |
| **5** | `AGND_MIC` | Mic Ground | Mikrofon-Rückleitung (2-Pin Micro-JST Pin 2) | Getrennte, rauscharme Vorverstärker-Masse |
| **6** | `BTN_PTT` | Digital In | Helm-PTT-Taster / Kinn-Klicker | ESP32-C6 GPIO 2, interner $45\,\text{k}\Omega$ Pullup, schaltet gegen GND |
