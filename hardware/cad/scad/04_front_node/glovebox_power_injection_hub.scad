// =============================================================================
// OpenMotorBridge - 5-Port Glovebox Media & Power-Injection Hub
// =============================================================================
// File: hardware/cad/scad/04_front_node/glovebox_power_injection_hub.scad
// Description: Compact power-injection and USB data hub tailored for the right
//              glovebox (Media Compartment) of Harley-Davidson Touring & Bagger
//              motorcycles (Road Glide, Street Glide, CVO, CVO ST 2024+):
//              1. Upstream Port: Connects to OEM Harley USB-C socket (Skyline OS / Boom! Box).
//              2. DC Power In: 12V Bordnetz feed from OMB Backbone (SC8102 Buck-Boost).
//              3. Port 1 (Smartphone Fast Charge): 30W USB-PD (thermal-safe for closed glovebox).
//              4. Port 2 (CarPlay Dongle): 10W geschalteter VBUS für Wireless CP/AA Adapter.
//              5. Port 3 (Media Pass-Through): High-Speed USB 2.0 for OEM USB Flash Drives/Updates.
// =============================================================================

$fn = 32;

HUB_L       = 72.0;   // Outer enclosure length (mm)
HUB_W       = 46.0;   // Outer enclosure width (mm)
HUB_H       = 22.0;   // Outer enclosure height (mm)
WALL_THICK  = 2.2;    // Robust automotive shell wall thickness (mm)
R_CORNER    = 3.0;    // Ergonomic corner radius (mm)

// 1. Lower Enclosure Tub (Unterteil)
module glovebox_hub_tub() {
    difference() {
        // Outer rounded body
        hull() {
            translate([R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 4.0, center=false);
            translate([HUB_L - R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 4.0, center=false);
            translate([R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 4.0, center=false);
            translate([HUB_L - R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=HUB_H - 4.0, center=false);
        }

        // Inner Electronics Cavity
        translate([WALL_THICK, WALL_THICK, WALL_THICK]) {
            cube([HUB_L - 2*WALL_THICK, HUB_W - 2*WALL_THICK, HUB_H], center=false);
        }

        // --- Port Cutouts on Front Face (Y = 0) ---
        // Port 1: 30W USB-PD Type-C Port (Smartphone Fast Charge)
        translate([16.0, -1.0, 8.5])
            cube([10.0, WALL_THICK + 2.0, 4.5], center=false);

        // Port 2: 10W USB-A Port (Wireless CarPlay / Android Auto Dongle)
        translate([32.0, -1.0, 7.0])
            cube([13.5, WALL_THICK + 2.0, 6.5], center=false);

        // Port 3: Media USB Pass-Through (USB Stick / OEM Update)
        translate([52.0, -1.0, 7.0])
            cube([13.5, WALL_THICK + 2.0, 6.5], center=false);

        // --- Rear Face Cutouts (Y = HUB_W) ---
        // Upstream USB-C Port to Harley Head Unit (Skyline OS / Boom! Box)
        translate([18.0, HUB_W - WALL_THICK - 1.0, 8.5])
            cube([10.0, WALL_THICK + 2.0, 4.5], center=false);

        // 12V DC Power Feed (2-Pin Molex Micro-Fit / JST-JWPF waterproof)
        translate([42.0, HUB_W - WALL_THICK - 1.0, 7.5])
            cube([11.0, WALL_THICK + 2.0, 7.0], center=false);

        // 4x Corner M2.5 Screw Boss Bores
        for (dx = [6.0, HUB_L - 6.0]) {
            for (dy = [6.0, HUB_W - 6.0]) {
                translate([dx, dy, WALL_THICK])
                    cylinder(r=1.3, h=HUB_H, center=false);
            }
        }

        // Bottom 3M Dual-Lock Recess (1.2 mm deep)
        translate([15.0, 10.0, -0.1])
            cube([HUB_L - 30.0, HUB_W - 20.0, 1.3], center=false);
    }

    // 4x Internal PCB Support Bosses with M2 threaded pilot holes
    for (dx = [6.0, HUB_L - 6.0]) {
        for (dy = [6.0, HUB_W - 6.0]) {
            difference() {
                translate([dx, dy, WALL_THICK])
                    cylinder(r=3.2, h=4.0, center=false);
                translate([dx, dy, WALL_THICK - 0.5])
                    cylinder(r=1.1, h=5.0, center=false);
            }
        }
    }
}

// 2. Upper Lid with Thermal Ventilation Louvers
module glovebox_hub_lid() {
    difference() {
        // Outer rounded lid plate
        hull() {
            translate([R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=4.0, center=false);
            translate([HUB_L - R_CORNER, R_CORNER, 0])
                cylinder(r=R_CORNER, h=4.0, center=false);
            translate([R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=4.0, center=false);
            translate([HUB_L - R_CORNER, HUB_W - R_CORNER, 0])
                cylinder(r=R_CORNER, h=4.0, center=false);
        }

        // 4x Corner M2.5 Countersunk Screw Holes
        for (dx = [6.0, HUB_L - 6.0]) {
            for (dy = [6.0, HUB_W - 6.0]) {
                translate([dx, dy, -1.0])
                    cylinder(r=1.4, h=6.0, center=false);
                translate([dx, dy, 2.2])
                    cylinder(r1=1.4, r2=2.8, h=2.0, center=false);
            }
        }

        // Slanted Passive Heat Dissipation Slots (Thermal protection in glovebox)
        for (sx = [20.0 : 5.0 : HUB_L - 20.0]) {
            translate([sx, 12.0, -1.0])
                cube([2.0, HUB_W - 24.0, 6.0], center=false);
        }
    }

    // Alignment Rim on Lid Underside (Interlocking into tub)
    difference() {
        translate([WALL_THICK + 0.3, WALL_THICK + 0.3, -2.0])
            cube([HUB_L - 2*(WALL_THICK + 0.3), HUB_W - 2*(WALL_THICK + 0.3), 2.0], center=false);
        translate([WALL_THICK + 1.8, WALL_THICK + 1.8, -2.5])
            cube([HUB_L - 2*(WALL_THICK + 1.8), HUB_W - 2*(WALL_THICK + 1.8), 3.0], center=false);
    }
}

// 3. Complete Assembly Preview
module glovebox_power_injection_hub_assembly() {
    color([0.2, 0.2, 0.22])
        glovebox_hub_tub();

    color([0.3, 0.3, 0.35], 0.95)
        translate([0, 0, HUB_H - 1.0])
            glovebox_hub_lid();
}

// Standalone execution preview
glovebox_power_injection_hub_assembly();
