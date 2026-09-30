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

## 2. Hierarchischer Zero-Touch Gruppen-Lifecycle: Micro-Cluster, Macro-Merge & Gestaffelte Dispersion

Ein fundamentaler Schwachpunkt bisheriger Motorrad-Funksysteme ist das manuelle Koppeln am Start: Fahrer müssen Knöpfe drücken, Apps synchronisieren oder QR-Codes scannen. OpenMotorBridge führt einen **vollkommen berührungslosen (Zero-Touch), hierarchischen Gruppen-Lifecycle** ein, der reale Ausfahrts-Szenarien vom heimatlichen Start über die Großgruppe bis zum gemeinsamen Heimweg lückenlos abbildet:

```
+-----------------------------------------------------------------------------------------+
|                  HIERARCHISCHER ZERO-TOUCH GRUPPEN-LIFECYCLE                            |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ 1. HEIM-SETUP / VERTEILTER START ]   Feste Buddies / Familie starten im Nahbereich   |
|                                         -> Sofortiges autarkes MICRO-CLUSTER (FOB-Kanal)|
|                                         (Ungestoerte Fahrt zum grossen Treffpunkt)      |
|             |                                                                           |
|             v                                                                           |
|  [ 2. MACRO-MERGE AM TREFFPUNKT ]       Versammlung mehrerer Micro-Cluster & Solofahrer |
|                                         Stillstand (v = 0 km/h, Radius < 40 m)          |
|                                         Gestaffelter Wiederanfahr-Puffer (60-120 s)     |
|             |                           -> Uebergeordneter MACRO-CLUSTER AES-256 Key    |
|             v                           (Micro-Cluster bleibt als Sub-Layer intakt!)    |
|                                                                                         |
|  [ 3. TOUR / MULTI-ROUTE CHECK ]        Heading-Lernphase: Automatische Aufteilung bei  |
|                                         unterschiedlichen Zielen (Cruiser vs. Heizer)   |
|             |                                                                           |
|       +-----+-------------------------+                                                 |
|       v                               v                                                 |
|  [ 4. KAFFEEPAUSE (GROUP_PAUSED) ]   [ 5. IN-FLIGHT FLYBY / DOUBT-TIMER ]               |
|  * Stillstand & Motor AUS            * Rollender Beitritt unterwegs (< 50 m Vektor)     |
|  * 30-60 min Deep-Sleep NVRAM        * Zweifel-Frist bei verpasstem Abzweig (15-30 s)   |
|  * Nahtlose Rekonstitution < 50 ms                                                      |
|             |                                                                           |
|             v                                                                           |
|  [ 6. END-OF-TRIP DISPERSION ]       Abschluss-Parkplatz: PRE_DISPERSE bei Stillstand   |
|                                      Auseinanderfahren beendet Macro-Session schweigend |
|             |                                                                           |
|             v                                                                           |
|  [ 7. HEIMWEG IM MICRO-CLUSTER ]     Unterliegende Micro-Gruppe (Familie / Buddies)     |
|                                      bleibt automatisch aktiv fuer den Heimweg!         |
+-----------------------------------------------------------------------------------------+
```

### 2.1 Stufe 1: Verteilter Start & Autarkes Micro-Cluster (Heim-Setup / Buddy-Gruppe)
In der Praxis starten eng verbundene Fahrer (z. B. Familie, Partner auf zwei Bikes oder enge Freunde aus demselben Ort) nicht erst am Großgruppen-Treffpunkt, sondern bereits zu Hause:
* **Zeitlich-räumliches Gleitfenster (Home-Start-Toleranz):** Starten zwei oder mehr OMB-Bikes im heimatlichen Nahbereich ($d < 500\,\text{m}$) innerhalb eines 15-Minuten-Zeitfensters (oder sind über denselben Smart-Keyfob-FOB-Kanal gekoppelt), schließen sie sich **sofort und vollautomatisch zu einem autarken Micro-Cluster** zusammen.
* **Ungestörte Anfahrt:** Auf der 20- bis 45-minütigen Fahrt zum eigentlichen Haupttreffpunkt läuft die Sprachkommunikation und das Routing über diesen privaten Micro-Kanal - vollkommen ohne manuelle Konfiguration.

### 2.2 Stufe 2: Macro-Merge am Sammel-Treffpunkt (Stillstands-Erkennung & Wiederanfahr-Puffer)
Am offiziellen Treffpunkt (z. B. Autobahnraststätte, Tankstelle oder Passfuß) treffen verschiedene Micro-Cluster sowie Solofahrer ein:
1. **Stillstands-Cluster ($v = 0\,\text{km/h}$ & Radius $< 40\,\text{m}$):** Alle eintreffenden Nodes erkennen die Sammelphase und schalten in den Zustand `PRE_MERGE_DISCOVERY`. Auf Kanal 1 tauschen sie diskrete Discovery-Beacons aus.
2. **Gestaffelter Wiederanfahr-Puffer (Konvoi-Toleranz):**
   * Beim Losfahren einer 10- bis 20-köpfigen Gruppe rollen die Motorräder nie exakt zeitgleich an, sondern ziehen sich an Ampeln, Tankstellenausfahrten und Kreuzungen über 60 bis 120 Sekunden auseinander.
   * Der Algorithmus wertet die Beschleunigung und das Heading mit einem dynamischen Toleranzpuffer aus.
3. **Generierung des übergeordneten Macro-Cluster AES-256 Keys:**
   * Sobald die Kolonne in dieselbe Ausfahrtsachse eingeschwenkt ist ($\Delta\text{Heading} < 30^\circ$, $v > 25\,\text{km/h}$ über $90\,\text{s}$), generiert der temporäre Leader (geringste MAC / höchster DLE-Score) einen gemeinsamen **AES-256 Großgruppen-Session-Key** und verteilt diesen verschlüsselt an alle Teilnehmer.
4. **Zwei-Ebenen-Routing (Dual-Layer Topology):**
   * **Macro-Layer (Großgruppe):** Standard für Kolonnenfunk, Gruppenwarnungen, Radar-Gefahrenmeldungen und DLE-Mesh-Routing.
   * **Micro-Layer (Buddy-Subgruppe):** Bleibt im Hintergrund als persistent hinterlegter Direktkanal aktiv (z. B. umschaltbar per Doppel-PTT).

### 2.3 Stufe 3: Multi-Route-Start & Richtungsspezifische Sub-Groups
Treffen sich am selben beliebten Startpunkt mehrere Gruppen mit unterschiedlichen Zielen (z. B. entspannte Cruiser vs. sportliche Pässe-Fahrer):
* In den ersten 3 Fahrminuten überwacht die Firmware die Fahrtrichtungsvektoren (**Heading-Lernphase**).
* Biegt ein Teil der Motorräder nach Norden und der andere nach Süden ab, teilt sich das System **vollautomatisch und schleifenfrei in zwei autonome Sub-Gruppen** mit jeweils eigenen Session-Keys auf. Es wird kein Fehlalarm generiert.

### 2.4 Stufe 4: Tankstellen- & Kaffeepausen-Schutz (Context-Aware GROUP_PAUSED & 30-min Deep-Sleep)
Bei Raststopps während der Tour darf die Gruppe weder zerfallen noch die Starterbatterie belasten:
* **Stillstands-Erkennung:** Fallen alle Nodes auf $0\,\text{km/h}$ in einem Radius $< 30\,\text{m}$ zusammen, wechselt das System in den Modus `GROUP_PAUSED`.
* **Immunität gegen Bewegungs-Fehlalarme:** Bewegt sich ein Fahrer kurz zur Luftdrucksäule oder zum Parkstreifen, ignoriert der Split-Algorithmus diese Bewegung vollständig.
* **30-Minuten NVS/RTC-Persistenz:** Nach 15 Minuten Motorstillstand geht die Zentralbox in den Tiefschlaf ($< 150\,\mu\text{A}$). Der vollständige Gruppenstatus (Session-Key, Node-Table, Rollen) liegt gesichert im RTC-RAM und SPI-Flash.
* Beim Wiedereinschalten ist das Gesamtsystem in $< 50\,\text{ms}$ ohne erneuten Handshake sofort wieder sprechbereit.

### 2.5 Stufe 5: In-Flight Join & Proximity-Flyby (Unterwegs-Treffpunkt)
Trifft ein Fahrer erst während der Tour auf den Konvoi (Aufgabeln an einer Raststätte oder Flyby auf der Bundesstraße):
* **Proximity-Flyby Kriterien:**
  1. Annäherung auf Distanz $d < 50\,\text{m}$.
  2. Synchronisierte Geschwindigkeit: $\Delta v < 15\,\text{km/h}$.
  3. Kursgleiche Fahrt: $\Delta\text{Heading} < 20^\circ$ über ein Beobachtungsfenster von mindestens **$30\,\text{Sekunden}$**.
* **One-Click Bestätigung:** Nach Erfüllung ertönt beim Leader die Ansage: *"Neuer Fahrer in Reichweite - Beitreten?"*. Ein einfacher Druck auf die Lenker-PTT bestätigt den Beitritt; der Session-Key wird in $< 200\,\text{ms}$ übertragen.

### 2.6 Stufe 6: Gestaffeltes Auschecken (End-of-Trip Dispersion) & Re-Aktivierung des Micro-Clusters
Das offizielle Ende einer Ausfahrt verlangt ein sauberes und lautloses Auflösen der Großgruppe, ohne die Teilnehmer für den Heimweg abzuschneiden:
1. **End-of-Trip Stillstand (`PRE_DISPERSE`):**
   * Am finalen Sammelpunkt (z. B. Parkplatz am Tour-Ende) schalten alle Fahrer die Motoren ab ($v = 0\,\text{km/h}$, IMU-Ruhe, KL15 AUS). Nach 5 Minuten Stillstand wechselt die State Machine in den Zustand `PRE_DISPERSE`.
2. **Lautloses Macro-Disperse:**
   * Verabschieden sich die Teilnehmer und fahren in unterschiedliche Himmelsrichtungen auseinander, erkennt das System die winkelmäßige Auffächerung.
   * Die **Macro-Session schließt sich vollkommen schweigend**; es werden keine Abreiß- oder Notfallalarme ausgelöst.
3. **Automatischer Erhalt des Micro-Clusters (Der Heimweg-Vorteil):**
   * Während die Großgruppe beendet ist, **bleibt das ursprüngliche Micro-Cluster (die Familie / Buddies aus Stufe 1) zu 100 % aktiv und wird automatisch wieder als primärer Kommunikationskanal geschaltet!**
   * Die Buddies können auf dem gesamten Rückweg nach Hause ungestört miteinander sprechen, bis jeder das heimatliche Ziel erreicht hat - ohne dass jemals ein Knopf gedrückt werden musste.

### 2.7 Stufe 7: Der "Doubt-Timer" bei verpasstem Abzweig vs. Geplante Routen-Trennung
* Weicht ein Fahrer unerwartet vom Kurs der Kolonne ab (z. B. Autobahnausfahrt verpasst):
* **Start des Doubt-Timers ($15\dots 30\,\text{Sekunden}$):** Das System stuft den Fahrer temporär in den Zustand `DOUBT_SPLIT` ein.
* **Szenario A (Verpasster Abzweig):** Hält der Fahrer nach wenigen Sekunden an oder sucht die Anschlussstelle, bleibt der Alarm scharf und meldet: *"Achtung: Möglicher Kursverlust / Split"*.
* **Szenario B (Geplante Trennung):** Fährt der Fahrer mit hoher Reisegeschwindigkeit zügig auf der neuen Route weiter, deklariert das System nach Ablauf des Timers das reguläre Verlassen (`GRACEFUL_LEAVE`).

### 2.8 Assistenz-Grundsatz: Diskrete Signalisierung (Human-in-the-Loop) statt Audio-Paternalismus
Im Einklang mit dem architektonischen Leitmotiv (*"Den Lead unterstützen, nicht ersetzen"*, siehe [Kapitel 01](01_system_architecture.md)) verzichtet OpenMotorBridge auf bevormundende Eingriffe in die Gruppenkommunikation:

1. **Heterogene Gruppen & Taktische Anker-Platzierung:**
   * In gemischten Ausfahrten nutzen oft nur 2 bis 3 Motorräder eine OpenMotorBridge (z. B. Lead-Anchor an der Spitze, Mid-Bridge in der Mitte, Sweep-Anchor am Schluss), während die übrigen 10 Teilnehmer reine Fremd-Headsets (Sena oder Cardo) ohne LoRa oder Telemetrie fahren.
   * Oft ist nicht einmal garantiert, dass der vorderste OMB-Fahrer der eigentliche Tourguide ist (der Guide kann z. B. ein reiner Sena-Fahrer an Position 1 sein).
2. **Strikter Verzicht auf ungefragte Roboter-Durchsagen:**
   * Das System unterlässt jegliche automatische Einspeisung synthetisierter TTS-Sprachansagen in das fremde Gruppenmesh. Eine unvermittelt einsetzende Computerstimme (*"Achtung Guide: Konvoi abgerissen!"*) stört die Konzentration, wirkt im fremden Funkkanal peinlich und widerspricht dem Respekt vor menschlicher Führung.
3. **Diskrete, private Signalisierung:**
   * Detektiert der stochastische Riss-Score einen Abriss oder liegt ein technisches Problem vor, erfolgt die Benachrichtigung **ausschließlich an die OMB-Fahrer**:
     * **Haptisch:** Spezifisches Vibrationsmuster am Smart-Keyfob (`PCBA 07`) in der Jackentasche.
     * **Akustisch (Local Only):** Dezenter Zweiklang-Gong ausschließlich im eigenen Helm - niemals im Gruppen-Mesh.
     * **Optisch:** Cockpit-HUD in der PWA oder kurzes Doppelblinken der Spiegel-Warn-LEDs.
4. **Menschliche Souveränität & eigene Stimme:**
   * Der OMB-Fahrer spürt/sieht das Signal, prüft kurz Rückspiegel oder Cockpit und entscheidet selbst:
     * *"Betrifft das mich selbst?"* (Bin ich zu weit zurückgefallen?) -> Eigene Fahrweise anpassen.
     * *"Fehlt jemand hinter mir?"* -> Bei Bedarf drückt der Fahrer kurz PTT und informiert den Guide mit seiner eigenen, natürlichen Stimme über Intercom (*"Du, Klaus, nimm mal kurz raus, hinten an der Ampel sind zwei hängengeblieben"*).
   * Die Technik dient als diskreter, feinfühliger Co-Pilot, der die menschliche Urteilskraft stärkt, anstatt sie zu ersetzen.

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
* Wird ein Audiosignal von einem Netzwerk ins andere übersetzt (z. B. Sena -> Cardo), injiziert der übersetzende Knoten ein digitales Kontroll-Flag (`FLAG_DO_NOT_TRANSLATE`).
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
