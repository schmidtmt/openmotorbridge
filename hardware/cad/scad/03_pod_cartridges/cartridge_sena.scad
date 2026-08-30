// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena 50S/60S Cartridge Sled (Pod 1 & Pod 2)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_sena.scad
// Description: Ready-to-print dual-tier cartridge sled for Sena 50S & 60S headsets.
//              Houses the lower Adapter PCB (DS2401 ID) and upper Sena 3D cradle.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;

module cartridge_sena_sled() {
    union() {
        // 1. Universal Base Sled
        cartridge_base_sled(
            sled_l = CARTRIDGE_BASE_L,
            sled_w = CARTRIDGE_BASE_W,
            sled_h = 18.0,
            wall   = 2.5
        );

        // 2. 4x M2 Mounting Standoffs for Lower Adapter PCB (50 x 22 mm)
        translate([15.0, 10.0, 2.5])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
        translate([60.0, 10.0, 2.5])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
        translate([15.0, 44.0, 2.5])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);
        translate([60.0, 44.0, 2.5])
            screw_boss(outer_r=2.0, inner_r=M2_SCREW_HOLE_R, h=2.5);

        // 3. Upper Sena 3D Cradle & Jog-Dial Nest Bosses (Top Deck at z = 18.0 mm)
        translate([55.0, 18.0, 18.0])
            cylinder(r=6.0, h=6.0, center=false); // Main jog-dial lock cylinder

        translate([55.0, 36.0, 18.0])
            cylinder(r=5.0, h=6.0, center=false); // Antenna pivot nest
    }
}

// Render complete Sena Cartridge
cartridge_sena_sled();
