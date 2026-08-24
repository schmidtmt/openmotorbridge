# 16 - Simulation & Digital Testbench

To verify the interplay of hardware, acoustics, ride dynamics, and network protocols prior to hardware manufacturing at automotive standards, OpenMotorBridge includes a modular Python simulation suite.

---

## 1. Simulation Modules Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 OPENMOTORBRIDGE DIGITAL TESTBENCH SUITE                     │
├───────────────────────┬───────────────────────┬─────────────────────────────┤
│ Module                │ Script                │ Test Scope                  │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 1. Audio DSP &        │ `audio_dsp_sim.py`    │ Raised-Cosine Ducking,      │
│    Microphone Guard   │                       │ 4-Stage Overload Protect,   │
│                       │                       │ Local HearThrough Isolation │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 2. Power Management   │ `power_ups_sim.py`    │ KL15 Ignition Cycles,       │
│    & UPS Rundown      │                       │ Engine Crank Voltage Dip,   │
│                       │                       │ JEITA LiPo Guard, 15m Run   │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 3. ADR-EKF Sensor     │ `adr_ekf_sim.py`      │ 15-State Kalman Filter,     │
│    Fusion & Tunnels   │                       │ 2.5 km Tunnel GNSS Outage,  │
│                       │                       │ Dynamic Lean Angle at 45°   │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 4. 1-Wire Cartridges  │ `cartridge_optopulse_ │ DS2401 LittleFS Parser,     │
│    & Opto-Sequencer   │  sim.py`              │ TLP222A PhotoMOS ms Timing, │
│                       │                       │ Gain-Offset Calibration     │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 5. OpenMotorMesh      │ `omm_network_sim.py`  │ DLE Scoring & Election,     │
│    Protocol & Radar   │                       │ Pass Partitioning, LoRa,    │
│                       │                       │ Siren Early Warning 10 Hz   │
└───────────────────────┴───────────────────────┴─────────────────────────────┘
```

---

## 2. Audio DSP & Microphone Guard Simulation (`audio_dsp_sim.py`)

* **Synthetic Test Signals:**
  * Port 1 (Sena) & Port 2 (Cardo) voice streams ($48\,\text{kHz}$).
  * Garmin navigation prompt (Priority 1, duration $3.5\,\text{s}$).
  * Front ambient microphone with variable wind and traffic noise amplitude.
* **Verification Criteria:**
  1. **Ducking Depth:** Port 1 and Port 2 are attenuated by exactly $-12\,\text{dB}$ during navigation playback.
  2. **Attack / Release:** $15\,\text{ms}$ attack, $600\,\text{ms}$ hold, $250\,\text{ms}$ raised-cosine release.
  3. **Speed-Gating Transparency:** $0-15\,\text{km/h}$ ($0\,\text{dB}$) $\rightarrow 15-30\,\text{km/h}$ (Raised-Cosine Fade) $\rightarrow > 30\,\text{km/h}$ ($-96\,\text{dB}$ Mute).
  4. **Leakage Test:** $0.0\,\text{dB}$ cross-bleed of ambient audio into mesh TX channels.

---

## 3. Power Management & UPS Rundown Simulation (`power_ups_sim.py`)

* **Simulated Voltage Profiles:**
  * Standby quiescent voltage ($12.6\,\text{V}$).
  * Engine Crank: Starter voltage drop to $7.8\,\text{V}$ for $450\,\text{ms}$ $\rightarrow$ Seamless UPS LiPo buffer engagement.
  * Trip End: KL15 Ignition OFF $\rightarrow$ 15-minute countdown for WebDAV upload and BGH track flush.
  * Starter battery undervoltage protection ($< 11.8\,\text{V}$) and ULP deep sleep ($< 20\,\mu\text{A}$ after 72 hours).
  * JEITA charging cutoff for freezing temperature ($< 0^\circ\text{C}$) and extreme heat ($> 45^\circ\text{C}$).

---

## 4. 15-State ADR-EKF & Tunnel Navigation Simulation (`adr_ekf_sim.py`)

* **Scenario:** Alpine pass ride (Sustenpass) with tight switchbacks followed by entry into a $2.5\,\text{km}$ mountain tunnel with 100% GNSS blackout.
* **Sensor Streams:**
  * Bosch BMI270 6-Axis IMU ($100\,\text{Hz}$).
  * u-blox MAX-M10S GNSS ($10\,\text{Hz}$, drops in tunnel).
  * Vehicle CAN bus wheel speed odometer.
* **Verification Results:**
  * Maximum position drift after $2.5\,\text{km}$ tunnel navigation: $< 14.2\,\text{m}$.
  * Cornering lean angle accuracy: $\pm 0.8^\circ$.

---

## 5. 1-Wire Cartridge & PhotoMOS Sequencer Simulation (`cartridge_optopulse_sim.py`)

* **Execution Flow:**
  1. Hot-plug event triggered on GPIO 2.
  2. Read 64-bit Silicon Serial UID via 1-Wire.
  3. Load and parse matching JSON profile from LittleFS.
  4. Measure optocoupler timing pulse widths:
     * Mesh Toggle: $200\,\text{ms} \pm 5\,\text{ms}$.
     * Channel Advance: $800\,\text{ms} \pm 10\,\text{ms}$.
     * Pairing Hold: $5000\,\text{ms} \pm 20\,\text{ms}$.
     * Quick-Pair Sync: $200\,\text{ms}$ pulses at $2\,\text{Hz}$.

---

## 6. Running the Unified Testbench

Execute all verification simulators with a single command:

```bash
python3 tools/run_all_simulations.py
```
