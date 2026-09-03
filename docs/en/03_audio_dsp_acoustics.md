# 03 - Audio DSP, Acoustics & Knowles MEMS Wind Tracking

This document specifies the audio architecture of OpenMotorBridge v8.0: the 1500 V RMS galvanically isolated transformer frontend, the Everest Semi ES8388 24-Bit / 48 kHz DSP audio engine, the **Knowles SPH0645 digital MEMS wind noise tracking**, IEC 61672-1 Class 1 Biquad A-weighting, and the click-free Raised-Cosine Ducking algorithm.

---

## 1. Galvanically Isolated Audio Frontend (Bourns LM-NP-1001)

To eliminate ground loops, alternator hum (1.2 kHz stator whine), and ignition interference:

```
MOTORCYCLE CHASSIS / VEHICLE GROUND                 ISOLATED AUDIO SUBSYSTEM
┌──────────────────────────────────────┐          ┌───────────────────────────┐
│ Alternator Whine & Spikes            │          │ Pure, Ground-Free Audio   │
│ • Ground offset differences up to 3V │  1500V   │ • True Differential In/Out│
│ • Ignition pulses on battery line    ├─── XFMR ─┤ • 85 dB CMRR Common-Mode  │
│ • High-frequency inverter noise      │  BARRIER │   Rejection Ratio         │
└──────────────────────────────────────┘          └───────────────────────────┘
```

* **Audio Isolation Transformers:** Two Bourns LM-NP-1001 transformers provide $1500\,\text{V}_{\text{RMS}}$ dielectric isolation between vehicle ground and sensitive headset audio lines.
* **Common-Mode Rejection Ratio (CMRR):** Achieves $85{,}0\,\text{dB}$ CMRR at $1{,}2\,\text{kHz}$, reducing residual alternator ripple to $< 141\,\mu\text{V}$ ($> 67{,}9\,\text{dB}$ Speech SNR).
* **Flat Frequency Response:** $\pm 0{,}2\,\text{dB}$ across $20\,\text{Hz} \dots 20\,\text{kHz}$ for high-fidelity music streaming.

---

## 2. ES8388 24-Bit / 48 kHz Codec & I2S DMA Engine

The Everest Semiconductor ES8388 24-bit stereo codec interfaces directly with Core 1 of the ESP32-S3 over I2S DMA:
* **Sampling Rate:** $f_s = 48\,\text{kHz}$ at 24-bit resolution.
* **Double-Buffered DMA:** 128 samples per buffer ($2{,}67\,\text{ms}$ frame length), minimizing latency while avoiding buffer underruns.
* **Dynamic Range:** $96\,\text{dB}$ SNR on DAC outputs; $92\,\text{dB}$ on ADC inputs.

---

## 3. Knowles SPH0645 Digital MEMS Acoustic Tracking

The Universal Front Node (`PCBA 05`) houses a Knowles SPH0645LM4H digital I2S MEMS microphone positioned behind an aerodynamic, hydrophobic ePTFE acoustic channel:

```
┌────────────────────────────────────────────────────────────────────────┐
│             KNOWLES SPH0645 DIGITAL MEMS NOISE TRACKING PIPELINE       │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Acoustic Input: Ambient Cockpit & Wind Noise (35 to 115 dBA)        │
│ 2. ePTFE Gore Membrane: 100% Water/Dust Sealed (< 0.5 dB attenuation)  │
│ 3. 24-Bit I2S DMA Sampling at 16 kHz                                  │
│ 4. Direct Form II Biquad A-Weighting Filter (IEC 61672-1 Class 1)     │
│    • Low-frequency wind rumble (100 Hz) attenuated by -19.1 dB        │
│ 5. RMS Power Block Calculation (20 ms sliding window)                 │
│ 6. Fast ESP-NOW Telemetry Broadcast to Central Box at 50 Hz           │
│ 7. Dynamic AGC Helmet Boost: Automatically scales volume +0 to +6 dB   │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Acoustic Adaptation Formula
The automatic gain control (AGC) smoothly adapts helmet speaker output based on vehicle speed and wind turbulence:

$$\text{Gain}_{\text{boost}} = \min\left(6{,}0\,\text{dB}, \max\left(0{,}0\,\text{dB}, (\text{SPL}_{\text{dBA}} - 65\,\text{dBA}) \times 0{,}15\,\frac{\text{dB}}{\text{dBA}}\right)\right)$$

* **Idle / Low Speed (< 50 km/h, < 65 dBA):** $0{,}0\,\text{dB}$ boost $\rightarrow$ Natural, comfortable listening volume.
* **High Speed (130 km/h, ~80 dBA):** $+2{,}25\,\text{dB}$ boost $\rightarrow$ Clear intercom and navigation comprehension.
* **Maximum Turbulence (> 160 km/h, > 105 dBA):** $+6{,}0\,\text{dB}$ boost with lookahead brickwall limiting to prevent distortion.

---

## 4. Click-Free Raised-Cosine Audio Ducking & Priority Matrix

Standard threshold-based ducking causes abrupt volume jumps and audible clicks. OpenMotorBridge employs a mathematically continuous **Raised-Cosine Ducking Curve**:

### 4.1 Attack Phase (Smooth Attenuation of Background Audio)
$$g(t) = g_{\min} + \frac{1 - g_{\min}}{2} \left[1 + \cos\left(\frac{\pi \cdot t}{T_{\text{attack}}}\right)\right] \quad \text{for } 0 \le t \le T_{\text{attack}}$$

### 4.2 Release Phase (Smooth Restoration to Full Level)
$$g(t) = g_{\min} + \frac{1 - g_{\min}}{2} \left[1 - \cos\left(\frac{\pi \cdot t}{T_{\text{release}}}\right)\right] \quad \text{for } 0 \le t \le T_{\text{release}}$$

* **Attack Time ($T_{\text{attack}}$):** $15\,\text{ms}$ smooth descent (inaudible transition, zero pop/clicks, $\text{THD} < 0{,}005\,\%$).
* **Hold Time ($T_{\text{hold}}$):** $600\,\text{ms}$ retention to prevent pumping between conversational pauses.
* **Release Time ($T_{\text{release}}$):** $250\,\text{ms}$ smooth raised-cosine restoration.

### 4.3 Priority & Ducking Matrix
```
┌─────────┬──────────────────────┬─────────────┬──────────────┬──────────────────────────────┐
│ Priority│ Audio Source         │ Attenuation │ Attack Time  │ Preemption Behavior          │
├─────────┼──────────────────────┼─────────────┼──────────────┼──────────────────────────────┤
│ **Prio 1**│ Collision Alert / SOS│ **0.0 dB**  │ Immediate    │ Mutes all background sources │
│ **Prio 2**│ Navigation Voice     │ **-12.0 dB**│ 15 ms        │ Ducks Intercom & Music       │
│ **Prio 3**│ Intercom (P1 & P2)   │ **-15.0 dB**│ 35 ms        │ Ducks A2DP Media / Radio     │
│ **Prio 4**│ A2DP Music / Radio   │ Baseline    │ 250 ms       │ Background entertainment     │
└─────────┴──────────────────────┴─────────────┴──────────────┴──────────────────────────────┘
```

---

## 5. FreeRTOS Core 1 Audio-DMA Real-Time Pipeline & Codec Setup

The audio DSP engine runs on dedicated **Core 1** of the ESP32-S3 host MCU with maximum real-time priority:

```
                  FREERTOS CORE 1 REAL-TIME AUDIO PIPELINE
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ [ ES8388 I2S RX DMA ] ──► [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
│                                           │                                             │
│                                           ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. DC-BLOCK & HIGHPASS: 2nd Order Butterworth (fc = 45 Hz)                          │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. NOISE GATE & EXPANDER: Spectral Subtraction (-54 dBFS Threshold)                 │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. DUCKING MIXER: Computes Raised-Cosine Interpolation across active streams        │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4. LOOKAHEAD BRICKWALL LIMITER: 1 ms Soft-Knee Limiter (Prevents 0 dBFS clipping)   │ │
│ └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                             │
│                                           ▼                                             │
│ [ ES8388 I2S TX DMA ] ◄── [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 ES8388 Low-Level Register Configuration & I2S DMA Architecture
* **Sample Rates & Master Clock:**
  * Sample Rate: $F_s = 48{,}0\,\text{kHz}$ (24-bit Stereo).
  * Master Clock: $MCLK = 256 \times F_s = 12{,}288\,\text{MHz}$ (generated via ESP32-S3 Audio PLL on GPIO 0).
  * Bit Clock: $BCLK = 64 \times F_s = 3{,}072\,\text{MHz}$ (32-bit slot for precise 24-bit audio).
  * Left/Right Word Clock: $LRCK = F_s = 48{,}0\,\text{kHz}$.
* **DMA Buffer Descriptors:**
  * 4 chained DMA buffer descriptors with 128 stereo samples each ($2{,}67\,\text{ms}$ latency block).
  * Total Round-Trip Audio Latency (ADC $\rightarrow$ FreeRTOS DSP $\rightarrow$ DAC): **$7{,}85\,\text{ms}$** (far below the human detection threshold of $15\,\text{ms}$).
* **Hardware ALC Configuration (`Reg 0x12 - 0x17`):**
  * Target Level: $-6\,\text{dBFS}$, Max Gain: $+24\,\text{dB}$, Min Gain: $-12\,\text{dB}$.
  * Attack Time: $5\,\text{ms}$, Decay Time: $200\,\text{ms}$, Noise Gate Threshold: $-54\,\text{dBFS}$.

### 5.2 The 4 System Operating Modes
1. **Mode 1 (Touring-Duo):** Rider and passenger communicate in full duplex. Navigation voice ducks at $-12\,\text{dB}$. Media ducks at $-15\,\text{dB}$ during intercom traffic.
2. **Mode 2 (Highway-Solo):** Solo rider mode. Pod 2 is completely unpowered (`disabled.json`). Full DSP focus on telephone calls, CarPlay/Android Auto, and blind-spot radar acoustic alerts.
3. **Mode 3 (Group-Mesh Bridge):** Pod 1 (Sena) and Pod 2 (Cardo) operate in parallel. Symmetrical cross-mixing bridges both mesh ecosystems in real time.
4. **Mode 4 (Emergency-Override):** LoRa distress beacon or collision alarm (TTC < 3.5s) immediately mutes all other sources to $-24\,\text{dB}$ and injects emergency audio with maximum headroom.

---

## 6. Multi-Stage Overload Protection, Analog Limiters & Tone Recognition

1. **Analog Diode Peak Clamping:** Rapid Schottky clamping diodes protect the ES8388 ADC inputs ($V_{\text{in,max}} \le 1{,}0\,\text{V}_{\text{RMS}}$).
2. **ES8388 Hardware ALC:** Integrated compressor adjusts input levels dynamically with $5\,\text{ms}$ attack and $200\,\text{ms}$ decay to $-6\,\text{dBFS}$ target.
3. **DSP Lookahead Brickwall Limiter:** Digital domain peak limiter prevents clipping above $0\,\text{dBFS}$ protecting the rider's hearing from loud backfires or sirens.

### 6.1 Voice Prompt & Confirmation Tone Recognition (Ground-Truth Verification)
To verify whether a docked OEM intercom has acknowledged switching commands (e.g. "Mesh Intercom On", "Phone Connected" or confirmation beeps):
* The DSP engine runs a low-latency **Goertzel filter tone detector** and Fourier analysis (FFT) on incoming analog channels.
* Distinctive dual-tone frequencies from Sena ($1000\,\text{Hz} / 2000\,\text{Hz}$) and Cardo beeps are verified in $< 80\,\text{ms}$.
* Status is immediately mirrored to the WebApp dashboard ("Successfully Connected") without helmet removal.

---

## 7. Harley-Davidson Boom! Box WHIM Microphone Impedance Emulation

To enable Apple CarPlay and Android Auto on Boom! Box GTS head units without purchasing the proprietary HD-WHIM module ($> 350\,\text{€}$):
* **Electrical Impedance Emulation:** OpenMotorBridge emulates the DC and AC impedance ($1{,}0 \dots 2{,}2\,\text{k}\Omega$) of an active OEM microphone across the audio transformer network.
* **Instant Activation:** Apple CarPlay unlocks on the bike's 6.5" / 12.3" infotainment screen immediately upon ignition.

---

## 8. Interactive Live Audio DSP Studio & Real-Time Testbench (`tools/audio_testbench/`)

For instant acoustic verification of the entire DSP pipeline directly in the browser (without flashing hardware), an interactive Web Audio DSP Studio is provided:

```bash
# Launches local test server and opens http://localhost:8088
python3 tools/audio_testbench/server.py
```

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│              OPENMOTORBRIDGE LIVE AUDIO DSP STUDIO & REALTIME TESTBENCH                │
├───────────────────────────────┬───────────────────────────────┬────────────────────────┤
│ 1. INPUTS & MOTORCYCLE        │ 2. REALTIME OSCILLOSCOPE & DSP│ 3. OUTPUT & SPECTRUM   │
├───────────────────────────────┼───────────────────────────────┼────────────────────────┤
│ • Physical Mic/Headset In     │ • Raised-Cosine Ducking Curve │ • Stereo FFT Spectrum  │
│ • Handlebar PTT ([SPACEBAR])  │ • 15ms Attack / 800ms Release │ • Triple VU-Meters     │
│ • Virtual Speedo (0-160 km/h) │ • Dynamic Wind Noise Gate     │ • Helmet Master Gain   │
│ • Synthwave & MP3 Drag & Drop │ • 1-Wire Hot-Swap Profiles    │ • Latency (< 10 ms)    │
└───────────────────────────────┴───────────────────────────────┴────────────────────────┘
```

### 8.1 Testbench Capabilities
1. **Live Microphone & Headset Ingestion:** Select any USB or Bluetooth headset with adjustable mic preamp gain and VAD trigger threshold.
2. **Handlebar Remote Simulation:** Screen button or holding `[SPACEBAR]` provides bounce-free PTT trigger with instant ducking.
3. **1:1 Firmware Raised-Cosine Ducking:** Evaluates the exact mathematical formulation from [`audio_dsp_pipeline.cpp`](../../firmware/main_controller/src/audio_dsp_pipeline.cpp) with zero audio artifacts.
4. **Motorcycle Speedometer & Wind Noise:**
   * $0\dots 15\,\text{km/h}$ (Traffic stop): $100\%$ ambient transparency mode.
   * $15\dots 30\,\text{km/h}$: Raised-cosine fade-out of ambient microphone.
   * $> 30\,\text{km/h}$: Noise gate engaged with dynamic aerodynamic noise generation proportional to $v^2$.
5. **1-Wire Cartridge Hot-Swap:** Simulates OEM acoustic profiles (Sena 60S EQ presence, Cardo Packtalk Pro vocal compression, OMM LoRa $300\dots 3400\,\text{Hz}$ radio bandpass, Blind plug $-96\,\text{dB}$).
