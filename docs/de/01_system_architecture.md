# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

Dieses Dokument spezifiziert die übergeordnete Gesamtsystem-Architektur der **OpenMotorBridge v8.0**, die universelle Satelliten-Topologie, die fahrzeugfesten Montagekonzepte (Koffer, Rahmen, Heck, Verkleidung bei 100 % kabellosem Helm-Komfort), die HF-Koexistenz sowie die nahtlose Integration in moderne OEM-Motorrad-Infotainmentsysteme.

---

## 1. Problemstellung & Architekturphilosophie

Klassische Motorrad-Kommunikationssysteme sind historisch stark fragmentiert:
* **Inkompatible Mesh-Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh und analoger PMR446-Funk können nicht direkt miteinander kommunizieren.
* **HF-Übersteuerungen & De-Sensing:** Der gleichzeitige Betrieb mehrerer 2,4-GHz-Mesh-Transceiver an einem einzigen Montagepunkt (z. B. am selben Helm oder in einer gemeinsamen Box) führt zu massiver Empfänger-Desensibilisierung (*De-Sensing*), Intermodulation und Reichweiteneinbrüchen von bis zu $80\,\%$.
* **Proprietäre Infotainment-Sperren:** Systeme wie Harley-Davidson Boom! Box GTS / Skyline OS oder BMW ConnectedRide verlangen teure, herstellereigene Schnittstellenmodule (z. B. HD WHIM), um Apple CarPlay oder Android Auto freizuschalten.

**OpenMotorBridge v8.0** löst diese Probleme durch eine modular entkoppelte **Satelliten-Topologie** mit galvanisch getrenntem DSP-Audio-Routing auf dem Motorrad:

```
                                  GESAMTSYSTEM-TOPOLOGIE
+---------------------------------------------------------------------------------------------+
| 1. COCKPIT / LENKER & KEYFOB:                                                               |
|    * Front-Node (PCBA 05): u-blox SAM-M10Q GNSS (J12 I2C), TMP117 / OPT3001 Kaltluftsensor  |
|    * PTT-Lenkertaster, MEMS-Windmikrofon, 20W USB-PD, CarPlay-Port, Totwinkel-Spiegel-LEDs  |
|    * Smart-Keyfob (PCBA 07): 868 MHz LoRa Pager (24/7 Diebstahlalarm & Notfall-Beacon)      |
|    * PWA Dashboard auf Smartphone / TFT via Web-Bluetooth (WebBLE)                          |
+---------------------------------------------------------------------------------------------+
| 2. ZENTRALE STEUERBOX (Unter der Sitzbank / im Pkw-Cockpit, IP67):                          |
|    * ESP32-S3 Dual-Core MCU (240 MHz) * ES8388 Audio-Codec & DSP Audio-Matrix               |
|    * Semtech SX1262 LoRa (868 MHz) an USV-Schiene * Taoglas FXP895 Antenne in Oberwanne    |
|    * Qorvo DW3110 UWB Transceiver (6.5 GHz Ch. 5) * Taoglas FXUWB10 Antenne in Unterwanne   |
|    * LM5164-Q1 72V Step-Down * BQ24075 USV & 2200mAh LiPo-Pufferakku * MicroSD-Blackbox    |
|    * Hardware Pair/Reset Taster SW1 * Automotive Deutsch DTM-12 Hauptstecker (12-Pin IP67)  |
+-+-----------------------------------------------------------------------------------------+-+
  |                                                                                         |
  v Zentraler Deutsch DTM-12 Industriestecker (Schlanker Pure-DC Kabelbaum)                 |
+-------------------------------------------+-----------------------------------------------+
| 3. SATELLITEN-POD 1 (2-Draht DC Links):   | 4. SATELLITEN-POD 2 (2-Draht DC Rechts):      |
| * Monolithisches MJF-Gehäuse (ohne PCB!)  | * Monolithisches MJF-Gehäuse (ohne PCB!)      |
| * 2 direkte Federkontakte (+5V & GND)     | * 2 direkte Federkontakte (+5V & GND)         |
| * Universal-Bucht für beliebige Kassette  | * Universal-Bucht für beliebige Kassette      |
|   (Sena Slim, Cardo Edge, Midland PMR,    |   (Sena Slim, Cardo Edge, Midland PMR,        |
|    OMM 2.4 GHz, Generic - auch 2x gleich!)|    OMM 2.4 GHz, Generic - auch 2x gleich!)    |
+-------------------------------------------+-----------------------------------------------+
  |                                                                                         |
  +-> 5. BORDNETZ & CAN: 4-adrige Zuleitung (KL30, KL15, GND, CAN_H, CAN_L)                |
  +-> 6. HECK-RADAR-ZWEIG: 2-Draht 12V Power (JWPF 2-Pin: RADAR_PWR_12V, RADAR_GND)         |
  |      Wheeltec MR20 77-GHz mmWave (PCBA 08) * Telemetrie 100% drahtlos via UWB (DW3110) +
  |                                                                                         |
  v Dedizierter UWB-Fahrzeug-Backbone (Qorvo DW3110 * 6.489 GHz Ch. 5 * Latenz < 0.4 ms)    |
+-------------------------------------------------------------------------------------------+
| 7. COCKPIT-SUBSYSTEM: Universal Front-Knoten (PCBA 05 Cockpit Hub & Sensorik)             |
| * u-blox SAM-M10Q Multi-GNSS mit integrierter Patchantenne an J12 (Qwiic I2C)             |
| * TI TMP117 Präzisions-Außentemperatur & OPT3001 Umgebungslicht im Kaltluftstrom (J12 I2C)|
| * Qorvo DW3110 UWB Transceiver auf Platinenunterseite mit FXUWB10 Antenne in Unterwanne   |
| * Automotive 4-Port USB 2.0 Hub (USB2514B) & geschalteter CarPlay-Port via TPS2051B       |
| * Knowles I2S MEMS Ambient-Mikrofon, Lenker-PTT (J3), Spiegel-LEDs (J9), Actioncam-Qi (J8)|
| * 100 % frei von internem 2.4-GHz-Funkfeuer (Null Störung für GNSS & CarPlay!)            |
+-------------------------------------------------------------------------------------------+
| 8. BEGLEITFAHRZEUG- & KOLONNEN-TOPOLOGIE (Pkw / Support-Van / Rallye / Wohnmobil):        |
| * 2 Pods an 2 Sonnenblenden: Fahrer Pod 1, Beifahrer Pod 2 (Sena/Cardo oder OMM/Midland)  |
| * Front-Node mit SAM-M10Q flach auf dem Armaturenbrett (100 % freie GNSS-Sicht)           |
| * Zentralbox mit 12V-Lader & UWB-Link * Null externe Antennen (keine Bruch-/Knickgefahr)  |
+-------------------------------------------------------------------------------------------+
+-------------------------------------------------------------------------------------------+
```

### 1.1 Das Leitmotiv: Den Lead unterstützen, nicht ersetzen

Klassische Telematik- und Assistenzsysteme neigen zum digitalen Paternalismus: Sie überfrachten das Cockpit mit Schaltempfehlungen, unaufgeforderten Stau-Warnungen und Navigations-Pop-ups. OpenMotorBridge folgt einer radikal gegensätzlichen Philosophie, die auf realer Gruppen-Fahrpraxis basiert:

* **Der Lead-Fahrer ist der beste Sensor der Welt:**
  * Kein Algorithmus und kein Satelliten-Uplink erkennt in Echtzeit Rollsplitt in der Kurve, eine unübersichtliche Baugrube, einen schleichenden Traktor oder Wildwechsel so präzise wie das geschulte Auge des vorausschauenden Tourguides.
  * Eine dreisekündige Ansage über die Intercom (*"Achtung, Baustelle rechts, wir fädeln links ein!"*) erreicht die gesamte Gruppe in Millisekunden, erfordert null Blickabwendung vom Asphalt und ermöglicht sofortige Anpassung von Tempo und Schräglage.
* **Primat der stabilen, markenübergreifenden Intercom:**
  * Die primäre Aufgabe von OpenMotorBridge ist es daher nicht, den Fahrer zu belehren, sondern die **unterbrechungsfreie Sprachkommunikation zwischen inkompatiblen Headset-Ökosystemen (Sena, Cardo, OMM)** felsenfest zu garantieren.
* **Respekt vor bewährten visuellen Signalen:**
  * Selbst bei einem unvorhergesehenen Funkausfall (z. B. leere Headset-Akkus) bricht eine gut geführte Gruppe nicht zusammen: Der aufmerksame Lead-Fahrer kontrolliert regelmäßig die Rückspiegel. Setzt ein Gruppenmitglied den rechten Blinker oder gibt Lichthupe, reagiert der Tourguide sofort und steuert die nächste Haltemöglichkeit an.
  * Digitale Systeme dürfen diese erprobten menschlichen Routinen niemals durch störende Cockpit-Menüs behindern.
* **Diskrete Signalisierung statt digitalem Paternalismus (Human-in-the-Loop):**
  * Das System unterlässt jegliche ungefragte Roboter-Sprachansagen in fremde Gruppen-Meshes (keine automatischen TTS-Durchsagen wie *"Achtung: Konvoi abgerissen!"* in den Sena/Cardo-Kanal).
  * Stattdessen informiert OpenMotorBridge den Fahrer **diskret und privat** (haptischer Alarm am Smart-Keyfob in der Jackentasche, dezenter Audio-Ping nur im eigenen Helm, optische Warn-LED am Spiegel).
  * Der menschliche Fahrer behält die volle Souveränität: Er prüft die Situation kurz im Rückspiegel oder auf dem Dashboard und entscheidet selbst, ob und wie er seine Mitfahrer mit eigener, natürlicher Stimme über die Intercom informiert. Das System stärkt die menschliche Führungskompetenz, anstatt sie zu bevormunden.

---

## 2. Modulare Systemphilosophie & Montagefreiheit (Die standardisierten Funktionsknoten)

OpenMotorBridge v8.0 definiert die Plattform über **standardisierte Funktionsknoten**:
1. **Zentralbox (Main ECU * PCBA 01):** Zentraler Rechenkern (ESP32-S3), 24-Bit Audio-DSP/Codec (ES8388), galvanische Trennübertrager, 72V Automotive Step-Down (LM5164-Q1) und LiPo-USV (BQ24075 mit 2.200 mAh Flachzelle). Beherbergt den **Semtech SX1262 LoRa-Transceiver (868 MHz)** direkt an der USV-Schiene (mit Taoglas FXP895/TG.19 Antenne in der Oberwanne) sowie den **Qorvo DW3110 UWB-Transceiver (6.5 GHz Ch. 5)** auf der Platinenunterseite (mit Taoglas FXUWB10 Flex-Antenne im Gehäuseboden). *(Typischerweise mittig unter der Sitzbank im Batteriefach oder im Pkw-Cockpit montiert).*
2. **Satelliten-Pod 1 (Bucht Links):** Universal-Wechselschacht für beliebige Kassetten (Sena SPIDER X Slim, Cardo Packtalk Edge, UCS-Standard, OMM 2.4 GHz oder Midland PMR446). Monolithisches MJF-Gehäuse mit direkten 2-Draht DC-Federkontakten (PCBA 02 ist ersatzlos entfallen).
3. **Satelliten-Pod 2 (Bucht Rechts):** Baugleicher, vollkommen symmetrischer Universal-Wechselschacht für beliebige Kassetten (auch 2x die gleiche wie in Bucht 1, z. B. 2x Midland auf getrennten Kanälen oder 2x Cardo/Sena in getrennten Gruppen). Nutzt exakt dasselbe monolithische Pod-Gehäuse mit direkten 2-Draht DC-Federkontakten. *(Typischerweise gegenüberliegende Fahrzeugseite zur maximalen HF-Raumdiversität).*
4. **Front-Node (Cockpit, Camera & Sensor Hub * PCBA 05):** Autonomer ESP32-S3 Satellit, integriertes **u-blox SAM-M10Q Multi-GNSS** (an Port `J12` Qwiic $I^2C$ mit freier Sicht in den Zenit), **TI TMP117** Präzisions-Außentemperaturfühler und **OPT3001** Umgebungslichtsensor im Kaltluftstrom der Frontverkleidung. Beherbergt den **Qorvo DW3110 UWB-Transceiver** auf der Platinenunterseite (mit Taoglas FXUWB10 Antenne im Gehäuseboden), Automotive USB 2.0 Hub für die Headless CP2AA-Bridge, 5 GHz Wi-Fi, geschalteten VBUS via TPS2051B, digitalen PTT-Tastereingang (`J3`), BSD Totwinkel-Spiegel-LEDs (`J9`), drahtloses Actioncam-Induktionsdock (`J8`), TCAN334G CAN-Transceiver und Knowles I2S MEMS-Windgeräuschmikrofon. *(Typischerweise unsichtbar in der Cockpitverkleidung oder Scheinwerfermaske).*
5. **Radar 2.0 Sub-MCU & Halo-Wings (PCBA 08 am Heck):** Autonomes 77-GHz Heck-Radar, versorgt über Peitsche 3 des Deutsch DTM-12 Kabelbaums mit reiner 2-Draht 12V DC-Power; Telemetrie und Kollisionswarnungen werden zu 100 % drahtlos über Ultra-Wideband (Qorvo DW3110) an die Zentralbox übertragen.

```
                     DIE STANDARDISIERTEN FUNKTIONSKNOTEN
+-----------------------------------------------------------------------------+
| 1. FRONT-NODE (Cockpit/Nacelle):  SAM-M10Q GNSS, Kaltluft-Sensorik (J12),   |
|    UWB-Backbone (6.5 GHz), USB-Hub, CP2AA Bridge, PTT, Cam-Qi & Wind-MEMS   |
+-----------------------------------------------------------------------------+
| 2. ZENTRALBOX (Unter Sitz/Akku):  DSP Audio-Matrix, LoRa 868MHz (SX1262),   |
|    UWB-Backbone (DW3110), USV-Pufferung, CAN-Bus, Deutsch DTM-12 Hauptflansch|
+------------------------------+----------------------------------------------+
| 3. POD 1 (Bucht Links):      | 4. POD 2 (Bucht Rechts):                     |
| * Universal-Schacht Bucht 1  | * Universal-Schacht Bucht 2                  |
| * Beliebige Kassetten        | * Beliebige Kassetten (auch 2x gleich!)      |
| * Monolithisch (kein PCB 02!)| * Monolithisch (kein PCB 02!)                |
+------------------------------+----------------------------------------------+
| 5. REINES OPTIONALES HECK-RADAR (An 2-Draht 12V Power am Heck):             |
| * Wheeltec MR20 77-GHz mmWave (PCBA 08) * Telemetrie 100% drahtlos via UWB  |
+-----------------------------------------------------------------------------+
```

> [!NOTE]
> **Montagefreiheit - *Your Vehicle, Your Choice*:**  
> Wo und wie ihr diese Module an eurem Fahrzeug platziert, ist bewusst **völlig euch überlassen**! OpenMotorBridge stellt die standardisierten Elektronik- und Gehäuse-Dimensionen sowie die Schnittstellen bereit.  
> Für ausgewählte Plattformen liefern wir in **[Kapitel 08 (Mechanik & Gehäuse)](08_enclosures_mechanics_cad.md)** komplett durchentwickelte, 100 % schraub- und klebefreie **Referenz-Montagekits** mit:
> * **Referenz-Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring):** Pod 1 & 2 geschützt in den Kofferdeckeln (Zero-Drill an Scharnierschrauben, 19 mm MagSafe Seitendurchführung in Koffer-Innenwand neben Kofferhalter), Front-Node am Geweihträger hinter der Sharknose-Außenhaut (mit SAM-M10Q GNSS und Kaltluft-Sensoren), Zentralbox im Batteriefach unter dem Sitz, optionales Radar an Peitsche 3 am Kennzeichenträger. *(Heckbürzel bleibt 100 % unberührt - kein Pod 3 unter der Forged-Carbon-Cowl!)*
> * **Referenz-Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 1 & 2 in den Kofferdeckeln (MagSafe Seitendurchführung), Front-Node unsichtbar in der 7"-Scheinwerfer-Nacelle, Zentralbox unter der Sitzbank. *(Die Touring Fender Console entfällt ersatzlos - der Heckkotflügel an der 1/4"-20 Sitzmutter bleibt 100 % serienmäßig clean!).*
> * **Referenz-Kit 3 (Classic Bagger & Cruiser - Street Glide / Electra Glide):** Pod 1 & 2 in den Kofferdeckeln, Front-Node in der Batwing-Verkleidung, Zentralbox unter dem Sitz, optionales Radar unter dem Kennzeichen an Peitsche 3.
> * **Referenz-Kit 4 (Adventure & Touring Enduros - BMW GS, KTM Adventure, Africa Twin):** Pod 1 & 2 werden **strikt fahrzeugfest am Motorrad** montiert: Entweder am Rohr-Kofferträger über das geschützte Heavy-Duty GSA Cage Dock ([`adventure_gsa_cage_dock.scad`](../../hardware/cad/scad/02_pod_base/adventure_gsa_cage_dock.scad)) im $45\,\text{mm}$ Totraum zwischen Kofferinnenwand und Rahmen, oder in der Sitzbank-Bügelfalte über das aerodynamische Transition Dock ([`adventure_transition_dock.scad`](../../hardware/cad/scad/02_pod_base/adventure_transition_dock.scad)). *(Strikte HF-Regel: Eine Montage im Inneren von Aluminium-Koffern ist physikalisch verboten, da Aluminium als Faradayscher Käfig 2,4-GHz- und UWB-Signale vollständig blockiert!).* Front-Node an der Navigationsstrebe hinter dem Windschild (freie GNSS-Sicht). Am Heckträger sitzt lediglich der schlanke, rein **optionale Radarträger** ([`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/05_accessories/adventure_rack_radar_mount.stl)) an Peitsche 3 - wer kein Radar fährt, montiert am Heck **überhaupt nichts**!
> * **Referenz-Kit 5 (Pkw / Support-Van / Rallye-Begleitfahrzeug / Wohnmobil):** 
>   * **2 Pods an 2 Sonnenblenden:** Fahrer-Sonnenblende = Pod 1, Beifahrer-Sonnenblende = Pod 2.
>     - *Modus A (Begleitfahrzeug Motorrad-Tour):* Pod 1 Sena SPIDER X Slim, Pod 2 Cardo Packtalk Edge oder Midland PMR446.
>     - *Modus B (Reine Auto-Kolonne / Offroad / Camper):* Pod 1 OMM 2.4 GHz Wechselkassette (HD-Audio-Mesh zwischen OMB-Fahrzeugen), Pod 2 Midland PMR446 Wechselkassette (Jedermann-Funk zu LKW, Streckenposten).
>     - *Modus C (Hybrid-Lead & OMM-Anchor):* Pod 1 OMM 2.4 GHz Wechselkassette (verbindet alle OMB-Bikes), Pod 2 Sena oder Cardo für Gastfahrer.
>   * **Armaturenbrett:** Front-Node mit u-blox SAM-M10Q flach an der Frontscheibe (100 % freie Sicht zum Himmel); Zentralbox auf vibrationsgedämpfter Keilaufnahme ([`car_dashboard_wedge_dock.stl`](../../hardware/cad/stl/05_accessories/car_dashboard_wedge_dock.stl)) mit 12V Zigarettenanzünder-PD-Speisung; drahtlose UWB-Verbindung zur Front; **null externe Antennen** (keine Knick-/Bruchgefahr beim Sonnenblenden-Kappen).

### 2.1 Whitepaper-Entwurfsentscheidung: Dezentrale Satelliten-Topologie vs. Monolithische Single-Box

In der frühen Konzeptphase wurde intensiv evaluiert, ob das gesamte System in einem einzigen, großen Zentralgehäuse (z. B. unter der Sitzbank oder hinter der Frontverkleidung) untergebracht werden sollte. Der monolithische Ansatz wurde nach physikalischen und messtechnischen Voruntersuchungen einstimmig verworfen:

#### Evaluierungsmatrix: Monolithische Zentralbox vs. OpenMotorBridge Satelliten-Architektur

| Bewertungskriterium | Option A: Monolithische Single-Box | Option B: Reine Lenker/Cockpit-Box | **Option C: OMB Dezentrale Satelliten (Gewählt)** |
| :--- | :--- | :--- | :--- |
| **HF-Selbststörung (Desensing)**| **Kritisch:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V Buck-Regler auf engstem Raum | **Kritisch:** Starkes Übersprechen auf Cockpit-TFT und Radio-Antenne | **Optimal (> 45 dB Isolation):** GNSS im Cockpit, Intercoms an den Heckflanken (Pod 1 & 2), UWB-Backbone auf 6.5 GHz |
| **Kabelbaum-Durchmesser** | **Massiv:** 26+ Einzelleitungen müssen quer durch das gesamte Motorrad gezogen werden | **Schlecht:** 18 Leitungen über den schwenkenden Lenkkopf (Kabelbruch-Risiko) | **Ultra-Schlank:** Deutsch DTM-12 Kabelbaum mit reinen 2-Draht-DC-Power-Peitschen; Daten 100% drahtlos via UWB |
| **Thermische Verlustleistung** | **Hot-Spot (> 18 W):** 72V DC/DC + Audio-Endstufen + Akkuladung unter der Sitzbank | **Thermischer Hitzetod (> 85 °C):** Stauwärme direkt hinter der Scheinwerfermaske | **Perfekt verteilt:** Max. 3-4 W pro Gehäuse; passive Wärmeabfuhr ohne Hotspots |
| **GNSS-Zenitsicht & Radar** | **Verschattet:** Sitzbank und Fahrer-Körper blockieren Satelliten & Heck-Sichtfeld | **Schlecht:** Heck-Radar vom Lenker aus physikalisch unmöglich | **Ideal:** SAM-M10Q hat freie Sicht durch Windschild; Radar hat freie Sicht nach hinten an Peitsche 3 |
| **Fahrtwind-Abtastung (AGC)** | **Physikalisch unmöglich:** Unter der Sitzbank herrscht kein dynamischer Staudruck | **Möglich:** Windmessung direkt am Lenker | **Exzellent:** Knowles I2S MEMS direkt an der Frontscheibe im Front-Node |

1. **Die Physik der HF-Koexistenz (Vermeidung von Receiver Desensitization):**
   * GNSS-Signale treffen die Erde mit extrem schwachen Pegeln von ca. **$-130\,\text{dBm}$ bis $-160\,\text{dBm}$**.
   * Die Auslagerung von Multi-GNSS in das Cockpit (Front-Node) platziert den Empfänger direkt unter die dielektrische Kunststoff-Scheibe mit ungetrübtem $180^\circ$-Blickwinkel zum Himmel.
   * Durch die Verbannung von OMM 2.4 GHz aus dem Cockpit und den Einsatz der **UWB-Funkbrücke (6.5 GHz)** herrscht im Cockpit vollkommene Ruhe im 2.4-GHz-Spektrum. Das GNSS leidet unter null Anhebung des Grundrauschens (*Noise Floor Lift*).
   * Die räumliche Trennung zwischen Front-Cockpit und den Heck-Pods (Pod 1 links, Pod 2 rechts) garantiert physikalisch über **$46\,\text{dB}$ Freiraumdämpfung** zwischen den 2.4-GHz-Mesh-Stufen und der Cockpit-Elektronik.
2. **Kabelbaum-Zuverlässigkeit über den Lenkkopf:**
   * Jedes Kabel, das über den beweglichen Lenkkopf geführt wird, unterliegt während der Fahrzeuglebensdauer Millionen von Biegewechseln.
   * Durch die Auslagerung der Cockpit-, Display- und PTT-Funktionen in den **Front-Node (PCBA 05)**, der über die hochzuverlässige, drahtlose **UWB-Funkbrücke (Qorvo DW3110, $< 0{,}4\,\text{ms}$ Latenz)** mit der Zentralbox kommuniziert, entfallen sämtliche empfindlichen Datenleitungen über die Lenkachse.
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
* **Klasse S (Smart Modular Cartridge mit Mechatronik * OMB-Referenz):** z. B. Sena SPIDER X Slim (Primärempfehlung), Sena 60S, Cardo Edge - 100 % ungeöffnetes Originalgerät im PA12-MJF Konturbett mit 3-Punkt EPDM-Dämpfung gegen $20\,\text{g}$ Vibration, 4 unabhängige mechatronische Aktuatoren auf PCBA 03 Rev 2.0 (WCH CH32V003 RISC-V Controller, In-System Flashing via Pin 5 UART), direkte $3{,}85\,\text{V}$ DC-Speisung ab Werk, null Pogo-Pins, null Löten, 100 % Erhalt von Werksgarantie & IPX-Schutz.
* **Klasse A (Drahtlos-Bridges & USB-Speisung):** z. B. Sena +Mesh (B2M-01), Sena MeshPort Blue/Red - versorgt über flaches 90° Micro-USB/USB-C Kabel, drahtlose Audioübertragung zum Helm, externe SMA-Bulkhead-Doppelbuchse mit Schutzkappe an der Frontblende.
* **Klasse B (Pogo-Pin Federkontakt-Cradles):** z. B. Sena 50S/60S/30K/20S EVO - vollwertiges analoges Audio (ES8388 Codec auf PCBA 03) und PTT-Tastung via AO3400A MOSFETs.
* **Klasse C (Magnetischer Air-Mount):** z. B. Cardo Packtalk Edge / Pro (Hinweis: Packtalk Neo unterstützt kein Laden während der Fahrt und ist ausgeschlossen) - werkzeugloses magnetisches Andocken über 2x N52 Neodym-Magnete.
* **Klasse D (Schiebe-Cradles):** z. B. Cardo Packtalk Bold/Black, Freecom-Serie - mechanische Gleitschiene mit Arretierfeder.
* **Klasse E (Analoger PMR446 Funk):** z. B. Midland G7/G9 Pro, XT30, Kenwood - 2-Pin Doppelklinkenanschluss mit PhotoMOS-PTT-Tastung.
*(Detaillierte Verkabelungsmatrix siehe [Spezifikation 02](02_intercom_matrix_profiles.md)).*

---

## 3. HF-Koexistenz & Raumdiversität ($> 35\,\text{dB}$ Entkopplung)

Werden Sena- und Cardo-Mesh-Geräte gleichzeitig betrieben, muss eine gegenseitige Blockade der 2,4-GHz-Empfänger zuverlässig verhindert werden:

1. **Räumliche Distanzierung ($d \ge 45\,\text{cm}$ durch Fahrzeug-Flankentrennung):**
   * **Keine Pod-Montage am Helm:** Die schweren Pods ($110 \times 54 \times 28\,\text{mm}$ Kassetten) verbleiben grundsätzlich fest am Fahrzeug (z. B. linker und rechter Kofferdeckel, Rahmenrohre oder Sturzbügel). Die Helme von Fahrer und Sozius bleiben zu 100 % kabel- und pod-frei.
   * **Physische & metallische Barriere:** Pod 1 (linke Fahrzeugflanke / linker Koffer) und Pod 2 (rechte Fahrzeugflanke / rechter Koffer) nutzen den massiven Motorradrahmen, den Kraftstofftank, den Motorblock und die Heckstruktur als natürliche metallische HF-Abschirmung.
2. **Schirmdämpfung:**
   * Die Freiraumdämpfung über $> 50\,\text{cm}$ in Kombination mit der massiven metallischen Abschirmung durch die Fahrzeugstruktur erzielt eine **HF-Entkopplung von $> 35\,\text{dB}$**.
   * Damit sinkt der Einkopplungspegel des Nachbarsenders unter $-15\,\text{dBm}$, wodurch die Eingangs-LNAs beider Headsets im linearen Bereich arbeiten und kein *De-Sensing* auftritt.
3. **Klare Frequenzzonen & UWB-Fahrzeug-Backbone:**
   * Durch die Verbannung von OMM 2.4 GHz aus dem Cockpit und den Entfall von Pod 3 ist das Motorrad in absolut saubere Funkzonen gegliedert:
     * **Heckflanken (2.4 GHz):** Pod 1 (Sena) und Pod 2 (Cardo) sind durch Rahmen und Tank gegeneinander $> 35\,\text{dB}$ und zum Cockpit $> 46\,\text{dB}$ isoliert.
     * **Zentralbox (868 MHz LoRa & 6.5 GHz UWB):** Sitzt geschützt unter der Sitzbank an der USV-Schiene für 24/7 Diebstahlschutz und PTT-Backbone.
     * **Cockpit (1.575 GHz GNSS & 6.5 GHz UWB):** Völlig frei von störendem 2.4-GHz-Dauerfeuer.

---

## 4. Physische Schnittstellen & Signalmatrix

### 4.1 Zentralbox Deutsch DTM-12 Hauptkabelbaum (Reiner Pure-DC & CAN Strang)
Die Verbindung aller Basis-Komponenten erfolgt über den zentralen, wasserdichten **Deutsch DTM-12 Industriestecker (IP67/IP69K)** an der Zentralbox:

| Zweig / Kabel | Anschlusstyp | Zielkomponente | Übertragene Signale / Querschnitt |
| :--- | :--- | :--- | :--- |
| **Peitsche 1 (250 mm)** | JST-JWPF / Superseal 2-Pin | **Satelliten-Pod 1** (Sena SPIDER X Slim / OMM 2.4 GHz) | `POD1_VCC` (+12V geschaltet, AWG22 0.34²), `POD1_GND` (Masse, AWG22 0.34²) |
| **Peitsche 2 (250 mm)** | JST-JWPF / Superseal 2-Pin | **Satelliten-Pod 2** (Cardo Edge / OMM 2.4 GHz / Midland) | `POD2_VCC` (+12V geschaltet, AWG22 0.34²), `POD2_GND` (Masse, AWG22 0.34²) |
| **Peitsche 3 (250 mm)** | JST-JWPF / Superseal 2-Pin | **Heck-Radar** (Radar 2.0 Sub-MCU PCBA 08) | `RADAR_PWR_12V` (+12V geschaltet, AWG22 0.34²), `RADAR_GND` (Masse, AWG22 0.34²) |
| **Peitsche 4 (250 mm)** | AMP Superseal 1.5 6-Pin | **Bordnetz & CAN** (Motorrad oder Pkw) | `KL30_IN` (12V Dauer, AWG20 0.5²), `KL15_IGN` (12V Zündung, AWG22 0.34²), `VEHICLE_GND` (AWG20 0.5²), `CHASSIS_EARTH` (AWG20 0.5²), `CAN_H` / `CAN_L` (AWG24 0.22²) |

*(Hinweis: Durch die All-UWB Funkarchitektur entfällt jegliche Signal- und Audioverdrahtung. Es werden nur noch 2-adrige Gleichstrompeitschen geführt!)*

### 4.2 Universal Front-Node (PCBA 05) Cockpit-Schnittstellen
Der Front-Node wird im Cockpit autark über eine 2-polige 12V-Leitung an Zündungsplus (KL15) versorgt und bündelt sämtliche Front-Komponenten:
* **Cockpit & Sensoren:** u-blox SAM-M10Q Multi-GNSS (Zenitsicht an J12), TI TMP117 Außentemperatur & OPT3001 Umgebungslicht im Kaltluftstrom.
* **Bedienelemente & Anzeigen:** 3-Tasten Lenker-PTT (J3), Totwinkel-Spiegel-LEDs (J9), Actioncam-Ladedock (J8), Zusatzscheinwerfer (J11).
* **Infotainment & USB:** Automotive 4-Port USB 2.0 Hub (USB2514B) mit 20W USB-PD Lenker-Ladeport (J5), geschaltetem CarPlay-Port (J6 via TPS2051B) und Host-Port zur Headunit (J4).
* **Detaillierte Pinbelegung & Schaltpläne:** Die vollständige elektrische Pinbelegung aller Steckverbinder (JST-PH, Molex, Qwiic) sowie Leitungsspezifikationen sind autoritativ in **[Kapitel 07: PCBA Hardware, Pinouts & Spezifikationen](07_pcba_hardware_pinouts.md)** dokumentiert.

---

## 5. Integration in OEM-Infotainmentsysteme

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 WHIM-Emulation & Apple CarPlay / Android Auto Freischaltung
* **Hintergrund:** Apple CarPlay setzt im Fahrzeug ein betriebsbereites Sprachmikrofon voraus. Harley-Davidson verriegelt CarPlay in der Boom! Box GTS Firmware standardmäßig und verlangt entweder das kabelgebundene 7-Pin DIN-Headset oder das proprietäre Bluetooth-Funkmodul **HD-WHIM** (*Wireless Headset Interface Module*, $> 350\,\text{€}$).
* **Elektrische Impedanz-Emulation:** OpenMotorBridge emuliert an den Audio-Schnittstellen über ein präzises Widerstands- und Übertragernetzwerk die charakteristische elektrische Gleich- und Wechselstrom-Impedanz ($1{,}0 \dots 2{,}2\,\text{k}\Omega$) eines aktiven OEM-Mikrofons.
* **Ergebnis:** Die Boom! Box GTS schaltet Apple CarPlay und Android Auto im 6,5"- bzw. 12,3"-Fahrzeugdisplay sofort frei - **ohne teures WHIM-Modul** und ohne unsichere Jumper-Stecker.
* **Nahtloses Ducking:** Navigationsansagen der Boom! Box werden über den ES8388 Codec priorisiert und über die aktiven Intercom-Gespräche mit einstellbarem Ducking ($-12\,\text{dB}$) sanft eingeblendet.

#### 5.1.2 Universal Cockpit & Front Hub (PCBA 05): USB-Subsystem, Live-Traffic & PTT
Der Front-Knoten (PCBA 05) dient auf **allen Motorrädern** als universeller Cockpit-Knoten und eliminiert empfindliche Signalkabel über den mechanisch beanspruchten Lenkkopf:
* **Drahtlose Funkbrücke zur Zentralbox:** Ein autonomer Controller-Knoten (ESP32-S3-WROOM-1U mit Vektor-DSP) hinter der Verkleidung kommuniziert über **UWB (Qorvo DW3110 / 6,5 GHz Ch. 5, $< 0{,}4\,\text{ms}$ Latenz)** und **BLE 5.0 (2M-PHY)** mit der Zentralbox.
* **Drahtgebundener Lenker-PTT (Optokoppler an `J3` / GPIO 0, $< 1{,}8\,\text{ms}$ Latenz):** Nur $30\dots 50\,\text{cm}$ kurzes, geschütztes Kabel am Lenker - kein bruchgefährdetes Signalkabel über den schwenkenden Lenkkopf nach hinten zur Zentralbox!
* **Digitales I2S-MEMS Ambient-Mikrofon (Knowles SPH0645LM4H-6):** Berechnet Umgebungs- und Fahrtwindgeräusche (dB-A/RMS) direkt an der Front für automatische Helmlautstärke-Nachführung (AGC) via Xtensa Vektor-DSP.
* **Automotive USB 2.0 Subsystem (Microchip USB2514B & TI TPS2051B):**
  * **Upstream Host Port (`J4`):** Führt direkt zum USB-Eingang der Harley-Davidson Boom! Box GTS / Skyline OS im Handschuhfach.
  * **Downstream Port 1 (`J5` / Lenker-Smartphone):** High-Speed Daten + 20W Automotive USB-PD Fast Charging (Southchip SC8102, 9V/2.2A & QC 3.0) für Smartphones am Lenker (QuadLock/SP Connect).
  * **Downstream Port 2 (`J6` / CP2AA-Dongle):** Geschalteter $+5{,}0\,\text{V}$ VBUS über `TI TPS2051B` Lastschalter mit softwaregesteuertem **2,5s-Kaltstart**, automatischem **Not-Power-Gating bei Verkleidungshitze** und 0.0 µA Deep-Sleep. Führt über ein $25\dots 30\,\text{cm}$ geschirmtes Kabel zum CP2AA-Dongle (3M Dual-Lock im Verkleidungshohlraum).
  * **Downstream Port 3 (Handschuhfach):** Durchgeschliffenes USB-Kabel ins Handschuhfach - bleibt zu **$100\,\%$ frei für MP3/FLAC USB-Sticks und offizielle OEM-Software-Updates** (inkl. hardwareseitiger Port-Sense Überwachung).
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

### 5.3 Heck-Radar 2.0 & Totwinkel-Assistent (Wheeltec MR20 77 GHz mmWave & Garmin Varia) an dediziertem Heck-Träger
* **Heck-Montage & Justage (Ohne Pod 3):** Das Heck-Radar wird vollkommen autark und ohne zusätzliches Gehäuse direkt über einen dedizierten, minimalen Halter (z. B. [`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/05_accessories/adventure_rack_radar_mount.stl) unter der Gepäckbrücke oder modellspezifische Adapter) montiert. Die Anbindung erfolgt über Peitsche 3 des Deutsch DTM-12 Kabelbaums (Pins 10-11: 12V geschaltet, GND); die 20 Hz Radar-Zieltelemetrie wird 100% drahtlos via UWB (DW3110) an die Zentralbox übertragen. Eine bionische Hirth-Verzahnung ermöglicht eine verzugsfreie 100% waagerechte Ausrichtung.
* **Dual-Radar-Architektur (Zwei austauschbare Radar-Engines):**
  * **Radar 2.0 (Wheeltec MR20 77 GHz mmWave - Standard):**
    - Integriert in IP67-Flügel-Gehäuse ([`radar_mr20_housing.scad`](../../hardware/cad/scad/05_accessories/radar_mr20_housing.scad)) mit PCBA 08 (ESP32-C5 Dual-Band Sub-MCU).
    - 77 GHz FMCW Horn-Array mit $\pm 60^\circ$ ($120^\circ$) horizontaler Erfassung und bis zu $90\,\text{m}$ Reichweite.
    - 36-LED Neopixel-Doppel-Warnflügel (18 links, 18 rechts): Richtungsbezogene Totwinkel-Warnung, Bremslicht-Strobe bei Verzögerung $> 0{,}4\,g$, dynamisch expandierender Annäherungs-Halo bei herannahendem Verkehr ($TTC < 2{,}5\,\text{s}$).
    - Autarke 5.9 GHz ITS-G5 (V2X) Keramik-Patchantennenkammer im linken Flügel für Car-to-X Sicherheitswarnungen.
    - Binder Serie 707 M5 4-Pin IP67 Schnittstelle (Power + Macro-UART), mechanisch entkoppelt.
  * **Radar 1.0 (Garmin Varia RTL515 / eRTL615 - Legacy):**
    - 24 GHz Doppler-Streaming (0xAA Preamble, $140\,\text{m}$ Erfassung, $20\,\text{Hz}$ Update) über GoPro Lock Dock.
* **Dynamische Bedrohungs-Klassifikation & Time-To-Collision (TTC):**
  * $\text{TTC} = \frac{d}{v_{\text{rel}}}$.
  * **Grün (Clear):** Kein Fahrzeug im Gefahrenbereich oder $v_{\text{rel}} \le 10\,\text{km/h}$.
  * **Gelb (Annäherung):** $d \le 80\,\text{m}$ und $v_{\text{rel}} > 15\,\text{km/h}$ (Fahrzeug nähert sich normal).
  * **Rot (Kollisionsrisiko):** $\text{TTC} < 3{,}5\,\text{s}$ oder ($d \le 35\,\text{m}$ und $v_{\text{rel}} > 25\,\text{km/h}$).
* **Akustische Helm-Warnung (Prio-1 Ducking):** Bei Bedrohung (Gelb/Rot) senkt die Audio-DSP-Pipeline Musik und Intercom sofort auf **$-18\,\text{dB}$** ab ($< 15\,\text{ms}$ Attack) und spielt einen prägnanten **synthetisierten Doppelton-Ping** ($880\,\text{Hz} \rightarrow 1760\,\text{Hz}$ bei Gelb bzw. $988\,\text{Hz} \rightarrow 1976\,\text{Hz}$ bei Rot) ins Fahrer-Headset.
* **Astronomische Dimmung & Tunnel-Erkennung:**
  * Berechnung des Sonnenstandswinkels $\alpha_{\text{sun}}$ aus GNSS-Koordinaten und UTC-Zeit: Dimm-Level von 100 % (Tag) über Dämmerung bis 18 % (Nacht).
  * **Tunnel-Detektor:** Abriss des GNSS-Signals ($Fix = 0$ für $> 1{,}5\,\text{s}$) bei $v > 30\,\text{km/h}$ schaltet die Totwinkel-LEDs sofort auf Nacht-Dimmung (18 %), um Blendung im Rückspiegel zu verhindern.
* **Blinker-Kopplung:** Bei Rechtsblinken Überwachung der linken Vorfahrtsspur; bei Linksblinken zwingende Überwachung beider Spuren.

#### 5.3.1 Autarke Wettertrend-Engine (BMP390 mit GNSS-Höhenkompensation)
* **Physikalischer Luftdruck-Trend:** Normierung des gemessenen Absolutdrucks über die GNSS-Ellipsoidhöhe ($P_0 = P \cdot (1 - h / 44330)^{-5.255}$).
* **Trend-Klassifikation:** Erkennt barometrische Druckabfälle $> 2{,}0\,\text{hPa/h}$ oder Temperaturstürze $> 3\,^\circ\text{C}/15\,\text{min}$ als herannahende Unwetterfront - autark ohne Mobilfunk-Uplink.
* **Fahrsicherheits-Anzeige:** Warnmeldung erfolgt im Stillstand ($v = 0\,\text{km/h}$) oder bei Rastpausen.

#### 5.3.2 Notbremsblinken (Emergency Stop Signal - ESS) über das Heck-Radar & Power-Port
* **Funktionsweise (100% CAN Listen-Only konform):**
  * Erkennt die 6-Achsen-IMU der Zentralbox eine massive Gefahrenbremsung ($a_x < -6{,}0\,\text{m/s}^2$ bzw. $> 0{,}6\,\text{g}$ Verzögerung aus hohem Tempo):
  * Sendet OpenMotorBridge über UART Makrobefehle:
    - Am Radar 2.0 (Wheeltec MR20): Triggert die beiden 18-LED Neopixel-Warnflügel (36 LEDs gesamt) in einen ultrahellen, synchron pulsierenden $4{,}5\,\text{Hz}$ Bremslicht-Stroboskop-Blitz.
    - Am Garmin Varia: Sendet `SET_LIGHT_MODE: STROBE_4HZ`.
  * **Ergebnis:** Höchste Warnwirkung für nachfolgende Fahrzeuge, **völlig ohne Eingriff in die originale Fahrzeug-Bremsleitung**.

#### 5.3.3 TI TMP117 Hochpräzisions-Außentemperatur & Glatteis-Wächter (Port J12 an Front Node)
* **Messort & Cockpit-Integration:**
  * Der digitale Temperatursensor **TI TMP117** ($\pm 0{,}1\,^\circ\text{C}$ Laborpräzision nach NIST, 16-Bit I2C) ist direkt über den Qwiic-Port `J12` des Front Nodes (PCBA 05) angebunden.
  * Er sitzt geschützt im laminaren Kühlluft-Einlass (Cold Air Scoop) der Frontverkleidung - thermisch vollständig entkoppelt von Motorabwärme und direkter Sonnenbestrahlung.
* **I2C Busprotokoll & Auflösung:**
  * 16-Bit Auflösung ($0{,}0078\,^\circ\text{C}$ LSB, Messintervall 1,0 s).
* **Glatteis-Frühwarnung (Black Ice Guard):**
  * Sinkt die gemessene Temperatur auf $T \le +3{,}0\,^\circ\text{C}$ (Gefahr von überfrierender Nässe und Reifglätte auf Brücken und Pässen), triggert OMB eine zweistufige Sicherheitsreaktion:
    1. **Akustischer Warnton:** Ein diskreter, tiefer Doppelton-Ping ($440\,\text{Hz} \rightarrow 330\,\text{Hz}$) wird einmalig ins Headset eingespielt.
    2. **Visuelles Glatteis-Symbol:** Im PWA Ride HUD und auf den Spiegel-LEDs (`J9`) wird das blaue Eiskristall-Warnsymbol aktiv, bis die Temperatur dauerhaft $+4{,}5\,^\circ\text{C}$ überschreitet (Hysterese gegen Flackern).

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
       > *"🚨 DIEBSTAHLWARNUNG: Dein Motorrad wird bewegt! (Distanz: 180 m)"*

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
  * OMB schaltet das Helmmikrofon für das Weitverkehrs-Mesh automatisch stumm (leiser Quittungston im Helm: *"Lokal-Modus"*).
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
* **Cockpit-Docking & Induktivladung:**
  * Auf dem Motorrad rastet der Keyfob magnetisch am Cockpit-Dock ein und wird über die integrierte Qi-Ladespule während der Fahrt 100 % kabellos nachgeladen.

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
  * Zusammen mit der IMU-Erschütterungsüberwachung ($6\,\mu\text{A}$) liefert der interne **2.200 mAh LiPo-Pufferakku** eine autarke Ortungs- und Alarmbereitschaft von **3 bis 4 Jahren** - selbst wenn Diebe die 12V-Bordbatterie trennen.

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
* **Systemweite Hochfrequenz-Architektur (Die 5 Funkbänder der OpenMotorBridge):**
  1. **UWB (6.489 GHz Ch. 5 / Qorvo DW3110):** Universeller, deterministischer Daten- und Audio-Backbone zwischen allen Knoten (Zentralbox, Front-Node, Pod 1, Pod 2, Heck-Radar). Null De-Sensing auf 2.4 GHz, Latenz $< 0{,}4\,\text{ms}$, AES-128-CCM verschlüsselt. Im Nahbereich (30-80 m) zusätzlich hochpräzises Inter-Bike Ranging für Platoon-Spacing und Konvoiführung.
  2. **Heck 5.9 GHz V2X & 77 GHz mmWave:** Externe 5.9 GHz V2X-Patchantenne (C-V2X / DSRC) am Heck plus Wheeltec MR20 mmWave Radar für 360°-Umfeldüberwachung und Notfall-Kollisionsstrobe.
  3. **Front 5 GHz Wi-Fi:** Dedizierter High-Speed Funklink am Front-Knoten für drahtloses Apple CarPlay und Android Auto (Headless CP2AA Bridge).
  4. **2.4 GHz Audio & Konnektivität:**
     * *Zentralbox:* Dedizierter Qualcomm HD-Bluetooth Audio-SoC (QCC3084) mit Dual-A2DP und LE Audio / Auracast (synchroner Audio-Mix für Fahrer- und Sozius-Helm) samt HFP-Telephonie-Engine; ESP-internes BLE rein für PWA Dashboard; Wi-Fi für Track-Upload und Handy-Proxy.
     * *Front-Node:* BLE für Action-Cam Steuerung (GoPro, Insta360, DJI).
  5. **LoRa 868 MHz (Semtech SX1262):** 3-Kanal-Langstrecken-Backbone zwischen den Fahrzeugen (Public Announcement, Private Session Group, Micro-Cluster/FOB-Pager) mit kilometerweiter Reichweite.

### 5.12 Kognitive Cockpit-Entlastung & Stille Absicherung im Hintergrund
* **Strikte Grenzziehung: Wann Automatisierung eingreift - und wann sie schweigt:**
  * Digitale Telemetrie und Sensorik greifen ausschließlich dort ein, wo die menschliche Sprache oder Wahrnehmung physikalisch versagt:
    1. **Sturz & eCall bei Handlungsunfähigkeit:** Liegt ein Fahrer nach einem Unfall mit $> 6{,}5\,\text{g}$ und $> 70^\circ$ Schräglage regungslos im Graben, ist er oft bewusstlos oder das Headset-Kabel ist abgerissen. Hier alarmiert die automatische LoRa-Notrufflut (868 MHz) mit GPS-Koordinaten autonom die Gruppe.
    2. **Gruppen-Abriss über Funkdistanz (Lost-Rider Tracking):** Überschreitet der Abstand zum Schlusslicht im Gebirge die 2,4-GHz-Audio-Reichweite ($> 1{,}5\,\text{km}$), meldet das 868-MHz-LoRa-Paket dem Guide lautlos und dezent die Distanz zum Zurückgefallenen.
    3. **Unsichtbare Gefahrenzonen:** Ein sich mit $+60\,\text{km/h}$ im toten Winkel näherndes Fahrzeug (Heck-Radar Garmin Varia) oder ein schleichender Druckabfall im Reifen (TPMS) werden frühzeitig erkannt, bevor das Motorrad instabil wird.
    4. **Parkplatzwächter (Zündung AUS):** Erschütterungen des abgestellten Motorrads werden lautlos an den 2-in-1 LoRa Smart-Keyfob (LRA-Pager) in der Jackentasche des Fahrers gemeldet.
* **Absolutes Push-Verbot für allgemeine Verkehrs- & Wettertexte während der Fahrt ($v > 0$):**
  * Weder Staumeldungen noch Wettertexte oder CAN-Spritstand-Broadcasts werden während der Fahrt auf das Display gepusht. Die kognitive Last des Fahrers bleibt zu 100 % für die Fahrzeugbeherrschung und die Blickführung frei.

### 5.13 Begleitfahrzeug- & Support-Van-Architektur (Rallye, Besenfahrzeug, Tour-Orga)
* **Rolle des Begleitfahrzeugs in organisierten Gruppen:**
  * Bei Alpentouren, geführten Gruppenreisen, Wüstenrallyes oder Fahrsicherheitstrainings fährt häufig ein Begleitfahrzeug (Kastenwagen, Van, Wohnmobil) mit Ersatzteilen, Werkzeug, Reisegepäck und Erste-Hilfe-Ausrüstung im Konvoi oder als Besenfahrzeug hinterher.
  * Herkömmliche Systeme scheitern im Pkw daran, dass die geschlossene Blechkarosserie als stark dämpfender Faradayscher Käfig wirkt und Motorrad-Intercoms keine Reichweite in ein geschlossenes Fahrzeug besitzen.
* **OpenMotorBridge Support-Van Kit (Referenz-Kit 5):**
  * **2 Pods an 2 Sonnenblenden (Fahrer- & Beifahrerseite):**
    * Pod 1 (Fahrerseite) und Pod 2 (Beifahrerseite) werden mit werkzeuglosen Sonnenblenden-Clips ([`car_sun_visor_pod_clip.stl`](../../hardware/cad/stl/05_accessories/car_sun_visor_pod_clip.stl)) an den beiden Sonnenblenden montiert.
    * **Physikalischer Vorteil:** Die Antennen strahlen ungehindert durch die Glas-Windschutzscheibe nach vorn und zur Seite ab - **100 % frei von metallischer Karosserie-Abschattung**, absolut verdeckt und ohne abstehende externe Antennen.
    * **Flexible Konvoi-Modi:**
      - **Modus A (Begleitfahrzeug für gemischte Motorradgruppe):** Pod 1 mit Sena SPIDER X Slim (Mesh 3.0/2.0), Pod 2 mit Cardo Packtalk Edge (DMC Gen 2). Ermöglicht gleichzeitige Vollduplex-Verbindung in beide großen Motorrad-Mesh-Welten!
      - **Modus B (Reiner Pkw-/Camper-Konvoi & Rallye-Orga):** Pod 1 mit OMM 2.4 GHz Kassette (OpenMotorMesh), Pod 2 mit Midland PMR446 Kassette für universellen Jedermannfunk.
      - **Modus C (Hybrid-Lead & OMM-Anchor):** Pod 1 mit OMM 2.4 GHz Kassette (verbindet alle OMB-Bikes im Konvoi), Pod 2 wahlweise Sena oder Cardo für Gastfahrer.
    * **Audio-Integration im Pkw (Headset-frei & Freisprech-Komfort):**
      - **Option 1 (Pkw-Freisprecheinrichtung via Qualcomm QCC3084):** Die Zentralbox auf dem Dashboard koppelt sich per Bluetooth (HFP 1.8 / A2DP) vollautomatisch als Mobiltelefon mit der Pkw-Freisprechanlage. Die Fahrzeuginsassen hören den Gruppenfunk glasklar über die Autolautsprecher und sprechen freihändig über das Pkw-Dachmikrofon!
      - **Option 2 (Apple CarPlay / Android Auto Audio-In/Out):** Bei USB-C Verbindung spiegelt die Zentralbox das PWA-Dashboard auf den großen Auto-Bildschirm und leitet Sprache latenzfrei über die USB-Audioschnittstelle.
      - **Option 3 (Autarkes OMM-Handgerät / Tischmikrofon):** Ein autarkes OMM 2.4 GHz Modul mit Schwanenhals-Mikrofon oder PTT-Taste liegt griffbereit auf der Mittelkonsole für den Beifahrer / Tourguide.
  * **Zentralbox-Docking & Dashboard-GNSS:**
    * Die Zentralbox ruht auf dem Armaturenbrett in der vibrationsdämpfenden Keilaufnahme ([`car_dashboard_wedge_dock.stl`](../../hardware/cad/stl/05_accessories/car_dashboard_wedge_dock.stl)).
    * Das u-blox SAM-M10Q Multi-GNSS-Modul sitzt mit optimaler Zenith-Sicht direkt unter der Windschutzscheibe auf dem Dashboard.
    * Der LoRa 868 MHz Transceiver (Semtech SX1262) arbeitet mit der integrierten Taoglas FXP895 Flexantenne im Gehäusedeckel der Zentralbox - keine Außenantennen nötig.
    * Die Stromversorgung erfolgt werkzeuglos über den 12V/24V-Zigarettenanzünder-Adapter (30W USB-PD).
  * **Verdeckte A-Säulen-Verkabelung:**
    * Ultraflache USB-C Flachbandkabel verlaufen unsichtbar hinter der Gummidichtung der A-Säulen direkt zu den beiden Sonnenblenden.
  * **Drahtlose Pkw-Telemetrie via Bluetooth-OBD2 (ELM327 / vGate):**
    * Die Zentralbox koppelt sich autark via Bluetooth 5.0 (BLE) mit einem kompakten OBD2-Dongle im Fahrerfußraum.
    * Pkw-Daten (Geschwindigkeit, Drehzahl, Tankfüllstand, Motortemperatur) werden autark ins 868-MHz-LoRa-Mesh übertragen - ohne Kabel im Fußraum und ohne Abhängigkeit von einer App auf dem Smartphone/Tablet.
* **Live-Gruppenüberwachung ohne Mobilfunknetz (PWA Fleet Dashboard):**
  * Auf einem im Pkw montierten iPad oder Android-Tablet läuft das PWA-Dashboard im Offline-Kartenmodus.
  * Über das 868 MHz LoRa-Mesh empfängt das Begleitfahrzeug im Sekundentakt Telemetriedaten (Position, Geschwindigkeit, SOS-/Sturzalarm, Reifendruck, Außentemperatur) aller Motorräder im Umkreis von bis zu $15\,\text{km}$ - autark, robust und vollkommen unabhängig von Mobilfunkmasten.

---

## 6. Internet-Uplink, V2X-Schwarmdaten & Waze "Auto-Klick" (Android Companion)

OpenMotorBridge besitzt für erweiterte Telematik- und Community-Funktionen einen dedizierten **Internet-Uplink über die Android Companion-App** (`bar.f0o.omb`), während das Gesamtsystem für alle fahr- und sicherheitskritischen Funktionen 100 % autark und offline-fähig bleibt:

### 6.1 Der physische Übertragungsweg: Warum BLE / USB statt Wi-Fi genutzt wird
* **Physische Wi-Fi-Exklusivität:** Während des Betriebs von drahtlosem Android Auto oder Apple CarPlay ist die WLAN-Schnittstelle des Smartphones mit dem 5-GHz-WLAN des COTS-Dongles belegt. Das Smartphone kann sich hardwarebedingt nicht gleichzeitig mit einem 2,4-GHz-WLAN des ESP32 verbinden.
* **Unterbrechungsfreier Datenkanal:** Die Übertragung zwischen OpenMotorBridge (ESP32-S3) und dem Smartphone erfolgt daher **strikt über Bluetooth Low Energy (WebBLE / RFCOMM)** oder über das USB-Kabel am Front-Node. Bluetooth und Wi-Fi laufen auf getrennten Funkstacks völlig störungsfrei parallel.

### 6.2 Der Android Internet-Uplink: Layer-5 SOCKS5-Relay, OpenTrafficMap & Waze "Auto-Klick"
Auf Android-Geräten bietet die Companion-App (`bar.f0o.omb`) im Hintergrund mächtige Integrationsmöglichkeiten, die auf iOS durch Apples Sandbox-Richtlinien blockiert werden:
1. **Layer-5 SOCKS5 / Stream-Relay mit Mobilfunk-Bindung:**
   * Die Android-App bindet ihre ausgehenden Sockets explizit an die Mobilfunk-Schnittstelle (`NetworkCapabilities.TRANSPORT_CELLULAR`).
   * **Kein VPN-Konflikt mit Tailscale:** Da das Relay rein auf Anwendungsebene (L5) als unprivilegierter TCP/UDP-Stream arbeitet und **keinen** Android `VpnService`-Slot belegt, bleibt ein parallel genutztes **Tailscale** oder WireGuard (z. B. für Home Assistant / Smart-Home) zu 100 % ungestört aktiv.
2. **V2X Car-to-X Vernetzung & OpenTrafficMap:**
   * Der 5.9-GHz-ITS-G5-Empfänger auf PCBA 08 empfängt lokale Car-to-X-Broadcasts:
     - **SPaT (Signal Phase and Timing):** Umschaltzeiten und Grünphasen vernetzter Lichtsignalanlagen (Ampeln).
     - **DENM:** Akute Gefahrenmeldungen (Geisterfahrer, Glatteis, Stauende hinter unübersichtlicher Kurve).
     - **CAM:** Positionen und Geschwindigkeiten benachbarter Fahrzeuge.
   * OpenMotorBridge überträgt diese Daten über UWB und BLE an die Companion-App, die sie über das Mobilfunknetz (4G/5G) in das **OpenTrafficMap-Projekt** einspeist und lokale Gefahren-Tiles (GeoJSON) lädt.
3. **Waze "Auto-Klick" & Schwarm-Automatisierung:**
   * Um die Community-Warnungen von Waze während der Fahrt ohne gefährliche Touchscreen-Bedienung zu nutzen:
   * Erkennt OMB über V2X ein relevantes Ereignis (Ampel rot, Baustelle, Unfall) oder über die 6-Achs-IMU eine Gefahrensituation (Vollbremsung $> 0{,}6\,\text{g}$, Notbremsstrobe, Sturz):
     - Sendet OMB ein Trigger-Telegramm an die Android Companion-App.
     - Die App nutzt den Android **AccessibilityService oder Intents**, um in Waze **vollautomatisch die Gefahrenmeldung abzusetzen ("Auto-Klick")**.
     - Der Fahrer behält beide Hände am Lenker; die Waze-Community wird in Echtzeit gewarnt und die Route bei Bedarf dynamisch angepasst.
4. **A-GPS Kaltstart-Beschleunigung (u-blox AssistNow Online):**
   * **Das Problem beim Kaltstart:** Nach längerer Standzeit oder beim Start in der Garage muss der GNSS-Chip die Satellitenbahnen (Ephemeriden) mit extrem langsamen $50\,\text{Bit/s}$ direkt aus dem Satellitensignal empfangen. Bei freiem Himmel dauert dieser Kaltstart mindestens $28\dots 36\,\text{Sekunden}$, unter Carports, Vordächern oder Bäumen oft $45\dots 90\,\text{Sekunden}$ (Time-To-First-Fix / TTFF).
   * **Lösung über den Internet-Uplink:** Beim Einschalten der Zündung (KL15) ruft die Companion-App über Mobilfunk ein kompaktes u-blox **AssistNow Online** Datenpaket ($\approx 3\dots 8\,\text{kB}$) ab.
   * **UBX-MGA Injektion in den SAM-M10Q:** Die App überträgt die Ephemeriden, den präzisen UTC-Zeitstempel und die grobe Position über BLE/USB an den Front-Knoten (PCBA 05), der sie über den Qwiic I2C-Port `J12` direkt in den u-blox SAM-M10Q injiziert.
   * **Ergebnis:** Der TTFF fällt von $\sim 30\,\text{s}$ auf **$< 1\dots 1{,}5\,\text{Sekunden}$** (Instant-3D-Fix), und die Empfindlichkeit beim Kaltstart verbessert sich um bis zu **$+15\,\text{dB}$** (Erfassung bis $-158\,\text{dBm}$). Das Bike hat bereits vollen Satelliten-Lock, bevor der Fahrer den Helm aufsetzt.
   * **Offline-Fallback:** Startet das Motorrad im tiefsten Funkloch, schaltet der SAM-M10Q nahtlos auf *AssistNow Autonomous* (on-chip Bahnextrapolation) oder greift bei kurzen Tankpausen ($< 4\,\text{h}$) auf den LiPo-gepufferten RTC-Speicher zurück (Hot Start: $< 1\,\text{s}$).

### 6.3 Die 100 % Offline-First Garantie (Safety First)
Sollte die Mobilfunkverbindung auf Pässen oder in Tälern abreißen:
* Sämtliche fahr- und sicherheitskritischen Funktionen – das 77-GHz-Radar ($< 15\,\text{ms}$), der UWB-Backbone ($< 0{,}4\,\text{ms}$), die Intercom-Mesh-Matrix (Sena/Cardo/OMM), die IMU-Sturzerkennung und das Notbremsblinken – arbeiten zu **100 % offline und autark** auf der Motorrad-Hardware.
* Im tiefsten Funkloch auf abgelegenen Pässen funktioniert OpenMotorBridge mit identischer Präzision und Schutzwirkung wie im Stadtzentrum.

---

## 7. Dokumentations-Architektur & Kapitel-Wegweiser (Single Source of Truth)

Zur Vermeidung von Redundanzen und zur Gewährleistung klarer Zuständigkeiten ist die Dokumentation modular gegliedert. Jedes Fachthema besitzt eine verbindliche **Single Source of Truth (SSOT)**:

| Themenbereich | Verbindliches Referenzdokument | Inhalt & Fokus |
| :--- | :--- | :--- |
| **Intercom-Profile & Matrix** | **[Kapitel 02](02_intercom_matrix_profiles.md)** | Sena Mesh 2.0/3.0, Cardo DMC Gen1/2, Midland PMR, Pegel- und Audio-Routing |
| **Akustik, DSP & Ducking** | **[Kapitel 03](03_acoustics_dsp_ducking.md)** | Raised-Cosine Filter, Ducking (-12 dB / -18 dB), Wind-AGC, Latenzbudgets |
| **OEM-Kassetten (Sena/Cardo)**| **[Kapitel 04](04_cartridge_specs.md)** | Gateway-Kassetten mit Mechatronik (PCBA 03), WCH CH32V003 Aktuatoren |
| **OMM Intercom-Module (2.4G & 446M)** | **[Kapitel 04b](04b_omm_intercom_module.md)** | PCBA 09 (2.4 GHz HD-Mesh) & PCBA 10 (446 MHz PMR/DMR), ECE 22.06 UCS |
| **Heck-Radar 2.0 (77 GHz)** | **[Kapitel 05](05_radar_bionic_mounting.md)** | Wheeltec MR20 mmWave, TTC-Bedrohungslogik, 36-LED Warnflügel, V2X-Patch |
| **Telemetrie & Blackbox** | **[Kapitel 06](06_telemetry_blackbox_webdav.md)** | MicroSD-FAT32 Ringpuffer, 15-State EKF Schräglage, WebDAV / Nextcloud Sync |
| **PCBA Hardware & Pinouts (SSOT)**| **[Kapitel 07](07_pcba_hardware_pinouts.md)** | **Alle Platinen (PCBA 01 bis 10)**, vollständige Pinbelegungen, Bauteilwerte |
| **Gehäuse, Mechanik & CAD (SSOT)**| **[Kapitel 08](08_enclosures_mechanics_cad.md)** | **Alle CAD-Modelle**, OpenSCAD Parameter, ECE-Normen, unverlierbare Muttern |
| **Firmware-Architektur** | **[Kapitel 09](09_firmware_architecture.md)** | FreeRTOS Task-Matrix, UWB Ranging-Protokoll, Ringpuffer & State-Machines |
| **Firmware Build Guide** | **[Kapitel 10b](10_firmware_build_guide.md)** | ESP-IDF v5.2 Setup, VS Code / CLI Kompilierung, CMake Targets, Flashen |
| **WebApp PWA Dashboard** | **[Kapitel 10](10_webapp_pwa_dashboard.md)** | Ride HUD, WebBLE Protokoll, Kassetten-Konfiguration, Offline-OSM-Karten |
| **CarPlay / Android Auto Bridge** | **[Kapitel 11](11_carplay_android_auto_bridge_architecture.md)**| Virtual WHIM, CP2AA Bridge, Multi-Path Wi-Fi/Cellular, Headless Dongle |
| **Diagnose, Service & Flashen** | **[Kapitel 12](12_diagnostics_service_flashing.md)**| WebSerial Terminal, NVS-Speicherbelegung, Bootloader & Notfallwiederherstellung |
| **Simulation & Testbench (HIL/SIL)**| **[Kapitel 13](13_simulation_testbench.md)** | Python Netlist Validator, FreeRTOS Timing-Verifikation, Signalintegrität |
| **EMV & HF-Hardening** | **[Kapitel 14](14_emv_rf_hardening.md)** | CISPR 25 Class 5, 2.4 GHz vs. UWB Koexistenz, ESD-Schutznetzwerke |
| **BOM, Beschaffung & Fertigung**| **[Kapitel 15](15_bom_manufacturing.md)** | **Vollständige Bauteillisten**, JLCPCB Bestelldaten, Zukaufteile, COTS-Docks |
| **Bauanleitung & Montage** | **[Kapitel 16](16_build_instructions_assembly.md)** | Schritt-für-Schritt Aufbau, Kabelkonfektionierung, Drehmomente, Inbetriebnahmetests |

