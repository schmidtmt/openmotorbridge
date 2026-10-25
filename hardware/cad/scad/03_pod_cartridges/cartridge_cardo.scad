// =============================================================================
// OpenMotorBridge - Satellite Pod: Cardo Packtalk Edge Serial Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_cardo.scad
// Description: True serial ("hintereinander") cartridge architecture:
//              - Front Section: PCBA 03 Smart Cartridge Controller (MCU, Power, Actuators)
//              - Rear Section: Original Cardo OEM Air-Mount Cradle + Packtalk Edge Unit
//              - Mechatronics: 2 solenoids with angled rectangular feet for Power On/Off
//              - Zero Custom Pogo-Pins: Uses 100% genuine Cardo factory harness to PCBA 03
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <../00_common/dummies/dummy_intercom_units.scad>;

module cartridge_cardo_assembly(exploded = false) {
    z_pcb    = exploded ? 20.0 : 5.0;
    z_cradle = exploded ? 15.0 : 2.5;
    z_device = exploded ? 32.0 : 4.5;

    // 1. Universal Base Sled (Anthracite PA12) with magnetic anti-theft latch
    color("darkslategray", 0.92)
        cartridge_base_sled(
            sled_l     = CARTRIDGE_BASE_L,
            sled_w     = CARTRIDGE_BASE_W,
            sled_h     = CARTRIDGE_BASE_H,
            wall       = 2.5,
            show_latch = true
        );

    // 2. PCBA 03 Satellite Pod Interface Controller (Front Section: X = 1.5 .. 43.5 mm)
    translate([1.5, (CARTRIDGE_BASE_W - 48.0)/2.0, z_pcb])
        dummy_adapter_pcb();

    // 3. Original OEM Cardo Air-Mount Cradle (Rear Section: X = 40.0 .. 124.0 mm)
    // Sits directly on sled floor (Z = 2.5 mm) - NO sandwich intermediate deck!
    translate([40.0, (CARTRIDGE_BASE_W - 46.0)/2.0, z_cradle])
        dummy_cardo_oem_airmount_cradle();

    // 4. Genuine Cardo Packtalk Edge OEM Unit clicked onto the OEM Air-Mount Cradle
    // Features 2 mechatronic solenoids with angled rectangular feet for Power On/Off
    translate([40.0, (CARTRIDGE_BASE_W - 46.0)/2.0, z_device])
        dummy_cardo_packtalk_edge(with_actuators = true);

    // 5. 2x M2.5 Stainless Steel Screws securing OEM Cradle to Sled Floor
    color("silver") {
        translate([55.0, CARTRIDGE_BASE_W/2.0, z_cradle + 1.5])
            cylinder(r=1.3, h=4.0, center=false, $fn=16);
        translate([102.0, CARTRIDGE_BASE_W/2.0, z_cradle + 1.5])
            cylinder(r=1.3, h=4.0, center=false, $fn=16);
    }
}

// Standalone assembly render
cartridge_cardo_assembly(exploded = false);
