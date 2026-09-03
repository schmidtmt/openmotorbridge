# 16 - Legal Compliance, Privacy (GDPR) & Licensing

This document defines the open-source licensing model, regulatory radio and automotive frameworks, data protection architecture (GDPR / BGH court rulings), and legal disclaimers for OpenMotorBridge.

---

## 1. Open-Source Licensing Model (Copyleft Focus)

To ensure community contributions (such as OEM-specific CAN and audio adapters for Honda, BMW, Harley, or Yamaha) remain open-source:

* **Firmware & Web Dashboard (Code):** GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html))
* **Hardware Schematics & PCB Layouts (KiCad / Gerber):** CERN Open Hardware Licence Strongly Reciprocal v2 ([CERN-OHL-S v2](https://ohwr.org/project/cernohl/wikis/Documents/CERN-OHL-version-2))
* **3D Printing & CAD Models (STEP, STL):** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
* **Documentation & Specifications:** Creative Commons Attribution-ShareAlike 4.0 ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))

---

## 2. Regulatory Radio Frameworks (RED 2014/53/EU & FCC Part 15)

OpenMotorBridge operates exclusively within standardized, globally license-free frequency bands:

* **2.4 GHz ISM Band:** Maximum 100 mW EIRP (20 dBm) in the EU (ETSI EN 300 328) and 1000 mW in the US (FCC Part 15). Harmonized worldwide without duty-cycle restrictions when using FHSS/DSSS.
* **868 MHz SRD Band (Sub-GHz LoRa):** Governed by ETSI EN 300 220. Restricted by statutory duty cycles (0.1% to 10% in Europe), utilized strictly for GPS radar and brief Push-to-Talk (PTT) voice bursts via Codec2 (1200 bps).
* **446 MHz (PMR446 - Optional Cartridges):** 500 mW ERP maximum with 12.5 kHz channel spacing in half-duplex simplex operation.

---

## 3. Vehicle Type Approval & E-Marking (ECE R10 Rev. 6)

* **Pre-Certified Transceivers:** Integrating off-the-shelf, certified OEM modules (e.g., Sena MeshPort Blue, Cardo Packtalk) preserves primary radio certification with the original manufacturer.
* **Non-Intrusive Listen-Only Interfacing:** The Central Box and Front Node interface with the motorcycle harness solely through galvanic isolators (Bourns 1500 V RMS transformers, Toshiba PhotoMOS relays, optocouplers) and passive CAN listening. **No commands are written to safety-critical ECUs (Engine ECU, ABS, Traction Control)**.

---

## 4. Privacy by Design & GDPR Compliance (BGH VI ZR 233/17)

* **Event-Driven Logging:** Telemetry and GPS data are stored exclusively on the internal local MicroSD card in a rolling ringbuffer.
* **Cyclic Auto-Purge:** Unprotected tracks are automatically purged when free space drops below 200 MB.
* **Zero Cloud Lock-in:** No central server infrastructure or data collection exists. Optional WebDAV uploads operate strictly over encrypted TLS 1.3 to the user's private NAS/cloud (Nextcloud/Synology).

---

## 5. Legal Disclaimer

### 5.1 "AS-IS" Warranty Disclaimer
The schematics, board layouts, 3D CAD files, firmware source code, and installation instructions published in this project are provided "AS IS" without warranty of any kind, either express or implied.

### 5.2 Limitation of Liability
Assembly, installation, and operation of this hardware and software occur entirely at the user's own risk. The author and contributors assume no liability for damages to vehicles, electrical harnesses, batteries, or connected devices, nor for any accidents or consequential damages.

### 5.3 Trademarks
Harley-Davidson®, BMW®, Garmin®, Sena®, Cardo®, Apple CarPlay®, Android Auto®, and other brand names mentioned are registered trademarks of their respective owners. This project is independent and has no official affiliation with these corporations.
