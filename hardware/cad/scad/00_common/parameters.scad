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

// --- 3. Satellite Pod Dimensions (Universal 1-Pod Housing) ---
POD_OUTER_L           = 100.0; // Outer length in X (mm)
POD_OUTER_W           = 60.0;  // Outer width in Y (mm)
POD_OUTER_H           = 28.0;  // Outer height in Z (mm)
POD_WALL              = 2.5;   // Nominal wall thickness (mm)
POD_BULKHEAD_X        = 22.0;  // Partition bulkhead position in X (mm)
POD_CHAMBER_L         = 78.0;  // Sliding chamber length in X (mm)
POD_CHAMBER_W         = 55.0;  // Sliding chamber width in Y (mm)
POD_CHAMBER_H         = 23.0;  // Sliding chamber height in Z (mm)

// --- 4. Pod Linear Guide Rails (Poka-Yoke Tongue & Groove) ---
POD_GROOVE_W          = 3.0;   // Internal guide groove width in Z (mm)
POD_GROOVE_DEPTH      = 1.5;   // Internal guide groove depth in Y (mm)
POD_GROOVE_LEFT_Z     = 8.2;   // Center height of left groove (mm)
POD_GROOVE_RIGHT_Z    = 14.2;  // Center height of right groove (mm, asym offset)

CARTRIDGE_TONGUE_W    = 2.6;   // Cartridge tongue rail height in Z (mm, 0.2mm clearance)
CARTRIDGE_TONGUE_PROT = 1.4;   // Cartridge tongue protrusion in Y (mm, 0.1mm clearance)
CARTRIDGE_CHAMFER_L   = 4.0;   // 30° lead-in chamfer nose length (mm)

// --- 5. Cartridge Dimensions ---
CARTRIDGE_BASE_L      = 75.0;  // Sled length in X (mm)
CARTRIDGE_BASE_W      = 54.0;  // Sled width in Y (mm)
CARTRIDGE_BASE_H      = 20.5;  // Sled height in Z (mm)
CARTRIDGE_FACE_L      = 4.0;   // Front faceplate thickness in X (mm)
CARTRIDGE_FACE_W      = 58.0;  // Front faceplate width in Y (mm)
CARTRIDGE_FACE_H      = 25.0;  // Front faceplate height in Z (mm)

// --- 6. Thermal Copper Studs (Kühlbolzen) ---
COPPER_STUD_DIA       = 8.0;   // Diameter of thermal copper studs (mm)
COPPER_STUD_R         = COPPER_STUD_DIA / 2.0; // Radius = 4.0 mm

// Main Box Thermal Stud Positions (4x in lower case floor)
MAIN_BOX_CU_POS = [
    [35.0, 25.0], // Position 1 (LM5164 DCDC Buck Regulator)
    [45.0, 25.0], // Position 2 (BQ25798 LiPo Charger)
    [30.0, 48.0], // Position 3 (ESP32-S3 Dual-Core SoC)
    [70.0, 40.0]  // Position 4 (Automotive TVS & LC Filter Zone)
];

// Pod & Cartridge Thermal Stud Positions (2x in floor)
POD_CU_POS = [
    [42.0, 30.0], // Forward thermal zone
    [72.0, 30.0]  // Rearward thermal zone
];

// --- 7. Screw & Clearance Dimensions ---
M2_SCREW_HOLE_R       = 1.1;   // M2 clearance hole (r = 1.1 mm -> Ø 2.2 mm)
M2_5_SCREW_HOLE_R     = 1.4;   // M2.5 clearance hole (r = 1.4 mm -> Ø 2.8 mm)
M3_SCREW_HOLE_R       = 1.65;  // M3 clearance hole (r = 1.65 mm -> Ø 3.3 mm)
M4_SCREW_HOLE_R       = 2.2;   // M4 clearance hole (r = 2.2 mm -> Ø 4.4 mm)
M8_BORE_R             = 4.0;   // M8 cable through-bore (r = 4.0 mm -> Ø 8.0 mm)
M8_STUDS_OUTER_R      = 6.0;   // M8 neck outer radius (Ø 12.0 mm)
