// =============================================================================
// OpenMotorBridge - Accessories: Under-Perch Tactile Switch Bracket
// =============================================================================
// File: hardware/cad/scad/05_accessories/under_perch_switch_bracket.scad
// Description: Ergonomic under-perch mounting bracket for dedicated IP67 tactile
//              handlebar switch (Front Node Port J3).
//
// ERGONOMIC & MECHANICAL HIGHLIGHTS:
// 1. Zero Handlebar Tubing Footprint: Mounts directly to the lower M4 Torx
//    housing bolt of Harley-Davidson hand controls (2014+ Rushmore/M8 Touring
//    and Softails) or under the M8/M10 mirror stem locknut.
// 2. Anti-Interference Architecture: Leaves the entire upper clutch perch
//    clamp 100% free for Dr. Jekill & Mr. Hyde or KessTech exhaust switches.
// 3. 2-Finger Clutch Lever Coverage: Positions the tactile push-button exactly
//    15 mm below the left turn signal switch in the natural downward sweep
//    of the thumb, allowing index & middle fingers to stay over the clutch lever.
// 4. Integrated Cable Channel & Zip-Tie Strain Relief for 2-wire PUR cable.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Render Selection ---
part = "assembly"; // Options: "assembly", "bracket", "mirror_plate", "cutaway"

// --- Parametric Dimensions ---
BRACKET_WALL        = 2.2;   // Structural wall thickness in PA12-CF (mm)
MOUNT_BOLT_DIA      = 4.3;   // Pass hole for M4 Harley housing screw (mm)
MOUNT_CBORE_DIA     = 8.2;   // Counterbore for M4 Torx bolt head (mm)
MOUNT_CBORE_DEPTH   = 3.0;   // Counterbore depth (mm)
MOUNT_FLANGE_THICK  = 5.0;   // Total mounting flange thickness (mm)
MOUNT_FLANGE_W      = 14.0;  // Flange width (mm)

// Anti-Rotation Shoulder (fits Harley switch housing lower rim radius ~16 mm)
HOUSING_LOCATE_R    = 16.5;  // Locating radius of housing contour (mm)
HOUSING_LIP_H       = 1.5;   // Anti-rotation registration lip height (mm)

// Arm Drop & Angle
ARM_DROP_Z          = 17.5;  // Vertical drop from mounting bolt to switch center (mm)
ARM_OFFSET_Y        = 11.0;  // Inward offset toward thumb (mm)
ARM_SWEEP_X         = 6.0;   // Rearward sweep toward rider (mm)
SWITCH_TILT_ANGLE   = 28.0;  // Upward tilt angle toward rider's thumb pad (degrees)

// Switch Housing Dimensions (Standard M7 / M8 IP67 Push-Button)
SWITCH_THREAD_DIA   = 7.2;   // Clearance hole for M7x0.75 threaded bushing (mm)
SWITCH_NUT_SW       = 10.2;  // Captive hex pocket across flats for M7/M8 nut (mm)
SWITCH_NUT_DEPTH    = 3.0;   // Nut pocket depth (mm)
SWITCH_BEZEL_DIA    = 12.0;  // Recessed bezel pocket outer diameter (mm)
SWITCH_BEZEL_DEPTH  = 2.0;   // Recess depth to prevent accidental brush (mm)
SWITCH_BODY_OD      = 15.0;  // Outer barrel diameter of bracket (mm)
SWITCH_BODY_LEN     = 13.0;  // Barrel axial length (mm)

// Cable Conduit & Strain Relief
CABLE_PASS_DIA      = 3.2;   // Pass hole for Ø 2.5 mm 2-core black PUR wire (mm)
ZIPTIE_SLOT_W       = 2.6;   // Zip-tie slot width (mm)
ZIPTIE_SLOT_H       = 1.4;   // Zip-tie slot height (mm)

// Mirror-Stem Adapter Extension (M8 / M10 through hole)
MIRROR_HOLE_DIA     = 10.3;  // Fits M8 and M10 mirror stems (mm)
MIRROR_PLATE_L      = 32.0;  // Extension plate length (mm)
MIRROR_PLATE_W      = 18.0;  // Extension plate width (mm)
MIRROR_PLATE_THICK  = 2.5;   // 2.5 mm stainless / PA12-CF plate (mm)

// Colors
COLOR_PA12_CF       = [0.20, 0.22, 0.24, 1.0]; // Charcoal matte PA12-CF
COLOR_STAINLESS     = [0.85, 0.86, 0.88, 1.0]; // Polished stainless steel
COLOR_RUBBER        = [0.10, 0.10, 0.10, 1.0]; // Black silicone boot
COLOR_RED_LED       = [0.90, 0.15, 0.15, 0.9]; // Anodized red button cap
COLOR_CABLE         = [0.08, 0.08, 0.08, 1.0]; // Matte PUR cable

// =============================================================================
// MODULE: Main Under-Perch Bracket Body
// =============================================================================
module under_perch_switch_bracket() {
    difference() {
        union() {
            // 1. Upper Mounting Flange with Anti-Rotation Shoulder
            hull() {
                translate([0, 0, 0])
                    cylinder(r=MOUNT_FLANGE_W/2, h=MOUNT_FLANGE_THICK, $fn=36);
                translate([MOUNT_FLANGE_W/2, 0, 0])
                    cylinder(r=3.0, h=MOUNT_FLANGE_THICK, $fn=24);
                translate([0, -MOUNT_FLANGE_W/2, 0])
                    cube([MOUNT_FLANGE_W/2, MOUNT_FLANGE_W/2, MOUNT_FLANGE_THICK]);
            }

            // Anti-rotation locating lip (nests against HD housing)
            translate([0, MOUNT_FLANGE_W/2 - 1.0, MOUNT_FLANGE_THICK])
                difference() {
                    cylinder(r=MOUNT_FLANGE_W/2, h=HOUSING_LIP_H, $fn=36);
                    translate([0, -5, -0.1])
                        cylinder(r=HOUSING_LOCATE_R, h=HOUSING_LIP_H + 0.2, $fn=48);
                }

            // 2. Bionic Connecting Rib (Organic Loft to Switch Barrel)
            hull() {
                // Top root at mounting flange
                translate([1.0, -1.0, 0.5])
                    cube([5.0, 6.0, MOUNT_FLANGE_THICK - 0.5]);

                // Mid transition knuckle
                translate([ARM_SWEEP_X * 0.4, -ARM_OFFSET_Y * 0.6, -ARM_DROP_Z * 0.55])
                    sphere(r=3.5, $fn=24);

                // Bottom anchor strictly at rear of switch barrel
                translate([ARM_SWEEP_X, -ARM_OFFSET_Y, -ARM_DROP_Z])
                    rotate([0, SWITCH_TILT_ANGLE, 0])
                        translate([0, 0, -SWITCH_BODY_LEN * 0.25])
                            cylinder(r=SWITCH_BODY_OD/2 - 0.5, h=SWITCH_BODY_LEN * 0.5, center=true, $fn=36);
            }

            // 3. Switch Barrel Housing
            translate([ARM_SWEEP_X, -ARM_OFFSET_Y, -ARM_DROP_Z]) {
                rotate([0, SWITCH_TILT_ANGLE, 0]) {
                    cylinder(r=SWITCH_BODY_OD/2, h=SWITCH_BODY_LEN, center=true, $fn=36);
                    // Cable exit snout at rear
                    translate([0, 0, -SWITCH_BODY_LEN/2 - 2.5])
                        cylinder(r1=SWITCH_BODY_OD/2 - 2.0, r2=CABLE_PASS_DIA/2 + 2.0, h=3.0, $fn=24);
                }
            }
        }

        // --- SUBTRACTIONS (Holes, Pockets & Cable Channels) ---

        // 1. M4 Mounting Bolt Pass Hole & Counterbore
        translate([0, 0, -0.5])
            cylinder(r=MOUNT_BOLT_DIA/2, h=MOUNT_FLANGE_THICK + 3.0, $fn=36);

        translate([0, 0, MOUNT_FLANGE_THICK - MOUNT_CBORE_DEPTH])
            cylinder(r=MOUNT_CBORE_DIA/2, h=MOUNT_CBORE_DEPTH + 3.0, $fn=36);

        // 2. Switch Barrel Bore & Recessed Bezel
        translate([ARM_SWEEP_X, -ARM_OFFSET_Y, -ARM_DROP_Z]) {
            rotate([0, SWITCH_TILT_ANGLE, 0]) {
                // Central threaded bushing pass hole
                cylinder(r=SWITCH_THREAD_DIA/2, h=SWITCH_BODY_LEN + 4.0, center=true, $fn=36);

                // Recessed Bezel Pocket (Front face)
                translate([0, 0, SWITCH_BODY_LEN/2 - SWITCH_BEZEL_DEPTH + 0.01])
                    cylinder(r=SWITCH_BEZEL_DIA/2, h=SWITCH_BEZEL_DEPTH + 1.0, $fn=36);

                // Captive Hex Nut Pocket (Rear internal face)
                translate([0, 0, -SWITCH_BODY_LEN/2 + 1.0])
                    rotate([0, 0, 30])
                        cylinder(r=SWITCH_NUT_SW / (2 * cos(30)), h=SWITCH_NUT_DEPTH + 1.0, $fn=6);

                // Cable passage out the rear snout
                translate([0, 0, -SWITCH_BODY_LEN/2 - 4.5])
                    cylinder(r=CABLE_PASS_DIA/2, h=6.0, $fn=24);

                // Side Zip-Tie Notch for cable strain relief
                translate([0, 0, -SWITCH_BODY_LEN/2 - 1.0])
                    rotate([90, 0, 0])
                        cylinder(r=ZIPTIE_SLOT_H/2, h=SWITCH_BODY_OD + 2.0, center=true, $fn=16);
            }
        }
    }
}

// =============================================================================
// MODULE: Optional Mirror-Stem Extension Plate (M8/M10 to Under-Perch M4)
// =============================================================================
module mirror_stem_adapter_plate() {
    difference() {
        hull() {
            // Mirror stem eyelet
            translate([0, 0, 0])
                cylinder(r=MIRROR_PLATE_W/2, h=MIRROR_PLATE_THICK, $fn=36);
            // Extension tab to M4 bracket
            translate([MIRROR_PLATE_L - MIRROR_PLATE_W/2, 0, 0])
                cylinder(r=MOUNT_FLANGE_W/2, h=MIRROR_PLATE_THICK, $fn=36);
        }

        // Mirror stem clearance hole (Ø 10.3 mm for M8/M10)
        translate([0, 0, -0.5])
            cylinder(r=MIRROR_HOLE_DIA/2, h=MIRROR_PLATE_THICK + 1.0, $fn=36);

        // M4 threaded/clearance hole to anchor the under-perch bracket
        translate([MIRROR_PLATE_L - MIRROR_PLATE_W/2, 0, -0.5])
            cylinder(r=MOUNT_BOLT_DIA/2, h=MIRROR_PLATE_THICK + 1.0, $fn=36);
    }
}

// =============================================================================
// DUMMY HARDWARE (Button, Screw & Cable for Master Assembly Previews)
// =============================================================================
module dummy_ip67_pushbutton() {
    translate([ARM_SWEEP_X, -ARM_OFFSET_Y, -ARM_DROP_Z]) {
        rotate([0, SWITCH_TILT_ANGLE, 0]) {
            // Metallic Bushing
            color(COLOR_STAINLESS)
                cylinder(r=SWITCH_THREAD_DIA/2 - 0.1, h=10.0, center=true, $fn=24);

            // Red Anodized Tactile Cap
            color(COLOR_RED_LED)
                translate([0, 0, SWITCH_BODY_LEN/2 - 0.5])
                    cylinder(r=4.2, h=2.5, $fn=32);

            // Silicone Water Seal Ring
            color(COLOR_RUBBER)
                translate([0, 0, SWITCH_BODY_LEN/2 - 1.2])
                    cylinder(r=5.5, h=1.0, $fn=32);

            // Cable tail exiting rear
            color(COLOR_CABLE)
                translate([0, 0, -SWITCH_BODY_LEN/2 - 12.0])
                    cylinder(r=CABLE_PASS_DIA/2 - 0.2, h=16.0, $fn=16);
        }
    }
}

module dummy_m4_torx_screw() {
    color(COLOR_STAINLESS) {
        translate([0, 0, MOUNT_FLANGE_THICK - 2.5])
            cylinder(r=3.8, h=2.6, $fn=24); // Low-profile head
        translate([0, 0, -8.0])
            cylinder(r=1.9, h=10.0, $fn=24); // M4 thread shaft
    }
}

// =============================================================================
// TOP-LEVEL RENDER CONTROLLER
// =============================================================================
if (part == "bracket") {
    // Clean oriented printable STL (flat mounting flange down on print bed)
    rotate([180, 0, 0])
        translate([0, 0, -MOUNT_FLANGE_THICK])
            under_perch_switch_bracket();
} else if (part == "mirror_plate") {
    mirror_stem_adapter_plate();
} else if (part == "assembly") {
    // Complete visual assembly for studio renders and inspection
    color(COLOR_PA12_CF)
        under_perch_switch_bracket();
    dummy_ip67_pushbutton();
    dummy_m4_torx_screw();
} else if (part == "cutaway") {
    // 50% Section cutaway for engineering verification
    difference() {
        union() {
            color(COLOR_PA12_CF)
                under_perch_switch_bracket();
            dummy_ip67_pushbutton();
            dummy_m4_torx_screw();
        }
        translate([0, -50, -50])
            cube([100, 100, 100]);
    }
} else {
    // Default fallback
    under_perch_switch_bracket();
}
