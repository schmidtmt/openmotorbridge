// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM 2.4 GHz UCS Serial Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_omm_transceiver.scad
// Description: True serial ("hintereinander") cartridge architecture:
//              - Front Section: PCBA 03 Smart Cartridge Controller (MCU, Power, Audio Codec)
//              - Middle Section: OMM 2.4 GHz UCS Transceiver Module (Autonomous Mesh)
//              - Rear Section: Dedicated 5V COTS Bi-Directional RF Booster Heatsink
//              - 100% Digital USB Audio & Telemetry: USB-C interconnect ribbon to PCBA 03
//              - Direct RF Coaxial Route: Booster SMA output to Front Faceplate Bulkhead
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <parts/omm_ucs_module.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <../00_common/dummies/dummy_intercom_units.scad>;

module cartridge_omm_transceiver_assembly(exploded = false) {
    z_pcb     = exploded ? 18.0 : 5.0;
    z_module  = exploded ? 36.0 : 3.5;
    z_booster = exploded ? 36.0 : 3.5;

    // 1. Universal Base Sled (Anthracite PA12 with Front SMA Bulkhead for Bike Antenna)
    color("darkslategray", 0.92)
        cartridge_base_sled(show_latch = true, has_sma_port = true);

    // 2. PCBA 03 Satellite Pod Interface Controller (Front Section: X = 1.5 .. 43.5 mm)
    translate([1.5, (CARTRIDGE_BASE_W - 48.0)/2.0, z_pcb])
        dummy_adapter_pcb();

    // 3. OMM 2.4 GHz UCS Autonomous Transceiver Module (Middle Section: X = 40.0 .. 94.0 mm)
    // Sits directly on floor ribs (Z = 3.5 mm) - NO sandwich intermediate deck!
    translate([40.0, (CARTRIDGE_BASE_W - 36.0)/2.0, z_module])
        omm_ucs_module_assembly(exploded = false);

    // 4. Dedicated 5V COTS Bi-Directional RF Booster in Rear Bay (X = 99.0 .. 124.0 mm)
    translate([99.0, (CARTRIDGE_BASE_W - 15.0)/2.0, z_booster])
        dummy_rf_booster_5v();

    // 5. Digital USB Audio Interconnect Ribbon (PCBA 03 J_AUDIO_PWR -> UCS Module USB-C)
    color([0.18, 0.18, 0.20]) {
        translate([32.0, CARTRIDGE_BASE_W/2.0 - 5.0, z_pcb + 1.2])
            cube([10.0, 10.0, 1.6]);
    }

    // 6. Low-Loss RG-178 RF Coaxial Interconnects
    // A. Interconnect Coax (UCS Output -> RF Booster Input)
    color("black") {
        translate([93.5, CARTRIDGE_BASE_W/2.0, z_booster + 3.0])
            rotate([0, 90, 0])
                cylinder(r=1.0, h=6.5, $fn=12);
    }
    // B. Main RF Coax (Booster Output -> Front Faceplate SMA Bulkhead)
    color("black") {
        translate([8.0, CARTRIDGE_BASE_W - 4.5, z_booster + 1.5])
            cube([92.0, 1.8, 1.8]);
    }
}

// Module alias for sled
module cartridge_omm_transceiver_sled() {
    cartridge_base_sled(has_sma_port = true);
}

// Standalone assembly render
cartridge_omm_transceiver_assembly(exploded = false);
