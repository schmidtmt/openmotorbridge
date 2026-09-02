# 20. Smart Fairing Controller & Wireless USB Hub Architecture

## 1. System Overview & Motivation

On modern motorcycles—especially touring platforms with batwing or sharknose fairings (e.g. Harley-Davidson Touring, BMW RT/K1600, Honda Gold Wing/Africa Twin, or adventure enduros)—the cockpit area serves as the central focal point for infotainment, navigation, action cams, and auxiliary charging.

Traditional wiring topologies suffered from severe real-world drawbacks:
1. **Mechanical Cable Stress Across Steering Head:** Running high-speed CAN-bus pairs and analog microphone cables through the triple tree to the rear under-seat box causes continuous flexing, sheath wear, and eventual fatigue failures.
2. **Analog Noise Ingress:** Pulling an analog microphone line 1.5 meters across the motorcycle frame picks up ignition coil EMF, alternator whine, and LED ballast switching noise.
3. **Unreliable Remote Batteries:** Handlebar-mounted wireless PTT buttons relying on coin cells (CR2032) consistently fail in cold winter temperatures.
4. **Wireless CarPlay Annoyance & Fairing Damage:** Commercial wireless CarPlay dongles (*Ottocast / CarlinKit*) stay powered on when parking near home or a café, hijacking the phone's Wi-Fi and blocking cellular data. The previous stopgap solution—drilling a hole in the glovebox for a mechanical toggle switch—permanently mars the motorcycle's original condition.

The **OpenMotorBridge Smart Fairing Controller (`openmotorbridge_smart_fairing`)** completely resolves these pain points with a unified front-end module integrating an **automotive USB 2.0 hub IC, software-controlled Ottocast power switching, on-board digital I2S MEMS ambient microphone, battery-free wired handlebar PTT, and ultra-low-latency wireless bridge (ESP-NOW)** to the Central Box.

---

## 2. Block Diagram & Topology

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                 OPENMOTORBRIDGE SMART FAIRING CONTROLLER & USB HUB (PCBA 05)                │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  [ Harley Boom! Box USB-Host ]                                                              │
│                │                                                                            │
│                ▼                                                                            │
│   ┌───────────────────────────┐                                                             │
│   │ AUTOMOTIVE USB 2.0 HUB IC │                                                             │
│   │ (Microchip USB2512B-AEZG) │                                                             │
│   └─────────────┬─────────────┘                                                             │
│                 │                                                                           │
│                 ├─► Downstream Port 1: Glovebox / Jukebox USB-A (Flash Drive / Cable)       │
│                 │                                                                           │
│                 └─► Downstream Port 2: Internal Ottocast / CarlinKit Wireless Dongle        │
│                           ▲                                                                 │
│                           │ [ VBUS High-Side Power Switch TI TPS2051B ]                     │
│                           │ (Controlled by ESP32-C3 GPIO6 with Fault Feedback on GPIO7)     │
│                                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────────────────────┐  │
│   │ ESPRESSIF ESP32-C3-WROOM-02 CONTROLLER (160 MHz RISC-V, 4MB Flash)                   │  │
│   │                                                                                      │  │
│   │ • 2.4 GHz ESP-NOW Wireless Link (< 3 ms Latency) & BLE 5.0 2M-PHY to Central Box     │  │
│   │ • Knowles SPH0645LM4H Digital I2S MEMS Ambient Mic (Edge-RMS dB-A Noise Tracking)    │  │
│   │ • Hardware-Debounced Input for Hardwired Handlebar PTT (100% Battery-Free)           │  │
│   │ • TI TCAN334G 3.3V CAN Transceiver (Local Tap for Fairing / TFT Dashboard CAN-Bus)   │  │
│   │ • I2C / GPIO Status Management & Automated Ottocast Power Cycling                    │  │
│   └──────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                             │
│   POWER MANAGEMENT:                                                                         │
│   • 12V Vehicle Input (Protected to ISO 7637-2 against Load Dump & High-Voltage Spikes)     │
│   • TI LMR36015 36V Synchronous Buck Converter ──► 5.0 V / 2.0 A (Hub, USB Ports & Logic)   │
│   • TI TLV75533P Low-Noise LDO ─────────────────► 3.3 V / 500 mA (ESP32-C3, MEMS, TCAN334G)│
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼ 2.4 GHz ESP-NOW Wireless Link (< 3 ms Latency)
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                 CENTRAL BOX UNDER SEAT (ESP32-S3 HOST ENGINE)                               │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Circuit Design & Key Components

### 3.1 Automotive USB 2.0 Hub Controller (Microchip USB2512B)
* **Component:** **Microchip USB2512B-AEZG** (36-Pin QFN, $6 \times 6\,\text{mm}$, Automotive AEC-Q100 qualified, temperature rating $-40\,^\circ\text{C} \dots +85\,^\circ\text{C}$).
* **Upstream Interface:** Connects directly into the factory 4-wire USB harness from the Boom! Box GTS / Skyline OS head unit (`D+`, `D-`, `VBUS`, `GND`).
* **Integrated Termination:** Internal $45\,\Omega$ series termination resistors and phase-locked loop for clean eye diagrams over extended vehicle wiring.
* **Downstream Port 1 (Glovebox Jukebox):**
  * Powers the factory USB-A port in the glovebox.
  * Continuously energized with current-limited $V_{\text{BUS}}$ ($1.0\,\text{A}$).
  * Accommodates USB flash drives with MP3/FLAC music, phone emergency charging, or official dealer firmware updates.
* **Downstream Port 2 (Internal Wireless CarPlay Dongle):**
  * Concealed connection to *Ottocast U2-Air* or *CarlinKit 5.0*.
  * The $+5\,\text{V}$ power rail ($V_{\text{BUS}}$) is routed through the software-switched power distribution IC `U3`.

### 3.2 Software-Controlled $V_{\text{BUS}}$ Power Switch (TI TPS2051B)
* **Component:** **Texas Instruments TPS2051BDBVR** (SOT-23-5) Automotive High-Side Power Distribution Switch with current limiting ($0.5\,\text{A} \dots 1.0\,\text{A}$) and active-high enable.
* **Control Architecture:**
  * `EN` (Pin 4) is driven by **ESP32-C3 GPIO6**. Setting `HIGH` supplies power to the Ottocast; setting `LOW` cuts power cleanly ($I_{\text{off}} < 1\,\mu\text{A}$).
  * `FAULT_N` (Pin 3, open-drain) reports directly to **ESP32-C3 GPIO7** with a $10\,\text{k}\Omega$ pull-up, immediately flagging overcurrent or thermal overload conditions to firmware.

---

## 4. Smart Operating Modes & Automated Logic

By linking the power switch to the ESP32-C3 firmware, manual switches are completely obsoleted:

### 4.1 Automated Café & Carport Protection (Auto Wi-Fi Release)
1. **The Issue:** Wireless CarPlay adapters broadcast a dedicated 5 GHz Wi-Fi hotspot. When the motorcycle is parked outside a hotel or in a carport, the rider's phone inside often remains trapped in the bike's Wi-Fi network, blocking mobile data and home Wi-Fi.
2. **Automated Solution:**
   * Upon ignition shut-off (`KL15 = 0V`), the Smart Fairing Controller initiates a **60-second shutdown timer**.
   * When the timer expires (or immediately if Bluetooth RSSI to the rider's helmet drops), the MCU drives `GPIO6 = LOW`.
   * The Ottocast shuts down instantly. The smartphone seamlessly rejoins the home or cellular network with zero manual intervention.

### 4.2 One-Click Hard Reboot via WebApp / PWA
* Wireless CarPlay dongles can occasionally freeze due to 5 GHz channel congestion.
* **Solution:** The OpenMotorBridge WebApp dashboard features a **"Wireless CarPlay Adapter"** widget with status badges `[Active] [Off] [Reboot]`.
* Tapping **"Reboot"** power-cycles $V_{\text{BUS}}$ for exactly $2.5\,\text{seconds}$. The dongle re-enumerates cleanly—no stopping, no tools, and no disconnecting the battery required.

### 4.3 Automated Host Collision Prevention
* If the USB2512B hub senses a data enumeration event on Port 1 (e.g. plugging in a flash drive for Boom! Box navigation map updates or firmware flashes), the ESP32-C3 automatically powers down Port 2 (Ottocast) for the duration of the transfer.
* USB host address conflicts or interrupted head unit flashes are physically impossible.

---

## 5. Digital I2S MEMS Ambient Microphone & Edge-DSP

Road, engine, and wind noise are captured directly at the leading edge of the fairing:

```
    ┌──────────────────────┐
    │  SPH0645LM4H-B MEMS  │
    │  I2S Digital Micro   │
    └──────────┬───────────┘
               │ 24-Bit Digital Audio @ 16 kHz (BCLK, WS, DATA)
               ▼
    ┌──────────────────────┐
    │  ESP32-C3 EDGE-DSP   │ ──► A-Weighting Filter (400 Hz .. 4 kHz)
    │  (Onboard Algorithm) │ ──► RMS Noise Energy Calculation (dB-A) every 20 ms
    └──────────┬───────────┘
               │
               ▼ Telemetry Packet via ESP-NOW (1 Byte: e.g. 68 dBA)
    ┌──────────────────────┐
    │  CENTRAL BOX DSP     │ ──► Dynamic Helmet Volume Scaling (AGC)
    └──────────────────────┘
```

1. **Component:** **Knowles SPH0645LM4H-B** (Miniature SMD, $3.5 \times 2.65 \times 0.98\,\text{mm}$), native digital I2S output, $65\,\text{dB(A)}$ SNR.
2. **Acoustic Port:** Located on the downward-facing edge of the fairing enclosure, covered with a hydrophobic **Gore ePTFE acoustic vent** (IP67 waterproof, dust-sealed).
3. **Bandwidth-Efficient Edge Computing:**
   * Instead of streaming raw PCM audio over RF, the ESP32-C3 calculates the A-weighted RMS sound level locally in real time.
   * Every $20\,\text{ms}$, a tiny 4-byte telemetry packet is transmitted via ESP-NOW to the Central Box.
   * **Bandwidth footprint:** $< 1.5\,\text{kbps}$!
4. **Standstill Transparency Mode ($< 30\,\text{km/h}$):**
   * At stoplights or toll booths, the microphone can optionally stream compressed LC3 audio ($24\,\text{kbps}$) into the rider's helmet, allowing natural conversation without taking off the helmet.

---

## 6. Hardwired Handlebar PTT (100% Battery-Free)

* **Connector:** Weatherproof 2-pin connector (JST-JWPF or screw terminal) on the enclosure perimeter.
* **Protection Circuitry:**
  * $10\,\text{k}\Omega$ pull-up to $+3.3\,\text{V}$.
  * Hardware RC low-pass filter ($R = 1\,\text{k}\Omega, C = 100\,\text{nF}, \tau = 100\,\mu\text{s}$) for noise-free switch debouncing.
  * **Bourns CDSOT23-SM05U** bidirectional TVS diode protecting against electrostatic discharge (ESD $\pm 30\,\text{kV}$).
* **Ultra-Low Latency:** Edge-triggered GPIO interrupt sends an immediate high-priority ESP-NOW frame. Total system latency from button press to the TLP222A optocoupler closing in the rear pod is **under $4\,\text{ms}$**!
* **Zero Maintenance:** Completely battery-free, immune to freezing winter weather down to $-30\,^\circ\text{C}$.

---

## 7. ESP32-C3 Controller Pin Allocation

| Pin / GPIO | Signal Name | Direction | Connected Function |
| :---: | :--- | :---: | :--- |
| **IO0** | `PTT_INPUT_N` | IN (Interrupt) | Hardwired Handlebar PTT Button (Active-Low, RC Debounced) |
| **IO1** | `MIC_I2S_WS` | OUT | Word Select / Frame Sync for Knowles SPH0645 MEMS |
| **IO2** | `MIC_I2S_BCLK` | OUT | Bit Clock for Knowles SPH0645 MEMS ($512\,\text{kHz}$) |
| **IO3** | `MIC_I2S_DATA` | IN | Serial 24-bit Audio Data Stream |
| **IO4** | `TWAI_RX` | IN | CAN-Bus Receive Line from TCAN334G Transceiver |
| **IO5** | `TWAI_TX` | OUT | CAN-Bus Transmit Line to TCAN334G Transceiver |
| **IO6** | `OTTOCAST_PWR_EN`| OUT | High-Side Switch Enable for Ottocast $V_{\text{BUS}}$ (TPS2051B) |
| **IO7** | `OTTOCAST_FAULT_N`| IN | Overcurrent & Thermal Fault Flag from TPS2051B |
| **IO8** | `LED_STATUS_G` | OUT | Green Operational & Link Status LED |
| **IO9** | `BOOT_SW` | IN | Onboard Boot / Flash Button |
| **IO18** | `USB_D-` | BIDI | Native USB for Firmware Flash & Diagnostics |
| **IO19** | `USB_D+` | BIDI | Native USB for Firmware Flash & Diagnostics |

---

## 8. PCB Manufacturing Specification (`05_smart_fairing_pcba`)

| Parameter | Specification | Technical Rationale |
| :--- | :--- | :--- |
| **Dimensions** | **$65.0 \times 42.0 \times 1.6\,\text{mm}$** | Compact footprint for hidden installation behind fairing or instruments |
| **Layer Stackup** | **4 Layers (JLC04161H-7628)** | L1: Signals/RF, L2: Solid Ground Plane, L3: 5V/3V3 Power, L4: Signals |
| **Base Material** | **FR-4 TG150** | High glass-transition temperature withstands summer fairing heat |
| **Surface Finish** | **ENIG (Electroless Nickel Immersion Gold)** | Corrosion-resistant against condensation and temperature cycling |
| **Copper Weight** | **$35\,\mu\text{m}$ (1 oz)** all layers | Ample current-carrying capacity for DCDC converters and USB charging |
| **Transient Protection** | TVS Diode **SMCJ36CA** (1500W Peak) | Clamps ISO 7637-2 load dump and alternator transient spikes |
