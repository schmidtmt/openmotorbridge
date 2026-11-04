// =============================================================================
// OpenMotorBridge - Cockpit Breakout & Handschuhfach-Hub Housing (PCBA 05B)
// =============================================================================
// File: hardware/cad/scad/04_front_node/cockpit_breakout_block.scad
// Description: Compact 50.0 x 20.0 mm media/power injection hub enclosure
//              housing PCBA 05B (v10.2 dual-edge opposing USB-C layout):
//              - North Face (Y = COCKPIT_BLOCK_W):
//                * J2: [ FRONT ] Downstream link to Front Node (X_pcb = 13.68 mm)
//                * J1: [ HOST ]  Upstream USB to Harley Skyline OS (X_pcb = 27.18 mm)
//              - South Face (Y = 0):
//                * J3: [ PHONE 15W ] Fast Charge at X_pcb = 7.82 mm
//                * J4: [ DONGLE ]    Wireless CarPlay/AA at X_pcb = 19.82 mm
//                * J5: [ MEDIA ]     USB 2.0 Media Stick at X_pcb = 31.82 mm
// =============================================================================

include <../00_common/parameters.scad>;

part = "all"; // [all, body, lid, clamp, assembly, closed, exploded, xray]
$fn  = 36;

// --- PCBA 05B Alignment Parameters (50.0 x 20.0 mm) ---
PCB_L           = 50.0;
PCB_W           = 20.0;
PCB_THICK       = 1.6;
WALL            = 2.2;    // Nominal wall thickness (mm)
PCB_CLR         = 0.6;
CORNER_R        = 2.5;    // Corner fillet radius (mm)

// --- Enclosure Dimensions ---
COCKPIT_BLOCK_L = PCB_L + 2 * (WALL + PCB_CLR); // 55.6 mm
COCKPIT_BLOCK_W = PCB_W + 2 * (WALL + PCB_CLR); // 25.6 mm
COCKPIT_BLOCK_H = 16.0;   // Outer enclosure height (mm)

PCB_OFFSET_X    = WALL + PCB_CLR; // 2.8 mm
PCB_OFFSET_Y    = WALL + PCB_CLR; // 2.8 mm
STANDOFF_H      = 2.5;    // Standoff height above floor for B.Cu passives (mm)
PCB_Z           = WALL + STANDOFF_H; // PCB bottom plane Z = 4.7 mm

// --- USB-C Port Cutout Coordinates ---
SOUTH_USB_X     = [PCB_OFFSET_X + 7.82, PCB_OFFSET_X + 19.82, PCB_OFFSET_X + 31.82];
NORTH_USB_X     = [PCB_OFFSET_X + 13.68, PCB_OFFSET_X + 27.18];
USB_PORT_W      = 9.8;    // Port width (mm)
USB_PORT_H      = 4.2;    // Port height (mm)
USB_PORT_Z      = PCB_Z + PCB_THICK + 1.6; // Center Z = 7.9 mm

// -----------------------------------------------------------------------------
// 1. Cockpit Breakout Main Body (Unterteil)
// -----------------------------------------------------------------------------
module cockpit_breakout_body() {
    color([0.22, 0.22, 0.24]) // Charcoal ASA / MJF PA12
    difference() {
        union() {
            // Main solid rounded housing block (55.6 x 25.6 x 16.0 mm)
            hull() {
                translate([CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
            }

            // Internal PCB mounting bosses (H1 at X_pcb=4.0, H2 at X_pcb=46.0, Y_pcb=16.0)
            translate([PCB_OFFSET_X + 4.0, PCB_OFFSET_Y + 16.0, WALL])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
            translate([PCB_OFFSET_X + 46.0, PCB_OFFSET_Y + 16.0, WALL])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
        }

        // --- Inner Electronics Cavity ---
        translate([WALL, WALL, WALL])
            cube(size=[COCKPIT_BLOCK_L - 2*WALL, COCKPIT_BLOCK_W - 2*WALL, COCKPIT_BLOCK_H], center=false);

        // --- 3x South Face USB-C Port Cutouts (Y = 0: J3 PHONE, J4 DONGLE, J5 MEDIA) ---
        for (ux = SOUTH_USB_X) {
            translate([ux - USB_PORT_W/2, -1.0, USB_PORT_Z - USB_PORT_H/2])
                cube(size=[USB_PORT_W, WALL + 2.0, USB_PORT_H], center=false);
        }

        // --- 2x North Face USB-C Port Cutouts (Y = COCKPIT_BLOCK_W: J2 FRONT, J1 HOST) ---
        for (ux = NORTH_USB_X) {
            translate([ux - USB_PORT_W/2, COCKPIT_BLOCK_W - WALL - 1.0, USB_PORT_Z - USB_PORT_H/2])
                cube(size=[USB_PORT_W, WALL + 2.0, USB_PORT_H], center=false);
        }

        // --- M2.5 Pilot Holes in PCB Standoff Bosses ---
        translate([PCB_OFFSET_X + 4.0, PCB_OFFSET_Y + 16.0, WALL - 0.5])
            cylinder(r=M2_5_PILOT_HOLE_R, h=STANDOFF_H + 2.0, center=false);
        translate([PCB_OFFSET_X + 46.0, PCB_OFFSET_Y + 16.0, WALL - 0.5])
            cylinder(r=M2_5_PILOT_HOLE_R, h=STANDOFF_H + 2.0, center=false);

        // --- Bottom 3M Dual-Lock Recess (1.2 mm deep, for glovebox floor) ---
        translate([8.0, 4.0, -0.1])
            cube(size=[COCKPIT_BLOCK_L - 16.0, COCKPIT_BLOCK_W - 8.0, 1.3], center=false);

        // --- Top Perimeter Lid Nesting Step ---
        difference() {
            translate([WALL - 1.0, WALL - 1.0, COCKPIT_BLOCK_H - 1.5])
                cube([COCKPIT_BLOCK_L - 2*(WALL - 1.0), COCKPIT_BLOCK_W - 2*(WALL - 1.0), 2.0]);
            translate([WALL + 0.3, WALL + 0.3, COCKPIT_BLOCK_H - 2.0])
                cube([COCKPIT_BLOCK_L - 2*(WALL + 0.3), COCKPIT_BLOCK_W - 2*(WALL + 0.3), 3.0]);
        }
    }
}

// -----------------------------------------------------------------------------
// 2. Weatherproof Snap/Screw Lid Plate (Oberteil / Deckel)
// -----------------------------------------------------------------------------
module cockpit_breakout_lid() {
    color([0.28, 0.28, 0.30]) // Anthracite ASA
    difference() {
        union() {
            hull() {
                translate([CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
            }
            translate([WALL + 0.2, WALL + 0.2, -1.4])
                cube([COCKPIT_BLOCK_L - 2*(WALL + 0.2), COCKPIT_BLOCK_W - 2*(WALL + 0.2), 1.5], center=false);
        }

        translate([WALL + 1.5, WALL + 1.5, -2.0])
            cube([COCKPIT_BLOCK_L - 2*(WALL + 1.5), COCKPIT_BLOCK_W - 2*(WALL + 1.5), 2.5], center=false);

        // 2x M2.5 Countersunk Screw Holes matching H1 and H2
        for (hx = [PCB_OFFSET_X + 4.0, PCB_OFFSET_X + 46.0]) {
            translate([hx, PCB_OFFSET_Y + 16.0, -2.0]) {
                cylinder(r=1.4, h=6.0, center=false);
                translate([0, 0, 3.0])
                    cylinder(r1=1.4, r2=2.8, h=1.8, center=false);
            }
        }

        translate([COCKPIT_BLOCK_L/2.0, COCKPIT_BLOCK_W/2.0, 2.0])
            linear_extrude(height = 0.8)
                text("OMB // HUB 05B", size = 2.2, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

// -----------------------------------------------------------------------------
// 3. Mechanical Anti-Vibration Strain-Relief Clamping Bar
// -----------------------------------------------------------------------------
module cockpit_breakout_clamp() {
    color([0.30, 0.30, 0.32])
    difference() {
        translate([2.0, 8.0, 0])
            cube(size=[COCKPIT_BLOCK_L - 4.0, 10.0, 4.5], center=false);
        for (hx = [PCB_OFFSET_X + 4.0, PCB_OFFSET_X + 46.0]) {
            translate([hx, 13.0, -0.5])
                cylinder(r=1.4, h=6.0, center=false);
        }
        for (ux = SOUTH_USB_X) {
            translate([ux, 7.9, 2.2])
                rotate([-90, 0, 0])
                    cylinder(r=2.5, h=10.5, center=false);
        }
    }
}

// -----------------------------------------------------------------------------
// 4. Dummy PCBA 05B Model (50.0 x 20.0 mm)
// -----------------------------------------------------------------------------
module dummy_cockpit_breakout_pcb() {
    translate([PCB_OFFSET_X, PCB_OFFSET_Y, PCB_Z]) {
        color([0.15, 0.15, 0.16])
        difference() {
            cube([PCB_L, PCB_W, PCB_THICK], center=false);
            translate([4.0, 16.0, -0.5])
                cylinder(r=1.35, h=PCB_THICK + 1.0, center=false);
            translate([46.0, 16.0, -0.5])
                cylinder(r=1.35, h=PCB_THICK + 1.0, center=false);
        }

        // 3x South USB-C Receptacles (J3=7.82, J4=19.82, J5=31.82)
        color([0.82, 0.82, 0.85]) {
            for (px = [7.82, 19.82, 31.82]) {
                translate([px - 4.47, -0.8, PCB_THICK])
                    cube([8.94, 7.3, 3.2], center=false);
            }
            // 2x North USB-C Receptacles (J2=13.68, J1=27.18)
            for (px = [13.68, 27.18]) {
                translate([px - 4.47, PCB_W - 6.5, PCB_THICK])
                    cube([8.94, 7.3, 3.2], center=false);
            }
        }

        // U1: Microchip USB2514B QFN-36 Hub Controller at (43.25, 6.41)
        color([0.12, 0.12, 0.14])
            translate([43.25 - 3.0, 6.41 - 3.0, PCB_THICK])
                cube([6.0, 6.0, 0.9], center=false);
    }
}

// -----------------------------------------------------------------------------
// Assembly & Presentation Selectors
// -----------------------------------------------------------------------------
if (part == "body") {
    cockpit_breakout_body();
} else if (part == "lid") {
    cockpit_breakout_lid();
} else if (part == "clamp") {
    cockpit_breakout_clamp();
} else if (part == "closed") {
    cockpit_breakout_body();
    translate([0, 0, COCKPIT_BLOCK_H - 0.2])
        cockpit_breakout_lid();
} else if (part == "exploded") {
    cockpit_breakout_body();
    translate([0, 0, 12.0])
        dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H + 20.0])
        cockpit_breakout_lid();
    translate([0, 0, COCKPIT_BLOCK_H + 32.0])
        cockpit_breakout_clamp();
} else if (part == "xray") {
    %cockpit_breakout_body();
    dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H - 0.2])
        %cockpit_breakout_lid();
} else {
    cockpit_breakout_body();
    dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H + 4.0])
        cockpit_breakout_lid();
}
