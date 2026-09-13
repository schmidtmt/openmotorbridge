// =============================================================================
// OpenMotorBridge - 2-in-1 LoRa Smart-Keyfob & Magnetic Cassette Key
// =============================================================================
// File: hardware/cad/scad/05_accessories/smart_keyfob_pager.scad
// Description: Multi-function pocket keyfob combining:
//   1. LoRa 868 MHz Silent Alarm Pager (SX1262 + LRA Haptic Motor + RGB Status)
//   2. N52 Neodymium Magnetic Key (20x10x5 mm) to unlock Pod Cartridge sleds
//   3. MagSafe Snap-Alignment Ring for Qi Wireless Charging on PCBA 06 Cockpit Dock
//   4. 316L Stainless Steel Keyring Eyelet for motorcycle key harness
//   5. Mu-Metal / Soft Iron Flux Shield (0.5 mm) protecting internal RF and battery
// =============================================================================

include <../00_common/parameters.scad>;

// Render Mode Toggle
EXPLODED_VIEW = false; // Set to true to inspect internal components and flux shield

// Dimensional Parameters
FOB_L = 58.0;  // Overall length (mm)
FOB_W = 34.0;  // Overall width (mm)
FOB_H = 13.0;  // Overall thickness (mm)
FOB_WALL = 1.8; // PA12-MJF structural wall thickness (mm)
CORNER_R = 6.0; // Ergonomic corner radius (mm)

// Magnet Key Dimensions (Side-Mounted for precise pod contact)
MAG_L = 20.0;
MAG_W = 10.0;
MAG_H = 5.0;

// MagSafe Magnetic Ring Dimensions (Back Face)
MAGSAFE_OD = 28.0;
MAGSAFE_ID = 22.0;
MAGSAFE_DEPTH = 1.0;

// Keyring Eyelet
EYELET_OD = 9.0;
EYELET_ID = 4.5;
EYELET_THICK = 3.5;

// Helper: Rounded Box
module rounded_box(l, w, h, r) {
    translate([r, r, 0])
        minkowski() {
            cube([l - 2*r, w - 2*r, h - 1.0]);
            cylinder(r=r, h=1.0, $fn=36);
        }
}

// 1. Lower Housing Shell (Matte Anthracite PA12-MJF)
module fob_lower_shell() {
    difference() {
        // Outer body
        rounded_box(FOB_L, FOB_W, FOB_H / 2.0, CORNER_R);

        // Internal Cavity
        translate([FOB_WALL, FOB_WALL, FOB_WALL])
            rounded_box(FOB_L - 2*FOB_WALL, FOB_W - 2*FOB_WALL, FOB_H / 2.0, CORNER_R - FOB_WALL);

        // MagSafe Alignment Pocket on Bottom Exterior
        translate([FOB_L / 2.0 - 4.0, FOB_W / 2.0, -0.1])
            difference() {
                cylinder(r=MAGSAFE_OD / 2.0, h=MAGSAFE_DEPTH + 0.1, $fn=48);
                cylinder(r=MAGSAFE_ID / 2.0, h=MAGSAFE_DEPTH + 0.2, $fn=48);
            }

        // Magnet Key Lateral Pocket (Recessed on narrow side, X-centered)
        translate([FOB_L / 2.0 - MAG_L / 2.0 - 4.0, FOB_W - MAG_W + 0.1, FOB_WALL])
            cube([MAG_L + 0.4, MAG_W, MAG_H + 0.4]);

        // Keyring Loop Cutout at Tail
        translate([FOB_L - 4.0, FOB_W / 2.0, -0.5])
            cylinder(r=EYELET_ID / 2.0, h=FOB_H + 1.0, $fn=32);
    }
}

// 2. Upper Housing Shell (With Indicator Diffuser Apertures)
module fob_upper_shell() {
    difference() {
        rounded_box(FOB_L, FOB_W, FOB_H / 2.0, CORNER_R);

        // Internal Hollow
        translate([FOB_WALL, FOB_WALL, -0.1])
            rounded_box(FOB_L - 2*FOB_WALL, FOB_W - 2*FOB_WALL, FOB_H / 2.0 - FOB_WALL + 0.1, CORNER_R - FOB_WALL);

        // RGB Status LED Light Pipe Bore (Ø 2.5 mm)
        translate([12.0, FOB_W / 2.0, FOB_H / 2.0 - 2.0])
            cylinder(r=1.25, h=3.0, $fn=24);

        // Haptic Acoustic Relief Vent (Three 0.8 mm Micro-Holes)
        for (offset = [-2.5, 0, 2.5]) {
            translate([22.0, FOB_W / 2.0 + offset, FOB_H / 2.0 - 2.0])
                cylinder(r=0.45, h=3.0, $fn=16);
        }

        // Keyring Loop Cutout at Tail
        translate([FOB_L - 4.0, FOB_W / 2.0, -0.5])
            cylinder(r=EYELET_ID / 2.0, h=FOB_H + 1.0, $fn=32);
    }
}

// 3. N52 Neodymium Permanent Magnet Block (20x10x5 mm)
module magnet_block() {
    color("#ff453a") { // High-Energy Rare Earth Red
        difference() {
            cube([MAG_L, MAG_W, MAG_H], center=false);
            // Laser Engraved North Pole Stripe
            translate([MAG_L / 2.0 - 0.5, -0.1, MAG_H / 2.0 - 1.5])
                cube([1.0, 0.4, 3.0]);
        }
    }
}

// 4. Soft Iron / Mu-Metal Magnetic Shield (0.5 mm)
module flux_shield_plate() {
    color("#94a3b8") { // Ferromagnetic Steel
        translate([0, 0, 0])
            cube([MAG_L + 2.0, 0.5, MAG_H + 2.0]);
    }
}

// 5. Internal Electronics PCBA
module internal_pcba() {
    color("#0d9488") { // Green PCB FR4
        translate([6.0, 5.0, 0])
            cube([FOB_L - 20.0, FOB_W - 16.0, 1.0]);
    }

    // Semtech SX1262 LoRa Transceiver IC (QFN-24)
    color("#1e293b")
        translate([14.0, 8.0, 1.0])
            cube([4.0, 4.0, 1.0]);

    // 868 MHz Miniature Helical Chip Antenna
    color("#b45309")
        translate([8.0, 16.0, 1.0])
            cube([10.0, 3.2, 2.0]);

    // LRA Haptic Vibration Motor (Ø 10 mm Coin)
    color("silver")
        translate([32.0, FOB_W / 2.0 - 5.0, 1.0])
            cylinder(r=5.0, h=3.0, $fn=32);

    // 180 mAh LiPo Pouch Cell (25 x 18 x 3.8 mm)
    color("#334155")
        translate([10.0, 6.0, -4.0])
            cube([25.0, 18.0, 3.8]);
}

// 6. Stainless Steel 316L Keyring Eyelet
module keyring_eyelet() {
    color("silver") {
        translate([FOB_L - 4.0, FOB_W / 2.0, FOB_H / 2.0])
            difference() {
                cylinder(r=EYELET_OD / 2.0, h=EYELET_THICK, center=true, $fn=36);
                cylinder(r=EYELET_ID / 2.0, h=EYELET_THICK + 0.4, center=true, $fn=36);
            }
    }
}

// 7. Protective TPU Shock-Absorbing Rim (Orange Accent)
module tpu_protective_rim() {
    color("#ff9f0a", 0.9) {
        difference() {
            rounded_box(FOB_L + 1.6, FOB_W + 1.6, FOB_H + 0.8, CORNER_R + 0.8);
            translate([0.8, 0.8, -0.5])
                rounded_box(FOB_L, FOB_W, FOB_H + 2.0, CORNER_R);
            // Magnet access slot on side
            translate([FOB_L / 2.0 - MAG_L / 2.0 - 5.0, FOB_W - 2.0, -1.0])
                cube([MAG_L + 2.0, 5.0, FOB_H + 3.0]);
        }
    }
}

// 8. Complete Assembly
module smart_keyfob_assembly() {
    z_expl = EXPLODED_VIEW ? 18.0 : 0.0;

    // Lower Shell
    color("#222831")
        translate([0, 0, 0])
            fob_lower_shell();

    // Internal Magnet Key
    translate([FOB_L / 2.0 - MAG_L / 2.0 - 4.0, FOB_W - MAG_W, FOB_WALL + 0.2])
        magnet_block();

    // Magnetic Flux Shield Plate (Directly behind magnet)
    translate([FOB_L / 2.0 - MAG_L / 2.0 - 5.0, FOB_W - MAG_W - 0.6, FOB_WALL])
        flux_shield_plate();

    // Internal PCBA & Battery
    translate([0, 0, FOB_H / 2.0 - 1.0])
        internal_pcba();

    // 316L Eyelet
    keyring_eyelet();

    // Upper Shell (Exploded if toggled)
    color("#1e293b")
        translate([0, 0, FOB_H / 2.0 + z_expl])
            fob_upper_shell();

    // TPU Rim
    translate([-0.8, -0.8, -0.4])
        tpu_protective_rim();
}

// Render Master Scene
smart_keyfob_assembly();
