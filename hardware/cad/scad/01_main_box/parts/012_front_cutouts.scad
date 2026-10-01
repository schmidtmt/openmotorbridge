// =============================================================================
// OpenMotorBridge - Main Box: Front Face & Antenna Cutout Tools
// =============================================================================
// File: hardware/cad/scad/01_main_box/parts/012_front_cutouts.scad
// Description: Parametric interface cutouts for the Central Box Oberwanne:
//              1. Deutsch DTM-12 automotive connector flange (J1).
//              2. IP67 waterproof USB-C service port with threaded cap.
//              3. Hardware SW1 button (Pair / Reset) with rubber boot.
//              4. WS2812B RGB Status LED light pipe window (Ø 3.2 mm).
//              5. Optional rear SMA antenna bulkhead port (Ø 6.5 mm with O-ring seat)
//                 for external high-gain LoRa 868 MHz rally antenna.
// =============================================================================

include <../../00_common/parameters.scad>;

module main_box_front_cutout_tool(wall_th=5.0) {
    // Height center along Z: Mid tray height is 15.0 mm. Center is at Z = 7.5 mm.
    z_mid = 7.5;

    // 1. IP67 USB-C Waterproof Panel Port (at X = 24.0 mm)
    // Round threaded barrel Ø 11.0 mm with flat indexing
    translate([24.0, -1.0, z_mid])
        rotate([-90, 0, 0])
            cylinder(r=5.5, h=wall_th + 2.0, center=false, $fn=32);

    // 2. WS2812B RGB Status LED Light Pipe Window (at X = 42.0 mm)
    // Ø 3.2 mm bore for diffuse PMMA light pipe with sealing O-ring
    translate([42.0, -1.0, z_mid])
        rotate([-90, 0, 0])
            cylinder(r=1.6, h=wall_th + 2.0, center=false, $fn=24);

    // 3. Hardware SW1 Push-Button (Pair / Reset at X = 54.0 mm)
    // Ø 6.5 mm bore for waterproof IP67 miniature tactile button with silicone boot
    translate([54.0, -1.0, z_mid])
        rotate([-90, 0, 0])
            cylinder(r=3.25, h=wall_th + 2.0, center=false, $fn=28);

    // 4. Automotive Deutsch DTM-12 Header Cutout (centered at X = 80.0 mm)
    // Rectangular pass-through 26.0 x 12.0 mm for 12-pin automotive sealed plug
    translate([80.0, wall_th/2.0, z_mid])
        cube([26.0, wall_th + 2.0, 12.0], center=true);

    // 2x M3 Flange Fastening Holes for DTM-12 (Pitch = 36.0 mm: X = 62.0 and 98.0 mm)
    for (dx = [-18.0, 18.0]) {
        translate([80.0 + dx, -1.0, z_mid])
            rotate([-90, 0, 0])
                cylinder(r=M3_SCREW_HOLE_R, h=wall_th + 2.0, center=false, $fn=24);
    }
}

// Module for Optional Rear SMA Antenna Bulkhead Port (for external LoRa 868 MHz antenna)
module main_box_rear_antenna_cutout_tool(length=110.0, width=74.0, wall_th=5.0) {
    z_mid = 7.5;
    // Positioned at rear wall (Y = width) near SX1262 LoRa module (X = 85.0 mm)
    translate([85.0, width + 1.0, z_mid]) {
        rotate([90, 0, 0]) {
            // Ø 6.5 mm through-bore for SMA bulkhead thread
            cylinder(r=SMA_BORE_R, h=wall_th + 2.0, center=false, $fn=32);
            // Ø 9.5 mm x 1.2 mm O-ring sealing counterbore on outer face
            cylinder(r=SMA_ORECESS_R, h=SMA_ORECESS_DEPTH + 1.0, center=false, $fn=32);
        }
    }
}

// Standalone preview
main_box_front_cutout_tool();
