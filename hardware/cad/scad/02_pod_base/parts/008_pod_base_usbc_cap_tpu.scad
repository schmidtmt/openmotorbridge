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
            // 1. Outer Flush Flange (Fits inside the 12.0 x 6.5 x 2.5 mm pocket)
            hull() {
                translate([-4.3, -1.8, 0])
                    cylinder(r=1.2, h=2.0, center=false);
                translate([4.3, -1.8, 0])
                    cylinder(r=1.2, h=2.0, center=false);
                translate([-4.3, 1.8, 0])
                    cylinder(r=1.2, h=2.0, center=false);
                translate([4.3, 1.8, 0])
                    cylinder(r=1.2, h=2.0, center=false);
            }

            // 2. Inner Sealing Plug (Presses into USB-C receptacle opening)
            translate([0, 0, 2.0]) {
                hull() {
                    translate([-3.4, -0.9, 0])
                        cylinder(r=0.8, h=4.5, center=false);
                    translate([3.4, -0.9, 0])
                        cylinder(r=0.8, h=4.5, center=false);
                    translate([-3.4, 0.9, 0])
                        cylinder(r=0.8, h=4.5, center=false);
                    translate([3.4, 0.9, 0])
                        cylinder(r=0.8, h=4.5, center=false);
                }

                // Dual Sealing Ribs (Dichtlippen +0.2 mm interference fit)
                translate([-4.0, -1.5, 1.5])
                    cube([8.0, 3.0, 0.6], center=false);
                translate([-4.0, -1.5, 3.2])
                    cube([8.0, 3.0, 0.6], center=false);
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
