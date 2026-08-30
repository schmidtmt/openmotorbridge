// =============================================================================
// OpenMotorBridge - Satellite Pod: Monocoque Tunnel Base
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/000_pod_tunnel_base.scad
// =============================================================================

include <../../00_common/parameters.scad>;

module pod_tunnel_base(length=100.0, width=60.0, height=28.0, wall=2.5) {
    difference() {
        // 1. Solid Outer Enclosure Body (100 x 60 x 28 mm)
        cube(size=[length, width, height], center=false);

        // 2. Hollow Internal Chamber (Open at front mouth +X)
        translate([wall, wall, wall]) {
            cube(size=[length - wall + 0.1, width - 2*wall, height - 2*wall], center=false);
        }
    }
}

// Standalone preview
pod_tunnel_base();
