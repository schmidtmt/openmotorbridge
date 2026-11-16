// =============================================================================
// OpenMotorBridge - Central Main Box: Slide-In Zwischenboden / Intermediate Tray (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/010_slide_tray.scad
// Description: Einschiebbarer Zwischenboden for the Central Box (Gehäuse Typ A)
//              utilizing the v10 Dual-Rail Monocoque Slide-In Principle:
//
// 1. Dual-Rail Track 1 Kinematics (Z = 18.0 mm):
//    - Lateral guide tongues sliding smoothly into the Rail 1 grooves of the tub.
//    - Chamfered front lead-in nose for effortless, self-aligning insertion.
//    - Separates the lower PCBA 01 compartment (Z = 0..17 mm) from the upper
//      battery & antenna chamber (Z = 18..38 mm) without requiring any screws!
//
// 2. Battery Accommodation:
//    - Dedicated cradle for 1S LiPo backup battery (2200 mAh flat cell: 67 x 38 x 5 mm).
//    - Lateral containment boundary ribs (h = 4.5 mm) preventing X/Y shifting.
//    - Underside damping recess for 1.0 mm vibration-absorbing EPDM foam.
//
// 3. Integrated RF Antenna Nests:
//    - Recessed adhesive nest for Taoglas FXP895 (LoRa 868 MHz flex PCB: 85 x 18 x 0.8 mm).
//    - Recessed adhesive nest for Taoglas FXP73 (2.4 GHz Wi-Fi/BLE: 47 x 7 x 0.5 mm).
//    - 100% metal-free, RF-transparent PA12 platform with maximum isolation.
//
// 4. Cable Management & Convective Airflow:
//    - J7 LiPo harness passthrough slot with C-clip strain relief.
//    - Dual U.FL coaxial cable drop channels to PCBA 01 RF ports (ANT1 & ANT2/3).
//    - Convective cooling breathing slots outside the battery footprint for PCBA 01
//      thermal dissipation towards the top lid Gore breather vent.
//
// 5. Ergonomic Rear Service Handle:
//    - Rear vertical pull/push ridge with tactile ribs for tool-free insertion & removal.
//    - Bottom registration detent locking against the tub lower rear sill.
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_slide_tray(
    tray_l   = 104.4, // Width along X inside tub chamber (mm)
    tray_w   = 68.0,  // Depth along Y from front wall to rear sill (mm)
    tray_t   = 2.0,   // Base floor thickness (mm)
    rail_z   = MAIN_BOX_RAIL1_Z // Nominal Rail 1 centerline height (18.0 mm)
) {
    tongue_prot = 1.3; // Lateral guide tongue protrusion into side groove (mm)
    tongue_h    = 2.0; // Guide tongue thickness in Z (mm)
    
    // Base coordinate origin:
    // Placed in assembly coordinates: X = 2.8, Y = 3.2, Z = rail_z - tray_t/2.0
    translate([2.8, 3.2, rail_z - tray_t/2.0]) {
        difference() {
            union() {
                // 1. Main Tray Structural Floor Plate
                cube([tray_l, tray_w, tray_t], center=false);

                // 2. Left Lateral Guide Tongue (slides into Left Rail 1 Groove)
                translate([-tongue_prot, 4.0, (tray_t - tongue_h)/2.0]) {
                    // Main tongue strip
                    cube([tongue_prot + 0.1, tray_w - 4.0, tongue_h], center=false);
                    // 45° Lead-in chamfer at front end
                    translate([0, -2.5, 0])
                        linear_extrude(height=tongue_h)
                            polygon(points=[[0, 0], [tongue_prot + 0.1, 2.5], [0, 2.5]]);
                }

                // 3. Right Lateral Guide Tongue (slides into Right Rail 1 Groove)
                translate([tray_l - 0.1, 4.0, (tray_t - tongue_h)/2.0]) {
                    // Main tongue strip
                    cube([tongue_prot + 0.1, tray_w - 4.0, tongue_h], center=false);
                    // 45° Lead-in chamfer at front end
                    translate([0, -2.5, 0])
                        linear_extrude(height=tongue_h)
                            polygon(points=[[tongue_prot + 0.1, 0], [0, 2.5], [tongue_prot + 0.1, 2.5]]);
                }

                // 4. Battery Containment Perimeter Ribs (for 67 x 38 x 5 mm LiPo in Front/Center + PCM)
                // Battery placement: X = 20.1..87.1 mm (dx = 67 mm), Y = 2.4..44.4 mm (dy = 42.0 mm clear)
                // Accommodates 38.0 mm cell body + 3.0 mm PCM strip + 1.0 mm margin
                // Rib height = 4.5 mm (Z = tray_t .. tray_t + 4.5)
                translate([18.0, 0.8, tray_t]) {
                    // Front containment rib
                    cube([71.6, 1.6, 4.5], center=false);
                    // Rear containment rib (separating battery from North antenna zone)
                    translate([0, 43.6, 0])
                        cube([71.6, 1.6, 4.5], center=false);
                    // Left containment rib
                    cube([1.6, 45.2, 4.5], center=false);
                    // Right containment rib
                    translate([70.0, 0, 0])
                        cube([1.6, 45.2, 4.5], center=false);
                    // 2x Elastic retention catch nubs
                    translate([1.6, 16.0, 3.8])
                        cube([0.8, 10.0, 0.8], center=false);
                    translate([69.2, 16.0, 3.8])
                        cube([0.8, 10.0, 0.8], center=false);
                }

                // 5. North Antenna Bed: Dual Antennas both at North (LoRa unten, 2.4 GHz darüber)
                // A. Taoglas FXP895 LoRa 868 MHz (85 x 18 mm at Y = 46.0..64.0 mm: UNTEN)
                translate([9.5, 45.5, tray_t]) {
                    cube([86.0, 1.4, 1.5], center=false);
                    translate([0, 18.6, 0])
                        cube([86.0, 1.4, 1.5], center=false);
                    cube([1.4, 20.0, 1.5], center=false);
                    translate([84.6, 0, 0])
                        cube([1.4, 20.0, 1.5], center=false);
                }

                // B. Taoglas FXP73 2.4 GHz Wi-Fi/BLE (47 x 7 mm at Y = 60.5..67.5 mm: ETWAS DARÜBER)
                // Elevated 1.2 mm rear ledge (separates FXP73 from 0.8 mm FXP895 with 0.4 mm PA12 floor)
                translate([27.5, 60.5, tray_t]) {
                    cube([48.0, 7.0, 1.2], center=false);
                    translate([0, 6.8, 0])
                        cube([48.0, 1.2, 2.2], center=false);
                }

                // 6. Rear Service Handle Flange (at Y = tray_w - 2.5 mm, Z = tray_t .. tray_t + 5.5 mm)
                translate([tray_l/2.0 - 20.0, tray_w - 2.2, tray_t]) {
                    cube([40.0, 2.2, 5.5], center=false);
                    // Tactile grip ribs
                    for (gx = [6.0, 14.0, 22.0, 30.0]) {
                        translate([gx, 1.8, 1.0])
                            cube([1.8, 0.8, 4.0], center=false);
                    }
                }

                // 7. Underside Registration Detent (engages front of tub rear sill)
                translate([tray_l/2.0 - 15.0, tray_w - 4.0, -1.2]) {
                    cube([30.0, 3.0, 1.2], center=false);
                }
            }

            // --- SUBTRACTIONS ---

            // 8. Taoglas FXP895 Shallow Adhesive Nest (85.2 x 18.2 x 0.6 mm for LoRa 868 MHz at North: UNTEN)
            // Located at Y = 46.0..64.0 mm, X = 10.0..95.2 mm
            translate([10.0, 46.0, tray_t - 0.4])
                cube([85.2, 18.0, 1.0], center=false);

            // 9. Taoglas FXP73 Shallow Adhesive Nest (47.5 x 7.2 x 0.5 mm for 2.4 GHz at North: ETWAS DARÜBER)
            // Located at Y = 60.5..67.5 mm, X = 28.0..75.5 mm (on elevated ledge)
            translate([28.0, 60.5, tray_t + 1.2 - 0.4])
                cube([47.5, 7.0, 1.0], center=false);

            // 10. Cable Passthrough Openings
            // A. Battery J5 open lateral U-notch (allows tool-free tray sliding with pre-crimped Molex 4P plug)
            // Positioned directly over PCBA 01 J5 (X = 90.0 mm to right edge, Y = 28.0..42.0 mm)
            translate([90.0, 28.0, -0.5])
                cube([tray_l - 90.0 + 2.0, 14.0, tray_t + 2.0], center=false);

            // B. Shared Dual U.FL RF Coaxial Drop Slot (routes both LoRa & 2.4 GHz cables down to PCBA 01 ANT1 & U2)
            // Positioned between the two antennas directly over ANT1 and U2 ports (X = 52.0..74.0 mm, Y = 56.0..62.0 mm)
            translate([52.0, 56.0, -0.5])
                cube([22.0, 6.0, tray_t + 2.0], center=false);

            // 11. Convective Thermal Breathing Louvers
            // Left flank breathing slots (X = 5.0..14.0 mm)
            for (sy = [10.0:7.0:38.0]) {
                translate([6.0, sy, -0.5])
                    cube([8.0, 2.4, tray_t + 2.0], center=false);
            }

            // Right flank breathing slots (X = 91.0..99.0 mm, directly over PCBA 01 L1 inductor & buck converter)
            for (sy = [12.0:7.0:26.0]) {
                translate([91.0, sy, -0.5])
                    cube([8.0, 2.4, tray_t + 2.0], center=false);
            }

            // 12. LiPo Underside Cushioning Foam Recess (65.0 x 40.0 x 0.8 mm)
            translate([20.0, 2.5, -0.1])
                cube([65.0, 40.0, 0.8], center=false);
        }
    }
}

// Standalone preview
main_box_slide_tray();
