# 12 - GNSS Multi-Constellation, Automotive Dead Reckoning (ADR) & Map-Matching

Das OMB-TourLog-Subsystem kombiniert hochpraezise Satellitennavigation (u-blox MAX-M10S) mit inertialsensorischer Koppelnavigation (Automotive Dead Reckoning - ADR) und CAN-Bus-Raddrehzahlen, um auch in Tunneln, tiefen Schluchten und bei Abschattungen lueckenlose Tracks mit voller Fahrzeugdynamik aufzuzeichnen.

---

## 1. Architektur & Sensor-Fusion (Automotive Dead Reckoning - ADR)

```
[ u-blox GNSS Modul (M10S 10 Hz) ] ──(UART 460.8k)──┐
[ CAN-Bus Raddrehzahl / Speed ] ────(10-20 Hz)───────┼─► [ 15-State Extended Kalman Filter ] ──► [ MicroSD: tour.gpx ]
[ Bosch BMI270 Gyro / Accel (I2C) ] ─(50-100 Hz)─────┘        (Dead Reckoning Engine)            (Mit Schräglage & G-Force)
```

### 1.1 Lueckenlose Tunnel-Navigation (Inertial Navigation)
Bricht der GPS-Empfang in Tunneln, dichten Waldgebieten oder alpinen Kehren ab, schaltet das System unterbrechungsfrei auf Traegheitsnavigation um:
* Die CAN-Bus Raddrehzahl (oder J1939 Radgeschwindigkeit) liefert die exakt gefahrene Distanz ($\Delta s = v \cdot \Delta t$).
* Das Gyroskop der BMI270 IMU integriert Kurven, Richtungs- und Hoehenaenderungen kontinuierlich auf.
* Der Track laeuft im Tunnel ohne Einfrieren, Spruenge oder Zick-Zack-Muster nahtlos weiter.

### 1.2 Kompensation von Multipath-Spruengen (Felswand-Filterung)
GPS-Messausreisser (z. B. 40-Meter-Positionssprueenge durch Signalreflexionen an steilen Felswaenden) werden vom Kalman-Filter automatisch verworfen: Die IMU meldet dem EKF, dass physikalisch keine entsprechende Querbeschleunigung stattgefunden hat, wodurch der Track auf der realen Fahrbahnlinie gehalten wird.

### 1.3 MotoGP-Style Telemetrie & Schraeglagen-Logging
Jeder Wegpunkt im GPX-Datensatz wird um hochpraezise Fahrdynamik-Metadaten erweitert:
- Kurvenschraeglage links/rechts (°): $\text{Lean\_Angle} = \arctan\left(\frac{v \cdot \dot{\psi}}{g}\right)$
- Laengs- und Querbeschleunigung (Brems- und Beschleunigungs-G-Kraefte)
- Bordnetz- und Batteriespannung

---

## 2. Track-Lifecycle & Intelligente Segmentierung
- **Auto-Start:** Startet eine neue Tour-Datei (`YYYY-MM-DD_HH-MM-SS.gpx`), sobald die Zuendung an ist und das Bike sich laenger als 10 s mit > 5 km/h bewegt.
- **Segment-Split (`<trkseg>`):** Bei Ampel- oder Tankstopps unter 15 Minuten wird die GPX-Datei nicht geschlossen, sondern ein neues Track-Segment geoeffnet.
- **Auto-Finalisierung:** Nach 15 Minuten Dauerstillstand oder 60 Sekunden nach Zuendung AUS wird die GPX-Struktur sauber abgeschlossen und fuer den WebDAV-Upload markiert.

---

## 3. GPX 2.0 Telemetrie & 1-PPS Video-Sync
- **1-PPS Hardware-Sync:** Das u-blox MAX-M10S Modul liefert an `PIN_GNSS_PPS` (GPIO 21) einen hochpraezisen 1-Hz-Takt mit Zeitjitter $< 1\,\mu\text{s}$ (RMS $< 15\,\text{ns}$).
- **Video-Marker:** Shutter-Events vom BLE-Lenkertaster werden mit Mikrozeitstempel eingebettet, um Actioncam-Footage (GoPro/Insta360/DJI) framegenau mit Schraeglagendaten zu synchronisieren:

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T09:15:00.100Z</time>
  <extensions>
    <omb:telemetry>
      <omb:lean_angle>44.2</omb:lean_angle>
      <omb:speed_kmh>84.6</omb:speed_kmh>
      <omb:accel_g_lon>-0.72</omb:accel_g_lon>
      <omb:battery_v>12.6</omb:battery_v>
      <omb:satellites>18</omb:satellites>
    </omb:telemetry>
  </extensions>
</trkpt>
```

---

## 4. Actioncam & 360-Grad-Kamera-Steuerung via Lenkertaster

OpenMotorBridge ermoeglicht die direkte drahtlose Steuerung von Actioncams ueber den Bluetooth-Lenkertaster und die synchrone Einbettung von GPS- und Schraeglagentelemetrie direkt in die Video-Metadaten.

### 4.1 Tastenbelegung am Lenkertaster
* **Kurzer Klick (Short Press):** Setzt einen Video-Highlight-Marker (`<omb:action_event>`) im aktiven GPX-Track (fuer automatisierte Best-of-Schnittlisten).
* **Doppelklick (Double Press):** Startet / Stoppt die Videoaufnahme auf der gekoppelten Actioncam (Aufnahme-Toggle).
* **Langer Klick (Long Press > 1.5 s):** Loest ein hochaufloesendes Einzelfoto (Snapshot) aus.
* **Apex-Auto-Trigger:** Ueberschreitet die Schraeglage einen Schwellwert von $> 45^\circ$, kann automatisch ein Highlight-Tag gesetzt werden.

### 4.2 Unterstuetzte Kamera-Protokolle (BLE-Integration)
1. **GoPro (Hero 9/10/11/12/13, Max):**
   * Steuerung ueber die offizielle **Open GoPro BLE API** (GATT Service `0xFEA6`, Shutter Start/Stop, Mode Change).
2. **Insta360 (X3 / X4 / Ace Pro / ONE RS 360):**
   * **Insta360 GPS Smart Remote Emulation:** Der ESP32-S3 emuliert die offizielle Insta360 GPS-Fernbedienung ueber BLE.
   * Telemetriedaten (10 Hz GPS-Position, Geschwindigkeit, Kompasskurs und Hoehe) werden live an die Insta360 gestreamt $\rightarrow$ die Kamera bettet die Telemetrie **nativ in den GPMF/INSV-Videocontainer** ein, sodass die Insta360 App Tachometer und Schraeglagen ohne manuelle Synchronisation direkt rendern kann!
3. **DJI (Osmo Action 3 / 4 / 5 Pro):**
   * DJI BLE Remote Protocol fuer Record Start/Stop und GPS-Tagging.
4. **Hardware-Kamera-Power:**
   * Der Schaltausgang `RESERVE_GPIO_B` (HD26 Pin 26) schaltet bei Bedarf ueber ein externes 5V USB-Power-Gate die Stromversorgung der Kameras bei Zuendung AN/AUS.

### 4.3 Telemetrie-Overlay & Post-Processing Pipeline
* **Driftfreie Synchronisation:** Durch den Abgleich des 1-PPS GPS-Zeitstempels mit dem Kamera-Timecode bleibt die Schräglagenanzeige selbst bei mehrstuendigen Fahrten auf $< 15\,\text{ms}$ framegenau synchron zum Videobild.
* **Universeller Telemetrie-Export:** Export der GPX-Tracks im passenden Format fuer **Telemetry Overlay, Garmin VIRB Edit, Dashware** oder automatisierte ffmpeg-Rendering-Pipelines.

---

## 5. Map-Matching & Universeller GPX-Export (Web-App Pipeline)

```
[ MicroSD: tour_raw.gpx ] ──(BLE Download)──► [ Web Dashboard / Smartphone ]
                                                      │
                                                      ▼
                                       [ Map-Matching Engine (OSRM / Valhalla) ]
                                                      │
                         ┌────────────────────────────┴────────────────────────────┐
                         ▼                                                         ▼
           [ Bereinigte Navi-Route (.gpx) ]                           [ Reiner Visual-Track (.gpx) ]
           (20-50 gesetzte Shaping Points fuer                         (1:1 geglaettete Linie fuer
            Garmin, Kurviger, Calimoto, TomTom)                        Google Maps, Komoot, Relive)
```

1. **Automatisches Road-Snapping:**
   * Die Web-App nutzt Routing-Engines (OSRM oder Valhalla), um die Rohkoordinaten mathematisch auf das reale Strassennetz von OpenStreetMap zu snappen. Wendemanoever auf Parkplaetzen und minimale GPS-Drifts werden automatisch bereinigt.
2. **Export fuer Motorrad-Navis (Shaping Points):**
   * Die App erzeugt eine echte, routingfaehige `.gpx`-Datei mit strategisch platzierten Wegepunkten (Shaping Points).
   * Diese kann direkt an Mitfahrer geteilt und in **Garmin Tread/Zūmo, BMW ConnectedRide, Kurviger, Calimoto oder TomTom** importiert werden, ohne dass das jeweilige Navi die Route eigenmaechtig umberechnet.
