// =============================================================================
// OpenMotorBridge - Satellite Pod: Base Assembly & Fitting Inspection
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod_base_assembly.scad
// Description: Full 3D assembly of the universal pod base with connected M8
//              cable connector, bulkhead partition, and inserted cartridge preview.
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_m8_connector.scad>;
use <pod_base_housing.scad>;

// View Mode: Set to true for slide-out exploded cartridge view
CARTRIDGE_PULLED_OUT = true;
SLIDE_OFFSET         = CARTRIDGE_PULLED_OUT ? 45.0 : 0.0;

module pod_base_full_assembly() {
    // 1. Pod Base Housing (Translucent Slate Grey for inner inspection)
    color("slategray", 0.75)
        pod_base_housing();

    // 2. M8 6-Pin IP67 Metal Connector (connected at rear)
    translate([0, POD_OUTER_W/2.0, POD_OUTER_H/2.0])
        rotate([0, 180, 0])
            dummy_m8_connector();

    // 3. 2x V4A Auto-Eject Coil Springs
    color("gold") {
        translate([POD_BULKHEAD_X + 2.0, 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.8, h=8.0, $fn=16);
        translate([POD_BULKHEAD_X + 2.0, 44.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.8, h=8.0, $fn=16);
    }
}

// Render complete assembly preview
pod_base_full_assembly();
