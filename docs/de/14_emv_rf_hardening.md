# 14 - EMV-, HF- & Umwelthärtung

## 1. Kfz-Transienten- und Überspannungsschutz
* **Bordnetz-Absicherung:** Konformität nach ISO 7637-2 (Pulse 1, 2a, 3a/b bis 100 V).
* **Überspannungsschutz:** Littelfuse SMCJ36CA TVS-Diode (36 V Standoff) am Eingang des LM5164 Schaltreglers.
* **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem niedrigem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
* **Entstörung:** Zweistufiger PI-Filter (Ferrit-Induktivität $10\,\mu\text{H}$ / 3 A + Keramikkondensatoren X7R) am 12V-Bordnetzeingang.

## 2. HF-Entkopplung & Raumdiversität
* **Koexistenz (2,4 GHz):** Durch die räumliche Trennung von Pod 1 (links) und Pod 2 (rechts) über das Fahrzeugchassis wird eine minimale Freiraumdämpfung von $> 35\,\text{dB}$ sichergestellt.
* **Kanalabschirmung:** Alle Zuleitungen (NF-Audio, UART, 1-Wire) sind über geschirmte Leitungen geführt; die Schirme liegen über niederinduktive Masseflächen am HD26-Stecker an.

## 3. Umweltschutz & Beschichtung
* **Vollverguss / Schutzlack:** Vollflächige Schutzlackierung aller Platinen nach IPC-CC-830B (Conformal Coating) gegen Feuchtigkeit, Salzsprühnebel und Kondenswasser.
* **Gehäuseschutz:** Zentralbox und Satelliten-Pods sind nach IP67 spezifiziert (geschlossenzellige Silikondichtungen, Gore-Druckausgleichselement Typ AVS 41).