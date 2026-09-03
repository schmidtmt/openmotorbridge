# OpenMotorBridge (v8.0) – Universelle Motorrad-Intercom- & Telemetrie-Bridge

<p align="center">
  <img src="docs/assets/openmotorbridge_logo.svg" alt="OpenMotorBridge Logo" width="220"/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="docs/assets/openmotormesh_logo.svg" alt="OpenMotorMesh Logo" width="220"/>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue.svg" alt="Language: English"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/Sprache-Deutsch-green.svg" alt="Sprache: Deutsch"/></a>
  <a href="https://cern-ohl.web.cern.ch/"><img src="https://img.shields.io/badge/Hardware%20License-CERN--OHL--S%20v2-orange.svg" alt="Hardware License: CERN-OHL-S v2"/></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.html"><img src="https://img.shields.io/badge/Software%20License-GPL%20v3-blue.svg" alt="Software License: GPL v3"/></a>
  <a href="https://creativecommons.org/licenses/by-sa/4.0/"><img src="https://img.shields.io/badge/Docs-CC%20BY--SA%204.0-lightgrey.svg" alt="Documentation: CC BY-SA 4.0"/></a>
</p>

Die **OpenMotorBridge (OMB)** ist eine offene, herstellerübergreifende Kommunikations- und Telemetrieplattform für Motorräder. Sie verbindet proprietäre Funk- und Mesh-Systeme (z. B. **Sena Mesh 3.0** und **Cardo DMC Gen2**) galvanisch getrennt mit einem offenen **2,4-GHz / 868-MHz OpenMotorMesh (OMM)**, hochpräzisem **GNSS-Tour-Logging (Automotive Dead Reckoning)** und einem **kabellosen WebBLE PWA Cockpit**.

---

## 📚 Inhaltsverzeichnis der Dokumentation

Die modulare technische Gesamtspezifikation gliedert sich in 16 thematisch strukturierte Kapitel:

1. [**01 - Systemarchitektur & Satelliten-Topologie**](docs/de/01_system_architecture.md)  
   *Überblick über die 5-Punkt-Topologie, HF-Diversität, Cockpit-Integration und das Gesamtsystem.*

2. [**02 - Intercom-Matrix, Profile & Dynamisches Routing**](docs/de/02_intercom_matrix_profiles.md)  
   *Die 5 OEM-Adapterklassen A–E, LittleFS-Profil-Engine, Zero-Latency PTT (< 1,8 ms) und Audio-Cross-Matrix.*

3. [**03 - Audio-DSP, Akustik & Knowles MEMS Wind-Tracking**](docs/de/03_audio_dsp_acoustics.md)  
   *1500V Bourns Trennung, ES8388 Audio-Codec, Knowles MEMS Fahrtwind-Abtastung & Raised-Cosine Ducking.*

4. [**04 - Mesh-Netzwerk, LoRa & GNSS-Navigation**](docs/de/04_mesh_lora_navigation.md)  
   *OpenMotorMesh (OMM), Dynamic Leader Election (DLE), 868 MHz LoRa Fallback & 10 Hz Multi-GNSS.*

5. [**05 - Stromversorgung, USV-Akkusystem & Power-Gate**](docs/de/05_power_management_ups.md)  
   *LM5164-Q1 72V Buck, BQ24075 USV, Front-Node LMR36015 / TPS2051B Power-Gate & 1-Klick CarPlay Kaltstart.*

6. [**06 - Telemetrie-Blackbox, SDIO-Ringpuffer & WebDAV-Sync**](docs/de/06_telemetry_blackbox_webdav.md)  
   *4-Bit High-Speed SDIO, BGH- und DSGVO-konformer Ringspeicher, ECDSA SHA-256 & automatischer Cloud-Sync.*

7. [**07 - Hardware-Architektur & Platinen-Pinouts (PCBA 01 bis 05)**](docs/de/07_pcba_hardware_pinouts.md)  
   *Alle 5 Leiterplatten im Detail: Lagenaufbau, Impedanzen, Net-Klassen, Funktionszonen und Pinout-Tabellen.*

8. [**08 - Mechanische Gehäuse, CAD & Dichtungssystem**](docs/de/08_enclosures_mechanics_cad.md)  
   *3-teilige Zentralbox, universelle Satelliten-Pods, Wechselkassetten, Heck-Pod 3 und 4-in-1 Front-Knoten.*

9. [**09 - Firmware-Architektur, FreeRTOS & Rollback-OTA**](docs/de/09_firmware_architecture.md)  
   *Multi-Core ESP32-S3, RP2040, ESP32-C3, ESP-NOW Low-Latency-Protokoll und ausfallsicheres Dual-Bank OTA.*

10. [**10 - WebApp PWA & Dashboard-Bedienung**](docs/de/10_webapp_pwa_dashboard.md)  
    *Autarkes WebBLE Dashboard, Fahrdynamik-HUD, Front-Node Steuerung (1-Klick Reboot) & 4-stufiger GPX-Export.*

11. [**11 - Digitale Simulation & Multi-Physik Master-Testbench**](docs/de/11_simulation_testbench.md)  
    *9 modulare Python-Testbenches und 10 HIL-Szenarien für SPICE, Thermik, Transienten, RF und Akustik.*

12. [**12 - EMV-Härtung, Schirmung & ESD-Schutz**](docs/de/12_emv_rf_hardening.md)  
    *Kfz-Transienten nach ISO 7637-2, 2.4 GHz vs 868 MHz Entkopplung, IPC-CC-830B Schutzlack & ISO 16750-3.*

13. [**13 - Stücklisten (BOM) & SMT-Fertigungsdaten**](docs/de/13_bom_manufacturing.md)  
    *Komplette Bauteilliste für alle 5 PCBAs, JLCPCB SMT-Bestellcheckliste, Kabelbaum-Pigtail & Normteile.*

14. [**14 - Bauanleitung, Verkabelung & Fahrzeug-Installation**](docs/de/14_build_instructions_assembly.md)  
    *Schritt-für-Schritt Aufbau, 3D-Druck (FDM vs. MJF), Front-Node Montage (BMW GS / Harley) & Inbetriebnahme.*

15. [**15 - Automotive-Standards & Normen-Referenzen**](docs/de/15_standards_references.md)  
    *Industrienormen: ISO 7637-2, ISO 16750, ECE R10, RED 2014/53/EU, IEC 61672-1 Class 1 und Bluetooth SIG.*

16. [**16 - Datenschutz (DSGVO), Recht & Konformität**](docs/de/16_legal_compliance_dsgvo.md)  
    *Open-Source-Lizenzen (GPL-3.0, CERN-OHL-S v2, CC BY-SA 4.0), DSGVO/BGH-Konformität & Haftungsausschluss.*

---

## 🛠️ Repository-Übersicht

* **`docs/de/`**: Sämtliche technische Spezifikationen und Designdokumente auf Deutsch.
* **`docs/en/`**: Vollständige technische Spezifikationen auf Englisch.
* **`firmware/main_controller/`**: ESP-IDF / C++ Quellcode für die zentrale Steuerbox (ESP32-S3).
* **`firmware/rear_coprocessor/`**: ESP-IDF / C++ Quellcode für den Heck-Pod 3 Co-Prozessor (ESP32-C3).
* **`webapp_pwa/`**: Offlinefähiges WebBLE Dashboard (HTML5, Vanilla JS, CSS3, Service Worker, i18n).
* **`hardware/`**: KiCad Schaltpläne, Gerber-Dateien und 3D-Modelle für das Gehäuse.

---

## 📜 Lizenzen

* **Hardware & PCB-Layouts:** [CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2) (Strongly Reciprocal)
* **Firmware & Web-Dashboard:** [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html)
* **Dokumentation & 3D-Modelle:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## ⚠️ Haftungsausschluss (Disclaimer)

Die in diesem Projekt veröffentlichten Inhalte werden unentgeltlich und auf "AS IS"-Basis zur Verfügung gestellt. Der Nachbau, Einbau und Betrieb erfolgt vollumfänglich auf eigene Verantwortung und eigenes Risiko des Anwenders. Alle genannten Markennamen (Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay®) sind eingetragene Warenzeichen ihrer jeweiligen Eigentümer.