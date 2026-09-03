# 02 - Intercom Matrix, Hardware Profiles & Dynamic Routing

This document defines the 5 OEM adapter classes (A through E), the dynamic LittleFS profile engine, the opto-isolated PTT keying architecture (< 1.8 ms latency), and the audio routing cross-matrix of OpenMotorBridge v8.0.

---

## 1. The 5 OEM Adapter Classes (A through E)

To support every intercom and radio standard on the market without proprietary lock-in, OpenMotorBridge categorizes all headsets into 5 distinct hardware classes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 5 OEM ADAPTER CLASSES (A THROUGH E)                         │
├───────┬───────────────────────────────┬───────────────────────────────┬────────────────┤
│ Class │ Intercom / Radio System       │ Interface / Cradle            │ Audio / PTT    │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **A** │ **Sena 50S / 60S / 30K / 20S**│ OEM Spring-Loaded Pogo Array  │ Galvanic Audio,│
│       │ (Mesh 2.0 / 3.0 & Wave)       │ Form-fit Snap-In with POM Lock│ Opto-PTT Keying│
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **B** │ **Cardo Packtalk Edge / Pro** │ Magnetic Air-Mount Cradle     │ Galvanic Audio,│
│       │ (Dynamic Mesh Comm. Gen 2)    │ Dual N52 Magnets + EPDM Strap │ Opto-PTT Keying│
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **C** │ **Midland BTR1 / XT Series**  │ Dovetail Slide / Bare-Board   │ Galvanic Audio,│
│       │ (Wave Mesh & Analog PMR446)   │ 2-Pin 2.5/3.5mm Double Jack   │ PhotoMOS PTT   │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **D** │ **OpenMotorMesh Transceiver** │ Direct Pod 3 Integration      │ LoRa 868 MHz,  │
│       │ (Long-Range LoRa & Multi-GNSS)│ RP2040 Coprocessor + SX1262   │ 10 Hz DGPS     │
├───────┼───────────────────────────────┼───────────────────────────────┼────────────────┤
│ **E** │ **Hermetic Dry-Box Blind Pod**│ Closed Front Bezel with       │ Mute (-96 dB), │
│       │ (Weatherproof Blank Cartridge)│ Internal 80x46x16mm Storage   │ 5V Rail OFF    │
└───────┴───────────────────────────────┴───────────────────────────────┴────────────────┘
```

---

## 2. Dynamic 1-Wire Profile Loading (LittleFS JSON Engine)

Each interchangeable cartridge integrates a **Maxim DS2401 64-Bit Silicon Serial ROM** on its carrier board (`PCBA 03`). Upon sliding a cartridge into Pod 1 or Pod 2:

1. **Hardware Detection:** The 1-Wire manager task on Core 0 reads the unique 64-bit ROM-ID within 25 ms.
2. **Profile Resolution:** The ROM-ID maps to a configuration file on the internal flash filesystem:
   * `0x01...` $\rightarrow$ `/profiles/sena_50s.json`
   * `0x02...` $\rightarrow$ `/profiles/cardo_edge.json`
   * `0x03...` $\rightarrow$ `/profiles/midland_pmr.json`
   * `0x04...` $\rightarrow$ `/profiles/omm_transceiver.json`
   * Unknown / Timeout $\rightarrow$ `/profiles/disabled.json` (Mute to prevent open noise).
3. **Dynamic DSP Parameterization:** The ES8388 Audio Codec automatically loads specific input sensitivities, Ducking curves, AGC thresholds, and optocoupler pulse timings without requiring a system reboot.

---

## 3. Opto-Isolated Zero-Latency PTT Keying (< 1.8 ms)

To trigger headset transmission (Push-to-Talk or Mesh Channel Toggle) cleanly without switch bouncing or voltage feedback into sensitive intercom inputs:

```
HANDLEBAR PTT PUSHBUTTON (COCKPIT)
┌─────────────────────────────────────────────────────────────┐
│ 1. Mechanical Handlebar Switch closes (Direct GPIO Interrupt)│
│ 2. ESP32-C3 builds IEEE 802.11 Vendor Action Frame (ESP-NOW)│
│ 3. Over-the-Air Transmission to Central Box: 0.90 ms        │
│ 4. ESP32-S3 Core 0 ISR decodes frame in 45 µs               │
│ 5. Toshiba TLP222A PhotoMOS switches in 0.50 ms             │
│ 6. Headset enters Transmit Mode: TOTAL LATENCY = 1.74 ms!   │
└─────────────────────────────────────────────────────────────┘
```

* **Galvanic Isolation:** The Toshiba TLP222A solid-state PhotoMOS relay isolates up to $1500\,\text{V}_{\text{RMS}}$ between motorcycle logic and the headset mic/key lines.
* **Bounce-Free:** Clean optical switching eliminates contact bounce and audio clicks.
* **Firmware Pulse Sequencer:** Supports configurable click patterns (Single-Click 200 ms for Mesh On/Off; Long-Press 1000 ms for Channel Switch).

---

## 4. Cross-Matrix Audio Routing & Priority Levels

The DSP mixer core routes audio signals dynamically across all connected endpoints:

| **Priority** | **Audio Source** | **Ducking Behavior** | **Target Endpoints** |
| :---: | :--- | :--- | :--- |
| **1 (Highest)** | **Emergency Intercom / Warning** | Ducks all other audio to $-24\,\text{dB}$ | Driver & Passenger Helmets |
| **2** | **Navigation Prompts (GPS/CarPlay)** | Smooth Raised-Cosine Ducking ($-18\,\text{dB}$) | Driver Helmet |
| **3** | **Mesh Intercom (Sena / Cardo / OMM)** | Low latency, Full-Duplex mixing | Group Broadcast |
| **4 (Lowest)** | **Media Audio (Music / FM Radio)** | Background music stream | Helmets (Muted during voice) |

---

## 5. 3-Phase Plug-and-Play Detection Sequence

To protect active headsets against electrical shorts and hot-plug transients, OpenMotorBridge executes a strict 3-phase hardware handshake:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CLASS-BASED HARDWARE PROFILE MATRIX                         │
├─────────┬───────────────────────────────┬─────────────────┬─────────────────┤
│ Class   │ Device Families               │ Mesh Protocol   │ DLE Score Bonus │
├─────────┼───────────────────────────────┼─────────────────┼─────────────────┤
│ **K1**  │ Sena 60S, Apex, 50S/R/C, SRL3 │ Sena Mesh 3.0/2 │ **+60 Points**  │
│ **K2**  │ Sena Spider RT1/ST1           │ Mesh 2.0 Basic  │ **+40 Points**  │
│ **K3**  │ Sena Vortex, 20S, 10S, SF, 5S │ Bluetooth 5.1/4 │ **+20 Points**  │
│ **K4**  │ Cardo Edge, Pro, Custom, Neo  │ Cardo DMC Gen2  │ **+60 Points**  │
│ **K5**  │ Cardo Freecom 4x/2x, Spirit HD│ Live Intercom   │ **+40 Points**  │
│ **K6**  │ Cardo Bold, Black, Slim       │ Cardo DMC Gen1  │ **+30 Points**  │
│ **K7**  │ Midland G9 Pro, Baofeng/UHF   │ PMR446 Analog   │ **+10 Points**  │
│ **K8**  │ Midland BTR1, Rush RCF, Wave  │ Midland Wave    │ **+30 Points**  │
│ **K0**  │ Disabled / Empty Slot         │ None            │ **0 Points**    │
└─────────┴───────────────────────────────┴─────────────────┴─────────────────┘
```

### 3.1 Detailed Device Classification & Profiles in Filesystem (`/data/profiles/`)
* **Class 1: Sena Next-Gen & High-Tier Mesh (`sena_60s.json`, `sena_apex.json`, `sena_50_series.json`):**
  * *Sena 60S:* Wave Mesh Intercom, up to 64 participants, dual-chip RF hardening, DLE +60 pts.
  * *Sena Apex / Apex Plus:* Mesh 3.0 reference cartridge, 32 nodes, DLE +60 pts.
  * *Sena 50S, 50R, 50C, SRL3, MeshPort Blue/Red:* Mesh 2.0/3.0, 24–32 nodes.
* **Class 2: Sena Spider & Mesh-Only (`sena_spider.json`):**
  * *Sena Spider RT1 / ST1:* Pure mesh devices without legacy Bluetooth intercom overhead, DLE +40 pts.
* **Class 3: Sena Bluetooth & 2-Way Intercom (`sena_vortex.json`, `sena_legacy_bt.json`):**
  * *Sena Vortex:* Bluetooth 5.1 2-way intercom (1:1 up to 1.2 km), quick-pair button trigger, DLE +20 pts.
  * *Sena 20S EVO, 30K, 10S, 10R, SF4/SF2, 5S, SMH10:* Jog-dial pulse sequence for BT multi-hop, DLE +20 pts.
* **Class 4: Cardo Dynamic Mesh Communications Gen2 (`cardo_dmc_gen2.json`):**
  * *Cardo Packtalk Pro, Edge, Custom, Neo:* DMC Gen2 with Open DMC, ultra-fast auto-reconnect, and DLE +60 pts.
* **Class 5: Cardo Live Intercom & Freecom Series (`cardo_freecom_live.json`):**
  * *Cardo Freecom 4x, Freecom 2x, Spirit HD:* Bluetooth 5.2 Live Intercom with automatic reconnect, DLE +40 pts.
* **Class 6: Cardo Legacy DMC Gen1 (`cardo_dmc_legacy.json`):**
  * *Cardo Packtalk Bold, Black, Slim, Smartpack:* DMC 1.0 with up to 15 participants, DLE +30 pts.
* **Class 7: Universal Analog & PMR446 Two-Way Radio Cartridges (`pmr446_gateway.json`):**
  * *Midland XT Series (XT10/XT30/XT50 Bare-Board) & Integrated SA818S Transceivers:* Compact PMR446 cartridge modules (500 mW ERP, 446.0–446.2 MHz, 16 channels, CTCSS/DCS) for analog group communications.
  * *Midland G9 Pro / Baofeng / Kenwood 2-Pin K-Type:* External handheld radios docked via weatherproof dual-jack faceplate.
  * *Hardware PTT:* Seamless keying via photoMOS relay (Toshiba TLP222A on Pin 6 `OPTO_PTT`) synchronized with handlebar PTT or automatic DSP threshold VOX.
  * *Audio Decoupling:* Galvanic isolation through studio-grade audio transformers (Bourns LM-NP-1001) completely suppresses alternator whine and ground loops.
* **Class 8: Midland Intercom & Wave Series (`midland_wave.json` / `midland_bt.json`):**
  * *Midland BTR1 Advanced, Rush RCF, BTX2 PRO S, Midland Wave, BT Mini:* Bluetooth 5.0/5.2 Intercom & Wave Mesh with digital audio pass-through and DLE +30 pts.

### 3.2 JSON Profile Schema Specification
Each hardware profile resides as an autonomous JSON file in the ESP32-S3 internal Flash filesystem (`/data/profiles/*.json`), specifying all gain, routing, and optocoupler timing parameters:

```json
{
  "id": "sena_60s",
  "name": "Sena 60S Wave Mesh 3.0",
  "vendor": "Sena Technologies",
  "hardware_tier": 1,
  "vcc_enabled": true,
  "vcc_current_limit_ma": 850,
  "soft_start_ms": 120,
  "input_gain_db": 0.0,
  "output_gain_db": -2.5,
  "ducking_attenuation_db": -12.0,
  "ducking_attack_ms": 35,
  "ducking_release_ms": 650,
  "noise_gate_threshold_db": -54,
  "control_mode": "pogo_pulse",
  "opto_trigger_duration_ms": 120,
  "opto_trigger_hold_ms": 1500,
  "mesh_capabilities": {
    "protocol": "Sena Wave Mesh 3.0",
    "max_group_nodes": 64,
    "dle_bonus_score": 60
  },
  "audio_routing": {
    "intercom_bridge": true,
    "rider_headset": true,
    "pillion_headset": true,
    "boombox_lineout": false
  }
}
```

---

## 4. 1-Wire DS2401 Cartridge Recognition & 3-Phase Plug-and-Play

Each cartridge carrier PCB (`openmotorbridge_pod_cartridge`) features a factory-soldered **Maxim/Analog Devices DS2401** silicon serial number chip, reporting a globally unique 64-bit UID (`Family Code 0x01 + 48-bit Serial + 8-bit CRC`) over a single data line.

```
┌─────────────────────────────────────────────────────────────┐
│          3-PHASE PLUG-AND-PLAY DETECTION SEQUENCE           │
├─────────────────────────────────────────────────────────────┤
│ 1. DETECTION: 1-Wire ID query (current-limited < 20 mA)     │
│ 2. VALIDATION: Family Code & 64-bit UID checked vs database │
│ 3. RELEASE: Only on match -> 5V MOSFET ON & Audio/UART live │
└─────────────────────────────────────────────────────────────┘
```

1. **Current-Limited Interrogation:** Upon cartridge insertion, the 5V high-side switch remains OFF. The 1-Wire driver polls with a current-limited sense voltage ($< 20\,\text{mA}$) to read the DS2401 UID.
2. **Dynamic Routing Assignment:**
   * **Rear Pod 3 UID detected:** Central Box switches pins 15/16 to high-speed UART (460,800 Baud) and initializes the NMEA/LoRa parser.
   * **Audio Cartridge (Sena/Cardo) detected:** Pins are routed to the Bourns audio path and ES8388 I2S DSP; the matching JSON profile is loaded.
   * **Blank Cartridge or Unassigned UID:** Bay remains unpowered (`disabled.json`).
3. **Controlled Soft-Start:** Once validated, the P-channel MOSFET energizes the cartridge via a soft-start ramp ($100-150\,\text{ms}$) preventing inrush dips.

---

## 5. OEM Adapter Connection System: Classes & Pinouts

OpenMotorBridge supports all standard commercial intercom units intact without opening their housings:

### 5.1 Cartridge Pinout Specification (`J2` / JST-SH 1.0 mm)

The 6-pin **JST-SH 1.0 mm header (`J2`)** on `PCBA 03` connects to the OEM headset cradle:

| Pin | Signal | Class A (+Mesh) | Class B (Sena 50S) | Class C (Cardo Edge)| Class E (PMR446) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Micro-USB Pin 5 (GND) | Pogo-Pin 1 (GND) | Air-Mount Pad 1 (GND) | Plug Shield / Chassis |
| **2** | `5V_VBUS` | Micro-USB Pin 1 (+5V) | Pogo-Pin 2 (5V Charge)| Air-Mount Pad 2 (5V Charge)| Battery Dummy 5V In |
| **3** | `AUDIO_R+` | *N/C (Pure BT Audio)* | Pogo-Pin 4 (Spk R+) | Air-Mount Pad 3 (Spk +)| Plug Speaker + |
| **4** | `AUDIO_R-` | *N/C (Pure BT Audio)* | Pogo-Pin 5 (Spk R-) | Air-Mount Pad 4 (Spk -)| Plug Speaker - |
| **5** | `MIC_IN+` | *N/C (Pure BT Audio)* | Pogo-Pin 6 (Mic +) | Air-Mount Pad 5 (Mic +)| Plug Microphone + |
| **6** | `OPTO_PTT` | *N/C* | Pogo-Pin 7 (Mesh-Btn)| *N/C* (Aux) | PTT Switch to Ground |

---

## 6. Safety Fallback: `disabled.json` & Zero-Trust Quarantine

If a bay is empty, a blank cartridge is inserted, or an unknown UID is read, ESP32-S3 immediately loads `disabled.json`:

```json
{
  "id": "disabled",
  "name": "Deaktiviert / Unbelegt (Disabled Slot)",
  "vendor": "OpenMotorBridge System",
  "hardware_tier": 0,
  "vcc_enabled": false,
  "soft_start_ms": 0,
  "input_gain_db": -96.0,
  "output_gain_db": -96.0,
  "ducking_attenuation_db": 0.0,
  "ducking_attack_ms": 0,
  "ducking_release_ms": 0,
  "noise_gate_threshold_db": -96,
  "control_mode": "disabled",
  "opto_trigger_duration_ms": 0,
  "opto_trigger_hold_ms": 0,
  "mesh_capabilities": {
    "protocol": "None",
    "max_group_nodes": 0,
    "dle_bonus_score": 0
  },
  "audio_routing": {
    "intercom_bridge": false,
    "rider_headset": false,
    "pillion_headset": false,
    "boombox_lineout": false
  }
}
```

### 6.1 Protective Actions of `disabled.json`
1. **Power Isolation (`vcc_enabled: false`):** The P-channel MOSFET disconnects power immediately $\rightarrow 0{,}0\,\text{mA}$ current draw.
2. **Audio Mute:** Codec input and output gains are locked to $-96\,\text{dB}$ eliminating open-line noise or crosstalk.
3. **High-Z Optocoupler:** TLP222A relays remain open.
4. **DLE Score = 0:** Prevents unverified hardware from affecting mesh leader election.

### 6.2 Zero-Trust Hardware Quarantine
Until newly inserted cartridge hardware (DS2401 UID) is assigned to a verified profile by the rider, the bay is **strictly treated as unpopulated**:
* **5V VCC Power Gate OFF (0.0 mA):** Prevents feeding incorrect voltage or current to an unknown device.
* **Audio DSP Mute (-96 dB):** Prevents audio popping or squeal.
* **Optocouplers High-Z (OFF):** Inhibits unintended button presses.
* **DLE Bonus = 0:** Zero weight in group election.
* **Controlled Soft-Release:** Only once confirmed in the WebApp (or matched in local flash), the controller executes a 50 ms soft-start ramp to power the module.

---

## 7. WebApp Workflow: Automatic Recognition & Profile Assignment

When new cartridge hardware is plugged in, the PWA launches an automated onboarding dialog:

```
┌─────────────────────────────────────────────────────────────┐
│ 🧩 NEW CARTRIDGE DETECTED!                                  │
├─────────────────────────────────────────────────────────────┤
│ Detected Bay:           Pod 1 (Left Frame)                  │
│ 1-Wire Silicon UID:     01:A2:3B:4C:5D:6E:7F:8A             │
├─────────────────────────────────────────────────────────────┤
│ This cartridge hardware is not yet linked to a profile.     │
│ Which intercom or radio is installed in this sled?          │
│                                                             │
│ Hardware Profile:  [ 🔵 Sena 50S / 50R / SRL3 (K1)      ▼ ] │
├─────────────────────────────────────────────────────────────┤
│ [ Assign Later ]            [ Assign & Save Profile ]       │
└─────────────────────────────────────────────────────────────┘
```

1. **Automatic Scan:** ESP32-S3 polls both 1-Wire ports every 2 seconds (`task_cartridge_manager`). Valid CRC8 and Family Code `0x01` triggers a BLE telemetry packet with the 64-bit UID to the WebApp.
2. **Assignment Modal:** The WebApp checks the UID against `/profiles/mapping.json` (or PWA `localStorage`). If unmapped, `#uuid-detect-modal` pops up automatically.
3. **Model Selection:** The rider selects their headset model from the dropdown list.
4. **Persistent Mapping:** The configuration `{"<UID>": "<profile_id>"}` is permanently saved to LittleFS and browser IndexedDB.
5. **Zero-Touch Reconnection:** Subsequent insertions into either pod bay automatically re-apply all gains and pulse timings without prompting.

### 7.1 Dynamic Profile Updates & JSON Merge Pipeline
When a manufacturer updates firmware (e.g. Sena upgrading from Mesh 2.0 to Mesh 3.0 or Cardo DMC Gen2 enhancements), OpenMotorBridge adapts via an automated **JSON merge pipeline**:

```
┌─────────────────────────────────────────────────────────────┐
│                 JSON PROFILE MERGE PIPELINE                 │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Base Vendor Profile       │ 2. Custom Rider Offsets      │
│    (e.g., sena_apex_v3.json) │    (Gains, Ducking Levels)   │
├──────────────────────────────┴──────────────────────────────┤
│                             ▼                               │
│ 3. Merged Live Profile in LittleFS Flash                    │
│    (Updated Opto Timings + Preserved Personal Settings)     │
└─────────────────────────────────────────────────────────────┘
```

* **Phase 1 (Base Parameters):** New optocoupler pulse durations, button timings, and DLE bonus ratings are loaded from the vendor release.
* **Phase 2 (User Settings Preservation):** Rider customizations (e.g. $+2{,}0\,\text{dB}$ mic gain, $-12\,\text{dB}$ nav ducking) override default values.
* **Phase 3 (Hot Reload):** The Central Box applies merged settings dynamically to the ES8388 codec and TLP222A pulse engine without requiring a reboot.

### 7.2 Hardware Upgrades (Replacing Headset in Existing Sled)
When upgrading an intercom inside an existing sled (e.g. replacing a Sena 20S with a Sena 60S Mesh 3.0 Wave):
1. **Persistent Silicon UID:** The DS2401 chip on `PCBA 03` retains its unique 64-bit ID.
2. **Dashboard Re-assignment:** In the **"🧩 Cartridges & DLE"** tab, the rider selects the new model from the dropdown.
3. **Automatic Overwrite:** The mapping `{"<UID>": "sena_60s"}` updates immediately in flash and browser storage.
4. **Instant Recognition:** Subsequent boot cycles immediately load the new profile with updated timings and higher DLE bonus (+60 pts).
5. **Ground-Truth Re-Sync (`🔄 Sync`):** The rider can verify flash mappings at any time with a single click.

---

## 8. Recommended Pod Configuration Scenarios

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   RECOMMENDED POD CONFIGURATION SCENARIOS                   │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ Setup Category        │ Pod 1 (Left)            │ Pod 2 (Right)             │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💎 **High-End Leader**│ **Sena 60S / Apex**     │ **Cardo Packtalk Edge**   │
│    (350 – 550 €)      │ (Mesh 3.0 Wave, Class B)│ (DMC Gen2 Air-Mount, Cl. C│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⚖️ **Price-Perf.**    │ **Sena Spider RT1/ST1** │ **Cardo Freecom 4x / Bold**│
│    (180 – 280 €)      │ (Mesh 2.0 Pure, Class B)│ (Live Intercom/DMC, Cl. D)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💰 **Budget Entry**   │ **Sena MeshPort Blue**  │ **IP67 Blank Cartridge**  │
│    (80 – 140 €)       │ (or Sena 20S/SF, Cl. A) │ (Slot unpowered/disabled) │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 🏔️ **Adventure/Offroad**│ **Sena Apex / 50S**   │ **Midland G9 Pro PMR446** │
│    (220 – 320 €)      │ (Mesh 3.0, Class B)     │ (Analog Radio Gateway, E) │
└───────────────────────┴─────────────────────────┴───────────────────────────┘
```
