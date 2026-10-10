// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Smart Pod Cartridge PCBA 03
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_adapter_pcb.scad
// Description: Accurate 1:1 3D model of the Smart Modular Cartridge PCB (PCBA 03)
//              matching hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb.
//              Dimensions: 35.0 x 25.0 x 1.6 mm with 2.0 mm chamfered corners.
//              Features:
//              - Bottom (B.Cu): PAD1 & PAD2 gold contact pads for Mill-Max spring pins,
//                U.FL coaxial socket ANT_UWB, DW3110 UWB Transceiver (QFN-16),
//                ES8388 Audio Codec (QFN-28), 4x MOSFETs (SOT-23), Fuse 1812.
//              - Top (F.Cu): ESP32-S2-MINI-1U MCU Module (with RF shield),
//                J_AUDIO_PWR 8-pin horizontal JST-SH header,
//                J_ACT 8-pin horizontal JST-SH header,
//                J_PROG 4-pin 1.27mm SMD pin header at bottom-left.
//              - 4x M2 mounting holes (29.0 x 19.0 mm pitch).
// =============================================================================

include <../parameters.scad>;

module dummy_adapter_pcb() {
    difference() {
        // 1. PCB Substrate (FR4 Matt Black / Dark Green, 35.0 x 25.0 x 1.6 mm)
        color([0.12, 0.16, 0.14]) {
            linear_extrude(height=1.6) {
                polygon(points=[
                    [2.0, 0.0],
                    [33.0, 0.0],
                    [35.0, 2.0],
                    [35.0, 23.0],
                    [33.0, 25.0],
                    [2.0, 25.0],
                    [0.0, 23.0],
                    [0.0, 2.0]
                ]);
            }
        }

        // 4x M2 Mounting Holes (H1..H4 at 29.0 x 19.0 mm pitch, Ø 2.2 mm)
        translate([3.0, 3.0, -0.2])   cylinder(r=1.1, h=2.0, $fn=24);
        translate([3.0, 22.0, -0.2])  cylinder(r=1.1, h=2.0, $fn=24);
        translate([32.0, 3.0, -0.2])  cylinder(r=1.1, h=2.0, $fn=24);
        translate([32.0, 22.0, -0.2]) cylinder(r=1.1, h=2.0, $fn=24);
    }

    // Gold ENIG Annular Rings for M2 Mounting Holes
    color("gold") {
        for (pos = [[3.0, 3.0], [3.0, 22.0], [32.0, 3.0], [32.0, 22.0]]) {
            translate([pos[0], pos[1], 1.605])
                difference() {
                    cylinder(r=1.75, h=0.02, center=true, $fn=24);
                    cylinder(r=1.1, h=0.03, center=true, $fn=24);
                }
            translate([pos[0], pos[1], -0.005])
                difference() {
                    cylinder(r=1.75, h=0.02, center=true, $fn=24);
                    cylinder(r=1.1, h=0.03, center=true, $fn=24);
                }
        }
    }

    // =========================================================================
    // 2. TOP LAYER (F.Cu) - ESP32-S2 Module, JST-SH Headers & J_PROG
    // =========================================================================

    // U1: ESP32-S2-MINI-1U Module (15.4 x 18.0 x 3.2 mm, centered at 18.9, 12.0)
    // Metal RF Shield Casing
    color([0.82, 0.84, 0.86]) {
        translate([18.90 - 7.7, 12.00 - 9.0, 1.6])
            cube([15.4, 14.0, 2.8], center=false);
    }
    // PCB Antenna / Header section of module
    color([0.10, 0.12, 0.10]) {
        translate([18.90 - 7.7, 12.00 + 5.0, 1.6])
            cube([15.4, 4.0, 1.0], center=false);
    }

    // J_AUDIO_PWR: 8-Pin JST-SH 1.0mm Horizontal Header (at X = 3.38, Y = 12.30, facing -X)
    color("whitesmoke") {
        translate([3.38 - 2.25, 12.30 - 4.5, 1.6])
            cube([4.5, 9.0, 2.2], center=false);
    }

    // J_ACT: 8-Pin JST-SH 1.0mm Horizontal Header (at X = 32.00, Y = 12.75, facing +X)
    color("whitesmoke") {
        translate([32.00 - 2.25, 12.75 - 4.5, 1.6])
            cube([4.5, 9.0, 2.2], center=false);
    }

    // J_PROG: 4-Pin 1.27mm Vertical Pin Header (at X = 8.00, Y = 22.11)
    // Black plastic base
    color([0.15, 0.15, 0.15]) {
        translate([8.00 - 2.54, 22.11 - 1.0, 1.6])
            cube([5.08, 2.0, 1.5], center=false);
    }
    // 4 Gold Square Pins
    color("gold") {
        for (i = [0:3]) {
            translate([8.00 - 1.905 + i * 1.27, 22.11, 1.6 + 1.5])
                cube([0.4, 0.4, 2.0], center=true);
        }
    }

    // =========================================================================
    // 3. BOTTOM LAYER (B.Cu) - Contact Pads, Codec, UWB, Fuse & MOSFETs
    // =========================================================================

    // PAD1 & PAD2: Mill-Max DC Spring Contact Pads (Gold ENIG, Ø 3.0 mm)
    color("gold") {
        // PAD1: +5V / +12V Power In at (1.50, 7.50)
        translate([1.50, 7.50, -0.02])
            cylinder(r=1.5, h=0.04, center=true, $fn=24);
        // PAD2: GND Return at (1.50, 17.50)
        translate([1.50, 17.50, -0.02])
            cylinder(r=1.5, h=0.04, center=true, $fn=24);
    }

    // ANT_UWB: Hirose U.FL SMT Socket (Silver / Gold center, facing -Z at 22.50, 2.20)
    color("silver") {
        translate([22.50, 2.20, -0.6])
            cube([3.0, 3.0, 1.2], center=true);
    }
    color("gold") {
        translate([22.50, 2.20, -1.22])
            cylinder(r=0.6, h=0.1, center=true, $fn=16);
    }

    // U_UWB: Qorvo DW3110 UWB Transceiver (QFN-16, 3.0 x 3.0 x 0.85 mm at 14.00, 2.25)
    color([0.12, 0.12, 0.12]) {
        translate([14.00 - 1.5, 2.25 - 1.5, -0.85])
            cube([3.0, 3.0, 0.85], center=false);
    }

    // Y_UWB: 38.4 MHz Crystal (2.0 x 1.6 x 0.65 mm at 15.00, 12.00)
    color([0.75, 0.75, 0.78]) {
        translate([15.00 - 1.0, 12.00 - 0.8, -0.65])
            cube([2.0, 1.6, 0.65], center=false);
    }

    // U3: Everest Semi ES8388 Stereo Audio Codec (QFN-28, 4.0 x 4.0 x 0.85 mm at 15.75, 22.75)
    color([0.15, 0.15, 0.15]) {
        translate([15.75 - 2.0, 22.75 - 2.0, -0.85])
            cube([4.0, 4.0, 0.85], center=false);
    }

    // F1: 1812 SMD Resettable PPTC Fuse (4.5 x 3.2 x 0.8 mm at 7.75, 2.00)
    color("darkgoldenrod") {
        translate([7.75 - 2.25, 2.00 - 1.6, -0.8])
            cube([4.5, 3.2, 0.8], center=false);
    }

    // Q1..Q4: 4x AO3400A SOT-23 MOSFETs (PTT / Power Switches at X = 27.70)
    color([0.18, 0.18, 0.18]) {
        for (y_pos = [7.15, 10.75, 14.35, 17.95]) {
            translate([27.70 - 1.45, y_pos - 0.65, -1.0])
                cube([2.9, 1.3, 1.0], center=false);
        }
    }

    // D1..D4: 4x SOD-323 Protection Diodes (at X = 30.80)
    color([0.22, 0.22, 0.22]) {
        for (y_pos = [6.50, 10.10, 13.70, 17.30]) {
            translate([30.80 - 1.25, y_pos - 0.62, -0.9])
                cube([2.5, 1.25, 0.9], center=false);
        }
    }

    // R1..R8: 0603 SMD Resistors (at X = 24.78)
    color([0.25, 0.25, 0.25]) {
        for (y_pos = [5.70, 7.30, 9.30, 10.90, 12.90, 14.50, 16.50, 18.10]) {
            translate([24.78 - 0.8, y_pos - 0.4, -0.55])
                cube([1.6, 0.8, 0.55], center=false);
        }
    }

    // C1, C2: SMD Capacitors (0603 & 0805 at X ~ 8.9)
    color("peru") {
        translate([8.97 - 0.8, 13.50 - 0.4, -0.55])
            cube([1.6, 0.8, 0.55], center=false);
        translate([8.80 - 1.0, 16.25 - 0.6, -0.8])
            cube([2.0, 1.2, 0.8], center=false);
    }
}

// Preview standalone
dummy_adapter_pcb();

