// =============================================================================
// OpenMotorBridge - CVO 25-Jahre Anniversary Eagle Nacelle (Harley-Davidson ST)
// =============================================================================
// Design-Linie: 25-Jahre-CVO Jubiläumslackierung (1999–2024 CVO Road Glide ST)
// 1. CVO-Farbton: Atlas Silver / Raven Metallic Slate Grey (#475569)
// 2. Adler-Auge: Stechendes Screamin' Eagle Rot/Orange (#ff3b00) als Lichtleiter-Linse
// 3. Predatory Beak: Aerodynamischer Hakenschnabel mit Kehl-Kiel (Zero Stirnfläche)
// 4. Wings & Feathers: 3D-gestaffelte Schwingen-Chevrons zu den 35 mm OEM Struts
// 5. Tail Diffuser: Flach über den Kotflügel gefächerte Stoßfedern
// =============================================================================

include <../00_common/parameters.scad>;
use <parts/007_pod_slide_dock_core.scad>;
use <pod_base_housing.scad>;

// -----------------------------------------------------------------------------
// Geometrische Parameter (Harley ST Fender & Universal-Pod Dock)
// -----------------------------------------------------------------------------
FENDER_R_TRANS = 140.0;
ST_POD_L      = 136.0;
ST_FUSE_W     = 78.0;
ST_DOCK_H     = 40.5;
WING_HALF_SPAN = 130.0;
LEG_DROP_Z     = -32.0;
LEG_LEN_X      = 54.0;

X_POD_FRONT   = -68.0;
X_POD_REAR    = +68.0;
X_BEAK_TIP    = -152.0;
X_TAIL_TIP    = +155.0;

// Farbpalette der 25-Jahre CVO Jubiläums-Sonderedition
COLOR_CVO_GREY     = "#475569"; // CVO Atlas Silver / Raven Metallic Grey
COLOR_CVO_DARK     = "#334155"; // Tiefer Anthrazit-Schatten für Konturen
COLOR_CVO_EYE      = "#ff3b00"; // Screamin' Eagle Feuer-Orange / Rot
COLOR_CVO_BEZEL    = "#1e293b"; // Dunkles Augenhöhlen-Inlay
COLOR_POD_BODY     = "#111827"; // Universal-Pod Blackbox Gehäuse

// =============================================================================
// 1. Adler-Auge (Das rot/orangene Auge der CVO-Lackierung)
// =============================================================================
// Separat fertigbares Bauteil (z.B. 3D-Druck in orange-transparentem Resin/PETG):
// Dient gleichzeitig als optische Status-Linse für openMotorBridge Heartbeat & CAN-LEDs.
module eagle_eye(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        union() {
            // Sichtbare facettierte Greifvogel-Linse mit Prismen-Iris
            hull() {
                // Vorderer Augenwinkel (spitz zur Schnabelwurzel)
                translate([-95.0, 31.0, 29.0]) sphere(r=1.0, $fn=16);
                
                // Obere Brauenkante (Aggressiver Raubvogel-Schwung)
                translate([-82.0, 38.0, 34.5]) sphere(r=1.5, $fn=16);
                
                // Hinterer Augenwinkel (auslaufender Speed-Streifen zur Schläfe)
                translate([-72.0, 38.5, 32.0]) sphere(r=1.2, $fn=16);
                
                // Unterer Lidschwung
                translate([-86.0, 37.0, 28.5]) sphere(r=1.4, $fn=16);
                
                // Zentrales Iris-Prisma (Tritt aus der Facette hervor)
                translate([-84.0, 39.5, 32.0]) sphere(r=2.5, $fn=24);
            }

            // Interner Lichtleiter-Zapfen (Light Pipe zur Pod-Front für PCB-LED)
            hull() {
                translate([-84.0, 36.0, 32.0]) sphere(r=2.0, $fn=16);
                translate([-69.5, 26.0, 28.0]) cylinder(r=1.8, h=2.0, center=true, $fn=16);
            }
        }
    }
}

// Augenhöhlen-Ausschnitt in der Nacelle
module eagle_eye_socket(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        union() {
            hull() {
                translate([-96.0, 30.5, 28.5]) sphere(r=1.6, $fn=16);
                translate([-82.0, 37.5, 34.5]) sphere(r=2.0, $fn=16);
                translate([-71.0, 38.0, 32.0]) sphere(r=1.6, $fn=16);
                translate([-86.0, 36.5, 28.0]) sphere(r=1.8, $fn=16);
                translate([-84.0, 38.0, 32.0]) sphere(r=3.2, $fn=24);
            }
            // Interner Lichtkanal zur Pod-Kammer
            hull() {
                translate([-84.0, 36.0, 32.0]) sphere(r=2.2, $fn=16);
                translate([-67.0, 25.0, 28.0]) cylinder(r=2.2, h=4.0, center=true, $fn=16);
            }
        }
    }
}

// =============================================================================
// 2. Adlerkopf & Schnabel mit V-Brustkiel (Zero Stirnfläche)
// =============================================================================
module eagle_beak_head() {
    union() {
        // A. Oberschnabel & Stirnwulst
        hull() {
            translate([X_POD_FRONT, -18.0, 37.0]) cube([0.5, 36.0, 3.5]);
            translate([X_POD_FRONT, 0, 40.5 - 2.0]) sphere(r=2.0, $fn=16);
            
            translate([-96.0, -24.0, 29.0]) cube([1.0, 48.0, 6.0]);
            translate([-96.0, 0, 36.5]) sphere(r=2.5, $fn=16);
        }
        
        // B. Aggressive Schnabelspitze (Hakenschnabel)
        hull() {
            translate([-96.0, -24.0, 29.0]) cube([1.0, 48.0, 6.0]);
            translate([-96.0, 0, 36.5]) sphere(r=2.5, $fn=16);

            translate([-128.0, -14.0, 16.0]) cube([1.0, 28.0, 4.0]);
            translate([-128.0, 0, 23.0]) sphere(r=2.0, $fn=16);
            
            translate([X_BEAK_TIP, 0, 5.0]) sphere(r=2.0, $fn=16);
            translate([X_BEAK_TIP + 8.0, -4.0, 2.0]) cube([4.0, 8.0, 4.0]);
        }

        // C. Wangen-Facetten & schützende Augenbrauen (Supraorbital Ridge)
        for (s = [-1, 1]) {
            mirror([0, s < 0 ? 1 : 0, 0]) {
                // Obere Schläfen-Facette (läuft über dem Auge vorbei)
                hull() {
                    translate([X_POD_FRONT, 39.0 - 3.5, 40.5 - 3.5]) sphere(r=3.5, $fn=20);
                    translate([X_POD_FRONT, 18.0, 37.0]) cube([0.5, 2.0, 3.5]);
                    translate([-96.0, 24.0, 29.0]) sphere(r=3.0, $fn=20);
                    translate([-96.0, 36.0, 24.0]) sphere(r=2.5, $fn=16);
                }

                // Greifvogel-Augenbraue (Hooded Brow Ridge über dem Auge)
                hull() {
                    translate([X_POD_FRONT, 37.0, 40.0]) sphere(r=1.5, $fn=16);
                    translate([-80.0, 37.5, 36.5]) sphere(r=1.8, $fn=16);
                    translate([-96.0, 26.0, 31.0]) sphere(r=1.5, $fn=16);
                }
                
                // Seitliche Wangen-Einfassung unter dem Auge
                hull() {
                    translate([X_POD_FRONT, 39.0 - 1.0, 2.0]) cube([0.5, 1.0, 36.0]);
                    translate([-96.0, 36.0, 2.0]) cube([0.5, 1.0, 22.0]);
                    translate([-128.0, 14.0, 2.0]) cube([0.5, 1.0, 14.0]);
                    translate([X_BEAK_TIP + 4.0, 0, 2.0]) sphere(r=2.0, $fn=16);
                }

                hull() {
                    translate([-96.0, 24.0, 29.0]) sphere(r=3.0, $fn=16);
                    translate([-96.0, 36.0, 24.0]) sphere(r=2.5, $fn=16);
                    translate([-128.0, 14.0, 16.0]) sphere(r=2.0, $fn=16);
                    translate([X_BEAK_TIP, 0, 5.0]) sphere(r=2.0, $fn=16);
                }
            }
        }

        // D. Dynamischer V-Brustkiel (Aero V-Prow Keel)
        // Schließt die Unterseite aerodynamisch ab
        hull() {
            translate([X_BEAK_TIP + 8.0, 0, 2.0]) sphere(r=2.0, $fn=16);
            translate([-118.0, 0, 1.0]) sphere(r=3.0, $fn=16);
            translate([-118.0, -18.0, 2.0]) cube([1.0, 36.0, 8.0]);
            translate([X_POD_FRONT, -ST_FUSE_W/2.0, 0]) cube([0.5, ST_FUSE_W, 2.5]);
        }
        hull() {
            translate([-118.0, 0, 1.0]) sphere(r=3.0, $fn=16);
            translate([-118.0, -18.0, 2.0]) cube([1.0, 36.0, 8.0]);
            translate([X_POD_FRONT, 0, 1.0]) sphere(r=3.0, $fn=16);
            translate([X_POD_FRONT, -ST_FUSE_W/2.0, 0]) cube([0.5, ST_FUSE_W, 24.0]);
        }
    }
}

// =============================================================================
// 3. Schwingen mit 3D CVO Feather Relieflinien
// =============================================================================
module eagle_wings(side=1) {
    mirror([0, side < 0 ? 1 : 0, 0]) {
        // Haupt-Flügelfläche (Primary Wing Aerofoil)
        hull() {
            translate([-118.0, ST_FUSE_W/2.0 - 4.0, 10.0]) cube([6.0, 4.0, 12.0]);
            translate([+35.0, ST_FUSE_W/2.0 - 4.0, 10.0]) cube([6.0, 4.0, 12.0]);
            translate([-25.0, 75.0, 16.0]) sphere(r=3.5, $fn=20);
            translate([+10.0, 72.0, 10.0]) sphere(r=3.0, $fn=16);
            translate([-27.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z + 14.0]) cube([54.0, 8.0, 6.0]);
        }

        // CVO Feather Relief Chevrons (Gestaffelte Flügelfedern)
        // Feder 1 (Vordere Leitfeder)
        hull() {
            translate([-100.0, ST_FUSE_W/2.0 - 2.0, 14.0]) cube([4.0, 2.0, 6.0]);
            translate([-32.0, 74.0, 19.5]) sphere(r=2.5, $fn=16);
            translate([-25.0, WING_HALF_SPAN - 6.0, LEG_DROP_Z + 18.5]) sphere(r=2.5, $fn=16);
        }
        
        // Feder 2 (Mittlere Schwungfeder)
        hull() {
            translate([-50.0, ST_FUSE_W/2.0 - 2.0, 16.0]) cube([25.0, 2.0, 6.0]);
            translate([-10.0, 74.0, 16.0]) sphere(r=2.5, $fn=16);
            translate([-5.0, WING_HALF_SPAN - 6.0, LEG_DROP_Z + 17.5]) sphere(r=2.5, $fn=16);
        }

        // Feder 3 (Hintere Schwungfeder)
        hull() {
            translate([-10.0, ST_FUSE_W/2.0 - 2.0, 18.0]) cube([35.0, 2.0, 6.0]);
            translate([+12.0, 72.0, 13.5]) sphere(r=2.5, $fn=16);
            translate([+16.0, WING_HALF_SPAN - 6.0, LEG_DROP_Z + 16.0]) sphere(r=2.5, $fn=16);
        }

        // Strut-Befestigungsschenkel mit aerodynamischer Vorderkanten-Fase
        hull() {
            translate([-LEG_LEN_X/2.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z])
                cube([LEG_LEN_X, 8.0, 24.0]);
            translate([-LEG_LEN_X/2.0 - 6.0, WING_HALF_SPAN - 4.0, LEG_DROP_Z + 4.0])
                cube([6.0, 4.0, 16.0]);
        }

        // Schwingen-Endspitzen (Winglet Feather Tips)
        hull() {
            translate([-27.0, WING_HALF_SPAN - 8.0, LEG_DROP_Z + 10.0]) cube([54.0, 8.0, 6.0]);
            translate([-22.0, WING_HALF_SPAN - 12.0, LEG_DROP_Z + 18.0]) cube([44.0, 4.0, 6.0]);
        }
    }
}

// =============================================================================
// 4. Stoßfedern-Heck (Flat Fanned Tail Feathers)
// =============================================================================
module eagle_tail() {
    union() {
        // Zentrale Hauptstoßfeder
        hull() {
            translate([X_POD_REAR - 1.0, -16.0, 2.0]) cube([2.0, 32.0, ST_DOCK_H - 4.0]);
            translate([110.0, -12.0, 2.0]) cube([2.0, 24.0, 14.0]);
            translate([X_TAIL_TIP - 6.0, -6.0, 2.0]) cube([6.0, 12.0, 4.0]);
            translate([X_TAIL_TIP, 0, 3.0]) sphere(r=1.5, $fn=12);
        }

        // Seitlich gestaffelte Heckfedern (3-Tier Tail Feathers)
        for (s = [-1, 1]) {
            mirror([0, s < 0 ? 1 : 0, 0]) {
                hull() {
                    translate([X_POD_REAR - 1.0, 15.0, 2.0]) cube([2.0, 16.0, 28.0]);
                    translate([105.0, 14.0, 2.0]) cube([2.0, 14.0, 10.0]);
                    translate([140.0, 8.0, 2.0]) cube([4.0, 8.0, 3.5]);
                }
                hull() {
                    translate([X_POD_REAR - 1.0, 28.0, 2.0]) cube([2.0, 11.0, 20.0]);
                    translate([95.0, 22.0, 2.0]) cube([2.0, 12.0, 8.0]);
                    translate([122.0, 14.0, 2.0]) cube([4.0, 8.0, 3.0]);
                }
            }
        }
    }
}

// =============================================================================
// 5. Nacelle-Hauptkörper in CVO-Grau mit allen Aussparungen
// =============================================================================
module cvo_eagle_nacelle_body() {
    difference() {
        union() {
            eagle_beak_head();
            translate([X_POD_FRONT, -ST_FUSE_W/2.0, 0])
                cube([ST_POD_L + 0.5, ST_FUSE_W, ST_DOCK_H]);
            eagle_tail();
            for (s = [-1, 1]) eagle_wings(s);
        }

        // Augenhöhlen für die rot/orangenen Adleraugen
        for (s = [-1, 1]) {
            eagle_eye_socket(s);
        }

        // Universal-Pod Einschubdock
        translate([0, 0, 2.5]) {
            pod_slide_dock_subtraction(
                dock_l = ST_POD_L,
                dock_w = 70.8,
                dock_h = 38.2,
                open_sky_h = 50.0
            );
        }

        // Verdeckter Unterflur-Kabelkanal (durch linke Schwinge zum Bike)
        hull() {
            translate([X_POD_FRONT - 2.0, 0, 16.0]) sphere(r=3.0, $fn=16);
            translate([-82.0, 20.0, 14.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-82.0, 20.0, 14.0]) sphere(r=3.0, $fn=16);
            translate([-34.0, 64.0, 9.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-34.0, 64.0, 9.0]) sphere(r=3.0, $fn=16);
            translate([-14.0, 98.0, -5.0]) sphere(r=3.0, $fn=16);
        }
        hull() {
            translate([-14.0, 98.0, -5.0]) sphere(r=3.0, $fn=16);
            translate([-8.0, 122.0, -18.0]) sphere(r=3.0, $fn=16);
        }
        translate([-8.0, 122.0, -24.0]) cube([5.6, 6.0, 22.0], center=true);

        // Harley OEM Strut-Befestigungslöcher (35 mm Lochabstand)
        for (x_bolt = [-17.5, +17.5]) {
            for (s = [-1, 1]) {
                translate([x_bolt, s * (WING_HALF_SPAN - 4.0), LEG_DROP_Z + 14.0])
                    rotate([s * 90, 0, 0]) cylinder(r=4.6, h=16.0, center=true, $fn=24);
            }
        }

        // Fender-Sattel Wölbung (Schmiegt sich an den Harley-Kotflügel)
        translate([0, 0, -(FENDER_R_TRANS - 2.0)]) {
            rotate([0, 90, 0])
                cylinder(r=FENDER_R_TRANS, h=350.0, center=true, $fn=80);
        }
    }
}

// =============================================================================
// Komplettbaugruppe (Multi-Material / Dual-Part Render)
// =============================================================================
module pod3_st_cvo_25_anniversary_eagle() {
    // 1. Nacelle-Rumpf im CVO Atlas Silver / Raven Metallic Grauton
    color(COLOR_CVO_GREY, 1.0)
        cvo_eagle_nacelle_body();

    // 2. Das stechende rot/orangene Adler-Auge (Links & Rechts)
    color(COLOR_CVO_EYE, 1.0) {
        for (s = [-1, 1]) {
            eagle_eye(s);
        }
    }

    // 3. Der Universal-Pod im Schacht
    translate([-POD_OUTER_L/2.0, -POD_OUTER_W/2.0, 2.5]) {
        color(COLOR_POD_BODY, 0.95)
            pod_base_housing();
    }
}

// Direkte Vorschau beim Öffnen in OpenSCAD:
pod3_st_cvo_25_anniversary_eagle();
