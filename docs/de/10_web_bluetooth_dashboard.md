# 10 - Web Bluetooth Dashboard & PWA Frontend

Dieses Dokument spezifiziert die Architektur des autarken Progressive Web App (PWA) Dashboards, die Web Bluetooth (WebBLE) Kommunikation, den lokalen **IndexedDB Offline-Speicher** sowie die **Export-Engine fuer erweiterte GPX-Formate** (Navi Shaping Points & Video Telemetrie).

---

## 1. Architektur & Offline-Faehigkeit
Das Dashboard ist eine vollstaendig autarke Progressive Web App (PWA) basierend auf standardisiertem HTML5, CSS3 und ES6 JavaScript. Die App kommuniziert ueber die Web Bluetooth API (WebBLE) direkt mit dem ESP32-S3 der Zentralbox – ohne Cloud-Zwang oder externe Serverabhaengigkeiten.
- **Lokaler Offline-Speicher (IndexedDB):** GPX-Touren koennen ueber BLE direkt von der MicroSD-Karte heruntergeladen und in der lokalen `omb_tours_db` des Browsers persistent gesichert werden.
- **Service Worker Caching:** Die gesamte WebApp laeuft offlinefaehig im Browser (Cache-First Strategie fuer PWA Installation auf iOS und Android).

---

## 2. Telemetrie & Steuerungsfunktionen
- **Echtzeit-Telemetrie:** Ueberwachung der Bordnetzspannung (KL15/KL30), USV-Akkuspannung (BQ24075) und CR2032-Batteriestatus des BLE-Lenkertasters (Service 0x180F).
- **Audio-Matrix-Steuerung:** Interaktiver Umschalter fuer Betriebsmodi (Standard, Single Rider, Cruise Mode) sowie Schieberegler fuer Ducking-Schwellwerte und Gain.
- **Kassetten- & Profilmanager:** Erkennung der via 1-Wire gesteckten Module, Anzeige der aktiven Hardwareprofile und Ground-Truth-Kanalwahl mit Re-Sync-Trigger.
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
