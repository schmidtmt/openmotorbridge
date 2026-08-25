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
        x_grid = x0 + radius * np.cos(theta_grid)
        y_grid = y0 + radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=alpha, shade=True, rstride=1, cstride=1)

def render_xray_assembly(output_png):
    """Renders the Generic Large-Format Pod + Cartridge assembly in semi-transparent X-ray aesthetic."""
    fig = plt.figure(figsize=(20, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # Coordinate Setup (mm) — GENERIC MAXIMUM ENVELOPE (Fits 100% Sena 50S/60S, Cardo Edge/Pro, OMM):
    # Pod Outer Housing: 120.0 mm along X (-60..+60), 64.0 mm along Y (-32..+32), 32.0 mm along Z (-16..+16)
    # Centric Cartridge Bay: 96.0 mm (X = -36 to +60 mm), 56.0 mm (Y = -28 to +28 mm), 24.0 mm (Z = -12 to +12 mm)
    # Wall thickness: Symmetric 3.0 mm top, bottom, left, right

    # 1. TRANSLUCENT OUTER POD HOUSING (PA12 MJF: 120x64x32mm)
    draw_box(ax, -60, -32, -16, 120, 64, 32, color='#38bdf8', alpha=0.14, edgecolor='#0284c7', linewidth=1.0)
    for cy in [-32, 32]:
        for cz in [-16, 16]:
            ax.plot([-60, 60], [cy, cy], [cz, cz], color='#38bdf8', linewidth=1.0, alpha=0.6)

    # 2. ASYMMETRIC POKA-YOKE GUIDE RAILS (Inside Chamber Walls)
    # Left Guide Rail (1.5mm keyway at Y = -28.0 mm)
    draw_box(ax, -36.0, -28.0, -1.0, 92.0, 1.5, 2.5, color='#0284c7', alpha=0.8, edgecolor='#38bdf8', linewidth=0.6)
    # Right Guide Rail (2.0mm keyway at Y = +26.5 mm)
    draw_box(ax, -36.0, 26.5, -1.0, 92.0, 2.0, 2.5, color='#0284c7', alpha=0.8, edgecolor='#38bdf8', linewidth=0.6)

    # 3. POD BASE PCB (openmotorbridge_pod_base: 48x24x1.6mm mounted on inner wall at X = -54.0 mm)
    draw_box(ax, -54.0, -24.0, -12.0, 1.6, 48.0, 24.0, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # Ground plane
    draw_box(ax, -53.9, -23.5, -11.5, 0.05, 47.0, 23.0, color='#eab308', alpha=0.8, edgecolor='#ca8a04', linewidth=0.4)

    # 4. M8 6-PIN IP67 RECEPTACLE (Mounted on outer face of Pod Base PCB at X = -54.0 mm)
    draw_box(ax, -58.0, -7.0, -7.0, 4.0, 14.0, 14.0, color='#94a3b8', alpha=0.98, edgecolor='#cbd5e1', linewidth=0.8)
    draw_cylinder(ax, x0=-58.0, y0=0, z0=0, radius=4.0, length=-20.0, color='#64748b', alpha=0.95, axis='x')
    draw_cylinder(ax, x0=-72.0, y0=0, z0=0, radius=4.6, length=-4.5, color='#eab308', alpha=1.0, axis='x')
    draw_cylinder(ax, x0=-70.0, y0=0, z0=0, radius=4.2, length=-2.0, color='#0f172a', alpha=1.0, axis='x')

    # 5. SP3012 TVS ARRAY & DECOUPLING CAP ON POD BASE PCB
    draw_box(ax, -52.4, 12.0, 3.0, 0.9, 3.2, 3.2, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6)
    draw_box(ax, -52.4, 12.5, -5.0, 0.8, 1.6, 0.9, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)

    # 6. EINSCHRAUBBARE SCHOTTWAND / SCHUTZBLENDE (Screwed-In Protective Bulkhead Cover: X = -44.0 to -42.0 mm)
    # Isolates Pod-Base PCB cavity completely from cartridge slide-in bay (56x24x2mm)
    draw_box(ax, -44.0, -28.0, -12.0, 2.0, 56.0, 24.0, color='#0284c7', alpha=0.55, edgecolor='#38bdf8', linewidth=0.9)
    # 2x M2 Countersunk Screws fixing bulkhead to housing bosses (Top-Left & Bottom-Right)
    draw_cylinder(ax, x0=-42.0, y0=-22.0, z0=8.0, radius=1.8, length=-2.0, color='#cbd5e1', alpha=1.0, axis='x')
    draw_cylinder(ax, x0=-42.0, y0=22.0, z0=-8.0, radius=1.8, length=-2.0, color='#cbd5e1', alpha=1.0, axis='x')

    # 6B. INTEGRATED PA12 PROTECTIVE SHROUD ON BULKHEAD (Centered at Y=0, Z=0, X = -42.0 to -36.0 mm)
    # 1.2mm wall with 45° self-centering funnel
    draw_box(ax, -42.0, -10.0, -3.0, 6.0, 20.0, 6.0, color='#0284c7', alpha=0.40, edgecolor='#38bdf8', linewidth=0.8)
    draw_box(ax, -52.4, -8.0, -1.5, 3.0, 16.0, 3.0, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pin_y_positions = np.linspace(-7.0, 7.0, 6)
    for py in pin_y_positions:
        # Gold Pins extending from PCB through bulkhead into PA12 protective funnel
        draw_cylinder(ax, x0=-49.4, y0=py, z0=0, radius=0.35, length=10.0, color='#fbbf24', alpha=1.0, axis='x')

    # 6C. ePTFE PRESSURE COMPENSATION VENT MEMBRANE (Ø 7.0 mm centered on LONG TOP ROOF at X = 0.0 mm, Z = +16.0 mm)
    draw_cylinder(ax, x0=0.0, y0=0.0, z0=15.2, radius=3.5, length=1.2, color='#f8fafc', alpha=0.98, axis='z')
    draw_cylinder(ax, x0=0.0, y0=0.0, z0=15.6, radius=2.0, length=0.9, color='#0f172a', alpha=1.0, axis='z') # Breathable ePTFE Gore/Schreiner Core

    # 6D. DUAL SPRING-LOADED AUTO-EJECT PUSHERS (V4A Edelstahl-Druckfedern at Y = -18.0 and Y = +18.0 mm)
    # Compressed under pre-tension against sled front face (pushes cartridge out 10mm upon button click)
    for sy in [-18.0, 18.0]:
        draw_cylinder(ax, x0=-42.0, y0=sy, z0=0.0, radius=2.2, length=6.0, color='#f59e0b', alpha=0.95, axis='x')
        draw_cylinder(ax, x0=-36.0, y0=sy, z0=0.0, radius=1.4, length=-4.5, color='#e2e8f0', alpha=1.0, axis='x')

    # 7. OPEN CARTRIDGE CARRIER SLED (Generischer U-Einschubschlitten ohne oberen Deckel: 92x54x23.5mm)
    # Bottom floor tray (Z = -11.0 to -9.0 mm)
    draw_box(ax, -36.0, -27.0, -11.0, 92.0, 54.0, 2.0, color='#a855f7', alpha=0.45, edgecolor='#c084fc', linewidth=0.9)
    # Left front face holding socket (X = -36.0 to -33.5 mm)
    draw_box(ax, -36.0, -27.0, -9.0, 2.5, 54.0, 19.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.8)
    # Left & right side guide rails (Y = -27.0 and Y = +25.0 mm)
    draw_box(ax, -33.5, -27.0, -9.0, 89.5, 2.0, 17.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.7)
    draw_box(ax, -33.5, 25.0, -9.0, 89.5, 2.0, 17.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.7)
    # OPEN TOP: No lid on cartridge! Full 23.5mm vertical headroom inside pod enclosure

    # 8. HORIZONTAL 6-PIN SOCKET ON CARTRIDGE FRONT EDGE (at X = -36.0 to -28.0 mm, Centered at Y=0, Z=0)
    # Socket slides directly into PA12 protective collar (piston-like seal)
    draw_box(ax, -36.0, -9.0, -2.0, 8.0, 18.0, 4.0, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.7)

    # 9. FLAT HORIZONTAL CARTRIDGE PCB (Lying directly in open sled floor at Z = -9.0 mm: 60x36x1.2mm)
    draw_box(ax, -33.5, -18.0, -9.0, 60.0, 36.0, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # 500mA PTC Fuse (F1) & Green Power LED (D1)
    draw_box(ax, -26.0, -8.0, -7.8, 2.0, 1.2, 0.8, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)
    draw_box(ax, -26.0, 8.0, -7.8, 2.0, 1.2, 0.8, color='#22c55e', alpha=1.0, edgecolor='#16a34a', linewidth=0.5)
    # DS2401 ID Chip & JST-SH 6P Header
    draw_box(ax, -20.0, -2.0, -7.8, 3.2, 3.2, 1.2, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -2.0, -6.0, -7.8, 4.0, 12.0, 2.0, color='#f8fafc', alpha=1.0, edgecolor='#cbd5e1', linewidth=0.6)

    # 10. SENA 50S / CARDO EDGE / OMM MODULE (Generischer 88x50mm Bauraum ohne Kopfbeschränkung)
    draw_box(ax, -28.0, -23.0, -1.0, 80.0, 46.0, 1.6, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    draw_box(ax, -24.0, -20.0, 0.6, 32.0, 26.0, 6.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 14.0, -18.0, 0.6, 30.0, 22.0, 5.5, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)

    # 11. IP67 SEALING FACEPLATE & DUAL SNAP-FIT LATCHES (Outer Right Flange at X = +56.0 mm)
    # Silicone Perimeter Flange Seal (Shore 40A, 2.0mm gasket around opening rim)
    draw_box(ax, 54.0, -29.0, -14.0, 2.0, 58.0, 28.0, color='#06b6d4', alpha=0.85, edgecolor='#0891b2', linewidth=0.9)
    # Solid PA12 Outer Faceplate / Grip Handle
    draw_box(ax, 56.0, -30.0, -15.0, 4.0, 60.0, 30.0, color='#6b21a8', alpha=0.95, edgecolor='#a855f7', linewidth=0.9)
    # Dual Quick-Release Snap-Fit Buttons (Lateral at Y = -28.0 and Y = +24.0 mm)
    draw_box(ax, 57.0, -28.5, -4.0, 3.5, 3.5, 8.0, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)
    draw_box(ax, 57.0, 25.0, -4.0, 3.5, 3.5, 8.0, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)

    # View angle setup with TRUE PHYSICAL ASPECT RATIO (prevents square distortion)
    ax.view_init(elev=22, azim=-50)
    span_x = 74 - (-82) # 156 mm
    span_y = 40 - (-40) # 80 mm
    span_z = 24 - (-24) # 48 mm
    ax.set_xlim([-82, 74])
    ax.set_ylim([-40, 40])
    ax.set_zlim([-24, 24])
    ax.set_box_aspect((span_x, span_y, span_z))
    ax.set_axis_off()

    # Title header
    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // GENERIC UNIVERSAL POD & OPEN SLED (120 x 64 x 32 mm)", 
             color='#38bdf8', fontsize=17, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "3D X-Ray CAD Architektur — 100% Generic Envelope für Sena 50S/60S, Cardo Edge/Pro & OMM Transceiver", 
             color='#94a3b8', fontsize=11.5, ha='center', fontfamily='sans-serif')

    # Technical Details Overlay
    left_card_text = (
        "UNIVERSAL-POD: 120 x 64 x 32 mm (MAX-ENVELOPE)\n"
        "──────────────────────────────────────────────────\n"
        "• M8 6-Pin IP67 Vollmetall-Einbaubuchse (M8 A-Code)\n"
        "• Pod-Base Platine (48 x 24 mm PCB mit SP3012 TVS)\n"
        "• Einschraubbare Schottwand (2x M2 Schrauben)\n"
        "  (100% Berührungsschutz & Platinenkapselung)\n"
        "• 6-Pin Stiftleiste mit PA12-Schutzkragen (Zentrisch)\n"
        "• Duale Edelstahl-Auswerferfedern (Auto-Eject)\n"
        "  (Federt Kassette bei Tastendruck 10mm aus)\n"
        "• Mittige ePTFE-Druckausgleichsmembran (Ø 7mm)\n"
        "  (Atmungsaktiv IP67 auf Gehäuse-Oberseite)\n"
        "• Asymmetrische Poka-Yoke Führungsstege (1.5 / 2.0mm)"
    )
    fig.text(0.04, 0.48, left_card_text, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111827', edgecolor='#38bdf8', alpha=0.92, lw=1.4))

    right_card_text = (
        "OFFENER EINSCHUB-SCHLITTEN (OPEN CARRIER SLED)\n"
        "──────────────────────────────────────────────────\n"
        "• Lichter Bauraum: 88 x 50 x 23.5 mm (Open Top)\n"
        "• 100% Kompatibel: Sena 50S/60S, Cardo Edge/Pro,\n"
        "  Cardo Bold/Freecom, Midland & OMM-Transceiver\n"
        "• Flat-Carrier-PCB (60 x 36 mm): DS2401 & JST-SH\n"
        "• Piston-Einschub: 6-Pin Buchse in Shroud\n\n"
        "IP67-SEITENDICHTUNG & QUICK-RELEASE RASTUNG:\n"
        "• Umlaufende Shore 40A Silikondichtung (2.0mm)\n"
        "• Duale seitliche Snap-Fit Schnellverriegelung\n"
        "• Taktiles 'Klick'-Einrasten & werkzeuglose\n"
        "  Schnell-Entriegelung über seitliche Drucktasten"
    )
    fig.text(0.68, 0.48, right_card_text, color='#e2e8f0', fontsize=9.2, fontfamily='monospace',
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
    # 1. M8 Threaded Collar & Nut: X = -96..-78
    # 2. Pod Base PCB (ADPT: 48x24mm): X = -64..-62
    # 3. Screwed-In Bulkhead Plate (2x M2): X = -38..-36 with Integrated Shroud (-36..-28)
    # 3C. Dual Stainless Steel Ejector Springs: X = -36..-24
    # 3B. ePTFE Pressure Vent Membrane: Floating above at center X = 0.0, Z = +26
    # 4. Open Cartridge Carrier Sled (U-Chassis ohne Deckel: 92x54x23.5mm): X = +4..+76
    # 5. Horizontal 6-Pin Socket: X = +4..+12
    # 6. Flat Cartridge Carrier PCB (60x36mm): X = +12..+64 (Z=-9)
    # 7. Sena 50S / Cardo Edge / OMM Module: X = +16..+72 (Z=+1)
    # 8. IP67 Perimeter Silicone Gasket: X = +86..+88
    # 9. Outer Sealing Faceplate with Snap-Fit Latches: X = +92..+98

    # 1. M8 Receptacle & Knurled Nut (Floating Left)
    draw_cylinder(ax, x0=-78, y0=0, z0=0, radius=4.0, length=-20.0, color='#64748b', alpha=0.95, axis='x')
    draw_cylinder(ax, x0=-90, y0=0, z0=0, radius=4.6, length=-4.5, color='#eab308', alpha=1.0, axis='x')

    # 2. Pod Base PCB (openmotorbridge_pod_base: 48x24x1.6mm at X = -64 mm)
    draw_box(ax, -64.0, -24.0, -12.0, 1.6, 48.0, 24.0, color='#059669', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    draw_box(ax, -62.4, 12.0, 3.0, 0.9, 3.2, 3.2, color='#0f172a', alpha=1.0, edgecolor='#64748b', linewidth=0.6) # SP3012
    draw_box(ax, -62.4, -8.0, -1.5, 3.0, 16.0, 3.0, color='#0f172a', alpha=1.0, edgecolor='#334155', linewidth=0.6)
    pin_y_positions = np.linspace(-7.0, 7.0, 6)
    for py in pin_y_positions:
        draw_cylinder(ax, x0=-59.4, y0=py, z0=0, radius=0.35, length=24.0, color='#fbbf24', alpha=1.0, axis='x')

    # 3. Screwed-In Bulkhead Plate (PA12 Schutz-Schottwand: 56x24x2mm at X = -38 mm)
    draw_box(ax, -38.0, -28.0, -12.0, 2.0, 56.0, 24.0, color='#0284c7', alpha=0.65, edgecolor='#38bdf8', linewidth=0.9)
    # 2x M2 Countersunk Screws fixing bulkhead
    draw_cylinder(ax, x0=-36.0, y0=-22.0, z0=8.0, radius=1.8, length=3.0, color='#cbd5e1', alpha=1.0, axis='x')
    draw_cylinder(ax, x0=-36.0, y0=22.0, z0=-8.0, radius=1.8, length=3.0, color='#cbd5e1', alpha=1.0, axis='x')
    # Integrated PA12 Shroud Collar (Floating with bulkhead at X = -36 to -28 mm)
    draw_box(ax, -36.0, -10.0, -3.0, 8.0, 20.0, 6.0, color='#0284c7', alpha=0.35, edgecolor='#38bdf8', linewidth=0.8)

    # 3C. Dual Stainless Steel Ejector Springs (Floating forward from Bulkhead at X = -36 to -24 mm)
    for sy in [-18.0, 18.0]:
        draw_cylinder(ax, x0=-36.0, y0=sy, z0=0.0, radius=2.2, length=9.0, color='#f59e0b', alpha=0.95, axis='x')
        draw_cylinder(ax, x0=-27.0, y0=sy, z0=0.0, radius=1.4, length=-6.0, color='#e2e8f0', alpha=1.0, axis='x')

    # 3B. ePTFE Pressure Vent Membrane (Floating above center of long top roof at X = 0.0 mm, Z = +26 mm)
    draw_cylinder(ax, x0=0.0, y0=0.0, z0=25.0, radius=4.5, length=2.0, color='#f8fafc', alpha=0.98, axis='z')
    draw_cylinder(ax, x0=0.0, y0=0.0, z0=25.5, radius=2.8, length=1.5, color='#0f172a', alpha=1.0, axis='z')

    # 4. Open Cartridge Carrier Sled (U-Chassis ohne Deckel at X = +4 mm: 72x54x23.5mm)
    # Bottom floor tray (Z = -11.0 to -9.0 mm)
    draw_box(ax, 4.0, -27.0, -11.0, 72.0, 54.0, 2.0, color='#a855f7', alpha=0.45, edgecolor='#c084fc', linewidth=0.9)
    # Left front face holding socket
    draw_box(ax, 4.0, -27.0, -9.0, 2.5, 54.0, 19.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.8)
    # Left & right side guide rails
    draw_box(ax, 6.5, -27.0, -9.0, 69.5, 2.0, 17.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.7)
    draw_box(ax, 6.5, 25.0, -9.0, 69.5, 2.0, 17.5, color='#a855f7', alpha=0.35, edgecolor='#c084fc', linewidth=0.7)

    # 5. Horizontal 6-Pin Socket on Cartridge Leading Edge
    draw_box(ax, 4.0, -9.0, -2.0, 8.0, 18.0, 4.0, color='#1e293b', alpha=0.98, edgecolor='#475569', linewidth=0.7)

    # 6. Flat Cartridge Carrier PCB (60x36x1.2mm, Lower Floor Layer Z = -9.0 mm)
    draw_box(ax, 10.0, -18.0, -9.0, 60.0, 36.0, 1.2, color='#047857', alpha=0.95, edgecolor='#10b981', linewidth=0.9)
    # 500mA PTC Fuse (F1), Power LED (D1), and DS2401 ID Chip
    draw_box(ax, 16.0, -8.0, -7.8, 2.0, 1.2, 0.8, color='#d97706', alpha=1.0, edgecolor='#b45309', linewidth=0.5)
    draw_box(ax, 16.0, 8.0, -7.8, 2.0, 1.2, 0.8, color='#22c55e', alpha=1.0, edgecolor='#16a34a', linewidth=0.5)
    draw_box(ax, 24.0, -2.0, -7.8, 3.2, 3.2, 1.2, color='#0f172a', alpha=1.0, edgecolor='#475569', linewidth=0.6)

    # 7. Sena 50S / Cardo Edge / OMM Module (Upper Layer Z = +0.5 mm)
    draw_box(ax, 12.0, -23.0, 0.5, 62.0, 46.0, 1.6, color='#065f46', alpha=0.95, edgecolor='#059669', linewidth=0.9)
    draw_box(ax, 16.0, -20.0, 2.1, 28.0, 24.0, 6.0, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax, 48.0, -18.0, 2.1, 24.0, 20.0, 5.5, color='#cbd5e1', alpha=0.98, edgecolor='#94a3b8', linewidth=0.8)

    # 8. IP67 Perimeter Silicone Flange Gasket (Shore 40A at X = +86 mm)
    draw_box(ax, 86.0, -29.0, -14.0, 2.0, 58.0, 28.0, color='#06b6d4', alpha=0.85, edgecolor='#0891b2', linewidth=0.9)

    # 9. Outer Sealing Faceplate & Snap-Fit Latches (X = +92 mm)
    draw_box(ax, 92.0, -30.0, -15.0, 4.0, 60.0, 30.0, color='#6b21a8', alpha=0.95, edgecolor='#a855f7', linewidth=0.9)
    draw_box(ax, 93.0, -28.5, -4.0, 3.5, 3.5, 8.0, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)
    draw_box(ax, 93.0, 25.0, -4.0, 3.5, 3.5, 8.0, color='#f59e0b', alpha=1.0, edgecolor='#d97706', linewidth=0.6)

    # Horizontal guide dashed alignment lines
    for corner in [(-27.0, -11.0), (27.0, -11.0), (27.0, 11.0), (-27.0, 11.0)]:
        ax.plot([-96, 96], [corner[0], corner[0]], [corner[1], corner[1]], color='#475569', linestyle='--', linewidth=0.7, alpha=0.6)

    ax.view_init(elev=20, azim=-50)
    span_x = 106 - (-106) # 212 mm
    span_y = 38 - (-38)   # 76 mm
    span_z = 28 - (-28)   # 56 mm
    ax.set_xlim([-106, 106])
    ax.set_ylim([-38, 38])
    ax.set_zlim([-28, 28])
    ax.set_box_aspect((span_x, span_y, span_z))
    ax.set_axis_off()

    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // EXPLODED UNIVERSAL POD & OPEN SLED ASSEMBLY", 
             color='#38bdf8', fontsize=17, fontweight='bold', ha='center', fontfamily='sans-serif')
    fig.text(0.5, 0.915, "Horizontale Explosionsdarstellung (120 x 64 x 32 mm): Schottwand, Auto-Eject Federn & Offener Großraum-Schlitten", 
             color='#94a3b8', fontsize=11.5, ha='center', fontfamily='sans-serif')

    exploded_legend = (
        "SCHICHT-HIERARCHIE ENTLANG DER EINSCHUBACHSE (X-ACHSE)\n"
        "─────────────────────────────────────────────────────────────\n"
        "[1] M8 6-PIN IP67 EINBAUBUCHSE & MUTTER (Links)\n"
        "    • M8 A-Coded Vollmetallbuchse mit Rüttelsicherung\n\n"
        "[2] POD-BASE PLATINE (48 x 24 mm PCB)\n"
        "    • Direkt aufgelötete M8-Buchse & SP3012 TVS\n\n"
        "[3] SCHUTZ-SCHOTTWAND MIT AUTO-EJECT FEDERN (2x M2)\n"
        "    • PA12-Trennwand (56 x 24 mm) kapselt Platine 100% berührungssicher\n"
        "    • Integrierter Schutzkragen & 45° Fangtrichter\n"
        "    • Duale Edelstahl-Federn werfen Kassette 10mm aus\n\n"
        "[4] MITTIGE ePTFE-DRUCKAUSGLEICHSMEMBRAN (Ø 7mm)\n"
        "    • Zentral auf langer Gehäuse-Oberseite (IP67)\n\n"
        "[5] OFFENER EINSCHUB-SCHLITTEN (92 x 54 x 23.5 mm)\n"
        "    • U-Chassis ohne Deckel (88 x 50 mm Lichter Bauraum)\n\n"
        "[6] 6-PIN FRONT-BUCHSENLEISTE (ZENTRISCH)\n"
        "    • Gleitet saugend in Schottwand-Schutzkragen ein\n\n"
        "[7] KASSETTEN-TRÄGERPLATINE (60 x 36 mm PCB)\n"
        "    • Liegt flach am Boden: PTC, LED, DS2401, JST-SH\n\n"
        "[8] SENA / CARDO / OMM MODUL-BAURAUM (80 x 46 mm)\n"
        "    • Volle lichte Bauhöhe nach oben unbeschränkt\n\n"
        "[9] SHORE 40A SILIKON-STIRNFLANSCHDICHTUNG (2.0 mm)\n"
        "    • Dichtet den Öffnungsflansch zu 100% IP67 ab\n\n"
        "[10] PA12-ABSCHLUSSBLENDE & SNAP-FIT RASTUNG\n"
        "    • Duale Rastnasen mit Klick-Verschluss & Tastern"
    )
    fig.text(0.04, 0.44, exploded_legend, color='#e2e8f0', fontsize=8.8, fontfamily='monospace',
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
