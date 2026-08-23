# OpenMotorBridge & OMB-TourLog v8.0

> **Universelle Satelliten-Architektur, HF-härtendes Intercom-Gateway & BGH-konformer Tour-Logger für Motorräder.**

OpenMotorBridge (OMB) verbindet fragmentierte Motorrad-Kommunikationssysteme (Sena Mesh 3.0/2.0, Cardo DMC Gen2/Gen1, PMR446 Analogfunk) herstellerübergreifend und latenzfrei mit Bord-Infotainmentsystemen (z. B. Harley-Davidson Boom! Box GTS / Skyline OS) sowie Weitbereichs-Mesh-Netzen (OpenMotorMesh LoRa 868 MHz).

---

## 📁 Projektdokumentation (`docs/de/`)

Die vollständige technische Dokumentation und Systemspezifikation ist modular in 17 Referenzkapitel unterteilt:

1. [**01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik**](docs/de/01_system_architecture.md)  
   *4-Punkte-Satelliten-Konzept, HF-Koexistenz und Raumdiversität zur Vermeidung von 2,4-GHz-De-Sensing.*

2. [**02 - PCB Hardware & Pinout-Spezifikation**](docs/de/02_pcb_hardware_pinout.md)  
   *4-Lagen FR4 ENIG Layout, GPIO-Mapping des ESP32-S3 und HD26 / 2x13 Wannenstecker-Pinout.*

3. [**03 - Audio-Frontend & Symmetrische Schnittstellen**](docs/de/03_audio_frontend_isolated.md)  
   *Galvanische Trennung via Bourns Audio-Trafos, TLP222A PhotoMOS Taster-Trigger und Quittungston-Erkennung.*

4. [**04 - Stromversorgung & USV**](docs/de/04_power_management_ups.md)  
   *LM5164 Automotive 65V Buck Converter, BQ24075 Power-Path LiPo-USV und ISO 7637-2 Transientenfilter.*

5. [**05 - Mechanische Konstruktion: Zentralbox & Universal-Kassetten-Pods**](docs/de/05_mechanical_enclosure_pods.md)  
   *IP67 MJF-Gehäusedesign, 6-Pin Mill-Max Pogo-Schnittstelle und Doppel-Sicherheits-Arretierung.*

6. [**06 - Dynamische Hardwareprofile (LittleFS JSON)**](docs/de/06_dynamic_profiles_spec.md)  
   *Spezifikation der JSON-Profile für Sena Apex, Cardo DMC Gen2, Legacy-Geräte und Midland PMR446.*

7. [**07 - MicroSD-Speicher, BGH-Ringspeicher & WebDAV-Sync**](docs/de/07_microsd_bgh_webdav.md)  
   *4-Bit SDIO-Bus, BGH-konformes rollierendes Löschen (BGH VI ZR 233/17) und TLS 1.3 WebDAV Auto-Upload.*

8. [**08 - DSP Audio-Engine & Betriebsmodi**](docs/de/08_dsp_audio_engine.md)  
   *Echtzeit-Mischmatrix mit Raised-Cosine-Ducking, Standard Mode, Single Rider Mode und Cruise Mode.*

9. [**09 - Firmware-Architektur (C++ / FreeRTOS)**](docs/de/09_firmware_architecture.md)  
   *ESP-IDF Multitasking-Aufteilung auf Core 0 (Kommunikation/BLE) und Core 1 (Audio DSP / I2S DMA).*

10. [**10 - Web Bluetooth Dashboard & PWA Frontend**](docs/de/10_web_bluetooth_dashboard.md)  
    *Autarke Offline-HTML5-App zur Echtzeit-Telemetrieüberwachung, Moduswahl und Kassetten-Konfiguration.*

11. [**11 - OpenMotorMesh & DLE Leader Election**](docs/de/11_openmotormesh_dle_election.md)  
    *Dynamische Gateway-Master-Wahl über 8-Bit `CAP_FLAGS` Beacons für Cross-Domain-Mesh-Brücken.*

12. [**12 - GNSS-Engine, Track-Lifecycle & Actioncam-Sync**](docs/de/12_gnss_track_lifecycle_video.md)  
    *u-blox MAX-M10S Multi-GNSS mit 10 Hz, automatische Segmentierung und 1-PPS Video-Marker.*

13. [**13 - Heck-Pod 3 & Digitale OMM-Transceiver-Architektur**](docs/de/13_rear_pod3_transceiver_arch.md)  
    *Auslagerung von GNSS, SX1262 LoRa 868 MHz und ESP32-C3 Co-Prozessor an den Heckbürzel.*

14. [**14 - EMV-, HF- & Umwelthärtung**](docs/de/14_emv_rf_hardening.md)  
    *Kfz-Transienten-Schutz, Schutzlackierung nach IPC-CC-830B und 35 dB Freiraumdämpfung am Chassis.*

15. [**15 - BOM & Fertigungsleitfaden**](docs/de/15_bom_manufacturing.md)  
    *Stückliste für JLCPCB SMT-Bestückung, CPL/Gerber-Vorgaben und 3D-Druck-Parameter in PA12.*

16. [**16 - Rechtliche Compliance, Lizenzen & DSGVO**](docs/de/16_legal_compliance_dsgvo.md)  
    *ECE R10, RED 2014/53/EU Konformität sowie Lizenzbestimmungen (CERN-OHL-S v2, GPL-3.0, CC BY-SA 4.0).*

17. [**17 - Quellen- & Normenverzeichnis**](docs/de/17_standards_references.md)  
    *Fundstellen für ISO 7637-2, Bluetooth SIG Battery Service (0x180F), UBX-M10 und Intercom-Protokolle.*

---

## 🛠️ Repository-Übersicht

* **`docs/de/`**: Sämtliche technische Spezifikationen und Designdokumente auf Deutsch.
* **`firmware/main_controller/`**: ESP-IDF / C++ Quellcode für die zentrale Steuerbox (ESP32-S3).
  * `data/profiles/`: LittleFS JSON-Konfigurationsdateien für gesteckte Kassetten.
* **`firmware/rear_coprocessor/`**: ESP-IDF / C++ Quellcode für den Heck-Pod 3 Co-Prozessor (ESP32-C3).
* **`webapp_pwa/`**: Offlinefähiges WebBLE Dashboard (HTML5, Vanilla JS, CSS3, Service Worker).
* **`hardware/`**: KiCad Schaltpläne, Gerber-Dateien und 3D-Modelle für das Gehäuse.

---

## 📜 Lizenzen

* **Hardware & Mechanik:** [CERN-OHL-S v2](https://cern-ohl.web.cern.ch/)
* **Firmware & Software:** [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html)
* **Dokumentation:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)