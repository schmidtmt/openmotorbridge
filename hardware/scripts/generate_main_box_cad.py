#!/usr/bin/env python3
"""
OpenMotorBridge Central Main Box Mechanical Enclosure CAD Generator
-------------------------------------------------------------------
Generates photorealistic 3D CAD visualizations for the 3-Piece Sandwich Enclosure
(openmotorbridge_main_box):
  1. Lower Tray (Unterwanne, 17.0 mm):
     - 100% closed immersion base with 4x M4 silentblock ears (128 x 56 mm)
     - 4x Solid Copper Thermal Studs (Ø 8 mm) in bottom floor
     - 2.0 mm Silicone Thermal Gap-Pad (Shore 00 35) under LM5164 / ESP32
     - 4-layer Main PCB (85 x 55 x 1.6 mm) on M2.5 vibration isolators
  2. Upper Tray with Mid-Baffle (Oberwanne mit Zwischenboden, 15.0 mm):
     - Front panel: HD26 harness wall flange, USB-C service port & RGB Status LED window
     - Upper compartment on mid-baffle: 1S LiPo UPS buffer battery (52 x 36 x 6.5 mm)
       secured in molded battery cradle by elastic EPDM rubber retention strap
     - Mid-baffle partition floor: 38x6 mm chamfered ribbon cable slot
       and 4x pressure equalization slots
     - 26-conductor flexible ribbon cable routing from HD26 through mid-baffle to J1
  3. Enclosure Lid (Gehäusedeckel, 6.0 mm):
     - Solid, homogeneous protective cover (PA12, 3.0 mm wall thickness)
     - Gore ePTFE pressure equalization vent (Ø 7 mm)
     - Perimeter Shore 40A silicone profile seal (100% hermetic)
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
    # Total Z = -19 to +19 mm (38 mm)
    # Unterwanne: Z = -19 to -2 mm (17 mm)
    # Oberwanne:   Z = -2 to +13 mm (15 mm)
    # Deckel:      Z = +13 to +19 mm (6 mm)
    # -------------------------------------------------------------
    span_x = 150.0 # -75 to +75 mm (incl. mounting ears)
    span_y = 90.0  # -45 to +45 mm
    span_z = 50.0  # -25 to +25 mm
    
    # -------------------------------------------------------------
    # 1. EXTERNAL 3D VIEW: 3-TIER SANDWICH ENCLOSURE
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#080c14')
    ax1.set_title("1. ZENTRALBOX 3-TEILIGES SANDWICH-GEHÄUSE (IP67 / IP69K)\n(Unterwanne: PCB & Kühlung | Oberwanne: HD26, USB-C, LED-Fenster & Akku | Deckel: Gore-Vent)", 
                  color='#38bdf8', fontsize=13, fontweight='bold', pad=15)
    
    # Tier 1: Unterwanne (PA12 Black: 110 x 74 x 17 mm, Z = -19 to -2)
    draw_box(ax1, -55, -37, -19, 110, 74, 17, color='#1e293b', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    # Perimeter Gasket Line 1 (Red at Z = -2)
    draw_box(ax1, -54.5, -36.5, -2.5, 109, 73, 0.8, color='#ef4444', alpha=0.95, edgecolor='#dc2626', linewidth=0.6)
    
    # Tier 2: Oberwanne (PA12 Mid-Frame: 110 x 74 x 15 mm, Z = -2 to +13)
    draw_box(ax1, -55, -37, -2, 110, 74, 15, color='#334155', alpha=0.85, edgecolor='#38bdf8', linewidth=1.0)
    # Perimeter Gasket Line 2 (Red at Z = +13)
    draw_box(ax1, -54.5, -36.5, 12.5, 109, 73, 0.8, color='#ef4444', alpha=0.95, edgecolor='#dc2626', linewidth=0.6)
    
    # Tier 3: Gehäusedeckel (PA12 Top Lid: 110 x 74 x 6 mm, Z = +13 to +19)
    draw_box(ax1, -55, -37, 13, 110, 74, 6, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    
    # 4x M4 Silent-Block Mounting Ears (at Unterwanne Z = -19 to -13)
    for ear_x in [-64, 55]:
        for ear_y in [-37, 23]:
            draw_box(ax1, ear_x, ear_y, -19, 9, 14, 6, color='#334155', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
            center_x = ear_x + 4.5
            center_y = ear_y + 7.0
            draw_cylinder(ax1, center_x, center_y, -19.5, 4.0, 7.0, color='#0f172a', alpha=0.95, axis='z')
            draw_cylinder(ax1, center_x, center_y, -20.0, 2.2, 8.0, color='#cbd5e1', alpha=0.95, axis='z')

    # Front Panel Features on Oberwanne (placed at Y = -37, Z = 0 to 11)
    # 1. HD26 D-Sub Wall Flange (39.2 x 15.4 mm at X = -15, Y = -37, Z = 5)
    draw_box(ax1, -32, -40, -1, 38, 3, 15, color='#0284c7', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    draw_box(ax1, -30, -42, 1, 34, 2, 11, color='#0f172a', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    for px in np.linspace(-27, 1, 8):
        for pz in np.linspace(3, 10, 3):
            draw_cylinder(ax1, px, -42.5, pz, 0.4, 1.5, color='#fbbf24', alpha=0.95, axis='y')
    draw_cylinder(ax1, -31.5, -41, 6.5, 1.5, 3.0, color='#cbd5e1', alpha=0.95, axis='y')
    draw_cylinder(ax1, 5.5, -41, 6.5, 1.5, 3.0, color='#cbd5e1', alpha=0.95, axis='y')
    
    # 2. USB-C Waterproof Service Port & Screw-Cap on Oberwanne (at X = 20, Y = -37, Z = 6.5)
    draw_cylinder(ax1, 20, -37, 6.5, 5.5, 4.0, color='#475569', alpha=0.95, axis='y')
    draw_cylinder(ax1, 20, -41, 6.5, 5.0, 3.0, color='#0284c7', alpha=0.95, axis='y')
    draw_cylinder(ax1, 20, -39, 6.5, 5.3, 0.8, color='#ef4444', alpha=0.95, axis='y')
    
    # 3. PMMA RGB Status LED Window on Oberwanne (at X = 38, Y = -37, Z = 6.5)
    draw_cylinder(ax1, 38, -37.5, 6.5, 2.5, 1.5, color='#10b981', alpha=0.95, axis='y')
    draw_cylinder(ax1, 38, -38.5, 6.5, 1.8, 1.0, color='#34d399', alpha=0.95, axis='y')
    
    # Top Lid Features:
    # 1. Gore ePTFE Pressure Equalization Vent (Ø 7.0 mm at center X = 0, Y = 0, Z = 18.5)
    draw_cylinder(ax1, 0, 0, 18.5, 4.0, 1.0, color='#ffffff', alpha=0.95, axis='z')
    draw_cylinder(ax1, 0, 0, 18.0, 5.0, 0.6, color='#64748b', alpha=0.95, axis='z')
    
    # 4x M3 Stainless Through-Screws
    for sx in [-48, 48]:
        for sy in [-30, 30]:
            draw_cylinder(ax1, sx, sy, 18.5, 2.5, 1.5, color='#cbd5e1', alpha=0.95, axis='z')
            
    # Bottom Thermal Stud Heads
    for bx in [-25, 15]:
        for by in [-12, 12]:
            draw_cylinder(ax1, bx, by, -20.0, 4.0, 1.5, color='#d97706', alpha=0.95, axis='z')
    
    # Annotations Ax1
    ax1.text(-12, -45, 16, "HD26 Flansch", color='#38bdf8', fontsize=9, fontweight='bold')
    ax1.text(18, -45, 14, "USB-C", color='#38bdf8', fontsize=9, fontweight='bold')
    ax1.text(36, -45, 14, "RGB-LED", color='#34d399', fontsize=9, fontweight='bold')
    ax1.text(-68, -42, -23, "4x M4 Silentblöcke", color='#94a3b8', fontsize=9, fontweight='bold')
    ax1.text(0, 0, 22, "Gore ePTFE Membran", color='#ffffff', fontsize=10, fontweight='bold')
    ax1.text(-54, 38, -10, "1. Unterwanne (PCB)", color='#64748b', fontsize=8)
    ax1.text(-54, 38, 5, "2. Oberwanne (Akku & Ports)", color='#64748b', fontsize=8)
    ax1.text(-54, 38, 16, "3. Deckel (100% dicht)", color='#64748b', fontsize=8)
    
    ax1.set_xlim([-75, 75])
    ax1.set_ylim([-45, 45])
    ax1.set_zlim([-25, 25])
    ax1.set_box_aspect((span_x, span_y, span_z))
    ax1.view_init(elev=24, azim=-55)
    ax1.axis('off')

    # -------------------------------------------------------------
    # 2. SECTION / X-RAY VIEW: SANDWICH LAYERS & CABLE ROUTING
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#080c14')
    ax2.set_title("2. SCHNITTANSICHT: SANDWICH-AUFBAU & KABELFÜHRUNG\n(Unten: PCB & Kühlbolzen | Zwischenboden: Kabel-Schlitz & Akku | Stirnseite: HD26, USB-C & LED)", 
                  color='#10b981', fontsize=13, fontweight='bold', pad=15)
    
    # ---------------------------------------------------------
    # LAYER 1: UNTERWANNE (Z = -19 to -2 mm) - PCB & KÜHLUNG
    # ---------------------------------------------------------
    draw_box(ax2, -55, -37, -19, 110, 74, 17, color='#059669', alpha=0.04, edgecolor='#059669', linewidth=0.6)
    
    # 4x Solid Copper Thermal Studs (Ø 8 mm in bottom hull Z=-19 to -12.5)
    copper_coords = [(-25, -12), (-25, 12), (15, -12), (15, 12)]
    for cx, cy in copper_coords:
        draw_cylinder(ax2, cx, cy, -19.5, 4.0, 7.0, color='#d97706', alpha=0.95, axis='z')
        draw_cylinder(ax2, cx, cy, -12.5, 5.0, 0.5, color='#f59e0b', alpha=0.95, axis='z')
    
    # Flexible Silicone Thermal Gap-Pad (60 x 40 x 2.0 mm, Z=-12.5 to -10.5)
    draw_box(ax2, -35, -20, -12.5, 60, 40, 2.0, color='#38bdf8', alpha=0.85, edgecolor='#0284c7', linewidth=0.8)
    
    # 4-Layer Main PCB (85 x 55 x 1.6 mm at Z = -10.5 to -8.9)
    draw_box(ax2, -42.5, -27.5, -10.5, 85, 55, 1.6, color='#065f46', alpha=0.95, edgecolor='#10b981', linewidth=1.0)
    
    # PCB Components:
    # - LM5164-Q1 Buck & Inductor (Hotspot 1 at X = -25, Y = -12)
    draw_box(ax2, -30, -16, -8.9, 10, 8, 4.5, color='#1e293b', alpha=0.95, edgecolor='#f59e0b', linewidth=0.8)
    # - TI BQ24075 UPS IC (Hotspot 2 at X = -25, Y = 10)
    draw_box(ax2, -28, 8, -8.9, 6, 6, 1.8, color='#0f172a', alpha=0.95, edgecolor='#e2e8f0', linewidth=0.5)
    # - ESP32-S3 DSP Module (Hotspot 3 at X = 10, Y = -5)
    draw_box(ax2, 0, -14, -8.9, 25, 18, 3.2, color='#cbd5e1', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax2, 25, -14, -8.9, 10, 18, 1.6, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.8)
    # - Bourns Transformers (X = -10, Y = 12)
    draw_box(ax2, -12, 8, -8.9, 12, 10, 5.0, color='#1e293b', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)
    draw_box(ax2, 3, 8, -8.9, 12, 10, 5.0, color='#1e293b', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)
    # - J1 2x13 Box Header on PCB (at X = -15, Y = -22)
    draw_box(ax2, -24, -22, -8.9, 34, 5, 5.4, color='#0f172a', alpha=0.95, edgecolor='#fbbf24', linewidth=0.8)

    # 4x Vibration PCB Mounts
    for px, py in [(-38, -23), (-38, 23), (38, -23), (38, 23)]:
        draw_cylinder(ax2, px, py, -16, 2.5, 5.5, color='#475569', alpha=0.95, axis='z')
        draw_cylinder(ax2, px, py, -10.5, 1.2, 3.0, color='#cbd5e1', alpha=0.95, axis='z')

    # ---------------------------------------------------------
    # LAYER 2: ZWISCHENBODEN & OBERWANNE (Z = -2 to +13 mm)
    # ---------------------------------------------------------
    # Solid Zwischenboden Partition Floor (PA12: 102 x 66 x 2.5 mm at Z = -2.0 to +0.5)
    # Left Section
    draw_box(ax2, -51, -33, -2.0, 26, 66, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)
    # Right Section
    draw_box(ax2, 13, -33, -2.0, 38, 66, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)
    # Center-Back Section
    draw_box(ax2, -25, -14, -2.0, 38, 47, 2.5, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8)

    # 1. 38.0 x 6.0 mm Ribbon Cable Pass-Through Slot in Zwischenboden
    draw_box(ax2, -25.5, -22.5, -2.2, 39, 8.5, 2.9, color='#0284c7', alpha=0.25, edgecolor='#38bdf8', linewidth=1.2)
    
    # 26-Conductor Ultra-Flexible Ribbon Cable (pink/violet AWG28) looping from HD26 in Oberwanne down to J1 on PCB
    draw_box(ax2, -22, -36, 4, 30, 14, 1.2, color='#f43f5e', alpha=0.90, edgecolor='#fda4af', linewidth=0.6)
    draw_box(ax2, -22, -22, -8.0, 30, 2, 13.0, color='#f43f5e', alpha=0.90, edgecolor='#fda4af', linewidth=0.6)

    # 2. 4x Labyrinth Pressure Equalization Slots in Zwischenboden (15 x 2 mm)
    for vx in [-35, -15, 5, 35]:
        draw_box(ax2, vx, 15, -2.2, 12, 2.5, 2.9, color='#0284c7', alpha=0.3, edgecolor='#38bdf8', linewidth=0.6)

    # ---------------------------------------------------------
    # UPPER COMPARTMENT: 1S LiPo BATTERY SITTING ON ZWISCHENBODEN
    # ---------------------------------------------------------
    # Battery Nesting Cradle / Bed on top of Zwischenboden (Z = 0.5 to 7.0 mm)
    draw_box(ax2, -28, -2, 0.5, 54, 34, 1.0, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
    
    # 1S LiPo UPS Buffer Battery (52 x 32 x 6.5 mm, resting on Zwischenboden cradle Z = 1.5 to 8.0 mm)
    draw_box(ax2, -26, 0, 1.5, 50, 30, 6.5, color='#3b82f6', alpha=0.90, edgecolor='#1d4ed8', linewidth=1.0)
    
    # EPDM Rubber Retention Strap across battery (10 mm wide band spanning battery at X = -1)
    draw_box(ax2, -3, -2, 8.0, 4.0, 34.0, 0.8, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=0.8)
    # Side Anchor Lugs on Oberwanne walls for strap
    draw_box(ax2, -4, -3, 3.0, 6.0, 2.0, 5.5, color='#475569', alpha=0.95, edgecolor='#94a3b8', linewidth=0.6)
    draw_box(ax2, -4, 31, 3.0, 6.0, 2.0, 5.5, color='#475569', alpha=0.95, edgecolor='#94a3b8', linewidth=0.6)

    # Front Panel LED in Oberwanne (at X = 38, Y = -37, Z = 6.5)
    draw_cylinder(ax2, 38, -37.5, 6.5, 2.5, 1.5, color='#10b981', alpha=0.95, axis='y')

    # ---------------------------------------------------------
    # LAYER 3: DECKEL (Z = +13 to +19 mm)
    # ---------------------------------------------------------
    draw_box(ax2, -55, -37, 13, 110, 74, 6, color='#0284c7', alpha=0.15, edgecolor='#38bdf8', linewidth=0.8)

    # Annotations Ax2
    ax2.text(-26, 0, 10, "1S LiPo-Akku (auf Zwischenboden)", color='#60a5fa', fontsize=9, fontweight='bold')
    ax2.text(-3, -8, 11, "EPDM-Spannband", color='#38bdf8', fontsize=8, fontweight='bold')
    ax2.text(-26, -28, 2, "38x6 mm Flachband-Schlitz", color='#38bdf8', fontsize=9, fontweight='bold')
    ax2.text(-26, -38, -3, "26-Pin Flachbandkabel", color='#f43f5e', fontsize=8, fontweight='bold')
    ax2.text(32, -38, 10, "RGB-LED (Front)", color='#34d399', fontsize=8, fontweight='bold')
    ax2.text(-35, 18, 2, "Druckausgleichsschlitze", color='#94a3b8', fontsize=8, fontweight='bold')
    ax2.text(-25, -25, -20, "4x Kupfer-Pins (Ø 8 mm)", color='#f59e0b', fontsize=9, fontweight='bold')
    ax2.text(-35, -28, -12, "2 mm Silikon-Pad", color='#38bdf8', fontsize=8, fontweight='bold')
    ax2.text(5, -18, -6, "Hauptplatine (85x55 mm)", color='#10b981', fontsize=9, fontweight='bold')

    ax2.set_xlim([-75, 75])
    ax2.set_ylim([-45, 45])
    ax2.set_zlim([-25, 25])
    ax2.set_box_aspect((span_x, span_y, span_z))
    ax2.view_init(elev=26, azim=-52)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ 3-Piece Sandwich Main Box CAD generated: {output_path}")

if __name__ == "__main__":
    out1 = "/Users/schmidtm/.gemini/antigravity-ide/brain/71a5d344-5a46-4a0e-bb50-16bb2304a17f/main_box_enclosure_cad.png"
    out2 = "/Users/schmidtm/openMotorBridge/hardware/cad/main_box_enclosure_cad.png"
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    render_main_box_cad(out1)
    render_main_box_cad(out2)
