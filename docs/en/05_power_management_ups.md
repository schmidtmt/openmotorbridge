# 05 - Power Management, UPS Battery & Front Node Power Gate

This document specifies the complete power management architecture of OpenMotorBridge v8.0: the 72V automotive step-down converter, the uninterruptible LiPo power supply (UPS), the **Universal Front Node power gate (TI LMR36015 & TPS2051B)** with 1-click CarPlay hard reboot, and the ultra-low-power hibernation mode.

---

## 1. DCDC Buck Converter System Architecture

To achieve high efficiency and minimal internal thermal rise within hermetically sealed IP67 enclosures, both the Central Box and Front Node employ high-voltage synchronous buck converters:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   DCDC CONVERTER SYSTEM ARCHITECTURE                        │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. CENTRAL BOX (PCBA 01): LM5164-Q1  │ 2. FRONT NODE (PCBA 05): LMR36015    │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Wide-Vin Input: 6.0 V - 65 V       │ • Wide-Vin Input: 4.2 V - 36 V       │
│ • Output: 5.0 V DC / 1.0 A Continuous│ • Output: 5.0 V DC / 2.0 A Continuous│
│ • Full-Load Efficiency: > 88 %       │ • Full-Load Efficiency: 91.8 % @ 2.0A│
│ • Transient Immunity: up to 100 V    │ • Output Ripple: 5.3 mVpp            │
│ • Powers: MCU, Audio DSP, UPS, Pods  │ • Powers: ESP32-C3, USB Hub, VBUS    │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Dynamic Power-Path Management & Integrated UPS Battery

- **Power-Path Controller:** Texas Instruments **BQ24075** with automatic load and charge current distribution.
- **UPS Battery Cell:** 1000 mAh wide-temperature single-cell LiPo ($3{,}7\,\text{V}$ nominal, $4{,}2\,\text{V}$ charge cutoff, operating discharge range $-20\,^\circ\text{C}$ to $+60\,^\circ\text{C}$).
- **JEITA NTC Thermal Management (Murata 10k NTC on BQ24075 TS Pin):**
  - **Cold Inhibit ($T < 0\,^\circ\text{C}$):** Charging current is clamped to $0\,\text{mA}$ in hardware to prevent lithium plating and dendrite growth during winter riding. The system operates normally directly from vehicle power.
  - **Heat Inhibit ($T > 45\,^\circ\text{C}$):** Charging stops to protect the pouch cell against gas swelling from engine heat soak under the seat.
- **Seamless Cold-Crank Switchover ($6{,}5\,\text{V}$ Dip):**  
  When cranking heavy high-compression engines (e.g. 1200cc Boxer or V-Twin), battery voltage momentarily dips to $6{,}5\,\text{V}$. The BQ24075 switches to internal LiPo buffering in $< 8{,}5\,\mu\text{s}$ without dropping the 5V system rail $\rightarrow$ Audio streams, mesh connectivity, and GNSS logs stay 100% uninterrupted.
- **Graceful Shutdown Run-On:** Keeps the system alive after ignition OFF for:
  - Finalizing and flushing GPX telemetry blackbox files to the MicroSD card.
  - Searching for authorized home Wi-Fi networks and executing TLS 1.3 WebDAV synchronization.
  - Sending clean BLE disconnect events to paired smartphones.

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
│ 12V Vehicle Net (KL15 IGN) │              │ ESP32-C3 Firmware          │
│ • Headlight / Accessory Tap├─────────────►│ • 1-Click Reboot Listener  │
│ • Reverse-Polarity & TVS   │              │ • Auto-Café 60s Countdown  │
└────────────────────────────┘              └─────────────┬──────────────┘
                                                          │ GPIO 1 (PWR_EN)
                                                          ▼
┌────────────────────────────┐              ┌────────────────────────────┐
│ Ottocast CarPlay Dongle    │  5V VBUS     │ TI TPS2051B Load Switch    │
│ • Port 1 (USB-A, Switched) │◄─────────────┤ • 1.05A Fast Short Clamp   │
│ • 1-Click Hard Restart     │ (max. 1.05A) │ • 1.2 ms Soft-Start Ramp   │
└────────────────────────────┘              └────────────────────────────┘
```

### 4.1 Automated Power Modes
1. **1-Click Hard Reboot:** If the CarPlay dongle freezes, clicking "⚡ CarPlay 1-Klick Kaltstart" in the WebApp triggers a 2.5-second VBUS disconnect via `TPS2051B` followed by a soft-start power-up ($1{,}2\,\text{ms}$).
2. **Auto-Café Mode (60s Timer):** Upon ignition OFF, VBUS remains energized for 60 seconds. If the engine is restarted within 60s, CarPlay resumes instantly. If the ignition remains off, VBUS cuts completely, allowing the rider's iPhone to automatically connect to home or hotel Wi-Fi without manual Bluetooth toggling.

---

## 5. Ultra-Low-Power Hibernate & Winter Storage

To protect the motorcycle battery during 6-month winter storage:
* **Deep Hibernation Draw:** In deep sleep, the entire system draws only **$16{,}5\,\mu\text{A}$** from the vehicle battery.
* **180-Day Battery Audit:** Over 180 days of cold garage storage, OpenMotorBridge drains only **$0{,}071\,\text{Ah}$ ($0{,}59\,\%$)** of a standard 12 Ah motorcycle battery $\rightarrow$ Guarantees 100% effortless engine cranking on the first touch in spring.
