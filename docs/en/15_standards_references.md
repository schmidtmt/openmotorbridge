# 15 - Automotive Standards & Technical References

This document lists all international automotive, industry, radio frequency, and protocol standards under which **OpenMotorBridge v8.0** is engineered, verified, and documented.

---

## 1. Automotive, EMC, Safety & Enclosure Standards

* **ISO 7637-2:2011:** *Road vehicles — Electrical disturbances from conduction and coupling — Part 2: Electrical transient conduction along supply lines only* (Pulses 1, 2a, 3a/b and load-dump protection up to 100 V).
* **ISO 16750-2:2012:** *Road vehicles — Environmental conditions and testing for electrical and electronic equipment — Part 2: Electrical loads* (Overvoltage, cold crank, reverse polarity testing).
* **ISO 16750-3:2012:** *Road vehicles — Environmental conditions and testing for electrical and electronic equipment — Part 3: Mechanical loads* (Broadband random vibration and mechanical shock testing up to 20 g).
* **ECE R10 Rev. 6:** *Uniform provisions concerning the approval of vehicles with regard to electromagnetic compatibility* (Type-approval conformity for aftermarket automotive electronics in listen-only mode).
* **DIN EN 60529 (VDE 0470-1):2014-09:** *Degrees of protection provided by enclosures (IP Code)* (IP67: Dust-tight and temporary submersion to 1 m; IP69K: High-pressure/steam-jet washdown).
* **DIN ISO 2768-m:** *General tolerances for linear and angular dimensions* (Manufacturing tolerances for 3D printing and machining).
* **UL 94 V-0:** *Standard for Tests for Flammability of Plastic Materials for Parts in Devices and Appliances* (Self-extinguishing materials for PA12 MJF enclosures and PCBs).
* **AEC-Q100 / AEC-Q200:** *Failure Mechanism Based Stress Test Qualification For Integrated Circuits / Passive Components* (Automotive qualification for LM5164, LMR36015, TCAN334G).
* **IPC-CC-830B / IPC-A-610G Class 3:** *Qualification and Performance of Electrical Insulating Compounds for Printed Wiring Assemblies* (Conformal coating standards and high-reliability soldering).

---

## 2. Radio, Wave Propagation & Telecommunications Standards

* **RED 2014/53/EU:** *Radio Equipment Directive* (European regulatory framework for CE radio equipment).
* **ETSI EN 300 328 v2.2.2:** *Wideband transmission systems; Data transmission equipment operating in the 2.4 GHz ISM band* (EIRP limits to 100 mW, FHSS/DSSS spread spectrum).
* **ETSI EN 300 220-2 v3.2.1:** *Short Range Devices (SRD) operating in the frequency range 25 MHz to 1 000 MHz* (LoRa 868 MHz Sub-GHz band duty cycle limits: 1% / 10%).
* **ETSI EN 301 489-1 / -3 / -17:** *ElectroMagnetic Compatibility (EMC) standard for radio equipment and services*.
* **FCC Part 15 Subpart C / B:** *Title 47 CFR Part 15 — Radio Frequency Devices* (US regulatory rules for unlicensed intentional and unintentional radiators).
* **3GPP TS 36.331 / TS 36.213 (Release 14/15 Sidelink C-V2X / ProSe):** *E-UTRA; Physical layer procedures / Radio Resource Control* (Reference for SC-FDMA TDMA slot structure in OpenMotorMesh).
* **ITU-R P.838 / P.840:** *Specific attenuation model for rain / fog for use in prediction methods* (Atmospheric path loss modeling for 2.4 GHz and 868 MHz).

---

## 3. Protocol, Bus & Interface Specifications

* **Bluetooth SIG:** *Battery Service Specification v1.0* (GATT UUID `0x180F`) and *Adopted Bluetooth Core Specification v5.0 / v5.2*.
* **u-blox AG:** *u-blox M10 SPG 5.10 Interface Description* (Doc UBX-21035062, UBX/NMEA 10 Hz PVT & 1-PPS Timecode).
* **Semtech Corporation:** *SX1261/2 Long Range Low Power Sub-GHz Transceiver Datasheet* (DS.SX1261-2.W.APP).
* **Maxim Integrated / Analog Devices:** *DS2401 Silicon Serial Number 1-Wire ROM Specification* (64-Bit UID).
* **Philips Semiconductors (NXP):** *I2S Bus Specification* (Inter-IC Sound 48 kHz / 24 Bit Audio DMA).
* **USB-IF:** *Universal Serial Bus Specification v2.0 High-Speed (480 Mbps)* and *USB Mass Storage Class (MSC) Bulk-Only Transport v1.0*.
* **Cardo Systems:** *Dynamic Mesh Communications (DMC 2.0 Operational Guidelines)*.
* **Sena Technologies:** *Mesh 2.0 / 3.0 Intercom Network Architecture Reference*.

---

## 4. Acoustics & Audio Standards

* **IEC 61672-1:2013:** *Electroacoustics — Sound level meters — Part 1: Specifications* (Class 1 A-Weighting filter curve for Knowles MEMS SPL tracking).
* **ITU-T P.862 / P.863:** *Perceptual evaluation of speech quality (PESQ/POLQA)* (Benchmark for speech intelligibility metrics in wind tunnel testing).
