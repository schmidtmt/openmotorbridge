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
            
            // Knowles MEMS Acoustic sound port hole (Ø 0.5 mm) at (72.00, 37.75)
            translate([72.00, 37.75, -0.1]) cylinder(r=0.25, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
        }
    }

    // 2. South Master Cockpit Header: J_COCKPIT (16-Pin Dual-Row 2.0mm SMT Latch Header)
    // Sits at PCB relative X=27.50 mm, Y=5.50 mm (KiCad: X=127.50 mm, Y=114.50 mm)
    // Carries Host, Dongle, Phone 20W PD, Action-Cam 5V, Navi 5V, and PTT
    color("ghostwhite") {
        translate([27.50 - 9.0, 5.50 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[18.0, 5.0, 6.8], center=false); // 16-Pin Dual Row Shrouded Header
    }

    // 3. North Master Vehicle Header: J_VEHICLE (12-Pin Dual-Row 2.0mm SMT Latch Header)
    // Sits at PCB relative X=27.50 mm, Y=44.58 mm (KiCad: X=127.50 mm, Y=75.42 mm)
    // Carries 12V In, CAN-Bus, Mirror BSD, Aux Light, and I2C Sensor Bus (3V3, GND, SDA, SCL)
    color("ghostwhite") {
        translate([27.50 - 7.0, 44.58 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[14.0, 5.0, 6.8], center=false); // 12-Pin Dual Row Shrouded Header
    }

    // 4. East Rim Connectors, Sensors & User Interfaces (X = 77..79 mm)
    // J7 USB-C Service Port (facing East)
    color("silver") {
        translate([FRONT_NODE_PCB_L - 7.5, 15.0 - 4.5, FRONT_NODE_PCB_H])
            cube(size=[8.0, 9.0, 3.2], center=false);
    }
    // Status RGB LED (WS2812B-2020) at (79.41, 31.05)
    color("white") {
        translate([79.41 - 1.0, 31.05 - 1.0, FRONT_NODE_PCB_H])
            cube(size=[2.0, 2.0, 0.9], center=false);
    }
    // SW1 (Boot Button) at (72.25, 26.50)
    color("darkslategray") {
        translate([72.25 - 1.5, 26.50 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.5], center=false);
    }
    // SW2 (Reset Button) at (46.40, 46.25)
    color("darkslategray") {
        translate([46.40 - 1.5, 46.25 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.5], center=false);
    }
    // Buffer Capacitor C_BUF (7343 D-Case Polymer 470uF) at (61.75, 11.87)
    color("gold") {
        translate([61.75 - 3.65, 11.87 - 2.15, FRONT_NODE_PCB_H])
            cube(size=[7.3, 4.3, 3.1], center=false);
    }

    // 5. ESP32-S3-WROOM-1U Module with U.FL Socket at (64.10, 39.66)
    color("silver") {
        translate([64.10 - 9.0, 39.66 - 12.75, FRONT_NODE_PCB_H])
            cube(size=[18.0, 25.5, 3.2], center=false);
    }
    color("gold") {
        translate([64.10, 39.66 + 10.0, FRONT_NODE_PCB_H + 3.2])
            cylinder(r=1.0, h=1.0, $fn=16); // U.FL connector
    }

    // 6. Microchip USB2514B 4-Port Automotive USB Hub (QFN-36) at (36.50, 17.59)
    color("darkslategray") {
        translate([36.50 - 3.0, 17.59 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[6.0, 6.0, 0.9], center=false);
    }
    // 24.000 MHz Crystal Y1 at (26.90, 18.35)
    color("silver") {
        translate([26.90 - 1.6, 18.35 - 1.25, FRONT_NODE_PCB_H])
            cube(size=[3.2, 2.5, 0.8], center=false);
    }

    // 7. SW3526 USB-PD 20W Fast Charge Controller (QFN-28 4x4mm) at (18.31, 26.05)
    color("darkslategray") {
        translate([18.31 - 2.0, 26.05 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 0.85], center=false); // U5 (PD Fast Charge)
    }

    // 8. Power Inductors: L2 (PD1 5x5mm), L1 (Main 5V Buck 7x7mm)
    color("dimgray") {
        translate([15.00 - 2.5, 18.50 - 2.5, FRONT_NODE_PCB_H]) cube(size=[5.0, 5.0, 3.0], center=false); // L2 (PD)
        translate([31.12 - 3.5, 32.25 - 3.5, FRONT_NODE_PCB_H]) cube(size=[7.0, 7.0, 3.0], center=false); // L1 (5V System Buck)
    }

    // 9. Knowles SPH0645 Digital I2S MEMS Microphone at (42.75, 31.89) & (42.75, 37.00)
    color("goldenrod") {
        translate([42.75 - 1.75, 31.89 - 1.32, FRONT_NODE_PCB_H])
            cube(size=[3.5, 2.65, 1.0], center=false);
    }

    // 10. Qorvo DW3000 UWB Transceiver Subsystem (U9, Y_UWB, ANT_UWB) at (45.00, 25.00)
    color("darkslategray") {
        translate([45.0 - 2.5, 25.0 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[5.0, 5.0, 0.9], center=false); // U9 (DW3000 QFN)
    }
    color("silver") {
        translate([37.0 - 1.6, 25.0 - 1.25, FRONT_NODE_PCB_H])
            cube(size=[3.2, 2.5, 0.8], center=false); // ANT_UWB Ceramic / U.FL
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
