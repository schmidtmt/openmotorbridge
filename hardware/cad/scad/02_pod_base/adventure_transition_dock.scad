// =============================================================================
// OpenMotorBridge - Adventure Transition Dock (Sitzbank-Bügelfalten-Konsole)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_transition_dock.scad
// Description: Two-piece automotive-sculpted console for universal Satellite Pods
//              (Pod 1 Left, Pod 2 Right) on BMW GS / Adventure bikes.
//              Integrates seamlessly into the optical waist crease ("Bügelfalte")
//              between rider and pillion seat.
//
//              Key Engineering Features:
//              1. Two-Piece Architecture: Lower Base Cradle + Upper Styled Deckel (Cowl).
//              2. Parting line hidden along the sharp lateral "Bügelfalte" character crease.
//              3. Rigid Under-Seat Bridge Interface: Inboard tongue bolts directly to
//                 `adventure_underseat_cross_rail.scad` (Zero-Drill, Zero-Torque).
//              4. 100% Hidden Cable Routing: 90° downward M8 PUR conduit routes directly
//                 into the under-seat rail and Central Box (zero visible external wires).
//              5. Aerodynamic Wedge Form: 22° tapered leading wedge blends into rider seat,
//                 eliminating snag with rider pants or boots.
//              6. Dual Lid Options:
//                 - "open_intercom": Sculpted bezel framing Cardo/Sena unit flush like OEM.
//                 - "closed_smooth": Seamless aerodynamic cover for blind box or internal transceiver.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
TD_POD_L            = 136.0; // Internal pod length clearance (mm)
TD_POD_W            = 71.0;  // Internal pod width clearance (mm)
TD_POD_H            = 38.5;  // Pod height (mm)
TD_WALL             = 3.2;   // Wall thickness (mm)
TD_FLOOR            = 3.5;   // Base floor thickness (mm)

// Outer Console Envelope
CONSOLE_TOTAL_L     = 192.0; // Stretched aerodynamic length (mm)
CONSOLE_NOSE_L      = 32.0;  // Front leading wedge extension (mm)
CONSOLE_TAIL_L      = 24.0;  // Rear tapering aero tail extension (mm)
CONSOLE_MAX_W       = 84.0;  // Outer maximum width at waist (mm)
CONSOLE_CREASE_Z    = 22.0;  // Height of lateral Bügelfalte character line (mm)
CONSOLE_TOTAL_H     = 42.0;  // Total height with lid (mm)

// Subframe tube interface (Ø 28 mm typical)
TUBE_R              = 14.0;  // Tube radius (mm)
TUBE_DROP_Z         = 10.0;  // Centerline drop below pod floor (mm)

// Under-Seat Cross-Rail Inboard Tongue
TONGUE_EXT_Y        = 24.0;  // Inboard tongue extension into bike center (mm)
TONGUE_WIDTH_X      = 40.0;  // Longitudinal width of tongue (mm)
TONGUE_THICK        = 5.0;   // Solid thickness (mm)
TONGUE_SCREW_DIST   = 24.0;  // Distance between M4 fastening holes (mm)

// Fastening Screws (4x M3 Torx connecting Lid to Base)
LID_SCREW_X1        = 12.0;
LID_SCREW_X2        = TD_POD_L - 12.0;
LID_SCREW_Y1        = 6.0;
LID_SCREW_Y2        = TD_POD_W - 6.0;

// Lofting Profile Helper
module console_hull_slice(x, w_base, w_crease, w_roof, z_crease, z_roof, r_fillet=3.0) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=1.0, center=true) {
        hull() {
            // Lower base corners
            translate([0, -w_base/2.0 + r_fillet]) circle(r=r_fillet, $fn=16);
            translate([0,  w_base/2.0 - r_fillet]) circle(r=r_fillet, $fn=16);
            // Lateral Bügelfalte character crease points
            translate([z_crease, -w_crease/2.0 + 1.0]) circle(r=1.0, $fn=12);
            translate([z_crease,  w_crease/2.0 - 1.0]) circle(r=1.0, $fn=12);
            // Upper roof corners (Tumblehome)
            translate([z_roof - r_fillet, -w_roof/2.0 + r_fillet]) circle(r=r_fillet, $fn=16);
            translate([z_roof - r_fillet,  w_roof/2.0 - r_fillet]) circle(r=r_fillet, $fn=16);
        }
    }
}

// Full 3D Automotive Lofted Console Body
module console_full_lofted_hull() {
    hull() {
        // 1. Front Nose Tip (Tapered leading wedge under rider seat)
        console_hull_slice(-CONSOLE_NOSE_L, 36.0, 42.0, 32.0, 14.0, 24.0, 2.0);
        // 2. Front Ramp Transition
        console_hull_slice(-12.0, 56.0, 68.0, 54.0, 18.0, 34.0, 3.0);
        // 3. Pod Front Bulkhead (Waist start)
        console_hull_slice(10.0, 72.0, CONSOLE_MAX_W, 70.0, CONSOLE_CREASE_Z, CONSOLE_TOTAL_H, 3.5);
    }
    hull() {
        // 3. Pod Front Bulkhead
        console_hull_slice(10.0, 72.0, CONSOLE_MAX_W, 70.0, CONSOLE_CREASE_Z, CONSOLE_TOTAL_H, 3.5);
        // 4. Pod Midsection (Deepest waist crease)
        console_hull_slice(TD_POD_L/2.0, 74.0, CONSOLE_MAX_W + 2.0, 72.0, CONSOLE_CREASE_Z, CONSOLE_TOTAL_H, 3.5);
        // 5. Pod Rear Bulkhead
        console_hull_slice(TD_POD_L - 10.0, 72.0, CONSOLE_MAX_W, 70.0, CONSOLE_CREASE_Z, CONSOLE_TOTAL_H, 3.5);
    }
    hull() {
        // 5. Pod Rear Bulkhead
        console_hull_slice(TD_POD_L - 10.0, 72.0, CONSOLE_MAX_W, 70.0, CONSOLE_CREASE_Z, CONSOLE_TOTAL_H, 3.5);
        // 6. Rear Tail Transition
        console_hull_slice(TD_POD_L + 12.0, 58.0, 68.0, 52.0, 18.0, 32.0, 3.0);
        // 7. Rear Tail Tip (Aero diffusor trailing edge)
        console_hull_slice(TD_POD_L + CONSOLE_TAIL_L, 40.0, 46.0, 34.0, 12.0, 20.0, 2.0);
    }
}

// Longitudinal Style Grooves on Roof
module console_roof_style_grooves() {
    for (side = [-1, 1]) {
        translate([0, side * 16.0, CONSOLE_TOTAL_H]) {
            hull() {
                translate([-CONSOLE_NOSE_L + 14.0, 0, 0]) sphere(r=1.0, $fn=12);
                translate([TD_POD_L + CONSOLE_TAIL_L - 12.0, 0, 0]) sphere(r=1.0, $fn=12);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE 1: ADVENTURE TRANSITION DOCK - BASE CRADLE (UNTERTEIL)
// -----------------------------------------------------------------------------
module adventure_transition_dock_base(side = "right") {
    // Inboard direction: towards bike centerline (right side -> -Y; left side -> +Y)
    y_dir = (side == "right") ? -1.0 : 1.0;

    difference() {
        union() {
            // Cut lofted body below the Bügelfalte crease line (Z <= CONSOLE_CREASE_Z)
            intersection() {
                console_full_lofted_hull();
                translate([-CONSOLE_NOSE_L - 5.0, -CONSOLE_MAX_W, -TUBE_DROP_Z - 10.0])
                    cube([CONSOLE_TOTAL_L + 15.0, 2 * CONSOLE_MAX_W, CONSOLE_CREASE_Z + TUBE_DROP_Z + 10.0]);
            }

            // Inboard Tongue to Under-Seat Cross-Rail
            translate([TD_POD_L/2.0 - TONGUE_WIDTH_X/2.0, 0, 0]) {
                if (y_dir < 0) {
                    translate([0, -CONSOLE_MAX_W/2.0 - TONGUE_EXT_Y + 4.0, 0])
                        cube([TONGUE_WIDTH_X, TONGUE_EXT_Y + 4.0, TONGUE_THICK]);
                } else {
                    translate([0, CONSOLE_MAX_W/2.0 - 8.0, 0])
                        cube([TONGUE_WIDTH_X, TONGUE_EXT_Y + 8.0, TONGUE_THICK]);
                }
            }

            // 4x Internal Lid Screw Bosses (M3 Brass Heat-Set or Nut-Pocket Seats)
            for (bx = [LID_SCREW_X1, LID_SCREW_X2]) {
                for (by = [-LID_SCREW_Y2/2.0 + 2.0, LID_SCREW_Y2/2.0 - 2.0]) {
                    translate([bx, by, 0])
                        cylinder(r=4.2, h=CONSOLE_CREASE_Z, $fn=20);
                }
            }
        }

        // --- SUBTRACTIONS ---

        // A1. Pod Main Reception Cavity (136 x 71 mm, sits on floor at Z = TD_FLOOR)
        translate([0, -TD_POD_W/2.0, TD_FLOOR])
            cube([TD_POD_L, TD_POD_W, CONSOLE_CREASE_Z + 10.0]);

        // A2. Front Nose M8 Connector & Wiring Chamber / Service-Bucht
        // Provides 24 mm longitudinal clearance for M8 overmolded plug, strain relief, and 90° lateral cable bend
        translate([-24.0, -25.0, TD_FLOOR])
            cube([26.0, 50.0, CONSOLE_CREASE_Z + 10.0]);

        // B. Subframe Tube Saddle (Concave Hohlkehle on bottom, fitting Ø 28 mm tube)
        translate([-CONSOLE_NOSE_L - 5.0, 0, -TUBE_DROP_Z])
            rotate([0, 90, 0])
                cylinder(r=TUBE_R, h=CONSOLE_TOTAL_L + 15.0, $fn=36);

        // C. Fastening Holes on Inboard Tongue (2x M4 to Under-Seat Rail)
        translate([TD_POD_L/2.0, y_dir * (CONSOLE_MAX_W/2.0 + TONGUE_EXT_Y/2.0), -1.0]) {
            for (dx = [-TONGUE_SCREW_DIST/2.0, TONGUE_SCREW_DIST/2.0]) {
                translate([dx, 0, 0]) {
                    cylinder(r=2.2, h=TONGUE_THICK + 3.0, $fn=16); // M4 through-bore
                    translate([0, 0, TONGUE_THICK - 1.5])
                        cylinder(r=4.5, h=3.0, $fn=16); // Counterbore
                }
            }
        }

        // D1. Direct Inboard Under-Seat Cable Ingress Port with Rounded 90° Bending Radius (R=10mm)
        // Passes through the inboard wall directly under the rider seat cushion into the dry subframe / battery tray
        translate([-12.0, 0, TD_FLOOR]) {
            hull() {
                cylinder(r=5.5, h=16.0, $fn=24);
                translate([0, y_dir * (CONSOLE_MAX_W/2.0 + 10.0), 0])
                    cylinder(r=5.5, h=16.0, $fn=24);
            }
        }

        // D1_Fillet: Smooth 90° lead-in chamfer to eliminate any sharp bending edge
        translate([-16.0, y_dir * (CONSOLE_MAX_W/2.0 - 6.0), TD_FLOOR + 5.0])
            rotate([0, 90, 0])
                cylinder(r=6.0, h=12.0, center=true, $fn=24);

        // D2. Inboard M8 PUR Cable 90° Conduit (Passes through tongue under seat to cross-rail)
        translate([12.0, 0, TD_FLOOR]) {
            hull() {
                cylinder(r=4.8, h=15.0, $fn=20);
                translate([0, y_dir * (CONSOLE_MAX_W/2.0 + TONGUE_EXT_Y + 2.0), 0])
                    cylinder(r=4.8, h=15.0, $fn=20);
            }
        }

        // D3. Integrated Ribbed Strain Relief Clamp Jaw & Dual Zip-Tie Slots (Feedback Zeile 16)
        // Two cross-slots for 2.8x1.6 mm cable ties anchoring the M8 PUR jacket firmly against vibration
        for (zt_x = [-18.0, -8.0]) {
            translate([zt_x, y_dir * (CONSOLE_MAX_W/2.0 - 8.0), TD_FLOOR - 1.0])
                cube([2.8, 12.0, 10.0], center=true);
        }

        // E. 4x M3 Screw Holes in Bosses (Ø 3.2 mm for heat-set or tapping)
        for (bx = [LID_SCREW_X1, LID_SCREW_X2]) {
            for (by = [-LID_SCREW_Y2/2.0 + 2.0, LID_SCREW_Y2/2.0 - 2.0]) {
                translate([bx, by, CONSOLE_CREASE_Z - 12.0])
                    cylinder(r=1.8, h=15.0, $fn=16);
            }
        }

        // F. Concealed EPDM Under-Pod Strap Channels (Optional backup securing)
        for (sx = [30.0, TD_POD_L - 30.0]) {
            translate([sx - 3.0, -CONSOLE_MAX_W, TD_FLOOR - 2.0])
                cube([6.0, 2 * CONSOLE_MAX_W, 2.5]);
        }
    }
}

// -----------------------------------------------------------------------------
// MODULE 2: ADVENTURE TRANSITION DOCK - DESIGN DECKEL / COWL (OBERTEIL)
// -----------------------------------------------------------------------------
module adventure_transition_dock_lid(variant = "open_intercom") {
    difference() {
        union() {
            // Cut lofted body above the Bügelfalte crease line (Z >= CONSOLE_CREASE_Z)
            intersection() {
                console_full_lofted_hull();
                translate([-CONSOLE_NOSE_L - 5.0, -CONSOLE_MAX_W, CONSOLE_CREASE_Z])
                    cube([CONSOLE_TOTAL_L + 15.0, 2 * CONSOLE_MAX_W, CONSOLE_TOTAL_H - CONSOLE_CREASE_Z + 5.0]);
            }
        }

        // --- SUBTRACTIONS ---

        // A. Style Grooves along roof
        console_roof_style_grooves();

        // B. Cartridge / Intercom Cutout Window (Variant Dependent)
        if (variant == "open_intercom") {
            // Sculpted bezel framing the Cardo Packtalk Edge / Sena unit flush like OEM
            translate([18.0, 0, CONSOLE_CREASE_Z - 1.0]) {
                hull() {
                    translate([0, -26.0, 0]) cylinder(r=5.0, h=CONSOLE_TOTAL_H, $fn=20);
                    translate([92.0, -26.0, 0]) cylinder(r=5.0, h=CONSOLE_TOTAL_H, $fn=20);
                    translate([0,  26.0, 0]) cylinder(r=5.0, h=CONSOLE_TOTAL_H, $fn=20);
                    translate([92.0,  26.0, 0]) cylinder(r=5.0, h=CONSOLE_TOTAL_H, $fn=20);
                }
            }
        }

        // C. 4x M3 Fastening Screw Counterbores
        for (bx = [LID_SCREW_X1, LID_SCREW_X2]) {
            for (by = [-LID_SCREW_Y2/2.0 + 2.0, LID_SCREW_Y2/2.0 - 2.0]) {
                translate([bx, by, CONSOLE_CREASE_Z - 2.0]) {
                    cylinder(r=1.7, h=25.0, $fn=16); // M3 through
                    translate([0, 0, CONSOLE_TOTAL_H - CONSOLE_CREASE_Z - 3.5])
                        cylinder(r=3.4, h=6.0, $fn=20); // M3 Torx-TR head counterbore
                }
            }
        }

        // D. Underside Nose Wiring Pocket (Extra headroom for cable bend)
        translate([-22.0, -22.0, CONSOLE_CREASE_Z - 1.0])
            cube([22.0, 44.0, 8.0]);
    }
}

// -----------------------------------------------------------------------------
// MASTER MODULE: ADVENTURE TRANSITION DOCK ASSEMBLY & STL RENDERER
// -----------------------------------------------------------------------------
module adventure_transition_dock(part = "assembly", side = "right", lid_variant = "open_intercom") {
    if (part == "base") {
        adventure_transition_dock_base(side = side);
    } else if (part == "lid") {
        adventure_transition_dock_lid(variant = lid_variant);
    } else {
        // Combined Assembly View with contrasting two-tone finishes
        color("#1c222b", 0.96)
            adventure_transition_dock_base(side = side);
        color("#2b3442", 0.98)
            adventure_transition_dock_lid(variant = lid_variant);
    }
}

// Standalone render
adventure_transition_dock(part = "assembly", side = "right", lid_variant = "open_intercom");
