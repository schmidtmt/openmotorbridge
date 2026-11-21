#!/usr/bin/env python3
"""
tools/generate_pinout_docs.py
=============================
Synchronizes Markdown pinout documentation tables from the Single Source of Truth (SSOT):
  data/pcba_pinouts.json

Supports automated injection of:
  - MCU / Main Module Pinouts:   <!-- AUTO_PINOUT_START: BOARD_ID --> ... <!-- AUTO_PINOUT_END: BOARD_ID -->
  - Sub-Chips & Peripherals:     <!-- AUTO_SUBCHIPS_START: BOARD_ID --> ... <!-- AUTO_SUBCHIPS_END: BOARD_ID -->
  - External Connectors:         <!-- AUTO_CONNECTORS_START: BOARD_ID --> ... <!-- AUTO_CONNECTORS_END: BOARD_ID -->

Usage:
  python3 tools/generate_pinout_docs.py         # Syncs docs/de/07_pcba_hardware_pinouts.md & docs/en/07_pcba_hardware_pinouts.md
"""

import json
import os
import re
import sys

JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/pcba_pinouts.json")
OUTPUT_DE = os.path.join(os.path.dirname(__file__), "../docs/de/07_pcba_hardware_pinouts.md")
OUTPUT_EN = os.path.join(os.path.dirname(__file__), "../docs/en/07_pcba_hardware_pinouts.md")

def render_mcu_table(b, lang="de"):
    pins = b.get("pins", [])
    if not pins:
        return ""
    
    lines = []
    if lang == "de":
        lines.append("| Pad | Signal / KiCad Net | ESP32 GPIO | Firmware Define | Ziel / IC | Signal-Typ & Elektr. Spezifikation |")
        lines.append("| :---: | :--- | :---: | :--- | :--- | :--- |")
    else:
        lines.append("| Pad | Signal / KiCad Net | ESP32 GPIO | Firmware Define | Target / IC | Signal Type & Electrical Spec |")
        lines.append("| :---: | :--- | :---: | :--- | :--- | :--- |")
        
    for p in pins:
        pad = str(p.get("pad", "-"))
        net = f"`{p['net']}`" if p.get("net") else "-"
        gpio = f"GPIO {p['gpio']}" if p.get("gpio") is not None else "-"
        fw = f"`{p['fw_define']}`" if p.get("fw_define") else "-"
        target = p.get("target", "-")
        
        desc = p.get("description", "-")
        sig_type = p.get("signal_type")
        if sig_type:
            detail = f"**{sig_type}** – {desc}"
        else:
            detail = desc
            
        lines.append(f"| {pad} | {net} | {gpio} | {fw} | {target} | {detail} |")
        
    return "\n".join(lines)

def render_subchips_tables(b, lang="de"):
    sub_chips = b.get("sub_chips", {})
    if not sub_chips:
        return ""
    
    blocks = []
    for sc_key, sc in sub_chips.items():
        lines = []
        name = sc.get("name", sc_key)
        ref = sc.get("ref", sc_key)
        pkg = sc.get("package", "")
        ds_url = sc.get("datasheet_url")
        pin_url = sc.get("pin_description_url", ds_url)
        table_ref = sc.get("table_ref", "Pinout & Pin Functions")
        
        lines.append(f"#### Sub-Chip `{ref}`: {name} ({pkg})")
        if ds_url:
            if lang == "de":
                lines.append(f"> **Hersteller-Datenblatt:** [{name}]({ds_url}) | **Pin-Definition:** [{table_ref}]({pin_url})  ")
            else:
                lines.append(f"> **Manufacturer Datasheet:** [{name}]({ds_url}) | **Pin Definitions:** [{table_ref}]({pin_url})  ")
        lines.append("")
        
        if lang == "de":
            lines.append("| Pad | Pin-Name | Signal / KiCad Net | Signal-Typ | Ziel / Quelle | Funktion & Elektr. Spezifikation |")
            lines.append("| :---: | :--- | :--- | :---: | :--- | :--- |")
        else:
            lines.append("| Pad | Pin Name | Signal / KiCad Net | Signal Type | Target / Source | Function & Electrical Spec |")
            lines.append("| :---: | :--- | :--- | :---: | :--- | :--- |")
        
        for p in sc.get("pins", []):
            pad = str(p.get("pad", "-"))
            pname = p.get("pin_name", "-")
            net = f"`{p['net']}`" if p.get("net") else "-"
            stype = p.get("type", "-")
            target = p.get("target", "-")
            spec = p.get("spec", "-")
            lines.append(f"| {pad} | `{pname}` | {net} | **{stype}** | {target} | {spec} |")
            
        blocks.append("\n".join(lines))
        
    return "\n\n".join(blocks)

def render_connectors_tables(b, lang="de"):
    connectors = b.get("connectors", {})
    if not connectors:
        return ""
        
    blocks = []
    for c_key, c in connectors.items():
        lines = []
        ref = c.get("ref", c_key)
        name = c.get("name", "")
        ctype = c.get("type", "")
        mating = c.get("mating", "")
        
        if lang == "de":
            lines.append(f"#### Stecker `{ref}`: {name}")
        else:
            lines.append(f"#### Connector `{ref}`: {name}")
        meta_info = []
        if ctype:
            meta_info.append(f"**Typ:** `{ctype}`" if lang == "de" else f"**Type:** `{ctype}`")
        if mating:
            meta_info.append(f"**Gegenstecker:** `{mating}`" if lang == "de" else f"**Mating Connector:** `{mating}`")
        if meta_info:
            lines.append(f"> {' | '.join(meta_info)}  ")
        lines.append("")
        
        if lang == "de":
            lines.append("| Pin | Signal / KiCad Net | Signal-Typ | Elektrische Spezifikation & Funktion |")
            lines.append("| :---: | :--- | :---: | :--- |")
        else:
            lines.append("| Pin | Signal / KiCad Net | Signal Type | Electrical Specification & Function |")
            lines.append("| :---: | :--- | :---: | :--- |")
        
        for p in c.get("pins", []):
            pin = str(p.get("pin", "-"))
            net = f"`{p['net']}`" if p.get("net") else "-"
            stype = p.get("type", "-")
            spec = p.get("spec", "-")
            lines.append(f"| **{pin}** | {net} | **{stype}** | {spec} |")
            
        blocks.append("\n".join(lines))
        
    return "\n\n".join(blocks)

def sync_markdown_file(doc_path, boards_data, lang="de"):
    if not os.path.exists(doc_path):
        print(f"Warning: {doc_path} not found, skipping.")
        return 0
        
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = 0

    # 1. MCU Pinouts
    pattern_mcu = re.compile(r"(<!-- AUTO_PINOUT_START:\s*([A-Za-z0-9_]+)\s*-->)(.*?)(<!-- AUTO_PINOUT_END:\s*\2\s*-->)", re.DOTALL)
    def _replace_mcu(match):
        nonlocal replacements
        tag_start = match.group(1)
        board_id = match.group(2).strip()
        tag_end = match.group(4)
        b = boards_data.get(board_id) or boards_data.get(board_id.replace(" ", "_"))
        if b:
            table_md = render_mcu_table(b, lang)
            replacements += 1
            return f"{tag_start}\n\n{table_md}\n\n{tag_end}"
        return match.group(0)
    content = pattern_mcu.sub(_replace_mcu, content)

    # 2. Sub-Chips
    pattern_sc = re.compile(r"(<!-- AUTO_SUBCHIPS_START:\s*([A-Za-z0-9_]+)\s*-->)(.*?)(<!-- AUTO_SUBCHIPS_END:\s*\2\s*-->)", re.DOTALL)
    def _replace_sc(match):
        nonlocal replacements
        tag_start = match.group(1)
        board_id = match.group(2).strip()
        tag_end = match.group(4)
        b = boards_data.get(board_id) or boards_data.get(board_id.replace(" ", "_"))
        if b and b.get("sub_chips"):
            table_md = render_subchips_tables(b, lang)
            replacements += 1
            return f"{tag_start}\n\n{table_md}\n\n{tag_end}"
        elif b:
            replacements += 1
            empty_msg = "*Keine separaten Sub-Chips auf dieser Baugruppe.*" if lang == "de" else "*No separate sub-chips on this assembly.*"
            return f"{tag_start}\n\n{empty_msg}\n\n{tag_end}"
        return match.group(0)
    content = pattern_sc.sub(_replace_sc, content)

    # 3. Connectors
    pattern_conn = re.compile(r"(<!-- AUTO_CONNECTORS_START:\s*([A-Za-z0-9_]+)\s*-->)(.*?)(<!-- AUTO_CONNECTORS_END:\s*\2\s*-->)", re.DOTALL)
    def _replace_conn(match):
        nonlocal replacements
        tag_start = match.group(1)
        board_id = match.group(2).strip()
        tag_end = match.group(4)
        b = boards_data.get(board_id) or boards_data.get(board_id.replace(" ", "_"))
        if b and b.get("connectors"):
            table_md = render_connectors_tables(b, lang)
            replacements += 1
            return f"{tag_start}\n\n{table_md}\n\n{tag_end}"
        elif b:
            replacements += 1
            empty_msg = "*Keine externen Steckverbinder auf dieser Baugruppe.*" if lang == "de" else "*No external connectors on this assembly.*"
            return f"{tag_start}\n\n{empty_msg}\n\n{tag_end}"
        return match.group(0)
    content = pattern_conn.sub(_replace_conn, content)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[OK] Injected {replacements} table section(s) into {doc_path}")
    return replacements

def main():
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found!")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    boards = data.get("boards", {})
    sync_markdown_file(OUTPUT_DE, boards, lang="de")
    if os.path.exists(OUTPUT_EN):
        sync_markdown_file(OUTPUT_EN, boards, lang="en")

if __name__ == "__main__":
    main()
