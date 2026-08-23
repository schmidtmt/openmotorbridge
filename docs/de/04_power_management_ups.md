# 04 - Stromversorgung, USV, Unterspannungsschutz, Winter-Erhaltung & Taster-Batterie

Dieses Dokument spezifiziert das dynamische Energiemanagement (LM5164 Buck + BQ24075 USV), den JEITA-Akkuschutz, den mehrstufigen Starterbatterie-Entladeschutz (Winter-Hibernate $< 20\,\mu\text{A}$) sowie die **zyklische CR2032-Batterieueberwachung des Lenkertasters**.

---

## 1. Primaer-Schaltregler (Buck Converter)
- **Regler-IC:** Texas Instruments LM5164-Q1 Synchronous Step-Down Regulator (Automotive Grade AEC-Q100).
- **Eingangsspannungsbereich:** 6.0 V bis 65 V DC dauerhaft (Transientenschutz nach ISO 7637-2 bis 100 V).
- **Ausgangsleistung:** 5.0 V DC / 1.0 A Dauerstrom zur Versorgung des Systems, der Satelliten-Pods und des LiPo-Laders.
- **Wirkungsgrad:** > 88 % im Hauptlastbereich (12 V zu 5 V bei 400 mA).

---

## 2. Dynamisches Power-Path Management & Integrierte USV
- **Power-Path Controller:** Texas Instruments BQ24075 mit automatischer Last- und Ladestromaufteilung.
- **USV-Akkuzelle:** 1000 mAh Wide-Temperature Single-Cell LiPo-Akku (3.7 V Nennspannung, 4.2 V Ladeschluss, Entladebereich -20 °C bis +60 °C).
- **JEITA NTC-Thermomanagement (Murata 10k NTC an BQ24075 TS-Pin):**
  - **Kaeltestopp (T < 0 °C):** Ladestrom wird in Hardware auf 0 mA gestoppt (verhindert Lithium-Plating / Dendritenbildung im Winter). Das System wird normal ueber das Bordnetz versorgt.
  - **Hitzestopp (T > 45 °C):** Ladestrom wird auf 0 mA gestoppt (Schutz vor Akkublaehen durch Motorabwaerme unter der Sitzbank).
- **Unterbrechungsfreies Umschalten:** Beim Wegfall von KL15/KL30 schaltet der BQ24075 innerhalb von < 5 us ohne Spannungseinbruch am 3.3V-LDO (TPS7A05) auf den Akku um.
- **Nachlauf-Phase (Graceful Shutdown):** Ermoeglicht einen Weiterbetrieb nach Zuendung AUS fuer:
  - Finalisierung und Flush des GPX-Dateisystems auf MicroSD.
  - Suche nach bekannten Heim-WLAN-SSIDs und Durchfuehrung des WebDAV-Uploads.
  - Geordnetes Senden von BLE-Disconnect-Events.

---

## 3. Kfz-Transienten-, EMV- & Verpolschutz
- **Eingangssicherung:** Bourns MF-MSMF050-2 Rueckstellbare PPTC-Sicherung (1812 SMD, 500 mA Hold / 1.0 A Trip).
- **Ueberspannungs- & Spikeschutz:** Littelfuse SMBJ33CA Bidirektionale TVS-Diode (33 V Standoff, 53.3 V max Clamping) $\rightarrow$ Bietet dem 65V LM5164 Regler komfortable $> 11{,}7\,\text{V}$ Sicherheits-Headroom bei Load-Dump-Impulsen nach ISO 16750-2.
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET in der Masseleitung mit extrem niedrigem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **Filterung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 4. Bordbatterie-Ueberwachung & Mehrstufige Schlafmodi

### 4.1 Spannungs-Messpfad & Batterie-Chemie
Die Bordnetzspannung an KL15 und KL30 wird ueber hochpraezise Spannungsteiler (100 kOhm / 10 kOhm, 0.1 % Toleranz, Teiler 1:11) an `PIN_ADC_VIGN` (GPIO 4) erfasst:

| Batterietyp | Nennspannung | Ladeschluss (Motor AN) | Warnschwelle (Low-Bat) | Hard Cut-Off (Schutz) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Blei-Saeure (Nass)** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel-Batterie** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium-Eisenphosphat)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starterbatterie)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 4.2 Mehrstufige 3-Stufen-Abschaltkaskade (Winterschlaf-Modus)

```
┌─────────────────────────────────────────────────────────────┐
│          3-STUFIGE POWER-DOWN KASKADE BEI ZUENDUNG AUS      │
├─────────────────────────────────────────────────────────────┤
│ 1. NACHLAUF (0..15 Min): WebDAV-Upload & GPX Flush (45 mA)  │
│ 2. DEEP SLEEP (15 Min..72 h): Ext-Interrupt KL15 (< 100 µA) │
│ 3. WINTER-HIBERNATE (> 72 h): ULP-Tiefschlaf (< 20 µA)      │
└─────────────────────────────────────────────────────────────┘
```

1. **Stufe 1 - Aktiver Nachlauf (0 bis 15 Minuten, $45\,\text{mA}$):**
   * Zündung (KL15) ist ausgeschaltet, System schließt GPX-Logs, führt WebDAV-Sync durch und trennt Bluetooth sauber.
2. **Stufe 2 - Standby Deep Sleep (15 Minuten bis 72 Stunden, $< 100\,\mu\text{A}$):**
   * Alle DC/DC-Lasten und Peripherie-Gitter sind stromlos. Der ESP32-S3 wacht blitzschnell ($< 5\,\text{ms}$) auf, sobald KL15 wieder HIGH wird.
3. **Stufe 3 - Ultra-Low-Power Hibernate (> 72 Stunden Stillstand, $< 20\,\mu\text{A}$):**
   * Schützt die Starterbatterie über 6 bis 12 Monate Winterpause vor Tiefentladung (Verlust $< 1{,}5\,\%$ der Nennkapazität pro Jahr), selbst wenn kein Erhaltungsladegerät angeschlossen ist.

---

## 5. Lenkertaster CR2032-Batterieueberwachung (BLE Service 0x180F)

Der drahtlose Bluetooth-Lenkertaster sendet seinen Batterieladezustand zyklisch ueber den standardisierten **Bluetooth SIG Battery Service (`UUID 0x180F`)** an die Zentralbox:

```
┌──────────────┬───────────────┬──────────────────────────────────────────────┐
│ Batteriestand│ Spannung CR2032│ System-Reaktion & Warnstufe                  │
├──────────────┼───────────────┼──────────────────────────────────────────────┤
│ **> 20 %**   │ > 2.5 V       │ Normalbetrieb (Grüne Anzeige im WebApp Dash) │
│ **≤ 15 %**   │ ≤ 2.3 V       │ **Gelbe Frühwarnung:** Status-LED Wechsel-   │
│              │               │ blitz Gelb-Rot • WebApp Push-Notification    │
│              │               │ • CAN-Bus Warnung an Motorrad-TFT-Display    │
│ **≤ 5 %**    │ ≤ 2.0 V       │ **Kritischer Alarm:** Rote Dauerwarnung      │
└──────────────┴───────────────┴──────────────────────────────────────────────┘
```

### 5.1 CAN-Bus Display-Integration
Ist die OpenMotorBridge an den Fahrzeug-CAN angebunden (z. B. Harley-Davidson Skyline OS / Boom! Box oder BMW Connected TFT), wird bei $V_{\text{CR2032}} \le 2{,}3\,\text{V}$ ein informatives Display-Pop-up generiert (*"Lenkertaster-Batterie schwach - bitte CR2032 wechseln"*).
