# 04b - OMM 2.4 GHz Intercom & Autonome OEM-Kassette

Dieses Dokument spezifiziert das **OpenMotorMesh (OMM) 2.4 GHz Intercom-Modul**: die universelle, quelloffene High-Definition Mesh-Intercom-Lösung von OpenMotorBridge als optionale Wechselkassette für Bucht 1 oder Bucht 2 sowie als autarkes Helm- und Begleitfahrzeug-Headset. Es beschreibt den vollständigen Protokoll-Stack von der physikalischen TDMA-Schicht (Layer 1) über die Schleifenvermeidung und Duplikatfilterung (Layer 2) und die 6LoWPAN/IPv6-Multicast-Vermittlung (Layer 3) bis hin zum RTP/Opus-Audiostreaming (Layer 4/7).

---

## 1. Modul-Konzept, UCS-Formfaktor & Trennung der Baugruppen

Um Missverständnissen zwischen der Träger-Mechatronik und dem Intercom-Modul vorzubeugen, trennt OpenMotorBridge v9.6 strikt zwischen **zwei physischen Baugruppen**:

```
+-----------------------------------------------------------------------------------------+
|                  ARCHITEKTUR-TRENNUNG: TRÄGERPLATINE VS. OMM-MODUL                      |
+----------------------------------------------------+------------------------------------+
| 1. KASSETTEN-TRÄGERPLATINE (PCBA 03 im Pod)        | 2. OMM 2.4 GHz OEM-MODUL (UCS)     |
+----------------------------------------------------+------------------------------------+
| * Verbleibt dauerhaft im Pod-Schlitten am Bike     | * Entnehmbares Intercom-Modul      |
| * Qorvo DW3110 UWB Transceiver (6.5 GHz Ch. 5)     | * Espressif ESP32-C6 (2.4 GHz)     |
| * Fahrzeug-Backbone zur Zentralbox (< 0.4 ms)      | * 2.4 GHz Wi-Fi 6 / 802.15.4 Mesh  |
| * Everest Semi ES8388 24-Bit / 48 kHz Audio-Codec  | * Integrierter 600-mAh-LiPo-Akku   |
| * 4x AO3400A MOSFETs + Mechatronik-Stößel (J_ACT)  | * 4x physische IP67-Taster         |
| * 12V -> 3.8V/5V DC-DC Bordnetz-Speisung           | * USB-C Buchse (Laden & WebUSB)    |
| * Null 2.4-GHz-Funk (Keine HF-Interferenz am Pod!) | * Null UWB (Funk nur auf 2.4 GHz)  |
+----------------------------------------------------+------------------------------------+
```

### 1.1 Physische Bedienelemente & Tasten-Layout des UCS-Adapters
Wird das OMM 2.4 GHz Modul aus dem Pod entnommen und als **autarkes Helm-Headset** (oder am Gürtel / Begleitfahrzeug) betrieben, muss es ohne Smartphone und mit dicken Motorradhandschuhen fehlerfrei bedienbar sein. Das Modul verfügt daher auf der Gehäuseoberseite über **4 taktile, wassergeschützte (IP67) Taster**:

```
+-----------------------------------------------------------------------------------------+
|                    BEDIENELEMENTE DES OMM 2.4 GHz MODULS (DRAUFSICHT)                   |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|      [ BTN 1: POWER / MFB ]               [ BTN 2: MESH / GROUP ]                       |
|      * 2s Halten : Ein- / Ausschalten     * Klick     : Open Mesh Ein / Stumm           |
|      * Klick     : Play/Pause / Akku-Ans. * 3s Halten : Open Mesh <-> Private Group     |
|      * 5s Halten : BT-Pairing (Smartphone)* 5s Halten : Quick-Join / Einladung senden   |
|                                                                                         |
|      [ BTN 3: VOL+ / KANAL+ ]             [ BTN 4: VOL- / KANAL- ]                      |
|      * Klick     : Lautstärke +           * Klick     : Lautstärke -                    |
|      * Doppelkl. : Nächster Kanal (1..6)  * Doppelkl. : Vorheriger Kanal (1..6)         |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

### 1.2 Mechatronische Aktuator-Steuerung & Makros im Pod-Betrieb
Wird das OMM-Modul im Pod auf der Smart Cartridge (`PCBA 03`) eingesetzt, greift das standardisierte Mechatronik-Konzept von OpenMotorBridge:
* **Deckungsgleiches 4-Punkt Raster:** Die 4 mechanischen Hubmagnete / Stößel auf `PCBA 03` (`ACT_1` bis `ACT_4`) sind exakt über den 4 Tastern des OMM-Moduls platziert.
* **Makro-Steuerung durch die Kassetten-MCU:** Wenn der Fahrer über das PWA-Dashboard oder die Lenkertasten einen Befehl gibt, triggert die Kassetten-MCU auf `PCBA 03` autonome Klick-Makros:

```
+----------------------+-----------------------+-----------------+-----------------------+
| Makro-Opcode         | Aktuator-Kombination  | Timing / Pulse  | Funktion am OMM-Modul |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x01` Power Boot**| **ACT_1 (Power)**     | **1.000 ms**    | Kaltstart nach Stand- |
|                      |                       |                 | zeit bei Zündung AN   |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x02` Power Off** | **ACT_1 (Power)**     | **2.000 ms**    | Sauberes Ausschalten  |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x03` Lauter**    | **ACT_3 (Plus)**      | **100 ms**      | Lautstärke +1         |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x04` Leiser**    | **ACT_4 (Minus)**     | **100 ms**      | Lautstärke -1         |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x05` Mesh Mute** | **ACT_2 (Mesh)**      | **200 ms**      | Mesh Stumm / Aktiv    |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x06` Group Mesh**| **ACT_2 (Mesh)**      | **3.000 ms**    | Open <-> Private Mesh |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x07` Kanal +1**  | **1. ACT_2 (Mesh 2x)**| **2x 150 ms**   | Menü "Kanalwahl"      |
| *(Autonomes Makro)*  | **2. Pause 200 ms**   |                 |                       |
|                      | **3. ACT_3 (Plus 1x)**| **150 ms**      | Nächster Kanal (1..6) |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x08` Kanal -1**  | **1. ACT_2 (Mesh 2x)**| **2x 150 ms**   | Menü "Kanalwahl"      |
| *(Autonomes Makro)*  | **2. Pause 200 ms**   |                 |                       |
|                      | **3. ACT_4 (Minus 1x)** **150 ms**     | Vorheriger Kanal      |
+----------------------+-----------------------+-----------------+-----------------------+
| **`0x09` Quick-Join**| **ACT_1 + ACT_2**     | **3.000 ms**    | Schnellbeitritt Gruppe|
+----------------------+-----------------------+-----------------+-----------------------+
```

* **Verschleißfreie Elektronik-Option (Zero-Wear):** Über die interne Schnittstelle `J_AUDIO_PWR` können die 4 Tasterleitungen des OMM-Moduls alternativ auch direkt digital (über UART-Steuerbefehle oder Open-Drain Schaltausgänge der Kassetten-MCU) geschaltet werden. Die mechanischen Hubmagnete gewährleisten die universelle Kompatibilität mit OEM-Geräten, während die digitale Tastung bei OMM-Modulen geräuschlos und vollkommen verschleißfrei arbeitet.

### 1.3 Elektrische Schnittstellen & UCS-Kabelarchitektur

Der **UCS-Standard (Universal Communication Solution)** nach **ECE 22.06** (initiiert von Cardo, Midland, Uclear) normiert primär die **mechanische Kavität und Außenkontur** des Headset-Gehäuses, definiert jedoch bewusst **keinen einheitlichen elektrischen Steckverbinder**. Um maximale Interoperabilität, Wasserfestigkeit (IP67) und Langlebigkeit zu garantieren, setzt das OMM 2.4 GHz Modul auf eine universelle **USB-C Multi-Funktions-Architektur**:

```
+-----------------------------------------------------------------------------------------+
|                OMM 2.4 GHz DUAL-USE SCHNITTSTELLEN-ARCHITEKTUR (USB-C)                  |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ OMM 2.4 GHz Modul im UCS-Gehäuse ]                                                   |
|        |                                                                                |
|        +---> 1x IP67-versiegelte USB-C Buchse (Geräteseite)                             |
|                    |                                                                    |
|                    +--- MODUS A: EINSATZ IM HELM (STANDALONE)                           |
|                    |    USB-C auf Helm-Kabelpeitsche:                                   |
|                    |    * Lautsprecher: Standard 3,5 mm Klinkenbuchse (TRS)             |
|                    |      (Volle Freiheit: 40 mm JBL, Sena HD, In-Ear Gehörschutz)      |
|                    |    * Mikrofon: Wasserdichter 2-Pin Verriegelungsstecker (JST-JWPF) |
|                    |      (Kompakt, rüttelfest, für Schwanenhals- oder Klebemikrofon)   |
|                    |                                                                    |
|                    +--- MODUS B: EINSATZ IM POD (SMART CARTRIDGE PCBA 03)               |
|                         USB-C auf 6-Pin JST-SH Adapterkabel (Länge 5 cm, 90° gewinkelt):|
|                         * Pin 1: GND                                                    |
|                         * Pin 2: VCC_5V (Dauer-Bordnetzladung)                          |
|                         * Pin 3..5: Digital Audio (I2S) / Analog Line-In/Out            |
|                         * Pin 6: UART Telemetrie / Zero-Wear Tastersteuerung            |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

1. **Standalone-Helmnutzung:** Der Fahrer clipst das OMM-Modul in die UCS-Kavität des Helms und verbindet die Helmpeitsche mit dem USB-C Port. Beliebige Lautsprecher (3,5 mm Klinke) und Mikrofone (2-Pin) können zerstörungsfrei getauscht werden.
2. **Gateway-Pod-Nutzung (UWB-Audio & Mill-Max DC):** Im Kassetten-Schlitten wird das Modul über ein kurzes 90°-abgewinkeltes USB-C Kabel direkt mit Header `J_AUDIO_PWR` auf `PCBA 03` gekoppelt. Die I2S-Audiodaten und Steuer-Events werden über den bordeigenen Qorvo DW3110 UWB Transceiver (6.5 GHz Ch. 5) mit einer deterministischen Latenz von $< 0{,}4\,\text{ms}$ jitterfrei und vollkommen digital zur Zentralbox (`PCBA 01`) gestreamt. Die Stromversorgung der Trägerplatine `PCBA 03` erfolgt über 2-polige Mill-Max Federkontakte aus Peitsche 1 bzw. Peitsche 2 des Deutsch DTM-12 Kabelbaums (+12V geschaltet / Masse).
3. **Wartung & Updates:** Dieselbe USB-C Buchse dient außerhalb des Fahrzeugs zum Schnellladen und für Firmware-Updates via WebUSB im Browser.

---

## 2. OMM 2.4 GHz Hardware- & Platinen-Design (PCBA Spezifikation)

Das Herzstück des Systems bildet die **OMM 2.4 GHz Autonome Intercom-Platine** (`openmotorbridge_omm_ucs`, interne System-ID: **`PCBA 09`**). Sie ist als eigenständige, hochintegrierte 2-Layer-Baugruppe konzipiert, die sowohl autark im Helm als auch als HF-Kern im Kassetten-Schlitten arbeitet.

```mermaid
flowchart TD
    subgraph Power["Power & Battery Management (TI BQ24075)"]
        USBC["IP67 USB-C Port\n(5V VBUS & Data)"] -->|5V In| PMIC["TI BQ24075 PMIC\n(Dynamic Power Path)"]
        BAT["1S LiPo 600 mAh\n(3.7V / 2.22 Wh\nmit DW01A PCM)"] <-->|Charge/Discharge| PMIC
        NTC["NTC 10k Thermistor\n(JEITA 0..45°C)"] -->|Temp Sense| PMIC
        PMIC -->|System Rail 3.8..4.4V| LDO["3.3V LDO Regulator\n(500 mA, Low-Iq)"]
        LDO -->|3.3V Rail| VDD["3.3V Systemnetz"]
    end

    subgraph MCU["Host MCU & RF Core"]
        C6["Espressif ESP32-C6-MINI-1\n(160 MHz RISC-V, 4 MB Flash)\n* 2.4 GHz Wi-Fi 6 (802.11ax)\n* 802.15.4 TDMA Mesh Radio\n* Bluetooth 5.3 LE"]
        ANT["Johanson 2450AT\nKeramik-Chipantenne\n(+2.2 dBi, 50-Ohm Pi-Netz)"] <-->|2.4 GHz RF| C6
        RGB["WS2812B-2020\nRGB Status-LED"] <--|GPIO 11| C6
        KEYS["4x IP67 Mikrotaster\n(Power, Mesh, Vol+, Vol-)"] -->|GPIO 0..3| C6
    end

    subgraph Audio["Audio Frontend (Everest Semi ES8311)"]
        C6 <-->|I2S Bus (MCLK, BCLK, WS, DOUT, DIN)\n+ I2C Control (SCL, SDA)| CODEC["Everest Semi ES8311\n(24-Bit / 96 kHz Audio Codec)"]
        CODEC -->|Class-D/AB Amp (100 mW @ 16 Ohm)| HP["Helmlautsprecher\n(40 mm JBL / Sena HD\nvia 3.5 mm Klinke)"]
        MIC["Mikrofon (ECM / Schwanenhals)\nvia 2-Pin JST-JWPF"] -->|Low-Noise Preamp + MICBIAS| CODEC
    end

    USBC <-->|USB 2.0 D+/D- & WebUSB Flashing| C6
    VDD --> C6
    VDD --> CODEC
```

### 2.1 Physikalische Platinen-Kenndaten & Lagenaufbau

| Parameter | Spezifikation | Begründung / Normbezug |
| :--- | :--- | :--- |
| **Baugruppen-ID** | **`PCBA 09`** (`openmotorbridge_omm_ucs`) | Universelle OMM 2.4 GHz Intercom-Platine |
| **Abmessungen** | **$60{,}0 \times 30{,}0 \times 1{,}0\,\text{mm}$** ($R = 2{,}5\,\text{mm}$) | Passgenau für flaches $9{,}5\,\text{mm}$ UCS-Gehäuse nach ECE 22.06 |
| **Lagenaufbau** | **2-Lagen FR4 TG150** ($35\,\mu\text{m}$ Cu) | Dünnes $1{,}0\,\text{mm}$ Kernmaterial für maximale Bauhöhenreserve |
| **Oberflächenfinish** | **ENIG** (Electroless Nickel Immersion Gold) | Korrosionsbeständig gegen Kondenswasser und Schweißdämpfe |
| **Lötstopplack** | Schwarz matt, weiße Bestückungsbeschriftung | Blendfrei, OEM-Look |
| **Befestigung** | 4x M2 Montagelöcher ($\varnothing 2{,}2\,\text{mm}$) | Bohrabstand $52{,}0 \times 22{,}0\,\text{mm}$, konzentrisch zu Gehäusedomen |
| **Schutzlackierung** | Conformal Coating (IPC-CC-830B Silikonharz) | Feuchtigkeitsschutz gegen Tropfwasser bei Helm-Montage |

### 2.2 Kernkomponenten & Schaltkreise

1. **Host-Mikrocontroller (`U1`):**
   * **Espressif ESP32-C6-MINI-1** (32-Bit RISC-V Single-Core @ $160\,\text{MHz}$, $512\,\text{kB}$ SRAM, $4\,\text{MB}$ Quad-SPI Flash).
   * **Drei integrierte 2.4-GHz-Funkstandards:** Wi-Fi 6 ($802.11\text{ax}$ mit Target Wake Time für minimale Stromaufnahme), IEEE 802.15.4 (Basis für das deterministische OMM TDMA-Mesh) und Bluetooth 5.3 LE (für Smartphone-Kopplung, PWA-Dashboard und Audio-Hands-Free).
2. **Power Management & Dynamic Power Path (`U2`):**
   * **Texas Instruments BQ24075RGTR** (QFN-16 $3 \times 3\,\text{mm}$) mit integriertem Power-Path Management.
   * **Unterbrechungsfreier Betrieb:** Erkennt der Lade-IC eine 5V-Speisung am USB-C Port (z. B. im Kassetten-Pod am Motorrad oder an einer Powerbank), versorgt er das System direkt über die interne $4{,}4\text{V}$-Schiene (`OUT`) und lädt den LiPo-Akku parallel mit programmierbaren $500\,\text{mA}$.
   * **Zero-Reboot Umschaltung:** Wird das Modul aus dem Pod gezogen, übernimmt der Akku über den internen $100\,\text{m}\Omega$ Ideal-Dioden-FET in $< 10\,\mu\text{s}$ – die Intercom läuft unterbrechungsfrei weiter, ohne dass das Mesh neu synchronisiert werden muss!
   * **Batterieüberwachung nach JEITA:** Ein $10\,\text{k}\Omega$ NTC-Thermistor an der Akkuzelle drosselt den Ladestrom bei hohen Temperaturen ($> 45^\circ\text{C}$) und blockiert das Laden unter $0^\circ\text{C}$.
3. **Integrierter LiPo Pouch-Akku (`BAT1`):**
   * **Kapazität:** $600\,\text{mAh}$ ($3{,}7\,\text{V}$ nominal, $2{,}22\,\text{Wh}$ Energieinhalt).
   * **Zellenmaße:** $38{,}0 \times 24{,}0 \times 4{,}5\,\text{mm}$ flach.
   * **Integrierte Schutzschaltung (PCM):** DW01A Controller mit 8205A Dual-MOSFET schützt gegen Überladung ($4{,}28\,\text{V}$ Cutoff), Tiefentladung ($2{,}4\,\text{V}$ Cutoff) und Kurzschluss ($> 2{,}5\,\text{A}$).
   * **Laufzeit im Standalone-Helmeinsatz:** **12 bis 14 Stunden** kontinuierliche Vollduplex-Mesh-Kommunikation.
4. **Audio Frontend Codec (`U4`):**
   * **Everest Semi ES8311** (QFN-20 $3 \times 3\,\text{mm}$): Ultra-Low-Power Mono-Audio-Codec ($< 14\,\text{mW}$ aktive Leistungsaufnahme).
   * **Integrierter Kopfhörerverstärker:** Liefert $100\,\text{mW}$ @ $16\,\Omega$ bzw. $55\,\text{mW}$ @ $32\,\Omega$ mit THD+N $< 0{,}03\,\%$ direkt an 40 mm Helmlautsprecher ohne nachgeschalteten Analog-Amp.
   * **Mikrofon-Frontend:** Rauscharmer Vorverstärker mit einstellbarem Gain ($+0\dots +30\,\text{dB}$ in 3-dB-Schritten), interner programmierbarer `MICBIAS`-Spannung ($2{,}0\dots 2{,}8\,\text{V}$) und integriertem Rauschfilter.
5. **HF-Antennensystem (`ANT1`):**
   * **Johanson Technology 2450AT45A100** ($9{,}5 \times 2{,}0 \times 1{,}2\,\text{mm}$ Keramik-Chip, Spitzen-Gain $+2{,}2\,\text{dBi}$).
   * An der vorderen Platinenkante über einer metallfreien Sperrfläche ($8{,}0 \times 4{,}0\,\text{mm}$ Keep-Out Zone) angeordnet.
   * Ein $50\,\Omega$ Pi-Filter (2x 0402 Shunt-Kondensatoren, 1x Serien-Induktivität) kompensiert die dielektrische Verstimmung durch das umgebende PA12-Gehäuse und die Helmschale.

### 2.3 ESP32-C6 Pinout & GPIO-Zuweisung

```
+-----------------------------------------------------------------------------------------+
|                  PCBA 09: ESP32-C6-MINI-1 PINOUT & HARDWARE-SCHNITTSTELLEN              |
+-------------+---------------+---------------+-------------------------------------------+
| ESP32-C6 Pin| Signal-Name   | Typ           | Funktion / Angeschlossenes Peripherieteil |
+-------------+---------------+---------------+-------------------------------------------+
| **GPIO 0**  | `BTN_PWR`     | Digital In    | SW1 (Power / MFB, Low-aktiv, Boot-Pin)    |
| **GPIO 1**  | `BTN_MESH`    | Digital In    | SW2 (Mesh / Group Toggle, Low-aktiv)      |
| **GPIO 2**  | `BTN_VOL_UP`  | Digital In    | SW3 (Lautstärke +, Low-aktiv)             |
| **GPIO 3**  | `BTN_VOL_DN`  | Digital In    | SW4 (Lautstärke -, Low-aktiv)             |
| **GPIO 4**  | `I2S_MCLK`    | Digital Out   | ES8311 Master Clock (12.288 MHz)          |
| **GPIO 5**  | `I2S_BCLK`    | Digital Out   | ES8311 Bit Clock (1.536 MHz)              |
| **GPIO 6**  | `I2S_WS`      | Digital Out   | ES8311 Word Select / Frame Sync (48 kHz)  |
| **GPIO 7**  | `I2S_SDOUT`   | Digital Out   | ES8311 DAC Audio Stream (Lautsprecher)    |
| **GPIO 8**  | `I2S_SDIN`    | Digital In    | ES8311 ADC Audio Stream (Mikrofon)        |
| **GPIO 9**  | `I2C_SCL`     | Open-Drain    | ES8311 Register Control SCL (4.7k Pullup) |
| **GPIO 10** | `I2C_SDA`     | Open-Drain    | ES8311 Register Control SDA (4.7k Pullup) |
| **GPIO 11** | `WS2812_DATA` | Digital Out   | D1 (WS2812B-2020 RGB Status-LED)          |
| **GPIO 12** | `CHG_STAT1`   | Digital In    | BQ24075 /STAT Ladeanzeige (Pullup)        |
| **GPIO 13** | `PWR_GOOD`    | Digital In    | BQ24075 /PGOOD VBUS-Erkennung             |
| **GPIO 14** | `VBAT_SENSE`  | Analog In     | Akku-Spannungsteiler (100k / 100k zu GND) |
| **GPIO 15** | `NTC_SENSE`   | Analog In     | Akku-Temperaturüberwachung (JEITA)        |
| **GPIO 16** | `UART_TX`     | Digital Out   | Serieller Bus / Zero-Wear Pod-Kopplung    |
| **GPIO 17** | `UART_RX`     | Digital In    | Serieller Bus / Zero-Wear Pod-Kopplung    |
| **USB_DP**  | `USB_D_P`     | USB 2.0 PHY   | USB-C D+ (WebUSB Firmware-Flashing & DFU) |
| **USB_DM**  | `USB_D_N`     | USB 2.0 PHY   | USB-C D- (WebUSB Firmware-Flashing & DFU) |
+-------------+---------------+---------------+-------------------------------------------+
```

### 2.4 Energiebudget & Betriebsmodi

| Betriebsmodus | Funkstatus | Audio / Codec | Stromaufnahme ($3{,}7\,\text{V}$) | Akkulaufzeit ($600\,\text{mAh}$) |
| :--- | :--- | :--- | :--- | :--- |
| **Deep Sleep (Ausgeschaltet)** | Alle Radios aus | ES8311 Power-Down | $22\,\mu\text{A}$ | $> 2{,}5\,\text{Jahre}$ |
| **Mesh Standby (Zuhören)** | 802.15.4 RX aktiv | DAC aktiv, kein Signal | $34\,\text{mA}$ | **ca. 17,6 Stunden** |
| **Mesh Vollduplex (Sprechen)** | 802.15.4 TX Burst | ADC + DAC voll aktiv | $52\,\text{mA}$ | **ca. 11,5 Stunden** |
| **Pod-Betrieb am Motorrad** | RX/TX aktiv | I2S Stream zu PCBA 03 | Gepuffert über $5\,\text{V}$ Bordnetz | **Unbegrenzt (Dauerladung)** |

---

## 3. OMM 2.4 GHz Mechanik & UCS-Gehäusedesign (nach ECE 22.06)

Das Gehäuse des OMM 2.4 GHz Moduls ist konsequent nach der internationalen **Universal Communication Solution (UCS) Spezifikation** im Rahmen der **Helmnorm ECE 22.06** ausgelegt.

![OMM 2.4 GHz UCS Intercom Modul CAD](../images/cad/omm_ucs_module_cad.png)

*Abbildung 4b.1: 3D-CAD-Ansicht des autonomen OMM 2.4 GHz UCS-Moduls (`omm_ucs_module_cad.png`). Sichtbar sind die zweischalige PA12-Monocoque-Konstruktion ($68 \times 36 \times 9{,}5\,\text{mm}$), die 4x formschlüssigen DIN 934 M2 Sechskant-Mutterntaschen in der Oberschale, die monolithische Shore 50A Silikon-Tastmatte mit Haptiknoppen, die frontale wasserdichte USB-C Lade- und Audioschnittstelle sowie die seitlichen ECE 22.06 Schnapprastnasen.*

```
+-----------------------------------------------------------------------------------------+
|                  UCS-GEHÄUSEABMESSUNGEN & ECE 22.06 RASTMECHANIK                        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|       |<--------------------------- 68,0 mm -------------------------->|                |
|       +----------------------------------------------------------------+  ^             |
|       | [Rastnase L]                                      [Rastnase R] |  |             |
|       |   |                                                    |       |  |             |
|       |   v                                                    v       |  | 36,0 mm     |
|   (=) |   +---+   [PWR/MFB]     [MESH]     [VOL+]     [VOL-]   +---+   |  |             |
|   USB |   |   |     (o)          (o)        (+)        (-)     |   |   |  |             |
|   -C  |   +---+                                                +---+   |  v             |
|       +----------------------------------------------------------------+                |
|                                                                                         |
|       |<----------------- 9,5 mm Gehäusedicke (Ultraschlank) ---------->|                |
|       +----------------------------------------------------------------+                |
|       | 1. OBERSCHALE (PA12 MJF, Dichtnut & 4x DIN 934 M2 Mutterntaschen)              |
|       | ~~~~~~~~~~~~~~~~~ Shore 40A Silikondichtschnur (IP67) ~~~~~~~~~~~~~~~~~        |
|       | 2. PCBA 09 (1,0 mm FR4) & 600-mAh-LiPo mit EPDM-Dämpfungspolster               |
|       | 3. UNTERSCHALE (PA12 MJF mit 4x M2 Senkschrauben & ECE 22.06 Helmrasten)       |
|       +----------------------------------------------------------------+                |
+-----------------------------------------------------------------------------------------+
```

### 3.1 Das ECE 22.06 UCS-Gehäusekonzept

Moderne Helme nach ECE 22.06 (wie Shoei Neotec 3 / GT-Air 3, Schuberth C5 / E2 / S3, Nolan N100-5, Arai Tour-X5) besitzen an der linken Außenseite oder im Nackenbereich eine **genormte, vertiefte Kavität**. Das OMM-Modul erfüllt diese Abmessungen auf den Zehntelmillimeter:
* **Außenmaße:** **$68{,}0 \times 36{,}0 \times 9{,}5\,\text{mm}$** (Länge x Breite x Gehäusedicke).
* **Gewicht:** Nur **$38\,\text{g}$** inklusive Akku und Platine – keine spürbare Helm-Asymmetrie oder Nackenermüdung.
* **ECE 22.06 Schlagprüfungskonform:** Durch die flache Bauform ($9{,}5\,\text{mm}$) ragt das Gehäuse nicht über die aerodynamische Abrisskante des Helms hinaus. Bei einem Aufprall scheren keine gefährlichen Kanten ab.

### 3.2 Gehäuseaufbau & 100% IP67 Dichtungskonzept

Das Gehäuse besteht aus drei präzise aufeinander abgestimmten Komponenten:

1. **Oberschale (`omm_ucs_top_shell.scad`):**
   * Gefertigt im **HP Multi Jet Fusion (MJF) Verfahren aus PA12** (oder PC/ABS Spritzguss).
   * Umlaufende Dichtungsnut ($1{,}0\,\text{mm}$ Breite, $1{,}2\,\text{mm}$ Tiefe) an der Trennebene zur Unterschale.
   * Aussparung für die Silikon-Tastmatte mit umlaufendem, hinterstochenem Dichtkragen.
   * **Formschlüssige DIN 934 M2 Sechskant-Mutterntaschen:** In den 4 Eckdomen sind exakte Sechskant-Aufnahmen eingearbeitet. Die V4A-Edelstahlmuttern werden bei der Erstmontage formschlüssig eingelegt und bleiben verliersicher verankert.
2. **Unterschale (`omm_ucs_bottom_shell.scad`):**
   * Enthält die 4 Schraubendurchgangsbohrungen ($\varnothing 2{,}3\,\text{mm}$) mit Senkungen für **DIN 912 M2 x 8 mm Zylinderschrauben**.
   * An den Längsseiten sind zwei federnde Rastnasen (Snap-Fit Claws) angeformt, die beim Einschieben in die Helmkavität mit einem satten Klick einrasten und das Modul rüttelfest sichern.
   * Innenliegende Akku-Wanne mit $0{,}5\,\text{mm}$ geschäumtem EPDM-Polster zur Absorption von Stoß- und Vibrationskräften.
   * Vordere Aussparung für die wasserdichte USB-C Buchse mit doppelter Dichtlippe.
3. **Einteilige Silikon-Tastmatte (`omm_ucs_silicone_keypad.scad`):**
   * Aus vulkanisiertem, UV- und handschweißbeständigem Silikon (Shore 50A, mattschwarz).
   * **100 % dichte Barriere:** Die Tastmatte ist monolithisch geschlossen. Es gibt keine Löcher oder Schlitze, durch die Wasser oder Feuchtigkeit ins Innere dringen könnte.
   * 4 erhabene Tastendome mit haptischen Relief-Symbolen ermöglichen die zielsichere Blindbedienung während der Fahrt.
   * Ein integrierter, optisch transparenter Silikondom leitet das Licht der WS2812B RGB-LED diffus an die Gehäuseoberfläche.

### 3.3 Verbindliche Befestigungs-Philosophie: Formschlüssige DIN 934 Mutterntaschen

> [!IMPORTANT]
> **Ausschluss selbstschneidender Schrauben in Kunststoff:**
> Das Schneiden von Gewinden direkt in Kunststoff-Kernlöcher führt bei Intercom-Gehäusen unweigerlich zum Totalverlust nach der ersten Demontage: Das Gewinde im weichen PA12 leiert aus und verliert die Klemmkraft, wodurch die IP67-Dichtung versagt.
> 
> Das OMM 2.4 GHz Gehäuse nutzt daher **ausnahmslos formschlüssige DIN 934 M2 Sechskantmutter-Taschen** in der Oberschale. Das Gehäuse kann über die 4x M2-Edelstahlschrauben **beliebig oft zerstörungsfrei geöffnet und wieder verschraubt werden** (z. B. für Akkutausch nach Jahren, Reinigung oder Hardware-Upgrades).

### 3.4 Dual-Use Schlitten-Einsatz im Kassetten-Pod

Wird das OMM-Modul im Motorrad-Pod betrieben:
1. Das geschlossene UCS-Gehäuse gleitet formschlüssig in die passgenaue Wanne des oberen Kassetten-Einsatzes ([`cartridge_insert_omm_ucs.scad`](../../hardware/cad/scad/03_pod_cartridges/parts/06_insert_omm_ucs.scad)) auf dem Universalschlitten ([`cartridge_base_sled.scad`](../../hardware/cad/scad/03_pod_cartridges/00_base_sled.scad)).
2. Ein elastisches EPDM-Gummispannband über den Haltenasen sichert das Modul gegen Herausfallen bei extremen Offroad-Vibrationen.
3. Über das kurze, 90°-abgewinkelte USB-C-Adapterkabel wird das Modul direkt mit Header `J_AUDIO_PWR` der Kassetten-Trägerplatine (`PCBA 03`) verbunden:
   * **Stromversorgung:** Dauerhafte $5\,\text{V}$-Bordnetzladung über die Mill-Max Kontakte aus Peitsche 1 bzw. 2.
   * **Audio-Brücke:** Das I2S-Audiosignal wird über den Qorvo DW3110 UWB-Transceiver (6.5 GHz Ch. 5) der Trägerplatine digital und jitterfrei mit $< 0{,}4\,\text{ms}$ Latenz zur Zentralbox (`PCBA 01`) übertragen.

---

## 4. Layer 1: 2.4 GHz High-Speed TDMA Superframe-Struktur

Das OMM 2.4 GHz Mesh basiert auf einem zeitgesteuerten Vielfachzugriffsverfahren (Slotted TDMA) über das ESP32-C6 Wi-Fi/ESP-NOW Radio:

```
+-----------------------------------------------------------------------------------------+
|                     10 ms TDMA SUPERFRAME-STRUKTUR (OMM 2.4 GHz)                        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  |<----------------------------- 10 ms SUPERFRAME ------------------------------------->|
|  +----------+----------+----------+----------+----------+----------+----------+-------+ |
|  | SUBFR. 0 | SUBFR. 1 | SUBFR. 2 | SUBFR. 3 | SUBFR. 4 |   ...    | SUBFR. 9 | GUARD | |
|  |  SYNC &  |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   |  AUDIO   | BAND  | |
|  | CONTROL  | SPRECHER1| SPRECHER2| SPRECHER3| SPRECHER4| SPRECHER5| SPRECHER6| 0.5ms | |
|  +----------+----------+----------+----------+----------+----------+----------+-------+ |
+-----------------------------------------------------------------------------------------+
```

* **Superframe-Dauer:** Exakt $10{,}0\,\text{ms}$ (100 Hz Bildwiederholrate).
* **Subframe 0 (Synchronisation & Control):**
  * Überträgt das Synchronisationssignal (Sidelink Synchronization Signal, SLSS) und Zeitschlitz-Zuweisungen.
  * Kündigt Sprecherwünsche (VAD / Lenker-PTT-Events) mit minimalem Overhead an.
* **Subframes 1-9 (Kollisionsfreie Audioschlitze):**
  * Jeder aktive Sprecher erhält einen exklusiven $0{,}95\,\text{ms}$ Zeitschlitz.
  * Übertragung von Opus-komprimierten Sprachframes ($24\,\text{kHz}$ Breitband / $16\dots 24\,\text{kbps}$).
  * Bis zu 6 Sprecher können gleichzeitig im Vollduplex sprechen, ohne dass Sprachpakete kollidieren.
* **System-Latenz:** Gesamtverzögerung vom Mikrofon bis zum Empfängerhörer: **$< 18\,\text{ms}$** (äquivalent zu Sena Mesh 3.0 / Cardo DMC Gen2).

---

## 5. Layer 2: 802.11s-Light Loop-Prevention & Duplicate-Filter

OpenMotorMesh implementiert Routing- und Schleifenvermeidungsmechanismen angelehnt an den IEEE 802.11s Standard (HWMP / Airtime Metric) direkt auf Sicherungsebene:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Mesh Control  |   Hop Limit   |     Mesh Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Originator Node MAC                       |
|                         (Bytes 0..3)                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Originator MAC (4..5)        |      Target Node MAC (0..1)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Target MAC (2..5)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Payload: 6LoWPAN / IPv6 Multicast / RTP / Opus Audio ...      |
```

### 5.1 Layer-2 Frame Header Definition & Duplicate-Filter
Jedes OMM-Paket kapselt die Nutzdaten in einen schlanken 16-Byte Header:

```cpp
struct MeshHeader_t {
    uint8_t  meshFlags;     // Priority (Bit 0..2) & Type Flags (Bit 3..7)
    uint8_t  hopLimit;      // TTL-Dekrement pro Hop (Schleifenschutz, Default = 5)
    uint16_t meshSeqNum;    // Monoton steigende Sequenznummer des Senders
    uint8_t  originMac[6];  // Erzeuger-Node MAC (aus 64-Bit DS2401 UID abgeleitet)
    uint8_t  targetMac[6];  // Multicast (33:33:...) oder Unicast-Ziel
} __attribute__((packed));
```

Beim Empfang eines Rohframes filtert die Firmware Duplikate **vor jeder Übergabe an den IP-Stack** in Hardware/DMA-Nähe heraus:

```cpp
void onRawPacketReceived(uint8_t* rawData, size_t len) {
    if (len < sizeof(MeshHeader_t)) return;
    
    MeshHeader_t* meshHdr = (MeshHeader_t*)rawData;
    uint8_t* payload = rawData + sizeof(MeshHeader_t);
    size_t payloadLen = len - sizeof(MeshHeader_t);

    // 1. Layer-2 Loop & Duplicate Filter (64-Entry Ringpuffer)
    if (meshHdr->hopLimit == 0) return;
    if (checkAndRegisterL2Duplicate(meshHdr->originMac, meshHdr->meshSeqNum)) {
        return; // Duplikat verworfen -> Spart CPU-, DMA- und IP-Stack-Last!
    }

    // 2. Lokale Weitergabe an Layer 3 (6LoWPAN / IPv6 Multicast)
    processL3Payload(payload, payloadLen);

    // 3. 802.11s Managed Forwarding: Weiterleiten, falls Node Relay-Rolle hat
    if (currentRideMode == MODE_RELAY_AR && meshHdr->hopLimit > 1) {
        meshHdr->hopLimit--;
        broadcastForward(rawData, len);
    }
}
```

### 5.2 Antennen- und Knoten-Diversität (Remote Radio Head / Split-MAC)
Auf dem Motorrad führt die Abschattung durch den Körper des Fahrers zu Richtungsabhängigkeiten im 2.4-GHz-Band. Stehen dem System zwei Empfänger zur Verfügung (z. B. Front-Node `PCBA 05` und Heck-Pod, oder zwei Antennen links und rechts über den Koffern):
* **Kein doppeltes Audio:** Beide Empfänger empfangen denselben L2-Frame. 
* **Blitzschneller L2-Cache:** Der erste eintreffende Frame wird verarbeitet. Trifft die Kopie $< 2\,\text{ms}$ später über den zweiten Pfad ein, matcht `checkAndRegisterL2Duplicate()` die Sequenznummer und verwirft das Paket in $< 5\,\mu\text{s}$.
* **Ergebnis:** Perfekte Raumdiversität ohne Jitter, ohne zusätzliche CPU-Last und ohne Verwirrung des Audio-Codecs.

---

## 6. Layer 3: 6LoWPAN & IPv6-Multicast Architecture

Klassische Ad-hoc-Netzwerke scheitern oft an ineffizienten Transportprotokollen. OMM setzt auf einen sauberen, standardisierten IPv6-Stack:

```
+-----------------------------------------------------------------------------------------+
|                  6LoWPAN & IPv6 MULTICAST ARCHITEKTUR (RFC 6282)                        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ LAYER 4: UDP / RTP ]       Opus Audio Frames (20 ms / 24 kHz Breitband)              |
|                                                                                         |
|  [ LAYER 3: IPv6 MULTICAST ]  Gruppenadressen (ff02::1:X), SLAAC fe80::/64              |
|                                                                                         |
|  [ 6LoWPAN KOMPRESSION ]      Komprimiert 40-Byte IPv6 Header auf 2 bis 4 Bytes         |
|                                                                                         |
|  [ LAYER 2: 802.11s-LIGHT ]   MeshHeader_t (16 Bytes), Duplicate-Filter & Hop-Limit     |
|                                                                                         |
|  [ LAYER 1: TDMA RADIO ]      ESP32-C6 2.4 GHz Slotted Radio (10 ms Superframe)         |
+-----------------------------------------------------------------------------------------+
```

### 6.1 Warum IPv6-Multicast statt TCP oder Unicast UDP?
* **Das TCP-Verbot im Mesh:** TCP ist streng verbindungsorientiertes 1:1 Unicast mit Quittierung (ACK) und Retransmission (ARQ). Geht bei $100\,\text{km/h}$ auf der Landstraße *ein einziges* TCP-Paket verloren, stoppt TCP den kompletten Stream (Head-of-Line Blocking). Die Latenz schießt binnen 2 Sekunden auf über $800\,\text{ms}$ hoch – unbrauchbar für Vollduplex-Intercom. Zudem unterstützt TCP prinzipbedingt kein Multicast.
* **Das Unicast-UDP Airtime-Problem:** Wollte ein Sender 20 Gruppenmitglieder per Unicast UDP bedienen, müsste er dasselbe Audiopaket 20 Mal hintereinander senden – das 2.4-GHz-Band würde sofort kollabieren.
* **Die Lösung: IPv6-Multicast:** Das Audiopaket wird **ein einziges Mal** an die Gruppenadresse gesendet. Jeder Knoten im Funkradius nimmt das Paket auf, ohne den Kanal zu überlasten.

### 6.2 6LoWPAN Header-Komprimierung (RFC 6282)
Ein Standard-IPv6-Header belegt 40 Bytes. Bei einem 10-ms-Opus-Audioframe (ca. 40 bis 60 Bytes Payload) würde ein 40-Byte-Header die Bandbreite halbieren.
* 6LoWPAN nutzt Kontext- und Adress-Elision: Da die Link-Local-Adressen direkt aus den 64-Bit-Hardware-UIDs hervorgehen und die Multicast-Präfixe statisch sind, schrumpft der IPv6-Header auf **2 bis 4 Bytes Overhead** zusammen.

### 6.3 SLAAC-Adressierung & RPL-Routing
* **Autonome Adressvergabe (SLAAC):** Jeder Knoten leitet seine IPv6 Link-Local-Adresse (`fe80::/64`) vollautomatisch und deterministisch aus der Dallas DS2401 Silicon-UID ab. Null manuelle Konfiguration, keine DHCP-Server nötig.
* **Dynamisches RPL (RFC 6550):** Für Teilnehmer außerhalb der 1-Hop-Sichtlinie spannt das Routing Protocol for Low-Power and Lossy Networks (RPL) automatisch einen optimalen, schleifenfreien Weiterleitungsbaum auf.

---

## 7. Layer 4 & Audio-Transport: Opus over RTP & Multicast-Kanäle

### 7.1 RTP Audio Streaming (RFC 3550)
* **Transport:** Encapsulation der Audiodaten in Real-time Transport Protocol (RTP) Paketen über UDP.
* **Adaptiver Jitter-Puffer (20 bis 50 ms):** Gleicht Packet Delay Variations (PDV) durch wechselnde Abstände in Kurvenkombinationen elastisch aus.
* **Packet Loss Concealment (PLC):** Verliert das Mesh ein einzelnes Sprachpaket, interpoliert der Opus-Decoder die fehlenden Audioschwingungen anhand der Formanten des Vorläufer-Frames – Audio bleibt ohne Knacken voll verständlich.
* **Opus-Konfiguration:** 24 kHz Samplingrate (Breitband HD), dynamische Bitrate $16\dots 24\,\text{kbps}$ VBR mit Voice Activity Detection (VAD).

### 7.2 Multicast-Kanalverwaltung (Open Mesh vs. Private Group)

```
+------------------+---------------------+-------------------+-------------------------------+
| Kanal-Modus      | IPv6 Multicast-Adr. | Verschlüsselung   | Einsatzzweck                  |
+------------------+---------------------+-------------------+-------------------------------+
| **Open Mesh CH 1**| ff02::1:1           | Keine (Offen)     | Offener Allgemein-Kanal       |
| **Open Mesh CH 2**| ff02::1:2           | Keine (Offen)     | Ausweichkanal Tourengruppe    |
| **Open Mesh CH 3**| ff02::1:3           | Keine (Offen)     | Sport- / Renngruppe           |
| **Open Mesh CH 4**| ff02::1:4           | Keine (Offen)     | Freie Gruppen                 |
| **Open Mesh CH 5**| ff02::1:5           | Keine (Offen)     | Begleitfahrzeuge / Support    |
| **Open Mesh CH 6**| ff02::1:6           | Keine (Offen)     | Event- / Streckenfunk         |
| **PRIVATE GROUP** | ff02::2:XX (UID)    | AES-128-GCM       | Geschlossene Gruppe (PWA)     |
+------------------+---------------------+-------------------+-------------------------------+
```

1. **Offene Multicast-Kanäle (CH 1 bis 6):**
   * Funktioniert analog zu Senas *Multi-Channel Open Mesh*: Jeder Teilnehmer im selben Funkkanal hört die Gruppe ohne vorheriges Pairing.
   * Ideal für spontane Touren, Treffen oder gemeinsame Ausfahrten mit fremden OMM-Nutzern.
2. **Private Gruppen mit AES-128-GCM Verschlüsselung:**
   * Für geschlossene Touren generiert der Tourguide in der PWA einen 128-Bit Session-Key.
   * Der Schlüssel wird entweder am Start via QR-Code im PWA-Dashboard gescannt oder über das LoRa-Backbone per Zero-Touch Handshake verteilt.
   * Die RTP-Payload wird mit AES-128-GCM verschlüsselt; Header bleiben für L2/L3-Routing lesbar. Unbefugte Zuhörer auf 2.4 GHz empfangen nur unlesbares Rauschen.

---

## 8. Dynamic Leader Election (DLE) im OMM-Mesh

Innerhalb jeder 2.4-GHz-Funkzelle wählt das Netzwerk vollautomatisch und dezentral genau einen **Cluster Head (Gateway Master)**, der das TDMA-Zeitschlitzraster synchronisiert und das Relaying steuert:

$$\text{Score}_{\text{DLE}} = S_{\text{HW}} + S_{\text{PWR}} + S_{\text{GNSS}} + S_{\text{LORA}} + S_{\text{UPTIME}}$$

```
+-----------------------------------+---------------------------------------------+------------+
| Parameter                         | Bedingung                                   | Punkte     |
+-----------------------------------+---------------------------------------------+------------+
| **S_HW (Hardware Tier)**          | OMM 2.4 GHz + DW3110 UWB Backbone aktiv     | **+50 Pkt**|
| **S_PWR (Stromversorgung)**       | Zündung aktiv (KL15 > 12.5 V via LM5164)    | **+20 Pkt**|
|                                   | Akkubetrieb (USV LiPo > 3.8 V)              | +5 Pkt     |
| **S_GNSS (Position & Takt)**      | 3D-Fix mit PDOP < 1.5 & 1-PPS Takt aktiv    | **+10 Pkt**|
| **S_LORA (Link-Qualität)**        | Mittlerer Nachbar-RSSI > -85 dBm            | **+10 Pkt**|
| **S_UPTIME (Hysterese-Schutz)**   | Aktuell amtierender Leader (Anti-Flapping)  | **+15 Pkt**|
+-----------------------------------+---------------------------------------------+------------+
```

* **Anti-Flapping:** Die Hysterese von $+15$ Punkten verhindert ständiges Hin- und Herschalten des Masters bei minimalen RSSI-Schwankungen.
* **1-PPS Synchronisation:** Nodes mit verlässlichem GNSS-1-PPS-Takt werden bevorzugt, da sie das TDMA-Zeitschlitzraster mit atomarer Präzision stabil halten.

---

## 9. Cluster Partitioning & LoRa Cross-Gateway Relay (LTE-Sidelink Adaption)

Reißt eine Motorradgruppe an einer roten Ampel, einem Bahnübergang oder in engen Bergkehren in zwei Hälften ab, greift die hybride Gateway-Kaskade:

```
[ FRONT-GRUPPE (Bikes 1-3) ]                         [ REAR-GRUPPE (Bikes 4-6) ]
  Lokales 2.4 GHz HD Mesh                              Lokales 2.4 GHz HD Mesh
  IPv6 Multicast (Opus HD)                             IPv6 Multicast (Opus HD)
             |                                                    |
     [ Leader 1 (Bike 1) ]                                [ Leader 2 (Bike 4) ]
             |                                                    |
             +======= 868 MHz LoRa Voice Tunnel (Codec2 1200bps) =+
```

1. **Autonome Sub-Leader Wahl:** Die hintere Gruppe verliert die 2.4-GHz-Beacons von Leader 1 ($T_{\text{timeout}} > 500\,\text{ms}$) und wählt in $< 200\,\text{ms}$ autonom Bike 4 als lokalen Leader 2.
2. **Lokales HD-Mesh bleibt aktiv:** Innerhalb der Front-Gruppe und innerhalb der Rear-Gruppe bleibt das 2.4-GHz-Voll-Duplex-Mesh mit voller Sprachqualität aktiv.
3. **LoRa Cross-Gateway Tunnel:** Spricht ein Fahrer in der hinteren Gruppe, komprimiert Leader 2 das Audio in ultrakompaktes Codec2 ($1200\,\text{bps}$) und sendet es als LoRa-Burst über 868 MHz an Leader 1.
4. **Re-Injektion in das Fremd-Mesh:** Leader 1 dekomprimiert das Signal und injiziert es als lokalen IPv6-Multicast-Frame in das 2.4-GHz-Mesh der Frontgruppe. Die Gruppe hört: *"Ampel rot, nehmt kurz Tempo raus!"*
5. **Cluster Fusion (Auto-Merge):** Schließt die Nachzügler-Gruppe wieder auf ($< 400\,\text{m}$), empfängt Leader 2 das Sync-Signal von Leader 1, gibt die Koordinator-Rolle geräuschlos ab und schließt den LoRa-Tunnel.

---

## 10. Integration in den Link-State Audio Bridging Graph

Wird die OMM 2.4 GHz Kassette in Bucht 1 oder Bucht 2 gesteckt, bindet der ESP32-S3 Hauptcontroller sie nahtlos in die fahrzeugübergreifende Routing-Matrix ein:

1. **DLE-Capability-Score:**
   * Das OMM 2.4 GHz Modul erhält im Link-State Graph einen **Basis-Score von +50 Punkten** (vollwertiges HD-Mesh mit bis zu 32 Teilnehmern).
2. **Cross-Bridging zu Sena / Cardo:**
   * Befinden sich in Bucht 1 ein Sena SPIDER X Slim und in Bucht 2 die OMM 2.4 GHz Kassette, übersetzt OpenMotorBridge Sprache bidirektional zwischen beiden Welten.
   * Das First-Receiver-Wins (FRW) Schiedsverfahren auf LoRa Kanal 2 verhindert Echos und Mehrfacheinspeisungen in Kolonnen mit mehreren Brücken-Motorrädern.
3. **Do-Not-Translate (DNT) Anti-Loop Flag:**
   * Aus dem OMM 2.4 GHz Mesh empfangene Audiosignale erhalten beim Weiterleiten an ein Sena/Cardo-Mesh das `FLAG_DO_NOT_TRANSLATE`, um akustische Rückkopplungsschleifen (Feedback Loops) über Dritte physikalisch unmöglich zu machen.
4. **PWA Koppel- & Wartungsmodus:**
   * Über das PWA-Dashboard kann der Fahrer die OMM-Kassette per Knopfdruck in den Pairing-Modus versetzen, Kanäle wechseln und Audio-Pegel anpassen.
5. **Autarke Firmware-Updates des OMM-Moduls (USB-C & BLE/Wi-Fi OTA):**
   * **Wichtige Architekturtrennung:** Das OMM 2.4 GHz Intercom-Modul besitzt **keinen eigenen UWB-Transceiver**. Der DW3110 UWB-Chip befindet sich ausschließlich auf der Kassetten-Trägerplatine (`PCBA 03`).
   * **Update-Pfade des OMM-Moduls (ESP32-C6):**
     * **Kabelgebunden via USB-C (WebUSB / DFU):** Über die stirnseitige USB-C-Buchse kann das Modul direkt am Smartphone, Tablet oder PC angeschlossen werden. Die PWA flasht die Firmware per WebUSB im Browser in $< 15\,\text{s}$ ohne zusätzliche Software.
     * **Drahtlos via Bluetooth LE / Wi-Fi (ESP-IDF OTA):** Das Smartphone verbindet sich per BLE oder Wi-Fi direkt mit dem ESP32-C6 des OMM-Moduls. Das Update wird drahtlos über die standardisierte A/B-Partitionierung (`ota_0`/`ota_1`) mit Rollback-Schutz eingespielt – völlig autark, sowohl im Helm-Betrieb als auch im Pod.
   * **Wartung der Kassetten-Trägerplatine (`PCBA 03`):**
     * Die fahrzeuggebundene Trägerplatine `PCBA 03` im Pod (deren ESP32-C6 und DW3110) wird im Fahrbetrieb über den internen UWB-Link von der Zentralbox (`PCBA 01`) gewartet und bei Bedarf per UWB-OTA aktualisiert.
     * Beide Systeme verfügen somit über getrennte, robuste und fehlertolerante Update-Mechanismen.

---

## 11. Begleitfahrzeug-Einsatz & Pkw-Audio-Routing (Kit 5 Kolonnen-Topologie)

In Begleitfahrzeugen (Support-Van, Besenwagen, Tourguide-Pkw, Rallye-Orga) fungiert das OMM 2.4 GHz Modul als Herzstück der Sprachkommunikation zwischen Pkw-Insassen und der Motorradgruppe:

```
+-----------------------------------------------------------------------------------------+
|                  BEGLEITFAHRZEUG / PKW-INTEGRATION (KIT 5 ARCHITEKTUR)                  |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ FAHRZEUG-INSASSEN ] <--- (Dachmikro / KFZ-Lautsprecher) ---> [ PKW-INFOTAINMENT ]    |
|                                                                        ^                |
|                                      BT HFP 1.8 / A2DP oder USB-C      |                |
|                                                                        v                |
|                                                           [ ZENTRALBOX PCBA 01 ]        |
|                                                           (Dashboard Wedge Dock)        |
|                                                                     ^                   |
|                                        UWB Ch. 5 (< 0.4 ms)         |                   |
|                                                                     v                   |
|  [ AUTARKES OMM-MOBILTEIL ]                               [ KASSETTEN-POD BUCHT 1 ]     |
|  (Mittelkonsole / Beifahrer)                              (OMM 2.4 GHz UCS-Modul)       |
|  * PTT am Lenkrad / Schwanenhals                                    |                   |
|  * 2.4 GHz TDMA Mesh Direktverbindung                               | 2.4 GHz TDMA Mesh |
|  * Integrierter 600-mAh-Akku                                        | (10 ms Superframe)|
|             |                                                       |                   |
|             +==================== KONVOI-MESH ======================+                   |
|                                     |                                                   |
|                        v            v            v                                      |
|                   [ Bike 1 ]   [ Bike 2 ]   [ Bike 3 ]                                  |
+-----------------------------------------------------------------------------------------+
```

### 11.1 Autarke Pkw-Nutzung & Bedienkonzepte
1. **OMM-Mobilteil auf der Mittelkonsole:**
   * Das OMM 2.4 GHz Modul kann mit seinem integrierten 600-mAh-LiPo-Akku völlig autark auf der Mittelkonsole betrieben werden.
   * **Schwanenhals- oder Handmikrofon:** Über die USB-C-Buchse mit Audio-Adapter wird ein Schwanenhals-Mikrofon für den Beifahrer oder Tour-Guide angeschlossen.
   * **Drahtlose oder kabelgebundene Lenkrad-PTT:** Ein ergonomischer PTT-Taster an der Lenkradspeiche triggert über BLE oder Schalteingang die Sendeaufforderung (VAD-Override), sodass der Fahrer beide Hände am Lenkrad behält.

### 11.2 Drei flexible Audio-Routing-Pfade im Pkw
1. **Pfad 1: Pkw-Freisprecheinrichtung via Qualcomm QCC3084 Bluetooth:**
   * Der QCC3084 SoC auf der Zentralbox meldet sich am Infotainmentsystem des Pkw (BMW iDrive, Audi MMI, Mercedes MBUX, Ford Sync etc.) als Smartphone via Bluetooth Hands-Free Profile (HFP 1.8 mit Breitband mSBC) an.
   * Eingehende Gruppensprache wird über die KFZ-Lautsprecher wiedergegeben.
   * Sprache des Fahrers wird über das werkseitige Pkw-Dachmikrofon aufgenommen und verzögerungsfrei ins Mesh eingespeist.
2. **Pfad 2: Apple CarPlay / Android Auto & USB-Audio:**
   * Bei Verbindung der Zentralbox mit dem Pkw-USB-Port streamt der ESP32-S3 USB-Audio (UAC 2.0 Class Device) latenzfrei ins Pkw-Soundsystem.
   * Parallel dazu wird das PWA-Dashboard im Vollbildmodus auf dem Pkw-Display dargestellt.
3. **Pfad 3: Direkteinspeisung / Analog AUX:**
   * Über den Klinken-/Line-Out des ES8388 Codecs kann jedes Standard-Pkw-Radio mit 3,5-mm-AUX-Buchse ohne jegliche Latenz angebunden werden.

---

## 12. Zusammenfassung der Hardware- & Software-Vorteile von OMM 2.4 GHz

| Kriterium | Proprietäre OEM-Systeme (Sena / Cardo) | OpenMotorMesh (OMM) 2.4 GHz UCS Modul |
| :--- | :--- | :--- |
| **Quellcode & Lizenz** | Geschlossenes Binär-Protokoll, Vendor-Lock-in | **100 % Open Source** (GPLv3 / Apache 2.0) |
| **Hardware-Plattform** | Proprietäre ASICs / CSR / Qualcomm | **Espressif ESP32-C6 RISC-V + TI BQ24075 + ES8311** |
| **Formfaktor** | Proprietäre Klemmen & Modulformen | **ECE 22.06 UCS Standard ($68 \times 36 \times 9{,}5\,\text{mm}$)** |
| **Befestigung / Wartung** | Verklebt oder selbstschneidende Schrauben | **Formschlüssige DIN 934 M2 Mutterntaschen (Captive Nuts)** |
| **Audio-Latenz** | ca. $20\dots 35\,\text{ms}$ (proprietär) | **$< 18\,\text{ms}$** (deterministischer 10 ms TDMA Superframe) |
| **Netzwerk-Protokoll** | Proprietär, Black-Box | **Standardisiertes 6LoWPAN / IPv6-Multicast & RPL** |
| **Sprachkompression** | Proprietärer SBC / aptX Stream | **Opus HD ($24\,\text{kHz}$ Breitband mit adaptivem Jitter-Puffer)** |
| **Kanalverwaltung** | Max. 9 Kanäle (Sena) bzw. 1 Gruppe | **6 offene Multicast-Kanäle + AES-128-GCM Privatgruppen** |
| **Dual-Use Einsatz** | Nur am Helm oder nur im Bike | **Autark im Helm oder als Kassetten-Einsatz im Pod** |
| **Fahrzeug-Backbone** | Bluetooth (hohe Latenz, Jitter) | **Qorvo DW3110 UWB 6.5 GHz Backbone ($< 0{,}4\,\text{ms}$)** |
| **Begleitfahrzeug** | Schlechte Reichweite, keine Pkw-Integration | **CarPlay / Android Auto & BT-HFP über Zentralbox** |
| **Akku & Laufzeit** | Fest verbaut ($400\dots 500\,\text{mAh}$) | **Tauschbarer 600 mAh LiPo (12-14 h) + Bordnetz-Dauerladung** |
