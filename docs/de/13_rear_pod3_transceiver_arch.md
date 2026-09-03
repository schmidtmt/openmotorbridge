# 13 - Heck-Pod 3: GNSS & Dual-PHY OpenMotorMesh Transceiver-Architektur

Der **Heck-Pod 3** (Position: Heckbürzel / Gepäckbrücke) ist das zentrale Funk- und Navigations-Gateway des OpenMotorBridge-Systems. Er nutzt das identische, universelle **Maximal-Envelope Pod-Gehäuse ($120{,}0 \times 64{,}0 \times 32{,}0\,\text{mm}$)** und beherbergt auf seinem offenen Einschubschlitten das Multi-Konstellations-GNSS-Modul (**u-blox MAX-M10S**), das vollständige **Dual-PHY OpenMotorMesh (2.4 GHz High-Speed + 868 MHz LoRa Long-Range)** sowie einen dedizierten **ESP32-C3 RISC-V Co-Prozessor**.

---

## 1. Systemaufbau & 1-Tier Modular-Architektur

Die Heck-Kassette nutzt den **zu 100 % universellen Grundschlitten ([cartridge_base_sled.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/00_base_sled.scad))**, der auch für Pod 1 (Sena) und Pod 2 (Cardo) im Einsatz ist. Der $116 \times 58\,\text{mm}$ große Schlitten ist in zwei hochoptimierte Funktionskammern aufgeteilt:

1. **Vordere Kammer ($X = 0 \dots 56\,\text{mm}$): Kompakte OMM-Transceiver-Platine ($55{,}0 \times 48{,}0\,\text{mm}$)**
   - Vierzinkiges 4-Lagen FR4 TG150 ENIG Board mit ESP32-C3-WROOM-02U (U.FL-Anschluss), Semtech SX1262 LoRa, u-blox MAX-M10S Multi-GNSS, Maxim DS2401 ID-Chip, 500mA PTC-Schutzstufe und zentrierter 6-Pin Präzisions-Stirnseitenbuchse.
   - Fest verschraubt in vier M2-Bodendomen des universellen Grundschlittens ($X = 4{,}5\,\text{mm}$ und $X = 50{,}5\,\text{mm}$).
2. **Hintere Kammer ($X = 57 \dots 110\,\text{mm}$): Modularer Antennen-Halter ([04_antenna_bracket_omm.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/parts/04_antenna_bracket_omm.scad))**
   - Eigenständiger PA12-Trägerkörper, verschraubt in den beiden hinteren Original-Eckdomen des Grundschlittens.
   - **GNSS (GPS):** Erhöhter Decken-Halter für eine $18 \times 18\,\text{mm}$ (oder $25 \times 25\,\text{mm}$) RHCP-Keramik-Patchantenne, die plan nach oben durch den HF-transparenten PA12-Deckel in den Zenit blickt ($0\,\text{dB}$ Polarisationsverlust).
   - **LoRa (868 MHz):** Vertikales Seitenwand-Bett für eine flexible 868-MHz-FPC-Dipolantenne an der Gehäuseaußenwand (vollkommen verlustfreie Durchdringung des PA12-Gehäuses).
   - **2,4 GHz Audio-Mesh:** Führt das U.FL-Mikro-Koaxkabel des ESP32-C3 direkt zur wasserdichten SMA-Buchse an der Stirnseite für die externe High-Gain Stabantenne.
3. **Wasserdichter PA12-Deckel ([03_insert_blindkassette.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad))**
   - Verschließt die gesamte Oberseite hermetisch und dichtet gegen Straßenschmutz und Hochdruckreiniger (IP67 / IP69K) ab.

### 1.1 3D-CAD-Gesamtbaugruppe & Explosionsdarstellung

![OpenMotorBridge Heck-Pod 3 CAD Baugruppen-Explosionsansicht](../images/cad/pod3_full_assembly_exploded_3d.png)

*Abbildung 13.2: 3D-CAD-Explosionsdarstellung der Heck-Pod 3 Gesamtkassette: Universeller Grundschlitten (mit 6 M2-Bodendomen für universelle Kompatibilität mit allen Pods), kompakte OMM-Platine vorne, modularer Antennen-Halter hinten (mit Decken-GPS-Patch und Seitenwand-LoRa-FPC) und wetterfestem PA12-Deckel.*

---

## 2. Hardware-Architektur & Stirnwand-Steckschnittstelle

```
                      ┌─────────────────────────────────────────────────────────────┐
                      │          HECK-POD 3 OPENMOTORMESH TRANSCEIVER-MODUL         │
                      │         (110 x 52 mm im offenen Kassetten-Einschubschlitten)│
                      │                                                             │
                      │   • J1: Zentrierte 6-Pin Winkelbuchsenleiste (Stirnseite)   │
                      │   • F1: 500mA PTC-Sicherung & D1: 5V Power-Status-LED       │
                      │   • U4: DS2401 1-Wire ID ROM (openmotormesh_pod3.json)      │
                      │   • J3..J5: 3x Murata MM8030 automatische HF-Umschalter     │
                      │                                                             │
                      │   ┌─────────────────────────────────────────────────────┐   │
                      │   │  ESP32-C3 RISC-V Co-Prozessor (32-Bit @ 160 MHz)    │   │
                      │   │  • Primary PHY: 2.4 GHz IEEE 802.15.4 / SC-FDMA     │   │
                      │   │  • HiFi Audio (Opus 24k) & Nahbereichs-Mesh         │   │
                      │   └──────────┬───────────────────────────┬──────────────┘   │
                      │              │ SPI Master (8 MHz)        │ UART1 (115.2k)   │
                      │              ▼                           ▼                  │
                      │   ┌──────────────────────┐    ┌─────────────────────────┐   │
                      │   │ Semtech SX1262 LoRa  │    │ u-blox MAX-M10S GNSS    │   │
                      │   │ • Fallback PHY 868MHz│    │ • 10 Hz Multi-GNSS PVT  │   │
                      │   │ • Codec2 & Radar     │    │ • 1-PPS Zeitnormal      │   │
                      │   └──────────────────────┘    └─────────────────────────┘   │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │ Horizontaler Kassetteneinschub (Auto-Eject)
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ SCHUTZ-SCHOTTWAND MIT DUALEN AUSWERFER-FEDERN (2x M2)       │
                      │  • PA12-Trennwand (56 x 24 mm) kapselt Pod-Base hermetisch  │
                      │  • 6-Pin Stiftleiste in PA12-Schutzkragen mit 45° Trichter  │
                      │  • Duale V4A Edelstahlfedern werfen Schlitten 10mm aus      │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ POD-BASISPLATINE (openmotorbridge_pod_base, 48 x 24 mm)     │
                      │  • U1: SP3012 TVS-Schutzmatrix                              │
                      │  • J2: Zentrierte M8 6-Pin IP67 Buchse nach außen (B.Cu)    │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │ Geschirmtes 6-adriges PUR-Kabel
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ HD26 Flanschbuchse -> Zentralbox ESP32-S3 Hauptrechner      │
                      └─────────────────────────────────────────────────────────────┘
```

---

## 2. Das Dual-PHY OpenMotorMesh im Heck-Pod 3

| Merkmal | **Primary PHY (2.4 GHz High-Speed Mesh)** | **Secondary Fallback PHY (868 MHz LoRa)** |
| :--- | :--- | :--- |
| **Hardware-Treiber** | **ESP32-C3 Internes 2.4-GHz-Radio** | **Semtech SX1262 Transceiver (+22 dBm)** |
| **Standard / Protokoll** | IEEE 802.15.4 / SC-FDMA TDMA (2 Mbps) | LoRa Chirp Spread Spectrum (BW 250 kHz, SF7) |
| **Antenne im Pod 3** | Pulse W3000 2.4 GHz Keramikantenne (`ANT3`) + Murata MM8030 Umschalter (`J3`) auf SMA | Pulse W3000 868-MHz-Keramik-Chipantenne (`ANT1`) + Murata MM8030 Umschalter (`J4`) auf SMA |
| **Audio-Codec** | **Opus Speech/Full-Band (24 kbps / 12 kbps)** | **Codec2 (1200 bps / 700 bps PTT Bursts)** |
| **Audio-Modus** | **Vollduplex kontinuierlich (HiFi Sprache)** | **Halbduplex PTT-Bursts (220 ms max.)** |
| **Musik-Sharing** | Ja (A2DP Dynamic Forwarding @ 64 kbps) | Nein (Bandbreite reserviert fuer Sprache) |
| **Telemetrie-Rate** | 10 Hz Echtzeit-Lage & Dynamik-Stream | 1 Hz komprimiertes Gruppenradar (12 Bytes) |
| **Typische Reichweite**| $150\,\text{m}$ bis $300\,\text{m}$ (Sichtverbindung) | **$1{,}0\,\text{km}$ bis $15{,}0\,\text{km}$ (Multi-Hop)** |
| **Hauptzweck** | Primaeres Gruppen-Intercom & Audiobruecke | **Automatischer Fallback bei Gruppenabriss** |

---

## 3. Kern-Bauelemente im Heck-Pod 3

1. **Haupt-Co-Prozessor (ESP32-C3-WROOM-02U mit HF-Schaltbuchse):**
   * 32-Bit RISC-V Single-Core @ 160 MHz mit 4 MB Embedded Flash.
   * Sendet und empfaengt das **2.4 GHz Primary High-Speed Mesh** (Opus 24k HiFi-Audio & 10 Hz Telemetrie).
   * Uebernimmt lokales 10 Hz NMEA/UBX-Parsing vom MAX-M10S und SPI-Steuerung des LoRa-Modems.
2. **GNSS Engine (u-blox MAX-M10S):**
   * Multi-Konstellation 4-System Parallelbetrieb (GPS, GLONASS, Galileo, BeiDou).
   * 1-PPS Hardware-Zeitsignal (Jitter $< 15\,\text{ns}$ RMS) an ESP32-C3 GPIO 6 und ueber Buchsenkontakt 5 an Zentralbox.
3. **OpenMotorMesh LoRa Transceiver (Semtech SX1262):**
   * Frequenzbereich: 868.0 – 868.6 MHz (EU ISM Band) / 915 MHz (US Band).
   * Sendeleistung: bis zu $+22\,\text{dBm}$ ($160\,\text{mW}$ EIRP).
   * Integrierter HF-Schalter, Tiefpassfilter und automatische Antennenumschaltung.
4. **1-Wire Identifikation (Maxim / ADI DS2401Z+):**
   * Liefert die 64-Bit Silicon Serial Number fuer die automatische Kassetten- und Steckplatzerkennung an der Zentralbox.
5. **Spannungsregelung (TI TPS7A0533):**
   * Ultra-Low-Noise Automotive LDO (5.0V Eingang $\rightarrow$ saubere 3.3V / 200mA fuer GNSS & LoRa).

---

### 3.1 Universelle HF-Schaltbuchsen-Architektur: Automatische Antennenumschaltung

Um maximale Flexibilität zu gewährleisten, sind **alle 3 Funk- und Navigationspfade** der Transceiver-Platine mit miniaturisierten **mechanischen HF-Schaltbuchsen (z. B. Murata MM8030-2610 / SWG-Serie)** ausgestattet.

```
                  FUNKTIONSPRINZIP DER HF-SCHALTBUCHSEN
  1. NORMALZUSTAND (Kein Kabel gesteckt)   2. GESTECKT (Pigtail zur SMA-Frontbuchse)
┌──────────────────────────────────────┐ ┌──────────────────────────────────────┐
│  HF-Chip ──► [Federkontakt] ──► Ant  │ │  HF-Chip ──► [Koax-Stecker] ──► SMA  │
│              (Geschlossen)   (Intern)│ │              (Offen!)         (Aussen)│
│                                      │ │              [Getrennt] ─X─► Ant     │
└──────────────────────────────────────┘ └──────────────────────────────────────┘
```

#### Das mechanische Umschaltprinzip:
* **Ohne Stecker (Normalbetrieb):** Eine federnde Beryllium-Kupfer-Zunge in der Buchse leitet das HF-Signal verlustfrei ($< 0{,}08\,\text{dB}$ Dämpfung) direkt auf die interne Onboard-Antenne (Pulse W3000 Keramik-Chip bzw. PCB-Antenne).
* **Mit Stecker (Koax-Pigtail eingeklinkt):** Beim Einschieben des Pigtail-Steckers drückt der Mittelkontakt die interne Feder mechanisch zur Seite:
  * Die Verbindung zur internen Onboard-Antenne wird **vollständig und automatisch unterbrochen** ($> 20\,\text{dB}$ Isolation).
  * 100 % der HF-Leistung werden verlustfrei auf das Koaxialkabel zur externen SMA-Frontblendenbuchse geleitet.
* **Beim Abziehen:** Die Federzunge schnappt sofort zurück – die interne Antenne ist ohne Löt- oder Konfigurationsaufwand augenblicklich wieder aktiv!

#### Die 3 Schaltbuchsen auf der Platine & das Steck-Szenario:
1. **Buchse `J3` (2.4 GHz Primary High-Speed Mesh – ESP32-C3) ──► [WERKSEITIGER DEFAULT]:**
   * Das interne Pigtail zur SMA-Frontblendenbuchse ist **ab Werk auf `J3` gesteckt**.
   * **Warum 2.4 GHz die Default-Wahl ist:** Der 2.4-GHz-Kanal überträgt das bandbreitenintensive **Opus-HiFi-Vollduplex-Audio** und hat mit interner Antenne physikalisch die kürzeste Reichweite ($150\dots 300\,\text{m}$). Durch Anschrauben einer winzigen 2,4-GHz-Stummelantenne ($\approx 30\,\text{mm}$ kurz) an der Kassettenblende springt die HiFi-Sprachreichweite auf **$600\dots 1.000\,\text{m}$**. Die Gruppe bleibt dauerhaft im glasklaren Stereo-Chat, ohne vorzeitig auf den schmalbandigen LoRa-Notfunk zurückzufallen!
2. **Buchse `J4` (868 MHz LoRa Fallback – Semtech SX1262):**
   * Läuft standardmäßig autark über die interne Pulse W3000 Keramik-Chipantenne ($1\dots 2{,}5\,\text{km}$ LoRa-Reichweite).
   * **Expeditions-Option:** Für Extrem-Touren im Gebirge oder in der Wüste kann der Fahrer das Pigtail werkzeuglos von `J3` auf `J4` umstecken. `J3` reaktiviert sofort seine interne 2.4-GHz-Antenne, während LoRa auf die externe Antenne geschaltet wird (**$> 25\,\text{km}$ LoRa-Reichweite**).
3. **Buchse `J5` (Multi-GNSS – u-blox MAX-M10S):**
   * Läuft standardmäßig autark über die interne GNSS-Keramikantenne.
   * **Alukoffer- / Gepäck-Option:** Falls schwere Alukoffer oder wasserdichte Zeltrollen direkt über dem Heck-Pod 3 montiert sind und die Satellitensicht abschirmen, kann das Pigtail auf `J5` gesteckt werden, um eine externe aktive GNSS-Patchantenne an der Heckspitze zu speisen.

---

## 4. Interne ESP32-C3 GPIO-Belegung

| ESP32-C3 GPIO | Peripherie / Signal | Richtung | Funktion |
| :--- | :--- | :---: | :--- |
| **GPIO 21** | `BRIDGE_TXD` | Output | High-Speed UART0 Tx zur Zentralbox (460.800 Baud) |
| **GPIO 20** | `BRIDGE_RXD` | Input | High-Speed UART0 Rx von Zentralbox (460.800 Baud) |
| **GPIO 4** | `GNSS_TXD` | Output | UART1 Tx zum u-blox MAX-M10S (115.200 Baud) |
| **GPIO 5** | `GNSS_RXD` | Input | UART1 Rx vom u-blox MAX-M10S (115.200 Baud) |
| **GPIO 6** | `GNSS_PPS` | Input (IRQ) | 1-PPS Hardware-Zeitsignal Interrupt |
| **GPIO 8** | `LORA_SCK` | Output | SX1262 SPI Clock (8 MHz) |
| **GPIO 9** | `LORA_MISO`| Input | SX1262 SPI Master-In Slave-Out |
| **GPIO 10** | `LORA_MOSI`| Output | SX1262 SPI Master-Out Slave-In |
| **GPIO 7** | `LORA_NSS` | Output | SX1262 SPI Chip Select |
| **GPIO 3** | `LORA_NRST`| Output | SX1262 Hardware-Reset |
| **GPIO 2** | `LORA_BUSY`| Input | SX1262 Status Busy |
| **GPIO 1** | `LORA_DIO1`| Input (IRQ) | SX1262 Packet Received / Transmit Done Interrupt |

---

## 5. Belegung der 6-Pin Pogo-Kontaktleiste

| Pogo-Pin | Signalname | Elektrische Spezifikation | Beschreibung |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `POD3_VCC` | 5.0 V DC (max. 250 mA) | Dauer-Versorgung ueber Zentralbox |
| **Pin 2** | `POD3_GND` | Power- & Signalmasse | Dedizierte Rueckleitung |
| **Pin 3** | `POD3_UART_TX` | 3.3 V LVTTL (460.800 Baud) | Datenstrom vom ESP32-C3 zur Zentralbox |
| **Pin 4** | `POD3_UART_RX` | 3.3 V LVTTL (460.800 Baud) | Steuerkommandos von Zentralbox zum ESP32-C3 |
| **Pin 5** | `POD3_GNSS_PPS`| 3.3 V Impuls (100 ms Breite) | 1-PPS Hardware-Zeitnormal-Synchronisation |
| **Pin 6** | `POD3_1WIRE_ID`| 1-Wire Open-Drain (3.3 V) | DS2401 Kassetten-Identifikationsbus |

---

## 6. Protokoll-Spezifikation (Heck-Pod $\leftrightarrow$ Zentralbox)

Die Kommunikation ueber die 460.800-Baud-Schnittstelle erfolgt paketorientiert mit CRC16-CCITT-Pruefsumme:

```
┌──────┬──────┬──────┬──────┬─────────────────┬──────┬──────┐
│ SYNC │ TYPE │ LEN  │ SEQ  │ PAYLOAD (0..n)  │ CRC16-CCITT  │
│ 0xAA │ 0x55 │ 1 B  │ 1 B  │ Variable        │ 2 Bytes      │
└──────┴──────┴──────┴──────┴─────────────────┴──────┴──────┘
```

### Nachrichtentypen (Message Types):
* **`0x01` - GNSS PVT Telemetrie (10 Hz):** Vorkomprimierter Binaervektor mit Latitude, Longitude, Altitude, Speed, Heading, PDOP und Satellitenstatus.
* **`0x02` - OMM 2.4 GHz Primary Audio Frame:** Opus 24k/12k Frame aus dem 2.4 GHz Proximity Mesh.
* **`0x03` - OMM 868 MHz LoRa Fallback Frame:** Codec2 Audio- oder Radar-Paket aus dem Long-Range Fallback.
* **`0x04` - OMM Tx Request (Dual-PHY):** Sendeauftrag der Zentralbox an das 2.4 GHz Mesh oder den SX1262 LoRa Transceiver.
* **`0x05` - DLE Status & Link Quality:** Signal-to-Noise Ratio (SNR), RSSI, PHY-Modus (2.4G vs 868M) und DLE Gateway-Score des Knotens.
* **`0xFE` - Firmware Update Bootloader Command:** `0xAA 0x55 0xFE 0x01 "BOOT"` leitet den ESP32-C3 ROM-Bootloader für das High-Speed UART Push-Flashen ein.

---

## 7. Firmware-Update & Fertigungs-Prüfschnittstelle

### 7.1 In-System UART-Push-Flashen (Fahrbetrieb)
* **Kein Gehäuseöffnen:** Updates werden transparent über die bestehende 6-Pin Kontaktleiste (`UART_TX` / `UART_RX`) eingespielt.
* **Synchroner Bootloader-Sprung:** Die Zentralbox steuert über `0xFE` und einen 100-ms Power-Cycle auf `POD3_VCC` den Download-Modus.
* **Übertragungsrate:** 460.800 Baud SLIP-Protokoll mit automatischer MD5-Prüfung ($< 6\,\text{s}$).

### 7.2 Fertigungs- & Entwicklungs-Testpunkte (Bottom Layer `B.Cu`)
Für die Erstprogrammierung und EOL-Prüfung in der Fertigung befinden sich auf der Unterseite standardisierte 1,0 mm SMD-Prüfpads:
* **`TP1` (TP_BOOT):** ESP32-C3 GPIO9 (Low-Aktiv für Bootloader)
* **`TP2` (TP_RST):** CHIP_PU (Hardware Reset)
* **`TP3` (TP_TX):** ESP32-C3 UART0 TX (GPIO21)
* **`TP4` (TP_RX):** ESP32-C3 UART0 RX (GPIO20)

---

## 8. Ausblick & Upgrade-Roadmap: Optionale LTE-M / 4G Cloud-Kassette & HF-Triplexer

### 8.1 Status quo V1 (Fokus auf Robustheit & Autarkie)
In der Version 1 konzentriert sich der Heck-Pod 3 auf das **robuste, kostenfreie Nah- und Weitverkehrs-Funknetzwerk**:
* **3x Onboard-Keramik-Chipantennen (Pulse W3000):** Vollständig gekapselt im PA12-Gehäuse für $868\,\text{MHz}$ LoRa, $1575\,\text{MHz}$ GNSS und $2{,}4\,\text{GHz}$ Mesh/BLE.
* **3x Murata MM8030 HF-Umschaltbuchsen:** Erlauben wahlweise das gezielte Herausführen eines Funkpfads auf eine externe SMA-Antenne.
* **Smartphone als Cloud-Gateway:** Die Internetanbindung (Cloud-Sync, WebApp-Karten, Notruf) erfolgt kostenlos und ohne extra SIM-Karte über das Smartphone des Fahrers am Smart Fairing Hub.

### 8.2 Upgrade-Pfad V2: Autarke LTE-M / NB-IoT Cloud-Kassette
Dank der modularen Kassetten-Architektur kann das System in einer späteren Ausbaustufe ohne Änderungen am Gehäuse oder Kabelbaum zu einem vollautonomen IoT-Cloud-Tracker aufgerüstet werden:

1. **Optionale Kassetten-Platine (`cartridge_omm_transceiver_lte`):**
   * Ein ultrakompaktes LTE Cat-1 bis / LTE-M IoT-Modem (z. B. *Quectel EG915N* oder *SIMCom SIM7080G*) wird auf dem großzügigen $110 \times 52\,\text{mm}$ Board integriert.
   * **Konnektivität:** Integrierte eSIM oder Nano-SIM (z. B. *1NCE IoT-Flat*: 10 € für 10 Jahre / 500 MB Datenvolumen ohne Monatsgebühr).
2. **HF-Triplexer (Frequenzweiche für 1-Kabel-Breitbandantenne):**
   * Statt drei separater Antennen oder manueller Umschalter kaskadiert die V2-Platine zwei keramische LTCC-Diplexer (0603 Bauform):
     * *Diplexer 1:* Trennt $868\,\text{MHz}$ LoRa / LTE-Low-Band ab.
     * *Diplexer 2:* Trennt $1575\,\text{MHz}$ GNSS und $2400\,\text{MHz}$ Mesh / LTE-High-Band ab.
     * *GNSS-Schutz:* Ein SAW-Bandpassfilter mit $> 50\,\text{dB}$ Dämpfung schützt den u-blox LNA vor Übersteuerung durch LoRa- und LTE-Sendeimpulse.
   * **Antenne:** Eine einzige externe Breitband-Kompaktantenne ($700 \dots 2700\,\text{MHz}$, z. B. Taoglas / Pulse LTE-Whip) speist alle Funkmodule gleichzeitig.
3. **Zusatzfunktionen der V2-Cloud-Kassette:**
   * **Autarkes eCall (Unfall-Notruf):** Setzt bei Sturzerkennung (IMU) automatisch Notruf-SMS und GPS-Koordinaten an Rettungsleitstellen ab – selbst wenn das Smartphone zerstört oder verloren ist.
   * **Diebstahlüberwachung & Geofencing:** Sendet Live-Positionen und Batterie-Warnungen auf das Smartphone, wenn das geparkte Motorrad bewegt wird.
   * **Unendliche Gruppen-Mesh-Brücke:** Bei Abreißen des LoRa-Sichtkontakts (z. B. in tiefen Tälern oder bei großer Gruppendistanz) wird die Sprach- und Positionsübertragung nahtlos über MQTT/Mobilfunk weitergeleitet.

