// =============================================================================
// OpenMotorBridge - Road Glide ST Through-Fairing Inductive Cam Dock (Qi IPT)
// =============================================================================
// File: hardware/cad/scad/05_accessories/road_glide_inductive_cam_dock.scad
// Description: Zero-drill, zero-external-wire continuous power docking system
//              for action cams (Insta360 X3/X4, GoPro) on Harley Sharknose fairings:
//              1. Inner TX Cradle (mounted under outer fairing deck behind headlamp)
//                 holds 15W Qi transmitter coil pressed against inner ABS surface.
//              2. Outer Cam Dock with 3M Dual Lock SJ3550 base, internal Qi RX coil
//                 (TI BQ51013B 5V/2A), 30mm ultra-short USB-C pigtail to camera,
//                 and universal 3-prong action-cam / 1/4"-20 tripod mounting head.
//              3. Pure magnetic inductive coupling through 2.5 - 3.0 mm ABS deck.
//                 100% factory paint preserved, 100% weatherproof, zero holes!
// =============================================================================

include <../00_common/parameters.scad>;

// --- Fairing & Electromagnetic Parameters ---
FAIRING_ABS_THICK   = 2.8;   // Nominal Road Glide ST outer fairing deck thickness (mm)
QI_COIL_DIA         = 50.0;  // Standard 15W Qi inductive ferrite coil diameter (mm)
QI_COIL_THICK       = 2.2;   // Coil + ferrite shield backing thickness (mm)
QI_RX_PCB_L         = 28.0;  // Rectifier / step-down converter board length (mm)
QI_RX_PCB_W         = 15.0;  // Rectifier board width (mm)

// --- Outer Dock Mechanical Parameters ---
DOCK_OUTER_L        = 64.0;  // Longitudinal length of aerodynamic dock base (mm)
DOCK_OUTER_W        = 56.0;  // Transverse width of dock base (mm)
DOCK_OUTER_H        = 18.0;  // Overall height from fairing deck to camera pivot (mm)
DUAL_LOCK_RECESS_D  = 2.8;   // Recess depth for 3M Dual Lock SJ3550 interlocking tape (mm)

// 1. Inner TX Coil Cradle (Glued inside fairing deck behind headlamp)
module road_glide_inner_qi_tx_cradle() {
    difference() {
        union() {
            // Mounting flange plate with rounded corners
            hull() {
                for (dx = [-28.0, 28.0]) {
                    for (dy = [-28.0, 28.0]) {
                        translate([dx, dy, 0])
                            cylinder(r=4.0, h=4.5, center=false, $fn=24);
                    }
                }
            }
            // Cable strain relief snout
            translate([-34.0, -6.0, 0])
                cube([12.0, 12.0, 5.0], center=false);
        }

        // Circular pocket for 15W Qi TX coil + ferrite disc
        translate([0, 0, 1.0])
            cylinder(r=QI_COIL_DIA/2.0 + 0.5, h=QI_COIL_THICK + 2.0, center=false, $fn=48);

        // Center thermal breather / alignment port
        cylinder(r=6.0, h=10.0, center=true, $fn=24);

        // Power wire routing groove to Front-Node Port 1 (PD 12V/9V)
        translate([-36.0, -2.5, 1.2])
            cube([25.0, 5.0, 3.5], center=false);

        // Perimeter 3M VHB bonding adhesive tape channels (1.0 mm deep)
        difference() {
            translate([0, 0, -0.1])
                cylinder(r=30.0, h=1.2, center=false, $fn=48);
            translate([0, 0, -0.2])
                cylinder(r=26.5, h=1.5, center=false, $fn=48);
        }
    }
}

// 2. Outer Quick-Release Inductive Action Cam Dock
module road_glide_outer_qi_cam_dock() {
    difference() {
        union() {
            // Aerodynamic teardrop / rounded wedge outer housing
            hull() {
                // Front aerodynamic nose
                translate([DOCK_OUTER_L/2.0 - 6.0, 0, 0])
                    cylinder(r=10.0, h=7.0, center=false, $fn=32);
                // Rear body
                translate([-DOCK_OUTER_L/2.0 + 12.0, -DOCK_OUTER_W/2.0 + 12.0, 0])
                    cylinder(r=8.0, h=8.5, center=false, $fn=24);
                translate([-DOCK_OUTER_L/2.0 + 12.0,  DOCK_OUTER_W/2.0 - 12.0, 0])
                    cylinder(r=8.0, h=8.5, center=false, $fn=24);
                // Upper camera mounting tower
                translate([0, 0, DOCK_OUTER_H - 4.0])
                    cylinder(r=12.0, h=4.0, center=false, $fn=36);
            }

            // Universal Action Camera 3-Prong Mounting Clevis
            translate([0, 0, DOCK_OUTER_H]) {
                for (prong_y = [-4.5, 1.5]) {
                    translate([-7.5, prong_y, 0]) {
                        difference() {
                            hull() {
                                cube([15.0, 3.0, 7.5], center=false);
                                translate([7.5, 1.5, 7.5])
                                    rotate([90, 0, 0])
                                        cylinder(r=7.5, h=3.0, center=true, $fn=32);
                            }
                            // M5 Bolt Pivot Bore
                            translate([7.5, 1.5, 7.5])
                                rotate([90, 0, 0])
                                    cylinder(r=2.6, h=6.0, center=true, $fn=24);
                        }
                    }
                }
                // Center prong
                translate([-7.5, -1.5, 0]) {
                    difference() {
                        hull() {
                            cube([15.0, 3.0, 7.5], center=false);
                            translate([7.5, 1.5, 7.5])
                                rotate([90, 0, 0])
                                    cylinder(r=7.5, h=3.0, center=true, $fn=32);
                        }
                        translate([7.5, 1.5, 7.5])
                            rotate([90, 0, 0])
                                cylinder(r=2.6, h=6.0, center=true, $fn=24);
                    }
                }
                // M5 Acorn Nut Captive Hex Pocket (on left flank)
                translate([0, -8.0, 7.5])
                    rotate([90, 0, 0])
                        cylinder(r=NUT_M5_SW/cos(30)/2, h=4.0, center=true, $fn=6);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Bottom 3M Dual Lock SJ3550 Interlocking Tape Recess (ensures flush mount)
        translate([0, 0, -0.1]) {
            hull() {
                for (dx = [-DOCK_OUTER_L/2.0 + 14.0, DOCK_OUTER_L/2.0 - 16.0]) {
                    for (dy = [-DOCK_OUTER_W/2.0 + 14.0, DOCK_OUTER_W/2.0 - 14.0]) {
                        translate([dx, dy, 0])
                            cylinder(r=5.0, h=DUAL_LOCK_RECESS_D + 0.1, center=false, $fn=24);
                    }
                }
            }
        }

        // B. Internal Qi Receiver Coil Cavity (centered right above Dual Lock floor)
        translate([0, 0, DUAL_LOCK_RECESS_D + 0.8])
            cylinder(r=QI_COIL_DIA/2.0 + 0.5, h=QI_COIL_THICK + 0.5, center=false, $fn=48);

        // C. Internal Rectifier & 5V/2A Step-Down PCB Pocket (TI BQ51013B)
        translate([-8.0, 0, DUAL_LOCK_RECESS_D + QI_COIL_THICK + 1.2])
            cube([QI_RX_PCB_L + 2.0, QI_RX_PCB_W + 1.0, 4.5], center=true);

        // D. Ultra-Short 30mm USB-C Cable Exit Port (Angled upward towards camera port)
        translate([16.0, 0, 6.0]) {
            rotate([0, -25, 0]) {
                cylinder(r=2.5, h=20.0, center=false, $fn=20); // Ø 5mm cable passage
                translate([0, 0, 10.0])
                    cylinder(r=4.0, h=6.0, center=false, $fn=24); // TPU strain relief boot recess
            }
        }

        // E. Standard 1/4"-20 Threaded Brass Bushing Option (Alternative to GoPro prongs)
        translate([0, 0, 2.0])
            cylinder(r=3.2, h=10.0, center=false, $fn=24);
    }
}

// 3. Full Through-Fairing Coupled Assembly (Visualization)
module road_glide_through_fairing_assembly() {
    // A. Outer Action Cam Dock (Molded Matte Black PA12)
    color("darkslategray", 0.95)
        translate([0, 0, FAIRING_ABS_THICK/2.0 + DUAL_LOCK_RECESS_D])
            road_glide_outer_qi_cam_dock();

    // B. Harley Road Glide Sharknose Fairing Deck (Representation in Amber ABS)
    color("darkorange", 0.35)
        translate([0, 0, 0])
            cube([120.0, 100.0, FAIRING_ABS_THICK], center=true);

    // C. Inner Qi 15W TX Coil Cradle (Mounted on underside)
    color("dimgray", 0.9)
        translate([0, 0, -FAIRING_ABS_THICK/2.0])
            rotate([180, 0, 0])
                road_glide_inner_qi_tx_cradle();
}

road_glide_through_fairing_assembly();
