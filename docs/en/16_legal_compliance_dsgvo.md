# 16 - Legal Compliance, Licensing, RF Regulations & GDPR

This document defines the open-source licensing model, regulatory RF and automotive compliance frameworks, data privacy architecture, and the legal liability disclaimer for the OpenMotorBridge project.

---

## 1. Open-Source Licensing Model (Copyleft Focus)

To ensure that future developments and vehicle-specific adaptations (e.g. custom CAN-bus or audio adapters for Honda, BMW, or Yamaha) remain open source and flow back to the community, this project is released under the following licenses:

* **Firmware & Web Dashboard (Code):** GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html))
* **Hardware & PCB Layouts (KiCad / Gerber):** CERN Open Hardware Licence Strongly Reciprocal v2 ([CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2))
* **3D Printing & CAD Models (STEP, STL, Enclosure Data):** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
* **Documentation & Specifications:** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))

---

## 2. Regulatory Frameworks & RF Certification (RED 2014/53/EU & FCC Part 15)

OpenMotorBridge utilizes exclusively standardized, globally license-free frequency bands:

* **2.4 GHz ISM Band:** Maximum 100 mW EIRP (20 dBm) in the EU (ETSI EN 300 328) / 1000 mW in the USA (FCC Part 15). The band is globally harmonized and has **no duty-cycle restrictions** when using FHSS/DSSS/LBT (enabling continuous full-duplex voice).
* **868 MHz SRD Band (Sub-GHz LoRa):** Governed by ETSI EN 300 220. Due to statutory duty-cycle limits (0.1% to 10%) in Europe, this band is not intended for continuous audio streaming (1% = max. 36 seconds airtime per hour; 10% High-Power = max. 360 seconds airtime per hour). In OMB, it is purposefully utilized for GPS group radar pings and short push-to-talk (PTT) voice messages using Codec2 (1200 bps).
* **446 MHz (PMR446 - Optional Cartridges):** Maximum 500 mW ERP with 12.5 kHz channel raster in half-duplex simplex mode, adhering to fixed antenna regulations.

---

## 3. Automotive Type Approval, CE Compliance & E-Marking (ECE R10 Rev. 6)

* **CE & RED Compliance:** Using pre-assembled, certified OEM modules (e.g. Sena MeshPort Blue or Cardo Packtalk cartridges) maintains primary wireless certification with the original manufacturer.
* **DIY Builds & Kits:** Assembling and operating uncertified transmitter hardware extensions via the expansion port is done under the user's own responsibility within national amateur radio or ISM regulations.
* **Automotive Type Approval & ECE R10 Rev. 6:** The central unit interfaces harmlessly with the motorcycle board network via galvanic isolation stages (Bourns 1500 V RMS transformers, Toshiba PhotoMOS relays) and listen-only CAN-bus monitoring. **No active write interventions are made into safety-critical control units (ECU, ABS, traction control).**

---

## 4. Data Privacy & GDPR / BGH Compliance (BGH VI ZR 233/17)

* **Event-Driven Logging:** Telemetry and GPS data are stored exclusively locally on the internal MicroSD card in a rolling ring buffer.
* **Automatic Overwrite:** Unprotected tracks and buffer segments are cyclically overwritten when the free storage threshold (< 200 MB) is reached.
* **Zero-Cloud Requirement:** No central server infrastructure or third-party telemetry collection exists. Optional WebDAV synchronization occurs exclusively encrypted (TLS 1.3) to private, user-configured storage (Nextcloud/Synology).

---

## 5. Legal Liability Disclaimer

### 5.1 Provided "AS-IS" (Without Warranty)
All schematics, board layouts, 3D printing files, source code, and installation guides published in this project are provided free of charge on an "AS IS" basis. No warranties or guarantees regarding function, reliability, completeness, or freedom from defects are provided.

### 5.2 Limitation of Liability for Vehicle & Property Damage
Assembly, installation, and operation of this hardware and software occur entirely at the user's own risk. The author and contributors accept no liability for damage to vehicles, onboard electronics, control units (CAN-bus), batteries, or connected devices, nor for consequential damages or accidents arising from the use or improper installation of this system.

### 5.3 Material & Manufacturing Notes (3D Printing / Components)
Recommended materials (e.g. PA12 MJF, ASA) and manufacturing instructions represent non-binding empirical guidance. Thermal, chemical (fuel/oil resistance), and mechanical resilience depend heavily on individual print parameters, filament quality, and proper assembly.

### 5.4 Road Traffic Regulations & RF Laws
This device does not hold a general E-mark / ABE type approval for public road use. The operator is solely responsible for ensuring compliance with applicable national laws regarding radio frequencies, maximum transmit power, and vehicle modifications.

### 5.5 Trademarks & Brand Names
Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay®, and other mentioned brand names are registered trademarks of their respective owners. This project is not affiliated with or endorsed by any of these companies.
