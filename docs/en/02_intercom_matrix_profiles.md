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

If a bay is empty, a blank cartridge is inserted, or an unknown UID is read:
1. **Power Cut (`vcc_enabled: false`):** The P-channel MOSFET stays open $\rightarrow 0{,}0\,\text{mA}$ quiescent draw.
2. **Audio Mute:** Codec input and output gains are locked to $-96\,\text{dB}$.
3. **High-Z Optocoupler:** TLP222A relays remain open.
4. **DLE Score = 0:** Prevents unverified hardware from affecting mesh leader election.

---

## 7. WebApp Workflow: Automatic Recognition & Profile Assignment

When unknown cartridge hardware is inserted, the PWA launches an automated onboarding dialog:
1. **Automatic Scan:** ESP32-S3 polls both 1-Wire ports every 2 seconds and forwards new UIDs via BLE.
2. **Assignment Modal:** The WebApp displays the `#uuid-detect-modal` prompt.
3. **Model Selection:** The rider selects their headset model from the dropdown list.
4. **Persistent Mapping:** The configuration `{"<UID>": "<profile_id>"}` is permanently saved to LittleFS and browser IndexedDB.
5. **Zero-Touch Reconnection:** Subsequent insertions automatically re-apply all gains and pulse timings.

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
