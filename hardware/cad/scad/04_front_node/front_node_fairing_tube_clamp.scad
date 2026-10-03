// =============================================================================
// OpenMotorBridge - Universal Front Node Fairing Tube Clamp (Verkleidungs-Rohrschelle)
// =============================================================================
// File: hardware/cad/scad/04_front_node/front_node_fairing_tube_clamp.scad
// Description: Heavy-duty 2-piece vibration-isolated tube clamp adapter connecting
//              the Universal Front Node (PCBA 05) to round metal fairing stays,
//              sub-fairing tubular brackets (Verkleidungsgeweih), GPS accessory bars,
//              and cockpit crossbars (Ø 12 mm to Ø 22 mm).
//
// Key Engineering Features:
// 1. Dual-Diameter 120° V-Prism: Self-centering geometry clamps rock-solid to:
//    - Ø 12 mm: BMW GS/GSA, Ténéré 700, Africa Twin, KTM GPS/Nav crossbars
//    - Ø 16 mm: Harley Road Glide (Sharknose) & Street Glide tubular fairing stays
//    - Ø 19 mm (3/4"): Harley Touring fairing support rods & cockpit frames
//    - Ø 22 mm (7/8"): Universal cockpit crossbars & handlebar tubes
// 2. Direct AMPS Interface (38 x 30 mm): Bolts flush to the 4x captive M4 nut
//    pockets on the bottom of front_node_lower_tub.stl.
// 3. Bi-Directional Mounting (0° / 90°): Symmetrical AMPS grid allows mounting
//    the Front Node either parallel (horizontal) or perpendicular (vertical)
//    to the fairing tube.
// 4. Non-Marring EPDM Rubber Channel: 1.2 mm recessed pocket for a 15 mm EPDM
//    anti-vibration damping strip, protecting painted/powder-coated tubes and
//    eliminating slip under harsh off-road vibration.
// 5. High-Strength Clamping: 2x M5 stainless clamping bolts with captive DIN 985
//    Nyloc stopnuts.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;

// --- Parametric Selector ---
// Options: "assembly", "base", "cap", "plate"
part = "plate";

// --- Tube Clamping Range ---
TUBE_MIN_DIA        = 12.0;  // Minimum bar diameter (mm, e.g. BMW GPS bar)
TUBE_MAX_DIA        = 22.2;  // Maximum bar diameter (mm, e.g. 7/8" cockpit tube)
TUBE_NOMINAL_DIA    = 16.0;  // Reference diameter for assembly preview (Harley stay)

// --- Dimensions ---
CLAMP_SPAN_Y        = 36.0;  // Clamp length along the round tube (mm)
CLAMP_BASE_W        = 56.0;  // Total width across the tube (mm)
CLAMP_BASE_THICK    = 10.5;  // Thickness from AMPS mating face to V-apex (mm)

// AMPS Grid (matching front_node_lower_tub.stl)
AMPS_DX             = AMPS_SPACING_X; // 38.0 mm
AMPS_DY             = AMPS_SPACING_Y; // 30.0 mm
AMPS_SCREW_R        = M4_SCREW_HOLE_R; // 2.2 mm (Ø 4.4 mm clearance)
AMPS_CBORE_R        = 4.2;   // Counterbore for M4 screw head (Ø 8.4 mm)
AMPS_CBORE_DEPTH    = 4.0;   // Counterbore depth (mm)

// Clamping Bolts (2x M5 along X at span 44.0 mm, centered in Y)
BOLT_SPAN_X         = 44.0;  // Center-to-center distance between M5 clamp bolts
BOLT_HOLE_R         = 2.7;   // M5 clearance hole (Ø 5.4 mm)
BOLT_CBORE_R        = 5.0;   // M5 socket head cap counterbore (Ø 10.0 mm)
NUT_M5_STOP_SW      = NUT_M5_SW + 0.3; // 8.5 mm across flats
NUT_M5_STOP_H       = 5.2;   // Stopnut depth (mm)

// EPDM Rubber Channel
EPDM_WIDTH          = 18.0;  // Width of rubber bed (mm)
EPDM_DEPTH          = 1.0;   // Damping recess depth (mm)

// =============================================================================
// MODULE: Clamp Base (Bolts to Front Node AMPS underside)
// =============================================================================
module fairing_tube_clamp_base() {
    difference() {
        // 1. Solid Base Block with Rounded Corners
        translate([-CLAMP_BASE_W/2, -CLAMP_SPAN_Y/2, -CLAMP_BASE_THICK]) {
            linear_extrude(height = CLAMP_BASE_THICK) {
                offset(r = 3.0) {
                    offset(delta = -3.0) {
                        square([CLAMP_BASE_W, CLAMP_SPAN_Y], center=false);
                    }
                }
            }
        }

        // 2. 120° V-Prism Cradle (Centered along Y-axis, apex at Z = -CLAMP_BASE_THICK + 3.0)
        // Accommodates Ø 12 mm to Ø 22 mm tubes with dual tangential line contacts
        translate([0, 0, -CLAMP_BASE_THICK - 0.5]) {
            rotate([0, 0, 0]) {
                // 120° V-cutout (prism extending along Y)
                rotate([0, 0, 0])
                    polyhedron(
                        points = [
                            [-16.0, -CLAMP_SPAN_Y/2 - 1.0, 9.5],
                            [ 16.0, -CLAMP_SPAN_Y/2 - 1.0, 9.5],
                            [  0.0, -CLAMP_SPAN_Y/2 - 1.0, 0.2],
                            [-16.0,  CLAMP_SPAN_Y/2 + 1.0, 9.5],
                            [ 16.0,  CLAMP_SPAN_Y/2 + 1.0, 9.5],
                            [  0.0,  CLAMP_SPAN_Y/2 + 1.0, 0.2]
                        ],
                        faces = [
                            [0, 1, 2], // Front
                            [3, 5, 4], // Back
                            [0, 2, 5, 3], // Left V slope
                            [1, 4, 5, 2], // Right V slope
                            [0, 3, 4, 1]  // Top
                        ]
                    );
            }
        }

        // 3. EPDM Rubber Grip Recess along V-groove
        translate([-EPDM_WIDTH/2, -CLAMP_SPAN_Y/2 - 1.0, -CLAMP_BASE_THICK - 0.1])
            cube([EPDM_WIDTH, CLAMP_SPAN_Y + 2.0, EPDM_DEPTH + 0.1]);

        // 4. AMPS 4-Hole Pattern (Counterbored M4 holes from bottom to top)
        // Allows screwing M4x12 mm DIN 912 screws through the clamp into the Front Node nut pockets
        amps_coords = [
            [-AMPS_DX/2, -AMPS_DY/2],
            [ AMPS_DX/2, -AMPS_DY/2],
            [-AMPS_DX/2,  AMPS_DY/2],
            [ AMPS_DX/2,  AMPS_DY/2]
        ];
        for (pt = amps_coords) {
            // M4 Clearance through-hole
            translate([pt[0], pt[1], -CLAMP_BASE_THICK - 1.0])
                cylinder(r = AMPS_SCREW_R, h = CLAMP_BASE_THICK + 2.0, $fn=36);
            // M4 Head Counterbore from the bottom (so screw heads are recessed below the tube)
            translate([pt[0], pt[1], -CLAMP_BASE_THICK - 0.1])
                cylinder(r = AMPS_CBORE_R, h = AMPS_CBORE_DEPTH, $fn=36);
        }

        // 5. 2x M5 Clamping Screw Clearance Holes (at X = +/- BOLT_SPAN_X/2, Y = 0)
        for (s = [-1, 1]) {
            translate([s * BOLT_SPAN_X/2, 0, -CLAMP_BASE_THICK - 1.0])
                cylinder(r = BOLT_HOLE_R, h = CLAMP_BASE_THICK + 2.0, $fn=36);
        }

        // 6. 2x Transverse Zip-Tie Backup Slots (5.0 mm wide x 1.6 mm deep)
        for (y_off = [-10.0, 10.0]) {
            translate([-CLAMP_BASE_W/2 - 1.0, y_off - 2.5, -CLAMP_BASE_THICK + 1.2])
                cube([CLAMP_BASE_W + 2.0, 5.0, 1.8]);
        }
    }
}

// =============================================================================
// MODULE: Clamp Cap (Matching lower retaining strap)
// =============================================================================
module fairing_tube_clamp_cap() {
    CAP_W       = CLAMP_BASE_W;
    CAP_L       = CLAMP_SPAN_Y;
    CAP_THICK   = 8.5; // Thickness from mating face to bottom arch

    difference() {
        // 1. Solid Cap Body with Rounded Corners
        translate([-CAP_W/2, -CAP_L/2, 0]) {
            linear_extrude(height = CAP_THICK) {
                offset(r = 3.0) {
                    offset(delta = -3.0) {
                        square([CAP_W, CAP_L], center=false);
                    }
                }
            }
        }

        // 2. 120° V-Prism Saddle (Centered along Y-axis, apex facing downwards)
        translate([0, 0, -0.5]) {
            polyhedron(
                points = [
                    [-16.0, -CAP_L/2 - 1.0, -0.5],
                    [ 16.0, -CAP_L/2 - 1.0, -0.5],
                    [  0.0, -CAP_L/2 - 1.0,  9.0],
                    [-16.0,  CAP_L/2 + 1.0, -0.5],
                    [ 16.0,  CAP_L/2 + 1.0, -0.5],
                    [  0.0,  CAP_L/2 + 1.0,  9.0]
                ],
                faces = [
                    [0, 2, 1], // Front
                    [3, 4, 5], // Back
                    [0, 3, 5, 2], // Left V slope
                    [1, 2, 5, 4], // Right V slope
                    [0, 1, 4, 3]  // Bottom
                ]
            );
        }

        // 3. EPDM Rubber Grip Recess in Cap
        translate([-EPDM_WIDTH/2, -CAP_L/2 - 1.0, -0.1])
            cube([EPDM_WIDTH, CAP_L + 2.0, EPDM_DEPTH + 0.1]);

        // 4. 2x M5 Clamping Screw Holes & Captive DIN 985 Stopnut Pockets
        for (s = [-1, 1]) {
            // M5 through-hole
            translate([s * BOLT_SPAN_X/2, 0, -1.0])
                cylinder(r = BOLT_HOLE_R, h = CAP_THICK + 2.0, $fn=36);

            // M5 Hex Stopnut Pocket on bottom
            translate([s * BOLT_SPAN_X/2, 0, CAP_THICK - NUT_M5_STOP_H + 0.1])
                rotate([0, 0, 30])
                    cylinder(r = NUT_M5_STOP_SW / cos(30) / 2.0, h = NUT_M5_STOP_H + 1.0, $fn=6);
        }
    }
}

// =============================================================================
// SELECTOR & RENDERING LOGIC
// =============================================================================
if (part == "base") {
    // Printable Base (mating face down on print bed)
    rotate([180, 0, 0])
        fairing_tube_clamp_base();
} else if (part == "cap") {
    // Printable Cap (mating face down on print bed)
    fairing_tube_clamp_cap();
} else if (part == "plate") {
    // 1-Click Print Plate: Base & Cap side-by-side (0 supports required!)
    translate([-CLAMP_BASE_W/2 - 4.0, 0, CLAMP_BASE_THICK])
        rotate([180, 0, 0])
            fairing_tube_clamp_base();

    translate([CLAMP_BASE_W/2 + 4.0, 0, 0])
        fairing_tube_clamp_cap();
} else if (part == "assembly") {
    // 3D Assembly Preview with Simulated Fairing Tube
    color([0.2, 0.2, 0.2, 1.0])
        fairing_tube_clamp_base();

    // Simulated Round Metal Tube (Ø 16 mm, e.g. Harley Fairing Stay)
    color([0.8, 0.8, 0.85, 0.8])
        translate([0, 0, -CLAMP_BASE_THICK - TUBE_NOMINAL_DIA/2 + 2.0])
            rotate([90, 0, 0])
                cylinder(r = TUBE_NOMINAL_DIA/2, h = 90.0, center=true, $fn=48);

    // Clamp Cap (clamped against tube)
    color([0.25, 0.25, 0.25, 1.0])
        translate([0, 0, -CLAMP_BASE_THICK - TUBE_NOMINAL_DIA + 1.0])
            rotate([180, 0, 0])
                fairing_tube_clamp_cap();
}
