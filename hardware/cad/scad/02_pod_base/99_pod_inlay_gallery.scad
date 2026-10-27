// =============================================================================
// OpenMotorBridge - Satellite Pod: v10.0 Monocoque Inlay Gallery (4 Variants)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod_inlay_gallery.scad
// Description: Multi-variant 3D inspection gallery comparing all 4 real-world
//              configurations of the universal Monocoque Satellite Pod (Typ B):
//
// 1. Sena SPIDER X Slim Inlay (Contoured foam nest + direct PCBA 03 cable whip)
// 2. Cardo Packtalk Edge Inlay (OEM Air-Mount cradle + direct PCBA 03 harness)
// 3. OMM 2.4 GHz UCS Transceiver Inlay (Direct USB-C Class 2.0 digital audio)
// 4. Hermetische Mini-Dry-Box (Waterproof safe for motorcycle spare key, papers, fuses)
//
// Features:
// - Ergonomic front-wall cutaway window to reveal the spacious 145 x 65 mm interior
//   and the bottom PCBA 03 board with flat silicone ribbon wiring.
// - Port A: 4-Pin IP67 Magnet-Abrissschnittstelle (HytePro) with silicone ribbon.
// - Port B: Recessed USB-C fast-charge socket with TPU weather cap.
// - Optional rear SMA antenna port (sealed with 0.4 mm knockout membrane).
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <../00_common/dummies/dummy_intercom_units.scad>;
use <../03_pod_cartridges/parts/03_insert_blindkassette.scad>;
use <parts/008_pod_base_usbc_cap_tpu.scad>;
use <parts/014_pod_dry_flap.scad>;
use <parts/015_pod_monocoque_tub.scad>;

// 4-Pin IP67 Magnet-Abrissschnittstelle (HytePro Style)
module pod_port_a_magnetic_connector() {
    // 1. Molded Black PBT Flange Body (14.5 x 7.5 x 4.0 mm, flush in bulkhead)
    color([0.15, 0.15, 0.18]) {
        translate([-2.0, -7.25, -3.75])
            cube([4.0, 14.5, 7.5], center=false);
    }
    // 2. Dual Rare-Earth Alignment Magnets (Nickel-plated silver)
    color("silver") {
        translate([-2.1, -5.0, 0])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=1.0, center=false, $fn=16);
        translate([-2.1, 5.0, 0])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=1.0, center=false, $fn=16);
    }
    // 3. 4x Gold-Plated Pogo Contact Terminals (Pitch 2.2 mm)
    color("gold") {
        for (py = [-3.3, -1.1, 1.1, 3.3]) {
            translate([-2.2, py, 0])
                rotate([0, 90, 0])
                    cylinder(r=0.6, h=1.2, center=false, $fn=16);
        }
    }
    // 4. Internal 4-Conductor Silicone Flat-Ribbon Cable (leads to J_BUS)
    translate([2.0, -3.6, -1.0]) {
        for (i = [0:3]) {
            c_color = (i == 0) ? "red" : (i == 1) ? "white" : (i == 2) ? "green" : "black";
            color(c_color)
                translate([0, i * 1.8, 0])
                    cube([14.0, 1.4, 1.0], center=false);
        }
    }
}

// Single Monocoque Pod Chamber Base (with cutaway inspection window)
module pod_monocoque_base_setup() {
    // 1. Monocoque Tub with Ergonomic Front Inspection Cutout
    // This allows clear visibility of the full floor, PCBA 03, and the expansive 145 x 65 mm interior!
    difference() {
        color([0.28, 0.30, 0.33])
            pod_monocoque_tub();

        // Front longitudinal wall cutaway window (cuts down near wall for 100% visibility)
        translate([10.0, -5.0, 14.0])
            cube([POD_OUTER_L - 20.0, POD_WALL + 6.0, POD_OUTER_H]);
    }

    // 2. Port A: 4-Pin IP67 Magnet-Abrissschnittstelle (Bulkhead top, Z = 26.5 mm)
    translate([0.0, POD_OUTER_W/2.0, POD_OUTER_H/2.0 + 7.5])
        pod_port_a_magnetic_connector();

    // 3. Port B: Flush In-Bag USB-C Socket with Cap (Bulkhead bottom, Z = 11.5 mm)
    translate([0.5, POD_OUTER_W/2.0, POD_OUTER_H/2.0 - 7.5])
        rotate([0, 90, 90])
            pod_base_usbc_cap_tpu();

    // 4. Lower PCBA 03 Interface Board (Green 4-layer FR4 PCB with JST headers)
    translate([6.0, 11.0, POD_WALL + 2.5])
        dummy_adapter_pcb();

    // 5. Translucent Amber EPDM Dry-Flap Splash Shield (folded back / protective deck)
    translate([6.0, 7.0, 14.0])
        color([0.92, 0.68, 0.18, 0.65])
            pod_dry_flap();
}

// -----------------------------------------------------------------------------
// VARIANT 1: Sena SPIDER X Slim Configuration
// -----------------------------------------------------------------------------
module pod_variant_sena() {
    pod_monocoque_base_setup();

    // Upper equipment chamber: Generous space for Sena SPIDER X Slim
    translate([52.0, (POD_OUTER_W - 44.0)/2.0, POD_WALL + 2.0]) {
        // Slim EPDM cradle bed
        color([0.18, 0.18, 0.20]) {
            difference() {
                cube([86.0, 44.0, 5.0], center=false);
                translate([2.0, 2.0, 1.5])
                    cube([82.0, 40.0, 4.0], center=false);
            }
        }
        // Sena SPIDER X Slim OEM unit
        translate([3.0, 3.0, 3.0])
            dummy_sena_spider_x_slim(with_quick_clamp = false);
    }
}

// -----------------------------------------------------------------------------
// VARIANT 2: Cardo Packtalk Edge Configuration
// -----------------------------------------------------------------------------
module pod_variant_cardo() {
    pod_monocoque_base_setup();

    // Upper equipment chamber: Cardo OEM Air-Mount Cradle + Packtalk Edge Unit
    translate([50.0, (POD_OUTER_W - 46.0)/2.0, POD_WALL + 1.5]) {
        // OEM Air-Mount Cradle screwed to floor
        dummy_cardo_oem_airmount_cradle();

        // Packtalk Edge Unit clicked into cradle
        translate([0, 0, 3.5])
            dummy_cardo_packtalk_edge(with_actuators = false);

        // 2x M2.5 Stainless fixing screws
        color("silver") {
            translate([15.0, 23.0, 2.0])
                cylinder(r=1.2, h=3.0, center=false, $fn=16);
            translate([62.0, 23.0, 2.0])
                cylinder(r=1.2, h=3.0, center=false, $fn=16);
        }
    }
}

// -----------------------------------------------------------------------------
// VARIANT 3: OMM 2.4 GHz UCS Transceiver Configuration (Full Scale Equipment Bed)
// -----------------------------------------------------------------------------
module pod_variant_omm() {
    pod_monocoque_base_setup();

    // Upper equipment chamber: Form-fitting EPDM Cradle Tray filling the full chamber
    translate([48.0, (POD_OUTER_W - 52.0)/2.0, POD_WALL + 1.0]) {
        // 1. Tailored High-Density EPDM Base Cradle Tray (90 x 52 mm)
        color([0.18, 0.19, 0.22]) {
            difference() {
                cube([90.0, 52.0, 16.0], center=false);
                // Pocket for main OMM Transceiver unit
                translate([4.0, 4.0, 3.0])
                    cube([78.0, 44.0, 14.0], center=false);
            }
        }

        // 2. Main OMM 2.4 GHz UCS Transceiver Unit (Full Scale: 78 x 44 x 14 mm)
        translate([4.0, 4.0, 3.0]) {
            // Rugged Matte Black Enclosure
            color([0.12, 0.13, 0.15])
                cube([78.0, 44.0, 12.0], center=false);

            // Anodized Aluminum Top Faceplate (Gunmetal Gray)
            color([0.35, 0.38, 0.42])
                translate([2.0, 2.0, 12.0])
                    cube([74.0, 40.0, 1.2], center=false);

            // OLED Mini Status Display / LED Activity Bar
            color([0.1, 0.85, 1.0, 0.95])
                translate([8.0, 16.0, 13.0])
                    cube([28.0, 12.0, 0.6], center=false);

            // 5V Bi-Directional RF Power Booster Module (Blue Anodized Aluminum Heatsink)
            translate([42.0, 6.0, 4.0]) {
                color([0.12, 0.38, 0.78])
                    cube([32.0, 24.0, 9.0], center=false);
                // Gold-Plated SMA Coaxial Bulkhead Connector
                color("gold")
                    translate([32.0, 12.0, 4.5])
                        rotate([0, 90, 0])
                            cylinder(r=3.2, h=6.0, center=false, $fn=16);
            }

            // 90° USB-C Ribbon Cable Lead (connecting to PCBA 03 under dry-flap)
            color([0.2, 0.2, 0.25])
                translate([-3.0, 18.0, 2.0])
                    cube([6.0, 10.0, 2.0], center=false);
        }
    }
}

// -----------------------------------------------------------------------------
// VARIANT 4: Hermetische Mini-Dry-Box Configuration
// -----------------------------------------------------------------------------
module pod_variant_drybox() {
    pod_monocoque_base_setup();

    // Upper equipment chamber: Staufach-Einlegeboden for key, papers, and fuses
    translate([48.0, (POD_OUTER_W - 52.0)/2.0, POD_WALL + 1.0]) {
        cartridge_insert_blindkassette(
            insert_l = 92.0,
            insert_w = 52.0,
            plate_th = 2.0,
            wall_h   = 10.0
        );
    }
}

// -----------------------------------------------------------------------------
// Master Quad Gallery Preview
// -----------------------------------------------------------------------------
module pod_inlay_quad_gallery() {
    spacing_y = 90.0;

    // Variant 1: Sena SPIDER X Slim (Y = 0 mm)
    translate([0, 0 * spacing_y, 0])
        pod_variant_sena();

    // Variant 2: Cardo Packtalk Edge (Y = 90 mm)
    translate([0, 1 * spacing_y, 0])
        pod_variant_cardo();

    // Variant 3: OMM 2.4 GHz UCS Transceiver (Y = 180 mm)
    translate([0, 2 * spacing_y, 0])
        pod_variant_omm();

    // Variant 4: Hermetische Mini-Dry-Box (Y = 270 mm)
    translate([0, 3 * spacing_y, 0])
        pod_variant_drybox();
}

// -----------------------------------------------------------------------------
// Render Selection
// -----------------------------------------------------------------------------
variant = "all"; // [all, sena, cardo, omm, drybox]

if (variant == "sena") {
    pod_variant_sena();
} else if (variant == "cardo") {
    pod_variant_cardo();
} else if (variant == "omm") {
    pod_variant_omm();
} else if (variant == "drybox") {
    pod_variant_drybox();
} else {
    pod_inlay_quad_gallery();
}
