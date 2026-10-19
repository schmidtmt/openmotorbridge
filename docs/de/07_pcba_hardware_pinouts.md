# 07 - Hardware-Architektur & Platinen-Pinouts (Das bereinigte 7-PCBA-Lineup)

Dieses Dokument bildet die **zentrale, autoritative Hardware-Spezifikation aller 7 aktiven Platinen-Baugruppen (`PCBA 01`, `03`, `05`, `07`, `08`, `09`, `10`)** des OpenMotorBridge Gesamtsystems (v9.6 Clean All-UWB Architecture), einschließlich Lagenaufbau, Impedanzkontrolle, Net-Klassen, Funktionszonen und vollständigen Pinout-Tabellen.

---

## 1. Systemübersicht des 5-Platinen-Lineups

Das Hardwaredesign von OpenMotorBridge folgt dem Grundsatz der radikalen Entflechtung: Daten- und Audioströme werden zu 100 % drahtlos über ein synchrones Ultra-Wideband-Backbone (UWB 6.5 GHz) geführt, während der fahrzeuggebundene Kabelbaum auf reine 2-Draht-Gleichspannung (12V DC) und CAN-Bus reduziert ist.

```
+----------------------------------------------------------------------------------------+
|                   DAS 7-PLATINEN-LINEUP DER OPENMOTORBRIDGE v9.6                       |
+-------+-------------------------------+---------------+---------+----------------------+
| Baugruppe | Name & Funktion           | Platinenmaße  | Lagen   | Kern-ICs / Bauteile  |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 01**| **Zentralbox Main Controller** | 85 x 55 mm    | 4 Lagen | ESP32-S3, QCC3084 BT,|
|       | (Unter der Sitzbank, Audio/USV)| (77x47 mm M3) | (ENIG)  | LM5164, BQ24075,     |
|       |                                |               |         | ES8388, SX1262 LoRa, |
|       |                                |               |         | DW3110 UWB, DTM-12   |
+-------+-------------------------------+---------------+---------+----------------------+
| **PCBA 03**| **Universal Smart Cartridge** | 35 x 25 mm    | 4 Lagen | Qorvo DW3110 UWB,    |
|       | (Kassettenträger Bucht 1 & 2) | (29x19 mm M2) | (ENIG)  | ESP32-C6, ES8388,    |
|       |                                | 2-seitig SMT  |         | TS5A3159, 4x AO3400A |
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
   * **`PCBA 02` (Pod-Basisplatine):** Ersatzlos gestrichen. Die Zuleitung führt direkt auf einen werkzeuglos verriegelnden IP67 2-Pin Blade-Direktstecker (`CON_POD_DC`) mit axialem NBR70 O-Ring und Edelstahl-U-Clip in der Schottwand des monolithischen Pod-Gehäuses.
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
2. **Direkte 2-Draht DC-Blade-Kontaktierung:** Die 2-adrige DC-Leitung vom Deutsch DTM-12 Stecker führt über einen werkzeuglos verriegelnden IP67 2-Pin Blade-Direktstecker (`CON_POD_DC`) mit axialem NBR70 O-Ring und Edelstahl-U-Clip durch die Gehäuserückwand direkt in den Schacht (100 % lötfrei) und kontaktiert formschlüssig in die werkseitig bestückte Dual-Beam Schlitzbuchse `J_DC_IN` auf `PCBA 03`.
3. **Null Ausfallrisiko:** Keine Schalter, keine aktiven ICs und keine empfindlichen Buchsen im Spritzwasserbereich der Kofferträger.

---

## 5. PCBA 03: Universal Smart Cartridge (`openmotorbridge_pod_cartridge` Rev 3.0)

![PCBA 03 Universalschlitten Cartridge Top 3D](../images/pcba/pcba03_pod_cartridge_3d.png)
*Abbildung 7.3a: KiCad 3D-Render der Universal Smart Cartridge Top (PCBA 03 Rev 3.0, 35 x 25 mm) mit ESP32-C6 Host-MCU, 4x AO3400A MOSFETs und J_ACT Mechatronik-Header.*

![PCBA 03 Universalschlitten Cartridge Bottom 3D](../images/pcba/pcba03_pod_cartridge_bottom_3d.png)
*Abbildung 7.3b: KiCad 3D-Render der Universal Smart Cartridge Bottom mit Qorvo DW3110 UWB Transceiver, ES8388 Stereo-Codec und Audio-Power-Header J_AUDIO_PWR.*

### 5.1 Technische Platinen-Kenndaten & Funktionale Lagen-Aufteilung
* **Abmessungen:** $35{,}0 \times 25{,}0\,\text{mm}$ (Raster $29{,}0 \times 19{,}0\,\text{mm}$ mit 4x M2 Befestigungsbohrungen H1..H4).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 (JLC04161H, $1{,}2\,\text{mm}$ Dicke, durchgehende GND-Plane L2 und Power-Plane L3, ENIG-Goldfinish).
* **Bestückung Top-Layer (F.Cu - Mechatronik, Host-MCU & Steuerung):**
  * `U1`: Espressif `ESP32-C6-MINI-1U` RISC-V Host-MCU (verwaltet Kassetten-Profile, UWB-Backbone, I2S-Codec-Steuerung, USB-Audio und Aktuator-Timings).
  * `Q1` - `Q4`: 4x N-Kanal MOSFETs (`AO3400A`, SOT-23, $30\,\text{V} / 5{,}7\,\text{A}$) samt Freilaufdioden `D1`-`D4` (`1N4148WS`, SOD-323). Platziert unmittelbar neben Header `J_ACT` für kürzeste Leiterbahnwege zu den Taster-Aktuatoren.
  * `R1` - `R4`: $100\,\Omega$ Gate-Serienwiderstände (0603).
  * `R5` - `R8`: $100\,\text{k}\Omega$ Gate-Pulldowns (0603) für definierten Ruhezustand.
  * `R9`: $10\,\text{k}\Omega$ Pull-up-Widerstand (0603) an `VCC_3V3` für das Kassetten-Erkennungssignal `OMM_DETECT`.
  * `J_ACT`: 8-poliger $1{,}0\,\text{mm}$ JST-SH Header (`BM08B-SRSS-TB` mit vertikalem Top-Entry-Anschluss und SMD-Schirmlaschen `MP` an GND) zur Ansteuerung der 4 Miniatur-Hubmagnete.
  * `J_AUDIO_PWR`: 8-poliger $1{,}0\,\text{mm}$ JST-SH Header (baugleich zu `J_ACT`, `BM08B-SRSS-TB` mit vertikalem Top-Entry-Anschluss, Schirmlaschen `MP` an GND) zur sternpunktförmigen Kelvin-Audio- und Power-Anbindung des jeweiligen OEM-Headsets bzw. OMM-Moduls.
  * `J_PROG`: 4-poliger $1{,}27\,\text{mm}$ SMD-Stiftleisten-Header (`PinHeader_1x04_P1.27mm_Vertical_SMD_Pin1Left`) für Flashen und Firmware-Recovery (`VCC_3V3`, `USB_DP`, `GND`, `PTT_USB_N`).
* **Bestückung Bottom-Layer (B.Cu - HF, Audio-Codec, Hardware-Umschaltung & Stromaufnahme):**
  * `U_UWB`: Qorvo `DW3110` Ultra-Wideband Transceiver (6.489 GHz Ch. 5, QFN-16-1EP) mit externer U.FL-Koaxialbuchse `ANT_UWB` (`Taoglas FXUWB10`) und hochpräzisem $38{,}4\,\text{MHz}$ Quarz `Y_UWB`. Strahlungsrichtung zeigt nach unten durch den dielektrischen Kunststoffboden der Kassette für optimale Funkverbindung zur Zentralbox.
  * `U3`: Everest Semi `ES8388` 24-Bit / 48 kHz Low-Noise Audio-Codec (QFN-28-1EP). Bewusst auf der **Unterseite (`B.Cu`)** platziert: Dadurch sind die empfindlichen analogen Audioleitungen durch die interne Kupfer-Massefläche hermetisch von den steilen Schaltflanken der Top-Layer-MOSFETs (`Q1`–`Q4`) und Aktuatorströmen entkoppelt. Wandelt das analoge Mikrofon- und Lautsprechersignal von Sena, Cardo oder Midland direkt auf der Kassette und streamt es jitterfrei digital via I2S/UWB.
  * `U4`: Texas Instruments `TS5A3159DBVR` Single-Pole Double-Throw (SPDT) Analog/Digital-Audio-Umschalter ($0{,}5\,\Omega$ Durchgangswiderstand, SOT-23-6). Ermöglicht die automatische, hardware-gesteuerte Umschaltung zwischen analogem Headset-Audio und digitalem OMM-USB-Audio.
  * `J_DC_IN`: Stirnseitige, werkseitig SMT-bestückte 2-polige Dual-Beam Automotive Flachstecker-Schlitzbuchse (10.0mm Pitch, 5A, IP2X fingersicher, liegende Montage auf B.Cu) für die formschlüssige Aufnahme der Klingen des IP67-Direktsteckers (`CON_POD_DC`) des Pod-Schachts (`Pin 1: +5V_IN`, `Pin 2: GND`). Vollkommen immun gegen Mikrounterbrechungen bei Vibrationen.
  * `F1`: Selbstrückstellende 500mA PPTC-Sicherung (Bourns `MF-MSMF050-2`, 1812 SMD) vor `VCC_5V_PROT`.
  * `C1`, `C2`: Keramische Stützkondensatoren ($100\,\text{nF}$ 0603 / $10\,\mu\text{F}$ 0805) an `VCC_3V3`.
  * `H1` - `H4`: 4x M2-Montagebohrungen mit durchkontaktiertem Pad (`MountingHole_2.2mm_M2_Pad`) an Systemmasse (`GND`).

### 5.2 Pinbelegung des Audio-Power-Headers (`J_AUDIO_PWR` / 8-Pin JST-SH 1.0mm) & Dual-Mode Umschaltung

Um sowohl **analoge OEM-Headsets (Sena, Cardo, Midland)** störungsfrei mit Kelvin-Massen anzubinden als auch **native OMM-Module (PCBA 09 / PCBA 10)** verlustfrei digital über denselben Steckverbinder zu betreiben, ist `J_AUDIO_PWR` als **Dual-Mode-Schnittstelle** mit automatischer Hardware-Umschaltung über `U4` (`TS5A3159DBVR`) und Pull-Up-Widerstand `R9` ($10\,\text{k}\Omega$ an `VCC_3V3`) ausgeführt:

| Pin | Signalname | Richtung | Funktion: Analog-Intercom (Sena / Cardo / Midland) | Funktion: Digital-OMM (PCBA 09 / PCBA 10) |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **`PGND` / `GND`** | Power Return | **Leistungs-Masse:** Rückstrom Lader / DC-DC ($0{,}2\dots 0{,}6\,\text{A}$) | **Leistungs-Masse:** Rückstrom Lader & HF-Endstufe ($0{,}2\dots 0{,}6\,\text{A}$) |
| **2** | **`VCC_5V_PROT`** | Power Out | Geregelte, abgesicherte +5V Speisung für Headset-Akku/Lader | Geregelte, abgesicherte +5V Speisung für OMM BQ24075 PMIC |
| **3** | **`AGND_AUDIO_IN`** | Audio GND | **Saubere Kopfhörermasse:** 3.5mm Sleeve – **stromlos ($I = 0\,\text{mA}$)!** | Nicht belegt (N/C) oder Koax-Schirmung (stromlos!) |
| **4** | **`AUDIO_IN_L`** | Audio In $\leftarrow$ | Line-Out Lautsprecher Links vom Headset zum ES8388 ADC | Nicht belegt (N/C) |
| **5** | **`AUDIO_IN_R`** | Audio In $\leftarrow$ | Line-Out Lautsprecher Rechts vom Headset zum ES8388 ADC | Nicht belegt (N/C) |
| **6** | **`OMM_DETECT`** | Control In $\leftarrow$ | **GND-Brücke im Kabelbaum (0V):** Hält `U4` in Ruhestellung (NC) | **Offen / N/C:** `R9` zieht auf HIGH ($3{,}3\,\text{V}$) $\rightarrow$ schaltet `U4` auf Digital-USB (NO) |
| **7** | **`AUDIO_IO_P`** | Dual-Mode I/O | **Analog `VOICE_OUT` (via U4 NC):** Sprache vom ES8388 DAC $\rightarrow$ OEM Mic | **Digital `USB_DP` (via U4 NO):** Nativer digitaler USB-Audio-Datenstrom D+ |
| **8** | **`PTT_USB_N`** | Dual-Mode I/O | **PTT_IO:** Push-to-Talk Tastung gegen Masse (Midland PMR446 / N/C) | **Digital `USB_DN`:** Nativer digitaler USB-Audio-Datenstrom D- |
| **MP** | **`GND`** | Schirmung | Beidseitige SMD-Montagelaschen des JST-SH Steckers auf GND-Plane | Beidseitige SMD-Montagelaschen des JST-SH Steckers auf GND-Plane |

> [!IMPORTANT]
> **Funktionsweise der automatischen Audio-Umschaltung via `U4` (`TS5A3159DBVR`):**
> 1. **Kassette mit Analog-Intercom (Sena SPIDER X Slim / Cardo Packtalk Edge / Midland):**  
>    Der Adapterkabelstrang überbrückt Pin 6 (`OMM_DETECT`) intern mit Masse (GND Pin 1 oder Pin 3). Der Umschalter `U4` verbleibt in Ruhestellung (**NC**): Pin 7 (`AUDIO_IO_P`) ist direkt mit dem Analogausgang `VOICE_OUT` des ES8388 Audio-Codecs verbunden. Die Sprachübertragung erfolgt vollkommen latenzfrei ($< 0{,}4\,\text{ms}$) analog in das Mikrofon des Headsets.
> 2. **Kassette mit nativem OMM-Modul (`PCBA 09` Mesh / `PCBA 10` 446 PMR/DMR):**  
>    Das 4-polige USB-C-Kabel (VBUS, GND, D+, D-) lässt Pin 6 (`OMM_DETECT`) unbeschaltet (**N/C**). Der $10\,\text{k}\Omega$-Pull-up-Widerstand `R9` auf `PCBA 03` zieht den Steuereingang IN von `U4` automatisch auf HIGH ($3{,}3\,\text{V}$). Der SPDT-Schalter `U4` schaltet in $< 35\,\text{ns}$ auf Arbeitskontakt (**NO**): Pin 7 wird von der analogen Audioleitung getrennt und direkt mit der nativen USB-Leitung `USB_DP` der ESP32-C6 Host-MCU verbunden. Zusammen mit Pin 8 (`PTT_USB_N` als `USB_DN`) entsteht ein vollwertiger, verlustfreier digitaler USB-2.0-Audiokanal direkt zwischen Intercom-Engine und OMB-Gateway. Mechatronik-Stößel, Wandlerverluste und analoge Brummschleifen entfallen vollständig!


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
* **Abmessungen:** $82{,}0 \times 50{,}0\,\text{mm}$ (Gehäuseaußenmaß $98 \times 68 \times 25\,\text{mm}$ im geschlossenen IP68-Monocoque-Gehäuse).
* **Lagenaufbau:** 4 Lagen FR-4 High-TG150 ($1{,}6\,\text{mm}$, ENIG-Goldfinish).
* **Top-Layer:** ESP32-S3 Controller, Microchip USB2514B USB-Hub (konfiguriert für 2 Downstream-Ports: Smartphone Fast-Charge PD 20W & CP2AA Dongle), Knowles SPH0645LM4H I2S MEMS Akustiksensor, WS2812B-2020 RGB-LED und 5 GHz Wi-Fi Anbindung für Headless CarPlay / Android Auto.
* **Bottom-Layer:** Qorvo DW3110 UWB Transceiver (6.489 GHz Ch. 5), TI LMR36015 Buck (5V System-Bus), einzelner Southchip SC8102 (oder SW3526) USB-PD 20W Fast-Charger (`U5` für Smartphone am Lenker bzw. Handschuhfach), TI TPS2051B Lastschalter für automatischen Dongle-Kaltstart und Auto-Café-Modus.
  *(Hinweis zur Konsolidierung: Der frühere zweite 20W-Ladekreis `U8` samt Spule `L3` für Handschuhfach-MP3 entfällt ersatzlos. Für Sonderanwendungen mit mehreren Geräten im Handschuhfach wird ein Standard COTS Mini-Hub mit PD-Passthrough genutzt).*

### 7.2 Die 2-Kabelbaum-Architektur & Steckverbinder (`J_COCKPIT`, `J_VEHICLE`, `J12`)

Anstelle von 12 einzelnen Steckverbindern an den Gehäuseflanken setzt der Universal Front-Knoten in v9.6 auf eine hochintegrierte **2-Kabelbaum-Architektur mit modularen Satelliten-Verteilern („Lego-Prinzip“)**. 

Auf der Platine sitzen genau **zwei robuste Haupt-Steckverbinder** (2,0 mm Raster, zweireihig mit Verriegelung) für die abgehenden Mantelleitungen sowie der externe Sensorbus:

```
                       [ PCBA 05 FRONT NODE PLATINE ]
     ┌─────────────────────────────────────────────────────────────┐
     │                                                             │
     │   [ J_COCKPIT ]                             [ J_VEHICLE ]   │
     │   (14-Pin Dual-Row 2.0 mm)                  (8-Pin 2.0 mm)  │
     │                                                             │
     │   • USB Upstream Host (Boom! Box)           • 12V In & GND  │
     │   • CP2AA Wireless Dongle                   • CAN-Bus       │
     │   • Smartphone USB-PD 20W                   • Spiegel-LEDs  │
     │   • PTT-Lenkertaster & Action-Cam           • Aux-Licht     │
     │                                                             │
     │   [ J7 ] USB-C Service-Port (Flanke)                        │
     │   [ J12 ] JST-SH 4-Pin Qwiic Sensorbus (SAM-M10Q GNSS)      │
     │   [ ANT_UWB ] U.FL 6.5 GHz Transceiver-Port                 │
     └─────────────────────────────────────────────────────────────┘
```

#### 7.2.1 Belegung Cockpit- & USB-Header (`J_COCKPIT` / 16-Pin Dual-Row 2.0 mm)

Fasst alle Cockpit-, Multimedia- und Lenker-Signale in einem einzigen, geschirmten Mantelkabel ($\varnothing 6{,}0\,\text{mm}$) zusammen, das zur **Cockpit-Verteilerleiste** führt:

| Pin | Signalname | Signalpegel / Richtung | Funktion & angeschlossene Cockpit-Peripherie |
| :---: | :--- | :--- | :--- |
| **1** | `USB_UP_VBUS` | +5V VBUS In | USB Upstream Host: Verbindung zum OEM-Motorrad-Infotainment (Harley Boom! Box / Skyline OS) |
| **2** | `USB_UP_DM` | USB 2.0 D- | D- Datenleitung zum Host-Infotainment |
| **3** | `USB_UP_DP` | USB 2.0 D+ | D+ Datenleitung zum Host-Infotainment |
| **4** | `GND` | Masse (0V) | Signal-Masse für Upstream Host |
| **5** | `VCC_5V_OTTOCAST` | +5V geschaltet (1.5A) | CP2AA Wireless Dongle: Stromversorgung mit Kaltstart-Reset via TPS2051B (unabhängig von Cam/Navi) |
| **6** | `USB_DN2_DM` | USB 2.0 D- | D- Datenleitung zum CP2AA Wireless CarPlay / Android Auto Dongle |
| **7** | `USB_DN2_DP` | USB 2.0 D+ | D+ Datenleitung zum CP2AA Wireless CarPlay / Android Auto Dongle |
| **8** | `GND` | Masse (0V) | Signal-Masse für CP2AA Dongle |
| **9** | `VBUS_PD_OUT` | +5V / +9V / +12V Out | Smartphone Fast-Charge PD 20W: Speisung via SC8102 / SW3526 Regler `U5` |
| **10**| `USB_DN1_DM` | USB 2.0 D- | D- Datenleitung Smartphone Fast-Charge Port |
| **11**| `USB_DN1_DP` | USB 2.0 D+ | D+ Datenleitung Smartphone Fast-Charge Port |
| **12**| `USB_DN1_CC` | Configuration Channel | USB-C CC-Leitung für PD 3.0 / QC4+ Aushandlung |
| **13**| `PGND` | Power-Masse | Hochstrom-Rückleitung für 20W USB-PD Ladekreis |
| **14**| `PTT_IN1_N` | Digital In (Pull-Up) | Lenkertaster: PTT Intercom Gruppenfunk / Voice-Assistent (Active-Low) |
| **15**| `VCC_5V_AUX` | +5V geschützt (bis 2.0A)| Power-Only Speisung für Action-Cam & 5V-Navi via TPS54302 3A-Buck & PPTC |
| **16**| `GND` | Power-Masse | Masse-Rückleitung für Action-Cam & 5V-Navi |

#### 7.2.2 Belegung Fahrzeug- & Bordnetz-Header (`J_VEHICLE` / 12-Pin Dual-Row 2.0 mm)

Fasst alle Stromversorgungs-, Bus-, Sensor- und Signalleitungen in einem zweiten, abgedichteten Mantelkabel ($\varnothing 6{,}0\,\text{mm}$) zusammen, das zur **Fahrzeug-Verteilerbox** führt:

| Pin | Signalname | Signalpegel / Richtung | Funktion & angeschlossene Bordnetz-Peripherie |
| :---: | :--- | :--- | :--- |
| **1** | `KL15_12V_SW` | +9V...+16V In | 12V Bordnetzspeisung: Zündungsplus (Standlicht / BMW Cartool-Stecker / Harley Neck) |
| **2** | `GND` | Power-Masse | Zentrale Versorgungs-Masse des Front-Knotens |
| **3** | `CAN_H` | CAN-FD High | Fahrzeug-CAN-Bus: Direkter Abgriff im Cockpit / Diagnosestecker mit TCAN334G & CPC1017N |
| **4** | `CAN_L` | CAN-FD Low | Fahrzeug-CAN-Bus: Differenzielle Datenleitung Low |
| **5** | `+12V_PROT` | +12V Daueranode | Gemeinsame geschützte Anodenspeisung für Totwinkel-Spiegel-LEDs (BSD) |
| **6** | `BSD_LEFT_N` | Kathode Links (Low-Side) | Geschaltete Masse für linke Spiegel-Totwinkel-Warnleuchte (Dual-MOSFET `Q1`) |
| **7** | `BSD_RIGHT_N`| Kathode Rechts (Low-Side)| Geschaltete Masse für rechte Spiegel-Totwinkel-Warnleuchte (Dual-MOSFET `Q1`) |
| **8** | `+12V_AUX` | +12V geschaltet (2.0A) | Zusatzscheinwerfer / Strobe oder 12V-Navi-Aktivhalterung (Garmin Zūmo XT2 / BMW Cradle) via TI TPS1H100 `Q2` |
| **9** | `+3V3_SENS` | +3.3V geschützt Out | Speisung für externen GNSS- & Klima-Sensor-Puck (u-blox SAM-M10Q, TMP117, OPT3001) |
| **10**| `GND` | Sensor-Masse | Masse-Rückleitung für I2C-Sensorbus |
| **11**| `I2C_SDA` | I2C Data (3.3V) | Bidirektionale I2C-Datenleitung mit 4.7k Pull-Up für Sensor-Puck am Verkleidungsschnabel |
| **12**| `I2C_SCL` | I2C Clock (3.3V) | I2C-Taktleitung (100 / 400 kHz) |

#### 7.2.3 Lokale Ports & Service-Schnittstellen

| Header | Typ | Signalname | Funktion & Besonderheiten |
| :--- | :--- | :--- | :--- |
| **`J7`** | **USB-C SMD (16-Pin)** | `USB 2.0 + VBUS` | Wasserdichter Service-Port: Bündig in rechter Gehäuseflanke mit TPU-Stopfen (Flashen & WebSerial) |
| **`ANT_UWB`**| **U.FL Hirose (SMD)** | `UWB_RF_CH5, GND` | 6.5 GHz UWB HF-Verbindung (50 Ohm) zur Taoglas FXUWB10 Flex-Antenne im Gehäuseboden |

---

### 7.2.4 Die modularen Satelliten-Verteiler („Lego-Prinzip“)

Die abgehenden Mantelleitungen von `J_COCKPIT` und `J_VEHICLE` münden in zwei kompakte, spezialisierte Satelliten-Verteiler:

1. **Cockpit-Verteiler (USB-C Leiste mit mechanischer Zug-Sicherung):**
   * Bietet 5 standardisierte, klar laserbeschriftete **USB-C Buchsen**:
     - `[ PHONE 20W ]`: Fast-Charge PD 20W + USB 2.0 Daten für Smartphone (oder Handschuhfach mit optionalem Mini-Hub).
     - `[ DONGLE ]`: 5V geschaltet (1.5A mit TPS2051B Kaltstart-Reset) + USB 2.0 Daten für Ottocast/Carlinkit CP2AA.
     - `[ HOST ]`: 5V VBUS In + USB 2.0 Daten zum OEM-Motorrad-Infotainment (Harley Boom! Box GTS / Skyline OS) oder zum Standalone Smart-Screen (Carpuride W502/W702, Chigee AIO-5).
     - `[ CAM 5V ]`: **Power-Only** USB-C (5V bis 2A, BC 1.2 DCP mit D+/D- gebrückt). Verhindert, dass Action-Cams (GoPro, Insta360) in den PC-Massenspeicher- oder Webcam-Modus wechseln.
     - `[ NAVI 5V ]`: **Power-Only** USB-C (5V bis 2A, BC 1.2 DCP) für USB-betriebene Navis (Garmin, TomTom, Beeline). *(Hinweis: Für 12V-Aktivhalterungen wie Garmin Zūmo XT2 oder BMW Cradle erfolgt die Speisung direkt über `+12V_AUX` am Fahrzeug-Satelliten).*
   * **PTT-Klemme:** 2-polige Schraub-/Federklemme für den Intercom-Gruppenfunk-Lenkertaster (`PTT_IN1_N` gegen `GND`).
   * **Integrierte Klemme:** Eine 3D-gedruckte Klemmleiste mit 2 Schrauben fixiert die Steckerhälse handelsüblicher COTS-USB-C-Kabel vibrationsfest und dient als vollwertige Zugentlastung.
   * Der Endkunde kann jedes beliebige Standard-USB-C-Kabel (20 cm, gewinkelt, Textilmantel etc.) werkzeuglos einstecken.
2. **Fahrzeug-Verteiler (Spritzwassergeschützte 5-Port Steckerbox):**
   * Beinhaltet kompakte, codierte COTS-Klick-Steckverbinder (JST-JWPF IP67 / JST-SM / Qwiic) für:
     - `[ 12V IN ]`: KL15 Zündungsplus & Power-GND (2-Pin)
     - `[ CAN BUS ]`: CAN_H, CAN_L, GND (3-Pin)
     - `[ MIRROR BSD ]`: Totwinkel-Radar-Spiegel-LEDs (3-Pin)
     - `[ AUX LIGHT ]`: Zusatzscheinwerfer / 12V-Navi-Cradle (2-Pin)
     - `[ GNSS / CLIMATE PUCK ]`: 4-Pin I2C-Steckverbindung (3V3, GND, SDA, SCL) für SAM-M10Q & TMP117 Sensor-Puck im Schnabel
   * **Wartungsvorteil:** Bei Beschädigung eines Spiegels, Scheinwerfers oder Sensors wird die Komponente in 60 Sekunden werkzeuglos abgesteckt und getauscht.
3. **Fahrzeugspezifische Flexibilität:**
   * **Adventure GS & Road King Special:** Die beiden Satelliten werden **getrennt montiert** (Cockpit-Leiste am Lenker/Windschild, Fahrzeug-Box am Rahmen/Schnabel). Dadurch wird **kein einziges unnötiges Kabel über den beweglichen Lenkkopf** geführt.
   * **Touring Fairing (Road Glide):** Beide Satelliten lassen sich über seitliche Schwalbenschwanz-Führungen mit einem Klick zu **einer einzigen Kombi-Box** vereinen und im Handschuhfach / Verkleidungsträger montieren.

### 7.3 Vollständige ESP32-S3 Controller Pinbelegung (PCBA 05 `U1`)

| Modul-Pad | Signalname | Signal-Typ | Funktion / Angeschlossene Peripherie |
| :---: | :--- | :---: | :--- |
| **Pad 1** | `GND` | Power | System-Masse |
| **Pad 2** | `VCC_3V3` | Power | +3.3V Hauptversorgung (LMR36015 / TPS7A05) |
| **Pad 3** | `ESP_EN` | Digital In | Hardware-Reset (10k Pull-Up, 100nF Entkoppelung) |
| **Pad 5** | `CAN_SILENT` | Digital Out | Hardware Listen-Only Pin für TI TCAN334G CAN-Transceiver |
| **Pad 6** | `MIC_I2S_WS` | Digital Out | I2S Word Select (LRCLK 48 kHz) für Knowles SPH0645LM4H Mikrofon (`MK1`) |
| **Pad 7** | `MIC_I2S_BCLK` | Digital Out | I2S Bit Clock (3.072 MHz) für Knowles SPH0645LM4H Mikrofon (`MK1`) |
| **Pad 8** | `PTT_IN1_N` | Digital In | Lenkertaster 1: PTT Intercom Funk / Voice (Active-Low) |
| **Pad 9** | `PTT_IN2_N` | Digital In | Lenkertaster 2: Action-Cam Bookmark / Highlight (Active-Low) |
| **Pad 10** | `PTT_IN3_N` | Digital In | Lenkertaster 3: Quick-Action / Navigationsmenü (Active-Low) |
| **Pad 12** | `MIC_I2S_DATA` | Digital In | I2S Seriendaten vom Knowles SPH0645LM4H MEMS-Mikrofon (`MK1`) |
| **Pad 13** | `USB_SERV_DM` | USB D- | Nativer USB-JTAG / CDC Service-Port (`J7`) |
| **Pad 14** | `USB_SERV_DP` | USB D+ | Nativer USB-JTAG / CDC Service-Port (`J7`) |
| **Pad 15** | `CAN_TERM_EN` | Digital Out | Steuersignal für CPC1017N Solid-State Relais (120 Ohm CAN-Busabschluss) |
| **Pad 17** | `I2C_SDA` | Open-Drain | I2C Datenleitung für `J_VEHICLE` (Pins 11/12) zum externen Sensor-Puck (SAM-M10Q, TMP117, OPT3001) |
| **Pad 18** | `I2C_SCL` | Open-Drain | I2C Taktleitung für `J_VEHICLE` (Pins 11/12) |
| **Pad 19** | `WS2812B_DIN` | Digital Out | Datenleitung für SMD WS2812B-2020 RGB Status-LED (`D4`) |
| **Pad 20** | `BSD_LED_LEFT` | Digital Out | Gate-Ansteuerung für Totwinkel-Spiegel-LED Links (`J9`, MOSFET `Q1`) |
| **Pad 21** | `BSD_LED_RIGHT`| Digital Out | Gate-Ansteuerung für Totwinkel-Spiegel-LED Rechts (`J9`, MOSFET `Q1`) |
| **Pad 22** | `AUX_LIGHT_EN` | Digital Out | Freigabesteuerung für TI TPS1H100 Smart High-Side Switch (`Q2` / `J11`) |
| **Pad 23** | `TWAI_TX` | Digital Out | CAN-Bus Sendedaten an TCAN334G Transceiver |
| **Pad 27** | `ESP_BOOT` | Digital In | Boot-Taster `SW1` (GPIO 0, Active-Low) |
| **Pad 30** | `UWB_SCK` | Digital Out | SPI Serial Clock zu Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 31** | `UWB_MOSI` | Digital Out | SPI Master-Out Slave-In zu Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 32** | `UWB_MISO` | Digital In | SPI Master-In Slave-Out von Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 33** | `UWB_CS` | Digital Out | SPI Chip-Select (Active-Low) zu Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 34** | `UWB_IRQ` | Digital In | Interrupt-Request von Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 35** | `UWB_RST` | Digital Out | Hardware-Reset zu Qorvo DW3110 UWB Transceiver (`U9`) |
| **Pad 36** | `TWAI_RX` | Digital In | CAN-Bus Empfangsdaten von TCAN334G Transceiver |
| **Pad 38** | `OTTOCAST_FAULT_N`| Digital In | Überstrom- & Thermofehler-Meldung von TPS2051B (Active-Low) |
| **Pad 39** | `OTTOCAST_PWR_EN` | Digital Out | VBUS-Schaltfreigabe für CP2AA Dongle via TPS2051B Lastschalter |
| **Pads 40-41**| `GND` | Power | Thermische Massepads (Thermal Vias zu In1.Cu) |

### 7.4 Digitales I2S-MEMS-Mikrofon `MK1` & Akustik-Bohrung

Das fahrtwindgeschützte digitale Mikrofon `MK1` (Knowles `SPH0645LM4H` im LGA-5-Gehäuse) ist bei $X = 172{,}00\,\text{mm}, Y = 82{,}25\,\text{mm}$ auf `F.Cu` platziert:
* **Akustik-Einlass:** Das Schallloch liegt auf Pad 5 und führt über eine durchkontaktierte $\varnothing 0{,}8\,\text{mm}$ Platinenbohrung direkt in den geschützten Kaltluftkanal des Frontgehäuses.
* **3D-Freigang:** Durch die Verschiebung von der Altposition `MIC1` zu `MK1` ist ein lichter Abstand von $> 3{,}5\,\text{mm}$ zum Pufferkondensator `C_BUF` und Boot-Taster `SW1` dauerhaft garantiert.
* **Signalintegrität:** Die I2S-Takt- und Datenleitungen (`MIC_I2S_BCLK`, `MIC_I2S_WS`, `MIC_I2S_DATA`) sind direkt auf Layer 1 mit flankierender Masseführung ohne Vias an den ESP32-S3 angebunden.

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

### 10.2 ESP32-C5 & DW3110 UWB Pinbelegung (PCBA 08 `U1` & `U3`)

| Modul-Pad | Signalname | Signal-Typ | Funktion / Hardware-Verbindung |
| :---: | :--- | :---: | :--- |
| **U1.1** | `GND` | Power | System-Masse |
| **U1.2** | `VCC_3V3` | Power | +3.3V geregelte Spannung von LDO `U2` (TPS7A05) |
| **U1.4** | `MR20_TX` | Digital Out | UART1 TX zu Wheeltec MR20 mmWave Radar (`J2.3`) |
| **U1.5** | `MR20_RX` | Digital In | UART1 RX von Wheeltec MR20 mmWave Radar (`J2.2`) |
| **U1.6** | `UWB_RST` | Digital Out | Hardware-Reset zu Qorvo DW3110 UWB Transceiver (`U3.12`) |
| **U1.7** | `ESP_EN` | Digital In | Hardware-Reset mit 10k Pull-Up und 100nF Filterkondensator |
| **U1.8** | `WS2812_DATA` | Digital Out | RMT/SPI-Datenstrom für alle 36x WS2812B-2020 RGB-LEDs (`D1`–`D36`) |
| **U1.10** | `UWB_SCK` | Digital Out | SPI Serial Clock zu Qorvo DW3110 UWB Transceiver (`U3.7`) |
| **U1.11** | `UWB_MOSI` | Digital Out | SPI Master-Out zu Qorvo DW3110 UWB Transceiver (`U3.9`) |
| **U1.12** | `UWB_MISO` | Digital In | SPI Master-In von Qorvo DW3110 UWB Transceiver (`U3.8`) |
| **U1.13** | `ESP_IO9_BOOT`| Digital In | Boot-Strap Pin (GPIO 9, Low = UART Bootloader Flashen) |
| **U1.14** | `UWB_CS` | Digital Out | SPI Chip-Select (Active-Low) zu DW3110 (`U3.10`) |
| **U1.15** | `UWB_IRQ` | Digital In | Interrupt-Request von DW3110 Transceiver (`U3.13`) |
| **U1.16** | `CENTRAL_TX` | Digital Out | UART0 TX zur seitlichen 90° Programmierleiste `J3.2` |
| **U1.17** | `CENTRAL_RX` | Digital In | UART0 RX von der seitlichen 90° Programmierleiste `J3.3` |
| **U1.18, 19** | `GND` | Power | Thermische Massepads |
| **U3.4 / 5** | `UWB_XTAL1/2`| Analog | 38.4 MHz HF-Quarz `Y1_UWB` für DW3110 |
| **U3.15** | `UWB_RF` | RF 6.5G | 50 Ohm UWB HF-Pfad zu U.FL-Buchse `J4` (Kanal 5/9) |

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
