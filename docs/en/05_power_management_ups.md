# 05 - Power Management, UPS & Vehicle Electrical Protection

This document specifies the dynamic power and protection management of OpenMotorBridge v10.0 Standardized Node Architecture: the primary switching regulators (Central Box `LM5164-Q1` & Front Node `TPS54302` + `SW3526`), the uninterruptible power supply (uninterruptible power supply with active `BQ24075` charger & power-path PMIC and **2,200 mAh Flat LiPo** on `J5` of PCBA 01, alongside `BQ24075` with 1,000 mAh LiPo on PCBA 09/10), the **Dual-Power Input Architecture (12V Net `J1` / 5V USB-C Service Input `J3`)**, automotive transient and reverse-polarity protection (ISO 7637-2 via `SMBJ33CA` and `LM66100` ideal diode), intelligent **dongle power management (1-click cold reboot & Auto-Café mode)**, **Apple Find My & Google Find My Device dual-beaconing**, and the multi-stage winter hibernation cascade (< 16.5 µA).

---

## 1. Primary Switching Regulators of the Assemblies

To achieve high efficiency and thermal headroom inside sealed IP67 enclosures, the regulator architecture is synchronized with [`07_pcba_hardware_pinouts.md`](07_pcba_hardware_pinouts.md):

```
+-----------------------------------------------------------------------------+
|                    DCDC CONVERTER ARCHITECTURE IN THE SYSTEM                |
+--------------------------------------+--------------------------------------+
| 1. CENTRAL BOX (PCBA 01): LM5164-Q1  | 2. FRONT NODE (PCBA 05): TPS54302    |
+--------------------------------------+--------------------------------------+
| * Input (via J1 DTM): 6.0 V - 100 V  | * Input voltage: 4.5 V - 28 V        |
| * Output: 5.0 V DC / 1.0 A Continuous| * Output: 5.0 V DC / 3.0 A Continuous|
| * Post-reg: TPS7A0533 LDO            | * PD Source: SW3526 (65W Buck-Boost) |
| * Dual-Input: LM66100 Ideal Diode    | * Protection: SMBJ24A + AO3401A P-FET|
| * Supplies: S31, Hub, Audio, LoRa    | * Supplies: ESP32-S31/E22, Hub, OLEDs |
+--------------------------------------+--------------------------------------+
```

### 1.1 Inductor & Filter Dimensioning (`PCBA 01` & `PCBA 05`)
The energy storage inductance $L$ of the buck converters is dimensioned for continuous conduction mode (CCM) and low output ripple across audio and RF rails:

$$L = \frac{V_{\text{OUT}} \cdot (V_{\text{IN,max}} - V_{\text{OUT}})}{V_{\text{IN,max}} \cdot \Delta I_L \cdot f_{\text{sw}}}$$

* **Central Box (`PCBA 01`, `U1 LM5164-Q1`):** Shielded $47\,\mu\text{H} / 68\,\mu\text{H}$ power inductor ($I_{\text{sat}} \ge 1{,}8\,\text{A}$), feeding ultra-low-IQ LDO `U11 TPS7A0533` (for `VCC_3V3` logic, digital hub, and audio DSP).
* **Front Node (`PCBA 05`, `U1 TPS54302` & `U4 SW3526`):** `TPS54302` ($400\,\text{kHz}$ synchronous buck, $3{,}0\,\text{A}$) for logic, `USB2514Bi` hub, dual OLEDs, and FSC-BT802, paired with an onboard **`SW3526` 65W Synchronous Buck-Boost PD-Source Controller (`U4`)** supplying the glovebox charging bay (15W inductive magnetic Qi puck + companion USB-C PD fast-charge port).
* **Input Capacitance:** Multi-stage 100V X7R multilayer ceramic capacitors (MLCC) and bulk capacitors reliably damp wiring harness inductances.

### 1.2 Laboratory Current Measurements (INA226 Precision Log @ 12.0 V Vehicle Net)
* **Normal Operation (Logic + Audio/Mesh without PD fast-charging):** $185\,\text{mA}$ ($2{,}22\,\text{W}$ with active Sena & Cardo audio bridge, LoRa 868MHz RX, and 10 Hz Multi-GNSS).
* **UPS Post-Run (Garage Wi-Fi WebDAV Sync):** $45\,\text{mA}$ ($0{,}54\,\text{W}$ during active transfer with ignition OFF).
* **Standby Deep Sleep (KL15 Ext-Interrupt):** **$92\,\mu\text{A}$** (System wakes in $< 5\,\text{ms}$ upon ignition ON).
* **ULP Winter Hibernate (> 72 h Inactive):** **$14{,}8\,\mu\text{A}$** (Preserves starter battery from deep discharge even after 12 months).

### 1.3 Dual-Power Input Architecture (12V Vehicle Net `J1` vs. 5V USB-C Service Input `J3`)

For firmware development, configuration, and desk diagnostics of the Central Box (`PCBA 01`), the Central Box does not require a 12V bench power supply and instead provides a reverse-current-protected **5V USB-C Service/Bench Input (`J3`)**:

```
             DUAL-INPUT POWER-ORING ARCHITECTURE (CENTRAL BOX PCBA 01)
+----------------------------+
| 12V VEHICLE NET (J1 DTM-6) |---> KL30_IN ---> [D2 SMBJ33CA TVS (33V Clamping)]
| KL30 (Batt) / KL15 (Ign.)  |        |
+----------------------------+        +---> [U12 TPS4H160-Q1 Quad Switch] ---> J6 Satellites (12V)
                                       |     (VBUS_FRONT, VBUS_POD1, VBUS_POD2, VBUS_RADAR)
                                       v
                                [U1 LM5164-Q1 Buck] (100V Wide-VIN Step-Down)
                                       |
                                       v
+----------------------------+   VCC_5V Rail <------------------------------+
| 5V USB-C SERVICE PORT (J3) |        |                                     |
| (PC / Standard 5V Supply)  |        +---> [U11 TPS7A0533 3.3V LDO]        |
+-------------+--------------+                 |                            |
              |                                v                            |
              +---> USBC_VBUS ---> [D3 LM66100 Ideal-Diode] ----------------+
                                   (Reverse Current Blocking / Zero Back-Feed)
```

* **Clear Separation of the Two Operating Modes:**
  * **1. On-Bike & 12V Testbench Full Operation (`J1` DTM06-6S on 12V Power):** When 12V vehicle net voltage is present at `J1`, the 100V synchronous step-down regulator **`U1` (`LM5164-Q1`)** efficiently converts vehicle voltage into `VCC_5V` and via the ultra-low-IQ LDO **`U11` (`TPS7A0533`)** into `VCC_3V3`. Simultaneously, the **`TPS4H160-Q1` Quad Automotive High-Side Smart Switch (`U12`)** switches monitored 12V power to the four peripheral branches on `J6` (`VBUS_FRONT`, `VBUS_POD1`, `VBUS_POD2`, `VBUS_RADAR`). In this mode, all satellites (`PCBA 05` Front Node, `PCBA 03` Pod 1/2, `PCBA 08` Rear Radar) are energized and can be flashed and operated over the 4-wire USB backbone via **Central Bus-DFU**.
  * **2. Workbench & Workshop Service Operation via 5V USB-C (`J3`):** When connected to a PC or USB charger, the **`LM66100` Ideal Diode (`D3`)** directly feeds the internal `VCC_5V` rail and via `U11` the 3.3V logic of the **Central Box (`PCBA 01`)** (`ESP32-S31`, `USB2517I` 7-port hub, Audio DSP, LoRa, and IMU).
  * **Bus-Wide Flashing & Workshop Power Budget:** Through the `USB2517I` 7-port hub on the Central Box, all peripheral branches (Branch 1 Front Node, Branch 2 Pod 1, Branch 3 Pod 2, Branch 4 Rear Radar) are linked over the USB bus, allowing the entire motorcycle to be flashed and diagnosed from this single USB-C service port via WebUSB / DFU.
    * **Power Budget Breakdown (Without external cockpit / glovebox loads):**
      * Central Box (`PCBA 01`): $\approx 1.6\,\text{W}$ ($320\,\text{mA}$)
      * Front Node & Sensor Puck (`PCBA 05` + `05D`): $\approx 1.4\,\text{W}$ ($280\,\text{mA}$)
      * Rear Radar (`PCBA 08` incl. MR20 Standby): $\approx 2.1\,\text{W}$ ($420\,\text{mA}$)
      * 2x Saddlebag Pods (`PCBA 02` + `03` incl. both OEM communicators in standby audio mode): $\approx 2.2\,\text{W}$ ($440\,\text{mA}$)
      * Harness and switching losses: $\approx 0.3\,\text{W}$
      * **Total Workshop Full Operation Power:** **$\approx 7.6\,\text{W}$ ($5.0\,\text{V} / 1.52\,\text{A}$)**.
      * *(Pure MCU flash/programming mode with radar RF idle and intercoms inactive: only $\approx 4.5\,\text{W}$ or $0.9\,\text{A}$, fully compliant with standard legacy USB 3.0).*
    * **Conclusion:** On any modern standard USB-C port ($5\,\text{V} / 3.0\,\text{A} = 15\,\text{W}$), the fully populated system uses only $\approx 51\,\%$ of the available power. Neither radar nor intercoms must be forcibly shut down in workshop mode. In firmware, internal LiPo charging via `BQ24075` is throttled to $500\,\text{mA}$ and external 30W smartphone fast-charging is disabled during bench mode.
  * **Zero Back-Feed Isolation:** The **`LM66100` Ideal Diode (`D3`)** strictly blocks reverse current from `VCC_5V` back to `J3`. When 12V vehicle power is active while a diagnostic laptop is plugged into `J3`, `D3` reliably prevents any back-feed into the programming PC.

---

## 2. Dynamic Power Management & Voltage Monitoring

- **Internal Voltage Regulation:** Texas Instruments **LM5164-Q1** (100V Synchronous Step-Down DC/DC Buck) for 5V and **TPS7A0533** (Ultra-Low Quiescent Current LDO) for 3.3V.
- **Battery & Temperature Sensing (`J5`):** 4-pin header for external battery monitoring and NTC thermistor:
  - **Voltage Divider `R12`/`R13` (100k/100k):** High-impedance divider feeding battery voltage to `BAT_SENSE` (`ADC1_CHANNEL_0` on ESP32-S31).
  - **NTC Divider `R14` (10k):** Measures pack temperature on `BAT_NTC` (`ADC1_CHANNEL_2`) for thermal charging protection.
- **Cold-Crank Immunity ($6.5\,\text{V}$ Dip):**
  When cranking heavy V-twin or boxer engines, the wide input range of the LM5164-Q1 (operational down to $6.0\,\text{V}$) combined with bulk decoupling maintains 5V and 3.3V logic rails without dropping out.
- **Graceful Shutdown Run-On:** Keeps the system alive after ignition OFF for:
  - Finalizing and flushing GPX telemetry blackbox files to the MicroSD card (`sdio_track_finalize()`).
  - WebDAV upload over home Wi-Fi or PWA relay.
  - Clean BLE disconnect signaling before entering deep sleep.

---

## 3. Automotive Transient, EMC & Polarity Protection (ISO 7637-2 & ISO 16750-2)

- **Overcurrent Protection & Current Limiting:** 4-channel automotive smart switch (**`U12 TPS4H160-Q1`**) with programmable current clamps for each external branch on `J6`.
- **Transient & Spike Clamping:** Littelfuse **`SMBJ33CA`** bidirectional TVS diode (**`D2`**, $33\,\text{V}$ standoff voltage) clamping ISO 16750-2 / ISO 7637-2 load dump spikes.
- **High-Voltage Rating:** The central buck converter **`U1 LM5164-Q1`** is rated for input transients up to $100\,\text{V}$, providing $> 45\,\text{V}$ margin above the clamped TVS voltage.
- **Decoupling & LC Filtering:** $10\,\mu\text{F}$ 100V X7R ceramic input capacitor (`C1`) at KL30 and LC filter network (`L1` $47\,\mu\text{H}$ + `C2` $22\,\mu\text{F}$) for minimum ripple on the 5V rail.

### 3.1 Two-Cable Architecture & Power Distribution with TI TPS4H160-Q1 Smart Switch Protection
All peripheral connections from Central Box (`PCBA 01`) route through the **Two-Cable Architecture** (Cable 1: 6-pin Deutsch DTM `J1` for vehicle net/CAN; Cable 2: 16-pin Automotive Connector `J4` for periphery bus). Every external branch is hardware-protected on `PCBA 01` via a dedicated channel of the **TI TPS4H160-Q1 Smart Switch (`U12`, `GPIO 13..16`)**:
* **Branch 1 (Front Node & Cockpit):** **60W Budget** (regulated locally on `PCBA 05` via the **`SW3526` Synchronous Buck-Boost PD-Source Controller `U4`** and `TPS54302` `U1`). Powers driver smartphone fast-charging (27–30W USB-PD/QC via the Glovebox Hub), dedicated motorcycle GPS (15W for Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), action-cam continuous power (10W weather-sealed USB-C), dual cockpit OLED displays (`PCBA 05C`, 2W in Speaker Corner Pods), and host MCU (`ESP32-S31` + `ESP32-E22`), sensor puck (`PCBA 05D`), & `USB2514Bi` hub (3.5W).
* **Branch 2 (Saddlebag Pod Left):** **30W USB-PD Budget** (regulated locally on `PCBA 03` via **`SW3516H` `U5`**) for internal in-bag USB receptacle (`J2`), `ESP32-C6-MINI-1U` host, `PCM2912A` audio codec, and mechatronic cold-start pushers.
* **Branch 3 (Saddlebag Pod Right):** **30W USB-PD Budget** for Bay 2, identical to Branch 2.
* **Branch 4 (Rear Radar MR20):** **12V Switched** (1.0A Max) for 77-GHz radar sensor and warning strobe LEDs.
* **Mechatronic Cold-Start Pulse:**
  * Each saddlebag pod incorporates dual mechatronic pushers (mini-solenoids on `012_universal_actuator_slide_bracket.scad`), switched via dual AO3400A MOSFETs on `PCBA 03`.
  * Upon ignition ON (KL15), the solenoids fire for 2.0 seconds (~4 N actuation force with Shore A50 silicone tips on Cardo or Sena power buttons) to cold-boot completely powered-off headsets from a zero-watt state; runtime control during riding then runs wear-free via BLE GATT / audio bus.
  * **Benefit:** Headsets remain 100% unpowered when parked (no marketing standby battery drain after 1-2 weeks!). Upon turning on the bike, they boot up reliably and connect immediately without opening the pod.
* **Glovebox Fast-Charging Architecture (Replacement of PCBA 05B):**
  * The legacy 5-port hub `PCBA 05B` and external wireless CarPlay/Android Auto dongles have been eliminated.
  * Instead, the glove compartment (e.g. Harley Touring) is powered via a rugged 2-wire DC feed from Front Node `J7` with up to 30–36W USB-PD / QC 4.0.
  * Installed in the compartment is a **magnetic Qi charging puck** (15W inductive Qi/Qi2 MagSafe, approx. 20–22W DC input power) plus a companion **USB-C PD fast-charge port** for full-speed wired charging (e.g. secondary phone or tablet).
  * Features adjustable current limiting with overcurrent trip in $< 1\,\mu\text{s}$ under short circuit, automatic thermal shutdown ($150\,^\circ\text{C}$ junction clamp), and monitoring by the `SW3526` controller.
* **Cockpit Power-Only Outputs (Directly on Front Node PCBA 05):**
  * **15W Motorcycle GPS (`J10`):** 12V/1.25A or 5V/3A DC power feed for Garmin Zūmo XT2 / Tread / Chigee AIO-5. **Strictly Power-Only:** Completely devoid of USB host data lines (`D+`, `D-`) so the navigation unit immediately boots into active route guidance on ignition ON rather than entering computer mass storage mode.
  * **10W Action-Cam (`J8`):** Weather-sealed 5V/2A DC USB-C lead for GoPro Hero / Insta360 directly at the cockpit. **USB BC 1.2 DCP Specification:** `D+` and `D-` are shorted with $R < 200\,\Omega$ inside the plug with zero connection to the `USB2514B` host controller. The camera detects a dedicated wall/bike charger and never halts in a PC connection / webcam / MTP dialog. Direct cockpit connection avoids any cumbersome routing through the glove compartment.

---

## 4. Glovebox Charging & Thermal Management (Qi Puck & USB-PD Fast-Charge)

By eliminating the CarPlay/Android Auto video streaming stack (no Wi-Fi Direct, no persistent H.264/H.265 hardware video decoding), smartphone thermal generation inside the closed glove compartment drops dramatically:

```
               GLOVEBOX CHARGING & POWER GATEWAY (30W USB-PD)
+----------------------------+              +----------------------------+
| 12V Vehicle Net (KL15 IGN) |              | Front Node PCBA 05         |
| * Headlight / Accessory Tap|              | * SW3526 PD Controller     |
+-------------+--------------+              | * I2C Telemetry & Protect  |
              |                             +-------------+--------------+
              v                                           |
+----------------------------+                            | 2-Wire DC Feed
| SW3526 Buck-Boost (J7)     +----------------------------+ (Up to 36W PD 3.0)
| * Up to 36W USB-PD / QC    |                            |
+----------------------------+                            v
                                            +----------------------------+
                                            | Glovebox Charging Bay      |
                                            | * 15W Qi Puck (MagSafe)    |
                                            | * Secondary USB-C PD Port  |
                                            +----------------------------+
```

### 4.1 Automatic Thermal Management & Overcurrent Protection
* The `SW3526` PD controller on `PCBA 05` continuously monitors current, voltage, and die temperature over I2C.
* In the event of excessive glovebox temperatures or smartphone misalignment on the Qi puck, the controller throttles charging current dynamically or performs a protective shutdown ($> 120\,^\circ\text{C}$).
* Upon ignition OFF (`KL15`), the power management engine safely disables charging with a delayed turn-off to protect the motorcycle battery.

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
Mounted in the cockpit, the Front Node is powered via the 4-wire branch (12V + USB 2.0) from the Central Box and regulates locally via its `TPS54302` buck converter (`U1`) and `SW3526` 65W USB-PD controller (`U4`). A high-impedance precision divider feeds the `ESP32-S31` ADC input to report handlebar switchgear and cockpit socket voltages to the Central Box in real time.

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

### 6.3 Central Box UPS LiPo (PCBA 01): BQ24075 & BAT_SENSE
The Central Box features an internal 1S LiPo cell (2,200 mAh) on `J5`, managed by the Texas Instruments `BQ24075RGTR` (`U4`) power-path PMIC:
* **Onboard Charging & UPS Power Path:** The cell charges automatically from the 5V system rail (`VCC_5V` from the LM5164-Q1 automotive buck or USB-C `J3`) at $I_{\mathrm{CHG}} = 1.0\,\text{A}$ ($I_{\mathrm{IN\_MAX}} = 1.5\,\text{A}$). Upon vehicle power interruption or cranking voltage dips, `U4` switches to the LiPo cell in $< 10\,\mu\text{s}$ glitch-free without MCU reboot.
* **Voltage Sensing (`BAT_SENSE`):** High-impedance divider `R12/R13` ($100\,\text{k}\Omega / 100\,\text{k}\Omega$) feeds cell voltage to `ADC1_CH9` (GPIO 10) of the ESP32-S31.
* **Thermal Protection (`BAT_NTC`):** The integrated $10\,\text{k}\Omega$ NTC thermistor on `J5` Pin 3 connects to `TS` of the `BQ24075` (JEITA charge cutoff below 0 °C and above 45 °C to prevent lithium plating during freezing winter conditions).
* **Thresholds & Cut-off:**
  * **$> 3.8\,\text{V}$ (> 60 % SoC):** Full UPS reserve (cranking buffer, GPX blackbox sealing, WebDAV sync).
  * **$\le 3.6\,\text{V}$ (approx. 15 % SoC):** Yellow early warning in telemetry; power-hungry background services suspended.
  * **$\le 3.3\,\text{V}$ (approx. 3 % SoC):** Emergency system cut-off into ULP deep sleep ($< 15\,\mu\text{A}$) to prevent irreversible cell damage from over-discharge.

### 6.4 OMM UCS Intercom Module (PCBA 09 / 10): LiPo & Autonomous Acoustic Voice Alerts
The universal ECE 22.06 intercom module (`PCBA 09` / `PCBA 10`) utilizes an internal 1S LiPo cell (1,000 mAh `Type 603040 / 602840`) on `BAT1` (JST-SH on bottom layer):
* **Operating Modes:**
  * *In Luggage Pod (Bay 1 / Bay 2):* Continuous charging via cartridge docking rail (`VCC_5V_PROT` via `U4` TS5A3159 / `J1` USB-C).
  * *In Helmet (Autonomous):* Standalone battery operation for 13–18 hours of continuous full-duplex intercom.
* **Acoustic In-Helmet Voice Prompts:**
  Because the OMM module in helmet mode connects directly via the ultra-low-power `ES8388` stereo codec (`U4`) and `J_HELMET` to the 40 mm helmet speakers, battery warnings are delivered prioritarily and distraction-free via voice prompts directly into the rider's ear:
  * **20 % SoC:** Gentle chime + voice prompt: *“Battery low – 20 percent remaining”*.
  * **10 % SoC:** Urgent double-beep + voice prompt: *“Battery critical – please recharge”*.
  * **5 % SoC:** Voice prompt: *“Battery empty – shutting down”* followed by graceful shutdown (ULP deep sleep to safeguard the LiPo cell).
* **Companion Notification:** Once the helmet comes within wireless range of the motorcycle (2.4 GHz OMM Mesh / BLE), the module transmits its battery state to the Front Node: the Cockpit OLEDs pop up `OMM BATT: 18% [!]`, and the WebApp dashboard updates in real time.

---

## 7. Multi-Battery Alert Infrastructure: LoRa Sentry, HomeSphere & Fallbacks

To ensure complete protection against unnoticed discharge during months of winter storage or long stays in windowless underground parking garages, OpenMotorBridge implements a multi-tier alert and reporting chain:

### 7.1 The Storage & Winter Hibernation Challenge
Motorcycle starter batteries suffer irreversible sulfation during winter storage if open-circuit voltage falls below $11.8\,\text{V}$ (lead-acid/AGM) or $12.8\,\text{V}$ (LiFePO4). Meanwhile, 2.4 GHz wireless technologies (Wi-Fi, BLE) fail completely through reinforced concrete ceilings and fire doors.

```
+-----------------------------------------------------------------------------+
|             MULTI-BATTERY STANDBY & WINTER ALERT PIPELINE                   |
+-----------------------------------------------------------------------------+
| 1. MOTORCYCLE (Garage): ESP32-S31 RTC Wakeup every 12h (40 ms Airtime)      |
|    -> Samples KL30 (Starter Batt), BAT_SENSE (UPS LiPo) & NTC (Temp)        |
|    -> Transmits 16-Byte LoRa Health Packet (0xFD) @ 868 MHz (+14..+22 dBm)  |
+-----------------------------------------------------------------------------+
                                      |
         +----------------------------+----------------------------+
         | (Primary: 868 MHz)                                      | (Fallback: Wi-Fi/IP)
         v                                                         v
+-------------------------------+                         +-------------------+
| HOMESPHERE USB LoRa Dongle    |                         | Home Wi-Fi Garage |
| * Penetrates reinforced concrete|                       | * MQTT / Webhook  |
| * HomeSphere Alert Engine     |                         | * Home Assistant  |
| * Push notification to phone  |                         | * ntfy / Telegram |
+-------------------------------+                         +-------------------+
```

### 7.2 Primary Route: 868 MHz Semtech SX1262 LoRa to HomeSphere (via USB LoRa Dongle)
* **Ultra-Low-Power Wake-up & Burst:** In winter storage, the Central Box remains in deep sleep ($< 15\,\mu\text{A}$ current draw).
* The internal RTC timer wakes the ESP32-S31 periodically (default: every 12 hours) for just **$pprox 40\,\text{ms}$**.
* The MCU samples the vehicle starter battery (`KL30`), UPS battery (`BAT_SENSE`), queries keyfob status via ultra-short BLE, and reads ambient temperature (`TMP117`/NTC).
* The onboard `SX1262` transceiver broadcasts a compact **16-byte LoRa health packet (`0xFD`)** at maximum transmit power (+14 to +22 dBm) in the 868 MHz SRD band.
* **HomeSphere Integration:** A **USB LoRa dongle** connected to the user's HomeSphere home automation hub receives the packet through reinforced concrete ceilings. HomeSphere feeds the telemetry directly into its existing alert infrastructure:
  * Instant smartphone push notification: *“⚠️ Motorcycle starter battery at 11.8 V – connect charger!”*
  * Battery health charts in the HomeSphere dashboard.
  * Smart garage outlet automation (e.g. activating a Ctek/Optimate trickle charger).

### 7.3 Fallback 1: Local Home Wi-Fi (Garage / Carport)
For riders without a LoRa dongle whose motorcycle is parked within home Wi-Fi range:
* During periodic wake-up, the ESP32-S31 attempts a brief connection to the configured home Wi-Fi.
* Telemetry alerts are dispatched directly over IP:
  * **Smart Home Hubs:** Dispatched via MQTT or REST webhook to **Home Assistant**, **ioBroker**, or **openHAB**.
  * **Standalone (No Server):** Direct HTTPS push via `esp_http_client` to services like **ntfy.sh**, **Pushover**, **Pushsafer**, or a **Telegram bot**.

### 7.4 Fallback 2: Public LoRaWAN / The Things Network (TTN)
* Because the onboard `SX1262` natively supports standard LoRaWAN Class A uplinks, the 16-byte winter health packet can be broadcast via public **The Things Network (TTN)** gateways.
* Urban and suburban regions provide dense free TTN coverage.
* A free TTN webhook forwards the payload to push notification endpoints on the rider's smartphone with **zero proprietary home receiving hardware**.

### 7.5 Fallback 3: Local Proximity & Ignition Sentry (Street Parking without RF Coverage)
For motorcycles parked on street curbs without any RF coverage:
* **BLE Proximity Beacon:** When the rider approaches with smartphone or keyfob, the Companion App / WebApp catches BLE advertisement packets and triggers a low-battery alert.
* **Cockpit Full-Screen Ignition Alert (KL15):** When the rider turns the key, the system evaluates battery voltage instantly before cranking. If terminal voltage is critically low, the **Dual Under-Perch Cockpit OLEDs** immediately present a prominent warning:
  ```
  +-----------------------------+
  |  ⚠️ 12V BATT LOW: 11.5 V    |
  |  START MOTOR IMMEDIATELY!   |
  +-----------------------------+
  ```
  An urgent voice alert plays through the helmet speakers, preventing the rider from flattening the battery by leaving accessories on.
