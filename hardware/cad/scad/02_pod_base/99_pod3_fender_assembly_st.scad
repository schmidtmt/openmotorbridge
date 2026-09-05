// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST Performance Bagger Fender Assembly (3D Scene)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod3_fender_assembly_st.scad
// Description: Photorealistic 3D visualization scene of the ST Performance
//              Aero-Winglet Nacelle (Typ D3) installed on a Road Glide ST.
//              Features:
//              1. Harley Touring rear fender arch (Deep Gloss Vivid Black).
//              2. Carbon-fiber solo seat cowl (front) & Piggyback suspension reservoirs.
//              3. 100% NON-INVASIVE MOUNTING: Zero holes drilled in the fender sheet metal!
//                 Rear mounting tongue clamped to OEM Blinkerbrücke studs (5/16"-18 / M8).
//              4. 100% MATHEMATICALLY SYMMETRICAL KotB swept winglets with vertical endplates.
//              5. Universal Pod 3 Housing nested inside console, pointing rearwards.
//              6. Slide-out Transceiver Cartridge demonstrating tool-free servicing.
//              7. Concealed M8 cable diving behind Blinkerbrücke into fender grommet.
//              8. License plate (180x200 mm) with zero upward occlusion (+30° legal).
//              9. Decoupled Garmin Varia radar mounted symmetrically below plate.
// =============================================================================

include <../00_common/parameters.scad>;
use <pod3_st_aero_winglet_nacelle.scad>;
use <pod_base_housing.scad>;
use <../03_pod_cartridges/cartridge_omm_transceiver.scad>;
use <radar_license_plate_bracket.scad>;

FENDER_R_WHEEL = 320.0;
FENDER_WIDTH   = 176.0;
Z_FENDER_TOP   = 5.5;

// Cartridge slide-out offset to demonstrate tool-free serviceability
CARTRIDGE_SLID_OUT = 35.0; // mm

// 1. Harley Rear Fender Arch (High Gloss Vivid Black)
module dummy_st_fender() {
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

// 2. Carbon-Fiber Solo Seat Cowl (Front of Pod 3)
module dummy_carbon_solo_cowl() {
    color("#1e293b", 0.95) // Carbon twill anthracite
        difference() {
            translate([-135.0, 0, 16.0])
                hull() {
                    rotate([0, 90, 0]) cylinder(r=55.0, h=70.0, center=true, $fn=32);
                    translate([40.0, 0, -10.0]) rotate([0, 90, 0]) cylinder(r=46.0, h=25.0, center=true, $fn=32);
                }
            translate([0, 0, Z_FENDER_TOP - FENDER_R_WHEEL])
                rotate([90, 0, 0]) cylinder(r=FENDER_R_WHEEL + 1.0, h=300.0, center=true, $fn=64);
        }
}

// 3. Performance Piggyback Shocks
module dummy_suspension_reservoirs() {
    color("#d97706") { // Anodized gold / bronze cylinder bodies
        translate([-10.0, -112.0, 22.0]) rotate([22, 0, 0]) cylinder(r=14.0, h=60.0, center=true, $fn=32);
        translate([-10.0, 112.0, 22.0]) rotate([-22, 0, 0]) cylinder(r=14.0, h=60.0, center=true, $fn=32);
    }
    color("#0f172a") { // Black billet compression clicker dials
        translate([-10.0, -112.0, 55.0]) cylinder(r=10.0, h=7.0, center=true, $fn=24);
        translate([-10.0, 112.0, 55.0]) cylinder(r=10.0, h=7.0, center=true, $fn=24);
    }
}

// 4. Blacked-Out Bullet Light Bar (Blinkerbrücke)
module dummy_bullet_light_bar_st(w=250.0) {
    color("#09090b") { // Blacked-out ST light bar
        translate([115.0, 0, 4.0]) {
            cube([16.0, 85.0, 12.0], center=true);
            translate([0, -w/2.0 + 15.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
            translate([0, w/2.0 - 15.0, 0]) rotate([0, 90, 0]) cylinder(r=13.0, h=26.0, center=true, $fn=32);
        }
    }
    color("#ef4444", 0.90) { // Smoked red ST turn signal / brake lenses
        translate([129.0, -w/2.0 + 15.0, 4.0]) sphere(r=12.5, $fn=24);
        translate([129.0, w/2.0 - 15.0, 4.0]) sphere(r=12.5, $fn=24);
    }
}

// 5. License Plate (180 x 200 mm)
module dummy_license_plate_st(w=180.0, h=200.0) {
    color("#f8fafc")
        translate([126.0, -w/2.0, -h + 4.0])
            cube([1.5, w, h], center=false);
    color("#1d4ed8")
        translate([126.8, -w/2.0, -45.0 + 4.0])
            cube([1.2, 28.0, 45.0], center=false);
}

// 6. Decoupled Garmin Varia Radar
module dummy_garmin_varia_st() {
    color("#09090b")
        translate([130.0, -20.0, -246.0])
            cube([18.0, 40.0, 72.0], center=false);
    color("#dc2626", 0.95)
        translate([148.5, -12.0, -230.0])
            cube([1.5, 24.0, 40.0], center=false);
}

// 7. Dummy Saddlebags (Koffer) & Fender Struts
module dummy_saddlebags_and_struts() {
    // Fender Strut Chrome/Black Rails (along Y = +/- 126 mm)
    color("#334155") {
        translate([-60.0, 126.0, -22.0]) cube([120.0, 6.0, 14.0], center=true);
        translate([-60.0, -126.0, -22.0]) cube([120.0, 6.0, 14.0], center=true);
    }
    // Hard Saddlebags (Koffer)
    color("#090d16", 0.94) { // Vivid Black Hard Bags
        translate([-80.0, 134.0, -140.0]) cube([260.0, 75.0, 140.0], center=false);
        translate([-80.0, -209.0, -140.0]) cube([260.0, 75.0, 140.0], center=false);
    }
}

module st_fender_assembly() {
    // 1. Rear Fender Arch
    dummy_st_fender();

    // 2. Carbon-Fiber Solo Seat Cowl
    dummy_carbon_solo_cowl();

    // 3. Performance Suspension Reservoirs
    dummy_suspension_reservoirs();

    // 4. Dummy Saddlebags & Fender Struts
    dummy_saddlebags_and_struts();

    // 5. ST Aero-Winglet Performance Bridge (Satin Black / Forged Carbon PA12)
    color("#0f172a", 0.96)
        pod3_st_aero_winglet_nacelle();

    // 6. Universal Pod 3 Base Housing (Sitting directly in the open dock cradle)
    // M8 neck faces forward (-X towards seat), open cartridge mouth faces rearward (+X)
    translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, 2.5]) {
        color("#475569", 0.95)
            pod_base_housing();

        // 7. Transceiver Cartridge (Slid out rearwards +X to demonstrate tool-free servicing!)
        translate([POD_BULKHEAD_X + CARTRIDGE_SLID_OUT, (POD_OUTER_W - CARTRIDGE_BASE_W)/2.0, POD_WALL]) {
            cartridge_omm_transceiver_assembly(exploded = false);
        }
    }

    // 8. Concealed M8 Cable (runs under left wing, drops down inside of left wingtip)
    color("#0284c7") {
        hull() {
            translate([-POD_OUTER_L/2.0 - 2.0, 0, 16.0]) sphere(r=2.5, $fn=16);
            translate([-82.0, 20.0, 15.0]) sphere(r=2.5, $fn=16);
        }
        hull() {
            translate([-82.0, 20.0, 15.0]) sphere(r=2.5, $fn=16);
            translate([-34.0, 64.0, 10.0]) sphere(r=2.5, $fn=16);
        }
        hull() {
            translate([-34.0, 64.0, 10.0]) sphere(r=2.5, $fn=16);
            translate([-14.0, 98.0, -4.0]) sphere(r=2.5, $fn=16);
        }
        hull() {
            translate([-14.0, 98.0, -4.0]) sphere(r=2.5, $fn=16);
            translate([-8.0, 122.0, -16.0]) sphere(r=2.5, $fn=16);
        }
        translate([-8.0, 122.0, -24.0])
            cylinder(r=2.5, h=22.0, center=true, $fn=24);
    }

    // 9. Blacked-Out Bullet Light Bar (Blinkerbrücke)
    dummy_bullet_light_bar_st();

    // 10. License Plate
    dummy_license_plate_st();

    // 11. Decoupled Radar License Plate Bracket
    color("#09090b")
        translate([120.0, 0, -196.0])
            radar_license_plate_bracket();

    // 12. Decoupled Radar Unit
    dummy_garmin_varia_st();
}

// Standalone preview (guarded)
if ($preview) {
    st_fender_assembly();
}
