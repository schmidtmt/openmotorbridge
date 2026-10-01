// =============================================================================
// OpenMotorBridge - Main Box: Lid Plate & Gore Vent Boss (Gehäusedeckel)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/020_lid_plate.scad
// Description: Ready-to-print enclosure top lid with continuous perimeter tongue
//              lip (Feder), integrated Gore ePTFE breather vent boss, internal
//              Taoglas FXP895 LoRa 868 MHz flex antenna pocket, and 4x M3 screw holes.
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_lid_plate(length=110.0, width=74.0, plate_h=4.0, lip_h=1.5, lip_w=1.6) {
    difference() {
        union() {
            // 1. Solid Top Lid Plate
            cube(size=[length, width, plate_h], center=false);

            // 2. Continuous Perimeter Tongue Lip (Feder for sealing groove)
            translate([0, 0, -lip_h]) {
                difference() {
                    translate([1.4, 1.4, 0])
                        cube(size=[length - 2.8, width - 2.8, lip_h], center=false);
                    translate([1.4 + lip_w, 1.4 + lip_w, -0.1])
                        cube(size=[length - 2.8 - 2*lip_w, width - 2.8 - 2*lip_w, lip_h + 0.2], center=false);
                }
            }

            // 3. Gore ePTFE Pressure Equalization Vent Boss (Top Center: Ø 7.0 mm x 1.5 mm)
            translate([length/2.0, width/2.0, plate_h])
                cylinder(r=3.5, h=1.5, center=false, $fn=36);
        }

        // 4. Gore Vent Center Breather Hole (Ø 3.0 mm through-hole)
        translate([length/2.0, width/2.0, -lip_h - 0.5])
            cylinder(r=1.5, h=plate_h + lip_h + 2.5, center=false, $fn=24);

        // 5. Internal LoRa 868 MHz Flex Antenna Pocket (Taoglas FXP895: 85.0 x 18.0 x 0.8 mm)
        // Recessed on underside of lid (facing downward into enclosure), 100% leak-proof
        translate([length/2.0, width/2.0, -lip_h - 0.1]) {
            cube([85.0, 18.0, 1.2], center=true);
            // U.FL Micro-Coaxial Cable Relief Channel leading toward front wire pass-through
            translate([20.0, -12.0, 0])
                cube([4.0, 14.0, 1.2], center=true);
        }

        // 6. 4x M3 Corner Countersunk Screw Holes
        corner_offset = MAIN_BOX_CORNER_POST / 2.0;
        for (pos = [
            [corner_offset, corner_offset],
            [length - corner_offset, corner_offset],
            [corner_offset, width - corner_offset],
            [length - corner_offset, width - corner_offset]
        ]) {
            translate([pos[0], pos[1], -lip_h - 0.5]) {
                cylinder(r=M3_SCREW_HOLE_R, h=plate_h + lip_h + 1.0, center=false, $fn=24);
                // 90° Countersink recess on top face
                translate([0, 0, plate_h + lip_h - 1.5])
                    cylinder(r1=M3_SCREW_HOLE_R, r2=3.2, h=1.8, center=false, $fn=24);
            }
        }
    }
}

// Standalone preview
main_box_lid_plate();
