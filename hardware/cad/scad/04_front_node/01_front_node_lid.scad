// =============================================================================
// OpenMotorBridge - Universal Front Node: Upper Enclosure Lid (Gehäusedeckel)
// =============================================================================
// File: hardware/cad/scad/04_front_node/01_front_node_lid.scad
// Description: HP MJF PA12 waterproof top lid with perimeter compression tongue,
//              M3 corner clamping holes, LED light-pipe tunnel, and internal
//              adhesive FPC antenna pocket with coaxial cable routing clips.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/003_sealing_system.scad>;

module front_node_upper_lid() {
    pcb_origin_x = FRONT_NODE_WALL + 3.5 + (FRONT_NODE_CHAMBER_L - FRONT_NODE_PCB_L) / 2.0; // 8.0 mm
    pcb_origin_y = FRONT_NODE_WALL + 3.5 + (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W) / 2.0; // 8.0 mm

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
            // South compression bar (over 53.0 mm 4-Port USB comb, X in [17.0, 70.0])
            translate([17.0, 0, -1.5])
                cube(size=[53.0, FRONT_NODE_WALL + 3.2, 1.5], center=false);
                
            // West compression bar (over 30.0 mm Signal/Power comb)
            translate([0, FRONT_NODE_WALL + 3.5 + 11.0, -1.5])
                cube(size=[FRONT_NODE_WALL + 3.2, 30.0, 1.5], center=false);
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
        
        // 6. Status LED Light-Pipe Tunnel (Ø 2.0 mm through-hole directly over D1)
        // D1 is at PCB rel [64.75, 22.25] -> Tub [72.75, 30.25]
        led_x = pcb_origin_x + 64.75;
        led_y = pcb_origin_y + 22.25;
        translate([led_x, led_y, -0.1])
            cylinder(r=1.0, h=FRONT_NODE_LID_H + 0.2, center=false);
            
        // 7. Internal FPC Antenna Pocket & Coaxial Cable Retention System
        // A. Recess pocket for adhesive 2.4 GHz FPC dipole (e.g. Molex 146153, 48 x 12 mm)
        translate([FRONT_NODE_WALL + 10.0, FRONT_NODE_OUTER_W / 2.0 - 6.0, FRONT_NODE_LID_H - FRONT_NODE_WALL - 0.6])
            cube(size=[48.0, 12.0, 0.7], center=false);
            
        // B. Recessed cable guide canal (Ø 1.5 mm) for U.FL coax lead to ESP32-C3
        translate([FRONT_NODE_WALL + 54.0, FRONT_NODE_OUTER_W / 2.0 - 2.5, FRONT_NODE_LID_H - FRONT_NODE_WALL - 1.0])
            cube(size=[10.0, 2.0, 1.1], center=false);
    }
}

// Standalone compilation
front_node_upper_lid();

