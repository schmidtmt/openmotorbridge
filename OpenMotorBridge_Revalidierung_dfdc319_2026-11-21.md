# OpenMotorBridge – Revalidierung `dfdc319`

**21. November 2026, Vergleich mit `4f65472`; Arbeitsverzeichnis sauber.**  
Vollständige Revalidierung aller zehn aktiven Hardware-Boards, der Fertigungspakete (Gerber RS-274X, CPL, BOM), der Firmware-Implementierungen (Treiber, Header, Stubs) und des CAD-/Mechanik-Status gegen die bisherigen Prüfberichte (`OpenMotorBridge_Revalidierung_4f65472_2026-11-18.md` und `OpenMotorBridge_Dokumentationsreview_2026-11-14.md`).

**Gesamtergebnis:** Mehrere zentrale Hardware- und Firmware-Befunde wurden mit Stand `dfdc319` nachweisbar gelöst (D4 in Main-BOM/CPL, C3-Pinout auf PCBA 07, S31 54-GPIO-Parität, BMP390-Bosch-Kompensationspolynom).  
**Gleichzeitig bleiben jedoch erhebliche, ungelöste Kritikpunkte in der Hardware, der Spannungsversorgung, den Firmware-Zusagen und der Mechanik bestehen.** PCBA 07 bleibt fertigungstechnisch gesperrt, und die zentrale 5V-USB-Werkstattversorgung ist in der aktuellen Topologie physikalisch nicht funktionsfähig.

---

## 1. Bestätigte Korrekturen (Stand `dfdc319`)

- **D4 vollständig in Main-Fertigungspaketen (V04 behoben):**  
  Die Schottky-Diode D4 (`PMEG4050EP`, SOD-128, LCSC `C85191`) zur Absicherung der zentralen USB-KL30-Rückspeisung ist nun konsistent in `01_main_box_pcba_bom_jlcpcb.csv` und `01_main_box_pcba_cpl_jlcpcb.csv` (X=176.00, Y=-115.00, top) enthalten.
- **ESP32-C3FH4 auf PCBA 07 nach Herstellerdatenblatt verdrahtet (V01 Teil 1 behoben):**  
  Der RISC-V SoC U1 im QFN-32 (5x5 mm) ist elektrisch und funktionell nach Espressif ESP32-C3 Datenblatt (Tabellen 2-1 und 2-2) angeschlossen:
  - Pin 1 (LNA_IN / RF): Führt direkt zur 50-$\Omega$-Leitung `BLE_ANT_50R` an ANT2.
  - Pins 2, 3, 11, 17, 31, 32: Alle VDD3P3- und VDDA-Versorgungen liegen an `VCC_3V3`.
  - Pin 7 (CHIP_EN): Liegt an `ESP_EN` mit RC-Verzögerung.
  - Pins 29/30 (XTAL_N / XTAL_P): Sind direkt mit dem 40.000 MHz Quarz Y1 verbunden.
  - Pins 25/26: Führen `USB_DM` und `USB_DP` an die Service-Schnittstelle J2.
  - Strapping: Pin 14 (GPIO8) steuert `LED_DATA`, Pin 15 (GPIO9 / BOOT) steuert `BTN_ARM_N` (mit 10k Pull-Up).
  - Pins 18–24 (integrierter SiP-Flash): Korrekt als NC belassen (nicht extern beschaltet).
- **S31-GPIO-Konsistenz (V03 behoben):**  
  Alle 54 Modulpads und Firmware-Header-Konstanten auf PCBA 01 (`main_box_config.h`) und PCBA 05 (`front_node_config.h`) stimmen mit dem 64-Pad ESP32-S31-WROOM-1U Datenblatt (Tabelle 3-2) überein (LoRa-SCK an GPIO 2 / Pad 4, I2S-MCLK an GPIO 35 / Pad 12, Front GNSS_RESET_N an GPIO 7 / Pad 11, etc.). Die Define-Kollision zwischen GNSS_RESET_N und WS2812B_DIN ist aufgelöst.
- **BMP390 Kalibrier- & Kompensationsalgorithmus (V06 behoben):**  
  In `firmware/front_node/src/front_sensor_hub.cpp` wurde der fehlerhafte Rohwert-Divisor (`raw_press / 256`) vollständig ersetzt durch das offizielle Bosch-Linearisierungs- und Kompensationspolynom 4. Ordnung (Temperatur & Druck in Pascal).
- **Fertigungsdaten (CPL/BOM):**  
  Alle zehn Fertigungspakete in `hardware/production_packages/` wurden über `hardware/scripts/export_manufacturing_packages.py` synchron neu generiert. CPL-Pick&Place-Drehwinkel und LCSC-Bauteilnummern sind hinterlegt.

---

## 2. Ungelöste Kritikpunkte & Mängel (Vollständige Übersicht)

### V02 · P1 · Qi-Ladecontroller U4 (BQ51050B) auf PCBA 07 verdrahtet Masse an VBAT und Spule an Masse
**Befund:** U4 (Texas Instruments BQ51050BRHLR im VQFN-20 / RHL-20 Gehäuse) weist im PCB fundamentale Fehlverdrahtungen auf:
- **Pin 1 (`PGND`) liegt an `VBAT`:** Der LiPo-Akku ist direkt gegen die interne Leistungsmasse des Laders kurzgeschlossen!
- **Pin 4 (`BOOT1`) liegt an `QI_AC2`:** Die Resonanzspule AC2 ist auf den internen Bootstrap-Pin gelegt.
- **Pins 18 & 19 (`AC2`) liegen hart auf `GND`:** Die Empfangsspule ist wechselstromseitig kurzgeschlossen.
- **Pins 11 & 12 (`BAT`) haben kein Netz:** Der eigentliche Ladeausgang hängt komplett in der Luft.
- **Pins 6..10 (`COMM1, ILIM, FOD, TS/CTRL`) haben kein Netz:** Sämtliche Sicherheitsbeschaltungen (Fremdkörpererkennung, NTC-Temperaturüberwachung, Ladestrombegrenzung) fehlen.
**Bewertung:** **PCBA 07 ist in diesem Zustand elektrisch unbrauchbar und brandgefährlich.**

---

### V05 · P1 · Das 5-V-Buck-Unterspannungs-Dilemma bei reiner USB-Speisung (Werkstattbetrieb)
**Befund:** Das Systemkonzept verspricht, dass alle Platinen (Zentralbox, Front Node, Satelliten-Pods, Radar) allein über den zentralen USB-Service-Port betrieben werden können (ohne 12V-Fahrzeugbatterie).  
**Elektrischer Widerspruch:**
1. USB-Eingangsspannung an J3 beträgt nominell 5,00 V (unter Last oft nur 4,75 V bis 4,85 V).
2. Auf PCBA 01 fällt Spannung über Diode D4 (PMEG4050EP: ca. 0,35–0,45 V) und den High-Side-Schalter U12 (TPS4H160: $R_{\text{ON}} \cdot I$) sowie den Kabelbaum ab.
3. Am Eingang der Satelliten (Front Node, Pods, Radar) kommen bestenfalls **4,20 V bis 4,40 V** an.
4. **Auf allen Satelliten sitzen TI `TPS54302` Step-Down (Buck) Abwärtswandler, die eine geregelte 5,0-V-Schiene erzeugen sollen.**
5. Ein Abwärtswandler kann aus 4,3 V physikalisch niemals 5,0 V erzeugen! Der TPS54302 spezifiziert eine minimale Eingangsspannung von 4,5 V und benötigt für 5,0 V Ausgang mindestens ca. 5,5 V bis 6,0 V (Drop-Out / $100\,\%$ Duty-Cycle Limit).
**Auswirkung:** Bei reiner 5V-USB-Speisung bricht die 5V-Schiene der Satelliten zusammen. 5V-Verbraucher (Aktuatoren, WS2812B-LEDs, GPS-Module, Codecs) verhungern oder booten im Dauer-Brownout.  
**Korrektur:** Die Doku muss klarstellen: Der 5V-USB-Port versorgt ausschließlich die Zentralbox für Firmware-Updates. Ein voller System- und Busbetrieb auf der Werkbank erfordert entweder ein externes 12V-Labornetzteil an KL30/KL31 oder einen USB-PD Sink Trigger (12V/20V).

---

### V01 (Rest) · P1 · Keyfob Akkumessung (`BAT_SENSE`) ist unbeschaltet (Floating Pad 4)
**Befund:** In `firmware/smart_keyfob/src/keyfob_config.h` wird deklariert:
```c
#define PIN_KEYFOB_BAT_ADC  GPIO_NUM_0  // U1 Pad 4 (BAT_SENSE)
```
Auf dem PCB (`openmotorbridge_smart_keyfob.kicad_pcb`) führt Pad 4 das Netz `BAT_SENSE`. **Dieses Netz besitzt jedoch im gesamten Layout nur genau ein einziges Pad (U1.4)!**
- Es gibt keinen 100k/100k Spannungsteiler zu `VBAT`.
- Die 3,7-V-Batteriespannung ist nirgendwo mit dem ADC verbunden.
- Würde `VBAT` (bis 4,2 V) direkt ohne Teiler an GPIO 0 angeschlossen, würde der ADC-Eingang des ESP32-C3 ($V_{\text{max}} = 3,6\,\text{V}$) zerstört.

---

### V07 · P2 · Preflight-Tool DRC Silent Masking & C6-Pad-Verwechslung
**Befund:**
1. **Silent Masking von Abstürzen:** Wenn `kicad-cli pcb drc` fehlschlägt oder mit `SIGABRT` abbricht, erzeugt es keine JSON-Datei. Das Skript fing dies zwar ab, lieferte aber bei fehlendem Report 0 Fehler zurück und druckte fälschlich: `✅ DRC Errors: 0, 100% Routed`.
2. **C6-Strapping-Bug:** Im ESP32-C6-Prüfzweig wurden Pad 13 und 14 abgefragt (die auf dem C6-MINI-1U Modul `IO1` / SCL und `GND` sind!) und fälschlich als GPIO 8 und 9 deklariert. Die echten Strapping-Pins liegen auf Pad 22 und 23.
3. **Blinder Fleck für Sub-Chips:** Das Skript auditierte bisher nur die Haupt-MCUs, weshalb der verpolte BQ51050B und das unbeschaltete `BAT_SENSE`-Pad jahrelang unbemerkt blieben.

---

### A01 · P1 · Build-Target & Toolchain-Widerspruch (ESP32-S31 vs. ESP32-S3)
**Befund:** Kapitel 09 und die SSOT beschreiben den Haupt- und Frontknoten-Controller als **ESP32-S31** (Espressif RISC-V Dual-Core mit ULP).  
Die tatsächliche Firmware-Build-Konfiguration (`platformio.ini`, `sdkconfig.defaults`, `CMakeLists.txt`) setzt jedoch unverändert auf:
```ini
board = esp32-s3-devkitc-1
idf_target = esp32s3
```
- Es gibt im aktuellen ESP-IDF v5.x kein natives Produktions-Target `esp32s31`.
- Der Code kompiliert für den Xtensa LX7 (ESP32-S3), während die Dokumentation die RISC-V Architektur als fertigen Stand beschreibt.
**Korrektur:** Offenlegen, dass der aktuelle Firmware-Stand ein Referenzbuild auf ESP32-S3-Basis ist und die Migration auf S31 ansteht, sobald Espressifs Toolchain dies unterstützt.

---

### A03 & A04 · P1 · Telemetrie-Blackbox & WebDAV sind im Code Dummy-Stubs
**Befund:** Kapitel 06 der Dokumentation verspricht:
- Crash-sichere DSGVO-konforme ECDSA-P256 Signierung jedes Telemetrie-Blocks.
- Rollierendes Überschreiben (Ringbuffer-Purge) bei vollem Speicher.
- Vollautomatischer WebDAV-Upload über TLS 1.3 bei Erreichen des Heim-WLANs.
**Code-Realität:**
- In `firmware/main_controller/src/sdio_ring_buffer.cpp`: Die SHA256-Hashkette ist implementiert, aber die kryptografische ECDSA-Signatur ist lediglich ein ungenutztes Flag. Der freie Speicherplatz wurde lange statisch auf 14.500 MB gesetzt.
- In `firmware/main_controller/src/webdav_uploader.cpp`: Der eigentliche Upload-Thread enthielt lange nur ein `vTaskDelay(1500)` mit Rückgabe `true`, ohne eine echte Dateiübertragung durchzuführen. Zwar existiert nun ein `esp_http_client`-Pfad, dieser ist jedoch weder im Gesamtsystem integriert noch auf Abbrüche/Wiederaufnahme bei Funkloch getestet.

---

### A05 · P1 · Fehlende Partitions-Dateien und unklare Flash-Anleitung
**Befund:** Die Firmware-Dokumentation beschreibt ein einheitliches 16-MB-Flashlayout mit A/B-OTA und SPIFFS/LittleFS Partition `storage` ab `0x610000`.  
- Im Ordner `firmware/main_controller/` existierte keine eigene `partitions.csv` (Standard-Fallback 4MB von ESP-IDF).
- Die Cartridge nutzt eine abweichende Adressaufteilung (`0x370000`).
- Eine Anleitung zur Generierung des im Handbuch genannten `data_image.bin` fehlt.

---

### B01..B12 · P1/P2 · Mechanik- & CAD-Kritikpunkte
In `OpenMotorBridge_Dokumentationsreview_2026-11-14.md` wurden gravierende Konstruktions- und Dokumentationswidersprüche im CAD nachgewiesen:
1. **B01 & B05 (Pod L-Deckel & Maßinkonsistenz):** Der Deckel ist 63,8 mm breit plus 1,6 mm Führungszunge (reicht bis Y=70,15 mm), die Wannen-Nut endet jedoch bei Y=68,5 mm. Dies führt zu einer geometrischen Kollision mit der Außenwand.
2. **B06 (Aktuator-Traversen):** Die Dokumentation beschreibt zwei unabhängig einschiebbare Wandnut-Traversen mit bündigen Senkkopfschrauben DIN 7991; die Bauanleitung fordert dagegen eine im Boden verschraubte Schlittenbaugruppe mit Zylinderkopfschrauben DIN 912.
3. **B07 (Dry Flap):** Das Teil wird in der Stückliste als „einschiebbarer Zwischendeckel“, in der Montage als „federbelastete Klappe“ und im CAD als 48x56 mm flexible Abdeckung ohne Feder modelliert.
4. **B08 (Dock-Kabel & Ports):** Die Docks (GSA / Kofferdeckel) beschreiben weiterhin 2-Draht-Versorgungskabel an veralteten Port-Koordinaten, obwohl die v10-Stirnwand das 4-Draht-Backbone (Versorgung + USB D+/D-) an übereinanderliegenden Ports verlangt.
5. **B11 (Handschuhfach-Hub):** Widersprüchliche Port-Anzahlen und -Formate (Text nennt 6-Pin Einspeisung und USB-A; CAD zeigt 5x USB-C).
6. **B12 (Sena Kaltstart vs. BLE):** Doku behauptet „100% digitale Bedienung ohne Stößeljustage“, fordert aber gleichzeitig Hubmagnete für den Kaltstart, da ausgeschaltete OEM-Geräte kein BLE-Wakeup unterstützen.

---

## 3. Revalidierungs-Matrix nach Modulen

| Modul / Komponente | Hardware-Status | Firmware-Status | Dokumentations-Status | Freigabestatus |
| :--- | :---: | :---: | :---: | :---: |
| **PCBA 01 (Zentralbox)** | ✅ 100% Routed, D4 in BOM/CPL | ⚠️ ESP32-S3 Build statt S31 | ⚠️ USB-Werkstatt-Speisung unzureichend | **Eingeschränkt** |
| **PCBA 03 (Cartridge)** | ✅ TS5A23157 + CH554E geroutet | ✅ C6-Header synchron | ⚠️ Veraltete TMUX-Kommentare bereinigt | **Freigegeben** |
| **PCBA 05 (Front Node)** | ✅ S31 + C3-Aux geroutet | ⚠️ S3 Build statt S31 | ⚠️ 5V-Buck Drop-Out bei USB-Betrieb | **Eingeschränkt** |
| **PCBA 05B (Glovebox Hub)**| ✅ Geroutet & DRC-konform | Entfällt (Passiv/Hub) | ⚠️ Widersprüchliche Portanzahl (Text vs CAD) | **Dokumentation anpassen** |
| **PCBA 05C (Mirror Pod)** | ✅ Geroutet & DRC-konform | Entfällt (Passiv/LED) | ✅ Konform | **Freigegeben** |
| **PCBA 05D (Sensor Puck)** | ✅ SAM-M10Q + BMP390 geroutet | ✅ Bosch-Polynom integriert | ✅ Konform | **Freigegeben** |
| **PCBA 07 (Smart Keyfob)** | ❌ **U4 BQ51050B verpolt, BAT_SENSE offen** | ⚠️ ADC liest offenes Pad | ❌ Veraltete Pinout-Tabellen | ❌ **GESPERRT (P1)** |
| **PCBA 08 (Radar Sub-MCU)** | ✅ ESP32-C5 geroutet | ✅ MR20 Protokoll vorhanden | ✅ Konform | **Freigegeben** |
| **PCBA 09 (OMM 2.4G Intercom)**| ✅ Geroutet & DRC-konform | ⚠️ 80/95% Akku-Platzhalter | ✅ Konform | **Freigegeben** |
| **PCBA 10 (OMM 446M Intercom)**| ✅ Geroutet & DRC-konform | ⚠️ Vocoder-Integration WIP | ✅ Konform | **Freigegeben** |

---

## 4. Sofortige Maßnahmen & Prioritätenliste

1. **Priorität 1 (Elektrische Sicherheit & Funktion):**
   - **PCBA 07 U4 (BQ51050B):** Vollständiges Re-Routing des VQFN-20 Gehäuses nach TI-Referenzdesign (Pin 1 auf GND, Spule an AC1/AC2 mit Bootstrap-Kondensatoren, Pin 11/12 an VBAT).
   - **PCBA 07 BAT_SENSE:** 100k/100k Spannungsteiler zwischen VBAT, Pad 4 (GPIO 0) und GND im Schaltplan und Layout ergänzen.
2. **Priorität 2 (Systemkonzept & Topologie):**
   - **USB-Versorgungskonzept (V05):** In Kapitel 05 und 16 unmissverständlich klarstellen: Reine 5V-USB-Versorgung betreibt ausschließlich die Zentralbox zu Flashzwecken. Vollständiger Busbetrieb erfordert 12V an KL30/KL31.
3. **Priorität 3 (Software-Ehrlichkeit):**
   - In Kapitel 06 den Telemetrie- und WebDAV-Status von „voll integriert“ auf „WIP / Referenztreiber vorhanden, Cloud-Sync in Verifikation“ präzisieren.
   - Das Build-Target ESP32-S3 als offizielles Zwischen-Target für den noch nicht im PlatformIO verfügbaren S31 deklarieren.
4. **Priorität 4 (Mechanik & CAD):**
   - Deckelmaß Y=70,15 mm im Pod-CAD gegen die Wanne freischneiden.
   - Traversenmontage (Boden vs. Nut) in Doku und Bauanleitung einheitlich auf Wandnut festlegen.
