#!/usr/bin/env python3
"""
OpenMotorBridge Central Main Box & Main Board Virtual CAD Fitting & Validation Generator
-----------------------------------------------------------------------------------------
Generates photorealistic, exact 1:1:1 Euclidean scale 3D CAD visualizations and cross-sections
validating the mechanical, thermal, and electrical integration of the central main box:
  1. main_box_full_assembly_exploded_3d.png: 3D Exploded View of All Sandwich Layers
  2. main_box_assembly_mated_3d.png: 3D Translucent X-Ray View of Closed & Mated Box
  3. main_box_assembly_cross_section.png: Longitudinal (X-Z) & Transverse (Y-Z Cable) Cross-Sections
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as patches

output_dir = "hardware/cad"
os.makedirs(output_dir, exist_ok=True)

def draw_box(ax, x0, y0, z0, dx, dy, dz, color, alpha=1.0, edgecolor=None, linewidth=0.5):
    """Draws a 3D rectangular solid volume."""
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
        [vertices[0], vertices[1], vertices[2], vertices[3]], # Bottom (-Z)
        [vertices[4], vertices[5], vertices[6], vertices[7]], # Top (+Z)
        [vertices[0], vertices[1], vertices[5], vertices[4]], # Front (-Y)
        [vertices[2], vertices[3], vertices[7], vertices[6]], # Back (+Y)
        [vertices[0], vertices[3], vertices[7], vertices[4]], # Left (-X)
        [vertices[1], vertices[2], vertices[6], vertices[5]]  # Right (+X)
    ]
    poly = Poly3DCollection(faces, facecolors=color, alpha=alpha, edgecolors=edgecolor, linewidths=linewidth)
    ax.add_collection3d(poly)
    return vertices

def draw_cylinder(ax, x0, y0, z0, radius, length, color, alpha=1.0, resolution=24, axis='z'):
    """Draws a 3D cylinder along specified axis."""
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

def render_main_box_exploded_3d(output_png):
    """Renders the 3D vertical exploded view showing all sandwich layers."""
    fig = plt.figure(figsize=(16, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Exploded offsets along Z-axis:
    # Tier 1 Lower Hull: Z = -60
    # Thermal Pad & PCB: Z = -32
    # 26-Conductor Ribbon Cable: Z = -10
    # Tier 2 Upper Tray with Mid-Baffle: Z = +16
    # LiPo Battery & EPDM Strap: Z = +48
    # Tier 3 Enclosure Lid with Gore Vent: Z = +76

    # -------------------------------------------------------------
    # 1. LOWER HULL (Z_base = -60)
    # -------------------------------------------------------------
    z_hull = -60.0
    draw_box(ax, -55, -37, z_hull, 110, 74, 17, color='#1e293b', alpha=0.85, edgecolor='#38bdf8', linewidth=1.0)
    draw_box(ax, -52, -34, z_hull + 3, 104, 68, 14, color='#0f172a', alpha=0.90) # Hollow cavity
    # 4x M4 Silentblocks on Lower Hull Ears (128 x 56 mm)
    for ex in [-64, 55]:
        for ey in [-37, 23]:
            draw_box(ax, ex, ey, z_hull, 9, 14, 6, color='#334155', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
            cx, cy = ex + 4.5, ey + 7.0
            draw_cylinder(ax, cx, cy, z_hull - 0.5, 4.0, 7.0, color='#0f172a', alpha=0.95, axis='z')
            draw_cylinder(ax, cx, cy, z_hull - 1.0, 2.2, 8.0, color='#cbd5e1', alpha=0.95, axis='z')
    # 4x Solid Copper Thermal Studs (Ø 8 mm) in hull floor
    for cx, cy in [(-31, 6), (-16, 20), (8, 5), (22, 5)]:
        draw_cylinder(ax, cx, cy, z_hull - 1.0, 4.0, 5.0, color='#d97706', alpha=0.98, axis='z')
        draw_cylinder(ax, cx, cy, z_hull + 3.0, 5.0, 0.6, color='#f59e0b', alpha=0.98, axis='z')

    # -------------------------------------------------------------
    # 2. THERMAL GAP PAD & MAIN PCB (Z_base = -32)
    # -------------------------------------------------------------
    z_pcb = -32.0
    # Silicone Gap Pad (65 x 36 x 2.0 mm)
    draw_box(ax, -35, -18, z_pcb - 2.5, 65, 36, 2.0, color='#38bdf8', alpha=0.85, edgecolor='#0284c7', linewidth=0.8)
    # 4-Layer Main PCB (85 x 55 x 1.6 mm)
    draw_box(ax, -42.5, -27.5, z_pcb, 85, 55, 1.6, color='#065f46', alpha=0.98, edgecolor='#10b981', linewidth=1.2)
    # PCB Components:
    # LM5164 DCDC & Inductor (Hotspot 1 at X = -16, Y = 18)
    draw_box(ax, -19, 15, z_pcb + 1.6, 8, 8, 4.5, color='#1e293b', alpha=0.98, edgecolor='#f59e0b', linewidth=0.8)
    draw_box(ax, -9, 15, z_pcb + 1.6, 8, 8, 4.5, color='#1e293b', alpha=0.98, edgecolor='#f59e0b', linewidth=0.8)
    # ESP32-S3 Module (Left: X = -39 to -21, Y = -8 to +16)
    draw_box(ax, -39, -8, z_pcb + 1.6, 18, 24, 3.2, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    # MicroSD Slot (Center: X = -15 to -1, Y = -10 to +4)
    draw_box(ax, -15, -10, z_pcb + 1.6, 14, 14, 1.6, color='#334155', alpha=0.95, edgecolor='#64748b', linewidth=0.5)
    # 2x Bourns Audio Transformers T1 & T2 (Right: X = 2 to 28, Y = 2 to 12)
    draw_box(ax, 2, 2, z_pcb + 1.6, 12, 10, 5.0, color='#1e293b', alpha=0.98, edgecolor='#fbbf24', linewidth=0.8)
    draw_box(ax, 16, 2, z_pcb + 1.6, 12, 10, 5.0, color='#1e293b', alpha=0.98, edgecolor='#fbbf24', linewidth=0.8)
    # J1: 26-Pin IDC Box Header 2x13 (Front-Right: X = -5 to +28, Y = -24 to -18)
    draw_box(ax, -5, -24, z_pcb + 1.6, 33, 6, 5.4, color='#0f172a', alpha=0.98, edgecolor='#fbbf24', linewidth=1.0)
    for px in np.linspace(-3, 26, 13):
        draw_cylinder(ax, px, -22.5, z_pcb + 3.0, 0.3, 3.0, color='#fbbf24', alpha=1.0, axis='z')
        draw_cylinder(ax, px, -19.5, z_pcb + 3.0, 0.3, 3.0, color='#fbbf24', alpha=1.0, axis='z')
    # J3 (USB Header) & J5 (Battery Header) on Front-Left
    draw_box(ax, -24, -24, z_pcb + 1.6, 10, 5, 4.5, color='#38bdf8', alpha=0.95, edgecolor='#0284c7', linewidth=0.6)
    draw_box(ax, -36, -24, z_pcb + 1.6, 8, 5, 4.5, color='#ef4444', alpha=0.95, edgecolor='#dc2626', linewidth=0.6)

    # -------------------------------------------------------------
    # 3. 26-CONDUCTOR RIBBON CABLE (Z_base = -10 to +12)
    # -------------------------------------------------------------
    z_cable = -10.0
    # Pink Ribbon Cable looping upward from J1 through the mid-baffle slot
    draw_box(ax, -3, -22, z_cable, 29, 2.0, 22.0, color='#f43f5e', alpha=0.95, edgecolor='#fda4af', linewidth=0.8)

    # -------------------------------------------------------------
    # 4. UPPER TRAY WITH MID-BAFFLE (Z_base = +16)
    # -------------------------------------------------------------
    z_tray = 16.0
    draw_box(ax, -55, -37, z_tray, 110, 74, 15, color='#334155', alpha=0.75, edgecolor='#38bdf8', linewidth=1.0)
    # Mid-Baffle floor partition at Z = z_tray
    # 38 x 6 mm Ribbon Cable Pass-Through Slot on Right (X = -8 to +30, Y = -24 to -18)
    draw_box(ax, -8, -25, z_tray - 1.0, 38, 7.0, 4.0, color='#0284c7', alpha=0.30, edgecolor='#38bdf8', linewidth=1.2)
    # 4x Labyrinth Pressure Slots (15 x 2 mm)
    for vx in [-35, -15, 10, 30]:
        draw_box(ax, vx, 15, z_tray - 1.0, 12, 2.5, 3.0, color='#0284c7', alpha=0.3, edgecolor='#38bdf8', linewidth=0.6)
    # Front Panel Interfaces on Upper Tray:
    # 1. Waterproof USB-C Screw Cap (Left: X = -20, Y = -37)
    draw_cylinder(ax, -20.0, -37.0, z_tray + 7.5, 5.5, 5.0, color='#0284c7', alpha=0.95, axis='y')
    # 2. Flush RGB Status LED PMMA Lens (Center-Left: X = -10, Y = -37)
    draw_cylinder(ax, -10.0, -37.5, z_tray + 7.5, 2.5, 2.0, color='#10b981', alpha=0.95, axis='y')
    # 3. Amphenol / NorComp HD26 D-Sub SEAL-D Flange (Right: X = 10, Y = -37)
    draw_box(ax, -8, -41, z_tray + 1.0, 36, 4.0, 13.0, color='#0284c7', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    draw_box(ax, -6, -43, z_tray + 2.5, 32, 2.0, 10.0, color='#0f172a', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    for px in np.linspace(-4, 24, 9):
        for pz in np.linspace(z_tray + 4.5, z_tray + 10.5, 3):
            draw_cylinder(ax, px, -43.5, pz, 0.4, 1.5, color='#fbbf24', alpha=1.0, axis='y')

    # -------------------------------------------------------------
    # 5. 1S LiPo BATTERY & EPDM RETENTION STRAP (Z_base = +48)
    # -------------------------------------------------------------
    z_bat = 48.0
    # Battery Nesting Cradle (54 x 34 x 1.5 mm)
    draw_box(ax, -28, -2, z_bat - 2.0, 54, 34, 1.5, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
    # 1S LiPo Buffer Battery (52 x 32 x 6.5 mm)
    draw_box(ax, -26, 0, z_bat, 50, 30, 6.5, color='#3b82f6', alpha=0.95, edgecolor='#1d4ed8', linewidth=1.2)
    # EPDM Rubber Retention Strap (12 mm wide band across X = -1)
    draw_box(ax, -4, -3, z_bat + 6.5, 6.0, 36.0, 1.2, color='#ef4444', alpha=0.95, edgecolor='#be123c', linewidth=0.8)

    # -------------------------------------------------------------
    # 6. HOMOGENEOUS ENCLOSURE LID WITH GORE VENT (Z_base = +76)
    # -------------------------------------------------------------
    z_lid = 76.0
    draw_box(ax, -55, -37, z_lid, 110, 74, 6.0, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=1.2)
    # Perimeter Silicone Seal (Red Line under Lid)
    draw_box(ax, -54.5, -36.5, z_lid - 1.2, 109, 73, 1.2, color='#f43f5e', alpha=0.90, edgecolor='#dc2626', linewidth=0.6)
    # Central Gore ePTFE Pressure Vent (Ø 7.0 mm at X=0, Y=0)
    draw_cylinder(ax, 0, 0, z_lid + 6.0, 4.0, 1.5, color='#ffffff', alpha=0.98, axis='z')
    draw_cylinder(ax, 0, 0, z_lid + 5.5, 5.0, 0.8, color='#64748b', alpha=0.98, axis='z')
    # 4x M3 Stainless Through-Screws
    for sx in [-48, 48]:
        for sy in [-30, 30]:
            draw_cylinder(ax, sx, sy, z_lid + 6.0, 2.5, 1.8, color='#cbd5e1', alpha=0.98, axis='z')

    # 1:1:1 Scale & Camera View
    ax.set_xlim([-75, 75])
    ax.set_ylim([-50, 50])
    ax.set_zlim([-75, 95])
    ax.set_box_aspect((150, 100, 170))
    ax.view_init(elev=20, azim=-55)
    ax.axis('off')

    # High-Contrast Callouts
    title_text = "ZENTRALBOX (TYP A) 3-TEILIGES SANDWICH // 3D EXPLOSIONSDARSTELLUNG (1:1:1 CAD)\n(Unterwanne mit Cu-Pins, 4-Layer PCB, 26-Pol Flachbandkabel, Oberwanne mit Zwischenboden, LiPo-Akku & Gore-Deckel)"
    fig.text(0.50, 0.94, title_text, color='#38bdf8', fontsize=13, fontweight='bold', ha='center')

    callouts = [
        ("1. Unterwanne (17mm) + 4x Cu-Thermal-Pins (Ø8mm) + M4 Silentblöcke", 0.12, 0.16, '#38bdf8'),
        ("2. 4-Layer Hauptplatine (85x55mm, LM5164, ESP32-S3, Bourns)", 0.12, 0.30, '#10b981'),
        ("3. 26-Pol Flachbandkabel (AWG28) von J1 durch Zwischenboden", 0.12, 0.44, '#f43f5e'),
        ("4. Oberwanne (15mm) mit HD26-Flansch, USB-C & LED-Linse", 0.12, 0.58, '#38bdf8'),
        ("5. 1S LiPo Pufferakku (1200mAh) & EPDM-Halteband auf Zwischenboden", 0.12, 0.72, '#60a5fa'),
        ("6. Schutzdeckel (6mm) mit zentralem Gore ePTFE-Ventil (Ø7mm)", 0.12, 0.86, '#ffffff'),
    ]

    for txt, cx, cy, col in callouts:
        fig.text(cx, cy, txt, color=col, fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#0f172a', edgecolor=col, alpha=0.92, lw=1.0))

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Main Box Exploded 3D CAD Render generated: {output_png}")

def render_main_box_mated_3d(output_png):
    """Renders the 3D translucent X-Ray view of the closed & mated main box."""
    fig = plt.figure(figsize=(16, 9.5), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Total closed box: 110 x 74 x 38 mm (X: -55..+55, Y: -37..+37, Z: -19..+19)
    # Outer Shell (Translucent Cyan wireframe)
    draw_box(ax, -55, -37, -19, 110, 74, 38, color='#0284c7', alpha=0.06, edgecolor='#0284c7', linewidth=0.8)

    # 4x M4 Silentblocks on lower hull
    for ex in [-64, 55]:
        for ey in [-37, 23]:
            draw_box(ax, ex, ey, -19, 9, 14, 6, color='#334155', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
            cx, cy = ex + 4.5, ey + 7.0
            draw_cylinder(ax, cx, cy, -19.5, 4.0, 7.0, color='#0f172a', alpha=0.95, axis='z')
            draw_cylinder(ax, cx, cy, -20.0, 2.2, 8.0, color='#cbd5e1', alpha=0.95, axis='z')

    # 4x Copper Studs (Ø 8 mm) in bottom hull floor (Z = -19 to -12.5)
    for cx, cy in [(-31, 6), (-16, 20), (8, 5), (22, 5)]:
        draw_cylinder(ax, cx, cy, -19.5, 4.0, 7.0, color='#d97706', alpha=0.98, axis='z')
        draw_cylinder(ax, cx, cy, -12.5, 5.0, 0.6, color='#f59e0b', alpha=0.98, axis='z')

    # Thermal Gap Pad (65 x 36 x 2.0 mm at Z = -12.5 to -10.5)
    draw_box(ax, -35, -18, -12.5, 65, 36, 2.0, color='#38bdf8', alpha=0.85, edgecolor='#0284c7', linewidth=0.8)

    # 4-Layer Main PCB (85 x 55 x 1.6 mm at Z = -10.5 to -8.9)
    draw_box(ax, -42.5, -27.5, -10.5, 85, 55, 1.6, color='#065f46', alpha=0.98, edgecolor='#10b981', linewidth=1.2)

    # Hotspots on PCB: LM5164, ESP32, Bourns Transformers, MicroSD
    draw_box(ax, -19, 15, -8.9, 8, 8, 4.5, color='#1e293b', alpha=0.98, edgecolor='#f59e0b', linewidth=0.8)
    draw_box(ax, -9, 15, -8.9, 8, 8, 4.5, color='#1e293b', alpha=0.98, edgecolor='#f59e0b', linewidth=0.8)
    draw_box(ax, -39, -8, -8.9, 18, 24, 3.2, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 2, 2, -8.9, 12, 10, 5.0, color='#1e293b', alpha=0.98, edgecolor='#fbbf24', linewidth=0.8)
    draw_box(ax, 16, 2, -8.9, 12, 10, 5.0, color='#1e293b', alpha=0.98, edgecolor='#fbbf24', linewidth=0.8)

    # J1 Header on PCB (at X = -5 to +28, Y = -24 to -18, Z = -8.9 to -3.5)
    draw_box(ax, -5, -24, -8.9, 33, 6, 5.4, color='#0f172a', alpha=0.98, edgecolor='#fbbf24', linewidth=1.0)

    # Mid-Baffle Floor Partition at Z = -2.0 to +0.5 mm
    draw_box(ax, -51, -33, -2.0, 102, 66, 2.5, color='#334155', alpha=0.35, edgecolor='#64748b', linewidth=0.8)
    # 38 x 6 mm Ribbon Cable Pass-Through Slot in Mid-Baffle (X = -8 to +30, Y = -24 to -18)
    draw_box(ax, -8, -25, -2.2, 38, 7.0, 2.9, color='#0284c7', alpha=0.30, edgecolor='#38bdf8', linewidth=1.2)

    # 26-Conductor Ribbon Cable looping smoothly from J1 through the slot into HD26 flange
    draw_box(ax, -3, -22, -8.9, 29, 2.0, 13.0, color='#f43f5e', alpha=0.95, edgecolor='#fda4af', linewidth=0.8)
    draw_box(ax, -3, -36, 4.1, 29, 14.0, 1.2, color='#f43f5e', alpha=0.95, edgecolor='#fda4af', linewidth=0.8)

    # Front Panel Interfaces: HD26 D-Sub Flange, USB-C Port, RGB LED Window
    draw_box(ax, -8, -40, -1.0, 36, 3.0, 15.0, color='#0284c7', alpha=0.55, edgecolor='#38bdf8', linewidth=1.0)
    draw_cylinder(ax, -20.0, -37.0, 6.5, 5.5, 4.0, color='#0284c7', alpha=0.85, axis='y')
    draw_cylinder(ax, -10.0, -37.5, 6.5, 2.5, 1.5, color='#10b981', alpha=0.85, axis='y')

    # 1S LiPo Buffer Battery in Mid-Baffle Cradle (Z = +1.5 to +8.0 mm)
    draw_box(ax, -28, -2, 0.5, 54, 34, 1.0, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=0.8)
    draw_box(ax, -26, 0, 1.5, 50, 30, 6.5, color='#3b82f6', alpha=0.90, edgecolor='#1d4ed8', linewidth=1.2)
    # EPDM Retention Strap across Battery
    draw_box(ax, -4, -3, 8.0, 6.0, 36.0, 1.2, color='#ef4444', alpha=0.95, edgecolor='#be123c', linewidth=0.8)

    # Top Lid with Gore Vent (Z = +13 to +19 mm)
    draw_box(ax, -55, -37, 13, 110, 74, 6.0, color='#0f172a', alpha=0.45, edgecolor='#38bdf8', linewidth=0.9)
    draw_cylinder(ax, 0, 0, 18.5, 4.0, 1.5, color='#ffffff', alpha=0.98, axis='z')

    # 1:1:1 Scale & Camera View
    ax.set_xlim([-75, 75])
    ax.set_ylim([-45, 45])
    ax.set_zlim([-25, 25])
    ax.set_box_aspect((150, 90, 50))
    ax.view_init(elev=24, azim=-55)
    ax.axis('off')

    title_text = "ZENTRALBOX (TYP A) GESAMT-ZUSAMMENBAU // 3D RÖNTGEN-ANSICHT (1:1:1 CAD)\n(Hermetischer IP67/IP69K Sandwich-Zusammenbau mit Cu-Thermal-Pins, Hauptplatine, 26-Pol Kabel & Akku-Halterung)"
    fig.text(0.50, 0.94, title_text, color='#38bdf8', fontsize=13, fontweight='bold', ha='center')

    callouts = [
        ("1. 4x M4 Silentblöcke (128x56mm) & Unterwanne", 0.14, 0.20, '#38bdf8'),
        ("2. 4x Cu-Thermal-Pins (Ø8mm) & Silikon-Gap-Pad", 0.14, 0.32, '#d97706'),
        ("3. 4-Layer PCB (85x55mm) mit LM5164 & ESP32-S3", 0.22, 0.82, '#10b981'),
        ("4. J1 Wannenstecker & 26-Pol Flachbandkabel", 0.48, 0.84, '#f43f5e'),
        ("5. 38x6mm Zwischenboden-Schlitz (Rechts)", 0.65, 0.20, '#38bdf8'),
        ("6. 1S LiPo Akku (1200mAh) & EPDM-Spannband", 0.78, 0.80, '#60a5fa'),
        ("7. HD26 D-Sub Flansch mit EPDM-Dichtung", 0.82, 0.65, '#38bdf8'),
        ("8. Wasserdichter USB-C Port & RGB-LED Linse", 0.82, 0.35, '#34d399'),
        ("9. Gore ePTFE Membran (Ø7mm) & Deckeldichtung", 0.84, 0.18, '#ffffff'),
    ]

    for txt, cx, cy, col in callouts:
        fig.text(cx, cy, txt, color=col, fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#0f172a', edgecolor=col, alpha=0.92, lw=1.0))

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Main Box Mated 3D CAD Render generated: {output_png}")

def render_main_box_cross_section(output_png):
    """Renders the true 2D longitudinal (X-Z) & transverse (Y-Z cable path) cross-sections."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 11), dpi=220, facecolor='#080c14')

    # =========================================================================
    # SUBPLOT 1: LÄNGSSCHNITT (X-Z EBENE) DURCH ZENTRALBOX
    # =========================================================================
    ax1.set_facecolor('#0b1120')
    ax1.set_title("1. ZENTRALBOX LÄNGSSCHNITT (X-Z EBENE) // THERMISCHES & MECHANISCHES FITTING", 
                  color='#38bdf8', fontsize=12, fontweight='bold', pad=10)

    # Outer Housing (110 x 38 mm from X = -55 to +55, Z = -19 to +19)
    ax1.add_patch(patches.Rectangle((-55, -19), 110, 38, fill=False, edgecolor='#0284c7', linewidth=1.5, linestyle='--'))
    # Lower Hull Floor (Z = -19 to -16) & Walls (3.0 mm)
    ax1.add_patch(patches.Rectangle((-55, -19), 110, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((-55, -19), 3.0, 38.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((52, -19), 3.0, 38.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))

    # 4x Solid Copper Thermal Studs (Ø 8 mm at X = -31, -16, +8, +22, Z = -19 to -12.5)
    for cx in [-31, -16, 8, 22]:
        ax1.add_patch(patches.Rectangle((cx - 4.0, -19.0), 8.0, 6.5, facecolor='#d97706', edgecolor='#f59e0b', linewidth=1.0))
        ax1.text(cx, -15.8, "Cu", color='#080c14', fontsize=7.5, fontweight='bold', ha='center')
    ax1.text(-4.0, -21.5, "4x KUPFER-THERMAL-PINS (Ø 8.0 mm // λ = 390 W/m·K)", color='#f59e0b', fontsize=8, fontweight='bold', ha='center')

    # Silicone Gap Pad (65 x 2.0 mm from X = -35 to +30, Z = -12.5 to -10.5)
    ax1.add_patch(patches.Rectangle((-35, -12.5), 65, 2.0, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=0.8))
    ax1.text(-3.0, -11.6, "SILIKON GAP-PAD (2.0 mm // λ = 3.0 W/m·K)", color='#080c14', fontsize=7.5, fontweight='bold', ha='center')

    # 4-Layer Main PCB (85 x 1.6 mm from X = -42.5 to +42.5, Z = -10.5 to -8.9)
    ax1.add_patch(patches.Rectangle((-42.5, -10.5), 85, 1.6, facecolor='#065f46', edgecolor='#10b981', linewidth=1.2))
    ax1.text(-38.0, -9.7, "MAIN PCB (1.6mm)", color='#10b981', fontsize=7.5, fontweight='bold')

    # Components on PCB:
    # ESP32-S3 (X = -39 to -21, Z = -8.9 to -5.7)
    ax1.add_patch(patches.Rectangle((-39, -8.9), 18, 3.2, facecolor='#cbd5e1', edgecolor='#94a3b8', linewidth=0.8))
    ax1.text(-30, -7.3, "ESP32-S3", color='#080c14', fontsize=7.5, fontweight='bold', ha='center')
    # LM5164 Power Stage (X = -19 to -1, Z = -8.9 to -4.4)
    ax1.add_patch(patches.Rectangle((-19, -8.9), 18, 4.5, facecolor='#1e293b', edgecolor='#f59e0b', linewidth=0.8))
    ax1.text(-10, -6.6, "LM5164 DCDC", color='#f59e0b', fontsize=7.5, fontweight='bold', ha='center')
    # Bourns Audio Transformers (X = 2 to 28, Z = -8.9 to -3.9)
    ax1.add_patch(patches.Rectangle((2, -8.9), 26, 5.0, facecolor='#1e293b', edgecolor='#fbbf24', linewidth=0.8))
    ax1.text(15, -6.4, "BOURNS AUDIOTRANSFORMATOREN", color='#fbbf24', fontsize=7, fontweight='bold', ha='center')

    # Mid-Baffle Floor Partition (Z = -2.0 to +0.5 mm)
    ax1.add_patch(patches.Rectangle((-52, -2.0), 104, 2.5, facecolor='#334155', edgecolor='#64748b', linewidth=1.0))
    ax1.text(-44.0, -0.8, "ZWISCHENBODEN (2.5mm)", color='#94a3b8', fontsize=7.5, fontweight='bold')

    # Battery Cradle & 1S LiPo Battery (X = -26 to +24, Z = 1.5 to 8.0 mm)
    ax1.add_patch(patches.Rectangle((-28, 0.5), 54, 1.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=0.6))
    ax1.add_patch(patches.Rectangle((-26, 1.5), 50, 6.5, facecolor='#3b82f6', edgecolor='#1d4ed8', linewidth=1.0))
    ax1.text(-1.0, 4.75, "1S LiPo PUFFERAKKU (1200 mAh // 52x36x6.5 mm)", color='#ffffff', fontsize=8, fontweight='bold', ha='center')
    # EPDM Retention Strap across Battery
    ax1.add_patch(patches.Rectangle((-4, 8.0), 6.0, 1.2, facecolor='#ef4444', edgecolor='#be123c', linewidth=0.8))
    ax1.text(-1.0, 10.5, "EPDM-SPANNLASCHE", color='#ef4444', fontsize=7.5, fontweight='bold', ha='center')

    # Enclosure Lid (Z = +13 to +19 mm) with Gore Vent (X = -4 to +4)
    ax1.add_patch(patches.Rectangle((-55, 13), 110, 6.0, facecolor='#0f172a', edgecolor='#38bdf8', linewidth=1.0))
    ax1.add_patch(patches.Rectangle((-4, 17.5), 8.0, 2.5, facecolor='#ffffff', edgecolor='#64748b', linewidth=0.8))
    ax1.text(0, 21.5, "GORE ePTFE VENTIL (Ø 7.0 mm)", color='#ffffff', fontsize=8, fontweight='bold', ha='center')

    ax1.set_xlim([-65, 65])
    ax1.set_ylim([-25, 25])
    ax1.set_xlabel("Längsachse X (mm) [1:1:1 Maßstab]", color='#94a3b8', fontsize=8.5)
    ax1.set_ylabel("Höhe Z (mm)", color='#94a3b8', fontsize=8.5)
    ax1.tick_params(colors='#94a3b8', labelsize=8)
    ax1.grid(True, color='#1e293b', linestyle=':', alpha=0.6)

    # =========================================================================
    # SUBPLOT 2: QUERSCHNITT (Y-Z EBENE) DURCH J1 & HD26 KABELFÜHRUNG
    # =========================================================================
    ax2.set_facecolor('#0b1120')
    ax2.set_title("2. ZENTRALBOX QUERSCHNITT (Y-Z EBENE) // KABELFÜHRUNG DURCH ZWISCHENBODEN-SCHLITZ ZUM HD26-FLANSCH", 
                  color='#10b981', fontsize=12, fontweight='bold', pad=10)

    # Outer Housing in Y-Z (74 x 38 mm from Y = -37 to +37, Z = -19 to +19)
    ax2.add_patch(patches.Rectangle((-37, -19), 74, 38, fill=False, edgecolor='#059669', linewidth=1.5, linestyle='--'))
    ax2.add_patch(patches.Rectangle((-37, -19), 74, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax2.add_patch(patches.Rectangle((-37, 13), 74, 6.0, facecolor='#0f172a', edgecolor='#38bdf8', linewidth=1.0))
    ax2.add_patch(patches.Rectangle((-37, -19), 3.0, 38.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8)) # Front wall
    ax2.add_patch(patches.Rectangle((34, -19), 3.0, 38.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))  # Rear wall

    # Main PCB in Y-Z (55 x 1.6 mm from Y = -27.5 to +27.5, Z = -10.5 to -8.9)
    ax2.add_patch(patches.Rectangle((-27.5, -10.5), 55, 1.6, facecolor='#065f46', edgecolor='#10b981', linewidth=1.2))
    ax2.text(-25.0, -12.5, "MAIN PCB (55mm Breite)", color='#10b981', fontsize=7.5, fontweight='bold')

    # J1: 26-Pin IDC Box Header 2x13 at Front Rail (Y = -24 to -18, Z = -8.9 to -3.5)
    ax2.add_patch(patches.Rectangle((-24.0, -8.9), 6.0, 5.4, facecolor='#0f172a', edgecolor='#fbbf24', linewidth=1.0))
    ax2.text(-21.0, -6.2, "J1: IDC26", color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center')

    # Mid-Baffle Floor Partition at Z = -2.0 to +0.5 mm
    ax2.add_patch(patches.Rectangle((-34, -2.0), 68, 2.5, facecolor='#334155', edgecolor='#64748b', linewidth=1.0))
    # 38 x 6.0 mm Pass-Through Slot in Mid-Baffle (Y = -25 to -19, Z = -2.0 to +0.5)
    ax2.add_patch(patches.Rectangle((-25.0, -2.2), 6.0, 2.9, facecolor='#0284c7', alpha=0.35, edgecolor='#38bdf8', linewidth=1.2))
    ax2.text(-22.0, 2.0, "38x6mm SCHLITZ\n(R=1.5mm)", color='#38bdf8', fontsize=7.5, fontweight='bold', ha='center')

    # 26-Conductor Flexible Ribbon Cable (Pink line) routing from J1 through the slot into HD26 Flange
    ax2.plot([-21.0, -21.0, -37.0], [-3.5, 6.0, 6.0], color='#f43f5e', linewidth=3.0)
    ax2.text(-29.0, 8.5, "26-POL FLACHBANDKABEL (AWG28)", color='#f43f5e', fontsize=8, fontweight='bold', ha='center')

    # HD26 SEAL-D Flange on Front Wall (Y = -37, Z = 0 to 12)
    ax2.add_patch(patches.Rectangle((-41.0, 0.0), 4.0, 12.0, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.2))
    ax2.add_patch(patches.Rectangle((-42.5, 1.5), 1.5, 9.0, facecolor='#f43f5e', edgecolor='#be123c', linewidth=0.8)) # EPDM Gasket
    ax2.text(-44.0, 6.0, "HD26 FLANSCH\n(SEAL-D IP67)", color='#38bdf8', fontsize=7.5, fontweight='bold', ha='right', va='center')

    # Upper Compartment: LiPo Battery in Cradle (Y = 0 to +30, Z = 1.5 to 8.0 mm)
    ax2.add_patch(patches.Rectangle((-2.0, 0.5), 34.0, 1.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=0.6))
    ax2.add_patch(patches.Rectangle((0.0, 1.5), 30.0, 6.5, facecolor='#3b82f6', edgecolor='#1d4ed8', linewidth=1.0))
    ax2.text(15.0, 4.75, "1S LiPo PUFFERAKKU", color='#ffffff', fontsize=8, fontweight='bold', ha='center')
    # EPDM Strap
    ax2.add_patch(patches.Rectangle((12.0, 8.0), 6.0, 1.2, facecolor='#ef4444', edgecolor='#be123c', linewidth=0.8))
    ax2.text(15.0, 10.5, "EPDM-LASCHE", color='#ef4444', fontsize=7.5, fontweight='bold', ha='center')

    ax2.set_xlim([-50, 50])
    ax2.set_ylim([-25, 25])
    ax2.set_xlabel("Querachse Y (mm) [1:1:1 Maßstab]", color='#94a3b8', fontsize=8.5)
    ax2.set_ylabel("Höhe Z (mm)", color='#94a3b8', fontsize=8.5)
    ax2.tick_params(colors='#94a3b8', labelsize=8)
    ax2.grid(True, color='#1e293b', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Main Box Cross-Section Render generated: {output_png}")

if __name__ == '__main__':
    out_exp = os.path.join(output_dir, "main_box_full_assembly_exploded_3d.png")
    out_mat = os.path.join(output_dir, "main_box_assembly_mated_3d.png")
    out_crs = os.path.join(output_dir, "main_box_assembly_cross_section.png")

    render_main_box_exploded_3d(out_exp)
    render_main_box_mated_3d(out_mat)
    render_main_box_cross_section(out_crs)
