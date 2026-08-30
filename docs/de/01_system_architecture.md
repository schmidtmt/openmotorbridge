# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

Dieses Dokument spezifiziert die übergeordnete Gesamtsystem-Architektur der **OpenMotorBridge v8.0**, die universelle 4-Punkte-Satelliten-Topologie, die flexiblen Montageoptionen (Helm- vs. Fahrzeugrahmen-Docking), die HF-Koexistenz sowie die nahtlose Integration in moderne OEM-Motorrad-Infotainmentsysteme.

---

## 1. Problemstellung & Architekturphilosophie

Klassische Motorrad-Kommunikationssysteme sind historisch stark fragmentiert:
* **Inkompatible Mesh-Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh und analoger PMR446-Funk können nicht direkt miteinander kommunizieren.
* **HF-Übersteuerungen & De-Sensing:** Der gleichzeitige Betrieb mehrerer 2,4-GHz-Mesh-Transceiver an einem einzigen Montagepunkt (z. B. am selben Helm oder in einer gemeinsamen Box) führt zu massiver Empfänger-Desensibilisierung (*De-Sensing*), Intermodulation und Reichweiteneinbrüchen von bis zu $80\,\%$.
* **Proprietäre Infotainment-Sperren:** Systeme wie Harley-Davidson Boom! Box GTS / Skyline OS oder BMW ConnectedRide verlangen teure, herstellereigene Schnittstellenmodule (z. B. HD WHIM), um Apple CarPlay oder Android Auto freizuschalten.

**OpenMotorBridge v8.0** löst diese Probleme durch eine modular entkoppelte **4-Punkte-Satelliten-Topologie** mit galvanisch getrenntem DSP-Audio-Routing:

```
                                  GESAMTSYSTEM-TOPOLOGIE
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. COCKPIT / LENKER (100 % Drahtlos):                                                       │
│    • BLE 5.0 Funk-Lenkertaster (CR2032 mit Batterie-Service 0x180F & PTT-Trigger)           │
│    • PWA Dashboard auf Smartphone / TFT via Web-Bluetooth (WebBLE)                          │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. ZENTRALE STEUERBOX (Unter der Sitzbank, IP67):                                           │
│    • ESP32-S3 Dual-Core MCU (240 MHz) • ES8388 Audio-Codec & DSP Audio-Mixer                │
│    • LM5164-Q1 72V Automotive Step-Down • BQ24075 USV & 1000mAh LiPo-Pufferakku             │
│    • 4-Bit High-Speed SDIO MicroSD-Ringspeicher • 2x Bourns 1500 V RMS Audio-Übertrager     │
└─┬─────────────────────────────────────────────────────────────────────────────────────────┬─┘
  │                                                                                         │
  ▼ Zentraler HD26-Flanschstecker (250 mm Y-Kabelbaumpeitsche)                              │
┌──────────────────────────────┬──────────────────────────────┬─────────────────────────────┤
│ 3. SATELLITEN-POD 1 (M8 6P): │ 4. SATELLITEN-POD 2 (M8 6P): │ 5. HECK-POD 3 (M8 6P):      │
│ • Universal Pod-Gehäuse      │ • Universal Pod-Gehäuse      │ • Universal Pod-Gehäuse     │
│ • Wechselschacht für Sena    │ • Wechselschacht für Cardo   │ • 1-Tier Monolith-Schlitten │
│   50S/60S/MeshPort-Kassette  │   Packtalk Edge / PMR446     │ • u-blox MAX-M10S Multi-GNSS│
│ • Helm- oder Rahmenmontage   │ • Helm- oder Rahmenmontage   │ • SX1262 LoRa 868MHz + C3   │
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. BORDNETZ-ANSCHLUSS: AMP Superseal 1.5 4-Pin (KL30 Dauerplus, KL15 Zündung, Masse)   │
  └─► 7. FRONT-ZWEIG: M8 4-Pin Buchse (Fahrzeug-CAN-Bus & IP67 Front-Ambient-Mikrofon)──────┘
```

---

## 2. Die universellen Montagekonzepte (Helm- vs. Rahmen-Docking)

Die Satelliten-Pods 1 und 2 sind mechanisch zu **100 % baugleich** und unterstützen zwei gleichberechtigte Montagephilosophien:

```
              OPTION A: HELM-DIREKTMONTAGE               OPTION B: FAHRZEUGRAHMEN-MONTAGE
         ┌─────────────────────────────────────┐      ┌─────────────────────────────────────┐
         │ • Pod 1 direkt am Fahrerhelm        │      │ • Pod 1 links an Tank/Rahmen        │
         │ • Pod 2 direkt am Soziushelm        │      │ • Pod 2 rechts an Heck/Sturzbügel   │
         │ • Pogo-Array dockt Headset am Helm  │      │ • Headsets verbleiben am Motorrad   │
         │ • 1 dünnes M8 Spiralkabel zum Bike  │      │ • Helm-Audio via BT oder Klinke     │
         └─────────────────────────────────────┘      └─────────────────────────────────────┘
```

### Option A: Helm-Direktmontage (Empfohlen für maximale Ergonomie)
* **Montage:** Der Pod wird mit der 3D-Druck-Helmklammer ([pod_mount_helmet_clamp.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/02_pod_base/pod_mount_helmet_clamp.scad)) direkt an der Helmschale befestigt (Klemmschuh oder 3M VHB Klebepad).
* **Vorteil:** Das Original-Headset (z. B. Sena 50S oder Cardo Packtalk Edge) sitzt in gewohnter Position am Helm. Seine vergoldeten OEM-Außenkontakte werden direkt vom Pogo-Pin-Array der Wechselkassette kontaktiert.
* **Verbindung:** Ein einziges, flexibles, geschirmtes M8 6-Pin Spiralkabel verbindet den Helm mit dem Motorrad-Kabelbaum.

### Option B: Fahrzeugrahmen-Montage (Komplett kabelfreier Helm)
* **Montage:** Pod 1 wird links am Fahrzeugrahmen/Seitendeckel und Pod 2 rechts am Rahmen montiert.
* **Vorteil:** Die Intercom-Geräte verbleiben dauerhaft und diebstahlgeschützt am Motorrad.
* **Helm-Kopplung:** Der Fahrerhelm verbindet sich drahtlos über Standard-Bluetooth mit dem System; die Intercom-Funkverbindung (Sena Mesh / Cardo DMC) wird über die fahrzeugfesten Pods abgewickelt.

---

## 3. HF-Koexistenz & Raumdiversität ($> 35\,\text{dB}$ Entkopplung)

Werden Sena- und Cardo-Mesh-Geräte gleichzeitig betrieben, muss eine gegenseitige Blockade der 2,4-GHz-Empfänger zuverlässig verhindert werden:

1. **Räumliche Distanzierung ($d \ge 45\,\text{cm}$):**
   * Bei Helm-Montage: Fahrerhelm (vorne/oben) und Soziushelm (hinten/oben) sind im Fahrbetrieb $50\dots 80\,\text{cm}$ voneinander entfernt.
   * Bei Rahmen-Montage: Pod 1 (linke Fahrzeugflanke) und Pod 2 (rechte Fahrzeugflanke) nutzen den massiven Motorradrahmen, Tank und Heckfender als metallische HF-Abschirmung.
2. **Schirmdämpfung:**
   * Die Freiraumdämpfung über $50\,\text{cm}$ in Kombination mit der metallischen Abschirmung durch den Fahrzeugrahmen erzielt eine **HF-Entkopplung von $> 35\,\text{dB}$**.
   * Damit sinkt der Einkopplungspegel des Nachbarsenders unter $-15\,\text{dBm}$, wodurch die Eingangs-LNAs beider Headsets im linearen Bereich arbeiten und kein *De-Sensing* auftritt.
3. **Tri-RF Architektur im Heck-Pod 3:**
   * Der Heck-Pod 3 vereint 2,4 GHz Mesh, 868 MHz LoRa und GNSS. Durch die $25 \times 25\,\text{mm}$ Groundplane der GNSS-Patchantenne und das $15 \times 8\,\text{mm}$ PCB-Keepout für die 2,4-GHz-Antenne ist eine gegenseitige Beeinflussung auf $< 0{,}2\,\text{dB}$ begrenzt.

---

## 4. Physische Schnittstellen & Signalmatrix

Die Verbindung aller Komponenten erfolgt über den zentralen HD26-Flansch an der Zentralbox:

| Zweig / Kabel | Anschlusstyp | Zielkomponente | Übertragene Signale |
| :--- | :--- | :--- | :--- |
| **Peitsche 1 (250 mm)** | M8 6-Pin A-kodiert (Buchse) | **Satelliten-Pod 1** (Fahrer) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Peitsche 2 (250 mm)** | M8 6-Pin A-kodiert (Buchse) | **Satelliten-Pod 2** (Sozius) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Peitsche 3 (250 mm)** | M8 6-Pin A-kodiert (Buchse) | **Heck-Pod 3** (OMM & GNSS) | UART_TX, UART_RX, 1-PPS_SYNC, 1-WIRE_ID, +5V_POD3, GND |
| **Peitsche 4 (250 mm)** | AMP Superseal 1.5 4-Pin | **12V Bordnetz** | KL30 (Dauerplus), KL15 (Zündung), GND (Power), GND (Sense) |
| **Peitsche 5 (250 mm)** | M8 4-Pin A-kodiert (Buchse) | **CAN-Bus & Front-Mic** | CAN_H, CAN_L, MIC_AMBIENT_IN, +3V3_MIC_BIAS |

---

## 5. Integration in OEM-Infotainmentsysteme

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS
* **WHIM-Emulation & Apple CarPlay / Android Auto:** 
  OpenMotorBridge emuliert an den Audio-Schnittstellen die elektrische Impedanz eines aktiven OEM-Headsets. Dadurch schaltet das Harley-Davidson Boom! Box GTS Infotainment Apple CarPlay und Android Auto im Display frei, **ohne dass das proprietäre HD-WHIM-Modul ($> 350\,\text{€}$) installiert werden muss**.
* **Nahtloses Ducking:** Navigationsansagen der Boom! Box werden über den ES8388 Codec priorisiert und über die aktiven Intercom-Gespräche mit einstellbarem Ducking ($-12\,\text{dB}$) sanft eingeblendet.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Echtzeit-Telemetrie:** Über den integrierten TCAN334G CAN-Transceiver lauscht die Zentralbox im Listen-Only-Modus auf dem Fahrzeugbus und erfasst Raddrehzahlen, Schräglage und Blinkersignale.
* **Display-Warnmeldungen:** Sinkt die Batteriespannung des BLE-Lenkertasters unter $2{,}3\,\text{V}$, wird eine Statusmeldung auf dem Motorrad-TFT-Display generiert (*"Lenkertaster-Batterie schwach - CR2032 wechseln"*).
