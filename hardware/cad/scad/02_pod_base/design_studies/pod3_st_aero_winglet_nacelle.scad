// =============================================================================
// OpenMotorBridge - Satellite Pod 3: ST Aero-Winglet Nacelle (Wrapper)
// =============================================================================
// Points to the master direct-football loft model in pod3_st_aero_winglet_football.scad

use <pod3_st_aero_winglet_football.scad>;

module pod3_st_aero_winglet_nacelle() {
    pod3_st_aero_winglet_football();
}

pod3_st_aero_winglet_nacelle();
