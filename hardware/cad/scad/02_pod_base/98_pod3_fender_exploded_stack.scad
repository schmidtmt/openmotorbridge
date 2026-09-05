// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Fender Mounting Exploded Stack View (3D Scene)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/98_pod3_fender_exploded_stack.scad
// Description: Educational exploded vertical stack view demonstrating the exact
//              layer-by-layer installation of Pod 3 on a Harley Touring rear fender:
//              Layer 1: Harley Steel Fender Arch (R=320mm wheel / R=140mm crown)
//              Layer 2: 1.5 mm EPDM Rubber Damping & Paint Protection Pad
//              Layer 3: Curved Saddle Cradle Foot with rear OEM Blinkerbrücke tongue
//              Layer 4: Universal Pod 3 Base Housing (Typ B, 100% unified, 135x70x38mm)
//              Layer 5: Transceiver Cartridge (PCBA 04: GNSS / LoRa / ESP-NOW)
//              Layer 6: ST Aero-Winglet Cowl (KotB swept wings & radome crest)
//              Layer 7: Hidden M8 Cable diving behind Blinker Bar into fender
//              Layer 8: License plate and decoupled Garmin Varia radar below.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/006_fender_curved_saddle.scad>;
use <pod3_st_aero_winglet_nacelle.scad>;
use <radar_license_plate_bracket.scad>;
use <pod_base_housing.scad>;
use <../03_pod_cartridges/cartridge_omm_transceiver.scad>;

FENDER_R_WHEEL = 320.0;
FENDER_WIDTH   = 176.0;
Z_FENDER_TOP   = 5.5;

// Vertical explosion spacing
Z_FENDER    = 0.0;
Z_BRIDGE    = 35.0;
Z_HOUSING   = 85.0;
Z_CARTRIDGE = 135.0;

module dummy_tail_and_radar() {
    // Blinkerbrücke
    color("#09090b") {
        translate([115.0, 0, 4.0]) {
            cube([16.0, 85.0, 12.0], center=true);
            translate([0, -60.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
            translate([0, 60.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
        }
    }
    color("#ef4444", 0.90) {
        translate([129.0, -60.0, 4.0]) sphere(r=12.5, $fn=24);
        translate([129.0, 60.0, 4.0]) sphere(r=12.5, $fn=24);
    }
    // License plate
    color("#f8fafc")
        translate([126.0, -90.0, -196.0])
            cube([1.5, 180.0, 200.0], center=false);
    color("#1d4ed8")
        translate([126.8, -90.0, -41.0])
            cube([1.2, 28.0, 45.0], center=false);
    // Decoupled radar
    color("#09090b") {
        translate([120.0, 0, -196.0])
            radar_license_plate_bracket();
        translate([130.0, -20.0, -246.0])
            cube([18.0, 40.0, 72.0], center=false);
    }
    color("#dc2626", 0.95)
        translate([148.5, -12.0, -230.0])
            cube([1.5, 24.0, 40.0], center=false);
}

module pod3_fender_exploded_stack() {
    // Layer 1: Harley Steel Fender Arch
    dummy_fender();

    // Layer 2: ST Aero-Winglet Performance Bridge (bolting to side fender struts)
    translate([0, 0, Z_BRIDGE])
        color("#0f172a", 0.96)
            pod3_st_aero_winglet_nacelle();

    // Layer 3: Universal Pod 3 Base Housing (open-top fit into dock)
    translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, Z_HOUSING])
        color("#475569", 0.95)
            pod_base_housing();

    // Layer 4: Transceiver Cartridge (PCBA 04: GNSS / LoRa / ESP-NOW)
    translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, Z_CARTRIDGE])
        translate([POD_BULKHEAD_X + 25.0, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL])
            cartridge_omm_transceiver_assembly(exploded = false);

    // Layer 5: Rear Tail, Light Bar, License Plate & Decoupled Radar
    dummy_tail_and_radar();
}

// Standalone preview (guarded)
if ($preview) {
    pod3_fender_exploded_stack();
}
