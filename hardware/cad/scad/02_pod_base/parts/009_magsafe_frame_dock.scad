// =============================================================================
// OpenMotorBridge - Satellite Pod: MagSafe Frame Dock (Under-Seat Breakaway Mount)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/009_magsafe_frame_dock.scad
// Description: High-durability stationary frame dock mounted under the seat
//              overhang (Harley Touring / CVO ST frame tube Ø 25.4 - 28.6 mm).
//              Houses PCBA 06 (26.0 x 11.5 mm MagSafe Breakout & TVS/PPTC board)
//              with internal slide-in guide rails, snap-lock retention teeth,
//              M8 cable compression strain relief, MagSafe magnetic lead-in funnel,
//              split tube clamp collar with M3 hardware, and dual zip-tie slots.
// =============================================================================

$fn = 50;

// =============================================================================
// PARAMETRIC CONFIGURATION
// =============================================================================
tube_dia_default      = 26.0;   // Harley subframe tube diameter (mm)
dock_len_default      = 42.0;   // Total dock body length (X-axis, mm)
dock_w_default        = 22.0;   // Main dock body width (Y-axis, mm)
dock_h_default        = 22.0;   // Main dock body height (Z-axis, mm)
wing_w_default        = 36.0;   // Clamp wing width across screw holes (mm)

// PCBA 06 Envelope
pcb_len_default       = 26.2;   // PCB length with tolerance (mm)
pcb_w_default         = 11.8;   // PCB width with tolerance (mm)
pcb_t_default         = 1.8;    // PCB slot thickness (mm)

// MagSafe Magnetic Coupling Interface
magsafe_w_default     = 16.5;   // MagSafe connector pocket width (mm)
magsafe_h_default     = 7.6;    // MagSafe connector pocket height (mm)
magsafe_depth_default = 6.5;    // MagSafe connector pocket depth (mm)

// M8 Cable Pass-Through & Strain Relief
m8_bore_dia_default   = 8.4;    // M8 cable pass-through bore (mm)

// =============================================================================
// 1. MAIN LOWER DOCK HOUSING (WITH SLIDE-IN PCB RAILS & MOUNTING CRADLE)
// =============================================================================
module magsafe_frame_dock_body(
    tube_dia      = tube_dia_default,
    dock_len      = dock_len_default,
    dock_w        = dock_w_default,
    dock_h        = dock_h_default,
    wing_w        = wing_w_default,
    pcb_len       = pcb_len_default,
    pcb_w         = pcb_w_default,
    pcb_t         = pcb_t_default,
    magsafe_w     = magsafe_w_default,
    magsafe_h     = magsafe_h_default,
    magsafe_depth = magsafe_depth_default,
    m8_bore_dia   = m8_bore_dia_default
) {
    difference() {
        union() {
            // 1.1 Main Ergonomic Aerodynamic Monocoque Block
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

            // 1.2 Dual Transverse Tube Clamp Wings (for 2x M3 Screws)
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

            // 1.3 MagSafe Outer Hood Reinforcement Collar
            translate([dock_len/2 - 2.0, 0, dock_h/2 - 2.0]) {
                hull() {
                    translate([0, -(magsafe_w/2 + 2.0), -(magsafe_h/2 + 2.0)])
                        cube([4.0, magsafe_w + 4.0, magsafe_h + 4.0], center=false);
                }
            }
        }

        // 1.4 Concave Frame Tube Cradle Saddle (Ø 26 mm) with Anti-Slip Ribs
        translate([0, 0, dock_h + tube_dia/2 - 2.5]) {
            rotate([0, 90, 0])
                cylinder(r=tube_dia/2, h=dock_len + 4.0, center=true);

            // Friction Grip Ribs (4x 0.8mm axial ribs)
            for (ang = [-30, -10, 10, 30]) {
                rotate([ang, 0, 0])
                    translate([0, 0, -tube_dia/2 + 0.3])
                        rotate([0, 90, 0])
                            cylinder(r=0.6, h=dock_len + 6.0, center=true);
            }
        }

        // 1.5 M3 Threaded Insert / Nut Pockets in Clamp Wings (Spacing Y = +/- 13.5 mm)
        for (sx = [-8.0, 8.0]) {
            for (sy = [-wing_w/2 + 4.0, wing_w/2 - 4.0]) {
                translate([sx, sy, -1]) {
                    // M3 screw pass hole (Ø 3.4 mm)
                    cylinder(r=1.7, h=dock_h + 2.0, center=false);
                    // Brass Heat-Set Insert Pocket (Ø 4.4 mm x 5.5 mm from bottom)
                    cylinder(r=2.2, h=6.0, center=false);
                }
            }
        }

        // 1.6 Dual Heavy-Duty Zip-Tie Slots (5.2 x 2.8 mm) for Universal Frame Mounting
        for (zx = [-12.0, 12.0]) {
            translate([zx, 0, dock_h - 4.0])
                cube([5.2, wing_w + 4.0, 2.8], center=true);
        }

        // -------------------------------------------------------------
        // INTERNAL PCBA 06 CAVITY & SLIDE-IN GUIDE RAILS
        // -------------------------------------------------------------
        // PCB Center at X = 0.0, Z = 8.5 mm
        translate([0, 0, 8.5]) {
            // Main PCB Board Cavity (26.2 x 11.8 x 6.0 mm clearance above/below)
            cube([pcb_len, pcb_w, 6.0], center=true);

            // Precision Lateral Slide-In Guide Rails (Slot W=12.2mm, H=1.9mm)
            cube([pcb_len + 2.0, pcb_w + 0.8, pcb_t], center=true);

            // Retention Snap Stops (engaging PCB side notches at X=0)
            // Left & Right side reliefs
            translate([0, 0, 0])
                cube([3.0, pcb_w + 2.5, 3.0], center=true);
        }

        // -------------------------------------------------------------
        // MAGSAFE RECEPTACLE POCKET & LEAD-IN FUNNEL (SADDLEBAG SIDE)
        // -------------------------------------------------------------
        translate([dock_len/2, 0, 8.5]) {
            // Exact Pocket for MagSafe Magnetic Receptacle
            translate([-magsafe_depth, -(magsafe_w/2), -(magsafe_h/2)])
                cube([magsafe_depth + 1.0, magsafe_w, magsafe_h], center=false);

            // Tactile 30° Lead-In Funnel (Einfädeltrichter for blind docking)
            hull() {
                translate([0.1, -(magsafe_w/2 + 2.0), -(magsafe_h/2 + 2.0)])
                    cube([0.1, magsafe_w + 4.0, magsafe_h + 4.0], center=false);
                translate([-2.5, -(magsafe_w/2), -(magsafe_h/2)])
                    cube([0.1, magsafe_w, magsafe_h], center=false);
            }
        }

        // -------------------------------------------------------------
        // M8 CABLE ENTRY & COMPRESSION STRAIN RELIEF (BIKE SIDE)
        // -------------------------------------------------------------
        translate([-dock_len/2 - 1.0, 0, 8.5]) {
            rotate([0, 90, 0]) {
                // Outer M8 Cable Pass Bore (Ø 8.4 mm)
                cylinder(r=m8_bore_dia/2, h=8.0, center=false);

                // Conical Strain-Relief Compression Chamber (Ø 10.0 -> 8.4 mm)
                cylinder(r1=5.2, r2=m8_bore_dia/2, h=6.0, center=false);

                // O-Ring / Gasket Counterbore (Ø 11.5 mm x 2.5 mm)
                cylinder(r=5.75, h=3.0, center=false);
            }
        }

        // -------------------------------------------------------------
        // BOTTOM SERVICE & POTTING ACCESS APERTURE
        // -------------------------------------------------------------
        translate([0, 0, -0.5]) {
            // Rectangular opening for bottom lid sealing
            hull() {
                translate([-dock_len/2 + 8.0, -dock_w/2 + 3.5, 0])
                    cylinder(r=2.0, h=4.0, center=false);
                translate([dock_len/2 - 8.0, -dock_w/2 + 3.5, 0])
                    cylinder(r=2.0, h=4.0, center=false);
                translate([-dock_len/2 + 8.0, dock_w/2 - 3.5, 0])
                    cylinder(r=2.0, h=4.0, center=false);
                translate([dock_len/2 - 8.0, dock_w/2 - 3.5, 0])
                    cylinder(r=2.0, h=4.0, center=false);
            }

            // Tongue-and-Groove Perimeter Gasket Ledge (0.8 mm step)
            hull() {
                translate([-dock_len/2 + 6.5, -dock_w/2 + 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([dock_len/2 - 6.5, -dock_w/2 + 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([-dock_len/2 + 6.5, dock_w/2 - 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([dock_len/2 - 6.5, dock_w/2 - 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
            }
        }

        // Bottom Lid M2.5 Screw Holes (2x at X = +/- 15.0 mm)
        for (lx = [-15.0, 15.0]) {
            translate([lx, 0, -1.0]) {
                cylinder(r=1.3, h=7.0, center=false); // M2.5 pilot hole (Ø 2.6 mm)
                cylinder(r=2.5, h=2.5, center=false); // Counterbore
            }
        }
    }
}

// =============================================================================
// 2. UPPER SPLIT TUBE CLAMP STRAP (FRAME MOUNT STRAP)
// =============================================================================
module magsafe_frame_dock_clamp(
    tube_dia = tube_dia_default,
    wing_w   = wing_w_default
) {
    clamp_len = 24.0;
    clamp_th  = 3.5;
    
    difference() {
        union() {
            // Half-cylindrical saddle matching tube OD
            rotate([0, 90, 0])
                cylinder(r=tube_dia/2 + clamp_th, h=clamp_len, center=true);

            // Clamp wings with rounded edges
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

        // Inner frame tube bore
        rotate([0, 90, 0])
            cylinder(r=tube_dia/2, h=clamp_len + 4.0, center=true);

        // Lower split clearance (prevents bottoming out before full torque)
        translate([0, 0, -tube_dia/2 - 10])
            cube([clamp_len + 6.0, wing_w + 6.0, 20.0], center=true);

        // M3 Screw Pass Holes & Counterbores (matching dock body at X = +/- 8.0 mm)
        for (sx = [-8.0, 8.0]) {
            for (sy = [-wing_w/2 + 4.0, wing_w/2 - 4.0]) {
                translate([sx, sy, -tube_dia]) {
                    cylinder(r=1.7, h=2*tube_dia, center=false); // M3 clearance (Ø 3.4 mm)
                    translate([0, 0, tube_dia + clamp_th + 1.0])
                        cylinder(r=3.2, h=10.0, center=false);   // DIN 912 Allen Head Counterbore (Ø 6.4 mm)
                }
            }
        }
    }
}

// =============================================================================
// 3. BOTTOM SERVICE & SEALING LID (FOR WATERPROOF POTTING / GASKET)
// =============================================================================
module magsafe_frame_dock_lid(
    dock_len = dock_len_default,
    dock_w   = dock_w_default
) {
    difference() {
        union() {
            // Main lid plate (thickness 2.0 mm)
            hull() {
                translate([-dock_len/2 + 6.5, -dock_w/2 + 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([dock_len/2 - 6.5, -dock_w/2 + 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([-dock_len/2 + 6.5, dock_w/2 - 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
                translate([dock_len/2 - 6.5, dock_w/2 - 2.0, 0])
                    cylinder(r=2.0, h=1.8, center=false);
            }

            // Tongue-and-Groove Sealing Ridge (0.8 mm step)
            translate([0, 0, 1.8]) {
                hull() {
                    translate([-dock_len/2 + 8.0, -dock_w/2 + 3.5, 0])
                        cylinder(r=1.8, h=1.2, center=false);
                    translate([dock_len/2 - 8.0, -dock_w/2 + 3.5, 0])
                        cylinder(r=1.8, h=1.2, center=false);
                    translate([-dock_len/2 + 8.0, dock_w/2 - 3.5, 0])
                        cylinder(r=1.8, h=1.2, center=false);
                    translate([dock_len/2 - 8.0, dock_w/2 - 3.5, 0])
                        cylinder(r=1.8, h=1.2, center=false);
                }
            }
        }

        // 2x M2.5 Counterbored Screw Holes (matching dock body at X = +/- 15.0 mm)
        for (lx = [-15.0, 15.0]) {
            translate([lx, 0, -1.0]) {
                cylinder(r=1.4, h=6.0, center=false); // M2.5 screw clearance (Ø 2.8 mm)
                cylinder(r=2.6, h=1.8, center=false); // DIN 7991 countersink / counterbore
            }
        }
    }
}

// =============================================================================
// 4. ASSEMBLY & PREVIEW
// =============================================================================
module magsafe_frame_dock_assembly() {
    // 1. Lower Dock Housing
    color([0.22, 0.22, 0.22, 1.0])
        magsafe_frame_dock_body();

    // 2. Simulated Frame Tube (Harley Touring Subframe Ø 26 mm)
    color([0.65, 0.65, 0.65, 0.35])
        translate([0, 0, dock_h_default + tube_dia_default/2 - 2.5])
            rotate([0, 90, 0])
                cylinder(r=tube_dia_default/2, h=60.0, center=true);

    // 3. Upper Tube Clamp Collar
    color([0.30, 0.30, 0.30, 1.0])
        translate([0, 0, dock_h_default + tube_dia_default/2 - 2.5])
            magsafe_frame_dock_clamp();

    // 4. Bottom Sealing Lid
    color([0.20, 0.20, 0.20, 1.0])
        translate([0, 0, -4.0])
            magsafe_frame_dock_lid();

    // 5. Simulated PCBA 06 Inside Guide Rails
    color([0.15, 0.45, 0.25, 0.9])
        translate([0, 0, 8.5])
            cube([pcb_len_default - 0.2, pcb_w_default - 0.3, 1.6], center=true);
}

// Default invocation for STL exports / standalone previews
magsafe_frame_dock_body();
