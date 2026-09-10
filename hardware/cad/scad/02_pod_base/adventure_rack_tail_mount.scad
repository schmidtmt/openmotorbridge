// =============================================================================
// OpenMotorBridge - Adventure Rack-Tail Mount ("Heck-Balkon" für Reiseenduros)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/adventure_rack_tail_mount.scad
// Description: Cantilever luggage rack extension bracket for BMW R1250/1300 GS/GSA,
//              KTM Adventure and Africa Twin.
//              Features:
//              1. Rigid mounting flange clamping to luggage rack / M6 base plate.
//              2. 65 mm cantilever tray holding Pod 3 clear behind aluminum topcase.
//              3. 100% full topcase lid opening and quick-release preservation.
//              4. Unoccluded 140° zenith sky view for u-blox MAX-M10S GNSS & LoRa.
//              5. 45° deflector wedge (Astabweiser) shielding +5 dBi 2.4 GHz antenna.
//              6. Underside M5 GoPro swivel hinge for Garmin Varia mmWave radar.
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/011_gopro_hirth_lock.scad>;

// --- Parametric Dimensions ---
RTM_POD_L           = 136.5; // Internal pocket length for Pod 3 (mm)
RTM_POD_W           = 71.5;  // Internal pocket width (mm)
RTM_WALL            = 3.5;   // Heavy-duty PA12-CF wall thickness (mm)
RTM_FLOOR           = 4.0;   // Solid bottom floor thickness (mm)
RTM_RIM_H           = 18.0;  // Lateral retaining rim height (mm)
RTM_CORNER_R        = 4.0;   // Outer fillet radius (mm)

// Cantilever extension & rack mounting flange
RTM_CANTILEVER_X    = 68.0;  // Rearward overhang behind topcase wall (mm)
RTM_FLANGE_L        = 55.0;  // Forward mounting flange length (mm)
RTM_FLANGE_W        = 110.0; // Flange width across rack (mm)
RTM_FLANGE_THICK    = 6.0;   // Heavy-duty mounting flange thickness (mm)
RTM_SLOT_SPACING_Y  = 80.0;  // M6 mounting slot lateral center distance (mm)
RTM_TUBE_DIA        = 18.2;  // Luggage rack tube cradle diameter (mm)

// Astabweiser (45° Deflector Fin) on rear edge
FIN_BASE_L          = 28.0;  // Length of deflector fin along X (mm)
FIN_WIDTH           = 22.0;  // Width of deflector fin along Y (mm)
FIN_HEIGHT          = 32.0;  // Height of deflector wedge in Z (mm)
ANTENNA_BORE_DIA    = 10.5;  // Snap-in groove for +5 dBi dipole antenna (mm)

// Radar hinge on underside
RADAR_DROP_Z        = 22.0;  // Drop below bottom plate for radar hinge (mm)
RADAR_LUG_THICK     = 4.0;   // GoPro dual-lug thickness (mm)
RADAR_LUG_GAP       = 6.2;   // Gap between lugs for standard GoPro tongue (mm)

module rtm_rounded_rect(l, w, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=h);
        translate([l-r, r, 0]) cylinder(r=r, h=h);
        translate([r, w-r, 0]) cylinder(r=r, h=h);
        translate([l-r, w-r, 0]) cylinder(r=r, h=h);
    }
}

module adventure_rack_tail_mount() {
    difference() {
        union() {
            // 1. Forward Luggage Rack Clamping Flange
            translate([-RTM_FLANGE_L, -(RTM_FLANGE_W - (RTM_POD_W + 2*RTM_WALL))/2.0, 0]) {
                hull() {
                    translate([RTM_CORNER_R, RTM_CORNER_R, 0])
                        cylinder(r=RTM_CORNER_R, h=RTM_FLANGE_THICK);
                    translate([RTM_FLANGE_L - RTM_CORNER_R, RTM_CORNER_R, 0])
                        cylinder(r=RTM_CORNER_R, h=RTM_FLANGE_THICK);
                    translate([RTM_CORNER_R, RTM_FLANGE_W - RTM_CORNER_R, 0])
                        cylinder(r=RTM_CORNER_R, h=RTM_FLANGE_THICK);
                    translate([RTM_FLANGE_L - RTM_CORNER_R, RTM_FLANGE_W - RTM_CORNER_R, 0])
                        cylinder(r=RTM_CORNER_R, h=RTM_FLANGE_THICK);
                }
            }

            // Stiffening Gussets between Flange and Cradle
            hull() {
                translate([-25.0, -10.0, 0]) cube([30.0, 10.0, RTM_FLANGE_THICK]);
                translate([5.0, 0, 0]) cube([15.0, 6.0, RTM_RIM_H]);
            }
            hull() {
                translate([-25.0, RTM_POD_W + 2*RTM_WALL, 0]) cube([30.0, 10.0, RTM_FLANGE_THICK]);
                translate([5.0, RTM_POD_W + 2*RTM_WALL - 6.0, 0]) cube([15.0, 6.0, RTM_RIM_H]);
            }

            // 2. Main Cantilever Cradle Body (Holds Pod 3 horizontal)
            rtm_rounded_rect(RTM_POD_L + 2*RTM_WALL, RTM_POD_W + 2*RTM_WALL, RTM_RIM_H, RTM_CORNER_R);

            // 3. 45° Astabweiser-Finne (Trailing edge deflector wedge for 2.4 GHz antenna)
            translate([RTM_POD_L + 2*RTM_WALL - 2.0, (RTM_POD_W + 2*RTM_WALL - FIN_WIDTH)/2.0, 0]) {
                hull() {
                    // Base transition
                    cube([4.0, FIN_WIDTH, RTM_RIM_H]);
                    // Angled deflector crest
                    translate([FIN_BASE_L, 0, 0])
                        cube([4.0, FIN_WIDTH, RTM_RIM_H + FIN_HEIGHT]);
                }
            }

            // 4. Underside M5 GoPro-Style Swivel Hinge for Garmin Varia mmWave Radar (Lateral pitch axis)
            translate([RTM_POD_L/2.0 + RTM_WALL, (RTM_POD_W + 2*RTM_WALL)/2.0, 0]) {
                // Central mounting pillar transition
                translate([-12.0, -14.0, -RADAR_DROP_Z + 6.0])
                    cube([24.0, 28.0, RADAR_DROP_Z - 5.0]);

                // Left lug (at -Y)
                translate([0, -RADAR_LUG_GAP/2.0 - RADAR_LUG_THICK, -RADAR_DROP_Z]) {
                    rotate([-90, 0, 0])
                        cylinder(r=8.0, h=RADAR_LUG_THICK);
                    translate([-8.0, 0, 0])
                        cube([16.0, RADAR_LUG_THICK, 7.0]);
                }

                // Right lug (at +Y)
                translate([0, RADAR_LUG_GAP/2.0, -RADAR_DROP_Z]) {
                    rotate([-90, 0, 0])
                        cylinder(r=8.0, h=RADAR_LUG_THICK);
                    translate([-8.0, 0, 0])
                        cube([16.0, RADAR_LUG_THICK, 7.0]);
                }
            }
        }

        // --- SUBTRACTIONS (Cavities, bores, slots, cable tunnels) ---

        // A. Pod 3 Main Cavity (Pocket with form-fit clearance)
        translate([RTM_WALL, RTM_WALL, RTM_FLOOR])
            cube([RTM_POD_L, RTM_POD_W, RTM_RIM_H + 5.0]);

        // Front slide opening for M8 cable & cassette insertion
        translate([-1.0, RTM_WALL + 6.0, RTM_FLOOR])
            cube([RTM_WALL + 2.0, RTM_POD_W - 12.0, RTM_RIM_H + 5.0]);

        // B. Forward Flange M6 Slotted Holes (for Rack adjustment)
        for (offset_y = [-RTM_SLOT_SPACING_Y/2.0, RTM_SLOT_SPACING_Y/2.0]) {
            translate([-RTM_FLANGE_L/2.0, (RTM_POD_W + 2*RTM_WALL)/2.0 + offset_y, -1.0]) {
                hull() {
                    translate([-8.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0); // Ø 6.6 mm slot
                    translate([8.0, 0, 0]) cylinder(r=3.3, h=RTM_FLANGE_THICK + 2.0);
                }
                // Counterbore for M6 socket head bolt DIN 912
                hull() {
                    translate([-8.0, 0, RTM_FLANGE_THICK - 2.5]) cylinder(r=5.5, h=4.0);
                    translate([8.0, 0, RTM_FLANGE_THICK - 2.5]) cylinder(r=5.5, h=4.0);
                }
            }
        }

        // C. Rack Tube V-Groove / Cradle underneath flange (Ø 18 mm tube nest)
        translate([-RTM_FLANGE_L/2.0, -25.0, -1.0])
            rotate([-90, 0, 0])
                cylinder(r=RTM_TUBE_DIA/2.0, h=RTM_FLANGE_W + 50.0);

        // D. Astabweiser Internal Antenna Channel & Snap Slot
        translate([RTM_POD_L + 2*RTM_WALL - 5.0, (RTM_POD_W + 2*RTM_WALL)/2.0, 0]) {
            // Diagonal antenna bore inside wedge
            translate([FIN_BASE_L/2.0, 0, (RTM_RIM_H + FIN_HEIGHT)/2.0])
                rotate([0, -35, 0]) {
                    cylinder(r=ANTENNA_BORE_DIA/2.0, h=50.0, center=true);
                    // Lateral snap slot
                    translate([0, -1.5, -25.0])
                        cube([ANTENNA_BORE_DIA, 3.0, 50.0]);
                }

            // Hidden coaxial passage into Pod 3 chamber
            translate([-8.0, 0, RTM_FLOOR + 4.0])
                rotate([0, 90, 0])
                    cylinder(r=2.5, h=20.0); // RG178/U.FL pass-through
        }

        // E. Underside GoPro Hinge Gap, M5 Through-Bore & Hirth Rosettes
        translate([RTM_POD_L/2.0 + RTM_WALL, (RTM_POD_W + 2*RTM_WALL)/2.0, 0]) {
            // Gap clearance between lugs
            translate([-10.0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z - 10.0])
                cube([20.0, RADAR_LUG_GAP, RADAR_DROP_Z + 2.0]);

            // M5 through-bore along Y (lateral pivot axis)
            translate([0, 0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=2.7, h=36.0, center=true);

            // M5 hexagonal stop nut pocket on right lug
            translate([0, RADAR_LUG_GAP/2.0 + RADAR_LUG_THICK - 2.4, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    cylinder(r=4.6, h=3.0, $fn=6);

            // Form-Fit Radial Hirth Rosette Subtractions (10°-Schritt Formschluss)
            // Left lug inner face (Y = -RADAR_LUG_GAP/2.0)
            translate([0, -RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([90, 0, 0])
                    gopro_hirth_subtraction_tool();

            // Right lug inner face (Y = RADAR_LUG_GAP/2.0)
            translate([0, RADAR_LUG_GAP/2.0, -RADAR_DROP_Z])
                rotate([-90, 0, 0])
                    gopro_hirth_subtraction_tool();
        }

        // F. Concealed M8 Cable Channel on Underbelly
        translate([15.0, (RTM_POD_W + 2*RTM_WALL)/2.0, -0.5]) {
            hull() {
                cylinder(r=5.0, h=RTM_FLOOR + 1.0); // Cable drop opening into Pod 3 Port A
                translate([-35.0, 0, 0]) cylinder(r=5.0, h=RTM_FLOOR + 1.0);
            }
        }

        // G. EPDM Tension Band Slots (2x lateral tie-down slots)
        for (slot_x = [30.0, RTM_POD_L - 25.0]) {
            translate([slot_x, -1.0, RTM_FLOOR + 2.0])
                cube([6.0, RTM_POD_W + 2*RTM_WALL + 2.0, 3.0]);
        }
    }
}

// Standalone render
adventure_rack_tail_mount();
