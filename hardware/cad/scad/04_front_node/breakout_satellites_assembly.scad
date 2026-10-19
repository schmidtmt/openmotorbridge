// =============================================================================
// OpenMotorBridge - Breakout Satellites 3D Assembly & Interlock View
// =============================================================================
// File: hardware/cad/scad/04_front_node/breakout_satellites_assembly.scad
// Description: Multi-mode 3D assembly model for documentation rendering:
//              - "cockpit": Standalone Cockpit Breakout with 5x USB-C & clamp
//              - "vehicle": Standalone Vehicle Breakout with COTS latch sockets
//              - "combo": Both satellites slide-interlocked via lateral Dovetail joint
//              - "exploded": Exploded presentation for manuals and installation guides
// =============================================================================

include <../00_common/parameters.scad>;
use <cockpit_breakout_block.scad>;
use <vehicle_breakout_block.scad>;

mode = "combo"; // [cockpit, vehicle, combo, exploded]

module breakout_satellites_assembly() {
    if (mode == "cockpit") {
        cockpit_breakout_body();
        translate([0, 0, 18.0 + 3.0])
            cockpit_breakout_clamp();
    } else if (mode == "vehicle") {
        vehicle_breakout_body();
        vehicle_breakout_lid();
    } else if (mode == "exploded") {
        // Cockpit unit
        translate([0, -20.0, 0]) {
            cockpit_breakout_body();
            translate([0, 0, 18.0 + 12.0])
                cockpit_breakout_clamp();
        }
        // Vehicle unit
        translate([0, 30.0, 0]) {
            vehicle_breakout_body();
            translate([0, 0, 18.0 + 8.0])
                vehicle_breakout_lid();
        }
    } else {
        // "combo" - Interlocked via lateral Dovetail joint
        // Cockpit Satellite (Front / South)
        cockpit_breakout_body();
        translate([0, 0, 18.0 + 1.5])
            cockpit_breakout_clamp();
            
        // Vehicle Satellite (Rear / North, slid onto Dovetail rail at Y = 28.0 mm)
        translate([0, 28.0, 0]) {
            vehicle_breakout_body();
            vehicle_breakout_lid();
        }
    }
}

breakout_satellites_assembly();
