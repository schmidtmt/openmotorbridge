// =============================================================================
// OPENMOTORBRIDGE SATELLITE POD GATEWAY / CARTRIDGE INTERFACE DUMMY PCB (PCBA 03)
// =============================================================================
// 100% Single-Sided SMT Assembly on F.Cu (Top Layer)
// Dimensions: 42.0 x 48.0 x 1.6 mm with 4x M2.5 Mounting Holes (36.0 x 42.0 mm pitch)
//
// Layout Topology (F.Cu Top Layer):
// - Left Bulkhead Edge:
//     * J_BUS (4-Pin JST-GH, bottom) at X = 3.5, Y = 37.0 (< 15 mm run to grommet)
//     * J_USB_OUT (4-Pin JST-GH, top) at X = 3.5, Y = 11.0 (silicone cable to Port B)
// - Top Zone (30W USB-PD Power Stage):
//     * SW3516 Sync Buck & PD Controller at X = 14.2, Y = 11.7
//     * 7x7 mm 10 uH Power Inductor at X = 24.2, Y = 6.25
//     * Filter Capacitors & 1812 Fuse
// - Center-Left Zone:
//     * U1: ESP32-C6-MINI-1U Host MCU at X = 8.5, Y = 24.0
// - Right Edge (Facing Rear Equipment Chamber):
//     * J_ACT (Actuator Connector) at X = 39.0, Y = 18.5 with Q1..Q4, D1..D4 on F.Cu
//     * J_AUDIO_PWR (8-Pin JST-SH) at X = 39.0, Y = 34.7
//     * U3 (ES8388 Codec) at X = 28.3, Y = 32.8 on F.Cu
//     * U4 (TS5A3159 Switch) at X = 29.7, Y = 41.1 on F.Cu
// - Bottom Layer (B.Cu): Unbroken Solid GND Plane (ENIG Gold Finish)
// =============================================================================

module dummy_adapter_pcb() {
    // 1. PCB Substrate (FR-4 4-Layer High-TG150, 42.0 x 48.0 x 1.6 mm)
    color([0.08, 0.28, 0.12]) {
        difference() {
            // Base polygon with 1.0 mm corner chamfers
            linear_extrude(height=1.6, center=false) {
                polygon(points=[
                    [1.0, 0.0],
                    [41.0, 0.0],
                    [42.0, 1.0],
                    [42.0, 47.0],
                    [41.0, 48.0],
                    [1.0, 48.0],
                    [0.0, 47.0],
                    [0.0, 1.0]
                ]);
            }

            // 4x M2.5 Mounting Holes (36.0 x 42.0 mm pitch, Ø 2.7 mm)
            // Centers at X = 3.0, 39.0; Y = 3.0, 45.0
            translate([3.0, 3.0, -0.2])   cylinder(r=1.35, h=2.0, $fn=24);
            translate([3.0, 45.0, -0.2])  cylinder(r=1.35, h=2.0, $fn=24);
            translate([39.0, 3.0, -0.2])  cylinder(r=1.35, h=2.0, $fn=24);
            translate([39.0, 45.0, -0.2]) cylinder(r=1.35, h=2.0, $fn=24);
        }
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
    // 2. LEFT BULKHEAD EDGE: J_USB_OUT (Top) & J_BUS (Bottom)
    // =========================================================================

    // J_USB_OUT: 4-Pin JST-GH 1.25mm SMD Shrouded Header at X = 3.5, Y = 11.0
    // Connects via flexible silicone ribbon cable to Port B (USB-C bulkhead socket)
    color([0.92, 0.92, 0.90]) {
        translate([3.5 - 2.25, 11.0 - 3.75, 1.6]) {
            difference() {
                cube([4.5, 7.5, 4.0], center=false);
                translate([0.8, 0.8, 0.8])
                    cube([2.9, 5.9, 3.3], center=false);
            }
        }
    }
    color("gold") {
        for (i = [0:3]) {
            translate([3.5, 11.0 - 1.875 + i * 1.25, 1.6 + 1.8])
                cube([0.35, 0.35, 2.0], center=true);
        }
    }

    // J_BUS: 4-Pin JST-GH 1.25mm SMD Shrouded Header at X = 3.5, Y = 37.0
    // Mates with cable from saddlebag wall grommet (< 15 mm direct run)
    color([0.92, 0.92, 0.90]) {
        translate([3.5 - 2.25, 37.0 - 3.75, 1.6]) {
            difference() {
                cube([4.5, 7.5, 4.0], center=false);
                translate([0.8, 0.8, 0.8])
                    cube([2.9, 5.9, 3.3], center=false);
            }
        }
    }
    color("gold") {
        for (i = [0:3]) {
            translate([3.5, 37.0 - 1.875 + i * 1.25, 1.6 + 1.8])
                cube([0.35, 0.35, 2.0], center=true);
        }
    }

    // =========================================================================
    // 3. 30W USB-PD CHARGING POWER STAGE (Top Zone, F.Cu)
    // =========================================================================

    // U_PD: SW3516 / IP6538 USB-PD Controller (QFN-32, 5.0 x 5.0 x 0.85 mm at X = 14.2, Y = 11.7)
    color([0.15, 0.15, 0.15]) {
        translate([14.2 - 2.5, 11.7 - 2.5, 1.6])
            cube([5.0, 5.0, 0.85], center=false);
    }

    // L_PD: 10 uH Shielded Power Inductor (7.0 x 7.0 x 4.5 mm at X = 24.2, Y = 6.25)
    color([0.25, 0.25, 0.28]) {
        translate([24.2 - 3.5, 6.25 - 3.5, 1.6])
            cube([7.0, 7.0, 4.5], center=false);
    }

    // C_PD_IN & C_PD_OUT: Solid Polymer Filter Capacitors (SMD 1210)
    color("peru") {
        translate([8.7, 4.0, 1.6])  cube([3.2, 2.5, 2.0], center=false);
        translate([31.8, 3.0, 1.6]) cube([3.2, 2.5, 2.0], center=false);
    }

    // F1: PPTC Polyfuse 1812 at X = 32.4, Y = 8.25
    color("darkgreen") {
        translate([32.4 - 2.25, 8.25 - 1.6, 1.6])
            cube([4.5, 3.2, 0.8], center=false);
    }

    // =========================================================================
    // 4. CENTER ZONE: ESP32-C6 MCU (F.Cu)
    // =========================================================================

    // U1: ESP32-C6-MINI-1U Module (13.2 x 16.6 x 2.4 mm at X = 8.5, Y = 24.0, rot 90)
    color([0.82, 0.84, 0.86]) {
        translate([8.5 - 6.5, 24.0 - 6.6, 1.6])
            cube([13.0, 13.2, 2.4], center=false);
    }
    // U.FL Antenna Section
    color([0.10, 0.12, 0.10]) {
        translate([8.5 + 6.5, 24.0 - 6.6, 1.6])
            cube([3.6, 13.2, 1.0], center=false);
    }
    color("gold") {
        translate([8.5 + 8.0, 24.0 + 3.5, 1.6 + 1.0])
            cylinder(r=1.0, h=1.0, center=false, $fn=16);
    }

    // =========================================================================
    // 5. RIGHT EDGE: J_ACT, J_AUDIO_PWR, CODEC & SWITCH (All on F.Cu)
    // =========================================================================

    // J_ACT: Actuator Header (JST-SH Vertical) at X = 39.0, Y = 18.5
    color("whitesmoke") {
        translate([39.0 - 1.45, 18.5 - 5.0, 1.6]) {
            difference() {
                cube([2.9, 10.0, 4.3], center=false);
                translate([0.45, 0.9, 0.8])
                    cube([2.0, 8.2, 3.6], center=false);
            }
        }
    }

    // Q1..Q4 Actuator MOSFETs (SOT-23 on F.Cu at X = 32.1, Y = 14..25)
    color([0.18, 0.18, 0.18]) {
        for (y_pos = [14.75, 18.25, 21.75, 25.25]) {
            translate([32.1 - 1.45, y_pos - 0.65, 1.6]) cube([2.9, 1.3, 1.0], center=false);
        }
    }

    // J_AUDIO_PWR: 8-Pin JST-SH 1.0mm Vertical Header at X = 39.0, Y = 34.7
    // Direct link to OEM Intercom harness (Sena, Cardo, OMM, Midland)
    color("whitesmoke") {
        translate([39.0 - 1.45, 34.7 - 5.0, 1.6]) {
            difference() {
                cube([2.9, 10.0, 4.3], center=false);
                translate([0.45, 0.9, 0.8])
                    cube([2.0, 8.2, 3.6], center=false);
            }
        }
    }

    // U3: ES8388 24-Bit Stereo Audio Codec (QFN-28, 4.0 x 4.0 mm on F.Cu at X = 28.3, Y = 32.8)
    color([0.15, 0.15, 0.15]) {
        translate([28.3 - 2.0, 32.8 - 2.0, 1.6])
            cube([4.0, 4.0, 0.85], center=false);
    }

    // U4: TS5A3159 Audio Switch (SOT-23-6 on F.Cu at X = 29.7, Y = 41.1)
    color([0.18, 0.18, 0.18]) {
        translate([29.7 - 1.45, 41.1 - 0.8, 1.6])
            cube([2.9, 1.6, 1.1], center=false);
    }
}

// Preview standalone
dummy_adapter_pcb();
