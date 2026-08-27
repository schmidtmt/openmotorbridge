# 16 - Simulation & Digitale Testbench

Um das Zusammenspiel von Hardware, Akustik, Fahrdynamik und Netzwerkprotokollen vor dem ersten Fertigungslauf auf Automotive-Niveau zu verifizieren, verfügt OpenMotorBridge über eine modulare Python-Simulations-Suite.

---

## 1. Übersicht der Simulations-Module

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 OPENMOTORBRIDGE DIGITALE TESTBENCH SUITE                    │
├───────────────────────┬───────────────────────┬─────────────────────────────┤
│ Modul                 │ Datei                 │ Test-Fokus                  │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 1. Audio-DSP &        │ `audio_dsp_sim.py`    │ Raised-Cosine Ducking,      │
│    Mikrofon-Schutz    │                       │ 4-Stufen Ambient-Schutz,    │
│                       │                       │ Local HearThrough Isolation │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 2. Powermanagement    │ `power_ups_sim.py`    │ KL15 Zündungszyklen,        │
│    & USV-Nachlauf     │                       │ Kurbelwellen-Einbruch,      │
│                       │                       │ JEITA LiPo-Schutz, 15m Run  │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 3. ADR-EKF Sensor-    │ `adr_ekf_sim.py`      │ 15-State Kalman-Filter,     │
│    fusion & Tunnel    │                       │ 2.5 km Tunnel ohne GNSS,    │
│                       │                       │ Dynamische Schräglage 45°   │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 4. 1-Wire Kassetten-  │ `cartridge_optopulse_ │ DS2401 LittleFS Parser,     │
│    & Opto-Sequenzer   │  sim.py`              │ TLP222A PhotoMOS ms-Timing, │
│                       │                       │ Gain-Offset Kalibrierung    │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 5. OpenMotorMesh      │ `omm_network_sim.py`  │ DLE Scoring-Wahl,           │
│    Protokoll & Radar  │                       │ Pass-Partitioning, LoRa,    │
│                       │                       │ Sirenen-Frühwarnung 10 Hz   │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ 6. PCB Design DFM/DRC │ `verify_pcb_designs_  │ JLCPCB 6-Stufen-Audit,      │
│    Verifikation       │  jlcpcb.py`           │ Leiterbahnen >= 0.127 mm,   │
│                       │                       │ Vias 0.3/0.6 mm, 0 DRC-Fehl.│
└───────────────────────┴───────────────────────┴─────────────────────────────┘
```

---

## 2. Audio-DSP & Mikrofonschutz-Simulation (`audio_dsp_sim.py`)

* **Simulierte Signale:** 
  * Port 1 (Sena) & Port 2 (Cardo) Sprachströme ($48\,\text{kHz}$).
  * Garmin-Navigationsansage (Prio 1, Dauer $3{,}5\,\text{s}$).
  * Front Ambient-Mikrofon mit variabler Windgeräusch- und Fahrtwind-Amplitude.
* **Verifikations-Kriterien:**
  1. **Ducking-Tiefe:** Port 1/2 werden während der Navi-Ansage exakt um $-12\,\text{dB}$ gedämpft.
  2. **Attack / Release:** $15\,\text{ms}$ Einschwingzeit, $600\,\text{ms}$ Haltezeit, $250\,\text{ms}$ Raised-Cosine Ausblendung.
  3. **Speed-Gating Transparenz:** $0-15\,\text{km/h}$ ($0\,\text{dB}$) $\rightarrow 15-30\,\text{km/h}$ (Raised-Cosine Fade) $\rightarrow > 30\,\text{km/h}$ ($-96\,\text{dB}$ Mute).
  4. **Leakage-Test:** $0{,}0\,\text{dB}$ Übersprechen des Frontmikrofons in die Mesh-TX-Leitungen.

---

## 3. Powermanagement & USV-Nachlauf-Simulation (`power_ups_sim.py`)

* **Simulierte Bordnetz-Spannungsverläufe:**
  * Ruhestrom im Stand ($12{,}6\,\text{V}$).
  * Motorstart: Starter-Einbruch auf $7{,}8\,\text{V}$ für $450\,\text{ms}$ $\rightarrow$ Unterbrechungsfreie Pufferung durch USV-Akku.
  * Fahrtende: KL15 Zündung AUS $\rightarrow$ 15 Minuten Countdown für WebDAV-Sync und BGH-Flush.
  * Tiefentladeschutz ($< 11{,}8\,\text{V}$) und ULP-Schlafmodus ($< 20\,\mu\text{A}$ nach 72 Stunden).
  * JEITA-Ladestop bei Kälte ($< 0^\circ\text{C}$) und Hitze ($> 45^\circ\text{C}$).

---

## 4. 15-State ADR-EKF & Tunnelfahrten-Simulation (`adr_ekf_sim.py`)

* **Szenario:** Alpenpass-Fahrt (Sustenpass) mit engen Kehren und Einfahrt in einen $2{,}5\,\text{km}$ langen Bergtunnel.
* **Sensordaten:**
  * Bosch BMI270 6-Achsen IMU ($100\,\text{Hz}$).
  * u-blox MAX-M10S GNSS ($10\,\text{Hz}$, Ausfall im Tunnel).
  * Fahrzeug-CAN Raddrehzahl-Odometer.
* **Verifikations-Ergebnis:**
  * Positionsfehler nach $2{,}5\,\text{km}$ Tunneldurchfahrt: $< 14{,}2\,\text{m}$.
  * Schräglagengenauigkeit in Kehren: $\pm 0{,}8^\circ$.

---

## 5. 1-Wire Kassetten- & PhotoMOS-Sequenzer-Simulation (`cartridge_optopulse_sim.py`)

* **Ablauf:**
  1. Simulation des Hot-Plug Events auf GPIO 2.
  2. Auslesen der 64-Bit Chip-UID via 1-Wire Protokoll.
  3. Laden des zugehörigen JSON-Profils aus LittleFS.
  4. Messung der Schaltimpulse der PhotoMOS-Optokoppler:
     * Mesh-Toggle: $200\,\text{ms} \pm 5\,\text{ms}$.
     * Channel Next: $800\,\text{ms} \pm 10\,\text{ms}$.
     * Pairing-Hold: $5000\,\text{ms} \pm 20\,\text{ms}$.
     * Quick-Pair: $200\,\text{ms}$ Pulse bei $2\,\text{Hz}$.

---

## 6. Ausführung der gesamten Testbench

Mit einem einzigen Befehl können alle Simulatoren automatisiert ausgeführt und validiert werden:

```bash
python3 tools/run_all_simulations.py
```

---

## 7. Automatisierte PCB Design- & DFM-Verifikation (`verify_pcb_designs_jlcpcb.py`)

* **Geprüfte Baugruppen:** Zentralbox-Hauptplatine, Pod-Basis, Universelle Wechselkassette, Heck-Pod 3 Transceiver.
* **Verifikations-Kriterien (JLCPCB-Standard):**
  1. **Leiterbahnbreiten & Abstände:** Signalbahnen $\ge 0{,}150\,\text{mm}$, Powerbahnen $\ge 0{,}350\,\text{mm}$ (Toleranzgrenze $\ge 0{,}127\,\text{mm}$).
  2. **Durchkontaktierungen (Vias):** $\varnothing\,0{,}30\,\text{mm}$ Bohrung, $\varnothing\,0{,}60\,\text{mm}$ Pad-Durchmesser, $0{,}15\,\text{mm}$ Restring.
  3. **Acid-Trap-Prüfung:** Eliminierung spitzer Leiterbahnwinkel $< 90^\circ$ durch $45^\circ$-Fasen.
  4. **Netlist & Pad-Zuordnung:** $100\,\%$ Zuweisung aller SMD- und THT-Pads ohne offene Ratsnest-Linien.
* **Ausführung:**
  ```bash
  python3 hardware/scripts/verify_pcb_designs_jlcpcb.py
  ```
