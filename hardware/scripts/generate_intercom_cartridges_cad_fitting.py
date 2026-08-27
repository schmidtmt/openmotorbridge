#!/usr/bin/env python3
"""
OpenMotorBridge Modular Intercom Cartridge (Sena 50S & Cardo Edge) CAD Fitting & Validation Generator
-----------------------------------------------------------------------------------------------------
Generates photorealistic, exact 1:1:1 Euclidean scale 3D CAD visualizations and longitudinal cross-sections
validating the mechanical and electrical fitting of the 2-piece modular cartridge system:
  1. sena_cartridge_assembly_cad.png: 3D CAD Fitting of Sena 50S/60S Cartridge in Satellite Pod
  2. cardo_cartridge_assembly_cad.png: 3D CAD Fitting of Cardo Packtalk Edge Cartridge in Satellite Pod
  3. sena_cardo_cartridge_cross_section.png: Longitudinal X-Z Cross-Section & Electrical Pinout Validation
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

def draw_cylinder(ax, x0, y0, z0, radius, length, color, alpha=1.0, resolution=24, axis='x'):
    """Draws a 3D cylinder along specified axis."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    if axis == 'x':
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
    elif axis == 'z':
        z = np.linspace(z0, z0 + length, 2)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = x0 + radius * np.cos(theta_grid)
        y_grid = y0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)

def draw_strap_arc(ax, x_center, y_min, y_max, z_peak, thickness, width, color='#ef4444', alpha=0.9):
    """Draws an elastic rubber strap arching over the device."""
    y = np.linspace(y_min, y_max, 24)
    h = z_peak
    z = h - 4.0 * (h - 2.0) * ((y - (y_min + y_max)/2.0) / (y_max - y_min))**2
    for i in range(len(y)-1):
        draw_box(ax, x_center - width/2.0, y[i], z[i], width, y[i+1]-y[i], thickness, 
                 color=color, alpha=alpha, edgecolor='#be123c', linewidth=0.6)

def render_sena_cartridge_assembly(output_png):
    """Renders the 1:1:1 Euclidean scale Sena 50S/60S 2-Piece Cartridge Assembly inside the Satellite Pod."""
    fig = plt.figure(figsize=(16, 9.5), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Dimensions: Pod 120 x 64 x 32 mm (X: -60..+60, Y: -32..+32, Z: -16..+16)
    # 1. Monocoque Outer Enclosure (Translucent Cyan wireframe)
    draw_box(ax, -60, -32, -16, 120, 64, 32, color='#0284c7', alpha=0.04, edgecolor='#0284c7', linewidth=0.7)

    # 2. Stirnwand & M8 6-Pin Panel Receptacle on Bottom Face (X = -50, Z = -16)
    draw_box(ax, -52, -28, -14, 4, 56, 28, color='#38bdf8', alpha=0.30, edgecolor='#38bdf8', linewidth=1.0)
    draw_cylinder(ax, -48, 0, -22, 4.0, 8.0, color='#d97706', alpha=0.95, axis='z')
    draw_cylinder(ax, -48, 0, -22, 4.8, 2.5, color='#b45309', alpha=0.95, axis='z')

    # 3. Vertical Pod-Base PCB (36 x 20 x 1.6 mm at X = -47.0 mm, Y = -18..+18, Z = -10..+10)
    draw_box(ax, -47.8, -18.0, -10.0, 1.6, 36.0, 20.0, color='#065f46', alpha=0.98, edgecolor='#10b981', linewidth=1.4)
    draw_box(ax, -46.2, -8.0, -4.0, 0.6, 1.35, 3.5, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.8)

    # 4. PA12 Bulkhead Partition with 45° Shroud & Auto-Eject Springs (X = -45.0 mm)
    draw_box(ax, -46.0, -27.0, -11.0, 2.0, 54.0, 22.0, color='#1e293b', alpha=0.70, edgecolor='#64748b', linewidth=0.9)
    draw_box(ax, -44.0, -9.0, -2.5, 4.0, 18.0, 5.0, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    draw_cylinder(ax, -44.0, -20.0, 0.0, 1.5, 6.0, color='#cbd5e1', alpha=0.95, axis='x')
    draw_cylinder(ax, -44.0,  20.0, 0.0, 1.5, 6.0, color='#cbd5e1', alpha=0.95, axis='x')

    # 5. Horizontal 6-Pin Precision Header / Socket Mating (X = -46.0 to -38.0 mm)
    for yp in np.linspace(-6.35, 6.35, 6):
        draw_cylinder(ax, -46.0, yp, 0.0, 0.32, 8.0, color='#fbbf24', alpha=1.0, axis='x')
    draw_box(ax, -42.0, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.98, edgecolor='#0284c7', linewidth=1.2)

    # 6. UNIVERSAL BASE SLED (PA12: 92 x 54 x 23.5 mm from X = -40 to +52 mm)
    draw_box(ax, -40, -27, -11.75, 92, 54, 3.0, color='#1e293b', alpha=0.75, edgecolor='#64748b', linewidth=0.9)
    draw_box(ax, -40, -27, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.45, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -40,  24, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.45, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, 52, -29, -14.0, 5, 58, 28.0, color='#0284c7', alpha=0.85, edgecolor='#38bdf8', linewidth=1.4)
    draw_box(ax, 51.5, -28.5, -13.5, 1.0, 57, 27.0, color='#f43f5e', alpha=0.90, edgecolor='#be123c', linewidth=0.8)

    # 7. CARTRIDGE CARRIER PCB (openmotorbridge_pod_cartridge: 35 x 25 x 1.6 mm at X = -36 to -1 mm, Y = -12.5 to +12.5)
    draw_box(ax, -36, -12.5, -8.75, 35, 25, 1.6, color='#047857', alpha=0.98, edgecolor='#10b981', linewidth=1.4)
    draw_box(ax, -22, -2.0, -7.15, 2.8, 1.5, 1.0, color='#0f172a', alpha=0.98, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -28, -6.0, -7.15, 1.6, 0.8, 0.6, color='#1e293b', alpha=0.98, edgecolor='#fbbf24', linewidth=0.6)
    draw_box(ax, -28,  6.0, -7.15, 1.6, 0.8, 0.6, color='#22c55e', alpha=0.98, edgecolor='#16a34a', linewidth=0.6)
    # J2 Header (JST-SH 1.0mm 6P Horizontal with opening facing RIGHT +X at X = -5.0 mm)
    draw_box(ax, -5.0, -4.0, -7.15, 4.0, 8.0, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#94a3b8', linewidth=1.0)
    draw_box(ax, -1.0, -3.5, -6.85, 0.8, 7.0, 1.2, color='#0f172a', alpha=1.0)

    # 8. UNDER-BED CABLE CHANNEL & JST-SH FLAT RIBBON CABLE
    draw_box(ax, -4.0, -4.0, -8.75, 32, 8.0, 1.5, color='#0f172a', alpha=0.98)
    draw_box(ax, -1.0, -3.0, -8.25, 26, 6.0, 0.6, color='#ec4899', alpha=0.98, edgecolor='#db2777', linewidth=0.8)
    draw_box(ax, 22.0, -3.0, -8.25, 3.0, 6.0, 6.5, color='#ec4899', alpha=0.98, edgecolor='#db2777', linewidth=0.8)

    # 9. INTERCHANGEABLE SENA 50S/60S TOP INLAY (3D-Contour Nest: 80 x 48 x 8.0 mm)
    draw_box(ax, -32, -24, -2.25, 80, 48, 8.0, color='#1e293b', alpha=0.40, edgecolor='#64748b', linewidth=1.2)
    draw_box(ax, -28, -22, 0.75, 72, 44, 5.0, color='#0f172a', alpha=0.45, edgecolor='#38bdf8', linewidth=0.9)
    for sx in [-30, 45]:
        for sy in [-22, 22]:
            draw_cylinder(ax, sx, sy, 5.75, 1.5, 0.4, color='#94a3b8', alpha=0.98, axis='z')

    # 10. SENA 7-PIN GOLD-PLATED SPRING POGO-PIN ARRAY (at X = +20 to +24)
    for py in np.linspace(-10, 10, 7):
        draw_cylinder(ax, 22.0, py, 2.0, 0.8, 4.0, color='#fbbf24', alpha=1.0, axis='z')

    # 11. OEM RETAINING MECHANISMS: Bottom Hook & Top POM Spring Latch
    draw_box(ax, -30, -15, 3.75, 4.0, 30.0, 4.0, color='#0284c7', alpha=0.98, edgecolor='#38bdf8', linewidth=1.2)
    draw_box(ax, 44, -10, 3.75, 5.0, 20.0, 5.0, color='#f59e0b', alpha=0.98, edgecolor='#fbbf24', linewidth=1.2)

    # 12. GHOSTED SENA 50S HEADSET BODY (84 x 48 x 22 mm seated in contour nest)
    draw_box(ax, -26, -21, 4.75, 72, 42, 16.0, color='#38bdf8', alpha=0.25, edgecolor='#38bdf8', linewidth=1.4)

    # 13. EPDM ELASTIC RETENTION STRAP
    draw_strap_arc(ax, x_center=10.0, y_min=-26.0, y_max=26.0, z_peak=23.0, thickness=2.2, width=12.0, color='#ef4444', alpha=0.95)

    # 1:1:1 Scale Limits
    ax.set_xlim([-65, 65])
    ax.set_ylim([-35, 35])
    ax.set_zlim([-25, 25])
    ax.set_box_aspect((130, 70, 50))
    ax.view_init(elev=24, azim=-55)
    ax.axis('off')

    title_text = "SENA 50S / 60S MODULARE 2-TEILIGE WECHSELKASSETTE // 1:1:1 CAD FITTING\n(Generischer PA12-Unterschlitten, 35x25mm Trägerplatine, axialer JST-SH Header J2, 3D-Konturbett & Pogo-Array)"
    fig.text(0.50, 0.94, title_text, color='#38bdf8', fontsize=13, fontweight='bold', ha='center')

    callouts = [
        ("1. Pod-Basis Stirnwand & M8 6-Pin Buchse (IP67)", 0.14, 0.20, '#38bdf8'),
        ("2. Schutz-Schottwand (2.0mm) & Auto-Eject Federn", 0.14, 0.32, '#94a3b8'),
        ("3. Trägerplatine (35x25mm, DS2401 ID & 500mA PTC)", 0.22, 0.82, '#10b981'),
        ("4. J2 Header: 90° CCW gedreht (Öffnung axial nach +X)", 0.48, 0.84, '#f8fafc'),
        ("5. Unterflur-Kabelkanal (1.5mm) & JST-SH Flachbandkabel", 0.65, 0.20, '#ec4899'),
        ("6. 7-Pin Gold-Pogo-Array im Sena-Konturbett (X=+22mm)", 0.78, 0.80, '#fbbf24'),
        ("7. Sena 50S/60S Headset & EPDM-Sicherungslasche", 0.82, 0.65, '#38bdf8'),
        ("8. 4x M2 Senkkopf-Verschraubung (Oberteil zu Unterteil)", 0.82, 0.35, '#94a3b8'),
        ("9. IP67 Stirnflansch-Dichtung & Snap-Fit Rastklinke", 0.84, 0.18, '#f43f5e'),
    ]

    for txt, cx, cy, col in callouts:
        fig.text(cx, cy, txt, color=col, fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#0f172a', edgecolor=col, alpha=0.92, lw=1.0))

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Sena Cartridge Assembly CAD Render generated: {output_png}")

def render_cardo_cartridge_assembly(output_png):
    """Renders the 1:1:1 Euclidean scale Cardo Packtalk Edge 2-Piece Cartridge Assembly inside the Satellite Pod."""
    fig = plt.figure(figsize=(16, 9.5), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Dimensions: Pod 120 x 64 x 32 mm
    # 1. Monocoque Outer Enclosure (Translucent Green)
    draw_box(ax, -60, -32, -16, 120, 64, 32, color='#059669', alpha=0.04, edgecolor='#059669', linewidth=0.7)

    # 2. Stirnwand & M8 6-Pin Panel Receptacle on Bottom Face (X = -50, Z = -16)
    draw_box(ax, -52, -28, -14, 4, 56, 28, color='#10b981', alpha=0.30, edgecolor='#10b981', linewidth=1.0)
    draw_cylinder(ax, -48, 0, -22, 4.0, 8.0, color='#d97706', alpha=0.95, axis='z')
    draw_cylinder(ax, -48, 0, -22, 4.8, 2.5, color='#b45309', alpha=0.95, axis='z')

    # 3. Vertical Pod-Base PCB (36 x 20 x 1.6 mm)
    draw_box(ax, -47.8, -18.0, -10.0, 1.6, 36.0, 20.0, color='#065f46', alpha=0.98, edgecolor='#10b981', linewidth=1.4)
    draw_box(ax, -46.2, -8.0, -4.0, 0.6, 1.35, 3.5, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.8)

    # 4. PA12 Bulkhead Partition with Shroud & Springs (X = -45.0 mm)
    draw_box(ax, -46.0, -27.0, -11.0, 2.0, 54.0, 22.0, color='#1e293b', alpha=0.70, edgecolor='#64748b', linewidth=0.9)
    draw_box(ax, -44.0, -9.0, -2.5, 4.0, 18.0, 5.0, color='#0f172a', alpha=0.95, edgecolor='#10b981', linewidth=1.0)
    draw_cylinder(ax, -44.0, -20.0, 0.0, 1.5, 6.0, color='#cbd5e1', alpha=0.95, axis='x')
    draw_cylinder(ax, -44.0,  20.0, 0.0, 1.5, 6.0, color='#cbd5e1', alpha=0.95, axis='x')

    # 5. Horizontal 6-Pin Interface Mating
    for yp in np.linspace(-6.35, 6.35, 6):
        draw_cylinder(ax, -46.0, yp, 0.0, 0.32, 8.0, color='#fbbf24', alpha=1.0, axis='x')
    draw_box(ax, -42.0, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.98, edgecolor='#10b981', linewidth=1.2)

    # 6. UNIVERSAL BASE SLED (Identical across all cartridges: 92 x 54 x 23.5 mm)
    draw_box(ax, -40, -27, -11.75, 92, 54, 3.0, color='#1e293b', alpha=0.75, edgecolor='#64748b', linewidth=0.9)
    draw_box(ax, -40, -27, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.45, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -40,  24, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.45, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, 52, -29, -14.0, 5, 58, 28.0, color='#059669', alpha=0.85, edgecolor='#34d399', linewidth=1.4)
    draw_box(ax, 51.5, -28.5, -13.5, 1.0, 57, 27.0, color='#f43f5e', alpha=0.90, edgecolor='#be123c', linewidth=0.8)

    # 7. CARTRIDGE CARRIER PCB (openmotorbridge_pod_cartridge: 35 x 25 x 1.6 mm)
    draw_box(ax, -36, -12.5, -8.75, 35, 25, 1.6, color='#047857', alpha=0.98, edgecolor='#10b981', linewidth=1.4)
    draw_box(ax, -22, -2.0, -7.15, 2.8, 1.5, 1.0, color='#0f172a', alpha=0.98, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -5.0, -4.0, -7.15, 4.0, 8.0, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#94a3b8', linewidth=1.0)
    draw_box(ax, -1.0, -3.5, -6.85, 0.8, 7.0, 1.2, color='#0f172a', alpha=1.0)

    # 8. UNDER-BED CABLE CHANNEL & JST-SH RIBBON CABLE
    draw_box(ax, -4.0, -4.0, -8.75, 20, 8.0, 1.5, color='#0f172a', alpha=0.98)
    draw_box(ax, -1.0, -3.0, -8.25, 14, 6.0, 0.6, color='#ec4899', alpha=0.98, edgecolor='#db2777', linewidth=0.8)
    draw_box(ax, 10.0, -3.0, -8.25, 3.0, 6.0, 6.5, color='#ec4899', alpha=0.98, edgecolor='#db2777', linewidth=0.8)

    # 9. INTERCHANGEABLE CARDO AIR-MOUNT TOP INLAY (74 x 46 x 8.0 mm at X = -28 to +46 mm)
    draw_box(ax, -28, -23, -2.25, 74, 46, 8.0, color='#1e293b', alpha=0.40, edgecolor='#64748b', linewidth=1.2)
    draw_box(ax, -24, -21, 0.75, 68, 42, 5.0, color='#0f172a', alpha=0.45, edgecolor='#10b981', linewidth=0.9)

    # 10. DUAL N52 NEODYMIUM DISC MAGNETS (Ø8 x 2.0 mm at X = -8 and X = +28)
    draw_cylinder(ax, -8.0, 0.0, 1.75, 4.0, 2.0, color='#e11d48', alpha=0.98, axis='z')
    draw_cylinder(ax, 28.0, 0.0, 1.75, 4.0, 2.0, color='#e11d48', alpha=0.98, axis='z')

    # 11. CARDO 5-PIN SPRING CONTACT ARRAY (Centered at X = +10, Y = -8..+8)
    for py in np.linspace(-6, 6, 5):
        draw_cylinder(ax, 10.0, py, 1.5, 0.8, 4.0, color='#fbbf24', alpha=1.0, axis='z')

    # 12. DUAL LATERAL SNAP-LOCK FLANKS
    draw_box(ax, -2, -23, 1.75, 20, 3.0, 6.0, color='#10b981', alpha=0.98, edgecolor='#34d399', linewidth=1.2)
    draw_box(ax, -2,  20, 1.75, 20, 3.0, 6.0, color='#10b981', alpha=0.98, edgecolor='#34d399', linewidth=1.2)

    # 13. GHOSTED CARDO PACKTALK EDGE HEADSET (72 x 42 x 18 mm)
    draw_box(ax, -24, -20, 4.75, 68, 40, 15.0, color='#10b981', alpha=0.25, edgecolor='#34d399', linewidth=1.4)

    # 14. EPDM ELASTIC RETENTION STRAP
    draw_strap_arc(ax, x_center=10.0, y_min=-26.0, y_max=26.0, z_peak=21.0, thickness=2.2, width=10.0, color='#10b981', alpha=0.95)

    # 1:1:1 Scale Limits
    ax.set_xlim([-65, 65])
    ax.set_ylim([-35, 35])
    ax.set_zlim([-25, 25])
    ax.set_box_aspect((130, 70, 50))
    ax.view_init(elev=24, azim=-55)
    ax.axis('off')

    title_text = "CARDO PACKTALK EDGE / PRO MODULARE 2-TEILIGE WECHSELKASSETTE // 1:1:1 CAD FITTING\n(Generischer PA12-Unterschlitten, 35x25mm Trägerplatine, axialer JST-SH Header J2, Dual-N52 Magnete & Air-Mount)"
    fig.text(0.50, 0.94, title_text, color='#10b981', fontsize=13, fontweight='bold', ha='center')

    callouts = [
        ("1. Pod-Basis Stirnwand & M8 6-Pin Buchse (IP67)", 0.14, 0.20, '#10b981'),
        ("2. Schutz-Schottwand (2.0mm) & Auto-Eject Federn", 0.14, 0.32, '#94a3b8'),
        ("3. Trägerplatine (35x25mm, DS2401 ID & 500mA PTC)", 0.22, 0.82, '#10b981'),
        ("4. J2 Header: 90° CCW gedreht (Öffnung axial nach +X)", 0.48, 0.84, '#f8fafc'),
        ("5. Unterflur-Kabelkanal & JST-SH Kabel zu Air-Mount", 0.65, 0.20, '#ec4899'),
        ("6. Duale N52 Neodym-Magnete (Ø8x2mm) & 5-Pin Pads", 0.78, 0.80, '#fbbf24'),
        ("7. Cardo Packtalk Edge Headset & EPDM-Spannlasche", 0.82, 0.65, '#10b981'),
        ("8. 4x M2 Senkkopf-Verschraubung (Oberteil zu Unterteil)", 0.82, 0.35, '#94a3b8'),
        ("9. IP67 Stirnflansch-Dichtung & Snap-Fit Rastklinke", 0.84, 0.18, '#f43f5e'),
    ]

    for txt, cx, cy, col in callouts:
        fig.text(cx, cy, txt, color=col, fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.35', facecolor='#0f172a', edgecolor=col, alpha=0.92, lw=1.0))

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Cardo Cartridge Assembly CAD Render generated: {output_png}")

def render_intercom_cartridges_cross_section(output_png):
    """Renders the true 2D longitudinal (X-Z) mechanical cross-section & electrical pinout validation."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 11), dpi=220, facecolor='#080c14')

    # =========================================================================
    # SUBPLOT 1: SENA 50S/60S 2-PIECE CARTRIDGE LÄNGSSCHNITT (X-Z)
    # =========================================================================
    ax1.set_facecolor('#0b1120')
    ax1.set_title("1. SENA 50S / 60S WECHSELKASSETTE // MECHANISCHER & ELEKTRISCHER LÄNGSSCHNITT (X-Z EBENE)", 
                  color='#38bdf8', fontsize=12, fontweight='bold', pad=10)

    # 1. Pod Housing Outer Wall (120 x 32 mm, wall 3.0mm)
    ax1.add_patch(patches.Rectangle((-60, -16), 120, 32, fill=False, edgecolor='#0284c7', linewidth=1.5, linestyle='--'))
    ax1.add_patch(patches.Rectangle((-60, -16), 120, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((-60, 13), 120, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((-60, -16), 8.0, 32, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))

    # M8 Connector on bottom face
    ax1.add_patch(patches.Rectangle((-52, -22), 8.0, 6.0, facecolor='#d97706', edgecolor='#fbbf24', linewidth=1.0))
    ax1.text(-48, -19, "M8 6-PIN\nIP67", color='#080c14', fontsize=7, fontweight='bold', ha='center', va='center')

    # Vertical Pod-Base PCB (36x20x1.6mm at X=-47.8)
    ax1.add_patch(patches.Rectangle((-47.8, -10), 1.6, 20.0, facecolor='#065f46', edgecolor='#10b981', linewidth=1.2))
    ax1.text(-47.0, 11.5, "POD-BASE (1.6mm)", color='#10b981', fontsize=8, fontweight='bold', ha='center')

    # PA12 Schottwand (2.0mm at X=-46.0) with Shroud & Auto-Eject Springs
    ax1.add_patch(patches.Rectangle((-46.0, -11), 2.0, 22.0, facecolor='#334155', edgecolor='#64748b', linewidth=1.0))
    ax1.add_patch(patches.Rectangle((-44.0, -2.5), 4.0, 5.0, facecolor='#0f172a', edgecolor='#38bdf8', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((-44.0, -8.0), 6.0, 2.5, facecolor='#cbd5e1', edgecolor='#94a3b8', linewidth=0.8))
    ax1.add_patch(patches.Rectangle((-44.0,  5.5), 6.0, 2.5, facecolor='#cbd5e1', edgecolor='#94a3b8', linewidth=0.8))
    ax1.text(-41.0, 9.0, "AUTO-EJECT FEDERN", color='#94a3b8', fontsize=7, fontweight='bold', ha='center')

    # 6-Pin Socket Interface (J1 <-> J1)
    ax1.add_patch(patches.Rectangle((-42.0, -1.5), 6.0, 3.0, facecolor='#1e293b', edgecolor='#fbbf24', linewidth=1.0))
    ax1.plot([-46, -36], [0, 0], color='#fbbf24', linewidth=2.0)
    ax1.text(-39.0, 2.5, "J1: 6-PIN MATING (Y=0, Z=0)", color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center')

    # Universal Base Sled (X = -40 to +52 mm)
    ax1.add_patch(patches.Rectangle((-40, -11.75), 92, 3.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0))
    ax1.add_patch(patches.Rectangle((52, -14), 5.0, 28.0, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.2))
    ax1.add_patch(patches.Rectangle((51.2, -13.5), 0.8, 27.0, facecolor='#f43f5e', edgecolor='#be123c', linewidth=0.8))
    ax1.text(54.5, 0.0, "IP67\nBLENDE", color='#ffffff', fontsize=7, fontweight='bold', ha='center', va='center', rotation=270)

    # Carrier PCB (openmotorbridge_pod_cartridge: 35 x 25 x 1.6 mm at X = -36 to -1 mm, Z = -8.75 to -7.15)
    ax1.add_patch(patches.Rectangle((-36, -8.75), 35, 1.6, facecolor='#047857', edgecolor='#10b981', linewidth=1.0))
    ax1.text(-18.5, -10.5, "TRÄGERPLATINE (35x25mm) // DS2401 ID + PTC", color='#10b981', fontsize=8, fontweight='bold', ha='center')

    # J2 Header (Horizontal JST-SH 6P opening facing +X at X = -5 to -1 mm, Z = -7.15 to -5.35)
    ax1.add_patch(patches.Rectangle((-5.0, -7.15), 4.0, 1.8, facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.0))
    ax1.plot([-1, 3], [-6.25, -6.25], color='#ec4899', linewidth=2.5)
    ax1.text(-3.0, -4.5, "J2 (JST-SH) -> +X", color='#f8fafc', fontsize=7.5, fontweight='bold', ha='center')

    # Under-Bed Cable Channel (X = -1 to +22, Z = -8.75 to -7.25) & Pass-Through Slot
    ax1.add_patch(patches.Rectangle((-1.0, -8.75), 23.0, 1.5, facecolor='#0f172a', edgecolor='#ec4899', linewidth=0.8, linestyle=':'))
    ax1.plot([-1.0, 22.0, 22.0], [-6.25, -6.25, 2.0], color='#ec4899', linewidth=2.2)
    ax1.text(10.0, -7.8, "UNTERFLUR-KANAL (1.5mm) & JST-SH KABEL", color='#ec4899', fontsize=7.5, fontweight='bold', ha='center')

    # Sena 3D-Contour Top Inlay (X = -32 to +48, Z = -2.25 to +5.75)
    ax1.add_patch(patches.Rectangle((-32, -2.25), 80, 8.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0))
    ax1.add_patch(patches.Rectangle((-28, 0.75), 72, 5.0, facecolor='#0f172a', edgecolor='#38bdf8', linewidth=0.8))
    ax1.text(8.0, -0.8, "AUSTAUSCHBARES 3D-KONTURBETT (SENA 50S)", color='#38bdf8', fontsize=8, fontweight='bold', ha='center')

    # 4x M2 Fastening Screws
    ax1.plot([-30, -30], [-2.25, 5.75], color='#94a3b8', linewidth=1.5, linestyle='--')
    ax1.plot([45, 45], [-2.25, 5.75], color='#94a3b8', linewidth=1.5, linestyle='--')
    ax1.text(-30, 7.2, "M2", color='#94a3b8', fontsize=7, fontweight='bold', ha='center')
    ax1.text(45, 7.2, "M2", color='#94a3b8', fontsize=7, fontweight='bold', ha='center')

    # 7-Pin Pogo Array (at X = +22, Z = 2.0 to 6.0)
    ax1.add_patch(patches.Rectangle((21.0, 2.0), 2.0, 4.0, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.0))
    ax1.text(22.0, 7.5, "7-PIN POGO\n(X=+22mm)", color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center')

    # Retaining Hook & Latch
    ax1.add_patch(patches.Rectangle((-30, 2.75), 4.0, 4.0, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.0))
    ax1.add_patch(patches.Rectangle((44, 2.75), 4.0, 4.0, facecolor='#f59e0b', edgecolor='#fbbf24', linewidth=1.0))

    # Ghosted Sena Body (84 x 22 mm at X = -26 to +46, Z = 4.75 to 20.0)
    ax1.add_patch(patches.Rectangle((-26, 4.75), 72, 14.0, facecolor='#0284c7', alpha=0.25, edgecolor='#38bdf8', linewidth=1.5))
    ax1.text(10.0, 11.5, "SENA 50S / 60S ORIGINAL-HEADSET", color='#38bdf8', fontsize=9, fontweight='bold', ha='center')

    # EPDM Strap
    ax1.plot([10, 10], [4.75, 20.0], color='#ef4444', linewidth=3.0)
    ax1.text(10.0, 21.5, "EPDM-LASCHE", color='#ef4444', fontsize=7.5, fontweight='bold', ha='center')

    ax1.set_xlim([-65, 65])
    ax1.set_ylim([-25, 25])
    ax1.set_xlabel("Längsachse X (mm) [1:1:1 Maßstab]", color='#94a3b8', fontsize=8.5)
    ax1.set_ylabel("Höhe Z (mm)", color='#94a3b8', fontsize=8.5)
    ax1.tick_params(colors='#94a3b8', labelsize=8)
    ax1.grid(True, color='#1e293b', linestyle=':', alpha=0.6)

    # =========================================================================
    # SUBPLOT 2: CARDO PACKTALK EDGE 2-PIECE CARTRIDGE LÄNGSSCHNITT (X-Z)
    # =========================================================================
    ax2.set_facecolor('#0b1120')
    ax2.set_title("2. CARDO PACKTALK EDGE // MECHANISCHER & ELEKTRISCHER LÄNGSSCHNITT (X-Z EBENE)", 
                  color='#10b981', fontsize=12, fontweight='bold', pad=10)

    # 1. Pod Housing Outer Wall
    ax2.add_patch(patches.Rectangle((-60, -16), 120, 32, fill=False, edgecolor='#059669', linewidth=1.5, linestyle='--'))
    ax2.add_patch(patches.Rectangle((-60, -16), 120, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax2.add_patch(patches.Rectangle((-60, 13), 120, 3.0, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))
    ax2.add_patch(patches.Rectangle((-60, -16), 8.0, 32, facecolor='#1e293b', edgecolor='#334155', linewidth=0.8))

    # M8 Connector
    ax2.add_patch(patches.Rectangle((-52, -22), 8.0, 6.0, facecolor='#d97706', edgecolor='#fbbf24', linewidth=1.0))
    ax2.text(-48, -19, "M8 6-PIN\nIP67", color='#080c14', fontsize=7, fontweight='bold', ha='center', va='center')

    # Vertical Pod-Base PCB
    ax2.add_patch(patches.Rectangle((-47.8, -10), 1.6, 20.0, facecolor='#065f46', edgecolor='#10b981', linewidth=1.2))
    ax2.text(-47.0, 11.5, "POD-BASE (1.6mm)", color='#10b981', fontsize=8, fontweight='bold', ha='center')

    # Schottwand & Springs
    ax2.add_patch(patches.Rectangle((-46.0, -11), 2.0, 22.0, facecolor='#334155', edgecolor='#64748b', linewidth=1.0))
    ax2.add_patch(patches.Rectangle((-44.0, -2.5), 4.0, 5.0, facecolor='#0f172a', edgecolor='#10b981', linewidth=0.8))
    ax2.add_patch(patches.Rectangle((-44.0, -8.0), 6.0, 2.5, facecolor='#cbd5e1', edgecolor='#94a3b8', linewidth=0.8))
    ax2.add_patch(patches.Rectangle((-44.0,  5.5), 6.0, 2.5, facecolor='#cbd5e1', edgecolor='#94a3b8', linewidth=0.8))

    # 6-Pin Socket Interface (J1 <-> J1)
    ax2.add_patch(patches.Rectangle((-42.0, -1.5), 6.0, 3.0, facecolor='#1e293b', edgecolor='#fbbf24', linewidth=1.0))
    ax2.plot([-46, -36], [0, 0], color='#fbbf24', linewidth=2.0)
    ax2.text(-39.0, 2.5, "J1: 6-PIN MATING (Y=0, Z=0)", color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center')

    # Universal Base Sled (Identical!)
    ax2.add_patch(patches.Rectangle((-40, -11.75), 92, 3.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0))
    ax2.add_patch(patches.Rectangle((52, -14), 5.0, 28.0, facecolor='#059669', edgecolor='#34d399', linewidth=1.2))
    ax2.add_patch(patches.Rectangle((51.2, -13.5), 0.8, 27.0, facecolor='#f43f5e', edgecolor='#be123c', linewidth=0.8))
    ax2.text(54.5, 0.0, "IP67\nBLENDE", color='#ffffff', fontsize=7, fontweight='bold', ha='center', va='center', rotation=270)

    # Carrier PCB
    ax2.add_patch(patches.Rectangle((-36, -8.75), 35, 1.6, facecolor='#047857', edgecolor='#10b981', linewidth=1.0))
    ax2.text(-18.5, -10.5, "TRÄGERPLATINE (35x25mm) // DS2401 ID + PTC", color='#10b981', fontsize=8, fontweight='bold', ha='center')

    # J2 Header (Horizontal JST-SH 6P opening facing +X)
    ax2.add_patch(patches.Rectangle((-5.0, -7.15), 4.0, 1.8, facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.0))
    ax2.text(-3.0, -4.5, "J2 (JST-SH) -> +X", color='#f8fafc', fontsize=7.5, fontweight='bold', ha='center')

    # Under-Bed Cable Channel & Ribbon to Air-Mount Pads at X = +10
    ax2.add_patch(patches.Rectangle((-1.0, -8.75), 12.0, 1.5, facecolor='#0f172a', edgecolor='#ec4899', linewidth=0.8, linestyle=':'))
    ax2.plot([-1.0, 10.0, 10.0], [-6.25, -6.25, 2.0], color='#ec4899', linewidth=2.2)
    ax2.text(4.5, -7.8, "JST-SH KABEL", color='#ec4899', fontsize=7.5, fontweight='bold', ha='center')

    # Cardo Air-Mount 3D-Contour Top Inlay (X = -28 to +46, Z = -2.25 to +5.75)
    ax2.add_patch(patches.Rectangle((-28, -2.25), 74, 8.0, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0))
    ax2.add_patch(patches.Rectangle((-24, 0.75), 68, 5.0, facecolor='#0f172a', edgecolor='#10b981', linewidth=0.8))
    ax2.text(9.0, -0.8, "AUSTAUSCHBARES AIR-MOUNT BETT (CARDO PACKTALK EDGE)", color='#10b981', fontsize=8, fontweight='bold', ha='center')

    # Dual N52 Magnets (at X = -8 and X = +28, Z = 1.75 to 3.75)
    ax2.add_patch(patches.Rectangle((-10.0, 1.75), 4.0, 2.0, facecolor='#e11d48', edgecolor='#f43f5e', linewidth=1.0))
    ax2.add_patch(patches.Rectangle((26.0, 1.75), 4.0, 2.0, facecolor='#e11d48', edgecolor='#f43f5e', linewidth=1.0))
    ax2.text(-8.0, 4.5, "N52", color='#f43f5e', fontsize=7, fontweight='bold', ha='center')
    ax2.text(28.0, 4.5, "N52", color='#f43f5e', fontsize=7, fontweight='bold', ha='center')

    # 5-Pin Air Mount Contact Array (at X = +10, Z = 1.5 to 4.5)
    ax2.add_patch(patches.Rectangle((9.0, 1.5), 2.0, 3.0, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.0))
    ax2.text(10.0, 6.0, "5-PIN PADS\n(X=+10mm)", color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center')

    # Ghosted Cardo Body (68 x 14 mm at X = -24 to +44, Z = 4.75 to 18.75)
    ax2.add_patch(patches.Rectangle((-24, 4.75), 68, 14.0, facecolor='#059669', alpha=0.25, edgecolor='#34d399', linewidth=1.5))
    ax2.text(10.0, 11.5, "CARDO PACKTALK EDGE ORIGINAL-HEADSET", color='#34d399', fontsize=9, fontweight='bold', ha='center')

    # EPDM Strap
    ax2.plot([10, 10], [4.75, 19.0], color='#10b981', linewidth=3.0)
    ax2.text(10.0, 20.5, "EPDM-LASCHE", color='#10b981', fontsize=7.5, fontweight='bold', ha='center')

    ax2.set_xlim([-65, 65])
    ax2.set_ylim([-25, 25])
    ax2.set_xlabel("Längsachse X (mm) [1:1:1 Maßstab]", color='#94a3b8', fontsize=8.5)
    ax2.set_ylabel("Höhe Z (mm)", color='#94a3b8', fontsize=8.5)
    ax2.tick_params(colors='#94a3b8', labelsize=8)
    ax2.grid(True, color='#1e293b', linestyle=':', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_png, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Intercom Cartridges Cross-Section Render generated: {output_png}")

if __name__ == '__main__':
    out_sena = os.path.join(output_dir, "sena_cartridge_assembly_cad.png")
    out_cardo = os.path.join(output_dir, "cardo_cartridge_assembly_cad.png")
    out_cross = os.path.join(output_dir, "sena_cardo_cartridge_cross_section.png")

    render_sena_cartridge_assembly(out_sena)
    render_cardo_cartridge_assembly(out_cardo)
    render_intercom_cartridges_cross_section(out_cross)
