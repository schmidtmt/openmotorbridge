# OpenMotorBridge Google Drive WebDAV Bridge (`omb-gdrive-bridge`)

Ein leichtgewichtiger, selbst gehosteter WebDAV-zu-Google-Drive Proxy für die **OpenMotorBridge** Motorrad-Elektronik. 

Der Service nimmt standardisierte WebDAV-`PUT`-Uploads der Motorrad-Zentralbox (ESP32-S3) entgegen und lädt die aufgezeichneten GPX-Touren und Telemetrie-Dateien automatisch in einen frei wählbaren Ordner auf deinem privaten **Google Drive** (`omb/tracks/`) hoch.

Optional kann nach jedem Upload ein MQTT-Event an dein Smart Home (**Homesphere** / **Home Assistant**) oder ein Webhook mit Fahrtdaten (Distanz, Dauer, max. Schräglage) geschickt werden.

---

## Architektur & Vorteile

```
┌─────────────────────────┐          WebDAV PUT          ┌───────────────────────────┐
│     OPENMOTORBRIDGE     │ ───────────────────────────► │     omb-gdrive-bridge     │
│  (ESP32-S3 Zentralbox)  │    (HTTPS mit Basic Auth)    │ (FastAPI Container <30MB) │
└─────────────────────────┘                              └─────────────┬─────────────┘
                                                                       │
                                                            Google Drive API v3
                                                          (OAuth2 Refresh-Token)
                                                                       │
                                                  ┌────────────────────┴────────────────────┐
                                                  ▼                                         ▼
                                     ┌──────────────────────────┐             ┌───────────────────────────┐
                                     │       GOOGLE DRIVE       │             │   SMART HOME / HOMESPHERE │
                                     │      /omb/tracks/        │             │      (Optionaler MQTT-    │
                                     │   • 2026-09-18_tour.gpx  │             │       Event-Push)         │
                                     └──────────────────────────┘             └───────────────────────────┘
```

* **100 % plattformunabhängig:** Funktioniert für iOS-Fahrer (keine teure Apple-Entwicklergebühr von 99 $/Jahr nötig) und Android-Nutzer gleichermaßen.
* **Autark & ohne Handyzwang:** Sobald das Motorrad in die heimische Garage rollt (oder unterwegs über den Mobilfunk-Proxy), lädt die Box die GPX-Datei direkt hoch.
* **Kein Rclone-Overkill:** Kein 100-MB-Binary und keine fremden Cloud-Dienste – ein winziger Python-Container mit < 30 MB RAM.
* **Zero-Trust & Datensouveränität:** Du hostest den Container selbst (z. B. auf deinem Server `omb.f0o.bar`, einer Synology-DiskStation, einem Raspberry Pi oder Unraid). Deine Daten und Google-Tokens verlassen niemals deine Hand.

---

## Schnellstart in 3 Schritten

### Schritt 1: Google Cloud Console vorbereiten
1. Öffne die [Google Cloud Console](https://console.cloud.google.com/) und wähle dein Projekt aus (oder erstelle ein neues, kostenloses Projekt).
2. Aktiviere die **Google Drive API**:
   * Menü $\rightarrow$ **APIs und Dienste** $\rightarrow$ **Bibliothek** $\rightarrow$ nach *"Google Drive API"* suchen und auf **Aktivieren** klicken.
3. Konfiguriere den **OAuth-Zustimmungsbildschirm** (Typ: *Extern*, Teststatus genügt für eigene Konten; trage deine eigene E-Mail-Adresse als Testnutzer ein).
4. Erstelle Anmeldedaten:
   * **Anmeldedaten erstellen** $\rightarrow$ **OAuth-Client-ID**.
   * Anwendungstyp: **Webanwendung** oder **Desktop-App**.
   * Autorisierte Weiterleitungs-URIs: `http://localhost:8085` hinzufügen.
   * Notiere dir deine **Client-ID** und dein **Client-Secret**.

---

### Schritt 2: Refresh-Token mit dem Ein-Schritt-Helfer erzeugen
Führe auf deinem Rechner das interaktive Setup-Skript aus:

```bash
cd apps/gdrive_webdav_bridge
pip install -r requirements.txt
python auth_helper.py
```

* Das Skript öffnet deinen Browser.
* Logge dich mit deinem Google-Konto ein und bestätige den Zugriff.
* Das Skript fängt den Code auf `http://localhost:8085` ab und gibt dir dein fertiges `GOOGLE_REFRESH_TOKEN` aus.

Erstelle nun deine `.env`-Datei:
```bash
cp .env.example .env
nano .env
```

Trage deine Daten ein:
```env
WEBDAV_USER=omb
WEBDAV_PASSWORD=DeinGeheimesMotorradPasswort123

GOOGLE_CLIENT_ID=113806676655-xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxx
GOOGLE_REFRESH_TOKEN=1//0gxxxx
GOOGLE_DRIVE_FOLDER=omb/tracks
```

---

### Schritt 3: Container starten (Podman oder Docker)

#### Mit Podman Compose:
```bash
podman-compose up -d
```

#### Mit Docker Compose:
```bash
docker compose up -d
```

Der Dienst läuft nun auf Port `8080` (oder hinter deinem Reverse-Proxy wie Nginx/Traefik auf `https://omb.f0o.bar`).

---

## Konfiguration in der OpenMotorBridge PWA

Öffne die OpenMotorBridge Weboberfläche auf deinem Motorrad (oder Smartphone):
1. Gehe zu **Tab 4: Touren & WebDAV** (`#tab-tours`).
2. Trage deine WebDAV-Verbindungsdaten ein:
   * **WebDAV Server URL:** `https://omb.f0o.bar/tracks/` (oder `http://192.168.1.50:8080/tracks/`)
   * **Benutzername:** `omb` (bzw. dein `WEBDAV_USER`)
   * **Passwort / Token:** Dein `WEBDAV_PASSWORD`
3. Klicke auf **Verbindung testen**. Fertig!

Sobald die Zündung ausgeschaltet wird, synchronisiert die Zentralbox alle neuen GPX-Dateien automatisch in dein Google Drive unter `/omb/tracks/`.

---

## Optionaler Event-Push (Homesphere / Home Assistant)

Wenn du `MQTT_ENABLED=true` oder `MQTT_BROKER` in der `.env` setzt, sendet der Service nach jedem erfolgreichen Upload ein JSON-Event an deinen MQTT-Broker:

```env
MQTT_ENABLED=true
MQTT_BROKER=192.168.1.50
MQTT_PORT=1883
MQTT_TOPIC=homesphere/omb/track_uploaded
```

### MQTT Payload Beispiel:
```json
{
  "event": "track_uploaded",
  "filename": "2026-09-18_alpentour.gpx",
  "size_bytes": 452100,
  "uploaded_at": "2026-09-18T14:35:10Z",
  "gdrive_file_id": "1A2B3C4D5E6F7G8H",
  "gdrive_link": "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H/view",
  "stats": {
    "point_count": 1420,
    "distance_km": 164.25,
    "duration_s": 9320,
    "max_lean_deg": 42.8,
    "start_time": "2026-09-18T10:15:00Z",
    "end_time": "2026-09-18T12:50:20Z"
  }
}
```

In Home Assistant kannst du daraufhin eine Benachrichtigung auf deinem Smartphone oder der Apple Watch / WearOS auslösen:
> *„Motorradtour beendet! 164,2 km gefahren, max. Schräglage 42,8°. Track liegt auf Google Drive bereit.“*

---

## Tests ausführen

```bash
cd apps/gdrive_webdav_bridge
pytest test_bridge.py -v
```
