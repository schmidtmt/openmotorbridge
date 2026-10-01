// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Smart Pod Cartridge PCBA 03
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_adapter_pcb.scad
// Description: Accurate 1:1 3D model of the Smart Modular Cartridge PCB (PCBA 03)
//              matching hardware/kicad_pod_cartridge/openmotorbridge_pod_cartridge.kicad_pcb.
//              Dimensions: 35.0 x 25.0 x 1.6 mm with 2.0 mm chamfered corners.
//              Features:
//              - Bottom (B.Cu): PAD1 & PAD2 gold contact pads for Mill-Max spring pins,
//                U.FL coaxial socket ANT_UWB, DW3110 UWB Transceiver (QFN-16).
//              - Top (F.Cu): ES8388 Audio Codec (QFN-28), MCU (TSSOP-20),
//                J_ACT 8-pin horizontal JST-SH header, J_AUDIO_PWR 6-pin JST-SH header.
//              - 4x M2 mounting holes (29.0 x 19.0 mm pitch).
// =============================================================================

include <../parameters.scad>;

module dummy_adapter_pcb() {
    difference() {
        // 1. PCB Substrate (FR4 Matt Black / Dark Green, 35.0 x 25.0 x 1.6 mm)
        color([0.12, 0.15, 0.14]) {
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

        // 4x M2 Mounting Holes (H1..H4 at 29.0 x 19.0 mm pitch)
        translate([3.0, 3.0, -0.2])   cylinder(r=1.1, h=2.0, $fn=16);
        translate([3.0, 22.0, -0.2])  cylinder(r=1.1, h=2.0, $fn=16);
        translate([32.0, 3.0, -0.2])  cylinder(r=1.1, h=2.0, $fn=16);
        translate([32.0, 22.0, -0.2]) cylinder(r=1.1, h=2.0, $fn=16);
    }

    // 2. Bottom Layer (B.Cu) - Mill-Max DC Spring Contact Pads & UWB Transceiver
    // PAD1: +5V / +12V Power In (Gold ENIG, 2.5 x 3.5 mm)
    color("gold") {
        translate([1.5 - 1.25, 7.5 - 1.75, -0.05])
            cube([2.5, 3.5, 0.08], center=false);
        // PAD2: GND Return (Gold ENIG, 2.5 x 3.5 mm)
        translate([1.5 - 1.25, 17.5 - 1.75, -0.05])
            cube([2.5, 3.5, 0.08], center=false);
    }

    // ANT_UWB: Hirose U.FL SMT Socket (Silver / Gold center, facing -Z)
    color("silver") {
        translate([11.0, 9.5, -1.2])
            cube([3.0, 3.0, 1.2], center=true);
    }
    color("gold") {
        translate([11.0, 9.5, -1.25])
            cylinder(r=0.6, h=0.3, center=true, $fn=12);
    }

    // U1: Qorvo DW3110 UWB Transceiver (QFN-16, 3.0 x 3.0 x 0.85 mm on B.Cu)
    color("black") {
        translate([15.0 - 1.5, 7.5 - 1.5, -0.85])
            cube([3.0, 3.0, 0.85], center=false);
        // 38.4 MHz Crystal
        translate([19.0, 7.5 - 1.0, -0.65])
            cube([2.0, 1.6, 0.65], center=false);
    }

    // 3. Top Layer (F.Cu) - Audio Codec, Logic, Drivers & Headers
    // U2: Everest Semi ES8388 Stereo Audio Codec (QFN-28, 4.0 x 4.0 x 0.85 mm)
    color("black") {
        translate([22.0 - 2.0, 15.5 - 2.0, 1.6])
            cube([4.0, 4.0, 0.85], center=false);
    }

    // U3: Sub-MCU / Logic (TSSOP-20, 6.5 x 4.4 x 1.1 mm)
    color("black") {
        translate([12.0 - 3.25, 16.0 - 2.2, 1.6])
            cube([6.5, 4.4, 1.1], center=false);
    }

    // 4x AO3400A SOT-23 MOSFETs (PTT / Power Switches)
    color("black") {
        translate([10.0, 5.0, 1.6])  cube([2.9, 1.3, 1.0], center=false);
        translate([10.0, 8.0, 1.6])  cube([2.9, 1.3, 1.0], center=false);
        translate([10.0, 11.0, 1.6]) cube([2.9, 1.3, 1.0], center=false);
    }

    // Fuse F1: 1812 SMD Resettable PPTC Fuse (4.5 x 3.2 x 0.8 mm)
    color("darkgoldenrod") {
        translate([5.0, 11.0, 1.6])
            cube([4.5, 3.2, 0.8], center=false);
    }

    // J_ACT: 8-Pin JST-SH 1.0mm Horizontal Header (X = 27.0, Y = 14.0, facing +X)
    color("whitesmoke") {
        translate([26.5, 14.0 - 4.5, 1.6])
            cube([4.5, 9.0, 2.2], center=false);
    }

    // J_AUDIO_PWR: 6-Pin JST-SH 1.0mm Horizontal Header (X = 27.0, Y = 5.0, facing +X)
    color("whitesmoke") {
        translate([26.5, 5.0 - 3.5, 1.6])
            cube([4.5, 7.0, 2.2], center=false);
    }
}

// Preview standalone
dummy_adapter_pcb();
