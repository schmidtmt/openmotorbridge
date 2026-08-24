#!/usr/bin/env python3
"""
OpenMotorBridge End-Cap Pod & Horizontal Cartridge 3D Mechanical CAD Generator
-----------------------------------------------------------------------------
Generates dimensionally accurate, photorealistic semi-transparent (Ghosted X-Ray)
3D CAD visualizations of the Stirnwand-Adapter (End-Cap Interface) Pod and Cartridge.

Mechanical Architecture (Based on End-Cap Interface Standard):
 +-+---------------------+
 |A+--------------------+|
 |D|                    ||  <-- Voller Bauraum für Wechselkassette / OMM-Platine
M8AP                    ||      (Sena Apex / Cardo DMC / u-blox GNSS + LoRa)
 |P|                    ||
 |T+--------------------+|
 +-+---------------------+
  ▲ ▲
  │ └── 6 vergoldete Mill-Max Pogo-Pins (P) an der inneren Stirnwand
  └──── M8-Stirnwand-Adapterplatine (ADPT) an der linken Gehäusestirnseite

Physical Dimensions:
- Pod Outer Enclosure: 68.0 mm (L) x 44.0 mm (W) x 24.0 mm (H) - Ultra-flat aerodynamic profile
- Left End-Cap Chamber: 12.0 mm (L) x 40.0 mm (W) x 20.0 mm (H)
- Stirnwand Adapter PCB (openmotorbridge_pod_base / ADPT): 36.0 x 20.0 x 1.6 mm
- M8 6-Pin IP67 Panel Receptacle: Centered on left end-wall (X = -34.0 mm)
- Mill-Max 6-Pin Pogo Array: Mounted horizontally on ADPT inner face, pointing +X into cartridge bay
- Shore 40A Silicone Perimeter Seal: Hermetic flange barrier at X = -22.0 mm
- Removable Cartridge (Wechselkassette): 52.0 mm (L) x 36.0 mm (W) x 16.5 mm (H)
- Sena Apex / Cardo OEM Inlay Module: 45.0 x 32.0 x 6.5 mm (Full internal clearance)
- Cartridge Carrier PCB: 35.0 x 25.0 x 1.2 mm with left-edge ENIG gold contact pads
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

def draw_cylinder(ax, x0, y0, z0, radius, length, color, alpha=1.0, resolution=32, axis='x'):
    """Draws a 3D cylinder along specified axis."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    if axis == 'x': # Cylinder along X axis (e.g. horizontal M8 connector or horizontal Pogo pins)
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
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)

def render_xray_assembly(output_png):
    """Renders the Centric Slide-In Pod + Cartridge assembly in semi-transparent X-ray aesthetic."""
    fig = plt.figure(figsize=(20, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Coordinate Setup (mm):
    # Pod Outer Housing: 68.0 mm along X (-34..+34), 44.0 mm along Y (-22..+22), 24.0 mm along Z (-12..+12)
    # Centric Cartridge Bay: 54.0 mm (X = -20 to +34 mm), 38.0 mm (Y = -19 to +19 mm), 18.0 mm (Z = -9 to +9 mm)
    # Wall thickness: Symmetric 3.0 mm top, bottom, left, right

    # 1. TRANSLUCENT OUTER POD HOUSING (PA12 MJF: 68x44x24mm)
    draw_box(ax, -34, -22, -12, 68, 44, 24, color='#38bdf8', alpha=0.14, edgecolor='#0284c7', linewidth=1.0)
    for cy in [-22, 22]:
        for cz in [-12, 12]:
            ax.plot([-34, 34], [cy, cy], [cz, cz], color='#38bdf8', linewidth=1.0, alpha=0.6)

    # 2. ASYMMETRIC POKA-YOKE GUIDE RAILS (Inside Chamber Walls)
    # Left Guide Rail (1.5mm keyway at Y = -19.0 mm)
    draw_box(ax, -20.0, -19.0, -1.0, 52.0, 1.5, 2.0, color='#0284c7', alpha=0.8, edgecolor='#38bdf8', linewidth=0.6)
    # Right Guide Rail (2.0mm keyway at Y = +17.0 mm)
    draw_box(ax, -20.0, 17.5, -1.0, 52.0, 2.0, 2.0, color='#0284c7', alpha=0.8, edgecolor='#38bdf8', linewidth=0.6)

    # 3. POD BASE PCB (openmotorbridge_pod_base: 36x20x1.6mm mounted on inner wall at X = -30.0 mm)
    draw_box(ax, -30.0, -18.0, -10.0, 1.6, 36.0, 20.0, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # Ground plane
    draw_box(ax, -29.9, -17.5, -9.5, 0.05, 35.0, 19.0, color='#eab308', alpha=0.8, edgecolor='#ca8a04', linewidth=0.4)

    # 4. M8 6-PIN IP67 RECEPTACLE (Mounted on outer face of Pod Base PCB at X = -30.0 mm)
    draw_box(ax, -33.5, -6.0, -6.0, 3.5, 12.0, 12.0, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    draw_cylinder(ax, x0=-33.5, y0=0, z0=0, radius=4.0, length=-18.5, color='#64748b', alpha=0.95, axis='x')
    draw_cylinder(ax, x0=-46.0, y0=0, z0=0, radius=4.6, length=-4.0, color='#eab308', alpha=1.0, axis='x')
    draw_cylinder(ax, x0=-44.0, y0=0, z0=0, radius=4.2, length=-1.8, color='#0f172a', alpha=1.0, axis='x')

    # 5. SP3012 TVS ARRAY & DECOUPLING CAP ON POD BASE PCB
    draw_box(ax, -28.4, 8.0, 2.0, 0.9, 3.2, 3.2, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -28.4, 8.5, -4.0, 0.8, 1.6, 0.9, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)

    # 6. HORIZONTAL 6-PIN PIN HEADER (Mating interface at X = -28.4 to -20.0 mm, Centered at Y=0, Z=0)
    draw_box(ax, -28.4, -7.5, -1.25, 2.5, 15.0, 2.5, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pin_y_positions = np.linspace(-6.35, 6.35, 6)
    for py in pin_y_positions:
        # Gold Pins extending horizontally into chamber
        draw_cylinder(ax, x0=-25.9, y0=py, z0=0, radius=0.32, length=6.5, color='#fbbf24', alpha=1.0, axis='x')

    # 7. REMOVABLE WECHSELKASSETTE SLED (52.0 x 36.0 x 16.5 mm, X = -19.5 to +32.5 mm)
    # Translucent smoky purple casing with 45° lead-in chamfer
    draw_box(ax, -19.5, -18.0, -8.25, 52.0, 36.0, 16.5, color='#a855f7', alpha=0.18, edgecolor='#c084fc', linewidth=0.9)

    # 8. HORIZONTAL 6-PIN SOCKET ON CARTRIDGE LEADING EDGE (at X = -19.5 to -13.5 mm, Centered at Y=0, Z=0)
    draw_box(ax, -19.5, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.7)

    # 9. FLAT HORIZONTAL CARTRIDGE PCB (Lying on cassette floor at Z = -6.5 mm, X = -19.0 to +16.0 mm)
    draw_box(ax, -19.0, -12.5, -6.5, 35.0, 25.0, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # 500mA PTC Fuse (F1) & Green Power LED (D1)
    draw_box(ax, -13.0, -5.0, -5.3, 1.6, 0.8, 0.6, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)
    draw_box(ax, -13.0, 5.0, -5.3, 1.6, 0.8, 0.6, color='#22c55e', alpha=1.0, edgecolor='#16a34a', linewidth=0.5)
    # DS2401 ID Chip & JST-SH 6P Header
    draw_box(ax, -8.0, -1.5, -5.3, 3.0, 3.0, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, 6.0, -5.0, -5.3, 3.5, 10.0, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#cbd5e1', linewidth=0.6)

    # 10. SENA APEX / CARDO OEM INTERCOM INLAY (Upper bay volume at Z = -1.0 mm)
    draw_box(ax, -15.0, -16.0, -1.0, 45.0, 32.0, 1.4, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    draw_box(ax, -12.0, -14.0, 0.4, 22.0, 18.0, 4.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 12.0, -14.0, 0.4, 16.0, 14.0, 3.8, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)

    # 11. POSITIVE MECHANICAL STOP & SNAP-LOCK RELEASE SLIDER (Right side at X = +32.5 mm)
    draw_box(ax, 31.0, -8.0, -4.0, 3.5, 16.0, 8.0, color='#e2e8f0', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 33.0, -5.0, -2.5, 2.0, 10.0, 5.0, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)

    # View angle setup (slanted isometric for maximum clarity)
    ax.view_init(elev=24, azim=-52)
    ax.set_xlim([-46, 42])
    ax.set_ylim([-28, 28])
    ax.set_zlim([-18, 18])
    ax.set_axis_off()

    # Title header
    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // CENTRIC POD & FLAT CARTRIDGE ASSEMBLY", 
             color='#38bdf8', fontsize=17, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "3D X-Ray CAD Architecture — 100% Centric Slide-In Bay with Poka-Yoke Rails & Horizontal 6-Pin Mating", 
             color='#94a3b8', fontsize=11.5, ha='center', fontfamily='sans-serif')

    # Technical Details Overlay
    left_card_text = (
        "POD-BASIS: M8-ADAPTER & 6-PIN HEADER\n"
        "─────────────────────────────────────────\n"
        "• M8 6-Pin IP67 Vollmetall-Einbaubuchse\n"
        "• Pod-Base Platine (36 x 20 mm PCB)\n"
        "• Integrierte Littelfuse SP3012 TVS-Matrix\n"
        "• 6-Pin Präzisions-Stiftleiste (Zentrisch)\n"
        "  (Exakt auf Symmetrieachse Y=0, Z=0)\n"
        "• Asymmetrische Poka-Yoke Führungsstege\n"
        "  (Links: 1.5 mm / Rechts: 2.0 mm Nut)"
    )
    fig.text(0.04, 0.48, left_card_text, color='#e2e8f0', fontsize=9.5, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    right_card_text = (
        "WECHSELKASSETTE MIT FLACH-PLATINE (52x36mm)\n"
        "─────────────────────────────────────────\n"
        "• Horizontale 6-Pin Front-Buchsenleiste\n"
        "• 45° Fangtrichter mit ±1.2mm Zentrierung\n"
        "• Formschlüssiger Endanschlag (PA12)\n\n"
        "KASSETTEN-TRÄGERPLATINE (35 x 25 mm PCB):\n"
        "• Liegt flach auf dem Kassettenboden\n"
        "• 500mA PTC-Sicherung & Grüne 5V Power-LED\n"
        "• DS2401 1-Wire ID + 90° JST-SH Flex-Verbinder\n\n"
        "INTEGRIERTES SENA / CARDO / OMM-MODUL:\n"
        "• Voller Bauraum für Headset-Inlay oder OMM"
    )
    fig.text(0.70, 0.48, right_card_text, color='#e2e8f0', fontsize=9.5, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#c084fc', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created Centric Pod 3D X-Ray Assembly Render: {output_png}")

def render_exploded_view(output_png):
    """Renders an Exploded View along the horizontal X-axis (Einschubachse)."""
    fig = plt.figure(figsize=(20, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Exploded offsets along horizontal X-axis (from left to right):
    # 1. M8 Threaded Collar & Nut: X = -72..-56
    # 2. Pod Base PCB (ADPT: 36x20mm): X = -34..-32
    # 3. Horizontal 6-Pin Pin Header: X = -22..-14
    # 4. Silicone Perimeter Gasket: X = -8..-6
    # 5. Removable Cartridge Shell with Poka-Yoke: X = +10..+56
    # 6. Horizontal 6-Pin Socket: X = +10..+16
    # 7. Flat Cartridge Carrier PCB (35x25mm): X = +16..+46 (Z=-6)
    # 8. Sena Apex OEM Inlay Module: X = +18..+54 (Z=+2)

    # 1. M8 Receptacle & Knurled Nut (Floating Left)
    draw_cylinder(ax, x0=-56, y0=0, z0=0, radius=4.0, length=-16.0, color='#64748b', alpha=0.95, axis='x')
    draw_cylinder(ax, x0=-64, y0=0, z0=0, radius=4.6, length=-4.0, color='#eab308', alpha=1.0, axis='x')

    # 2. Pod Base PCB (openmotorbridge_pod_base: 36x20x1.6mm at X = -34 mm)
    draw_box(ax, -34.0, -18.0, -10.0, 1.6, 36.0, 20.0, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    draw_box(ax, -32.4, 8.0, 2.0, 0.9, 3.2, 3.2, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6) # SP3012

    # 3. Horizontal 6-Pin Pin Header (Floating at X = -20 mm, Centered at Y=0, Z=0)
    draw_box(ax, -20.0, -7.5, -1.25, 2.5, 15.0, 2.5, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pin_y_positions = np.linspace(-6.35, 6.35, 6)
    for py in pin_y_positions:
        draw_cylinder(ax, x0=-17.5, y0=py, z0=0, radius=0.32, length=6.0, color='#fbbf24', alpha=1.0, axis='x')

    # 4. Silicone Perimeter Gasket (Shore 40A at X = -8 mm)
    draw_box(ax, -8.0, -18.5, -8.5, 1.5, 37.0, 17.0, color='#06b6d4', alpha=0.75, edgecolor='#0891b2', linewidth=0.9)

    # 5. Removable Cartridge Shell (Wechselkassette with Poka-Yoke at X = +10 mm)
    draw_box(ax, 10.0, -18.0, -8.25, 46.0, 36.0, 16.5, color='#a855f7', alpha=0.25, edgecolor='#c084fc', linewidth=0.9)
    # Horizontal 6-Pin Socket on Cartridge Leading Edge
    draw_box(ax, 10.0, -7.8, -1.5, 6.0, 15.6, 3.0, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.7)

    # 6. Flat Cartridge Carrier PCB (35x25x1.2mm, Lower Floor Layer Z = -5.5 mm)
    draw_box(ax, 14.0, -12.5, -5.5, 35.0, 25.0, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # 500mA PTC Fuse (F1), Power LED (D1), and DS2401 ID Chip
    draw_box(ax, 18.0, -5.0, -4.3, 1.6, 0.8, 0.6, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)
    draw_box(ax, 18.0, 5.0, -4.3, 1.6, 0.8, 0.6, color='#22c55e', alpha=1.0, edgecolor='#16a34a', linewidth=0.5)
    draw_box(ax, 23.0, -1.5, -4.3, 3.0, 3.0, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)

    # 7. Sena Apex / Cardo OEM Inlay Module (45x32x6.5mm, Upper Layer Z = +1.0 mm)
    draw_box(ax, 13.0, -16.0, 1.0, 41.0, 32.0, 1.4, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    draw_box(ax, 16.0, -14.0, 2.4, 20.0, 18.0, 4.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 38.0, -14.0, 2.4, 14.0, 14.0, 3.8, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)

    # Horizontal guide dashed alignment lines
    for corner in [(-18.0, -8.0), (18.0, -8.0), (18.0, 8.0), (-18.0, 8.0)]:
        ax.plot([-60, 56], [corner[0], corner[0]], [corner[1], corner[1]], color='#475569', linestyle='--', linewidth=0.7, alpha=0.6)

    ax.view_init(elev=20, azim=-50)
    ax.set_xlim([-70, 58])
    ax.set_ylim([-26, 26])
    ax.set_zlim([-18, 18])
    ax.set_axis_off()

    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // EXPLODED CENTRIC POD & CARTRIDGE ASSEMBLY", 
             color='#38bdf8', fontsize=17, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "Horizontale Explosionsdarstellung entlang der Kassetten-Einschubachse (X-Achse)", 
             color='#94a3b8', fontsize=11.5, ha='center', fontfamily='sans-serif')

    exploded_legend = (
        "SCHICHT-HIERARCHIE ENTLANG DER EINSCHUBACHSE (X-ACHSE)\n"
        "─────────────────────────────────────────────────────\n"
        "[1] M8-EINBAUBUCHSE MIT ÜBERWURFMUTTER (Links)\n"
        "    • M8 6-Pin IP67 A-Coded mit Rüttelsicherung\n\n"
        "[2] POD-BASE PLATINE (36 x 20 mm PCB)\n"
        "    • Direkt aufgelötete M8-Buchse & Littelfuse TVS\n\n"
        "[3] 6-PIN PRÄZISIONS-STIFTLEISTE (ZENTRISCH)\n"
        "    • Horizontale Goldkontakte (Y=0, Z=0)\n\n"
        "[4] SHORE 40A SILIKON-STIRNFLANSCHDICHTUNG\n"
        "    • Hermetische Barriere gegen Feuchtigkeit & Staub\n\n"
        "[5] WECHSELKASSETTE MIT POKA-YOKE (52x36mm)\n"
        "    • Asymmetrische Führungsnuten (1.5mm / 2.0mm)\n\n"
        "[6] 6-PIN FRONT-BUCHSENLEISTE (ZENTRISCH)\n"
        "    • 45° Fangtrichter zur exakten Selbstzentrierung\n\n"
        "[7] KASSETTEN-TRÄGERPLATINE (35 x 25 mm PCB)\n"
        "    • Liegt flach am Boden: PTC, LED, DS2401, JST-SH\n\n"
        "[8] SENA / CARDO / OMM MODUL-BAURAUM (45 x 32 mm)\n"
        "    • Voller Bauraum ohne störenden Doppelboden"
    )
    fig.text(0.04, 0.46, exploded_legend, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created Centric Pod 3D Exploded View Render: {output_png}")

def export_vrml_assembly(output_wrl):
    """Exports the End-Cap Stirnwand Pod Assembly in VRML 2.0 format."""
    wrl_content = """#VRML V2.0 utf8
# OpenMotorBridge Stirnwand-Adapter (End-Cap) Pod & Cartridge 3D Mechanical Assembly
# Generated by OpenMotorBridge CAD Engine

Group {
  children [
    # 1. Translucent Outer Pod Enclosure (68x44x24mm, Makrolon Polycarbonate)
    Transform {
      translation 0.0 0.0 0.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.22 0.74 0.97
              specularColor 0.8 0.8 0.8
              transparency 0.78
              shininess 0.9
            }
          }
          geometry Box { size 0.068 0.044 0.024 }
        }
      ]
    }

    # 2. Translucent Removable Cartridge Shell (52x36x16.5mm, Polycarbonate)
    Transform {
      translation 0.0065 0.0 0.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.65 0.33 0.96
              specularColor 0.7 0.7 0.7
              transparency 0.72
              shininess 0.8
            }
          }
          geometry Box { size 0.052 0.036 0.0165 }
        }
      ]
    }

    # 3. Stirnwand Adapter PCB (openmotorbridge_pod_base / ADPT: 36x20x1.6mm vertical)
    Transform {
      translation -0.030 0.0 0.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.58 0.41
              specularColor 0.3 0.3 0.3
              shininess 0.4
            }
          }
          geometry Box { size 0.0016 0.036 0.020 }
        }
      ]
    }

    # 4. Sena Apex / Cardo OEM Inlay Module (45x32x6.5mm)
    Transform {
      translation 0.0075 0.0 0.001
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.37 0.27
              specularColor 0.3 0.3 0.3
              shininess 0.4
            }
          }
          geometry Box { size 0.045 0.032 0.0016 }
        }
      ]
    }

    # 5. Cartridge Carrier PCB (35x25x1.2mm, openmotorbridge_pod_cartridge)
    Transform {
      translation -0.0015 0.0 -0.0055
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.47 0.34
              specularColor 0.3 0.3 0.3
              shininess 0.4
            }
          }
          geometry Box { size 0.035 0.025 0.0012 }
        }
      ]
    }

    # 6. M8 Metal Panel Receptacle on Left Stirnwand
    Transform {
      translation -0.0425 0.0 0.0
      rotation 0.0 0.0 1.0 1.5708
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.75 0.75 0.78
              specularColor 0.9 0.9 0.9
              shininess 0.8
            }
          }
          geometry Cylinder {
            radius 0.004
            height 0.019
          }
        }
      ]
    }

    # 7. Silicone Perimeter Flange Gasket (Shore 40A Boot, 37x17x1.2mm)
    Transform {
      translation -0.0205 0.0 0.0
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.71 0.83
              transparency 0.4
              shininess 0.2
            }
          }
          geometry Box { size 0.0012 0.037 0.017 }
        }
      ]
    }
  ]
}
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_wrl)), exist_ok=True)
    with open(output_wrl, 'w', encoding='utf-8') as f:
        f.write(wrl_content)
    print(f"✓ Exported Stirnwand-Adapter 3D VRML Assembly Model: {output_wrl}")

if __name__ == '__main__':
    xray_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly_render_xray.png'))
    exploded_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_exploded_view.png'))
    vrml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly.wrl'))
    render_xray_assembly(xray_path)
    render_exploded_view(exploded_path)
    export_vrml_assembly(vrml_path)
