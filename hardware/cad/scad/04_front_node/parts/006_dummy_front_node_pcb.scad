// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal Front Node PCB (PCBA 05)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/006_dummy_front_node_pcb.scad
// Description: Exact 1:1 3D dummy of openmotorbridge_front_node.kicad_pcb
//              (82.0 x 50.0 x 1.6 mm, 4-Layer FR4) reflecting the post-enlargement
//              routed board with Dual SW3526 USB-PD 20W subsystem, ESP32-S3,
//              USB2514B 4-Port Hub, Knowles MEMS, and North/South/East connector rails.
// =============================================================================

include <../../00_common/parameters.scad>;

module dummy_front_node_pcb() {
    // 1. PCB Substrate (FR4 4-Layer Green, 82.0 x 50.0 x 1.6 mm)
    color("forestgreen") {
        difference() {
            // Rounded rectangle substrate matching KiCad Edge.Cuts
            linear_extrude(height = FRONT_NODE_PCB_H) {
                offset(r = FRONT_NODE_PCB_R) {
                    offset(delta = -FRONT_NODE_PCB_R) {
                        square([FRONT_NODE_PCB_L, FRONT_NODE_PCB_W], center=false);
                    }
                }
            }
            
            // 4x M2.5 Mounting Holes (KiCad H1-H4)
            translate([3.50, 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([FRONT_NODE_PCB_L - 3.50, 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([3.50, FRONT_NODE_PCB_W - 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([FRONT_NODE_PCB_L - 3.50, FRONT_NODE_PCB_W - 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            
            // Knowles MEMS Acoustic sound port hole (Ø 0.5 mm) at (43.00, 28.96)
            translate([43.00, 28.96, -0.1]) cylinder(r=0.25, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
        }
    }

    // 2. South Connectors (6x JST-PH along front rim Y = 4.0 mm, facing South)
    // J4 (Host 4P), J5 (Phone PD 5P), J6 (CP2AA 4P), J5_MP3 (Glovebox PD 5P), J6_AUX (Cockpit 4P), J8 (Action-Cam 2P)
    color("ghostwhite") {
        translate([15.25 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J4 (4-Pin)
        translate([29.00 - 6.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[12.0, 4.5, 7.5], center=false); // J5 (5-Pin mit CC)
        translate([40.50 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J6 (4-Pin)
        translate([53.75 - 6.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[12.0, 4.5, 7.5], center=false); // J5_MP3 (5-Pin mit CC)
        translate([65.25 - 5.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J6_AUX (4-Pin)
        translate([72.75 - 3.0, 0.5, FRONT_NODE_PCB_H]) cube(size=[6.0, 4.5, 7.5], center=false);  // J8 (2-Pin)
    }

    // 3. North Connectors (6x JST-PH along rear rim Y = 46.5 mm, facing North)
    // J9 (BSD 3P), J3 (PTT 4P), J1 (12V 2P), J10 (Qi 2P), J11 (Aux 2P), J2 (CAN 3P)
    color("ghostwhite") {
        translate([25.50 - 4.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[8.0, 4.5, 7.5], center=false);  // J9 (3-Pin)
        translate([35.25 - 5.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[10.0, 4.5, 7.5], center=false); // J3 (4-Pin)
        translate([46.75 - 3.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[6.0, 4.5, 7.5], center=false);  // J1 (2-Pin)
        translate([53.75 - 3.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[6.0, 4.5, 7.5], center=false);  // J10 (2-Pin)
        translate([60.75 - 3.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[6.0, 4.5, 7.5], center=false);  // J11 (2-Pin)
        translate([67.75 - 4.0, FRONT_NODE_PCB_W - 5.0, FRONT_NODE_PCB_H]) cube(size=[8.0, 4.5, 7.5], center=false);  // J2 (3-Pin)
    }

    // 4. East Rim Connectors, Sensors & User Interfaces (X = 77..79 mm)
    // J7 USB-C Service Port (facing East)
    color("silver") {
        translate([FRONT_NODE_PCB_L - 7.5, 15.07 - 4.5, FRONT_NODE_PCB_H])
            cube(size=[8.0, 9.0, 3.2], center=false);
    }
    // J12 Qwiic I2C (1.0mm JST-SH 4-Pin, facing East)
    color("ghostwhite") {
        translate([FRONT_NODE_PCB_L - 5.5, 25.05 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[5.0, 5.0, 3.0], center=false);
    }
    // Status RGB LED (WS2812B-2020) at (79.41, 31.05)
    color("white") {
        translate([79.41 - 1.0, 31.05 - 1.0, FRONT_NODE_PCB_H])
            cube(size=[2.0, 2.0, 0.9], center=false);
    }
    // SW1 (Boot Button) at (73.60, 31.00)
    color("darkslategray") {
        translate([73.60 - 1.5, 31.00 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.5], center=false);
    }
    // SW2 (Reset Button) at (63.10, 12.25)
    color("darkslategray") {
        translate([63.10 - 1.5, 12.25 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.5], center=false);
    }
    // Buffer Capacitor C_BUF (7343 D-Case Polymer 470uF) at (78.25, 38.63)
    color("gold") {
        translate([78.25 - 3.65, 38.63 - 2.15, FRONT_NODE_PCB_H])
            cube(size=[7.3, 4.3, 3.1], center=false);
    }

    // 5. ESP32-S3-WROOM-1U Module with U.FL Socket at (57.75, 31.59)
    color("silver") {
        translate([57.75 - 9.0, 31.59 - 12.75, FRONT_NODE_PCB_H])
            cube(size=[18.0, 25.5, 3.2], center=false);
    }
    color("gold") {
        translate([57.75, 31.59 + 10.0, FRONT_NODE_PCB_H + 3.2])
            cylinder(r=1.0, h=1.0, $fn=16); // U.FL connector
    }

    // 6. Microchip USB2514B 4-Port Automotive USB Hub (QFN-36) at (42.00, 18.00)
    color("darkslategray") {
        translate([42.00 - 3.0, 18.00 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[6.0, 6.0, 0.9], center=false);
    }
    // 24.000 MHz Crystal Y1 at (33.40, 18.15)
    color("silver") {
        translate([33.40 - 1.6, 18.15 - 1.25, FRONT_NODE_PCB_H])
            cube(size=[3.2, 2.5, 0.8], center=false);
    }

    // 7. Dual Independent SW3526 USB-PD 20W Fast Charge Controllers (QFN-28 4x4mm)
    color("darkslategray") {
        translate([15.00 - 2.0, 26.50 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 0.85], center=false); // U5 (PD1 Lenker)
        translate([21.50 - 2.0, 26.00 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 0.85], center=false); // U8 (PD3 Handschuhfach)
    }

    // 8. Power Inductors: L2 (PD1 5x5mm), L3 (PD3 5x5mm), L1 (Main 5V Buck 7x7mm)
    color("dimgray") {
        translate([15.00 - 2.5, 18.50 - 2.5, FRONT_NODE_PCB_H]) cube(size=[5.0, 5.0, 3.0], center=false); // L2 (PD1 Lenker)
        translate([21.50 - 2.5, 18.50 - 2.5, FRONT_NODE_PCB_H]) cube(size=[5.0, 5.0, 3.0], center=false); // L3 (PD3 Handschuhfach)
        translate([31.38 - 3.5, 33.75 - 3.5, FRONT_NODE_PCB_H]) cube(size=[7.0, 7.0, 3.0], center=false); // L1 (5V System Buck)
    }

    // 9. Knowles SPH0645 Digital I2S MEMS Microphone at (43.00, 28.96)
    color("goldenrod") {
        translate([43.00 - 1.75, 28.96 - 1.32, FRONT_NODE_PCB_H])
            cube(size=[3.5, 2.65, 1.0], center=false);
    }

    // 10. Automotive Power & Protection Stage (West area, internal)
    color("darkslategray") {
        // U3 (TPS54302 5V 3A Step-Down Buck, SOT-23-6) at (10.89, 41.80)
        translate([10.89 - 1.5, 41.80 - 1.5, FRONT_NODE_PCB_H]) cube(size=[3.0, 3.0, 1.3], center=false);
        // U6 (TCAN334G 3.3V CAN Transceiver, SOIC-8) at (5.16, 17.78)
        translate([5.16 - 2.0, 17.78 - 2.5, FRONT_NODE_PCB_H]) cube(size=[4.0, 5.0, 1.6], center=false);
        // K1 (CPC1017N Solid State Relay, SOP-4) at (9.69, 10.61)
        translate([9.69 - 2.2, 10.61 - 1.3, FRONT_NODE_PCB_H]) cube(size=[4.4, 2.6, 2.0], center=false);
        // Q2 (TPS1H100 Aux Light High-Side Switch, HTSSOP-14) at (5.36, 29.00)
        translate([5.36 - 2.2, 29.00 - 2.5, FRONT_NODE_PCB_H]) cube(size=[4.4, 5.0, 1.2], center=false);
        // U4 (TPS2051B CP2AA Power Switch, SOT-23-5) at (43.70, 35.64)
        translate([43.70 - 1.5, 35.64 - 1.5, FRONT_NODE_PCB_H]) cube(size=[3.0, 3.0, 1.3], center=false);
    }
    color("black") {
        // D4 (SMCJ36CA 36V TVS Diode, SMB) at (3.25, 38.60)
        translate([3.25 - 2.5, 38.60 - 1.8, FRONT_NODE_PCB_H]) cube(size=[5.0, 3.6, 2.3], center=false);
    }
}

// Standalone compilation
dummy_front_node_pcb();
