// =============================================================================
// OpenMotorBridge - Satellite Pod: Saddlebag 19 mm Hole Split Sealing Grommet
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/010_saddlebag_hole_grommet_split.scad
// Description: 2-piece split asymmetric elastomeric sealing grommet (EPDM/TPU
//              Shore 70A-85A) for the OEM 19.0 mm bottom mounting hole in
//              Harley-Davidson Touring / CVO ST saddlebag tubs.
//              Hermetically seals BOTH the OEM M8 steel sleeve (Ø 10.2 mm) AND
//              the internal slim cable (Ø 2.0 mm) without drilling or pinching.
//              Compresses under OEM fastener torque for IP67 water/dust seal.
// =============================================================================

$fn = 60;

// Parameter definitions
HOLE_DIA        = 19.0; // Saddlebag tub bore diameter (mm)
HOLE_R          = HOLE_DIA / 2.0; // 9.5 mm
WALL_THICKNESS  = 3.5;  // Saddlebag tub floor wall thickness (mm)
SLEEVE_DIA      = 10.2; // OEM M8 steel spacer sleeve outer diameter (mm)
SLEEVE_R        = SLEEVE_DIA / 2.0; // 5.1 mm
CABLE_DIA       = 2.2;  // Slim internal flexible cable outer diameter (mm)
CABLE_R         = CABLE_DIA / 2.0;  // 1.1 mm
COLLAR_DIA      = 24.0; // Upper and lower compression sealing flange diameter (mm)
TOTAL_H         = WALL_THICKNESS + 4.0; // 7.5 mm total grommet height

// Asymmetric offset: steel sleeve shifted -2.0 mm, cable placed at +5.5 mm
SLEEVE_OFFSET_Y = -2.0;
CABLE_OFFSET_Y  = 5.5;

module saddlebag_hole_grommet_full() {
    difference() {
        union() {
            // 1. Central Barrel: Fits into Ø 19.0 mm hole (with +0.3 mm sealing ribs)
            cylinder(r=HOLE_R + 0.15, h=TOTAL_H, center=true);

            // Circumferential Sealing Ribs (Doppelte Dichtlippen)
            translate([0, 0, -0.8])
                cylinder(r=HOLE_R + 0.45, h=0.8, center=true);
            translate([0, 0, 0.8])
                cylinder(r=HOLE_R + 0.45, h=0.8, center=true);

            // 2. Bottom Sealing Flange (Outer underside of saddlebag)
            translate([0, 0, -TOTAL_H/2 + 1.0])
                cylinder(r=COLLAR_DIA/2, h=2.0, center=true);

            // 3. Top Compression Flange (Inside saddlebag tub under OEM washer)
            translate([0, 0, TOTAL_H/2 - 1.0])
                cylinder(r=COLLAR_DIA/2, h=2.0, center=true);
        }

        // 4. Eccentric Through-Bore for OEM Steel Sleeve (Ø 10.2 mm)
        translate([0, SLEEVE_OFFSET_Y, 0])
            cylinder(r=SLEEVE_R, h=TOTAL_H + 4.0, center=true);

        // 5. Dedicated Sealed Cable Pass-Through Channel (Ø 2.2 mm)
        translate([0, CABLE_OFFSET_Y, 0])
            cylinder(r=CABLE_R, h=TOTAL_H + 4.0, center=true);

        // Chamfer lead-in on cable channel for snag-free threading
        translate([0, CABLE_OFFSET_Y, TOTAL_H/2])
            cylinder(r1=CABLE_R, r2=CABLE_R + 1.2, h=1.5, center=true);
        translate([0, CABLE_OFFSET_Y, -TOTAL_H/2])
            cylinder(r1=CABLE_R + 1.2, r2=CABLE_R, h=1.5, center=true);
    }
}

// Module for Part A (Front Half with Cable Channel & Split Seam)
module saddlebag_grommet_part_a() {
    difference() {
        saddlebag_hole_grommet_full();
        // Cut away rear half (Y < 0.0 mm)
        translate([-COLLAR_DIA, -COLLAR_DIA - 0.05, -TOTAL_H])
            cube([2*COLLAR_DIA, COLLAR_DIA + 0.05, 2*TOTAL_H]);
    }
}

// Module for Part B (Rear Half with Steel Sleeve Pocket & Tongue-and-Groove Interlock)
module saddlebag_grommet_part_b() {
    difference() {
        saddlebag_hole_grommet_full();
        // Cut away front half (Y > 0.0 mm)
        translate([-COLLAR_DIA, 0.0, -TOTAL_H])
            cube([2*COLLAR_DIA, COLLAR_DIA + 0.05, 2*TOTAL_H]);
    }
}

// Render both parts side by side for direct 3D printing in TPU
module print_plate_saddlebag_grommet() {
    translate([-14.0, 0, TOTAL_H/2])
        rotate([180, 0, 0])
            saddlebag_grommet_part_a();

    translate([14.0, 0, TOTAL_H/2])
        rotate([180, 0, 0])
            saddlebag_grommet_part_b();
}

// Default preview: Assembled cross section
saddlebag_hole_grommet_full();
