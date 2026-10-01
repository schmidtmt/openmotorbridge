// =============================================================================
// OpenMotorBridge - Universal Saddlebag Lid Dock (Kofferdeckel-Halter)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/saddlebag_lid_dock.scad
// Description: HP MJF PA12 mounting caddy for Universal Pods 1 & 2 inside
//              Harley-Davidson Touring One-Touch saddlebag lids (2014-2024+).
//              Zero-Drill: Picks up factory hinge/tether Torx screws and/or
//              3M VHB landing pads. Features integrated cable routing along
//              the lid tether and an overhead drip guard.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
DOCK_POD_L          = 136.0; // Clearance for 135 mm Pod
DOCK_POD_W          = 71.0;  // Clearance for 70 mm Pod
DOCK_POD_H          = 39.0;  // Clearance for 38 mm Pod
DOCK_WALL           = 3.0;   // Solid MJF PA12 wall thickness
DOCK_CORNER_R       = 4.0;   // Outer verrundung

// Outer cradle envelope
CRADLE_OUTER_L      = DOCK_POD_L + DOCK_WALL;
CRADLE_OUTER_W      = DOCK_POD_W + 2 * DOCK_WALL;
CRADLE_OUTER_H      = 26.0;  // Half-height cradle for quick cartridge access

// Flange dimensions for Harley One-Touch Hinge / Tether Torx screws
FLANGE_EXT_W        = 22.0;  // Extension of side flange towards hinge
FLANGE_THICK        = 4.0;   // Rigid mounting flange thickness
TORX_HOLE_R         = 2.8;   // M5 / Torx T20 clearance hole (Ø 5.6 mm)
TORX_SPACING_X      = 52.0;  // Typical Harley hinge/tether screw distance

module rounded_box(l, w, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=h);
        translate([l-r, r, 0]) cylinder(r=r, h=h);
        translate([r, w-r, 0]) cylinder(r=r, h=h);
        translate([l-r, w-r, 0]) cylinder(r=r, h=h);
    }
}

module saddlebag_lid_dock() {
    difference() {
        union() {
            // 1. Main Cradle Body
            rounded_box(CRADLE_OUTER_L, CRADLE_OUTER_W, CRADLE_OUTER_H, DOCK_CORNER_R);

            // 2. Zero-Drill Torx Mounting Flange (Inboard edge facing hinge)
            translate([20.0, -FLANGE_EXT_W, 0]) {
                hull() {
                    translate([DOCK_CORNER_R, DOCK_CORNER_R, 0]) cylinder(r=DOCK_CORNER_R, h=FLANGE_THICK);
                    translate([TORX_SPACING_X + 25.0 - DOCK_CORNER_R, DOCK_CORNER_R, 0]) cylinder(r=DOCK_CORNER_R, h=FLANGE_THICK);
                    translate([DOCK_CORNER_R, FLANGE_EXT_W + DOCK_WALL, 0]) cylinder(r=DOCK_CORNER_R, h=FLANGE_THICK);
                    translate([TORX_SPACING_X + 25.0 - DOCK_CORNER_R, FLANGE_EXT_W + DOCK_WALL, 0]) cylinder(r=DOCK_CORNER_R, h=FLANGE_THICK);
                }
            }

            // 3. Single-Port Cable Strain-Relief Snout (Dedicated to Port B at Y=46)
            // Completely encloses the slim 2-wire DC tether cable with solid protective roof
            translate([CRADLE_OUTER_L - 4.0, 35.0, 0]) {
                hull() {
                    cube([4.0, 22.0, 28.5]);
                    translate([14.0, 2.0, 0]) cube([1.0, 18.0, 26.5]);
                }
            }

            // 4. Overhead Drip Lip (Tropfkante) over cartridge slot
            translate([0, 0, CRADLE_OUTER_H - 1.0]) {
                hull() {
                    translate([0, 0, 0]) cube([12.0, CRADLE_OUTER_W, 1.0]);
                    translate([-4.0, 0, 3.0]) cube([16.0, CRADLE_OUTER_W, 2.0]);
                }
            }
        }

        // --- SUBTRACTIONS ---

        // A. Pod Main Reception Cavity
        translate([0, DOCK_WALL, DOCK_WALL]) {
            cube([DOCK_POD_L + 5.0, DOCK_POD_W, DOCK_POD_H + 5.0]);
        }

        // B. Cartridge Ejection Window & Viewing Window (Floor cutouts)
        translate([18.0, DOCK_WALL + 10.0, -1.0]) {
            rounded_box(80.0, DOCK_POD_W - 20.0, DOCK_WALL + 2.0, 4.0);
        }

        // C1. Port A (M8): Internal Blind Clearance Pocket (No external through-hole!)
        // Aligned at Dock Y = DOCK_WALL + 27.0 = 30.0 mm, Z = DOCK_WALL + 19.0 = 22.0 mm
        // Provides 3.0 mm clearance for the 2.0 mm protruding M8 collar & screw cap on the pod,
        // while the exterior dock wall remains 100% solid and clean (0 false cables).
        translate([CRADLE_OUTER_L - DOCK_WALL - 0.1, 30.0, 22.0]) {
            rotate([0, 90, 0])
                hull() {
                    for (dy = [-6.5, 6.5]) {
                        for (dz = [-6.5, 6.5]) {
                            translate([dz, dy, 0])
                                cylinder(r=2.0, h=3.0, center=false, $fn=16);
                        }
                    }
                }
        }

        // C2. Port B (Slim USB-C): Primary Saddlebag Tether Cable Exit Bore & Plug-Well
        // Aligned at Dock Y = DOCK_WALL + 43.0 = 46.0 mm, Z = DOCK_WALL + 18.0 = 21.0 mm
        // Tunnel is fully enclosed within the snout housing (solid continuous roof)
        translate([CRADLE_OUTER_L - DOCK_WALL - 0.1, 46.0, 21.0]) {
            rotate([0, 90, 0])
                hull() {
                    for (dy = [-3.0, 3.0]) {
                        for (dz = [-1.5, 1.5]) {
                            translate([dz, dy, 0])
                                cylinder(r=2.2, h=22.0, center=false, $fn=20);
                        }
                    }
                }
        }

        // D. Torx Slotted Holes for Harley Hinge Attachment
        translate([20.0 + 12.0, -FLANGE_EXT_W/2, -1.0]) {
            // Hole 1 (Slotted for tolerance)
            hull() {
                translate([-3.0, 0, 0]) cylinder(r=TORX_HOLE_R, h=FLANGE_THICK + 2.0);
                translate([3.0, 0, 0]) cylinder(r=TORX_HOLE_R, h=FLANGE_THICK + 2.0);
            }
            // Hole 2 (Slotted for tolerance)
            translate([TORX_SPACING_X, 0, 0]) {
                hull() {
                    translate([-3.0, 0, 0]) cylinder(r=TORX_HOLE_R, h=FLANGE_THICK + 2.0);
                    translate([3.0, 0, 0]) cylinder(r=TORX_HOLE_R, h=FLANGE_THICK + 2.0);
                }
            }
        }

        // E. 3M VHB / Dual-Lock Landing Pad Recesses on Bottom
        translate([25.0, DOCK_WALL + 4.0, -0.1]) {
            cube([65.0, 24.0, 0.8]);
        }
        translate([25.0, DOCK_WALL + DOCK_POD_W - 28.0, -0.1]) {
            cube([65.0, 24.0, 0.8]);
        }

        // F. Single Zip-Tie Clamping Tunnel for Port B Tether Cable
        // Cleanly pierces through the flanks of the Port B snout (Y = 32 to 58)
        translate([CRADLE_OUTER_L + 5.0, 32.0, 3.0]) {
            cube([3.5, 28.0, 3.2]);
        }

        // G. 4x Lateral Relief Pockets for Pod Base Strap Hook Lugs (X=25 and X=110)
        // Pod lugs project 3.0 mm laterally. Pockets provide 14.0 x 4.0 x 8.5 mm clearance.
        for (hx = [26.0, 111.0]) {
            // Inboard flank (Y = 0)
            translate([hx - 7.0, DOCK_WALL - 3.8, DOCK_WALL - 0.1])
                cube([14.0, 4.0, 8.5]);
            // Outboard flank (Y = DOCK_WALL + DOCK_POD_W)
            translate([hx - 7.0, DOCK_WALL + DOCK_POD_W - 0.2, DOCK_WALL - 0.1])
                cube([14.0, 4.0, 8.5]);
        }
    }
}

// Render monolithic module
saddlebag_lid_dock();
