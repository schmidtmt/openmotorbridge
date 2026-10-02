// =============================================================================
// OpenMotorBridge - Satellite Pod: COTS 2-Pin Magnetic Frame Dock
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/cots_magnetic_frame_dock.scad
// Description: Modern, high-durability stationary frame dock for direct mounting
//              of an industrial COTS 2-Pin Magnetic Pogo Connector (e.g. HytePro
//              M411 or generic IP68 2-pole magnetic pogo socket, NO PCB!).
//              Clamps around subframe tubes Ø 25.4 - 28.6 mm (1" to 1.125").
//
// 100% PURE-DC COTS ARCHITECTURE:
// - Eliminates obsolete PCBA 06 breakout board and M8 threaded pass-throughs.
// - Directly accommodates the COTS 2-Pin magnetic socket with positive retaining
//   shoulder (absorbs 10-15 N axial breakaway force during pannier removal).
// - Integrated Stage-1 cable strain relief channel for 2x 0.5 mm² PUR/FLRY cable.
// - Clamps securely via 2x or 4x DIN 912 M3 bolts into captive DIN 934 M3 nut pockets.
// =============================================================================

$fn = 60;

// =============================================================================
// PARAMETRIC CONFIGURATION
// =============================================================================
tube_dia_default       = 26.0;   // Subframe tube diameter (Harley / BMW GS, mm)
dock_len_default       = 36.0;   // Total dock body length (X-axis, mm)
dock_w_default         = 18.0;   // Main dock body width (Y-axis, mm)
dock_h_default         = 19.0;   // Total body height to saddle apex (Z-axis, mm)
wing_w_default         = 38.0;   // Clamp wing width across M3 screw holes (mm)

// COTS Magnetic Socket Nest (e.g. HytePro M411 2-Pin)
// Socket front face: 12.4 x 5.4 mm (with 0.3mm print tolerance = 12.8 x 5.8 mm)
socket_w_default       = 12.8;   // Outer width of magnetic socket front face (mm)
socket_h_default       = 5.8;    // Outer height of magnetic socket front face (mm)
socket_depth_default   = 8.5;    // Depth of socket body pocket (mm)
socket_flange_w        = 14.8;   // Retaining shoulder / flange width (mm)
socket_flange_h        = 7.2;    // Retaining shoulder height (mm)
socket_flange_t        = 2.2;    // Retaining shoulder thickness (mm)

// Cable Strain Relief Channel (2x 0.5 mm² PUR / FLRY cable Ø 3.6 - 4.2 mm)
cable_bore_dia_default = 4.4;    // Cable pass-through bore diameter (mm)
zip_tie_w_default      = 2.8;    // Mini cable tie slot width (mm)
zip_tie_h_default      = 1.5;    // Mini cable tie slot height (mm)

// Fasteners (DIN 912 M3 bolts & captive DIN 934 M3 nuts)
screw_m3_pass_dia      = 3.4;    // M3 clearance hole (mm)
nut_m3_sw              = 5.6;    // DIN 934 M3 width across flats (mm)
nut_m3_h               = 2.6;    // DIN 934 M3 nut pocket depth (mm)
screw_spacing_x        = 22.0;   // Longitudinal spacing between M3 bolts (mm)
wing_hole_y            = 14.0;   // Lateral offset from center (Y = ±14 mm)

// =============================================================================
// 1. COTS MAGNETIC FRAME DOCK BODY (LOWER DOCK WITH TUBE SADDLE & SOCKET NEST)
// =============================================================================
module cots_magnetic_frame_dock_body(
    tube_dia      = tube_dia_default,
    dock_len      = dock_len_default,
    dock_w        = dock_w_default,
    dock_h        = dock_h_default,
    wing_w        = wing_w_default,
    socket_w      = socket_w_default,
    socket_h      = socket_h_default,
    socket_depth  = socket_depth_default
) {
    difference() {
        union() {
            // Main solid body with rounded edges
            hull() {
                translate([-dock_len/2 + 2, -dock_w/2 + 2, 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, -dock_w/2 + 2, 2])
                    sphere(r=2);
                translate([-dock_len/2 + 2, dock_w/2 - 2, 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, dock_w/2 - 2, 2])
                    sphere(r=2);
                translate([-dock_len/2 + 2, -dock_w/2 + 2, dock_h - 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, -dock_w/2 + 2, dock_h - 2])
                    sphere(r=2);
                translate([-dock_len/2 + 2, dock_w/2 - 2, dock_h - 2])
                    sphere(r=2);
                translate([dock_len/2 - 2, dock_w/2 - 2, dock_h - 2])
                    sphere(r=2);
            }

            // Lateral clamp wings (symmetric Y = ±wing_hole_y)
            hull() {
                translate([-screw_spacing_x/2 - 3, -wing_w/2, 0])
                    cube([screw_spacing_x + 6, wing_w, 7.0]);
                translate([-screw_spacing_x/2 - 1, -wing_w/2 + 1, 0])
                    cube([screw_spacing_x + 2, wing_w - 2, 8.5]);
            }
        }

        // --- SUBTRACTIONS ---

        // 1. Frame Tube Saddle (concave cradle along X-axis at top face)
        translate([0, 0, dock_h + tube_dia/2 - 3.5])
            rotate([0, 90, 0])
                cylinder(d=tube_dia, h=dock_len + 4, center=true);

        // 2. Front Socket Cavity (faces +X direction, towards saddlebag grommet)
        // Main pocket for COTS 2-Pin magnetic connector
        translate([dock_len/2 - socket_depth/2 + 0.1, 0, 5.0])
            cube([socket_depth + 0.2, socket_w, socket_h], center=true);

        // Retaining shoulder / flange pocket (prevents pulling out during breakaway)
        translate([dock_len/2 - socket_depth + socket_flange_t/2, 0, 5.0])
            cube([socket_flange_t + 0.2, socket_flange_w, socket_flange_h], center=true);

        // 3. Rear Cable Pass-Through & Solder Cup Chamber
        translate([-dock_len/4, 0, 5.0])
            rotate([0, 90, 0])
                cylinder(d=cable_bore_dia_default, h=dock_len/2 + 2, center=true);

        // Rear wire transition chamber
        translate([0, 0, 5.0])
            cube([10.0, 8.0, 6.0], center=true);

        // 4. Integrated Mini-Cable-Tie Channel (Stage-1 Strain Relief)
        translate([-6.0, 0, 5.0])
            difference() {
                cylinder(d=cable_bore_dia_default + 6.0, h=zip_tie_w_default, center=true);
                cylinder(d=cable_bore_dia_default + 1.0, h=zip_tie_w_default + 0.2, center=true);
            }

        // 5. 4x M3 Clamp Screw Clearance Holes (DIN 912)
        for (sx = [-screw_spacing_x/2, screw_spacing_x/2]) {
            for (sy = [-wing_hole_y, wing_hole_y]) {
                translate([sx, sy, -1])
                    cylinder(d=screw_m3_pass_dia, h=dock_h + 4);
                
                // Captive DIN 934 M3 Hex Nut Pockets on bottom face
                translate([sx, sy, -0.1])
                    rotate([0, 0, 30])
                        cylinder(d=nut_m3_sw / cos(30), h=nut_m3_h + 0.1, $fn=6);
            }
        }
    }
}

// =============================================================================
// 2. COTS MAGNETIC FRAME CLAMP STRAP (UPPER SHELL STRAP AROUND TUBE)
// =============================================================================
module cots_magnetic_frame_clamp(
    tube_dia      = tube_dia_default,
    dock_len      = dock_len_default,
    wing_w        = wing_w_default
) {
    clamp_t = 4.0;
    clamp_len = screw_spacing_x + 8.0;

    difference() {
        union() {
            // Half-cylinder strap arching over tube
            translate([0, 0, 0])
                rotate([0, 90, 0])
                    cylinder(d=tube_dia + 2*clamp_t, h=clamp_len, center=true);

            // Lateral clamp mounting ears
            translate([-clamp_len/2, -wing_w/2, -clamp_t/2])
                cube([clamp_len, wing_w, clamp_t + 2.5]);
        }

        // Internal tube clearance
        rotate([0, 90, 0])
            cylinder(d=tube_dia, h=clamp_len + 2, center=true);

        // Cut off lower half (keep only upper strap arch)
        translate([-clamp_len - 1, -wing_w - 1, -tube_dia - clamp_t])
            cube([2*clamp_len + 2, 2*wing_w + 2, tube_dia + clamp_t]);

        // 4x M3 Bolt Clearance Pass-Holes with DIN 912 Allen Head Counterbores
        for (sx = [-screw_spacing_x/2, screw_spacing_x/2]) {
            for (sy = [-wing_hole_y, wing_hole_y]) {
                translate([sx, sy, -5])
                    cylinder(d=screw_m3_pass_dia, h=15);
                translate([sx, sy, 1.2])
                    cylinder(d=6.0, h=8.0); // DIN 912 head recess
            }
        }
    }
}

// =============================================================================
// 3. COMPLETE ASSEMBLED PREVIEW
// =============================================================================
module cots_magnetic_frame_dock_assembly() {
    // Dock Body
    color([0.25, 0.25, 0.28])
        cots_magnetic_frame_dock_body();

    // Frame Tube (Translucent Grey Preview)
    %translate([0, 0, dock_h_default + tube_dia_default/2 - 3.5])
        rotate([0, 90, 0])
            cylinder(d=tube_dia_default, h=60, center=true);

    // Upper Clamp Strap (Orange Accent)
    color([0.85, 0.45, 0.15])
        translate([0, 0, dock_h_default + tube_dia_default - 7.0])
            cots_magnetic_frame_clamp();

    // COTS Magnetic Socket Dummy (Gold / Nickel Preview)
    color([0.85, 0.75, 0.25])
        translate([dock_len_default/2 - socket_depth_default/2, 0, 5.0])
            cube([socket_depth_default, socket_w_default - 0.4, socket_h_default - 0.4], center=true);
}

// Default export mode
part = "assembly"; // "body", "clamp", "assembly"

if (part == "body") {
    cots_magnetic_frame_dock_body();
} else if (part == "clamp") {
    rotate([180, 0, 0])
        cots_magnetic_frame_clamp();
} else {
    cots_magnetic_frame_dock_assembly();
}
