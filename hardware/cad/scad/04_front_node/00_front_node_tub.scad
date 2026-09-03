// =============================================================================
// OpenMotorBridge - Universal Front Node: Lower Enclosure Tub (Unterteil)
// =============================================================================
// File: hardware/cad/scad/04_front_node/00_front_node_tub.scad
// Description: HP MJF PA12 waterproof lower case tub with 4-in-1 universal
//              mounting system, PCB standoffs, acoustic vent, and cable comb slots.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <parts/001_pcb_standoffs.scad>;
include <parts/002_acoustic_vent.scad>;
include <parts/003_sealing_system.scad>;
include <parts/004_mounting_system.scad>;
include <parts/005_cable_combs.scad>;

module front_node_lower_tub() {
    difference() {
        union() {
            // 1. Solid outer tub body with rounded corners
            linear_extrude(height = FRONT_NODE_TUB_H) {
                offset(r = FRONT_NODE_CORNER_R) {
                    offset(delta = -FRONT_NODE_CORNER_R) {
                        square([FRONT_NODE_OUTER_L, FRONT_NODE_OUTER_W], center=false);
                    }
                }
            }
            
            // 2. Additive 2x M4/M5 Silentblock Flange Mounting Ears (East & West)
            front_node_flange_ears(ear_len = 14.0, ear_w = 14.0, ear_h = 5.0, hole_r = 2.5);
        }
        
        // 3. Hollow internal chamber (leaves 2.5 mm wall and 2.5 mm floor)
        translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL]) {
            cube(size=[FRONT_NODE_CHAMBER_L, FRONT_NODE_CHAMBER_W, FRONT_NODE_TUB_H + 1.0], center=false);
        }
        
        // 4. Perimeter Sealing Groove (Nut for Ø 1.5 mm O-ring cord)
        front_node_sealing_groove_tool(
            length = FRONT_NODE_OUTER_L,
            width  = FRONT_NODE_OUTER_W,
            z_top  = FRONT_NODE_TUB_H,
            groove_w = 2.0,
            groove_depth = 1.6
        );
        
        // 5. 4x M3 Corner Clamping Screw Holes (core holes for M3 threaded inserts)
        corner_offsets = [
            [FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
            [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
            [FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R],
            [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R]
        ];
        for (co = corner_offsets) {
            translate([co[0], co[1], FRONT_NODE_TUB_H - 12.0])
                cylinder(r=M3_SCREW_HOLE_R, h=12.2, center=false);
        }
        
        // 6. South USB Cable Comb Cutout Pocket
        translate([FRONT_NODE_WALL + 3.5, 0, 0])
            south_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 8.0, h = 8.1);
            
        // 7. West Signal/Power Cable Comb Cutout Pocket
        translate([0, FRONT_NODE_WALL + 3.5, 0])
            west_cable_comb_cutout(z_start = FRONT_NODE_TUB_H - 7.5, h = 7.6);
            
        // 8. USB-C Service Port Opening
        translate([FRONT_NODE_WALL + 3.5, 0, 0])
            front_node_usbc_service_cutout();
            
        // 9. Acoustic Vent Port Cutout for Knowles MEMS (floor)
        translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, 0])
            front_node_acoustic_vent_cutout(floor_thickness = FRONT_NODE_WALL);
            
        // 10. AMPS 4-Hole Mounting Pattern Cutouts (floor underside)
        front_node_amps_cutouts(h_depth = 5.0);
        
        // 11. Crossed Zip-Tie & Hose Clamp Tunnels (floor underside)
        front_node_ziptie_tunnels(slot_w = 5.5, slot_depth = 2.2);
        
        // 12. 3M Dual-Lock Landing Pad Recess (floor underside)
        front_node_dual_lock_recess(pad_l = 50.0, pad_w = 28.0, pad_depth = 0.6);
    }
    
    // 13. Additive: 4x Internal M2.5 PCB Standoffs (rising from floor)
    translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL]) {
        front_node_pcb_standoffs(h = FRONT_NODE_STANDOFF_H);
    }
}

// Standalone compilation
front_node_lower_tub();
