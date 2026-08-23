# 16 - Rechtliche Compliance, Lizenzen & DSGVO

## 1. Open-Source-Lizenzierung
- **Hardware & CAD:** CERN Open Hardware Licence Strongly Reciprocal v2 (CERN-OHL-S v2).
- **Firmware & Software:** GNU General Public License v3.0 (GPL-3.0).
- **Dokumentation:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

## 2. Kfz- und Funk-Zulassung
- **ECE R10 Rev. 6:** Einhaltung der Grenzwerte fuer elektromagnetische Vertraeglichkeit im Kfz-Betrieb.
- **RED 2014/53/EU:** Konformitaet der Funkmodule (ESP32-S3, ESP32-C3, SX1262 LoRa) mit den europaeischen Frequenz- und Leistungsnormen.

## 3. Datenschutz & BGH-Konformitaet (BGH VI ZR 233/17)
- **Anlassbezogenes Logging:** Daten werden ausschliesslich lokal auf der MicroSD-Karte im rollierenden Puffer gespeichert.
- **Automatisches Ueberschreiben:** Ungeschuetzte Tracks werden bei Erreichen des Schwellwerts (< 200 MB freier Speicher) zyklisch ueberschrieben.
- **Kein Cloud-Zwang:** Der optionale WebDAV-Upload erfolgt ausschliesslich in private Benutzernetzwerke.
