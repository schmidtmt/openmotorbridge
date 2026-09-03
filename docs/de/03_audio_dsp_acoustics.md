# 03 - Audio-DSP, Akustik & Knowles MEMS Fahrtwind-Kompensation

Dieses Dokument spezifiziert die analoge Signalverarbeitung, die galvanische Trennarchitektur mit Studio-Übertragern, die FreeRTOS Core 1 DSP-Pipeline mit stetig differenzierbarem Raised-Cosine-Ducking sowie die dynamische **Helm-Lautstärkenachführung (AGC)** auf Basis des digitalen Knowles MEMS Fahrtwind-Akustiksensors am Front-Knoten.

---

## 1. Galvanische Trennung & Symmetrierung (Zero-Ground-Loop Topologie)

Um Masseschleifen, Zündfunk-Einstreuungen und hochfrequentes Lichtmaschinenpfeifen ($1{,}0\dots 2{,}5\,\text{kHz}$) über das Fahrzeugchassis zu $100\,\%$ zu unterbinden, sind beide analogen Intercom-Kanäle (**Port 1 Fahrer** und **Port 2 Sozius**) galvanisch vollständig isoliert:

* **Trennübertrager:** 2x **Bourns LM-NP-1001-B1L** Studio-Audio-Transformatoren mit $1500\,\text{V}_{\text{RMS}}$ Isolationsspannung und $1:1$ Übersetzungsverhältnis ($600\,\Omega : 600\,\Omega$).
* **Galvanische Barriere:** Ein durchgehender $4{,}0\,\text{mm}$ Isolationsgraben auf allen 4 Kupferlagen trennt die Fahrzeugmasse (`GND_PWR`) von der analogen Audiomasse (`AGND`).
* **Symmetrische Signalführung:** Echte differenzielle Signalführung ($NF+$ und $NF-$) über verdrillte, geschirmte Adernpaare vom HD26-Kabelbaum bis in die jeweiligen Kassetten-Pods.

```
FAHRZEUGSEITE / INTERCOM (PORT 1 & 2)                  ISOLIERTE DSP-SEITE (MAIN CORE)
=====================================                  ===============================
                                         4.0 mm Graben
[ NF_IN+ ] ──┬──[ 100nF ]──┐                 │
             │             ├──( Bourns )─────┼───[ RC-Tiefpass ]──► [ ES8388 ADC L1+ ]
          [ TVS 5.6V ]     │  (LM-NP-1001)   │                     (Differenzieller
             │             ├──( 1500V RMS )──┼───[ RC-Tiefpass ]──► [ ES8388 ADC L1- ]
[ NF_IN- ] ──┴──[ 100nF ]──┘                 │                      Eingangsverstärker)
                                             │
─────────────────────────────────────────────┼─────────────────────────────────────────
                                             │
[ OPTO_P ] ──┬─────────────────┐             │
             │                 │             │
          [ TVS 5.6V ]   [ TLP222A PhotoMOS ]┼◄───[ 1 kOhm ]─────── [ ESP32-S3 GPIO ]
             │           [ R_ON < 1.0 Ohm   ]│                     (Opto-Puls Sequenzer)
[ OPTO_N ] ──┴──[ 100nF ]──────┘             │
                                             │
[ AGND_POD ] ────────────────────────────────┴───────────────────── [ GND_DIGITAL ]
```

### 1.1 Technische Kennwerte & Audio-Performance

| Parameter | Spezifikationswert | Messbedingung / Standard | Bedeutung im Fahrbetrieb |
| :--- | :---: | :--- | :--- |
| **Isolationsspannung** | **$1500\,\text{V}_{\text{RMS}}$** | 60 s @ $50\,\text{Hz}$ (Bourns LM-NP-1001) | Schutz gegen Hochspannungs-Zündspitzen |
| **Gleichtaktunterdrückung (CMRR)**| **$> 85\,\text{dB}$** | $f = 1{,}2\,\text{kHz}$ (Lichtmaschinen-Rippel) | Eliminiert Drehzahl-Pfeifen vollständig |
| **Klirrfaktor (THD+N)** | **$< 0{,}02\,\%$** | $1\,\text{kHz}, 1{,}0\,\text{V}_{\text{RMS}}$ an $600\,\Omega$ | Glasklare, unverzerrte Sprachwiedergabe |
| **Frequenzgang** | **$20\,\text{Hz} - 20\,\text{kHz} \pm 0{,}5\,\text{dB}$** | HiFi-Audiowiedergabe | Verlustfreies Musik-Sharing & Navi-Audio |
| **Signal-Rausch-Abstand (SNR)**| **$> 88\,\text{dB}$** | A-gewichtet, $1\,\text{V}_{\text{RMS}}$ Referenz | Rauschfreier Standby ohne Zischen im Helm |
| **Übersprechdämpfung (Channel Sep.)**| **$> 92\,\text{dB}$** | $1\,\text{kHz}$ zwischen Port 1 und Port 2 | Keine gegenseitigen Audio-Geisterstimmen |

---

## 2. Mathematische Raised-Cosine-Ducking-Synthese

Klassische lineare Fades erzeugen bei transienten Pegelsprüngen hörbare Klickgeräusche. OpenMotorBridge nutzt **stetig differenzierbare ($C^1$-stetige) Raised-Cosine-Funktionen**:

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

### 2.2 Prioritäten- & Ducking-Matrix

| Priorität | Signalquelle | Ducking-Dämpfung | Attack ($T_{\text{att}}$) | Hold ($T_{\text{hold}}$) | Release ($T_{\text{rel}}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Prio 1** | **Radar-Ping / Notruf** | **$-18\,\text{dB}$** | $5\,\text{ms}$ | $800\,\text{ms}$ | $200\,\text{ms}$ |
| **Prio 2** | **Navigations-Ansagen** (Smartphone / GPS) | **$-12\,\text{dB}$** | $15\,\text{ms}$ | $600\,\text{ms}$ | $250\,\text{ms}$ |
| **Prio 3** | **Intercom Port 1 & 2** (Sena / Cardo) | **$-8\,\text{dB}$** | $25\,\text{ms}$ | $400\,\text{ms}$ | $200\,\text{ms}$ |
| **Prio 4** | **Musik-Streaming** (Bluetooth A2DP) | **$0\,\text{dB}$** (Basis) | -- | -- | -- |

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
│ │ 2. AGC GAIN-STAGE: Wendet Knowles MEMS Fahrtwind-Lautstärkeanhebung an               │ │
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

### 3.1 ES8388 Low-Level Registerkonfiguration & I2S DMA-Architektur
* **Taktraten & Master-Clock:**
  * Abtastrate $F_s = 48{,}0\,\text{kHz}$ (24-Bit Stereo).
  * Master Clock: $MCLK = 256 \times F_s = 12{,}288\,\text{MHz}$ (generiert über ESP32-S3 Audio-PLL auf GPIO 0).
  * Bit Clock: $BCLK = 64 \times F_s = 3{,}072\,\text{MHz}$ (32-Bit Frame-Slot für präzise 24-Bit Wortbreite).
  * Left/Right Word Clock: $LRCK = F_s = 48{,}0\,\text{kHz}$.
* **DMA-Pufferstruktur:**
  * 4 verkettete DMA-Deskriptoren mit je 128 Stereo-Samples ($2{,}67\,\text{ms}$ Blockzeit).
  * Gesamte Audio-Latenz (ADC $\rightarrow$ FreeRTOS DSP $\rightarrow$ DAC): **$7{,}85\,\text{ms}$** (unterhalb der Wahrnehmungsschwelle von $15\,\text{ms}$).
* **Hardware-ALC Register-Set (`Reg 0x12 - 0x17`):**
  * Target Level: $-6\,\text{dBFS}$, Max Gain: $+24\,\text{dB}$, Min Gain: $-12\,\text{dB}$.
  * Attack Time: $5\,\text{ms}$, Decay Time: $200\,\text{ms}$, Noise Gate Threshold: $-54\,\text{dBFS}$.

---

## 4. Digitaler Knowles MEMS Akustiksensor & AGC Fahrtwind-Kompensation

Zur automatischen Anpassung der Helm-Lautstärke an turbulente Windgeräusche bei steigender Fahrgeschwindigkeit sitzt auf dem Front-Knoten ein digitales I2S-MEMS-Mikrofon (**Knowles SPH0645LM4H**):

```
                       AKUSTIK-PFAD (FRONT-KNOTEN -> HELM)
┌────────────────────────────┐              ┌────────────────────────────┐
│ Knowles SPH0645 MEMS       │              │ ESP32-C3 Front Controller  │
│ • Hydrophobe ePTFE-Membran │ I2S DMA Bus  │ • Biquad A-Weighting nach  │
│ • 65.4 dB SNR, 120 dBA AOP ├─────────────►│   IEC 61672-1 Class 1      │
│ • Integrierter 24-Bit ADC  │              │ • 50 Hz RMS-Schallpegel dBA│
└────────────────────────────┘              └─────────────┬──────────────┘
                                                          │ ESP-NOW (0.9 ms)
                                                          ▼
┌────────────────────────────┐              ┌────────────────────────────┐
│ Helm-Lautsprecher          │ I2S TX DMA   │ ESP32-S3 Hauptcontroller   │
│ • Gehörschutz-begrenzt     │◄─────────────┤ • Raised-Cosine AGC-Gain   │
│ • Automatisch laut/leise   │              │ • Schwellwert: 70 dBA      │
└────────────────────────────┘              └────────────────────────────┘
```

### 4.1 Digitalfilterung: Biquad A-Weighting nach IEC 61672-1
Um unhörbare niederfrequente Luftdruckschwankungen (Wirbelschleppen von LKWs, $10\dots 40\,\text{Hz}$) nicht als Lärm fehlzuinterpretieren, filtert der ESP32-C3 das Audiosignal in Echtzeit mit einem biquadratischen IIR-Filter:
* **Dämpfung bei $100\,\text{Hz}$:** $-19{,}1\,\text{dB}$ (korrespondierend zur menschlichen Hörempfindlichkeit).
* **Durchlassbereich bei $1\dots 4\,\text{kHz}$:** $0{,}0\,\text{dB}$ (Sprachrelevanter Bereich).

### 4.2 Geschwindigkeits- & Lärm-Kennlinie der Lautstärkenachführung (AGC)

```
FAHRWIND-PEGEL          FAHRGESCHWINDIGKEIT    AGC LAUTSTÄRKE-BOOST    AKUSTIK-STATUS
< 70 dB(A)              0 .. 50 km/h           +0.0 dB                 Normalbetrieb / Transparenz
70 .. 80 dB(A)          50 .. 90 km/h          +1.0 .. +2.0 dB         Leichte Anhebung
80 .. 95 dB(A)          90 .. 140 km/h         +2.0 .. +4.5 dB         Autobahn-Kompensation
> 95 dB(A)              > 140 km/h             +5.0 .. +6.0 dB (Max)   Volle Sprachverständlichkeit
```

* **Transparenzmodus bei Stillstand ($0\dots 15\,\text{km/h}$):** An roten Ampeln und beim Rangieren wird der Schall über einen Sprach-Bandpass ($350\,\text{Hz} - 3{,}2\,\text{kHz}$) dezent in den Helm eingeblendet, sodass Verkehrsgeräusche und Durchsagen ohne Absetzen des Helms klar verständlich sind.

### 4.3 Die 4 Betriebsmodi des Gesamtsystems
1. **Modus 1 (Touring-Duo):** Fahrer und Sozius hören sich gegenseitig mit vollem Duplex. Navi blendet sich mit $-12\,\text{dB}$ Ducking ein. Musik wird bei Intercom-Aktivität auf $-15\,\text{dB}$ gesenkt.
2. **Modus 2 (Highway-Solo):** Fahrer fährt allein. Pod 2 ist stromlos (`disabled.json`). Voller DSP-Fokus auf Telefonie, CarPlay/Android Auto und Radar-Akustik.
3. **Modus 3 (Group-Mesh Bridge):** Pod 1 (Sena) und Pod 2 (Cardo) sind parallel aktiv. Cross-Mix verbindet beide Gruppen in Echtzeit.
4. **Modus 4 (Emergency-Override):** LoRa-Notruffunk oder Radar-Kollisionsalarm (TTC < 3.5s) schalten alle anderen Audioquellen sofort auf $-24\,\text{dB}$ stumm und injizieren den Notruf bzw. Alarm-Doppelton mit maximalem Headroom.

---

## 5. Mehrstufiger Übersteuerungsschutz, Analog-Limiter & Signalerfassung

1. **Analoger Dioden-Spitzenwertbegrenzer:** Dem ES8388 ADC-Eingang ist ein schneller Schottky-Klemmdioden-Limiter vorgeschaltet ($V_{\text{in,max}} \le 1{,}0\,\text{V}_{\text{RMS}}$).
2. **ES8388 Hardware-ALC:** Der integrierte Hardware-Kompressor regelt den Eingangspegel dynamisch mit einer Attack-Zeit von $5\,\text{ms}$ und Decay von $200\,\text{ms}$ auf ein sicheres Target von $-6\,\text{dBFS}$.
3. **DSP Lookahead Brickwall-Limiter:** Verhindert im digitalen Bereich jegliches Übersteuern über $0\,\text{dBFS}$, um das Gehör des Fahrers vor Spitzenpegeln (Martinshorn, Auspuffknallen) zu schützen.

### 5.1 Quittungston- & Voice-Prompt-Erkennung (Ground-Truth Verifikation)
Um zu überprüfen, ob ein angebundenes OEM-Headset Schaltbefehle tatsächlich angenommen hat (z. B. "Mesh Intercom On", "Phone Connected" oder Bestätigungstöne):
* Die DSP-Engine führt an den analogen Eingangskanälen eine latenzarme **Goertzel-Filter-Tonerkennung** und Fourier-Analyse (FFT) durch.
* Charakteristische Dual-Tone-Frequenzen von Sena ($1000\,\text{Hz} / 2000\,\text{Hz}$) und Cardo Beeps werden in $< 80\,\text{ms}$ verifiziert.
* Das Ergebnis wird via BLE an das WebApp-Dashboard gemeldet ("Erfolgreich gekoppelt"), ohne dass der Fahrer den Helm abnehmen muss.

---

## 6. Harley-Davidson Boom! Box WHIM-Mikrofon-Impedanz-Emulation

Zur Freischaltung von Apple CarPlay in der Boom! Box GTS Infotainment-Headunit ohne das proprietäre HD-WHIM-Modul ($> 350\,\text{€}$):
* **Elektrische Impedanz-Emulation:** OpenMotorBridge emuliert über ein präzises Widerstands- und Übertragernetzwerk an den Audio-Schnittstellen die Gleich- und Wechselstrom-Impedanz ($1{,}0 \dots 2{,}2\,\text{k}\Omega$) eines aktiven OEM-Mikrofons.
* **Ergebnis:** Apple CarPlay und Android Auto werden im Fahrzeugdisplay sofort freigeschaltet.

---

## 7. Interaktives Live Audio DSP Studio & Echtzeit-Simulator (`tools/audio_testbench/`)

Für die sofortige akustische Verifikation der gesamten DSP-Pipeline im Browser (ohne geflashte Hardware) steht das autarke Web Audio DSP Studio zur Verfügung:

```bash
# Startet den lokalen HTTP-Server und öffnet http://localhost:8088
python3 tools/audio_testbench/server.py
```

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               OPENMOTORBRIDGE LIVE AUDIO DSP STUDIO & ECHTZEIT-SIMULATOR               │
├───────────────────────────────┬───────────────────────────────┬────────────────────────┤
│ 1. EINGABEN & FAHRZEUG        │ 2. ECHTZEIT-OSZILLOSKOP & DSP │ 3. OUTPUT & SPEKTRUM   │
├───────────────────────────────┼───────────────────────────────┼────────────────────────┤
│ • Reales Mikrofon/Headset     │ • Raised-Cosine Ducking Kurve │ • Stereo FFT Spektrum  │
│ • Lenker-PTT Taste ([SPACE])  │ • 15ms Attack / 800ms Release │ • Triple VU-Meter      │
│ • Virtueller Tacho (0-160km/h)│ • AGC Windgeräusch-Gate       │ • Helm-Master-Pegel    │
│ • Synthwave & MP3 Drag&Drop   │ • 1-Wire Kassetten-Hot-Swap   │ • Latenzzähler (<10ms) │
└───────────────────────────────┴───────────────────────────────┴────────────────────────┘
```

### 7.1 Funktionsumfang des Simulators
1. **Mikrofon- & Headset-Live-Einspeisung:** Wähle jedes angebundene USB- oder Bluetooth-Headset mit regelbarem Gain und VAD-Schwellwert.
2. **Lenker-PTT Fernbedienung:** Taste im UI oder Halten der `[LEERTASTE]` schaltet das Mikrofon prellfrei frei und triggert das Ducking.
3. **1:1 Firmware Raised-Cosine Ducking:** Implementiert exakt die mathematische Kennlinie aus [`audio_dsp_pipeline.cpp`](../../firmware/main_controller/src/audio_dsp_pipeline.cpp) mit kontinuierlichem Dämpfungsverlauf.
4. **Motorrad-Tachometer & Fahrtwind:**
   * $0\dots 15\,\text{km/h}$ (Ampel/Rangieren): $100\,\%$ Transparenzmodus aktiv.
   * $15\dots 30\,\text{km/h}$: Stetiges Ausblenden über Raised-Cosine Flanke.
   * $> 30\,\text{km/h}$: Windgeräusch-Gate aktiv mit dynamischer Pink-Noise-Beimischung proportional zu $v^2$.
5. **1-Wire Kassetten-Hot-Swap:** Simuliert die hardware-spezifischen Klangprofile (Sena 60S Preamp/EQ, Cardo Packtalk Pro Kompression, OMM LoRa Telemetrie-Bandpass $300\dots 3400\,\text{Hz}$, Blindkassette $-96\,\text{dB}$).
