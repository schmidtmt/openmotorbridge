# 07 - MicroSD-Speicher, BGH-Ringspeicher & WebDAV-Sync

## 1. Speicheranbindung
- 4-Bit SDIO-Bus (40 MHz) angebunden an den ESP32-S3 fuer Durchsatzraten > 12 MB/s.
- Dateisystem: FAT32 mit dynamischer Sektor-Pufferung.

## 2. Ringspeicher & BGH-Konformitaet (BGH VI ZR 233/17 / DSGVO)
- Tourdaten werden als rollierender Puffer in `/tracks/` gespeichert.
- Sinkt der freie Speicher unter 200 MB, loescht die Firmware automatisch die aeltesten ungeschuetzten GPX-Dateien in 50-MB-Bloecken.
- Favoriten und manuell markierte Abschnitte (`*.fav.gpx`) sind dauerhaft vor dem Ueberschreiben geschuetzt.

## 3. WebDAV-Upload im Heim-WLAN
- Beim Ausschalten der Zuendung (KL15 < 11.8 V) scannt das System fuer 60 s nach bekannten SSIDs.
- Wird ein konfiguriertes Heim-WLAN erkannt, laedt ein TLS 1.3 WebDAV-Client neue Touren vollautomatisch auf Nextcloud oder Synology hoch (ca. 1.8 MB/s).
- Nach erfolgreichem Upload schaltet sich die Box geordnet in den Deep Sleep.
