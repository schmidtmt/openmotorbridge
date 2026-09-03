# 12 - EMC Hardening, RF Shielding & Environmental Protection

This document specifies the protection circuitry against vehicle electrical transients (ISO 7637-2), RF decoupling across the 2.4 GHz and 868 MHz bands, conformal coating per IPC-CC-830B, and mechanical vibration isolation according to ISO 16750-3.

---

## 1. Automotive Transient & Overvoltage Protection (ISO 7637-2 & ISO 16750-2)

* **Transient Compliance:** Full conformity to ISO 7637-2 (Pulses 1, 2a, 3a/b up to 100 V) and ISO 16750-2 load dump.
* **Input Fusing:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
* **TVS Clamping:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) $\rightarrow$ maintains $> 11{,}7\,\text{V}$ margin below the LM5164's 65V limit.
* **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-channel MOSFET in ground return ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **EMI Filtering:** 2-stage LC-PI filter ($10\,\mu\text{H}$ shielded inductor, 3 A + 2x $10\,\mu\text{F}$ X7R 100V ceramics).

---

## 2. RF Decoupling & Spatial Diversity

* **2.4 GHz Coexistence (Sena vs. Cardo):** Physical separation of Pod 1 (left frame rail) and Pod 2 (right frame rail) across the metallic chassis provides $> 35\,\text{dB}$ free-space path loss, preventing de-sensing and intermodulation.
* **Rear Pod 3 Tri-RF Architecture:**
  * **2.4 GHz ESP32-C3 PCB Antenna:** Placed at the front edge in a $15 \times 8\,\text{mm}$ copper keepout area.
  * **868 MHz LoRa Helical Antenna:** Lateral mount with $50\,\Omega$ microstrip feed and dedicated $60 \times 36\,\text{mm}$ ground plane ($> -1{,}5\,\text{dBi}$ gain).
  * **u-blox Multi-GNSS Ceramic Patch ($25 \times 25 \times 4\,\text{mm}$):** Centered with an unobstructed $180^\circ$ hemispherical sky view through the RF-transparent PA12 ceiling ($\varepsilon_r \approx 3{,}2$).
* **Central ePTFE Pressure Equalization Vent:** $\varnothing\,7{,}0\,\text{mm}$ Gore/Schreiner Air Vent centered on the pod roof symmetrically relieves thermal pressure pulses without distorting RF radiation patterns.
* **Shielded Harnessing:** All pod interconnects use 6-conductor shielded PUR cables with continuous 360° shield bonding at M8 and HD26 metal flanges.

---

## 3. Conformal Coating & Climatic Resistance (IPC-CC-830B)

* **Material:** Modified polyurethane conformal coating (*Peters Elpeguard SL 1307 FLZ* or *Electrolube UR5041*).
* **Layer Thickness:** $40\,\mu\text{m} \dots 60\,\mu\text{m}$ (dielectric breakdown $> 60\,\text{kV/mm}$ against fog and road salt).
* **Masking Zones:** MicroSD slot internal contacts, 2x13 box header, pogo contact pads, test points, and ePTFE vent openings.

---

## 4. Vibration & Shock Hardening (ISO 16750-3)

* **PCB Isolation:** 4x NBR O-rings (ID 3.0 mm, cross-section 1.0 mm) between enclosure bosses and PCB underside.
* **Screw Locking:** M2.5 board screws torqued to $0{,}35\,\text{Nm}$ and secured with medium-strength threadlocker (*Loctite 243* blue).
* **Component Underfill:** Bourns LM-NP-1001 transformer corners anchored with elastomeric silicone adhesive (*Dow Corning 732* / *Dowsil 3145*).
* **Battery Cushioning:** LiPo UPS cell anchored in the upper enclosure tray with $1{,}0\,\text{mm}$ vibration damping foam (*3M VHB 4910* / EPDM) and an elastic EPDM retention strap (Shore 50A).
