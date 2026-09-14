// =============================================================================
// OpenMotorBridge - Dummy 3D Model: 1S LiPo Backup Battery (2200 mAh Flat Cell)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_lipo_battery.scad
// Description: 3D model of the 2200 mAh ultra-flat LiPo pouch cell (504068 / 503870)
//              with integrated PCM protection board and Molex Micro-Fit 3.0 wires.
// =============================================================================

include <../parameters.scad>;

module dummy_lipo_battery() {
    // 1. Pouch Cell Body (Ultra-flat silver/blue sleeve, 67 x 38 x 5.0 mm)
    color("dodgerblue")
        cube(size=[67.0, 38.0, 5.0], center=false);

    // 2. Integrated PCM Protection Board (Edge strip)
    color("dimgray")
        translate([0.0, 38.0, 0.5])
            cube(size=[67.0, 3.0, 4.0], center=false);

    // 3. Silicone Output Wires (Red + Black + NTC Yellow)
    color("red")
        translate([25.0, 41.0, 2.5])
            rotate([-90, 0, 0])
                cylinder(r=0.7, h=10.0, $fn=16);

    color("black")
        translate([30.0, 41.0, 2.5])
            rotate([-90, 0, 0])
                cylinder(r=0.7, h=10.0, $fn=16);

    // 4. Molex Micro-Fit 3.0 2-Pin Plug
    color("white")
        translate([23.5, 51.0, 0.5])
            cube(size=[9.6, 7.0, 5.0], center=false);
}

// Preview standalone
dummy_lipo_battery();
