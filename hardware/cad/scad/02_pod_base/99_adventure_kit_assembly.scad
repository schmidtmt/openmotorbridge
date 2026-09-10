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
use <adventure_transition_dock.scad>;
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
RTM_RIM_H           = 18.0;
FIN_BASE_L          = 28.0;
FIN_HEIGHT          = 32.0;
RADAR_DROP_Z        = 22.0;

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
    // 1. Ø 18 mm Stainless Steel Rack Tube (Touratech / OEM GSA)
    color("lightgray", 0.95) {
        translate([0, 0, -120.0])
            cylinder(r=9.0, h=240.0, center=false, $fn=32);
        // Cross brace tube at 60°
        rotate([0, 60, 0])
            translate([-9.0, 0, -40.0])
                cylinder(r=9.0, h=160.0, center=false, $fn=32);
    }

    // 2. Heavy-Duty Ø 18 mm Clamping Shells (PA12-CF)
    translate([0, 0, 0]) {
        color("#222831", 0.95)
            adventure_pannier_rack_clamp_base();
        color("#222831", 0.95)
            translate([0, 0, -2.0])
                rotate([180, 0, 0])
                    adventure_pannier_rack_clamp_cap();
    }

    // Clamping Hardware (2x M5 DIN 912 socket bolts & DIN 985 locknuts)
    color("silver") {
        for (y_pos = [-17.0, 17.0]) {
            translate([0, y_pos, -18.0])
                cylinder(r=2.5, h=38.0, $fn=16);
            translate([0, y_pos, 16.0])
                cylinder(r=4.5, h=4.0, $fn=16);
        }
    }

    // 3. Pod 1 Base Housing (Securely nested in the inner frame triangle)
    translate([12.0, -POD_OUTER_W/2.0, 20.0]) {
        color("slategray", 0.85)
            pod_base_housing();

        // M8 Industrial Pur-Cable at Port A
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
// CONFIG B: Standard GS Transition Dock (Sitzbank-Bügelfalte)
// -----------------------------------------------------------------------------
module adventure_config_b_transition_dock() {
    // 1. Ø 28 mm Rear Subframe Tube (R1250/1300 GS under-seat trellis)
    color("#404756", 0.95) {
        rotate([0, 80, 0])
            cylinder(r=14.0, h=260.0, center=true, $fn=32);
    }

    // 2. Adventure Transition Dock Cradle (PA12-CF)
    translate([-68.0, -42.0, 5.0]) {
        color("#1c222b", 0.95)
            adventure_transition_dock();

        // 3. Pod 2 Base Housing (Mounted inside dock)
        translate([3.2, 3.2, 3.5]) {
            color("slategray", 0.85)
                pod_base_housing();

            // M8 Cable at Port A
            translate([0, POD_OUTER_W/2.0 - 8.0, POD_OUTER_H/2.0])
                rotate([0, 180, 0])
                    dummy_m8_connector();

            // 4. Cardo DMC Gen2 Cartridge (Inserted)
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
    // 1. Emulated Aluminum Topcase Back Wall & Tubular Luggage Rack
    color("silver", 0.75) {
        // Vertical Topcase Back Wall (2 mm aluminum plate)
        translate([-90.0, -70.0, 12.0])
            cube([4.0, 140.0, 150.0]);
        // Topcase base lip
        translate([-90.0, -70.0, 8.0])
            cube([35.0, 140.0, 6.0]);
        // Rack transverse tube
        translate([-40.0, 0, 0])
            rotate([90, 0, 0])
                cylinder(r=9.0, h=160.0, center=true, $fn=32);
    }

    // 2. Adventure Rack-Tail Mount Cantilever Tray (PA12-CF)
    translate([-15.0, -42.0, 0]) {
        color("#1a1f26", 0.95)
            adventure_rack_tail_mount();

        // 3. Dipol 2.4 GHz +5 dBi Antenna (Snag-proof inside Astabweiser Fin)
        color("#00adb5", 0.95) {
            translate([RTM_POD_L + 2*RTM_WALL - 5.0 + FIN_BASE_L/2.0, (RTM_POD_W + 2*RTM_WALL)/2.0, (RTM_RIM_H + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0])
                    cylinder(r=4.8, h=46.0, center=true, $fn=16);
        }

        // 4. Pod 3 Base Housing (Horizontal in tray with clear sky view)
        translate([3.5, 3.5, 4.0]) {
            color("slategray", 0.85)
                pod_base_housing();

            // Rear Transceiver Cartridge (u-blox MAX-M10S & SX1262 LoRa)
            translate([POD_BULKHEAD_X + 2.0, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
                cartridge_omm_transceiver_assembly(exploded = false);
            }
        }

        // 5. Underside M5 GoPro Hinge with 36-Tooth Hirth Anti-Slip Lock & Garmin Varia Radar
        translate([RTM_POD_L/2.0 + RTM_WALL, (RTM_POD_W + 2*RTM_WALL)/2.0, -RADAR_DROP_Z]) {
            // GoPro Quarter-Turn Anti-Theft Lock Adapter Dock
            rotate([0, 12, 0]) { // 12° Pitch Trim for Level Radar Horizon
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
        // Full Side-by-Side Studio Stage View
        // Left (-160 mm): GSA Rohrträger-Klemmschelle
        translate([-160.0, 0, 0])
            adventure_config_a_gsa_rack();

        // Center (0 mm): Standard-GS Transition Dock
        translate([0, 0, 0])
            adventure_config_b_transition_dock();

        // Right (+190 mm): Gepäckbrücken-Ausleger "Heck-Balkon" & Radar
        translate([190.0, 0, 0])
            adventure_config_c_rack_tail_radar();
    }
}

// Render the complete assembly
adventure_kit_master_scene();
