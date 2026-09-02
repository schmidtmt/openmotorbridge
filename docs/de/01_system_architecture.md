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
  ├─► 7. HECK-SENSOR-ZWEIG: M8 4-Pin Buchse (Heck-Radar / Totwinkel-Sensor / lokaler OBD2)──┤
  │                                                                                         │
  ▼ 2.4 GHz Ultra-Low-Latency Funkverbindung (ESP-NOW < 3ms & BLE 5.0 2M-PHY)               │
┌───────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. COCKPIT-SUBSYSTEM: Wireless Smart Fairing & 4-Port Power Hub (Frontverkleidung)        │
│ • 4-Port High-Power DCDC USB-Hub (2x USB-C PD, 2x USB-A für Phone, Cam, Navi, Intern)    │
│ • Digitales I2S-MEMS Ambient-Mikrofon mit ePTFE-Membran (Edge-RMS-Schallpegelmessung)     │
│ • Direkter kabelgebundener Lenker-PTT-Tastereintritt (GPIO-Interrupt, 100% batteriefrei)  │
│ • Optionaler Front-CAN-Transceiver (für Bikes mit CAN in Verkleidung / TFT-Cockpit)       │
│ • Einzige fahrzeugseitige Zuleitung: Robuste 2-adrige 12V-Bordnetzspeisung (kein Buskabel)│
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Die universellen Montagekonzepte (Helm- vs. Rahmen-Docking)

## 2. Universelles Montagekonzept (Fahrzeugrahmen-, Sturzbügel- & Rohrbett-Montage)

Die Satelliten-Pods 1, 2 und 3 sind mechanisch zu **100 % baugleich** und für die werkzeuglose Schnellmontage an allen gängigen Motorrad-Rohrdurchmessern und Flachstellen ausgelegt:

```
          UNIVERSELLE RAHMEN- & ROHRBETT-MONTAGE (100% KABELFREIER HELM)
          ┌─────────────────────────────────────────────────────────────┐
          │ • Integrierte V-Nut / Hohlkehle an der Pod-Unterseite       │
          │ • Passend für Rohre von Ø 18 mm bis Ø 35 mm (1" / 1 1/8")   │
          │ • 4x Einhängenasen für 2x wetterfeste EPDM-Spannringe       │
          │ • 100% werkzeuglose Montage in 5 Sekunden ohne Lackschäden  │
          │ • Pod 1 links am Rahmen / Sturzbügel (Fahrer-Mesh)          │
          │ • Pod 2 rechts am Rahmen / Sturzbügel (Sozius-Mesh)         │
          │ • Pod 3 am Heckrahmen / Gepäckträger (OMM Dual-PHY & GNSS)  │
          └──────────────────────────────┬──────────────────────────────┘
                                         │
                                         ▼ Bluetooth A2DP / HFP / LE Audio
          ┌─────────────────────────────────────────────────────────────┐
          │ FAHRER- & SOZIUS-HELME (100% Kabellos & Leicht):            │
          │ • Kein schweres Zusatzgehäuse am Helm (0g Zusatzgewicht)    │
          │ • Keine störenden Spiralkabel oder flatternden Leitungen    │
          │ • Fahrer nutzt normales OEM-Headset / integrierte Lautspr.  │
          │ • Zentralbox streamt gemischtes Audio kabellos an die Helme │
          └─────────────────────────────────────────────────────────────┘
```

### 2.1 Montage am Fahrzeug (Sturzbügel, Rahmenunterzug, Heckbrücke)
* **Universal-Prisma (V-Nut):** An der Unterseite jedes Pod-Gehäuses ist eine $120^\circ$-Prismenkehle ($R = 15\,\text{mm}$) angeformt. Sie schmiegt sich formschlüssig an alle typischen Motorrad-Rohre an:
  * $\varnothing 22\,\text{mm}$ ($7/8"$ Standard-Lenker und Rahmenstreben)
  * $\varnothing 25{,}4\,\text{mm}$ ($1"$ Sturzbügel und Harley-Rahmenrohre)
  * $\varnothing 28{,}6\,\text{mm}$ ($1\,1/8"$ Fatbar- & Enduro-Rahmen)
  * $\varnothing 32\,\text{mm}$ ($1\,1/4"$ Custom-Sturzbügel)
  * **Flache Montage:** Liegt auf ebenen Flächen (unter der Sitzbank / am Seitendeckel) kippstabil auf den Außenstegen auf.
* **EPDM-Spannring-Befestigung:** Zwei UV-beständige EPDM-Gummispannringe (oder Silikon-Leiterbänder) werden um das Rahmenrohr gezogen und in die 4 seitlichen Einhängenasen eingehängt. Das dämpft gleichzeitig hochfrequente Motorvibrationen ab.
* **Dauerhafte Diebstahlsicherung:** Durch die integrierten $5{,}0 \times 2{,}5\,\text{mm}$ Durchgangsschlitze können alternativ Standard-Kabelbinder ($4{,}8\,\text{mm}$) oder Edelstahl-Schlauchschellen gezogen werden.

### 2.2 Kabelloser Helm-Komfort
* Die schweren Intercom-Geräte (Sena 50S / Cardo Edge) verbleiben wetter- und diebstahlgeschützt an den Motorrad-Pods.
* Die Helme von Fahrer und Sozius bleiben zu $100\,\%$ leicht, aerodynamisch original und frei von Kabeln. Die Audio-Ein- und Ausgabe erfolgt vollkommen drahtlos über die integrierte Bluetooth-Schnittstelle der Zentralbox.

### 2.3 Universelle OEM-Adapter-Kompatibilität (Off-the-Shelf)
Die erweiterten Pod-Kassetten ($110 \times 54 \times 28\,\text{mm}$ Innenraum) nehmen alle handelsüblichen OEM-Geräte im ungeöffneten Originalzustand auf:
* **Klasse A (Drahtlos-Bridges & USB-Speisung):** z. B. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red – versorgt über flaches 90° Micro-USB/USB-C Kabel, drahtlose Audioübertragung zum Helm, externe SMA-Bulkhead-Doppelbuchse mit Schutzkappe an der Frontblende.
* **Klasse B (Pogo-Pin Federkontakt-Cradles):** z. B. Sena 50S/60S/30K/20S EVO – vollwertiges analoges Audio (ES8388 Codec) und TLP222A PTT-Synthese.
* **Klasse C (Magnetischer Air-Mount):** z. B. Cardo Packtalk Edge/Pro/Neo – werkzeugloses magnetisches Andocken über 2x N52 Neodym-Magnete.
* **Klasse D (Schiebe-Cradles):** z. B. Cardo Packtalk Bold/Black, Freecom-Serie – mechanische Gleitschiene mit Arretierfeder.
* **Klasse E (Analoger PMR446 Funk):** z. B. Midland G7/G9 Pro, XT30, Kenwood – 2-Pin Doppelklinkenanschluss mit PhotoMOS-PTT-Tastung.
*(Detaillierte Verkabelungsmatrix siehe [Spezifikation 06, Abschnitt 8](file:///Users/schmidtm/openMotorBridge/docs/de/06_dynamic_profiles_spec.md#8-systematik-der-oem-adapter-anbindung-anschluss-klassen--verkabelungs-matrix)).*

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
| **Peitsche 5 (250 mm)** | M8 4-Pin A-kodiert (Buchse) | **Heck-Radar & lokaler OBD2** | RADAR_PWR_12V, RADAR_GND, RADAR_RX (UART/CAN_H), RADAR_TX (UART/CAN_L) |

---

## 5. Integration in OEM-Infotainmentsysteme

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 WHIM-Emulation & Apple CarPlay / Android Auto Freischaltung
* **Hintergrund:** Apple CarPlay setzt im Fahrzeug ein betriebsbereites Sprachmikrofon voraus. Harley-Davidson verriegelt CarPlay in der Boom! Box GTS Firmware standardmäßig und verlangt entweder das kabelgebundene 7-Pin DIN-Headset oder das proprietäre Bluetooth-Funkmodul **HD-WHIM** (*Wireless Headset Interface Module*, $> 350\,\text{€}$).
* **Elektrische Impedanz-Emulation:** OpenMotorBridge emuliert an den Audio-Schnittstellen über ein präzises Widerstands- und Übertragernetzwerk die charakteristische elektrische Gleich- und Wechselstrom-Impedanz ($1{,}0 \dots 2{,}2\,\text{k}\Omega$) eines aktiven OEM-Mikrofons.
* **Ergebnis:** Die Boom! Box GTS schaltet Apple CarPlay und Android Auto im 6,5"- bzw. 12,3"-Fahrzeugdisplay sofort frei – **ohne teures WHIM-Modul** und ohne unsichere Jumper-Stecker.
* **Nahtloses Ducking:** Navigationsansagen der Boom! Box werden über den ES8388 Codec priorisiert und über die aktiven Intercom-Gespräche mit einstellbarem Ducking ($-12\,\text{dB}$) sanft eingeblendet.

#### 5.1.2 Wireless Smart Fairing & 4-Port Power Hub
Um empfindliche Signal-Kabelbäume über den mechanisch beanspruchten Lenkkopf zu eliminieren und maximale Ladeleistung im Cockpit bereitstrzustellen:
* **Drahtlose Funkbrücke zur Zentralbox:** Ein autonomer Controller-Knoten (ESP32-C3 / nRF52840) hinter der Verkleidung kommuniziert über **ESP-NOW ($< 3\,\text{ms}$ Latenz)** und **BLE 5.0 (2M-PHY)** mit der Zentralbox.
* **4-Port High-Power DCDC USB-Hub:**
  * **Port 1 (USB-C PD 30W):** Schnellladung für Smartphone (Navigation / Wireless CarPlay).
  * **Port 2 (USB-C 15W):** Dauerstromversorgung für Action-Cams (GoPro / Insta360).
  * **Port 3 (USB-A 10W):** Universalspeisung für separates Motorrad-Navi (Garmin Zumo / TomTom Rider).
  * **Port 4 (USB-A intern):** Führt zum drahtlosen CarPlay-Adapter (*Ottocast / CarlinKit*) im Boom! Box USB-Zweig inkl. Handschuhfach-Trennschalter.
* **Digitales I2S-MEMS Ambient-Mikrofon (Knowles):** Sitzt wettergeschützt hinter einer ePTFE-Schallmembran direkt auf der Front-Platine. Der Controller berechnet den Umgebungsgeräuschpegel (dB-A/RMS) per Edge-DSP vor Ort und sendet kompakte Pegelwerte an die Zentralbox für die Helm-Lautstärkenachführung.
* **Kabelgebundener Lenker-PTT (100 % batteriefrei):** Der PTT-Taster am Lenker schaltet direkt auf den Interrupt-GPIO des Front-Knotens. Keine leeren Knopfzellen im Winter!
* **Minimaler Installationsaufwand:** Vom Motorrad wird nach vorne lediglich **eine 2-adrige 12V-Stromleitung** benötigt (am Scheinwerfer oder Zubehörstecker abgegriffen).

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Echtzeit-Telemetrie:** Über den integrierten TCAN334G CAN-Transceiver lauscht die Zentralbox im Listen-Only-Modus auf dem Fahrzeugbus und erfasst Raddrehzahlen, Schräglage und Blinkersignale.
* **Display-Warnmeldungen:** Statusmeldungen können direkt im Motorrad-TFT-Display generiert werden.

### 5.3 Heck-Radar & Totwinkel-Assistent (Garmin Varia / 24 GHz mmWave) am Pod 3 Kombihalter
* **Heck-Kombihalter:** Der Montagehalter für Pod 3 am Heck integriert einen winkelverstellbaren GoPro-kompatiblen Ausleger zur präzisen horizontalen Justage des Radarsensors.
* **Direktanschluss an Peitsche 5:** 12V-Power und bidirektionale Telemetrie (UART / CAN) über die M8 4-Pin Schnittstelle.
* **Akustische Helm-Warnung:** Bei Annäherung eines Fahrzeugs mit hoher Relativgeschwindigkeit senkt die Audio-DSP-Engine Intercom/Musik ab (Ducking) und spielt einen prägnanten Doppelton-Ping ins Headset.
* **Visuelle Anzeige:** Die WebApp zeigt ein radar-gestütztes Display mit Fahrzeug-Tracking und Farbkodierung (grün/gelb/rot).
