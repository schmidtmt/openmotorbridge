# 10 - Web Bluetooth Dashboard & PWA Frontend

## 1. Architektur & Offline-Faehigkeit
Das Dashboard ist eine vollstaendig autarke Progressive Web App (PWA) basierend auf standardisiertem HTML5, CSS3 und ES6 JavaScript. Die App kommuniziert ueber die Web Bluetooth API (WebBLE) direkt mit dem ESP32-S3 der Zentralbox - ohne Cloud-Zwang oder externe Serverabhaengigkeiten.
- **Lokaler Offline-Speicher:** GPX-Touren koennen ueber BLE direkt heruntergeladen und in der lokalen IndexedDB des Browsers gesichert werden.

## 2. Telemetrie & Steuerungsfunktionen
- **Echtzeit-Telemetrie:** Ueberwachung der Bordnetzspannung (KL15/KL30), USV-Akkuspannung (BQ24075) und CR2032-Batteriestatus des BLE-Lenkertasters (Service 0x180F).
- **Audio-Matrix-Steuerung:** Interaktiver Umschalter fuer Betriebsmodi (Standard, Single Rider, Cruise Mode) sowie Schieberegler fuer Ducking-Schwellwerte und Gain.
- **Kassetten- & Profilmanager:** Erkennung der via 1-Wire gesteckten Module, Anzeige der aktiven Hardwareprofile und Ground-Truth-Kanalwahl mit Re-Sync-Trigger.
- **Kassetten-Onboarding-Wizard:** Schritt-fuer-Schritt-Anleitung bei Neu-Kopplung (Bluetooth Classic am Intercom deaktivieren, Pairings loeschen, reinen Mesh-Betrieb erzwingen).
