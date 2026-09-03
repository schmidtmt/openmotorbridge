# 16 - Datenschutz (DSGVO), Recht & Konformität

Dieses Dokument definiert das Open-Source-Lizenzmodell, die regulatorischen Funk- und Kfz-Rahmenbedingungen, die Datenschutz-Architektur (DSGVO / BGH-Dashcam-Rechtsprechung) sowie den rechtlichen Haftungsausschluss für das Projekt OpenMotorBridge.

---

## 1. Open-Source-Lizenzmodell (Copyleft-Fokus)

Um sicherzustellen, dass Weiterentwicklungen (z. B. herstellerspezifische CAN- und Audio-Adapter für Honda, BMW, Harley oder Yamaha) als Open Source an die Community zurückfließen, steht dieses Projekt unter folgenden Lizenzen:

* **Firmware & Web-Dashboard (Code):** GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.de.html))
* **Hardware & PCB-Layouts (KiCad / Gerber):** CERN Open Hardware Licence Strongly Reciprocal v2 ([CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2))
* **3D-Druck- & CAD-Modelle (STEP, STL, Gehäusedaten):** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de))
* **Dokumentation & Protokoll-Spezifikationen:** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de))

---

## 2. Regulatorische Rahmenbedingungen & Funk-Zulassung (RED 2014/53/EU & FCC Part 15)

OpenMotorBridge nutzt ausschließlich standardisierte, weltweit lizenzfreie Frequenzbänder:

* **2,4-GHz-ISM-Band:** Maximal 100 mW EIRP (20 dBm) in der EU (ETSI EN 300 328) bzw. 1000 mW in den USA (FCC Part 15). Das Band ist weltweit harmonisiert und unterliegt bei Einsatz von FHSS/DSSS/LBT **keinem Duty-Cycle-Limit** (erlaubt kontinuierliches Full-Duplex-Audio).
* **868-MHz-SRD-Band (Sub-GHz LoRa):** Geregelt durch ETSI EN 300 220. Aufgrund der gesetzlichen Duty-Cycle-Limits (0,1 % bis 10 %) in Europa ist dieses Band für kontinuierliches Audio-Dauerstreaming ungeeignet (1 % = max. 36 s Sendezeit pro Stunde; 10 % High-Power = max. 360 s Sendezeit pro Stunde). Es wird in OMB gezielt für GPS-Gruppenradar und kurze Push-to-Talk (PTT) Sprachpakete mit Codec2 (1200 bps) genutzt.
* **446 MHz (PMR446 - Optionale Kassetten):** Maximal 500 mW ERP mit 12,5-kHz-Kanalraster im Halbduplex-Simplex-Betrieb unter Beachtung fester Antennenvorgaben.

---

## 3. Kfz-Typgenehmigung, CE-Konformität & E-Markierung (ECE R10 Rev. 6)

* **CE- & RED-Konformität:** Die Nutzung von vorkonfektionierten, zertifizierten Originalmodulen (z. B. Sena MeshPort Blue, Cardo Packtalk Kassetten) belässt die primäre Funkzulassung beim Originalhersteller.
* **Eigenbauten & Bausätze:** Der Nachbau und Betrieb von unzertifizierten Sender-Hardwareerweiterungen über den Expansion Port erfolgt auf eigene Verantwortung im Rahmen der jeweiligen nationalen Amateurfunk- bzw. ISM-Bestimmungen.
* **Kfz-Typgenehmigung & E-Markierung (ECE R10 Rev. 6):** Die Zentralbox und der Front-Knoten greifen über galvanische Trennglieder (Bourns 1500 V RMS Übertrager, Toshiba PhotoMOS-Relais, opto-isolierte PTT) und den CAN-Bus im Listen-Only-Modus vollkommen rückwirkungsfrei auf das Bordnetz zu. Es werden **keine Eingriffe in sicherheitsrelevante Steuergeräte (ECU, ABS, Traktionskontrolle)** vorgenommen.

---

## 4. Datenschutz & BGH-Konformität (BGH VI ZR 233/17 & DSGVO)

* **Anlassbezogenes Logging:** Telemetrie- und GPS-Daten werden ausschließlich lokal auf der internen MicroSD-Karte in einem rollierenden Ringpuffer gespeichert.
* **Automatisches Überschreiben:** Ungeschützte Tracks und Ringspeicher-Segmente werden bei Erreichen des Mindestspeicher-Schwellwerts (< 200 MB freier Speicher) zyklisch überschrieben.
* **Zero-Cloud-Zwang:** Es existiert keine zentrale Server-Infrastruktur oder Telemetrie-Übertragung an Dritte. Der optionale WebDAV-Upload erfolgt ausschließlich verschlüsselt (TLS 1.3) in private, vom Nutzer konfigurierte Cloud-/NAS-Speicher (Nextcloud/Synology).

---

## 5. Rechtlicher Haftungsausschluss (Disclaimer)

### 5.1 Bereitstellung "AS-IS" (Ohne Gewähr)
Die in diesem Projekt veröffentlichten Schaltpläne, Platinenlayouts, 3D-Druckdateien, Quellcodes und Einbauleitfäden werden unentgeltlich und "wie besehen" (AS IS) zur Verfügung gestellt. Es wird keinerlei Garantie oder Gewährleistung für Funktion, Zuverlässigkeit, Vollständigkeit oder Schadensfreiheit übernommen.

### 5.2 Haftungsausschluss für Fahrzeug- & Sachschäden
Der Nachbau, Einbau und Betrieb der Hard- und Software erfolgt vollumfänglich auf eigene Gefahr und eigenes Risiko des Nutzers. Der Autor und die Mitwirkenden haften nicht für Schäden an Fahrzeugen, Bordelektronik, Steuergeräten (CAN-Bus), Batterien oder sonstigen angeschlossenen Geräten sowie für Folgeschäden oder Unfälle, die aus der Nutzung oder dem fehlerhaften Einbau dieses Systems resultieren.

### 5.3 Straßenverkehrsordnung & Funk-Regularien
Das Gerät besitzt keine allgemeine E-Kennzeichnung / ABE für den öffentlichen Straßenverkehr. Der Betreiber ist selbst dafür verantwortlich, dass die geltenden nationalen Vorschriften hinsichtlich Funkfrequenzen, maximaler Sendeleistung (z. B. 100 mW EIRP im 2,4-GHz-Band) und Anbauten am Kraftfahrzeug eingehalten werden.

### 5.4 Marken- und Warenzeichen
Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay®, Android Auto® und sonstige erwähnte Markennamen sind eingetragene Warenzeichen der jeweiligen Eigentümer. Dieses Projekt steht in keinerlei geschäftlicher oder offizieller Verbindung zu diesen Unternehmen.
