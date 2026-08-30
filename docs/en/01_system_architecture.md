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

Satellite Pods 1 and 2 are mechanically **100% identical** and support two equally robust deployment strategies:

```
              OPTION A: HELMET DIRECT MOUNT               OPTION B: VEHICLE FRAME MOUNT
         ┌─────────────────────────────────────┐      ┌─────────────────────────────────────┐
         │ • Pod 1 directly on Rider Helmet    │      │ • Pod 1 left on tank/frame          │
         │ • Pod 2 directly on Pillion Helmet  │      │ • Pod 2 right on rear/crash bar     │
         │ • Pogo array docks headset on helmet│      │ • Headsets stay mounted on bike     │
         │ • 1 slim M8 spiral cord to bike     │      │ • Helmet audio via BT or aux cable  │
         └─────────────────────────────────────┘      └─────────────────────────────────────┘
```

### Option A: Direct Helmet Docking (Recommended for Maximum Ergonomics)
* **Mounting:** The Pod mounts directly to the helmet shell using the 3D printed clamp bracket ([pod_mount_helmet_clamp.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/pod_mount_helmet_clamp.scad)) or 3M VHB adhesive pad.
* **Advantage:** The OEM headset (e.g., Sena 50S or Cardo Packtalk Edge) stays in its natural helmet position. Its gold-plated docking contacts are engaged directly by the cartridge's Pogo-pin array.
* **Connection:** A single flexible, shielded M8 6-pin spiral cable connects the helmet to the motorcycle harness.

### Option B: Vehicle Frame Docking (Zero-Cable Helmet Setup)
* **Mounting:** Pod 1 mounts on the left bike frame / side panel, and Pod 2 mounts on the right frame.
* **Advantage:** Intercom units stay permanently locked on the motorcycle.
* **Helmet Link:** The rider's helmet connects wirelessly via standard Bluetooth to the bridge, while high-power mesh communication is handled by the bike-mounted pods.

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
* **WHIM Emulation & Apple CarPlay / Android Auto:**
  OpenMotorBridge emulates active OEM headset impedance networks. This unlocks Apple CarPlay and Android Auto on the Boom! Box display **without purchasing the proprietary HD WHIM module ($> \$350$)**.
* **Seamless Audio Ducking:** Boom! Box navigation announcements are prioritized and smoothly blended over active intercom conversations with adjustable ducking ($-12\,\text{dB}$).

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Real-time Telemetry:** Via the TCAN334G transceiver in listen-only mode, the bridge captures wheel speeds, lean angles, and turn indicators.
* **TFT Display Notifications:** If the wireless remote battery drops below $2.3\,\text{V}$, an alert is broadcast to the TFT display (*"Handlebar remote battery low - replace CR2032"*).
