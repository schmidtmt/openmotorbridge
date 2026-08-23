# 06 - Dynamische Hardwareprofile (LittleFS JSON)

Die Profile liegen im LittleFS-Dateisystem unter `/profiles/` und definieren Audio-Gain, Rauschunterdrückung, Opto-Timing, DLE-Boni und RF-Hardening-Vorgaben.

## 1. Profil-Struktur

```json
{
  "id": "sena_apex_v1",
  "name": "Sena Apex / Apex Plus (Mesh 3.0)",
  "vendor": "Sena Technologies",
  "hardware_tier": 1,
  "vcc_enabled": true,
  "soft_start_ms": 120,
  "input_gain_db": 2.0,
  "output_gain_db": 0.0,
  "noise_gate_threshold_db": -46,
  "control_mode": "pulse_multilevel",
  "toggle_mesh_ms": 200,
  "channel_next_ms": 1000,
  "ptt_hold": false,
  "mesh_capabilities": {
    "protocol": "Sena_Mesh_3.0",
    "generation": 3,
    "max_nodes": 32,
    "open_mesh": true,
    "preconfig_channels": 9,
    "dle_bonus_score": 60
  },
  "rf_hardening": {
    "disable_bluetooth_classic": true,
    "clear_phone_gps_pairings": true,
    "enforce_mesh_only_mode": true,
    "disable_audio_multitasking": true,
    "expected_idle_current_ma": 45
  }
}

```

## 2. Unterstützte Kassetten-Profile
- sena_apex.json: Sena Apex / Apex Plus (Mesh 3.0, 32 Nodes, DLE +60 Pkt.).
- sena_legacy.json: Sena Spider / 50S / 30K (Mesh 2.0, 24 Nodes, DLE +30 Pkt.).
- cardo_dmc_gen2.json: Cardo Edge / Pro (DMC 2.0, 32 Nodes, Open DMC, DLE +60 Pkt.).
- cardo_dmc_legacy.json: Cardo Bold / Black (DMC 1.0, 15 Nodes, DLE +30 Pkt.).
- pmr446_gateway.json: Analogfunk VOX / PTT-Relay Profil.