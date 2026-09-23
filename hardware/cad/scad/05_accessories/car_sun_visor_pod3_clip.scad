// =============================================================================
// OpenMotorBridge - Universal Car Sun Visor Mount for Satellite Pod 3
// =============================================================================
// File: hardware/cad/scad/05_accessories/car_sun_visor_pod3_clip.scad
// Description: Universal automotive mounting clip for Pod 3 (GNSS, LoRa, 5.9GHz V2X):
//              1. Attaches securely to passenger sun visor in ANY vehicle type
//                 (Station wagon, SUV, hatchback, sports coupe, sedan).
//              2. Bypasses bulky windshield ADAS / camera boxes behind the rear-view mirror.
//              3. Optimal 180° skyward RF view through top windshield zone.
//              4. Tool-free 5-minute cable run directly into the roof headliner seam.
//              5. Non-marring compliant spring clamp jaws (14 .. 22 mm visor thickness).
//              6. Low-profile stealth look (resembles an electronic toll tag / transponder).
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Visor Clamp Dimensions ---
VISOR_THICK_NOM     = 18.0;  // Nominal sun visor thickness (mm)
VISOR_CLAMP_GAP     = 14.5;  // Inner clamping gap at rest for firm friction grip (mm)
VISOR_CLAMP_DEPTH   = 55.0;  // Clamping reach over visor body (mm)
VISOR_CLAMP_WIDTH   = 38.0;  // Clamp tongue width in Y (mm)
CLAMP_SPRING_THICK  = 3.2;   // Spring leaf thickness (PETG / PA12 flexible spring)

// --- Pod 3 Docking Cradle Dimensions ---
CRADLE_L            = POD_OUTER_L + 4.0;  // 139.0 mm
CRADLE_W            = POD_OUTER_W + 3.0;  // 73.0 mm
CRADLE_WALL         = 2.8;                // Sidewall thickness (mm)
CRADLE_LIP_H        = 14.0;               // Side retention lip height (mm)

module sun_visor_spring_tongue() {
    // Upper compliant spring clamp leaf with curved entry lead-in
    translate([0, 0, VISOR_CLAMP_GAP]) {
        hull() {
            // Root hinge section
            translate([0, -VISOR_CLAMP_WIDTH/2.0, 0])
                cube([8.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
            // Main clamping span
            translate([VISOR_CLAMP_DEPTH - 12.0, -VISOR_CLAMP_WIDTH/2.0, -1.0])
                cube([10.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
        }

        // Upturned lead-in lip for easy one-handed push onto visor
        translate([VISOR_CLAMP_DEPTH - 5.0, -VISOR_CLAMP_WIDTH/2.0, 0]) {
            rotate([0, -35, 0])
                cube([16.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
        }

        // Non-marring soft grip friction ribs (3x transverse ridges)
        for (rx = [15.0, 28.0, 42.0]) {
            translate([rx, -VISOR_CLAMP_WIDTH/2.0 + 2.0, -0.8])
                rotate([0, 90, 0])
                    cylinder(r=1.2, h=VISOR_CLAMP_WIDTH - 4.0, center=false, $fn=16);
        }
    }
}

module pod3_docking_cradle() {
    difference() {
        union() {
            // Main cradle floor plate
            translate([-CRADLE_L/2.0, -CRADLE_W/2.0, 0])
                cube([CRADLE_L, CRADLE_W, 3.2], center=false);

            // Left & Right retention sidewalls with Pod 3 strap-lug lock pockets
            for (side = [-CRADLE_W/2.0, CRADLE_W/2.0 - CRADLE_WALL]) {
                translate([-CRADLE_L/2.0, side, 0]) {
                    cube([CRADLE_L, CRADLE_WALL, CRADLE_LIP_H], center=false);
                }
            }

            // Front stop lip
            translate([CRADLE_L/2.0 - CRADLE_WALL, -CRADLE_W/2.0, 0])
                cube([CRADLE_WALL, CRADLE_W, CRADLE_LIP_H], center=false);

            // Rear snap detents (click into Pod 3 housing corner fillets)
            for (dy = [-CRADLE_W/2.0 + 8.0, CRADLE_W/2.0 - 8.0]) {
                translate([-CRADLE_L/2.0 + 3.0, dy, CRADLE_LIP_H - 2.0])
                    sphere(r=2.0, $fn=24);
            }
        }

        // --- SUBTRACTIONS ---

        // 1. Pod 3 Main Bed Recess (135 x 70 mm clearance)
        translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, 1.2])
            cube([POD_OUTER_L + 0.5, POD_OUTER_W + 0.5, CRADLE_LIP_H + 2.0], center=false);

        // 2. Headliner Cable Exit Channel (Directs USB-C cable up towards roof seam)
        translate([-CRADLE_L/2.0 - 1.0, -8.0, 1.0])
            cube([12.0, 16.0, 8.0], center=false);

        // Cable clip grooves along rear spine
        translate([-CRADLE_L/2.0 + 4.0, -2.5, 0.8])
            cube([20.0, 5.0, 6.0], center=false);

        // 3. Weight reduction cutouts in floor plate
        for (dx = [-35.0, 0.0, 35.0]) {
            translate([dx, 0, -1.0])
                cylinder(r=16.0, h=6.0, center=true, $fn=36);
        }
    }
}

module car_sun_visor_pod3_clip() {
    // 1. Lower Pod 3 Docking Bed
    pod3_docking_cradle();

    // 2. Robust Central Clamp Spine & Neck
    translate([-10.0, -VISOR_CLAMP_WIDTH/2.0, -1.0]) {
        difference() {
            cube([VISOR_CLAMP_DEPTH + 10.0, VISOR_CLAMP_WIDTH, VISOR_CLAMP_GAP + CLAMP_SPRING_THICK + 2.0], center=false);
            // Core throat cutout between upper tongue and cradle
            translate([8.0, -1.0, 4.0])
                cube([VISOR_CLAMP_DEPTH + 5.0, VISOR_CLAMP_WIDTH + 2.0, VISOR_CLAMP_GAP - 1.0], center=false);
        }
    }

    // 3. Compliant Visor Spring Tongue
    translate([-2.0, 0, 0])
        sun_visor_spring_tongue();
}

car_sun_visor_pod3_clip();
