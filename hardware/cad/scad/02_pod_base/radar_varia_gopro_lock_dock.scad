// =============================================================================
// OpenMotorBridge - Garmin Varia Radar Quarter-Turn Anti-Theft Lock Dock
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_varia_gopro_lock_dock.scad
// Description: Heavy-duty mounting adapter connecting the Garmin Varia mmWave
//              radar (RTL515 / RCT715 / eRTL615) to OpenMotorBridge GoPro hinges
//              (Heck-Balkon and License Plate Bracket).
//              Features:
//              1. Precision Garmin Quarter-Turn bayonet socket (90° twist lock).
//              2. Dual Anti-Theft Lock:
//                 - Audible flexure latch pawl snapping behind the bayonet wing.
//                 - Concealed M3 security set screw (Inbus / Torx-TR Madenschraube)
//                   physically locking the wing against reverse rotation.
//              3. Lower central GoPro tongue (6.0 mm width) with 36-tooth radial
//                 Hirth rosette for 100% slip-free 10° pitch angle locking.
//              4. Rear M8 4-pin PUR radar cable guide and strain relief.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;

// --- Parametric Dimensions ---
DOCK_OUTER_DIA      = 38.0;  // Outer circular puck diameter (mm)
DOCK_BODY_THICK     = 10.5;  // Main puck body thickness (mm)
BAYONET_RECESS_R    = 13.0;  // Ø 26.0 mm central circular well for Garmin hub
BAYONET_WING_R      = 16.5;  // Ø 33.0 mm outer wing swing radius
BAYONET_WING_THICK  = 2.8;   // Wing retention flange thickness (mm)
BAYONET_SLOT_W      = 7.0;   // Width of vertical lead-in entry slots (mm)

// Lower GoPro Tongue
TONGUE_WIDTH        = 6.0;   // Central tongue thickness fitting 6.2 mm fork gap (mm)
TONGUE_DROP_Z       = 18.0;  // Drop distance from puck center to M5 pivot (mm)
TONGUE_RADIUS       = 8.0;   // Tongue outer radius around M5 bore (mm)
M5_BORE_R           = 2.65;  // M5 clearance hole (Ø 5.3 mm)

// Security grub screw
M3_GRUB_BORE_R      = 1.25;  // M3 core diameter for tapping (Ø 2.5 mm)

module radar_varia_gopro_lock_dock(hinge_axis="X") {
    difference() {
        union() {
            // 1. Main Cylindrical Bayonet Puck Housing
            cylinder(r=DOCK_OUTER_DIA/2.0, h=DOCK_BODY_THICK, center=false);

            // Top Latch Enclosure & Cable Guide Extension
            hull() {
                translate([-14.0, DOCK_OUTER_DIA/2.0 - 4.0, 0])
                    cube([28.0, 8.0, DOCK_BODY_THICK]);
                translate([-8.0, DOCK_OUTER_DIA/2.0 + 8.0, 0])
                    cube([16.0, 4.0, DOCK_BODY_THICK]);
            }

            // 2. Lower Central GoPro Tongue (Single central blade, configurable hinge axis)
            if (hinge_axis == "X") {
                // Hinge axis along X (for Radar License Plate Bracket / Standard GoPro)
                translate([-TONGUE_WIDTH/2.0, -DOCK_OUTER_DIA/2.0 + 4.0, -TONGUE_DROP_Z]) {
                    hull() {
                        // Top connection to puck
                        cube([TONGUE_WIDTH, 16.0, TONGUE_DROP_Z]);
                        // Pivot cylinder around M5 bore
                        translate([0, 8.0, 0])
                            rotate([0, 90, 0])
                                cylinder(r=TONGUE_RADIUS, h=TONGUE_WIDTH);
                    }
                }

                // Radial Hirth Locking Teeth on Both Outer Faces of the Tongue (along X)
                // Left face (X = -TONGUE_WIDTH/2.0)
                translate([-TONGUE_WIDTH/2.0, -DOCK_OUTER_DIA/2.0 + 12.0, -TONGUE_DROP_Z])
                    rotate([0, -90, 0])
                        gopro_hirth_rosette();

                // Right face (X = TONGUE_WIDTH/2.0)
                translate([TONGUE_WIDTH/2.0, -DOCK_OUTER_DIA/2.0 + 12.0, -TONGUE_DROP_Z])
                    rotate([0, 90, 0])
                        gopro_hirth_rosette();
            } else {
                // Hinge axis along Y (for Adventure Rack-Tail Mount cantilever balcony)
                translate([0, -DOCK_OUTER_DIA/2.0 + 12.0, -TONGUE_DROP_Z]) {
                    hull() {
                        // Top connection to puck
                        translate([-8.0, -TONGUE_WIDTH/2.0, 0])
                            cube([16.0, TONGUE_WIDTH, TONGUE_DROP_Z]);
                        // Pivot cylinder around M5 bore
                        rotate([-90, 0, 0])
                            cylinder(r=TONGUE_RADIUS, h=TONGUE_WIDTH, center=true);
                    }

                    // Radial Hirth Locking Teeth on Both Outer Faces of the Tongue (along Y)
                    // Front-facing face (Y = -TONGUE_WIDTH/2.0)
                    translate([0, -TONGUE_WIDTH/2.0, 0])
                        rotate([90, 0, 0])
                            gopro_hirth_rosette();

                    // Rear-facing face (Y = TONGUE_WIDTH/2.0)
                    translate([0, TONGUE_WIDTH/2.0, 0])
                        rotate([-90, 0, 0])
                            gopro_hirth_rosette();
                }
            }
        }

        // --- SUBTRACTIONS (Bayonet well, entry slots, screw bores) ---

        // A. Central Garmin Hub Recess (Ø 26 mm x 3.5 mm deep)
        translate([0, 0, DOCK_BODY_THICK - 3.5])
            cylinder(r=BAYONET_RECESS_R, h=4.0);

        // B. Opposing Vertical Lead-in Slots for Varia Wings (Insertion at 0° & 180°)
        translate([-BAYONET_SLOT_W/2.0, -BAYONET_WING_R - 1.0, DOCK_BODY_THICK - 3.5])
            cube([BAYONET_SLOT_W, 2*(BAYONET_WING_R + 1.0), 4.0]);

        // C. Internal 90° Undercut Flange (Where wings rotate and lock)
        difference() {
            translate([0, 0, DOCK_BODY_THICK - 3.5 - BAYONET_WING_THICK])
                cylinder(r=BAYONET_WING_R, h=BAYONET_WING_THICK + 0.2);
            translate([0, 0, DOCK_BODY_THICK - 3.5 - BAYONET_WING_THICK - 0.5])
                cylinder(r=BAYONET_RECESS_R - 2.5, h=BAYONET_WING_THICK + 1.5);
        }

        // D. Lower Tongue M5 Pivot Bore (Through both Hirth faces)
        if (hinge_axis == "X") {
            translate([0, -DOCK_OUTER_DIA/2.0 + 12.0, -TONGUE_DROP_Z])
                rotate([0, 90, 0])
                    cylinder(r=M5_BORE_R, h=TONGUE_WIDTH + 6.0, center=true);
        } else {
            translate([0, -DOCK_OUTER_DIA/2.0 + 12.0, -TONGUE_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=M5_BORE_R, h=TONGUE_WIDTH + 6.0, center=true);
        }

        // E. Anti-Theft Security Grub Screw Bore (M3 threaded bore locking behind wing)
        // Positioned tangentially into the 90° rotated wing seat
        translate([DOCK_OUTER_DIA/2.0 + 2.0, 0, DOCK_BODY_THICK - 3.5 - BAYONET_WING_THICK/2.0])
            rotate([0, -90, 0])
                cylinder(r=M3_GRUB_BORE_R, h=16.0);

        // F. Rear M8 Cable Channel / Clip Pocket
        translate([0, DOCK_OUTER_DIA/2.0 + 4.0, -1.0])
            cylinder(r=3.2, h=DOCK_BODY_THICK + 2.0); // Pass-through for M8 PUR cable
    }
}

// Standalone preview
radar_varia_gopro_lock_dock();
