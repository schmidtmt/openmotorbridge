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
use <../00_common/dummies/dummy_intercom_units.scad>;

module pod_port_a_magnetic_connector() {
    // 1. Molded Black PBT Flange Body (14.5 x 7.5 x 4.0 mm, flush in bulkhead)
    color([0.15, 0.15, 0.18]) {
        translate([-2.0, -7.25, -3.75])
            cube([4.0, 14.5, 7.5], center=false);
    }
    // 2. Dual Rare-Earth Alignment Magnets (Nickel-plated silver)
    color("silver") {
        translate([-2.1, -5.0, 0])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=1.0, center=false, $fn=16);
        translate([-2.1, 5.0, 0])
            rotate([0, 90, 0])
                cylinder(r=1.5, h=1.0, center=false, $fn=16);
    }
    // 3. 4x Gold-Plated Pogo Contact Terminals (Pitch 2.2 mm)
    color("gold") {
        for (py = [-3.3, -1.1, 1.1, 3.3]) {
            translate([-2.2, py, 0])
                rotate([0, 90, 0])
                    cylinder(r=0.6, h=1.2, center=false, $fn=16);
        }
    }
    // 4. Internal 4-Conductor Silicone Flat-Ribbon Cable (leads to J_BUS)
    translate([2.0, -3.6, -1.0]) {
        for (i = [0:3]) {
            c_color = (i == 0) ? "red" : (i == 1) ? "white" : (i == 2) ? "green" : "black";
            color(c_color)
                translate([0, i * 1.8, 0])
                    cube([14.0, 1.4, 1.0], center=false);
        }
    }
}
use <../00_common/dummies/dummy_adapter_pcb.scad>;
use <parts/008_pod_base_usbc_cap_tpu.scad>;
use <parts/012_universal_actuator_slide_bracket.scad>;
use <parts/013_pod_slide_lid.scad>;
use <parts/014_pod_dry_flap.scad>;
use <parts/015_pod_monocoque_tub.scad>;

VIEW_MODE = "cutaway"; // ["cutaway", "exploded", "xray", "fob_lock"]

// Exploded & Slide-in offsets
EXP_LID_X      = (VIEW_MODE == "exploded") ? 55.0 : 0.0;  // Displaced horizontally along X to reveal rear slide-in slot!
EXP_LID_Z      = (VIEW_MODE == "exploded") ? 15.0 : 0.0;  // Elevated slightly to showcase internal equipment chamber
EXP_BRACKET_Z  = (VIEW_MODE == "exploded") ? 24.0 : 0.0;
EXP_FLAP_Z     = (VIEW_MODE == "exploded") ? 14.0 : 0.0;
EXP_PCB_Z      = (VIEW_MODE == "exploded") ? 6.0  : 0.0;
SLIDE_LID_X    = (VIEW_MODE == "cutaway")  ? 35.0 : 0.0;  // Lid partially retracted along X-rails to demonstrate sliding action!

module internal_wiring_preview() {
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
            // Cut away near longitudinal wall (Y = -10 to 22 mm) to open full view into both zones
            translate([8.0, -10.0, 10.0])
                cube([POD_OUTER_L - 16.0, 32.0, POD_OUTER_H + 20.0]);
        }
    } else if (VIEW_MODE == "xray") {
        color([0.3, 0.45, 0.65, 0.28])
            pod_monocoque_tub();
    } else {
        color([0.28, 0.30, 0.33])
            pod_monocoque_tub();
    }

    // 2. Port A: 4-Pin IP67 Magnet-Abrissschnittstelle (Bulkhead center, top: Z = 26.5 mm)
    translate([0.0, POD_OUTER_W/2.0, POD_OUTER_H/2.0 + 7.5])
        pod_port_a_magnetic_connector();

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

    // 7. Upper Equipment Bay: Cardo Packtalk Edge WITH 2D Dual-Rocker Plate
    translate([50.0, (POD_OUTER_W - 46.0)/2.0, POD_WALL + 1.5 + EXP_BRACKET_Z]) {
        // OEM Air-Mount Cradle screwed to floor
        dummy_cardo_oem_airmount_cradle();

        // Packtalk Edge Unit clicked into cradle
        translate([0, 0, 3.5])
            dummy_cardo_packtalk_edge(with_actuators = false);

        // Ultra-Low-Profile 2D Dual-Rocker Actuator Plate (Clicked onto cradle, height only 6.5 mm!)
        // Enables fully automatic ignition-coupled Power-On / Power-Off (KL15) for Cardo
        translate([-1.0, 0, 22.0])
            cardo_edge_2d_rocker_plate(show_actuators = true);
    }

    // 8. Tool-Free Slide-In Lid (Sliding horizontally inside sidewall C-grooves at Z = 32.4 mm)
    // Firmly captured and locked from above by the solid PA12 upper retaining lip (Z = 35.2 to 38.0 mm)
    lid_z_pos = 32.4;

    if (VIEW_MODE == "cutaway") {
        difference() {
            translate([2.0 + SLIDE_LID_X, (POD_OUTER_W - 60.5)/2.0, lid_z_pos + EXP_LID_Z]) {
                color([0.22, 0.23, 0.25, 0.95])
                    pod_slide_lid();
            }
            // Cut away near corner to expose internal C-groove engagement and equipment
            translate([-10.0, -10.0, -10.0])
                cube([85.0, POD_OUTER_W/2.0 + 5.0, POD_OUTER_H + 50.0]);
        }
    } else {
        translate([2.0 + SLIDE_LID_X + EXP_LID_X, (POD_OUTER_W - 60.5)/2.0, lid_z_pos + EXP_LID_Z]) {
            color([0.22, 0.23, 0.25, (VIEW_MODE == "xray" ? 0.35 : 0.95)])
                pod_slide_lid();
        }
    }
}

// Render selected view
pod_monocoque_full_assembly();
