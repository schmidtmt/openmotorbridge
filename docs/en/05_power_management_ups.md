# 05 - Power Management, UPS Battery & Front Node Power Gate

This document specifies the complete power management architecture of OpenMotorBridge v8.0: the 72V automotive step-down converter, the uninterruptible LiPo power supply (UPS), the **Universal Front Node power gate (TI LMR36015 & TPS2051B)** with 1-click CarPlay hard reboot, and the ultra-low-power hibernation mode.

---

## 1. Central Box Power Supply (TI LM5164-Q1 & BQ24075 UPS)

Motorcycle electrical systems exhibit extreme voltage fluctuations ranging from severe cold cranking dips ($6{,}5\,\text{V}$) to destructive load-dump transients ($> 87\,\text{V}$):

```
VEHICLE 12V/24V BATTERY (KL30 / KL15)
┌─────────────────────────────────────────────────────────────┐
│ 1. Littelfuse SMBJ33CA TVS + Bourns PPTC Fuse (500mA/1A)    │
│ 2. TI LM5164-Q1 Wide-Vin Step-Down (9V - 72V In -> 5.15V Out)│
│ 3. TI BQ24075 Dynamic Power-Path Controller                 │
│    • System is powered primarily from the DCDC converter    │
│    • Excess current charges the internal 1000mAh 1S LiPo   │
│    • Seamless switchover to battery in < 8.5 µs during crank│
└─────────────────────────────────────────────────────────────┘
```

### 1.1 Cold Crank Ride-Through ($6.5\,\text{V}$)
When cranking a cold high-compression engine (e.g., 1200cc V-Twin or Boxer), the vehicle battery voltage momentarily collapses to $6{,}5\,\text{V}$. The BQ24075 instantaneously engages the LiPo battery backup without dropping the $5\,\text{V}$ internal rail, preventing MCU reboots, audio dropouts, or lost GPS tracks.

---

## 2. Universal Front Node Power Architecture (`PCBA 05`)

The Universal Front Node integrates a dedicated automotive power stage designed to supply high-power wireless CarPlay/Android Auto dongles and charging ports:

```
┌────────────────────────────────────────────────────────────────────────┐
│               PCBA 05: FRONT NODE POWER MANAGEMENT ARCHITECTURE        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. 12V BORDNETZ INPUT:                                                 │
│    • Reverse polarity protection (Schottky) & TVS clamp                │
│    • TI LMR36015F Synchronous Buck (36V In -> 5.00V / 2.0A Out)        │
│    • High efficiency of 91.8% -> Negligible thermal dissipation in pod │
├────────────────────────────────────────────────────────────────────────┤
│ 2. TI TPS2051B HIGH-SIDE VBUS POWER GATE:                             │
│    • Controls Port 1 USB-A VBUS supply to the Ottocast dongle          │
│    • Current clamp at 1.05A (short-circuit and inrush current safety)  │
│    • Soft-start turn-on in 1.2 ms (prevents 5V dip on 100 µF loads)    │
├────────────────────────────────────────────────────────────────────────┤
│ 3. INTELLIGENT WIRELESS DONGLE MANAGEMENT:                             │
│    • 1-Click Hard Reboot: Pulsed 2.5s VBUS cutoff to unfreeze dongles  │
│    • Auto-Café Mode: Shuts down VBUS 60s after ignition OFF to release │
│      the smartphone's Wi-Fi for café/home networks                     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Ultra-Low-Power Hibernate & Winter Storage

To protect the motorcycle battery during 6-month winter storage:
* **Current Consumption:** In deep hibernation, the entire system draws only **$16{,}5\,\mu\text{A}$** from the vehicle battery.
* **Winter Discharge:** Over 180 days, OpenMotorBridge drains less than **$0{,}071\,\text{Ah}$ ($0{,}59\,\%$)** of a standard 12 Ah motorcycle battery $\rightarrow$ The engine starts effortlessly on the first crank in spring.
