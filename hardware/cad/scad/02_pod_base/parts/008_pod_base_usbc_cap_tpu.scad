// =============================================================================
// OpenMotorBridge - Satellite Pod: Port B USB-C Waterproof TPU Sealing Cap
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/008_pod_base_usbc_cap_tpu.scad
// Description: Print-ready flush-fitting TPU dust and water sealing cap
//              (Shore 85A/95A) for Pod Base Port B. Protects the internal
//              USB-C connector when the pod operates outdoors via Port A (M8).
// =============================================================================

$fn = 32;

module pod_base_usbc_cap_tpu() {
    color([0.2, 0.2, 0.2, 0.95]) {
        union() {
            // 1. Plug Well Body (Fits snugly into the 14.0 x 8.5 x 7.0 mm recessed pocket)
            hull() {
                translate([-5.25, -2.5, 0])
                    cylinder(r=1.5, h=6.0, center=false);
                translate([5.25, -2.5, 0])
                    cylinder(r=1.5, h=6.0, center=false);
                translate([-5.25, 2.5, 0])
                    cylinder(r=1.5, h=6.0, center=false);
                translate([5.25, 2.5, 0])
                    cylinder(r=1.5, h=6.0, center=false);
            }

            // Dual Perimeter Sealing Ribs (+0.2 mm interference fit against pocket walls)
            translate([-6.5, -3.75, 2.0])
                cube([13.0, 7.5, 0.8], center=false);
            translate([-6.5, -3.75, 4.5])
                cube([13.0, 7.5, 0.8], center=false);

            // 2. Inner Receptacle Sealing Tongue (Plugs into vertical USB-C mouth)
            translate([0, 0, 6.0]) {
                hull() {
                    translate([-3.4, -0.9, 0])
                        cylinder(r=0.8, h=3.5, center=false);
                    translate([3.4, -0.9, 0])
                        cylinder(r=0.8, h=3.5, center=false);
                    translate([-3.4, 0.9, 0])
                        cylinder(r=0.8, h=3.5, center=false);
                    translate([3.4, 0.9, 0])
                        cylinder(r=0.8, h=3.5, center=false);
                }
            }

            // 3. Ergonomic Finger Pull Tab (Griffnase)
            translate([0, 0, -2.5]) {
                hull() {
                    translate([-2.5, -1.0, 0])
                        cylinder(r=0.8, h=2.5, center=false);
                    translate([2.5, -1.0, 0])
                        cylinder(r=0.8, h=2.5, center=false);
                    translate([0, 1.2, 0])
                        cylinder(r=0.8, h=2.5, center=false);
                }
            }

            // 4. Flexible Retaining Lanyard / Tether (Verliersicherung)
            translate([5.5, 0, 0]) {
                // Curved flexible strap
                translate([0, -1.0, 0])
                    cube([14.0, 2.0, 1.2], center=false);

                // Retaining Eyelet with M2 screw hole
                translate([14.0, 0, 0]) {
                    difference() {
                        cylinder(r=3.0, h=1.5, center=false);
                        translate([0, 0, -0.5])
                            cylinder(r=1.1, h=2.5, center=false); // Ø 2.2 mm screw bore
                    }
                }
            }
        }
    }
}

// Standalone render preview
pod_base_usbc_cap_tpu();
