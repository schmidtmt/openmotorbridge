# 14 - EMV-, HF-, Vibrations- & Umwelthaertung

Dieses Dokument spezifiziert die Schutzschaltungen gegen Kfz-Bordnetz-Transienten (ISO 7637-2), die HF-Entkopplung im 2.4-GHz- und 868-MHz-Band, die Schutzlackierung nach IPC-CC-830B sowie die mechanische Vibrations- und Schockdaempfung nach ISO 16750-3.

---

## 1. Kfz-Transienten- und Ueberspannungsschutz (ISO 7637-2 & ISO 16750-2)

* **Bordnetz-Absicherung:** Vollstaendige Konformitaet nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V) und ISO 16750-2 Load-Dump.
* **Eingangssicherung:** Bourns MF-MSMF050-2 rueckstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
* **Ueberspannungsschutz:** Littelfuse SMBJ33CA bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) $\rightarrow$ bietet dem 65V LM5164 Regler komfortable $> 11{,}7\,\text{V}$ Sicherheitsabstand bei Load-Dumps.
* **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem geringem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Filterung & Entstoerung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor / 3 A + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 2. HF-Entkopplung & Raumdiversitaet

* **2,4-GHz-Koexistenz (Sena vs. Cardo):** Durch die raeumliche Trennung von Pod 1 (Rahmen links) und Pod 2 (Rahmen rechts) ueber das metallische Fahrzeugchassis wird eine minimale Freiraumdaempfung von $> 35\,\text{dB}$ sichergestellt. Dies verhindert De-Sensing und HF-Intermodulation effektiv.
* **868-MHz-Isolation:** Der SX1262 LoRa-Transceiver strahlt am Heckbuerzel (Pod 3) ab – $> 1{,}2\,\text{m}$ entfernt von den 2,4-GHz-Kassetten.
* **Geschirmte Zuleitungen:** Alle Zuleitungen (NF-Audio, High-Speed UART, 1-Wire) sind ueber 6-adrig geschirmte PUR-Kabel gefuehrt; die Gesamtschirme liegen ueber niederinduktive Masseflaechen am HD26-Flansch an.

---

## 3. Schutzlackierung & Klimabestaendigkeit (IPC-CC-830B)

### 3.1 Schutzlack-Spezifikation (Conformal Coating)
* **Material:** Modifizierter Polyurethan-Schutzlack (*Peters Elpeguard SL 1307 FLZ* oder *Electrolube UR5041*).
* **Schichtdicke:** $40\,\mu\text{m}$ bis $60\,\mu\text{m}$ (gemessen auf planen Kupferflaechen).
* **Durchschlagfestigkeit:** $> 60\,\text{kV/mm}$ (zuverlaessiger Schutz vor Kriechstroemen bei Betauung, Nebel und salzhaltigem Spritzwasser).

### 3.2 Maskierungszonen vor dem Lackierprozess
Folgende Bauteile und Kontaktflaechen duerfen **nicht** beschichtet werden:
1. MicroSD-Kartenhalter-Kontakte (innenliegende Federzungen).
2. 2x13 Wannenstecker (J1) & externe HD26-Flanschpins.
3. Mill-Max 6-Pin Pogo-Kontakt-Pads an den Kassetten und Pods.
4. SMD-Testpunkte (TP_5V, TP_3V3, TP_GND).
5. Druckausgleichs-Bohrung des M8 ePTFE-Ventils.

---

## 4. Vibrations- & Schockfestigkeit (ISO 16750-3)

### 4.1 Schwingungsdaempfung am Motorrad
* **Platinenentkopplung:** 4x NBR-O-Ringe (Innendurchmesser 3,0 mm, Schnurstaerke 1,0 mm) zwischen den Gehaeusedomen und der PCB-Unterseite daempfen hochfrequente Motorvibrationen.
* **Schraubensicherung:** Alle PCB-Befestigungsschrauben (M2,5) werden mit einem Drehmoment von $0{,}35\,\text{Nm}$ angezogen und mit mittelfestem Sicherungslack (blau, *Loctite 243*) gesichert.
* **Bauteilfixierung (Underfill / RTV-Silikon):**
  * **Bourns LM-NP-1001 Uebertrager:** Ecken werden mit elastischem Silikonkleber (*Dow Corning 732* / *Dowsil 3145*) gegen Rissbildung an SMD-Loetstellen gesichert.
  * **Pufferakku:** Vollflaechige Fixierung in der Oberwanne mit vibrationsdaempfendem $1{,}0\,\text{mm}$ Acrylat-Schaumklebeband (*3M VHB 4910*).
