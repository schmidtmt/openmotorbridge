# 05 - Mechanical Construction: Central Box, Sealing Concept & Universal Pods

This document specifies the IP67 enclosure design for the central main box (Type A) and the fully universal, vehicle-agnostic satellite pod system (Type B) with modular quick-swap cartridge bays and standard 6-pin Pogo interface.

---

## 1. Enclosure Type A: Central Main Box (Under Seat)
- **External Dimensions:** 96.0 x 66.0 x 43.5 mm (L x W x H).
- **Internal Clearance:** 88.0 x 58.0 mm (PCB footprint 85.0 x 55.0 mm).
- **Material & Manufacturing:** PA12 via HP Multi Jet Fusion (MJF) 3D printing (or UV/fuel resistant ASA via FDM with min. 6 perimeters / 2.4 mm solid walls), glass-bead blasted, black vapor-smoothed, and hydrophobic sealed.
- **Ingress Protection:** IP67 (dust tight, immersion proof up to 1 m water depth).

```
┌────────────────────────────────────────────────────────────┐  ▲
│ 1. LID (3.0 mm wall thickness + M8 ePTFE Vent + Ridge)     │  │
├────────────────────────────────────────────────────────────┤  │ 43.5 mm
│ 2. UPPER TRAY / MID BAFFLE (15.0 mm internal clearance)    │  │ Total
├────────────────────────────────────────────────────────────┤  │ Height
│ 3. LOWER CASE (20.0 mm internal clearance + PCB standoffs) │  │
└────────────────────────────────────────────────────────────┘  ▼
```

### 1.1 Sandwich Construction & PCB Mounting
1. **Lower Case:** Recessed battery pocket (52.0 x 36.0 x 6.5 mm) for LiPo buffer pack (vibration-damped with 3M VHB 4910 foam tape) and NTC thermistor. Four Ruthex M3 x 5.7 mm brass heat-set inserts.
2. **Electronics Tray:** 4-layer PCB (85.0 x 55.0 mm) mounted on four 4.0 mm cylinder standoffs with M2.5 x 5 mm screws (3.6 mm pilot holes with Ruthex M2.5 heat-set inserts) and NBR O-rings for vibration isolation.
3. **Mid Baffle / Upper Tray:** Shields power electronics and battery; 6x ventilation slots (18.0 x 2.5 mm) equalize internal air pressure.
4. **Enclosure Lid:** Bolted through with four M3 x 40/45 mm stainless steel socket head screws (DIN 912 / ISO 4762) into bottom Ruthex M3 brass inserts ($0.8\,\text{Nm}$ torque, secured with *Loctite 243*).

### 1.2 Gasket Concept & Pressure Equalization
- **Perimeter Tongue-and-Groove Gasket:** 2x NBR or silicone cord gaskets (2.0 mm diameter, 50–60 Shore A) in 2.5 x 1.5 mm grooves (25% defined pre-compression).
- **Pressure Equalization Vent:** M8 x 1.25 threaded vent with waterproof ePTFE membrane (Gore Automotive Vent AVS 41 / Schreiner). Airflow $> 120\,\text{ml/min}$ @ 70 mbar, water intrusion point $> 1.5\,\text{bar}$.
- **HD26 Wall Flange:** IP67 D-Sub HD26 flange socket with silicone seal in enclosure wall, internally strain-relieved via 26-conductor ribbon cable to 2x13 box header (J1).

---

## 2. Enclosure Type B: Universal Satellite Pod (Identical for Pods 1, 2, and 3)
- **100% Universal Design:** All 3 pod locations on the motorcycle use the identical, fully universal enclosure body.
- **Bay Dimensions:** 64.0 x 46.0 x 23.5 mm.
- **Cartridge Module:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).
- **Contact Array:** Mill-Max 6-pin pogo pin array (Series 824-22-006-00-001101, 2.54 mm pitch, 1.4 mm working stroke) with silicone boot gasket mating against ENIG pads.
- **3-Stage Locking Mechanism:**
  1. *Snap-Lock:* POM-C spring latches with tactile acoustic click.
  2. *Cam-Lock:* Front 90-degree stainless steel rotating cam lock positively prevents accidental release under $> 20\,\text{g}$ shock loads.
  3. *Push-to-Eject:* Rubberized rocker lever ejects cartridge by 8.0 mm upon unlocking.
- **Universal Mounting:** Integrated M5 backplate for flat mounting, 3M Dual-Lock, or CNC aluminum tube clamps (compatible with all standard tube diameters: 22.0 mm, 28.6 mm, 1.0 inch, and 25–32 mm crash bars).

---

## 3. Universal 6-Pin Pogo Contact Pinout

| Pogo Pin | Pods 1 & 2 (Left / Right: Audio & Intercom Cartridges) | Pod 3 (Rear: GNSS & OpenMotorMesh LoRa) |
| :---: | :--- | :--- |
| **Pin 1** | **`VCC`** (5V switched supply via P-FET) | **`VCC`** (5V continuous supply) |
| **Pin 2** | **`GND`** (Dedicated power & signal ground) | **`GND`** (Dedicated power & signal ground) |
| **Pin 3** | **`NF_P`** (Balanced audio signal + via Bourns) | **`UART_TX`** (Rear Co-Processor $\rightarrow$ Central Box) |
| **Pin 4** | **`NF_N`** (Balanced audio signal - via Bourns) | **`UART_RX`** (Central Box $\rightarrow$ Rear Co-Processor) |
| **Pin 5** | **`OPTO`** (TLP222A button simulation trigger) | **`GNSS_PPS`** (1-PPS hardware time sync) |
| **Pin 6** | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 rear cartridge identification) |

---

## 4. Universal Cable Harness (Central Box to Pods)
- **Cable Type:** High-flexibility, oil- and UV-resistant PUR cable with tinned copper braided shield.
- **Conductors:** $2 \times 0.25\,\text{mm}^2$ (VCC / GND for up to 1 A charging current) + $4 \times 0.14\,\text{mm}^2$ twisted pairs (Audio/UART, Opto/PPS, 1-Wire ID).
- **Shield Termination:** Braided shield terminated low-inductance to `GND_SHIELD` (Pin 22) on central box only.
- **Vehicle Flexibility:** Because the pods share an identical form factor, Pods 1, 2, and 3 can be mounted flexibly on any motorcycle type (Harley-Davidson, BMW GS, KTM, Yamaha, Honda, Ducati, Triumph) on frame rails, crash bars, fairing stays, or luggage racks.
