// =============================================================================
// OpenMotorBridge - Adventure Rack-Tail Mount ("Rallye-Aero-Balkon" für Reiseenduros)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_rack_tail_mount.scad
// Description: Two-piece automotive-sculpted cantilever luggage rack extension for
//              BMW R1200 / R1250 / R1300 GS/GSA, KTM Adventure & Africa Twin.
//              Key Engineering & Design Highlights:
//              1. Two-Piece Architecture: Lower Base Cradle + Upper Styled Aero-Cowl.
//              2. Dynamic Rising Wedge & Boat-Tail Kammback Silhouette (Zero "Klotz-Optik").
//              3. Double-Bubble Roof with central aero flow channel leading to the Shark-Fin.
//              4. Organically Integrated 45° Shark-Fin (Astabweiser) for +5 dBi 2.4 GHz dipole antenna.
//              5. 68 mm cantilever overhang behind aluminum topcase (100% lid clearance).
//              6. 140° unoccluded zenith sky view for MAX-M10S GNSS & SX1262 LoRa.
//              7. Bionic teardrop underside radar pylon with 36-tooth Hirth coupling
//                 for Garmin Varia mmWave radar at 90..95 cm road clearance.
//              8. 15° Tumblehome side flanks with 45° lower roost/stone-deflector bevel.
//              9. Forward mounting flange for Ø 18 mm rack tube with 2x M6 slotted holes.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;

// --- Parametric Dimensions ---
RTM_POD_X0          = 4.0;   // Pod pocket start along X (mm)
RTM_POD_L           = 136.5; // Internal pocket length for Pod 3 (mm)
RTM_POD_W           = 71.5;  // Internal pocket width (mm)
RTM_POD_H           = 38.5;  // Internal pod height (mm)
RTM_WALL            = 3.5;   // Heavy-duty PA12-CF wall thickness (mm)
RTM_FLOOR           = 4.0;   // Solid bottom floor thickness (mm)

// Parting Line & Height Profile
RTM_SPLIT_Z         = 20.0;  // Continuous horizontal parting line between Base and Cowl (mm)
RTM_TOTAL_H         = 43.0;  // Peak height at top of Cowl (mm)
RTM_BEVEL           = 5.0;   // 45° Lower stone-deflector undercut bevel (mm)

// Cantilever extension & rack mounting flange
RTM_CANTILEVER_X    = 68.0;  // Overhang behind topcase rear wall (mm)
RTM_FLANGE_L        = 56.0;  // Forward mounting flange length (mm)
RTM_FLANGE_W        = 112.0; // Flange width across rack (mm)
RTM_FLANGE_THICK    = 6.5;   // Heavy-duty mounting flange thickness (mm)
RTM_SLOT_SPACING_Y  = 80.0;  // M6 mounting slot lateral center distance (mm)
RTM_TUBE_DIA        = 18.2;  // Luggage rack tube cradle diameter (mm)

// Astabweiser (45° Shark-Fin) on rear edge
FIN_BASE_L          = 36.0;  // Length of deflector fin along X (mm)
FIN_WIDTH           = 16.0;  // Max width of deflector fin along Y (mm)
FIN_HEIGHT          = 30.0;  // Height of deflector wedge above roof in Z (mm)
ANTENNA_BORE_DIA    = 10.5;  // Snap-in groove for +5 dBi dipole antenna (mm)

// Radar hinge on underside
RADAR_DROP_Z        = 22.0;  // Drop below bottom plate for radar hinge (mm)
RADAR_LUG_THICK     = 4.0;   // GoPro dual-lug thickness (mm)
RADAR_LUG_GAP       = 6.2;   // Gap between lugs for standard GoPro tongue (mm)

// 4x M3 Fastening Screws connecting Cowl to Base
RTM_SCREW_X1        = 14.0;
RTM_SCREW_X2        = RTM_POD_X0 + RTM_POD_L - 8.0;
RTM_SCREW_Y         = 36.5;

// =============================================================================
// AERODYNAMIC LOFTING PROFILE ENGINE
// =============================================================================
module rtm_hull_cross_section(x, w_base, w_split, w_roof, z_top, r_fillet=3.0) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=1.0, center=true) {
        hull() {
            // Lower floor chamfered base points
            translate([RTM_BEVEL, -w_base/2.0 + RTM_BEVEL]) circle(r=2.0, $fn=16);
            translate([RTM_BEVEL,  w_base/2.0 - RTM_BEVEL]) circle(r=2.0, $fn=16);
            translate([0, -w_base/2.0 + 2.0*RTM_BEVEL]) square([1.0, 1.0], center=true);
            translate([0,  w_base/2.0 - 2.0*RTM_BEVEL]) square([1.0, 1.0], center=true);

            // Parting line character crease (Lichtkante at exact RTM_SPLIT_Z)
            translate([RTM_SPLIT_Z, -w_split/2.0 + 0.8]) circle(r=0.8, $fn=12);
            translate([RTM_SPLIT_Z,  w_split/2.0 - 0.8]) circle(r=0.8, $fn=12);

            // Upper roof tumblehome corner lobes (Double-Bubble effect)
            translate([z_top - r_fillet, -w_roof/2.0 + r_fillet]) circle(r=r_fillet, $fn=16);
            translate([z_top - r_fillet,  w_roof/2.0 - r_fillet]) circle(r=r_fillet, $fn=16);

            // Center aero roof flow channel
            translate([z_top - r_fillet - 1.4, 0]) circle(r=r_fillet, $fn=16);
        }
    }
}

// Master Continuous Automotive Sculpted Hull
module rtm_master_lofted_hull() {
    // 1. Leading Front Nose Wedge
    hull() {
        rtm_hull_cross_section(-20.0, 68.0, 72.0, 62.0, 26.0, 2.5);
        rtm_hull_cross_section(-6.0,  74.0, 80.0, 70.0, 38.0, 3.0);
    }
    // 2. Front Ramp to Main Pod Cavity
    hull() {
        rtm_hull_cross_section(-6.0,  74.0, 80.0, 70.0, 38.0, 3.0);
        rtm_hull_cross_section(RTM_POD_X0, 76.0, 84.0, 74.0, RTM_TOTAL_H, 3.5);
    }
    // 3. Pod Midsection (Deep aerodynamic waistline)
    hull() {
        rtm_hull_cross_section(RTM_POD_X0, 76.0, 84.0, 74.0, RTM_TOTAL_H, 3.5);
        rtm_hull_cross_section(RTM_POD_X0 + RTM_POD_L/2.0, 78.0, 86.0, 76.0, RTM_TOTAL_H, 3.5);
        rtm_hull_cross_section(RTM_POD_X0 + RTM_POD_L, 76.0, 84.0, 74.0, RTM_TOTAL_H, 3.5);
    }
    // 4. Rear Tail Taper & Ducktail Kammback Spoiler
    hull() {
        rtm_hull_cross_section(RTM_POD_X0 + RTM_POD_L, 76.0, 84.0, 74.0, RTM_TOTAL_H, 3.5);
        rtm_hull_cross_section(RTM_POD_X0 + RTM_POD_L + 14.0, 66.0, 74.0, 64.0, 39.0, 3.0);
        rtm_hull_cross_section(RTM_POD_X0 + RTM_POD_L + 28.0, 50.0, 56.0, 46.0, 32.0, 2.0);
    }
}

// -----------------------------------------------------------------------------
// MODULE 1: ADVENTURE RACK-TAIL MOUNT - BASE CRADLE (UNTERTEIL)
// -----------------------------------------------------------------------------
module adventure_rack_tail_mount_base() {
    difference() {
        union() {
            // 1. Lower Half of Lofted Body (Z <= RTM_SPLIT_Z)
            intersection() {
                rtm_master_lofted_hull();
                translate([-30.0, -RTM_FLANGE_W/2.0, -2.0])
                    cube([RTM_POD_L + 80.0, RTM_FLANGE_W, RTM_SPLIT_Z + 2.0]);
            }

            // 2. Forward Luggage Rack Clamping Flange
            translate([-RTM_FLANGE_L, -RTM_FLANGE_W/2.0, 0]) {
                hull() {
                    translate([8.0, 8.0, 0]) cylinder(r=8.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([RTM_FLANGE_L - 8.0, 8.0, 0]) cylinder(r=8.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([8.0, RTM_FLANGE_W - 8.0, 0]) cylinder(r=8.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([RTM_FLANGE_L - 8.0, RTM_FLANGE_W - 8.0, 0]) cylinder(r=8.0, h=RTM_FLANGE_THICK, $fn=24);
                }
            }

            // 3. Sweeping Sculpted Structural Gussets (Flange to Main Cradle)
            for (side = [-1, 1]) {
                hull() {
                    translate([-38.0, side * (RTM_FLANGE_W/2.0 - 12.0), 0])
                        cube([38.0, 12.0, RTM_FLANGE_THICK]);
                    translate([0, side * (84.0/2.0 - 6.0), 0])
                        cube([26.0, 6.0, RTM_SPLIT_Z - 1.0]);
                }
            }

            // 4. 4x M3 Lid Fastening Bosses
            for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
                for (side = [-1, 1]) {
                    translate([bx, side * (RTM_SCREW_Y - 2.5), 0])
                        cylinder(r=4.2, h=RTM_SPLIT_Z, $fn=20);
                }
            }

            // 5. Bionic Teardrop Underside Radar Mount Pylon
            translate([RTM_POD_X0 + RTM_POD_L/2.0, 0, 0]) {
                // Streamlined Airfoil Pylon Body
                hull() {
                    // Top blend into underbelly
                    translate([-26.0, -14.0, 0]) cube([52.0, 28.0, 2.0]);
                    // Middle transition
                    translate([-16.0, -11.0, -RADAR_DROP_Z + 8.0]) cube([32.0, 22.0, 3.0]);
                    // Lower lug support
                    translate([-9.0, -8.0, -RADAR_DROP_Z + 3.0]) cube([18.0, 16.0, 5.0]);
                }

                // Dual GoPro Lugs (Left & Right)
                for (side = [-1, 1]) {
                    y_lug = side * (RADAR_LUG_GAP/2.0 + RADAR_LUG_THICK/2.0);
                    translate([0, y_lug, -RADAR_DROP_Z]) {
                        rotate([-90, 0, 0])
                            cylinder(r=8.0, h=RADAR_LUG_THICK, center=true, $fn=32);
                        translate([-8.0, -RADAR_LUG_THICK/2.0, 0])
                            cube([16.0, RADAR_LUG_THICK, 8.0]);
                    }
                }
            }
        }

        // --- SUBTRACTIONS (Base) ---

        // A. Pod 3 Main Pocket (Internal clearance 136.5 x 71.5 mm, sits at Z = RTM_FLOOR)
        translate([RTM_POD_X0, -RTM_POD_W/2.0, RTM_FLOOR])
            cube([RTM_POD_L, RTM_POD_W, RTM_SPLIT_Z + 5.0]);

        // B. Forward Flange M6 Slotted Holes (for Rack adjustment)
        for (offset_y = [-RTM_SLOT_SPACING_Y/2.0, RTM_SLOT_SPACING_Y/2.0]) {
            translate([-RTM_FLANGE_L/2.0, offset_y, -1.0]) {
                hull() {
                    translate([-9.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0, $fn=20);
                    translate([ 9.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0, $fn=20);
                }
                // Counterbore for M6 socket head bolt DIN 912
                hull() {
                    translate([-9.0, 0, RTM_FLANGE_THICK - 2.8]) cylinder(r=5.6, h=5.0, $fn=24);
                    translate([ 9.0, 0, RTM_FLANGE_THICK - 2.8]) cylinder(r=5.6, h=5.0, $fn=24);
                }
            }
        }

        // C. Rack Tube V-Groove / Saddle underneath flange (Ø 18.2 mm nest)
        translate([-RTM_FLANGE_L/2.0, -RTM_FLANGE_W/2.0 - 5.0, -0.5])
            rotate([-90, 0, 0])
                cylinder(r=RTM_TUBE_DIA/2.0, h=RTM_FLANGE_W + 10.0, $fn=36);

        // D. 4x M3 Fastening Screw Pilot Holes in Bosses (Ø 2.5 mm for tapping or brass heat-set)
        for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
            for (side = [-1, 1]) {
                translate([bx, side * (RTM_SCREW_Y - 2.5), RTM_SPLIT_Z - 12.0])
                    cylinder(r=1.6, h=14.0, $fn=16);
            }
        }

        // E. Underside GoPro Hinge Gap, M5 Through-Bore & Hirth Rosettes
        translate([RTM_POD_X0 + RTM_POD_L/2.0, 0, 0]) {
            // Gap clearance between lugs
            translate([-11.0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z - 10.0])
                cube([22.0, RADAR_LUG_GAP, RADAR_DROP_Z + 2.0]);

            // M5 through-bore along Y (lateral pivot axis)
            translate([0, 0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=2.7, h=36.0, center=true, $fn=24);

            // M5 hexagonal stop nut pocket on right lug
            translate([0, RADAR_LUG_GAP/2.0 + RADAR_LUG_THICK - 2.5, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=4.6, h=3.2, $fn=6);

            // Form-Fit Radial Hirth Rosettes (10° increments)
            translate([0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([90, 0, 0])
                    gopro_hirth_subtraction_tool();

            translate([0, RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    gopro_hirth_subtraction_tool();
        }

        // F. Concealed Underbelly M8 Cable Routing Passage (100% hidden in tube shadow)
        translate([RTM_POD_X0 + 12.0, 0, -0.5]) {
            hull() {
                cylinder(r=5.5, h=RTM_FLOOR + 1.0, $fn=20);
                translate([-24.0, 0, 0]) cylinder(r=5.5, h=RTM_FLOOR + 1.0, $fn=20);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE 2: ADVENTURE RACK-TAIL MOUNT - DESIGN AERO-COWL (OBERTEIL)
// -----------------------------------------------------------------------------
module adventure_rack_tail_mount_cowl() {
    difference() {
        union() {
            // 1. Upper Half of Lofted Body (Z >= RTM_SPLIT_Z)
            intersection() {
                rtm_master_lofted_hull();
                translate([-30.0, -RTM_FLANGE_W/2.0, RTM_SPLIT_Z])
                    cube([RTM_POD_L + 80.0, RTM_FLANGE_W, RTM_TOTAL_H - RTM_SPLIT_Z + 10.0]);
            }

            // 2. Organically Integrated 45° Shark-Fin (Astabweiser)
            translate([RTM_POD_X0 + RTM_POD_L - 8.0, 0, RTM_SPLIT_Z]) {
                hull() {
                    // Front base transition emerging out of roof valley
                    translate([0, 0, RTM_TOTAL_H - RTM_SPLIT_Z - 4.0])
                        rotate([0, 90, 0]) cylinder(r=FIN_WIDTH/2.0, h=4.0, center=false, $fn=24);
                    // Raked leading apex rising at 45°
                    translate([FIN_BASE_L, 0, RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT - 6.0])
                        rotate([0, 90, 0]) cylinder(r=3.5, h=4.0, center=false, $fn=20);
                    // Lower rear blend into ducktail
                    translate([FIN_BASE_L + 14.0, 0, RTM_TOTAL_H - RTM_SPLIT_Z - 6.0])
                        rotate([0, 90, 0]) cylinder(r=3.0, h=4.0, center=false, $fn=16);
                }
            }
        }

        // --- SUBTRACTIONS (Cowl) ---

        // A. Internal Hollow Pod Headroom Chamber (Roof shell thickness 3.2 mm)
        translate([RTM_POD_X0, -RTM_POD_W/2.0, RTM_SPLIT_Z - 1.0])
            cube([RTM_POD_L, RTM_POD_W, RTM_TOTAL_H - RTM_SPLIT_Z - 3.2]);

        // B. 140° Zenith GNSS Ceramic Antenna Radome Window
        translate([RTM_POD_X0 + RTM_POD_L/2.0 + 8.0, 0, RTM_TOTAL_H - 1.4]) {
            hull() {
                translate([-20.0, -18.0, 0]) cylinder(r=4.0, h=3.0, $fn=16);
                translate([ 20.0, -18.0, 0]) cylinder(r=4.0, h=3.0, $fn=16);
                translate([-20.0,  18.0, 0]) cylinder(r=4.0, h=3.0, $fn=16);
                translate([ 20.0,  18.0, 0]) cylinder(r=4.0, h=3.0, $fn=16);
            }
        }

        // C. Astabweiser Internal Antenna Channel & Snap Slot
        translate([RTM_POD_X0 + RTM_POD_L - 8.0, 0, RTM_SPLIT_Z]) {
            // Diagonal antenna bore inside fin (35° tilt)
            translate([FIN_BASE_L/2.0 + 2.0, 0, (RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0]) {
                    cylinder(r=ANTENNA_BORE_DIA/2.0, h=60.0, center=true, $fn=24);
                    // Lateral snap insertion slit on trailing edge
                    translate([0, -1.6, -26.0])
                        cube([ANTENNA_BORE_DIA, 3.2, 58.0]);
                }

            // Concealed coaxial wire duct into transceiver chamber
            translate([-6.0, 0, 4.0])
                rotate([0, 90, 0])
                    cylinder(r=2.5, h=25.0, $fn=16);
        }

        // D. 4x M3 Torx Counterbore Holes (Fastens Cowl to Base)
        for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
            for (side = [-1, 1]) {
                translate([bx, side * (RTM_SCREW_Y - 2.5), RTM_SPLIT_Z - 2.0]) {
                    cylinder(r=1.7, h=28.0, $fn=16); // M3 through-bore
                    translate([0, 0, RTM_TOTAL_H - RTM_SPLIT_Z - 2.2])
                        cylinder(r=3.5, h=6.0, $fn=20); // Counterbore well
                }
            }
        }

        // E. Lateral Dakar-Style Speed Grooves (Upper Flank Styling)
        for (side = [-1, 1]) {
            translate([RTM_POD_X0 + RTM_POD_L/2.0, side * (75.0/2.0 + 1.0), RTM_TOTAL_H - 5.5]) {
                rotate([0, 90, 0])
                    cylinder(r=1.4, h=RTM_POD_L - 24.0, center=true, $fn=16);
            }
            translate([RTM_POD_X0 + RTM_POD_L/2.0 - 10.0, side * (78.0/2.0 + 1.0), RTM_SPLIT_Z + 4.5]) {
                rotate([0, 90, 0])
                    cylinder(r=1.2, h=RTM_POD_L - 45.0, center=true, $fn=16);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// MASTER MODULE: ADVENTURE RACK-TAIL MOUNT ASSEMBLY & STL RENDERER
// -----------------------------------------------------------------------------
module adventure_rack_tail_mount(part = "assembly") {
    if (part == "base") {
        adventure_rack_tail_mount_base();
    } else if (part == "cowl") {
        adventure_rack_tail_mount_cowl();
    } else {
        // Combined Two-Piece Assembly View with contrasting OEM finishes:
        // Deep textured PA12-CF base + Satin Rallye Grey cowl + Stainless fasteners
        color("#1a1f26", 0.98)
            adventure_rack_tail_mount_base();

        color("#3a4454", 0.98)
            adventure_rack_tail_mount_cowl();

        // 2.4 GHz +5 dBi Dipole Antenna (Accent cyan in fin channel)
        color("#00adb5", 0.95) {
            translate([RTM_POD_X0 + RTM_POD_L - 8.0 + FIN_BASE_L/2.0 + 2.0, 0, (RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0])
                    cylinder(r=4.8, h=52.0, center=true, $fn=20);
        }

        // 4x Stainless Steel V4A Torx Fasteners
        color("silver") {
            for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
                for (side = [-1, 1]) {
                    translate([bx, side * (RTM_SCREW_Y - 2.5), RTM_TOTAL_H - 1.5])
                        cylinder(r=3.2, h=1.5, center=true, $fn=20);
                }
            }
        }
    }
}

// Standalone render
adventure_rack_tail_mount(part = "assembly");
