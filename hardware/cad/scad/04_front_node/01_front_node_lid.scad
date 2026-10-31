// =============================================================================
// OpenMotorBridge - Universal Front Node: L-Slide Lid (v10.0 Monocoque)
// =============================================================================
// File: hardware/cad/scad/04_front_node/01_front_node_lid.scad
// Description: HP MJF PA12 waterproof slide lid (Schiebedeckel) utilizing the v10
//              Monocoque Slide-In Principle:
//              1. Lateral guide tongues engaging longitudinal C-grooves (Z = 16.5 mm).
//              2. Front wedge-lock nose (Keilanzug) seating into East wall undercut.
//              3. Monolithic vertical Heckwand (West end) with lower sill drip apron.
//              4. Dual deadbolt snap-latches engaging lower sill sockets.
//              5. Integrated Gore ePTFE pressure compensation membrane seat.
//              6. Top docking interface (snap slots) for environmental Sensor Puck.
//              7. Status LED optical light-pipe aperture over LED1.
//              8. Universal Dual-Antenna Cradles for ESP32-E22 (2x2 MIMO 5/6 GHz):
//                 - Recessed adhesive nests for 2x Flex PCB dipoles (Taoglas FXP73 / Molex)
//                 - Snap-in C-clips for 2x internal omnidirectional stub antennas (Ø 6.5 mm)
//                 - Strain-relief coaxial wire routing channels to ANT1 & ANT2.
// =============================================================================

include <../00_common/parameters.scad>;

module front_node_upper_lid() {
    ch_x_start   = FRONT_NODE_WALL + 3.5; // 6.0 mm
    ch_y_start   = FRONT_NODE_WALL + 3.5; // 6.0 mm
    rail_z       = FRONT_NODE_RAIL_Z;     // 16.5 mm
    rail_h       = 2.4;                   // Tongue height (clearance inside 2.8 mm C-groove)
    tongue_prot  = 1.4;                   // Tongue protrusion into C-groove
    lid_top_z    = FRONT_NODE_OUTER_H;    // 22.0 mm
    lid_th       = lid_top_z - (rail_z - rail_h/2.0); // ~6.7 mm

    color([0.22, 0.24, 0.26]) {
        difference() {
            union() {
                // 1. Horizontal Slide Lid Main Plate
                // Fits inside tub chamber (Y = ch_y_start + 0.3 .. ch_y_start + FRONT_NODE_CHAMBER_W - 0.3)
                translate([ch_x_start - 0.5, ch_y_start + 0.3, rail_z - rail_h/2.0]) {
                    cube([
                        FRONT_NODE_CHAMBER_L + 0.5,
                        FRONT_NODE_CHAMBER_W - 0.6,
                        lid_th
                    ], center=false);
                }

                // 2. South Lateral Guide Tongue (engages South C-Groove)
                translate([ch_x_start + 1.0, ch_y_start - tongue_prot + 0.3, rail_z - rail_h/2.0]) {
                    cube([FRONT_NODE_CHAMBER_L - 3.0, tongue_prot + 0.2, rail_h], center=false);
                    // 45° Lead-in chamfer at front (East) tip
                    translate([FRONT_NODE_CHAMBER_L - 3.0, 0, 0])
                        linear_extrude(height=rail_h)
                            polygon(points=[[0, 0], [2.0, tongue_prot], [0, tongue_prot]]);
                }

                // 3. North Lateral Guide Tongue (engages North C-Groove)
                translate([ch_x_start + 1.0, ch_y_start + FRONT_NODE_CHAMBER_W - 0.5, rail_z - rail_h/2.0]) {
                    cube([FRONT_NODE_CHAMBER_L - 3.0, tongue_prot + 0.2, rail_h], center=false);
                    // 45° Lead-in chamfer at front (East) tip
                    translate([FRONT_NODE_CHAMBER_L - 3.0, 0, 0])
                        linear_extrude(height=rail_h)
                            polygon(points=[[0, 0], [0, -tongue_prot], [2.0, -tongue_prot]]);
                }

                // 4. Front Wedge-Lock Nose (Keilanzug into East wall undercut)
                translate([ch_x_start + FRONT_NODE_CHAMBER_L - 0.1, ch_y_start + 2.0, rail_z - 0.4]) {
                    cube([1.6, FRONT_NODE_CHAMBER_W - 4.0, rail_h + 0.8], center=false);
                }

                // 5. Monolithic Rear Vertical Heckwand (West end: X = 0..6.0 mm, Z = 6.0..22.0 mm)
                translate([0, ch_y_start, FRONT_NODE_REAR_SILL_H]) {
                    cube([ch_x_start + 0.5, FRONT_NODE_CHAMBER_W, lid_top_z - FRONT_NODE_REAR_SILL_H], center=false);
                }

                // Drip Apron (Tropfnase) overlapping lower sill down to Z = 3.5 mm
                translate([0, ch_y_start - 0.5, 3.5]) {
                    cube([2.2, FRONT_NODE_CHAMBER_W + 1.0, FRONT_NODE_REAR_SILL_H - 3.5 + 0.5], center=false);
                }

                // 6. Dual Slam-to-Shut Deadbolt Locking Legs (West corners into sill sockets)
                // Left locking leg
                translate([2.1, ch_y_start + 4.2, 2.0]) {
                    cube([3.0, 3.0, FRONT_NODE_REAR_SILL_H - 2.0 + 1.0], center=false);
                    // Snap catch barb
                    translate([0, -0.6, 0])
                        cube([3.0, 0.8, 1.6], center=false);
                }
                // Right locking leg
                translate([2.1, ch_y_start + FRONT_NODE_CHAMBER_W - 7.2, 2.0]) {
                    cube([3.0, 3.0, FRONT_NODE_REAR_SILL_H - 2.0 + 1.0], center=false);
                    // Snap catch barb
                    translate([0, 2.8, 0])
                        cube([3.0, 0.8, 1.6], center=false);
                }

                // 7. Internal Antenna Snap-In C-Clips (for optional internal stub antennas Ø 6.5 mm)
                // North Stub Antenna C-Clips (Bay 1)
                for (cx = [25.0, 55.0]) {
                    translate([ch_x_start + cx, ch_y_start + FRONT_NODE_CHAMBER_W - 6.5, rail_z - rail_h/2.0]) {
                        difference() {
                            cylinder(r=4.2, h=3.0, $fn=24);
                            translate([0, 0, -0.1])
                                cylinder(r=3.25, h=3.2, $fn=24); // Ø 6.5 mm bore
                            translate([-5.0, 0, -0.1])
                                cube([10.0, 5.0, 3.5], center=false); // snap entry opening
                        }
                    }
                }
                // South / Transverse Stub Antenna C-Clips (Bay 2)
                for (cx = [25.0, 55.0]) {
                    translate([ch_x_start + cx, ch_y_start + 6.5, rail_z - rail_h/2.0]) {
                        difference() {
                            cylinder(r=4.2, h=3.0, $fn=24);
                            translate([0, 0, -0.1])
                                cylinder(r=3.25, h=3.2, $fn=24); // Ø 6.5 mm bore
                            translate([-5.0, -5.0, -0.1])
                                cube([10.0, 5.0, 3.5], center=false); // snap entry opening
                        }
                    }
                }
            }

            // --- SUBTRACTIONS (Lid Cavities & Interfaces) ---

            // 8. Internal Weight & Clearance Hollow (Z = rail_z - rail_h/2.0 .. lid_top_z - 2.0 mm)
            translate([ch_x_start + 1.0, ch_y_start + 1.5, rail_z - rail_h/2.0 - 0.1]) {
                cube([FRONT_NODE_CHAMBER_L - 2.0, FRONT_NODE_CHAMBER_W - 3.0, lid_th - 2.0 + 0.1], center=false);
            }

            // 9. Universal Wi-Fi 6E Antenna Pockets (Taoglas FXP73 / Molex Flex PCB Dipoles 46 x 9 mm)
            // Bay 1: Longitudinal Flex Antenna Nest (North zone)
            translate([ch_x_start + 15.0, ch_y_start + FRONT_NODE_CHAMBER_W - 11.5, lid_top_z - 2.0 - 0.7]) {
                cube([46.0, 9.0, 0.8], center=false);
                // U.FL Coaxial routing channel leading towards West / North-West (ANT1)
                translate([-14.0, 3.5, -0.5])
                    cube([15.0, 2.0, 1.4], center=false);
            }

            // Bay 2: Longitudinal Flex Antenna Nest (South zone - 90° spatial diversity)
            translate([ch_x_start + 15.0, ch_y_start + 2.5, lid_top_z - 2.0 - 0.7]) {
                cube([46.0, 9.0, 0.8], center=false);
                // U.FL Coaxial routing channel leading towards West / South-West (ANT2)
                translate([-14.0, 3.5, -0.5])
                    cube([15.0, 2.0, 1.4], center=false);
            }

            // 10. Gore ePTFE Breather Vent Seat (Center-West of lid)
            translate([ch_x_start + 25.0, ch_y_start + FRONT_NODE_CHAMBER_W / 2.0, lid_top_z - 1.2]) {
                // Circular membrane nest Ø 10.0 mm x 1.2 mm
                cylinder(r=5.0, h=1.5, center=false, $fn=32);
                // Central through-vent bore Ø 3.0 mm
                translate([0, 0, -4.0])
                    cylinder(r=1.5, h=5.0, center=false, $fn=24);
            }

            // 11. Modular Sensor Puck Docking Interface (Snap Slots matching sensor_puck_environmental)
            // Sensor Puck footprint is 44 x 44 mm, centered at X = ch_x_start + 55 mm, Y = ch_y_start + 28 mm
            // Slot 1 (South catch): Y = 10.0 mm
            translate([ch_x_start + 55.0 - 8.5, ch_y_start + 28.0 - 22.0 - 1.5, lid_top_z - 3.2]) {
                cube([17.0, 2.8, 3.5], center=false);
                // Catch barb undercut
                translate([0, -0.8, 0])
                    cube([17.0, 1.2, 1.8], center=false);
            }
            // Slot 2 (North catch): Y = 46.0 mm
            translate([ch_x_start + 55.0 - 8.5, ch_y_start + 28.0 + 22.0 - 1.3, lid_top_z - 3.2]) {
                cube([17.0, 2.8, 3.5], center=false);
                // Catch barb undercut
                translate([0, 2.4, 0])
                    cube([17.0, 1.2, 1.8], center=false);
            }

            // 12. Status LED Light-Pipe Aperture (Ø 3.0 mm over LED1 at East side)
            // KiCad LED1 is at relative X=80.20 mm, Y=37.08 mm
            translate([ch_x_start + 2.0 + 80.20 - 4.0, ch_y_start + 3.0 + (50.0 - 37.08), lid_top_z - 3.0]) {
                cylinder(r=1.6, h=4.0, center=false, $fn=24);
                // Counterbore dome for light diffuser
                cylinder(r=2.5, h=1.5, center=false, $fn=24);
            }

            // 13. Service Release Pry Slot on Rear Heckwand (West face at X = 0)
            translate([-0.1, ch_y_start + FRONT_NODE_CHAMBER_W / 2.0 - 6.0, lid_top_z - 2.5]) {
                cube([2.5, 12.0, 2.0], center=false);
            }
        }
    }
}

// Standalone compilation
front_node_upper_lid();
