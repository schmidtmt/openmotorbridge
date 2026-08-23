# 14 - EMV-, HF- & Umwelthaertung

## 1. Kfz-Transienten- und Ueberspannungsschutz
- **Bordnetz-Absicherung:** Konformitaet nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V).
- **Ueberspannungsschutz:** Littelfuse SMCJ36CA TVS-Diode (36 V Standoff) am Eingang des LM5164 Schaltreglers.
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung (R_DS(on) < 25 mOhm).
- **Entstoerung:** Zweistufiger PI-Filter (Ferrit-Induktivitaet 10 uH / 3 A + Keramikkondensatoren X7R) am 12V-Bordnetzeingang.

## 2. HF-Entkopplung & Raumdiversitaet
- Durch die raeumliche Trennung von Pod 1 (links) und Pod 2 (rechts) ueber das Fahrzeugchassis wird eine minimale Freiraumdaempfung von > 35 dB sichergestellt.
- Alle Zuleitungen (NF-Audio, UART, 1-Wire) sind ueber geschirmte Leitungen gefuehrt; Schirme liegen ueber niederinduktive Masseflaechen am HD26-Stecker an.

## 3. Umweltschutz & Beschichtung
- Vollflaechige Schutzlackierung aller Platinen nach IPC-CC-830B (Conformal Coating) gegen Feuchtigkeit und Salzspruehnebel.
- Gehaeuse nach IP67 spezifiziert mit Gore-Druckausgleichselement Typ AVS 41.
