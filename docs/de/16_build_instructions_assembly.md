# 16 - Bauanleitung, Verkabelung & Fahrzeug-Installation

Dieses Dokument ist die vollständige, praxisorientierte Schritt-für-Schritt-Bauanleitung für den Zusammenbau und die fahrzeugspezifische Montage eines kompletten **OpenMotorBridge (v10.0 Native USB-PD & Edge-AI Generation)** Gesamtsystems.

---

## 1. Übersicht des Gesamtkits (Was wird gebaut?)

Ein vollständiges OpenMotorBridge-Fahrzeugkit der Generation v10.0 verzichtet vollständig auf fehleranfällige UWB-Nahbereichsfunkstrecken, Motorschlitten und Kassetten-Servos. Stattdessen setzt es auf einen **robusten 4-Draht Automotive USB-PD & USB 2.0 Bus (`VBUS`, `GND`, `D+`, `D-`)** mit bis zu 60 W Leistung je Strang, kombiniert mit dem **ESP32-S31** (Dual-Core 320 MHz RISC-V mit 128-bit SIMD AI-Beschleuniger für On-Device Sprach-/Audioerkennung) und dem dedizierten **Qualcomm QCC3084** Bluetooth-Audio-SoC.

```text
                      +-------------------------------------------------------------+
                      |               1x ZENTRALE MAIN BOX (IP67)                   |
                      |            (Unter der Sitzbank / Batteriebrücke)            |
                      |    * Hauptrechner: ESP32-S31 (Dual-Core RISC-V @ 320 MHz,   |
                      |      128-bit SIMD AI-Audio-Engine, Native USB 2.0 480 Mbps) |
                      |    * Audio-SoC: Qualcomm QCC3084 (Dual-A2DP, aptX HD, HFP)  |
                      |    * Notfunk/SOS: SX1262 LoRa 868 MHz (Taoglas FXP895)      |
                      |    * Power Delivery: Multi-Port USB-PD Engine (bis 60 W)    |
                      |    * USV-Puffer: 2.200 mAh LiPo mit Molex Micro-Fit 3.0     |
                      +------------------------------+------------------------------+
                                                     |
                         1x ZENTRALER KABELBAUM (DEUTSCH DTM-12 IP67/IP69K)
                                                     |
        +----------------------------+---------------+----------------------------+
        |                            |                                            |
        v Strang 1                   v Strang 2                                   v Strang 3
  (4-Draht USB-PD)             (4-Draht USB-PD)                             (4-Draht USB-PD / CAN)
+-------------------+        +-------------------+                        +-------------------+
| 4-Pin Magnet-     |        | 4-Pin Magnet-     |                        | 1x HECK-RADAR 2.0 |
| Abreißkupplung    |        | Abreißkupplung    |                        | (Kennzeichen/Heck)|
| (HytePro M411)    |        | (HytePro M411)    |                        | * Wheeltec MR20   |
+---------+---------+        +---------+---------+                        |   77 GHz (PCBA 08)|
          |                            |                                  | * 36x Warn-LEDs   |
          v Kofferwand-Tülle           v Kofferwand-Tülle                 | * Drip-Loop &     |
+-------------------+        +-------------------+                        |   Roost-Deflector |
| 1x POD 1 LINKS    |        | 1x POD 2 RECHTS   |                        +-------------------+
| (Im Hartschalen-  |        | (Im Hartschalen-  |
|  koffer)          |        |  koffer)          |
| * Slide-in Deckel |        | * Slide-in Deckel |
|   mit Dichtung &  |        |   mit Dichtung &  |
|   FOB-Magnetverschl|       |   FOB-Magnetverschl|
| * Zwischendeckel  |        | * Zwischendeckel  |
|   (Dry-Flap)      |        |   (Dry-Flap)      |
| * Koffer-USB-Lade-|        | * Koffer-USB-Lade-|
|   dose (5V/12V PD)|        |   dose (5V/12V PD)|
| * PCBA 03 Smart-  |        | * PCBA 03 Smart-  |
|   Gateway-Modul   |        |   Gateway-Modul   |
|   (Sena / Cardo / |        |   (Sena / Cardo / |
|    OMM / Midland) |        |    OMM / Midland) |
+-------------------+        +-------------------+
                                       |
                                       | Strang 4: 4-Draht Automotive Bus (USB-PD / USB 2.0)
                                       | Verlegt durch den offenen Harley-Backbone-Kabelkanal
                                       | (100 % lötfrei, ZERO Tank-Demontage via Nylon-Fish-Tape)
                                       v
                     +------------------------------------+
                     |  1x FRONT-KNOTEN & COCKPIT-HUB     |
                     |  (Am Lenker-Riser / Gabelbrücke)   |
                     |  * u-blox SAM-M10Q Multi-GNSS      |
                     |  * TI TMP117 & OPT3001 Sensoren    |
                     |  * Knowles MEMS Fahrtwind-Sensor   |
                     |  * Qi-Wireless / USB-PD Phone-Port |
                     +-----------------+------------------+
                                       |
                                       +-----------------------------------+
                                       |                                   |
                                       v                                   v
                       +-------------------------------+   +-------------------------------+
                       | 2x SYMMETRISCHE SPIEGEL-PODS  |   | 1x HANDSCHUHEFACH 2-PORT HUB  |
                       | (Links & Rechts Spiegelfüße)  |   | (Rechtes Fach, CVO ST)        |
                       | * Links:  PTT-Taste & BSD-LED |   | * Unterseiten-OEM-Tülle       |
                       | * Rechts: Cam-Tag & BSD-LED   |   | * 1x Wireless CarPlay Dongle  |
                       | * Bilaterale Totwinkel-Warnung|   | * 1x Freier USB-Ladeport      |
                       +-------------------------------+   +-------------------------------+
```

---

## 2. Bereitstellung vor Montagebeginn (Pre-Assembly Checklist)

> [!TIP]
> **100 % lötkolbenfreie Montage (IKEA-Prinzip) & Native USB-DFU:**  
> Alle 3D-Druckteile (`.scad` / `.stl`) wurden mit definierten Toleranzen ($+0{,}15\,\text{mm}$ für HP MJF PA12 bzw. ASA/PET-CF) konstruiert. Auf das fehleranfällige Einschmelzen von Gewindebuchsen (Ruthex) wurde im gesamten System konsequent verzichtet: Alle Verschraubungen nutzen formschlüssige **DIN 934 Sechskant-Mutterntaschen** (einfach von Hand einlegen). Selbstschneidende Gewinde in Kunststoff sind verboten.  
> **Native USB-DFU & Dual-Power Input:** Alle Controller (ESP32-S31, ESP32-C6) besitzen integrierte USB-Serial/JTAG-Peripherie. Die Zentralbox unterstützt Dual-Power Input: Auf der Werkbank reicht ein ganz normales USB-C Smartphone-/Laptop-Netzteil (oder PC USB-Port) – **kein 12V-Labornetzteil mehr nötig!** Jede Baugruppe wird über ein Standard-USB-C-Kabel direkt geflasht.

Alle Einzelteile, Platinen-Bestelldaten und COTS-Zukauflisten sind detailliert in **[Kapitel 15: Stücklisten & SMT-Fertigungsdaten](15_bom_manufacturing.md)** aufgeführt. Vor Montagebeginn sicherstellen, dass folgende Baugruppen bereitliegen:

* [ ] **3D-Druckteile (MJF PA12 schwarz oder FDM ASA/PET-CF):**
  * **1x Main Box:** Unterwanne mit Dämpferdomen, Zwischenboden mit $70 \times 10\,\text{mm}$ Kabelbucht, schwenkbare Akkubrücke mit Rastfeder ([`main_box_battery_bridge.stl`](../../hardware/cad/stl/01_main_box/main_box_battery_bridge.stl)), Gehäusedeckel ([`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl)).
  * **2x Koffer-Pods v10.0:** Pod-Wannen für Koffer-Innenmontage, 2x Slide-in Deckel mit integrierter Neodym-Riegelaufnahme, 2x Spritzschutz-Zwischendeckel (Dry-Flap mit Dichtlippe), 2x USB-Ladeport-Aufnahmerahmen.
  * **1x Front-Knoten Riser-Gehäuse:** Kompakte Unterwanne mit Riser- / Triple-Tree Klemmschelle, Gehäusedeckel mit Gore-Membranaufnahme für MEMS-Fahrtwind-Sensor.
  * **2x Symmetrische Under-Perch Spiegel-Pods (Links & Rechts):** Formschöne Halterungen zur Montage unter beiden Spiegelschrauben ([`under_perch_mirror_pod.stl`](../../hardware/cad/stl/04_front_node/under_perch_mirror_pod.stl)) mit Führung für taktilen Taster (Links: PTT; Rechts: Cam-Highlight) und LED-Linsentrichter für bilaterale Totwinkel-Warnanzeige (BSD).
  * **1x Handschuhfach-Hub-Gehäuse:** Kompakter 2-Port USB-Verteiler für das rechte Handschuhfach der 2024+ CVO Road Glide ST.
  * **1x Heck-Radar Halterung:** MR20 Radar-Gehäuse mit Hirth-Neigungsverstellung, Kennzeichenträger und integriertem Schmutzfänger (Roost-Deflector).
* [ ] **Vollautomatisch bestückte Platinen (SMT-gefertigt):**
  * **1x PCBA 01 (Zentralbox):** Host-Platine mit **ESP32-S31**, **Qualcomm QCC3084**, SX1262 LoRa 868 MHz, Automotive USB-PD Hub-Engine (z.B. SW3526 / TI TPS25750), Dual-Power Input (12V DTM-12 & USB-C PD Sink mit Ideal-Diode OR-ing), DTM-12 Buchsenheader und USB-C DFU-Port. *(DW3110 UWB entfällt komplett!)*
  * **2x PCBA 03 (Koffer-Pod Gateway):** Universal-Schnittstellenplatine mit USB-PD Sink/Buck-Regler, Koffer-USB-A/C Ladeport, Intercom-Audio-Routing (Sena / Cardo / OMM / Midland) und PTT-Tastung. *(Servos und Hubmagnete entfallen komplett!)*
  * **1x PCBA 05 (Front-Knoten Riser-Hub):** Kompakt-Platine mit SAM-M10Q GNSS, TMP117 / OPT3001, Knowles MEMS Fahrtwind-Mikrofon und 12V/USB-PD Zubehörspeisung.
  * **2x PCBA 05B (All-in-One Under-Perch Platine):** Baugleiche Mini-Platinen für linken und rechten Spiegelfuß mit hochpräzisem Mikrotaster (Links: PTT; Rechts: Cam-Highlight) und ultraheller Amber-LED (BSD).
  * **1x PCBA 08 (Heck-Radar Sub-MCU):** 77 GHz Radar-Controller mit 36x Strobe-Warn-LEDs.
* [ ] **V4A Edelstahl-Normteile & Magnete (100 % lötfrei):**
  * 8x DIN 934 / DIN 985 M3 Edelstahlmuttern (Gehäuse-Mutterntaschen)
  * 6x DIN 934 M4 Muttern (Radar- & Riser-Klemmung)
  * 4x M3 x 40 mm Schrauben (Zentralbox), 4x M3 x 20 mm Schrauben (Front-Knoten)
  * 8x M2.5 x 6 mm Platinenschrauben (Zentralbox & Front-Node)
  * 4x N52 Neodym-Magnete ($\varnothing 8 \times 3\,\text{mm}$) für die Kofferdeckel-Verriegelung
  * 1x OMB Smart Keyfob mit integriertem N52 Entriegelungs-Gegenmagneten
* [ ] **Dichtungen, Pufferakku & Antennen:**
  * Silikon-Rundschnur Ø 1,5 mm Shore 40A ($40\,\text{cm}$ Main Box, $25\,\text{cm}$ Front-Knoten)
  * 2x Silikon-Profildichtungen für die Koffer-Slide-in-Deckel
  * 2x EPDM/TPU Wanddurchführungs-Tüllen für die Koffer-Vorderwand
  * **1x 1S LiPo Flat-Pack 2.200 mAh** ($68 \times 39 \times 5{,}0\,\text{mm}$) mit Molex Micro-Fit 3.0 Stecker (USV)
  * **1x Taoglas FXP895 LoRa 868 MHz Flex-Antenne** mit U.FL Kabel
  * **1x Taoglas FXP73 2.4/5 GHz Wi-Fi/BLE Flex-Antenne** mit U.FL Kabel
  * 2x Gore ePTFE Druckausgleichs- und Akustik-Membranpads
* [ ] **Vorkonfektionierte Automotive-Kabelbäume:**
  * **1x Deutsch DTM-12 Zentral-Kabelbaum** (12-polig auf 4 Stränge: Pod 1, Pod 2, Front-Node, Heck-Radar sowie 12V Bordnetz-Speisung)
  * **2x HytePro 4-Pin Magnet-Abreißkupplungen (IP67)** mit 4-adrigem Silikon-Flachbandkabel ($V_{\text{BUS}}$, `GND`, `D+`, `D-`)
  * **1x 4-adriges hochflexibles geschirmtes Automotive-Kabel (AWG22/28)** für den Backbone-Zug (Länge ca. $1{,}5\,\text{m}$)
  * **1x Nylon-Einziehfeder (Fish-Tape, Ø 3 mm, Länge 2 m)** zum Durchziehen des Kabels durch den Rahmentunnel
* [ ] **Werkzeuge:**
  * Innensechskantschlüsselsatz (1.5 / 2.0 / 2.5 / 3.0 / 4.0 mm), Torx TX10 / TX25, Gabelschlüssel SW 7 / 8 / 10 mm, Cuttermesser, dielektrisches Silikonfett.

---

## 3. Montage der Baugruppen (Schritt-für-Schritt)

### Schritt 1: Zentralbox (Main Box) montieren
1. **Muttern einlegen:** 4x DIN 934 M3 Edelstahlmuttern von unten in die formschlüssigen Sechskant-Mutterntaschen der Unterwanne ([`main_box_lower_case.stl`](../../hardware/cad/stl/01_main_box/main_box_lower_case.stl)) eindrücken.
2. **Hauptplatine einsetzen:**
   * Fertig bestückte `PCBA 01` (mit ESP32-S31, Qualcomm QCC3084 und USB-PD Engine) auf die Dämpferdome setzen.
   * Platine mit 4x M2.5 $\times 6\,\text{mm}$ Schrauben handfest fixieren.
3. **Kabelstränge vorverlegen & Zwischenboden aufsetzen:**
   * Deutsch DTM-12 Hauptstecker an `PCBA 01` anstecken.
   * U.FL-Koaxialkabel der LoRa-Antenne (`ANT1`, FXP895) und der Wi-Fi-Antenne anstecken.
   * Zwischenboden ([`main_box_mid_tray.stl`](../../hardware/cad/stl/01_main_box/main_box_mid_tray.stl)) aufsetzen. Alle Leitungen gleiten quetschfrei durch die $70 \times 10\,\text{mm}$ Kabelbucht in die obere Kammer.
4. **2.200 mAh LiPo-Akku & schwenkbare Akkubrücke montieren:**
   * Den 2.200 mAh LiPo-Flachakku in die Wanne des Zwischenbodens einlegen und Molex Micro-Fit 3.0 Stecker anstecken.
   * Beide Flexantennen (Taoglas FXP895 LoRa und Taoglas FXP73 2.4 GHz) in die vorgesehenen Antennentaschen der Akkubrücke ([`main_box_battery_bridge.stl`](../../hardware/cad/stl/01_main_box/main_box_battery_bridge.stl)) einkleben.
   * Akkubrücke mit ihren beiden Einhängenocken links einstecken, umlegen und mit dem elastischen Schnapphaken rechts verriegeln. Der Akku sitzt bis $20\,\text{g}$ vibrationsfest.
5. **Gehäusedeckel & Dichtung:**
   * Silikon-Rundschnur (Ø 1,5 mm, $40\,\text{cm}$) dünn mit Silikonfett benetzen und in die umlaufende Deckelnut einlegen.
   * Gehäusedeckel ([`main_box_lid.stl`](../../hardware/cad/stl/01_main_box/main_box_lid.stl)) aufsetzen und mit 4x M3 $\times 40\,\text{mm}$ V4A-Schrauben über Kreuz anziehen. Der Deckel ist zu 100 % kabelfrei.

---

### Schritt 2: Koffer-Pods v10.0 montieren (Slide-in Deckel & Koffer-USB-Lader)
1. **Das v10.0 Pod-Konzept verstehen (100 % servicefreundlich & motorfrei):**
   * Es gibt keine störanfälligen Motorschlitten oder Auswerfer-Servos mehr.
   * Der Pod sitzt dauerhaft geschützt im vorderen Innenbereich des Hartschalenkoffers.
   * Ein **Slide-in Deckel** mit umlaufender Dichtlippe verschließt die Einschuböffnung. Im geschlossenen Zustand verriegelt ein federbelasteter Neodym-Riegelbolzen den Deckel formschlüssig.
   * **Öffnen per FOB:** Zur Entnahme des Kommunikationsmoduls wird der magnetische OMB Smart Keyfob einfach an die Gehäuse-Markierung gehalten. Das Magnetfeld zieht den Riegelbolzen zurück, und der Deckel kann leicht herausgezogen werden.
   * **Zwischendeckel (Dry-Flap):** Direkt hinter dem Außendeckel sitzt eine federbelastete Spritzschutzklappe. Selbst wenn der Kofferdeckel bei Regen geöffnet wird, bleibt die Elektronik absolut trocken.
   * **Integrierter Koffer-USB-Ladeport:** Auf der Innenseite des Pods stellt `PCBA 03` eine spritzwassergeschützte USB-C Buchse (5V/12V PD bis 30W) bereit. Damit können Action-Cams, Helmpolster-Trockner, Powerbanks oder Smartphones während der Fahrt direkt im Koffer geladen werden!
2. **Platinen- & Stecker-Montage:**
   * Platine `PCBA 03` mit 4x M2.5 Schrauben in das Pod-Gehäuse einsetzen.
   * 4-Draht-Zuleitung vom Koffer-Durchführungspunkt an die Klemmleiste / Buchse von `PCBA 03` anstecken (`VBUS`, `GND`, `D+`, `D-`).
   * Intercom-Kabelpeitsche (für Sena SPIDER X Slim, Cardo Packtalk Edge, OMM UCS oder Midland Funk) an den Buchsenleisten von `PCBA 03` anstecken.
3. **Slide-in Deckel & Magnetverriegelung komplettieren:**
   * Den kleinen N52 Neodym-Magneten mit Führungsstift in die Riegeltasche des Deckels einlegen und mit der Rückstellfeder vorspannen.
   * Dichtprofil in die umlaufende Nut des Slide-in Deckels einpassen und mit Silikonfett schmieren. Deckel probehalber einschieben: Er rastet mit einem deutlichen "Klick" ein. Bei Annäherung des Smart Keyfobs federt der Riegel zurück und gibt den Deckel frei.

---

### Schritt 3: Multi-Protokoll Gateway-Inlays anschließen
1. **Sena SPIDER X Slim / 50S (Referenz K2a):**
   * Vorkonfektioniertes Adapterkabel von `PCBA 03` anstecken (Audio In, Audio Out, PTT, 5V Speisung).
   * Sena-Modul in das formschlüssige PA12-Nest einsetzen. Stromversorgung erfolgt direkt über den verlustarmen Onboard-Step-Down von `PCBA 03` (kein separater Akku nötig).
2. **Cardo Packtalk Edge / Pro (Klasse 1d DMC Gen2):**
   * Audio- und Ladekabel an die Cardo Air-Mount Docking-Kabelpeitsche anstecken.
   * Cardo-Einheit in die Halterung einklicken. Dauerladung während des aktiven Betriebs wird über die getrennte `PGND`-Masseleitung brummfrei unterstützt.
3. **OpenMotorMesh (OMM) 2.4 GHz & 446 PMR Module (Klasse 4 / 3b UCS):**
   * Direkt über USB-C Digital-Audio mit nativer digitaler Übertragung an `PCBA 03` angebunden.
   * Maximale Audioqualität ohne analoge Doppelwandlung.
4. **Midland PMR446 Analogfunk:**
   * Anbindung über die galvanisch getrennten Audio-Trafos und Optokoppler-PTT von `PCBA 03`.

---

### Schritt 4: Front-Knoten am Riser & Symmetrische Dual Under-Perch Spiegel-Pods montieren
1. **Front-Knoten Riser-Montage:**
   * Der Front-Knoten (`PCBA 05`) wird im kompakten Gehäuse direkt am Lenker-Riser oder der oberen Gabelbrücke montiert (mittels beiliegender Riser-Klemmschelle).
   * **Vorteil:** Volle Umströmung mit kühlem Fahrtwind ($< 35^\circ\text{C}$), ungestörter Empfang für den u-blox SAM-M10Q GNSS-Empfänger und direkter Zugriff auf das Knowles MEMS Fahrtwind-Mikrofon zur dynamischen Lautstärkenachführung.
2. **Symmetrische Dual Under-Perch Spiegel-Pods montieren (Links & Rechts):**
   * Die linke und rechte Spiegelschraube unter den beiden Lenkerarmaturen kurz lösen.
   * Die beiden ergonomischen Spiegel-Pods ([`under_perch_mirror_pod.stl`](../../hardware/cad/stl/04_front_node/under_perch_mirror_pod.stl)) formschlüssig unter die Spiegelfüße stecken und die Schrauben mit $15\,\text{Nm}$ vorschriftsmäßig festziehen.
   * **Symmetrische Ergonomie & Sicherheitsgewinn:**
     * **Linker Pod:** Taktiler PTT-Taster liegt perfekt am linken Daumen (Intercom-Funk & Sprachassistent); Amber-LED strahlt blendfrei in den linken Rückspiegel (Überholverkehr links).
     * **Rechter Pod:** Taktiler Action-Cam-Tag Taster am rechten Daumen setzt sofortige Highlights/Bookmarks im Video; Amber-LED strahlt in den rechten Rückspiegel (Verkehr rechts beim Einscheren).
     * **Bilateral:** Echte 360° Totwinkel-Überwachung direkt im peripheren Blickfeld des jeweils relevanten Spiegels!
   * Die beiden dünnen, mattschwarzen PUR-Kabel werden unauffällig an den OEM-Kabelbäumen entlang nach unten zum Front-Knoten am Riser geführt und an `J_POD_L` bzw. `J_POD_R` angesteckt.

---

## 4. Erstinbetriebnahme, Flashen & Dry-Run (Tisch-Testaufbau)

> [!IMPORTANT]
> **Native USB-DFU & Schreibtisch-Betrieb über USB-C (Kein 12V-Labornetzteil nötig!):**  
> Bei OpenMotorBridge v10.0 entfällt jegliches Hantieren mit externen 12V-Labornetzteilen, Krokodilklemmen oder externen USB-UART-Wandlern:  
> * **Dual-Power Input:** Die Zentralbox kann auf der Werkbank **direkt über ein ganz normales USB-C Smartphone- oder Laptop-Netzteil** (5V 3A oder 9V–20V PD bis 60W) oder eine Powerbank betrieben werden. Der interne USB-PD Sink Controller (CH224K) und das Dual Ideal-Diode OR-ing versorgen die Zentralbox, laden den LiPo-Pufferakku und speisen über den 4-Draht Bus auch die angeschlossenen Koffer-Pods und den Front-Node!
> * **Native USB-DFU:** Der **ESP32-S31** der Zentralbox meldet sich über dasselbe USB-C Kabel direkt als `ESP32-S31 USB JTAG/serial debug unit` am PC/Mac an.
> * Flashen und Konfigurieren erfolgen direkt im Browser über die **OpenMotorBridge Web-PWA (WebSerial API)** oder die ESP-IDF Konsole.

```text
+-------------------------------------------------------------------------------------------------+
                      OPENMOTORBRIDGE v10.0 TISCH-TESTAUFBAU (BENCH-DRY-RUN)
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   [ USB-C NETZTEIL (5V-20V PD) ODER 12V DC LABORNETZTEIL ]                                      |
|        |                                                                                        |
|        | USB-C PD Sink (5V-20V bis 60W) ODER 12V DTM-12 (Dual Ideal-Diode OR-ing)               |
|        v                                                                                        |
|   +---------------+     4-Draht Bus (USB-PD / USB 2.0)     +---------------+                    |
|   |  ZENTRALBOX   |=======================================>|  FRONT-KNOTEN | (Am Riser)         |
|   |  (PCBA 01)    |   (VBUS, GND, D+, D-)                  |  (PCBA 05)    | SAM-M10Q GNSS      |
|   |  ESP32-S31    |                                        +-------+-------+ TMP117 / Knowles   |
|   |  QCC3084 Audio|                                                |                            |
|   |  USB-PD Hub   |                                                v                            |
|   +-------+-------+                                   +-------------------------+               |
|           |                                           | 2x SYMMETRISCHE SPIEGEL-|               |
|           | 4-Draht Bus (USB-PD)                      | PODS (Links PTT /       |               |
|           |                                           | Rechts Cam-Tag & BSD)   |               |
|           |                                           +-------------------------+               |
|           +-------------------------------+                                                     |
|           | Strang 1                      | Strang 2                                            |
|           v                               v                                                     |
|   +---------------+               +---------------+                                             |
|   | KOFFER-POD 1  | (Links)       | KOFFER-POD 2  | (Rechts)                                    |
|   | PCBA 03 Smart |               | PCBA 03 Smart |                                             |
|   | Intercom-Modul|               | Intercom-Modul|                                             |
|   | Koffer-USB-Port               | Koffer-USB-Port                                             |
|   +---------------+               +---------------+                                             |
|                                                                                                 |
|   USB-C DFU-Port an PCBA 01                                                                     |
|        |                                                                                        |
|        v Standard USB-C Kabel (WebSerial / DFU)                                                 |
|   [ LAPTOP / WORKBENCH MIT OMB-PWA ]                                                            |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

### Der geführte 4-Punkte v10.0 Smoke-Test
1. [x] **Stromversorgung, USV & USB-PD (Check 1):** Zentralbox über USB-C Netzteil (oder 12V Labornetzteil) verbinden. Interne 5.0 V und 3.3 V Schienen stabil, USV-LiPo (2.200 mAh) lädt mit 4.18 V. USB-PD Power Negotiation versorgt alle Stränge mit sauberer Spannung.
2. [x] **Koffer-Pods & Intercom-Gateway (Check 2):** Beide Pods melden sich über den USB-2.0-Bus fehlerfrei an. Intercom-Audio (Sena/Cardo/OMM) wird erkannt; PTT-Schaltung reagiert verzögerungsfrei. Integrierter Koffer-USB-Port liefert volle Ladespannung.
3. [x] **Front-Knoten & Cockpit-Bedienung (Check 3):** SAM-M10Q liefert 3D-GNSS-Fix, TMP117 liefert Umgebungstemperatur, Knowles MEMS reagiert auf Schnipsen. Betätigung der linken PTT-Taste schaltet Funk/Intercom, linke Spiegel-LED leuchtet bernsteinfarben auf. Betätigung der rechten Action-Cam Taste setzt einen Highlight-Marker, rechte Spiegel-LED leuchtet bernsteinfarben auf.
4. [x] **LoRa Notfunk & 77 GHz Heck-Radar (Check 4):** SX1262 LoRa 868 MHz Ping-Echo erfolgreich; Wheeltec MR20 Radar meldet Zielerkennung und steuert die 36 Heck-Strobe-LEDs an.

---

## 5. Fahrzeugspezifische Montage & Verkabelung am Motorrad

### 5.1 Montage Harley-Davidson 2024+ CVO Road Glide ST (FLTRXSE / Touring Plattform)

> [!CAUTION]
> **GARANTIE- & LACKSCHUTZ: DIE DREI EISERNEN CVO-REGELN:**  
> 1. **ZERO OUTER FAIRING REMOVAL (Niemals die Sharknose-Außenhaut abnehmen!):**  
>    Bei der 2024+ CVO Road Glide ST sind die Rockford Fosgate Lautsprechergitter und die mittleren Luftführungsschlitze mit extrem bruchgefährdeten Druckclips im lackierten Verkleidungskörper eingerastet. Ein Abhebeln führt fast unweigerlich zu abgebrochenen Haltenasen oder feinen Kratzern im exklusiven Raven Metallic Custom-Lack. **Die Außenverkleidung bleibt für den gesamten OMB-Einbau zu 100 % unangetastet!**  
> 2. **ZERO FUEL TANK LIFTING (Niemals den Benzintank anheben oder abbauen!):**  
>    Der Harley-Davidson Touring-Rahmen besitzt auf der Oberseite des Hauptrohrs einen ab Werk integrierten, offenen Kunststoff-Kabelkanal ("Backbone Wire Caddy"). Dieser ist direkt von unterhalb der Fahrersitzbank zugänglich. Mit einer flexiblen Nylon-Einziehfeder wird das 4-Draht-Kabel in 5 Minuten hindurchgezogen – ohne eine einzige Schraube am Tank zu lösen!  
> 3. **HERMETISCHES HANDSCHUHFACH (Niemals Kabel über Türdichtungen quetschen!):**  
>    Das rechte Handschuhfach wird ausschließlich von *unten* durch die werkseitige Gummitülle angefahren. Die Deckeldichtung bleibt zu 100 % unversehrt und absolut wasserdicht.

#### Schritt 5.1.1: Zentralbox unter der Sitzbank montieren
1. Fahrersitzbank abnehmen (hintere Rändelschraube lösen, Sitz nach hinten abziehen).
2. Die Zentralbox auf der Rahmenbrücke direkt vor/über der Starterbatterie platzieren.
3. Mit 4x M4 Silentblöcken oder hochfestem 3M Dual-Lock Klettband vibrationsfest fixieren.
4. 12V-Stromversorgung: Das Pluskabel (mit 7.5A COTS-Sicherung) an Klemme 30 (Dauerplus) bzw. Klemme 15 (geschaltetes Zündungsplus am OEM-Diagnosestecker) anschließen; Massekabel an den zentralen Rahmenmassepunkt legen.

#### Schritt 5.1.2: 5-Minuten Backbone-Kabelzug (Zero Tank-Demontage)
1. Die vordere Sitzzungen-Halterung am Rahmentunnel lokalisieren. Genau dort beginnt der offene OEM-Kabelkanal unter der Tankmittelkonsole.
2. Die flexible Nylon-Einziehfeder (Fish-Tape, Ø 3 mm) von unter der Sitzbank vorsichtig in den Kanal einschieben und nach vorne führen, bis die Spitze am Lenkkopf austritt.
3. Das 4-adrige geschirmte Automotive-Kabel (AWG22/28, Strang 4) mit Textilband an der Einzugsfederspitze fixieren.
4. Einzugsfeder nach vorne durchziehen. Das Kabel liegt nun perfekt geschützt, unsichtbar und scheuerfrei im originalen Kabelkanal.
5. Das hintere Kabelende am DTM-12 Zentralstecker einpinnen; das vordere Kabelende am Lenkkopf zur oberen Gabelbrücke führen.

#### Schritt 5.1.3: Front-Knoten & Symmetrische Dual Under-Perch Spiegel-Pods
1. **Front-Knoten:** Mit der Halterung formschön an den Lenker-Risern oder der oberen Gabelbrücke verschrauben. Das aus dem Rahmentunnel austretende 4-Draht-Kabel anstecken.
2. **Symmetrische Under-Perch Spiegel-Pods (Links & Rechts):**
   * Die linke und rechte Spiegelschraube unter den Armaturen lösen.
   * Die beiden baugleichen Pods aufstecken und Spiegelschrauben mit je $15\,\text{Nm}$ vorschriftsmäßig festziehen.
   * Die dünnen 3-Draht-Kabel entlang der Armaturenkabelbäume zum Front-Knoten führen und an `J_POD_L` bzw. `J_POD_R` einstecken.
   * **Ergebnis:** Symmetrische Optik am Lenker, linker Daumen bedient PTT, rechter Daumen markiert Action-Cam Highlights, beidseitige bernsteinfarbene Totwinkelwarnung direkt in beiden Rückspiegeln!

#### Schritt 5.1.3b: Symmetrische Cockpit-Displays (Dual Speaker Corner-Pods)
1. **Ergonomisches Grundprinzip (Bagger & Touring):**
   * Das Fahrer-Smartphone lädt wetter- und vibrationsgeschützt im rechten Handschuhfach (Media-Compartment) via USB-PD.
   * Für fahrrelevante Blicke (Glanceable Telemetry) werden zwei kompakte Miniatur-Displays symmetrisch im primären Sichtfeld des Fahrers platziert.
2. **Montageort an den Rockford Fosgate Stage II Lautsprechern:**
   * Die beiden Display-Pods ([`cockpit_speaker_corner_pod.scad`](../../hardware/cad/scad/04_front_node/cockpit_speaker_corner_pod.scad)) clipsen formschlüssig an die **unteren inneren Ecken** der Lautsprechergitter beidseits des 12.3" Skyline OS Displays.
   * **Markenschutz & Ästhetik:** Die oberen Rockford Fosgate Schriftzüge und das Harley-Davidson Bar & Shield Emblem bleiben zu 100 % sichtbar und unberührt. Die Riser-Abdeckung mit der gefrästen "CVO ST"-Plakette bleibt frei.
3. **Unsichtbare Kabelführung (Zero Fairing Disassembly):**
   * Das Kabel taucht an der unteren Kante direkt in die natürliche Schattenfuge der Lautsprechereinfassung ein und verläuft verdeckt nach unten in den Lenkkopf-/Gabelbrückenbereich zum Front-Node (`PCBA 05`).
   * **0 cm sichtbares Kabel, 0 Schrauben an der Außenverkleidung lösen!**
4. **Funktion:** Der ESP32-S3 auf `PCBA 05` treibt die Displays per SPI/QSPI (links: Heckradar-Abstandsbalken & Totwinkel; rechts: Turn-by-Turn Pfeile, TPMS-Drücke, Intercom-Sprechstatus und Smartphone-Akkustand).

#### Schritt 5.1.4: Handschuhfach 2-Port USB-Hub (CVO ST Infotainment-Bypass)
1. Das rechte Handschuhfach der CVO Road Glide ST öffnen.
2. An der Unterseite des Handschuhfachs befindet sich die originale Harley-Gummitülle für Zubehörverkabelung.
3. Das USB-Verbindungskabel vom Front-Knoten (oder der OEM-Headunit) von *unten* durch die Tülle nach oben in das Fach führen.
4. Den kompakten OMB 2-Port USB-Hub anstecken und im Fach mit Klett fixieren:
   * **Port 1:** Nimmt den Wireless CarPlay Dongle (z.B. Ottocast U2-Air / Carlinkit 5.0) auf. Die Stromversorgung ist absolut stabil (kein Abstürzen der 12.3" Skyline OS Headunit durch Spannungsabfall!).
   * **Port 2:** Steht frei zum Laden des Fahrer-Smartphones oder für USB-Musiksticks zur Verfügung.
5. Die Handschuhfachtür schließt hermetisch dicht – kein Kabel wird über die weiche Dichtlippe gequetscht!

#### Schritt 5.1.5: Koffer-Pods & 100 % Zero-Drill Kofferwand-Durchführung (OEM Ø 19 mm)
1. **Magnet-Abreißkupplung am Rahmenrohr:**
   * Die 2-Pin/4-Pin HytePro Magnet-Pogo Buchse (`cots_pogo_magnetic_2pin`, IP68) mit Klemmschelle am hinteren Rahmenrohr unter dem Sitzbanküberhang befestigen.
2. **100 % Zero-Drill Kofferwand-Durchführung (OEM Ø 19,0 mm Bohrung):**
   * **Kein Bohren im Koffer:** Weder Kofferboden noch Kofferwände werden angebohrt (absolutes Tabu bei CVO ST).
   * Die vordere OEM-Kofferverschraubung (silberner Spannhebel & Unterlegscheibe) lösen und die werkseitige OEM-Vollgummitülle nach innen herausdrücken. Die freiliegende ABS-Bohrung der Kofferwanne besitzt einen Durchmesser von **$\varnothing 19{,}0\,\text{mm}$**.
   * **Stecker-Durchführung ohne Werkzeug:** Das fertig konfektionierte OMB-Kabel samt Stecker (USB-C / JST-GH, Außenmaß max. $\approx 12 \times 7\,\text{mm}$) wird berührungsfrei durch das freie $\varnothing 19\,\text{mm}$ Loch in den Koffer geschoben (kein Auspinnen, kein Zerschneiden, kein Löten!).
   * **Geteilte TPU-Dichtung einsetzen:** Die zweischalige EPDM/TPU-Dichtung ([`010_saddlebag_hole_grommet_split.scad`](../../hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad), Halbschale A & B) von beiden Seiten um das Kabel und die OEM-M8-Stahlhülse legen und formschlüssig in die $\varnothing 19\,\text{mm}$ Bohrung einpressen (IP67).
   * **U-förmige Tunnel-Distanzscheibe aufschieben:** Die C-förmig geschlitzte 4 mm PA12-CF/Alu Distanzscheibe seitlich über das Kabel unter die OEM-$\varnothing 25\,\text{mm}$-Stahlscheibe schieben.
   * **OEM-Spannhebel festziehen:** Der OEM-Spannhebel wird eingedreht. Die $\varnothing 25\,\text{mm}$ OEM-Stahlscheibe liegt plan auf der Distanzscheibe auf; der Anzugsdruck wird zu 100 % metallisch auf die Stahlhülse übertragen. Das Kabel läuft völlig druck- und klemmfrei durch den 4 mm hohen Tunnel an der Innenwand nach oben. Der Hebel dreht beim Festspannen 360° frei über dem Kabelausgang!
3. **Koffer-Pod montieren:**
   * Pod-Gehäuse im Kofferinneren (vorzugsweise im Kofferdeckel via [`saddlebag_lid_dock.scad`](../../hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad) an den Scharnierschrauben) montieren.
   * 4-Draht-Kabel an `PCBA 03` anstecken.
   * Intercom-Modul einsetzen und Slide-in Deckel einschieben, bis er magnetisch verriegelt.
4. **Bedienung im Alltag (100 % Breakaway):** Beim Abnehmen der Koffer (z. B. für Hotel, Reifenwechsel, Wäsche) werden **nur die beiden OEM-Spannhebel gelöst** und der Koffer angehoben. Die externe Magnetkupplung am Rahmen trennt sich bei $10\dots 15\,\text{N}$ völlig selbsttätig und zerstörungsfrei ("MagSafe-Prinzip"). Im Kofferinneren wird kein Stecker berührt! Beim Wiederaufsetzen zieht sich die Kupplung magnetisch zentriert zusammen.

#### Schritt 5.1.6: 77 GHz Heck-Radar am Kennzeichenträger
1. Das MR20 Radar-Gehäuse an den Kennzeichenträger montieren.
2. Das 4-adrige Kabel von Strang 3 am Heckrahmen entlang nach unten führen.
3. Unbedingt eine **Abtropfschlaufe (Drip-Loop)** von $30\,\text{mm}$ Radius vor dem Eintritt in die M8-Kabelverschraubung vorsehen, damit ablaufendes Regenwasser abtropfen kann und nicht an der Verschraubung ansteht.
4. Den monolithischen Schmutzfänger (Roost-Deflector) ausrichten, um aufgewirbelte Steinchen vom Hinterrad abzuleiten.

---

### 5.2 Montage Adventure-Plattform (BMW R 1200 / 1250 / 1300 GS & GSA)

> [!IMPORTANT]
> **KABELFÜHRUNG BEI DER GS/GSA (Die Realität im Vergleich zur Harley):**  
> Die v10.0 Bus-Architektur (4-Draht Automotive USB-PD) funktioniert auf einer Reiseenduro exakt genauso zuverlässig wie auf der Harley. **Der entscheidende mechanische Unterschied ist jedoch die Verlegung des Verbindungskabels:**  
> Während die Harley Touring einen offenen, geraden Rahmentunnel besitzt (durch den ein Kabel in 5 Minuten per Nylon-Einzugsfeder geschoben werden kann), besitzt die BMW GS einen voluminösen 20-Liter- (bzw. 30-Liter bei der GSA) Tank, geschachtelte Seitenverkleidungen und vor allem die **BMW Telelever-Vorderradführung (Längslenker)**:  
> * **Achtung vor Blindverlegung:** Ein blind oder lose eingezogenes Kabel kann sich bei starkem Einfedern im Telelever-Dreieck verfangen oder beim Lenkanschlag schlagartig auf Zug geraten und abscheren.  
> * **Die saubere Praxis-Verlegung (ca. 20–25 Minuten):**  
>   1. Die linke oder rechte obere Tankseitenblende mit 3–4 Schrauben (Torx T25) lösen und leicht anheben.  
>   2. Das 4-adrige geschirmte Automotive-Kabel (`VBUS`, `GND`, `D+`, `D-`) von der Zentralbox (unter der Sitzbank) parallel zum werksseitigen BMW-Hauptkabelbaum an den oberen Rahmenrohren entlang nach vorne führen und mit UV-stabilen Kabelbindern locker fixieren.  
>   3. **Der Telelever-Bogen am Lenkkopf:** Das Kabel muss am Steuerkopf **exakt der natürlichen Biegung der originalen Bremsleitungen und Kabelstränge** folgen! Eine großzügige Bewegungsschlaufe vorsehen und vor dem finalen Festziehen der Kabelbinder die Gabel mehrmals von vollem Links- bis vollem Rechtsanschlag drehen sowie die Front einmal tief einfedern: Es darf in keiner Position Zugspannung oder Scheuerung an scharfen Kanten entstehen.  
>   4. Das Kabelende an die Ø 12 mm Navigationsstrebe über dem TFT führen und am Front-Node anstecken.

* **Zentralbox:** Im Rahmendreieck oder Werkzeugfach unter der Fahrersitzbank auf 4x M4 Silentblöcken montieren.
* **Front-Knoten:** Direkt an der Ø 12 mm GPS-Querstrebe über dem 6.5" TFT-Display mit der 2-teiligen Klemmschelle fixieren. Liefert Kaltluft-Sensorik, ungestörten GNSS-Empfang und Strom für Navigationsgeräte / Smartphones (QuadLock / SP Connect).
* **All-in-One Under-Perch Spiegel-Pod:** An der linken Spiegelaufnahme montieren (Daumen-PTT + bernsteinfarbene BSD-Radar-Warn-LED).
* **12V-Stromversorgung:** Mit dem vorkonfektionierten **BMW Cartool-Adapterkabel** direkt in den originalen 3-Pin Cartool-Zubehörstecker über dem Lenkkopf einstecken. Liefert sauberes Zündungsplus (KL15) mit automatischer ZFE/BCO-Abschaltung nach 60 Sekunden (kein Entladen der Starterbatterie, keine CAN-Fehlereinträge).
* **Koffer-Pods:** Strikt **fahrzeugfest** am Motorrad montieren – entweder am Rohr-Kofferträger über das geschützte [GSA Cage Dock](../../hardware/cad/scad/02_pod_base/adventure_gsa_cage_dock.scad) im 45 mm Totraum zwischen Alukoffer und Radkasten oder in der Sitzbank-Bügelfalte über das [Transition Dock](../../hardware/cad/scad/02_pod_base/adventure_transition_dock.scad). *(Wichtig: Pods niemals im Inneren von Aluminiumkoffern montieren, da Aluminium 2,4-GHz-Signale wie ein Faradayscher Käfig abschirmt!).*
* **Heck-Radar:** Über den minimalen [Adventure Rack Radar Mount](../../hardware/cad/scad/02_pod_base/adventure_rack_radar_mount.scad) direkt an das hintere Ø 18 mm Rohr der Gepäckbrücke klemmen. Der $45^\circ$-Abweiserkeil schützt vor Steinschlag grobstolliger Enduroreifen; Topcases bleiben dank Montage von unten voll zugänglich und per Schnellverschluss abnehmbar.

---

### 5.3 Begleitfahrzeug- & Autokolonnen-Installation (Support-Car / Van / Wohnmobil)

> [!TIP]
> **DIE v10.0 REVOLUTION IM BEGLEITFAHRZEUG: ZENTRALBOX & FRONT-NODE WIEDER VEREINT!**  
> In den früheren Generationen (v8.0/v9.0) mussten Zentralbox und Front-Node im Auto zwingend getrennt werden (Fahrersitz vs. Beifahrersitz), um extreme Nahfeld-Kopplung und De-Sensing der beiden 6.5-GHz-UWB-Antennen zu verhindern.  
> **Mit dem vollständigen Entfall von UWB in v10.0 gibt es keinerlei Funkkonflikt mehr:**  
> Im Begleitfahrzeug können **Zentralbox (`PCBA 01`) und Front-Node (`PCBA 05`) ab sofort wieder direkt zusammen montiert werden** (als kompakte, gestackte oder nebeneinander montierte „All-in-One Car Support Core Unit“)!

```
                v10.0 ALL-IN-ONE CAR SUPPORT TOPOLOGIE (10-MINUTEN-SETUP)
+-----------------------------------------------------------------------------------------+
| WINDSCHUTZSCHEIBE / A-SÄULE:                   SONNENBLENDEN:                           |
| [ SAM-M10Q GNSS-Puck an Scheibenbasis ]        [ Pod 1 (Fahrer) & Pod 2 (Beifahrer) ]   |
| (Im unbedampften Mautbox-Scheibenfenster)      (2.4 GHz strahlt frei durch Frontscheibe)|
+-----------------------------------------------------------------------------------------+
       ^                                                        ^
       | Dünnes I2C-Sensorkabel                                 | 2x 4-Draht USB-PD Zuleitungen
+---------------------------------------------------------------+-------------------------+
| ZENTRALE "CAR SUPPORT CORE UNIT" (Kompakt unter Beifahrersitz oder Mittelkonsole):       |
| +------------------------------------+     +------------------------------------------+ |
| |        FRONT-NODE (PCBA 05)        |<===>|           ZENTRALBOX (PCBA 01)           | |
| | * 4-Port USB-Hub für Infotainment  | 10cm| * ESP32-S31 AI-Host & QCC3084 Audio-SoC  | |
| | * 20W USB-PD Lade-Bypass Ottocast  | Bus | * SX1262 LoRa Notfunk & Diebstahl-Sentry | |
| +------------------------------------+     +--------------------+---------------------+ |
+-----------------------------------------------------------------|-----------------------+
       |                                                          |
       | USB-Kabel & PTT                                          | Koaxialkabel (RG-174)
       v                                                          v
+--------------------------------------+      +-------------------------------------------+
| MITTELKONSOLE (Bedienbereich):       |      | EXTERNE 868-MHz-MAGNETFUSS-DACHANTENNE:   |
| * OEM Media-USB (Nur Daten D+/D-)    |      | * Haftet kratzfrei auf dem Autodach       |
| * AAWireless/Ottocast an OMB (5V/3A) |      | * Dach als HF-Groundplane liefert         |
| * PTT-Taster an Schalthebel/Handbremse|      |   15–25 km echte LoRa-Reichweite zur Gruppe|
+--------------------------------------+      +-------------------------------------------+
```

1. **Platzierung der vereinten Core Unit:**
   * Zentralbox und Front-Node werden als Doppel-Einheit im thermisch kühlen Fußraum unter dem Beifahrersitz oder im Mitteltunnel platziert.
   * **Stromversorgung mit nur EINEM Kabel:** Ein einziges 12V-Automotive-Kabel führt zur 12V-Zigarettenanzünderdose (Fond oder Mittelkonsole) – kein Y-Kabel-Wirrwarr quer durch den Fahrzeuginnenraum mehr nötig!
2. **Kabelausgänge der vereinten Einheit:**
   * **Nach oben zum Dach:** Ein $2{,}5\,\text{m}$ langes RG-174 Koaxialkabel führt unter dem Teppich nach hinten durch die Heckklappendichtung zur externen $\varnothing 30\,\text{mm}$ Magnetfuß-Dachantenne. Garantiert $15\dots 25\,\text{km}$ LoRa-Reichweite zur Motorradgruppe über Berge hinweg (überwindet die Faradaysche Dämpfung der Blechkarosserie).
   * **Zur Frontscheibe:** Ein dünnes 4-adriges Sensorkabel führt zur Scheibenbasis (Mautbox-Fenster) zum SAM-M10Q GNSS-Puck.
   * **Zu den Sonnenblenden:** Zwei 4-adrige Flachbandkabel führen verdeckt entlang der A-Säulen-Dichtungen zu Pod 1 (Fahrer: Sena/OMM) und Pod 2 (Beifahrer: Cardo/Midland).
   * **Zur Mittelkonsole (AAWireless Clean Power-Injection):**
     * Der AAWireless- oder Ottocast-Adapter wird direkt an den $5\,\text{V}\,/\,3\,\text{A}$ ($15\,\text{W}$) USB-Port von OpenMotorBridge eingesteckt.
     * Ein reines High-Speed Datenkabel (`D+`, `D-`, `GND` mit isoliertem `VBUS`) führt in den OEM-Media-USB-Port des Autos.
     * **Effekt:** Das Auto-Radio empfängt sofort stabiles Android Auto / Apple CarPlay ohne die berüchtigten Bootloops, die durch die schwachen $500\,\text{mA}$-Werksbuchsen entstehen!
     * Der PTT-Taster wird mit Klett am Schalthebel oder an der Handbremse befestigt.
3. **Mietwagen- & Rallye-Tauglichkeit:** Das gesamte Setup ist in weniger als 10 Minuten in jedem beliebigen Begleitfahrzeug einsatzbereit und hinterlässt beim Ausbau null Montagespuren.

---

## 6. Endabnahme, Probefahrt & Sign-Off Checkliste

1. **Zündungs-Check (KL15):**
   * Zündung EIN: Zentralbox und Front-Node erwachen synchron in $< 500\,\text{ms}$.
   * USB-PD Schienen stabil; grüne Status-LED an `PCBA 01` leuchtet permanent.
   * Spiegel-LEDs quittieren für 1,0 s (Amber Selbsttest).
2. **Koffer-Pods & Ladefunktion:**
   * Slide-in Deckel mit Smart-Keyfob entriegeln und prüfen: Schnappt weich ein und aus.
   * Smartphone / Action-Cam an den Koffer-USB-Port anstecken: Lädt zuverlässig mit vollem PD-Ladestrom.
   * Intercom-Kommunikation prüfen: Audio wird verlustfrei und brummfrei über das Headset übertragen.
3. **Totwinkel-Radar Test:**
   * Eine Person nähert sich von hinten dem stehenden Motorrad: Die Amber-LED am linken Under-Perch Spiegel-Pod leuchtet ab 25 m Entfernung kontinuierlich auf.
   * Linken Blinker setzen, während sich die Person im Erfassungsbereich befindet: Warn-LED blitzt mit 8 Hz Rot/Amber; Heck-Radar Strobe-LEDs warnen nach hinten.
4. **Infotainment & Headunit (CVO Road Glide ST):**
   * 12.3" Skyline OS Display verbindet sich binnen 15 Sekunden drahtlos mit Apple CarPlay / Android Auto über den Dongle im Handschuhfach.
   * Sprachbedienung über den PTT-Taster am Spiegelfuß startet die Siri / Google Assistant Navigation ohne Fehltrigger.
5. **Probefahrt & Dynamik:**
   * Knowles Fahrtwind-Mikrofon regelt die Lautstärke des Helmsystems bei steigender Geschwindigkeit harmonisch nach.
   * Raised-Cosine Ducking senkt Musik bei Funksprüchen weich um $-18\,\text{dB}$ ab.
6. **Zündung AUS:**
   * Zündung ausschalten: Zentralbox meldet sauberen Shutdown; USV sichert alle Logdaten.
   * Diebstahl-Sentry auf LoRa 868 MHz bleibt im Ultra-Low-Power-Modus 24/7 aktiv.
