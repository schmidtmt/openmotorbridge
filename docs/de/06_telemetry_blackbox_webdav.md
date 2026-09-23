# 06 - Telemetrie-Blackbox, SDIO-Ringpuffer & WebDAV-Sync

Dieses Dokument spezifiziert das Telemetrie- und Speicher-Subsystem der OpenMotorBridge v8.0: die 4-Bit High-Speed SDIO-Schnittstelle, den DSGVO- und BGH-konformen Ringspeicher mit kryptographischer Signierung, den automatischen TLS-gesicherten WebDAV-Cloud-Upload sowie den sparsamen **USB Mass Storage Class (MSC) Modus** für den werkzeuglosen Datenaustausch am Rechner.

---

## 1. Speicheranbindung & High-Speed SDIO (4-Bit @ 40 MHz)

* **Schnittstelle:** Nativer 4-Bit SDIO-Bus @ 40 MHz direkt angebunden an den ESP32-S3 (GPIOs 40–45).
* **Durchsatz:** Kontinuierliche Schreibrate $> 12\,\text{MB/s}$ (unterbrechungsfreies 10 Hz GPX-, IMU-, Schräglagen- und Audio-Telemetrie-Logging).
* **Dateisystem:** FAT32 mit dynamischer Sektor-Pufferung (Clustergröße 32 kB).
* **Ausfallsicherheit:** Der integrierte BQ24075 USV-Puffer garantiert selbst bei plötzlichem Bordnetzabriss das saubere Schließen der FAT-Dateitabellen ohne Datenkorruption.

---

## 2. Sensor-Fusion & Automotive Dead Reckoning (ADR Engine)

Das Telemetrie-Subsystem führt Daten des Multi-GNSS-Empfängers (**u-blox MAX-M10S** im Heck-Pod 3), der 6-Achsen-IMU (**Bosch BMI270**) und optionaler Raddrehzahlen (über fahrzeugseitigen CAN-Bus oder ABS-Sensorpulse) in einem **15-State Error-State Extended Kalman Filter (ES-EKF)** zusammen:

```
[ u-blox Multi-GNSS (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Raddrehzahl / Speed ] ────(10-20 Hz)───────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ─(50-100 Hz)─────┘        (Dead Reckoning Engine)            (Mit Schräglage & G-Force)
```

### 2.1 Lückenlose Tunnel-Navigation (Inertial Navigation)
Bricht der GNSS-Empfang in Tunneln, Unterführungen, dichten Waldgebieten oder engen Schluchten ab:
* Die Raddrehzahl liefert die präzise Wegstrecke ($\Delta s = v \cdot \Delta t$).
* Das Gyroskop der BMI270 IMU integriert Kurven, Richtungs- und Höhenänderungen kontinuierlich weiter.
* Der Track läuft im Tunnel ohne Einfrieren, Sprünge oder Zick-Zack-Muster nahtlos auf der Fahrbahnlinie weiter.

### 2.2 Kompensation von Multipath-Sprüngen (Felswand-Filterung bei Alpenpässen)
GNSS-Messausreißer (z. B. $40\,\text{m}$-Positionssprünge durch Signalreflexionen an steilen Felswänden in Pässen) werden vom Kalman-Filter automatisch verworfen: Die IMU meldet dem EKF, dass physikalisch keine entsprechende Querbeschleunigung stattgefunden hat, wodurch der Track auf der realen Fahrbahnlinie gehalten wird.

---

## 3. MotoGP-Style Telemetrie & GPX 2.0 XML-Spezifikation

Jeder Wegpunkt im GPX-Datensatz wird mit $10\,\text{Hz}$ um hochpräzise Fahrdynamik-Metadaten erweitert:
* **Kurvenschräglage links/rechts (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$ (separat erfasst für Links- und Rechtskurven).
* **Längs- und Querbeschleunigung (Brems- und Beschleunigungs-G-Kräfte):** Aus kalibrierten IMU-Werten ($+g$ Beschleunigung, $-g$ Bremsverzögerung).
* **Umgebungstemperatur (°C):** Hochpräzise Außentemperaturmessung über die 2-Stufen-Architektur.
* **Motordrehzahl (U/min):** Bei CAN-Bus Anbindung ausgelesene Motordrehzahl mit $10\,\text{Hz}$.
* **Bordnetz- und Batteriespannung:** Zur Diagnose von Lichtmaschine und Regler.
* **1-PPS Hardware-Zeitsynchronisation:** Mit $< 15\,\text{ns}$ Jitter für framegenaue Actioncam-Videomarker.
* **CAN-Gangstufe (`<omb:gear>`):** Eingelegter Gang (0 = Neutral, 1..6) aus CAN-Telemetrie zur Auswertung von Schaltvorgängen.
* **Funkverbindungs-QoS (`<omb:comm_tier>`):** Aktive Funkebene (`hd` = 2.4 GHz Opus HD-Voice, `lora` = 868 MHz Codec2 Fallback).

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:accel_g_lat>0.98</omb:accel_g_lat>
      <omb:temp>21.4</omb:temp>
      <omb:rpm>4850</omb:rpm>
      <omb:gear>4</omb:gear>
      <omb:comm_tier>hd</omb:comm_tier>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
      <omb:hdop>0.8</omb:hdop>
    </omb:telemetry>
  </extensions>
</trkpt>
```

### 3.1 2-Stufen-Architektur für Außentemperatur-Sensorik

Um Leitungen durch den Lenkkopf zum kabellosen Frontnode strikt zu vermeiden und Fehlmessungen durch Motorwärme auszuschließen, nutzt OpenMotorBridge ein 2-Stufen-Konzept:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             2-STUFEN ARCHITEKTUR FÜR UMGEBUNGSTEMPERATUR                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ STUFE 1: CAN-Bus Broadcast (BMW R1250/R1300 GS, Harley Pan America / HD-LAN) │
│ • Nutzt OEM-Ansaugluft-/Außentemperatursensor des Motorrads (CAN-ID 0x2D0)   │
│ • 0 zusätzliche Kabel, 0 Bauteilekosten, 100 % werkskalibriert               │
├─────────────────────────────────────────────────────────────────────────────┤
│ STUFE 2: Heck-Pod 3 Antennenfuß-Sensorik (Universal / CVO ST / Non-CAN)     │
│ • Sensorik (DS18B20 1-Wire oder TI TMP117 / SHT40 I2C an J6) an PCBA 04 (ESP32-C3) │
│ • Montage: Im Antennensockel / Fahrtwindkanal der Telemetrieflosse           │
│   (cvo_st_telemetry_fin.stl) direkt an der externen 2.4 GHz Antenne          │
│ • Thermische Entkopplung: Verhindert Fehlmessungen durch Motorstauwärme      │
│   unter der Solositz-Hutze (45–55 °C)                                        │
│ • Kabelfrei am Lenkkopf: Das 100 % kabellose Frontnode-Prinzip bleibt gewahrt│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Barometrische Höhenkalibrierung (Kalman-Fusion)

Neben GNSS-Höhenmessungen erfasst der Bosch BMP390 / BMP581 Luftdrucksensor am Heck-Pod barometrische Höhendifferenzen auf $\pm 10\,\text{cm}$ genau. Ein kontinuierlicher Abgleich im 15-State Extended Kalman Filter gegen die u-blox MAX-M10S 3D-Fix-Koordinaten bei stabiler Fahrt kalibriert den QNH-Referenzdruck vollautomatisch – ganz ohne manuelle Höhen-Nullung durch den Fahrer.

### 3.3 Schaltvorgang-Zähler (Shift Counter) & Funk-QoS-Tracking

1. **Shift Counter State-Machine:**
   * Aus den CAN-Tags `<omb:gear>` ermittelt der Bridge-Parser Gangwechsel mit Unterscheidung in Hoch- (`shifts_up`) und Runterschalten (`shifts_down`).
   * Zur Vermeidung von Doppelzählungen bei schnellen Schaltfolgen filtert ein Hysterese-Entpreller temporäre Neutral-Zwischenschritte (`1 -> N -> 2` zählt als 1 Hochschaltvorgang).
   * Die Kennzahl `shifts_per_km` liefert einen objektiven Indikator für kurvenreiches Schalten vs. entspanntes Gleiten im höchsten Gang.

2. **Funk-QoS & LoRa-Fallback-Protokollierung:**
   * Das Intercom-Subsystem loggt jede Umschaltung von 2.4 GHz Opus HD-Voice auf 868 MHz Codec2 LoRa (`<omb:comm_tier>lora</omb:comm_tier>`).
   * Erfasst werden Verfügbarkeit in Prozent (`comm_hd_pct`), Anzahl der Rückfall-Ereignisse (`comm_lora_fallback_count`) sowie die Gesamtdauer im LoRa-Modus (`comm_lora_fallback_duration_s`).

### 3.4 Direkte Kopplung an Betriebsmodi (Zero-Overkill Scorecards)

Statt unübersichtlicher Einstellungsmenüs koppelt OpenMotorBridge die Telemetrie-Auswertung direkt an die drei existierenden Modi aus `🎛️ Audio-Routing & Betriebsmodi`:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 TELEMETRIE-SCORECARDS NACH BETRIEBSMODUS                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ MODUS 1: Single Rider Mode 🏍️ (Sportlich & Fahrdynamik)                     │
│ • Schräglagen L/R, Kurvendichte (Kurven/km), Zeitanteil in Schräglage (%)    │
│ • Shift Counter (Gesamt, Up/Down, Shifts/km), G-Forces, Notbremsungen, RPM  │
├─────────────────────────────────────────────────────────────────────────────┤
│ MODUS 0: Standard Mesh Bridge 👥 (Gruppe & Intercom-Verfügbarkeit)          │
│ • Funk-Verfügbarkeit (% HD-Voice), LoRa-Fallbacks, Cluster-Zustellung        │
│ • Kolonnen-Tempo (Ø km/h), Gesamtkurven, Bordnetz-Stabilität                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ MODUS 2: Cruise Mode 🛣️ (Cruising & Tour-Komfort)                           │
│ • Netto-/Pausenzeiten, Höhenprofil & Höhenmeter, Außentemperatur-Spanne     │
│ • Bremsruhe (Sanfte Bremsungen), Reisetempo, Schaltkomfort-Index            │
└─────────────────────────────────────────────────────────────────────────────┘
```

In der WebApp PWA ermöglicht der Tour Inspector über drei Pills (`[ 🏍️ Sportlich ]`, `[ 👥 Gruppe / Funk ]`, `[ 🛣️ Cruising ]`) jederzeit den sofortigen Wechsel der Scorecard-Perspektive.

### 3.5 GPS-Koexistenz & HF-Entstörung bei LoRa-Sendeimpulsen (+22 dBm)

Bei +22 dBm (160 mW) LoRa-Sendeleistung auf 868 MHz besteht theoretisch das Risiko einer Übersteuerung (De-Sensing) des hochempfindlichen GNSS-Eingangsverstärkers (LNA des u-blox MAX-M10S bei 1575,42 MHz). OpenMotorBridge verhindert Störungen durch ein 3-fach Schutzkonzept:
1. **SAW-Bandpass-Vorfilter:** Ein steilflankiger Oberflächenwellen-Filter (SAW) vor dem LNA dämpft 868 MHz um $> 55\,\text{dB}$.
2. **Geometrische Antennen-Isolation:** Die LoRa-Antenne sitzt im Heck-Pod vertikal polarisiert und orthogonal versetzt zur horizontalen GNSS-Keramik-Patchantenne in der CVO-ST-Finne.
3. **Inertiale EKF-Stützung:** Bei kurzzeitigen HF-Bursts überbrückt das 15-State Kalman-Filter eventuelle SNR-Dips nahtlos über die IMU-Koppelnavigation.

---

## 4. Track-Lifecycle & Intelligente Segmentierung

* **Auto-Start:** Startet eine neue Tour-Datei (`YYYY-MM-DD_HH-MM-SS.gpx`), sobald die Zündung (KL15) aktiv ist und sich das Motorrad länger als 10 Sekunden mit $> 5\,\text{km/h}$ bewegt.
* **Segment-Split (`<trkseg>`):** Bei Ampel- oder kurzen Tankstopps unter 15 Minuten wird die Datei nicht geschlossen, sondern ein neues Track-Segment geöffnet, um Routen-Artefakte im Stand zu eliminieren.
* **Auto-Finalisierung:** Nach 15 Minuten Dauerstillstand oder 60 Sekunden nach Zündung AUS wird die GPX-XML-Struktur sauber mit `</gpx>` abgeschlossen und für den WebDAV-Upload markiert.

---

## 5. Ringspeicher & BGH-Konformität (BGH VI ZR 233/17 & DSGVO)

Um den strengen Vorgaben des Bundesgerichtshofs (BGH-Urteil VI ZR 233/17) und der DSGVO bezüglich anlassloser Überwachung im Straßenverkehr zu entsprechen:

```
┌─────────────────────────────────────────────────────────────┐
│          BGH-KONFORME ROLLIERENDE SPEICHER-ARCHITEKTUR      │
├─────────────────────────────────────────────────────────────┤
│ • Kontinuierliches Ringspeicher-Verzeichnis: /tracks/       │
│ • Auto-Purge Schwellwert: Freier Speicher < 200 MB          │
│ • Älteste ungeschützte Segmente werden in 50MB-Blöcken      │
│   automatisch überschrieben                                 │
│ • Manueller Highlight-Schutz via Lenkertaster (*.fav.gpx)   │
│ • Unfall-Sensor-Trigger: Schock > 4G sperrt letzte 15 Min. │
└─────────────────────────────────────────────────────────────┘
```

1. **Rollierender Ringspeicher:** Normale Fahrdaten werden in 15-Minuten-Segmenten rollierend überschrieben.
2. **Crash-Freeze (Unfall-Erkennung):** Erkennt die Bosch BMI270 IMU einen extremen Stoßimpuls ($> 4{,}0\,\text{G}$) oder das Abreißen der Zündung bei hoher Querbeschleunigung (Sturz), werden die letzten 15 Minuten sowie alle Nachlaufdaten schreibgeschützt fixiert.
3. **Kryptographische Integrität (ECDSA SHA-256):** Jeder Track-Datensatz wird blockweise mit einem auf der ATECC608A / ESP32-eFuse hinterlegten Hardware-Schlüssel signiert, um die Echtheit der Schräglagen- und Geschwindigkeitsdaten vor Gericht nachzuweisen.

---

## 6. Map-Matching & Universeller GPX-Export (Web-App Pipeline)

```
[ MicroSD: tour_raw.gpx ] ──(BLE / WebDAV)──► [ Web Dashboard / Smartphone ]
                                                      │
                                                      ▼
                                       [ Map-Matching Engine (OSRM / Valhalla) ]
                                                      │
                         ┌────────────────────────────┴────────────────────────────┐
                         ▼                                                         ▼
           [ Bereinigte Navi-Route (.gpx) ]                           [ Reiner Visual-Track (.gpx) ]
           (20-50 gesetzte Shaping Points für                          (1:1 geglättete Linie für
            Garmin, Kurviger, Calimoto, TomTom)                        Google Maps, Komoot, Relive)
```

1. **Automatisches Road-Snapping:**
   * Die Web-App nutzt Routing-Engines (OSRM oder Valhalla), um die Rohkoordinaten mathematisch auf das reale Straßennetz von OpenStreetMap zu snappen. Wendemanöver auf Parkplätzen und minimale GPS-Drifts werden automatisch bereinigt.
2. **Export für Motorrad-Navis (Shaping Points):**
   * Die App erzeugt eine echte, routingfähige `.gpx`-Datei mit strategisch platzierten Wegepunkten (Shaping Points).
   * Diese kann direkt an Mitfahrer geteilt und in **Garmin Tread/Zūmo, BMW ConnectedRide, Kurviger, Calimoto oder TomTom** importiert werden, ohne dass das jeweilige Navi die Route eigenmächtig umberechnet.

---

## 7. Automatischer WebDAV / Nextcloud Upload im Heim-WLAN

```
MOTORRAD ROLLT IN DIE GARAGE (ZÜNDUNG AUS)
┌─────────────────────────────────────────────────────────────┐
│ 1. KL15 fällt ab -> USV-Nachlauf schaltet ein (Graceful Run)│
│ 2. ESP32-S3 scannt 60 s nach bekannten Heim-WLAN SSIDs      │
│ 3. WLAN gefunden -> Verbindung via WPA2/WPA3 Personal/Ent.  │
│ 4. TLS 1.3 Client verbindet zu Nextcloud / ownCloud / NAS   │
│ 5. Upload aller neuen *.gpx und Telemetrie-Dateien (1.8 MB/s)│
│ 6. Abschlussmeldung -> Dateisystem unmount -> Deep Sleep    │
└─────────────────────────────────────────────────────────────┘
```

* **Vollautomatisch:** Der Fahrer muss weder sein Smartphone zücken noch Speicherkarten entnehmen. Die Touren des Tages liegen beim Eintreten ins Haus bereits fertig im Nextcloud-Ordner bereit.

### 7.1 Cloud-Speicher-Architektur: Nextcloud vs. Schlanker Google-Drive WebDAV-Proxy (`omb.f0o.bar`)

Während Power-User mit eigener Nextcloud oder Synology-NAS direkt deren native WebDAV-URL ansprechen, können Fahrer ohne eigenen Server den schlanken **OpenMotorBridge Google-Drive WebDAV-Proxy** einsetzen:

1. **Vorteile der Cloud-Service-Architektur:**
   * **100 % plattformunabhängig:** Vollkommen identische Funktion für iPhone- (iOS ohne teure App-Store-Entwicklerlizenz) und Android-Fahrer.
   * **Autark & Smartphone-frei:** Das Motorrad lädt bei Ankunft im Heim-WLAN (oder unterwegs über den Mobilfunk-Proxy) völlig selbstständig hoch – das Smartphone kann ausgeschaltet in der Tasche bleiben.
2. **Warum kein klobiges Rclone?**
   * Rclone ist mit über 100 MB Binary und unzähligen Cloud-Subsystemen für diesen Zweck überdimensioniert.
   * Der WebDAV-Bedarf der Zentralbox beschränkt sich auf den Standard-HTTP-Befehl `PUT /tracks/<dateiname>.gpx` (Dateigröße typisch 200 KB bis 3 MB) mit HTTP Basic Auth.
3. **Architektur des Microservice (`omb-gdrive-bridge` auf `omb.f0o.bar`):**
   * Ein leichtgewichtiger Python/FastAPI-Container (< 30 MB RAM) empfängt den WebDAV-`PUT`-Stream.
   * Über das einmalig hinterlegte Google OAuth2-Refresh-Token (Google Drive API v3) wird die GPX-Datei direkt in den Zielordner `omb/tracks/` auf Google Drive abgelegt.
   * Nach erfolgreichem Upload antwortet der Server mit `201 Created`.
   * **Smart-Home-Hook & Rich Tour-Statistiken:** Sendet unmittelbar nach Upload vollautomatisierte Telemetrie-Events via MQTT (`omb/tracks/uploaded` als JSON sowie `omb/tracks/summary` als formatierte Textnachricht) und/oder Webhook:
     * **Uhrzeiten & Nettofahrzeit:** Start- und Endzeitpunkt sowie reine Netto-Fahrzeit (automatischer Stillstandsfilter $< 3\,\text{km/h}$) und Pausendauer.
     * **Höhenprofil & Höhenmeter:** Min./Max. Höhe über NN sowie kumulierte Höhenmeter aufwärts ($\sum \Delta h_{\text{auf}}$) und abwärts ($\sum \Delta h_{\text{ab}}$).
     * **Umgebungstemperatur:** Minimal-, Maximal- und Durchschnittstemperatur der Tour ($T_{\min}, T_{\max}, T_{\text{avg}}$).
     * **Geschwindigkeiten:** Höchstgeschwindigkeit ($v_{\max}$) und echte Netto-Durchschnittsgeschwindigkeit ($\bar{v}_{\text{netto}}$).
     * **Fahrdynamik (G-Kräfte):** Maximale Beschleunigung ($+g$) und maximale Bremsverzögerung ($-g$).
     * **Schräglagen-Auswertung:** Maximale Schräglage getrennt nach Links- und Rechtskurven.
     * **Kurvenzähler:** Intelligente Hysterese-Erkennung für Links-, Rechts- und Gesamtkurvenanzahl.
     * **Motordrehzahl (CAN):** Maximale und durchschnittliche Drehzahl (U/min).
     * **Bordnetz-Gesundheit:** Minimale und durchschnittliche Batteriespannung während der Fahrt.
4. **Self-Hosted & Zero-Trust Datenschutz (Kein Fremdzugriff auf fremde Drives):**
   * **Volle Datensouveränität:** OpenMotorBridge betreibt keinen zentralen Sammeldienst für Nutzerdaten. Der Microservice `omb-gdrive-bridge` wird als schlüsselfertiges Open-Source-Image (`Dockerfile` / `podman-compose.yml`) bereitgestellt.
   * **Eigene Google-Credentials:** Jeder Nutzer richtet seinen Dienst bei sich selbst ein (z. B. auf dem eigenen Server `omb.f0o.bar`, Synology Docker, Raspberry Pi oder Unraid) und hinterlegt dort seine eigenen Google-Cloud-API-Credentials.
   * **Null Haftung & Null DSGVO-Schnittstellen:** Niemand muss dem OpenMotorBridge-Projekt Zugriff auf sein privates Google Drive gewähren. Bewegungsprofile, Schräglagendaten und Fahrstrecken verbleiben zu 100 % in der Hand des jeweiligen Fahrers.
   * **Quellcode & Setup-Anleitung:** Vollständiger Code, Dockerfile und das interaktive Token-Setup-Tool liegen einsatzbereit im Repository unter [`apps/gdrive_webdav_bridge/`](../../apps/gdrive_webdav_bridge/README.md).

---

## 8. Minimaler USB Mass Storage Class (MSC) Modus

Wird die Zentralbox über den nativen USB-C-Port an einen PC, Mac oder ein Tablet angeschlossen, während die Fahrzeugzündung (KL15) ausgeschaltet ist, startet der ESP32-S3 im **Minimalen USB MSC Modus**:

```
┌─────────────────────────────────────────────────────────────┐
│             MINIMALER USB MASS STORAGE CLASS MODUS          │
├─────────────────────────────────────────────────────────────┤
│ • VBUS-Erkennung (5V am nativen USB-C Port)                 │
│ • Haupt-Relais & Audio-DSP (ES8388) bleiben STROMISOLIERT   │
│ • Funkmodule (LoRa, Mesh, Bluetooth) bleiben DEAKTIVIERT    │
│ • Stromaufnahme aus USB-Port: < 80 mA (Keine Belastung Akku)│
│ • MicroSD-Karte wird als USB-Flash-Laufwerk bereitgestellt  │
└─────────────────────────────────────────────────────────────┘
```

* **Kein Werkzeug / Kein Kartenauswurf:** Der Rechner bindet die Box direkt als USB-Laufwerk `OPENMOTOR` ein.
* **Direktzugriff:** Touren aus `/tracks/` können direkt in Google Earth, BaseCamp, GPXSee oder Kurviger geöffnet werden.
