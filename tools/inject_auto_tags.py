#!/usr/bin/env python3
import re, sys

PATH = "docs/de/07_pcba_hardware_pinouts.md"

with open(PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. PCBA_01:
# Insert AUTO_CONNECTORS under 3.2
text = text.replace(
    "### 3.2 Platinen-Steckverbinder & Exakte Pinbelegung\n",
    "### 3.2 Platinen-Steckverbinder & Exakte Pinbelegung\n\n<!-- AUTO_CONNECTORS_START: PCBA_01 -->\n<!-- AUTO_CONNECTORS_END: PCBA_01 -->\n"
)
# Insert AUTO_SUBCHIPS under 3.3
text = text.replace(
    "### 3.3 Microchip USB2517I-JZX 7-Port Hub Architektur (`U8`)\n",
    "### 3.3 Sub-Chips & Peripherie-Bausteine (USB2517I, QCC3084, SX1262, TCAN334G)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_01 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_01 -->\n\n### 3.4 Microchip USB2517I-JZX 7-Port Hub Architektur (`U8`)\n"
)

# 2. PCBA_03:
# Replace the connector section 5.2 - 5.5 in PCBA_03
pcba03_target_start = "### 5.2 Pinbelegung des 4-Pin Bus-Eingangs (`J_BUS` / 4-Pin JST-GH 1.25mm)"
pcba03_replacement = """### 5.2 Externe Steckverbinder & Schnittstellen (J_BUS, J_USB_OUT, J_ACT, J_AUDIO_PWR)

<!-- AUTO_CONNECTORS_START: PCBA_03 -->
<!-- AUTO_CONNECTORS_END: PCBA_03 -->

### 5.3 Sub-Chips & Peripherie-Bausteine (CH554E, TS5A23157, ES8388)

<!-- AUTO_SUBCHIPS_START: PCBA_03 -->
<!-- AUTO_SUBCHIPS_END: PCBA_03 -->

### 5.4 ESP32-C6-MINI-1U (`U1`) Vollständige Pinout-Matrix

<!-- AUTO_PINOUT_START: PCBA_03 -->
<!-- AUTO_PINOUT_END: PCBA_03 -->

### 5.5 Funktionsweise der Hardware- und Protokoll-Umschaltung"""

text = text.replace(pcba03_target_start, pcba03_replacement)

# 3. PCBA_05:
# Add AUTO_CONNECTORS and AUTO_SUBCHIPS around 7.1.3
text = text.replace(
    "#### 7.1.3 Pinbelegung Header J4: Handschuhfach-Hub Lifeline (JST-GH 1.25mm 8-Pin Horizontal)",
    "### 7.1.4 Externe Steckverbinder & Schnittstellen (J1..J11)\n\n<!-- AUTO_CONNECTORS_START: PCBA_05 -->\n<!-- AUTO_CONNECTORS_END: PCBA_05 -->\n\n### 7.1.5 Sub-Chips & Peripherie-Bausteine (USB2514Bi, C3-Bridge)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_05 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_05 -->\n\n#### 7.1.6 Detail-Pinbelegung Header J4: Handschuhfach-Hub Lifeline (JST-GH 1.25mm 8-Pin Horizontal)"
)

# 4. PCBA_07:
# Replace Section 9.2 table with AUTO tags
pcba07_target = "### 9.2 Vollständige Pinbelegung des ESP32-C3FH4 SoC (PCBA 07 `U1`)"
pcba07_replacement = """### 9.2 Vollständige Pinbelegung des ESP32-C3FH4 SoC (PCBA 07 `U1`)

<!-- AUTO_PINOUT_START: PCBA_07 -->
<!-- AUTO_PINOUT_END: PCBA_07 -->

### 9.3 Sub-Chips & Peripherie-Bausteine (SX1262 LoRa & BQ51050B Qi-Lader)

<!-- AUTO_SUBCHIPS_START: PCBA_07 -->
<!-- AUTO_SUBCHIPS_END: PCBA_07 -->

### 9.4 Externe Steckverbinder (J1 LiPo, J3 Qi-Spule)

<!-- AUTO_CONNECTORS_START: PCBA_07 -->
<!-- AUTO_CONNECTORS_END: PCBA_07 -->"""

text = text.replace(pcba07_target, pcba07_replacement)

# 5. PCBA_08:
text = text.replace(
    "### 10.3 Steckverbinder-Pinbelegung\n",
    "### 10.3 Steckverbinder-Pinbelegung\n\n<!-- AUTO_CONNECTORS_START: PCBA_08 -->\n<!-- AUTO_CONNECTORS_END: PCBA_08 -->\n"
)
text = text.replace(
    "### 10.4 Vollständige Pinbelegung der Host-MCU U1 (ESP32-C5-WROOM-1U)\n",
    "### 10.4 Vollständige Pinbelegung der Host-MCU U1 (ESP32-C5-WROOM-1U)\n\n<!-- AUTO_PINOUT_START: PCBA_08 -->\n<!-- AUTO_PINOUT_END: PCBA_08 -->\n\n### 10.4.1 Sub-Chips (Wheeltec MR20 77GHz Radar)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_08 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_08 -->\n"
)

# 6. PCBA_09:
text = text.replace(
    "### 11.3 Vollständige GPIO-Pinbelegung (ESP32-C6-MINI-1U)\n",
    "### 11.3 Vollständige GPIO-Pinbelegung (ESP32-C6-MINI-1U)\n\n<!-- AUTO_PINOUT_START: PCBA_09 -->\n<!-- AUTO_PINOUT_END: PCBA_09 -->\n\n### 11.3.1 Sub-Chips (ES8388 Codec & BQ24075 Lader)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_09 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_09 -->\n"
)
text = text.replace(
    "### 11.4 Belegung des 16-Pin Multi-Use USB-C Steckverbinders (`J1`)\n",
    "### 11.4 Externe Steckverbinder (J1 USB-C & J2 Helm-Audio)\n\n<!-- AUTO_CONNECTORS_START: PCBA_09 -->\n<!-- AUTO_CONNECTORS_END: PCBA_09 -->\n\n#### 11.4.1 Detailbeschreibung Multi-Use USB-C (`J1`)\n"
)

# 7. PCBA_10:
text = text.replace(
    "### 12.3 Vollständige GPIO-Pinbelegung (ESP32-C6 zu SA818-DMR & Peripherie)\n",
    "### 12.3 Vollständige GPIO-Pinbelegung (ESP32-C6 zu SA818-DMR & Peripherie)\n\n<!-- AUTO_PINOUT_START: PCBA_10 -->\n<!-- AUTO_PINOUT_END: PCBA_10 -->\n\n### 12.3.1 Sub-Chips (SA818-DMR & ES8388 Codec)\n\n<!-- AUTO_SUBCHIPS_START: PCBA_10 -->\n<!-- AUTO_SUBCHIPS_END: PCBA_10 -->\n"
)
text = text.replace(
    "### 12.4 Belegung des 16-Pin Multi-Use USB-C Steckverbinders (`J1`)\n",
    "### 12.4 Externe Steckverbinder (J1 USB-C & J2 Helm-Audio)\n\n<!-- AUTO_CONNECTORS_START: PCBA_10 -->\n<!-- AUTO_CONNECTORS_END: PCBA_10 -->\n\n#### 12.4.1 Detailbeschreibung Multi-Use USB-C (`J1`)\n"
)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("✅ Successfully injected AUTO tags into docs/de/07_pcba_hardware_pinouts.md!")
