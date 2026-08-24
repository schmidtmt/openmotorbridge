#!/usr/bin/env python3
"""
OpenMotorBridge Pod & Cartridge Mechanical 3D CAD Generator & Premium X-Ray Renderer
-----------------------------------------------------------------------------------
Generates photorealistic, dimensionally accurate semi-transparent (ghosted X-Ray) 3D CAD
visualizations of the Universal Satellite Pod Enclosure and Removable Intercom Cartridge.

Accurate Mechanical Dimensions:
- Universal Pod Outer Enclosure: 68.0 x 48.0 x 34.0 mm (Schacht: 64.0 x 46.0 x 23.5 mm)
- Removable Cartridge (Wechselkassette): 54.0 x 37.5 x 17.0 mm (PA12 MJF / Polycarbonate)
- Sena Apex / Cardo OEM Intercom Board: 45.0 x 32.0 x 6.5 mm (RF cans, Dual Mesh Chipsets)
- Cartridge Carrier PCB (openmotorbridge_pod_cartridge): 35.0 x 25.0 x 1.2 mm (JST-SH 6P + DS2401 ID)
- Pod Base PCB (openmotorbridge_pod_base): 28.0 x 28.0 x 1.6 mm (M8 IP67 socket + SP3012 TVS)
- Mill-Max 6-Pin Pogo-Pin Array (Series 824, 2.54mm pitch, 1.4mm stroke)
- Shore 40A Silicone Perimeter Boot Gasket (IP67 sealing)
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

def draw_cylinder(ax, x_c, y_c, z0, radius, height, color, alpha=1.0, resolution=32, axis='z'):
    """Draws a 3D cylinder along specified axis."""
    theta = np.linspace(0, 2 * np.pi, resolution)
    if axis == 'z':
        z = np.linspace(z0, z0 + height, 2)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = x_c + radius * np.cos(theta_grid)
        y_grid = y_c + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)
    elif axis == 'y': # Cylinder protruding along Y axis (e.g. M8 connector)
        y = np.linspace(y0 := y_c, y0 + height, 2)
        theta_grid, y_grid = np.meshgrid(theta, y)
        x_grid = x_c + radius * np.cos(theta_grid)
        z_grid = z0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)

def render_xray_assembly(output_png):
    """Renders the true-to-scale assembled Pod + Cartridge + Sena Apex Inlay in semi-transparent X-ray aesthetic."""
    fig = plt.figure(figsize=(20, 12), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Coordinates setup (mm):
    # Pod Outer Housing: 68.0 mm (X: -34..+34) x 48.0 mm (Y: -24..+24) x 34.0 mm (Z: 0..34)
    # Cartridge: 54.0 mm (X: -27..+27) x 37.5 mm (Y: -18.75..+18.75) x 17.0 mm (Z: 14..31)

    # 1. TRANSLUCENT OUTER POD ENCLOSURE (Makrolon Polycarbonate / PA12 MJF: 68x48x34mm)
    draw_box(ax, -34, -24, 0, 68, 48, 34, color='#38bdf8', alpha=0.14, edgecolor='#0284c7', linewidth=1.0)
    # Corner chamfer lines
    for cx in [-34, 34]:
        for cy in [-24, 24]:
            ax.plot([cx, cx], [cy, cy], [0, 34], color='#38bdf8', linewidth=1.2, alpha=0.6)

    # 2. POM-C SNAP-LOCK RELEASE SLIDER & LATCH (Right housing wall at X = +34 mm)
    draw_box(ax, 32.5, -8, 18, 3.5, 16, 10, color='#e2e8f0', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 34.0, -5, 20, 2.0, 10, 6, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)

    # 3. INTERNAL COMPARTMENT DIVIDER (Z = 12.5 mm, separates Pod-Base Cavity from Cartridge Bay)
    draw_box(ax, -31, -21, 12.5, 62, 42, 1.5, color='#1e293b', alpha=0.45, edgecolor='#475569', linewidth=0.6)

    # 4. POD BASE PCB (openmotorbridge_pod_base: 28 x 28 x 1.6 mm at Z = 2.5 mm, Centered in Base)
    draw_box(ax, -14, -14, 2.5, 28, 28, 1.6, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # Ground ring / trace on Pod Base
    draw_box(ax, -13.5, -13.5, 4.1, 27, 27, 0.05, color='#eab308', alpha=0.8, edgecolor='#ca8a04', linewidth=0.4)

    # 5. M8 DIRECT PCB-MOUNT RECEPTACLE (Metal body at Z = 4.1 mm, threaded collar extending forward)
    draw_box(ax, -6, -6, 4.1, 12, 14, 8.4, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    # M8 Metal Snout extending through front housing wall (Y = -6 to Y = -30 mm)
    draw_cylinder(ax, x_c=0, y_c=-6, z0=8.3, radius=4.0, height=-24, color='#64748b', alpha=0.95, axis='y')
    # M8 Brass Thread Ridges / Knurled Collar & Anti-Vibration Nut
    draw_cylinder(ax, x_c=0, y_c=-25.5, z0=8.3, radius=4.6, height=-4.0, color='#eab308', alpha=1.0, axis='y')
    # Internal EPDM O-Ring (Black)
    draw_cylinder(ax, x_c=0, y_c=-23.5, z0=8.3, radius=4.2, height=-1.8, color='#0f172a', alpha=1.0, axis='y')

    # 6. SP3012 TVS ARRAY & CAPACITOR ON POD BASE PCB (Left wing: X = -9, Y = 0)
    draw_box(ax, -10.5, -2, 4.15, 3.2, 3.2, 0.9, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -10.0, 3.5, 4.15, 1.6, 0.9, 0.8, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)

    # 7. M2 MOUNTING FASTENERS WITH SILICONE DAMPING (X = -11 and X = +11, Z = 2.5..9)
    draw_cylinder(ax, x_c=-11, y_c=0, z0=2.5, radius=2.4, height=2.2, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=2.5, radius=2.4, height=2.2, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=-11, y_c=0, z0=4.7, radius=1.0, height=4.5, color='#e2e8f0', alpha=1.0, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=4.7, radius=1.0, height=4.5, color='#e2e8f0', alpha=1.0, axis='z')

    # 8. MILL-MAX 6-PIN POGO PIN ARRAY (Series 824, Z = 4.1 mm to Z = 15.5 mm)
    draw_box(ax, -7.5, 7.5, 4.1, 15, 2.5, 2.8, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pogo_x_positions = np.linspace(-6.35, 6.35, 6)
    for px in pogo_x_positions:
        # Lower barrel (Gold)
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=6.9, radius=0.48, height=6.6, color='#fbbf24', alpha=1.0, axis='z')
        # Plunger tip making contact at Z = 15.0 mm (Gold)
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=13.5, radius=0.38, height=1.8, color='#f59e0b', alpha=1.0, axis='z')

    # 9. SHORE 40A SILICONE PERIMETER GASKET (55 x 38.5 x 1.5 mm at Z = 13.8 mm)
    draw_box(ax, -27.5, -19.25, 13.8, 55, 38.5, 1.2, color='#06b6d4', alpha=0.65, edgecolor='#0891b2', linewidth=0.7)

    # 10. REMOVABLE WECHSELKASSETTE ENCLOSURE (54.0 x 37.5 x 17.0 mm, Z = 14.5 to 31.5 mm)
    # Translucent smoky purple casing (Alpha = 0.20)
    draw_box(ax, -27, -18.75, 14.5, 54, 37.5, 17.0, color='#a855f7', alpha=0.18, edgecolor='#c084fc', linewidth=0.9)

    # 11. CARTRIDGE CARRIER PCB (openmotorbridge_pod_cartridge: 35.0 x 25.0 x 1.2 mm at Z = 15.5 mm)
    draw_box(ax, -17.5, -12.5, 15.5, 35, 25, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # 6 Gold ENIG Pogo Contact Pads on Carrier PCB Bottom (Z = 15.2 mm)
    for px in pogo_x_positions:
        draw_box(ax, px - 0.7, 8.0, 15.0, 1.4, 1.5, 0.5, color='#f59e0b', alpha=1.0, edgecolor='#fbbf24', linewidth=0.6)

    # Carrier PCB Electronics: DS2401 ID + JST-SH 6P Socket
    draw_box(ax, -2.0, -1.0, 16.7, 3.5, 2.5, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6) # DS2401
    draw_box(ax, -5.0, -10.5, 16.7, 10.0, 3.5, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#cbd5e1', linewidth=0.6) # JST-SH 6P Low-Profile

    # 12. SENA APEX / CARDO DMC OEM INTERCOM INLAY MODULE (45.0 x 32.0 x 6.5 mm at Z = 20.0 mm)
    # Green FR4 OEM Mainboard
    draw_box(ax, -22.5, -16.0, 20.0, 45, 32, 1.4, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    # Large Metal RF Shielding Can (Sena Mesh 3.0 / Qualcomm Quad-Core Transceiver)
    draw_box(ax, -20.0, -6.0, 21.4, 22.0, 20.0, 4.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    # Secondary Bluetooth 5.3 RF Shield Can
    draw_box(ax, 4.0, -6.0, 21.4, 16.0, 14.0, 3.8, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    # Audio DSP & Codec IC (Wolfson / Cirrus Logic)
    draw_box(ax, 5.0, 9.0, 21.4, 6.0, 5.0, 1.2, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.5)
    # Gold Micro U.FL Antenna Connector
    draw_cylinder(ax, x_c=-18.0, y_c=-12.0, z0=21.4, radius=1.2, height=1.4, color='#fbbf24', alpha=1.0, axis='z')

    # Flexible FPC / JST-SH Interconnect Cable linking Carrier PCB to Sena OEM Module
    draw_box(ax, -4.0, -11.0, 17.5, 8.0, 2.0, 3.2, color='#f59e0b', alpha=0.9, edgecolor='#d97706', linewidth=0.4)

    # 13. ERGONOMIC GLOVE GRIP RIBS & STATUS LIGHTPIPE (Top of Cartridge, Z = 31.5 mm)
    for rib_y in np.linspace(-12, 12, 6):
        draw_box(ax, -22, rib_y - 0.8, 31.5, 44, 1.6, 1.2, color='#9333ea', alpha=0.65, edgecolor='#a855f7', linewidth=0.6)
    # Status LED Lightpipe (Diffused Green PMMA)
    draw_cylinder(ax, x_c=0, y_c=-14.0, z0=31.5, radius=2.0, height=1.6, color='#22c55e', alpha=0.95, axis='z')

    # View setup
    ax.view_init(elev=24, azim=-48)
    ax.set_xlim([-40, 40])
    ax.set_ylim([-34, 32])
    ax.set_zlim([-2, 42])
    ax.set_axis_off()

    # Title header
    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // UNIVERSAL SATELLITE POD & SENA APEX CARTRIDGE", 
             color='#38bdf8', fontsize=18, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "3D X-Ray CAD Architecture — True-to-Scale Assembly with Sena Apex / Cardo OEM Inlay (IP67)", 
             color='#94a3b8', fontsize=12, ha='center', fontfamily='sans-serif')

    # Technical Details Overlay
    left_card_text = (
        "WECHSELKASSETTE (54.0 x 37.5 x 17.0 mm)\n"
        "─────────────────────────────────────────\n"
        "• Translucent PA12 / Polycarbonat Shell\n"
        "• Handschuh-Riffelung & PMMA-Lichtleiter\n"
        "• POM-C Snap-Lock Verrastung (>85 N)\n\n"
        "INTEGRIERTES SENA APEX / MESH OEM-INLAY:\n"
        "• 45.0 x 32.0 x 6.5 mm OEM-Hauptplatine\n"
        "• Qualcomm Mesh 3.0 + Dual-BT RF Cans\n"
        "• U.FL Koaxialer Antennenanschluss\n\n"
        "KASSETTEN-TRÄGERPLATINE (35x25mm PCB):\n"
        "• DS2401 1-Wire Silicon Serial ID\n"
        "• Flacher JST-SH 1.0mm 6P Flex-Verbinder\n"
        "• 6x vergoldete ENIG-Pads (2.54mm Raster)"
    )
    fig.text(0.03, 0.46, left_card_text, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#c084fc', alpha=0.92, lw=1.4))

    right_card_text = (
        "UNTERER BEREICH: POD-BASIS & SCHNITTSTELLE\n"
        "─────────────────────────────────────────\n"
        "• Pod-Aussengehaeuse (68 x 48 x 34 mm)\n"
        "• Kassetten-Schacht (64 x 46 x 23.5 mm)\n"
        "• Shore 40A Silikon-Formschuhdichtung (IP67)\n"
        "• Mill-Max 6-Pin Pogo-Array (1.4mm Hub)\n\n"
        "POD-BODENPLATINE (28 x 28 mm PCB):\n"
        "• Littelfuse SP3012 TVS Array (<0.5 pF)\n"
        "• 2x M2 Silikon-Entkopplungsdome (Orange)\n\n"
        "M8-FAHRZEUGSCHNITTSTELLE (IP67):\n"
        "• Direkt aufgeloetete M8 6-Pin Einbaubuchse\n"
        "• M8x0.5 Vollmetallkragen mit EPDM O-Ring\n"
        "• Ruettelsichere Ueberwurfmutter (Anti-Vib)"
    )
    fig.text(0.68, 0.46, right_card_text, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created Accurate 3D X-Ray Assembly Render: {output_png}")

def render_exploded_view(output_png):
    """Renders an Exploded View of the true-scale Pod + Cartridge + Sena Inlay Stack."""
    fig = plt.figure(figsize=(20, 13), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Exploded offsets along Z-axis:
    # 1. Cartridge Top Shell: Z = 74..90
    # 2. Sena Apex OEM Inlay Module: Z = 56..64
    # 3. Cartridge Carrier PCB (35x25mm): Z = 42..44
    # 4. Silicone Perimeter Gasket: Z = 30..32
    # 5. Pod Divider & Pogo Array: Z = 16..24
    # 6. Pod Base PCB (28x28mm) & M8 Socket: Z = 0..10
    # 7. Pod Lower Enclosure Shell (68x48mm): Z = -26..-12

    # Layer 1: Cartridge Top Shell (54 x 37.5 x 16 mm, Polycarbonate)
    draw_box(ax, -27, -18.75, 74, 54, 37.5, 16, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.9)
    for rib_y in np.linspace(-12, 12, 6):
        draw_box(ax, -22, rib_y - 0.8, 90, 44, 1.6, 1.2, color='#9333ea', alpha=0.7, edgecolor='#a855f7', linewidth=0.6)
    draw_box(ax, 27, -6, 78, 2.5, 12, 8, color='#e2e8f0', alpha=0.95, edgecolor='#94a3b8', linewidth=0.6)

    # Layer 2: Sena Apex / Cardo OEM Intercom Inlay (45 x 32 x 6.5 mm)
    draw_box(ax, -22.5, -16.0, 56, 45, 32, 1.6, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    draw_box(ax, -20.0, -6.0, 57.6, 22.0, 20.0, 4.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 4.0, -6.0, 57.6, 16.0, 14.0, 3.8, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)

    # Layer 3: Cartridge Carrier PCB (openmotorbridge_pod_cartridge: 35 x 25 x 1.2 mm)
    draw_box(ax, -17.5, -12.5, 42, 35, 25, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    draw_box(ax, -2.0, -1.0, 43.2, 3.5, 2.5, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -5.0, -10.5, 43.2, 10.0, 3.5, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#cbd5e1', linewidth=0.6)

    # Layer 4: Silicone Perimeter Gasket (55 x 38.5 x 2.0 mm)
    draw_box(ax, -27.5, -19.25, 30, 55, 38.5, 2.0, color='#06b6d4', alpha=0.75, edgecolor='#0891b2', linewidth=0.9)

    # Layer 5: Mill-Max 6-Pin Pogo Array (Floating)
    draw_box(ax, -7.5, 7.5, 16, 15, 2.5, 3.0, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pogo_x_positions = np.linspace(-6.35, 6.35, 6)
    for px in pogo_x_positions:
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=19, radius=0.48, height=7.5, color='#fbbf24', alpha=1.0, axis='z')

    # Layer 6: Pod Base PCB (openmotorbridge_pod_base: 28 x 28 mm) & M8 Direct Receptacle
    draw_box(ax, -14, -14, 0, 28, 28, 1.6, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    draw_box(ax, -6, -6, 1.6, 12, 14, 8.4, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    draw_cylinder(ax, x_c=0, y_c=-6, z0=5.8, radius=4.0, height=-22, color='#64748b', alpha=0.95, axis='y')
    draw_cylinder(ax, x_c=0, y_c=-24, z0=5.8, radius=4.6, height=-4.0, color='#eab308', alpha=1.0, axis='y')
    draw_cylinder(ax, x_c=-11, y_c=0, z0=-8, radius=2.4, height=3.0, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=-8, radius=2.4, height=3.0, color='#f97316', alpha=0.95, axis='z')

    # Layer 7: Translucent Lower Pod Enclosure Shell (68 x 48 x 16 mm)
    draw_box(ax, -34, -24, -26, 68, 48, 16, color='#38bdf8', alpha=0.22, edgecolor='#0284c7', linewidth=0.9)

    # Vertical alignment guide lines
    for corner in [(-27, -18.75), (27, -18.75), (27, 18.75), (-27, 18.75)]:
        ax.plot([corner[0], corner[0]], [corner[1], corner[1]], [-26, 92], color='#475569', linestyle='--', linewidth=0.7, alpha=0.6)

    ax.view_init(elev=20, azim=-48)
    ax.set_xlim([-40, 40])
    ax.set_ylim([-36, 32])
    ax.set_zlim([-32, 98])
    ax.set_axis_off()

    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // EXPLODED POD & CARTRIDGE ASSEMBLY", 
             color='#38bdf8', fontsize=18, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "Explosionsdarstellung aller mechanischen & elektronischen Baugruppen (True-Scale)", 
             color='#94a3b8', fontsize=12, ha='center', fontfamily='sans-serif')

    exploded_legend = (
        "SCHICHT-HIERARCHIE (VON OBEN NACH UNTEN)\n"
        "─────────────────────────────────────────\n"
        "[1] KASSETTEN-OBERTEIL (Translucent Polycarbonat)\n"
        "    • 54.0 x 37.5 x 17.0 mm Gehaeuseschale\n"
        "    • POM-C Snap-Lock Verrastung\n\n"
        "[2] SENA APEX / MESH OEM-INLAY MODUL\n"
        "    • 45.0 x 32.0 x 6.5 mm Original-Platine\n"
        "    • Qualcomm Mesh 3.0 & BT 5.3 RF-Shields\n\n"
        "[3] KASSETTEN-TRÄGERPLATINE (35 x 25 mm PCB)\n"
        "    • DS2401 ID + JST-SH 1.0mm 6P Flex-Verbinder\n"
        "    • 6 vergoldete ENIG Pogo-Zielkontaktpads\n\n"
        "[4] SHORE 40A SILIKON-FORMSCHUHDICHTUNG (IP67)\n"
        "    • 55 x 38.5 mm umlaufende Feuchtigkeitsbarriere\n\n"
        "[5] MILL-MAX 6-PIN POGO-PIN FEDERKONTAKT-ARRAY\n"
        "    • Serie 824, 1.4mm Hub, vergoldete Tauchspitzen\n\n"
        "[6] POD-BODENPLATINE (openmotorbridge_pod_base, 28x28mm)\n"
        "    • Direkt verloetete M8 6-Pin IP67 Einbaubuchse\n"
        "    • Integrierte Littelfuse SP3012 TVS Matrix (<0.5pF)\n"
        "    • 2x M2 Silikon-Entkopplungsdome (Shore 40A)\n\n"
        "[7] POD-UNTERGEHÄUSE (Makrolon / PA12 MJF)\n"
        "    • 68 x 48 x 34 mm Gehaeusekoerper mit M8-Durchbruch"
    )
    fig.text(0.03, 0.44, exploded_legend, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created Accurate 3D Exploded View Render: {output_png}")

def export_vrml_assembly(output_wrl):
    """Exports the true-to-scale 3D Pod & Cartridge Assembly in VRML 2.0 format."""
    wrl_content = """#VRML V2.0 utf8
# OpenMotorBridge Universal Satellite Pod & Cartridge 3D Mechanical Assembly (True Scale)
# Generated by OpenMotorBridge CAD Engine

Group {
  children [
    # 1. Translucent Outer Pod Enclosure (68x48x34mm, Makrolon Polycarbonate)
    Transform {
      translation 0.0 0.0 0.017
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
          geometry Box { size 0.068 0.048 0.034 }
        }
      ]
    }

    # 2. Translucent Removable Cartridge Shell (54x37.5x17mm, Polycarbonate)
    Transform {
      translation 0.0 0.0 0.023
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
          geometry Box { size 0.054 0.0375 0.017 }
        }
      ]
    }

    # 3. Sena Apex / Cardo OEM Inlay Module (45x32x6.5mm)
    Transform {
      translation 0.0 0.0 0.024
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

    # 4. Cartridge Carrier PCB (35x25x1.2mm, openmotorbridge_pod_cartridge)
    Transform {
      translation 0.0 0.0 0.016
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

    # 5. Pod Base PCB (28x28x1.6mm, openmotorbridge_pod_base)
    Transform {
      translation 0.0 0.0 0.0033
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.58 0.41
              specularColor 0.3 0.3 0.3
              shininess 0.4
            }
          }
          geometry Box { size 0.028 0.028 0.0016 }
        }
      ]
    }

    # 6. M8 Metal Direct-Mount Receptacle with Threaded Collar
    Transform {
      translation 0.0 -0.018 0.008
      rotation 1.0 0.0 0.0 1.5708
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
            height 0.024
          }
        }
      ]
    }

    # 7. Silicone Perimeter Gasket (Shore 40A Cyan Boot, 55x38.5mm)
    Transform {
      translation 0.0 0.0 0.0145
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.71 0.83
              transparency 0.4
              shininess 0.2
            }
          }
          geometry Box { size 0.055 0.0385 0.0015 }
        }
      ]
    }
  ]
}
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_wrl)), exist_ok=True)
    with open(output_wrl, 'w', encoding='utf-8') as f:
        f.write(wrl_content)
    print(f"✓ Exported Accurate 3D VRML Assembly Model: {output_wrl}")

if __name__ == '__main__':
    xray_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly_render_xray.png'))
    exploded_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_exploded_view.png'))
    vrml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly.wrl'))
    render_xray_assembly(xray_path)
    render_exploded_view(exploded_path)
    export_vrml_assembly(vrml_path)
