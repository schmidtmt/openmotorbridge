// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Rear Transceiver & GoPro Mount Assembly
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod3_rear_assembly.scad
// Description: Full 3D assembly inspection of Pod 3 (Heckbürzel / Gepäckträger)
//              demonstrating that NO intermediary adapter PCB is needed: The
//              openmotorbridge_rear_transceiver PCB with GPS patch antenna and LoRa
//              sits directly inside the cartridge sled and plugs into the pod bulkhead.
// =============================================================================

include <../00_common/parameters.scad>;
include <pod_base_housing.scad>;
include <pod_mount_gopro_rack.scad>;
include <../03_pod_cartridges/cartridge_omm_transceiver.scad>;
include <../00_common/dummies/dummy_omm_transceiver_pcb.scad>;
include <../00_common/dummies/dummy_m8_connector.scad>;

// View Mode: Set to true for slide-out exploded view
EXPLODED_VIEW = true;
SLIDE_X      = EXPLODED_VIEW ? 45.0 : 24.0;
MOUNT_Z      = EXPLODED_VIEW ? -15.0 : 0.0;

module pod3_rear_assembly() {
    // 1. Pod Base Housing (Translucent Slate Grey)
    color("darkslategray", 0.75)
        pod_base_housing();

    // 2. GoPro / Luggage Rack Mount Adapter Plate (Underneath)
    color("dimgray", 0.9)
        translate([10.0, (POD_OUTER_W - 50.0)/2.0, MOUNT_Z])
            pod_mount_gopro_rack(plate_l=80.0, plate_w=50.0, plate_t=4.0);

    // 3. M8 6-Pin IP67 Metal Connector (Connected at rear)
    translate([0, POD_OUTER_W/2.0, POD_OUTER_H/2.0])
        rotate([0, 180, 0])
            dummy_m8_connector();

    // 4. OMM Transceiver Cartridge Sled (Direct 1-Tier Sled, no adapter board!)
    translate([SLIDE_X, 3.0, 2.5]) {
        color("slategray", 0.85)
            cartridge_omm_transceiver_sled();

        // 5. OMM Transceiver PCB with GNSS Patch Antenna & LoRa Shield (Sits directly in sled)
        translate([2.5, 3.0, 3.0])
            dummy_omm_transceiver_pcb();
    }
}

// Render complete assembly
pod3_rear_assembly();
