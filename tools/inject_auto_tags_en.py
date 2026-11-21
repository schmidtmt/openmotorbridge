#!/usr/bin/env python3
import os

PATH = "docs/en/07_pcba_hardware_pinouts.md"
if not os.path.exists(PATH):
    print(f"Error: {PATH} not found")
    exit(1)

with open(PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. PCBA_01:
text = text.replace(
    "### 3.2 PCB Connectors & Exact Pinout Tables\n",
    "### 3.2 PCB Connectors & Exact Pinout Tables\n\n<!-- AUTO_CONNECTORS_START: PCBA_01 -->\n<!-- AUTO_CONNECTORS_END: PCBA_01 -->\n"
)
text = text.replace(
    "### 3.3 Microchip USB2517I-JZX 7-Port Hub Architecture (`U8`)\n",
    "### 3.3 Sub-Chips & Peripheral Components (USB2517I, QCC3084, SX1262, TCAN334G)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_01 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_01 -->\n\n### 3.4 Microchip USB2517I-JZX 7-Port Hub Architecture (`U8`)\n"
)

# 2. PCBA_03:
pcba03_target_start = "### 5.2 Pinout of 4-Pin Bus Input (`J_BUS` / 4-Pin JST-GH 1.25mm)"
pcba03_replacement = """### 5.2 External Connectors & Interfaces (J_BUS, J_USB_OUT, J_ACT, J_AUDIO_PWR)

<!-- AUTO_CONNECTORS_START: PCBA_03 -->
<!-- AUTO_CONNECTORS_END: PCBA_03 -->

### 5.3 Sub-Chips & Peripheral Components (CH554E, TS5A23157, ES8388)

<!-- AUTO_SUBCHIPS_START: PCBA_03 -->
<!-- AUTO_SUBCHIPS_END: PCBA_03 -->

### 5.4 ESP32-C6-MINI-1U (`U1`) Complete Pinout Matrix

<!-- AUTO_PINOUT_START: PCBA_03 -->
<!-- AUTO_PINOUT_END: PCBA_03 -->

### 5.5 Hardware Switching & 3.0 Mbps Bridge Operation"""
text = text.replace(pcba03_target_start, pcba03_replacement)

# 3. PCBA_05:
text = text.replace(
    "### 7.1.3 ESP32-C3FH4 (`U10`) Auxiliary MCU Pinout Matrix (USB Audio / SkylineOS Headset Bridge)",
    "### 7.1.4 External Connectors & Interfaces (J1..J11)\n\n<!-- AUTO_CONNECTORS_START: PCBA_05 -->\n<!-- AUTO_CONNECTORS_END: PCBA_05 -->\n\n### 7.1.5 Sub-Chips & Peripherals (USB2514Bi, C3-Bridge)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_05 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_05 -->\n\n### 7.1.3 ESP32-C3FH4 (`U10`) Auxiliary MCU Pinout Matrix (USB Audio / SkylineOS Headset Bridge)"
)

# 4. PCBA_07:
pcba07_target = "### 9.2 Complete Interface & Pin-Mapping of ESP32-C3FH4 SoC (PCBA 07 `U1`)"
pcba07_replacement = """### 9.2 Complete Interface & Pin-Mapping of ESP32-C3FH4 SoC (PCBA 07 `U1`)

<!-- AUTO_PINOUT_START: PCBA_07 -->
<!-- AUTO_PINOUT_END: PCBA_07 -->

### 9.3 Sub-Chips & Peripherals (SX1262 LoRa & BQ51050B Qi Charger)

<!-- AUTO_SUBCHIPS_START: PCBA_07 -->
<!-- AUTO_SUBCHIPS_END: PCBA_07 -->

### 9.4 External Connectors (J1 LiPo, J3 Qi Coil)

<!-- AUTO_CONNECTORS_START: PCBA_07 -->
<!-- AUTO_CONNECTORS_END: PCBA_07 -->"""
text = text.replace(pcba07_target, pcba07_replacement)

# 5. PCBA_08:
text = text.replace(
    "### 10.3 Connector Pinout Definitions\n",
    "### 10.3 Connector Pinout Definitions\n\n<!-- AUTO_CONNECTORS_START: PCBA_08 -->\n<!-- AUTO_CONNECTORS_END: PCBA_08 -->\n"
)
text = text.replace(
    "### 10.4 Complete Pinout of Host MCU U1 (ESP32-C5-WROOM-1U)\n",
    "### 10.4 Complete Pinout of Host MCU U1 (ESP32-C5-WROOM-1U)\n\n<!-- AUTO_PINOUT_START: PCBA_08 -->\n<!-- AUTO_PINOUT_END: PCBA_08 -->\n\n### 10.4.1 Sub-Chips (Wheeltec MR20 77GHz Radar)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_08 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_08 -->\n"
)

# 6. PCBA_09:
text = text.replace(
    "### 11.3 Complete GPIO Pinout (ESP32-C6-MINI-1U)\n",
    "### 11.3 Complete GPIO Pinout (ESP32-C6-MINI-1U)\n\n<!-- AUTO_PINOUT_START: PCBA_09 -->\n<!-- AUTO_PINOUT_END: PCBA_09 -->\n\n### 11.3.1 Sub-Chips (ES8388 Codec & BQ24075 Charger)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_09 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_09 -->\n"
)
text = text.replace(
    "### 11.4 16-Pin Multi-Use USB-C Connector Pinout (`J1`)\n",
    "### 11.4 External Connectors (J1 USB-C & J2 Helmet Audio)\n\n<!-- AUTO_CONNECTORS_START: PCBA_09 -->\n<!-- AUTO_CONNECTORS_END: PCBA_09 -->\n\n#### 11.4.1 Multi-Use USB-C Details (`J1`)\n"
)

# 7. PCBA_10:
text = text.replace(
    "### 12.3 Complete GPIO Pinout (ESP32-C6 to SA818-DMR & Periphery)\n",
    "### 12.3 Complete GPIO Pinout (ESP32-C6 to SA818-DMR & Periphery)\n\n<!-- AUTO_PINOUT_START: PCBA_10 -->\n<!-- AUTO_PINOUT_END: PCBA_10 -->\n\n### 12.3.1 Sub-Chips (SA818-DMR & ES8388 Codec)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_10 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_10 -->\n"
)
text = text.replace(
    "### 12.4 16-Pin Multi-Use USB-C Connector Pinout (`J1`)\n",
    "### 12.4 External Connectors (J1 USB-C & J2 Helmet Audio)\n\n<!-- AUTO_CONNECTORS_START: PCBA_10 -->\n<!-- AUTO_CONNECTORS_END: PCBA_10 -->\n\n#### 12.4.1 Multi-Use USB-C Details (`J1`)\n"
)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Injected AUTO tags into docs/en/07_pcba_hardware_pinouts.md!")
