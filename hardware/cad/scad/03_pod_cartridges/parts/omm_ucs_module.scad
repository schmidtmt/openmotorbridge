// =============================================================================
// OpenMotorBridge - Universal OMM Tri-Band ECE 22.06 UCS Intercom Module
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/omm_ucs_module.scad
// Description: Standalone, parametric 3D CAD model of the unified OpenMotorMesh
//              (OMM) Universal Tri-Band Intercom transceiver (2.4 GHz HD-Mesh +
//              BT Classic/BLE Bridge + 446 MHz Analog PMR446 / Digital DMR Tier I)
//              in standardized ECE 22.06 UCS form factor:
//              - ECE 22.06 UCS compliant envelope: 68.0 x 36.0 x 16.0 mm
//                (7 mm thinner than Cardo Packtalk Edge [23 mm], 11 mm thinner
//                than Sena 50S [27 mm], matching Sena 50R Slim [16 mm]!)
//              - Accommodates both the NiceRF SA818-DMR (38 x 16 x 3.2 mm) AND
//                a full 1000 mAh 1S LiPo Pouch Cell (Typ 603040 / 602840:
//                40 x 28 x 6.0 mm) with 0.0 mm bottom protrusion
//              - BAT1 (2-Pin JST-SH) placed directly beneath J1 USB-C on B.Cu
//                (Local X=3.45, Y=15.05 mm) -> 100% clear of the 1000 mAh battery!
//              - J_HELMET (6-Pin JST-SH) placed at +X edge on B.Cu
//                (Local X=57.05, Y=14.70 mm) -> 100% clear of the 1000 mAh battery!
//              - Top Shell (PA12 MJF) with 4x DIN 934 M2 captive hex nut pockets
//                and internal 2.4 GHz FPC antenna recess
//              - Bottom Shell (PA12 MJF) with 4x DIN 912 M2 screw counterbores
//                and 2x ECE 22.06 snap-fit helmet retention claws
//              - Monolithic Shore 50A silicone keypad with 4 tactile buttons
//                and translucent RGB status LED light pipe dome
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;
use <../../00_common/dummies/dummy_omm446_ucs_pcb.scad>;

// UCS Standard Dimensions (Universal Tri-Band + 1000 mAh LiPo Envelope)
UCS_L          = 68.0; // Outer length in X (mm)
UCS_W          = 36.0; // Outer width in Y (mm)
UCS_H_BOT      = 10.5; // Bottom shell height in Z (mm: 1.1mm floor + 6.0mm 1000mAh LiPo + 0.2mm pad + 3.2mm SA818-DMR)
UCS_H_TOP      = 5.5;  // Top shell height in Z (mm: 1.0mm PCB + 3.2mm USB-C/C6 + 1.3mm ceiling)
UCS_H_TOTAL    = UCS_H_TOP + UCS_H_BOT; // 16.0 mm total height
UCS_CORNER_R   = 3.5;  // Exterior corner radius (mm)
UCS_WALL       = 1.5;  // Side wall thickness (mm)
UCS_FLOOR      = 1.1;  // Bottom floor thickness under battery (mm)

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

        // Keypad Top Recess & Button Pass-Through Apertures (Z = UCS_H_TOP - 1.2 .. UCS_H_TOP + 0.2)
        translate([9.0, 6.0, UCS_H_TOP - 1.2]) {
            cube(size=[50.0, 24.5, 1.5], center=false);
        }

        // 4x Button Stem Holes (Ø 5.0 mm for tactile button plungers)
        // KiCad SW1..SW4: Local X=13, 25, 37, 49 -> X_mod = 17, 29, 41, 53 mm; Y_mod = 25.0 mm
        translate([17.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([29.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([41.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);
        translate([53.0, 25.0, UCS_H_TOP - 2.5]) cylinder(r=2.5, h=3.0, $fn=24);

        // RGB LED Diffuser Hole (Ø 2.6 mm)
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

        // Rear Dual-SMA RF Coax Port Half-Cutouts (+X Edge: Port 1 @ Y=12.5 mm [2.4 GHz], Port 2 @ Y=23.5 mm [446 MHz])
        for (sma_y = [12.5, 23.5]) {
            translate([UCS_L - 3.5, sma_y - 2.5, -0.1])
                cube(size=[4.0, 5.0, 1.8], center=false);
        }
    }
}

// 2. OMM UCS Bottom Shell (PA12 MJF with 1000 mAh Battery Bay, BAT1 Pocket & ECE 22.06 Snap-Fit Claws)
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

            // 2x ECE 22.06 Flexible Snap-Fit Retaining Claws (Lower 4.0 mm Helmet Recess Zone)
            // Left Flank Claw
            translate([UCS_L/2.0 - 6.0, -1.2, 0]) {
                cube(size=[12.0, 1.4, 3.5], center=false);
                translate([0, -0.4, 2.2])
                    cube(size=[12.0, 0.6, 1.3], center=false);
            }
            // Right Flank Claw
            translate([UCS_L/2.0 - 6.0, UCS_W - 0.2, 0]) {
                cube(size=[12.0, 1.4, 3.5], center=false);
                translate([0, 1.2, 2.2])
                    cube(size=[12.0, 0.6, 1.3], center=false);
            }
        }

        // A. Central Inner Bay for 1000 mAh LiPo (40 x 28 x 6.0 mm) + SA818-DMR (38 x 16 x 3.2 mm)
        //    Spans X_mod = 13.0 .. 55.0 mm (42.0 mm length), Y_mod = 3.5 .. 32.5 mm (29.0 mm width), Z = 1.1 .. 10.6 mm
        translate([13.0, (UCS_W - 29.0)/2.0, UCS_FLOOR]) {
            cube(size=[42.0, 29.0, UCS_H_BOT - UCS_FLOOR + 0.1], center=false);
        }

        // B. Upper B.Cu Component Clearance Cavity (for U6 ESP32-PICO-V3-02, BAT1 under J1, and J_HELMET)
        //    Spans X_mod = 4.5 .. 63.5 mm, Y_mod = 3.5 .. 32.5 mm, Z = UCS_H_BOT - 3.6 .. UCS_H_BOT + 0.1 mm
        //    (Leaving the 4 corner screw posts at X=8/60, Y=7/29 solid!)
        translate([5.0, (UCS_W - 12.0)/2.0, UCS_H_BOT - 4.0]) {
            cube(size=[58.0, 12.0, 4.1], center=false);
        }
        // Clearance pocket for U6 ESP32-PICO-V3-02 at Local X=16.70, Y=4.45 -> X_mod=20.7, Y_mod=7.45
        translate([16.0, 3.2, UCS_H_BOT - 2.0]) {
            cube(size=[10.0, 9.0, 2.1], center=false);
        }

        // Perimeter Tongue Ridge (Matching Top Shell Groove at Z = UCS_H_BOT - 1.0 .. UCS_H_BOT)
        translate([0, 0, UCS_H_BOT - 1.0]) {
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

        // 4x DIN 912 M2 x 8 mm Screw Through-Holes with Deep Head Counterbores (From Bottom Face)
        for (pos = [
            [UCS_SCREW_X1, UCS_SCREW_Y1],
            [UCS_SCREW_X2, UCS_SCREW_Y1],
            [UCS_SCREW_X1, UCS_SCREW_Y2],
            [UCS_SCREW_X2, UCS_SCREW_Y2]
        ]) {
            // Screw Clearance Hole
            translate([pos[0], pos[1], -0.1])
                cylinder(r=M2_SCREW_HOLE_R, h=UCS_H_BOT + 0.2, $fn=24);
            // Counterbore for DIN 912 M2 Head (Ø 4.2 mm, depth 6.5 mm so M2x8mm reaches top shell nut pocket!)
            translate([pos[0], pos[1], -0.1])
                cylinder(r=2.1, h=6.5, $fn=30);
        }

        // Front USB-C Port Tunnel Half-Cutout (-X Edge)
        translate([-0.5, (UCS_W - 9.5)/2.0, UCS_H_BOT - 2.0])
            cube(size=[4.0, 9.5, 2.2], center=false);

        // Rear Dual-SMA RF Coax Port Half-Cutouts (+X Edge: Port 1 @ Y=12.5 mm [2.4 GHz], Port 2 @ Y=23.5 mm [446 MHz])
        for (sma_y = [12.5, 23.5]) {
            translate([UCS_L - 3.5, sma_y - 2.5, UCS_H_BOT - 2.0])
                cube(size=[4.0, 5.0, 2.2], center=false);
        }

        // Bottom Helmet Audio Harness Pass-Through Slot (for 6-Pin J_HELMET at X_mod = 61.05 mm)
        // Positioned at X_mod = 55.0 .. 64.0 mm (completely clear of the 1000 mAh battery!), Y centered
        translate([55.0, (UCS_W - 9.0)/2.0, -0.1])
            cube(size=[9.0, 9.0, UCS_H_BOT + 0.2], center=false);
    }
}

// 3. Monolithic Shore 50A Silicone Keypad (100% Watertight, Zero Holes)
module omm_ucs_silicone_keypad() {
    color([0.15, 0.15, 0.16]) {
        // Base Mat Plate (0.8 mm thick)
        cube(size=[49.0, 23.5, 0.8], center=false);

        // 4 Raised Tactile Key Domes (aligned with SW1..SW4)
        translate([7.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30);  // Power / PTT (SW1)
        translate([19.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Mode: OMM 2.4 / BT / PMR446 / DMR (SW2)
        translate([31.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Vol+ / Ch+ (SW3)
        translate([43.5, 18.5, 0.8]) cylinder(r=3.2, h=1.6, $fn=30); // Vol- / Ch- (SW4)
    }

    // Translucent Silicone RGB-LED Light-Pipe Dome (aligned with D1)
    color("cyan", 0.7) {
        translate([25.5, 22.72, 0.8])
            cylinder(r=1.2, h=1.5, $fn=20);
    }
}

// 4. Complete Universal OMM Tri-Band UCS Module Assembly (Dual-Use: Standalone Helmet & Pod)
module omm_ucs_module_assembly(exploded = false, show_antenna = true) {
    z_bot    = 0.0;
    z_pcb    = exploded ? 20.0 : UCS_H_BOT;
    z_top    = exploded ? 34.0 : UCS_H_BOT;
    z_key    = exploded ? 44.0 : (UCS_H_BOT + UCS_H_TOP - 1.2);
    z_screws = exploded ? -12.0 : 4.5;

    // A. Bottom Shell (PA12 Charcoal, 10.5 mm height enclosing 1000 mAh LiPo + SA818-DMR)
    color([0.22, 0.24, 0.26])
        omm_ucs_bottom_shell();

    // B. Internal Universal OMM Tri-Band PCBA with 1000 mAh LiPo & SA818-DMR
    translate([4.0, 3.0, z_pcb])
        dummy_omm446_ucs_pcb(include_battery = true);

    // C. Top Shell (PA12 Anthracite, 5.5 mm height)
    color([0.18, 0.20, 0.22])
        translate([0, 0, z_top])
            omm_ucs_top_shell();

    // D. Waterproof Silicone Keypad
    translate([9.5, 6.5, z_key])
        omm_ucs_silicone_keypad();

    // E. 4x DIN 912 M2 x 8 mm Stainless Steel Screws
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

    // F. Dual Compact Helmet Stubby Antennas at +X Twin-SMA Ports (Z = 10.5 mm, clearing UCS slot by 1.8 mm)
    if (show_antenna) {
        // Port 1 (Y = 12.5 mm): 38 mm 2.4 GHz OMM Mesh Stubby Antenna
        translate([UCS_L + (exploded ? 12.0 : 0.5), 12.5, UCS_H_BOT]) {
            rotate([0, 90, 0]) {
                color("gold") cylinder(r=3.0, h=3.0, $fn=24);
                color([0.15, 0.16, 0.18]) {
                    translate([0, 0, 3.0])
                        cylinder(r1=3.4, r2=2.2, h=33.0, $fn=24);
                    translate([0, 0, 36.0])
                        sphere(r=2.2, $fn=20);
                }
            }
        }
        // Port 2 (Y = 23.5 mm): 48 mm 446 MHz PMR446 / DMR Tier I Helical Stubby Antenna
        translate([UCS_L + (exploded ? 12.0 : 0.5), 23.5, UCS_H_BOT]) {
            rotate([0, 90, 0]) {
                color("gold") cylinder(r=3.0, h=3.0, $fn=24);
                color([0.15, 0.16, 0.18]) {
                    translate([0, 0, 3.0])
                        cylinder(r1=3.4, r2=2.3, h=43.0, $fn=24);
                    translate([0, 0, 46.0])
                        sphere(r=2.3, $fn=20);
                }
            }
        }
    }
}

// Standalone Preview
omm_ucs_module_assembly(exploded = true);
