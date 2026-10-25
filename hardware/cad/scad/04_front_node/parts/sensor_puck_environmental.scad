// =============================================================================
// OpenMotorBridge - Front Node: Modular Snap-On Environmental Sensor Puck
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/sensor_puck_environmental.scad
// Description: Modular snap-on sensor cradle ("Körbchen") housing the external
//              environmental and positioning sensors:
//              1. u-blox SAM-M10Q Multi-GNSS module with sky zenith view.
//              2. TI TMP117 high-precision ambient thermometer in laminar airflow grill.
//              3. TI OPT3001 ambient light sensor with top optical aperture.
//              4. Knowles SPH0645 I2S MEMS acoustic sensor for AGC noise measurement.
//              Mounting modes:
//              - Bike Mode: Snaps directly onto Front Node upper lid via dual snap-arms.
//              - Automotive / Remote Mode: Unclips with one thumb press and docks onto
//                car dashboard / windshield wedge dock via 1.5 m JST-GH extension lead.
// =============================================================================

$fn = 32;

PUCK_L      = 44.0;   // Longitudinal length (mm)
PUCK_W      = 44.0;   // Transverse width (mm)
PUCK_H      = 15.0;   // Height (mm)
WALL_THICK  = 2.0;    // Wall thickness (mm)
R_PUCK      = 6.0;    // Smooth aerodynamic corner radius (mm)

// 1. Lower Puck Base & Sensor Cradle
module sensor_puck_cradle() {
    difference() {
        // Outer Squircle Aerodynamic Housing Body
        hull() {
            translate([R_PUCK, R_PUCK, 0])
                cylinder(r=R_PUCK, h=PUCK_H, center=false);
            translate([PUCK_L - R_PUCK, R_PUCK, 0])
                cylinder(r=R_PUCK, h=PUCK_H, center=false);
            translate([R_PUCK, PUCK_W - R_PUCK, 0])
                cylinder(r=R_PUCK, h=PUCK_H, center=false);
            translate([PUCK_L - R_PUCK, PUCK_W - R_PUCK, 0])
                cylinder(r=R_PUCK, h=PUCK_H, center=false);
        }

        // Inner Electronics Cavity for Sensor PCB
        translate([WALL_THICK, WALL_THICK, WALL_THICK]) {
            cube([PUCK_L - 2*WALL_THICK, PUCK_W - 2*WALL_THICK, PUCK_H + 1.0], center=false);
        }

        // Top Optical Light Port (Ø 4.5 mm aperture for TI OPT3001)
        translate([PUCK_L/2.0 - 10.0, PUCK_W/2.0, PUCK_H - 1.0])
            cylinder(r=2.25, h=3.0, center=false);

        // Front Laminar Airflow & Acoustic Grill (for TMP117 thermometer & Knowles MEMS)
        for (gz = [5.0, 8.0, 11.0]) {
            translate([WALL_THICK - 0.5, PUCK_W/2.0 - 8.0, gz])
                cube([WALL_THICK + 1.0, 16.0, 1.4], center=false);
        }

        // Rear Cable Notch (for 6-Pin JST-GH cable to Front Node J_SENSOR_EXT)
        translate([PUCK_L - WALL_THICK - 1.0, PUCK_W/2.0 - 6.0, 3.0])
            cube([WALL_THICK + 2.0, 12.0, 8.0], center=false);
    }

    // 4x Internal PCB Corner Rest Bosses (Z = 2.0 .. 4.5 mm)
    for (dx = [6.0, PUCK_L - 6.0]) {
        for (dy = [6.0, PUCK_W - 6.0]) {
            translate([dx - 1.5, dy - 1.5, WALL_THICK])
                cube([3.0, 3.0, 2.5], center=false);
        }
    }

    // Dual Bottom Snap-Fit Arms (Rastlaschen für werkzeuglose Front-Node Schnellmontage)
    translate([PUCK_L/2.0 - 8.0, -1.8, -4.5])
        cube([16.0, 2.0, 5.0], center=false);
    translate([PUCK_L/2.0 - 8.0, -2.6, -4.5])
        cube([16.0, 1.2, 2.0], center=false); // Catch barb 1

    translate([PUCK_L/2.0 - 8.0, PUCK_W - 0.2, -4.5])
        cube([16.0, 2.0, 5.0], center=false);
    translate([PUCK_L/2.0 - 8.0, PUCK_W + 1.4, -4.5])
        cube([16.0, 1.2, 2.0], center=false); // Catch barb 2
}

// 2. Translucent Optical / Protective Cap
module sensor_puck_cap() {
    difference() {
        hull() {
            translate([R_PUCK, R_PUCK, 0])
                cylinder(r=R_PUCK, h=2.5, center=false);
            translate([PUCK_L - R_PUCK, R_PUCK, 0])
                cylinder(r=R_PUCK, h=2.5, center=false);
            translate([R_PUCK, PUCK_W - R_PUCK, 0])
                cylinder(r=R_PUCK, h=2.5, center=false);
            translate([PUCK_L - R_PUCK, PUCK_W - R_PUCK, 0])
                cylinder(r=R_PUCK, h=2.5, center=false);
        }

        // Inner clearance rim
        translate([WALL_THICK + 0.3, WALL_THICK + 0.3, -1.0])
            cube([PUCK_L - 2*(WALL_THICK + 0.3), PUCK_W - 2*(WALL_THICK + 0.3), 2.5], center=false);

        // Center optical window
        translate([PUCK_L/2.0 - 10.0, PUCK_W/2.0, -0.5])
            cylinder(r=2.5, h=4.0, center=false);
    }
}

// 3. Complete Assembly Preview
module sensor_puck_environmental_assembly() {
    color([0.22, 0.24, 0.26])
        sensor_puck_cradle();

    color([0.7, 0.8, 0.9, 0.8])
        translate([0, 0, PUCK_H])
            sensor_puck_cap();
}

// Standalone execution preview
sensor_puck_environmental_assembly();
