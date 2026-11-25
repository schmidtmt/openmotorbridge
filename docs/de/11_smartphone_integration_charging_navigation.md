# 11 - Smartphone-Integration, Lade-Architektur & Navigations-Ergonomie

Dieses Dokument spezifiziert die verbindliche Schnittstelle zwischen Fahrer-Smartphone und OpenMotorBridge (OMB), die Fast-Charging-Ladeinfrastruktur im Handschuhfach, die Navigations-Architektur mit Werks-Headunits sowie die ergonomischen Unterschiede zwischen verschiedenen Fahrzeugplattformen (BMW GS vs. Harley-Davidson Touring).

---

## 1. Systemüberblick: Bewusster Entfall von Apple CarPlay & Android Auto

Frühere Konzepte sahen vor, Apple CarPlay und Android Auto über USB-Dongles und MFi-Headset-Emulationen auf die Werksdisplays (z. B. Harley Boom! Box GTS oder Skyline OS) zu spiegeln. Aus umfassenden Praxistests und realen Fahrpraxis-Erfahrungen wurde dieses Konzept **vollständig und bewusst verworfen**:

1. **Thermischer Notabschaltungs-Schutz im Handschuhfach:**
   * Ein Smartphone, das im geschlossenen Verkleidungs-Handschuhfach induktiv geladen wird und gleichzeitig einen 5 GHz Wi-Fi Direct H.264/H.265-Videostreaming-Stack betreibt, erreicht bei sommerlichen Außentemperaturen im Fach binnen 15–20 Minuten über $65\,^\circ\text{C}$.
   * Die Folge ist eine unweigerliche **thermische Schutzabschaltung des Smartphones** mitten auf der Tour.
2. **Proprietäre Instabilität & Update-Bruch:**
   * Display-Spiegelungen über USB-Dongles und emulierte Headset-Handshakes sind notorisch unzuverlässig, neigen zu Puffer-Latenzen und werden bei OEM-Firmwareupdates regelmäßig blockiert.
3. **Kabelbaum-Verschlankung & EMV-Schutz:**
   * Durch den Entfall des Handschuhfach-USB-Hubs (`PCBA 05B`) entfallen empfindliche High-Speed USB-Differenzialdatenpaare im Cockpit-Kabelbaum. Das Handschuhfach wird über eine **reine 2-adrige DC-Leitung** gespeist – null EMV-Einkopplung, null Datenkollisionen.

**Das Leitprinzip:** OpenMotorBridge konzentriert sich auf das, worin es unschlagbar ist: **Latenzfreie Audio-Hoheit (3× QCC3086), vollwertige HFP 1.8 Telefonie mit Helmmikrofon-Rückkanal, deterministisches DSP-Ducking und stabiles 30W Fast-Charging.**

---

## 2. Die reale Smartphone-Kopplung (Qualcomm QCC3086 `U9`)

Alle Interaktionen mit dem Smartphone laufen über den dedizierten Bluetooth 5.4 Audio-Transceiver **Qualcomm QCC3086 (`U9`)** und den System-DSP **ESP32-S31 (`U2`)**:

```
+----------------------------------------------------------------------------------------+
|                      SMARTPHONE ⟷ OPENMOTORBRIDGE SCHNITTSTELLEN                       |
+----------------------------------------------------------------------------------------+
  [Fahrer-Smartphone (im Handschuhfach oder am Lenker)]
        │
        ├─► [Bluetooth A2DP Sink] ──────► Qualcomm QCC3086 (U9) ──► I2S ──► ESP32-S31 DSP
        │   (Hi-Fi Musik Spotify/Apple)                             (Raised-Cosine Ducking)
        │
        ◄─► [Bluetooth HFP 1.8] ────────► Qualcomm QCC3086 (U9) ◄─► I2S ◄─► ESP32-S31 DSP
        │   (Vollduplex-Telefonie)        (mSBC / LC3 Speech)       ▲   (Helm-Mic Rückkanal)
        │                                                           │
        │                                                Fahrer-Helm (U13 QCC3086)
        │                                                Sozius-Helm (U14 QCC3086)
        │
        ◄─► [Bluetooth AVRCP 1.6] ──────► QCC3086 UART ◄── CAN-Bus ◄── Werks-Lenkertasten
        │   (Play/Pause, Next/Prev, Vol)                            (Harley LHCM / BMW Wheel)
        │
        ◄─► [BLE GATT Telemetrie] ──────► ESP32-S31 (U2) Onboard-Keramik (ANT3)
            (Schräglage, TPMS, eCall, Setup, Turn-by-Turn Pfeilnavigation via COMM_48)
```

### 2.1 Hi-Fi Musik-Streaming (A2DP Sink)
* **Codecs:** aptX Adaptive, aptX Lossless, LC3, AAC, SBC.
* **Latenz & Link-Budget:** Empfangen über die hocheffiziente Taoglas FXP73 Flex-Antenne im Zentralbox-Deckel (`ANT2`). Maximale Empfangsreserve auch bei feuchter Lederjacke oder Distanz zum Bike.
* **DSP-Ducking:** Das Mischpult im ESP32-S31 senkt die Musik bei Navigationshinweisen sanft um **-12 dB** und bei Radar-/Gefahrenwarnungen sofort um **-18 dB** ab.

### 2.2 Vollduplex-Telefonie & Freisprechen (HFP 1.8 mit Voice-Rückkanal)
* **Das Problem bisheriger Lösungen:** Reine A2DP-Audio-Empfänger können keine Sprache an das Smartphone zurücksenden. Ein Anruf zwang den Fahrer zum Anhalten, Ausziehen der Handschuhe und Herausholen des Telefons.
* **Die QCC3086-Lösung:**
  * Unterstützt das vollwertige **Hands-Free Profile (HFP 1.8)** mit `mSBC`- und `LC3`-Breitband-Sprachübertragung.
  * **Uplink (Voice-Rückkanal):** Das Fahrer-Helmmikrofon (empfangen über `U13`) wird vom DSP digital gefiltert (Windgeräuschunterdrückung) und mit **< 20 ms Latenz** als Rückkanal an das Smartphone übertragen.
  * Telefonate können während der Fahrt in glasklarer Qualität geführt werden.

### 2.3 Medien- & Anrufsteuerung über Werks-Lenkertasten
* **CAN-Bus Integration (100 % Listen-Only):**
  * Die Zentralbox liest über den automotiven CAN-Transceiver `TCAN334G` (`U6`) die Tastendrücke der originalen Lenkerarmaturen mit:
    * **Harley-Davidson:** Left Hand Control Module (LHCM) und Right Hand Control Module (RHCM).
    * **BMW Motorrad:** Multi-Controller (Wonderwheel) am linken Lenkergriff.
* **Befehlsübersetzung:**
  * **Musik:** Lautstärke (`Vol+`/`Vol-`), Track Vor/Zurück, Play/Pause ➔ Der ESP32-S31 übersetzt dies in **AVRCP 1.6** Steuerbefehle an den QCC3086 (`U9`).
  * **Telefonie:** Eingehender Anruf im Helm ➔ Druck auf die Werks-Taste am Lenker sendet `ATA` (Anruf annehmen). Langer Druck sendet `AT+CHUP` (Auflegen/Ablehnen).
  * **Custom Bikes:** Für Motorräder ohne CAN-Bus stellt die Frontnode (`PCBA 05`) diskrete Tastereingänge (`BTN_L`, `BTN_R`, PTT) bereit.

---

## 3. Lade-Architektur (Universal Dual-Mode: Normal 5V BC1.2 vs. USB-PD 3.0)

Die Ladeinfrastruktur im Cockpit und Handschuhfach wird zentral von der Front Node (`PCBA 05`) gespeist. Sämtliche Wandlungselektronik und Abwärme verbleibt auf der Platine im fahrtwindgekühlten Riser-Gehäuse, sodass weder am Lenker noch im geschlossenen Verkleidungsfach ein zusätzlicher 12V-Wandler nötig ist:

### 3.1 Universeller Multi-Protokoll Regler (SW3526 auf Front Node `PCBA 05`)
* **Reine USB-Ladeleitung ab Front Node (`J4`):** Vom integrierten Schnellladeregler **`SW3526` (`U5`)** auf `PCBA 05` führt eine robuste, fertig ausgeregelte Ladeleitung direkt zum gewünschten Ladeort (Lenker-Halterung oder Handschuhfach).
* **Dual-Mode Protokoll-Unterstützung (Normal vs. Fast-Charging):**
  * **USB Power Delivery 3.0 (PD) / QuickCharge 4.0:** Dynamische Spannungsverhandlung (5V / 9V / 12V / 15V) mit bis zu **30–36 W Ladeleistung**.
  * **USB BC1.2 DCP Standard (5V / bis 2.4A):** Nativer Fallback auf klassisches, ungeregeltes 5V-Laden.
* **Warum die Dual-Mode-Unterstützung (Normal + PD) unverzichtbar ist:**
  Viele motorradspezifische Zubehörteile auf Tour – wie Action-Cams, Helmlampen, Funk-Fernbedienungen, ältere Helm-Headsets, Reifendruck-Prüfgeräte oder USB-Akkupacks – besitzen **keinen USB-PD Controller** und können keine höheren Spannungen aushandeln. Würde ein Anschluss reine PD-Verhandlung erzwingen, blieben diese 5V-Legacy-Geräte schlichtweg ungeladen (dies gilt analog auch für Zubehör, das unterwegs in den Koffern an den `SW3516`-Ports von `PCBA 03` geladen wird). Der `SW3526` erkennt automatisch, was angeschlossen ist, und liefert für jedes Gerät das passende Ladeschema.

### 3.2 Modulare Nutzung: Entweder kabellos (Qi) ODER kabelgebunden
Da vom Front Node genau ein dedizierter Schnelllade-Kabelstrang abgeht, ist dieser als **modulare 1:1-Verbindung** ausgelegt (keine erfundene parallele „Doppel-Buchse“ an demselben Kabel):

* **Modus A: Kabellos (Qi / MagSafe / QuadLock):**
  * **Am Lenker (BMW GS / Enduro):** Das Kabel von `J4` wird direkt in den wetterfesten **Quad Lock Waterproof Wireless Charging Head** gesteckt. Der Kopf verhandelt mit dem `SW3526` per PD seine 9V/12V und lädt das eingeklinkte Smartphone vibrationsentkoppelt mit bis zu 15 W.
  * **Im Handschuhfach (Harley Touring):** Das Kabel führt zu einem flachen COTS-Qi-/MagSafe-Puck (z. B. QuadLock MAG kompatibel), auf dem das Telefon magnetisch haftet und mit 15 W induktiv lädt.
* **Modus B: Kabelgebunden (USB-C Direktanschluss):**
  * Steht maximaler Ladestrom im Fokus, wird das Smartphone bei sommerlicher Hitze für Induktionsladung zu warm ($> 40\,^\circ\text{C}$), oder soll Zubehör ohne Qi geladen werden: Das Kabel wird einfach an der Rückseite des Ladekopfes / Pucks abgezogen und direkt in das Endgerät gesteckt.
* **Action-Cams & Cockpit-Zubehör:**
  * Für Action-Cams (GoPro, Insta360) an Scheibe oder Lenker muss nicht das Smartphone-Ladekabel zweckentfremdet werden. Hierfür stellt die Front Node den separaten Port **`J8` (`CAM 5V` / 2.0A)** mit eigenem Kabel bereit.

---

## 4. Navigations-Architektur & Werks-Headunits

Moderne Motorrad-Headunits sind geschlossene Systeme. OpenMotorBridge löst die Navigation auf praxiserprobte Weise:

```
+----------------------------------------------------------------------------------------+
|                          DREI WEGE ZUR NAVIGATION MIT OMB                             |
+----------------------------------------------------------------------------------------+

  1. WERKS-BORDNAVI (Harley Boom! Box / SkylineOS oder BMW ConnectedRide TFT)
     [Harley / BMW Werksnavi] ──(Bluetooth Audio)──► Front Node (PCBA 05 FSC-BT802)
                                                                 │
                                                   (Digitaler Audiobus)
                                                                 ▼
     [Fahrer- & Soziushelm] ◄── (DSP Ducking -12 dB) ◄── Zentralbox ESP32-S31 DSP

  2. SMARTPHONE AUDIO-NAVIGATION (Kurviger, Calimoto, Google Maps)
     [Smartphone im Fach] ──(Bluetooth A2DP/HFP)──► QCC3086 (U9) ──► ESP32-S31 DSP ──► Helme

  3. NATIVES OMB-COCKPIT DISPLAY (Custom Bikes & Naked Bikes)
     [Smartphone App] ──────(BLE GATT COMM_48)────► ESP32-S31 ──► Cockpit OLED/TFT Display
     (Turn-by-Turn Pfeile, Restdistanz in Metern, Straßenname, Tempolimit)
```

### 4.1 Werks-Bordnavi (Harley SkylineOS / Boom! Box GTS / BMW TFT)
* Werks-Headunits erlauben kein Einschleusen externer Kartengrafiken oder Drittanbieter-Pfeile ohne CarPlay.
* **Die OMB-Lösung:** Nutzt der Fahrer das werksseitige Bordnavi auf dem großen Display, fängt das **FSC-BT802 Modul** auf der Frontnode (`PCBA 05`) die Audioansagen per Bluetooth digital ab.
* Der Zentralbox-DSP senkt Musik um -12 dB ab und legt die Navigationsansage in Studioqualität auf die Helme.

### 4.2 Smartphone Audio-Navigation (Kurviger / Calimoto)
* Viele Tourenfahrer bevorzugen die Kurvenalgorithmen von Kurviger oder Calimoto.
* Das Smartphone berechnet die Route im Handschuhfach. Die präzisen Sprachkommandos werden über den QCC3086 (`U9`) eingespielt. Der Fahrer navigiert zu **100 % über das Gehör**, ohne den Blick vom Asphalt abzuwenden.

### 4.3 BLE-Turn-by-Turn Pfeilnavigation (`COMM_48`)
* Für Motorräder mit dem **nativen OMB-Cockpit-Display** (z. B. Custom Bikes, ältere Harleys oder als Zusatz-Instrument):
* Smartphone-Apps senden kompakte BLE-GATT-Pakete:
  * Manöver-Icon-Code (Abbiegen links/rechts, Kreisverkehr mit Ausfahrtsnummer).
  * Distanz zum Abbiegepunkt in Metern.
  * Straßenname (UTF-8) und Tempolimit.
* Extrem stromsparend, blendfrei und verzögerungsfrei direkt im Sichtfeld.

---

## 5. Ergonomie- & Display-Realität: GS/GSA vs. Harley Road Glide

In der Praxis existiert ein elementarer Unterschied in der Cockpit-Ergonomie zwischen Reiseenduros und Touring-Maschinen:

| Merkmal | BMW GS / GSA & Adventure Bikes | Harley-Davidson Touring (Road Glide / Street Glide) |
| :--- | :--- | :--- |
| **Smartphone-Montageort** | Am Lenker / an der Scheibe (z. B. QuadLock / SP Connect) | Unsichtbar im geschlossenen Handschuhfach auf dem Qi-Puck |
| **Sichtbarkeit des Smartphone-Displays** | **Voll im direkten Sichtfeld des Fahrers** | **Nicht sichtbar (im geschlossenen Fach)** |
| **App-Nutzung während der Fahrt** | Die **OMB Companion App** (Live-Schräglage, Reifendruck, Radar-Warnanzeige) oder Kurviger-Karten sind permanent sichtbar. | **Die OMB-App kann NICHT auf den Harley-Bildschirm gespiegelt werden** (bewusster Entfall von Android Auto / CarPlay). |
| **Praxis-Navigation** | Visuell über Smartphone am Lenker oder BMW Navigator | **Sicht-Navigation über das Harley-Werksnavi auf dem 12.3"/6.5" Bildschirm**; Smartphone liefert Musik & Telefonie oder Audio-Tourenführung im Helm. |
| **Stromversorgung (`J4`)** | Führt flexibel zum Ladekopf am Lenker | Führt als 2-Draht DC-Zuleitung zum 30W Qi-Puck im Handschuhfach |

### Der ehrliche Kompromiss auf der Road Glide
Wir dokumentieren diesen Zustand ohne Schönfärberei:
* Mit Android Auto wäre eine Einblendung unserer App auf dem Harley-Screen theoretisch denkbar gewesen.
* Da Android Auto und CarPlay jedoch aufgrund von Instabilität, Dongle-Frust und Hitzeentwicklung im Fach **vollständig gestrichen wurden, sieht man die OMB-App auf der Harley während der Fahrt nicht.**
* Der Fahrer hat auf der Road Glide die klare, stressfreie Rollenverteilung:
  1. **Großer Werks-Bildschirm:** Reines Harley-Bordnavi und Standard-Tacho/Fahrzeuginfos.
  2. **Helme:** Vollständige, latenzfreie Audio-Führung (Navi-Ansagen, Spotify-Musik, Freisprech-Telefonie, Intercom, Radar-Warntöne).
  3. **Handschuhfach:** Telefon lädt kühl und magnetisch gesichert auf dem Qi-Puck.
