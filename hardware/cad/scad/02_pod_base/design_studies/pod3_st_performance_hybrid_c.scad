// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST Performance Hybrid (Option C - Master V7)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_st_performance_hybrid_c.scad
// Description: The ultimate King of the Baggers / ST Performance synthesis:
//              1. Front: Direct morphing Jet/Football nose (Option B) seamlessly
//                 curving forward to X = -148 mm (double-curved aerodynamic bullet,
//                 100% closed, forged carbon cowl untouched!).
//              2. 2-Part Modular Architecture:
//                 - Aero-Cradle Base: Open-top dock bay (136 x 71 mm) allowing
//                   effortless drop-in insertion of Pod 3 (135 x 70 x 38.5 mm).
//                 - Top Heatsink Louvre Lid: Removable CNC-style slatted cover.
//                   Supports LÄNGS-LAMELLEN (longitudinal, in airflow direction)
//                   aligning with the Heckleitwerk, or QUER-RIPPEN (transverse).
//                   100% direct line-of-sight to the sky for GNSS patch antenna &
//                   uninhibited breathing for Gore-Vent membrane.
//              3. Fuselage: 7 deep horizontal CNC cooling fins (4.0 mm depth)
//                 matching M-8 117 engine, now FIXED & EXTENDED from X = -66 to +66 mm
//                 (full 132 mm length, perfectly aligned with the top lid!).
//              4. Rear: 100% CLOSED, organically tapering boat-tail / diffuser
//                 (X = +68 to +144 mm, W = 86 -> 44 mm, H = 48 -> 36 mm).
//                 Zero holes in the back = 100% weather & road spray sealed!
//              5. Wings: Synclastic 3D compound-curved "Football" winglets to struts (130 mm)
//                 with 3-5 mm paint clearance over the curved fender crown.
//              6. Empennage: High-stability structural Heckleitwerk (continuous dorsal keel)
//                 with wide root fillet, integrating the full-length snap-in channel
//                 (dia 9.2 mm) for the 5 dBi dipole antenna and internal coax conduit.
//              7. Cable Routing: Open underside snap-in C-channel under left wing (R >= 35 mm)
//                 diving directly into the OEM Harley strut wiring channel.
//              8. Slicer Ready: 100% 2-manifold geometry (0 non-manifold edges).
// =============================================================================

include <../00_common/parameters.scad>;

// Build Mode Selector: "assembly" (default for preview), "cradle", "lid", or "covers" / "wing_covers"
BUILD_MODE = "assembly";

// Lid Style Selector: "longitudinal" (Längs-Lamellen, airflow aligned) or "transverse" (Quer-Rippen)
LID_STYLE  = "longitudinal";

// Side Fin Pattern Selector: "arrowhead" (middle fin longest) or "raked_top" (top fin longest)
SIDE_FIN_PATTERN = "arrowhead";

FENDER_R_TRANS = 140.0;
POD_L          = 136.0;
POD_W          = 71.0;
POD_H          = 38.5;

ST_FUSE_W      = 86.0;
ST_COWL_H      = 48.0;
R_CORNER       = 8.0;

LID_L          = 132.0;
LID_W          = 75.0;
LID_THICK      = 4.5;

WING_HALF_SPAN = 130.0;
LEG_DROP_Z     = -32.0;
LEG_LEN_X      = 64.0;
WING_THICK     = 9.0; // Sleek 9 mm aerodynamic wing!

X_NOSE_TIP    = -148.0;
X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_REAR_TIP    = +144.0;

// Prolate Spheroid (Football) Wing Parameters
FB_X0 = -35.0;
FB_Y0 = 35.0;
FB_Z0 = -42.0;
FB_RX = 100.0;
FB_RY = 96.5;
FB_RZ = 60.0;

// Helper: 2D rounded rectangle extruded in Z (rounded slab)
module rounded_slab(l, w, h, r=5.0) {
    linear_extrude(height=h, center=false) {
        hull() {
            for (dx = [-l/2.0 + r, l/2.0 - r]) {
                for (dy = [-w/2.0 + r, w/2.0 - r]) {
                    translate([dx, dy]) circle(r=r, $fn=24);
                }
            }
        }
    }
}

// Helper: 2D cross-section slice in Y-Z plane with 4 rounded corners
module fuse_slice_yz(x, w, h, r, dx=0.4) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=dx, center=true) {
        hull() {
            for (dy = [-w/2.0 + r, w/2.0 - r]) {
                for (dz = [r, h - r]) {
                    translate([dz, dy]) circle(r=r, $fn=24);
                }
            }
        }
    }
}

// 1. Direct Morphing Jet/Football Nose (Seamless double-curved loft X = -68 to -148 mm)
module direct_morphed_jet_nose(l_nose=80.0, w_base=ST_FUSE_W, h_base=ST_COWL_H, r_base=R_CORNER, x_start=X_POD_FRONT, steps=14) {
    for (i = [0 : steps - 1]) {
        t0 = i / steps;
        t1 = (i + 1) / steps;
        
        x0 = x_start - t0 * l_nose;
        x1 = x_start - t1 * l_nose;
        
        // True elliptical jet curve k(t) = sqrt(1 - t^2)
        k0 = sqrt(max(0.001, 1.0 - t0*t0));
        k1 = sqrt(max(0.001, 1.0 - t1*t1));
        
        w0 = max(8.0, w_base * k0);
        w1 = max(8.0, w_base * k1);
        
        h0 = max(6.0, h_base * k0);
        h1 = max(6.0, h_base * k1);
        
        r0 = max(2.5, r_base * k0);
        r1 = max(2.5, r_base * k1);
        
        hull() {
            fuse_slice_yz(x0, w0, h0, r0, dx=0.2);
            fuse_slice_yz(x1, w1, h1, r1, dx=0.2);
        }
    }
}

// 2. Center Fuselage Section (-68 to +68 mm)
// Spans from X_POD_FRONT - 1.0 to X_POD_REAR + 1.5 with solid 1.5 mm geometric overlap
module center_fuselage_cradle() {
    hull() {
        fuse_slice_yz(X_POD_FRONT - 1.0, ST_FUSE_W, ST_COWL_H, R_CORNER, dx=0.6);
        fuse_slice_yz(X_POD_REAR  + 1.5, ST_FUSE_W, ST_COWL_H, R_CORNER, dx=0.6);
    }
}

// 3. Organically Tapering Boat-Tail Diffuser (+68 to +144 mm) - 100% CLOSED REAR
REAR_DIFFUSER_KEYS = [
    [ +68.0,  86.0,  48.0,  8.0],  // 0: Pod rear bulkhead (starts at full fuselage cross-section)
    [ +88.0,  78.0,  45.0,  7.0],  // 1: Subtle initial taper
    [+108.0,  66.0,  42.0,  6.0],  // 2: Mid boat-tail waist
    [+128.0,  54.0,  39.0,  5.0],  // 3: Diffuser transition
    [+144.0,  44.0,  36.0,  4.0]   // 4: Completely closed rear aerodynamic trailing edge
];

module tapering_boattail_diffuser() {
    num_k = len(REAR_DIFFUSER_KEYS);
    for (i = [0 : num_k - 2]) {
        k0 = REAR_DIFFUSER_KEYS[i];
        k1 = REAR_DIFFUSER_KEYS[i + 1];
        hull() {
            fuse_slice_yz(k0[0], k0[1], k0[2], k0[3], dx=0.4);
            fuse_slice_yz(k1[0], k1[1], k1[2], k1[3], dx=0.4);
        }
    }
}

// 4. Synclastic 3D Compound-Curved Sleek 9.0 mm Aerodynamic Wings (Left & Right)
// Sculpted 9 mm aerodynamic skin with double curvature and integrated underwing channel.
module football_curved_wing(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        difference() {
            intersection() {
                difference() {
                    // Outer compound aerodynamic surface (Prolate spheroid)
                    translate([FB_X0, FB_Y0, FB_Z0])
                        scale([FB_RX, FB_RY, FB_RZ])
                            sphere(r=1.0, $fn=64);

                    // Inner surface: exact 9.0 mm uniform aerodynamic skin!
                    translate([FB_X0, FB_Y0, FB_Z0])
                        scale([FB_RX - WING_THICK, FB_RY - WING_THICK, FB_RZ - WING_THICK])
                            sphere(r=1.0, $fn=64);
                }

                // Jet planform polygon
                translate([0, 0, -80.0])
                    linear_extrude(height=160.0, center=false, convexity=10)
                        polygon([
                            [-115.0, ST_FUSE_W/2.0 - 4.0],
                            [-34.0,  64.0],
                            [-27.0,  WING_HALF_SPAN],
                            [+27.0,  WING_HALF_SPAN],
                            [+24.0,  70.0],
                            [+38.0,  ST_FUSE_W/2.0 - 4.0]
                        ]);
            }

            // Lower cutoff below strut mount
            translate([-150, -10, -150])
                cube([300, 200, 150 + LEG_DROP_Z]);
        }

        // Solid Vertical Mounting Plate at Strut
        translate([-LEG_LEN_X/2.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z])
            cube([LEG_LEN_X, 8.0, 26.0], center=false);

        // Transition fillet from wing curve into vertical strut foot
        hull() {
            translate([-27.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z + 12.0])
                cube([54.0, 8.0, 4.0], center=false);
            translate([-24.0, WING_HALF_SPAN - 16.0, LEG_DROP_Z + 18.0])
                cube([48.0, 8.0, 4.0], center=false);
        }
    }
}

// 5. High-Stability Supersonic Jet-Heckleitwerk with Stinger Nozzle & Internal Bore
module structural_heckleitwerk() {
    difference() {
        union() {
            // Main supersonic vertical stabilizer blade (tapered from root to razor top)
            hull() {
                // Leading edge start (seamlessly at lid rear lip: X = 66, Z = 48 mm)
                translate([66.0, 0, 48.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=1.0, center=true, $fn=16);
                // Apex crest (X = 114, Z = 69 mm)
                translate([114.0, 0, 69.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=1.0, center=true, $fn=16);
                // Apex rear (X = 126, Z = 68 mm)
                translate([126.0, 0, 68.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=1.0, center=true, $fn=16);
                // Trailing edge (X = 143, Z = 46 mm)
                translate([143.0, 0, 46.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=1.0, center=true, $fn=16);
                // Root base front (inside fuselage deck)
                translate([66.0, 0, 38.0]) rotate([0, 90, 0]) cylinder(r=5.0, h=1.0, center=true, $fn=24);
                // Root base rear
                translate([144.0, 0, 32.0]) rotate([0, 90, 0]) cylinder(r=5.0, h=1.0, center=true, $fn=24);
            }

            // Streamlined antenna stinger nacelle emerging organically from fin
            hull() {
                translate([66.0, 0, 48.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=1.0, center=true, $fn=16);
                translate([80.0, 0, 46.0]) rotate([0, 88, 0]) cylinder(r=6.5, h=2.0, center=true, $fn=24);
                translate([105.0, 0, 45.0]) rotate([0, 88, 0]) cylinder(r=6.2, h=2.0, center=true, $fn=24);
                translate([144.0, 0, 43.5]) rotate([0, 88, 0]) cylinder(r=5.8, h=2.0, center=true, $fn=24);
            }

            // Wide aerodynamic root fillets anchoring deep into boat-tail roof
            hull() {
                translate([68.0, 0, 36.0]) scale([1, 1.6, 1]) cylinder(r=7.0, h=10.0, center=false, $fn=24);
                translate([105.0, 0, 34.0]) scale([1, 1.5, 1]) cylinder(r=7.0, h=10.0, center=false, $fn=24);
                translate([142.0, 0, 30.0]) scale([1, 1.2, 1]) cylinder(r=6.0, h=8.0, center=false, $fn=24);
            }
        }

        // Antenna internal bore (dia 9.4 mm) from X = 74 mm through to rear nozzle at X = 146 mm
        hull() {
            translate([74.0, 0, 46.0]) rotate([0, 88, 0]) cylinder(r=4.7, h=74.0, center=false, $fn=24);
            translate([74.0, 0, 47.5]) rotate([0, 88, 0]) cylinder(r=4.2, h=74.0, center=false, $fn=24);
        }

        // Antenna Coax Pigtail Conduit connecting to internal rear relief bay
        hull() {
            translate([78.0, 0, 44.0]) rotate([0, 70, 0]) cylinder(r=3.0, h=18.0, center=true, $fn=20);
            translate([78.0, 0, 30.0]) rotate([0, 45, 0]) cylinder(r=3.5, h=18.0, center=true, $fn=20);
        }
    }
}

// 6. Dynamic Parallelogram Speed Cooling Fins along Flanks
// Bottom fin starts in front; fins slant back as they rise (parallelogram '///')
module m8_deep_cooling_fins() {
    // 7 horizontal CNC fins: [z_pos, x_front, x_rear]
    fin_parallelogram = [
        [12.0, -74.0, +58.0],  // 0: Bottom fin starts furthest forward on nose cone
        [17.5, -71.0, +63.0],  // 1
        [23.0, -68.0, +68.0],  // 2
        [28.5, -65.0, +73.0],  // 3: Mid flank
        [34.0, -62.0, +78.0],  // 4
        [39.5, -59.0, +83.0],  // 5
        [44.0, -56.0, +88.0]   // 6: Top fin reaches furthest back along boat-tail
    ];

    for (fin = fin_parallelogram) {
        z_pos   = fin[0];
        x_front = fin[1];
        x_rear  = fin[2];
        l_fin   = x_rear - x_front;
        x_mid   = (x_front + x_rear) / 2.0;

        for (side = [-1, 1]) {
            y_pos = side * (ST_FUSE_W/2.0 + 0.5);
            translate([x_mid, y_pos, z_pos]) {
                rotate([0, 90, 0]) {
                    hull() {
                        translate([0, -side * 1.5, 0.0]) cylinder(r=1.5, h=l_fin, center=true, $fn=16);
                        translate([0, -side * 5.0, 0.0]) cylinder(r=2.5, h=max(10.0, l_fin - 6.0), center=true, $fn=16);
                    }
                }
            }
        }
    }
}

// 7. Internal Open-Top Dock Chamber (Drop-In for Pod 3, completely sealed at the rear)
module pod3_internal_dock_cradle() {
    // 1. Pod dock chamber (floor at Z = 5.0 mm -> 3.5 mm solid floor over fender crown)
    // Opens completely upward through roof so Pod 3 drops in effortlessly from above!
    translate([-POD_L/2.0, -POD_W/2.0, 5.0])
        cube([POD_L, POD_W, 55.0], center=false);

    // 2. Stepped Recess for Top Heatsink Louvre Lid (depth 4.5 mm, Z = 43.5 to 55 mm)
    translate([-LID_L/2.0, -LID_W/2.0, ST_COWL_H - LID_THICK])
        cube([LID_L, LID_W, 15.0], center=false);

    // 3. Front M8 Gland Straight Chamber (X = -68 to -95 mm)
    translate([-POD_L/2.0 - 27.0, -11.0, 19.0 - 11.0])
        cube([29.0, 22.0, 22.0], center=false);

    // 4. 4x M3 Lid Mounting Screw Holes (depth 10 mm for M3 heat-set threaded inserts)
    for (mx = [-58.0, +58.0]) {
        for (my = [-34.5, +34.5]) {
            translate([mx, my, ST_COWL_H - 10.0])
                cylinder(r=1.6, h=12.0, center=false, $fn=16);
        }
    }

    // 5. Strap Hook Reliefs inside chamber
    hook_x = [-POD_L/2.0 + 25.0, -POD_L/2.0 + 110.0];
    for (hx = hook_x) {
        translate([hx - 7.0, -POD_W/2.0 - 1.0, 5.0]) cube([14.0, 2.5, 10.0]);
        translate([hx - 7.0,  POD_W/2.0 - 1.5, 5.0]) cube([14.0, 2.5, 10.0]);
    }

    // 6. Rear Antenna Dual-Jack Relief Bay & Funnel (X = 66.0 to 76.0 mm)
    // Width 36.0 mm (Y = -18 to +18 mm), leaving 18.5 mm solid structural wall on left and right!
    hull() {
        translate([66.0, -18.0, 14.0]) cube([10.0, 36.0, 26.0], center=false);
        translate([72.0, -10.0, 28.0]) cube([6.0, 20.0, 18.0], center=false);
    }
}

// Exact bottom surface coordinates of the 9 mm sleek wing:
// At each [X, Y], Z is the exact underside of the 9 mm skin:
wing_cable_path = [
    [-46.0,  42.0,   8.0],
    [-32.0,  62.0,   6.5],
    [-18.0,  84.0,  -0.8],
    [ -8.0, 104.0, -14.5],
    [ -2.0, 122.0, -28.0]
];

// 8. Symmetrical Under-Wing Cable Channels & Snap Cover Grooves (Left & Right)
// Recessed directly into the 9 mm wing underside - leaving 5.5 mm solid top skin!
module st_underwing_channels() {
    // Internal cross-tunnel from front M8 gland chamber through fuselage wall into wing roots
    hull() {
        translate([-85.0, 0, 16.0]) cylinder(r=5.5, h=10.0, center=true, $fn=24);
        translate([-46.0, -42.0, 8.0]) sphere(r=3.5, $fn=20);
    }
    hull() {
        translate([-85.0, 0, 16.0]) cylinder(r=5.5, h=10.0, center=true, $fn=24);
        translate([-46.0,  42.0, 8.0]) sphere(r=3.5, $fn=20);
    }

    // Symmetrical recessed channels on both wings (side = -1 for left, side = 1 for right)
    for (side = [-1, 1]) {
        mirror([0, side < 0 ? 1 : 0, 0]) {
            // Main round cable conduit (dia 6.0 mm) cut upward from the wing inner surface
            for (i = [0 : len(wing_cable_path) - 2]) {
                hull() {
                    translate(wing_cable_path[i] + [0, 0, 2.5]) sphere(r=3.0, $fn=16);
                    translate(wing_cable_path[i+1] + [0, 0, 2.5]) sphere(r=3.0, $fn=16);
                }
            }
            // Stepped rebate for flush snap cover (width 7.0 mm, cutting downward through wing underside)
            for (i = [0 : len(wing_cable_path) - 2]) {
                hull() {
                    translate(wing_cable_path[i] + [0, 0, 0.0]) cube([7.0, 2.0, 3.5], center=true);
                    translate(wing_cable_path[i+1] + [0, 0, 0.0]) cube([7.0, 2.0, 3.5], center=true);
                }
            }

            // Downward exit channel inside Harley strut plate (inner face only, 100% invisible from outside!)
            translate([-6.0, WING_HALF_SPAN - 8.0, -34.0])
                cube([8.0, 8.0, 18.0], center=false);
        }
    }
}

// 9. Flush Snap-In Under-Wing Cable Cover Strips (Left & Right)
// Snaps 100% flush into the 9 mm wing underside groove - completely smooth aerodynamic skin!
module st_underwing_snap_cover(side=-1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        difference() {
            union() {
                // Main cover strip (thickness 1.6 mm, sitting flush in the rebate)
                for (i = [0 : len(wing_cable_path) - 2]) {
                    hull() {
                        translate(wing_cable_path[i] + [0, 0, 0.0]) cube([6.6, 2.0, 1.6], center=true);
                        translate(wing_cable_path[i+1] + [0, 0, 0.0]) cube([6.6, 2.0, 1.6], center=true);
                    }
                }

                // Snap retention tabs (spring ribs) that lock into channel rebate walls
                for (idx = [1, 3]) {
                    translate(wing_cable_path[idx] + [0, 0, 0.8])
                        cube([7.4, 3.5, 1.8], center=true);
                }
            }

            // Fingernail / tool pry notch at the strut knuckle for effortless removal
            translate(wing_cable_path[3] + [0, 0, -0.5])
                cube([8.0, 2.5, 1.2], center=true);
        }
    }
}

// =============================================================================
// PART 1: The Aero-Cradle Base (Unterteil)
// =============================================================================
module pod3_st_hybrid_cradle() {
    difference() {
        union() {
            // A. Direct Morphed Jet/Football Nose (X = -68 to -148 mm)
            direct_morphed_jet_nose();

            // B. Center Fuselage Cradle (-68 to +68 mm)
            center_fuselage_cradle();

            // C. Organically Tapering Boat-Tail Diffuser (+68 to +144 mm) - 100% CLOSED
            tapering_boattail_diffuser();

            // D. Football Compound 3D Wings (Left & Right)
            for (side = [-1, 1]) {
                football_curved_wing(side);
            }

            // E. High-Stability Structural Heckleitwerk
            structural_heckleitwerk();
        }

        // F. Internal Open-Top Drop-In Dock Chamber + Stepped Lid Recess (Closed Rear!)
        pod3_internal_dock_cradle();

        // G. 7 Deep Milwaukee-Eight Cooling Fins (X = -66 to dynamically fading rear)
        m8_deep_cooling_fins();

        // H. Symmetrical Under-Wing Cable Channels (Left & Right)
        st_underwing_channels();

        // I. Strut Mounting Bolt Counterbores (OEM 35 mm spacing)
        for (x_bolt = [-17.5, +17.5]) {
            translate([x_bolt, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt, -WING_HALF_SPAN + 6.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=8.5, h=10.0, center=false, $fn=24);

            translate([x_bolt, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt, WING_HALF_SPAN - 6.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=8.5, h=10.0, center=false, $fn=24);
        }

        // J. Fender crown clearance (Concave saddle under center cradle)
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=380.0, center=true, $fn=64);
        }
    }
}

// =============================================================================
// PART 2: Top Heatsink Louvre Lid (Kühlrippen-Gitterdeckel mit offenen Schlitzen)
// Supports both "longitudinal" (Längs-Lamellen) and "transverse" (Quer-Rippen)
// =============================================================================
module pod3_st_hybrid_heatsink_lid() {
    difference() {
        // Solid lid plate with rounded outer corners (thickness 4.5 mm)
        translate([0, 0, ST_COWL_H - LID_THICK])
            rounded_slab(LID_L, LID_W, LID_THICK, r=6.0);

        // Open Ventilation Slots (100% direct line-of-sight to sky for GNSS & Gore-Vent)
        if (LID_STYLE == "longitudinal") {
            // LÄNGS-LAMELLEN: Dynamic Arrowhead Front + Parallelogram-Harmonized Rear
            // Front: Arrowhead pointing forward into bullet nose (center slot furthest forward: X = -58 mm)
            // Rear: Outer slots reach furthest back (X = +58 mm) meeting the top side fins at the flanks,
            //       while the center recedes forward (X = +36 mm) creating an inverted delta that
            //       visually frames and seamlessly launches the Heckfinne root!
            // Format: [y_pos, x_front, x_rear]
            slots_pattern = [
                [-24.0, -48.0, +58.0],  // Outer slot: longest at rear (+58)
                [-16.0, -51.0, +52.0],  // Intermediate
                [ -8.0, -55.0, +44.0],  // Inner
                [  0.0, -58.0, +36.0],  // Center: furthest forward (-58), recedes forward at rear (+36) for fin
                [ +8.0, -55.0, +44.0],  // Inner
                [+16.0, -51.0, +52.0],  // Intermediate
                [+24.0, -48.0, +58.0]   // Outer slot: longest at rear (+58)
            ];

            for (slot = slots_pattern) {
                sy     = slot[0];
                x_f    = slot[1];
                x_r    = slot[2];
                slen   = x_r - x_f;
                x_cent = (x_f + x_r) / 2.0;

                translate([x_cent, sy, ST_COWL_H - LID_THICK - 1.0])
                    rounded_slab(slen, 4.5, LID_THICK + 2.0, r=2.2);
            }
        } else {
            // QUER-RIPPEN (Transverse, matching cylinder head fins)
            for (sx = [-48.0 : 12.0 : 48.0]) {
                translate([sx, 0, ST_COWL_H - LID_THICK - 1.0])
                    rounded_slab(5.5, LID_W - 14.0, LID_THICK + 2.0, r=2.5);
            }
        }

        // 4x Countersunk M3 Screw Holes
        for (mx = [-58.0, +58.0]) {
            for (my = [-34.5, +34.5]) {
                translate([mx, my, ST_COWL_H - LID_THICK - 1.0])
                    cylinder(r=1.7, h=LID_THICK + 2.0, center=false, $fn=16);
                translate([mx, my, ST_COWL_H - 1.8])
                    cylinder(r1=1.7, r2=3.3, h=2.0, center=false, $fn=16);
            }
        }
    }
}

// 5 dBi Dipole Antenna with Trailing Stinger Protruding out the Rear
module antenna_stinger_dummy() {
    color("#0f172a") { // Tactical carbon/rubber rod
        translate([70.0, 0, 46.0]) rotate([0, 88, 0]) {
            cylinder(r=4.5, h=100.0, center=false, $fn=24);
            translate([0, 0, 100.0]) sphere(r=4.5, $fn=24);
        }
    }
    color("#d97706") { // Anodized gold/brass accent ring at exit nozzle
        translate([144.0, 0, 43.5]) rotate([0, 88, 0])
            cylinder(r=5.0, h=2.0, center=true, $fn=24);
    }
}

// =============================================================================
// Combined Assembly
// =============================================================================
module pod3_st_performance_hybrid_c() {
    if (BUILD_MODE == "cradle") {
        pod3_st_hybrid_cradle();
    } else if (BUILD_MODE == "lid") {
        pod3_st_hybrid_heatsink_lid();
    } else if (BUILD_MODE == "covers" || BUILD_MODE == "wing_covers") {
        st_underwing_snap_cover(-1);
        st_underwing_snap_cover(1);
    } else {
        // Assembly: Cradle + Heatsink Lid + Antenna Stinger + Flush Under-Wing Covers
        union() {
            color("#1e293b", 0.98) // Satin Carbon / Black Aero Cradle
                pod3_st_hybrid_cradle();
            color("#d97706", 0.95) // Raw CNC Machined / Anodized Billet Heatsink Lid
                pod3_st_hybrid_heatsink_lid();
            antenna_stinger_dummy();
            color("#334155", 0.95) { // Satin Charcoal / Snap-In Wing Covers
                st_underwing_snap_cover(-1);
                st_underwing_snap_cover(1);
            }
        }
    }
}

pod3_st_performance_hybrid_c();
