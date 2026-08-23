# 05 - Mechanical Construction: Central Box, Sealing Concept & Universal Pods

## 1. Enclosure Type A: Central Control Box (Under Seat)
- **Outer Dimensions:** 95.0 x 65.0 x 24.0 mm (excluding mounting flanges).
- **Material & Process:** PA12 Multi Jet Fusion (MJF) 3D printing, bead-blasted, chemical vapor smoothed in black, and hydrophobically sealed.
- **Ingress Protection:** IP67.

### 1.1 Sandwich Structure & PCB Mount
1. **Base Shell:** Recessed battery compartment (52.0 x 36.0 x 6.5 mm) for the 1000 mAh LiPo battery with NTC sensor, cushioned with 2.0 mm EPDM foam. Four Ruthex M3 x 5.7 mm brass threaded inserts.
2. **Electronics Level:** 4-layer PCB (85.0 x 55.0 mm) mounted on four 4.0 mm standoffs via M3 x 6 mm Torx screws (ISO 14581, A2 stainless steel, Loctite 243).
3. **Top Cover:** Fastened via six M3 x 12 mm socket head cap screws (ISO 4762) with 0.8 Nm torque.

### 1.2 Sealing Concept & Pressure Equalization
- **Tongue-and-Groove O-Ring Gasket:** Solid silicone cord (Shore 45-50 A, D = 1.8 mm), pre-compressed by 30% to 1.25 mm.
- **Pressure Vent:** Gore Automotive Vent AVS 41 with ePTFE membrane (M8 x 1.25 thread).
- **HD26 Wall Flange:** IP67 sealed flange with EPDM flat gasket, decoupled internally via 26-pin ribbon cable to 2x13 box header.

## 2. Enclosure Type B: Universal Satellite Pods (Identical for Pod 1, 2, and 3)
- **Bay Dimensions:** 64.0 x 46.0 x 23.5 mm.
- **Electronics Cartridge:** 54.0 x 37.5 x 17.0 mm (PA12 MJF).
- **Contact Array:** 6-pin Mill-Max spring-loaded Pogo-pin array (Series 824-22-006-00-001101, 2.54 mm pitch, 1.4 mm working stroke) with silicone boot seal against gold-plated ENIG pads.
- **3-Stage Safety Locking:**
  1. *Snap-Lock:* POM-C spring latches with audible click.
  2. *Cam-Lock:* Front-facing 90-degree stainless steel rotary cam latch locks latches positively against $> 20\,\text{g}$ road shocks.
  3. *Push-to-Eject:* Rubberized lever rocker ejects cartridge by 8.0 mm upon unlocking.
- **Mounting:** M5 backplate for flat mounting or CNC pipe clamps (22.0 mm, 28.6 mm, 1 inch handlebars/frame tubes).

## 3. 6-Pin Pogo Pinout Assignment

| Pogo Pin | Pod 1 & 2 (Left / Right: Audio & Intercom) | Pod 3 (Rear: GNSS & OpenMotorMesh LoRa) |
| :---: | :--- | :--- |
| **Pin 1** | **`VCC`** (5V switched supply via MOSFET) | **`VCC`** (5V continuous supply) |
| **Pin 2** | **`GND`** (Dedicated power & signal ground) | **`GND`** (Dedicated power & signal ground) |
| **Pin 3** | **`NF_P`** (Balanced audio signal + via Bourns) | **`UART_TX`** (Rear Co-Processor $\rightarrow$ Central Box) |
| **Pin 4** | **`NF_N`** (Balanced audio signal - via Bourns) | **`UART_RX`** (Central Box $\rightarrow$ Rear Co-Processor) |
| **Pin 5** | **`OPTO`** (TLP222A key simulation trigger) | **`GNSS_PPS`** (1-PPS hardware time reference sync) |
| **Pin 6** | **`1-WIRE_ID`** (DS2401 Silicon Serial Number) | **`1-WIRE_ID`** (DS2401 Rear cartridge detection) |

## 4. Cable Harness Specification (Central Box to Pods)
- **Cable Type:** High-flexibility, oil- and UV-resistant PUR jacket cable with tinned copper braid shield.
- **Conductor Layout:** $2 \times 0.25\,\text{mm}^2$ (VCC / GND for up to 1.0 A charging current) + $4 \times 0.14\,\text{mm}^2$ twisted pairs (Audio/UART, Opto/PPS, 1-Wire ID).
- **Shield Connection:** Overall braided shield connected single-ended to `GND_SHIELD` (Pin 22) on the central control box.
