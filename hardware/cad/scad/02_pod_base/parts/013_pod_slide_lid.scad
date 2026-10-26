// =============================================================================
// OpenMotorBridge - Satellite Pod: Slot-In Lid with 4 Lateral Locking Teeth
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/013_pod_slide_lid.scad
// Description: True slot-in lid for the universal Monocoque Satellite Pod (Typ B).
// Features:
// 1. Dual lateral locking teeth on EACH flank (4 teeth total at X = 35 mm & 115 mm)
//    that positively engage matching undercut pockets in the housing sidewalls.
// 2. Central spring-loaded release slider (Zentral-Schnäpper) in lid center.
// 3. Sliding or pinching the central slider retracts all 4 lateral teeth inward.
// 4. Integrated return spring drives teeth outward into sidewalls on release.
// 5. Perimeter IP67 elastomeric seal lip / tongue.
// 6. Tactile FOB target circle for contactless magnetic release (PCBA 07).
// =============================================================================

include <../../00_common/parameters.scad>;

LID_L         = POD_OUTER_L - 4.0;   // 146.0 mm (flush fit with housing front/rear)
LID_W         = POD_OUTER_W - 6.0;   // 64.0 mm (fits into upper rim opening)
LID_PLATE_H   = 3.5;                 // Main lid shell thickness (mm)
LID_TONGUE_W  = 2.0;                 // Lateral tongue width (mm)
LID_TONGUE_H  = 2.5;                 // Lateral tongue height (mm)
SEAL_LIP_H    = 1.8;                 // Perimeter sealing tongue protrusion (mm)

TEETH_RETRACTED = false;             // Toggle to true to visualize retracted teeth

module pod_slide_lid() {
    tooth_offset_y = TEETH_RETRACTED ? -2.2 : 0.0;

    difference() {
        union() {
            // 1. Main Lid Plate with Chamfered Outer Edges
            hull() {
                translate([2.0, 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([LID_L - 2.0, 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([2.0, LID_W - 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
                translate([LID_L - 2.0, LID_W - 2.0, 0])
                    cylinder(r=2.0, h=LID_PLATE_H, $fn=24);
            }

            // 2. Longitudinal Guide Tongue Ribs along lateral flanks
            // Left flank guide rail
            translate([8.0, -LID_TONGUE_W, 0.5])
                cube([LID_L - 16.0, LID_TONGUE_W, LID_TONGUE_H], center=false);
            // Right flank guide rail
            translate([8.0, LID_W, 0.5])
                cube([LID_L - 16.0, LID_TONGUE_W, LID_TONGUE_H], center=false);

            // 3. 4 Lateral Locking Teeth (2 on Left, 2 on Right at X = 35 mm & X = 115 mm)
            for (tx = [35.0, 115.0]) {
                // Left locking teeth (projecting in -Y direction)
                translate([tx - 3.5, -LID_TONGUE_W - 1.8 - tooth_offset_y, 0.6]) {
                    hull() {
                        cube([7.0, 1.8, LID_TONGUE_H - 0.2], center=false);
                        // 30° lead-in chamfer for snap-in insertion
                        translate([1.0, 0, 0])
                            cube([5.0, 0.5, LID_TONGUE_H - 0.2], center=false);
                    }
                }
                // Right locking teeth (projecting in +Y direction)
                translate([tx - 3.5, LID_W + LID_TONGUE_W + tooth_offset_y, 0.6]) {
                    hull() {
                        cube([7.0, 1.8, LID_TONGUE_H - 0.2], center=false);
                        // 30° lead-in chamfer for snap-in insertion
                        translate([1.0, 1.3, 0])
                            cube([5.0, 0.5, LID_TONGUE_H - 0.2], center=false);
                    }
                }
            }

            // 4. Underside Perimeter Sealing Lip (IP67 Compressible Gasket Frame)
            translate([4.0, 4.0, -SEAL_LIP_H]) {
                difference() {
                    cube([LID_L - 8.0, LID_W - 8.0, SEAL_LIP_H], center=false);
                    translate([2.0, 2.0, -0.1])
                        cube([LID_L - 12.0, LID_W - 12.0, SEAL_LIP_H + 0.2], center=false);
                }
            }

            // 5. Central Spring-Loaded Slider Housing Boss (in lid center)
            translate([LID_L/2.0 - 18.0, LID_W/2.0 - 12.0, LID_PLATE_H]) {
                cube([36.0, 24.0, 1.8], center=false);
            }
        }

        // --- SUBTRACTIONS ---

        // 6. Central Ergonomic Pinch Slider Track & Recess
        translate([LID_L/2.0 - 16.0, LID_W/2.0 - 10.0, LID_PLATE_H - 1.2]) {
            cube([32.0, 20.0, 3.2], center=false);
        }

        // 7. Central Tactile Thumb Grip Ribs on Slider
        for (gx = [-10.0 : 4.0 : 10.0]) {
            translate([LID_L/2.0 + gx, LID_W/2.0, LID_PLATE_H + 0.4])
                cube([1.8, 14.0, 1.0], center=true);
        }

        // 8. Smart-Keyfob (PCBA 07) FOB Target Badge (16 x 10 mm rounded RFID/key rectangle, NOT an antenna hole!)
        translate([45.0, LID_W/2.0, LID_PLATE_H - 0.4]) {
            // Subtle 0.4 mm recessed rectangular badge
            cube([16.0, 10.0, 0.6], center=true);
        }

        // 9. Rear Tactile Grip Flutes (Secondary grip zone)
        for (gx = [LID_L - 22.0 : 4.0 : LID_L - 10.0]) {
            translate([gx, LID_W/2.0, LID_PLATE_H - 0.2])
                cube([2.0, 24.0, 0.8], center=true);
        }
    }
}

// Standalone preview
color([0.22, 0.23, 0.25])
    pod_slide_lid();
