# 01 - Systemarchitektur, Universelle Satelliten-Topologie & Akustik

Dieses Dokument spezifiziert die übergeordnete Gesamtsystem-Architektur der **OpenMotorBridge v10.0 (Native USB-PD & Edge-AI Generation)**, die universelle Satelliten-Topologie, die fahrzeugfesten Montagekonzepte (Koffer, Rahmen, Heck, Riser bei 100 % kabellosem Helm-Komfort), die HF-Koexistenz sowie die nahtlose Integration in moderne OEM-Motorrad-Infotainmentsysteme.

---

## 1. Problemstellung & Architekturphilosophie

Klassische Motorrad-Kommunikationssysteme sind historisch stark fragmentiert:
* **Inkompatible Mesh-Standards:** Sena Mesh 2.0/3.0, Cardo DMC Gen1/Gen2, Midland Wave Mesh und analoger PMR446-Funk können nicht direkt miteinander kommunizieren.
* **HF-Übersteuerungen & De-Sensing:** Der gleichzeitige Betrieb mehrerer 2,4-GHz-Mesh-Transceiver an einem einzigen Montagepunkt (z. B. am selben Helm oder in einer gemeinsamen Box) führt zu massiver Empfänger-Desensibilisierung (*De-Sensing*), Intermodulation und Reichweiteneinbrüchen von bis zu $80\,\%$.
* **Proprietäre Infotainment-Sperren:** Systeme wie Harley-Davidson Boom! Box GTS / Skyline OS oder BMW ConnectedRide verlangen teure, herstellereigene Schnittstellenmodule (z. B. HD WHIM), um Apple CarPlay oder Android Auto freizuschalten.

**OpenMotorBridge v10.0** löst diese Probleme durch eine modular entkoppelte **Satelliten-Topologie**, angebunden über einen **robusten 4-Draht Automotive USB-PD & USB 2.0 Bus (`VBUS`, `GND`, `D+`, `D-`)**, kombiniert mit dem **ESP32-S31** (Edge-AI Audio) und dem dedizierten **Qualcomm QCC3084** Bluetooth-Audio-SoC:

```
                                  GESAMTSYSTEM-TOPOLOGIE (v10.0)
+---------------------------------------------------------------------------------------------+
| 1. COCKPIT / LENKER & KEYFOB:                                                               |
|    * Front-Node (PCBA 05): 60W USB-PD Engine, modularer Sensor-Puck ("Körbchen")             |
|    * Symmetrische Dual Under-Perch Spiegel-Pods (Links: PTT & BSD | Rechts: Cam-Tag & BSD)  |
|    * 4-Port Handschuhfach Hub: 30W PD + 10W Dongle + Harley Headset-Emulation via USB        |
|    * Smart-Keyfob (PCBA 07): 868 MHz LoRa Pager (24/7 Diebstahlalarm & Notfall-Beacon)      |
|    * PWA Dashboard auf Smartphone / TFT via Web-Bluetooth (WebBLE)                          |
+---------------------------------------------------------------------------------------------+
| 2. ZENTRALE STEUERBOX (Unter der Sitzbank auf Batteriebrücke, IP67):                        |
|    * ESP32-S31 Dual-Core RISC-V (320 MHz, 128-bit SIMD AI Accelerator für Audio-Klassifiz.)|
|    * Qualcomm QCC3084 Audio-SoC (Dual-A2DP, aptX HD, HFP 1.8, Auracast ohne Host-Jitter)    |
|    * Semtech SX1262 LoRa (868 MHz) an USV-Schiene * Taoglas FXP895 Antenne in Akkubrücke    |
|    * Multi-Port Automotive USB-PD Power-Engine & USB 2.0 High-Speed Hub                     |
|    * Dual-Power Input: 12V Bordnetz OR USB-PD Sink (5V-20V USB-C für Werkstatt-Desk)        |
|    * LM5164-Q1 72V Step-Down * Dual Ideal-Diode OR-ing * BQ24075 USV & 2200mAh LiPo-Puffer   |
|    * Zwei-Kabel-Architektur: 6-Pin DTM (Bordnetz/CAN) + 16-Pin Peripherie-Bus (4 Stränge)  |
+--+---------------------------------------------------------------------------------------+--+
   |                                                                                       |
   v 16-Pin Automotive Peripherie-Bus (Verzweigt extern sauber in 4 autarke 4-Ader-Stränge) |
+-----------------------------------------+-----------------------------------------------+
| 3. SATELLITEN-POD 1 (Koffer Links, 30W):| 4. SATELLITEN-POD 2 (Koffer Rechts, 30W):     |
| * Slide-in Deckel & FOB-Magnetriegel    | * Slide-in Deckel & FOB-Magnetriegel          |
| * Zwischendeckel (Dry-Flap)             | * Zwischendeckel (Dry-Flap)                   |
| * 2 mechatronische Drücker auf          | * 2 mechatronische Drücker auf                |
|   Universal-Schiene ("One Size Fits All"|   Universal-Schiene ("One Size Fits All"      |
|   2,0s Kaltstart-Impuls auf KL15)       |   2,0s Kaltstart-Impuls auf KL15)             |
| * Koffer-USB-Ladedose (30W USB-PD)      | * Koffer-USB-Ladedose (30W USB-PD)            |
| * Wetterfester Outdoor-USB-Port (GS/ST) | * Wetterfester Outdoor-USB-Port (GS/ST)       |
| * 4-Pin Magnet-Abreißkupplung (IP68)    | * 4-Pin Magnet-Abreißkupplung (IP68)          |
+-----------------------------------------+-----------------------------------------------+
   |                                                                                       |
   +-> 5. BORDNETZ & CAN (Kabel 1): 6-Pin Deutsch DTM (KL30, KL15, GND, CAN_H, CAN_L, Schirm)
   +-> 6. HECK-RADAR (Strang 4): 4-Draht 12V Power & High-Speed CAN / Serial               |
   |      Wheeltec MR20 77-GHz mmWave (PCBA 08) * 36x Alert-LEDs * Drip-Loop & Roost-Defl. |
   |                                                                                       |
   v Strang 1: 4-Draht Automotive Backbone (60W Power & High-Speed Bus durch Rahmentunnel) |
+-----------------------------------------------------------------------------------------+
| 7. FRONT-KNOTEN & COCKPIT-HUB (PCBA 05 am Lenker-Riser / Gabelbrücke, 60W Power Budget):|
| * Modularer Sensor-Puck ("Körbchen"): SAM-M10Q GNSS, TMP117, OPT3001, Knowles MEMS       |
| * 60W USB-PD Speisung: 27W Phone + 15W Navi + 10W Action-Cam + Displays + Sensoren      |
| * Speist Dual Cockpit Speaker Corner Pods (2x OLED-Displays in Lautsprechergittern)     |
| * Speist 4-Port Handschuhfach-Hub & stellt Harley Headset-Emulation via USB bereit      |
| * Direkte Anbindung an symmetrische Dual Under-Perch Spiegel-Pods (Links PTT, Rechts Cam)|
+-----------------------------------------------------------------------------------------+
| 8. BEGLEITFAHRZEUG- & KOLONNEN-TOPOLOGIE (Pkw / Support-Van / Rallye / Wohnmobil):      |
| * All-in-One Car Support Core Unit: Zentralbox & Front-Node kompakt vereint             |
| * Absetzbarer Sensor-Puck ("Körbchen") an Dashboard/Windschutzscheibe via 1,5m Kabel    |
| * 4-Port Media Hub & CarPlay Clean Power-Injection mit OEM Media-USB Passthrough        |
| * 2 Pods an 2 Sonnenblenden: Fahrer Pod 1, Beifahrer Pod 2 (Sena/Cardo oder OMM/Midland)|
| * Externe 868-MHz-Magnetfuß-Dachantenne als Standard (15-25 km LoRa-Reichweite)         |
+-----------------------------------------------------------------------------------------+
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
  * Stattdessen informiert OpenMotorBridge den Fahrer **diskret und privat** (haptischer Alarm am Smart-Keyfob in der Jackentasche, dezenter Audio-Ping nur im eigenen Helm, optische Warn-LEDs an beiden Rückspiegeln).
  * Der menschliche Fahrer behält die volle Souveränität: Er prüft die Situation kurz im Rückspiegel oder auf dem Dashboard und entscheidet selbst, ob und wie er seine Mitfahrer mit eigener, natürlicher Stimme über die Intercom informiert. Das System stärkt die menschliche Führungskompetenz, anstatt sie zu bevormunden.

---

## 2. Modulare Systemphilosophie & Montagefreiheit (Die standardisierten Funktionsknoten)

OpenMotorBridge v10.0 definiert die Plattform über **standardisierte Funktionsknoten**:
1. **Zentralbox (Main ECU * PCBA 01):** Zentraler Rechenkern (**ESP32-S31** Dual-Core RISC-V @ 320 MHz mit 128-bit SIMD AI-Beschleuniger für On-Device Audio-/Sprachverarbeitung), dedizierter **Qualcomm QCC3084** Bluetooth-Audio-SoC (Dual-A2DP, aptX HD, HFP 1.8, Auracast), Multi-Port Automotive USB-PD Power-Engine, 72V Automotive Step-Down (LM5164-Q1) und LiPo-USV (BQ24075 mit 2.200 mAh Flachzelle). **Dual-Power Input:** Unterstützt neben dem 12V Bordnetz auch einen **USB-PD Sink Eingang (5V–20V)** über den nativen USB-C Port mit Ideal-Diode OR-ing – ermöglicht vollständiges Flashen, Testen und Kalibrieren auf der Werkbank mit jedem Smartphone-/Laptop-Netzteil ohne 12V-Labornetzgerät. **Zwei-Kabel-Architektur:** Kabel 1 (6-Pin Deutsch DTM) für Bordnetz & CAN; Kabel 2 (16-Pin Automotive Connector) für die 4 autarken Systemstränge (Front-Node 60W, Pod 1 30W, Pod 2 30W, Radar MR20 12V). Beherbergt den **Semtech SX1262 LoRa-Transceiver (868 MHz)** direkt an der USV-Schiene. *(Montage mittig unter der Sitzbank auf der Batteriebrücke).*
2. **Satelliten-Pod 1 (Bucht Links, 30W Budget):** Universal-Koffer-Pod mit **Slide-in Deckel**, integrierter **FOB-Magnetverriegelung** (berührungsloses Öffnen mit dem Smart-Keyfob), innenliegendem **Zwischendeckel (Dry-Flap)** und **integrierter Koffer-USB-Ladedose (30W USB-PD)** sowie wetterfestem Outdoor-Port (IP68 Kappe & Dichtmanschette für Starkregen-Laden). Beherbergt die universelle Schnittstellenplatine `PCBA 03` (Sena SPIDER X, Cardo Packtalk Edge, UCS-Standard, OMM 2.4 GHz oder Midland PMR446). **Mechatronischer Kaltstart:** Zwei mechatronische Drücker (Mini-Hubmagnete) auf universeller Doppel-Schiebeschlitten-Schiene (`012_universal_actuator_slide_bracket.scad`) lösen bei Zündung-AN (KL15) einen simultanen 2,0s Einschaltimpuls aus ("One Size Fits All" – kein Standby-Batteriefraß, kein Garantieverlust durch Platinenlöten, kein Pod-Ausbau vor Touren). Anbindung über 4-Draht Bus mit 4-Pin Magnet-Abreißkupplung (IP68).
3. **Satelliten-Pod 2 (Bucht Rechts, 30W Budget):** Baugleicher, vollkommen symmetrischer Universal-Koffer-Pod mit Slide-in Deckel, FOB-Magnetverriegelung, Zwischendeckel, interner 30W USB-Ladedose, Outdoor-Port und mechatronischem Doppel-Drücker (auch 2x die gleiche Intercom wie in Bucht 1, z. B. 2x Cardo oder 2x Sena in getrennten Gruppen).
4. **Front-Node & Cockpit-Hub (PCBA 05 am Riser, 60W Power Budget):** Am Lenker-Riser / oberen Gabelbrücke montiert. **60W USB-PD Power-Engine** (Southchip SC8721/SC8102 Synchronous Buck-Boost) versorgt verlässlich Fahrer-Smartphone-Schnellladung (bis 27W), dediziertes Motorrad-Navi (15W für Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride), Action-Cam Dauerstrom (10W via wetterfestem USB-C Kabel), Dual Cockpit OLED-Displays (2W in Speaker Corner Pods) und Sensorik/Host-MCU/Hub (3,5W). **Modularer Sensor-Puck ("Körbchen"):** Integriert **u-blox SAM-M10Q Multi-GNSS**, **TI TMP117** Außenthermometer, **OPT3001** Umgebungslicht und **Knowles MEMS-Windmikrofon**; rastet am Bike oben auf den Front-Node ein und kann im Pkw/Van per 1,5m Kabel an die Windschutzscheibe geclipst werden. Direkte Schnittstelle zu den symmetrischen Dual Under-Perch Spiegel-Pods. Verbunden mit der Zentralbox über das 4-Draht Automotive Backbone-Kabel im Harley-Rahmentunnel (**ZERO Tank-Demontage!**).
5. **Symmetrische Dual Under-Perch Spiegel-Pods (Links & Rechts):** Formschön und aerodynamisch jeweils unter die linke und rechte Spiegelschraube geklemmt.
   * **Werksprofil (Default):**
     * **Linker Spiegel-Pod:** Taktiler Daumen-PTT-Taster (Funk/Intercom & Sprachassistent) + linke bernsteinfarbene Totwinkel-Warn-LED (BSD) gerichtet auf das linke Spiegelglas.
     * **Rechter Spiegel-Pod:** Taktiler Daumen-Taster für Action-Cam (Kurzdruck: Highlight-Tag / Bookmark für Insta360/GoPro/DJI via BLE; Langdruck: Video Start/Stopp / SOS) + rechte bernsteinfarbene Totwinkel-Warn-LED (BSD) gerichtet auf das rechte Spiegelglas.
   * **100 % Software-Defined Button Mapping (Freie Tastenbelegung via PWA):** Physische Taster frei konfigurierbar (Kurzdruck, Doppelklick, Halten für PTT, Gefahren-Marker, Cam-Tags, Garagentor via BLE).
   * **Sicherheitsgewinn:** Echte bilaterale Totwinkelüberwachung direkt im peripheren Sichtfeld beider Spiegel. 100 % symmetrische Ergonomie, baugleiche innere Platine (`PCBA 05B`).
6. **4-Port Handschuhfach Media & Power-Injection Hub (`glovebox_power_injection_hub.scad`):** Im rechten Medienfach der Touring-Verkleidung (Road Glide, Street Glide, CVO, CVO ST). Wird vom Front-Node (`PCBA 05`) über eine kombinierte High-Power & USB 2.0 Zuleitung versorgt. Tappt den werksseitigen Harley USB-C Port zur Head Unit (Skyline OS / Boom! Box) und speist geregelte **30W USB-PD** (thermisch optimiert für geschlossene Handschuhfächer) für das Smartphone sowie **10W geschaltete Dongle-Power** (Wireless CarPlay / Android Auto mit Überhitzungs-Notabschaltung) ein. 1x freier Media USB 2.0 Port für USB-Sticks/Updates. **Harley Headset-Emulation via USB:** Das High-Speed Datenpaar verbindet den Front-Node direkt mit Port 4 zur OEM-Headunit; OMB emuliert ein digitales MFi / USB Audio Class Headset, schaltet Apple CarPlay nativ frei und leitet Helm-Mikrofonaudio digital ohne Massebrummen ein. Alle im Handschuhfach angeschlossenen Geräte verbleiben zu 100 % im Fach (Action-Cam & Navi werden direkt am Front-Node versorgt – kein Kabeldurchzug durch das Fach!).
7. **Radar 2.0 Sub-MCU & Heck-Wings (PCBA 08 am Heck):** Autonomes 77-GHz Heck-Radar (Wheeltec MR20), versorgt über Strang 4 des 16-Pin Peripherie-Kabelbaums mit 4-Draht Power & High-Speed Bus; 36 Strobe-Warn-LEDs, Abtropfschlaufe (Drip-Loop) und integrierter Schmutzfänger (Roost-Deflector). Optionaler Under-Fender Mount für Cruiser/Bobber.

```
                     DIE STANDARDISIERTEN FUNKTIONSKNOTEN (v10.0)
+-----------------------------------------------------------------------------+
| 1. FRONT-NODE (Am Lenker-Riser):  SAM-M10Q GNSS, Kaltluft-Sensorik,         |
|    Knowles Wind-MEMS, Qi/USB-PD Zubehörspeisung, Riser-Klemmung             |
+-----------------------------------------------------------------------------+
| 2. SYMMETRISCHE DUAL UNDER-PERCH SPIEGEL-PODS (Links & Rechts):             |
|    * Links:  Taktile PTT-Taste, Linke Totwinkel-Warn-LED (BSD Amber)        |
|    * Rechts: Taktile Action-Cam-Tag Taste, Rechte Totwinkel-LED (BSD Amber) |
+-----------------------------------------------------------------------------+
| 3. HANDSCHUHFACH-HUB (Rechts): 2-Port USB-Hub, unterseitige OEM-Tülle,      |
|    stabiler Ottocast CarPlay/AA Bypass, 1x freier USB-Ladeport              |
+-----------------------------------------------------------------------------+
| 4. ZENTRALBOX (Unter Sitz/Akku): ESP32-S31 AI-Host, QCC3084 Audio-SoC,      |
|    SX1262 LoRa 868MHz, Multi-Port USB-PD Engine, USV, Zwei-Kabel-Anschluss  |
|    Dual-Power Input: 12V Bordnetz OR USB-PD Sink (5V-20V für Werkbank/Desk) |
+------------------------------+----------------------------------------------+
| 5. POD 1 (Koffer Links):     | 6. POD 2 (Koffer Rechts):                    |
| * Slide-in Deckel & FOB-Lock | * Slide-in Deckel & FOB-Lock                 |
| * Zwischendeckel (Dry-Flap)  | * Zwischendeckel (Dry-Flap)                  |
| * Koffer-USB-Ladedose        | * Koffer-USB-Ladedose                        |
| * 4-Pin Magnet-Abreißkupplung| * 4-Pin Magnet-Abreißkupplung                |
+------------------------------+----------------------------------------------+
| 7. HECK-RADAR 2.0 (Kennzeichenträger): Wheeltec MR20 77-GHz, 36x LEDs       |
+-----------------------------------------------------------------------------+
```

> [!NOTE]
> **Montagefreiheit - *Your Vehicle, Your Choice*:**  
> Wo und wie ihr diese Module an eurem Fahrzeug platziert, ist bewusst **völlig euch überlassen**! OpenMotorBridge stellt die standardisierten Elektronik- und Gehäuse-Dimensionen sowie die Schnittstellen bereit.  
> Für ausgewählte Plattformen liefern wir in **[Kapitel 08 (Mechanik & Gehäuse)](08_enclosures_mechanics_cad.md)** komplett durchentwickelte, 100 % schraub- und klebefreie **Referenz-Montagekits** mit:
> * **Referenz-Kit 1 (Harley-Davidson CVO Road Glide ST & New Touring FLTRX/FLHX):**
>   - **ZERO OUTER FAIRING REMOVAL:** Niemals die lackierte Sharknose-Außenhaut oder Lautsprechergitter abhebeln! Die Außenverkleidung bleibt unangetastet.
>   - **ZERO FUEL TANK LIFTING:** 4-Draht Backbone-Kabel wird per Nylon-Einziehfeder in 5 Minuten durch den offenen Harley-Kabelkanal im Rahmentunnel gezogen. Tank bleibt montiert.
>   - **Front-Node am Riser / Gabelbrücke:** Perfekte Fahrtwindkühlung ($< 35^\circ\text{C}$), beste GNSS-Sicht.
>   - **Symmetrische Dual Under-Perch Spiegel-Pods:** Links PTT & BSD-LED; Rechts Action-Cam-Tag & BSD-LED unter den Spiegelschrauben.
>   - **Handschuhfach von unten:** Durch OEM-Gummitülle erschlossen (keine Kabel über Türdichtungen!).
>   - **Pod 1 & 2 in den Koffer-Innenwänden:** Slide-in Deckel mit FOB-Magnetriegel, Zwischendeckel und interner USB-Ladedose; 4-Pin Magnet-Abreißkupplung am Rahmen.
>   - **Zentralbox:** Im Batteriefach unter dem Sitz. Dual-Power Input für Schreibtisch-Tests. Heck-Radar an Kennzeichenbrücke.
> * **Referenz-Kit 2 (Harley-Davidson Road King Special / FLHRXS):** Pod 1 & 2 in den Hartschalenkoffern, Front-Node an der Riser-Klemme / Scheinwerfer-Nacelle, Zentralbox unter der Sitzbank.
> * **Referenz-Kit 3 (Classic Bagger & Cruiser - Street Glide / Electra Glide):** Pod 1 & 2 in den Koffern, Front-Node am Riser / Batwing-Lenkeraufnahme, Zentralbox unter dem Sitz, optionales Radar unter dem Kennzeichen.
> * **Referenz-Kit 4 (Adventure & Touring Enduros - BMW GS, KTM Adventure, Africa Twin):** Pod 1 & 2 werden **strikt fahrzeugfest am Motorrad** montiert (am Rohr-Kofferträger oder in der Sitzbank-Bügelfalte; nicht im Inneren von Aluminiumkoffern!). Front-Node an der Navigationsstrebe über dem TFT. Radar am Heck-Gepäckträger.
> * **Referenz-Kit 5 (Pkw / Support-Van / Rallye-Begleitfahrzeug / Wohnmobil):** All-in-One Car Support Core Unit (Zentralbox + Front-Node vereint), AAWireless Power-Bypass (5V 3A vom OMB-Regler, reine Datenleitung zum Werks-Radio), 2 Pods an Sonnenblenden via Schnellwechsel-Clips, externe LoRa-Magnetfuß-Dachantenne.


### 2.1 Whitepaper-Entwurfsentscheidung: Dezentrale Satelliten-Topologie vs. Monolithische Single-Box

In der frühen Konzeptphase wurde intensiv evaluiert, ob das gesamte System in einem einzigen, großen Zentralgehäuse (z. B. unter der Sitzbank oder hinter der Frontverkleidung) untergebracht werden sollte. Der monolithische Ansatz wurde nach physikalischen und messtechnischen Voruntersuchungen einstimmig verworfen:

#### Evaluierungsmatrix: Monolithische Zentralbox vs. OpenMotorBridge Satelliten-Architektur

| Bewertungskriterium | Option A: Monolithische Single-Box | Option B: Reine Lenker/Cockpit-Box | **Option C: OMB Dezentrale Satelliten (Gewählt)** |
| :--- | :--- | :--- | :--- |
| **HF-Selbststörung (Desensing)**| **Kritisch:** 2.4 GHz BLE, Wi-Fi, 868 MHz LoRa, GNSS L1/L5 & 72V Buck-Regler auf engstem Raum | **Kritisch:** Starkes Übersprechen auf Cockpit-TFT und Radio-Antenne | **Optimal (> 45 dB Isolation):** GNSS im Cockpit, Intercoms an den Heckflanken (Pod 1 & 2), geschirmter 4-Draht Bus |
| **Kabelbaum-Durchmesser** | **Massiv:** 26+ Einzelleitungen müssen quer durch das gesamte Motorrad gezogen werden | **Schlecht:** 18 Leitungen über den schwenkenden Lenkkopf (Kabelbruch-Risiko) | **Ultra-Schlank:** Zwei-Kabel-Architektur mit 4-Draht USB-PD/Daten-Strängen; ZERO Tank-Lifting im Rahmentunnel |
| **Thermische Verlustleistung** | **Hot-Spot (> 18 W):** 72V DC/DC + Audio-Endstufen + Akkuladung unter der Sitzbank | **Thermischer Hitzetod (> 85 °C):** Stauwärme direkt hinter der Scheinwerfermaske | **Perfekt verteilt:** Max. 3-4 W pro Gehäuse; passive Wärmeabfuhr ohne Hotspots |
| **GNSS-Zenitsicht & Radar** | **Verschattet:** Sitzbank und Fahrer-Körper blockieren Satelliten & Heck-Sichtfeld | **Schlecht:** Heck-Radar vom Lenker aus physikalisch unmöglich | **Ideal:** SAM-M10Q hat freie Sicht durch Windschild; Radar hat freie Sicht nach hinten an Peitsche 3 |
| **Fahrtwind-Abtastung (AGC)** | **Physikalisch unmöglich:** Unter der Sitzbank herrscht kein dynamischer Staudruck | **Möglich:** Windmessung direkt am Lenker | **Exzellent:** Knowles I2S MEMS direkt an der Frontscheibe im Front-Node |

1. **Die Physik der HF-Koexistenz (Vermeidung von Receiver Desensitization):**
   * GNSS-Signale treffen die Erde mit extrem schwachen Pegeln von ca. **$-130\,\text{dBm}$ bis $-160\,\text{dBm}$**.
   * Die Auslagerung von Multi-GNSS in das Cockpit (Front-Node) platziert den Empfänger direkt unter die dielektrische Kunststoff-Scheibe mit ungetrübtem $180^\circ$-Blickwinkel zum Himmel.
   * Durch die Verbannung von OMM 2.4 GHz aus dem Cockpit und den Einsatz des geschirmten **4-Draht Automotive-Busses** herrscht im Cockpit vollkommene Ruhe im 2.4-GHz-Spektrum. Das GNSS leidet unter null Anhebung des Grundrauschens (*Noise Floor Lift*).
   * Die räumliche Trennung zwischen Front-Cockpit und den Heck-Pods (Pod 1 links, Pod 2 rechts) garantiert physikalisch über **$46\,\text{dB}$ Freiraumdämpfung** zwischen den 2.4-GHz-Mesh-Stufen und der Cockpit-Elektronik.
2. **Kabelbaum-Zuverlässigkeit über den Lenkkopf:**
   * Jedes Kabel, das über den beweglichen Lenkkopf geführt wird, unterliegt während der Fahrzeuglebensdauer Millionen von Biegewechseln.
   * Durch die Auslagerung der Cockpit-, Display- und PTT-Funktionen in den **Front-Node (PCBA 05)**, der über das hochzuverlässige **4-Draht Automotive Backbone-Kabel** (durch den Harley-Rahmentunnel ohne Tank-Demontage) mit der Zentralbox verbunden ist, entfallen empfindliche HF-Funkstrecken und bruchgefährdete Einzelleitungen über die Lenkachse.
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
Die universellen Monocoque-Pods ($150 \times 70 \times 38\,\text{mm}$ mit werkzeuglosem Slide-in Deckel, Trockenklappe und $124 \times 53 \times 28\,\text{mm}$ Innenraum) nehmen alle handelsüblichen OEM-Geräte im ungeöffneten Originalzustand direkt in der oberen Bucht auf:
* **Klasse S (Direkte Pod-Aufnahme * OMB-Referenz):** z. B. Sena SPIDER X Slim (Primärempfehlung), Cardo Packtalk Edge (Air-Mount), OMM UCS 2.4 GHz - 100 % ungeöffnetes Originalgerät im PA12-MJF Konturbett mit 3-Punkt EPDM-Dämpfung gegen $20\,\text{g}$ Vibration, direkt an PCBA 03 angebunden (USB-PD Ladeversorgung bis 30W, USB Audio Class, direkte elektrische PTT-Tastung oder BLE-Steuerung), null Pogo-Pins, null Löten, 100 % Erhalt von Werksgarantie & IP67-Schutz. Fehleranfällige Wechselkassettenschlitten und Hubmagnete sind vollständig eliminiert.
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
   * **Keine Pod-Montage am Helm:** Die wetterfesten Monocoque-Pods ($150 \times 70 \times 38\,\text{mm}$) verbleiben grundsätzlich fest am Fahrzeug (z. B. linker und rechter Kofferdeckel, Rahmenrohre oder Sturzbügel). Die Helme von Fahrer und Sozius bleiben zu 100 % kabel- und pod-frei.
   * **Physische & metallische Barriere:** Pod 1 (linke Fahrzeugflanke / linker Koffer) und Pod 2 (rechte Fahrzeugflanke / rechter Koffer) nutzen den massiven Motorradrahmen, den Kraftstofftank, den Motorblock und die Heckstruktur als natürliche metallische HF-Abschirmung.
2. **Schirmdämpfung:**
   * Die Freiraumdämpfung über $> 50\,\text{cm}$ in Kombination mit der massiven metallischen Abschirmung durch die Fahrzeugstruktur erzielt eine **HF-Entkopplung von $> 35\,\text{dB}$**.
   * Damit sinkt der Einkopplungspegel des Nachbarsenders unter $-15\,\text{dBm}$, wodurch die Eingangs-LNAs beider Headsets im linearen Bereich arbeiten und kein *De-Sensing* auftritt.
3. **Klare Frequenzzonen & Entlastung des 2.4-GHz-Spektrums:**
   * Durch die Verbannung von OMM 2.4 GHz aus dem Cockpit und den Entfall von Funk-Backbones zugunsten des geschirmten 4-Draht Busses ist das Motorrad in absolut saubere Funkzonen gegliedert:
     * **Heckflanken (2.4 GHz):** Pod 1 (Sena) und Pod 2 (Cardo) sind durch Rahmen und Tank gegeneinander $> 35\,\text{dB}$ und zum Cockpit $> 46\,\text{dB}$ isoliert.
     * **Zentralbox (868 MHz LoRa):** Sitzt geschützt unter der Sitzbank an der USV-Schiene für 24/7 Diebstahlschutz und PTT-Backbone via 4-Draht Bus.
     * **Cockpit (1.575 GHz GNSS & 5 GHz Wi-Fi für CP2AA):** Völlig frei von störendem 2.4-GHz-Dauerfeuer.

---

## 4. Physische Schnittstellen & Signalmatrix

### 4.1 Zentralbox Zwei-Kabel-Architektur (Bordnetz, CAN & 16-Pin Peripherie-Bus)
Um unübersichtliches Kabelchaos und unlösbare Steckerbelegungen zu verhindern, trennt OpenMotorBridge v10.0 das fahrzeugseitige Bordnetz strikt vom modularen OMB-Peripheriebus über **zwei getrennte, wasserdichte Automotive-Industriestecker (IP67/IP69K)** an der Gehäusefront der Zentralbox:

#### A. Kabel 1: Fahrzeug-Bordnetz & CAN-Bus (6-Pin Deutsch DTM06-6S)
Direkte Anbindung an Batterie, Zündschloss und Fahrzeug-CAN:
* **Pin 1:** `KL30_IN` (+12V Dauerplus abgesichert, AWG20 0.5 mm²)
* **Pin 2:** `KL15_IGN` (+12V Zündungsplus Messung & Weckimpuls, AWG22 0.34 mm²)
* **Pin 3:** `VEHICLE_GND` (Fahrzeugmasse Batterie-Minus, AWG20 0.5 mm²)
* **Pin 4:** `CAN_H` (High-Speed CAN nach ISO 11898-2, AWG24 0.22 mm²)
* **Pin 5:** `CAN_L` (Low-Speed / Dominant CAN nach ISO 11898-2, AWG24 0.22 mm²)
* **Pin 6:** `CHASSIS_SHIELD` (Rahmen-Masse / EMV-Schirmgeflecht)

#### B. Kabel 2: OMB Peripherie-Bus (16-Pin Automotive Connector, z. B. TE Superseal / Deutsch DTM 16-Pin)
Führt 4 autarke Systemzweige (jeweils 4 Adern: `VCC`, `GND`, `D+`, `D-`) und verzweigt sich außerhalb der Zentralbox im geschützten Kabelbaum in 4 separate Peitschen:

| Strang / Peitsche | Anschlusstyp | Zielkomponente | Leistung & Übertragene Signale |
| :--- | :--- | :--- | :--- |
| **Strang 1 (Front-Backbone)** | 4-Pin Automotive Sealed | **Front-Node & Cockpit** (PCBA 05) | **60W USB-PD** (`VBUS_60W`, AWG18), `GND` (AWG18), `USB_D+` / `USB_D-` (AWG26 verdrillt) |
| **Strang 2 (Koffer Links)** | 4-Pin Magnet-Abreißkupplung IP68 | **Satelliten-Pod 1** (Sena / Cardo / OMM) | **30W USB-PD** (`POD1_VBUS`, AWG20), `POD1_GND` (AWG20), `USB_D+` / `USB_D-` (AWG28 verdrillt) |
| **Strang 3 (Koffer Rechts)** | 4-Pin Magnet-Abreißkupplung IP68 | **Satelliten-Pod 2** (Cardo / Sena / OMM) | **30W USB-PD** (`POD2_VBUS`, AWG20), `POD2_GND` (AWG20), `USB_D+` / `USB_D-` (AWG28 verdrillt) |
| **Strang 4 (Heck-Radar)** | Binder M5 4-Pin IP67 | **Heck-Radar MR20** (PCBA 08) | **12V geschaltet** (`RADAR_12V`, AWG22), `RADAR_GND` (AWG22), `USB_D+` / `USB_D-` (AWG28 verdrillt) |

### 4.2 Universal Front-Node (PCBA 05) Cockpit-Schnittstellen (60W Power Budget)
Der Front-Node bündelt sämtliche Front-, Cockpit- und Sensorschnittstellen und wird über Strang 1 des Backbone-Kabels mit bis zu **60W USB-PD** versorgt:
* **Modularer Sensor-Puck ("Körbchen"):** Integriert u-blox SAM-M10Q Multi-GNSS (Zenitsicht), TI TMP117 NIST-Thermometer, OPT3001 Lichtsensor und Knowles I2S MEMS. Rastet werkzeuglos direkt oben auf den Front-Node ein; kann im Pkw/Van per 1,5m Verlängerungskabel an die Windschutzscheibe geclipst werden (`car_dashboard_wedge_dock.scad`).
* **Cockpit-Displays & Anzeigen:** Speist die beiden Cockpit Speaker Corner Pods (`cockpit_speaker_corner_pod.scad`) mit Dual-OLED-Displays in den Rockford Fosgate Lautsprechergittern (2W für Radar-Balken, TPMS, Turn-by-Turn).
* **Bedienelemente & Totwinkel-LEDs:** Direkte Anbindung an symmetrische Dual Under-Perch Spiegel-Pods (JST-GH).
* **Dediziertes Motorrad-Navi (15W - Power-Only):** Speist Garmin Zūmo XT2 / Tread / Chigee AIO-5 / Carpuride direkt am Front-Node über eine 12V/1.25A bzw. 5V/3A DC-Leitung. **Hardware-Regel:** Reine Stromversorgung ohne USB-Host-Datenleitungen, damit Garmin/Chigee sofort in den normalen Navigationsbetrieb starten und nicht in den PC-Massenspeicher-Modus verfallen!
* **Smartphone-Schnellladung (bis 27W):** USB-PD Speisung für SP Connect / QuadLock Ladehalterung am Lenker oder über den 4-Port Handschuhfach-Hub.
* **Action-Cam Dauerstrom (10W - Power-Only / BC 1.2 DCP):** Wetterfeste USB-C Zuleitung direkt am Front-Node (`PCBA 05`, `J8`) für GoPro Hero oder Insta360 X3/X4 am Lenker oder an der Verkleidung. **Hardware-Regel:** D+/D- sind physikalisch vom `USB2514B` USB-Host isoliert und im Kamerastecker nach USB BC 1.2 DCP ($R < 200\,\Omega$) gebrückt. Die Kamera erkennt ein reines Hochstrom-Ladegerät, startet bei Zündung-AN sofort die Schleifenaufnahme und blockiert niemals in einem "PC verbunden / Webcam / MTP"-Dialog! Die direkte Front-Node-Anbindung am Cockpit spart zudem den unlogischen Umweg über das Handschuhfach.
* **4-Port Handschuhfach Media & Power-Injection Hub (`glovebox_power_injection_hub.scad`):** Wird über ein kombiniertes High-Power & USB 2.0 Kabel gespeist; liefert saubere 30W Schnellladeleistung sowie 10W geschaltete Dongle-Power, 1x freien Media-Port und führt die **Harley Headset-Emulation via USB** an Port 4 zur Headunit. Alle im Handschuhfach angeschlossenen Geräte verbleiben vollständig im Fach.

---

## 5. Integration in OEM-Infotainmentsysteme

### 5.1 Harley-Davidson Boom! Box GTS & Skyline OS

#### 5.1.1 Harley Headset-Emulation via USB & Apple CarPlay / Android Auto Freischaltung
* **Hintergrund & USB-Emulation:** Apple CarPlay setzt im Fahrzeug ein betriebsbereites Sprachmikrofon voraus. Harley-Davidson verriegelt CarPlay in der Boom! Box GTS und Skyline OS Firmware standardmäßig und verlangt entweder das kabelgebundene 7-Pin DIN-Headset oder das proprietäre Bluetooth-Funkmodul **HD-WHIM** (*Wireless Headset Interface Module*, $> 350\,\text{€}$).
* **Digitale Headset-Emulation via USB:** OpenMotorBridge wickelt die Headset- und Mikrofonanbindung **vollständig digital über USB** ab! Über die USB 2.0 High-Speed Verbindung vom Front-Node (`PCBA 05`) über Port 4 des Handschuhfach-Hubs (`glovebox_power_injection_hub.scad`) an die OEM-Headunit meldet sich OpenMotorBridge als konformes Apple MFi-Headset bzw. USB Audio Class Device an.
* **Ergebnis:** Die Boom! Box GTS / Skyline OS erkennt sofort ein aktives digitales Headset und schaltet Apple CarPlay sowie Android Auto im 6,5"- bzw. 12,3"-Touchscreen frei – **ohne teures WHIM-Modul**, ohne fehleranfällige analoge Brückenstecker und ohne teure Händler-Freischaltung (Digital Tech).
* **Bidirektionale Audio-Integration:** Fahrer- und Beifahrer-Helmmikrofone werden digital direkt in den Freisprech- und Sprachsteuerungs-Kanal der Headunit geroutet (Siri, Anrufe, Adresssuche), während Navi-Ansagen und Medien verlustfrei und mit sanftem Ducking ($-12\,\text{dB}$) in die Intercom-Audiomatrix zurückgespeist werden – absolut immun gegen analoge Masseschleifen und Lichtmaschinen-Pfeifen.

#### 5.1.2 Universal Cockpit & Front Hub (PCBA 05): USB-Subsystem, Live-Traffic & PTT
Der Front-Knoten (PCBA 05) dient auf **allen Motorrädern** als universeller Cockpit-Knoten und eliminiert empfindliche Signalkabel über den mechanisch beanspruchten Lenkkopf:
* **Nativer 4-Draht USB-Backbone zur Zentralbox:** Der Front-Node kommuniziert über den geschirmten **4-Draht Automotive USB 2.0 Bus (`VBUS`, `GND`, `D+`, `D-`)** mit $< 0{,}2\,\text{ms}$ Latenz mit der Zentralbox (Strang 1 des 16-Pin Peripheriebusses). Zero Funk-Jitter, unempfindlich gegen EMV-Einstrahlung von Zündkerzen oder LED-Scheinwerfern.
* **Drahtgebundener Lenker-PTT (Optokoppler an `J3` / GPIO 0, $< 1{,}8\,\text{ms}$ Latenz):** Nur $30\dots 50\,\text{cm}$ kurzes, geschütztes Kabel am Lenker - kein bruchgefährdetes Signalkabel über den schwenkenden Lenkkopf nach hinten zur Zentralbox!
* **Digitales I2S-MEMS Ambient-Mikrofon (Sipeed / Zilltek MSM261S4030H0R / Knowles SPH0645):** Berechnet Umgebungs- und Fahrtwindgeräusche (dB-A/RMS) direkt an der Front für automatische Helmlautstärke-Nachführung (AGC) via Xtensa Vektor-DSP. Standard-I2S mit hoher Bauteilverfügbarkeit.
* **Automotive USB 2.0 Subsystem (Microchip USB2514B 4-Port Hub & Power-Architektur):**
  * **Upstream Host Port (`J4`):** Führt über das kombinierte Power- und High-Speed-USB-Kabel zum 4-Port Handschuhfach-Hub (`glovebox_power_injection_hub.scad`) und dort an Port 4 zur Harley Boom! Box GTS / Skyline OS für Headset-Emulation und CarPlay.
  * **Downstream Port 1 (Smartphone-Datenlink):** High-Speed Datenverbindung zum Smartphone am Handschuhfach-Port 1 (oder Lenkerhalterung `J5`) für kabelgebundenes CarPlay / Android Auto.
  * **Downstream Port 2 (`J6` / CP2AA-Dongle):** Geschalteter $+5{,}0\,\text{V}$ VBUS über `TI TPS2051B` Lastschalter mit softwaregesteuertem **2,5s-Kaltstart**, automatischem **Not-Power-Gating bei Verkleidungshitze** und 0.0 µA Deep-Sleep für den Wireless CarPlay / Android Auto Dongle (3M Dual-Lock im Verkleidungshohlraum).
  * **Downstream Port 3 (Handschuhfach Media-Port):** Durchgeschliffener USB-Port an Handschuhfach-Port 3 - bleibt zu **$100\,\%$ frei für MP3/FLAC USB-Sticks und offizielle OEM-Software-Updates** (inkl. hardwareseitiger Port-Sense Überwachung).
  * **Downstream Port 4 (ESP32-S3 Interner OTG-Port):** Dedizierter nativer USB-Port des ESP32-S3 für digitale Headset-Emulation (MFi / USB Audio Class) und CDC-NCM Ethernet Tethering zur OEM-Headunit.
  * **USB-C Service Port (`J7`):** Nativer Diagnose-, Kalibrier- und Flash-Port direkt am ESP32-S3.
  * **Strikte Trennung von Navi (`J10`) & Action-Cam (`J8`):** Beide Geräte erhalten **ausschließlich reine Stromversorgungs-Leitungen (Power-Only / BC 1.2 DCP)** von den Schaltreglern und besitzen **keinerlei Datenverbindung zum USB2514B Hub**, wodurch PC-Verbindungs- und Webcam-Blockaden ausgeschlossen sind.
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
* **Automotive Stromversorgung:** Vollständig gespeist über Strang 1 des OMB-Peripheriebusses (60W USB-PD); integrierter TI TPS63070 Buck-Boost Wandler garantiert Kaltstart-Stabilität nach ISO 7637-2 Pulse 4.

### 5.2 BMW Motorrad ConnectedRide & CAN-Bus Integration
* **Echtzeit-Telemetrie:** Über den integrierten TCAN334G CAN-Transceiver lauscht die Zentralbox im Listen-Only-Modus auf dem Fahrzeugbus und erfasst Raddrehzahlen, Schräglage und Blinkersignale.
* **Display-Warnmeldungen:** Statusmeldungen können direkt im Motorrad-TFT-Display generiert werden.

### 5.3 Heck-Radar 2.0 & Totwinkel-Assistent (Wheeltec MR20 77 GHz mmWave & Garmin Varia) an dediziertem Heck-Träger
* **Heck-Montage & Justage (Ohne Pod 3):** Das Heck-Radar wird vollkommen autark und ohne zusätzliches Gehäuse direkt über einen dedizierten, minimalen Halter (z. B. [`adventure_rack_radar_mount.stl`](../../hardware/cad/stl/02_pod_base/adventure_rack_radar_mount.stl) unter der Gepäckbrücke oder modellspezifische Adapter) montiert. Die Anbindung erfolgt über Strang 4 des 16-Pin Automotive Kabelbaums (Pins: 12V geschaltet, GND); die 20 Hz Radar-Zieltelemetrie wird über die geschirmte High-Speed Datenleitung (CAN/UART) an die Zentralbox übertragen. Eine bionische Hirth-Verzahnung ermöglicht eine verzugsfreie 100% waagerechte Ausrichtung.
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
     * Die Reed-Kontakte an den Pod-Slide-in-Deckeln erkennen das unbefugte Öffnen der Koffer-Pods.
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
  * Kombiniert den $20 \times 10 \times 5\,\text{mm}$ N52-Neodym-Magnetschlüssel für die berührungslose Entriegelung des Pod-Slide-in-Deckels mit einem stummen LoRa 868 MHz Silent Alarm Pager in einem kompakten PA12-MJF Gehäuse ($58 \times 34 \times 13\,\text{mm}$).
  * Ein integriertes $0{,}5\,\text{mm}$ Weicheisen-Abschirmblech schützt interne Elektronik und Akku vor Magnetfeldsättigung.
* **Kryptografische Absicherung & Selektivität:**
  * Verschlüsselt mit AES-128 GCM und 32-Bit Monotonic Nonce (Anti-Replay). Nur der autorisierte Pager des Besitzers schlägt an; unbefugtes Abhören oder Auslösen von Fehlalarmen ist ausgeschlossen.
* **Zero-False-Alarm & Anti-Theft:**
  * Bei anwesendem BLE-Token des Fahrers ($< 1{,}5\,\text{m}$) wird das Öffnen des Pod-Deckels als legitim erkannt. Unbefugtes Aufhebeln ohne Keyfob löst sofort einen lautlosen Pager-Notruf mit bis zu 4,5 km Reichweite aus.
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
  * Im Standby / Deep Sleep sendet der ESP32-S31 im Zeitmultiplex abwechselnd **Apple Find My (FMNP)** und **Google Find My Device (FMDN)** BLE-Werbepakete (alle 2,0 Sekunden, Sendedauer ca. $2{,}5\,\text{ms}$).
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
  1. **Automotive 4-Draht USB-PD & USB 2.0 Backbone (Kabelgebunden):** Hochrobuster physischer Bus (`VBUS`, `GND`, `D+`, `D-`) zwischen Zentralbox, Front-Node und den Koffer-Pods. Ersetzt das frühere UWB-Funkbackbone vollständig: bis zu 60W USB-PD Ladeleistung, latenzfreie USB 2.0 Audio- und Steuerdaten, 100 % immun gegen Funkschatten durch Regenkombis, nasses Gepäck oder Alukoffer.
  2. **Heck 5 GHz V2X & 77 GHz mmWave:** ESP32-C5 mit 5 GHz Raw-Packet-Injection (802.11p OCB) für fahrzeugübergreifende V2X-Warnmeldungen (CAM / DENM) plus Wheeltec MR20 mmWave Radar für 360°-Umfeldüberwachung und Notfall-Kollisionsstrobe.
  3. **Front 5 GHz / 6 GHz Wi-Fi (C5 / E22):** Dedizierter High-Speed Funklink am Front-Knoten für drahtloses Apple CarPlay und Android Auto (10 cm Line-of-Sight zum Smartphone) sowie High-Speed Dashcam-Videosync. Vollständig befreit von BLE-Overhead.
  4. **2.4 GHz Audio & Geometrischer BLE-Master:**
     * *Zentralbox:* Dedizierter Qualcomm HD-Bluetooth Audio-SoC (QCC3084) mit Dual-A2DP und LE Audio / Auracast (synchroner Audio-Mix für Fahrer- und Sozius-Helm) samt HFP-Telephonie-Engine. Der **ESP32-S31 fungiert als zentraler geometrischer BLE-Master** mit externer Gehäuse-U.FL-Antenne und bündelt sämtliche Peripherie (OEM-Adapter in beiden Pods, Lenkertaster, Action-Cam, Keyfob, TPMS und PWA Dashboard). Das interne Wi-Fi des S31 ist im Fahrbetrieb deaktiviert, um jegliche HF-Interferenz mit dem QCC3084 zu verhindern.
  5. **LoRa 868 MHz (Semtech SX1262):** 3-Kanal-Langstrecken-Backbone zwischen den Fahrzeugen (Public Announcement, Private Session Group, Micro-Cluster/FOB-Pager) mit kilometerweiter Reichweite direkt an der USV-Schiene.

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
      - **Modus B (Reiner Pkw-/Camper-Konvoi & Rallye-Orga):** Pod 1 mit OMM 2.4 GHz Modul (OpenMotorMesh), Pod 2 mit Midland PMR446 Funkgerät für universellen Jedermannfunk.
      - **Modus C (Hybrid-Lead & OMM-Anchor):** Pod 1 mit OMM 2.4 GHz Modul (verbindet alle OMB-Bikes im Konvoi), Pod 2 wahlweise Sena oder Cardo für Gastfahrer.
    * **Audio-Integration im Pkw (Headset-frei & Freisprech-Komfort):**
      - **Option 1 (Pkw-Freisprecheinrichtung via Qualcomm QCC3084):** Die Zentralbox unterm Sitz koppelt sich per Bluetooth (HFP 1.8 / A2DP) vollautomatisch als Mobiltelefon mit der Pkw-Freisprechanlage. Die Fahrzeuginsassen hören den Gruppenfunk glasklar über die Autolautsprecher und sprechen freihändig über das Pkw-Dachmikrofon!
      - **Option 2 (AAWireless / CarPlay Clean Power-Injection & OEM-Media-Passthrough):** Die werkseitigen USB-Media-Buchsen moderner und älterer Pkw liefern oft streng nach alter USB 2.0-Norm nur $500\,\text{mA}$ ($2{,}5\,\text{W}$) oder instabile Spannung. Beim Starten von Wireless Android Auto / Apple CarPlay (AAWireless, Ottocast, Carlinkit) erzeugt das 5-GHz-WLAN-Modem Stromspitzen von $1{,}2\dots 1{,}8\,\text{A}$, was am OEM-Port zu endlosen Bootloops, Hitze und Verbindungsabbrüchen führt. **Die OMB-Lösung:** Der AAWireless-Adapter wird direkt an den Front-Node / Core-Unit USB-Port von OpenMotorBridge angeschlossen und aus dem bordeigenen 12V-Schaltregler mit felsenfesten $5\,\text{V}\,/\,3\,\text{A}$ ($15\,\text{W}$) versorgt. Zum OEM-Media-USB-Port des Autos führt lediglich ein reines High-Speed Datenkabel (`D+`, `D-`, `GND` bei galvanisch getrenntem / blockiertem `VBUS`). Der Auto-Bildschirm empfängt saubere USB-Daten, liefert aber keinen Milliampere Strom – 100 % Stabilität, null Abstürze!
      - **Option 3 (Autarkes OMM-Handgerät / Tischmikrofon):** Ein autarkes OMM 2.4 GHz Modul mit Schwanenhals-Mikrofon oder PTT-Taste liegt griffbereit auf der Mittelkonsole für den Beifahrer / Tourguide (angeschlossen an Port `J6` des Cockpit-Satelliten).
  * **All-in-One Car Support Core Unit (Kompakt vereint & Thermoschutz):**
    * **Zentralbox (`PCBA 01`) und Front-Node (`PCBA 05`) vereint:** Da UWB in v10.0 vollständig durch den drahtgebundenen 4-Draht Automotive-Bus ersetzt wurde, entfällt jegliches HF-De-Sensing. Beide Platinen werden kompakt als gemeinsame Doppel-Einheit („All-in-One Car Support Core Unit“) im thermisch kühlen Fußraum unter dem Beifahrersitz oder im Mitteltunnel montiert.
    * **Nur EIN Stromkabel nötig:** Ein einziges 12V-Kabel zur Zigarettenanzünderdose oder zum Sicherungskasten versorgt die gesamte Einheit – kein Y-Kabel-Wirrwarr quer durch den Fahrzeuginnenraum mehr nötig!
    * **SAM-M10Q GNSS-Puck:** Unauffällig an der Windschutzscheibenecke über ein dünnes Sensorkabel angebunden.
  * **Externe 868-MHz-Magnetfuß-Dachantenne als Default (15–25 km LoRa-Reichweite):**
    * Im geschlossenen Stahlblech-Pkw dämpft die Karosserie Funkwellen im Innenraum um $20\dots 30\,\text{dB}$ (Faradayscher Käfig).
    * Referenz-Kit 5 beinhaltet daher standardmäßig einen kompakten $\varnothing 30\,\text{mm}$ Mini-Magnetfuß auf dem Dach mit $2{,}5\,\text{m}$ dünnem RG-174 Koaxialkabel, das verdeckt durch die elastische Gummidichtung der Heckklappe geführt wird.
    * Das Metalldach dient als $360^\circ$ Groundplane ($+3\,\text{dBi}$ Gewinn) und garantiert $15\dots 25\,\text{km}$ echte LoRa-Reichweite zur Motorradgruppe über Täler und Pässe hinweg.
  * **Verdeckte Kabelverlegung:**
    * Flache USB-C Kabel zu den Sonnenblenden-Pods verlaufen unsichtbar hinter den Gummidichtungen der A-Säulen.
  * **Drahtlose oder kabelgebundene Pkw-Telemetrie:**
    * Wahlweise drahtlos via Bluetooth 5.0 (BLE) mit einem kompakten OBD2-Dongle (vGate / OBDLink) im Fahrerfußraum oder kabelgebunden über den 12-Pin Fahrzeug-Satelliten.
    * Pkw-Daten (Geschwindigkeit, Drehzahl, Tankfüllstand, Motortemperatur) werden autark ins 868-MHz-LoRa-Mesh übertragen - ohne Smartphone-Abhängigkeit.
* **Live-Gruppenüberwachung ohne Mobilfunknetz (PWA Fleet Dashboard):**
  * Auf einem im Pkw montierten iPad oder Android-Tablet läuft das PWA-Dashboard im Offline-Kartenmodus.
  * Über das 868 MHz LoRa-Mesh empfängt das Begleitfahrzeug im Sekundentakt Telemetriedaten (Position, Geschwindigkeit, SOS-/Sturzalarm, Reifendruck, Außentemperatur) aller Motorräder im Umkreis von bis zu $15\,\text{km}$ - autark, robust und vollkommen unabhängig von Mobilfunkmasten.

---

## 6. Internet-Uplink, V2X-Schwarmdaten & Waze "Auto-Klick" (Android Companion)

OpenMotorBridge besitzt für erweiterte Telematik- und Community-Funktionen einen dedizierten **Internet-Uplink über die Android Companion-App** (`bar.f0o.omb`), während das Gesamtsystem für alle fahr- und sicherheitskritischen Funktionen 100 % autark und offline-fähig bleibt:

### 6.1 Der physische Übertragungsweg: Warum BLE / USB statt Wi-Fi genutzt wird
* **Physische Wi-Fi-Exklusivität:** Während des Betriebs von drahtlosem Android Auto oder Apple CarPlay ist die WLAN-Schnittstelle des Smartphones mit dem 5-GHz-WLAN des COTS-Dongles belegt. Das Smartphone kann sich hardwarebedingt nicht gleichzeitig mit einem 2,4-GHz-WLAN des ESP32 verbinden.
* **Unterbrechungsfreier Datenkanal:** Die Übertragung zwischen OpenMotorBridge (ESP32-S31) und dem Smartphone erfolgt daher **strikt über Bluetooth Low Energy (WebBLE / RFCOMM)** oder über das USB-Kabel am Front-Node. Bluetooth und Wi-Fi laufen auf getrennten Funkstacks völlig störungsfrei parallel.

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
   * OpenMotorBridge überträgt diese Daten über den 4-Draht Bus und BLE an die Companion-App, die sie über das Mobilfunknetz (4G/5G) in das **OpenTrafficMap-Projekt** einspeist und lokale Gefahren-Tiles (GeoJSON) lädt.
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
* Sämtliche fahr- und sicherheitskritischen Funktionen – das 77-GHz-Radar ($< 15\,\text{ms}$), der 4-Draht USB-Backbone ($< 0{,}2\,\text{ms}$), die Intercom-Mesh-Matrix (Sena/Cardo/OMM), die IMU-Sturzerkennung und das Notbremsblinken – arbeiten zu **100 % offline und autark** auf der Motorrad-Hardware.
* Im tiefsten Funkloch auf abgelegenen Pässen funktioniert OpenMotorBridge mit identischer Präzision und Schutzwirkung wie im Stadtzentrum.

---

## 7. Dokumentations-Architektur & Kapitel-Wegweiser (Single Source of Truth)

Zur Vermeidung von Redundanzen und zur Gewährleistung klarer Zuständigkeiten ist die Dokumentation modular gegliedert. Jedes Fachthema besitzt eine verbindliche **Single Source of Truth (SSOT)**:

| Themenbereich | Verbindliches Referenzdokument | Inhalt & Fokus |
| :--- | :--- | :--- |
| **Intercom-Profile & Matrix** | **[Kapitel 02](02_intercom_matrix_profiles.md)** | Sena Mesh 2.0/3.0, Cardo DMC Gen1/2, Midland PMR, Audio-Routing & Pegelanpassung |
| **Akustik, DSP & Ducking** | **[Kapitel 03](03_audio_dsp_acoustics.md)** | Raised-Cosine Filter, Ducking (-12 dB / -18 dB), Wind-AGC, Latenzbudgets |
| **Mesh, LoRa & Navigation** | **[Kapitel 04](04_mesh_lora_navigation.md)** | SX1262 LoRa-Mesh, Dynamisches Routing, Notfall-SOS, Cluster-Merging |
| **OMM Intercom-Module (2.4G & 446M)** | **[Kapitel 04b](04b_omm_intercom_module.md)** | PCBA 09 (2.4 GHz HD-Mesh) & PCBA 10 (446 MHz PMR/DMR), ECE 22.06 UCS |
| **Power Management & USV** | **[Kapitel 05](05_power_management_ups.md)** | LM5164 Step-Down, BQ24075 USV, Dual-Batterie Kaltstart, JEITA-Thermomanagement |
| **Telemetrie & Blackbox** | **[Kapitel 06](06_telemetry_blackbox_webdav.md)** | MicroSD-FAT32 Ringpuffer, 15-State EKF Schräglage, WebDAV / Nextcloud Sync |
| **PCBA Hardware & Pinouts (SSOT)**| **[Kapitel 07](07_pcba_hardware_pinouts.md)** | **Alle Platinen (PCBA 01 bis 10)**, vollständige Pinbelegungen, Bauteilwerte |
| **Gehäuse, Mechanik & CAD (SSOT)**| **[Kapitel 08](08_enclosures_mechanics_cad.md)** | **Alle CAD-Modelle**, OpenSCAD Parameter, ECE-Normen, unverlierbare Muttern |
| **Firmware-Architektur** | **[Kapitel 09](09_firmware_architecture.md)** | FreeRTOS Task-Matrix, 4-Draht USB-PD & USB 2.0 Protokoll, 5-Gesten-Engine |
| **WebApp PWA Dashboard** | **[Kapitel 10](10_webapp_pwa_dashboard.md)** | Ride HUD, WebBLE Protokoll, Pod- & Profil-Konfiguration, Offline-OSM-Vektorkarten |
| **CarPlay / Android Auto Bridge** | **[Kapitel 11](11_carplay_android_auto_bridge_architecture.md)**| Virtual WHIM, CP2AA Bridge, Multi-Path Wi-Fi/Cellular, Headless Dongle |
| **CAN-Bus Fahrzeugprofile** | **[Kapitel 12](12_can_bus_vehicle_profiles.md)** | BMW, KTM, Ducati, Harley CAN-Matrizen, LIN/K-Line Interfaces |
| **Simulation & Testbench (HIL/SIL)**| **[Kapitel 13](13_simulation_testbench.md)** | Python Netlist Validator, FreeRTOS Timing-Verifikation, Signalintegrität |
| **EMV & HF-Hardening** | **[Kapitel 14](14_emv_rf_hardening.md)** | CISPR 25 Class 5, 8-Band HF-Matrix, ESD-Schutznetzwerke, Koexistenz |
| **BOM, Beschaffung & Fertigung**| **[Kapitel 15](15_bom_manufacturing.md)** | **Vollständige Bauteillisten**, JLCPCB SMT-Daten, Zukaufteile, COTS-Docks, Kabelbäume |
| **Bauanleitung & Montage** | **[Kapitel 16](16_build_instructions_assembly.md)** | Schritt-für-Schritt Aufbau, Kabelkonfektionierung, Drehmomente, Inbetriebnahmetests |
| **Normen & Referenzen** | **[Kapitel 17](17_standards_references.md)** | ECE 22.06, DIN/ISO-Normen, IEEE 802.11, Bluetooth SIG, USB-IF Spezifikationen |
| **Rechtliche Konformität & Datenschutz** | **[Kapitel 18](18_legal_compliance_dsgvo.md)** | RED 2014/53/EU, FCC Part 15, CE-Kennzeichnung, DSGVO Telemetrie-Konformität |

