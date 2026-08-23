# 03 - Audio-Frontend & Symmetrische Schnittstellen

## 1. Galvanische Trennung & Symmetrierung
- Jeder analoge Intercom-Kanal (Port 1 und Port 2) ist ueber einen Bourns LM-NP-1001-B1L Audio-Uebertrager mit 1500 V RMS galvanisch isoliert.
- Verhindert Brummschleifen und hochfrequente Zuendstoerungen ueber das Massepotential des Fahrzeugs.
- Echte symmetrische Signalfuehrung (NF+ / NF-) bis in die Kassetten-Pods.

## 2. Optokoppler-Schaltung (PhotoMOS)
- Tastensimulationen erfolgen ueber prellfreie Toshiba TLP222A Halbleiter-PhotoMOS-Relais (R_ON < 1 Ohm, V_CE,sat = 0 V).
- Ein Tiefpassfilter (100 nF Keramikkondensator) und eine 5.6 V TVS-Diode am Ausgang schuetzen die Trigger-Leitung gegen Spikes und ESD.

## 3. Quittungston- & Voice-Prompt-Erkennung
Nach einem optogekoppelten Schaltpuls prueft der ADC an `ADC_LINE_LVL` innerhalb von 500 ms auf einen Audio-Burst (> -30 dBFS). Dies bestaetigt das erfolgreiche Umschalten von Kanaelen oder Betriebsmodi unabhaengig von Systemsprache oder Firmwarestand des Endgeraets.

## 4. Externer IP67 Ambient-Mikrofon-Frontend (M8-Zweig an Pin 25)
- Ein optionales IP67 Miniatur-MEMS-Mikrofon (*Knowles SPH0645* / analoges *SiSonic* mit hydrophober Gore ePTFE-Akustikmembran) wird ueber einen wasserdichten **M8 3-Pin-Kabelbaumabzweig** an der Front (Cockpit / Gabelbruecke / Scheinwerfer-Windschatten) angebunden.
- Signalpfad: Pin 25 (`MIC_AMBIENT_IN`) speist direkt den zweiten Stereo-Eingang des Everest ES8388 Codecs (`LIN2`).

## 5. Mehrstufiger Uebersteuerungsschutz & Analog-Limiter
Um das Gehoer des Fahrers bei extremen Schallereignissen im Stadtverkehr (z. B. Martinshorn, Hupen, LKW-Druckluftbremse, Auspuffknall mit bis zu $120\,\text{dB SPL}$) vor Gehoerschaeden und unertraeglichem digitalem Rechteck-Clipping zu schuetzen:
1. **Analoger Dioden-Spitzenwertbegrenzer:** Dem ES8388 ADC-Eingang `LIN2` ist ein schneller Schottky-Klemmdioden-Limiter vorgeschaltet ($V_{\text{in,max}} \le 1{,}0\,\text{V}_{\text{RMS}}$).
2. **ES8388 Hardware-ALC (Automatic Level Control):** Der integrierte Hardware-Kompressor regelt den Eingangspegel dynamisch mit einer Attack-Zeit von $5\,\text{ms}$ und Decay von $200\,\text{ms}$ auf ein sicheres Target von $-6\,\text{dBFS}$.
3. **DSP Lookahead Brickwall-Limiter:** Auf Core 1 verhindert ein $1\,\text{ms}$ Lookahead Peak Limiter mit Soft-Knee jegliches Uebersteuern ueber $0\,\text{dBFS}$.

