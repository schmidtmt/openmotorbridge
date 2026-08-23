# 13 - Rear Pod 3: Hardware Architecture, GNSS, LoRa & Co-Processor

Satellite Pod 3 combines high-precision positioning (GNSS), digital long-range communication (OpenMotorMesh LoRa 868 MHz), and an autonomous co-processor inside an aerodynamic, waterproof IP67 enclosure mounted on the rear fender or luggage rack.

---

## 1. Detailed Hardware Architecture in Rear Pod 3

```
 6-Pin Pogo Interface (from Central Box)
 ┌────────────────────────────────────────────────────────┐
 │ Pin 1: POD3_VCC (5V) ────► [ TI TPS7A0533 3.3V LDO ]   │
 │ Pin 2: POD3_GND ─────────► [ Common Ground Plane ]     │
 │ Pin 3: POD3_UART_TX ◄──── [ ESP32-C3 UART0 TX ]        │
 │ Pin 4: POD3_UART_RX ────► [ ESP32-C3 UART0 RX ]        │
 │ Pin 5: POD3_GNSS_PPS ◄─── [ MAX-M10S TIMEPULSE ]       │
 │ Pin 6: POD3_1WIRE_ID ◄─── [ Maxim DS2401Z+ ID ]        │
 └────────────────────────────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
 [ u-blox MAX-M10S GNSS ]            [ Semtech SX1262 LoRa ]
   • 25x25mm Patch Antenna             • 868 MHz Helical Antenna
   • 10 Hz PVT Navigation              • +22 dBm PA
   • UART1 to ESP32-C3                 • SPI Master to ESP32-C3
```

### 1.1 Core Components in Rear Pod 3
1. **Main Co-Processor (ESP32-C3-WROOM-02):**
   * 32-bit RISC-V single-core @ 160 MHz with 4 MB embedded flash.
   * Handles local 10 Hz NMEA/UBX parsing from the MAX-M10S.
   * Controls the SX1262 LoRa transceiver over high-speed SPI (10 MHz).
   * Processes OMM Layer 2 frame encoding/decoding (Codec2 voice frames, GPS telemetry, DLE beacons).
2. **GNSS Engine (u-blox MAX-M10S):**
   * Multi-constellation 4-system concurrent reception (GPS, GLONASS, Galileo, BeiDou).
   * 25 x 25 x 4 mm ceramic patch antenna with integrated LNA and SAW bandpass filter.
   * 1-PPS hardware time pulse (jitter $< 15\,\text{ns}$ RMS) routed directly to Pogo Pin 5.
3. **OpenMotorMesh LoRa Transceiver (Semtech SX1262):**
   * Frequency range: 868.0 – 868.6 MHz (EU ISM band) / 915 MHz (US band).
   * Output power: up to $+22\,\text{dBm}$ ($160\,\text{mW}$ EIRP).
   * Integrated RF switch, low-pass filter, and matched 868 MHz helical antenna.
4. **1-Wire Identification (Maxim / ADI DS2401Z+):**
   * Delivers the 64-bit Silicon Serial Number for automated cartridge and port detection by the central box.
5. **Power Regulation (TI TPS7A0533):**
   * Ultra-low-noise automotive LDO (5.0V input $\rightarrow$ clean 3.3V / 200mA for GNSS and LoRa).

---

## 2. 6-Pin Pogo Pinout Assignment

| Pogo Pin | Signal Name | Electrical Specification | Description |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `POD3_VCC` | 5.0 V DC (max. 250 mA) | Continuous supply from central box |
| **Pin 2** | `POD3_GND` | Power & Signal Ground | Dedicated return path |
| **Pin 3** | `POD3_UART_TX` | 3.3 V LVTTL (460,800 Baud) | Data stream from ESP32-C3 to central box |
| **Pin 4** | `POD3_UART_RX` | 3.3 V LVTTL (460,800 Baud) | Commands from central box to ESP32-C3 |
| **Pin 5** | `POD3_GNSS_PPS`| 3.3 V Pulse (100 ms width) | 1-PPS hardware time reference synchronization |
| **Pin 6** | `POD3_1WIRE_ID`| 1-Wire Open-Drain (3.3 V) | DS2401 cartridge identification bus |

---

## 3. High-Speed UART Protocol & Frame Structure
Communication between Rear Pod 3 and the main box uses a binary, CRC-16 protected frame protocol at **460,800 Baud**:

```
┌──────┬──────┬────────────┬─────────┬──────────────┬─────────┐
│ SOF  │ LEN  │ MSG_TYPE   │ SEQ_NUM │ PAYLOAD      │ CRC-16  │
│ 0xAA │ 1 B  │ 0x01..0x05 │ 1 B     │ 0..250 Bytes │ 2 Bytes │
└──────┴──────┴────────────┴─────────┴──────────────┴─────────┘
```
- `MSG_TYPE 0x01` (PVT Telemetry): 10 Hz GPS position, speed, altitude, satellite count.
- `MSG_TYPE 0x02` (LoRa Rx Voice Frame): Received Codec2 audio packet (300 Bytes) for intercom mixing.
- `MSG_TYPE 0x03` (LoRa Tx Voice Frame): Codec2 audio packet to be transmitted over LoRa.
- `MSG_TYPE 0x04` (DLE Status & Beacons): Exchange of RSSI metrics and cluster routing tables.

---

## 4. Advantages of Rear Fender Placement
- **Optimal 360-Degree GNSS Sky View:** No line-of-sight obstruction from the rider, windscreen, or fuel tank.
- **Maximum RF Isolation:** The 868 MHz transmitter radiates at the rear – $> 1.2\,\text{m}$ away from the 2.4 GHz side mesh units (Pod 1 & Pod 2).
- **Offloads the Main MCU:** Frees the ESP32-S3 from time-critical NMEA parsing and LoRa SPI polling.
