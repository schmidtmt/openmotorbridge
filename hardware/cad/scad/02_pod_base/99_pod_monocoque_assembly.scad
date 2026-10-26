// =============================================================================
// OpenMotorBridge - Satellite Pod: Full v10.0 Monocoque Assembly & Inspection
// =============================================================================
// File: hardware/cad/scad/02_pod_base/99_pod_monocoque_assembly.scad
// Description: Complete 3D assembly of the v10.0 universal Monocoque Satellite
//              Pod (Typ B). Features tool-free slide-in lid, FOB magnetic latch,
//              Zweizonen-Aufbau with EPDM Dry-Flap, floor-mounted PCBA 03, and
//              Universal Dual-Actuator Slide Bracket.
//
// View Modes:
// - VIEW_MODE = "cutaway": Longitudinal cut showing two-zone interior & ports
// - VIEW_MODE = "exploded": Vertical stack exploded along Z
// - VIEW_MODE = "xray": Ghosted translucent shell showing all internals
// - VIEW_MODE = "fob_lock": Detail view of magnetic latch & keyfob release
// =============================================================================

include <../00_common/parameters.scad>;
use <../00_common/dummies/dummy_m8_connector.scad>;
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <parts/008_pod_base_usbc_cap_tpu.scad>;
use <parts/012_universal_actuator_slide_bracket.scad>;
use <parts/013_pod_slide_lid.scad>;
use <parts/014_pod_dry_flap.scad>;
use <parts/015_pod_monocoque_tub.scad>;

VIEW_MODE = "cutaway"; // ["cutaway", "exploded", "xray", "fob_lock"]

// Exploded offsets
EXP_LID_Z      = (VIEW_MODE == "exploded") ? 75.0 : 0.0;
EXP_BRACKET_Z  = (VIEW_MODE == "exploded") ? 38.0 : 0.0;
EXP_FLAP_Z     = (VIEW_MODE == "exploded") ? 22.0 : 0.0;
EXP_PCB_Z      = (VIEW_MODE == "exploded") ? 8.0  : 0.0;
SLIDE_LID_X    = (VIEW_MODE == "cutaway")  ? 25.0 : 0.0;

module internal_wiring_preview() {
    // Port A Bus internal silicone ribbon (from bulkhead at Z=26.5 to J_BUS at X=9.5, Y=48.0)
    color([0.2, 0.5, 0.8, 0.9]) {
        translate([1.5, 33.0, 15.0])
            rotate([0, 15, 0])
                cube([8.0, 4.0, 11.0], center=false);
    }
    // Port B USB-C internal silicone cable (from bulkhead at Z=11.5 to J_USB_OUT at X=9.5, Y=22.0)
    color([0.85, 0.3, 0.2, 0.9]) {
        translate([1.5, 20.0, 8.5])
            cube([8.0, 4.0, 4.5], center=false);
    }
}

module pod_monocoque_full_assembly() {
    // 1. Monocoque Housing Tub
    if (VIEW_MODE == "cutaway") {
        difference() {
            color([0.28, 0.30, 0.33])
                pod_monocoque_tub();
            // Cut away near half (Y = -10 to 35 mm) so camera looks right into the two zones
            translate([-10.0, -10.0, -10.0])
                cube([POD_OUTER_L + 20.0, POD_OUTER_W/2.0 + 10.0, POD_OUTER_H + 20.0]);
        }
    } else if (VIEW_MODE == "xray") {
        color([0.3, 0.45, 0.65, 0.28])
            pod_monocoque_tub();
    } else {
        color([0.28, 0.30, 0.33])
            pod_monocoque_tub();
    }

    // 2. Port A: M8 4-Pin IP67 Metal Bus Connector (Bulkhead center, top: Z = 26.5 mm)
    translate([0.0, POD_OUTER_W/2.0, POD_OUTER_H/2.0 + 7.5])
        rotate([0, 180, 0])
            dummy_m8_connector();

    // 3. Port B: In-Bag USB-C Fast-Charge Socket (Bulkhead center, bottom: Z = 11.5 mm)
    translate([0.5, POD_OUTER_W/2.0, POD_OUTER_H/2.0 - 7.5])
        rotate([0, 90, 90])
            pod_base_usbc_cap_tpu();

    // 4. Internal Wiring (Silicone leads connecting bulkhead ports to PCBA 03)
    internal_wiring_preview();

    // 5. PCBA 03 Interface Board (resting on 4x M2.5 elastomer dampers at floor)
    translate([6.0, 11.0, POD_WALL + 3.0 + EXP_PCB_Z]) {
        dummy_adapter_pcb();
    }

    // 6. Intermediate Dry-Flap Splash Shield (isolating lower PCBA 03 zone)
    translate([6.0, 7.0, 14.5 + EXP_FLAP_Z]) {
        color([0.92, 0.68, 0.18, 0.88])
            pod_dry_flap();
    }

    // 7. Universal Dual-Actuator Slide Bracket (in upper equipment chamber)
    translate([48.0, 8.0, POD_WALL + 1.0 + EXP_BRACKET_Z]) {
        universal_actuator_slide_bracket_assembly();
    }

    // 8. Tool-Free Slide-In Lid
    if (VIEW_MODE == "cutaway") {
        difference() {
            translate([2.0 + SLIDE_LID_X, 3.0, POD_OUTER_H - 3.5 + EXP_LID_Z]) {
                color([0.22, 0.23, 0.25, 0.95])
                    pod_slide_lid();
            }
            translate([-10.0, -10.0, -10.0])
                cube([POD_OUTER_L + 60.0, POD_OUTER_W/2.0 + 10.0, POD_OUTER_H + 50.0]);
        }
    } else {
        translate([2.0 + SLIDE_LID_X, 3.0, POD_OUTER_H - 3.5 + EXP_LID_Z]) {
            color([0.22, 0.23, 0.25, (VIEW_MODE == "xray" ? 0.35 : 0.95)])
                pod_slide_lid();
        }
    }
}

// Render selected view
pod_monocoque_full_assembly();
