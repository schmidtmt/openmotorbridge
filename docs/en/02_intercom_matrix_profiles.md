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

| Priority | Audio Source | Ducking Behavior | Target Endpoints |
| :---: | :--- | :--- | :--- |
| **1 (Highest)** | **Emergency Intercom / Warning** | Ducks all other audio to $-24\,\text{dB}$ | Driver & Passenger Helmets |
| **2** | **Navigation Prompts (GPS/CarPlay)** | Smooth Raised-Cosine Ducking ($-18\,\text{dB}$) | Driver Helmet |
| **3** | **Mesh Intercom (Sena / Cardo / OMM)** | Low latency, Full-Duplex mixing | Group Broadcast |
| **4 (Lowest)** | **Media Audio (Music / FM Radio)** | Background music stream | Helmets (Muted during voice) |
