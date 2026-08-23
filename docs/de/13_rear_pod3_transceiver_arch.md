# 13 - Heck-Pod 3: Hardware-Architektur, GNSS, LoRa & Co-Prozessor

Der Heck-Pod 3 buendelt praezise Positionsbestimmung (GNSS), digitalen Weitbereichsfunk (OpenMotorMesh LoRa 868 MHz) und einen autarken Co-Prozessor in einem aerodynamischen, wasserdichten IP67-Gehaeuse am Heckbuerzel oder Gepaecktraeger.

---

## 1. Detaillierte Hardware-Architektur im Heck-Pod 3

```
 6-Pin Pogo Interface (von Zentralbox)
 ┌────────────────────────────────────────────────────────┐
 │ Pin 1: POD3_VCC (5V) ────► [ TI TPS7A0533 3.3V LDO ]   │
 │ Pin 2: POD3_GND ─────────► [ Gemeinsame Masseflaeche ] │
 │ Pin 3: POD3_UART_TX ◄──── [ ESP32-C3 UART0 TX ]        │
 │ Pin 4: POD3_UART_RX ────► [ ESP32-C3 UART0 RX ]        │
 │ Pin 5: POD3_GNSS_PPS ◄─── [ MAX-M10S TIMEPULSE ]       │
 │ Pin 6: POD3_1WIRE_ID ◄─── [ Maxim DS2401Z+ ID ]        │
 └────────────────────────────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
 [ u-blox MAX-M10S GNSS ]            [ Semtech SX1262 LoRa ]
   • 25x25mm Patch-Antenne             • 868 MHz Wendelantenne
   • 10 Hz PVT Navigation              • +22 dBm PA
   • UART1 an ESP32-C3                 • SPI Master an ESP32-C3
```

### 1.1 Kern-Bauelemente im Heck-Pod 3
1. **Haupt-Co-Prozessor (ESP32-C3-WROOM-02):**
   * 32-Bit RISC-V Single-Core @ 160 MHz mit 4 MB Embedded Flash.
   * Uebernimmt lokales 10 Hz NMEA/UBX-Parsing vom MAX-M10S.
   * Steuert den SX1262 LoRa-Transceiver ueber High-Speed SPI (10 MHz).
   * Verarbeitet OMM Layer 2 Frame En-/Decodierung (Codec2 Voice Frames, GPS Telemetrie, DLE Beacons).
2. **GNSS Engine (u-blox MAX-M10S):**
   * Multi-Konstellation 4-System Parallelbetrieb (GPS, GLONASS, Galileo, BeiDou).
   * 25 x 25 x 4 mm Keramik-Patchantenne mit integriertem LNA und SAW-Bandpassfilter.
   * 1-PPS Hardware-Zeitsignal (Jitter $< 15\,\text{ns}$ RMS) direkt auf Pogo-Pin 5 gefuehrt.
3. **OpenMotorMesh LoRa Transceiver (Semtech SX1262):**
   * Frequenzbereich: 868.0 – 868.6 MHz (EU ISM Band) / 915 MHz (US Band).
   * Sendeleistung: bis zu $+22\,\text{dBm}$ ($160\,\text{mW}$ EIRP).
   * Integrierter HF-Schalter, Tiefpassfilter und abgestimmte 868-MHz-Wendelantenne.
4. **1-Wire Identifikation (Maxim / ADI DS2401Z+):**
   * Liefert die 64-Bit Silicon Serial Number fuer die automatische Kassetten- und Steckplatzerkennung an der Zentralbox.
5. **Spannungsregelung (TI TPS7A0533):**
   * Ultra-Low-Noise Automotive LDO (5.0V Eingang $\rightarrow$ saubere 3.3V / 200mA fuer GNSS & LoRa).

---

## 2. Belegung der 6-Pin Pogo-Kontaktleiste

| Pogo-Pin | Signalname | Elektrische Spezifikation | Beschreibung |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `POD3_VCC` | 5.0 V DC (max. 250 mA) | Dauer-Versorgung ueber Zentralbox |
| **Pin 2** | `POD3_GND` | Power- & Signalmasse | Dedizierte Rueckleitung |
| **Pin 3** | `POD3_UART_TX` | 3.3 V LVTTL (460.800 Baud) | Datenstrom vom ESP32-C3 zur Zentralbox |
| **Pin 4** | `POD3_UART_RX` | 3.3 V LVTTL (460.800 Baud) | Steuerkommandos von Zentralbox zum ESP32-C3 |
| **Pin 5** | `POD3_GNSS_PPS`| 3.3 V Impuls (100 ms Breite) | 1-PPS Hardware-Zeitnormal-Synchronisation |
| **Pin 6** | `POD3_1WIRE_ID`| 1-Wire Open-Drain (3.3 V) | DS2401 Kassetten-Identifikationsbus |

---

## 3. High-Speed UART-Protokoll & Frame-Struktur
Die Kommunikation zwischen Heck-Pod 3 und der Hauptbox erfolgt ueber ein binaeres, CRC-16-gesichertes Frame-Protokoll bei **460.800 Baud**:

```
┌──────┬──────┬────────────┬─────────┬──────────────┬─────────┐
│ SOF  │ LEN  │ MSG_TYPE   │ SEQ_NUM │ PAYLOAD      │ CRC-16  │
│ 0xAA │ 1 B  │ 0x01..0x05 │ 1 B     │ 0..250 Bytes │ 2 Bytes │
└──────┴──────┴────────────┴─────────┴──────────────┴─────────┘
```
- `MSG_TYPE 0x01` (PVT Telemetry): 10 Hz GPS-Position, Geschwindigkeit, Hoehe, Satellitenanzahl.
- `MSG_TYPE 0x02` (LoRa Rx Voice Frame): Empfangenes Codec2 Audio-Paket (300 Bytes) zur Einspeisung.
- `MSG_TYPE 0x03` (LoRa Tx Voice Frame): Zu sendendes Codec2 Audio-Paket von der Hauptbox.
- `MSG_TYPE 0x04` (DLE Status & Beacons): Austausch von Signalstaerken und Cluster-Routing-Tabellen.

---

## 4. Vorteile der Auslagerung an den Heckbuerzel
- **Optimale 360-Grad-GNSS-Sicht:** Keine Abschattung durch den Fahrerkoerper, Tank oder die Frontverkleidung.
- **Maximale HF-Isolation:** Der 868-MHz-Weitbereichssender strahlt am Heck ab – $> 1{,}2\,\text{m}$ entfernt von den 2,4-GHz-Mesh-Kassetten (Pod 1 & Pod 2) an den vorderen Rahmenseiten.
- **Entlastung der Haupt-MCU:** Der ESP32-S3 wird vollstaendig von zeitkritischen NMEA/UBX-Interrupts und LoRa-SPI-Polling befreit.
