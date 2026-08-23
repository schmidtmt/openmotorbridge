# 08 - DSP Audio Engine, Raised-Cosine Ducking & Operating Modes

## 1. Core 1 Real-Time Audio Engine
Audio mixing is handled entirely on ESP32-S3 Core 1 using hardware I2S DMA buffers with an end-to-end latency of **$< 8\,\text{ms}$** at 48 kHz / 24-bit stereo.

## 2. Raised-Cosine Smooth Ducking
To prevent acoustic clicks and harsh clipping when navigation prompts or prioritized mesh calls arrive, ducking attenuation follows a smooth raised-cosine window:
$$w(t) = \frac{1}{2} \left[ 1 - \cos\left( \frac{\pi t}{T_{\text{fade}}} \right) \right]$$
- **Fade-In Time ($T_{\text{fade}}$):** 25 ms.
- **Fade-Out Time:** 150 ms.
- **Attenuation Depth:** User adjustable from $-3\,\text{dB}$ to $-24\,\text{dB}$ (default: $-12\,\text{dB}$).

## 3. Audio Operating Modes

| Mode | Name | Port 1 (Sena) | Port 2 (Cardo/PMR) | Infotainment Navi | Output Routing |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **0** | **Standard Mode** | Active (0 dB) | Active (0 dB) | Priority Ducking | Symmetrical mix to rider headset |
| **1** | **Single Rider Mode** | Active (0 dB) | Muted ($-\infty\,\text{dB}$) | Priority Ducking | Rider headset only |
| **2** | **Cruise Mode** | Active ($-6\,\text{dB}$) | Active ($-6\,\text{dB}$) | Priority Ducking | Harley-Davidson fairing speakers |

## 4. Speed-Dependent Transparency Mode & AGC Limiter

For safe awareness at traffic lights, toll gates, or slow manoeuvring up to $30\,\text{km/h}$, the DSP mixes the optional front ambient microphone (`MIC_AMBIENT_IN`) into the rider audio feed:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             DSP SPEED-GATING & OVERDRIVE PROTECTION PIPELINE                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. BANDPASS FILTER: 350 Hz - 3.2 kHz (Rejects exhaust rumble & wind noise)  │
│ 2. AGC & LIMITER: -6 dBFS Target Level, 1 ms Lookahead Brickwall Ceiling    │
│ 3. SPEED FADE: 0-15 km/h: 0 dB -> 15-30 km/h: Raised-Cosine ramp            │
│    -> > 30 km/h: Full Hardware Noise-Gate Mute (-96 dB)                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Voice Bandpass ($350\,\text{Hz} - 3.2\,\text{kHz}$):** Completely eliminates low-frequency exhaust rumble ($< 300\,\text{Hz}$) and high-frequency tyre/wind hiss ($> 3.5\,\text{kHz}$).
* **Dynamic Automatic Gain Control (AGC):** Automatically boosts quiet conversation by up to $+18\,\text{dB}$ while clamping loud horns, truck air brakes, or siren bursts within $5\,\text{ms}$ to a safe $-6\,\text{dBFS}$ level.
* **Speed-Gating Cascade:**
  * **$0 - 15\,\text{km/h}$:** $0\,\text{dB}$ (full transparency).
  * **$15 - 30\,\text{km/h}$:** Smooth raised-cosine attenuation.
  * **$> 30\,\text{km/h}$:** Absolute noise-gate isolation ($-96\,\text{dB}$ Mute).

