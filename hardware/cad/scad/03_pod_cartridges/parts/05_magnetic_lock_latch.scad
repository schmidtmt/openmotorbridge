// =============================================================================
// OpenMotorBridge - Magnetic Anti-Theft Lock Latch (Magnetischer Diebstahlschutz)
// =============================================================================
// File: hardware/cad/scad/03_pod_cartridges/parts/05_magnetic_lock_latch.scad
// Description: Spring-loaded, magnet-actuated anti-theft rocker pawl module
//              for OpenMotorBridge universal cartridges (Sena, Cardo, Transceiver).
//              Wirkprinzip: 1. Klasse 2-Arm-Wippe mit Drehpunkt in der Mitte:
//              - Hinterer Arm (X = 46 mm): Hält den ferromagnetischen Stahlanker (Ø 6 mm).
//              - Drehpunkt (X = 58 mm): M2 Edelstahl-Schwenkachse.
//              - Vorderer Arm (X = 70 mm): Sägezahn-Rastkralle mit 30° Einschubschräge
//                und 90° Sperrflanke gegen Herausziehen.
//              - Druckfeder drückt den hinteren Arm nach innen -> vorderer Zahn schnappt nach außen.
//              - Externer N52 Neodym-Magnet zieht den hinteren Arm nach außen ->
//                vorderer Zahn schwenkt nach innen -> Kassette entriegelt & federt aus!
// =============================================================================

include <../../00_common/parameters.scad>;

// --- Parametric Dimensions ---
LATCH_PIVOT_X       = 58.0;  // Center pivot position in sled X (mm)
LATCH_MAGNET_X      = 46.0;  // Ferromagnetic anchor position in sled X (mm)
LATCH_TOOTH_X       = 70.0;  // Locking sawtooth pawl position in sled X (mm)

LATCH_ARM_H         = 6.0;   // Rocker lever height in Z (mm)
LATCH_ARM_THICK     = 2.6;   // Rocker beam thickness in Y (mm)
LATCH_PIVOT_BORE_R  = 1.1;   // M2 pivot bore radius (Ø 2.2 mm)

// Sawtooth wedge pawl geometry
PAWL_PROTRUSION_Y   = 2.5;   // Locking pawl reach beyond guide rail (mm)
PAWL_LENGTH_X       = 8.0;   // Pawl tooth length along X (mm)
PAWL_RAMP_ANGLE     = 30.0;  // 30° lead-in ramp for smooth insertion

// Internal magnetic anchor & spring cavities
MAGNET_PIN_DIA      = 6.2;   // Bore for Ø 6.0 mm steel dowel pin (mm)
MAGNET_PIN_R        = MAGNET_PIN_DIA / 2.0;
MAGNET_PIN_L        = 8.0;   // Length of steel core (mm)
SPRING_BORE_DIA     = 3.8;   // Bore for Ø 3.5 mm return compression spring (mm)
SPRING_BORE_R       = SPRING_BORE_DIA / 2.0;
SPRING_BORE_DEPTH   = 6.0;   // Spring pocket depth (mm)

// 1. The 3D-Printable Rocker Lever (Die Verriegelungswippe)
module magnetic_lock_rocker_lever() {
    difference() {
        union() {
            // Central pivot cylinder
            translate([LATCH_PIVOT_X, 0, 0])
                cylinder(r=3.8, h=LATCH_ARM_H, center=true);

            // Forward locking arm
            hull() {
                translate([LATCH_PIVOT_X, -LATCH_ARM_THICK/2.0, -LATCH_ARM_H/2.0])
                    cube([1.0, LATCH_ARM_THICK, LATCH_ARM_H]);
                translate([LATCH_TOOTH_X - PAWL_LENGTH_X, -LATCH_ARM_THICK/2.0, -LATCH_ARM_H/2.0])
                    cube([1.0, LATCH_ARM_THICK, LATCH_ARM_H]);
            }

            // Forward Sawtooth Locking Tooth (30° slope facing rear, 90° stop facing forward)
            translate([LATCH_TOOTH_X - PAWL_LENGTH_X, -LATCH_ARM_THICK/2.0 - PAWL_PROTRUSION_Y, -LATCH_ARM_H/2.0]) {
                polyhedron(
                    points=[
                        [0, PAWL_PROTRUSION_Y, 0],
                        [PAWL_LENGTH_X, PAWL_PROTRUSION_Y, 0],
                        [PAWL_LENGTH_X, 0, 0],
                        [0, PAWL_PROTRUSION_Y, LATCH_ARM_H],
                        [PAWL_LENGTH_X, PAWL_PROTRUSION_Y, LATCH_ARM_H],
                        [PAWL_LENGTH_X, 0, LATCH_ARM_H]
                    ],
                    faces=[
                        [0,1,2], [3,5,4], [0,2,5,3], [1,4,5,2], [0,3,4,1]
                    ]
                );
            }

            // Rearward magnetic anchor arm
            hull() {
                translate([LATCH_PIVOT_X, -LATCH_ARM_THICK/2.0, -LATCH_ARM_H/2.0])
                    cube([1.0, LATCH_ARM_THICK, LATCH_ARM_H]);
                translate([LATCH_MAGNET_X - 2.0, -LATCH_ARM_THICK/2.0, -LATCH_ARM_H/2.0])
                    cube([4.0, LATCH_ARM_THICK + 3.0, LATCH_ARM_H]);
            }
        }

        // M2 Center Pivot Through-Bore
        translate([LATCH_PIVOT_X, 0, -LATCH_ARM_H/2.0 - 1.0])
            cylinder(r=LATCH_PIVOT_BORE_R, h=LATCH_ARM_H + 2.0);

        // Ferromagnetic Steel Pin Pocket (in rear arm)
        translate([LATCH_MAGNET_X, 0, 0])
            rotate([90, 0, 0])
                cylinder(r=MAGNET_PIN_R, h=MAGNET_PIN_L, center=true);

        // Return Spring Pocket (on inner face of rear arm)
        translate([LATCH_MAGNET_X, 2.0, 0])
            rotate([-90, 0, 0])
                cylinder(r=SPRING_BORE_R, h=SPRING_BORE_DEPTH + 1.0);
    }
}

// 2. Boolean Cutout Tool for Cartridge Base Sled (Erzeugt Schwenktasche & M2 Schraubdom)
module magnetic_lock_sled_pocket_tool(wall=2.5, z_center=POD_GROOVE_LEFT_Z) {
    // Rocker Swing Cavity
    translate([LATCH_MAGNET_X - 6.0, -1.0, z_center - LATCH_ARM_H/2.0 - 0.8])
        cube([LATCH_TOOTH_X - LATCH_MAGNET_X + 12.0, wall + 4.5, LATCH_ARM_H + 1.6]);

    // Outer Slot in Guide Tongue for Tooth Protrusion
    translate([LATCH_TOOTH_X - PAWL_LENGTH_X - 1.0, -CARTRIDGE_TONGUE_PROT - 1.0, z_center - LATCH_ARM_H/2.0 - 0.5])
        cube([PAWL_LENGTH_X + 2.0, CARTRIDGE_TONGUE_PROT + 2.0, LATCH_ARM_H + 1.0]);

    // M2 Pivot Standoff / Screw Boss
    translate([LATCH_PIVOT_X, wall + 1.5, z_center])
        cylinder(r=LATCH_PIVOT_BORE_R, h=15.0, center=true);
}

// 3. Boolean Cutout Tool for Pod Base Housing Detent (Rastkerbe im Führungsnut-Grund)
module magnetic_lock_housing_detent_tool(wall=POD_WALL, z_center=POD_GROOVE_LEFT_Z) {
    detent_x_pos = POD_BULKHEAD_X + LATCH_TOOTH_X; // X in housing = 18 + 70 = 88 mm
    // Locking Detent Pocket in Left Guide Groove
    translate([detent_x_pos - PAWL_LENGTH_X - 1.0, wall - 1.5, z_center - LATCH_ARM_H/2.0 - 0.6]) {
        // Sharp 90° blocking shoulder at rear (preventing pull-out)
        cube([PAWL_LENGTH_X + 2.0, 2.5, LATCH_ARM_H + 1.2]);
    }
}

// 4. Boolean Tool for Housing Exterior Magnet Alignment Indicator (Zielkreis)
module magnetic_lock_housing_target_tool(wall=POD_WALL, z_center=POD_GROOVE_LEFT_Z) {
    target_x_pos = POD_BULKHEAD_X + LATCH_MAGNET_X; // X in housing = 18 + 46 = 64 mm
    // Outer Debossed Target Circle for Neodymium Key
    translate([target_x_pos, -0.1, z_center]) {
        rotate([90, 0, 0]) {
            // Outer alignment ring (Ø 18 mm x 0.6 mm deep)
            difference() {
                cylinder(r=9.0, h=0.6, center=false);
                cylinder(r=7.5, h=0.7, center=false);
            }
            // Center tactile alignment pip
            cylinder(r=2.5, h=0.6, center=false);
        }
    }
}

// Standalone render of the rocker lever
magnetic_lock_rocker_lever();
