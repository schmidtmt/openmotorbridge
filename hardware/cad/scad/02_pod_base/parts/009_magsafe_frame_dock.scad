// =============================================================================
// OpenMotorBridge - Satellite Pod: MagSafe Frame Dock (Under-Seat Breakaway Mount)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad
// Description: Stationary frame dock mounted under the seat overhang (Harley
//              Touring / CVO ST frame tube Ø 25.4 - 28.6 mm / 1" - 1.125").
//              Interfaces the bike-side M8 harness to the 6-pin IP67 MagSafe
//              magnetic breakaway coupling facing the saddlebag.
//              Releases smoothly at 10-15 N pull force during bag removal.
// =============================================================================

$fn = 40;

module magsafe_frame_dock(
    tube_dia = 26.0,         // Harley subframe tube diameter (mm)
    dock_len = 38.0,         // Total dock body length (mm)
    dock_w = 24.0,           // Total dock width (mm)
    dock_h = 22.0,           // Total dock height (mm)
    magsafe_w = 16.5,        // MagSafe magnetic connector width (mm)
    magsafe_h = 7.5,         // MagSafe magnetic connector height (mm)
    magsafe_depth = 8.0,     // Pocket depth for magnetic insert (mm)
    m8_bore_dia = 8.2        // M8 cable pass-through bore (mm)
) {
    difference() {
        union() {
            // 1. Main Solid Dock Monocoque Block with Rounded Edges
            hull() {
                translate([-dock_len/2 + 2, -dock_w/2 + 2, 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, -dock_w/2 + 2, 2])
                    sphere(r=2);
                translate([-dock_len/2 + 2, dock_w/2 - 2, 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, dock_w/2 - 2, 2])
                    sphere(r=2);

                translate([-dock_len/2 + 2, -dock_w/2 + 2, dock_h - 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, -dock_w/2 + 2, dock_h - 2])
                    sphere(r=2);
                translate([-dock_len/2 + 2, dock_w/2 - 2, dock_h - 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, dock_w/2 - 2, dock_h - 2])
                    sphere(r=2);
            }

            // 2. Dual Cable-Tie Flanges / Clamp Wings for Frame Tube
            translate([0, 0, dock_h]) {
                difference() {
                    cylinder(r=tube_dia/2 + 3.5, h=12.0, center=false);
                    translate([0, 0, -1])
                        cylinder(r=tube_dia/2, h=14.0, center=false);
                    // Split clamp opening
                    translate([-tube_dia - 5, -5, -1])
                        cube([2*(tube_dia + 5), 10, 15], center=false);
                }
            }
        }

        // 3. Saddlebag-Facing MagSafe Magnetic Receptacle Pocket (45° angle)
        translate([8.0, 0, 4.0]) {
            rotate([0, 25, 0]) {
                // Pocket for 6-pin magnetic connector with N52 magnets
                hull() {
                    translate([-(magsafe_depth+1), -(magsafe_w/2 - 1.5), -(magsafe_h/2 - 1.5)])
                        cylinder(r=1.5, h=magsafe_h - 3.0, center=false);
                    translate([-(magsafe_depth+1), (magsafe_w/2 - 1.5), -(magsafe_h/2 - 1.5)])
                        cylinder(r=1.5, h=magsafe_h - 3.0, center=false);
                    translate([2, -(magsafe_w/2 - 1.5), -(magsafe_h/2 - 1.5)])
                        cylinder(r=1.5, h=magsafe_h - 3.0, center=false);
                    translate([2, (magsafe_w/2 - 1.5), -(magsafe_h/2 - 1.5)])
                        cylinder(r=1.5, h=magsafe_h - 3.0, center=false);
                }

                // Lead-in alignment bevel (Einfädeltrichter for blind snap)
                translate([1.0, 0, 0])
                    hull() {
                        cube([3.0, magsafe_w + 3.0, magsafe_h + 3.0], center=true);
                        translate([-2.0, 0, 0])
                            cube([1.0, magsafe_w, magsafe_h], center=true);
                    }
            }
        }

        // 4. Rear Bike-Facing M8 Receptacle / Cable Channel (Ø 8.2 mm)
        translate([-dock_len/2 - 1.0, 0, dock_h/2]) {
            rotate([0, 90, 0])
                cylinder(r=m8_bore_dia/2, h=dock_len/2 + 5.0, center=false);
            // M8 Nut hex pocket / Thread recess
            rotate([0, 90, 0])
                cylinder(r=6.5, h=6.0, center=false);
        }

        // 5. Internal Wire Routing Chamber linking M8 port to MagSafe pocket
        translate([-2.0, 0, dock_h/2 - 2.0])
            cube([12.0, 10.0, 8.0], center=true);

        // 6. Dual Zip-Tie Slots (5.0 x 2.5 mm) for secure subframe mounting
        translate([-8.0, 0, dock_h + 4.0])
            cube([5.0, dock_w + 10.0, 2.8], center=true);
        translate([8.0, 0, dock_h + 4.0])
            cube([5.0, dock_w + 10.0, 2.8], center=true);
    }
}

// Standalone render preview
magsafe_frame_dock();
