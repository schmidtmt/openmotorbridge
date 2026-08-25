#!/usr/bin/env python3
"""
OpenMotorBridge Central Main Box Mechanical Enclosure CAD Generator
-------------------------------------------------------------------
Generates photorealistic 3D CAD visualizations for the Central Main Box Enclosure
(openmotorbridge_main_box):
  - IP67 PA12/Aluminum housing (110 x 74 x 38 mm)
  - 4x M4 Silent-block mounting ears (128 x 56 mm hole spacing)
  - Front panel: HD26 harness flange, USB-C service cap with O-ring
  - Top lid: PMMA RGB Status LED light guide (Ø 3 mm), Gore ePTFE vent (Ø 7 mm)
  - Mid-Baffle (Zwischenboden): Integrated 38x6 mm chamfered cable pass-through slot,
    Ø 5 mm LED shaft, and 4x pressure equalization slots
  - Thermal management: 4x Solid Copper Thermal Studs (Ø 8 mm) in bottom hull
    coupled to 2.0 mm flexible silicone gap-pad (Shore 00 35) under LM5164/ESP32
  - Bottom internal LiPo UPS battery pocket (52 x 36 x 6.5 mm)
  - 4-layer FR4 Main PCB (85 x 55 mm) on vibration-isolated M2.5 standoffs
  - 26-conductor flexible ribbon cable routed through the mid-baffle slot to J1 header
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_box(ax, x0, y0, z0, dx, dy, dz, color, alpha=1.0, edgecolor=None, linewidth=0.5):
    """Draws a 3D box."""
    vertices = np.array([
        [x0, y0, z0],
        [x0 + dx, y0, z0],
        [x0 + dx, y0 + dy, z0],
        [x0, y0 + dy, z0],
        [x0, y0, z0 + dz],
        [x0 + dx, y0, z0 + dz],
        [x0 + dx, y0 + dy, z0 + dz],
        [x0, y0 + dy, z0 + dz]
    ])
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]], # Bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]], # Top
        [vertices[0], vertices[1], vertices[5], vertices[4]], # Front
        [vertices[2], vertices[3], vertices[7], vertices[6]], # Back
        [vertices[0], vertices[3], vertices[7], vertices[4]], # Left
        [vertices[1], vertices[2], vertices[6], vertices[5]]  # Right
    ]
    poly = Poly3DCollection(faces, facecolors=color, alpha=alpha, edgecolors=edgecolor, linewidths=linewidth)
    ax.add_collection3d(poly)
    return vertices

def draw_cylinder(ax, x0, y0, z0, radius, length, color, alpha=1.0, resolution=32, axis='z'):
    """Draws a 3D cylinder."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    if axis == 'z':
        z = np.linspace(z0, z0 + length, 2)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = x0 + radius * np.cos(theta_grid)
        y_grid = y0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)
    elif axis == 'x':
        x = np.linspace(x0, x0 + length, 2)
        theta_grid, x_grid = np.meshgrid(theta, x)
        y_grid = y0 + radius * np.cos(theta_grid)
        z_grid = z0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)
    elif axis == 'y':
        y = np.linspace(y0, y0 + length, 2)
        theta_grid, y_grid = np.meshgrid(theta, y)
        x_grid = x0 + radius * np.cos(theta_grid)
        z_grid = z0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)

def render_main_box_cad(output_path):
    fig = plt.figure(figsize=(24, 12), dpi=220, facecolor='#080c14')
    
    # -------------------------------------------------------------
    # Aspect Ratio Setup (True 1:1:1 Scale based on 110 x 74 x 38 mm)
    # -------------------------------------------------------------
    span_x = 150.0 # -75 to +75 mm (incl. mounting ears)
    span_y = 90.0  # -45 to +45 mm
    span_z = 50.0  # -25 to +25 mm
    
    # -------------------------------------------------------------
    # 1. EXTERNAL 3D VIEW: IP67 ENCLOSURE WITH FLANGE, SERVICE CAP & EARS
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#080c14')
    ax1.set_title("1. ZENTRALBOX BASISGEHÄUSE IP67 / IP69K (AUSSENANSICHT)\n(HD26-Kabelbaumflansch, USB-C Service-Kappe, PMMA-Lichtleiter & 4x M4 Silentblöcke)", 
                  color='#38bdf8', fontsize=13, fontweight='bold', pad=15)
    
    # Main Lower Hull (PA12 Black: 110 x 74 x 26 mm from Z = -18 to +8)
    draw_box(ax1, -55, -37, -18, 110, 74, 26, color='#1e293b', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    
    # Top Lid (PA12: 110 x 74 x 12 mm from Z = +8 to +20)
    draw_box(ax1, -55, -37, 8, 110, 74, 12, color='#0284c7', alpha=0.20, edgecolor='#38bdf8', linewidth=1.0)
    
    # Perimeter Silicone Sealing Gasket (Red line at Z=8)
    draw_box(ax1, -54, -36, 7.5, 108, 72, 1.0, color='#ef4444', alpha=0.95, edgecolor='#dc2626', linewidth=0.8)
    
    # 4-Layer Main PCB (Visible inside: 85 x 55 x 1.6 mm)
    draw_box(ax1, -42.5, -27.5, -6.0, 85, 55, 1.6, color='#059669', alpha=0.85, edgecolor='#10b981', linewidth=0.8)
    
    # 4x M4 Silent-Block Mounting Ears (Flanges at 4 corners, hole spacing 128 x 56 mm)
    for ear_x in [-64, 55]:
        for ear_y in [-37, 23]:
            draw_box(ax1, ear_x, ear_y, -18, 9, 14, 6, color='#334155', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
            center_x = ear_x + 4.5
            center_y = ear_y + 7.0
            draw_cylinder(ax1, center_x, center_y, -18.5, 4.0, 7.0, color='#0f172a', alpha=0.95, axis='z')
            draw_cylinder(ax1, center_x, center_y, -19.0, 2.2, 8.0, color='#cbd5e1', alpha=0.95, axis='z')

    # Front Panel Features (placed at Y = -37)
    # HD26 D-Sub Wall Flange (39.2 x 15.4 mm at X = -10, Y = -37, Z = -5)
    draw_box(ax1, -25, -40, -11, 40, 3, 16, color='#0284c7', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    draw_box(ax1, -23, -42, -9, 36, 2, 12, color='#0f172a', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    for px in np.linspace(-20, 10, 9):
        for pz in np.linspace(-7, 1, 3):
            draw_cylinder(ax1, px, -42.5, pz, 0.4, 1.5, color='#fbbf24', alpha=0.95, axis='y')
    draw_cylinder(ax1, -24.5, -41, -3, 1.5, 3.0, color='#cbd5e1', alpha=0.95, axis='y')
    draw_cylinder(ax1, 14.5, -41, -3, 1.5, 3.0, color='#cbd5e1', alpha=0.95, axis='y')
    
    # USB-C Waterproof Service Port & Screw-Cap (at X = 32, Y = -37, Z = -3)
    draw_cylinder(ax1, 32, -37, -3, 6.0, 4.0, color='#475569', alpha=0.95, axis='y')
    draw_cylinder(ax1, 32, -41, -3, 5.5, 3.0, color='#0284c7', alpha=0.95, axis='y')
    draw_cylinder(ax1, 32, -39, -3, 5.8, 0.8, color='#ef4444', alpha=0.95, axis='y')
    
    # Top Lid Features:
    # 1. PMMA RGB Status LED Light Guide (Ø 3.0 mm at X = 25, Y = 0, Z = 19)
    draw_cylinder(ax1, 25, 0, 18, 2.0, 4.0, color='#34d399', alpha=0.95, axis='z')
    # 2. Gore ePTFE Pressure Equalization Vent (Ø 7.0 mm at X = -10, Y = 0, Z = 19.5)
    draw_cylinder(ax1, -10, 0, 19.5, 4.0, 1.0, color='#ffffff', alpha=0.95, axis='z')
    draw_cylinder(ax1, -10, 0, 19.0, 5.0, 0.6, color='#64748b', alpha=0.95, axis='z')
    
    # 4x M3 Stainless Lid Screws
    for sx in [-48, 48]:
        for sy in [-30, 30]:
            draw_cylinder(ax1, sx, sy, 19.0, 2.5, 1.5, color='#cbd5e1', alpha=0.95, axis='z')
            
    # Bottom Thermal Stud Heads
    for bx in [-25, 15]:
        for by in [-12, 12]:
            draw_cylinder(ax1, bx, by, -19.0, 4.0, 1.5, color='#d97706', alpha=0.95, axis='z')
    
    # Annotations Ax1
    ax1.text(-5, -45, 12, "HD26 Flansch (Kabelbaum)", color='#38bdf8', fontsize=10, fontweight='bold')
    ax1.text(32, -45, 10, "USB-C Service-Port (IP67)", color='#38bdf8', fontsize=10, fontweight='bold')
    ax1.text(-68, -42, -22, "4x M4 Silentblöcke", color='#94a3b8', fontsize=10, fontweight='bold')
    ax1.text(-12, 0, 24, "Gore ePTFE Membran", color='#ffffff', fontsize=10, fontweight='bold')
    ax1.text(25, 0, 24, "PMMA RGB-Lichtleiter", color='#34d399', fontsize=10, fontweight='bold')
    
    ax1.set_xlim([-75, 75])
    ax1.set_ylim([-45, 45])
    ax1.set_zlim([-25, 25])
    ax1.set_box_aspect((span_x, span_y, span_z))
    ax1.view_init(elev=24, azim=-55)
    ax1.axis('off')

    # -------------------------------------------------------------
    # 2. SECTION / X-RAY VIEW: ZWISCHENBODEN, KABELKANAL, THERMAL & PCB
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#080c14')
    ax2.set_title("2. SCHNITTANSICHT: ZWISCHENBODEN, KABELDURCHFÜHRUNG & KÜHLUNG\n(38x6mm Flachband-Schlitz, LED-Schacht, 4x Kupfer-Bolzen, Silikon-Pad & LiPo-USV)", 
                  color='#10b981', fontsize=13, fontweight='bold', pad=15)
    
    # Lower Hull Floor Outline (Translucent outline: 110 x 74 x 26 mm)
    draw_box(ax2, -55, -37, -18, 110, 74, 26, color='#059669', alpha=0.05, edgecolor='#059669', linewidth=0.8)
    
    # 1. 4x Solid Copper Thermal Studs (Ø 8 mm x 6 mm, embedded in bottom floor Z=-18 to -12)
    copper_coords = [(-25, -12), (-25, 12), (15, -12), (15, 12)]
    for cx, cy in copper_coords:
        draw_cylinder(ax2, cx, cy, -18.5, 4.0, 6.5, color='#d97706', alpha=0.95, axis='z')
        draw_cylinder(ax2, cx, cy, -12.0, 5.0, 0.5, color='#f59e0b', alpha=0.95, axis='z')
    
    # 2. Flexible Silicone Thermal Gap-Pad (Shore 00 35, 60 x 40 x 2.0 mm, Z=-12 to -10)
    draw_box(ax2, -35, -20, -12, 60, 40, 2.0, color='#38bdf8', alpha=0.85, edgecolor='#0284c7', linewidth=0.8)
    
    # 3. 1S LiPo UPS Buffer Battery (52 x 36 x 6.5 mm in recessed floor cavity Z=-18 to -11.5)
    draw_box(ax2, -50, -18, -17.5, 12, 36, 6.0, color='#3b82f6', alpha=0.85, edgecolor='#1d4ed8', linewidth=0.8)
    
    # 4. 4-Layer Main PCB (FR4 TG150: 85 x 55 x 1.6 mm at Z = -10 to -8.4)
    draw_box(ax2, -42.5, -27.5, -10.0, 85, 55, 1.6, color='#065f46', alpha=0.95, edgecolor='#10b981', linewidth=1.0)
    
    # Key Components on PCB:
    # - LM5164-Q1 Buck Converter & Shielded Inductor (Hotspot 1 at X = -25, Y = -12, Z = -8.4)
    draw_box(ax2, -30, -16, -8.4, 10, 8, 4.5, color='#1e293b', alpha=0.95, edgecolor='#f59e0b', linewidth=0.8)
    draw_box(ax2, -28, -6, -8.4, 6, 5, 2.0, color='#0f172a', alpha=0.95, edgecolor='#e2e8f0', linewidth=0.5)
    
    # - TI BQ24075 UPS Power-Path IC (Hotspot 2 at X = -25, Y = 10, Z = -8.4)
    draw_box(ax2, -28, 8, -8.4, 6, 6, 1.8, color='#0f172a', alpha=0.95, edgecolor='#e2e8f0', linewidth=0.5)
    
    # - ESP32-S3 Dual-Core DSP Module (Hotspot 3 at X = 10, Y = -5, Z = -8.4)
    draw_box(ax2, 0, -14, -8.4, 25, 18, 3.2, color='#cbd5e1', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax2, 25, -14, -8.4, 10, 18, 1.6, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.8)
    
    # - Bourns Audio Isolation Transformers (Zone 4 at X = -10, Y = 12, Z = -8.4)
    draw_box(ax2, -12, 8, -8.4, 12, 10, 6.0, color='#1e293b', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)
    draw_box(ax2, 3, 8, -8.4, 12, 10, 6.0, color='#1e293b', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)
    
    # - J1 2x13 Box Header on PCB (X = -22 to +12, Y = -23 to -17, Z = -8.4 to -3.0)
    draw_box(ax2, -20, -22, -8.4, 34, 5, 5.4, color='#0f172a', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)

    # -------------------------------------------------------------
    # 5. ZWISCHENBODEN (MID-BAFFLE PLATE) AT Z = 2.0 TO 4.5 MM
    # -------------------------------------------------------------
    # Main Baffle Plate Left Section (X = -51 to -20)
    draw_box(ax2, -51, -33, 2.0, 31, 66, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)
    # Main Baffle Plate Right Section (X = 18 to 51)
    draw_box(ax2, 18, -33, 2.0, 33, 66, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)
    # Main Baffle Plate Center-Back Section (X = -20 to 18, Y = -14 to 33)
    draw_box(ax2, -20, -14, 2.0, 38, 47, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)
    
    # Highlight: 38.0 x 6.0 mm Cable Pass-Through Slot (at X = -20 to 18, Y = -22 to -14)
    # Slot boundary frame (chamfered outline)
    draw_box(ax2, -20.5, -22.5, 1.8, 39, 8.5, 2.9, color='#0284c7', alpha=0.25, edgecolor='#38bdf8', linewidth=1.2)
    
    # 26-Conductor Ultra-Flexible Ribbon Cable (pink/violet AWG28) looping through the slot
    # From HD26 connector at front (Y=-37, Z=-5) looping up through slot (Z=3) down to J1 (Z=-3)
    draw_box(ax2, -18, -36, -6, 30, 14, 1.2, color='#f43f5e', alpha=0.90, edgecolor='#fda4af', linewidth=0.6)
    draw_box(ax2, -18, -22, -6, 30, 2, 9.0, color='#f43f5e', alpha=0.90, edgecolor='#fda4af', linewidth=0.6)
    draw_box(ax2, -18, -21, 2.5, 30, 3, 1.2, color='#f43f5e', alpha=0.90, edgecolor='#fda4af', linewidth=0.6)
    
    # Ø 5.0 mm Optical LED Shaft Aperture in Zwischenboden (at X = 25, Y = 0)
    draw_cylinder(ax2, 25, 0, 1.5, 2.8, 3.5, color='#0284c7', alpha=0.4, axis='z')
    
    # 4x Pressure Equalization & Venting Slots in Zwischenboden (15 x 2 mm)
    for vx in [-35, -15, 5, 35]:
        draw_box(ax2, vx, 15, 1.8, 12, 2.5, 2.9, color='#0284c7', alpha=0.3, edgecolor='#38bdf8', linewidth=0.6)
    
    # Top Lid PMMA Light Guide descending through the LED shaft down to PCB LED
    draw_cylinder(ax2, 25, 0, -6.8, 1.5, 26.0, color='#34d399', alpha=0.85, axis='z')
    draw_box(ax2, 23.5, -1.5, -8.4, 3.0, 3.0, 1.6, color='#10b981', alpha=0.95, edgecolor='#ffffff', linewidth=0.5)
    
    # 4x Vibration-Isolated PCB Standoffs
    for px, py in [(-38, -23), (-38, 23), (38, -23), (38, 23)]:
        draw_cylinder(ax2, px, py, -15, 2.5, 5.0, color='#475569', alpha=0.95, axis='z')
        draw_cylinder(ax2, px, py, -10.5, 3.0, 1.0, color='#ef4444', alpha=0.95, axis='z')
        draw_cylinder(ax2, px, py, -8.4, 1.2, 3.0, color='#cbd5e1', alpha=0.95, axis='z')

    # Annotations Ax2
    ax2.text(-22, -28, 7, "38x6 mm Kabel-Durchführung (Zwischenboden)", color='#38bdf8', fontsize=10, fontweight='bold')
    ax2.text(-18, -38, -2, "26-Pin Flachbandkabel", color='#f43f5e', fontsize=9, fontweight='bold')
    ax2.text(26, 0, 8, "Ø 5 mm LED-Schacht", color='#34d399', fontsize=9, fontweight='bold')
    ax2.text(-35, 18, 7, "4x Druckausgleichsschlitze", color='#94a3b8', fontsize=9, fontweight='bold')
    ax2.text(-25, -25, -20, "4x Kupfer-Bolzen (Ø 8 mm)", color='#f59e0b', fontsize=10, fontweight='bold')
    ax2.text(-35, -28, -11, "2 mm Silikon-Wärmeleitpad", color='#38bdf8', fontsize=10, fontweight='bold')
    ax2.text(-52, -25, -16, "1S LiPo Akku (USV)", color='#60a5fa', fontsize=10, fontweight='bold')
    ax2.text(-30, -18, -3, "LM5164 Buck", color='#f59e0b', fontsize=8, fontweight='bold')
    ax2.text(5, -18, -3, "ESP32-S3", color='#e2e8f0', fontsize=8, fontweight='bold')

    ax2.set_xlim([-75, 75])
    ax2.set_ylim([-45, 45])
    ax2.set_zlim([-25, 25])
    ax2.set_box_aspect((span_x, span_y, span_z))
    ax2.view_init(elev=26, azim=-52)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Main Box Mechanical Enclosure CAD generated: {output_path}")

if __name__ == "__main__":
    out1 = "/Users/schmidtm/.gemini/antigravity-ide/brain/71a5d344-5a46-4a0e-bb50-16bb2304a17f/main_box_enclosure_cad.png"
    out2 = "/Users/schmidtm/openMotorBridge/hardware/cad/main_box_enclosure_cad.png"
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    render_main_box_cad(out1)
    render_main_box_cad(out2)
