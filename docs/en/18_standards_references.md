# 18 - Standards & Reference Norms

This document catalogs all international automotive, RF, environmental, and protocol standards applied in the design, testing, and documentation of **OpenMotorBridge v8.0**.

---

## 1. Automotive, EMC, Safety & Enclosure Norms

* **ISO 7637-2:2011:** *Road vehicles — Electrical disturbances from conduction and coupling — Part 2: Electrical transient conduction along supply lines only* (Pulse 1, 2a, 3a/b and load-dump protection).
* **ISO 16750-2:2012:** *Road vehicles — Environmental conditions and testing for electrical and electronic equipment — Part 2: Electrical loads* (Overvoltage, cold crank, and reverse polarity testing).
* **ISO 16750-3:2012:** *Road vehicles — Environmental conditions and testing for electrical and electronic equipment — Part 3: Mechanical loads* (Random vibration and shock profiles for two-wheelers/motorcycles).
* **ECE R10 Rev. 6:** *Uniform provisions concerning the approval of vehicles with regard to electromagnetic compatibility* (Type-approval compliance for automotive accessories in listen-only mode).
* **DIN EN 60529 (VDE 0470-1):2014-09:** *Degrees of protection provided by enclosures (IP Code)* (IP67: Dust-tight & continuous immersion up to 1m; IP69K: High-pressure/steam-jet washdown).
* **DIN ISO 2768-m:** *General tolerances for linear and angular dimensions* (Manufacturing tolerances for 3D printing, CNC machining, and enclosure fitments).
* **UL 94 V-0:** *Standard for Tests for Flammability of Plastic Materials for Parts in Devices and Appliances* (Self-extinguishing materials for PA12 MJF, seals, and circuit boards).
* **AEC-Q100 / AEC-Q200:** *Failure Mechanism Based Stress Test Qualification For Integrated Circuits / Passive Components* (Automotive qualification of LM5164, TCAN334G, and passives).
* **IPC-CC-830B / IPC-A-610G Class 3:** *Qualification and Performance of Electrical Insulating Compounds for Printed Wiring Assemblies* (Conformal coating standards and solder joint reliability).

---

## 2. Radio, Wave Propagation & Telecommunications Standards

* **RED 2014/53/EU:** *Radio Equipment Directive* (European Radio Equipment Directive for CE compliance).
* **ETSI EN 300 328 v2.2.2:** *Wideband transmission systems; Data transmission equipment operating in the 2,4 GHz ISM band* (Power limits up to 100 mW EIRP, FHSS/DSSS spread spectrum).
* **ETSI EN 300 220-2 v3.2.1:** *Short Range Devices (SRD) operating in the frequency range 25 MHz to 1 000 MHz* (LoRa 868 MHz Sub-GHz band, duty-cycle limits 1% / 10%).
* **ETSI EN 301 489-1 / -3 / -17:** *ElectroMagnetic Compatibility (EMC) standard for radio equipment and services* (Harmonized EMC standards for short-range devices and wideband systems).
* **FCC Part 15 Subpart C / B:** *Title 47 CFR Part 15 — Radio Frequency Devices* (US regulatory compliance for unlicensed intentional and digital radiators).
* **3GPP TS 36.331 / TS 36.213 (Release 14/15 Sidelink C-V2X / ProSe):** *E-UTRA; Physical layer procedures / Radio Resource Control* (Reference for SC-FDMA TDMA superframe structure in OpenMotorMesh).
* **ITU-R P.838 / P.840:** *Specific attenuation model for rain / fog for use in prediction methods* (Atmospheric and precipitation attenuation models used in 2.4 GHz and 868 MHz simulations).

---

## 3. Protocol, Bus & Interface Specifications

* **Bluetooth SIG:**
  * *Battery Service Specification v1.0* (GATT UUID `0x180F`, Battery Level Characteristic `0x2A19`).
  * *Adopted Bluetooth Core Specification v5.0 / v5.2* (LE 2M PHY & Long Range Coded PHY).
* **u-blox AG:** *u-blox M10 SPG 5.10 Interface Description* (Doc No. UBX-21035062, UBX/NMEA 10 Hz PVT & 1-PPS Timecode).
* **Semtech Corporation:** *SX1261/2 Long Range Low Power Sub-GHz Transceiver Datasheet* (DS.SX1261-2.W.APP).
* **Maxim Integrated / Analog Devices:** *DS2401 Silicon Serial Number 1-Wire ROM Specification* (64-Bit Unique Identification).
* **Philips Semiconductors (NXP):** *I2S Bus Specification* (Inter-IC Sound 48 kHz / 24 Bit Audio DMA).
* **USB-IF:** *Universal Serial Bus Mass Storage Class (MSC) Bulk-Only Transport v1.0*.
* **Cardo Systems:** *Dynamic Mesh Communications (DMC 2.0 Open Intercom Operational Guidelines)*.
* **Sena Technologies:** *Mesh 2.0 / 3.0 Intercom Network Architecture Reference*.

---

## 4. Privacy, Legal & Open-Source Licenses

* **BGH Ruling VI ZR 233/17 (May 15, 2018):** *Admissibility of event-driven dashcam and telemetry recordings in road traffic* (Legal foundation for the rolling ringbuffer).
* **GDPR (EU Regulation 2016/679):** *Art. 5 (Data minimization & storage limitation)* and *Art. 25 (Privacy by Design and by Default)*.
* **GNU General Public License v3.0 (GPL-3.0):** Open-source license for firmware source code and PWA dashboard.
* **CERN Open Hardware Licence Strongly Reciprocal v2 (CERN-OHL-S v2):** Open-source hardware license for schematics and PCB layouts.
* **Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0):** License for 3D CAD models and technical specifications.
