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

The comprehensive technical specification is split into 17 modular chapters:

1. [**01 - System Architecture & Satellite Topology**](docs/en/01_system_architecture.md)  
   *Overview of the 4-point architecture, spatial RF diversity, and multi-domain concept.*

2. [**02 - PCB Hardware & HD26 Pinout**](docs/en/02_pcb_hardware_pinout.md)  
   *Main board schematic, ESP32-S3 GPIO mapping, and the 26-pin IP67 enclosure interface.*

3. [**03 - Isolated Audio Frontend & Level Matching**](docs/en/03_audio_frontend_isolated.md)  
   *Galvanic isolation via Bourns audio transformers and PhotoMOS PTT simulation (TLP222A).*

4. [**04 - Automotive Power Management & UPS**](docs/en/04_power_management_ups.md)  
   *LM5164-Q1 buck regulator, BQ24075 UPS with JEITA NTC monitoring, and 5 battery profiles.*

5. [**05 - Mechanical Enclosure & Modular Cartridges**](docs/en/05_mechanical_enclosure_pods.md)  
   *IP67 enclosure concept (Type A central box, Type B pods) in PA12 MJF with Mill-Max pogo bays.*

6. [**06 - Dynamic Profiles & 1-Wire DS2401 Detection**](docs/en/06_dynamic_profiles_spec.md)  
   *Automatic cartridge hardware detection via DS2401 Silicon Serial Number and LittleFS JSON profiles.*

7. [**07 - MicroSD BGH Ring Buffer & WebDAV Sync**](docs/en/07_microsd_bgh_webdav.md)  
   *4-Bit SDIO FAT32 filesystem, GDPR-compliant ring buffer logging, and encrypted TLS 1.3 sync.*

8. [**08 - DSP Audio Engine & Raised-Cosine Ducking**](docs/en/08_dsp_audio_engine.md)  
   *I2S DMA audio pipeline, raised-cosine crossfading, speed-dependent gain, and Codec2 encoding.*

9. [**09 - Firmware Architecture & FreeRTOS Design**](docs/en/09_firmware_architecture.md)  
   *Dual-core FreeRTOS task architecture, lockless ring buffers, and task supervisors.*

10. [**10 - Web Bluetooth Dashboard & PWA Architecture**](docs/en/10_web_bluetooth_dashboard.md)  
    *Zero-cloud PWA web app, Web Bluetooth API (WebBLE), vehicle dynamics HUD, and i18n switcher.*

11. [**11 - OpenMotorMesh (OMM), DLE & Cluster Relay**](docs/en/11_openmotormesh_dle_election.md)  
    *Dual-PHY (2.4 GHz Sidelink + 868 MHz LoRa), Adaptive QoS, DLE scoring, and cluster relay.*

12. [**12 - GNSS Multi-Constellation, ADR & Video Sync**](docs/en/12_gnss_track_lifecycle_video.md)  
    *u-blox MAX-M10S, 15-state EKF dead reckoning, map-matching, and Actioncam Smart Remote control.*

13. [**13 - Rear Pod 3 & Digital Transceiver Architecture**](docs/en/13_rear_pod3_transceiver_arch.md)  
    *Rear pod integration of GNSS, SX1262 LoRa 868 MHz, and ESP32-C3 RISC-V co-processor.*

14. [**14 - EMC, RF & Environmental Hardening**](docs/en/14_emv_rf_hardening.md)  
    *Automotive transient protection, conformal coating (IPC-CC-830B), and 35 dB chassis isolation.*

15. [**15 - Bill of Materials (BOM) & Manufacturing**](docs/en/15_bom_manufacturing.md)  
    *Complete 3-tier BOM for JLCPCB SMT assembly (Main Box, Rear Pod 3, Cartridges) & CPL parameters.*

16. [**16 - Simulation & Digital Testbench**](docs/en/16_simulation_testbench.md)  
    *Automotive Simulation Suite: Audio DSP, Raised-Cosine Ducking, Power Management, 15-State ADR-EKF & 1-Wire.*

17. [**17 - Legal Compliance, Licensing, Regulations & GDPR**](docs/en/17_legal_compliance_dsgvo.md)  
    *ECE R10, RED 2014/53/EU compliance, RF spectrum regulations, open-source licenses & disclaimer.*

18. [**18 - Standards & Normative References**](docs/en/18_standards_references.md)  
    *Reference index for ISO 7637-2, Bluetooth SIG Battery Service (0x180F), and intercom protocols.*

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
