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
* **Kurvenschräglage links/rechts (°):** $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
* **Längs- und Querbeschleunigung (Brems- und Beschleunigungs-G-Kräfte):** Aus kalibrierten IMU-Werten.
* **Bordnetz- und Batteriespannung:** Zur Diagnose von Lichtmaschine und Regler.
* **1-PPS Hardware-Zeitsynchronisation:** Mit $< 15\,\text{ns}$ Jitter für framegenaue Actioncam-Videomarker.

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
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
      <omb:hdop>0.8</omb:hdop>
    </omb:telemetry>
  </extensions>
</trkpt>
```

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
