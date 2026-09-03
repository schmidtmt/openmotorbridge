# 06 - Telemetrie-Blackbox, SDIO-Ringpuffer & WebDAV-Sync

Dieses Dokument spezifiziert das Telemetrie- und Speicher-Subsystem der OpenMotorBridge v8.0: die 4-Bit High-Speed SDIO-Schnittstelle, den DSGVO- und BGH-konformen Ringspeicher mit kryptographischer Signierung, den automatischen TLS-gesicherten WebDAV-Cloud-Upload sowie den sparsamen **USB Mass Storage Class (MSC) Modus** für den werkzeuglosen Datenaustausch am Rechner.

---

## 1. Speicheranbindung & High-Speed SDIO (4-Bit @ 40 MHz)

* **Schnittstelle:** Nativer 4-Bit SDIO-Bus @ 40 MHz direkt angebunden an den ESP32-S3 (GPIOs 40–45).
* **Durchsatz:** Kontinuierliche Schreibrate $> 12\,\text{MB/s}$ (unterbrechungsfreies 10 Hz GPX-, IMU-, Schräglagen- und Audio-Telemetrie-Logging).
* **Dateisystem:** FAT32 mit dynamischer Sektor-Pufferung (Clustergröße 32 kB).
* **Ausfallsicherheit:** Der integrierte BQ24075 USV-Puffer garantiert selbst bei plötzlichem Bordnetzabriss das saubere Schließen der FAT-Dateitabellen ohne Datenkorruption.

---

## 2. Ringspeicher & BGH-Konformität (BGH VI ZR 233/17 & DSGVO)

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

## 3. Automatischer WebDAV / Nextcloud Upload im Heim-WLAN

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

## 4. Minimaler USB Mass Storage Class (MSC) Modus

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
