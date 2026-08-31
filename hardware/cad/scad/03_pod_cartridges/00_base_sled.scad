// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Cartridge Base Sled (Grundschlitten)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/00_base_sled.scad
// Description: Shared parametric base sled for all interchangeable cartridges.
//              Includes sled floor, side walls, asymmetrical Poka-Yoke guide ribs
//              with 30° lead-in chamfer, dual spring-loaded snap-fit cantilever
//              arms with squeeze release buttons and 85° latch teeth, front
//              faceplate with sealing collar, and ePTFE membrane boss.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;

module cartridge_base_sled(
    sled_l   = CARTRIDGE_BASE_L,
    sled_w   = CARTRIDGE_BASE_W,
    sled_h   = CARTRIDGE_BASE_H,
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

            // 4. 4x M2 Lower Carrier PCB Mounting Standoffs (for 35x25mm openmotorbridge_pod_cartridge PCB)
            // Exact KiCad match: PCB at X=1.5..36.5, Y=14.5..39.5 -> Holes at (4.5, 17.5), (4.5, 36.5), (33.5, 17.5), (33.5, 36.5)
            translate([4.5, 17.5, wall])
                screw_boss(outer_r=2.2, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([33.5, 17.5, wall])
                screw_boss(outer_r=2.2, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([4.5, 36.5, wall])
                screw_boss(outer_r=2.2, inner_r=M2_SCREW_HOLE_R, h=2.5);
            translate([33.5, 36.5, wall])
                screw_boss(outer_r=2.2, inner_r=M2_SCREW_HOLE_R, h=2.5);

            // 5. 4x M2 Insert Fastening Corner Posts (h = 5.5 mm, z = 2.5 .. 8.0 mm)
            // Secures interchangeable modular OEM inserts (Sena, Cardo, Blindkassette) at outer perimeter
            translate([6.0, 6.0, wall])
                screw_boss(outer_r=2.8, inner_r=M2_SCREW_HOLE_R, h=5.5);
            translate([sled_l - 7.0, 6.0, wall])
                screw_boss(outer_r=2.8, inner_r=M2_SCREW_HOLE_R, h=5.5);
            translate([6.0, sled_w - 6.0, wall])
                screw_boss(outer_r=2.8, inner_r=M2_SCREW_HOLE_R, h=5.5);
            translate([sled_l - 7.0, sled_w - 6.0, wall])
                screw_boss(outer_r=2.8, inner_r=M2_SCREW_HOLE_R, h=5.5);

            // 7. Lateral Support Ledges / Shoulders (Auflagestufen at z = 2.5 .. 8.0 mm)
            // Provides continuous rigid shelf for the OEM insert and maintains 1.8 mm clearance over Carrier PCB
            translate([10.0, wall, wall])
                cube(size=[sled_l - 20.0, 1.2, 5.5], center=false);
            translate([10.0, sled_w - wall - 1.2, wall])
                cube(size=[sled_l - 20.0, 1.2, 5.5], center=false);

            // 8. Front Faceplate (4.0 x 58.0 x 25.0 mm at x = sled_l)
            translate([sled_l, -2.0, -1.5])
                cube(size=[CARTRIDGE_FACE_L, CARTRIDGE_FACE_W, CARTRIDGE_FACE_H], center=false);

            // 5. Continuous 360° Perimeter Sealing Collar (Flansch-Dichtsitz für Silikondichtung)
            // Sits at x = sled_l - 2.5 .. sled_l, completely unobstructed all around
            translate([sled_l - 2.5, -1.0, -0.5]) {
                difference() {
                    cube(size=[2.5, sled_w + 2.0, sled_h + 3.0], center=false);
                    translate([-0.1, 1.8, 1.8])
                        cube(size=[2.7, sled_w - 1.6, sled_h - 0.6], center=false);
                }
            }

            // 6. Asymmetrical Poka-Yoke Guide Ribs (Tongue Rails) with 30° Lead-in Nose
            // --- Left Guide Rib (z = 8.2 mm center, height 2.6 mm, protrusion 1.4 mm) ---
            translate([CARTRIDGE_CHAMFER_L, -CARTRIDGE_TONGUE_PROT, POD_GROOVE_LEFT_Z - CARTRIDGE_TONGUE_W/2.0])
                cube(size=[sled_l - CARTRIDGE_CHAMFER_L - 3.5, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W], center=false);

            // Left 30° Lead-in Nose (x = 0 .. 4 mm)
            translate([0, -CARTRIDGE_TONGUE_PROT, POD_GROOVE_LEFT_Z - CARTRIDGE_TONGUE_W/2.0 + 0.3])
                cube(size=[CARTRIDGE_CHAMFER_L, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W - 0.6], center=false);

            // --- Right Guide Rib (z = 14.2 mm center, height 2.6 mm, protrusion 1.4 mm) ---
            translate([CARTRIDGE_CHAMFER_L, sled_w, POD_GROOVE_RIGHT_Z - CARTRIDGE_TONGUE_W/2.0])
                cube(size=[sled_l - CARTRIDGE_CHAMFER_L - 3.5, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W], center=false);

            // Right 30° Lead-in Nose (x = 0 .. 4 mm)
            translate([0, sled_w, POD_GROOVE_RIGHT_Z - CARTRIDGE_TONGUE_W/2.0 + 0.3])
                cube(size=[CARTRIDGE_CHAMFER_L, CARTRIDGE_TONGUE_PROT, CARTRIDGE_TONGUE_W - 0.6], center=false);

            // 7. Dual Recessed Snap-Fit Cantilever Arms & Ergonomic Quick-Release Buttons
            // --- Left Arm (x = 54.0 .. 70.0 mm, in side wall, clears sealing collar at x = 72.5) ---
            translate([54.0, -1.8, 6.0])
                cube(size=[16.0, 1.8, 10.0], center=false);

            // Left Triangular Latch Tooth (at x = 58.0, 1.8 mm retention undercut)
            translate([58.0, -3.4, 6.5]) {
                polyhedron(
                    points=[
                        [0, 1.6, 0], [4.0, 1.6, 0], [4.0, 0, 0], [0, 1.6, 9.0], [4.0, 1.6, 9.0], [4.0, 0, 9.0]
                    ],
                    faces=[
                        [0,1,2], [3,5,4], [0,2,5,3], [1,4,5,2], [0,3,4,1]
                    ]
                );
            }

            // Left Textured Quick-Release Squeeze Button Pad (on Faceplate Flank)
            translate([sled_l - 0.5, -4.0, 5.0]) {
                cube(size=[CARTRIDGE_FACE_L + 1.5, 2.0, 12.0], center=false);
                // 3x Tactile Grip Ribs
                for (rz = [2.0, 6.0, 10.0]) {
                    translate([0.5, -0.6, rz])
                        cube(size=[CARTRIDGE_FACE_L, 0.6, 1.2], center=false);
                }
            }

            // Left Flexure Link between arm and button (passes outside the sealed pod rim)
            translate([70.0, -3.0, 8.0])
                cube(size=[sled_l - 70.0, 1.4, 6.0], center=false);

            // --- Right Arm (x = 54.0 .. 70.0 mm, in side wall) ---
            translate([54.0, sled_w, 6.0])
                cube(size=[16.0, 1.8, 10.0], center=false);

            // Right Triangular Latch Tooth
            translate([58.0, sled_w + 1.8, 6.5]) {
                polyhedron(
                    points=[
                        [0, 0, 0], [4.0, 0, 0], [4.0, 1.6, 0], [0, 0, 9.0], [4.0, 0, 9.0], [4.0, 1.6, 9.0]
                    ],
                    faces=[
                        [0,2,1], [3,4,5], [0,3,5,2], [1,2,5,4], [0,1,4,3]
                    ]
                );
            }

            // Right Textured Quick-Release Squeeze Button Pad (on Faceplate Flank)
            translate([sled_l - 0.5, sled_w + 2.0, 5.0]) {
                cube(size=[CARTRIDGE_FACE_L + 1.5, 2.0, 12.0], center=false);
                // 3x Tactile Grip Ribs
                for (rz = [2.0, 6.0, 10.0]) {
                    translate([0.5, 2.0, rz])
                        cube(size=[CARTRIDGE_FACE_L, 0.6, 1.2], center=false);
                }
            }

            // Right Flexure Link between arm and button
            translate([70.0, sled_w + 1.6, 8.0])
                cube(size=[sled_l - 70.0, 1.4, 6.0], center=false);

            // 8. Front ePTFE Gore Vent Boss on Faceplate
            translate([sled_l + 2.0, sled_w/2.0, 18.0])
                rotate([0, 90, 0])
                    cylinder(r=3.0, h=2.0, center=false);
        }

        // 9. Side Wall Clearance Slots for Latch Arm Inward Flexure
        // Left Arm Clearance Slots (1.0 mm slit above and below arm)
        translate([52.0, -2.5, 4.8])
            cube(size=[19.0, wall + 3.0, 1.0], center=false);
        translate([52.0, -2.5, 16.2])
            cube(size=[19.0, wall + 3.0, 1.0], center=false);
        translate([52.0, -2.5, 4.8])
            cube(size=[2.0, wall + 3.0, 12.4], center=false);

        // Right Arm Clearance Slots
        translate([52.0, sled_w - wall - 0.5, 4.8])
            cube(size=[19.0, wall + 3.0, 1.0], center=false);
        translate([52.0, sled_w - wall - 0.5, 16.2])
            cube(size=[19.0, wall + 3.0, 1.0], center=false);
        translate([52.0, sled_w - wall - 0.5, 4.8])
            cube(size=[2.0, wall + 3.0, 12.4], center=false);

        // 10. Front ePTFE Breather Through-Hole (Ø 2.0 mm)
        translate([sled_l - 3.0, sled_w/2.0, 18.0])
            rotate([0, 90, 0])
                cylinder(r=1.0, h=CARTRIDGE_FACE_L + 6.0, center=false);

        // 11. Floor Convective Breathing Slots (4x 14 x 2.5 mm)
        translate([18.0, 10.0, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([18.0, sled_w - 12.5, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([44.0, 10.0, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
        translate([44.0, sled_w - 12.5, -0.5]) cube(size=[14.0, 2.5, wall + 1.0], center=false);
    }
}

// Standalone preview
cartridge_base_sled();
