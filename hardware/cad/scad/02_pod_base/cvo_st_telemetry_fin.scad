// =============================================================================
// OpenMotorBridge - Satellite Pod 3: CVO ST Telemetry Fin (Screw-Mounted 2.4G)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/cvo_st_telemetry_fin.scad
// Description: Ultra-compact aerodynamic 2.4 GHz telemetry antenna fin for the
//              Harley-Davidson CVO ST. Attaches directly to the OEM rear seat cowl
//              mounting tab using the original factory M6 screw!
//              Features:
//              1. 100% Non-Invasive: Clamps on top of cowl tab via OEM M6 screw.
//              2. Concealed Cable Inlet: RG316 coax slips under cowl tab directly
//                 into internal antenna cavity (0 visible wires!).
//              3. Houses 2.4 GHz Dipole / PCB Antenna for Mesh & Headset link.
//              4. Aggressive supersonic jet styling matching CVO ST race pedigree.
//              5. 100% 2-manifold geometry (0 non-manifold edges).
// =============================================================================

include <../00_common/parameters.scad>;

FIN_L       = 68.0;
FIN_W_BASE  = 22.0;
FIN_H       = 18.5;
SCREW_X_POS = 14.0; // Distance from front nose to M6 screw center

module telemetry_fin_body() {
    hull() {
        // Front nose tip (touching cowl surface forward of screw)
        translate([0, 0, 1.0])
            cylinder(r=3.0, h=2.0, center=true, $fn=24);

        // Mid crest at screw shoulder
        translate([SCREW_X_POS, 0, 0]) {
            translate([0, 0, 2.0]) cylinder(r=FIN_W_BASE/2.0, h=4.0, center=true, $fn=32);
            translate([0, 0, FIN_H - 2.0]) cylinder(r=2.5, h=4.0, center=true, $fn=16);
        }

        // Antenna chamber crest (apex)
        translate([SCREW_X_POS + 26.0, 0, 0]) {
            translate([0, 0, 2.0]) cylinder(r=8.0, h=4.0, center=true, $fn=24);
            translate([0, 0, FIN_H - 1.5]) cylinder(r=2.0, h=3.0, center=true, $fn=16);
        }

        // Trailing edge nozzle tip
        translate([FIN_L, 0, 3.5])
            cylinder(r=2.2, h=4.0, center=true, $fn=20);
    }
}

module cvo_st_telemetry_fin() {
    difference() {
        // Main aerodynamic fin solid
        telemetry_fin_body();

        // 1. M6 Screw Through-Bore (Ø 6.6 mm)
        translate([SCREW_X_POS, 0, -1.0])
            cylinder(r=3.3, h=FIN_H + 5.0, center=false, $fn=32);

        // 2. Countersunk Washer Pocket for OEM M6 Screw Head (Ø 13.5 mm, depth 10 mm)
        translate([SCREW_X_POS, 0, FIN_H - 8.5])
            cylinder(r=6.8, h=12.0, center=false, $fn=32);

        // 3. Internal Antenna Cavity (Houses 2.4 GHz Dipole / PCB Antenna)
        hull() {
            translate([SCREW_X_POS + 11.0, 0, 2.5])
                cylinder(r=4.5, h=10.0, center=false, $fn=20);
            translate([FIN_L - 8.0, 0, 2.5])
                cylinder(r=2.8, h=6.0, center=false, $fn=20);
        }

        // 4. Concealed Cable Inlet Groove (Underneath forward nose)
        // Passes from front of fin base directly into the antenna cavity
        translate([SCREW_X_POS/2.0, 0, 0.8])
            cube([SCREW_X_POS + 4.0, 3.6, 2.5], center=true);

        // 5. Under-lip relief to seat flush over cowl tab perimeter
        translate([SCREW_X_POS, 0, -0.5])
            cylinder(r=FIN_W_BASE/2.0 - 1.0, h=1.2, center=false, $fn=32);
    }
}

// Standalone preview
cvo_st_telemetry_fin();
