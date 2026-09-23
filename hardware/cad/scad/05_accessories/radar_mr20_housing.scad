// =============================================================================
// OpenMotorBridge - Radar 2.0 Sub-MCU & Wheeltec MR20 Sealed IP67 Housing
// =============================================================================
// File: hardware/cad/scad/05_accessories/radar_mr20_housing.scad
// Description: Fully enclosed, waterproof IP67 symmetrical housing for:
//              1. Wheeltec MR20 77-GHz mmWave radar transceiver (60.5x50.5x8.2 mm).
//                 Placed dead center at X=0, Z=0.
//              2. Front PCBA 08 (115.0x65.0 mm) with central 61.0x51.0 mm cutout,
//                 36x WS2812B-2020 LEDs (multi-column warning wings left & right),
//                 and ESP32-C5 Sub-MCU on the rear wing.
//              3. Full inline cable-adapter module & wire loop accommodated
//                 in generous 112x62x17 mm rear cavity (Feedback Zeile 46 & Radar).
//              4. Dedicated 5.9 GHz ITS-G5 (V2X) Ceramic Patch Antenna Snap Cradle
//                 in the left wing cavity (20x20mm / 25x25mm) with snap-fit tabs
//                 and U.FL coax cable routing (User directive: external high-gain antenna!).
//              5. Binder Serie 707 M5 4-pin IP67 bulkhead connector on center axis X=0.
//              6. Optically clear, RF-transparent Polycarbonate radome window.
//              7. Direct Garmin Quarter-Turn Bayonet male mount on rear wall
//                 (locks into radar_varia_gopro_lock_dock.scad and license plate bracket),
//                 plus symmetrical 40 mm M4 rear insert bosses & lower clevis.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Symmetrical Housing Dimensions (Variante 1: Flügel-Rechteck 115 x 65 mm) ---
RADAR_HOUSING_W     = 121.0; // Outer transverse width in X (mm)
RADAR_HOUSING_H     = 71.0;  // Outer vertical height in Z (mm)
RADAR_HOUSING_D     = 34.0;  // Outer depth in Y (front radome to back wall, mm)
RADAR_WALL_THICK    = 2.8;   // Nominal MJF PA12 wall thickness (mm)
RADAR_CORNER_R      = 5.0;   // Outer corner fillet radius (mm)

// --- Internal Component Envelopes ---
MR20_MODULE_W       = 60.5;  // MR20 transceiver width (mm)
MR20_MODULE_H       = 50.5;  // MR20 transceiver height (mm)
MR20_MODULE_D       = 8.5;   // MR20 core depth (mm)

PCBA08_W            = 115.0; // PCBA 08 outer width (mm)
PCBA08_H            = 65.0;  // PCBA 08 outer height (mm)
PCBA08_THICK        = 1.6;   // PCB thickness (mm)

// Generous rear cavity for MR20 inline cable-adapter module and harness loop
ADAPTER_CAVITY_W    = 112.0; // Full width for cable loop & adapter (mm)
ADAPTER_CAVITY_H    = 62.0;  // Full height (mm)
ADAPTER_CAVITY_D    = 17.0;  // Depth behind radar module (mm)

// --- 5.9 GHz V2X Ceramic Patch Antenna Cradle Dimensions ---
V2X_PATCH_W         = 20.5;  // Pocket width for 20x20mm ceramic patch (mm)
V2X_PATCH_H         = 20.5;  // Pocket height (mm)
V2X_PATCH_THICK     = 4.2;   // Ceramic patch thickness (mm)
V2X_PATCH_25_STEP   = 25.5;  // Outer step for 25x25mm patch antennas (mm)
V2X_CRADLE_WALL     = 1.5;   // Cradle retaining rib thickness (mm)
V2X_CABLE_NOTCH_W   = 3.2;   // Micro-coax U.FL exit slot width (mm)

// --- Radome & Halo Step ---
RADOME_WINDOW_W     = 116.0; // Outer width of transparent radome plate (mm)
RADOME_WINDOW_H     = 66.0;  // Outer height (mm)
RADOME_WINDOW_THICK = 1.6;   // RF-transparent optical PC window thickness (mm)

SEAL_GROOVE_W       = 1.8;   // IP67 elastomeric O-ring cord width (mm)
SEAL_GROOVE_D       = 1.3;   // O-ring compression depth (mm)

// --- Connector & Mounting ---
BINDER_M5_BORE_DIA  = 5.2;   // Binder Serie 707 M5 panel cut-out (mm)
BINDER_M5_FLAT_DIST = 4.75;  // Anti-rotation D-flat distance (mm)
CLEVIS_TONGUE_W     = 6.0;   // Compatible with underfender and GoPro mounts (mm)
CLEVIS_BORE_DIA     = 5.2;   // M5 clamping bolt clearance (mm)
REAR_M4_PITCH       = 40.0;  // Symmetrical spacing between rear brass inserts (mm)

// --- Garmin Quarter-Turn Bayonet Dimensions ---
GARMIN_HUB_DIA      = 25.2;  // Male hub diameter (mm, fits Ø 26.0 mm socket)
GARMIN_HUB_PROT     = 3.2;   // Male hub protrusion from back wall (mm)
GARMIN_WING_DIA     = 32.2;  // Wing tip-to-tip diameter (mm, fits Ø 33.0 mm undercut)
GARMIN_WING_W       = 6.6;   // Wing width (mm, passes 7.0 mm entry slot)
GARMIN_WING_THICK   = 2.4;   // Retention wing flange thickness (mm)
GARMIN_WING_OFFSET  = 0.7;   // Axial gap between back wall and wing bottom (mm)

// Helper: Rounded 2D rectangle in X-Z plane (centered at X=0, Z=0)
module rounded_rect_xz(w, h, r) {
    hull() {
        translate([-w/2 + r, 0, -h/2 + r]) circle(r=r, $fn=32);
        translate([ w/2 - r, 0, -h/2 + r]) circle(r=r, $fn=32);
        translate([-w/2 + r, 0,  h/2 - r]) circle(r=r, $fn=32);
        translate([ w/2 - r, 0,  h/2 - r]) circle(r=r, $fn=32);
    }
}

// Helper: Male Garmin Quarter-Turn Bayonet Mount (Centered at X=0, Z=0, protruding along -Y)
module garmin_male_bayonet() {
    union() {
        // 1. Central Cylindrical Hub (Ø 25.2 mm x 3.2 mm)
        rotate([90, 0, 0])
            cylinder(r=GARMIN_HUB_DIA/2, h=GARMIN_HUB_PROT, center=false, $fn=48);

        // 2. Dual Symmetrical Locking Wings (Vertical insertion orientation, twists 90° into lock)
        translate([0, -GARMIN_WING_OFFSET - GARMIN_WING_THICK, 0]) {
            intersection() {
                // Outer swing cylinder
                rotate([90, 0, 0])
                    cylinder(r=GARMIN_WING_DIA/2, h=GARMIN_WING_THICK, center=false, $fn=48);

                // Vertical wing blade (width = GARMIN_WING_W in X)
                translate([-GARMIN_WING_W/2, 0, -GARMIN_WING_DIA/2])
                    cube([GARMIN_WING_W, GARMIN_WING_THICK, GARMIN_WING_DIA], center=false);
            }
        }

        // 3. Lead-in Chamfers on clockwise rotation corners for smooth engagement
        for (sign_z = [-1, 1]) {
            translate([sign_z * (GARMIN_WING_W/2 - 0.8), -GARMIN_WING_OFFSET - GARMIN_WING_THICK, sign_z * (GARMIN_WING_DIA/2 - 2.5)]) {
                rotate([45, 0, 0])
                    cube([1.6, 1.2, 3.0], center=true);
            }
        }
    }
}

// Helper: 5.9 GHz V2X Ceramic Patch Antenna Snap Cradle (Left Wing Chamber, centered at X = -44.0, Z = 0)
module v2x_patch_antenna_cradle() {
    cradle_outer_w = V2X_PATCH_W + 2 * V2X_CRADLE_WALL;
    cradle_outer_h = V2X_PATCH_H + 2 * V2X_CRADLE_WALL;
    cradle_depth   = V2X_PATCH_THICK + 1.2;

    translate([-44.0, -RADAR_HOUSING_D + RADAR_WALL_THICK, 0]) {
        difference() {
            // Outer cradle body rising from the inside back wall forward along +Y
            translate([-cradle_outer_w/2, 0, -cradle_outer_h/2])
                cube([cradle_outer_w, cradle_depth, cradle_outer_h], center=false);

            // Internal pocket for 20x20mm ceramic patch antenna
            translate([-V2X_PATCH_W/2, -0.1, -V2X_PATCH_H/2])
                cube([V2X_PATCH_W, V2X_PATCH_THICK + 0.1, V2X_PATCH_H], center=false);

            // U.FL micro-coax cable exit notch at top
            translate([-V2X_CABLE_NOTCH_W/2, -0.1, V2X_PATCH_H/2 - 1.0])
                cube([V2X_CABLE_NOTCH_W, cradle_depth + 1.0, cradle_outer_h/2 + 2.0], center=false);
        }

        // Dual flexible snap-retention tabs at left and right upper edges
        for (sx = [-V2X_PATCH_W/2, V2X_PATCH_W/2]) {
            translate([sx, V2X_PATCH_THICK, 0]) {
                rotate([0, 0, (sx < 0 ? 0 : 180)]) {
                    hull() {
                        translate([0, 0, -4.0]) cube([0.1, 0.8, 8.0], center=false);
                        translate([-0.8, 0.8, -4.0]) cube([0.1, 0.1, 8.0], center=false);
                    }
                }
            }
        }
    }
}

// 1. Symmetrical Main Housing Tub (MJF PA12)
module radar_mr20_main_tub(include_lower_clevis=true) {
    difference() {
        union() {
            // Main sculptured outer body (centered in X and Z)
            hull() {
                translate([0, 0, 0])
                    rotate([90, 0, 0])
                        linear_extrude(height=RADAR_HOUSING_D - RADAR_CORNER_R, center=false)
                            rounded_rect_xz(RADAR_HOUSING_W, RADAR_HOUSING_H, RADAR_CORNER_R);

                translate([0, -(RADAR_HOUSING_D - RADAR_CORNER_R/2), 0])
                    rotate([90, 0, 0])
                        linear_extrude(height=RADAR_CORNER_R/2, center=false)
                            rounded_rect_xz(RADAR_HOUSING_W - 2*RADAR_CORNER_R, RADAR_HOUSING_H - 2*RADAR_CORNER_R, 1.0);
            }

            // Bottom Binder M5 Bulkhead Boss (Centered at X = 0)
            translate([0, -RADAR_HOUSING_D/2, -RADAR_HOUSING_H/2 - 7.0]) {
                hull() {
                    translate([0, 0, 3.5])
                        cube([16.0, 16.0, 7.0], center=true);
                    translate([0, 0, 0])
                        cylinder(r=7.0, h=3.0, center=true, $fn=36);
                }
            }

            // Lower Clevis Mounting Tongue (Centered at X = 0, rear of connector)
            if (include_lower_clevis) {
                translate([0, -RADAR_HOUSING_D + 5.0, -RADAR_HOUSING_H/2 - 9.0]) {
                    difference() {
                        hull() {
                            translate([0, 0, 5.0]) cube([CLEVIS_TONGUE_W, 14.0, 10.0], center=true);
                            translate([0, 0, 0]) rotate([0, 90, 0]) cylinder(r=8.0, h=CLEVIS_TONGUE_W, center=true, $fn=36);
                        }
                        // M5 Pivot Bore
                        rotate([0, 90, 0])
                            cylinder(r=CLEVIS_BORE_DIA/2, h=CLEVIS_TONGUE_W + 2.0, center=true, $fn=32);
                        // Hirth Index Serrations (radial 10° pitch)
                        for (side = [-CLEVIS_TONGUE_W/2, CLEVIS_TONGUE_W/2]) {
                            for (a = [0 : 10 : 350]) {
                                rotate([a, 0, 0])
                                    translate([side, 0, 0])
                                        rotate([0, 90, 0])
                                            cylinder(r1=0.4, r2=0.1, h=0.8, center=true, $fn=4);
                            }
                        }
                    }
                }
            }

            // Rear Garmin Male Quarter-Turn Bayonet Mount (Centered at X=0, Z=0)
            translate([0, -RADAR_HOUSING_D, 0.0]) {
                garmin_male_bayonet();
            }

            // Rear M4 Standoff Bosses (Symmetrical at X = ±20 mm, Z = 0)
            for (dx = [-REAR_M4_PITCH/2, REAR_M4_PITCH/2]) {
                translate([dx, -RADAR_HOUSING_D, 0.0]) {
                    rotate([90, 0, 0])
                        cylinder(r=5.5, h=3.0, center=false, $fn=24);
                }
            }
        }

        // --- INTERNAL CAVITIES (100% Symmetrical) ---

        // 1. Front Radome Window Recess Step
        translate([0, 1.0, 0]) {
            rotate([90, 0, 0])
                linear_extrude(height=RADOME_WINDOW_THICK + 1.2, center=false)
                    rounded_rect_xz(RADOME_WINDOW_W, RADOME_WINDOW_H, 4.0);
        }

        // 2. Peripheral O-Ring Sealing Groove
        difference() {
            translate([0, -RADOME_WINDOW_THICK + 0.2, 0])
                rotate([90, 0, 0])
                    linear_extrude(height=SEAL_GROOVE_D, center=false)
                        rounded_rect_xz(RADOME_WINDOW_W - 2.0, RADOME_WINDOW_H - 2.0, 4.0);

            translate([0, -RADOME_WINDOW_THICK, 0])
                rotate([90, 0, 0])
                    linear_extrude(height=SEAL_GROOVE_D + 0.5, center=false)
                        rounded_rect_xz(RADOME_WINDOW_W - 2.0 - 2*SEAL_GROOVE_W, RADOME_WINDOW_H - 2.0 - 2*SEAL_GROOVE_W, 3.0);
        }

        // 3. PCBA 08 Tray Step (115.0 x 65.0 mm, centered at X=0, Z=0)
        translate([0, -RADOME_WINDOW_THICK, 0]) {
            rotate([90, 0, 0])
                linear_extrude(height=PCBA08_THICK + 1.0, center=false)
                    rounded_rect_xz(PCBA08_W + 0.6, PCBA08_H + 0.6, 3.5);
        }

        // 4. MR20 Radar Transceiver Center Pocket (Dead Center at X=0, Z=0)
        translate([0, -MR20_MODULE_D/2 - RADOME_WINDOW_THICK - PCBA08_THICK, 0]) {
            cube([MR20_MODULE_W + 0.6, MR20_MODULE_D + 0.4, MR20_MODULE_H + 0.6], center=true);
        }

        // 5. Main Rear Cavity for Inline Cable Adapter Module & Wiring Loop (Feedback Zeile 46)
        translate([0, -RADAR_HOUSING_D + ADAPTER_CAVITY_D/2 + RADAR_WALL_THICK, 0]) {
            cube([ADAPTER_CAVITY_W, ADAPTER_CAVITY_D, ADAPTER_CAVITY_H], center=true);
        }

        // 6. Binder M5 Bulkhead Connector Bore & Anti-Rotation D-Flat (Centered on X = 0)
        translate([0, -RADAR_HOUSING_D/2, -RADAR_HOUSING_H/2 - 12.0]) {
            intersection() {
                cylinder(r=BINDER_M5_BORE_DIA/2, h=18.0, center=false, $fn=32);
                translate([-BINDER_M5_BORE_DIA/2, -BINDER_M5_FLAT_DIST/2, 0])
                    cube([BINDER_M5_BORE_DIA, BINDER_M5_FLAT_DIST, 18.0]);
            }
        }

        // 7. Rear M4 Brass Threaded Insert Pockets (Ruthex M4x8.1, Symmetrical at X = ±20 mm, Z = 0)
        for (dx = [-REAR_M4_PITCH/2, REAR_M4_PITCH/2]) {
            translate([dx, -RADAR_HOUSING_D - 0.5, 0.0]) {
                rotate([90, 0, 0])
                    cylinder(r=2.9, h=9.0, center=false, $fn=24); // 5.8 mm bore for M4 heat insert
            }
        }

        // 8. Front Radome Bezel Fastening Screws (4x M2.5 Torx in corners, Symmetrical)
        for (sx = [-RADOME_WINDOW_W/2 + 3.5, RADOME_WINDOW_W/2 - 3.5]) {
            for (sz = [-RADOME_WINDOW_H/2 + 3.5, RADOME_WINDOW_H/2 - 3.5]) {
                translate([sx, 2.0, sz]) {
                    rotate([90, 0, 0]) {
                        cylinder(r=1.4, h=10.0, center=false, $fn=16); // M2.5 thread bore
                        translate([0, 0, -2.5])
                            cylinder(r=2.6, h=3.0, center=false, $fn=24); // screw head pocket
                    }
                }
            }
        }
    }

    // Monolithic 5.9 GHz V2X Ceramic Patch Antenna Snap Cradle (Left Wing Chamber)
    v2x_patch_antenna_cradle();
}

// 2. Symmetrical Optical Radome Window Insert (Laser-cut / Molded PC or PETG)
module radar_mr20_radome_window() {
    color([0.9, 0.95, 1.0, 0.4]) {
        difference() {
            rotate([90, 0, 0])
                linear_extrude(height=RADOME_WINDOW_THICK, center=false)
                    rounded_rect_xz(RADOME_WINDOW_W, RADOME_WINDOW_H, 4.0);

            // 4x M2.5 Corner Screw Holes
            for (sx = [-RADOME_WINDOW_W/2 + 3.5, RADOME_WINDOW_W/2 - 3.5]) {
                for (sz = [-RADOME_WINDOW_H/2 + 3.5, RADOME_WINDOW_H/2 - 3.5]) {
                    translate([sx, 1.0, sz])
                        rotate([90, 0, 0])
                            cylinder(r=1.4, h=RADOME_WINDOW_THICK + 2.0, center=false, $fn=16);
                }
            }
        }
    }
}

// 3. Complete Assembly Preview
module radar_mr20_assembly() {
    radar_mr20_main_tub();
    translate([0, 0.5, 0])
        radar_mr20_radome_window();
}

// Default Render: Main Tub
radar_mr20_main_tub();
