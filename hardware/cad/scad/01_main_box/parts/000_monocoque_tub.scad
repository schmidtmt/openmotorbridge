// =============================================================================
// OpenMotorBridge - Central Main Box: Monocoque Housing Tub (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/000_monocoque_tub.scad
// Description: Monolithic PA12-MJF monocoque enclosure tub for the Central Box
//              (Gehäuse Typ A: 110 x 74 x 38 mm). Implements the v10 Dual-Rail
//              Monocoque Slide-In architecture:
//
// 1. Lower Zone (Z = 0..17 mm):
//    - 100% solid, leak-free floor (2.5 mm wall thickness).
//    - 4x M2.5/M3 PCB standoffs (h = 3.5 mm) for PCBA 01 (85 x 55 mm, 77 x 47 mm pitch).
//    - 4x outer M4 silentblock mounting ears (128 x 46..56 mm pitch).
//    - Solid front wall (Y = 0) with automotive flanges (Deutsch DTM 6-Pin,
//      Cable 2 16-Pin Periphery), USB-C service port (J3), and SW1 button.
//
// 2. Middle Level (Z = 18.0..20.4 mm):
//    - Dual-Rail Track 1: Longitudinal support grooves for the slide-in
//      Zwischenboden (battery & antenna tray).
//
// 3. Upper Level (Z = 32.5..38.0 mm):
//    - Dual-Rail Track 2: Deep C-profile guide grooves with solid 2.5 mm PA12
//      retaining roof lips for the L-Slide Lid (form-fit lock, zero vertical lift).
//    - Front wedge-lock pocket (Keilanzug-Nut) for airtight sealing.
//
// 4. Rear Portal (Y = 74 mm):
//    - Lower sill (Z = 0..15 mm) with MicroSD service access, optional SMA port,
//      and dual corner latch sockets for Slam-to-Shut deadbolt locking.
//    - Insertion portal (Z = 15..38 mm) for horizontal slide-in kinematics.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;
use <004_mounting_ears.scad>;

module main_box_monocoque_tub(
    length = MAIN_BOX_OUTER_L,
    width  = MAIN_BOX_OUTER_W,
    height = MAIN_BOX_TOTAL_H,
    wall   = MAIN_BOX_WALL
) {
    r_corner = MAIN_BOX_CORNER_R;

    difference() {
        union() {
            // 1. Monolithic 5-Sided Outer Hull with Rounded Vertical Corners
            hull() {
                translate([r_corner, r_corner, 0])
                    cylinder(r=r_corner, h=height, $fn=32);
                translate([length - r_corner, r_corner, 0])
                    cylinder(r=r_corner, h=height, $fn=32);
                translate([r_corner, width - r_corner, 0])
                    cylinder(r=r_corner, h=height, $fn=32);
                translate([length - r_corner, width - r_corner, 0])
                    cylinder(r=r_corner, h=height, $fn=32);
            }

            // 2. 4x Outer M4 Silentblock Mounting Ears
            main_box_mounting_ears(
                length=length,
                width=width,
                ear_len=14.0,
                ear_w=12.0,
                ear_h=5.0,
                edge_offset=14.0
            );

            // 3. 4x PCB Standoff Columns (h = 3.5 mm, Z = wall .. wall + 3.5)
            // Pitch: 77.0 x 47.0 mm (PCBA 01: 85 x 55 mm centered at [12.5, 9.5])
            for (pos = [
                [12.5 + 4.0,  9.5 + 4.0],   // H1 (16.5, 13.5)
                [12.5 + 81.0, 9.5 + 4.0],   // H2 (93.5, 13.5)
                [12.5 + 4.0,  9.5 + 51.0],  // H3 (16.5, 60.5)
                [12.5 + 81.0, 9.5 + 51.0]   // H4 (93.5, 60.5)
            ]) {
                translate([pos[0], pos[1], wall])
                    cylinder(r=3.2, h=3.5, $fn=24);
            }

            // 4. Rail 1 Reinforcement Ledges (supporting Slide-In Tray from below at Z = 16.5..18.0 mm)
            // Left flank ledge
            translate([wall, wall + 2.0, 16.5])
                cube([2.0, width - 2*wall - 4.0, 1.8], center=false);
            // Right flank ledge
            translate([length - wall - 2.0, wall + 2.0, 16.5])
                cube([2.0, width - 2*wall - 4.0, 1.8], center=false);
            // Front stop ledge (Y = wall)
            translate([wall, wall, 16.5])
                cube([length - 2*wall, 2.5, 1.8], center=false);
        }

        // --- SUBTRACTIONS ---

        // 5. Main Internal Chamber (Clears PCBA 01 and Upper Compartment)
        translate([wall, wall, wall]) {
            cube([
                length - 2*wall,
                width - 2*wall,
                height - wall + 1.0
            ], center=false);
        }

        // 6. 4x Captive DIN 934 M2.5 / M3 Hex Nut Pockets & Screw Bores for PCB
        for (pos = [
            [12.5 + 4.0,  9.5 + 4.0],
            [12.5 + 81.0, 9.5 + 4.0],
            [12.5 + 4.0,  9.5 + 51.0],
            [12.5 + 81.0, 9.5 + 51.0]
        ]) {
            // Screw bore through standoff
            translate([pos[0], pos[1], -0.5])
                cylinder(r=M3_SCREW_HOLE_R, h=wall + 4.5, $fn=20);
            // Hex nut pocket on underside (Z = 0..NUT_M3_H)
            translate([pos[0], pos[1], -0.1])
                cylinder(r=NUT_M3_SW / 2.0 / cos(30), h=NUT_M3_H, $fn=6);
        }

        // 7. DUAL-RAIL TRACK 1: Slide-In Tray Guide Grooves (Z = 18.0..20.4 mm)
        // Left guide groove into left wall (X = wall - 1.5 .. wall)
        translate([wall - MAIN_BOX_RAIL1_DEPTH, wall + 1.0, MAIN_BOX_RAIL1_Z - MAIN_BOX_RAIL1_H/2.0])
            cube([MAIN_BOX_RAIL1_DEPTH + 0.1, width - wall, MAIN_BOX_RAIL1_H], center=false);
        // Right guide groove into right wall
        translate([length - wall - 0.1, wall + 1.0, MAIN_BOX_RAIL1_Z - MAIN_BOX_RAIL1_H/2.0])
            cube([MAIN_BOX_RAIL1_DEPTH + 0.1, width - wall, MAIN_BOX_RAIL1_H], center=false);

        // 8. DUAL-RAIL TRACK 2: L-Slide Lid C-Grooves (Z = 32.5..35.5 mm)
        // Left C-groove with solid PA12 retaining lip above it (Z = 35.5..38.0 mm)
        translate([wall - MAIN_BOX_RAIL2_DEPTH, wall + 2.0, MAIN_BOX_RAIL2_Z - MAIN_BOX_RAIL2_H/2.0])
            cube([MAIN_BOX_RAIL2_DEPTH + 0.1, width - wall + 2.0, MAIN_BOX_RAIL2_H], center=false);
        // Right C-groove with solid PA12 retaining lip above it
        translate([length - wall - 0.1, wall + 2.0, MAIN_BOX_RAIL2_Z - MAIN_BOX_RAIL2_H/2.0])
            cube([MAIN_BOX_RAIL2_DEPTH + 0.1, width - wall + 2.0, MAIN_BOX_RAIL2_H], center=false);

        // 9. Front Wall Wedge-Lock Pocket (Keilanzug-Nut at Y = wall)
        // Front nose of slide lid seats into this undercut to compress the front seal
        translate([wall + 1.0, wall - 1.2, MAIN_BOX_RAIL2_Z - 0.5])
            cube([length - 2*wall - 2.0, 1.5, MAIN_BOX_RAIL2_H + 1.0], center=false);

        // 10. REAR PORTAL OPENING (at Y = width, above the 15.0 mm sill)
        // Completely open from Z = MAIN_BOX_REAR_SILL_H to top Z = height + 1.0 mm!
        translate([wall, width - wall - 1.0, MAIN_BOX_REAR_SILL_H])
            cube([length - 2*wall, wall + 2.0, height - MAIN_BOX_REAR_SILL_H + 2.0], center=false);

        // Entry throats for Rail 2 C-grooves at the rear portal
        translate([wall - MAIN_BOX_RAIL2_DEPTH - 0.5, width - wall - 1.0, MAIN_BOX_RAIL2_Z - MAIN_BOX_RAIL2_H/2.0])
            cube([length - 2*wall + 2*MAIN_BOX_RAIL2_DEPTH + 1.0, wall + 2.0, height - MAIN_BOX_RAIL2_Z + 2.0], center=false);

        // 11. Rear Lower Sill (Z = 0..15 mm) Deadbolt Latch Sockets & MicroSD Window:
        // Left corner socket (blind pocket depth 4.5 mm into sill top face)
        translate([wall + 4.0, width - wall - 0.5, MAIN_BOX_REAR_SILL_H - 4.5])
            cube([4.0, wall + 1.5, 5.0], center=false);
        // Right corner socket (blind pocket depth 4.5 mm into sill top face)
        translate([length - wall - 8.0, width - wall - 0.5, MAIN_BOX_REAR_SILL_H - 4.5])
            cube([4.0, wall + 1.5, 5.0], center=false);

        // Exterior Step/Rebate on Lower Sill for Flush Overlap of L-Slide Lid Drip Apron
        translate([wall - 0.5, width - 1.6, MAIN_BOX_REAR_SILL_H - 4.0])
            cube([length - 2*wall + 1.0, 2.0, 4.5], center=false);

        // MicroSD Service Access Slot (centered at X = 12.5 + 37.28 = 49.8 mm, Z = 4.0..8.5 mm)
        translate([49.8 - 7.5, width - wall - 1.0, 4.0])
            cube([15.0, wall + 2.0, 4.5], center=false);

        // Optional Rear SMA Antenna Port (Ø 6.5 mm with O-Ring Pocket at X = 85.0 mm, Z = 8.5 mm)
        translate([85.0, width + 0.5, 8.5]) {
            rotate([90, 0, 0]) {
                // Through hole Ø 6.5 mm
                cylinder(r=SMA_BORE_R, h=wall + 2.0, center=false, $fn=28);
                // O-ring compression recess Ø 9.5 mm x 1.2 mm
                cylinder(r=SMA_ORECESS_R, h=SMA_ORECESS_DEPTH + 0.5, center=false, $fn=32);
            }
        }

        // 12. FRONT WALL INTERFACE PORT CUTOUTS (at Y = 0)
        // A. Deutsch DTM 6-Pin Flange Cutout (Cable 1 Bordnetz & CAN, centered at X = 25.0 mm, Z = 11.5 mm)
        translate([25.0 - 9.5, -1.0, 11.5 - 6.0])
            cube([19.0, wall + 2.0, 12.0], center=false);
        // 2x M3 Flange Screw Bores for DTM-6 (Pitch = 28.0 mm: X = 11.0 and X = 39.0 mm)
        for (dx = [-14.0, 14.0]) {
            translate([25.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    cylinder(r=M3_SCREW_HOLE_R, h=wall + 2.0, $fn=24);
        }

        // B. 16-Pin Periphery Bus Flange Cutout (Cable 2 Peripherie, centered at X = 58.0 mm, Z = 11.5 mm)
        translate([58.0 - 11.0, -1.0, 11.5 - 6.0])
            cube([22.0, wall + 2.0, 12.0], center=false);
        // 2x M3 Flange Screw Bores for 16-Pin Flange (Pitch = 32.0 mm: X = 42.0 and X = 74.0 mm)
        for (dx = [-16.0, 16.0]) {
            translate([58.0 + dx, -1.0, 11.5])
                rotate([-90, 0, 0])
                    cylinder(r=M3_SCREW_HOLE_R, h=wall + 2.0, $fn=24);
        }

        // C. USB-C Service & Flash Port (J3 Receptacle Cutout, centered at X = 82.0 mm, Z = 7.6 mm)
        translate([82.0 - 5.0, -1.0, 7.6 - 2.2])
            cube([10.0, wall + 2.0, 4.4], center=false);
        // Recessed O-ring sealing pocket / cap recess for USB-C (14.0 x 8.0 mm, depth 1.2 mm)
        translate([82.0 - 7.0, -0.5, 7.6 - 4.0])
            cube([14.0, 1.8, 8.0], center=false);

        // D. Hardware SW1 Button & Status LED Window (centered at X = 96.0 mm, Z = 8.5 mm)
        translate([96.0, -1.0, 8.5])
            rotate([-90, 0, 0])
                cylinder(r=3.25, h=wall + 2.0, $fn=28);
    }
}

// Standalone preview
main_box_monocoque_tub();
