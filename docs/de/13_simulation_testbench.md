# 13 - Digitale Simulation & Multi-Physik Master-Testbench (12 Module)

Um das Zusammenspiel von Hardware, Akustik, Fahrdynamik, Thermik, Hochfrequenz-Physik und Netzwerkprotokollen vor dem ersten Fertigungslauf auf Automotive-Niveau lückenlos zu verifizieren, verfügt OpenMotorBridge über eine modulare Python-Simulations-Suite.

> [!NOTE]
> **v10.0 Standardized Node Architecture Testbench-Update:**  
> OpenMotorBridge v10.0 ersetzt das frühere UWB-Backbone durch einen hochrobusten, geschirmten **4-Ader Automotive-USB-Bus** (`VCC_BUS` 12V/PD, `GND`, `USB_D-`, `USB_D+`) mit bis zu 60W Ladeleistung und $< 0{,}2\,\text{ms}$ Latenz. Die Zentralbox (`PCBA 01`) integriert Dual-Power Input (12V Bordnetz via Deutsch DTM-12 vs. 5V–20V USB-PD Sink via TI LM5050 Ideal-Dioden-OR-ing). Die Testbench simuliert das 7-Platinen-System (`PCBA 01`, `03`, `05`, `05B`, `07`, `08`, `09`, `10`), die symmetrischen Spiegel-Pods mit 5-Gesten-Erkennung, kassettenfreie Monocoque-Pods mit EPDM-Dry-Flap und unterbrechungsfreie USB Audio Class 2.0 Streams.

---

## 1. Übersicht der Simulations-Module

```
+-----------------------------------------------------------------------------------------+
|                       OPENMOTORBRIDGE DIGITALE TESTBENCH SUITE                          |
+---------------------------+-----------------------------------+-------------------------+
| Modul                     | Datei                             | Test-Fokus / Standard   |
+---------------------------+-----------------------------------+-------------------------+
| 1. Multi-Board SPICE      | `openmotorbridge_full_system_     | 87V Load Dump, 6.5V USV,|
|    Verbundsimulation      |  sim.py`                          | 85dB CMRR, Front Node   |
+---------------------------+-----------------------------------+-------------------------+
| 2. Hardware-in-the-Loop   | `firmware_hil_system_sim.py`      | 10 Live-Szenarien, PTT, |
|    Firmware-Simulator     |                                   | Front Node, DLE Mesh    |
+---------------------------+-----------------------------------+-------------------------+
| 3. 8h-Tagestour Thermik   | `thermal_day_tour_sim.py`         | -20°C Frost bis +58°C   |
|    Multi-Physik           |                                   | Motor-Wärmestau im Stau |
+---------------------------+-----------------------------------+-------------------------+
| 4. All-Weather Funk- &    | `rf_rain_propagation_sim.py`      | ITU-R P.838/P.840 Regen,|
|    Wellenausbreitung      |                                   | Nebel, Gischt, Dual-PHY |
+---------------------------+-----------------------------------+-------------------------+
| 5. Kfz-Transienten-       | `automotive_iso7637_pulses_sim.py`| ISO 7637-2 Level 4      |
|    Störfestigkeit         |                                   | -150V, +50V, +/-220V    |
+---------------------------+-----------------------------------+-------------------------+
| 6. Akustik & Wind-DSP     | `acoustic_wind_dsp_sim.py`        | 180 km/h Wind (93dB SPL)|
|    Sprachverständlichkeit |                                   | 120Hz HPF, STOI > 0.70  |
+---------------------------+-----------------------------------+-------------------------+
| 7. 20-Fahrer Großgruppen- | `mesh_group_scaling_sim.py`       | 1.52 km Konvoi, 100% PDR|
|    Mesh & Partitioning    |                                   | DLE Sub-Mesh Split/Merge|
+---------------------------+-----------------------------------+-------------------------+
| 8. 180-Tage Winterpause   | `battery_winter_standby_sim.py`   | 16.5 µA ULP-Hibernate,  |
|    Ruhestrom-Analyse      |                                   | 0.59% Entladung / 6 Mon.|
+---------------------------+-----------------------------------+-------------------------+
| 9. Universal Front Node   | `front_node_wireless_hub_sim.py`  | USB2514B Eye, MEMS DSP, |
|    (PCBA 05)              |                                   | TPS2051B, USB Bus, BLE      |
+---------------------------+-----------------------------------+-------------------------+
| 10. Live Audio DSP Studio | `tools/audio_testbench/server.py` | Interaktive Web-Audio   |
|     & Echtzeit-Simulator  |                                   | Suite, Mic/PTT/Tacho/EQ |
+---------------------------+-----------------------------------+-------------------------+
| 11. Multi-Motorrad        | `openmotorbridge_digital_twin.py` | 5 PCBs (v10.0), Wil-Watt-|
|     Digital-Twin & HIL    |                                   | Ricken, Tunnel EKF-DR,  |
|                           |                                   | 2.4G/LoRa Handover, PWA |
+---------------------------+-----------------------------------+-------------------------+
| 12. HIL/SIL Netzlisten-   | `testbench_netlist_validator.py`  | KiCad .net vs. C++ GPIO,|
|     & Firmware-Validator  |                                   | SPI-Mock, Task-Latenz   |
+---------------------------+-----------------------------------+-------------------------+
```

---

## 2. Multi-Board SPICE & Kabelbaum-Verbundsimulation (`openmotorbridge_full_system_sim.py`)

* **Geprüfte Kriterien:**
  1. **Automotive Load Dump (ISO 7637-2 / 87V Impuls 5b):** Clamping durch SMBJ33CA TVS-Diode auf sichere $54{,}1\,\text{V}$ ($+10{,}9\,\text{V}$ Headroom zum $65\,\text{V}$-Limit des LM5164 Buck).
  2. **USV-Kaltstart (6.5V Cold Crank):** BQ24075 schaltet unterbrechungsfrei ($0\,\mu\text{s}$) auf LiPo-Pufferung um.
  3. **Staged Power Sequencing Inrush Profile:** T=0ms Core, T=200ms Radar, T=350ms Cartridge, T=500ms Audio/CAN ($I_{\text{peak}} = 1{,}45\,\text{A} < 3{,}0\,\text{A}$).
  4. **Satelliten-Pod Interface (PCBA 03):** USB-PD Controller (SC8721/TPS25750) bis 30W/60W Laden, ES8388 Audio-Codec via USB Audio Class 2.0 und OptoMOS K1 PTT-Keying Delay ($< 10\,\mu\text{s}$). Hubmagnete und DW3110 entfallen ersatzlos.
  5. **Radar 2.0 Sub-MCU & Halo Wings (PCBA 08):** Wheeltec 77 GHz MR20 Radar Target Tracking, TTC-Mathematik und Stromversorgung der 36x WS2812B Halo Wings ($5\,\text{V} / 1{,}8\,\text{A}$ max).
  6. **Universal Front Node DCDC & Hub (PCBA 05):** TPS54302 Synchrongleichrichter mit $92{,}4\,\%$ Wirkungsgrad ($9{,}6\,\text{mV}$ Ripple), USB2514B High-Speed Augendiagramm mit $88{,}5\,\%$ Öffnung, SAM-M10Q 10 Hz PVT & AssistNow A-GPS ($1{,}8\,\text{s}$ TTFF), TMP117 Kaltluftsensor ($\pm 0{,}1^\circ\text{C}$), OPT3001 Lux-Sensor.
  7. **Geschirmter 4-Draht-Automotive-Kabelbaum & JST-GH:** Spannungsabfall über Bordnetz $< 150\,\text{mV}$ (Front Node $130{,}6\,\text{mV}$, Radar $81{,}1\,\text{mV}$, Cartridge $7{,}5\,\text{mV}$).
  8. **4-Draht Automotive-USB-Bus Backbone:** Front Node ($< 0{,}20\,\text{ms}$), Pod ($< 0{,}15\,\text{ms}$), Radar UART ($< 0{,}25\,\text{ms}$) $\rightarrow$ Deterministische Gesamtlatenz $< 0{,}20\,\text{ms}$.
  9. **Symmetrische Spiegel-Pods (PCBA 05B) 5-Gesten Engine:** Vom Tastendruck am Spiegel-Pod über den 4-Draht USB-Bus zum OptoMOS K1 in nur **$< 0{,}20\,\text{ms}$**.
  10. **Ottocast Auto-Café VBUS-Abschaltung:** Automatischer $60\,\text{s}$ Countdown nach Zündung AUS zur Freigabe des Smartphone-WLANs sowie 1-Klick Hard-Reboot ($2{,}5\,\text{s}$ Power-Cut).

---

## 3. Hardware-in-the-Loop (HIL) Firmware-Simulator (`firmware_hil_system_sim.py`)

Führt die reale C++-Firmware-Logik auf einer virtuellen Mehr-Platinen-Hardware aus und deckt 10 Lebenszyklus-Szenarien ab:

* **Szenario 1:** Zündung AN (KL15 = $12{,}60\,\text{V}$) ODER USB-PD Sink (5V-20V Werkbank-Modus) $\rightarrow$ TI LM5050 Ideal-Dioden-OR-ing Validierung $\rightarrow$ Staged Power-On Boot aller Controller $\rightarrow$ USB-Bus-Enumeration aller Knoten.
* **Szenario 2 (Satelliten-Pod USB Handshake & Profile):** USB-Enumeration des Pods $\rightarrow$ Erkennung des Profils (Sena SPIDER X Slim, Cardo Packtalk Pro, OMM UCS, PMR446) $\rightarrow$ USB-PD Ladeverhandlung (5V/9V/12V/20V bis 30W/60W).
* **Szenario 3 (Front Sensor Hub & 10 Hz GNSS):** SAM-M10Q 10 Hz Multi-GNSS Fix mit AssistNow A-GPS Seed $\rightarrow$ 4-Draht USB-Bus Übertragung an ADR-EKF $\rightarrow$ TI TMP117 Kaltluftstrom-Messung löst bei $\le 3{,}5^\circ\text{C}$ akustische Glatteiswarnung im Helm aus.
* **Szenario 4 (Spiegel-Pod 5-Gesten -> USB-Bus -> Pod Keying):** Daumentaster am Spiegel-Pod $\rightarrow$ 5-Gesten Entprellung ($< 10\,\mu\text{s}$) $\rightarrow$ USB-Bus Frame $\rightarrow$ Pod schaltet PTT via OptoMOS K1 in insgesamt **$< 0{,}20\,\text{ms}$** durch.
* **Szenario 5 (77 GHz Radar Gefahrenerkennung & Halo Wings):** Wheeltec MR20 erfasst schnell herannahendes Fahrzeug ($18\,\text{m}$, $-45\,\text{km/h}$, TTC $1{,}44\,\text{s}$) $\rightarrow$ Stufe 2 Kollisionswarnung $\rightarrow$ 36x WS2812B Halo Wings zünden expandierenden Chevron-Strobe.
* **Szenario 6 (Starter-Kaltstart 6.5V):** Starter zieht $150\,\text{A}$ $\rightarrow$ Bordnetz bricht für $350\,\text{ms}$ auf $6{,}50\,\text{V}$ ein $\rightarrow$ BQ24075 USV-Pufferung hält Systemspannung auf $4{,}12\,\text{V}$ $\rightarrow$ $0$ USB-Paket-Verluste, $0$ Reboots.
* **Szenario 7 (SW1 Hardware Pairing-Fenster & Roaming):** Taster SW1 an Zentralbox aktiviert 60-Sekunden ECDH-Pairing-Fenster $\rightarrow$ Automatische Zuweisung von Roaming-Slots für Gast-Motorräder (z. B. *"BIKE_2_BMW_R1300GS"*).
* **Szenario 8 (Universal Group Split Rescue Engine):** Konvoi verliert Peer hinter Bergkamm (RSSI $< -92\,\text{dBm}$) $\rightarrow$ Rescue Engine initiiert Fallback auf LoRa 868.3 MHz Positionstracking.
* **Szenario 9 (Front Node CP2AA 1-Klick Reset & Auto-Café):** 1-Klick CarPlay Reboot ($2{,}5\,\text{s}$ TPS2051B VBUS-Kaltstart) und $60\,\text{s}$ Auto-Café Abschalt-Countdown nach Zündung AUS.
* **Szenario 10 (15-Minuten GPX/WebDAV Run-Down):** Zündung AUS $\rightarrow$ 15-minütiger Nachlauf mit MicroSD Blackbox-Sync und WebDAV-Upload über Heim-WLAN $\rightarrow$ ULP-Tiefschlaf ($< 18\,\mu\text{A}$).

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

## 10. Universal Front Node (PCBA 05) (`front_node_wireless_hub_sim.py`)

Verifiziert alle hochfrequenten, leistungselektronischen und funktechnischen Subsysteme der Front-Knoten-Baugruppe (PCBA 05):

1. **USB 2.0 High-Speed Augendiagramm (Microchip USB2514B):**
   * Datenrate: $480{,}0\,\text{Mbps}$ mit $Z_{\text{diff}} = 90{,}2\,\Omega$ (Toleranzfenster: $90 \pm 9\,\Omega$).
   * Intra-Pair Laufzeitversatz: nur $2{,}38\,\text{ps}$ (Spezifikation: $< 45\,\text{ps}$).
   * Augenöffnung: $89{,}4\,\%$ Augenbreite ($1863\,\text{ps}$) und $362{,}7\,\text{mV}$ differentielle Höhe $\rightarrow$ Perfekt rauschfreie Datenübertragung zu Dongle und Handschuhfach.
2. **TI TPS2051B VBUS Lastschalter & Schutzschaltung:**
   * Soft-Start Einschaltstrom: sanfter Anstieg in $1{,}20\,\text{ms}$ begrenzt Spitzenstrom bei $100\,\mu\text{F}$ Dongle-Pufferung auf $0{,}417\,\text{A}$ ($< 1{,}0\,\text{A}$ Limit).
   * Kurzschlussabschaltung: $6{,}2\,\mu\text{s}$ Reaktionszeit auf `FAULT_N` bei Überstrom.
   * 1-Klick Kaltstart: $2{,}50\,\text{s}$ kompletter VBUS-Power-Cycle zum zuverlässigen Rebooten hängender Wireless-Dongles.
3. **Knowles SPH0645 Digitales I2S MEMS & A-Weighting Filter:**
   * Abtastung: $16\,\text{kHz}$ / 24-Bit über Direct Memory Access (DMA).
   * Biquad Direct Form II Digitalfilter nach IEC 61672-1 Class 1 ($100\,\text{Hz}$ Winddruck-Dämpfung $-19{,}1\,\text{dB}$).
   * $20\,\text{ms}$ RMS-Blockbildung mit kalibrierter $\text{dB(A)}$-Telemetrie an die Zentralbox im $50\,\text{Hz}$ Takt.
4. **Spiegel-Pod Ultra-Low-Latency PTT & Gesten Budget (< 0.2 ms):**
   * Hardware-RC & TVS ESD Filterung: $8{,}0\,\mu\text{s}$.
   * GPIO Edge-Interrupt & 5-Gesten Engine: $15{,}0\,\mu\text{s}$.
   * Nativer USB 2.0 Frame über 4-Draht Bus: $45{,}0\,\mu\text{s}$.
   * Zentralbox USB RX & DSP Dispatch: $30{,}0\,\mu\text{s}$.
   * Pod OptoMOS K1 Relais-Schaltung: $< 50{,}0\,\mu\text{s}$.
   * **Gesamtlatenz (Glass-to-Glass): $< 0{,}20\,\text{ms}$** (Anforderung $< 5{,}0\,\text{ms}$) bei $100{,}0\,\%$ Zuverlässigkeit über geschirmte Leitung.
5. **Dual-Bank OTA Rollback-Schutz:**
   * Fehlersimulation: Spannungsunterbrechung bei $45\,\%$ Flash-Fortschritt in Partition `ota_1`.
   * Bootloader-Integritätsprüfung erkennt unvollständige Signatur und bootet zuverlässig `ota_0` $\rightarrow$ **$0{,}0\,\%$ Brick-Risiko**.

---

## 11. Multi-Motorrad Digital-Twin & 8-PCB HIL Simulator (`openmotorbridge_digital_twin.py`)

Der **Digital Twin Simulator** ([`openmotorbridge_digital_twin.py`](../../tools/simulators/openmotorbridge_digital_twin.py)) emuliert einen realitätsgetreuen 2-Fahrzeuge-Verbund (Bike A = Leader, Bike B = Chaser) mit insgesamt **8 physikalisch modellierten Platinen** (4 PCB-Klassen pro Motorrad) entlang der geodätischen Referenzstrecke **Wil SG $\rightarrow$ Wattwil (Tunnel) $\rightarrow$ Wattwil-Kreisel $\rightarrow$ Rickenpass**:

```
                      DIGITAL TWIN ARCHITEKTUR (8 PLATINEN & 2 BIKES)
=======================================================================================

   [ GEODÄTISCHER TRACK: WIL --> WATTWIL-TUNNEL (2.2km) --> KREISEL --> RICKENPASS ]
                                         |
         +-------------------------------+-------------------------------+
         v                                                               v
 +----------------------------------------+            +----------------------------------------+
 |          MOTORRAD A (LEADER)           |            |          MOTORRAD B (CHASER)           |
 |  * PCBA 01 (ESP32-S31 + QCC3084 + LoRa)  |            |  * PCBA 01 (ESP32-S31 + QCC3084 + LoRa)  |
 |  * PCBA 03 (Pods 1/2 4-Draht Bus Inlays)   |            |  * PCBA 03 (Pods 1/2 4-Draht Bus Inlays)   |
 |  * PCBA 05 (Universal Front Node)      |            |  * PCBA 05 (Universal Front Node)      |
 +-------------------+--------------------+            +-------------------+--------------------+
                     |                                                     |
                     +----------------> [ RF PROPAGATION ENGINE ] <--------+
                                        * Log-Distance Modell (Friis)
                                        * 38 dB Dämpfung in Tunnelröhre
                                        * 2.4 GHz OMM High-Speed Mesh (<150m)
                                        * 868 MHz LoRa Fallback (>150m / Tunnel)
                                        * Dynamic Leader Election (DLE)
                                                       |
                                                       v
                                        +-----------------------------+
                                        | PURE-PYTHON WEBSOCKET SERVER|  (Port 8765)
                                        +--------------+--------------+
                                                       |
                                                       v
                                        +-----------------------------+
                                        |    OPENMOTORBRIDGE PWA      |  Live Dashboard
                                        | (Tacho, Schräglage, Radar,  |  im Webbrowser
                                        |  EKF-Tunnel-DR, Mesh-Topol.)|
                                        +-----------------------------+
```

### Die Kernkomponenten & Test-Features:
1. **Aktive Platinenklassen pro Motorrad:**
   * **PCBA 01 (Zentralbox):** 15-State ADR-EKF Filterung, Power Supervisor (Dual-Power: 12V DTM-12 & USB-PD Sink), ESP32-S31 AI DSP, Qualcomm QCC3084 BT 5.4 Audio SoC & Semtech SX1262 LoRa 868 MHz Transceiver.
   * **PCBA 03 (Satelliten-Pods, 2x):** 4-Draht Bus Interface mit ESP32-C6 Host-MCU, ES8388 Audio-Codec, bis 30W/60W USB-PD Ladeport mit Dry-Flap, OptoMOS K1 PTT-Relais (`sena_spider`, `cardo_edge`, `omm_ucs`, `pmr446`).
   * **PCBA 05 (Universal Front Node) & PCBA 05B (Spiegel-Pods, 2x):** u-blox SAM-M10Q Multi-GNSS via I2C, Knowles MEMS Akustikmessung, 4-Draht Bus Interface und symmetrische Under-Perch Spiegel-Pods mit 5-Gesten Tastern und BSD LEDs.
2. **Geodätischer Track (`wil_wattwil_ricken.py`):**
   * $11\,682$ Stützpunkte mit realistischer Beschleunigung, Kurvenschräglage ($\theta_{\text{lean}} = \arctan(v \cdot \dot{\psi} / g)$ bis $42^\circ$) und Höhenprofil ($570\dots 795\,\text{m}$ ü. M.).
3. **15-State ADR-EKF Tunnelausfall & Koppelnavigation:**
   * Bei Einfahrt in den $2{,}2\,\text{km}$ langen Wattwil-Tunnel bricht der GNSS-Fix schlagartig ab ($Sats = 0$, $HDOP = 99{,}9$).
   * Das EKF integriert CAN-Raddrehzahl und IMU-Gierrate mit realistischem Rest-Drift.
   * Nach $132\,\text{s}$ Tunnelfahrt beträgt die Positionsdrift am Wattwil-Kreisel lediglich **$18{,}83\,\text{m}$** (Automotive-Norm $< 30\,\text{m}$ bzw. $< 1{,}5\,\%$) $\rightarrow$ das Motorrad trifft die Kreiseleinfahrt geometrisch präzise.
4. **HF-Propagation & Dynamischer Dual-PHY Handover:**
   * **Freie Strecke ($d < 150\,\text{m}$):** 2.4 GHz High-Speed Mesh ($250\,\text{kbps}$, Opus 24k Full-Duplex Audio, 20 Hz Telemetrie).
   * **Tunnelfahrt oder Abriss ($RSSI < -88\,\text{dBm}$):** Automatischer nahtloser Handover auf 868 MHz LoRa (Half-Duplex PTT, 1 Hz Telemetrie).
   * **Wiederannäherung am Rickenpass:** Hysterese-gesteuerter Rück-Handover auf 2.4 GHz Mesh ($+4\,\text{dB}$ Marge).
5. **Live PWA-Anbindung:**
   * Pure-Python RFC 6455 WebSocket Server auf `ws://localhost:8765`.
   * In der PWA ([`webapp_pwa/index.html`](../../webapp_pwa/index.html)) schaltet der Button **🚀 Digital Twin** die Verbindung sofort aktiv. Alle Tacho-, Schräglagen-, Radar-, Tunnel- und Mesh-Daten werden mit 10 Hz live visualisiert.
6. **Containerisierung:**
   * [`tools/simulators/Dockerfile.sim`](../../tools/simulators/Dockerfile.sim) ermöglicht die Ausführung in Podman oder Docker.

---

## 12. Interaktives Live Audio DSP Studio & Echtzeit-Simulator (`tools/audio_testbench/`)

Während die 11 numerischen Python-Module die Grenzparameter rechnerisch auditieren, dient das **Live Audio DSP Studio** der hörbaren Echtzeit-Erprobung im Webbrowser:

```bash
python3 tools/audio_testbench/server.py
```

* **Reale Mikrofon-Einspeisung:** Unterstützt jedes angeschlossene Headset / USB-Mikrofon mit einstellbarem Vorverstärker-Pegel und VAD-Schwellwert.
* **Leertaste als Lenker-PTT:** Halten der Leertaste `[SPACE]` simuliert die prellfreie Auslösung des TLP222A Optokopplers.
* **Firmware-identisches Raised-Cosine Ducking:** Stetige Lautstärkeabsenkung um $-12\,\text{dB}$ mit $15\,\text{ms}$ Attack und $800\,\text{ms}$ Release ohne jegliche Knackgeräusche.
* **Virtueller Motorrad-Tacho (0 bis 160 km/h):**
  * $0\dots 15\,\text{km/h}$ (Ampel / Stillstand): Transparenzmodus mit Umgebungs-Einblendung ($350\,\text{Hz}\dots 3{,}2\,\text{kHz}$).
  * $15\dots 30\,\text{km/h}$: Raised-Cosine Ausblendung.
  * $> 30\,\text{km/h}$: Windgeräusch-Gate aktiv mit dynamischem rosa Rauschen proportional zu $v^2$.
* **USB Pod-Hot-Swap & Handshake:** Umschaltung zwischen Sena SPIDER X Slim (EQ-Boost), Cardo Packtalk Pro (Vocal-Kompression), OMM LoRa Notfall-Bandpass ($300\dots 3400\,\text{Hz}$) und Stummschaltung (Dry Box).
* **Visuelle DSP-Telemetrie:** Stereo FFT-Spektrumanalysator, Dreifach-VU-Meter und Oszilloskop für den Dämpfungsverlauf.

---

## 13. HIL/SIL Netzlisten- & Firmware-Validator (`tools/simulators/testbench_netlist_validator.py`)

Um vor der Platinenbestellung (PCBA 01 bis 08) und vor dem ersten Flashvorgang sicherzustellen, dass die realen KiCad-Schaltpläne und der C++ Firmware-Quellcode zu 100 % deckungsgleich sind, gleicht der **HIL/SIL Netzlisten- & Firmware-Validator** alle Schnittstellen automatisiert ab:

```bash
python3 tools/simulators/testbench_netlist_validator.py
```

### 13.1 Kern-Prüfungen der HIL/SIL Pipeline:
1. **Automatischer KiCad S-Expression Netlist Parser:**
   * Liest `hardware/kicad_main_box/openmotorbridge_main.net` ein und verifiziert alle 72 Netze und Schlüsselbausteine:
     - `U1` (TI LM5164-Q1 72V Buck), `U2` (ESP32-S31 AI RISC-V), `U3` (Everest Semi ES8388), `U6` (TI TCAN334G), `U7` (Semtech SX1262), `U8` (TI LM5050-Q1 Ideal-Diode), `U9` (Qualcomm QCC3084 BT 5.4), `U10` (TI TPS7A0533 LDO) und `ANT1` (Taoglas FXP895).
2. **Firmware-GPIO-Kollisionsprüfung:**
   * Parst `firmware/front_node/src/front_node_config.h` sowie die Zentralbox-Treiber.
   * Prüft alle 22 GPIO-Definitionen auf Mehrfachbelegungen, Floating-Pins und Pin-Multiplexing-Konflikte (0 Kollisionen zulässig).
3. **SPI-Transceiver Hardware-Mocking (HIL/SIL):**
   * **4-Draht USB-Bus:** USB 2.0 High-Speed @ 480 Mbps, maximales Latenzbudget $< 200\,\mu\text{s}$ ($< 0{,}2\,\text{ms}$ Kriterium).
   * **Semtech SX1262 LoRa:** SPI3 @ 10 MHz, maximales Latenzbudget $850\,\mu\text{s}$.
   * **Everest Semi ES8388:** I2S0 @ 12.288 MHz, DMA-Pufferzeit $2670\,\mu\text{s}$.
4. **FreeRTOS Task-Profiler & Worst-Case Execution Time (WCET):**
   * Simuliert die Core-Auslastung unter Last (Gleichzeitiger USB-Bus-Stream, Audio-DSP, CAN-FD Empfang und EKF-Dead-Reckoning):
     - `USB_Bus_Task` (Prio 22, Core 0): WCET $110\,\mu\text{s}$ (Budget $250\,\mu\text{s}$, Marge $+140\,\mu\text{s}$).
     - `Audio_DSP_Task` (Prio 20, Core 1): WCET $1420\,\mu\text{s}$ (Budget $2667\,\mu\text{s}$, Marge $+1247\,\mu\text{s}$).
     - `CAN_TWAI_Task` (Prio 15, Core 0): WCET $80\,\mu\text{s}$ (Budget $1000\,\mu\text{s}$, Marge $+920\,\mu\text{s}$).

---

## 14. Ausführung der Master-Testbench

Alle numerischen Batch-Testbenches und Validatoren können vollautomatisiert ausgeführt werden:

```bash
# Gesamte Simulations-Suite ausführen
python3 tools/run_all_simulations.py

# HIL/SIL Netzlisten- und Firmware-Validator separat starten
python3 tools/simulators/testbench_netlist_validator.py
```
