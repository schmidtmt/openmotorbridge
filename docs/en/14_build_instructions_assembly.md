# 14 - Build Instructions, Wiring & Vehicle Installation

This document is the comprehensive, hands-on assembly guide for building a complete **OpenMotorBridge (v8.0)** hardware kit for a motorcycle. It details 3D printing parameters, mechanical assembly, cable harnessing, Front Node installation, and the step-by-step commissioning checklist.

---

## 1. Kit Architecture Overview

A complete OpenMotorBridge motorcycle installation comprises:

```
                      ┌─────────────────────────────────────────┐
                      │    1x CENTRAL MAIN BOX (IP67)           │
                      │    (Under-seat / tail frame)            │
                      │    • Lower case + mid tray + lid        │
                      │    • Main PCB (ESP32-S3, Codec, UPS)    │
                      │    • Integrated LiPo backup battery     │
                      └────────────────────┬────────────────────┘
                                           │
                        1x CENTRAL HARNESS (HD26 IP67)
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐              ┌──────────────────┐
│ 1x POD 1 (LEFT)  │             │ 1x POD 2 (RIGHT) │              │ 1x POD 3 (TAIL)  │
│ (Frame / Bar)    │             │ (Frame / Bar)    │              │ (Tail Cowl)      │
│ • Pod Enclosure  │             │ • Pod Enclosure  │              │ • Pod Enclosure  │
│ • Baseboard      │             │ • Baseboard      │              │ • Baseboard      │
│ • CARTRIDGE 1    │             │ • CARTRIDGE 2    │              │ • CARTRIDGE 3    │
│   (e.g., Sena)   │             │   (e.g., Cardo)  │              │   (LoRa + GNSS)  │
└──────────────────┘             └──────────────────┘              └──────────────────┘
                                           │
                                           ▼ 2.4 GHz Wireless Link (ESP-NOW < 1.8 ms)
                                 ┌──────────────────────────────────┐
                                 │ 1x UNIVERSAL FRONT NODE (IP67)   │
                                 │ (Smart Fairing Hub & Cockpit)    │
                                 │ • 4-in-1 Universal Mounting      │
                                 │ • Ottocast USB-A Port (CarPlay)  │
                                 │ • Glovebox USB-C Charging Port   │
                                 │ • Knowles MEMS Wind Sensor       │
                                 │ • Battery-Free Handlebar PTT     │
                                 └──────────────────────────────────┘
```

---

## 2. 3D Printing Guidelines (FDM vs. Industrial MJF)

### Recommended Filaments for Outdoor Motorcycle Use (FDM):
* **PETG:** *Ideal for open-frame printers.* UV-resistant, oil/chemical tolerant, heat stable up to $80\,^\circ\text{C}$.
* **ASA (or ABS):** *Best choice for enclosed printers (Bambu X1/P1, Prusa XL).* 100% UV stable, heat resistant to $100\,^\circ\text{C}$.
* **PA-CF / PET-CF:** Extreme stiffness and OEM-grade matte carbon texture.
* ❌ *Warning:* **Do NOT use standard PLA**, as it softens and deforms in direct sunlight (exceeding $55\,^\circ\text{C}$).

### Optimal Slicer Settings for IP67 Water Resistance:
* **Perimeters (Walls):** Set to 4–5 walls ($\approx 1{,}6 \dots 2{,}0\,\text{mm}$ thickness, resulting in 100% solid shell).
* **Infill:** $25 \dots 40\,\%$ Gyroid.
* **Layer Height:** $0{,}16\,\text{mm}$ (produces smooth O-ring sealing grooves).
* **Flow Rate:** $102 \dots 104\,\%$ (slight over-extrusion fuses inter-layer micropores).

---

## 3. Subsystem Assembly Steps

### Step 1: Central Control Box Assembly
1. **Heat-Set Inserts:** Melt 4x M3 brass threaded inserts (Ruthex) into the lower tub using a soldering iron ($240\,^\circ\text{C}$).
2. **Mount Main PCB:** Secure the main controller (`PCBA 01`) onto the damping standoffs using M2.5 screws.
3. **Mid Tray & Battery:** Position the upper case with the intermediate tray, place the 1000 mAh LiPo into the battery pocket, and secure with the EPDM strap.
4. **Gasket & Lid:** Seat the $\varnothing 1{,}5\,\text{mm}$ silicone O-ring cord into the perimeter groove, adhere the Gore ePTFE vent, and tighten the 4x M3 x 40 mm stainless screws in a cross pattern.

### Step 2: Satellite Pods 1, 2, and Rear Pod 3
1. **Install Baseboard:** Slide `openmotorbridge_pod_base` into the pod tub and tighten the M8 hex nut.
2. **Mount Bulkhead:** Secure the protective partition wall with 2x M2 countersunk screws.
3. **Assemble Cartridge:** Snap the cartridge carrier (`PCBA 03`) into the sled and connect the OEM headset cradle (Sena pogo pins or Cardo Air-Mount).

---

## 4. Universal Front Node Assembly & Vehicle Installation

### 4.1 Enclosure Assembly
1. **Heat-Set Inserts:**
   * Melt 4x M3 inserts into the enclosure corners.
   * Melt 4x M4 inserts into the AMPS pattern ($30 \times 38\,\text{mm}$) on the bottom.
2. **Acoustic Membrane:** Adhere the hydrophobic Gore ePTFE acoustic membrane over the Knowles MEMS sound port.
3. **Mount PCB:** Fasten `PCBA 05` using M2.5 screws.
4. **Wiring & Gaskets:** Route lead wires through the EPDM rubber combs, seat the silicone cord gasket, and screw down the lid using 4x M3 x 20 mm bolts.
5. **Dust Cap:** Attach the silicone tethered dust cap over the USB-C port `J2`.

### 4.2 Motorcycle Mounting (4 Options)

```
┌────────────────────────────────────────────────────────────────────────┐
│               FRONT NODE 4-IN-1 MOUNTING OPTIONS                       │
├────────────────────────────────────────────────────────────────────────┤
│ Option 1: AMPS Pattern (30 x 38 mm)                                    │
│ • Bolts directly to RAM-Mount balls, Garmin brackets, nav towers       │
├────────────────────────────────────────────────────────────────────────┤
│ Option 2: 120° V-Groove Tube Saddle with EPDM O-Rings                  │
│ • Toolless attachment to Ø 22 mm to Ø 32 mm crash bars (BMW GS)        │
├────────────────────────────────────────────────────────────────────────┤
│ Option 3: M4 Silentblocks                                              │
│ • Vibration-isolated screw mounting inside the fairing beak            │
├────────────────────────────────────────────────────────────────────────┤
│ Option 4: 3M Dual-Lock Recesses                                        │
│ • Concealed attachment inside Harley Batwing / Sharknose fairings      │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Electrical Connections
* **12V Vehicle Power:** Connect a single 2-core wire (KL15 switched ignition and chassis ground) to the parking light or accessory socket.
* **Ottocast Dongle:** Plug into USB-A Port `J1` and affix with 3M Dual-Lock inside the fairing.
* **Glovebox Extension:** Route a USB-C cable from Port `J2` to the glovebox for smartphone charging.
* **Handlebar PTT:** Wire the mechanical handlebar button to 2-pin header `J3`.

---

## 5. First Commissioning & Flashing Checklist

```bash
# 1. Flash Central Main Controller (ESP32-S3)
cd openMotorBridge/firmware/main_controller
pio run --target upload
pio run --target uploadfs

# 2. Flash Rear Tail Coprocessor (RP2040)
cd ../rear_coprocessor
pio run --target upload

# 3. Flash Front Node (ESP32-C3)
cd ../front_node
pio run --target upload
```

### Verification Checklist:
1. [ ] **Bench Power:** Apply $12{,}0\,\text{V DC}$ (current limit $150\,\text{mA}$). Quiescent draw should measure $45 \dots 75\,\text{mA}$.
2. [ ] **Status LED:** Pulses green (system ready, UPS charging).
3. [ ] **Web Dashboard:** Connect via Web Bluetooth to `OpenMotorBridge_v8`.
4. [ ] **Cartridge Detection:** Insert cartridges into Pods 1 and 2 $\rightarrow$ Headset profiles appear immediately.
5. [ ] **Front Node Wireless Link:** Dashboard displays `ESP-NOW LINK (2.4 GHz) - READY`.
6. [ ] **PTT Test:** Press handlebar button $\rightarrow$ Dashboard PTT tile illuminates green (`< 1.8 ms Latency`).
7. [ ] **CarPlay Hard Reboot:** Click "CarPlay 1-Click Hard Reboot" $\rightarrow$ VBUS drops to $0{,}00\,\text{V}$ for $2{,}5\,\text{s}$ and restarts cleanly.
8. [ ] **Audio Check:** Pair headset and play music $\rightarrow$ Crystal-clear audio free of ground loops.
