# 04 - Power Supply, UPS, Under-Voltage Protection, Winter Hibernation & Button Battery

This document specifies the dynamic power management (LM5164 buck converter + BQ24075 UPS), JEITA thermal protection, 3-tier vehicle battery discharge protection (winter hibernation $< 20\,\mu\text{A}$), and **cyclic CR2032 handlebar battery monitoring**.

---

## 1. Primary Switching Regulator (Buck Converter)
- **Regulator IC:** Texas Instruments LM5164-Q1 synchronous step-down regulator (Automotive Grade AEC-Q100).
- **Input Voltage Range:** 6.0 V to 65 V DC continuous (ISO 7637-2 transient protection up to 100 V).
- **Output Capability:** 5.0 V DC / 1.0 A continuous current powering host MCU, satellite pods, and LiPo charger.
- **Efficiency:** > 88% in main load range (12 V to 5 V @ 400 mA).

---

## 2. Dynamic Power-Path Management & Integrated UPS
- **Power-Path Controller:** Texas Instruments BQ24075 with dynamic power management (DPM).
- **UPS Battery Cell:** 1000 mAh wide-temperature single-cell LiPo pack (3.7 V nominal, 4.2 V charge termination, discharge range -20 °C to +60 °C).
- **JEITA NTC Thermal Management (Murata 10k NTC on BQ24075 TS Pin):**
  - **Cold Cutoff (T < 0 °C):** Charging current is cut in hardware to 0 mA (prevents lithium plating / dendrite formation). System runs directly from vehicle power.
  - **Hot Cutoff (T > 45 °C):** Charging cut to 0 mA (prevents cell swelling from engine heat under seat).
- **Seamless Switchover:** BQ24075 switches to battery in $< 5\,\mu\text{s}$ upon ignition shutoff without brownout on the 3.3V rail.
- **Graceful Shutdown Rundown:** Allows timed operation after ignition off for:
  - Finalizing and flushing GPX track logs to MicroSD.
  - Scanning for known home Wi-Fi networks and executing TLS 1.3 WebDAV sync.
  - Orderly BLE disconnection.

---

## 3. Automotive Transient, EMC & Reverse-Polarity Protection
- **Input Fuse:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
- **Surge & Spike Clamping:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) $\rightarrow$ gives the 65V LM5164 regulator $> 11.7\,\text{V}$ safe headroom during ISO 16750-2 load dump pulses.
- **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-channel MOSFET in ground path with ultra-low on-resistance ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **Filtering:** Two-stage LC-PI filter ($10\,\mu\text{H}$ shielded automotive inductor + 2x $10\,\mu\text{F}$ X7R 100V ceramic capacitors) on KL30/KL15 input.

---

## 4. Vehicle Battery Monitoring & 3-Tier Sleep Cascade

### 4.1 Voltage Sensing & Supported Battery Chemistries
Vehicle voltage on KL15 and KL30 is monitored via precision resistor dividers (100 kOhm / 10 kOhm, 0.1% tolerance, 1:11 ratio) on `PIN_ADC_VIGN` (GPIO 4):

| Battery Chemistry | Nominal Voltage | Charging (Engine ON) | Low-Bat Warning | Hard Cut-Off (Protection) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Wet Lead-Acid** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)**| 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel Battery** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium Iron Phosphate)**| 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starter Battery)**| 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 4.2 3-Tier Power-Down Cascade (Winter Storage Protection)

```
┌─────────────────────────────────────────────────────────────┐
│          3-TIER POWER-DOWN CASCADE UPON IGNITION OFF        │
├─────────────────────────────────────────────────────────────┤
│ 1. RUNDOWN (0..15 min): WebDAV upload & GPX flush (45 mA)   │
│ 2. DEEP SLEEP (15 min..72 h): Ext-interrupt KL15 (< 100 µA) │
│ 3. WINTER HIBERNATE (> 72 h): ULP deep shutdown (< 20 µA)   │
└─────────────────────────────────────────────────────────────┘
```

1. **Tier 1 - Active Rundown (0 to 15 minutes, $45\,\text{mA}$):**
   * Ignition (KL15) is off; system wraps up GPX logging, performs WebDAV upload, and disconnects BLE cleanly.
2. **Tier 2 - Standby Deep Sleep (15 minutes to 72 hours, $< 100\,\mu\text{A}$):**
   * High-power rails are shut down. ESP32-S3 wakes up in $< 5\,\text{ms}$ when KL15 goes HIGH.
3. **Tier 3 - Ultra-Low-Power Hibernate (> 72 hours inactivity, $< 20\,\mu\text{A}$):**
   * Protects the motorcycle battery over 6 to 12 months of winter storage (loss $< 1.5\%$ battery capacity per year), even without a maintenance trickle charger.

---

## 5. Handlebar Remote CR2032 Battery Monitoring (BLE Service 0x180F)

The wireless handlebar remote cyclically reports its remaining battery charge using standard **Bluetooth SIG Battery Service (`UUID 0x180F`)**:

```
┌──────────────┬───────────────┬──────────────────────────────────────────────┐
│ Battery Level│ CR2032 Voltage│ System Action & Alert Tier                   │
├──────────────┼───────────────┼──────────────────────────────────────────────┤
│ **> 20 %**   │ > 2.5 V       │ Normal Operation (Green indicator in WebApp) │
│ **≤ 15 %**   │ ≤ 2.3 V       │ **Yellow Early Warning:** Status LED yellow- │
│              │               │ red alternate flash • WebApp notification    │
│              │               │ • CAN-Bus alert frame to motorcycle TFT      │
│ **≤ 5 %**    │ ≤ 2.0 V       │ **Critical Alarm:** Persistent red alert     │
└──────────────┴───────────────┴──────────────────────────────────────────────┘
```

### 5.1 CAN-Bus Dashboard Notification
When connected to the motorcycle CAN bus (e.g. Harley-Davidson Skyline OS / Boom! Box or BMW Connected TFT), dropping below $V_{\text{CR2032}} \le 2.3\,\text{V}$ generates an on-screen prompt (*"Handlebar remote battery low - please replace CR2032"*).
