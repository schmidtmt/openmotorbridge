# 06 - Dynamic Hardware Profiles (LittleFS JSON Specification)

Each plugged cartridge contains a Dallas DS2401 Silicon Serial Number read over 1-Wire. The ESP32-S3 uses this ID to dynamically load a tailored JSON profile from the internal `littlefs` partition (`/data/profiles/`).

## 1. JSON Profile Schema Definition

```json
{
  "profile_id": "sena_apex",
  "vendor": "Sena Technologies",
  "model": "Apex / Apex Plus (Mesh 3.0)",
  "hardware_tier": 1,
  "audio": {
    "input_gain_db": 2.0,
    "output_gain_db": 0.0,
    "noise_gate_threshold_db": -42.0
  },
  "opto_timings_ms": {
    "mesh_toggle_pulse": 200,
    "channel_next_pulse": 1000,
    "debounce_delay": 500
  },
  "rf_hardening": {
    "disable_bluetooth_classic": true,
    "force_mesh_only": true
  }
}
```

## 2. Standard Profile Catalog
- `sena_apex.json`: Sena Mesh 3.0 / 2.0 (Apex, 50S, 50R, Spider ST1/RT1).
- `cardo_dmc_gen2.json`: Cardo Dynamic Mesh Communication Gen2 (Packtalk Pro, Edge, Neo).
- `sena_legacy.json`: Sena 20S / 30K Bluetooth Classic Intercom.
- `cardo_dmc_legacy.json`: Cardo Packtalk Bold / Black DMC Gen1.
- `pmr446_gateway.json`: Midland G9 Pro / G13 PMR446 Analog Radio Gateway.
