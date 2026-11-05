// =============================================================================
// OpenMotorBridge - Front Node: Modular Snap-On Environmental Sensor Puck
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/sensor_puck_environmental.scad
// Description: Modular snap-on sensor cradle ("Körbchen") housing PCBA 05D
//              (34.0 x 34.0 mm) with exact 1:1 sensor and mounting parity:
//              1. u-blox SAM-M10Q Multi-GNSS patch module with unobstructed zenith sky view.
//              2. TI TMP117 high-precision thermometer on thermally isolated PCB island
//                 with direct laminar airflow ventilation slots on flank.
//              3. TI OPT3001 ambient light luxmeter with top optical aperture.
//              4. 3x M2 mounting screw bosses (H1, H2, H3) matching KiCad PCB.
//              5. Rear notch for 6-pin JST-GH cable to Front Node J_SENSOR_EXT.
//              Mounting modes:
//              - Bike Mode: Snaps directly onto Front Node upper lid via dual snap-arms.
//              - Remote Mode: Unclips with one thumb press and docks onto dashboard /
//                windshield wedge dock via JST-GH extension lead.
// =============================================================================

$fn = 32;

// --- Physical Puck Outer Envelope (Form-fit with Front Node lid snap slots) ---
PUCK_L          = 44.0;   // Outer longitudinal length (mm)
PUCK_W          = 44.0;   // Outer transverse width (mm)
PUCK_H          = 15.0;   // Total cradle height (mm)
WALL_THICK      = 2.0;    // Structural wall thickness (mm)
FLOOR_THICK     = 2.0;    // Bottom floor thickness (mm)
R_PUCK          = 6.0;    // Aerodynamic corner radius (mm)

// --- PCBA 05D Physical Parameters (KiCad openmotorbridge_sensor_puck.kicad_pcb) ---
PCB_L           = 34.0;   // PCB length (mm)
PCB_W           = 34.0;   // PCB width (mm)
PCB_T           = 1.6;    // FR4 substrate thickness (mm)
PCB_CLR         = 0.4;    // Internal clearance (mm)
STANDOFF_H      = 2.5;    // Standoff height under PCB (mm)

// Centered PCB origin inside 44 x 44 mm housing:
PCB_X0          = (PUCK_L - PCB_L) / 2.0; // 5.0 mm
PCB_Y0          = (PUCK_W - PCB_W) / 2.0; // 5.0 mm

// --- Exact Component Positions (from KiCad PCB coordinates) ---
// 1. OPT3001 Ambient Light Sensor U3 at (18.35, 5.61) on PCB
OPT_X           = PCB_X0 + 18.35; // 23.35 mm
OPT_Y           = PCB_Y0 + 5.61;  // 10.61 mm

// 2. TMP117 Temperature Sensor U2 at (5.0, 7.0) on PCB (thermal island)
TMP_X           = PCB_X0 + 5.0;   // 10.0 mm
TMP_Y           = PCB_Y0 + 7.0;   // 12.0 mm

// 3. J1 JST-GH 6-Pin Connector at (30.15, 18.28) facing +X
J1_X            = PCB_X0 + 30.15; // 35.15 mm
J1_Y            = PCB_Y0 + 18.28; // 23.28 mm

// 4. 3x M2 Mounting Holes: H1 (3.5, 30.5), H2 (30.5, 30.5), H3 (30.5, 3.5)
BOSS_LIST = [
    [PCB_X0 + 3.5,  PCB_Y0 + 30.5], // H1: (8.5, 35.5)
    [PCB_X0 + 30.5, PCB_Y0 + 30.5], // H2: (35.5, 35.5)
    [PCB_X0 + 30.5, PCB_Y0 + 3.5]   // H3: (35.5, 8.5)
];

// -----------------------------------------------------------------------------
// 1. Lower Puck Base & Sensor Cradle
// -----------------------------------------------------------------------------
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

        // Inner Electronics Cavity for PCBA 05D (clears 34.0 x 34.0 mm PCB + components)
        translate([WALL_THICK, WALL_THICK, FLOOR_THICK]) {
            cube([PUCK_L - 2*WALL_THICK, PUCK_W - 2*WALL_THICK, PUCK_H + 1.0], center=false);
        }

        // Top Optical Light Port (Ø 4.5 mm aperture precisely over TI OPT3001)
        translate([OPT_X, OPT_Y, PUCK_H - 1.0])
            cylinder(r=2.25, h=3.0, center=false);

        // Laminar Airflow Vent Grill (for TMP117 thermometer on West flank X = 0)
        // Positioned adjacent to the thermally isolated PCB island (Y = 8.0 .. 16.0 mm)
        for (gz = [5.5, 8.5, 11.5]) {
            translate([-0.5, TMP_Y - 4.5, gz])
                cube([WALL_THICK + 1.0, 9.0, 1.4], center=false);
        }

        // Rear Cable Notch on East Flank (for 6-Pin JST-GH cable to Front Node J_SENSOR_EXT)
        // Centered directly on J1 at Y = 23.28 mm
        translate([PUCK_L - WALL_THICK - 1.0, J1_Y - 5.5, FLOOR_THICK + STANDOFF_H])
            cube([WALL_THICK + 2.0, 11.0, 7.5], center=false);
    }

    // 3x Internal M2 Mounting Bosses matching PCBA 05D (H1, H2, H3)
    // Corner at (8.5, 8.5) is kept completely open to avoid heat conduction to TMP117!
    for (pt = BOSS_LIST) {
        difference() {
            translate([pt[0], pt[1], FLOOR_THICK])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
            translate([pt[0], pt[1], FLOOR_THICK - 0.5])
                cylinder(r=0.95, h=STANDOFF_H + 1.0, center=false); // M2 pilot hole
        }
    }

    // 4x Internal Lateral Locating Corner Guides (34.8 x 34.8 mm pocket stops)
    corner_guides = [
        [PCB_X0 - PCB_CLR, PCB_Y0 - PCB_CLR],
        [PCB_X0 + PCB_L + PCB_CLR - 2.5, PCB_Y0 - PCB_CLR],
        [PCB_X0 - PCB_CLR, PCB_Y0 + PCB_W + PCB_CLR - 2.5],
        [PCB_X0 + PCB_L + PCB_CLR - 2.5, PCB_Y0 + PCB_W + PCB_CLR - 2.5]
    ];
    for (cg = corner_guides) {
        translate([cg[0], cg[1], FLOOR_THICK])
            cube([2.5, 2.5, STANDOFF_H + 3.0], center=false);
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

// -----------------------------------------------------------------------------
// 2. Translucent Optical / Protective Cap
// -----------------------------------------------------------------------------
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

        // Center optical window precisely over TI OPT3001
        translate([OPT_X, OPT_Y, -0.5])
            cylinder(r=2.5, h=4.0, center=false);
    }
}

// -----------------------------------------------------------------------------
// 3. Complete Assembly Preview
// -----------------------------------------------------------------------------
module sensor_puck_environmental_assembly() {
    color([0.22, 0.24, 0.26])
        sensor_puck_cradle();

    color([0.7, 0.8, 0.9, 0.8])
        translate([0, 0, PUCK_H])
            sensor_puck_cap();
}

// Standalone execution preview / part selector ("assembly" | "bottom" | "top")
part = "assembly";
if (part == "bottom" || part == "cradle") {
    sensor_puck_cradle();
} else if (part == "top" || part == "cap") {
    sensor_puck_cap();
} else {
    sensor_puck_environmental_assembly();
}
