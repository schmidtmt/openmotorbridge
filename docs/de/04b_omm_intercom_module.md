# 04b - OMM 2.4 GHz Intercom & Autonome OEM-Kassette

Dieses Dokument spezifiziert das **OpenMotorMesh (OMM) 2.4 GHz Intercom-Modul**: die universelle, quelloffene High-Definition Mesh-Intercom-Lösung von OpenMotorBridge als optionale Wechselkassette für Bucht 1 oder Bucht 2 sowie als autarkes Helm- und Begleitfahrzeug-Headset. Es beschreibt den vollständigen Protokoll-Stack von der physikalischen TDMA-Schicht (Layer 1) über die Schleifenvermeidung und Duplikatfilterung (Layer 2) und die 6LoWPAN/IPv6-Multicast-Vermittlung (Layer 3) bis hin zum RTP/Opus-Audiostreaming (Layer 4/7).

---

## 1. Modul-Konzept & Universelle Kassetten-Kompatibilität (UCS)

Das OMM 2.4 GHz Modul wurde als **100 % offene, abofreie und herstellerunabhängige Alternative** zu proprietären Intercom-Systemen (Sena Mesh 3.0 / Cardo DMC Gen2) entwickelt:

```
+-----------------------------------------------------------------------------------------+
|               OMM 2.4 GHz OEM-KASSETTE (UNIVERSAL CASSETTE STANDARD - UCS)              |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ FORMFAKTOR UCS ]          Standard-Kassette (35 x 25 mm Trägerplatine PCBA 03)       |
|  * Bucht 1 oder Bucht 2      Symmetrischer Einschub in jede OMB-Gehäusebucht            |
|  * Standalone-Fähig          Mit Klick-Halterung auch direkt am Helm/Gürtel nutzbar     |
|                                                                                         |
|  [ ENERGIE & AKKU-KONZEPT ]  Wechselakku + Unterbrechungsfreies Laden im Betrieb        |
|  * Im Pod-Betrieb            Dauerbetrieb über 2-Draht DC-Federkontakte (12V -> 3.8V/5V)|
|  * Standalone-Betrieb        Integrierte LiPo-Flachzelle (600 mAh, ~10 h Laufzeit)      |
|  * Pass-Through Charging     Laden während aktiver Mesh-Kommunikation ohne Reboots      |
|                                                                                         |
|  [ HF & DRAHTLOS-BACKBONE ]  Qorvo DW3110 UWB + ESP32-C6 (2.4 GHz Wi-Fi 6 / 802.15.4)  |
|  * Fahrzeug-Intern           Digitales Audio via UWB an PCBA 01 (< 0.4 ms Latenz)       |
|  * Gruppen-Mesh              2.4 GHz TDMA / IPv6 Multicast Mesh (bis 32 Fahrer, HD)     |
+-----------------------------------------------------------------------------------------+
```

### 1.1 Mechanische Bauformen & Einsatzszenarien
1. **Fahrzeugeinsatz im OMB-Pod (Bucht 1 oder Bucht 2):**
   * Die OMM 2.4 GHz Kassette sitzt formschlüssig im MJF-PA12-Kassettenschlitten.
   * Die Stromversorgung erfolgt vollständig fahrzeuggebunden über die beiden vergoldeten Federkontakte im Pod-Boden.
   * Die Audioübertragung zur Zentralbox (`PCBA 01`) läuft über den integrierten DW3110 UWB-Transceiver - völlig frei von Brummschleifen und Leitungsstörungen.
2. **Autarker Helm- und Standalone-Betrieb:**
   * Dank des Universal Cassette Standards (UCS) kann das Modul mit einem Handgriff entnommen und in ein kompaktes Helm- oder Lenker-Cradle geklickt werden.
   * Der integrierte 600-mAh-LiPo-Akku versorgt das Modul unterwegs für über 10 Stunden Dauerfunk.
   * Über den USB-C-Anschluss an der Stirnseite wird der Akku geladen - auch während der Fahrt (*Pass-Through Charging*).

---

## 2. Layer 1: 2.4 GHz High-Speed TDMA Superframe-Struktur

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

## 3. Layer 2: 802.11s-Light Loop-Prevention & Duplicate-Filter

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

### 3.1 Layer-2 Frame Header Definition & Duplicate-Filter
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

### 3.2 Antennen- und Knoten-Diversität (Remote Radio Head / Split-MAC)
Auf dem Motorrad führt die Abschattung durch den Körper des Fahrers zu Richtungsabhängigkeiten im 2.4-GHz-Band. Stehen dem System zwei Empfänger zur Verfügung (z. B. Front-Node `PCBA 05` und Heck-Pod, oder zwei Antennen links und rechts über den Koffern):
* **Kein doppeltes Audio:** Beide Empfänger empfangen denselben L2-Frame. 
* **Blitzschneller L2-Cache:** Der erste eintreffende Frame wird verarbeitet. Trifft die Kopie $< 2\,\text{ms}$ später über den zweiten Pfad ein, matcht `checkAndRegisterL2Duplicate()` die Sequenznummer und verwirft das Paket in $< 5\,\mu\text{s}$.
* **Ergebnis:** Perfekte Raumdiversität ohne Jitter, ohne zusätzliche CPU-Last und ohne Verwirrung des Audio-Codecs.

---

## 4. Layer 3: 6LoWPAN & IPv6-Multicast Architecture

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

### 4.1 Warum IPv6-Multicast statt TCP oder Unicast UDP?
* **Das TCP-Verbot im Mesh:** TCP ist streng verbindungsorientiertes 1:1 Unicast mit Quittierung (ACK) und Retransmission (ARQ). Geht bei $100\,\text{km/h}$ auf der Landstraße *ein einziges* TCP-Paket verloren, stoppt TCP den kompletten Stream (Head-of-Line Blocking). Die Latenz schießt binnen 2 Sekunden auf über $800\,\text{ms}$ hoch – unbrauchbar für Vollduplex-Intercom. Zudem unterstützt TCP prinzipbedingt kein Multicast.
* **Das Unicast-UDP Airtime-Problem:** Wollte ein Sender 20 Gruppenmitglieder per Unicast UDP bedienen, müsste er dasselbe Audiopaket 20 Mal hintereinander senden – das 2.4-GHz-Band würde sofort kollabieren.
* **Die Lösung: IPv6-Multicast:** Das Audiopaket wird **ein einziges Mal** an die Gruppenadresse gesendet. Jeder Knoten im Funkradius nimmt das Paket auf, ohne den Kanal zu überlasten.

### 4.2 6LoWPAN Header-Komprimierung (RFC 6282)
Ein Standard-IPv6-Header belegt 40 Bytes. Bei einem 10-ms-Opus-Audioframe (ca. 40 bis 60 Bytes Payload) würde ein 40-Byte-Header die Bandbreite halbieren.
* 6LoWPAN nutzt Kontext- und Adress-Elision: Da die Link-Local-Adressen direkt aus den 64-Bit-Hardware-UIDs hervorgehen und die Multicast-Präfixe statisch sind, schrumpft der IPv6-Header auf **2 bis 4 Bytes Overhead** zusammen.

### 4.3 SLAAC-Adressierung & RPL-Routing
* **Autonome Adressvergabe (SLAAC):** Jeder Knoten leitet seine IPv6 Link-Local-Adresse (`fe80::/64`) vollautomatisch und deterministisch aus der Dallas DS2401 Silicon-UID ab. Null manuelle Konfiguration, keine DHCP-Server nötig.
* **Dynamisches RPL (RFC 6550):** Für Teilnehmer außerhalb der 1-Hop-Sichtlinie spannt das Routing Protocol for Low-Power and Lossy Networks (RPL) automatisch einen optimalen, schleifenfreien Weiterleitungsbaum auf.

---

## 5. Layer 4 & Audio-Transport: Opus over RTP & Multicast-Kanäle

### 5.1 RTP Audio Streaming (RFC 3550)
* **Transport:** Encapsulation der Audiodaten in Real-time Transport Protocol (RTP) Paketen über UDP.
* **Adaptiver Jitter-Puffer (20 bis 50 ms):** Gleicht Packet Delay Variations (PDV) durch wechselnde Abstände in Kurvenkombinationen elastisch aus.
* **Packet Loss Concealment (PLC):** Verliert das Mesh ein einzelnes Sprachpaket, interpoliert der Opus-Decoder die fehlenden Audioschwingungen anhand der Formanten des Vorläufer-Frames – Audio bleibt ohne Knacken voll verständlich.
* **Opus-Konfiguration:** 24 kHz Samplingrate (Breitband HD), dynamische Bitrate $16\dots 24\,\text{kbps}$ VBR mit Voice Activity Detection (VAD).

### 5.2 Multicast-Kanalverwaltung (Open Mesh vs. Private Group)

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

## 6. Dynamic Leader Election (DLE) im OMM-Mesh

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

## 7. Cluster Partitioning & LoRa Cross-Gateway Relay (LTE-Sidelink Adaption)

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

## 8. Integration in den Link-State Audio Bridging Graph

Wird die OMM 2.4 GHz Kassette in Bucht 1 oder Bucht 2 gesteckt, bindet der ESP32-S3 Hauptcontroller sie nahtlos in die fahrzeugübergreifende Routing-Matrix ein:

1. **DLE-Capability-Score:**
   * Das OMM 2.4 GHz Modul erhält im Link-State Graph einen **Basis-Score von +50 Punkten** (vollwertiges HD-Mesh mit bis zu 32 Teilnehmern).
2. **Cross-Bridging zu Sena / Cardo:**
   * Befinden sich in Bucht 1 ein Sena SPIDER X Slim und in Bucht 2 die OMM 2.4 GHz Kassette, übersetzt OpenMotorBridge Sprache bidirektional zwischen beiden Welten.
   * Das First-Receiver-Wins (FRW) Schiedsverfahren auf LoRa Kanal 2 verhindert Echos und Mehrfacheinspeisungen in Kolonnen mit mehreren Brücken-Motorrädern.
3. **Do-Not-Translate (DNT) Anti-Loop Flag:**
   * Aus dem OMM 2.4 GHz Mesh empfangene Audiosignale erhalten beim Weiterleiten an ein Sena/Cardo-Mesh das `FLAG_DO_NOT_TRANSLATE`, um akustische Rückkopplungsschleifen (Feedback Loops) über Dritte physikalisch unmöglich zu machen.
4. **PWA Koppel- & Wartungsmodus:**
   * Über die WebApp kann die OMM-Kassette per Knopfdruck in den Pairing-Modus versetzt, Kanäle gewechselt und Firmware-Updates (OTA über UWB) eingespielt werden.
