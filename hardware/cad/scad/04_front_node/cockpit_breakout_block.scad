// =============================================================================
// OpenMotorBridge - Cockpit Breakout & Handschuhfach-Hub Housing (PCBA 05B)
// =============================================================================
// File: hardware/cad/scad/04_front_node/cockpit_breakout_block.scad
// Description: Multi-function modular distribution bar and media/power injection
//              hub tailored for motorcycle cockpit, handlebar, fairing, and the
//              Harley-Davidson glovebox (Media Compartment).
//              Houses PCBA 05B (76.0 x 20.0 mm):
//              1. J1: [ PHONE 20W ] USB-PD Fast Charge at X = 14.0 mm
//              2. J2: [ DONGLE ] 10W Switched 5V for Wireless CarPlay/AA at X = 26.0 mm
//              3. J3: [ HOST ] Upstream USB to Harley Skyline OS / Boom! Box at X = 38.0 mm
//              4. J4: [ CAM 5V ] / Media Stick Pass-Through at X = 50.0 mm
//              5. J5: [ NAVI 5V ] Garmin / Chigee / Smartphone at X = 62.0 mm
//              6. J6: [ PTT ] 2-Pin JST-GH Push-to-Talk Terminal at X = 73.8 mm
//              7. J_IN: 16-Pin Dual-Row 2.0 mm Shielded Harness from Front Node
//              Features:
//              - Front-face beveled USB-C port apertures (9.6 x 3.8 mm, 45° lead-in)
//              - West-flank cable inflow gland (Ø 6.2 mm) with zip-tie anchor
//              - Lateral Dovetail rail (male) along North edge for interlock
//              - Bottom 3M Dual-Lock recess (1.2 mm deep) for glovebox floor
//              - Bottom zip-tie channels for handlebar / tube clamping
//              - Precision screw bosses for PCBA 05B mounting holes H1 and H2
//              - Flush weatherproof snap/screw lid plate
//              - Anti-vibration strain-relief clamping bar for rugged touring
// =============================================================================

include <../00_common/parameters.scad>;

part = "all"; // [all, body, lid, clamp, assembly, closed, exploded, xray]
$fn  = 36;

// --- Enclosure Dimensions ---
COCKPIT_BLOCK_L = 86.0;   // Outer enclosure length (mm)
COCKPIT_BLOCK_W = 28.0;   // Outer enclosure width (mm)
COCKPIT_BLOCK_H = 18.0;   // Outer enclosure height (mm)
WALL            = 2.2;    // Nominal wall thickness (mm)
CORNER_R        = 2.5;    // Corner fillet radius (mm)

// --- Internal Cavity Dimensions ---
CAVITY_L        = 81.6;   // Inner cavity length along X (mm)
CAVITY_W        = 23.6;   // Inner cavity width along Y (mm)
CAVITY_H        = COCKPIT_BLOCK_H - WALL; // Inner cavity depth (mm)

// --- PCBA 05B Alignment Parameters ---
PCB_L           = 76.0;
PCB_W           = 20.0;
PCB_THICK       = 1.6;
PCB_OFFSET_X    = 4.18;   // X-offset of PCB within housing: J1 at 4.18 + 9.82 = 14.0 mm
PCB_OFFSET_Y    = 2.2;    // Y-offset of PCB: front edge flush with inner front wall
STANDOFF_H      = 2.0;    // Standoff height above floor (mm)
PCB_Z           = WALL + STANDOFF_H; // PCB bottom plane Z = 4.2 mm

// --- USB-C & Port Cutout Coordinates ---
USB_X           = [14.0, 26.0, 38.0, 50.0, 62.0];
USB_PORT_W      = 9.6;    // Port width (mm)
USB_PORT_H      = 3.8;    // Port height (mm)
USB_PORT_Z      = PCB_Z + PCB_THICK + 1.6; // Center Z = 4.2 + 1.6 + 1.6 = 7.4 mm

// --- Dovetail Interlocking Parameters (Matches vehicle_breakout_block) ---
DOVETAIL_W_BOTTOM = 6.0;
DOVETAIL_W_TOP    = 8.4;
DOVETAIL_H        = 3.0;
DOVETAIL_L        = COCKPIT_BLOCK_L - 10.0; // 76.0 mm

module dovetail_male(length = DOVETAIL_L) {
    linear_extrude(height = length) {
        polygon(points=[
            [-DOVETAIL_W_BOTTOM/2, 0],
            [ DOVETAIL_W_BOTTOM/2, 0],
            [ DOVETAIL_W_TOP/2,    DOVETAIL_H],
            [-DOVETAIL_W_TOP/2,    DOVETAIL_H]
        ]);
    }
}

// -----------------------------------------------------------------------------
// 1. Cockpit Breakout Main Body (Unterteil)
// -----------------------------------------------------------------------------
module cockpit_breakout_body() {
    color([0.22, 0.22, 0.24]) // Charcoal ASA / MJF PA12
    difference() {
        union() {
            // Main solid rounded housing block
            hull() {
                translate([CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=COCKPIT_BLOCK_H, center=false);
            }
            
            // Lateral Male Dovetail Rail along North edge (Y = COCKPIT_BLOCK_W)
            translate([COCKPIT_BLOCK_L - 5.0, COCKPIT_BLOCK_W, 3.5])
                rotate([0, -90, 0])
                    rotate([0, 0, 90])
                        dovetail_male();

            // Internal PCB mounting bosses (H1 and H2)
            // H1 at (PCB_OFFSET_X + 4.0, PCB_OFFSET_Y + 16.0) = (8.18, 18.2)
            translate([PCB_OFFSET_X + 4.0, PCB_OFFSET_Y + 16.0, WALL])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
            // H2 at (PCB_OFFSET_X + 72.0, PCB_OFFSET_Y + 16.0) = (76.18, 18.2)
            translate([PCB_OFFSET_X + 72.0, PCB_OFFSET_Y + 16.0, WALL])
                cylinder(r=2.8, h=STANDOFF_H, center=false);
        }
        
        // --- Inner Electronics Cavity ---
        translate([WALL, WALL, WALL])
            cube(size=[COCKPIT_BLOCK_L - 2*WALL, COCKPIT_BLOCK_W - 2*WALL, COCKPIT_BLOCK_H], center=false);
            
        // --- 5x Front USB-C Port Cutouts (South Face Y = 0) ---
        for (ux = USB_X) {
            // Primary rectangular aperture
            translate([ux - USB_PORT_W/2, -1.0, USB_PORT_Z - USB_PORT_H/2])
                cube(size=[USB_PORT_W, WALL + 2.0, USB_PORT_H], center=false);
                
            // 45° Lead-in chamfer for overmolded USB-C boot collars
            translate([ux, 0.4, USB_PORT_Z])
                rotate([0, 0, 0])
                    hull() {
                        translate([-USB_PORT_W/2, -1.5, -USB_PORT_H/2])
                            cube([USB_PORT_W, 0.1, USB_PORT_H]);
                        translate([-(USB_PORT_W + 2.4)/2, -0.5, -(USB_PORT_H + 2.4)/2])
                            cube([USB_PORT_W + 2.4, 0.1, USB_PORT_H + 2.4]);
                    }
        }
        // --- Cable Inflow Gland on West Flank (X = 0) ---
        // Ø 6.2 mm bore for shielded 16-wire harness from Front Node
        translate([-1.0, PCB_OFFSET_Y + 12.0, USB_PORT_Z + 1.0])
            rotate([0, 90, 0])
                cylinder(r=3.1, h=WALL + 2.5, center=false);
                
        // Internal zip-tie strain-relief tie-down anchor channel
        translate([WALL + 2.5, PCB_OFFSET_Y + 12.0 - 1.25, 0])
            cube(size=[2.5, 2.5, COCKPIT_BLOCK_H - 3.0], center=false);
            
        // --- M2.5 Pilot Holes in PCB Standoff Bosses ---
        translate([PCB_OFFSET_X + 4.0, PCB_OFFSET_Y + 16.0, WALL - 0.5])
            cylinder(r=M2_5_PILOT_HOLE_R, h=STANDOFF_H + 2.0, center=false);
        translate([PCB_OFFSET_X + 72.0, PCB_OFFSET_Y + 16.0, WALL - 0.5])
            cylinder(r=M2_5_PILOT_HOLE_R, h=STANDOFF_H + 2.0, center=false);

        // --- 2x M3 Pilot Holes for Anti-Vibration Clamp / Lid (X = 6.0 and X = 70.0) ---
        translate([6.0, 18.0, COCKPIT_BLOCK_H - 10.0])
            cylinder(r=M3_PILOT_HOLE_R, h=10.5, center=false);
        translate([70.0, 18.0, COCKPIT_BLOCK_H - 10.0])
            cylinder(r=M3_PILOT_HOLE_R, h=10.5, center=false);

        // --- Bottom 3M Dual-Lock Recess (1.2 mm deep, for glovebox floor) ---
        translate([15.0, 5.0, -0.1])
            cube(size=[56.0, 18.0, 1.3], center=false);
            
        // --- Bottom 2x Zip-Tie Channels (for handlebar / tube mounting) ---
        translate([20.0, -0.5, 0])
            cube(size=[4.0, COCKPIT_BLOCK_W + 1.0, 2.2], center=false);
        translate([56.0, -0.5, 0])
            cube(size=[4.0, COCKPIT_BLOCK_W + 1.0, 2.2], center=false);

        // --- Top Perimeter Lid Nesting Step (Nut: 1.0 mm deep, 1.2 mm wide) ---
        difference() {
            translate([WALL - 1.0, WALL - 1.0, COCKPIT_BLOCK_H - 1.5])
                cube([COCKPIT_BLOCK_L - 2*(WALL - 1.0), COCKPIT_BLOCK_W - 2*(WALL - 1.0), 2.0]);
            translate([WALL + 0.3, WALL + 0.3, COCKPIT_BLOCK_H - 2.0])
                cube([COCKPIT_BLOCK_L - 2*(WALL + 0.3), COCKPIT_BLOCK_W - 2*(WALL + 0.3), 3.0]);
        }
    }
}

// -----------------------------------------------------------------------------
// 2. Weatherproof Snap/Screw Lid Plate (Oberteil / Deckel)
// -----------------------------------------------------------------------------
module cockpit_breakout_lid() {
    color([0.28, 0.28, 0.30]) // Anthracite ASA
    difference() {
        union() {
            // Main flush lid plate
            hull() {
                translate([CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
                translate([COCKPIT_BLOCK_L - CORNER_R, COCKPIT_BLOCK_W - CORNER_R, 0])
                    cylinder(r=CORNER_R, h=2.5, center=false);
            }
            
            // Perimeter Interlocking Lip (Feder) that nests into the base tub
            translate([WALL + 0.2, WALL + 0.2, -1.4])
                cube([COCKPIT_BLOCK_L - 2*(WALL + 0.2), COCKPIT_BLOCK_W - 2*(WALL + 0.2), 1.5], center=false);
        }

        // Inner relief cavity to save weight and clear high tall components
        translate([WALL + 1.5, WALL + 1.5, -2.0])
            cube([COCKPIT_BLOCK_L - 2*(WALL + 1.5), COCKPIT_BLOCK_W - 2*(WALL + 1.5), 2.5], center=false);

        // 2x M3 Countersunk Screw Holes matching clamp/body mounting
        translate([6.0, 18.0, -2.0]) {
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false);
            translate([0, 0, 3.0])
                cylinder(r1=M3_SCREW_HOLE_R, r2=3.4, h=1.8, center=false);
        }
        translate([70.0, 18.0, -2.0]) {
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false);
            translate([0, 0, 3.0])
                cylinder(r1=M3_SCREW_HOLE_R, r2=3.4, h=1.8, center=false);
        }

        // Embossed OpenMotorBridge Logo & Port Identification Text
        translate([38.0, 6.0, 2.0])
            linear_extrude(height = 0.8)
                text("OPENMOTORBRIDGE // HUB 05B", size = 2.4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

// -----------------------------------------------------------------------------
// 3. Mechanical Anti-Vibration Strain-Relief Clamping Bar
// -----------------------------------------------------------------------------
module cockpit_breakout_clamp() {
    color([0.30, 0.30, 0.32]) // Stiff clamp bar
    difference() {
        // Main clamping bar spanning over the 5 USB-C plug necks
        translate([2.0, 13.0, 0])
            cube(size=[74.0, 10.0, 4.5], center=false);
            
        // 2x M3 Clearance Holes
        translate([6.0, 18.0, -0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false);
        translate([70.0, 18.0, -0.5])
            cylinder(r=M3_SCREW_HOLE_R, h=6.0, center=false);
            
        // M3 Counterbore pockets for DIN 912 socket head screws
        translate([6.0, 18.0, 2.0])
            cylinder(r=3.1, h=3.0, center=false);
        translate([70.0, 18.0, 2.0])
            cylinder(r=3.1, h=3.0, center=false);
            
        // 5x Semicircular clamping grooves for USB-C cable collars
        for (ux = USB_X) {
            translate([ux, 13.0 - 0.1, 2.2])
                rotate([-90, 0, 0])
                    cylinder(r=2.5, h=10.5, center=false);
        }
    }
}

// -----------------------------------------------------------------------------
// 4. Dummy PCBA 05B Model (Visual Verification & 3D Renders)
// -----------------------------------------------------------------------------
module dummy_cockpit_breakout_pcb() {
    translate([PCB_OFFSET_X, PCB_OFFSET_Y, PCB_Z]) {
        // FR4 PCB Substrate (Black Soldermask)
        color([0.15, 0.15, 0.16])
        difference() {
            cube([PCB_L, PCB_W, PCB_THICK], center=false);
            // 2x M2.5 Mounting Holes (H1 and H2)
            translate([4.0, 16.0, -0.5])
                cylinder(r=1.35, h=PCB_THICK + 1.0, center=false);
            translate([72.0, 16.0, -0.5])
                cylinder(r=1.35, h=PCB_THICK + 1.0, center=false);
        }

        // 5x USB-C Receptacles (Stainless Steel Metallic)
        color([0.82, 0.82, 0.85]) {
            for (px = [9.82, 21.82, 33.82, 45.82, 57.82]) {
                translate([px - 4.47, -0.8, PCB_THICK])
                    cube([8.94, 7.3, 3.2], center=false);
            }
        }

        // U1: Microchip USB2514B QFN-36 Hub Controller at (69.25, 6.41)
        color([0.12, 0.12, 0.14])
            translate([69.25 - 3.0, 6.41 - 3.0, PCB_THICK])
                cube([6.0, 6.0, 0.9], center=false);

        // 5x Pairs of CC 0603 Resistors under J1..J5
        color([0.72, 0.58, 0.35]) {
            for (px = [9.82, 21.82, 33.82, 45.82, 57.82]) {
                translate([px - 1.8, 11.5 - 0.4, PCB_THICK])
                    cube([1.6, 0.8, 0.6], center=false);
                translate([px + 0.2, 11.5 - 0.4, PCB_THICK])
                    cube([1.6, 0.8, 0.6], center=false);
            }
            // Passives around U1 (Crystal, caps, reset)
            translate([60.5 - 0.8, 16.27 - 0.4, PCB_THICK])
                cube([1.6, 0.8, 0.6], center=false);
            translate([65.75 - 0.8, 16.20 - 0.4, PCB_THICK])
                cube([1.6, 0.8, 0.6], center=false);
        }
    }
}

// -----------------------------------------------------------------------------
// Assembly & Presentation Selectors
// -----------------------------------------------------------------------------
if (part == "body") {
    cockpit_breakout_body();
} else if (part == "lid") {
    cockpit_breakout_lid();
} else if (part == "clamp") {
    cockpit_breakout_clamp();
} else if (part == "closed") {
    cockpit_breakout_body();
    translate([0, 0, COCKPIT_BLOCK_H - 0.2])
        cockpit_breakout_lid();
} else if (part == "exploded") {
    // Exploded presentation: Body + PCB + Lid + Clamp
    cockpit_breakout_body();
    translate([0, 0, 12.0])
        dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H + 20.0])
        cockpit_breakout_lid();
    translate([0, 0, COCKPIT_BLOCK_H + 32.0])
        cockpit_breakout_clamp();
} else if (part == "xray") {
    // Semi-transparent housing showing internal PCB
    %cockpit_breakout_body();
    dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H - 0.2])
        %cockpit_breakout_lid();
} else {
    // Default "all" assembly
    cockpit_breakout_body();
    dummy_cockpit_breakout_pcb();
    translate([0, 0, COCKPIT_BLOCK_H + 4.0])
        cockpit_breakout_lid();
}
