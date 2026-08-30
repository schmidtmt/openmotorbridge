// =============================================================================
// OpenMotorBridge - Satellite Pod: Waterproof Blindkassette (Dry Box Dummy)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_blindkassette.scad
// Description: Ready-to-print waterproof IP67 dummy cartridge with reinforced
//              sealed lid for weather protection when no headset is installed.
// =============================================================================

include <../00_common/parameters.scad>;
include <00_base_sled.scad>;

module cartridge_blindkassette_waterproof() {
    union() {
        // 1. Universal Base Sled
        cartridge_base_sled(
            sled_l = CARTRIDGE_BASE_L,
            sled_w = CARTRIDGE_BASE_W,
            sled_h = 18.0,
            wall   = 2.5
        );

        // 2. Solid Sealed Enclosure Box (65.0 x 44.0 x 18.0 mm)
        translate([5.0, 5.0, 2.5])
            cube(size=[65.0, 44.0, 18.0], center=false);

        // 3. 4x Transverse Reinforcing Structural Ribs
        for (x_rib = [18.0, 30.0, 42.0, 54.0]) {
            translate([x_rib, 5.0, 20.5])
                cube(size=[2.5, 44.0, 2.0], center=false);
        }
    }
}

// Render complete Blindkassette
cartridge_blindkassette_waterproof();
