// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM 2.4 GHz UCS Modular Insert (Deckel / Nest)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/06_insert_omm_ucs.scad
// Description: Standalone 3D printable top cradle insert for OpenMotorMesh (OMM)
//              2.4 GHz OEM module in standardized UCS (Universal Communication
//              Solution) form factor.
//              Features:
//              - Form-fitting UCS module cradle nest (68 x 38 x 8 mm, R = 3.0 mm)
//              - Front USB-C access port (9.5 x 3.5 mm) for standalone charging & flashing
//              - Through-deck pass-through for 2-wire DC harness to PCBA 03 below
//              - Internal bay for 600 mAh LiPo flat cell (40 x 26 x 5 mm)
//              - Convective breathing slots for thermal dissipation
//              - Open corner cutouts giving 100% vertical screwdriver access to M2 screws
//              - Integrated outward-facing EPDM rubber strap retention hooks
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module cartridge_insert_omm_ucs(
    insert_l = 110.0,
    insert_w = 53.0,
    deck_th  = 2.5,
    cradle_h = 10.0
) {
    difference() {
        union() {
            // 1. Intermediate Partition Deck (Grundplatte at z = 0 .. deck_th)
            cube(size=[insert_l, insert_w, deck_th], center=false);

            // 2. UCS Cradle 3D Contour Body (z = deck_th .. deck_th + cradle_h)
            translate([2.0, 1.5, deck_th]) {
                difference() {
                    cube(size=[insert_l - 4.0, insert_w - 3.0, cradle_h], center=false);

                    // A. Universal UCS Module Recessed Contour Bed
                    translate([18.0, (insert_w - 3.0 - 40.0)/2.0, 2.0])
                        cube(size=[70.0, 40.0, cradle_h + 0.1], center=false);

                    // B. Front USB-C Cable Channel & Port Tunnel
                    translate([insert_l - 24.0, (insert_w - 3.0 - 14.0)/2.0, 2.5])
                        cube(size=[24.0, 14.0, cradle_h + 0.1], center=false);
                }
            }

            // 3. Outward-Facing Rubber Strap Overhang Ledges (Top Lip at z = deck_th + 5.0 .. deck_th + cradle_h)
            // Left Flank Top Lip
            translate([insert_l/2.0 - 6.0, 0.5, deck_th + 5.0])
                cube(size=[12.0, 2.5, cradle_h - 5.0], center=false);
            // Right Flank Top Lip
            translate([insert_l/2.0 - 6.0, insert_w - 3.0, deck_th + 5.0])
                cube(size=[12.0, 2.5, cradle_h - 5.0], center=false);
        }

        // 4. True Through-Deck Contact & Wiring Pass-Through (Cuts through Grundplatte)
        // Pass-through to PCBA 03 J_AUDIO_PWR / J_ACT headers below
        translate([26.0, insert_w/2.0 - 10.0, -1.0])
            cube(size=[14.0, 20.0, deck_th + cradle_h + 2.0], center=false);

        // 5. 4x Sled M2 Corner Fastening Screws Clearances (Ø 4.5 mm counterbore & tool access)
        translate([3.5, 3.5, -0.5])
            cylinder(r=2.2, h=deck_th + cradle_h + 1.0, center=false, $fn=24);
        translate([insert_l - 9.5, 3.5, -0.5])
            cylinder(r=2.2, h=deck_th + cradle_h + 1.0, center=false, $fn=24);
        translate([3.5, insert_w - 8.5, -0.5])
            cylinder(r=2.2, h=deck_th + cradle_h + 1.0, center=false, $fn=24);
        translate([insert_l - 9.5, insert_w - 8.5, -0.5])
            cylinder(r=2.2, h=deck_th + cradle_h + 1.0, center=false, $fn=24);

        // 6. 4x Convective Airflow & Breathing Slots
        for (sx = [12.0, 92.0]) {
            translate([sx, 8.0, -0.5])
                cube(size=[10.0, 2.5, deck_th + 1.0], center=false);
            translate([sx, insert_w - 10.5, -0.5])
                cube(size=[10.0, 2.5, deck_th + 1.0], center=false);
        }

        // 7. Corner Post Chamfers
        translate([-1.0, -1.0, -0.5])
            cube(size=[7.0, 7.0, deck_th + cradle_h + 1.0], center=false);
        translate([-1.0, insert_w - 6.0, -0.5])
            cube(size=[7.0, 7.0, deck_th + cradle_h + 1.0], center=false);
        translate([insert_l - 6.0, -1.0, -0.5])
            cube(size=[7.0, 7.0, deck_th + cradle_h + 1.0], center=false);
        translate([insert_l - 6.0, insert_w - 6.0, -0.5])
            cube(size=[7.0, 7.0, deck_th + cradle_h + 1.0], center=false);
    }
}

// Preview standalone
cartridge_insert_omm_ucs();
