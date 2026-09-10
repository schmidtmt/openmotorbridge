// =============================================================================
// OpenMotorBridge - Adventure Transition Dock (Sitzbank-Bügelfalten-Brücke)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_transition_dock.scad
// Description: Under-seat frame bridge dock for standard BMW GS (R1200/1250/1300 GS,
//              F750/850 GS, KTM, Africa Twin) without pannier luggage racks.
//              Mounts Pod 1 or Pod 2 precisely in the optical waist crease
//              between rider and passenger seats.
//              Features:
//              1. Contoured subframe saddle fitting Ø 22-32 mm frame tubes.
//              2. 100% pannier-independent: usable naked, with Vario or soft bags.
//              3. Positioned clear of rider boots and passenger footpegs.
//              4. Dual EPDM tension strap slots & M5 frame bolt tabs.
//              5. Outward-facing RF clearance with 0 dB shadowing.
// =============================================================================

include <../00_common/parameters.scad>;

// --- Parametric Dimensions ---
TD_POD_L            = 136.0; // Internal pod length clearance (mm)
TD_POD_W            = 71.0;  // Internal pod width clearance (mm)
TD_WALL             = 3.2;   // Wall thickness (mm)
TD_FLOOR            = 3.5;   // Floor thickness (mm)
TD_CRADLE_H         = 24.0;  // Half-height cradle for lean integration (mm)
TD_CORNER_R         = 4.0;   // Fillet radius (mm)

// Subframe tube interface & mounting tabs
TUBE_SADDLE_R       = 14.0;  // Subframe tube radius (Ø 28 mm typical)
MOUNT_TAB_L         = 24.0;  // Length of front/rear mounting tabs (mm)
MOUNT_TAB_THICK     = 4.5;   // Tab thickness (mm)
MOUNT_HOLE_R        = 2.8;   // M5 clearance hole (Ø 5.6 mm)

module td_rounded_box(l, w, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=h);
        translate([l-r, r, 0]) cylinder(r=r, h=h);
        translate([r, w-r, 0]) cylinder(r=r, h=h);
        translate([l-r, w-r, 0]) cylinder(r=r, h=h);
    }
}

module adventure_transition_dock() {
    difference() {
        union() {
            // 1. Main Pod Carrier Cradle
            td_rounded_box(TD_POD_L + 2*TD_WALL, TD_POD_W + 2*TD_WALL, TD_CRADLE_H, TD_CORNER_R);

            // 2. Front Subframe Mounting Tab (Bolts to seat bracket / frame tab)
            translate([-MOUNT_TAB_L, (TD_POD_W + 2*TD_WALL)/2.0 - 15.0, 0]) {
                hull() {
                    translate([TD_CORNER_R, TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([MOUNT_TAB_L + 5.0, TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([TD_CORNER_R, 30.0 - TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([MOUNT_TAB_L + 5.0, 30.0 - TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                }
            }

            // 3. Rear Subframe Mounting Tab
            translate([TD_POD_L + 2*TD_WALL - 5.0, (TD_POD_W + 2*TD_WALL)/2.0 - 15.0, 0]) {
                hull() {
                    translate([0, TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([MOUNT_TAB_L - TD_CORNER_R, TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([0, 30.0 - TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                    translate([MOUNT_TAB_L - TD_CORNER_R, 30.0 - TD_CORNER_R, 0]) cylinder(r=TD_CORNER_R, h=MOUNT_TAB_THICK);
                }
            }

            // 4. Underside Subframe Tube Saddles (Form-fit rest for frame tubes)
            translate([TD_WALL + 20.0, -4.0, -10.0])
                cube([25.0, TD_POD_W + 2*TD_WALL + 8.0, 12.0]);
            translate([TD_POD_L - 35.0, -4.0, -10.0])
                cube([25.0, TD_POD_W + 2*TD_WALL + 8.0, 12.0]);
        }

        // --- SUBTRACTIONS ---

        // A. Internal Pod Chamber Pocket
        translate([TD_WALL, TD_WALL, TD_FLOOR])
            cube([TD_POD_L, TD_POD_W, TD_CRADLE_H + 5.0]);

        // Open front throat for quick-release cartridge sliding
        translate([-1.0, TD_WALL + 5.0, TD_FLOOR])
            cube([TD_WALL + 2.0, TD_POD_W - 10.0, TD_CRADLE_H + 5.0]);

        // B. Mounting Holes on Front and Rear Tabs (M5 with washer recesses)
        translate([-MOUNT_TAB_L/2.0, (TD_POD_W + 2*TD_WALL)/2.0, -1.0]) {
            cylinder(r=MOUNT_HOLE_R, h=MOUNT_TAB_THICK + 2.0);
            translate([0, 0, MOUNT_TAB_THICK - 1.5])
                cylinder(r=5.5, h=3.0); // Washer recess
        }
        translate([TD_POD_L + 2*TD_WALL + MOUNT_TAB_L/2.0 - 5.0, (TD_POD_W + 2*TD_WALL)/2.0, -1.0]) {
            cylinder(r=MOUNT_HOLE_R, h=MOUNT_TAB_THICK + 2.0);
            translate([0, 0, MOUNT_TAB_THICK - 1.5])
                cylinder(r=5.5, h=3.0);
        }

        // C. Subframe Tube Hohlkehlen (Concave saddle cuts on bottom)
        translate([TD_WALL + 32.5, -10.0, -10.0])
            rotate([-90, 0, 0])
                cylinder(r=TUBE_SADDLE_R, h=TD_POD_W + 2*TD_WALL + 20.0);

        translate([TD_POD_L - 22.5, -10.0, -10.0])
            rotate([-90, 0, 0])
                cylinder(r=TUBE_SADDLE_R, h=TD_POD_W + 2*TD_WALL + 20.0);

        // D. Dual Heavy-Duty EPDM Strap / Zip-Tie Channels
        for (strap_x = [TD_WALL + 32.5, TD_POD_L - 22.5]) {
            translate([strap_x - 3.0, -1.0, TD_FLOOR + 1.5])
                cube([6.0, TD_POD_W + 2*TD_WALL + 2.0, 3.2]);
        }

        // E. Underside M8 Harness Pass-Through Slot (Routes under seat to battery)
        translate([TD_POD_L - 5.0, (TD_POD_W + 2*TD_WALL)/2.0, -12.0])
            hull() {
                cylinder(r=5.5, h=20.0);
                translate([0, -15.0, 0]) cylinder(r=5.5, h=20.0);
            }
    }
}

// Standalone render
adventure_transition_dock();
