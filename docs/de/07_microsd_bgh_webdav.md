# 07 - MicroSD-Speicher, BGH-Ringspeicher & WebDAV-Sync

## 1. Speicheranbindung
* 4-Bit SDIO-Bus ($40\,\text{MHz}$) angebunden an den ESP32-S3 für Durchsatzraten $> 12\,\text{MB/s}$.
* Formatierung: FAT32 mit dynamischer Sektor-Pufferung.

## 2. Ringspeicher & BGH-Konformität (BGH VI ZR 233/17 / DSGVO)
* Tourdaten werden als rollierender Puffer in `/tracks/` gespeichert.
* Sinkt der freie Speicher unter $200\,\text{MB}$, löscht die Firmware automatisch die ältesten ungeschützten GPX-Dateien in $50\text{-MB}$-Blöcken.
* Favoriten und manuell markierte Abschnitte (`*.fav.gpx`) sind vor dem Löschen geschützt.

## 3. WebDAV-Upload im Heim-WLAN
* Beim Ausschalten der Zündung (KL15 $< 11{,}8\,\text{V}$) scannt das System für $60\,\text{s}$ nach bekannten SSIDs.
* Wird ein konfiguriertes Heim-WLAN gefunden, lädt ein TLS 1.3 WebDAV-Client neue Touren auf Nextcloud oder Synology hoch (ca. $1{,}8\,\text{MB/s}$).
* Nach erfolgreichem Upload schaltet sich die Box geordnet in den Deep Sleep.