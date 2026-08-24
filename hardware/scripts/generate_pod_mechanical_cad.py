#!/usr/bin/env python3
"""
OpenMotorBridge Pod & Cartridge Mechanical 3D CAD Generator & Premium X-Ray Renderer
-----------------------------------------------------------------------------------
Generates high-resolution semi-transparent (ghosted X-Ray / Glassmorphism) 3D CAD
visualizations of the Universal Satellite Pod Enclosure and Removable Intercom Cartridge.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

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
    """Renders the assembled Pod + Cartridge in semi-transparent X-ray aesthetic."""
    fig = plt.figure(figsize=(19, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Coordinate setup: Pod center at (0, 0), Base Z=0
    # Pod Outer: 36 x 36 x 44 mm (-18..18, -18..18, 0..44)
    # Cartridge: 30 x 30 x 20 mm (-15..15, -15..15, 22..42)

    # 1. TRANSLUCENT OUTER POD ENCLOSURE (Makrolon Polycarbonate, Alpha = 0.16)
    draw_box(ax, -18, -18, 0, 36, 36, 44, color='#38bdf8', alpha=0.16, edgecolor='#0284c7', linewidth=1.0)
    # Beveled corner chamfers (simulated as accent wireframes)
    for cx in [-18, 18]:
        for cy in [-18, 18]:
            ax.plot([cx, cx], [cy, cy], [0, 44], color='#38bdf8', linewidth=1.2, alpha=0.7)

    # 2. POM-C SNAP-LOCK RELEASE SLIDER & LATCH (Right housing wall at X = +18 mm)
    draw_box(ax, 16.5, -6, 28, 3.5, 12, 8, color='#e2e8f0', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 17.8, -4, 30, 2.0, 8, 4, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)

    # 3. INTERNAL COMPARTMENT DIVIDER (Z = 20 mm, separates Base Cavity from Cartridge Bay)
    draw_box(ax, -15.5, -15.5, 19.5, 31, 31, 1.5, color='#1e293b', alpha=0.45, edgecolor='#475569', linewidth=0.6)

    # 4. POD BASE PCB (openmotorbridge_pod_base: 28 x 28 x 1.6 mm at Z = 4 mm)
    draw_box(ax, -14, -14, 4, 28, 28, 1.6, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # Gold edge traces and ground ring
    draw_box(ax, -13.5, -13.5, 5.6, 27, 27, 0.05, color='#eab308', alpha=0.8, edgecolor='#ca8a04', linewidth=0.4)

    # 5. M8 DIRECT PCB-MOUNT CONNECTOR (Metal body at Z = 5.6 mm, threaded collar extending forward)
    # Metal shielded body on PCB
    draw_box(ax, -6, -6, 5.6, 12, 14, 9.0, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    # M8 Threaded Metal Snout extending through front housing wall (Y = -6 to Y = -24 mm)
    draw_cylinder(ax, x_c=0, y_c=-6, z0=10.1, radius=4.0, height=-18, color='#64748b', alpha=0.95, axis='y')
    # M8 Brass Thread Ridges / Knurled Ring & IP67 Nut
    draw_cylinder(ax, x_c=0, y_c=-19.5, z0=10.1, radius=4.6, height=-3.5, color='#eab308', alpha=1.0, axis='y')
    # Internal EPDM O-Ring (Black)
    draw_cylinder(ax, x_c=0, y_c=-17.5, z0=10.1, radius=4.2, height=-1.5, color='#0f172a', alpha=1.0, axis='y')

    # 6. SP3012 TVS ARRAY & CAPACITOR ON POD BASE PCB (Free Left wing: X = -9, Y = 0)
    draw_box(ax, -10.5, -2, 5.65, 3.2, 3.2, 0.9, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -10.0, 3.5, 5.65, 1.6, 0.9, 0.8, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)

    # 7. M2 MOUNTING FASTENERS WITH SHORE 40A SILICONE DAMPING (Left X=-11, Right X=+11, Z=4..12)
    # Silicone vibration damping washers (Vibrant Orange)
    draw_cylinder(ax, x_c=-11, y_c=0, z0=4, radius=2.6, height=2.5, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=4, radius=2.6, height=2.5, color='#f97316', alpha=0.95, axis='z')
    # M2 Stainless steel screws
    draw_cylinder(ax, x_c=-11, y_c=0, z0=6.5, radius=1.1, height=5.5, color='#e2e8f0', alpha=1.0, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=6.5, radius=1.1, height=5.5, color='#e2e8f0', alpha=1.0, axis='z')

    # 8. MILL-MAX 6-PIN POGO PIN ARRAY (Series 824, Z = 5.6 mm to Z = 22.5 mm)
    # Black header body on Pod Base PCB (Y = 8.5 mm)
    draw_box(ax, -7.5, 7.5, 5.6, 15, 2.5, 3.0, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    # 6 Gold spring pogo pins extending upward through divider slots into cartridge bay
    pogo_x_positions = np.linspace(-6.35, 6.35, 6)
    for px in pogo_x_positions:
        # Lower barrel (Gold)
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=8.6, radius=0.48, height=11.5, color='#fbbf24', alpha=1.0, axis='z')
        # Plunger tip making contact at Z = 22.0 mm (Gold)
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=20.1, radius=0.38, height=2.4, color='#f59e0b', alpha=1.0, axis='z')

    # 9. SHORE 40A SILICONE PERIMETER GASKET (Sealing boundary between Pod divider and Cartridge)
    draw_box(ax, -14.5, -14.5, 21.0, 29, 29, 1.2, color='#06b6d4', alpha=0.65, edgecolor='#0891b2', linewidth=0.7)

    # 10. REMOVABLE CARTRIDGE (Wechselkassette: Inserted in upper bay, Z = 22.0 to 42.0 mm)
    # Semi-transparent cartridge outer casing (Smoky purple-translucent, Alpha = 0.22)
    draw_box(ax, -14, -14, 22.0, 28, 28, 20.0, color='#a855f7', alpha=0.20, edgecolor='#c084fc', linewidth=0.9)

    # 11. CARTRIDGE PCB (openmotorbridge_cartridge: 24 x 16 x 1.2 mm at Z = 23.5 mm)
    draw_box(ax, -12, -8, 23.5, 24, 16, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)

    # 12. 6 GOLD ENIG MATING PADS ON CARTRIDGE PCB BOTTOM (Z = 23.5 mm)
    for px in pogo_x_positions:
        draw_box(ax, px - 0.7, 8.0, 23.0, 1.4, 1.5, 0.5, color='#f59e0b', alpha=1.0, edgecolor='#fbbf24', linewidth=0.6)

    # 13. CARTRIDGE ON-BOARD ELECTRONICS (Z = 24.7 mm)
    # DS2401 1-Wire Silicon Serial ID (TSOC-6)
    draw_box(ax, -9.0, -4.0, 24.7, 3.5, 3.0, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    # AT24C08 I2C Profile EEPROM (SOIC-8)
    draw_box(ax, -2.0, -4.0, 24.7, 4.5, 4.0, 1.2, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    # Toshiba TLP222A PhotoMOS Relays (DIP-4 / SMD)
    draw_box(ax, 5.0, -5.0, 24.7, 5.0, 4.5, 2.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)

    # 14. ERGONOMIC GRIP RIBS & STATUS LIGHTPIPE ON TOP OF CARTRIDGE (Z = 42.0 mm)
    for rib_y in np.linspace(-10, 10, 5):
        draw_box(ax, -11, rib_y - 0.8, 42.0, 22, 1.6, 1.2, color='#9333ea', alpha=0.6, edgecolor='#a855f7', linewidth=0.6)
    # Transparent LED Status Lightpipe
    draw_cylinder(ax, x_c=0, y_c=-9, z0=42.0, radius=1.8, height=1.5, color='#22c55e', alpha=0.9, axis='z')

    # View angle & lighting
    ax.view_init(elev=24, azim=-50)
    ax.set_xlim([-24, 24])
    ax.set_ylim([-26, 24])
    ax.set_zlim([-2, 48])
    ax.set_axis_off()

    # Title header
    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // UNIVERSAL SATELLITE POD & CARTRIDGE", 
             color='#38bdf8', fontsize=18, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "3D X-Ray CAD Architecture — 5-Layer Precision Mechanical & Electrical Stack (IP67)", 
             color='#94a3b8', fontsize=12, ha='center', fontfamily='sans-serif')

    # Left & Right Technical Legend Cards
    left_card_text = (
        "OBERER BEREICH: WECHSELKASSETTE\n"
        "──────────────────────────────────\n"
        "• Translucent Polycarbonat Shell\n"
        "  (30x30x20mm Wechsel-Inlay)\n"
        "• POM-C Snap-Lock Verriegelung\n"
        "• Griffige Handschuh-Riffelung\n"
        "• Status-LED Lichtleiter (Gruen)\n\n"
        "KASSETTEN-ELEKTRONIK (24x16mm PCB):\n"
        "• DS2401 1-Wire Silicon Serial ID\n"
        "• AT24C08 I2C Profil-EEPROM\n"
        "• Toshiba TLP222A PhotoMOS Relais\n"
        "• 6x vergoldete ENIG-Pads (2.54mm)"
    )
    fig.text(0.04, 0.48, left_card_text, color='#e2e8f0', fontsize=9.5, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#c084fc', alpha=0.92, lw=1.4))

    right_card_text = (
        "UNTERER BEREICH: POD-BASIS & SCHNITTSTELLE\n"
        "─────────────────────────────────────────\n"
        "• IP67 Perimeter Silikon-Formschuh\n"
        "  (Shore 40A Dichtwulst)\n"
        "• Mill-Max 6-Pin Pogo-Pin Array\n"
        "  (1.4mm Hub, 60g Vorspannung)\n\n"
        "POD-BODENPLATINE (28x28mm PCB):\n"
        "• Littelfuse SP3012 TVS Matrix (<0.5pF)\n"
        "• 2x M2 Silikon-Entkopplungsdome (Orange)\n\n"
        "M8-FAHRZEUGSCHNITTSTELLE (IP67):\n"
        "• Direkt aufgeloetete M8 6-Pin Buchse\n"
        "• Vollmetall-Schirmkragen mit M8x0.5\n"
        "• EPDM O-Ring & Rüttelsicherungs-Mutter"
    )
    fig.text(0.68, 0.48, right_card_text, color='#e2e8f0', fontsize=9.5, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created 3D X-Ray Assembly Render: {output_png}")

def render_exploded_view(output_png):
    """Renders an Exploded View (Explosionsdarstellung) of the Pod + Cartridge Stack."""
    fig = plt.figure(figsize=(19, 12), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Exploded offsets along Z-axis:
    # 1. Cartridge Top Shell: Z = 62..78
    # 2. Cartridge PCB: Z = 46..48
    # 3. Silicone Gasket: Z = 34..36
    # 4. Pod Divider & Pogo Array: Z = 18..28
    # 5. Pod Base PCB & M8 Socket: Z = 2..12
    # 6. Pod Base Lower Shell & M2 Screws: Z = -24..-10

    # Layer 1: Cartridge Top Shell (Polycarbonat)
    draw_box(ax, -14, -14, 62, 28, 28, 16, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.9)
    for rib_y in np.linspace(-10, 10, 5):
        draw_box(ax, -11, rib_y - 0.8, 78, 22, 1.6, 1.2, color='#9333ea', alpha=0.7, edgecolor='#a855f7', linewidth=0.6)
    draw_box(ax, 14, -4, 66, 2.5, 8, 8, color='#e2e8f0', alpha=0.95, edgecolor='#94a3b8', linewidth=0.6)

    # Layer 2: Cartridge PCB
    draw_box(ax, -12, -8, 46, 24, 16, 1.6, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # Components
    draw_box(ax, -9.0, -4.0, 47.6, 3.5, 3.0, 1.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -2.0, -4.0, 47.6, 4.5, 4.0, 1.2, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, 5.0, -5.0, 47.6, 5.0, 4.5, 2.0, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)

    # Layer 3: Silicone Perimeter Gasket
    draw_box(ax, -14.5, -14.5, 34, 29, 29, 2.0, color='#06b6d4', alpha=0.75, edgecolor='#0891b2', linewidth=0.9)

    # Layer 4: Mill-Max 6-Pin Pogo Array (Floating)
    draw_box(ax, -7.5, 7.5, 18, 15, 2.5, 3.0, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pogo_x_positions = np.linspace(-6.35, 6.35, 6)
    for px in pogo_x_positions:
        draw_cylinder(ax, x_c=px, y_c=8.75, z0=21, radius=0.48, height=7.0, color='#fbbf24', alpha=1.0, axis='z')

    # Layer 5: Pod Base PCB (openmotorbridge_pod_base) & Direct M8 Connector
    draw_box(ax, -14, -14, 2, 28, 28, 1.6, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    draw_box(ax, -6, -6, 3.6, 12, 14, 9.0, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    draw_cylinder(ax, x_c=0, y_c=-6, z0=8.1, radius=4.0, height=-18, color='#64748b', alpha=0.95, axis='y')
    draw_cylinder(ax, x_c=0, y_c=-20, z0=8.1, radius=4.5, height=-3.5, color='#eab308', alpha=1.0, axis='y')
    draw_box(ax, -10.5, -2, 3.6, 3.0, 3.0, 0.8, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -10.0, 3, 3.6, 1.6, 0.8, 0.8, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)

    # Layer 6: M2 Silicone Damping Rings & Screws
    draw_cylinder(ax, x_c=-11, y_c=0, z0=-8, radius=2.6, height=3.0, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=-8, radius=2.6, height=3.0, color='#f97316', alpha=0.95, axis='z')
    draw_cylinder(ax, x_c=-11, y_c=0, z0=-5, radius=1.1, height=8.0, color='#e2e8f0', alpha=1.0, axis='z')
    draw_cylinder(ax, x_c=11, y_c=0, z0=-5, radius=1.1, height=8.0, color='#e2e8f0', alpha=1.0, axis='z')

    # Layer 7: Translucent Lower Pod Enclosure Shell
    draw_box(ax, -18, -18, -24, 36, 36, 18, color='#38bdf8', alpha=0.22, edgecolor='#0284c7', linewidth=0.9)

    # Connecting vertical guide dashed lines
    for corner in [(-14, -14), (14, -14), (14, 14), (-14, 14)]:
        ax.plot([corner[0], corner[0]], [corner[1], corner[1]], [-24, 80], color='#475569', linestyle='--', linewidth=0.7, alpha=0.6)

    ax.view_init(elev=20, azim=-50)
    ax.set_xlim([-25, 25])
    ax.set_ylim([-28, 25])
    ax.set_zlim([-30, 85])
    ax.set_axis_off()

    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // EXPLODED POD & CARTRIDGE ASSEMBLY", 
             color='#38bdf8', fontsize=18, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "Explosionsdarstellung aller mechanischen & elektronischen Baugruppen", 
             color='#94a3b8', fontsize=12, ha='center', fontfamily='sans-serif')

    # Exploded Legend Cards
    exploded_legend = (
        "SCHICHT-HIERARCHIE (VON OBEN NACH UNTEN)\n"
        "─────────────────────────────────────────\n"
        "[1] KASSETTEN-OBERTEIL (Translucent Polycarbonat)\n"
        "    • 30x30x20mm Gehaeuseschale mit Grifflaschen\n"
        "    • POM-C Snap-Lock Verrastung\n\n"
        "[2] KASSETTEN-PLATINE (openmotorbridge_cartridge)\n"
        "    • DS2401 ID + AT24C08 EEPROM + TLP222A Optos\n\n"
        "[3] SHORE 40A SILIKON-FORMSCHUHDICHTUNG (IP67)\n"
        "    • Umlaufende Barriere gegen Feuchtigkeit & Staub\n\n"
        "[4] MILL-MAX 6-PIN POGO-PIN FEDERKONTAKT-ARRAY\n"
        "    • Serie 824, 1.4mm Hub, vergoldete Tauchspitzen\n\n"
        "[5] POD-BODENPLATINE (openmotorbridge_pod_base, 28x28mm)\n"
        "    • Direkt verloetete M8 6-Pin IP67 Einbaubuchse\n"
        "    • Integrierte Littelfuse SP3012 TVS Matrix (<0.5pF)\n\n"
        "[6] M2 SILIKON-ENTKOPPLUNGSRINGE (Shore 40A)\n"
        "    • Vibrationsdaempfung gegen Motor- und Fahrbahnstoesse\n\n"
        "[7] POD-UNTERGEHAEUSE (Makrolon / PA6-GF30)\n"
        "    • 36x36x44mm Gehaeusekoerper mit M8-Durchbruch"
    )
    fig.text(0.04, 0.45, exploded_legend, color='#e2e8f0', fontsize=9.5, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Created 3D Exploded View Render: {output_png}")

def export_vrml_assembly(output_wrl):
    """Exports the 3D Pod & Cartridge Assembly in VRML 2.0 format for 3D CAD/Viewer inspection."""
    wrl_content = """#VRML V2.0 utf8
# OpenMotorBridge Universal Satellite Pod & Cartridge 3D Mechanical Assembly
# Generated by OpenMotorBridge CAD Engine

Group {
  children [
    # 1. Translucent Outer Pod Enclosure (36x36x44mm, Makrolon Polycarbonate)
    Transform {
      translation 0.0 0.0 0.022
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.22 0.74 0.97
              specularColor 0.8 0.8 0.8
              transparency 0.75
              shininess 0.9
            }
          }
          geometry Box { size 0.036 0.036 0.044 }
        }
      ]
    }

    # 2. Translucent Removable Cartridge Shell (30x30x20mm, Polycarbonate)
    Transform {
      translation 0.0 0.0 0.032
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.65 0.33 0.96
              specularColor 0.7 0.7 0.7
              transparency 0.70
              shininess 0.8
            }
          }
          geometry Box { size 0.028 0.028 0.020 }
        }
      ]
    }

    # 3. Pod Base PCB (28x28x1.6mm, FR4 Green)
    Transform {
      translation 0.0 0.0 0.0048
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

    # 4. Cartridge PCB (24x16x1.2mm, FR4 Green)
    Transform {
      translation 0.0 0.0 0.0241
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.47 0.34
              specularColor 0.3 0.3 0.3
              shininess 0.4
            }
          }
          geometry Box { size 0.024 0.016 0.0012 }
        }
      ]
    }

    # 5. M8 Metal Direct-Mount Receptacle with Threaded Collar
    Transform {
      translation 0.0 -0.012 0.009
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
            height 0.016
          }
        }
      ]
    }

    # 6. Silicone Perimeter Gasket (Shore 40A Cyan Boot)
    Transform {
      translation 0.0 0.0 0.0215
      children [
        Shape {
          appearance Appearance {
            material Material {
              diffuseColor 0.02 0.71 0.83
              transparency 0.4
              shininess 0.2
            }
          }
          geometry Box { size 0.029 0.029 0.0012 }
        }
      ]
    }
  ]
}
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_wrl)), exist_ok=True)
    with open(output_wrl, 'w', encoding='utf-8') as f:
        f.write(wrl_content)
    print(f"✓ Exported 3D VRML Assembly Model: {output_wrl}")

if __name__ == '__main__':
    xray_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly_render_xray.png'))
    exploded_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_exploded_view.png'))
    vrml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cad/openmotorbridge_pod_assembly.wrl'))
    render_xray_assembly(xray_path)
    render_exploded_view(exploded_path)
    export_vrml_assembly(vrml_path)
