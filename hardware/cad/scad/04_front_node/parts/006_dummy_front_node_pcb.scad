// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal Front Node PCB
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/006_dummy_front_node_pcb.scad
// Description: Accurate 3D dummy of openmotorbridge_front_node PCB for
//              collision verification, enclosure fitting, and rendering.
// =============================================================================

include <../../00_common/parameters.scad>;

module dummy_front_node_pcb() {
    // 1. PCB Substrate (FR4 4-Layer Green, 68 x 44 x 1.6 mm)
    color("forestgreen") {
        difference() {
            // Rounded rectangle substrate
            linear_extrude(height = FRONT_NODE_PCB_H) {
                offset(r = FRONT_NODE_PCB_R) {
                    offset(delta = -FRONT_NODE_PCB_R) {
                        square([FRONT_NODE_PCB_L, FRONT_NODE_PCB_W], center=false);
                    }
                }
            }
            
            // 4x M2.5 Mounting Holes (H1-H4)
            translate([3.5, 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2);
            translate([64.5, 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2);
            translate([3.5, 40.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2);
            translate([64.5, 40.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2);
            
            // Knowles MEMS Acoustic hole (Ø 0.5 mm)
            translate([22.5, 15.46, -0.1]) cylinder(r=0.25, h=FRONT_NODE_PCB_H + 0.2);
        }
    }

    // 2. South Connectors (J6: CarPlay, J5: Glovebox, J4: USB Host) - 4-Pin JST-PH
    color("ghostwhite") {
        translate([15.75 - 5.0, 0.5, FRONT_NODE_PCB_H])
            cube(size=[10.0, 4.5, 7.5], center=false); // J6
        translate([29.50 - 5.0, 0.5, FRONT_NODE_PCB_H])
            cube(size=[10.0, 4.5, 7.5], center=false); // J5
        translate([43.25 - 5.0, 0.5, FRONT_NODE_PCB_H])
            cube(size=[10.0, 4.5, 7.5], center=false); // J4
    }

    // 3. South USB-C Service Port (J7)
    color("silver") {
        translate([53.82 - 4.5, -1.0, FRONT_NODE_PCB_H])
            cube(size=[9.0, 7.5, 3.2], center=false);
    }

    // 4. West Connectors (J1: 12V ACC, J2: CAN, J3: PTT)
    color("ghostwhite") {
        translate([0.5, 14.0 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[4.5, 6.0, 7.5], center=false); // J1 (2-pin)
        translate([0.5, 26.25 - 4.0, FRONT_NODE_PCB_H])
            cube(size=[4.5, 8.0, 7.5], center=false); // J2 (3-pin)
        translate([0.5, 34.25 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[4.5, 6.0, 7.5], center=false); // J3 (2-pin)
    }

    // 5. ESP32-C3-WROOM-02U Module with U.FL
    color("silver") {
        translate([49.5 - 9.0, 15.25 - 6.6, FRONT_NODE_PCB_H])
            cube(size=[18.0, 13.2, 3.2], center=false);
    }
    color("gold") {
        translate([49.5 + 6.0, 15.25 + 4.5, FRONT_NODE_PCB_H + 3.2])
            cylinder(r=1.0, h=1.0, $fn=16); // U.FL connector
    }

    // 6. Microchip USB2512B AEC-Q100 Hub IC (QFN-36)
    color("darkslategray") {
        translate([32.0 - 3.0, 29.8 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[6.0, 6.0, 0.9], center=false);
    }

    // 7. Knowles SPH0645 Digital I2S MEMS Microphone
    color("goldenrod") {
        translate([22.5 - 1.75, 15.46 - 1.32, FRONT_NODE_PCB_H])
            cube(size=[3.5, 2.65, 1.0], center=false);
    }

    // 8. Power Inductor L1 (4.7 uH Choke)
    color("dimgray") {
        translate([22.38 - 3.5, 6.75 - 3.5, FRONT_NODE_PCB_H])
            cube(size=[7.0, 7.0, 3.0], center=false);
    }

    // 9. SMD Pushbuttons SW1 (Reset) & SW2 (Boot)
    color("darkslategray") {
        translate([64.4 - 2.0, 23.5 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 2.5], center=false); // SW1
        translate([22.5 - 2.0, 22.0 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 2.5], center=false); // SW2
    }

    // 10. Status LED D1 (Green 0805)
    color("limegreen") {
        translate([66.25 - 1.0, 30.19 - 0.6, FRONT_NODE_PCB_H])
            cube(size=[2.0, 1.2, 0.8], center=false);
    }
}
