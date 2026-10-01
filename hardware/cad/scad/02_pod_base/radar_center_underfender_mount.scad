// =============================================================================
// OpenMotorBridge - Stealth Center Under-Fender Radar Mount
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_center_underfender_mount.scad
// Description: Ultra-compact, low-profile stealth mounting bracket attaching the
//              mmWave blind-spot radar centered underneath the rear fender lip
//              or fender strut.
//              Specifically engineered for custom bikes and bobbers with
//              side-mounted license plate brackets:
//              1. Enforces strict centerline mounting (eliminating the lethal
//                 right-side RF radar blind spot caused by tire occlusion).
//              2. Attaches to sprung chassis/fender mass (protecting radar electronics
//                 against 25g unsprung wheel axle shocks).
//              3. Actioncam-style heavy-duty swivel tilt connection:
//                 Slots into `radar_swivel_tilt_cradle.scad` which is firmly bolted
//                 via 2x M4 screws into internal DIN 934 nuts in the radar housing.
//              4. Female clevis (7.0 mm slot) with dual 36-tooth radial Hirth rosettes
//                 (10° pitch indexing) and recessed M5 screw/nut seats.
//              5. Monolithic forward-facing Tire Roost Deflector Shield:
//                 Shields the radar housing, hinge, and bottom M8 cable gland from
//                 high-speed water spray, mud, and gravel hurled by the rear tire.
//              6. 46.0 mm vertical drop providing full tilt clearance for 71 mm Radar 2.0.
//              7. 100% Soldering-Iron Free.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;
use <radar_swivel_tilt_cradle.scad>;
use <../05_accessories/radar_mr20_housing.scad>;

// --- Part Selector for Multi-Part STL Export & Assembly Rendering ---
part = "mount"; // "mount", "assembly"

// --- Parametric Dimensions ---
FENDER_CURVE_R      = 210.0; // Typical rear fender underbelly curvature radius (mm)
MOUNT_BASE_L        = 52.0;  // Base plate length in Y (front-to-back, mm)
MOUNT_BASE_W        = 46.0;  // Base plate width in X (transverse, mm)
MOUNT_BASE_THICK    = 4.5;   // Nominal base plate thickness (mm)
RADAR_CLEVIS_DROP_Z = 46.0;  // Vertical drop providing clearance for 71mm Radar 2.0 housing (mm)
CLEVIS_SLOT_W       = 7.0;   // Female clevis gap for 6.0 mm cradle tongue (mm)
LUG_THICK           = 5.0;   // Thickness of left and right clevis prongs (mm)
LUG_OUTER_R         = 9.0;   // Clevis lug outer radius around M5 bore (mm)
SCREW_SPACING_Y     = 28.0;  // Center-to-center distance between M4/M5 mounting holes (mm)

module radar_center_underfender_mount() {
    difference() {
        union() {
            // 1. Curved Base Flange (Hugging the inner or lower fender radius)
            intersection() {
                // Outer bounding block
                translate([-MOUNT_BASE_W/2.0, -MOUNT_BASE_L/2.0, -MOUNT_BASE_THICK])
                    cube([MOUNT_BASE_W, MOUNT_BASE_L, MOUNT_BASE_THICK + 6.0], center=false);

                // Curved cylinder matching fender contour
                translate([0, 0, -FENDER_CURVE_R])
                    rotate([0, 90, 0])
                        cylinder(r=FENDER_CURVE_R, h=MOUNT_BASE_W + 10.0, center=true, $fn=120);
            }

            // 2. Central Structural Neck / Gusset Spine (Heavy-duty continuous column)
            hull() {
                // Top blend into curved base
                translate([-16.0, -12.0, -MOUNT_BASE_THICK])
                    cube([32.0, 24.0, MOUNT_BASE_THICK], center=false);

                // Lower clevis hub
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -6.0, -RADAR_CLEVIS_DROP_Z])
                    cube([CLEVIS_SLOT_W + 2.0*LUG_THICK, 16.0, 12.0], center=false);
            }

            // 3. Monolithic Forward Tire-Roost Deflector Shield (Spritzwasser- & Steinschlagschild)
            // Extends downward on the -Y side (facing the rotating rear tire)
            hull() {
                translate([-MOUNT_BASE_W/2.0 + 3.0, -MOUNT_BASE_L/2.0 + 2.0, -MOUNT_BASE_THICK])
                    cube([MOUNT_BASE_W - 6.0, 4.0, 2.0], center=false);
                translate([-MOUNT_BASE_W/2.0 + 5.0, -14.0, -RADAR_CLEVIS_DROP_Z - 10.0])
                    cube([MOUNT_BASE_W - 10.0, 3.5, 6.0], center=false);
            }

            // 4. Left Clevis Lug (with recessed M5 screw head counterbore)
            translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 10.0], center=false);
            }

            // 5. Right Clevis Lug (with recessed DIN 934 M5 captive nut pocket)
            translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 10.0], center=false);
            }

            // 6. Stiffening Gussets (Lateral triangular structural ribs)
            hull() {
                translate([-MOUNT_BASE_W/2.0 + 4.0, 0, -MOUNT_BASE_THICK])
                    cube([4.0, 6.0, 2.0], center=false);
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -2.0, -RADAR_CLEVIS_DROP_Z + 2.0])
                    cube([2.0, 4.0, 8.0], center=false);
            }
            hull() {
                translate([MOUNT_BASE_W/2.0 - 8.0, 0, -MOUNT_BASE_THICK])
                    cube([4.0, 6.0, 2.0], center=false);
                translate([CLEVIS_SLOT_W/2.0 + LUG_THICK - 2.0, -2.0, -RADAR_CLEVIS_DROP_Z + 2.0])
                    cube([2.0, 4.0, 8.0], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Clevis Slot Gap (7.0 mm clearance for 6.0 mm tongue)
        translate([-CLEVIS_SLOT_W/2.0, -LUG_OUTER_R - 2.0, -RADAR_CLEVIS_DROP_Z - LUG_OUTER_R - 4.0])
            cube([CLEVIS_SLOT_W, LUG_OUTER_R * 2.0 + 16.0, RADAR_CLEVIS_DROP_Z + 10.0], center=false);

        // B. Horizontal M5 Swivel Pin Bore
        translate([0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=2.65, h=MOUNT_BASE_W + 10.0, center=true, $fn=36);

        // C. M5 Hex Nut Pocket on Right Lug (DIN 934 M5, 100% Soldering-Iron Free)
        translate([CLEVIS_SLOT_W/2.0 + LUG_THICK - 2.8, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=4.6, h=5.0, center=false, $fn=6);

        // C2. M5 Screw Head Cylindrical Counterbore on Left Lug (Recessed flush fit)
        translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK + 3.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, -90, 0])
                cylinder(r=5.0, h=4.0, center=false, $fn=32);

        // D. Dual Hirth Rosettes on Inner Lug Faces (Formschluss 10° Anti-Vibration Locking)
        // Left lug inner face (X = -CLEVIS_SLOT_W/2.0 = -3.5 mm)
        translate([-CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, -90, 0])
                gopro_hirth_subtraction_tool();

        // Right lug inner face (X = +CLEVIS_SLOT_W/2.0 = +3.5 mm)
        translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                gopro_hirth_subtraction_tool();

        // E. Dual M4/M5 Countersunk Mounting Screws (along Y centerline)
        for (sy = [-SCREW_SPACING_Y/2.0, SCREW_SPACING_Y/2.0]) {
            translate([0, sy, -RADAR_CLEVIS_DROP_Z - 10.0]) {
                // Shaft hole Ø 4.5 mm
                cylinder(r=2.3, h=RADAR_CLEVIS_DROP_Z + 25.0, center=false, $fn=32);
                // 90° Countersink head recess on underside
                translate([0, 0, RADAR_CLEVIS_DROP_Z - MOUNT_BASE_THICK - 2.0])
                    cylinder(r1=2.3, r2=4.8, h=2.5, center=false, $fn=32);
            }
        }

        // F. Concealed M8 Radar Cable Conduit (Ø 5.5 mm vertical/diagonal channel)
        hull() {
            translate([0, 8.0, -RADAR_CLEVIS_DROP_Z + 6.0])
                sphere(r=3.0, $fn=24);
            translate([0, 18.0, 4.0])
                sphere(r=3.2, $fn=24);
        }

        // G. Cable Entry Slot on Back Face (leads cable to underfender clip channel)
        translate([-3.0, 8.0, -RADAR_CLEVIS_DROP_Z + 2.0])
            cube([6.0, 14.0, 10.0], center=false);
    }
}

// 2. Full Assembly Demonstration (Fender Section + Underfender Mount + Swivel Cradle + Radar 2.0 Housing)
module radar_underfender_mount_assembly(tilt_angle = 0.0) {
    // A. Rear Fender Sheet Metal Mock-up (R = 210 mm, cropped arc segment)
    color([0.75, 0.77, 0.80, 0.45]) {
        intersection() {
            translate([0, 0, -FENDER_CURVE_R])
                rotate([0, 90, 0])
                    difference() {
                        cylinder(r=FENDER_CURVE_R + 1.5, h=70.0, center=true, $fn=120);
                        cylinder(r=FENDER_CURVE_R, h=72.0, center=true, $fn=120);
                    }
            translate([0, -8.0, 5.0])
                cube([80.0, 64.0, 30.0], center=true);
        }
    }

    // B. Stealth Underfender Mount (MJF PA12 Anthracite)
    color([0.22, 0.24, 0.26])
        radar_center_underfender_mount();

    // Pivot is at [0, 0, -RADAR_CLEVIS_DROP_Z]
    translate([0, 0, -RADAR_CLEVIS_DROP_Z]) {
        // M5 Clamping Hardware (DIN 912 M5x25 + DIN 934 M5 nut)
        color([0.82, 0.82, 0.85]) {
            translate([-8.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=2.5, h=20.0, center=false, $fn=24);
            translate([-8.5, 0, 0])
                rotate([0, -90, 0])
                    cylinder(r=4.2, h=4.0, center=false, $fn=28);
            translate([8.0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(r=4.5, h=3.5, center=false, $fn=6);
        }

        // C. Tiltable Sub-Assembly (Rotates around horizontal M5 axis)
        rotate([tilt_angle, 0, 0]) {
            // Position cradle: cradle pivot is at [0, -CRADLE_PLATE_THICK - PIVOT_OFFSET_Y, 0] = [0, -20.5, 0]
            translate([0, 20.5, 0]) {
                color([0.18, 0.40, 0.46])
                    radar_swivel_tilt_cradle();

                // 2x M4 Screws bolting cradle to radar housing
                color([0.82, 0.82, 0.85]) {
                    for (dx = [-20.0, 20.0]) {
                        translate([dx, -6.5, 0])
                            rotate([90, 0, 0]) {
                                cylinder(r=3.5, h=3.8, center=false, $fn=24);
                                cylinder(r=2.0, h=14.0, center=false, $fn=20);
                            }
                    }
                }

                // D. Radar 2.0 Housing Assembly
                translate([0, 34.0, 0]) {
                    radar_mr20_assembly();
                }
            }
        }
    }
}

// Standalone preview and build target
if (part == "assembly") {
    radar_underfender_mount_assembly();
} else {
    radar_center_underfender_mount();
}
