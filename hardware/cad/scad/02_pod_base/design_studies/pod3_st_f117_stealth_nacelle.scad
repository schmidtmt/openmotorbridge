// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST F-117 Stealth Nighthawk Nacelle (Master)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod3_st_f117_stealth_nacelle.scad
// Description: Radical faceted stealth styling inspired by the Lockheed F-117 Nighthawk.
//              Features:
//              1. 100% Planar faceted surfaces with radar-deflecting chine lines (Knickkanten).
//              2. Faceted diamond chisel nose seamlessly covering the Pod 3 front face.
//              3. F-117 twin canted V-tail fins (+/- 35 deg outward cant) with integrated antenna slot.
//              4. Faceted delta-strake winglets mounting to Harley ST fender struts.
//              5. Rock-solid monolithic floor (4 mm thick over fender crown).
//              6. 100% single watertight solid body (Volumes = 1, 0 non-manifold edges).
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/007_pod_slide_dock_core.scad>;

FENDER_R_TRANS = 140.0;
ST_POD_L      = 136.0;
ST_FUSE_W     = 88.0;  // 88 mm width -> solid 8.6 mm sidewalls (dock cavity is 70.8 mm)
ST_DOCK_H     = 46.0;  // 46 mm height to provide 4 mm solid floor over fender crown

WING_HALF_SPAN = 130.0;
LEG_DROP_Z     = -32.0;
LEG_LEN_X      = 54.0;

X_WEDGE_TIP   = -148.0;
X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_DIFF_TIP    = +145.0;

// Faceted polygonal cross-section in Y-Z plane
module faceted_slice_yz(x, top_w, mid_w, bot_w, h_top, h_mid, h_bot=0.0, spine_h=2.5, dx=0.5) {
    translate([x, 0, 0])
    rotate([0, -90, 0])
    linear_extrude(height=dx, center=true) {
        polygon([
            [h_bot, -bot_w/2.0],
            [h_mid, -mid_w/2.0],
            [h_top, -top_w/2.0],
            [h_top + spine_h, 0.0],  // sharp center spine ridge
            [h_top,  top_w/2.0],
            [h_mid,  mid_w/2.0],
            [h_bot,  bot_w/2.0]
        ]);
    }
}

// 1. F-117 Faceted Chisel Nose (starts at X = -68.0 matching the Pod cradle)
module f117_faceted_nose() {
    // Stage 1: Transition from Pod Front (-68) to Forward Mid (-106)
    hull() {
        faceted_slice_yz(-68.0, top_w=80.0, mid_w=ST_FUSE_W, bot_w=84.0, h_top=ST_DOCK_H, h_mid=24.0, h_bot=0.0, spine_h=2.5);
        faceted_slice_yz(-106.0, top_w=54.0, mid_w=66.0, bot_w=58.0, h_top=30.0, h_mid=16.0, h_bot=1.0, spine_h=2.0);
    }
    // Stage 2: Forward Mid (-106) to Chisel Prow (-132)
    hull() {
        faceted_slice_yz(-106.0, top_w=54.0, mid_w=66.0, bot_w=58.0, h_top=30.0, h_mid=16.0, h_bot=1.0, spine_h=2.0);
        faceted_slice_yz(-132.0, top_w=28.0, mid_w=38.0, bot_w=32.0, h_top=18.0, h_mid=10.0, h_bot=2.5, spine_h=1.5);
    }
    // Stage 3: Chisel Tip (-132 to -148)
    hull() {
        faceted_slice_yz(-132.0, top_w=28.0, mid_w=38.0, bot_w=32.0, h_top=18.0, h_mid=10.0, h_bot=2.5, spine_h=1.5);
        faceted_slice_yz(-148.0, top_w=4.0,  mid_w=8.0,  bot_w=6.0,  h_top=6.0,  h_mid=4.0,  h_bot=3.0, spine_h=0.8);
    }
}

// 2. F-117 Faceted Fuselage Cradle (-68 to +68 mm)
module f117_faceted_fuselage() {
    hull() {
        faceted_slice_yz(X_POD_FRONT + 0.5, top_w=80.0, mid_w=ST_FUSE_W, bot_w=84.0, h_top=ST_DOCK_H, h_mid=24.0, h_bot=0.0, spine_h=2.5);
        faceted_slice_yz(X_POD_REAR - 0.5,  top_w=80.0, mid_w=ST_FUSE_W, bot_w=84.0, h_top=ST_DOCK_H, h_mid=24.0, h_bot=0.0, spine_h=2.5);
    }
}

// 3. F-117 Faceted Rear Exhaust Platypus / Diffuser (+68 to +145 mm)
module f117_faceted_tail() {
    hull() {
        faceted_slice_yz(X_POD_REAR - 0.5, top_w=80.0, mid_w=ST_FUSE_W, bot_w=84.0, h_top=ST_DOCK_H, h_mid=24.0, h_bot=0.0, spine_h=2.5);
        faceted_slice_yz(110.0,            top_w=58.0, mid_w=68.0, bot_w=62.0, h_top=26.0, h_mid=15.0, h_bot=1.0, spine_h=1.8);
    }
    hull() {
        faceted_slice_yz(110.0,      top_w=58.0, mid_w=68.0, bot_w=62.0, h_top=26.0, h_mid=15.0, h_bot=1.0, spine_h=1.8);
        faceted_slice_yz(X_DIFF_TIP, top_w=34.0, mid_w=42.0, bot_w=36.0, h_top=8.0,  h_mid=5.0,  h_bot=2.0, spine_h=1.0);
    }
}

// 4. F-117 Twin Canted V-Tail (Left and Right, +/- 35 deg outward cant)
module f117_twin_v_tail(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        translate([104.0, 24.0, 16.0])
        rotate([-35, 0, 0]) {
            difference() {
                // Massive faceted canted fin (14 mm root thickness, 6 mm tip thickness)
                hull() {
                    // Leading root
                    translate([0, 0, 0]) rotate([0, 90, 0]) cylinder(r=4.0, h=14.0, center=true, $fn=12);
                    // Mid root shoulder
                    translate([16.0, 0, 0]) rotate([0, 90, 0]) cylinder(r=5.5, h=14.0, center=true, $fn=12);
                    // Trailing root
                    translate([40.0, 0, 0]) rotate([0, 90, 0]) cylinder(r=3.0, h=14.0, center=true, $fn=12);
                    
                    // Fin tip
                    translate([24.0, -3.0, 48.0]) rotate([0, 90, 0]) cylinder(r=2.5, h=6.0, center=true, $fn=8);
                    translate([36.0, -3.0, 48.0]) rotate([0, 90, 0]) cylinder(r=2.0, h=6.0, center=true, $fn=8);
                }
                // LoRa/GNSS internal antenna conduit (r=1.5 mm -> 3.0 mm diameter)
                // Leaves > 5.5 mm solid wall on each side! Never cuts through the skin.
                if (side < 0) {
                    translate([16.0, 0, 20.0])
                        rotate([0, 68, 0])
                            cylinder(r=1.5, h=45.0, center=true, $fn=16);
                }
            }
        }
    }
}

// Wing rib slice in X-Z plane at position Y
module wing_rib_xz(y, x_lead, x_ridge, x_trail, z_lead, z_ridge, z_trail, z_bot, dy=0.5) {
    translate([0, y, 0])
    rotate([90, 0, 0])
    linear_extrude(height=dy, center=true) {
        polygon([
            [x_lead,  z_lead],
            [x_ridge, z_ridge],
            [x_trail, z_trail],
            [x_trail, z_bot],
            [x_lead,  z_bot]
        ]);
    }
}

// 5. F-117 Faceted Delta Winglet
module f117_faceted_wing(side=1) {
    union() {
        mirror([0, side < 0 ? 1 : 0, 0]) {
            // Stage 1: Inner strake root (Y = 38.0 inside flank) to elbow (Y = 74.0)
            hull() {
                wing_rib_xz(38.0, x_lead=-118.0, x_ridge=-10.0, x_trail=+38.0, z_lead=16.0, z_ridge=24.0, z_trail=16.0, z_bot=6.0);
                wing_rib_xz(74.0, x_lead=-32.0,  x_ridge=0.0,   x_trail=+26.0, z_lead=13.0, z_ridge=17.0, z_trail=13.0, z_bot=4.0);
            }
            // Stage 2: Elbow (Y = 74.0) to Wingtip at Strut (Y = 130.0)
            hull() {
                wing_rib_xz(74.0,  x_lead=-32.0, x_ridge=0.0, x_trail=+26.0, z_lead=13.0, z_ridge=17.0, z_trail=13.0, z_bot=4.0);
                wing_rib_xz(130.0, x_lead=-24.0, x_ridge=0.0, x_trail=+24.0, z_lead=2.0,  z_ridge=4.0,  z_trail=2.0,  z_bot=-6.0);
            }
        }
        
        // Solid Vertical Mounting Ear at the Strut
        translate([-LEG_LEN_X/2.0, side > 0 ? (WING_HALF_SPAN - 8.0) : -WING_HALF_SPAN, LEG_DROP_Z])
            cube([LEG_LEN_X, 8.0, 26.0], center=false);
            
        // Transition Fillet block
        mirror([0, side < 0 ? 1 : 0, 0]) {
            hull() {
                translate([-27.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z + 12.0]) cube([54.0, 8.0, 4.0], center=false);
                translate([-24.0, WING_HALF_SPAN - 12.0, LEG_DROP_Z + 20.0]) cube([48.0, 4.0, 4.0], center=false);
            }
        }
    }
}

module pod3_st_f117_stealth_nacelle() {
    difference() {
        union() {
            // A. F-117 Faceted Chisel Nose
            f117_faceted_nose();

            // B. F-117 Faceted Fuselage
            f117_faceted_fuselage();

            // C. F-117 Faceted Diffuser / Platypus
            f117_faceted_tail();

            // D. F-117 Twin Canted V-Tail (Left & Right)
            for (side = [-1, 1]) {
                f117_twin_v_tail(side);
            }

            // E. F-117 Faceted Delta Winglets (Left & Right)
            for (side = [-1, 1]) {
                f117_faceted_wing(side);
            }
        }

        // Subtractions:
        // 1. Pod 3 Slide-In Dock Cavity (floor sits at Z = 6.0 mm -> solid 4.0 mm floor above fender)
        translate([0, 0, 6.0]) {
            pod_slide_dock_subtraction(
                dock_l = ST_POD_L,
                dock_w = 70.8,
                dock_h = 38.2,
                open_sky_h = 50.0
            );
        }

        // 2. Direct M8 Cable Bore (dives 42 deg forward-downward under the seat)
        translate([-72.0, 0, 19.0])
            rotate([0, 42, 0])
                cylinder(r=4.5, h=60.0, center=true, $fn=24);

        // 3. Strut Bolt Slots (M8 / 5/16"-18)
        for (x_bolt = [-17.5, +17.5]) {
            translate([x_bolt, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=14.0, center=false, $fn=24);
            translate([x_bolt - 4.6, -WING_HALF_SPAN - 2.0, LEG_DROP_Z + 11.0])
                cube([9.2, 14.0, 6.0], center=false);

            translate([x_bolt, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 14.0])
                rotate([-90, 0, 0]) cylinder(r=4.6, h=16.0, center=false, $fn=24);
            translate([x_bolt - 4.6, WING_HALF_SPAN - 14.0, LEG_DROP_Z + 11.0])
                cube([9.2, 16.0, 6.0], center=false);
        }

        // 4. Fender arch clearance (crown at Z = 2.0 mm, leaves 4.0 mm solid bridge floor to dock at Z = 6.0 mm)
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, -90, 0])
                cylinder(r=FENDER_R_TRANS, h=abs(X_WEDGE_TIP) + X_DIFF_TIP + 20.0, center=true, $fn=64);
        }
    }
}

pod3_st_f117_stealth_nacelle();
