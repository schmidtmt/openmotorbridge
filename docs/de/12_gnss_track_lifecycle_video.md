# 12 - GNSS-Engine, Track-Lifecycle & Actioncam-Sync

## 1. Hardware & Performance
* u-blox MAX-M10S Multi-GNSS Receiver im Heck-Pod 3 mit 25 x 25 mm Keramik-Patchantenne.
* Gleichzeitiger Empfang von GPS, GLONASS, Galileo und BeiDou bei 10 Hz Aktualisierungsrate.
* Empfindlichkeit: -167 dBm Navigation Tracking; Kaltstart < 26 s.

## 2. Track-Lifecycle State Machine
* **Tour Start:** Automatische Aufzeichnung startet, sobald KL15 aktiv ist und Geschwindigkeit > 5 km/h über 10 Sekunden überschreitet.
* **Kurzer Stopp (< 15 min):** Erzeugt ein neues `<trkseg>` innerhalb der aktuellen GPX-Datei (Tankstopps, Ampelphasen).
* **Langer Stillstand (> 15 min oder Zündung AUS):** Schließt die aktuelle Tour ab und finalisiert die XML-Struktur auf der MicroSD-Karte.

## 3. Actioncam Synchronisation (GPX 2.0 Erweiterung)
Hardware-getaktete Events (z. B. Shutter-Trigger über BLE-Lenkertaster) werden mit 1-PPS-Genauigkeit (< 1 µs) direkt in das GPX-Schema eingebettet:

```xml
<trkpt lat="47.3769" lon="8.5417">
  <ele>408.2</ele>
  <time>2026-08-23T08:34:26Z</time>
  <extensions>
    <omb:action_event type="video_marker" camera="gopro_hero12" clip_offset_ms="12450"/>
  </extensions>
</trkpt>