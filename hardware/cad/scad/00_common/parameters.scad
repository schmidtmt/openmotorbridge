// =============================================================================
// OpenMotorBridge - Global CAD Parameters & Settings
// =============================================================================
// File: hardware/cad/scad/00_common/parameters.scad
// Description: Global dimensional constants, manufacturing clearances and
//              circle resolution ($fn) for all OpenSCAD modules.
// =============================================================================

// --- 1. Circle & Curve Resolution ---
$fn = 60; // Smooth cylinders and holes for high-quality MJF 3D printing

// --- 2. Central Main Box Dimensions (3-Tier Sandwich) ---
MAIN_BOX_OUTER_L      = 110.0; // Outer length in X (mm)
MAIN_BOX_OUTER_W      = 74.0;  // Outer width in Y (mm)
MAIN_BOX_LOWER_H      = 17.0;  // Lower case height in Z (mm)
MAIN_BOX_MID_H        = 15.0;  // Mid tray height in Z (mm)
MAIN_BOX_LID_H        = 4.0;   // Lid plate thickness in Z (mm)
MAIN_BOX_WALL         = 2.5;   // Nominal wall thickness (mm)
MAIN_BOX_CORNER_POST  = 5.0;   // Corner clamping screw post size (mm)

// --- 3. Satellite Pod Dimensions (Universal Enlarged Envelope) ---
POD_OUTER_L           = 135.0; // Outer length in X (mm)
POD_OUTER_W           = 70.0;  // Outer width in Y (mm)
POD_OUTER_H           = 38.0;  // Outer height in Z (mm)
POD_WALL              = 3.5;   // Nominal wall thickness (mm)
POD_BULKHEAD_X        = 18.0;  // Partition bulkhead position in X (mm)
POD_CHAMBER_L         = 117.0; // Sliding chamber length in X (mm)
POD_CHAMBER_W         = 63.0;  // Sliding chamber width in Y (mm)
POD_CHAMBER_H         = 31.0;  // Sliding chamber height in Z (mm)

// --- 4. Pod Linear Guide Rails (Poka-Yoke Tongue & Groove) ---
POD_GROOVE_W          = 3.0;   // Internal guide groove width in Z (mm)
POD_GROOVE_DEPTH      = 1.5;   // Internal guide groove depth in Y (mm)
POD_GROOVE_LEFT_Z     = 10.0;  // Center height of left groove (mm)
POD_GROOVE_RIGHT_Z    = 18.0;  // Center height of right groove (mm, asym offset)

CARTRIDGE_TONGUE_W    = 2.6;   // Cartridge tongue rail height in Z (mm, 0.2mm clearance)
CARTRIDGE_TONGUE_PROT = 1.4;   // Cartridge tongue protrusion in Y (mm, 0.1mm clearance)
CARTRIDGE_CHAMFER_L   = 4.0;   // 30° lead-in chamfer nose length (mm)

// --- 5. Cartridge Dimensions (Enlarged Universal Sled) ---
CARTRIDGE_BASE_L      = 116.0; // Sled length in X (mm)
CARTRIDGE_BASE_W      = 58.0;  // Sled width in Y (mm)
CARTRIDGE_BASE_H      = 28.0;  // Sled height in Z (mm)
CARTRIDGE_FACE_L      = 4.0;   // Front faceplate thickness in X (mm)
CARTRIDGE_FACE_W      = 64.0;  // Front faceplate width in Y (mm)
CARTRIDGE_FACE_H      = 34.0;  // Front faceplate height in Z (mm)

// --- 5a. RF Interface & Sealing Dimensions ---
SMA_BORE_R            = 3.25;  // Ø 6.5 mm through-hole for standard SMA bulkhead
SMA_ORECESS_R         = 4.75;  // Ø 9.5 mm recess for waterproof silicone O-ring
SMA_ORECESS_DEPTH     = 1.2;   // 1.2 mm deep O-ring compression pocket

// --- 5b. Magnetic Anti-Theft Lock System ---
LATCH_PIVOT_X         = 58.0;  // Center pivot position along sled X (mm)
LATCH_MAGNET_X        = 46.0;  // Ferromagnetic anchor position along sled X (mm)
LATCH_TOOTH_X         = 70.0;  // Locking sawtooth pawl position along sled X (mm)
LATCH_ARM_H           = 6.0;   // Rocker lever height in Z (mm)
LATCH_ARM_THICK       = 2.6;   // Rocker beam thickness in Y (mm)
LATCH_MAGNET_PIN_DIA  = 6.2;   // Bore for Ø 6.0 mm steel dowel pin (mm)
LATCH_SPRING_DIA      = 3.8;   // Bore for Ø 3.5 mm return compression spring (mm)

// --- 6. Standard Captive Hex Nut Pockets (DIN 934 / DIN 985 with +0.2 mm MJF/FDM clearance) ---
NUT_M2_SW             = 4.2;   // M2 across flats (nominal 4.0 mm)
NUT_M2_H              = 1.8;   // M2 thickness (nominal 1.6 mm)
NUT_M2_5_SW           = 5.2;   // M2.5 across flats (nominal 5.0 mm)
NUT_M2_5_H            = 2.2;   // M2.5 thickness (nominal 2.0 mm)
NUT_M3_SW             = 5.7;   // M3 across flats (nominal 5.5 mm)
NUT_M3_H              = 2.6;   // M3 thickness (nominal 2.4 mm)
NUT_M4_SW             = 7.2;   // M4 across flats (nominal 7.0 mm)
NUT_M4_H              = 3.4;   // M4 thickness (nominal 3.2 mm)
NUT_M5_SW             = 8.2;   // M5 across flats (nominal 8.0 mm)
NUT_M5_H              = 4.2;   // M5 thickness (nominal 4.0 mm)

// Direct Plastic Thread-Forming / Self-Tapping Pilot Holes in PA12 (100% Soldering-Iron Free)
M2_PILOT_HOLE_R       = 0.85;  // Core hole for M2 screws in PA12 (Ø 1.7 mm)
M2_5_PILOT_HOLE_R     = 1.05;  // Core hole for M2.5 screws in PA12 (Ø 2.1 mm)
M3_PILOT_HOLE_R       = 1.25;  // Core hole for M3 screws in PA12 (Ø 2.5 mm)

// --- 7. Screw & Clearance Dimensions ---
M2_SCREW_HOLE_R       = 1.1;   // M2 clearance hole (r = 1.1 mm -> Ø 2.2 mm)
M2_5_SCREW_HOLE_R     = 1.4;   // M2.5 clearance hole (r = 1.4 mm -> Ø 2.8 mm)
M3_SCREW_HOLE_R       = 1.65;  // M3 clearance hole (r = 1.65 mm -> Ø 3.3 mm)
M4_SCREW_HOLE_R       = 2.2;   // M4 clearance hole (r = 2.2 mm -> Ø 4.4 mm)
M8_BORE_R             = 4.0;   // M8 cable through-bore (r = 4.0 mm -> Ø 8.0 mm)
M8_STUDS_OUTER_R      = 6.0;   // M8 neck outer radius (Ø 12.0 mm)

// --- 8. Universal Front Node Enclosure Dimensions (Type E: 98 x 68 x 25 mm) ---
FRONT_NODE_PCB_L      = 82.0;  // PCB length in X (mm, PCBA 05)
FRONT_NODE_PCB_W      = 50.0;  // PCB width in Y (mm, PCBA 05)
FRONT_NODE_PCB_H      = 1.6;   // PCB thickness in Z (mm)
FRONT_NODE_PCB_R      = 2.5;   // PCB corner radius (mm)

FRONT_NODE_CHAMBER_L  = 86.0;  // Internal chamber length in X (mm, 2mm margin per side)
FRONT_NODE_CHAMBER_W  = 56.0;  // Internal chamber width in Y (mm, 3mm margin per side)
FRONT_NODE_TUB_H      = 17.5;  // Lower tub depth in Z (mm)
FRONT_NODE_LID_H      = 7.5;   // Upper lid height in Z (mm)
FRONT_NODE_WALL       = 2.5;   // Wall thickness in HP MJF PA12 (mm)
FRONT_NODE_CORNER_R   = 4.0;   // Outer enclosure corner radius (mm)

FRONT_NODE_OUTER_L    = FRONT_NODE_CHAMBER_L + 2 * FRONT_NODE_WALL + 7.0; // 98.0 mm
FRONT_NODE_OUTER_W    = FRONT_NODE_CHAMBER_W + 2 * FRONT_NODE_WALL + 7.0; // 68.0 mm
FRONT_NODE_OUTER_H    = FRONT_NODE_TUB_H + FRONT_NODE_LID_H;              // 25.0 mm

// PCB Standoff Heights & Radii (100% Soldering-Iron Free)
FRONT_NODE_STANDOFF_H = 3.0;   // Height of PCB standoffs from floor (mm)
FRONT_NODE_STANDOFF_R = 3.0;   // Outer radius of M2.5 screw bosses (mm)
FRONT_NODE_CORE_HOLE_R= M2_5_PILOT_HOLE_R; // Core hole for direct M2.5 screw engagement (Ø 2.1 mm)

// AMPS 4-Hole Mounting Pattern (38 x 30 mm with DIN 934 M4 Captive Nut Pockets)
AMPS_SPACING_X        = 38.0;  // AMPS hole distance in X (mm)
AMPS_SPACING_Y        = 30.0;  // AMPS hole distance in Y (mm)
AMPS_NUT_SW           = NUT_M4_SW; // Captive M4 hex nut pocket across flats (7.2 mm)
AMPS_NUT_H            = NUT_M4_H;  // Captive M4 hex nut pocket depth (3.4 mm)

// Acoustic Vent for Knowles SPH0645 MEMS
FRONT_NODE_MIC_HOLE_R = 1.25;  // Sound canal radius (Ø 2.5 mm)
FRONT_NODE_MIC_MEMB_R = 3.0;   // Gore ePTFE membrane pocket radius (Ø 6.0 mm)
FRONT_NODE_MIC_MEMB_D = 0.8;   // Membrane pocket depth (mm)

