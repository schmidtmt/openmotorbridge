// =============================================================================
// OpenMotorBridge - Dummy 3D Model: Satellite Pod Interface Board PCBA 03
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_adapter_pcb.scad
// Description: Accurate 1:1 3D model of the Satellite Pod Interface Board (PCBA 03)
//              Dimensions: 42.0 x 48.0 x 1.6 mm with 2.0 mm chamfered corners.
//              Features:
//              - Left Bulkhead Edge (Facing saddlebag grommet & chassis USB-C port):
//                * J_BUS (4-Pin JST-GH 1.25mm SMD, bottom-left at Y = 12.0 mm)
//                * J_USB_OUT (4-Pin JST-GH 1.25mm SMD, top-left at Y = 38.0 mm)
//                  leading via internal flexible silicone harness to Port B
//                * 30W USB-PD Buck-Boost converter zone (SW3516 QFN-32 + 7x7 mm Inductor)
//              - Center Zone:
//                * U1: ESP32-C6-MINI-1U RISC-V MCU Module (with RF shield & U.FL)
//                * U3: ES8388 24-Bit Audio Codec (QFN-28)
//                * U4: TS5A3159 Analog/Digital Switch (SOT-23-6)
//              - Right Edge (Facing rear equipment chamber / OEM adapters):
//                * J_AUDIO_PWR: 8-Pin JST-SH 1.0mm SMD header (top-right at Y = 36.0 mm)
//                * J_ACT: 4-Pin JST-SH 1.0mm SMD header (bottom-right at Y = 12.0 mm)
//                * Dual AO3400A MOSFETs & flyback diodes for 5V cold-start solenoids
//              - 4x M2.5 mounting holes (36.0 x 42.0 mm pitch).
//              - Completely removed: DW3110 UWB, 38.4 MHz crystal, J_PROG SWD, blade slot.
// =============================================================================

include <../parameters.scad>;

module dummy_adapter_pcb() {
    difference() {
        // 1. PCB Substrate (FR4 Matt Black, 42.0 x 48.0 x 1.6 mm with 2.0 mm corner chamfers)
        color([0.12, 0.14, 0.13]) {
            linear_extrude(height=1.6) {
                polygon(points=[
                    [2.0, 0.0],
                    [40.0, 0.0],
                    [42.0, 2.0],
                    [42.0, 46.0],
                    [40.0, 48.0],
                    [2.0, 48.0],
                    [0.0, 46.0],
                    [0.0, 2.0]
                ]);
            }
        }

        // 4x M2.5 Mounting Holes (36.0 x 42.0 mm pitch, Ø 2.7 mm)
        // Centers at X = 3.0, 39.0; Y = 3.0, 45.0
        translate([3.0, 3.0, -0.2])   cylinder(r=1.35, h=2.0, $fn=24);
        translate([3.0, 45.0, -0.2])  cylinder(r=1.35, h=2.0, $fn=24);
        translate([39.0, 3.0, -0.2])  cylinder(r=1.35, h=2.0, $fn=24);
        translate([39.0, 45.0, -0.2]) cylinder(r=1.35, h=2.0, $fn=24);
    }

    // Gold ENIG Annular Rings for M2.5 Mounting Holes
    color("gold") {
        for (pos = [[3.0, 3.0], [3.0, 45.0], [39.0, 3.0], [39.0, 45.0]]) {
            translate([pos[0], pos[1], 1.605])
                difference() {
                    cylinder(r=2.1, h=0.02, center=true, $fn=24);
                    cylinder(r=1.35, h=0.03, center=true, $fn=24);
                }
            translate([pos[0], pos[1], -0.005])
                difference() {
                    cylinder(r=2.1, h=0.02, center=true, $fn=24);
                    cylinder(r=1.35, h=0.03, center=true, $fn=24);
                }
        }
    }

    // =========================================================================
    // 2. LEFT BULKHEAD EDGE: J_BUS (Bottom-Left) & J_USB_OUT (Top-Left)
    // =========================================================================

    // J_BUS: 4-Pin JST-GH 1.25mm SMD Horizontal Shrouded Header (at X = 0.5, Y = 12.0)
    // Mates with cable from saddlebag wall grommet (< 15 mm direct run)
    color([0.92, 0.92, 0.90]) {
        translate([0.5, 12.0 - 3.75, 1.6]) {
            difference() {
                // Outer shrouded body (4.5 x 7.5 x 4.0 mm)
                cube([4.5, 7.5, 4.0], center=false);
                // Entry slot for GHR-04V-S plug (facing -X)
                translate([-0.1, 0.8, 0.8])
                    cube([3.5, 5.9, 2.6], center=false);
            }
        }
    }
    // 4 Gold Contact Pins inside J_BUS
    color("gold") {
        for (i = [0:3]) {
            translate([2.2, 12.0 - 1.875 + i * 1.25, 1.6 + 1.8])
                cube([2.0, 0.35, 0.35], center=true);
        }
    }

    // J_USB_OUT: 4-Pin JST-GH 1.25mm SMD Horizontal Shrouded Header (at X = 0.5, Y = 38.0)
    // Connects via 4-wire silicone ribbon cable to chassis-mounted USB-C socket (Port B)
    color([0.92, 0.92, 0.90]) {
        translate([0.5, 38.0 - 3.75, 1.6]) {
            difference() {
                cube([4.5, 7.5, 4.0], center=false);
                translate([-0.1, 0.8, 0.8])
                    cube([3.5, 5.9, 2.6], center=false);
            }
        }
    }
    // 4 Gold Contact Pins inside J_USB_OUT
    color("gold") {
        for (i = [0:3]) {
            translate([2.2, 38.0 - 1.875 + i * 1.25, 1.6 + 1.8])
                cube([2.0, 0.35, 0.35], center=true);
        }
    }

    // =========================================================================
    // 3. 30W USB-PD CHARGING POWER STAGE (Top-Left Zone)
    // =========================================================================

    // U_PD: SW3516 / IP6538 USB-PD Controller & Sync Buck Converter (QFN-32, 5.0 x 5.0 x 0.85 mm at X = 9.0, Y = 38.0)
    color([0.15, 0.15, 0.15]) {
        translate([9.0 - 2.5, 38.0 - 2.5, 1.6])
            cube([5.0, 5.0, 0.85], center=false);
    }

    // L_PD: 10 uH High-Current Shielded Power Inductor (7.0 x 7.0 x 4.5 mm at X = 16.5, Y = 38.0)
    color([0.25, 0.25, 0.28]) {
        translate([16.5 - 3.5, 38.0 - 3.5, 1.6])
            cube([7.0, 7.0, 4.5], center=false);
    }

    // C_IN / C_OUT: 4x Solid Polymer Filter Capacitors (SMD 1210, 3.2 x 2.5 x 2.0 mm)
    color("peru") {
        translate([8.5, 43.5, 1.6]) cube([3.2, 2.5, 2.0], center=false);
        translate([13.0, 43.5, 1.6]) cube([3.2, 2.5, 2.0], center=false);
        translate([8.5, 31.5, 1.6]) cube([3.2, 2.5, 2.0], center=false);
        translate([13.0, 31.5, 1.6]) cube([3.2, 2.5, 2.0], center=false);
    }

    // =========================================================================
    // 4. CENTER ZONE: ESP32-C6 MCU & AUDIO CODEC
    // =========================================================================

    // U1: ESP32-C6-MINI-1U RISC-V Module (13.2 x 16.6 x 2.4 mm at X = 26.0, Y = 24.0)
    // Metal RF Shield Casing
    color([0.82, 0.84, 0.86]) {
        translate([26.0 - 6.6, 24.0 - 8.3, 1.6])
            cube([13.2, 13.0, 2.4], center=false);
    }
    // Module PCB & U.FL Antenna Section
    color([0.10, 0.12, 0.10]) {
        translate([26.0 - 6.6, 24.0 + 4.7, 1.6])
            cube([13.2, 3.6, 1.0], center=false);
    }
    // U.FL Antenna Socket on ESP32-C6
    color("gold") {
        translate([26.0 + 3.5, 24.0 + 6.5, 1.6 + 1.0])
            cylinder(r=1.0, h=1.0, center=false, $fn=16);
    }

    // U3: ES8388 24-Bit Stereo Audio Codec (QFN-28, 4.0 x 4.0 x 0.85 mm at X = 13.5, Y = 20.0)
    color([0.15, 0.15, 0.15]) {
        translate([13.5 - 2.0, 20.0 - 2.0, 1.6])
            cube([4.0, 4.0, 0.85], center=false);
    }

    // U4: TS5A3159 High-Speed Audio Switch (SOT-23-6 at X = 13.5, Y = 13.0)
    color([0.18, 0.18, 0.18]) {
        translate([13.5 - 1.45, 13.0 - 0.8, 1.6])
            cube([2.9, 1.6, 1.1], center=false);
    }

    // =========================================================================
    // 5. RIGHT EDGE (FACING REAR EQUIPMENT CHAMBER): J_AUDIO_PWR & J_ACT
    // =========================================================================

    // J_AUDIO_PWR: 8-Pin JST-SH 1.0mm Vertical Header (at X = 39.5, Y = 36.0, Top-Entry +Z)
    // Direct link to OEM Intercom harness (Sena, Cardo, OMM, Midland)
    color("whitesmoke") {
        translate([39.5 - 1.45, 36.0 - 5.0, 1.6]) {
            difference() {
                // Outer Shrouded Body (2.9 x 10.0 x 4.3 mm)
                cube([2.9, 10.0, 4.3], center=false);
                // Top-Entry Mating Slot for SHR-08V-S (from +Z)
                translate([0.45, 0.9, 0.8])
                    cube([2.0, 8.2, 3.6], center=false);
            }
        }
    }
    // 8 Gold Contact Pins inside J_AUDIO_PWR
    color("gold") {
        for (i = [0:7]) {
            translate([39.5, 36.0 - 3.5 + i * 1.0, 1.6 + 1.2])
                cube([0.3, 0.3, 2.0], center=true);
        }
    }

    // J_ACT: 4-Pin JST-SH 1.0mm Vertical Header (at X = 39.5, Y = 12.0, Top-Entry +Z)
    // Direct link to 5V Solenoids on universal actuator slide bracket
    // Vertical separation = 36.0 - 12.0 = 24.0 mm (> 20 mm isolation against inductive spikes!)
    color("whitesmoke") {
        translate([39.5 - 1.45, 12.0 - 3.0, 1.6]) {
            difference() {
                // Outer Shrouded Body (2.9 x 6.0 x 4.3 mm)
                cube([2.9, 6.0, 4.3], center=false);
                // Top-Entry Mating Slot for SHR-04V-S (from +Z)
                translate([0.45, 0.9, 0.8])
                    cube([2.0, 4.2, 3.6], center=false);
            }
        }
    }
    // 4 Gold Contact Pins inside J_ACT
    color("gold") {
        for (i = [0:3]) {
            translate([39.5, 12.0 - 1.5 + i * 1.0, 1.6 + 1.2])
                cube([0.3, 0.3, 2.0], center=true);
        }
    }

    // Q1, Q2: Dual N-Channel Power MOSFETs (AO3400A / SOT-23, 30V/4A at X = 34.0, Y = 10.0 & 14.0)
    color([0.18, 0.18, 0.18]) {
        translate([34.0 - 1.45, 10.0 - 0.65, 1.6]) cube([2.9, 1.3, 1.0], center=false);
        translate([34.0 - 1.45, 14.0 - 0.65, 1.6]) cube([2.9, 1.3, 1.0], center=false);
    }

    // D_FLY1, D_FLY2: Dual Flyback Schottky Diodes (SOD-123 at X = 30.5, Y = 10.0 & 14.0)
    color([0.22, 0.22, 0.22]) {
        translate([30.5 - 1.3, 10.0 - 0.75, 1.6]) cube([2.6, 1.5, 1.1], center=false);
        translate([30.5 - 1.3, 14.0 - 0.75, 1.6]) cube([2.6, 1.5, 1.1], center=false);
    }
}

// Preview standalone
dummy_adapter_pcb();
