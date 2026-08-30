// =============================================================================
// OpenMotorBridge - Satellite Pod: Translucent 3D X-Ray Inspection Scene
// =============================================================================
// File: hardware/cad/scad/02_pod_base/97_pod_xray_assembly.scad
// Description: Translucent Ghosted X-Ray inspection assembly of the closed Pod
//              with inserted cartridge. Highlights internal guide rails, 6-pin
//              piston mating inside the shroud, bulkhead, and copper studs.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/dummies/dummy_m8_connector.scad>;
include <pod_base_housing.scad>;
include <parts/004_pod_copper_studs.scad>;
include <../03_pod_cartridges/00_base_sled.scad>;
include <../03_pod_cartridges/cartridge_sena.scad>;

module pod_xray_inspection_assembly() {
    // 1. Pod Base Outer Housing (Translucent Blue-Gray Glass / Ghosted Shell)
    color([0.2, 0.35, 0.55, 0.32])
        pod_base_housing();

    // 2. 2x Copper Thermal Studs (Floor)
    color("darkgoldenrod", 1.0)
        pod_copper_studs(h=3.5);

    // 3. M8 6-Pin IP67 Metal Connector (Rear)
    translate([0, POD_OUTER_W/2.0, POD_OUTER_H/2.0])
        rotate([0, 180, 0])
            dummy_m8_connector();

    // 4. 2x V4A Auto-Eject Coil Springs
    color("gold", 1.0) {
        translate([POD_BULKHEAD_X + 2.0, 16.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.5, h=10.0);
        translate([POD_BULKHEAD_X + 2.0, 44.0, POD_OUTER_H/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.5, h=10.0);
    }

    // 5. Fully Inserted Cartridge Sled (Opaque Royal Blue / Gold)
    translate([24.0, 3.0, 2.5]) {
        color("dodgerblue", 0.95)
            cartridge_sena_sled();
    }
}

// Render complete X-Ray inspection
pod_xray_inspection_assembly();
