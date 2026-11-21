#!/usr/bin/env python3
"""
OpenMotorBridge System Communication Matrix Documentation Generator
Generates docs/de/12_system_communication_matrix.md & docs/en/12_system_communication_matrix.md
from data/system_communication_matrix.json
"""

import json
import os
import sys

JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/system_communication_matrix.json")
OUTPUT_DE = os.path.join(os.path.dirname(__file__), "../docs/de/12_system_communication_matrix.md")
OUTPUT_EN = os.path.join(os.path.dirname(__file__), "../docs/en/12_system_communication_matrix.md")

def status_badge(status, lang="de"):
    if lang == "de":
        if status == "implemented":
            return "✅ Implementiert"
        elif status == "partial":
            return "⚠️ Teilweise / Entwurf"
        elif status == "missing":
            return "❌ **FEHLT (Offen)**"
        elif status == "external":
            return "🌐 Extern (OEM-Funk)"
    else:
        if status == "implemented":
            return "✅ Implemented"
        elif status == "partial":
            return "⚠️ Partial / Draft"
        elif status == "missing":
            return "❌ **MISSING (Open)**"
        elif status == "external":
            return "🌐 External (OEM RF)"
    return status

def generate_doc(data, lang="de"):
    meta = data.get("_meta", {})
    nodes = data.get("nodes", {})
    buses = data.get("buses", {})
    channels = data.get("channels", [])

    lines = []
    title = meta.get('title', 'System Communication Matrix')
    if lang == "en":
        title = "OpenMotorBridge System Communication Matrix (SSOT)"
    lines.append(f"# {title}")
    lines.append("")
    
    if lang == "de":
        lines.append(f"> **Dokumenten-ID:** `{meta.get('doc_id')}`  ")
        lines.append(f"> **Version:** `{meta.get('version')}` | **Datum:** `{meta.get('last_updated')}`  ")
        lines.append(f"> **Status:** `{meta.get('status')}`  ")
        lines.append(f"> **SSOT-Quelldatei:** [`data/system_communication_matrix.json`](../../data/system_communication_matrix.json)  ")
        lines.append("")
        lines.append(f"{meta.get('description', '')}")
    else:
        lines.append(f"> **Document ID:** `{meta.get('doc_id')}`  ")
        lines.append(f"> **Version:** `{meta.get('version')}` | **Date:** `{meta.get('last_updated')}`  ")
        lines.append(f"> **Status:** Architectural Ground Truth  ")
        lines.append(f"> **SSOT Source File:** [`data/system_communication_matrix.json`](../../data/system_communication_matrix.json)  ")
        lines.append("")
        lines.append("Comprehensive definition of all logical and physical communication relationships across all nodes, controllers, peripheral devices, OEM adapters, helmets, and the rider smartphone within the OpenMotorBridge system.")
    
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Nodes
    if lang == "de":
        lines.append("## 1. System-Knoten, Controller & Endgeräte (Nodes)")
        lines.append("")
        lines.append("| Node-Key | Platinen-ID / Typ | Bezeichnung | Controller / Hardware | Primäre System-Rolle |")
    else:
        lines.append("## 1. System Nodes, Controllers & End Devices (Nodes)")
        lines.append("")
        lines.append("| Node Key | Board ID / Type | Designation | Controller / Hardware | Primary System Role |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for key, n in nodes.items():
        lines.append(f"| `{key}` | **{n.get('id')}** | {n.get('name')} | `{n.get('controller')}` | {n.get('role')} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 2. Buses
    if lang == "de":
        lines.append("## 2. Physische Bus-Topologie & Übertragungsmedien (Buses)")
        lines.append("")
        lines.append("| Bus-Identifier | Beschreibung, physischer Pfad & Isolation |")
    else:
        lines.append("## 2. Physical Bus Topology & Transmission Media (Buses)")
        lines.append("")
        lines.append("| Bus Identifier | Description, Physical Routing & Isolation |")
    lines.append("| :--- | :--- |")
    for b_key, b_desc in buses.items():
        lines.append(f"| `{b_key}` | {b_desc} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group channels into categories
    if lang == "de":
        sections = [
            ("3. Schiene 1: Frontnode <-> Zentralbox (USB-Backbone Strang 1)", ["BUS_USB_BACKBONE_CH1"]),
            ("4. Frontnode Inter-Chip Brücke (Chip 1 <-> Chip 2 auf PCBA 05)", ["BUS_FRONT_INTER_CHIP", "BUS_FRONT_I2S"]),
            ("5. Schiene 2: Frontnode <-> Infotainment (SkylineOS & Nachrüst-AA)", ["BUS_FRONT_INFOTAINMENT_MUX", "BUS_POWER_NAVI_J10"]),
            ("6. Pod-Cartridges <-> Zentralbox (USB-Backbone Strang 2 & 3)", ["BUS_USB_BACKBONE_CH2", "BUS_USB_BACKBONE_CH3"]),
            ("7. Pod-Cartridge <-> OEM-Adapter & OMM-Module (Stecker J4)", ["BUS_POD_J4_HYBRID_L", "BUS_POD_J4_HYBRID_R"]),
            ("8. Koffer-Gateways (Bay 1 & Bay 2) <-> Externe Gruppen-Teilnehmer (Drahtloses Mesh & Funk)", ["BUS_RF_INTERCOM_L", "BUS_RF_INTERCOM_R"]),
            ("9. Zentralbox <-> Heck-Radar 2.0 & V2X (USB-Backbone Strang 4)", ["BUS_USB_BACKBONE_CH4"]),
            ("10. Zentralbox <-> Smartphone & Helm-Headsets (Bluetooth 5.4 Dual-A2DP, LE Audio & HFP)", ["BUS_BLUETOOTH_CENTRAL"]),
            ("11. Smartphone <-> Frontnode Dongle (Wireless CarPlay / Android Auto)", ["BUS_WIFI_BT_DONGLE"]),
            ("12. Zentralbox <-> Motorrad CAN-Bus (Einziger CAN-Knoten im Bike)", ["BUS_VEHICLE_CAN"]),
            ("13. Zentralbox / Frontnode <-> Action-Cam & Dashcam (BLE & Synchronisation)", ["BUS_BLE_ACTIONCAM"]),
            ("14. Zentralbox (U13 A2DP) <-> OEM-Adapter (Drahtloses Mesh-Music-Sharing)", ["BUS_A2DP_POD_MESH"]),
        ]
    else:
        sections = [
            ("3. Rail 1: Front Node <-> Central Box (USB Backbone Leg 1)", ["BUS_USB_BACKBONE_CH1"]),
            ("4. Front Node Inter-Chip Bridge (Chip 1 <-> Chip 2 on PCBA 05)", ["BUS_FRONT_INTER_CHIP", "BUS_FRONT_I2S"]),
            ("5. Rail 2: Front Node <-> Infotainment (SkylineOS & Aftermarket AA)", ["BUS_FRONT_INFOTAINMENT_MUX", "BUS_POWER_NAVI_J10"]),
            ("6. Pod Cartridges <-> Central Box (USB Backbone Legs 2 & 3)", ["BUS_USB_BACKBONE_CH2", "BUS_USB_BACKBONE_CH3"]),
            ("7. Pod Cartridge <-> OEM Adapter & OMM Modules (Connector J4)", ["BUS_POD_J4_HYBRID_L", "BUS_POD_J4_HYBRID_R"]),
            ("8. Luggage Gateways (Bay 1 & Bay 2) <-> External Group Participants (Wireless Mesh & Radio)", ["BUS_RF_INTERCOM_L", "BUS_RF_INTERCOM_R"]),
            ("9. Central Box <-> Rear Radar 2.0 & V2X (USB Backbone Leg 4)", ["BUS_USB_BACKBONE_CH4"]),
            ("10. Central Box <-> Smartphone & Helmet Headsets (Bluetooth 5.4 Dual-A2DP, LE Audio & HFP)", ["BUS_BLUETOOTH_CENTRAL"]),
            ("11. Smartphone <-> Front Node Dongle (Wireless CarPlay / Android Auto)", ["BUS_WIFI_BT_DONGLE"]),
            ("12. Central Box <-> Motorcycle CAN Bus (Sole CAN Node on Motorcycle)", ["BUS_VEHICLE_CAN"]),
            ("13. Central Box / Front Node <-> Action Cam & Dashcam (BLE & Sync)", ["BUS_BLE_ACTIONCAM"]),
            ("14. Central Box (U13 A2DP) <-> OEM Adapter (Wireless Mesh Music Sharing)", ["BUS_A2DP_POD_MESH"]),
        ]

    for title, bus_filters in sections:
        lines.append(f"## {title}")
        lines.append("")
        if lang == "de":
            lines.append("| ID | Von $\\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |")
        else:
            lines.append("| ID | From $\\rightarrow$ To | Bus & Protocol | Packet / Type | Rate | Payload Data | Purpose & Function | Firmware Status |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |")

        matching = [c for c in channels if c.get("bus") in bus_filters]
        for c in matching:
            c_id = c.get("id")
            src = c.get("source").replace("NODE_", "")
            tgt = c.get("target").replace("NODE_", "")
            bus_proto = f"`{c.get('bus')}`<br>*{c.get('protocol')}*"
            pkt = f"`{c.get('pkt_type')}`"
            rate = c.get("rate")
            payload = "<br>".join([f"• {p}" for p in c.get("payload", [])])
            purpose = c.get("purpose")
            status = status_badge(c.get("fw_status"), lang=lang)

            lines.append(f"| **{c_id}** | `{src}` $\\rightarrow$<br>`{tgt}` | {bus_proto} | {pkt} | {rate} | {payload} | {purpose} | {status} |")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Summary of gaps
    missing_channels = [c for c in channels if c.get("fw_status") in ["missing", "partial"]]
    if lang == "de":
        lines.append("## 15. Konsolidierte Firmware-Lücken-Matrix & Entwicklungs-Roadmap")
        lines.append("")
        lines.append(f"Insgesamt wurden **{len(channels)} Kommunikationsbeziehungen** erfasst.")
        lines.append(f"Davon sind **{len(missing_channels)} Kanäle** noch offen oder nur teilweise implementiert:")
        lines.append("")
        lines.append("| Kanal-ID | Betroffene Knoten | Bus | Fehlende Funktionalität / Aufgabenstellung | Dringlichkeit |")
    else:
        lines.append("## 15. Consolidated Firmware Gap Matrix & Development Roadmap")
        lines.append("")
        lines.append(f"A total of **{len(channels)} communication channels** are documented.")
        lines.append(f"Of these, **{len(missing_channels)} channels** are currently open or partially implemented:")
        lines.append("")
        lines.append("| Channel ID | Affected Nodes | Bus | Pending Functionality / Task Description | Urgency |")
    lines.append("| :--- | :--- | :--- | :--- | :---: |")
    
    for mc in missing_channels:
        cid = mc.get("id")
        src = mc.get("source").replace("NODE_", "")
        tgt = mc.get("target").replace("NODE_", "")
        bus = mc.get("bus")
        desc = mc.get("purpose")
        if lang == "de":
            prio = "🔴 Hoch (Core)" if any(k in cid for k in ["AUDIO", "INTERCHIP", "WHIM", "SD"]) else "🟡 Mittel"
        else:
            prio = "🔴 High (Core)" if any(k in cid for k in ["AUDIO", "INTERCHIP", "WHIM", "SD"]) else "🟡 Medium"
        lines.append(f"| **{cid}** | `{src}` $\\rightarrow$ `{tgt}` | `{bus}` | {desc} | {prio} |")

    lines.append("")
    lines.append("---")
    if lang == "de":
        lines.append("*Automatisch generiert durch `tools/generate_comm_docs.py` aus `data/system_communication_matrix.json`.*")
    else:
        lines.append("*Automatically generated by `tools/generate_comm_docs.py` from `data/system_communication_matrix.json`.*")

    return "\n".join(lines) + "\n"

def main():
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found!")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Generate German Doc
    doc_de = generate_doc(data, lang="de")
    os.makedirs(os.path.dirname(OUTPUT_DE), exist_ok=True)
    with open(OUTPUT_DE, "w", encoding="utf-8") as f:
        f.write(doc_de)
    print(f"✅ Generated {OUTPUT_DE} successfully ({len(data.get('channels', []))} channels documented)!")

    # Generate English Doc
    doc_en = generate_doc(data, lang="en")
    os.makedirs(os.path.dirname(OUTPUT_EN), exist_ok=True)
    with open(OUTPUT_EN, "w", encoding="utf-8") as f:
        f.write(doc_en)
    print(f"✅ Generated {OUTPUT_EN} successfully ({len(data.get('channels', []))} channels documented)!")

if __name__ == "__main__":
    main()
