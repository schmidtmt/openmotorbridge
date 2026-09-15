# 05 - Power Management, UPS & Vehicle Electrical Protection

This document specifies the dynamic power and protection management of OpenMotorBridge v8.0: the primary switching regulators (Central Box LM5164-Q1 & Front Node LMR36015), the uninterruptible power supply (UPS with BQ24075 and **2,200 mAh Flat LiPo**), automotive transient and reverse-polarity protection (ISO 7637-2), intelligent **dongle power management (1-click cold reboot & Auto-Café mode)**, **Apple Find My & Google Find My Device dual-beaconing**, and the multi-stage winter hibernation cascade (< 16.5 µA).

---

## 1. Primary Switching Regulators of the Assemblies

To achieve high efficiency with minimal self-heating inside sealed IP67 enclosures, both the Central Box and Front Node employ highly integrated synchronous step-down converters:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DCDC CONVERTER ARCHITECTURE IN THE SYSTEM                │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. CENTRAL BOX (PCBA 01): LM5164-Q1  │ 2. FRONT NODE (PCBA 05): LMR36015    │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Wide input range: 6.0 V - 65 V     │ • Input voltage: 4.2 V - 36 V        │
│ • Output: 5.0 V DC / 1.0 A Continuous│ • Output: 5.0 V DC / 2.0 A Continuous│
│ • Efficiency: > 88 % at full load    │ • Efficiency: 91.8 % at 2.0 A        │
│ • Transient protection up to 100 V   │ • Output ripple: 5.3 mVpp            │
│ • Supplies: MCU, Audio, UPS, Pod 1-3 │ • Supplies: ESP32-S3, USB2514B, VBUS │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 1.1 LM5164-Q1 Inductor & Filter Dimensioning
The energy storage inductance $L$ of the synchronous buck converter is calculated for continuous conduction mode (CCM) and minimal output ripple:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Calculation Parameters:** $V_{\text{IN,max}} = 65\,\text{V}$, $V_{\text{OUT}} = 5{,}0\,\text{V}$, $f_{\text{sw}} = 400\,\text{kHz}$, ripple current ratio $\Delta I_L = 0{,}30 \times I_{\text{OUT}} = 300\,\text{mA}$.
* **Result:** $L = \frac{5{,}0 \cdot (65 - 5)}{65 \cdot 0{,}30 \cdot 400 \times 10^3} \approx 38{,}4\,\mu\text{H} \rightarrow$ **Selected: $47\,\mu\text{H}$** (Würth WE-PD 744770147 / Coilcraft XAL5030-473, $I_{\text{sat}} = 2{,}1\,\text{A}$, $R_{\text{DC}} = 115\,\text{m}\Omega$).
* **Input Capacitance:** $2 \times 10\,\mu\text{F}$ 100V X7R multilayer ceramic capacitors (MLCC) reliably damp wiring harness inductances.

### 1.2 Laboratory Current Measurements (INA226 Precision Log @ 12.0 V Vehicle Net)
* **Normal Operation (Full Load):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ with active Sena & Cardo audio bridge, LoRa 868MHz RX, and 10 Hz Multi-GNSS).
* **UPS Post-Run (Wi-Fi WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ during active transfer with ignition OFF).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wakes in $< 5\,\text{ms}$ upon ignition ON).
* **ULP Winter Hibernate (> 72 h Inactive):** **$14{,}8\,\mu\text{A}$** (Measured with INA226; preserves starter battery from deep discharge even after 12 months).

---

## 2. Dynamic Power-Path Management & Integrated UPS

- **Power-Path Controller:** Texas Instruments **BQ24075** with automatic load and charge current distribution.
- **UPS Battery Cell:** 2,200 mAh wide-temperature single-cell flat LiPo ($3{,}7\,\text{V}$ nominal, $4{,}2\,\text{V}$ charge cutoff, operating discharge range $-20\,^\circ\text{C}$ to $+60\,^\circ\text{C}$, Type 504068 / 503870, $68 \times 39 \times 5{,}0\,\text{mm}$).
- **JEITA NTC Thermal Management (Murata 10k NTC on BQ24075 TS Pin):**
  - **Cold Inhibit ($T < 0\,^\circ\text{C}$):** Charging current is clamped to $0\,\text{mA}$ in hardware to prevent lithium plating and dendrite growth during winter riding. The system operates normally directly from vehicle power.
  - **Heat Inhibit ($T > 45\,^\circ\text{C}$):** Charging stops to protect the pouch cell against gas swelling from engine heat soak under the seat.
- **Seamless Cold-Crank Switchover ($6{,}5\,\text{V}$ Dip):**  
  When cranking heavy high-compression engines (e.g. 1200cc Boxer or V-Twin), battery voltage momentarily dips to $6{,}5\,\text{V}$. The BQ24075 switches to internal LiPo buffering in $< 8{,}5\,\mu\text{s}$ without dropping the 5V system rail $\rightarrow$ Audio streams, mesh connectivity, and GNSS logs stay 100% uninterrupted.
- **Graceful Shutdown Run-On:** Keeps the system alive after ignition OFF for:
  - Finalizing and flushing GPX telemetry blackbox files to the MicroSD card.
  - Searching for authorized home Wi-Fi networks and executing TLS 1.3 WebDAV synchronization.
  - Sending clean BLE disconnect events to paired smartphones.

### 2.1 Autonomous Crowdsourced Tracking & Anti-Theft Battery Endurance (Apple & Google Dual-Beacon)
When parked or if thieves sever the 12V motorcycle battery, the Central Box switches to the internal 2,200 mAh LiPo cell:
* **Interleaved Dual-Beaconing:** The ESP32-S3 broadcasts alternating Apple Find My (FMNP) and Google Find My Device (FMDN) BLE advertisements every 2.0 seconds ($2{,}5\,\text{ms}$ TX burst, average current draw $\approx 15\,\mu\text{A}$).
* **Shock Monitoring (Wake-on-Motion):** The 6-axis IMU (LIS3DH / ICM-42688) monitors physical tampering consuming only $6\,\mu\text{A}$.
* **Battery Budget:** With total quiescent draw of $\approx 31\,\mu\text{A}$ ($0{,}031\,\text{mA}$), the 2,200 mAh cell provides a theoretical standby endurance of over **70,000 hours (~8 years)**, or practically **3 to 4 years of autonomous tracking and alarm standby** accounting for self-discharge and sub-zero winter temperatures ($-15\,^\circ\text{C}$).

---

## 3. Automotive Transient, EMC & Polarity Protection (ISO 7637-2 & ISO 16750-2)

- **Overcurrent Protection:** Bourns `MF-MSMF050-2` resettable PPTC fuse (1812 SMD, $500\,\text{mA}$ hold / $1{,}0\,\text{A}$ trip).
- **Transient & Spike Clamping:** Littelfuse `SMBJ33CA` bidirectional TVS diode ($33\,\text{V}$ standoff, $53{,}3\,\text{V}$ max clamping). Provides the 65V-rated LM5164 regulator with $> 11{,}7\,\text{V}$ safe headroom during ISO 16750-2 Pulse 5b load dumps ($87\,\text{V}$).
- **Reverse Polarity Protection:** Diodes Inc. `DMP6023L` P-channel MOSFET with ultra-low on-resistance ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **LC-PI Filtering:** Dual-stage LC-PI filter ($10\,\mu\text{H}$ shielded automotive inductor + 2x $10\,\mu\text{F}$ X7R 100V ceramic capacitors) at KL30 and KL15 inputs.

---

## 4. Universal Front Node VBUS Power Gate & Ottocast State Machine

The Universal Front Node features intelligent power management for external wireless CarPlay / Android Auto dongles (*Ottocast / CarlinKit*):

```
                   FRONT NODE OTTOCAST POWER-GATE
┌────────────────────────────┐              ┌────────────────────────────┐
│ 12V Vehicle Net (KL15 IGN) │              │ ESP32-S3 Firmware          │
│ • Headlight / Accessory Tap├─────────────►│ • 1-Click Reboot Listener  │
│ • Reverse-Polarity & TVS   │              │ • Auto-Café 60s Countdown  │
└────────────────────────────┘              └─────────────┬──────────────┘
                                                          │ GPIO 1 (PWR_EN)
                                                          ▼
┌────────────────────────────┐              ┌────────────────────────────┐
│ Ottocast CarPlay Dongle    │  5V VBUS     │ TI TPS2051B Load Switch    │
│ • Port 2 (USB-A, Switched) │◄─────────────┤ • 1.05A Fast Short Clamp   │
│ • 1-Click Hard Restart     │ (max. 1.05A) │ • 1.2 ms Soft-Start Ramp   │
└────────────────────────────┘              └────────────────────────────┘
```

### 4.1 Automated Power Modes
1. **1-Click Hard Reboot:** If the CarPlay dongle freezes, clicking "⚡ CarPlay 1-Klick Kaltstart" in the WebApp triggers a 2.5-second VBUS disconnect via `TPS2051B` followed by a soft-start power-up ($1{,}2\,\text{ms}$).
2. **Auto-Café Mode (60s Timer):** Upon ignition OFF, VBUS remains energized for 60 seconds. If the engine is restarted within 60s, CarPlay resumes instantly. If the ignition remains off, VBUS cuts completely, allowing the rider's iPhone to automatically connect to home or hotel Wi-Fi without manual Bluetooth toggling.

---

## 5. Vehicle Battery Health Monitoring & 3-Tier Sleep Cascade

Vehicle battery voltage at KL15 and KL30 is monitored via precision voltage dividers ($100\,\text{k}\Omega / 10\,\text{k}\Omega$, $0{,}1\,\%$ tolerance) at `PIN_ADC_VIGN`:

### 5.1 Starter Battery Protection Thresholds

| Battery Chemistry | Nominal Voltage | Float / Running (Engine ON) | Low-Bat Warning | Hard Cut-Off (Protection) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Flooded Lead-Acid** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel Battery** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium Iron Phosphate)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starter Battery)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 5.2 3-Tier Power-Down Cascade

```
┌─────────────────────────────────────────────────────────────┐
│          3-TIER POWER-DOWN CASCADE UPON IGNITION OFF        │
├─────────────────────────────────────────────────────────────┤
│ 1. RUN-ON (0..15 min): WebDAV Upload & GPX Flush (45 mA)    │
│ 2. DEEP SLEEP (15 min..72 h): Ext-Interrupt KL15 (< 100 µA) │
│ 3. WINTER-HIBERNATE (> 72 h): ULP Deep Sleep (< 16.5 µA)    │
└─────────────────────────────────────────────────────────────┘
```

* **Tier 3 - ULP Hibernate:** In deep sleep, the system draws only **$14{,}8\,\mu\text{A}$**. Over 180 days of cold winter storage, OpenMotorBridge drains only **$0{,}064\,\text{Ah}$ ($0{,}53\,\%$)** of a typical 12 Ah motorcycle battery, guaranteeing effortless engine start in spring.

---

## 6. Decentralized Power Monitoring: Smart Keyfob LiPo & Front Node

The OpenMotorBridge ecosystem continuously monitors its decentralized peripheral nodes:

### 6.1 Front Node (PCBA 05): Electrical System Monitoring
Mounted in the cockpit, the Front Node is powered directly from the 12V vehicle electrical system via an onboard TI LM5164-Q1 buck converter. A high-impedance precision divider feeds an ADC input to report handlebar switchgear and cockpit socket voltages to the Central Box in real time.

### 6.2 Smart Keyfob & Pager (PCBA 07): LiPo Fuel Gauge (BLE Service 0x180F & LoRa)
The portable Smart Keyfob is powered by an internal 3.7V LiPo cell (350–500 mAh) charged via USB-C. A **Maxim MAX17048 I2C fuel gauge** measures State of Charge (SoC in %), cell voltage, and discharge rate without requiring an external sense resistor. The Keyfob reports its battery status periodically via the standard **Bluetooth SIG Battery Service (`UUID 0x180F`)** and within its periodic LoRa health beacons:

```
┌──────────────┬───────────────┬──────────────────────────────────────────────┐
│ SoC (LiPo)   │ Cell Voltage  │ System Reaction & Warning Level              │
├──────────────┼───────────────┼──────────────────────────────────────────────┤
│ **> 20 %**   │ 3.7 V - 4.2 V │ Normal Operation (Green indicator in WebApp) │
│ **≤ 15 %**   │ ≤ 3.6 V       │ **Yellow Early Warning:** Alternating yellow │
│              │               │ LED blink • Push: "Recharge Keyfob via USB-C"│
│              │               │ • Pager display shows low-battery icon       │
│ **≤ 5 %**    │ ≤ 3.3 V       │ **Critical Alarm:** Persistent red warning,  │
│              │               │ automatic ULP deep sleep to protect cell     │
└──────────────┴───────────────┴──────────────────────────────────────────────┘
```
