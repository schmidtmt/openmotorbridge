// =============================================================================
// OpenMotorBridge - 2-in-1 LoRa Smart-Keyfob & Magnetic Cassette Key
// =============================================================================
// File: hardware/cad/scad/05_accessories/smart_keyfob_pager.scad
// Description: Multi-function pocket keyfob combining:
//   1. LoRa 868 MHz Silent Alarm Pager (SX1262 + LRA Haptic Motor + RGB Status)
//   2. N52 Neodymium Magnetic Key (20x10x5 mm) to unlock Pod Cartridge sleds
//   3. MagSafe Snap-Alignment Ring for Qi Wireless Charging on PCBA 06 Cockpit Dock
//   4. 316L Stainless Steel Keyring Eyelet in solid isolated waterproof bulkhead
//   5. Mu-Metal / Soft Iron Flux Shield (0.5 mm) protecting internal RF and battery
//   6. Dual Tactile Sealed Keys (SW1: ARM/MUTE, SW2: SOS) via Silicone/TPU Membrane
//   7. Formschlüssige PCB-Klemmung (Auflageschultern & Zentrierpins, schraubenlos)
//   8. IP67 Waterproofing: Nut-und-Feder Labyrinthdichtung, ePTFE Akustikmembran
// =============================================================================

include <../00_common/parameters.scad>;

// Render Mode Toggle
EXPLODED_VIEW = false;

// Dimensional Parameters
FOB_L = 58.0;   // Overall length (mm)
FOB_W = 34.0;   // Overall width (mm)
FOB_H = 13.0;   // Overall thickness (mm)
FOB_WALL = 1.8; // Structural shell wall thickness (mm)
CORNER_R = 6.0; // Outer ergonomic corner radius (mm)

// Internal Cavity Parameters (Strictly bounded to isolate keyring)
CAV_X_START = 3.5;
CAV_X_END   = 44.5;
CAV_L       = CAV_X_END - CAV_X_START; // 41.0 mm (Leaves 13.5 mm solid tail for eyelet)
CAV_W       = FOB_W - 2 * FOB_WALL;    // 30.4 mm

// PCBA 07 Parameters (38.0 x 19.0 x 1.0 mm, matches KiCad Edge.Cuts)
PCB_L = 38.0;
PCB_W = 19.0;
PCB_T = 1.0;
PCB_X = 5.0;  // X position in fob (5.0 to 43.0 mm)
PCB_Y = 4.0;  // Y position in fob (4.0 to 23.0 mm)
PCB_Z = 5.0;  // Z position (resting on shelf at Z=5.0)

// Magnet Key Dimensions (Lateral pocket, shielded)
MAG_L = 20.0;
MAG_W = 10.0;
MAG_H = 5.0;

// MagSafe Magnetic Ring Dimensions (Back Face)
MAGSAFE_OD = 28.0;
MAGSAFE_ID = 22.0;
MAGSAFE_DEPTH = 1.0;

// Keyring Eyelet Dimensions (Tail Bulkhead)
EYELET_X = 52.5;
EYELET_Y = FOB_W / 2.0; // 17.0 mm
EYELET_OD = 8.5;
EYELET_ID = 4.5;
EYELET_THICK = 4.5;

// Exact KiCad Component Locations on PCBA 07 (mapped to Fob Coordinates)
// KiCad Origin (100.0, 70.0) -> Fob Origin (PCB_X, PCB_Y)
// X_fob = PCB_X + (X_kicad - 100.0)
// Y_fob = PCB_Y + (Y_kicad - 70.0)
// SW1 (BTN_ARM): KiCad (125.5, 86.75) -> Fob (30.5, 20.75) -> inverted Y for outer ergonomic layout
SW1_X = PCB_X + 25.5; // 30.5 mm
SW1_Y = PCB_Y + 5.5;  // 9.5 mm (Ergonomic outer edge placement)

SW2_X = PCB_X + 34.0; // 39.0 mm
SW2_Y = PCB_Y + 5.5;  // 9.5 mm (Ergonomic outer edge placement)

LED_X = PCB_X + 35.9; // 40.9 mm (Near SW2)
LED_Y = PCB_Y + 11.5; // 15.5 mm

BUZZER_X = PCB_X + 31.25; // 36.25 mm
BUZZER_Y = PCB_Y + 16.5;  // 20.5 mm

// P_BAT Battery Solder Pads (KiCad 132.34, 81.0 on F.Cu)
P_BAT_X = PCB_X + 32.34; // 37.34 mm
P_BAT_Y = PCB_Y + 11.0;  // 15.0 mm

// Helper: Rounded Box
module rounded_box(l, w, h, r) {
    translate([r, r, 0])
        minkowski() {
            cube([max(0.1, l - 2*r), max(0.1, w - 2*r), max(0.1, h - 1.0)]);
            cylinder(r=r, h=1.0, $fn=36);
        }
}

// 1. Lower Housing Shell (Matte Anthracite PA12-MJF with PCB shelves, battery pocket & anti-pinch cable trench)
module fob_lower_shell() {
    union() {
        difference() {
            union() {
                // Outer Main Body
                rounded_box(FOB_L, FOB_W, FOB_H / 2.0, CORNER_R);

                // Tongue Seal Lip (Labyrinthdichtung: 0.8 mm high along parting line)
                translate([FOB_WALL - 0.4, FOB_WALL - 0.4, FOB_H / 2.0])
                    difference() {
                        rounded_box(FOB_L - 2*(FOB_WALL - 0.4), FOB_W - 2*(FOB_WALL - 0.4), 0.9, CORNER_R - 1.2);
                        translate([0.8, 0.8, -0.1])
                            rounded_box(FOB_L - 2*(FOB_WALL + 0.4), FOB_W - 2*(FOB_WALL + 0.4), 1.2, CORNER_R - 2.0);
                    }
            }

            // Lower Battery Compartment Recess (for 25x18x3.8 mm LiPo pouch cell at bottom)
            translate([PCB_X + 1.5, PCB_Y + 0.5, 1.2])
                cube([26.0, 18.0, 4.0]);

            // Form-Fitting Stepped PCB Well (Cut down to Z=5.0 mm with 0.2 mm perimeter clearance)
            // Leaves precision resting ledge at Z = 5.0 mm on all 4 sides!
            translate([PCB_X - 0.2, PCB_Y - 0.2, PCB_Z])
                cube([PCB_L + 0.4, PCB_W + 0.4, FOB_H / 2.0 + 0.1]);

            // Dedicated Anti-Pinch Battery Cable Routing Trench (Kabelbucht / Freisparung)
            // Generous 7.0 mm wide, 1.8 mm deep recess below PCB level (Z=3.2 to 6.2 mm)
            // Extends from battery terminal (X=31) past the PCB right edge (X=43) to tail bulkhead (X=44.5)
            // Prevents any pinching or crushing of AWG 28/30 silicone battery wires between PCB & shell!
            translate([PCB_X + 26.0, P_BAT_Y - 3.5, 3.2])
                cube([CAV_X_END - (PCB_X + 26.0), 7.0, 3.2]);

            // Magnet Key Compartment & Shield Slot (Recessed on lateral long side)
            translate([FOB_L / 2.0 - MAG_L / 2.0 - 4.0, FOB_W - MAG_W - 0.6, FOB_WALL])
                cube([MAG_L + 0.4, MAG_W + 0.8, MAG_H + 0.4]);

            // MagSafe Magnetic Alignment Pocket on Bottom Exterior
            translate([FOB_L / 2.0 - 4.0, FOB_W / 2.0, -0.1])
                difference() {
                    cylinder(r=MAGSAFE_OD / 2.0, h=MAGSAFE_DEPTH + 0.1, $fn=48);
                    cylinder(r=MAGSAFE_ID / 2.0, h=MAGSAFE_DEPTH + 0.2, $fn=48);
                }

            // Keyring Bushing Bore in Solid Bulkhead at Tail (Hermetically isolated from cavity!)
            translate([EYELET_X, EYELET_Y, -0.5])
                cylinder(r=EYELET_OD / 2.0 + 0.05, h=FOB_H + 1.0, $fn=36);
        }

        // PCB Corner Alignment Stops (R=0.55 mm, rising from Z=5.0 to 6.0 mm at outer corners)
        for (dx = [PCB_X + 1.2, PCB_X + PCB_L - 1.2]) {
            for (dy = [PCB_Y + 1.2, PCB_Y + PCB_W - 1.2]) {
                translate([dx, dy, PCB_Z])
                    cylinder(r=0.55, h=1.0, $fn=16);
            }
        }
    }
}

// 2. Upper Housing Shell (With Dual Button Apertures, LED Light Guide, Acoustic Vent & Clamping Ribs)
module fob_upper_shell() {
    difference() {
        // Outer Main Body
        rounded_box(FOB_L, FOB_W, FOB_H / 2.0, CORNER_R);

        // Internal Cavity Hollow (Stops at CAV_X_END = 44.5 mm)
        translate([CAV_X_START, FOB_WALL, -0.1])
            rounded_box(CAV_L, CAV_W, FOB_H / 2.0 - FOB_WALL + 0.1, 3.0);

        // Sealing Groove for Lower Shell Tongue Lip (0.9 mm wide, 1.0 mm deep)
        translate([FOB_WALL - 0.5, FOB_WALL - 0.5, -0.1])
            difference() {
                rounded_box(FOB_L - 2*(FOB_WALL - 0.5), FOB_W - 2*(FOB_WALL - 0.5), 1.1, CORNER_R - 1.1);
                translate([1.0, 1.0, -0.2])
                    rounded_box(FOB_L - 2*(FOB_WALL + 0.5), FOB_W - 2*(FOB_WALL + 0.5), 1.5, CORNER_R - 2.1);
            }

        // Dual Button Recess (Bezel well on top face)
        translate([SW1_X - 4.5, SW1_Y - 4.0, FOB_H / 2.0 - 1.8])
            rounded_box(SW2_X - SW1_X + 9.0, 8.0, 2.0, 2.0);

        // Button 1 Aperture (SW1: ARM / MUTE / UNLOCK - Ø 5.0 mm)
        translate([SW1_X, SW1_Y, -0.5])
            cylinder(r=2.5, h=FOB_H, $fn=24);

        // Button 2 Aperture (SW2: SOS / PAIR - Ø 4.5 mm)
        translate([SW2_X, SW2_Y, -0.5])
            cylinder(r=2.25, h=FOB_H, $fn=24);

        // RGB Status LED Light Pipe Bore (Ø 2.2 mm with stepped collar for PMMA lens)
        translate([LED_X, LED_Y, -0.5])
            cylinder(r=1.1, h=FOB_H, $fn=24);
        translate([LED_X, LED_Y, FOB_H / 2.0 - 0.8])
            cylinder(r=1.6, h=1.0, $fn=24);

        // Piezo Buzzer Acoustic Relief Vent (3x Ø 0.8 mm Micro-Holes positioned over LS1)
        for (offset = [-1.8, 0, 1.8]) {
            translate([BUZZER_X, BUZZER_Y + offset, -0.5])
                cylinder(r=0.45, h=FOB_H, $fn=16);
        }

        // Internal Hydrophobic ePTFE Acoustic Membrane Pocket (Ø 6.0 mm x 0.4 mm)
        translate([BUZZER_X, BUZZER_Y, -0.1])
            cylinder(r=3.2, h=0.5, $fn=24);

        // Keyring Bushing Bore in Solid Bulkhead at Tail
        translate([EYELET_X, EYELET_Y, -0.5])
            cylinder(r=EYELET_OD / 2.0 + 0.05, h=FOB_H + 1.0, $fn=36);
    }

    // Internal PCB Clamping Ribs (Press down on component-free margins of PCB at Z = 5.0 mm)
    // Rib 1: Along lower edge (Y = PCB_Y + 0.2 mm, X = 6.0 to 30.0 mm)
    translate([PCB_X + 1.0, PCB_Y + 0.2, 0])
        cube([24.0, 0.8, FOB_H / 2.0 - FOB_WALL]);

    // Rib 2: Along upper edge (Y = PCB_Y + PCB_W - 1.0 mm, X = 6.0 to 30.0 mm)
    // Keeps area X > 30.0 mm completely open for P_BAT wiring loop & buzzer acoustics!
    translate([PCB_X + 1.0, PCB_Y + PCB_W - 1.0, 0])
        cube([24.0, 0.8, FOB_H / 2.0 - FOB_WALL]);
}

// 3. Dual Tactile Silicone / TPU Sealing Membrane with Plungers (IP67 Sealed Keypad)
module silicone_button_keypad() {
    color("#ff9f0a") { // High-visibility waterproof orange elastomer
        // Base Sealing Gasket (0.8 mm thick sealing membrane)
        translate([SW1_X - 4.2, SW1_Y - 3.8, 0])
            rounded_box(SW2_X - SW1_X + 8.4, 7.6, 0.8, 1.5);

        // Button 1 (ARM / MUTE) - Raised tactile convex button cap
        translate([SW1_X, SW1_Y, 0.8]) {
            cylinder(r=2.3, h=1.4, $fn=24);
            // Tactile Lock / Arm Icon Steg
            translate([-1.2, -0.4, 1.4])
                cube([2.4, 0.8, 0.4]);
        }
        // Button 1 Downward Actuation Plunger (directly contacts SW1 Alps tactile switch)
        translate([SW1_X, SW1_Y, -3.7])
            cylinder(r=1.2, h=3.7, $fn=16);

        // Button 2 (SOS / PAIR) - Slightly recessed concave safety cap
        translate([SW2_X, SW2_Y, 0.8]) {
            cylinder(r=2.1, h=1.0, $fn=24);
            // Raised Center Tactile Pip
            translate([0, 0, 1.0])
                sphere(r=0.5, $fn=16);
        }
        // Button 2 Downward Actuation Plunger (contacts SW2 Alps switch)
        translate([SW2_X, SW2_Y, -3.7])
            cylinder(r=1.2, h=3.7, $fn=16);
    }
}

// 4. Optical PMMA Clear Diffuser Light Guide (Over WS2812B RGB LED)
module pmma_light_guide() {
    color("cyan", 0.75) {
        translate([LED_X, LED_Y, 0]) {
            cylinder(r=1.0, h=4.5, $fn=24);
            // Retention Flange at base
            translate([0, 0, 2.5])
                cylinder(r=1.5, h=0.8, $fn=24);
        }
    }
}

// 5. Hydrophobic ePTFE Acoustic Vent Membrane (Gore-Tex IP67 Patch)
module eptfe_acoustic_vent() {
    color("white", 0.8) {
        translate([BUZZER_X, BUZZER_Y, 0])
            cylinder(r=3.0, h=0.2, $fn=24);
    }
}

// 6. N52 Neodymium Permanent Magnet Block (20x10x5 mm) with North Pole Indicator
module magnet_block() {
    color("silver") {
        difference() {
            cube([MAG_L, MAG_W, MAG_H], center=false);
            translate([-0.1, MAG_W - 0.8, -0.1])
                rotate([45, 0, 0])
                    cube([MAG_L + 0.2, 1.5, 1.5]);
        }
    }
    color("crimson")
        translate([MAG_L / 2.0 - 1.0, MAG_W - 0.2, 0.8])
            cube([2.0, 0.8, MAG_H - 1.6]);
}

// 7. Mu-Metal / Soft Iron Magnetic Flux Shield (0.5 mm)
module flux_shield_plate() {
    color("#94a3b8") {
        cube([MAG_L + 2.0, 0.5, MAG_H + 2.0]);
    }
}

// 8. Authentic Internal Electronics PCBA 07 (Accurate KiCad Layout)
module internal_pcba(include_battery = true) {
    // Green FR4 PCB Substrate (38.0 x 19.0 x 1.0 mm)
    color("#0d9488") {
        translate([PCB_X, PCB_Y, 0])
            cube([PCB_L, PCB_W, PCB_T]);
    }

    // 868 MHz LoRa Antenna (ANT1 at KiCad 102.0, 73.5)
    color("#b45309")
        translate([PCB_X + 2.0, PCB_Y + 12.0, PCB_T])
            cube([8.0, 3.0, 1.5]);

    // 2.4 GHz BLE Ceramic Chip Antenna (ANT2 at KiCad 102.0, 85.5)
    color("#b45309")
        translate([PCB_X + 2.0, PCB_Y + 3.5, PCB_T])
            cube([6.5, 2.2, 1.2]);

    // Semtech SX1262 LoRa Transceiver IC (QFN-24, KiCad 114.5, 74.75)
    color("#1e293b")
        translate([PCB_X + 12.5, PCB_Y + 11.0, PCB_T])
            cube([4.0, 4.0, 0.9]);

    // Nordic nRF52840 Multiprotocol SoC (AQFN-73, KiCad 117.25, 84.0)
    color("#1e293b")
        translate([PCB_X + 15.0, PCB_Y + 3.0, PCB_T])
            cube([7.0, 7.0, 0.9]);

    // DRV2605L Haptic Driver (MSOP-10, KiCad 120.0, 73.6)
    color("#334155")
        translate([PCB_X + 19.0, PCB_Y + 12.5, PCB_T])
            cube([3.0, 3.0, 0.8]);

    // MAX17048 LiPo Fuel Gauge (WSON-6, KiCad 124.1, 78.9)
    color("#334155")
        translate([PCB_X + 23.0, PCB_Y + 8.5, PCB_T])
            cube([2.0, 2.0, 0.8]);

    // Alps SKRK SMD Tactile Switch 1 (SW1: BTN_ARM)
    color("#cbd5e1") {
        translate([SW1_X - 1.5, SW1_Y - 1.5, PCB_T]) {
            cube([3.0, 3.0, 1.5]);
            color("black")
                translate([1.5, 1.5, 1.5])
                    cylinder(r=0.7, h=0.4, $fn=16);
        }
    }

    // Alps SKRK SMD Tactile Switch 2 (SW2: BTN_SOS)
    color("#cbd5e1") {
        translate([SW2_X - 1.5, SW2_Y - 1.5, PCB_T]) {
            cube([3.0, 3.0, 1.5]);
            color("crimson")
                translate([1.5, 1.5, 1.5])
                    cylinder(r=0.7, h=0.4, $fn=16);
        }
    }

    // WS2812B-2020 Addressable RGB Status LED (D1, 2.0x2.0 mm)
    color("white")
        translate([LED_X - 1.0, LED_Y - 1.0, PCB_T])
            cube([2.0, 2.0, 0.7]);

    // CUI CPT-9019S Piezo Acoustic Buzzer (LS1, KiCad 131.25, 75.25)
    color("#475569")
        translate([BUZZER_X, BUZZER_Y, PCB_T])
            cylinder(r=4.5, h=1.9, $fn=32);

    // LRA Haptic Coin Motor (Ø 8.0 mm x 2.5 mm)
    color("silver")
        translate([PCB_X + 23.5, PCB_Y + 4.5, PCB_T])
            cylinder(r=4.0, h=2.5, $fn=24);

    // P_BAT SMD Solder Pads (0805 metric, KiCad 132.34, 81.0 on F.Cu)
    color("gold")
        translate([P_BAT_X - 1.0, P_BAT_Y - 0.7, PCB_T])
            cube([2.0, 1.4, 0.1]);

    if (include_battery) {
        // 180 mAh LiPo Pouch Cell (25 x 18 x 3.8 mm, beneath PCB)
        color("#334155")
            translate([PCB_X + 2.0, PCB_Y + 0.5, -3.8])
                cube([25.0, 18.0, 3.8]);

        // Qi Wireless Charging Receiver Coil (Ø 24 mm ultra-thin copper coil)
        color("#b45309", 0.8)
            translate([FOB_L / 2.0 - 4.0, FOB_W / 2.0, -4.0])
                cylinder(r=11.5, h=0.3, $fn=48);

        // Anti-Pinch Flexible Battery Wiring (AWG 28 Silicone: Red VBAT+, Black GND-)
        // Routes from lower battery bay through cable trench, around PCB edge to P_BAT pads
        // Red Wire (VBAT+)
        color("crimson") {
            translate([PCB_X + 25.0, P_BAT_Y - 0.7, -1.8])
                rotate([0, 90, 0])
                    cylinder(r=0.45, h=13.5, $fn=16);
            translate([PCB_X + 38.5, P_BAT_Y - 0.7, -1.8])
                cylinder(r=0.45, h=3.6, $fn=16);
            translate([P_BAT_X, P_BAT_Y - 0.7, 1.8])
                rotate([0, 90, 0])
                    cylinder(r=0.45, h=PCB_X + 38.5 - P_BAT_X, $fn=16);
            translate([P_BAT_X, P_BAT_Y - 0.7, PCB_T])
                cylinder(r=0.45, h=0.8, $fn=16);
        }

        // Black Wire (GND-)
        color("#1e293b") {
            translate([PCB_X + 25.0, P_BAT_Y + 0.7, -1.8])
                rotate([0, 90, 0])
                    cylinder(r=0.45, h=13.5, $fn=16);
            translate([PCB_X + 38.5, P_BAT_Y + 0.7, -1.8])
                cylinder(r=0.45, h=3.6, $fn=16);
            translate([P_BAT_X, P_BAT_Y + 0.7, 1.8])
                rotate([0, 90, 0])
                    cylinder(r=0.45, h=PCB_X + 38.5 - P_BAT_X, $fn=16);
            translate([P_BAT_X, P_BAT_Y + 0.7, PCB_T])
                cylinder(r=0.45, h=0.8, $fn=16);
        }
    }
}

// 9. 316L Stainless Steel Keyring Eyelet Bushing
module keyring_eyelet_bushing() {
    color("silver") {
        translate([EYELET_X, EYELET_Y, 0.1])
            difference() {
                cylinder(r=EYELET_OD / 2.0, h=FOB_H - 0.2, $fn=36);
                translate([0, 0, -0.2])
                    cylinder(r=EYELET_ID / 2.0, h=FOB_H + 0.2, $fn=36);
            }
    }
}

// 10. Protective TPU Shock-Absorbing Rim (Orange Accent)
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

// 11. Complete Assembly
module smart_keyfob_assembly(is_exploded = false) {
    if (is_exploded || EXPLODED_VIEW) {
        // EXPLODED VIEW
        // 1. Lower Shell
        color("#222831")
            translate([0, 0, 0])
                fob_lower_shell();

        // 2. Qi Receiver Coil (floating above lower shell)
        color("#b45309", 0.95)
            translate([FOB_L / 2.0 - 4.0, FOB_W / 2.0, 7.5])
                cylinder(r=11.5, h=0.4, $fn=48);

        // 3. LiPo Pouch Cell (lifted above coil)
        color("#334155")
            translate([PCB_X + 2.0, PCB_Y + 0.5, 11.0])
                cube([25.0, 18.0, 3.8]);

        // 4. Magnet & Shield Plate (shifted sideways)
        translate([FOB_L / 2.0 - MAG_L / 2.0 - 4.0, FOB_W - MAG_W + 8.0, 8.0])
            magnet_block();
        translate([FOB_L / 2.0 - MAG_L / 2.0 - 5.0, FOB_W - MAG_W + 4.0, 8.0])
            flux_shield_plate();

        // 5. PCBA 07 (without integrated battery, floating high)
        translate([0, 0, 20.0])
            internal_pcba(include_battery = false);

        // 6. 316L Bushing in solid bulkhead
        translate([0, 0, 0])
            keyring_eyelet_bushing();

        // 7. Upper Shell
        color("#1e293b")
            translate([0, 0, 36.0])
                fob_upper_shell();

        // 8. ePTFE Acoustic Vent Patch
        translate([0, 0, 37.5])
            eptfe_acoustic_vent();

        // 9. Sealed Silicone Keypad Membrane
        translate([0, 0, 48.0])
            silicone_button_keypad();

        // 10. Clear PMMA Light Guide
        translate([0, 0, 50.5])
            pmma_light_guide();

        // 11. TPU Shock Rim
        translate([-0.8, -0.8, -12.0])
            tpu_protective_rim();

    } else {
        // ASSEMBLED VIEW
        // Lower Shell
        color("#222831")
            translate([0, 0, 0])
                fob_lower_shell();

        // Magnet Key
        translate([FOB_L / 2.0 - MAG_L / 2.0 - 4.0, FOB_W - MAG_W, FOB_WALL + 0.2])
            magnet_block();

        // Flux Shield Plate
        translate([FOB_L / 2.0 - MAG_L / 2.0 - 5.0, FOB_W - MAG_W - 0.6, FOB_WALL])
            flux_shield_plate();

        // Internal PCBA & Battery
        translate([0, 0, PCB_Z])
            internal_pcba(include_battery = true);

        // 316L Bushing
        keyring_eyelet_bushing();

        // Upper Shell
        color("#1e293b")
            translate([0, 0, FOB_H / 2.0])
                fob_upper_shell();

        // ePTFE Membrane (inside upper shell)
        translate([0, 0, FOB_H / 2.0 + 0.3])
            eptfe_acoustic_vent();

        // Sealed Silicone Keypad (seated flush in upper well)
        translate([0, 0, FOB_H - 1.8])
            silicone_button_keypad();

        // PMMA Light Guide (seated in bore)
        translate([0, 0, FOB_H - 4.2])
            pmma_light_guide();

        // TPU Rim
        translate([-0.8, -0.8, -0.4])
            tpu_protective_rim();
    }
}

// Configurable Output Part Selector
part = "assembly"; // "assembly", "lower", "upper", "rim", "keypad", "exploded"

if (part == "lower") {
    fob_lower_shell();
} else if (part == "upper") {
    fob_upper_shell();
} else if (part == "rim") {
    tpu_protective_rim();
} else if (part == "keypad") {
    silicone_button_keypad();
} else if (part == "exploded") {
    smart_keyfob_assembly(is_exploded = true);
} else {
    smart_keyfob_assembly(is_exploded = false);
}



