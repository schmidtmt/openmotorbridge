# 01 - System Architecture, Universal Satellite Topology & Acoustics

This document specifies the overall system architecture of **OpenMotorBridge v8.0**, the universal 4-point satellite topology, flexible mounting paradigms (helmet vs. vehicle frame docking), RF coexistence, and seamless integration into modern OEM motorcycle infotainment systems.

---

## 1. Problem Statement & Architectural Philosophy

Classic motorcycle communication systems are historically fragmented:
* **Incompatible Mesh Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh, and analog PMR446 radio cannot communicate directly.
* **RF Overload & De-Sensing:** Operating multiple 2.4 GHz mesh transceivers in close proximity (e.g., on the same helmet or in a single enclosure) results in severe receiver desensitization (*De-Sensing*), intermodulation, and range drops of up to $80\,\%$.
* **Proprietary Infotainment Lock-in:** Systems like Harley-Davidson Boom! Box GTS / Skyline OS or BMW ConnectedRide require expensive OEM modules (such as the HD WHIM) to unlock Apple CarPlay or Android Auto.

**OpenMotorBridge v8.0** resolves these bottlenecks via a modular, decoupled **4-Point Satellite Topology** with galvanically isolated DSP audio routing:

```
                                     SYSTEM TOPOLOGY OVERVIEW
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT / HANDLEBAR (100% Wireless):                                                     │
│    • BLE 5.0 Wireless Remote (CR2032 with Battery Service 0x180F & PTT trigger)             │
│    • PWA Dashboard on Smartphone / TFT display via Web Bluetooth (WebBLE)                   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTRAL CONTROL BOX (Under-Seat, IP67 Sealed):                                           │
│    • ESP32-S3 Dual-Core MCU (240 MHz) • ES8388 Audio Codec & DSP Audio Mixer               │
│    • LM5164-Q1 72V Automotive Step-Down • BQ24075 UPS & 1000mAh LiPo Backup Battery         │
│    • 4-Bit High-Speed SDIO MicroSD Ringbuffer • 2x Bourns 1500 V RMS Audio Isolation Xfmrs  │
└─┬─────────────────────────────────────────────────────────────────────────────────────────┬─┘
  │                                                                                         │
  ▼ Central HD26 Flanged Connector (250 mm Y-Breakout Harness Pigtails)                     │
┌──────────────────────────────┬──────────────────────────────┬─────────────────────────────┤
│ 3. SATELLITE POD 1 (M8 6P):  │ 4. SATELLITE POD 2 (M8 6P):  │ 5. REAR POD 3 (M8 6P):      │
│ • Universal Pod Enclosure    │ • Universal Pod Enclosure    │ • Universal Pod Enclosure   │
│ • Intercom Bridge A (Sena    │ • Intercom Bridge B (Cardo   │ • 1-Tier Monolithic Sled    │
│   50S/60S/MeshPort Sled)     │   Packtalk Edge / PMR446)    │ • u-blox MAX-M10S Multi-GNSS│
│ • Saddlebag, Frame, Rear or  │ • Saddlebag, Frame, Rear or  │ • SX1262 LoRa 868MHz + RP2040│
│   Helmet Mounting            │   Helmet Mounting            │ • 2.4 GHz OMM-Mesh (ESP32-C3)│
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. VEHICLE POWER: AMP Superseal 1.5 4-Pin (KL30 Batt+, KL15 Ign+, Chassis Ground)       │
  ├─► 7. REAR SENSOR BRANCH: M8 4-Pin (Rear Radar / Blind-Spot Sensor / Local OBD2-CAN)─────┤
  │                                                                                         │
  ▼ 2.4 GHz Ultra-Low-Latency Wireless Link (ESP-NOW < 3ms & BLE 5.0 2M-PHY)                │
┌───────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. COCKPIT SUBSYSTEM: Wireless Universal Front Node (PCBA 05 Cockpit & Cam Bridge)       │
│ • Automotive 2-Port USB 2.0 Hub (Microchip USB2512B) for Boom! Box & CarPlay Adapter       │
│ • Switched CarPlay Port via TI TPS2051B (Controlled 2.5s Cold Reboot & 60s Auto-Café)      │
│ • Digital I2S MEMS Ambient Mic with ePTFE Acoustic Vent (Edge RMS Noise Level Tracking)   │
│ • Hardwired Handlebar PTT Pushbutton Input (Direct GPIO Interrupt, 100% Battery-Free!)    │
│ • Integrated Cockpit CAN-Bus Transceiver (TCAN334G with 120 Ohm) for Fairing TFT Displays │
│ • Only Single Vehicle Wire Needed: Rugged 2-Core 12V Power Cable (KL15 / GND)              │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Modular System Philosophy & Mounting Freedom (The 5 Functional Nodes)

OpenMotorBridge v8.0 defines the platform across **5 standardized functional nodes**:
1. **Central Box (Main ECU):** Central computational core (ESP32-S3), 24-bit audio DSP/codec (ES8388), galvanic isolation transformers, 72V automotive step-down (LM5164-Q1), and LiPo UPS (BQ24075). *(Typically mounted centrally under the seat in the battery compartment).*
2. **Rear Pod 3 (Backbone & Telemetry):** Multi-GNSS (u-blox MAX-M10S), 868 MHz LoRa (Semtech SX1262), 2.4 GHz OMM Mesh co-processor (ESP32-C3), and 6-axis IMU (BMI270). *(Typically mounted at the rear with an unobstructed view of the zenith).*
3. **Satellite Pod 1 (Intercom Bridge A):** Universal cartridge bay for Sena (Mesh 2.0/3.0 / Bluetooth). *(Typically on the left vehicle side).*
4. **Satellite Pod 2 (Intercom Bridge B):** Universal cartridge bay for Cardo (DMC Gen1/Gen2 / Bluetooth) or analog PMR446 radio. *(Typically on the right vehicle side for RF spatial diversity).*
5. **Front Node (Cockpit & Camera Hub):** Autonomous ESP32-C3 satellite, automotive USB 2.0 hub (USB2512B) for Apple CarPlay/Ottocast, switched 5V action cam charge port with BLE shutter, digital PTT button input, and Knowles MEMS ambient noise microphone. *(Typically hidden behind fairings or inside the headlight nacelle).*

```
                     THE 5 STANDARDIZED FUNCTIONAL NODES
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. FRONT NODE (Cockpit/Nacelle):  Wireless USB, Action Cam, PTT & Audio Hub │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. CENTRAL BOX (Under Seat/Batt): DSP Audio Matrix, Power Supply, UPS, CAN  │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│ 3. POD 1 (Left/Saddlebag):   │ 4. POD 2 (Right/Saddlebag):  │ 5. REAR POD 3:│
│ • Intercom Bridge A (Sena)   │ • Intercom Bridge B (Cardo)  │ • GNSS / LoRa │
│ • 100% Quick-Swap Cartridge  │ • 100% Quick-Swap Cartridge  │ • OMM 2.4 GHz │
└──────────────────────────────┴──────────────────────────────┴───────────────┘
```

> [!NOTE]
> **Mounting Freedom – *Your Bike, Your Choice*:**  
> Where and how you place these 5 enclosures on your motorcycle is deliberately **entirely up to you**! OpenMotorBridge provides the standardized electronic layouts, enclosure dimensions, and interfaces.  
> For popular motorcycle categories, we deliver turnkey, 100% zero-drill and adhesive-free **Reference Mounting Kits** in **[Chapter 08 (Mechanics & CAD)](file:///Users/schmidtm/openMotorBridge/docs/en/08_enclosures_mechanics_cad.md)**:
> * **Reference Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring):** Pod 3 inside the Under-Cowl Skeleton Dock under the forged carbon cowl, Pods 1 & 2 protected inside the saddlebag lids (zero-drill Torx hinge screws, quick disconnect), Front Node on fairing bracket behind outer sharknose skin.
> * **Reference Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 3 in the Touring Fender Console on the rear fender, Pods 1 & 2 in the saddlebag lids, Front Node hidden inside the 7" headlight nacelle.
> * **Reference Kit 3 (Classic Bagger & Cruiser – Street Glide / Electra Glide):** Pod 3 in the Touring Stealth Console seamless to passenger seat, decoupled radar below the license plate, Pods 1 & 2 in the saddlebag lids.
> * **Reference Kit 4 (Adventure & Touring Enduros – BMW GS, KTM Adventure, Africa Twin):** Pod 3 directly on luggage rack / tubular subframe with integrated M5 GoPro radar arm, Pods 1 & 2 on crash bars via 120° V-grooves and EPDM tension straps, Front Node on nav crossbar or inside beak.
>
> Riders are encouraged to replicate these kits, adapt them for other motorcycle models, or design custom brackets based on our open CAD/STEP dimensional envelopes!

### 2.1 Vehicle Mounting (Crash Bars, Frame Tubes, Luggage Racks)
* **Universal Prism (V-Groove):** The bottom of each pod housing features a $120^\circ$ prism contour ($R = 15\,\text{mm}$) that cradles all standard motorcycle frame tubes:
  * $\varnothing 22\,\text{mm}$ ($7/8"$ handlebars and rear subframe tubes)
  * $\varnothing 25.4\,\text{mm}$ ($1"$ crash bars and cruiser frame tubes)
  * $\varnothing 28.6\,\text{mm}$ ($1\,1/8"$ tapered handlebars and enduro frames)
  * $\varnothing 32\,\text{mm}$ ($1\,1/4"$ heavy-duty crash bars)
  * **Flat Surfaces:** Sits rock-solid on flat panels (under-seat battery tray / side covers).
* **EPDM Tension Ring Retention:** Two UV-resistant EPDM rubber rings (or silicone ladder straps) wrap around the tube and hook into the 4 lateral side lugs. This simultaneously isolates high-frequency engine vibrations.
* **Theft-Resistant Fixed Mounting:** Integrated $5.0 \times 2.5\,\text{mm}$ passthrough slots allow threading standard $4.8\,\text{mm}$ zip-ties or stainless hose clamps.

### 2.2 Wireless Helmet Audio
* Heavy intercom hardware (Sena 50S / Cardo Edge) stays safely locked and weather-protected on the motorcycle.
* Helmets remain $100\%$ lightweight, aerodynamically stock, and completely cable-free. Audio I/O connects wirelessly via the Central Box's integrated Bluetooth interface.

### 2.3 Universal Off-the-Shelf OEM Adapter Interfacing
The enlarged pod cartridges ($110 \times 54 \times 28\,\text{mm}$ interior cavity) accommodate all commercial off-the-shelf OEM adapters in their factory-unopened state:
* **Class A (Wireless Bridges & USB Power):** e.g. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red – powered via low-profile 90° Micro-USB/USB-C, wireless BT audio bridge to helmet, external SMA bulkhead double-jack with silicone protection plug on faceplate.
* **Class B (Pogo-Pin Spring-Contact Cradles):** e.g. Sena 50S/60S/30K/20S EVO – full analog audio (ES8388 codec) and TLP222A PTT synthesis.
* **Class C (Magnetic Air-Mount):** e.g. Cardo Packtalk Edge/Pro/Neo – tool-free magnetic latching via dual N52 Neodymium magnets.
* **Class D (Slide Cradles):** e.g. Cardo Packtalk Bold/Black, Freecom series – mechanical slide rail with catch spring.
* **Class E (Analogue PMR446 Radios):** e.g. Midland G7/G9 Pro, XT30, Kenwood – 2-pin dual audio jack with PhotoMOS PTT keying.
*(Detailed wiring matrix and pinouts available in [Specification 06, Section 8](file:///Users/schmidtm/openMotorBridge/docs/en/06_dynamic_profiles_spec.md#8-taxonomy-of-oem-adapter-interfacing-connection-classes--wiring-matrix)).*

---

## 3. RF Coexistence & Spatial Diversity ($> 35\,\text{dB}$ Isolation)

When operating Sena and Cardo mesh units simultaneously, receiver blocking must be reliably prevented:

1. **Physical Separation ($d \ge 45\,\text{cm}$):**
   * Helmet setup: Rider helmet (front/high) and pillion helmet (rear/high) maintain $50\dots 80\,\text{cm}$ separation.
   * Frame setup: Pod 1 (left side) and Pod 2 (right side) utilize the motorcycle's steel/aluminum chassis, engine block, and fuel tank as an RF barrier.
2. **Shielding Attenuation:**
   * Free-space loss over $50\,\text{cm}$ combined with chassis metal shielding achieves an **RF isolation of $> 35\,\text{dB}$**.
   * Coupling levels at adjacent receivers remain below $-15\,\text{dBm}$, keeping low-noise amplifiers (LNAs) in their linear region and preventing *De-Sensing*.
3. **Tri-RF Architecture in Rear Pod 3:**
   * Rear Pod 3 integrates 2.4 GHz Mesh, 868 MHz LoRa, and GNSS. The $25 \times 25\,\text{mm}$ patch ground plane and $15 \times 8\,\text{mm}$ antenna keepout restrict mutual RF degradation to $< 0.2\,\text{dB}$.

---

## 4. Physical Interfaces & Signal Matrix

All system signals converge at the central HD26 flanged connector:

| Branch / Cable | Connector Type | Target Device | Transferred Signals |
| :--- | :--- | :--- | :--- |
| **Pigtail 1 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 1** (Intercom Bridge A: Sena Mesh / Universal) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Pigtail 2 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 2** (Intercom Bridge B: Cardo DMC / PMR446) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Pigtail 3 (250 mm)** | M8 6-Pin A-Coded (Female) | **Rear Pod 3** (OMM & GNSS) | UART_TX, UART_RX, 1-PPS_SYNC, 1-WIRE_ID, +5V_POD3, GND |
| **Pigtail 4 (250 mm)** | AMP Superseal 1.5 4-Pin | **12V Vehicle Power** | KL30 (Batt+), KL15 (Ign+), GND (Power), GND (Sense) |
| **Pigtail 5 (250 mm)** | M8 4-Pin A-Coded (Female) | **Rear Radar & Local OBD2** | RADAR_PWR_12V, RADAR_GND, RADAR_RX (UART/CAN_H), RADAR_TX (UART/CAN_L) |

---

## 5. Integration into OEM Infotainment Systems

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 WHIM Emulation & Apple CarPlay / Android Auto Unlocking
* **Background:** Apple CarPlay strictly mandates an active speech microphone. Harley-Davidson locks CarPlay in factory Boom! Box GTS firmware unless either a wired 7-pin DIN headset or the proprietary **HD-WHIM** (*Wireless Headset Interface Module*, $> \$350$) is installed.
* **Impedance Emulation:** OpenMotorBridge replicates the DC bias and AC impedance ($1.0 \dots 2.2\,\text{k}\Omega$) of an active OEM electret microphone via its isolated Bourns transformer frontend.
* **Result:** The Boom! Box GTS unlocks Apple CarPlay and Android Auto on the 6.5" or 12.3" touchscreen immediately — **without requiring the \$350 WHIM module** or unreliable jumper bypass plugs.
* **Seamless Audio Ducking:** Boom! Box navigation announcements are prioritized and smoothly blended over active intercom conversations with adjustable ducking ($-12\,\text{dB}$).

#### 5.1.2 Wireless Universal Front Node, Automotive USB Hub & Action Cam Subsystem (PCBA 05)
To eliminate fragile signal wiring harnesses through the flexed steering head and provide uninterrupted infotainment, action cam, and PTT connectivity in the cockpit:
* **Wireless RF Bridge to Central Box:** An autonomous controller node (ESP32-C3 RISC-V) inside the fairing communicates via **ESP-NOW ($< 0.9\,\text{ms}$ latency)** and **BLE 5.0 (2M-PHY)** directly to the Central Box.
* **Automotive USB 2.0 High-Speed Subsystem (Microchip USB2512B & TI TPS2051B):**
  * **Upstream Host Port (`J4`):** Connects directly to the USB input of the Harley-Davidson Boom! Box GTS / Skyline OS in the glovebox.
  * **Downstream Port 1 (`J5` / Phone & Glovebox):** Uninterrupted $+5.0\,\text{V}$ VBUS (up to $2.0\,\text{A}$) for clean smartphone charging or navigation devices.
  * **Downstream Port 2 (`J6` / Ottocast CarPlay):** Switched $+5.0\,\text{V}$ VBUS via `TI TPS2051B` power gate with software-controlled **2.5s cold restart** and **Auto-Café 60s timer** upon ignition off.
  * **USB-C Service Port (`J7`):** Native diagnostic, calibration, and flashing receptacle (relocated to the right-side edge next to `D1`) for the ESP32-C3 controller.
* **Dedicated 5V Action Cam Power Header (`J8` / Charge-Only):**
  * Provides **clean $+5.0\,\text{V}$ DC charging power (up to $2.0\,\text{A}$)** for action cameras (GoPro, Insta360, DJI) – purposely **without data lines**, preventing the Boom! Box infotainment system from erroneously locking the camera into USB mass storage transfer mode.
* **Integrated Action Cam BLE Shutter Bridge (GoPro, Insta360, DJI Action):**
  * The ESP32-C3 controls cockpit action and 360° cameras directly via Bluetooth Low Energy (Open GoPro API, Insta360 Smart Remote GATT, DJI Remote profile) — completely eliminating the need for bulky separate handlebar remotes!
  * **Handlebar Pushbutton Gesture Control (on `J3` / GPIO 0):**
    * *Single short press ($< 400\,\text{ms}$):* Intercom / Radio PTT.
    * *Double-click (2x short):* **Action Cam Start / Stop Recording Toggle** (with acoustic confirmation chime in helmet).
    * *Long press ($> 1.5\,\text{s}$):* **HiLight Tag / Bookmark** in the active video track.
  * **Insta360 Telemetry Injection:** Streams live GNSS telemetry (speed, lean angle, elevation) via BLE directly into the Insta360 video stream.
* **Intelligent Standstill Filter & KL15 Buffer Capacitor (`C_BUF`):**
  * A compact buffer capacitor ($470\dots 1000\,\mu\text{F}$ 10V polymer SMD) in the top-right PCB corner keeps the ESP32-C3 powered for $\approx 1\dots 2\,\text{seconds}$ when switched ignition (KL15) turns off.
  * The controller instantly senses the falling edge on `KL15_SENSE` and fires the BLE *"Stop Recording"* packet to the camera within $30\,\text{ms}$.
  * **Advantage:** Fuel stops, red lights, and pauses are automatically cut from video footage; the camera finalizes its MP4 container and enters sleep mode. Upon turning ignition back on, recording resumes seamlessly.
* **Digital I2S MEMS Ambient Microphone (Knowles SPH0645LM4H-6):** Edge-DSP ambient road/engine noise computation for automatic helmet volume AGC.
* **Minimal Bike Wiring:** Single **2-core 12V automotive power lead (`J1`)** tapped at switched KL15 ignition; on-board TI TPS54302 buck converter produces the $+5\,\text{V}$ rail.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Real-time Telemetry:** Via the TCAN334G transceiver in listen-only mode, the bridge captures wheel speeds, lean angles, and turn indicators.
* **TFT Display Notifications:** System alerts can be rendered directly on the motorcycle TFT dashboard.

### 5.3 Rear Radar & Blind-Spot Assistant (Garmin Varia / 24 GHz mmWave) on Pod 3 Dual-Mount Bracket
* **Pod 3 Dual-Mount Bracket & Alignment:** The rear mounting bracket securely holds the universal Pod 3 housing while integrating an angle-adjustable GoPro-compatible M5 arm for horizontal radar leveling ($\pm 5^\circ$).
* **Direct Connection to Pigtail 5:** Provides switched 12V power and bidirectional telemetry (UART2 on `RESERVE_GPIO_A/B` or CAN-Bus) through the waterproof M8 4-pin interface.
* **Supported Radar Hardware:**
  * **Garmin Varia Radar:** RTL515 / eRTL615 serial streaming protocol (0xAA preamble, $140\,\text{m}$ range, $20\,\text{Hz}$ update rate).
  * **24 GHz mmWave Doppler Radars:** Automotive compact modules (e.g. BGT24LTR11 / HLK-LD2410 / DFROBOT).
* **Dynamic Threat Estimation & Time-To-Collision (TTC):**
  * $\text{TTC} = \frac{d}{v_{\text{rel}}}$.
  * **Clear (Green):** No vehicle in danger zone or $v_{\text{rel}} \le 10\,\text{km/h}$.
  * **Amber (Approaching):** $d \le 80\,\text{m}$ and $v_{\text{rel}} > 15\,\text{km/h}$ (standard vehicle closing in).
  * **Red (Collision Hazard):** $\text{TTC} < 3.5\,\text{s}$ or ($d \le 35\,\text{m}$ and $v_{\text{rel}} > 25\,\text{km/h}$).
* **Acoustic Helmet Warnings (Priority-1 Ducking):** On amber/red hazard alerts, the audio DSP immediately ducks music/intercom to **$-18\,\text{dB}$** ($< 15\,\text{ms}$ attack) and injects a crisp **synthesized dual-tone chime** ($880\,\text{Hz} \rightarrow 1760\,\text{Hz}$ on Amber, $988\,\text{Hz} \rightarrow 1976\,\text{Hz}$ on Red) directly into the rider's helmet.
* **Blind-Spot Detection (BSD) & Mirror LEDs:** When an approaching vehicle enters the close-range blind-spot zone ($d < 15\,\text{m}$, $|\text{azimuth}| > 3^\circ$), virtual left/right mirror indicator pills flash in amber or red on the WebApp HUD.
