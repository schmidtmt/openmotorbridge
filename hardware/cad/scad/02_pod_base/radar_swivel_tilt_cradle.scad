// =============================================================================
// OpenMotorBridge - Radar 2.0 Heavy-Duty Center-of-Gravity Swivel Tilt Cradle
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_swivel_tilt_cradle.scad
// Description: Heavy-duty, vibration-proof Actioncam/GoPro-style swivel tilt cradle
//              for the Radar 2.0 (Wheeltec MR20) sealed housing.
//              Features:
//              1. Symmetrical 2x M4 bolted connection (40.0 mm pitch) directly
//                 clamping into the internal DIN 934 M4 captive nuts of the
//                 radar housing. 100% immune to vibration loosening or snapping.
//              2. Central 6.0 mm wide GoPro/Actioncam tongue positioned at the
//                 vertical center of gravity (Z = 0) with horizontal M5 pivot bore.
//              3. Dual 36-tooth radial Hirth rosettes on left & right tongue faces
//                 (10° positive form-fit locking), locking into the female clevis of
//                 `radar_license_plate_bracket.scad` and `radar_center_underfender_mount.scad`.
//              4. Central Ø 34.0 mm clearance well accommodating the male Garmin
//                 quarter-turn bayonet on the housing without interference.
//              5. Dual boss-and-socket shear register pockets around M4 bores
//                 absorbing 100% of lateral shock loads off the screw threads.
//              6. Integrated cable tie strain-relief saddles for the M8 radar harness.
//              7. 100% Soldering-Iron Free (DIN 912 M4 screws + DIN 912 M5 pivot bolt).
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;
use <radar_license_plate_bracket.scad>;
use <../05_accessories/radar_mr20_housing.scad>;

// --- Part Selector for Multi-Part STL Export & Assembly Rendering ---
part = "cradle"; // "cradle", "assembly"

// --- Parametric Dimensions ---
CRADLE_PLATE_W      = 58.0;  // Total adapter plate width in X (mm)
CRADLE_PLATE_H      = 40.0;  // Total adapter plate height in Z (mm, cleanly encloses Ø34mm Garmin well)
CRADLE_PLATE_THICK  = 8.5;   // Base plate thickness in Y (mm)
CRADLE_CORNER_R     = 4.0;   // Corner fillet radius (mm)

REAR_M4_PITCH       = 40.0;  // Symmetrical spacing between M4 mounting screws (mm)
M4_HEAD_RECESS_R    = 4.2;   // Recess radius for DIN 912 M4 socket head screw (mm)
M4_HEAD_RECESS_D    = 4.5;   // Recess depth from back face (mm)
M4_BORE_R           = 2.2;   // M4 through-bore clearance radius (mm)

BOSS_REGISTER_R     = 5.8;   // Pocket radius mating with housing M4 boss (r=5.5mm, mm)
BOSS_REGISTER_D     = 3.2;   // Depth of register pocket on front mating face (mm)

GARMIN_CLEAR_DIA    = 34.0;  // Central clearance diameter for Garmin bayonet (mm)
GARMIN_CLEAR_D      = 6.0;   // Depth of central clearance pocket (mm)

// Actioncam / GoPro Hinge Tongue
TONGUE_WIDTH        = 6.0;   // Standard central blade thickness fitting 7.0mm clevis (mm)
TONGUE_RADIUS       = 8.5;   // Outer radius around M5 pivot axis (mm)
PIVOT_OFFSET_Y      = 12.0;  // Distance from back of plate to M5 pivot axis (mm)
M5_PIVOT_BORE_R     = 2.65;  // M5 pivot bolt clearance radius (mm)

// Helper: 2D Rounded Rectangle in X-Z plane
module rounded_rect_xz(w, h, r) {
    hull() {
        translate([-w/2 + r, 0, -h/2 + r]) sphere(r=0.01);
        translate([ w/2 - r, 0, -h/2 + r]) sphere(r=0.01);
        translate([-w/2 + r, 0,  h/2 - r]) sphere(r=0.01);
        translate([ w/2 - r, 0,  h/2 - r]) sphere(r=0.01);
    }
}

module radar_swivel_tilt_cradle() {
    difference() {
        union() {
            // 1. Main Solid Backing Plate (Front face at Y = 0, rear face at Y = -CRADLE_PLATE_THICK)
            hull() {
                for (sx = [-CRADLE_PLATE_W/2 + CRADLE_CORNER_R, CRADLE_PLATE_W/2 - CRADLE_CORNER_R]) {
                    for (sz = [-CRADLE_PLATE_H/2 + CRADLE_CORNER_R, CRADLE_PLATE_H/2 - CRADLE_CORNER_R]) {
                        translate([sx, 0, sz])
                            rotate([90, 0, 0])
                                cylinder(r=CRADLE_CORNER_R, h=CRADLE_PLATE_THICK, center=false, $fn=32);
                    }
                }
            }

            // 2. Central Actioncam/GoPro Tongue (Protruding rearward along -Y)
            translate([-TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0]) {
                // Pivot barrel
                rotate([0, 90, 0])
                    cylinder(r=TONGUE_RADIUS, h=TONGUE_WIDTH, center=false, $fn=36);

                // Blend neck connecting barrel to back of plate
                translate([0, 0, -TONGUE_RADIUS])
                    cube([TONGUE_WIDTH, PIVOT_OFFSET_Y + 0.1, 2.0 * TONGUE_RADIUS], center=false);
            }

            // 3. Stiffening Gusset Ribs (Triangular gussets stabilizing tongue against lateral road vibrations)
            // Upper and lower triangular stiffeners
            hull() {
                translate([-TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK, -CRADLE_PLATE_H/2 + 2.0])
                    cube([TONGUE_WIDTH, 1.0, CRADLE_PLATE_H - 4.0], center=false);
                translate([-TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y * 0.7, -TONGUE_RADIUS])
                    cube([TONGUE_WIDTH, 1.0, 2.0 * TONGUE_RADIUS], center=false);
            }

            // Lateral wing fillets blending tongue base into plate
            hull() {
                translate([-10.0, -CRADLE_PLATE_THICK - 2.5, -TONGUE_RADIUS])
                    cube([20.0, 2.5, 2.0 * TONGUE_RADIUS], center=false);
                translate([-TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y + 2.0, -TONGUE_RADIUS])
                    cube([TONGUE_WIDTH, 2.0, 2.0 * TONGUE_RADIUS], center=false);
            }

            // 4. Dual Radial Hirth Rosettes on Outer Faces of the Tongue (Formschluss 10° Indexing)
            // Left face (X = -TONGUE_WIDTH/2.0 = -3.0 mm)
            translate([-TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0])
                rotate([0, -90, 0])
                    gopro_hirth_rosette();

            // Right face (X = TONGUE_WIDTH/2.0 = +3.0 mm)
            translate([TONGUE_WIDTH/2.0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0])
                rotate([0, 90, 0])
                    gopro_hirth_rosette();

            // 5. Cable Strain-Relief Saddle on Bottom Lip (Z = -CRADLE_PLATE_H/2)
            translate([-6.0, -CRADLE_PLATE_THICK - 4.0, -CRADLE_PLATE_H/2]) {
                cube([12.0, 4.0, 4.0], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Dual M4 Through-Bores (Pitch: 40.0 mm along X, centered at Z = 0)
        for (dx = [-REAR_M4_PITCH/2.0, REAR_M4_PITCH/2.0]) {
            // M4 Screw shaft hole (through entire plate)
            translate([dx, 1.0, 0])
                rotate([90, 0, 0])
                    cylinder(r=M4_BORE_R, h=CRADLE_PLATE_THICK + 2.0, center=false, $fn=24);

            // DIN 912 / ISO 7380 M4 Screw Head Cylindrical Counterbore (from back face)
            translate([dx, -CRADLE_PLATE_THICK + M4_HEAD_RECESS_D, 0])
                rotate([90, 0, 0])
                    cylinder(r=M4_HEAD_RECESS_R, h=M4_HEAD_RECESS_D + 0.5, center=false, $fn=28);

            // Boss-and-Socket Shear Register Pocket on Front Face (receives housing M4 standoff boss)
            translate([dx, 0.1, 0])
                rotate([90, 0, 0])
                    cylinder(r=BOSS_REGISTER_R, h=BOSS_REGISTER_D + 0.1, center=false, $fn=28);
        }

        // B. Central Garmin Bayonet Clearance Well (Front face at Y = 0)
        translate([0, 0.1, 0])
            rotate([90, 0, 0])
                cylinder(r=GARMIN_CLEAR_DIA/2.0, h=GARMIN_CLEAR_D + 0.1, center=false, $fn=48);

        // C. Horizontal M5 Swivel Pin Bore (Through both Hirth rosettes)
        translate([0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0])
            rotate([0, 90, 0])
                cylinder(r=M5_PIVOT_BORE_R, h=TONGUE_WIDTH + 6.0, center=true, $fn=32);

        // D. Cable Tie Slot in Strain-Relief Saddle (2.5 x 1.4 mm slot for zip-tie)
        translate([-4.0, -CRADLE_PLATE_THICK - 2.5, -CRADLE_PLATE_H/2 - 1.0])
            cube([8.0, 1.6, 6.0], center=false);
    }
}

// 2. Full Assembly Demonstration (Bracket + Swivel Cradle + M5 Hirth Hinge + Bolted Radar Housing)
module radar_tilt_mount_assembly(tilt_angle = -5.0) {
    // A. License Plate Mounting Bracket (Top)
    color([0.22, 0.24, 0.26])
        radar_license_plate_bracket();

    // Pivot is at [0, 12.0, -RADAR_DROP_Z]
    translate([0, 12.0, -48.0]) {
        // M5 Clamping Hardware (DIN 912 M5x20 Screw + DIN 934 M5 Locknut)
        color([0.82, 0.82, 0.85]) {
            // M5 Screw (enters from left at X = -5.5)
            translate([-8.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=2.5, h=18.0, center=false, $fn=24);
            // M5 Socket head
            translate([-8.5, 0, 0])
                rotate([0, -90, 0])
                    cylinder(r=4.2, h=4.0, center=false, $fn=28);
            // M5 Hex nut on right side (recessed in lug)
            translate([7.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=4.5, h=3.5, center=false, $fn=6);
        }

        // B. Tiltable Sub-Assembly (Rotates around horizontal M5 axis)
        rotate([tilt_angle, 0, 0]) {
            // Cradle position: its pivot is at [0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0] = [0, -20.5, 0]
            translate([0, CRADLE_PLATE_THICK + PIVOT_OFFSET_Y, 0]) {
                // Swivel Cradle (MJF PA12 Anthracite)
                color([0.18, 0.40, 0.46])
                    radar_swivel_tilt_cradle();

                // 2x DIN 912 M4 Screws bolting cradle to radar housing
                color([0.82, 0.82, 0.85]) {
                    for (dx = [-REAR_M4_PITCH/2.0, REAR_M4_PITCH/2.0]) {
                        translate([dx, -CRADLE_PLATE_THICK + 2.0, 0])
                            rotate([90, 0, 0]) {
                                cylinder(r=3.5, h=3.8, center=false, $fn=24); // Screw head
                                cylinder(r=2.0, h=14.0, center=false, $fn=20); // Screw shaft
                            }
                    }
                }

                // C. Radar 2.0 Housing Assembly
                // Radar housing rear wall is at Y = -RADAR_HOUSING_D = -34.0 mm
                // Cradle front face is at Y = 0 mm
                translate([0, 34.0, 0]) {
                    radar_mr20_assembly();
                }
            }
        }
    }
}

// Standalone preview and build target
if (part == "assembly") {
    radar_tilt_mount_assembly();
} else {
    radar_swivel_tilt_cradle();
}

