#!/usr/bin/env python3
"""
OpenMotorBridge Rack-Tail Mount & Tail-Balcony Technical Illustration Generator
--------------------------------------------------------------------------------
Generates ultra-high-definition, publication-grade engineering graphics for:
  1. Section 6.4.2 Abbildung 1: Side Cross-Section View (Topcase, Rack-Tail Mount, Pod 3, Radar)
  2. Section 6.4.2 Abbildung 2: Top-Down Plan View (Rack-Tail Mount, Pod 3 Tray, Antenna Fin)
  3. Section 6.4.2 Abbildung 3: Dual Radar Lock (36-Tooth Hirth Gear + Anti-Theft Bayonet Dock)

Output directory: docs/images/cad/
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

OUTPUT_DIR = "docs/images/cad"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Shared Color Palette (Modern Dark Engineering Theme)
BG_COLOR       = '#080c14'
PANEL_BG       = '#0f172a'
GRID_COLOR     = '#1e293b'
ACCENT_BLUE    = '#38bdf8'
CYAN_HIGHLIGHT = '#00adb5'
TEXT_LIGHT     = '#f8fafc'
TEXT_MUTED     = '#94a3b8'
ALU_COLOR      = '#cbd5e1'
PA12_CF        = '#1e293b'
PA12_EDGE      = '#38bdf8'
RADAR_RED      = '#ef4444'
RADAR_BEAM     = '#f43f5e'
GOLD_PAD       = '#fbbf24'
STAINLESS      = '#94a3b8'


# =============================================================================
# 1. SIDE CROSS-SECTION: GS REAR WITH TOPCASE, HECK-BALKON & VARIA RADAR
# =============================================================================
def generate_side_cross_section():
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.grid(True, linestyle='--', alpha=0.18, color=GRID_COLOR)
    ax.set_axisbelow(True)

    # 1. Stainless Steel Rack Tubes (Ø 18 mm)
    rack_x = [-90, -40, 10]
    for rx in rack_x:
        ax.add_patch(patches.Circle((rx, 0), radius=9.0, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.5, zorder=3))
        ax.add_patch(patches.Circle((rx, 0), radius=7.5, facecolor='#1e293b', edgecolor='#64748b', linewidth=0.8, zorder=4))
        # Center marker
        ax.plot(rx, 0, '+', color='#94a3b8', markersize=6, zorder=5)

    # Horizontal rack connecting bar
    ax.add_patch(patches.Rectangle((-105, -3), 130, 6, facecolor='#334155', edgecolor='#64748b', linewidth=1.0, zorder=2))

    # 2. Aluminum Topcase (Touratech Zega Evo / BMW Adventure 38L)
    # Case body
    topcase_box = patches.Rectangle((-100, 15), 90, 110, facecolor='#1e293b', alpha=0.92, edgecolor=ALU_COLOR, linewidth=2.0, zorder=2)
    ax.add_patch(topcase_box)
    # Aluminum skin hatching / highlight
    ax.add_patch(patches.Rectangle((-98, 17), 86, 106, facecolor='#334155', alpha=0.35, zorder=2))
    # Topcase lid opening arc & arrow
    ax.annotate('', xy=(-35, 140), xytext=(-10, 125),
                arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=2.2, connectionstyle="arc3,rad=-0.25"), zorder=6)
    ax.text(-22, 145, "Deckel öffnet 100% frei nach oben/vorn!", color=ACCENT_BLUE, fontsize=10, weight='bold', ha='center')

    # Topcase lower base mount / quick release latch
    ax.add_patch(patches.Rectangle((-95, 6), 80, 9, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.2, zorder=3))
    ax.text(-55, 10.5, "5-Sekunden Koffer-Schnellverschluss (Verriegelung am Träger)", color='#e2e8f0', fontsize=8.5, ha='center', zorder=5)

    # Topcase label
    ax.text(-55, 75, "ALUMINIUM-TOPCASE (38 L)\n(z. B. Touratech Zega Evo /\nBMW Adventure Alukoffer)\n[Massive 1.5 mm Alu-Wand schirmt HF ab!]",
            color=ALU_COLOR, fontsize=10.5, weight='bold', ha='center', va='center', zorder=5)

    # 3. Rack-Tail Mount Cantilever Tray ("Heck-Balkon" Ausleger)
    # Cantilever arm extending behind topcase
    cantilever_path = [
        (-40, -4),     # Front clamp mount point at rack
        (8, -4),
        (8, -8),
        (92, -8),      # Tray floor rear edge
        (92, 22),      # Astabweiser tip
        (72, 8),       # 45° deflector fin top
        (65, 8),
        (65, 16),      # Pod 3 front rim
        (8, 16),
        (8, 5),
        (-40, 5),
        (-40, -4)
    ]
    cantilever_poly = patches.Polygon(cantilever_path, closed=True, facecolor='#0f172a', edgecolor=PA12_EDGE, linewidth=2.0, zorder=4)
    ax.add_patch(cantilever_poly)

    # 4. Pod 3 Gehäuse (Transceiver Pod: 135 x 70 x 38 mm in Tray)
    pod3_rect = patches.Rectangle((12, -4), 50, 18, facecolor='#0369a1', alpha=0.55, edgecolor='#38bdf8', linewidth=1.6, zorder=5)
    ax.add_patch(pod3_rect)
    # MAX-M10S Ceramic Patch Antenna on top of Pod 3
    ax.add_patch(patches.Rectangle((16, 14), 18, 4.5, facecolor='#b45309', edgecolor=GOLD_PAD, linewidth=1.2, zorder=6))
    ax.text(25, 16.2, "MAX-M10S GNSS", color=TEXT_LIGHT, fontsize=7.5, weight='bold', ha='center', va='center', zorder=7)

    # Internal LoRa & IMU markers
    ax.add_patch(patches.Rectangle((38, 2), 16, 8, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=0.8, zorder=6))
    ax.text(46, 6, "SX1262 LoRa\n& BMI270 IMU", color='#cbd5e1', fontsize=6.8, ha='center', va='center', zorder=7)

    # 5. GNSS & LoRa 140° Sky Zenith Cone
    zenith_cone = [
        (25, 18.5),
        (-15, 95),
        (65, 95),
        (25, 18.5)
    ]
    ax.add_patch(patches.Polygon(zenith_cone, closed=True, facecolor='#38bdf8', alpha=0.15, edgecolor='#38bdf8', linestyle='--', linewidth=1.2, zorder=3))
    ax.text(25, 80, "FREIER 140°-HIMMELSZENIT\n(Vollkommen unverschattet\nhinter Topcase-Rückwand)",
            color=ACCENT_BLUE, fontsize=9.5, weight='bold', ha='center', va='center', zorder=6)

    # 6. 45°-Astabweiser-Keil & Integrierte 2.4 GHz +5 dBi Antenne
    # Deflector fin triangle
    fin_pts = [(65, -8), (92, -8), (92, 22), (65, 8)]
    ax.add_patch(patches.Polygon(fin_pts, closed=True, facecolor='#1e293b', edgecolor='#00adb5', linewidth=1.5, zorder=5))

    # Dipole antenna embedded inside fin channel
    ax.plot([72, 88], [-2, 14], color=CYAN_HIGHLIGHT, linewidth=5.5, solid_capstyle='round', zorder=6)
    ax.plot([72, 88], [-2, 14], color='#e0f2fe', linewidth=1.5, solid_capstyle='round', zorder=7)
    
    # Text placed cleanly to the right of the fin
    ax.text(100, 14, "45°-ASTABWEISER-KEIL\n• Äste & Gurte gleiten ab\n• +5 dBi 2.4 GHz Dipolantenne\n  (voll geschützt versenkt)",
            color=CYAN_HIGHLIGHT, fontsize=9, weight='bold', va='center', zorder=7)
    ax.annotate('', xy=(88, 14), xytext=(98, 14),
                arrowprops=dict(arrowstyle="->", color=CYAN_HIGHLIGHT, lw=1.2), zorder=8)

    # Branch deflection arrow
    ax.annotate('', xy=(98, 30), xytext=(72, 2),
                arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=2.0, linestyle=':'), zorder=8)
    ax.text(82, 34, "Abgleitbahn", color='#38bdf8', fontsize=8, style='italic', ha='center', zorder=8)

    # 7. Underside M5 GoPro-Gabel with Hirth Gear
    gopro_fork = patches.Rectangle((30, -22), 16, 14, facecolor='#1e293b', edgecolor='#94a3b8', linewidth=1.2, zorder=4)
    ax.add_patch(gopro_fork)
    # Hirth tooth rosette indication
    ax.add_patch(patches.Circle((38, -15), radius=5.5, facecolor='#334155', edgecolor=GOLD_PAD, linewidth=1.2, zorder=5))
    ax.plot(38, -15, 'o', color=GOLD_PAD, markersize=4, zorder=6)
    ax.text(38, -15, "10°", color=BG_COLOR, fontsize=6.5, weight='bold', ha='center', va='center', zorder=7)

    # 8. Garmin Varia mmWave Radar (RTL515 / RCT715)
    radar_x = 38
    radar_y = -45
    # Radar body
    ax.add_patch(patches.Rectangle((radar_x - 11, radar_y - 25), 22, 50, facecolor='#11151c', edgecolor='#64748b', linewidth=1.5, zorder=5))
    # Red LED lens ring
    ax.add_patch(patches.Circle((radar_x, radar_y + 8), radius=7.5, facecolor='#991b1b', edgecolor=RADAR_RED, linewidth=1.5, zorder=6))
    ax.add_patch(patches.Circle((radar_x, radar_y + 8), radius=5.0, facecolor=RADAR_RED, alpha=0.8, zorder=7))
    # mmWave radome window
    ax.add_patch(patches.Rectangle((radar_x - 9, radar_y - 20), 18, 22, facecolor='#18181b', edgecolor='#3f3f46', linewidth=1.0, zorder=6))
    ax.text(radar_x, radar_y - 9, "24 GHz\nmmWave", color='#a1a1aa', fontsize=7.5, ha='center', va='center', zorder=7)

    # Radar Beam cone
    radar_cone = [
        (radar_x + 11, radar_y),
        (radar_x + 95, radar_y + 35),
        (radar_x + 95, radar_y - 35),
        (radar_x + 11, radar_y)
    ]
    ax.add_patch(patches.Polygon(radar_cone, closed=True, facecolor=RADAR_BEAM, alpha=0.12, edgecolor=RADAR_BEAM, linestyle='--', linewidth=1.2, zorder=2))
    # Radar wave arcs
    for arc_r in [30, 50, 70]:
        arc = patches.Arc((radar_x + 11, radar_y), arc_r*2, arc_r*1.5, angle=0, theta1=-25, theta2=25, color=RADAR_BEAM, linewidth=1.2, alpha=0.6, zorder=3)
        ax.add_patch(arc)
    ax.text(radar_x + 55, radar_y - 42, "GARMIN VARIA RADAR\n(140 m Rückraum-Erfassung,\n140° Weitwinkel-Keule)", color=RADAR_RED, fontsize=9.5, weight='bold', ha='center', zorder=6)

    # 9. Dimension Callouts
    # Cantilever Overhang Dimension (68 mm) placed cleanly above
    ax.annotate('', xy=(-10, 48), xytext=(58, 48),
                arrowprops=dict(arrowstyle="<->", color='#38bdf8', lw=1.5), zorder=8)
    ax.text(24, 52, "65..68 mm Auskragung hinter Topcase-Wand", color='#38bdf8', fontsize=9.5, weight='bold', ha='center', zorder=8)
    ax.plot([-10, -10], [15, 52], ':', color='#38bdf8', linewidth=1.0, zorder=7)
    ax.plot([58, 58], [15, 52], ':', color='#38bdf8', linewidth=1.0, zorder=7)

    # Height above ground (90..95 cm)
    ax.plot([-115, 140], [-85, -85], color='#475569', linestyle='-', linewidth=2.0, zorder=2)
    ax.text(-110, -81, "FAHRBAHN-NIVEAU (BODEN)", color='#64748b', fontsize=8.5, weight='bold', zorder=3)

    ax.annotate('', xy=(12, -85), xytext=(12, radar_y),
                arrowprops=dict(arrowstyle="<->", color=GOLD_PAD, lw=1.5), zorder=8)
    ax.text(14, -65, "90..95 cm Radar-Höhe:\n• Voll geschützt vor Steinschlag (Tire Roost)\n• Sicher bei tiefen Wasserdurchfahrten",
            color=GOLD_PAD, fontsize=9, weight='bold', va='center', zorder=8)

    # Titles & Labels
    ax.set_title("OPENMOTORBRIDGE // HECK-POD 3 RACK-TAIL MOUNT & HECK-BALKON (SEITEN-SCHNITTANSICHT)",
                 fontsize=14.5, color=TEXT_LIGHT, weight='heavy', pad=18)
    ax.text(0.5, 0.965, "Kollisionsfreie Topcase-Deckelöffnung · 140° Freier Himmels-Zenit für GNSS/LoRa · Integrierter Astabweiser · Hirth-Neigungssicherung",
            transform=fig.transFigure, fontsize=10, color=TEXT_MUTED, ha='center')

    ax.set_xlim(-120, 150)
    ax.set_ylim(-95, 155)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "rack_tail_mount_side_cross_section.png")
    plt.savefig(out_path, facecolor=BG_COLOR, edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Rendered Side Cross-Section CAD diagram to {out_path}")


# =============================================================================
# 2. TOP-DOWN PLAN VIEW: HECK-BALKON WITH POD 3 TRAY & INTEGRATED ANTENNA
# =============================================================================
def generate_top_view():
    fig, ax = plt.subplots(figsize=(17, 9.5), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.grid(True, linestyle='--', alpha=0.18, color=GRID_COLOR)
    ax.set_axisbelow(True)

    # 1. Topcase Rear Wall (Running along Y at X=-35)
    ax.add_patch(patches.Rectangle((-58, -65), 18, 130, facecolor='#1e293b', edgecolor=ALU_COLOR, linewidth=2.0, zorder=2))
    ax.text(-49, 0, "ALU-TOPCASE RÜCKWAND\n(Touratech Zega Evo / BMW Adv.)",
            color=ALU_COLOR, fontsize=9.5, weight='bold', rotation=90, va='center', ha='center', zorder=4)

    # 2. Mounting Flange to Rack (Forward slots)
    ax.add_patch(patches.Rectangle((-40, -55), 37, 110, facecolor='#0f172a', edgecolor=PA12_EDGE, linewidth=1.5, zorder=3))
    # M6 Mounting Slots
    for sy in [-38, 38]:
        ax.add_patch(patches.FancyBboxPatch((-26, sy - 4), 14, 8, boxstyle="round,pad=1.5", facecolor='#334155', edgecolor=GOLD_PAD, linewidth=1.2, zorder=5))
        ax.text(-19, sy, "M6", color=GOLD_PAD, fontsize=8, weight='bold', ha='center', va='center', zorder=6)
    ax.text(-19, 0, "2x M6 Verschraubung\n(Trägerplatte oder\nØ 18 mm Halbschellen)", color='#cbd5e1', fontsize=8.2, ha='center', va='center', zorder=5)

    # 3. Cantilever Pod 3 Housing Tray (136.5 x 71.5 x 18 mm rim)
    tray_outer = patches.Rectangle((-3, -37.5), 78, 75, facecolor='#0f172a', edgecolor=PA12_EDGE, linewidth=2.0, zorder=4)
    ax.add_patch(tray_outer)
    # Inner pocket
    tray_inner = patches.Rectangle((0, -34), 72, 68, facecolor='#0369a1', alpha=0.35, edgecolor='#0284c7', linewidth=1.2, zorder=5)
    ax.add_patch(tray_inner)

    # 4. Pod 3 Component Placement in Tray
    # u-blox MAX-M10S Ceramic Patch
    ax.add_patch(patches.Rectangle((12, -15), 25, 30, facecolor='#b45309', edgecolor=GOLD_PAD, linewidth=1.5, zorder=6))
    ax.text(24.5, 0, "u-blox MAX-M10S\nKeramik-Patchantenne\n(Blickt vollkommen frei\nnach oben zum Zenit)",
            color=TEXT_LIGHT, fontsize=8.5, weight='bold', ha='center', va='center', zorder=7)

    # M8 Connector Entry Port from below
    ax.add_patch(patches.Circle((6, -26), radius=5.5, facecolor='#d97706', edgecolor='#fbbf24', linewidth=1.2, zorder=6))
    ax.text(6, -26, "M8", color=BG_COLOR, fontsize=7.5, weight='bold', ha='center', va='center', zorder=7)
    ax.text(14, -26, "M8 Zuleitung läuft von unten ein", color='#cbd5e1', fontsize=8, va='center', zorder=7)

    # SX1262 LoRa Module & IMU
    ax.add_patch(patches.Rectangle((42, -28), 26, 20, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=6))
    ax.text(55, -18, "SX1262 LoRa\n& BMI270 IMU", color='#cbd5e1', fontsize=7.5, ha='center', va='center', zorder=7)

    # 5. Astabweiser-Finne (PA12-CF) at rear edge
    fin_poly = [
        (75, -20),
        (102, -12),
        (102, 12),
        (75, 20),
        (75, -20)
    ]
    ax.add_patch(patches.Polygon(fin_poly, closed=True, facecolor='#1e293b', edgecolor=CYAN_HIGHLIGHT, linewidth=1.8, zorder=5))

    # Embedded 2.4 GHz Antenna in protective channel
    ax.plot([82, 96], [-6, 6], color=CYAN_HIGHLIGHT, linewidth=6.0, solid_capstyle='round', zorder=6)
    ax.plot([82, 96], [-6, 6], color='#e0f2fe', linewidth=2.0, solid_capstyle='round', zorder=7)
    
    # Text positioned cleanly to the right of the fin
    ax.text(108, 0, "ASTABWEISER-FINNE\n• 2.4 GHz +5 dBi Dipol\n  (eingeclipst in Nut)\n• RG178 Koax intern",
            color=CYAN_HIGHLIGHT, fontsize=8.5, weight='bold', va='center', zorder=7)
    ax.annotate('', xy=(100, 0), xytext=(107, 0),
                arrowprops=dict(arrowstyle="->", color=CYAN_HIGHLIGHT, lw=1.2), zorder=8)

    # Internal coax cable trace
    ax.plot([55, 75, 82], [0, 0, -6], color='#f59e0b', linestyle='--', linewidth=1.5, zorder=6)
    ax.text(68, -4, "Koax", color='#f59e0b', fontsize=7, ha='center', zorder=7)

    # 6. Underside GoPro Hinge Axis Indicator
    ax.plot([35, 35], [-45, 45], color='#f43f5e', linestyle='-.', linewidth=1.2, zorder=3)
    ax.text(35, 48, "Symmetrie-Achse: Garmin Varia Radar Schwenkarm (Unterseite)", color='#f43f5e', fontsize=8.5, ha='center', zorder=5)

    # Dimensions
    # Flange Width
    ax.annotate('', xy=(-62, -55), xytext=(-62, 55),
                arrowprops=dict(arrowstyle="<->", color='#94a3b8', lw=1.2), zorder=8)
    ax.text(-65, 0, "110 mm Flanschbreite", color='#94a3b8', fontsize=8.5, rotation=90, va='center', ha='right', zorder=8)

    # Tray Length
    ax.annotate('', xy=(-3, -42), xytext=(75, -42),
                arrowprops=dict(arrowstyle="<->", color=ACCENT_BLUE, lw=1.2), zorder=8)
    ax.text(36, -46, "78 mm Korbbreite (Pod 3 Aufnahme: 135 x 70 mm)", color=ACCENT_BLUE, fontsize=8.5, ha='center', zorder=8)

    ax.set_title("OPENMOTORBRIDGE // RACK-TAIL MOUNT DRAUFSICHT (X-Y EBENE)",
                 fontsize=14.5, color=TEXT_LIGHT, weight='heavy', pad=18)
    ax.text(0.5, 0.965, "Formbündige Pod 3 Wanne · Geschützter Koaxialkanal · Astabweiser mit integriertem Antennenschacht · 2x M6 Verschraubung",
            transform=fig.transFigure, fontsize=10, color=TEXT_MUTED, ha='center')

    ax.set_xlim(-75, 150)
    ax.set_ylim(-65, 65)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "rack_tail_mount_top_view.png")
    plt.savefig(out_path, facecolor=BG_COLOR, edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Rendered Top-Down CAD diagram to {out_path}")


# =============================================================================
# 3. DUAL RADAR LOCK: 36-TOOTH HIRTH GEAR & ANTI-THEFT BAYONET DOCK
# =============================================================================
def generate_dual_radar_lock():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 10), dpi=220, facecolor=BG_COLOR)
    for ax in (ax1, ax2):
        ax.set_facecolor(BG_COLOR)
        ax.grid(True, linestyle='--', alpha=0.18, color=GRID_COLOR)
        ax.set_axisbelow(True)

    # -------------------------------------------------------------------------
    # PANEL A: HIRTH-FORMSCHLUSS (10°-RASTUNG)
    # -------------------------------------------------------------------------
    ax1.set_title("A. RADIALE HIRTH-VERZAHNUNG (10°-RASTUNG)\n[Absack-Schutz bei Offroad-Wellblech & Pistenrütteln]",
                  fontsize=12.5, color=TEXT_LIGHT, weight='heavy', pad=15)

    # Draw Central Hirth Rosette (GoPro Tongue)
    center_y = 0
    # Center 6 mm Tongue
    ax1.add_patch(patches.Rectangle((-10, -35), 20, 70, facecolor='#1e293b', edgecolor=PA12_EDGE, linewidth=1.5, zorder=3))
    ax1.text(0, -42, "Zentrale 6.0 mm GoPro-Zunge\n(beidseitige Hirth-Rosette)", color=ACCENT_BLUE, fontsize=9.5, weight='bold', ha='center')

    # Left & Right Fork Lugs (Gabelwangen)
    ax1.add_patch(patches.Rectangle((-32, -30), 14, 60, facecolor='#0f172a', edgecolor='#64748b', linewidth=1.2, zorder=2))
    ax1.text(-25, 34, "Gabelwange\nLinks", color='#94a3b8', fontsize=8.5, ha='center')

    ax1.add_patch(patches.Rectangle((18, -30), 14, 60, facecolor='#0f172a', edgecolor='#64748b', linewidth=1.2, zorder=2))
    ax1.text(25, 34, "Gabelwange\nRechts", color='#94a3b8', fontsize=8.5, ha='center')

    # Central Through Bore & M5 Bolt
    ax1.add_patch(patches.Rectangle((-45, -5), 90, 10, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.5, zorder=5))
    ax1.plot([-45, 45], [0, 0], '-.', color='#cbd5e1', linewidth=1.0, zorder=6)
    # M5 Bolt Head (Torx-TR Security)
    ax1.add_patch(patches.Rectangle((-48, -9), 8, 18, facecolor='#64748b', edgecolor=GOLD_PAD, linewidth=1.5, zorder=7))
    ax1.text(-55, 0, "M5 Torx-TR\nSicherheits-\nSchraube", color=GOLD_PAD, fontsize=8.5, weight='bold', ha='right', va='center')
    # M5 Nyloc Nut
    ax1.add_patch(patches.Rectangle((40, -8), 8, 16, facecolor='#64748b', edgecolor='#cbd5e1', linewidth=1.2, zorder=7))
    ax1.text(52, 0, "DIN 985\nStoppmutter", color='#cbd5e1', fontsize=8.5, ha='left', va='center')

    # Hirth Teeth Serration Pattern (Left & Right Interfaces)
    for side in [-10, 10]:
        teeth_y = np.linspace(-25, 25, 13)
        for i in range(len(teeth_y) - 1):
            y_bot = teeth_y[i]
            y_mid = (teeth_y[i] + teeth_y[i+1]) / 2.0
            y_top = teeth_y[i+1]
            sign = 1 if side == -10 else -1
            tooth_poly = [(side, y_bot), (side + sign*3.0, y_mid), (side, y_top)]
            ax1.add_patch(patches.Polygon(tooth_poly, closed=True, facecolor=GOLD_PAD, edgecolor='#b45309', linewidth=0.8, zorder=4))

    # Key Features Bullet Box
    callout_text_a = (
        "• 36 Präzisionszähne (10° Teilung)\n"
        "• ±20° Neigungsjustage für exakt horizontalen Radar-Horizont\n"
        "• 100% formschlüssige Blockierung nach Anziehen (3.5 Nm)\n"
        "• Absacken durch Wellblech/Roost physikalisch UNMÖGLICH!"
    )
    ax1.text(0, -78, callout_text_a, color='#e2e8f0', fontsize=9.5,
             bbox=dict(boxstyle="round,pad=0.6", facecolor='#0f172a', edgecolor=GOLD_PAD, linewidth=1.2),
             ha='center', va='center')

    ax1.set_xlim(-85, 85)
    ax1.set_ylim(-95, 55)
    ax1.axis('off')

    # -------------------------------------------------------------------------
    # PANEL B: GARMIN DIEBSTAHL-VERRIEGELUNG (QUARTER-TURN + M3 LOCK)
    # -------------------------------------------------------------------------
    ax2.set_title("B. GARMIN VARIA DIEBSTAHL-VERRIEGELUNG\n[Kein Abziehen bei Zwischenstopps / 90°-Sperrmade]",
                  fontsize=12.5, color=TEXT_LIGHT, weight='heavy', pad=15)

    # 1. Dock Housing Chamber
    ax2.add_patch(patches.Circle((0, 0), radius=38.0, facecolor='#0f172a', edgecolor=PA12_EDGE, linewidth=1.8, zorder=2))
    ax2.add_patch(patches.Circle((0, 0), radius=28.0, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=3))

    # 2. Garmin Bayonet Locking Wings (Mated State after 90° Turn)
    # Wing Left & Right
    ax2.add_patch(patches.Rectangle((-26, -7), 52, 14, facecolor='#334155', edgecolor=ALU_COLOR, linewidth=1.2, zorder=4))
    ax2.add_patch(patches.Circle((0, 0), radius=10.0, facecolor='#11151c', edgecolor='#64748b', linewidth=1.0, zorder=5))
    ax2.text(0, 0, "Garmin\nQuarter-\nTurn", color='#e2e8f0', fontsize=7.5, weight='bold', ha='center', va='center', zorder=6)

    # 90° Insertion Entry Slots (Vertical)
    ax2.plot([0, 0], [10, 26], color='#64748b', linestyle=':', linewidth=2.0, zorder=4)
    ax2.plot([0, 0], [-10, -26], color='#64748b', linestyle=':', linewidth=2.0, zorder=4)

    # Rotation Arc Arrow
    arc = patches.Arc((0, 0), 46, 46, angle=0, theta1=0, theta2=90, color=ACCENT_BLUE, linewidth=2.0, zorder=7)
    ax2.add_patch(arc)
    ax2.annotate('', xy=(0, 23), xytext=(22, 6),
                arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=2.0), zorder=8)
    ax2.text(25, 25, "90° Bajonett-\nDrehung", color=ACCENT_BLUE, fontsize=8.5, weight='bold', ha='center')

    # 3. Tangential M3 Security Locking Grub Screw (Madenschraube)
    ax2.add_patch(patches.Rectangle((-32, 7.5), 14, 5.5, facecolor='#dc2626', edgecolor=GOLD_PAD, linewidth=1.2, zorder=7))
    ax2.plot([-32, -18], [10.25, 10.25], '-.', color='#fef08a', linewidth=0.8, zorder=8)
    ax2.plot(-25, 10.25, 'x', color='#ffffff', markersize=6, zorder=9)

    ax2.annotate('M3 Sicherungs-Madenschraube\n(Torx-TR mit Innenstift):\nBlockiert Rückdrehung 100%!',
                 xy=(-25, 10.25), xytext=(-65, 30),
                 arrowprops=dict(arrowstyle="->", color=GOLD_PAD, lw=1.5),
                 color=GOLD_PAD, fontsize=9, weight='bold', ha='center', zorder=10)

    # 4. M8 Cable Strain Relief Port
    ax2.add_patch(patches.Rectangle((-6, -46), 12, 10, facecolor='#b45309', edgecolor=GOLD_PAD, linewidth=1.2, zorder=6))
    ax2.text(0, -41, "M8 PUR", color=BG_COLOR, fontsize=7.5, weight='bold', ha='center', va='center', zorder=7)

    # Key Features Bullet Box
    callout_text_b = (
        "• Kompatibel mit allen Garmin Varia (RTL515 / RCT715 / eRTL615)\n"
        "• Federbelastete Einrastklinke + tangentiale M3 Madenschraube\n"
        "• Ohne Spezialbit (Torx-TR) kein Abdrehen oder Entwenden möglich\n"
        "• M8 Zugentlastung schützt Signalleitung bei Erschütterung"
    )
    ax2.text(0, -78, callout_text_b, color='#e2e8f0', fontsize=9.5,
             bbox=dict(boxstyle="round,pad=0.6", facecolor='#0f172a', edgecolor=ACCENT_BLUE, linewidth=1.2),
             ha='center', va='center')

    ax2.set_xlim(-85, 85)
    ax2.set_ylim(-95, 55)
    ax2.axis('off')

    plt.suptitle("OPENMOTORBRIDGE // DUALER RADAR-LOCK: HIRTH-VERZAHNUNG & DIEBSTAHLSICHERES DOCK",
                 fontsize=14.5, color=TEXT_LIGHT, weight='heavy', y=0.98)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "radar_hirth_lock_dock_cad.png")
    plt.savefig(out_path, facecolor=BG_COLOR, edgecolor='none', dpi=220)
    plt.close()
    print(f"✓ Rendered Dual Radar Lock CAD diagram to {out_path}")


if __name__ == '__main__':
    print("Generating Rack-Tail Mount & Dual Radar Lock CAD Diagrams...")
    generate_side_cross_section()
    generate_top_view()
    generate_dual_radar_lock()
    print("✓ All 3 illustrations generated successfully!")
