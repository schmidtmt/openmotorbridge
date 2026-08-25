#!/usr/bin/env python3
"""
OpenMotorBridge Wiring Harness (Kabelbaum) Technical Illustration Generator
---------------------------------------------------------------------------
Generates a high-resolution, photorealistic engineering diagram and topology sketch
of the modular OpenMotorBridge wiring harness:
  - HD26 SEAL-D waterproof D-Sub main connector at Central Control Box
  - Braided main trunk cable with molded IP67 Y-breakout junction (Formmuffe)
  - Branch 1 (Pod 1 Links - Sena / Audio 1): M8 6-Pin A-coded female (Yellow)
  - Branch 2 (Pod 2 Rechts - Cardo / Audio 2): M8 6-Pin A-coded female (Cyan)
  - Branch 3 (Pod 3 Heck - GNSS & LoRa Mesh): M8 6-Pin A-coded female (Purple)
  - Branch 4 (Bordnetz 12V / Power): Inline Fuse (KL30), KL15, Ring Terminals (Red/Black)
  - Branch 5 (CAN-Bus & Aux / Telemetrie): M8 4-Pin A-coded female (Green)
  - Full DIN 72551 wire color code, AWG gauge, and pinout breakdown tables.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def draw_bezier_cable(ax, p0, p1, p2, p3, width=8, color='#1e293b', edge_color='#38bdf8', alpha=0.9, n_points=100):
    """Draws a smooth braided cable along a cubic Bezier curve."""
    t = np.linspace(0, 1, n_points)
    # Cubic Bezier formula: B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3
    bx = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
    by = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
    
    # Outer glow / shield
    ax.plot(bx, by, color=edge_color, linewidth=width+3, alpha=alpha*0.4, solid_capstyle='round', zorder=2)
    # Main cable sheath
    ax.plot(bx, by, color=color, linewidth=width, alpha=alpha, solid_capstyle='round', zorder=3)
    # Highlight texture line (braided look)
    ax.plot(bx, by, color='#64748b', linewidth=width*0.25, linestyle=':', alpha=0.7, zorder=4)
    return bx, by

def draw_m8_connector(ax, x, y, label, sublabel, color_code, angle_deg=0, is_4pin=False):
    """Draws a detailed M8 circular connector with knurled metal nut and colored identification band."""
    # Transform coordinates based on angle
    rad = np.radians(angle_deg)
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    
    # Metal Body (Silver / Dark Steel)
    body = patches.Rectangle((x-18, y-10), 36, 20, facecolor='#334155', edgecolor='#94a3b8', linewidth=1.2, zorder=5)
    ax.add_patch(body)
    
    # Knurled Coupling Nut (Gerändelte Überwurfmutter)
    for kx in np.linspace(x-14, x+14, 8):
        ax.plot([kx, kx], [y-10, y+10], color='#cbd5e1', linewidth=1.0, zorder=6)
    
    # Color-coded Identification Ring (Farbcodierter Kennring)
    ring = patches.Rectangle((x-22, y-8), 6, 16, facecolor=color_code, edgecolor='#ffffff', linewidth=0.8, zorder=7)
    ax.add_patch(ring)
    
    # Strain Relief Boot (Knickschutztülle)
    boot = patches.Polygon([[x-22, y-6], [x-32, y-4], [x-32, y+4], [x-22, y+6]], 
                           facecolor='#0f172a', edgecolor='#475569', linewidth=1.0, zorder=4)
    ax.add_patch(boot)
    
    # M8 Circular Socket Face (Steckgesicht)
    socket_face = patches.Circle((x+24, y), 9, facecolor='#0f172a', edgecolor='#cbd5e1', linewidth=1.5, zorder=8)
    ax.add_patch(socket_face)
    
    # Polarization Keyway (Kodiernase)
    ax.plot([x+24, x+24], [y+5, y+9], color='#38bdf8', linewidth=2.0, zorder=9)
    
    # Gold Pins (Vergoldete Kontaktbuchsen)
    num_pins = 4 if is_4pin else 6
    r_pin = 4.5
    for i in range(num_pins):
        phi = 2 * np.pi * i / num_pins - np.pi/2
        px = x + 24 + r_pin * np.cos(phi)
        py = y + r_pin * np.sin(phi)
        pin = patches.Circle((px, py), 1.2, facecolor='#fbbf24', edgecolor='#d97706', linewidth=0.6, zorder=10)
        ax.add_patch(pin)
    
    # Labels
    ax.text(x+38, y+4, label, color='#ffffff', fontsize=11, fontweight='bold', va='center', zorder=11)
    ax.text(x+38, y-6, sublabel, color=color_code, fontsize=9, fontweight='semibold', va='center', zorder=11)

def render_wiring_harness(output_path):
    fig, ax = plt.subplots(figsize=(26, 15), dpi=220, facecolor='#080c14')
    ax.set_facecolor('#080c14')
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 600)
    ax.axis('off')
    
    # -------------------------------------------------------------
    # 1. TITLE & HEADER BAR
    # -------------------------------------------------------------
    ax.text(500, 575, "OPENMOTORBRIDGE — ZENTRALER AUTOMOTIVE-KABELBAUM (HARNESS v8.0)", 
            color='#38bdf8', fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(500, 555, "HD26 SEAL-D Hauptflansch zu 5x M8/Kfz-Modulabgängen (IP67/IP69K, DIN 72551 & ISO 6722)", 
            color='#94a3b8', fontsize=11, ha='center', va='center')
    
    # -------------------------------------------------------------
    # 2. CENTRAL CONTROL BOX (LINKS: ZENTRALBOX BASISGEHÄUSE)
    # -------------------------------------------------------------
    # Main Box 3-Piece Sandwich Housing
    box_rect = patches.FancyBboxPatch((30, 260), 140, 180, boxstyle="round,pad=4,rounding_size=8",
                                     facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2.0, zorder=2)
    ax.add_patch(box_rect)
    
    # Internal Tier Demarcations
    ax.plot([30, 170], [320, 320], color='#ef4444', linewidth=1.2, linestyle='--', zorder=3)
    ax.plot([30, 170], [380, 380], color='#ef4444', linewidth=1.2, linestyle='--', zorder=3)
    
    # Box Titles & Annotations
    ax.text(100, 425, "ZENTRALBOX", color='#38bdf8', fontsize=12, fontweight='bold', ha='center')
    ax.text(100, 408, "openmotorbridge_main_box", color='#94a3b8', fontsize=8, ha='center')
    ax.text(100, 350, "Oberwanne & Akku", color='#cbd5e1', fontsize=9, ha='center')
    ax.text(100, 290, "Unterwanne (PCB & Kühlung)", color='#10b981', fontsize=8, ha='center')
    
    # 4x M4 Silentblocks (Mounting Ears)
    for ex, ey in [(20, 270), (20, 430), (180, 270), (180, 430)]:
        ear = patches.Circle((ex, ey), 8, facecolor='#334155', edgecolor='#64748b', linewidth=1.2, zorder=3)
        hole = patches.Circle((ex, ey), 4, facecolor='#0f172a', edgecolor='#cbd5e1', linewidth=0.8, zorder=4)
        ax.add_patch(ear)
        ax.add_patch(hole)
        
    # USB-C Service Cap on Box Front
    usb_cap = patches.Circle((170, 365), 7, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.2, zorder=5)
    ax.add_patch(usb_cap)
    ax.text(180, 365, "USB-C", color='#38bdf8', fontsize=8, va='center', zorder=6)
    
    # RGB Status LED on Box Front
    led_win = patches.Circle((170, 345), 4, facecolor='#10b981', edgecolor='#ffffff', linewidth=1.0, zorder=5)
    ax.add_patch(led_win)
    ax.text(180, 345, "RGB-LED", color='#34d399', fontsize=8, va='center', zorder=6)
    
    # -------------------------------------------------------------
    # 3. HD26 D-SUB WATERPROOF PLUG & STRAIN RELIEF
    # -------------------------------------------------------------
    # HD26 Wall Flange on Box
    flange = patches.Rectangle((165, 305), 10, 30, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.5, zorder=5)
    ax.add_patch(flange)
    
    # HD26 Mating Cable Plug (Gegenstecker am Kabelbaum)
    plug_body = patches.Polygon([[175, 303], [195, 307], [210, 312], [210, 328], [195, 333], [175, 337]], 
                                facecolor='#0f172a', edgecolor='#94a3b8', linewidth=1.5, zorder=6)
    ax.add_patch(plug_body)
    # 2x Jackscrews with knurled thumbscrews
    ax.add_patch(patches.Circle((175, 305), 3, facecolor='#cbd5e1', edgecolor='#475569', linewidth=0.8, zorder=7))
    ax.add_patch(patches.Circle((175, 335), 3, facecolor='#cbd5e1', edgecolor='#475569', linewidth=0.8, zorder=7))
    
    # Rubber Strain Relief Boot
    boot_main = patches.Polygon([[210, 314], [235, 317], [235, 323], [210, 326]],
                                facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=5)
    ax.add_patch(boot_main)
    
    ax.text(195, 290, "HD26 SEAL-D (IP67)", color='#38bdf8', fontsize=9, fontweight='bold', ha='center')

    # -------------------------------------------------------------
    # 4. MAIN TRUNK CABLE (HAUPTSTAMM: 26-POLIG GEBÜNDELT)
    # -------------------------------------------------------------
    # Main shielded braided trunk (from X=235, Y=320 to X=420, Y=320)
    draw_bezier_cable(ax, (235, 320), (290, 320), (350, 320), (420, 320), width=16, color='#0f172a', edge_color='#38bdf8')
    
    # Heat Shrink Label / Banderole
    label_patch = patches.Rectangle((270, 310), 100, 20, facecolor='#334155', edgecolor='#f59e0b', linewidth=1.0, zorder=6)
    ax.add_patch(label_patch)
    ax.text(320, 320, "OPENMOTORBRIDGE HARNESS v8.0\n[26x AWG24/28 PUR / SHIELDED]", 
            color='#fbbf24', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=7)

    # -------------------------------------------------------------
    # 5. MOLDED IP67 Y-BREAKOUT JUNCTION (AUTOMOTIVE FORMMUFFE)
    # -------------------------------------------------------------
    # Molded distribution hub where 26 wires split into 5 branches
    hub = patches.Polygon([[420, 310], [450, 295], [470, 275], [470, 365], [450, 345], [420, 330]], 
                          facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2.0, zorder=5)
    ax.add_patch(hub)
    ax.text(445, 320, "IP67\nFORMMUFFE\n(Y-HUB)", color='#38bdf8', fontsize=8, fontweight='bold', ha='center', va='center', zorder=6)

    # -------------------------------------------------------------
    # 6. FIVE MODULAR BRANCH CABLES & CONNECTORS
    # -------------------------------------------------------------
    
    # -------------------------------------------------------------
    # BRANCH 1: POD 1 LINKS (SENA / AUDIO 1) -> M8 6-Pin (Yellow)
    # -------------------------------------------------------------
    draw_bezier_cable(ax, (470, 355), (550, 420), (620, 480), (700, 480), width=9, color='#0f172a', edge_color='#f59e0b')
    draw_m8_connector(ax, 720, 480, "POD 1 (LINKS - SENA APEX / SPIDER)", 
                      "M8 6-Pin Buchse | VCC, GND, NF_P/N (Symmetrisch), OPTO, 1-Wire ID", '#f59e0b')
    
    # -------------------------------------------------------------
    # BRANCH 2: POD 2 RECHTS (CARDO / AUDIO 2) -> M8 6-Pin (Cyan)
    # -------------------------------------------------------------
    draw_bezier_cable(ax, (470, 335), (550, 370), (620, 400), (700, 400), width=9, color='#0f172a', edge_color='#06b6d4')
    draw_m8_connector(ax, 720, 400, "POD 2 (RECHTS - CARDO PACKTALK / PMR446)", 
                      "M8 6-Pin Buchse | VCC, GND, NF_P/N (Symmetrisch), OPTO, 1-Wire ID", '#06b6d4')

    # -------------------------------------------------------------
    # BRANCH 3: POD 3 HECK (GNSS & LORA MESH) -> M8 6-Pin (Purple)
    # -------------------------------------------------------------
    draw_bezier_cable(ax, (470, 315), (550, 320), (620, 320), (700, 320), width=9, color='#0f172a', edge_color='#a855f7')
    draw_m8_connector(ax, 720, 320, "POD 3 (HECK - GNSS MAX-M10S & LORA MESH)", 
                      "M8 6-Pin Buchse | 5V VCC, GND, UART_TX/RX (384k), 1-PPS TimeSync, ID", '#a855f7')

    # -------------------------------------------------------------
    # BRANCH 4: BORDNETZ 12V / STARTERBATTERIE & ZÜNDUNG (Red/Black)
    # -------------------------------------------------------------
    draw_bezier_cable(ax, (470, 295), (550, 260), (620, 240), (700, 240), width=10, color='#0f172a', edge_color='#ef4444')
    
    # Waterproof Inline Fuse Holder (Wasserdichter ATO/Mini-Sicherungshalter)
    fuse_box = patches.Rectangle((710, 230), 30, 20, facecolor='#b91c1c', edgecolor='#ef4444', linewidth=1.5, zorder=6)
    ax.add_patch(fuse_box)
    ax.text(725, 240, "5A", color='#ffffff', fontsize=9, fontweight='bold', ha='center', va='center', zorder=7)
    
    # Flying Leads & Ring Terminals (M6 vergoldete Ringkabelschuhe)
    # KL30 (Dauerplus Rot)
    ax.plot([740, 780], [245, 255], color='#ef4444', linewidth=3.0, zorder=5)
    ax.add_patch(patches.Circle((785, 256), 5, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.0, zorder=6))
    ax.add_patch(patches.Circle((785, 256), 2.5, facecolor='#080c14', zorder=7))
    ax.text(795, 256, "KL30 (Dauerplus 12V, 5A abgesichert)", color='#ef4444', fontsize=9, fontweight='bold', va='center')
    
    # KL15 (Zündungsplus Gelb/Blau)
    ax.plot([740, 780], [240, 240], color='#38bdf8', linewidth=2.5, zorder=5)
    ax.add_patch(patches.Rectangle((780, 237), 10, 6, facecolor='#0284c7', edgecolor='#38bdf8', zorder=6))
    ax.text(795, 240, "KL15 (Zündungsplus geschaltet / Sense)", color='#38bdf8', fontsize=9, fontweight='bold', va='center')

    # GND (Fahrzeugmasse Schwarz)
    ax.plot([740, 780], [235, 225], color='#64748b', linewidth=3.0, zorder=5)
    ax.add_patch(patches.Circle((785, 224), 5, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.0, zorder=6))
    ax.add_patch(patches.Circle((785, 224), 2.5, facecolor='#080c14', zorder=7))
    ax.text(795, 224, "GND (Batterie-Masse / Chassis M6 Ring)", color='#94a3b8', fontsize=9, fontweight='bold', va='center')

    # -------------------------------------------------------------
    # BRANCH 5: CAN-BUS & TELEMETRIE / AUX -> M8 4-Pin (Green)
    # -------------------------------------------------------------
    draw_bezier_cable(ax, (470, 275), (550, 200), (620, 160), (700, 160), width=8, color='#0f172a', edge_color='#10b981')
    draw_m8_connector(ax, 720, 160, "AUX / CAN-BUS & TELEMETRIE", 
                      "M8 4-Pin Buchse | CAN_H, CAN_L (ISO 11898-2), Ext-Mic Audio In, GND", '#10b981', is_4pin=True)

    # -------------------------------------------------------------
    # 7. PINOUT & WIRE SPECIFICATION TABLE (BOTTOM PANEL)
    # -------------------------------------------------------------
    # Background card for specifications
    table_card = patches.FancyBboxPatch((30, 20), 940, 105, boxstyle="round,pad=3,rounding_size=6",
                                        facecolor='#0f172a', edgecolor='#334155', linewidth=1.2, zorder=2)
    ax.add_patch(table_card)
    
    ax.text(45, 110, "HD26 PINOUT & SIGNAL-AUFTEILUNG (AUTOMOTIVE SPEZIFIKATION):", 
            color='#38bdf8', fontsize=10, fontweight='bold')
    
    col1_text = (
        "• ABGANG 1 (Pod 1 Links - Sena):\n"
        "  Pin 1: VCC_POD1 (5V Switched)\n"
        "  Pin 2: GND_POD1 (Power Mass)\n"
        "  Pin 3: NF1_P (Audio Pos. Bourns)\n"
        "  Pin 4: NF1_N (Audio Neg. Bourns)\n"
        "  Pin 5: OPTO_TRIG1 (TLP222A Button)\n"
        "  Pin 6: 1WIRE_ID1 (DS2401 ROM)"
    )
    ax.text(45, 95, col1_text, color='#f59e0b', fontsize=8, va='top', fontfamily='monospace')
    
    col2_text = (
        "• ABGANG 2 (Pod 2 Rechts - Cardo):\n"
        "  Pin 7: VCC_POD2 (5V Switched)\n"
        "  Pin 8: GND_POD2 (Power Mass)\n"
        "  Pin 9: NF2_P (Audio Pos. Bourns)\n"
        "  Pin 10: NF2_N (Audio Neg. Bourns)\n"
        "  Pin 11: OPTO_TRIG2 (TLP222A)\n"
        "  Pin 12: 1WIRE_ID2 (DS2401 ROM)"
    )
    ax.text(235, 95, col2_text, color='#06b6d4', fontsize=8, va='top', fontfamily='monospace')

    col3_text = (
        "• ABGANG 3 (Pod 3 Heck - GNSS/Mesh):\n"
        "  Pin 13: VCC_POD3 (5V Dauer-Power)\n"
        "  Pin 14: GND_POD3 (Digital Mass)\n"
        "  Pin 15: UART_TX (Host -> Pod3)\n"
        "  Pin 16: UART_RX (Pod3 -> Host)\n"
        "  Pin 17: GNSS_PPS (Time Sync)\n"
        "  Pin 18: 1WIRE_ID3 (DS2401 ROM)"
    )
    ax.text(430, 95, col3_text, color='#a855f7', fontsize=8, va='top', fontfamily='monospace')

    col4_text = (
        "• ABGANG 4 (Bordnetz 12V):\n"
        "  Pin 19: KL30 (Dauerplus 12V)\n"
        "  Pin 20: KL15 (Zündung Sense)\n"
        "  Pin 21: GND_PWR (Batteriemasse)\n"
        "  Pin 22: SHIELD / CHASSIS_GND\n"
        "  Sicherung: 5A Mini-Blade ATO\n"
        "  Querschnitt: AWG20 / 0.75 mm²"
    )
    ax.text(625, 95, col4_text, color='#ef4444', fontsize=8, va='top', fontfamily='monospace')

    col5_text = (
        "• ABGANG 5 (CAN & Aux):\n"
        "  Pin 23: CAN_H (ISO 11898-2)\n"
        "  Pin 24: CAN_L (ISO 11898-2)\n"
        "  Pin 25: EXT_MIC_IN (Analog)\n"
        "  Pin 26: RESERVE_IO (3.3V)\n"
        "  Kabel: AWG24 Paarverseilt\n"
        "  Schirm: 360° Cu-Geflecht"
    )
    ax.text(800, 95, col5_text, color='#10b981', fontsize=8, va='top', fontfamily='monospace')

    plt.tight_layout()
    plt.savefig(output_path, dpi=220, facecolor='#080c14', bbox_inches='tight')
    plt.close()
    print(f"✓ Wiring Harness Schematic CAD generated: {output_path}")

if __name__ == "__main__":
    out1 = "/Users/schmidtm/.gemini/antigravity-ide/brain/71a5d344-5a46-4a0e-bb50-16bb2304a17f/wiring_harness_cad.png"
    out2 = "/Users/schmidtm/openMotorBridge/hardware/cad/wiring_harness_cad.png"
    os.makedirs(os.path.dirname(out2), exist_ok=True)
    render_wiring_harness(out1)
    render_wiring_harness(out2)
