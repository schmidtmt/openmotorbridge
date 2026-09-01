# 03 - Audio Frontend & Balanced Isolated Interfaces

This document specifies the analog signal path, galvanic isolation architecture using studio transformers, bounce-free optocoupler keying, and audio level protection in **OpenMotorBridge v8.0**.

---

## 1. Galvanic Isolation & Balanced Topology (Zero-Ground-Loop Architecture)

To eliminate ground loops, spark plug ignition spikes, and alternator whine ($1.0\dots 2.5\,\text{kHz}$) through the motorcycle chassis, both analog intercom channels (**Port 1 Rider** and **Port 2 Pillion**) are 100% galvanically isolated:

* **Isolation Transformers:** 2x **Bourns LM-NP-1001-B1L** studio audio transformers rated at $1500\,\text{V}_{\text{RMS}}$ isolation with a $1:1$ turns ratio ($600\,\Omega : 600\,\Omega$).
* **Galvanic Barrier:** A continuous $4.0\,\text{mm}$ isolation trench across all 4 copper layers separates vehicle chassis ground (`GND_PWR`) from analog audio ground (`AGND`).
* **Balanced Signal Routing:** True differential lines ($NF+$ and $NF-$) routed over twisted, shielded pairs from the HD26 harness to the respective satellite pods.

---

## 2. Galvanically Isolated Audio & Opto Frontend Schematic

```
VEHICLE / INTERCOM SIDE (PORT 1 & 2)                  ISOLATED DSP CORE SIDE
====================================                  ======================
                                         4.0 mm Moat
[ NF_IN+ ] ──┬──[ 100nF ]──┐                 │
             │             ├──( Bourns )─────┼───[ RC Low-Pass ]──► [ ES8388 ADC L1+ ]
          [ TVS 5.6V ]     │  (LM-NP-1001)   │                     (Differential
             │             ├──( 1500V RMS )──┼───[ RC Low-Pass ]──► [ ES8388 ADC L1- ]
[ NF_IN- ] ──┴──[ 100nF ]──┘                 │                      Preamplifier)
                                             │
─────────────────────────────────────────────┼─────────────────────────────────────────
                                             │
[ OPTO_P ] ──┬─────────────────┐             │
             │                 │             │
          [ TVS 5.6V ]   [ TLP222A PhotoMOS ]┼◄───[ 1 kOhm ]─────── [ ESP32-S3 GPIO ]
             │           [ R_ON < 1.0 Ohm   ]│                     (Opto-Pulse Sequencer)
[ OPTO_N ] ──┴──[ 100nF ]──────┘             │
                                             │
[ AGND_POD ] ────────────────────────────────┴───────────────────── [ GND_DIGITAL ]
```

---

## 3. Technical Parameters & Audio Performance

| Parameter | Specification | Test Condition / Standard | Performance in Riding Conditions |
| :--- | :---: | :--- | :--- |
| **Isolation Voltage** | **$1500\,\text{V}_{\text{RMS}}$** | 60 s @ $50\,\text{Hz}$ (Bourns LM-NP-1001) | Full protection against ignition spikes |
| **Common Mode Rejection (CMRR)**| **$> 85\,\text{dB}$** | $f = 1.2\,\text{kHz}$ (Alternator ripple) | Completely eliminates RPM engine whine |
| **Total Harmonic Distortion (THD+N)**| **$< 0.02\,\%$** | $1\,\text{kHz}, 1.0\,\text{V}_{\text{RMS}}$ @ $600\,\Omega$ | Crystal-clear, uncompressed speech |
| **Frequency Response** | **$20\,\text{Hz} - 20\,\text{kHz} \pm 0.5\,\text{dB}$** | HiFi Studio Standard | Lossless music sharing & navigation |
| **Signal-to-Noise Ratio (SNR)**| **$> 88\,\text{dB}$** | A-weighted, $1\,\text{V}_{\text{RMS}}$ reference | Dead-silent standby without hiss |
| **Crosstalk Rejection** | **$> 92\,\text{dB}$** | $1\,\text{kHz}$ between Port 1 and Port 2 | Zero voice ghosting between rider/pillion |

---

## 4. Optocoupler Keying & Bounce-Free Button Simulation (PhotoMOS)

To control Sena, Cardo, or Midland intercom units inside the cartridge automatically (e.g., Mesh On/Off, Channel Next, PTT trigger):

1. **Solid-State PhotoMOS Relays:** Uses the **Toshiba TLP222A** with an optically isolated MOSFET output.
   * **Advantage over mechanical relays:** Zero contact bounce ($t_{\text{bounce}} = 0\,\mu\text{s}$), infinite switching lifespan, immune to vibration, hermetically sealed.
   * **On-Resistance:** $R_{\text{ON}} < 1.0\,\Omega$ with saturation voltage $V_{\text{CE,sat}} \approx 0\,\text{V}$ (equivalent to an ideal mechanical contact).
2. **Protection Circuit:**
   * An ultra-fast $5.6\,\text{V}$ TVS diode on the output protects against ESD during cartridge insertion.
   * A $100\,\text{nF}$ ceramic capacitor filters RF noise from nearby 2.4 GHz antennas.

---

## 5. Voice Prompt & Beep Detection (Ground-Truth Verification)

After triggering a pulse (e.g., double-click for "Mesh Channel Next"), the firmware verifies execution in hardware:

* **Signal Path:** The audio ADC monitors `ADC_LINE_LVL` within a $500\,\text{ms}$ time window.
* **Detection Threshold:** If the level exceeds $-30\,\text{dBFS}$ (confirmation beep or voice prompt *"Channel 2"*), the action is marked as confirmed.
* **Benefit:** 100% autonomous, language-agnostic verification without requiring proprietary Bluetooth API licensing.

---

## 6. External IP67 Ambient Microphone Frontend (M8 Branch at Pin 25)

An optional IP67 miniature MEMS microphone (*Knowles SPH0645* / analog *SiSonic* with hydrophobic Gore ePTFE acoustic membrane) connects via the **M8 4-pin front branch** at Pin 25 (`MIC_AMBIENT_IN`) in the cockpit:

* **Purpose:** Captures environmental acoustics (transparency mode at traffic lights, toll gates, sirens).
* **Phantom Power:** The main board provides a low-noise $+3.3\,\text{V}$ microphone bias (`+3V3_MIC_BIAS`) via a $2.2\,\text{k}\Omega$ metal-film pull-up.

---

## 7. Multi-Stage Overload Protection & Analog Limiter

To protect rider hearing during extreme acoustic events (sirens, horns in tunnels, truck air brakes up to $120\,\text{dB SPL}$):

1. **Analog Diode Peak Clamping:** Fast Schottky clamp diodes at the ES8388 `LIN2` input limit voltage ($V_{\text{in,max}} \le 1.0\,\text{V}_{\text{RMS}}$).
2. **ES8388 Hardware ALC (Automatic Level Control):** Dynamic compression with $5\,\text{ms}$ attack and $200\,\text{ms}$ decay to a safe $-6\,\text{dBFS}$ target.
3. **DSP Lookahead Brickwall Limiter:** A $1\,\text{ms}$ soft-knee lookahead limiter on Core 1 guarantees zero clipping above $0\,\text{dBFS}$.

---

## 8. Harley-Davidson Boom! Box GTS WHIM Microphone Impedance Emulation

To unlock Apple CarPlay on the Boom! Box GTS infotainment system without purchasing the proprietary HD-WHIM module ($> \$350$):

### 8.1 OEM Microphone Detection Mechanism
During boot, the Boom! Box GTS samples its 7-pin audio connector (or internal WHIM harness) for an active voice microphone:
1. **DC Bias Check:** The head unit applies a DC bias voltage ($V_{\text{MIC\_BIAS}} \approx 8 \dots 10\,\text{V}$) via an internal pull-up resistor.
2. **Impedance Measurement:** If open-circuit (no headset plugged in), CarPlay startup is blocked with *"No headset connected"*.
3. **Detection Window:** An active headset is verified when load impedance falls within $1.0 \dots 2.2\,\text{k}\Omega$ and audio feedback is measurable.

### 8.2 Circuit Implementation in OpenMotorBridge
* **Isolated Impedance Matching:** The primary side of the Bourns LM-NP-1001 transformer is coupled to the Boom! Box microphone pin via an RC network ($R_{\text{BIAS}} = 1.5\,\text{k}\Omega$ metal film $1\%$, $C = 10\,\mu\text{F}$ tantalum).
* **Signal Pass-Through:** Outgoing speech (rider headset via Sena/Cardo or front ambient mic) is cleanly modulated into the Boom! Box microphone input, enabling Siri voice navigation and voice commands at highway speeds.
* **Advantage:** The Boom! Box continuously detects a legitimate OEM headset. Apple CarPlay starts immediately upon ignition without requiring manual jumper plugs or fragile DIY resistors.
