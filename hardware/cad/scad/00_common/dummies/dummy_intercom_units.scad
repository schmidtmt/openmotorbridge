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

    // A. Main Aerodynamic Wedge Body
    color([0.16, 0.17, 0.19]) {
        hull() {
            // Front Nose
            translate([0, body_w*0.2, 0])
                cube([2.0, body_w*0.6, body_h_front]);
            // Rear Base
            translate([body_l - 12.0, 0, 0])
                cube([10.0, body_w, body_h_rear]);
        }
    }

    // B. Rear Control Roller Wheel
    color([0.25, 0.26, 0.28]) {
        translate([body_l - 6.0, body_w/2.0, body_h_rear * 0.65]) {
            rotate([0, 90, 0]) {
                cylinder(r=10.0, h=7.0, center=true, $fn=32);
                // Silver center hub
                color([0.8, 0.8, 0.85])
                    cylinder(r=4.5, h=7.4, center=true, $fn=24);
            }
        }
    }

    // C. 3 Slanted Tactile Buttons on Top Ridge
    // Button 1: Front (Media / Power Key)
    color([0.12, 0.12, 0.14]) {
        translate([24.0, body_w/2.0 - 6.0, body_h_front + 1.2])
            rotate([0, -8, 0])
                cube([14.0, 12.0, 2.5], center=true);
        // Button 2: Middle (Mobile Phone Key)
        translate([44.0, body_w/2.0 - 6.0, body_h_front + 3.8])
            rotate([0, -8, 0])
                cube([14.0, 12.0, 2.5], center=true);
        // Button 3: Rear (DMC Intercom / Power Key)
        translate([63.0, body_w/2.0 - 6.0, body_h_front + 6.4])
            rotate([0, -8, 0])
                cube([14.0, 12.0, 2.5], center=true);
    }

    // D. Outer Flank Status LED Bar (Cyan glow)
    color([0.0, 0.85, 1.0, 0.9]) {
        translate([30.0, body_w - 0.5, body_h_front * 0.6])
            cube([32.0, 1.2, 2.2]);
    }

    // E. Silver "cardo" Branding Badge
    color([0.85, 0.85, 0.9]) {
        translate([34.0, 0.8, body_h_front * 0.55])
            cube([22.0, 0.6, 3.5]);
    }

    // F. 2 MECHATRONIC ACTUATORS WITH RECTANGULAR ANGLED FEET
    if (with_actuators) {
        // Actuator Bridge / Support Carrier
        color("darkslategray", 0.9) {
            translate([20.0, body_w/2.0 - 15.0, body_h_rear + 6.0])
                cube([48.0, 18.0, 3.0]);
            // Side Mounting Legs
            translate([20.0, body_w/2.0 - 15.0, body_h_front + 2.0])
                cube([4.0, 18.0, body_h_rear - body_h_front + 4.0]);
            translate([64.0, body_w/2.0 - 15.0, body_h_rear - 2.0])
                cube([4.0, 18.0, 8.0]);
        }

        // Two independent solenoid plungers:
        // Actuator 1: over Front Button (Media / Power) at X = 24.0
        // Actuator 2: over Rear Button (Intercom / Power) at X = 63.0
        for (ax = [24.0, 63.0]) {
            // Solenoid Coil Housing
            color("silver")
                translate([ax, body_w/2.0 - 6.0, body_h_rear + 7.5])
                    cylinder(r=3.2, h=10.0, center=false, $fn=24);

            // Stainless Steel Helical Coil Spring
            color("gold")
                translate([ax, body_w/2.0 - 6.0, body_h_rear + 0.5])
                    cylinder(r=2.5, h=6.0, center=false, $fn=16);

            // Plunger Shaft
            color("silver")
                translate([ax, body_w/2.0 - 6.0, body_h_front + 2.0])
                    cylinder(r=1.2, h=body_h_rear - body_h_front + 16.0, center=false, $fn=16);

            // RECTANGULAR ANGLED FOOT (matching slanted narrow OEM keys)
            color([0.95, 0.5, 0.1]) { // High-vis amber TPU tip
                translate([ax, body_w/2.0 - 6.0, (ax == 24.0 ? body_h_front + 2.5 : body_h_front + 7.5)])
                    rotate([0, -8, 0])
                        cube([10.0, 6.5, 3.0], center=true);
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
