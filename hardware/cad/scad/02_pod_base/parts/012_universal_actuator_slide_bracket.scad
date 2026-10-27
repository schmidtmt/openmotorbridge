// =============================================================================
// OpenMotorBridge - Satellite Pod: Modular Dual-Strut Actuator System (v10.0)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad
// Description: Ultra-slim, fully modular dual-strut actuator system with 3-axis
//              independent adjustment (X, Y, Z), 100% IKEA-principle fasteners
//              (DIN 934 captive hex nuts), and external EPDM rail sealing plugs.
//
// Key Architectural Principles (v10.0 Monocoque Pod):
// 1. Two Independent Slot-In Cross-Struts (Querstreben):
//    - Replaces bulky 4-legged bridge plates with two independent, slim traversers.
//    - Slides freely along the X-axis in integrated sidewall C-rails (Z = 22.0 mm).
//    - Sidewall C-rail undercut absorbs 100% of the upward actuator reaction force
//      (3..5 N) directly into the rigid 3 mm PA12 monocoque sidewalls.
//    - The tub floor remains 100% smooth, sealed, and boss-free.
//
// 2. 3-Axis Independent Alignment (X, Y, Z):
//    - X-Axis (Longitudinal): Strut slides in sidewall rails to match button X.
//    - Y-Axis (Transverse): Carriage slides in central strut slot (Y = 16..54 mm).
//    - Z-Axis (Height): Vertical slot on carriage gives 8 mm continuous stroke
//      adjustment to match button heights across Cardo, Sena, Midland, and PMR.
//
// 3. 100% IKEA-Principle Fastening (Zero Heat-Set, Zero Screws into Plastic):
//    - All clamps use standard DIN 934 M2.5 stainless steel hex nuts held in
//      form-fit captive nut pockets.
//    - Infinite reuse, zero stripping, completely vibration-proof under 10G loads.
//
// 4. External EPDM Rubber Sealing Plugs (Gummistopfen):
//    - Pressed into the rear C-rail entry openings at the bulkhead.
//    - Seals the rail cavities 100% watertight (IP68) and acts as mechanical
//      anti-slip travel limiters.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;
use <../../00_common/dummies/dummy_intercom_units.scad>;

$fn = 28;

// 1. External EPDM Rail Sealing Plug (Gummistopfen)
module epdm_rail_sealing_plug() {
    color([0.12, 0.12, 0.14]) { // Matte EPDM rubber black
        // Plug stem inserting into C-rail pocket
        translate([-4.0, -1.6, -1.3])
            cube([4.0, 3.2, 2.6], center=false);
        // Outer sealing collar / flange (flush against rear exterior bulkhead)
        translate([0.0, -2.5, -2.2])
            hull() {
                translate([0, 0.5, 0.5]) cube([1.5, 4.0, 3.4]);
                translate([0, 0, 0]) cube([1.5, 5.0, 4.4]);
            }
        // Pull-tab / grip rib
        translate([1.5, -1.0, -0.6])
            cube([2.0, 2.0, 1.2], center=false);
    }
}

// 2. Independent Cross-Strut (Querstrebe mit Y-Langloch & bündig versenkten Schrauben)
module actuator_cross_strut(
    strut_w = 10.0,      // Width in X (mm)
    strut_th = 2.8,      // Thickness in Z (mm) - Ultra-slim 2.8 mm flat profile
    slot_len = 38.0,     // Length of central Y-slot (mm)
    slot_w = 2.8         // M2.5 clearance width (mm)
) {
    beam_len_y = 62.5;   // Interior span between sidewalls (Y = 3.75 to 66.25)
    tab_out = 2.4;       // Guide tab protrusion into sidewall C-rail
    tab_th  = 2.4;       // Tab thickness in Z (slides in 2.8 mm C-rail)

    color([0.22, 0.24, 0.27]) { // PA12 Carbon dark grey
        difference() {
            union() {
                // Central Traverse Beam - Completely flat top surface across entire span
                translate([-strut_w/2.0, (POD_OUTER_W - beam_len_y)/2.0, 0])
                    cube([strut_w, beam_len_y, strut_th], center=false);

                // Left Guide Tab (enters left sidewall C-rail at Y = 1.35..3.75 mm)
                translate([-strut_w/2.0 + 1.0, (POD_OUTER_W - beam_len_y)/2.0 - tab_out, (strut_th - tab_th)/2.0])
                    cube([strut_w - 2.0, tab_out + 0.1, tab_th], center=false);

                // Right Guide Tab (enters right sidewall C-rail at Y = 66.25..68.65 mm)
                translate([-strut_w/2.0 + 1.0, (POD_OUTER_W + beam_len_y)/2.0 - 0.1, (strut_th - tab_th)/2.0])
                    cube([strut_w - 2.0, tab_out + 0.1, tab_th], center=false);
            }

            // Central Y-Axis Slotted Guide Rail (Langloch für M2.5 Schraube)
            translate([0, POD_OUTER_W/2.0 - slot_len/2.0, -1.0])
                hull() {
                    cylinder(r=slot_w/2.0, h=strut_th + 2.0);
                    translate([0, slot_len, 0])
                        cylinder(r=slot_w/2.0, h=strut_th + 2.0);
                }

            // Continuous 90° Countersink along top of Y-slot for flush DIN 7991 M2.5 screw head
            translate([0, POD_OUTER_W/2.0 - slot_len/2.0, strut_th - 1.4])
                hull() {
                    cylinder(r1=slot_w/2.0, r2=2.6, h=1.5);
                    translate([0, slot_len, 0])
                        cylinder(r1=slot_w/2.0, r2=2.6, h=1.5);
                }

            // Left end clamping screw - 100% Flush Countersunk Bore (DIN 7991)
            translate([0, (POD_OUTER_W - beam_len_y)/2.0 + 3.5, -1.0])
                cylinder(r=1.4, h=strut_th + 2.0);
            translate([0, (POD_OUTER_W - beam_len_y)/2.0 + 3.5, strut_th - 1.4])
                cylinder(r1=1.4, r2=2.6, h=1.5);

            // Right end clamping screw - 100% Flush Countersunk Bore (DIN 7991)
            translate([0, (POD_OUTER_W + beam_len_y)/2.0 - 3.5, -1.0])
                cylinder(r=1.4, h=strut_th + 2.0);
            translate([0, (POD_OUTER_W + beam_len_y)/2.0 - 3.5, strut_th - 1.4])
                cylinder(r1=1.4, r2=2.6, h=1.5);
        }
    }

    // 2x M2.5 Stainless Steel Torx Flush Countersunk Screws (DIN 7991 A4) at strut ends
    // 100% Flush with the flat top deck - ZERO protrusion above the strut beam!
    color("silver") {
        translate([0, (POD_OUTER_W - beam_len_y)/2.0 + 3.5, strut_th - 1.4]) {
            cylinder(r1=1.4, r2=2.5, h=1.4, center=false);
            color("dimgray")
                translate([0, 0, 1.15]) cylinder(r=0.8, h=0.25, center=false, $fn=6);
        }
        translate([0, (POD_OUTER_W + beam_len_y)/2.0 - 3.5, strut_th - 1.4]) {
            cylinder(r1=1.4, r2=2.5, h=1.4, center=false);
            color("dimgray")
                translate([0, 0, 1.15]) cylinder(r=0.8, h=0.25, center=false, $fn=6);
        }
    }
}

// 3. Compact Under-Slung 2-in-1 Z-Carriage (Hängender Y-Schlitten + Z-Höhenverstellung mit 8 mm Hub)
module actuator_z_carriage(
    rocker_color = [0.92, 0.45, 0.10], // Orange or Blue
    z_offset = 0.0                      // Vertical height fine adjustment (-4..+4 mm)
) {
    carriage_l = 13.0;     // Dimension in X
    carriage_w = 11.0;     // Dimension in Y
    carriage_body_h = 7.0; // Body height hanging below strut

    // A. Under-Slung Sliding Carriage Block (rides directly against underside of strut)
    color([0.28, 0.30, 0.34]) {
        difference() {
            union() {
                // Main Under-Slung Body Block (hanging below Z = 0)
                translate([-carriage_l/2.0, -carriage_w/2.0, -carriage_body_h])
                    cube([carriage_l, carriage_w, carriage_body_h], center=false);

                // Upper Alignment Tongue (protrudes into strut Y-slot for zero-play guide)
                translate([-carriage_l/2.0 + 1.5, -1.3, 0.0])
                    cube([carriage_l - 3.0, 2.6, 2.0], center=false);
            }

            // Central Vertical Clamp Bore & Captive DIN 934 M2.5 Nut Pocket (accessible underneath)
            translate([0, 0, -carriage_body_h - 1.0])
                cylinder(r=1.4, h=carriage_body_h + 3.0);
            translate([0, 0, -carriage_body_h + 1.2])
                rotate([0, 0, 30])
                    hex_nut_pocket(sw=NUT_M2_5_SW, h=NUT_M2_5_H + 0.5, screw_r=1.4, through_h=4.0);

            // Vertical Z-Adjustment Slotted Guide (Langloch für Z-Hub)
            translate([0, carriage_w/2.0 + 0.1, -carriage_body_h/2.0])
                rotate([90, 0, 0])
                    hull() {
                        cylinder(r=1.4, h=carriage_w + 1.0);
                        translate([0, -3.5, 0])
                            cylinder(r=1.4, h=carriage_w + 1.0);
                    }
        }
    }

    // B. M2.5 Stainless Steel Flush Countersunk Screw (DIN 7991 Torx)
    // Sits 100% flush inside the strut's countersunk slot - ZERO protrusion upwards!
    color("silver") {
        translate([0, 0, 2.8 - 1.4]) {
            cylinder(r1=1.4, r2=2.5, h=1.4, center=false);
            color("dimgray")
                translate([0, 0, 1.15]) cylinder(r=0.8, h=0.25, center=false, $fn=6);
        }
    }

    // C. Micro-Actuator (Flat Horizontal 5V Solenoid + 90° Downward Bellcrank Rocker)
    translate([0, 0, z_offset]) {
        // Solenoid body
        color("silver")
            translate([7.0, 0, -carriage_body_h/2.0])
                rotate([0, 90, 0])
                    cylinder(r=2.2, h=10.0, center=true, $fn=20);
        color("gold")
            translate([1.5, 0, -carriage_body_h/2.0])
                rotate([0, 90, 0])
                    cylinder(r=1.5, h=3.0, center=true, $fn=16);

        // 90° Downward Bellcrank Rocker Arm
        color(rocker_color) {
            translate([0, 0, -carriage_body_h/2.0 - 3.0]) {
                rotate([0, 10, 0])
                    cube([2.8, 2.2, 5.0], center=true);
                translate([2.5, 0, 2.5])
                    cube([5.0, 1.8, 1.6], center=true);
            }
        }

        // Soft Shore A50 TPU Pusher Tip (depresses intercom key directly)
        color([rocker_color[0]*0.9, rocker_color[1]*0.9, rocker_color[2]*0.9])
            translate([0, 0, -carriage_body_h/2.0 - 6.5])
                cylinder(r=2.2, h=2.0, center=true, $fn=16);
    }
}

// 4. Universal Dual-Strut Actuator System (Master Module)
module universal_actuator_slide_bracket(
    strut1_x = 78.0,      // Front strut position along X (default: Cardo Media key)
    strut2_x = 119.0,     // Rear strut position along X (default: Cardo Intercom key)
    carriage1_y = 22.0,   // Front carriage position along Y (Media key Y)
    carriage2_y = 37.0,   // Rear carriage position along Y (Intercom key Y)
    carriage1_z = 0.0,    // Front carriage Z adjustment
    carriage2_z = 0.0,    // Rear carriage Z adjustment
    show_actuators = true,
    show_plugs = true,
    plug_x_offset = 0.0
) {
    strut_z = 21.6; // Height matching sidewall C-rail center

    // STRUT 1: Front Key Actuator Traverse
    translate([strut1_x, 0, strut_z]) {
        actuator_cross_strut();
        if (show_actuators) {
            translate([0, carriage1_y, 0])
                actuator_z_carriage(
                    rocker_color = [0.92, 0.45, 0.10], // Orange (Media)
                    z_offset = carriage1_z
                );
        }
    }

    // STRUT 2: Rear Key Actuator Traverse
    translate([strut2_x, 0, strut_z]) {
        actuator_cross_strut();
        if (show_actuators) {
            translate([0, carriage2_y, 0])
                actuator_z_carriage(
                    rocker_color = [0.15, 0.48, 0.88], // Blue (Intercom)
                    z_offset = carriage2_z
                );
        }
    }

    // External EPDM Rail Sealing Plugs (inserted from rear bulkhead at X = 150 mm)
    if (show_plugs) {
        // Left rail plug
        translate([POD_OUTER_L + plug_x_offset, POD_WALL + 0.8, strut_z + 1.5])
            rotate([0, 0, 0])
                epdm_rail_sealing_plug();

        // Right rail plug
        translate([POD_OUTER_L + plug_x_offset, POD_OUTER_W - POD_WALL - 0.8, strut_z + 1.5])
            rotate([0, 0, 0])
                epdm_rail_sealing_plug();
    }
}

// Complete Assembly: Cardo Packtalk Edge with Dual Slot-In Actuator Struts
module cardo_with_universal_slide_bracket_assembly() {
    // 1. Cardo OEM Air-Mount Cradle (Screwed directly to flat monocoque tub floor)
    translate([52.0, (POD_OUTER_W - 46.0)/2.0, POD_WALL])
        dummy_cardo_oem_airmount_cradle();

    // 2. Cardo Packtalk Edge (Docked inside cradle)
    translate([52.0, (POD_OUTER_W - 46.0)/2.0, POD_WALL + 3.5])
        dummy_cardo_packtalk_edge(with_actuators = false);

    // 3. Dual Slot-In Actuator Struts & Z-Carriages (Adjusted over Cardo Keys)
    universal_actuator_slide_bracket(
        strut1_x = 76.0,      // Aligned over Front Media Key
        strut2_x = 117.0,     // Aligned over Rear Intercom Key
        carriage1_y = 22.0,   // Media key Y
        carriage2_y = 37.0,   // Intercom key Y (15 mm lateral offset!)
        carriage1_z = -1.0,
        carriage2_z = -1.0,
        show_actuators = true,
        show_plugs = false
    );

    // Showcase 2x EPDM rail sealing plugs neatly at rear rail exits
    translate([132.0, 3.5, 23.1]) epdm_rail_sealing_plug();
    translate([132.0, 66.5, 23.1]) epdm_rail_sealing_plug();
}

// Standalone execution preview
cardo_with_universal_slide_bracket_assembly();
