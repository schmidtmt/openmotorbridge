// =============================================================================
// OpenMotorBridge - Stealth Center Under-Fender Radar Mount
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_center_underfender_mount.scad
// Description: Ultra-compact, low-profile stealth mounting bracket attaching the
//              Garmin Varia mmWave blind-spot radar centered underneath the rear
//              fender lip or fender strut.
//              Specifically engineered for custom bikes and bobbers with
//              side-mounted license plate brackets:
//              1. Enforces strict centerline mounting (eliminating the lethal
//                 right-side RF radar blind spot caused by tire occlusion).
//              2. Attaches to sprung chassis/fender mass (protecting radar electronics
//                 against 25g unsprung wheel axle shocks).
//              3. Dual mounting options: 3M VHB 5952 heavy-duty bonding pad or
//                 dual M4/M5 countersunk mounting screws.
//              4. Female clevis with 36-tooth radial Hirth rosette (10° pitch indexing)
//                 matching `radar_varia_gopro_lock_dock.scad`.
//              5. Concealed M8 PUR cable guide leading into the inner fender channel.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;

// --- Parametric Dimensions ---
FENDER_CURVE_R      = 210.0; // Typical rear fender underbelly curvature radius (mm)
MOUNT_BASE_L        = 46.0;  // Base plate length in Y (front-to-back, mm)
MOUNT_BASE_W        = 42.0;  // Base plate width in X (transverse, mm)
MOUNT_BASE_THICK    = 4.5;   // Nominal base plate thickness (mm)
RADAR_CLEVIS_DROP_Z = 24.0;  // Vertical drop from fender underside to M5 pivot (mm)
CLEVIS_SLOT_W       = 7.0;   // Female clevis gap for 6.0 mm dock tongue (mm)
LUG_THICK           = 4.0;   // Thickness of left and right clevis prongs (mm)
LUG_OUTER_R         = 8.5;   // Clevis lug outer radius around M5 bore (mm)
SCREW_SPACING_Y     = 26.0;  // Center-to-center distance between M4/M5 mounting holes (mm)

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

            // 2. Central Structural Neck / Gusset Spine
            hull() {
                // Top blend into curved base
                translate([-14.0, -10.0, -MOUNT_BASE_THICK])
                    cube([28.0, 20.0, MOUNT_BASE_THICK], center=false);

                // Lower clevis hub
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -4.0, -RADAR_CLEVIS_DROP_Z])
                    cube([CLEVIS_SLOT_W + 2.0*LUG_THICK, 14.0, 10.0], center=false);
            }

            // 3. Left Clevis Lug (X = -7.5 mm to -3.5 mm)
            translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 8.0], center=false);
            }

            // 4. Right Clevis Lug (X = +3.5 mm to +7.5 mm)
            translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 8.0], center=false);
            }

            // 5. Aerodynamic Lateral Reinforcement Gussets
            hull() {
                translate([-MOUNT_BASE_W/2.0 + 4.0, -2.0, -MOUNT_BASE_THICK])
                    cube([4.0, 4.0, 2.0], center=false);
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -2.0, -RADAR_CLEVIS_DROP_Z + 2.0])
                    cube([2.0, 4.0, 6.0], center=false);
            }
            hull() {
                translate([MOUNT_BASE_W/2.0 - 8.0, -2.0, -MOUNT_BASE_THICK])
                    cube([4.0, 4.0, 2.0], center=false);
                translate([CLEVIS_SLOT_W/2.0 + LUG_THICK - 2.0, -2.0, -RADAR_CLEVIS_DROP_Z + 2.0])
                    cube([2.0, 4.0, 6.0], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Clevis Slot Gap (7.0 mm clearance for 6.0 mm tongue)
        translate([-CLEVIS_SLOT_W/2.0, -LUG_OUTER_R - 2.0, -RADAR_CLEVIS_DROP_Z - LUG_OUTER_R - 2.0])
            cube([CLEVIS_SLOT_W, LUG_OUTER_R * 2.0 + 10.0, RADAR_CLEVIS_DROP_Z + 10.0], center=false);

        // B. Horizontal M5 Swivel Pin Bore
        translate([0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=2.65, h=MOUNT_BASE_W + 10.0, center=true, $fn=36);

        // C. M5 Hex Locknut Pocket on Right Lug (Outer face at X = 7.5 mm)
        translate([CLEVIS_SLOT_W/2.0 + LUG_THICK - 2.2, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=4.6, h=6.0, center=false, $fn=6);

        // D. Dual Hirth Rosettes on Inner Lug Faces (10° positive anti-vibration locking)
        // Left lug inner face (X = -3.5 mm, normal pointing +X)
        translate([-CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, -90, 0])
                gopro_hirth_subtraction_tool();

        // Right lug inner face (X = +3.5 mm, normal pointing -X)
        translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                gopro_hirth_subtraction_tool();

        // E. Dual M4/M5 Countersunk Mounting Screws (along Y centerline)
        for (sy = [-SCREW_SPACING_Y/2.0, SCREW_SPACING_Y/2.0]) {
            translate([0, sy, -RADAR_CLEVIS_DROP_Z - 5.0]) {
                // Shaft hole Ø 4.5 mm
                cylinder(r=2.3, h=RADAR_CLEVIS_DROP_Z + 20.0, center=false, $fn=32);
                // 90° Countersink head recess on underside
                translate([0, 0, RADAR_CLEVIS_DROP_Z - MOUNT_BASE_THICK - 2.0])
                    cylinder(r1=2.3, r2=4.8, h=2.5, center=false, $fn=32);
            }
        }

        // F. Concealed M8 Radar Cable Conduit (Ø 5.5 mm vertical/diagonal channel)
        hull() {
            translate([0, 8.0, -RADAR_CLEVIS_DROP_Z + 4.0])
                sphere(r=2.8, $fn=24);
            translate([0, 16.0, 4.0])
                sphere(r=3.0, $fn=24);
        }

        // G. Cable Entry Slot on Back Face
        translate([-2.5, 6.0, -RADAR_CLEVIS_DROP_Z + 2.0])
            cube([5.0, 12.0, 8.0], center=false);
    }
}

// Standalone preview and build target
radar_center_underfender_mount();
