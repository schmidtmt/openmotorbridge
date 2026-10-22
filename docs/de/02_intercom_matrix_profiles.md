# 02 - Intercom-Matrix, PTT-Steuerung & Dynamische Pod-Profile

Dieses Dokument spezifiziert die universelle **Intercom-Routing-Matrix**, die latenzfreie **Lenker-PTT-Steuerung** (< 0,2 ms) sowie das klassenorientierte **Hardwareprofil-System** der OpenMotorBridge v10.0 Standardized Architecture auf Basis der 4-Draht Automotive USB-PD & USB 2.0 Busarchitektur, nativer USB-Enumeration (`USB_DESC_POD_ANNOUNCE`), gestaffeltem Power-Sequencing und der LittleFS-Profil-Engine.

---

## 1. Intercom-Routing-Matrix & Brückenarchitektur

Die OpenMotorBridge fungiert als aktive Audio-Kreuzschiene und Brückengateway zwischen zwei physischen Intercom-Einheiten (Bucht 1 und Bucht 2), externen Audioquellen (Navi / Boom! Box) und den Bluetooth-Helmen von Fahrer und Sozius:

```
                            INTERCOM ROUTING MATRIX (v10.0 4-DRAHT BUS)
+----------------------------------------------------------------------------------------+
|                                                                                        |
|   SATELLITEN-POD 1 (Koffer Links * Sena)      SATELLITEN-POD 2 (Koffer Rechts * Cardo) |
|   +--------------------------+                +--------------------------+             |
|   | * Sena SPIDER X Slim     |                | * Cardo Packtalk Edge    |             |
|   | * PCBA 03 Gateway-Board  |                | * PCBA 03 Gateway-Board  |             |
|   | * USB-C PD Ladeport 30W  |                | * USB-C PD Ladeport 30W  |             |
|   +------------+-------------+                +------------+-------------+             |
|                |                                           |                           |
|                | 4-Draht Automotive Bus (VBUS, GND, D+, D-) Peitsche 1 & 2             |
|                | Gestaffelt: T=200ms (USB-PD Sink)         | Gestaffelt: T=350ms       |
|                |                                           |                           |
|                +-------------+-----------------------------+                           |
|                              | High-Speed USB 2.0 Audio Class & Steuer-Streams         |
|                              | (Automotive USB 2.0 / Latenz < 0.2 ms / Vollduplex)     |
|                              v                                                         |
|       +------------------------------------------------------------+                   |
|       |     ESP32-S311 AI RISC-V DSP & ES8388 24-BIT / 48 kHz AUDIO  |                   |
|       |  * Raised-Cosine Ducking (Prio: Radar > Navi > Intercom)   |                   |
|       |  * Symmetrischer Intercom-Cross-Mix (Bucht 1 <-> Bucht 2)  |                   |
|       |  * Knowles MEMS Fahrtwind-Lautstärkenachführung (AGC)      |                   |
|       +-----------------------------+------------------------------+                   |
|                                     | Synchroner I2S Digital-Bus (48 kHz / 24-Bit PCM) |
|                                     v                                                  |
|       +------------------------------------------------------------+                   |
|       |        QUALCOMM QCC3084 BLUETOOTH 5.4 AUDIO-SOC (U9)       |                   |
|       |  * Dual-A2DP Hardware-Encoder (aptX HD & aptX Adaptive)    |                   |
|       |  * LE Audio Auracast Broadcast Engine                      |                   |
|       |  * HFP 1.8 Wideband Speech Telefonie & Mikrofon-Uplink     |                   |
|       |  * Onboard Keramik-Chipantenne (Null Koaxialkabel-Overhead)|                   |
|       +-----------------------------+------------------------------+                   |
|                                     |                                                  |
|              +----------------------+----------------------+                           |
|              | RF-Stream 1 (aptX HD)                       | RF-Stream 2 (aptX / LC3)  |
|              v                                             v                           |
|   +----------------------------+              +----------------------------+           |
|   | FAHRER-HELM (Bluetooth)    |              | SOZIUS-HELM (Bluetooth)    |           |
|   | * Sena/Cardo/OEM Headset   |              | * Sena/Cardo/OEM Headset   |           |
|   | * aptX Adaptive (< 20 ms)  |              | * Synchroner Dual-A2DP Mix |           |
|   | * HFP 1.8 Mikrofon-Uplink  |              | * Getrennte AVRCP-Lautst.  |           |
|   +----------------------------+              +----------------------------+           |
+----------------------------------------------------------------------------------------+
```

### 1.1 Die 3 Standard-Betriebsmodi
1. **Modus 0: Standard-Modus (Full Mesh Bridge):**  
   Bucht 1 (z. B. Sena Mesh 3.0) und Bucht 2 (z. B. Cardo DMC Gen2) sind gleichzeitig aktiv. Sprache von Sena-Fahrern wird in Millisekunden in das Cardo-Mesh übertragen und umgekehrt. Fahrer und Sozius hören beide Gruppen symmetrisch gemischt im Helm via Bluetooth.
2. **Modus 1: Single Rider Mode (Fokus-Modus):**  
   Bucht 2 wird softwareseitig stummgeschaltet (`-96 dB`). Der volle DSP- und Routing-Fokus liegt auf dem Primär-Gateway (Bucht 1), Navigationsdurchsagen und Smartphone-A2DP-Musik.
3. **Modus 2: Cruise Mode (Bordlautsprecher-Ausgabe):**  
   Intercom-Signale werden um $-6\,\text{dB}$ bedämpft und auf die Bordlautsprecher (Harley-Davidson Boom! Box GTS / BMW Soundanlage) geroutet.

### 1.2 Cross-Intercom Bridge (Bucht 1 ↔ Bucht 2) mit Anti-Feedback Loopback-Gate
* **Bidirektionale Kopplung:** Ermöglicht die nahtlose Audio-Brücke zwischen inkompatiblen Herstellern (z. B. Sena Spider X Slim Mesh 3.0 in Bucht 1 und Cardo DMC Gen2 in Bucht 2).
* **Einstellbare Überblend-Dämpfung:** Bleed-Pegel stufenlos von $-18\,\text{dB}$ bis $0\,\text{dB}$ (Standard: $-6\,\text{dB}$) in der WebApp konfigurierbar.
* **Anti-Feedback Loopback Gate ($-24\,\text{dB}$ Schutzschaltung):**  
  Sobald auf Bucht 1 Sprache erkannt wird (VOX aktiv oder PTT gedrückt), dämpft der DSP den Rückkopplungspfad von Bucht 2 nach Bucht 1 schlagartig um $-24\,\text{dB}$. Dadurch wird verhindert, dass die aus dem Cardo-Kopfhörer des Sozius austretende Stimme des Fahrers über dessen Mikrofon wieder in das Sena-Mesh zurückgesendet wird (Unterdrückung von Echos und akustischen Pfeifschleifen).

### 1.3 Sidetone Eigenstimmen-Rückführung
* **Natürliche Stimmrückmeldung:** Im geschlossenen, geräuschgedämmten Integralhelm neigen Fahrer bei Autobahngeschwindigkeit zum unbewussten Schreien.
* **Latenzfreier Rückhörpfad:** Der DSP führt das gefilterte Mikrofon-Signal latenzfrei (< 2,7 ms) mit einstellbarem Pegel ($-40\,\text{dB}$ bis $0\,\text{dB}$, Standard: $-12\,\text{dB}$, $< -35\,\text{dB} = \text{Mute}$) in die eigenen Helm-Lautsprecher zurück.
* **VOX-Koppelung:** Sidetone wird nur aufgeschaltet, wenn VOX oder PTT aktiv ist.

### 1.4 Intelligentes Navi Auto-Sensing (Pegelgesteuertes Ducking)
* **Hardwareunabhängiges Ducking:** Funktioniert auch bei analogen Line-In-Navigationsgeräten (z. B. Garmin Zūmo XT2 oder BMW Motorrad Navigator) ohne dedizierte Steuerleitung.
* **Schwellenwert-Logik:** Überschreitet das eingehende Navigations-Audio $-36\,\text{dBFS}$ für länger als $50\,\text{ms}$, leitet die Ducking-Engine sofort ein weiches Raised-Cosine Ducking ($-12\,\text{dB}$) auf Musik und Intercom ein.
* **Hold & Release:** Nach Ende der Ansage (Pegel $< -42\,\text{dBFS}$) verbleibt das Ducking für $800\,\text{ms}$ im Hold-Zustand und blendet dann mit $250\,\text{ms}$ sanft auf Vollpegel zurück.

### 1.5 Physische Dual-Helm-Anbindung über Qualcomm QCC3084 & aptX HD / Adaptive

Im Gegensatz zu vereinfachten ESP32-Software-A2DP-Lösungen wird die Bluetooth-Anbindung der Helme bei OpenMotorBridge von einem **dedizierten Qualcomm QCC3084 Bluetooth 5.4 Audio-SoC (`U9` auf PCBA 01)** in echter Hardware ausgeführt:

1. **Vollständige HF- und CPU-Entkopplung:**
   * Der interne Funkcontroller des ESP32-S31 teilt sich eine einzige 2.4-GHz-HF-Endstufe zwischen Wi-Fi (PWA Webserver, WebDAV Touren-Upload) und Bluetooth Low Energy (PWA-Dashboard, BLE-Sensoren). Würde der ESP32 parallel zwei hochauflösende A2DP-Stereoströme berechnen und senden, käme es bei HF-Störungen oder hoher CPU-Last unweigerlich zu Audio-Aussetzern, Knacksern und Latenzen $> 150\,\text{ms}$.
   * Durch die Auslagerung auf den Qualcomm QCC3084 läuft das Helm-Audio autark auf einem dedizierten Dual-Core 32-Bit Audioprozessor ($80\,\text{MHz}$) mit integriertem $240\,\text{MHz}$ Kalimba Hardware-Audio-DSP.
2. **Echtes Dual-A2DP & aptX HD / Adaptive:**
   * **Fahrer-Helm (Stream 1):** Dynamische Umschaltung zwischen **aptX HD** ($24\,\text{Bit} / 48\,\text{kHz}$, Studio-HiFi für Musik) und **aptX Adaptive Low-Latency Mode** ($< 20\,\text{ms}$ Audio-Latenz für vollkommen natürliche, lippensynchrone Gegensprechkommunikation).
   * **Sozius-Helm (Stream 2):** Phasenstarr synchronisiertes Zweit-Streaming via A2DP (aptX / LC3). Lautstärke und Klangprofil lassen sich für den Sozius über AVRCP völlig unabhängig vom Fahrer einstellen.
3. **LE Audio Auracast Broadcast:**
   * Ermöglicht das Teilen des gesamten Audio-Mixes (Intercom, Musik, Navi) mit beliebig vielen Auracast-fähigen Empfängern im Begleittross ohne Pairings-Limit.
4. **HFP 1.8 Wideband Speech & Fahrermikrofon-Uplink:**
   * Der QCC3084 übernimmt das vollständige Bluetooth Hands-Free Profile (HFP 1.8 mit mSBC / aptX Voice, $16\,\text{kHz}$ Wideband Speech).
   * Das vom Helm-Headset aufgenommene Mikrofonsignal des Fahrers wird vom QCC3084 digital decodiert und über die synchrone Leitung `I2S_DIN` verlustfrei und jitterfrei in die DSP-Pipeline des ESP32-S31 zurückgespeist.
5. **Onboard Keramik-Chipantenne (Null Koaxialkabel-Overhead):**
   * Das QCC3084-Modul integriert eine miniaturisierte $2{,}4\,\text{GHz}$ Hochleistungs-Keramik-Chipantenne direkt auf dem Modulträger ($13 \times 18\,\text{mm}$).
   * Die HF-Abstrahlung erfolgt direkt durch das ABS/PA12-Gehäuse der Zentralbox in Richtung Fahrer-/Sozius-Helm. Es wird **kein 4. Koaxialkabel, kein U.FL-Steckverbinder und kein Montageaufwand im Gehäusedeckel** benötigt!

### 1.6 Strategischer Leitfaden: Das „Bridge-the-Gap“-Prinzip & Helm-Akkuschonung

> [!IMPORTANT]
> **Leitsatz gegen die 2000-Euro-Kostenfalle:**
> OpenMotorBridge zwingt niemanden, bereits vorhandene, teure Hardware doppelt zu kaufen. Wer bereits einen Premium-Helm mit integriertem System besitzt (z. B. Schuberth C5 + SC2 oder Shoei Neotec 3 + SRL3 für 800–1200 €), nutzt diesen als primären Funkknoten. Am Motorrad wird ausschließlich die **jeweils fehlende Gegenmarke bestückt (Bridge-the-Gap)**. Das spart über 50 % der Anschaffungskosten!

#### Die zwei klaren Nutzungsprofile:
1. **Profil A: „Bridge-the-Gap“ (Fahrer hat bereits teuren OEM-Helm):**
   * *Helm besitzt Sena (z. B. SC2):* Am Bike wird in Bucht 1 **nur Cardo (Packtalk Edge/Neo)** bestückt. Bucht 2 bleibt frei für **OMM 446 (PMR446 Funk)** oder eine Dry-Box.
   * *Helm besitzt Cardo (z. B. Beyond GTS):* Am Bike wird in Bucht 1 **nur Sena (Spider X Slim)** bestückt.
   * *Vollständige Gruppenbrücke:* Über die Zentralbox kann der Fahrer mit beiden Welten sprechen; OMB überbrückt bei Bedarf sogar zwischen der Sena- und Cardo-Gruppe.
2. **Profil B: „Helmet-Agnostic“ (Dumb Helmet / Universeller Helm):**
   * Der Fahrer setzt auf einen günstigen Standardhelm (oder ECE 22.06 UCS mit OMM 2.4).
   * Beide Koffer-Pods am Bike sind bestückt (Sena + Cardo).
   * *Vorteil:* Helmwechsel ist jederzeit kostenlos und ohne Markenbindung möglich.
3. **Profil C: „Autarkes OMB Lite“ (Dual-Engine UCS-Helm & Standalone Intercom):**
   * Der Fahrer nutzt das autarke **OMM UCS-Modul (`PCBA 09` oder `PCBA 10`)** direkt im Helm oder in der Tasche.
   * **Dual-Engine:** Der `ESP32-C6` wickelt das reine OMM-Mesh (Wi-Fi 6) oder DMR-Funk ab, während der `ESP32-PICO-V3-02` parallel Bluetooth Classic (Universal Intercom, A2DP, OMI) und BLE bereitstellt.
   * **Voll autark (USA-Leihmotorrad, Buggy, Fahrrad):** Funktioniert ohne Bike-Hauptbox mit integriertem LiPo-Akku.
   * **Universal Gateway:** Klinkt sich per **Cardo DMC-Bluetooth Bridge** in fremde Cardo-Gruppen ein oder holt Fremdfahrer ins OMM-Mesh.

#### Massiver Akku-Vorteil durch reine Bluetooth-Nutzung am Helm:
* Ein aktiver Mesh-Transceiver am Helm (Sena Mesh oder Cardo DMC) zieht permanent **$80\dots 130\,\text{mA}$** und leert den 1000-mAh-Helmakku nach **7 bis 9 Stunden** (oft schon vor Tourende!).
* Wird der Helm hingegen **nur per stromsparendem Bluetooth (HFP/A2DP)** an die OMB-Zentralbox gekoppelt (während das Mesh vom 12V-gespeisten Pod am Bike abgewickelt wird), sinkt die Stromaufnahme auf **$15\dots 22\,\text{mA}$**.
* **Ergebnis:** Der Helm-Akku hält **18 bis 24+ Stunden** – locker ein ganzes langes Tourenwochenende ohne Zwischenladen!

#### Ergonomie & Direktanbindung (Warum flache Taster & Micro-Peitschen überlegen sind):
* In v10.0 sind störanfällige mechanische Hubmagnete und Tauchstößel **vollständig eliminiert**. Die Steuerung erfolgt digital via BLE GATT / AVRCP oder direkte elektrische PTT-Tastung (`PTT_KEY`).
* Flache Bauformen (wie beim Sena Spider X Slim oder Cardo Packtalk Edge) mit formschlüssigen Kabelpeitschen oder Air-Mount-Docks garantieren vibrationsfeste, hermetisch dichte Unterbringung in der oberen Pod-Bucht.

---

---

## 2. Zero-Latency PTT-Steuerung & Digitaler USB-Trigger (< 0,2 ms)

Klassische Bluetooth-Fernbedienungen am Lenker leiden unter hohen Latenzen ($80 \dots 250\,	ext{ms}$) und Verbindungsaussetzern. OpenMotorBridge v10.0 löst dieses Problem durch eine deterministische **4-Draht Automotive USB-PTT-Signalkette**:

```
               LENKER-PTT SIGNALKETTE (GLAS-ZU-GLAS < 0,20 ms)
+----------------------------------------------------------------------------------------+
| 1. UNDER-PERCH TASTE (Am Spiegelfuß PCBA 05B verdrahtet):                              |
|    * Taktiler Goldkontakt-Schalter unter dem Spiegelfuß (IP67, 100% batteriefrei)       |
|    * Hardware-Schmitt-Trigger-Entprellung (12 µs Latenz)                               |
|    * GPIO Pegel-Interrupt auf Front-Node PCBA 05 (5-Gesten Trigger Engine)             |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 2. ULTRA-LOW-LATENCY 4-DRAHT AUTOMOTIVE BACKBONE: FRONT-NODE -> ZENTRALBOX              |
|    * High-Speed USB 2.0 Interrupt Transfer (< 60 µs Bus-Transitzeit)                   |
|    * Geschirmte Automotive-Leitung durch Rahmentunnel-Kabelkanal (ZERO Tank-Lifting)    |
|    * Null HF-Kollision mit 2.4 GHz Bluetooth, Wi-Fi oder Sena/Cardo Mesh (PDR: 100 %)  |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 3. ZENTRALBOX DISPATCHER & USB-ROUTING: ZENTRALBOX -> POD 1 / POD 2                    |
|    * ESP32-S311 AI Core 0 ISR erfasst PTT-Event (< 20 µs) & dispatcht Audio-Pfad        |
|    * Latenzfreies Mikrofon-Gating & Raised-Cosine Ducking im Hardware-Audio-DSP        |
+----------------------------------------------------------------------------------------+
|                                        v                                               |
| 4. INTERFACE TRIGGER (PCBA 03 im Satelliten-Pod):                                       |
|    * Direkte elektrische OptoMOS PTT-Tastung (`PTT_KEY`) in < 10 µs oder               |
|    * Digitaler USB Audio Class Stream / BLE GATT Befehl (< 2 ms)                       |
|    * Gesamtlatenz vom Lenkertaster bis zum aktiven Mesh-TX: < 0,20 ms                  |
+----------------------------------------------------------------------------------------+
```

### 2.1 Digitale Direktanbindung & Kassetten- und Stößelfreies Pod-Konzept (v10.0)

In früheren Generationen wurden Headsets über mechanische Tauchanker-Hubmagnete bedient. In OpenMotorBridge v10.0 wurde dieses mechanische Konzept vollständig durch **digitale Direktanbindung und smartes Power-Cycling** ersetzt:
* **Null mechanischer Verschleiß:** Keine Hubmagnete, keine Stößelbrücken, keine Auswurffedern.
* **100 % Erhalt von Garantie & IP67-Schutz:** Das Headset wird fabrikneu und ungeöffnet in die obere Bucht des Monocoque-Pods gebettet. 
* **OptoMOS PTT-Keying (`CPC1017N`):** Schaltet galvanisch isoliert in $< 10\,\mu	ext{s}$ PTT gegen Masse für Funkgeräte (Midland PMR446) oder Audio-Keying.
* **Smart USB-PD Power-Cycling:** Automatischer Kaltstart bei Zündung EIN und sicheres Herunterfahren bei Zündung AUS über softwaregesteuertes Power-Gating der internen USB-PD Ladeversorgung.

### 2.2 Symmetrische Dual Under-Perch Tastenbelegung & 5-Gesten-Engine

Jeder Spiegel-Pod (`PCBA 05B`) verfügt über einen taktilen Taster, der softwaredefiniert in der WebApp (PWA) mit bis zu 5 Gesten frei konfiguriert werden kann:

```
+----------------------------------------------------------------------------------------+
|              DIE 5 GESTEN-TRIGGER DER UNDER-PERCH SPIEGEL-PODS (v10.0)                 |
+-----------------------+-----------------------+----------------------------------------+
| Geste                 | Zeitfenster / Beding. | Typische Standard-Belegung             |
+-----------------------+-----------------------+----------------------------------------+
| **`SHORT_CLICK`**     | $30 \dots 250\,	ext{ms}$  | Cam-Tag (Rechts) / Intercom Ch+ (Links)|
+-----------------------+-----------------------+----------------------------------------+
| **`DOUBLE_CLICK`**    | 2 Klicks in $< 400\,	ext{ms}$| Video Start/Stopp (Rechts) / Siri/Google|
+-----------------------+-----------------------+----------------------------------------+
| **`TRIPLE_CLICK`**    | 3 Klicks in $< 600\,	ext{ms}$| Waze 1-Click Gefahren-Pin (Schlagloch) |
+-----------------------+-----------------------+----------------------------------------+
| **`LONG_PRESS`**      | $500 \dots 1500\,	ext{ms}$| Radar Stummschaltung / Garagentor BLE  |
+-----------------------+-----------------------+----------------------------------------+
| **`HOLD_GATE`**       | Halten $> 250\,	ext{ms}$  | **Lenker-PTT Funksprech-Taste (Push)** |
+-----------------------+-----------------------+----------------------------------------+
```

## 3. Klassenorientierte Hardwareprofile & Gerätehierarchie

Alle unterstützten Intercom- und Funkgeräte sind in klar voneinander abgegrenzte Hardware-Klassen eingeteilt. Inkompatible Mesh-Generationen (z. B. Mesh 3.0 vs. Mesh 2.0 sowie Sena Mesh vs. Cardo DMC) sind strikt getrennt:

```
+-----------------------------------------------------------------------------------------+
|                  KLASSENORIENTIERTE HARDWARE-PROFIL-MATRIX (v9.6 REVISED)                |
+----------+-------------------------------------+-----------------------+----------------+
| Klasse   | Gerätefamilien                      | Funk-Protokoll        | DLE-Score Bonus|
+----------+-------------------------------------+-----------------------+----------------+
| **K1a**  | Sena 60S, 60R, 60X, Spider X Slim,  | Sena Mesh 3.0 & Wave  | **+60 Punkte** |
|          | Schuberth SC2 (mit Firmware Mesh 3),| (Next-Gen Dual Mesh)  |                |
|          | Sena MeshON (Adapter, 800 m)        |                       |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1b**  | Sena 50S, 50R, 50C, Spider ST1/RT1, | Sena Mesh 2.0         | **+40 Punkte** |
|          | Sena +Mesh Adapter, SRL-Mesh        | (Vorgänger-Standard)  |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1c**  | Sena 30K, +Mesh 1.0 (Legacy / EOL)  | Sena Mesh 1.0         | **+20 Punkte** |
+----------+-------------------------------------+-----------------------+----------------+
| **K1d**  | Cardo Packtalk Edge, Pro, Neo,      | Cardo DMC Gen2        | **+60 Punkte** |
|          | Cardo Packtalk Custom               | (Dynamic Mesh 2.0)    |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K1e**  | Cardo Packtalk Bold, Black, Slim    | Cardo DMC Gen1 Legacy | **+30 Punkte** |
+----------+-------------------------------------+-----------------------+----------------+
| **K2**   | Sena Apex, Apex Plus (BT 6.0),      | Bluetooth Intercom    | **+30 Punkte** |
|          | Sena Vertex, 10R, 20S EVO, 5R,      | (Point-to-Point &     |                |
|          | Cardo Freecom 4x/2x, Spirit HD      | Daisy-Chain Multi-Hop)|                |
+----------+-------------------------------------+-----------------------+----------------+
| **K3a**  | Midland G7 Pro bis G18 Pro, XT-Reihe| PMR446 Analog (FM)    | **+15 Punkte** |
+----------+-------------------------------------+-----------------------+----------------+
| **K3b**  | OMM 446 (PCBA 10), Midland D-10,    | Digital DMR Tier I    | **+45 Punkte** |
|          | NiceRF SA818-DMR Transceiver        | & PMR446 Dual-Mode    |                |
+----------+-------------------------------------+-----------------------+----------------+
| **K4**   | OMM 2.4 GHz Universal (PCBA 09 UCS) | OMM TDMA / IPv6 Mesh  | **+55 Punkte** |
+----------+-------------------------------------+-----------------------+----------------+
| **K0**   | Deaktiviert / Leerer Pod-Slot (Dry-Box) | Keines (eFuse OFF)    | **0 Punkte**   |
+----------+-------------------------------------+-----------------------+----------------+
```

### 3.1 Detaillierte Geräte-Klassifizierung & Profile im Dateisystem (`/data/profiles/`)

Da Pods im v10.0 System standardisierte Trägerbays darstellen, fungieren die Profil-Punkte als deterministische **Capability-Scores für das dezentrale Link-State Routing**: Führen mehrere Bikes im Konvoi unterschiedliche Schnittstellen mit, legt die Routing-Matrix fest, welcher Node primär als loop-freie Brücke fungiert.

#### Klasse 1a: Sena Mesh 3.0 & Wave (`sena_60_series.json`, `sena_spider_x.json`, `sena_meshon.json`, `schuberth_sc2.json`):
* **Sena 60er Serie (60S, 60R, 60X):** Next-Gen Flaggschiff mit Mesh 3.0 und Wave-Zellfunk-Fallback. Während das 60S ein voluminöses Drehrad besitzt, ist das **Sena 60X** als flaches, modulares System konstruiert.
* **Sena SPIDER X Slim (`sena_spider_x.json` - Top-Empfehlung für die Pod-Bucht):**
  * *100 % akkulos ab Werk:* Wird über die werksseitige 2-Draht-Akkuleitung direkt mit $3{,}85\,\text{V}$ Festspannung von PCBA 03 versorgt. Keine Brandgefahr, kein Aufblähen von LiPos im heißen Pod, keine Alterung.
  * *Volle Mesh 3.0 & Wave Parität:* Volle Reichweite bis $2{,}0\,\text{km}$ bei extrem schlanken Abmessungen ($74{,}5 \times 31 \times 16\,\text{mm}$, $23{,}2\,\text{g}$).
  * *Mechatronik-Vorteil:* Verfügt über **klar definierte, flache Einzeltaster** (Center, Plus, Minus, Mesh) – ideal für die flache Unterbringung im Pod-Bett (im Gegensatz zu sperrigen Drehrädern). DLE-Score: **+60 Pkt.**
* **Schuberth SC2 (mit Firmware Mesh 3.0 Update):**
  * Premium-Sena-Mesh-Plattform. Durch das offizielle Schuberth/Sena Firmware-Update (via *SCHUBERTH Bluetooth Device Manager*) erhält das SC2 vollen **Mesh 3.0 Support** inklusive umschaltbarem Mesh 2.0 Kompatibilitätsmodus. DLE-Score: **+60 Pkt.**
* **Sena MeshON (`sena_meshon.json`):**
  * Ultrakompakter, leichter ($22{,}5\,\text{g}$) Mesh 3.0 Adapter (mit Mesh 2.0 Fallback).
  * *Einschränkung:* Antennenreichweite ist mit ca. $800\,\text{m}$ etwa halb so groß wie bei vollwertigen Geräten, besitzt einen internen LiPo-Akku. DLE-Score: **+45 Pkt.**

#### Klasse 1b: Sena Mesh 2.0 (`sena_50_series.json`, `sena_spider.json`):
* *Sena 50S, 50R, 50C, SRL-Mesh:* Etablierter Mesh-2.0-Standard (24–32 Nodes). Kompatibilität zu Mesh 3.0 erfordert Umschaltung in den Legacy-Modus.
* *Sena Spider ST1 vs. Spider RT1:*
  * *Spider ST1:* Nutzt ein großes Jog-Dial (Drehrad). **Achtung für Mechatronik:** Drehräder sind für lineare Hubmagnet-Stößel mechanisch extrem ungünstig und fehleranfällig!
  * *Spider RT1:* Nutzt 3 ergonomische Taster. Mechanisch deutlich zuverlässiger zu betätigen. DLE-Score: **+40 Pkt.**
* *Sena +Mesh (B2M-01):* Älterer reiner Mesh 2.0 Adapter für Bluetooth-Headsets (800 m Reichweite).

#### Klasse 1c: Sena Mesh 1.0 Legacy:
* *Sena 30K:* Älteste Mesh-Generation, heute für Neuinstallationen obsolet.

#### Klasse 1d: Cardo Dynamic Mesh Communications Gen2 (`cardo_packtalk_edge.json`):
* *Cardo Packtalk Edge / Pro:* DMC Gen2 Referenz-Intercom mit Air-Mount-Magnethalterung, USB-C-Dauerladung ("Charge while Riding") und nativer digitaler BLE/Audio-Anbindung.
* *Dedizierte Tasten:* Das Packtalk Edge besitzt klar definierte Taster (`Media`, `Mobile`, `Intercom`) sowie einen axialen Center-Press auf das Drehrad. DLE-Score: **+60 Pkt.**
* *Cardo Packtalk Neo:* Gleicher DMC Gen2 Chip wie Edge, jedoch ohne Air-Mount und laut Spezifikation ohne Dauerladung während des Betriebs.
* *Cardo Packtalk Custom:* Software-limitiertes Abo-Modell.

#### Klasse 1e: Cardo DMC Gen1 Legacy (`cardo_dmc_legacy.json`):
* *Cardo Packtalk Bold, Black, Slim, Smartpack:* DMC 1.0 (bis 15 Teilnehmer), DLE-Score: **+30 Pkt.**

#### Klasse 2: Bluetooth Intercoms & Bluetooth 6.0 (`sena_apex.json`, `cardo_freecom_live.json`):
* **Sena Apex & Apex Plus (`sena_apex.json`):**
  * **Wichtige Richtigstellung:** Das Sena Apex ist **KEIN Mesh-System**, sondern ein modernes **Bluetooth 6.0 Intercom** (2-Wege bei Apex, 4-Wege bei Apex Plus).
  * Nutzt den neuen Bluetooth 6.0 Core für überragende Reichweite und HD-Sprachübertragung. Die Konfiguration via Sena-App erfolgt nativ über BLE GATT.
* *Sena Classic Bluetooth:* 10R, 20S EVO, 5R, 3S Plus, SMH5.
* *Cardo Bluetooth:* Spirit, Spirit HD, Freecom 2x, Freecom 4x (Bluetooth 5.2 Live Intercom mit Auto-Reconnect).
* *Midland Bluetooth:* BTX1 Pro S, BTX2 Pro S, BT Mini, BTR1 Advanced.

#### Klasse 3: PMR446 Jedermannfunk & Digital DMR Tier I (`pmr446_gateway.json` / `omm_446.json`):
* **Klasse 3a (Analog FM):** 16 Kanäle (446.0–446.2 MHz, CTCSS/DCS) für 100 % Kompatibilität mit allen bestehenden Handfunkgeräten im Feld (Midland G7 Pro, G9 Pro, G11, G13, G15, G18).
* **Klasse 3b (Digital DMR Tier I & OMM 446 `PCBA 10`):**
  * **OMM 446 ECE 22.06 UCS Modul:** Volldigitales DMR Tier I + Analog FM Kombimodul auf Basis des NiceRF SA818-DMR Transceivers.
  * Kompatibel zu modernen Digitalfunkgeräten wie dem **Midland D-10** (glasklare, rauschfreie Sprache ohne Knacken bis zur Reichweitengrenze).
  * 100 % digital steuerbar via UART (Kanal, CTCSS, Squelch) über CarPlay / PWA Dashboard.
  * Formschlüssig integrierte 446-MHz-Helixantenne im Pod-Deckel.

#### Klasse 4: OpenMotorMesh 2.4 GHz Universal-Modul (UCS) (`omm_2_4ghz.json`):
* Quelloffenes TDMA / IPv6-Multicast Mesh-Modul auf Basis des **ESP32-C6 (`PCBA 09`)**.
* Nativer Bluetooth 5.3 LE Audio (LC3-Codec) Support (< 30 ms Latenz) für drahtlose Helmkopplung oder formschlüssig in Bucht 1/2 gedockt. DLE-Score: **+55 Pkt.**

---

### 3.2 Praxis-Leitfaden: Universelles OEM-Upcycling für Helmwechsler (Schuberth SC2, Shoei SRL-Serie, HJC Smart 50B)

> [!TIP]
> **Nachhaltiges Gateway-Recycling für Helm-Wechsler:**
> Motorradhelme erreichen nach 5 bis 7 Jahren ihre sicherheitsrelevante Lebensdauer (Materialermüdung des EPS-Styroporkerns nach ECE 22.05/22.06) und müssen ersetzt werden. Wer von **Schuberth** (C5/E2/S3 mit SC2), **Shoei** (Neotec 2/3 oder GT-Air 2/3 mit SRL2/SRL-Mesh/SRL3) oder **HJC** (RPHA 71/91 mit Smart HJC 50B) auf einen neuen Helm oder eine andere Marke wechselt, steht vor einem bekannten Problem:  
> Die bisherigen, teuren Kommunikationssysteme (Neupreis 300–450 €) sind **proprietär auf die Helmschale zugeschnitten** und passen mechanisch in keinen anderen Helm. Am Gebrauchtmarkt bringen sie wegen gealterter Akkus oft kaum noch Erlös.
> 
> **Die OpenMotorBridge-Lösung:** Alle diese Systeme basieren intern auf hochwertiger **Sena-OEM-Hardware** (Sena 50er / Spider-Plattform mit vollem Mesh 2.0 und offiziellem Mesh 3.0 Firmware-Support). Sobald man an die Zuleitungen gelangt, lassen sich diese ausgemusterten Geräte mit minimalem Aufwand als **100 % wartungsfreie, autarke Mesh-Gateways für 0 € Neuinvestition** in Bucht 1 des OMB-Satelliten-Pods weiterbetreiben!

#### Die 4 universellen Upcycling-Säulen ("Universal Gateway Blueprint"):

```
+-----------------------------------------------------------------------------------------+
|             UNIVERSELLER OEM-INTERCOM "BATTERY ELIMINATOR" DAUERSTROM-SCHALTPLAN        |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  [ OMB Pod Bordnetz: PCBA 03 ]                                                          |
|        |                                                                                |
|        +---> VCC_5V (Pin 2)  -------> [ Miniatur Step-Down DC-DC / LDO ]               |
|        |                                 (z. B. MP2315 oder TPS62840)                   |
|        |                                          |                                     |
|        |                                          v +3,75 V DC Festspannung             |
|        |                                          |                                     |
|        |                              +-----------+-----------+                         |
|        |                              |                       |                         |
|        |                              v                       v                         |
|        |                          [ BAT+ ]                 [ NTC ]                      |
|        |                              |                       |                         |
|        |                              | OEM-Platine           +--- [ 10 kOhm NTC ]      |
|        |                              | (Akku ausgelötet)     |    (Simuliert 22 °C)    |
|        |                              v                       v                         |
|        +---> PGND (Pin 1)  ---------> [ BAT- / GND ] <--------+                         |
|                                                                                         |
|  => Modul "sieht" dauerhaft vollen 3,7V-Akku; USB-C bleibt unbeschaltet (keine Ladesperre)|
+-----------------------------------------------------------------------------------------+
```

1. **Säule 1: Der "Battery-Eliminator" (Dauerbetrieb ohne Ladesperre & ohne Brandgefahr):**
   * *Das Lade-Problem:* Nahezu alle Sena-OEM-Geräte (SC2, SRL, Smart HJC) schalten bei 5V an der Ladebuchse aus Sicherheitsgründen sofort ab (*Shutdown on Charge*), um Überhitzung im Helm zu verhindern.
   * *Das Sicherheits-Problem:* Ein alternder LiPo-Pouch-Akku im geschlossenen, sonnenaufgeheizten Motorradkoffer ($> 60^\circ\text{C}$) stellt ein thermisches Risiko dar (Aufblähen, Zelltod).
   * *Die Lösung:* Akku öffnen, Zelle an den Lötfahnen ablöten und entsorgen. Eine stabilisierte $3{,}75\dots 3{,}85\,\text{V}$ Gleichspannung (erzeugt aus den 5V von `PCBA 03` durch einen ultrakompakten Buck-Converter wie MP2315) wird direkt an `BAT+` und `BAT-` gelötet.
   * *Der $10\,\text{k}\Omega$-NTC-Dummy (Essentiell):* Das integrierte Sena-Powermanagement prüft beim Booten den internen NTC-Temperaturwiderstand. Fehlt dieser, verweigert die MCU den Start ("Sensorfehler"). Ein handelsüblicher **$10\,\text{k}\Omega$-Festwiderstand zwischen NTC-Pad und GND** simuliert dauerhaft ideale 22 °C. Das Gerät bootet zuverlässig und ohne Fehlermeldung.

2. **Säule 2: Brummfreie Audio-Anbindung (`J_AUDIO_PWR` auf `PCBA 03`):**
   * Lautsprecherleitungen (L/R) und Mikrofonleitungen führen bei allen OEM-Systemen als Standard-Kupferadern aus der Elektronik.
   * Diese werden auf den vorkonfektionierten 8-Pin JST-SH Stecker von `PCBA 03` gelegt.
   * **Kelvin-Grounding:** Da die Audiomassen (`AGND_SPK` Pin 3 und `AGND_MIC` Pin 6) vollständig von der DC-Versorgungsmasse (`PGND` Pin 1) getrennt geführt werden, ist das Audiosignal absolut resistent gegen hochfrequente Mesh-Sendeimpulse und Generatorpfeifen.

3. **Säule 3: Externe Koaxial-Fahrzeugantenne (Extremer Reichweitengewinn):**
   * Nahezu alle helm-integrierten Systeme führen das 2.4-GHz-HF-Signal über winzige Koaxialkabel (U.FL / IPEX-Stecker oder angelötete Micro-Koax-Pigtails) zu den Helmschalen-Antennen.
   * Im OMB-Basisschlitten wird dieses Kabel über einen kurzen Adapter auf die frontale SMA-Flanschbuchse geführt (`has_sma_port = true`).
   * Daran wird eine externe $2{,}4\,\text{GHz}$-Fahrzeugantenne am Motorradheck angeschlossen.
   * **Vorteil:** Die Funkwellen strahlen frei in alle Richtungen ab – ohne Dämpfung durch Helm-EPS, Vollsichtvisiere oder den Körper von Fahrer und Sozius. Die reale Reichweite im Gruppenverband übertrifft den Helmbetrieb spürbar!

4. **Säule 4: Drahtlose Fernbedienung vs. Direktansteuerung:**
   * **Schuberth SC2:** Verfügt werkseitig über eine separate **Bluetooth Low Energy (BLE) Fernbedienung**. Diese wird einfach per Klett/Clip an die linke Lenkerarmatur gesetzt. **Kein einziges Steuerkabel** muss vom Lenker zum Koffer/Pod verlegt werden!
   * **Shoei SRL-Mesh / SRL3 & HJC Smart 50B:**
     * *Drahtlose BLE-Kopplung:* Unterstützen die offizielle **Sena RC3 / RC4 Lenkerfernbedienung** (BLE) für kabellose Cockpit-Steuerung.
     * *Mechatronische Stößelbrücke:* Alternativ können die kompakten OEM-Tastenmodule direkt in den Schlitten eingelegt und über die 4 Linear-Tauchanker auf `PCBA 03` automatisiert getaktet werden.
     * *Verdrahtete Cockpit-Taster:* Die Tasterleitungen können parallel zu Schließertastern an der Lenkerarmatur geführt werden.

#### Spezifische OEM-Modellübersicht für Upcycling:

| OEM-Modell | Helm-Kompatibilität | Sena-Basisplattform | Mesh-Unterstützung | Antennenanschluss | Besonderheiten für OMB-Pods |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Schuberth SC2** | Schuberth C5, E2, S3 | Sena 50 / Spider | **Mesh 3.0** (offizielle FW) & Mesh 2.0 | Micro-Koax Pigtail | Monolithische Haupteinheit ($75 \times 40 \times 12\,\text{mm}$); BLE-Fernbedienung ab Werk inklusive! |
| **Shoei SRL-Mesh** | Shoei Neotec 2, GT-Air 2, J-Cruise 2 | Sena 50S/50R | **Mesh 3.0** & Mesh 2.0 | U.FL / Koax-Stecker | 3-teiliger Kabelbaum; Nacken-Hauptmodul und Tastenleiste passen flach nebeneinander in Basisschlitten. |
| **Shoei SRL3** | Shoei Neotec 3, GT-Air 3 | Sena 50 Next-Gen | **Mesh 3.0** & Mesh 2.0 | Integrierte Koax-Zuleitung | Kompaktere Gehäusebauform; identisches 3,75V Battery-Eliminator-Prinzip. |
| **Shoei SRL / SRL2** | Shoei Neotec 2, GT-Air 2 | Sena 20S Plattform | Nur Bluetooth 4.1 | Feste Drahtantenne | Reines Bluetooth-Gateway (Klasse 2); ideal für Sozius-Kopplung oder Handy-Navigation. |
| **Smart HJC 50B** | HJC RPHA 71/91, i71, i91, F71 | Sena 50-Serie | **Mesh 3.0** & Mesh 2.0 | U.FL Koaxial-Buchse | Extrem kompaktes Einschub-Hauptmodul; werkseitig aufgeräumte Anschlüsse. |
| **Smart HJC 21B / 20B**| HJC Helme (ECE 22.06) | Sena Bluetooth | Nur Bluetooth 5.1 | Feste Antenne | Kostengünstiges Zweit-Gateway für Telefonie und GPS-Audio. |

#### Mechanischer Einbau in den Universal-Grundschlitten (`00_base_sled.scad`):
* Der lichte Innenraum des Basisschlittens ($124 \times 53 \times 28\,\text{mm}$ bei $130 \times 58 \times 28\,\text{mm}$ Außenmaß) bietet mehr als genug Volumen für alle genannten OEM-Hauptplatinen (die selten größer als $75 \times 40 \times 12\,\text{mm}$ sind).
* Die verbleibenden $35\,\text{mm}$ freier Längsbauraum nehmen den Step-Down-Regler, die NTC-Beschaltung, Audio-Übertrager und die Silikon-Kabelabfänge auf.
* Verschlossen wird das System mit der soliden **Dry-Box Inlay ([`03_insert_blindkassette.scad`](../../hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad))** und 4x M2-Senkkopfschrauben – zu 100 % wetterfest und unsichtbar (oder wahlweise mit einem individuellen 3D-Druck-Inlay mit Tastendurchbrüchen).

---

### 3.3 JSON Profil-Schema Spezifikation
Jedes Hardwareprofil liegt als eigenständige JSON-Datei im internen Flash-Dateisystem (`/data/profiles/*.json`) des ESP32-S31 und definiert alle Pegel-, Routing-, Mechatronik- und BLE-Steuerungs-Parameter:

```json
{
  "id": "sena_spider_x",
  "name": "Sena Spider X Slim (Direct Pod Interface)",
  "vendor": "Sena Technologies",
  "hardware_tier": 1,
  "vcc_enabled": true,
  "direct_dc_supported": true,
  "direct_dc_voltage_v": 3.85,
  "soft_start_ms": 80,
  "input_gain_db": 1.5,
  "output_gain_db": 0.0,
  "noise_gate_threshold_db": -44,
  "control_mode": "direct_digital_and_opto",
  "direct_interface": {
    "controller_type": "ESP32C6_RISCV",
    "onewire_emulation": true,
    "protocol": "usb_cdc_or_uart",
    "num_actuators": 4,
    "command_table": {
      "0x01": { "name": "POWER_BOOT", "actuators": [1, 3], "duration_ms": 1000 },
      "0x02": { "name": "POWER_OFF", "actuators": [1, 3], "duration_ms": 200 },
      "0x03": { "name": "VOL_PLUS", "actuators": [1], "duration_ms": 100 },
      "0x04": { "name": "VOL_MINUS", "actuators": [2], "duration_ms": 100 },
      "0x05": { "name": "MESH_TOGGLE", "actuators": [4], "duration_ms": 200 },
      "0x06": { "name": "GROUP_MESH_TOGGLE", "actuators": [4], "duration_ms": 3000 }
    }
  },
  "ble_control": {
    "supported": true,
    "flavor": "sena_rc_gatt",
    "service_uuid": "0xFFE0",
    "device_name_prefix": "SPIDER-X",
    "capabilities": {
      "power_boot": false,
      "power_off": true,
      "mesh_toggle": true,
      "group_toggle": true,
      "volume_control": true,
      "channel_select": true,
      "mic_mute": true,
      "telemetry": true,
      "le_audio_lc3": false
    },
    "command_mapping": {
      "0x03": { "name": "VOL_PLUS", "ble_cmd": "0xAA550301" },
      "0x04": { "name": "VOL_MINUS", "ble_cmd": "0xAA550302" },
      "0x05": { "name": "MESH_TOGGLE", "ble_cmd": "0xAA550501" },
      "0x06": { "name": "GROUP_MESH_TOGGLE", "ble_cmd": "0xAA550601" }
    },
    "fallback_to_mechatronics_on_disconnect": true
  },
  "mesh_capabilities": {
    "protocol": "Sena_Mesh_3.0_Wave",
    "generation": 3,
    "max_nodes": 32,
    "open_mesh": true,
    "preconfig_channels": 6,
    "dle_bonus_score": 60
  }
}
```

#### Die 5 BLE-Geschmacksrichtungen (`flavor`) im Profil-Schema:
1. **`omm_native` (`0x00MB`):**  
   Nativer OpenMotorMesh BLE 5.3 GATT Server (für `omm_ucs.json` / `PCBA 09` und Gateway-Pods). Bietet granulare 16-Bit Charakteristiken (`0x0001` PTT, `0x0002` Mesh-Modus, `0x0003` Kanal, `0x0004` Lautstärke, `0x0005` Telemetrie, `0x0006` LE Audio LC3 Konfiguration). Volles Bi-direktionales Stereo mit $< 25\,\text{ms}$ Latenz.
2. **`sena_rc_gatt` (`0xFFE0`):**  
   Sena Remote Control GATT Protokoll (kompatibel mit Sena RC3, RC4, Handlebar Remote). Steuert Mesh On/Off, Gruppenmesh, Lautstärke und Kanalwechsel ohne physische Stößelbewegungen.
3. **`cardo_ble_v2` (`0xFE59`):**  
   Cardo Connect / Packtalk Edge/Pro Remote BLE API. Unterstützt DMC Mute/Unmute, Lautstärke-Inkremente und Gruppen-Reconnects.
4. **`hid_consumer_control` (`0x0C`):**  
   Standard Bluetooth Human Interface Device Consumer Control für Legacy-Headsets und Midland BTR1 (Lautstärke, Wiedergabe/Pause).
5. **`none`:**  
   Keine BLE-Schnittstelle vorhanden (reine Analogfunkgeräte wie Midland G9 Pro PMR446, `omm_pmr446.json` oder deaktivierte Pods). Sämtliche Befehle werden direkt über die OptoMOS PTT-Schaltung ausgeführt.

> [!NOTE]
> **Architektur-Grundsatz:** Im `ble_control`-Objekt ist `power_boot` prinzipbedingt **immer `false`**, da unbestromte Intercom-Geräte im Deep-Sleep/Aus-Zustand kein Bluetooth empfangen können. Das Einschalten erfolgt ausnahmslos über den initialen mechanischen Kaltstart-Impuls der Hubmagnete (`0x01`). Während der gesamten Fahrt wird anschließend zu 100 % verschleißfrei digital per BLE gesteuert. Verliert die Verbindung den Sync, greift sofort `fallback_to_mechatronics_on_disconnect`.

---

## 4. 4-Draht USB-PD Pod-Erkennung, Gestaffeltes Power-Sequencing & Plug-and-Play

Jede Satelliten-Pod Trägerplatine (`PCBA 03`) ist über den geschirmten 4-Draht Automotive Bus angebunden. Die Erkennung erfolgt nativ über High-Speed USB 2.0 Deskriptor-Austausch (CDC-ACM / HID) beim Booten:

```
+-------------------------------------------------------------+
|        4-DRAHT USB-PD PLUG-AND-PLAY & SEQUENCING ABLAUF     |
+-------------------------------------------------------------+
| 1. GESTAFFELTE BESTROMUNG (Power-Sequencer via DTM-12):     |
|    * T=0ms: Zentralbox & Front-Node booten synchron auf KL15|
|    * T=200ms: Pod 1 (VCC_BUS via TPS25982 eFuse Soft-Start) |
|    * T=350ms: Pod 2 (VCC_BUS via TPS25982 eFuse Soft-Start) |
|    * T=500ms: Heckradar (+12V DC geschaltet)                |
+-------------------------------------------------------------+
| 2. USB 2.0 HIGH-SPEED ENUMERATION & DESKRIPTOR-HANDSHAKE:   |
|    * PCBA 03 enumeriert am internen USB2514B Hub            |
|    * Überträgt 64-Bit UID & Hardware-Deskriptor             |
|    * Handelt USB-PD Ladeleistung aus (bis 30W je Pod)       |
+-------------------------------------------------------------+
| 3. PROFILAKTIVIERUNG & AUDIO-FREIGABE:                      |
|    * Zentralbox lädt /storage/profiles/<UID>.json           |
|    * Audio-Routing via DSP & Bluetooth zum Helm freigeschalt|
|    * OptoMOS PTT & digitale BLE/USB Schnittstellen aktiv    |
+-------------------------------------------------------------+
```

### 4.1 Die 3 Phasen der 4-Draht USB Plug-and-Play Erkennung
1. **Phase 1: Gestaffelte Bestromung (Power-Sequencing):**  
   Um Einschaltstromspitzen (Inrush Currents) beim Zündungsstart nach ISO 16750-2 sicher unter dem Schwellenwert der Bordnetzsicherung zu halten, werden die Satelliten-Buchten gestaffelt bestromt:
   - $T = 0\,	ext{ms}$: Zentralbox (`PCBA 01`) und Front-Node (`PCBA 05`) starten synchron bei Zündung EIN (KL15).
   - $T = 200\,	ext{ms}$: Pod 1 erhält VBUS über die programmierbare Automotive eFuse `TI TPS25982` mit definierter Soft-Start-Rampe.
   - $T = 350\,	ext{ms}$: Pod 2 erhält VBUS über die zweite eFuse.
   - $T = 500\,	ext{ms}$: Heckradar erhält geschaltete +12V DC.
2. **Phase 2: High-Speed USB Enumeration:**  
   Sobald die MCU auf PCBA 03 bootet ($< 25\,	ext{ms}$), meldet sie sich am USB 2.0 Host der Zentralbox:
   - Überträgt 64-Bit Hardware-UID, Firmware-Version und Hardware-Klasse (`0x01` Sena, `0x02` Cardo, `0x03` OMM, `0x04` Midland, `0x00` Dry Box).
   - Verifiziert den kryptografischen Geräte-Deskriptor.
   - Handelt USB-PD Leistungsprofile (5V/3A, 9V/3A, 12V/2.5A) für den internen Koffer-Ladeport aus.
3. **Phase 3: Automatische Profil-Aktivierung:**  
   - Die Zentralbox prüft das LittleFS-Flash auf `/storage/profiles/<UID>.json`.
   - Das passende Herstellerprofil (Gain-Level, Raised-Cosine Ducking-Prioritäten, PTT-Mappings) wird im ESP32-S311 DSP aktiviert.
   - Ist ein Pod leer oder als Dry-Box konfiguriert, bleibt der Audiozweig im sicheren `disabled.json` Zustand (Ladefunktion bleibt aktiv).

### 4.2 Steuerungs-Hierarchie: Digitaler BLE/USB-Primärpfad & OptoMOS-Keying
* **Laufzeit-Befehle via BLE GATT & AVRCP:** Mesh-Aktivierung, Gruppenwechsel, Lautstärke und Statusabfragen erfolgen 100 % digital über standardisierte Funk- und USB-Protokolle.
* **OptoMOS PTT-Keying:** Für Analogfunk (Midland PMR446) tastet das optoisolierte Relais `CPC1017N` prellfrei und galvanisch getrennt gegen Masse.
* **Automatisierter Kaltstart:** Über USB-PD Power-Path-Management startet das Headset bei Zündung EIN automatisch und fährt bei Zündung AUS geordnet herunter.

## 5. Systematik der OEM-Adapter-Anbindung: Klassen & Verkabelung

OpenMotorBridge unterstützt alle marktgängigen Intercom-Geräte im Originalzustand ohne Öffnen des Gehäuses:

```
+----------------------------------------------------------------------------------------+
|                   ÜBERSICHT DER 5 OEM-ADAPTER ANSCHLUSS-KLASSEN                       |
+-------------------+-----------------------------+--------------------------------------+
| Adapter-Klasse    | Typische Geräte-Vertreter   | Anschluss- & Schnittstellen-Typ      |
+-------------------+-----------------------------+--------------------------------------+
| **Klasse A:**     | Sena +Mesh (B2M-01),        | * Reine 5V-Speisung (90° Micro-USB / |
| Drahtlos-Bridge   | Sena MeshPort Blue / Red,   |   USB-C) über Header J_AUDIO_PWR     |
| (Nur-Strom / USB) | Cardo Packtalk Outdoor Dongle|   (Pin 1 & 2)                        |
|                   |                             | * Audio drahtlos via Bluetooth      |
|                   |                             | * Externe SMA-Bulkhead Doppelbuchse  |
|                   |                             | * Mechanik: OEM-Schlitten & Gummiband|
+-------------------+-----------------------------+--------------------------------------+
| **Klasse B:**     | Sena 50S, 60S, 30K,         | * Vollwertig analog (Audio In & Out) |
| Pogo-Pin Klemmen  | Sena 20S EVO, SRL3          | * Flachband von J_AUDIO_PWR auf      |
| (Federkontakt-Bett|                             |   Pogo-Pin Kontaktleiste im Inlay    |
|                   |                             | * AO3400A PTT-Tastung auf PCBA 03    |
| **Klasse C:**     | Cardo Packtalk Edge,        | * Vollwertig analog (Audio In & Out) |
| Magnetischer      | Cardo Packtalk Pro          | * 5-Pol Federkontaktfeld im Inlay    |
| Air-Mount         | *(Neo/Custom ausgeschlossen)| * 2x N52 Neodym-Magnete mit Führungs-|
|                   |                             |   keil für werkzeugloses Andocken    |
+-------------------+-----------------------------+--------------------------------------+
| **Klasse D:**     | Cardo Packtalk Bold / Black,| * Vollwertig analog (Audio In & Out) |
| Schiebe-Cradle    | Cardo Freecom 1 / 2 / 4+    | * Seitliche Schiebekontakte im Inlay |
|                   |                             | * Mechanik: Gleitschiene mit Arretier|
+-------------------+-----------------------------+--------------------------------------+
| **Klasse E:**     | Midland G7 / G9 Pro, G13,   | * 2-Pin Doppelklinke (2.5mm + 3.5mm) |
| Analoger Funk     | Midland XT30, Baofeng,      | * AO3400A tastet PTT gegen Masse     |
| (PMR446 / Kenwood)| Kenwood TK-Serie            | * 5V DC/DC Speisung (Batteriedummy)  |
|                   |                             | * Feste 446MHz Wendel oder SMA-Front |
+-------------------+-----------------------------+--------------------------------------+
```

> [!IMPORTANT]
> **Ausschlusskriterium für Cardo Packtalk Neo & Custom ("Laden während Betrieb"):**
> * Das **Cardo Packtalk Neo** besitzt keinen magnetischen Air-Mount, sondern ein fest verkabeltes Klick-Cradle. Entscheidender ist jedoch die elektronische Inkompatibilität: Laut offizieller Cardo-Spezifikation unterstützt das Neo **kein Laden während des Betriebs** (*"Charge while riding: Nein"*). Da OpenMotorBridge prinzipbedingt als fahrzeuggebundenes System permanent über das 12V-Bordnetz (via PCBA 03) gespeist wird, scheidet das Neo aus - das Headset schaltet bei USB-Spannung ab bzw. kann auf ganztägigen Touren nicht unterbrechungsfrei betrieben werden.
> * Das **Cardo Packtalk Custom** erfordert zudem kostenpflichtige Monats-/Jahresabonnements zur Freischaltung von Kernfunktionen und widerspricht damit dem abofreien Open-Source-Grundsatz von OpenMotorBridge.
> * **Empfehlung für Cardo-Mesh:** Ausschließlich **Cardo Packtalk Edge** (oder Packtalk Pro) einsetzen, da diese Modelle vollwertiges Schnellladen während aktiver Mesh-Kommunikation unterstützen.

### 5.1 Detaillierte Pin-Belegung der Pod-Schnittstelle (`J_AUDIO_PWR` / 8-Pin JST-SH 1.0mm)

Um das gefürchtete **Übersprechen von Lade- und Sendeströmen in das Audiosignal (Common-Impedance Coupling)** physikalisch zu verhindern, ist der Header `J_AUDIO_PWR` auf `PCBA 03` als **8-Pin JST-SH Steckverbinder** mit vollständiger Kelvin-Massen-Trennung ausgeführt:

| Pin | Signal | Klasse 1a/1b (Sena SPIDER X Slim) | Klasse 1d (Cardo Packtalk Edge) | Klasse 3a (Midland PMR446) | Klasse 4 (OMM 2.4/446 UCS) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `PGND` | 2-Pin DC Return (Power Ground) | USB-C Lade-Masse (Power Ground) | DC Batteriedummy GND | USB-C Power Return |
| **2** | `VCC_HEADSET` | +3.85V Direct-DC Speisung | +5V VBUS Schnellladung | +5V VBUS Batteriedummy | +5V VBUS Power-Path |
| **3** | `AGND_SPK` | Klinke 3.5mm Schirm (Audio GND, $I=0$) | Klinke 3.5mm Schirm (Audio GND, $I=0$) | Klinke 3.5mm Schirm (Audio GND, $I=0$) | Audio Ground (DAC/ADC, $I=0$) |
| **4** | `AUDIO_L_IN` | 3.5mm Klinke Links (Spk In L $\leftarrow$) | 3.5mm Klinke Links (Spk In L $\leftarrow$) | 3.5mm Klinke Mono (Spk In $\leftarrow$) | I2S / Line-In Links ($\leftarrow$) |
| **5** | `AUDIO_R_IN` | 3.5mm Klinke Rechts (Spk In R $\leftarrow$) | 3.5mm Klinke Rechts (Spk In R $\leftarrow$) | 3.5mm Klinke gebrückt (Spk In $\leftarrow$) | I2S / Line-In Rechts ($\leftarrow$) |
| **6** | `AGND_MIC` | 2.5mm Mic Rückleiter (Audio GND, $I=0$) | Cardo 2-Pin Mic- (Audio GND, $I=0$) | 2.5mm Mic Schirm (Audio GND, $I=0$) | Mic Ground ($I=0$) |
| **7** | `MIC_OUT` | 2.5mm Mic Signal (Voice Out $\rightarrow$) | Cardo 2-Pin Mic+ (Voice Out $\rightarrow$) | 2.5mm Mic Signal (Voice Out $\rightarrow$) | Mic Signal (Voice Out $\rightarrow$) |
| **8** | `PTT_IO` | N/C (Mechatronik aktiv) | N/C (Mechatronik aktiv) | PTT-Tastung gegen Masse (MOSFET `Q4`) | Digital PTT / Config IO |

> [!IMPORTANT]
> **Kein Strombrummen dank Kelvin-Grounding:**
> Über die Pins 3 (`AGND_SPK`) und 6 (`AGND_MIC`) fließt **kein Lade- oder Betriebsstrom** ($I = 0\,\text{A} \implies \Delta V = 0\,\text{mV}$). Der bis zu $600\,\text{mA}$ starke Lade- und HF-Sendestrom fließt ausschließlich über Pin 1 (`PGND`) direkt zum DC-Filter der Trägerplatine ab. Dadurch bleibt das empfindliche Mikrofonsignal ($5\dots 15\,\text{mV}$) zu 100 % frei von Mesh-TDMA-Knattern und Schaltregler-Pfeifen!

---

## 6. Sicherheits-Fallback: `disabled.json` & Zero-Trust Quarantäne

Wird ein Steckplatz nicht belegt, eine Dry-Box eingesetzt oder ein Pod in der WebApp manuell stillgelegt, lädt der ESP32-S31 sofort das Profil `disabled.json`:

```json
{
  "id": "disabled",
  "name": "Deaktiviert / Unbelegt (Disabled Slot)",
  "vendor": "OpenMotorBridge System",
  "hardware_tier": 0,
  "vcc_enabled": false,
  "soft_start_ms": 0,
  "input_gain_db": -96.0,
  "output_gain_db": -96.0,
  "ducking_attenuation_db": 0.0,
  "ducking_attack_ms": 0,
  "ducking_release_ms": 0,
  "noise_gate_threshold_db": -96,
  "control_mode": "disabled",
  "opto_trigger_duration_ms": 0,
  "opto_trigger_hold_ms": 0,
  "mesh_capabilities": {
    "protocol": "None",
    "max_group_nodes": 0,
    "dle_bonus_score": 0
  },
  "audio_routing": {
    "intercom_bridge": false,
    "rider_headset": false,
    "pillion_headset": false,
    "boombox_lineout": false
  }
}
```

### 6.1 Schutzwirkungen des `disabled.json` Profils
1. **Stromlos-Schaltung (`vcc_enabled: false`):** Die elektronische Sicherung (eFuse) auf PCBA 01 trennt die Bucht sofort ab $\rightarrow 0{,}0\,\text{mA}$ Ruhestrom.
2. **Vollständige Audio-Stummschaltung:** Ein- und Ausgangs-Gains des ES8388 Codecs werden auf $-96\,\text{dB}$ gesetzt, um jegliches Rauschen oder Einstreuungen zu eliminieren.
3. **Deaktivierung von Schaltsignalen:** Die AO3400A MOSFETs auf PCBA 03 bleiben gesperrt, um jegliche Tasterbetätigung zu verhindern.
4. **Capability-Bereinigung:** Der Capability-Score-Beitrag für den Routing-Graphen fällt sofort auf 0 Punkte zurück.

### 6.2 Zero-Trust Hardware-Quarantäne (Fail-Safe Schutzabschaltung)
Solange eine neu angeschlossene Pod-Hardware (Pod-Hardware UID) keinem verifizierten Profil zugewiesen wurde, wird der entsprechende Pod-Steckplatz **strikt wie ein unvollständig oder fehlerhaft gesteckter Slot behandelt**:
* **5V VCC Power-Gate OFF (0,0 mA):** Die eFuse zum OEM-Gerät bleibt gesperrt.
* **Audio DSP Mute (-96 dB):** Beide Audiokanäle sind stummgeschaltet, um Knacken, Rauschen oder Brummschleifen zu verhindern.
* **Aktuatoren gesperrt:** Keine unkontrollierten Tastimpulse an das Headset.
* **Routing-Bonus = 0:** Keine Beeinflussung der Gruppen-Wahl.
* **Freigabe erst nach Bestätigung:** Erst wenn der Nutzer in der WebApp das Profil bestätigt (oder die UID bereits im Flash-Mapping hinterlegt ist), führt der Controller eine kontrollierte Soft-Start-Einschaltsequenz (50 ms Inrush-Limiting) durch und schaltet die Audiopegel frei.

---

## 7. WebApp-Workflow: Automatische Erkennung & Profilzuweisung

Beim Erkennen einer neuen Pod-Hardware führt die PWA einen automatischen Onboarding-Dialog aus:

```
+-------------------------------------------------------------+
| 🧩 NEUER POD ERKANNT!                                       |
+-------------------------------------------------------------+
| Erkannter Steckplatz:   Pod 1 (Bucht links)                 |
| Pod-Hardware UID:      02:A2:3B:4C:5D:6E:7F:8A             |
+-------------------------------------------------------------+
| Dieser Pod-Hardware wurde bisher noch kein Profil           |
| zugewiesen. Welches Intercom oder Funkgerät ist verbaut?    |
|                                                             |
| Hardware-Profil:  [ 🔵 Sena 50S / 50R / SRL3 (K1)      v ]  |
+-------------------------------------------------------------+
| [ Später zuweisen ]         [ Profil zuweisen & speichern ] |
|                                                             |
| *Bei reinen BT-Adaptern (z.B. Sena Mesh+):                  |
| [ 🔍 Bluetooth-Gerät koppeln ]                              |
+-------------------------------------------------------------+
```

1. **Automatischer USB-Handshake:** Sobald die Bucht über das gestaffelte Power-Sequencing bestromt wird, meldet sich der Pod über den USB-Deskriptor `USB_DESC_POD_ANNOUNCE` mit ihrer 64-Bit Hardware-UID. Die Zentralbox leitet die UID via BLE an die WebApp weiter.
2. **Dialog-Pop-up:** Die WebApp vergleicht die UID mit der Zuordnungstabelle (`/profiles/mapping.json` / PWA `localStorage`). Ist die UID neu, öffnet sich automatisch das Zuweisungs-Modal (`#uuid-detect-modal`).
3. **Profil-Auswahl & Speicherung:** Der Fahrer wählt sein Modell aus dem Dropdown. Bei drahtlosen Bluetooth-Adaptern (z. B. Sena Mesh+) kann direkt der Scan- und Kopplungsworkflow ausgelöst werden.
4. **Persistentes Mapping:** Das Mapping `{"<UID>": "<profile_id>"}` wird dauerhaft im ESP32 LittleFS und im Browser gespeichert.
5. **Wiedererkennung:** Zukünftig wird dieser Pod an jedem beliebigen Steckplatz sofort automatisch parametrisiert.

### 7.1 Dynamisches Profil-Update & JSON-Merge-Verfahren
Wenn ein Hersteller (z. B. Sena beim Sprung von Mesh 2.0 auf Mesh 3.0 oder Cardo bei DMC Gen 2) seine Firmware aktualisiert, passt sich OpenMotorBridge über ein intelligentes **JSON-Merge-Verfahren** an:

```
+-------------------------------------------------------------+
|                 JSON PROFIL-MERGE-VERFAHREN                 |
+------------------------------+------------------------------+
| 1. Basis-Herstellerprofil    | 2. Individuelle User-Offsets |
|    (z.B. sena_apex_v3.json)  |    (Ducking & Audio-Gains)   |
+------------------------------+------------------------------+
|                             v                               |
| 3. Gemergtes Live-Profil im LittleFS Flash-Speicher          |
|    (Aktualisierte Mechatronik-Timings + persönliche Gains)  |
+-------------------------------------------------------------+
```

* **Phase 1 (Basis-Parameter):** Neue Aktuator-Pulsdauern (z. B. `ptt_pulse_ms: 180`), geänderte Kanalwechselmuster und Capability-Scores werden aus dem neuen Hersteller-JSON geladen.
* **Phase 2 (User-Settings Preservation):** Individuelle Anpassungen des Fahrers (z. B. $+2{,}0\,\text{dB}$ Mikrofonpegel, $-12\,\text{dB}$ Navi-Ducking) bleiben beim Update erhalten und werden über die Basiswerte gemerged.
* **Phase 3 (Hot-Reload):** Die Zentralbox wendet die gemergten Parameter im laufenden Betrieb ohne Neustart sofort auf den ES8388 Codec und die Mechatronik-Engine an.

### 7.2 Hardware-Upgrade & OEM-Adapter-Update (Austausch des Headsets im bestehenden Pod)
Rüstet der Fahrer nach einiger Zeit sein Intercom auf (z. B. von Sena 20S auf Sena 60S Mesh 3.0 Wave) und behält die Trägerplatine bei:
1. **Unveränderte Chip-UID:** Die 64-Bit Hardware-UID des Pod-Controllers bleibt identisch.
2. **Auswahl im Dashboard:** Im Tab **"🧩 Pods & DLE"** der WebApp wählt der Fahrer im Dropdown des Slots einfach das neu eingebaute Modell (*"⚡ Sena 60S (Mesh 3.0 Wave)"*).
3. **Automatisches Überschreiben:** Die WebApp aktualisiert sofort das Mapping synchron im Browser und im ESP32 LittleFS (`/profiles/mapping.json`).
4. **Verlässlicher Reload:** Beim nächsten Einstecken oder Booten wird sofort das neue Profil mit den neuen Mechatronik-Timings und dem höheren Capability-Score (+60 Pkt.) geladen.
5. **Ground-Truth Re-Sync (`🔄 Sync`):** Mit dem Sync-Button kann der Fahrer jederzeit verifizieren, welches Profil der real gesteckten Hardware-UID im Flash zugeordnet ist.

---

## 8. Empfohlene Bestückungs-Szenarien nach Preis und Einsatzzweck

```
+-----------------------------------------------------------------------------+
|                 EMPFOHLENE POD-BESTÜCKUNGS-SZENARIEN                        |
+-----------------------+-------------------------+---------------------------+
| Setup-Kategorie       | Pod 1 (Links)           | Pod 2 (Rechts)            |
+-----------------------+-------------------------+---------------------------+
| ⭐ **OMB-Empfehlung** | **Sena SPIDER X Slim**  | **Cardo Packtalk Edge**   |
|   (Preis-Leistungs-   | (Mesh 3.0 Direct-DC,K2a)| (DMC Gen2 Air-Mount, K4)  |
|    Sieger & Referenz) | (DLE +60 Pkt., ~210 €)  | (DLE +60 Pkt., ~320 €)    |
+-----------------------+-------------------------+---------------------------+
| 💎 **High-End Leader**| **Sena 60S / Apex**     | **Cardo Packtalk Edge**   |
|    (350 - 550 €)      | (Mesh 3.0 Wave, K1)     | (DMC Gen2 Air-Mount, K4)  |
+-----------------------+-------------------------+---------------------------+
| ⚖️ **Lean & Modern**  | **Sena SPIDER X Slim**  | **Cardo Freecom 4x / Bold**|
|    (180 - 260 €)      | (Mesh 3.0 Direct-DC,K2a)| (Live Intercom/DMC, K5/K6)|
+-----------------------+-------------------------+---------------------------+
| 💰 **Budget Einstieg**| **Sena MeshPort Blue**  | **IP67 Dry-Box**          |
|    (80 - 140 €)       | (oder Sena 20S/SF, K3)  | (Slot stromlos / disabled)|
+-----------------------+-------------------------+---------------------------+
| 🏔️ **Adventure/Offroad**| **Sena Apex / 50S**   | **Midland G9 Pro PMR446** |
|    (220 - 320 €)      | (Mesh 3.0, K1)          | (Analogfunk Gateway, K7)  |
+-----------------------+-------------------------+---------------------------+
```

### 8.1 Warum das Sena SPIDER X Slim unsere offizielle Referenz-Empfehlung für Pod 1 ist

Das **Sena SPIDER X Slim** (Klasse 2a - `sena_spider_x.json`) ist die **offizielle Primärempfehlung** des OpenMotorBridge-Projekts für Satelliten-Pod 1. Es vereint alle geforderten Next-Gen-Funkmerkmale mit einer idealen mechanischen und elektrischen Eignung für den Pod-Betrieb:

1. **Volle Mesh 3.0 & Wave Parität (Zukunftssicher ohne Kompromisse):**
   * Bietet die identische, modernste Mesh-Architektur wie Senas teure Flaggschiffe (Sena 60S / Apex) mit **Mesh 3.0 & 2.0**, Wave Intercom und Bluetooth 5.3.
   * Unterstützt bis zu 32 Teilnehmer im Mesh (Multi-Channel Open Mesh Kanäle 1-6) und erhält den **vollen DLE-Score-Bonus von +60 Punkten**.

2. **Befreit von nutzlosem Helm-Overhead (Schlankes Transceiver-Design):**
   * Klassische Flaggschiff-Headsets (wie das 60S oder 50S) sind mit teuren Drehrädern (Jog-Dial), Helmlampen, LCD-Statusschirmchen und fest integrierten Lautsprecher-Kabelsträngen überfrachtet - Komponenten, die im geschlossenen Pod-Gehäuse am Motorrad völlig nutzlos sind, Platz rauben und mechanisch verschleißen können.
   * Das SPIDER X Slim ist radikal auf das Wesentliche reduziert: Mit ultrakompakten Abmessungen von $74{,}5 \times 31 \times 16\,\text{mm}$ und einem Federgewicht von nur **$23{,}2\,\text{g}$** passt es ideal in den Pod-Bucht.

3. **Direct-DC & Integrierte 3-fach Kabelpeitsche (Kein Pogo-Pin-Cradle nötig!):**
   * **Der größte Konstruktions- und Praxiserfolg:** Laut offizieller Sena-Dokumentation (*SPIDER X Slim Benutzerhandbuch v1.0.0*, S. 6) führt die Haupteinheit alle drei elementaren Schnittstellen über robuste, werkseitige Miniatur-Steckverbinder an einer flexiblen Kabelpeitsche heraus:
     * **Anschluss ⑧: Akkupack-Anschluss (Direct-DC):** 2-polige Zuleitung für permanente $3{,}85\,\text{V}$-Festspannung direkt vom Träger-PCB (kein LiPo-Akku im Pod, keine Brandgefahr, keine Alterung!).
     * **Anschluss ⑨: Mikrofon-Buchse:** Direkte Einspeisung des analogen Sprachsignals vom ES8388 Audio-Codec / DAC auf der Trägerplatine (keine externe Mikrofon-Kapsel nötig).
     * **Anschluss ⑩: Lautsprecher-Buchsen:** Direkter Audio-Line-Abgriff des ankommenden Mesh-Funkverkehrs in den Line-In / ADC des ES8388 Codecs.
     * *(Zusätzlich: Anschluss ⑦ USB-C an der Stirnseite für optionale Service-/OTA-Wartung).*
   * **Mechanischer Meilenstein (Null Pogo-Pins):** Es ist **kein klobiges, fehleranfälliges Klemm-Cradle mit Federkontakt-Pogo-Pins** (wie bei Sena 50S/60S oder Cardo Packtalk) erforderlich! Pogo-Pins neigen bei Motorrad-Vibrationen ($> 20\,\text{g}$) und Feuchtigkeit zu Kontaktprellen, Übergangswiderständen und Korrosion. Beim SPIDER X Slim werden alle drei Stecker direkt, formschlüssig und vibrationsfest über einen passiven Adapterkabelstrang auf den 8-poligen JST-SH Header `J_AUDIO_PWR` des OMB-Pod-Trägers (PCBA 03) gesteckt.
   * **100 % Plug & Play, Null Lötarbeiten, voller Garantieerhalt:** Das Originalgehäuse muss nicht geöffnet, mechanisch beschädigt oder umgelötet werden. Das Modul wird einfach aus der Verkaufsverpackung in den 3D-Druck-Schlitten gelegt und angesteckt.
   * **Automatisches Booten & Abschalten:** Das Modul startet stabil mit der Zündung (KL15) und schaltet bei Zündung-AUS sauber ab.

4. **Überragendes Preis-Leistungs-Verhältnis:**
   * Mit einem Marktpreis von ca. **180 - 240 €** (Straßenpreis) bietet das SPIDER X Slim die exakt gleiche DLE-Netzwerkleistung (+60 Pkt.) wie ein Sena 60S (ca. 450 - 550 €) - bei mehr als 50 % Kostenersparnis!

---

## 9. Proximity & Standstill Privacy Mute (Lokal-Gesprächsmodus bei Zwischenstopps)

### Problemstellung im Gruppen-Mesh
Halten zwei Fahrer einer Motorradgruppe an einer roten Ampel, an einer Mautstation oder am Straßenrand nebeneinander an und klappen ihre Helmvisiere hoch, um sich direkt abzustimmen:
1. **Akustische Echos & Rückkopplungsschleifen:** Das Mikrofon von Fahrer A erfasst die Stimme von Fahrer B mit einer Latenz von $15\dots 30\,\text{ms}$, wodurch im Helmlautsprecher ein störender Hall-Effekt entsteht.
2. **Kanalbelastung für die restliche Gruppe:** Die anderen 6-10 Fahrer der Gruppe (die 500 Meter weiter vorne oder hinten fahren) müssen die private Abstimmung zwangsweise mitanhören.

### Intelligente Nahbereichs-Stummschaltung
OpenMotorBridge löst dieses Problem durch eine vollautomatische **Proximity-Mute-Logik**:

```
+----------------------------------------------------------------------------------------+
|               PROXIMITY & STANDSTILL PRIVACY MUTE LOGIK                                |
+----------------------------------------------------------------------------------------+

  [1. SENSORIK-AUSWERTUNG IN ECHTZEIT]
  +-- Bedingung 1: Fahrzeug steht still (CAN-Geschwindigkeit v = 0.0 km/h)
  +-- Bedingung 2: Partner-Motorrad im extremen Nahbereich (< 3.0 m)
                   Erkannt über OMM 2.4 GHz RSSI (> -45 dBm)

  [2. AKUSTISCHER ÜBERGANG (Automatisch)]
  +-- OpenMotorBridge schaltet den Mikrofon-Uplink in das Weitverkehrs-Mesh STUMM
  +-- Diskreter Bestätigungston im Helm (Zweiklang "Lokal-Modus aktiv")
  +-- Fahrer unterhalten sich ganz natürlich durch die offenen Visiere von Angesicht zu Angesicht!

  [3. AUTOMATISCHE REAKTIVIERUNG DES MESH-NETZES]
  +-- Option A: Das Motorrad fährt wieder an (v > 8.0 km/h)
  +-- Option B: Fahrer tippt kurz den Lenker-PTT an (< 400 ms) -> Mesh sofort wieder offen!
```
