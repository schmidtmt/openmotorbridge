// =============================================================================
// OpenMotorBridge - PCBA 05B Handschuhfach-Hub Gehäuse (100% Parity)
// =============================================================================
// File: hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad
// Description: Ultra-slim media compartment power-injection and USB data hub
//              custom-tailored for PCBA 05B (76.0 x 20.0 mm).
//              Designed for the right glovebox of Harley-Davidson Touring & Bagger
//              motorcycles (Road Glide, Street Glide, CVO, CVO ST 2024+):
//              1. J1 [HOST]: Connects to OEM Harley USB-C socket (Skyline OS / Boom! Box).
//              2. J2 [NODE]: Downstream link to Universal Front Node PCBA 05.
//              3. J3 [PHONE]: 15W/30W Fast-Charge port for smartphone inside compartment.
//              4. J4 [DONGLE]: Gated 10W USB port for wireless CarPlay / Android Auto adapter.
//              5. J5 [MEDIA]: High-Speed USB 2.0 pass-through for USB thumb drives & updates.
// =============================================================================

$fn = 32;

// --- PCB 05B Physical Dimensions ---
PCB_L       = 76.0;   // PCB length (mm)
PCB_W       = 20.0;   // PCB width (mm)
PCB_T       = 1.6;    // PCB substrate thickness (mm)
PCB_CLR     = 0.5;    // Internal perimeter clearance (mm)

// --- Enclosure Outer Envelope ---
WALL_THICK  = 2.0;    // Robust PA12-MJF shell thickness (mm)
FLOOR_THICK = 2.0;    // Floor thickness (mm)
STANDOFF_H  = 2.5;    // PCB bottom component clearance (mm)
INNER_L     = PCB_L + 2 * PCB_CLR; // 77.0 mm
INNER_W     = PCB_W + 2 * PCB_CLR; // 21.0 mm
INNER_H     = 10.5;   // Interior clearance height (mm)

HUB_L       = INNER_L + 2 * WALL_THICK; // 81.0 mm
HUB_W       = INNER_W + 2 * WALL_THICK; // 25.0 mm
HUB_H       = FLOOR_THICK + INNER_H + 2.5; // 15.0 mm
R_CORNER    = 3.0;    // Corner fillet radius (mm)

// --- USB-C Port Center Coordinates (matching KiCad footprints in row at 12.0mm pitch) ---
// PCB origin offset inside tub cavity:
X0          = WALL_THICK + PCB_CLR; // 2.5 mm
Y0          = WALL_THICK + PCB_CLR; // 2.5 mm

PORT_X_LIST = [
    X0 + 9.82,  // J1: SKYLINE_HOST (12.32 mm)
    X0 + 21.82, // J2: FRONT_NODE   (24.32 mm)
    X0 + 33.82, // J3: PHONE_CHARGE (36.32 mm)
    X0 + 45.82, // J4: DONGLE       (48.32 mm)
    X0 + 57.82  // J5: MEDIA        (60.32 mm)
];

PORT_LABELS = ["HOST", "NODE", "PHONE", "DONGLE", "MEDIA"];

PORT_USBC_W = 10.2;   // USB-C receptacle cutout width (mm)
PORT_USBC_H = 4.6;    // USB-C receptacle cutout height (mm)
PORT_Z_CTR  = FLOOR_THICK + STANDOFF_H + PCB_T + 1.6; // 7.7 mm

// --- Mounting Boss Locations (KiCad H1 & H2 at X=4.0 and X=72.0, Y=16.0) ---
BOSS_X1     = X0 + 4.0;   // 6.5 mm
BOSS_X2     = X0 + 72.0;  // 74.5 mm
BOSS_Y      = Y0 + 16.0;  // 18.5 mm

// -----------------------------------------------------------------------------
// 1. Lower Enclosure Tub (Unterteil)
// -----------------------------------------------------------------------------
module glovebox_hub_tub() {
    difference() {
        // Outer rounded body
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

        // Inner Electronics Cavity
        translate([WALL_THICK, WALL_THICK, FLOOR_THICK]) {
            cube([INNER_L, INNER_W, HUB_H], center=false);
        }

        // 5x USB-C Receptacle Port Cutouts on Front Face (Y = 0)
        for (px = PORT_X_LIST) {
            translate([px - PORT_USBC_W/2.0, -1.0, PORT_Z_CTR - PORT_USBC_H/2.0])
                hull() {
                    translate([1.2, 0, 1.2])
                        rotate([-90, 0, 0]) cylinder(r=1.2, h=WALL_THICK + 2.0, center=false);
                    translate([PORT_USBC_W - 1.2, 0, 1.2])
                        rotate([-90, 0, 0]) cylinder(r=1.2, h=WALL_THICK + 2.0, center=false);
                    translate([1.2, 0, PORT_USBC_H - 1.2])
                        rotate([-90, 0, 0]) cylinder(r=1.2, h=WALL_THICK + 2.0, center=false);
                    translate([PORT_USBC_W - 1.2, 0, PORT_USBC_H - 1.2])
                        rotate([-90, 0, 0]) cylinder(r=1.2, h=WALL_THICK + 2.0, center=false);
                }
        }

        // Debossed Poka-Yoke Labels above ports on Front Lip (0.5 mm deep)
        for (i = [0 : len(PORT_X_LIST) - 1]) {
            translate([PORT_X_LIST[i], 0.4, PORT_Z_CTR + PORT_USBC_H/2.0 + 1.4])
                rotate([90, 0, 0])
                    linear_extrude(height=0.6)
                        text(PORT_LABELS[i], size=1.8, halign="center", valign="center", font="Liberation Sans:style=Bold");
        }

        // Bottom 3M Dual-Lock Recess (1.0 mm deep on underside)
        translate([12.0, 4.0, -0.1])
            cube([HUB_L - 24.0, HUB_W - 8.0, 1.1], center=false);
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
        // Outer rounded lid plate
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

        // Slanted Passive Heat Dissipation Slots (Thermal safety for 30W charging)
        for (sx = [18.0 : 6.0 : HUB_L - 18.0]) {
            translate([sx, HUB_W/2.0 - 5.0, -1.0])
                cube([1.8, 10.0, 5.0], center=false);
        }

        // Debossed Logo / Title
        translate([HUB_L/2.0, HUB_W - 3.8, 2.5])
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
