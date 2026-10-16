// =============================================================================
// OpenMotorBridge - Satellite Pod: Cartridge Assembly & Comparison Gallery
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/99_cartridge_assembly.scad
// Description: Multi-cartridge 3D inspection gallery comparing all 4 variants side-by-side:
//              1. OMM 2.4 GHz UCS Transceiver Cartridge (with PCBA 03 & COTS RF Booster)
//              2. Sena SPIDER X Slim Cartridge (with original OEM Quick-Snap Cradle)
//              3. Cardo Packtalk Edge Cartridge (with original OEM Air-Mount Cradle & 2 Actuators)
//              4. Waterproof IP67 Blindkassette (Dry Box Dummy Cartridge)
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <cartridge_omm_transceiver.scad>;
use <cartridge_sena.scad>;
use <cartridge_cardo.scad>;
use <cartridge_blindkassette.scad>;

// Render all 4 cartridge variants parallel side-by-side for 100% unobstructed visual inspection
module cartridge_gallery_preview() {
    spacing_y = 80.0;

    // 1. OMM 2.4 GHz UCS Transceiver Cartridge with 5V RF Booster (Y = 0 mm)
    translate([0, 0 * spacing_y, 0]) {
        cartridge_omm_transceiver_assembly(exploded = false);
    }

    // 2. Sena SPIDER X Slim in Original OEM Quick-Snap Cradle (Y = 80 mm)
    translate([0, 1 * spacing_y, 0]) {
        cartridge_sena_assembly(exploded = false);
    }

    // 3. Cardo Packtalk Edge in Original OEM Air-Mount Cradle + 2 Actuators (Y = 160 mm)
    translate([0, 2 * spacing_y, 0]) {
        cartridge_cardo_assembly(exploded = false);
    }

    // 4. Waterproof Blindkassette / Leerkassette (Y = 240 mm, with floor insert tray am Boden)
    translate([0, 3 * spacing_y, 0]) {
        cartridge_blindkassette_assembly(exploded = false);
    }
}

// Render complete cartridge gallery
cartridge_gallery_preview();
