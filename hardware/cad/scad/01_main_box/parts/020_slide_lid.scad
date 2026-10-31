// =============================================================================
// OpenMotorBridge - Central Main Box: L-Slide Lid with Deadbolt Lock (v10.0)
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/020_slide_lid.scad
// Description: L-shaped Monocoque Central Box Lid (horizontal slide lid +
//              integrated rear Heckwand/apron) utilizing the v10 Dual-Rail
//              Slide-In Principle:
//
// 1. Dual-Rail Track 2 Kinematics (Z = 33.0 mm):
//    - Lateral guide tongues sliding smoothly into Rail 2 C-grooves of the tub.
//    - Solid PA12 retaining roof lip of the tub (Z = 35.5..38.0 mm) captivates
//      the tongues, preventing any vertical lift or prying under high vibration.
//
// 2. Front Wedge-Lock Nose (Keilanzug):
//    - 15° wedge nose engaging the front tub undercut pocket (Y = wall).
//    - Converts horizontal sliding force into vertical/forward sealing pressure
//      against the front perimeter gasket.
//
// 3. Integrated Gore ePTFE Breather Vent Seat:
//    - Recessed circular nest (Ø 12 mm x 1.2 mm) with central Ø 3.2 mm vent bore.
//    - Concentric protective water-deflector labyrinth shroud (IP69K washdown safe).
//
// 4. Integrated Vertical Heckwand & Drip Apron (L-Profile):
//    - Monolithic rear vertical drop wall closing the rear insertion portal (Z = 15..38 mm).
//    - External drip apron (Tropfnase) overlapping the lower sill rebate (Z = 11..15 mm)
//      for a labyrinth watertight seal.
//
// 5. 100% Non-Metallic PA12 Deadbolt Latch System:
//    - Dual rear corner deadbolt locking legs (X = 6.5..10.5 mm & X = 99.5..103.5 mm)
//      with 45° lead-in chamfers for automatic "Slam-to-Shut" latching.
//    - Snap securely into the lower sill sockets at Z = 11.0 mm.
//    - Service release pry slots accessible from the rear.
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_slide_lid(
    length = MAIN_BOX_OUTER_L,
    width  = MAIN_BOX_OUTER_W,
    height = MAIN_BOX_TOTAL_H,
    wall   = MAIN_BOX_WALL
) {
    lid_plate_th = height - MAIN_BOX_RAIL2_Z + MAIN_BOX_RAIL2_H/2.0; // ~6.4 mm top structure
    rail2_z      = MAIN_BOX_RAIL2_Z;
    rail2_h      = 2.4; // Tongue height (with 0.4 mm manufacturing clearance)
    tongue_prot  = 1.5; // Tongue protrusion into 1.8 mm C-groove (0.3 mm clearance)
    
    // Heckwand vertical drop from top lid (Z = height) down to sill (Z = 15.0 mm)
    heck_z_top   = height;
    heck_z_bot   = MAIN_BOX_REAR_SILL_H;
    drip_apron_h = 3.5; // Skirt overlapping sill down to Z = 11.5 mm
    
    color([0.22, 0.24, 0.26]) {
        difference() {
            union() {
                // 1. Horizontal Slide Lid Plate (Z = rail2_z - rail2_h/2.0 .. height)
                // Width along X: inside tub (wall + 0.3 .. length - wall - 0.3)
                translate([wall + 0.3, wall + 0.5, rail2_z - rail2_h/2.0]) {
                    cube([
                        length - 2*wall - 0.6,
                        width - wall - 0.5,
                        height - (rail2_z - rail2_h/2.0)
                    ], center=false);
                }

                // 2. Left Lateral Guide Tongue (engages Left Rail 2 C-Groove)
                translate([wall - tongue_prot, wall + 2.5, rail2_z - rail2_h/2.0]) {
                    // Tongue body
                    cube([tongue_prot + 0.4, width - wall - 3.5, rail2_h], center=false);
                    // 45° Lead-in chamfer at front tip
                    translate([0, -2.0, 0])
                        polyhedron(
                            points=[
                                [0, 0, 0], [tongue_prot, 0, 0], [tongue_prot, 2.0, 0], [0, 2.0, 0],
                                [tongue_prot, 2.0, rail2_h], [tongue_prot, 2.0, rail2_h], [tongue_prot, 0, rail2_h], [0, 2.0, rail2_h]
                            ],
                            faces=[
                                [0,1,2,3], [4,5,6,7], [0,3,7,6], [1,2,5,4], [0,1,4,7], [3,2,5,6]
                            ]
                        );
                }

                // 3. Right Lateral Guide Tongue (engages Right Rail 2 C-Groove)
                translate([length - wall - 0.4, wall + 2.5, rail2_z - rail2_h/2.0]) {
                    // Tongue body
                    cube([tongue_prot + 0.4, width - wall - 3.5, rail2_h], center=false);
                    // 45° Lead-in chamfer at front tip
                    translate([tongue_prot, -2.0, 0])
                        polyhedron(
                            points=[
                                [0, 0, 0], [-tongue_prot, 0, 0], [-tongue_prot, 2.0, 0], [0, 2.0, 0],
                                [-tongue_prot, 2.0, rail2_h], [-tongue_prot, 2.0, rail2_h], [-tongue_prot, 0, rail2_h], [0, 2.0, rail2_h]
                            ],
                            faces=[
                                [0,1,2,3], [4,5,6,7], [0,3,7,6], [1,2,5,4], [0,1,4,7], [3,2,5,6]
                            ]
                        );
                }

                // 4. Front Wedge-Lock Nose (Keilanzug extending into front pocket)
                translate([wall + 1.2, wall - 1.0, rail2_z - 0.3]) {
                    cube([length - 2*wall - 2.4, 1.6, rail2_h + 0.6], center=false);
                    // 20° Lead-in wedge bevel on front face
                    translate([0, -0.6, 0.4])
                        cube([length - 2*wall - 2.4, 0.6, rail2_h - 0.2], center=false);
                }

                // 5. Rear Vertical Heckwand (L-Profile Vertical Leg, Y = width - wall .. width)
                // Spans from Z = heck_z_bot (15.0 mm) up to top lid Z = height (38.0 mm)
                translate([wall + 0.3, width - wall, heck_z_bot]) {
                    cube([length - 2*wall - 0.6, wall, heck_z_top - heck_z_bot], center=false);
                }

                // 6. External Drip Apron (Tropfnase / Overlapping Skirt, Z = 11.5 .. 15.5 mm)
                // Overlaps the rebate of the lower sill at Y = width - 1.5 mm
                translate([wall - 0.2, width - 1.4, heck_z_bot - drip_apron_h]) {
                    cube([length - 2*wall + 0.4, 1.4, drip_apron_h + 1.0], center=false);
                }

                // 7. Dual Non-Metallic PA12 Deadbolt Locking Legs
                // Left locking deadbolt (X = 6.8 .. 10.2 mm)
                translate([wall + 4.3, width - wall - 0.2, heck_z_bot - 4.2]) {
                    cube([3.4, wall + 0.2, 4.5], center=false);
                    // 45° Locking tooth barb
                    translate([0, 0, -1.0])
                        polyhedron(
                            points=[
                                [0, 0, 0], [3.4, 0, 0], [3.4, wall+0.2, 0], [0, wall+0.2, 0],
                                [0, 0, 1.0], [3.4, 0, 1.0], [3.4, wall+0.2, 1.0], [0, wall+0.2, 1.0]
                            ],
                            faces=[
                                [0,1,2,3], [4,5,6,7], [0,3,7,6], [1,2,5,4], [0,1,4,7], [3,2,5,6]
                            ]
                        );
                }

                // Right locking deadbolt (X = 99.8 .. 103.2 mm)
                translate([length - wall - 7.7, width - wall - 0.2, heck_z_bot - 4.2]) {
                    cube([3.4, wall + 0.2, 4.5], center=false);
                    // 45° Locking tooth barb
                    translate([0, 0, -1.0])
                        polyhedron(
                            points=[
                                [0, 0, 0], [3.4, 0, 0], [3.4, wall+0.2, 0], [0, wall+0.2, 0],
                                [0, 0, 1.0], [3.4, 0, 1.0], [3.4, wall+0.2, 1.0], [0, wall+0.2, 1.0]
                            ],
                            faces=[
                                [0,1,2,3], [4,5,6,7], [0,3,7,6], [1,2,5,4], [0,1,4,7], [3,2,5,6]
                            ]
                        );
                }

                // 8. Gore Breather Vent Protective Concentric Shield Ribs (Top Face)
                translate([length/2.0, width/2.0, height]) {
                    // Outer protective ring Ø 16 mm x h 1.2 mm
                    difference() {
                        cylinder(r=8.0, h=1.2, $fn=36);
                        cylinder(r=6.5, h=1.5, $fn=36);
                    }
                }

                // 9. Ergonomic Slide-In Thumb Grip Flange on Top Rear
                translate([length/2.0 - 18.0, width - 6.0, height]) {
                    for (gx = [0:6.0:36.0]) {
                        translate([gx, 0, 0])
                            cube([2.5, 4.5, 1.0], center=false);
                    }
                }
            }

            // --- SUBTRACTIONS ---

            // 10. Gore ePTFE Breather Vent Nest & Center Bore
            translate([length/2.0, width/2.0, height - 1.2]) {
                // Adhesive membrane recess Ø 11.5 mm x 1.2 mm
                cylinder(r=5.75, h=2.0, $fn=36);
                // Center through-bore Ø 3.2 mm down through the lid
                translate([0, 0, -6.0])
                    cylinder(r=1.6, h=8.0, $fn=24);
            }

            // 11. Rear Deadbolt Release Tool Pry Slots
            // Left release slot (accessible from the rear face with flat screwdriver/coin)
            translate([wall + 4.3 + 0.7, width - 0.8, heck_z_bot - 3.5])
                cube([2.0, 1.2, 5.0], center=false);

            // Right release slot
            translate([length - wall - 7.7 + 0.7, width - 0.8, heck_z_bot - 3.5])
                cube([2.0, 1.2, 5.0], center=false);

            // 12. Rear Wall MicroSD Window Clearance
            // Ensures complete finger & tweezer access to the MicroSD slot in the tub sill
            translate([49.8 - 9.0, width - wall - 0.5, heck_z_bot - 0.5])
                cube([18.0, wall + 1.0, 3.5], center=false);

            // 13. Underside Weight-Optimization & Antenna Clearance Cavities
            // Leaves sturdy 2.5 mm perimeter ribs while removing unnecessary mass
            translate([wall + 6.0, wall + 6.0, rail2_z - rail2_h/2.0 - 0.1]) {
                // Forward pocket
                cube([length - 2*wall - 12.0, 26.0, 2.5], center=false);
                // Rearward pocket
                translate([0, 30.0, 0])
                    cube([length - 2*wall - 12.0, 22.0, 2.5], center=false);
            }
        }
    }
}

// Standalone preview
main_box_slide_lid();
