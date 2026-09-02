# 10 - Web Bluetooth Dashboard & PWA Frontend

Dieses Dokument spezifiziert die Architektur des autarken Progressive Web App (PWA) Dashboards, die Web Bluetooth (WebBLE) Kommunikation, den lokalen **IndexedDB Offline-Speicher** sowie die **Export-Engine fuer erweiterte GPX-Formate** (Navi Shaping Points & Video Telemetrie).

---

## 1. Architektur & Offline-Faehigkeit
Das Dashboard ist eine vollstaendig autarke Progressive Web App (PWA) basierend auf standardisiertem HTML5, CSS3 und ES6 JavaScript. Die App kommuniziert ueber die Web Bluetooth API (WebBLE) direkt mit dem ESP32-S3 der Zentralbox – ohne Cloud-Zwang oder externe Serverabhaengigkeiten.
- **Lokaler Offline-Speicher (IndexedDB):** GPX-Touren koennen ueber BLE direkt von der MicroSD-Karte heruntergeladen und in der lokalen `omb_tours_db` des Browsers persistent gesichert werden.
- **Service Worker Caching:** Die gesamte WebApp laeuft offlinefaehig im Browser (Cache-First Strategie fuer PWA Installation auf iOS und Android).

### 1.1 Plattform- & Browser-Kompatibilität (Web Bluetooth)

Die W3C Web-Bluetooth-API wird je nach Betriebssystem unterschiedlich unterstützt:

| Plattform | Empfohlener Browser | Verbindungsmethode & Besonderheiten |
| :--- | :--- | :--- |
| **Android / PC / Mac / Linux** | **Google Chrome, MS Edge, Opera** | **Nativ:** Direkte Unterstützung der Web Bluetooth API. Voraussetzung: Sicherer Kontext (`https://` oder `http://localhost`). |
| **Apple iOS / iPadOS** (iPhone, iPad) | **[Bluefy – Web BLE Browser](https://apps.apple.com/app/bluefy-web-ble-browser/id1492822055)** (kostenlos im App Store) | **Erforderlich:** Apple blockiert in WebKit/Safari (und damit auch in iOS-Chrome/Edge) den Zugriff auf Web Bluetooth. *Bluefy* stellt eine standardkonforme Brücke über Apples natives *CoreBluetooth* bereit. |
| **Desktop Safari / Firefox** | Nicht unterstützt | Desktop-Safari und Mozilla Firefox unterstützen Web Bluetooth herstellerseitig nicht. |

---

## 2. Telemetrie & Steuerungsfunktionen
- **Echtzeit-Telemetrie:** Ueberwachung der Bordnetzspannung (KL15/KL30), USV-Akkuspannung (BQ24075) und CR2032-Batteriestatus des BLE-Lenkertasters (Service 0x180F).
- **Audio-Matrix-Steuerung:** Interaktiver Umschalter fuer Betriebsmodi (Standard, Single Rider, Cruise Mode) sowie Schieberegler fuer Ducking-Schwellwerte und Gain.
- **Kassetten- & Profilmanager:** Erkennung der via 1-Wire gesteckten Module, Anzeige der aktiven Hardwareprofile und Ground-Truth-Kanalwahl mit Re-Sync-Trigger (`🔄 Sync`). Bei Headset-Upgrades (z. B. Sena 60S statt 20S in bestehender Kassette) verknüpft die WebApp die neue Auswahl sofort persistent mit der 1-Wire DS2401 Chip-UID, sodass künftig nach jedem Aus- und Einstecken automatisch das neue Profil geladen wird.
- **Kassetten-Onboarding-Wizard:** Schritt-fuer-Schritt-Anleitung bei Neu-Kopplung (Bluetooth Classic am Intercom deaktivieren, Pairings loeschen, reinen Mesh-Betrieb erzwingen).
- **WS2812B RGB Status-LED Widget:** Live-Spiegelung des optischen Gehaeusestatus im Dashboard.

---

## 3. Erweiterter GPX-Export & Navi-Formatierung

Die integrierte GPX-Export-Engine transformiert die aufgezeichneten 10-Hz-Rohdaten in 4 spezialisierte Zielformate:

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

1. **Garmin / BMW Shaping Points (`<rtept>` & `<gpxx:RoutePointExtension>`):**
   * Verhindert eigenmaechtiges Neuberechnen der Navis durch Einbetten von nicht-ansagenden Zwischenzielen entlang der Passstrassen und Kurven.
2. **Actioncam Timecode-Sync (`<omb:action_event>`):**
   * Betten Lenkertaster-Klicks als framegenaue Schnittmarken ein.

---

## 4. Smart Firmware & OEM Adapter Update-Hub

Das Dashboard integriert eine zentrale Steuerungszentrale für alle Firmware- und Kassetten-Aktualisierungen:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 SMART FIRMWARE & OEM ADAPTER UPDATE-HUB                     │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 📡 OMM Heck-Pod 3 In-System Flasher  │ 🎴 Sena / Cardo Mesh 3.0 Assistent   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • 1-Klick High-Speed UART Push       │ • 1. Auto-Pairing Puls (TLP222A 5s)  │
│ • 460.800 Baud SLIP Loader           │ • 2. Deep-Link zu offizieller App    │
│ • Automatische MD5 Checksummen-Prüf. │ • 3. JSON Profil-Merge & Gain-Sync   │
│ • Kein Zerlegen des Motorrads        │ • Kein manuelles Tastengefummel      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

1. **OMM In-System Firmware Push:**
   * Streamt `omm_rear.bin` über das 6-Pin UART-Interface direkt auf den ESP32-C3 Co-Prozessor des Heck-Pods mit animierter Fortschrittsanzeige ($< 6\,\text{s}$).
2. **Sena & Cardo Smart Adapter Assistant:**
   * **Schritt 1:** Triggert über den TLP222A Optokoppler der Kassette den 5-Sekunden-Puls für den Bluetooth-Pairing-Modus.
   * **Schritt 2:** Öffnet per Deep-Link die offizielle Sena- oder Cardo-Smartphone-App zum drahtlosen Einspielen des Hersteller-Updates.
   * **Schritt 3:** Führt nach Abschluss das aktualisierte LittleFS JSON-Profil (z.B. `sena_apex_v3.json`) mit den individuellen DSP- und Ducking-Einstellungen zusammen.

