#!/usr/bin/env python3
"""
OpenMotorBridge IP67 Dummy Cartridge (Blindkassette) CAD Generator
------------------------------------------------------------------
Generates photorealistic 3D CAD visualizations for the IP67 Blind / Dummy Cartridge
(Pod_Dummy_Cartridge_IP67.stl):
  - 100% Form-identical sled body (92 x 54 x 23.5 mm)
  - Closed ergonomic faceplate (58 x 28 x 5 mm) with finger grip recess & knurling
  - Perimeter silicone/EPDM sealing gasket (IP67 / IP69K sealing against pod bay)
  - Dual side snap-fit locking latches with auto-eject interface
  - Integrated waterproof mini dry-storage compartment (Staufach 88 x 50 x 20 mm)
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

def render_dummy_cartridge_cad(output_path):
    fig = plt.figure(figsize=(20, 10), dpi=220, facecolor='#080c14')
    
    span_x = 140.0
    span_y = 74.0
    span_z = 40.0
    
    # -------------------------------------------------------------
    # 1. ISOMETRIC VIEW: IP67 BLINDKASSETTE WITH GASKET & STAUFACH
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#080c14')
    ax1.set_title("1. IP67 BLINDKASSETTE (Pod_Dummy_Cartridge_IP67.stl)\n(Formschlüssiger PA12-Verschluss, Silikon-Dichtung & Notfall-Staufach)", 
                  color='#38bdf8', fontsize=13, fontweight='bold', pad=15)
    
    # Outer Translucent Pod Housing (120x64x32mm)
    draw_box(ax1, -60, -32, -16, 120, 64, 32, color='#0284c7', alpha=0.08, edgecolor='#0284c7', linewidth=0.5)
    # Bulkhead & M8 adapter
    draw_box(ax1, -36, -28, -12, 2, 56, 24, color='#38bdf8', alpha=0.35, edgecolor='#38bdf8', linewidth=0.8)
    draw_cylinder(ax1, -60, 0, 0, 5.0, 24.0, color='#94a3b8', alpha=0.5, axis='x')
    
    # Sled Outer Body (PA12: 92x54x23.5mm)
    draw_box(ax1, -34, -27, -11.75, 92, 54, 3.0, color='#334155', alpha=0.75, edgecolor='#64748b', linewidth=0.8) # Floor
    draw_box(ax1, -34, -27, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.60, edgecolor='#64748b', linewidth=0.5) # Side 1
    draw_box(ax1, -34, 24, -11.75, 92, 3.0, 23.5, color='#334155', alpha=0.60, edgecolor='#64748b', linewidth=0.5) # Side 2
    draw_box(ax1, -34, -27, 8.75, 92, 54, 3.0, color='#334155', alpha=0.40, edgecolor='#64748b', linewidth=0.5)  # Closed Roof
    
    # Solid Front Faceplate (58x28x5mm at X = 55)
    draw_box(ax1, 55, -29, -14, 5, 58, 28, color='#1e293b', alpha=0.95, edgecolor='#38bdf8', linewidth=1.2)
    # Front Finger Grip Recess / Knurled Texture
    draw_box(ax1, 58, -18, -6, 2.5, 36, 12, color='#0f172a', alpha=0.95, edgecolor='#0284c7', linewidth=0.8)
    for gy in np.linspace(-14, 14, 8):
        draw_box(ax1, 60, gy, -4, 0.8, 1.5, 8, color='#38bdf8', alpha=0.8, edgecolor='#0284c7', linewidth=0.4)
        
    # Dual Lateral Snap-Fit Latch Buttons (on Faceplate Flanks)
    draw_box(ax1, 52, -31, -8, 6, 3, 16, color='#f59e0b', alpha=0.95, edgecolor='#fbbf24', linewidth=1.0)
    draw_box(ax1, 52, 28, -8, 6, 3, 16, color='#f59e0b', alpha=0.95, edgecolor='#fbbf24', linewidth=1.0)
    
    # Perimeter Silicone Sealing Gasket (Red EPDM O-Ring around faceplate collar at X = 53)
    draw_box(ax1, 53, -28.5, -13.5, 2.5, 57, 27, color='#ef4444', alpha=0.90, edgecolor='#b91c1c', linewidth=1.0)
    
    # Integrated Waterproof Dry-Storage Box (Interior cavity 80x46x16mm for cash / documents / tools)
    draw_box(ax1, -30, -23, -8.75, 80, 46, 17.5, color='#0284c7', alpha=0.15, edgecolor='#38bdf8', linewidth=0.8)
    # Emergency Cash / Micro Tool Representation inside cavity
    draw_box(ax1, -15, -12, -7.0, 40, 24, 4.0, color='#10b981', alpha=0.75, edgecolor='#059669', linewidth=0.8) # Stashed items
    
    # Lateral Thermal / Guide Slide Rails on Flanks
    draw_box(ax1, -30, -27.5, -4, 75, 1.0, 10, color='#cbd5e1', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax1, -30, 26.5, -4, 75, 1.0, 10, color='#cbd5e1', alpha=0.95, edgecolor='#94a3b8', linewidth=0.8)
    
    ax1.set_xlim([-70, 70])
    ax1.set_ylim([-37, 37])
    ax1.set_zlim([-20, 24])
    ax1.set_box_aspect((span_x, span_y, span_z))
    ax1.view_init(elev=24, azim=-55)
    ax1.axis('off')

    # -------------------------------------------------------------
    # 2. X-RAY / SECTION VIEW: SEALING, EJECT-SPRINGS & AIR VENT
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#080c14')
    ax2.set_title("2. SCHNITTANSICHT & DICHTUNGSKONZEPT\n(IP67 Dichtsitz, Auto-Eject Federn & ePTFE Druckausgleich)", 
                  color='#10b981', fontsize=13, fontweight='bold', pad=15)
    
    # Translucent Pod Body
    draw_box(ax2, -60, -32, -16, 120, 64, 32, color='#059669', alpha=0.08, edgecolor='#059669', linewidth=0.5)
    
    # Top ePTFE Air Vent Membrane (Ø 7 mm at X=0, Y=0, Z=16)
    draw_cylinder(ax2, 0, 0, 15.5, 3.5, 1.2, color='#ffffff', alpha=0.95, axis='z')
    
    # Rear Bulkhead with Dual Ejection Springs at X = -36
    draw_box(ax2, -36, -28, -12, 2, 56, 24, color='#10b981', alpha=0.45, edgecolor='#10b981', linewidth=0.8)
    draw_cylinder(ax2, -36, -16, 0, 2.5, 10.0, color='#fbbf24', alpha=0.95, axis='x') # Left Spring
    draw_cylinder(ax2, -36, 16, 0, 2.5, 10.0, color='#fbbf24', alpha=0.95, axis='x')  # Right Spring
    
    # Sled Section View (cut open to show solid closed front & hollow interior)
    draw_box(ax2, -34, -26, -11, 88, 52, 2.5, color='#334155', alpha=0.8, edgecolor='#64748b', linewidth=0.8) # Floor
    draw_box(ax2, -34, -26, -11, 88, 2.5, 22, color='#334155', alpha=0.6, edgecolor='#64748b', linewidth=0.5)  # Left Wall
    
    # Closed Front Faceplate & Dual Compression Gasket
    draw_box(ax2, 54, -29, -14, 6, 58, 28, color='#1e293b', alpha=0.9, edgecolor='#10b981', linewidth=1.0)
    draw_box(ax2, 52, -28, -13, 2.5, 56, 26, color='#ef4444', alpha=0.95, edgecolor='#dc2626', linewidth=1.0) # Gasket
    
    # Stash Compartment with Removable Seal Lid
    draw_box(ax2, -28, -22, -8, 76, 44, 16, color='#059669', alpha=0.25, edgecolor='#34d399', linewidth=0.8)
    draw_box(ax2, -29, -23, 7.5, 78, 46, 2.0, color='#065f46', alpha=0.85, edgecolor='#10b981', linewidth=0.8) # Lid
    
    # M8 Connector Port & Centered Pin Shroud at base
    draw_cylinder(ax2, -60, 0, 0, 5.0, 24.0, color='#94a3b8', alpha=0.6, axis='x')
    draw_box(ax2, -36, -8, -6, 6, 16, 12, color='#1e293b', alpha=0.9, edgecolor='#94a3b8', linewidth=0.8) # Shroud
    
    ax2.set_xlim([-70, 70])
    ax2.set_ylim([-37, 37])
    ax2.set_zlim([-20, 24])
    ax2.set_box_aspect((span_x, span_y, span_z))
    ax2.view_init(elev=22, azim=-65)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ IP67 Dummy Cartridge CAD generated: {output_path}")

if __name__ == "__main__":
    out1 = "/Users/schmidtm/.gemini/antigravity-ide/brain/3c459d9f-b53d-4587-ae74-c2a74bcda330/dummy_cartridge_cad.png"
    out2 = "/Users/schmidtm/openMotorBridge/hardware/cad/dummy_cartridge_cad.png"
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    render_dummy_cartridge_cad(out1)
    render_dummy_cartridge_cad(out2)
