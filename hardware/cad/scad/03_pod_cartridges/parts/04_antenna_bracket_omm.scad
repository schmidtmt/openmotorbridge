// =============================================================================
// OpenMotorBridge - Satellite Pod: OMM Transceiver Antenna Bracket
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/04_antenna_bracket_omm.scad
// Description: Parametric modular antenna carrier bracket for Pod 3.
//              Mounts in the rear chamber of the universal cartridge base sled
//              (X = 58.0 .. 112.0 mm) via the two rear corner posts.
//              Features:
//              1. Elevated top cradle for 18x18mm / 25x25mm GNSS patch antenna
//              2. Lateral vertical bed for 868 MHz LoRa FPC dipole antenna
//              3. Cable channels & strain relief for U.FL micro-coax leads
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;

module omm_antenna_bracket(
    bracket_l = 52.0,  // Length in X (X = 58.0 .. 110.0 mm in sled frame)
    bracket_w = 52.0,  // Width in Y (fits inside 53 mm sled bay)
    bracket_h = 20.0,  // Height in Z (reaches up to top lid)
    wall      = 2.0
) {
    difference() {
        union() {
            // 1. Base Plate & Floor Stiffeners (Z = 0 .. 2.5 mm)
            cube([bracket_l, bracket_w, 2.5], center=false);

            // 2. Dual Rear Fastening Ears (aligning with sled rear corner posts at X=51.0, Y=3.5 & Y=48.5)
            // Standoff ears with 2.8mm outer radius, h = 5.5 mm
            translate([bracket_l - 3.0, 3.5, 0])
                cylinder(r=4.0, h=5.5, center=false, $fn=24);
            translate([bracket_l - 3.0, bracket_w - 3.5, 0])
                cylinder(r=4.0, h=5.5, center=false, $fn=24);

            // 3. Elevated GNSS Ceramic Patch Antenna Tower & Cradle (Z = 2.5 .. bracket_h)
            // Centered in Y, positioned at X = 12.0 .. 42.0 mm
            translate([12.0, (bracket_w - 28.0)/2.0, 0]) {
                // Support A-frame columns
                cube([28.0, 28.0, bracket_h - 4.0], center=false);
                // Top cradle perimeter flange (Z = bracket_h - 4.0 .. bracket_h)
                translate([-1.0, -1.0, bracket_h - 4.0])
                    cube([30.0, 30.0, 4.0], center=false);
            }

            // 4. Lateral LoRa 868 MHz FPC Antenna Bed (Left vertical wall along Y = 0 .. 2.5 mm)
            translate([2.0, 0, 0])
                cube([bracket_l - 8.0, 2.5, 16.0], center=false);

            // Top retaining lip for LoRa FPC antenna
            translate([2.0, 0, 14.5])
                cube([bracket_l - 8.0, 3.5, 1.5], center=false);

            // 5. Center-to-Side Structural Ribs (Kreuzverrippung)
            translate([2.0, bracket_w/2.0 - 1.0, 0])
                cube([bracket_l - 6.0, 2.0, 6.0], center=false);
        }

        // --- SUBTRACTIONS (Clearances, pockets, bores) ---

        // A. 2x M2 Fastening Holes (Countersunk for M2 screws into rear sled posts)
        translate([bracket_l - 3.0, 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=7.0, center=false, $fn=20);
        translate([bracket_l - 3.0, bracket_w - 3.5, -0.5])
            cylinder(r=M2_SCREW_HOLE_R, h=7.0, center=false, $fn=20);

        // B. GNSS Ceramic Patch Antenna Pocket (25.5 x 25.5 x 3.5 mm deep at top face)
        translate([13.25, (bracket_w - 25.5)/2.0, bracket_h - 3.5])
            cube([25.5, 25.5, 4.0], center=false);

        // Nested 18.5 x 18.5 mm center pocket for compact patch antennas
        translate([16.75, (bracket_w - 18.5)/2.0, bracket_h - 5.0])
            cube([18.5, 18.5, 2.0], center=false);

        // Center through-hole for GNSS coaxial cable / pin feed (Ø 5.0 mm)
        translate([26.0, bracket_w/2.0, 0])
            cylinder(r=2.5, h=bracket_h + 1.0, center=false, $fn=20);

        // C. Lateral LoRa FPC Antenna Recessed Adhesive Channel (40 x 12 x 1.0 mm)
        translate([5.0, -0.1, 2.5])
            cube([bracket_l - 14.0, 1.2, 12.0], center=false);

        // LoRa Coax Exit Notch (at X = 4.0 mm)
        translate([2.0, -0.5, 2.5])
            cube([3.0, 4.0, 4.0], center=false);

        // D. Longitudinal Cable Channel (runs through floor for 2.4G coax to front/rear SMA)
        translate([-0.5, bracket_w/2.0 + 8.0, -0.5])
            cube([bracket_l + 2.0, 5.0, 2.0], center=false);

        // E. Weight Reduction Hollow Under GNSS Tower
        translate([15.0, (bracket_w - 22.0)/2.0, -0.5])
            cube([22.0, 22.0, bracket_h - 6.0], center=false);
    }
}

// Standalone printable preview
omm_antenna_bracket();
