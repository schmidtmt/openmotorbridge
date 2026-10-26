// =============================================================================
// OpenMotorBridge - Satellite Pod: Low-Profile 2D Rocker Actuator Plate
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/012_universal_actuator_slide_bracket.scad
// Description: Ultra-low-profile mechatronic 2D dual-rocker actuator plate
//              for automatic ignition-coupled Power-On / Power-Off (KL15).
//
// Solves:
// 1. Hardware Reality: Sena and Cardo DO NOT have USB-Power-On or BLE-Wakeup
//    when turned OFF. To power on/off with ignition, 2 buttons MUST be pressed!
// 2. Vertical Headroom: Pod interior is 32 mm, Cardo crest is 21.5 mm -> only 10.5 mm
//    clearance to lid! Vertical solenoids collide. This plate uses FLAT HORIZONTAL
//    micro-actuators with 90° downward rockers (total height only 6.5 mm!).
// 3. 2D Button Staggering: Cardo buttons are not 1D!
//    - Front Media Key: X = 22.0 mm, Y = 13.0 mm (narrow nose)
//    - Rear Intercom Key: X = 63.0 mm, Y = 28.0 mm (wide rear) -> 15 mm Y-offset!
// 4. Downward Pivot Domes: Domes and lever journals point DOWNWARD into the
//    negative space beside the keys, keeping the top surface 100% flush.
// 5. Positive Clamping & Routing: Plate clips securely onto the OEM Air-Mount cradle;
//    flat flex cable routes forward under the dry-flap to J_ACT on PCBA 03.
// =============================================================================

include <../../00_common/parameters.scad>;
use <../../00_common/dummies/dummy_intercom_units.scad>;

$fn = 32;

// Ultra-Flat 2D Dual-Rocker Actuator Plate
module cardo_edge_2d_rocker_plate(show_actuators = true) {
    plate_l = 86.0;
    plate_w = 46.0;
    plate_th = 2.0;

    // 1. Contoured Main Carrier Plate (Molded in Matte Anthracite PA12)
    color([0.22, 0.24, 0.27]) {
        difference() {
            union() {
                // Main low-profile deck
                translate([0, 0, 0])
                    cube([plate_l, plate_w, plate_th], center=false);

                // 4x Heavy-Duty Downward Structural Snap Legs (22.0 mm tall, reaching cradle base at Z = -22.0 mm!)
                // Firmly clamping Cardo Edge & latching under the OEM Air-Mount cradle bottom flange
                for (cx = [8.0, plate_l - 14.0]) {
                    // Left flank structural snap leg
                    translate([cx, -2.8, -22.0])
                        cube([7.0, 3.2, 22.0], center=false);
                    // Heavy snap hook barb under cradle base
                    translate([cx, -0.6, -22.8])
                        cube([7.0, 2.2, 2.2], center=false);

                    // Right flank structural snap leg
                    translate([cx, plate_w - 0.4, -22.0])
                        cube([7.0, 3.2, 22.0], center=false);
                    // Heavy snap hook barb under cradle base
                    translate([cx, plate_w - 1.6, -22.8])
                        cube([7.0, 2.2, 2.2], center=false);
                }

                // 2x Lateral Chassis Standoff Ears (Direct M2.5 floor boss bolting)
                // Left chassis ear at X = 44.0 mm, Y = -5.0 mm
                translate([41.0, -5.5, -22.0])
                    cube([8.0, 5.5, 24.0], center=false);
                // Right chassis ear at X = 44.0 mm, Y = plate_w
                translate([41.0, plate_w, -22.0])
                    cube([8.0, 5.5, 24.0], center=false);

                // Downward-pointing pivot bearing journals (Dome nach UNTEN!)
                // Front Lever 1 Journal at X = 22.0, Y = 13.0
                translate([19.0, 10.0, -4.5])
                    cube([6.0, 6.0, 5.0], center=false);

                // Rear Lever 2 Journal at X = 63.0, Y = 28.0 (15 mm lateral offset!)
                translate([60.0, 25.0, -4.5])
                    cube([6.0, 6.0, 5.0], center=false);
            }

            // Cutout window over Cardo center phone button & status LEDs
            translate([34.0, 12.0, -1.0])
                cube([18.0, 22.0, plate_th + 2.0], center=false);

            // Front Rocker Slot (X = 22.0 mm, Y = 13.0 mm)
            translate([20.0, 11.5, -5.0])
                cube([4.0, 3.0, 8.0], center=false);

            // Rear Rocker Slot (X = 63.0 mm, Y = 28.0 mm)
            translate([61.0, 26.5, -5.0])
                cube([4.0, 3.0, 8.0], center=false);

            // Cable exit chamfer at front nose
            translate([-1.0, 18.0, -1.0])
                cube([4.0, 10.0, plate_th + 2.0], center=false);

            // 2x M2.5 Chassis Screw Clearance Bores (Through lateral ears into floor bosses)
            translate([45.0, -2.8, -24.0])
                cylinder(r=1.4, h=30.0, center=false, $fn=16);
            translate([45.0, plate_w + 2.8, -24.0])
                cylinder(r=1.4, h=30.0, center=false, $fn=16);
        }
    }

    if (show_actuators) {
        // 2. 2x M2.5 Stainless Steel Chassis Fastening Screws (Bolted directly to pod floor brass inserts!)
        color("silver") {
            // Left M2.5 Torx Cap Screw
            translate([45.0, -2.8, plate_th]) {
                cylinder(r=2.3, h=1.8, center=false, $fn=20);
                translate([0, 0, 1.8]) cylinder(r=1.0, h=0.2, center=false, $fn=6); // hex socket
                translate([0, 0, -23.0]) cylinder(r=1.25, h=23.0, center=false, $fn=16);
            }
            // Right M2.5 Torx Cap Screw
            translate([45.0, plate_w + 2.8, plate_th]) {
                cylinder(r=2.3, h=1.8, center=false, $fn=20);
                translate([0, 0, 1.8]) cylinder(r=1.0, h=0.2, center=false, $fn=6); // hex socket
                translate([0, 0, -23.0]) cylinder(r=1.25, h=23.0, center=false, $fn=16);
            }
        }

        // 3. Front 90° Bellcrank Rocker Arm (Orange Anodized Aluminum)
        // Positioned at X = 22.0 mm, Y = 13.0 mm (Media / Power Key)
        color([0.92, 0.45, 0.10]) {
            translate([22.0, 13.0, -1.5]) {
                // Rocker body
                rotate([0, 12, 0])
                    cube([3.2, 2.4, 5.0], center=true);
                // Horizontal pull link
                translate([4.0, 0, 1.5])
                    cube([8.0, 1.8, 1.6], center=true);
            }
        }
        // Front Soft Shore A50 TPU Pusher Tip (Pushover Media Key)
        color([1.0, 0.6, 0.1])
            translate([22.0, 13.0, -4.5])
                cylinder(r=2.2, h=1.8, center=true, $fn=16);

        // 3. Rear 90° Bellcrank Rocker Arm (Blue Anodized Aluminum)
        // Positioned at X = 63.0 mm, Y = 28.0 mm (Intercom / Power Key - 15 mm Y-Offset!)
        color([0.15, 0.48, 0.88]) {
            translate([63.0, 28.0, -1.5]) {
                // Rocker body
                rotate([0, 12, 0])
                    cube([3.2, 2.4, 5.0], center=true);
                // Horizontal pull link
                translate([4.0, 0, 1.5])
                    cube([8.0, 1.8, 1.6], center=true);
            }
        }
        // Rear Soft Shore A50 TPU Pusher Tip (Pushover Intercom Key)
        color([0.2, 0.7, 1.0])
            translate([63.0, 28.0, -4.5])
                cylinder(r=2.2, h=1.8, center=true, $fn=16);

        // 4. Flat Horizontal Micro-Solenoid / Linear Actuators (Flachliegend: nur 5.0 mm hoch!)
        // Actuator 1 (Front, driving Media rocker)
        color("silver")
            translate([30.0, 13.0, plate_th + 1.2])
                rotate([0, 90, 0])
                    cylinder(r=2.2, h=12.0, center=true, $fn=20);
        color("gold")
            translate([24.0, 13.0, plate_th + 1.2])
                rotate([0, 90, 0])
                    cylinder(r=1.5, h=3.0, center=true, $fn=16);

        // Actuator 2 (Rear, driving Intercom rocker)
        color("silver")
            translate([71.0, 28.0, plate_th + 1.2])
                rotate([0, 90, 0])
                    cylinder(r=2.2, h=12.0, center=true, $fn=20);
        color("gold")
            translate([65.0, 28.0, plate_th + 1.2])
                rotate([0, 90, 0])
                    cylinder(r=1.5, h=3.0, center=true, $fn=16);

        // 5. Flat Actuator Ribbon Cable (routes forward under dry-flap to J_ACT on PCBA 03)
        color([0.15, 0.15, 0.15]) {
            translate([0, 20.0, 0.8])
                cube([30.0, 6.0, 0.6], center=false);
            // JST-SH 8-Pin connector plug
            translate([-4.0, 20.0, 0.2])
                cube([4.0, 6.0, 2.0], center=false);
        }
    }
}

// Complete assembly: Cardo Packtalk Edge WITH 2D Rocker Plate clicked into cradle
module cardo_with_2d_rocker_plate_assembly() {
    // A. Cardo OEM Air-Mount Cradle (Screwed to pod floor)
    dummy_cardo_oem_airmount_cradle();

    // B. Cardo Packtalk Edge (Docked inside cradle)
    translate([0, 0, 3.5])
        dummy_cardo_packtalk_edge(with_actuators = false);

    // C. Ultra-Flat 2D Dual-Rocker Plate (Clicked onto cradle, height = only 6.5 mm!)
    translate([-1.0, 0, 22.0])
        cardo_edge_2d_rocker_plate(show_actuators = true);
}

// Standalone execution preview
cardo_with_2d_rocker_plate_assembly();
