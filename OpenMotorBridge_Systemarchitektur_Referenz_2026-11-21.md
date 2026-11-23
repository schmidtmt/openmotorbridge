# OpenMotorBridge - Systemarchitektur & Hardware-Referenz (Offsite-Dokument)

**Stand:** 21. November 2026  
**Status:** Verbindliche Systemreferenz für die Umsetzung (Tabula-Rasa Konsens)  
**Geltungsbereich:** Zentralbox (`PCBA 01`), Koffer-Pods (`PCBA 03`), Front Node (`PCBA 05`), Radar/Heck-Node (`PCBA 08`)

---

## 1. Leitprinzipien & Grundphilosophie

1. **Keine Hacks, keine Phantom-Chips:**
   Das System verlässt sich nicht auf reverse-engineerte DRM-Workarounds, emulierte Headset-Dongles oder instabile USB-OTG-Experimente. Jede Schnittstelle wird standardkonform und physikalisch sauber ausgeführt.
2. **Das Helm-Dogma: Ein Helm = 1 einzige Bluetooth-Verbindung:**
   Motorrad-Headsets (Sena, Cardo, etc.) scheitern in der Praxis reproduzierbar, wenn sie parallel zum Motorrad noch eine zweite Verbindung (z. B. Helm-zu-Helm-Intercom) verwalten müssen (Verbindungsabrisse, Prioritäts-Kollisionen bei Navi-Ansagen).
   * **Die Regel:** Jeder Helm koppelt sich **ausschließlich mit OpenMotorBridge**.
   * Die Zentralbox übernimmt das gesamte Mischen, Ducking und das private Gegensprechen zwischen Fahrer und Sozius.
3. **Bewusster Entfall von Android Auto & Apple CarPlay (Fokus Universal Cockpit):**
   * Kein Video-Streaming (H.264/H.265) und kein komplexer Host-Stack: Verhindert Hitzeprobleme im geschlossenen Handschuhfach beim gleichzeitigen induktiven Qi-Laden.
   * Eliminierung von Puffer-Latenzen und Verbindungsabbrüchen.
   * Volle Konzentration auf das native Cockpit: Fahrdynamik, Sensorik, Reifendruck, optische Radar-Warnung, Turn-by-Turn-Pfeile via BLE sowie native Audiosteuerung (AVRCP/A2DP) und Telefonie (HFP 1.8 mit Mikrofon-Rückkanal).
4. **Klare Zonierung des Fahrzeugs:**
   HF-Sender werden räumlich entkoppelt und dort platziert, wo sich ihre Gegenstellen befinden (Cockpit vorne, Helme/Smartphone Mitte, Koffer/Radar hinten).

---

## 2. Die 4 physischen Funktionszonen

```
=============================================================================================
                               GESAMTSYSTEM-TOPOLOGIE
=============================================================================================

[ZONE 1: COCKPIT / FRONT (PCBA 05)]
* Koppelt SkylineOS (Harley) / BMW Navigator (GS) per Bluetooth (15 cm Luftlinie)
* Steuert den "Cruise Mode" (Musik auf Verkleidungslautsprecher via Profil-Aushandlung)
* Natives Universal Cockpit (Sensordaten, Fahrdynamik, Radar-Warn-LEDs/Grafik; bewusst OHNE CarPlay/Android Auto)
* 20W DC-Versorgung für magnetischen Qi-Lade-Puck (Handschuhfach) mit Zusatz-Lademöglichkeit (USB-C PD)
                                  |
                                  | Geschirmter 4-Ader Automotive-Bus
                                  | (VBUS, GND, CAN_H, CAN_L bzw. USB @ 480 Mbps, < 0.2 ms Latenz)
                                  v
[ZONE 2: MITTE / UNTER DER SITZBANK (PCBA 01 - ZENTRALBOX)]
* 2× Qualcomm QCC3086: Unabhängige Source-Transceiver für Helm 1 (Fahrer, U13) & Helm 2 (Sozius, U14)
  -> Anbindung: 2× Onboard-Keramikantennen (Johanson 2450AT) an Platinenkanten (50 cm zu Helm)
* 1× Qualcomm QCC3086: Smartphone-Transceiver (U9: A2DP Sink, AVRCP, HFP 1.8 Low-Latency Voice-Rückkanal)
  -> Anbindung: Taoglas FXP73 Flex-Antenne im Deckel (ANT2) für maximale Reichweite zur Jackentasche
* 1× ESP32-S31: Zentraler Audio-DSP (Mischpult, Raised-Cosine Ducking), USB-Host, BLE (ANT3)
* 1× Semtech SX1262: LoRa 868 MHz Diebstahlschutz/Beacon & Keyfob Pager an Taoglas FXP895 im Deckel (ANT1)
* USV & Thermik: 2.200 mAh LiPo-Puffer; alle 10 Konvektionsschlitze zum Gore-Vent bleiben 100% frei
                                  |
         +------------------------+------------------------+
         | 4-Ader Bus                                      | 4-Ader Bus (OPTIONAL)
         v                                                 v
[ZONE 3: SATTELTASCHEN / KOFFER (PCBA 03)]     [ZONE 4: HECK (PCBA 08 - RADAR-NODE)]
* Autarkes Mesh-Gateway (Sena <-> Cardo)        * REIN OPTIONALES UPGRADE-MODUL
* Mechatronik (KL15, Cradles, Pogo-Pins)        * Mittig auf Fahrzeugachse, metallfrei gedämpft
  bleibt 1:1 in allen Stufen identisch!         * 24/77 GHz Radar-Sensorik & V2X-Warnungen
* Stufe 1 (Basis ohne Radar): Kabelgebunden     * Stufe 2 (Upgrade): Beherbergt 2x QCC3086
  (ES8388 AD/DA-Wandler für Mic/Speaker, OMM USB) * Drahtlose BT-Anbindung zu Pods L/R
* Stufe 2 (Upgrade mit Radar): Drahtlos via BT  * Ermöglicht Hi-Fi Music-Sharing in Mesh-Gruppe
  (ES8388 AD/DA-Wandler werden Cold Standby)      (Pod-AD/DA-Wandler gehen in Cold Standby)
=============================================================================================
```

---

## 3. Detaillierte Zonen-Spezifikation

### 3.1 Zone 1: Cockpit / Front Node (`PCBA 05`)
* **Lage:** Kanzel / hinter Verkleidung / unter Windschild.
* **Bluetooth-Kanal (Infotainment- & Bike-Bridge):**
  * **Hardware:** Feasycom FSC-BT802 (Qualcomm CSR8670, aptX Low Latency, I2S + UART) am ESP32-S31 Node-Controller.
  * **Harley SkylineOS / Boom! Box GTS:**
    * Meldet sich als Standard-Bluetooth-Headset an.
    * **Cruise Mode:** Deaktiviert das A2DP-Sink-Profil. SkylineOS schaltet die Audioausgabe automatisch auf die Verkleidungslautsprecher um.
    * **Solo-Modus / Intercom:** Audio wird über den Systembus zur Zentralbox gestreamt.
  * **BMW GS / GSA (Navigator VI / ConnectedRide TFT):**
    * Verbindet sich per Bluetooth mit dem Navigator/TFT.
    * Fängt Sprachansagen ab und schickt sie mit Priorität 2 nach hinten.
* **Ausbau von Android Auto & Apple CarPlay:**
  * Bewusster Entfall jeglicher Display-Spiegelung / Videostreaming-Stacks.
  * Verhindert thermische Überlastung des Smartphones im geschlossenen Handschuhfach bei Sonneneinstrahlung und induktiver Ladung.
  * Das Cockpit dient als robustes, blendfreies Dashboard für native Fahrzeug-Telemetrie, Reifendruck, Radar-Gefahrenzonen, Lenkertastenbedienung und BLE-Pfeilnavigation.
* **Handschuhfach & Stromversorgung:**
  * Der historische USB-Hub (`PCBA 05B`) entfällt ersatzlos.
  * Ersatz durch einen **magnetischen Qi-Ladepuck (15W/20W MagSafe/Qi2)** mit integrierter **Zusatz-Lademöglichkeit (USB-C PD)** für Zubehör (z. B. Dashcam, Action-Cam oder Zweitgerät).
  * Gespeist über eine reine 2-adrige DC-Leitung (keine USB-Datenleitung ins Handschuhfach, keine EMV-Einkopplung).

---

### 3.2 Zone 2: Zentralbox (`PCBA 01` unter der Sitzbank)
* **Lage:** Auf der Batteriebrücke unter der Sitzbank (IP67, $110 \times 74 \times 38\,\text{mm}$).
* **Bluetooth-Architektur (Triple-QCC3086 Gleichteil-Design):**

| Chip-Referenz | Chip-Typ | Funktion | Bluetooth-Rolle | Antennen-Typ & Platzierung |
| :--- | :--- | :--- | :--- | :--- |
| **`U9`** | **Qualcomm QCC3086** | Smartphone Link | Sink (A2DP Musik) + HFP 1.8 Low-Latency Voice-Rückkanal | **Taoglas FXP73 Flex im Deckel (`ANT2`)** |
| **`U13`** | **Qualcomm QCC3086** | Helm 1 (Fahrer) | Source (A2DP Audio) + Low-Latency Mic In | Onboard Keramik (Johanson 2450AT, Nordost-Kante) |
| **`U14`** | **Qualcomm QCC3086** | Helm 2 (Sozius) | Source (A2DP Audio) + Low-Latency Mic In | Onboard Keramik (Johanson 2450AT, Südost-Kante) |
| **`U2`** | **ESP32-S31** | System-MCU, DSP, BLE | BLE (Dashboard, App-Telemetrie) | Onboard Keramik (`ANT3`, West-Kante) |
| **`U10`** | **Semtech SX1262** | LoRa 868 MHz Sentry | LoRa P2P Beacon & Keyfob Pager | **Taoglas FXP895 Flex im Deckel (`ANT1`)** |

* **Antennen- und Gehäuse-Thermik:**
  * Im Deckel befinden sich **nur zwei Antennen**: `ANT1` (LoRa $85 \times 18\,\text{mm}$) und `ANT2` (Smartphone $47 \times 7\,\text{mm}$).
  * **Die 10 Konvektionsschlitze bei $Y = 58\,\text{mm}$ bleiben vollständig frei.** Die Abwärme der Schaltregler (`LM5164`, `BQ24075`, `TPS4H160`) entweicht ungehindert zur Gore-Tex ePTFE-Membran.
  * Der 2.200 mAh LiPo-Akku bleibt thermisch geschützt und liegt nicht auf HF-Leitungen.
* **Link-Budget der Helme:**
  * Bei 50–70 cm Distanz durch Schaumstoff/Leder reicht die Onboard-Keramikantenne (+10 dBm TX, -95 dBm RX-Sensitivität) für ein Signal von $\approx -27\,\text{dBm}$ mit über 55 dB Signalreserve.
* **Smartphone-Verbindung (`U9`):**
  * Erhält die hocheffiziente Deckelantenne (`ANT2`), um Körperschattierung (Lederjacke, Rucksack) und Distanz (Tankstelle, Laufen ums Bike) mit maximalem Link-Budget abzufangen.
  * Unterstützt volles Freisprechen via HFP 1.8: Eingehende Anrufe können ohne Anhalten oder Handschuhausziehen direkt per Lenkertaster und Helm-Mikrofon beantwortet werden.

---

### 3.3 Zone 3: Koffer-Pods (`PCBA 03` in Seitentaschen)
* **Lage:** In den Seitenkoffern / Packtaschen.
* **Verbindung:** Über geschirmten 4-Ader-Bus (Stränge 2 & 3).
* **Mechatronik (1:1 unverändert in allen Stufen):**
  * Startimpuls erfolgt bei Zündung-EIN (KL15) über einen definierten Bestromungsimpuls auf den Taster/Magneten.
  * Cradles, Stecker und mechanische Passung bleiben 100 % identisch, unabhängig davon, ob das System mit oder ohne Radar betrieben wird.
* **Dual-Modus Betriebsstrategie:**
  * **Stufe 1 (Basis ohne Radar): Kabelgebundener Betrieb**
    * Sprache und Audio aus dem Sena/Cardo-Mesh werden über die Onboard-`ES8388`-Codecs (analoge AD/DA-Wandlung mit Kelvin-Masse) verarbeitet.
    * OMM (OpenMotorMesh) Datenanbindung läuft stabil über USB.
    * Latenz: $< 0{,}2\,\text{ms}$, 100 % autark, absolut störungsfrei.
  * **Stufe 2 (Upgrade mit Radar-Node PCBA 08): Drahtlose Bluetooth-Anbindung**
    * Die 2× QCC3086 des Radar-Nodes übernehmen die Audio-Strecke zu den Pods per Bluetooth.
    * Ermöglicht Hi-Fi Music-Sharing in die gesamte externe Mesh-Gruppe.
    * Die analogen `ES8388` AD/DA-Wandler auf PCBA 03 gehen in den **Cold Standby** (stehen als redundanter Fallback jederzeit bereit).

---

### 3.4 Zone 4: Heck / Radar Node (`PCBA 08`) – MODULARES UPGRADE
* **Lage:** Symmetrisch auf der Fahrzeug-Längsachse (Kennzeichenaufnahme / Rücklichtbereich).
* **Modularer Status:** **100 % OPTIONAL.** Das Gesamtsystem (Stufe 1) ist ohne Einschränkung der Cockpit-, Helm- oder Telefonie-Funktionen voll betriebsfähig.
* **Doppelfunktion bei Verbau (Stufe 2):**
  1. **Sensorik & Sicherheit:** 24 GHz / 77 GHz Radarsensorik für Totwinkel- und Abstandsüberwachung. Sendet Zieldaten digital per CAN/USB an die Zentralbox für das akustische Radar-Ducking (-18 dB Chime) und optische Dashboard-Warnungen.
  2. **High-End Audio-Upgrade & Music-Sharing:** Beherbergt 2× Qualcomm QCC3086 (`U4`, `U5`), die als drahtlose Nahfeld-Transmitter (30 cm Funkstrecke) zu den Koffer-Pods L & R fungieren und synchrones Hi-Fi-Musik-Sharing in die Gruppenkommunikation ermöglichen.
* **Mechanik:**
  * 100 % metallfreie Schwingungsentkopplung (Silikon-/EPDM-Grommets).
  * Absolutes Metall-Verbot im Nahfeld der Radar- und V2X-Antennen.

---

## 4. Das 2-Stufen-Modularitätsmodell (Graceful Degradation)

Um dem Anspruch von puristischen Custom Bikes (kein Kasten am Heck) bis zur vollausgestatteten Reiseenduro/Tourer gerecht zu werden, arbeitet das System in zwei klaren Stufen:

```
+-----------------------------------------------------------------------------------------+
| STUFE 1: BASIS-SYSTEM (100 % Clean Rear, OHNE Radar-Knoten)                             |
| * Geeignet für: Puristische Custom Bikes, Chopper, Bobber (z. B. seitlicher KZH)         |
| * Zentralbox (PCBA 01) + Front Node (PCBA 05) + Koffer-Pods (PCBA 03)                   |
| * Triple-QCC3086 auf PCBA 01:                                                           |
|   - Fahrer- & Sozius-Helme: VOLLDUAL AKTIV (U13, U14)                                   |
|   - Smartphone Streaming & Telefonie-Freisprechen: VOLL AKTIV (U9 HFP 1.8 Rückkanal)    |
| * Handschuhfach: Magnetischer Qi-Ladepuck (15W/20W) + USB-C PD Zusatz-Ladeport           |
| * Koffer-Pods (PCBA 03): 100 % kabelgebundene AD/DA-Wandlung für Mic & Speaker (ES8388) |
|   OMM-Daten über USB. Mechatronik (KL15-Impuls) 1:1 aktiv.                              |
| * Einschränkung: Kein Totwinkel-Radar, kein drahtloses BT-Music-Sharing in externe Mesh  |
+-----------------------------------------------------------------------------------------+
                                           |
                                           | Upgrade durch Hinzufügen von PCBA 08 am Heck
                                           v
+-----------------------------------------------------------------------------------------+
| STUFE 2: EXPANDED SYSTEM (MIT Radar-Node PCBA 08 am Heck)                                |
| * Geeignet für: Tourenmaschinen, Adventure-Bikes (BMW GS/GSA, Harley Touring)           |
| * Alle Funktionen aus Stufe 1 bleiben zu 100 % erhalten                                 |
| * Totwinkel-Radar & V2X-Gefahrenwarnungen (akustisch im Helm & optisch auf Display)     |
| * AUDIO-UPGRADE & MUSIC-SHARING:                                                        |
|   2x QCC3086 auf PCBA 08 übernehmen die Audio-Strecke zu den Pods drahtlos via BT.      |
|   Synchronisiertes Hi-Fi Music-Sharing in die gesamte Sena/Cardo-Gruppe!                |
| * Pod-AD/DA-Wandler (ES8388) gehen in den Cold Standby (Redundanz). Mechatronik bleibt.  |
+-----------------------------------------------------------------------------------------+
```

---

## 5. Audio-Routing & DSP-Prioritäten (ESP32-S31)

Das Audio-Mischpult im ESP32-S31 verarbeitet alle Audioströme mit **Raised-Cosine Ducking** (weiche Übergänge ohne Knacken):

1. **Priorität 1 (Höchste Priorität): Radar- & Crash-Warnungen**
   * Dämpft alle anderen Audioquellen sofort um **-18 dB**.
   * Akustischer Raumklang-Chime direkt auf die Helme.
2. **Priorität 2: Navi-Sprachansagen (SkylineOS / BMW Navigator via Front Node)**
   * Dämpft Musik um **-12 dB**.
   * Sprachansage wird über Fahrer- und Soziushelm gelegt.
3. **Priorität 3: Telefonie & Privates Fahrer-Sozius Intercom**
   * Eingehende Telefonanrufe (Smartphone via QCC3086 `U9`) und Intercom (`U13` / `U14`).
   * Helm-Mikrofone werden gemischt und mit minimaler Latenz (< 20 ms) an Smartphone und Gegenstelle übertragen.
   * Musik wird dezent abgesenkt (-6 dB bzw. Stummschaltung während Anruf).
4. **Priorität 4: Externe Mesh-Gruppe (Sena / Cardo via Pods)**
   * Gruppenfunk wird auf Wunsch zugemischt oder per PTT getastet.
   * Stufe 1: Über analoge Codecs (ES8388).
   * Stufe 2: Über drahtlose QCC3086-Links des Radar-Nodes.
5. **Priorität 5 (Hintergrund): Musik-Streaming (Smartphone via QCC3086 `U9`)**
   * Läuft kontinuierlich im Hintergrund.
   * Im **Cruise Mode** über Front Node auf Verkleidungslautsprecher geroutet.
   * Im Normalmodus synchron auf beide Helme (sowie in Stufe 2 via Radar-Node ins Music-Sharing).

---

## 6. Konkrete Implementierungs-Schritte

### 6.1 Zentralbox (`PCBA 01`)
* **Triple-QCC3086 Architektur umgesetzt:**
  * `U9`: QCC3086 Smartphone Link (A2DP Sink + HFP 1.8 Voice-Rückkanal) an Taoglas FXP73 (`ANT2`).
  * `U13`: QCC3086 Helm 1 (Fahrer) an Keramikantenne 1 (Nordost).
  * `U14`: QCC3086 Helm 2 (Sozius) an Keramikantenne 2 (Südost).
* Identischer WLCSP-99 Footprint (`Qualcomm_QCC3086_Module`), 15 Pins, 0 Leiterbahn-Änderungen.
* KiCad DRC bestätigt: **0 unconnected items, 0 schematic parity issues**.

### 6.2 Front Node (`PCBA 05`)
* FSC-BT802 (Qualcomm CSR8670) für Bike/Infotainment-Bridge platziert.
* Digitale MEMS-Mikrofone (`SPH0645LM4H`) und Lenkertaster-Interfaces integriert.
* Ausbau aller CarPlay/Android-Auto-Relikte.
* Handschuhfach-Versorgung: Reine 2-adrige DC-Speisung für magnetischen Qi-Ladepuck (15W/20W) und USB-C PD Zusatz-Ladeport.

### 6.3 Radar-Knoten (`PCBA 08`)
* Dual QCC3086 (`U4`, `U5`) auf Bottom-Layer für drahtlose Pod-Anbindung L/R platziert und geroutet.
* 4× Aufnahmetaschen für metallfreie Silikon-/EPDM-Dämpfungsgrommets im Cradle vorgesehen.
* Reines modulares Plug & Play Upgrade (Stufe 2).

### 6.4 Archivierung
* `PCBA 05B` (Glovebox Hub) als historisch archiviert.
* Koffer-Pods (`PCBA 03`) Mechatronik und AD/DA-Wandler bleiben unverändert hardware-kompatibel für Stufe 1 & 2.

---

## 7. Smartphone-Schnittstellen, Datenflüsse & Protokolle (SSOT)

Mit der Umstellung auf den Qualcomm QCC3086 (`U9`) und der Bereinigung der Systemarchitektur ist die Schnittstelle zwischen Smartphone und OpenMotorBridge (OMB) verbindlich wie folgt definiert:

### 7.1 Was komplett entfällt (Architektur-Bereinigung)
* **Apple CarPlay & Android Auto Video-Tunneling:**
  * Vollständiger Ausbau. Keine instabilen H.264/H.265-Videostreams über 5 GHz Wi-Fi Direct, keine Dongle-Hacks, keine Display-Spiegelungs-Abstürze.
  * Verhindert zuverlässig die thermische Notabschaltung des Smartphones im geschlossenen Handschuhfach.
* **USB-Datenleitung ins Handschuhfach:**
  * Keine geschirmten USB-Differenzialdatenpaare mehr im Kabelbaum zum Handschuhfach.
  * Vollständiger Wegfall des 5-Port-Hubs (`PCBA 05B`) und der Kaltstart-Reset-Schaltung (`TPS2051B`).

### 7.2 Aktive Kommunikations- & Audio-Kanäle zum Smartphone

| Kanal / Protokoll | Physischer Chip & Antenne | Datenrichtung | Funktion & Spezifikation |
| :--- | :--- | :---: | :--- |
| **Musik-Streaming (A2DP Sink)** | QCC3086 (`U9`) an Taoglas FXP73 (`ANT2`) | Phone ➔ OMB | Hi-Fi Stereo Audio (aptX Adaptive / Lossless, AAC, SBC) mit minimaler Latenz. DSP-Mischung mit Raised-Cosine Ducking (-12 dB bei Navi, -18 dB bei Radar). |
| **Mediensteuerung (AVRCP 1.6)** | QCC3086 (`U9`) UART an ESP32-S31 | Bidirektional | Lenkertaster-Steuerung: Play, Pause, Track Next/Prev. Textuelle Übertragung von Metadaten (Titel, Interpret, Album). |
| **Vollduplex-Telefonie (HFP 1.8)** | QCC3086 (`U9`) an Taoglas FXP73 (`ANT2`) | Bidirektional | **Downlink:** Anruferstimme via I2S in den DSP und auf die Helme.<br>**Uplink (Voice-Rückkanal):** Helmmikrofone (Fahrer `U13`, Sozius `U14`) werden mit < 20 ms Latenz windgeräuschkompensiert ans Telefon übertragen. Freisprechen ohne Anhalten oder Helmabsetzen! |
| **Anrufsteuerung (HFP AT-Cmds)** | QCC3086 (`U9`) UART an ESP32-S31 | OMB ➔ Phone | Anruf annehmen (`ATA`), ablehnen/beenden (`AT+CHUP`), Sprachassistent triggern (Siri / Google Assistant). |
| **Pfeilnavigation (BLE GATT `COMM_48`)** | ESP32-S31 (`U2`) an Onboard Keramik (`ANT3`) | Phone ➔ OMB | Übertragung kompakter Turn-by-Turn Navigationsdaten (Manöver-Icon, Distanz in Metern, Straßenname, Tempolimit, ETA) aus Smartphone-Apps (Kurviger, Calimoto, Google Maps) **für das native/optionale OMB-Cockpit-Display**. |
| **Telemetrie & Companion App** | ESP32-S31 (`U2`) an Onboard Keramik (`ANT3`) | Bidirektional | Live-Übertragung von Schräglage (IMU), Reifendruck & -temperatur (TPMS), Bordspannung, Radar-Objekten sowie Audio-Mixer-Profilen an die OMB-App. |
| **eCall-Unfallnotruf (BLE GATT)** | ESP32-S31 (`U2`) an Onboard Keramik (`ANT3`) | OMB ➔ Phone | Bei schwerem Sturz/Überschlag (IMU-Crash-Erkennung) sendet OMB ein Notfall-Telegramm; Smartphone-App setzt Notruf mit GPS-Koordinaten ab. |
| **SOCKS5-Proxy & Daten-Tethering** | QCC3086 (`U9`, SPP/PAN) oder ESP32-S31 (Wi-Fi) | Bidirektional | Internet-Gateway über Mobilfunk des Smartphones: Backend-Upload von Tourendaten, Wetterabfrage und OTA-Updates. |

### 7.3 Lade-Architektur im Handschuhfach (Echter Fast-Charger)
* **Reine 2-adrige DC-Speisung:** Keine Datenleitungen, keine EMV-Störungen im Handschuhfach.
* **Leistung & Fast-Charging-Regler:**
  * Gespeist über einen automotiven Fast-Charging-Buck-Controller (z. B. SW3526 / MPQ4228) mit bis zu **30–36 W Gesamt-Eingangsleistung**.
  * **Echter Fast-Charger:** Unterstützt USB Power Delivery 3.0 (PD) und QuickCharge 4.0 (5V, 9V, 12V Verhandlung).
* **Magnetischer Qi-Ladepuck (Qi2 / MagSafe kompatibel):**
  * Verhandelt per USB-PD 9V/12V Eingangsspannung.
  * Liefert die **nach WPC-Standard maximal genormten 15 Watt induktive Ladeleistung** an das Smartphone.
  * Aufgrund des induktiven Wirkungsgrads ($\approx 70\,\%$) zieht der Puck 20–22 W auf der DC-Seite.
  * Da kein CarPlay-Videostreaming auf dem Smartphone läuft, bleibt das Gerät im geschlossenen Fach thermisch stabil.
* **Zusatz-Ladeanschluss:**
  * Parallele USB-C PD Buchse im Handschuhfach mit bis zu 20–30 W Fast-Charging für Dashcam, Action-Cam, Powerbank oder Zweitgerät.

---

## 8. Ergonomie-, Navigations- & Display-Realität: GS/GSA vs. Harley-Davidson

In der praktischen Fahrzeug-Integration unterscheiden sich Adventure-Bikes (BMW GS) und Tourer (Harley-Davidson Road Glide / Street Glide) grundlegend. Das System trägt dieser Realität Rechnung:

### 8.1 Werks-Headunits & Navigation (Geschlossene Systeme)
* **Die Realität der OEM-Systeme:**
  * Weder Harley-Davidson (Boom! Box GTS / SkylineOS) noch BMW (ConnectedRide TFT) erlauben das Einspeisen externer Drittanbieter-Pfeile oder Kartengrafiken über offene Schnittstellen.
* **Architektonische Lösung:**
  1. **Werks-Bordnavi (Harley / BMW):**
     * Das Motorrad nutzt seine bordeigene Navigation auf dem Werksbildschirm.
     * Die Sprachansagen werden über den Bluetooth-Chip der Frontnode (`PCBA 05`, FSC-BT802) digital abgegriffen und im Zentralbox-DSP mit -12 dB Musik-Ducking glasklar in die Helme eingespielt.
  2. **Smartphone-Navigation (Kurviger / Calimoto / Google Maps):**
     * Läuft auf dem Smartphone im Hintergrund. Die Audio-Führung wird über den QCC3086 (`U9`) synchron in die Helme gestreamt.
  3. **BLE-Pfeilnavigation (`COMM_48`):**
     * Ist dediziert für das **native/optionale OMB-Cockpit-Display** (z. B. an Custom Bikes, Naked Bikes oder als Zusatzinstrument).

### 8.2 Werks-Lenkertasten-Bedienung (CAN-Bus Integration)
* **Harley-Davidson:** Taster der Lenkerarmaturen (LHCM / RHCM: Lautstärke, Track, PTT, Phone) werden auf dem Fahrzeug-CAN-Bus über den `TCAN334G` Transceiver der Zentralbox in Echtzeit mitgelesen.
* **BMW Motorrad:** Multi-Controller (Wonderwheel) CAN/LIN-Telegramme werden ebenfalls nativ ausgewertet.
* **Umsetzung:**
  * **Musik:** Lautstärke (`Vol+`/`Vol-`), Track Vor/Zurück, Play/Pause ➔ Direkte Übersetzung in AVRCP 1.6 Befehle an den QCC3086 (`U9`).
  * **Telefonie:** Eingehender Anruf im Helm ➔ Druck auf die Werks-Taste am Lenker sendet `ATA` (Anruf annehmen). Langer Druck sendet `AT+CHUP` (Auflegen/Ablehnen).
  * **Bikes ohne CAN:** Diskrete Tastereingänge (`BTN_L`, `BTN_R`, PTT) an der Frontnode (`PCBA 05`).

### 8.3 Das Display-Dilemma & der bewusste Kompromiss (Harley Road Glide vs. BMW GS)
Hier besteht ein unumgänglicher ergonomischer Unterschied zwischen den Fahrzeugtypen:

* **Fall A: BMW GS / GSA & Adventure Bikes (Smartphone am Lenker sichtbar)**
  * Das Smartphone wird an einer Lenkerhalterung (z. B. QuadLock / SP Connect) im direkten Sichtfeld montiert.
  * **Ergebnis:** Die OMB Companion App (Live-Schräglage, Reifendruck, Radar-Warnanzeige) oder Navigationskarten (Kurviger) sind permanent im Blick.
  * **Stromversorgung:** Die 30W-Ladeleitung (`J4`) kann flexibel zum Lenker-Ladekopf geführt werden.

* **Fall B: Harley-Davidson Touring (Road Glide / Street Glide)**
  * Am Lenker einer modernen Road Glide / Street Glide ist kaum Platz für eine Smartphone-Halterung, und das Motorrad besitzt bereits ein riesiges Werksdisplay (6.5" bzw. 12.3" SkylineOS).
  * Das Smartphone liegt unsichtbar im geschlossenen Handschuhfach auf dem Qi-Schnellladepuck.
  * **Der ehrliche, bewusste Kompromiss durch den Entfall von Android Auto / CarPlay:**
    * **Das Smartphone-Display bzw. die OMB Companion App kann auf der Harley NICHT auf den großen Werksbildschirm gespiegelt werden.**
    * Der Fahrer sieht unsere App während der Fahrt nicht.
    * **Die reale Praxis-Bedienung auf der Road Glide:**
      1. Für die visuelle Kartennavigation nutzt der Fahrer das verlässliche **Harley-Bordnavi auf dem großen Bildschirm**.
      2. Für Musik, Telefonie und Touren-Tracking läuft das Smartphone als robuster Server im Handschuhfach.
      3. Für Audio-geführte Kurviger-/Calimoto-Touren erfolgt die präzise Navigation **rein über das Gehör im Helm** (mit automatischem Musik-Ducking).
      4. Radar-Gefahrenwarnungen erfolgen akustisch mit Priorität 1 (-18 dB Ducking) im Helm sowie optional über dezente Warn-LEDs im Cockpit.

