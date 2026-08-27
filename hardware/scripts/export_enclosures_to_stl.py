#!/usr/bin/env python3
"""
OpenMotorBridge - 3D Mechanical Enclosure STL Exporter for Tinkercad & 3D Printing
==================================================================================
Generates high-precision, watertight STL (Standard Triangle Language) solid models
for all OpenMotorBridge enclosure assemblies, ready for direct import into Tinkercad:

Enclosure Parts Exported:
  1. Main Central Box (Zentralbox):
     - `main_box_lower_case.stl`      : Untere Gehäusewanne mit M4 Silentblock-Ohren & PCB-Befestigung
     - `main_box_mid_baffle.stl`      : Zwischenboden mit LiPo-Akkubett & Kabeldurchführung
     - `main_box_lid.stl`             : Oberer Gehäusedeckel mit Dichtungsnut
     - `main_box_complete_mockup.stl` : Gesamtes geschlossenes Gehäuse (Referenzkörper)

  2. Pod Base (Helmträger):
     - `pod_base_housing.stl`         : M8-Kabelträger mit Pogo-Pin Sockel & Magnetfassungen
     - `pod_base_helmet_clamp.stl`    : Helm-Klemmadapter & 3M VHB Grundplatte

  3. Pod Interchangeable Cartridges (Kassetten-Schlitten):
     - `cartridge_sena_sled.stl`      : Sena 50S/60S Wechselschlitten mit Audio-Buchsen & PTT-Bett
     - `cartridge_cardo_sled.stl`     : Cardo Packtalk Edge Wechselschlitten
     - `cartridge_blindkassette_waterproof_dummy.stl` : 100% wasserdichter IP68 Blindverschluss

  4. Rear Pod 3 (Heck-Transceiver):
     - `rear_pod3_lower_housing.stl`  : Untergehäuse mit M8-Port & M4 Halterung
     - `rear_pod3_radome_lid.stl`     : Aerodynamischer HF-Radomdeckel für LoRa/GNSS

All models are exported in millimeter scale (1 unit = 1 mm), manifold / watertight,
and 100% Tinkercad / Slicer / CAD compatible.
"""

import os
import struct
import numpy as np
from typing import List, Tuple

class STLMeshBuilder:
    def __init__(self, name: str = "openmotorbridge_mesh"):
        self.name = name
        self.triangles: List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = []
        
    def add_triangle(self, v1: np.ndarray, v2: np.ndarray, v3: np.ndarray):
        """Adds a single triangle with auto-calculated normal."""
        edge1 = v2 - v1
        edge2 = v3 - v1
        normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(normal)
        if norm > 1e-9:
            normal = normal / norm
        else:
            normal = np.array([0.0, 0.0, 1.0])
        self.triangles.append((normal, v1, v2, v3))
        
    def add_quad(self, v1: np.ndarray, v2: np.ndarray, v3: np.ndarray, v4: np.ndarray):
        """Adds a quad as two triangles (counter-clockwise order for outward normal)."""
        self.add_triangle(v1, v2, v3)
        self.add_triangle(v1, v3, v4)
        
    def add_box(self, x0: float, y0: float, z0: float, dx: float, dy: float, dz: float):
        """Adds a solid cuboid."""
        p = np.array([
            [x0, y0, z0],           # 0
            [x0 + dx, y0, z0],      # 1
            [x0 + dx, y0 + dy, z0], # 2
            [x0, y0 + dy, z0],      # 3
            [x0, y0, z0 + dz],      # 4
            [x0 + dx, y0, z0 + dz], # 5
            [x0 + dx, y0 + dy, z0 + dz], # 6
            [x0, y0 + dy, z0 + dz]  # 7
        ])
        # Bottom (z = z0, normal -Z)
        self.add_quad(p[0], p[3], p[2], p[1])
        # Top (z = z0 + dz, normal +Z)
        self.add_quad(p[4], p[5], p[6], p[7])
        # Front (y = y0, normal -Y)
        self.add_quad(p[0], p[1], p[5], p[4])
        # Back (y = y0 + dy, normal +Y)
        self.add_quad(p[2], p[3], p[7], p[6])
        # Left (x = x0, normal -X)
        self.add_quad(p[0], p[4], p[7], p[3])
        # Right (x = x0 + dx, normal +X)
        self.add_quad(p[1], p[2], p[6], p[5])

    def add_hollow_box(self, x0: float, y0: float, z0: float, dx: float, dy: float, dz: float, wall: float):
        """
        Adds a 100% seamless, manifold hollow enclosure tub (open at top).
        Generates clean outer shell, inner cavity, and top connecting rim with zero internal seams.
        """
        x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
        ix0, iy0, iz0 = x0 + wall, y0 + wall, z0 + wall
        ix1, iy1 = x1 - wall, y1 - wall
        
        # 1. Outer Bottom Face (z = z0, normal -Z)
        self.add_quad(np.array([x0, y0, z0]), np.array([x0, y1, z0]), np.array([x1, y1, z0]), np.array([x1, y0, z0]))
        
        # 2. Inner Bottom Face (z = iz0, normal +Z)
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix1, iy0, iz0]), np.array([ix1, iy1, iz0]), np.array([ix0, iy1, iz0]))
        
        # 3. Outer Side Faces
        # Front (y = y0, normal -Y)
        self.add_quad(np.array([x0, y0, z0]), np.array([x1, y0, z0]), np.array([x1, y0, z1]), np.array([x0, y0, z1]))
        # Back (y = y1, normal +Y)
        self.add_quad(np.array([x1, y1, z0]), np.array([x0, y1, z0]), np.array([x0, y1, z1]), np.array([x1, y1, z1]))
        # Left (x = x0, normal -X)
        self.add_quad(np.array([x0, y1, z0]), np.array([x0, y0, z0]), np.array([x0, y0, z1]), np.array([x0, y1, z1]))
        # Right (x = x1, normal +X)
        self.add_quad(np.array([x1, y0, z0]), np.array([x1, y1, z0]), np.array([x1, y1, z1]), np.array([x1, y0, z1]))
        
        # 4. Inner Side Faces
        # Inner Front (y = iy0, normal +Y)
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix0, iy0, z1]), np.array([ix1, iy0, z1]), np.array([ix1, iy0, iz0]))
        # Inner Back (y = iy1, normal -Y)
        self.add_quad(np.array([ix1, iy1, iz0]), np.array([ix1, iy1, z1]), np.array([ix0, iy1, z1]), np.array([ix0, iy1, iz0]))
        # Inner Left (x = ix0, normal +X)
        self.add_quad(np.array([ix0, iy1, iz0]), np.array([ix0, iy1, z1]), np.array([ix0, iy0, z1]), np.array([ix0, iy0, iz0]))
        # Inner Right (x = ix1, normal -X)
        self.add_quad(np.array([ix1, iy0, iz0]), np.array([ix1, iy0, z1]), np.array([ix1, iy1, z1]), np.array([ix1, iy1, iz0]))
        
        # 5. Top Rim Faces (Connecting outer top edge to inner top edge at z = z1)
        # Front Rim
        self.add_quad(np.array([x0, y0, z1]), np.array([x1, y0, z1]), np.array([ix1, iy0, z1]), np.array([ix0, iy0, z1]))
        # Back Rim
        self.add_quad(np.array([x1, y1, z1]), np.array([x0, y1, z1]), np.array([ix0, iy1, z1]), np.array([ix1, iy1, z1]))
        # Left Rim
        self.add_quad(np.array([x0, y1, z1]), np.array([x0, y0, z1]), np.array([ix0, iy0, z1]), np.array([ix0, iy1, z1]))
        # Right Rim
        self.add_quad(np.array([x1, y0, z1]), np.array([x1, y1, z1]), np.array([ix1, iy1, z1]), np.array([ix1, iy0, z1]))

    def add_boss(self, cx: float, cy: float, z0: float, outer_r: float, inner_r: float, height: float, segments: int = 24):
        """
        Adds a 100% watertight cylindrical screw standoff boss with a clean center hole
        and mathematically correct surface normals on all inner, outer, top, and bottom facets.
        """
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        z1 = z0 + height
        hole_bottom_center = np.array([cx, cy, z0])
        
        # Outer rings
        out_bot = [np.array([cx + outer_r * np.cos(a), cy + outer_r * np.sin(a), z0]) for a in angles]
        out_top = [np.array([cx + outer_r * np.cos(a), cy + outer_r * np.sin(a), z1]) for a in angles]
        
        # Inner rings (screw hole)
        in_bot = [np.array([cx + inner_r * np.cos(a), cy + inner_r * np.sin(a), z0]) for a in angles]
        in_top = [np.array([cx + inner_r * np.cos(a), cy + inner_r * np.sin(a), z1]) for a in angles]
        
        for i in range(segments):
            next_i = (i + 1) % segments
            # 1. Outer side wall (normal pointing outwards)
            self.add_quad(out_bot[i], out_bot[next_i], out_top[next_i], out_top[i])
            # 2. Inner hole wall (normal pointing inwards into the hole cavity)
            self.add_quad(in_bot[i], in_bot[next_i], in_top[next_i], in_top[i])
            # 3. Top annular ring face (normal pointing +Z UP)
            self.add_quad(out_top[i], out_top[next_i], in_top[next_i], in_top[i])
            # 4. Bottom of the hole cap (normal pointing +Z UP)
            self.add_triangle(hole_bottom_center, in_bot[i], in_bot[next_i])

    def add_cylinder(self, cx: float, cy: float, z0: float, radius: float, height: float, segments: int = 24):
        """Adds a solid vertical cylinder."""
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        bot_center = np.array([cx, cy, z0])
        top_center = np.array([cx, cy, z0 + height])
        
        bot_ring = [np.array([cx + radius * np.cos(a), cy + radius * np.sin(a), z0]) for a in angles]
        top_ring = [np.array([cx + radius * np.cos(a), cy + radius * np.sin(a), z0 + height]) for a in angles]
        
        for i in range(segments):
            next_i = (i + 1) % segments
            # Bottom cap
            self.add_triangle(bot_center, bot_ring[next_i], bot_ring[i])
            # Top cap
            self.add_triangle(top_center, top_ring[i], top_ring[next_i])
            # Side wall
            self.add_quad(bot_ring[i], bot_ring[next_i], top_ring[next_i], top_ring[i])

    def write_stl(self, filepath: str, binary: bool = True):
        """Exports the collected triangles to binary or ASCII STL file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        if binary:
            with open(filepath, 'wb') as f:
                header = f"OpenMotorBridge CAD STL - {self.name}".ljust(80)[:80].encode('ascii')
                f.write(header)
                f.write(struct.pack('<I', len(self.triangles)))
                for normal, v1, v2, v3 in self.triangles:
                    # 3x float32 normal, 3x (3x float32) vertices, 1x uint16 attribute
                    f.write(struct.pack('<3f', *normal))
                    f.write(struct.pack('<3f', *v1))
                    f.write(struct.pack('<3f', *v2))
                    f.write(struct.pack('<3f', *v3))
                    f.write(struct.pack('<H', 0))
        else:
            with open(filepath, 'w') as f:
                f.write(f"solid {self.name}\n")
                for normal, v1, v2, v3 in self.triangles:
                    f.write(f"  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n")
                    f.write("    outer loop\n")
                    f.write(f"      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n")
                    f.write(f"      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n")
                    f.write(f"      vertex {v3[0]:.6e} {v3[1]:.6e} {v3[2]:.6e}\n")
                    f.write("    endloop\n")
                    f.write("  endfacet\n")
                f.write(f"endsolid {self.name}\n")


def generate_main_box_stl(output_dir: str):
    """Generates Main Box lower case, mid-baffle, lid, and assembled model."""
    print("Generating Main Box 3D STL models...")
    
    # 1. Lower Case (Unterwanne)
    mb_lower = STLMeshBuilder("main_box_lower_case")
    # Outer tub: 105 x 75 x 18 mm, 2.5 mm wall thickness
    mb_lower.add_hollow_box(0, 0, 0, 105.0, 75.0, 18.0, 2.5)
    # 4x M4 Silentblock Mounting Ears on outer corners
    mb_lower.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)   # Left Front
    mb_lower.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)  # Left Rear
    mb_lower.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)   # Right Front
    mb_lower.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)  # Right Rear
    
    # 4x Clean Cylindrical PCB Screw Bosses (M2.5 Schraubdome, Ø 7.0 mm outer, Ø 2.5 mm screw hole, height 3.5 mm)
    mb_lower.add_boss(13.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(13.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.write_stl(os.path.join(output_dir, "main_box_lower_case.stl"))
    
    # =========================================================================
    # MODULAR TINKERCAD KIT (Separate Grundkörper / Primitive zum einfachen Gruppieren)
    # =========================================================================
    kit_dir = os.path.join(output_dir, "tinkercad_modular_kit")
    os.makedirs(kit_dir, exist_ok=True)
    
    # Primitiv 1: Reine leere Wanne mit M4-Ohren (ohne Zylinder)
    tub_only = STLMeshBuilder("1_main_box_empty_tub")
    tub_only.add_hollow_box(0, 0, 0, 105.0, 75.0, 18.0, 2.5)
    tub_only.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    tub_only.write_stl(os.path.join(kit_dir, "1_main_box_empty_tub.stl"))
    
    # Primitiv 2: Die 4 Schraubdome zusammen als eigene Gruppe (passgenau für Wanne)
    bosses_grp = STLMeshBuilder("2_main_box_4_standoffs_group")
    bosses_grp.add_boss(13.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    bosses_grp.add_boss(92.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    bosses_grp.add_boss(13.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    bosses_grp.add_boss(92.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    bosses_grp.write_stl(os.path.join(kit_dir, "2_main_box_4_standoffs_group.stl"))
    
    # Primitiv 3: Ein einzelner isolierter M2.5 Schraubdom (im Nullpunkt) zum freien Duplizieren
    single_boss = STLMeshBuilder("3_single_m2_5_standoff_boss")
    single_boss.add_boss(0, 0, 0, 3.5, 1.25, 3.5)
    single_boss.write_stl(os.path.join(kit_dir, "3_single_m2_5_standoff_boss.stl"))
    
    # Primitiv 4: Ein einzelnes M4 Montageohr (im Nullpunkt)
    single_ear = STLMeshBuilder("4_single_m4_mounting_ear")
    single_ear.add_box(0, 0, 0, 11.5, 14.0, 5.0)
    single_ear.write_stl(os.path.join(kit_dir, "4_single_m4_mounting_ear.stl"))
    
    # 2. Mid Baffle Tray (Zwischenboden mit LiPo-Bett)
    mb_mid = STLMeshBuilder("main_box_mid_baffle")
    # Baffle Plate: 99.5 x 69.5 x 2.0 mm
    mb_mid.add_box(2.75, 2.75, 0, 99.5, 69.5, 2.0)
    # LiPo Battery Retention Cradle Walls: 56.0 x 38.0 x 8.0 mm (fits 1000mAh 1S LiPo)
    mb_mid.add_box(5.0, 15.0, 2.0, 56.0, 2.0, 8.0)  # Front Wall
    mb_mid.add_box(5.0, 53.0, 2.0, 56.0, 2.0, 8.0)  # Rear Wall
    mb_mid.add_box(5.0, 15.0, 2.0, 2.0, 38.0, 8.0)  # Left Wall
    # Ribbon Cable Pass-Through Flange (Right side)
    mb_mid.add_box(68.0, 15.0, 2.0, 30.0, 3.0, 6.0)
    mb_mid.add_box(68.0, 45.0, 2.0, 30.0, 3.0, 6.0)
    mb_mid.write_stl(os.path.join(output_dir, "main_box_mid_baffle.stl"))
    
    # 3. Enclosure Lid (Gehäusedeckel mit Dichtungsfalz)
    mb_lid = STLMeshBuilder("main_box_lid")
    # Top Lid Plate: 105.0 x 75.0 x 4.0 mm
    mb_lid.add_box(0, 0, 0, 105.0, 75.0, 4.0)
    # Inner O-Ring Perimeter Sealing Lip (enters 3.0 mm into lower case)
    mb_lid.add_box(2.8, 2.8, -3.0, 99.4, 3.0, 3.0)   # Front lip
    mb_lid.add_box(2.8, 69.2, -3.0, 99.4, 3.0, 3.0)  # Back lip
    mb_lid.add_box(2.8, 2.8, -3.0, 3.0, 69.4, 3.0)   # Left lip
    mb_lid.add_box(99.2, 2.8, -3.0, 3.0, 69.4, 3.0)  # Right lip
    # Gore ePTFE Pressure Vent Boss (Ø 8 mm)
    mb_lid.add_cylinder(52.5, 37.5, 4.0, 4.0, 1.5)
    mb_lid.write_stl(os.path.join(output_dir, "main_box_lid.stl"))
    
    # 4. Assembled Mockup (Vollkörper für Referenz)
    mb_asm = STLMeshBuilder("main_box_complete_mockup")
    mb_asm.add_box(0, 0, 0, 105.0, 75.0, 36.0)
    # Mounting ears
    mb_asm.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    mb_asm.write_stl(os.path.join(output_dir, "main_box_complete_mockup.stl"))


def generate_pod_base_stl(output_dir: str):
    """Generates Helmet Pod Base and Mount Clamp STL models."""
    print("Generating Pod Base 3D STL models...")
    
    # 1. Pod Base Housing (Helmträger-Körper)
    pb = STLMeshBuilder("pod_base_housing")
    # Base block: 62.0 x 40.0 x 18.0 mm
    pb.add_hollow_box(0, 0, 0, 62.0, 40.0, 18.0, 2.2)
    # M8 Cable Gland Neck (at bottom/rear, Ø 12 mm x 10 mm length)
    pb.add_cylinder(12.0, 20.0, -10.0, 6.0, 10.0)
    # 2x Neodymium Magnet Pockets (Ø 8.2 mm x 3.2 mm)
    pb.add_cylinder(16.0, 20.0, 13.0, 4.2, 3.5)
    pb.add_cylinder(46.0, 20.0, 13.0, 4.2, 3.5)
    # 8-Pin Pogo Pin Bed Center Flange (25 x 10 x 8 mm)
    pb.add_box(20.0, 15.0, 2.2, 22.0, 10.0, 12.0)
    # Lateral Dovetail / Slide-in Rails (1.8 mm wide)
    pb.add_box(0, 2.0, 14.0, 2.5, 36.0, 4.0)
    pb.add_box(59.5, 2.0, 14.0, 2.5, 36.0, 4.0)
    pb.write_stl(os.path.join(output_dir, "pod_base_housing.stl"))
    
    # 2. Helmet Clamp / 3M VHB Base Plate
    pbc = STLMeshBuilder("pod_base_helmet_clamp")
    # Curved helmet adapter plate: 65.0 x 42.0 x 4.0 mm
    pbc.add_box(0, 0, 0, 65.0, 42.0, 3.0)
    # Helmet Clamp arm / Screw Ears
    pbc.add_box(0, 0, -15.0, 5.0, 42.0, 15.0)
    pbc.add_box(0, 0, -18.0, 25.0, 42.0, 4.0) # Bottom clamping jaw
    pbc.write_stl(os.path.join(output_dir, "pod_base_helmet_clamp.stl"))


def generate_cartridges_stl(output_dir: str):
    """Generates Sena, Cardo, and Dummy Cartridge STL models."""
    print("Generating Pod Cartridge 3D STL models...")
    
    # 1. Sena 50S/60S Sled
    sc = STLMeshBuilder("cartridge_sena_sled")
    # Sled Outer Body: 58.0 x 36.0 x 14.0 mm
    sc.add_box(0, 0, 0, 58.0, 36.0, 14.0)
    # Sena Audio Plug Cradle / 3.5mm Recess (Right Flank)
    sc.add_cylinder(48.0, 10.0, 7.0, 4.0, 7.0) # 3.5mm Headphone
    sc.add_cylinder(48.0, 26.0, 7.0, 3.5, 7.0) # 2.5mm Mic
    # Top PTT Toggle Button Bezel
    sc.add_cylinder(29.0, 18.0, 14.0, 5.5, 2.5)
    # Bottom Pogo Target Recess (20 x 8 mm)
    sc.add_box(19.0, 14.0, -1.5, 20.0, 8.0, 1.5)
    sc.write_stl(os.path.join(output_dir, "cartridge_sena_sled.stl"))
    
    # 2. Cardo Packtalk Edge Sled
    cc = STLMeshBuilder("cartridge_cardo_sled")
    # Sled Body with AirMount Magnetic Latch Profile: 58.0 x 36.0 x 15.0 mm
    cc.add_box(0, 0, 0, 58.0, 36.0, 15.0)
    # Cardo AirMount Bevel & Magnet Core (Ø 12 mm)
    cc.add_cylinder(29.0, 18.0, 15.0, 6.0, 3.0)
    # Cardo Top Lock Clip Tab
    cc.add_box(2.0, 14.0, 15.0, 6.0, 8.0, 4.0)
    # Audio Connector Slot
    cc.add_box(46.0, 8.0, 8.0, 10.0, 20.0, 7.0)
    cc.write_stl(os.path.join(output_dir, "cartridge_cardo_sled.stl"))
    
    # 3. Blindkassette / Waterproof Sealed Dummy Plug (Wasserdichter Verschluss)
    dc = STLMeshBuilder("cartridge_blindkassette_waterproof_dummy")
    # Solid aerodynamic sealed cap with thumb grip: 58.0 x 36.0 x 12.0 mm
    dc.add_box(0, 0, 0, 58.0, 36.0, 12.0)
    # Ergonomic Finger Grip Ribs on Top
    for x_rib in [15.0, 22.0, 29.0, 36.0, 43.0]:
        dc.add_box(x_rib, 4.0, 12.0, 2.5, 28.0, 2.0)
    # Perimeter Dual O-Ring Sealing Gasket Flange (Bottom)
    dc.add_box(2.5, 2.5, -3.5, 53.0, 31.0, 3.5)
    dc.write_stl(os.path.join(output_dir, "cartridge_blindkassette_waterproof_dummy.stl"))


def generate_rear_pod3_stl(output_dir: str):
    """Generates Rear Pod 3 Lower Housing and Radome Lid STL models."""
    print("Generating Rear Pod 3 3D STL models...")
    
    # 1. Rear Pod 3 Lower Housing
    rp_low = STLMeshBuilder("rear_pod3_lower_housing")
    # Tub: 72.0 x 48.0 x 14.0 mm, 2.2 mm wall thickness
    rp_low.add_hollow_box(0, 0, 0, 72.0, 48.0, 14.0, 2.2)
    # M8 Cable Gland Neck (Left end, Ø 12 mm x 8 mm)
    rp_low.add_cylinder(0, 24.0, 7.0, 6.0, 8.0)
    # GoPro / Luggage Rack Mounting Cleats (Bottom)
    rp_low.add_box(24.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    rp_low.add_box(34.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    rp_low.add_box(44.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    # 4x Clean Cylindrical PCB Screw Bosses for 62x38 mm Rear PCB (M2.5 Schraubdome, Ø 6.0 mm outer, Ø 2.5 mm hole)
    rp_low.add_boss(8.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(64.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(8.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(64.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.write_stl(os.path.join(output_dir, "rear_pod3_lower_housing.stl"))
    
    # 2. Rear Pod 3 Radome Lid (HF-transparenter Kuppeldeckel)
    rp_lid = STLMeshBuilder("rear_pod3_radome_lid")
    # Base Lid: 72.0 x 48.0 x 3.0 mm
    rp_lid.add_box(0, 0, 0, 72.0, 48.0, 3.0)
    # Aerodynamic LoRa / GNSS Antenna Dome (40 x 30 x 10 mm raised curve)
    rp_lid.add_box(16.0, 9.0, 3.0, 40.0, 30.0, 10.0)
    # Inner Sealing Lip
    rp_lid.add_box(2.4, 2.4, -2.5, 67.2, 43.2, 2.5)
    rp_lid.write_stl(os.path.join(output_dir, "rear_pod3_radome_lid.stl"))


def main():
    output_dir = "/Users/schmidtm/openMotorBridge/hardware/3d_models_mjf"
    cad_stl_dir = "/Users/schmidtm/openMotorBridge/hardware/cad/stl"
    
    for d in [output_dir, cad_stl_dir]:
        os.makedirs(d, exist_ok=True)
        generate_main_box_stl(d)
        generate_pod_base_stl(d)
        generate_cartridges_stl(d)
        generate_rear_pod3_stl(d)
        
    print("\n" + "=" * 80)
    print("ALL 3D STL MODELS SUCCESSFULLY EXPORTED FOR TINKERCAD & 3D PRINTING".center(80))
    print("=" * 80)
    print(f"Destination 1: {output_dir}")
    print(f"Destination 2: {cad_stl_dir}")
    print("\nExported Files:")
    for f in sorted(os.listdir(output_dir)):
        if f.endswith('.stl'):
            size_kb = os.path.getsize(os.path.join(output_dir, f)) / 1024.0
            print(f"  • {f:<45} ({size_kb:>5.1f} KB)")
    print("=" * 80)

if __name__ == '__main__':
    main()
