// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM Rear Transceiver Cartridge (Pod 3 Heck)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: Ready-to-print single-tier cartridge sled for Pod 3.
//              Houses the OMM Rear Transceiver PCB (ESP32-S3, SX1262 LoRa,
//              GNSS Engine & Ceramic Patch Antenna) with 4x M2.5 standoffs.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <00_base_sled.scad>;

module cartridge_omm_transceiver_sled() {
    union() {
        // 1. Universal Base Sled (with full 20.5 mm walls & guide ribs)
        cartridge_base_sled(
            sled_l = CARTRIDGE_BASE_L,
            sled_w = CARTRIDGE_BASE_W,
            sled_h = 20.5,
            wall   = 2.5
        );

        // 2. 4x M2.5 Mounting Screw Standoffs for OMM Transceiver PCB (70 x 48 mm)
        translate([2.5 + 4.0, 3.0 + 4.0, 2.5])
            screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=3.0);

        translate([2.5 + 66.0, 3.0 + 4.0, 2.5])
            screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=3.0);

        translate([2.5 + 4.0, 3.0 + 44.0, 2.5])
            screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=3.0);

        translate([2.5 + 66.0, 3.0 + 44.0, 2.5])
            screw_boss(outer_r=2.5, inner_r=M2_5_SCREW_HOLE_R, h=3.0);
    }
}

// Render complete OMM Transceiver Cartridge
cartridge_omm_transceiver_sled();
