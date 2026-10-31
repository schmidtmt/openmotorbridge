// =============================================================================
// OpenMotorBridge - Universal Front Node: Monocoque Lower Tub (v10.0 Slot-In)
// =============================================================================
// File: hardware/cad/scad/04_front_node/00_front_node_tub.scad
// Description: HP MJF PA12 waterproof monolithic monocoque lower case tub with
//              4-in-1 universal mounting system, PCBA 05 standoffs, acoustic vent,
//              longitudinal C-profile guide rails, front wedge lock pocket, and
//              rear slide portal. 100% free of vertical clamping screws!
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <parts/000_front_node_base_tub.scad>;
use <parts/001_pcb_standoffs.scad>;
use <parts/002_acoustic_vent.scad>;
use <parts/004_mounting_system.scad>;
use <parts/005_cable_combs.scad>;

module front_node_lower_tub() {
    ch_x_start = FRONT_NODE_WALL + 3.5; // 6.0 mm
    ch_y_start = FRONT_NODE_WALL + 3.5; // 6.0 mm
    rail_bottom_z = FRONT_NODE_RAIL_Z - FRONT_NODE_RAIL_H/2.0; // 15.1 mm

    difference() {
        union() {
            // 1. Monolithic Monocoque Base Tub Body (with C-rails, front wedge pocket & West portal)
            front_node_base_tub();
            
            // 2. Additive 2x M4/M5 Silentblock Flange Mounting Ears (East & West flanks)
            front_node_flange_ears(ear_len = 14.0, ear_w = 14.0, ear_h = 5.0, hole_r = 2.5);

            // 3. Stiffening fillets along bottom interior perimeter
            translate([ch_x_start + 1.0, ch_y_start + 1.0, FRONT_NODE_WALL])
                cube([FRONT_NODE_CHAMBER_L - 2.0, 1.2, 1.5], center=false);
            translate([ch_x_start + 1.0, ch_y_start + FRONT_NODE_CHAMBER_W - 2.2, FRONT_NODE_WALL])
                cube([FRONT_NODE_CHAMBER_L - 2.0, 1.2, 1.5], center=false);
        }
        
        // 4. South Cockpit Cable Gland Cutout (Y = 0 mm, X = 35.5 mm, Z = 9.5 mm)
        // Kept below the C-rail guide roof (z_top = 15.1 mm) to preserve continuous guide rail!
        south_round_cable_gland_cutout(
            x_center = 35.5,
            z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 3.5,
            bore_r   = 4.5,
            collar_r = 6.0,
            z_top    = rail_bottom_z
        );
            
        // 5. North Vehicle Cable Gland Cutout (Y = 68.0 mm, X = 35.5 mm, Z = 9.5 mm)
        north_round_cable_gland_cutout(
            x_center = 35.5,
            z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 3.5,
            bore_r   = 4.5,
            collar_r = 6.0,
            z_top    = rail_bottom_z
        );
            
        // 6. USB-C Service Port Opening (East wall, X = 98 mm, Y = 24.1 mm)
        front_node_usbc_service_cutout();
            
        // 7. Acoustic Vent Port Cutout for Knowles MEMS (floor, aligned with MK1)
        translate([ch_x_start, ch_y_start, 0])
            front_node_acoustic_vent_cutout(floor_thickness = FRONT_NODE_WALL);
            
        // 8. AMPS 4-Hole Mounting Pattern Cutouts (floor underside)
        front_node_amps_cutouts(h_depth = 5.0);
        
        // 9. Crossed Zip-Tie & Hose Clamp Tunnels (floor underside)
        front_node_ziptie_tunnels(slot_w = 5.5, slot_depth = 1.4);
        
        // 10. 3M Dual-Lock Landing Pad Recess (floor underside)
        front_node_dual_lock_recess(pad_l = 50.0, pad_w = 28.0, pad_depth = 0.6);
    }
    
    // 11. Additive: 4x Internal M2.5 PCB Standoffs (rising from floor at H1-H4 pitch 75.0 x 43.0 mm)
    translate([ch_x_start, ch_y_start, FRONT_NODE_WALL]) {
        front_node_pcb_standoffs(h = FRONT_NODE_STANDOFF_H);
    }
}

// Standalone compilation
front_node_lower_tub();
