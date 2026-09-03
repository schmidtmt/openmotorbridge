# 11 - Digital Simulation & Multi-Physics Master Testbench (9 Modules)

To exhaustively verify the interaction of hardware, acoustics, vehicle dynamics, thermal behavior, high-frequency physics, and network protocols prior to physical manufacturing, OpenMotorBridge features a modular Python simulation suite.

---

## 1. Overview of the 9 Simulation Modules

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       OPENMOTORBRIDGE DIGITAL TESTBENCH SUITE                           │
├───────────────────────────┬───────────────────────────────────┬─────────────────────────┤
│ Module                    │ Script File                       │ Test Focus / Standard   │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 1. Multi-Board SPICE      │ `openmotorbridge_full_system_     │ 87V Load Dump, 6.5V UPS,│
│    System Simulation      │  sim.py`                          │ 85dB CMRR, Front Node   │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 2. Hardware-in-the-Loop   │ `firmware_hil_system_sim.py`      │ 10 Live Scenarios, PTT, │
│    Firmware Simulator     │                                   │ Front Node, DLE Mesh    │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 3. 8h Thermal Day Tour    │ `thermal_day_tour_sim.py`         │ -20°C Frost to +58°C    │
│    Multi-Physics          │                                   │ Under-Seat Heat Soak    │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 4. All-Weather RF Wave    │ `rf_rain_propagation_sim.py`      │ ITU-R P.838/P.840 Rain, │
│    Propagation            │                                   │ Fog, Spray, Dual-PHY    │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 5. Automotive Transient   │ `automotive_iso7637_pulses_sim.py`│ ISO 7637-2 Level 4      │
│    Immunity               │                                   │ -150V, +50V, +/-220V    │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 6. Acoustics & Wind DSP   │ `acoustic_wind_dsp_sim.py`        │ 180 km/h Wind (93dB SPL)│
│    Speech Intelligibility │                                   │ 120Hz HPF, STOI > 0.70  │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 7. 20-Rider Group Convoy  │ `mesh_group_scaling_sim.py`       │ 1.52 km Convoy, 100% PDR│
│    Mesh & Partitioning    │                                   │ DLE Sub-Mesh Split/Merge│
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 8. 180-Day Winter Storage │ `battery_winter_standby_sim.py`   │ 16.5 µA ULP-Hibernate,  │
│    Quiescent Drain        │                                   │ 0.59% Drain / 6 Months  │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 9. Universal Front Node & │ `front_node_wireless_hub_sim.py`  │ USB2512B Eye, MEMS DSP, │
│    Smart Fairing Hub      │                                   │ TPS2051B, ESP-NOW, OTA  │
└───────────────────────────┴───────────────────────────────────┴─────────────────────────┘
```

---

## 2. Multi-Board SPICE System Simulation (`openmotorbridge_full_system_sim.py`)

* **Verified Criteria:**
  1. **Automotive Load Dump (ISO 7637-2 / 87V Pulse 5b):** Clamping via SMBJ33CA TVS to safe $54{,}1\,\text{V}$ ($+10{,}9\,\text{V}$ headroom below the LM5164's 65V limit).
  2. **UPS Cold Crank (6.5V Dip):** BQ24075 engages LiPo backup within $8{,}5\,\mu\text{s}$ without dropping the 5V rail.
  3. **Bourns Audio Transformer CMRR:** $85{,}0\,\text{dB}$ common-mode rejection against alternator whine $\rightarrow$ Residual noise at codec $< 141\,\mu\text{V}$ ($67{,}9\,\text{dB}$ SNR).
  4. **1-Wire Signal Integrity over 1.5m Harness:** Rise time $t_{\text{rise}} = 1{,}74\,\mu\text{s}$ across $167{,}9\,\text{pF}$ total capacitance ($65{,}3\,\%$ margin to $5{,}0\,\mu\text{s}$ spec).
  5. **PTT-to-LoRa End-to-End Latency:** Total path from helmet key through optocoupler, Opus encoder, and UART bridge takes **$14{,}59\,\text{ms}$** ($< 25\,\text{ms}$ aviation standard).
  6. **Front Node DCDC & Hub:** LMR36015 buck converter delivers $91{,}8\,\%$ efficiency ($5{,}3\,\text{mV}$ ripple); USB2512B achieves $88{,}5\,\%$ eye opening with $18{,}5\,\text{ps}$ skew.
  7. **Front Node Zero-Latency PTT:** Glass-to-glass latency from mechanical handlebar switch over ESP-NOW to TLP222A optocoupler firing is only **$1{,}74\,\text{ms}$**.

---

## 3. Hardware-in-the-Loop (HIL) Firmware Simulator (`firmware_hil_system_sim.py`)

Executes production C++ firmware algorithms against a virtual multi-board testbench across 10 lifecycle scenarios:

* **Scenario 1:** Ignition ON (KL15 = $12{,}60\,\text{V}$) $\rightarrow$ Cold boot of all MCUs $\rightarrow$ ESP-NOW link established.
* **Scenario 2A (Blank Pod):** No 1-Wire ID detected $\rightarrow$ Automatic `"disabled"` profile (Mute at $-96\,\text{dB}$ to protect against open inputs).
* **Scenario 2B (Hot-Swap):** Insertion of Sena 60S / Cardo Edge cartridge on a live system $\rightarrow$ 1-Wire detection in $< 2\,\text{s}$ $\rightarrow$ Immediate profile loading and unmuting.
* **Scenario 3:** NEO-M9N GNSS 3D-DGPS lock (22 satellites) and 1-PPS hardware time sync.
* **Scenario 4 (Dual-PTT & Acoustics):**
  * Helmet PTT press $\rightarrow$ Opus 24k Mesh broadcast.
  * Handlebar PTT press $\rightarrow$ ESP-NOW Action Frame $\rightarrow$ Optocoupler firing in **$1{,}74\,\text{ms}$**.
  * Knowles SPH0645 MEMS captures wind noise at 130 km/h ($79\,\text{dBA}$) $\rightarrow$ Audio DSP AGC boosts volume by $+1{,}0\,\text{dB}$.
* **Scenario 5:** Engine start ($6{,}5\,\text{V}$ cranking dip) $\rightarrow$ Instant UPS takeover $\rightarrow$ 0 audio dropouts, 0 MCU reboots.
* **Scenario 6 (Cable Tear & Short):** M8 cable pulled out $\rightarrow$ Bourns PPTC trips in $1{,}2\,\text{ms}$ ($< 15\,\text{mA}$ fault current, zero voltage drop on main PCB) $\rightarrow$ Anti-pop mute protects speakers.
* **Scenario 7 (CAN-Bus Interruption):** TCAN334G fault protection $\rightarrow$ Seamless fallback to GNSS/IMU dead-reckoning.
* **Scenario 8 (Battery Voltage Alarm):**
  * Stage A ($< 11{,}8\,\text{V}$): Yellow LED, low battery chime, non-essential load shedding.
  * Stage B ($0{,}0\,\text{V}$ fuse blowout at 80 km/h): UPS takeover, voice warning *"WARNING: MAIN POWER LOST"*, emergency GPX sync.
* **Scenario 9 (Smart Fairing Power Gate):** 1-click hard reboot (2.5s VBUS cutoff) and Auto-Café 60s countdown timer.
* **Scenario 10:** Ignition OFF $\rightarrow$ 15-minute WebDAV/GPX sync window $\rightarrow$ ULP deep sleep ($< 20\,\mu\text{A}$).

---

## 4. Running the Master Testbench

All 9 testbenches run automatically with a single command:

```bash
python3 tools/run_all_simulations.py
```
