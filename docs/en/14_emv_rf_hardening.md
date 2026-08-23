# 14 - EMC, RF Hardening & Environmental Resistance

Motorcycle environments present severe electrical and climatic stresses (ignition pulses, alternator load dumps, extreme engine heat, winter road salt, high-pressure jet washers).

## 1. Automotive Transient Hardening
- **ISO 7637-2 / ISO 16750-2 Compliance:** The central box features a multi-stage input filter with an SMBJ33CA TVS diode and Bourns PPTC resettable fuse, protecting against 100V transients and load dump spikes.
- **Reverse Polarity:** DMP6023L P-MOSFET gate prevents damage from reverse battery connections during maintenance.

## 2. RF Hardening & De-Sensing Prevention
- **Spatial Separation:** $> 40\,\text{cm}$ physical distance between Pod 1 and Pod 2 yields $> 35\,\text{dB}$ of chassis attenuation.
- **RF-Hardening Configuration:** Cartridge JSON profiles enforce "Bluetooth Classic OFF" to eliminate in-band 2.4 GHz channel collisions.

## 3. Environmental Protection (IPC-CC-830B & IP67)
- **Conformal Coating:** All PCB assemblies are coated with acrylic conformal coating per IPC-CC-830B (resistant to humidity, vibration, and road salt).
- **IP67 Sealing:** Pre-compressed silicone gaskets and Gore-Tex pressure equalization vents prevent condensation build-up inside enclosures.
