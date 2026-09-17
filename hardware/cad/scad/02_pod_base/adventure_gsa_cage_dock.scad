// =============================================================================
// OpenMotorBridge - GSA Heavy-Duty Pannier Rack Cage Dock (Kofferträger-Käfig-Konsole)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_gsa_cage_dock.scad
// Description: Heavy-duty armored exoskeleton caddy attaching Satellite Pods 1 & 2
//              inside the triangular truss niche of BMW GS Adventure / Touratech
//              Ø 18 mm stainless steel pannier racks.
//
//              Key Engineering Features:
//              1. Dual-Tube Clamp Saddle: Two integrated Ø 18 mm clamps spaced 85 mm
//                 apart along the rack tube, completely eliminating single-point wobble.
//              2. Armored Roost & Stone Guard: Faceted 45° deflection skid plate facing
//                 the rear wheel, protecting the pod from mud, gravel roost, and impacts.
//              3. Stealth Niche Integration: Tucks the pod deep into the dead space
//                 between the pannier rack loop and motorcycle chassis (100% hidden
//                 behind aluminum luggage cases).
//              4. Concealed M8 Harness Conduit: Recessed channel along the inner tube
//                 shadow routes the M8 PUR cable forward to the subframe without exposed loops.
//              5. Heavy-Duty Expedition Aesthetics: Matte-black PA12-CF faceted geometry
//                 matching Touratech / Wunderlich GSA toolbox styling.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
GSA_TUBE_DIA        = 18.2;  // Ø 18 mm stainless steel rack tube bore (mm)
GSA_TUBE_R          = GSA_TUBE_DIA / 2.0;
GSA_POD_L           = 136.0; // Internal pod length clearance (mm)
GSA_POD_W           = 71.0;  // Internal pod width clearance (mm)
GSA_POD_H           = 38.5;  // Internal pod height clearance (mm)
GSA_WALL            = 3.5;   // Armored structural wall thickness (mm)
GSA_FLOOR           = 4.0;   // Armored bottom skid plate thickness (mm)

// Outer Caddy Envelope
CADDY_TOTAL_L       = 162.0; // Total exoskeleton length (mm)
CADDY_TOTAL_W       = 82.0;  // Total width (nested pod + walls, mm)
CADDY_TOTAL_H       = 44.0;  // Total height (mm)
CADDY_CHAMFER       = 6.0;   // Faceted rally chamfer (mm)

// Dual Clamping Stations (Spaced along tube at X1 and X2)
CLAMP_SPAN_X        = 85.0;  // Center-to-center distance between clamps (mm)
CLAMP_X1            = 28.0;  // First clamp center position (mm)
CLAMP_X2            = CLAMP_X1 + CLAMP_SPAN_X; // Second clamp center (113 mm)
CLAMP_WIDTH_X       = 24.0;  // Width of each individual clamp block (mm)
CLAMP_BOLT_DIST_Z   = 32.0;  // Distance between upper & lower M5 clamping bolts (mm)
CLAMP_BOLT_R        = 2.8;   // M5 clearance hole (Ø 5.6 mm)
CLAMP_NUT_R         = 4.6;   // M5 hex nut pocket across corners (mm)
CLAMP_NUT_H         = 4.8;   // Hex stopnut depth (mm)

// Tube Offset: Shifts the tube axis relative to the pod body for stealth tuck-in
TUBE_OFFSET_Y       = -GSA_TUBE_R - 2.0; // Tube rests against outer flank of caddy
TUBE_OFFSET_Z       = CADDY_TOTAL_H / 2.0; // Centered in height

// Faceted Solid Hull Helper
module gsa_faceted_box(l, w, h, ch) {
    hull() {
        // Bottom chamfered corners (Stone deflector bevel)
        translate([ch, ch, 0]) cylinder(r=ch, h=0.1, $fn=16);
        translate([l - ch, ch, 0]) cylinder(r=ch, h=0.1, $fn=16);
        translate([ch, w - ch, 0]) cylinder(r=ch, h=0.1, $fn=16);
        translate([l - ch, w - ch, 0]) cylinder(r=ch, h=0.1, $fn=16);

        // Mid-height flare
        translate([0, 0, ch]) cube([l, w, h - 2 * ch]);

        // Top chamfered corners
        translate([ch, ch, h]) cylinder(r=ch, h=0.1, $fn=16);
        translate([l - ch, ch, h]) cylinder(r=ch, h=0.1, $fn=16);
        translate([ch, w - ch, h]) cylinder(r=ch, h=0.1, $fn=16);
        translate([l - ch, w - ch, h]) cylinder(r=ch, h=0.1, $fn=16);
    }
}

// -----------------------------------------------------------------------------
// MODULE 1: GSA CAGE DOCK MAIN BODY (ARMORED EXOSKELETON)
// -----------------------------------------------------------------------------
module adventure_gsa_cage_dock_body() {
    difference() {
        union() {
            // 1. Main Armored Caddy Box (Rally Faceted)
            gsa_faceted_box(CADDY_TOTAL_L, CADDY_TOTAL_W, CADDY_TOTAL_H, CADDY_CHAMFER);

            // 2. Dual Clamping Bosses extending towards the rack tube (Y <= 0)
            for (cx = [CLAMP_X1, CLAMP_X2]) {
                translate([cx - CLAMP_WIDTH_X/2.0, TUBE_OFFSET_Y - GSA_TUBE_R - 2.0, 2.0]) {
                    hull() {
                        cube([CLAMP_WIDTH_X, 10.0, CADDY_TOTAL_H - 4.0]);
                        translate([0, GSA_TUBE_R + 8.0, 0])
                            cube([CLAMP_WIDTH_X, 2.0, CADDY_TOTAL_H - 4.0]);
                    }
                }
            }

            // 3. Heavy-Duty Diagonal Reinforcing Ribs between clamps
            translate([CLAMP_X1 + CLAMP_WIDTH_X/2.0, TUBE_OFFSET_Y + 1.0, 4.0])
                cube([CLAMP_SPAN_X - CLAMP_WIDTH_X, 6.0, CADDY_TOTAL_H - 8.0]);
        }

        // --- SUBTRACTIONS ---

        // A. Pod Main Reception Chamber (Deep recessed pocket)
        translate([12.0, GSA_WALL + 4.0, GSA_FLOOR])
            cube([GSA_POD_L, GSA_POD_W, CADDY_TOTAL_H + 5.0]);

        // Front mouth opening for quick-release cartridge sliding
        translate([GSA_POD_L + 10.0, GSA_WALL + 8.0, GSA_FLOOR])
            cube([CADDY_TOTAL_L - GSA_POD_L, GSA_POD_W - 8.0, CADDY_TOTAL_H + 5.0]);

        // B. Ø 18 mm Continuous Stainless Steel Tube Semi-Circular Saddle
        translate([-5.0, TUBE_OFFSET_Y, TUBE_OFFSET_Z])
            rotate([0, 90, 0])
                cylinder(r=GSA_TUBE_R, h=CADDY_TOTAL_L + 10.0, $fn=36);

        // Anti-slip internal friction grip ridges
        for (cx = [CLAMP_X1, CLAMP_X2]) {
            for (dx = [-6.0, 0.0, 6.0]) {
                translate([cx + dx, TUBE_OFFSET_Y, TUBE_OFFSET_Z])
                    rotate([0, 90, 0])
                        difference() {
                            cylinder(r=GSA_TUBE_R + 0.6, h=1.5, center=true, $fn=36);
                            cylinder(r=GSA_TUBE_R, h=2.0, center=true, $fn=36);
                        }
            }
        }

        // C. Dual M5 Clamping Bolt Through-Bores with Hex Nut Pockets
        for (cx = [CLAMP_X1, CLAMP_X2]) {
            for (dz = [-CLAMP_BOLT_DIST_Z/2.0, CLAMP_BOLT_DIST_Z/2.0]) {
                translate([cx, TUBE_OFFSET_Y - GSA_TUBE_R - 8.0, TUBE_OFFSET_Z + dz]) {
                    rotate([-90, 0, 0]) {
                        // M5 clearance bore
                        cylinder(r=CLAMP_BOLT_R, h=20.0, $fn=20);
                        // Hex locknut retention pocket (DIN 985)
                        translate([0, 0, 10.0])
                            cylinder(r=CLAMP_NUT_R, h=CLAMP_NUT_H + 2.0, $fn=6);
                    }
                }
            }
        }

        // D. Internal M8 PUR Cable Concealed Routing Channel (Port A to front tube shadow)
        translate([4.0, GSA_WALL + 20.0, GSA_FLOOR]) {
            hull() {
                cube([10.0, 16.0, 12.0]);
                translate([0, -18.0, 0]) cube([10.0, 16.0, 12.0]);
            }
        }

        // E. Lateral Expedition Style Cutouts (Lightweighting & aesthetics)
        for (gx = [CLAMP_X1 + 18.0, CLAMP_X1 + 42.0]) {
            translate([gx, CADDY_TOTAL_W - 4.0, 10.0])
                cube([16.0, 6.0, CADDY_TOTAL_H - 20.0]);
        }

        // F. Drain / Weep Holes on Bottom Skid Plate
        for (dx = [35.0, 80.0, 125.0]) {
            translate([dx, CADDY_TOTAL_W/2.0, -1.0])
                cylinder(r=2.5, h=GSA_FLOOR + 2.0, $fn=16);
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE 2: HEAVY-DUTY Ø 18 MM CLAMPING CAPS (PAIR)
// -----------------------------------------------------------------------------
module adventure_gsa_clamp_cap() {
    difference() {
        // Clamping block
        translate([-CLAMP_WIDTH_X/2.0, -14.0, -CLAMP_BOLT_DIST_Z/2.0 - 5.0])
            cube([CLAMP_WIDTH_X, 14.0, CLAMP_BOLT_DIST_Z + 10.0]);

        // Semi-circular tube saddle
        translate([-CLAMP_WIDTH_X/2.0 - 1.0, 0, 0])
            rotate([0, 90, 0])
                cylinder(r=GSA_TUBE_R, h=CLAMP_WIDTH_X + 2.0, $fn=36);

        // 2x M5 Clamping Bolt Bores with Deep DIN 912 Socket Head Counterbores
        for (dz = [-CLAMP_BOLT_DIST_Z/2.0, CLAMP_BOLT_DIST_Z/2.0]) {
            translate([0, 2.0, dz]) {
                rotate([-90, 0, 0]) {
                    cylinder(r=CLAMP_BOLT_R, h=25.0, center=true, $fn=20);
                    translate([0, 0, -14.0])
                        cylinder(r=5.0, h=8.0, $fn=20); // Counterbore
                }
            }
        }
    }
}

// -----------------------------------------------------------------------------
// MASTER MODULE: GSA CAGE DOCK ASSEMBLY
// -----------------------------------------------------------------------------
module adventure_gsa_cage_dock(part = "assembly") {
    if (part == "body") {
        adventure_gsa_cage_dock_body();
    } else if (part == "cap") {
        adventure_gsa_clamp_cap();
    } else {
        // Assembled View
        color("#1c222b", 0.96)
            adventure_gsa_cage_dock_body();

        // Dual Clamping Caps clamped around tube
        for (cx = [CLAMP_X1, CLAMP_X2]) {
            translate([cx, TUBE_OFFSET_Y, TUBE_OFFSET_Z])
                color("#28303d", 0.98)
                    adventure_gsa_clamp_cap();
        }

        // Fastening Hardware (4x M5 DIN 912 V4A Socket Bolts)
        color("silver") {
            for (cx = [CLAMP_X1, CLAMP_X2]) {
                for (dz = [-CLAMP_BOLT_DIST_Z/2.0, CLAMP_BOLT_DIST_Z/2.0]) {
                    translate([cx, TUBE_OFFSET_Y - GSA_TUBE_R - 10.0, TUBE_OFFSET_Z + dz])
                        rotate([-90, 0, 0])
                            cylinder(r=2.5, h=28.0, $fn=16);
                }
            }
        }
    }
}

// Standalone render
adventure_gsa_cage_dock(part = "assembly");
