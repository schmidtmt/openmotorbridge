// =============================================================================
// OpenMotorBridge - Satellite Pod: Rear GoPro & Luggage Rack Mount (Pod 3)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_mount_gopro_rack.scad
// Description: Standard 3-prong GoPro compatible mounting adapter plate for
//              tail, topcase, or tubular luggage rack mounting of Pod 3.
// =============================================================================

include <../00_common/parameters.scad>;

module pod_mount_gopro_rack(plate_l=80.0, plate_w=50.0, plate_t=4.0) {
    difference() {
        union() {
            // 1. Adapter Base Plate
            cube(size=[plate_l, plate_w, plate_t], center=false);

            // 2. 3x Standard GoPro Cleats (Underneath center: 3x 3.0mm fingers, 3.0mm gaps)
            translate([28.0, plate_w/2.0 - 4.0, -10.0])
                cube(size=[4.0, 8.0, 10.0], center=false);
            translate([38.0, plate_w/2.0 - 4.0, -10.0])
                cube(size=[4.0, 8.0, 10.0], center=false);
            translate([48.0, plate_w/2.0 - 4.0, -10.0])
                cube(size=[4.0, 8.0, 10.0], center=false);
        }

        // 3. GoPro M5 Through-Bolt Hole (across the 3 cleats)
        translate([20.0, plate_w/2.0, -5.0])
            rotate([0, 90, 0])
                cylinder(r=2.6, h=40.0, center=false); // Ø 5.2 mm for M5 thumbscrew

        // 4. 2x M3 Screws to Pod Housing Bottom
        translate([15.0, plate_w/2.0, -1.0])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_t + 2.0, center=false);
        translate([65.0, plate_w/2.0, -1.0])
            cylinder(r=M3_SCREW_HOLE_R, h=plate_t + 2.0, center=false);
    }
}

// Render complete GoPro mount
pod_mount_gopro_rack();
