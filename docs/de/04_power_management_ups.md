# 04 - Stromversorgung & USV

## 1. Primär-Schaltregler (Buck Converter)
* Texas Instruments LM5164 Synchronous Step-Down Regulator.
* Eingangsspannungsbereich: $6{,}0\,\text{V}$ bis $65\,\text{V}$ DC (Transientenschutz nach ISO 7637-2 bis $100\,\text{V}$).
* Ausgang: $5{,}0\,\text{V} / 1{,}0\,\text{A}$ für System, Pods und USV-Ladung.

## 2. Power-Path Management & USV
* Texas Instruments BQ24075 mit integriertem $1000\,\text{mAh}$ LiPo-Akku (unterbrechungsfreie Umschaltung $< 5\,\mu\text{s}$).
* Ermöglicht das kontrollierte Nachlaufen bei Zündung AUS (KL15 $< 11{,}8\,\text{V}$) für Tour-Finalisierung und WebDAV-Upload.

## 3. Schutzbeschaltung
* Überspannungsschutz: Littelfuse SMCJ36CA TVS-Diode ($36\,\text{V}$ Standoff).
* Verpolschutz: Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung (nahezu verlustfrei).