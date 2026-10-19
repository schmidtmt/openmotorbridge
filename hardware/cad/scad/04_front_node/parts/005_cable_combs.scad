// =============================================================================
// OpenMotorBridge - Front Node: IP68 Circular TPU Cable Glands & Strain Relief
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/005_cable_combs.scad
// Description: IP68 hermetic circular cable gland ports for South (Cockpit 16P)
//              and North (Vehicle 8P) Ø 6.0 mm jacket cables, plus East USB-C.
// =============================================================================

include <../../00_common/parameters.scad>;

// 1. South Cockpit Cable Gland Cutout (in Tub South Wall, Y = 0 mm, X = 35.5 mm)
// Aligned directly with PCBA 05 J_COCKPIT (KiCad: X=127.50 mm, Y=114.50 mm)
module south_round_cable_gland_cutout(
    x_center = 35.5,
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 4.0, // Z = 9.5 mm
    bore_r   = 4.0, // Ø 8.0 mm bore for TPU boot
    collar_r = 5.2, // Ø 10.4 mm internal retention counterbore
    collar_d = 1.2
) {
    // A. Main pass-through cylindrical bore through South wall
    translate([x_center, -1.0, z_center])
        rotate([-90, 0, 0])
            cylinder(r=bore_r, h=FRONT_NODE_WALL + 2.0, center=false, $fn=36);
            
    // B. Internal counterbore on inner tub face for anti-pullout collar
    translate([x_center, FRONT_NODE_WALL - collar_d, z_center])
        rotate([-90, 0, 0])
            cylinder(r=collar_r, h=collar_d + 1.0, center=false, $fn=36);
}

// Backwards-compatible alias for tub subtraction
module south_cable_comb_cutout(z_start = 0, h = 0) {
    south_round_cable_gland_cutout();
}

// 2. North Vehicle Cable Gland Cutout (in Tub North Wall, Y = 68.0 mm, X = 35.5 mm)
// Aligned directly with PCBA 05 J_VEHICLE (KiCad: X=127.50 mm, Y=75.42 mm)
module north_round_cable_gland_cutout(
    x_center = 35.5,
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 4.0, // Z = 9.5 mm
    bore_r   = 4.0, // Ø 8.0 mm bore for TPU boot
    collar_r = 5.2, // Ø 10.4 mm internal retention counterbore
    collar_d = 1.2
) {
    // A. Main pass-through cylindrical bore through North wall
    translate([x_center, FRONT_NODE_OUTER_W - FRONT_NODE_WALL - 1.0, z_center])
        rotate([-90, 0, 0])
            cylinder(r=bore_r, h=FRONT_NODE_WALL + 2.0, center=false, $fn=36);
            
    // B. Internal counterbore on inner tub face for anti-pullout collar
    translate([x_center, FRONT_NODE_OUTER_W - FRONT_NODE_WALL - 0.1, z_center])
        rotate([-90, 0, 0])
            cylinder(r=collar_r, h=collar_d + 0.1, center=false, $fn=36);
}

// Backwards-compatible alias for tub subtraction
module north_cable_comb_cutout(z_start = 0, h = 0) {
    north_round_cable_gland_cutout();
}

// 3. USB-C Service Port Cutout (East wall, X = 98.0 mm, Y = 24.1 mm, forward right flank)
module front_node_usbc_service_cutout(
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8,
    y_center = 24.1, // Aligned with J7 (KiCad: Y=104.93 on board -> Y_pcb = 15.07 mm + 9.0 mm tub offset = 24.07 mm)
    w = 10.5,
    h = 4.8
) {
    // A. Main pass-through rectangular bore through East wall
    translate([FRONT_NODE_OUTER_L - 7.0, y_center - w/2.0, z_center - h/2.0])
        cube(size=[8.0, w, h], center=false);
        
    // B. Recessed pocket for silicone dust plug collar (1.2 mm deep on outer East face)
    translate([FRONT_NODE_OUTER_L - 1.2, y_center - (w + 3.0)/2.0, z_center - (h + 3.0)/2.0])
        cube(size=[1.4, w + 3.0, h + 3.0], center=false);
}

// 4. Circular TPU Cable Gland Boot (Individual Component)
module front_node_tpu_cable_boot(
    cable_r   = 3.05, // Ø 6.1 mm tight fit on Ø 6.0 mm jacket cable
    bore_r    = 3.95, // Ø 7.9 mm snug fit in Ø 8.0 mm wall hole
    flange_r  = 5.0,  // Ø 10.0 mm retaining collar
    flange_w  = 1.4,  // Collar thickness
    groove_w  = 2.5,  // Wall snap groove (matching FRONT_NODE_WALL = 2.5 mm)
    boot_len  = 13.0  // Conical strain-relief extension length
) {
    color([0.15, 0.15, 0.15, 0.95]) // Black flexible TPU (Shore 85A/95A)
    difference() {
        union() {
            // A. Inner anti-pullout retaining flange
            cylinder(r=flange_r, h=flange_w, center=false, $fn=36);
            
            // B. Cylindrical wall pass-through section
            translate([0, 0, flange_w])
                cylinder(r=bore_r, h=groove_w, center=false, $fn=36);
                
            // C. Outer sealing ring / shoulder (locks against outer wall face)
            translate([0, 0, flange_w + groove_w])
                cylinder(r=flange_r, h=1.5, center=false, $fn=36);
                
            // D. Conical anti-kink strain-relief flex boot
            translate([0, 0, flange_w + groove_w + 1.5])
                cylinder(r1=flange_r, r2=cable_r + 1.0, h=boot_len, center=false, $fn=36);
                
            // E. Concentric anti-kink flex ribs along the boot cone
            for (z = [3.0, 6.5, 10.0]) {
                translate([0, 0, flange_w + groove_w + 1.5 + z])
                    cylinder(r1=cable_r + 1.6, r2=cable_r + 1.1, h=1.0, center=false, $fn=36);
            }
        }
        
        // Continuous central through-bore for the jacket cable
        translate([0, 0, -1.0])
            cylinder(r=cable_r, h=flange_w + groove_w + 1.5 + boot_len + 2.0, center=false, $fn=36);
    }
}

// 5. Printable Pair of TPU Cable Glands (Front Node)
module front_node_cable_glands_pair() {
    union() {
        // Cockpit Boot (South)
        translate([0, -8.0, 0])
            front_node_tpu_cable_boot();
            
        // Vehicle Boot (North)
        translate([0, 8.0, 0])
            front_node_tpu_cable_boot();
            
        // Breakaway 0.8 mm runner joining both boots for reliable build-plate adhesion
        translate([-1.5, -8.0, 0])
            cube(size=[3.0, 16.0, 0.8], center=false);
    }
}

// 6. Installed Boot Helpers for Assemblies
module front_node_south_cable_boot_installed() {
    translate([35.5, FRONT_NODE_WALL, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 4.0])
        rotate([90, 0, 0])
            front_node_tpu_cable_boot();
}

module front_node_north_cable_boot_installed() {
    translate([35.5, FRONT_NODE_OUTER_W - FRONT_NODE_WALL, FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + 4.0])
        rotate([-90, 0, 0])
            front_node_tpu_cable_boot();
}

// Backwards-compatible aliases for legacy assembly files
module south_epdm_cable_comb() {
    front_node_south_cable_boot_installed();
}

module north_epdm_cable_comb() {
    front_node_north_cable_boot_installed();
}

// Standalone render
front_node_cable_glands_pair();
