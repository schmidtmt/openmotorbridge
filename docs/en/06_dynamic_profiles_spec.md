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
* **Midland G9 Pro, Baofeng/Kenwood 2-Pin K-Type, Motorola T82:** Hardware PTT via PhotoMOS relay or VOX gate.

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
