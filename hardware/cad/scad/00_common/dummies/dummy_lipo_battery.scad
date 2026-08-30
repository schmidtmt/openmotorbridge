// =============================================================================
// OpenMotorBridge - Dummy 3D Model: 1S LiPo Backup Battery (1000 mAh)
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_lipo_battery.scad
// Description: 3D model of the 1000 mAh LiPo pouch cell with protection circuit
//              and JST-PH 2.0 connector wires.
// =============================================================================

include <../parameters.scad>;

module dummy_lipo_battery() {
    // 1. Pouch Cell Body (Blue heatshrink sleeve, 50 x 35 x 6.0 mm)
    color("dodgerblue")
        cube(size=[50.0, 35.0, 6.0], center=false);

    // 2. Integrated PCM Protection Board (Top edge)
    color("dimgray")
        translate([0.0, 35.0, 1.0])
            cube(size=[50.0, 4.0, 4.0], center=false);

    // 3. Silicone Output Wires (Red + Black)
    color("red")
        translate([15.0, 39.0, 2.5])
            rotate([-90, 0, 0])
                cylinder(r=0.7, h=12.0);

    color("black")
        translate([20.0, 39.0, 2.5])
            rotate([-90, 0, 0])
                cylinder(r=0.7, h=12.0);

    // 4. JST-PH 2.0 2-Pin Plug
    color("white")
        translate([13.5, 51.0, 0.5])
            cube(size=[8.0, 6.0, 4.5], center=false);
}

// Preview standalone
dummy_lipo_battery();
