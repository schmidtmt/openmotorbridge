# 12 - EMV-Härtung, Schirmung & ESD-Schutz

Dieses Dokument spezifiziert die Schutzschaltungen gegen Kfz-Bordnetz-Transienten (ISO 7637-2), die HF-Entkopplung im 2.4-GHz- und 868-MHz-Band, die Schutzlackierung nach IPC-CC-830B sowie die mechanische Vibrations- und Schockdämpfung nach ISO 16750-3.

---

## 1. Kfz-Transienten- und Überspannungsschutz (ISO 7637-2 & ISO 16750-2)

* **Bordnetz-Absicherung:** Vollständige Konformität nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V) und ISO 16750-2 Load-Dump.
* **Eingangssicherung:** Bourns MF-MSMF050-2 rückstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
* **Überspannungsschutz:** Littelfuse SMBJ33CA bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) $\rightarrow$ bietet dem 65V LM5164 Regler komfortable $> 11{,}7\,\text{V}$ Sicherheitsabstand bei Load-Dumps.
* **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem geringem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Filterung & Entstörung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor / 3 A + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 2. HF-Entkopplung & Raumdiversität

* **2,4-GHz-Koexistenz (Sena vs. Cardo):** Durch die räumliche Trennung von Pod 1 (Rahmen links) und Pod 2 (Rahmen rechts) über das metallische Fahrzeugchassis wird eine minimale Freiraumdämpfung von $> 35\,\text{dB}$ sichergestellt. Dies verhindert De-Sensing und HF-Intermodulation effektiv.
* **Heck-Pod 3 Antennen-Architektur (Tri-RF Layout):**
  * **2.4 GHz ESP32-C3 PCB-Antenne:** Platziert am vorderen Platinenrand in einer $15 \times 8\,\text{mm}$ Kupfer- und Bauteil-Freihaltezone (Keepout Area) ohne Masseflächen auf allen 4 Lagen.
  * **868 MHz LoRa-Wendelantenne:** Seitlich/hinten montiert mit dedizierter $50\,\Omega$ Microstrip-Speisung und symmetrischer $60 \times 36\,\text{mm}$ Groundplane für optimalen Wirkungsgrad ($> -1{,}5\,\text{dBi}$).
  * **u-blox Multi-GNSS Keramik-Patchantenne ($25 \times 25 \times 4\,\text{mm}$):** Zentriert mit ungehindertem $180^\circ$-Halbkugel-Himmelsblick nach oben durch die funktransparente PA12-Gehäusedecke ($3{,}0\,\text{mm}$ Wandstärke, $\varepsilon_r \approx 3{,}2$).
* **Zentrale ePTFE-Druckausgleichsmembran:** $\varnothing\,7{,}0\,\text{mm}$ Gore/Schreiner Air Vent mittig auf dem Pod-Dach gleicht thermische Druckstöße symmetrisch aus, ohne das HF-Fernfeld zu verzerren.
* **Geschirmte Zuleitungen:** Alle Zuleitungen (NF-Audio, High-Speed UART, 1-Wire) sind über 6-adrig geschirmte PUR-Kabel geführt; die Gesamtschirme liegen über niederinduktive Masseflächen am M8-Metallflansch und HD26-Flansch an.

---

## 3. Schutzlackierung & Klimabeständigkeit (IPC-CC-830B)

### 3.1 Schutzlack-Spezifikation (Conformal Coating)
* **Material:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (gemessen auf planen Kupferflächen).
* **Durchschlagfestigkeit:** $> 60\,\text{kV/mm}$ (zuverlässiger Schutz vor Kriechströmen bei Betauung, Nebel und salzhaltigem Spritzwasser).

### 3.2 Maskierungszonen vor dem Lackierprozess
Folgende Bauteile und Kontaktflächen dürfen **nicht** beschichtet werden:
1. MicroSD-Kartenhalter-Kontakte (innenliegende Federzungen).
2. 2x13 Wannenstecker (J1) & externe HD26-Flanschpins.
3. Mill-Max 6-Pin Pogo-Kontakt-Pads an den Kassetten und Pods.
4. SMD-Testpunkte (TP_5V, TP_3V3, TP_GND).
5. Druckausgleichs-Bohrung des M8 ePTFE-Ventils.

---

## 4. Vibrations- & Schockfestigkeit (ISO 16750-3)

### 4.1 Schwingungsdämpfung am Motorrad
* **Platinenentkopplung:** 4x NBR-O-Ringe (Innendurchmesser 3,0 mm, Schnurstärke 1,0 mm) zwischen den Gehäusedomen und der PCB-Unterseite dämpfen hochfrequente Motorvibrationen.
* **Schraubensicherung:** Alle PCB-Befestigungsschrauben (M2,5) werden mit einem Drehmoment von $0{,}35\,\text{Nm}$ angezogen und mit mittelfestem Sicherungslack (blau, *Loctite 243*) gesichert.
* **Bauteilfixierung (Underfill / RTV-Silikon):**
  * **Bourns LM-NP-1001 Übertrager:** Ecken werden mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) gegen Rissbildung an SMD-Lötstellen gesichert.
  * **Pufferakku:** Fixierung in der Oberwanne auf dem Zwischenboden mit vibrationsdämpfendem $1{,}0\,\text{mm}$ Schaumpolster (*3M VHB 4910* / EPDM) und elastischem EPDM-Gummispannband (Shore 50A).
