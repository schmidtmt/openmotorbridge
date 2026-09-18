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
│ 1. COCKPIT / LENKER & KEYFOB:                                                               │
│    • Front-Node (PCBA 05): Kabelgebundener Lenkertaster- / PTT-Eingang (optogekoppelt)       │
│    • Smart-Keyfob (PCBA 07): BLE/LoRa Pager (LiPo mit MAX17048 Fuel Gauge & Funk-PTT)       │
│    • PWA Dashboard auf Smartphone / TFT via Web-Bluetooth (WebBLE)                          │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. ZENTRALE STEUERBOX (Unter der Sitzbank, IP67):                                           │
│    • ESP32-S3 Dual-Core MCU (240 MHz) • ES8388 Audio-Codec & DSP Audio-Mixer                │
│    • LM5164-Q1 72V Automotive Step-Down • BQ24075 USV & 2200mAh Flat-LiPo-Pufferakku        │
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

### 1.1 Das Leitmotiv: Den Lead unterstützen, nicht ersetzen

Klassische Telematik- und Assistenzsysteme neigen zum digitalen Paternalismus: Sie überfrachten das Cockpit mit Schaltempfehlungen, unaufgeforderten Stau-Warnungen und Navigations-Pop-ups. OpenMotorBridge folgt einer radikal gegensätzlichen Philosophie, die auf realer Gruppen-Fahrpraxis basiert:

* **Der Lead-Fahrer ist der beste Sensor der Welt:**
  * Kein Algorithmus und kein Satelliten-Uplink erkennt in Echtzeit Rollsplitt in der Kurve, eine unübersichtliche Baugrube, einen schleichenden Traktor oder Wildwechsel so präzise wie das geschulte Auge des vorausschauenden Tourguides.
  * Eine dreisekündige Ansage über die Intercom (*„Achtung, Baustelle rechts, wir fädeln links ein!“*) erreicht die gesamte Gruppe in Millisekunden, erfordert null Blickabwendung vom Asphalt und ermöglicht sofortige Anpassung von Tempo und Schräglage.
* **Primat der stabilen, markenübergreifenden Intercom:**
  * Die primäre Aufgabe von OpenMotorBridge ist es daher nicht, den Fahrer zu belehren, sondern die **unterbrechungsfreie Sprachkommunikation zwischen inkompatiblen Headset-Ökosystemen (Sena, Cardo, OMM)** felsenfest zu garantieren.
* **Respekt vor bewährten visuellen Signalen:**
  * Selbst bei einem unvorhergesehenen Funkausfall (z. B. leere Headset-Akkus) bricht eine gut geführte Gruppe nicht zusammen: Der aufmerksame Lead-Fahrer kontrolliert regelmäßig die Rückspiegel. Setzt ein Gruppenmitglied den rechten Blinker oder gibt Lichthupe, reagiert der Tourguide sofort und steuert die nächste Haltemöglichkeit an.
  * Digitale Systeme dürfen diese erprobten menschlichen Routinen niemals durch störende Cockpit-Menüs behindern.

---

## 2. Modulare Systemphilosophie & Montagefreiheit (Die 5 Funktionsknoten)

OpenMotorBridge v8.0 definiert die Plattform über **5 standardisierte Funktionsknoten**:
1. **Zentralbox (Main ECU):** Zentraler Rechenkern (ESP32-S3), 24-Bit Audio-DSP/Codec (ES8388), galvanische Trennübertrager, 72V Automotive Step-Down (LM5164-Q1) und LiPo-USV (BQ24075 mit 2.200 mAh Flachzelle). *(Typischerweise mittig unter der Sitzbank im Batteriefach montiert).*
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
> Für ausgewählte Plattformen liefern wir in **[Kapitel 08 (Mechanik & Gehäuse)](08_enclosures_mechanics_cad.md)** komplett durchentwickelte, 100 % schraub- und klebefreie **Referenz-Montagekits** mit:
> * **Referenz-Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring):** Pod 3 im Under-Cowl Skeleton Dock unter der Forged-Carbon-Hutze, Pod 1 & 2 geschützt in den Kofferdeckeln (Zero-Drill an Scharnierschrauben, Schnellkupplung), Front-Node am Geweihträger hinter der Sharknose-Außenhaut.
> * **Referenz-Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 3 in der Touring Fender Console auf dem Kotflügel, Pod 1 & 2 in den Kofferdeckeln, Front-Node unsichtbar in der 7"-Scheinwerfer-Nacelle.
> * **Referenz-Kit 3 (Classic Bagger & Cruiser – Street Glide / Electra Glide):** Pod 3 in der Touring Stealth Console nahtlos an der Soziusbank, entkoppeltes Radar unter dem Kennzeichen, Pod 1 & 2 in den Kofferdeckeln.
> * **Referenz-Kit 4 (Adventure & Touring Enduros – BMW GS, KTM Adventure, Africa Twin):** Pod 3 direkt auf Gepäckbrücke / Rohrheck mit integriertem M5-GoPro-Radarausleger, Pod 1 & 2 an Sturzbügeln per Rohrbett mit V-Nut und EPDM-Spannringen, Front-Node an Navigationsstrebe oder im Schnabel.
>
> Ihr könnt diese Referenzen 1:1 nachbauen, für euer eigenes Modell adaptieren oder anhand der offenen CAD-/STEP-Maße völlig eigene Halterungen designen, die perfekt zu eurem Motorrad passen!

### 2.1 Whitepaper-Entwurfsentscheidung: Dezentrale Satelliten-Topologie vs. Monolithische Single-Box

In der frühen Konzeptphase wurde intensiv evaluiert, ob das gesamte System in einem einzigen, großen Zentralgehäuse (z. B. unter der Sitzbank oder hinter der Frontverkleidung) untergebracht werden sollte. Der monolithische Ansatz wurde nach physikalischen und messtechnischen Voruntersuchungen einstimmig verworfen:

#### Evaluierungsmatrix: Monolithische Zentralbox vs. OpenMotorBridge Satelliten-Architektur

| Bewertungskriterium | Option A: Monolithische Single-Box | Option B: Reine Lenker/Cockpit-Box | **Option C: OMB Dezentrale Satelliten (Gewählt)** |
| :--- | :--- | :--- | :--- |
| **HF-Selbststörung (Desensing)**| **Kritisch:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V Buck-Regler auf engstem Raum | **Kritisch:** Starkes Übersprechen auf Cockpit-TFT und Radio-Antenne | **Optimal (> 45 dB Isolation):** GNSS/LoRa am Heck, Intercoms an den Flanken, Display vorn |
| **Kabelbaum-Durchmesser** | **Massiv:** 26+ Einzelleitungen müssen quer durch das gesamte Motorrad gezogen werden | **Schlecht:** 18 Leitungen über den schwenkenden Lenkkopf (Kabelbruch-Risiko) | **Ultra-Schlank:** Nur 6-polige M8-Verbindung zum Heck; Front-Node autark via ESP-NOW |
| **Thermische Verlustleistung** | **Hot-Spot (> 18 W):** 72V DC/DC + Audio-Endstufen + Akkuladung unter der Sitzbank | **Thermischer Hitzetod (> 85 °C):** Stauwärme direkt hinter der Scheinwerfermaske | **Perfekt verteilt:** Max. 3–4 W pro Gehäuse; passive Wärmeabfuhr ohne Hotspots |
| **GNSS-Zenitsicht & Radar** | **Verschattet:** Sitzbank und Fahrer-Körper blockieren Satelliten & Heck-Sichtfeld | **Schlecht:** Heck-Radar vom Lenker aus physikalisch unmöglich | **Ideal:** Heck-Pod 3 hat 360°-Horizontblick und freie Radarsicht nach hinten |
| **Fahrtwind-Abtastung (AGC)** | **Physikalisch unmöglich:** Unter der Sitzbank herrscht kein dynamischer Staudruck | **Möglich:** Windmessung direkt am Lenker | **Exzellent:** Knowles I2S MEMS direkt an der Frontscheibe im Front-Node |

1. **Die Physik der HF-Koexistenz (Vermeidung von Receiver Desensitization):**
   * GNSS-Signale treffen die Erde mit extrem schwachen Pegeln von ca. **$-130\,\text{dBm}$ bis $-160\,\text{dBm}$**.
   * Befinden sich ein 72V-Schaltregler (LM5164-Q1 mit schnellen Schaltflanken), ein 868-MHz-LoRa-Sender (+22 dBm / 160 mW) und zwei 2.4-GHz-Mesh-Transceiver im selben Metallgehäuse auf wenigen Zentimetern Abstand, heben die Breitband-Oberwellen das Grundrauschen an (*Noise Floor Lift*). Das GNSS verliert die Phasenverriegelung (Cycle Slip) und die Ortungsgenauigkeit bricht ein.
   * Die räumliche Trennung (Heck-Pod 3 für Navigation, Pod 1/2 für Intercom an den Flanken) garantiert physikalisch über **$45\,\text{dB}$ Freiraumdämpfung** zwischen den HF-Stufen.
2. **Kabelbaum-Zuverlässigkeit über den Lenkkopf:**
   * Jedes Kabel, das über den beweglichen Lenkkopf geführt wird, unterliegt während der Fahrzeuglebensdauer Millionen von Biegewechseln.
   * Durch die Auslagerung der Cockpit-, Display- und PTT-Funktionen in den **Front-Node (PCBA 05)**, der über die hochzuverlässige, drahtlose **ESP-NOW Funkbrücke (< 0.9 ms Latenz)** mit der Zentralbox kommuniziert, entfallen sämtliche empfindlichen Datenleitungen über die Lenkachse.
3. **Ergebnis:** Höchste Signalintegrität, null Hotspots, maximale Langlebigkeit und unübertroffene Montageflexibilität auf jedem Motorradtyp.

### 2.2 Universelle Gehäuse-Grundformen & Rohrbett-Option (Universal-V-Nut)
Für Naked Bikes, Enduros und klassische Rahmenrohre verfügen die Universal-Pod-Gehäuse (Typ B) an der Unterseite über eine integrierte $120^\circ$-Prismenkehle ($R = 15\,\text{mm}$):
* Passend für alle typischen Rohre von $\varnothing 18\,\text{mm}$ bis $\varnothing 35\,\text{mm}$ ($7/8"$, $1"$, $1\,1/8"$, $1\,1/4"$).
* 4 Einhängenasen für wetterfeste EPDM-Spannringe zur werkzeuglosen Schnellmontage ohne Lackkontakt.
* Durchgangsschlitze ($5{,}0 \times 2{,}5\,\text{mm}$) für Kabelbinder oder Schellen bei dauerhafter Diebstahlsicherung.

### 2.3 Kabelloser Helm-Komfort
* Die schweren Intercom-Geräte (Sena 50S / Cardo Edge) verbleiben wetter- und diebstahlgeschützt an den Motorrad-Pods (z. B. im Kofferdeckel oder unter der Abdeckung).
* Die Helme von Fahrer und Sozius bleiben zu $100\,\%$ leicht, aerodynamisch original und frei von Kabeln. Die Audio-Ein- und Ausgabe erfolgt vollkommen drahtlos über die integrierte Bluetooth-Schnittstelle der Zentralbox.

### 2.4 Universelle OEM-Adapter-Kompatibilität (Off-the-Shelf)
Die erweiterten Pod-Kassetten ($110 \times 54 \times 28\,\text{mm}$ Innenraum) nehmen alle handelsüblichen OEM-Geräte im ungeöffneten Originalzustand auf:
* **Klasse S (Smart Modular Cartridge mit Mechatronik • OMB-Referenz):** z. B. Sena SPIDER X Slim (Primärempfehlung), Sena 60S, Cardo Edge – 100 % ungeöffnetes Originalgerät im PA12-MJF Konturbett mit 3-Punkt EPDM-Dämpfung gegen $20\,\text{g}$ Vibration, 4 unabhängige mechatronische Aktuatoren auf PCBA 03 Rev 2.0 (WCH CH32V003 RISC-V Controller, In-System Flashing via Pin 5 UART), direkte $3{,}85\,\text{V}$ DC-Speisung ab Werk, null Pogo-Pins, null Löten, 100 % Erhalt von Werksgarantie & IPX-Schutz.
* **Klasse A (Drahtlos-Bridges & USB-Speisung):** z. B. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red – versorgt über flaches 90° Micro-USB/USB-C Kabel, drahtlose Audioübertragung zum Helm, externe SMA-Bulkhead-Doppelbuchse mit Schutzkappe an der Frontblende.
* **Klasse B (Pogo-Pin Federkontakt-Cradles):** z. B. Sena 50S/60S/30K/20S EVO – vollwertiges analoges Audio (ES8388 Codec) und TLP222A PTT-Synthese.
* **Klasse C (Magnetischer Air-Mount):** z. B. Cardo Packtalk Edge / Pro (Hinweis: Packtalk Neo unterstützt kein Laden während der Fahrt und ist ausgeschlossen) – werkzeugloses magnetisches Andocken über 2x N52 Neodym-Magnete.
* **Klasse D (Schiebe-Cradles):** z. B. Cardo Packtalk Bold/Black, Freecom-Serie – mechanische Gleitschiene mit Arretierfeder.
* **Klasse E (Analoger PMR446 Funk):** z. B. Midland G7/G9 Pro, XT30, Kenwood – 2-Pin Doppelklinkenanschluss mit PhotoMOS-PTT-Tastung.
*(Detaillierte Verkabelungsmatrix siehe [Spezifikation 02](02_intercom_matrix_profiles.md)).*

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

### 5.8 2-in-1 LoRa Smart-Keyfob (Alarm-Pager, N52 Magnetschlüssel & MagSafe Qi Dock)
* **All-in-One Schlüsselanhänger:**
  * Kombiniert den $20 \times 10 \times 5\,\text{mm}$ N52-Neodym-Magnetschlüssel für den mechanischen Kassettenverschluss mit einem stummen LoRa 868 MHz Silent Alarm Pager in einem kompakten PA12-MJF Gehäuse ($58 \times 34 \times 13\,\text{mm}$).
  * Ein integriertes $0{,}5\,\text{mm}$ Weicheisen-Abschirmblech schützt interne Elektronik und Akku vor Magnetfeldsättigung.
* **Kryptografische Absicherung & Selektivität:**
  * Verschlüsselt mit AES-128 GCM und 32-Bit Monotonic Nonce (Anti-Replay). Nur der autorisierte Pager des Besitzers schlägt an; unbefugtes Abhören oder Auslösen von Fehlalarmen ist ausgeschlossen.
* **Zero-False-Alarm & Anti-Theft:**
  * Bei anwesendem BLE-Token des Fahrers ($< 1{,}5\,\text{m}$) wird die Kassettenentnahme als legitim erkannt. Unbefugtes Aufhebeln ohne Keyfob löst sofort einen lautlosen Pager-Notruf mit bis zu 4,5 km Reichweite aus.
* **MagSafe Cockpit-Docking:**
  * Auf dem Motorrad rastet der Keyfob magnetisch auf dem Cockpit-Dock (PCBA 06) ein und wird während der Fahrt induktiv nachgeladen.

### 5.9 Aktives Sicherheits-Lichtmanagement (ESS Notbremsblinken & Front-Zusatzlicht J11)
* **ESS Notbremsblinken (Emergency Stop Signal):**
  * Überwacht die Längsverzögerung $a_x$ über die 6-Achs IMU (Standard-Schwelle $a_x < -0{,}60\,\text{g}$, konfigurierbar auf $-0{,}45\,\text{g}$ oder $-0{,}75\,\text{g}$).
  * Bei einer Gefahrenbremsung taktet OMB das Garmin Varia Rücklicht über UART2 und externe Zusatzleuchten (z. B. Cosmo Moto via `RESERVE_GPIO_B`) mit einem hochfrequenten **4,5 Hz Stroboskop-Warnblinken**, um den nachfolgenden Verkehr vor Auffahrunfällen zu schützen.
* **Front-Zusatzscheinwerfer (Front-Node J11 via TPS1H100):**
  * Der 4,5A Smart High-Side Switch auf dem Universal Front-Node steuert LED-Zusatzscheinwerfer in drei wählbaren Betriebsmodi: `[AUS]`, `[DAUER-EIN]` (Tagfahrlicht/Nebel) oder `[AUTO-STROBE BEI ESS]` (visuelles Warnsignal nach vorne bei Vollbremsung).

### 5.10 Apple Find My & Google Find My Device Schwarmortung (Dual-Beaconing)
* **Globale Ortung ohne SIM-Karte & laufende Gebühren:**
  * Im Standby / Deep Sleep sendet der ESP32-S3 im Zeitmultiplex abwechselnd **Apple Find My (FMNP)** und **Google Find My Device (FMDN)** BLE-Werbepakete (alle 2,0 Sekunden, Sendedauer ca. $2{,}5\,\text{ms}$).
  * Über **~1,5 Mrd. iPhones und ~3 Mrd. Android-Smartphones** weltweit wird das Motorrad bei Diebstahl selbst in Tiefgaragen und fremden Städten anonym und hochpräzise geortet.
* **Autarkes USV-Powermanagement:**
  * Der mittlere Ruhestrom des Dual-Beaconings liegt bei nur ca. **$15\,\mu\text{A}$**.
  * Zusammen mit der IMU-Erschütterungsüberwachung ($6\,\mu\text{A}$) liefert der interne **2.200 mAh LiPo-Pufferakku** eine autarke Ortungs- und Alarmbereitschaft von **3 bis 4 Jahren** – selbst wenn Diebe die 12V-Bordbatterie trennen.

### 5.11 Smart Docking Telemetrie & "Handy vergessen"-Alarmierung
* **Ablaufunabhängige Korrelationslogik (Fahrer-Alltag):**
  * Biker starten häufig erst das Motorrad (Handy noch in der Jackentasche) und docken das Smartphone erst nach dem Warmlaufen am Lenker (Qi `J10` / USB `J5`) oder im Handschuhfach (`J5_MP3`) an.
  * Das Smartphone ist bereits per Bluetooth LE mit OMB gekoppelt. Sobald der Ladevorgang startet, meldet das Smartphone über das OS-Event `chargingchange` seinen Ladezustand per BLE $\rightarrow$ OMB korreliert Ladelast und BLE-Identität verlässlich.
* **3-Stufen-Geräteerkennung:**
  * *USB-Stick / MP3-Player (Klasse `0x08`):* Minimaler Strom ($< 0{,}5\,\text{W}$), lokale Musikwiedergabe, **kein Fehlalarm** beim Verlassen des Fahrzeugs.
  * *Fahrer-Handy:* USB-PD ($> 15\,\text{W}$) oder Qi ($10\dots 15\,\text{W}$) mit aktivem BLE-Handshake.
  * *Gast-Gerät:* Neutrales Laden ohne Profilwechsel.
* **Flankengetriggerter Wechsel & "Handy vergessen"-Alarm:**
  * Der automatische Wechsel in die Cockpit-Ansicht erfolgt **strikt einmalig auf der steigenden Flanke** des Ladebeginns. Manuelle Navigationen zu anderen Tabs werden respektiert (User Override Protection).
  * Schaltet der Fahrer die Zündung aus (`KL15 == 0`) und entfernt sich vom Motorrad ($d > 3\,\text{m}$), während Qi oder USB weiterhin ein aufliegendes Smartphone melden, schlägt das System sofort Alarm: Zwei Huptöne am Motorrad und ein LRA-Vibrationsstakkato auf dem Smart-Keyfob warnen vor dem Zurücklassen des teuren Geräts.
* **Architektonische Entscheidung zu UWB (Ultra-Wideband):**
  * Da OpenMotorBridge als Telemetrie-, Audio- und Alarmsystem arbeitet und die Freigabe des Motorstarts beim originalen OEM-Zündschloss/Schlüssel verbleibt, ist UWB (hoher Ruhestrom 30–50 mA, Zusatz-ICs, Antennenaufwand) als reines Zubehörsystem **Overengineering** und wird bewusst zu Gunsten von BLE, LoRa und Find My Device weggelassen.

### 5.12 Kognitive Cockpit-Entlastung & Stille Absicherung im Hintergrund
* **Strikte Grenzziehung: Wann Automatisierung eingreift – und wann sie schweigt:**
  * Digitale Telemetrie und Sensorik greifen ausschließlich dort ein, wo die menschliche Sprache oder Wahrnehmung physikalisch versagt:
    1. **Sturz & eCall bei Handlungsunfähigkeit:** Liegt ein Fahrer nach einem Unfall mit $> 6{,}5\,\text{g}$ und $> 70^\circ$ Schräglage regungslos im Graben, ist er oft bewusstlos oder das Headset-Kabel ist abgerissen. Hier alarmiert die automatische LoRa-Notrufflut (868 MHz) mit GPS-Koordinaten autonom die Gruppe.
    2. **Gruppen-Abriss über Funkdistanz (Lost-Rider Tracking):** Überschreitet der Abstand zum Schlusslicht im Gebirge die 2,4-GHz-Audio-Reichweite ($> 1{,}5\,\text{km}$), meldet das 868-MHz-LoRa-Paket dem Guide lautlos und dezent die Distanz zum Zurückgefallenen.
    3. **Unsichtbare Gefahrenzonen:** Ein sich mit $+60\,\text{km/h}$ im toten Winkel näherndes Fahrzeug (Heck-Radar Garmin Varia) oder ein schleichender Druckabfall im Reifen (TPMS) werden frühzeitig erkannt, bevor das Motorrad instabil wird.
    4. **Parkplatzwächter (Zündung AUS):** Erschütterungen des abgestellten Motorrads werden lautlos an den 2-in-1 LoRa Smart-Keyfob (LRA-Pager) in der Jackentasche des Fahrers gemeldet.
* **Absolutes Push-Verbot für allgemeine Verkehrs- & Wettertexte während der Fahrt ($v > 0$):**
  * Weder Staumeldungen noch Wettertexte oder CAN-Spritstand-Broadcasts werden während der Fahrt auf das Display gepusht. Die kognitive Last des Fahrers bleibt zu 100 % für die Fahrzeugbeherrschung und die Blickführung frei.
