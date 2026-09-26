# 14 - EMV-Härtung, Schirmung & ESD-Schutz

Dieses Dokument spezifiziert die Schutzschaltungen gegen Kfz-Bordnetz-Transienten (ISO 7637-2), die HF-Entkopplung im 2.4-GHz-, 868-MHz- und 6.5-GHz-UWB-Band, die Schutzlackierung nach IPC-CC-830B sowie die mechanische Vibrations- und Schockdämpfung nach ISO 16750-3 für die OpenMotorBridge v8.0 Clean Architecture.

---

## 1. Kfz-Transienten- und Überspannungsschutz (ISO 7637-2 & ISO 16750-2)

* **Bordnetz-Absicherung:** Vollständige Konformität nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V) und ISO 16750-2 Load-Dump.
* **Eingangssicherung:** Bourns MF-MSMF050-2 rückstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
* **Überspannungsschutz:** Littelfuse SMBJ33CA bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) $\rightarrow$ bietet dem 65V LM5164 Regler komfortable $> 11{,}7\,\text{V}$ Sicherheitsabstand bei Load-Dumps.
* **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem geringem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Filterung & Entstörung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor / 3 A + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 2. HF-Entkopplung, UWB-Backbone & Raumdiversität

* **2,4-GHz-Koexistenz (Sena vs. Cardo):** Durch die räumliche Trennung von Pod 1 (Rahmen links / Koffer links) und Pod 2 (Rahmen rechts / Koffer rechts) über das metallische Fahrzeugchassis wird eine minimale Freiraumdämpfung von $> 35\,\text{dB}$ sichergestellt. Dies verhindert De-Sensing und HF-Intermodulation effektiv.
* **Deterministischer UWB Fahrzeug-Backbone (Qorvo DW3110 / 6.489 GHz Ch. 5):**
  * Drahtlose Verbindung zwischen Front-Knoten (`PCBA 05`) und Zentralbox (`PCBA 01`).
  * Vollständig konform mit **ETSI EN 302 065-1, EN 302 065-3** und **EU-Beschluss 2019/785** ($-41{,}3\,\text{dBm/MHz}$, kontinuierlicher legaler Sendebetrieb ohne Duty-Cycle-Beschränkung).
  * Arbeitet im Frequenzbereich 6.240–6.739 GHz (Mittenfrequenz 6.489 GHz) mit 499.2 MHz Bandbreite weitab von 2.4 GHz (WLAN, Bluetooth, Mesh) und 5.8 GHz.
  * **Antennenintegration:** Taoglas FXUWB10 Flex-Antenne montiert in einer $11 \times 11 \times 0{,}6\,\text{mm}$ Aussparung im Gehäuseboden (Unterwanne) von Zentralbox und Front-Knoten. Verbindung über 20 mm U.FL Mikro-Koax. Die PCB-Oberseite behält eine geschlossene Massefläche (Zero-Keepout), und der Gehäusedeckel kann ohne Kabelzug geöffnet werden.
* **LoRa 868 MHz (Semtech SX1262) auf der Zentralbox (`PCBA 01`):**
  * Direkt auf der Zentralbox integriert und 24/7 über die USV-Batterieschiene gepuffert für unterbrechungsfreie Diebstahl-Sentry und Gruppen-Telemetrie.
  * Taoglas FXP895 Flex-Antenne ($110 \times 20 \times 0{,}8\,\text{mm}$) in einer geschützten Tasche im Deckel der Zentralbox mit 50 $\Omega$ U.FL Speisung.
* **Multi-GNSS & Sensor-Koexistenz am Front-Knoten (`PCBA 05`):**
  * u-blox SAM-M10Q mit integrierter $15 \times 15\,\text{mm}$ Keramik-Patchantenne, angebunden über Qwiic I2C (`J12`) im kalten Fahrtwind-Staudruckbereich.
  * Koexistenz mit TI TMP117 ($\pm 0{,}1\,^\circ\text{C}$ Temperatur) und OPT3001 Umgebungslichtsensor ohne HF-Einstrahlung auf den GNSS-LNA.
* **Zentrale ePTFE-Druckausgleichsmembran:** $\varnothing\,7{,}0\,\text{mm}$ Gore/Schreiner Air Vent mittig auf dem Gehäusedach gleicht thermische Druckstöße symmetrisch aus, ohne das HF-Fernfeld zu verzerren.
* **Geschirmter HD26 SEAL-D Hauptkabelbaum:**
  * 4 Abzweige (Peitsche 1: Pod 1, Peitsche 2: Pod 2, Peitsche 4: Bordnetz, Peitsche 5: Heckradar).
  * 19 Pins aktiv belegt; Pins 9–11 unbeschaltet/Reserve.
  * Schirmung über $360^\circ$-Kontaktierung am metallischen HD26-Gehäuseflansch.

---

## 3. Schutzlackierung & Klimabeständigkeit (IPC-CC-830B)

### 3.1 Schutzlack-Spezifikation (Conformal Coating)
* **Material:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (gemessen auf planen Kupferflächen).
* **Durchschlagfestigkeit:** $> 60\,\text{kV/mm}$ (zuverlässiger Schutz vor Kriechströmen bei Betauung, Nebel und salzhaltigem Spritzwasser).

### 3.2 Maskierungszonen vor dem Lackierprozess
Folgende Bauteile und Kontaktflächen dürfen **nicht** beschichtet werden:
1. MicroSD-Kartenhalter-Kontakte (innenliegende Federzungen auf PCBA 01).
2. HD26 SEAL-D Flanschpins & M8-Steckverbinder-Kontakte.
3. J12 Qwiic I2C Buchsenkontakte auf PCBA 05.
4. USB-Buchsen (USB-A, USB-C) am Front-Knoten.
5. SMD-Testpunkte (TP_5V, TP_3V3, TP_GND).
6. Druckausgleichs-Bohrung der ePTFE-Membran.

---

## 4. Vibrations- & Schockfestigkeit (ISO 16750-3)

### 4.1 Schwingungsdämpfung am Motorrad
* **Platinenentkopplung:** 4x NBR-O-Ringe (Innendurchmesser 3,0 mm, Schnurstärke 1,0 mm) zwischen den Gehäusedomen und der PCB-Unterseite dämpfen hochfrequente Motorvibrationen.
* **Schraubensicherung:** Alle PCB-Befestigungsschrauben (M2,5) werden mit einem Drehmoment von $0{,}35\,\text{Nm}$ angezogen und mit mittelfestem Sicherungslack (blau, *Loctite 243*) gesichert.
* **Bauteilfixierung (Underfill / RTV-Silikon):**
  * **Bourns LM-NP-1001 Übertrager:** Ecken werden mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) gegen Rissbildung an SMD-Lötstellen gesichert.
  * **Pufferakku:** Fixierung in der Oberwanne auf dem Zwischenboden mit vibrationsdämpfendem $1{,}0\,\text{mm}$ Schaumpolster (*3M VHB 4910* / EPDM) und elastischem EPDM-Gummispannband (Shore 50A).
