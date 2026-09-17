// =============================================================================
// OpenMotorBridge - Adventure Rack-Tail Mount ("Rallye-Aero-Balkon" für Reiseenduros)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_rack_tail_mount.scad
// Description: Two-piece automotive-sculpted cantilever luggage rack extension for
//              BMW R1200 / R1250 / R1300 GS/GSA, KTM Adventure & Africa Twin.
//              Features:
//              1. Two-Piece Architecture: Lower Base Cradle + Upper Styled Aero-Cowl.
//              2. 68 mm cantilever overhang behind aluminum topcase (100% lid clearance).
//              3. 140° unoccluded zenith sky view for MAX-M10S GNSS & SX1262 LoRa.
//              4. Integrated 45° Shark-Fin (Astabweiser) for +5 dBi 2.4 GHz dipole antenna.
//              5. Bionic teardrop underside radar pylon with 36-tooth Hirth coupling
//                 for Garmin Varia mmWave radar at 90..95 cm road clearance.
//              6. Faceted 3D Tumblehome (15° inward draft) & 45° lower stone-deflector bevel.
//              7. Forward mounting flange for Ø 18 mm rack tube with 2x M6 slotted holes.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;

// --- Parametric Dimensions ---
RTM_POD_L           = 136.5; // Internal pocket length for Pod 3 (mm)
RTM_POD_W           = 71.5;  // Internal pocket width (mm)
RTM_POD_H           = 38.5;  // Pod height (mm)
RTM_WALL            = 3.5;   // Heavy-duty PA12-CF wall thickness (mm)
RTM_FLOOR           = 4.0;   // Solid bottom floor thickness (mm)

// Parting Line & Height Profile
RTM_SPLIT_Z         = 20.0;  // Height of horizontal parting line between Base and Cowl (mm)
RTM_TOTAL_H         = 43.0;  // Total height including Aero Cowl (mm)
RTM_CREASE_W        = 82.0;  // Maximum outer width at parting line (mm)
RTM_ROOF_W          = 74.0;  // Tapered roof width at top (15° Tumblehome) (mm)
RTM_BASE_W          = 76.0;  // Width at bottom floor (mm)
RTM_BEVEL           = 5.0;   // 45° Lower stone-deflector undercut bevel (mm)

// Cantilever extension & rack mounting flange
RTM_CANTILEVER_X    = 68.0;  // Overhang behind topcase rear wall (mm)
RTM_FLANGE_L        = 55.0;  // Forward mounting flange length (mm)
RTM_FLANGE_W        = 110.0; // Flange width across rack (mm)
RTM_FLANGE_THICK    = 6.5;   // Heavy-duty mounting flange thickness (mm)
RTM_SLOT_SPACING_Y  = 80.0;  // M6 mounting slot lateral center distance (mm)
RTM_TUBE_DIA        = 18.2;  // Luggage rack tube cradle diameter (mm)

// Astabweiser (45° Shark-Fin) on rear edge
FIN_BASE_L          = 34.0;  // Length of deflector fin along X (mm)
FIN_WIDTH           = 22.0;  // Width of deflector fin along Y (mm)
FIN_HEIGHT          = 32.0;  // Height of deflector wedge above roof in Z (mm)
ANTENNA_BORE_DIA    = 10.5;  // Snap-in groove for +5 dBi dipole antenna (mm)

// Radar hinge on underside
RADAR_DROP_Z        = 22.0;  // Drop below bottom plate for radar hinge (mm)
RADAR_LUG_THICK     = 4.0;   // GoPro dual-lug thickness (mm)
RADAR_LUG_GAP       = 6.2;   // Gap between lugs for standard GoPro tongue (mm)

// 4x M3 Fastening Screws connecting Cowl to Base
RTM_SCREW_X1        = 12.0;
RTM_SCREW_X2        = RTM_POD_L - 10.0;
RTM_SCREW_Y         = 36.2;

// Lofted Profile Slice for Main Body
module rtm_hull_cross_section(x, w_base, w_split, w_roof, z_split, z_top, r_fillet=3.0) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=1.0, center=true) {
        hull() {
            // Lower floor chamfered base
            translate([RTM_BEVEL, -w_base/2.0 + RTM_BEVEL]) circle(r=2.0, $fn=16);
            translate([RTM_BEVEL,  w_base/2.0 - RTM_BEVEL]) circle(r=2.0, $fn=16);
            translate([0, -w_base/2.0 + 2.0*RTM_BEVEL]) square([1.0, 1.0], center=true);
            translate([0,  w_base/2.0 - 2.0*RTM_BEVEL]) square([1.0, 1.0], center=true);

            // Parting line character crease
            translate([z_split, -w_split/2.0 + 1.0]) circle(r=1.0, $fn=12);
            translate([z_split,  w_split/2.0 - 1.0]) circle(r=1.0, $fn=12);

            // Tumblehome upper roof corners
            translate([z_top - r_fillet, -w_roof/2.0 + r_fillet]) circle(r=r_fillet, $fn=16);
            translate([z_top - r_fillet,  w_roof/2.0 - r_fillet]) circle(r=r_fillet, $fn=16);
        }
    }
}

// Master Continuous Lofted Exoskeleton
module rtm_master_lofted_hull() {
    hull() {
        // Front bulkhead (meets topcase back wall)
        rtm_hull_cross_section(-4.0, RTM_BASE_W, RTM_CREASE_W, RTM_ROOF_W, RTM_SPLIT_Z, RTM_TOTAL_H - 3.0, 3.0);
        // Mid-front transition
        rtm_hull_cross_section(20.0, RTM_BASE_W, RTM_CREASE_W, RTM_ROOF_W, RTM_SPLIT_Z, RTM_TOTAL_H, 3.0);
    }
    hull() {
        // Mid-front transition
        rtm_hull_cross_section(20.0, RTM_BASE_W, RTM_CREASE_W, RTM_ROOF_W, RTM_SPLIT_Z, RTM_TOTAL_H, 3.0);
        // Pod center section
        rtm_hull_cross_section(RTM_POD_L/2.0, RTM_BASE_W + 2.0, RTM_CREASE_W + 2.0, RTM_ROOF_W + 1.0, RTM_SPLIT_Z, RTM_TOTAL_H, 3.0);
        // Pod rear section
        rtm_hull_cross_section(RTM_POD_L - 5.0, RTM_BASE_W, RTM_CREASE_W, RTM_ROOF_W, RTM_SPLIT_Z, RTM_TOTAL_H, 3.0);
    }
    hull() {
        // Pod rear section
        rtm_hull_cross_section(RTM_POD_L - 5.0, RTM_BASE_W, RTM_CREASE_W, RTM_ROOF_W, RTM_SPLIT_Z, RTM_TOTAL_H, 3.0);
        // Rear tail extension
        rtm_hull_cross_section(RTM_POD_L + 6.0, RTM_BASE_W - 4.0, RTM_CREASE_W - 4.0, RTM_ROOF_W - 4.0, RTM_SPLIT_Z, RTM_TOTAL_H - 1.0, 3.0);
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
                translate([-10.0, -RTM_FLANGE_W/2.0, -1.0])
                    cube([RTM_POD_L + 25.0, RTM_FLANGE_W, RTM_SPLIT_Z + 1.0]);
            }

            // 2. Forward Luggage Rack Clamping Flange
            translate([-RTM_FLANGE_L, -RTM_FLANGE_W/2.0, 0]) {
                hull() {
                    translate([5.0, 5.0, 0]) cylinder(r=5.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([RTM_FLANGE_L - 5.0, 5.0, 0]) cylinder(r=5.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([5.0, RTM_FLANGE_W - 5.0, 0]) cylinder(r=5.0, h=RTM_FLANGE_THICK, $fn=24);
                    translate([RTM_FLANGE_L - 5.0, RTM_FLANGE_W - 5.0, 0]) cylinder(r=5.0, h=RTM_FLANGE_THICK, $fn=24);
                }
            }

            // 3. Sweeping Triangular Stiffening Gussets (Flange to Cradle)
            for (side = [-1, 1]) {
                hull() {
                    translate([-28.0, side * (RTM_FLANGE_W/2.0 - 12.0), 0])
                        cube([28.0, 10.0, RTM_FLANGE_THICK]);
                    translate([4.0, side * (RTM_CREASE_W/2.0 - 6.0), 0])
                        cube([24.0, 6.0, RTM_SPLIT_Z]);
                }
            }

            // 4. 4x M3 Lid Fastening Bosses
            for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
                for (side = [-1, 1]) {
                    translate([bx, side * (RTM_SCREW_Y - 2.5), 0])
                        cylinder(r=4.0, h=RTM_SPLIT_Z, $fn=20);
                }
            }

            // 5. Bionic Teardrop Underside Radar Mount Pylon
            translate([RTM_POD_L/2.0, 0, 0]) {
                // Streamlined Airfoil Pylon Body
                hull() {
                    // Top blend into underbelly
                    translate([-22.0, -13.0, 0]) cube([44.0, 26.0, 2.0]);
                    // Middle transition
                    translate([-14.0, -11.0, -RADAR_DROP_Z + 7.0]) cube([28.0, 22.0, 3.0]);
                    // Lower lug support
                    translate([-8.0, -8.0, -RADAR_DROP_Z + 3.0]) cube([16.0, 16.0, 4.0]);
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
        translate([0, -RTM_POD_W/2.0, RTM_FLOOR])
            cube([RTM_POD_L, RTM_POD_W, RTM_SPLIT_Z + 5.0]);

        // Front pass-through opening for M8 cable
        translate([-12.0, -RTM_POD_W/2.0 + 8.0, RTM_FLOOR])
            cube([16.0, RTM_POD_W - 16.0, RTM_SPLIT_Z + 5.0]);

        // B. Forward Flange M6 Slotted Holes (for Rack adjustment)
        for (offset_y = [-RTM_SLOT_SPACING_Y/2.0, RTM_SLOT_SPACING_Y/2.0]) {
            translate([-RTM_FLANGE_L/2.0, offset_y, -1.0]) {
                hull() {
                    translate([-8.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0, $fn=20);
                    translate([ 8.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0, $fn=20);
                }
                // Counterbore for M6 socket head bolt DIN 912
                hull() {
                    translate([-8.0, 0, RTM_FLANGE_THICK - 2.5]) cylinder(r=5.5, h=4.0, $fn=24);
                    translate([ 8.0, 0, RTM_FLANGE_THICK - 2.5]) cylinder(r=5.5, h=4.0, $fn=24);
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
                translate([bx, side * (RTM_SCREW_Y - 2.5), RTM_SPLIT_Z - 10.0])
                    cylinder(r=1.6, h=12.0, $fn=16);
            }
        }

        // E. Underside GoPro Hinge Gap, M5 Through-Bore & Hirth Rosettes
        translate([RTM_POD_L/2.0, 0, 0]) {
            // Gap clearance between lugs
            translate([-10.0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z - 10.0])
                cube([20.0, RADAR_LUG_GAP, RADAR_DROP_Z + 2.0]);

            // M5 through-bore along Y (lateral pivot axis)
            translate([0, 0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=2.7, h=36.0, center=true, $fn=24);

            // M5 hexagonal stop nut pocket on right lug
            translate([0, RADAR_LUG_GAP/2.0 + RADAR_LUG_THICK - 2.4, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=4.6, h=3.0, $fn=6);

            // Form-Fit Radial Hirth Rosettes (10° increments)
            translate([0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([90, 0, 0])
                    gopro_hirth_subtraction_tool();

            translate([0, RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    gopro_hirth_subtraction_tool();
        }

        // F. Concealed M8 Cable Channel on Underbelly
        translate([15.0, 0, -0.5]) {
            hull() {
                cylinder(r=5.0, h=RTM_FLOOR + 1.0, $fn=20);
                translate([-35.0, 0, 0]) cylinder(r=5.0, h=RTM_FLOOR + 1.0, $fn=20);
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
                translate([-10.0, -RTM_FLANGE_W/2.0, RTM_SPLIT_Z])
                    cube([RTM_POD_L + 25.0, RTM_FLANGE_W, RTM_TOTAL_H - RTM_SPLIT_Z + 5.0]);
            }

            // 2. Integrated 45° Shark-Fin (Astabweiser for 2.4 GHz Dipole Antenna)
            translate([RTM_POD_L - 5.0, -FIN_WIDTH/2.0, RTM_SPLIT_Z]) {
                hull() {
                    // Base transition flowing from cowl roof
                    translate([0, 0, 0]) cube([4.0, FIN_WIDTH, RTM_TOTAL_H - RTM_SPLIT_Z]);
                    // Angled deflector crest sweeping up at 45°
                    translate([FIN_BASE_L, 0, 0])
                        cube([4.0, FIN_WIDTH, RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT]);
                }
            }
        }

        // --- SUBTRACTIONS (Cowl) ---

        // A. Internal Hollow Pod Headroom Chamber
        translate([0, -RTM_POD_W/2.0, RTM_SPLIT_Z - 1.0])
            cube([RTM_POD_L, RTM_POD_W, RTM_TOTAL_H - RTM_SPLIT_Z - 2.5]);

        // Front slide opening matching base
        translate([-12.0, -RTM_POD_W/2.0 + 8.0, RTM_SPLIT_Z - 1.0])
            cube([16.0, RTM_POD_W - 16.0, RTM_TOTAL_H - RTM_SPLIT_Z + 5.0]);

        // B. 140° Zenith GNSS Ceramic Antenna Radome Window
        // Thin low-dielectric dome (1.5 mm wall) directly over u-blox MAX-M10S patch
        translate([RTM_POD_L/2.0 + 10.0, 0, RTM_TOTAL_H - 1.5]) {
            hull() {
                translate([-18.0, -18.0, 0]) cylinder(r=3.0, h=3.0, $fn=16);
                translate([ 18.0, -18.0, 0]) cylinder(r=3.0, h=3.0, $fn=16);
                translate([-18.0,  18.0, 0]) cylinder(r=3.0, h=3.0, $fn=16);
                translate([ 18.0,  18.0, 0]) cylinder(r=3.0, h=3.0, $fn=16);
            }
        }

        // C. Astabweiser Internal Antenna Channel & Snap Slot
        translate([RTM_POD_L - 5.0, 0, RTM_SPLIT_Z]) {
            // Diagonal antenna bore inside fin (35° tilt)
            translate([FIN_BASE_L/2.0, 0, (RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0]) {
                    cylinder(r=ANTENNA_BORE_DIA/2.0, h=55.0, center=true, $fn=24);
                    // Lateral snap insertion slit
                    translate([0, -1.5, -25.0])
                        cube([ANTENNA_BORE_DIA, 3.0, 55.0]);
                }

            // Hidden coaxial passage into Pod 3 chamber
            translate([-8.0, 0, 4.0])
                rotate([0, 90, 0])
                    cylinder(r=2.5, h=25.0, $fn=16);
        }

        // D. 4x M3 Torx Counterbore Holes (for fastening cowl to base)
        for (bx = [RTM_SCREW_X1, RTM_SCREW_X2]) {
            for (side = [-1, 1]) {
                translate([bx, side * (RTM_SCREW_Y - 2.5), RTM_SPLIT_Z - 2.0]) {
                    cylinder(r=1.7, h=25.0, $fn=16); // M3 through-bore
                    translate([0, 0, RTM_TOTAL_H - RTM_SPLIT_Z - 2.5])
                        cylinder(r=3.4, h=6.0, $fn=20); // Counterbore
                }
            }
        }

        // E. Lateral Dakar-Style Speed Grooves (Upper Flank Styling)
        for (side = [-1, 1]) {
            translate([RTM_POD_L/2.0, side * (RTM_ROOF_W/2.0 + 1.0), RTM_TOTAL_H - 6.0]) {
                rotate([0, 90, 0])
                    cylinder(r=1.2, h=RTM_POD_L - 30.0, center=true, $fn=12);
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
        // Combined Two-Piece Assembly View with contrasting finishes
        color("#1c222b", 0.96)
            adventure_rack_tail_mount_base();
        color("#2b3442", 0.98)
            adventure_rack_tail_mount_cowl();
    }
}

// Standalone render
adventure_rack_tail_mount(part = "assembly");
