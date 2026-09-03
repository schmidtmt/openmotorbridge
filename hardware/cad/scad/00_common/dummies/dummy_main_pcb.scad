// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Main Board PCB
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_main_pcb.scad
// Description: Realistic 3D representation of the central openMotorBridge
//              mainboard for clearance checks, enclosure fitting & rendering.
// =============================================================================

include <../parameters.scad>;

module dummy_main_pcb() {
    // 1. PCB Substrate (FR4 4-Layer Green, 95 x 65 x 1.6 mm)
    color("forestgreen") {
        difference() {
            cube(size=[95.0, 65.0, 1.6], center=false);
            // 4x M2.5 Mounting Holes (inward offset 4.0 mm)
            translate([4.0, 4.0, -0.1]) cylinder(r=1.35, h=2.0);
            translate([91.0, 4.0, -0.1]) cylinder(r=1.35, h=2.0);
            translate([4.0, 61.0, -0.1]) cylinder(r=1.35, h=2.0);
            translate([91.0, 61.0, -0.1]) cylinder(r=1.35, h=2.0);
        }
    }

    // 2. High-Density 26-Pin Automotive D-Sub Connector (HD26 at Front Edge)
    color("royalblue")
        translate([2.5, -4.0, 1.6])
            cube(size=[39.0, 12.5, 9.0], center=false);

    // 3. USB-C Programming & Diagnostic Port
    color("silver")
        translate([50.0, -2.5, 1.6])
            cube(size=[9.0, 7.5, 3.2], center=false);

    // 4. Status LEDs (3x 0805 RGB/Status Windows)
    color("red")   translate([70.0, 2.0, 1.6]) cube(size=[2.0, 1.25, 0.8]);
    color("green") translate([74.0, 2.0, 1.6]) cube(size=[2.0, 1.25, 0.8]);
    color("blue")  translate([78.0, 2.0, 1.6]) cube(size=[2.0, 1.25, 0.8]);

    // 5. LM5164 100V DCDC Buck Inductor & Power Stage
    color("darkslategray")
        translate([30.0, 20.0, 1.6])
            cube(size=[10.0, 10.0, 4.5], center=false);

    // 6. ESP32-S3-WROOM-1U Wireless MCU Module (18.0 x 19.2 mm with U.FL connector)
    color("silver")
        translate([20.0, 42.0, 1.6])
            cube(size=[18.0, 19.2, 3.2], center=false);
    color("gold")
        translate([20.0 + 14.5, 42.0 + 16.0, 1.6 + 3.2])
            cylinder(r=1.2, h=1.0, $fn=16);

    // 7. BQ25798 LiPo Solar/Vehicle Charger IC & Choke
    color("dimgray")
        translate([42.0, 22.0, 1.6])
            cube(size=[7.0, 7.0, 3.0], center=false);

    // 8. 4x Copper Thermal Stud Contact Pads (under the PCB floor)
    color("darkorange") {
        translate([35.0, 25.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
        translate([45.0, 25.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
        translate([30.0, 48.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
        translate([70.0, 40.0, -2.5]) cylinder(r=COPPER_STUD_R, h=2.5);
    }
}

// Preview standalone
dummy_main_pcb();
