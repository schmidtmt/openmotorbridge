// =============================================================================
// OpenMotorBridge - Main Box: Lid Plate & Gore Vent Boss (Gehäusedeckel)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/020_lid_plate.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_lid_plate(length=110.0, width=74.0, plate_h=3.0, lip_h=1.5, lip_w=1.6) {
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
                cylinder(r=3.5, h=1.5, center=false);
        }

        // 4. Gore Vent Center Breather Hole (Ø 3.0 mm through-hole)
        translate([length/2.0, width/2.0, -lip_h - 0.5])
            cylinder(r=1.5, h=plate_h + lip_h + 2.5, center=false);

        // 5. 4x M3 Corner Countersunk Screw Holes
        translate([3.0, 3.0, -lip_h - 0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_h + lip_h + 1.0, center=false);
        translate([length - 3.0, 3.0, -lip_h - 0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_h + lip_h + 1.0, center=false);
        translate([3.0, width - 3.0, -lip_h - 0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_h + lip_h + 1.0, center=false);
        translate([length - 3.0, width - 3.0, -lip_h - 0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_h + lip_h + 1.0, center=false);
    }
}

// Standalone preview
main_box_lid_plate();
