# 17 - Dongle-Free CarPlay & Android Auto Bridge Architektur (PCBA 05)

## 1. Systemüberblick & Problemstellung

Modernere Motorräder – insbesondere **Harley-Davidson Modelle mit Boom! Box GTS und dem 2024+ Skyline OS** – bieten großformatige Touchscreen-Displays mit Smartphone-Integration. In der Praxis stehen Fahrer jedoch vor massiven proprietären Barrieren:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROPRIETÄRE INFOTAINMENT-BARRIERE (OEM)                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [Fahrer-Smartphone]                                   [Harley Skyline OS / Boom! Box]
  • Android Auto: Komplett gesperrt oder fehlerhaft  ──► USB-Port blockiert Verbindung
  • Apple CarPlay: Erfordert OEM-Headset-Handshake    ──► "Kein Headset verbunden"
                   (WHIM-Modul für 450 € nötig!)           (CarPlay bleibt grau & inaktiv)
  • Externe Dongles: Fliegen lose in der Fairing,     ──► Abstürze bei Sommerhitze (>65°C),
                     ziehen Ruhestrom, kein WHIM-Byp.     Verbindungsabbrüche, Kabelsalat
```

### Die OpenMotorBridge Lösung: Integrierte Bridge auf PCBA 05

Die OpenMotorBridge v8.0 integriert die Dongle- und Headset-Emulationslogik direkt auf der **PCBA 05 (Universal Front-Knoten)** in der Frontverkleidung (Batwing / Sharknose / Lampenmaske). Dadurch entfallen externe Dongles, zusätzliche Kabel und teure OEM-Freischaltmodule restlos.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               OPENMOTORBRIDGE DONGLE-FREE ARCHITEKTUR (PCBA 05 EMBEDDED)               │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [Smartphone (iOS / Android)]
              │ Wireless (Wi-Fi 5 GHz 802.11ac + BLE 5.2)
              ▼
  ┌────────────────────────────────────────────────────────────────────────────────────┐
  │ PCBA 05: UNIVERSAL FRONT-NODE (In Fairing integriert)                              │
  │                                                                                    │
  │   ┌────────────────────────────────────────────────────────────────────────────┐   │
  │   │ Linux SOM (Allwinner V3s / T113-S3 Dual-Core ARM Cortex-A7 @ 1.2 GHz)      │   │
  │   │                                                                            │   │
  │   │  • Wireless Host: Hostapd (5 GHz Wi-Fi) & BlueZ Bluetooth Stack            │   │
  │   │  • Protocol Bridge Daemon:                                                 │   │
  │   │      - Android Auto Client: Empfängt H.264 Video + Audio vom Android-Phone │   │
  │   │      - CarPlay Accessory Emulator: Kapselt Video in Apple CarLife Stream   │   │
  │   │      - WHIM / Headset Emulator: Simuliert aktives Apple MFi-Headset        │   │
  │   │  • Video Transcoder Engine: H.264 Zero-Copy NAL Passthrough (< 35 ms)      │   │
  │   │  • Audio Mixer & I2S Bridge: Kopplung mit Helmmikrofon (Sena/Cardo)        │   │
  │   └────────────────────────────────────────────────────────────────────────────┘   │
  │                                     │                                              │
  │   ┌─────────────────────────────────┴──────────────────────────────────────────┐   │
  │   │ ESP32-S3 Front Controller: Power-Gate MOSFET, CAN-Bus Sniffer, BLE-PTT     │   │
  │   └─────────────────────────────────┬──────────────────────────────────────────┘   │
  └─────────────────────────────────────┼──────────────────────────────────────────────┘
                                        │ USB 2.0 High-Speed OTG (Kabel im Fach)
                                        ▼
                  [Harley-Davidson Skyline OS / Boom! Box GTS Display]
                   • Erkennt "Offizielles Apple CarPlay mit Headset"
                   • Vollbild-Navigation (Google Maps, Calimoto, Kurviger)
                   • Volle Lenker-Fernbedienung (Joystick & Voice Button)
```

---

## 2. Hardware-Evaluation & SOM-Auswahl

Für den lüfterlosen Dauerbetrieb im geschlossenen Hohlraum der Motorrad-Frontverkleidung (Temperaturbereich nach ISO 16750-2 von **-40 °C bis +85 °C**) scheiden Standard-Einplatinencomputer (wie Raspberry Pi 4/5) aufgrund ihrer hohen Verlustleistung (> 5 W) und thermischen Drosselung aus.

### Vergleichsmatrix System-on-Module (SOM)

| Kriterium | Allwinner V3s | Allwinner T113-S3 (Empfohlen) | NXP i.MX6ULL | Raspberry Pi CM4 |
| :--- | :--- | :--- | :--- | :--- |
| **CPU Core** | 1x Cortex-A7 @ 1.2 GHz | **2x Cortex-A7 @ 1.2 GHz** | 1x Cortex-A7 @ 792 MHz | 4x Cortex-A72 @ 1.5 GHz |
| **DSP** | Kein | **HiFi4 Audio DSP (400 MHz)**| Kein | Kein |
| **RAM (integriert)**| 64 MB DDR2 SIP | **128 MB DDR3 SIP** | Extern (128–512 MB) | Extern (1–8 GB) |
| **Video Decoder** | 1080p @ 60 fps H.264 | **1080p @ 60 fps H.264/H.265**| 720p @ 30 fps (Software) | 4K @ 60 fps |
| **USB Controller** | 1x OTG 2.0, 1x Host | **1x OTG 2.0, 1x Host 2.0** | 2x USB 2.0 OTG | 1x USB 2.0 |
| **Leistungsaufnahme**| ~0.8 W (Volllast) | **~1.1 W (Streaming)** | ~1.0 W | > 4.5 W (Überhitzungsgefahr) |
| **Gehäusetemp. (65°C)**| 72 °C (Passiv) | **76 °C (Passiv)** | 74 °C (Passiv) | > 95 °C (Thermal Throttle) |
| **Kosten (1k Stk.)**| ca. 4.80 $ | **ca. 6.20 $** | ca. 14.50 $ | ca. 35.00 $ |

### Display-Auflösungen: Boom! Box GTS vs. Skyline OS (12.3")

| Infotainment-System | Display-Typ & Diagonale | Native Panel-Auflösung | CarPlay Streaming-Profil |
| :--- | :--- | :--- | :--- |
| **Boom! Box GTS** | 6.5" TFT Touchscreen | **800 × 480 (WVGA, 5:3)** | 800 × 480 @ 60 fps (H.264 Baseline) |
| **Skyline OS (2024+)**| 12.3" Ultrawide TFT | **1920 × 720 (Ultrawide 8:3)** | 1920 × 720 / 1280 × 720 Fenster-Modus |

> [!IMPORTANT]
> **Reichen 1080p beim Allwinner T113-S3 wirklich aus?**
> - **Auflösungsbedarf Display:** Das physische 12.3"-Panel der neuen Harley-Generation hat eine native Auflösung von **$1920 \times 720$ Pixeln** (Automotive Breitbild-Standard, Seitenverhältnis 8:3). CarPlay nutzt auf der Harley entweder ein Teilfenster (z. B. $1280 \times 720$) neben den virtuellen Rundinstrumenten oder den vollen Breitbildbereich ($1920 \times 720$). Die CarPlay-Spezifikation unterstützt maximal **1080p ($1920 \times 1080$)** bzw. $1920 \times 720$. Rein auflösungsseitig reicht 1080p also vollkommen aus.
> - **Die kritische Hardware-Grenze des Allwinner T113-S3:** Der T113-S3 besitzt zwar eine VPU zur Hardware-**Decodierung** von H.264/H.265 bis 1080p60, verfügt jedoch über **keinen schnellen H.264-Hardware-Encoder**!
>   - Wenn Android Auto und Skyline OS dieselbe native Auflösung ($1280 \times 720$ oder $1920 \times 720$) und kompatible H.264-Profile aushandeln, genügt *Zero-Copy NAL Passthrough* (reines Umpaketieren ohne Re-Encoding, CPU-Last $< 12\,\%$, Latenz $< 35\,\text{ms}$).
>   - Müssen jedoch Auflösungen skaliert oder Frame-Raten umgerechnet werden, bricht die Dual-Core Cortex-A7 CPU beim Software-Encoding ein ($> 150\,\text{ms}$ Latenz, Ruckeln).

### Hardware-Design auf PCBA 05
* **SoC:** Allwinner T113-S3 im kompakten QFN128-Gehäuse mit 128 MB integriertem DDR3-RAM.
* **Speicher:** 8 GB eMMC 5.1 (Automotive pSLC Mode für 100.000 Schreibzyklen, vibrationsfest).
* **Wi-Fi / BT:** Realtek RTL8821CS (802.11a/b/g/n/ac 1T1R 5 GHz mit WPA3-Personal + Bluetooth 5.0 Dual Mode).
* **Automotive USB-Switch:** TI TS3USB221 High-Speed USB 2.0 Multiplexer für unterbrechungsfreies Umschalten zwischen Accessory- und Host-Modus.
* **P-Kanal Power-Gate (Kaltstart-Reset):** Vishay SI2301CDS P-MOSFET schaltet die 5V VBUS-Spannung zum SOM über einen GPIO des ESP32-S3 in 2.5 s ab (Warmstart-Funktion gegen Display-Freeze).

---

## 3. Architektur-Dilemma: Linux-Blackbox vs. Embedded RTOS vs. Modularer Dongle

In der Praxis existiert eine berechtigte Skepsis gegenüber einer „Linux-Blackbox“ im fest verbauten Front-Knoten:
- **Nachteile einer integrierten Linux-Lösung:** Bootzeiten von 15–25 Sekunden, Dateisystem-Korruption (Ext4/eMMC) bei hartem Ausschalten der Zündung, ständiger Wartungsaufwand für Kernel-Sicherheits-Patches und Inkompatibilitäten bei neuen Android Auto / iOS Major-Updates.
- **Warum scheidet ein FPGA aus?** Apple CarPlay und Android Auto sind keine reinen Videoschnittstellen (wie HDMI oder LVDS), sondern hochkomplexe Netzwerk- und Krypto-Software-Stacks (OSI Schichten 4–7: WPA3 Wi-Fi Direct, TLS 1.3, Bonjour/mDNS, Hunderte Google Protobuf RPCs). Eine Synthese in VHDL/Verilog ist unwirtschaftlich und erfordert im Endeffekt wiederum einen Soft-Core-Prozessor mit Betriebssystem.

### Die drei Lösungswege im Vergleich

| Kriterium | Option A: Festes Linux-SOM auf PCBA 05 | Option B: Pure MCU / FreeRTOS (ESP32-S3 / Crossover MCU) | Option C: OpenMotorBridge Smart-Managed Dongle (Empfohlen) |
| :--- | :--- | :--- | :--- |
| **Linux-Blackbox?** | **Ja** (Kernel, Rootfs, Wartung) | **Nein** (100% Bare-Metal Firmware) | **Nein** (OMB bleibt 100% Linux-frei) |
| **Kaltstart / Bootzeit** | 15–20 Sekunden | **< 300 Millisekunden** | **< 300 Millisekunden (OMB instant-on)** |
| **iPhone Wireless CarPlay** | Ja | **Ja** (Schlanker RTSP/CarPlay Bridge Stack)| **Ja** (Nativ über USB oder Crossover-MCU) |
| **Android Auto ➔ CarPlay** | Ja (via NAL Passthrough) | Extrem limitiert (kein H.264 Scaling) | **Ja** (Über ausgelagerten Mini-Stick) |
| **Wartung bei Google/Apple Update** | Firmware-Flash der Motorrad-Hardware | Firmware-Flash nötig | **Einfaches 2-Minuten-App-Update des Sticks** |
| **Platzbedarf in Sharknose** | Minimal (direkt auf PCB) | Minimal (direkt auf PCB) | **Minimal** (Kompakt im Sharknose-Handschuhfach) |
| **Ruhestrom bei Standby** | Sleep-Mode Steuerung nötig | **0.0 µA** (Deep Sleep) | **Echte 0.0 µA** (TPS2553 Power-Switch trennt VBUS) |

### Das empfohlene hybride Referenzdesign: OpenMotorBridge Smart-Managed Frontnode

#### 1. Die Ausgangslage bei Harley-Davidson (Skyline OS & Boom! Box GTS)
* **Apple CarPlay ist ab Werk nur KABELGEBUNDEN:** Der Fahrer muss das Smartphone jedes Mal umständlich im Fach an das USB-Kabel anstecken.
* **Android Auto existiert ab Werk GAR NICHT:** Harley verweigert die native Android-Auto-Lizenzierung.
* **Wichtige Dongle-Unterscheidung (CP2AA vs. reine AA-Dongles):**
  Ein herkömmlicher Wireless-Android-Auto-Dongle (wie z. B. *Motorola MA1*) funktioniert an einer Harley **überhaupt nicht**, weil er eine fahrzeugseitige Android-Auto-Schnittstelle voraussetzt. An einer Harley muss der Adapter zwingend ein **Übersetzungs-Adapter (CP2AA: CarPlay-to-Android-Auto)** sein (z. B. *Ottocast U2-X Pro* oder *Carlinkit 4.0*), der sich gegenüber der Harley als Apple CarPlay ausgibt und dem Smartphone drahtloses Android Auto bereitstellt!

#### 2. Der Mehrwert: Vollautomatischer, Headless-Betrieb durch OpenMotorBridge

Normalerweise nerven diese 2-in-1-Adapter im Alltag, weil man zwischen CarPlay und Android Auto manuell umschalten oder auf dem Display warten muss. OpenMotorBridge eliminiert dieses Problem vollständig:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             OPENMOTORBRIDGE HEADLESS DONGLE MANAGEMENT (PCBA 05)                       │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [1. FAHRER-ERKENNUNG BEI ZÜNDUNG EIN (< 200 ms via BLE / PWA-Profil)]
  ├──► Fall A: Fahrer hat Android-Smartphone erkannt
  │    • OMB schaltet den TPS2051B Lastschalter EIN (5.0 V VBUS)
  │    • OMB steuert den Dongle headless an ──► Direktstart im CP2AA-Übersetzungsmodus
  │    • Kein Auswahldialog ("iPhone / Android?") auf dem Harley-Screen!
  │    • Harley zeigt kabelloses Android Auto über CarPlay-Stream.
  │
  ├──► Fall B: Fahrer hat iPhone erkannt
  │    • Option 1: Dongle wird von OMB im reinen Wireless-CarPlay Pass-Through gestartet
  │      (macht aus dem kabelgebundenen Skyline OS CarPlay ein drahtloses CarPlay!).
  │    • Option 2 (Handy am Ladekabel): OMB lässt den Dongle-Port STROMLOS.
  │
  └──► Fall C: Kein gekoppeltes Smartphone / Kurze Tour / Radio-Betrieb
       • OMB lässt den Dongle-USB-Port KOMPLETT AUS (0.0 mA).
       • Keine Erwärmung in der Verkleidung, kein Funkmüll, kein Boot-Overhead!
```

#### 3. Kernvorteile für den Fahrer
1. **Drahtlose Freiheit für beide Welten:**
   - iPhone-Fahrer erhalten **Wireless CarPlay** (ohne Kabel ins Fach fummeln zu müssen).
   - Android-Fahrer erhalten **Wireless Android Auto** auf dem Harley-Display.
2. **Absolut Headless:** Kein Tastendruck am Dongle, kein Menü im Webbrowser (`192.168.1.101`), kein Auswahlscreen.
3. **Hardware-Schutz & Zero-Drain:** Der Dongle läuft nur dann, wenn er wirklich gebraucht wird. Ansonsten bleibt er stromlos.
4. **Wartungsfreiheit:** Wenn Google oder Apple ihre Protokolle ändern, bleibt die feste Motorrad-Elektronik unberührt – man aktualisiert einfach den 40-€-Stick per Smartphone-App.

---

## 4. Protokoll-Bridging: Android Auto zu Apple CarPlay Emulation

Harley-Davidson unterstützt bei neueren Baujahren nativ ausschließlich **Apple CarPlay**. Android-Nutzer bleiben außen vor. Die OpenMotorBridge implementiert einen universellen Übersetzer:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROTOKOLL-BRIDGING ABLAUF-DIAGRAMM                              │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [Android Smartphone]               [OpenMotorBridge SOM]            [Harley Skyline OS]
           │                                   │                                │
           │ 1. Wireless Android Auto Auth     │                                │
           ├──────────────────────────────────►│                                │
           │    (Wi-Fi 5 GHz TLS Handshake)    │                                │
           │                                   │ 2. Apple MFi USB iAP2 Init     │
           │                                   ├───────────────────────────────►│
           │                                   │    (Simuliert Apple iPhone)    │
           │                                   │                                │
           │                                   │ 3. WHIM Headset Presence Auth  │
           │                                   ├───────────────────────────────►│
           │                                   │    "Headset Connected: OK"     │
           │                                   │◄───────────────────────────────┤
           │                                   │    Harley schaltet CarPlay EIN │
           │                                   │                                │
           │ 4. Video-Stream (H.264 720p @60)  │                                │
           ├──────────────────────────────────►│ 5. NAL Repackaging (Zero-Copy) │
           │                                   ├───────────────────────────────►│
           │                                   │    CarPlay Video Surface Frame │
           │                                   │                                │
           │ 6. Audio-Stream (Opus / PCM)      │ 7. I2S Audio Ducking Engine    │
           ├──────────────────────────────────►│    (-18 dB bei Radar-Warnung)  │
           │                                   ├───────────────────────────────►│
           │                                   │    PCM 48 kHz Stereo Output    │
           │                                   │                                │
           │                                   │ 8. Lenkertaste / PTT gedrückt  │
           │ 9. Google Assistant Aktivierung   │◄───────────────────────────────┤
           │◄──────────────────────────────────┤    Injiziert als HID-Key Event │
```

### Video Pipeline & Latenz-Optimierung
* **Zero-Copy H.264 NAL Passthrough:** Android Auto sendet Videoframes als standardkonforme H.264 Annex-B NAL-Units. Der Bridge-Daemon transkodiert das Video nicht neu, sondern verpackt die NAL-Units direkt in das von Apple CarPlay geforderte RTP/AVP-Containerformat.
* **Latenz-Budget:**
  * Wi-Fi Übertragung Smartphone ➔ SOM: **12 ms**
  * NAL Repackaging & Socket Buffer: **3 ms**
  * USB High-Speed Transfer SOM ➔ Skyline OS: **4 ms**
  * Display-Rendering im Motorrad: **16 ms**
  * **Gesamtlatenz (Glass-to-Glass): 35 ms** (Vollkommen flüssig bei 60 fps, keine spürbare Verzögerung bei Touch-Eingaben).

## 5. WHIM Headset-Bypass & Helmmikrofon-Routing

### Das Harley WHIM-Problem
Harley-Davidson sperrt die CarPlay-Aktivierung im Infotainment-System, wenn kein kabelgebundenes 7-Pin-Headset oder das 450 € teure **Wireless Headset Interface Module (WHIM)** erkannt wird. Zubehör-Headsets (wie Standard-Sena oder Cardo) werden zwar per Bluetooth gekoppelt, schalten CarPlay aber **nicht** frei oder degradieren die Audioausgabe auf minderwertiges Mono (A2DP blockiert).

### OpenMotorBridge Virtual WHIM Generator
1. **USB iAP2 Feature Descriptor:** Die Bridge meldet sich am USB-Bus als zertifiziertes Apple MFi-Zubehör mit aktiviertem Sprach-Endpunkt (`VoiceOverAudio` Feature-Bit `0x04` aktiv).
2. **Reines Bluetooth HD Audio Helmmikrofon-Routing (100% kabellos):**
   - Der Fahrer- (und Sozius-)Helm ist **ausschließlich drahtlos per Bluetooth HD Audio** (LE Audio LC3 oder Bluetooth Classic HFP 1.8 Wideband Speech) mit OpenMotorBridge gekoppelt. Es gibt **keinerlei Kabelverbindung** zum Helm!
   - Die Kassetten-Pods (Pod 1 / Pod 2) dienen rein als optionale **Fahrzeug-Schnittstellen** (z. B. für den kabelgebundenen Harley-OEM-Kabelbaum älterer Boom! Box GTS Modelle), niemals für das Headset des Fahrers.
   - Der ESP32-S3 Audio-DSP übernimmt die Windgeräuschunterdrückung, AGC und das Raised-Cosine-Ducking (-18 dB bei Radar-Warnung) und schleift den aufbereiteten digitalen Sprachkanal via USB Audio Class (UAC) direkt in die Headunit ein.
3. **Nahtlose Sprachassistenten:** Wenn der Fahrer die Lenkertaste drückt oder *"Hey Siri"* bzw. *"Hey Google"* sagt, öffnet die Bridge den Mikrofonstream direkt zum Smartphone. Das Motorrad akzeptiert die Audioeingabe ohne jede Fehlermeldung oder WHIM-Sperre.

---

## 6. Lenkerbedienung & CAN-Bus Injektion

Über die Universal Front-Node (PCBA 05) werden die Bedienelemente des Motorrads direkt mit den Smartphone-Funktionen verknüpft:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BEDIENMATRIX: LENKERTASTER & ACTIONS                            │
└────────────────────────────────────────────────────────────────────────────────────────┘

  Bedienelement am Motorrad           Signalweg                    Aktion auf Display
  ─────────────────────────────────────────────────────────────────────────────────────
  Joystick Links kurz                CAN-Bus / Front-Node         Vorheriger Musiktitel
  Joystick Rechts kurz               CAN-Bus / Front-Node         Nächster Musiktitel
  Joystick Klick / Mute              CAN-Bus / Front-Node         Play / Pause Toggle
  Voice-Taste (Sprechtaste) kurz     CAN-Bus / Front-Node         Siri / Google Assistant
  Voice-Taste lang (> 2.0 s)         Front-Node GPIO              OpenMotorBridge PTT
  Radar-Warnung (Garmin Varia)       Heck-Pod CAN-Telegramm       Navi/Musik -18 dB Duck
  eCall Sturz erkannt (> 6.5 g)      Main-Box LoRa SOS            Vollbild SOS Notruf-Overlay
```

---

## 7. Thermomanagement & Kaltstart-Schutz (Automotive Grade)

### 1. Kaltstart-Sicherheit (ISO 7637-2 Pulse 4)
Beim Betätigen des Motorrad-Anlassers bricht die Bordnetzspannung oft kurzzeitig auf **5.8 V bis 6.5 V** ein. Der integrierte Aufwärts-/Abwärtswandler (Buck-Boost TPS63070) auf PCBA 05 hält die 5.0 V VBUS-Versorgung des SOMs absolut stabil bei **5.00 V ± 1%**, sodass das Navigationssystem beim Starten des Motors **nicht** neu bootet.

### 2. Fairing-Hitzeschutz (Bis 85 °C Umgebung)
In der geschlossenen Frontverkleidung über dem heißen V-Twin-Motor staut sich im Hochsommer die Hitze. Das SOM nutzt ein mehrstufiges DVFS-Profil (Dynamic Voltage and Frequency Scaling):
* **< 65 °C:** Volle Leistung (Dual-Core @ 1.2 GHz, 1080p60 NAL passthrough).
* **65 °C – 78 °C:** Taktfrequenz 1.0 GHz, Core-Spannung von 1.20 V auf 1.10 V gesenkt (-28 % Abwärme).
* **> 78 °C:** Taktfrequenz 816 MHz, Core-Spannung 1.00 V (-48 % Abwärme). Der 720p60 Video-Stream läuft ruckelfrei weiter.

### 3. One-Click Hard Reboot via PWA & Lenkertaste
Sollte sich das Smartphone oder der CarPlay-Stack aufhängen, kann das SOM über die PWA (Tab 1 Cockpit & Tab 5 Hardware) oder durch 3-sekündiges Halten der PTT-Taste neu gestartet werden:
* ESP32-S3 sperrt das P-MOSFET Gate für **2500 ms**.
* SOM und USB-Bus sind restlos stromlos (0.0 V, Entladung über 100 Ω Pulldown).
* Saubere Re-Initialisierung des USB-Handshakes mit dem Motorrad in unter 6 Sekunden.

---

## 8. Zusammenfassung & Vorteile

| Feature | Herkömmlicher Carlinkit / Ottocast Dongle | OpenMotorBridge PCBA 05 Bridge |
| :--- | :--- | :--- |
| **Einbauort** | Lose im Fach / Handschuhfach (Kabelsalat) | **Voll integriert in Frontverkleidung (PCBA 05)** |
| **Harley WHIM-Zwang**| CarPlay blockiert ohne teures Extra-Modul | **Voll emuliert (WHIM & MFi Headset Bypass)** |
| **Android Auto** | Auf neueren Harleys oft nicht unterstützt | **Voll unterstützt via Android-Auto-to-CarPlay Bridge** |
| **Helmmikrofon** | Nur eigenes Dongle-Mic oder schlechte BT-Kopplung| **Direktkopplung mit Sena/Cardo Helmen via I2S** |
| **Radar Ducking** | Keine Verbindung zu Heck-Radar Sensoren | **Raised-Cosine Ducking (-18 dB) bei Annäherung** |
| **Sommerhitze (>65°C)**| Stürzt nach 20–40 min ab | **Automotive DVFS & Kaltstart-geschützt bis 85 °C** |
