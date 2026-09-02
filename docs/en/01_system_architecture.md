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
│ • Helmet or Frame Mounted    │ • Helmet or Frame Mounted    │ • SX1262 LoRa 868MHz + C3   │
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. VEHICLE POWER: AMP Superseal 1.5 4-Pin (KL30 Batt+, KL15 Ign+, Chassis Ground)       │
  └─► 7. FRONT BRANCH: M8 4-Pin Receptacle (Vehicle CAN-Bus & IP67 Front Ambient Mic)────────┘
```

---

## 2. Universal Mounting Concepts (Helmet- vs. Frame-Docking)

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
| **Pigtail 5 (250 mm)** | M8 4-Pin A-Coded (Female) | **CAN-Bus & Front Mic** | CAN_H, CAN_L, MIC_AMBIENT_IN, +3V3_MIC_BIAS |

---

## 5. Integration into OEM Infotainment Systems

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 WHIM Emulation & Apple CarPlay / Android Auto Unlocking
* **Background:** Apple CarPlay strictly mandates an active speech microphone. Harley-Davidson locks CarPlay in factory Boom! Box GTS firmware unless either a wired 7-pin DIN headset or the proprietary **HD-WHIM** (*Wireless Headset Interface Module*, $> \$350$) is installed.
* **Impedance Emulation:** OpenMotorBridge replicates the DC bias and AC impedance ($1.0 \dots 2.2\,\text{k}\Omega$) of an active OEM electret microphone via its isolated Bourns transformer frontend.
* **Result:** The Boom! Box GTS unlocks Apple CarPlay and Android Auto on the 6.5" or 12.3" touchscreen immediately — **without requiring the \$350 WHIM module** or unreliable jumper bypass plugs.
* **Seamless Audio Ducking:** Boom! Box navigation announcements are prioritized and smoothly blended over active intercom conversations with adjustable ducking ($-12\,\text{dB}$).

#### 5.1.2 Discrete Fairing 2-Port USB Hub & Ottocast Wireless Adapter
To eliminate the need to pull out and plug in a smartphone in the cramped, sun-heated glovebox every ride:
* **Fairing Topology (Batwing / Sharknose):** Behind the speedometer cluster, a compact automotive-grade 2-port USB 2.0 data hub is looped into the factory head unit USB lead:
  * **Port 1 (Glovebox):** Continues to the factory Jukebox glovebox for flash drives with music, wired charging, or official Boom! Box firmware updates.
  * **Port 2 (Internal Fairing):** Secured invisibly with 3M Dual-Lock inside the fairing, powering a wireless CarPlay/Android Auto adapter (e.g. *Ottocast U2-Air / Mini* or *CarlinKit 5.0*).
* **The Glovebox $V_{\text{BUS}}$ Cutoff Switch:**
  * A discrete, IP65 rocker switch in the glovebox breaks the $+5\,\text{V}$ power wire ($V_{\text{BUS}}$) feeding Port 2 (Ottocast).
  * **Three Essential Functions:**
    1. **Collision Avoidance:** If a phone or USB flash drive is connected in the glovebox for system updates, flipping the switch disconnects the Ottocast, avoiding USB host address conflicts.
    2. **Wi-Fi Release when Parked:** When the motorcycle is parked near a café, hotel room, or carport within Bluetooth range, switching off the Ottocast prevents the bike from continuously hijacking the phone's Wi-Fi and mobile data connection.
    3. **Instant Hard Reboot:** Enables a rapid cold power cycle of the wireless adapter without taking off the fairing or disconnecting the main motorcycle battery.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Real-time Telemetry:** Via the TCAN334G transceiver in listen-only mode, the bridge captures wheel speeds, lean angles, and turn indicators.
* **TFT Display Notifications:** If the wireless remote battery drops below $2.3\,\text{V}$, an alert is broadcast to the TFT display (*"Handlebar remote battery low - replace CR2032"*).
