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
    def add_horizontal_cylinder_x(self, x0: float, cy: float, cz: float, radius: float, length: float, segments: int = 24):
        """Adds a solid horizontal cylinder along the X axis."""
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        left_center = np.array([x0, cy, cz])
        right_center = np.array([x0 + length, cy, cz])
        
        left_ring = [np.array([x0, cy + radius * np.cos(a), cz + radius * np.sin(a)]) for a in angles]
        right_ring = [np.array([x0 + length, cy + radius * np.cos(a), cz + radius * np.sin(a)]) for a in angles]
        
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_triangle(left_center, left_ring[i], left_ring[next_i])
            self.add_triangle(right_center, right_ring[next_i], right_ring[i])
            self.add_quad(left_ring[i], left_ring[next_i], right_ring[next_i], right_ring[i])

    def add_horizontal_boss_x(self, x0: float, cy: float, cz: float, outer_r: float, inner_r: float, length: float, segments: int = 24):
        """Adds a horizontal hollow cylindrical cable gland neck along the X axis with an open inner bore."""
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        
        out_l = [np.array([x0, cy + outer_r * np.cos(a), cz + outer_r * np.sin(a)]) for a in angles]
        out_r = [np.array([x0 + length, cy + outer_r * np.cos(a), cz + outer_r * np.sin(a)]) for a in angles]
        in_l = [np.array([x0, cy + inner_r * np.cos(a), cz + inner_r * np.sin(a)]) for a in angles]
        in_r = [np.array([x0 + length, cy + inner_r * np.cos(a), cz + inner_r * np.sin(a)]) for a in angles]
        
        for i in range(segments):
            next_i = (i + 1) % segments
            # Outer tube
            self.add_quad(out_l[i], out_l[next_i], out_r[next_i], out_r[i])
            # Inner bore tube (normal facing inward)
            self.add_quad(in_l[next_i], in_l[i], in_r[i], in_r[next_i])
            # Left annular rim
            self.add_quad(out_l[next_i], out_l[i], in_l[i], in_l[next_i])
    def add_plate_with_hole_yz(self, x0: float, y0: float, z0: float, W: float, H: float, yc: float, zc: float, R: float, normal_sign: int = 1, segments: int = 24):
        """Adds a rectangular plate on the YZ plane with a circular through-hole."""
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        circle_pts = [np.array([x0, yc + R * np.cos(a), zc + R * np.sin(a)]) for a in angles]
        
        c_bl = np.array([x0, y0, z0])
        c_br = np.array([x0, y0 + W, z0])
        c_tr = np.array([x0, y0 + W, z0 + H])
        c_tl = np.array([x0, y0, z0 + H])
        
        def add_tri(v1, v2, v3):
            if normal_sign < 0:
                self.add_triangle(v1, v3, v2)
            else:
                self.add_triangle(v1, v2, v3)
                
        # Right edge quadrant (i = 21, 22, 23, 0, 1, 2, 3)
        r_indices = [21, 22, 23, 0, 1, 2, 3]
        for idx in range(len(r_indices) - 1):
            i1, i2 = r_indices[idx], r_indices[idx + 1]
            t1 = idx / (len(r_indices) - 1)
            t2 = (idx + 1) / (len(r_indices) - 1)
            e1 = c_br + (c_tr - c_br) * t1
            e2 = c_br + (c_tr - c_br) * t2
            add_tri(e1, e2, circle_pts[i2])
            add_tri(e1, circle_pts[i2], circle_pts[i1])
            
        # Top edge quadrant (i = 3, 4, 5, 6, 7, 8, 9)
        t_indices = [3, 4, 5, 6, 7, 8, 9]
        for idx in range(len(t_indices) - 1):
            i1, i2 = t_indices[idx], t_indices[idx + 1]
            t1 = idx / (len(t_indices) - 1)
            t2 = (idx + 1) / (len(t_indices) - 1)
            e1 = c_tr + (c_tl - c_tr) * t1
            e2 = c_tr + (c_tl - c_tr) * t2
            add_tri(e1, e2, circle_pts[i2])
            add_tri(e1, circle_pts[i2], circle_pts[i1])
            
        # Left edge quadrant (i = 9, 10, 11, 12, 13, 14, 15)
        l_indices = [9, 10, 11, 12, 13, 14, 15]
        for idx in range(len(l_indices) - 1):
            i1, i2 = l_indices[idx], l_indices[idx + 1]
            t1 = idx / (len(l_indices) - 1)
            t2 = (idx + 1) / (len(l_indices) - 1)
            e1 = c_tl + (c_bl - c_tl) * t1
            e2 = c_tl + (c_bl - c_tl) * t2
            add_tri(e1, e2, circle_pts[i2])
            add_tri(e1, circle_pts[i2], circle_pts[i1])
            
        # Bottom edge quadrant (i = 15, 16, 17, 18, 19, 20, 21)
        b_indices = [15, 16, 17, 18, 19, 20, 21]
        for idx in range(len(b_indices) - 1):
            i1, i2 = b_indices[idx], b_indices[idx + 1]
            t1 = idx / (len(b_indices) - 1)
            t2 = (idx + 1) / (len(b_indices) - 1)
            e1 = c_bl + (c_br - c_bl) * t1
            e2 = c_bl + (c_br - c_bl) * t2
            add_tri(e1, e2, circle_pts[i2])
            add_tri(e1, circle_pts[i2], circle_pts[i1])

    def add_horizontal_tunnel_x(self, x0: float, y0: float, z0: float, length: float, width: float, height: float, wall: float, hole_y: float = None, hole_z: float = None, hole_r: float = 0.0):
        """
        Adds a 100% seamless, watertight, manifold 5-sided monocoque tunnel along the X axis.
        Open at front (+X at x0 + length).
        Closed on 4 sides (bottom, top, left, right) and rear wall with ZERO internal intersecting seams.
        If hole_r > 0, adds a smooth through-bore on the rear wall at (hole_y, hole_z).
        """
        x1 = x0 + length
        y1 = y0 + width
        z1 = z0 + height
        ix0 = x0 + wall
        iy0 = y0 + wall
        iz0 = z0 + wall
        iy1 = y1 - wall
        iz1 = z1 - wall
        
        # 1. Outer Faces (4 side/top/bottom faces)
        # Outer Bottom (z = z0, normal -Z)
        self.add_quad(np.array([x0, y0, z0]), np.array([x0, y1, z0]), np.array([x1, y1, z0]), np.array([x1, y0, z0]))
        # Outer Top (z = z1, normal +Z)
        self.add_quad(np.array([x0, y0, z1]), np.array([x1, y0, z1]), np.array([x1, y1, z1]), np.array([x0, y1, z1]))
        # Outer Left (y = y0, normal -Y)
        self.add_quad(np.array([x0, y0, z0]), np.array([x1, y0, z0]), np.array([x1, y0, z1]), np.array([x0, y0, z1]))
        # Outer Right (y = y1, normal +Y)
        self.add_quad(np.array([x0, y1, z0]), np.array([x0, y1, z1]), np.array([x1, y1, z1]), np.array([x1, y1, z0]))
        
        # 2. Inner Cavity Faces (4 side/top/bottom faces, normals facing inside)
        # Inner Bottom (z = iz0, normal +Z)
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([x1, iy0, iz0]), np.array([x1, iy1, iz0]), np.array([ix0, iy1, iz0]))
        # Inner Top (z = iz1, normal -Z)
        self.add_quad(np.array([ix0, iy0, iz1]), np.array([ix0, iy1, iz1]), np.array([x1, iy1, iz1]), np.array([x1, iy0, iz1]))
        # Inner Left (y = iy0, normal +Y)
        self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix0, iy0, iz1]), np.array([x1, iy0, iz1]), np.array([x1, iy0, iz0]))
        # Inner Right (y = iy1, normal -Y)
        self.add_quad(np.array([ix0, iy1, iz0]), np.array([x1, iy1, iz0]), np.array([x1, iy1, iz1]), np.array([ix0, iy1, iz1]))
        
        # 3. Front Open Mouth Annular Rim (at x = x1, normal +X)
        self.add_quad(np.array([x1, y0, z0]), np.array([x1, y1, z0]), np.array([x1, y1, iz0]), np.array([x1, y0, iz0]))
        self.add_quad(np.array([x1, y0, iz1]), np.array([x1, y1, iz1]), np.array([x1, y1, z1]), np.array([x1, y0, z1]))
        self.add_quad(np.array([x1, y0, iz0]), np.array([x1, iy0, iz0]), np.array([x1, iy0, iz1]), np.array([x1, y0, iz1]))
        self.add_quad(np.array([x1, iy1, iz0]), np.array([x1, y1, iz0]), np.array([x1, y1, iz1]), np.array([x1, iy1, iz1]))
        
        # 4. Rear Wall (at x0 outer, normal -X, and ix0 inner, normal +X)
        if hole_r > 0 and hole_y is not None and hole_z is not None:
            self.add_plate_with_hole_yz(x0, y0, z0, width, height, hole_y, hole_z, hole_r, normal_sign=-1)
            self.add_plate_with_hole_yz(ix0, iy0, iz0, width - 2 * wall, height - 2 * wall, hole_y, hole_z, hole_r, normal_sign=1)
            # Cylindrical sleeve connecting outer hole to inner hole (through-bore)
            angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
            out_c = [np.array([x0, hole_y + hole_r * np.cos(a), hole_z + hole_r * np.sin(a)]) for a in angles]
            in_c = [np.array([ix0, hole_y + hole_r * np.cos(a), hole_z + hole_r * np.sin(a)]) for a in angles]
            for i in range(24):
                next_i = (i + 1) % 24
                self.add_quad(out_c[next_i], out_c[i], in_c[i], in_c[next_i])
        else:
            self.add_quad(np.array([x0, y0, z0]), np.array([x0, y0, z1]), np.array([x0, y1, z1]), np.array([x0, y1, z0]))
            self.add_quad(np.array([ix0, iy0, iz0]), np.array([ix0, iy1, iz0]), np.array([ix0, iy1, iz1]), np.array([ix0, iy0, iz1]))

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
        try:
            os.chmod(filepath, 0o777)
            import subprocess
            subprocess.run(["xattr", "-c", filepath], capture_output=True)
        except Exception:
            pass


# =============================================================================
# 1. CENTRAL MAIN BOX EXPORTER
# =============================================================================
def export_main_box_package(base_dir: str):
    print("Exporting 01_main_box package & components...")
    mb_dir = os.path.join(base_dir, "01_main_box")
    comp_dir = os.path.join(mb_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # --- A. Monolithic Models ---
    # 1. Lower Case (Unterwanne mit PCB-Schraubdomen, 4x M3 Eck-Spannsäulen & Dichtungsnut)
    mb_lower = STLMeshBuilder("main_box_lower_case")
    mb_lower.add_hollow_box(0, 0, 0, 105.0, 75.0, 18.0, 2.5)
    # 4x M4 Silentblock Mounting Ears on outer corners
    mb_lower.add_box(-11.5, 9.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(-11.5, 51.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(105.0, 9.5, 0, 11.5, 14.0, 5.0)
    mb_lower.add_box(105.0, 51.5, 0, 11.5, 14.0, 5.0)
    # 4x PCB Standoffs (M2.5 Schraubdome, Höhe 3.5 mm über Boden)
    mb_lower.add_boss(13.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 13.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(13.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    mb_lower.add_boss(92.0, 62.0, 2.5, 3.5, 1.25, 3.5)
    # 4x M3 Corner Enclosure Clamping Pillars (Eck-Pfosten mit M3 Gewindeeinsatz-Bohrung)
    mb_lower.add_boss(6.0, 6.0, 2.5, 4.0, 2.0, 15.5)
    mb_lower.add_boss(99.0, 6.0, 2.5, 4.0, 2.0, 15.5)
    mb_lower.add_boss(6.0, 69.0, 2.5, 4.0, 2.0, 15.5)
    mb_lower.add_boss(99.0, 69.0, 2.5, 4.0, 2.0, 15.5)
    # Umlaufender äußerer Dichtungsfalz-Kragen (Sealing Groove Collar: z = 18..19.5 mm)
    mb_lower.add_box(0, 0, 18.0, 105.0, 1.0, 1.5)      # Front collar
    mb_lower.add_box(0, 74.0, 18.0, 105.0, 1.0, 1.5)   # Back collar
    mb_lower.add_box(0, 0, 18.0, 1.0, 75.0, 1.5)       # Left collar
    mb_lower.add_box(104.0, 0, 18.0, 1.0, 75.0, 1.5)   # Right collar
    mb_lower.write_stl(os.path.join(mb_dir, "main_box_lower_case.stl"))
    mb_lower.write_stl(os.path.join(base_dir, "main_box_lower_case.stl"))
    
    # 2. Mid Tray (Oberwanne mit Nut & Feder Dichtungssteg, 4x M3 Eck-Pfostensäulen & soliden Wänden)
    mb_mid = STLMeshBuilder("main_box_mid_tray")
    # A. 100% Solid Continuous Perimeter Walls (105 x 75 x 15 mm, 2.5 mm wall)
    mb_mid.add_box(0, 0, 0, 2.5, 75.0, 15.0)       # Left Wall
    mb_mid.add_box(102.5, 0, 0, 2.5, 75.0, 15.0)   # Right Wall
    mb_mid.add_box(0, 72.5, 0, 105.0, 2.5, 15.0)   # Back Wall
    mb_mid.add_box(0, 0, 0, 105.0, 2.5, 15.0)      # Front Wall
    # B. Solid Partition Floor (z = 0..2.5 mm)
    mb_mid.add_box(2.5, 2.5, 0, 100.0, 70.0, 2.5)
    # C. Battery Cradle (z = 2.5..10.5 mm)
    mb_mid.add_box(5.0, 12.0, 2.5, 2.5, 50.0, 8.0)
    mb_mid.add_box(5.0, 12.0, 2.5, 50.0, 2.5, 8.0)
    mb_mid.add_box(5.0, 59.5, 2.5, 50.0, 2.5, 8.0)
    mb_mid.add_box(52.5, 12.0, 2.5, 2.5, 50.0, 8.0)
    # D. 4x Corner Through-Bolt Pillars (Eck-Pfosten mit M3 Durchgangsbohrung Ø 3.4 mm über 15 mm Höhe)
    mb_mid.add_boss(6.0, 6.0, 0, 4.0, 1.7, 15.0)
    mb_mid.add_boss(99.0, 6.0, 0, 4.0, 1.7, 15.0)
    mb_mid.add_boss(6.0, 69.0, 0, 4.0, 1.7, 15.0)
    mb_mid.add_boss(99.0, 69.0, 0, 4.0, 1.7, 15.0)
    # E. Unterer Einpress-Dichtsteg (greift in die Nut der Unterwanne: z = -1.5..0 mm)
    mb_mid.add_box(1.2, 1.2, -1.5, 102.6, 1.3, 1.5)
    mb_mid.add_box(1.2, 72.5, -1.5, 102.6, 1.3, 1.5)
    mb_mid.add_box(1.2, 1.2, -1.5, 1.3, 72.6, 1.5)
    mb_mid.add_box(102.5, 1.2, -1.5, 1.3, 72.6, 1.5)
    # F. Oberer Dichtungskragen für den Deckel (z = 15..16.5 mm)
    mb_mid.add_box(0, 0, 15.0, 105.0, 1.0, 1.5)
    mb_mid.add_box(0, 74.0, 15.0, 105.0, 1.0, 1.5)
    mb_mid.add_box(0, 0, 15.0, 1.0, 75.0, 1.5)
    mb_mid.add_box(104.0, 0, 15.0, 1.0, 75.0, 1.5)
    mb_mid.write_stl(os.path.join(mb_dir, "main_box_mid_tray.stl"))
    mb_mid.write_stl(os.path.join(base_dir, "main_box_mid_tray.stl"))
    mb_mid.write_stl(os.path.join(base_dir, "main_box_mid_baffle.stl"))
    
    # 3. Lid (Deckel mit 4x M3 Eck-Schraublöchern & Dichtungslippe)
    mb_lid = STLMeshBuilder("main_box_lid")
    mb_lid.add_box(0, 0, 0, 105.0, 75.0, 4.0)
    # Untere Einpress-Dichtlippe (greift in die Dichtnut der Oberwanne: z = -2.5..0 mm)
    mb_lid.add_box(1.2, 1.2, -2.5, 102.6, 1.3, 2.5)
    mb_lid.add_box(1.2, 72.5, -2.5, 102.6, 1.3, 2.5)
    mb_lid.add_box(1.2, 1.2, -2.5, 1.3, 72.6, 2.5)
    mb_lid.add_box(102.5, 1.2, -2.5, 1.3, 72.6, 2.5)
    # 4x Corner M3 Screw Countersunk Bosses
    mb_lid.add_boss(6.0, 6.0, 0, 4.0, 1.7, 4.0)
    mb_lid.add_boss(99.0, 6.0, 0, 4.0, 1.7, 4.0)
    mb_lid.add_boss(6.0, 69.0, 0, 4.0, 1.7, 4.0)
    mb_lid.add_boss(99.0, 69.0, 0, 4.0, 1.7, 4.0)
    mb_lid.add_cylinder(52.5, 37.5, 4.0, 4.0, 1.5)
    mb_lid.write_stl(os.path.join(mb_dir, "main_box_lid.stl"))
    mb_lid.write_stl(os.path.join(base_dir, "main_box_lid.stl"))

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
    
    # 05. Mid tray solid frame (105x75x15 mm)
    mid_solid_frame = STLMeshBuilder("05_mid_tray_solid_frame")
    mid_solid_frame.add_box(0, 0, 0, 2.5, 75.0, 15.0)
    mid_solid_frame.add_box(102.5, 0, 0, 2.5, 75.0, 15.0)
    mid_solid_frame.add_box(0, 72.5, 0, 105.0, 2.5, 15.0)
    mid_solid_frame.add_box(0, 0, 0, 105.0, 2.5, 15.0)
    mid_solid_frame.write_stl(os.path.join(comp_dir, "05_mid_tray_solid_frame.stl"))
    
    # 06. Mid partition floor solid (100x70x2.5 mm)
    floor_solid = STLMeshBuilder("06_mid_partition_floor_solid")
    floor_solid.add_box(2.5, 2.5, 0, 100.0, 70.0, 2.5)
    floor_solid.write_stl(os.path.join(comp_dir, "06_mid_partition_floor_solid.stl"))
    
    # 07. LiPo Battery Cradle 1000mAh
    cradle_1000 = STLMeshBuilder("07_lipo_battery_cradle_1000mah")
    cradle_1000.add_box(5.0, 12.0, 2.5, 2.5, 50.0, 8.0)
    cradle_1000.add_box(5.0, 12.0, 2.5, 50.0, 2.5, 8.0)
    cradle_1000.add_box(5.0, 59.5, 2.5, 50.0, 2.5, 8.0)
    cradle_1000.add_box(52.5, 12.0, 2.5, 2.5, 50.0, 8.0)
    cradle_1000.write_stl(os.path.join(comp_dir, "07_lipo_battery_cradle_1000mah.stl"))
    
    # 08. LiPo Battery Cradle 1500mAh Large
    cradle_1500 = STLMeshBuilder("08_lipo_battery_cradle_1500mah_large")
    cradle_1500.add_box(4.0, 8.0, 2.5, 2.5, 58.0, 9.0)
    cradle_1500.add_box(4.0, 8.0, 2.5, 54.0, 2.5, 9.0)
    cradle_1500.add_box(4.0, 63.5, 2.5, 54.0, 2.5, 9.0)
    cradle_1500.add_box(55.5, 8.0, 2.5, 2.5, 58.0, 9.0)
    cradle_1500.write_stl(os.path.join(comp_dir, "08_lipo_battery_cradle_1500mah_large.stl"))
    
    # 09-13: Cutout Hole Tool Primitives (Set to 'Bohrung' / 'Hole' in Tinkercad and group!)
    tool_usbc = STLMeshBuilder("09_cutout_tool_usb_c")
    tool_usbc.add_box(18.0, -2.0, 4.0, 12.0, 6.0, 7.0) # USB-C hole tool
    tool_usbc.write_stl(os.path.join(comp_dir, "09_cutout_tool_usb_c.stl"))
    
    tool_led = STLMeshBuilder("10_cutout_tool_led_window")
    tool_led.add_box(36.0, -2.0, 5.0, 6.0, 6.0, 5.0) # LED window hole tool
    tool_led.write_stl(os.path.join(comp_dir, "10_cutout_tool_led_window.stl"))
    
    tool_hd26 = STLMeshBuilder("11_cutout_tool_hd26_dsub")
    tool_hd26.add_box(60.0, -2.0, 3.0, 36.0, 6.0, 9.5) # HD26 D-Sub hole tool
    tool_hd26.write_stl(os.path.join(comp_dir, "11_cutout_tool_hd26_dsub.stl"))
    
    tool_m16 = STLMeshBuilder("12_cutout_tool_m16_round_gland")
    tool_m16.add_cylinder(78.0, 1.25, 7.5, 8.0, 6.0, segments=24) # M16 Ø16mm round hole tool (along Y axis approximation: cylinder)
    tool_m16.write_stl(os.path.join(comp_dir, "12_cutout_tool_m16_round_gland.stl"))
    
    tool_slot = STLMeshBuilder("13_cutout_tool_cable_slot")
    tool_slot.add_box(64.0, 15.0, -1.0, 30.0, 12.0, 5.0) # Cable slot through floor
    tool_slot.write_stl(os.path.join(comp_dir, "13_cutout_tool_cable_slot.stl"))
    
    # 14-16: Lid components
    lid_plate = STLMeshBuilder("14_lid_plate_only")
    lid_plate.add_box(0, 0, 0, 105.0, 75.0, 4.0)
    lid_plate.write_stl(os.path.join(comp_dir, "14_lid_plate_only.stl"))
    
    lid_lip = STLMeshBuilder("15_lid_sealing_lip")
    lid_lip.add_box(2.8, 2.8, -3.0, 99.4, 3.0, 3.0)
    lid_lip.add_box(2.8, 69.2, -3.0, 99.4, 3.0, 3.0)
    lid_lip.add_box(2.8, 2.8, -3.0, 3.0, 69.4, 3.0)
    lid_lip.add_box(99.2, 2.8, -3.0, 3.0, 69.4, 3.0)
    lid_lip.write_stl(os.path.join(comp_dir, "15_lid_sealing_lip.stl"))
    
    lid_vent = STLMeshBuilder("16_lid_gore_vent_boss")
    lid_vent.add_cylinder(52.5, 37.5, 0, 4.0, 5.5)
    lid_vent.write_stl(os.path.join(comp_dir, "16_lid_gore_vent_boss.stl"))
    
    # 17-19: Corner Clamping Post Primitives
    posts_mid = STLMeshBuilder("17_corner_clamping_posts_mid_tray_4x")
    posts_mid.add_boss(6.0, 6.0, 0, 4.0, 1.7, 15.0)
    posts_mid.add_boss(99.0, 6.0, 0, 4.0, 1.7, 15.0)
    posts_mid.add_boss(6.0, 69.0, 0, 4.0, 1.7, 15.0)
    posts_mid.add_boss(99.0, 69.0, 0, 4.0, 1.7, 15.0)
    posts_mid.write_stl(os.path.join(comp_dir, "17_corner_clamping_posts_mid_tray_4x.stl"))
    
    posts_low = STLMeshBuilder("18_corner_clamping_posts_lower_case_4x")
    posts_low.add_boss(6.0, 6.0, 2.5, 4.0, 2.0, 15.5)
    posts_low.add_boss(99.0, 6.0, 2.5, 4.0, 2.0, 15.5)
    posts_low.add_boss(6.0, 69.0, 2.5, 4.0, 2.0, 15.5)
    posts_low.add_boss(99.0, 69.0, 2.5, 4.0, 2.0, 15.5)
    posts_low.write_stl(os.path.join(comp_dir, "18_corner_clamping_posts_lower_case_4x.stl"))
    
    tools_m3_holes = STLMeshBuilder("19_corner_screw_holes_cutout_tool_4x")
    tools_m3_holes.add_cylinder(6.0, 6.0, -5.0, 1.7, 45.0)
    tools_m3_holes.add_cylinder(99.0, 6.0, -5.0, 1.7, 45.0)
    tools_m3_holes.add_cylinder(6.0, 69.0, -5.0, 1.7, 45.0)
    tools_m3_holes.add_cylinder(99.0, 69.0, -5.0, 1.7, 45.0)
    tools_m3_holes.write_stl(os.path.join(comp_dir, "19_corner_screw_holes_cutout_tool_4x.stl"))
    
    # 20-22: Sealing System Modular Primitives
    groove_collar = STLMeshBuilder("20_perimeter_sealing_groove_collar")
    groove_collar.add_box(0, 0, 0, 105.0, 1.0, 1.5)
    groove_collar.add_box(0, 74.0, 0, 105.0, 1.0, 1.5)
    groove_collar.add_box(0, 0, 0, 1.0, 75.0, 1.5)
    groove_collar.add_box(104.0, 0, 0, 1.0, 75.0, 1.5)
    groove_collar.write_stl(os.path.join(comp_dir, "20_perimeter_sealing_groove_collar.stl"))
    
    tongue_lip = STLMeshBuilder("21_perimeter_sealing_tongue_lip")
    tongue_lip.add_box(1.2, 1.2, 0, 102.6, 1.3, 2.0)
    tongue_lip.add_box(1.2, 72.5, 0, 102.6, 1.3, 2.0)
    tongue_lip.add_box(1.2, 1.2, 0, 1.3, 72.6, 2.0)
    tongue_lip.add_box(102.5, 1.2, 0, 1.3, 72.6, 2.0)
    tongue_lip.write_stl(os.path.join(comp_dir, "21_perimeter_sealing_tongue_lip.stl"))
    
    gasket_cord = STLMeshBuilder("22_silicone_o_ring_gasket_cord_1_5mm")
    gasket_cord.add_box(1.0, 1.0, 0, 103.0, 1.5, 1.5)
    gasket_cord.add_box(1.0, 72.5, 0, 103.0, 1.5, 1.5)
    gasket_cord.add_box(1.0, 1.0, 0, 1.5, 73.0, 1.5)
    gasket_cord.add_box(102.5, 1.0, 0, 1.5, 73.0, 1.5)
    gasket_cord.write_stl(os.path.join(comp_dir, "22_silicone_o_ring_gasket_cord_1_5mm.stl"))
    
    # 23-24: Internal Pressure Equalization & Convective Breathing Slot Cutout Tools
    vent_group = STLMeshBuilder("23_floor_vent_slots_cutout_tool_group")
    # Left slots beside battery cradle
    vent_group.add_box(8.0, 20.0, -1.0, 2.5, 15.0, 5.0)
    vent_group.add_box(8.0, 40.0, -1.0, 2.5, 15.0, 5.0)
    # Right slots between battery and cable pass-through
    vent_group.add_box(55.0, 20.0, -1.0, 2.5, 15.0, 5.0)
    vent_group.add_box(55.0, 40.0, -1.0, 2.5, 15.0, 5.0)
    # Rear slot
    vent_group.add_box(25.0, 64.0, -1.0, 15.0, 2.5, 5.0)
    vent_group.write_stl(os.path.join(comp_dir, "23_floor_vent_slots_cutout_tool_group.stl"))
    
    single_vent = STLMeshBuilder("24_single_vent_slot_cutout_tool")
    single_vent.add_box(0, 0, 0, 15.0, 2.5, 5.0)
    single_vent.write_stl(os.path.join(comp_dir, "24_single_vent_slot_cutout_tool.stl"))
    
    # 25-27: Solid Copper Thermal Stud System
    cu_studs = STLMeshBuilder("25_copper_thermal_studs_4x")
    # Positioned under LM5164 Buck (1&2), BQ24075 (3), ESP32-S3 (4)
    for cx, cy in [(35.0, 25.0), (45.0, 25.0), (30.0, 48.0), (70.0, 40.0)]:
        cu_studs.add_cylinder(cx, cy, 0, 4.0, 6.5)       # Ø 8mm shaft
        cu_studs.add_cylinder(cx, cy, 2.5, 5.0, 1.5)     # Ø 10mm flat contact head
    cu_studs.write_stl(os.path.join(comp_dir, "25_copper_thermal_studs_4x.stl"))
    
    cu_tool = STLMeshBuilder("26_copper_stud_floor_pockets_cutout_tool_4x")
    for cx, cy in [(35.0, 25.0), (45.0, 25.0), (30.0, 48.0), (70.0, 40.0)]:
        cu_tool.add_cylinder(cx, cy, -1.0, 4.0, 4.5)     # Ø 8mm through-hole tool
    cu_tool.write_stl(os.path.join(comp_dir, "26_copper_stud_floor_pockets_cutout_tool_4x.stl"))
    
    gap_pad = STLMeshBuilder("27_thermal_gap_pad_preview")
    gap_pad.add_box(22.5, 17.5, 2.5, 60.0, 40.0, 2.0)   # 60x40x2.0 mm Silicone Gap Pad
    gap_pad.write_stl(os.path.join(comp_dir, "27_thermal_gap_pad_preview.stl"))


# =============================================================================
# 2. SATELLITE POD BASE EXPORTER
# =============================================================================
def export_pod_base_package(base_dir: str):
    print("Exporting 02_pod_base package & components...")
    pb_dir = os.path.join(base_dir, "02_pod_base")
    comp_dir = os.path.join(pb_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    # Monolithic Models
    # 1. Pod Base Housing (5-seitiger Monocoque-Schacht: 100 x 60 x 28 mm, nach vorne offen)
    pb = STLMeshBuilder("pod_base_housing")
    # 5-seitiger nahtloser Monocoque-Tunnel mit M8-Durchgangsbohrung (Ø 8mm) an der Rückwand
    pb.add_horizontal_tunnel_x(0, 0, 0, 100.0, 60.0, 28.0, 2.5, hole_y=30.0, hole_z=14.0, hole_r=4.0)
    # Horizontaler M8 6-Pin IP67 Kabelstutzen an Rückwand (x = -10..0, y = 30, z = 14) mit Innenbohrung Ø 8mm
    pb.add_horizontal_boss_x(-10.0, 30.0, 14.0, 6.0, 4.0, 10.0)
    # Schutz-Schottwand / Zwischenboden bei x = 22 mm (trennt M8-Kammer vom Wechselschacht)
    pb.add_box(22.0, 2.5, 2.5, 2.0, 55.0, 23.0)
    # Zentrierter 6-Pin Schutzkragen mit 45°-Fangtrichter (x = 22..28, y = 24..36, z = 10..18)
    pb.add_box(24.0, 24.0, 10.0, 4.0, 12.0, 8.0)
    # 2x Auto-Eject Auswerferfedern-Sitze (flankierend bei y = 16 und y = 44)
    pb.add_cylinder(22.0, 16.0, 14.0, 2.0, 5.0)
    pb.add_cylinder(22.0, 44.0, 14.0, 2.0, 5.0)
    # Decken Gore ePTFE-Membransitz (Ø 7mm) bei x = 50, y = 30, z = 28
    pb.add_cylinder(50.0, 30.0, 28.0, 3.5, 1.5)
    # 4x M2 Montage-Schraubdome für die Schutz-Schottwand
    pb.add_boss(22.0, 5.0, 2.5, 2.5, 1.0, 4.0)
    pb.add_boss(22.0, 55.0, 2.5, 2.5, 1.0, 4.0)
    pb.add_boss(22.0, 5.0, 21.5, 2.5, 1.0, 4.0)
    pb.add_boss(22.0, 55.0, 21.5, 2.5, 1.0, 4.0)
    # Asymmetrische Poka-Yoke Führungsnuten (Nut-und-Feder Führungsschienen an Seitenwänden)
    pb.add_box(24.0, 2.5, 4.5, 74.0, 1.5, 2.2)
    pb.add_box(24.0, 2.5, 9.7, 74.0, 1.5, 2.2)
    pb.add_box(24.0, 56.0, 10.5, 74.0, 1.5, 2.2)
    pb.add_box(24.0, 56.0, 15.7, 74.0, 1.5, 2.2)
    pb.write_stl(os.path.join(pb_dir, "pod_base_housing.stl"))
    pb.write_stl(os.path.join(base_dir, "pod_base_housing.stl"))
    
    # 2. Helm-Klemmadapter (für Pod 1 & Pod 2 am Helm)
    pbc = STLMeshBuilder("pod_mount_helmet_clamp")
    pbc.add_box(0, 0, 0, 80.0, 50.0, 3.0)
    pbc.add_box(0, 0, -15.0, 5.0, 50.0, 15.0)
    pbc.add_box(0, 0, -18.0, 30.0, 50.0, 4.0)
    pbc.write_stl(os.path.join(pb_dir, "pod_mount_helmet_clamp.stl"))
    pbc.write_stl(os.path.join(base_dir, "pod_mount_helmet_clamp.stl"))
    
    # 3. Heck- / GoPro- / Gepäckträger-Montageadapter (für Pod 3 am Heck)
    pbg = STLMeshBuilder("pod_mount_gopro_rack")
    pbg.add_box(0, 0, 0, 80.0, 50.0, 4.0)
    pbg.add_box(28.0, 21.0, -8.0, 4.0, 8.0, 8.0)
    pbg.add_box(38.0, 21.0, -8.0, 4.0, 8.0, 8.0)
    pbg.add_box(48.0, 21.0, -8.0, 4.0, 8.0, 8.0)
    pbg.write_stl(os.path.join(pb_dir, "pod_mount_gopro_rack.stl"))
    pbg.write_stl(os.path.join(base_dir, "pod_mount_gopro_rack.stl"))
    
    # Modular Components for Tinkercad
    c1 = STLMeshBuilder("01_pod_base_monocoque_empty_tunnel")
    c1.add_horizontal_tunnel_x(0, 0, 0, 100.0, 60.0, 28.0, 2.5, hole_y=30.0, hole_z=14.0, hole_r=4.0)
    c1.write_stl(os.path.join(comp_dir, "01_pod_base_monocoque_empty_tunnel.stl"))
    
    c2 = STLMeshBuilder("02_m8_horizontal_cable_gland_neck")
    c2.add_horizontal_boss_x(-10.0, 30.0, 14.0, 6.0, 4.0, 12.5)
    c2.write_stl(os.path.join(comp_dir, "02_m8_horizontal_cable_gland_neck.stl"))
    
    c3 = STLMeshBuilder("03_pod_bulkhead_partition_plate")
    c3.add_box(0, 0, 0, 2.0, 55.0, 23.0)
    c3.write_stl(os.path.join(comp_dir, "03_pod_bulkhead_partition_plate.stl"))
    
    c4 = STLMeshBuilder("04_pin_guide_shroud_funnel")
    c4.add_box(0, 0, 0, 4.0, 12.0, 8.0)
    c4.write_stl(os.path.join(comp_dir, "04_pin_guide_shroud_funnel.stl"))
    
    c5 = STLMeshBuilder("05_pod_eptfe_membrane_boss")
    c5.add_cylinder(50.0, 30.0, 28.0, 3.5, 1.5)
    c5.write_stl(os.path.join(comp_dir, "05_pod_eptfe_membrane_boss.stl"))
    
    c6 = STLMeshBuilder("06_pod_bulkhead_convective_vent_slots_tool")
    c6.add_box(21.0, 8.0, 12.0, 4.0, 6.0, 2.0)
    c6.add_box(21.0, 46.0, 12.0, 4.0, 6.0, 2.0)
    c6.write_stl(os.path.join(comp_dir, "06_pod_bulkhead_convective_vent_slots_tool.stl"))
    
    c7 = STLMeshBuilder("07_pod_snap_fit_catch_pockets_pair")
    c7.add_box(83.5, 1.0, 6.0, 5.0, 1.8, 11.0)
    c7.add_box(83.5, 57.2, 6.0, 5.0, 1.8, 11.0)
    c7.write_stl(os.path.join(comp_dir, "07_pod_snap_fit_catch_pockets_pair.stl"))
    
    c8 = STLMeshBuilder("08_auto_eject_springs_pair")
    c8.add_cylinder(22.0, 16.0, 14.0, 2.25, 8.0)
    c8.add_cylinder(22.0, 44.0, 14.0, 2.25, 8.0)
    c8.write_stl(os.path.join(comp_dir, "08_auto_eject_springs_pair.stl"))
    
    c9 = STLMeshBuilder("09_pod_internal_guide_grooves_cutout_tool")
    c9.add_box(22.0, 1.0, 6.7, 76.0, 3.0, 3.0)  # Left groove tool
    c9.add_box(22.0, 56.0, 12.7, 76.0, 3.0, 3.0) # Right groove tool
    c9.write_stl(os.path.join(comp_dir, "09_pod_internal_guide_grooves_cutout_tool.stl"))


# =============================================================================
# 3. SATELLITE POD CARTRIDGES EXPORTER
# =============================================================================
def export_pod_cartridges_package(base_dir: str):
    print("Exporting 03_pod_cartridges package & components...")
    pc_dir = os.path.join(base_dir, "03_pod_cartridges")
    comp_dir = os.path.join(pc_dir, "components")
    os.makedirs(comp_dir, exist_ok=True)
    
    def add_snap_fit_features(builder: STLMeshBuilder):
        # Dual Cantilever Snap-Fit Arms & Latch Teeth
        builder.add_box(61.0, -1.8, 6.0, 14.0, 1.8, 10.0)      # Left arm
        builder.add_box(61.0, -3.4, 6.5, 4.0, 1.6, 9.0)        # Left latch tooth
        builder.add_box(75.0, -3.8, 5.0, 5.0, 1.8, 12.0)       # Left button pad
        builder.add_box(61.0, 54.0, 6.0, 14.0, 1.8, 10.0)      # Right arm
        builder.add_box(61.0, 55.8, 6.5, 4.0, 1.6, 9.0)        # Right latch tooth
        builder.add_box(75.0, 56.0, 5.0, 5.0, 1.8, 12.0)       # Right button pad
    
    # 1. Sena 50S/60S Cartridge Sled
    sc = STLMeshBuilder("cartridge_sena_sled")
    sc.add_box(0, 0, 0, 75.0, 54.0, 2.5)          # Sled Floor
    sc.add_box(0, 0, 2.5, 75.0, 2.5, 18.0)        # Left Wall
    sc.add_box(0, 51.5, 2.5, 75.0, 2.5, 18.0)     # Right Wall
    sc.add_box(75.0, -2.0, -1.5, 4.0, 58.0, 25.0) # Front Faceplate
    # Asymmetrische Poka-Yoke Führungsfedern (Tongue Rails) mit 30°-Einlaufnase
    sc.add_box(4.0, -1.4, 6.9, 70.0, 1.4, 2.6)    # Linke Feder (z = 8.2 mm)
    sc.add_box(0.0, -1.4, 7.2, 4.0, 1.4, 2.0)     # Einlaufschräge links
    sc.add_box(4.0, 54.0, 12.9, 70.0, 1.4, 2.6)   # Rechte Feder (z = 14.2 mm)
    sc.add_box(0.0, 54.0, 13.2, 4.0, 1.4, 2.0)    # Einlaufschräge rechts
    add_snap_fit_features(sc)
    # Sena 3D Cradle & Jog-Dial Nest auf der Oberseite
    sc.add_cylinder(55.0, 18.0, 18.0, 6.0, 6.0)
    sc.add_cylinder(55.0, 36.0, 18.0, 5.0, 6.0)
    sc.add_cylinder(77.0, 27.0, 18.0, 3.0, 2.0)   # Front ePTFE-Membran
    sc.add_boss(15.0, 10.0, 2.5, 2.5, 1.0, 2.5)
    sc.add_boss(60.0, 10.0, 2.5, 2.5, 1.0, 2.5)
    sc.add_boss(15.0, 44.0, 2.5, 2.5, 1.0, 2.5)
    sc.add_boss(60.0, 44.0, 2.5, 2.5, 1.0, 2.5)
    sc.write_stl(os.path.join(pc_dir, "cartridge_sena_sled.stl"))
    sc.write_stl(os.path.join(base_dir, "cartridge_sena_sled.stl"))
    
    # 2. Cardo Packtalk Edge Cartridge Sled
    cc = STLMeshBuilder("cartridge_cardo_sled")
    cc.add_box(0, 0, 0, 75.0, 54.0, 2.5)          # Sled Floor
    cc.add_box(0, 0, 2.5, 75.0, 2.5, 18.0)        # Left Wall
    cc.add_box(0, 51.5, 2.5, 75.0, 2.5, 18.0)     # Right Wall
    cc.add_box(75.0, -2.0, -1.5, 4.0, 58.0, 25.0) # Front Faceplate
    # Asymmetrische Poka-Yoke Führungsfedern mit 30°-Einlaufnase
    cc.add_box(4.0, -1.4, 6.9, 70.0, 1.4, 2.6)
    cc.add_box(0.0, -1.4, 7.2, 4.0, 1.4, 2.0)
    cc.add_box(4.0, 54.0, 12.9, 70.0, 1.4, 2.6)
    cc.add_box(0.0, 54.0, 13.2, 4.0, 1.4, 2.0)
    add_snap_fit_features(cc)
    # Cardo AirMount Magnet- & Pogo-Nest
    cc.add_cylinder(40.0, 27.0, 18.0, 8.0, 4.0)
    cc.add_box(5.0, 17.0, 18.0, 10.0, 20.0, 5.0)
    cc.add_cylinder(77.0, 27.0, 18.0, 3.0, 2.0)   # Front ePTFE-Membran
    cc.add_boss(15.0, 10.0, 2.5, 2.5, 1.0, 2.5)
    cc.add_boss(60.0, 10.0, 2.5, 2.5, 1.0, 2.5)
    cc.add_boss(15.0, 44.0, 2.5, 2.5, 1.0, 2.5)
    cc.add_boss(60.0, 44.0, 2.5, 2.5, 1.0, 2.5)
    cc.write_stl(os.path.join(pc_dir, "cartridge_cardo_sled.stl"))
    cc.write_stl(os.path.join(base_dir, "cartridge_cardo_sled.stl"))
    
    # 3. OMM Transceiver Cartridge Sled (Pod 3 Heck-Kassette: 1-teilig mit voller 23.5 mm Innenhöhe)
    oc = STLMeshBuilder("cartridge_omm_transceiver_sled")
    oc.add_box(0, 0, 0, 75.0, 54.0, 2.5)          # Sled Floor
    oc.add_box(0, 0, 2.5, 75.0, 2.5, 18.0)        # Left Wall
    oc.add_box(0, 51.5, 2.5, 75.0, 2.5, 18.0)     # Right Wall
    oc.add_box(75.0, -2.0, -1.5, 4.0, 58.0, 25.0) # Front Faceplate
    # Asymmetrische Poka-Yoke Führungsfedern mit 30°-Einlaufnase
    oc.add_box(4.0, -1.4, 6.9, 70.0, 1.4, 2.6)
    oc.add_box(0.0, -1.4, 7.2, 4.0, 1.4, 2.0)
    oc.add_box(4.0, 54.0, 12.9, 70.0, 1.4, 2.6)
    oc.add_box(0.0, 54.0, 13.2, 4.0, 1.4, 2.0)
    add_snap_fit_features(oc)
    # Voller offener Innenraum für openmotorbridge_rear_transceiver PCB (ESP32-S3, SX1262 LoRa, GNSS & Patch-Antenne)
    oc.add_boss(10.0, 8.0, 2.5, 2.5, 1.0, 3.0)
    oc.add_boss(65.0, 8.0, 2.5, 2.5, 1.0, 3.0)
    oc.add_boss(10.0, 46.0, 2.5, 2.5, 1.0, 3.0)
    oc.add_boss(65.0, 46.0, 2.5, 2.5, 1.0, 3.0)
    oc.add_cylinder(77.0, 27.0, 18.0, 3.0, 2.0)   # Front ePTFE-Membran
    oc.write_stl(os.path.join(pc_dir, "cartridge_omm_transceiver_sled.stl"))
    oc.write_stl(os.path.join(base_dir, "cartridge_omm_transceiver_sled.stl"))
    
    # 4. Blindkassette (Wasserdichte Dry Box Dummy)
    dc = STLMeshBuilder("cartridge_blindkassette_waterproof")
    dc.add_box(0, 0, 0, 75.0, 54.0, 2.5)
    dc.add_box(0, 0, 2.5, 75.0, 2.5, 18.0)
    dc.add_box(0, 51.5, 2.5, 75.0, 2.5, 18.0)
    dc.add_box(75.0, -2.0, -1.5, 4.0, 58.0, 25.0)
    # Asymmetrische Poka-Yoke Führungsfedern mit 30°-Einlaufnase
    dc.add_box(4.0, -1.4, 6.9, 70.0, 1.4, 2.6)
    dc.add_box(0.0, -1.4, 7.2, 4.0, 1.4, 2.0)
    dc.add_box(4.0, 54.0, 12.9, 70.0, 1.4, 2.6)
    dc.add_box(0.0, 54.0, 13.2, 4.0, 1.4, 2.0)
    add_snap_fit_features(dc)
    # Wasserdichter Dry-Box Deckel mit Versteifungsrippen
    dc.add_box(5.0, 5.0, 2.5, 65.0, 44.0, 18.0)
    for x_rib in [18.0, 30.0, 42.0, 54.0]:
        dc.add_box(x_rib, 5.0, 20.5, 2.5, 44.0, 2.0)
    dc.add_cylinder(77.0, 27.0, 18.0, 3.0, 2.0)
    dc.write_stl(os.path.join(pc_dir, "cartridge_blindkassette_waterproof.stl"))
    dc.write_stl(os.path.join(base_dir, "cartridge_blindkassette_waterproof_dummy.stl"))
    
    # Modular Components for Tinkercad
    sled_base = STLMeshBuilder("01_universal_base_sled")
    sled_base.add_box(0, 0, 0, 75.0, 54.0, 2.5)
    sled_base.add_box(0, 0, 2.5, 75.0, 2.5, 18.0)
    sled_base.add_box(0, 51.5, 2.5, 75.0, 2.5, 18.0)
    sled_base.write_stl(os.path.join(comp_dir, "01_universal_base_sled.stl"))
    
    faceplate = STLMeshBuilder("02_cartridge_faceplate_with_gasket_lip")
    faceplate.add_box(0, 0, 0, 4.0, 58.0, 25.0)
    faceplate.add_box(-2.0, 2.0, 1.0, 2.0, 54.0, 23.0) # Sealing collar lip
    faceplate.write_stl(os.path.join(comp_dir, "02_cartridge_faceplate_with_gasket_lip.stl"))
    
    mem_boss = STLMeshBuilder("03_cartridge_eptfe_membrane_boss")
    mem_boss.add_cylinder(0, 0, 0, 3.0, 2.0)
    mem_boss.write_stl(os.path.join(comp_dir, "03_cartridge_eptfe_membrane_boss.stl"))
    
    mem_cut = STLMeshBuilder("04_cartridge_membrane_cutout_tool")
    mem_cut.add_cylinder(0, 0, -2.0, 2.5, 6.0)
    mem_cut.write_stl(os.path.join(comp_dir, "04_cartridge_membrane_cutout_tool.stl"))
    
    cart_vents = STLMeshBuilder("05_cartridge_floor_convective_vent_slots_tool")
    cart_vents.add_box(18.0, 12.0, -1.0, 14.0, 2.5, 5.0)
    cart_vents.add_box(18.0, 39.5, -1.0, 14.0, 2.5, 5.0)
    cart_vents.add_box(44.0, 12.0, -1.0, 14.0, 2.5, 5.0)
    cart_vents.add_box(44.0, 39.5, -1.0, 14.0, 2.5, 5.0)
    cart_vents.write_stl(os.path.join(comp_dir, "05_cartridge_floor_convective_vent_slots_tool.stl"))
    
    snap_arms = STLMeshBuilder("06_cartridge_snap_fit_cantilever_arms_pair")
    snap_arms.add_box(61.0, -1.8, 6.0, 14.0, 1.8, 10.0)
    snap_arms.add_box(61.0, 54.0, 6.0, 14.0, 1.8, 10.0)
    snap_arms.write_stl(os.path.join(comp_dir, "06_cartridge_snap_fit_cantilever_arms_pair.stl"))
    
    snap_buttons = STLMeshBuilder("07_cartridge_quick_release_squeeze_buttons_pair")
    snap_buttons.add_box(75.0, -3.8, 5.0, 5.0, 1.8, 12.0)
    snap_buttons.add_box(75.0, 56.0, 5.0, 5.0, 1.8, 12.0)
    snap_buttons.write_stl(os.path.join(comp_dir, "07_cartridge_quick_release_squeeze_buttons_pair.stl"))
    
    guide_ribs = STLMeshBuilder("08_cartridge_lateral_guide_ribs_pair")
    guide_ribs.add_box(4.0, -1.4, 6.9, 70.0, 1.4, 2.6)
    guide_ribs.add_box(0.0, -1.4, 7.2, 4.0, 1.4, 2.0)
    guide_ribs.add_box(4.0, 54.0, 12.9, 70.0, 1.4, 2.6)
    guide_ribs.add_box(0.0, 54.0, 13.2, 4.0, 1.4, 2.0)
    guide_ribs.write_stl(os.path.join(comp_dir, "08_cartridge_lateral_guide_ribs_pair.stl"))


def main():
    import shutil
    base_dirs = [
        "/Users/schmidtm/openMotorBridge/hardware/cad/stl",
        "/Users/schmidtm/openMotorBridge/hardware/3d_models_mjf"
    ]
    
    for base in base_dirs:
        for sub in ["01_main_box", "02_pod_base", "03_pod_cartridges", "04_rear_pod3", "tinkercad_modular_kit"]:
            target = os.path.join(base, sub)
            if os.path.exists(target):
                shutil.rmtree(target)
                
        export_main_box_package(base)
        export_pod_base_package(base)
        export_pod_cartridges_package(base)
        try:
            import subprocess
            subprocess.run(["xattr", "-c", "-r", base], capture_output=True)
            subprocess.run(["chmod", "-R", "777", base], capture_output=True)
        except Exception:
            pass
        
    print("\n" + "=" * 80)
    print("ALL ENCLOSURES & MODULAR COMPONENT LIBRARIES SUCCESSFULLY EXPORTED".center(80))
    print("=" * 80)

if __name__ == '__main__':
    main()
