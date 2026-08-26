#!/usr/bin/env python3
"""
OpenMotorBridge Pod 3 Full Virtual 3D Assembly CAD Generator (Close-up & Detailed)
---------------------------------------------------------------------------------
Generates high-resolution, perfectly framed 3D CAD visualizations of the
assembled Rear Pod 3 system:
 1. Mated 3D Close-up View (Pod Base + Cartridge + Pod 3 PCB)
 2. Exploded 3D Stacking View
 3. Cross-Sectional Dimensioned Clearance View
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

def render_mated_closeup(output_png):
    """Renders a tight, high-detail 3D view of the mated boards inside the translucent cartridge."""
    fig = plt.figure(figsize=(18, 11), dpi=220, facecolor='#080c14')
    ax = fig.add_subplot(111, projection='3d', facecolor='#080c14')

    # 1. POD BASE PCB (36.0 x 20.0 x 1.6 mm) — Emerald Green FR4
    draw_box(ax, -18.0, -10.0, -1.6, 36.0, 20.0, 1.6, color='#065f46', alpha=0.92, edgecolor='#10b981', linewidth=1.2)
    # M2 Mounting Holes
    draw_cylinder(ax, -15.0, 0.0, -1.8, 1.1, 2.0, color='#1e293b', alpha=1.0, axis='z')
    draw_cylinder(ax,  15.0, 0.0, -1.8, 1.1, 2.0, color='#1e293b', alpha=1.0, axis='z')
    draw_cylinder(ax, -15.0, 0.0, -0.05, 1.7, 0.1, color='#fbbf24', alpha=0.9, axis='z')
    draw_cylinder(ax,  15.0, 0.0, -0.05, 1.7, 0.1, color='#fbbf24', alpha=0.9, axis='z')

    # TVS U1 & C1 on Pod Base
    draw_box(ax, -10.0, -4.0, 0.0, 1.35, 3.5, 0.6, color='#1e293b', alpha=0.95, edgecolor='#475569', linewidth=0.6)
    draw_box(ax, -10.0,  4.0, 0.0, 1.6, 0.8, 0.8, color='#b45309', alpha=0.95, edgecolor='#d97706', linewidth=0.6)

    # 2. M8 6-PIN RECEPTACLE (Bottom of Base)
    draw_cylinder(ax, 0.0, 0.0, -12.0, 4.0, 10.4, color='#d97706', alpha=0.88, axis='z')
    draw_cylinder(ax, 0.0, 0.0, -12.0, 3.2, 1.0, color='#0f172a', alpha=0.95, axis='z')
    draw_cylinder(ax, 0.0, 0.0, -3.0, 5.0, 1.4, color='#b45309', alpha=0.95, axis='z')
    for ang in np.linspace(0, 2*np.pi, 6, endpoint=False):
        px = 1.8 * np.cos(ang)
        py = 1.8 * np.sin(ang)
        draw_cylinder(ax, px, py, -11.5, 0.35, 3.5, color='#fbbf24', alpha=1.0, axis='z')

    # 3. MATED CONNECTOR PAIR (J1 Header on Base <-> J1 Socket on Pod 3)
    # J1 SMD Pin Header Base (Z = 0.0 to 2.5 mm)
    draw_box(ax, -1.27, -7.62, 0.0, 2.54, 15.24, 2.5, color='#0f172a', alpha=0.95, edgecolor='#334155', linewidth=0.8)
    # 6 Gold Mating Pins (Z = 0.0 to 8.5 mm)
    y_pins = np.linspace(-6.35, 6.35, 6)
    for yp in y_pins:
        draw_cylinder(ax, 0.0, yp, 0.0, 0.32, 8.5, color='#fbbf24', alpha=1.0, axis='z')
        # SMD Tabs on Base
        draw_box(ax, -2.2, yp-0.5, 0.0, 4.4, 1.0, 0.2, color='#fbbf24', alpha=0.9)

    # J1 SMD Socket Header Body (Z = 2.5 to 8.5 mm)
    draw_box(ax, -1.5, -7.8, 2.5, 3.0, 15.6, 6.0, color='#1e293b', alpha=0.88, edgecolor='#0284c7', linewidth=1.0)

    # 4. REAR POD 3 SENSOR PCB (48.0 x 32.0 x 1.6 mm, Z = 8.5 to 10.1 mm)
    draw_box(ax, -24.0, -16.0, 8.5, 48.0, 32.0, 1.6, color='#047857', alpha=0.88, edgecolor='#34d399', linewidth=1.5)
    for cx in [-21.0, 21.0]:
        for cy in [-13.0, 13.0]:
            draw_cylinder(ax, cx, cy, 8.5, 1.5, 1.6, color='#fbbf24', alpha=0.9, axis='z')
            draw_cylinder(ax, cx, cy, 8.4, 1.0, 1.8, color='#0f172a', alpha=1.0, axis='z')

    # ESP32-S3 Module (U1: Z = 10.1 to 13.3 mm)
    draw_box(ax, -20.0, -12.75, 10.1, 18.0, 25.5, 2.8, color='#94a3b8', alpha=0.92, edgecolor='#cbd5e1', linewidth=1.0)
    draw_box(ax, -2.0, -12.75, 10.1, 5.0, 25.5, 0.8, color='#022c22', alpha=0.95, edgecolor='#059669', linewidth=0.8)
    for my in np.linspace(-11.0, 11.0, 8):
        draw_box(ax, -1.5, my, 10.9, 4.0, 0.6, 0.05, color='#fbbf24', alpha=1.0)

    # LSM6DSOX IMU (U2)
    draw_box(ax, 7.0, -8.0, 10.1, 2.5, 3.0, 0.86, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=0.8)

    # VL53L4CD ToF Distance Sensor (U3)
    draw_box(ax, 14.0, -1.2, 10.1, 4.4, 2.4, 1.0, color='#18181b', alpha=0.95, edgecolor='#f43f5e', linewidth=1.0)
    draw_cylinder(ax, 15.0, 0.0, 11.1, 0.5, 0.05, color='#38bdf8', alpha=0.9, axis='z')
    draw_cylinder(ax, 17.0, 0.0, 11.1, 0.6, 0.05, color='#38bdf8', alpha=0.9, axis='z')

    # WS2812B RGB Status LED (D1)
    draw_box(ax, 8.0, 6.0, 10.1, 2.0, 2.0, 0.7, color='#ffffff', alpha=0.95, edgecolor='#a855f7', linewidth=0.8)
    draw_cylinder(ax, 9.0, 7.0, 10.8, 0.6, 0.05, color='#22c55e', alpha=1.0, axis='z')

    # High-Power Brake Light LED Array (D2)
    for by in np.linspace(-10.0, 10.0, 4):
        draw_box(ax, 20.0, by-1.0, 10.1, 2.0, 2.0, 0.8, color='#ef4444', alpha=0.95, edgecolor='#f87171', linewidth=0.8)
        draw_cylinder(ax, 21.0, by, 10.9, 0.5, 0.1, color='#ff0000', alpha=0.8, axis='z')

    # 5. TRANSLUCENT CARTRIDGE TRAY (Wechselkassette: 54.0 x 36.0 x 14.0 mm)
    draw_box(ax, -26.0, -18.0, 1.5, 52.0, 36.0, 13.0, color='#3b82f6', alpha=0.12, edgecolor='#60a5fa', linewidth=0.9)
    # Optical Rear Window at +X
    draw_box(ax, 25.5, -13.0, 7.5, 0.8, 26.0, 6.5, color='#e0f2fe', alpha=0.35, edgecolor='#38bdf8', linewidth=1.2)

    # 6. TRANSLUCENT BULKHEAD & OUTER ENCLOSURE
    draw_box(ax, -28.0, -20.0, -9.0, 60.0, 40.0, 24.0, color='#0284c7', alpha=0.07, edgecolor='#0369a1', linewidth=1.0)

    # Annotations positioned clearly
    callouts = [
        ("M8 6-Pin IP67 Panel Receptacle (J2)\n[Bottom Base]", (0, -4, -12), (0, -28, -14)),
        ("Pod Base PCB (36x20mm)\nDual-SMD Architecture", (-18, -10, -1.6), (-28, -26, -3)),
        ("6-Pin Mating Connector (J1)\nSMD Header <-> SMD Socket (8.5mm)", (0, 7.6, 5.0), (-16, 26, 6)),
        ("Rear Pod 3 Sensor PCB (48x32mm)\nDual-Layer Sensor Motherboard", (24, -16, 9.3), (32, -26, 10)),
        ("ESP32-S3 RF Module (U1)\nDual-Core 240MHz, 16MB Flash", (-10, 0, 13.0), (-24, 26, 20)),
        ("VL53L4CD ToF Distance Sensor\n& Brake Light Array", (21, 0, 11.0), (32, 22, 18)),
        ("Removable Cartridge Shell\n(Tool-Free Slide Tray)", (26, 18, 13.0), (28, 28, 12)),
    ]

    for label, target, pos in callouts:
        ax.text(pos[0], pos[1], pos[2], label, color='#38bdf8', fontsize=8.5,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#0b1329', edgecolor='#0284c7', alpha=0.92, lw=0.9),
                ha='center', va='center', weight='bold')
        ax.plot([target[0], pos[0]], [target[1], pos[1]], [target[2], pos[2]], color='#38bdf8', linestyle='--', linewidth=1.0, alpha=0.75)

    # Titles
    fig.text(0.5, 0.95, "OPENMOTORBRIDGE // REAR POD 3 FULL 3D ASSEMBLY",
             ha='center', va='top', fontsize=16, color='#f8fafc', weight='heavy', family='sans-serif')
    fig.text(0.5, 0.915, "Pod Base PCB (openmotorbridge_pod_base)  ◄►  Interchangeable Sensor Cartridge (openmotorbridge_rear_pod3)",
             ha='center', va='top', fontsize=11, color='#38bdf8', weight='bold', family='sans-serif')

    specs = (
        "MECHANICAL INTERFACE SPECS:\n"
        "• Pod Base PCB: 36.0 x 20.0 x 1.6 mm\n"
        "• Rear Pod 3 PCB: 48.0 x 32.0 x 1.6 mm\n"
        "• Stacking Height: 8.50 mm (SMD Header/Socket)\n"
        "• Enclosure Profile: 60 x 40 x 24 mm (IP67)\n"
        "• Sensor Aperture: Sealed Polycarbonate Window"
    )
    fig.text(0.04, 0.08, specs, fontsize=8.5, color='#94a3b8', family='monospace',
             bbox=dict(boxstyle='square,pad=0.6', facecolor='#090d16', edgecolor='#1e293b', alpha=0.95, lw=1.0))

    ax.set_xlim(-34, 38)
    ax.set_ylim(-32, 32)
    ax.set_zlim(-16, 24)
    ax.set_axis_off()
    ax.view_init(elev=26, azim=-55)

    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Saved Close-up 3D Mated render to {output_png}")

def render_cross_section_view(output_png):
    """Renders a dimensioned 2D/3D Cross-Sectional View showing vertical stack-up clearances."""
    fig, ax = plt.subplots(figsize=(16, 9), dpi=220, facecolor='#080c14')
    ax.set_facecolor('#080c14')

    # Y-axis is Z-Height (mm), X-axis is Length (mm along X: -35 to +35 mm)
    # Background Grid
    ax.grid(True, linestyle=':', color='#1e293b', alpha=0.6)

    # 1. Outer Pod Housing Wall (-Z to +Z)
    # Bottom Wall (Z = -10 to -7 mm)
    ax.fill_between([-32, 32], -10, -7, color='#0369a1', alpha=0.25, label='Outer Enclosure (MJF PA12)')
    ax.plot([-32, 32, 32, -32, -32], [-10, -10, -7, -7, -10], color='#0284c7', lw=1.2)

    # Top Roof Wall (Z = +14 to +17 mm)
    ax.fill_between([-32, 32], 14, 17, color='#0369a1', alpha=0.25)
    ax.plot([-32, 32, 32, -32, -32], [14, 14, 17, 17, 14], color='#0284c7', lw=1.2)

    # 2. M8 6-Pin Panel Receptacle (Centered at X=0, Z = -16 to -1.6 mm)
    ax.fill_between([-4, 4], -16, -1.6, color='#d97706', alpha=0.85, label='M8 6-Pin IP67 Receptacle')
    ax.plot([-4, 4, 4, -4, -4], [-16, -16, -1.6, -1.6, -16], color='#b45309', lw=1.5)
    # M8 Flange Nut
    ax.fill_between([-5.5, 5.5], -7, -5, color='#b45309', alpha=0.95)

    # 3. Pod Base PCB (X = -18 to +18 mm, Z = -1.6 to 0.0 mm)
    ax.fill_between([-18, 18], -1.6, 0.0, color='#065f46', alpha=0.95, label='Pod Base PCB (openmotorbridge_pod_base: 36x20mm)')
    ax.plot([-18, 18, 18, -18, -18], [-1.6, -1.6, 0.0, 0.0, -1.6], color='#10b981', lw=1.8)

    # TVS Protection U1 & C1
    ax.fill_between([-11, -8.5], 0.0, 0.8, color='#334155', alpha=0.95)
    ax.text(-9.75, 1.2, "TVS Array\n(SP3012)", color='#94a3b8', fontsize=7.5, ha='center')

    # 4. Connector Pair (J1: X = -1.5 to +1.5 mm, Z = 0.0 to 8.5 mm)
    # SMD Pin Header Base (Z = 0.0 to 2.5 mm)
    ax.fill_between([-1.3, 1.3], 0.0, 2.5, color='#0f172a', alpha=0.95, label='SMD Pin Header (J1 Plug, Base PCB)')
    ax.plot([-1.3, 1.3, 1.3, -1.3, -1.3], [0.0, 0.0, 2.5, 2.5, 0.0], color='#64748b', lw=1.0)
    # Gold Contact Pins (Z = 2.5 to 8.5 mm)
    ax.fill_between([-0.4, 0.4], 2.5, 8.5, color='#fbbf24', alpha=1.0, label='6x Gold Pins (Mating Interface)')
    # SMD Socket Receptacle Body (Z = 2.5 to 8.5 mm)
    ax.fill_between([-1.6, -0.4], 2.5, 8.5, color='#1e293b', alpha=0.9)
    ax.fill_between([0.4, 1.6], 2.5, 8.5, color='#1e293b', alpha=0.9)
    ax.plot([-1.6, 1.6, 1.6, -1.6, -1.6], [2.5, 2.5, 8.5, 8.5, 2.5], color='#0284c7', lw=1.0)

    # 5. Rear Pod 3 Sensor PCB (X = -24 to +24 mm, Z = 8.5 to 10.1 mm)
    ax.fill_between([-24, 24], 8.5, 10.1, color='#047857', alpha=0.95, label='Rear Pod 3 PCB (openmotorbridge_rear_pod3: 48x32mm)')
    ax.plot([-24, 24, 24, -24, -24], [8.5, 8.5, 10.1, 10.1, 8.5], color='#34d399', lw=1.8)

    # ESP32-S3 Module (X = -20 to -2 mm, Z = 10.1 to 13.3 mm)
    ax.fill_between([-20, -2], 10.1, 13.3, color='#94a3b8', alpha=0.95, label='ESP32-S3-WROOM-1 Module')
    ax.plot([-20, -2, -2, -20, -20], [10.1, 10.1, 13.3, 13.3, 10.1], color='#cbd5e1', lw=1.2)
    ax.text(-11.0, 11.7, "ESP32-S3 MCU (3.2mm)", color='#0f172a', fontsize=8, weight='bold', ha='center', va='center')

    # ToF Sensor & Brake LEDs (X = +12 to +23 mm, Z = 10.1 to 11.1 mm)
    ax.fill_between([12, 18], 10.1, 11.1, color='#e11d48', alpha=0.95)
    ax.fill_between([19, 23], 10.1, 11.1, color='#ef4444', alpha=0.95)
    ax.text(17.5, 12.0, "ToF + Brake LEDs", color='#f43f5e', fontsize=8, weight='bold', ha='center')

    # Removable Cartridge Tray Shell (Z = 1.0 to 14.0 mm)
    ax.plot([-26, -26, 26, 26], [1.0, 14.0, 14.0, 1.0], color='#38bdf8', linestyle='--', lw=1.5, label='Wechselkassette Shell')

    # Dimension Arrows & Markers
    # 1. Mating Stacking Height (8.50 mm)
    ax.annotate('', xy=(2.5, 8.5), xytext=(2.5, 0.0),
                arrowprops=dict(arrowstyle='<->', color='#fbbf24', lw=1.5))
    ax.text(3.2, 4.25, "Stacking Height: 8.50 mm", color='#fbbf24', fontsize=9, weight='bold', va='center')

    # 2. ESP32 Clearance to Roof (0.70 mm)
    ax.annotate('', xy=(-11, 14.0), xytext=(-11, 13.3),
                arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=1.2))
    ax.text(-11, 13.65, "  0.70 mm Air Gap", color='#38bdf8', fontsize=8, va='center')

    # 3. Overall Height
    ax.annotate('', xy=(-34, 17.0), xytext=(-34, -10.0),
                arrowprops=dict(arrowstyle='<->', color='#f8fafc', lw=1.5))
    ax.text(-35, 3.5, "Total Enclosure Height: 27.0 mm", color='#f8fafc', fontsize=9, weight='bold', ha='right', va='center', rotation=90)

    # Titles & Legend
    ax.set_title("OPENMOTORBRIDGE // REAR POD 3 VERTICAL STACK-UP CROSS SECTION", fontsize=15, color='#f8fafc', weight='bold', pad=20)
    ax.set_xlabel("X Position [mm] (Length along Module)", fontsize=11, color='#94a3b8', labelpad=10)
    ax.set_ylabel("Z Height [mm] (Vertical Stacking)", fontsize=11, color='#94a3b8', labelpad=10)

    ax.set_xlim(-42, 42)
    ax.set_ylim(-18, 20)
    ax.tick_params(colors='#94a3b8')

    leg = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=True, facecolor='#090d16', edgecolor='#1e293b', fontsize=8.5)
    for text in leg.get_texts():
        text.set_color('#cbd5e1')

    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=220, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved Cross-Section CAD render to {output_png}")

if __name__ == '__main__':
    mated_out = os.path.join(output_dir, "pod3_assembly_mated_closeup.png")
    section_out = os.path.join(output_dir, "pod3_assembly_cross_section.png")
    render_mated_closeup(mated_out)
    render_cross_section_view(section_out)
