#!/usr/bin/env python3
"""
Generate Photorealistic VRML 2.0 3D Models for KiCad PCBA 06:
1. M8 6-Pin + Shield Horizontal Receptacle (m8_6pin_horizontal_receptacle.wrl)
2. MagSafe 6-Pin Magnetic Dock Receptacle (magsafe_6pin_dock_connector.wrl)

Uses IndexedFaceSet with correct outward-pointing CCW normals and specular lighting
for raytraced 3D rendering in KiCad.
"""

import math
import os

def create_cylinder_ifs(radius, height, segments=32, center=(0,0,0), axis='x', color=(0.82, 0.82, 0.85), spec=(0.95, 0.95, 0.95), shine=0.9):
    cx, cy, cz = center
    points = []
    half = height / 2.0
    # Bottom circle (at -half along axis)
    for i in range(segments):
        ang = 2 * math.pi * i / segments
        c = radius * math.cos(ang)
        s = radius * math.sin(ang)
        if axis == 'x':
            points.append((cx - half, cy + c, cz + s))
        elif axis == 'y':
            points.append((cx + c, cy - half, cz + s))
        else:
            points.append((cx + c, cy + s, cz - half))
            
    # Top circle (at +half along axis)
    for i in range(segments):
        ang = 2 * math.pi * i / segments
        c = radius * math.cos(ang)
        s = radius * math.sin(ang)
        if axis == 'x':
            points.append((cx + half, cy + c, cz + s))
        elif axis == 'y':
            points.append((cx + c, cy + half, cz + s))
        else:
            points.append((cx + c, cy + s, cz + half))

    coordIndex = []
    # Side quads (CCW looking from outside)
    for i in range(segments):
        nxt = (i + 1) % segments
        p1 = i
        p2 = nxt
        p3 = segments + nxt
        p4 = segments + i
        coordIndex.append(f"{p1}, {p2}, {p3}, {p4}, -1")
    # Bottom cap (looking from outside -axis, CCW)
    bot_cap = ", ".join(str(i) for i in reversed(range(segments))) + ", -1"
    coordIndex.append(bot_cap)
    # Top cap (looking from outside +axis, CCW)
    top_cap = ", ".join(str(segments + i) for i in range(segments)) + ", -1"
    coordIndex.append(top_cap)

    pts_str = ",\n        ".join(f"{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}" for p in points)
    idx_str = ",\n        ".join(coordIndex)

    return f"""Shape {{
  appearance Appearance {{
    material Material {{
      diffuseColor {color[0]:.3f} {color[1]:.3f} {color[2]:.3f}
      specularColor {spec[0]:.3f} {spec[1]:.3f} {spec[2]:.3f}
      shininess {shine:.2f}
    }}
  }}
  geometry IndexedFaceSet {{
    solid FALSE
    coord Coordinate {{
      point [
        {pts_str}
      ]
    }}
    coordIndex [
      {idx_str}
    ]
  }}
}}"""

def create_box_ifs(size, center=(0,0,0), color=(0.82, 0.82, 0.85), spec=(0.95, 0.95, 0.95), shine=0.9):
    sx, sy, sz = size
    cx, cy, cz = center
    hx, hy, hz = sx/2.0, sy/2.0, sz/2.0
    # 8 vertices:
    # 0: -X -Y -Z
    # 1: +X -Y -Z
    # 2: +X +Y -Z
    # 3: -X +Y -Z
    # 4: -X -Y +Z
    # 5: +X -Y +Z
    # 6: +X +Y +Z
    # 7: -X +Y +Z
    pts = [
        (cx - hx, cy - hy, cz - hz), # 0
        (cx + hx, cy - hy, cz - hz), # 1
        (cx + hx, cy + hy, cz - hz), # 2
        (cx - hx, cy + hy, cz - hz), # 3
        (cx - hx, cy - hy, cz + hz), # 4
        (cx + hx, cy - hy, cz + hz), # 5
        (cx + hx, cy + hy, cz + hz), # 6
        (cx - hx, cy + hy, cz + hz), # 7
    ]
    # Faces with outward CCW vertex ordering
    coordIndex = [
        "0, 3, 2, 1, -1", # -Z bottom
        "4, 5, 6, 7, -1", # +Z top
        "0, 1, 5, 4, -1", # -Y front
        "1, 2, 6, 5, -1", # +X right
        "2, 3, 7, 6, -1", # +Y back
        "3, 0, 4, 7, -1", # -X left
    ]
    pts_str = ",\n        ".join(f"{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}" for p in pts)
    idx_str = ",\n        ".join(coordIndex)

    return f"""Shape {{
  appearance Appearance {{
    material Material {{
      diffuseColor {color[0]:.3f} {color[1]:.3f} {color[2]:.3f}
      specularColor {spec[0]:.3f} {spec[1]:.3f} {spec[2]:.3f}
      shininess {shine:.2f}
    }}
  }}
  geometry IndexedFaceSet {{
    solid FALSE
    coord Coordinate {{
      point [
        {pts_str}
      ]
    }}
    coordIndex [
      {idx_str}
    ]
  }}
}}"""

def generate_m8_model():
    parts = []
    # 1. Main M8 Threaded Barrel (Nickel-plated Brass, OD=8.0mm, L=10.0mm, centered at X=-7.5, Z=4.0)
    parts.append(create_cylinder_ifs(radius=4.0, height=10.0, segments=36, center=(-7.5, 0, 4.0), axis='x',
                                     color=(0.84, 0.85, 0.88), spec=(0.98, 0.98, 0.98), shine=0.92))
    
    # 1b. M8 Thread Ridge Simulation (4 rings)
    for tx in [-4.5, -6.5, -8.5, -10.5]:
        parts.append(create_cylinder_ifs(radius=4.12, height=0.45, segments=28, center=(tx, 0, 4.0), axis='x',
                                         color=(0.76, 0.77, 0.80), spec=(0.9, 0.9, 0.9), shine=0.85))

    # 2. Knurled Flange Collar (OD=10.2mm, L=2.5mm, at X=-2.5, Z=4.0)
    parts.append(create_cylinder_ifs(radius=5.1, height=2.5, segments=36, center=(-2.5, 0, 4.0), axis='x',
                                     color=(0.74, 0.75, 0.78), spec=(0.92, 0.92, 0.92), shine=0.88))
    # Knurl tactile bevel ring
    parts.append(create_cylinder_ifs(radius=5.25, height=1.2, segments=24, center=(-2.5, 0, 4.0), axis='x',
                                     color=(0.68, 0.70, 0.72), spec=(0.85, 0.85, 0.85), shine=0.80))

    # 3. Inner Insulator Core (PA66 Black Nylon, OD=6.4mm, L=9.5mm, at X=-7.8, Z=4.0)
    parts.append(create_cylinder_ifs(radius=3.2, height=9.5, segments=28, center=(-7.8, 0, 4.0), axis='x',
                                     color=(0.12, 0.12, 0.14), spec=(0.25, 0.25, 0.25), shine=0.30))

    # 4. A-Coded Polarization Key
    parts.append(create_box_ifs(size=(1.5, 0.9, 1.2), center=(-12.0, 0.0, 5.8),
                                color=(0.10, 0.10, 0.12), spec=(0.2, 0.2, 0.2), shine=0.2))

    # 5. 6 Gold Pin Contacts (inside M8 circular barrel face at X=-11.0)
    for i in range(6):
        ang = i * (2.0 * math.pi / 6.0)
        py = 1.9 * math.cos(ang)
        pz = 4.0 + 1.9 * math.sin(ang)
        parts.append(create_cylinder_ifs(radius=0.4, height=3.0, segments=16, center=(-11.0, py, pz), axis='x',
                                         color=(0.92, 0.78, 0.22), spec=(0.98, 0.92, 0.60), shine=0.95))

    # 6. Center Pin
    parts.append(create_cylinder_ifs(radius=0.35, height=3.0, segments=16, center=(-11.0, 0, 4.0), axis='x',
                                     color=(0.90, 0.76, 0.20), spec=(0.95, 0.90, 0.55), shine=0.92))

    # 7. Rear Carrier Block (sits on PCB surface, X=-1.2, Y=0, Z=1.6)
    parts.append(create_box_ifs(size=(2.4, 10.4, 3.2), center=(-1.2, 0, 1.6),
                                color=(0.20, 0.21, 0.23), spec=(0.35, 0.35, 0.35), shine=0.4))

    # 8. Solder Leads dropping down to J1 PCB pads 1..7
    pads_y = [-4.5, -3.0, -1.5, 0.0, 1.5, 3.0, 4.5]
    for py in pads_y:
        parts.append(create_box_ifs(size=(1.6, 0.7, 0.4), center=(-0.2, py, 0.2),
                                    color=(0.90, 0.78, 0.24), spec=(0.96, 0.90, 0.60), shine=0.90))
        parts.append(create_box_ifs(size=(0.7, 0.7, 1.8), center=(-0.8, py, 1.0),
                                    color=(0.88, 0.76, 0.22), spec=(0.95, 0.90, 0.55), shine=0.90))

    # 9. Lateral Ground Shield Retention Tabs
    parts.append(create_box_ifs(size=(1.8, 1.0, 2.4), center=(-1.2, -5.2, 1.2),
                                color=(0.75, 0.75, 0.78), spec=(0.9, 0.9, 0.9), shine=0.8))
    parts.append(create_box_ifs(size=(1.8, 1.0, 2.4), center=(-1.2, 5.2, 1.2),
                                color=(0.75, 0.75, 0.78), spec=(0.9, 0.9, 0.9), shine=0.8))

    wrl_content = "#VRML V2.0 utf8\n# M8 6-Pin + Shield Horizontal Receptacle Model\nGroup {\n  children [\n"
    wrl_content += ",\n".join(parts)
    wrl_content += "\n  ]\n}\n"
    return wrl_content

def generate_magsafe_model():
    parts = []
    # 1. Main Outer Shroud (Brushed Titanium / Gunmetal Aluminum Alloy, X=6.5mm, Y=14.8mm, Z=5.8mm, centered at X=4.5, Z=3.1)
    parts.append(create_box_ifs(size=(6.5, 14.8, 5.8), center=(4.5, 0, 3.1),
                                color=(0.52, 0.55, 0.58), spec=(0.85, 0.88, 0.92), shine=0.88))

    # Chamfered corner accents
    for sy in [-7.1, 7.1]:
        parts.append(create_cylinder_ifs(radius=0.7, height=5.6, segments=20, center=(4.5, sy, 3.1), axis='z',
                                         color=(0.48, 0.50, 0.54), spec=(0.80, 0.85, 0.88), shine=0.85))

    # 2. Recessed Magnetic Docking Face Cavity (Dark Ceramic / Anodized Core)
    parts.append(create_box_ifs(size=(1.6, 13.6, 4.8), center=(7.0, 0, 3.1),
                                color=(0.14, 0.15, 0.17), spec=(0.3, 0.3, 0.3), shine=0.35))

    # 3. Dual Neodymium N52 Permanent Magnet Poles (Left & Right Flanks)
    for my in [-5.3, 5.3]:
        parts.append(create_box_ifs(size=(1.5, 2.2, 4.2), center=(7.1, my, 3.1),
                                    color=(0.68, 0.70, 0.74), spec=(0.98, 0.98, 0.98), shine=0.96))
        parts.append(create_box_ifs(size=(0.4, 2.0, 4.0), center=(7.8, my, 3.1),
                                    color=(0.78, 0.80, 0.84), spec=(0.99, 0.99, 0.99), shine=0.98))

    # 4. 6 Precision Gold Pogo / Contact Points (Matching J2 Pad Y Coordinates)
    j2_y = [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]
    for py in j2_y:
        # Front contact pin
        parts.append(create_cylinder_ifs(radius=0.5, height=1.6, segments=20, center=(7.4, py, 3.1), axis='x',
                                         color=(0.94, 0.80, 0.24), spec=(0.98, 0.94, 0.65), shine=0.96))
        # Gold collar rim
        parts.append(create_cylinder_ifs(radius=0.75, height=0.4, segments=20, center=(6.8, py, 3.1), axis='x',
                                         color=(0.88, 0.74, 0.20), spec=(0.92, 0.88, 0.55), shine=0.90))

        # Rear SMD Solder Pin connecting to J2 PCB pad
        parts.append(create_box_ifs(size=(2.4, 0.8, 0.4), center=(0.2, py, 0.2),
                                    color=(0.90, 0.78, 0.24), spec=(0.96, 0.90, 0.60), shine=0.90))
        # Pin bridge into housing
        parts.append(create_box_ifs(size=(1.2, 0.65, 1.8), center=(1.0, py, 1.0),
                                    color=(0.86, 0.74, 0.22), spec=(0.94, 0.88, 0.55), shine=0.88))

    # 5. Lateral SMD Metal Retention Lugs
    parts.append(create_box_ifs(size=(2.0, 1.4, 1.2), center=(1.5, -7.0, 0.6),
                                color=(0.82, 0.82, 0.85), spec=(0.95, 0.95, 0.95), shine=0.90))
    parts.append(create_box_ifs(size=(2.0, 1.4, 1.2), center=(1.5, 7.0, 0.6),
                                color=(0.82, 0.82, 0.85), spec=(0.95, 0.95, 0.95), shine=0.90))

    wrl_content = "#VRML V2.0 utf8\n# MagSafe 6-Pin Magnetic Dock Receptacle Model\nGroup {\n  children [\n"
    wrl_content += ",\n".join(parts)
    wrl_content += "\n  ]\n}\n"
    return wrl_content

if __name__ == '__main__':
    target_dir = 'hardware/kicad_magsafe_dock'
    os.makedirs(target_dir, exist_ok=True)
    m8_path = os.path.join(target_dir, 'm8_6pin_horizontal_receptacle.wrl')
    magsafe_path = os.path.join(target_dir, 'magsafe_6pin_dock_connector.wrl')

    with open(m8_path, 'w', encoding='utf-8') as f:
        f.write(generate_m8_model())
    print(f"✓ Generated {m8_path}")

    with open(magsafe_path, 'w', encoding='utf-8') as f:
        f.write(generate_magsafe_model())
    print(f"✓ Generated {magsafe_path}")
