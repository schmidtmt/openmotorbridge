// =============================================================================
// OpenMotorBridge - Front Node: IP68 Multi-Port Flush TPU Plugs & Glands (v10.0)
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/005_cable_combs.scad
// Description: Flush, low-profile TPU sealing plugs (no protruding thorns/horns)
//              and tub cutouts for Front Node PCBA 05:
//              - Cockpit Wall (North, Y=68 mm): 3x Standard Oval Ports (CKPT 1, SENSOR, CKPT 2)
//              - Vehicle Wall (South, Y=0 mm):  2x Oval Ports (MAIN, DONGLE) +
//                                               3x Mini Ports (AUX 12V, NAV 12V, CAM 5V)
//              - Poka-Yoke debossed lettering on PA12 tub wall and TPU plugs.
// =============================================================================

include <../../00_common/parameters.scad>;

// -----------------------------------------------------------------------------
// 1. Port Cutouts for Tub Wall Subtraction
// -----------------------------------------------------------------------------

// Standard Oval U-Slot Cutout (11.0 mm wide x 8.1 mm high, below C-rail)
module front_node_oval_u_slot_cutout(
    x_center,
    y_wall,     // 0.0 for South, FRONT_NODE_OUTER_W for North
    z_bottom = 7.0,
    z_top    = 15.1,
    slot_w   = 11.0,
    collar_w = 13.0,
    collar_d = 1.2,
    wall_th  = 6.0, // FRONT_NODE_WALL + 3.5 mm inner sill
    is_north = false
) {
    h = z_top - z_bottom;
    r = (slot_w > 5.0) ? 2.5 : 1.5;
    y_dir = is_north ? -1.0 : 1.0;
    y_start = is_north ? y_wall + 1.0 : y_wall - 1.0;
    y_len = wall_th + 2.0;

    // A. Main pass-through slot
    translate([x_center - slot_w/2.0 + r, y_wall - (is_north ? wall_th + 1.0 : -1.0), z_bottom + r]) {
        // Hull for rounded bottom
        hull() {
            translate([0, 0, 0])
                rotate([-90, 0, 0])
                    cylinder(r=r, h=y_len, center=false, $fn=24);
            translate([slot_w - 2*r, 0, 0])
                rotate([-90, 0, 0])
                    cylinder(r=r, h=y_len, center=false, $fn=24);
            translate([0, 0, h - r])
                rotate([-90, 0, 0])
                    cylinder(r=r, h=y_len, center=false, $fn=24);
            translate([slot_w - 2*r, 0, h - r])
                rotate([-90, 0, 0])
                    cylinder(r=r, h=y_len, center=false, $fn=24);
        }
    }

    // B. Internal retention collar recess on inner chamber face
    c_r = r + 1.0;
    y_col_start = is_north ? (y_wall - wall_th - 0.1) : (y_wall + wall_th - collar_d);
    translate([x_center - collar_w/2.0 + c_r, y_col_start, z_bottom + r - 0.5]) {
        hull() {
            translate([0, 0, 0])
                rotate([-90, 0, 0])
                    cylinder(r=c_r, h=collar_d + 0.1, center=false, $fn=24);
            translate([collar_w - 2*c_r, 0, 0])
                rotate([-90, 0, 0])
                    cylinder(r=c_r, h=collar_d + 0.1, center=false, $fn=24);
            translate([0, 0, h - r + 0.5])
                rotate([-90, 0, 0])
                    cylinder(r=c_r, h=collar_d + 0.1, center=false, $fn=24);
            translate([collar_w - 2*c_r, 0, h - r + 0.5])
                rotate([-90, 0, 0])
                    cylinder(r=c_r, h=collar_d + 0.1, center=false, $fn=24);
        }
    }
}

// Mini U-Slot Cutout (6.5 mm wide x 7.6 mm high)
module front_node_mini_u_slot_cutout(
    x_center,
    y_wall,
    z_bottom = 7.5,
    z_top    = 15.1,
    slot_w   = 6.5,
    collar_w = 8.5,
    collar_d = 1.2,
    wall_th  = 6.0,
    is_north = false
) {
    front_node_oval_u_slot_cutout(
        x_center = x_center,
        y_wall   = y_wall,
        z_bottom = z_bottom,
        z_top    = z_top,
        slot_w   = slot_w,
        collar_w = collar_w,
        collar_d = collar_d,
        wall_th  = wall_th,
        is_north = is_north
    );
}

// -----------------------------------------------------------------------------
// 2. Combined Cutouts for Tub Lower Wall
// -----------------------------------------------------------------------------

// All Cockpit Ports on North Wall (Y = 68.0 mm)
module front_node_cockpit_ports_cutout() {
    y_north = FRONT_NODE_OUTER_W; // 68.0 mm
    
    // CKPT 1 (X = 35.5 mm): Oval Port for J_POD_R (29.5) + J_DISP_R (41.5)
    front_node_oval_u_slot_cutout(x_center = 35.5, y_wall = y_north, is_north = true);
    
    // SENSOR (X = 54.5 mm): Oval Port for J_SENSOR_EXT (54.5) to top puck
    front_node_oval_u_slot_cutout(x_center = 54.5, y_wall = y_north, is_north = true);
    
    // CKPT 2 (X = 73.0 mm): Oval Port for J_DISP_L (67.5) + J_POD_L (78.5)
    front_node_oval_u_slot_cutout(x_center = 73.0, y_wall = y_north, is_north = true);
}

// All Vehicle & Accessory Ports on South Wall (Y = 0.0 mm)
module front_node_vehicle_ports_cutout() {
    y_south = 0.0;
    
    // Port 1 [ MAIN ] (X = 34.5 mm): J1 Backbone (28.5) + J4 Hub (40.2)
    front_node_oval_u_slot_cutout(x_center = 34.5, y_wall = y_south, is_north = false);
    
    // Port 2 [ DONGLE ] (X = 52.0 mm): J_DONGLE (52.0)
    front_node_oval_u_slot_cutout(x_center = 52.0, y_wall = y_south, is_north = false);
    
    // Port 3 [ AUX 12V ] (X = 62.0 mm): J_AUX_LIGHT (62.0)
    front_node_mini_u_slot_cutout(x_center = 62.0, y_wall = y_south, is_north = false);
    
    // Port 4 [ NAV 12V ] (X = 70.25 mm): J10 Navi (70.25)
    front_node_mini_u_slot_cutout(x_center = 70.25, y_wall = y_south, is_north = false);
    
    // Port 5 [ CAM 5V ] (X = 78.25 mm): J8 Cam (78.25)
    front_node_mini_u_slot_cutout(x_center = 78.25, y_wall = y_south, is_north = false);
}

// All Cutouts Master Module
module front_node_all_ports_cutouts() {
    front_node_cockpit_ports_cutout();
    front_node_vehicle_ports_cutout();
}

// USB-C Service Port Cutout (East wall, X = 98.0 mm, Y = 24.1 mm)
module front_node_usbc_service_cutout(
    z_center = FRONT_NODE_WALL + FRONT_NODE_STANDOFF_H + FRONT_NODE_PCB_H + 1.8,
    y_center = 24.1,
    w = 10.5,
    h = 4.8
) {
    // Main pass-through rectangular bore through East wall
    translate([FRONT_NODE_OUTER_L - 7.0, y_center - w/2.0, z_center - h/2.0])
        cube(size=[8.0, w, h], center=false);
        
    // Recessed pocket for silicone dust plug collar (1.2 mm deep on outer East face)
    translate([FRONT_NODE_OUTER_L - 1.2, y_center - (w + 3.0)/2.0, z_center - (h + 3.0)/2.0])
        cube(size=[1.4, w + 3.0, h + 3.0], center=false);
}

// -----------------------------------------------------------------------------
// 3. Poka-Yoke Debossed Labels in Outer PA12 Tub Wall (0.5 mm deep)
// -----------------------------------------------------------------------------
module front_node_all_port_labels_deboss() {
    y_north = FRONT_NODE_OUTER_W; // 68.0 mm
    y_south = 0.0;
    z_lbl   = 16.2; // Above C-rail centerline, on upper tub rim
    depth   = 0.6;  // 0.6 mm debossed into PA12 wall

    // Cockpit Wall Labels (Facing North / Rider)
    translate([35.5, y_north - depth + 0.1, z_lbl])
        rotate([90, 0, 180])
            linear_extrude(height = depth + 0.2)
                text("CKPT 1", size = 2.0, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([54.5, y_north - depth + 0.1, z_lbl])
        rotate([90, 0, 180])
            linear_extrude(height = depth + 0.2)
                text("SENSOR", size = 2.0, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([73.0, y_north - depth + 0.1, z_lbl])
        rotate([90, 0, 180])
            linear_extrude(height = depth + 0.2)
                text("CKPT 2", size = 2.0, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    // Vehicle Wall Labels (Facing South / Vehicle Front)
    translate([34.5, -0.1, z_lbl])
        rotate([90, 0, 0])
            linear_extrude(height = depth + 0.2)
                text("MAIN", size = 2.0, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([52.0, -0.1, z_lbl])
        rotate([90, 0, 0])
            linear_extrude(height = depth + 0.2)
                text("DONGLE", size = 1.8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([62.0, -0.1, z_lbl])
        rotate([90, 0, 0])
            linear_extrude(height = depth + 0.2)
                text("AUX 12V", size = 1.4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([70.25, -0.1, z_lbl])
        rotate([90, 0, 0])
            linear_extrude(height = depth + 0.2)
                text("NAV 12V", size = 1.4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

    translate([78.25, -0.1, z_lbl])
        rotate([90, 0, 0])
            linear_extrude(height = depth + 0.2)
                text("CAM 5V", size = 1.4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
}

// -----------------------------------------------------------------------------
// 4. Low-Profile Flush TPU Inserts & Blind Plugs (0.0 mm Protrusion)
// -----------------------------------------------------------------------------

// Base Oval TPU Plug Body
module front_node_tpu_oval_body(
    slot_w   = 10.8, // 0.2 mm clearance for snug press-fit in 11.0 mm slot
    collar_w = 12.8,
    collar_d = 1.2,
    wall_th  = 6.0,
    z_bottom = 7.0,
    z_top    = 15.1,
    r        = 2.4
) {
    h = z_top - z_bottom; // 8.1 mm
    c_r = r + 0.9;
    
    translate([0, 0, z_bottom]) {
        // A. Wall Section (Flush with outer wall face Y = 0)
        translate([-slot_w/2.0 + r, 0, r]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=24);
                translate([slot_w - 2*r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=24);
                translate([0, 0, h - r]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=24);
                translate([slot_w - 2*r, 0, h - r]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=24);
            }
        }
        
        // B. Inner Retention Collar (locks inside chamber at Y = wall_th - collar_d)
        translate([-collar_w/2.0 + c_r, wall_th - collar_d, r - 0.4]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=24);
                translate([collar_w - 2*c_r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=24);
                translate([0, 0, h - r + 0.4]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=24);
                translate([collar_w - 2*c_r, 0, h - r + 0.4]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=24);
            }
        }
        
        // C. Subtle 0.5 mm Outer Flush Lip (prevents pushing too far into tub)
        translate([-slot_w/2.0 - 0.5 + r, -0.6, r - 0.3]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=24);
                translate([slot_w + 1.0 - 2*r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=24);
                translate([0, 0, h - r + 0.3]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=24);
                translate([slot_w + 1.0 - 2*r, 0, h - r + 0.3]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=24);
            }
        }
    }
}

// Flush Oval Blind Plug with Embossed Face
module front_node_tpu_oval_blind_plug(label_text = "DONGLE") {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_oval_body();
            // Debossed text on outer face
            translate([0, -0.6 - 0.1, 11.0])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.5)
                        text(label_text, size = 1.8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        }
    }
}

// Dual-Cable Gland Insert (e.g. for CKPT 1, CKPT 2, or MAIN Backbone+Hub)
module front_node_tpu_oval_dual_gland(cable_r1 = 1.8, cable_r2 = 1.8, slit_w = 0.4) {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_oval_body();
            
            // Cable bore 1 (left)
            translate([-2.6, -1.0, 11.0])
                rotate([-90, 0, 0])
                    cylinder(r=cable_r1, h=10.0, center=false, $fn=24);
            // Slit 1 to top
            translate([-2.6 - slit_w/2.0, -1.0, 11.0])
                cube([slit_w, 10.0, 5.0], center=false);

            // Cable bore 2 (right)
            translate([2.6, -1.0, 11.0])
                rotate([-90, 0, 0])
                    cylinder(r=cable_r2, h=10.0, center=false, $fn=24);
            // Slit 2 to top
            translate([2.6 - slit_w/2.0, -1.0, 11.0])
                cube([slit_w, 10.0, 5.0], center=false);
        }
    }
}

// Single-Cable Gland Insert (e.g. for J1 Backbone solo or single handlebar cable)
module front_node_tpu_oval_single_gland(cable_r = 2.8, slit_w = 0.4) {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_oval_body();
            
            // Center cable bore
            translate([0, -1.0, 11.0])
                rotate([-90, 0, 0])
                    cylinder(r=cable_r, h=10.0, center=false, $fn=24);
            // Slit to top
            translate([-slit_w/2.0, -1.0, 11.0])
                cube([slit_w, 10.0, 5.0], center=false);
        }
    }
}

// Sensor-Puck Ribbon Gland
module front_node_tpu_oval_sensor_gland(slot_w = 7.5, slot_th = 1.6) {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_oval_body();
            // Rectangular ribbon pass-through slot
            translate([-slot_w/2.0, -1.0, 11.0 - slot_th/2.0])
                cube([slot_w, 10.0, slot_th], center=false);
            // Top slit
            translate([-0.2, -1.0, 11.0])
                cube([0.4, 10.0, 5.0], center=false);
        }
    }
}

// Base Mini TPU Plug Body (6.3 mm wide x 7.4 mm high)
module front_node_tpu_mini_body(
    slot_w   = 6.3, // 0.2 mm clearance for 6.5 mm slot
    collar_w = 8.3,
    collar_d = 1.2,
    wall_th  = 6.0,
    z_bottom = 7.5,
    z_top    = 15.1,
    r        = 1.4
) {
    h = z_top - z_bottom;
    c_r = r + 0.8;
    
    translate([0, 0, z_bottom]) {
        // A. Wall Section
        translate([-slot_w/2.0 + r, 0, r]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=20);
                translate([slot_w - 2*r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=20);
                translate([0, 0, h - r]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=20);
                translate([slot_w - 2*r, 0, h - r]) rotate([-90, 0, 0]) cylinder(r=r, h=wall_th, $fn=20);
            }
        }
        
        // B. Inner Retention Collar
        translate([-collar_w/2.0 + c_r, wall_th - collar_d, r - 0.3]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=20);
                translate([collar_w - 2*c_r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=20);
                translate([0, 0, h - r + 0.3]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=20);
                translate([collar_w - 2*c_r, 0, h - r + 0.3]) rotate([-90, 0, 0]) cylinder(r=c_r, h=collar_d, $fn=20);
            }
        }
        
        // C. Subtle 0.5 mm Outer Flush Lip
        translate([-slot_w/2.0 - 0.4 + r, -0.6, r - 0.2]) {
            hull() {
                translate([0, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=20);
                translate([slot_w + 0.8 - 2*r, 0, 0]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=20);
                translate([0, 0, h - r + 0.2]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=20);
                translate([slot_w + 0.8 - 2*r, 0, h - r + 0.2]) rotate([-90, 0, 0]) cylinder(r=r, h=0.6, $fn=20);
            }
        }
    }
}

// Flush Mini Blind Plug with Embossed Label
module front_node_tpu_mini_blind_plug(label_text = "CAM") {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_mini_body();
            // Debossed text on outer face
            translate([0, -0.6 - 0.1, 11.2])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.5)
                        text(label_text, size = 1.6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        }
    }
}

// Mini Cable Gland Insert (e.g. for Cam 5V or Navi 12V cable)
module front_node_tpu_mini_cable_gland(cable_r = 1.5, label_text = "CAM", slit_w = 0.4) {
    color([0.15, 0.15, 0.15, 0.95]) {
        difference() {
            front_node_tpu_mini_body();
            
            // Center cable bore
            translate([0, -1.0, 11.2])
                rotate([-90, 0, 0])
                    cylinder(r=cable_r, h=10.0, center=false, $fn=24);
            // Slit to top
            translate([-slit_w/2.0, -1.0, 11.2])
                cube([slit_w, 10.0, 5.0], center=false);
                
            // Small label debossed above cable bore
            translate([0, -0.6 - 0.1, 13.8])
                rotate([90, 0, 0])
                    linear_extrude(height = 0.4)
                        text(label_text, size = 1.0, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        }
    }
}

// -----------------------------------------------------------------------------
// 5. Printable Complete Set of Front Node TPU Seals
// -----------------------------------------------------------------------------
module front_node_cable_glands_pair() {
    // Printable set: 3x Oval plugs + 3x Mini plugs laid flat on build plate (Z=0)
    union() {
        // Oval 1: DONGLE Blind Plug
        translate([-24.0, 0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_oval_blind_plug("DONGLE");
                
        // Oval 2: CKPT / Dual Cable Gland
        translate([0, 0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_oval_dual_gland();
                
        // Oval 3: MAIN / Single Cable Gland
        translate([24.0, 0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_oval_single_gland();

        // Mini 1: CAM Blind Plug
        translate([-20.0, 22.0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_mini_blind_plug("CAM");
                
        // Mini 2: NAV Blind Plug
        translate([0, 22.0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_mini_blind_plug("NAV");
                
        // Mini 3: AUX Blind Plug
        translate([20.0, 22.0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_mini_blind_plug("AUX");

        // Mini 4: CAM Cable Gland (for action cam use)
        translate([-10.0, 40.0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_mini_cable_gland(cable_r=1.5, label_text="CAM");

        // Mini 5: NAV Cable Gland (for navi use)
        translate([10.0, 40.0, 0])
            rotate([-90, 0, 0])
                front_node_tpu_mini_cable_gland(cable_r=1.8, label_text="NAV");
    }
}

// Backwards-compatible aliases for legacy assembly files
module south_round_cable_gland_cutout(x_center=35.5, z_center=9.5, bore_r=4.5, collar_r=6.0, z_top=15.1) {
    front_node_vehicle_ports_cutout();
}
module north_round_cable_gland_cutout(x_center=35.5, z_center=9.5, bore_r=4.5, collar_r=6.0, z_top=15.1) {
    front_node_cockpit_ports_cutout();
}
module front_node_south_cable_boot_installed() {
    translate([34.5, 0, 0]) front_node_tpu_oval_dual_gland();
    translate([52.0, 0, 0]) front_node_tpu_oval_blind_plug("DONGLE");
    translate([62.0, 0, 0]) front_node_tpu_mini_blind_plug("AUX");
    translate([70.25, 0, 0]) front_node_tpu_mini_blind_plug("NAV");
    translate([78.25, 0, 0]) front_node_tpu_mini_blind_plug("CAM");
}
module front_node_north_cable_boot_installed() {
    translate([35.5, FRONT_NODE_OUTER_W, 0]) rotate([0, 0, 180]) front_node_tpu_oval_dual_gland();
    translate([54.5, FRONT_NODE_OUTER_W, 0]) rotate([0, 0, 180]) front_node_tpu_oval_sensor_gland();
    translate([73.0, FRONT_NODE_OUTER_W, 0]) rotate([0, 0, 180]) front_node_tpu_oval_dual_gland();
}
module south_epdm_cable_comb() { front_node_south_cable_boot_installed(); }
module north_epdm_cable_comb() { front_node_north_cable_boot_installed(); }

// Standalone render
front_node_cable_glands_pair();
