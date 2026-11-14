# 05 - Power Management, UPS & Vehicle Electrical Protection

This document specifies the dynamic power and protection management of OpenMotorBridge v10.0 Standardized Node Architecture: the primary switching regulators (Central Box `LM2596S-5.0` & Front Node `TPS54302` + `SW3526`), the uninterruptible power supply (UPS with `BQ24075`, `TPS2115A`, and **2,200 mAh Flat LiPo**), the **Dual-Power Input Architecture (12V Net `J1` / 5V USB-C Service Input `J3`)**, automotive transient and reverse-polarity protection (ISO 7637-2 via `LM74700-Q1`), intelligent **dongle power management (1-click cold reboot & Auto-Café mode)**, **Apple Find My & Google Find My Device dual-beaconing**, and the multi-stage winter hibernation cascade (< 16.5 µA).

---

## 1. Primary Switching Regulators of the Assemblies

To achieve high efficiency and thermal headroom inside sealed IP67 enclosures, the regulator architecture is synchronized with [`07_pcba_hardware_pinouts.md`](file:///Users/schmidtm/openMotorBridge/docs/en/07_pcba_hardware_pinouts.md):

```
+-----------------------------------------------------------------------------+
|                    DCDC CONVERTER ARCHITECTURE IN THE SYSTEM                |
+--------------------------------------+--------------------------------------+
| 1. CENTRAL BOX (PCBA 01): LM2596S-5.0| 2. FRONT NODE (PCBA 05): TPS54302    |
+--------------------------------------+--------------------------------------+
| * Input (via LM74700): 6.0 V - 40 V  | * Input voltage: 4.5 V - 28 V        |
| * Output: 5.0 V DC / 3.0 A Continuous| * Output: 5.0 V DC / 3.0 A Continuous|
| * Post-reg: 2x AMS1117-3.3 LDOs      | * PD Source: SW3526 (65W Buck-Boost) |
| * UPS Mux: BQ24075 + TPS2115A OR-ing | * Protection: SMBJ24A + AO3401A P-FET|
| * Supplies: S31, Hub, Audio, UPS     | * Supplies: ESP32-P4/E22, Hub, OLEDs |
+--------------------------------------+--------------------------------------+
```

### 1.1 Inductor & Filter Dimensioning (`PCBA 01` & `PCBA 05`)
The energy storage inductance $L$ of the buck converters is dimensioned for continuous conduction mode (CCM) and low output ripple across audio and RF rails:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Central Box (`PCBA 01`, `U7 LM2596S-5.0`):** Shielded $33\,\mu\text{H} / 47\,\mu\text{H}$ power inductor ($I_{\text{sat}} \ge 3{,}5\,\text{A}$), feeding dual `AMS1117-3.3` LDO rails (`U3` for MCU/Hub logic and `U15` dedicated ultra-clean rail for `QCC3084`/`ES8388` Audio DSP).
* **Front Node (`PCBA 05`, `U1 TPS54302` & `U4 SW3526`):** `TPS54302` ($400\,\text{kHz}$ synchronous buck, $3{,}0\,\text{A}$) for logic, `USB2514Bi` hub, and dual OLEDs, paired with an onboard **`SW3526` 65W Synchronous Buck-Boost PD-Source Controller (`U4`)** supplying the Glovebox Hub (`PCBA 05B`).
* **Input Capacitance:** Multi-stage 100V X7R multilayer ceramic capacitors (MLCC) and bulk capacitors reliably damp wiring harness inductances.

### 1.2 Laboratory Current Measurements (INA226 Precision Log @ 12.0 V Vehicle Net)
* **Normal Operation (Logic + Audio/Mesh without PD fast-charging):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ with active Sena & Cardo audio bridge, LoRa 868MHz RX, and 10 Hz Multi-GNSS).
* **UPS Post-Run (Garage Wi-Fi WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ during active transfer with ignition OFF).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wakes in $< 5\,\text{ms}$ upon ignition ON).
* **ULP Winter Hibernate (> 72 h Inactive):** **$14{,}8\,\mu\text{A}$** (Preserves starter battery from deep discharge even after 12 months).

### 1.3 Dual-Power Input Architecture (12V Vehicle Net `J1` vs. 5V USB-C Service Input `J3`)

For firmware development, **Central Bus-DFU flashing**, PWA testing, and workbench diagnostics, the Central Box (`PCBA 01`) provides a reverse-current-protected **5V USB-C Service/Bench Input (`J3`)**:

```
             DUAL-INPUT POWER-ORING ARCHITECTURE (CENTRAL BOX PCBA 01)
+----------------------------+
| 12V VEHICLE NET (J1 DTM-6) |---> [F1 PPTC + D1 SMBJ33A + U1 LM74700 Ideal-Diode]
| KL30 (Batt) / KL15 (Ign.)  |         |
+----------------------------+         +---> 12V_SYS ---> [U12 TPS25921 Quad eFuse] (Pods/Front/Radar)
                                       |
                                       v
                                [U7 LM2596S-5.0 Buck] ---> 5V_BUCK ---+
                                                                      |
+----------------------------+                                        v
| 5V USB-C SERVICE PORT (J3) |---> [D3 LM66100 Ideal-Diode] -----> [U5 TPS2115A / 5V_SYS Rail]
| (PC / Standard 5V Supply)  |     (Zero Back-Feed Block)             * ESP32-S31 + USB2517I Hub
+----------------------------+                                        * BQ24075 UPS Charger (U2)
```

* **Clear Separation Between 5V Service Input (`J3`) and 12V High-Power Feed (`J1`):**
  * **On-Bike & 12V Testbench Operation (`J1` DTM06-6S):** When 12V vehicle power is applied to `J1`, `12V_SYS` feeds all four `TPS25921` eFuse branches (`U12`) for high-power 12V loads (Front Node 60W USB-PD Source via `SW3526`, Saddlebag Pods 30W USB-PD Source via `SW3516H`, 12V mechatronic solenoids, and 12V rear radar) as well as the `LM2596S-5.0` buck (`U7`) and `BQ24075` UPS charger.
  * **Workbench & Desk Diagnostics via 5V USB-C (`J3`):** When connected only to a laptop or 5V USB-C adapter via `J3`, the **`LM66100` Ideal Diode (`D3`)** directly powers the `5V_SYS` logic rail (`ESP32-S31`, `USB2517I` 7-port hub, Audio DSP, LoRa, and UPS charger). This enables full diagnostics and **Central Bus-DFU flashing** of the Central Box and downstream USB-bus nodes without a 12V power supply. (Note: `12V_SYS`, downstream 30W/60W USB-PD outputs `SW3516H`/`SW3526`, and 12V actuators remain unpowered during 5V-only USB service operation.)
  * **Zero Back-Feed Isolation:** `LM74700-Q1` (`U1`, 12V path), `LM66100` (`D3`, 5V USB path), and `TPS2115A` (`U5`) strictly prevent 12V vehicle power from back-feeding into the USB-C port / PC host and prevent 5V USB power from leaking into the vehicle harness.

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

- **Overcurrent Protection:** Resettable automotive PPTC fuse (`F1`) at the `J1` KL30 input plus dedicated 4-channel eFuses (`U12 TPS25921`) for all external branches.
- **Transient & Spike Clamping:** Littelfuse `SMBJ33A` / `SMBJ33CA` TVS diode (`D1`, $33\,\text{V}$ standoff) clamping ISO 16750-2 load dump transients.
- **Active Reverse Polarity Protection:** Texas Instruments **`LM74700-Q1`** (`U1`) ideal-diode controller driving an external N-channel MOSFET (`Q1`, $R_{\text{DS(on)}} < 10\,\text{m}\Omega$).
- **LC-PI Filtering:** Dual-stage LC-PI filter ($10\,\mu\text{H}$ shielded automotive inductor + $2 \times 10\,\mu\text{F}$ X7R 100V ceramic capacitors) at KL30 and KL15 inputs.

### 3.1 Two-Cable Architecture & Power Distribution with TI TPS25921 eFuse Protection
All peripheral connections from Central Box (`PCBA 01`) route through the **Two-Cable Architecture** (Cable 1: 6-pin Deutsch DTM `J1` for vehicle net/CAN; Cable 2: 16-pin Automotive Connector `J4` for periphery bus). Every external branch is hardware-protected on `PCBA 01` via a dedicated **TI TPS25921 eFuse (`U12`, `GPIO 13..16`)**:
* **Branch 1 (Front Node & Cockpit):** **60W Budget** (regulated locally on `PCBA 05` via the **`SW3526` Synchronous Buck-Boost PD-Source Controller `U4`** and `TPS54302` `U1`). Powers driver smartphone fast-charging (27–30W USB-PD/QC via the Glovebox Hub), dedicated motorcycle GPS (15W for Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), action-cam continuous power (10W weather-sealed USB-C), dual cockpit OLED displays (`PCBA 05C`, 2W in Speaker Corner Pods), and host MCU (`ESP32-P4` + `ESP32-E22`), sensor puck (`PCBA 05D`), & `USB2514Bi` hub (3.5W).
* **Branch 2 (Saddlebag Pod Left):** **30W USB-PD Budget** (regulated locally on `PCBA 03` via **`SW3516H` `U5`**) for internal in-bag USB receptacle (`J2`), `ESP32-C6-MINI-1U` host, `PCM2912A` audio codec, and mechatronic cold-start pushers.
* **Branch 3 (Saddlebag Pod Right):** **30W USB-PD Budget** for Bay 2, identical to Branch 2.
* **Branch 4 (Rear Radar MR20):** **12V Switched** (1.0A Max) for 77-GHz radar sensor and warning strobe LEDs.
* **Mechatronic Cold-Start Pulse:**
  * Each saddlebag pod incorporates dual mechatronic pushers (mini-solenoids on `012_universal_actuator_slide_bracket.scad`), switched via dual AO3400A MOSFETs on `PCBA 03`.
  * Upon ignition ON (KL15), the solenoids fire for 2.0 seconds (~4 N actuation force with Shore A50 silicone tips on Cardo or Sena power buttons) to cold-boot completely powered-off headsets from a zero-watt state; runtime control during riding then runs wear-free via BLE GATT / audio bus.
  * **Benefit:** Headsets remain 100% unpowered when parked (no marketing standby battery drain after 1-2 weeks!). Upon turning on the bike, they boot up reliably and connect immediately without opening the pod.
* **5-Port Glovebox Hub (`PCBA 05B`, `glovebox_power_injection_hub.scad`, `82 × 54 × 15 mm`) & Harley Headset Emulation via USB:**
  * Features **5× USB-C receptacles**: North edge with **`J1` (`FRONT`)** from Front Node (`PCBA 05`) and **`J2` (`HOST`)** to the Harley OEM glovebox media lead; South edge with **`J3` (`PHONE`, 30W USB-PD)**, **`J4` (`DONGLE`, 10W switched via `TPS2051B`)**, and **`J5` (`MEDIA`, USB 2.0 passthrough)**.
  * **Harley Headset Emulation via USB:** Connects the Front Node directly to the head unit at `J2` (`HOST`); OpenMotorBridge emulates a digital MFi / USB Audio Class headset, unlocks Apple CarPlay natively, and transmits intercom/voice microphones digitally without ground loops.
  * Adjustable current limit with overcurrent trip in $< 1\,\mu\text{s}$, automatic thermal shutdown ($150\,^\circ\text{C}$ junction clamp), and fault status reporting (`FLT`) to the `ESP32-S31`.
* **Cockpit Power-Only Outputs (Directly on Front Node PCBA 05):**
  * **15W Motorcycle GPS (`J10`):** 12V/1.25A or 5V/3A DC power feed for Garmin Zūmo XT2 / Tread / Chigee AIO-5. **Strictly Power-Only:** Completely devoid of USB host data lines (`D+`, `D-`) so the navigation unit immediately boots into active route guidance on ignition ON rather than entering computer mass storage mode.
  * **10W Action-Cam (`J8`):** Weather-sealed 5V/2A DC USB-C lead for GoPro Hero / Insta360 directly at the cockpit. **USB BC 1.2 DCP Specification:** `D+` and `D-` are shorted with $R < 200\,\Omega$ inside the plug with zero connection to the `USB2514B` host controller. The camera detects a dedicated wall/bike charger and never halts in a PC connection / webcam / MTP dialog. Direct cockpit connection avoids any cumbersome routing through the glove compartment.

---

## 4. Universal Front Node VBUS Power Gate & Ottocast State Machine

The Universal Front Node features intelligent power management for external wireless CarPlay / Android Auto dongles (*Ottocast / CarlinKit*):

```
                   FRONT NODE OTTOCAST POWER-GATE
+----------------------------+              +----------------------------+
| 12V Vehicle Net (KL15 IGN) |              | ESP32-S3 Firmware          |
| * Headlight / Accessory Tap+------------->| * 1-Click Reboot Listener  |
| * Reverse-Polarity & TVS   |              | * Auto-Café 60s Countdown  |
+----------------------------+              +-------------+--------------+
                                                          | GPIO 1 (PWR_EN)
                                                          v
+----------------------------+              +----------------------------+
| Ottocast CarPlay Dongle    |  5V VBUS     | TI TPS2051B Load Switch    |
| * Port 2 (USB-A, Switched) |<-------------+ * 1.05A Fast Short Clamp   |
| * 1-Click Hard Restart     | (max. 1.05A) | * 1.2 ms Soft-Start Ramp   |
+----------------------------+              +----------------------------+
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
+-------------------------------------------------------------+
|          3-TIER POWER-DOWN CASCADE UPON IGNITION OFF        |
+-------------------------------------------------------------+
| 1. RUN-ON (0..15 min): WebDAV Upload & GPX Flush (45 mA)    |
| 2. DEEP SLEEP (15 min..72 h): Ext-Interrupt KL15 (< 100 µA) |
| 3. WINTER-HIBERNATE (> 72 h): ULP Deep Sleep (< 16.5 µA)    |
+-------------------------------------------------------------+
```

* **Tier 3 - ULP Hibernate:** In deep sleep, the system draws only **$14{,}8\,\mu\text{A}$**. Over 180 days of cold winter storage, OpenMotorBridge drains only **$0{,}064\,\text{Ah}$ ($0{,}53\,\%$)** of a typical 12 Ah motorcycle battery, guaranteeing effortless engine start in spring.

---

## 6. Decentralized Power Monitoring: Smart Keyfob LiPo & Front Node

The OpenMotorBridge ecosystem continuously monitors its decentralized peripheral nodes:

### 6.1 Front Node (PCBA 05): Electrical System Monitoring
Mounted in the cockpit, the Front Node is powered via the 4-wire branch (12V + USB 2.0) from the Central Box and regulates locally via its `TPS54302` buck converter (`U1`) and `SW3526` 65W USB-PD controller (`U4`). A high-impedance precision divider feeds the `ESP32-P4` ADC input to report handlebar switchgear and cockpit socket voltages to the Central Box in real time.

### 6.2 Smart Keyfob & Pager (PCBA 07): LiPo Fuel Gauge (BLE Service 0x180F & LoRa)
The portable Smart Keyfob is powered by an internal 3.7V LiPo cell (350-500 mAh) charged via USB-C. A **Maxim MAX17048 I2C fuel gauge** measures State of Charge (SoC in %), cell voltage, and discharge rate without requiring an external sense resistor. The Keyfob reports its battery status periodically via the standard **Bluetooth SIG Battery Service (`UUID 0x180F`)** and within its periodic LoRa health beacons:

```
+--------------+---------------+----------------------------------------------+
| SoC (LiPo)   | Cell Voltage  | System Reaction & Warning Level              |
+--------------+---------------+----------------------------------------------+
| **> 20 %**   | 3.7 V - 4.2 V | Normal Operation (Green indicator in WebApp) |
| **≤ 15 %**   | ≤ 3.6 V       | **Yellow Early Warning:** Alternating yellow |
|              |               | LED blink * Push: "Recharge Keyfob via USB-C"|
|              |               | * Pager display shows low-battery icon       |
| **≤ 5 %**    | ≤ 3.3 V       | **Critical Alarm:** Persistent red warning,  |
|              |               | automatic ULP deep sleep to protect cell     |
+--------------+---------------+----------------------------------------------+
```
