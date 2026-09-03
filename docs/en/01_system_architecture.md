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
│ • Cartridge Sled for Sena    │ • Cartridge Sled for Cardo   │ • 1-Tier Monolithic Sled    │
│   50S/60S/MeshPort           │   Packtalk Edge / PMR446     │ • u-blox MAX-M10S Multi-GNSS│
│ • Helmet or Frame Mounted    │ • Helmet or Frame Mounted    │ • SX1262 LoRa 868MHz + RP2040│
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. VEHICLE POWER: AMP Superseal 1.5 4-Pin (KL30 Batt+, KL15 Ign+, Chassis Ground)       │
  ├─► 7. REAR SENSOR BRANCH: M8 4-Pin (Rear Radar / Blind-Spot Sensor / Local OBD2-CAN)─────┤
  │                                                                                         │
  ▼ 2.4 GHz Ultra-Low-Latency Wireless Link (ESP-NOW < 3ms & BLE 5.0 2M-PHY)                │
┌───────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. COCKPIT SUBSYSTEM: Wireless Universal Front Node (Smart Fairing Controller)             │
│ • Automotive 2-Port USB 2.0 Hub (Microchip USB2512B) for Boom! Box & CarPlay Adapter       │
│ • Switched CarPlay Port via TI TPS2051B (Controlled 2.5s Cold Reboot & 60s Auto-Café)      │
│ • Digital I2S MEMS Ambient Mic with ePTFE Acoustic Vent (Edge RMS Noise Level Tracking)   │
│ • Hardwired Handlebar PTT Pushbutton Input (Direct GPIO Interrupt, 100% Battery-Free!)    │
│ • Integrated Cockpit CAN-Bus Transceiver (TCAN334G with 120 Ohm) for Fairing TFT Displays │
│ • Only Single Vehicle Wire Needed: Rugged 2-Core 12V Power Cable (KL15 / GND)              │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Universal Mounting Concept (Vehicle Frame, Crash Bar & Tube Saddle Mount)

Satellite Pods 1, 2, and 3 are mechanically **100% identical** and designed for toolless quick-mounting to all standard motorcycle tube diameters and flat surfaces:

```
          UNIVERSAL FRAME & TUBE SADDLE MOUNT (100% WIRELESS HELMET COMFORT)
          ┌─────────────────────────────────────────────────────────────┐
          │ • Integrated V-groove / tube saddle on pod bottom           │
          │ • Fits tube diameters from Ø 18 mm to Ø 35 mm (1" / 1 1/8") │
          │ • 4x hook lugs for 2x weatherproof EPDM rubber tension rings│
          │ • 100% toolless mounting in 5 seconds without paint damage  │
          │ • Pod 1 left on frame / crash bar (Rider Mesh)              │
          │ • Pod 2 right on frame / crash bar (Pillion Mesh)           │
          │ • Pod 3 on rear frame / luggage rack (OMM Dual-PHY & GNSS)  │
          └──────────────────────────────┬──────────────────────────────┘
                                         │
                                         ▼ Bluetooth A2DP / HFP / LE Audio
          ┌─────────────────────────────────────────────────────────────┐
          │ RIDER & PILLION HELMETS (100% Wireless & Lightweight):      │
          │ • Zero bulky extra housing on helmet (0g extra weight)      │
          │ • No flapping cables or dangling coiled wires               │
          │ • Rider wears regular OEM headset / integrated speakers     │
          │ • Central Box streams mixed audio wirelessly to both helmets│
          └─────────────────────────────────────────────────────────────┘
```

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
| **Pigtail 1 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 1** (Rider) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Pigtail 2 (250 mm)** | M8 6-Pin A-Coded (Female) | **Satellite Pod 2** (Pillion) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
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
