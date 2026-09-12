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
│ • Intercom-Brücke A (Sena    │ • Intercom-Brücke B (Cardo   │ • 1-Tier Monolith-Schlitten │
│   50S/60S/MeshPort-Kassette) │   Packtalk Edge / PMR446)    │ • u-blox MAX-M10S Multi-GNSS│
│ • Koffer-, Rahmen-, Heck-    │ • Koffer-, Rahmen-, Heck-    │ • SX1262 LoRa 868MHz + RP2040│
│   oder Helm-Montage          │   oder Helm-Montage          │ • 2.4 GHz OMM-Mesh (RP2040) │
└──────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
  │                                                                                         │
  ├─► 6. BORDNETZ-ANSCHLUSS: AMP Superseal 1.5 4-Pin (KL30 Dauerplus, KL15 Zündung, Masse)   │
  ├─► 7. HECK-SENSOR-ZWEIG: M8 4-Pin Buchse (Heck-Radar / Totwinkel-Sensor / lokaler OBD2)──┤
  │                                                                                         │
  ▼ 2.4 GHz Ultra-Low-Latency Funkverbindung (ESP-NOW < 3ms & BLE 5.0 2M-PHY)               │
┌───────────────────────────────────────────────────────────────────────────────────────────┤
│ 8. COCKPIT-SUBSYSTEM: Wireless Universal Front-Knoten (PCBA 05 Cockpit & Cam Bridge)     │
│ • Automotive 4-Port USB 2.0 Hub (Microchip USB2514B) für Boom! Box & CP2AA-Dongle        │
│ • Geschalteter CarPlay-Port via TI TPS2051B (gesteuerter 2,5s Kaltstart & Hitzeschutz)   │
│ • Digitales I2S-MEMS Ambient-Mikrofon mit ePTFE-Membran (Edge-RMS-Schallpegelmessung)     │
│ • Direkter kabelgebundener Lenker-PTT-Tastereintritt (GPIO-Interrupt, 100% batteriefrei)  │
│ • Integrierter Cockpit-CAN-Transceiver (TCAN334G mit Auto-Sensing 120R) für TFT-Cockpits │
│ • Einzige fahrzeugseitige Zuleitung: Robuste 2-adrige 12V-Bordnetzspeisung (KL15 / GND)   │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Modulare Systemphilosophie & Montagefreiheit (Die 5 Funktionsknoten)

OpenMotorBridge v8.0 definiert die Plattform über **5 standardisierte Funktionsknoten**:
1. **Zentralbox (Main ECU):** Zentraler Rechenkern (ESP32-S3), 24-Bit Audio-DSP/Codec (ES8388), galvanische Trennübertrager, 72V Automotive Step-Down (LM5164-Q1) und LiPo-USV (BQ24075). *(Typischerweise mittig unter der Sitzbank im Batteriefach montiert).*
2. **Heck-Pod 3 (Backbone & Telemetrie):** Multi-GNSS (u-blox MAX-M10S), 868 MHz LoRa (Semtech SX1262), 2.4 GHz OMM-Mesh-Co-Prozessor (RP2040) und 6-Achs-IMU (BMI270). *(Typischerweise am Heck mit ungestörter Sicht in den Zenit).*
3. **Satelliten-Pod 1 (Intercom-Brücke A):** Universal-Wechselschacht für Sena (Mesh 2.0/3.0 / Bluetooth). *(Typischerweise linke Fahrzeugseite).*
4. **Satelliten-Pod 2 (Intercom-Brücke B):** Universal-Wechselschacht für Cardo (DMC Gen1/Gen2 / Bluetooth) oder analogen Funk (PMR446). *(Typischerweise rechte Fahrzeugseite zur HF-Raumdiversität).*
5. **Front-Node (Cockpit & Camera Hub):** Autonomer ESP32-S3 Satellit, Automotive USB 2.0 4-Port Hub (USB2514B) für Apple CarPlay/Android Auto CP2AA-Dongle, 20W USB-PD Fast-Charging (Southchip SC8102), geschalteter VBUS mit TPS2051B, digitaler PTT-Tastereingang, TCAN334G CAN-Transceiver und Knowles I2S MEMS-Windgeräuschmikrofon. *(Typischerweise unsichtbar in der Cockpitverkleidung oder Scheinwerfermaske).*

```
                     DIE 5 STANDARDISIERTEN FUNKTIONSKNOTEN
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. FRONT-NODE (Cockpit/Nacelle):  Drahtloser USB-, Cam-, PTT- & Audio-Hub   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. ZENTRALBOX (Unter Sitz/Akku):  DSP Audio-Matrix, Power Supply, USV, CAN  │
├──────────────────────────────┬──────────────────────────────┬───────────────┤
│ 3. POD 1 (Links/Koffer):     │ 4. POD 2 (Rechts/Koffer):    │ 5. HECK-POD 3:│
│ • Intercom-Brücke A (Sena)   │ • Intercom-Brücke B (Cardo)  │ • GNSS / LoRa │
│ • 100% Wechselschacht        │ • 100% Wechselschacht        │ • OMM 2.4 GHz │
└──────────────────────────────┴──────────────────────────────┴───────────────┘
```

> [!NOTE]
> **Montagefreiheit – *Your Bike, Your Choice*:**  
> Wo und wie ihr diese 5 Boxen an eurem Motorrad platziert, ist bewusst **völlig euch überlassen**! OpenMotorBridge stellt die standardisierten Elektronik- und Gehäuse-Dimensionen sowie die Schnittstellen bereit.  
> Für ausgewählte Plattformen liefern wir in **[Kapitel 08 (Mechanik & Gehäuse)](file:///Users/schmidtm/openMotorBridge/docs/de/08_enclosures_mechanics_cad.md)** komplett durchentwickelte, 100 % schraub- und klebefreie **Referenz-Montagekits** mit:
> * **Referenz-Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring):** Pod 3 im Under-Cowl Skeleton Dock unter der Forged-Carbon-Hutze, Pod 1 & 2 geschützt in den Kofferdeckeln (Zero-Drill an Scharnierschrauben, Schnellkupplung), Front-Node am Geweihträger hinter der Sharknose-Außenhaut.
> * **Referenz-Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 3 in der Touring Fender Console auf dem Kotflügel, Pod 1 & 2 in den Kofferdeckeln, Front-Node unsichtbar in der 7"-Scheinwerfer-Nacelle.
> * **Referenz-Kit 3 (Classic Bagger & Cruiser – Street Glide / Electra Glide):** Pod 3 in der Touring Stealth Console nahtlos an der Soziusbank, entkoppeltes Radar unter dem Kennzeichen, Pod 1 & 2 in den Kofferdeckeln.
> * **Referenz-Kit 4 (Adventure & Touring Enduros – BMW GS, KTM Adventure, Africa Twin):** Pod 3 direkt auf Gepäckbrücke / Rohrheck mit integriertem M5-GoPro-Radarausleger, Pod 1 & 2 an Sturzbügeln per Rohrbett mit V-Nut und EPDM-Spannringen, Front-Node an Navigationsstrebe oder im Schnabel.
>
> Ihr könnt diese Referenzen 1:1 nachbauen, für euer eigenes Modell adaptieren oder anhand der offenen CAD-/STEP-Maße völlig eigene Halterungen designen, die perfekt zu eurem Motorrad passen!

### 2.1 Universelle Gehäuse-Grundformen & Rohrbett-Option (Universal-V-Nut)
Für Naked Bikes, Enduros und klassische Rahmenrohre verfügen die Universal-Pod-Gehäuse (Typ B) an der Unterseite über eine integrierte $120^\circ$-Prismenkehle ($R = 15\,\text{mm}$):
* Passend für alle typischen Rohre von $\varnothing 18\,\text{mm}$ bis $\varnothing 35\,\text{mm}$ ($7/8"$, $1"$, $1\,1/8"$, $1\,1/4"$).
* 4 Einhängenasen für wetterfeste EPDM-Spannringe zur werkzeuglosen Schnellmontage ohne Lackkontakt.
* Durchgangsschlitze ($5{,}0 \times 2{,}5\,\text{mm}$) für Kabelbinder oder Schellen bei dauerhafter Diebstahlsicherung.

### 2.2 Kabelloser Helm-Komfort
* Die schweren Intercom-Geräte (Sena 50S / Cardo Edge) verbleiben wetter- und diebstahlgeschützt an den Motorrad-Pods (z. B. im Kofferdeckel oder unter der Abdeckung).
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
| **Peitsche 1 (250 mm)** | M8 6-Pin A-kodiert (Buchse) | **Satelliten-Pod 1** (Intercom-Brücke A: Sena Mesh / Universal) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
| **Peitsche 2 (250 mm)** | M8 6-Pin A-kodiert (Buchse) | **Satelliten-Pod 2** (Intercom-Brücke B: Cardo DMC / PMR446) | NF_OUT+, NF_OUT-, OPTO_TRIGGER, 1-WIRE_ID, +5V_VBUS, GND |
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

#### 5.1.2 Universal Cockpit & Front Hub (PCBA 05): USB-Subsystem, Live-Traffic & PTT
Der Front-Knoten (PCBA 05) dient auf **allen Motorrädern** als universeller Cockpit-Knoten und eliminiert empfindliche Signalkabel über den mechanisch beanspruchten Lenkkopf:
* **Drahtlose Funkbrücke zur Zentralbox:** Ein autonomer Controller-Knoten (ESP32-S3-WROOM-1U mit Vektor-DSP) hinter der Verkleidung kommuniziert über **ESP-NOW ($< 0{,}9\,\text{ms}$ Latenz)** und **BLE 5.0 (2M-PHY)** mit der Zentralbox.
* **Drahtgebundener Lenker-PTT (Optokoppler an `J3` / GPIO 0, $< 1{,}8\,\text{ms}$ Latenz):** Nur $30\dots 50\,\text{cm}$ kurzes, geschütztes Kabel am Lenker – kein bruchgefährdetes Signalkabel über den schwenkenden Lenkkopf nach hinten zur Zentralbox!
* **Digitales I2S-MEMS Ambient-Mikrofon (Knowles SPH0645LM4H-6):** Berechnet Umgebungs- und Fahrtwindgeräusche (dB-A/RMS) direkt an der Front für automatische Helmlautstärke-Nachführung (AGC) via Xtensa Vektor-DSP.
* **Automotive USB 2.0 Subsystem (Microchip USB2514B & TI TPS2051B):**
  * **Upstream Host Port (`J4`):** Führt direkt zum USB-Eingang der Harley-Davidson Boom! Box GTS / Skyline OS im Handschuhfach.
  * **Downstream Port 1 (`J5` / Lenker-Smartphone):** High-Speed Daten + 20W Automotive USB-PD Fast Charging (Southchip SC8102, 9V/2.2A & QC 3.0) für Smartphones am Lenker (QuadLock/SP Connect).
  * **Downstream Port 2 (`J6` / CP2AA-Dongle):** Geschalteter $+5{,}0\,\text{V}$ VBUS über `TI TPS2051B` Lastschalter mit softwaregesteuertem **2,5s-Kaltstart**, automatischem **Not-Power-Gating bei Verkleidungshitze** und 0.0 µA Deep-Sleep. Führt über ein $25\dots 30\,\text{cm}$ geschirmtes Kabel zum CP2AA-Dongle (3M Dual-Lock im Verkleidungshohlraum).
  * **Downstream Port 3 (Handschuhfach):** Durchgeschliffenes USB-Kabel ins Handschuhfach – bleibt zu **$100\,\%$ frei für MP3/FLAC USB-Sticks und offizielle OEM-Software-Updates** (inkl. hardwareseitiger Port-Sense Überwachung).
  * **Downstream Port 4 (Cockpit-Zubehör):** High-Speed Daten für Dashcam-Speicher, Chigee-Display oder Zūmo-Navi.
  * **USB-C Service Port (`J7`):** Nativer Diagnose-, Kalibrier- und Flash-Port.
* **USB-Media Proxy & Source-Aware CAN Gating:**
  * Emuliert gegenüber Skyline OS ein MFi-iPod / USB Audio Class Gerät: Track-Titel, Interpret, Album und Spieldauer erscheinen nativ auf dem 12.3" Harley-Bildschirm, während das Audiosignal per LDAC/aptX direkt im Helm bleibt (kein WHIM-Zwang).
  * **Kollisionsschutz:** Wertet `infotainment_source_active` (CAN `0x388`) und Hub-Port 3 aus, damit Wippen-Befehle nur an das Smartphone geleitet werden, wenn OMB/CarPlay/BT aktiv ist (kein versehentliches Streaming bei MP3-Stick oder Radio!).
* **USB CDC-NCM Ethernet Tethering für das interne Werks-Navi:**
  * Meldet sich am Port `J4` als virtueller Netzwerkadapter an und routet Internetdaten vom Smartphone an die Harley.
  * **Vorteil:** Das interne Werks-Navi (HERE / TomTom) hat bei Zündung-AN **sofort Live-Traffic, Baustellen- und Stauwarnungen**, ohne dass der Fahrer manuell einen Smartphone-WLAN-Hotspot starten muss.
* **Dedizierter Action-Cam BLE Shutter-Bridge:**
  * Steuert GoPro, Insta360 und DJI direkt über BLE in direkter Sichtlinie ($< 0{,}5\,\text{m}$) via Lenker-PTT Doppel-Klick.
* **Intelligente Tankpausen-Automatik & KL15-Pufferkondensator (`C_BUF`):**
  * Pufferkondensator ($470\dots 1000\,\mu\text{F}$) hält den Controller bei Zündungsaus für $\approx 1\dots 2\,\text{s}$ am Leben, sendet *"Stop Recording"* an die Kamera und sichert die Datei.
* **Minimaler Installationsaufwand:** Lediglich **eine 2-adrige 12V-Stromleitung (`J1`)** an Zündungsplus KL15; integrierter TI TPS63070 Buck-Boost Wandler garantiert Kaltstart-Stabilität nach ISO 7637-2 Pulse 4.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Echtzeit-Telemetrie:** Über den integrierten TCAN334G CAN-Transceiver lauscht die Zentralbox im Listen-Only-Modus auf dem Fahrzeugbus und erfasst Raddrehzahlen, Schräglage und Blinkersignale.
* **Display-Warnmeldungen:** Statusmeldungen können direkt im Motorrad-TFT-Display generiert werden.

### 5.3 Heck-Radar & Totwinkel-Assistent (Garmin Varia / 24 GHz mmWave) am Pod 3 Kombihalter
* **Heck-Kombihalter & Justage:** Der Montagehalter für Pod 3 am Heck integriert einen winkelverstellbaren GoPro-kompatiblen M5-Ausleger zur präzisen horizontalen Justage des Radarsensors ($\pm 5^\circ$).
* **Direktanschluss an Peitsche 5:** 12V-Power und bidirektionale Telemetrie (UART2 auf `RESERVE_GPIO_A/B` oder CAN-Bus) über die wasserdichte M8 4-Pin Schnittstelle.
* **Unterstützte Radarsysteme:**
  * **Garmin Varia Radar:** RTL515 / eRTL615 serielles Streaming-Protokoll (0xAA Preamble, $140\,\text{m}$ Erfassung, $20\,\text{Hz}$ Update).
  * **24 GHz mmWave Doppler-Radare:** Kompakte Automotive-Radarmodule (z. B. BGT24LTR11 / HLK-LD2410 / DFROBOT).
* **Dynamische Bedrohungs-Klassifikation & Time-To-Collision (TTC):**
  * $\text{TTC} = \frac{d}{v_{\text{rel}}}$.
  * **Grün (Clear):** Kein Fahrzeug im Gefahrenbereich oder $v_{\text{rel}} \le 10\,\text{km/h}$.
  * **Gelb (Annäherung):** $d \le 80\,\text{m}$ und $v_{\text{rel}} > 15\,\text{km/h}$ (Fahrzeug nähert sich normal).
  * **Rot (Kollisionsrisiko):** $\text{TTC} < 3{,}5\,\text{s}$ oder ($d \le 35\,\text{m}$ und $v_{\text{rel}} > 25\,\text{km/h}$).
* **Akustische Helm-Warnung (Prio-1 Ducking):** Bei Bedrohung (Gelb/Rot) senkt die Audio-DSP-Pipeline Musik und Intercom sofort auf **$-18\,\text{dB}$** ab ($< 15\,\text{ms}$ Attack) und spielt einen prägnanten **synthetisierten Doppelton-Ping** ($880\,\text{Hz} \rightarrow 1760\,\text{Hz}$ bei Gelb bzw. $988\,\text{Hz} \rightarrow 1976\,\text{Hz}$ bei Rot) ins Fahrer-Headset.
* **Totwinkel-Assistent (BSD) & Spiegel-LEDs:** Befindet sich ein herannahendes Fahrzeug im Nahbereich ($d < 15\,\text{m}$) auf der linken oder rechten Spur ($|\text{Azimut}| > 3^\circ$), warnen die virtuellen Spiegel-Pills im WebApp-Cockpit pulsierend in Bernstein oder Rot.

#### 5.3.1 Notbremsblinken (Emergency Stop Signal - ESS) über das Heck-Radar & Power-Port
* **Funktionsweise (100% CAN Listen-Only konform):**
  * Erkennt die 6-Achsen-IMU der Zentralbox eine massive Gefahrenbremsung ($a_x < -6{,}0\,\text{m/s}^2$ bzw. $> 0{,}6\,\text{g}$ Verzögerung aus hohem Tempo):
  * Sendet OpenMotorBridge über den seriellen Steuerkanal (`RADAR_TX/RX` an Peitsche 5) den Befehl `SET_LIGHT_MODE: STROBE_4HZ` an das Garmin Varia Radar.
  * **Ergebnis:** Die ultrahellen High-Power-Rücklicht-LEDs des Radars blitzen mit **$4\dots 5\,\text{Hz}$ stroboskopartig** auf, um nachfolgende Autofahrer sofort vor einem Auffahrunfall zu warnen.
  * **Zusatzausgang:** Alternativ oder parallel kann der geschaltete Leistungsausgang `RESERVE_GPIO_B` (High-Side Smart-MOSFET) ein Zusatzbremslicht oder Helmfunk-Bremslicht (z. B. Cosmo Moto) triggern – **völlig ohne Eingriff in die originale Fahrzeug-Bremsleitung**.

### 5.4 LoRa 868 MHz Alarmanlagen-Pager & Parkplatzwächter (Werks-BCM + Autonom)
* **Das Problem herkömmlicher Alarmanlagen:** Geht an der Passhöhe oder am Hotel die Alarmanlage des Motorrads los, ist der Fahrer oft zu weit entfernt ($> 50\dots 100\,\text{m}$) und hört die Hupe nicht.
* **OpenMotorBridge als intelligenter LoRa-Pager:**
  1. **Werksalarmanlagen-Integration (z. B. Harley Smart Security / BMW DWA):**
     * OpenMotorBridge lauscht im Schlafmodus (versorgt über die interne 18650-USV-Zelle) auf dem CAN-Bus.
     * Schlägt die Werksalarmanlage an (`bcm_alarm_triggered == 1`), erkennt OMB dies sofort.
  2. **Autonome Überwachung (für Bikes ohne Werksalarm oder bei Koffer-Diebstahl):**
     * Die interne 6-Achsen IMU erkennt Lageänderungen (Aufrichten vom Seitenständer, Erschütterung).
     * Die Reed-Kontakte an den Koffer-Schlitten erkennen das unbefugte Entriegeln von Kassetten.
  3. **Fernmelde-Alarm via LoRa 868 MHz (Packet Type `0xFE`):**
     * OMB sendet blitzschnell ein LoRa-Notfallpaket mit $1\dots 5\,\text{km}$ Reichweite (durchdringt Hotelbetonwände) an den LoRa-Taschenempfänger des Fahrers oder die anderen Gruppen-Bikes:
       > *„🚨 DIEBSTAHLWARNUNG: Dein Motorrad wird bewegt! (Distanz: 180 m)“*

### 5.5 Universelles BLE-Reifendruckkontrollsystem (TPMS) für Bikes ohne CAN-RDKS
* **Einsatzbereich:** Für alle Maschinen ohne werkseitigen CAN-Reifendruck (Naked Bikes, Sportler, Enduros wie Yamaha Tenere 700, KTM Adventure).
* **Funktion:**
  * Der integrierte Bluetooth 5.0 Controller der Zentralbox scannt passiv die Standard-Advertisement-Frames handelsüblicher BLE-Ventilkappen (z. B. FOBO Bike / Deelife).
  * Kein Kabelaufwand, Ventilkappen werden einfach aufgeschraubt und in der WebApp PWA angelernt.
  * **Anzeige & Warnung:** Reifendruck und Reifentemperatur werden live im Ride HUD dargestellt. Bei plötzlichem Druckverlust in Schräglage ertönt sofort ein akustischer Prioritäts-Warnton im Helm.

### 5.6 Proximity & Standstill Privacy Mute (Lokal-Gesprächsmodus)
* **Problemstellung:** Halten zwei Gruppenfahrer an einer Ampel oder am Straßenrand nebeneinander an und unterhalten sich bei offenem Visier, entstehen im Mesh-Intercom störende Echos und die restliche Gruppe wird mit privaten Absprachen beschallt.
* **Automatische Nahbereichs-Stummschaltung:**
  * **Bedingung:** Fahrzeugstillstand ($v = 0\,\text{km/h}$) UND Erkennung von extremem Nahbereich ($< 3\,\text{m}$, 2.4 GHz RSSI $> -45\,\text{dBm}$ zum Partner-Bike).
  * OMB schaltet das Helmmikrofon für das Weitverkehrs-Mesh automatisch stumm (leiser Quittungston im Helm: *„Lokal-Modus“*).
  * Beide Fahrer unterhalten sich ganz natürlich durch die offenen Visiere.
  * Sobald wieder angefahren wird ($v > 8\,\text{km/h}$) oder der PTT kurz gedrückt wird, öffnet sich das Gruppen-Mesh automatisch wieder.

### 5.7 Action-Cam Event-Tagging & Video-Telemetrie (.srt / .csv)
* **Automatisches Bookmarken von Schrecksekunden:**
  * Neben der manuellen PTT-Geste (1x lang für landschaftliche Highlights) setzt der Front-Node bei Sicherheitsereignissen automatisch einen BLE-Bookmark im Video:
    * Notbremsung ($a_x < -6{,}0\,\text{m/s}^2$)
    * Radar-Kollisionsgefahr ROT ($\text{TTC} < 2{,}5\,\text{s}$)
    * eCall-Sturzerkennung ($> 6{,}5\,\text{g}$)
  * Verhindert das zeitraubende Suchen nach heiklen Verkehrssituationen beim abendlichen Video-Schnitt.
* **Video-Telemetrie-Export:**
  * Die PWA exportiert passend zum GPX-Track eine zeitsynchronisierte `.srt`- oder `.csv`-Telemetriedatei.
  * Ermöglicht das pixelgenaue Einblenden von Tacho, Schräglage und Radar-Gefahrenbalken in Programmen wie Dashware oder Insta360 Studio.
