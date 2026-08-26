#!/usr/bin/env python3
"""
OpenMotorBridge Pod 3 Full Virtual 3D Assembly CAD Generator (True 90° Stirnwand Architecture)
---------------------------------------------------------------------------------------------
Accurate 3D CAD visualization based on the official End-Cap Stirnwand Interface Standard:
 1. Vertical Stirnwand Adapter PCB (openmotorbridge_pod_base: 36.0 x 20.0 mm in Y-Z plane at X = -28 mm)
    - M8 6-Pin IP67 Receptacle mounted horizontally pointing -X through the end-wall
    - 6-Pin Precision Header mounted horizontally pointing +X into the cartridge bay
 2. Horizontal Sensor PCB (openmotorbridge_rear_pod3: 48.0 x 32.0 mm in X-Y plane at Z = 0 mm)
    - Leading edge 6-Pin Socket mating horizontally at 90° to the Stirnwand
    - ESP32-S3, IMU, ToF Distance Radar & High-Power Brake LEDs at the rear optical window (+X)
 3. Removable Cartridge Tray (Wechselkassette) sliding horizontally into Monocoque Pod Housing
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
    """Draws a 3D rectangular solid or semi-transparent volume."""
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

def render_true_90deg_mated_assembly(output_png):
    """Renders the true 90° Stirnwand-to-Cartridge Mated 3D View."""
    fig = plt.figure(figsize=(16, 10), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # =========================================================================
    # 1. VERTICAL STIRNWAND ADAPTER PCB (openmotorbridge_pod_base)
    # Position: Y-Z plane at X = -28.0 mm (Thickness: 1.6 mm, from X = -29.6 to -28.0 mm)
    # Dimensions: 36.0 mm wide (Y: -18 to +18) x 20.0 mm high (Z: -10 to +10)
    # =========================================================================
    draw_box(ax, -29.6, -18.0, -10.0, 1.6, 36.0, 20.0, color='#065f46', alpha=0.95, edgecolor='#10b981', linewidth=1.2)
    
    # 2x M2 Mounting Holes at Y = +/-15 mm, Z = 0
    draw_cylinder(ax, -30.0, -15.0, 0.0, 1.1, 2.2, color='#1e293b', alpha=1.0, axis='x')
    draw_cylinder(ax, -30.0,  15.0, 0.0, 1.1, 2.2, color='#1e293b', alpha=1.0, axis='x')
    draw_cylinder(ax, -28.05, -15.0, 0.0, 1.7, 0.1, color='#fbbf24', alpha=0.9, axis='x')
    draw_cylinder(ax, -28.05,  15.0, 0.0, 1.7, 0.1, color='#fbbf24', alpha=0.9, axis='x')

    # TVS Protection Array (SP3012) & C1 on Inner Face (F.Cu at X = -28.0 mm)
    draw_box(ax, -28.0, -10.0, -4.0, 0.6, 1.35, 3.5, color='#1e293b', alpha=0.95, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -28.0, -10.0,  4.0, 0.8, 1.6, 0.8, color='#b45309', alpha=0.95, edgecolor='#d97706', linewidth=0.6)

    # =========================================================================
    # 2. HORIZONTAL M8 6-PIN IP67 RECEPTACLE (Mounted on B.Cu, pointing -X outwards)
    # =========================================================================
    draw_cylinder(ax, -42.0, 0.0, 0.0, 4.0, 12.4, color='#d97706', alpha=0.90, axis='x')
    draw_cylinder(ax, -42.0, 0.0, 0.0, 3.2, 1.0, color='#0f172a', alpha=0.95, axis='x') # Inner core
    draw_cylinder(ax, -33.0, 0.0, 0.0, 5.0, 2.5, color='#b45309', alpha=0.95, axis='x') # Flange Nut
    for ang in np.linspace(0, 2*np.pi, 6, endpoint=False):
        py = 1.8 * np.cos(ang)
        pz = 1.8 * np.sin(ang)
        draw_cylinder(ax, -41.5, py, pz, 0.35, 4.0, color='#fbbf24', alpha=1.0, axis='x')

    # =========================================================================
    # 3. 90-DEGREE 6-PIN MATING INTERFACE (X = -28.0 to -20.0 mm)
    # J1 Header Base on Stirnwand PCB (X = -28.0 to -25.5 mm)
    # =========================================================================
    draw_box(ax, -28.0, -7.62, -1.27, 2.5, 15.24, 2.54, color='#0f172a', alpha=0.95, edgecolor='#334155', linewidth=0.8)
    
    # 6 Horizontal Gold Mating Pins (pointing +X into cartridge bay, X = -28.0 to -20.0 mm)
    y_pins = np.linspace(-6.35, 6.35, 6)
    for yp in y_pins:
        draw_cylinder(ax, -28.0, yp, 0.0, 0.32, 8.0, color='#fbbf24', alpha=1.0, axis='x')

    # 6-Pin Right-Angle / Horizontal Socket on Cartridge PCB (X = -26.0 to -20.0 mm)
    draw_box(ax, -26.0, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.90, edgecolor='#0284c7', linewidth=1.0)

    # =========================================================================
    # 4. HORIZONTAL REAR POD 3 SENSOR PCB (openmotorbridge_rear_pod3)
    # Position: X-Y plane at Z = 0.0 mm (Thickness: 1.6 mm, from Z = -0.8 to +0.8 mm)
    # Dimensions: 48.0 mm long (X: -20.0 to +28.0) x 32.0 mm wide (Y: -16.0 to +16.0)
    # =========================================================================
    draw_box(ax, -20.0, -16.0, -0.8, 48.0, 32.0, 1.6, color='#047857', alpha=0.90, edgecolor='#34d399', linewidth=1.5)
    
    # Gold ENIG mounting pads
    for cx in [-17.0, 25.0]:
        for cy in [-13.0, 13.0]:
            draw_cylinder(ax, cx, cy, -0.9, 1.5, 1.8, color='#fbbf24', alpha=0.9, axis='z')
            draw_cylinder(ax, cx, cy, -1.0, 1.0, 2.0, color='#0f172a', alpha=1.0, axis='z')

    # ESP32-S3 Module (U1) on Top of Pod 3 PCB (Z = +0.8 to +4.0 mm)
    draw_box(ax, -16.0, -12.75, 0.8, 18.0, 25.5, 2.8, color='#94a3b8', alpha=0.92, edgecolor='#cbd5e1', linewidth=1.0)
    draw_box(ax, 2.0, -12.75, 0.8, 5.0, 25.5, 0.8, color='#022c22', alpha=0.95, edgecolor='#059669', linewidth=0.8)
    for my in np.linspace(-11.0, 11.0, 8):
        draw_box(ax, 2.5, my, 1.6, 4.0, 0.6, 0.05, color='#fbbf24', alpha=1.0)

    # LSM6DSOX 6-Axis IMU (U2)
    draw_box(ax, 10.0, -8.0, 0.8, 2.5, 3.0, 0.86, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=0.8)

    # VL53L4CD Time-of-Flight Radar / Distance Sensor (U3: facing rear +X)
    draw_box(ax, 20.0, -1.2, 0.8, 4.4, 2.4, 1.0, color='#18181b', alpha=0.95, edgecolor='#f43f5e', linewidth=1.0)
    draw_cylinder(ax, 24.4, -0.5, 1.3, 0.5, 1.2, color='#38bdf8', alpha=0.9, axis='x')
    draw_cylinder(ax, 24.4,  0.5, 1.3, 0.6, 1.2, color='#38bdf8', alpha=0.9, axis='x')

    # WS2812B RGB Status LED (D1)
    draw_box(ax, 10.0, 6.0, 0.8, 2.0, 2.0, 0.7, color='#ffffff', alpha=0.95, edgecolor='#a855f7', linewidth=0.8)
    draw_cylinder(ax, 11.0, 7.0, 1.5, 0.6, 0.1, color='#22c55e', alpha=1.0, axis='z')

    # High-Power Brake Light LED Array (D2: 4x Red LEDs along rear +X edge)
    for by in np.linspace(-10.0, 10.0, 4):
        draw_box(ax, 25.0, by-1.0, 0.8, 2.0, 2.0, 0.8, color='#ef4444', alpha=0.95, edgecolor='#f87171', linewidth=0.8)
        draw_cylinder(ax, 27.0, by, 1.2, 0.6, 1.2, color='#ff0000', alpha=0.85, axis='x')

    # =========================================================================
    # 5. TRANSLUCENT WECHSELKASSETTE TRAY (PA12: 52.0 x 36.0 x 14.0 mm)
    # =========================================================================
    draw_box(ax, -22.0, -18.0, -6.0, 52.0, 36.0, 12.0, color='#3b82f6', alpha=0.10, edgecolor='#60a5fa', linewidth=0.9)
    draw_box(ax, 29.8, -13.0, -4.0, 0.8, 26.0, 8.0, color='#e0f2fe', alpha=0.35, edgecolor='#38bdf8', linewidth=1.2)

    # =========================================================================
    # 6. TRANSLUCENT OUTER MONOCOQUE POD HOUSING (PA12: 68.0 x 44.0 x 24.0 mm)
    # =========================================================================
    draw_box(ax, -34.0, -22.0, -12.0, 68.0, 44.0, 24.0, color='#0284c7', alpha=0.06, edgecolor='#0369a1', linewidth=1.0)
    draw_box(ax, -34.0, -22.0, -12.0, 4.0, 44.0, 24.0, color='#0369a1', alpha=0.15, edgecolor='#0284c7', linewidth=1.2)

    # =========================================================================
    # 7. PRECISE ANNOTATIONS & CALLOUTS
    # =========================================================================
    callouts = [
        ("1. M8 6-Pin IP67 Buchse\n[Horizontaler Kabelabgang]", (-42, 0, 0), (-45, -24, 7)),
        ("2. Vertikale Stirnwand-Basis (36x20mm)\n[Steht senkrecht im Y-Z-Schnitt]", (-28.8, -18, 0), (-32, -30, -7)),
        ("3. 90°-Steckverbindung (J1)\n[Horizontale Kontakt-Übergabe]", (-24, 7.6, 0), (-16, 26, 12)),
        ("4. Horizontale Pod 3 Platine (48x32mm)\n[Liegt waagerecht im X-Y-Schnitt]", (4, -16, 0), (10, -28, -9)),
        ("ESP32-S3 MCU (240MHz)\n[Auf Oberseite F.Cu]", (-7, 0, 3.6), (-10, 24, 18)),
        ("ToF-Radar & Brems-LEDs\n[Blicken nach hinten +X]", (27, 0, 1.2), (32, 22, 10)),
        ("Wechselkassette (PA12 Schlitten)\n[Schiebt horizontal nach -X ein]", (10, 18, 0), (20, 28, -6)),
    ]

    for label, target, pos in callouts:
        ax.text(pos[0], pos[1], pos[2], label, color='#38bdf8', fontsize=8.5,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#0b1329', edgecolor='#0284c7', alpha=0.92, lw=0.9),
                ha='center', va='center', weight='bold')
        ax.plot([target[0], pos[0]], [target[1], pos[1]], [target[2], pos[2]], color='#38bdf8', linestyle='--', linewidth=1.0, alpha=0.75)

    # Titles & Badges
    fig.text(0.5, 0.96, "OPENMOTORBRIDGE // REAR POD 3 ECHTE 90° STIRNWAND-MONTAGE",
             ha='center', va='top', fontsize=16, color='#f8fafc', weight='heavy', family='sans-serif')
    fig.text(0.5, 0.925, "Vertikale Stirnwand-Basis (Y-Z-Ebene)  ◄►  Horizontale Wechselkassette (X-Y-Ebene)",
             ha='center', va='top', fontsize=11, color='#38bdf8', weight='bold', family='sans-serif')

    specs = (
        "ARCHITEKTUR & FIT-PARAMETER:\n"
        "• Stirnwand-Platine: 36 x 20 mm (Vertikal im Y-Z-Schnitt)\n"
        "• Kassetten-Platine: 48 x 32 mm (Horizontal im X-Y-Schnitt)\n"
        "• Fügerichtung: Horizontal (+X nach -X, rechtwinklig zur Stirnwand)\n"
        "• Sensor-Blickrichtung: Horizontal nach hinten (+X durch Heckfenster)\n"
        "• M8-Kabelabgang: Horizontal nach vorne/außen (-X durch Stirnwand)"
    )
    fig.text(0.03, 0.05, specs, fontsize=8.5, color='#94a3b8', family='monospace',
             bbox=dict(boxstyle='square,pad=0.6', facecolor='#090d16', edgecolor='#1e293b', alpha=0.95, lw=1.0))

    ax.set_xlim(-46, 38)
    ax.set_ylim(-30, 30)
    ax.set_zlim(-16, 18)
    ax.set_axis_off()
    ax.view_init(elev=24, azim=-55)

    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Saved True 90° Mated 3D Assembly CAD render to {output_png}")

def render_true_90deg_exploded_assembly(output_png):
    """Renders the true horizontal exploded sequence showing how the module slides together."""
    fig = plt.figure(figsize=(18, 10), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # 1. M8 6-Pin IP67 Receptacle (X = -56 mm)
    draw_cylinder(ax, -64.0, 0.0, 0.0, 4.0, 12.0, color='#d97706', alpha=0.9, axis='x')
    draw_cylinder(ax, -52.0, 0.0, 0.0, 5.0, 2.5, color='#b45309', alpha=0.95, axis='x')

    # 2. Bulkhead Wall with M8 Port (X = -44 mm)
    draw_box(ax, -46.0, -22.0, -12.0, 4.0, 44.0, 24.0, color='#0284c7', alpha=0.20, edgecolor='#0369a1', linewidth=1.2)
    draw_cylinder(ax, -48.0, 0.0, 0.0, 5.5, 8.0, color='#1e293b', alpha=0.8, axis='x')

    # 3. Vertikale Stirnwand Base PCB (X = -28 mm)
    draw_box(ax, -29.6, -18.0, -10.0, 1.6, 36.0, 20.0, color='#065f46', alpha=0.92, edgecolor='#10b981', linewidth=1.2)
    draw_cylinder(ax, -30.0, -15.0, 0.0, 1.1, 2.2, color='#1e293b', alpha=1.0, axis='x')
    draw_cylinder(ax, -30.0,  15.0, 0.0, 1.1, 2.2, color='#1e293b', alpha=1.0, axis='x')
    draw_box(ax, -28.0, -10.0, -4.0, 0.6, 1.35, 3.5, color='#1e293b', alpha=0.95, edgecolor='#475569', linewidth=0.6)

    # 4. 6-Pin Horizontal Pin Header (X = -14 mm)
    draw_box(ax, -16.5, -7.62, -1.27, 2.5, 15.24, 2.54, color='#0f172a', alpha=0.95, edgecolor='#334155', linewidth=0.8)
    for yp in np.linspace(-6.35, 6.35, 6):
        draw_cylinder(ax, -16.5, yp, 0.0, 0.32, 8.0, color='#fbbf24', alpha=1.0, axis='x')

    # 5. Horizontale Pod 3 Sensor PCB (X = +12 mm)
    draw_box(ax, -12.0, -16.0, -0.8, 48.0, 32.0, 1.6, color='#047857', alpha=0.88, edgecolor='#34d399', linewidth=1.5)
    draw_box(ax, -12.0, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.95, edgecolor='#0284c7', linewidth=1.0)
    draw_box(ax, -8.0, -12.75, 0.8, 18.0, 25.5, 2.8, color='#94a3b8', alpha=0.92, edgecolor='#cbd5e1', linewidth=1.0)
    draw_box(ax, 28.0, -1.2, 0.8, 4.4, 2.4, 1.0, color='#18181b', alpha=0.95, edgecolor='#f43f5e', linewidth=1.0)
    for by in np.linspace(-10.0, 10.0, 4):
        draw_box(ax, 33.0, by-1.0, 0.8, 2.0, 2.0, 0.8, color='#ef4444', alpha=0.95, edgecolor='#f87171', linewidth=0.8)

    # 6. Wechselkassette Tray (X = +40 mm)
    draw_box(ax, 36.0, -18.0, -6.0, 30.0, 36.0, 12.0, color='#38bdf8', alpha=0.15, edgecolor='#60a5fa', linewidth=1.0)

    # 7. Optical Rear End-Cap Window (X = +62 mm)
    draw_box(ax, 68.0, -14.0, -5.0, 2.0, 28.0, 10.0, color='#e0f2fe', alpha=0.45, edgecolor='#38bdf8', linewidth=1.5)

    # Horizontal Assembly Guide Axis
    for gy in [-15.0, 0.0, 15.0]:
        ax.plot([-68, 72], [gy, gy], [0, 0], color='#38bdf8', linestyle=':', linewidth=1.2, alpha=0.5)

    # Callouts
    exploded_notes = [
        ("1. M8 6-Pin IP67 Stecker", (-56, 0, 0), (-58, -24, 11)),
        ("2. Stirnwand-Flansch (Gehäuse)", (-44, 0, 0), (-46, 24, 13)),
        ("3. Vertikale Stirnwand-Basis (36x20mm)\n[Dual-SMD mit TVS-Matrix]", (-28, 0, 0), (-28, -26, -13)),
        ("4. 6-Pol Präzisions-Stiftleiste (J1)\n[Horizontale Steckverbindung]", (-14, 0, 0), (-14, 26, 13)),
        ("5. Horizontale Pod 3 Platine (48x32mm)\n[ESP32-S3 + ToF + IMU + Brems-LEDs]", (12, 0, 0), (12, -26, -13)),
        ("6. Wechselkassette (PA12 Schlitten)", (50, 0, 0), (46, 26, 13)),
        ("7. Heck-Optikfenster (Polycarbonat)", (70, 0, 0), (66, -22, 11)),
    ]

    for label, target, pos in exploded_notes:
        ax.text(pos[0], pos[1], pos[2], label, color='#38bdf8', fontsize=8.5,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#0b1329', edgecolor='#0284c7', alpha=0.92, lw=0.9),
                ha='center', va='center', weight='bold')
        ax.plot([target[0], pos[0]], [target[1], pos[1]], [target[2], pos[2]], color='#38bdf8', linestyle='--', linewidth=1.0, alpha=0.75)

    fig.text(0.5, 0.96, "OPENMOTORBRIDGE // REAR POD 3 HORIZONTALE EXPLOSIONSDARSTELLUNG",
             ha='center', va='top', fontsize=16, color='#f8fafc', weight='heavy', family='sans-serif')
    fig.text(0.5, 0.925, "Rechtwinklige 90°-Fügung: Vertikale Stirnwand-Basis  ◄►  Horizontaler Kassetteneinschub",
             ha='center', va='top', fontsize=11, color='#38bdf8', weight='bold', family='sans-serif')

    ax.set_xlim(-70, 75)
    ax.set_ylim(-34, 34)
    ax.set_zlim(-20, 20)
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-60)

    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Saved True 90° Exploded 3D Assembly CAD render to {output_png}")

def render_true_90deg_cross_section_view(output_png):
    """Renders the true 90° 2D/3D X-Z side cross-section view showing horizontal slide-in."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=220, facecolor='#080c14')
    ax.set_facecolor('#080c14')

    # Grid & Axes
    ax.grid(True, linestyle='--', alpha=0.15, color='#38bdf8')
    ax.set_axisbelow(True)

    # 1. Outer Enclosure (PA12 Bulkhead + Body)
    # Total Length: X = -34.0 to +34.0 (68 mm), Height: Z = -12.0 to +12.0 (24 mm)
    # Bulkhead Wall (Left End-Wall): X = -34.0 to -30.0 mm
    ax.add_patch(patches.Rectangle((-34.0, -12.0), 4.0, 24.0, facecolor='#0369a1', alpha=0.35, edgecolor='#0284c7', linewidth=1.5, label='Monocoque-Gehäuse (MJF PA12)'))
    # Enclosure Roof & Floor
    ax.add_patch(patches.Rectangle((-30.0, 9.0), 64.0, 3.0, facecolor='#0369a1', alpha=0.25, edgecolor='#0284c7', linewidth=1.2))
    ax.add_patch(patches.Rectangle((-30.0, -12.0), 64.0, 3.0, facecolor='#0369a1', alpha=0.25, edgecolor='#0284c7', linewidth=1.2))

    # 2. M8 6-Pin IP67 Receptacle (Horizontal at X = -44.0 to -29.6 mm, Z = -4.0 to +4.0 mm)
    ax.add_patch(patches.Rectangle((-44.0, -4.0), 14.4, 8.0, facecolor='#d97706', alpha=0.85, edgecolor='#fbbf24', linewidth=1.2, label='M8 6-Pol IP67 Buchse (Horizontal)'))
    ax.add_patch(patches.Rectangle((-33.0, -5.0), 2.5, 10.0, facecolor='#b45309', alpha=0.95, edgecolor='#d97706', linewidth=1.0))

    # 3. Vertikale Stirnwand-Adapterplatine (openmotorbridge_pod_base: X = -29.6 to -28.0 mm, Z = -10.0 to +10.0 mm)
    ax.add_patch(patches.Rectangle((-29.6, -10.0), 1.6, 20.0, facecolor='#065f46', alpha=0.95, edgecolor='#10b981', linewidth=1.5, label='Pod-Base-Platine (36x20 mm, Vertikal)'))
    # TVS Array on Inner Face
    ax.add_patch(patches.Rectangle((-28.0, -3.5), 0.6, 7.0, facecolor='#1e293b', alpha=0.95, edgecolor='#475569', linewidth=0.8))

    # 4. 6-Pin Horizontal Mating Header (X = -28.0 to -20.0 mm, Z = -1.27 to +1.27 mm)
    ax.add_patch(patches.Rectangle((-28.0, -1.27), 2.5, 2.54, facecolor='#0f172a', alpha=0.95, edgecolor='#334155', linewidth=0.8, label='SMD-Stiftleiste J1 (Horizontal)'))
    ax.add_patch(patches.Rectangle((-25.5, -0.32), 5.5, 0.64, facecolor='#fbbf24', alpha=1.0, edgecolor='#d97706', linewidth=0.5, label='6x Vergoldete Stifte (Fügezone)'))

    # 5. Right-Angle / Horizontal Socket on Cartridge PCB (X = -25.0 to -20.0 mm, Z = -1.5 to +1.5 mm)
    ax.add_patch(patches.Rectangle((-25.0, -1.5), 5.0, 3.0, facecolor='#1e293b', alpha=0.88, edgecolor='#0284c7', linewidth=1.0, label='Kassetten-Buchsenleiste (90°-Winkel)'))

    # 6. Horizontale Pod 3 Sensor-Platine (openmotorbridge_rear_pod3: X = -20.0 to +28.0 mm, Z = -0.8 to +0.8 mm)
    ax.add_patch(patches.Rectangle((-20.0, -0.8), 48.0, 1.6, facecolor='#047857', alpha=0.92, edgecolor='#34d399', linewidth=1.5, label='Rear Pod 3 Platine (48x32 mm, Horizontal)'))

    # 7. ESP32-S3 Module on Top of Pod 3 (X = -16.0 to +2.0 mm, Z = +0.8 to +4.0 mm)
    ax.add_patch(patches.Rectangle((-16.0, 0.8), 18.0, 3.2, facecolor='#94a3b8', alpha=0.95, edgecolor='#cbd5e1', linewidth=1.0, label='ESP32-S3 WROOM Modul (3.2 mm)'))

    # 8. ToF Radar Sensor (X = 20.0 to 24.4 mm, Z = +0.8 to +2.0 mm)
    ax.add_patch(patches.Rectangle((20.0, 0.8), 4.4, 1.2, facecolor='#18181b', alpha=0.95, edgecolor='#f43f5e', linewidth=1.0, label='VL53L4CD ToF-Sensor & Brems-LEDs'))
    # Brake LEDs (X = 25.0 to 27.0 mm, Z = +0.8 to +2.0 mm)
    ax.add_patch(patches.Rectangle((25.0, 0.8), 2.0, 1.2, facecolor='#ef4444', alpha=0.95, edgecolor='#f87171', linewidth=1.0))

    # 9. Optical Window at Rear End-Cap (X = +33.0 to +34.0 mm, Z = -5.0 to +5.0 mm)
    ax.add_patch(patches.Rectangle((33.0, -5.0), 1.0, 10.0, facecolor='#e0f2fe', alpha=0.55, edgecolor='#38bdf8', linewidth=1.2, label='Optisches Polycarbonat-Fenster'))

    # 10. Wechselkassette Tray Outline (Dashed blue line)
    ax.add_patch(patches.Rectangle((-22.0, -6.0), 54.0, 12.0, fill=False, edgecolor='#60a5fa', linestyle='--', linewidth=1.2, label='Wechselkassette (PA12 Schlitten)'))

    # Clearances & Dimensions
    # Arrow for insertion direction
    ax.annotate('', xy=(-22, -8), xytext=(15, -8),
                arrowprops=dict(arrowstyle="->", color="#38bdf8", lw=2.0))
    ax.text(-3.5, -9.5, "Einschub-Richtung (+X nach -X)", color="#38bdf8", fontsize=10, weight='bold', ha='center')

    # Dimension Arrow for Pod Height
    ax.annotate('', xy=(38, -12), xytext=(38, 12),
                arrowprops=dict(arrowstyle="<->", color="#f8fafc", lw=1.5))
    ax.text(40, 0, "Gehäusehöhe: 24.0 mm", color="#f8fafc", fontsize=9.5, rotation=90, va='center')

    # Dimension Arrow for Air Gap above ESP32
    ax.annotate('', xy=(-7, 4.0), xytext=(-7, 9.0),
                arrowprops=dict(arrowstyle="<->", color="#38bdf8", lw=1.2))
    ax.text(-7, 6.5, " 5.0 mm Luftspalt", color="#38bdf8", fontsize=9, va='center')

    ax.set_title("OPENMOTORBRIDGE // REAR POD 3 SEITEN-SCHNITTANSICHT (X-Z EBENE)", fontsize=15, color='#f8fafc', weight='heavy', pad=15)
    ax.set_xlabel("X-Position entlang Modul [mm] (Horizontaler Einschub)", fontsize=11, color='#94a3b8')
    ax.set_ylabel("Z-Position [mm] (Vertikale Modulhöhe)", fontsize=11, color='#94a3b8')
    ax.tick_params(colors='#64748b', labelsize=9)

    ax.set_xlim(-50, 48)
    ax.set_ylim(-16, 16)

    # Legend
    legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, framealpha=0.95, facecolor='#0b1329', edgecolor='#1e293b', fontsize=8.5)
    for text in legend.get_texts():
        text.set_color('#cbd5e1')

    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Saved True 90° Side Cross-Section CAD render to {output_png}")

if __name__ == '__main__':
    mated_out = os.path.join(output_dir, "pod3_assembly_mated_closeup.png")
    exploded_out = os.path.join(output_dir, "pod3_full_assembly_exploded_3d.png")
    section_out = os.path.join(output_dir, "pod3_assembly_cross_section.png")
    render_true_90deg_mated_assembly(mated_out)
    render_true_90deg_exploded_assembly(exploded_out)
    render_true_90deg_cross_section_view(section_out)
