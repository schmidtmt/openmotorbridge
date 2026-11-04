// =============================================================================
// OpenMotorBridge - PCBA 05B Handschuhfach-Hub Gehäuse (50.0 x 20.0 mm, 100% Parity)
// =============================================================================
// File: hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad
// Description: Ultra-compact media compartment power-injection and USB data hub
//              custom-tailored for PCBA 05B (50.0 x 20.0 mm, dual-sided USB-C).
//              Designed for the right glovebox of Harley-Davidson Touring & Bagger
//              motorcycles (Road Glide, Street Glide, CVO, CVO ST 2024+):
//              - North Edge (Vehicle / Upstream Side, Y = HUB_W):
//                * J2 [FRONT]: Downstream link to Universal Front Node (X_pcb = 13.68 mm)
//                * J1 [HOST]:  Connects to OEM Harley USB-C socket (X_pcb = 27.18 mm)
//              - South Edge (User / Device Side, Y = 0):
//                * J3 [PHONE]:  15W Fast-Charge port for smartphone (X_pcb = 7.82 mm)
//                * J4 [DONGLE]: Gated USB port for wireless CarPlay/AA (X_pcb = 19.82 mm)
//                * J5 [MEDIA]:  High-Speed USB 2.0 pass-through (X_pcb = 31.82 mm)
// =============================================================================

$fn = 32;

// --- PCB 05B Physical Dimensions (KiCad X=26..76, Y=0..20 -> 50.0 x 20.0 mm) ---
PCB_L       = 50.0;   // PCB length (mm) - 34% shorter via opposing USB-C rows
PCB_W       = 20.0;   // PCB width (mm)
PCB_T       = 1.6;    // PCB substrate thickness (mm)
PCB_CLR     = 0.5;    // Internal perimeter clearance (mm)

// --- Enclosure Outer Envelope ---
WALL_THICK  = 2.0;    // Robust PA12-MJF shell thickness (mm)
FLOOR_THICK = 2.0;    // Floor thickness (mm)
STANDOFF_H  = 2.5;    // PCB bottom component clearance for R1..R10 & C_IN1 (mm)
INNER_L     = PCB_L + 2 * PCB_CLR; // 51.0 mm
INNER_W     = PCB_W + 2 * PCB_CLR; // 21.0 mm
INNER_H     = 10.5;   // Interior clearance height (mm)

HUB_L       = INNER_L + 2 * WALL_THICK; // 55.0 mm
HUB_W       = INNER_W + 2 * WALL_THICK; // 25.0 mm
HUB_H       = FLOOR_THICK + INNER_H + 2.5; // 15.0 mm
R_CORNER    = 3.0;    // Corner fillet radius (mm)

// --- PCB Origin Offset Inside Tub Cavity ---
X0          = WALL_THICK + PCB_CLR; // 2.5 mm
Y0          = WALL_THICK + PCB_CLR; // 2.5 mm

// --- South Face (Y = 0) 3x USB-C Ports: J3 (PHONE), J4 (DONGLE), J5 (MEDIA) ---
SOUTH_PORT_X = [
    X0 + 7.82,  // J3: PHONE_CHARGE (KiCad X=33.82 -> 7.82 mm)
    X0 + 19.82, // J4: DONGLE       (KiCad X=45.82 -> 19.82 mm)
    X0 + 31.82  // J5: MEDIA        (KiCad X=57.82 -> 31.82 mm)
];
SOUTH_LABELS = ["PHONE", "DONGLE", "MEDIA"];

// --- North Face (Y = HUB_W) 2x USB-C Ports: J2 (FRONT_NODE), J1 (SKYLINE_HOST) ---
NORTH_PORT_X = [
    X0 + 13.68, // J2: FRONT_NODE   (KiCad X=39.68 -> 13.68 mm)
    X0 + 27.18  // J1: SKYLINE_HOST (KiCad X=53.18 -> 27.18 mm)
];
NORTH_LABELS = ["FRONT", "HOST"];

PORT_USBC_W = 10.2;   // USB-C receptacle cutout width (mm)
PORT_USBC_H = 4.6;    // USB-C receptacle cutout height (mm)
PORT_Z_CTR  = FLOOR_THICK + STANDOFF_H + PCB_T + 1.6; // 7.7 mm

// --- Mounting Boss Locations (KiCad H1 at X=30->4.0, H2 at X=72->46.0, Y=16.0) ---
BOSS_X1     = X0 + 4.0;   // 6.5 mm
BOSS_X2     = X0 + 46.0;  // 48.5 mm
BOSS_Y      = Y0 + 16.0;  // 18.5 mm

module usbc_cutout(depth) {
    hull() {
        translate([1.2, 0, 1.2])
            rotate([-90, 0, 0]) cylinder(r=1.2, h=depth, center=false);
        translate([PORT_USBC_W - 1.2, 0, 1.2])
            rotate([-90, 0, 0]) cylinder(r=1.2, h=depth, center=false);
        translate([1.2, 0, PORT_USBC_H - 1.2])
            rotate([-90, 0, 0]) cylinder(r=1.2, h=depth, center=false);
        translate([PORT_USBC_W - 1.2, 0, PORT_USBC_H - 1.2])
            rotate([-90, 0, 0]) cylinder(r=1.2, h=depth, center=false);
    }
}

// -----------------------------------------------------------------------------
// 1. Lower Enclosure Tub (Unterteil)
// -----------------------------------------------------------------------------
module glovebox_hub_tub() {
    difference() {
        // Outer rounded body (55.0 x 25.0 mm)
        hull() {
            translate([R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 3.0, center=false);
            translate([HUB_L - R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 3.0, center=false);
            translate([R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 3.0, center=false);
            translate([HUB_L - R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 3.0, center=false);
        }

        // Inner Electronics Cavity (51.0 x 21.0 mm)
        translate([WALL_THICK, WALL_THICK, FLOOR_THICK]) {
            cube([INNER_L, INNER_W, HUB_H], center=false);
        }

        // 3x South Face USB-C Cutouts (Y = 0: PHONE, DONGLE, MEDIA)
        for (px = SOUTH_PORT_X) {
            translate([px - PORT_USBC_W/2.0, -1.0, PORT_Z_CTR - PORT_USBC_H/2.0])
                usbc_cutout(WALL_THICK + 2.0);
        }

        // 2x North Face USB-C Cutouts (Y = HUB_W: FRONT, HOST)
        for (px = NORTH_PORT_X) {
            translate([px - PORT_USBC_W/2.0, HUB_W - WALL_THICK - 1.0, PORT_Z_CTR - PORT_USBC_H/2.0])
                usbc_cutout(WALL_THICK + 2.0);
        }

        // Debossed Poka-Yoke Labels above South ports
        for (i = [0 : len(SOUTH_PORT_X) - 1]) {
            translate([SOUTH_PORT_X[i], 0.4, PORT_Z_CTR + PORT_USBC_H/2.0 + 1.2])
                rotate([90, 0, 0])
                    linear_extrude(height=0.6)
                        text(SOUTH_LABELS[i], size=1.7, halign="center", valign="center", font="Liberation Sans:style=Bold");
        }

        // Bottom 3M Dual-Lock Recess (1.0 mm deep on underside)
        translate([8.0, 4.0, -0.1])
            cube([HUB_L - 16.0, HUB_W - 8.0, 1.1], center=false);
    }

    // 2x Internal PCB Support Bosses with M2.5 threaded pilot holes (KiCad H1 & H2)
    for (bx = [BOSS_X1, BOSS_X2]) {
        difference() {
            translate([bx, BOSS_Y, FLOOR_THICK])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
            translate([bx, BOSS_Y, FLOOR_THICK - 0.5])
                cylinder(r=1.1, h=STANDOFF_H + 1.0, center=false);
        }
    }
}

// -----------------------------------------------------------------------------
// 2. Upper Lid with Snap Latch & Passive Ventilation
// -----------------------------------------------------------------------------
module glovebox_hub_lid() {
    difference() {
        // Outer rounded lid plate (55.0 x 25.0 mm)
        hull() {
            translate([R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=3.0, center=false);
            translate([HUB_L - R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=3.0, center=false);
            translate([R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=3.0, center=false);
            translate([HUB_L - R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=3.0, center=false);
        }

        // 2x M2.5 Countersunk Screw Holes (aligning with PCB bosses H1 & H2)
        for (bx = [BOSS_X1, BOSS_X2]) {
            translate([bx, BOSS_Y, -1.0])
                cylinder(r=1.4, h=6.0, center=false);
            translate([bx, BOSS_Y, 1.4])
                cylinder(r1=1.4, r2=2.8, h=1.8, center=false);
        }

        // Passive Heat Dissipation Slots over East USB2514B Hub IC area
        for (sx = [12.0 : 5.5 : HUB_L - 12.0]) {
            translate([sx, HUB_W/2.0 - 4.5, -1.0])
                cube([1.6, 9.0, 5.0], center=false);
        }

        // Debossed Title
        translate([HUB_L/2.0, 4.2, 2.5])
            linear_extrude(height=0.6)
                text("OMB HUB 05B", size=2.0, halign="center", valign="center", font="Liberation Sans:style=Bold");
    }

    // Interlocking Lip on Lid Underside (inserts 1.8mm into tub)
    difference() {
        translate([WALL_THICK + 0.2, WALL_THICK + 0.2, -1.8])
            cube([INNER_L - 0.4, INNER_W - 0.4, 1.8], center=false);
        translate([WALL_THICK + 1.4, WALL_THICK + 1.4, -2.0])
            cube([INNER_L - 2.8, INNER_W - 2.8, 2.2], center=false);
    }
}

// -----------------------------------------------------------------------------
// 3. Complete Assembly Preview
// -----------------------------------------------------------------------------
module glovebox_power_injection_hub_assembly() {
    color([0.20, 0.22, 0.24])
        glovebox_hub_tub();

    color([0.28, 0.30, 0.34], 0.95)
        translate([0, 0, HUB_H - 1.0])
            glovebox_hub_lid();
}

// Standalone execution preview
glovebox_power_injection_hub_assembly();
