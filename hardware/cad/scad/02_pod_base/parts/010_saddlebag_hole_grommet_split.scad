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

// Stage-1 Strain Relief Tower parameters (Inside saddlebag tub on Part A)
TOWER_H         = 9.0;  // Tower height above top flange (mm)
ZIP_TIE_W       = 2.8;  // Width of mini zip-tie slot (mm)
ZIP_TIE_H       = 1.6;  // Thickness of mini zip-tie slot (mm)

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

            // 4. Integrated Stage-1 Strain-Relief Tower (Inside saddlebag tub, Part A)
            translate([0, 0, TOTAL_H/2]) {
                hull() {
                    translate([-4.5, 3.5, 0]) cylinder(r=1.5, h=TOWER_H);
                    translate([4.5, 3.5, 0]) cylinder(r=1.5, h=TOWER_H);
                    translate([-4.5, 10.0, 0]) cylinder(r=1.5, h=TOWER_H);
                    translate([4.5, 10.0, 0]) cylinder(r=1.5, h=TOWER_H);
                }
            }
        }

        // Subtractions:
        // A. Eccentric Through-Bore for OEM Steel Sleeve (Ø 10.2 mm)
        translate([0, SLEEVE_OFFSET_Y, 0])
            cylinder(r=SLEEVE_R, h=TOTAL_H + 4.0, center=true);

        // B. Washer Clearance Recess (Provides Ø 17.0 mm flat seating for OEM washer)
        translate([0, SLEEVE_OFFSET_Y, TOTAL_H/2 + TOWER_H/2])
            cylinder(r=8.5, h=TOWER_H + 2.0, center=true, $fn=60);

        // C. Dedicated Sealed Cable Pass-Through Channel (Ø 2.2 mm)
        translate([0, CABLE_OFFSET_Y, 0])
            cylinder(r=CABLE_R, h=TOTAL_H + 2*TOWER_H + 10.0, center=true);

        // Chamfer lead-in on bottom cable channel
        translate([0, CABLE_OFFSET_Y, -TOTAL_H/2])
            cylinder(r1=CABLE_R + 1.2, r2=CABLE_R, h=1.5, center=true);

        // Funnel lead-out at top of strain relief tower
        translate([0, CABLE_OFFSET_Y, TOTAL_H/2 + TOWER_H])
            cylinder(r1=CABLE_R, r2=CABLE_R + 1.2, h=2.0, center=true);

        // D. Lateral Zip-Tie Clamping Slot (Passes behind cable at Y = CABLE_OFFSET_Y + 2.8)
        translate([0, CABLE_OFFSET_Y + 2.8, TOTAL_H/2 + 4.5])
            cube([16.0, ZIP_TIE_W, ZIP_TIE_H], center=true);

        // E. Circumferential Zip-Tie Retention Groove on outer flanks
        translate([0, CABLE_OFFSET_Y, TOTAL_H/2 + 4.5]) {
            difference() {
                cylinder(r=9.5, h=ZIP_TIE_H, center=true);
                cylinder(r=7.2, h=ZIP_TIE_H + 0.5, center=true);
            }
        }

        // F. Lateral Cable Insertion Slit (0.7 mm wide from split face Y=0 to cable channel)
        translate([-0.35, -0.1, -TOTAL_H/2 - 1.0])
            cube([0.7, CABLE_OFFSET_Y + 0.2, TOTAL_H + TOWER_H + 2.0]);
    }
}

// Module for Part A (Front Half with Cable Channel, Slit & Strain Relief Tower)
module saddlebag_grommet_part_a() {
    difference() {
        saddlebag_hole_grommet_full();
        // Cut away rear half (Y < 0.0 mm)
        translate([-COLLAR_DIA, -COLLAR_DIA - 0.05, -TOTAL_H])
            cube([2*COLLAR_DIA, COLLAR_DIA + 0.05, 2*TOTAL_H + 2*TOWER_H]);
    }
}

// Module for Part B (Rear Half with Steel Sleeve Pocket)
module saddlebag_grommet_part_b() {
    difference() {
        saddlebag_hole_grommet_full();
        // Cut away front half (Y > 0.0 mm)
        translate([-COLLAR_DIA, 0.0, -TOTAL_H])
            cube([2*COLLAR_DIA, COLLAR_DIA + 0.05, 2*TOTAL_H + 2*TOWER_H]);
    }
}

// Render both parts side by side for direct 3D printing in TPU (flat on printbed, zero supports)
module print_plate_saddlebag_grommet() {
    translate([-16.0, 0, TOTAL_H/2])
        saddlebag_grommet_part_a();

    translate([16.0, 0, TOTAL_H/2])
        saddlebag_grommet_part_b();
}

// Default preview: Assembled grommet with Stage-1 strain relief
saddlebag_hole_grommet_full();
