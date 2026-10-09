# 07 - Hardware-Architektur & Platinen-Pinouts (Das bereinigte 5-PCBA-Lineup)

Dieses Dokument bildet die **zentrale, autoritative Hardware-Spezifikation aller 5 aktiven Platinen-Baugruppen (`PCBA 01`, `03`, `05`, `07`, `08`)** des OpenMotorBridge Gesamtsystems (v9.6 Clean All-UWB Architecture), einschließlich Lagenaufbau, Impedanzkontrolle, Net-Klassen, Funktionszonen und vollständigen Pinout-Tabellen.

---

## 1. Systemübersicht des 5-Platinen-Lineups

Das Hardwaredesign von OpenMotorBridge folgt dem Grundsatz der radikalen Entflechtung: Daten- und Audioströme werden zu 100 % drahtlos über ein synchrones Ultra-Wideband-Backbone (UWB 6.5 GHz) geführt, während der fahrzeuggebundene Kabelbaum auf reine 2-Draht-Gleichspannung (12V DC) und CAN-Bus reduziert ist.

```
+----------------------------------------------------------------------------------------+
|                   DAS 5-PLATINEN-LINEUP DER OPENMOTORBRIDGE v9.6                       |
+-------+-------------------------------+---------------+---------+----------------------+
| Baugruppe | Name & Funktion           | Platinenmaße  | Lagen   | Kern-ICs / Bauteile  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 01**| **Zentralbox Main Controller** | 85 x 55 mm    | 4 Lagen | ESP32-S3, QCC3084 BT,|
|       | (Unter der Sitzbank, Audio/USV)| (77x47 mm M3) | (ENIG)  | LM5164, BQ24075,     |
|       |                                |               |         | ES8388, SX1262 LoRa, |
|       |                                |               |         | DW3110 UWB, DTM-12   |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 03**| **Universal Smart Cartridge** | 35 x 25 mm    | 2 Lagen | Qorvo DW3110 UWB,    |
|       | (Kassettenträger Bucht 1 & 2) | (29x19 mm M2) | (ENIG)  | ESP32-C6, ES8388,    |
|       |                                | 2-seitig SMT  |         | 4x AO3400A, J_ACT    |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 05**| **Universal Front-Knoten**    | 82 x 50 mm    | 4 Lagen | ESP32-S3, DW3110 UWB,|
|       | (Cockpit, GNSS, Sensoren, UWB)| (4x M2.5)     | (ENIG)  | SAM-M10Q, USB2514B,  |
|       |                               |               |         | SC8102 PD20W, TPS2051|
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 07**| **2-in-1 LoRa Smart-Keyfob**  | 38 x 19 mm    | 2 Lagen | Nordic nRF52840 SoC, |
|       | (Silent Pager, N52 Key & Qi)  | (Tasche M2)   | (ENIG)  | SX1262 LoRa, DRV2605L|
|       |                               |               |         | BQ51003 Qi, JST-ACH  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 08**| **Radar 2.0 Sub-MCU & Wings** | 115 x 65 mm   | 2 Lagen | ESP32-C5, DW3110 UWB,|
|       | (Wheeltec 77GHz & V2X Patch)  | (Flügel M2.5) | (ENIG)  | Wheeltec MR20 (AoP),  |
|       |                               |               |         | 36x WS2812B, JWPF 12V |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 09**| **OMM 2.4 GHz UCS Intercom**  | 60 x 30 mm    | 2 Lagen | ESP32-C6 RISC-V,     |
|       | (ECE 22.06 Autonom & Pod)     | (UCS M2)      | (ENIG)  | TI BQ24075, ES8388,  |
|       |                               |               |         | 600mAh LiPo, FXP73   |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 10**| **OMM 446 MHz UCS Intercom**  | 60 x 30 mm    | 4 Lagen | NiceRF SA818-DMR,    |
|       | (DMR Tier I & Analog PMR446)  | (UCS M2)      | (ENIG)  | ESP32-C6, BQ24075,   |
|       |                               |               |         | ES8388, Helix-Antenne|
+-------+-------------------------------+---------------+---------+----------------------+
```

### 1.1 Gliederung nach Systemkomponenten
1. **Kern-Baugruppen (Standard-Ausstattung jedes Bikes):**
   * **`PCBA 01` (Zentralbox Main Controller):** Zentrale Recheneinheit unter der Sitzbank für Energie-Management, USV, DSP-Mischung, Dual-Bluetooth-Headsets, LoRa-Schwarm und UWB-Koordination.
   * **`PCBA 03` (Universal Smart Cartridge):** Universelle Trägerplatine für Bucht 1 und Bucht 2. Beherbergt wahlweise Sena SPIDER X Slim, Cardo Packtalk Edge, das OMM 2.4 GHz Modul (`PCBA 09`) oder das OMM 446 MHz Funkmodul (`PCBA 10`).
   * **`PCBA 05` (Universal Front-Knoten):** Cockpit-Einheit für Multi-GNSS (SAM-M10Q), Kaltluft-Sensorik, Ambient-Mikrofon, USB-Hub und Headless CarPlay/Android Auto Bridge.
2. **Empfohlene Erweiterungen & Peripherie:**
   * **`PCBA 07` (2-in-1 LoRa Smart-Keyfob & Silent Pager):** Tragbarer Schlüsselanhänger für 4,5 km Weitbereichs-Alarmierung, N52-Magnetschlüssel und induktive Qi-Ladung.
   * **`PCBA 08` (Radar 2.0 Sub-MCU & Warnflügel):** Heckmodul mit 77-GHz-mmWave-Sensorik (AoP), autonomem Brems- und Kollisionsstrobe sowie 5.9 GHz V2X-Uplink.
   * **`PCBA 09` (OMM 2.4 GHz Autonomes Intercom-Modul):** Quelloffenes, autarkes ECE 22.06 UCS-Intercom-Modul für den Helm und als High-Speed Mesh-Einsatz im Kassetten-Schlitten (`PCBA 03`).
   * **`PCBA 10` (OMM 446 MHz Autonomes Funkmodul):** Quelloffenes ECE 22.06 UCS-Funkmodul (Dual-Mode: Analog PMR446 + Digital DMR Tier I), voll kompatibel zu Midland G-Serie und D-10, mit Power-Path USV-Laden und 0.2W/0.5W Umschaltung.
3. **Ersatzlos entfallene Baugruppen (Architektur-Bereinigung v9.6):**
   * **`PCBA 02` (Pod-Basisplatine):** Ersatzlos gestrichen. Die Zuleitung führt direkt auf zwei vergoldete Federkontakte im Schachtboden.
   * **`PCBA 04` (Heck-Pod 3):** Ersatzlos gestrichen. Heck-Pod 3 entfällt vollständig; LoRa sitzt auf `PCBA 01`, GNSS auf `PCBA 05`.
   * **`PCBA 06` (MagSafe Frame Dock Platine):** Ersatzlos gestrichen. Die elektrische Verbindung bei Koffer-Pods erfolgt über einen handelsüblichen industriellen 2-Pin Magnet-Pogo-Steckverbinder (IP68 COTS).

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
| Layer 3 (In2.Cu): Power-Planes (VCC_3V3, VCC_5V Polygone)   |  (17.5 µm Standard)
+-------------------------------------------------------------+
| -- Prepreg 7628 (Dielektrikum, Er = 4.4, Dicke 0.2 mm) --   |
+-------------------------------------------------------------+
| Layer 4 (B.Cu - Bottom): Sekundär-Routing, DW3110 UWB       |  (35 µm / 1 oz Cu)
+-------------------------------------------------------------+
```

### 2.1 Standardisierte Net-Klassen & Leiterbahn-Geometrien
* **`Default`:** Leiterbahnbreite $0{,}20\,\text{mm}$, Mindestabstand $0{,}20\,\text{mm}$ (Logiksignale, GPIOs).
* **`Power_5V_12V`:** Leiterbahnbreite $0{,}60\,\text{mm}$ (Stromtragfähigkeit bis $2{,}2\,\text{A}$ bei $\Delta T < 10\,^\circ\text{C}$).
* **`RF_50R`:** Leiterbahnbreite $0{,}35\,\text{mm}$, Koplanarabstand $0{,}20\,\text{mm}$ zur Massefläche (50 Ohm Wellenwiderstand für 868 MHz LoRa und DW3110 UWB 6.5 GHz).
* **`USB_90R_DIFF`:** Leiterbahnbreite $0{,}20\,\text{mm}$, differentieller Leiterbahnabstand $0{,}15\,\text{mm}$ ($90\,\Omega \pm 10\,\%$ Differenzimpedanz für USB 2.0 High-Speed 480 Mbps).
* **`Audio_Sensitive`:** Leiterbahnbreite $0{,}25\,\text{mm}$, Abstand $0{,}30\,\text{mm}$ (abgeschirmt durch flankierende GND-Leiterbahnen).

---

## 3. PCBA 01: Zentralbox Main Controller (`openmotorbridge_central_box`)

![PCBA 01 Zentralbox Main Controller Top 3D](../images/pcba/pcba01_central_box_3d.png)
*Abbildung 7.1a: KiCad 3D-Render der Zentralbox-Hauptplatine Top (PCBA 01, 85 x 55 mm, 4 Lagen) mit ESP32-S3 WROOM-1, Qualcomm QCC3084 BT 5.4 Audio SoC, LM5164-Q1 72V Buck, BQ24075 USV, ES8388 DSP-Codec, Semtech SX1262 LoRa und Deutsch DTM-12 Header.*

![PCBA 01 Zentralbox Main Controller Bottom 3D](../images/pcba/pcba01_central_box_bottom_3d.png)
*Abbildung 7.1b: KiCad 3D-Render der Zentralbox-Hauptplatine Bottom mit DM3D MicroSD-Push-Pull-Slot, Qorvo DW3110 UWB Transceiver, BMI270 6-Achs-IMU und TCAN334G CAN-Transceiver.*

### 3.1 Technische Platinen-Kenndaten & Top/Bottom-Aufteilung
* **Abmessungen:** $85{,}0 \times 55{,}0\,\text{mm}$ (Außenkontur mit 4x M2.5 Montagebohrungen, $77{,}0 \times 47{,}0\,\text{mm}$ Lochabstand).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$ Gesamtdicke, ENIG-Goldfinish).
* **Bestückung Top-Layer (F.Cu):**
  * **Hauptcontroller (`U2`):** Espressif `ESP32-S3-WROOM-1U` (Dual-Core @ 240 MHz, 16 MB Flash, 8 MB Octal-PSRAM) für Systemsteuerung, CAN-Bus, FreeRTOS DSP-Pipeline und PWA-Webserver.
  * **Dedizierter Helm-Audio-SoC (`U9`):** **Qualcomm QCC3084** Bluetooth 5.4 Audio-SoC ($13 \times 18\,\text{mm}$) für Dual-A2DP (aptX HD, Low Latency), LE Audio Auracast Broadcast und kristallklare Hands-Free Telefonie (HFP 1.8 mit Wideband Speech) mit integrierter Keramik-Chipantenne.  
    *(Wichtige Entkopplung: Der interne BLE-Stack des ESP32-S3 dient rein dem WebApp-Dashboard und Sensordaten, während der QCC3084 das Helm-Audio völlig unbeeinflusst von CPU-Spitzen abwickelt).*
  * **Weitbereichsfunk (`U10`):** Semtech `SX1262` LoRa Transceiver (+22 dBm PA) mit U.FL-Buchse `ANT1` zur Taoglas FXP895 Antenne in der Gehäusedeckeltasche.
  * **Bordnetz-Speisung (`U1`):** Texas Instruments `LM5164-Q1` synchroner 72V-Buck-Converter und TI `BQ24075` Power-Path-Controller mit Ladeschaltung für die interne 2.200-mAh-USV-Zelle.
  * **Status-Anzeige (`D1`):** WS2812B RGB Smart-LED zur optischen Status- und Pairing-Signalisierung.
  * **Bedienelemente & Interface:** Hardware-Taster `SW1` (Pairing / Werkseinstellung / ESP32 Bootloader) und automotiver Deutsch DTM-12 Shrouded Header `J1` sowie Box-Header `J3` und JST-Header `J4`/`J5`.
* **Bestückung Bottom-Layer (B.Cu):**
  * **MicroSD-Kartenslot (`J2`):** Hirose `DM3D-SF` Push-Pull MicroSD-Kartenhalter, montiert an der oberen Platinenkante ($X=146{,}0, Y=79{,}0$, $180^\circ$ gedreht) mit Karteneinschub bündig zur Gehäusekante für werkzeugfreie Zugänglichkeit (0 mm Überlappung, >2.4 mm Sicherheitsabstand zu allen Nachbarbauteilen).
  * **UWB-Funkknoten (`U8`):** Qorvo `DW3110` Ultra-Wideband IEEE 802.15.4z Transceiver (Kanal 5 @ 6.489 GHz) mit $38{,}4\,\text{MHz}$ Quarz `Y1_UWB` und U.FL-Buchse `ANT2` zur Taoglas FXUWB10 Antenne in der Gehäusebodentasche.
  * **Audio-Codec (`U3`):** Everest Semi `ES8388` 24-Bit / 48 kHz Low-Power Stereo-Audio-Codec.
  * **Sensoren (`U5`):** Bosch `BMI270` 6-Achs-IMU (I2C) zur Wake-on-Motion Diebstahlüberwachung und Sturzerkennung.
  * **CAN-Transceiver (`U6`):** Texas Instruments `TCAN334G` / `TCAN1042V` 5 Mbps CAN-FD Bus-Transceiver.
  * **Low-Noise LDO (`U11`):** Texas Instruments `TPS7A0533` 3.3V Ultra-Low-Noise LDO für saubere Analog- und Sensor-Spannungsversorgung.
  * Durchgehende thermische Massevias zur Wärmeabfuhr des LM5164 und der eFuses.

### 3.2 Pinbelegung des 12-poligen Deutsch DTM-12 Steckverbinders (`J1`)

```
+---------------------------------------------------------------------------------------------------------------+
| DEUTSCH DTM-12 PINBELEGUNG (ZENTRALBOX POWER, CAN & DC-PEITSCHEN 1 BIS 4)                                     |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
| Pin | Signalname     | Signalart / Pegel        | Querschnitt | Kabelbaum-Zweig     | Funktion & Schutz       |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
|  1  | KL30_IN        | +9V...+72V DC Dauerplus  | AWG20 0.50² | Peitsche 4 (Bordnetz)| Bordnetz Dauerplus     |
|  2  | KL15_IGN       | +9V...+72V DC Zündungspl.| AWG22 0.34² | Peitsche 4 (Bordnetz)| Zündungssignal (KL15)   |
|  3  | VEHICLE_GND    | Power-Masse (0V)         | AWG20 0.50² | Peitsche 4 (Bordnetz)| Zentrale Bordnetzmasse  |
|  4  | CAN_H          | CAN-FD High (ISO 11898-2)| AWG24 0.22² | Peitsche 4 (Bordnetz)| Fahrzeug-CAN Bus High   |
|  5  | CAN_L          | CAN-FD Low (ISO 11898-2) | AWG24 0.22² | Peitsche 4 (Bordnetz)| Fahrzeug-CAN Bus Low    |
|  6  | POD1_VCC       | +12V geschaltet (0,5A)   | AWG22 0.34² | Peitsche 1 (Pod 1)  | DC-Power Bucht 1 (eFuse)|
|  7  | POD1_GND       | Power-Masse (0V)         | AWG22 0.34² | Peitsche 1 (Pod 1)  | Masse Bucht 1 (Links)   |
|  8  | POD2_VCC       | +12V geschaltet (0,5A)   | AWG22 0.34² | Peitsche 2 (Pod 2)  | DC-Power Bucht 2 (eFuse)|
|  9  | POD2_GND       | Power-Masse (0V)         | AWG22 0.34² | Peitsche 2 (Pod 2)  | Masse Bucht 2 (Rechts)  |
| 10  | RADAR_PWR_12V  | +12V geschaltet (1,0A)   | AWG22 0.34² | Peitsche 3 (Radar)  | DC-Power Heck-Radar     |
| 11  | RADAR_GND      | Power-Masse (0V)         | AWG22 0.34² | Peitsche 3 (Radar)  | Masse Heck-Radar        |
| 12  | CHASSIS_EARTH  | Schirmmasse              | AWG20 0.50² | Peitsche 4 (Bordnetz)| Gehäuse- & Schirmschutz |
+-----+----------------+--------------------------+-------------+---------------------+-------------------------+
```

### 3.3 Pinbelegung & Systemanbindung: Qualcomm QCC3084 BT 5.4 Audio SoC (`U9`)

Der auf der Oberseite (`F.Cu` bei $X=175{,}0, Y=106{,}0$) platzierte **Qualcomm QCC3084** ($13 \times 18\,\text{mm}$ Modul mit integrierter Keramik-Chipantenne) verbindet die Helme drahtlos über hardware-beschleunigtes Dual-A2DP (aptX HD / Adaptive) und HFP 1.8:

```
+----------------------------------------------------------------------------------------+
| QUALCOMM QCC3084 PINBELEGUNG & SCHNITTSTELLEN ZUM ESP32-S3 / ES8388                    |
+-----+----------------+--------------------+-------------------+------------------------+
| Pin | Signalname     | Signalart          | Verbunden mit     | Funktion & Protokoll   |
+-----+----------------+--------------------+-------------------+------------------------+
|  1  | VCC_3V3        | Power In (+3.3V)   | LM5164 3.3V Bus   | Modul-Betriebsspannung |
|  2  | GND            | Masse (0V)         | GND_PWR Plane     | HF- und Systemmasse    |
|  3  | I2S_MCLK       | Digital In (Clock) | ESP32-S3 (GPIO 9) | Master-Clock (12.288M) |
|  4  | I2S_BCLK       | Digital In (BitClk)| ESP32-S3 (GPIO 10)| Bit-Clock (3.072 MHz)  |
|  5  | I2S_WS         | Digital In (LRCK)  | ESP32-S3 (GPIO 11)| Word-Select (48 kHz)   |
|  6  | I2S_DOUT       | Digital In (Audio) | ESP32-S3 (GPIO 12)| Stereo-PCM zum QCC3084 |
|  7  | I2S_DIN        | Digital Out (Mic)  | ESP32-S3 (GPIO 13)| HFP-Mikrofon zum DSP   |
|  8  | GND            | Masse (0V)         | GND_PWR Plane     | HF-Schirmmasse         |
|  9  | BT_UART_TX     | Digital Out (UART) | ESP32-S3 (GPIO 18)| QCC3084 Telemetrie/AT  |
| 10  | BT_UART_RX     | Digital In (UART)  | ESP32-S3 (GPIO 17)| ESP32 AT-Steuerbefehle |
| 11  | BT_EN          | Digital In (Reset) | ESP32-S3 (GPIO 16)| Kaltstart & Power-Down |
| 12  | GND            | Masse (0V)         | GND_PWR Plane     | HF-Schirmmasse         |
+-----+----------------+--------------------+-------------------+------------------------+
```

* **Integrierte Keramik-Chipantenne:** 2.402–2.480 GHz, Gewinn $+2{,}0\,\text{dBi}$, omnidirektionale Charakteristik nach oben/vorn zum Cockpit und Fahrer-/Sozius-Helm.
* **Keine Koax-Zuleitung:** Durch die direkte Abstrahlung vom Modulsubstrat bleibt das Innere der Zentralbox aufgeräumt und störungsarm.

---

## 4. Satelliten Pod-Gehäuse & Entfall von PCBA 02 (Monolithisches Gehäuse)

Die frühere Pod-Basisplatine (`PCBA 02`) ist in v9.6 **vollständig und ersatzlos entfallen**:
1. **Monolithischer Gehäusekörper:** Das Pod-Gehäuse (`pod_base_housing.stl`) ist ein 100 % passives 3D-Druck-Präzisionsteil (MJF PA12).
2. **Direkte 2-Draht DC-Federkontaktierung:** Die 2-adrige DC-Leitung vom Deutsch DTM-12 Stecker führt über eine rückseitige Formdichtung direkt in den Schacht und endet an zwei massiven, vergoldeten Federkontakten (Mill-Max).
3. **Null Ausfallrisiko:** Keine Schalter, keine aktiven ICs und keine empfindlichen Buchsen im Spritzwasserbereich der Kofferträger.

---

## 5. PCBA 03: Universal Smart Cartridge (`openmotorbridge_pod_cartridge` Rev 3.0)

![PCBA 03 Universalschlitten Cartridge Top 3D](../images/pcba/pcba03_pod_cartridge_3d.png)
*Abbildung 7.3a: KiCad 3D-Render der Universal Smart Cartridge Top (PCBA 03 Rev 3.0, 35 x 25 mm) mit ESP32-C6 Host-MCU, 4x AO3400A MOSFETs und J_ACT Mechatronik-Header.*

![PCBA 03 Universalschlitten Cartridge Bottom 3D](../images/pcba/pcba03_pod_cartridge_bottom_3d.png)
*Abbildung 7.3b: KiCad 3D-Render der Universal Smart Cartridge Bottom mit Qorvo DW3110 UWB Transceiver, ES8388 Stereo-Codec und Audio-Power-Header J_AUDIO_PWR.*

### 5.1 Technische Platinen-Kenndaten & Funktionale Lagen-Aufteilung
* **Abmessungen:** $35{,}0 \times 25{,}0\,\text{mm}$ (Raster $29{,}0 \times 19{,}0\,\text{mm}$ mit 4x M2 Befestigungsbohrungen).
* **Lagenaufbau:** 2 Lagen FR-4 High-TG150 ($1{,}2\,\text{mm}$ Dicke, $35\,\mu\text{m}$ Cu beidseitig, ENIG-Goldfinish).
* **Bestückung Top-Layer (F.Cu - Mechatronik & Steuerung):**
  * `U2`: Espressif `ESP32-C6` RISC-V Host-MCU (verwaltet Kassetten-Profile, UWB-Kommunikation und Aktuator-Timings).
  * `Q1` - `Q4`: 4x N-Kanal MOSFETs (`AO3400A`, SOT-23, $30\,\text{V} / 5{,}7\,\text{A}$) samt Freilaufdioden `D1`-`D4`. Platziert unmittelbar neben dem Header `J_ACT` für kürzeste Leiterbahnwege zu den Taster-Aktuatoren.
  * `J_ACT`: 8-poliger $1{,}0\,\text{mm}$ JST-SH Header zur Ansteuerung der 4 Miniatur-Hubmagnete.
  * `J_AUDIO_PWR`: **8-poliger $1{,}0\,\text{mm}$ JST-SH Header** (baugleich zu `J_ACT`) zur galvanisch getrennten Stern-Masseanbindung des Adapterkabelstrangs an das jeweilige OEM-Headset.
* **Bestückung Bottom-Layer (B.Cu - HF, Audio-Codec & Stromaufnahme):**
  * `U1`: Qorvo `DW3110` Ultra-Wideband Transceiver (6.489 GHz Ch. 5) mit integrierter PCB-Antenne. Strahlungsrichtung zeigt nach unten durch den Kunststoffboden der Kassette für optimale Funkverbindung zur Zentralbox.
  * `U3`: Everest Semi `ES8388` 24-Bit / 48 kHz Low-Noise Audio-Codec. Bewusst auf der **Unterseite (`B.Cu`)** platziert: Dadurch sind die empfindlichen analogen Mikrofon- und Kopfhörerleitungen durch die interne Kupfer-Massefläche hermetisch von den steilen Schaltflanken der Top-Layer-MOSFETs (`Q1`–`Q4`) und Aktuatorströmen entkoppelt. Wandelt das analoge Mikrofon- und Lautsprechersignal von Sena, Cardo oder Midland direkt auf der Kassette und streamt es jitterfrei digital via I2S/UWB.
  * `PAD1` & `PAD2`: Stirnseitige, massive vergoldete Kontaktflächen (ENIG) für die 2-Draht DC-Federkontakte des Pods.
  * `F1`: Selbstrückstellende 500mA PPTC-Sicherung.

### 5.2 Pinbelegung des Audio-Power-Headers (`J_AUDIO_PWR` / 8-Pin JST-SH 1.0mm)

Um das gefürchtete **Übersprechen von Lade- und Sendeströmen in das Audiosignal (Common-Impedance Coupling)** physikalisch auszuschließen, ist der Header `J_AUDIO_PWR` als **8-Pin JST-SH** mit strikter Trennung von Leistungs- und Audio-Massen ausgelegt:

| Pin | Signalname | Richtung | Funktion & OEM-Verbindung |
| :---: | :--- | :---: | :--- |
| **1** | **`PGND`** | Power Return | **Leistungs-Masse:** Führt den gesamten Rückstrom des Laders / DC-DC-Wandlers ($0{,}2\dots 0{,}6\,\text{A}$) |
| **2** | **`VCC_HEADSET`** | Power Out (+5V / +3.85V) | Geregelte Betriebsspannung für das Intercom-Modul (Lade- oder Dauerstrom) |
| **3** | **`AGND_SPK`** | Audio-Massebezug | **Saubere Kopfhörermasse:** Führt zum 3,5-mm-Klinkenhülsen-Kontakt (Sleeve) – **stromlos ($I = 0\,\text{mA}$)!** |
| **4** | **`AUDIO_L_IN`** | Audio In $\leftarrow$ OEM | Line-Out Lautsprecher Links vom Headset zum ES8388 ADC (Kanal 1) |
| **5** | **`AUDIO_R_IN`** | Audio In $\leftarrow$ OEM | Line-Out Lautsprecher Rechts vom Headset zum ES8388 ADC (Kanal 2) |
| **6** | **`AGND_MIC`** | Audio-Massebezug | **Saubere Mikrofonmasse:** Eigener Rückleiter für den Mikrofoneingang – **stromlos ($I = 0\,\text{mA}$)!** |
| **7** | **`MIC_OUT`** | Audio Out $\rightarrow$ OEM | Mikrofonsignal vom ES8388 DAC in das Headset ($< 1\,\text{ms}$ Latenz) |
| **8** | **`PTT_IO`** | Bidir / Open-Drain | PTT-Tastung gegen Masse (Midland PMR446) oder DMR/Mode-Select |

> [!IMPORTANT]
> **Warum 8 Pins die Strombrumm-Problematik („Lade- & Mesh-Surren“) zu 100 % lösen:**
> 1. **Das Problem geteilter Massen:** Zieht ein Headset z. B. $300\,\text{mA}$ Lade- oder HF-Sendestrom über eine gemeinsame Masseleitung mit $80\,\text{m}\Omega$ Gesamtwiderstand (Steckkontakt + Litze), schwankt das Massepotential um $\Delta V = 300\,\text{mA} \times 0{,}08\,\Omega = 24\,\text{mV}$. Da Mikrofon-Signale typisch nur $5\dots 15\,\text{mV}$ betragen, würde der Mikrofoneingang des Headsets dieses $24\,\text{mV}$ Spannungsbrummen (Mesh-TDMA-Knattern, Schaltregler-Pfeifen) um $+30\,\text{dB}$ vorverstärken!
> 2. **Die OpenMotorBridge-Lösung (Kelvin-Grounding):** Durch die getrennten Pins `AGND_SPK` (Pin 3) und `AGND_MIC` (Pin 6) fließt **kein einziger Milliampere Betriebsstrom** ($I_{\text{Audio}} = 0\,\text{A}$). Der ohmsche Spannungsabfall ist physikalisch **exakt $\Delta V = 0\,\text{mV}$**. Der hohe Laststrom fließt isoliert über Pin 1 (`PGND`) direkt zum DC-DC-Filter auf `PCBA 03` ab.
> 3. **BOM-Vorteil:** Durch den Wechsel auf 8 Pins nutzt `J_AUDIO_PWR` exakt dieselbe LCSC-Teilenummer (`JST_SH_SM08B-SRSS-TB`) wie der Mechatronik-Header `J_ACT`. Das spart einen Feeder-Slot bei JLCPCB und eliminiert Bestückungsfehler.


### 5.3 Pinbelegung des Aktuator-Headers (`J_ACT` / 8-Pin JST-SH 1.0mm)
| Pin | Signalname | Ansteuerung | Mapping: Sena SPIDER X Slim | Mapping: Cardo Packtalk Edge |
| :---: | :--- | :---: | :--- | :--- |
| **1 & 2** | `VCC_5V` | Dauer-5V | Gemeinsame Versorgungs-Schiene für alle 4 Aktuatoren |
| **3** | `ACT1_OUT` | MOSFET `Q1` | **Plus (+)** (Lauter / Menü vor) | **Media Button** (Front/Top) |
| **4** | `ACT2_OUT` | MOSFET `Q2` | **Minus (-)** (Leiser / Menü zurück)| **Mobile Button** (Phone/Pairing) |
| **5** | `ACT3_OUT` | MOSFET `Q3` | **Center / Phone** (Bestätigen)   | **Intercom Button** (DMC Grouping) |
| **6** | `ACT4_OUT` | MOSFET `Q4` | **Mesh Button** (45° seitlich)    | **Control Wheel Center-Press** |
| **7 & 8** | `GND` | Power-Masse | Massebezug für Rückstrom | Massebezug für Rückstrom |

---

## 6. PCBA 04: Heck-Pod 3 (Ersatzlos entfallen)

Die Heckplatine `PCBA 04` und das zugehörige Heckgehäuse Pod 3 sind **vollständig gestrichen**:
* Der Semtech SX1262 LoRa-Transceiver arbeitet direkt auf der Zentralbox (`PCBA 01`).
* Das u-blox SAM-M10Q GNSS-Modul arbeitet im Fahrtwindeinlass des Front-Knotens (`PCBA 05`).

---

## 7. PCBA 05: Universal Front-Knoten (`openmotorbridge_front_node`)

![PCBA 05 Universal Front-Knoten Top 3D](../images/pcba/pcba05_front_node_3d.png)
*Abbildung 7.5a: KiCad 3D-Render des Universal Front-Knotens Top (PCBA 05, 82 x 50 mm) mit ESP32-S3-WROOM-1U, u-blox SAM-M10Q GNSS, Microchip USB2514B Hub und Southchip SC8102 USB-PD 20W Fast-Charge.*

![PCBA 05 Universal Front-Knoten Bottom 3D](../images/pcba/pcba05_front_node_bottom_3d.png)
*Abbildung 7.5b: KiCad 3D-Render des Universal Front-Knotens Bottom mit Qorvo DW3110 UWB Transceiver und U.FL-HF-Verbindung.*

### 7.1 Technische Platinen-Kenndaten
* **Abmessungen:** $82{,}0 \times 50{,}0\,\text{mm}$ (Gehäuseaußenmaß $98 \times 68 \times 25\,\text{mm}$ mit 4-in-1 Halterung).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$, ENIG-Goldfinish).
* **Top-Layer:** ESP32-S3 Controller, USB2514B USB-Hub, u-blox SAM-M10Q Multi-GNSS mit integrierter Patchantenne, Knowles SPH0645LM4H I2S MEMS Akustiksensor, WS2812B-2020 RGB-LED und 5 GHz Wi-Fi Anbindung für Headless CarPlay / Android Auto.
* **Bottom-Layer:** Qorvo DW3110 UWB Transceiver (6.489 GHz Ch. 5), TI LMR36015 Buck, SC8102 USB-PD 20W Fast-Charger, TI TPS2051B Lastschalter für automatischen Dongle-Kaltstart und Auto-Café-Modus.

### 7.2 Vollständige Pinbelegung der Front-Node Steckverbinder (`J1` bis `J12`)

Alle internen Cockpit-, Lade- und Sensoranschlüsse sind auf vibrationsfeste **JST-PH Steckverbinder (2,0 mm Raster)** sowie **JST-SH / Qwiic (1,0 mm Raster)** geführt. Handelsübliche, vorkonfektionierte COTS-Pigtail-Kabel werden werkzeuglos angesteckt:

| Header | Typ / Raster | Pin | Signalname | Signalpegel / Richtung | Funktion & angeschlossene Cockpit-Peripherie |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`J1`** | **JST-PH 2-Pin**<br>(2.0 mm) | 1<br>2 | `KL15_12V_SW`<br>`GND` | +9V...+16V In<br>Power-Masse | **12V Bordnetzspeisung:** Zündungsplus (Standlicht / Cartool-Stecker / Y-Kabel Abzweig A) |
| **`J2`** | **JST-PH 3-Pin**<br>(2.0 mm) | 1<br>2<br>3 | `CAN_H`<br>`CAN_L`<br>`GND` | CAN-FD High<br>CAN-FD Low<br>Massebezug | **Fahrzeug-CAN-Bus:** Direkter Abgriff im Cockpit / Diagnosestecker mit TCAN334G & CPC1017N Busabschluss |
| **`J3`** | **JST-PH 4-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4 | `GND`<br>`PTT_IN1_N`<br>`PTT_IN2_N`<br>`PTT_IN3_N` | Masse (0V)<br>Digital In (Pull-Up)<br>Digital In (Pull-Up)<br>Digital In (Pull-Up) | **Lenkerarmatur / Multifunktionstaster:**<br>Taste 1: PTT Intercom Funk / Voice<br>Taste 2: Action-Cam Bookmark / Highlight<br>Taste 3: Quick-Action / Navigationsmenü |
| **`J4`** | **JST-PH 4-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4 | `USB_UP_VBUS`<br>`USB_UP_DM`<br>`USB_UP_DP`<br>`GND` | +5V VBUS In<br>USB 2.0 D-<br>USB 2.0 D+<br>Masse (0V) | **USB Upstream Host:** Verbindung zum OEM-Motorrad-Infotainment (Harley Boom! Box / Skyline OS) |
| **`J5`** | **JST-PH 5-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4<br>5 | `VBUS_PD1_OUT`<br>`USB_DN1_DM`<br>`USB_DN1_DP`<br>`USB_DN1_CC`<br>`GND` | +5V / +9V / +12V Out<br>USB 2.0 D-<br>USB 2.0 D+<br>Configuration Channel<br>Power-Masse | **Smartphone Fast-Charge PD 20W:** Pigtail auf wetterfeste USB-C Buchse am Lenker (SW3526 Regler `U5`, USB-PD 3.0, QC4+) |
| **`J5_MP3`** | **JST-PH 5-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4<br>5 | `VBUS_PD3_OUT`<br>`USB_DN3_DM`<br>`USB_DN3_DP`<br>`USB_DN3_CC`<br>`GND` | +5V / +9V / +12V Out<br>USB 2.0 D-<br>USB 2.0 D+<br>Configuration Channel<br>Power-Masse | **Glovebox / Media-Bay PD 20W + MP3:** Pigtail ins Handschuhfach für Musik-USB-Sticks, Powerbanks und Zweithandy (SW3526 `U8`) |
| **`J6`** | **JST-PH 4-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4 | `VCC_5V_OTTOCAST`<br>`USB_DN2_DM`<br>`USB_DN2_DP`<br>`GND` | +5V geschaltet (1.5A)<br>USB 2.0 D-<br>USB 2.0 D+<br>Masse (0V) | **CP2AA Wireless Dongle Pigtail:** USB-A Buchsenkabel für Ottocast / Carlinkit Adapter mit automatischem Kaltstart via TPS2051B |
| **`J6_AUX`** | **JST-PH 4-Pin**<br>(2.0 mm) | 1<br>2<br>3<br>4 | `VCC_5V`<br>`USB_DN4_DM`<br>`USB_DN4_DP`<br>`GND` | +5V Out (1.0A)<br>USB 2.0 D-<br>USB 2.0 D+<br>Masse (0V) | **Cockpit Aux USB:** Freier Port für Dashcam, Chigee AIO-5 Display, Garmin Zūmo oder Reifendruck-Empfänger |
| **`J7`** | **USB-C SMD**<br>(16-Pin) | All | `USB-C Standard` | USB 2.0 + VBUS | **Wasserdichter Service-Port:** Bündig in der rechten Gehäuseflanke mit TPU-Stopfen (Flashen & WebSerial Diagnose) |
| **`J8`** | **JST-PH 2-Pin**<br>(2.0 mm) | 1<br>2 | `VCC_5V`<br>`GND` | +5V geschaltet (1.5A)<br>Power-Masse | **Action-Cam Power:** 5V-Speisung für Helm- oder Verkleidungskamera (GoPro / Insta360), schaltet mit Zündung |
| **`J9`** | **JST-PH 3-Pin**<br>(2.0 mm) | 1<br>2<br>3 | `+12V_PROT`<br>`BSD_LEFT_N`<br>`BSD_RIGHT_N` | +12V Daueranode<br>Kathode Links (Low-Side)<br>Kathode Rechts (Low-Side) | **Spiegel-Warn-LEDs (Totwinkel-Radar):** Y-Kabel zu den Rückspiegel-LEDs, geschaltet via Dual-MOSFET `Q1` |
| **`J10`** | **JST-PH 2-Pin**<br>(2.0 mm) | 1<br>2 | `+12V_PROT`<br>`GND` | +12V geschaltet (1.5A)<br>Power-Masse | **Qi Wireless Charging Head:** Speist SP Connect / Quad Lock Induktivlader (0.0 µA Ruhestrom bei Zündung AUS) |
| **`J11`** | **JST-PH 2-Pin**<br>(2.0 mm) | 1<br>2 | `+12V_AUX`<br>`GND` | +12V geschaltet (2.0A)<br>Power-Masse | **Zusatzscheinwerfer / Strobe:** Schaltstufe für Nebelscheinwerfer oder High-Beam Signal |
| **`J12`** | **JST-SH 4-Pin**<br>(1.0 mm) | 1<br>2<br>3<br>4 | `GND`<br>`VCC_3V3`<br>`I2C_SDA`<br>`I2C_SCL` | Masse (0V)<br>+3.3V Power Out<br>I2C Datenleitung<br>I2C Taktleitung | **Qwiic / STEMMA QT Sensor-Bus:** Steckverbindung zum SAM-M10Q GNSS-Modul sowie TMP117 / OPT3001 Sensoren |
| **`ANT_UWB`**| **U.FL Hirose** | 1<br>2 | `UWB_RF_CH5`<br>`GND` | 6.5 GHz RF (50 Ohm)<br>Schirmmasse | **UWB Flex-Antenne:** 20 mm U.FL Kabel zur Taoglas FXUWB10 Antenne in der Gehäuseboden-Bucht |

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
* **100 % Lötfreie Induktionsspulen-Montage (`J_QI`):**
  * Die 28-mm-Qi-Empfängerspule wird über einen ultrakompakten **2-poligen JST-ACH SMD-Header (`J_QI`)** vibrationsfest angesteckt.
  * Beim Zusammenbau sind keinerlei manuelle Lötarbeiten erforderlich.

---

## 10. PCBA 08: 77 GHz mmWave Radar Sub-MCU & Warnflügel (`openmotorbridge_radar_submcu`)

![PCBA 08 Radar 2.0 Sub-MCU & Warnflügel 3D](../images/pcba/pcba08_radar_submcu_3d.png)

*Abbildung 7.8: 3D-CAD-Ansicht der PCBA 08 mit symmetrischem 115 x 65 mm Flügelkörper, zentralem 61 x 51 mm Radardurchbruch für das Wheeltec MR20 mmWave Radar, 36x WS2812B-2020 LEDs, ESP32-C5 Sub-MCU und integriertem Qorvo DW3110 UWB Transceiver.*

### 10.1 Technische Platinen-Kenndaten & All-UWB Backbone
* **Abmessungen:** $115{,}0 \times 65{,}0 \times 1{,}6\,\text{mm}$ (2 Lagen FR-4 High-TG150, ENIG-Goldfinish).
* **Zentraler Radardurchbruch:** $61{,}0 \times 51{,}0\,\text{mm}$ rechteckiges Sichtfenster für das Wheeltec MR20 77-GHz-Sensormodul.
* **Bestückung & HF-Architektur (Strikt 2x U.FL, kein 2.4 GHz am Heck):**
  * Espressif `ESP32-C5` Dual-Band RISC-V SoC: Dient als Sub-MCU und 5.9 GHz V2X-Uplink (C-V2X / ITS-G5 802.11p) über dedizierte U.FL-Buchse `U.FL_5G9_V2X` an Taoglas FXP524 Flexantenne.
  * **WICHTIGER HF-GRUNDSATZ:** Das 2.4-GHz-HF-Frontend des ESP32-C5 (Wi-Fi/BLE) ist am Heck **strikt deaktiviert bzw. unbeschaltet**. Am Heck existiert **keine 2.4 GHz Antenne**, um HF-Kollisionen und Intermodulationsprodukte mit OMM 2.4 GHz und Cardo/Sena-Pods am Bike vollständig zu eliminieren.
  * Qorvo `DW3110` Ultra-Wideband Transceiver (`U3`) mit U.FL-Buchse `J4` für eine Taoglas FXUWB10 Flexantenne (6.5 GHz UWB Kanal 5/9). Sämtliche Radar-Rohdatenvektoren werden drahtlos über UWB an die Zentralbox gestreamt (**Null Kupfer-Datenleitungen zum Fahrzeug**).
  * **HF-Gesamtübersicht PCBA 08:** Genau **2x U.FL HF-Buchsen** (`J4` für 6.5 GHz UWB, `U.FL_5G9_V2X` für 5.9 GHz V2X). Das Wheeltec MR20 77-GHz-Radar verfügt über integrierte Antenna-on-Package (AoP) Patch-Antennen auf der Sensor-Frontseite und benötigt keine externen HF-Koaxialleitungen.
  * 36x SMD `WS2812B-2020` RGB-LEDs auf den symmetrischen Warnflügeln (18 links / 18 rechts).
* **Steckverbinder & Wartung:**
  * `J1`: Wasserdichter 2-poliger 12V Automotive-Stecker (JST JWPF) für Zuleitung (`RADAR_PWR_12V` / `RADAR_GND`). Der frühere Binder M5 Stecker entfällt ersatzlos.
  * `J2`: 4-Pin JST-SH Header zum Wheeltec MR20 mmWave Radar (UART1 @ 115.200 Baud).
  * `J3`: **90° gewinkelte 4-Pin Stiftleiste (`3V3`, `TX`, `RX`, `GND`)** bündig an der seitlichen Gehäusekante für bequemes Flashen und Firmware-Debugging des ESP32-C5 ohne Ausbau der Platine.
* **Autonome Notfall-Strobe-Steuerung:**
  * Erkennt der lokale ESP32-C5 einen herannahenden Auffahrunfall (Time-to-Collision $\text{TTC} < 1{,}5\,\text{s}$), löst er den hochfrequenten Notfall-Strobe der 36 LEDs **lokal in $< 1\,\text{ms}$** aus - völlig unabhängig vom Funkverkehr zur Zentralbox.

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
   * `J_HELMET`: 6-Pin JST-SH 1.0mm SMD Horizontal-Header (`SM06B-SRSS-TB`) auf `B.Cu` ($X=126{,}625, Y=99{,}75\,\text{mm}$ in KiCad bzw. $X_{\text{mod}} = 60{,}6\,\text{mm}$) im hinteren Gehäuseabteil gegenüber USB-C. Führt reines, brummfreies Audio ins Helminnere.
   * `BAT1`: 2-polige JST-SH Micro-Buchse (`BM02B-SRSS-TB`) zum 1S LiPo Pouch-Akku (600 mAh mit integriertem PCM).

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

Der stirnseitige USB-C Port `J1` (`TYPE-C-31-M-12_IP67`) dient als universelle Schnittstelle für **Laden**, **WebUSB/DFU-Flashing** und den **Kassetten-Einschubkontakt**:

| USB-C Pins | Netzname | Signal-Typ | Funktion / Adapter-Verbindung |
| :---: | :--- | :--- | :--- |
| **A1, B12, A12, B1, SH** | `GND` / `PGND` | Power Ground | Pin 1 Kassetten-Header `J_AUDIO_PWR` & Schirmung: Führt Lade- & Betriebs-Rückstrom |
| **A4, B9, A9, B4** | `VBUS_5V` | Power In (+5V) | Pin 2 Kassetten-Header & USB-Ladekabel: 5V Speisung & BQ24075 USV-Akkuladung |
| **A6, B6 (`DP1`, `DP2`)** | `USB_DP` | USB 2.0 PHY | ESP32-C6 GPIO 13 (via TVS `D2`): **Nativer USB D+ für WebUSB / DFU Firmware-Flashing** |
| **A7, B7 (`DN1`, `DN2`)** | `USB_DN` | USB 2.0 PHY | ESP32-C6 GPIO 12 (via TVS `D2`): **Nativer USB D- für WebUSB / DFU Firmware-Flashing** |
| **A5 (`CC1`)** | `HP_OUT_L` | Audio Out | Pin 4 Kassetten-Header: Stereo Audio Links vom ES8388 `LOUT1` im Kassetten-Betrieb |
| **B5 (`CC2`)** | `HP_OUT_R` | Audio Out | Pin 5 Kassetten-Header: Stereo Audio Rechts vom ES8388 `ROUT1` im Kassetten-Betrieb |
| **A8 (`SBU1`)** | `MIC_IN+` | Audio In | Pin 7 Kassetten-Header: Mikrofonsignal zum ES8388 `MIC1P` im Kassetten-Betrieb |
| **B8 (`SBU2`)** | `AGND_SPK` | Analog Ground | Pin 3 & 6 Kassetten-Header: Stromloser Audio-Massebezug ($I = 0\,\text{mA}$) |

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
     - **PMR/DMR HF-Pfad:** Der HF-Ausgang des NiceRF SA818-DMR speist über ein Tiefpass-/Bandpassfilter die U.FL-Buchse `J_RF` (`B.Cu`) sowie das parallele Lötpad `PAD_ANT` (`F.Cu`) am oberen Platinenrand ($X = 110{,}5, Y = 87{,}0\,\text{mm}$).
     - Ein kurzes $50\,\text{mm}$ Mikro-Koaxialpigtail (RG-178 / 1.13mm) führt von `J_RF` zur wasserdichten SMA-Bulkhead-Buchse (IP67 mit EPDM O-Ring) an der Gehäusestirnseite.
     - **Helm-Default:** Im Helmbetrieb wird die $48\,\text{mm}$ kurze 446 MHz Wendel-Stummelantenne aufgeschraubt (ca. $0\dots +1{,}5\,\text{dBi}$, $1{,}5\dots 2{,}5\,\text{km}$ Reichweite). Im Kassettenbetrieb im Pod führt ein Koaxialkabel zur Außenantenne am Motorrad ($3\dots 6\,\text{km}$).
     - **Bluetooth Co-Prozessor (`U6`):** Der `ESP32-PICO-V3-02` arbeitet auf seine eigene Johanson 2450AT Keramik-Chipantenne (`ANT1`) für Nahfeld-Kopplungen.
6. **Bedienelemente & Steckverbinder:**
   * 4x taktile Mikrotaster (`SW1` bis `SW4`): PTT (Push-to-Talk / MFB), Mode (Analog/DMR Toggle), Ch+, Ch-.
   * 1x WS2812B-2020 RGB Status-LED (`D1`, RX Grün, TX Rot, DMR Blau, Chg Gelb).
   * `J1`: Wasserdichte IP67 USB-C Buchse (16-Pin) für 5V Laden, WebUSB DFU und Kassetten-Einschub.
   * `J_HELMET`: 6-Pin JST-SH 1.0mm SMD Horizontal-Header (`SM06B-SRSS-TB`) auf `B.Cu` ($X=126{,}625, Y=99{,}75\,\text{mm}$ in KiCad) – identische Belegung und Platzierung wie PCBA 09.
   * `BAT1`: 2-polige JST-SH Micro-Buchse (`BM02B-SRSS-TB`) zum 1S LiPo Pouch-Akku (600 mAh mit integriertem PCM).

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
