# 08 - DSP Audio-Engine & Betriebsmodi

## 1. Prioritaeten- & Ducking-Matrix
Der DSP-Task auf Core 1 mischt Audioquellen latenzfrei (< 8 ms) ueber Raised-Cosine-Fadekurven:

| Prioritaet | Signalquelle | Ducking-Daempfung | Attack-Zeit | Release-Zeit |
| :--- | :--- | :--- | :--- | :--- |
| **Prio 1** | Navi-Ansagen (Smartphone/Boom! Box) | -12 dB | 15 ms | 800 ms |
| **Prio 2** | Intercom Port 1 & 2 (Sena / Cardo) | -8 dB | 25 ms | 500 ms |
| **Prio 3** | Musik (A2DP Streaming) | 0 dB (Hintergrund) | -- | -- |

## 2. Betriebsmodi
- **Standard Mode:** Beide Intercom-Ports aktiv, automatische Ducking-Mischung zum Fahrerhelm.
- **Single Rider Mode:** Port 2 stummgeschaltet, volle Konzentration auf Fahrerhelm und Navi.
- **Cruise Mode:** Bluetooth-Helmverbindung getrennt; Infotainment schaltet auf die Harley-Bordlautsprecher um.

## 3. Geschwindigkeitsabhaengiger Transparenzmodus & AGC-Limiter

Fuer sicheres Stehen an Ampeln, Mautstellen oder Rangieren bis $30\,\text{km/h}$ mischt der DSP das optionale Front-Ambient-Mikrofon (`MIC_AMBIENT_IN`) in den Fahrer-Audio-Feed:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             DSP SPEED-GATING & UEBERSTEUERUNGSSCHUTZ-PIPELINE               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. BANDPASS-FILTER: 350 Hz - 3.2 kHz (Unterdrueckt Auspuff- & Windzischen)  │
│ 2. AGC & LIMITER: -6 dBFS Target Level, 1 ms Lookahead Brickwall Ceiling    │
│ 3. GESCHWINDIGKEITS-FADE: 0-15 km/h: 0 dB -> 15-30 km/h: Raised-Cosine      │
│    -> > 30 km/h: Vollstaendiges Noise-Gate Mute (-96 dB)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Sprach-Bandpass ($350\,\text{Hz} - 3{,}2\,\text{kHz}$):** Filtert tieffrequentes Motor- und Auspuffblubbern ($< 300\,\text{Hz}$) sowie hochfrequentes Wind- und Reifenzischen ($> 3{,}5\,\text{kHz}$) vollstaendig heraus.
* **Dynamische AGC-Pegelregelung:** Regelt leise Sprache automatisch um bis zu $+18\,\text{dB}$ hoch und bremst laute Hupen oder LKW-Druckluftbremsen in $5\,\text{ms}$ auf sichere $-6\,\text{dBFS}$ herunter.
* **Speed-Gating:**
  * **$0 - 15\,\text{km/h}$:** $0\,\text{dB}$ (volle Transparenz).
  * **$15 - 30\,\text{km/h}$:** Stetiges Raised-Cosine Ausblenden.
  * **$> 30\,\text{km/h}$:** Hardware-Stummschaltung ($-96\,\text{dB}$ Mute).

