// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Cartridge Sled (Pod 1 & 2)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_cardo.scad
// Description: Ready-to-print dual-tier cartridge sled for Cardo Packtalk Edge.
//              Houses the lower Adapter PCB (DS2401 ID) and upper Cardo AirMount
//              magnetic docking cradle with Pogo pin cutout.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;

module cartridge_cardo_sled() {
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

        // 3. Upper Cardo AirMount Neodymium Magnet Pocket Boss (Top Deck at z = 18.0 mm)
        translate([40.0, 27.0, 18.0])
            cylinder(r=8.0, h=4.0, center=false); // N52 Magnet boss

        // 4. Cardo Pogo-Pin Array Shroud Boss
        translate([5.0, 17.0, 18.0])
            cube(size=[10.0, 20.0, 5.0], center=false);
    }
}

// Render complete Cardo Cartridge
cartridge_cardo_sled();
