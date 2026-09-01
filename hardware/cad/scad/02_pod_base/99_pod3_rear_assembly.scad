// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Rear Transceiver Assembly
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod3_rear_assembly.scad
// Description: Full 3D assembly inspection of Pod 3 (Heckbürzel / Gepäckträger)
//              demonstrating that NO intermediary adapter PCB is needed: The
//              openmotorbridge_rear_transceiver PCB with GPS patch antenna and LoRa
//              sits directly inside the cartridge sled and plugs into the pod bulkhead.
// =============================================================================

include <../00_common/parameters.scad>;
include <pod_base_housing.scad>;
include <../03_pod_cartridges/cartridge_omm_transceiver.scad>;
include <../00_common/dummies/dummy_m8_connector.scad>;

// View Mode: Set to true for slide-out exploded view
EXPLODED_VIEW = true;
SLIDE_X      = EXPLODED_VIEW ? 45.0 : 24.0;

module pod3_rear_assembly() {
    // 1. Pod Base Housing (Translucent Slate Grey)
    color("darkslategray", 0.75)
        pod_base_housing();

    // 2. M8 6-Pin IP67 Metal Connector (Connected at rear)
    translate([0, POD_OUTER_W/2.0, POD_OUTER_H/2.0])
        rotate([0, 180, 0])
            dummy_m8_connector();

    // 3. OMM Transceiver Cartridge Assembly (Slides into the Pod Base Tunnel)
    translate([SLIDE_X, 3.0, 2.5])
        cartridge_omm_transceiver_assembly(exploded = EXPLODED_VIEW);
}

// Render complete assembly
pod3_rear_assembly();
