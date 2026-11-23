// =============================================================================
// OpenMotorBridge - Radar 2.0 Vibration Isolation Elastomer Pad
// =============================================================================
// File: hardware/cad/scad/02_pod_base/radar_vibration_damping_pad.scad
// Description: Laser-cut / die-cut EPDM (Shore 60A/70A) or 3D-printed TPU 85A
//              vibration damping pad sandwiched between the heavy-duty
//              swivel cradle (radar_swivel_tilt_cradle.scad) and the
//              sealed Radar 2.0 housing (radar_mr20_housing.scad).
//
// Function:
// 1. Decouples high-frequency motorcycle engine harmonics (50 - 250 Hz,
//    Harley V2 Milwaukee-Eight, Boxer, single-cylinder) from transmitting into
//    the Wheeltec MR20 77-GHz mmWave radar module.
// 2. Eliminates Doppler phase noise and FFT target velocity spreading.
// 3. Dual-layer architecture: Rigid Hirth rosette maintains precision pitch
//    angle (+/- 2 deg) against wind/drag; EPDM pad dampens micro-vibrations.
// =============================================================================

include <../00_common/parameters.scad>;

PAD_W           = 58.0;  // Total pad width in X (mm, matches cradle plate)
PAD_H           = 40.0;  // Total pad height in Z (mm, matches cradle plate)
PAD_THICK       = 2.0;   // Damping pad thickness in Y (mm)
PAD_CORNER_R    = 4.0;   // Corner fillet radius (mm)

REAR_M4_PITCH   = 40.0;  // Symmetrical spacing between M4 mounting screws (mm)
M4_CUTOUT_R     = 6.0;   // Clearance radius around M4 boss / bushing (mm)
GARMIN_CLEAR_R  = 17.0;  // Central clearance radius for Ø 34 mm Garmin well (mm)

module radar_vibration_damping_pad() {
    difference() {
        // 1. Solid Elastomer Base Plate in X-Z plane (thickness along +Y)
        hull() {
            for (sx = [-PAD_W/2 + PAD_CORNER_R, PAD_W/2 - PAD_CORNER_R]) {
                for (sz = [-PAD_H/2 + PAD_CORNER_R, PAD_H/2 - PAD_CORNER_R]) {
                    translate([sx, 0, sz])
                        rotate([-90, 0, 0])
                            cylinder(r=PAD_CORNER_R, h=PAD_THICK, center=false, $fn=32);
                }
            }
        }

        // 2. Central Garmin Quarter-Turn Bayonet Clearance Cutout
        translate([0, -0.5, 0])
            rotate([-90, 0, 0])
                cylinder(r=GARMIN_CLEAR_R, h=PAD_THICK + 1.0, center=false, $fn=48);

        // 3. Symmetrical M4 Boss Clearance Cutouts (Pitch: 40.0 mm)
        for (dx = [-REAR_M4_PITCH/2, REAR_M4_PITCH/2]) {
            translate([dx, -0.5, 0])
                rotate([-90, 0, 0])
                    cylinder(r=M4_CUTOUT_R, h=PAD_THICK + 1.0, center=false, $fn=32);
        }
    }
}

// Standalone render
color([0.15, 0.15, 0.16, 0.95])
    radar_vibration_damping_pad();
