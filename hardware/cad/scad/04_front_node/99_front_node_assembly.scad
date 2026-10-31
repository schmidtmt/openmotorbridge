// =============================================================================
// OpenMotorBridge - Universal Front Node: Exploded 3D Assembly View (v10.0)
// =============================================================================
// File: hardware/cad/scad/04_front_node/99_front_node_assembly.scad
// Description: Multi-tier exploded view demonstrating the v10.0 Monocoque Slide-In
//              architecture, PCBA 05 v10 integration, dual Wi-Fi 6E antennas
//              (flex and internal stub support), L-Slide Lid, and snap-on Sensor Puck.
// =============================================================================

include <../00_common/parameters.scad>;
use <00_front_node_tub.scad>;
use <01_front_node_lid.scad>;
use <parts/005_cable_combs.scad>;
use <parts/006_dummy_front_node_pcb.scad>;
use <parts/sensor_puck_environmental.scad>;
use <03_front_node_usbc_plug.scad>;

// Exploded offsets along Z
EXPLODE_PCB_Z      = 12.0;
EXPLODE_ANTENNA_Z  = 28.0;
EXPLODE_LID_Z      = 44.0;
EXPLODE_PUCK_Z     = 66.0;

// Dummy Taoglas FXP73 / Molex Wi-Fi 6E Flex Antenna (46 x 9 x 0.5 mm)
module dummy_wifi_flex_antenna() {
    color([0.15, 0.35, 0.20]) // Dark green flex substrate
        cube([46.0, 9.0, 0.5], center=false);
    color("gold") // Exposed radiating dipole trace
        translate([2.0, 1.0, 0.5])
            cube([42.0, 7.0, 0.05], center=false);
    color("black") // U.FL miniature coax lead
        translate([4.0, 4.5, 0.5])
            cylinder(r=0.6, h=18.0, $fn=16);
}

// Dummy Internal Omnidirectional Stub Antenna (Ø 6.5 mm x 32 mm)
module dummy_wifi_stub_antenna() {
    color("black") {
        rotate([0, 90, 0])
            cylinder(r=3.25, h=32.0, center=false, $fn=24);
        // Coaxial lead
        translate([0, 0, 0])
            cylinder(r=0.6, h=16.0, center=false, $fn=16);
    }
}

module front_node_exploded_assembly() {
    ch_x_start = FRONT_NODE_WALL + 3.5; // 6.0 mm
    ch_y_start = FRONT_NODE_WALL + 3.5; // 6.0 mm
    pcb_x = ch_x_start + (FRONT_NODE_CHAMBER_L - FRONT_NODE_PCB_L)/2.0; // 8.0 mm
    pcb_y = ch_y_start + (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W)/2.0; // 9.0 mm

    // 1. Lower Monocoque Tub (Base level)
    color([0.16, 0.18, 0.20])
        front_node_lower_tub();
        
    // 2. Gore ePTFE Acoustic Vent Membrane (under the tub floor, aligned with MK1 at 11.20, 46.30)
    color("white")
        translate([pcb_x + 11.20, pcb_y + 46.30, -1.0])
            cylinder(r=FRONT_NODE_MIC_MEMB_R, h=0.2, center=false);
            
    // 3. Universal Front Node PCB Assembly (centered on standoffs)
    translate([pcb_x, pcb_y, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + EXPLODE_PCB_Z])
        dummy_front_node_pcb();
        
    // 4. Dual Wi-Fi 6E Antennas for ESP32-E22 (2x2 MIMO 5/6 GHz)
    // Antenna 1: North longitudinal flex antenna (Bay 1)
    translate([ch_x_start + 15.0, ch_y_start + FRONT_NODE_CHAMBER_W - 11.5, EXPLODE_ANTENNA_Z])
        dummy_wifi_flex_antenna();

    // Antenna 2: South longitudinal flex antenna (Bay 2)
    translate([ch_x_start + 15.0, ch_y_start + 2.5, EXPLODE_ANTENNA_Z])
        dummy_wifi_flex_antenna();

    // 5. South Cockpit TPU Cable Boot (floating forwards along Y)
    translate([0, -18.0, 0])
        front_node_south_cable_boot_installed();
        
    // 6. North Vehicle TPU Cable Boot (floating rearwards along Y)
    translate([0, 18.0, 0])
        front_node_north_cable_boot_installed();
        
    // 7. USB-C Protective Plug (floating East, right flank)
    translate([FRONT_NODE_OUTER_L + 18.0, 24.1, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8])
        rotate([0, 90, 90])
            front_node_usbc_plug();
            
    // 8. Monocoque L-Slide Lid (v10 with guide tongues & Heckwand)
    color([0.22, 0.24, 0.26])
        translate([0, 0, EXPLODE_LID_Z])
            front_node_upper_lid();

    // 9. Modular Snap-On Environmental Sensor Puck (u-blox SAM-M10Q, TMP117, OPT3001)
    translate([ch_x_start + 55.0 - 22.0, ch_y_start + 28.0 - 22.0, EXPLODE_PUCK_Z])
        sensor_puck_environmental_assembly();
}

front_node_exploded_assembly();
