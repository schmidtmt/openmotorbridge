// =============================================================================
// OpenMotorBridge - Satellite Pod: Cartridge Assembly & Comparison Matrix
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/99_cartridge_assembly.scad
// Description: Multi-cartridge 3D inspection scene comparing the 4 variants:
//              1. OMM Rear Transceiver Cartridge (with inserted PCB & Patch Antenna)
//              2. Sena 50S/60S Cartridge (with inserted Adapter PCB)
//              3. Cardo Packtalk Edge Cartridge (with inserted Adapter PCB)
//              4. Waterproof Blindkassette (Dry Box Dummy)
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/dummies/dummy_omm_transceiver_pcb.scad>;
include <../00_common/dummies/dummy_adapter_pcb.scad>;
include <cartridge_omm_transceiver.scad>;
include <cartridge_sena.scad>;
include <cartridge_cardo.scad>;
include <cartridge_blindkassette.scad>;

// Render all 4 cartridge variants side by side for visual design check
module cartridge_gallery_preview() {
    // 1. OMM Transceiver Cartridge (Pod 3 Heck, Front Left)
    translate([0, 0, 0]) {
        color("darkslategray", 0.8)
            cartridge_omm_transceiver_sled();
        // Inserted PCB Dummy
        translate([2.5, 3.0, 5.5])
            dummy_omm_transceiver_pcb();
    }

    // 2. Sena 50S/60S Cartridge (Front Right)
    translate([0, 80.0, 0]) {
        color("slategray", 0.85)
            cartridge_sena_sled();
        // Inserted Adapter PCB Dummy
        translate([12.0, 16.0, 5.0])
            dummy_adapter_pcb();
    }

    // 3. Cardo Packtalk Edge Cartridge (Rear Left)
    translate([100.0, 0, 0]) {
        color("dimgray", 0.85)
            cartridge_cardo_sled();
        // Inserted Adapter PCB Dummy
        translate([12.0, 16.0, 5.0])
            dummy_adapter_pcb();
    }

    // 4. Waterproof Blindkassette (Rear Right)
    translate([100.0, 80.0, 0]) {
        color("black", 0.9)
            cartridge_blindkassette_waterproof();
    }
}

// Render complete cartridge gallery
cartridge_gallery_preview();
