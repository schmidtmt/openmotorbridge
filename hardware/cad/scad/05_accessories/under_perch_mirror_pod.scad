// =============================================================================
// OpenMotorBridge - Accessories: Ultra-Compact Universal Under-Perch Mirror Pod
// =============================================================================
// File: hardware/cad/scad/05_accessories/under_perch_mirror_pod.scad
// Description: Ultra-compact under-perch enclosure housing the Z-stacked
//              bilateral-symmetric PCBA 05C (18.25 x 14.0 mm, v10.2-ultracompact).
//              100% mathematically and mechanically invariant along the central
//              Y=0 axis: ONE single universal PCBA serves BOTH Left and Right
//              motorcycle mirror perches without modifications!
//
// Features:
// - Ultra-compact 23.05 x 18.8 mm outer footprint (43% shorter than v10.1).
// - Z-Stacked Double-Sided Architecture:
//   * Top (F.Cu): J1 JST-GH 4P (-X=5.625), Dual Amber 1206 BSD LEDs (+X=5.875, Y=±4.2),
//                 and single central M2 mounting screw H1 (+X=5.875, Y=0.0).
//   * Bottom (B.Cu): Omron B3SL-1002P IP67 tactile switch centered at X=-0.125, Y=0.0.
// - Unified 38° upward stadium light hood with central M2 fastener boss.
// - Clamps under M8/M10 mirror stem with anti-rotation perch lip.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Render Selection ---
part = "assembly"; // Options: "assembly", "base", "cover", "lens", "button", "pcb_dummy", "exploded"
side = "left";     // Options: "left", "right" (flange mirrors across Y=0)

// --- PCBA 05C Ultra-Compact Dimensions (18.25 x 14.0 mm) ---
PCB_L               = 18.25; // Length (mm) - 43% shorter via Z-stacking
PCB_W               = 14.0;  // Width (mm)
PCB_T               = 1.6;   // Thickness (mm)
PCB_CLEARANCE       = 0.4;   // Internal pocket tolerance (mm)

// --- Enclosure Body Parameters ---
WALL_THICK          = 2.0;   // Structural wall thickness in PA12-CF (mm)
POD_L               = PCB_L + 2 * (WALL_THICK + PCB_CLEARANCE); // 23.05 mm
POD_W               = PCB_W + 2 * (WALL_THICK + PCB_CLEARANCE); // 18.80 mm
POD_H               = 16.5;  // Total height (mm)
BASE_H              = 11.5;  // Lower shell depth (mm)
COVER_H             = 5.0;   // Upper lid thickness (mm)
CORNER_R            = 2.5;   // Outer fillet radius (mm)

// --- M8/M10 Mirror Stem Mounting Flange ---
FLANGE_THICK        = 4.5;   // Robust clamping flange thickness (mm)
FLANGE_DIA          = 22.0;  // Flange outer diameter (mm)
MIRROR_HOLE_DIA     = 10.3;  // Fits standard M8 and M10 mirror stems (mm)
FLANGE_OFFSET_X     = -4.5;  // Offset from pod center along X (mm)
FLANGE_OFFSET_Y     = 17.5;  // Lateral offset from pod center along Y (mm)
ANTI_ROTATION_LIP_H = 1.5;   // Registration shoulder against perch body (mm)

// --- Coordinates Relative to PCBA Center (X_center = 9.125, Y_center = 7.00) ---
// H1 & Dual BSD LEDs at KiCad X = 15.00 mm -> +5.875 mm from center
H1_X                = 5.875; // Single M2 mounting screw X (mm)
H1_Y                = 0.0;   // Symmetrically centered on Y=0 axis (mm)

// SW1 (Omron B3SL-1002P on B.Cu) at KiCad X = 9.00, Y = 7.00 -> -0.125 mm from center
SW_X_OFFSET         = -0.125;
SW_Y_OFFSET         = 0.0;
BUTTON_CAP_DIA      = 8.5;   // Ergonomic thumb paddle diameter (mm)
BUTTON_RECESS_DEPTH = 1.5;   // Guard bezel to prevent accidental actuation (mm)

// --- Optical BSD LED Stadium Light Tunnel (38° Upward to Mirror Glass) ---
// Symmetrically spans across LED1 (+4.2 mm) and LED2 (-4.2 mm) at X = +5.875 mm
TUNNEL_X            = 5.875; // Aligned with LED1/LED2 at KiCad X = 15.00 mm
TUNNEL_Y_SPAN       = 8.4;   // Distance between LED centers (4.2 - (-4.2))
TUNNEL_WIDTH        = 5.6;   // Aperture width along X (mm)
TUNNEL_LENGTH       = 12.8;  // Aperture length along Y (mm)
TUNNEL_ANGLE        = 38.0;  // Angle upward into rider's mirror eye-box (degrees)
HOOD_OVERHANG       = 3.0;   // StVZO anti-glare sun hood extension (mm)
LENS_X              = 5.0;   // Frosted amber diffuser lens width (mm)
LENS_Y              = 12.0;  // Frosted amber diffuser lens length (mm)
LENS_THICK          = 1.2;   // Lens thickness (mm)

// --- JST-GH 4-Pin Cable Gland Conduit ---
CABLE_PORT_DIA      = 4.2;   // Bore for 4-core AWG28 shielded PUR cable (mm)
CABLE_STRAIN_L      = 5.5;   // Integrated conical strain relief nipple (mm)

// --- Central Single Fastener (M2 Stainless Thread-Forming Screw) ---
M2_SCREW_DIA        = 2.2;   // Clearance hole (mm)
M2_BOSS_OD          = 4.8;   // Central screw boss outer diameter (mm)
M2_POCKET_DEPTH     = 7.5;   // Core hole depth in base (mm)

// --- Colors ---
COLOR_PA12_CF       = [0.22, 0.23, 0.25, 1.0]; // Matte charcoal PA12-CF
COLOR_LID           = [0.18, 0.19, 0.21, 1.0]; // Contrast lid
COLOR_AMBER_LENS    = [1.00, 0.65, 0.05, 0.85]; // Amber optical diffuser
COLOR_BUTTON_TPU    = [0.15, 0.15, 0.15, 1.0]; // Grippy black TPU dome
COLOR_FR4           = [0.10, 0.45, 0.15, 1.0]; // Green FR4 PCB
COLOR_STAINLESS     = [0.85, 0.86, 0.88, 1.0]; // Stainless steel hardware

// =============================================================================
// Helper Modules
// =============================================================================

module rounded_box(x, y, z, r) {
    hull() {
        translate([-x/2 + r, -y/2 + r, 0]) cylinder(r=r, h=z, $fn=32);
        translate([ x/2 - r, -y/2 + r, 0]) cylinder(r=r, h=z, $fn=32);
        translate([ x/2 - r,  y/2 - r, 0]) cylinder(r=r, h=z, $fn=32);
        translate([-x/2 + r,  y/2 - r, 0]) cylinder(r=r, h=z, $fn=32);
    }
}

module stadium(x, y, h) {
    r = min(x, y) / 2;
    hull() {
        if (x >= y) {
            translate([-x/2 + r, 0, 0]) cylinder(r=r, h=h, $fn=32);
            translate([ x/2 - r, 0, 0]) cylinder(r=r, h=h, $fn=32);
        } else {
            translate([0, -y/2 + r, 0]) cylinder(r=r, h=h, $fn=32);
            translate([0,  y/2 - r, 0]) cylinder(r=r, h=h, $fn=32);
        }
    }
}

// =============================================================================
// Component Modules
// =============================================================================

module mirror_flange() {
    difference() {
        union() {
            // Main clamping disc
            translate([FLANGE_OFFSET_X, FLANGE_OFFSET_Y, 0])
                cylinder(d=FLANGE_DIA, h=FLANGE_THICK, $fn=48);
            
            // Connecting bridge web to ultra-compact main pod
            hull() {
                translate([FLANGE_OFFSET_X, FLANGE_OFFSET_Y, 0])
                    cylinder(d=FLANGE_DIA * 0.85, h=FLANGE_THICK, $fn=32);
                translate([0, 0, 0])
                    rounded_box(14.0, POD_W, FLANGE_THICK, CORNER_R);
            }

            // Anti-rotation locating shoulder
            translate([FLANGE_OFFSET_X, FLANGE_OFFSET_Y + FLANGE_DIA/2 - 2, FLANGE_THICK])
                cylinder(d1=4.0, d2=3.0, h=ANTI_ROTATION_LIP_H, $fn=24);
        }

        // Center mirror stem through-hole (M8 / M10 clear)
        translate([FLANGE_OFFSET_X, FLANGE_OFFSET_Y, -1])
            cylinder(d=MIRROR_HOLE_DIA, h=FLANGE_THICK + ANTI_ROTATION_LIP_H + 2, $fn=48);

        // Top chamfer for mirror locknut seating
        translate([FLANGE_OFFSET_X, FLANGE_OFFSET_Y, FLANGE_THICK - 0.8])
            cylinder(d1=MIRROR_HOLE_DIA, d2=MIRROR_HOLE_DIA + 1.6, h=1.0, $fn=48);
    }
}

module pod_base() {
    difference() {
        union() {
            // Main housing body (23.05 x 18.80 mm)
            rounded_box(POD_L, POD_W, BASE_H, CORNER_R);

            // Integrated mirror stem mounting flange
            mirror_flange();

            // Cable entry snout (Centered at Y=0, X=-POD_L/2)
            translate([-POD_L/2 - CABLE_STRAIN_L/2, 0, BASE_H/2])
                rotate([0, 90, 0])
                    cylinder(d1=CABLE_PORT_DIA + 3.0, d2=CABLE_PORT_DIA + 1.8, h=CABLE_STRAIN_L, center=true, $fn=24);
        }

        // Internal PCBA cavity (18.25 x 14.0 mm + clearance)
        translate([0, 0, WALL_THICK])
            rounded_box(PCB_L + 2*PCB_CLEARANCE, PCB_W + 2*PCB_CLEARANCE, BASE_H, 1.0);

        // Cable conduit pass-through (Axial on Y=0)
        translate([-POD_L/2 - CABLE_STRAIN_L - 1, 0, BASE_H/2])
            rotate([0, 90, 0])
                cylinder(d=CABLE_PORT_DIA, h=POD_L/2 + CABLE_STRAIN_L, $fn=24);

        // Tactile button thumb opening on lower face (centered under SW1 on B.Cu)
        translate([SW_X_OFFSET, SW_Y_OFFSET, -1]) {
            cylinder(d=BUTTON_CAP_DIA, h=WALL_THICK + 2, $fn=32);
            // Finger-centering conical chamfer
            cylinder(d1=BUTTON_CAP_DIA + 2.5, d2=BUTTON_CAP_DIA, h=BUTTON_RECESS_DEPTH + 1, $fn=32);
        }

        // Lip rabbet for sealing lid
        translate([0, 0, BASE_H - 1.5])
            difference() {
                rounded_box(POD_L + 1, POD_W + 1, 2, CORNER_R);
                rounded_box(POD_L - 1.6, POD_W - 1.6, 3, CORNER_R - 0.8);
            }
    }

    // Single M2 PCB mounting boss at H1 (+5.875, 0.0)
    difference() {
        translate([H1_X, H1_Y, 0])
            cylinder(d=M2_BOSS_OD, h=BASE_H - COVER_H, $fn=32);
        translate([H1_X, H1_Y, BASE_H - COVER_H - M2_POCKET_DEPTH + 1.0])
            cylinder(d=M2_SCREW_DIA - 0.4, h=M2_POCKET_DEPTH + 1.0, $fn=24);
    }
}

module pod_cover() {
    difference() {
        union() {
            // Main cover plate
            rounded_box(POD_L, POD_W, COVER_H, CORNER_R);

            // Upward 38° Bilateral BSD Light Tunnel Hood over LED1 & LED2
            translate([TUNNEL_X, 0, COVER_H])
                rotate([0, -TUNNEL_ANGLE, 0])
                    difference() {
                        stadium(TUNNEL_WIDTH + 2.2, TUNNEL_LENGTH + 2.2, HOOD_OVERHANG + 2.5);
                        translate([0, 0, -1])
                            stadium(TUNNEL_WIDTH, TUNNEL_LENGTH, HOOD_OVERHANG + 4.5);
                    }
        }

        // Internal hollow / mating lip (leaving central M2 boss bridge intact)
        difference() {
            translate([0, 0, -0.5])
                rounded_box(POD_L - 2*WALL_THICK, POD_W - 2*WALL_THICK, COVER_H - 1.8, 1.0);
            translate([H1_X, H1_Y, -1.0])
                cylinder(d=M2_BOSS_OD + 1.2, h=COVER_H + 2.0, $fn=24);
        }

        // Dual symmetric light apertures for LED1 (+Y=4.2) and LED2 (-Y=4.2)
        for (ly = [-4.2, 4.2]) {
            translate([TUNNEL_X, ly, -1])
                rotate([0, -TUNNEL_ANGLE, 0])
                    cylinder(d=4.4, h=COVER_H + HOOD_OVERHANG + 6, $fn=24);
        }

        // Single Central M2 Screw counterbore at H1 (+5.875, 0)
        translate([H1_X, H1_Y, -1])
            cylinder(d=M2_SCREW_DIA, h=COVER_H + 6, $fn=24);
        translate([H1_X, H1_Y, COVER_H - 1.8])
            cylinder(d=4.2, h=5.0, $fn=24);
    }
}

module diffuser_lens() {
    difference() {
        translate([TUNNEL_X, 0, COVER_H + 1.8])
            rotate([0, -TUNNEL_ANGLE, 0])
                translate([0, 0, -LENS_THICK/2])
                    stadium(LENS_X, LENS_Y, LENS_THICK);
        translate([H1_X, H1_Y, 0])
            cylinder(d=4.4, h=COVER_H + 10, $fn=24);
    }
}

module button_dome() {
    translate([SW_X_OFFSET, SW_Y_OFFSET, -0.5]) {
        // Outer thumb paddle
        cylinder(d=BUTTON_CAP_DIA - 0.6, h=2.5, center=true, $fn=32);
        // Tactile nub contacting Omron B3SL switch actuator on B.Cu
        translate([0, 0, 1.8])
            cylinder(d=2.8, h=1.8, center=true, $fn=16);
    }
}

module pcba_dummy() {
    translate([0, 0, BASE_H - COVER_H]) {
        // Green FR4 substrate (18.25 x 14.0 mm) with M2 hole H1 at (+5.875, 0)
        difference() {
            color(COLOR_FR4)
                rounded_box(PCB_L, PCB_W, PCB_T, 1.5);
            translate([H1_X, H1_Y, -0.5])
                cylinder(d=2.2, h=PCB_T + 1.0, $fn=24);
        }

        // J1 Connector (JST-GH 4P on F.Cu) at KiCad X=3.50 -> -5.625 mm
        color([0.95, 0.95, 0.95, 1.0])
            translate([-5.625, 0.0, PCB_T + 1.4])
                cube([4.25, 6.0, 2.8], center=true);

        // SW1 (Omron B3SL-1002P on B.Cu) at KiCad X=9.00 -> -0.125 mm
        color([0.3, 0.3, 0.3, 1.0])
            translate([SW_X_OFFSET, SW_Y_OFFSET, -1.5])
                cube([6.0, 6.0, 3.0], center=true);

        // Dual 1206 Amber BSD LEDs on F.Cu at KiCad X=15.00 -> +5.875 mm, Y=±4.2 mm
        color(COLOR_AMBER_LENS) {
            translate([H1_X, 4.2, PCB_T + 0.4])
                cube([3.2, 1.6, 0.8], center=true);
            translate([H1_X, -4.2, PCB_T + 0.4])
                cube([3.2, 1.6, 0.8], center=true);
        }

        // R1 & R2 Resistors at KiCad X=4.825 -> -4.30 mm, Y=±5.75 mm
        color([0.2, 0.2, 0.2, 1.0]) {
            translate([-4.30, 5.75, PCB_T + 0.25]) cube([1.6, 0.8, 0.5], center=true);
            translate([-4.30, -5.75, PCB_T + 0.25]) cube([1.6, 0.8, 0.5], center=true);
        }
    }
}

// =============================================================================
// Top-Level Assembly with Bilateral Symmetry
// =============================================================================

module full_pod_assembly() {
    mirror([0, (side == "right" ? 1 : 0), 0]) {
        color(COLOR_PA12_CF)
            pod_base();

        color(COLOR_LID)
            translate([0, 0, BASE_H])
                pod_cover();

        color(COLOR_AMBER_LENS)
            translate([0, 0, BASE_H])
                diffuser_lens();

        color(COLOR_BUTTON_TPU)
            button_dome();

        pcba_dummy();
    }
}

// --- Render Switch ---
if (part == "assembly") {
    full_pod_assembly();
} else if (part == "base") {
    mirror([0, (side == "right" ? 1 : 0), 0])
        color(COLOR_PA12_CF) pod_base();
} else if (part == "cover") {
    mirror([0, (side == "right" ? 1 : 0), 0])
        color(COLOR_LID) pod_cover();
} else if (part == "lens") {
    color(COLOR_AMBER_LENS) diffuser_lens();
} else if (part == "button") {
    color(COLOR_BUTTON_TPU) button_dome();
} else if (part == "pcb_dummy") {
    pcba_dummy();
} else if (part == "exploded") {
    mirror([0, (side == "right" ? 1 : 0), 0]) {
        color(COLOR_PA12_CF) pod_base();
        color(COLOR_BUTTON_TPU) translate([0, 0, -8]) button_dome();
        translate([0, 0, 4]) pcba_dummy();
        color(COLOR_LID) translate([0, 0, BASE_H + 12]) pod_cover();
        color(COLOR_AMBER_LENS) translate([0, 0, BASE_H + 20]) diffuser_lens();
    }
}
