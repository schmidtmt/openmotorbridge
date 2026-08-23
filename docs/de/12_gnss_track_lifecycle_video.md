# 12 - GNSS Multi-Constellation, IMU Traegheitsnavigation & Video-Sync

Das OMB-TourLog-Subsystem kombiniert hochpraezise Satellitennavigation mit inertialsensorischer Koppelnavigation (Dead Reckoning), um auch in Tunnels, engen Schluchten und bei Abschattungen lueckenlose Tracks mit vollstaendiger Fahrzeugdynamik aufzuzeichnen.

## 1. 15-State Extended Kalman Filter (EKF) & Traegheitsnavigation
Faellt das Satellitensignal aus, schaltet das System nahtlos auf Traegheitskopplung um. Der EKF schaetzt kontinuierlich folgende Zustaende:
- Position im Navigationskoordinatensystem (Nord, Ost, Hoehe)
- Geschwindigkeitsvektor ueber Grund
- Orientierungsquaternion (Schraeglage / Lean Angle, Nickwinkel, Gierwinkel)
- Dynamischer Sensor-Bias von Beschleunigungsmesser und Gyroskop (Bosch BMI270)

### Schraeglagen- und Zentrifugalkraft-Berechnung
Lean_Angle = arctan((v * yaw_rate) / g)  
Das Filter unterscheidet anhand der Querbeschleunigung und Gierrate zuverlaessig zwischen echter Kurvenschraeglage und statischer Fahrbahnneigung.

## 2. Track-Lifecycle & Intelligente Segmentierung
- **Auto-Start:** Startet eine neue Tour-Datei (`YYYY-MM-DD_HH-MM-SS.gpx`), sobald die Zuendung an ist und das Bike sich laenger als 10 s mit > 5 km/h bewegt.
- **Segment-Split (`<trkseg>`):** Bei Ampel- oder Tankstopps unter 15 Minuten wird die GPX-Datei nicht geschlossen, sondern ein neues Track-Segment geoeffnet.
- **Auto-Finalisierung:** Nach 15 Minuten Dauerstillstand oder 60 Sekunden nach Zuendung AUS wird die GPX-Struktur sauber abgeschlossen und fuer den WebDAV-Upload markiert.

## 3. GPX 2.0 Telemetrie & 1-PPS Video-Sync
- **Telemetrie-Tags:** Geschwindigkeit, Schraeglage, Beschleunigungswerte und Satelliten-Metadaten pro Trackpunkt.
- **1-PPS Hardware-Sync:** Das u-blox MAX-M10S Modul liefert an `PIN_GNSS_PPS` einen hochpraezisen 1-Hz-Takt mit Zeitjitter < 1 us.
- **Video-Marker:** Shutter-Events vom BLE-Lenkertaster werden mit Mikrozeitstempel eingebettet, um Actioncam-Footage (GoPro/Insta360) framegenau mit Schraeglagendaten zu ueberblenden.
