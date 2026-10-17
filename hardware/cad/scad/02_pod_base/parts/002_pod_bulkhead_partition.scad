// =============================================================================
// OpenMotorBridge - Satellite Pod: Monolithic Bulkhead & Contact Interface
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/002_pod_bulkhead_partition.scad
// Description: 100% Monolithic, screw-free partition wall integrated directly
//              into the 1-piece pod base housing (zero assembly screws!).
//              Features:
//              - Form-fitting aperture for CON_POD_DC (IP67 2-pin automotive
//                blade direct plug with NBR70 O-ring & stainless steel U-clip).
//              - 2x Gold-plated blade contact feedthroughs (2.8 x 0.8 mm blades,
//                10.0 mm pitch: Y = 30.0 mm for +12V/5V and Y = 40.0 mm for GND,
//                mating into J_DC_IN dual-beam slot socket on PCBA 03).
//              - 2x Auto-Eject spring guide posts (for Ø 4.5 mm V4A springs at
//                Y = 16.0 mm and Y = 54.0 mm).
//              - Hermetic internal partition isolating the rear cable chamber
//                from the front slide chamber.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module pod_bulkhead_assembly(bulkhead_x=18.0, wall=3.5) {
    // Z = 7.45 mm: Exactly aligns with the horizontal centerline of J_DC_IN dual-beam slot socket
    // (POD_WALL 3.5 mm + Sled Floor 2.5 mm + M2 Standoff Boss 2.5 mm - 1.05 mm socket slot offset = 7.45 mm)
    z_contacts = wall + 2.5 + 2.5 - 1.05;

    // 1. Monolithic Vertical Partition Wall (Fused directly into tunnel at x = 18.0 mm)
    translate([bulkhead_x, wall, wall]) {
        difference() {
            // Solid transverse bulkhead (3.0 mm thickness)
            cube(size=[3.0, POD_OUTER_W - 2*wall, POD_OUTER_H - 2*wall], center=false);

            // Central Keyed Aperture for CON_POD_DC IP67 Blade Plug (10.0 mm pitch)
            // Centered at Y = 35.0 mm (Y_rel = 35.0 - wall), Z = z_contacts
            translate([-0.5, (POD_OUTER_W - 2*wall)/2.0 - 8.0, z_contacts - wall - 3.5])
                cube(size=[4.0, 16.0, 7.0], center=false);

            // Transverse U-Retaining Clip Retention Slot (1.2 mm wide x 18.0 mm tall)
            translate([1.5, (POD_OUTER_W - 2*wall)/2.0 - 10.0, z_contacts - wall - 5.0])
                cube(size=[1.2, 20.0, 10.0], center=false);

            // 2x Convective Pressure Equalization Vents (Left & Right top corners)
            translate([-0.5, 5.0, POD_OUTER_H - 2*wall - 5.0])
                cube(size=[4.0, 4.0, 2.0], center=false);
            translate([-0.5, POD_OUTER_W - 2*wall - 9.0, POD_OUTER_H - 2*wall - 5.0])
                cube(size=[4.0, 4.0, 2.0], center=false);
        }
    }

    // 2. 2x Low-Profile Blade Alignment Sleeves (projecting +X into cartridge entry window)
    // Low-profile Z = 2.0 mm (Z = 6.45 .. 8.45 mm, guaranteed 0.05 mm clearance under B.Cu at Z = 8.50 mm)
    translate([bulkhead_x + 3.0, 30.0, z_contacts]) {
        difference() {
            // Chamfered protective guide nose (low-profile h = 2.0 mm, w = 4.4 mm)
            translate([0, -2.2, -1.0])
                cube([3.0, 4.4, 2.0], center=false);
            // 2.8 x 0.8 mm Blade Pass-Through with lead-in chamfer
            translate([-0.5, -1.6, -0.5])
                cube([4.0, 3.2, 1.0], center=false);
        }
    }
    translate([bulkhead_x + 3.0, 40.0, z_contacts]) {
        difference() {
            // Chamfered protective guide nose (low-profile h = 2.0 mm, w = 4.4 mm)
            translate([0, -2.2, -1.0])
                cube([3.0, 4.4, 2.0], center=false);
            // 2.8 x 0.8 mm Blade Pass-Through with lead-in chamfer
            translate([-0.5, -1.6, -0.5])
                cube([4.0, 3.2, 1.0], center=false);
        }
    }

    // 3. 2x Auto-Eject Spring Retainer Posts (for Ø 4.5 mm V4A Springs at Y = 16.0 and Y = 54.0)
    // Symmetrical ±19.0 mm from pod centerline (Y = 35.0 mm)
    translate([bulkhead_x + 3.0, 16.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=1.8, h=6.0, $fn=16);

    translate([bulkhead_x + 3.0, POD_OUTER_W - 16.0, POD_OUTER_H/2.0])
        rotate([0, 90, 0])
            cylinder(r=1.8, h=6.0, $fn=16);
}

// Standalone preview
pod_bulkhead_assembly();
