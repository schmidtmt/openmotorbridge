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
│ **C3**  │ Sena 20S EVO, 10S, SF, SMH10  │ Bluetooth 4.1/2 │ **+20 points**  │
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

### Class 3: Sena Legacy & Bluetooth Intercom (`sena_legacy_bt.json`)
* **Sena 20S EVO, 30K, 10S, 10R, SF4/SF2, SMH10:** Jog-dial pulse timing for BT multi-hop, DLE +20 pts.

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

When a cartridge slot is empty, removed, or explicitly disabled in the WebApp dashboard, the ESP32-S3 instantly applies `disabled.json`:

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
