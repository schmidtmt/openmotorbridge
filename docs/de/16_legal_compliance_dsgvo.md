# 16 - Rechtliche Compliance, Lizenzen & DSGVO

## 1. Open-Source-Lizenzierung
* **Hardware & CAD:** CERN Open Hardware Licence Strongly Reciprocal v2 (CERN-OHL-S v2).
* **Firmware & Software:** GNU General Public License v3.0 (GPL-3.0).
* **Dokumentation:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

## 2. Kfz- und Funk-Zulassung
* **ECE R10 Rev. 6:** Einhaltung der Grenzwerte für elektromagnetische Verträglichkeit im Kfz-Betrieb (keine Störaussendung auf Fahrzeugbusse).
* **RED 2014/53/EU:** Konformität der Funkmodule (ESP32-S3, ESP32-C3, SX1262 LoRa) mit den harmonisierten europäischen Frequenz- und Leistungsnormen.

## 3. Datenschutz & BGH-Konformität (BGH VI ZR 233/17)
* **Anlassbezogene Aufzeichnung:** GPS- und Telemetriedaten werden ausschließlich lokal auf der MicroSD-Karte im rollierenden Ringspeicher vorgehalten.
* **Automatisches Überschreiben:** Ungeschützte Daten werden bei Erreichen des Schwellwerts ($< 200\,\text{MB}$ freier Speicher) zyklisch in $50\text{-MB}$-Blöcken überschrieben.
* **Kein Cloud-Zwang:** Kein automatischer Transfer an Dritte. Der optionale WebDAV-Upload erfolgt ausschließlich in private, vom Nutzer betriebene Netzwerkspeicher.