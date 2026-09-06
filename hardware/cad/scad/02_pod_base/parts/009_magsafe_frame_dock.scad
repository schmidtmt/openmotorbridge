// =============================================================================
// OpenMotorBridge - Satellite Pod: MagSafe Frame Dock (Under-Seat Breakaway Mount)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad
// Description: High-durability stationary frame dock mounted under the seat
//              overhang (Harley Touring / CVO ST frame tube Ø 25.4 - 28.6 mm).
//              Houses PCBA 06 (28.0 x 11.5 mm MagSafe Breakout & TVS/PPTC board).
//
// CLAMSHELL + CENTRAL M2.5 SCREW BOSS DESIGN:
// - Split horizontally at connector/PCB centerline Z = 8.5 mm into:
//   1. Upper Shell (magsafe_frame_dock_body):
//      - Semicircular upper M8 cradle & MagSafe nest
//      - Ø 26 mm frame tube cradle saddle & M3 clamp wings
//      - Internal central boss with M2.5 brass heat-set insert pocket (Ruthex Ø 3.6 x 4.5mm)
//      - Perimeter sealing tongue for IP67 watertight seal
//   2. Lower Shell (magsafe_frame_dock_lid):
//      - Semicircular lower M8 cradle & MagSafe nest
//      - PCB perimeter resting ledge at Z = 7.7 mm
//      - Internal central boss with M2.5 screw pass hole (Ø 2.8mm) and DIN 912 counterbore (Ø 5.2 x 2.8mm)
//      - Perimeter sealing groove
//   3. Clamp Strap (magsafe_frame_dock_clamp):
//      - Clamps around Ø 26 mm subframe tube via 4x M3 hardware
//
// ZERO SIDE SCREW EARS: Total enclosure width remains sleek (16.0 mm).
// Rigid pre-soldered M8 + PCB + MagSafe assembly drops straight into the lower
// cradle without axial pushing or cable stress.
// =============================================================================

$fn = 60;

// =============================================================================
// PARAMETRIC CONFIGURATION
// =============================================================================
tube_dia_default      = 26.0;   // Harley subframe tube diameter (mm)
dock_len_default      = 44.0;   // Total dock body length (X-axis, mm)
dock_w_default        = 16.0;   // Main dock body width (Y-axis, mm)
dock_h_default        = 21.0;   // Total assembled height to tube saddle apex (Z-axis, mm)
split_z_default       = 8.5;    // Horizontal clamshell split plane (connector centerline, mm)
wing_w_default        = 36.0;   // Clamp wing width across M3 screw holes (mm)

// PCBA 06 Envelope (28.0 x 11.5 x 1.6 mm)
pcb_len_default       = 28.4;   // PCB cavity length with clearance (mm)
pcb_w_default         = 11.8;   // PCB cavity width with clearance (mm)
pcb_t_default         = 1.6;    // PCB substrate thickness (mm)
pcb_z_bot_default     = 7.7;    // Z-level of PCB bottom face (mm)
pcb_z_top_default     = 9.3;    // Z-level of PCB top face (mm)

// Central Mounting Boss (M2.5)
boss_dia_default      = 4.4;    // Boss outer diameter (fits PCB Ø 4.5mm keepout, mm)
insert_dia_default    = 3.6;    // Heat-set insert hole diameter (Ruthex M2.5, mm)
insert_depth_default  = 4.5;    // Heat-set insert hole depth (mm)
screw_pass_dia_default= 2.8;    // M2.5 screw clearance pass hole (mm)
screw_head_dia_default= 5.2;    // DIN 912 M2.5 Allen head counterbore diameter (mm)
screw_head_h_default  = 2.8;    // DIN 912 M2.5 counterbore depth (mm)

// MagSafe Magnetic Dock Interface
magsafe_w_default     = 12.2;   // MagSafe connector pocket width (mm)
magsafe_h_default     = 5.4;    // MagSafe connector pocket height (mm)
magsafe_depth_default = 7.0;    // MagSafe connector pocket depth from East face (mm)

// M8 Cable Pass-Through & Collar Retention
m8_bore_dia_default   = 8.4;    // M8 cable pass-through bore (mm)
m8_collar_dia_default = 10.4;   // M8 retaining collar / O-ring groove diameter (mm)
m8_collar_w_default   = 3.0;    // Collar groove width (mm)

// =============================================================================
// 1. UPPER DOCK HOUSING (WITH TUBE SADDLE, CLAMP WINGS & UPPER CRADLE)
// =============================================================================
module magsafe_frame_dock_body(
    tube_dia      = tube_dia_default,
    dock_len      = dock_len_default,
    dock_w        = dock_w_default,
    dock_h        = dock_h_default,
    split_z       = split_z_default,
    wing_w        = wing_w_default,
    pcb_len       = pcb_len_default,
    pcb_w         = pcb_w_default,
    boss_dia      = boss_dia_default,
    insert_dia    = insert_dia_default,
    insert_depth  = insert_depth_default,
    magsafe_w     = magsafe_w_default,
    magsafe_h     = magsafe_h_default,
    magsafe_depth = magsafe_depth_default,
    m8_bore_dia   = m8_bore_dia_default,
    m8_collar_dia = m8_collar_dia_default,
    m8_collar_w   = m8_collar_w_default
) {
    difference() {
        union() {
            // Main Upper Shell Monocoque Body
            difference() {
                union() {
                    // Outer rounded block
                    intersection() {
                        hull() {
                            translate([-dock_len/2 + 3, -dock_w/2 + 3, 3])
                                sphere(r=3);
                            translate([dock_len/2 - 3, -dock_w/2 + 3, 3])
                                sphere(r=3);
                            translate([-dock_len/2 + 3, dock_w/2 - 3, 3])
                                sphere(r=3);
                            translate([dock_len/2 - 3, dock_w/2 - 3, 3])
                                sphere(r=3);

                            translate([-dock_len/2 + 3, -dock_w/2 + 3, dock_h - 3])
                                sphere(r=3);
                            translate([dock_len/2 - 3, -dock_w/2 + 3, dock_h - 3])
                                sphere(r=3);
                            translate([-dock_len/2 + 3, dock_w/2 - 3, dock_h - 3])
                                sphere(r=3);
                            translate([dock_len/2 - 3, dock_w/2 - 3, dock_h - 3])
                                sphere(r=3);
                        }
                        // Clip strictly to Z >= split_z
                        translate([0, 0, split_z + (dock_h - split_z)/2 + 20])
                            cube([dock_len + 10, dock_w + 10, dock_h - split_z + 40], center=true);
                    }

                    // Dual Transverse Tube Clamp Wings (for 4x M3 Screws)
                    translate([0, 0, dock_h - 6.0]) {
                        hull() {
                            translate([-8.0, -wing_w/2 + 3.5, 0])
                                cylinder(r=3.5, h=6.0, center=false);
                            translate([8.0, -wing_w/2 + 3.5, 0])
                                cylinder(r=3.5, h=6.0, center=false);
                            translate([-8.0, wing_w/2 - 3.5, 0])
                                cylinder(r=3.5, h=6.0, center=false);
                            translate([8.0, wing_w/2 - 3.5, 0])
                                cylinder(r=3.5, h=6.0, center=false);
                        }
                    }

                    // Perimeter Sealing Tongue (0.8mm step down at split plane Z = split_z)
                    translate([0, 0, split_z - 0.8]) {
                        difference() {
                            hull() {
                                translate([-dock_len/2 + 2.5, -dock_w/2 + 2.5, 0])
                                    cylinder(r=2.5, h=0.81, center=false);
                                translate([dock_len/2 - 2.5, -dock_w/2 + 2.5, 0])
                                    cylinder(r=2.5, h=0.81, center=false);
                                translate([-dock_len/2 + 2.5, dock_w/2 - 2.5, 0])
                                    cylinder(r=2.5, h=0.81, center=false);
                                translate([dock_len/2 - 2.5, dock_w/2 - 2.5, 0])
                                    cylinder(r=2.5, h=0.81, center=false);
                            }
                            translate([0, 0, -0.5])
                                cube([pcb_len, pcb_w, 2.0], center=true);
                        }
                    }
                }

                // Frame Tube Saddle Cradle (Ø 26 mm) with Grip Ribs
                translate([0, 0, dock_h + tube_dia/2 - 2.5]) {
                    rotate([0, 90, 0])
                        cylinder(r=tube_dia/2, h=dock_len + 4.0, center=true);

                    for (ang = [-30, -10, 10, 30]) {
                        rotate([ang, 0, 0])
                            translate([0, 0, -tube_dia/2 + 0.3])
                                rotate([0, 90, 0])
                                    cylinder(r=0.6, h=dock_len + 6.0, center=true);
                    }
                }

                // M3 Threaded Insert Pockets in Clamp Wings (4x at X = +/- 8.0, Y = +/- 14.0 mm)
                for (sx = [-8.0, 8.0]) {
                    for (sy = [-wing_w/2 + 4.0, wing_w/2 - 4.0]) {
                        translate([sx, sy, dock_h - 10.0]) {
                            cylinder(r=1.7, h=12.0, center=false);
                            cylinder(r=2.2, h=6.0, center=false);
                        }
                    }
                }

                // Dual Heavy-Duty Zip-Tie Slots (5.2 x 2.8 mm)
                for (zx = [-12.0, 12.0]) {
                    translate([zx, 0, dock_h - 4.0])
                        cube([5.2, wing_w + 4.0, 2.8], center=true);
                }

                // Upper Internal PCBA Cavity (Z = split_z to 12.0 mm, 2.7 mm above PCB)
                translate([0, 0, split_z]) {
                    translate([-pcb_len/2, -pcb_w/2, 0])
                        cube([pcb_len, pcb_w, 12.0 - split_z], center=false);
                }

                // Upper Semicircular M8 Cradle (West End, X = -23.0 to -14.0)
                translate([-dock_len/2 - 1.0, 0, split_z]) {
                    rotate([0, 90, 0]) {
                        cylinder(r=m8_bore_dia/2, h=10.0, center=false);
                        translate([0, 0, 3.0])
                            cylinder(r=m8_collar_dia/2, h=m8_collar_w, center=false);
                    }
                }

                // Upper Semicircular MagSafe Nest (East End, X = +14.0 to +23.0)
                translate([dock_len/2 - magsafe_depth, -(magsafe_w/2), split_z]) {
                    cube([magsafe_depth + 2.0, magsafe_w, magsafe_h/2], center=false);
                }
                // MagSafe 30° Lead-In Funnel
                translate([dock_len/2, 0, split_z]) {
                    hull() {
                        translate([0.1, -(magsafe_w/2 + 1.5), 0])
                            cube([0.1, magsafe_w + 3.0, magsafe_h/2 + 1.5], center=false);
                        translate([-2.0, -(magsafe_w/2), 0])
                            cube([0.1, magsafe_w, magsafe_h/2], center=false);
                    }
                }
            }

            // Central Internal Boss: robust tapered boss from PCB top (Z=9.3) anchored into roof (Z=16.0)
            translate([0, 0, 9.3])
                cylinder(r1=boss_dia/2, r2=3.2, h=16.0 - 9.3, center=false);
        }

        // Central Boss Heat-Set Insert Pocket (Ruthex M2.5: Ø 3.6 mm x 4.5 mm)
        translate([0, 0, 9.3 - 0.1])
            cylinder(r=insert_dia/2, h=insert_depth + 0.1, center=false);
    }
}

// =============================================================================
// 2. LOWER DOCK HOUSING (WITH CENTRAL SCREW PASS HOLE & LOWER CRADLE)
// =============================================================================
module magsafe_frame_dock_lid(
    dock_len          = dock_len_default,
    dock_w            = dock_w_default,
    dock_h            = dock_h_default,
    split_z           = split_z_default,
    pcb_len           = pcb_len_default,
    pcb_w             = pcb_w_default,
    boss_dia          = boss_dia_default,
    screw_pass_dia    = screw_pass_dia_default,
    screw_head_dia    = screw_head_dia_default,
    screw_head_h      = screw_head_h_default,
    magsafe_w         = magsafe_w_default,
    magsafe_h         = magsafe_h_default,
    magsafe_depth     = magsafe_depth_default,
    m8_bore_dia       = m8_bore_dia_default,
    m8_collar_dia     = m8_collar_dia_default,
    m8_collar_w       = m8_collar_w_default
) {
    difference() {
        union() {
            // Main Lower Shell Monocoque Body
            difference() {
                intersection() {
                    hull() {
                        translate([-dock_len/2 + 3, -dock_w/2 + 3, 3])
                            sphere(r=3);
                        translate([dock_len/2 - 3, -dock_w/2 + 3, 3])
                            sphere(r=3);
                        translate([-dock_len/2 + 3, dock_w/2 - 3, 3])
                            sphere(r=3);
                        translate([dock_len/2 - 3, dock_w/2 - 3, 3])
                            sphere(r=3);

                        translate([-dock_len/2 + 3, -dock_w/2 + 3, dock_h - 3])
                            sphere(r=3);
                        translate([dock_len/2 - 3, -dock_w/2 + 3, dock_h - 3])
                            sphere(r=3);
                        translate([-dock_len/2 + 3, dock_w/2 - 3, dock_h - 3])
                            sphere(r=3);
                        translate([dock_len/2 - 3, dock_w/2 - 3, dock_h - 3])
                            sphere(r=3);
                    }
                    // Clip strictly to Z <= split_z
                    translate([0, 0, split_z/2])
                        cube([dock_len + 10, dock_w + 10, split_z + 0.01], center=true);
                }

                // Lower Internal PCBA Cavity (Floor at Z = 6.2 mm, 1.5mm clearance below PCB)
                translate([0, 0, 6.2]) {
                    translate([-pcb_len/2, -pcb_w/2, 0])
                        cube([pcb_len, pcb_w, split_z - 6.2 + 0.1], center=false);
                }

                // PCB Perimeter Resting Ledge Step (Recessed from Z = 7.7 to split_z)
                translate([0, 0, 7.7]) {
                    translate([-(pcb_len + 0.8)/2, -(pcb_w + 0.8)/2, 0])
                        cube([pcb_len + 0.8, pcb_w + 0.8, split_z - 7.7 + 0.1], center=false);
                }

                // Lower Semicircular M8 Cradle (West End, X = -23.0 to -14.0)
                translate([-dock_len/2 - 1.0, 0, split_z]) {
                    rotate([0, 90, 0]) {
                        cylinder(r=m8_bore_dia/2, h=10.0, center=false);
                        translate([0, 0, 3.0])
                            cylinder(r=m8_collar_dia/2, h=m8_collar_w, center=false);
                    }
                }

                // Lower Semicircular MagSafe Nest (East End, X = +14.0 to +23.0)
                translate([dock_len/2 - magsafe_depth, -(magsafe_w/2), split_z - magsafe_h/2]) {
                    cube([magsafe_depth + 2.0, magsafe_w, magsafe_h/2 + 0.01], center=false);
                }
                // MagSafe 30° Lead-In Funnel
                translate([dock_len/2, 0, split_z]) {
                    hull() {
                        translate([0.1, -(magsafe_w/2 + 1.5), -(magsafe_h/2 + 1.5)])
                            cube([0.1, magsafe_w + 3.0, magsafe_h/2 + 1.5], center=false);
                        translate([-2.0, -(magsafe_w/2), -magsafe_h/2])
                            cube([0.1, magsafe_w, magsafe_h/2], center=false);
                    }
                }

                // Perimeter Sealing Groove (Recess matching upper shell tongue at Z = split_z)
                translate([0, 0, split_z - 0.8]) {
                    difference() {
                        hull() {
                            translate([-dock_len/2 + 2.2, -dock_w/2 + 2.2, 0])
                                cylinder(r=2.5, h=1.0, center=false);
                            translate([dock_len/2 - 2.2, -dock_w/2 + 2.2, 0])
                                cylinder(r=2.5, h=1.0, center=false);
                            translate([-dock_len/2 + 2.2, dock_w/2 - 2.2, 0])
                                cylinder(r=2.5, h=1.0, center=false);
                            translate([dock_len/2 - 2.2, dock_w/2 - 2.2, 0])
                                cylinder(r=2.5, h=1.0, center=false);
                        }
                        hull() {
                            translate([-dock_len/2 + 3.4, -dock_w/2 + 3.4, -0.5])
                                cylinder(r=2.5, h=2.0, center=false);
                            translate([dock_len/2 - 3.4, -dock_w/2 + 3.4, -0.5])
                                cylinder(r=2.5, h=2.0, center=false);
                            translate([-dock_len/2 + 3.4, dock_w/2 - 3.4, -0.5])
                                cylinder(r=2.5, h=2.0, center=false);
                            translate([dock_len/2 - 3.4, dock_w/2 - 3.4, -0.5])
                                cylinder(r=2.5, h=2.0, center=false);
                        }
                    }
                }
            }

            // Central Internal Boss: stands inside cavity from floor (Z=0) up to PCB bottom (Z=7.7)
            translate([0, 0, 0])
                cylinder(r=boss_dia/2, h=7.7, center=false);
        }

        // Central M2.5 Screw Clearance Hole (Ø 2.8 mm)
        translate([0, 0, -1.0])
            cylinder(r=screw_pass_dia/2, h=10.0, center=false);

        // DIN 912 Allen Screw Head Counterbore (Ø 5.2 mm x 2.8 mm from bottom)
        translate([0, 0, -0.1])
            cylinder(r=screw_head_dia/2, h=screw_head_h + 0.1, center=false);
    }
}

// =============================================================================
// 3. UPPER SPLIT TUBE CLAMP STRAP (FRAME MOUNT STRAP)
// =============================================================================
module magsafe_frame_dock_clamp(
    tube_dia = tube_dia_default,
    wing_w   = wing_w_default
) {
    clamp_len = 24.0;
    clamp_th  = 3.5;
    
    difference() {
        union() {
            rotate([0, 90, 0])
                cylinder(r=tube_dia/2 + clamp_th, h=clamp_len, center=true);

            translate([0, 0, -clamp_th]) {
                hull() {
                    translate([-clamp_len/2 + 3.5, -wing_w/2 + 3.5, 0])
                        cylinder(r=3.5, h=clamp_th + 3.0, center=false);
                    translate([clamp_len/2 - 3.5, -wing_w/2 + 3.5, 0])
                        cylinder(r=3.5, h=clamp_th + 3.0, center=false);
                    translate([-clamp_len/2 + 3.5, wing_w/2 - 3.5, 0])
                        cylinder(r=3.5, h=clamp_th + 3.0, center=false);
                    translate([clamp_len/2 - 3.5, wing_w/2 - 3.5, 0])
                        cylinder(r=3.5, h=clamp_th + 3.0, center=false);
                }
            }
        }

        rotate([0, 90, 0])
            cylinder(r=tube_dia/2, h=clamp_len + 4.0, center=true);

        translate([0, 0, -tube_dia/2 - 10])
            cube([clamp_len + 6.0, wing_w + 6.0, 20.0], center=true);

        for (sx = [-8.0, 8.0]) {
            for (sy = [-wing_w/2 + 4.0, wing_w/2 - 4.0]) {
                translate([sx, sy, -tube_dia]) {
                    cylinder(r=1.7, h=2*tube_dia, center=false);
                    translate([0, 0, tube_dia + clamp_th + 1.0])
                        cylinder(r=3.2, h=10.0, center=false);
                }
            }
        }
    }
}

// =============================================================================
// 4. COMPLETE EXPLODED ASSEMBLY PREVIEW
// =============================================================================
module magsafe_frame_dock_assembly() {
    // 1. Upper Shell (Body)
    color([0.25, 0.25, 0.28, 1.0])
        translate([0, 0, 5.0])
            magsafe_frame_dock_body();

    // 2. Simulated PCBA 06 with Central M2.5 Hole
    color([0.15, 0.50, 0.25, 0.95])
        translate([0, 0, split_z_default])
            difference() {
                cube([28.0, 11.5, 1.6], center=true);
                cylinder(r=1.35, h=2.0, center=true);
            }

    // 3. Lower Shell (Lid)
    color([0.35, 0.35, 0.38, 1.0])
        translate([0, 0, -5.0])
            magsafe_frame_dock_lid();

    // 4. Simulated Frame Tube (Harley Touring Subframe Ø 26 mm)
    color([0.70, 0.70, 0.75, 0.40])
        translate([0, 0, dock_h_default + tube_dia_default/2 - 2.5 + 5.0])
            rotate([0, 90, 0])
                cylinder(r=tube_dia_default/2, h=65.0, center=true);

    // 5. Upper Tube Clamp Collar
    color([0.28, 0.28, 0.30, 1.0])
        translate([0, 0, dock_h_default + tube_dia_default/2 - 2.5 + 15.0])
            magsafe_frame_dock_clamp();

    // 6. Central Clamping Screw (DIN 912 M2.5 x 12 mm)
    color([0.85, 0.85, 0.90, 1.0])
        translate([0, 0, -12.0]) {
            cylinder(r=1.25, h=14.0, center=false);
            cylinder(r=2.25, h=2.5, center=false);
        }
}

// =============================================================================
// SELECTOR FOR EXPORT / RENDER
// =============================================================================
part = "assembly"; // Options: "body", "lid", "clamp", "assembly"

if (part == "body") {
    magsafe_frame_dock_body();
} else if (part == "lid") {
    magsafe_frame_dock_lid();
} else if (part == "clamp") {
    magsafe_frame_dock_clamp();
} else {
    magsafe_frame_dock_assembly();
}
