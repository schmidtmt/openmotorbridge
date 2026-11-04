// ============================================================================
// OpenMotorBridge - Cockpit Under-Perch Mirror-Stem Switch & BSD Pod (PCBA 05C)
// ============================================================================
// File: hardware/cad/scad/05_accessories/under_perch_mirror_pod.scad
// Version: 10.3 (100% Left/Right Symmetric Housing + 45° Pivoting Thumb
//                Paddle Rocker + Unbroken Angled Optical TIR Prism)
// Author: OpenMotorBridge Hardware Team
// License: CERN-OHL-S v2
//
// Description:
//   Ultra-compact IP67 enclosure (23.25 x 20.0 x 16.5 mm) for the 4-layer
//   PCBA 05C (18.25 x 14.0 mm) that mounts directly under the M8/M10 mirror
//   thread (or perch bolt) on both Left and Right handlebars using 100%
//   identical PCB and housing parts:
//   - PCBA 05C Dual-Side Stackup:
//       * F.Cu (Top, +Z):    LED1 & LED2 (1206 Amber/Red, X=+5.875, Y=+-4.2)
//                            D1 (SOD-323), R1/R2/R3 (0402), J1 (BM04B-SRSS-TB
//                            at X=-6.375, Y=0)
//       * B.Cu (Bottom, -Z): SW1 (Omron B3SL-1002P IP67 Tactile Switch at
//                            X=-0.125, Y=0, facing straight DOWN -Z)
//       * H1 (Mounting):     M2 through-hole at X=+4.875, Y=0
//   - 100% Symmetrical Left/Right Architecture (Y = 0 Mirror Plane):
//       * Inline M8/M10 mirror stem mounting flange on the -X spine, flush
//         with the top surface (Z = POD_H) so the pod sits cleanly beneath
//         left or right mirror perches without any L/R housing variants.
//       * Removable top cover (`pod_cover`) sits in front of the rear flange
//         spine so the cover can be opened without unbolting the mirror stem.
//   - 45° Pivoting Thumb Paddle Rocker (Option C):
//       * Converts horizontal (+X -> -X) or diagonal (+X/-Z) gloved thumb
//         presses at the front/bottom edge into a vertical (+Z) lift directly
//         onto the downward-facing SW1 on B.Cu via an internal lever arm
//         pivoting around rear trunnions at X = -6.2 mm.
//   - Unbroken Angled Optical TIR Prism (`diffuser_lens`):
//       * Clear/Amber PMMA/PC optical lightguide with two vertical light-
//         collection legs directly over LED1 & LED2 (straddling the submerged
//         M2 cover screw H1) that merge above the screw head into a single,
//         unbroken angled ("abgeknickt") Total Internal Reflection (TIR)
//         prism head deflecting the vertical LED light at 38° toward the
//         mirror glass / rider, shielded toward the road by a StVZO bezel.
// ============================================================================

$fn = 64;

// --- Export Selection ---
// "assembly" | "exploded" | "cutaway" | "base" | "cover" | "lens" | "button"
part = "assembly";
// Kept for CLI backwards-compatibility; geometry is 100% Y=0 symmetric
side = "left";

// --- Exact PCBA 05C Dimensions & Component Coordinates (PCB Center = 0,0) ---
PCB_L             = 18.25;  // X: -9.125 to +9.125 mm
PCB_W             = 14.00;  // Y: -7.000 to +7.000 mm
PCB_T             = 1.60;   // 4-Layer FR4 thickness
PCB_CLEARANCE     = 0.25;   // Radial fit tolerance

// Exact Component Coordinates relative to PCB center (0,0):
J1_X              = -6.375; // JST-SH 4-pin vertical connector (F.Cu)
J1_Y              =  0.000;
SW1_X             = -0.125; // Omron B3SL-1002P tactile switch (B.Cu, faces -Z)
SW1_Y             =  0.000;
SW1_H             =  3.40;  // Switch body + plunger height below B.Cu
H1_X              =  4.875; // M2 mounting hole (X=+4.875, Y=0.0)
H1_Y              =  0.000;
LED_X             =  5.875; // Dual 1206 LEDs (F.Cu, emitting +Z)
LED1_Y            = -4.200; // LED1 (Amber/Red)
LED2_Y            =  4.200; // LED2 (Amber/Red)

// --- Enclosure Outer Dimensions ---
WALL              = 2.25;
POD_L             = PCB_L + 2 * WALL + 0.50; // 23.25 mm (X: -11.625 to +11.625)
POD_W             = PCB_W + 2 * WALL + 1.50; // 20.00 mm (Y: -10.0 to +10.0)
POD_H             = 16.50;                   // Total height (Z: 0 to 16.5)
POD_R             = 2.80;                    // Corner fillet radius

// Vertical Stackup (Z = 0 is bottom of pod_base, Z = 16.5 is top under-perch face)
PCB_Z             = 5.40;                    // B.Cu at Z=5.40, F.Cu at Z=7.00
POD_SPLIT_Z       = 11.20;                   // Split plane between base and cover
SPINE_X_END       = -8.80;                   // Rear flange spine front face (X: -11.625 to -8.80)
COVER_X_START     = -8.60;                   // Cover starts 0.2 mm in front of rear spine

// --- Inline Mirror Stem Mounting Flange (-X Spine, Y = 0 Symmetric) ---
FLANGE_X          = -POD_L/2 - 9.40;         // X = -21.025 mm
FLANGE_Y          = 0.00;                    // 100% Symmetric on Y=0 axis
FLANGE_D          = 21.00;                   // Outer boss diameter
FLANGE_T          = 4.20;                    // Clamping plate thickness (Z: 12.3 to 16.5)
MIRROR_HOLE_D     = 10.50;                   // M10 mirror stem clearance

// --- 45° Pivoting Thumb Rocker (Option C) ---
PIVOT_X           = -6.20;                   // Rear pivot axle X
PIVOT_Z           =  2.50;                   // Rear pivot axle Z
PIVOT_D           =  2.40;                   // Pivot pin diameter
ROCKER_W          = 12.40;                   // Paddle & lever width (Y: -6.2 to +6.2)

// --- Angled Optical TIR Prism (`diffuser_lens`) ---
PRISM_W           = 11.60;                   // Continuous prism width (Y: -5.8 to +5.8)
PRISM_COLLAR_Z    = 14.90;                   // Lower bridge above M2 screw head (H1)
PRISM_TOP_Z       = POD_H + 5.20;            // Protrudes 5.2 mm above cover top

// --- Color Palette ---
C_ASA_BLACK       = [0.14, 0.15, 0.17, 1.0];
C_TPU_SLATE       = [0.24, 0.27, 0.31, 1.0];
C_PC_AMBER        = [1.00, 0.60, 0.05, 0.88];
C_PCB_GREEN       = [0.08, 0.38, 0.18, 1.0];
C_GOLD            = [0.85, 0.70, 0.20, 1.0];

// ============================================================================
// Helper Modules
// ============================================================================
module rounded_rect_3d(l, w, h, r) {
    hull() {
        for (dx = [-l/2 + r, l/2 - r])
            for (dy = [-w/2 + r, w/2 - r])
                translate([dx, dy, 0])
                    cylinder(r = r, h = h);
    }
}

// ============================================================================
// 1. Inline Symmetric Mirror-Stem Mounting Flange (-X End, Flush with Z=POD_H)
// ============================================================================
module mirror_flange() {
    difference() {
        union() {
            // Rear full-height structural spine on pod_base (X: -11.625 to -8.80)
            hull() {
                for (dy = [-POD_W/2 + POD_R, POD_W/2 - POD_R])
                    translate([-POD_L/2 + POD_R, dy, POD_SPLIT_Z - 0.5])
                        cylinder(r = POD_R, h = POD_H - POD_SPLIT_Z + 0.5);
                translate([SPINE_X_END - 0.8, -POD_W/2 + 1.5, POD_SPLIT_Z - 0.5])
                    cube([0.8, POD_W - 3.0, POD_H - POD_SPLIT_Z + 0.5]);
            }

            // Top flush clamping flange bridging from rear spine to FLANGE_X
            hull() {
                translate([FLANGE_X, FLANGE_Y, POD_H - FLANGE_T])
                    cylinder(d = FLANGE_D, h = FLANGE_T);
                translate([-POD_L/2, -POD_W/2 + 2.2, POD_H - FLANGE_T])
                    cube([2.8, POD_W - 4.4, FLANGE_T]);
            }

            // Diagonal twin structural gussets from pod base down-slope to flange
            for (sy = [-1, 1]) {
                hull() {
                    translate([FLANGE_X + 3.2, sy * 4.8, POD_H - FLANGE_T])
                        cylinder(d = 3.2, h = 0.6);
                    translate([-POD_L/2 + 1.2, sy * (POD_W/2 - 2.6), 4.2])
                        cylinder(d = 3.2, h = POD_H - 4.2);
                }
            }

            // Anti-rotation crush ribs on top surface (+Z perch contact face)
            for (ang = [55, 180, 305]) {
                translate([FLANGE_X + (FLANGE_D/2 - 2.0) * cos(ang),
                           FLANGE_Y + (FLANGE_D/2 - 2.0) * sin(ang),
                           POD_H - 0.1])
                    cylinder(d1 = 2.2, d2 = 1.4, h = 0.7);
            }
        }

        // M10 Mirror Stem Through-Hole
        translate([FLANGE_X, FLANGE_Y, -1])
            cylinder(d = MIRROR_HOLE_D, h = POD_H + 10);

        // Lower washer/nut clearance counterbore from below (up to Z = POD_H - FLANGE_T)
        translate([FLANGE_X, FLANGE_Y, -1])
            cylinder(d = 18.2, h = POD_H - FLANGE_T + 1.0);

        // Protected under-flange cable entry groove from rear into J1 chamber
        hull() {
            translate([-POD_L/2 - 3.5, 0, PCB_Z + PCB_T + 2.0])
                rotate([0, 90, 0])
                    cylinder(d = 4.0, h = 7.5);
            translate([J1_X, 0, PCB_Z + PCB_T + 1.8])
                cylinder(d = 4.4, h = 2.4);
        }
    }
}

// ============================================================================
// 2. Pod Lower Base (`pod_base`) - 100% Left/Right Symmetric
// ============================================================================
module pod_base() {
    difference() {
        union() {
            // Main lower housing body up to split line (Z = 0 to 11.20)
            rounded_rect_3d(POD_L, POD_W, POD_SPLIT_Z, POD_R);

            // Alignment lip into cover (only in front of rear spine: X > COVER_X_START)
            intersection() {
                translate([0, 0, POD_SPLIT_Z])
                    rounded_rect_3d(POD_L - 2.2, POD_W - 2.2, 1.1, max(0.6, POD_R - 1.1));
                translate([COVER_X_START + 0.8, -POD_W, POD_SPLIT_Z])
                    cube([POD_L, 2 * POD_W, 2.0]);
            }

            // Symmetric Inline Mirror Flange & Rear Spine
            mirror_flange();
        }

        // --- Upper PCB & Component Chamber (Z = PCB_Z to Top) ---
        translate([0, 0, PCB_Z])
            rounded_rect_3d(PCB_L + 2*PCB_CLEARANCE, PCB_W + 2*PCB_CLEARANCE, POD_H, 0.8);

        // Rear cable entry channel from under-flange groove into J1 (X = -6.375)
        hull() {
            translate([-POD_L/2 - 3.5, 0, PCB_Z + PCB_T + 2.0])
                rotate([0, 90, 0])
                    cylinder(d = 4.0, h = 7.5);
            translate([J1_X, 0, PCB_Z + PCB_T + 1.5])
                cylinder(d = 4.8, h = 3.5);
        }

        // --- Lower Chamber for SW1 (B.Cu) & 45° Pivoting Thumb Rocker ---
        // Internal lever channel from X = -8.0 to +POD_L/2 + 2 (Z = 1.0 to PCB_Z + 0.1)
        translate([-8.0, -ROCKER_W/2 - 0.35, 1.0])
            cube([POD_L/2 + 8.0 + 2.0, ROCKER_W + 0.70, PCB_Z - 0.9]);

        // Open front-bottom slot at +X so the 45° paddle sweeps freely
        translate([POD_L/2 - 3.8, -ROCKER_W/2 - 0.35, -0.5])
            cube([6.0, ROCKER_W + 0.70, 6.8]);

        // Beveled ergonomic thumb access cutout around the +X front-bottom opening
        hull() {
            translate([POD_L/2 - 1.2, -ROCKER_W/2 - 1.0, -0.1])
                cube([3.0, ROCKER_W + 2.0, 5.2]);
            translate([POD_L/2 + 0.5, -ROCKER_W/2 - 1.8, -0.1])
                cube([1.0, ROCKER_W + 3.6, 6.2]);
        }

        // Pivot axle trunnion sockets at X = PIVOT_X (-6.2), Z = PIVOT_Z (2.5)
        translate([PIVOT_X, 0, PIVOT_Z])
            rotate([90, 0, 0])
                cylinder(d = PIVOT_D + 0.45, h = ROCKER_W + 3.4, center = true);

        // Snap-in assembly slots from PCB cavity down to trunnion sockets
        for (sy = [-1, 1]) {
            translate([PIVOT_X - (PIVOT_D + 0.3)/2,
                       sy * (ROCKER_W/2 + 0.85) - 0.85,
                       PIVOT_Z])
                cube([PIVOT_D + 0.3, 1.7, PCB_Z - PIVOT_Z + 0.5]);
        }

        // --- Central M2 Thread Boss / Brass Heat-Set Insert Hole at H1 ---
        translate([H1_X, H1_Y, 1.2])
            cylinder(d = 3.2, h = POD_H);
    }

    // --- Internal PCB Support Ledges & H1 Standoff Pillar (at Z = PCB_Z = 5.4) ---
    // 1. Central H1 M2 standoff boss (positioned at X=+4.875, Y=0, with lateral
    //    bypass bridges around it in the rocker arm)
    difference() {
        translate([H1_X, H1_Y, 0.0])
            cylinder(d = 5.2, h = PCB_Z);
        translate([H1_X, H1_Y, 1.0])
            cylinder(d = 3.0, h = PCB_Z + 1.0);
    }

    // 2. Corner PCB support ledges at Z = PCB_Z (supporting the 4 corners of PCBA 05C)
    for (sx = [-1, 1]) {
        for (sy = [-1, 1]) {
            translate([sx * (PCB_L/2 - 1.2), sy * (PCB_W/2 - 0.8), PCB_Z - 1.8])
                cylinder(d = 2.6, h = 1.8);
        }
    }
}

// ============================================================================
// 3. 45° Pivoting Thumb Paddle Rocker (`button_dome` - Option C)
// ============================================================================
// Converts a horizontal (+X -> -X) or 45° diagonal (+X/-Z) gloved thumb press
// at the front/bottom edge into a straight upward (+Z) lift on SW1 (B.Cu).
module button_dome() {
    difference() {
        union() {
            // 1. Rear Pivot Axle + Lateral Trunnion Pins (X = -6.2, Z = 2.5)
            translate([PIVOT_X, 0, PIVOT_Z])
                rotate([90, 0, 0])
                    cylinder(d = PIVOT_D, h = ROCKER_W + 2.6, center = true);

            // 2. Internal Lever Arm (X = -6.2 to +9.2, Z = 1.5 to 3.4)
            hull() {
                translate([PIVOT_X, 0, PIVOT_Z])
                    rotate([90, 0, 0])
                        cylinder(d = PIVOT_D, h = ROCKER_W - 0.4, center = true);
                translate([9.0, 0, 2.3])
                    rotate([90, 0, 0])
                        cylinder(d = 2.0, h = ROCKER_W - 0.4, center = true);
            }

            // 3. Vertical Actuator Cam Nub directly beneath SW1 (X = -0.125, Y = 0)
            // Contacts Omron B3SL-1002P plunger on B.Cu (at Z = 5.4 - 1.4 = 4.0 mm)
            translate([SW1_X, SW1_Y, 2.6]) {
                cylinder(d1 = 5.0, d2 = 3.4, h = 1.35);
                translate([0, 0, 1.35])
                    scale([1, 1, 0.35])
                        sphere(d = 3.4);
            }

            // 4. External 45°-Angled Ergonomic Thumb Paddle at Front/Bottom (+X / -Z)
            // The lower-front thumb contact face is angled at 45° facing (+X, -Z)
            // so pressing inward/upward with the thumb lifts the lever in +Z!
            hull() {
                // Inner transition at housing front wall (X = +8.8)
                translate([8.8, 0, 1.9])
                    rotate([90, 0, 0])
                        cylinder(d = 1.8, h = ROCKER_W - 0.4, center = true);
                translate([9.6, 0, 4.8])
                    rotate([90, 0, 0])
                        cylinder(d = 1.8, h = ROCKER_W - 0.4, center = true);
                // Lower tip of the 45° thumb face (X = +10.4, Z = 0.6)
                translate([10.4, 0, 0.6])
                    rotate([90, 0, 0])
                        cylinder(d = 1.6, h = ROCKER_W - 0.4, center = true);
                // Outer-upper crest of the 45° thumb face (X = +14.2, Z = 4.4)
                translate([14.2, 0, 4.4])
                    rotate([90, 0, 0])
                        cylinder(d = 1.8, h = ROCKER_W - 0.4, center = true);
                // Upper travel-stop lip tucking under the housing front overhang
                translate([12.2, 0, 5.4])
                    rotate([90, 0, 0])
                        cylinder(d = 1.4, h = ROCKER_W - 0.4, center = true);
            }

            // 5. Tactile Grip Ribs along the 45° (+X / -Z) Thumb Contact Face
            for (t = [0.22, 0.48, 0.74]) {
                rib_x = 10.4 + t * (14.2 - 10.4) + 0.45;
                rib_z = 0.6  + t * (4.4  - 0.6)  - 0.45;
                translate([rib_x, 0, rib_z])
                    rotate([90, 0, 0])
                        cylinder(d = 1.05, h = ROCKER_W - 1.4, center = true);
            }
        }

        // Slotted clearance window around the central M2 standoff pillar (H1 at X=+4.875, Y=0)
        hull() {
            translate([H1_X - 0.5, H1_Y, -1])
                cylinder(d = 6.0, h = 10);
            translate([H1_X + 0.7, H1_Y, -1])
                cylinder(d = 6.0, h = 10);
        }
    }
}

// ============================================================================
// 4. Unbroken Angled Optical TIR Prism (`diffuser_lens`)
// ============================================================================
// Collects vertical (+Z) light from LED1 & LED2 (X=+5.875, Y=+-4.2) via two
// lower collimator legs (straddling the recessed M2 cover screw H1 at Y=0),
// then merges above the M2 screw head into a single, unbroken bent ("abgeknickt")
// Total Internal Reflection (TIR) prism that redirects the beam at 38° toward
// the mirror/rider.
module diffuser_lens() {
    union() {
        // 1. Dual Vertical Light-Collector Pillars over LED1 & LED2 (Z = 8.4 to 15.2)
        for (ly = [LED1_Y, LED2_Y]) {
            translate([LED_X, ly, PCB_Z + PCB_T + 1.4])
                cylinder(d1 = 3.4, d2 = 4.0, h = PRISM_COLLAR_Z - (PCB_Z + PCB_T + 1.4) + 0.4);
        }

        // 2. Retention Flange Collar seated inside pod_cover above M2 screw head (Z = 14.9 to 16.5)
        translate([LED_X - 0.2, 0, PRISM_COLLAR_Z])
            rounded_rect_3d(5.2, PRISM_W, POD_H - PRISM_COLLAR_Z + 0.1, 1.2);

        // 3. Unbroken Angled ("Abgeknickt") TIR Optical Prism Head above Cover (Z = 16.4 to 21.7)
        //    - Vertical lower body rises out of the cover
        //    - Back (+X) 48° TIR mirror facet reflects vertical rays into the -38° axis
        //    - Front (-X/+Z) angled emission head bends toward the mirror/rider
        hull() {
            // Base footprint at cover surface (Z = 16.4)
            translate([LED_X - 0.1, 0, POD_H - 0.1])
                rounded_rect_3d(4.8, PRISM_W - 0.4, 0.4, 1.0);

            // Vertical knee before bend (Z = 18.2)
            translate([LED_X - 0.3, 0, POD_H + 1.7])
                rounded_rect_3d(4.6, PRISM_W - 0.4, 0.4, 1.0);

            // Angled prism crest (bent toward -X / mirror at 38°, Z = 21.6)
            translate([LED_X - 2.4, 0, PRISM_TOP_Z - 0.4])
                rounded_rect_3d(3.2, PRISM_W - 0.8, 0.4, 0.9);
        }

        // 4. Micro-Fresnel Horizontal Collimator Grooves on the -X/+Z Emission Face
        for (z_off = [1.4, 2.5, 3.6]) {
            translate([LED_X - 1.9 - z_off * 0.36, 0, POD_H + z_off])
                rotate([0, -38, 0])
                    rotate([90, 0, 0])
                        cylinder(d = 0.65, h = PRISM_W - 2.2, center = true);
        }
    }
}

// ============================================================================
// 5. Pod Upper Cover (`pod_cover`) with Submerged M2 Mount & StVZO Shield
// ============================================================================
// Sits in front of the rear flange spine (X = -8.60 to +11.625, Z = 11.4 to 16.5)
// so it can be removed upward without unbolting the mirror stem.
module pod_cover() {
    cover_h = POD_H - POD_SPLIT_Z - 0.20; // 5.10 mm
    difference() {
        union() {
            // 1. Main upper cover body (cropped cleanly at X = COVER_X_START in front of spine)
            intersection() {
                translate([0, 0, POD_SPLIT_Z + 0.20])
                    rounded_rect_3d(POD_L, POD_W, cover_h, POD_R);
                translate([COVER_X_START, -POD_W, POD_SPLIT_Z])
                    cube([POD_L + 5.0, 2 * POD_W, cover_h + 2.0]);
            }

            // 2. StVZO Anti-Glare Back & Side Bezel cupping the +X rear and +-Y sides
            //    of the angled prism (blocks stray light toward oncoming traffic while
            //    leaving the bent amber prism profile and -X emission face wide open)
            difference() {
                hull() {
                    translate([LED_X + 0.3, 0, POD_H - 0.2])
                        rounded_rect_3d(6.8, PRISM_W + 2.6, 0.4, 1.6);
                    translate([LED_X + 0.5, 0, PRISM_TOP_Z - 0.6])
                        rounded_rect_3d(4.4, PRISM_W + 1.8, 0.4, 1.3);
                }
                // Cut open the entire front (-X) and inner prism cavity so the amber
                // bent prism is prominently visible from the rider/mirror side and side view
                translate([LED_X - 3.6, -PRISM_W/2 + 0.1, POD_H - 0.5])
                    cube([6.2, PRISM_W - 0.2, 8.0]);
                // Diagonal side-window cut so the "abgeknickt" prism knee is visible from the side
                translate([LED_X - 4.5, -POD_W, POD_H + 1.4])
                    rotate([0, -34, 0])
                        cube([7.2, 2 * POD_W, 8.0]);
            }
        }

        // Mating recess for pod_base alignment lip at Z = 11.2 to 12.4
        translate([0, 0, POD_SPLIT_Z])
            rounded_rect_3d(POD_L - 1.9, POD_W - 1.9, 1.25, max(0.6, POD_R - 0.95));

        // Upper PCB component headroom cavity (J1 connector & SMD parts)
        translate([-1.5, 0, POD_SPLIT_Z])
            rounded_rect_3d(PCB_L - 2.0, PCB_W - 1.0, 2.2, 0.8);

        // Dual vertical optical channels for the two prism collector legs (LED1 & LED2)
        for (ly = [LED1_Y, LED2_Y]) {
            translate([LED_X, ly, POD_SPLIT_Z - 0.5])
                cylinder(d = 4.25, h = cover_h + 2.0);
        }

        // Upper pocket for the prism bridge collar (Z = PRISM_COLLAR_Z to POD_H + 1)
        translate([LED_X - 0.2, 0, PRISM_COLLAR_Z - 0.1])
            rounded_rect_3d(5.45, PRISM_W + 0.25, POD_H - PRISM_COLLAR_Z + 1.5, 1.25);

        // Submerged Central M2 Screw Counterbore at H1 (X=+4.875, Y=0)
        // Screw is installed BEFORE snapping the prism into the cover, so the
        // screw head sits cleanly at Z = 12.8..14.6 mm beneath the prism bridge!
        translate([H1_X, H1_Y, POD_SPLIT_Z - 0.5])
            cylinder(d = 2.4, h = cover_h + 2.0);
        translate([H1_X, H1_Y, POD_SPLIT_Z + 1.4])
            cylinder(d = 4.3, h = cover_h + 1.0);
    }
}

// ============================================================================
// 6. Dummy PCBA 05C Model (for Assembly / Cutaway Verification)
// ============================================================================
module pcba_05c_dummy() {
    translate([0, 0, PCB_Z]) {
        // 4-Layer FR4 Substrate (18.25 x 14.0 x 1.6 mm)
        color(C_PCB_GREEN)
        difference() {
            translate([-PCB_L/2, -PCB_W/2, 0])
                cube([PCB_L, PCB_W, PCB_T]);
            translate([H1_X, H1_Y, -0.5])
                cylinder(d = 2.2, h = PCB_T + 1.0);
        }

        // B.Cu (-Z): SW1 Omron B3SL-1002P IP67 Tactile Switch facing straight DOWN
        color([0.20, 0.20, 0.22])
        translate([SW1_X - 3.1, SW1_Y - 3.1, -1.0])
            cube([6.2, 6.2, 1.0]);
        color([0.85, 0.35, 0.10])
        translate([SW1_X, SW1_Y, -1.45])
            cylinder(d = 2.5, h = 0.45);

        // F.Cu (+Z): LED1 & LED2 (1206 Amber/Red, emitting vertically +Z)
        color([1.0, 0.55, 0.0])
        for (ly = [LED1_Y, LED2_Y]) {
            translate([LED_X - 0.8, ly - 1.6, PCB_T])
                cube([1.6, 3.2, 1.1]);
        }

        // F.Cu (+Z): J1 JST-SH 4-Pin Vertical Connector (BM04B-SRSS-TB)
        color([0.92, 0.90, 0.85])
        translate([J1_X - 1.45, J1_Y - 3.0, PCB_T])
            cube([2.9, 6.0, 4.25]);
    }
}

// ============================================================================
// Top-Level Dispatcher
// ============================================================================
if (part == "base") {
    pod_base();
} else if (part == "cover") {
    pod_cover();
} else if (part == "lens") {
    diffuser_lens();
} else if (part == "button") {
    button_dome();
} else if (part == "exploded") {
    color(C_ASA_BLACK) pod_base();
    translate([8, 0, -10]) color(C_TPU_SLATE) button_dome();
    translate([0, 0, 7])   pcba_05c_dummy();
    translate([0, 0, 16])  color(C_ASA_BLACK) pod_cover();
    translate([0, 0, 25])  color(C_PC_AMBER)  diffuser_lens();
} else if (part == "cutaway") {
    difference() {
        union() {
            color(C_ASA_BLACK) pod_base();
            color(C_TPU_SLATE) button_dome();
            pcba_05c_dummy();
            color(C_ASA_BLACK) pod_cover();
            color(C_PC_AMBER)  diffuser_lens();
        }
        translate([-50, -50, -20])
            cube([100, 50, 60]);
    }
} else {
    // Full Assembly
    color(C_ASA_BLACK) pod_base();
    color(C_TPU_SLATE) button_dome();
    pcba_05c_dummy();
    color(C_ASA_BLACK) pod_cover();
    color(C_PC_AMBER)  diffuser_lens();
}
