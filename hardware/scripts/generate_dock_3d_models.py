#!/usr/bin/env python3
"""
Generate Photorealistic, True-to-Scale VRML 2.0 3D Models for KiCad PCBA 06:
1. M8 6-Pin + Shield Horizontal Receptacle (m8_6pin_horizontal_receptacle.wrl)
2. MagSafe 6-Pin Magnetic Dock Receptacle (magsafe_6pin_dock_connector.wrl)

Refined for realistic electronics / micro-connector scale:
- Delicately proportioned SMD gull-wing solder leads (0.18mm sheet metal thickness, 0.38mm width)
  instead of chunky "Starkstrom" bars.
- MagSafe body trimmed from 14.8mm down to a sleek 11.8mm width (perfect flush fit with 11.5mm PCB).
- Fine Ø 0.65mm spring-loaded pogo pin plungers with subtle gold plating.
"""

import math
import os

def create_cylinder_ifs(radius, height, segments=32, center=(0,0,0), axis='x', color=(0.82, 0.82, 0.85), spec=(0.95, 0.95, 0.95), shine=0.9):
    cx, cy, cz = center
    points = []
    half = height / 2.0
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
    for i in range(segments):
        nxt = (i + 1) % segments
        p1 = i
        p2 = nxt
        p3 = segments + nxt
        p4 = segments + i
        coordIndex.append(f"{p1}, {p2}, {p3}, {p4}, -1")
    bot_cap = ", ".join(str(i) for i in reversed(range(segments))) + ", -1"
    coordIndex.append(bot_cap)
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
        parts.append(create_cylinder_ifs(radius=4.10, height=0.40, segments=28, center=(tx, 0, 4.0), axis='x',
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

    # 5. 6 Fine Gold Contact Pins (inside M8 circular barrel face at X=-11.0, Ø 0.6mm)
    for i in range(6):
        ang = i * (2.0 * math.pi / 6.0)
        py = 1.9 * math.cos(ang)
        pz = 4.0 + 1.9 * math.sin(ang)
        parts.append(create_cylinder_ifs(radius=0.30, height=3.0, segments=16, center=(-11.0, py, pz), axis='x',
                                         color=(0.88, 0.76, 0.22), spec=(0.95, 0.90, 0.55), shine=0.90))

    # 6. Center Pin (Ø 0.5mm)
    parts.append(create_cylinder_ifs(radius=0.25, height=3.0, segments=16, center=(-11.0, 0, 4.0), axis='x',
                                     color=(0.86, 0.74, 0.20), spec=(0.92, 0.88, 0.50), shine=0.88))

    # 7. Rear Carrier Block (Black PPS / PBT insulator, sitting snugly on PCB, X=-1.5, Y=0, Z=1.5)
    parts.append(create_box_ifs(size=(1.8, 9.8, 2.6), center=(-1.4, 0, 1.3),
                                color=(0.16, 0.17, 0.18), spec=(0.3, 0.3, 0.3), shine=0.35))

    # 8. Delicate Stamped Solder Leads (Real 0.18mm thickness, 0.36mm width)
    # Sits flat on the PCB pads with realistic solder fillet
    pads_y = [-4.5, -3.0, -1.5, 0.0, 1.5, 3.0, 4.5]
    for py in pads_y:
        # Flat solder foot on pad
        parts.append(create_box_ifs(size=(1.2, 0.36, 0.18), center=(-0.3, py, 0.10),
                                    color=(0.88, 0.76, 0.25), spec=(0.92, 0.88, 0.55), shine=0.85))
        # Small bent vertical leg into carrier block
        parts.append(create_box_ifs(size=(0.25, 0.36, 1.2), center=(-0.8, py, 0.65),
                                    color=(0.85, 0.74, 0.22), spec=(0.90, 0.85, 0.50), shine=0.85))
        # Tiny shiny solder meniscus on pad
        parts.append(create_box_ifs(size=(0.8, 0.50, 0.12), center=(-0.2, py, 0.06),
                                    color=(0.78, 0.80, 0.82), spec=(0.95, 0.95, 0.95), shine=0.90))

    wrl_content = "#VRML V2.0 utf8\n# M8 6-Pin + Shield Horizontal Receptacle Model\nGroup {\n  children [\n"
    wrl_content += ",\n".join(parts)
    wrl_content += "\n  ]\n}\n"
    return wrl_content

def generate_magsafe_model():
    parts = []
    # 1. Main Outer Shroud (Sleek Brushed Gunmetal/Titanium Aluminum Alloy)
    # Scaled down to W=11.8mm (flush with 11.5mm PCB!), H=5.0mm, L=5.2mm
    # Centered at X=3.8mm, Z=2.7mm above PCB
    shroud_w = 11.8
    shroud_h = 5.0
    shroud_l = 5.2
    cx = 3.8
    cz = 2.6

    parts.append(create_box_ifs(size=(shroud_l, shroud_w, shroud_h), center=(cx, 0, cz),
                                color=(0.42, 0.44, 0.47), spec=(0.75, 0.78, 0.82), shine=0.85))

    # Rounded Corner Accents (Pill-shaped MagSafe silhouette)
    for sy in [-shroud_w/2 + 0.6, shroud_w/2 - 0.6]:
        parts.append(create_cylinder_ifs(radius=0.6, height=shroud_h - 0.2, segments=20, center=(cx, sy, cz), axis='z',
                                         color=(0.38, 0.40, 0.43), spec=(0.70, 0.74, 0.78), shine=0.80))

    # 2. Recessed Magnetic Docking Face Cavity (Dark Anodized / Graphite Face)
    # Face at X = 6.4mm, cavity recessed to X = 5.2mm
    parts.append(create_box_ifs(size=(1.2, 10.4, 4.0), center=(5.8, 0, cz),
                                color=(0.12, 0.13, 0.15), spec=(0.25, 0.25, 0.25), shine=0.30))

    # 3. Compact N52 Neodymium Magnet Flanks (Slim 1.1mm wide poles on left and right)
    for my in [-4.5, 4.5]:
        parts.append(create_box_ifs(size=(1.0, 1.1, 3.4), center=(5.9, my, cz),
                                    color=(0.65, 0.68, 0.72), spec=(0.98, 0.98, 0.98), shine=0.96))
        # Polished nickel face
        parts.append(create_box_ifs(size=(0.2, 1.0, 3.2), center=(6.4, my, cz),
                                    color=(0.75, 0.78, 0.82), spec=(0.99, 0.99, 0.99), shine=0.98))

    # 4. 6 Fine Gold Pogo Pin Plungers (Realistic Ø 0.65mm micro-contacts)
    # Centered at pad positions Y = [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]
    j2_y = [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]
    for py in j2_y:
        # Fine gold plunger tip (Ø 0.65mm, radius 0.32mm)
        parts.append(create_cylinder_ifs(radius=0.32, height=1.4, segments=16, center=(6.2, py, cz), axis='x',
                                         color=(0.90, 0.78, 0.22), spec=(0.95, 0.90, 0.60), shine=0.95))
        # Subtle gold collar ring
        parts.append(create_cylinder_ifs(radius=0.48, height=0.3, segments=16, center=(5.7, py, cz), axis='x',
                                         color=(0.85, 0.74, 0.20), spec=(0.90, 0.85, 0.50), shine=0.90))

        # Delicate Stamped SMD Gull-Wing Solder Foot on Pad (0.18mm thick, 0.38mm wide)
        parts.append(create_box_ifs(size=(1.4, 0.38, 0.18), center=(0.4, py, 0.10),
                                    color=(0.88, 0.76, 0.24), spec=(0.92, 0.88, 0.55), shine=0.88))
        # Fine bridge entering connector body
        parts.append(create_box_ifs(size=(0.6, 0.38, 0.8), center=(1.1, py, 0.50),
                                    color=(0.85, 0.74, 0.20), spec=(0.90, 0.85, 0.50), shine=0.85))
        # Small silver solder meniscus on pad
        parts.append(create_box_ifs(size=(0.9, 0.55, 0.12), center=(0.3, py, 0.06),
                                    color=(0.78, 0.80, 0.82), spec=(0.95, 0.95, 0.95), shine=0.90))

    # 5. Delicate Lateral SMD Ground Anchor Lugs (Left & Right Flanks)
    parts.append(create_box_ifs(size=(1.2, 0.5, 0.6), center=(1.4, -shroud_w/2 + 0.3, 0.35),
                                color=(0.72, 0.74, 0.77), spec=(0.9, 0.9, 0.9), shine=0.85))
    parts.append(create_box_ifs(size=(1.2, 0.5, 0.6), center=(1.4, shroud_w/2 - 0.3, 0.35),
                                color=(0.72, 0.74, 0.77), spec=(0.9, 0.9, 0.9), shine=0.85))

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
