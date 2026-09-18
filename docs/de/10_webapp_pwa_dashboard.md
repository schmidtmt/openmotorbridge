# 10 - WebApp PWA & Dashboard-Bedienung

Dieses Dokument spezifiziert die Architektur des autarken **Progressive Web App (PWA) Dashboards**, die Web Bluetooth (WebBLE) Kommunikation, den lokalen **IndexedDB Offline-Speicher**, die Bedienoberfläche des **Universal Front-Knotens** (1-Klick CarPlay Kaltstart, Fahrtwind-VU-Meter, Auto-Café Timer) sowie die **Export-Engine für erweiterte GPX-Formate** (Navi Shaping Points & Video Telemetrie).

---

## 1. Architektur & Offline-Fähigkeit

Das Dashboard ist eine vollständig autarke Progressive Web App (PWA) basierend auf standardisiertem HTML5, modernem Vanilla CSS3 (Glassmorphismus-Design) und ES6 JavaScript. Die App kommuniziert über die Web Bluetooth API (WebBLE) direkt mit dem ESP32-S3 der Zentralbox – ohne Cloud-Zwang oder externe Serverabhängigkeiten.

- **Lokaler Offline-Speicher (IndexedDB):** GPX-Touren können über BLE direkt von der MicroSD-Karte heruntergeladen und in der lokalen `omb_tours_db` des Browsers gesichert werden.
- **Service Worker Caching:** Die gesamte WebApp läuft offlinefähig im Browser (Cache-First Strategie für PWA Installation auf iOS und Android).

### 1.1 Plattform- & Browser-Kompatibilität (Web Bluetooth)

| Plattform | Empfohlener Browser | Verbindungsmethode & Besonderheiten |
| :--- | :--- | :--- |
| **Android / PC / Mac / Linux** | **Google Chrome, MS Edge, Opera** | **Nativ:** Direkte Unterstützung der Web Bluetooth API. Voraussetzung: Sicherer Kontext (`https://` oder `http://localhost`). |
| **Apple iOS / iPadOS** (iPhone, iPad) | **[Bluefy – Web BLE Browser](https://apps.apple.com/app/bluefy-web-ble-browser/id1492822055)** | **Erforderlich:** Apple blockiert in WebKit/Safari den direkten BLE-Zugriff. *Bluefy* stellt eine standardkonforme Brücke über Apples natives *CoreBluetooth* bereit. |

### 1.2 Native Android Begleit-App & Google Play Store (TWA / Native Companion)
Für Fahrer, die eine Installation über den Google Play Store, automatische Hintergrund-Dienste oder Zero-Touch Bluetooth-Wiederverbindung bevorzugen, ist die Android-App-Identität in der Google Play Console reserviert:
* **App-Name:** `OpenMotorBridge`
* **Package Name / Application ID:** `bar.f0o.omb`
* **Integrations- & Architekturpfade:**
  1. **Trusted Web Activity (TWA):** Schlankes Android-Package basierend auf Chrome Custom Tabs und Google Digital Asset Links (`.well-known/assetlinks.json`). Ermöglicht 1-Klick-Installation aus dem Google Play Store, native Vollbild-Darstellung ohne Browserleiste und native WebBLE-Unterstützung mit null Wartungs-Overhead zur WebApp.
  2. **Nativer Foreground Service (BLE Auto-Reconnect & Background Sync):** Optionaler nativer Begleitdienst mit Sticky-Notification (*„OpenMotorBridge aktiv“*). Hält die BLE-GATT-Verbindung zur Zentralbox auch dann stabil aufrecht, wenn das Smartphone bei ausgeschaltetem Display in der Jackentasche verbleibt, startet automatisches GPX-Fahrt-Logging bei Zündung EIN und leitet eCall-Notrufe selbst im Hintergrund verzögerungsfrei weiter.
  3. **Integrierter Internet-Uplink Proxy (Layer-5 SOCKS5 / HTTP-Relay):** Fungiert als transparenter lokaler Uplink-Proxy für den Front-Node (PCBA 05) und das Werks-Navi (z. B. Harley Skyline OS / Boom! Box GTS für HERE-Live-Traffic).
     * **Kein VPN-Konflikt:** Arbeitet rein auf Anwendungsebene (L5 POSIX-Sockets) und belegt **keinen** Android `VpnService`-Slot. Dauerhafte VPNs wie **Tailscale** (z. B. für Smart-Home-Zugriff / *Homesphere* / Home Assistant) bleiben uneingeschränkt aktiv.
     * **Kein Hotspot-Zwang:** Der Akku-fressende persönliche WLAN-Hotspot am Smartphone muss nicht manuell aktiviert werden; Datenanfragen der Headunit laufen geräuschlos über die Companion-App via Mobilfunk.
     * **Automatischer Cloud- & WebDAV-Sync:** Telemetriedaten und GPX-Touren können live oder nach Fahrtende direkt über den Proxy in private Clouds oder MQTT-Broker gepusht werden.

---

## 2. Dashboard Tabs & Funktionsumfang

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OPENMOTORBRIDGE PWA DASHBOARD NAVIGATION                        │
├─────────────────┬─────────────────┬──────────────────┬────────────────┬────────────────┤
│ 📊 Cockpit &    │ 🎧 Audio &      │ 🧩 Kassetten &   │ 🗺️ Touren &    │ ⚙️ Hardware &   │
│    Power        │    Ducking      │    DLE           │    WebDAV      │    Reserve     │
└─────────────────┴─────────────────┴──────────────────┴────────────────┴────────────────┘
```

### 2.1 Tab 1: Cockpit & Power (`#tab-cockpit`)

![PWA Tab 1: Cockpit, EKF Schräglage & Heck-Radar HUD](../images/pwa/pwa_tab1_cockpit_radar_hud.png)

* **Fahrdynamik & Schräglage:** Animierte Neigungsanzeige des Motorrads (15-State EKF mit Bosch BMI270), 10 Hz Dead-Reckoning Status.
* **Spannungs- & Thermomanagement:** Live-Anzeige von Bordnetz (KL15), USV-LiPo und Starterbatterie-Entladeschutz.
* **Universal Front-Knoten Card:**
  * Live CarPlay/AA Status (TPS2051B Spannung/Strom).
  * 1-Klick Hard-Reset Button ($2{,}5\,\text{s}$ VBUS Kaltstart).
  * Lenker-PTT Status (< 1.8 ms Latenzanzeige, Test-Button).
  * 4. Metrik-Kachel: Action-Cam BLE Bridge (REC-Toggle, HiLight Marker, Tankpausen-Filter, Pairing-Modal).
  * Live Fahrtwind-Lärmpegel VU-Meter (Knowles MEMS dB(A) & AGC-Boost).
  * **Status-Badge:** Live 2.4 GHz ESP-NOW Funklink (`ESP-NOW LINK (2.4 GHz)` / `OFFLINE`).
  * **4 Subsystem-Kacheln:**
    1. **📱 Wireless CarPlay / AA (Ottocast):** Live-Spannung & Strom (`5.00 V · 380 mA`), Betriebsstatus (`AKTIV`, `REBOOT`, `STANDBY`).
    2. **⚡ Lenker-PTT (Zero-Latency):** Bereitschaftsstatus und Latenzanzeige (`< 1.8 ms Latenz`) mit leuchtender Pulse-Animation bei Tastendruck (1x = Funk, 2x = Cam Toggle, Lang = HiLight Tag).
    3. **🎙️ Cockpit-Lärm (Knowles MEMS):** Live-Schallpegel in $\text{dB(A)}$ und berechnete Lautstärkenachführung (`+0.0 dB` bis `+6.0 dB Boost`).
    4. **🎥 Action-Cam BLE Bridge (GoPro / Insta360 / DJI):** Kamera-Typ (`GoPro Hero 12` / `Insta360 X4`), Akkustand (%), verbleibende SD-Zeit, pulsierender roter REC-Status.
  * **Fahrtwind-Lärm VU-Meter:** Farbkodierter Balken ($35\,\text{dB(A)}$ Standgas bis $115\,\text{dB(A)}$ Höchstgeschwindigkeit).
  * **Interaktive Steuerungen:**
    * **`⚡ CarPlay 1-Klick Kaltstart (2.5s)`:** Löst einen hardwareseitigen Power-Cycle am TI TPS2051B Lastschalter aus (2.5s Spannungsabschaltung mit Countdown-Animation auf dem Button).
    * **`🔘 Lenker-PTT Testen`:** Simuliert den Lenkertaster mit haptischer und optischer Bestätigung.
    * **`🎥 Cam Start/Stopp & HiLight`:** Manuelle Touch-Auslösung und Lesezeichen-Setzung für Action-Cams.
    * **`Tankpausen-Filter (KL15)` Toggle:** Automatischer Aufnahmestopp bei Zündungsaus zur Vermeidung von Leerlauf-Aufnahmen.
    * **`Auto-Café Mode (60s)` Toggle:** Schaltet die automatische VBUS-Abschaltung bei Zündung AUS zur Freigabe des Smartphone-WLANs um.
* **Heck-Radar & Totwinkel-Assistent (BSD HUD Card):**
  * **Status-Badges:** Echtzeit-Gefahrenstufe (`FREI`, `⚠️ FAHRZEUG NÄHERT SICH`, `🚨 KOLLISIONSRISIKO!`) und Hardware-Link (`GARMIN VARIA / 24 GHz M8`).
  * **Virtuelle Spiegel-Warn-LEDs (BSD):** Linker (`#bsd-mirror-left`) und rechter (`#bsd-mirror-right`) Spiegelindikator mit Abstandsdisplay und pulsierender Leuchtanimation (Bernstein / Rot), wenn ein herannahendes Fahrzeug den Totwinkel-Nahbereich ($d < 15\,\text{m}$, Spurversatz) betritt.
  * **Zentraler Heckradar-Sektor (HTML5 Canvas):** $40^\circ$-Fächersektor nach hinten mit Distanzringen ($25\,\text{m}$, $50\,\text{m}$, $100\,\text{m}$, $140\,\text{m}$), animiertem Sweep-Strahl und dynamisch getrackten Fahrzeugblips inklusive Abstands- und $\Delta v$-Tags.
  * **4 Telemetrie-Kacheln:** Nächstes Objekt ($d$), Relativgeschwindigkeit ($\Delta v$), Time-To-Collision ($\text{TTC}$) und Helm-Ducking-Status ($-18\,\text{dB}$ Prio-1).
  * **Interaktive Steuerungen:**
    * **`🚗 Annäherung Simulieren`:** Startet eine 10-sekündige Überholsimulation eines herannahenden Fahrzeugs ($120\,\text{m} \rightarrow 8\,\text{m}$, $+42\,\text{km/h}$) mit automatischer Gefahreneskalation.
    * **`🔔 Warnping Testen`:** Spielt den synthetisierten Prio-1 Doppelton ($880\,\text{Hz} / 1760\,\text{Hz}$) über die Web Audio API im Browser ab.
    * **`Akustischer Helm-Warnping` Toggle:** Erlaubt das vorübergehende Stummschalten der Helmpings.

### 2.2 Tab 2: Audio & Ducking (`#tab-audio`)

![PWA Tab 2: Audio Routing, Ducking & Smart Cartridge Mechatronik](../images/pwa/pwa_tab2_audio_smart_cartridge.png)

* **Betriebsmodus-Wahl:** Umschaltung zwischen Standard Mode (Mesh Bridge), Single Rider Mode und Cruise Mode.
* **Schieberegler:** Eingangspegel Port 1 (Sena), Port 2 (Cardo), Ducking-Dämpfung und Transparenz-Lautstärke.
* **Echtzeit-Pegelbalken:** Live-Pegelüberwachung aller 4 Audio-Eingangskanäle.
* **🦾 Smart Cartridge Mechatronik-Bedienfeld (PCBA 03 Rev 2.0):**
  * Live-Statusanzeige des Kassetten-Controllers (CH32V003 Synced).
  * `⚡ Power Boot`: Löst über Opcode `0x01` den synchronen Tastendruck `Center + (+)` (1000 ms) aus – autom. Kaltstart nach Standzeiten $> 3$ Tage.
  * `🔘 Mesh Ein/Aus`: Opcode `0x05` (200 ms Einzelpuls).
  * `⏭️ Kanal +1 / ⏮️ Kanal -1`: Autonome Kassetten-Makros (`0x07` / `0x08`, 2x Mesh + 1x Plus/Minus).
  * `🔊 Lauter / 🔉 Leiser`: Einzeltasten-Impulse (`0x03` / `0x04`, 100 ms) über unabhängige Aktuatoren `ACT_PLUS` bzw. `ACT_MINUS`.
  * `👥 Group Mesh`: 3000 ms Haltepuls (`0x06`) für nahtloses Umschalten zwischen öffentlichem Open Mesh und privatem Gruppen-Mesh.

### 2.3 Tab 3: Kassetten & DLE (`#tab-cartridges`)

![PWA Tab 3: Kassetten-Erkennung & DLE Live-Status](../images/pwa/pwa_tab3_cartridges_dle_status.png)

* **Live-Status:** Anzeige der eingesteckten Kassetten in Slot 1 und Slot 2 mit 1-Wire UIDs (nativ emuliert oder DS2401).
* **Smart Cartridge Kennzeichnung:** Visualisierung von Hardware-Architektur (RISC-V CH32V003, 4x MOSFETs, In-System Flashing aktiv).
* **Kassetten-Onboarding-Wizard:** Interaktive 3-Schritte-Anleitung beim Einsetzen neuer Headsets.
* **Ground-Truth Sync & ISP-Flashing:** Re-Synchronisation der Konfigurationstabellen direkt in das EEPROM des Kassetten-MCUs über Pin 5 Single-Wire UART.

### 2.4 Tab 4: Touren & WebDAV (`#tab-tours`)

![PWA Tab 4: Touren-Historie, Replay & BGH-konformer GPX-Export](../images/pwa/pwa_tab4_tours_gpx_export.png)

* **Tour-Historie:** Tabellarische Auflistung aller auf der MicroSD gespeicherten GPX-Dateien mit Datum, Distanz und maximaler Schräglage.
* **GPX-Export & Tour-Replay:** Download in 4 spezialisierten Profilen (Moto-Navi Shaping, Video-Sync, Clean Track, Raw EKF) sowie visuelles Abspielen der Tour im Cockpit-Radar.
* **WebDAV-Konfiguration:** Zugangsdaten für automatisches Hochladen zu Nextcloud/Synology.

### 2.5 Tab 5: Geräte- & Verbindungs-Manager (Device Hub • `#tab-hardware`)

![PWA Tab 5: Geräte- & Verbindungs-Manager, Dual-Headset Hub & LoRa Smart-Keyfob](../images/pwa/pwa_tab5_device_hub_keyfob.png)

Der Geräte-Manager ist in zwei klar voneinander getrennte Bereiche strukturiert:

#### Teil 1: Persönliche Geräte (Fahrer & Sozius)
* **Fahrer- & Sozius-Smartphones:** WebBLE Verbindungsstatus, Signalstärke (RSSI), 1-Klick Kaltstart des CarPlay/AA CP2AA-Dongles (TPS2051B VBUS Power-Cycle), Audio-Share Toggle für Sozius.
* **Dual-Headset Hub (Fahrer & Sozius):** Bluetooth Audio Manager für Schuberth/Sena, Cardo DMC und Bluetooth-Headsets (LC3/aptX Codec, Akkustand, Suchlauf).
* **Dual Action-Cam Hub:** Verwaltung von GoPro (Hero 11/12/13), Insta360 (X3/X4/Ace) und DJI Action-Cams mit Auto-REC, Tankpausen-Filter und PTT-HiLight Marker.
* **2-in-1 LoRa Smart-Keyfob (Alarm-Pager & Kassetten-Key):**
  * AES-128 GCM Verschlüsselungs-Status & Monotonic Sequence Nonce.
  * BLE Nahfeld-Präsenzerkennung (Zero-False-Alarm bei legitimer Kassettenentnahme).
  * `[Test-Alarm (LRA)]`: Sendet einen haptischen Test-Alarm an den Pager.
  * `[Pager neu koppeln]`: Neuer kryptografischer Schlüssel-Handshake via Dock/BLE.
  * `[Buddy-Alarm]`: Checkbox zum automatischen Weiterleiten von Diebstahlalarmen ins Gruppen-Mesh.

#### Teil 2: Motorrad & OpenMotorBridge Systemknoten
* **Universal Front-Node (Cockpit-Hub • PCBA 05):** ESP-NOW Funklink, Wi-Fi SoftAP Fallback Toggle, Proximity-Rescue Beacon.
* **Heck-Radar & Spiegel-Totwinkel-LEDs (BSD):** Master-Schalter für Radar-Power und Spiegel-Totwinkel-LEDs (Header `J9` via MOSFET `Q1`) mit 2-Sekunden-Testblitz.
* **Sicherheits-Lichtmanagement:**
  * **ESS Notbremsblinken:** Master-Toggle für 4,5 Hz Stroboskop-Warnblinken (Garmin Varia UART2 & `RESERVE_GPIO_B`), konfigurierbare Verzögerungsschwelle ($-0{,}45\,\text{g}$, $-0{,}60\,\text{g}$, $-0{,}75\,\text{g}$) und Button `[Bremsblitz-Test]`.
  * **Front-Zusatzscheinwerfer (J11 an Front-Node via TPS1H100):** Modi `[AUS]`, `[DAUER-EIN]` und `[AUTO-STROBE BEI ESS]`.
* **Reifendruck-Kontrollsystem (TPMS):** Live-Druck/Temperatur aus BLE GAP Ventilkappen (FOBO / Deelife) & Anlernassistent.
* **Fahrzeug-CAN Profil-Manager & Live Hex Sniffer:** Community-Profil-Auswahl (Harley, BMW, KTM, Ducati, OBD2) und interaktiver Sniffer mit ID-Filterung und CSV-Export.

### 2.6 Smart Docking & Einmalig flankengetriggerter Fahrmodus (User-Override Schutz)

Wird das Fahrer-Smartphone am Cockpit-Dock (Qi `J10`) oder per USB-Kabel am Lenker (`J5`) bzw. im Handschuhfach (`J5_MP3`) eingesteckt, schaltet die WebApp das Dashboard intelligent um:

* **Einmalige Flankentriggerung (Single-Edge Transition):**
  * Der automatische Wechsel auf den Tab `#tab-cockpit` (Fahrmodus) wird **strikt nur auf der steigenden Flanke** des Ladezustands ausgeführt (Übergang von `charging == false` auf `charging == true`).
  * **Schutz vor Rauswerfen bei manueller Bedienung (User Override):**
    * Möchte der Fahrer nach dem Einstecken des Telefons bewusst in den Einstellungen etwas justieren, einen Musiktitel in den Medien wählen oder Sensordiagnosen prüfen, klickt er einfach auf den gewünschten Tab.
    * Die WebApp merkt sich diesen benutzerinitiierten Tab-Wechsel und erzwingt **keinen** Rücksprung, solange das Gerät im Dock verbleibt. Die Zustandsmaschine kämpft niemals gegen den Benutzer!
    * Erst nach einem vollständigen Abnehmen und erneuten Andocken (neue steigende Flanke) oder beim Losfahren (Geschwindigkeit $v > 5\,\text{km/h}$) wird das Cockpit wieder automatisch fokussiert.
* **Konfigurierbarkeit in den App-Einstellungen:**
  * In Tab 5 (Einstellungen) lässt sich die Automatik individuell anpassen:
    `[x] Bei Smartphone-Docking automatisch ins Cockpit wechseln (Standard: Aktiv)`.
* **"Handy vergessen"-Warnlogik (Lenker & Handschuhfach):**
  * Erkennt die Zentralbox beim Abstellen des Motors `KL15 == 0` (Zündung AUS) und meldet der Qi- oder USB-Port weiterhin ein aufliegendes/ladendes Gerät, während die BLE-Signalstärke des Fahrers schwindet ($d > 3\,\text{m}$), schlägt das System Alarm:
  * Zwei kurze Huptöne am Motorrad (*Doppel-Chirp*) und ein hämmerndes LRA-Vibrationsmuster auf dem Smart-Keyfob warnen den Fahrer sofort, bevor er sich vom Motorrad entfernt.

### 2.7 Architektonische Trennung: Echte Hardware (`index.html`) vs. Simulations-Suite (`demo.html`)
* **`index.html` (Produktions-Cockpit):** Reine Instrumentenanzeige für den echten Motorradbetrieb (`window.OMB_MODE = 'hardware'`). Vollständig bereinigt von Simulationsbuttons und Teststrecken; alle Kacheln zeigen im unverbundenen Zustand sauber `Standby` / `--`.
* **`demo.html` (Interaktive Simulations-Suite):** Dedizierte Präsentations- und HIL-Testbench (`window.OMB_MODE = 'demo'`) mit Sticky-Banner, Streckenauswahl (Wil SG $\rightarrow$ Rickenpass, Kerenzerberg), eCall-Crashtest und ausklappbarem **Live-Injektionspanel** (Echtzeit-Schieberegler für Tempo, Schräglage, Heckradar-Distanz, TPMS und Notbremsung).

### 2.8 Kognitive Cockpit-Ruhe & Strikte Anzeigestille während der Fahrt (v > 0)

Ein Smartphone-Display am Motorradlenker (6,1" bis 6,7") hat im Vergleich zu 10,25"-Automotive-Displays eine sehr begrenzte Fläche. Jedes unbedachte Aufploppen eines Banners löst im peripheren Sichtfeld (*Augenwinkel*) einen unwillkürlichen Fixierungsreflex (*Sakkade*) aus. Bei Schräglage im Kurvenscheitelpunkt oder beim Anbremsen führt dies zu gefährlichem Blindflug und Zielfixierung (*Target Fixation*).

* **Zero-Distraction Prinzip während der Fahrt ($v > 0$):**
  * **Absolutes Push-Verbot für Nicht-Sicherheits-Informationen:**
    * Staumeldungen, Straßensperrungen, Wetterradar-Texte und Gruppen-Spritwarnungen werden während der Fahrt **unter keinen Umständen** als Pop-up oder animiertes Banner eingeblendet.
    * Es gibt keine modalen Fenster, die den Tacho, die Schräglage oder das Heck-Radar überlagern.
* **Aufgabenteilung Navigation vs. Cockpit-Telemetrie:**
  * Routenführung, dynamische Stauumfahrung und Sperrungs-Handling gehören exklusiv in die **spezialisierte Navigations-App** (Apple CarPlay / Android Auto via PCBA 05 Front-Knoten, Kurviger, Calimoto oder Garmin).
  * Die Navi-App berechnet Ausweichrouten geräuschlos im Hintergrund und leitet den Fahrer per dezenter Sprachansage im Helm um (*„In 300 Metern rechts abbiegen“*). Der Fahrer muss auf dem Motorrad keine Stauberichte lesen.
* **Informationsausgabe ausschließlich im Stillstand ($v = 0\,\text{km/h}$):**
  * Erst wenn das Motorrad für mindestens **$5\,\text{Sekunden}$ vollständig steht** ($v = 0\,\text{km/h}$ an einer roten Ampel, Schranke oder Rastpause), blendet die PWA auf Wunsch eine ruhige, statische Informationskarte ein (Wetter-Trend, Streckensperrungen der Umgebung).
  * Sobald das Fahrzeug wieder anrollt ($v > 3\,\text{km/h}$), schaltet die Ansicht verzögerungsfrei und lautlos zurück in das minimalistische Primär-Cockpit.

---

## 3. Erweiterter GPX-Export & Navi-Formatierung

Die integrierte Export-Engine transformiert die aufgezeichneten 10-Hz-Rohdaten in 4 spezialisierte Zielformate:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       OMB GPX-EXPORT-ENGINE FORMATE                         │
├───────────────────┬───────────────────────────────┬─────────────────────────┤
│ Format-Profil     │ Zielsysteme                   │ Besonderheiten          │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **1. Moto-Navi**  │ Garmin Zūmo XT/XT2, BMW CRN,  │ • Road-Snapping (OSM)   │
│    **(Shaping)**  │ Kurviger, Calimoto, TomTom    │ • Strategische Wegpunkte│
│                   │                               │ • Garmin `<gpxx:>` Ext  │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **2. Video-Sync** │ Telemetry Overlay, VIRB Edit, │ • 10 Hz 1-PPS Timecode  │
│    **(HiFi EKF)** │ Dashware, Insta360, GoPro     │ • Kurvenschräglage (°)  │
│                   │                               │ • Video Highlight-Marker│
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **3. Clean Track**│ Google Earth, Komoot, Relive, │ • Douglas-Peucker RDP   │
│    **(Visual)**   │ Strava, Apple/Google Maps     │ • Schlanke Dateigröße   │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **4. Raw EKF**    │ Analyse, MATLAB, Telemetrie   │ • Alle IMU & CAN Sensor-│
│    **(Diagnose)** │                               │   Rohdaten ungefiltert  │
└───────────────────┴───────────────────────────────┴─────────────────────────┘
```
