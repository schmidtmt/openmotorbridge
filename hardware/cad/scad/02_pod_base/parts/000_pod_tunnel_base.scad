// =============================================================================
// OpenMotorBridge - Satellite Pod: Monocoque Tunnel Base with Tube Saddle
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/000_pod_tunnel_base.scad
// Description: 5-sided monocoque tunnel with integrated V-groove tube saddle,
//              zip-tie slots, and internal dual snap-fit catch pockets (Rasttaschen)
//              for the cartridge quick-release auto-eject mechanism.
// =============================================================================

include <../../00_common/parameters.scad>;

module pod_tunnel_base(length=100.0, width=60.0, height=28.0, wall=2.5, r_edge=3.0) {
    difference() {
        // 1. Solid Outer Enclosure Body with Rounded Corners (100 x 60 x 28 mm)
        hull() {
            translate([r_edge, r_edge, r_edge])
                sphere(r=r_edge, $fn=16);
            translate([length - r_edge, r_edge, r_edge])
                sphere(r=r_edge, $fn=16);
            translate([r_edge, width - r_edge, r_edge])
                sphere(r=r_edge, $fn=16);
            translate([length - r_edge, width - r_edge, r_edge])
                sphere(r=r_edge, $fn=16);

            translate([r_edge, r_edge, height - r_edge])
                sphere(r=r_edge, $fn=16);
            translate([length - r_edge, r_edge, height - r_edge])
                sphere(r=r_edge, $fn=16);
            translate([r_edge, width - r_edge, height - r_edge])
                sphere(r=r_edge, $fn=16);
            translate([length - r_edge, width - r_edge, height - r_edge])
                sphere(r=r_edge, $fn=16);
        }

        // 2. Hollow Internal Chamber (Open at front mouth +X)
        translate([wall, wall, wall]) {
            cube(size=[length - wall + 0.1, width - 2*wall, height - 2*wall], center=false);
        }

        // 3. Universal Tube Saddle / V-Groove Prism at Bottom (for Frame Tubes Ø 18 - 35 mm)
        translate([-1.0, width/2.0, -14.0]) {
            rotate([0, 90, 0])
                cylinder(r=15.0, h=length + 2.0, $fn=32);
        }

        // 4. Transverse Cable-Tie / Zip-Tie Slots (5.0 x 2.5 mm @ x = 20 mm & x = 80 mm)
        translate([20.0 - 2.5, -1.0, wall - 1.2])
            cube([5.0, width + 2.0, 2.5], center=false);
        translate([80.0 - 2.5, -1.0, wall - 1.2])
            cube([5.0, width + 2.0, 2.5], center=false);

        // 5. Dual Internal Snap-Fit Catch Pockets (Rasttaschen in Seitenwänden)
        // Left Internal Catch Pocket (x = 83.5 .. 88.5 mm, y = wall - 1.6 .. wall mm, z = 6.0 .. 17.0 mm)
        translate([83.5, wall - 1.6, 6.0])
            cube(size=[5.0, 1.8, 11.0], center=false);

        // Right Internal Catch Pocket (x = 83.5 .. 88.5 mm, y = width - wall .. width - wall + 1.6 mm)
        translate([83.5, width - wall - 0.2, 6.0])
            cube(size=[5.0, 1.8, 11.0], center=false);
    }
}

// Standalone preview
pod_tunnel_base();
