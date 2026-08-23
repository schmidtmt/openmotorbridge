# 04 - Stromversorgung, USV, Unterspannungsschutz & Winter-Erhaltung

## 1. Primaer-Schaltregler (Buck Converter)
- **Regler-IC:** Texas Instruments LM5164-Q1 Synchronous Step-Down Regulator (Automotive Grade AEC-Q100).
- **Eingangsspannungsbereich:** 6.0 V bis 65 V DC dauerhaft (Transientenschutz nach ISO 7637-2 bis 100 V).
- **Ausgangsleistung:** 5.0 V DC / 1.0 A Dauerstrom zur Versorgung des Systems, der Satelliten-Pods und des LiPo-Laders.
- **Wirkungsgrad:** > 88 % im Hauptlastbereich (12 V zu 5 V bei 400 mA).

## 2. Dynamisches Power-Path Management & Integrierte USV
- **Power-Path Controller:** Texas Instruments BQ24075 mit automatischer Last- und Ladestromaufteilung.
- **USV-Akkuzelle:** 1000 mAh Wide-Temperature Single-Cell LiPo-Akku (3.7 V Nennspannung, 4.2 V Ladeschluss, Entladebereich -20 °C bis +60 °C).
- **JEITA NTC-Thermomanagement (Murata 10k NTC an BQ24075 TS-Pin):**
  - **Kaeltestopp (T < 0 °C):** Ladestrom wird in Hardware auf 0 mA gestoppt (verhindert Lithium-Plating / Dendritenbildung im Winter). Das System wird normal ueber das Bordnetz versorgt.
  - **Hitzestopp (T > 45 °C):** Ladestrom wird auf 0 mA gestoppt (Schutz vor Akkublaehen durch Motorabwaerme unter der Sitzbank).
- **Unterbrechungsfreies Umschalten:** Beim Wegfall von KL15/KL30 schaltet der BQ24075 innerhalb von < 5 us ohne Spannungseinbruch am 3.3V-LDO (TPS7A05) auf den Akku um.
- **Nachlauf-Phase (Graceful Shutdown):** Ermoeglicht einen 60- bis 120-sekundigen Weiterbetrieb nach Zuendung AUS fuer:
  - Finalisierung und Flush des GPX-Dateisystems auf MicroSD.
  - Suche nach bekannten Heim-WLAN-SSIDs und Durchfuehrung des WebDAV-Uploads.
  - Geordnetes Senden von BLE-Disconnect-Events.

## 3. Kfz-Transienten-, EMV- & Verpolschutz
- **Eingangssicherung:** Bourns MF-MSMF050-2 Rueckstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
- **Ueberspannungs- & Spikeschutz:** Littelfuse SMBJ33CA Bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) -> Bietet dem 65V LM5164 Regler komfortable > 11.7 V Sicherheits-Headroom bei Load-Dump-Impulsen nach ISO 16750-2.
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem niedrigem Durchlasswiderstand (R_DS(on) < 25 mOhm).
- **Filterung:** Zweistufiger LC-PI-Filter (10 uH Shielded Automotive Inductor + 2x 10 uF X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

## 4. Bordbatterie-Ueberwachung, Unterspannungsschutz & Winter-Erhaltung

### 4.1 Spannungs-Messpfad & Batterie-Chemie
Die Bordnetzspannung an KL15 und KL30 wird ueber hochpraezise Spannungsteiler (100 kOhm / 10 kOhm, 0.1 % Toleranz, Teiler 1:11) an `PIN_ADC_VIGN` (GPIO 4) erfasst. Folgende 5 Batterietypen werden unterstuetzt:

| Batterietyp | Nennspannung | Ladeschluss (Motor AN) | Warnschwelle (Low-Bat) | Hard Cut-Off (Schutz) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Blei-Saeure (Nass)** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel-Batterie** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium-Eisenphosphat)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starterbatterie)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 4.2 Mehrstufige Abschalt-Logik (Anti-Tiefentladung)
1. **Stufe 1 - Normaler Ruhezustand (KL15 = AUS, KL30 > Schwelle):** ESP32-S3 im Light Sleep / Deep Sleep mit Wake-Up ueber GPIO-Pegelaenderung an KL15. Ruhestrom: < 1.2 mA.
2. **Stufe 2 - Low-Battery Deep Sleep (KL30 < Abschaltschwelle):** Deaktivierung aller Power-Gates und Wechsel in den ULP Deep Sleep (< 25 uA).
3. **Stufe 3 - Winter-Storage-Mode (Langzeit-Stillstand ueber Monate):** Nach > 14 Tagen Stillstand schaltet das System in den ULP-Minimalzustand, sodass die Starterbatterie auch ueber 5 bis 6 Monate Winterpause bei -20 °C nicht entladen wird.
