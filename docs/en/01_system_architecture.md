# 01 - System Architecture, Universal Satellite Topology & Acoustics

This document specifies the overall system architecture of **OpenMotorBridge v8.0**, the universal satellite topology, vehicle-integrated mounting concepts (saddlebag, frame, tail, and fairing docking with 100% wireless helmet comfort), RF coexistence, and seamless integration into modern OEM motorcycle infotainment systems.

---

## 1. Problem Statement & Architectural Philosophy

Classic motorcycle communication systems are historically fragmented:
* **Incompatible Mesh Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh, and analog PMR446 radio cannot communicate directly.
* **RF Overload & De-Sensing:** Operating multiple 2.4 GHz mesh transceivers in close proximity (e.g., on the same helmet or in a single enclosure) results in severe receiver desensitization (*De-Sensing*), intermodulation, and range drops of up to $80\,\%$.
* **Proprietary Infotainment Lock-in:** Systems like Harley-Davidson Boom! Box GTS / Skyline OS or BMW ConnectedRide require expensive OEM modules (such as the HD WHIM) to unlock Apple CarPlay or Android Auto.

**OpenMotorBridge v8.0** resolves these bottlenecks via a modular, decoupled **Satellite Topology** with galvanically isolated DSP audio routing on the motorcycle:

```
                                     SYSTEM TOPOLOGY OVERVIEW
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT / HANDLEBAR & KEYFOB:                                                            │
│    • Front Node (PCBA 05): Hardwired Handlebar Switch / PTT Input (Optocoupled)             │
│    • Smart Keyfob (PCBA 07): BLE/LoRa Pager (LiPo with MAX17048 Fuel Gauge & Wireless PTT)  │
│    • PWA Dashboard on Smartphone / TFT display via Web Bluetooth (WebBLE)                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTRAL CONTROL BOX (Under-Seat / in Vehicle Cockpit, IP67 Sealed):                      │
│    • ESP32-S3 Dual-Core MCU (240 MHz) • ES8388 Audio Codec & DSP Audio Mixer               │
│    • LM5164-Q1 72V Automotive Step-Down • BQ24075 UPS & 2200mAh Flat LiPo Backup Battery    │
│    • 4-Bit High-Speed SDIO MicroSD Ringbuffer • 2x Bourns 1500 V RMS Audio Isolation Xfmrs  │
└─┬─────────────────────────────────────────────────────────────────────────────────────────┬─┘
  │                                                                                         │
  ▼ Central HD26 Flanged Connector (250 mm Y-Breakout Harness Pigtails)                     │
┌──────────────────────────────┬──────────────────────────────┬─────────────────────────────┤
│ 3. SATELLITE POD 1 (M8 6P):  │ 4. SATELLITE POD 2 (M8 6P):  │ 5. REAR POD 3 (M8 6P):      │
│ • Universal Pod Enclosure    │ • Universal Pod Enclosure    │ • Universal Pod Enclosure   │
│ • Intercom Bridge A (Sena    │ • Intercom Bridge B (Cardo   │ • 1-Tier Monolithic Sled    │
│   50S/60S/MeshPort Sled)     │   Packtalk Edge / PMR446)    │ • u-blox MAX-M10S Multi-GNSS│
│ • Saddlebag, Frame, Rear or  │ • Saddlebag, Frame, Rear or  │ • SX1262 LoRa 868MHz        │
│   Crash Bar Mounting         │   Crash Bar Mounting         │ • DS18B20 Temp Sensor (J6)  │
│                              │                              │ • 2.4 GHz OMM-Mesh (ESP32-C3│
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. VEHICLE POWER: AMP Superseal 1.5 4-Pin / 12V Car Charger (KL30, KL15, GND)           │
  ├─► 7. REAR RADAR BRANCH: M8 4-Pin / Binder M5 4-Pin (Radar 2.0 Sub-MCU PCBA 08 /            │
  │      Wheeltec MR20 77-GHz mmWave / 36x Halo RGB LEDs / 5.9 GHz V2X or Garmin Varia)───────┤
  │                                                                                         │
  ▼ 2.4 GHz Ultra-Low-Latency Wireless Link (ESP-NOW < 3ms & BLE 5.0 2M-PHY)                │
┌───────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. COCKPIT SUBSYSTEM: Wireless Universal Front Node (PCBA 05 Cockpit & Cam Bridge)       │
│ • Automotive 4-Port USB 2.0 Hub (Microchip USB2514B) for Boom! Box & CP2AA COTS Dongle   │
│ • Switched Dongle Port via TI TPS2051B (Controlled 2.5s Cold Reboot & 60s Auto-Café)     │
│ • 20W USB-PD Fast-Charging Handlebar Port via Southchip SC8102 Synchronous Buck-Boost      │
│ • Digital I2S MEMS Ambient Mic with ePTFE Acoustic Vent (Edge RMS Noise Level Tracking)   │
│ • Hardwired Handlebar PTT Pushbutton Input (Port J3: PTT, Cam-Mark, Siri, < 5 ms)         │
│ • Blind-Spot Mirror LEDs (Port J9: N-MOSFET drivers L+R for amber 12V LEDs)               │
│ • Wireless Actioncam Induction Dock (Port J8: 5V Qi charging coil with auto-shutter stop) │
│ • Integrated Cockpit CAN-Bus Transceiver (TCAN334G with 120 Ohm) for Fairing TFT Displays │
│ • Only Single Vehicle Wire Needed: Rugged 2-Core 12V Power Cable (KL15 / GND)              │
├───────────────────────────────────────────────────────────────────────────────────────────┤
│ 9. SUPPORT VEHICLE TOPOLOGY (Car / Support-Van / Rally Sweep Vehicle / RV):               │
│ • Central Box with Dashboard Wedge Dock (car_dashboard_wedge_dock.stl) & 12V Cig Lighter  │
│ • Rear Pod 3 on Passenger Sun Visor Clip (car_sun_visor_pod3_clip.stl) via 3m Roof Cable  │
│ • Live LoRa-Mesh Fleet Tracking of All Group Bikes on Tablet / Smartphone (PWA Offline)  │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Guiding Principle: "Empower the Lead, Don't Replace Him"

Traditional telematics and motorcycle rider assistance systems tend toward digital paternalism: they clutter the cockpit with gearshift recommendations, unsolicited traffic jam warnings, and modal navigation pop-ups. OpenMotorBridge follows a radically opposite philosophy grounded in real-world group riding:

* **The Lead Rider is the Ultimate Sensor:**
  * No algorithm and no satellite uplink can detect mid-corner gravel, an obscured construction trench, a slow tractor around a blind bend, or crossing wildlife as rapidly and accurately as the trained eyes of an attentive road captain.
  * A 3-second voice announcement over the intercom (*"Watch out, road work on the right, merge left!"*) reaches every group member in milliseconds, requires zero glance diversion from the road surface, and allows immediate adjustment of speed and line.
* **Primacy of Stable, Cross-Brand Intercom:**
  * OpenMotorBridge's primary mission is not to lecture the rider, but to provide **unshakeable, uninterrupted voice communication between incompatible headset brands (Sena, Cardo, OMM)** with zero latency.
* **Respect for Established Visual Riding Habits:**
  * Even during an unforeseen radio dropout (e.g. depleted headset batteries), an organized group never falls apart: an attentive lead rider regularly scans the rear-view mirrors. If a following rider indicates right or flashes their high beam, the lead immediately recognizes the signal and pulls over at the next safe opportunity.
  * Digital electronics must respect and support these proven human routines rather than disrupting them with distracting on-screen menus.

---

## 2. Modular System Philosophy & Mounting Freedom (The Standardized Functional Nodes)

OpenMotorBridge v8.0 defines the platform across **standardized functional nodes**:
1. **Central Box (Main ECU):** Central computational core (ESP32-S3), 24-bit audio DSP/codec (ES8388), galvanic isolation transformers, 72V automotive step-down (LM5164-Q1), and LiPo UPS (BQ24075 with 2,200 mAh flat pouch cell). *(Typically mounted centrally under the seat in the battery compartment or in the car dashboard).*
2. **Rear Pod 3 (Backbone, Telemetry & Temperature):** Multi-GNSS (u-blox MAX-M10S), 868 MHz LoRa (Semtech SX1262), 2.4 GHz OMM Mesh co-processor (ESP32-C3 RISC-V), 6-axis IMU (BMI270), and the **waterproof Dallas DS18B20 1-Wire stainless steel immersion probe (Port J6)** for continuous road and ambient temperature monitoring in the slipstream shadow (black ice warning at $T \le +3.0^\circ\text{C}$). *(Typically mounted at the rear with an unobstructed view of the zenith, or on the car sun visor).*
3. **Satellite Pod 1 (Intercom Bridge A):** Universal cartridge bay for Sena (Mesh 2.0/3.0 / Bluetooth). *(Typically on the left vehicle side).*
4. **Satellite Pod 2 (Intercom Bridge B):** Universal cartridge bay for Cardo (DMC Gen1/Gen2 / Bluetooth) or analog PMR446 radio. *(Typically on the right vehicle side for RF spatial diversity).*
5. **Front Node (Cockpit, Camera & Sensor Hub):** Autonomous ESP32-S3 satellite, automotive USB 2.0 4-port hub (USB2514B) for Apple CarPlay / Android Auto CP2AA dongle, fast-charging handlebar smartphone port (Southchip SC8102 20W USB-PD), switched VBUS via TPS2051B, digital PTT button input (Port J3), BSD blind-spot mirror LEDs (Port J9), wireless actioncam induction dock (Port J8), TCAN334G CAN transceiver, and Knowles I2S MEMS ambient wind noise microphone. *(Typically hidden behind fairings or inside the headlight nacelle).*
6. **Radar 2.0 Sub-MCU & Halo-Wings (PCBA 08 - Active Rear Safety Module):** Wheeltec MR20 77-GHz mmWave radar (up to $90\,\text{m}$ detection range, $\pm 60^\circ$ FoV), ESP32-C5 Dual-Band Sub-MCU, 36x addressable Halo RGB LEDs (18 left, 18 right) for dynamic blind-spot and emergency brake strobe warning, 5.9 GHz ITS-G5 (V2X) ceramic patch antenna cradle, and industrial Binder Series 707 M5 IP67 connector.

```
                     THE STANDARDIZED FUNCTIONAL NODES
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. FRONT NODE (Cockpit/Nacelle):  Wireless USB, Cam, PTT & Audio Hub        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTRAL BOX (Under Seat/Batt): DSP Audio Matrix, Power Supply, UPS, CAN  │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│ 3. POD 1 (Left/Saddlebag):   │ 4. POD 2 (Right/Saddlebag):  │ 5. REAR POD 3:│
│ • Intercom Bridge A (Sena)   │ • Intercom Bridge B (Cardo)  │ • GNSS / LoRa │
│ • 100% Quick-Swap Cartridge  │ • 100% Quick-Swap Cartridge  │ • DS18B20 Temp│
├──────────────────────────────┴──────────────────────────────┴───────────────┤
│ 6. RADAR 2.0 SUB-MCU & HALO-WINGS (PCBA 08 at Rear):                        │
│ • Wheeltec MR20 77-GHz mmWave Radar • 36x Halo RGB LEDs • 5.9 GHz V2X CAN   │
└─────────────────────────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **Mounting Freedom – *Your Bike, Your Choice*:**  
> Where and how you place these modules on your motorcycle or vehicle is deliberately **entirely up to you**! OpenMotorBridge provides the standardized electronic layouts, enclosure dimensions, and interfaces.  
> For popular motorcycle categories and support vehicles, we deliver turnkey, 100% zero-drill and adhesive-free **Reference Mounting Kits** in **[Chapter 08 (Mechanics & CAD)](08_enclosures_mechanics_cad.md)**:
> * **Reference Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring):** Pod 3 inside the Under-Cowl Skeleton Dock under the forged carbon cowl, Pods 1 & 2 protected inside the saddlebag lids (zero-drill Torx hinge screws, 19 mm MagSafe side pass-through in saddlebag inner side-wall beside OEM mount), Front Node on fairing bracket behind outer sharknose skin, Radar 2.0 at license plate carrier.
> * **Reference Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 3 in the Touring Fender Console on the rear fender, Pods 1 & 2 in the saddlebag lids (MagSafe side pass-through), Front Node hidden inside the 7" headlight nacelle.
> * **Reference Kit 3 (Classic Bagger & Cruiser – Street Glide / Electra Glide):** Pod 3 in the Touring Stealth Console seamless to passenger seat, decoupled Radar 2.0 below the license plate, Pods 1 & 2 in the saddlebag lids.
> * **Reference Kit 4 (Adventure & Touring Enduros – BMW GS, KTM Adventure, Africa Twin):** Pod 3 directly on luggage rack / tubular subframe with integrated M5 GoPro radar arm, Pods 1 & 2 on crash bars via 120° V-grooves and EPDM tension straps, Front Node on nav crossbar or inside beak.
> * **Reference Kit 5 (Car / Support-Van / Rally Sweep Vehicle / RV):** Pod 3 in the Sun Visor Clip ([`car_sun_visor_pod3_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod3_clip.stl)) on passenger sun visor for non-shielded LoRa/GNSS through windshield; Satellite Pods 1 & 2 via 3M Dual-Lock on dashboard or concealed at seat console (interchangeable with visor clip on cartridge swap); 3 m flat USB-C cable concealed behind headliner and A-pillar; Central Box on vibration-damped wedge dock ([`car_dashboard_wedge_dock.stl`](../../hardware/cad/stl/05_accessories/car_dashboard_wedge_dock.stl)) on dashboard with 12V cigarette lighter PD adapter; autonomous Bluetooth OBD2 telemetry (ELM327 / vGate) coupled directly to Central Box; PWA dashboard on iPad/tablet for live tracking of all group bikes without cellular connectivity.
>
> Riders and support crews are encouraged to replicate these kits, adapt them for other vehicle models, or design custom brackets based on our open CAD/STEP dimensional envelopes!

### 2.1 Whitepaper Design Rationale: Decentralized Satellite Topology vs. Monolithic Single-Box

During the initial concept phase, an in-depth engineering evaluation analyzed whether the entire system should be housed within a single, large central enclosure (e.g. under the seat or behind the front fairing). The monolithic approach was unanimously rejected after electromagnetic simulation and physical prototyping:

#### Evaluation Matrix: Monolithic Single-Box vs. OpenMotorBridge Decentralized Satellite Architecture

| Evaluation Metric | Option A: Monolithic Single-Box | Option B: Handlebar/Cockpit-Only Box | **Option C: OMB Decentralized Satellites (Selected)** |
| :--- | :--- | :--- | :--- |
| **RF Self-Interference (De-Sensing)** | **Critical:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V buck converter in extreme proximity | **Critical:** Severe cross-talk into cockpit TFT and motorcycle radio antenna | **Optimal (> 45 dB Isolation):** GNSS/LoRa at rear, Intercoms on lateral flanks, display at front |
| **Harness Bundle Diameter** | **Bulky:** 26+ discrete wire conductors routed through the motorcycle chassis | **Poor:** 18 conductors routed across the pivoting steering head (harness fatigue risk) | **Ultra-Slim:** Only a 6-pole M8 bus connection to the rear; Front Node autonomous via ESP-NOW |
| **Thermal Dissipation** | **Hot-Spot (> 18 W):** 72V DC/DC + audio power amplifiers + battery charging under seat | **Thermal Overheating (> 85 °C):** Trapped heat accumulation directly behind headlight nacelle | **Evenly Distributed:** Max. 3–4 W per enclosure; passive convection cooling with zero hot-spots |
| **GNSS Zenith View & Radar** | **Obstructed:** Seat bench and rider's body block satellites & rear radar aperture | **Poor:** Rear blind-spot radar from handlebars is physically impossible | **Ideal:** Rear Pod 3 has unobstructed 360° sky view and clear backward radar field-of-view |
| **Dynamic Wind Sampling (AGC)** | **Physically impossible:** Zero dynamic ram-air pressure underneath the seat | **Feasible:** Wind pressure measurement directly at handlebar | **Excellent:** Knowles I2S MEMS positioned directly at windshield line in Front Node |

1. **Physics of RF Coexistence (Mitigating Receiver De-Sensitization):**
   * GNSS satellite signals reach the ground at ultra-low power levels of approximately **$-130\,\text{dBm}$ to $-160\,\text{dBm}$**.
   * Placing a high-voltage switching regulator (LM5164-Q1 with fast switching edges), an 868 MHz LoRa transmitter (+22 dBm / 160 mW), and dual 2.4 GHz mesh radios inside the same metallic chassis within inches of each other lifts the wideband thermal noise floor (*Noise Floor Lift*). The GNSS receiver suffers cycle slips, losing carrier phase lock and degrading precision.
   * Physical spatial separation (Rear Pod 3 for navigation, Pods 1 & 2 for intercoms on the lateral flanks) naturally enforces **$> 45\,\text{dB}$ of free-space path loss** between RF stages.
2. **Harness Reliability Across the Steering Head:**
   * Every copper conductor traversing the rotating steering head suffers millions of bending cycles over a motorcycle's operational life.
   * By segregating cockpit, USB display, and PTT functions into the **Front Node (PCBA 05)** communicating over an ultra-low-latency **ESP-NOW wireless bridge (< 0.9 ms latency)** with the Central Box, zero vulnerable data signal wires cross the steering axis.
3. **Conclusion:** Maximum signal integrity, zero thermal hot-spots, superior long-term mechanical reliability, and unmatched installation flexibility across all motorcycle categories.

### 2.2 Vehicle Mounting (Crash Bars, Frame Tubes, Luggage Racks)
* **Universal Prism (V-Groove):** The bottom of each pod housing features a $120^\circ$ prism contour ($R = 15\,\text{mm}$) that cradles all standard motorcycle frame tubes:
  * $\varnothing 22\,\text{mm}$ ($7/8"$ handlebars and rear subframe tubes)
  * $\varnothing 25.4\,\text{mm}$ ($1"$ crash bars and cruiser frame tubes)
  * $\varnothing 28.6\,\text{mm}$ ($1\,1/8"$ tapered handlebars and enduro frames)
  * $\varnothing 32\,\text{mm}$ ($1\,1/4"$ heavy-duty crash bars)
  * **Flat Surfaces:** Sits rock-solid on flat panels (under-seat battery tray / side covers).
* **EPDM Tension Ring Retention:** Two UV-resistant EPDM rubber rings (or silicone ladder straps) wrap around the tube and hook into the 4 lateral side lugs. This simultaneously isolates high-frequency engine vibrations.
* **Theft-Resistant Fixed Mounting:** Integrated $5.0 \times 2.5\,\text{mm}$ passthrough slots allow threading standard $4.8\,\text{mm}$ zip-ties or stainless hose clamps.

### 2.3 Wireless Helmet Audio
* Heavy intercom hardware (Sena 50S / Cardo Edge) stays safely locked and weather-protected on the motorcycle.
* Helmets remain $100\%$ lightweight, aerodynamically stock, and completely cable-free. Audio I/O connects wirelessly via the Central Box's integrated Bluetooth interface.

### 2.4 Universal Off-the-Shelf OEM Adapter Interfacing
The enlarged pod cartridges ($110 \times 54 \times 28\,\text{mm}$ interior cavity) accommodate all commercial off-the-shelf OEM adapters in their factory-unopened state:
* **Class S (Smart Modular Cartridge with Mechatronics • OMB Reference):** e.g. Sena SPIDER X Slim (primary recommendation), Sena 60S, Cardo Edge – 100% factory-unopened original device seated in a PA12-MJF form-fit cradle with 3-point EPDM damping against $20\,\text{g}$ shock/vibration, 4 independent mechatronic actuators on PCBA 03 Rev 2.0 (WCH CH32V003 RISC-V MCU, In-System Flashing via Pin 5 UART), factory $3.85\,\text{V}$ DC direct power supply, zero pogo pins, zero soldering, 100% preservation of manufacturer warranty and IPX weatherproofing.
* **Class A (Wireless Bridges & USB Power):** e.g. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red – powered via low-profile 90° Micro-USB/USB-C, wireless BT audio bridge to helmet, external SMA bulkhead double-jack with silicone protection plug on faceplate.
* **Class B (Pogo-Pin Spring-Contact Cradles):** e.g. Sena 50S/60S/30K/20S EVO – full analog audio (ES8388 codec) and TLP222A PTT synthesis.
* **Class C (Magnetic Air-Mount):** e.g. Cardo Packtalk Edge / Pro (Note: Packtalk Neo lacks charge-while-riding and is excluded) – tool-free magnetic latching via dual N52 Neodymium magnets.
* **Class D (Slide Cradles):** e.g. Cardo Packtalk Bold/Black, Freecom series – mechanical slide rail with catch spring.
* **Class E (Analogue PMR446 Radios):** e.g. Midland G7/G9 Pro, XT30, Kenwood – 2-pin dual audio jack with PhotoMOS PTT keying.
*(Detailed wiring matrix and pinouts available in [Specification 02 (Intercom Matrix & Profiles)](02_intercom_matrix_profiles.md)).*

---

## 3. RF Coexistence & Spatial Diversity ($> 35\,\text{dB}$ Isolation)

When operating Sena and Cardo mesh units simultaneously, receiver blocking must be reliably prevented:

1. **Physical Separation ($d \ge 45\,\text{cm}$ via Lateral Flank Placement):**
   * **Zero Pods on Helmets:** The heavy universal pods ($110 \times 54 \times 28\,\text{mm}$ cartridges) remain permanently mounted on the vehicle (e.g. left and right saddlebag lids, frame tubes, or crash bars). Rider and pillion helmets remain 100% cable-free and unburdened by bulky pods.
   * **Physical & Metallic Barrier:** Pod 1 (left vehicle flank / left saddlebag) and Pod 2 (right vehicle flank / right saddlebag) utilize the motorcycle's steel/aluminum chassis, fuel tank, engine block, and rear subframe as a natural metallic RF shield.
2. **Shielding Attenuation:**
   * Free-space loss over $> 50\,\text{cm}$ combined with chassis metallic shielding achieves an **RF isolation of $> 35\,\text{dB}$**.
   * Coupling levels at adjacent receivers remain below $-15\,\text{dBm}$, keeping low-noise amplifiers (LNAs) in their linear region and preventing *De-Sensing*.
3. **Tri-RF Architecture in Rear Pod 3:**
   * Rear Pod 3 integrates 2.4 GHz Mesh, 868 MHz LoRa, and GNSS. The $25 \times 25\,\text{mm}$ patch ground plane and $15 \times 8\,\text{mm}$ antenna keepout restrict mutual RF degradation to $< 0.2\,\text{dB}$.

---

## 4. Physical Interfaces & Signal Matrix

### 4.1 Central HD26 Harness Pigtail Matrix (Central Box Main Connector)
All main system signals converge at the central HD26 flanged connector:

| Branch / Cable | Connector Type | Target Device | Transferred Signals / Conductors |
| :--- | :--- | :--- | :--- |
| **Pigtail 1 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 1** (Intercom Bridge A: Sena / Universal) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Pigtail 2 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 2** (Intercom Bridge B: Cardo / PMR446) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Pigtail 3 (250 mm)** | M8 6-Pin A-Coded (Female) | **Rear Pod 3** (GNSS, LoRa & Temperature) | UART_TX, UART_RX, 1-PPS_SYNC, 1-WIRE_ID, +5V_POD3, GND |
| **Pigtail 4 (250 mm)** | AMP Superseal 1.5 4-Pin / 12V Car | **Vehicle Power Supply** (Motorcycle or Car 12V Cigarette Lighter) | KL30 (Batt+), KL15 (Ign+), GND (Power), GND (Sense) |
| **Pigtail 5 (250 mm)** | M8 4-Pin A-Coded / Binder M5 4P | **Rear Radar 2.0 (PCBA 08)** / Garmin Varia | RADAR_PWR_12V, RADAR_GND, RADAR_RX (UART/CAN_H), RADAR_TX (UART/CAN_L) |

### 4.2 Rear Pod 3 (PCBA 04) Interface Matrix
| Port | Connector Type | Function | Connected Hardware / Signal |
| :--- | :--- | :--- | :--- |
| **`J1`** | M8 6-Pin Flange Plug | Bus Feed from Central Box | UART (TX/RX), 1-PPS Time Sync, 1-Wire ID, +5V, GND |
| **`J2`** | JST-SH 1.0mm 4-Pin | I2C Telemetry Bus | BMI270 (6-Axis IMU), BMP390 (Barometer/Weather Trend), QMC5883L (Compass) |
| **`J3`** | Murata MM8030 / SMA | RF Mesh 2.4 GHz | Dipole Antenna / OMM Mesh Transceiver |
| **`J4`** | Murata MM8030 / SMA | RF LoRa 868 MHz | Dipole Antenna / SX1262 LoRa Alpine Pass Radio |
| **`J5`** | Murata MM8030 / SMA | RF GNSS L1/L5 | Active/Passive Patch Antenna for MAX-M10S |
| **`J6`** | JST-PH 2.0mm 3-Pin | 1-Wire Ambient Temperature | **Dallas DS18B20 Stainless Immersion Probe (IP67)** in Slipstream Shadow |

### 4.3 Front Node (PCBA 05) Cockpit Interface Matrix
| Port | Connector Type | Function | Connected Hardware |
| :--- | :--- | :--- | :--- |
| **`J1`** | JST-PH 2.0mm 2-Pin | 12V Switched Power | Local power feed (KL15 & GND) at steering head / cartool / headlight |
| **`J2`** | JST-PH 2.0mm 3-Pin | Display Audio CAN | Cockpit CAN bus (CAN_H, CAN_L, GND) for Harley Skyline OS / TFT |
| **`J3`** | JST-PH 2.0mm 4-Pin | Handlebar Multi-Button Interface | 3x IP67 microswitches: PTT Intercom, Video Bookmark, Siri/Voice (< 5 ms) |
| **`J4`** | Molex Micro-Fit 4-Pin / USB | USB Host Upstream | Uplink to Boom! Box GTS / Skyline OS display headunit |
| **`J5`** | USB-C Receptacle IP67 | 20W USB-PD Fast Charging | Handlebar smartphone (QuadLock / SP Connect) via SC8102 Buck-Boost |
| **`J6`** | Molex Micro-Fit 4-Pin | Switched CarPlay Port | Wireless CP2AA dongle with 1-click TPS2051B cold reboot |
| **`J7`** | USB-C Onboard | Service & Flash Port | ESP32-S3 firmware update & WebSerial diagnostics |
| **`J8`** | JST-PH 2.0mm 2-Pin | Actioncam Power Supply | 5V Qi charging coil in camera dock with automatic BLE shutter stop |
| **`J9`** | JST-PH 2.0mm 3-Pin | Blind-Spot Mirror LEDs | 2x amber 12V LEDs on mirror stems via N-MOSFET drivers L+R |
| **`J10`** | JST-PH 2.0mm 2-Pin | Qi Wireless Cradle | 12V switched feed for wireless charging cradle (zero quiescent current) |
| **`J11`** | JST-PH 2.0mm 2-Pin | Auxiliary Front Spotlights | Up to 4.5A high-side switched LED lights (auto-strobe on emergency stop) |

---

## 5. Integration into OEM Infotainment Systems

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 WHIM Emulation & Apple CarPlay / Android Auto Unlocking
* **Background:** Apple CarPlay strictly mandates an active speech microphone. Harley-Davidson locks CarPlay in factory Boom! Box GTS firmware unless either a wired 7-pin DIN headset or the proprietary **HD-WHIM** (*Wireless Headset Interface Module*, $> \$350$) is installed.
* **Impedance Emulation:** OpenMotorBridge replicates the DC bias and AC impedance ($1.0 \dots 2.2\,\text{k}\Omega$) of an active OEM electret microphone via its isolated Bourns transformer frontend.
* **Result:** The Boom! Box GTS unlocks Apple CarPlay and Android Auto on the 6.5" or 12.3" touchscreen immediately — **without requiring the \$350 WHIM module** or unreliable jumper bypass plugs.
* **Seamless Audio Ducking:** Boom! Box navigation announcements are prioritized and smoothly blended over active intercom conversations with adjustable ducking ($-12\,\text{dB}$).

#### 5.1.2 Universal Cockpit & Front Hub (PCBA 05): USB Subsystem, Live Traffic & PTT
The Front Node (PCBA 05) serves on **all motorcycle types** as the universal cockpit hub, eliminating vulnerable wiring across the flexed steering head:
* **Wireless RF Bridge to Central Box:** An autonomous controller node (ESP32-S3 Dual-Core Xtensa LX7 @ 240 MHz with Vector DSP) inside the fairing communicates via **ESP-NOW ($< 0.9\,\text{ms}$ latency)** and **BLE 5.0 (2M-PHY)** directly to the Central Box.
* **Wired Handlebar PTT (Optocoupler at `J3` / GPIO 0, $< 1.8\,\text{ms}$ Latency):** Minimal $30\dots 50\,\text{cm}$ harness at the handlebar — zero failure-prone signal wires crossing the steering neck!
* **Digital I2S MEMS Ambient Microphone (Knowles SPH0645LM4H-6):** Edge-DSP ambient wind/road noise computation directly at the windshield (physically impossible under the seat) for automatic helmet volume AGC.
* **Automotive USB 2.0 Subsystem (Microchip USB2514B 4-Port Hub & Power Architecture):**
  * **Upstream Host Port (`J4`):** Connects directly to the USB input of the Harley-Davidson Boom! Box GTS / Skyline OS in the glovebox.
  * **Downstream Port 1 (Handlebar Phone Fast-Charging):** Dedicated $20\,\text{W}$ USB-PD fast-charging port via `Southchip SC8102` synchronous buck-boost converter directly on the handlebar.
  * **Downstream Port 2 (CP2AA COTS Dongle):** Switched $+5.0\,\text{V}$ VBUS via `TI TPS2051B` power switch with software-controlled **2.5s cold restart** and **Auto-Café 60s timer** upon ignition off. The commercial CarPlay/Android Auto dongle is mounted inside the fairing cavity thermally decoupled via a $25\dots 30\,\text{cm}$ shielded pigtail (3M Dual-Lock).
  * **Downstream Port 3 (Glovebox Passthrough & Media Port):** Transparent feedthrough with Port-Sense (100% free for USB MP3 sticks, firmware updates, and direct phone wired CarPlay).
  * **Downstream Port 4 (Cockpit Accessories):** High-power accessory feed for dashcams, external displays (Chigee AIO-5), or navigation systems (Garmin Zūmo XT2).
  * **USB-C Service Port (`J7`):** Native diagnostic, calibration, and flashing receptacle directly connected to the ESP32-S3 native USB-JTAG/OTG interface.
* **USB-Media Proxy & Source-Aware CAN Gating:**
  * Emulates an MFi-iPod / USB Audio Class device to Skyline OS: Displays track, artist, album, and duration natively on the 12.3" Harley screen, while audio stays in the helmet via LDAC/aptX (no WHIM needed).
  * **Collision Protection:** Checks `infotainment_source_active` (CAN `0x388`) and Hub Port 1 to ensure handlebar media buttons only control the phone when OMB/CarPlay/BT is active (preventing phantom streaming while listening to MP3 sticks or radio).
* **USB CDC-NCM Ethernet Tethering for Internal OEM Navigation:**
  * Presents as a virtual automotive network interface at port `J4`, routing phone data to the bike.
  * **Benefit:** Factory navigation (HERE / TomTom) gets **instant live traffic, congestion flow, and road closure alerts upon ignition ON** without manual phone hotspot setup.
* **Intelligent Standstill Filter & KL15 Buffer Capacitor (`C_BUF`):**
  * Low-ESR buffer capacitors keep the controller alive for $\approx 1\dots 2\,\text{s}$ upon ignition off, cleanly closing all open files.
* **Minimal Bike Wiring:** Single **2-core 12V automotive power lead (`J1`)** tapped at switched KL15 ignition; on-board TI TPS63070 buck-boost & LMR36015 buck converters provide full ISO 7637-2 cold-cranking compliance.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Real-time Telemetry:** Via the TCAN334G transceiver in listen-only mode, the bridge captures wheel speeds, lean angles, and turn indicators.
* **TFT Display Notifications:** System alerts can be rendered directly on the motorcycle TFT dashboard.

### 5.3 Rear Radar 2.0 & Blind-Spot Assistant (Wheeltec MR20 77 GHz mmWave & Garmin Varia) on Pod 3 Dual-Mount Bracket
* **Dual-Mount Bracket & Alignment:** The rear mounting bracket for Pod 3 or the decoupled license plate carrier ([`radar_license_plate_bracket.scad`](../../hardware/cad/scad/02_pod_base/radar_license_plate_bracket.scad)) integrates a bionic 36-tooth Hirth coupling for distortion-free horizontal radar leveling.
* **Dual-Radar Architecture (Two Interchangeable Radar Engines):**
  * **Radar 2.0 (Wheeltec MR20 77 GHz mmWave – Standard):**
    - Integrated in an IP67 winged monocoque housing ([`radar_mr20_housing.scad`](../../hardware/cad/scad/05_accessories/radar_mr20_housing.scad)) with PCBA 08 (ESP32-C5 Dual-Band Sub-MCU).
    - 77 GHz FMCW horn-array antenna with $\pm 60^\circ$ ($120^\circ$) horizontal FoV and up to $90\,\text{m}$ detection range.
    - 36-LED Neopixel dual warning wings (18 left, 18 right): Directional blind-spot detection (BSD), brake-light strobe on deceleration $> 0.4\,g$, and dynamically expanding proximity halo on rapid overtaking traffic ($TTC < 2.5\,\text{s}$).
    - Autonomous 5.9 GHz ITS-G5 (V2X) ceramic patch antenna cradle in the left wing for Car-to-X safety broadcasts.
    - Binder Series 707 M5 4-pin IP67 connector (power + macro-UART), mechanically decoupled.
  * **Radar 1.0 (Garmin Varia RTL515 / eRTL615 – Legacy):**
    - 24 GHz Doppler streaming (0xAA preamble, $140\,\text{m}$ detection range, $20\,\text{Hz}$ update) via GoPro Lock Dock.
* **Dynamic Threat Estimation & Time-To-Collision (TTC):**
  * $\text{TTC} = \frac{d}{v_{\text{rel}}}$.
  * **Clear (Green):** No vehicle in danger zone or $v_{\text{rel}} \le 10\,\text{km/h}$.
  * **Amber (Approaching):** $d \le 80\,\text{m}$ and $v_{\text{rel}} > 15\,\text{km/h}$ (standard vehicle closing in).
  * **Red (Collision Hazard):** $\text{TTC} < 3.5\,\text{s}$ or ($d \le 35\,\text{m}$ and $v_{\text{rel}} > 25\,\text{km/h}$).
* **Acoustic Helmet Warnings (Priority-1 Ducking):** On amber/red hazard alerts, the audio DSP immediately ducks music/intercom to **$-18\,\text{dB}$** ($< 15\,\text{ms}$ attack) and injects a crisp **synthesized dual-tone chime** ($880\,\text{Hz} \rightarrow 1760\,\text{Hz}$ on Amber, $988\,\text{Hz} \rightarrow 1976\,\text{Hz}$ on Red) directly into the rider's helmet.
* **Astronomical Dimming & Tunnel Detection:**
  * Computes the solar elevation angle $\alpha_{\text{sun}}$ from GNSS coordinates and UTC time: Dimming levels transition smoothly from 100% (daylight) down to 18% (night).
  * **Tunnel Detector:** Immediate loss of GNSS signal ($Fix = 0$ for $> 1.5\,\text{s}$) at speed $> 30\,\text{km/h}$ forces BSD LEDs to night dimming (18%) to eliminate rear-view mirror glare.
* **Turn Signal Coupling:** Right turn signal monitors left overtaking lane; left turn signal enforces dual-lane threat monitoring.

#### 5.3.1 Autonomous Weather Trend Engine (BMP390 with GNSS Altitude Compensation)
* **Physical Barometric Trend:** Normalizes ambient absolute pressure against GNSS ellipsoid altitude ($P_0 = P \cdot (1 - h / 44330)^{-5.255}$).
* **Trend Classification:** Detects barometric drops $> 2.0\,\text{hPa/h}$ or temperature plunges $> 3\,^\circ\text{C}/15\,\text{min}$ as incoming storm fronts without requiring any cellular data uplink.
* **Safe Delivery:** Weather alerts are announced while stationary ($v = 0\,\text{km/h}$) or during rest stops.

#### 5.3.2 Emergency Stop Signal (ESS) Brake Flashing via Rear Radar & Aux Power Port
* **100% CAN Listen-Only Compliant Operation:**
  * When the Central Box 6-DOF IMU detects acute emergency deceleration ($a_x < -6.0\,\text{m/s}^2$ or $> 0.6\,\text{g}$ from speed):
  * OpenMotorBridge dispatches serial macro commands over UART:
    - On Radar 2.0 (Wheeltec MR20): Triggers the dual 18-LED Neopixel warning wings (36 LEDs total) into an ultra-bright, synchronized $4.5\,\text{Hz}$ emergency brake strobe.
    - On Garmin Varia: Transmits `SET_LIGHT_MODE: STROBE_4HZ`.
  * **Result:** Maximum warning conspicuity for trailing drivers with **zero splicing into factory motorcycle hydraulic lines or wiring**.

#### 5.3.3 Dallas DS18B20 1-Wire Road & Ambient Temperature Safety (Port J6 on Pod 3)
* **Mounting Location & Thermal Decoupling:**
  * The waterproof stainless steel immersion probe (IP67, $\varnothing 6 \times 50\,\text{mm}$) connects via a 3-pin JST-PH cable to port `J6` on PCBA 04 in Rear Pod 3.
  * The probe emerges through the bottom face of the rear pod, positioned directly in the **slipstream shadow** (shielded from direct sunlight and rising engine/exhaust heat) in the airflow just above the road surface.
* **1-Wire Bus Protocol & Precision:**
  * Operates in true 3-wire mode (`+3.3V`, `1-WIRE_DATA`, `GND`) with an onboard 4.7 kΩ pull-up on PCBA 04.
  * 12-bit digital resolution ($0.0625\,^\circ\text{C}$ step size, sampling interval 2.0 s).
* **Black Ice Guard (Early Warning):**
  * When measured road temperature drops to $T \le +3.0\,^\circ\text{C}$ (hazard of freezing moisture, wet patches, and black ice on bridges and mountain passes), OMB initiates a two-tier safety warning:
    1. **Acoustic Warning Chime:** A discreet low dual-tone ping ($440\,\text{Hz} \rightarrow 330\,\text{Hz}$) is played once into the rider headset.
    2. **Visual Snowflake Indicator:** The blue ice-crystal warning icon lights up persistently in the PWA Ride HUD and on the TFT cluster until temperature sustainably rises above $+4.5\,^\circ\text{C}$ (hysteretic deadband against flicker).

### 5.4 LoRa 868 MHz Bike Alarm Pager & Parking Sentry (OEM BCM + Autonomous IMU)
* **The Limitation of Traditional Bike Alarms:** When parked at a hotel or mountain pass café, the bike's audible horn alarm cannot be heard from $> 50\dots 100\,\text{m}$ away.
* **OpenMotorBridge as Long-Range LoRa Pager:**
  1. **OEM Alarm Integration (e.g. Harley Smart Security / BMW DWA):**
     * OMB monitors the CAN bus in low-power standby (buffered by the onboard 18650 UPS cell).
     * If the factory BCM triggers the vehicle alarm (`bcm_alarm_triggered == 1`), OMB immediately detects the broadcast.
  2. **Autonomous Protection (for bikes without OEM alarm or luggage tamper):**
     * Internal 6-DOF IMU detects attitude changes (lifting off sidestand, impact shocks).
     * Reed switches on luggage sled docks detect unauthorized cartridge extraction.
  3. **LoRa 868 MHz Long-Range Alert (Packet Type `0xFE`):**
     * OMB transmits an instant emergency packet with $1\dots 5\,\text{km}$ penetration through concrete hotel walls to the rider's pocket receiver or group bikes:
       > *„🚨 THEFT ALERT: Your motorcycle is being moved! (Distance: 180 m)“*

### 5.5 Universal BLE Tire Pressure Monitoring (TPMS) for Non-CAN Bikes
* **Target Motorcycles:** All bikes lacking factory CAN tire pressure sensors (Naked bikes, sportbikes, enduros like Yamaha Ténéré 700, KTM Adventure).
* **Operation:**
  * The Central Box Bluetooth 5.0 controller passively captures standard advertisement frames from commercial BLE valve cap sensors (e.g. FOBO Bike / Deelife).
  * No wiring required; valve caps screw directly onto stems and pair in seconds via the WebApp PWA.
  * **Cockpit Display & Voice Warnings:** Live tire pressure and temperature appear on the Ride HUD; sudden pressure drop triggers immediate priority acoustic warnings in the helmet.

### 5.6 Proximity & Standstill Privacy Mute (Local Conversation Mode)
* **Problem:** When two riders stop side-by-side at a stoplight or roadside with visors raised, their open helmet mics cause acoustic feedback and broadcast private discussions to the entire mesh group.
* **Automated Proximity Muting:**
  * **Condition:** Vehicle at rest ($v = 0\,\text{km/h}$) AND extreme proximity detected ($< 3\,\text{m}$, 2.4 GHz RSSI $> -45\,\text{dBm}$ to partner bike).
  * OMB automatically mutes helmet mic transmission to the wide-area group mesh (playing a subtle confirmation chime: *"Local Mode"*).
  * Riders speak naturally face-to-face through open visors.
  * Resuming riding ($v > 8\,\text{km/h}$) or single-clicking PTT instantly reopens the group mesh.

### 5.7 Action Cam Event Tagging & Video Telemetry (.srt / .csv)
* **Automated Incident Bookmarking:**
  * In addition to manual PTT bookmarking for scenic viewpoints, the Front Node automatically fires a BLE bookmark to GoPro / Insta360 cameras on safety events:
    * Emergency braking ($a_x < -6.0\,\text{m/s}^2$)
    * Radar collision hazard RED ($\text{TTC} < 2.5\,\text{s}$)
    * eCall crash detection ($> 6.5\,\text{g}$)
  * Eliminates tedious scrubbing through hours of raw tour footage to locate critical traffic incidents.
* **Video Telemetry Export:**
  * The PWA exports time-synchronized `.srt` or `.csv` telemetry alongside GPX tracks, enabling pixel-perfect speed, lean angle, and radar hazard overlays in Dashware or Insta360 Studio.

### 5.8 2-in-1 LoRa Smart-Keyfob (Alarm-Pager, N52 Key & MagSafe Qi Dock)
* **All-in-One Keychain Token:**
  * Combines the $20 \times 10 \times 5\,\text{mm}$ N52 neodymium magnetic key for cartridge mechanical latch release with a silent LoRa 868 MHz alarm pager inside a compact PA12-MJF enclosure ($58 \times 34 \times 13\,\text{mm}$).
  * An integrated $0{,}5\,\text{mm}$ mu-metal shield isolates internal electronics, LRA actuator, and LiPo cell from magnetic saturation.
* **Rechargeable LiPo & MagSafe Cockpit Docking:**
  * Features a rechargeable 250 mAh 1S LiPo pouch cell, eliminating coin-cell failures in sub-zero winter rides.
  * Recharges inductively whenever snapped onto the PCBA 06 MagSafe frame dock at the handlebar.
* **Tactile LRA & Acoustic Alerting:**
  * Powered by a TI DRV2605L driver driving a $10 \times 3{,}6\,\text{mm}$ LRA coin motor for crisp pre-alarm clicks and crescendo theft alarms easily felt through heavy leather riding gear.

### 5.9 Active Safety Light Management (ESS Hazard Strobe & Aux Light J11)
* **Emergency Stop Signal (ESS):**
  * Monitors longitudinal deceleration $a_x$ via the 6-axis IMU (default threshold $a_x < -0{,}60\,\text{g}$).
  * On emergency hard braking, OMB pulses the Garmin Varia taillight and auxiliary indicators with high-frequency **4.5 Hz stroboscopic hazard flashing** to alert trailing traffic.
* **Auxiliary Headlights (Front Node J11 via TPS1H100):**
  * The 4.5A smart high-side switch drives auxiliary LED fog/driving lights across three modes: `[OFF]`, `[ALWAYS-ON]`, or `[AUTO-STROBE ON ESS]`.

### 5.10 Apple Find My & Google Find My Device Crowdsourced Tracking (Dual-Beaconing)
* **Global Tracking with Zero SIM & Zero Monthly Fees:**
  * In standby / deep sleep, the ESP32-S3 broadcasts alternating **Apple Find My (FMNP)** and **Google Find My Device (FMDN)** BLE advertisements every 2.0 seconds ($2{,}5\,\text{ms}$ duration).
  * Leverages over **~1.5 billion iPhones and ~3 billion Android smartphones** globally to locate stolen motorcycles even inside underground parking garages and unfamiliar cities.
* **Ultra-Low-Power Autonomous Endurance:**
  * Dual-beaconing draws an average current of only $\approx 15\,\mu\text{A}$.
  * Combined with IMU wake-on-motion ($6\,\mu\text{A}$), the internal **2,200 mAh LiPo backup cell** delivers **3 to 4 years of autonomous tracking readiness**, even if thieves sever the motorcycle's 12V starter battery.

### 5.11 Smart Docking Telemetry & "Phone Left-Behind" Alerting
* **Workflow-Agnostic Correlation Engine:**
  * Riders frequently start the motorcycle while their phone is still in their jacket pocket, docking it on the handlebar (Qi `J10` / USB `J5`) or in the glove box (`J5_MP3`) minutes later after engine warmup.
  * The smartphone connects over Bluetooth LE on startup. Once placed in the dock, the smartphone reports its charging state (`battery.charging == true`) over BLE, allowing OMB to immediately correlate charging current with the rider's identity.
* **3-Tier Device Detection Matrix:**
  * *USB Memory Stick / MP3 Player (Class `0x08`):* Minimal current draw ($< 0{,}5\,\text{W}$), media mounted locally, **zero false alarms** on departure.
  * *Rider Smartphone:* High USB-PD ($> 15\,\text{W}$) or Qi ($10\dots 15\,\text{W}$) charging draw with active BLE owner handshake.
  * *Guest Device:* Neutral charging without dashboard profile changes.
* **Single-Edge Transition & Left-Behind Warning:**
  * Automatic switching to the Cockpit view executes **strictly once upon the rising edge** of docking. Manual navigation to other tabs is strictly respected without force-redirecting (User Override Protection).
  * If the rider turns ignition OFF (`KL15 == 0`) and walks away ($d > 3\,\text{m}$) while Qi or USB still detects a seated smartphone, the system sounds two rapid horn chirps and vibrates the Smart-Keyfob to prevent leaving expensive phones behind.
* **Architectural Decision Regarding UWB (Ultra-Wideband):**
  * Because OpenMotorBridge serves as an accessory, telemetry, and alarm platform while ignition control remains with the OEM lock and transponder, UWB (high quiescent draw 30–50 mA, specialized silicon, antenna tuning) represents unnecessary **overengineering** and is deliberately omitted in favor of BLE, LoRa, and Find My Device.

### 5.12 Cognitive Cockpit Decluttering & Silent Background Protection
* **Strict Demarcation: When Automation Acts – and When It Stays Silent:**
  * Digital telemetry and automated alerts trigger exclusively where human voice or perception physically fails:
    1. **Crash Detection & eCall on Incapacitation:** If a rider lies motionless in a ditch following an impact with $> 6.5\,\text{g}$ and $> 70^\circ$ lean angle, they are often unconscious or their helmet cable has severed. Here, the autonomous LoRa emergency broadcast (868 MHz) floods GPS distress packets to the entire group.
    2. **Group Separation Beyond Audio Range (Lost-Rider Tracking):** If the gap to the sweep rider in mountain terrain exceeds the 2.4 GHz audio range ($> 1.5\,\text{km}$), an 868 MHz LoRa packet silently alerts the lead rider with the exact distance to the separated member.
    3. **Invisible Hazard Zones:** Vehicles approaching rapidly ($+60\,\text{km/h}$) in the blind spot (Garmin Varia rear radar) or creeping tire pressure loss (TPMS) are caught before motorcycle stability is compromised.
    4. **Silent Parking Sentry (Ignition OFF):** Tampering with the parked motorcycle silently triggers the 2-in-1 LoRa Smart-Keyfob (LRA haptic pager) in the rider's jacket pocket.
* **Strict Ban on Riding-Time Push Alerts ($v > 0$):**
  * General traffic congestion alerts, weather radar text summaries, and CAN fuel broadcast spam are strictly banned from pushing onto the screen while in motion. The rider's cognitive bandwidth remains 100% dedicated to vehicle control and apex sightlines.

### 5.13 Support Vehicle & Van Architecture (Rally, Sweep Vehicle, Tour Operations)
* **The Role of the Support Vehicle in Organized Groups:**
  * During alpine tours, guided motorcycle adventures, desert rallies, or riding academies, a support vehicle (van, transporter, motorhome/RV) often follows the convoy as a luggage carrier, tool transport, mobile workshop, or sweep vehicle.
  * Conventional motorcycle electronics fail in automobiles because the closed sheet-metal chassis acts as a heavily attenuating Faraday cage, and motorcycle intercoms lack RF penetration into an enclosed car cabin.
* **OpenMotorBridge Support-Van Kit (Reference Kit 5):**
  * **Rear Pod 3 as Sun Visor Transceiver:**
    * Rear Pod 3 (PCBA 04 with LoRa SX1262 and u-blox MAX-M10S) clips onto the passenger sun visor using the tool-free snap bracket ([`car_sun_visor_pod3_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod3_clip.stl)).
    * **RF Physics Advantage:** Antennas radiate forward and laterally through the glass automotive windshield — **100% free of metallic chassis attenuation and Faraday shielding**.
  * **Satellite Pods 1 & 2 for Intercom & Radio (3M Dual-Lock):**
    * Pod 1 (e.g. Sena Mesh) and Pod 2 (e.g. Cardo DMC or Midland CB/PMR) attach vibration-isolated via 3M Dual-Lock mushroom tape to the dashboard beside the Central Box or concealed along the front seat console.
    * Because all pods (1, 2, 3) share identical monocoque enclosures ($135 \times 70 \times 26\,\text{mm}$), any pod can also snap into the sun visor clip if needed. Obsolete parcel-shelf mounting is eliminated due to lack of rigid shelves in modern vans/wagons and severe metallic RF shielding inside luggage trunks.
  * **Concealed Roof Headliner Routing:**
    * A 3 m ultra-flat USB-C ribbon cable routes invisibly behind the automotive headliner and down the rubber weatherstrip of the A-pillar to the dashboard.
  * **Central Box Docking & 12V Vehicle Power:**
    * The Central Box rests securely on the dashboard in the vibration-damped wedge dock ([`car_dashboard_wedge_dock.stl`](../../hardware/cad/stl/05_accessories/car_dashboard_wedge_dock.stl)).
    * Power is supplied tool-free via the included 12V/24V cigarette lighter adapter (30W USB-PD fast charger).
  * **Wireless Automotive Telemetry via Bluetooth OBD2 (ELM327 / vGate):**
    * The Central Box couples autonomously via Bluetooth 5.0 (BLE) to a compact OBD2 dongle plugged under the steering column.
    * Vehicle telemetry (speed, RPM, fuel tank level %, engine coolant temp) broadcasts into the 868 MHz LoRa mesh — zero footwell wiring and zero dependency on a smartphone/tablet app.
* **Real-Time Fleet Telemetry without Cellular Service (PWA Fleet Dashboard):**
  * An iPad or Android tablet mounted in the car runs the OpenMotorBridge PWA dashboard in offline vector map mode.
  * Over the 868 MHz LoRa mesh, the support crew receives second-by-second telemetry updates (GPS coordinate fixes, road speeds, crash/SOS alerts, tire pressures, ambient road temperature) from all group motorcycles over a radius of up to $15\,\text{km}$ — autonomous, robust, and completely independent of cellular network coverage.

