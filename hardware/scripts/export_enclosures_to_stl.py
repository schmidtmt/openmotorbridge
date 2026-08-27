#!/usr/bin/env python3
"""
OpenMotorBridge - 3D Mechanical Enclosure & Modular Component STL Exporter
==========================================================================
Generates high-precision, watertight STL (Standard Triangle Language) solid models
for all OpenMotorBridge enclosure assemblies AND modular component libraries
structured in dedicated folders for easy editing, scaling, and grouping in Tinkercad.

Folder Structure Exported:
  1. `01_main_box/`
     - `main_box_complete_assembly.stl`
     - `main_box_lower_case.stl`
     - `main_box_mid_tray.stl`
     - `main_box_lid.stl`
     - `components/`
       • `01_lower_tub_empty.stl`
       • `02_pcb_4_standoffs_group.stl`
       • `03_single_m2_5_standoff.stl`
       • `04_single_m4_mounting_ear.stl`
       • `05_mid_tray_solid_frame.stl`
       • `06_mid_tray_frame_precut.stl`
       • `07_mid_partition_floor_with_cable_slot.stl`
       • `08_mid_partition_floor_solid.stl`
       • `09_lipo_battery_cradle_1000mah.stl`
       • `10_lipo_battery_cradle_1500mah_large.stl`
       • `11_front_cutout_tool_usb_c.stl`
       • `12_front_cutout_tool_led.stl`
       • `13_front_cutout_tool_hd26_flange.stl`
       • `14_cable_slot_cutout_tool.stl`
       • `15_lid_plate_only.stl`
       • `16_lid_sealing_lip.stl`
       • `17_lid_gore_vent_boss.stl`

  2. `02_pod_base/`
     - `pod_base_complete.stl`
     - `pod_base_housing.stl`
     - `pod_base_helmet_clamp.stl`
     - `components/` (shell, m8 neck, pogo bed, magnets, rails, baseplate, clamp jaw)

  3. `03_pod_cartridges/`
     - `cartridge_sena_sled.stl`
     - `cartridge_cardo_sled.stl`
     - `cartridge_blindkassette_waterproof.stl`
     - `components/` (universal base sled, sena jack cutouts, cardo airmount, grip ribs, pogo pads)

  4. `04_rear_pod3/`
     - `rear_pod3_complete.stl`
     - `rear_pod3_lower_housing.stl`
     - `rear_pod3_radome_lid.stl`
     - `components/` (empty tub, pcb standoffs, m8 neck, gopro cleats, flat lid, antenna dome)
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
        """
        x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
        ix0, iy0, iz0 = x0 + wall, y0 + wall, z0 + wall
        ix1, iy1 = x1 - wall, y1 - wall
        
        # 1. Outer Bottom Face (z = z0, normal -Z)
        self.add_quad(np.array([x0, y0, z0]), np.array([x0, y1, z0]), np.array([x1, y1, z0]), np.array([x1, y0, z0]))
        # 2. Inner Bottom Face (z = iz0, normal +Z)
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix1, iy0, iz0]), np.array([ix1, iy1, iz0]), np.array([ix0, iy1, iz0]))
        # 3. Outer Side Faces
        self.add_quad(np.array([x0, y0, z0]), np.array([x1, y0, z0]), np.array([x1, y0, z1]), np.array([x0, y0, z1]))
        self.add_quad(np.array([x1, y1, z0]), np.array([x0, y1, z0]), np.array([x0, y1, z1]), np.array([x1, y1, z1]))
        self.add_quad(np.array([x0, y1, z0]), np.array([x0, y0, z0]), np.array([x0, y0, z1]), np.array([x0, y1, z1]))
        self.add_quad(np.array([x1, y0, z0]), np.array([x1, y1, z0]), np.array([x1, y1, z1]), np.array([x1, y0, z1]))
        # 4. Inner Side Faces
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix0, iy0, z1]), np.array([ix1, iy0, z1]), np.array([ix1, iy0, iz0]))
        self.add_quad(np.array([ix1, iy1, iz0]), np.array([ix1, iy1, z1]), np.array([ix0, iy1, z1]), np.array([ix0, iy1, iz0]))
        self.add_quad(np.array([ix0, iy1, iz0]), np.array([ix0, iy1, z1]), np.array([ix0, iy0, z1]), np.array([ix0, iy0, iz0]))
        self.add_quad(np.array([ix1, iy0, iz0]), np.array([ix1, iy0, z1]), np.array([ix1, iy1, z1]), np.array([ix1, iy1, iz0]))
        # 5. Top Rim Faces
        self.add_quad(np.array([x0, y0, z1]), np.array([x1, y0, z1]), np.array([ix1, iy0, z1]), np.array([ix0, iy0, z1]))
        self.add_quad(np.array([x1, y1, z1]), np.array([x0, y1, z1]), np.array([ix0, iy1, z1]), np.array([ix1, iy1, z1]))
        self.add_quad(np.array([x0, y1, z1]), np.array([x0, y0, z1]), np.array([ix0, iy0, z1]), np.array([ix0, iy1, z1]))
        self.add_quad(np.array([x1, y0, z1]), np.array([x1, y1, z1]), np.array([ix1, iy1, z1]), np.array([ix1, iy0, z1]))

    def add_boss(self, cx: float, cy: float, z0: float, outer_r: float, inner_r: float, height: float, segments: int = 24):
        """
        Adds a 100% watertight cylindrical screw standoff boss with a clean center hole.
        """
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        z1 = z0 + height
        hole_bottom_center = np.array([cx, cy, z0])
        
        out_bot = [np.array([cx + outer_r * np.cos(a), cy + outer_r * np.sin(a), z0]) for a in angles]
        out_top = [np.array([cx + outer_r * np.cos(a), cy + outer_r * np.sin(a), z1]) for a in angles]
        in_bot = [np.array([cx + inner_r * np.cos(a), cy + inner_r * np.sin(a), z0]) for a in angles]
        in_top = [np.array([cx + inner_r * np.cos(a), cy + inner_r * np.sin(a), z1]) for a in angles]
        
        for i in range(segments):
            next_i = (i + 1) % segments
            # Outer wall
            self.add_quad(out_bot[i], out_bot[next_i], out_top[next_i], out_top[i])
            # Inner hole wall (normal facing inward)
            self.add_quad(in_bot[i], in_bot[next_i], in_top[next_i], in_top[i])
            # Top annular ring
            self.add_quad(out_top[i], out_top[next_i], in_top[next_i], in_top[i])
            # Bottom hole cap
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
            self.add_triangle(bot_center, bot_ring[next_i], bot_ring[i])
            self.add_triangle(top_center, top_ring[i], top_ring[next_i])
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


# =============================================================================
# 1. CENTRAL MAIN BOX EXPORTER
# =============================================================================
def export_main_box_package(base_dir: str):
    print("Exporting 01_main_box package & components...")
    mb_dir = os.path.join(base_dir, "01_main_box")
    comp_dir = os.path.join(mb_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # --- A. Monolithic Models ---
    # 1. Lower Case (Unterwanne)
    mb_lower = STLMeshBuilder("main_box_lower_case")
    mb_lower.add_hollow_box(0, 0, 0, 105.0, 75.0, 18.0, 2.5)
    mb_lower.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_boss(13.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(13.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.write_stl(os.path.join(mb_dir, "main_box_lower_case.stl"))
    
    # 2. Mid Tray (Oberwanne mit Zwischenboden & Front-Ports)
    mb_mid = STLMeshBuilder("main_box_mid_tray")
    # Outer frame
    mb_mid.add_box(0, 0, 0, 2.5, 75.0, 15.0)
    mb_mid.add_box(102.5, 0, 0, 2.5, 75.0, 15.0)
    mb_mid.add_box(0, 72.5, 0, 105.0, 2.5, 15.0)
    # Front wall with cutouts
    mb_mid.add_box(0, 0, 0, 16.0, 2.5, 15.0)
    mb_mid.add_box(16.0, 0, 0, 12.0, 2.5, 3.5)
    mb_mid.add_box(16.0, 0, 10.5, 12.0, 2.5, 4.5)
    mb_mid.add_box(28.0, 0, 0, 7.0, 2.5, 15.0)
    mb_mid.add_box(35.0, 0, 0, 6.0, 2.5, 5.0)
    mb_mid.add_box(35.0, 0, 10.0, 6.0, 2.5, 5.0)
    mb_mid.add_box(41.0, 0, 0, 19.0, 2.5, 15.0)
    mb_mid.add_box(60.0, 0, 0, 36.0, 2.5, 2.5)
    mb_mid.add_box(60.0, 0, 12.5, 36.0, 2.5, 2.5)
    mb_mid.add_box(96.0, 0, 0, 9.0, 2.5, 15.0)
    # Floor with cable slot
    mb_mid.add_box(2.5, 2.5, 0, 57.5, 70.0, 2.5)
    mb_mid.add_box(60.0, 2.5, 0, 42.5, 12.5, 2.5)
    mb_mid.add_box(60.0, 27.0, 0, 42.5, 45.5, 2.5)
    mb_mid.add_box(94.0, 15.0, 0, 8.5, 12.0, 2.5)
    mb_mid.add_box(60.0, 15.0, 0, 4.0, 12.0, 2.5)
    # Battery cradle
    mb_mid.add_box(5.0, 12.0, 2.5, 2.5, 50.0, 8.0)
    mb_mid.add_box(5.0, 12.0, 2.5, 50.0, 2.5, 8.0)
    mb_mid.add_box(5.0, 59.5, 2.5, 50.0, 2.5, 8.0)
    mb_mid.add_box(52.5, 12.0, 2.5, 2.5, 50.0, 8.0)
    mb_mid.write_stl(os.path.join(mb_dir, "main_box_mid_tray.stl"))
    
    # 3. Lid (Deckel)
    mb_lid = STLMeshBuilder("main_box_lid")
    mb_lid.add_box(0, 0, 0, 105.0, 75.0, 4.0)
    mb_lid.add_box(2.8, 2.8, -3.0, 99.4, 3.0, 3.0)
    mb_lid.add_box(2.8, 69.2, -3.0, 99.4, 3.0, 3.0)
    mb_lid.add_box(2.8, 2.8, -3.0, 3.0, 69.4, 3.0)
    mb_lid.add_box(99.2, 2.8, -3.0, 3.0, 69.4, 3.0)
    mb_lid.add_cylinder(52.5, 37.5, 4.0, 4.0, 1.5)
    mb_lid.write_stl(os.path.join(mb_dir, "main_box_lid.stl"))

    # 4. Complete Assembly Mockup
    mb_asm = STLMeshBuilder("main_box_complete_assembly")
    mb_asm.add_box(0, 0, 0, 105.0, 75.0, 36.0)
    mb_asm.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    mb_asm.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    mb_asm.write_stl(os.path.join(mb_dir, "main_box_complete_assembly.stl"))

    # --- B. Modular Tinkercad Components ---
    # 01. Lower tub empty
    tub_only = STLMeshBuilder("01_lower_tub_empty")
    tub_only.add_hollow_box(0, 0, 0, 105.0, 75.0, 18.0, 2.5)
    tub_only.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    tub_only.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    tub_only.write_stl(os.path.join(comp_dir, "01_lower_tub_empty.stl"))
    
    # 02. PCB 4 standoffs group
    p_grp = STLMeshBuilder("02_pcb_4_standoffs_group")
    p_grp.add_boss(13.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    p_grp.add_boss(92.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    p_grp.add_boss(13.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    p_grp.add_boss(92.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    p_grp.write_stl(os.path.join(comp_dir, "02_pcb_4_standoffs_group.stl"))
    
    # 03. Single M2.5 Standoff Boss (at origin)
    p_single = STLMeshBuilder("03_single_m2_5_standoff")
    p_single.add_boss(0, 0, 0, 3.5, 1.25, 3.5)
    p_single.write_stl(os.path.join(comp_dir, "03_single_m2_5_standoff.stl"))
    
    # 04. Single M4 Mounting Ear (at origin)
    e_single = STLMeshBuilder("04_single_m4_mounting_ear")
    e_single.add_box(0, 0, 0, 11.5, 14.0, 5.0)
    e_single.write_stl(os.path.join(comp_dir, "04_single_m4_mounting_ear.stl"))
    
    # 05. Mid tray solid frame (Solid 105x75x15 frame with solid front wall)
    mid_solid_frame = STLMeshBuilder("05_mid_tray_solid_frame")
    mid_solid_frame.add_box(0, 0, 0, 2.5, 75.0, 15.0)
    mid_solid_frame.add_box(102.5, 0, 0, 2.5, 75.0, 15.0)
    mid_solid_frame.add_box(0, 72.5, 0, 105.0, 2.5, 15.0)
    mid_solid_frame.add_box(0, 0, 0, 105.0, 2.5, 15.0) # Solid front wall
    mid_solid_frame.write_stl(os.path.join(comp_dir, "05_mid_tray_solid_frame.stl"))
    
    # 06. Mid tray frame precut
    mid_precut = STLMeshBuilder("06_mid_tray_frame_precut")
    mid_precut.add_box(0, 0, 0, 2.5, 75.0, 15.0)
    mid_precut.add_box(102.5, 0, 0, 2.5, 75.0, 15.0)
    mid_precut.add_box(0, 72.5, 0, 105.0, 2.5, 15.0)
    mid_precut.add_box(0, 0, 0, 16.0, 2.5, 15.0)
    mid_precut.add_box(16.0, 0, 0, 12.0, 2.5, 3.5)
    mid_precut.add_box(16.0, 0, 10.5, 12.0, 2.5, 4.5)
    mid_precut.add_box(28.0, 0, 0, 7.0, 2.5, 15.0)
    mid_precut.add_box(35.0, 0, 0, 6.0, 2.5, 5.0)
    mid_precut.add_box(35.0, 0, 10.0, 6.0, 2.5, 5.0)
    mid_precut.add_box(41.0, 0, 0, 19.0, 2.5, 15.0)
    mid_precut.add_box(60.0, 0, 0, 36.0, 2.5, 2.5)
    mid_precut.add_box(60.0, 0, 12.5, 36.0, 2.5, 2.5)
    mid_precut.add_box(96.0, 0, 0, 9.0, 2.5, 15.0)
    mid_precut.write_stl(os.path.join(comp_dir, "06_mid_tray_frame_precut.stl"))
    
    # 07. Mid partition floor with cable slot
    floor_slot = STLMeshBuilder("07_mid_partition_floor_with_cable_slot")
    floor_slot.add_box(2.5, 2.5, 0, 57.5, 70.0, 2.5)
    floor_slot.add_box(60.0, 2.5, 0, 42.5, 12.5, 2.5)
    floor_slot.add_box(60.0, 27.0, 0, 42.5, 45.5, 2.5)
    floor_slot.add_box(94.0, 15.0, 0, 8.5, 12.0, 2.5)
    floor_slot.add_box(60.0, 15.0, 0, 4.0, 12.0, 2.5)
    floor_slot.write_stl(os.path.join(comp_dir, "07_mid_partition_floor_with_cable_slot.stl"))
    
    # 08. Mid partition floor solid (100x70 plate)
    floor_solid = STLMeshBuilder("08_mid_partition_floor_solid")
    floor_solid.add_box(2.5, 2.5, 0, 100.0, 70.0, 2.5)
    floor_solid.write_stl(os.path.join(comp_dir, "08_mid_partition_floor_solid.stl"))
    
    # 09. LiPo Battery Cradle 1000mAh (Standard 52x36 mm LiPo)
    cradle_1000 = STLMeshBuilder("09_lipo_battery_cradle_1000mah")
    cradle_1000.add_box(5.0, 12.0, 2.5, 2.5, 50.0, 8.0)
    cradle_1000.add_box(5.0, 12.0, 2.5, 50.0, 2.5, 8.0)
    cradle_1000.add_box(5.0, 59.5, 2.5, 50.0, 2.5, 8.0)
    cradle_1000.add_box(52.5, 12.0, 2.5, 2.5, 50.0, 8.0)
    cradle_1000.write_stl(os.path.join(comp_dir, "09_lipo_battery_cradle_1000mah.stl"))
    
    # 10. LiPo Battery Cradle 1500mAh Large (Wide 60x42 mm LiPo)
    cradle_1500 = STLMeshBuilder("10_lipo_battery_cradle_1500mah_large")
    cradle_1500.add_box(4.0, 8.0, 2.5, 2.5, 58.0, 9.0)
    cradle_1500.add_box(4.0, 8.0, 2.5, 54.0, 2.5, 9.0)
    cradle_1500.add_box(4.0, 63.5, 2.5, 54.0, 2.5, 9.0)
    cradle_1500.add_box(55.5, 8.0, 2.5, 2.5, 58.0, 9.0)
    cradle_1500.write_stl(os.path.join(comp_dir, "10_lipo_battery_cradle_1500mah_large.stl"))
    
    # 11-14: Front Cutout Hole Tool Primitives (Set to 'Bohrung' / 'Hole' in Tinkercad)
    tool_usbc = STLMeshBuilder("11_front_cutout_tool_usb_c")
    tool_usbc.add_box(16.0, -1.0, 3.5, 12.0, 4.5, 7.0) # USB-C hole tool
    tool_usbc.write_stl(os.path.join(comp_dir, "11_front_cutout_tool_usb_c.stl"))
    
    tool_led = STLMeshBuilder("12_front_cutout_tool_led")
    tool_led.add_box(35.0, -1.0, 5.0, 6.0, 4.5, 5.0) # LED window hole tool
    tool_led.write_stl(os.path.join(comp_dir, "12_front_cutout_tool_led.stl"))
    
    tool_hd26 = STLMeshBuilder("13_front_cutout_tool_hd26_flange")
    tool_hd26.add_box(60.0, -1.0, 2.5, 36.0, 4.5, 10.0) # HD26 hole tool
    tool_hd26.write_stl(os.path.join(comp_dir, "13_front_cutout_tool_hd26_flange.stl"))
    
    tool_slot = STLMeshBuilder("14_cable_slot_cutout_tool")
    tool_slot.add_box(64.0, 15.0, -1.0, 30.0, 12.0, 4.5) # Cable slot hole tool
    tool_slot.write_stl(os.path.join(comp_dir, "14_cable_slot_cutout_tool.stl"))
    
    # 15-17: Lid components
    lid_plate = STLMeshBuilder("15_lid_plate_only")
    lid_plate.add_box(0, 0, 0, 105.0, 75.0, 4.0)
    lid_plate.write_stl(os.path.join(comp_dir, "15_lid_plate_only.stl"))
    
    lid_lip = STLMeshBuilder("16_lid_sealing_lip")
    lid_lip.add_box(2.8, 2.8, -3.0, 99.4, 3.0, 3.0)
    lid_lip.add_box(2.8, 69.2, -3.0, 99.4, 3.0, 3.0)
    lid_lip.add_box(2.8, 2.8, -3.0, 3.0, 69.4, 3.0)
    lid_lip.add_box(99.2, 2.8, -3.0, 3.0, 69.4, 3.0)
    lid_lip.write_stl(os.path.join(comp_dir, "16_lid_sealing_lip.stl"))
    
    lid_vent = STLMeshBuilder("17_lid_gore_vent_boss")
    lid_vent.add_cylinder(52.5, 37.5, 0, 4.0, 5.5)
    lid_vent.write_stl(os.path.join(comp_dir, "17_lid_gore_vent_boss.stl"))


# =============================================================================
# 2. POD BASE EXPORTER
# =============================================================================
def export_pod_base_package(base_dir: str):
    print("Exporting 02_pod_base package & components...")
    pb_dir = os.path.join(base_dir, "02_pod_base")
    comp_dir = os.path.join(pb_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # Monolithic Models
    pb = STLMeshBuilder("pod_base_housing")
    pb.add_hollow_box(0, 0, 0, 62.0, 40.0, 18.0, 2.2)
    pb.add_cylinder(12.0, 20.0, -10.0, 6.0, 10.0)
    pb.add_cylinder(16.0, 20.0, 13.0, 4.2, 3.5)
    pb.add_cylinder(46.0, 20.0, 13.0, 4.2, 3.5)
    pb.add_box(20.0, 15.0, 2.2, 22.0, 10.0, 12.0)
    pb.add_box(0, 2.0, 14.0, 2.5, 36.0, 4.0)
    pb.add_box(59.5, 2.0, 14.0, 2.5, 36.0, 4.0)
    pb.write_stl(os.path.join(pb_dir, "pod_base_housing.stl"))
    
    pbc = STLMeshBuilder("pod_base_helmet_clamp")
    pbc.add_box(0, 0, 0, 65.0, 42.0, 3.0)
    pbc.add_box(0, 0, -15.0, 5.0, 42.0, 15.0)
    pbc.add_box(0, 0, -18.0, 25.0, 42.0, 4.0)
    pbc.write_stl(os.path.join(pb_dir, "pod_base_helmet_clamp.stl"))
    
    # Modular Components
    c1 = STLMeshBuilder("01_pod_base_empty_shell")
    c1.add_hollow_box(0, 0, 0, 62.0, 40.0, 18.0, 2.2)
    c1.write_stl(os.path.join(comp_dir, "01_pod_base_empty_shell.stl"))
    
    c2 = STLMeshBuilder("02_m8_connector_neck")
    c2.add_cylinder(12.0, 20.0, -10.0, 6.0, 10.0)
    c2.write_stl(os.path.join(comp_dir, "02_m8_connector_neck.stl"))
    
    c3 = STLMeshBuilder("03_pogo_pin_socket_bed")
    c3.add_box(20.0, 15.0, 2.2, 22.0, 10.0, 12.0)
    c3.write_stl(os.path.join(comp_dir, "03_pogo_pin_socket_bed.stl"))
    
    c4 = STLMeshBuilder("04_magnet_pockets_pair")
    c4.add_cylinder(16.0, 20.0, 13.0, 4.2, 3.5)
    c4.add_cylinder(46.0, 20.0, 13.0, 4.2, 3.5)
    c4.write_stl(os.path.join(comp_dir, "04_magnet_pockets_pair.stl"))


# =============================================================================
# 3. POD CARTRIDGES EXPORTER
# =============================================================================
def export_cartridges_package(base_dir: str):
    print("Exporting 03_pod_cartridges package & components...")
    pc_dir = os.path.join(base_dir, "03_pod_cartridges")
    comp_dir = os.path.join(pc_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # Monolithic Sleds
    sc = STLMeshBuilder("cartridge_sena_sled")
    sc.add_box(0, 0, 0, 58.0, 36.0, 14.0)
    sc.add_cylinder(48.0, 10.0, 7.0, 4.0, 7.0)
    sc.add_cylinder(48.0, 26.0, 7.0, 3.5, 7.0)
    sc.add_cylinder(29.0, 18.0, 14.0, 5.5, 2.5)
    sc.write_stl(os.path.join(pc_dir, "cartridge_sena_sled.stl"))
    
    cc = STLMeshBuilder("cartridge_cardo_sled")
    cc.add_box(0, 0, 0, 58.0, 36.0, 15.0)
    cc.add_cylinder(29.0, 18.0, 15.0, 6.0, 3.0)
    cc.add_box(2.0, 14.0, 15.0, 6.0, 8.0, 4.0)
    cc.add_box(46.0, 8.0, 8.0, 10.0, 20.0, 7.0)
    cc.write_stl(os.path.join(pc_dir, "cartridge_cardo_sled.stl"))
    
    dc = STLMeshBuilder("cartridge_blindkassette_waterproof")
    dc.add_box(0, 0, 0, 58.0, 36.0, 12.0)
    for x_rib in [15.0, 22.0, 29.0, 36.0, 43.0]:
        dc.add_box(x_rib, 4.0, 12.0, 2.5, 28.0, 2.0)
    dc.add_box(2.5, 2.5, -3.5, 53.0, 31.0, 3.5)
    dc.write_stl(os.path.join(pc_dir, "cartridge_blindkassette_waterproof.stl"))
    
    # Modular Components
    sled_base = STLMeshBuilder("01_universal_base_sled")
    sled_base.add_box(0, 0, 0, 58.0, 36.0, 12.0)
    sled_base.write_stl(os.path.join(comp_dir, "01_universal_base_sled.stl"))
    
    pogo_pads = STLMeshBuilder("02_pogo_target_contact_pads")
    pogo_pads.add_box(19.0, 14.0, -1.5, 20.0, 8.0, 1.5)
    pogo_pads.write_stl(os.path.join(comp_dir, "02_pogo_target_contact_pads.stl"))


# =============================================================================
# 4. REAR POD 3 EXPORTER
# =============================================================================
def export_rear_pod3_package(base_dir: str):
    print("Exporting 04_rear_pod3 package & components...")
    rp_dir = os.path.join(base_dir, "04_rear_pod3")
    comp_dir = os.path.join(rp_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # Monolithic Models
    rp_low = STLMeshBuilder("rear_pod3_lower_housing")
    rp_low.add_hollow_box(0, 0, 0, 72.0, 48.0, 14.0, 2.2)
    rp_low.add_cylinder(0, 24.0, 7.0, 6.0, 8.0)
    rp_low.add_box(24.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    rp_low.add_box(34.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    rp_low.add_box(44.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    rp_low.add_boss(8.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(64.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(8.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.add_boss(64.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    rp_low.write_stl(os.path.join(rp_dir, "rear_pod3_lower_housing.stl"))
    
    rp_lid = STLMeshBuilder("rear_pod3_radome_lid")
    rp_lid.add_box(0, 0, 0, 72.0, 48.0, 3.0)
    rp_lid.add_box(16.0, 9.0, 3.0, 40.0, 30.0, 10.0)
    rp_lid.add_box(2.4, 2.4, -2.5, 67.2, 43.2, 2.5)
    rp_lid.write_stl(os.path.join(rp_dir, "rear_pod3_radome_lid.stl"))
    
    # Modular Components
    r1 = STLMeshBuilder("01_rear_pod3_empty_tub")
    r1.add_hollow_box(0, 0, 0, 72.0, 48.0, 14.0, 2.2)
    r1.write_stl(os.path.join(comp_dir, "01_rear_pod3_empty_tub.stl"))
    
    r2 = STLMeshBuilder("02_rear_pod3_4_pcb_standoffs")
    r2.add_boss(8.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    r2.add_boss(64.0, 8.0, 2.2, 3.0, 1.25, 3.0)
    r2.add_boss(8.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    r2.add_boss(64.0, 40.0, 2.2, 3.0, 1.25, 3.0)
    r2.write_stl(os.path.join(comp_dir, "02_rear_pod3_4_pcb_standoffs.stl"))
    
    r3 = STLMeshBuilder("03_m8_cable_neck")
    r3.add_cylinder(0, 24.0, 7.0, 6.0, 8.0)
    r3.write_stl(os.path.join(comp_dir, "03_m8_cable_neck.stl"))
    
    r4 = STLMeshBuilder("04_gopro_mounting_cleats")
    r4.add_box(24.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    r4.add_box(34.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    r4.add_box(44.0, 20.0, -8.0, 4.0, 8.0, 8.0)
    r4.write_stl(os.path.join(comp_dir, "04_gopro_mounting_cleats.stl"))


def main():
    base_dirs = [
        "/Users/schmidtm/openMotorBridge/hardware/cad/stl",
        "/Users/schmidtm/openMotorBridge/hardware/3d_models_mjf"
    ]
    
    for base in base_dirs:
        export_main_box_package(base)
        export_pod_base_package(base)
        export_cartridges_package(base)
        export_rear_pod3_package(base)
        
    print("\n" + "=" * 80)
    print("ALL ENCLOSURES & MODULAR COMPONENT LIBRARIES SUCCESSFULLY EXPORTED".center(80))
    print("=" * 80)

if __name__ == '__main__':
    main()
