// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Base Housing (Schachtgehäuse)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_base_housing.scad
// Description: Ready-to-print universal pod base housing for all 3 positions
//              (Pod 1 Left, Pod 2 Right, Pod 3 Rear). Includes 5-sided monocoque
//              tunnel with rounded corners, universal frame tube saddle (V-groove),
//              4x EPDM strap hook lugs, Dual-Port rear wall (Port A M8 on left,
//              Port B USB-C pocket on right), bulkhead partition, asymmetrical
//              Poka-Yoke guide grooves, and ceiling Gore ePTFE breather.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
use <parts/000_pod_tunnel_base.scad>;
use <parts/001_pod_rear_m8_gland.scad>;
use <parts/002_pod_bulkhead_partition.scad>;
use <parts/003_pod_guide_grooves.scad>;
use <parts/005_pod_strap_hooks.scad>;

module pod_base_housing() {
    port_offset_y = 8.0; // Symmetrical offset from centerline (yc = POD_OUTER_W / 2.0 = 35.0 mm; Port A = 27 mm, Port B = 43 mm)

    difference() {
        union() {
            // 1. Monocoque 5-Sided Tunnel Body (135 x 70 x 38 mm with V-Groove & Zip-Tie Slots)
            pod_tunnel_base(
                length=POD_OUTER_L,
                width=POD_OUTER_W,
                height=POD_OUTER_H,
                wall=POD_WALL,
                r_edge=3.0
            );

            // 2. 4x EPDM Rubber Strap Hook Lugs on Lower Flanks
            pod_strap_hook_lugs(
                length=POD_OUTER_L,
                width=POD_OUTER_W,
                hook_w=8.0,
                hook_out=3.0,
                hook_h=4.5
            );

            // 3. Rear Port A: M8 6-Pin IP67 Cable Gland Stutzen (Shifted Left: yc = 26.0 mm)
            pod_rear_m8_neck(
                neck_len=10.0,
                outer_r=M8_STUDS_OUTER_R,
                inner_r=M8_BORE_R,
                yc=POD_OUTER_W/2.0 - port_offset_y,
                zc=POD_OUTER_H/2.0
            );

            // 4. Protective Bulkhead Partition with 6-Pin Shroud & Spring Seats (x = 18 mm)
            pod_bulkhead_assembly(
                bulkhead_x=POD_BULKHEAD_X,
                wall=POD_WALL
            );

            // 5. Asymmetrical Poka-Yoke Internal Linear Guide Rails (Tongue & Groove)
            pod_internal_guide_ribs(
                start_x=POD_BULKHEAD_X + 2.0,
                length=POD_OUTER_L - POD_BULKHEAD_X - 4.0,
                wall=POD_WALL
            );

            // 6. Rear Port B: Internal Sleeve Boss (Encloses USB-C pocket against inner chamber)
            pod_rear_usbc_internal_sleeve(
                depth=10.0,
                outer_w=17.0,
                outer_h=11.5,
                yc=POD_OUTER_W/2.0 + port_offset_y,
                zc=POD_OUTER_H/2.0
            );

            // 7. Ceiling Gore ePTFE Breather Vent Boss (Top center, fused into ceiling)
            translate([POD_OUTER_L/2.0, POD_OUTER_W/2.0, POD_OUTER_H - 1.0])
                cylinder(r=3.5, h=2.5, center=false, $fn=16);
        }

        // 8. Rear Port A: M8 Continuous Cable Through-Bore (Shifted Left: yc = 27.0 mm)
        pod_rear_m8_through_hole_tool(
            wall_th=POD_WALL + 1.0,
            inner_r=M8_BORE_R,
            yc=POD_OUTER_W/2.0 - port_offset_y,
            zc=POD_OUTER_H/2.0
        );

        // 9. Rear Port B: Recessed USB-C Vertical Socket Plug-Well & Seat (Depth 7.0 mm)
        pod_rear_usbc_pocket_tool(
            wall_th=18.0,
            pocket_depth=7.0,
            pocket_w=14.0,
            pocket_h=8.5,
            port_w=9.6,
            port_h=4.0,
            yc=POD_OUTER_W/2.0 + port_offset_y,
            zc=POD_OUTER_H/2.0
        );

        // 9. Ceiling Gore Vent Center Breather Hole (Ø 3.0 mm)
        translate([POD_OUTER_L/2.0, POD_OUTER_W/2.0, POD_OUTER_H - POD_WALL - 0.5])
            cylinder(r=1.5, h=POD_WALL + 2.5, center=false, $fn=16);
    }
}

// Render complete universal pod housing
pod_base_housing();
