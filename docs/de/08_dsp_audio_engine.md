# 08 - DSP Audio-Engine & Betriebsmodi

## 1. Prioritäten- & Ducking-Matrix
Der DSP-Task auf Core 1 mischt Audioquellen latenzfrei ($< 8\,\text{ms}$) über Raised-Cosine-Fadekurven:

| Priorität | Signalquelle | Ducking-Dämpfung | Attack-Zeit | Release-Zeit |
| :--- | :--- | :--- | :--- | :--- |
| **Prio 1** | Navi-Ansagen (Smartphone/Boom! Box) | $-12\,\text{dB}$ | $15\,\text{ms}$ | $800\,\text{ms}$ |
| **Prio 2** | Intercom Port 1 & 2 (Sena / Cardo) | $-8\,\text{dB}$ | $25\,\text{ms}$ | $500\,\text{ms}$ |
| **Prio 3** | Musik (A2DP Streaming) | $0\,\text{dB}$ (Hintergrund) | -- | -- |

## 2. Betriebsmodi
* **Standard Mode:** Beide Intercom-Ports aktiv, automatische Ducking-Mischung zum Fahrerhelm.
* **Single Rider Mode:** Port 2 stummgeschaltet, volle Konzentration auf Fahrerhelm und Navi.
* **Cruise Mode:** Bluetooth-Helmverbindung getrennt; Infotainment schaltet auf die Harley-Bordlautsprecher um.