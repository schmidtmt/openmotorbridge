# OpenMotorBridge: USB-Systemarchitektur & Grundprinzipien
**Dokumenten-ID:** OMB-ARCH-USB-2026-V1  
**Status:** Verbindliche Systemvorgabe (Architectural Ground Truth)  
**Datum:** 19. November 2026  
**Gültig für:** PCBA 01 (Main Box), PCBA 03 (Pod Cartridge), PCBA 05 (Front-Node), PCBA 08 (Radar), PCBA 09/10 (OMM)

---

## 1. Präambel & Verbindlichkeit

Dieses Dokument definiert die unverrückbare **Grundarchitektur der USB-Topologie, Master/Client-Rollen und Signalpfade** für das Gesamtsystem OpenMotorBridge.

> [!IMPORTANT]
> **Verbindlichkeitsklausel:**  
> Jede zukünftige Schaltungs-, Firmware- oder Layoutänderung **muss zwingend** gegen diese Grundprinzipien gegengecheckt werden.  
> Jede Änderung, die gegen eines dieser Grundprinzipien verstößt, **ist unzulässig** bzw. muss vor jeder Umsetzung im Detail diskutiert und angepasst werden, bis sie wieder vollständig mit diesen Prinzipien konform ist.

---

## 2. Grundprinzip 1: Der alleinige USB-Master (Zentralbox PCBA 01)

### 2.1 Single-Host-Architektur
* Der **`ESP32-S31` auf der Zentralbox (`PCBA 01`)** ist der **einzige und alleinige USB-Master (Host)** auf dem internen Fahrzeug-Backbone-Netzwerk.
* **Kein Satellit** (weder Front-Node, noch Pods, noch Radar) darf auf diesem Bus jemals als USB-Host agieren.
* Alle Satelliten sind reine **USB-Clients (Devices)**.

### 2.2 Physische Topologie & Hub-Isolation
Die Zentralbox hostet den Bus über ihren On-Board Industrial-Hub `U8` (`Microchip USB2517I`). Über den zentralen 16-poligen Molex Micro-Lock Plus Peripheriestecker `J6` werden 4 strikt getrennte, geschützte Downstream-Stränge sternförmig im Fahrzeug verteilt:

```
                          ┌───────────────────────────┐
                          │   Zentralbox (PCBA 01)    │
                          │   ESP32-S31 [USB-MASTER]  │
                          │            │              │
                          │   USB-Hub (USB2517I)      │
                          └──────┬───┬───┬───┬────────┘
                                 │   │   │   │
        ┌────────────────────────┘   │   │   └────────────────────────┐
        │ BUS1                       │   │                       BUS4 │
        ▼                            │   │                            ▼
┌──────────────┐                     │   │                     ┌──────────────┐
│  Front-Node  │                     │   │                     │  Rear Radar  │
│  (PCBA 05)   │                     │   │                     │  (PCBA 08)   │
│ [USB-Client] │                     │   │                     │ [USB-Client] │
└──────────────┘                     │   │                     └──────────────┘
                                     │   │
                        ┌────────────┘   └────────────┐
                        │ BUS2                   BUS3 │
                        ▼                             ▼
                 ┌──────────────┐              ┌──────────────┐
                 │ Pod 1 Links  │              │ Pod 2 Rechts │
                 │  (PCBA 03)   │              │  (PCBA 03)   │
                 │ [USB-Client] │              │ [USB-Client] │
                 └──────────────┘              └──────────────┘
```

* **Strang 1 (`BUS1`):** Front-Node (`PCBA 05`) $\rightarrow$ USB Client (Sensoren, Taster, Status, Display-Brücke).
* **Strang 2 (`BUS2`):** Pod 1 Links (`PCBA 03`) $\rightarrow$ USB Client (Bay 1 Audio & PTT).
* **Strang 3 (`BUS3`):** Pod 2 Rechts (`PCBA 03`) $\rightarrow$ USB Client (Bay 2 Audio & PTT).
* **Strang 4 (`BUS4`):** Heck-Radar (`PCBA 08`) $\rightarrow$ USB Client (Radar-Target-Streams & Blind-Spot-Daten).

---

## 3. Grundprinzip 2: Front-Node Multi-Host / Dual-Client & Mode-Switch

### 3.1 Das Multi-Host-Dilemma am Lenker
Am Front-Node treffen zwei physikalisch und logisch getrennte USB-Host-Systeme aufeinander:
1. **Fahrzeug-Backbone:** Zentralbox (`ESP32-S31` ist Host).
2. **Infotainment-System:** Das Motorrad-Infotainment (**Harley-Davidson Boom! Box GTS / SkylineOS**) oder ein nachgerüstetes System (**Nachrüst-Android-Auto / CarPlay-Box / Display**) ist der Host.

Ein USB-Client kann niemals gleichzeitig an zwei asynchronen USB-Hosts hängen (unterschiedliche VBUS-Domänen, asynchrone SOF-Token, getrennte Bus-Zustände).

### 3.2 Die Dual-Client-Architektur des Front-Nodes
Der Front-Node stellt **zwei getrennte USB-Client-Pfade** bereit:
* **Client 1 (Backbone-Client):** Kommuniziert mit der Zentralbox (Sensoren, Lenkertaster, Blinker/Licht-Trigger, Telemetrie, PTT).
* **Client 2 (Infotainment-Client):** Kommuniziert mit der Headunit als Eingabe-/Steuerungs-Peripherie.

### 3.3 Mode-Switch statt 3. USB-Client (SkylineOS vs. Nachrüst-AA)
* **Funktionale Exklusivität:** Ein Motorrad betreibt zu jedem Zeitpunkt genau **ein** aktives Haupt-Infotainment:
  * **OEM-Betrieb:** Die Werks-Headunit (**SkylineOS**) ist der Master.
  * **Aftermarket-Betrieb:** Die Nachrüst-Box / das externe AA-Display am Pigtail `J6` ist der Master.
* **Hardware-Realisierung via High-Speed USB-Mux:**
  Ein 2:1 High-Speed USB-Multiplexer (z.B. TI `TS3USB221` oder OnSemi `FSUSB42`) schaltet die Datenleitungen (`D+` / `D-`) des Infotainment-Clients 2 um:

```
[ Zentralbox (Host) ]
        │ (Backbone USB J1)
        ▼
┌─────────────────────────────────────────────────────────────────┐
│ FRONT-NODE (PCBA 05)                                            │
│                                                                 │
│  [ Client 1: Backbone-Interface ]                               │
│                                                                 │
│  [ Client 2: Infotainment-Interface ]                           │
│           │                                                     │
│     (D+ / D-)                                                   │
│           ▼                                                     │
│    ┌──────────────┐                                             │
│    │ 2:1 USB-Mux  │─── Pos A: OEM ────────► [ SkylineOS / GTS ] │
│    │ (TS3USB221)  │                                             │
│    │              │─── Pos B: Aftermarket ─► [ Nachrüst-AA J6 ] │
│    └──────▲───────┘                                             │
│           │                                                     │
│     [ Mode-Steuerung & CP2AA_PWR_EN ]                           │
└─────────────────────────────────────────────────────────────────┘
```

* **Vorteile der Mux-Architektur:**
  1. **Kein 3. Client nötig:** Die Front-Node Firmware bedient für Infotainment-Events genau einen logischen Stack.
  2. **Galvanische & logische Entkopplung:** Keine Querverbindungen zwischen SkylineOS und Nachrüst-Dongle; kein Back-Powering.
  3. **Energie-Management:** In Position A bleibt `CP2AA_PWR_EN` inaktiv (Nachrüst-Dongle komplett stromlos). In Position B wird er selektiv bestromt.

---

## 4. Grundprinzip 3: Pod-Cartridges (PCBA 03) – Single Device ID & Hybrid-Audio

### 4.1 Genau eine USB-Identität pro Pod
* **Verbot von USB-Hubs & COTS-Audiochips im Pod:**
  Auf der Wechseleinschub-Platine `PCBA 03` darf sich **kein USB-Hub** und kein COTS-USB-Audiochip befinden.
* **Deterministische Bay-Erkennung:**
  Jeder Pod meldet sich an der Zentralbox als **genau ein USB-Composite-Device** mit einer festen, unverwechselbaren Hardware-ID an (z.B. über Bay-Strap-Pin: Linker Einschub = Bay 1, Rechter Einschub = Bay 2).
* **Vermeidung von Host-Rennen:**
  Die Zentralbox weist den Audio-Stream deterministisch dem jeweiligen Helm (Fahrer / Sozius) zu. Dynamische ALSA-Soundkarten-Vertauschungen beim Heißstecken sind physikalisch ausgeschlossen.

### 4.2 Keine HF-Sender auf der Pod-Platine
* Im Pod-Gehäuse befindet sich **kein eigener BLE- oder 2.4-GHz-Transceiver** (außer dem eigentlichen eingesteckten OEM- oder OMM-Funkmodul).
* **Grund:** Vermeidung von Funküberlagerung (RF Congestion) durch 3 parallele 2.4-GHz-Sender auf engstem Raum.
* **Konsequenz:** Alle PTT-, Steuer- und Einschalt-Signale (`Q1..Q4`) werden **ausschließlich kabelgebunden digital** von der Zentralbox über den USB-Backbone an den Pod übertragen.

### 4.3 Hybrid-Audio & PTT-Umschaltung an Stecker J4 via Signal-Switch (TMUX1574)
Der 8-polige Intercom-Schnittstellenstecker `J4` (`AUDIO_PWR_8P`) verbindet den Pod mit dem jeweiligen Intercom-Adapter (Sena, Cardo, Midland oder OMM). **An `J4` liegt kein USB an.** Die Umschaltung zwischen analogem Headset und digitalem Mesh erfolgt über einen kompakten 4-Kanal 2:1 Signal-Switch (`TI TMUX1574`, WQFN-16 / TSSOP-16) anhand des Signals `OMM_DETECT` (Pin 6):

| Pin J4 | Basis-Signal | Bank 0: OEM-Adapter (`OMM_DETECT = 0`, Analog) | Bank 1: OpenMotorMesh (`OMM_DETECT = 1`, Digital I2S) |
| :---: | :---: | :--- | :--- |
| **1** | `PGND` | Power-Masse | Power-Masse |
| **2** | `VBUS_5V` | 5V Stromversorgung Intercom | 5V Stromversorgung OMM |
| **3** | `AGND` | Analoge Audio-Masse | Schirm / Digitale Masse |
| **4** | **MUX CH1** | `AUDIO_IN_L` (Analog Audio Out L vom Codec-DAC zum Helm) | `I2S_BCLK` (Digital Audio Bit Clock vom ESP32-C6) |
| **5** | **MUX CH2** | `AUDIO_IN_R` (Analog Audio Out R vom Codec-DAC zum Helm) | `I2S_WS` (Digital Audio Word Select / LRCLK vom ESP32-C6) |
| **6** | `OMM_DETECT` | Pull-Down auf PCBA 03 (Logisch `0`) | Pull-Up auf PCBA 09/10 (Logisch `1`) |
| **7** | **MUX CH3** | `VOICE_OUT` (Analoges Helmmikrofon zum Codec-ADC) | `I2S_DOUT` (Digital Audio Data Out zum Mesh) |
| **8** | **MUX CH4** | `PTT_BTN` (Hardware-PTT nach GND getastet) | `I2S_DIN` (Digital Audio Data In vom Mesh) *(PTT digital im Stream)* |

* **OEM-Mode (Sena / Cardo / Midland):**
  * Zentralbox streamt Audiodaten im OMB-Frameformat (`USB_PKT_AUDIO_STREAM_DOWN`, 0x24) über USB an den Pod-ESP32-C6 $\rightarrow$ I2S an Codec `ES8388` $\rightarrow$ analoge Ausgabe über Pins 4/5 an Helm.
  * Helmmikrofon kommt über Pin 7 in den Pod-Codec `ES8388` $\rightarrow$ Digitalisierung via I2S $\rightarrow$ ESP32-C6 packt Samples in OMB-Frames (`USB_PKT_AUDIO_STREAM_UP`, 0x25) $\rightarrow$ USB an Zentralbox.
  * PTT-Taste am Lenker $\rightarrow$ Signal an Front-Node $\rightarrow$ Zentralbox schickt digitales PTT-Event an Pod $\rightarrow$ Pod-MCU zieht Pin 8 per Open-Drain gegen Masse.
* **Native OpenMotorMesh Mode (OMM):**
  * Vollständig verlustfreier, digitaler I2S-Direktpfad zwischen Pod-ESP32-C6 und OMM-Transceiver.
  * Keine unnötige D/A $\rightarrow$ A/D Wandlung; minimale Latenz und maximale Sprachqualität im Mesh.
  * **In-Band PTT:** Das PTT-Signal wird im OMM-Modus digital als Status-Flag im Audiostream übertragen. Dadurch wird Pin 8 auf Stecker `J4` frei und übernimmt als vierter I2S-Pin die Datenleitung `I2S_DIN` (Return-Audio vom Mesh).
  * Der On-Board Codec `ES8388` wird in diesem Modus per I2C schlafen gelegt (Power-Down, Ausgänge Hi-Z).

### 4.4 Backbone-Audio im OpenMotorBridge-Frameformat (Kein UAC / Kein USB-Switch)
* Der Pod agiert an der Zentralbox **nicht als Standard-USB-Audiogerät (UAC)**.
* Der gesamte Audio-Austausch (Microphone Upstream, Master-Mix Downstream) erfolgt in unserem **proprietären OpenMotorBridge-Frameformat** (`UsbAudioStreamUpPkt` / `USB_PKT_AUDIO_STREAM_UP` bzw. `USB_PKT_AUDIO_STREAM_DOWN`) über den regulären USB-Backbone-Endpoint des ESP32-C6.
* Dadurch meldet sich jeder Pod immer als **genau ein konsistentes USB-Device** an. Enumeration-Races und ALSA-Index-Vertauschungen sind ausgeschlossen.

### 4.5 Ladeanschluss J2 bleibt reiner Ladeport
* Der externe USB-C Port `J2` am Pod bleibt ein **reiner 30W USB-PD Ladeausgang** (`SW3516` Buck-Boost).
* Es werden **keine USB-Datenleitungen** auf `J2` geroutet, um Bus-Kurzschlüsse mit dem internen Backbone zu verhindern.

---

## 5. Checkliste für zukünftige Schaltungs- und Softwareänderungen

Vor der Freigabe jeder Hardware- oder Firmware-Änderung ist diese Checkliste verbindlich abzuarbeiten:

| Prüfpunkt | Kriterium | Bestanden? |
| :--- | :--- | :---: |
| **CP-01** | Ist der Zentralbox `ESP32-S31` weiterhin der einzige USB-Host auf dem internen Backbone? | [ ] |
| **CP-02** | Werden alle Satelliten (Front-Node, Pod L, Pod R, Radar) als reine USB-Clients am Hub `U8` betrieben? | [ ] |
| **CP-03** | Sind Front-Node Backbone-Client und Infotainment-Client galvanisch/elektrisch voneinander getrennt? | [ ] |
| **CP-04** | Schaltet der Front-Node Infotainment-Pfad via Hardware-Mux zwischen SkylineOS und Nachrüst-AA um? | [ ] |
| **CP-05** | Meldet sich der Pod mit genau einer eindeutigen USB-ID an (kein interner Hub, kein COTS-Soundchip)? | [ ] |
| **CP-06** | Schaltet der Pod-Bus-Switch `TMUX1574` Pins 4, 5, 7, 8 anhand von `OMM_DETECT` sauber zwischen Analog/PTT und I2S um? | [ ] |
| **CP-07** | Bleibt der Pod frei von eigenen BLE/2.4GHz-Sendern und Ladeport J2 frei von Datenleitungen? | [ ] |

---
**Genehmigt und festgehalten im Projekt OpenMotorBridge.**  
*Jede Abweichung erfordert ein Re-Engineering und eine Re-Validierung anhand dieses Dokuments.*

