// =============================================================================
// OpenMotorBridge - GoPro Hirth Anti-Slip Rosette (Radiale Formschluss-Verzahnung)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/011_gopro_hirth_lock.scad
// Description: Parametric radial Hirth-type interlocking teeth for GoPro swivel
//              hinges. Eliminates angle drift from engine vibration and harsh
//              offroad bumps (TET / washboard gravel) in fine 10° or 5° steps.
//              Features:
//              1. Radially arrayed interlocking wedge teeth around M5 central bore.
//              2. Positive form-fit locking: 100% immune to rotational slipping.
//              3. Reusable modules for both male tongues and female clevis prongs.
// =============================================================================

include <../../00_common/parameters.scad>;

// --- Parametric Dimensions ---
HIRTH_R_INNER       = 3.0;   // Inner clearance radius around M5 bore (mm)
HIRTH_R_OUTER       = 7.6;   // Outer tooth perimeter radius (mm)
HIRTH_TOOTH_H       = 0.55;  // Tooth peak height for crisp MJF PA12 engagement (mm)
HIRTH_NUM_TEETH     = 36;    // 36 teeth = 10° angle increments (or 72 for 5°)

// 1. Single Radial Wedge Tooth
module hirth_single_tooth(r_in=HIRTH_R_INNER, r_out=HIRTH_R_OUTER, h=HIRTH_TOOTH_H, angle_step=10.0) {
    w_outer = 2.0 * r_out * sin(angle_step / 2.0);
    w_inner = 2.0 * r_in * sin(angle_step / 2.0);

    hull() {
        // Ridge line at peak height h
        translate([r_in, 0, h]) cube([r_out - r_in, 0.05, 0.05], center=false);
        // Base facet left
        rotate([0, 0, -angle_step/2.0])
            translate([r_in, -w_inner/2.0, 0]) cube([r_out - r_in, 0.05, 0.05], center=false);
        // Base facet right
        rotate([0, 0, angle_step/2.0])
            translate([r_in, w_inner/2.0, 0]) cube([r_out - r_in, 0.05, 0.05], center=false);
    }
}

// 2. Full 360° Hirth Locking Rosette Disk
module gopro_hirth_rosette(
    r_in        = HIRTH_R_INNER,
    r_out       = HIRTH_R_OUTER,
    tooth_h     = HIRTH_TOOTH_H,
    num_teeth   = HIRTH_NUM_TEETH
) {
    step = 360.0 / num_teeth;
    for (i = [0 : num_teeth - 1]) {
        rotate([0, 0, i * step])
            hirth_single_tooth(r_in=r_in, r_out=r_out, h=tooth_h, angle_step=step);
    }
}

// 3. Subtraction Tool to imprint Rosette into an existing lug face
module gopro_hirth_subtraction_tool(
    r_in        = HIRTH_R_INNER,
    r_out       = HIRTH_R_OUTER,
    tooth_h     = HIRTH_TOOTH_H,
    num_teeth   = HIRTH_NUM_TEETH
) {
    // Inverted negative teeth
    rotate([0, 0, 180.0 / num_teeth])
        gopro_hirth_rosette(r_in=r_in, r_out=r_out, tooth_h=tooth_h, num_teeth=num_teeth);
}

// Standalone preview
gopro_hirth_rosette();
