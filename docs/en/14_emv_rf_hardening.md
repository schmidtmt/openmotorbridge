# 14 - EMC, RF, Vibration & Environmental Hardening

This document specifies circuit protections against automotive power transients (ISO 7637-2), RF isolation in the 2.4 GHz and 868 MHz bands, conformal coating (IPC-CC-830B), and mechanical vibration / shock damping (ISO 16750-3).

---

## 1. Automotive Transient & Surge Protection (ISO 7637-2 & ISO 16750-2)

* **Vehicle Network Hardening:** Full compliance with ISO 7637-2 (Pulses 1, 2a, 3a/b up to 100 V) and ISO 16750-2 load dump requirements.
* **Input Protection:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
* **Surge Clamping:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) $\rightarrow$ provides $> 11.7\,\text{V}$ safety headroom to the 65V LM5164 buck regulator.
* **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-channel MOSFET with ultra-low on-resistance ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Filtering & EMI Suppression:** Two-stage LC-PI filter ($10\,\mu\text{H}$ shielded automotive inductor / 3 A + 2x $10\,\mu\text{F}$ X7R 100V ceramic capacitors) at KL30/KL15 input.

---

## 2. RF Isolation & Spatial Diversity

* **2.4 GHz Coexistence (Sena vs. Cardo):** Spatial separation of Pod 1 (left chassis rail) and Pod 2 (right chassis rail) across the metal vehicle frame provides $> 35\,\text{dB}$ free-space attenuation, effectively preventing de-sensing and intermodulation.
* **868 MHz Isolation:** SX1262 LoRa radiates from the rear pod (Pod 3) – $> 1.2\,\text{m}$ away from the side 2.4 GHz mesh units.
* **Shielded Cabling:** Symmetrical 6-conductor PUR shielded cables; shields connect to low-inductance chassis ground at the HD26 flange.

---

## 3. Conformal Coating & Climate Resistance (IPC-CC-830B)

### 3.1 Conformal Coating Specification
* **Material:** Modified polyurethane coating (*Peters Elpeguard SL 1307 FLZ* or *Electrolube UR5041*).
* **Layer Thickness:** $40\,\mu\text{m}$ to $60\,\mu\text{m}$ (measured on flat copper surfaces).
* **Dielectric Strength:** $> 60\,\text{kV/mm}$ (protection against moisture condensation and road salt spray).

### 3.2 Masking Zones Prior to Coating
The following components and contact surfaces must **not** be coated:
1. MicroSD card socket internal spring contacts.
2. 2x13 box header (J1) and outer HD26 flange pins.
3. Mill-Max 6-pin pogo target contact pads on cartridges and pods.
4. SMD test points (TP_5V, TP_3V3, TP_GND).
5. M8 ePTFE pressure equalization vent orifice.

---

## 4. Vibration & Shock Hardening (ISO 16750-3)

### 4.1 Motorcycle Vibration Damping
* **PCB Decoupling:** 4x NBR O-rings (3.0 mm ID, 1.0 mm cord thickness) between enclosure standoffs and PCB bottom mitigate high-frequency engine vibration.
* **Threadlocking:** All M2.5 PCB mounting screws are tightened to $0.35\,\text{Nm}$ and secured with medium-strength threadlocker (*Loctite 243* blue).
* **Component Bonding (Underfill / RTV Silicone):**
  * **Bourns LM-NP-1001 Transformers:** Corners are stabilized with flexible RTV silicone (*Dow Corning 732* / *Dowsil 3145*) to prevent solder joint fatigue.
  * **Buffer Battery:** Full-surface bonding inside upper case with $1.0\,\text{mm}$ vibration-absorbing acrylic foam tape (*3M VHB 4910*).
