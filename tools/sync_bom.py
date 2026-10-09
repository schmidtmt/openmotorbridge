#!/usr/bin/env python3
"""
tools/sync_bom.py - OpenMotorBridge Single Source of Truth BOM Synchronizer

Synchronizes the central parts catalog (data/bom_parts.json) and component assembly
recipes (data/bom_assemblies.json) with:
1. webapp_pwa/js/bom_catalog.js (Browser-ready JS database & rollup engine)
2. docs/de/15_bom_manufacturing.md (Consolidated procurement tables & assembly breakdown)
3. docs/en/15_bom_manufacturing.md (Consolidated procurement tables & assembly breakdown)

Usage:
    python3 tools/sync_bom.py [--check]
"""

import json
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARTS_JSON_PATH = os.path.join(REPO_ROOT, "data", "bom_parts.json")
ASSEMBLIES_JSON_PATH = os.path.join(REPO_ROOT, "data", "bom_assemblies.json")
PWA_CATALOG_JS_PATH = os.path.join(REPO_ROOT, "webapp_pwa", "js", "bom_catalog.js")
DOCS_DE_PATH = os.path.join(REPO_ROOT, "docs", "de", "15_bom_manufacturing.md")
DOCS_EN_PATH = os.path.join(REPO_ROOT, "docs", "en", "15_bom_manufacturing.md")


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_integrity(parts_data, assemblies_data):
    parts = parts_data.get("parts", {})
    assemblies = assemblies_data.get("assemblies", {})
    missing_refs = []

    for asm_id, asm in assemblies.items():
        for item in asm.get("parts", []):
            part_id = item.get("part_id")
            if part_id not in parts:
                missing_refs.append(f"Assembly '{asm_id}' references unknown part '{part_id}'")

    if missing_refs:
        print("[ERROR] Integrity check failed:")
        for err in missing_refs:
            print(f"  - {err}")
        sys.exit(1)
    print(f"[OK] Integrity check passed: {len(parts)} parts, {len(assemblies)} assemblies verified.")


def rollup_assemblies(assemblies_data, parts_data, active_counts):
    """
    Rolls up total quantities of parts for given assembly counts.
    active_counts: dict of { assembly_id: count }
    """
    parts_catalog = parts_data.get("parts", {})
    assemblies_catalog = assemblies_data.get("assemblies", {})

    total_quantities = {}

    for asm_id, count in active_counts.items():
        if count <= 0 or asm_id not in assemblies_catalog:
            continue
        asm = assemblies_catalog[asm_id]
        for item in asm.get("parts", []):
            p_id = item["part_id"]
            qty = item["qty"]
            total_quantities[p_id] = total_quantities.get(p_id, 0.0) + (qty * count)

    return total_quantities


def format_qty(qty, unit):
    if unit == "m":
        return f"{qty:.1f} m" if qty != int(qty) else f"{int(qty)} m"
    if unit == "Set":
        return f"{int(qty)} Set" if qty == 1 else f"{int(qty)} Sets"
    if unit == "Paar":
        return f"{int(qty)} Paar"
    int_qty = int(qty)
    return f"{int_qty} Stk." if int_qty == qty else f"{qty:g} Stk."


def format_qty_en(qty, unit):
    if unit == "m":
        return f"{qty:.1f} m" if qty != int(qty) else f"{int(qty)} m"
    if unit == "Set":
        return f"{int(qty)} Set" if qty == 1 else f"{int(qty)} Sets"
    if unit == "Paar":
        return f"{int(qty)} Pair" if qty == 1 else f"{int(qty)} Pairs"
    int_qty = int(qty)
    return f"{int_qty} pcs" if int_qty == qty else f"{qty:g} pcs"


def generate_cots_markdown_table(parts_data, assemblies_data, lang="de"):
    is_de = lang == "de"
    # Reference complete motorcycle setup:
    # 1x Main Box, 1x Front Node, 2x Pod Base, 2x Cartridge Carrier,
    # 1x Inlay Sena, 1x Inlay Cardo, 1x OMM UCS 2.4G, 1x OMM 446M,
    # 1x Helmet Kit 2.4G, 1x Radar 2.0, 1x General Accessories
    ref_counts = {
        "assembly_main_box": 1,
        "assembly_front_node": 1,
        "assembly_pod_base": 2,
        "assembly_cartridge_carrier": 2,
        "assembly_inlay_sena_spider": 1,
        "assembly_inlay_cardo_edge": 1,
        "assembly_omm_ucs_module_24g": 1,
        "assembly_omm_ucs_module_446m": 1,
        "assembly_omm_helmet_kit_24g": 1,
        "assembly_radar2": 1,
        "assembly_general_accessories": 1
    }

    totals = rollup_assemblies(assemblies_data, parts_data, ref_counts)
    parts = parts_data.get("parts", {})

    # Exclude 3D printed parts and raw PCBs from COTS/Fastener procurement table
    # (they have their own sections)
    cots_types = {"fastener", "seal", "cots_electronic", "antenna", "cable"}

    rows = []
    # Deterministic sorting
    type_priority = {
        "fastener": 1,
        "seal": 2,
        "cots_electronic": 3,
        "antenna": 4,
        "cable": 5
    }

    sorted_part_ids = sorted(
        totals.keys(),
        key=lambda pid: (
            type_priority.get(parts[pid].get("type", ""), 99),
            parts[pid]["name"]["de"]
        )
    )

    for pid in sorted_part_ids:
        part = parts[pid]
        p_type = part.get("type", "")
        if p_type not in cots_types:
            continue

        name = part["name"]["de"] if is_de else part["name"]["en"]
        spec = part.get("spec", "")
        source = part.get("source", "")
        unit = part.get("unit", "Stk.")
        qty_str = format_qty(totals[pid], unit) if is_de else format_qty_en(totals[pid], unit)
        desc = part["desc"]["de"] if is_de else part["desc"]["en"]

        # Clean markdown formatting
        name_clean = f"**{name}**"
        rows.append(f"| {name_clean} | {spec} | {source} | {qty_str} | {desc} |")

    header = (
        "| Bauteil | Spezifikation / Typ | Bezugsquelle | Menge (Ref-Set) | Montageort & Funktion |\n"
        "| :--- | :--- | :--- | :---: | :--- |\n"
    ) if is_de else (
        "| Component | Specification / Type | Sourcing Source | Qty (Ref-Set) | Location & Purpose |\n"
        "| :--- | :--- | :--- | :---: | :--- |\n"
    )

    return header + "\n".join(rows) + "\n"


def generate_pwa_js_catalog(parts_data, assemblies_data):
    js_content = f"""// OpenMotorBridge Single Source of Truth (SSOT) BOM Database
// Auto-generated by tools/sync_bom.py - DO NOT EDIT DIRECTLY!
// To update, edit data/bom_parts.json or data/bom_assemblies.json and run 'python3 tools/sync_bom.py'.

const BOM_PARTS = {json.dumps(parts_data.get("parts", {}), indent=2, ensure_ascii=False)};

const BOM_ASSEMBLIES = {json.dumps(assemblies_data.get("assemblies", {}), indent=2, ensure_ascii=False)};

/**
 * Rolls up all parts for a given dictionary of active assembly quantities.
 * @param {{[assemblyId: string]: number}} activeCounts - Map of assembly IDs to quantity
 * @returns {{{{ [partId: string]: number }}}} - Aggregated part quantities
 */
function rollUpBomParts(activeCounts) {{
    const totals = {{}};
    for (const [asmId, count] of Object.entries(activeCounts)) {{
        if (!count || count <= 0 || !BOM_ASSEMBLIES[asmId]) continue;
        const asm = BOM_ASSEMBLIES[asmId];
        for (const item of (asm.parts || [])) {{
            totals[item.part_id] = (totals[item.part_id] || 0) + (item.qty * count);
        }}
    }}
    for (const [partId, val] of Object.entries(totals)) {{
        totals[partId] = Math.round(val * 1000) / 1000;
    }}
    return totals;
}}

/**
 * Categorizes rolled-up parts into clean arrays for PWA display.
 * @param {{{{ [partId: string]: number }}}} partQuantities
 * @param {{'de'|'en'}} lang
 */
function categorizeRolledUpBom(partQuantities, lang = 'de') {{
    const isDe = lang === 'de';
    const result = {{
        parts3D: [],
        pcbas: [],
        cots: [],
        fasteners: [],
        seals: [],
        cables: [],
        antennas: [],
        totalCostMin: 0,
        totalCostMax: 0
    }};

    for (const [partId, qty] of Object.entries(partQuantities)) {{
        if (!qty || qty <= 0 || !BOM_PARTS[partId]) continue;
        const part = BOM_PARTS[partId];
        const costMin = (part.cost_eur ? part.cost_eur[0] : 0) * qty;
        const costMax = (part.cost_eur ? part.cost_eur[1] : 0) * qty;
        result.totalCostMin += costMin;
        result.totalCostMax += costMax;

        const entry = {{
            id: partId,
            name: isDe ? part.name.de : part.name.en,
            spec: part.spec,
            source: part.source,
            qty: qty,
            unit: part.unit,
            desc: isDe ? part.desc.de : part.desc.en,
            costMin: costMin,
            costMax: costMax,
            type: part.type,
            pkgQty: part.pkg_qty || 1,
            pkgName: part.pkg_name || ''
        }};

        if (part.type === 'part_3d') {{
            result.parts3D.push({{
                group: part.group || '3D-Druck',
                file: part.file || part.spec.split(' ')[0],
                name: entry.name,
                qty: qty,
                desc: entry.desc,
                source: part.source
            }});
        }} else if (part.type === 'pcba') {{
            result.pcbas.push({{
                name: entry.name,
                id: part.id_kicad || entry.id,
                spec: entry.spec,
                qty: qty,
                desc: entry.desc
            }});
        }} else if (part.type === 'fastener') {{
            result.fasteners.push(entry);
            result.cots.push(entry);
        }} else if (part.type === 'seal') {{
            result.seals.push(entry);
            result.cots.push(entry);
        }} else if (part.type === 'cable') {{
            result.cables.push(entry);
            result.cots.push(entry);
        }} else if (part.type === 'antenna') {{
            result.antennas.push(entry);
            result.cots.push(entry);
        }} else {{
            result.cots.push(entry);
        }}
    }}

    return result;
}}

if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{ BOM_PARTS, BOM_ASSEMBLIES, rollUpBomParts, categorizeRolledUpBom }};
}}
"""
    return js_content


def update_markdown_file(filepath, new_table_md, lang="de"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- AUTOGEN_BOM_TABLE_START -->"
    end_marker = "<!-- AUTOGEN_BOM_TABLE_END -->"

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        re.DOTALL
    )

    wrapped_table = f"{start_marker}\n\n{new_table_md}\n{end_marker}"

    if pattern.search(content):
        updated_content = pattern.sub(wrapped_table, content)
    else:
        sec12_prefix = r"## 12\..*"
        sec13_prefix = r"## 13\..*"

        sec_pattern = re.compile(
            rf"(^|\n)({sec12_prefix}\n\n).*?(\n\n---\n\n{sec13_prefix})",
            re.DOTALL
        )
        if sec_pattern.search(content):
            updated_content = sec_pattern.sub(rf"\1\2{wrapped_table}\3", content)
        else:
            print(f"[WARN] Could not find insertion point in {filepath}")
            return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"[OK] Updated {filepath}")
    return True


def main():
    print("=== OpenMotorBridge BOM Synchronizer ===")
    parts_data = load_json(PARTS_JSON_PATH)
    assemblies_data = load_json(ASSEMBLIES_JSON_PATH)

    validate_integrity(parts_data, assemblies_data)

    # 1. Generate PWA Catalog JS
    pwa_js = generate_pwa_js_catalog(parts_data, assemblies_data)
    with open(PWA_CATALOG_JS_PATH, "w", encoding="utf-8") as f:
        f.write(pwa_js)
    print(f"[OK] Generated {PWA_CATALOG_JS_PATH} ({len(pwa_js.encode('utf-8'))} bytes)")

    # 2. Update German Docs
    de_table = generate_cots_markdown_table(parts_data, assemblies_data, lang="de")
    update_markdown_file(DOCS_DE_PATH, de_table, lang="de")

    # 3. Update English Docs
    en_table = generate_cots_markdown_table(parts_data, assemblies_data, lang="en")
    update_markdown_file(DOCS_EN_PATH, en_table, lang="en")

    print("[SUCCESS] All BOM catalogs & documents are fully synchronized!")


if __name__ == "__main__":
    main()
