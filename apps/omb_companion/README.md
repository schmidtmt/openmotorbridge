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

### 5. Nativer Smart Firmware & Node-OTA Hub
* **Keine WebBLE-Abbrüche:** Im Gegensatz zur PWA kein Verbindungsabriss bei gesperrtem Bildschirm oder Ruhezustand (Foreground-Service mit WakeLock).
* **Multi-Node Unterstützung:**
  * **Central Controller (ESP32-S3):** `openmotorbridge_central.bin`
  * **OMM UCS Intercom (PCBA 09 / ESP32-C3):** High-Speed UART Push (460.800 Baud SLIP)
  * **Front-Node Cockpit (PCBA 05):** ESP-NOW & Ottocast Flasher
  * **Radar Sub-MCU (PCBA 02):** 77 GHz Transceiver-Coprozessor
* **Offline-Caching für die Garage:** Binärdateien können vorab im heimischen WLAN auf das Smartphone geladen werden – das Motorrad kann draußen in der Tiefgarage völlig offline geflasht werden.
* **Eigene Test-Firmware:** Beliebige `.bin`-Dateien können direkt über den nativen Dateimanager ausgewählt und geflasht werden.
* **Live-Diagnoselog:** Scrollbare Terminalkonsole mit detailliertem Übertragungsprotokoll und Fehlerüberwachung.

---

## 🛠️ Entwicklung & Build

### App lokal starten
```bash
cd apps/omb_companion
flutter run
```

### Automatisiertes Build- & Deployment-Skript (Homesphere-Pattern)

Vor jedem Build wird automatisch die Versionsnummer und der Build-Code in `pubspec.yaml` erhöht, das Release-APK gebaut, die Metadaten (`version.json`, `apps.json`) generiert und auf alle konfigurierten Ziele (lokales Staging, Google Drive, Homeserver/Pi) verteilt:

```bash
# Aus dem Repository-Root:
./tools/build_and_deploy_companion.sh

# Oder aus apps/omb_companion/:
./scripts/build_and_deploy.sh
```

#### Nützliche CLI-Optionen:
* `--no-bump` – Behält die aktuelle Version bei ohne sie zu erhöhen.
* `--patch` – Erhöht explizit den SemVer-Patch (z. B. `1.0.1` ➔ `1.0.2`).
* `--minor` – Erhöht die Minor-Version (z. B. `1.0.x` ➔ `1.1.0`).
* `--major` – Erhöht die Major-Version (z. B. `1.x.x` ➔ `2.0.0`).
* `--ios` – Kompiliert zusätzlich auf macOS die iOS-App und schnürt eine unsignierte IPA für SideStore / AltStore.
* `--remote` – Erzwingt den SCP-Upload auf den lokalen Server / Raspberry Pi (`homesphere.f0o.bar`).
* `--tag` – Erstellt automatisch ein signiertes Git-Release-Tag `vX.Y.Z-B` und pusht es zu GitHub.

#### Bereitstellungs-Ziele (Automatisch erkannt):
1. **Lokales Staging (`apps/omb_companion/dist/`):**
   * `openmotorbridge-release.apk` & `openmotorbridge-X.Y.Z-B.apk`
   * `version.json` (für In-App OTA Self-Update)
   * `apps.json` (für SideStore / AltStore)
   * `logo.jpg`
2. **Google Drive Sync:**
   * Wird automatisch in `/Meine Ablage/OpenMotorBridge/app/` abgelegt, sofern Google Drive auf dem Mac eingebunden ist.
3. **Lokaler Homeserver / Raspberry Pi:**
   * Übertragung per `scp` auf `homesphere.f0o.bar` nach `/home/schmidtm/homesphere/api-service/data/static/` für sofortige Verfügbarkeit im lokalen Netzwerk.

### Eigene Update-Konfiguration (`version.json` auf deinem lokalen Server)
```json
{
  "version": "1.0.1",
  "url": "http://192.168.1.100:8080/app-release.apk",
  "notes": "Neu: Optimierte SOCKS5-Verbindungsüberwachung und Radar-Alarmfilter."
}
```
In der App unter **Self-Update** einfach `http://192.168.1.100:8080/version.json` eintragen – die App erkennt neue Versionen sofort und installiert sie per Fingertipp!
