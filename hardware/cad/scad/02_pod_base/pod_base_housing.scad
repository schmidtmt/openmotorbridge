// =============================================================================
// OpenMotorBridge - Satellite Pod: Universal Base Housing (Schachtgehäuse)
// =============================================================================
// File: hardware/cad/scad/02_pod_base/pod_base_housing.scad
// Description: Ready-to-print universal pod base housing for all 3 positions
//              (Pod 1 Left, Pod 2 Right, Pod 3 Rear). Includes 5-sided monocoque
//              tunnel with rounded corners, universal frame tube saddle (V-groove),
//              4x EPDM strap hook lugs, rear M8 cable gland neck, bulkhead partition,
//              asymmetrical Poka-Yoke guide grooves, and ceiling Gore ePTFE breather.
// =============================================================================

include <../00_common/parameters.scad>;
include <../00_common/screw_bosses.scad>;
include <parts/000_pod_tunnel_base.scad>;
include <parts/001_pod_rear_m8_gland.scad>;
include <parts/002_pod_bulkhead_partition.scad>;
include <parts/003_pod_guide_grooves.scad>;
include <parts/005_pod_strap_hooks.scad>;

module pod_base_housing() {
    difference() {
        union() {
            // 1. Monocoque 5-Sided Tunnel Body (100 x 60 x 28 mm with V-Groove & Zip-Tie Slots)
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

            // 3. Rear M8 6-Pin IP67 Cable Gland Stutzen (x = -10.0 .. 0.0 mm)
            pod_rear_m8_neck(
                neck_len=10.0,
                outer_r=M8_STUDS_OUTER_R,
                inner_r=M8_BORE_R,
                yc=POD_OUTER_W/2.0,
                zc=POD_OUTER_H/2.0
            );

            // 4. Protective Bulkhead Partition with 6-Pin Shroud & Spring Seats (x = 22 mm)
            pod_bulkhead_assembly(
                bulkhead_x=POD_BULKHEAD_X,
                wall=POD_WALL
            );

            // 5. Asymmetrical Poka-Yoke Internal Linear Guide Rails (Tongue & Groove)
            pod_internal_guide_ribs(
                start_x=24.0,
                length=76.0,
                wall=POD_WALL
            );

            // 6. Ceiling Gore ePTFE Breather Vent Boss (Top center: x = 50.0, y = 30.0, z = 28.0)
            translate([50.0, POD_OUTER_W/2.0, POD_OUTER_H])
                cylinder(r=3.5, h=1.5, center=false, $fn=16);
        }

        // 7. Rear Wall M8 Continuous Cable Through-Bore (Ø 8.0 mm into chamber)
        pod_rear_m8_through_hole_tool(
            wall_th=POD_WALL + 1.0,
            inner_r=M8_BORE_R,
            yc=POD_OUTER_W/2.0,
            zc=POD_OUTER_H/2.0
        );

        // 8. Ceiling Gore Vent Center Breather Hole (Ø 3.0 mm)
        translate([50.0, POD_OUTER_W/2.0, POD_OUTER_H - POD_WALL - 0.5])
            cylinder(r=1.5, h=POD_WALL + 2.5, center=false, $fn=16);
    }
}

// Render complete universal pod housing
pod_base_housing();
