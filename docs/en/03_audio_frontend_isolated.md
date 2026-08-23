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
