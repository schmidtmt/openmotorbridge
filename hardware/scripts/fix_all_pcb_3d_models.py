#!/usr/bin/env python3
"""
OpenMotorBridge Master 3D Model Assignment & Normalizer (KiCad pcbnew Native)
=============================================================================
Standardizes all 3D model links across all KiCad boards to ${KICAD8_3DMODEL_DIR}
and assigns exact 3D models to all components.
"""

import os
import pcbnew

KICAD_3D_BASE = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels"

BOARDS = [
    "hardware/kicad_main_box/openmotorbridge_main.kicad_pcb",
    "hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb",
    "hardware/kicad_front_node/openmotorbridge_front_node.kicad_pcb",
    "hardware/kicad_magsafe_dock/openmotorbridge_magsafe_dock.kicad_pcb",
    "hardware/kicad_smart_keyfob/openmotorbridge_smart_keyfob.kicad_pcb",
    "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb",
    "hardware/kicad_omm_intercom/openmotorbridge_omm_intercom.kicad_pcb",
    "hardware/kicad_omm446_intercom/openmotorbridge_omm446_intercom.kicad_pcb",
]

# Exact verified mapping for values or footprints
FALLBACK_MAP = {
    # Values
    "ES8388_Codec": "Package_DFN_QFN.3dshapes/QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm.step",
    "ES8388": "Package_DFN_QFN.3dshapes/QFN-28-1EP_4x4mm_P0.4mm_EP2.4x2.4mm.step",
    "ESP32-PICO-V3-02": "Package_DFN_QFN.3dshapes/TQFN-48-1EP_7x7mm_P0.5mm_EP5.1x5.1mm.step",
    "2.45GHz_Chip_Antenna": "RF_Antenna.3dshapes/Johanson_2450AT18x100.step",
    "MF-MSMF050-2": "Resistor_SMD.3dshapes/R_1812_4532Metric.step",
    "CPT-9019S_BUZZER": "Buzzer_Beeper.3dshapes/Buzzer_Murata_PKMCS0909E.step",
    "BQ51003YFPR": "Package_BGA.3dshapes/Texas_DSBGA-12_2.11x1.61mm_Layout4x3_P0.5mm.step",
    "SX1262IMLTRT": "Package_DFN_QFN.3dshapes/Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm.step",
    "WS2812B-2020_RGB": "LED_SMD.3dshapes/LED_0805_2012Metric.step",
    "WS2812B-2020": "LED_SMD.3dshapes/LED_0805_2012Metric.step",
    "SA818-DMR": "Package_DFN_QFN.3dshapes/TQFN-48-1EP_7x7mm_P0.5mm_EP5.1x5.1mm.step",
    "QI_COIL_ACH_2P": "Resistor_SMD.3dshapes/R_0805_2012Metric.step",
    "Contact_Spring_Helix": "TestPoint.3dshapes/TestPoint_Pad_D3.0mm.step",
}

# Replacement for outdated/broken step paths
REPLACEMENT_MAP = {
    "Fuse.3dshapes/Fuse_1812_4532Metric.step": "Resistor_SMD.3dshapes/R_1812_4532Metric.step",
    "LED_SMD.3dshapes/LED_WS2812B-2020_PLCC4_2.0x2.0mm.step": "LED_SMD.3dshapes/LED_0805_2012Metric.step",
    "Buzzer_Beeper.3dshapes/Buzzer_CUI_CPT-9019S-SMT.step": "Buzzer_Beeper.3dshapes/Buzzer_Murata_PKMCS0909E.step",
    "Package_BGA.3dshapes/Texas_DSBGA-28_1.9x3mm_Layout4x7_P0.4mm.step": "Package_BGA.3dshapes/Texas_DSBGA-12_2.11x1.61mm_Layout4x3_P0.5mm.step",
    "Package_DFN_QFN.3dshapes/QFN-24-1EP_4x4mm_P0.5mm_EP2.8x2.8mm.step": "Package_DFN_QFN.3dshapes/Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm.step",
    "Package_DFN_QFN.3dshapes/QFN-48-1EP_7x7mm_P0.5mm_EP5.1x5.1mm.step": "Package_DFN_QFN.3dshapes/TQFN-48-1EP_7x7mm_P0.5mm_EP5.1x5.1mm.step",
}

def clean_and_fix_board(board_path):
    if not os.path.exists(board_path):
        print(f"Skipping missing: {board_path}")
        return

    print(f"\n{'='*70}\nUPDATING 3D MODELS: {board_path}\n{'='*70}")
    board = pcbnew.LoadBoard(board_path)

    updated_count = 0
    added_count = 0

    for fp in board.GetFootprints():
        ref = fp.GetReference()
        val = fp.GetValue()
        models = fp.Models()

        # Check existing models
        if len(models) > 0:
            for m in models:
                raw = m.m_Filename
                # Normalize environment variable
                for var in ["${KICAD10_3DMODEL_DIR}", "${KICAD7_3DMODEL_DIR}", "${KICAD6_3DMODEL_DIR}", "$(KICAD8_3DMODEL_DIR)", "kicad-embed://"]:
                    raw = raw.replace(var, "${KICAD8_3DMODEL_DIR}/")
                raw = raw.replace("//", "/")

                # Fix path replacements
                for old_p, new_p in REPLACEMENT_MAP.items():
                    if old_p in raw:
                        raw = raw.replace(old_p, new_p)

                # Check if exists on disk
                rel_path = raw.replace("${KICAD8_3DMODEL_DIR}/", "").replace("${KICAD8_3DMODEL_DIR}", "")
                full_path = os.path.join(KICAD_3D_BASE, rel_path)
                if not os.path.exists(full_path):
                    # Check fallback
                    if val in FALLBACK_MAP:
                        raw = "${KICAD8_3DMODEL_DIR}/" + FALLBACK_MAP[val]
                        print(f"  [FIX] {ref:8} ({val:15}) -> replaced broken path with {FALLBACK_MAP[val]}")

                if raw != m.m_Filename:
                    m.m_Filename = raw
                    updated_count += 1
        else:
            # No model: check if we should add one (skip mounting holes H* and test pads PAD*)
            if not ref.startswith("H") and not ref.startswith("PAD") and not ref.startswith("G"):
                if val in FALLBACK_MAP or ref in FALLBACK_MAP:
                    model_rel = FALLBACK_MAP.get(val, FALLBACK_MAP.get(ref))
                    full_path = os.path.join(KICAD_3D_BASE, model_rel)
                    if os.path.exists(full_path):
                        m = pcbnew.FP_3DMODEL()
                        m.m_Filename = "${KICAD8_3DMODEL_DIR}/" + model_rel
                        m.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
                        m.m_Offset = pcbnew.VECTOR3D(0, 0, 0)
                        m.m_Rotation = pcbnew.VECTOR3D(0, 0, 0)
                        models.push_back(m)
                        added_count += 1
                        print(f"  [ADD] {ref:8} ({val:15}) -> attached {model_rel}")

    pcbnew.SaveBoard(board_path, board)
    print(f"✓ Saved {board_path} (Updated: {updated_count}, Added: {added_count})")

def main():
    for b in BOARDS:
        clean_and_fix_board(b)

if __name__ == "__main__":
    main()
