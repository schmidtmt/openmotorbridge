// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Cartridge Base Sled (Grundschlitten)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/00_base_sled.scad
// Description: Shared parametric base sled for all interchangeable cartridges.
//              Includes sled floor, side walls, asymmetrical Poka-Yoke guide ribs
//              with 30° lead-in chamfer, 2x floor copper stud pads, front faceplate
//              with sealing collar & POM snap-fit latch seat, and ePTFE membrane boss.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;

module cartridge_base_sled(
    sled_l   = CARTRIDGE_BASE_L,
    sled_w   = CARTRIDGE_BASE_W,
    sled_h   = 18.0,
    wall     = 2.5
) {
    difference() {
        union() {
            // 1. Sled Floor (75.0 x 54.0 x 2.5 mm)
            cube(size=[sled_l, sled_w, wall], center=false);

            // 2. Left Side Wall (75.0 x 2.5 x sled_h mm)
            cube(size=[sled_l, wall, sled_h + wall], center=false);

            // 3. Right Side Wall (75.0 x 2.5 x sled_h mm)
            translate([0, sled_w - wall, 0])
                cube(size=[sled_l, wall, sled_h + wall], center=false);

            // 4. Front Faceplate (4.0 x 58.0 x 25.0 mm at x = sled_l)
            translate([sled_l, -2.0, -1.5])
                cube(size=[CARTRIDGE_FACE_L, CARTRIDGE_FACE_W, CARTRIDGE_FACE_H], center=false);

            // 5. Front Sealing Collar Lip (Flansch-Dichtkragen: Shore 40A Silicone Seat)
            translate([sled_l - 2.0, 0.0, -0.5]) {
                difference() {
                    cube(size=[2.0, sled_w, sled_h + 3.0], center=false);
                    translate([-0.1, 1.5, 1.5])
                        cube(size=[2.2, sled_w - 3.0, sled_h], center=false);
                }
            }

            // 6. Asymmetrical Poka-Yoke Guide Ribs (Tongue Rails) with 30° Lead-in Nose
            // --- Left Guide Rib (z = 8.2 mm center, height 2.6 mm, protrusion 1.4 mm) ---
            translate([CARTRIDGE_CHAMFER_L, -CARTRIDGE_TONGUE_PROT, POD_GROOVE_LEFT_Z - CARTRIDGE_TONGUE_W/2.0])
                cube(size=[sled_l - CARTRIDGE_CHAMFER_L - 1.0, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W], center=false);

            // Left 30° Lead-in Nose (x = 0 .. 4 mm)
            translate([0, -CARTRIDGE_TONGUE_PROT, POD_GROOVE_LEFT_Z - CARTRIDGE_TONGUE_W/2.0 + 0.3])
                cube(size=[CARTRIDGE_CHAMFER_L, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W - 0.6], center=false);

            // --- Right Guide Rib (z = 14.2 mm center, height 2.6 mm, protrusion 1.4 mm) ---
            translate([CARTRIDGE_CHAMFER_L, sled_w, POD_GROOVE_RIGHT_Z - CARTRIDGE_TONGUE_W/2.0])
                cube(size=[sled_l - CARTRIDGE_CHAMFER_L - 1.0, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W], center=false);

            // Right 30° Lead-in Nose (x = 0 .. 4 mm)
            translate([0, sled_w, POD_GROOVE_RIGHT_Z - CARTRIDGE_TONGUE_W/2.0 + 0.3])
                cube(size=[CARTRIDGE_CHAMFER_L, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W - 0.6], center=false);

            // 7. 2x Copper Thermal Stud Pads in Sled Floor (Ø 8.0 x 2.5 mm)
            translate([42.0, sled_w/2.0, 0.0])
                copper_stud(r=COPPER_STUD_R, h=wall);
            translate([60.0, sled_w/2.0, 0.0])
                copper_stud(r=COPPER_STUD_R, h=wall);

            // 8. Front ePTFE Gore Vent Boss on Faceplate
            translate([sled_l + 2.0, sled_w/2.0, 18.0])
                rotate([0, 90, 0])
                    cylinder(r=3.0, h=2.0, center=false);
        }

        // 9. Front ePTFE Breather Through-Hole (Ø 2.0 mm)
        translate([sled_l - 1.0, sled_w/2.0, 18.0])
            rotate([0, 90, 0])
                cylinder(r=1.0, h=CARTRIDGE_FACE_L + 4.0, center=false);

        // 10. Floor Convective Breathing Slots (4x 14 x 2.5 mm)
        translate([18.0, 10.0, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([18.0, sled_w - 12.5, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([44.0, 10.0, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([44.0, sled_w - 12.5, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
    }
}

// Standalone preview
cartridge_base_sled();
