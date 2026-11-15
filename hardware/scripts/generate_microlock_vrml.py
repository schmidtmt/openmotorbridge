#!/usr/bin/env python3
"""
Generates a detailed, highly accurate VRML 2.0 3D model for:
Molex Micro-Lock Plus 1.25mm 16-Pin (2x08) Vertical SMD Header (505433-1671)
Matching the style, positive locking clip, solder leads, and metal retention tabs of J1.
Scale: KiCad VRML units (1 unit = 2.54 mm).
"""

import math

def s(val):
    """Scale mm to KiCad VRML units"""
    return val / 2.54

class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def add_vertex(self, x, y, z):
        idx = len(self.vertices)
        self.vertices.append((s(x), s(y), s(z)))
        return idx

    def add_quad(self, v0, v1, v2, v3):
        self.faces.append([v0, v1, v2, v3])

    def add_tri(self, v0, v1, v2):
        self.faces.append([v0, v1, v2])

    def add_box(self, xmin, xmax, ymin, ymax, zmin, zmax):
        # 8 vertices
        v0 = self.add_vertex(xmin, ymin, zmin)
        v1 = self.add_vertex(xmax, ymin, zmin)
        v2 = self.add_vertex(xmax, ymax, zmin)
        v3 = self.add_vertex(xmin, ymax, zmin)
        v4 = self.add_vertex(xmin, ymin, zmax)
        v5 = self.add_vertex(xmax, ymin, zmax)
        v6 = self.add_vertex(xmax, ymax, zmax)
        v7 = self.add_vertex(xmin, ymax, zmax)

        # 6 faces (counter-clockwise looking from outside)
        self.add_quad(v0, v3, v2, v1) # bottom (zmin)
        self.add_quad(v4, v5, v6, v7) # top (zmax)
        self.add_quad(v0, v1, v5, v4) # front (ymin)
        self.add_quad(v2, v3, v7, v6) # back (ymax)
        self.add_quad(v3, v0, v4, v7) # left (xmin)
        self.add_quad(v1, v2, v6, v5) # right (xmax)

    def add_wedge_y(self, xmin, xmax, y_back, y_front, z_bot, z_top):
        """Triangular prism sloping down in Y towards the front"""
        v0 = self.add_vertex(xmin, y_back, z_bot)
        v1 = self.add_vertex(xmax, y_back, z_bot)
        v2 = self.add_vertex(xmax, y_front, z_bot)
        v3 = self.add_vertex(xmin, y_front, z_bot)
        v4 = self.add_vertex(xmin, y_back, z_top)
        v5 = self.add_vertex(xmax, y_back, z_top)

        self.add_quad(v0, v3, v2, v1) # bottom
        self.add_quad(v0, v1, v5, v4) # back
        self.add_quad(v2, v3, v4, v5) # sloped front
        self.add_tri(v3, v0, v4)      # left
        self.add_tri(v1, v2, v5)      # right

    def to_vrml_indexed_face_set(self):
        pts_str = ",\n            ".join(f"{x:.5f} {y:.5f} {z:.5f}" for x, y, z in self.vertices)
        faces_str = ",\n          ".join(", ".join(map(str, f)) + ", -1" for f in self.faces)
        return f"""IndexedFaceSet {{
        coord Coordinate {{
          point [
            {pts_str}
          ]
        }}
        coordIndex [
          {faces_str}
        ]
      }}"""

def build_model():
    plastic = MeshBuilder()
    metal = MeshBuilder()
    solder_leads = MeshBuilder()
    gold = MeshBuilder()

    # Outer dimensions
    w_half = 13.15 / 2.0  # 6.575 mm
    d_half = 5.60 / 2.0   # 2.80 mm
    h = 5.40              # 5.40 mm
    floor_z = 1.20        # 1.20 mm
    cav_w_half = 5.375    # Cavity width: 10.75 mm
    cav_d_half = 1.90     # Cavity depth: 3.80 mm

    # 1. PLASTIC HOUSING
    # Base floor slab: Z = 0.3 to floor_z
    plastic.add_box(-w_half, w_half, -d_half, d_half, 0.3, floor_z)

    # End walls (left and right)
    plastic.add_box(-w_half, -cav_w_half, -d_half, d_half, floor_z, h)
    plastic.add_box(cav_w_half, w_half, -d_half, d_half, floor_z, h)

    # Back wall: Y = cav_d_half to d_half
    plastic.add_box(-cav_w_half, cav_w_half, cav_d_half, d_half, floor_z, h)

    # Front wall:
    latch_w_half = 2.4   # Central latch half-width: 4.8 mm
    # Left front wall section
    plastic.add_box(-cav_w_half, -latch_w_half, -d_half, -cav_d_half, floor_z, h)
    # Right front wall section
    plastic.add_box(latch_w_half, cav_w_half, -d_half, -cav_d_half, floor_z, h)

    # Central front wall below latch window (Z = floor_z to 2.2 mm)
    plastic.add_box(-latch_w_half, latch_w_half, -d_half, -cav_d_half, floor_z, 2.2)

    # Central front wall upper section (Z = 3.8 to h)
    plastic.add_box(-latch_w_half, latch_w_half, -d_half, -cav_d_half, 3.8, h)

    # Left & right inner pillars beside latch window (Z = 2.2 to 3.8)
    plastic.add_box(-latch_w_half, -1.35, -d_half, -cav_d_half, 2.2, 3.8)
    plastic.add_box(1.35, latch_w_half, -d_half, -cav_d_half, 2.2, 3.8)

    # --- BEFESTIGUNGSKLIPS (PROMINENT POSITIVE LOCK MECHANISM) ---
    # Latch tower protruding forward from Y = -d_half (-2.8 mm) to Y = -3.7 mm
    latch_y_outer = -3.7
    latch_win_x = 1.35     # Window aperture half-width: 2.7 mm
    latch_win_z_bot = 2.0  # Window sill
    latch_win_z_top = 3.85 # Window crossbar underside

    # Left latch pillar (X = -latch_w_half to -latch_win_x)
    plastic.add_box(-latch_w_half, -latch_win_x, latch_y_outer, -d_half, 0.8, h)
    # Right latch pillar (X = latch_win_x to latch_w_half)
    plastic.add_box(latch_win_x, latch_w_half, latch_y_outer, -d_half, 0.8, h)
    # Latch sill under window
    plastic.add_box(-latch_win_x, latch_win_x, latch_y_outer, -d_half, 0.8, latch_win_z_bot)

    # Latch Crossbar / Bridge (Z = latch_win_z_top to 4.7 mm)
    plastic.add_box(-latch_win_x, latch_win_x, latch_y_outer, -d_half, latch_win_z_top, 4.7)

    # Beveled lead-in ramp at top of latch bridge (Z = 4.7 to h = 5.4 mm)
    plastic.add_wedge_y(-latch_w_half, latch_w_half, -d_half, latch_y_outer, 4.7, h)

    # Central locking catch tooth projecting into window (audible click latch!)
    plastic.add_box(-0.85, 0.85, -3.3, -d_half, 3.4, 3.85)

    # Latch side-wing bevels (chamfering the outer latch tower into the front wall)
    plastic.add_box(-latch_w_half - 0.4, -latch_w_half, -3.3, -d_half, 0.8, h - 0.4)
    plastic.add_box(latch_w_half, latch_w_half + 0.4, -3.3, -d_half, 0.8, h - 0.4)

    # Pin channel dividers on front wall (giving J1-style vertical slots)
    for i in range(8):
        px = -4.375 + i * 1.25
        # Vertical slot rib between pins
        if i < 7 and not (-latch_w_half <= px + 0.625 <= latch_w_half):
            plastic.add_box(px + 0.45, px + 0.80, -d_half - 0.15, -d_half, 0.3, 2.4)

    # Inner keying ribs on left/right cavity walls
    plastic.add_box(-cav_w_half, -cav_w_half + 0.4, -0.6, 0.6, floor_z, h)
    plastic.add_box(cav_w_half - 0.4, cav_w_half, -0.6, 0.6, floor_z, h)

    # 2. METAL RETENTION NAILS (MP1, MP2)
    # Left Retention Nail (MP1 at X = -6.35 mm, centered at Y = 0)
    # Side anchor plate
    metal.add_box(-w_half - 0.32, -w_half, -1.2, 1.2, 0.3, 3.8)
    # Solder foot extending out onto PCB pad at Z = 0.05 mm
    metal.add_box(-w_half - 0.95, -w_half + 0.1, -0.85, 0.85, 0.0, 0.28)
    # Bent support tab
    metal.add_box(-w_half - 0.32, -w_half + 0.2, -1.2, 1.2, 3.5, 4.0)

    # Right Retention Nail (MP2 at X = +6.35 mm, centered at Y = 0)
    metal.add_box(w_half, w_half + 0.32, -1.2, 1.2, 0.3, 3.8)
    metal.add_box(w_half - 0.1, w_half + 0.95, -0.85, 0.85, 0.0, 0.28)
    metal.add_box(w_half - 0.2, w_half + 0.32, -1.2, 1.2, 3.5, 4.0)

    # 3. SOLDER LEADS (EXTENDING OUT ONTO PCB PADS LIKE J1)
    # 8 front leads extending forward to Y = -3.4 mm (Pad center at Y = -1.85 to -3.2 mm)
    # 8 rear leads extending backward to Y = +3.4 mm
    lead_w = 0.45
    for i in range(8):
        px = -4.375 + i * 1.25

        # Front solder lead (visible gull-wing / flat pad tab)
        solder_leads.add_box(px - lead_w/2, px + lead_w/2, -3.35, -2.4, 0.0, 0.22)
        # Lead riser into housing
        solder_leads.add_box(px - lead_w/2, px + lead_w/2, -2.5, -1.0, 0.0, 0.5)

        # Rear solder lead
        solder_leads.add_box(px - lead_w/2, px + lead_w/2, 2.4, 3.35, 0.0, 0.22)
        solder_leads.add_box(px - lead_w/2, px + lead_w/2, 1.0, 2.5, 0.0, 0.5)

    # 4. 16 GOLD CONTACT PINS
    pin_w = 0.35
    pin_h = 3.3 # from floor_z up to 4.5 mm
    for i in range(8):
        px = -4.375 + i * 1.25

        # Row 1 (Front Row at Y = -1.0 mm)
        gold.add_box(px - pin_w/2, px + pin_w/2, -1.0 - pin_w/2, -1.0 + pin_w/2, floor_z, floor_z + pin_h)
        gold.add_box(px - pin_w/3, px + pin_w/3, -1.0 - pin_w/3, -1.0 + pin_w/3, floor_z + pin_h, floor_z + pin_h + 0.25)

        # Row 2 (Back Row at Y = +1.0 mm)
        gold.add_box(px - pin_w/2, px + pin_w/2, 1.0 - pin_w/2, 1.0 + pin_w/2, floor_z, floor_z + pin_h)
        gold.add_box(px - pin_w/3, px + pin_w/3, 1.0 - pin_w/3, 1.0 + pin_w/3, floor_z + pin_h, floor_z + pin_h + 0.25)

    vrml = f"""#VRML V2.0 utf8
# Molex Micro-Lock Plus 1.25mm 16-Pin (2x08) Vertical SMD Header (505433-1671)
# High-detail model with prominent positive Befestigungsklips, retention nails & pins.

Group {{
  children [
    # 1. Main Plastic Shrouded Housing with Positive Lock Clip
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.94 0.93 0.90
          ambientIntensity 0.35
          specularColor 0.25 0.25 0.25
          shininess 0.25
        }}
      }}
      geometry {plastic.to_vrml_indexed_face_set()}
    }},

    # 2. Side Solder Retention Nails (MP1 & MP2)
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.85 0.85 0.88
          ambientIntensity 0.45
          specularColor 0.90 0.90 0.95
          shininess 0.80
        }}
      }}
      geometry {metal.to_vrml_indexed_face_set()}
    }},

    # 3. Solder Leads (Tinned Copper / Silver on PCB pads)
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.80 0.80 0.82
          ambientIntensity 0.40
          specularColor 0.85 0.85 0.88
          shininess 0.70
        }}
      }}
      geometry {solder_leads.to_vrml_indexed_face_set()}
    }},

    # 4. 16 Gold Contact Pins
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.88 0.74 0.22
          ambientIntensity 0.4
          specularColor 0.92 0.82 0.35
          shininess 0.65
        }}
      }}
      geometry {gold.to_vrml_indexed_face_set()}
    }}
  ]
}}
"""
    return vrml

if __name__ == "__main__":
    out_path = "hardware/kicad_main_box/3dmodels/Molex_Micro-Lock_Plus_505433-1671_2x08_P1.25mm_Vertical.wrl"
    content = build_model()
    with open(out_path, "w") as f:
        f.write(content)
    print(f"Generated {out_path} ({len(content)} bytes)")
