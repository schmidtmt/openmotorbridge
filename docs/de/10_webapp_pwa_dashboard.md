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
* **Betriebsmodus-Wahl:** Umschaltung zwischen Standard Mode (Mesh Bridge), Single Rider Mode und Cruise Mode.
* **Schieberegler:** Eingangspegel Port 1 (Sena), Port 2 (Cardo), Ducking-Dämpfung und Transparenz-Lautstärke.
* **Echtzeit-Pegelbalken:** Live-Pegelüberwachung aller 4 Audio-Eingangskanäle.

### 2.3 Tab 3: Kassetten & DLE (`#tab-cartridges`)
* **Live-Status:** Anzeige der eingesteckten Kassetten in Slot 1 und Slot 2 mit 1-Wire UIDs.
* **Kassetten-Onboarding-Wizard:** Interaktive 3-Schritte-Anleitung beim Einsetzen neuer Headsets.
* **Ground-Truth Sync:** Button zur Synchronisation des LittleFS-Mappings.

### 2.4 Tab 4: Touren & WebDAV (`#tab-tours`)
* **Tour-Historie:** Tabellarische Auflistung aller auf der MicroSD gespeicherten GPX-Dateien mit Datum, Distanz und maximaler Schräglage.
* **GPX-Export & Tour-Replay:** Download in 4 spezialisierten Profilen (Moto-Navi Shaping, Video-Sync, Clean Track, Raw EKF) sowie visuelles Abspielen der Tour im Cockpit-Radar.
* **WebDAV-Konfiguration:** Zugangsdaten für automatisches Hochladen zu Nextcloud/Synology.

### 2.5 Tab 5: Hardware & Reserve (`#tab-hardware`)
* **Front-Knoten Diagnostik:** Übersicht der Spezifikationen (ESP32-C3, LMR36015, USB2512B, TPS2051B, Knowles MEMS) und Button zur Prüfung von OTA-Firmware-Updates.
* **Reserve I/O:** Status und Toggle-Schalter für HD26 Pin 25 (`RESERVE_GPIO_A`) und Pin 26 (`RESERVE_GPIO_B`).
* **Zentralbox Soft-Reboot:** Gesteuerter Warmstart des Hauptsystems.

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
