# 17 - Rechtliche Compliance, Lizenzen, Funk-Regularien & DSGVO

Dieses Dokument definiert das Open-Source-Lizenzmodell, die regulatorischen Funk- und Kfz-Rahmenbedingungen, die Datenschutz-Architektur sowie den rechtlichen Haftungsausschluss fuer das Projekt OpenMotorBridge.

---

## 1. Open-Source-Lizenzmodell (Copyleft-Fokus)

Um sicherzustellen, dass Weiterentwicklungen (z. B. herstellerspezifische CAN- und Audio-Adapter fuer Honda, BMW oder Yamaha) als Open Source an die Community zurueckfliessen, steht dieses Projekt unter folgenden Lizenzen:

* **Firmware & Web-Dashboard (Code):** GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.de.html))
* **Hardware & PCB-Layouts (KiCad / Gerber):** CERN Open Hardware Licence Strongly Reciprocal v2 ([CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2))
* **3D-Druck- & CAD-Modelle (STEP, STL, Gehaeusedaten):** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de))
* **Dokumentation & Protokoll-Spezifikationen:** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de))

---

## 2. Regulatorische Rahmenbedingungen & Funk-Zulassung (RED 2014/53/EU & FCC Part 15)

OpenMotorBridge nutzt ausschliesslich standardisierte, weltweit lizenzfreie Frequenzbaender:

* **2,4-GHz-ISM-Band:** Maximal 100 mW EIRP (20 dBm) in der EU (ETSI EN 300 328) bzw. 1000 mW in den USA (FCC Part 15). Das Band ist weltweit harmonisiert und unterliegt bei Einsatz von FHSS/DSSS/LBT **keinem Duty-Cycle-Limit** (erlaubt kontinuierliches Full-Duplex-Audio).
* **868-MHz-SRD-Band (Sub-GHz LoRa):** Geregelt durch ETSI EN 300 220. Aufgrund der gesetzlichen Duty-Cycle-Limits (0,1 % bis 10 %) in Europa ist dieses Band fuer kontinuierliches Audio-Dauerstreaming ungeeignet (1 % = max. 36 s Sendezeit pro Stunde; 10 % High-Power = max. 360 s Sendezeit pro Stunde). Es wird in OMB gezielt fuer GPS-Gruppenradar und kurze Push-to-Talk (PTT) Sprachpakete mit Codec2 (1200 bps) genutzt.
* **446 MHz (PMR446 - Optionale Kassetten):** Maximal 500 mW ERP mit 12,5-kHz-Kanalraster im Halbduplex-Simplex-Betrieb unter Beachtung fester Antennenvorgaben.

---

## 3. Kfz-Typgenehmigung, CE-Konformitaet & E-Markierung (ECE R10 Rev. 6)

* **CE- & RED-Konformitaet:** Die Nutzung von vorkonfektionierten, zertifizierten Originalmodulen (z. B. Sena MeshPort Blue, Cardo Packtalk Kassetten) belaesst die primaere Funkzulassung beim Originalhersteller.
* **Eigenbauten & Bausaetze:** Der Nachbau und Betrieb von unzertifizierten Sender-Hardwareerweiterungen ueber den Expansion Port erfolgt auf eigene Verantwortung im Rahmen der jeweiligen nationalen Amateurfunk- bzw. ISM-Bestimmungen.
* **Kfz-Typgenehmigung & E-Markierung (ECE R10 Rev. 6):** Die Zentralbox greift ueber galvanische Trennglieder (Bourns 1500 V RMS Uebertrager, Toshiba PhotoMOS-Relais) und den CAN-Bus im Listen-Only-Modus vollkommen rueckwirkungsfrei auf das Bordnetz zu. Es werden **keine Eingriffe in sicherheitsrelevante Steuergeraete (ECU, ABS, Traktionskontrolle)** vorgenommen.

---

## 4. Datenschutz & BGH-Konformitaet (BGH VI ZR 233/17 & DSGVO)

* **Anlassbezogenes Logging:** Telemetrie- und GPS-Daten werden ausschliesslich lokal auf der internen MicroSD-Karte in einem rollierenden Ringpuffer gespeichert.
* **Automatisches Ueberschreiben:** Ungeschuetzte Tracks und Ringspeicher-Segmente werden bei Erreichen des Mindestspeicher-Schwellwerts (< 200 MB freier Speicher) zyklisch ueberschrieben.
* **Zero-Cloud-Zwang:** Es existiert keine zentrale Server-Infrastruktur oder Telemetrie-Uebertragung an Dritte. Der optionale WebDAV-Upload erfolgt ausschliesslich verschluesselt (TLS 1.3) in private, vom Nutzer konfigurierte Cloud-/NAS-Speicher (Nextcloud/Synology).

---

## 5. Rechtlicher Haftungsausschluss (Disclaimer)

### 5.1 Bereitstellung "AS-IS" (Ohne Gewaehr)
Die in diesem Projekt veroeffentlichten Schaltplaene, Platinenlayouts, 3D-Druckdateien, Quellcodes und Einbauleitfaeden werden unentgeltlich und "wie besehen" (AS IS) zur Verfuegung gestellt. Es wird keinerlei Garantie oder Gewaehrleistung fuer Funktion, Zuverlaessigkeit, Vollstaendigkeit oder Schadensfreiheit uebernommen.

### 5.2 Haftungsausschluss fuer Fahrzeug- & Sachschaeden
Der Nachbau, Einbau und Betrieb der Hard- und Software erfolgt vollumfaenglich auf eigene Gefahr und eigenes Risiko des Nutzers. Der Autor und die Mitwirkenden haften nicht fuer Schaeden an Fahrzeugen, Bordelektronik, Steuergeraeten (CAN-Bus), Batterien oder sonstigen angeschlossenen Geraeten sowie fuer Folgeschaeden oder Unfaelle, die aus der Nutzung oder dem fehlerhaften Einbau dieses Systems resultieren.

### 5.3 Material- & Fertigungshinweise (3D-Druck / Bauteile)
Die genannten Materialempfehlungen (z. B. PA12 MJF, ASA) und Fertigungsrichtlinien stellen lediglich unverbindliche Erfahrungswerte dar. Die thermische, chemische (Benzin/Oel) und mechanische Bestaendigkeit haengt massgeblich von den individuellen Druckparametern, dem verwendeten Filament und der fachgerechten Montage ab.

### 5.4 Strassenverkehrsordnung & Funk-Regularien
Das Geraet besitzt keine allgemeine E-Kennzeichnung / ABE fuer den oeffentlichen Strassenverkehr. Der Betreiber ist selbst dafuer verantwortlich, dass die geltenden nationalen Vorschriften hinsichtlich Funkfrequenzen, maximaler Sendeleistung (z. B. 100 mW EIRP im 2,4-GHz-Band) und Anbauten am Kraftfahrzeug eingehalten werden.

### 5.5 Marken- und Warenzeichen
Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay® und sonstige erwaehnte Markennamen sind eingetragene Warenzeichen der jeweiligen Eigentuemer. Dieses Projekt steht in keinerlei geschaeftlicher oder offizieller Verbindung zu diesen Unternehmen.
