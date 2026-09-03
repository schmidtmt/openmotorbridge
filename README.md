# OpenMotorBridge (v8.0) – Universal Motorcycle Intercom & Telemetry Bridge

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

**OpenMotorBridge (OMB)** is an open-source, cross-vendor communication and telemetry bridge for motorcycles. It seamlessly interconnects proprietary wireless intercom systems (**Sena Mesh 3.0** and **Cardo DMC Gen2**) with an open **2.4 GHz / 868 MHz OpenMotorMesh (OMM)**, high-precision **GNSS Tour Logging (Automotive Dead Reckoning)**, and a **wireless WebBLE PWA cockpit dashboard**.

---

## 📚 Technical Documentation

The comprehensive technical specification is split into 16 logically organized chapters:

1. [**01 - System Architecture & Satellite Topology**](docs/en/01_system_architecture.md)  
   *Overview of the 5-point architecture, spatial RF diversity, cockpit integration, and overall system design.*

2. [**02 - Intercom Matrix, Hardware Profiles & Routing**](docs/en/02_intercom_matrix_profiles.md)  
   *The 5 OEM adapter classes A–E, LittleFS profile engine, zero-latency PTT (< 1.8 ms), and audio cross-matrix.*

3. [**03 - Audio DSP, Acoustics & Knowles MEMS Wind Tracking**](docs/en/03_audio_dsp_acoustics.md)  
   *1500V Bourns isolation, ES8388 Codec, Knowles MEMS acoustic wind sampling, and Raised-Cosine Ducking.*

4. [**04 - Mesh Network, LoRa & GNSS Navigation**](docs/en/04_mesh_lora_navigation.md)  
   *OpenMotorMesh (OMM), Dynamic Leader Election (DLE), 868 MHz LoRa fallback, and 10 Hz Multi-GNSS.*

5. [**05 - Power Management, UPS Battery & Power Gate**](docs/en/05_power_management_ups.md)  
   *LM5164-Q1 72V buck, BQ24075 UPS, Front Node LMR36015 / TPS2051B power gate & 1-click CarPlay hard reboot.*

6. [**06 - Telemetry Blackbox, SDIO Ringbuffer & WebDAV Sync**](docs/en/06_telemetry_blackbox_webdav.md)  
   *4-bit high-speed SDIO, GDPR/court-compliant ringbuffer, ECDSA SHA-256, and automated private cloud sync.*

7. [**07 - Hardware Architecture & Board Pinouts (PCBA 01 to 05)**](docs/en/07_pcba_hardware_pinouts.md)  
   *All 5 circuit boards: layer stackup, controlled impedance, net classes, functional zoning, and pinouts.*

8. [**08 - Mechanical Enclosures, CAD & Sealing System**](docs/en/08_enclosures_mechanics_cad.md)  
   *3-piece Central Box, universal satellite pods, modular cartridges, Rear Pod 3, and 4-in-1 Front Node.*

9. [**09 - Firmware Architecture, FreeRTOS & Rollback-OTA**](docs/en/09_firmware_architecture.md)  
   *Multi-core ESP32-S3, RP2040, ESP32-C3, ESP-NOW low-latency protocol (< 1.8 ms), and dual-bank rollback OTA.*

10. [**10 - WebApp PWA & Dashboard Operation**](docs/en/10_webapp_pwa_dashboard.md)  
    *Zero-cloud PWA web app, Web Bluetooth API (WebBLE), vehicle dynamics HUD, and Front Node controls.*

11. [**11 - Digital Simulation & Multi-Physics Master Testbench**](docs/en/11_simulation_testbench.md)  
    *9 modular Python testbenches and 10 HIL scenarios verifying SPICE, thermal, transients, RF, and acoustics.*

12. [**12 - EMC Hardening, RF Shielding & Environmental Protection**](docs/en/12_emv_rf_hardening.md)  
    *Automotive transient immunity (ISO 7637-2), 2.4 GHz vs 868 MHz isolation, IPC-CC-830B coating, and shock damping.*

13. [**13 - Bill of Materials (BOM) & SMT Manufacturing**](docs/en/13_bom_manufacturing.md)  
    *Complete 5-board BOM for JLCPCB SMT production, ordering checklist, wiring harness pigtail, and COTS items.*

14. [**14 - Build Instructions, Wiring & Vehicle Installation**](docs/en/14_build_instructions_assembly.md)  
    *Step-by-step assembly guide, 3D printing parameters (FDM vs. MJF), Front Node mounting, and commissioning.*

15. [**15 - Automotive Standards & Technical References**](docs/en/15_standards_references.md)  
    *Index for ISO 7637-2, ISO 16750, ECE R10, RED 2014/53/EU, IEC 61672-1 Class 1, and Bluetooth SIG.*

16. [**16 - Legal Compliance, Privacy (GDPR) & Licensing**](docs/en/16_legal_compliance_dsgvo.md)  
    *Open-source licenses (GPL-3.0, CERN-OHL-S v2, CC BY-SA 4.0), GDPR compliance, and liability disclaimer.*

---

## 🛠️ Repository Layout

* **`docs/de/`**: Complete technical specifications in German.
* **`docs/en/`**: Complete technical specifications in English.
* **`firmware/main_controller/`**: ESP-IDF / C++ source code for the central main box (ESP32-S3).
* **`firmware/rear_coprocessor/`**: ESP-IDF / C++ source code for the Rear Pod 3 co-processor (ESP32-C3).
* **`webapp_pwa/`**: Zero-cloud offline WebBLE dashboard (HTML5, Vanilla JS, CSS3, Service Worker, i18n).
* **`hardware/`**: KiCad schematics, Gerber files, and 3D enclosure CAD models.

---

## 📜 Licenses

* **Hardware & PCB Layouts:** [CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2) (Strongly Reciprocal)
* **Firmware & Web Dashboard:** [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html)
* **Documentation & 3D Models:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## ⚠️ Liability Disclaimer

All information, schematics, board layouts, 3D printing files, and software published in this project are provided free of charge on an "AS IS" basis. Assembly, installation, and operation occur entirely at the user's own risk. All mentioned brand names (Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay®) are registered trademarks of their respective owners.
