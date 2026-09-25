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
//              5. Non-marring compliant spring clamp jaws (14 .. 22 mm visor thickness)
//                 located strictly on the exterior underside of the cradle.
//              6. Completely unobstructed upper docking cradle cavity for Pod 3.
//              7. Low-profile stealth look (resembles an electronic toll tag / transponder).
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Visor Clamp Dimensions ---
VISOR_THICK_NOM     = 18.0;  // Nominal sun visor thickness (mm)
VISOR_CLAMP_GAP     = 14.5;  // Inner clamping gap at rest for firm friction grip (mm)
VISOR_CLAMP_DEPTH   = 58.0;  // Clamping reach over visor body (mm)
VISOR_CLAMP_WIDTH   = 42.0;  // Clamp tongue width in Y (mm)
CLAMP_SPRING_THICK  = 3.2;   // Spring leaf thickness (PETG / PA12 flexible spring)

// --- Pod 3 Docking Cradle Dimensions ---
CRADLE_L            = POD_OUTER_L + 4.0;  // 139.0 mm
CRADLE_W            = POD_OUTER_W + 3.0;  // 73.0 mm
CRADLE_WALL         = 2.8;                // Sidewall thickness (mm)
CRADLE_LIP_H        = 14.0;               // Side retention lip height (mm)

module sun_visor_spring_tongue() {
    // Compliant spring clamp leaf located strictly in negative Z (underside of cradle)
    translate([0, 0, -(VISOR_CLAMP_GAP + CLAMP_SPRING_THICK)]) {
        // Main clamping leaf span
        hull() {
            // Root junction
            translate([0, -VISOR_CLAMP_WIDTH/2.0, 0])
                cube([8.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
            // Extended clamping arm
            translate([VISOR_CLAMP_DEPTH - 12.0, -VISOR_CLAMP_WIDTH/2.0, 0])
                cube([10.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
        }

        // Upturned/flared lead-in lip for easy one-handed push onto visor
        translate([VISOR_CLAMP_DEPTH - 5.0, -VISOR_CLAMP_WIDTH/2.0, 0]) {
            rotate([0, 30, 0])
                cube([15.0, VISOR_CLAMP_WIDTH, CLAMP_SPRING_THICK], center=false);
        }

        // Non-marring soft grip friction ribs (3x transverse rounded ridges)
        for (rx = [15.0, 28.0, 42.0]) {
            translate([rx, -VISOR_CLAMP_WIDTH/2.0 + 2.0, CLAMP_SPRING_THICK])
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

        // --- SUBTRACTIONS (100% unobstructed internal cavity) ---

        // 1. Pod 3 Main Bed Recess (135 x 70 mm clearance)
        translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, 1.2])
            cube([POD_OUTER_L + 0.5, POD_OUTER_W + 0.5, CRADLE_LIP_H + 2.0], center=false);

        // 2. Headliner Cable Exit Channel (Directs USB-C cable up towards roof seam)
        translate([-CRADLE_L/2.0 - 1.0, -8.0, 1.0])
            cube([12.0, 16.0, 8.0], center=false);

        // Cable clip grooves along rear spine
        translate([-CRADLE_L/2.0 + 4.0, -2.5, 0.8])
            cube([20.0, 5.0, 6.0], center=false);

        // 3. Weight reduction cutouts in floor plate (outside clamping footprint)
        for (dx = [-45.0, 45.0]) {
            translate([dx, 0, -1.0])
                cylinder(r=15.0, h=6.0, center=true, $fn=36);
        }
    }
}

module car_sun_visor_pod3_clip() {
    // 1. Upper Pod 3 Docking Bed (in +Z: 0 .. +14 mm)
    pod3_docking_cradle();

    // 2. Robust Underside Spine & Visor Clamp Bridge (in -Z: 0 .. -18 mm)
    // The spine drops down from the bottom of the cradle floor to the spring tongue
    translate([-25.0, -VISOR_CLAMP_WIDTH/2.0, -(VISOR_CLAMP_GAP + CLAMP_SPRING_THICK)]) {
        difference() {
            // Solid U-channel bridge
            cube([12.0, VISOR_CLAMP_WIDTH, VISOR_CLAMP_GAP + CLAMP_SPRING_THICK + 0.1], center=false);
            // Generous inner fillet relief
            translate([12.0, -1.0, VISOR_CLAMP_GAP + CLAMP_SPRING_THICK])
                rotate([0, 45, 0])
                    cube([8.0, VISOR_CLAMP_WIDTH + 2.0, 8.0], center=false);
        }
    }

    // 3. Compliant Visor Spring Tongue (in -Z, runs parallel to cradle bottom)
    translate([-25.0, 0, 0])
        sun_visor_spring_tongue();
}

// --- Parametric Render / Export Modes ---
part = "assembly"; // ["assembly", "single"]

if (part == "assembly") {
    // Top cradle perspective (shows Pod 3 docking cavity, snap detents & cable exit)
    translate([0, -48.0, 0])
        car_sun_visor_pod3_clip();

    // Underside perspective (shows visor clamp jaw, clamping gap, ridges & lead-in lip)
    translate([0, 48.0, 0])
        rotate([180, 0, 0])
            car_sun_visor_pod3_clip();
} else {
    car_sun_visor_pod3_clip();
}


