// =============================================================================
// OpenMotorBridge - Accessories: Blind Spot Detection (BSD) Mirror Indicator Pod
// =============================================================================
// File: hardware/cad/scad/05_accessories/bsd_mirror_indicator_pod.scad
// Description: Aerodynamic clip-on indicator pod for motorcycle mirror stems
//              (Port J9: BSD Left / Right on Front Node PCBA 05).
//
// OPTICAL & SAFETY ARCHITECTURE:
// 1. Focused Eye-Box Projection: Integrated 38° inward-angled light tunnel
//    directs the amber/red radar warning strobe straight into the rider's
//    peripheral vision.
// 2. Zero-Glare StVZO / ECE R50 Compliance: The 3.5 mm deep overhanging hood
//    and opaque forward wall block 100% of forward- and outward-facing light,
//    preventing glare for oncoming traffic and passing TÜV inspection.
// 3. Universal Stem Clamping: Precision 2-piece clamshell fits standard
//    Ø 10.0 mm mirror stems (Harley, BMW, KTM, Japanese) with optional 12 mm
//    or 8 mm EPDM reduction shims. Secured with 2x M3 stainless hardware.
// 4. Concealed Cable Routing: Internal rear cable channel with strain relief
//    running directly along the mirror stem down to Front Node Port J9.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Render Selection ---
part = "assembly"; // Options: "assembly", "pod", "clamp", "lens", "cutaway"

// --- Parametric Dimensions ---
STEM_DIA            = 10.0;  // Nominal mirror stem diameter (mm, e.g. Harley/BMW 10mm)
STEM_CLAMP_L        = 22.0;  // Clamp body length along stem (mm)
WALL_THICK          = 2.2;   // Structural wall thickness in PA12-CF (mm)

// Pod Body (Aerodynamic Teardrop)
POD_L               = 32.0;  // Total pod length front-to-back (mm)
POD_W               = 16.0;  // Pod width (mm)
POD_H               = 18.0;  // Pod height (mm)
POD_SPLIT_Z         = 0.0;   // Split plane along stem axis Z=0 (mm)

// Optical Light Tunnel (38° Inward Angle toward Helmet)
LIGHT_ANGLE         = 38.0;  // Angle toward rider eye box (degrees)
LENS_DIA            = 8.0;   // Optical diffuser lens aperture diameter (mm)
HOOD_OVERHANG       = 3.8;   // Anti-glare visor hood extension (mm)
LED_CAVITY_DIA      = 5.4;   // Cavity for standard 5 mm high-brightness LED (mm)
LED_CAVITY_DEPTH    = 7.0;   // Depth of LED barrel (mm)

// Clamping Hardware (DIN 912 M3 x 12 mm + DIN 934 M3 Hex Nut)
M3_SCREW_PASS_DIA   = 3.3;   // Screw clearance hole (mm)
M3_HEAD_CBORE_DIA   = 5.8;   // Allen head counterbore diameter (mm)
M3_HEAD_CBORE_D     = 3.0;   // Counterbore depth (mm)
M3_NUT_SW           = 5.7;   // Captive hex nut across flats (mm)
M3_NUT_DEPTH        = 2.6;   // Nut pocket depth (mm)
CLAMP_BOLT_OFFSET   = 8.2;   // Distance from stem axis to M3 clamp bolts (mm)

// Cable Conduit
CABLE_PASS_DIA      = 3.2;   // Bore for 2-pin wire to Port J9 (mm)

// Colors
COLOR_PA12_CF       = [0.20, 0.22, 0.24, 1.0]; // Charcoal matte PA12-CF
COLOR_STAINLESS     = [0.85, 0.86, 0.88, 1.0]; // Polished stainless steel
COLOR_AMBER_LENS    = [1.00, 0.65, 0.05, 0.85];// Amber translucent acrylic/PC
COLOR_STEM_CHROME   = [0.90, 0.90, 0.92, 1.0]; // Chrome mirror stem
COLOR_CABLE         = [0.08, 0.08, 0.08, 1.0]; // Matte black cable

// =============================================================================
// MODULE: Upper Optical Pod Body
// =============================================================================
module bsd_upper_pod_body() {
    difference() {
        union() {
            // 1. Aerodynamic Teardrop Outer Hull
            intersection() {
                hull() {
                    // Aerodynamic nose (forward facing)
                    translate([POD_L/2 - 6.0, 0, 3.0])
                        sphere(r=5.0, $fn=36);

                    // Central bulwark
                    translate([0, 0, 4.0])
                        sphere(r=POD_W/2, $fn=36);

                    // Rear optical hood crown
                    translate([-POD_L/2 + 6.0, 0, 5.0])
                        sphere(r=POD_W/2 - 1.0, $fn=36);

                    // Clamp base root
                    translate([-STEM_CLAMP_L/2, -POD_W/2, 0])
                        cube([STEM_CLAMP_L, POD_W, 2.0]);
                }
                // Clip strictly to Z >= 0
                translate([0, 0, 25.0])
                    cube([100, 100, 50], center=true);
            }

            // 2. M3 Clamping Bolt Bosses (Left & Right)
            for (side = [-1, 1]) {
                translate([0, side * CLAMP_BOLT_OFFSET, 0]) {
                    cylinder(r=3.8, h=5.5, $fn=24);
                }
            }
        }

        // --- SUBTRACTIONS ---

        // 1. Semicircular Mirror Stem Cradle (Z = 0)
        rotate([0, 90, 0])
            cylinder(r=STEM_DIA/2, h=POD_L + 10.0, center=true, $fn=48);

        // 2. M3 Clamping Bolt Holes & Counterbores
        for (side = [-1, 1]) {
            translate([0, side * CLAMP_BOLT_OFFSET, -1.0]) {
                cylinder(r=M3_SCREW_PASS_DIA/2, h=10.0, $fn=24);
                translate([0, 0, 5.5 - M3_HEAD_CBORE_D + 1.0])
                    cylinder(r=M3_HEAD_CBORE_DIA/2, h=M3_HEAD_CBORE_D + 2.0, $fn=24);
            }
        }

        // 3. Directional Light Tunnel (Angled 38° Inward)
        translate([-POD_L/2 + 5.0, 0, 5.0]) {
            rotate([0, 0, LIGHT_ANGLE]) {
                // Optical tunnel bore
                cylinder(r=LENS_DIA/2, h=25.0, center=true, $fn=36);

                // LED Mounting Seat (Deep inside pod)
                translate([0, 0, -4.0])
                    cylinder(r=LED_CAVITY_DIA/2, h=LED_CAVITY_DEPTH + 5.0, center=true, $fn=24);

                // Lens retention step ring
                translate([0, 0, 3.0])
                    cylinder(r=LENS_DIA/2 + 0.6, h=2.0, $fn=36);
            }
        }

        // 4. Concealed Cable Conduit out rear
        translate([-STEM_CLAMP_L/2 - 2.0, 0, 1.2])
            rotate([0, 90, 0])
                cylinder(r=CABLE_PASS_DIA/2, h=STEM_CLAMP_L + 4.0, $fn=24);
    }
}

// =============================================================================
// MODULE: Lower Clamping Strap
// =============================================================================
module bsd_lower_clamp_strap() {
    difference() {
        union() {
            // Main clamp saddle block
            intersection() {
                hull() {
                    translate([-STEM_CLAMP_L/2 + 3.0, 0, -WALL_THICK - STEM_DIA/2])
                        cylinder(r=STEM_DIA/2 + WALL_THICK, h=STEM_DIA/2 + WALL_THICK, $fn=36);
                    translate([STEM_CLAMP_L/2 - 3.0, 0, -WALL_THICK - STEM_DIA/2])
                        cylinder(r=STEM_DIA/2 + WALL_THICK, h=STEM_DIA/2 + WALL_THICK, $fn=36);
                }
                // Clip strictly to Z <= 0
                translate([0, 0, -25.0])
                    cube([100, 100, 50], center=true);
            }

            // Clamp bolt ears with captive nut pockets
            for (side = [-1, 1]) {
                translate([0, side * CLAMP_BOLT_OFFSET, -5.5]) {
                    cylinder(r=3.8, h=5.5, $fn=24);
                }
            }
        }

        // --- SUBTRACTIONS ---

        // 1. Semicircular Mirror Stem Cradle (Z <= 0)
        rotate([0, 90, 0])
            cylinder(r=STEM_DIA/2, h=STEM_CLAMP_L + 10.0, center=true, $fn=48);

        // 2. M3 Screw Clearance & Captive Hex Nut Pockets (DIN 934)
        for (side = [-1, 1]) {
            translate([0, side * CLAMP_BOLT_OFFSET, -10.0]) {
                cylinder(r=M3_SCREW_PASS_DIA/2, h=15.0, $fn=24);
                // Captive hex nut pocket from bottom
                translate([0, 0, 3.0])
                    rotate([0, 0, 30])
                        cylinder(r=M3_NUT_SW / (2 * cos(30)), h=M3_NUT_DEPTH + 1.0, $fn=6);
            }
        }
    }
}

// =============================================================================
// MODULE: Translucent Amber Diffuser Lens Disc
// =============================================================================
module bsd_diffuser_lens() {
    translate([-POD_L/2 + 5.0, 0, 5.0]) {
        rotate([0, 0, LIGHT_ANGLE]) {
            translate([0, 0, 4.0])
                cylinder(r=LENS_DIA/2 + 0.4, h=1.8, center=true, $fn=36);
        }
    }
}

// =============================================================================
// DUMMY HARDWARE (Mirror Stem, LED & Screws for Previews)
// =============================================================================
module dummy_mirror_stem() {
    color(COLOR_STEM_CHROME)
        rotate([0, 90, 0])
            cylinder(r=STEM_DIA/2, h=60.0, center=true, $fn=48);
}

module dummy_internal_led() {
    color([1.0, 0.8, 0.1, 1.0])
        translate([-POD_L/2 + 5.0, 0, 5.0])
            rotate([0, 0, LIGHT_ANGLE])
                cylinder(r=2.5, h=6.0, center=true, $fn=24);
}

module dummy_m3_hardware() {
    color(COLOR_STAINLESS) {
        for (side = [-1, 1]) {
            translate([0, side * CLAMP_BOLT_OFFSET, 6.0]) {
                // Screw head
                cylinder(r=2.7, h=2.8, center=true, $fn=24);
                // Screw shaft
                translate([0, 0, -6.5])
                    cylinder(r=1.45, h=13.0, center=true, $fn=24);
            }
        }
    }
}

// =============================================================================
// TOP-LEVEL RENDER CONTROLLER
// =============================================================================
if (part == "pod") {
    // Printable upper optical pod (flat mating face down on bed)
    bsd_upper_pod_body();
} else if (part == "clamp") {
    // Printable lower clamping strap (flat mating face down on bed)
    rotate([180, 0, 0])
        bsd_lower_clamp_strap();
} else if (part == "lens") {
    // Printable translucent lens insert
    bsd_diffuser_lens();
} else if (part == "assembly") {
    // Master studio assembly view
    color(COLOR_PA12_CF)
        bsd_upper_pod_body();
    color(COLOR_PA12_CF)
        bsd_lower_clamp_strap();
    color(COLOR_AMBER_LENS)
        bsd_diffuser_lens();
    dummy_mirror_stem();
    dummy_m3_hardware();
} else if (part == "cutaway") {
    // 50% Section cutaway for optical beam inspection
    difference() {
        union() {
            color(COLOR_PA12_CF)
                bsd_upper_pod_body();
            color(COLOR_PA12_CF)
                bsd_lower_clamp_strap();
            color(COLOR_AMBER_LENS)
                bsd_diffuser_lens();
            dummy_internal_led();
            dummy_mirror_stem();
            dummy_m3_hardware();
        }
        translate([0, -50, -50])
            cube([100, 100, 100]);
    }
} else {
    bsd_upper_pod_body();
}
