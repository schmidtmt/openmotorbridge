// =============================================================================
// OpenMotorBridge - Universal Front Node: Upper Enclosure Lid (Gehäusedeckel)
// =============================================================================
// File: hardware/cad/scad/04_front_node/01_front_node_lid.scad
// Description: HP MJF PA12 waterproof top lid with perimeter compression tongue,
//              M3 corner clamping holes, LED light-pipe tunnel, and internal
//              adhesive FPC antenna pocket.
// =============================================================================

include <../00_common/parameters.scad>;
include <parts/003_sealing_system.scad>;

module front_node_upper_lid() {
    difference() {
        union() {
            // 1. Solid lid body with rounded corners
            linear_extrude(height = FRONT_NODE_LID_H) {
                offset(r = FRONT_NODE_CORNER_R) {
                    offset(delta = -FRONT_NODE_CORNER_R) {
                        square([FRONT_NODE_OUTER_L, FRONT_NODE_OUTER_W], center=false);
                    }
                }
            }
            
            // 2. Perimeter Sealing Tongue / Lip (protrudes downwards into tub groove)
            front_node_sealing_tongue_lip(
                length = FRONT_NODE_OUTER_L,
                width  = FRONT_NODE_OUTER_W,
                lip_w  = 1.5,
                lip_h  = 1.4
            );
            
            // 3. Clamping Pressure Ribs over South & West Cable Combs
            // South compression bar (over 38 mm USB comb)
            translate([FRONT_NODE_WALL + 3.5 + 12.0, 0, -1.5])
                cube(size=[38.0, FRONT_NODE_WALL, 1.5], center=false);
                
            // West compression bar (over 30 mm Signal/Power comb)
            translate([0, FRONT_NODE_WALL + 3.5 + 11.0, -1.5])
                cube(size=[FRONT_NODE_WALL, 30.0, 1.5], center=false);
        }
        
        // 4. Internal cavity recess (reduces weight & creates headroom over tall parts)
        translate([FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5, -0.1]) {
            cube(size=[FRONT_NODE_CHAMBER_L, FRONT_NODE_CHAMBER_W, FRONT_NODE_LID_H - FRONT_NODE_WALL + 0.1], center=false);
        }
        
        // 5. 4x M3 Corner Clamping Screw Holes (Through-hole with counterbore for DIN 912)
        corner_offsets = [
            [FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
            [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_CORNER_R],
            [FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R],
            [FRONT_NODE_OUTER_L - FRONT_NODE_CORNER_R, FRONT_NODE_OUTER_W - FRONT_NODE_CORNER_R]
        ];
        for (co = corner_offsets) {
            // M3 screw through-hole Ø 3.4 mm
            translate([co[0], co[1], -2.0])
                cylinder(r=1.7, h=FRONT_NODE_LID_H + 4.0, center=false);
                
            // DIN 912 M3 cap head counterbore Ø 6.2 mm, depth 3.5 mm
            translate([co[0], co[1], FRONT_NODE_LID_H - 3.2])
                cylinder(r=3.1, h=3.5, center=false);
        }
        
        // 6. Status LED Light-Pipe Tunnel (Ø 2.0 mm through-hole over D1)
        // PCB origin is [FRONT_NODE_WALL + 3.5, FRONT_NODE_WALL + 3.5]
        // D1 is at [PCB_X + 66.25, PCB_Y + 30.19]
        led_x = FRONT_NODE_WALL + 3.5 + 66.25;
        led_y = FRONT_NODE_WALL + 3.5 + 30.19;
        translate([led_x, led_y, -0.1])
            cylinder(r=1.0, h=FRONT_NODE_LID_H + 0.2, center=false);
            
        // 7. Internal FPC Antenna Pocket (recess in ceiling for adhesive 2.4 GHz dipole)
        translate([FRONT_NODE_WALL + 10.0, FRONT_NODE_OUTER_W / 2.0 - 6.0, FRONT_NODE_LID_H - FRONT_NODE_WALL - 0.5])
            cube(size=[48.0, 12.0, 0.6], center=false);
    }
}

// Standalone compilation
front_node_upper_lid();
