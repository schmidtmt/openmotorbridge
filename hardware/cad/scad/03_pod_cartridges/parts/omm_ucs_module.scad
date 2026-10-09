// =============================================================================
// OpenMotorBridge - OMM 2.4 GHz ECE 22.06 UCS Intercom Module Enclosure
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/omm_ucs_module.scad
// Description: Standalone, parametric 3D CAD model of the OpenMotorMesh (OMM)
//              2.4 GHz Intercom transceiver in standardized UCS form factor:
//              - ECE 22.06 UCS compliant envelope: 68.0 x 36.0 x 9.5 mm
//              - Top Shell (PA12 MJF) with 4x DIN 934 M2 captive hex nut pockets
//              - Bottom Shell (PA12 MJF) with 4x DIN 912 M2 screw counterbores
//                and 2x ECE 22.06 snap-fit helmet retention claws
//              - Monolithic Shore 50A silicone keypad with 4 tactile buttons
//                and translucent RGB status LED light pipe dome
//              - Perimeter IP67 sealing groove (1.0 mm wide x 1.2 mm deep)
//              - Front waterproof USB-C access port with O-ring seat
//              - 100% Soldering-Iron & Self-Tapping-Free: Infinite service cycles!
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;
use <../../00_common/dummies/dummy_omm_ucs_pcb.scad>;

// UCS Standard Dimensions
UCS_L          = 68.0; // Outer length in X (mm)
UCS_W          = 36.0; // Outer width in Y (mm)
UCS_H_TOP      = 5.5;  // Top shell height in Z (mm)
UCS_H_BOT      = 4.0;  // Bottom shell height in Z (mm)
UCS_H_TOTAL    = UCS_H_TOP + UCS_H_BOT; // 9.5 mm
UCS_CORNER_R   = 3.5;  // Exterior corner radius (mm)
UCS_WALL       = 1.5;  // Wall thickness (mm)

// Screw Centers (52.0 x 22.0 mm pitch, centered)
UCS_SCREW_X1   = (UCS_L - 52.0) / 2.0; // 8.0 mm
UCS_SCREW_X2   = UCS_L - UCS_SCREW_X1; // 60.0 mm
UCS_SCREW_Y1   = (UCS_W - 22.0) / 2.0; // 7.0 mm
UCS_SCREW_Y2   = UCS_W - UCS_SCREW_Y1; // 29.0 mm

// 1. OMM UCS Top Shell (PA12 MJF, Anthracite)
module omm_ucs_top_shell() {
    difference() {
        // Outer Shell Monocoque
        hull() {
            translate([UCS_CORNER_R, UCS_CORNER_R, 0])
                cylinder(r=UCS_CORNER_R, h=UCS_H_TOP, $fn=36);
            translate([UCS_L - UCS_CORNER_R, UCS_CORNER_R, 0])
                cylinder(r=UCS_CORNER_R, h=UCS_H_TOP, $fn=36);
            translate([UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0])
                cylinder(r=UCS_CORNER_R, h=UCS_H_TOP, $fn=36);
            translate([UCS_L - UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0])
                cylinder(r=UCS_CORNER_R, h=UCS_H_TOP, $fn=36);
        }

        // Inner Cavity (Z = -0.1 .. UCS_H_TOP - UCS_WALL)
        translate([UCS_WALL, UCS_WALL, -0.1]) {
            hull() {
                translate([UCS_CORNER_R - 0.5, UCS_CORNER_R - 0.5, 0])
                    cylinder(r=UCS_CORNER_R - 0.5, h=UCS_H_TOP - UCS_WALL + 0.1, $fn=24);
                translate([UCS_L - 2*UCS_WALL - (UCS_CORNER_R - 0.5), UCS_CORNER_R - 0.5, 0])
                    cylinder(r=UCS_CORNER_R - 0.5, h=UCS_H_TOP - UCS_WALL + 0.1, $fn=24);
                translate([UCS_CORNER_R - 0.5, UCS_W - 2*UCS_WALL - (UCS_CORNER_R - 0.5), 0])
                    cylinder(r=UCS_CORNER_R - 0.5, h=UCS_H_TOP - UCS_WALL + 0.1, $fn=24);
                translate([UCS_L - 2*UCS_WALL - (UCS_CORNER_R - 0.5), UCS_W - 2*UCS_WALL - (UCS_CORNER_R - 0.5), 0])
                    cylinder(r=UCS_CORNER_R - 0.5, h=UCS_H_TOP - UCS_WALL + 0.1, $fn=24);
            }
        }

        // Keypad Top Recess & Button Pass-Through Apertures (Z = UCS_H_TOP - 1.5 .. UCS_H_TOP + 0.2)
        translate([9.0, 6.0, UCS_H_TOP - 1.2]) {
            cube(size=[50.0, 24.5, 1.5], center=false);
        }

        // 4x Button Stem Holes (Ø 5.0 mm for tactile button plungers)
        // KiCad SW1..SW4: X=83, 95, 107, 119 -> X_rel = 13, 25, 37, 49 -> X_mod = 17, 29, 41, 53 mm
        // KiCad Y=107.0 -> Y_rel = 22.0 -> Y_mod = 3.0 + 22.0 = 25.0 mm
        translate([17.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([29.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([41.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([53.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);

        // RGB LED Diffuser Hole (Ø 2.5 mm)
        // KiCad D1 (WS2812B): X=100.98 -> X_mod = 34.98 mm (centered between SW2 and SW3)
        // KiCad Y=111.22 -> Y_mod = 3.0 + (111.22 - 85.0) = 29.22 mm
        translate([35.0, 29.22, UCS_H_TOP - 2.5]) cylinder(r=1.3, h=3.0, $fn=20);

        // Perimeter Sealing Groove (1.0 mm wide x 1.2 mm deep for Shore 40A silicone bead)
        translate([0, 0, -0.1]) {
            difference() {
                hull() {
                    translate([UCS_CORNER_R, UCS_CORNER_R, 0]) cylinder(r=UCS_CORNER_R - 0.2, h=1.3, $fn=36);
                    translate([UCS_L - UCS_CORNER_R, UCS_CORNER_R, 0]) cylinder(r=UCS_CORNER_R - 0.2, h=1.3, $fn=36);
                    translate([UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0]) cylinder(r=UCS_CORNER_R - 0.2, h=1.3, $fn=36);
                    translate([UCS_L - UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0]) cylinder(r=UCS_CORNER_R - 0.2, h=1.3, $fn=36);
                }
                hull() {
                    translate([UCS_CORNER_R + 1.0, UCS_CORNER_R + 1.0, -0.1]) cylinder(r=UCS_CORNER_R - 0.2, h=1.5, $fn=36);
                    translate([UCS_L - UCS_CORNER_R - 1.0, UCS_CORNER_R + 1.0, -0.1]) cylinder(r=UCS_CORNER_R - 0.2, h=1.5, $fn=36);
                    translate([UCS_CORNER_R + 1.0, UCS_W - UCS_CORNER_R - 1.0, -0.1]) cylinder(r=UCS_CORNER_R - 0.2, h=1.5, $fn=36);
                    translate([UCS_L - UCS_CORNER_R - 1.0, UCS_W - UCS_CORNER_R - 1.0, -0.1]) cylinder(r=UCS_CORNER_R - 0.2, h=1.5, $fn=36);
                }
            }
        }

        // 4x Form-Fitting DIN 934 M2 Hex Nut Pockets (Captive Nuts, NO plastic tapping!)
        translate([UCS_SCREW_X1, UCS_SCREW_Y1, 1.2]) hex_nut_pocket(sw=NUT_M2_SW, h=NUT_M2_H, screw_r=M2_SCREW_HOLE_R, through_h=4.0);
        translate([UCS_SCREW_X2, UCS_SCREW_Y1, 1.2]) hex_nut_pocket(sw=NUT_M2_SW, h=NUT_M2_H, screw_r=M2_SCREW_HOLE_R, through_h=4.0);
        translate([UCS_SCREW_X1, UCS_SCREW_Y2, 1.2]) hex_nut_pocket(sw=NUT_M2_SW, h=NUT_M2_H, screw_r=M2_SCREW_HOLE_R, through_h=4.0);
        translate([UCS_SCREW_X2, UCS_SCREW_Y2, 1.2]) hex_nut_pocket(sw=NUT_M2_SW, h=NUT_M2_H, screw_r=M2_SCREW_HOLE_R, through_h=4.0);

        // Front USB-C Port Tunnel Half-Cutout (-X Edge)
        translate([-0.5, (UCS_W - 9.5)/2.0, -0.1])
            cube(size=[4.0, 9.5, 2.0], center=false);

        // Rear RF Coax Port Half-Cutout (+X Edge) for PCBA 10 U.FL J_RF
        translate([UCS_L - 3.5, (UCS_W - 5.0)/2.0, -0.1])
            cube(size=[4.0, 5.0, 1.8], center=false);
    }
}

// 2. OMM UCS Bottom Shell (PA12 MJF with ECE 22.06 Snap-Fit Claws)
module omm_ucs_bottom_shell() {
    difference() {
        union() {
            // Main Bottom Monocoque
            hull() {
                translate([UCS_CORNER_R, UCS_CORNER_R, 0])
                    cylinder(r=UCS_CORNER_R, h=UCS_H_BOT, $fn=36);
                translate([UCS_L - UCS_CORNER_R, UCS_CORNER_R, 0])
                    cylinder(r=UCS_CORNER_R, h=UCS_H_BOT, $fn=36);
                translate([UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0])
                    cylinder(r=UCS_CORNER_R, h=UCS_H_BOT, $fn=36);
                translate([UCS_L - UCS_CORNER_R, UCS_W - UCS_CORNER_R, 0])
                    cylinder(r=UCS_CORNER_R, h=UCS_H_BOT, $fn=36);
            }

            // 2x ECE 22.06 Flexible Snap-Fit Retaining Claws (Flanks)
            // Left Flank Claw
            translate([UCS_L/2.0 - 6.0, -1.2, 0]) {
                cube(size=[12.0, 1.4, UCS_H_BOT - 0.5], center=false);
                // 45° Lead-in Catch Nose
                translate([0, -0.4, UCS_H_BOT - 1.8])
                    cube(size=[12.0, 0.6, 1.3], center=false);
            }
            // Right Flank Claw
            translate([UCS_L/2.0 - 6.0, UCS_W - 0.2, 0]) {
                cube(size=[12.0, 1.4, UCS_H_BOT - 0.5], center=false);
                // 45° Lead-in Catch Nose
                translate([0, 1.2, UCS_H_BOT - 1.8])
                    cube(size=[12.0, 0.6, 1.3], center=false);
            }
        }

        // Inner Battery Recess (600 mAh LiPo: 38 x 24 x 4.5 mm + 0.5 mm EPDM pad)
        translate([(UCS_L - 40.0)/2.0, (UCS_W - 25.0)/2.0, UCS_WALL]) {
            cube(size=[40.0, 25.0, UCS_H_BOT + 0.1], center=false);
        }

        // Perimeter Tongue Ridge (Matching Top Shell Groove)
        translate([0, 0, UCS_H_BOT - 1.0]) {
            // Cut clearance around tongue
            difference() {
                cube(size=[UCS_L, UCS_W, 1.2], center=false);
                hull() {
                    translate([UCS_CORNER_R + 0.8, UCS_CORNER_R + 0.8, -0.1]) cylinder(r=UCS_CORNER_R - 0.8, h=1.4, $fn=36);
                    translate([UCS_L - UCS_CORNER_R - 0.8, UCS_CORNER_R + 0.8, -0.1]) cylinder(r=UCS_CORNER_R - 0.8, h=1.4, $fn=36);
                    translate([UCS_CORNER_R + 0.8, UCS_W - UCS_CORNER_R - 0.8, -0.1]) cylinder(r=UCS_CORNER_R - 0.8, h=1.4, $fn=36);
                    translate([UCS_L - UCS_CORNER_R - 0.8, UCS_W - UCS_CORNER_R - 0.8, -0.1]) cylinder(r=UCS_CORNER_R - 0.8, h=1.4, $fn=36);
                }
            }
        }

        // 4x DIN 912 M2 Screw Through-Holes with Head Counterbores (From Bottom Face)
        for (pos = [
            [UCS_SCREW_X1, UCS_SCREW_Y1],
            [UCS_SCREW_X2, UCS_SCREW_Y1],
            [UCS_SCREW_X1, UCS_SCREW_Y2],
            [UCS_SCREW_X2, UCS_SCREW_Y2]
        ]) {
            // Screw Clearance Hole
            translate([pos[0], pos[1], -0.1])
                cylinder(r=M2_SCREW_HOLE_R, h=UCS_H_BOT + 0.2, $fn=24);
            // Counterbore for DIN 912 M2 Head (Ø 4.2 mm, depth 2.2 mm)
            translate([pos[0], pos[1], -0.1])
                cylinder(r=2.1, h=2.2, $fn=30);
        }

        // Front USB-C Port Tunnel Half-Cutout (-X Edge)
        translate([-0.5, (UCS_W - 9.5)/2.0, UCS_H_BOT - 2.0])
            cube(size=[4.0, 9.5, 2.2], center=false);

        // Rear RF Coax Port Half-Cutout (+X Edge) for PCBA 10 U.FL J_RF
        translate([UCS_L - 3.5, (UCS_W - 5.0)/2.0, UCS_H_BOT - 2.0])
            cube(size=[4.0, 5.0, 2.2], center=false);
    }
}

// 3. Monolithic Shore 50A Silicone Keypad (100% Watertight, Zero Holes)
module omm_ucs_silicone_keypad() {
    color([0.15, 0.15, 0.16]) {
        // Base Mat Plate (0.8 mm thick)
        cube(size=[49.0, 23.5, 0.8], center=false);

        // 4 Raised Tactile Key Domes (aligned with SW1..SW4 at X_mod = 17, 29, 41, 53 mm; keypad base X=9.5 -> rel_X = 7.5, 19.5, 31.5, 43.5 mm)
        // Y_mod = 25.0 mm; keypad base Y=6.5 -> rel_Y = 18.5 mm
        translate([7.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30);  // Power / PTT (SW1)
        translate([19.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Mesh / Mode (SW2)
        translate([31.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Vol+ / Ch+ (SW3)
        translate([43.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Vol- / Ch- (SW4)
    }

    // Translucent Silicone RGB-LED Light-Pipe Dome (aligned with D1 at X_mod = 35.0, Y_mod = 29.22 mm; keypad rel = 25.5, 22.72 mm)
    color("cyan", 0.7) {
        translate([25.5, 22.72, 0.8])
            cylinder(r=1.2, h=1.5, $fn=20);
    }
}

// 4. Complete OMM UCS Module Assembly (Dual-Use: Standalone Helmet & Pod Cartridge)
module omm_ucs_module_assembly(exploded = false) {
    z_bot    = 0.0;
    z_pcb    = exploded ? 14.0 : 1.6;
    z_top    = exploded ? 28.0 : UCS_H_BOT;
    z_key    = exploded ? 38.0 : (UCS_H_BOT + UCS_H_TOP - 1.2);
    z_screws = exploded ? -14.0 : -2.0;

    // A. Bottom Shell (PA12 Charcoal)
    color([0.22, 0.24, 0.26])
        omm_ucs_bottom_shell();

    // B. Internal PCBA 09 with LiPo & Components
    translate([4.0, 3.0, z_pcb])
        dummy_omm_ucs_pcb();

    // C. Top Shell (Sits directly on bottom shell without inverted rotation)
    color([0.18, 0.20, 0.22])
        translate([0, 0, z_top])
            omm_ucs_top_shell();

    // D. Waterproof Silicone Keypad (Aligned with top shell button apertures)
    translate([9.5, 6.5, z_key])
        omm_ucs_silicone_keypad();

    // E. 4x DIN 912 M2 x 8 mm Stainless Steel Screws (Thread from bottom into captive M2 nuts)
    color("silver") {
        for (pos = [
            [UCS_SCREW_X1, UCS_SCREW_Y1],
            [UCS_SCREW_X2, UCS_SCREW_Y1],
            [UCS_SCREW_X1, UCS_SCREW_Y2],
            [UCS_SCREW_X2, UCS_SCREW_Y2]
        ]) {
            translate([pos[0], pos[1], z_screws])
                cylinder(r=1.0, h=8.0, $fn=20);
        }
    }
}

// Standalone Preview
omm_ucs_module_assembly(exploded = true);
