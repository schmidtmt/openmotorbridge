// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Universal Front Node PCB (PCBA 05 v10.0)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/006_dummy_front_node_pcb.scad
// Description: Exact 1:1 3D dummy of openmotorbridge_front_node.kicad_pcb
//              (82.0 x 50.0 x 1.6 mm, 4-Layer FR4) reflecting the v10.0 routed
//              board with ESP32-S31 + ESP32-E22, Feasycom FSC-BT802 (U2),
//              Microchip USB2514Bi Hub (U4), SW3526 30W Fast-Charge, Knowles MEMS,
//              and horizontal JST GH connectors.
//
// Axis convention:
//   X: West (0 mm) -> East (82 mm)
//   Y: South (0 mm, Cockpit) -> North (50 mm, Vehicle / Front)
//   Z: Bottom (0 mm) -> Top (1.6 mm substrate + components)
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
            
            // Knowles MEMS Acoustic sound port hole (Ø 0.8 mm) at (11.20, 3.70)
            translate([11.20, 3.70, -0.1]) cylinder(r=0.4, h=FRONT_NODE_PCB_H + 0.2, $fn=16);
        }
    }

    // 2. Dual U.FL Antenna Ports for Wi-Fi (ANT1 at 12.20, 48.00 and ANT2 at 8.50, 48.00)
    color("gold") {
        translate([12.20, 48.00, FRONT_NODE_PCB_H]) {
            cylinder(r=1.2, h=1.4, $fn=16);
            translate([0, 0, 1.4]) cylinder(r=0.6, h=0.4, $fn=16);
        }
        translate([8.50, 48.00, FRONT_NODE_PCB_H]) {
            cylinder(r=1.2, h=1.4, $fn=16);
            translate([0, 0, 1.4]) cylinder(r=0.6, h=0.4, $fn=16);
        }
    }

    // 3. ESP32-S31-WROOM-1U Core Controller Module (U1 at 10.34, 24.55)
    color("silver") {
        translate([10.34 - 9.0, 24.55 - 12.75, FRONT_NODE_PCB_H])
            cube(size=[18.0, 25.5, 3.2], center=false); // Shield can
    }

    // 4. Feasycom FSC-BT802 Bluetooth 5.1 Infotainment Module (U2 at 30.16, 21.25)
    // CSR8670 Dual-Mode Audio: 10.0 x 13.0 x 2.0 mm with shield can
    color([0.15, 0.40, 0.55]) {
        translate([30.16 - 5.0, 21.25 - 6.5, FRONT_NODE_PCB_H])
            cube(size=[10.0, 13.0, 2.0], center=false);
    }

    // 5. ESP32-E22 High-Power Wi-Fi 6E Subsystem (U3 at 9.00, 43.25)
    color("silver") {
        translate([9.00 - 4.0, 43.25 - 4.0, FRONT_NODE_PCB_H])
            cube(size=[8.0, 8.0, 1.8], center=false); // Shield can
    }

    // 6. Microchip USB2514Bi Automotive 4-Port USB Hub (U4 at 53.00, 22.00)
    color("darkslategray") {
        translate([53.00 - 2.5, 22.00 - 2.5, FRONT_NODE_PCB_H])
            cube(size=[5.0, 5.0, 0.9], center=false); // QFN-32
    }

    // 7. SW3526 Synchronous Step-Down USB-PD Controller (U5 at 42.56, 37.55)
    color("darkslategray") {
        translate([42.56 - 2.0, 37.55 - 2.0, FRONT_NODE_PCB_H])
            cube(size=[4.0, 4.0, 0.85], center=false); // QFN-28
    }

    // 8. Knowles SPH0645 Digital I2S MEMS Microphone (MK1 at 11.20, 3.70)
    color("goldenrod") {
        translate([11.20 - 1.75, 3.70 - 1.32, FRONT_NODE_PCB_H])
            cube(size=[3.5, 2.65, 1.0], center=false);
    }

    // 9. Tactical Switches: SW1 (Boot at 2.25, 38.90) & SW2 (Reset at 2.25, 9.50)
    color("dimgray") {
        translate([2.25 - 1.5, 38.90 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.6], center=false);
        translate([2.25 - 1.5, 9.50 - 1.5, FRONT_NODE_PCB_H])
            cube(size=[3.0, 3.0, 1.6], center=false);
    }

    // 10. Status RGB LED (LED1 WS2812B-2020 at 80.20, 12.92)
    color("white") {
        translate([80.20 - 1.0, 12.92 - 1.0, FRONT_NODE_PCB_H])
            cube(size=[2.0, 2.0, 0.9], center=false);
    }

    // 11. Power Regulators: U3 (TPS54302 at 74.14, 37.50), U4 (TPS2051B at 25.61, 38.55), U7 (TLV75533 at 6.80, 9.86)
    color("darkslategray") {
        translate([74.14 - 1.5, 37.50 - 1.5, FRONT_NODE_PCB_H]) cube([3.0, 3.0, 1.4], center=false);
        translate([25.61 - 1.5, 38.55 - 1.5, FRONT_NODE_PCB_H]) cube([3.0, 3.0, 1.4], center=false);
        translate([6.80 - 1.5, 9.86 - 1.5, FRONT_NODE_PCB_H]) cube([3.0, 3.0, 1.4], center=false);
    }

    // 12. NORTH EDGE CONNECTORS (Vehicle & Accessories: J1, J4, J5, J7, J10, J8 at Y = 46.65 mm, facing +Y)
    color("ghostwhite") {
        // J1: Backbone 4P JST GH (19.73, 46.65)
        translate([19.73 - 3.5, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
        // J4: Ext Hub 8P JST GH (32.85, 46.65)
        translate([32.85 - 6.0, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([12.0, 4.25, 4.5], center=false);
        // J5: Dongle 4P JST GH (45.98, 46.65)
        translate([45.98 - 3.5, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
        // J7: Aux Light 2P JST GH (55.35, 46.65)
        translate([55.35 - 2.25, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([4.5, 4.25, 4.5], center=false);
        // J10: Navi Power 2P JST GH (63.48, 46.65)
        translate([63.48 - 2.25, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([4.5, 4.25, 4.5], center=false);
        // J8: Cam Power 2P JST GH (71.60, 46.65)
        translate([71.60 - 2.25, 46.65 - 0.25, FRONT_NODE_PCB_H]) cube([4.5, 4.25, 4.5], center=false);
    }

    // 13. SOUTH EDGE CONNECTORS (Cockpit: J3, J11, J6, J9, J2 at Y = 3.50 mm, facing -Y)
    color("ghostwhite") {
        // J3: Pod R 4P JST GH (19.73, 3.50)
        translate([19.73 - 3.5, 3.50 - 4.0, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
        // J11: Disp R 4P JST GH (31.24, 3.50)
        translate([31.24 - 3.5, 3.50 - 4.0, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
        // J6: Sensor Puck 8P JST GH (45.25, 3.50)
        translate([45.25 - 6.0, 3.50 - 4.0, FRONT_NODE_PCB_H]) cube([12.0, 4.25, 4.5], center=false);
        // J9: Disp L 4P JST GH (59.26, 3.50)
        translate([59.26 - 3.5, 3.50 - 4.0, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
        // J2: Pod L 4P JST GH (70.77, 3.50)
        translate([70.77 - 3.5, 3.50 - 4.0, FRONT_NODE_PCB_H]) cube([7.0, 4.25, 4.5], center=false);
    }
}

// Standalone compilation
dummy_front_node_pcb();
