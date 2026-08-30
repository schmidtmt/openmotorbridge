# 08 - DSP Audio-Engine, Raised-Cosine Ducking & Betriebsmodi

Dieses Dokument spezifiziert die interne digitale Signalverarbeitung (DSP) der **OpenMotorBridge v8.0**, die mathematische Formulierung des stetig differenzierbaren Raised-Cosine-Ducking-Algorithmus, die FreeRTOS Core 1 Audio-Pipeline sowie die geschwindigkeitsabhängigen Betriebsmodi.

---

## 1. Prioritäten- & Ducking-Matrix

Der Audio-DSP-Task läuft mit höchster Priorität auf **Core 1** des ESP32-S3 und mischt alle Signalquellen latenzarm ($t_{\text{latency}} < 8\,\text{ms}$) über stetige Überblendkurven:

| Priorität | Signalquelle | Ducking-Dämpfung | Attack-Zeit ($T_{\text{att}}$) | Hold-Zeit ($T_{\text{hold}}$) | Release-Zeit ($T_{\text{rel}}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Prio 1** | **Navigations-Ansagen** (Smartphone / Boom! Box) | **$-12\,\text{dB}$** | $15\,\text{ms}$ | $600\,\text{ms}$ | $250\,\text{ms}$ |
| **Prio 2** | **Intercom Port 1 & 2** (Sena Mesh / Cardo DMC) | **$-8\,\text{dB}$** | $25\,\text{ms}$ | $400\,\text{ms}$ | $200\,\text{ms}$ |
| **Prio 3** | **Musik-Streaming** (A2DP / Bluetooth Audio) | **$0\,\text{dB}$** (Basis) | -- | -- | -- |
| **Prio 4** | **Ambient-Mikrofon** (Transparenzmodus) | Dynamisch ($0\dots -96\,\text{dB}$) | $5\,\text{ms}$ | $100\,\text{ms}$ | $150\,\text{ms}$ |

---

## 2. Mathematische Raised-Cosine-Ducking-Synthese

Klassische lineare oder harte Audio-Fades erzeugen bei transienten Pegelsprüngen hörbare Knackgeräusche und Phasenverzerrungen. OpenMotorBridge nutzt zur Pegelüberblendung **stetig differenzierbare ($C^1$-stetige) Raised-Cosine-Funktionen**:

### 2.1 Attack-Phase (Weiches Absenken des Hintergrund-Audios):
$$g_{\text{att}}(t) = G_{\text{duck}} + (1 - G_{\text{duck}}) \cdot \frac{1}{2} \left[ 1 + \cos\left( \frac{\pi \cdot t}{T_{\text{att}}} \right) \right] \quad \text{für } 0 \le t \le T_{\text{att}}$$

### 2.2 Release-Phase (Weiche Rückkehr auf Vollpegel):
$$g_{\text{rel}}(t) = G_{\text{duck}} + (1 - G_{\text{duck}}) \cdot \frac{1}{2} \left[ 1 - \cos\left( \frac{\pi \cdot t}{T_{\text{rel}}} \right) \right] \quad \text{für } 0 \le t \le T_{\text{rel}}$$

*Hierbei ist $G_{\text{duck}} = 10^{\frac{\text{Damping [dB]}}{20}}$ (z. B. $G_{\text{duck}} = 0{,}251$ für $-12\,\text{dB}$).*

```
GAIN
1.0 ┬────────────────────────┐                              ┌────────────────────────
    │                        │ ◄─── Attack (15 ms)           │ ◄─── Release (250 ms)
    │                         \                             /
0.25┼                          \───────────────────────────/
    │                           ▲                          ▲
0.0 ┴───────────────────────────┴──────────────────────────┴─────────────────────────► ZEIT
    [ Normal: Musik 100% ]     [ Navi spricht: Hold 600ms ] [ Zurück zu 100% Musik ]
```

* **Vorteil:** Die Ableitung $\frac{\mathrm{d}g}{\mathrm{d}t}$ an den Übergangspunkten $t=0$ und $t=T$ ist exakt $0$. Dadurch treten keinerlei Phasensprünge oder Klick-Artefakte im Helm auf.

---

## 3. FreeRTOS Core 1 Audio-DMA Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    FREERTOS CORE 1 ECHTZEIT-AUDIO PIPELINE (48 kHz / 24 Bit)            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│ [ ES8388 I2S RX DMA ] ──► [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
│                                           │                                             │
│                                           ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 1. FAST PEAK DETECTOR: Erfasst Pegel & VOX-Schwellen auf LIN1/LIN2 in < 1 ms        │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2. SPEED-GATED BANDPASS: 350 Hz - 3.2 kHz Biquad IIR-Filter für Front-Mikrofon      │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 3. DUCKING MIXER: Berechnet Raised-Cosine Überblendung der aktiven Kanäle           │ │
│ ├─────────────────────────────────────────────────────────────────────────────────────┤ │
│ │ 4. LOOKAHEAD BRICKWALL LIMITER: 1 ms Soft-Knee Begrenzer (Verhindert 0 dBFS Clip)   │ │
│ └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                             │
│                                           ▼                                             │
│ [ ES8388 I2S TX DMA ] ◄── [ Double Buffer (2x 128 Samples @ 2.67 ms) ]                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Betriebsmodi des Gesamtsystems

Über den BLE-Lenkertaster oder das WebApp-Dashboard kann der Fahrer zwischen 3 Grundmodi wählen:

1. **Standard Mode (Dual-Intercom & Auto-Mix):**
   * Beide Intercom-Kanäle (Port 1 Sena & Port 2 Cardo) sind aktiv.
   * Navi-Ansagen und Smartphone-Audio werden priorisiert über beide Helme gemischt.
2. **Single Rider Mode (Solo-Fahrer Modus):**
   * Port 2 (Sozius) ist stummgeschaltet; alle DSP-Ressourcen konzentrieren sich auf den Fahrerhelm, Navi-Routing und OMM-Gruppenfunk.
3. **Cruise Mode (Bordlautsprecher-Betrieb):**
   * Trennt die Bluetooth-Helmausgabe bei Fahrzeugen mit eigenem Soundsystem (z. B. Harley-Davidson Street Glide / Road Glide / BMW RT).
   * Audio wird über den analogen Vorverstärkerausgang direkt in den Fahrzeug-Verstärker eingespeist.

---

## 5. Geschwindigkeitsabhängiger Transparenzmodus & Speed-Gating

Beim Stillstand an roten Ampeln, an Mautstellen oder beim Rangieren auf Parkplätzen bis $30\,\text{km/h}$ blendet die DSP-Engine das externe Front-Ambient-Mikrofon automatisch ein:

```
GESCHWINDIGKEIT               TRANSPARENZ-PEGEL (MIC_AMBIENT)
0 .. 15 km/h                  0 dB (Volle Durchleitung: Gespräche & Verkehr hörbar)
15 .. 30 km/h                 Raised-Cosine Fade-Out (0 dB bis -96 dB)
> 30 km/h                     -96 dB (Vollständiges Mute gegen Fahrtwindgeräusche)
```

* **Stimm-Bandpass ($350\,\text{Hz} - 3{,}2\,\text{kHz}$):** Unterdrückt dumpfes Motorbrummen ($< 300\,\text{Hz}$) sowie hochfrequentes Windrauschen ($> 3{,}5\,\text{kHz}$).
* **Hardware-AGC:** Hebt leise Sprache an Mautstellen automatisch um bis zu $+18\,\text{dB}$ an und fängt laute Signalhörner in $5\,\text{ms}$ auf sichere $-6\,\text{dBFS}$ ab.
