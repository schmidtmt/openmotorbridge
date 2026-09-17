// =============================================================================
// OpenMotorBridge - Adventure Kit Master 3D Assembly & Fitting Inspection
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_adventure_kit_assembly.scad
// Description: Comprehensive photorealistic 3D visualization scene displaying
//              all three Adventure Mounting Configurations side by side:
//
//   [1] CONFIG A (Left): BMW GSA / Heavy-Duty Pannier Rack Clamp
//       - Ø 18 mm stainless steel pannier rack tube (Roll-cage crash protection)
//       - Heavy-duty clamp pair (base + cap) with dual M5 bolts & locknuts
//       - Pod 1 Base Housing with M8 PUR cable & inserted Sena 60S Cartridge
//
//   [2] CONFIG B (Center): Standard BMW GS Transition Dock (Sitzbank-Bügelfalte)
//       - Ø 28 mm subframe tube & under-seat mounting interface
//       - Ergonomic waist-crease carrier cradle (100% pannier-independent)
//       - Pod 2 Base Housing with Cardo Packtalk Edge Cartridge
//
//   [3] CONFIG C (Right): Luggage Rack-Tail Mount ("Heck-Balkon" behind Topcase)
//       - 65 mm cantilever extension holding Pod 3 clear behind aluminum topcase
//       - 45° Astabweiser-Finne protecting the +5 dBi 2.4 GHz dipole antenna
//       - Rear Pod 3 Transceiver Cartridge (u-blox MAX-M10S GNSS & SX1262 LoRa)
//       - Underside M5 GoPro swivel hinge with 36-tooth Hirth anti-slip lock
//       - Garmin Varia mmWave radar with quarter-turn anti-theft dock
// =============================================================================

include <../00_common/parameters.scad>;
use <adventure_pannier_rack_clamp.scad>;
use <adventure_gsa_cage_dock.scad>;
use <adventure_transition_dock.scad>;
use <adventure_underseat_cross_rail.scad>;
use <adventure_rack_tail_mount.scad>;
use <pod_base_housing.scad>;
use <radar_varia_gopro_lock_dock.scad>;
use <parts/011_gopro_hirth_lock.scad>;
use <../03_pod_cartridges/cartridge_sena.scad>;
use <../03_pod_cartridges/cartridge_cardo.scad>;
use <../03_pod_cartridges/cartridge_omm_transceiver.scad>;
use <../00_common/dummies/dummy_m8_connector.scad>;

// Parametric References from adventure_rack_tail_mount
RTM_POD_L           = 136.5;
RTM_POD_W           = 71.5;
RTM_WALL            = 3.5;
RTM_SPLIT_Z         = 20.0;
RTM_TOTAL_H         = 43.0;
FIN_BASE_L          = 34.0;
FIN_HEIGHT          = 32.0;
RADAR_DROP_Z        = 22.0;
TD_POD_L            = 136.0;
TD_POD_W            = 71.0;

// View Selector: "ALL", "GSA_CLAMP", "GS_TRANSITION", "RACK_TAIL_RADAR"
VIEW_MODE = "ALL";

// Dummy Garmin Varia Radar Unit (Sleek aerodynamic housing)
module dummy_garmin_varia_radar() {
    color("#11151c", 0.95) {
        hull() {
            translate([0, 0, -10.0]) cylinder(r=16.0, h=30.0, center=true, $fn=32);
            translate([0, 0, -42.0]) cylinder(r=13.0, h=25.0, center=true, $fn=32);
        }
    }
    // High-Intensity Rear LED Light Ring & Strobe Window
    color("crimson", 0.9)
        translate([0, 8.5, -20.0])
            rotate([90, 0, 0])
                cylinder(r=9.0, h=2.0, center=true, $fn=24);

    // Quarter-turn mounting puck on back
    color("#2c3440", 1.0)
        translate([0, -8.5, -20.0])
            rotate([-90, 0, 0])
                cylinder(r=14.0, h=4.0, center=true, $fn=24);
}

// -----------------------------------------------------------------------------
// CONFIG A: GSA Stainless Steel Pannier Rack Clamp Installation
// -----------------------------------------------------------------------------
module adventure_config_a_gsa_rack() {
    // 1. Ø 18 mm Stainless Steel Rack Tube Structure (Touratech / OEM GSA)
    color("lightgray", 0.95) {
        // Main longitudinal carrier tube running through the dual clamps
        translate([-30.0, -11.1, 22.0])
            rotate([0, 90, 0])
                cylinder(r=9.0, h=220.0, center=false, $fn=32);

        // Vertical strut tube at rear
        translate([-30.0, -11.1, -80.0])
            cylinder(r=9.0, h=180.0, center=false, $fn=32);

        // Diagonal cross-brace tube at 50°
        translate([130.0, -11.1, 22.0])
            rotate([0, 50, 0])
                cylinder(r=9.0, h=140.0, center=false, $fn=32);
    }

    // 2. Heavy-Duty Armored Cage Dock (PA12-CF Exoskeleton with Dual Clamps)
    adventure_gsa_cage_dock(part = "assembly");

    // 3. Pod 1 Base Housing (Deeply recessed inside the armored cage)
    translate([12.0, 7.5, 4.0]) {
        color("slategray", 0.85)
            pod_base_housing();

        // M8 Industrial PUR Cable at Port A (routes in tube shadow forward)
        translate([0, POD_OUTER_W/2.0 - 8.0, POD_OUTER_H/2.0])
            rotate([0, 180, 0])
                dummy_m8_connector();

        // 4. Sena 60S Wave 3.0 Cartridge (Pushed into slot)
        translate([POD_BULKHEAD_X + 2.0, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
            cartridge_sena_assembly(exploded = false);
        }
    }
}

// -----------------------------------------------------------------------------
// CONFIG B: Standard GS Transition Dock (Sitzbank-Bügelfalte & Sattelbrücke)
// -----------------------------------------------------------------------------
module adventure_config_b_transition_dock() {
    // 1. Dual Ø 28 mm Rear Subframe Trellis (Left & Right tubes at 10° rise angle)
    color("#404756", 0.95) {
        // Right frame tube (where the dock rests)
        translate([0, 0, -10.0])
            rotate([0, 80, 0])
                cylinder(r=14.0, h=260.0, center=true, $fn=32);

        // Left frame tube (Opposite flank under seat, 200 mm span)
        translate([0, -200.0, -10.0])
            rotate([0, 80, 0])
                cylinder(r=14.0, h=260.0, center=true, $fn=32);
    }

    // 2. Under-Seat Cross-Rail (Sattelbrücke - 100% hidden beneath seat foam)
    translate([0, -100.0, 0.0]) {
        color("#222831", 0.92)
            adventure_underseat_cross_rail();

        // Fastening hardware: 2x M4 stainless bolts connecting dock tongue to rail
        color("silver") {
            for (dx = [-12.0, 12.0]) {
                translate([dx, 46.0, -2.0])
                    cylinder(r=2.0, h=10.0, center=true, $fn=16);
            }
        }
    }

    // 3. Adventure Transition Dock (Sculpted OEM Console: Base + Styled Lid)
    // Aligned along the subframe tube at the seat waist crease
    translate([-TD_POD_L/2.0 + 8.0, 0, 0]) {
        // Base Cradle & Upper Styled Lid
        adventure_transition_dock(part = "assembly", side = "right", lid_variant = "open_intercom");

        // 4. Pod 2 Base Housing (Nested inside the sculpted console)
        translate([0, -TD_POD_W/2.0, 3.5]) {
            color("slategray", 0.85)
                pod_base_housing();

            // M8 Cable at Port A routing into the under-seat bridge channel
            translate([0, POD_OUTER_W/2.0 - 8.0, POD_OUTER_H/2.0])
                rotate([0, 180, 0])
                    dummy_m8_connector();

            // 5. Cardo DMC Gen2 Cartridge (Flush inside the lid's sculpted bezel)
            translate([POD_BULKHEAD_X + 2.0, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
                cartridge_cardo_assembly(exploded = false);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// CONFIG C: Luggage Rack-Tail Mount ("Heck-Balkon" with Astabweiser & Radar)
// -----------------------------------------------------------------------------
module adventure_config_c_rack_tail_radar() {
    // 1. BMW GS Tubular Stainless Steel Luggage Rack Structure (Ø 18 mm tubes)
    color("lightgray", 0.95) {
        // Transverse rear rack tube (where the mounting flange clamps onto)
        translate([-42.0, 0, 0])
            rotate([90, 0, 0])
                cylinder(r=9.0, h=170.0, center=true, $fn=32);

        // Left longitudinal rack carrier tube
        translate([-130.0, -45.0, 0])
            rotate([0, 90, 0])
                cylinder(r=9.0, h=100.0, center=false, $fn=32);

        // Right longitudinal rack carrier tube
        translate([-130.0, 45.0, 0])
            rotate([0, 90, 0])
                cylinder(r=9.0, h=100.0, center=false, $fn=32);

        // Diagonal rack support struts
        for (side = [-1, 1]) {
            translate([-110.0, side * 45.0, -70.0])
                rotate([0, 40, 0])
                    cylinder(r=8.0, h=110.0, center=false, $fn=24);
        }
    }

    // 2. Aluminum Topcase Reference Floor & Rear Lip (Touratech Zega / BMW Adventure)
    // Low-profile base contour clearly shows the topcase boundary while leaving the
    // entire Rallye-Aero-Balkon, clamp flange, and radar 100% visible!
    color("silver", 0.9) {
        // Lower aluminum bottom tray of topcase
        translate([-165.0, -80.0, 8.0])
            cube([115.0, 160.0, 5.0]);
        // Lower rear edge extrusion & lid seal lip (height 28 mm)
        translate([-53.0, -80.0, 8.0])
            cube([4.0, 160.0, 28.0]);
        // Black polymer corner crash protectors
        color("#222831") {
            for (side = [-1, 1]) {
                translate([-54.0, side * 75.0 - 5.0, 8.0])
                    cube([6.0, 10.0, 24.0]);
            }
        }
    }

    // 3. Adventure Rack-Tail Mount (Two-Piece Rallye-Aero-Balkon)
    // Clamped securely to the Ø 18 mm transverse rack tube
    translate([-14.0, 0, 0]) {
        // Complete Two-Piece Aero Assembly (Base Cradle + Sculpted Aero Cowl)
        adventure_rack_tail_mount(part = "assembly");

        // 2x M6 V4A Mounting Bolts in Flange Slots
        color("silver") {
            for (offset_y = [-40.0, 40.0]) {
                translate([-28.0, offset_y, 7.5])
                    cylinder(r=5.0, h=4.0, center=true, $fn=24);
            }
        }

        // 4. Dipol 2.4 GHz +5 dBi Antenna (Accent cyan nested inside Astabweiser Fin)
        color("#00adb5", 0.95) {
            translate([RTM_POD_L - 8.0 + FIN_BASE_L/2.0 + 2.0, 0, (RTM_TOTAL_H - RTM_SPLIT_Z + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0])
                    cylinder(r=4.8, h=52.0, center=true, $fn=20);
        }

        // 5. Underside M5 GoPro Hinge with 36-Tooth Hirth Anti-Slip Lock & Garmin Varia Radar
        translate([RTM_POD_L/2.0 + 8.0, 0, -RADAR_DROP_Z]) {
            // GoPro Quarter-Turn Anti-Theft Lock Adapter Dock
            rotate([0, 10, 0]) { // 10° Pitch Trim for Level Radar Horizon
                color("#2b323c", 0.95)
                    radar_varia_gopro_lock_dock(hinge_axis = "X");

                // M5 Lock Bolt with Hirth Engagement Disc
                color("silver") {
                    rotate([-90, 0, 0])
                        cylinder(r=2.5, h=28.0, center=true, $fn=16);
                }

                // Garmin Varia Radar Unit (Symmetrically positioned under Pod 3)
                translate([0, 0, -28.0])
                    dummy_garmin_varia_radar();
            }
        }
    }
}

// -----------------------------------------------------------------------------
// MASTER 3D SCENE COMPOSITION
// -----------------------------------------------------------------------------
module adventure_kit_master_scene() {
    if (VIEW_MODE == "GSA_CLAMP") {
        adventure_config_a_gsa_rack();
    } else if (VIEW_MODE == "GS_TRANSITION") {
        adventure_config_b_transition_dock();
    } else if (VIEW_MODE == "RACK_TAIL_RADAR") {
        adventure_config_c_rack_tail_radar();
    } else {
        // Full Side-by-Side Studio Stage View with balanced spacing (280 mm span)
        // Left (-280 mm): GSA Rohrträger-Klemmschelle
        translate([-280.0, 0, 0])
            adventure_config_a_gsa_rack();

        // Center (0 mm): Standard-GS Transition Dock
        translate([0, 0, 0])
            adventure_config_b_transition_dock();

        // Right (+280 mm): Gepäckbrücken-Ausleger "Heck-Balkon" & Radar
        translate([280.0, 0, 0])
            adventure_config_c_rack_tail_radar();
    }
}

// Render the complete assembly
adventure_kit_master_scene();

