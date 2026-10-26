// =============================================================================
// OpenMotorBridge - Satellite Pod: Monocoque Housing Tub (v10.0)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/parts/015_pod_monocoque_tub.scad
// Description: Monolithic PA12-MJF monocoque enclosure tub for the universal
//              Satellite Pod (Typ B). Eliminates all modular cassettes, sleds,
//              and ejection springs in favor of a direct two-zone architecture:
//
// 1. Lower Zone (X = 4..48 mm, Z = 3.5..14 mm):
//    - 4x M2.5 elastomeric damping standoffs (36.0 x 42.0 mm pitch) for PCBA 03.
//    - Front bulkhead Port A: M8 4-pin Bus socket (Z = 26.5 mm, Y = 35.0 mm).
//    - Front bulkhead Port B: Recessed 30W USB-C PD socket (Z = 11.5 mm, Y = 35.0 mm).
//    - Dry-Flap perimeter seating shelf at Z = 14.5 mm.
//
// 2. Upper Zone / Equipment Chamber (X = 48..144 mm, Z = 3.5..34 mm):
//    - Direct bed for OEM Intercoms (Cardo Packtalk Edge Air-Mount, Sena SPIDER,
//      OMM UCS, Midland PMR446) or 100% watertight Mini-Dry-Box.
//    - Integral mounting floor for Universal Dual-Actuator Slide Bracket
//      (012_universal_actuator_slide_bracket.scad).
//
// 3. Top Rim & Slide-In Lid Guides:
//    - Continuous longitudinal slide-in guide tracks (Z = 33.5 mm).
//    - Concealed FOB magnetic latch pocket and alignment ring.
//
// 4. Exterior Features:
//    - Bottom universal frame tube saddle (V-groove for Ø 18..35 mm tubes).
//    - 4x EPDM strap hook lugs on lower flanks.
//    - Ceiling Gore-Tex ePTFE breather vent.
// =============================================================================

include <../../00_common/parameters.scad>;
include <../../00_common/screw_bosses.scad>;
use <001_pod_rear_m8_gland.scad>;
use <005_pod_strap_hooks.scad>;

module pod_monocoque_tub() {
    port_yc   = POD_OUTER_W / 2.0;          // 35.0 mm (horizontally centered)
    port_a_zc = POD_OUTER_H / 2.0 + 7.5;    // 26.5 mm (upper: Port A Bus)
    port_b_zc = POD_OUTER_H / 2.0 - 7.5;    // 11.5 mm (lower: Port B USB-C)
    r_corner  = 3.5;

    difference() {
        union() {
            // 1. Monolithic 5-Sided Outer Hull with Rounded Corners
            hull() {
                translate([r_corner, r_corner, r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([POD_OUTER_L - r_corner, r_corner, r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([r_corner, POD_OUTER_W - r_corner, r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([POD_OUTER_L - r_corner, POD_OUTER_W - r_corner, r_corner])
                    sphere(r=r_corner, $fn=24);

                translate([r_corner, r_corner, POD_OUTER_H - r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([POD_OUTER_L - r_corner, r_corner, POD_OUTER_H - r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([r_corner, POD_OUTER_W - r_corner, POD_OUTER_H - r_corner])
                    sphere(r=r_corner, $fn=24);
                translate([POD_OUTER_L - r_corner, POD_OUTER_W - r_corner, POD_OUTER_H - r_corner])
                    sphere(r=r_corner, $fn=24);
            }

            // 2. 4x EPDM Strap Hook Lugs on Lower Flanks
            pod_strap_hook_lugs(
                length=POD_OUTER_L,
                width=POD_OUTER_W,
                hook_w=8.0,
                hook_out=3.0,
                hook_h=4.5
            );

            // 3. Port A: M8 Protective Collar on Bulkhead Wall (x = 0)
            pod_rear_m8_neck(
                collar_len=2.0,
                outer_size=16.0,
                inner_size=11.5,
                r_corner=1.5,
                yc=port_yc,
                zc=port_a_zc
            );

            // 4. Port B: Internal USB-C Housing Sleeve Boss (x = 0)
            pod_rear_usbc_internal_sleeve(
                depth=14.0,
                outer_w=17.0,
                outer_h=11.5,
                yc=port_yc,
                zc=port_b_zc
            );

            // 5. 4x PCBA 03 M2.5 Elastomer Damping Standoff Bosses (36.0 x 42.0 mm pitch)
            // PCBA 03 positioned at X = 6.0 .. 48.0 mm, Y = 11.0 .. 59.0 mm
            for (pos = [
                [6.0 + 3.0, 11.0 + 3.0],
                [6.0 + 3.0, 11.0 + 45.0],
                [6.0 + 39.0, 11.0 + 3.0],
                [6.0 + 39.0, 11.0 + 45.0]
            ]) {
                translate([pos[0], pos[1], POD_WALL])
                    cylinder(r=3.2, h=3.0, $fn=20);
            }

            // 6. Actuator Slide Bracket Mounting Bosses (in rear chamber)
            for (ax = [56.0, 140.0]) {
                translate([ax, 14.0, POD_WALL])
                    cylinder(r=3.0, h=2.5, $fn=20);
                translate([ax, POD_OUTER_W - 14.0, POD_WALL])
                    cylinder(r=3.0, h=2.5, $fn=20);
            }

            // 7. Dry-Flap Internal Seating Shelf Ledges
            translate([6.0, POD_WALL, 14.0])
                cube([46.0, 2.5, 2.0], center=false);
            translate([6.0, POD_OUTER_W - POD_WALL - 2.5, 14.0])
                cube([46.0, 2.5, 2.0], center=false);
            translate([50.0, POD_WALL, 14.0])
                cube([2.0, POD_OUTER_W - 2*POD_WALL, 2.0], center=false);

            // 7b. Optional Front SMA Bulkhead Reinforcement Boss (inner face at X = POD_OUTER_L - POD_WALL)
            translate([POD_OUTER_L - POD_WALL - 2.5, POD_OUTER_W/2.0, 19.0]) {
                rotate([0, 90, 0])
                    cylinder(r=7.0, h=2.5, center=false, $fn=24);
            }
        }

        // --- SUBTRACTIONS ---

        // 8. Main Internal Chamber (open at top for slide-in lid and device access)
        translate([POD_WALL, POD_WALL, POD_WALL]) {
            cube([
                POD_OUTER_L - 2*POD_WALL,
                POD_OUTER_W - 2*POD_WALL,
                POD_OUTER_H - POD_WALL + 0.5
            ], center=false);
        }
        // 9. Top Rim Continuous Slide-in Guide Grooves & Rear Entry Slot (Einschubschlitz)
        // Left guide groove (Y = POD_WALL - 1.6) runs from front stop (X = 6.0) all the way through rear wall (X = POD_OUTER_L + 1.0)
        translate([6.0, POD_WALL - 1.6, POD_OUTER_H - 4.5])
            cube([POD_OUTER_L - 5.0, 2.0, 3.2], center=false);
        // Right guide groove (Y = POD_OUTER_W - POD_WALL - 0.4)
        translate([6.0, POD_OUTER_W - POD_WALL - 0.4, POD_OUTER_H - 4.5])
            cube([POD_OUTER_L - 5.0, 2.0, 3.2], center=false);

        // Rear Slide-in Entry Opening (Lid slides in horizontally from rear along X)
        translate([POD_OUTER_L - POD_WALL - 0.5, POD_WALL - 1.6, POD_OUTER_H - 4.8])
            cube([POD_WALL + 2.0, POD_OUTER_W - 2*POD_WALL + 3.2, 5.0], center=false);

        // Internal FOB Anti-Theft Magnetic Latch Socket (100% INTERNAL - Zero outside access!)
        // Blind hole at X = 16.0 mm, Y = POD_OUTER_W/2 for the spring-loaded magnetic deadbolt
        translate([16.0, POD_OUTER_W/2.0, POD_OUTER_H - 9.0])
            cylinder(r=2.5, h=5.5, center=false, $fn=24);

        // 10. Port A: 4-Pin IP67 Magnet-Abrissschnittstelle (HytePro Style Bulkhead Pocket)
        // Rectangular flange pocket (15.0 x 8.0 mm) with silicone flat-cable internal passthrough
        translate([-1.0, port_yc - 7.5, port_a_zc - 4.0])
            cube([POD_WALL + 2.0, 15.0, 8.0], center=false);
        // 2x M2 Fixing Screws for Magnetic Bulkhead Flange
        for (sy = [port_yc - 9.5, port_yc + 9.5]) {
            translate([-1.0, sy, port_a_zc])
                rotate([0, 90, 0])
                    cylinder(r=1.1, h=POD_WALL + 2.0, $fn=16);
        }

        // 11. Port B: Recessed USB-C Vertical Socket Plug-Well & Seat
        pod_rear_usbc_pocket_tool(
            wall_th=18.0,
            pocket_depth=7.0,
            pocket_w=14.0,
            pocket_h=8.5,
            port_w=9.6,
            port_h=4.0,
            yc=port_yc,
            zc=port_b_zc
        );

        // 12. Bottom Universal Tube Saddle V-Groove Prism (for Frame Tubes Ø 18..35 mm)
        translate([-1.0, POD_OUTER_W/2.0, -14.0]) {
            rotate([0, 90, 0])
                cylinder(r=15.0, h=POD_OUTER_L + 2.0, $fn=36);
        }

        // 13. 4x M2.5 Screw Pilot Holes for PCBA 03
        for (pos = [
            [6.0 + 3.0, 11.0 + 3.0],
            [6.0 + 3.0, 11.0 + 45.0],
            [6.0 + 39.0, 11.0 + 3.0],
            [6.0 + 39.0, 11.0 + 45.0]
        ]) {
            translate([pos[0], pos[1], POD_WALL - 0.5])
                cylinder(r=M2_5_PILOT_HOLE_R, h=5.0, $fn=20);
        }

        // 14. 4x M2.5 Pilot Holes for Actuator Slide Bracket
        for (ax = [56.0, 140.0]) {
            translate([ax, 14.0, POD_WALL - 0.5])
                cylinder(r=M2_5_PILOT_HOLE_R, h=5.0, $fn=20);
            translate([ax, POD_OUTER_W - 14.0, POD_WALL - 0.5])
                cylinder(r=M2_5_PILOT_HOLE_R, h=5.0, $fn=20);
        }

        // 15. FOB Contactless Magnetic Latch Cavity (in lateral wall at X = 55 mm)
        translate([52.0, POD_WALL - 1.2, POD_OUTER_H - 12.0])
            cube([12.0, 3.5, 8.0], center=false);

        // 16. Transverse Zip-Tie Slots (5.0 x 2.5 mm) in Bottom Saddle
        translate([25.0 - 2.5, -1.0, POD_WALL - 1.2])
            cube([5.0, POD_OUTER_W + 2.0, 2.5], center=false);
        translate([POD_OUTER_L - 25.0 - 2.5, -1.0, POD_WALL - 1.2])
            cube([5.0, POD_OUTER_W + 2.0, 2.5], center=false);

        // 17. Optional Front SMA Bulkhead Antenna Port (at X = POD_OUTER_L) with 0.4 mm Knockout Membrane
        // Default state: 100% solid, sealed, airtight & leak-proof (IP68 / IP69K), identical to Central Box.
        // Total wall thickness with boss = POD_WALL + 2.5 = 5.0 mm.
        translate([POD_OUTER_L - POD_WALL - 2.5 - 0.1, POD_OUTER_W/2.0, 19.0]) {
            rotate([0, 90, 0]) {
                // Internal blind pilot bore leaving exact 0.4 mm solid membrane
                cylinder(r=SMA_BORE_R, h=5.0 - 1.2 - 0.4 + 0.1, center=false, $fn=32);
            }
        }
        // External O-ring recess (depth = 1.2 mm) from outside face inward
        translate([POD_OUTER_L - 1.2, POD_OUTER_W/2.0, 19.0]) {
            rotate([0, 90, 0]) {
                cylinder(r=SMA_ORECESS_R, h=1.2, center=false, $fn=32);
            }
        }
    }
}

// Standalone preview
color([0.28, 0.29, 0.32])
    pod_monocoque_tub();
