# 06 - Class-Oriented Hardware Profiles & Cartridge Detection

OpenMotorBridge utilizes an extensible, class-oriented profile architecture based on **LittleFS JSON files** (`/profiles/*.json`) to automatically recognize, configure, and power-manage a broad spectrum of Sena, Cardo, and radio cartridges via the 1-Wire bus (`DS2401`).

---

## 1. Class-Oriented Hardware Hierarchy

All supported intercom and radio cartridges are structured into standardized hardware classes:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CLASS-ORIENTED HARDWARE PROFILE MATRIX                      │
├─────────┬───────────────────────────────┬─────────────────┬─────────────────┤
│ Class   │ Device Families               │ Mesh Protocol   │ DLE Score Bonus │
├─────────┼───────────────────────────────┼─────────────────┼─────────────────┤
│ **C1**  │ Sena 60S, Apex, 50S/R/C, SRL3 │ Sena Mesh 3.0/2 │ **+60 points**  │
│ **C2**  │ Sena Spider RT1/ST1           │ Mesh 2.0 Basic  │ **+40 points**  │
│ **C3**  │ Sena Vortex, 20S, 10S, SF, 5S │ Bluetooth 5.1/4 │ **+20 points**  │
│ **C4**  │ Cardo Edge, Pro, Custom, Neo  │ Cardo DMC Gen2  │ **+60 points**  │
│ **C5**  │ Cardo Freecom 4x/2x, Spirit HD│ Live Intercom   │ **+40 points**  │
│ **C6**  │ Cardo Bold, Black, Slim       │ Cardo DMC Gen1  │ **+30 points**  │
│ **C7**  │ Midland G9 Pro, Baofeng/UHF   │ PMR446 Analogue │ **+10 points**  │
│ **C0**  │ Disabled / Empty Slot         │ None            │ **0 points**    │
└─────────┴───────────────────────────────┴─────────────────┴─────────────────┘
```

---

## 2. Profile Overview in Filesystem (`/data/profiles/`)

### Class 1: Sena Next-Gen & High-Tier Mesh (`sena_60s.json`, `sena_apex.json`, `sena_50_series.json`)
* **Sena 60S (`sena_60s.json`):** Wave-Mesh intercom, up to 64 nodes, dual-chip RF-hardening.
* **Sena Apex / Apex Plus (`sena_apex.json`):** Mesh 3.0 reference cartridge, 32 nodes, DLE +60 pts.
* **Sena 50 Series & MeshPort (`sena_50_series.json`):** 50S, 50R, 50C, SRL3, MeshPort Blue/Red (Mesh 2.0/3.0, 24–32 nodes).

### Class 2: Sena Spider & Mesh-Only (`sena_spider.json`)
* **Sena Spider RT1 / ST1:** Dedicated mesh units without Bluetooth intercom overhead, DLE +40 pts.

### Class 3: Sena Bluetooth & 2-Way Intercom (`sena_vortex.json`, `sena_legacy_bt.json`)
* **Sena Vortex (`sena_vortex.json`):** Bluetooth 5.1 2-way intercom (1:1 up to 1.2 km), quick-pair button trigger, DLE +20 pts.
* **Sena 20S EVO, 30K, 10S, 10R, SF4/SF2, 5S, SMH10 (`sena_legacy_bt.json`):** Jog-dial pulse timing for BT multi-hop, DLE +20 pts.

### Class 4: Cardo Dynamic Mesh Communications Gen2 (`cardo_dmc_gen2.json`)
* **Cardo Packtalk Pro, Edge, Custom, Neo:** DMC Gen2 with Open DMC, fast auto-reconnect, and DLE +60 pts.

### Class 5: Cardo Live Intercom & Freecom Series (`cardo_freecom_live.json`)
* **Cardo Freecom 4x, Freecom 2x, Spirit HD:** Bluetooth 5.2 Live Intercom with auto-reconnect, DLE +40 pts.

### Class 6: Cardo Legacy DMC Gen1 (`cardo_dmc_legacy.json`)
* **Cardo Packtalk Bold, Black, Slim, Smartpack:** DMC 1.0 with up to 15 nodes, DLE +30 pts.

### Class 7: Universal Analogue & PMR446 Radio Cartridges (`pmr446_gateway.json`)
* **Midland XT Series (XT10/XT30/XT50 Bare-Board) & Embedded SA818S Transceivers:** Compact PMR446 cartridge modules (500 mW ERP, 446.0–446.2 MHz, 16 channels, CTCSS/DCS) for analogue group communications.
* **Midland G9 Pro / Baofeng / Kenwood 2-Pin K-Type:** External handheld radios connected via weatherproof dual-jack faceplate.
* **Hardware PTT:** Seamless transmit keying via PhotoMOS optocoupler (Toshiba TLP222A on Pin 5 `OPTO`) synchronized with handlebar PTT button or automatic DSP VOX.
* **Audio Isolation:** Galvanic decoupling via studio-grade transformer (Bourns LM-NP-1001) completely eliminates ground loops and alternator whine.

### Class 8: Midland Intercom & Wave Series (`midland_wave.json` / `midland_bt.json`)
* **Midland BTR1 Advanced, Rush RCF, BTX2 PRO S, Midland Wave, BT Mini:** Bluetooth 5.0/5.2 Intercom & Wave Mesh with digital audio pass-through and DLE +30 pts.

---

## 3. Safety Fallback: `disabled.json` (Slot Shutdown)

When a cartridge slot is empty, populated with a dummy blank, or disabled in the WebApp dashboard, the ESP32-S3 instantly applies `disabled.json`:

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

### Safety Features of `disabled.json`:
1. **Zero Power Draw (`vcc_enabled: false`):** Opens the P-FET power gate $\rightarrow$ 0.0 mA idle current.
2. **Audio Line Isolation:** Sets ES8388 codec input and output gain stages to $-96\,\text{dB}$, silencing line crosstalk and open-pin pickup.
3. **Trigger Deactivation:** Keeps Toshiba TLP222A PhotoMOS relays high-impedance.
4. **DLE Reset:** Drops DLE score contribution to 0 points.

---

## 4. Plug-and-Play Hardware Protection & Auto-Routing

To prevent wiring shorts or misconfigurations (e.g. plugging an audio cartridge into Pod 3 or the rear transceiver into Pod 1), cartridge onboarding operates in 3 distinct phases:

```
┌─────────────────────────────────────────────────────────────┐
│             3-PHASE PLUG-AND-PLAY ONBOARDING SEQUENCE       │
├─────────────────────────────────────────────────────────────┤
│ 1. DETECTION PHASE: 1-Wire ID query (Current limited < 20mA)│
│ 2. VALIDATION: Check family code & UID against profile table│
│ 3. ENABLING: Match verified -> 5V MOSFET ON & Audio/UART En │
└─────────────────────────────────────────────────────────────┘
```

1. **Current-Limited Detection Phase:** When inserted, the 5V main power MOSFET remains off. The 1-Wire driver queries the 64-bit DS2401 silicon serial number under minimal sensing current.
2. **Automatic Route Assignment:**
   * **Rear Pod 3 UID detected:** Host MCU switches pins 15/16 to High-Speed UART (@ 460,800 Baud) and initializes the NMEA/LoRa parser.
   * **Audio Cartridge (Sena/Cardo) detected:** Pins connect to Bourns audio paths and ES8388 DSP; matching JSON profile is loaded.
   * **Dummy Cartridge or Open-Pin detected:** Slot is maintained in zero-power isolation (`disabled.json`).
3. **Soft-Start Activation:** Once validated, the P-FET applies 5V power over a controlled soft-start ramp ($100-150\,\text{ms}$).

---

## 5. Buyer's Guide & Best-Practice Configurations by Budget and Group Setup

Depending on project budget, riding discipline, and whether the rider group relies primarily on Sena, Cardo, or a mixed ecosystem, the following cartridge setups are recommended:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 RECOMMENDED POD CARTRIDGE CONFIGURATIONS                    │
├───────────────────────┬─────────────────────────┬───────────────────────────┤
│ Setup Category        │ Pod 1 (Left Frame)      │ Pod 2 (Right Frame)       │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💎 **High-End Leader**│ **Sena 60S / Apex**     │ **Cardo Packtalk Edge**   │
│    (350 – 550 €)      │ (Mesh 3.0 Wave, C1)     │ (DMC Gen2 Air-Mount, C4)  │
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ ⚖️ **Best Value**     │ **Sena Spider RT1/ST1** │ **Cardo Freecom 4x / Bold**│
│    (180 – 280 €)      │ (Mesh 2.0 Pure, C2)     │ (Live Intercom/DMC, C5/C6)│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 💰 **Budget Starter** │ **Sena MeshPort Blue**  │ **IP67 Dummy Cartridge**  │
│    (80 – 140 €)       │ (or Sena 20S/SF, C3)    │ (Slot powered-off/disabled│
├───────────────────────┼─────────────────────────┼───────────────────────────┤
│ 🏔️ **Adventure/Offroad**│ **Sena Apex / 50S**   │ **Midland G9 Pro PMR446** │
│    (220 – 320 €)      │ (Mesh 3.0, C1)          │ (Analogue Radio, C7)      │
└───────────────────────┴─────────────────────────┴───────────────────────────┘
```

### 5.1 💎 High-End & DLE Leader Setup (Maximum Mesh & Future-Proofing)
* **Target Audience:** Tour guides, group road-captains, large mixed riding packs with state-of-the-art intercoms.
* **Recommended Hardware:**
  * **Pod 1:** *Sena 60S* or *Sena Apex* (Wave Mesh 3.0, 64 nodes, DLE +60 pts)
  * **Pod 2:** *Cardo Packtalk Pro* or *Packtalk Edge* (DMC Gen2, Air Mount, DLE +60 pts)
* **Key Benefit:** Full $120\,\text{points}$ gateway bonus (auto-elected DLE Group Leader), studio-grade audio quality, $< 8\,\text{ms}$ bridge latency.

### 5.2 ⚖️ Best Value / "Sweet Spot" (The Universal Everyday All-Rounder)
* **Target Audience:** Motorcycle friend groups with a split mix of Sena and Cardo riders.
* **Recommended Hardware:**
  * **Pod 1:** *Sena Spider RT1 / ST1* (Pure mesh without Bluetooth intercom overhead, approx. $120-140\,\text{€}$ new / $85\,\text{€}$ used, DLE +40 pts)
  * **Pod 2:** *Cardo Freecom 4x* or used *Cardo Packtalk Bold (DMC Gen1)* (approx. $100-140\,\text{€}$, DLE +40/+30 pts)
* **Key Benefit:** Complete, full-duplex cross-mesh bridge bridging Sena Mesh and Cardo DMC for under $250\,\text{€}$ total investment.

### 5.3 💰 Budget & Phased Entry (Affordable Start, Upgrade Anytime)
* **Target Audience:** Budget-conscious riders, solo riders with occasional pillion use, or single-brand groups.
* **Recommended Hardware:**
  * **Pod 1:** *Sena MeshPort Blue* or used *Sena 20S / 10S / SF4* (approx. $45-65\,\text{€}$ used, DLE +20/+40 pts)
  * **Pod 2:** **IP67 Dummy Cartridge (`Pod_Dummy_Cartridge_IP67.stl`)** $\rightarrow$ Dual O-ring sealed and electrically isolated via `disabled.json` ($0.0\,\text{mA}$).
* **Key Benefit:** Minimal upfront cost ($< 100\,\text{€}$). Slot 2 remains ready for instant tool-free plug-and-play expansion later.

### 5.4 🏔️ Adventure, Offroad & Desert Expeditions (Cellular & Bluetooth Range Independent)
* **Target Audience:** Trans-Euro-Trail (TET), remote alpine passes, and wilderness expeditions with zero cellular reception.
* **Recommended Hardware:**
  * **Pod 1:** *Sena Apex* or *Sena 50S* (Local group mesh)
  * **Pod 2:** *Midland G9 Pro / Baofeng PMR446 Cartridge* (Analogue 446 MHz long-range radio gateway)
  * **Pod 3 (Rear):** *Dual-PHY OpenMotorMesh (868 MHz LoRa Fallback)* for up to $15\,\text{km}$ emergency PTT and group radar.

---

## 6. Dynamic Profile Update & Merge Engine (WebApp / Mesh 3.0 Sync)

When an intercom manufacturer (e.g. Sena upgrading from Mesh 2.0 to Mesh 3.0, or Cardo introducing DMC Gen 2) releases updated firmware, OpenMotorBridge dynamically adapts using an intelligent **JSON Merge Engine**:

```
┌─────────────────────────────────────────────────────────────┐
│                 JSON PROFILE MERGE ENGINE                   │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Upstream Base Profile     │ 2. Custom User-Configured    │
│    (e.g. sena_apex_v3.json)  │    Offsets (Ducking & Gains) │
├──────────────────────────────┴──────────────────────────────┤
│                             ▼                               │
│ 3. Merged Live Runtime Profile in LittleFS Flash Storage    │
│    (Updated Opto Timings + Preserved Personal Audio Gains)  │
└─────────────────────────────────────────────────────────────┘
```

### The 3 Phases of Profile Merging:
1. **Base Parameters:** New optocoupler pulse durations (e.g. `ptt_pulse_ms: 180`), updated channel switching sequences (`[1000, 300, 200]`), and DLE score bonuses are imported from the new vendor JSON.
2. **User-Settings Preservation:** Custom rider adjustments (e.g. $+2.0\,\text{dB}$ microphone gain, $-12\,\text{dB}$ navi ducking attenuation) are preserved and merged cleanly over base defaults.
3. **Hot-Reload:** Central Box immediately applies merged parameters at runtime to the ES8388 codec and TLP222A opto-sequencer without requiring a system reboot.

---

## 7. WebApp Workflow: Automatic Detection & Initial Assignment of New Cartridge UIDs

When a rider builds or plugs in a new cartridge carrier PCB with a factory-fresh DS2401 chip, the OpenMotorBridge WebApp/PWA initiates a streamlined onboarding dialogue:

```
┌─────────────────────────────────────────────────────────────┐
│ 🧩 NEW CARTRIDGE DETECTED!                                  │
├─────────────────────────────────────────────────────────────┤
│ Detected Slot:          Pod 1 (Frame Left)                  │
│ 1-Wire Chip UID:        01:A2:3B:4C:5D:6E:7F:8A             │
├─────────────────────────────────────────────────────────────┤
│ This cartridge hardware has not yet been assigned a profile.│
│ Which intercom model is installed?                          │
│                                                             │
│ Hardware Profile:  [ 🔵 Sena 50S / 50R / SRL3 (K1)      ▼ ] │
├─────────────────────────────────────────────────────────────┤
│ [ Assign Later ]                 [ Assign & Save Profile ]  │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Workflow:
1. **Automatic Scan:** The ESP32-S3 polls both 1-Wire ports every 2 seconds (`task_cartridge_manager`). When detecting a presence pulse with valid CRC8 and family code `0x01` (DS2401), it transmits the 64-bit UID via BLE telemetry to the WebApp.
2. **Dialogue Pop-up:** The WebApp checks the UID against the persistent mapping table (`/profiles/mapping.json` / PWA `localStorage`). If the UID is new, the assignment modal (`#uuid-detect-modal`) opens automatically.
3. **Profile Selection & Storage:** The rider selects the installed hardware model (e.g. *Sena 50S*, *Cardo Packtalk Edge*, *PMR446*) and clicks "Assign & Save".
4. **Persistent Mapping:** The mapping `{"<UID>": "<profile_id>"}` is stored permanently in the ESP32 LittleFS and browser storage.
5. **Seamless Re-identification:** In the future, plugging this cartridge into either Pod 1 or Pod 2 automatically identifies, parameterizes, and includes it in DLE Gateway calculations without prompts.

---

### 7.1 Zero-Trust Hardware Quarantine (Fail-Safe Inrush Protection)

> [!CAUTION]
> **Electronics Safety Principle:** As long as an inserted cartridge hardware (DS2401 UID) has not been confirmed with a verified profile, the slot is **treated strictly as an unseated or invalid slot**:
> 1. **5V VCC Power-Gate OFF (0.0 mA):** The P-channel high-side switch to the OEM cradle remains completely off. The intercom receives zero operating power.
> 2. **Audio DSP Mute (-96 dB):** Both audio channels (input & output) on the ES8388 codec are muted in hardware and software to prevent pops, noise, or crosstalk.
> 3. **Optocouplers High-Z (OFF):** TLP222A relays for PTT and button triggers remain open.
> 4. **DLE Gateway Bonus = 0:** Unconfirmed hardware is excluded from DLE gateway score calculation.
> 
> **Only when the rider confirms the profile in the WebApp** (or the UID is already stored in the flash mapping), the controller executes a controlled soft-start sequence (50 ms inrush-current limiting) and un-mutes audio paths.

---

### 7.2 Hardware Upgrade & OEM Adapter Updates (Replacing Headsets in Existing Cartridges)

A common real-world scenario: over time, a rider upgrades their intercom hardware—for example, removing an older Sena 20S or Cardo Freecom from the 3D-printed enclosure and replacing it with a flagship device (e.g. Sena 60S Mesh 3.0 Wave or Cardo Packtalk Pro / Edge DMC Gen2), while keeping the universal cartridge carrier PCB (`openmotorbridge_pod_cartridge`) with its DS2401 ID chip.

#### Persistent UID Re-mapping Principle:
1. **Unchanged Chip UID:**
   Because the DS2401 silicon serial number chip is soldered onto the carrier PCB, the upgraded cartridge retains its factory 64-bit hardware UID (e.g. `01:4F:2A:90:12:00:8C`).
2. **Immediate Selection in Dashboard:**
   In the **„🧩 Cartridges & DLE“** tab of the WebApp, the rider simply chooses the newly installed model from the dropdown (e.g. *„⚡ Sena 60S (Mesh 3.0 Wave)“*).
3. **Automatic Overwrite of the Mapping Table:**
   Selecting the new profile in the dropdown **immediately and automatically** updates the persistent mapping table:
   ```json
   {
     "01:4F:2A:90:12:00:8C": "sena_60s"
   }
   ```
   This entry is permanently saved in browser storage (`localStorage`) and synchronized to the ESP32 LittleFS (`/profiles/mapping.json`).
4. **Behavior Upon Removal & Re-insertion:**
   When the cartridge is subsequently removed, swapped to another slot, or the motorcycle is restarted weeks later:
   * The 1-Wire bus reads the UID `01:4F:2A:90:12:00:8C`.
   * The mapping table returns **`sena_60s`** (the previous legacy profile is overwritten).
   * **The new profile is reliably and automatically loaded**—applying the updated optocoupler pulses, audio gains, and the higher DLE Mesh 3.0 score bonus (+60 pts).
5. **Ground-Truth Re-Sync (`🔄 Sync`):**
   The rider can click the Sync button at any time to verify which profile in flash storage corresponds to the physical UID currently seated in the slot, or use **`🧩 Learn UUID`** to interactively reconfigure the mapping.

---

## 8. Taxonomy of OEM Adapter Interfacing: Connection Classes & Wiring Matrix

OpenMotorBridge accommodates a wide spectrum of commercial off-the-shelf OEM headsets, handheld radios, and wireless bridge dongles without requiring users to open, modify, or desolder devices. To maintain clean universal plug-and-play modularity, the system classifies all OEM hardware into **5 standardized connection classes**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   OVERVIEW OF THE 5 OEM ADAPTER CONNECTION CLASSES                     │
├───────────────────┬─────────────────────────────┬──────────────────────────────────────┤
│ Adapter Class     │ Typical Hardware Models     │ Interfacing & Connection Scheme      │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Class A:**      │ Sena +Mesh (B2M-01),        │ • Switched 5V power only (90° Micro- │
│ Wireless Bridge   │ Sena MeshPort Blue / Red,   │   USB / USB-C) from J2 (Pins 1 & 2)  │
│ (Power-Only / USB)│ Cardo Packtalk Outdoor USB  │ • Audio routed wirelessly via BT     │
│                   │                             │ • External SMA bulkhead double-jack  │
│                   │                             │ • Mechanics: OEM slide-mount & strap │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Class B:**      │ Sena 50S, 60S, 30K,         │ • Full analog stereo (Audio In & Out)│
│ Pogo-Pin Clamps   │ Sena 20S EVO, SRL3          │ • 6-conductor ribbon from J2 to pogo │
│ (Spring-Pin Array)│                             │   array on contour nest              │
│                   │                             │ • TLP222A PTT synthesis (Pin 6)      │
│                   │                             │ • Mechanics: Click-in cradle nest    │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Class C:**      │ Cardo Packtalk Edge,        │ • Full analog stereo (Audio In & Out)│
│ Magnetic Air-Mount│ Cardo Packtalk Pro,         │ • 5-pad spring-contact array in nest │
│                   │ Cardo Packtalk Neo          │ • Dual N52 Neodymium guidance magnets│
│                   │                             │   for tool-free magnetic latching    │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Class D:**      │ Cardo Packtalk Bold / Black,│ • Full analog stereo (Audio In & Out)│
│ Slide Cradle      │ Cardo Freecom 1 / 2 / 4+    │ • Lateral wiping contacts in cradle  │
│                   │                             │ • Mechanics: Slide rail with latch   │
├───────────────────┼─────────────────────────────┼──────────────────────────────────────┤
│ **Class E:**      │ Midland G7 / G9 Pro, G13,   │ • 2-Pin dual audio jack (2.5mm+3.5mm)│
│ Analogue Radio    │ Midland XT30, Baofeng,      │ • Opto-PTT keys transmitter to ground│
│ (PMR446 / Kenwood)│ Kenwood TK Series           │ • 5V DC/DC regulator (battery dummy) │
│                   │                             │ • Fixed 446MHz helix or SMA front jack│
└───────────────────┴─────────────────────────────┴──────────────────────────────────────┘
```

### 8.1 Detailed Pinout of Cartridge Header (`J2`) Across Adapter Classes

The 6-pin **JST-SH 1.0 mm header (`J2`)** on the universal cartridge carrier PCB (`openmotorbridge_pod_cartridge`) distributes all power, audio, and synthesis lines. The appropriate pre-crimped inlay harness plugs directly into `J2`:

| Pin | Signal | Class A (e.g. +Mesh) | Class B (e.g. Sena 50S) | Class C (e.g. Cardo Edge)| Class E (PMR446 Radio) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | `GND` | Micro-USB Pin 5 (GND) | Pogo-Pin 1 (GND) | Air-Mount Pad 1 (GND) | Jack shield / Ground |
| **2** | `5V_VBUS` | Micro-USB Pin 1 (+5V) | Pogo-Pin 2 (5V Charge)| Air-Mount Pad 2 (5V Charge)| Battery dummy 5V In |
| **3** | `AUDIO_R+` | *N/C (Pure BT Audio)* | Pogo-Pin 4 (Spk R+) | Air-Mount Pad 3 (Spk +)| Jack Speaker + |
| **4** | `AUDIO_R-` | *N/C (Pure BT Audio)* | Pogo-Pin 5 (Spk R-) | Air-Mount Pad 4 (Spk -)| Jack Speaker - |
| **5** | `MIC_IN+` | *N/C (Pure BT Audio)* | Pogo-Pin 6 (Mic +) | Air-Mount Pad 5 (Mic +)| Jack Microphone + |
| **6** | `OPTO_PTT` | *N/C* | Pogo-Pin 7 (Mesh-Btn)| *N/C* (Aux) | PTT trigger to ground |

---

### 8.2 RF and Antenna Concepts Across Hardware Enclosures

1. **Adapters with External Antenna Sockets (e.g. Sena +Mesh, PMR446 Radios):**
   * **Front Bulkhead Double-Jack:** A waterproof SMA flange bulkhead (with silicone O-ring) is mounted on the cartridge faceplate.
   * **Internal Pigtail:** A short, flexible RG178 coaxial pigtail connects the internal bulkhead to the antenna port of the OEM device (maintaining bend radius $R \ge 12\,\text{mm}$).
   * **Optional External Aerial:** Riders can screw on an ultra-compact 2.4 GHz stub antenna ($25\dots 30\,\text{mm}$) directly, or connect a low-loss cable to a high-gain antenna on the windshield or tail.
   * **Protective Cap:** When unused, a waterproof silicone cap or threaded brass O-ring plug seals the port to IP67.
2. **Adapters with Integrated Folding Antennas (e.g. Sena 50S / 60S):**
   * The open-top sled design provides the full $28.0\,\text{mm}$ clearance height, allowing factory folding antennas to be deployed inside the chamber without interfering with the pod ceiling.
3. **Adapters with Internal Chip Antennas (e.g. Cardo Packtalk Edge DMC Gen2):**
   * RF radiation passes through the high-grade PA12 plastic enclosure virtually unattenuated ($\le 0.4\,\text{dB}$ insertion loss at 2.4 GHz), requiring zero external perforations.



