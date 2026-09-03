# 02 - Intercom-Matrix, PTT-Steuerung & Dynamische Kassetten-Profile

Dieses Dokument spezifiziert die universelle **Intercom-Routing-Matrix**, die latenzfreie **Lenker-PTT-Steuerung** (< 1,8 ms) sowie das klassenorientierte **Hardwareprofil-System** der OpenMotorBridge v8.0 auf Basis des 1-Wire DS2401 ID-Chips und der LittleFS-Profil-Engine.

---

## 1. Intercom-Routing-Matrix & Brückenarchitektur

Die OpenMotorBridge fungiert als aktive Audio-Kreuzschiene und Brückengateway zwischen zwei physischen Intercom-Einheiten (Pod 1 und Pod 2), externen Audioquellen (Navi / Boom! Box) und den Bluetooth-Helmen von Fahrer und Sozius:

```
                               INTERCOM ROUTING MATRIX
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                        │
│   SATELLITEN-POD 1 (Sena Mesh)           SATELLITEN-POD 2 (Cardo DMC / PMR446)         │
│   ┌──────────────────────────┐           ┌──────────────────────────┐                  │
│   │ • Sena 50S / 60S / Apex  │           │ • Cardo Edge / Pro / Neo │                  │
│   │ • 1-Wire DS2401 ROM-ID   │           │ • 1-Wire DS2401 ROM-ID   │                  │
│   │ • TLP222A Opto-Trigger   │           │ • TLP222A Opto-Trigger   │                  │
│   └────────────┬─────────────┘           └────────────┬─────────────┘                  │
│                │ NF_P1_OUT/IN                         │ NF_P2_OUT/IN                   │
│                ▼                                      ▼                                │
│   ┌──────────────────────────┐           ┌──────────────────────────┐                  │
│   │ Bourns LM-NP-1001-B1L    │           │ Bourns LM-NP-1001-B1L    │                  │
│   │ 1500V RMS Trennübertrager│           │ 1500V RMS Trennübertrager│                  │
│   └────────────┬─────────────┘           └────────────┬─────────────┘                  │
│                │ Differenziell                        │ Differenziell                  │
│                ▼                                      ▼                                │
│       ┌────────────────────────────────────────────────────────────┐                   │
│       │        ES8388 24-BIT I2S STEREO AUDIO CODEC & DSP          │                   │
│       │  • Raised-Cosine Ducking (Prio: Notfall > Navi > Intercom) │                   │
│       │  • Symmetrischer Intercom-Cross-Mix (P1 <-> P2)            │                   │
│       │  • Knowles MEMS Fahrtwind-Lautstärkenachführung (AGC)      │                   │
│       └─────────────────────────────┬──────────────────────────────┘                   │
│                                     │                                                  │
│              ┌──────────────────────┴──────────────────────┐                           │
│              ▼                                             ▼                           │
│   ┌────────────────────────────┐              ┌────────────────────────────┐           │
│   │ FAHRER-HELM (Bluetooth)    │              │ SOZIUS-HELM (Bluetooth)    │           │
│   │ • Sena/Cardo/OEM Headset   │              │ • Sena/Cardo/OEM Headset   │           │
│   │ • Gemischtes Gesamt-Audio  │              │ • Getrennte Lautstärke     │           │
│   └────────────────────────────┘              └────────────────────────────┘           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Die 3 Standard-Betriebsmodi
1. **Modus 0: Standard-Modus (Full Mesh Bridge):**  
   Port 1 (z. B. Sena Wave 3.0) und Port 2 (z. B. Cardo DMC Gen2) sind gleichzeitig aktiv. Sprache von Sena-Fahrern wird in Millisekunden in das Cardo-Mesh übertragen und umgekehrt. Fahrer und Sozius hören beide Gruppen symmetrisch gemischt.
2. **Modus 1: Single Rider Mode (Fokus-Modus):**  
   Port 2 wird softwareseitig stummgeschaltet (`-96 dB`). Der volle DSP- und Routing-Fokus liegt auf dem Primär-Headset (Port 1), Navigationsdurchsagen und Smartphone-A2DP-Musik.
3. **Modus 2: Cruise Mode (Bordlautsprecher-Ausgabe):**  
   Intercom-Signale werden um $-6\,\text{dB}$ bedämpft und auf die Bordlautsprecher (Harley-Davidson Boom! Box GTS / BMW Soundanlage) geroutet.

---

## 2. Zero-Latency PTT-Steuerung & Optokoppler-Zündung (< 1,8 ms)

Klassische Bluetooth-Fernbedienungen am Lenker leiden unter hohen Latenzen ($80 \dots 250\,\text{ms}$) und Verbindungsaussetzern. OpenMotorBridge löst dieses Problem durch eine hybride PTT-Architektur:

```
               LENKER-PTT SIGNALKETTE (GLAS-ZU-GLAS < 1,8 ms)
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. LENKERTRASTER (Am Front-Knoten verdrahtet):                                         │
│    • Mechanischer Goldkontakt-Taster am Lenker (IP67, 100% batteriefrei)               │
│    • Hardware-Schmitt-Trigger-Entprellung (12 µs Latenz)                               │
│    • GPIO 0 Pegel-Interrupt auf ESP32-C3 RISC-V Controller                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                               │
│ 2. ULTRA-LOW-LATENCY FUNKBRÜCKE (ESP-NOW 2.4 GHz):                                     │
│    • Direktes IEEE 802.11 Vendor-Specific Action Frame (Payload: 8 Bytes)              │
│    • Keine TCP/IP- oder BLE-Stack-Latenzen                                             │
│    • Übertragungszeit Front-Knoten -> Zentralbox: 0,90 ms (PDR: 99,8 %)                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                        ▼                                               │
│ 3. ZENTRALBOX HARDWARE-TRIGGER:                                                        │
│    • ESP32-S3 Core 0 ISR erfasst ESP-NOW Frame                                         │
│    • Sofortiges Durchschalten des Toshiba TLP222A PhotoMOS Optokopplers (< 45 µs)      │
│    • Gesamtzeit vom Tastendruck bis zum gezündeten Intercom-PTT: 1,74 ms               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Hardware-Eigenschaften des Toshiba TLP222A Optokopplers
* **Galvanische Isolation:** $1500\,\text{V}_{\text{RMS}}$ Durchschlagsfestigkeit zwischen Steuer- und Lastkreis.
* **Schaltzeit:** Einschaltzeit $t_{\text{ON}} \le 0{,}5\,\text{ms}$, Ausschaltzeit $t_{\text{OFF}} \le 0{,}2\,\text{ms}$.
* **Prellfreiheit:** Da rein photo-elektronisch (Halbleiter-MOSFET-Schalter), treten im Gegensatz zu mechanischen Relais keinerlei Kontaktprellen oder Funkenstörungen auf.
* **Schonung der Headset-Elektronik:** Schaltet direkt gegen Masse oder Signal-Bias, exakt entsprechend der OEM-Tasterbeschaltung (z. B. Sena Mesh-Taste oder Cardo Phone-Button).

---

## 3. Klassenorientierte Hardwareprofile & Gerätehierarchie

Alle unterstützten Intercom- und Funkkassetten sind in 8 standardisierte Hardware-Klassen eingeteilt:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 KLASSENORIENTIERTE HARDWARE-PROFIL-MATRIX                   │
├─────────┬───────────────────────────────┬─────────────────┬─────────────────┤
│ Klasse  │ Gerätefamilien                │ Mesh-Protokoll  │ DLE-Score Bonus │
├─────────┼───────────────────────────────┼─────────────────┼─────────────────┤
│ **K1**  │ Sena 60S, Apex, 50S/R/C, SRL3 │ Sena Mesh 3.0/2 │ **+60 Punkte**  │
│ **K2**  │ Sena Spider RT1/ST1           │ Mesh 2.0 Basic  │ **+40 Punkte**  │
│ **K3**  │ Sena Vortex, 20S, 10S, SF, 5S │ Bluetooth 5.1/4 │ **+20 Punkte**  │
│ **K4**  │ Cardo Edge, Pro, Custom, Neo  │ Cardo DMC Gen2  │ **+60 Punkte**  │
│ **K5**  │ Cardo Freecom 4x/2x, Spirit HD│ Live Intercom   │ **+40 Punkte**  │
│ **K6**  │ Cardo Bold, Black, Slim       │ Cardo DMC Gen1  │ **+30 Punkte**  │
│ **K7**  │ Midland G9 Pro, Baofeng/UHF   │ PMR446 Analog   │ **+10 Punkte**  │
│ **K8**  │ Midland BTR1, Rush RCF, Wave  │ Midland Wave    │ **+30 Punkte**  │
│ **K0**  │ Deaktiviert / Leerer Slot     │ Keines          │ **0 Punkte**    │
└─────────┴───────────────────────────────┴─────────────────┴─────────────────┘
```

---

## 4. 1-Wire DS2401 Kassetten-Erkennung & 3-Phasen Plug-and-Play

Jede Kassetten-Trägerplatine (`openmotorbridge_pod_cartridge`) besitzt einen fest verlöteten **Maxim/Analog Devices DS2401** Silizium-Seriennummern-Chip. Dieser übermittelt eine weltweit eindeutige 64-Bit-UID (`Family-Code 0x01 + 48-Bit Seriennummer + 8-Bit CRC`) über nur eine einzige Datenleitung.

```
┌─────────────────────────────────────────────────────────────┐
│          3-PHASEN PLUG-AND-PLAY ERKENNUNGSSEQUENZ           │
├─────────────────────────────────────────────────────────────┤
│ 1. ERKENNUNGSPHASE: 1-Wire ID Abfrage (Strombegrenzt < 20mA)│
│ 2. VALIDIERUNG: Family-Code & UID Check gegen Profiltabelle │
│ 3. FREIGABE: Erst bei Match -> 5V MOSFET EIN & Audio/UART On│
└─────────────────────────────────────────────────────────────┘
```

1. **Strombegrenzte Erkennungsphase:** Beim Einstecken bleibt die Haupt-Speisung (5V MOSFET) gesperrt. Der 1-Wire-Treiber pollt mit strombegrenzter Hilfsspannung ($< 20\,\text{mA}$) und liest die UID aus.
2. **Automatische Routing-Zuweisung:**
   * **Heck-Pod 3 UID erkannt:** Zentralbox schaltet Pins 15/16 auf High-Speed UART (@ 460.800 Baud) und initialisiert den NMEA/LoRa-Parser.
   * **Audio-Kassette (Sena/Cardo) erkannt:** Pins werden an den Bourns NF-Pfad und ES8388 I2S-DSP geschaltet; das zugehörige JSON-Profil wird geladen.
   * **Dummy-Kassette oder Open-Pin erkannt:** Slot bleibt dauerhaft stromlos geschaltet (`disabled.json`).
3. **Soft-Start:** Nach erfolgreicher Validierung schaltet der P-FET die Speisespannung über eine definierte Soft-Start-Rampe ($100-150\,\text{ms}$) ein.

---

## 5. Systematik der OEM-Adapter-Anbindung: Klassen & Verkabelung

OpenMotorBridge unterstützt alle marktgängigen Intercom-Geräte im Originalzustand ohne Öffnen des Gehäuses:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   ÜBERSICHT DER 5 OEM-ADAPTER ANSCHLUSS-KLASSEN                       │
├───────────────────┬─────────────────────────────┬──────────────────────────────────────┤
│ Adapter-Klasse    │ Typische Geräte-Vertreter   │ Anschluss- & Schnittstellen-Typ      │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Klasse A:**     │ Sena +Mesh (B2M-01),        │ • Reine 5V-Speisung (90° Micro-USB / │
│ Drahtlos-Bridge   │ Sena MeshPort Blue / Red,   │   USB-C) über Header J2 (Pin 1 & 2)  │
│ (Nur-Strom / USB) │ Cardo Packtalk Outdoor Dongle│ • Audio drahtlos via Bluetooth      │
│                   │                             │ • Externe SMA-Bulkhead Doppelbuchse  │
│                   │                             │ • Mechanik: OEM-Schlitten & Gummiband│
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Klasse B:**     │ Sena 50S, 60S, 30K,         │ • Vollwertig analog (Audio In & Out) │
│ Pogo-Pin Klemmen  │ Sena 20S EVO, SRL3          │ • 6-adriges Flachband von J2 auf     │
│ (Federkontakt-Bett│                             │   Pogo-Pin Kontaktleiste im Inlay    │
│                   │                             │ • TLP222A PTT-Trigger (Pin 6)        │
│                   │                             │ • Mechanik: Klick-Bett wie Helmclip  │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Klasse C:**     │ Cardo Packtalk Edge,        │ • Vollwertig analog (Audio In & Out) │
│ Magnetischer      │ Cardo Packtalk Pro,         │ • 5-Pol Federkontaktfeld im Inlay    │
│ Air-Mount         │ Cardo Packtalk Neo          │ • 2x N52 Neodym-Magnete mit Führungs-│
│                   │                             │   keil für werkzeugloses Andocken    │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Klasse D:**     │ Cardo Packtalk Bold / Black,│ • Vollwertig analog (Audio In & Out) │
│ Schiebe-Cradle    │ Cardo Freecom 1 / 2 / 4+    │ • Seitliche Schiebekontakte im Inlay │
│                   │                             │ • Mechanik: Gleitschiene mit Arretier│
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Klasse E:**     │ Midland G7 / G9 Pro, G13,   │ • 2-Pin Doppelklinke (2.5mm + 3.5mm) │
│ Analoger Funk     │ Midland XT30, Baofeng,      │ • Opto-PTT tastet PTT gegen Masse    │
│ (PMR446 / Kenwood)│ Kenwood TK-Serie            │ • 5V DC/DC Speisung (Batteriedummy)  │
│                   │                             │ • Feste 446MHz Wendel oder SMA-Front │
└───────────────────┴─────────────────────────────┴──────────────────────────────────────┘
```

### 5.1 Detaillierte Pin-Belegung der Kassetten-Schnittstelle (`J2`)
Der 6-polige **JST-SH 1.0 mm Header (`J2`)** auf der Kassettenplatine führt alle Signale:

| Pin | Signal | Klasse A (+Mesh) | Klasse B (Sena 50S) | Klasse C (Cardo Edge)| Klasse E (PMR446) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Micro-USB Pin 5 (GND) | Pogo-Pin 1 (GND) | Air-Mount Pad 1 (GND) | Klinke Schirm / Masse |
| **2** | `5V_VBUS` | Micro-USB Pin 1 (+5V) | Pogo-Pin 2 (5V Charge)| Air-Mount Pad 2 (5V Charge)| Batteriedummy 5V In |
| **3** | `AUDIO_R+` | *N/C (Reines BT-Audio)* | Pogo-Pin 4 (Spk R+) | Air-Mount Pad 3 (Spk +)| Klinke Lautsprecher + |
| **4** | `AUDIO_R-` | *N/C (Reines BT-Audio)* | Pogo-Pin 5 (Spk R-) | Air-Mount Pad 4 (Spk -)| Klinke Lautsprecher - |
| **5** | `MIC_IN+` | *N/C (Reines BT-Audio)* | Pogo-Pin 6 (Mic +) | Air-Mount Pad 5 (Mic +)| Klinke Mikrofon + |
| **6** | `OPTO_PTT` | *N/C* | Pogo-Pin 7 (Mesh-Btn)| *N/C* (Aux) | PTT Taster gegen Masse |

---

## 6. Sicherheits-Fallback: `disabled.json` & Zero-Trust Quarantäne

Wird ein Steckplatz nicht belegt, eine Blindkassette eingesetzt oder eine unbekannte UID erkannt:
1. **Stromlos-Schaltung (`vcc_enabled: false`):** Der P-Kanal MOSFET öffnet sofort $\rightarrow 0{,}0\,\text{mA}$ Ruhestrom.
2. **Audio-Stummschaltung:** Ein- und Ausgangs-Gains des ES8388 werden auf $-96\,\text{dB}$ gesetzt.
3. **Optokoppler hochohmig:** TLP222A Relais bleiben dauerhaft geöffnet.
4. **DLE-Score = 0:** Kein Einrechnen unbestätigter Hardware in das Gruppen-Routing.

---

## 7. WebApp-Workflow: Automatische Erkennung & Profilzuweisung

Beim Einstecken einer neuen Kassetten-Hardware führt die PWA einen automatischen Onboarding-Dialog aus:
1. **Automatischer Scan:** ESP32-S3 pollt alle 2 Sekunden beide 1-Wire-Ports und sendet neue UIDs via BLE an die WebApp.
2. **Dialog-Pop-up:** Die WebApp öffnet das Zuweisungs-Modal (`#uuid-detect-modal`).
3. **Profil-Auswahl & Speicherung:** Der Fahrer wählt sein Modell aus dem Dropdown.
4. **Persistentes Mapping:** Das Mapping `{"<UID>": "<profile_id>"}` wird dauerhaft im ESP32 LittleFS und im Browser gespeichert.
5. **Wiedererkennung:** Zukünftig wird diese Kassette an jedem beliebigen Steckplatz sofort automatisch parametrisiert.

---

## 8. Empfohlene Bestückungs-Szenarien nach Preis und Einsatzzweck

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EMPFOHLENE POD-BESTÜCKUNGS-SZENARIEN                        │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ Setup-Kategorie       │ Pod 1 (Links)           │ Pod 2 (Rechts)            │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💎 **High-End Leader**│ **Sena 60S / Apex**     │ **Cardo Packtalk Edge**   │
│    (350 – 550 €)      │ (Mesh 3.0 Wave, K1)     │ (DMC Gen2 Air-Mount, K4)  │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⚖️ **Preis-Leistung** │ **Sena Spider RT1/ST1** │ **Cardo Freecom 4x / Bold**│
│    (180 – 280 €)      │ (Mesh 2.0 Pure, K2)     │ (Live Intercom/DMC, K5/K6)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💰 **Budget Einstieg**│ **Sena MeshPort Blue**  │ **IP67 Blind-Kassette**   │
│    (80 – 140 €)       │ (oder Sena 20S/SF, K3)  │ (Slot stromlos / disabled)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 🏔️ **Adventure/Offroad**│ **Sena Apex / 50S**   │ **Midland G9 Pro PMR446** │
│    (220 – 320 €)      │ (Mesh 3.0, K1)          │ (Analogfunk Gateway, K7)  │
└───────────────────────┴─────────────────────────┴───────────────────────────┘
```
