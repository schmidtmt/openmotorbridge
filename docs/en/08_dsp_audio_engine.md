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
