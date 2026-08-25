#!/usr/bin/env python3
"""
OpenMotorBridge Modular Cartridge Variants CAD Generator
--------------------------------------------------------
Generates high-precision, photorealistic 3D CAD visualizations for the three
primary swappable cartridge configurations inside the 120x64x32mm Universal Pod:
  1. Sena 50S / 60S Quick-Snap Cradle (3D Contour Negative Nest, JST-SH Routing & Top EPDM Strap)
  2. Cardo Packtalk Edge / Pro Magnetic Air Mount (Contour Bedding, JST-SH Routing & Dual N52)
  3. Midland BTR1 / XT30 Slide & PMR Inlay (Dovetail Rail, JST-SH Routing & EPDM Strap)
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

def draw_strap_arc(ax, x_center, y_min, y_max, z_peak, thickness, width, color='#f43f5e', alpha=0.9):
    """Draws an elastic rubber strap arching over the device."""
    y = np.linspace(y_min, y_max, 24)
    h = z_peak
    z = h - 4.0 * (h - 2.0) * ((y - (y_min + y_max)/2.0) / (y_max - y_min))**2
    
    for i in range(len(y)-1):
        draw_box(ax, x_center - width/2.0, y[i], z[i], width, y[i+1]-y[i], thickness, 
                 color=color, alpha=alpha, edgecolor='#be123c', linewidth=0.6)

def render_trio_cartridge_cad(output_path):
    fig = plt.figure(figsize=(26, 10), dpi=220, facecolor='#080c14')
    
    span_x = 140.0
    span_y = 74.0
    span_z = 40.0
    
    # -------------------------------------------------------------
    # 1. SENA 50S / 60S QUICK-SNAP + CONTOUR NEST + EPDM STRAP
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(131, projection='3d', facecolor='#080c14')
    ax1.set_title("1. SENA 50S / 60S KONTUR-NEST & JST-SH KABELFÜHRUNG\n(3D-Negativboden, JST-SH Flexkanal zu Pogo-Array & EPDM-Lasche)", 
                  color='#38bdf8', fontsize=12, fontweight='bold', pad=15)
    
    # Outer Translucent Pod Housing (120x64x32mm)
    draw_box(ax1, -60, -32, -16, 120, 64, 32, color='#0284c7', alpha=0.08, edgecolor='#0284c7', linewidth=0.5)
    # Bulkhead & M8 adapter
    draw_box(ax1, -36, -28, -12, 2, 56, 24, color='#38bdf8', alpha=0.35, edgecolor='#38bdf8', linewidth=0.8)
    draw_cylinder(ax1, -60, 0, 0, 5.0, 24.0, color='#94a3b8', alpha=0.5, axis='x')
    
    # Base Sled (PA12: 92x54x23.5mm)
    draw_box(ax1, -34, -27, -11.75, 92, 54, 3.0, color='#475569', alpha=0.55, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax1, -34, -27, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax1, -34, 24, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax1, 55, -29, -14, 5, 58, 28, color='#0284c7', alpha=0.7, edgecolor='#38bdf8', linewidth=1.0)
    
    # Carrier PCB on floor (60x36mm at X = -18..+42, Y = -18..+18)
    draw_box(ax1, -18, -18, -8.75, 60, 36, 1.2, color='#047857', alpha=0.9, edgecolor='#10b981', linewidth=0.8)
    
    # J2 Header (JST-SH 1.0mm 6-Pin Horizontal on PCB at X = 32, Y = -4)
    draw_box(ax1, 30, -5, -7.55, 6, 10, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#94a3b8', linewidth=0.8)
    
    # Form-Fit 3D Contour Negative Nest (Schwingungsgedämpftes TPU-Formbett, 80x48x7mm)
    draw_box(ax1, -28, -24, -7.55, 80, 48, 7.0, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=1.0)
    # Recessed nesting pocket for Sena curve
    draw_box(ax1, -25, -22, -4.55, 74, 44, 4.0, color='#0f172a', alpha=0.95, edgecolor='#38bdf8', linewidth=0.8)
    
    # Under-Bed Cable Channel & JST-SH Ribbon (runs from J2 at X=30 along -Y to Pogo Array at X=-22)
    draw_box(ax1, -22, -14, -6.55, 54, 4, 1.2, color='#ec4899', alpha=0.95, edgecolor='#f43f5e', linewidth=0.6) # Ribbon Cable
    
    # Sena Spring-Loaded Gold Pogo Contact Array (7 pins at X = -22)
    for py in np.linspace(-12, 12, 7):
        draw_cylinder(ax1, -22, py, -1.55, 0.9, 3.5, color='#fbbf24', alpha=1.0, axis='z')
        
    # Sena Lower Anchor Lip (Bottom Hook at X = -25)
    draw_box(ax1, -26, -16, 2.45, 5, 32, 4.0, color='#0ea5e9', alpha=0.95, edgecolor='#38bdf8', linewidth=1.0)
    
    # Sena Top Spring Release Latch (POM button at X = 42)
    draw_box(ax1, 42, -12, 2.45, 7, 24, 5.0, color='#f59e0b', alpha=0.95, edgecolor='#fbbf24', linewidth=1.0)
    
    # Sena 50S Ghost Dummy Body (84x48x18mm seated in contour pocket)
    draw_box(ax1, -24, -22, 0.45, 72, 44, 18, color='#3b82f6', alpha=0.22, edgecolor='#60a5fa', linewidth=1.2)
    
    # EPDM Rubber Retention Strap
    draw_strap_arc(ax1, x_center=12.0, y_min=-26.0, y_max=26.0, z_peak=20.5, thickness=2.2, width=12.0, color='#ef4444', alpha=0.95)
    draw_cylinder(ax1, 12.0, -27.0, 4.0, 2.0, 3.0, color='#94a3b8', alpha=1.0, axis='y')
    draw_cylinder(ax1, 12.0, 24.0, 4.0, 2.0, 3.0, color='#94a3b8', alpha=1.0, axis='y')
    
    # 6-Pin Socket Header at leading edge (X = -34)
    draw_box(ax1, -34, -10, -8.75, 8, 20, 5, color='#e2e8f0', alpha=0.9, edgecolor='#cbd5e1', linewidth=0.8)
    
    ax1.set_xlim([-70, 70])
    ax1.set_ylim([-37, 37])
    ax1.set_zlim([-20, 24])
    ax1.set_box_aspect((span_x, span_y, span_z))
    ax1.view_init(elev=24, azim=-55)
    ax1.axis('off')

    # -------------------------------------------------------------
    # 2. CARDO PACKTALK EDGE / PRO MAGNETIC AIR MOUNT + ROUTING
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(132, projection='3d', facecolor='#080c14')
    ax2.set_title("2. CARDO PACKTALK EDGE AIR MOUNT & KABELFÜHRUNG\n(3D-Negativboden, JST-SH Flexkanal zu Air-Mount-Pads & Dual-N52)", 
                  color='#10b981', fontsize=12, fontweight='bold', pad=15)
    
    # Outer Translucent Pod Housing (120x64x32mm)
    draw_box(ax2, -60, -32, -16, 120, 64, 32, color='#059669', alpha=0.08, edgecolor='#059669', linewidth=0.5)
    # Bulkhead & M8 adapter
    draw_box(ax2, -36, -28, -12, 2, 56, 24, color='#10b981', alpha=0.35, edgecolor='#10b981', linewidth=0.8)
    draw_cylinder(ax2, -60, 0, 0, 5.0, 24.0, color='#94a3b8', alpha=0.5, axis='x')
    
    # Base Sled (PA12: 92x54x23.5mm)
    draw_box(ax2, -34, -27, -11.75, 92, 54, 3.0, color='#475569', alpha=0.55, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax2, -34, -27, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax2, -34, 24, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax2, 55, -29, -14, 5, 58, 28, color='#059669', alpha=0.7, edgecolor='#34d399', linewidth=1.0)
    
    # Carrier PCB (60x36mm)
    draw_box(ax2, -18, -18, -8.75, 60, 36, 1.2, color='#047857', alpha=0.9, edgecolor='#10b981', linewidth=0.8)
    
    # J2 Header (JST-SH 1.0mm 6-Pin Horizontal on PCB at X = 30, Y = -5)
    draw_box(ax2, 30, -5, -7.55, 6, 10, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#94a3b8', linewidth=0.8)
    
    # Cardo Air Mount 3D Contour Nest (74x46x7mm)
    draw_box(ax2, -24, -23, -7.55, 74, 46, 7.0, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=1.0)
    draw_box(ax2, -21, -21, -4.55, 68, 42, 4.0, color='#0f172a', alpha=0.95, edgecolor='#10b981', linewidth=0.8)
    
    # Under-Bed Cable Channel & JST-SH Ribbon (runs from J2 at X=30 to Air Mount Pads at X=9)
    draw_box(ax2, 9, -5, -6.55, 23, 4, 1.2, color='#ec4899', alpha=0.95, edgecolor='#f43f5e', linewidth=0.6)
    
    # Dual Embedded N52 Neodymium Disc Magnets (Ø8x2mm)
    draw_cylinder(ax2, -6, 0, -2.55, 4.0, 2.0, color='#e11d48', alpha=0.95, axis='z')
    draw_cylinder(ax2, 24, 0, -2.55, 4.0, 2.0, color='#e11d48', alpha=0.95, axis='z')
    
    # Cardo 5-Pin Spring Contact Array (at X = 9)
    for py in np.linspace(-8, 8, 5):
        draw_cylinder(ax2, 9, py, -2.55, 0.8, 3.5, color='#fbbf24', alpha=1.0, axis='z')
        
    # Dual Lateral Snap-Lock Jaws
    draw_box(ax2, -2, -23, -1.55, 22, 3.0, 7.0, color='#10b981', alpha=0.95, edgecolor='#34d399', linewidth=1.0)
    draw_box(ax2, -2, 20, -1.55, 22, 3.0, 7.0, color='#10b981', alpha=0.95, edgecolor='#34d399', linewidth=1.0)
    
    # Cardo Packtalk Edge Ghost Dummy
    draw_box(ax2, -22, -21, 0.45, 70, 42, 16, color='#10b981', alpha=0.22, edgecolor='#34d399', linewidth=1.2)
    
    # EPDM Rubber Retention Strap
    draw_strap_arc(ax2, x_center=10.0, y_min=-26.0, y_max=26.0, z_peak=18.5, thickness=2.2, width=10.0, color='#10b981', alpha=0.85)
    
    # 6-Pin Socket Header
    draw_box(ax2, -34, -10, -8.75, 8, 20, 5, color='#e2e8f0', alpha=0.9, edgecolor='#cbd5e1', linewidth=0.8)
    
    ax2.set_xlim([-70, 70])
    ax2.set_ylim([-37, 37])
    ax2.set_zlim([-20, 24])
    ax2.set_box_aspect((span_x, span_y, span_z))
    ax2.view_init(elev=24, azim=-55)
    ax2.axis('off')

    # -------------------------------------------------------------
    # 3. MIDLAND BTR1 & XT30 SLIDE / BARE-PCB CRADLE + ROUTING
    # -------------------------------------------------------------
    ax3 = fig.add_subplot(133, projection='3d', facecolor='#080c14')
    ax3.set_title("3. MIDLAND BTR1 & XT30 KONTUR & KABELFÜHRUNG\n(3D-Negativbett, JST-SH Kabelkanal zu PMR-Lötpads / SMA & Lasche)", 
                  color='#f59e0b', fontsize=12, fontweight='bold', pad=15)
    
    # Outer Translucent Pod Housing (120x64x32mm)
    draw_box(ax3, -60, -32, -16, 120, 64, 32, color='#d97706', alpha=0.08, edgecolor='#d97706', linewidth=0.5)
    # Bulkhead & M8 adapter
    draw_box(ax3, -36, -28, -12, 2, 56, 24, color='#f59e0b', alpha=0.35, edgecolor='#f59e0b', linewidth=0.8)
    draw_cylinder(ax3, -60, 0, 0, 5.0, 24.0, color='#94a3b8', alpha=0.5, axis='x')
    
    # Base Sled (PA12: 92x54x23.5mm)
    draw_box(ax3, -34, -27, -11.75, 92, 54, 3.0, color='#475569', alpha=0.55, edgecolor='#94a3b8', linewidth=0.8)
    draw_box(ax3, -34, -27, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax3, -34, 24, -11.75, 92, 3.0, 23.5, color='#475569', alpha=0.30, edgecolor='#94a3b8', linewidth=0.5)
    draw_box(ax3, 55, -29, -14, 5, 58, 28, color='#d97706', alpha=0.7, edgecolor='#fbbf24', linewidth=1.0)
    
    # Carrier PCB (60x36mm)
    draw_box(ax3, -18, -18, -8.75, 60, 36, 1.2, color='#047857', alpha=0.9, edgecolor='#10b981', linewidth=0.8)
    
    # J2 Header (JST-SH 1.0mm 6-Pin Horizontal on PCB at X = 30, Y = -5)
    draw_box(ax3, 30, -5, -7.55, 6, 10, 1.8, color='#f8fafc', alpha=1.0, edgecolor='#94a3b8', linewidth=0.8)
    
    # Form-Fit 3D Contour Negative Nest for Midland PCB / Intercom (76x46x7mm)
    draw_box(ax3, -24, -23, -7.55, 76, 46, 7.0, color='#1e293b', alpha=0.95, edgecolor='#64748b', linewidth=1.0)
    draw_box(ax3, -21, -21, -4.55, 70, 42, 4.0, color='#0f172a', alpha=0.95, edgecolor='#f59e0b', linewidth=0.8)
    
    # Under-Bed Cable Channel & JST-SH Wiring Harness (runs from J2 at X=30 to Bare Board pads at X=8)
    draw_box(ax3, 8, -5, -6.55, 24, 4, 1.2, color='#ec4899', alpha=0.95, edgecolor='#f43f5e', linewidth=0.6)
    
    # Midland XT30 / Compact PMR446 Bare-Board Inlay (64x38x3mm)
    draw_box(ax3, -18, -19, -4.0, 64, 38, 3.0, color='#065f46', alpha=0.85, edgecolor='#10b981', linewidth=1.0)
    draw_box(ax3, -6, -11, -1.0, 24, 22, 5.0, color='#334155', alpha=0.9, edgecolor='#64748b', linewidth=0.8)
    
    # 4-Point Silicone Dampened PCB Clamping Posts (4x M2 standoffs)
    for cx in [-15, 38]:
        for cy in [-16, 16]:
            draw_cylinder(ax3, cx, cy, -7.55, 2.0, 6.0, color='#94a3b8', alpha=0.9, axis='z')
            
    # Dovetail Slide Guide Rail
    draw_box(ax3, -22, -15, 2.45, 68, 3.0, 4.0, color='#f59e0b', alpha=0.9, edgecolor='#fbbf24', linewidth=0.8)
    draw_box(ax3, -22, 12, 2.45, 68, 3.0, 4.0, color='#f59e0b', alpha=0.9, edgecolor='#fbbf24', linewidth=0.8)
    
    # PMR446 Internal Helical Antenna Coil (Ø6 x 32mm copper coil along X)
    draw_cylinder(ax3, -3, 17, 4.45, 3.0, 32.0, color='#b45309', alpha=0.9, axis='x')
    
    # Optional SMA Front Jack on Faceplate
    draw_cylinder(ax3, 56, 16, 0, 3.2, 8.0, color='#fbbf24', alpha=0.95, axis='x')
    
    # EPDM Rubber Retention Strap
    draw_strap_arc(ax3, x_center=12.0, y_min=-26.0, y_max=26.0, z_peak=16.5, thickness=2.2, width=12.0, color='#f59e0b', alpha=0.95)
    
    # 6-Pin Socket Header
    draw_box(ax3, -34, -10, -8.75, 8, 20, 5, color='#e2e8f0', alpha=0.9, edgecolor='#cbd5e1', linewidth=0.8)
    
    ax3.set_xlim([-70, 70])
    ax3.set_ylim([-37, 37])
    ax3.set_zlim([-20, 24])
    ax3.set_box_aspect((span_x, span_y, span_z))
    ax3.view_init(elev=24, azim=-55)
    ax3.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Trio Cartridge CAD with JST-SH Routing & Contour Nest generated: {output_path}")

if __name__ == "__main__":
    out1 = "/Users/schmidtm/.gemini/antigravity-ide/brain/3c459d9f-b53d-4587-ae74-c2a74bcda330/cartridge_variants_trio.png"
    out2 = "/Users/schmidtm/openMotorBridge/hardware/cad/cartridge_variants_trio.png"
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    render_trio_cartridge_cad(out1)
    render_trio_cartridge_cad(out2)
