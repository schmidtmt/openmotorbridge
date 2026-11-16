// =============================================================================
// OpenMotorBridge - Front Node: Modular Snap-On Environmental Sensor Puck
// =============================================================================
// File: hardware/cad/scad/04_front_node/parts/sensor_puck_environmental.scad
// Description: Compact modular snap-on sensor cradle ("Körbchen") precisely
//              tailored to PCBA 05D (34.0 x 34.0 mm) with exact 1:1 hardware parity:
//              1. u-blox SAM-M10Q Multi-GNSS patch module with zenith sky view.
//              2. TI TMP117 high-precision thermometer on thermally isolated PCB island
//                 with laminar airflow ventilation slots on West flank.
//              3. TI OPT3001 ambient light luxmeter with top optical aperture & bevel.
//              4. 3x M2 mounting screw bosses (H1, H2, H3) matching KiCad PCB coordinates.
//              5. East flank notch for 6-pin JST-GH cable (J1 - SENSOR_IN from Front Node).
//              6. North flank notch for 6-pin JST-SH cable (J2 - EXP_OUT expansion bus).
//              7. Snap-fit cap with stepped perimeter seal lip and corner pry slot.
//              8. Dual bottom snap-fit arms for toolless Front Node lid docking.
// =============================================================================

$fn = 48;

// --- Physical Puck Outer Envelope (Form-fit with Front Node lid snap slots) ---
PUCK_L          = 38.0;   // Outer longitudinal length (mm)
PUCK_W          = 38.0;   // Outer transverse width (mm)
PUCK_H          = 15.0;   // Total cradle height (mm)
WALL_THICK      = 1.6;    // Structural wall thickness (mm)
FLOOR_THICK     = 1.8;    // Bottom floor thickness (mm)
R_PUCK          = 4.5;    // Aerodynamic corner radius (mm)

// --- PCBA 05D Physical Parameters (KiCad openmotorbridge_sensor_puck.kicad_pcb) ---
PCB_L           = 34.0;   // PCB length (mm)
PCB_W           = 34.0;   // PCB width (mm)
PCB_T           = 1.6;    // FR4 substrate thickness (mm)
PCB_CLR         = 0.35;   // Internal perimeter clearance (mm)
STANDOFF_H      = 2.5;    // Standoff height under PCB (mm)

// Centered PCB origin inside 38 x 38 mm housing (2.0 mm wall + clearance offset):
PCB_X0          = (PUCK_L - PCB_L) / 2.0; // 2.0 mm
PCB_Y0          = (PUCK_W - PCB_W) / 2.0; // 2.0 mm

// --- Exact Component Positions (from KiCad PCB coordinates) ---
// 1. OPT3001 Ambient Light Sensor U3 at (18.35, 5.61) on PCB
OPT_X           = PCB_X0 + 18.35; // 20.35 mm
OPT_Y           = PCB_Y0 + 5.61;  // 7.61 mm

// 2. TMP117 Temperature Sensor U2 at (5.0, 7.0) on PCB (thermal island)
TMP_X           = PCB_X0 + 5.0;   // 7.0 mm
TMP_Y           = PCB_Y0 + 7.0;   // 9.0 mm

// 3. J1 JST-GH 6-Pin Connector at (30.15, 18.28) facing East (+X)
J1_X            = PCB_X0 + 30.15; // 32.15 mm
J1_Y            = PCB_Y0 + 18.28; // 20.28 mm

// 4. J2 JST-SH 6-Pin Connector at (22.95, 30.12) facing North (+Y)
J2_X            = PCB_X0 + 22.95; // 24.95 mm
J2_Y            = PCB_Y0 + 30.12; // 32.12 mm

// 5. 3x M2 Mounting Holes: H1 (3.5, 30.5), H2 (30.5, 30.5), H3 (30.5, 3.5)
// (Corner at PCB (3.5, 3.5) is kept completely open for TMP117 thermal isolation!)
BOSS_LIST = [
    [PCB_X0 + 3.5,  PCB_Y0 + 30.5], // H1: (5.5, 32.5)
    [PCB_X0 + 30.5, PCB_Y0 + 30.5], // H2: (32.5, 32.5)
    [PCB_X0 + 30.5, PCB_Y0 + 3.5]   // H3: (32.5, 5.5)
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

        // Inner Electronics Cavity for PCBA 05D (34.7 x 34.7 mm clears 34.0 x 34.0 mm PCB)
        translate([WALL_THICK, WALL_THICK, FLOOR_THICK]) {
            cube([PUCK_L - 2*WALL_THICK, PUCK_W - 2*WALL_THICK, PUCK_H + 1.0], center=false);
        }

        // Stepped Rebate Rim for Top Cap Sealing (0.8 mm deep x 1.0 mm rim)
        translate([WALL_THICK - 0.5, WALL_THICK - 0.5, PUCK_H - 1.8]) {
            cube([PUCK_L - 2*(WALL_THICK - 0.5), PUCK_W - 2*(WALL_THICK - 0.5), 2.0], center=false);
        }

        // Laminar Airflow Vent Grill (for TMP117 thermometer on West flank X = 0)
        // Directly aligned with the thermally isolated PCB island (Y = 6.0 .. 12.0 mm)
        for (gz = [FLOOR_THICK + 1.5, FLOOR_THICK + 4.5, FLOOR_THICK + 7.5]) {
            translate([-0.5, TMP_Y - 3.5, gz])
                cube([WALL_THICK + 1.0, 7.0, 1.4], center=false);
        }

        // J1 Cable Notch on East Flank (+X) for JST-GH 6-Pin Connector
        // Opens from PCB level to top rim so PCB drops in freely from above
        translate([PUCK_L - WALL_THICK - 0.5, J1_Y - 6.5, FLOOR_THICK + STANDOFF_H]) {
            cube([WALL_THICK + 1.0, 13.0, PUCK_H], center=false);
            // Beveled outer lead-in for cable strain relief and easy unlatching
            translate([0.5, -1.0, 0])
                cube([WALL_THICK + 1.0, 15.0, PUCK_H], center=false);
        }

        // J2 Cable Notch on North Flank (+Y) for JST-SH 6-Pin Expansion Connector
        translate([J2_X - 5.5, PUCK_W - WALL_THICK - 0.5, FLOOR_THICK + STANDOFF_H]) {
            cube([11.0, WALL_THICK + 1.0, PUCK_H], center=false);
            // Beveled outer lead-in
            translate([-1.0, 0.5, 0])
                cube([13.0, WALL_THICK + 1.0, PUCK_H], center=false);
        }

        // Corner Service Pry Slot (SW corner for easy cap removal)
        translate([0, 0, PUCK_H - 1.5])
            rotate([0, 0, 45])
                translate([-2.0, -1.0, 0])
                    cube([4.0, 2.0, 2.0], center=false);
    }

    // 3x Internal M2 Mounting Bosses matching PCBA 05D (H1, H2, H3)
    // Corner at (5.5, 5.5) is kept completely open to avoid heat conduction to TMP117!
    for (pt = BOSS_LIST) {
        difference() {
            translate([pt[0], pt[1], FLOOR_THICK])
                cylinder(r=2.5, h=STANDOFF_H, center=false);
            translate([pt[0], pt[1], FLOOR_THICK - 0.5])
                cylinder(r=0.95, h=STANDOFF_H + 1.0, center=false); // M2 pilot hole
        }
    }

    // 4x Internal Lateral Locating Chamfer Corner Stops (supports 2.0 x 2.0 mm PCB chamfers)
    // Placed at the 4 inner corners to hold PCB securely without thermal coupling
    translate([WALL_THICK, WALL_THICK, FLOOR_THICK])
        rotate([0, 0, 45])
            translate([-0.5, -0.5, 0])
                cube([1.5, 1.5, STANDOFF_H + 2.0], center=false);
    translate([PUCK_L - WALL_THICK, WALL_THICK, FLOOR_THICK])
        rotate([0, 0, 45])
            translate([-0.5, -0.5, 0])
                cube([1.5, 1.5, STANDOFF_H + 2.0], center=false);
    translate([WALL_THICK, PUCK_W - WALL_THICK, FLOOR_THICK])
        rotate([0, 0, 45])
            translate([-0.5, -0.5, 0])
                cube([1.5, 1.5, STANDOFF_H + 2.0], center=false);
    translate([PUCK_L - WALL_THICK, PUCK_W - WALL_THICK, FLOOR_THICK])
        rotate([0, 0, 45])
            translate([-0.5, -0.5, 0])
                cube([1.5, 1.5, STANDOFF_H + 2.0], center=false);

    // Dual Bottom Snap-Fit Arms (Rastlaschen für werkzeuglose Front-Node Schnellmontage)
    // Adjusted to 38.0 mm span matching Front Node lid slots
    translate([PUCK_L/2.0 - 7.0, -1.6, -4.5])
        cube([14.0, 1.8, 5.0], center=false);
    translate([PUCK_L/2.0 - 7.0, -2.4, -4.5])
        cube([14.0, 1.0, 2.0], center=false); // Catch barb 1

    translate([PUCK_L/2.0 - 7.0, PUCK_W - 0.2, -4.5])
        cube([14.0, 1.8, 5.0], center=false);
    translate([PUCK_L/2.0 - 7.0, PUCK_W + 1.4, -4.5])
        cube([14.0, 1.0, 2.0], center=false); // Catch barb 2
}

// -----------------------------------------------------------------------------
// 2. Translucent Optical / Protective Cap with Stepped Perimeter Snap Lip
// -----------------------------------------------------------------------------
module sensor_puck_cap() {
    difference() {
        union() {
            // Main Top Plate (2.2 mm thick squircle matching cradle outer profile)
            hull() {
                translate([R_PUCK, R_PUCK, 0])
                    cylinder(r=R_PUCK, h=2.2, center=false);
                translate([PUCK_L - R_PUCK, R_PUCK, 0])
                    cylinder(r=R_PUCK, h=2.2, center=false);
                translate([R_PUCK, PUCK_W - R_PUCK, 0])
                    cylinder(r=R_PUCK, h=2.2, center=false);
                translate([PUCK_L - R_PUCK, PUCK_W - R_PUCK, 0])
                    cylinder(r=R_PUCK, h=2.2, center=false);
            }

            // Stepped Perimeter Snap/Seal Lip (inserts 1.6 mm into cradle rebate)
            translate([0, 0, -1.6]) {
                hull() {
                    translate([R_PUCK, R_PUCK, 0])
                        cylinder(r=R_PUCK - WALL_THICK + 0.35, h=1.6, center=false);
                    translate([PUCK_L - R_PUCK, R_PUCK, 0])
                        cylinder(r=R_PUCK - WALL_THICK + 0.35, h=1.6, center=false);
                    translate([R_PUCK, PUCK_W - R_PUCK, 0])
                        cylinder(r=R_PUCK - WALL_THICK + 0.35, h=1.6, center=false);
                    translate([PUCK_L - R_PUCK, PUCK_W - R_PUCK, 0])
                        cylinder(r=R_PUCK - WALL_THICK + 0.35, h=1.6, center=false);
                }
            }
        }

        // Inner Electronics Cavity Relief (lightens cap and provides dome clearance)
        translate([WALL_THICK + 0.8, WALL_THICK + 0.8, -2.0]) {
            cube([PUCK_L - 2*(WALL_THICK + 0.8), PUCK_W - 2*(WALL_THICK + 0.8), 2.5], center=false);
        }

        // Center Optical Light Port precisely over TI OPT3001 at (20.35, 7.61)
        // With 45-degree conical light-gathering collector bevel
        translate([OPT_X, OPT_Y, -2.0])
            cylinder(r=2.0, h=5.0, center=false);
        translate([OPT_X, OPT_Y, 0.8])
            cylinder(r1=2.0, r2=3.5, h=1.5, center=false); // Conical bevel
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
