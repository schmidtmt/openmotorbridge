# OpenMotorBridge Companion App (`bar.f0o.omb`)

Offizielle plattformübergreifende Begleit-App für das OpenMotorBridge Motorrad-Ökosystem, entwickelt mit **Flutter (Dart)** und nativen **Android-Plattform-Services (Kotlin)**.

---

## 🚀 Kernfunktionen

### 1. In-App OTA Self-Updater (Homesphere-Prinzip)
* **Keine Wartezeiten im Google Play Store:** Aktualisiert sich direkt in der App.
* **Flexible Update-Quellen:**
  * **Lokaler Homeserver:** URL zu `version.json` oder direktem APK-Link (z. B. `http://192.168.1.100:8080/omb-update.apk`).
  * **GitHub Releases:** Automatischer Abruf des neuesten APKs aus den Releases von `schmidtmt/openmotorbridge`.
* **Download-Fortschritt & 1-Klick Installation:** Lädt die APK in den App-Cache und startet über Androids `FileProvider` (`ACTION_VIEW`) den nativen Installationsdialog.

### 2. Layer-5 SOCKS5 & HTTP Mobilfunk-Proxy (`TRANSPORT_CELLULAR`)
* **Zero Wi-Fi Konflikt:** Bypasst das 5 GHz WLAN des Smartphones, das exklusiv durch Wireless CarPlay / Android Auto belegt ist.
* **Zero VPN Konflikt:** Läuft rein im User-Space als L5-Stream-Relay auf `127.0.0.1:8080` und belegt **keinen** Android `VpnService`-Slot. Dauerhaft aktive VPNs wie **Tailscale** oder WireGuard (für Home Assistant / Homesphere) bleiben 100 % ungestört parallel aktiv!
* **Automatisches Mobilfunk-Binding:** Nutzt Androids `ConnectivityManager.requestNetwork()` mit `TRANSPORT_CELLULAR`, um alle ausgehenden Proxy-Sockets fest an 4G/5G zu binden.

### 3. Cross-Platform BLE-Brücke (Native CoreBluetooth auf iOS)
* Basiert auf `flutter_blue_plus` und spricht auf iOS direkt mit Apples nativem `CoreBluetooth` C-Stack (keine WebBLE-/Bluefy-Einschränkungen!).
* Automatischer Reconnect zum ESP32-S3 (`OMB-CENTRAL-*`).
* Live-Telemetrie im Glassmorphism Dashboard: Bordnetzspannung, IMU-Schräglage, Zündungsstatus (KL15) und 77-GHz-Heckradar-Warnungen.

### 4. u-blox AssistNow Online A-GPS Injection
* Lädt beim Start der Zündung ein kompaktes MGA-Ephemeridenpaket (~3–8 kB) über die Mobilfunkverbindung herunter.
* Speist die Binärframes via BLE in den SAM-M10Q GNSS-Chip auf Front-Node PCBA 05 ein.
* **Ergebnis:** Kaltstart-TTFF sinkt von ~30 s auf unter **1.5 Sekunden** (Instant-3D-Fix)!

---

## 🛠️ Entwicklung & Build

### App lokal starten
```bash
cd apps/omb_companion
flutter run
```

### Release APK für den lokalen Server bauen
```bash
flutter build apk --release
# Die fertige APK liegt unter:
# build/app/outputs/flutter-apk/app-release.apk
```

### Eigene Update-Konfiguration (`version.json` auf deinem lokalen Server)
```json
{
  "version": "1.0.1",
  "url": "http://192.168.1.100:8080/app-release.apk",
  "notes": "Neu: Optimierte SOCKS5-Verbindungsüberwachung und Radar-Alarmfilter."
}
```
In der App unter **Self-Update** einfach `http://192.168.1.100:8080/version.json` eintragen – die App erkennt neue Versionen sofort und installiert sie per Fingertipp!
