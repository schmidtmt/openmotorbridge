// =============================================================================
// OpenMotorBridge - OEM Intercom & Accessory 3D Dummy Models
// =============================================================================
// File: hardware/cad/scad/00_common/dummies/dummy_intercom_units.scad
// Description: High-precision photorealistic 3D dummy models for CAD visualization:
//              1. Cardo Packtalk Edge (Aerodynamic wedge, roller wheel, 3 buttons)
//                 + 2 Mechatronic Actuators with rectangular angled feet
//              2. Sena SPIDER X Slim (Curved tapered body, 3 buttons, mesh key)
//                 + Quick-Clamp retaining bracket with knurled brass thumbscrew
//              3. 5V COTS Bi-Directional RF Booster (25x15x6 mm, blue heatsink, SMA)
// =============================================================================

// -----------------------------------------------------------------------------
// 1. CARDO PACKTALK EDGE OEM INTERCOM DUMMY
// -----------------------------------------------------------------------------
module dummy_cardo_packtalk_edge(with_actuators = true) {
    body_l = 84.0;
    body_w = 46.0;
    body_h_front = 14.0;
    body_h_rear  = 23.0;
    y_center     = body_w / 2.0;

    // A. Main Aerodynamic Wedge Body with Sculpted Central Concave Depression (Vertiefung)
    color([0.16, 0.17, 0.19]) {
        difference() {
            hull() {
                // Front Nose
                translate([0, body_w*0.2, 0])
                    cube([2.0, body_w*0.6, body_h_front]);
                // Rear Base
                translate([body_l - 12.0, 0, 0])
                    cube([10.0, body_w, body_h_rear]);
            }
            // Ergonomic Central Concave Depression (Vertiefung / Air-Mount waist scoop at X = 42 mm)
            // Carves out a smooth concave saddle dip between front and rear button ridges
            translate([42.0, y_center - 4.0, body_h_rear + 7.5])
                rotate([0, 90, 0])
                    cylinder(r=16.0, h=34.0, center=true, $fn=48);
        }
    }

    // B. Rear Control Roller Wheel
    color([0.25, 0.26, 0.28]) {
        translate([body_l - 6.0, y_center, body_h_rear * 0.65]) {
            rotate([0, 90, 0]) {
                cylinder(r=10.0, h=7.0, center=true, $fn=32);
                // Silver center hub
                color([0.8, 0.8, 0.85])
                    cylinder(r=4.5, h=7.4, center=true, $fn=24);
            }
        }
    }

    // C. 3 Slanted Tactile Buttons on Top Ridge
    // Button 1: Front Ridge (Media / Power Key)
    color([0.12, 0.12, 0.14]) {
        translate([22.0, y_center - 6.0, body_h_front - 0.5])
            rotate([0, -8, 0])
                cube([12.0, 10.0, 2.2], center=true);
        // Button 2: Center (Phone Key - recessed flush in the bottom of the depression)
        translate([42.0, y_center - 6.0, 9.8])
            cube([11.0, 9.0, 1.8], center=true);
        // Button 3: Rear Ridge (DMC Intercom / Power Key)
        translate([63.0, y_center - 6.0, body_h_rear - 3.2])
            rotate([0, 10, 0])
                cube([12.0, 10.0, 2.2], center=true);
    }

    // D. Outer Flank Status LED Bar (Cyan glow)
    color([0.0, 0.85, 1.0, 0.9]) {
        translate([28.0, body_w - 0.5, body_h_front * 0.55])
            cube([32.0, 1.2, 2.2]);
    }

    // E. Silver "cardo" Branding Badge
    color([0.85, 0.85, 0.9]) {
        translate([32.0, 0.8, body_h_front * 0.5])
            cube([22.0, 0.6, 3.5]);
    }

    // F. 2 MECHATRONIC ACTUATORS WITH RECTANGULAR ANGLED FEET
    // Twin independent cantilever towers over Front & Rear Power keys (leaving the center depression open!)
    if (with_actuators) {
        // Solenoid 1: Over Front Button (Media / Power) at X = 22.0 mm
        // Solenoid 2: Over Rear Button (Intercom / Power) at X = 63.0 mm
        for (cfg = [[22.0, body_h_front + 12.0, body_h_front - 0.5, -8],
                    [63.0, body_h_rear + 9.0,  body_h_rear - 3.2,   10]]) {
            ax     = cfg[0];
            z_coil = cfg[1];
            z_btn  = cfg[2];
            rot_y  = cfg[3];

            // Slender Cantilever Support Post (Anthracite PA12)
            color("darkslategray", 0.9) {
                translate([ax - 4.0, y_center - 15.0, 0])
                    cube([8.0, 3.0, z_coil]);
                translate([ax - 4.0, y_center - 15.0, z_coil - 3.0])
                    cube([8.0, 12.0, 3.0]);
            }

            // Solenoid Coil Housing (Silver / Metallic)
            color("silver")
                translate([ax, y_center - 6.0, z_coil])
                    cylinder(r=3.0, h=9.0, center=false, $fn=24);

            // Stainless Steel Helical Coil Spring
            color("gold")
                translate([ax, y_center - 6.0, z_coil - 5.0])
                    cylinder(r=2.2, h=5.0, center=false, $fn=16);

            // Plunger Shaft
            color("silver")
                translate([ax, y_center - 6.0, z_btn + 1.5])
                    cylinder(r=1.2, h=z_coil - z_btn + 2.0, center=false, $fn=16);

            // RECTANGULAR ANGLED FOOT (matching slanted narrow OEM keys)
            color([0.95, 0.5, 0.1]) { // High-vis amber TPU tip
                translate([ax, y_center - 6.0, z_btn + 1.2])
                    rotate([0, rot_y, 0])
                        cube([9.0, 5.5, 2.4], center=true);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// 1b. CARDO PACKTALK EDGE ORIGINAL OEM AIR-MOUNT CRADLE
// -----------------------------------------------------------------------------
module dummy_cardo_oem_airmount_cradle() {
    cradle_l = 84.0;
    cradle_w = 46.0;
    cradle_h = 6.5;

    // A. Black Automotive PA66 Injection-Molded Cradle Base
    color([0.13, 0.13, 0.15]) {
        difference() {
            cube([cradle_l, cradle_w, cradle_h], center=false);
            // Recessed magnetic docking bed
            translate([2.0, 2.0, 1.8])
                cube([cradle_l - 4.0, cradle_w - 4.0, cradle_h]);
            // 2x M2.5 / M3 OEM Mounting screw counterbore holes to sled floor
            translate([15.0, cradle_w/2.0, -0.5])
                cylinder(r=1.5, h=3.0, center=false, $fn=16);
            translate([cradle_l - 15.0, cradle_w/2.0, -0.5])
                cylinder(r=1.5, h=3.0, center=false, $fn=16);
        }
    }

    // B. Dual Embedded N52 Neodymium Air-Mount Permanent Magnets (Ø 8.0 x 3.0 mm)
    color("silver") {
        translate([24.0, cradle_w/2.0, 1.5])
            cylinder(r=4.0, h=3.0, center=false, $fn=32);
        translate([62.0, cradle_w/2.0, 1.5])
            cylinder(r=4.0, h=3.0, center=false, $fn=32);
    }

    // C. 5-Pin Gold-Plated Spring Pogo Contact Array
    color("gold") {
        for (i = [-2:2]) {
            translate([43.0 + i * 2.54, cradle_w/2.0, 1.2]) {
                cylinder(r=0.8, h=3.2, center=false, $fn=16);
                translate([0, 0, 3.2]) sphere(r=0.8, $fn=16);
            }
        }
    }

    // D. Cardo Mechanical Spring Release Latch (on outboard flank)
    color([0.22, 0.22, 0.25]) {
        translate([40.0, -2.5, 1.5])
            cube([16.0, 3.0, 4.0]);
        // Latch lever tooth
        translate([44.0, -3.5, 2.0])
            cube([8.0, 1.5, 3.0]);
    }

    // E. Factory Cable Pigtail exiting front towards PCBA 03 (-X)
    // Rubber strain relief boot
    color([0.1, 0.1, 0.1]) {
        translate([-4.0, cradle_w/2.0 - 5.0, 1.5])
            cube([5.0, 10.0, 3.5]);
        // Cable harness running forward
        translate([-12.0, cradle_w/2.0 - 2.0, 2.0])
            cube([9.0, 4.0, 2.5]);
    }
    // 3.5mm Stereo Audio Plug & Mic Lead at end of harness
    color("silver") {
        translate([-16.0, cradle_w/2.0 - 1.0, 2.0])
            rotate([0, 90, 0])
                cylinder(r=1.8, h=5.0, $fn=16);
    }
    color("gold") {
        translate([-19.0, cradle_w/2.0 - 1.0, 2.0])
            rotate([0, 90, 0])
                cylinder(r=1.0, h=3.5, $fn=16);
    }
}

// -----------------------------------------------------------------------------
// 2. SENA SPIDER X SLIM OEM INTERCOM DUMMY
// -----------------------------------------------------------------------------
module dummy_sena_spider_x_slim() {
    body_l = 74.5;
    body_w = 31.0;
    body_h = 16.0;

    // A. Main Sleek Ergonomic Body (Curved & Tapered ends)
    color([0.18, 0.19, 0.22]) {
        hull() {
            // Front curved nose
            translate([6.0, body_w/2.0, 0])
                cylinder(r=body_w*0.35, h=body_h - 2.0, $fn=24);
            // Center wide section
            translate([body_l/2.0, body_w/2.0, 0])
                cylinder(r=body_w*0.48, h=body_h, $fn=24);
            // Rear curved tail
            translate([body_l - 6.0, body_w/2.0, 0])
                cylinder(r=body_w*0.32, h=body_h - 3.0, $fn=24);
        }
    }

    // B. Top Tactile 3-Button Field: (+), Center, (-)
    color([0.10, 0.11, 0.13]) {
        // (+) Button
        translate([22.0, body_w/2.0, body_h - 0.2]) {
            cube([12.0, 14.0, 2.0], center=true);
            color("silver") {
                translate([0, 0, 1.2]) cube([6.0, 1.8, 0.6], center=true);
                translate([0, 0, 1.2]) cube([1.8, 6.0, 0.6], center=true);
            }
        }
        // Center Button
        translate([37.0, body_w/2.0, body_h]) {
            cube([12.0, 14.0, 2.0], center=true);
            color("silver")
                translate([0, 0, 1.2]) cylinder(r=2.5, h=0.6, center=true, $fn=16);
        }
        // (-) Button
        translate([52.0, body_w/2.0, body_h - 0.2]) {
            cube([12.0, 14.0, 2.0], center=true);
            color("silver")
                translate([0, 0, 1.2]) cube([6.0, 1.8, 0.6], center=true);
        }
    }

    // C. Lateral Mesh Intercom Key & Folded Antenna
    color([0.12, 0.13, 0.15]) {
        translate([28.0, -1.5, body_h*0.4])
            cube([24.0, 3.0, 6.0]);
        // Mesh Logo Accent
        color([0.9, 0.2, 0.2])
            translate([36.0, -2.0, body_h*0.45])
                cube([8.0, 0.8, 4.0]);
    }
}

// -----------------------------------------------------------------------------
// 2b. SENA SPIDER X SLIM ORIGINAL OEM QUICK-SNAP CRADLE
// -----------------------------------------------------------------------------
module dummy_sena_oem_cradle() {
    cradle_l = 76.0;
    cradle_w = 33.0;
    cradle_h = 3.5;

    // A. Black Automotive PA66 Slim Quick-Snap Cradle Base
    color([0.12, 0.12, 0.14]) {
        difference() {
            cube([cradle_l, cradle_w, cradle_h], center=false);
            // Recessed bed for Sena unit
            translate([2.0, 1.5, 1.2])
                cube([cradle_l - 4.0, cradle_w - 3.0, cradle_h]);
            // Floor mounting holes to sled
            translate([12.0, cradle_w/2.0, -0.5])
                cylinder(r=1.2, h=3.0, $fn=16);
            translate([cradle_l - 12.0, cradle_w/2.0, -0.5])
                cylinder(r=1.2, h=3.0, $fn=16);
        }
        // End snap tabs
        translate([0, cradle_w/2.0 - 4.0, 1.2])
            cube([2.0, 8.0, 3.5]);
        translate([cradle_l - 2.0, cradle_w/2.0 - 4.0, 1.2])
            cube([2.0, 8.0, 3.5]);
    }

    // B. Factory 3-Wire Cable Peitsche (Direct-Power, Mic, Speaker) exiting front (-X)
    color([0.1, 0.1, 0.1]) {
        translate([-4.0, cradle_w/2.0 - 3.0, 1.0])
            cube([5.0, 6.0, 2.2]);
        translate([-12.0, cradle_w/2.0 - 1.5, 1.2])
            cube([9.0, 3.0, 1.8]);
    }
    // Miniature gold contact pins / JST plug at front
    color("gold") {
        translate([-15.0, cradle_w/2.0 - 2.0, 1.2])
            cube([3.5, 4.0, 1.8]);
    }
}

// -----------------------------------------------------------------------------
// 3. 5V COTS BI-DIRECTIONAL RF BOOSTER DUMMY (25x15x6 mm)
// -----------------------------------------------------------------------------
module dummy_rf_booster_5v() {
    booster_l = 25.0;
    booster_w = 15.0;
    booster_h = 6.0;

    // Anodized Blue CNC Aluminum Shielded Housing
    color([0.15, 0.42, 0.85]) {
        difference() {
            cube([booster_l, booster_w, booster_h], center=false);
            // Heatsink Micro-Grooves on top
            for (gx = [4.0 : 3.0 : booster_l - 4.0]) {
                translate([gx, -0.1, booster_h - 1.2])
                    cube([1.2, booster_w + 0.2, 1.5]);
            }
        }
    }

    // Gold RF Connectors at both ends (SMA / U.FL)
    color("gold") {
        // RF Input Port (-X)
        translate([-2.5, booster_w/2.0, booster_h/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.2, h=3.0, center=false, $fn=16);
        // RF Output Port (+X)
        translate([booster_l - 0.5, booster_w/2.0, booster_h/2.0])
            rotate([0, 90, 0])
                cylinder(r=2.2, h=3.0, center=false, $fn=16);
    }

    // 5V DC Power Solder Leads (Red & Black)
    color("red")
        translate([booster_l/2.0 - 2.0, 1.0, booster_h])
            cylinder(r=0.6, h=3.0, $fn=10);
    color("black")
        translate([booster_l/2.0 + 2.0, 1.0, booster_h])
            cylinder(r=0.6, h=3.0, $fn=10);
}
