// =============================================================================
// OpenMotorBridge - Dummy 3D Model: M8 6-Pin IP67 Metal Connector & Cable
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_m8_connector.scad
// Description: Realistic 3D model of the M8 circular waterproof connector
//              with knurled nut and flexible PUR cable.
// =============================================================================

include <../parameters.scad>;

module dummy_m8_connector() {
    // 1. Threaded Metal Body / Bulkhead (Brass nickel-plated, Ø 8.0 mm)
    color("silver")
        rotate([0, 90, 0])
            cylinder(r=4.0, h=15.0);

    // 2. Knurled Coupling Nut (Ø 10.0 mm x 8.0 mm)
    color("dimgray")
        translate([-4.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=5.0, h=8.0);

    // 3. Molded PUR Cable Boot (Black strain relief)
    color("black")
        translate([-16.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r1=3.0, r2=4.5, h=12.0);

    // 4. Heavy-Duty PUR Cable Jacket (Ø 5.5 mm x 30.0 mm)
    color("black")
        translate([-46.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=2.75, h=30.0);

    // 5. 6-Pin Gold Insert (Front view)
    color("gold") {
        for (a = [0:60:300]) {
            translate([15.0, 2.0 * cos(a), 2.0 * sin(a)])
                rotate([0, 90, 0])
                    cylinder(r=0.4, h=2.0);
        }
    }
}

// Preview standalone
dummy_m8_connector();
