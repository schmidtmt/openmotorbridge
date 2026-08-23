# OpenMotorBridge & OMB-TourLog v8.0

> **Universal Satellite Architecture, RF-Hardened Intercom Gateway & Privacy-Compliant Motorcycle Tour Logger.**

[![Language: German](https://img.shields.io/badge/Language-German-blue.svg)](README.de.md)
[![Language: English](https://img.shields.io/badge/Language-English-green.svg)](README.md)
[![Hardware License](https://img.shields.io/badge/Hardware-CERN--OHL--S_v2-orange.svg)](https://cern-ohl.web.cern.ch/)
[![Firmware License](https://img.shields.io/badge/Firmware-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Docs License](https://img.shields.io/badge/Docs-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

OpenMotorBridge (OMB) unites fragmented motorcycle communication systems (Sena Mesh 3.0/2.0, Cardo DMC Gen2/Gen1, PMR446 analog radio) without vendor lock-in and with zero latency to onboard vehicle infotainment (e.g. Harley-Davidson Boom! Box GTS / Skyline OS) and long-range mesh networks (OpenMotorMesh LoRa 868 MHz).

---

## 📁 Technical Documentation

Full technical specifications and architectural documentation are available in English and German:

* **English Documentation:** [`docs/en/`](docs/en/)
* **German Documentation:** [`docs/de/`](docs/de/) (or see [README.de.md](README.de.md))

### English Chapter Index:
1. [**01 - System Architecture, Universal Satellite Topology & Acoustics**](docs/en/01_system_architecture.md)
2. [**02 - PCB Hardware & Pinout Specification**](docs/en/02_pcb_hardware_pinout.md)
3. [**03 - Audio Frontend & Isolated Interfaces**](docs/en/03_audio_frontend_isolated.md)
4. [**04 - Power Management, UPS, Undervoltage Protection & Winter Storage**](docs/en/04_power_management_ups.md)
5. [**05 - Mechanical Construction: Central Box, Sealing Concept & Universal Pods**](docs/en/05_mechanical_enclosure_pods.md)
6. [**06 - Dynamic Hardware Profiles (LittleFS JSON Specification)**](docs/en/06_dynamic_profiles_spec.md)
7. [**07 - MicroSD Storage, BGH Compliant Ring Buffer & WebDAV Auto-Sync**](docs/en/07_microsd_bgh_webdav.md)
8. [**08 - DSP Audio Engine, Raised-Cosine Ducking & Operating Modes**](docs/en/08_dsp_audio_engine.md)
9. [**09 - Firmware Architecture (C++ / FreeRTOS / ESP-IDF v5.x)**](docs/en/09_firmware_architecture.md)
10. [**10 - Web Bluetooth Dashboard & PWA Frontend**](docs/en/10_web_bluetooth_dashboard.md)
11. [**11 - OpenMotorMesh (868 MHz LoRa) & Dynamic Leader Election (DLE)**](docs/en/11_openmotormesh_dle_election.md)
12. [**12 - GNSS Engine, Track Lifecycle & Action Cam Sync**](docs/en/12_gnss_track_lifecycle_video.md)
13. [**13 - Rear Pod 3 & Digital OMM Transceiver Architecture**](docs/en/13_rear_pod3_transceiver_arch.md)
14. [**14 - EMC, RF Hardening & Environmental Resistance**](docs/en/14_emv_rf_hardening.md)
15. [**15 - Bill of Materials (BOM) & Manufacturing Guide**](docs/en/15_bom_manufacturing.md)
16. [**16 - Legal Compliance, Licenses & Data Privacy (GDPR)**](docs/en/16_legal_compliance_dsgvo.md)
17. [**17 - Standards, Norms & Reference Directory**](docs/en/17_standards_references.md)

---

## 🛠️ Repository Structure

* **`docs/en/`** & **`docs/de/`**: Technical documentation in English and German.
* **`firmware/main_controller/`**: ESP-IDF v5 C++ firmware for the central box (ESP32-S3).
* **`firmware/rear_coprocessor/`**: ESP-IDF v5 C++ firmware for Satellite Pod 3 (ESP32-C3).
* **`webapp_pwa/`**: Autonomous WebBLE Dashboard Progressive Web App (HTML5, Vanilla JS, CSS3, Service Worker) with bilingual i18n support.
* **`hardware/`**: KiCad 7/8 schematics, block diagrams, and MJF 3D enclosure models.

---

## 📜 Licenses

* **Hardware & Mechanics:** [CERN-OHL-S v2 (Strongly Reciprocal)](https://cern-ohl.web.cern.ch/)
* **Firmware & Software:** [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html)
* **Documentation & Graphics:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)
