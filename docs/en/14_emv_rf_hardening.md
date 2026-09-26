# 14 - EMC Hardening, RF Shielding & Environmental Protection

This document specifies the protection circuitry against vehicle electrical transients (ISO 7637-2), RF decoupling across the 2.4 GHz, 868 MHz, and 6.5 GHz UWB bands, conformal coating per IPC-CC-830B, and mechanical vibration isolation according to ISO 16750-3 for the OpenMotorBridge v8.0 Clean Architecture.

---

## 1. Automotive Transient & Overvoltage Protection (ISO 7637-2 & ISO 16750-2)

* **Transient Compliance:** Full conformity to ISO 7637-2 (Pulses 1, 2a, 3a/b up to 100 V) and ISO 16750-2 load dump.
* **Input Fusing:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
* **TVS Clamping:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) $\rightarrow$ maintains $> 11.7\,\text{V}$ margin below the LM5164's 65V limit.
* **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-channel MOSFET in ground return ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **EMI Filtering:** 2-stage LC-PI filter ($10\,\mu\text{H}$ shielded inductor, 3 A + 2x $10\,\mu\text{F}$ X7R 100V ceramics) at KL30/KL15 input.

---

## 2. RF Decoupling, UWB Backbone & Spatial Diversity

* **2.4 GHz Coexistence (Sena vs. Cardo):** Physical separation of Pod 1 (left frame rail / left pannier) and Pod 2 (right frame rail / right pannier) across the metallic chassis provides $> 35\,\text{dB}$ free-space path loss, preventing de-sensing and intermodulation.
* **Deterministic UWB Vehicle Backbone (Qorvo DW3110 / 6.489 GHz Ch. 5):**
  * Wireless backbone linking Front Node (`PCBA 05`) and Central Box (`PCBA 01`).
  * Fully compliant with **ETSI EN 302 065-1, EN 302 065-3**, and **EU Decision 2019/785** ($-41.3\,\text{dBm/MHz}$, continuous legal transmission without duty-cycle capping).
  * Operates across 6.240–6.739 GHz (center frequency 6.489 GHz) with 499.2 MHz bandwidth, far above 2.4 GHz (Wi-Fi, Bluetooth, Mesh) and 5.8 GHz.
  * **Antenna Integration:** Taoglas FXUWB10 flex antenna mounted inside an $11 \times 11 \times 0.6\,\text{mm}$ recess in the enclosure bottom tub floor of both Central Box and Front Node. Connected via 20 mm U.FL micro-coax. The PCB top layer maintains an unbroken solid ground plane (zero keepout cuts), and the enclosure lid can be serviced without cable strain.
* **LoRa 868 MHz (Semtech SX1262) on Central Box (`PCBA 01`):**
  * Integrated directly on the Central Box PCB and buffered 24/7 via the UPS battery rail for uninterrupted theft sentry and group telemetry.
  * Taoglas FXP895 flex antenna ($110 \times 20 \times 0.8\,\text{mm}$) accommodated in a protected lid pocket of the Central Box with $50\,\Omega$ U.FL feed.
* **Multi-GNSS & Sensor Coexistence on Front Node (`PCBA 05`):**
  * u-blox SAM-M10Q with integrated $15 \times 15\,\text{mm}$ ceramic patch antenna, interfaced via Qwiic I2C (`J12`) in the cold ram-air intake zone.
  * Coexistence with TI TMP117 ($\pm 0.1\,^\circ\text{C}$ temperature) and OPT3001 ambient light sensor without RF desensing of the GNSS LNA.
* **Central ePTFE Pressure Equalization Vent:** $\varnothing\,7.0\,\text{mm}$ Gore/Schreiner Air Vent centered on the enclosure roof symmetrically relieves thermal pressure pulses without distorting RF radiation patterns.
* **Shielded HD26 SEAL-D Main Harness:**
  * 4 branches (Whip 1: Pod 1, Whip 2: Pod 2, Whip 4: Vehicle Power, Whip 5: Rear Radar).
  * 19 active pins; pins 9–11 unassigned/reserve.
  * Continuous $360^\circ$ shielding bonded to the metal HD26 enclosure flange.

---

## 3. Conformal Coating & Climatic Resistance (IPC-CC-830B)

### 3.1 Conformal Coating Specification
* **Material:** Modified polyurethane conformal coating (*Peters Elpeguard SL 1307 FLZ* or *Electrolube UR5041*).
* **Layer Thickness:** $40\,\mu\text{m} \dots 60\,\mu\text{m}$ (measured on planar copper areas).
* **Dielectric Breakdown:** $> 60\,\text{kV/mm}$ (reliable protection against condensation, fog, and road salt spray).

### 3.2 Masking Zones Prior to Coating
The following components and contact surfaces must **not** be coated:
1. MicroSD card slot internal spring contacts (PCBA 01).
2. HD26 SEAL-D flange pins & M8 connector pin headers.
3. J12 Qwiic I2C socket contacts on PCBA 05.
4. USB ports (USB-A, USB-C) on Front Node.
5. SMD test points (TP_5V, TP_3V3, TP_GND).
6. ePTFE pressure equalization vent membrane opening.

---

## 4. Vibration & Shock Hardening (ISO 16750-3)

### 4.1 Vibration Isolation on Motorcycle
* **PCB Isolation:** 4x NBR O-rings (ID 3.0 mm, cross-section 1.0 mm) between enclosure bosses and PCB underside dampen high-frequency engine harmonics.
* **Screw Locking:** All M2.5 board screws torqued to $0.35\,\text{Nm}$ and secured with medium-strength threadlocker (*Loctite 243* blue).
* **Component Underfill:**
  * **Bourns LM-NP-1001 Transformer:** Corners anchored with elastomeric silicone adhesive (*Dow Corning 732* / *Dowsil 3145*) to prevent solder fatigue.
  * **UPS Battery Cushioning:** LiPo cell anchored in the upper enclosure tray above the partition plate using $1.0\,\text{mm}$ damping foam (*3M VHB 4910* / EPDM) and an elastic EPDM retention strap (Shore 50A).
