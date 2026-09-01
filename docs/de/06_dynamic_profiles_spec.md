# 06 - Klassenorientierte Hardwareprofile & Kassetten-Erkennung

OpenMotorBridge nutzt ein klassenorientiertes, erweiterbares Profil-System auf Basis von **LittleFS JSON-Dateien** (`/profiles/*.json`), um verschiedenste Sena-, Cardo- und Funk-Geraete beim Einstecken ueber den 1-Wire-Bus (`DS2401`) automatisch zu erkennen und zu konfigurieren.

---

## 1. Klassenorientierte Geraete-Hierarchie

Alle unterstuetzten Intercom- und Funkkassetten sind in 6 standardisierte Hardware-Klassen eingeteilt:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KLASSENORIENTIERTE HARDWARE-PROFIL-MATRIX                   │
├─────────┬───────────────────────────────┬─────────────────┬─────────────────┤
│ Klasse  │ Geraetefamilien               │ Mesh-Protokoll  │ DLE-Score Bonus │
├─────────┼───────────────────────────────┼─────────────────┼─────────────────┤
│ **K1**  │ Sena 60S, Apex, 50S/R/C, SRL3 │ Sena Mesh 3.0/2 │ **+60 Punkte**  │
│ **K2**  │ Sena Spider RT1/ST1           │ Mesh 2.0 Basic  │ **+40 Punkte**  │
│ **K3**  │ Sena Vortex, 20S, 10S, SF, 5S │ Bluetooth 5.1/4 │ **+20 Punkte**  │
│ **K4**  │ Cardo Edge, Pro, Custom, Neo  │ Cardo DMC Gen2  │ **+60 Punkte**  │
│ **K5**  │ Cardo Freecom 4x/2x, Spirit HD│ Live Intercom   │ **+40 Punkte**  │
│ **K6**  │ Cardo Bold, Black, Slim       │ Cardo DMC Gen1  │ **+30 Punkte**  │
│ **K7**  │ Midland G9 Pro, Baofeng/UHF   │ PMR446 Analog   │ **+10 Punkte**  │
│ **K0**  │ Deaktiviert / Leerer Slot     │ Keines          │ **0 Punkte**    │
└─────────┴───────────────────────────────┴─────────────────┴─────────────────┘
```

---

## 2. Profil-Uebersicht im Dateisystem (`/data/profiles/`)

### Klasse 1: Sena Next-Gen & High-Tier Mesh (`sena_60s.json`, `sena_apex.json`, `sena_50_series.json`)
* **Sena 60S (`sena_60s.json`):** Wave-Mesh-Intercom, bis zu 64 Teilnehmer, Dual-Chip RF-Hardening.
* **Sena Apex / Apex Plus (`sena_apex.json`):** Mesh 3.0 Referenzkassette, 32 Nodes, DLE +60 Pkt.
* **Sena 50er Serie & MeshPort (`sena_50_series.json`):** 50S, 50R, 50C, SRL3, MeshPort Blue/Red (Mesh 2.0/3.0, 24–32 Nodes).

### Klasse 2: Sena Spider & Mesh-Only (`sena_spider.json`)
* **Sena Spider RT1 / ST1:** Reine Mesh-Geraete ohne Bluetooth-Intercom-Overhead, DLE +40 Pkt.

### Klasse 3: Sena Bluetooth & 2-Way Intercom (`sena_vortex.json`, `sena_legacy_bt.json`)
* **Sena Vortex (`sena_vortex.json`):** Bluetooth 5.1 2-Wege-Intercom (1:1 bis 1,2 km), Quick-Pair Button-Trigger, DLE +20 Pkt.
* **Sena 20S EVO, 30K, 10S, 10R, SF4/SF2, 5S, SMH10 (`sena_legacy_bt.json`):** Jog-Dial Pulsmuster fuer BT-Multi-Hop, DLE +20 Pkt.

### Klasse 4: Cardo Dynamic Mesh Communications Gen2 (`cardo_dmc_gen2.json`)
* **Cardo Packtalk Pro, Edge, Custom, Neo:** DMC Gen2 mit Open DMC, schnellem Auto-Reconnect und DLE +60 Pkt.

### Klasse 5: Cardo Live Intercom & Freecom Serie (`cardo_freecom_live.json`)
* **Cardo Freecom 4x, Freecom 2x, Spirit HD:** Bluetooth 5.2 Live Intercom mit automatischem Reconnect, DLE +40 Pkt.

### Klasse 6: Cardo Legacy DMC Gen1 (`cardo_dmc_legacy.json`)
* **Cardo Packtalk Bold, Black, Slim, Smartpack:** DMC 1.0 mit bis zu 15 Teilnehmern, DLE +30 Pkt.

### Klasse 7: Universelle Analog- & PMR446-Funkkassetten (`pmr446_gateway.json`)
* **Midland XT-Serie (XT10/XT30/XT50 Bare-Board) & Integrierte SA818S Transceiver:** Kompakte PMR446-Kassettenmodule (500 mW ERP, 446.0–446.2 MHz, 16 Kanäle, CTCSS/DCS) für analoge Gruppen-Kommunikation.
* **Midland G9 Pro / Baofeng / Kenwood 2-Pin K-Type:** Externe Handfunkgeräte über wassergeschützte Doppelklinken-Blende.
* **Hardware-PTT:** Unterbrechungsfreie Tastung über PhotoMOS-Relais (Toshiba TLP222A auf Pin 5 `OPTO`) synchronisiert mit der Lenker-PTT-Taste oder automatischer DSP-Schwellwert-VOX.
* **Audio-Entkopplung:** Galvanische Trennung über Studio-Übertrager (Bourns LM-NP-1001) verhindert Masseschleifen und Bordnetz-Pfeifen vollständig.

### Klasse 8: Midland Intercom & Wave Serie (`midland_wave.json` / `midland_bt.json`)
* **Midland BTR1 Advanced, Rush RCF, BTX2 PRO S, Midland Wave, BT Mini:** Bluetooth 5.0/5.2 Intercom & Wave Mesh mit digitalem Audio-Pass-Through und DLE +30 Pkt.

---

## 3. Sicherheits-Fallback: `disabled.json` (Slot-Abschaltung)

Wird ein Steckplatz nicht belegt, eine Dummy-Leerkassette eingesetzt oder ein Pod in der WebApp manuell stillgelegt, laedt der ESP32-S3 sofort das Profil `disabled.json`:

```json
{
    "id": "disabled",
    "name": "Deaktiviert / Unbelegt (Disabled Slot)",
    "vendor": "OpenMotorBridge System",
    "hardware_tier": 0,
    "vcc_enabled": false,
    "soft_start_ms": 0,
    "input_gain_db": -96.0,
    "output_gain_db": -96.0,
    "noise_gate_threshold_db": -96,
    "control_mode": "disabled",
    "mesh_capabilities": {
        "protocol": "None",
        "dle_bonus_score": 0
    },
    "rf_hardening": {
        "expected_idle_current_ma": 0
    }
}
```

### Schutzwirkungen des `disabled.json` Profils:
1. **Stromlos-Schaltung (`vcc_enabled: false`):** Der zugehoerige P-Kanal MOSFET Power-Gate oeffnet sofort $\rightarrow$ 0.0 mA Stromverbrauch.
2. **Vollstaendige Audio-Stummschaltung:** Die Ein- und Ausgangs-Gains des ES8388 Codecs werden auf $-96\,\text{dB}$ gesetzt, um jegliches Rauschen oder Einstreuungen von offenen Leitungen zu eliminieren.
3. **Deaktivierung von Schaltsignalen:** Die Toshiba TLP222A Optokoppler bleiben dauerhaft hochohmig.
4. **DLE-Bereinigung:** Der DLE-Score-Beitrag faellt sofort auf 0 Punkte zurueck.

---

## 4. Plug-and-Play Hardware-Port-Schutz & Auto-Routing

Um Kurzschluesse und Fehlkonfigurationen (z. B. versehentliches Stecken einer Audio-Kassette an Pod 3 oder des Heck-Transceivers an Pod 1) zu verhindern, arbeitet die Kassetten-Initialisierung in 3 Phasen:

```
┌─────────────────────────────────────────────────────────────┐
│          3-PHASEN PLUG-AND-PLAY ERKENNUNGSSEQUENZ           │
├─────────────────────────────────────────────────────────────┤
│ 1. ERKENNUNGSPHASE: 1-Wire ID Abfrage (Strombegrenzt < 20mA)│
│ 2. VALIDIERUNG: Family-Code & UID Check gegen Profiltabelle │
│ 3. FREIGABE: Erst bei Match -> 5V MOSFET EIN & Audio/UART On│
└─────────────────────────────────────────────────────────────┘
```

1. **Strombegrenzte Erkennungsphase:** Beim Einstecken bleibt die Haupt-Speisung (5V MOSFET) gesperrt. Der 1-Wire-Treiber liest die 64-Bit Silicon Serial Number des DS2401 aus.
2. **Automatische Routing-Zuweisung:**
   * **Heck-Pod 3 UID erkannt:** Zentralbox schaltet Pins 15/16 auf High-Speed UART (@ 460.800 Baud) und initialisiert den NMEA/LoRa-Parser.
   * **Audio-Kassette (Sena/Cardo) erkannt:** Pins werden an den Bourns NF-Pfad und ES8388 I2S-DSP geschaltet; das zugehoerige JSON-Profil wird geladen.
   * **Dummy-Kassette oder Open-Pin erkannt:** Slot bleibt dauerhaft stromlos geschaltet (`disabled.json`).
3. **Soft-Start:** Nach erfolgreicher Validierung schaltet der P-FET die Speisespannung ueber eine definierte Soft-Start-Rampe ($100-150\,\text{ms}$) ein.

---

## 5. Kaufberatung & Adapter-Empfehlungen nach Preisspanne und Gruppen-Mesh

Je nach Budget, Fahrprofil und der in der Motorradgruppe vorherrschenden Intercom-Marken (Sena vs. Cardo vs. Mischbetrieb) empfehlen sich folgende Kassetten-Kombinationen:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EMPFOHLENE POD-BESTUECKUNGS-SZENARIEN                       │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ Setup-Kategorie       │ Pod 1 (Links)           │ Pod 2 (Rechts)            │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💎 **High-End Leader**│ **Sena 60S / Apex**     │ **Cardo Packtalk Edge**   │
│    (350 – 550 €)      │ (Mesh 3.0 Wave, K1)     │ (DMC Gen2 Air-Mount, K4)  │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⚖️ **Preis-Leistung** │ **Sena Spider RT1/ST1** │ **Cardo Freecom 4x / Bold**│
│    (180 – 280 €)      │ (Mesh 2.0 Pure, K2)     │ (Live Intercom/DMC, K5/K6)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💰 **Budget Einstieg**│ **Sena MeshPort Blue**  │ **IP67 Dummy-Kassette**   │
│    (80 – 140 €)       │ (oder Sena 20S/SF, K3)  │ (Slot stromlos / disabled)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 🏔️ **Adventure/Offroad**│ **Sena Apex / 50S**   │ **Midland G9 Pro PMR446** │
│    (220 – 320 €)      │ (Mesh 3.0, K1)          │ (Analogfunk Gateway, K7)  │
└───────────────────────┴─────────────────────────┴───────────────────────────┘
```

### 5.1 💎 High-End & DLE Leader Setup (Maximum Mesh & Zukunftssicherheit)
* **Zielgruppe:** Tourenguides, Vielfahrer, große gemischte Reisegruppen mit modernster Ausstattung.
* **Empfohlene Bestückung:**
  * **Pod 1:** *Sena 60S* oder *Sena Apex* (Wave Mesh 3.0, 64 Nodes, DLE +60 Pkt.)
  * **Pod 2:** *Cardo Packtalk Pro* oder *Packtalk Edge* (DMC Gen2, Air Mount, DLE +60 Pkt.)
* **Vorteile:** Volle $120\,\text{Punkte}$ Gateway-Bonus (dieses Motorrad wird automatisch zum DLE Leader der gesamten Gruppe), HiFi-Audioqualität mit minimaler Latenz ($< 8\,\text{ms}$).

### 5.2 ⚖️ Preis-Leistungs-Sieger / "Sweet Spot" (Der universelle Allrounder)
* **Zielgruppe:** Motorrad-Freundeskreise, in denen sowohl Sena- als auch Cardo-Fahrer unterwegs sind.
* **Empfohlene Bestückung:**
  * **Pod 1:** *Sena Spider RT1 / ST1* (Reines Mesh-Only ohne Bluetooth-Intercom-Overhead, ca. $120-140\,\text{€}$ neu / $85\,\text{€}$ gebraucht, DLE +40 Pkt.)
  * **Pod 2:** *Cardo Freecom 4x* oder gebrauchtes *Cardo Packtalk Bold (DMC Gen1)* (ca. $100-140\,\text{€}$, DLE +40/+30 Pkt.)
* **Vorteile:** Vollwertige Zwei-Wege-Mesh-Brücke zwischen Sena Mesh und Cardo DMC für unter $250\,\text{€}$ Gesamtbudget.

### 5.3 💰 Budget- & Stufen-Einstieg (Günstig starten, später aufrüsten)
* **Zielgruppe:** Einsteiger, Solofahrer mit gelegentlichem Soziusbetrieb oder Fahrer, deren Gruppe ausschließlich eine Marke nutzt.
* **Empfohlene Bestückung:**
  * **Pod 1:** *Sena MeshPort Blue* oder gebrauchtes *Sena 20S / 10S / SF4* (ca. $45-65\,\text{€}$ gebraucht, DLE +20/+40 Pkt.)
  * **Pod 2:** **IP67 Blind- / Leerkassette (`Pod_Dummy_Cartridge_IP67.stl`)** $\rightarrow$ Schacht ist doppelt O-Ring-versiegelt, firmwareseitig über `disabled.json` isoliert ($0{,}0\,\text{mA}$).
* **Vorteile:** Minimaler Anschaffungspreis ($< 100\,\text{€}$). Zweiter Schacht kann bei Bedarf jederzeit per Plug-and-Play mit einer Cardo- oder Funkkassette nachgerüstet werden.

### 5.4 🏔️ Adventure, Fernreise & Offroad (Unabhängig von Mobilfunk & Bluetooth-Reichweite)
* **Zielgruppe:** Trans-Euro-Trail (TET), Wüsten- und Hochgebirgsreisen, Enduro-Touren ohne Handynetz.
* **Empfohlene Bestückung:**
  * **Pod 1:** *Sena Apex* oder *Sena 50S* (Nahbereichs-Mesh für die Gruppe)
  * **Pod 2:** *Midland G9 Pro / Baofeng PMR446 Funkkassette* (Analoger Weitstreckenfunk über 446 MHz für kilometerweite Kommunikation)
  * **Pod 3 (Heck):** *Dual-PHY OpenMotorMesh (868 MHz LoRa Fallback)* für bis zu $15\,\text{km}$ Notfall-PTT und Gruppenradar.

---

## 6. Dynamisches Profil-Update & Merge-Verfahren (WebApp / Mesh 3.0 Sync)

Wenn ein Hersteller (z. B. Sena beim Sprung von Mesh 2.0 auf Mesh 3.0 oder Cardo bei DMC Gen 2) seine Firmware aktualisiert, passt sich OpenMotorBridge über ein intelligentes **JSON-Merge-Verfahren** an:

```
┌─────────────────────────────────────────────────────────────┐
│                 JSON PROFIL-MERGE-VERFAHREN                 │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Basis-Herstellerprofil    │ 2. Individuelle User-Offsets │
│    (z.B. sena_apex_v3.json)  │    (Ducking & Audio-Gains)   │
├──────────────────────────────┴──────────────────────────────┤
│                             ▼                               │
│ 3. Gemergtes Live-Profil im LittleFS Flash-Speicher          │
│    (Aktualisierte Opto-Timings + persönliche Lautstärken)   │
└─────────────────────────────────────────────────────────────┘
```

### Die 3 Phasen des Profil-Merges:
1. **Basis-Parameter:** Neue Optokoppler-Pulsdauern (z. B. `ptt_pulse_ms: 180`), geänderte Kanalwechselmuster (`[1000, 300, 200]`) und DLE-Bonuswerte werden aus dem neuen Hersteller-JSON geladen.
2. **User-Settings Preservation:** Individuelle Anpassungen des Fahrers (z. B. $+2{,}0\,\text{dB}$ Mikrofonpegel, $-12\,\text{dB}$ Navi-Ducking) bleiben beim Update erhalten und werden über die Basiswerte gemerged.
3. **Hot-Reload:** Die Zentralbox wendet die gemergten Parameter im laufenden Betrieb ohne Neustart sofort auf den ES8388 Codec und die TLP222A Opto-Puls-Engine an.

---

## 7. WebApp-Workflow: Automatische Erkennung & Erstzuweisung neuer Kassetten-UIDs

Wenn ein Nutzer eine neue Kassetten-Trägerplatine mit fabrikneuem DS2401 Chip baut oder einsteckt, führt die OpenMotorBridge WebApp/PWA einen benutzerfreundlichen Onboarding-Dialog durch:

```
┌─────────────────────────────────────────────────────────────┐
│ 🧩 NEUE KASSETTE ERKANNT!                                   │
├─────────────────────────────────────────────────────────────┤
│ Erkannter Steckplatz:   Pod 1 (Rahmen links)                │
│ 1-Wire Chip-UID:        01:A2:3B:4C:5D:6E:7F:8A             │
├─────────────────────────────────────────────────────────────┤
│ Dieser Kassetten-Hardware wurde bisher noch kein Profil     │
│ zugewiesen. Welches Intercom oder Funkgerät ist verbaut?    │
│                                                             │
│ Hardware-Profil:  [ 🔵 Sena 50S / 50R / SRL3 (K1)      ▼ ]  │
├─────────────────────────────────────────────────────────────┤
│ [ Später zuweisen ]         [ Profil zuweisen & speichern ] │
└─────────────────────────────────────────────────────────────┘
```

### Der Schritt-für-Schritt-Ablauf:
1. **Automatischer Scan:** Der ESP32-S3 pollt im 2-Sekunden-Takt (`task_cartridge_manager`) beide 1-Wire-Ports. Erkennt er einen Presence-Pulse mit gültiger CRC8 und Family-Code `0x01` (DS2401), sendet er die 64-Bit UID via BLE-Telemetrie an die WebApp.
2. **Dialog-Pop-up:** Die WebApp vergleicht die UID mit der hinterlegten Zuordnungstabelle (`/profiles/mapping.json` / PWA `localStorage`). Ist die UID neu, öffnet sich automatisch das Zuweisungs-Modal (`#uuid-detect-modal`).
3. **Profil-Auswahl & Speicherung:** Der Fahrer wählt sein Modell (z. B. *Sena 50S*, *Cardo Packtalk Edge*, *PMR446*) und klickt auf "Zuweisen".
4. **Persistentes Mapping:** Das Mapping `{"<UID>": "<profile_id>"}` wird dauerhaft im ESP32 LittleFS und im Browser gespeichert.
5. **Vollautomatische Wiedererkennung:** Zukünftig wird diese physische Kassette an jedem beliebigen Pod-Steckplatz (Pod 1 oder Pod 2) sofort ohne Rückfrage als das zugewiesene Modell erkannt, parametrisiert und im DLE-Gateway eingerechnet.

---

### 7.1 Zero-Trust Hardware-Quarantäne (Fail-Safe Schutzabschaltung)

> [!CAUTION]
> **Elektronikschutz-Prinzip:** Solange eine neu gesteckte Kassetten-Hardware (DS2401 UID) keinem verifizierten Profil zugewiesen wurde, wird der entsprechende Pod-Steckplatz **strikt wie ein unvollständig oder fehlerhaft gesteckter Slot behandelt**:
> 1. **5V VCC Power-Gate OFF (0,0 mA):** Der P-Kanal Lastschalter zum OEM-Cradle bleibt vollständig gesperrt. Das Intercom erhält keinerlei Betriebsspannung.
> 2. **Audio DSP Mute (-96 dB):** Beide Audiokanäle (Eingang & Ausgang) des ES8388 Codecs sind software- und hardwareseitig stummgeschaltet, um Knacken, Rauschen oder Übersprechen zu verhindern.
> 3. **Optokoppler hochohmig (OFF):** Die TLP222A Relais für PTT und Tasterauslösung bleiben geöffnet.
> 4. **DLE Gateway-Bonus = 0:** Kein Einrechnen unbestätigter Hardware in den DLE-Score.
> 
> **Erst wenn der Nutzer in der WebApp das Profil bestätigt** (oder die UID bereits im Flash-Mapping hinterlegt ist), führt der Controller eine kontrollierte Soft-Start-Einschaltsequenz (50 ms Inrush-Limiting) durch und schaltet die Audiopegel frei.


