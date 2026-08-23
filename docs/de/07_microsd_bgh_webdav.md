# 07 - MicroSD-Speicher, BGH-Ringspeicher, WebDAV-Sync & USB MSC

Dieses Dokument spezifiziert die Speicheranbindung ueber 4-Bit SDIO, den DSGVO/BGH-konformen Ringspeicher, den automatischen WebDAV-Upload sowie den **minimalen USB Mass Storage Class (MSC) Modus** fuer den direkten PC/Mac-Zugriff.

---

## 1. Speicheranbindung & High-Speed SDIO

* **Schnittstelle:** Nativer 4-Bit SDIO-Bus @ 40 MHz angebunden an den ESP32-S3 (GPIOs 40–45).
* **Durchsatz:** Kontinuierliche Schreibrate $> 12\,\text{MB/s}$ (unterbrechungsfreies 10 Hz GPX-, IMU- und Audio-Telemetrie-Logging).
* **Dateisystem:** FAT32 mit dynamischer Sektor-Pufferung (Clustergroesse 32 kB).

---

## 2. Ringspeicher & BGH-Konformitaet (BGH VI ZR 233/17 / DSGVO)

* **Rollierender Puffer:** Tourdaten werden als rollierender Puffer im Verzeichnis `/tracks/` abgelegt.
* **Auto-Purge-Schwellwert:** Sinkt der freie Speicher auf der MicroSD-Karte unter $200\,\text{MB}$, loescht die Firmware automatisch die aeltesten ungeschuetzten GPX-Dateien in 50-MB-Bloecken.
* **Schreibschutz fuer Highlights:** Manuell ueber den Lenkertaster markierte Abschnitte oder in der WebApp als Favorit gesetzte Touren (`*.fav.gpx`) sind dauerhaft vor dem Ueberschreiben geschuetzt.

---

## 3. WebDAV-Upload im Heim-WLAN

* **Automatischer Scan:** Beim Ausschalten der Zuendung (KL15 $< 11{,}8\,\text{V}$) scannt das System im USV-Nachlauf fuer bis zu 60 s nach bekannten Heim-WLAN-Netzwerken.
* **TLS 1.3 Upload:** Wird ein konfiguriertes Netzwerk erkannt, laedt der integrierte WebDAV-Client alle neuen GPX-Tracks vollautomatisch und verschluesselt (TLS 1.3) auf eine Nextcloud-, ownCloud- oder Synology-NAS hoch (Transferrate ca. $1{,}8\,\text{MB/s}$).
* **Rundown:** Nach erfolgreichem Sync schliesst das System das Dateisystem sauber ab und wechselt in den Deep Sleep.

---

## 4. USB Mass Storage Class (MSC) & Minimaler Boot-Modus

Wird die Zentralbox ueber den nativen USB-C-Port an einen PC, Mac oder ein Android/iPad-Tablet angeschlossen, waehrend die Fahrzeugzuendung (KL15) ausgeschaltet ist, startet der ESP32-S3 im **Minimalen USB MSC Modus**:

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

### Vorteile in der Praxis:
1. **Kein Werkzeug / Kein Kartenauswurf:** Die MicroSD-Karte verbleibt geschuetzt im IP67-Gehaeuse. Der Rechner erkennt die Box sofort als USB-Laufwerk `OPENMOTOR`.
2. **Direkter Zugriff:** Touren aus `/tracks/` koennen direkt in Google Earth, BaseCamp oder Kurviger geoeffnet und Kassetten-Profile in `/profiles/` editiert werden.
3. **Akku-Schonung:** Der Modus bootet nur den USB-Stack und den SDIO-Treiber; das gesamte Motorrad-Bordnetz und die Audioelektronik bleiben stromlos.
