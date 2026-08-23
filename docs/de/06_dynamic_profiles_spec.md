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
* **Midland G9 Pro, Baofeng/Kenwood 2-Pin K-Type, Motorola T82:** Hardware-PTT ueber PhotoMOS-Relais oder VOX-Schwellwertsteuerung.

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
