// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal Front Node PCB (PCBA 05)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/006_dummy_front_node_pcb.scad
// Description: Accurate 3D dummy of openmotorbridge_front_node PCB (82 x 50 mm)
//              for collision verification, enclosure fitting, and rendering.
// =============================================================================

include <../../00_common/parameters.scad>;

module dummy_front_node_pcb() {
    // 1. PCB Substrate (FR4 4-Layer Green, 82 x 50 x 1.6 mm)
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
            translate([3.5, 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
            translate([FRONT_NODE_PCB_L - 3.5, 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
            translate([3.5, FRONT_NODE_PCB_W - 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
            translate([FRONT_NODE_PCB_L - 3.5, FRONT_NODE_PCB_W - 3.5, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
            
            // Knowles MEMS Acoustic hole (Ø 0.5 mm)
            translate([45.0, 40.0, -0.1]) cylinder(r=0.25, h=FRONT_NODE_PCB_H + 0.2, $fn=12);
        }
    }

    // 2. South Connectors (6x JST-PH along front rim Y = 0)
    // J4 (Host), J5 (Phone PD), J6 (CP2AA), J5_MP3 (Glovebox), J6_AUX (Cockpit), J8 (Action-Cam)
    color("ghostwhite") {
        translate([12.5 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J4
        translate([24.5 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J5
        translate([36.5 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J6
        translate([48.5 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J5_MP3
        translate([60.5 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J6_AUX
        translate([70.5 - 3.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[6.0, 4.5, 7.5], center=false);  // J8 (2-Pin)
    }

    // 3. West Connectors (6x JST-PH along vehicle rim X = 0)
    // J9 (BSD, 3P), J3 (PTT, 4P), J2 (CAN, 3P), J11 (Aux, 2P), J10 (Qi, 2P), J1 (12V, 2P)
    color("ghostwhite") {
        translate([0.5, 5.5 - 4.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 8.0, 7.5], center=false);  // J9
        translate([0.5, 13.0 - 5.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 10.0, 7.5], center=false); // J3
        translate([0.5, 20.5 - 4.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 8.0, 7.5], center=false);  // J2
        translate([0.5, 27.5 - 3.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 6.0, 7.5], center=false);  // J11
        translate([0.5, 34.5 - 3.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 6.0, 7.5], center=false);  // J10
        translate([0.5, 41.5 - 3.0, FRONT_NODE_PCB_H]) cube(size=[4.5, 6.0, 7.5], center=false);  // J1
    }

    // 4. East Connectors & Service Port (X = 82.0 mm)
    // J7 USB-C Service Port (facing East)
    color("silver") {
        translate([FRONT_NODE_PCB_L - 7.5, 15.1 - 4.5, FRONT_NODE_PCB_H])
            cube(size=[8.0, 9.0, 3.2], center=false);
    }
    // J12 Qwiic I2C (1.0mm JST-SH)
    color("ghostwhite") {
        translate([FRONT_NODE_PCB_L - 6.0, 35.0 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[5.0, 5.0, 3.0], center=false);
    }

    // 5. ESP32-S3-WROOM-1U Module with U.FL
    color("silver") {
        translate([52.0 - 9.0, 36.0 - 12.7, FRONT_NODE_PCB_H])
            cube(size=[18.0, 25.5, 3.2], center=false);
    }
    color("gold") {
        translate([52.0, 46.0, FRONT_NODE_PCB_H + 3.2])
            cylinder(r=1.0, h=1.0, $fn=16); // U.FL connector
    }

    // 6. Microchip USB2514B 4-Port Hub (QFN-36)
    color("darkslategray") {
        translate([42.0 - 3.0, 18.0 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[6.0, 6.0, 0.9], center=false);
    }

    // 7. Southchip SC8102 USB-PD Buck (QFN-32)
    color("darkslategray") {
        translate([21.0 - 2.5, 30.0 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[5.0, 5.0, 0.9], center=false);
    }

    // 8. Power Inductor L1 (4.7 uH Main Choke) & L2 (10 uH PD Choke)
    color("dimgray") {
        translate([24.0 - 3.5, 41.0 - 3.5, FRONT_NODE_PCB_H]) cube(size=[7.0, 7.0, 3.0], center=false); // L1
        translate([21.0 - 3.6, 22.0 - 3.6, FRONT_NODE_PCB_H]) cube(size=[7.3, 7.3, 4.5], center=false); // L2
    }

    // 9. Buffer Capacitor C_BUF (7343 D-Case Polymer)
    color("gold") {
        translate([65.0 - 3.65, 42.0 - 2.15, FRONT_NODE_PCB_H])
            cube(size=[7.3, 4.3, 3.1], center=false);
    }

    // 10. Status RGB LED (WS2812B-2020)
    color("white") {
        translate([75.0 - 1.0, 42.0 - 1.0, FRONT_NODE_PCB_H])
            cube(size=[2.0, 2.0, 0.9], center=false);
    }

    // 11. SMD Pushbuttons SW1 (Boot) & SW2 (Reset)
    color("darkslategray") {
        translate([75.0 - 1.5, 35.0 - 1.5, FRONT_NODE_PCB_H]) cube(size=[3.0, 3.0, 1.5], center=false);
        translate([75.0 - 1.5, 15.0 - 1.5, FRONT_NODE_PCB_H]) cube(size=[3.0, 3.0, 1.5], center=false);
    }
}

// Standalone compilation
dummy_front_node_pcb();
