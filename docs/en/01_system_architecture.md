# 01 - System Architecture, Universal Satellite Topology & Acoustics

## 1. Problem Statement & Architectural Philosophy
Traditional motorcycle intercom communication systems are heavily fragmented (Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, PMR446 analog radio, proprietary infotainment units such as Harley-Davidson Boom! Box GTS / Skyline OS). Previous integration attempts failed due to bulky wiring harnesses, poor ergonomics, and severe RF de-sensing caused by co-locating multiple 2.4 GHz transmitters in close proximity.

OpenMotorBridge v8.0 solves this via a **universal 4-point satellite topology**:
- **Central Control Box (Under Seat):** Houses the main MCU (ESP32-S3), UPS power management, SDIO ring buffer, DSP audio mixer, and Bluetooth transceivers. Zero active 2.4 GHz mesh or long-range RF transmitters inside the enclosure.
- **Satellite Pod 1 (Left Chassis Side):** Cartridge bay for primary intercom (e.g. Sena Apex / Spider Mesh 3.0).
- **Satellite Pod 2 (Right Chassis Side):** Cartridge bay for secondary intercom (e.g. Cardo Packtalk Pro / Edge DMC Gen2 or Midland PMR446).
- **Satellite Pod 3 (Rear Fender / Luggage Rack):** Combined unit featuring u-blox MAX-M10S GNSS (unobstructed 360-degree sky view) and OpenMotorMesh transceiver (SX1262 LoRa 868 MHz) with dedicated ESP32-C3 co-processor.
- **Cockpit / Front Area:** 100% wireless via BLE 5.0 (handlebar remote with CR2032 voltage monitoring via SIG Service 0x180F) and an autonomous USB hub in the fairing.

## 2. RF Coexistence & Spatial Diversity
Mounting Pod 1 on the left and Pod 2 on the right side of the motorcycle frame achieves a physical separation of at least 40 to 50 cm. The motorcycle battery, steel/aluminum chassis, and rear fender act as an effective RF shield. This setup guarantees over 35 dB of isolation between the 2.4 GHz mesh transmitters, completely eliminating receiver desensitization and blocking.

## 3. OEM Infotainment Integration (Harley-Davidson Boom! Box GTS & Skyline OS)
- **WHIM Emulation & Apple CarPlay / Android Auto:** OpenMotorBridge emulates an active headset via resistor bias networks, unlocking Apple CarPlay / Android Auto on the Boom! Box GTS display without requiring the expensive OEM HD-WHIM module.
- **Seamless Voice Guidance:** Navigation prompts from the bike infotainment are prioritized by the DSP and blended over intercom conversations using smooth Raised-Cosine ducking.
