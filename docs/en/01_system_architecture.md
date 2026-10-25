# 01 - System Architecture, Universal Satellite Topology & Acoustics

This document specifies the overall system architecture of **OpenMotorBridge v10.0 (Native USB-PD & Edge-AI Generation)**, the universal satellite topology, vehicle-integrated mounting concepts (saddlebag, frame, tail, and riser docking with 100% wireless helmet comfort), RF coexistence, and seamless integration into modern OEM motorcycle infotainment systems.

---

## 1. Problem Statement & Architectural Philosophy

Classic motorcycle communication systems are historically fragmented:
* **Incompatible Mesh Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh, and analog PMR446 radio cannot communicate directly.
* **RF Overload & De-Sensing:** Operating multiple 2.4 GHz mesh transceivers in close proximity (e.g., on the same helmet or in a single enclosure) results in severe receiver desensitization (*De-Sensing*), intermodulation, and range drops of up to $80\,\%$.
* **Proprietary Infotainment Lock-in:** Systems like Harley-Davidson Boom! Box GTS / Skyline OS or BMW ConnectedRide require expensive OEM modules (such as the HD WHIM) to unlock Apple CarPlay or Android Auto.

**OpenMotorBridge v10.0** resolves these bottlenecks via a modular, decoupled **Satellite Topology**, interconnected via a **ruggedized 4-wire Automotive USB-PD & USB 2.0 bus (`VBUS`, `GND`, `D+`, `D-`)**, combined with the **ESP32-S31** (Edge-AI Audio) and a dedicated **Qualcomm QCC3084** Bluetooth audio SoC:

```
                                  SYSTEM TOPOLOGY OVERVIEW (v10.0)
+---------------------------------------------------------------------------------------------+
| 1. COCKPIT / HANDLEBAR & KEYFOB:                                                            |
|    * Front Node (PCBA 05): 60W USB-PD Engine, Modular Sensor-Puck ("Basket")                  |
|    * Symmetrical Dual Under-Perch Mirror Pods (Left: PTT & BSD | Right: Cam-Tag & BSD)      |
|    * 5-Port Glovebox Hub: 30W PD + 10W Dongle + Harley Headset Emulation via USB             |
|    * Smart Keyfob (PCBA 07): 868 MHz LoRa Pager (24/7 Anti-Theft Sentry & Emergency Beacon) |
|    * PWA Dashboard on Smartphone / TFT display via Web Bluetooth (WebBLE)                   |
+---------------------------------------------------------------------------------------------+
| 2. CENTRAL CONTROL BOX (Under-Seat / over battery bridge, IP67 Sealed):                     |
|    * ESP32-S31 Dual-Core RISC-V (320 MHz, 128-bit SIMD AI Accelerator for Audio Modeling)  |
|    * Qualcomm QCC3084 BT 5.4 Audio SoC (Dual-A2DP, aptX HD, HFP 1.8, Auracast, zero jitter) |
|    * Semtech SX1262 LoRa (868 MHz) on UPS rail * Taoglas FXP895 flex antenna in bridge       |
|    * Multi-Port Automotive USB-PD Power-Engine & High-Speed USB 2.0 Hub                     |
|    * Dual-Power Input: 12V Vehicle OR USB-PD Sink (5V-20V USB-C for Bench/Desk)             |
|    * LM5164-Q1 72V Step-Down * Dual Ideal-Diode OR-ing * BQ24075 UPS & 2200mAh LiPo Backup   |
|    * Two-Cable Architecture: 6-Pin DTM (Bordnetz/CAN) + 16-Pin Periphery Bus (4 Branches)   |
+--+---------------------------------------------------------------------------------------+--+
   |                                                                                       |
   v 16-Pin Automotive Peripherie Bus (Splits externally into 4 independent 4-wire branches)   |
+-----------------------------------------+-----------------------------------------------+
| 3. SATELLITE POD 1 (Saddlebag L, 30W):  | 4. SATELLITE POD 2 (Saddlebag R, 30W):        |
| * Slide-in Lid with FOB Magnetic Lock   | * Slide-in Lid with FOB Magnetic Lock         |
| * Intermediate Dry-Flap Guard           | * Intermediate Dry-Flap Guard                 |
| * Dual Mechatronic Pushers on Universal | * Dual Mechatronic Pushers on Universal       |
|   Slide Rails ("One Size Fits All",     |   Slide Rails ("One Size Fits All",           |
|   2.0s Cold-Start Pulse on KL15)        |   2.0s Cold-Start Pulse on KL15)              |
| * In-Bag USB Charging Port (30W USB-PD) | * In-Bag USB Charging Port (30W USB-PD)       |
| * Weatherproof Outdoor USB Port (GS/ST) | * Weatherproof Outdoor USB Port (GS/ST)       |
| * 4-Pin Magnetic Breakaway Coupling IP68| * 4-Pin Magnetic Breakaway Coupling IP68     |
+-----------------------------------------+-----------------------------------------------+
   |                                                                                       |
   +-> 5. VEHICLE POWER & CAN (Cable 1): 6-Pin Deutsch DTM (KL30, KL15, GND, CAN_H, CAN_L, Shield)
   +-> 6. REAR RADAR (Branch 4): 4-Wire 12V Power & High-Speed CAN / Serial                |
   |      Wheeltec MR20 77-GHz mmWave (PCBA 08) * 36x Alert LEDs * Drip-Loop & Roost Defl. |
   |                                                                                       |
   v Branch 1: 4-Wire Automotive Backbone (60W Power & High-Speed Bus through Frame Tunnel) |
+-----------------------------------------------------------------------------------------+
| 7. FRONT NODE & COCKPIT HUB (PCBA 05 at Riser / Triple Tree, 60W Power Budget):         |
| * Modular Sensor-Puck ("Basket"): SAM-M10Q GNSS, TMP117, OPT3001, Knowles MEMS           |
| * 60W USB-PD Power: 27W Phone + 15W Navi + 10W Action-Cam + Dual Cockpit OLED Displays   |
| * Feeds Dual Cockpit Speaker Corner Pods (2x OLED displays inside Rockford speaker grilles) |
| * Feeds 5-Port Glovebox Hub & provides Harley Headset Emulation via USB                 |
| * Direct interface to Symmetrical Dual Under-Perch Mirror Pods (Left PTT, Right Cam-Tag)|
+-----------------------------------------------------------------------------------------+
| 8. SUPPORT VEHICLE TOPOLOGY (Car / Support-Van / Rally Sweep Vehicle / RV):             |
| * All-in-One Car Support Core Unit: Central Box & Front Node consolidated               |
| * Detachable Sensor-Puck ("Basket") docked to windshield/dashboard via 1.5m lead       |
| * 5-Port Media Hub & CarPlay Clean Power-Injection with OEM Media-USB Passthrough        |
| * 2 Pods on Sun Visors: Driver Pod 1, Passenger Pod 2 (Sena/Cardo or OMM/Midland)       |
| * External 868 MHz Magnetic Roof Antenna standard (15-25 km LoRa range to bike group)   |
+-----------------------------------------------------------------------------------------+
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

OpenMotorBridge v10.0 defines the platform across **standardized functional nodes** without redundant pods or wiring bloat:
1. **Central Control Box (Main ECU * PCBA 01):** Computational core (**ESP32-S31** Dual-Core RISC-V @ 320 MHz with 128-bit SIMD AI accelerator for on-device voice/audio classification), dedicated **Qualcomm QCC3084** Bluetooth 5.4 Audio SoC (Dual-A2DP, aptX HD, HFP 1.8, Auracast without host jitter), multi-port automotive USB-PD power engine, 72V automotive step-down (LM5164-Q1), and LiPo UPS (BQ24075 with 2,200 mAh flat pouch cell). **Dual-Power Input:** In addition to 12V vehicle power, the Central Box supports a **USB-PD Sink input (5V–20V)** via its native USB-C port with ideal-diode OR-ing -- enabling complete benchtop flashing, testing, and sensor calibration using any standard smartphone or laptop charger without requiring a 12V bench power supply. **Two-Cable Architecture:** Cable 1 (6-Pin Deutsch DTM) for vehicle net & CAN; Cable 2 (16-Pin Automotive Connector) for the 4 autonomous system branches (Front Node 60W, Pod 1 30W, Pod 2 30W, Radar MR20 12V). Houses the **Semtech SX1262 LoRa transceiver (868 MHz)** directly on the UPS rail. *(Mounted centrally under seat over battery bridge).*
2. **Satellite Pod 1 (Saddlebag Left, 30W Budget):** Universal saddlebag pod featuring a **slide-in lid**, captive **FOB magnetic latch** (proximity release using the smart keyfob), internal **intermediate dry-flap splash guard**, **integrated in-bag USB charging port (30W USB-PD)**, and weatherproof outdoor port (IP68 cap & rain charging gasket collar). Houses `PCBA 03` interface board for Sena SPIDER X, Cardo Packtalk Edge, UCS standard, OMM 2.4 GHz, or Midland PMR446. **Mechatronic Cold-Start:** Dual mechatronic pushers (mini-solenoids) on universal slide rails (`012_universal_actuator_slide_bracket.scad`) fire a simultaneous 2.0s push impulse on KL15 ignition ON ("One Size Fits All" – no standby battery drain during weeks of downtime, no soldering, no pod disassembly). Interconnected via 4-wire bus with 4-pin IP68 magnetic breakaway coupling.
3. **Satellite Pod 2 (Saddlebag Right, 30W Budget):** Fully symmetrical universal saddlebag pod with slide-in lid, FOB magnetic latch, dry-flap, internal 30W USB charging port, outdoor port, and mechatronic dual pushers (dual identical intercoms supported, e.g. 2x Cardo or 2x Sena in separate mesh channels).
4. **Front Node & Cockpit Hub (PCBA 05 at Riser, 60W Power Budget):** Mounted on handlebar riser / triple tree. **60W USB-PD Power Engine** (Southchip SC8721/SC8102 Synchronous Buck-Boost) reliably feeds driver phone fast-charging (up to 27W), dedicated motorcycle GPS (15W for Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), action-cam continuous power (10W via weather-sealed USB-C lead), dual cockpit OLED displays (2W in Speaker Corner Pods), and sensors/host MCU/hub (3.5W). **Modular Sensor-Puck ("Basket"):** Integrates **u-blox SAM-M10Q Multi-GNSS**, **TI TMP117** thermometer, **OPT3001** light sensor, and **Knowles MEMS wind microphone**; snaps directly onto Front Node on bikes, or docks to car windshield via 1.5m extension lead. Directly interfaces to symmetrical dual under-perch mirror pods. Connected to Central Box via 4-wire backbone through Harley frame tunnel (**ZERO tank lifting required!**).
5. **Symmetrical Dual Under-Perch Mirror Pods (Left & Right):** Form-fitted and aerodynamic brackets clamped directly under both mirror perch studs.
   * **Left Mirror Pod:** Tactile thumb button (Factory default: PTT intercom/radio & voice assistant) + left directed amber blind-spot warning LED (BSD) aimed at left mirror reflection.
   * **Right Mirror Pod:** Tactile thumb button (Factory default: Short-press: Highlight Tag / Bookmark for Insta360/GoPro/DJI via BLE; Long-press: Video Record Start/Stop or SOS) + right directed amber blind-spot warning LED (BSD) aimed at right mirror reflection.
   * **100% Software-Defined Button Mapping (Freely Remappable via PWA):** The physical switches are software-defined and freely configurable (short-press, double-click, long-press for PTT, hazard pins, cam tags, garage doors via BLE).
   * **Safety Advantage:** True bilateral blind-spot detection directly in the rider's peripheral mirror glance angle. 100% symmetrical cockpit ergonomics with identical internal electronics (`PCBA 05B`).
6. **5-Port Glovebox Media & Power-Injection Hub (`glovebox_power_injection_hub.scad`):** Located in the right fairing glove box of Touring baggers (Road Glide, Street Glide, CVO, CVO ST). Powered from Front Node (`PCBA 05`) via a combined high-power & USB 2.0 cable. Taps the OEM Harley USB-C port to head unit (Skyline OS / Boom! Box) and injects regulated **30W USB-PD** (thermally safe for closed compartments) for phone charging plus **10W switched dongle power** (Wireless CarPlay / Android Auto with thermal protection gating). 1x free media USB 2.0 port for flash drives and dealer updates. **Harley Headset Emulation via USB:** High-speed data pair connects Front Node directly to Port 5 for OEM head unit; emulates MFi / USB Audio Class headset, unlocks Apple CarPlay natively, and routes helmet mic audio digitally without ground loops.
7. **Radar 2.0 Sub-MCU & Rear Warning Wings (PCBA 08 at Rear):** Autonomous 77-GHz rear radar (Wheeltec MR20), fed via branch 4 of the 16-pin periphery harness; 36x strobe warning LEDs, downward drip-loop, and roost deflector. Optional under-fender mount for cruiser/bobber builds.

```
                     THE STANDARDIZED FUNCTIONAL NODES (v10.0)
+-----------------------------------------------------------------------------+
| 1. FRONT NODE (At Handlebar Riser): SAM-M10Q GNSS, Airflow Sensors,         |
|    Knowles Wind MEMS, Qi/USB-PD Accessory Power, Riser Bar Clamp            |
+-----------------------------------------------------------------------------+
| 2. SYMMETRICAL DUAL UNDER-PERCH MIRROR PODS (Left & Right):                 |
|    * Left:  Tactile Button (Default: PTT), Left Blind-Spot Alert LED (BSD)   |
|    * Right: Tactile Button (Default: Cam-Tag), Right Blind-Spot Alert LED    |
|    * 100% Software-Defined: Freely remappable via PWA (PTT/Cam/Voice/SOS)    |
+-----------------------------------------------------------------------------+
| 3. GLOVE BOX HUB (Right Box): 2-Port USB Hub, bottom OEM grommet entry,     |
|    stable Ottocast CarPlay/AA bypass, 1x free USB charging port             |
+-----------------------------------------------------------------------------+
| 4. CENTRAL BOX (Under Seat/Batt): ESP32-S31 AI Host, QCC3084 Audio SoC,     |
|    SX1262 LoRa 868MHz, Multi-Port USB-PD Engine, UPS, Two-Cable Connection  |
|    Dual-Power Input: 12V Vehicle OR USB-PD Sink (5V-20V for Bench/Desk)     |
+------------------------------+----------------------------------------------+
| 5. POD 1 (Saddlebag Left):   | 6. POD 2 (Saddlebag Right):                  |
| * Slide-in Lid & FOB Lock    | * Slide-in Lid & FOB Lock                    |
| * Intermediate Dry-Flap      | * Intermediate Dry-Flap                      |
| * In-Bag USB Charging Port   | * In-Bag USB Charging Port                   |
| * 4-Pin Magnetic Breakaway   | * 4-Pin Magnetic Breakaway                   |
+------------------------------+----------------------------------------------+
| 7. REAR RADAR 2.0 (License Plate): Wheeltec MR20 77-GHz, 36x Alert LEDs     |
+-----------------------------------------------------------------------------+
```

> [!NOTE]
> **Mounting Freedom - *Your Bike, Your Choice*:**  
> Where and how you place these modules on your motorcycle or vehicle is deliberately **entirely up to you**! OpenMotorBridge provides the standardized electronic layouts, enclosure dimensions, and interfaces.  
> For popular motorcycle categories and support vehicles, we deliver turnkey, 100% zero-drill and adhesive-free **Reference Mounting Kits** in **[Chapter 08 (Mechanics & CAD)](08_enclosures_mechanics_cad.md)**:
> * **Reference Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring FLTRX/FLHX):**
>   - **ZERO OUTER FAIRING REMOVAL:** Never pry the painted Sharknose outer shell or Rockford Fosgate speaker grilles! The outer fairing remains 100% untouched.
>   - **ZERO FUEL TANK LIFTING:** 4-wire backbone cable is pulled through the open factory backbone wire caddy in 5 minutes using a nylon fish tape. Tank stays bolted in place.
>   - **Front Node at Riser / Triple Tree:** Optimal ambient airflow cooling ($< 35^\circ\text{C}$), unobstructed GNSS sky view.
>   - **Symmetrical Dual Under-Perch Mirror Pods:** Left PTT & BSD alert LED; Right Cam-Tag & BSD alert LED under mirror studs.
>   - **Glove Box Entry from Below:** Routed through the OEM rubber floor grommet (never pinching cables over door seals).
>   - **Pods 1 & 2 on Saddlebag Inner Walls:** Slide-in lid with FOB magnetic latch, dry-flap, and in-bag USB charging; 4-pin magnetic breakaway coupling on frame.
>   - **Central Box:** In battery tray under the seat. Dual-power input for desk diagnostics. Rear radar on license plate bracket.
> * **Reference Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pods 1 & 2 in saddlebags, Front Node at riser clamp / headlight nacelle, Central Box under seat.
> * **Reference Kit 3 (Classic Bagger & Cruiser - Street Glide / Electra Glide):** Pods 1 & 2 in saddlebags, Front Node at riser / batwing handlebar mount, Central Box under seat.
> * **Reference Kit 4 (Adventure & Touring Enduros - BMW GS, KTM Adventure, Africa Twin):** Pods 1 & 2 mounted strictly vehicle-fixed on crash bars / luggage rack (never inside aluminum cases!). Front Node on nav crossbar above TFT. Radar on rear luggage rack.
> * **Reference Kit 5 (Car / Support-Van / Rally Sweep Vehicle / RV):** All-in-One Car Support Core Unit (Central Box + Front Node consolidated), AAWireless Power Bypass (5V 3A clean power injection, pure data link to car head unit), 2 Pods on sun visors via quick-release clips, external roof magnetic LoRa antenna.

### 2.1 Whitepaper Design Rationale: Decentralized Satellite Topology vs. Monolithic Single-Box

During the initial concept phase, an in-depth engineering evaluation analyzed whether the entire system should be housed within a single, large central enclosure (e.g. under the seat or behind the front fairing). The monolithic approach was unanimously rejected after electromagnetic simulation and physical prototyping:

#### Evaluation Matrix: Monolithic Single-Box vs. OpenMotorBridge Decentralized Satellite Architecture

| Evaluation Metric | Option A: Monolithic Single-Box | Option B: Handlebar/Cockpit-Only Box | **Option C: OMB Decentralized Satellites (Selected)** |
| :--- | :--- | :--- | :--- |
| **RF Self-Interference (De-Sensing)** | **Critical:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V buck converter in extreme proximity | **Critical:** Severe cross-talk into cockpit TFT and motorcycle radio antenna | **Optimal (> 45 dB Isolation):** GNSS at front air intake, LoRa in Central Box, Intercoms on lateral flanks |
| **Harness Bundle Diameter** | **Bulky:** 26+ discrete wire conductors routed through the motorcycle chassis | **Poor:** 18 conductors routed across the pivoting steering head (harness fatigue risk) | **Ultra-Slim:** Two-Cable Architecture with 4-wire USB-PD/data branches; ZERO tank lifting in frame caddy |
| **Thermal Dissipation** | **Hot-Spot (> 18 W):** 72V DC/DC + audio power amplifiers + battery charging under seat | **Thermal Overheating (> 85 °C):** Trapped heat accumulation directly behind headlight nacelle | **Evenly Distributed:** Max. 3-4 W per enclosure; passive convection cooling with zero hot-spots |
| **GNSS Zenith View & Radar** | **Obstructed:** Seat bench and rider's body block satellites & rear radar aperture | **Poor:** Rear blind-spot radar from handlebars is physically impossible | **Ideal:** Front Node SAM-M10Q has clear forward sky view; Rear Radar mounts directly on luggage/plate |
| **Dynamic Wind Sampling (AGC)** | **Physically impossible:** Zero dynamic ram-air pressure underneath the seat | **Feasible:** Wind pressure measurement directly at handlebar | **Excellent:** Knowles I2S MEMS positioned directly at windshield line in Front Node |

1. **Physics of RF Coexistence (Mitigating Receiver De-Sensitization):**
   * GNSS satellite signals reach the ground at ultra-low power levels of approximately **$-130\,\text{dBm}$ to $-160\,\text{dBm}$**.
   * Placing a high-voltage switching regulator, an 868 MHz LoRa transmitter, and dual 2.4 GHz mesh radios inside the same metallic chassis within inches of each other lifts the wideband thermal noise floor (*Noise Floor Lift*).
   * By placing the SAM-M10Q GNSS module in the Front Node in the cold air scoop, moving the internal vehicle backbone to the shielded **4-wire Automotive USB-PD & USB 2.0 bus**, housing LoRa 868 MHz in the Central Box, and placing Pods 1 & 2 on the lateral flanks, mutual RF degradation is eliminated.
2. **Harness Reliability Across the Steering Head:**
   * Every copper conductor traversing the rotating steering head suffers millions of bending cycles over a motorcycle's operational life.
   * By segregating cockpit, USB display, and PTT functions into the **Front Node (PCBA 05)** connected over the ruggedized **4-wire Automotive Backbone cable** pulled through the Harley frame wire caddy without tank removal, zero fragile data signal wires cross the steering axis.
3. **Conclusion:** Maximum signal integrity, zero thermal hot-spots, superior long-term mechanical reliability, and unmatched installation flexibility across all motorcycle categories.k.stl)) on dashboard with 12V cigarette lighter PD adapter; autonomous Bluetooth OBD2 telemetry (ELM327 / vGate) coupled directly to Central Box; PWA dashboard on iPad/tablet for live tracking of all group bikes without cellular connectivity.
>
> Riders and support crews are encouraged to replicate these kits, adapt them for other vehicle models, or design custom brackets based on our open CAD/STEP dimensional envelopes!

### 2.1 Whitepaper Design Rationale: Decentralized Satellite Topology vs. Monolithic Single-Box

During the initial concept phase, an in-depth engineering evaluation analyzed whether the entire system should be housed within a single, large central enclosure (e.g. under the seat or behind the front fairing). The monolithic approach was unanimously rejected after electromagnetic simulation and physical prototyping:

#### Evaluation Matrix: Monolithic Single-Box vs. OpenMotorBridge Decentralized Satellite Architecture

| Evaluation Metric | Option A: Monolithic Single-Box | Option B: Handlebar/Cockpit-Only Box | **Option C: OMB Decentralized Satellites (Selected)** |
| :--- | :--- | :--- | :--- |
| **RF Self-Interference (De-Sensing)** | **Critical:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V buck converter in extreme proximity | **Critical:** Severe cross-talk into cockpit TFT and motorcycle radio antenna | **Optimal (> 45 dB Isolation):** GNSS on Front Node (windshield line), LoRa on Central Box (under seat), Intercoms on lateral flanks |
| **Harness Bundle Diameter** | **Bulky:** 26+ discrete wire conductors routed through the motorcycle chassis | **Poor:** 18 conductors routed across the pivoting steering head (harness fatigue risk) | **Ultra-Slim:** 4-wire Automotive Backbone routed through frame caddy without tank removal (< 0.2 ms) |
| **Thermal Dissipation** | **Hot-Spot (> 18 W):** 72V DC/DC + audio power amplifiers + battery charging under seat | **Thermal Overheating (> 85 °C):** Trapped heat accumulation directly behind headlight nacelle | **Evenly Distributed:** Max. 3-4 W per enclosure; passive convection cooling with zero hot-spots |
| **GNSS Zenith View & Radar** | **Obstructed:** Seat bench and rider's body block satellites & rear radar aperture | **Poor:** Rear blind-spot radar from handlebars is physically impossible | **Ideal:** Front Node SAM-M10Q has unobstructed 360° sky view, rear radar on Peitsche 5 sits clear at tail |
| **Dynamic Wind Sampling (AGC)** | **Physically impossible:** Zero dynamic ram-air pressure underneath the seat | **Feasible:** Wind pressure measurement directly at handlebar | **Excellent:** Knowles I2S MEMS positioned directly at windshield line in Front Node |

1. **Physics of RF Coexistence (Mitigating Receiver De-Sensitization):**
   * GNSS satellite signals reach the ground at ultra-low power levels of approximately **$-130\,\text{dBm}$ to $-160\,\text{dBm}$**.
   * Placing a high-voltage switching regulator (LM5164-Q1 with fast switching edges), an 868 MHz LoRa transmitter (+22 dBm / 160 mW), and dual 2.4 GHz mesh radios inside the same metallic chassis within inches of each other lifts the wideband thermal noise floor (*Noise Floor Lift*). The GNSS receiver suffers cycle slips, losing carrier phase lock and degrading precision.
   * Physical spatial separation (Front Node SAM-M10Q in cockpit nacelle, Central Box under seat, Pods 1 & 2 on lateral flanks) naturally enforces **$> 45\,\text{dB}$ of free-space path loss** between RF stages.
2. **Harness Reliability Across the Steering Head:**
   * Every copper conductor traversing the rotating steering head suffers millions of bending cycles over a motorcycle's operational life.
   * By segregating cockpit, USB display, and PTT functions into the **Front Node (PCBA 05)** connected over the ruggedized **4-wire Automotive Backbone cable** pulled through the Harley frame wire caddy without tank removal, zero fragile data signal wires cross the steering axis.
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
The universal monocoque pods ($150 \times 70 \times 38\,\text{mm}$ with tool-free slide-in lid, dry-flap, and $124 \times 53 \times 28\,\text{mm}$ interior cavity) accommodate all commercial off-the-shelf OEM adapters directly in the upper cradle:
* **Class S (Direct Pod Cradle * OMB Reference):** e.g. Sena SPIDER X Slim (primary recommendation), Cardo Packtalk Edge (Air-Mount), OMM UCS 2.4 GHz - 100% factory-unopened original device seated in a PA12-MJF form-fit cradle with 3-point EPDM damping against $20\,\text{g}$ shock/vibration, directly interfaced to PCBA 03 (USB-PD charging up to 30W, USB Audio Class, direct electrical PTT keying or BLE control), zero pogo pins, zero soldering, 100% preservation of warranty and IP67 weatherproofing. Brittle swap cartridges and solenoids are completely eliminated.
* **Class A (Wireless Bridges & USB Power):** e.g. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red - powered via internal USB-C port, wireless audio to helmet.
* **Class B (Pogo-Pin Cradles):** e.g. Sena 50S/60S/30K/20S EVO - analog audio via ES8388 codec on PCBA 03 and PTT keying via AO3400A MOSFETs.
* **Class C (Magnetic Air-Mount):** e.g. Cardo Packtalk Edge / Pro - tool-free magnetic docking via 2x N52 neodymium magnets.
* **Class D (Slide Cradles):** e.g. Cardo Packtalk Bold/Black, Freecom series - mechanical slide rail.
* **Class E (Analog PMR446 Radio):** e.g. Midland G7/G9 Pro, XT30 - dual-jack connection with PhotoMOS PTT keying.
*(Detailed wiring matrix and pinouts available in [Specification 02 (Intercom Matrix & Profiles)](02_intercom_matrix_profiles.md)).*

---

## 3. RF Coexistence, Spectrum Cleansing & Spatial Diversity (> 35 dB Isolation)

When operating multiple wireless transceivers simultaneously, RF congestion and receiver de-sensitization must be eliminated:

1. **Elimination of Cockpit 2.4 GHz Congestion via 4-Wire Automotive Bus:**
   * Traditional wireless motorcycle networks crowd all data, audio, and sensor streams onto 2.4 GHz (Bluetooth, Wi-Fi, ESP-NOW), causing severe packet collisions and latency spikes.
   * OpenMotorBridge completely decouples internal vehicle telemetry by migrating the Front Node <-> Central Box backbone link to the shielded **4-wire Automotive USB-PD & USB 2.0 bus (`VBUS`, `GND`, `D+`, `D-`)**.
   * **Zero RF Interference & Zero De-Sensing:** Eliminating short-range wireless backbones ensures zero RF desensitization of cockpit GNSS or helmet Bluetooth, and guarantees deterministic $< 0.2\,\text{ms}$ latency even through wet luggage or aluminum panniers.
2. **Physical Separation ($d \ge 45\,\text{cm}$ via Lateral Flank Placement):**
   * **Zero Pods on Helmets:** The weather-sealed universal monocoque pods ($150 \times 70 \times 38\,\text{mm}$) remain permanently mounted on the vehicle (e.g. left and right saddlebag lids, frame tubes, or crash bars). Rider and pillion helmets remain 100% cable-free.
   * **Metallic Barrier:** Pod 1 (left vehicle flank / left saddlebag) and Pod 2 (right vehicle flank / right saddlebag) utilize the motorcycle's steel/aluminum chassis, fuel tank, and engine block as a natural metallic shield, delivering **$> 35\,\text{dB}$ of free-space and absorption isolation**.
3. **Clean Spectrum Allocation Matrix:**
   * **4-Wire Automotive Bus:** Wired vehicle backbone (Front Node <-> Central Box, $< 0.2\,\text{ms}$ deterministic latency, 60W USB-PD).
   * **868 MHz (LoRa):** Long-range emergency fallback, tactical GPS telemetry, and 24/7 anti-theft sentry directly on Central Box PCBA 01.
   * **2.4 GHz:** Strictly reserved for external helmet audio links (Pod 1 Sena, Pod 2 Cardo) and smartphone BLE.
   * **5 GHz Wi-Fi:** Reserved for wireless Apple CarPlay / Android Auto (CP2AA bridge).

---

## 4. Physical Interfaces & Signal Matrix

### 4.1 Central Box Two-Cable Architecture (Vehicle Power, CAN & 16-Pin Periphery Bus)
To prevent cable clutter and resolve pin count limitations, OpenMotorBridge v10.0 strictly separates vehicle-side power/CAN from the modular OMB periphery bus via **two separate, sealed automotive-grade industrial connectors (IP67/IP69K)** on the Central Box front face:

#### A. Cable 1: Vehicle Power & CAN Bus (6-Pin Deutsch DTM06-6S)
Direct connection to vehicle battery, ignition switch, and OEM CAN network:
* **Pin 1:** `KL30_IN` (+12V fused continuous battery power, AWG20 0.5 mm²)
* **Pin 2:** `KL15_IGN` (+12V ignition switched wake-up & voltage sense, AWG22 0.34 mm²)
* **Pin 3:** `VEHICLE_GND` (Chassis ground / battery negative, AWG20 0.5 mm²)
* **Pin 4:** `CAN_H` (High-Speed CAN per ISO 11898-2, AWG24 0.22 mm²)
* **Pin 5:** `CAN_L` (Low-Speed / Dominant CAN per ISO 11898-2, AWG24 0.22 mm²)
* **Pin 6:** `CHASSIS_SHIELD` (Frame earth / braided EMI shield)

#### B. Cable 2: OMB Periphery Bus (16-Pin Automotive Connector, e.g. TE Superseal / Deutsch DTM 16-Pin)
Carries 4 autonomous system branches (each with 4 conductors: `VCC`, `GND`, `D+`, `D-`) and breaks out externally within the protected vehicle harness into 4 dedicated branch pigtails:

| Branch / Pigtail | Connector Type | Target Device | Power & Transferred Signals |
| :--- | :--- | :--- | :--- |
| **Branch 1 (Front Backbone)** | 4-Pin Automotive Sealed | **Front Node & Cockpit** (PCBA 05) | **60W USB-PD** (`VBUS_60W`, AWG18), `GND` (AWG18), `USB_D+` / `USB_D-` (AWG26 twisted) |
| **Branch 2 (Saddlebag Left)** | 4-Pin Magnetic Breakaway IP68 | **Satellite Pod 1** (Sena / Cardo / OMM) | **30W USB-PD** (`POD1_VBUS`, AWG20), `POD1_GND` (AWG20), `USB_D+` / `USB_D-` (AWG28 twisted) |
| **Branch 3 (Saddlebag Right)** | 4-Pin Magnetic Breakaway IP68 | **Satellite Pod 2** (Cardo / Sena / OMM) | **30W USB-PD** (`POD2_VBUS`, AWG20), `POD2_GND` (AWG20), `USB_D+` / `USB_D-` (AWG28 twisted) |
| **Branch 4 (Rear Radar)** | Binder M5 4-Pin IP67 | **Rear Radar MR20** (PCBA 08) | **12V Switched** (`RADAR_12V`, AWG22), `RADAR_GND` (AWG22), `CAN_H`/`TX`, `CAN_L`/`RX` |

### 4.2 Central Box (PCBA 01) RF & Sensor Interface Architecture
| Subsystem | Component | Location / Interface | Function |
| :--- | :--- | :--- | :--- |
| **LoRa 868 MHz** | Semtech SX1262 | Onboard PCBA 01 (SPI) | Long-range tactical telemetry & 24/7 theft sentry (FXP895 antenna in enclosure lid) |
| **Automotive Backbone Hub** | USB2514B / High-Speed USB | PCBA 01 | 4-wire Automotive USB-PD & USB 2.0 host engine managing Front Node (60W) and Pods (30W) |
| **CAN-Bus** | TI TCAN334G | Onboard PCBA 01 (Cable 1 DTM-6 pins 4/5) | Vehicle CAN telemetry & listen-only monitoring |
| **Dual-Bluetooth** | Qualcomm QCC3084 | Top side PCBA 01 (I2S/UART) | Dedicated dual-helmet A2DP/HFP audio gateway |
| **IMU** | Bosch BMI270 | Onboard PCBA 01 (I2C) | 6-DOF lean angle, acceleration, crash & tilt detection |
| **Barometer** | Bosch BMP390 | Onboard PCBA 01 (I2C) | Barometric weather trend & absolute pressure elevation |

### 4.3 Front Node (PCBA 05) Cockpit Interface Matrix (60W Power Budget)
| Port | Connector Type | Function | Connected Hardware |
| :--- | :--- | :--- | :--- |
| **`J1`** | JST-PH 2.0mm 2-Pin | 12V Switched Power | Auxiliary switched feed (KL15 & GND) for optional local taps |
| **`J2`** | JST-PH 2.0mm 3-Pin | Display Audio CAN | Cockpit CAN bus (CAN_H, CAN_L, GND) for Harley Skyline OS / TFT |
| **`J3`** | JST-PH 2.0mm 4-Pin | Handlebar Multi-Button Interface | 3x IP67 microswitches: PTT Intercom, Video Bookmark, Siri/Voice (< 1.8 ms) |
| **`J4`** | Molex Micro-Fit 4-Pin / USB | Combined Power & USB Upstream | Link to 5-Port Glovebox Hub (`glovebox_power_injection_hub.scad`) Port 5 for Headset Emulation & CarPlay |
| **`J5`** | USB-C Receptacle IP67 | 27W USB-PD Fast Charging | Handlebar smartphone (QuadLock / SP Connect) via SC8721/SC8102 Buck-Boost |
| **`J6`** | Molex Micro-Fit 4-Pin | Switched CarPlay Port | Wireless CP2AA dongle with 1-click TPS2051B cold reboot |
| **`J7`** | USB-C Onboard | Service & Flash Port | ESP32-S3 firmware update & WebSerial diagnostics |
| **`J8`** | JST-PH 2.0mm 2-Pin | 10W Action-Cam Power Supply | Weather-sealed direct USB-C lead for GoPro / Insta360 camera |
| **`J9`** | JST-PH 2.0mm 3-Pin | Blind-Spot Mirror LEDs | 2x amber 12V LEDs on mirror stems via N-MOSFET drivers L+R |
| **`J10`** | JST-PH 2.0mm 2-Pin | 15W Dedicated GPS Nav Feed | 12V/1.25A or 5V/3A DC power lead for Garmin Zūmo XT2 / Tread / Chigee AIO-5 |
| **`J11`** | JST-PH 2.0mm 2-Pin | Auxiliary Front Spotlights | Up to 4.5A high-side switched LED lights (auto-strobe on emergency stop) |
| **`J12`** | SparkFun Qwiic (JST-SH 4P) | Modular Sensor-Puck ("Basket") | **u-blox SAM-M10Q Multi-GNSS patch**, **TI TMP117** precision temp, **OPT3001** light sensor |
| **`J_BUS`** | 4-Pin JST-GH (1.25 mm) | 4-Wire Automotive Backbone | Branch 1: `VCC_BUS` (60W USB-PD), `GND`, `USB_D-`, `USB_D+` to Central Box (< 0.2 ms latency) |

---

## 5. Integration into OEM Infotainment Systems

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 Harley Headset Emulation via USB & Apple CarPlay / Android Auto Unlocking
* **Background & USB Emulation:** Apple CarPlay strictly mandates an active speech microphone. Harley-Davidson locks CarPlay in factory Boom! Box GTS and Skyline OS firmware unless either a wired 7-pin DIN headset or the proprietary **HD-WHIM** (*Wireless Headset Interface Module*, $> \$350$) is installed.
* **Digital Headset Emulation via USB:** OpenMotorBridge handles headset and microphone integration **100% digitally over USB**! Over the USB 2.0 High-Speed link from the Front Node (`PCBA 05`) routed through Port 5 of the 5-Port Glovebox Hub (`glovebox_power_injection_hub.scad`) into the OEM head unit, OpenMotorBridge enumerates as a compliant Apple MFi digital headset and USB Audio Class composite device.
* **Result:** Boom! Box GTS and Skyline OS instantly detect an active digital headset and unlock Apple CarPlay and Android Auto on the 6.5" or 12.3" touchscreen -- **without requiring the \$350 WHIM module**, without unreliable analog jumper plugs, and without dealer flashing (Digital Tech).
* **Bidirectional Digital Audio Integration:** Helmet microphone audio from both rider and passenger is packetized and streamed digitally over USB into the head unit's voice command and phone call channels (Siri, phone calls, navigation voice input). Motorcycle navigation prompts and media audio are fed back losslessly into the OpenMotorBridge intercom audio matrix with smooth ducking ($-12\,\text{dB}$) -- completely free of analog ground loops or alternator whine.

#### 5.1.2 Universal Cockpit & Front Hub (PCBA 05): USB Subsystem, Live Traffic & PTT
The Front Node (PCBA 05) serves on **all motorcycle types** as the universal cockpit hub, eliminating vulnerable wiring across the flexed steering head:
* **Native 4-Wire Automotive USB Backbone to Central Box:** The Front Node communicates via the shielded **4-wire Automotive USB 2.0 bus (`VBUS`, `GND`, `D+`, `D-`)** with $< 0.2\,\text{ms}$ deterministic latency to the Central Box (Branch 1 of the 16-Pin periphery harness, 60W USB-PD). Completely immune to RF shadowing from wet rain gear, luggage, or aluminum fairings.
* **Wired Handlebar PTT (Optocoupler at `J3` / GPIO 0, $< 1.8\,\text{ms}$ Latency):** Minimal $30\dots 50\,\text{cm}$ harness at the handlebar -- zero failure-prone signal wires crossing the steering neck!
* **Digital I2S MEMS Ambient Microphone (Sipeed / Zilltek MSM261S4030H0R / Knowles SPH0645):** Edge-DSP ambient wind/road noise computation directly at the windshield (physically impossible under the seat) for automatic helmet volume AGC. Standard Philips I2S with high production availability.
* **Cockpit Multi-Sensor & GNSS Integration (Port `J12`):** u-blox SAM-M10Q multi-constellation GNSS patch antenna, TI TMP117 NIST-traceable temperature sensor ($\pm 0.1^\circ\text{C}$), and TI OPT3001 ambient light sensor mounted in the detachable sensor puck ("basket").
* **Automotive USB 2.0 Subsystem (Microchip USB2514B 4-Port Hub & Power Architecture):**
  * **Upstream Host Port (`J4`):** Connects via the combined power and High-Speed USB cable to the 5-Port Glovebox Hub (`glovebox_power_injection_hub.scad`) and through Port 5 into the Harley-Davidson Boom! Box GTS / Skyline OS for Headset Emulation and CarPlay.
  * **Downstream Port 1 (Handlebar Phone Fast-Charging & GPS):** Dedicated $27\,\text{W}$ USB-PD fast-charging port (Southchip SC8721/SC8102, 9V/3A) for handlebar smartphone (QuadLock / SP Connect) or Garmin Zūmo XT2.
  * **Downstream Port 2 (CP2AA COTS Dongle):** Switched $+5.0\,\text{V}$ VBUS via `TI TPS2051B` power switch with software-controlled **2.5s cold restart** and **Auto-Café 60s timer** upon ignition off. The commercial CarPlay/Android Auto dongle is mounted inside the fairing cavity thermally decoupled via a $25\dots 30\,\text{cm}$ shielded pigtail (3M Dual-Lock).
  * **Downstream Port 3 (Glovebox Passthrough & Media Port):** Transparent feedthrough with Port-Sense (100% free for USB MP3 sticks, firmware updates, and direct phone wired CarPlay).
  * **Downstream Port 4 (Cockpit Accessories / Action Cam):** 10W weather-sealed USB-C lead for action cam (GoPro Hero / Insta360) or external displays (Chigee AIO-5).
  * **USB-C Service Port (`J7`):** Native diagnostic, calibration, and flashing receptacle directly connected to the ESP32-S3 native USB-JTAG/OTG interface.
* **USB-Media Proxy & Source-Aware CAN Gating:**
  * Emulates an MFi-iPod / USB Audio Class device to Skyline OS: Displays track, artist, album, and duration natively on the 12.3" Harley screen, while audio stays in the helmet via LDAC/aptX (no WHIM needed).
  * **Collision Protection:** Checks `infotainment_source_active` (CAN `0x388`) and Hub Port 1 to ensure handlebar media buttons only control the phone when OMB/CarPlay/BT is active (preventing phantom streaming while listening to MP3 sticks or radio).
* **USB CDC-NCM Ethernet Tethering for Internal OEM Navigation:**
  * Presents as a virtual automotive network interface at port `J4`, routing phone data to the bike.
  * **Benefit:** Factory navigation (HERE / TomTom) gets **instant live traffic, congestion flow, and road closure alerts upon ignition ON** without manual phone hotspot setup.
* **Intelligent Standstill Filter & KL15 Buffer Capacitor (`C_BUF`):**
  * Low-ESR buffer capacitors keep the controller alive for $\approx 1\dots 2\,\text{s}$ upon ignition off, cleanly closing all open files.
* **Automotive Power Supply:** Fully supplied via Branch 1 of the OMB periphery bus (60W USB-PD); onboard TI TPS63070 buck-boost provides full ISO 7637-2 cold-cranking compliance.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Real-time Telemetry:** Via the TCAN334G transceiver in listen-only mode, the bridge captures wheel speeds, lean angles, and turn indicators.
* **TFT Display Notifications:** System alerts can be rendered directly on the motorcycle TFT dashboard.

### 5.3 Rear Radar 2.0 & Blind-Spot Assistant (Wheeltec MR20 77 GHz mmWave & Garmin Varia) on Dedicated Standalone Mount
* **Rear Mounting & Leveling (Zero Pod 3):** The rear radar module mounts completely autonomously without requiring an extra satellite enclosure, seated on a minimal dedicated bracket (e.g. [`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl) under the luggage bridge or model-specific plate adapters). Connection is routed via Branch 4 of the 16-Pin Automotive harness (Pins: 12V switched, GND; telemetry streams via shielded high-speed CAN / Serial). A bionic 36-tooth Hirth coupling ensures distortion-free, 100% horizontal leveling.
* **Dual-Radar Architecture (Two Interchangeable Radar Engines):**
  * **Radar 2.0 (Wheeltec MR20 77 GHz mmWave - Standard):**
    - Integrated in an IP67 winged monocoque housing ([`radar_mr20_housing.scad`](../../hardware/cad/scad/05_accessories/radar_mr20_housing.scad)) with PCBA 08 (ESP32-C5 Dual-Band Sub-MCU).
    - 77 GHz FMCW horn-array antenna with $\pm 60^\circ$ ($120^\circ$) horizontal FoV and up to $90\,\text{m}$ detection range.
    - 36-LED Neopixel dual warning wings (18 left, 18 right): Directional blind-spot detection (BSD), brake-light strobe on deceleration $> 0.4\,g$, and dynamically expanding proximity halo on rapid overtaking traffic ($TTC < 2.5\,\text{s}$).
    - Autonomous 5.9 GHz ITS-G5 (V2X) ceramic patch antenna cradle in the left wing for Car-to-X safety broadcasts.
    - Binder Series 707 M5 4-pin IP67 connector (power + macro-UART), mechanically decoupled.
  * **Radar 1.0 (Garmin Varia RTL515 / eRTL615 - Legacy):**
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

#### 5.3.3 TI TMP117 High-Precision Road & Ambient Temperature Safety (Port J12 on Front Node)
* **Mounting Location & Cockpit Integration:**
  * The digital precision temperature sensor **TI TMP117** ($\pm 0.1^\circ\text{C}$ NIST-traceable laboratory accuracy, 16-bit I2C) connects directly via Qwiic port `J12` on the Front Node (PCBA 05).
  * It sits shielded inside the laminar cold air scoop of the front fairing -- thermally isolated from engine heat soak and direct solar irradiation.
* **I2C Protocol & Resolution:**
  * 16-bit resolution ($0.0078^\circ\text{C}$ LSB, sampling rate 1.0 s).
* **Black Ice Guard (Early Warning):**
  * When measured ambient temperature drops to $T \le +3.0^\circ\text{C}$ (hazard of freezing wet patches and black ice on bridges and mountain passes), OMB initiates a two-tier safety warning:
    1. **Acoustic Warning Chime:** A discreet low dual-tone ping ($440\,\text{Hz} \rightarrow 330\,\text{Hz}$) is played once into the rider headset.
    2. **Visual Snowflake Indicator:** The blue ice-crystal warning icon lights up persistently in the PWA Ride HUD and on the mirror LEDs (`J9`) until temperature sustainably rises above $+4.5^\circ\text{C}$ (hysteretic deadband against flicker).

### 5.4 LoRa 868 MHz Bike Alarm Pager & Parking Sentry (OEM BCM + Autonomous IMU)
* **The Limitation of Traditional Bike Alarms:** When parked at a hotel or mountain pass café, the bike's audible horn alarm cannot be heard from $> 50\dots 100\,\text{m}$ away.
* **OpenMotorBridge as Long-Range LoRa Pager:**
  1. **OEM Alarm Integration (e.g. Harley Smart Security / BMW DWA):**
     * OMB monitors the CAN bus in low-power standby (buffered by the onboard 18650 UPS cell).
     * If the factory BCM triggers the vehicle alarm (`bcm_alarm_triggered == 1`), OMB immediately detects the broadcast.
  2. **Autonomous Protection (for bikes without OEM alarm or luggage tamper):**
     * Internal 6-DOF IMU detects attitude changes (lifting off sidestand, impact shocks).
     * Reed switches on pod slide-in lids detect unauthorized pod tampering.
  3. **LoRa 868 MHz Long-Range Alert (Packet Type `0xFE`):**
     * OMB transmits an instant emergency packet with $1\dots 5\,\text{km}$ penetration through concrete hotel walls to the rider's pocket receiver or group bikes:
       > *"🚨 THEFT ALERT: Your motorcycle is being moved! (Distance: 180 m)"*

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
  * Combines the $20 \times 10 \times 5\,\text{mm}$ N52 neodymium magnetic key for contactless pod slide-in lid latch release with a silent LoRa 868 MHz alarm pager inside a compact PA12-MJF enclosure ($58 \times 34 \times 13\,\text{mm}$).
  * An integrated $0{,}5\,\text{mm}$ mu-metal shield isolates internal electronics, LRA actuator, and LiPo cell from magnetic saturation.
* **Rechargeable LiPo & MagSafe Cockpit Docking:**
  * Features a rechargeable 250 mAh 1S LiPo pouch cell, eliminating coin-cell failures in sub-zero winter rides.
  * Recharges inductively whenever magnetically docked on the Cockpit Qi pad or MagSafe frame dock (`009_magsafe_frame_dock.stl`) during rides.
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
* **Architectural Elimination of UWB (Transition to 4-Wire Automotive Bus):**
  * In OpenMotorBridge v10.0, the experimental 6.5 GHz UWB wireless backbone is completely superseded by the ruggedized **4-wire Automotive USB-PD & USB 2.0 backbone (`VBUS`, `GND`, `D+`, `D-`)**.
  * This provides up to 60W USB-PD charging power to all satellite nodes, delivers deterministic $< 0.2\,\text{ms}$ latency, eliminates antenna de-sensing, and enables Zero-Disassembly WebUSB flashing.

### 5.12 Cognitive Cockpit Decluttering & Silent Background Protection
* **Strict Demarcation: When Automation Acts - and When It Stays Silent:**
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
  * **2 Pods on 2 Sun Visors (Driver & Passenger Sides):**
    * Pod 1 (driver side) and Pod 2 (passenger side) snap onto the sun visors using tool-free visor clips ([`car_sun_visor_pod_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod_clip.stl)).
    * **RF Physics Advantage:** Antennas radiate forward and laterally through the glass automotive windshield -- **100% free of metallic chassis attenuation and Faraday shielding**, fully concealed with zero external vehicle antennas.
    * **Versatile Convoy Modes:**
      - **Mode A (Chase vehicle for mixed motorcycle group):** Pod 1 with Sena SPIDER X Slim (Mesh 3.0/2.0), Pod 2 with Cardo Packtalk Edge (DMC Gen 2). Enables simultaneous full-duplex communication into both major motorcycle mesh ecosystems!
      - **Mode B (Pure Car/Camper Convoy):** Pod 1 with OMM 2.4 GHz Module (OpenMotorMesh), Pod 2 with Midland PMR446 Radio for universal public radio.
  * **All-in-One Car Support Core Unit (Zero UWB & Thermal Safety):**
    * **Central Box (`PCBA 01`) and Front Node (`PCBA 05`) Consolidated:** With UWB completely replaced in v10.0 by the 4-wire automotive bus, near-field de-sensing is eliminated. Both boards are mounted together as a compact dual unit ("All-in-One Car Support Core Unit") under the passenger seat or in the center console.
    * **Single 12V Power Cable:** A single automotive 12V connection to the cigarette lighter or fuse tap powers the entire core unit -- eliminating cross-cabin Y-harness clutter.
    * **SAM-M10Q GNSS Puck:** Positioned unobtrusively at windshield corner connected via a slim sensor wire.
  * **Audio Integration & AAWireless / CarPlay Clean Power Injection:**
    * **Option 1 (Vehicle Handsfree via QCC3084):** Central Box pairs via Bluetooth (HFP 1.8 / A2DP) to the car's handsfree system. Convoy radio audio plays over car speakers, driver speaks through the car roof mic.
    * **Option 2 (AAWireless / CarPlay Clean Power Injection & OEM Media Passthrough):** Factory car USB media sockets are often limited to strict legacy USB 2.0 specs ($500\,\text{mA} / 2.5\,\text{W}$) or fluctuate under load. When running Wireless Android Auto / Apple CarPlay (AAWireless, Ottocast, Carlinkit), 5 GHz Wi-Fi transceivers cause peak draws of $1.2\dots 1.8\,\text{A}$, causing endless bootloops and dropouts. **OMB Solution:** The AAWireless adapter plugs directly into OMB's dedicated 5V 3A ($15\,\text{W}$) buck regulator port for rock-solid power. A pure USB 2.0 data cable (`D+`, `D-`, `GND` with isolated/blocked `VBUS`) connects to the car's OEM Media USB socket. The car Head Unit receives high-speed data without supplying current -- completely eliminating bootloops!
    * **Option 3 (Autonomous OMM Handset / Desk Mic):** An autonomous OMM 2.4 GHz module with gooseneck microphone or PTT button rests in the center console for the passenger/guide.
  * **External 868 MHz Magnetic Roof Antenna as Default (15–25 km LoRa Range):**
    * In an automotive steel cabin, the Faraday body attenuates RF signals by $20\dots 30\,\text{dB}$.
    * Reference Kit 5 therefore standardizes on a miniature $\varnothing 30\,\text{mm}$ magnetic roof mount antenna with $2.5\,\text{m}$ thin RG-174 coaxial cable routed through the elastic tailgate weatherstrip seal.
    * The metallic vehicle roof acts as a $360^\circ$ ground plane ($+3\,\text{dBi}$ gain), ensuring $15\dots 25\,\text{km}$ real-world LoRa range to the motorcycle group across valleys and mountain passes.
  * **Concealed Wiring:**
    * Ultra-flat USB-C ribbon cables route invisibly behind A-pillar weatherstrips directly to the two sun visors.
  * **Automotive Telemetry:**
    * Autonomous wireless coupling via Bluetooth 5.0 (BLE) to an OBD2 dongle (vGate / OBDLink) or hardwired 16-pin OBD2 right-angle cable from the 12-pin Vehicle Satellite.
    * Vehicle telemetry (speed, RPM, fuel level %, coolant temperature) broadcasts autonomously into the 868 MHz LoRa mesh -- zero smartphone dependency.
* **Real-Time Fleet Telemetry without Cellular Service (PWA Fleet Dashboard):**
  * An iPad or Android tablet mounted in the car runs the OpenMotorBridge PWA dashboard in offline vector map mode.
  * Over the 868 MHz LoRa mesh, the support crew receives second-by-second telemetry updates (GPS coordinate fixes, road speeds, crash/SOS alerts, tire pressures, ambient road temperature) from all group motorcycles over a radius of up to $15\,\text{km}$ -- autonomous, robust, and completely independent of cellular network coverage.

---

## 13. Documentation Roadmap & Single Source of Truth (SSOT) Architecture

To eliminate redundancy and enforce strict ownership of topics, the OpenMotorBridge documentation is structured modularly. Every technical domain possesses an authoritative **Single Source of Truth (SSOT)**:

| Technical Domain | Authoritative Reference Document | Scope & Core Focus |
| :--- | :--- | :--- |
| **Intercom Profiles & Matrix** | **[Chapter 02](02_intercom_matrix_profiles.md)** | Sena Mesh 2.0/3.0, Cardo DMC Gen1/2, Midland PMR, Audio Routing & Levels |
| **Acoustics, DSP & Ducking** | **[Chapter 03](03_audio_dsp_acoustics.md)** | Raised-Cosine Filters, Ducking (-12 dB / -18 dB), Wind-AGC, Latency Budgets |
| **Mesh, LoRa & Navigation** | **[Chapter 04](04_mesh_lora_navigation.md)** | SX1262 LoRa Mesh, Dynamic Routing, Emergency SOS, Cluster Merging |
| **OMM Intercom Modules (2.4G & 446M)** | **[Chapter 04b](04b_omm_intercom_module.md)** | PCBA 09 (2.4 GHz HD-Mesh) & PCBA 10 (446 MHz PMR/DMR), ECE 22.06 UCS |
| **Power Management & UPS** | **[Chapter 05](05_power_management_ups.md)** | LM5164 Step-Down, BQ24075 UPS, Dual-Battery Cold Boot, JEITA Thermal |
| **Telemetry & Blackbox** | **[Chapter 06](06_telemetry_blackbox_webdav.md)** | MicroSD-FAT32 Ring Buffer, 15-State EKF Lean Angle, WebDAV / Cloud Sync |
| **PCBA Hardware & Pinouts (SSOT)**| **[Chapter 07](07_pcba_hardware_pinouts.md)** | **All Boards (PCBA 01 through 10)**, Complete Pinouts, Component Specs |
| **Enclosures, Mechanics & CAD (SSOT)**| **[Chapter 08](08_enclosures_mechanics_cad.md)** | **All CAD Models**, OpenSCAD Parameters, ECE Standards, Captive Hex Nuts |
| **Firmware Architecture** | **[Chapter 09](09_firmware_architecture.md)** | FreeRTOS Task Matrix, 4-Wire USB-PD & USB 2.0 Protocol, 5-Gesture Engine |
| **WebApp PWA Dashboard** | **[Chapter 10](10_webapp_pwa_dashboard.md)** | Ride HUD, WebBLE Protocol, Pod & Profile Config, Offline OSM Vector Maps |
| **CarPlay / Android Auto Bridge** | **[Chapter 11](11_carplay_android_auto_bridge_architecture.md)**| Virtual WHIM, CP2AA Bridge, Multi-Path Wi-Fi/Cellular, Headless Dongle |
| **CAN Bus Vehicle Profiles** | **[Chapter 12](12_can_bus_vehicle_profiles.md)** | BMW, KTM, Ducati, Harley CAN Matrices, LIN/K-Line Interfaces |
| **Simulation & Testbench (HIL/SIL)**| **[Chapter 13](13_simulation_testbench.md)** | Python Netlist Validator, FreeRTOS Timing Verification, Signal Integrity |
| **EMC & RF Hardening** | **[Chapter 14](14_emv_rf_hardening.md)** | CISPR 25 Class 5, 8-Band RF Matrix, ESD Protection, Coexistence |
| **BOM, Procurement & Manufacturing**| **[Chapter 15](15_bom_manufacturing.md)** | **Complete Bill of Materials**, JLCPCB SMT Data, COTS Docks, Harnesses |
| **Assembly Instructions** | **[Chapter 16](16_build_instructions_assembly.md)** | Step-by-Step Build Guide, Harness Fabrication, Torques, Commissioning |
| **Standards & References** | **[Chapter 17](17_standards_references.md)** | ECE 22.06, DIN/ISO Standards, IEEE 802.11, Bluetooth SIG, USB-IF Specs |
| **Legal Compliance & Privacy** | **[Chapter 18](18_legal_compliance_dsgvo.md)** | RED 2014/53/EU, FCC Part 15, CE Marking, GDPR Telemetry Compliance |

