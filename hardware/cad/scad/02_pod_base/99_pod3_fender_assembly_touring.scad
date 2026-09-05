// =============================================================================
// OpenMotorBridge - Satellite Pod 3: Touring Bagger Full Fender Assembly (3D Scene)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod3_fender_assembly_touring.scad
// Description: Photorealistic 3D visualization scene of the Touring Stealth
//              Console (Typ D2) installed on a Harley-Davidson Touring rear fender.
//              Features:
//              1. Harley Touring rear fender arch (Deep Gloss Vivid Black).
//              2. 100% NON-INVASIVE MOUNTING: Zero holes drilled in the fender sheet metal!
//                 Rear mounting tongue clamped to OEM Blinkerbrücke studs (5/16"-18 / M8).
//              3. Organic teardrop contours matching classic Road King, Street Glide, Ultra lines.
//              4. Universal Pod 3 Housing nested inside console, pointing rearwards.
//              5. Slide-out Transceiver Cartridge demonstrating tool-free servicing.
//              6. Concealed M8 cable diving behind Blinkerbrücke into fender grommet.
//              7. Bullet turn signal bar (Blinker-Traverse with amber lenses).
//              8. Standard 180x200 mm motorcycle license plate (+30° legal view).
//              9. Decoupled Garmin Varia mmWave radar mounted under license plate.
// =============================================================================

include <../00_common/parameters.scad>;
use <pod3_touring_stealth_console.scad>;
use <pod_base_housing.scad>;
use <../03_pod_cartridges/cartridge_omm_transceiver.scad>;
use <radar_license_plate_bracket.scad>;

FENDER_R_WHEEL = 320.0;
FENDER_WIDTH   = 176.0;
Z_FENDER_TOP   = 5.5;

// Cartridge slide-out offset to demonstrate tool-free serviceability
CARTRIDGE_SLID_OUT = 35.0; // mm

// 1. Harley Rear Fender Arch (High Gloss Vivid Black)
module dummy_touring_fender() {
    color("#090d16", 0.98) // Vivid Black
    difference() {
        translate([0, 0, Z_FENDER_TOP - FENDER_R_WHEEL])
            rotate([90, 0, 0])
                cylinder(r=FENDER_R_WHEEL, h=FENDER_WIDTH, center=true, $fn=128);

        // Tire clearance cut
        translate([0, 0, Z_FENDER_TOP - FENDER_R_WHEEL])
            rotate([90, 0, 0])
                cylinder(r=FENDER_R_WHEEL - 18.0, h=FENDER_WIDTH + 20.0, center=true, $fn=64);

        // Front cut (under seat)
        translate([-FENDER_R_WHEEL - 140.0, -FENDER_WIDTH, Z_FENDER_TOP - FENDER_R_WHEEL - 50.0])
            cube([FENDER_R_WHEEL, 2*FENDER_WIDTH, 2*FENDER_R_WHEEL]);

        // Rear cut (below turn signals)
        translate([170.0, -FENDER_WIDTH, Z_FENDER_TOP - FENDER_R_WHEEL - 50.0])
            cube([FENDER_R_WHEEL, 2*FENDER_WIDTH, 2*FENDER_R_WHEEL]);

        // Lower half cut
        translate([-2*FENDER_R_WHEEL, -FENDER_WIDTH, Z_FENDER_TOP - 2*FENDER_R_WHEEL])
            cube([4*FENDER_R_WHEEL, 2*FENDER_WIDTH, FENDER_R_WHEEL]);
    }
}

// 2. Chrome / Satin Bullet Light Bar
module dummy_bullet_light_bar_touring(w=260.0) {
    color("#475569") { // Satin metallic finish
        translate([115.0, 0, 4.0]) {
            cube([16.0, 85.0, 12.0], center=true);
            translate([0, -w/2.0 + 15.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
            translate([0, w/2.0 - 15.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
        }
    }
    color("#f59e0b", 0.85) { // Amber bullet lenses
        translate([129.0, -w/2.0 + 15.0, 4.0]) sphere(r=12.5, $fn=24);
        translate([129.0, w/2.0 - 15.0, 4.0]) sphere(r=12.5, $fn=24);
    }
}

// 3. License Plate (180 x 200 mm)
module dummy_license_plate_touring(w=180.0, h=200.0) {
    color("#f8fafc")
        translate([126.0, -w/2.0, -h + 4.0])
            cube([1.5, w, h], center=false);
    color("#1d4ed8")
        translate([126.8, -w/2.0, -45.0 + 4.0])
            cube([1.2, 28.0, 45.0], center=false);
}

// 4. Decoupled Garmin Varia Radar
module dummy_garmin_varia_touring() {
    color("#09090b")
        translate([130.0, -20.0, -246.0])
            cube([18.0, 40.0, 72.0], center=false);
    color("#dc2626", 0.95)
        translate([148.5, -12.0, -230.0])
            cube([1.5, 24.0, 40.0], center=false);
}

// 5. Dummy Harley Passenger Seat (Doppelsitzbank)
module dummy_passenger_seat_touring() {
    color("#1e1b18", 0.98) // Black stitched leather
    translate([-260.0, -110.0, 12.0]) {
        hull() {
            cube([120.0, 220.0, 45.0], center=false);
            translate([110.0, 15.0, 0])
                cube([15.0, 190.0, 32.0], center=false);
            translate([122.0, 30.0, 0])
                cube([6.0, 160.0, 20.0], center=false);
        }
    }
}

module touring_fender_assembly() {
    // 1. Rear Fender Arch
    dummy_touring_fender();

    // 2. Dummy Passenger Seat (Front of console hugs its rear curve)
    dummy_passenger_seat_touring();

    // 3. Touring Stealth Console (Matte Charcoal / Gloss Black PA12)
    color("#1e293b", 0.96)
        pod3_touring_stealth_console();

    // 4. Universal Pod 3 Base Housing (Sitting directly in the open dock cradle)
    // M8 neck faces forward (-X towards seat), open cartridge mouth faces rearward (+X)
    translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, 2.5]) {
        color("#475569", 0.95)
            pod_base_housing();

        // 5. Transceiver Cartridge (Slid out rearwards +X to demonstrate tool-free servicing!)
        translate([POD_BULKHEAD_X + CARTRIDGE_SLID_OUT, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
            cartridge_omm_transceiver_assembly(exploded = false);
        }
    }

    // 6. Forward M8 Cable (runs out front of pod at X=-68, dives directly under seat)
    color("#0284c7") {
        translate([-POD_OUTER_L/2.0 - 5.0, 0, 21.5])
            rotate([0, 90, 0])
                cylinder(r=4.0, h=40.0, center=true, $fn=24);
        translate([-POD_OUTER_L/2.0 - 35.0, 0, 12.0])
            cylinder(r=4.0, h=18.0, center=true, $fn=24);
    }

    // 7. Bullet Turn Signal Bar (Blinkerbrücke)
    dummy_bullet_light_bar_touring();

    // 8. License Plate
    dummy_license_plate_touring();

    // 9. Decoupled Radar License Plate Bracket
    color("#09090b")
        translate([120.0, 0, -196.0])
            radar_license_plate_bracket();

    // 10. Decoupled Radar Unit
    dummy_garmin_varia_touring();
}

// Standalone preview (guarded)
if ($preview) {
    touring_fender_assembly();
}
