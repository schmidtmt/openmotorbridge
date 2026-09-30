# 04 - LoRa 868MHz Schwarm-Backbone, Link-State-Bridging & Zero-Touch Gruppen-Lifecycle

Dieses Dokument spezifiziert das fahrzeugübergreifende Weitbereichs- und Schwarm-Backbone der OpenMotorBridge v9.6 Clean Architecture: das **3-Kanal LoRa 868 MHz Funknetzwerk**, den **Zero-Touch Gruppen-Lifecycle** (selbstorganisierende Gruppenbildung ohne Tastendruck), den **schleifenfreien Link-State Audio Bridging Graph** (Precomputed Routing-Matrizen, First-Receiver-Wins Schiedsverfahren, Do-Not-Translate Flags) sowie die taktische **LoRa Voice Fallback Engine** bei Kolonnensplits.

> [!NOTE]
> * Das optionale **OpenMotorMesh 2.4 GHz HD-Audio Kassetten-Modul** (UCS-kompatibles OEM-Modul mit eigenem Mesh 3.0 / ESP-NOW) wird ausführlich im eigenständigen Dokument [04b - OMM 2.4 GHz Intercom & OEM-Kassette](file:///Users/schmidtm/openMotorBridge/docs/de/04b_omm_intercom_module.md) beschrieben.
> * Die Sensorfusion der Koppelnavigation (**Automotive Dead Reckoning - ADR**), u-blox SAM-M10Q Multi-GNSS, IMU-Neigungsmessung und Actioncam-Zeitsynchronisation werden im Dokument [06 - Telemetrie, Sensorfusion, Blackbox & WebDAV](file:///Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md) behandelt.

---

## 1. 3-Kanal LoRa 868 MHz Frequenz- & Spektrums-Architektur

Zur strikten Entkopplung von Gruppenbildung, taktischem Schwarmdatenaustausch und fahrzeugeigener Sicherheitsperipherie arbeitet das Semtech SX1262 LoRa-Subsystem auf der Zentralbox (`PCBA 01`) auf **drei logisch und frequenzmäßig getrennten Kanälen** im europäischen 868-MHz-SRD/ISM-Band:

```
+-----------------------------------------------------------------------------------------+
|                       3-KANAL LORA 868 MHz SPEKTRUMS-ARCHITEKTUR                        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  KANAL 1: 868.100 MHz (SF7 / BW 125 kHz / Unverschlüsselt)                             |
|  * Offenes Announce-Beaconing (Radius < 25 m, Δt < 60 s)                                |
|  * Ephemerer ECDH-Schlüsselaustausch zur Gruppeninitiierung                             |
|  * EU-weiter offener eCall-Notruftunnel (Kollisionsmeldung & GPS-Pings)                 |
|                                                                                         |
|  KANAL 2: 868.300 MHz (SF8 / BW 250 kHz / AES-128-GCM Verschlüsselt)                    |
|  * Taktische Kolonnen-Telemetrie & Relativ-Radar (5 Hz Intervall)                        |
|  * Link-State Bridging Status ("First-Receiver-Wins" Arbitrierung in < 8 ms)            |
|  * Taktischer PTT-Sprachburst (Codec2 1200 bps / Opus 6 kbps bei Kolonnenabriss)        |
|                                                                                         |
|  KANAL 3: 868.500 MHz (SF10 / BW 125 kHz / Peer-to-Peer Verschlüsselt)                  |
|  * Privater Sicherheitskanal: Zentralbox (PCBA 01) <--> Smart-Keyfob & Pager (PCBA 07)  |
|  * Bis zu 4,5 km Freifeld-Reichweite für Park-Alarme (IMU-Erschütterung, Kassettenraub) |
+-----------------------------------------------------------------------------------------+
```

### 1.1 HF-Parameter & ETSI-Konformität

| Kanal | Frequenz | Sendeleistung | Spreading Factor / BW | Max. Airtime | Verwendungszweck |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Kanal 1 (Discovery)** | 868.100 MHz | +14 dBm (25 mW) | SF7 / 125 kHz | $\approx 28\,\text{ms}$ | Offenes Beaconing, Announce, Notruf |
| **Kanal 2 (Group Data)** | 868.300 MHz | +14 dBm (25 mW) | SF8 / 250 kHz | $\approx 18\,\text{ms}$ | Dynamischer Schwarm & Link-State Matrix |
| **Kanal 2 (Voice Fallback)**| 868.300 MHz | +22 dBm (160 mW)*| SF7 / 250 kHz | $\approx 120\,\text{ms}$ | Notfall-PTT Sprache (Duty-Cycle geregelt) |
| **Kanal 3 (Smart Keyfob)** | 868.500 MHz | +22 dBm (160 mW) | SF10 / 125 kHz | $\approx 180\,\text{ms}$ | Bike-Sentry Alarm & Pager-Quittung |

*\*Hintergrund zur Sendeleistung: Gemäß ETSI EN 300 220 ist im Subband 868.0-868.6 MHz bis zu +14 dBm bei 1 % Duty Cycle zulässig. Für Notruf- und Voice-Bursts schaltet der SX1262 über seine integrierte High-Power PA kurzzeitig auf bis zu +22 dBm bei strenger Duty-Cycle-Budgetierung.*

---

## 2. Zero-Touch Gruppen-Lifecycle (Vollautomatische Gruppenbildung)

Ein fundamentaler Schwachpunkt bisheriger Motorrad-Funksysteme ist das manuelle Koppeln am Start: Fahrer müssen Knöpfe drücken, Apps synchronisieren oder QR-Codes scannen. OpenMotorBridge führt einen **vollkommen berührungslosen (Zero-Touch) Gruppen-Lifecycle** ein:

```
+-----------------------------------------------------------------------------------------+
|                        ZERO-TOUCH GRUPPENBILDUNGS-AUTOMAT                               |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ 1. PROXIMITY DISCOVERY ]  Distanz < 25 m, Zeitfenster Δt < 60 s, UTC-Zeitsync        |
|             |                                                                           |
|             v                                                                           |
|  [ 2. HEADING FILTER ]       Fahrstart: Kursabweichung ΔHeading < 30°                   |
|             |                Geschwindigkeit v > 25 km/h für Dauer t > 120 s            |
|             v                                                                           |
|  [ 3. KEY EXCHANGE ]         Autonomer ECDH Ephemeral Key-Exchange auf Kanal 1           |
|             |                Erzeugung des gemeinsamen AES-128 Session-Keys             |
|             v                                                                           |
|  [ 4. GROUP ACTIVE ]         Aktives Schwarm-Mesh auf Kanal 2 mit Link-State Bridging   |
|             |                                                                           |
|       +-----+-------------------------+                                                 |
|       v                               v                                                 |
|  [ 5. KAFFEEPAUSE ]          [ 6. IN-FLIGHT JOIN / SPLIT ]                              |
|  * Zündung AUS (60 min)      * Rolling Merge bei Treffen unterwegs                      |
|  * Mesh-State im NVRAM       * Intentional Split vs. echter Abriss (Doubt-Timer)        |
+-----------------------------------------------------------------------------------------+
```

### 2.1 Stufe 1: Raum-Zeitliche Nahbereichs-Erkennung (Proximity Discovery)
* Treffen sich mehrere OMB-Bikes an einer Tankstelle, einem Parkplatz oder vor der Garage, senden sie auf Kanal 1 (868.100 MHz) ein unverschlüsseltes, kurzes Discovery-Beacon.
* **Filterkriterien:**
  1. **Geografischer Radius:** Berechnet aus den u-blox SAM-M10Q GNSS-Koordinaten: $d < 25\,\text{m}$.
  2. **Zeitfenster:** Gemeinsame Präsenz im Radius über mindestens $\Delta t \ge 60\,\text{Sekunden}$.
  3. **UTC-Synchronisation:** 1-PPS GNSS-Zeitstempel validieren, dass alle Bikes denselben realen Zeitpunkt teilen (Schutz vor alten GPS-Geisterdaten).

### 2.2 Stufe 2: Vektor-Kohärenz & Fahrtrichtungs-Filter (Heading & Velocity)
Verhindert, dass fremde Motorräder, die zufällig an derselben Ampel oder Tankstelle stehen, ungewollt der Gruppe beitreten:
* Fahren die Bikes los, überwacht der ESP32-S3 für **$120\,\text{Sekunden}$**:
  * **Geschwindigkeit:** $v > 25\,\text{km/h}$.
  * **Fahrtrichtungs-Kohärenz:** Die Differenz der Kompasskurse (GNSS Heading) muss $\Delta\text{Heading} < 30^\circ$ betragen.
* Erst wenn beide Kriterien 120 Sekunden lang kontinuierlich erfüllt sind, gilt die Gruppe als bestätigt.

### 2.3 Stufe 3: Dynamischer Schlüssel-Austausch (ECDH Key Exchange)
* Die bestätigten Bikes führen über Kanal 1 einen ephemeren **Elliptic Curve Diffie-Hellman (ECDH auf Curve25519)** Schlüsselaustausch durch.
* Es wird ein kryptografisch sicherer **AES-128 Gruppen-Sitzungsschlüssel** generiert.
* Ab diesem Zeitpunkt schalten alle Nodes auf Kanal 2 (868.300 MHz) um. Abhörsicherheit und Integritätsschutz (AES-128-GCM) sind für die gesamte Tagestour gewährleistet.

### 2.4 Stufe 4: 60-Minuten Kaffeepausen-Persistenz (Mesh State Keep-Alive)
* Halten die Fahrer für eine Pause an und schalten die Zündung aus (KL15 AUS), verfällt die Gruppe **nicht**:
* Der ESP32-S3 sichert den vollständigen Gruppen-State (Node-IDs, AES-Session-Key, Link-State-Topologie) im batteriegepufferten RTC-Fast-SRAM und SPI-Flash NVRAM.
* Die Zentralbox wechselt in den energiearmen Light Standby ($< 15\,\text{mA}$).
* **Wiederaufnahme:** Schalten die Fahrer innerhalb von **60 Minuten** die Zündung wieder ein, wird die Gruppe **in $< 1{,}5\,\text{Sekunden}$ ohne erneutes Pairing oder Discovery nahtlos fortgesetzt**.

### 2.5 Stufe 5: In-Flight Join & Rolling Merge (Spontaner Beitritt unterwegs)
Kommt ein Fahrer später hinzu (z. B. Treffpunkt an einer Autobahnauffahrt während der Fahrt):
* **3-Stufen Vektor-Koinzidenzfilter:**
  1. Relativer Abstand: $d < 50\,\text{m}$.
  2. Geschwindigkeitsdifferenz: $\Delta v < 15\,\text{km/h}$.
  3. Kursdifferenz: $\Delta\text{Heading} < 20^\circ$ über ein Beobachtungsfenster von mindestens **$30\,\text{Sekunden}$**.
* Nach Erfüllung initiiert der beitretende Node einen Challenge-Response-Handshake auf Kanal 1. Der aktuelle Gruppen-Leader (höchster DLE-Score) übermittelt den verschlüsselten Session-Key für Kanal 2.

### 2.6 Stufe 6: Geplante Trennung (Dispersion) vs. Notfall-Abriss (Doubt Timer)
Verlässt ein Fahrer die Gruppe absichtlich (z. B. früheres Abbiegen nach Hause), darf kein Notfallalarm ausgelöst werden:
* **Absichtliche Trennung (Graceful Dispersion):** Biegt ein Bike an einer Kreuzung ab und weicht der Kurs für $> 20\,\text{s}$ um $> 45^\circ$ von der Kolonnenachse ab, klassifiziert der Algorithmus dies als beabsichtigten Split. Der Node wird lautlos aus der aktiven Mesh-Tabelle ausgetragen.
* **Echter Abriss (Unbeabsichtigter Verlust):**
  * Bricht der Heartbeat ab, während das Bike denselben Kurs und dieselbe Straße fuhr (z. B. Sturz, Panne oder Felswand), startet ein **20 bis 30 Sekunden Doubt-Timer** (Zweifel-Timer).
  * Bleibt die Funkverbindung nach Ablauf des Doubt-Timers abgerissen, aktiviert sich automatisch die LoRa Fallback Engine.

---

## 3. Schleifenfreier Link-State Audio Bridging Graph

Sind in einer Gruppe unterschiedliche Headset-Ökosysteme vertreten (z. B. Fahrer A mit Sena Mesh 3.0, Fahrer B mit Cardo DMC, Fahrer C mit beiden Systemen im Bike), darf **keine unkontrollierte Echo-Schleife (Feedback Loop)** entstehen:

```
                  SCHLEIFENFREIER AUDIO-ÜBERGANGSGRAF
                  
  [ FAHRER 1 (SENA) ] <-- Sena Mesh --> [ OMB NODE A (Sena + Cardo) ]
                                                   |
                                                   | Übersetzung: Sena -> Cardo
                                                   v
  [ FAHRER 2 (CARDO) ] <-- Cardo DMC --> [ OMB NODE B (Sena + Cardo) ]
            |                                      |
            +----------- BLOCKIERT! ---------------+
            (Node B erkennt via LoRa: Node A übersetzt bereits!
             Keine Rückübersetzung Cardo -> Sena -> Null Echo!)
```

### 3.1 Entkopplung vom klassischen DLE & Precomputed Routing Matrizen
* In v9.6 Clean Architecture ist OMM 2.4 GHz eine optionale Wechselkassette. Die Brücken-Entscheidung darf daher **nicht von einem zentralen OMM-Leader abhängen**.
* Jeder Knoten ermittelt autonom seine angebundenen Kassetten-Klassen (Sena, Cardo, OMM 2.4, Midland) und berechnet daraus seinen **Capability-Score**:
  $$\text{Score}_{\text{Bridge}} = S_{\text{HW\_Kombi}} + S_{\text{RSSI}} + S_{\text{PWR}} + S_{\text{HYST}}$$
* Im Speicher jedes ESP32-S3 liegt eine **offline vorberechnete Link-State Matrix**, die für jede denkbare Gruppenkonstellation vorab festlegt, welche Knoten als primäre und sekundäre Brücken fungieren.

### 3.2 First-Receiver-Wins (FRW) Arbitrierung via LoRa
Trifft ein Sprachpaket an zwei Bikes gleichzeitig ein, die beide zwischen Sena und Cardo übersetzen könnten:
1. **Erster Empfänger gewinnt:** Der Knoten, dessen Audio-ADC/Codec die Sprache zuerst detektiert, sendet in **$< 8\,\text{ms}$** ein kurzes Arbitrierungs-Paket auf LoRa Kanal 2:
   `LORA_PKT_BRIDGING_ACTIVE { Source: SENA, Target: CARDO, Node: 0x4A, Seq: 1042 }`
2. **Unterdrückung bei Nachbarknoten:** Alle anderen Dual-Kassetten-Bikes empfangen diesen LoRa-Hinweis und sperren ihre eigene Audio-Weiterleitung von Sena nach Cardo für die Dauer der Sprachaktivität ($+ 400\,\text{ms}$ Hangover-Zeit).
3. **Ergebnis:** Es übersetzt zu jedem Zeitpunkt exakt ein einziger Knoten. Doppeleinspeisungen und Phasenverzögerungen sind ausgeschlossen.

### 3.3 Do-Not-Translate (DNT) Header-Flag & Anti-Loop Schutz
* Wird ein Audiosignal von einem Netzwerk ins andere übersetzt (z. B. Sena $\rightarrow$ Cardo), injiziert der übersetzende Knoten ein digitales Kontroll-Flag (`FLAG_DO_NOT_TRANSLATE`).
* Empfängt ein anderes OMB-Bike im Cardo-Netzwerk dieses Sprachpaket, erkennt die DSP-Pipeline anhand des DNT-Flags sofort, dass dieses Audiosignal ursprünglich aus dem Sena-Netzwerk stammt.
* **Strikte Sperre:** Eine Rückübersetzung in Richtung Sena wird hardware- und softwareseitig **hart blockiert**. Akustische Rückkopplungsschleifen (Feedback Loops) sind physikalisch unmöglich.

### 3.4 Strikte LoRa-Audio-Einweg-Regel (LoRa Voice One-Way Rule)
Das 868-MHz-Band bietet nur begrenzte Bandbreite und unterliegt gesetzlichen Duty-Cycle-Beschränkungen. Daher gilt eine unverletzliche Systemregel:
* **Über LoRa Voice Fallback wird AUSSCHLIESSLICH das Mikrofonsignal des lokalen Fahrers übertragen!**
* Funkverkehr, der aus einem lokalen 2.4-GHz-Mesh (Sena oder Cardo) empfangen wird, darf **unter keinen Umständen** in das LoRa-Netzwerk re-injiziert werden.
* Dies verhindert, dass ein einzelner entfernter Fahrer das gesamte LoRa-Band mit unkontrolliertem Gruppenlärm belegt.

---

## 4. Taktische LoRa Fallback Engine & PTT Voice Bursts

Reißt der 2.4-GHz-Intercom-Kontakt in Gebirgspässen für länger als die $20\dots 30\,\text{s}$ des Doubt-Timers ab:

```
+-----------------------------------------------------------------------------------------+
|                     LORA TACTICAL VOICE FALLBACK ENGINE (868 MHz)                       |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ GRUPPE ZERRISSEN ] --> Doubt-Timer abgelaufen (20..30 s)                             |
|                                  |                                                      |
|                                  v                                                      |
|  [ STUFE 1: 25-Byte RADAR ]  GPS-Position, Kurs, Speed & Status (Airtime ~18 ms)        |
|                                  |                                                      |
|                                  v                                                      |
|  [ STUFE 2: TTS WARNUNG ]    "🚨 Achtung: Michael 1,8 km zurückgefallen, steht."        |
|                                  |                                                      |
|                                  v                                                      |
|  [ STUFE 3: CODEC2 PTT ]     3 s Sprache in 450 Bytes via SF7 (Airtime ~120 ms)         |
|                              Überträgt STRIKT nur lokales Mikrofon                      |
+-----------------------------------------------------------------------------------------+
```

1. **Stufe 1 - Taktisches 25-Byte Not-Telemetrie-Paket (LoRa Kanal 2):**
   * Sendet Node-ID, präzise GPS-Koordinaten (SAM-M10Q), Geschwindigkeit, Kurs, Bordspannung und Stillstand-Flag. Airtime nur $\approx 18\,\text{ms}$ (vollständig ETSI 1 % konform).
2. **Stufe 2 - Automatische Text-to-Speech (TTS) Ansage im Helm der Gruppe:**
   * Die Zentralboxen der verbleibenden Fahrer synthetisieren sofort eine klare Durchsage direkt ins Headset:
     > *"🚨 Achtung: Michael 1,8 km zurückgefallen, Fahrzeug steht."*
3. **Stufe 3 - Taktischer PTT-Sprachburst via Codec2 (1200 bps) / Opus (6 kbps):**
   * Benötigt der isolierte Fahrer Hilfe, hält er die Lenker-PTT gedrückt.
   * Der ESP32-S3 komprimiert 3 Sekunden Sprache in nur 450 Bytes.
   * Die Übertragung erfolgt über LoRa in ca. $120\,\text{ms}$ Airtime - mit $1\dots 15\,\text{km}$ Reichweite durch Bergmassive hindurch.

---

## 5. Binäre Paketformate auf LoRa Kanal 2 & 3

Sämtliche Pakete auf Kanal 2 und 3 sind byteweise gepackt (`__attribute__((packed))`) und mit CRC-16 gesichert:

### 5.1 16-Byte Taktisches Relativ-Radar & Telemetriepaket (`0x03`)
```cpp
struct __attribute__((packed)) OmmRadarPacket_t {
    uint8_t  packet_type;       // 0x03 = TYPE_RADAR
    uint8_t  node_id_short;     // Eindeutige 8-Bit Kurz-ID des Motorrads
    int32_t  latitude_1e7;      // Breitengrad * 1e7 (WGS84)
    int32_t  longitude_1e7;     // Längengrad * 1e7 (WGS84)
    int16_t  altitude_m;        // Höhe über Normalnull (-500 .. +8000 m)
    uint8_t  speed_kmh;         // 0 .. 255 km/h
    uint8_t  heading_div2;      // Fahrtrichtung / 2 (0..179 entspricht 0..358°)
    int8_t   lean_angle_deg;    // Schräglage (-60 .. +60 Grad)
    uint8_t  status_flags;      // Bit 0: 1-PPS Lock, Bit 1: KL15, Bit 2..7: Batt %
};
```

### 5.2 Notfall- & Sirenen-Frühwarnpaket (`0xFF`)
```cpp
struct __attribute__((packed)) OmmEmergencyAlert_t {
    uint8_t  packet_type;       // 0xFF = TYPE_EMERGENCY
    uint8_t  alert_subtype;     // 0x01: Martinshorn/Sirene, 0x02: Sturzerkennung (eCall)
    uint64_t sender_uid;        // 64-Bit Hardware-UID des sendenden Bikes
    int32_t  event_lat_1e7;     // GPS-Koordinaten des Unfallortes
    int32_t  event_lon_1e7;
    uint16_t alert_duration_ms; // Alarm-Gültigkeitsdauer (z. B. 10.000 ms)
    uint8_t  crc8_checksum;     // CRC-8/AUTOSAR Prüfsumme
};
```

### 5.3 Bike-Alarm & Smart-Keyfob Sicherheits-Token (`0xFE` auf Kanal 3)
```cpp
struct __attribute__((packed)) OmmBikeAlarmAlert_t {
    uint8_t  packet_type;       // 0xFE = TYPE_BIKE_ALARM
    uint8_t  alarm_source;      // 0x01: BCM Alarm, 0x02: IMU Schock, 0x03: Kassettenraub
    uint32_t msg_seq;           // Monoton steigender 32-Bit Zähler (Anti-Replay)
    uint64_t bike_uid;          // 64-Bit UID des betroffenen Fahrzeugs
    int32_t  park_lat_1e7;      // Letzter bekannter Parkstandort
    int32_t  park_lon_1e7;
    uint8_t  battery_soc_pct;   // Ladezustand der internen USV-Zelle (0..100 %)
    uint8_t  flags;             // Bit 0: Buddy-Mesh Weiterleitung aktiv
    uint8_t  auth_tag[4];       // 32-Bit AES-128-GCM Authentifizierungs-Tag
    uint8_t  crc8_checksum;     // CRC-8/AUTOSAR Prüfsumme
};
```

---

## 6. Schnittstellen- & Querverweise

1. **OMM 2.4 GHz HD-Audio Kassetten-Modul:**  
   Die Spezifikation der 2.4-GHz-Wechselkassette für Bucht 1 oder Bucht 2, das TDMA-Superframe-Modell sowie PWA Multicast- und Verschlüsselungskanäle sind dokumentiert in [04b - OMM 2.4 GHz Intercom & OEM-Kassette](file:///Users/schmidtm/openMotorBridge/docs/de/04b_omm_intercom_module.md).
2. **Koppelnavigation (ADR), IMU-Sensorfusion & Telemetrie-Blackbox:**  
   Der 15-State Error-State Kalman-Filter (ES-EKF) zur Koppelung von u-blox SAM-M10Q GNSS mit Fahrzeug-Raddrehzahl, Kurvenschräglage und Actioncam-Zeitsynchronisation ist dokumentiert in [06 - Telemetrie, Sensorfusion, Blackbox & WebDAV](file:///Users/schmidtm/openMotorBridge/docs/de/06_telemetry_blackbox_webdav.md).
