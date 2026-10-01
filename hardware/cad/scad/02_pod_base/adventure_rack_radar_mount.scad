// =============================================================================
// OpenMotorBridge - Adventure Bike Rear Luggage Rack Radar Mount
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_rack_radar_mount.scad
// Description: Heavy-duty, vibration-proof tube-clamp radar mount for adventure
//              and touring enduros (BMW R1200 / R1250 / R1300 GS/GSA, KTM 890/1290,
//              Honda Africa Twin, Yamaha Ténéré 700).
//              Key Engineering Highlights:
//              1. Direct clamping to Ø 18.0 mm rear luggage rack cross-tubes.
//              2. Two-piece architecture: Lower Base Mount + Upper Clamp Cap.
//              3. 100% Soldering-Iron Free: 2x DIN 912 M5 clamp screws tightening
//                 into captive DIN 934 M5 hex nut pockets. Bottom-accessible screw
//                 heads allow adjustment without removing topcase baseplates.
//              4. Drop truss neck (Z_DROP = 46.0 mm) ensuring full pitch clearance
//                 (±18°) for the Radar 2.0 housing (~180g) below the luggage rack.
//              5. Clevis with dual 36-tooth radial Hirth rosettes (10° positive
//                 anti-vibration locking), mating seamlessly with the interchangeable
//                 `radar_swivel_tilt_cradle.scad`.
//              6. Integrated 45° offroad roost / stone-deflector wedge (Schmutz-
//                 und Steinschlag-Spoiler) shielding the joint and bottom M8 gland.
//              7. Concealed cable routing channel in the tube shadow.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;
use <radar_swivel_tilt_cradle.scad>;
use <../05_accessories/radar_mr20_housing.scad>;

// --- Part Selector for Multi-Part STL Export & Assembly Rendering ---
part = "mount"; // "mount", "clamp_cap", "assembly"

// --- Parametric Dimensions ---
RACK_TUBE_DIA       = 18.2;  // Standard luggage rack tube cradle diameter (mm)
RACK_CLAMP_W        = 34.0;  // Clamp width along tube axis X (mm)
RACK_CLAMP_L        = 46.0;  // Clamp depth across Y (mm)
RACK_CLAMP_BASE_H   = 16.0;  // Height of clamp block on lower base (mm)
RACK_CLAMP_CAP_H    = 10.0;  // Height of upper clamp cap (mm)

CLAMP_SCREW_PITCH_Y = 32.0;  // Pitch between forward and rear M5 clamp screws (mm)
CLAMP_SCREW_DIA     = 5.3;   // M5 screw through-hole clearance diameter (mm)
M5_HEAD_BORE_R      = 5.0;   // M5 socket head counterbore radius (DIN 912, mm)
M5_HEAD_BORE_D      = 6.0;   // M5 socket head counterbore depth (mm)
M5_NUT_POCKET_R     = 4.6;   // DIN 934 M5 captive nut radius across corners (mm)
M5_NUT_POCKET_D     = 4.5;   // DIN 934 M5 nut pocket depth (mm)

// Clevis Drop & Geometry (identical to radar_center_underfender_mount.scad)
RADAR_CLEVIS_DROP_Z = 46.0;  // Vertical drop from tube center to pivot axis (mm)
CLEVIS_SLOT_W       = 7.0;   // Female slot clearance for 6.0 mm tongue (mm)
LUG_THICK           = 4.0;   // Clevis lug thickness (mm)
LUG_OUTER_R         = 8.5;   // Clevis outer lug radius (mm)

// Roost & Stone Deflector Wedge
DEFLECTOR_W         = 34.0;  // Stone deflector width across tire spray path (mm)
DEFLECTOR_ANGLE     = 45.0;  // Raked deflector angle (degrees)

// -----------------------------------------------------------------------------
// MODULE 1: ADVENTURE RACK RADAR MOUNT (LOWER BASE TRUSS)
// -----------------------------------------------------------------------------
module adventure_rack_radar_mount() {
    difference() {
        union() {
            // 1. Semi-cylindrical Tube Cradle Base Block
            // Tube centerline is at [0, 0, 0], lower block extends from Z = 0 down to Z = -RACK_CLAMP_BASE_H
            hull() {
                translate([-RACK_CLAMP_W/2.0, -RACK_CLAMP_L/2.0, -RACK_CLAMP_BASE_H])
                    cube([RACK_CLAMP_W, RACK_CLAMP_L, 4.0]);
                translate([-RACK_CLAMP_W/2.0, -RACK_CLAMP_L/2.0 + 2.0, -2.0])
                    cube([RACK_CLAMP_W, RACK_CLAMP_L - 4.0, 2.0]);
            }

            // 2. High-Strength Drop Truss Neck (Transitions from clamp base to clevis)
            hull() {
                // Top blend under tube saddle
                translate([-RACK_CLAMP_W/2.0 + 2.0, -14.0, -RACK_CLAMP_BASE_H])
                    cube([RACK_CLAMP_W - 4.0, 28.0, 2.0]);
                // Mid transition
                translate([-11.0, -11.0, -RADAR_CLEVIS_DROP_Z + 12.0])
                    cube([22.0, 22.0, 4.0]);
                // Lower clevis hub
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -LUG_OUTER_R, -RADAR_CLEVIS_DROP_Z])
                    cube([CLEVIS_SLOT_W + 2.0 * LUG_THICK, 2.0 * LUG_OUTER_R, 6.0]);
            }

            // 3. Integrated 45° Offroad Roost & Stone Deflector Wedge (Facing forward -Y)
            // Fends off high-velocity gravel and tire roost flung upward by the rear tire
            hull() {
                translate([-DEFLECTOR_W/2.0, -RACK_CLAMP_L/2.0, -RACK_CLAMP_BASE_H])
                    cube([DEFLECTOR_W, 3.5, 2.0]);
                translate([-DEFLECTOR_W/2.0, -16.0, -RADAR_CLEVIS_DROP_Z - 2.0])
                    cube([DEFLECTOR_W, 3.5, 6.0]);
                translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, -LUG_OUTER_R - 2.0, -RADAR_CLEVIS_DROP_Z - 6.0])
                    cube([CLEVIS_SLOT_W + 2.0 * LUG_THICK, 2.5, 6.0]);
            }

            // 4. Dual Clevis Lugs (Left & Right)
            // Left Lug (X = -CLEVIS_SLOT_W/2 - LUG_THICK to -CLEVIS_SLOT_W/2)
            translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 10.0], center=false);
            }

            // Right Lug (X = CLEVIS_SLOT_W/2 to CLEVIS_SLOT_W/2 + LUG_THICK)
            translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z]) {
                rotate([0, 90, 0])
                    cylinder(r=LUG_OUTER_R, h=LUG_THICK, center=false, $fn=36);
                translate([0, -LUG_OUTER_R, 0])
                    cube([LUG_THICK, LUG_OUTER_R * 2.0, 10.0], center=false);
            }

            // 5. Lateral Gusset Stiffening Ribs
            for (side = [-1, 1]) {
                hull() {
                    translate([side * (RACK_CLAMP_W/2.0 - 4.0) - 2.0, -8.0, -RACK_CLAMP_BASE_H])
                        cube([4.0, 16.0, 2.0]);
                    translate([side * (CLEVIS_SLOT_W/2.0 + LUG_THICK) - (side > 0 ? 3.0 : 1.0), -LUG_OUTER_R, -RADAR_CLEVIS_DROP_Z + 2.0])
                        cube([4.0, LUG_OUTER_R * 2.0, 6.0]);
                }
            }
        }

        // --- SUBTRACTIONS (Base Mount) ---

        // A. Horizontal Ø 18.2 mm Rack Tube Saddle (along X axis)
        translate([-RACK_CLAMP_W/2.0 - 5.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=RACK_TUBE_DIA/2.0, h=RACK_CLAMP_W + 10.0, center=false, $fn=64);

        // B. 2x M5 Clamping Screw Holes (Forward & Rear of tube at Y = ±CLAMP_SCREW_PITCH_Y/2)
        for (sy = [-CLAMP_SCREW_PITCH_Y/2.0, CLAMP_SCREW_PITCH_Y/2.0]) {
            // Clearance shaft hole Ø 5.3 mm
            translate([0, sy, -RACK_CLAMP_BASE_H - 5.0])
                cylinder(r=CLAMP_SCREW_DIA/2.0, h=RACK_CLAMP_BASE_H + 10.0, center=false, $fn=32);

            // DIN 912 M5 socket head counterbore on underside (accessible from below bike!)
            translate([0, sy, -RACK_CLAMP_BASE_H - 0.5])
                cylinder(r=M5_HEAD_BORE_R, h=M5_HEAD_BORE_D + 1.0, center=false, $fn=32);
        }

        // C. Central Clevis Slot Gap (7.0 mm clearance for 6.0 mm tongue)
        translate([-CLEVIS_SLOT_W/2.0, -LUG_OUTER_R - 2.0, -RADAR_CLEVIS_DROP_Z - LUG_OUTER_R - 4.0])
            cube([CLEVIS_SLOT_W, LUG_OUTER_R * 2.0 + 16.0, RADAR_CLEVIS_DROP_Z + 10.0], center=false);

        // D. Horizontal M5 Swivel Pin Bore along X
        translate([0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=2.65, h=RACK_CLAMP_W + 10.0, center=true, $fn=36);

        // E. M5 Hex Nut Pocket on Right Lug (DIN 934 M5, 100% Soldering-Iron Free)
        translate([CLEVIS_SLOT_W/2.0 + LUG_THICK - 2.8, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=M5_NUT_POCKET_R, h=5.0, center=false, $fn=6);

        // E2. M5 Screw Head Cylindrical Counterbore on Left Lug
        translate([-CLEVIS_SLOT_W/2.0 - LUG_THICK + 3.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, -90, 0])
                cylinder(r=5.0, h=4.0, center=false, $fn=32);

        // F. Dual Hirth Rosettes on Inner Lug Faces (Formschluss 10° Anti-Vibration Locking)
        // Left lug inner face (X = -CLEVIS_SLOT_W/2 = -3.5 mm)
        translate([-CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, -90, 0])
                gopro_hirth_subtraction_tool();

        // Right lug inner face (X = +CLEVIS_SLOT_W/2 = +3.5 mm)
        translate([CLEVIS_SLOT_W/2.0, 0, -RADAR_CLEVIS_DROP_Z])
            rotate([0, 90, 0])
                gopro_hirth_subtraction_tool();

        // G. Concealed M8 Radar Cable Conduit (Ø 6.0 mm channel routing behind tube into frame)
        hull() {
            translate([0, 10.0, -RADAR_CLEVIS_DROP_Z + 6.0])
                sphere(r=3.0, $fn=24);
            translate([0, 14.0, -RACK_CLAMP_BASE_H + 4.0])
                sphere(r=3.2, $fn=24);
            translate([0, 12.0, 2.0])
                sphere(r=3.5, $fn=24);
        }

        // H. Cable Entry Slot on Back Face (leads cable from cradle up into channel)
        translate([-3.0, 8.0, -RADAR_CLEVIS_DROP_Z + 2.0])
            cube([6.0, 14.0, 12.0], center=false);
    }
}

// -----------------------------------------------------------------------------
// MODULE 2: ADVENTURE RACK RADAR CLAMP CAP (UPPER HALF)
// -----------------------------------------------------------------------------
module adventure_rack_radar_clamp_cap() {
    difference() {
        // Solid cap block
        hull() {
            translate([-RACK_CLAMP_W/2.0, -RACK_CLAMP_L/2.0, 0])
                cube([RACK_CLAMP_W, RACK_CLAMP_L, 2.0]);
            translate([-RACK_CLAMP_W/2.0 + 2.0, -RACK_CLAMP_L/2.0 + 2.0, RACK_CLAMP_CAP_H - 2.0])
                cube([RACK_CLAMP_W - 4.0, RACK_CLAMP_L - 4.0, 2.0]);
        }

        // Subtraction A: Semi-cylindrical Tube Saddle (along X)
        translate([-RACK_CLAMP_W/2.0 - 5.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=RACK_TUBE_DIA/2.0, h=RACK_CLAMP_W + 10.0, center=false, $fn=64);

        // Subtraction B: 2x M5 Clamp Screw Holes + Captive DIN 934 Nut Pockets on Top Face
        for (sy = [-CLAMP_SCREW_PITCH_Y/2.0, CLAMP_SCREW_PITCH_Y/2.0]) {
            // Clearance shaft hole Ø 5.3 mm
            translate([0, sy, -2.0])
                cylinder(r=CLAMP_SCREW_DIA/2.0, h=RACK_CLAMP_CAP_H + 4.0, center=false, $fn=32);

            // DIN 934 M5 captive nut pocket on top face
            translate([0, sy, RACK_CLAMP_CAP_H - M5_NUT_POCKET_D + 0.1])
                cylinder(r=M5_NUT_POCKET_R, h=M5_NUT_POCKET_D + 1.0, center=false, $fn=6);
        }

        // Subtraction C: Chamfered outer edges for smooth snag-free finish
        for (side = [-1, 1]) {
            translate([0, side * (RACK_CLAMP_L/2.0), RACK_CLAMP_CAP_H])
                rotate([45, 0, 0])
                    cube([RACK_CLAMP_W + 10.0, 4.0, 4.0], center=true);
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE 3: FULL ADVENTURE RACK RADAR ASSEMBLY DEMONSTRATION
// -----------------------------------------------------------------------------
module adventure_rack_radar_assembly(tilt_angle = 0.0) {
    // A. Stainless Steel Luggage Rack Tube Mockup (Ø 18.0 mm)
    color([0.80, 0.82, 0.85, 0.6]) {
        rotate([0, 90, 0])
            cylinder(r=18.0/2.0, h=120.0, center=true, $fn=48);
    }

    // B. Upper Clamp Cap (MJF PA12 Anthracite)
    color([0.22, 0.24, 0.26])
        adventure_rack_radar_clamp_cap();

    // C. 2x M5 Stainless Clamping Screws & DIN 934 Nuts
    color([0.85, 0.85, 0.88]) {
        for (sy = [-CLAMP_SCREW_PITCH_Y/2.0, CLAMP_SCREW_PITCH_Y/2.0]) {
            // M5 DIN 912 Socket Head Screw (inserted from below)
            translate([0, sy, -RACK_CLAMP_BASE_H])
                cylinder(r=2.5, h=RACK_CLAMP_BASE_H + RACK_CLAMP_CAP_H - 2.0, center=false, $fn=24);
            translate([0, sy, -RACK_CLAMP_BASE_H])
                rotate([180, 0, 0])
                    cylinder(r=4.2, h=4.5, center=false, $fn=28);
            // M5 DIN 934 Hex Nut in top pocket
            translate([0, sy, RACK_CLAMP_CAP_H - 3.5])
                cylinder(r=4.5, h=3.5, center=false, $fn=6);
        }
    }

    // D. Lower Base Mount (MJF PA12 Anthracite)
    color([0.20, 0.22, 0.24])
        adventure_rack_radar_mount();

    // Pivot axis is at [0, 0, -RADAR_CLEVIS_DROP_Z]
    translate([0, 0, -RADAR_CLEVIS_DROP_Z]) {
        // M5 Clamping Hardware (DIN 912 M5x25 + DIN 934 M5 nut)
        color([0.85, 0.85, 0.88]) {
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

        // E. Tiltable Sub-Assembly (Rotates around horizontal M5 axis)
        rotate([tilt_angle, 0, 0]) {
            // Cradle pivot is at [0, -20.5, 0] relative to cradle plate
            translate([0, 20.5, 0]) {
                color([0.18, 0.40, 0.46])
                    radar_swivel_tilt_cradle();

                // 2x M4 Screws bolting cradle to radar housing
                color([0.85, 0.85, 0.88]) {
                    for (dx = [-20.0, 20.0]) {
                        translate([dx, -6.5, 0])
                            rotate([90, 0, 0]) {
                                cylinder(r=3.5, h=3.8, center=false, $fn=24);
                                cylinder(r=2.0, h=14.0, center=false, $fn=20);
                            }
                    }
                }

                // F. Radar 2.0 Housing Assembly (Wheeltec MR20 Sealed Radar)
                translate([0, 34.0, 0]) {
                    radar_mr20_assembly();
                }
            }
        }
    }
}

// Standalone preview and build target
if (part == "assembly") {
    adventure_rack_radar_assembly();
} else if (part == "clamp_cap") {
    adventure_rack_radar_clamp_cap();
} else {
    adventure_rack_radar_mount();
}
