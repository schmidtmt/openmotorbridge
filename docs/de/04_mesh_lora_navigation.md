# 04 - Funk-Mesh (IEEE 802.15.4), LoRa 868MHz & Koppelnavigation (GNSS/ADR)

Dieses Dokument spezifiziert die Dual-PHY Funk-Mesh-Architektur des **OpenMotorMesh (OMM)**, den dynamischen Leader-Wahl-Algorithmus (**Dynamic Leader Election - DLE**), die Sub-Mesh-Relay-Funktion sowie die hochpräzise Koppelnavigation (**Automotive Dead Reckoning - ADR**) mit Sensorfusion und Actioncam-Zeitsynchronisation.

---

## 1. Dual-PHY Architektur: 2.4 GHz Proximity & 868 MHz LoRa Backbone

OpenMotorMesh kombiniert zwei komplementäre Funkschnittstellen, um sowohl HiFi-Sprachübertragung im Nahbereich als auch ausfallsicheren Kolonnenfunk über viele Kilometer zu gewährleisten:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DUAL-PHY HIERARCHIE IN OPENMOTORBRIDGE                   │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. NAHBEREICH: 2.4 GHz LTE-Sidelink  │ 2. WEITBEREICH: 868 MHz LoRa (Pod 3) │
│ (Intra-Cluster / Proximity < 500m)   │ (Inter-Cluster & Fallback 1 - 15 km) │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • 10 ms Superframe (SC-FDMA TDMA)    │ • Semtech SX1262 LoRa (+22 dBm PA)   │
│ • Full-Duplex HiFi-Voice (Opus SILK) │ • Schmalband PTT-Sprache (Codec2)    │
│ • Stereo Music-Sharing & Navi-Ducking│ • Lückenloses GPS-Gruppenradar      │
│ • 100 % Duty-Cycle erlaubt           │ • ETSI 1 % / 10 % Duty-Cycle konform │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 1.1 2.4-GHz Proximity High-Speed PHY (SC-FDMA TDMA)
* **Superframe (10 ms):** Unterteilt in 10 Subframes à 1 ms (Slotted TDMA) angelehnt an LTE-V2X Sidelink.
* **Synchronisation:** Der Cluster Leader sendet alle 100 ms ein primäres Synchronisationssignal (SLSS), auf das sich alle Gruppenmitglieder einrasten.
* **Kontrollkanal (PSCCH-Light):** In Subframe 0 werden Sprecherankündigungen und Zeitschlitz-Zuweisungen übertragen.
* **Kollisionsfreier Sprachkanal (PSSCH-Light):** Subframes 1–9 transportieren komprimierte Opus-Audio-Pakete ohne Kanalüberbuchung oder Jitter.

### 1.2 868-MHz Sub-GHz Long-Range PHY (SX1262 LoRa im Heck-Pod 3)
* **Frequenzband:** 868.0 – 868.6 MHz (EU ISM, bis zu +22 dBm Sendeleistung an Monopol-Antenne).
* **Ausfallsicherung:** Reißt die 2,4-GHz-Sichtverbindung in Pässen, Kehren oder Kolonnensplits ab, schaltet OMM unterbrechungsfrei auf 868 MHz LoRa um.
* **Sprachübertragung:** Schmalband-Sprachtunnel via Codec2 (1200 bps) für Notfall-PTT über Distanzen von $1\dots 15\,\text{km}$.
* **Gruppenradar:** Übermittelt GPS-Koordinaten aller Gruppenmitglieder für das Cockpit-Radar im 5-Sekunden-Intervall.

### 1.3 Dreifach-Koaxial-Bypass (Murata MM8030 HF-Umschaltbuchsen)
Der Heck-Pod 3 vereint alle drei HF-Subsysteme (2.4 GHz Mesh, 868 MHz LoRa, Multi-GNSS) und ermöglicht durch integrierte **Murata MM8030-2610** Umschaltbuchsen die unterbrechungsfreie Umschaltung zwischen internen Antennen und externen Fahrzeug-Antennen:
* **Interne Antennen (Standard):** Im dielektrischen Radom geschützt arbeiten eine Inverted-F PCB-Antenne (IFA für 2.4 GHz), eine $868\,\text{MHz}$ Wendelspule und ein $25 \times 25\,\text{mm}$ Keramik-Patch (GNSS).
* **Externer Bypass (Plug & Play):** Beim Einstecken eines externen Koaxial-Steckers (z. B. externe $+5\,\text{dBi}$ Stabantenne oder aktive GNSS-Dachantenne) öffnet der interne mechanische Schalter den Pfad zur internen Antenne automatisch mit $< 0{,}15\,\text{dB}$ Einfügedämpfung und $> 25\,\text{dB}$ Isolation.
* **Keine Gehäuseöffnung erforderlich:** Externes Zubehör kann ohne Werkzeugeingriff direkt adaptiert werden.

---

## 2. Layer 2: 802.11s-Light Loop-Prevention & Managed Forwarding

OpenMotorMesh implementiert Routing- und Schleifenschutz-Mechanismen aus IEEE 802.11s direkt auf Layer 2:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Mesh Control  |   Hop Limit   |     Mesh Sequence Number      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Originator Node MAC                       |
|                       (Bytes 0..3)                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Originator MAC (4..5)        |      Target Node MAC (0..1)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Target MAC (2..5)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Payload: 6LoWPAN / IPv6 Multicast / RTP / Opus Audio ...      |
```

* **Hop Limit (TTL):** Wird bei jedem Relais-Hop dekrementiert ($T_{\text{max}} = 5$).
* **Sequence-Cache:** Jeder Knoten speichert die letzten 64 Sequence-Numbers empfangener Pakete; Duplikate werden in Hardware sofort verworfen.

### 2.1 Layer-2 Frame-Header C++ Struct & Duplicate Filter
```cpp
struct MeshHeader_t {
    uint8_t  meshFlags;     // Priority & Type Flags (Bit 0..2: Prio, Bit 3..7: Type)
    uint8_t  hopLimit;      // TTL Dekrement pro Hop (Loop-Schutz, Default = 5)
    uint16_t meshSeqNum;    // Fortlaufende ID des Senders
    uint8_t  originMac[6];  // Erzeuger-Node MAC (aus DS2401 UID abgeleitet)
    uint8_t  targetMac[6];  // Multicast (ff:ff:...) oder Unicast Node MAC
} __attribute__((packed));

void onRawPacketReceived(uint8_t* rawData, size_t len) {
    if (len < sizeof(MeshHeader_t)) return;
    
    MeshHeader_t* meshHdr = (MeshHeader_t*)rawData;
    uint8_t* payload = rawData + sizeof(MeshHeader_t);
    size_t payloadLen = len - sizeof(MeshHeader_t);

    // 1. Layer-2 Loop & Duplicate Filter
    if (meshHdr->hopLimit == 0) return;
    if (checkAndRegisterL2Duplicate(meshHdr->originMac, meshHdr->meshSeqNum)) {
        return; // Duplikat verworfen -> Spart CPU- und DMA-Last
    }

    // 2. Lokale Verarbeitung (Audio Playout oder Radar-Dekodierung)
    processL3Payload(payload, payloadLen);

    // 3. Managed Forwarding: Weiterleitung wenn wir Relay-Master sind
    if (currentRideMode == MODE_RELAY_AR) {
        meshHdr->hopLimit--;
        broadcastForward(rawData, len);
    }
}
```

---

## 3. Layer 3 & 4: 6LoWPAN, IPv6 Multicast & Audio-Streaming

* **Multicast-Routing:** Sprachdaten werden via IPv6-Multicast an Gruppen-Adressen (z. B. `ff02::1`) gesendet. Ein einziges Paket erreicht alle Gruppen-Teilnehmer ohne ressourcenfressende Unicast-Duplikation.
* **Header-Kompression (6LoWPAN nach RFC 6282):** Komprimiert den 40-Byte IPv6-Header auf 2 bis 4 Bytes für minimale Funk-Overheads.
* **Autonome Adressierung (SLAAC):** Jeder Node generiert seine eigene Link-Local-Adresse (`fe80::/64`) autonom aus der 64-Bit DS2401 Chip-UID.

---

## 4. Dynamic Leader Election (DLE) Algorithmus

Das Mesh wählt vollautomatisch und autonom den optimalen Gateway-Knoten der Gruppe. Innerhalb jeder Funkzelle wird autonom genau ein zentraler Gateway-Master (Cluster Head) gewählt:

$$\text{Score}_{\text{DLE}} = S_{\text{HW}} + S_{\text{PWR}} + S_{\text{GNSS}} + S_{\text{LORA}} + S_{\text{UPTIME}} + S_{\text{MIC}}$$

| Parameter | Bedingung | Punkte |
| :--- | :--- | :---: |
| **S_HW (Hardware Tier)** | Sena Apex (Mesh 3.0) ODER Cardo Edge (DMC Gen2) gesteckt | **+60 Pkt.** |
| | Sena Legacy / Cardo DMC Gen1 gesteckt | +30 Pkt. |
| **S_PWR (Stromversorgung)** | Zündung aktiv (KL15 > 12.5 V via LM5164) | **+20 Pkt.** |
| | Pufferbetrieb (USV-Akku > 3.8 V) | +5 Pkt. |
| **S_GNSS (Positionsstabilität)**| 3D Fix mit PDOP < 1.5 & 1-PPS Lock | **+10 Pkt.** |
| **S_LORA (Link-Qualität)** | Durchschnittlicher Nachbar-RSSI > -85 dBm | **+10 Pkt.** |
| **S_MIC (Akustik-Sensor)** | IP67 Front Ambient-Mikrofon aktiv (`FEAT_ENV_MIC`) | **+5 Pkt.** |
| **S_UPTIME (Hysterese-Schutz)** | Bereits aktiver Leader (verhindert Flattern) | **+15 Pkt.** |

### 4.1 Node Capability Vector & Smarte Kolonnen-Funktionen
Im periodischen DLE-Beacon kündigt jeder Knoten seine Ausstattungsmerkmale an:

```cpp
enum OmmFeatureBits : uint8_t {
    FEAT_DUAL_MESH_BRIDGE  = (1 << 0), // Sena + Cardo aktiv (+60 Pkt)
    FEAT_LORA_HIGH_POWER   = (1 << 1), // SX1262 +22 dBm PA
    FEAT_GNSS_1PPS_LOCK    = (1 << 2), // Zeitnormal-Master
    FEAT_CAN_TELEMETRY     = (1 << 3), // OBD2 / CAN-Bus aktiv
    FEAT_ENV_MIC_ACTIVE    = (1 << 4), // Front Ambient-Mikrofon aktiv (+5 Pkt)
    FEAT_USV_BAT_BUFFER    = (1 << 5)  // USV Pufferbetrieb möglich
};
```

1. **🚨 Kolonnen-Sirenen-Frühwarnung (Siren Early Warning):**
   * Erkennt das Frontmikrofon des Führungs-Bikes an einer Kreuzung ein Martinshorn ($350\dots 1000\,\text{Hz}$ Frequenzwechsel eines herannahenden Einsatzfahrzeugs), sendet der Node ein `ALERT_SIREN_APPROACHING`-Paket an die gesamte Kolonne.
   * Alle nachfolgenden Fahrer erhalten einen Warnton im Helm, bevor die Sirene für sie direkt hörbar ist.
2. **🎙️ Guide Pass-Through (Maut-/Grenzkontroll-Kanal):**
   * Der Leader kann bei Stillstand an Mautstellen oder Grenzen sein geregeltes Frontmikrofon per Tastendruck für 10 Sekunden ins Gruppen-Mesh schalten, um Anweisungen des Personals für alle hörbar zu machen.

### 4.2 Adaptive Tiered QoS (Stufenweises Bandbreiten- & Reichweiten-Modell)
Um Verbindungsabrisse im Keim zu ersticken, greift ein 3-stufiges Kaskaden-Modell:
1. **Stufe 1 - Nahbereich (< 500 m, 2.4 GHz):** Full-Duplex HD-Voice, A2DP Music-Sharing und Navi-Ducking aktiv. LoRa sendet im Hintergrund Pings (Duty-Cycle $< 0{,}1\,\%$).
2. **Stufe 2 - Randbereich (500 m - 1.2 km):** Bei sinkendem Link-Quality-Index wird Music-Sharing automatisch pausiert, um die volle Kanalbandbreite der Sprache zu widmen.
3. **Stufe 3 - Weitbereich / Abgerissen (1 km - 15 km, 868 MHz LoRa):**
   * Music-Sharing: AUS.
   * GPS-Gruppenradar & Telemetrie: 100 % aktiv auf dem Dashboard.
   * Sprache: Automatischer Fallback auf Codec2 (1200 bps PTT-Funk).

### 4.3 Cluster Partitioning & Inter-Cluster Gateway Relay (LTE-Sidelink Adaption)
Wird eine Gruppe durch äußere Einflüsse (rote Ampel, Bahnübergang, Passkuppe) getrennt, greift die automatische Cluster-Teilung:

```mermaid
sequenceDiagram
    participant VG as Vordergruppe (Bikes 1-3)
    participant L1 as Leader 1 (Bike 1)
    participant L2 as Leader 2 (Bike 4)
    participant HG as Hintergruppe (Bikes 4-6)

    Note over VG,HG: Einheitliche Gruppe (Leader 1 aktiv auf 2.4 GHz)
    Note over VG,HG: Gruppe wird getrennt (z. B. Ampel schaltet Rot)
    HG->>HG: 2.4 GHz Beacon von Leader 1 verloren -> DLE Neu-Wahl
    HG->>L2: Bike 4 wird autonom zu Leader 2 gewählt
    Note over VG: Lokales 2.4 GHz Mesh aktiv (HD Audio)
    Note over HG: Lokales 2.4 GHz Mesh aktiv (HD Audio)
    HG->>L2: Bike 5 spricht im lokalen 2.4 GHz Mesh
    L2->>L2: VAD Trigger: Sprache lokal erkannt, Cluster getrennt
    L2->>L1: Sende Codec2 Audio-Paket (300 B) via 868 MHz LoRa
    L1->>VG: Dekomprimiere & speise Audio in 2.4 GHz Mesh der Vordergruppe ein
    Note over VG: Vordergruppe hört: "Stehen an der roten Ampel!"
```

1. **Autonome Sub-Leader Wahl:** Die Hintergruppe erkennt den Verlust des primären Leaders (Beacon-Timeout $> 500\,\text{ms}$) und wählt sofort Bike 4 zum lokalen Leader 2.
2. **Lokale HD-Sprache bleibt aktiv:** Innerhalb beider Teilgruppen läuft das 2.4-GHz-Mesh ununterbrochen weiter.
3. **LoRa Cross-Gateway Voice Tunnel:** Sprudelt in einer Teilgruppe Sprache auf, encodiert der lokale Leader diese in Codec2 (1200 bps) und sendet sie über 868 MHz LoRa an den entfernten Leader, welcher sie lokal wieder einspeist.
4. **Cluster-Fusion (Re-Merge):** Sobald die Hintergruppe aufschließt ($< 400\,\text{m}$), erkennt Leader 2 den primären Leader 1, tritt in den Normalmodus zurück und schließt den LoRa-Tunnel.

### 4.4 OpenMotorMesh Paketformate & Binärspezifikation
Alle OMM-Pakete nutzen ein kompaktes, byteweise gepacktes Binärformat:

#### Kompaktes 16-Byte Gruppenradar-Telemetriepaket (`TYPE_RADAR = 0x03`)
```cpp
struct __attribute__((packed)) OmmRadarPacket_t {
    uint8_t  packet_type;       // 0x03 = TYPE_RADAR
    uint8_t  node_id_short;     // Untere 8-Bit der DS2401 ID
    int32_t  latitude_1e7;      // Breitengrad * 10.000.000
    int32_t  longitude_1e7;     // Längengrad * 10.000.000
    int16_t  altitude_m;        // Höhe über Meer (-500 .. +8000 m)
    uint8_t  speed_kmh;         // 0 .. 255 km/h
    uint8_t  heading_div2;      // Kurs / 2 (0..179 entspricht 0..358 Grad)
    int8_t   lean_angle_deg;    // Schräglage (-60..+60 Grad)
    uint8_t  status_flags;      // Bit 0: 1-PPS Lock, Bit 1: KL15, Bit 2..7: Batt%
};
```

#### Notfall- & Sirenen-Frühwarnpaket (`TYPE_EMERGENCY = 0xFF`)
```cpp
struct __attribute__((packed)) OmmEmergencyAlert_t {
    uint8_t  packet_type;       // 0xFF = TYPE_EMERGENCY
    uint8_t  alert_subtype;     // 0x01: Martinshorn/Sirene, 0x02: Sturzerkennung (eCall)
    uint64_t sender_uid;        // 64-Bit Chip UID des erzeugenden Bikes
    int32_t  event_lat_1e7;     // GPS-Koordinaten des Notfall-Events
    int32_t  event_lon_1e7;
    uint16_t alert_duration_ms; // Gültigkeitsdauer des Alarms (z. B. 10.000 ms)
    uint8_t  crc8_checksum;     // CRC-8/AUTOSAR Prüfsumme
};
```

---

## 5. Heck-Pod 3 Transceiver-Architektur & UART-Protokoll

Der Heck-Pod 3 (`PCBA 04`) dient als zentraler RF-Gateway- und GNSS-Knoten und beherbergt einen **Raspberry Pi RP2040** Dual-Core Coprozessor:
* **Core 0 (`rear_nmea_task`):** Parst UBX/NMEA Datenströme des u-blox MAX-M10S Multi-GNSS mit 10 Hz und berechnet Positionsprädiktionen.
* **Core 1 (`rear_lora_task`):** Steuert den Semtech SX1262 LoRa Transceiver über SPI (@ 16 MHz), verwaltet CSMA/CA Kanalzugriffe und puffert ein- und ausgehende OMM-Frames.

### 5.1 Protokoll-Spezifikation (Heck-Pod $\leftrightarrow$ Zentralbox)
Die Kommunikation über die 460.800-Baud-Schnittstelle erfolgt paketorientiert mit CRC16-CCITT-Prüfsumme:

```
┌──────┬──────┬──────┬──────┬─────────────────┬──────┬──────┐
│ SYNC │ TYPE │ LEN  │ SEQ  │ PAYLOAD (0..n)  │ CRC16-CCITT  │
│ 0xAA │ 0x55 │ 1 B  │ 1 B  │ Variable        │ 2 Bytes      │
└──────┴──────┴──────┴──────┴─────────────────┴──────┴──────┘
```

#### Nachrichtentypen (Message Types):
* **`0x01` - GNSS PVT Telemetrie (10 Hz):** Vorkomprimierter Binärvektor mit Latitude, Longitude, Altitude, Speed, Heading, PDOP und Satellitenstatus.
* **`0x02` - OMM 2.4 GHz Primary Audio Frame:** Opus 24k/12k Frame aus dem 2.4 GHz Proximity Mesh.
* **`0x03` - OMM 868 MHz LoRa Fallback Frame:** Codec2 Audio- oder Radar-Paket aus dem Long-Range Fallback.
* **`0x04` - OMM Tx Request (Dual-PHY):** Sendeauftrag der Zentralbox an das 2.4 GHz Mesh oder den SX1262 LoRa Transceiver.
* **`0x05` - DLE Status & Link Quality:** Signal-to-Noise Ratio (SNR), RSSI, PHY-Modus (2.4G vs 868M) und DLE Gateway-Score des Knotens.
* **`0xFE` - Firmware Update Bootloader Command:** `0xAA 0x55 0xFE 0x01 "BOOT"` schaltet den RP2040 in den USB-ROM-Bootloader-Modus für Push-Flashen.

### 5.2 V2 Upgrade-Roadmap: Optionale LTE-M / NB-IoT Cloud-Kassette & HF-Triplexer
Für Langstreckenfahrer und weltweite Gruppenvernetzung ist eine alternative Monolith-Kassette für Pod 3 vorbereitet:
* **Quectel BG95-M3 Modem:** Unterstützt LTE Cat M1, NB-IoT, eGPRS und integriertes GNSS.
* **HF-Triplexer:** Ermöglicht die gemeinsame Nutzung der Antennenports für 868 MHz LoRa, LTE-M (Bänder B1/B3/B8/B20) und GNSS L1.
* **Cloud Telemetry Mirror:** Automatischer Live-Standort-Upload ins Web-Portal auch außerhalb von Mesh- und LoRa-Reichweiten.

---

## 6. Automotive Dead Reckoning (ADR) & Sensorfusion

Das GNSS-Subsystem im Heck-Pod 3 (**u-blox NEO-M9N / MAX-M10S**) ist mit der 6-Achsen-IMU (**Bosch BMI270**) und den Fahrzeug-Raddrehzahlen über einen **15-State Error-State Kalman-Filter (ES-EKF)** gekoppelt:

```
[ u-blox GNSS Modul (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Raddrehzahl / Speed ] ────(10-20 Hz)───────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ─(50-100 Hz)─────┘        (Dead Reckoning Engine)            (Mit Schräglage & G-Force)
```

### 4.1 Tunnel- und Schlucht-Navigation
* Fällt das Satellitensignal in Tunneln oder Gebirgsschluchten aus, integriert der Kalman-Filter Raddrehzahl und Gyroskop-Winkelgeschwindigkeiten kontinuierlich weiter.
* Der Track läuft ohne Positions-Einfrieren oder Zick-Zack-Muster absolut präzise auf der Fahrbahnlinie.

### 4.2 MotoGP-Style Telemetrie im GPX 2.0 Format
Jeder Wegpunkt speichert die vollständige Fahrzeugdynamik:
* **Kurvenschräglage links/rechts (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
* **Längs- und Querbeschleunigung (Brems- und Beschleunigungs-G-Kräfte)**
* **Bordnetzspannung und Satelliten-Metriken**

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
    </omb:telemetry>
  </extensions>
</trkpt>
```

---

## 7. Actioncam-Steuerung & 1-PPS Framegenaue Zeitsynchronisation

OpenMotorBridge steuert gekoppelte Actioncams drahtlos über den Lenkertaster und bettet Sensordaten direkt in die Videoaufnahmen ein:

1. **1-PPS Hardware-Zeitstempel:** Das GNSS-Modul liefert an `PIN_GNSS_PPS` einen 1-Hz-Impuls mit $< 15\,\text{ns}$ Jitter, wodurch Video-Footage und Schräglagendaten über Stunden framegenau synchron bleiben.
2. **Unterstützte Kamera-Protokolle:**
   * **GoPro (Hero 9/10/11/12/13):** Open GoPro BLE API (GATT Service `0xFEA6`).
   * **Insta360 (X3 / X4 / Ace Pro):** Emulation der offiziellen Insta360 GPS Smart Remote; Telemetriedaten werden nativ in den Videocontainer (GPMF/INSV) eingebettet.
   * **DJI (Osmo Action 3/4/5 Pro):** DJI BLE Remote Protokoll.
3. **Lenkertaster-Gesten:**
   * **Klick:** Video-Highlight Marker im GPX-Track setzen.
   * **Doppelklick:** Aufnahme Start/Stopp.
   * **Apex-Auto-Trigger:** Schräglagen über $45^\circ$ setzen automatisch einen Highlight-Tag.
