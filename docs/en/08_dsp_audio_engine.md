# 08 - DSP Audio Engine, Raised-Cosine Ducking & Operating Modes

This document specifies the digital signal processing (DSP) pipeline of **OpenMotorBridge v8.0**, the mathematical formulation of continuously differentiable Raised-Cosine ducking, the FreeRTOS Core 1 audio DMA pipeline, and speed-gated operating modes.

---

## 1. Priority & Ducking Matrix

The audio DSP task executes with highest priority on **Core 1** of the ESP32-S3, mixing all audio channels with ultra-low latency ($t_{\text{latency}} < 8\,\text{ms}$) via smooth crossfade curves:

| Priority | Audio Source | Ducking Attenuation | Attack Time ($T_{\text{att}}$) | Hold Time ($T_{\text{hold}}$) | Release Time ($T_{\text{rel}}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Prio 1** | **Navigation Prompts** (Smartphone / Boom! Box) | **$-12\,\text{dB}$** | $15\,\text{ms}$ | $600\,\text{ms}$ | $250\,\text{ms}$ |
| **Prio 2** | **Intercom Port 1 & 2** (Sena Mesh / Cardo DMC) | **$-8\,\text{dB}$** | $25\,\text{ms}$ | $400\,\text{ms}$ | $200\,\text{ms}$ |
| **Prio 3** | **Music Streaming** (A2DP / Bluetooth Audio) | **$0\,\text{dB}$** (Base) | -- | -- | -- |
| **Prio 4** | **Ambient Mic** (Transparency Mode) | Dynamic ($0\dots -96\,\text{dB}$) | $5\,\text{ms}$ | $100\,\text{ms}$ | $150\,\text{ms}$ |

---

## 2. Mathematical Raised-Cosine Ducking Synthesis

Standard linear or step-wise fades create audible pops and phase discontinuities during sudden volume changes. OpenMotorBridge utilizes **continuously differentiable ($C^1$-smooth) Raised-Cosine blending**:

### 2.1 Attack Phase (Smooth Background Ducking):
$$g_{\text{att}}(t) = G_{\text{duck}} + (1 - G_{\text{duck}}) \cdot \frac{1}{2} \left[ 1 + \cos\left( \frac{\pi \cdot t}{T_{\text{att}}} \right) \right] \quad \text{for } 0 \le t \le T_{\text{att}}$$

### 2.2 Release Phase (Smooth Return to Full Gain):
$$g_{\text{rel}}(t) = G_{\text{duck}} + (1 - G_{\text{duck}}) \cdot \frac{1}{2} \left[ 1 - \cos\left( \frac{\pi \cdot t}{T_{\text{rel}}} \right) \right] \quad \text{for } 0 \le t \le T_{\text{rel}}$$

*Where $G_{\text{duck}} = 10^{\frac{\text{Damping [dB]}}{20}}$ (e.g., $G_{\text{duck}} = 0.251$ for $-12\,\text{dB}$).*

```
GAIN
1.0 ┬────────────────────────┐                              ┌────────────────────────
    │                        │ ◄─── Attack (15 ms)           │ ◄─── Release (250 ms)
    │                         \                             /
0.25┼                          \───────────────────────────/
    │                           ▲                          ▲
0.0 ┴───────────────────────────┴──────────────────────────┴─────────────────────────► TIME
    [ Normal: Music 100% ]     [ Nav Active: Hold 600ms ]  [ Return to 100% Music ]
```

* **Advantage:** The derivative $\frac{\mathrm{d}g}{\mathrm{d}t}$ at transition points $t=0$ and $t=T$ is precisely $0$, eliminating clicking artifacts and phase jumps in the helmet.

---

## 3. FreeRTOS Core 1 Audio DMA Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    FREERTOS CORE 1 REAL-TIME AUDIO PIPELINE (48 kHz / 24 Bit)           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│ [ ES8388 I2S RX DMA ] ──► [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
│                                           │                                             │
│                                           ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. FAST PEAK DETECTOR: Captures levels & VOX gates on LIN1/LIN2 in < 1 ms           │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. SPEED-GATED BANDPASS: 350 Hz - 3.2 kHz Biquad IIR filter for front mic           │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. DUCKING MIXER: Computes Raised-Cosine gain transitions on active channels        │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4. LOOKAHEAD BRICKWALL LIMITER: 1 ms soft-knee ceiling (prevents 0 dBFS clipping)   │ │
│ └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                             │
│                                           ▼                                             │
│ [ ES8388 I2S TX DMA ] ◄── [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. System Operating Modes

The rider can select between 3 primary modes via the handlebar remote or PWA dashboard:

1. **Standard Mode (Dual-Intercom & Auto-Mix):**
   * Both intercom channels (Port 1 Sena & Port 2 Cardo) are active.
   * Navigation prompts and media are blended automatically across both helmets.
2. **Single Rider Mode (Solo Focus):**
   * Port 2 (Pillion) is muted; all DSP horsepower focuses on the rider helmet, GPS routing, and OMM mesh.
3. **Cruise Mode (Chassis Speaker Output):**
   * Disconnects helmet audio for motorcycles equipped with fairing speakers (e.g., Harley-Davidson Street/Road Glide, BMW RT).
   * Audio is routed through the analog pre-amp output into the motorcycle's onboard amplifier.

---

## 5. Speed-Gated Transparency Mode

At stoplights, toll booths, or parking speeds up to $30\,\text{km/h}$, the DSP automatically injects ambient microphone audio into the rider's feed:

```
VEHICLE SPEED                 TRANSPARENCY GAIN (MIC_AMBIENT)
0 .. 15 km/h                  0 dB (Full pass-through: Conversations & traffic audible)
15 .. 30 km/h                 Raised-Cosine Fade-Out (0 dB to -96 dB)
> 30 km/h                     -96 dB (Complete mute against wind noise)
```

* **Vocal Bandpass ($350\,\text{Hz} - 3.2\,\text{kHz}$):** Rejects low engine rumble ($< 300\,\text{Hz}$) and high-frequency wind buffeting ($> 3.5\,\text{kHz}$).
* **Hardware AGC:** Boosts quiet speech at toll gates by up to $+18\,\text{dB}$ and compresses loud horns within $5\,\text{ms}$ down to $-6\,\text{dBFS}$.
