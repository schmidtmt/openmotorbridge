# 05 - Energie-Management, USV & Kfz-Bordnetzschutz

Dieses Dokument spezifiziert das dynamische Energie- und Schutzmanagement der OpenMotorBridge v8.0: die primären Schaltregler (Zentralbox LM5164-Q1 & Front-Knoten LMR36015), die unterbrechungsfreie Stromversorgung (USV mit BQ24075 und 1000 mAh LiPo), den automobilen Transienten- und Verpolschutz (ISO 7637-2), das intelligente **Dongle-Powermanagement (1-Klick Kaltstart & Auto-Café Mode)** sowie die mehrstufige Winterschlaf-Kaskade (< 16,5 µA).

---

## 1. Primär-Schaltregler der Baugruppen

Um hohe Wirkungsgrade bei minimaler Eigenerwärmung im geschlossenen IP67-Gehäuse zu erzielen, arbeiten Zentralbox und Front-Knoten mit hochintegrierten synchronen Abwärtswandlern:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DCDC WANDLER-ARCHITEKTUR IM SYSTEM                       │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. ZENTRALBOX (PCBA 01): LM5164-Q1   │ 2. FRONT-KNOTEN (PCBA 05): LMR36015  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Weitbereichseingang: 6.0 V - 65 V  │ • Eingangsspannung: 4.2 V - 36 V     │
│ • Ausgang: 5.0 V DC / 1.0 A Dauer    │ • Ausgang: 5.0 V DC / 2.0 A Dauer    │
│ • Wirkungsgrad: > 88 % bei Volllast  │ • Wirkungsgrad: 91.8 % bei 2.0 A     │
│ • Transientenschutz bis 100 V        │ • Restwelligkeit: 5.3 mVpp           │
│ • Versorgt: MCU, Audio, USV, Pod 1-3 │ • Versorgt: ESP32-C3, USB-Hub, VBUS  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Dynamisches Power-Path Management & Integrierte USV

- **Power-Path Controller:** Texas Instruments **BQ24075** mit automatischer Last- und Ladestromaufteilung.
- **USV-Akkuzelle:** 1000 mAh Wide-Temperature Single-Cell LiPo-Akku ($3{,}7\,\text{V}$ Nennspannung, $4{,}2\,\text{V}$ Ladeschluss, Entladebereich $-20\,^\circ\text{C}$ bis $+60\,^\circ\text{C}$).
- **JEITA NTC-Thermomanagement (Murata 10k NTC an BQ24075 TS-Pin):**
  - **Kältestopp ($T < 0\,^\circ\text{C}$):** Ladestrom wird in Hardware auf $0\,\text{mA}$ gestoppt (verhindert Lithium-Plating / Dendritenbildung im Winter). Das System wird normal über das Bordnetz versorgt.
  - **Hitzestopp ($T > 45\,^\circ\text{C}$):** Ladestrom wird auf $0\,\text{mA}$ gestoppt (Schutz vor Akkublähen durch Motorabwärme unter der Sitzbank).
- **Unterbrechungsfreies Umschalten bei Kaltstart (Cranking):**  
  Bricht die Bordnetzspannung beim Anlassen schwerer V2-Motoren kurzzeitig auf $6{,}5\,\text{V}$ ein, schaltet der BQ24075 in $< 5\,\mu\text{s}$ ohne jeglichen Spannungseinbruch auf den internen Pufferakku um. Audio-Streams, Funk-Mesh und GNSS-Tracking laufen unterbrechungsfrei weiter!
- **Nachlauf-Phase (Graceful Shutdown):** Ermöglicht einen Weiterbetrieb nach Zündung AUS für:
  - Finalisierung und Flush des GPX-Dateisystems auf die MicroSD-Karte.
  - Suche nach bekannten Heim-WLAN-SSIDs und Durchführung des WebDAV-Uploads.
  - Geordnetes Senden von BLE-Disconnect-Events.

---

## 3. Kfz-Transienten-, EMV- & Verpolschutz (ISO 7637-2 & ISO 16750-2)

- **Eingangssicherung:** Bourns MF-MSMF050-2 Rückstellbare PPTC-Sicherung (1812 SMD, $500\,\text{mA}$ Hold / $1{,}0\,\text{A}$ Trip).
- **Überspannungs- & Spikeschutz:** Littelfuse SMBJ33CA Bidirektionale TVS-Diode ($33\,\text{V}$ Standoff, $53{,}3\,\text{V}$ max Clamping). Bietet dem 65V-LM5164-Regler komfortable $> 11{,}7\,\text{V}$ Sicherheits-Headroom bei Load-Dump-Impulsen nach ISO 16750-2 (Impuls 5b bis $87\,\text{V}$).
- **Verpolschutz:** Diodes Inc. DMP6023L P-Kanal MOSFET mit extrem niedrigem Durchlasswiderstand ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **Filterung:** Zweistufiger LC-PI-Filter ($10\,\mu\text{H}$ Shielded Automotive Inductor + 2x $10\,\mu\text{F}$ X7R 100V Keramikkondensatoren) am KL30/KL15-Eingang.

---

## 4. Front-Knoten VBUS Lastschalter & Ottocast Power-Management

Der Universal Front-Knoten verfügt über ein intelligentes Energiemanagement für externe Wireless CarPlay / Android Auto Dongle (*Ottocast / CarlinKit*):

```
                   FRONT-KNOTEN OTTOCAST POWER-GATE
┌────────────────────────────┐              ┌────────────────────────────┐
│ 12V Bordnetz (KL15 Zündung)│              │ ESP32-C3 Firmware          │
│ • Scheinwerfer / Zubehör   │              │ • 1-Click Reboot Listener  │
└─────────────┬──────────────┘              │ • Auto-Café 60s Countdown  │
              │                             └─────────────┬──────────────┘
              ▼                                           │ GPIO 1 (EN)
┌────────────────────────────┐                            │
│ TI LMR36015 Buck (5.00V)   │                            ▼
│ • 91.8 % Wirkungsgrad      ├─────────────►┌────────────────────────────┐
│ • 5.3 mVpp Restwelligkeit  │              │ TI TPS2051B Load Switch    │
└────────────────────────────┘              │ • 1.05A Current Clamp      │
                                            │ • 6.5 µs Fault Trip        │
                                            │ • 0.42A Soft-Start Inrush  │
                                            └─────────────┬──────────────┘
                                                          │ 5.0V VBUS
                                                          ▼
                                            ┌────────────────────────────┐
                                            │ Ottocast CarPlay Adapter   │
                                            │ • USB-A Buchse Port 1      │
                                            └────────────────────────────┘
```

### 4.1 1-Klick Dongle Kaltstart (Hard Reset via PWA)
Hängt sich der drahtlose CarPlay-Adapter auf, muss der Fahrer nicht mehr anhalten und den USB-Stecker ziehen:
* Ein Klick auf den Button **"CarPlay 1-Klick Kaltstart"** im WebApp-Dashboard sendet den Befehl `PKT_TYPE_CMD_POWER_CYCLE` über ESP-NOW an den Front-Knoten.
* Der ESP32-C3 zieht den Enable-Pin des TPS2051B für exakt $2{,}5\,\text{Sekunden}$ auf LOW.
* Der Dongle wird vollständig spannungsfrei geschaltet ($0{,}00\,\text{V}$) und startet anschließend frisch durch.

### 4.2 Auto-Café Modus: 60s WLAN-Freigabe bei Zündung AUS
* **Problem:** Wireless-CarPlay-Dongles spannen ein 5-GHz-WLAN auf, mit dem das Smartphone dauerhaft gekoppelt bleibt. Schaltet der Fahrer die Zündung ab und betritt ein Café, versucht das Telefon weiterhin Daten über das Dongle-WLAN zu routen $\rightarrow$ kein Internetzugriff im Café!
* **OpenMotorBridge Lösung:** 
  * Erkennt der Controller das Abfallen von KL15 (Zündung AUS), startet ein interner $60\,\text{s}$ Countdown.
  * Nach Ablauf trennt der TPS2051B die VBUS-Versorgung des Dongles komplett ab.
  * Das Smartphone verbindet sich sofort reibungslos mit dem Café-WLAN oder Mobilfunknetz.
  * Bei Wiedereinschalten der Zündung schaltet der Port in $< 10\,\text{ms}$ wieder ein.

---

## 5. Bordbatterie-Überwachung & 3-Stufen Winterschlaf-Kaskade

Die Bordnetzspannung an KL15 und KL30 wird über hochpräzise Spannungsteiler ($100\,\text{k}\Omega / 10\,\text{k}\Omega$, $0{,}1\,\%$ Toleranz) an `PIN_ADC_VIGN` erfasst:

### 5.1 Starterbatterie-Schutzschwellen

| Batterietyp | Nennspannung | Ladeschluss (Motor AN) | Warnschwelle (Low-Bat) | Hard Cut-Off (Schutz) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Blei-Säure (Nass)** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel-Batterie** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium-Eisenphosphat)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starterbatterie)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 5.2 3-Stufen Abschaltkaskade

```
┌─────────────────────────────────────────────────────────────┐
│          3-STUFIGE POWER-DOWN KASKADE BEI ZÜNDUNG AUS       │
├─────────────────────────────────────────────────────────────┤
│ 1. NACHLAUF (0..15 Min): WebDAV-Upload & GPX Flush (45 mA)  │
│ 2. DEEP SLEEP (15 Min..72 h): Ext-Interrupt KL15 (< 100 µA) │
│ 3. WINTER-HIBERNATE (> 72 h): ULP-Tiefschlaf (< 16.5 µA)    │
└─────────────────────────────────────────────────────────────┘
```

* **Stufe 3 - ULP-Hibernate:** Schützt die Starterbatterie über 6 bis 12 Monate Winterpause vor Tiefentladung (Verlust $< 1{,}5\,\%$ der Nennkapazität pro Jahr), selbst wenn kein Erhaltungsladegerät angeschlossen ist.

---

## 6. Lenkertaster CR2032-Batterieüberwachung (BLE Service 0x180F)

Der drahtlose Bluetooth-Lenkertaster sendet seinen Batterieladezustand zyklisch über den standardisierten **Bluetooth SIG Battery Service (`UUID 0x180F`)** an die Zentralbox:

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
