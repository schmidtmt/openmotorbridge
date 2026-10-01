// =============================================================================
// OpenMotorBridge - Satellite Pod: 4x EPDM Strap Hook Lugs (Einhängenasen)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/005_pod_strap_hooks.scad
// Description: 4 integrated side hook lugs for toolless EPDM rubber ring &
//              ladder strap attachment on motorcycle frame tubes and crash bars.
// =============================================================================

module pod_strap_hook_lugs(length=100.0, width=60.0, hook_w=8.0, hook_out=3.0, hook_h=4.5) {
    // 4 Hook locations: 2 on Left flank (y = 0), 2 on Right flank (y = width)
    x_positions = [25.0, length - 25.0];

    for (x = x_positions) {
        // Left Flank Hooks (y = 0, pointing up +Z)
        translate([x - hook_w/2.0, -hook_out, 1.5]) {
            difference() {
                union() {
                    // Base protrusion overlapping 2.5 mm into wall
                    cube([hook_w, hook_out + 2.5, hook_h], center=false);
                    // Upward retaining lip
                    translate([0, 0, hook_h - 1.0])
                        cube([hook_w, 1.5, 2.5], center=false);
                }
                // Chamfer bottom edge
                translate([-0.1, 0, -0.1])
                    rotate([45, 0, 0])
                        cube([hook_w + 0.2, 2.0, 2.0], center=false);
            }
        }

        // Right Flank Hooks (y = width, pointing up +Z)
        translate([x - hook_w/2.0, width - 2.5, 1.5]) {
            difference() {
                union() {
                    // Base protrusion overlapping 2.5 mm into wall
                    cube([hook_w, hook_out + 2.5, hook_h], center=false);
                    // Upward retaining lip
                    translate([0, hook_out + 1.0, hook_h - 1.0])
                        cube([hook_w, 1.5, 2.5], center=false);
                }
                // Chamfer bottom edge
                translate([-0.1, hook_out + 2.4, -0.1])
                    rotate([-45, 0, 0])
                        cube([hook_w + 0.2, 2.0, 2.0], center=false);
            }
        }
    }
}

// Standalone preview
pod_strap_hook_lugs();
