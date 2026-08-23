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
