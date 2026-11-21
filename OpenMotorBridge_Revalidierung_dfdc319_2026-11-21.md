# OpenMotorBridge – Revalidierung `dfdc319`

**21. November 2026, Vergleich mit `4f65472`; Arbeitsverzeichnis sauber.** Erneute umfassende Inventur, Fertigungspaket-Prüfung (Gerber, CPL, BOM mit LCSC-Teilenummern), vollständiger MCU- und Subchip-Pinabgleich aller zehn aktiven Boards gegen die offiziellen Hersteller-Datenblätter, Prüfung des BMP390-Kompensationspfads, der USB-Busversorgung und der CPL-Bestückungsdaten.

**Ergebnis:** Wesentliche Meilensteine wurden erfolgreich verifiziert: Die Integration der Diode D4 in BOM/CPL ist behoben, der ESP32-C3FH4 auf PCBA 07 ist nun zu 100 % herstellerkonform verdrahtet, alle 54 S31-GPIO-Defines stimmen exakt mit Tabelle 3-2 des S31-Datenblatts überein, und die Bosch BMP390-Druckkompensation wurde im Sensortreiber mathematisch korrekt implementiert.  
**Kritischer Restbefund (P1):** Der Qi-Wireless-Ladecontroller U4 (BQ51050BRHLR) auf PCBA 07 weist weiterhin schwere Pinvertauschungen auf (Masse an VBAT, fehlende Bootstrap- und Batterie-Ausgangsbeschaltung) und war in der SSOT fälschlich als 28-Pin-Bauteil hinterlegt. Zudem besaß das Preflight-Skript blinde Flecken für Subchips sowie einen C6-Pad-Anzeigefehler. **Keine Gesamtfreigabe für PCBA 07.**

---

## Bestätigte Korrekturen (Stand `dfdc319`)

- **D4 vollständig in Main-Fertigungspaketen (V04 behoben):** Die Schottky-Diode D4 (PMEG4050EP, SOD-128, LCSC `C85191`) zur Absicherung der zentralen USB-KL30-Rückspeisung ist nun konsistent in `01_main_box_pcba_bom_jlcpcb.csv` und `01_main_box_pcba_cpl_jlcpcb.csv` (Pos X=176.00, Y=-115.00, Side=top) enthalten.
- **ESP32-C3FH4 auf PCBA 07 vollständig nach Herstellerdatenblatt verdrahtet (V01 behoben):** Der neue RISC-V SoC U1 im QFN-32 (5x5 mm) ist elektrisch und funktionell exakt nach Espressif ESP32-C3 Datenblatt (Tabellen 2-1 und 2-2) angeschlossen:
  - Pin 1 (LNA_IN / RF): Führt direkt zur 50-$\Omega$-Leitung `BLE_ANT_50R` an ANT2 (Johanson Chipantenne).
  - Pins 2, 3, 11, 17, 31, 32: Alle VDD3P3- und VDDA-Versorgungen liegen an `VCC_3V3`.
  - Pin 7 (CHIP_EN): Liegt an `ESP_EN` mit RC-Verzögerung.
  - Pins 29/30 (XTAL_N / XTAL_P): Sind direkt mit dem 40.000 MHz Quarz Y1 verbunden.
  - Pins 25/26: Führen `USB_DM` und `USB_DP` an die Service-Schnittstelle J2.
  - Strapping: Pin 14 (GPIO8) steuert `LED_DATA`, Pin 15 (GPIO9 / BOOT) steuert `BTN_ARM_N` (mit 10k Pull-Up).
  - Pins 18–24 (integrierter SiP-Flash): Korrekt als NC belassen (nicht extern beschaltet).
- **S31-GPIO-Konsistenz (V03 behoben):** Alle 54 Modulpads und Firmware-Header-Konstanten auf PCBA 01 (`main_box_config.h`) und PCBA 05 (`front_node_config.h`) stimmen mit dem realen 64-Pad ESP32-S31-WROOM-1U Datenblatt (Tabelle 3-2) überein:
  - Main LoRa-SCK: Pad 4 führt Netz `SPI_SCK` $\rightarrow$ deklariert als `GPIO_NUM_2` (Tabelle 3-2: Pad 4 = GPIO2).
  - Main I2S-MCLK: Pad 12 führt Netz `I2S_MCLK` $\rightarrow$ deklariert als `GPIO_NUM_35` (Tabelle 3-2: Pad 12 = GPIO35).
  - Front GNSS_RESET_N: Pad 11 führt Netz `GNSS_RESET_N` $\rightarrow$ deklariert als `GPIO_NUM_7` (Tabelle 3-2: Pad 11 = GPIO7).
  - Front Mikrofon DATA: Pad 12 führt Netz `MIC_DATA` $\rightarrow$ deklariert als `GPIO_NUM_35`.
  - Front E22_EN: Pad 36 führt Netz `E22_EN` $\rightarrow$ deklariert als `GPIO_NUM_59`.
  - Die Define-Kollision zwischen GNSS_RESET_N und WS2812B_DIN ist aufgelöst.
- **BMP390 Kalibrier- & Kompensationsalgorithmus (V06 behoben):** In `firmware/front_node/src/front_sensor_hub.cpp` wurde der fehlerhafte Rohwert-Divisor (`raw_press / 256`) vollständig ersetzt durch:
  - Burst-Read der 21 Kalibrierkoeffizienten (`NVM_PAR_T1..T3`, `NVM_PAR_P1..P11`) aus Register `0x31..0x45`.
  - Linearisierte Temperaturkompensation ($T_{\text{lin}}$) nach Bosch Datenblatt Abschnitt 3.11.
  - Kompensationspolynom 4. Ordnung für den atmosphärischen Druck in Pascal ($300..1250\,\text{hPa}$).
- **Fertigungsdaten & CPL-Ausrichtung:** Alle zehn Fertigungspakete in `hardware/production_packages/` wurden über `hardware/scripts/export_manufacturing_packages.py` synchron neu gebaut. CPL-Pick&Place-Drehwinkel (z.B. U1 auf PCBA 07 auf $-90^\circ$) und LCSC-Bauteilnummern (inkl. U13 ESP32-PICO `C2686884`, U4 TS5A23157 `C22509`, U7 CH554E `C111388`, U4 BMP390 `C2843537`) sind konsistent.

---

## Verbleibende & Neu Identifizierte Befunde

### V02 · P1 · Qi-Ladecontroller U4 (BQ51050B) auf PCBA 07 verdrahtet Masse an VBAT und Spule an Masse

U4 ist im Schaltplan und Layout als Texas Instruments BQ51050BRHLR im Gehäuse VQFN-20 (RHL, 3.5 x 4.5 mm) bestückt. Die physische Netzbelegung weicht fundamental von der Pinbelegung des TI-Datenblatts ab:

| Physischer Pin (RHL-20) | TI-Funktion (Hersteller) | Aktuelles PCB-Netz (`openmotorbridge_smart_keyfob.kicad_pcb`) | Status / Auswirkung |
| :---: | :---: | :---: | :--- |
| **1** | **PGND** (Power Ground) | **`VBAT`** | ❌ **Akku kurzgeschlossen gegen IC-Masse!** |
| **2** | **AC1** (AC-Eingang 1) | `QI_AC1` | ✅ OK |
| **3** | **AC1** (AC-Eingang 1) | `QI_AC1` | ✅ OK |
| **4** | **BOOT1** (Bootstrap Cap 1) | **`QI_AC2`** | ❌ **Eingangsspule AC2 an internem Bootstrap-Pin** |
| **5** | **CLAMP1** (Resonanz-Clamp 1) | *ohne Netz* | ❌ Resonanzkreis unvollständig |
| **6..10** | **COMM1, ILIM, FOD, TS/CTRL** | *ohne Netz* | ❌ Keine Strom- & Temperaturüberwachung |
| **11, 12** | **BAT** (Ladeausgang Akku) | *ohne Netz* | ❌ **Tatsächlicher Batterie-Ladeausgang hängt in der Luft** |
| **14** | **RECT** (Gleichrichter-Ausgang) | *ohne Netz* | ❌ Glättungskondensator fehlt |
| **17** | **BOOT2** (Bootstrap Cap 2) | **`GND`** | ❌ Bootstrap auf Masse gelegt |
| **18** | **AC2** (AC-Eingang 2) | **`GND`** | ❌ **Spuleneingang AC2 hart auf Masse kurzgeschlossen** |
| **19** | **AC2** (AC-Eingang 2) | **`GND`** | ❌ **Spuleneingang AC2 hart auf Masse kurzgeschlossen** |
| **20, 21** | **PGND / Thermal Pad** | `GND` | ✅ OK |

**Ursachenanalyse:** In `data/pcba_pinouts.json` (SSOT) war U4 fälschlicherweise als „QFN-28 (4.5x3.5 mm)“ eingetragen. Das Layout übernahm veraltete Dummy-Konnektivität, bei der Pad 1 blind als VBAT geroutet wurde.
**Erforderlich:** Vollständige Übernahme der TI BQ51050B RHL-20 Referenzbeschaltung:
1. `QI_COIL_AC1` an Pins 2 & 3; Serienkondensator $C_{\text{BOOT1}}$ zwischen Pin 4 und Pins 2/3.
2. `QI_COIL_AC2` an Pins 18 & 19; Serienkondensator $C_{\text{BOOT2}}$ zwischen Pin 17 und Pins 18/19.
3. Resonanz- und Glättungskondensatoren an Pin 14 (`RECT`).
4. Pin 11 & 12 an `VBAT` (mit 10 $\mu\text{F}$ Puffer).
5. Pin 1, 20 und Thermal Pad 21 an `GND`.

---

### V07b · P2 · Script-Bugs & blinde Flecken im Preflight-Prüftool (`tools/audit_pcbas_preflight.py`)

Das Preflight-Tool lief formal mit Exitcode 0 durch, übersah jedoch den U4-Fehler und enthielt Ausgabefehler:
1. **Falsche Pin-Zuordnung im C6-Prüfzweig (Zeile 343–352):**
   ```python
   # FALSCH (in tools/audit_pcbas_preflight.py):
   pad13_net = mcu_pads.get("13", "")  # Gibt fälschlich als GPIO 8 / STRAP aus
   pad14_net = mcu_pads.get("14", "")  # Gibt fälschlich als GPIO 9 / BOOT aus
   ```
   Auf dem ESP32-C6-MINI-1U ist Pad 13 jedoch `IO1` (`I2C_SCL`) und Pad 14 ist `GND`! Die echten Strapping-Pins liegen auf **Pad 22 (`GPIO8`)** und **Pad 23 (`GPIO9`)**. Das Skript meldete daher scheinbar „Pad 14 (GPIO 9 / BOOT): Net = GND“, was beim Betrachter den Eindruck erweckte, der Boot-Pin läge auf Masse, obwohl der echte Boot-Pin (Pad 23) korrekt auf `I2C_SDA` / High liegt.
2. **Blinder Fleck für Sub-Chips:**
   Das Skript prüfte bisher ausschließlich die primäre MCU (`mcu_ref`), ignorierte aber sämtliche Sub-Chips (`U4 BQ51050B`, `U4 TS5A23157`, `U7 CH554E`, `U4 BMP390`). Daher bemerkte die Preflight-DRC nicht, dass U4 auf PCBA 07 falsch beschaltet ist.
**Erforderlich:** Korrektur der C6-Padabfrage im Prüfskript und Erweiterung des Preflight-Audits auf alle in der SSOT definierten `sub_chips`.

---

### V08 · P2 · Veraltete Dokumentations- & Header-Artefakte in Smart Cartridge (`firmware/smart_cartridge/src/cartridge_config.h`)

In `cartridge_config.h` Zeilen 43–46 sind noch historische Kommentare aus der Entwicklungsphase vor dem TS5A23157- und CH554E-Umbau enthalten:
```c
#define PIN_I2S_BCLK GPIO_NUM_7   // U1 Pad 16 -> ... & TMUX1574 CH1 Bank 1 (3.072 MHz)
#define PIN_I2S_DOUT GPIO_NUM_15  // U1 Pad 20 -> ... & TMUX1574 CH3 Bank 1 (to OMM Mesh)
```
- Der Multiplexer `TMUX1574` existiert auf PCBA 03 nicht mehr (ersetzt durch TI `TS5A23157`, U4).
- Das OMM-Mesh-Modul wird nicht per I2S über den Multiplexer bedient, sondern digital über den USB-Host-Controller `CH554E` (U7) via 3.0 Mbps UART (`PIN_CH554_UART_TX/RX` an GPIO 20/21). Die I2S-Leitungen von U1 gehen exklusiv an den lokalen ES8388-Codec U3 für analoge OEM-Headsets.
**Erforderlich:** Bereinigung der veralteten Kommentare in `cartridge_config.h`.

---

## System-Auditergebnis & Matrix (Stand `dfdc319`)

| Board | Funktion / Rolle | KiCad DRC | KiCad Unconnected | SSOT Parität | Silizium-Datenblatt-Audit | Freigabestatus |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PCBA 01** | Zentralbox Controller (S31 + QCC3084 + PICO + SX1262) | **0** | **0** | **100 %** | ✅ 100 % konform (S31, PICO, Codec, D4) | **Produktionsbereit** |
| **PCBA 03** | Universal Smart Cartridge (C6 + ES8388 + TS5A23157 + CH554E) | **0** | **0** | **100 %** | ✅ 100 % konform (C6, CH554E, TS5A) | **Produktionsbereit** |
| **PCBA 05** | Universal Front Node (S31 + C3-Aux + USB-Hub) | **0** | **0** | **100 %** | ✅ 100 % konform (S31, C3FH4, JST-GH) | **Produktionsbereit** |
| **PCBA 05B** | Cockpit Media & Glovebox Hub | **0** | **0** | **100 %** | ✅ 100 % konform | **Produktionsbereit** |
| **PCBA 05C** | Ultra-Compact Mirror Pod | **0** | **0** | **100 %** | ✅ 100 % konform | **Produktionsbereit** |
| **PCBA 05D** | Environmental & GNSS Sensor Puck (SAM-M10Q + BMP390) | **0** | **0** | **100 %** | ✅ 100 % konform (BMP390 Bosch-linearisiert) | **Produktionsbereit** |
| **PCBA 07** | 2-in-1 LoRa Smart Keyfob & Pager | **0** | **0** | **Partiell** | ⚠️ U1 OK, **U4 BQ51050B fehlerhaft** | ❌ **Gesperrt (V02 offen)** |
| **PCBA 08** | Radar 2.0 Sub-MCU & Visual Halo (C5) | **0** | **0** | **100 %** | ✅ 100 % konform | **Produktionsbereit** |
| **PCBA 09** | OMM 2.4 GHz Tri-Band UCS Intercom | **0** | **0** | **100 %** | ✅ 100 % konform | **Produktionsbereit** |
| **PCBA 10** | OMM 446 MHz PMR/DMR Transceiver Module | **0** | **0** | **100 %** | ✅ 100 % konform | **Produktionsbereit** |

**Gesamtfreigabe:** 9 von 10 Boards vollständig freigabefähig. PCBA 07 bleibt bis zur Korrektur des BQ51050B-Netzroutings gesperrt.
