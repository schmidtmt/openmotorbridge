# 03 - Audio Frontend & Isolated Interfaces

## 1. Galvanic Isolation (Bourns Audio Transformers)
To completely prevent ground loops and alternator whine between the motorcycle electrical system and the satellite pods, Port 1 and Port 2 are equipped with **Bourns LM-NP-1001-B1L** 1:1 SMD audio isolation transformers:
- **Dielectric Strength:** 1500 V RMS galvanic isolation.
- **Frequency Response:** 20 Hz to 20 kHz (± 0.25 dB).
- **Impedance Matching:** 600 Ohm : 600 Ohm nominal.

## 2. Optocoupler Key Sequencing (Toshiba TLP222A)
Key presses on the intercoms (e.g. Sena Mesh Toggle or Cardo Channel Advance) are simulated using **Toshiba TLP222A** PhotoMOS solid-state relays:
- **Contact Resistance:** $R_{\text{on}} < 2\,\Omega$, bounce-free switching.
- **Switching Time:** $< 1.0\,\text{ms}$ response time.
- **Galvanic Isolation:** 1500 V RMS between MCU control line and cartridge electronics.

## 3. Acknowledgement Tone Detection (Audio Sense)
The analog output of the audio path features a precision diode peak detector connected to `PIN_ADC_LINE_LVL` (GPIO 3). When a key simulation is executed, the DSP monitors the audio return path for the characteristic beep/acknowledgement tones emitted by Sena/Cardo units to confirm successful mode changes.

## 4. External IP67 Ambient Microphone Frontend (M8 Branch on Pin 25)
- An optional IP67 miniature MEMS microphone (*Knowles SPH0645* / analog *SiSonic* with hydrophobic Gore ePTFE acoustic vent) connects via a waterproof **M8 3-Pin inline branch** at the front (cockpit / triple clamp / headlight slipstream).
- Signal path: Pin 25 (`MIC_AMBIENT_IN`) feeds directly into the Everest ES8388 Codec secondary stereo input (`LIN2`).

## 5. Multi-Stage Overdrive Protection & Hardware Limiter
To protect the rider's hearing from acoustic trauma during sudden loud traffic events (sirens, truck air brakes, emergency horns, exhaust backfires up to $120\,\text{dB SPL}$):
1. **Analogue Diode Peak Limiter:** A fast Schottky clamping diode limiter ($V_{\text{in,max}} \le 1.0\,\text{V}_{\text{RMS}}$) precedes the ES8388 `LIN2` ADC input.
2. **ES8388 Hardware ALC (Automatic Level Control):** The on-chip hardware dynamic compressor adjusts input gain automatically ($5\,\text{ms}$ attack, $200\,\text{ms}$ decay) to a safe target level of $-6\,\text{dBFS}$.
3. **DSP Lookahead Brickwall Limiter:** Core 1 executes a $1\,\text{ms}$ lookahead peak limiter with soft-knee saturation, preventing any clipping above $0\,\text{dBFS}$.

