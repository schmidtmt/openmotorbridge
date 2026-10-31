// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal Front Node PCB (PCBA 05 v10.0)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/006_dummy_front_node_pcb.scad
// Description: Exact 1:1 3D dummy of openmotorbridge_front_node.kicad_pcb
//              (82.0 x 50.0 x 1.6 mm, 4-Layer FR4) reflecting the v10.0 routed
//              board with ESP32-E22 Dual Wi-Fi 6E (ANT1 & ANT2 U.FL sockets),
//              USB2514B Hub, SW3526 20W PD, Knowles MEMS, and JST connector rails.
// =============================================================================

include <../../00_common/parameters.scad>;

module dummy_front_node_pcb() {
    // 1. PCB Substrate (FR4 4-Layer Dark Blue/Green, 82.0 x 50.0 x 1.6 mm)
    color([0.10, 0.25, 0.20]) {
        difference() {
            // Rounded rectangle substrate matching KiCad Edge.Cuts
            linear_extrude(height = FRONT_NODE_PCB_H) {
                offset(r = FRONT_NODE_PCB_R) {
                    offset(delta = -FRONT_NODE_PCB_R) {
                        square([FRONT_NODE_PCB_L, FRONT_NODE_PCB_W], center=false);
                    }
                }
            }
            
            // 4x M2.5 Mounting Holes (KiCad H1-H4 at 75.0 x 43.0 mm pitch)
            translate([3.50, 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([FRONT_NODE_PCB_L - 3.50, 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([3.50, FRONT_NODE_PCB_W - 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            translate([FRONT_NODE_PCB_L - 3.50, FRONT_NODE_PCB_W - 3.50, -0.1]) cylinder(r=1.35, h=FRONT_NODE_PCB_H + 0.2, $fn=24);
            
            // Knowles MEMS Acoustic sound port hole (Ø 0.8 mm) at (11.20, 46.30)
            translate([11.20, 46.30, -0.1]) cylinder(r=0.4, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
        }
    }

    // 2. Dual U.FL Antenna Ports for ESP32-E22 (2x2 MIMO 5/6 GHz Wi-Fi 6E)
    // ANT1 at (12.20, 2.00) and ANT2 at (8.50, 2.00)
    color("gold") {
        translate([12.20, 2.00, FRONT_NODE_PCB_H]) {
            cylinder(r=1.2, h=1.4, $fn=16);
            translate([0, 0, 1.4]) cylinder(r=0.6, h=0.4, $fn=16);
        }
        translate([8.50, 2.00, FRONT_NODE_PCB_H]) {
            cylinder(r=1.2, h=1.4, $fn=16);
            translate([0, 0, 1.4]) cylinder(r=0.6, h=0.4, $fn=16);
        }
    }

    // 3. ESP32-S3 / ESP32-E22 Radio & Core Controller Module (U1 at 10.34, 25.45)
    color("silver") {
        translate([10.34 - 9.0, 25.45 - 9.0, FRONT_NODE_PCB_H])
            cube(size=[18.0, 18.0, 3.0], center=false); // Shield can
    }

    // 4. Microchip USB2514B Automotive 4-Port USB 2.0 Hub (U2 at 30.41, 21.50)
    color("darkslategray") {
        translate([30.41 - 3.0, 21.50 - 3.0, FRONT_NODE_PCB_H])
            cube(size=[6.0, 6.0, 0.9], center=false); // QFN-36
    }

    // 5. SW3526 Synchronous Step-Down USB-PD Controller (U5 at 42.56, 12.45)
    color("darkslategray") {
        translate([42.56 - 2.0, 12.45 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 0.85], center=false); // QFN-28
    }

    // 6. Knowles SPH0645 Digital I2S MEMS Microphone (MK1 at 11.20, 46.30)
    color("goldenrod") {
        translate([11.20 - 1.75, 46.30 - 1.32, FRONT_NODE_PCB_H])
            cube(size=[3.5, 2.65, 1.0], center=false);
    }

    // 7. Tactical Switches: SW1 (Boot at 2.25, 11.10) & SW2 (Reset at 2.25, 40.50)
    color("dimgray") {
        translate([2.25 - 1.5, 11.10 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.6], center=false);
        translate([2.25 - 1.5, 40.50 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.6], center=false);
    }

    // 8. Status RGB LED (LED1 WS2812B-2020 at 80.20, 37.08)
    color("white") {
        translate([80.20 - 1.0, 37.08 - 1.0, FRONT_NODE_PCB_H])
            cube(size=[2.0, 2.0, 0.9], center=false);
    }

    // 9. North Edge Connectors (J1, J4, J_DONGLE, J_AUX_LIGHT, J10, J8)
    color("ghostwhite") {
        // J1 (JST GH 4P at 20.47, 3.35)
        translate([20.47 - 3.5, 3.35 - 2.0, FRONT_NODE_PCB_H]) cube([7.0, 4.0, 4.5], center=false);
        // J4 (JST GH 6P at 32.22, 3.35)
        translate([32.22 - 4.75, 3.35 - 2.0, FRONT_NODE_PCB_H]) cube([9.5, 4.0, 4.5], center=false);
        // J_DONGLE (JST GH 4P at 43.97, 3.35)
        translate([43.97 - 3.5, 3.35 - 2.0, FRONT_NODE_PCB_H]) cube([7.0, 4.0, 4.5], center=false);
        // J_AUX_LIGHT (JST PH 2P at 54.00, 7.00)
        translate([54.00 - 3.0, 7.00 - 2.5, FRONT_NODE_PCB_H]) cube([6.0, 5.0, 5.5], center=false);
        // J10 (JST PH 2P at 62.25, 7.00)
        translate([62.25 - 3.0, 7.00 - 2.5, FRONT_NODE_PCB_H]) cube([6.0, 5.0, 5.5], center=false);
        // J8 (JST PH 2P at 70.25, 6.95)
        translate([70.25 - 3.0, 6.95 - 2.5, FRONT_NODE_PCB_H]) cube([6.0, 5.0, 5.5], center=false);
    }

    // 10. South Edge Connectors (J_POD_R, J_DISP_R, J_SENSOR_EXT, J_DISP_L, J_POD_L)
    color("ghostwhite") {
        // J_POD_R (JST GH 4P at 21.50, 46.50)
        translate([21.50 - 3.5, 46.50 - 2.0, FRONT_NODE_PCB_H]) cube([7.0, 4.0, 4.5], center=false);
        // J_DISP_R (JST SH 4P at 33.50, 46.50)
        translate([33.50 - 3.0, 46.50 - 1.5, FRONT_NODE_PCB_H]) cube([6.0, 3.0, 3.2], center=false);
        // J_SENSOR_EXT (JST GH 6P at 46.50, 46.50)
        translate([46.50 - 4.75, 46.50 - 2.0, FRONT_NODE_PCB_H]) cube([9.5, 4.0, 4.5], center=false);
        // J_DISP_L (JST SH 4P at 59.50, 46.50)
        translate([59.50 - 3.0, 46.50 - 1.5, FRONT_NODE_PCB_H]) cube([6.0, 3.0, 3.2], center=false);
        // J_POD_L (JST GH 4P at 70.50, 46.50)
        translate([70.50 - 3.5, 46.50 - 2.0, FRONT_NODE_PCB_H]) cube([7.0, 4.0, 4.5], center=false);
    }
}

// Standalone compilation
dummy_front_node_pcb();
