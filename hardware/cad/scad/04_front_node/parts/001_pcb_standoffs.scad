// =============================================================================
// OpenMotorBridge - Front Node PCB Standoffs
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/001_pcb_standoffs.scad
// Description: 4x M2.5 cylindrical screw boss standoffs matching KiCad H1-H4.
// =============================================================================

include <../../00_common/parameters.scad>;

// Relative offset of PCB inside internal chamber (2mm border clearance)
PCB_OFFSET_X = (FRONT_NODE_CHAMBER_L - FRONT_NODE_PCB_L) / 2.0; // 2.0 mm
PCB_OFFSET_Y = (FRONT_NODE_CHAMBER_W - FRONT_NODE_PCB_W) / 2.0; // 2.0 mm

// Standoff coordinates relative to inner chamber origin (0,0)
FRONT_NODE_STANDOFF_COORDS = [
    [PCB_OFFSET_X + 3.5,  PCB_OFFSET_Y + 3.5],  // H1 (bottom-left / SW)
    [PCB_OFFSET_X + 64.5, PCB_OFFSET_Y + 3.5],  // H2 (bottom-right / SE)
    [PCB_OFFSET_X + 3.5,  PCB_OFFSET_Y + 40.5], // H3 (top-left / NW)
    [PCB_OFFSET_X + 64.5, PCB_OFFSET_Y + 40.5]  // H4 (top-right / NE)
];

module front_node_pcb_standoffs(h = FRONT_NODE_STANDOFF_H) {
    for (pos = FRONT_NODE_STANDOFF_COORDS) {
        translate([pos[0], pos[1], 0]) {
            difference() {
                cylinder(r=FRONT_NODE_STANDOFF_R, h=h, center=false);
                translate([0, 0, -0.1])
                    cylinder(r=FRONT_NODE_INSERT_R, h=h + 0.2, center=false);
            }
        }
    }
}

// Standalone render / STL export
front_node_pcb_standoffs();
