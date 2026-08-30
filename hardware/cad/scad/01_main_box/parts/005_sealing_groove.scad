// =============================================================================
// OpenMotorBridge - Main Box: Perimeter Sealing Groove & Tongue (Nut & Feder)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/005_sealing_groove.scad
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. Gasket Groove Cutout Tool (Nut for Lower Case upper rim: 2.0 mm wide x 1.8 mm deep)
module main_box_sealing_groove_tool(length=110.0, width=74.0, z_top=17.0, groove_w=2.0, groove_depth=1.8) {
    translate([0, 0, z_top - groove_depth]) {
        difference() {
            translate([1.2, 1.2, 0])
                cube(size=[length - 2.4, width - 2.4, groove_depth + 0.1], center=false);
            translate([1.2 + groove_w, 1.2 + groove_w, -0.1])
                cube(size=[length - 2.4 - 2*groove_w, width - 2.4 - 2*groove_w, groove_depth + 0.3], center=false);
        }
    }
}

// 2. Gasket Tongue / Lip (Feder for Mid Tray lower rim: 1.6 mm wide x 1.5 mm high)
module main_box_sealing_tongue_lip(length=110.0, width=74.0, lip_w=1.6, lip_h=1.5) {
    difference() {
        translate([1.4, 1.4, -lip_h])
            cube(size=[length - 2.8, width - 2.8, lip_h], center=false);
        translate([1.4 + lip_w, 1.4 + lip_w, -lip_h - 0.1])
            cube(size=[length - 2.8 - 2*lip_w, width - 2.8 - 2*lip_w, lip_h + 0.2], center=false);
    }
}
