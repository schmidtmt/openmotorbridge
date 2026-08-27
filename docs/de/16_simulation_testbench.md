# 16 - Simulation & Digitale Testbench

Um das Zusammenspiel von Hardware, Akustik, Fahrdynamik, Thermik, Hochfrequenz-Physik und Netzwerkprotokollen vor dem ersten Fertigungslauf auf Automotive-Niveau lückenlos zu verifizieren, verfügt OpenMotorBridge über eine modulare Python-Simulations-Suite.

---

## 1. Übersicht der Simulations-Module

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       OPENMOTORBRIDGE DIGITALE TESTBENCH SUITE                          │
├───────────────────────────┬───────────────────────────────────┬─────────────────────────┤
│ Modul                     │ Datei                             │ Test-Fokus / Standard   │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 1. Multi-Board SPICE      │ `openmotorbridge_full_system_     │ 87V Load Dump, 6.5V USV,│
│    Verbundsimulation      │  sim.py`                          │ 85dB CMRR, 1.5m 1-Wire  │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 2. Hardware-in-the-Loop   │ `firmware_hil_system_sim.py`      │ 9 Live-Szenarien, PTT,  │
│    Firmware-Simulator     │                                   │ Blindkassette, DLE Mesh │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 3. 8h-Tagestour Thermik   │ `thermal_day_tour_sim.py`         │ -20°C Frost bis +58°C   │
│    Multi-Physik           │                                   │ Motor-Wärmestau im Stau │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 4. All-Weather Funk- &    │ `rf_rain_propagation_sim.py`      │ ITU-R P.838/P.840 Regen,│
│    Wellenausbreitung      │                                   │ Nebel, Gischt, Dual-PHY │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 5. Kfz-Transienten-       │ `automotive_iso7637_pulses_sim.py`│ ISO 7637-2 Level 4      │
│    Störfestigkeit         │                                   │ -150V, +50V, +/-220V    │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 6. Akustik & Wind-DSP     │ `acoustic_wind_dsp_sim.py`        │ 180 km/h Wind (93dB SPL)│
│    Sprachverständlichkeit │                                   │ 120Hz HPF, STOI > 0.70  │
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 7. 20-Fahrer Großgruppen- │ `mesh_group_scaling_sim.py`       │ 1.52 km Konvoi, 100% PDR│
│    Mesh & Partitioning    │                                   │ DLE Sub-Mesh Split/Merge│
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 8. 180-Tage Winterpause   │ `battery_winter_standby_sim.py`   │ 16.5 µA ULP-Hibernate,  │
│    Ruhestrom-Analyse      │                                   │ 0.59% Entladung / 6 Mon.│
├───────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ 9. PCB Design DFM/DRC     │ `verify_pcb_designs_jlcpcb.py`    │ JLCPCB 6-Stufen-Audit,  │
│    Verifikation           │                                   │ 4 Platinen, 0 DRC-Fehler│
└───────────────────────────┴───────────────────────────────────┴─────────────────────────┘
```

---

## 2. Multi-Board SPICE & Kabelbaum-Verbundsimulation (`openmotorbridge_full_system_sim.py`)

* **Geprüfte Kriterien:**
  1. **Automotive Load Dump (ISO 7637-2 / 87V Impuls 5b):** Clamping durch SMBJ33CA TVS-Diode auf sichere $54{,}1\,\text{V}$ ($+10{,}9\,\text{V}$ Headroom zum $65\,\text{V}$-Limit des LM5164 Buck).
  2. **USV-Kaltstart (6.5V Cold Crank):** BQ24075 schaltet in $8{,}5\,\mu\text{s}$ unterbrechungsfrei auf LiPo-Pufferung um.
  3. **Bourns Audio-Übertrager CMRR:** $85{,}0\,\text{dB}$ Gleichtaktunterdrückung gegen $1{,}2\,\text{kHz}$ Lichtmaschinen-Pfeifen $\rightarrow$ Restrauschen am Audio-Codec $< 141\,\mu\text{V}$ (glasklare $67{,}9\,\text{dB}$ Sprach-SNR).
  4. **1-Wire Signalintegrität über 1.5m Kabelbaum:** Flankenanstiegszeit $t_{\text{rise}} = 1{,}74\,\mu\text{s}$ über $167{,}9\,\text{pF}$ Gesamtkapazität ($65{,}3\,\%$ Sicherheitsmarge zur $5{,}0\,\mu\text{s}$-Norm).
  5. **PTT-zu-LoRa End-to-End Latenz:** Vom Tastendruck am Helm über Optokoppler, Opus-Encoder und UART-Bridge zum LoRa-Sendepuls in nur **$14{,}59\,\text{ms}$** ($< 25\,\text{ms}$ Aviation-Intercom-Norm).

---

## 3. Hardware-in-the-Loop (HIL) Firmware-Simulator (`firmware_hil_system_sim.py`)

Führt die reale C++-Firmware-Logik auf einer virtuellen Mehr-Platinen-Hardware aus und deckt 9 Lebenszyklus-Szenarien ab:

* **Szenario 1:** Zündung AN (KL15 = $12{,}60\,\text{V}$) $\rightarrow$ Cold Boot beider Controller $\rightarrow$ Grüne Status-LED.
* **Szenario 2A (Blindkassette):** Keine 1-Wire ROM-ID $\rightarrow$ Automatisches Profil `"disabled"` (Mute auf $-96\,\text{dB}$ Gain zum Schutz vor Rauschen und offenen Einstreuungen).
* **Szenario 2B (Hot-Swap):** Einklicken der Sena 60S / Cardo Edge Kassette im laufenden Betrieb $\rightarrow$ 1-Wire Erkennung in $< 2\,\text{s}$ $\rightarrow$ Laden des Profils, Audio-Entsperrung und Gain-Konfiguration.
* **Szenario 3:** NEO-M9N GNSS 3D-DGPS Fix (22 Satelliten) und 1-PPS Hardware-Zeitsynchronisation.
* **Szenario 4:** PTT-Tastendruck $\rightarrow$ Opus 24k Audio-Encodierung $\rightarrow$ Simultan-Broadcast auf $2{,}4\,\text{GHz}$ IEEE 802.15.4 Mesh und $868\,\text{MHz}$ SX1262 LoRa Fallback.
* **Szenario 5:** Motorstart ($6{,}5\,\text{V}$ Spannungseinbruch) $\rightarrow$ USV-Sofortpufferung $\rightarrow$ $0$ Audio-Drops, $0$ Reboots.
* **Szenario 6 (Kabelabriss & Kurzschluss):** M8-Kabel zum Helm reißt ab $\rightarrow$ Bourns PTC-Sicherung löst in $1{,}2\,\text{ms}$ aus ($< 15\,\text{mA}$ Kurzschlussstrom, $0\,\text{V}$ Einbruch auf Hauptplatine) $\rightarrow$ Anti-Pop Mute schützt Helmlautsprecher vor Krachen $\rightarrow$ Rote Warn-LED.
* **Szenario 7 (CAN-Bus Abriss):** TCAN334G Fehlerschutz $\rightarrow$ Automatischer Fallback der Geschwindigkeitserfassung auf GNSS/IMU-Koppelnavigation.
* **Szenario 8 (Bordnetz-Spannungsalarm):**
  * Stufe A ($< 11{,}8\,\text{V}$): Gelbe LED, Helm-Warnton (*Low Battery Chime*), Lastabwurf.
  * Stufe B ($0{,}0\,\text{V}$ Sicherungsausfall bei $80\,\text{km/h}$): USV-Übernahme, Sprachwarnung *"WARNING: MAIN POWER LOST"*, roter Strobe, Notfall-GPX-Flush.
* **Szenario 9:** Zündung AUS $\rightarrow$ 15-minütiger WebDAV/GPX Sync-Timer $\rightarrow$ ULP-Tiefschlaf ($< 20\,\mu\text{A}$).

---

## 4. 8-Stunden Tagestour Thermosimulation (`thermal_day_tour_sim.py`)

Modelliert die thermische Verlustleistung ($P \approx 2{,}0 - 2{,}6\,\text{W}$), Wärmekapazitäten ($C_{\text{PCB}} = 40{,}5\,\text{J/K}$, $C_{\text{ENC}} = 144\,\text{J/K}$) und Konvektion bei Geschwindigkeiten von $0$ bis $130\,\text{km/h}$:

* **Extrem-Sommer (Worst-Case Wüstenstau):**  
  Außentemperatur $45^\circ\text{C}$ + $58^\circ\text{C}$ Motorrad-Wärmestau unter der Sitzbank im Stillstand.
  * LM5164 DCDC Buck: $93{,}8^\circ\text{C}$ (Limit $150^\circ\text{C}$, $+56{,}2^\circ\text{C}$ Reserve).
  * ESP32-S3 Dual-Core: $90{,}2^\circ\text{C}$ (Limit $105^\circ\text{C}$, $+14{,}8^\circ\text{C}$ Reserve $\rightarrow$ **Kein Throttling**).
  * 3.3V LDO: $110{,}4^\circ\text{C}$ (Limit $125^\circ\text{C}$, $+14{,}6^\circ\text{C}$ Reserve).
  * NTC JEITA-Schutz: Schaltet LiPo-Ladestrom bei $> 45^\circ\text{C}$ Zellentemperatur ab.
* **Arktischer Winter ($-20^\circ\text{C}$ Kaltstart $\rightarrow -5^\circ\text{C}$ Tour):**  
  * Eigenerwärmung: Die $2\,\text{W}$ Verlustleistung erwärmt das IP67-Gehäuse innerhalb von $10\,\text{min}$ auf $+10^\circ\text{C}$.
  * JEITA-Kälteschutz: Sperrt Ladung unter $0^\circ\text{C}$ (Lithium-Plating-Schutz), erlaubt aber sicheres Entladen bis $-20^\circ\text{C}$.
  * TCXO-Oszillatoren ($\pm 0{,}5\,\text{ppm}$): $0\,\text{Hz}$ Frequenzdrift bei LoRa und GNSS.

---

## 5. All-Weather ITU-R Funk- & Wellenausbreitung (`rf_rain_propagation_sim.py`)

Berechnet die Dämpfung nach ITU-R P.838-3 (Regen), ITU-R P.840-9 (Nebel) und ITU-R P.676-13 (Luftfeuchte) inklusive dielektrischer Radom-Verstimmung ($\epsilon_r = 80$ Wasserfilm):

| Wetterszenario | $2{,}4\,\text{GHz}$ HiFi Range (Opus 24k) | $868\,\text{MHz}$ LoRa Fallback Range | GNSS Satelliten-C/N0 |
| :--- | :---: | :---: | :---: |
| **Trocken & Klar ($25^\circ\text{C}$)** | **$3126\,\text{m}$** | **$3{,}98\,\text{km}$** | $44{,}0\,\text{dB-Hz}$ (3D DGPS Fix) |
| **Dichter Alpennebel ($<30\,\text{m}$ Sicht)** | **$2047\,\text{m}$** | **$3{,}98\,\text{km}$** | $43{,}5\,\text{dB-Hz}$ (3D DGPS Fix) |
| **Tropisch Schwül ($40^\circ\text{C}$ / $100\%$ rF)** | **$2175\,\text{m}$** | **$3{,}98\,\text{km}$** | $43{,}7\,\text{dB-Hz}$ (3D DGPS Fix) |
| **Autobahn-Gischt & Spritzwasser** | **$1424\,\text{m}$** | **$3{,}98\,\text{km}$** | $42{,}3\,\text{dB-Hz}$ (3D DGPS Fix) |
| **Starker Sommerregen ($25\,\text{mm/h}$)** | **$1188\,\text{m}$** | **$3{,}98\,\text{km}$** | $41{,}7\,\text{dB-Hz}$ (3D DGPS Fix) |
| **Tropischer Wolkenbruch ($50\,\text{mm/h}$)** | **$878\,\text{m}$** | **$3{,}98\,\text{km}$** | $40{,}5\,\text{dB-Hz}$ (3D DGPS Fix) |

---

## 6. Kfz-Transienten nach ISO 7637-2 Level 4 (`automotive_iso7637_pulses_sim.py`)

* **Puls 1 (Induktives Relais-Abschalten $-150\,\text{V}$, $2\,\text{ms}$):** $100\,\%$ von Schottky-Diode geblockt ($0\,\text{V}$ auf Board, USV puffert $5\,\text{V}$).
* **Puls 2a (Schalttransiente $+50\,\text{V}$):** TVS klemmt auf $41{,}0\,\text{V}$ ($+24\,\text{V}$ Headroom zum $65\,\text{V}$ Buck).
* **Puls 3a/3b (Zündkerzenbursts $\pm 220\,\text{V}$, $100\,\text{ns}$):** LC-Filter dämpft um $-118{,}5\,\text{dB}$ auf unmerkliche $12{,}4\,\text{mV}$ Restwelligkeit.
* **Verpolungsschutz ($-14{,}2\,\text{V}$ Falschanschluss):** Schottky sperrt vollständig (Sperrstrom $< 18{,}5\,\mu\text{A}$).

---

## 7. Akustik & Windgeräusch-DSP bei 180 km/h (`acoustic_wind_dsp_sim.py`)

* **Windgeräusch-Modell:** Turbulente Grenzschichtdrücke am Helmvisier steigen auf bis zu $92{,}6\,\text{dB SPL}$ bei $180\,\text{km/h}$.
* **DSP-Wirkung:**
  * $120\,\text{Hz}$ 2nd-Order Hochpass schneidet $82\,\%$ der Winddruckenergie ab.
  * Spektral-Subtraktion verbessert den Signal-Rauschabstand um bis zu $+28{,}5\,\text{dB}$.
* **Sprachverständlichkeit (STOI Score):**
  * $100\,\text{km/h}$: **$0{,}80 / 1{,}00$** (Sehr gut verständlich)
  * $160\,\text{km/h}$: **$0{,}70 / 1{,}00$** (Gute Verständlichkeit über Opus 24k)
  * $180\,\text{km/h}$: **$0{,}67 / 1{,}00$** (Klare Stimm-Ortung, kein Übersteuern).

---

## 8. 20-Fahrer Großgruppen-Mesh (`mesh_group_scaling_sim.py`)

* **Konvoi:** 20 Motorräder ($1{,}52\,\text{km}$ Kolonnenlänge).
* **Metriken:** $100{,}0\,\%$ Packet Delivery Ratio (PDR), $11{,}5\,\text{ms}$ HiFi-Latenz auf $2{,}4\,\text{GHz}$, $26{,}5\,\text{ms}$ LoRa-Fallback.
* **Mesh-Partitioning:** Automatische Aufteilung in zwei autonome Sub-Meshes per Dynamic Leader Election (DLE) und verschmelzungsfreies Re-Merge nach Wiedersehen in $< 250\,\text{ms}$.

---

## 9. 180-Tage Winterpause in der Garage (`battery_winter_standby_sim.py`)

* **Ruhestrom im ULP-Hibernate:** Nur **$16{,}5\,\mu\text{A}$**.
* **Entladung nach 6 Monaten:** OpenMotorBridge verbraucht nur **$0{,}071\,\text{Ah}$ ($0{,}59\,\%$** einer $12\,\text{Ah}$ Batterie).
* **Frühjahrs-Zustand:** Die Motorradbatterie hat im Frühling noch **$85{,}3\,\%$ SoC ($12{,}65\,\text{V}$)** $\rightarrow$ Motorrad springt sofort beim ersten Startversuch an.

---

## 10. Ausführung der Master-Testbench

Alle 8 Testbenches können vollautomatisiert mit einem einzigen Befehl ausgeführt werden:

```bash
python3 tools/run_all_simulations.py
```
