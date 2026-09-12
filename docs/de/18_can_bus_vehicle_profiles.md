# 18 - Fahrzeug-CAN-Bus-Profile, DBC-JSON-Schema & Universal Telemetrie-Engine

## 1. Problemstellung & Systemüberblick

Moderne Motorräder verfügen über digitale Datenbusse (ISO 11898-2 CAN-Bus, CAN-FD oder LIN), über die Motorsteuergerät (ECU), ABS-/Traktionssystem, Cockpit-Instrumente und Lenkerarmaturen miteinander kommunizieren. Für ein herstellerübergreifendes System wie **OpenMotorBridge** existiert jedoch keine einheitliche Schnittstelle:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               HERSTELLERSPEZIFISCHE CAN-BUS HETEROGENITÄT IM MOTORRAD                  │
└────────────────────────────────────────────────────────────────────────────────────────┘

  Hersteller / Plattform         Baudrate    CAN-ID Format     Besonderheiten
  ────────────────────────────────────────────────────────────────────────────────────────
  Harley-Davidson (HD-LAN / CVO) 500 kbps    11-Bit & 29-Bit   Lenker-Joysticks, BCM-Heartbeats, TPMS
  BMW Motorrad (K2x / K5x / K6x) 500 kbps    11-Bit Standard   Wonderwheel-Drehrad, RDC-Druck, Fahrmodi
  KTM / Husqvarna (Bosch CAN)    500 kbps    11-Bit Standard   Schräglagensensorik, MTC, ABS-Status
  Ducati (Bosch / Mitsubishi)    500 kbps    11-Bit Standard   DTC, DQS-Schaltautomat, D-Air Airbag
  Generisch (Euro 4 / Euro 5)    500 kbps    11-Bit (OBD-2)    Standard-PIDs nach ISO 15765-4
```

### Die OpenMotorBridge Lösung: Das Kassetten-Prinzip für den CAN-Bus

Analog zu unserem bewährten **Kassetten-Profilmanager für Intercom-Module** (Sena, Cardo etc. in [Spezifikation 02](file:///Users/schmidtm/openMotorBridge/docs/de/02_intercom_matrix_profiles.md)) implementiert OpenMotorBridge eine **dynamische CAN-Profil-Engine**:
1. Sämtliche herstellerspezifischen CAN-Definitionen liegen als **schlanke JSON-Dateien im internen LittleFS-Flash** (`/data/can_profiles/*.json`).
2. Die Firmware enthält **keine fest einprogrammierten Hersteller-Sonderlocken** mehr, sondern parst eingehende Frames rein datengetrieben über ein hardwarebeschleunigtes Bit-Extraktions-Gitter.
3. Der Fahrer kann sein Modell entweder in der **PWA unter Tab 5 auswählen**, oder OpenMotorBridge erkennt das Motorrad vollautomatisch über einen **passiven 500-ms-Bus-Fingerprint**.

---

## 2. LittleFS CAN-Profil JSON-Schema (`can_profile_schema_v1.json`)

Jedes Fahrzeugprofil definiert die physikalischen Bus-Parameter sowie ein Feld von Signalen mit Bit-Start, Länge, Endianness, Skalierungsfaktor und Wertebereich:

```json
{
  "schema_version": 1,
  "profile_id": "harley_skyline_2024",
  "manufacturer": "Harley-Davidson",
  "model_family": "Touring & CVO (2024+ Skyline OS)",
  "bus_config": {
    "baudrate_kbps": 500,
    "listen_only": true,
    "termination_120r": true,
    "auto_recovery": true
  },
  "fingerprint": {
    "characteristic_can_ids": ["0x280", "0x290", "0x380"],
    "min_frame_count": 10
  },
  "signals": {
    "speed_kmh": {
      "can_id": "0x280",
      "is_extended": false,
      "start_bit": 16,
      "length_bits": 16,
      "endianness": "little",
      "scale": 0.0625,
      "offset": 0.0,
      "min": 0.0,
      "max": 299.0,
      "unit": "km/h"
    },
    "engine_rpm": {
      "can_id": "0x200",
      "is_extended": false,
      "start_bit": 0,
      "length_bits": 16,
      "endianness": "little",
      "scale": 1.0,
      "offset": 0.0,
      "min": 0.0,
      "max": 9000.0,
      "unit": "rpm"
    },
    "gear_selected": {
      "can_id": "0x280",
      "is_extended": false,
      "start_bit": 32,
      "length_bits": 4,
      "endianness": "little",
      "scale": 1.0,
      "offset": 0.0,
      "enum_mapping": {
        "0": "N",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "15": "Error/Clutch"
      }
    },
    "engine_temp_c": {
      "can_id": "0x380",
      "is_extended": false,
      "start_bit": 0,
      "length_bits": 8,
      "endianness": "little",
      "scale": 1.0,
      "offset": -40.0,
      "unit": "°C"
    },
    "fuel_remaining_liters": {
      "can_id": "0x400",
      "is_extended": false,
      "start_bit": 8,
      "length_bits": 8,
      "endianness": "little",
      "scale": 0.1,
      "offset": 0.0,
      "unit": "l"
    },
    "fuel_range_km": {
      "can_id": "0x400",
      "is_extended": false,
      "start_bit": 16,
      "length_bits": 16,
      "endianness": "little",
      "scale": 1.0,
      "offset": 0.0,
      "unit": "km"
    },
    "tire_pressure_front_bar": {
      "can_id": "0x420",
      "is_extended": false,
      "start_bit": 0,
      "length_bits": 8,
      "endianness": "little",
      "scale": 0.025,
      "offset": 0.0,
      "unit": "bar"
    },
    "tire_pressure_rear_bar": {
      "can_id": "0x420",
      "is_extended": false,
      "start_bit": 8,
      "length_bits": 8,
      "endianness": "little",
      "scale": 0.025,
      "offset": 0.0,
      "unit": "bar"
    },
    "turn_indicator": {
      "can_id": "0x290",
      "is_extended": false,
      "start_bit": 0,
      "length_bits": 2,
      "endianness": "little",
      "enum_mapping": {
        "0": "off",
        "1": "left",
        "2": "right",
        "3": "hazard"
      }
    },
    "brake_front_active": {
      "can_id": "0x280",
      "is_extended": false,
      "start_bit": 40,
      "length_bits": 1,
      "endianness": "little"
    },
    "brake_rear_active": {
      "can_id": "0x280",
      "is_extended": false,
      "start_bit": 41,
      "length_bits": 1,
      "endianness": "little"
    },
    "handlebar_voice_btn": {
      "can_id": "0x290",
      "is_extended": false,
      "start_bit": 16,
      "length_bits": 1,
      "endianness": "little"
    },
    "handlebar_joystick_left": {
      "can_id": "0x290",
      "is_extended": false,
      "start_bit": 17,
      "length_bits": 1,
      "endianness": "little"
    },
    "handlebar_joystick_right": {
      "can_id": "0x290",
      "is_extended": false,
      "start_bit": 18,
      "length_bits": 1,
      "endianness": "little"
    },
    "handlebar_joystick_click": {
      "can_id": "0x290",
      "is_extended": false,
      "start_bit": 19,
      "length_bits": 1,
      "endianness": "little"
    }
  }
}
```

---

## 3. Die Referenz-Profile im Auslieferungszustand

Die Firmware liefert ab Werk vorkonfigurierte Profile für die gängigsten Fahrzeugplattformen aus:

### 3.1 Harley-Davidson HD-LAN / Skyline OS (`harley_skyline_2024.json`)
* **Plattformen:** Road Glide (FLTRX), Street Glide (FLHX), CVO Touring ab 2023.5 / 2024.
* **Besonderheiten:** 
  * Direkter Abgriff der Daumen-Joysticks am linken und rechten Lenkerschalter (`0x290`: Track Next, Prev, Click).
  * Infotainment-Quellenfilterung (`0x388`: `infotainment_source_active`) verhindert Geister-Streaming bei lokalem MP3-Stick / Radio.
  * BCM Alarmanlagen-Überwachung (`0x390`: `bcm_alarm_triggered`) für stillen LoRa 868 MHz Diebstahlalarm.
  * Reifendruck-Überwachung (TPMS) beider Räder in 0,025-bar-Schritten.
  * Tacho- und Drehzahlübertragung für den dead-reckoning EKF-Tunnelnavigationsfilter.

### 3.2 BMW Motorrad K5x / K6x (`bmw_motorrad_k5x_r1250_r1300.json`)
* **Plattformen:** R 1250 GS / R 1300 GS, R 1250 RT, S 1000 XR, F 900 GS ab Modelljahr 2018.
* **Besonderheiten:**
  * **Wonderwheel Multi-Controller:**
    * Drehimpulse vor/zurück (CAN-ID `0x2A0`, Byte 1).
    * Kippen links/rechts (CAN-ID `0x2A0`, Byte 2, Bit 0/1).
  * **RDC Reifendruck:** Temperaturkompensierte Druckwerte vorne und hinten (CAN-ID `0x2D0`).
  * **Fahrwerks- & Bremsdaten:** Raddrehzahlen von Vorder- und Hinterrad (CAN-ID `0x130`).

```json
{
  "profile_id": "bmw_motorrad_k5x_r1250_r1300",
  "manufacturer": "BMW Motorrad",
  "model_family": "R 1250 / R 1300 GS & RT Platform",
  "bus_config": {
    "baudrate_kbps": 500,
    "listen_only": true,
    "termination_120r": true
  },
  "signals": {
    "wonderwheel_scroll": { "can_id": "0x2A0", "start_bit": 8, "length_bits": 8, "endianness": "little", "scale": 1.0, "offset": 0.0, "unit": "clicks" },
    "wonderwheel_tilt_left": { "can_id": "0x2A0", "start_bit": 16, "length_bits": 1, "endianness": "little" },
    "wonderwheel_tilt_right": { "can_id": "0x2A0", "start_bit": 17, "length_bits": 1, "endianness": "little" },
    "tire_pressure_front_bar": { "can_id": "0x2D0", "start_bit": 16, "length_bits": 8, "endianness": "little", "scale": 0.02, "offset": 0.0, "unit": "bar" },
    "tire_pressure_rear_bar": { "can_id": "0x2D0", "start_bit": 24, "length_bits": 8, "endianness": "little", "scale": 0.02, "offset": 0.0, "unit": "bar" },
    "ambient_temp_c": { "can_id": "0x2D0", "start_bit": 0, "length_bits": 8, "endianness": "little", "scale": 0.5, "offset": -40.0, "unit": "°C" }
  }
}
```

### 3.3 Universelles Euro-4 / Euro-5 OBD2-Profil (`generic_obd2_iso15765.json`)
* **Plattformen:** Alle Motorräder mit standardisiertem roten 6-Pin Euro-5 OBD-Stecker (KTM, Yamaha, Kawasaki, Honda, Triumph, Suzuki).
* **Funktion:** Fragt standardisierte PIDs zyklisch ab (Drehzahl `0x0C`, Geschwindigkeit `0x0D`, Kühlmitteltemperatur `0x05`, Tankfüllstand `0x2F`).

---

## 4. Sicherheits- & Entkopplungs-Architektur (Automotive Safety)

Da der CAN-Bus eines Motorrads sicherheitskritische Steuergeräte (ABS-Modulator, Ride-by-Wire Drosselklappe, Traktionskontrolle) verbindet, gilt für OpenMotorBridge das oberste Sicherheitsgebot:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               CAN-BUS SICHERHEITS- UND ISOLATIONS-PRINZIPIEN                           │
└────────────────────────────────────────────────────────────────────────────────────────┘

  1. LISTEN-ONLY MODUS (ISO 11898-2)
     • Der TI TCAN334G Transceiver schaltet den TX-Treiber standardmäßig stromlos.
     • OpenMotorBridge erzeugt kein einziges ACK-Bit und kein Error-Frame.
     • Völlig unsichtbar für die Motorrad-Elektronik; Fehlerspeicher bleibt 100 % sauber.

  2. AUTOMATIC BUS-OFF RECOVERY
     • Bei Leitungsstörungen (z. B. Wackelkontakt) trennt der ESP32 TWAI-Controller den Bus
       in < 1 Millisekunde ab und führt erst nach 1.000 ms Ruhezeit einen Kaltstart durch.

  3. FAHRZEUG-MASSENTRENNUNG & DUAL-NODE ARCHITEKTUR
     • Sowohl auf der Zentralbox (PCBA 01) als auch auf dem Front-Knoten (PCBA 05) schützt das
       gefilterte Masse- und Schutznetzwerk des TI TCAN334G Transceivers gegen fahrzeugweiten
       Masseversatz zwischen Heck und Cockpit.
     • Das elektronische Solid-State Relais (CPC1017N) garantiert zudem eine automatische
       120-Ohm-Abschlussimpedanz-Erkennung und verhindert Bus-Kollaps bei Parallelschaltung.

  4. SOURCE-AWARE HANDLEBAR GATING (KOLLISIONSSCHUTZ)
     • Um zu verhindern, dass Lenkertasten bei Radio- oder MP3-Stick-Wiedergabe versehentlich
       parallel das Smartphone-Streaming starten, wertet OMB die aktive Audioquelle
       (z. B. 0x388 `infotainment_source_active`) und den USB2514B Hub-Status (Port 3 Sense) aus.
     • Events werden nur an das Smartphone durchgereicht, wenn OMB/CarPlay/BT aktiv ist!
```

---

## 5. WebApp-Workflow: Profilverwaltung & Live-Monitor (PWA Tab 5)

In der OpenMotorBridge PWA (Tab 5 *Hardware & Settings*) erhält der Fahrer ein mächtiges Cockpit-Tool:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CAN-BUS PROFIL-MANAGER & LIVE-MONITOR                           │
└────────────────────────────────────────────────────────────────────────────────────────┘

  Fahrzeugprofil: [ 🏍️ Harley-Davidson Touring (2024+ Skyline OS)                     ▼ ]
  
  Status: 🟢 VERBUNDEN (500 kbps, Listen-Only, 142 Frames/s)
  [ 🔍 Bus automatisch scannen ]   [ 📥 Profil importieren ]   [ 🔄 Auf Werkseinstellung ]

  LIVE-TELEMETRIE AUS DEM MOTORRAD-BUS:
  ┌─────────────────────────────────┬─────────────────────────────────┬──────────────────┐
  │ Raddrehzahl:       54.2 km/h    │ Motordrehzahl:      2.420 U/min │ Gang:       4    │
  │ Reifendruck Vorn:  2.45 bar 🟢  │ Reifendruck Hinten: 2.80 bar 🟢 │ Tank:  14.2 Liter│
  │ Kühlmitteltemp:    88 °C 🟢     │ Restreichweite:     240 km      │ Blinker:    Aus  │
  └─────────────────────────────────┴─────────────────────────────────┴──────────────────┘

  INTERAKTIVER LENKERTASTER-TEST:
  • Joystick Links: [ INAKTIV ]  • Joystick Rechts: [ INAKTIV ]  • Voice-Taste: [ GEDRÜCKT 🟢 ]
```

1. **Auto-Scan & Fingerprinting:**
   * Ein Klick auf `🔍 Bus automatisch scannen` lässt den ESP32 für 500 ms lauschen.
   * Ergleicht empfangene CAN-IDs mit den `characteristic_can_ids` aller im LittleFS gespeicherten Profile ab.
   * Erkennt er z. B. `0x280` und `0x290`, schlägt er sofort vor: *„Harley-Davidson 2024+ erkannt. Profil aktivieren?“*
2. **Community-Profile & JSON-Import:**
   * Neue Motorradmodelle erfordern **kein Firmware-Update**.
   * Jeder Nutzer kann eine einfache JSON-Datei in die PWA hochladen oder per QR-Code mit Freunden teilen.
3. **Optischer Lenkertaster-Test:**
   * Drückt man am Lenker den Joystick oder die Sprechtaste, leuchtet das entsprechende Symbol in der PWA sofort grün auf – perfekte Funktionsprüfung ohne Diagnosegerät!

---

---

## 6. Automatische Sensor-Fusion: Trägheitsnavigation (ADR-EKF) mit CAN-Raddrehzahl

Ein herausragendes Alleinstellungsmerkmal von OpenMotorBridge ist die **unterbrechungsfreie Tunnelführung (Automotive Dead Reckoning, ADR)** über das 15-Zustands-Extended-Kalman-Filter (`adr_ekf_filter.cpp`):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               DYNAMISCHE CAN-SIGNALABFRAGE IM KALMAN-FILTER (ADR-EKF)                  │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [CAN-PROFIL-MANAGER]
  • Prüft aktives Profil: can_profile_has_signal("speed_kmh" | "wheel_speed_rear")
           │
           ├──► JA (Signal im Profil definiert & empfangen):
           │    • EKF-Modus: HOHE KONFIDENZ (R_speed = 0.05 m²/s²)
           │    • Distanzfortschreibung: ds = v_can * dt
           │    • Drift im 2.500-m-Tunnel: < 1.5 m (Kein Beschleunigungs-Drift!)
           │    • Schlupferkennung bei BMW (v_rear vs. v_front)
           │    • Zentripetal-Schräglagenkompensation: theta = atan(v_can * yaw_rate / g)
           │
           └──► NEIN (Naked Bike ohne CAN-Bus oder Signal fehlt):
                • EKF-Modus: AUTOMATISCHER FALLBACK (IMU Dead Reckoning)
                • Distanzfortschreibung: Doppel-Integration von a_x (IMU)
                • Barometer-Höhenstützung & Stillstandserkennung (Zero Velocity Update, ZUPT)
```

### Die Vorteile der dynamischen Parameterabfrage:

1. **Dynamische Messrauschen-Adaption ($R$-Matrix):**
   * Wenn das CAN-Profil meldet, dass eine echte Raddrehzahl (z. B. Harley `0x280` oder BMW `0x130`) vorhanden ist, schaltet das EKF-Filter die Messunsicherheit der Vorwärtsgeschwindigkeit von $0{,}80\,\text{m}^2/\text{s}^2$ (IMU-Schätzung) auf **$0{,}02\,\text{m}^2/\text{s}^2$ (präziser ABS-Sensor)** um.
   * Der gefürchtete exponentielle Drift der Doppel-Integration von Beschleunigungswerten ($s = \frac{1}{2} a t^2$) wird vollständig eliminiert!
2. **Schräglagen-Validierung in Echtzeit:**
   * In schnellen Kurven kompensiert der EKF die Fliehkraft auf die IMU mit dem physikalischen Modell $\theta = \arctan\left(\frac{v_{\text{can}} \cdot \dot{\psi}}{g}\right)$.
   * Mit präziser CAN-Raddrehzahl ist die Schräglagenberechnung absolut immun gegen Fahrbahnunebenheiten und Kurvenschlaglöcher.
3. **PWA-Statusanzeige:**
   * Der Fahrer sieht in der PWA sofort, welche Datenquelle aktiv ist:
     * 🟢 `ADR Source: CAN Wheel Speed (0.06 km/h Res, 50 Hz)`
     * 🟡 `ADR Source: IMU Inertial Integration (Estimated)`

---

## 7. Zusammenfassung & Mehrwert

| Kriterium | Herkömmliche Zubehör-Systeme | OpenMotorBridge CAN-Profil-Engine |
| :--- | :--- | :--- |
| **Hersteller-Kompatibilität** | Oft nur für eine einzige Marke | **Universell (Harley, BMW, KTM, Ducati, OBD2)** |
| **Anpassbarkeit** | Fest in C-Code einprogrammiert | **Dynamische JSON-Dateien im LittleFS Flash** |
| **Sicherheit** | Sendet störende Frames auf den Bus | **100 % passiver Listen-Only Modus (TÜV-sicher)** |
| **Lenkerbedienung** | Nur eigene, klobige Plastiktaster | **Originale Motorrad-Lenkertaster & Wonderwheel** |
| **Telemetrie-Tiefe** | Nur GPS-Geschwindigkeit | **Echter Reifendruck, Motortemperatur, Tank, Bremsdruck** |
| **EKF-Trägheitsnavigation** | Blind bei GNSS-Verlust | **Präzise Tunnel-Stützung über CAN-Raddrehzahl (< 1,5 m Drift)** |
| **Updates** | Nur über komplettes Firmware-Flashen | **Einfaches Hochladen neuer JSON-Profile per PWA** |
