# OpenMotorBridge - Live Audio DSP Studio & Real-Time Testbench

Standalone, zero-dependency interactive acoustic emulator and real-time DSP workbench for the OpenMotorBridge motorcycle intercom system.

Runs completely independently from the production PWA (`webapp_pwa/`) and implements the exact algorithms from [`firmware/main_controller/src/audio_dsp_pipeline.cpp`](../../firmware/main_controller/src/audio_dsp_pipeline.cpp).

---

## Quickstart

Launch the testbench server:

```bash
python3 tools/audio_testbench/server.py
```

This automatically opens `http://localhost:8088` in your default browser.

---

## Features

1. **Live Microphone & Headset Ingestion:**
   * Select any connected USB or Bluetooth headset / microphone.
   * Adjustable Mic Gain and real-time Voice Activity Detection (VAD) threshold.
   * Physical Push-to-Talk (PTT) button or hold `[SPACEBAR]` as handlebar remote.

2. **Music Playback & Media Streaming:**
   * Built-in rhythmic Riding-Synthwave generator (works with 0 external files).
   * Drag & drop your own MP3 / WAV / FLAC / M4A files directly into the browser.
   * Play YouTube Music in another tab or play music locally.

3. **1:1 Firmware Raised-Cosine Audio Ducking:**
   * Automatically drops music volume smoothly by **-12 dB** (configurable -6 to -96 dB) with **15 ms attack**.
   * Fades music back to 100% over **800 ms release** once speech or PTT stops.
   * Real-time oscilloscope tracking the gain reduction envelope.

4. **Motorcycle Speedometer (0 - 160 km/h):**
   * **0 to 15 km/h (Traffic Light):** 100% Ambient Transparency active.
   * **15 to 30 km/h:** Raised-cosine crossfade out.
   * **> 30 km/h:** Ambient mic gated out to suppress helmet wind noise.
   * Dynamic aerodynamic pink noise generation proportional to $v^2$.

5. **1-Wire Cartridge Hot-Swap Emulation:**
   * **Sena 60S:** +2.5 dB Preamp Gain, 2.8 kHz presence EQ peak.
   * **Cardo Packtalk Pro:** Natural voice compression, 120 Hz low-cut.
   * **OMM LoRa Transceiver (Rear Pod 3):** 300 - 3400 Hz telecommunication bandpass filter with slight radio warmth (Opus 24k / LoRa speech simulation).
   * **Blindkassette:** Complete slot mute (-96 dB).

6. **Visual Telemetry:**
   * Stereo FFT Spectrum Analyzer.
   * Triple VU meters (Mic In, Music In, Helmet Master Out).
   * Latency counter (< 10 ms on modern macOS Web Audio).
