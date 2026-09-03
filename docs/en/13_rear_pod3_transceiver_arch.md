# 13 - Rear Pod 3: GNSS & Dual-PHY OpenMotorMesh Transceiver Architecture

**Rear Pod 3** (located at the rear fender / luggage rack) serves as the primary navigation and radio gateway for OpenMotorBridge. It utilizes the identical universal **Generic Maximum Envelope ($120.0 \times 64.0 \times 32.0\,\text{mm}$)** and houses the multi-constellation GNSS engine (**u-blox MAX-M10S**), the complete **Dual-PHY OpenMotorMesh system (2.4 GHz High-Speed Primary + 868 MHz LoRa Long-Range Fallback)**, and a dedicated **ESP32-C3 RISC-V co-processor** within its open carrier sled.

---

## 1. System Topology & 1-Tier Modular Architecture

The rear cartridge utilizes the **100% universal base sled ([cartridge_base_sled.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/00_base_sled.scad))**, identical to the sleds deployed in Pod 1 (Sena) and Pod 2 (Cardo). The $116 \times 58\,\text{mm}$ interior sled volume is cleanly split into two specialized chambers:

1. **Forward Chamber ($X = 0 \dots 56\,\text{mm}$): Compact OMM Transceiver PCBA ($55.0 \times 48.0\,\text{mm}$)**
   - 4-layer FR4 TG150 ENIG board carrying the ESP32-C3-WROOM-02U (with native U.FL micro-coax port), Semtech SX1262 LoRa transceiver, u-blox MAX-M10S multi-GNSS engine, Maxim DS2401 ID silicon serial chip, 500mA PTC protection stage, and centered 6-pin precision socket header.
   - Securely fastened via four M2 floor standoffs integrated into the universal base sled ($X = 4.5\,\text{mm}$ and $X = 50.5\,\text{mm}$).
2. **Aft Chamber ($X = 57 \dots 110\,\text{mm}$): Modular Antenna Bracket ([04_antenna_bracket_omm.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/parts/04_antenna_bracket_omm.scad))**
   - Independent PA12 bracket frame secured via the two rear corner posts of the universal base sled.
   - **GNSS (GPS):** Elevated top cradle holding an $18 \times 18\,\text{mm}$ (or $25 \times 25\,\text{mm}$) RHCP ceramic patch antenna facing straight up through the RF-transparent PA12 roof ($0\,\text{dB}$ polarization mismatch loss).
   - **LoRa (868 MHz):** Vertical sidewall bed securing a flexible 868 MHz FPC dipole antenna along the outer enclosure wall (unimpeded RF penetration through PA12).
   - **2.4 GHz Audio Mesh:** Guides the U.FL micro-coax line from the ESP32-C3 directly to the waterproof front/rear SMA bulkhead connector for the high-gain external whip antenna.
3. **Weatherproof Solid PA12 Cover ([03_insert_blindkassette.scad](file:///Users/schmidtm/openMotorBridge/hardware/cad/scad/03_pod_cartridges/parts/03_insert_blindkassette.scad))**
   - Hermetically seals the assembly against rain, dust, and high-pressure vehicle washing (IP67 / IP69K).

### 1.1 3D CAD Assembly & Exploded View

![OpenMotorBridge Rear Pod 3 CAD Assembly Exploded View](../images/cad/pod3_full_assembly_exploded_3d.png)

*Figure 13.2: 3D CAD exploded view of the complete Rear Pod 3 assembly: Universal base sled (with 6 floor standoffs ensuring 100% commonality across all pods), compact OMM PCBA forward, modular antenna bracket aft (holding the zenith GPS patch and sidewall LoRa FPC), and weatherproof solid PA12 top cover.*

---

## 2. Hardware Architecture & End-Wall Mating Interface

```
                      ┌─────────────────────────────────────────────────────────────┐
                      │          REAR POD 3 OPENMOTORMESH TRANSCEIVER MODULE        │
                      │       (110 x 52 mm on the open carrier sled floor)          │
                      │                                                             │
                      │   • J1: Centered 6-Pin Right-Angle Socket on Leading Edge   │
                      │   • F1: 500mA PTC Fuse & D1: 5V Power Status LED            │
                      │   • U4: DS2401 1-Wire ID ROM (openmotormesh_pod3.json)      │
                      │   • J3..J5: 3x Murata MM8030 Auto RF Break-Switches         │
                      │                                                             │
                      │   ┌─────────────────────────────────────────────────────┐   │
                      │   │  ESP32-C3 RISC-V Co-Processor (32-Bit @ 160 MHz)    │   │
                      │   │  • Primary PHY: 2.4 GHz IEEE 802.15.4 / SC-FDMA     │   │
                      │   │  • HiFi Audio (Opus 24k) & Near-Field Mesh          │   │
                      │   └──────────┬───────────────────────────┬──────────────┘   │
                      │              │ SPI Master (8 MHz)        │ UART1 (115.2k)   │
                      │              ▼                           ▼                  │
                      │   ┌──────────────────────┐    ┌─────────────────────────┐   │
                      │   │ Semtech SX1262 LoRa  │    │ u-blox MAX-M10S GNSS    │   │
                      │   │ • Fallback PHY 868MHz│    │ • 10 Hz Multi-GNSS PVT  │   │
                      │   │ • Codec2 & Radar     │    │ • 1-PPS Time Standard   │   │
                      │   └──────────────────────┘    └─────────────────────────┘   │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │ Horizontal Cartridge Slide-in (Auto-Eject)
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ PROTECTIVE BULKHEAD WITH DUAL AUTO-EJECT SPRINGS (2x M2)    │
                      │  • PA12 Partition (56 x 24 mm) seals Pod Base hermetically  │
                      │  • 6-Pin Shrouded Header with 45° Self-Centering Funnel     │
                      │  • Dual V4A Stainless Steel Springs pop sled out by 10mm    │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ POD BASE PCB (openmotorbridge_pod_base, 48 x 24 mm)         │
                      │  • U1: SP3012 TVS Protection Matrix                         │
                      │  • J2: Centered M8 6-Pin IP67 Receptacle on Outside (B.Cu)  │
                      └──────────────────────────────┬──────────────────────────────┘
                                                     │ Shielded 6-Core PUR Harness
                                                     ▼
                      ┌─────────────────────────────────────────────────────────────┐
                      │ HD26 Flange Receptacle -> Main Box ESP32-S3 Host Processor  │
                      └─────────────────────────────────────────────────────────────┘
```

---

## 2. Dual-PHY OpenMotorMesh Matrix in Rear Pod 3

| Feature | **Primary PHY (2.4 GHz High-Speed Mesh)** | **Secondary Fallback PHY (868 MHz LoRa)** |
| :--- | :--- | :--- |
| **Hardware Driver** | **ESP32-C3 Integrated 2.4 GHz Radio** | **Semtech SX1262 Transceiver (+22 dBm)** |
| **Standard / Protocol** | IEEE 802.15.4 / SC-FDMA TDMA (2 Mbps) | LoRa Chirp Spread Spectrum (BW 250 kHz, SF7) |
| **Antenna in Pod 3** | Pulse W3000 2.4 GHz ceramic chip antenna (`ANT3`) + Murata MM8030 switch (`J3`) to SMA | Pulse W3000 868 MHz ceramic chip antenna (`ANT1`) + Murata MM8030 switch (`J4`) to SMA |
| **Audio Codec** | **Opus Speech/Full-Band (24 kbps / 12 kbps)** | **Codec2 (1200 bps / 700 bps PTT Bursts)** |
| **Audio Mode** | **Full-Duplex Continuous (HiFi Voice)** | **Half-Duplex PTT Bursts (220 ms max.)** |
| **Music Sharing** | Yes (A2DP dynamic forwarding @ 64 kbps) | No (bandwidth reserved for voice & SOS) |
| **Telemetry Rate** | 10 Hz real-time dynamics stream | 1 Hz compressed group radar (12 Bytes) |
| **Typical Range** | $150\,\text{m}$ to $300\,\text{m}$ (line-of-sight) | **$1.0\,\text{km}$ to $15.0\,\text{km}$ (multi-hop)** |
| **Primary Role** | Primary group intercom & audio bridge | **Automatic fallback on group separation** |

---

## 3. Core Components in Rear Pod 3

1. **Main Co-Processor (ESP32-C3-WROOM-02U with RF Switch Receptacle):**
   * 32-bit RISC-V single-core @ 160 MHz with 4 MB embedded flash.
   * Transmits and receives **2.4 GHz Primary High-Speed Mesh** (Opus 24k HiFi audio & 10 Hz telemetry).
   * Performs local 10 Hz NMEA/UBX parsing from MAX-M10S and SPI control of the LoRa modem.
2. **GNSS Engine (u-blox MAX-M10S):**
   * Concurrent 4-system multi-constellation operation (GPS, GLONASS, Galileo, BeiDou).
   * 1-PPS hardware timepulse (jitter $< 15\,\text{ns}$ RMS) connected to ESP32-C3 GPIO 6 and female socket contact 5.
3. **OpenMotorMesh LoRa Transceiver (Semtech SX1262):**
   * Frequency Range: 868.0 – 868.6 MHz (EU ISM band) / 915 MHz (US band).
   * Output Power: up to $+22\,\text{dBm}$ ($160\,\text{mW}$ EIRP).
   * Integrated RF switch, low-pass filter, and automatic antenna disconnect switching.
4. **1-Wire Identification (Maxim / ADI DS2401Z+):**
   * Provides 64-bit silicon serial number for automated cartridge detection.
5. **Voltage Regulation (TI TPS7A0533):**
   * Ultra-low-noise automotive LDO (5.0V in $\rightarrow$ clean 3.3V / 200mA for GNSS & LoRa).

---

### 3.1 Universal RF Switch Receptacle Architecture: Automated Antenna Cut-Off

To provide ultimate deployment versatility, **all three RF and navigation paths** on the transceiver board feature miniature **mechanical RF switch receptacles (e.g. Murata MM8030-2610 / SWG Series)**.

```
            OPERATING PRINCIPLE OF MECHANICAL RF SWITCH RECEPTACLES
  1. UNMATED (No cable plugged in)         2. MATED (Pigtail to external SMA bulkhead)
┌──────────────────────────────────────┐ ┌──────────────────────────────────────┐
│  RF-IC ──► [Spring Leaf] ──► Ant     │ │  RF-IC ──► [Center Pin] ──► Ext SMA  │
│            (Closed/Normal) (Internal)│ │            (Lifted!)        (External)│
│                                      │ │            [Isolated] ─X─► Ant       │
└──────────────────────────────────────┘ └──────────────────────────────────────┘
```

#### The Mechanical Switching Principle:
* **Unmated (Default Internal Operation):** An internal phosphor-bronze spring leaf connects the RF transceiver output with near-zero loss ($< 0.08\,\text{dB}$) directly to the onboard antenna (Pulse W3000 ceramic chip or PCB trace).
* **Mated (Coaxial Pigtail Inserted):** Inserting the coaxial pigtail plug physically deflects the spring leaf:
  * The connection to the onboard antenna is **mechanically broken and completely isolated** ($> 20\,\text{dB}$ isolation).
  * 100% of RF transmission power flows directly into the coaxial cable toward the external waterproof SMA bulkhead on the faceplate.
* **Extraction:** When unplugged, the spring leaf immediately snaps back—instantly restoring internal antenna operation with zero soldering or manual bridging!

#### The Three On-Board Switch Receptacles & Mating Scenarios:
1. **Receptacle `J3` (2.4 GHz Primary High-Speed Mesh – ESP32-C3) ──► [FACTORY DEFAULT]:**
   * The internal pigtail to the SMA faceplate bulkhead is **plugged into `J3` by default**.
   * **Why 2.4 GHz is the Primary Default:** 2.4 GHz carries high-bandwidth **Opus HiFi full-duplex audio** and naturally suffers the shortest physical range ($150\dots 300\,\text{m}$ with internal antennas). Adding an ultra-compact 2.4 GHz stub aerial ($\approx 30\,\text{mm}$ tall) boosts crystal-clear voice range to **$600\dots 1,000\,\text{m}$**. The riding group stays in pristine stereo voice chat across large convoy gaps without dropping into low-bandwidth LoRa emergency mode.
2. **Receptacle `J4` (868 MHz LoRa Fallback – Semtech SX1262):**
   * Operates autonomously via its onboard Pulse W3000 ceramic antenna ($1\dots 2.5\,\text{km}$ LoRa range).
   * **Expedition Setup:** For trans-continental tours or desert expeditions, the rider can move the pigtail from `J3` to `J4`. `J3` automatically restores its internal 2.4 GHz antenna, while LoRa is routed to the external aerial for **$> 25\,\text{km}$ long-range multi-hop coverage**.
3. **Receptacle `J5` (Multi-GNSS – u-blox MAX-M10S):**
   * Operates autonomously via its onboard GNSS ceramic antenna.
   * **Pannier / Luggage Shielding Setup:** If heavy aluminum cases or dry-bags completely cover the rear pod, the pigtail can be plugged into `J5` to feed an external active GNSS antenna on the tail tip.

---

## 4. Internal ESP32-C3 GPIO Pin Mapping

| ESP32-C3 GPIO | Peripheral / Signal | Direction | Function |
| :--- | :--- | :---: | :--- |
| **GPIO 21** | `BRIDGE_TXD` | Output | High-Speed UART0 Tx to Central Box (460,800 Baud) |
| **GPIO 20** | `BRIDGE_RXD` | Input | High-Speed UART0 Rx from Central Box (460,800 Baud) |
| **GPIO 4** | `GNSS_TXD` | Output | UART1 Tx to u-blox MAX-M10S (115,200 Baud) |
| **GPIO 5** | `GNSS_RXD` | Input | UART1 Rx from u-blox MAX-M10S (115,200 Baud) |
| **GPIO 6** | `GNSS_PPS` | Input (IRQ) | 1-PPS Hardware Timepulse Interrupt |
| **GPIO 8** | `LORA_SCK` | Output | SX1262 SPI Clock (8 MHz) |
| **GPIO 9** | `LORA_MISO`| Input | SX1262 SPI Master-In Slave-Out |
| **GPIO 10** | `LORA_MOSI`| Output | SX1262 SPI Master-Out Slave-In |
| **GPIO 7** | `LORA_NSS` | Output | SX1262 SPI Chip Select |
| **GPIO 3** | `LORA_NRST`| Output | SX1262 Hardware Reset |
| **GPIO 2** | `LORA_BUSY`| Input | SX1262 Status Busy |
| **GPIO 1** | `LORA_DIO1`| Input (IRQ) | SX1262 Packet Received / Transmit Done Interrupt |

---

## 5. 6-Pin Pogo Contact Interface Pinout

| Pogo Pin | Signal Name | Electrical Specification | Description |
| :---: | :--- | :--- | :--- |
| **Pin 1** | `POD3_VCC` | 5.0 V DC (max. 250 mA) | Continuous 5V power from Central Box |
| **Pin 2** | `POD3_GND` | Power & Signal Ground | Dedicated return path |
| **Pin 3** | `POD3_UART_TX` | 3.3 V LVTTL (460,800 Baud) | Stream from ESP32-C3 to Central Box |
| **Pin 4** | `POD3_UART_RX` | 3.3 V LVTTL (460,800 Baud) | Commands from Central Box to ESP32-C3 |
| **Pin 5** | `POD3_GNSS_PPS`| 3.3 V pulse (100 ms width) | 1-PPS hardware time synchronization |
| **Pin 6** | `POD3_1WIRE_ID`| 1-Wire Open-Drain (3.3 V) | DS2401 cartridge identification bus |

---

## 6. Protocol Specification (Rear Pod $\leftrightarrow$ Central Box)

Communication across the 460,800 Baud bridge is packet-oriented with CRC16-CCITT checksum:

```
┌──────┬──────┬──────┬──────┬─────────────────┬──────┬──────┐
│ SYNC │ TYPE │ LEN  │ SEQ  │ PAYLOAD (0..n)  │ CRC16-CCITT  │
│ 0xAA │ 0x55 │ 1 B  │ 1 B  │ Variable        │ 2 Bytes      │
└──────┴──────┴──────┴──────┴─────────────────┴──────┴──────┘
```

### Message Types:
* **`0x01` - GNSS PVT Telemetry (10 Hz):** Pre-compressed binary vector with Latitude, Longitude, Altitude, Speed, Heading, PDOP, and Satellite stats.
* **`0x02` - OMM 2.4 GHz Primary Audio Frame:** Opus 24k/12k frame from 2.4 GHz proximity mesh.
* **`0x03` - OMM 868 MHz LoRa Fallback Frame:** Codec2 audio or radar packet from long-range fallback.
* **`0x04` - OMM Tx Request (Dual-PHY):** Transmit command from Central Box to 2.4 GHz mesh or SX1262 LoRa.
* **`0x05` - DLE Status & Link Quality:** Signal-to-Noise Ratio (SNR), RSSI, active PHY mode (2.4G vs 868M), and node DLE score.
* **`0xFE` - Bootloader Jump / Flasher Trigger:** Forces ESP32-C3 into ROM download mode for UART push-flashing.

---

## 7. In-System Firmware Flashing & Production Test Interface

To ensure straightforward initial flashing in the factory and seamless in-system updates at the motorcycle:

### 7.1 In-System UART Push-Flashing (Operational)
* During active motorcycle operation, firmware updates are pushed directly by the Central Box (`firmware/main_controller/src/omm_flasher.cpp`) over `UART_TX` and `UART_RX` at 460,800 baud.
* The Central Box resets the ESP32-C3 via the switched `POD3_PWR_EN` power line and synchronizes using standard ESP-ROM SLIP frames.
* **Flash duration:** $< 6\,\text{seconds}$ for $850\,\text{kB}$ firmware binary with verified MD5 checksum.

### 7.2 Bottom-Layer Production Test Points (`B.Cu`)
For End-of-Line (EOL) testing on the manufacturing bed of nails without soldering cables:
* **`TP1` (`TP_BOOT`):** ESP32-C3 GPIO9 (Pull to GND for manual ROM bootloader entry).
* **`TP2` (`TP_RST`):** ESP32-C3 CHIP_EN / Hardware Reset.
* **`TP3` (`TP_TX`):** Direct ESP32-C3 U0TXD test pad.
* **`TP4` (`TP_RX`):** Direct ESP32-C3 U0RXD test pad.

---

## 8. Roadmap & Upgrade Path: Optional LTE-M / 4G Cloud Cartridge & RF Triplexer

### 8.1 Status Quo V1 (Focused on Reliability & Zero Running Costs)
In Version 1, Rear Pod 3 focuses strictly on **robust, zero-cost ad-hoc mesh networking**:
* **3x Onboard Ceramic Chip Antennas (Pulse W3000):** Fully encapsulated inside the PA12 enclosure for $868\,\text{MHz}$ LoRa, $1575\,\text{MHz}$ GNSS, and $2.4\,\text{GHz}$ Mesh/BLE.
* **3x Murata MM8030 RF Switch Jacks:** Allow selective routing of individual radio paths to an external SMA antenna connector.
* **Smartphone as Cloud Gateway:** All cloud features (live telemetry, WebApp mapping, crash alerting) run cost-free through the rider's smartphone linked via the Smart Fairing Hub.

### 8.2 Upgrade Path V2: Autonomous LTE-M / NB-IoT Cloud Cartridge
Thanks to the modular 1-tier cartridge concept, the system can later be upgraded to a standalone IoT cloud tracker without modifying motorcycle wiring or base pod enclosures:

1. **Optional Cartridge PCB (`cartridge_omm_transceiver_lte`):**
   * Incorporates an ultra-compact LTE Cat-1 bis / LTE-M IoT modem (e.g. *Quectel EG915N* or *SIMCom SIM7080G*) onto the spacious $110 \times 52\,\text{mm}$ carrier.
   * **Connectivity:** Integrated eSIM or Nano-SIM (e.g. *1NCE IoT Flat*: 10 € for 10 years / 500 MB data with no monthly fees).
2. **RF Triplexer (Single-Feed Broadband Antenna):**
   * Instead of three discrete antennas or manual selector switches, the V2 board cascades two miniature LTCC ceramic diplexers (0603 footprint):
     * *Diplexer 1:* Splits $868\,\text{MHz}$ LoRa / LTE low band.
     * *Diplexer 2:* Splits $1575\,\text{MHz}$ GNSS and $2400\,\text{MHz}$ mesh / LTE high band.
     * *GNSS Protection:* A SAW bandpass filter with $> 50\,\text{dB}$ out-of-band attenuation shields the u-blox LNA from LoRa and LTE transmit desensitization.
   * **Antenna:** A single external broadband antenna ($700 \dots 2700\,\text{MHz}$, e.g. Taoglas / Pulse LTE whip) feeds all three transceivers simultaneously.
3. **Advanced V2 Capabilities:**
   * **Autonomous eCall Crash Notification:** Sends emergency SMS and GPS coordinates to rescue dispatch upon IMU tip-over detection—even if the smartphone is destroyed or thrown from the bike.
   * **Anti-Theft Geofencing & Motion Alert:** Transmits silent alarm notifications and battery status if the parked motorcycle is disturbed.
   * **Infinite Group Mesh Relay:** Seamlessly routes voice and position data over MQTT / cellular whenever LoRa line-of-sight is lost across mountain ranges.


