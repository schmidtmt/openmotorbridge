// =============================================================================
// OpenMotorBridge - Satellite Pod: Sena SPIDER X Slim Serial Cartridge Assembly
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/cartridge_sena.scad
// Description: True serial ("hintereinander") cartridge architecture:
//              - Front Section: PCBA 03 Smart Cartridge Controller (MCU, Power, Audio)
//              - Rear Section: Original Sena OEM Quick-Snap Cradle + SPIDER X Slim
//              - Direct OEM Cable Peitsche: 3-wire harness (power, mic, speaker)
//                plugs directly into J_AUDIO_PWR on PCBA 03 (zero custom pogo-pins)
//              - Ultra-compact: 22.0 mm total height (massive vertical margin)
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <00_base_sled.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <../00_common/dummies/dummy_intercom_units.scad>;

module cartridge_sena_assembly(exploded = false) {
    z_pcb    = exploded ? 18.0 : 5.0;
    z_cradle = exploded ? 18.0 : 2.5;
    z_device = exploded ? 36.0 : 4.5;

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

    // 3. Original OEM Sena Quick-Snap Cradle (Rear Section: X = 44.0 .. 120.0 mm)
    // Sits directly on sled floor (Z = 2.5 mm) - NO sandwich intermediate deck!
    translate([44.0, (CARTRIDGE_BASE_W - 33.0)/2.0, z_cradle])
        dummy_sena_oem_cradle();

    // 4. Genuine Sena SPIDER X Slim OEM Unit clicked into original OEM cradle
    translate([45.0, (CARTRIDGE_BASE_W - 31.0)/2.0, z_device])
        dummy_sena_spider_x_slim();

    // 5. 2x M2 Stainless Steel Screws securing OEM Cradle to Sled Floor
    color("silver") {
        translate([56.0, CARTRIDGE_BASE_W/2.0, z_cradle + 1.2])
            cylinder(r=1.1, h=3.0, center=false, $fn=16);
        translate([108.0, CARTRIDGE_BASE_W/2.0, z_cradle + 1.2])
            cylinder(r=1.1, h=3.0, center=false, $fn=16);
    }
}

// Standalone assembly render
cartridge_sena_assembly(exploded = false);
