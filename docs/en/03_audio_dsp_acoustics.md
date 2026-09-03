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

## 4. Click-Free Raised-Cosine Audio Ducking

Standard threshold-based ducking causes abrupt volume jumps and audible clicks. OpenMotorBridge employs a mathematically continuous **Raised-Cosine Ducking Curve**:

$$g(t) = \begin{cases} 1{,}0 & \text{for } t < 0 \\ g_{\min} + \frac{1 - g_{\min}}{2} \left[1 + \cos\left(\frac{\pi \cdot t}{T_{\text{attack}}}\right)\right] & \text{for } 0 \le t \le T_{\text{attack}} \\ g_{\min} & \text{during voice prompt} \end{cases}$$

* **Attack Time ($T_{\text{attack}}$):** $15\,\text{ms}$ smooth descent (inaudible transition).
* **Hold Time ($T_{\text{hold}}$):** $600\,\text{ms}$ retention to prevent pumping between words.
* **Release Time ($T_{\text{release}}$):** $250\,\text{ms}$ smooth raised-cosine return.

---

## 5. Interactive Live Audio DSP Studio & Real-Time Testbench (`tools/audio_testbench/`)

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

### 5.1 Testbench Capabilities
1. **Live Microphone & Headset Ingestion:** Select any USB or Bluetooth headset with adjustable mic preamp gain and VAD trigger threshold.
2. **Handlebar Remote Simulation:** Screen button or holding `[SPACEBAR]` provides bounce-free PTT trigger with instant ducking.
3. **1:1 Firmware Raised-Cosine Ducking:** Evaluates the exact mathematical formulation from [`audio_dsp_pipeline.cpp`](../../firmware/main_controller/src/audio_dsp_pipeline.cpp) with zero audio artifacts.
4. **Motorcycle Speedometer & Wind Noise:**
   * $0\dots 15\,\text{km/h}$ (Traffic stop): $100\%$ ambient transparency mode.
   * $15\dots 30\,\text{km/h}$: Raised-cosine fade-out of ambient microphone.
   * $> 30\,\text{km/h}$: Noise gate engaged with dynamic aerodynamic noise generation proportional to $v^2$.
5. **1-Wire Cartridge Hot-Swap:** Simulates OEM acoustic profiles (Sena 60S EQ presence, Cardo Packtalk Pro vocal compression, OMM LoRa $300\dots 3400\,\text{Hz}$ radio bandpass, Blind plug $-96\,\text{dB}$).
