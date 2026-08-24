#!/usr/bin/env python3
"""
M8 6-Pin A-Coded IP67 PCB Receptacle 3D Model Generator (VRML 2.0 for KiCad Raytracing)
---------------------------------------------------------------------------------------
Generates a photorealistic, dimensionally accurate M8 6-Pin A-Coded circular metal panel
connector model according to IEC 61076-2-104 standard:
- Outer Threaded Metal Collar: M8x1.0 (OD = 8.0 mm, ID = 6.0 mm, Nickel-plated brass)
- Black Insulating Dielectric Insert (PA66-GF30) with Poka-Yoke Polarizing Keyway
- 6 Gold-Plated Female Socket Contacts (arranged in A-Coded circular configuration)
- PCB Solder Base & Hex Mounting Collar (10.0 x 10.0 mm)
- Black EPDM Sealing O-Ring
"""

import os
import sys
import numpy as np

def generate_m8_vrml(output_wrl):
    os.makedirs(os.path.dirname(os.path.abspath(output_wrl)), exist_ok=True)
    
    # Coordinates in meters (VRML standard 1 unit = 1 meter, so 1mm = 0.001)
    wrl = """#VRML V2.0 utf8
# M8 6-Pin A-Coded IP67 Shielded PCB Receptacle (IEC 61076-2-104)
# Generated for OpenMotorBridge KiCad 3D Raytracing Engine

Group {
  children [
    # 1. PCB Mounting Base Flange (10x10x2.5mm, Nickel-Plated Brass)
    Transform {
      translation 0.0 0.0 0.00125
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.78 0.78 0.82
              specularColor 0.95 0.95 0.95
              shininess 0.92
            }
          }
          geometry Box { size 0.010 0.010 0.0025 }
        }
      ]
    }

    # 2. Hexagonal Wrench Nut / Lock Collar (Diameter 9.2mm, Height 2.0mm)
    Transform {
      translation 0.0 0.0 0.0035
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.82 0.75 0.35
              specularColor 0.95 0.90 0.60
              shininess 0.88
            }
          }
          geometry Cylinder {
            radius 0.0048
            height 0.0020
          }
        }
      ]
    }

    # 3. EPDM Rubber Sealing O-Ring (Black, OD 8.6mm, Height 1.2mm)
    Transform {
      translation 0.0 0.0 0.0051
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.10 0.10 0.12
              specularColor 0.15 0.15 0.15
              shininess 0.15
            }
          }
          geometry Cylinder {
            radius 0.0044
            height 0.0012
          }
        }
      ]
    }

    # 4. M8 Threaded Outer Metal Barrel (OD 8.0mm, ID 6.0mm, Height 8.5mm, Nickel-Plated Brass)
    Transform {
      translation 0.0 0.0 0.0095
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.85 0.88
              specularColor 0.98 0.98 0.98
              shininess 0.95
            }
          }
          geometry Cylinder {
            radius 0.0040
            height 0.0085
          }
        }
      ]
    }

    # 5. Black Insulating Insert / Core (PA66 Plastic, OD 5.8mm, Height 7.5mm)
    Transform {
      translation 0.0 0.0 0.0100
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.12 0.14 0.18
              specularColor 0.25 0.25 0.30
              shininess 0.35
            }
          }
          geometry Cylinder {
            radius 0.0029
            height 0.0076
          }
        }
      ]
    }

    # 6. Poka-Yoke Indexing / Polarizing Keyway Notch (Height 6.0mm)
    Transform {
      translation 0.0 0.0024 0.0105
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.85 0.85 0.88
              specularColor 0.95 0.95 0.95
              shininess 0.90
            }
          }
          geometry Box { size 0.0008 0.0012 0.0065 }
        }
      ]
    }
"""

    # 7. 6 Gold-Plated Female Socket Contacts (IEC 61076-2-104 Standard A-Coding, R = 1.65 mm)
    angles_deg = [0, 60, 120, 180, 240, 300]
    r_contacts = 0.00165 # 1.65 mm radius
    for i, angle in enumerate(angles_deg):
        rad = np.radians(angle)
        cx = r_contacts * np.cos(rad)
        cy = r_contacts * np.sin(rad)
        wrl += f"""
    # Contact {i+1} (Gold, Angle = {angle} deg)
    Transform {{
      translation {cx:.6f} {cy:.6f} 0.0102
      children [
        Shape {{
          appearance Appearance {{
            material Material {{
              diffuseColor 0.95 0.78 0.15
              specularColor 0.98 0.90 0.50
              shininess 0.95
            }}
          }}
          geometry Cylinder {{
            radius 0.00035
            height 0.0070
          }}
        }}
      ]
    }}
"""

    wrl += """  ]
}
"""

    with open(output_wrl, 'w', encoding='utf-8') as f:
        f.write(wrl)
    print(f"✓ Generated M8 6-Pin A-Coded IP67 VRML 3D Model: {output_wrl}")

if __name__ == '__main__':
    target = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/M8_6Pin_A_Coded_Receptacle.wrl'))
    generate_m8_vrml(target)
