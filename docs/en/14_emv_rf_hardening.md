# 14 - EMC Hardening, RF Shielding & Environmental Protection

This document specifies the protection circuitry against vehicle electrical transients (ISO 7637-2), EMC hardening of the shielded 4-wire automotive USB bus, RF decoupling across the 2.4 GHz, 868 MHz, 5.9 GHz, and 77 GHz bands, conformal coating per IPC-CC-830B, and mechanical vibration isolation according to ISO 16750-3 for the OpenMotorBridge v10.0 Standardized Node Architecture.

---

## 1. Automotive Transient & Overvoltage Protection (ISO 7637-2 & ISO 16750-2)

* **Transient Compliance:** Full conformity to ISO 7637-2 (Pulses 1, 2a, 3a/b up to 100 V) and ISO 16750-2 load dump.
* **Input Fusing:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
* **TVS Clamping:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) $\rightarrow$ maintains $> 11.7\,\text{V}$ margin below the LM5164's 65V limit.
* **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-channel MOSFET in ground return ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **EMI Filtering:** 2-stage LC-PI filter ($10\,\mu\text{H}$ shielded inductor, 3 A + 2x $10\,\mu\text{F}$ X7R 100V ceramics) at KL30/KL15 input.

---

## 2. RF Decoupling, 4-Wire Automotive Bus & EMC Hardening

* **2.4 GHz Coexistence (Sena vs. Cardo vs. OMM):** Physical separation of Pod 1 (left pannier) and Pod 2 (right pannier) across the metallic chassis provides $> 35\,\text{dB}$ free-space path loss, preventing de-sensing and intermodulation.
* **Shielded 4-Wire Automotive Bus (Replacement of UWB):**
  * In v10.0, the experimental 6.5 GHz UWB subsystem (DW3110) has been eliminated. Communication between Central Box (`PCBA 01`), saddlebag pods (`PCBA 03`), and Front Node (`PCBA 05`) runs over a rugged, shielded **4-wire automotive bus** (`VCC_BUS` 12V/PD, `GND`, `USB_D-`, `USB_D+`).
  * **Common-Mode Chokes:** Differential USB data lines ($90\,\Omega$ differential impedance) are filtered by Murata DLW21SN900HQ2L common-mode chokes ($90\,\Omega$ @ $100\,\text{MHz}$), rejecting high-frequency noise from alternators and switched-mode converters.
  * **TVS ESD Protection:** Every port is protected by STMicroelectronics USBLC6-2SC6 / Littelfuse SP3012 arrays (parasitic capacitance $< 0.5\,\text{pF}$, $\pm 15\,\text{kV}$ air / $\pm 8\,\text{kV}$ contact ESD per IEC 61000-4-2 Level 4).
  * **Star Grounding & Dual-Power Protection:** Power ground (`PGND`) is strictly isolated from sensitive audio ground (`AGND`). On `PCBA 01`, a TI LM5050 ideal-diode controller blocks reverse currents between 12V vehicle power and the benchtop USB-PD sink.
* **LoRa 868 MHz (Semtech SX1262) & Wi-Fi/BLE (ESP32-S3) on Central Box (`PCBA 01`):**
  * SX1262 LoRa transceiver buffered 24/7 via the UPS battery rail for uninterrupted theft sentry and group telemetry.
  * **Hinged Battery & Dual-Antenna Bridge:** Taoglas FXP895 LoRa-868 flex antenna ($86 \times 16 \times 1.0\,\text{mm}$) and Taoglas FXP73 2.4 GHz flex antenna ($47 \times 7.5 \times 0.8\,\text{mm}$) housed in form-fitting recessed pockets under a $0.8\,\text{mm}$ snap-on PA12 protective cover plate with C-clip strain-relief clamps. The enclosure lid remains 100% passive and cable-free.
  * **Rear SMA Port Knockout Membrane:** Molded with a $0.4\,\text{mm}$ PA12 knockout membrane, keeping the enclosure 100% sealed (IP68/IP69K) by default while allowing quick punch-out for an external SMA antenna on carbon fiber or rally bikes.
* **Multi-GNSS & Sensor Coexistence on Front Node (`PCBA 05`):**
  * u-blox SAM-M10Q with integrated $15 \times 15\,\text{mm}$ ceramic patch antenna, interfaced via Qwiic I2C (`J12`) in the cold ram-air intake zone.
  * Coexistence with TI TMP117 ($\pm 0.1\,^\circ\text{C}$ temperature) and OPT3001 ambient light sensor without RF desensing of the GNSS LNA.
* **Central ePTFE Pressure Equalization Vent:** $\varnothing\,7.0\,\text{mm}$ Gore/Schreiner Air Vent centered on the enclosure roof symmetrically relieves thermal pressure pulses without distorting RF radiation patterns.
* **Robust Deutsch DTM-12 Main Harness:**
  * All 12 pins assigned per DTM-12 pinout table (Pins 1–5, 12 for Branch 4 / Vehicle & CAN; Pins 6–7 for Branch 1 / Pod 1; Pins 8–9 for Branch 2 / Pod 2; Pins 10–11 for Branch 3 / Rear Radar).
  * Continuous IP68/IP69K sealing with Raychem DR-25 heatshrink and molded boots.

---

## 3. Conformal Coating & Climatic Resistance (IPC-CC-830B)

### 3.1 Conformal Coating Specification
* **Material:** Modified polyurethane conformal coating (*Peters Elpeguard SL 1307 FLZ* or *Electrolube UR5041*).
* **Layer Thickness:** $40\,\mu\text{m} \dots 60\,\mu\text{m}$ (measured on planar copper areas).
* **Dielectric Breakdown:** $> 60\,\text{kV/mm}$ (reliable protection against condensation, fog, and road salt spray).

### 3.2 Masking Zones Prior to Coating
The following components and contact surfaces must **not** be coated:
1. MicroSD card slot internal spring contacts (PCBA 01).
2. Deutsch DTM-12 header pins & gold-plated spring contacts.
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
  * **UPS Battery Cushioning:** LiPo cell anchored in the upper enclosure tray above the partition plate using $1.0\,\text{mm}$ damping foam (*3M VHB 4910* / EPDM) and an elastic EPDM retention strap (Shore 50A).
