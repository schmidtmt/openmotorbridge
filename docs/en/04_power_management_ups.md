# 04 - Power Management, UPS, Undervoltage Protection & Winter Storage

## 1. Primary Buck Converter
- **Regulator IC:** Texas Instruments LM5164-Q1 Synchronous Step-Down Regulator (Automotive Grade AEC-Q100).
- **Input Voltage Range:** 6.0 V to 65 V DC continuous (transient protection per ISO 7637-2 up to 100 V).
- **Output Capability:** 5.0 V DC / 1.0 A continuous power for system, satellite pods, and LiPo charger.
- **Efficiency:** > 88% in primary load range (12 V to 5 V @ 400 mA).

## 2. Dynamic Power-Path Management & Integrated UPS
- **Power-Path Controller:** Texas Instruments BQ24075 with automatic load and charge current distribution.
- **UPS Battery Cell:** 1000 mAh wide-temperature single-cell LiPo battery (3.7 V nominal, 4.2 V charge termination, discharge range -20 °C to +60 °C).
- **JEITA NTC Thermal Control (Murata 10k NTC on BQ24075 TS Pin):**
  - **Cold Inhibit ($T < 0\,^\circ\text{C}$):** Hardware charge current cut to 0 mA to prevent lithium plating and dendrite growth in sub-zero winter temperatures.
  - **Heat Inhibit ($T > 45\,^\circ\text{C}$):** Hardware charge current cut to 0 mA to protect the battery from engine heat under the seat.
- **Seamless Switchover:** In case of vehicle ignition cut-off (KL15/KL30 lost), the BQ24075 switches to internal LiPo within $< 5\,\mu\text{s}$ without any glitch on the 3.3V LDO line.
- **Graceful Shutdown Period:** Allows 60 to 120 seconds of continuous operation after ignition off for:
  - Finalizing and flushing GPX track logs to MicroSD.
  - Connecting to home Wi-Fi and performing TLS 1.3 WebDAV auto-upload.
  - Cleanly broadcasting BLE disconnect events.

## 3. Automotive Transient, EMC & Reverse Polarity Protection
- **Input Fuse:** Bourns MF-MSMF050-2 resettable PPTC fuse (1812 SMD, 500 mA hold / 1.0 A trip).
- **Surge & Spike Clamp:** Littelfuse SMBJ33CA bidirectional TVS diode (33 V standoff, 53.3 V max clamping) -> provides $> 11.7\,\text{V}$ safety headroom below the LM5164's 65 V maximum rating during ISO 16750-2 load dump events.
- **Reverse Polarity Protection:** Diodes Inc. DMP6023L P-Channel MOSFET with low on-resistance ($R_{\text{DS(on)}} < 25\,\text{m}\Omega$).
- **Filtering:** Two-stage LC-PI filter (10 µH shielded automotive inductor + 2x 10 µF X7R 100V ceramic capacitors).

## 4. Vehicle Battery Monitoring & Winter Storage

### 4.1 Voltage Sensing & Battery Chemistry
Vehicle voltage on KL15 and KL30 is monitored via precision voltage dividers (100 kΩ / 10 kΩ, 0.1% tolerance, 1:11 ratio) at `PIN_ADC_VIGN` (GPIO 4). 5 starter battery chemistries are supported:

| Battery Chemistry | Nominal Voltage | Charging (Engine ON) | Low-Bat Warning | Hard Cut-Off (Protection) |
| :--- | :---: | :---: | :---: | :---: |
| **Standard Flooded Lead-Acid (Wet)** | 12.0 V - 12.6 V | 14.2 V - 14.4 V | 11.9 V | **11.6 V** |
| **AGM (Absorbent Glass Mat)** | 12.6 V - 12.8 V | 14.4 V - 14.7 V | 12.0 V | **11.8 V** |
| **Gel Battery** | 12.6 V - 12.8 V | 14.1 V - 14.4 V | 12.0 V | **11.8 V** |
| **LiFePO4 (Lithium Iron Phosphate)** | 13.2 V - 13.3 V | 14.4 V - 14.6 V | 13.0 V | **12.8 V** |
| **Li-Ion (NMC Starter Battery)** | 11.1 V - 12.6 V | 12.6 V - 13.0 V | 10.8 V | **10.5 V** |

### 4.2 Multi-Stage Power Saving & Winter Storage Logic
1. **Stage 1 - Normal Standby (KL15 = OFF, KL30 > Cut-Off):** ESP32-S3 in light sleep / deep sleep with wake-up on KL15 rising edge. Quiescent current: $< 1.2\,\text{mA}$.
2. **Stage 2 - Low-Battery Deep Sleep (KL30 < Cut-Off):** Disables all power gates and enters ULP deep sleep ($< 25\,\mu\text{A}$).
3. **Stage 3 - Winter-Storage-Mode (Long-term multi-month parking):** After $> 14$ days of continuous parking, system remains in ultra-low quiescent state ($< 25\,\mu\text{A}$), preventing starter battery drain over 5 to 6 months of sub-zero winter storage.
