#!/usr/bin/env python3
"""
OpenMotorBridge Saddlebag Wiring & MagSafe Breakaway Technical Illustration Generator
-------------------------------------------------------------------------------------
Generates ultra-high-definition, publication-grade engineering graphics for:
  Section 6.5.2: Saddlebag Cable Routing, Switched Power & Mechanic-Proof MagSafe Breakaway

Output: docs/images/cad/saddlebag_magsafe_wiring_cad.png
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

# Shared Color Palette (Dark Modern Engineering)
BG_COLOR       = '#080c14'
PANEL_BG       = '#0f172a'
PANEL_BORDER   = '#1e293b'
GRID_COLOR     = '#1e293b'
ACCENT_BLUE    = '#38bdf8'
CYAN_HIGHLIGHT = '#00adb5'
TEXT_LIGHT     = '#f8fafc'
TEXT_MUTED     = '#94a3b8'
ALU_COLOR      = '#cbd5e1'
GOLD_PAD       = '#fbbf24'
STAINLESS      = '#94a3b8'
MAGNET_RED     = '#ef4444'
MAGNET_BLUE    = '#3b82f6'
SUCCESS_GREEN  = '#22c55e'
WARNING_ORANGE = '#f97316'
BAG_BODY       = '#131d31'
BAG_EDGE       = '#475569'


def generate_saddlebag_wiring_diagram():
    fig, ax = plt.subplots(figsize=(20, 11.5), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.grid(True, linestyle='--', alpha=0.15, color=GRID_COLOR)
    ax.set_axisbelow(True)

    # Coords system: X: -105 to 145, Y: -48 to 92
    ax.set_xlim(-105, 145)
    ax.set_ylim(-48, 92)
    ax.set_aspect('equal')

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    header_box = patches.FancyBboxPatch((-100, 77), 240, 11,
                                       boxstyle="round,pad=0.5,rounding_size=2.0",
                                       facecolor=PANEL_BG, edgecolor=ACCENT_BLUE,
                                       linewidth=1.2, zorder=2)
    ax.add_patch(header_box)
    ax.text(20, 83.5, "OPENMOTORBRIDGE // KOFFER-VERKABELUNG & MAGSAFE-ABREISS-SCHNITTSTELLE (IP67)",
            color=TEXT_LIGHT, fontsize=13, fontweight='bold', ha='center', va='center', family='sans-serif', zorder=12)
    ax.text(20, 79.5, "Zone 1: Motorradrahmen (Fest verlegt)  ◄──  Selbstzentrierende Abreißtrennung (~10-15 N)  ──►  Zone 2: Koffer-Innenraum & Deckel-Pod (0 N Zuglast)",
            color=CYAN_HIGHLIGHT, fontsize=9.5, ha='center', va='center', family='sans-serif', zorder=12)

    # =========================================================================
    # ZONE 1: MOTORRADRAHMEN (LINKS, X: -100 bis -20)
    # =========================================================================
    zone1_box = patches.FancyBboxPatch((-100, -42), 76, 114,
                                       boxstyle="round,pad=0.8,rounding_size=2.5",
                                       facecolor='#0b1120', edgecolor='#334155',
                                       linewidth=1.0, linestyle='--', zorder=1)
    ax.add_patch(zone1_box)
    ax.text(-62, 68, "ZONE 1: MOTORRADRAHMEN", color=ACCENT_BLUE, fontsize=11, fontweight='bold', ha='center', zorder=12)
    ax.text(-62, 65, "Fest verlegt, wetter- & rüttelsicher unter Sitzbank", color=TEXT_MUTED, fontsize=8, ha='center', zorder=12)

    # Motorrad-Rahmenrohr (Ø 26 mm)
    ax.add_patch(patches.Rectangle((-88, -25), 10, 85, facecolor='#1e293b', edgecolor='#475569', linewidth=1.5, zorder=2))
    ax.plot([-83, -83], [-25, 60], linestyle='-.', color='#64748b', linewidth=0.8, zorder=3)
    ax.text(-83, 56, "Rahmenrohr Ø 26 mm", color=TEXT_MUTED, fontsize=7.5, ha='center', rotation=90, zorder=12)

    # Sitzbank-Kontur (Schematisch)
    seat_path = Path([(-98, 48), (-45, 52), (-25, 46), (-25, 36), (-98, 36), (-98, 48)])
    ax.add_patch(patches.PathPatch(seat_path, facecolor='#1e1e24', edgecolor='#3f3f46', linewidth=1.2, zorder=2))
    ax.text(-60, 42, "FAHRERSITZBANK-KONTUR", color='#71717a', fontsize=8, fontweight='bold', ha='center', zorder=12)

    # Central Box (unter Sitzbank)
    cbox = patches.FancyBboxPatch((-76, 13), 46, 21, boxstyle="round,pad=0.5,rounding_size=1.5",
                                  facecolor='#1e293b', edgecolor=ACCENT_BLUE, linewidth=1.2, zorder=3)
    ax.add_patch(cbox)
    ax.text(-53, 29, "ZENTRALBOX (PCBA 01)", color=TEXT_LIGHT, fontsize=9.5, fontweight='bold', ha='center', zorder=12)
    ax.text(-53, 24.5, "• KL15 Zündungserkennung (LM5164 DCDC 5V)", color=CYAN_HIGHLIGHT, fontsize=7.4, ha='center', zorder=12)
    ax.text(-53, 20.5, "• BQ24075 LiPo-USV (6.5V Crank-Puffer)", color='#a5f3fc', fontsize=7.4, ha='center', zorder=12)
    ax.text(-53, 16.5, "• TLP222A Optokoppler (OEM-Boot / PTT)", color='#93c5fd', fontsize=7.4, ha='center', zorder=12)

    # M8 PUR Systemkabel von Central Box zum MagSafe Dock
    cable_zone1_x = [-53, -53, -38, -38]
    cable_zone1_y = [13, 0, 0, -10]
    ax.plot(cable_zone1_x, cable_zone1_y, color='#0284c7', linewidth=3.5, zorder=4)
    ax.plot(cable_zone1_x, cable_zone1_y, color='#38bdf8', linewidth=1.5, zorder=5)
    ax.text(-44, 3.5, "M8 PUR Automotive-Kabel", color='#7dd3fc', fontsize=7.5, ha='left', zorder=12)

    # Stationäres MagSafe Rahmen-Dock (009_magsafe_frame_dock.scad)
    dock_box = patches.FancyBboxPatch((-52, -30), 28, 20, boxstyle="round,pad=0.5,rounding_size=1.5",
                                      facecolor='#111827', edgecolor='#38bdf8', linewidth=1.5, zorder=3)
    ax.add_patch(dock_box)
    ax.text(-38, -14, "MAGSAFE RAHMEN-DOCK", color=TEXT_LIGHT, fontsize=8.5, fontweight='bold', ha='center', zorder=12)
    ax.text(-38, -18, "009_magsafe_frame_dock.scad", color=CYAN_HIGHLIGHT, fontsize=7.0, ha='center', family='monospace', zorder=12)
    ax.text(-38, -22, "• Ø 26 mm Rohrsattel-Klemmung", color='#94a3b8', fontsize=7.0, ha='center', zorder=12)
    ax.text(-38, -26, "• PCBA 06 Schutzplatine (TVS-ESD)", color=GOLD_PAD, fontsize=7.0, ha='center', zorder=12)

    # 6-Pin MagSafe Pogo-Pin Buchse (Bike-Side, stationär)
    pogo_base = patches.Rectangle((-24, -24), 6, 10, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0, zorder=6)
    ax.add_patch(pogo_base)
    # Magnetische Pol-Flächen (Rot / Blau)
    ax.add_patch(patches.Rectangle((-24, -23.5), 2.5, 3.5, facecolor=MAGNET_RED, edgecolor='none', zorder=7))
    ax.add_patch(patches.Rectangle((-24, -17.5), 2.5, 3.5, facecolor=MAGNET_BLUE, edgecolor='none', zorder=7))
    # 6 vergoldete Pogo-Pins
    for py in np.linspace(-22, -16, 5):
        ax.add_patch(patches.Rectangle((-21.5, py), 3.5, 0.9, facecolor=GOLD_PAD, edgecolor='#d97706', linewidth=0.5, zorder=8))

    # =========================================================================
    # TRENNSTELLE: MAGSAFE-ABREISSKUPPLUNG (MITTE, X: -20 bis 15)
    # =========================================================================
    sep_box = patches.FancyBboxPatch((-19, -42), 30, 114,
                                     boxstyle="round,pad=0.8,rounding_size=2.5",
                                     facecolor='#0d1527', edgecolor='#0284c7',
                                     linewidth=1.2, linestyle=':', zorder=1)
    ax.add_patch(sep_box)
    ax.text(-4, 68, "TRENNSTELLE (IP67)", color=CYAN_HIGHLIGHT, fontsize=10.5, fontweight='bold', ha='center', zorder=12)
    ax.text(-4, 65, "Werkstattsichere Abreißkupplung", color=TEXT_MUTED, fontsize=8, ha='center', zorder=12)

    # 6-Pin MagSafe Stecker (Koffer-Pigtail Seite)
    plug_base = patches.Rectangle((-2, -24), 6, 10, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.0, zorder=6)
    ax.add_patch(plug_base)
    # Magnetische Pol-Gegenflächen
    ax.add_patch(patches.Rectangle((1.5, -23.5), 2.5, 3.5, facecolor=MAGNET_BLUE, edgecolor='none', zorder=7))
    ax.add_patch(patches.Rectangle((1.5, -17.5), 2.5, 3.5, facecolor=MAGNET_RED, edgecolor='none', zorder=7))
    # Goldene Kontaktpads
    for py in np.linspace(-22, -16, 5):
        ax.add_patch(patches.Rectangle((-1.5, py), 1.5, 0.9, facecolor=GOLD_PAD, edgecolor='#d97706', linewidth=0.5, zorder=8))

    # Magnetische Feldlinien & Kraftpfeile
    ax.annotate("", xy=(-18, -19), xytext=(-2, -19),
                arrowprops=dict(arrowstyle="<->", color=CYAN_HIGHLIGHT, lw=2.0, shrinkA=3, shrinkB=3), zorder=9)
    ax.annotate("", xy=(-18, -14), xytext=(-2, -14),
                arrowprops=dict(arrowstyle="<->", color=CYAN_HIGHLIGHT, lw=1.2, linestyle='--', shrinkA=3, shrinkB=3), zorder=9)
    ax.annotate("", xy=(-18, -24), xytext=(-2, -24),
                arrowprops=dict(arrowstyle="<->", color=CYAN_HIGHLIGHT, lw=1.2, linestyle='--', shrinkA=3, shrinkB=3), zorder=9)

    # Kraft-Banner
    callout_mag = patches.FancyBboxPatch((-16, -6), 24, 18, boxstyle="round,pad=0.4,rounding_size=1.2",
                                         facecolor='#022c22', edgecolor=SUCCESS_GREEN, linewidth=1.2, zorder=3)
    ax.add_patch(callout_mag)
    ax.text(-4, 7.5, "KLACK! (Zentrierung)", color='#4ade80', fontsize=8.5, fontweight='bold', ha='center', zorder=12)
    ax.text(-4, 4.0, "N52-Neodym polarisiert", color='#86efac', fontsize=7.2, ha='center', zorder=12)
    ax.text(-4, 0.0, "PLOPP! (Abreißtrennung)", color=WARNING_ORANGE, fontsize=8.5, fontweight='bold', ha='center', zorder=12)
    ax.text(-4, -3.5, "F_axial ≈ 10..15 N", color='#fdba74', fontsize=7.8, fontweight='bold', ha='center', zorder=12)

    # Mechaniker-Hinweis
    ax.text(-4, 30, "WERKSTATT-SICHERHEIT:\nMechaniker nimmt Koffer ab,\nohne nach Kabeln zu suchen.\nKein Kabel-Abriss,\nkein Stecker-Bruch!",
            color='#fde047', fontsize=7.5, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#422006', edgecolor='#eab308', lw=1.0), zorder=12)

    # =========================================================================
    # ZONE 2: KOFFER-INNENRAUM & DECKEL-POD (RECHTS, X: 15 bis 138)
    # =========================================================================
    zone2_box = patches.FancyBboxPatch((15, -42), 123, 114,
                                       boxstyle="round,pad=0.8,rounding_size=2.5",
                                       facecolor='#090f1d', edgecolor='#334155',
                                       linewidth=1.0, linestyle='--', zorder=1)
    ax.add_patch(zone2_box)
    ax.text(76, 68, "ZONE 2: KOFFER-INNENRAUM (TROCKEN, SAUBER, GESCHÜTZT)", color=ACCENT_BLUE, fontsize=11, fontweight='bold', ha='center', zorder=12)
    ax.text(76, 65, "Schlankes Flachkabel (< 2 mm), 2-Stufen-Zugentlastung, 0 Newton am USB-C Stecker", color=TEXT_MUTED, fontsize=8, ha='center', zorder=12)

    # Koffer-Umriss (Saddlebag Cutaway)
    bag_outer = Path([
        (20, -32), (120, -32), (130, 20), (128, 38), (116, 40), (22, 40), (18, 10), (20, -32)
    ])
    ax.add_patch(patches.PathPatch(bag_outer, facecolor='#131d31', edgecolor='#475569', linewidth=2.0, zorder=2))
    ax.text(70, -30, "HARLEY-DAVIDSON TOURING SADDLEBAG (ABS-KOFFER)", color='#475569', fontsize=8.5, fontweight='bold', ha='center', zorder=12)

    # Kofferdeckel (Hinged Lid)
    lid_outer = Path([
        (20, 39), (118, 39), (125, 54), (25, 54), (20, 39)
    ])
    ax.add_patch(patches.PathPatch(lid_outer, facecolor='#1e293b', edgecolor='#64748b', linewidth=1.5, zorder=2))
    ax.text(32, 46.5, "KOFFERDECKEL (Hinged Lid)", color='#94a3b8', fontsize=8, fontweight='bold', ha='left', zorder=12)

    # 1. Stufe: Seitliche Koffer-Durchführung (oberhalb Schwingenlager) & 2-Stufen-Zugentlastung
    grommet_box = patches.Rectangle((17, -24), 6, 12, facecolor='#334155', edgecolor=CYAN_HIGHLIGHT, linewidth=1.2, zorder=4)
    ax.add_patch(grommet_box)
    ax.text(20, -8, "SEITLICHE DURCHFÜHRUNG\n(Koffer-Vorderwand oberhalb Schwingenlager)\nSplit-Dichtung (010_saddlebag_hole_grommet_split.scad)", color=CYAN_HIGHLIGHT, fontsize=6.8, ha='center', fontweight='bold', zorder=12)

    clamp_tower = patches.Rectangle((23, -23), 8, 10, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.0, zorder=5)
    ax.add_patch(clamp_tower)
    ax.text(27, -18, "STUFE 1\nKLEMMTURM", color='#38bdf8', fontsize=6.5, fontweight='bold', ha='center', va='center', zorder=12)

    # Kraft-Einleitungspfeil an Stufe 1
    ax.annotate("100% Abreißkraft (10-15 N)\nwird hier in Koffer-Vorderwand eingeleitet!\n(0 N Zuglast im Innenraum)",
                xy=(31, -18), xytext=(48, -18),
                arrowprops=dict(arrowstyle="->", color=WARNING_ORANGE, lw=1.5),
                color='#fed7aa', fontsize=7.5, va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#431407', edgecolor=WARNING_ORANGE, lw=0.8), zorder=12)

    # Kofferboden Intakt Callout (Wasser-/Pfützenschutz)
    ax.text(68, -40, "KEIN LOCH IM KOFFERBODEN!\n• Koffer kann bedenkenlos auf nassem Asphalt / in Pfützen abgestellt werden\n• Durchführung liegt im geschützten Wind- & Spritzwasserschatten des Rahmens",
            color='#bbf7d0', fontsize=7.2, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#064e3b', edgecolor=SUCCESS_GREEN, lw=1.0), zorder=12)

    # Gepäck- & Dosen-Symbol am Kofferboden (zeigt Flüssigkeitsdämpfung)
    ax.add_patch(patches.Rectangle((75, -28), 12, 12, facecolor='#1e293b', edgecolor='#64748b', linewidth=0.8, zorder=3))
    ax.add_patch(patches.Rectangle((90, -28), 10, 10, facecolor='#1e293b', edgecolor='#64748b', linewidth=0.8, zorder=3))
    ax.text(88, -22, "Gepäck / Getränkedosen\n(Bodendämpfung > 20 dB)", color='#64748b', fontsize=6.5, ha='center', zorder=12)

    # Kofferdeckel-Fangband (Textilband, steigt schräg auf)
    ax.plot([30, 92], [-14, 42], color='#52525b', linewidth=7.0, zorder=3)
    ax.plot([30, 92], [-14, 42], color='#71717a', linewidth=4.0, linestyle='--', zorder=3)
    ax.text(62, 12, "Textiles Deckel-Fangband (Check Strap)", color='#a1a1aa', fontsize=7.2, ha='center', rotation=43, zorder=12)

    # Pigtail-Kabelverlauf: MagSafe-Stecker -> Seitliche Durchführung -> Stufe 1 -> Fangband -> Stufe 2
    cable_koffer_x = [4, 17, 27, 33, 92, 97]
    cable_koffer_y = [-19, -19, -19, -12, 42, 45]
    ax.plot(cable_koffer_x, cable_koffer_y, color='#0284c7', linewidth=2.5, zorder=5)
    ax.plot(cable_koffer_x, cable_koffer_y, color='#38bdf8', linewidth=1.0, zorder=6)
    ax.text(56, 19, "Schlankes Flachkabel (< 2 mm, 0 N Zuglast)", color='#38bdf8', fontsize=7.2, ha='center', rotation=43, zorder=12)

    # Kofferdeckel-Dock (saddlebag_lid_dock.scad) im Deckel
    dock_cradle = patches.FancyBboxPatch((82, 37), 44, 19, boxstyle="round,pad=0.5,rounding_size=1.5",
                                         facecolor='#0f172a', edgecolor='#38bdf8', linewidth=1.5, zorder=5)
    ax.add_patch(dock_cradle)
    ax.text(104, 53, "KOFFERDECKEL-DOCK (saddlebag_lid_dock.scad)", color=TEXT_LIGHT, fontsize=7.5, fontweight='bold', ha='center', zorder=12)

    # Stufe 2: Schnauz mit Kabelbinder-Tunnel
    ax.add_patch(patches.Rectangle((87, 40), 8, 7, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=0.8, zorder=6))
    ax.text(91, 43.5, "STUFE 2\nSCHNAUZ", color='#38bdf8', fontsize=6.0, fontweight='bold', ha='center', va='center', zorder=12)

    # Pod / Satelliten-Pod Gehäuse mit Kassette
    pod_box = patches.FancyBboxPatch((97, 40), 25, 10, boxstyle="round,pad=0.3,rounding_size=1.0",
                                    facecolor='#1e293b', edgecolor=CYAN_HIGHLIGHT, linewidth=1.2, zorder=7)
    ax.add_patch(pod_box)
    ax.text(109.5, 46.5, "SATELLITEN-POD", color=TEXT_LIGHT, fontsize=7.2, fontweight='bold', ha='center', zorder=12)
    ax.text(109.5, 43.0, "Sena / Cardo Kassette", color=CYAN_HIGHLIGHT, fontsize=6.4, ha='center', zorder=12)

    # Port B (USB-C Slim) Direktverbindung
    ax.add_patch(patches.Rectangle((95.5, 42.5), 3.0, 3.5, facecolor='#334155', edgecolor='#f59e0b', linewidth=0.8, zorder=8))
    ax.text(97, 40.5, "PORT B", color=GOLD_PAD, fontsize=6.0, fontweight='bold', ha='center', zorder=12)

    # Null Newton Callout am USB-C Port
    ax.annotate("0 NEWTON ZUGLAST!\nStecker 100% mechanisch entkoppelt",
                xy=(97, 44), xytext=(78, 28),
                arrowprops=dict(arrowstyle="->", color=SUCCESS_GREEN, lw=1.5),
                color='#bbf7d0', fontsize=7.8, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#064e3b', edgecolor=SUCCESS_GREEN, lw=1.0), zorder=12)

    # RF Abstrahlung nach oben/außen
    ax.annotate("", xy=(118, 64), xytext=(114, 51),
                arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=2.0), zorder=9)
    ax.annotate("", xy=(125, 60), xytext=(117, 49),
                arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=1.5), zorder=9)
    ax.annotate("", xy=(130, 54), xytext=(119, 46),
                arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=1.2), zorder=9)

    ax.text(115, 72, "HF-VORTEIL KOFFERDECKEL:\n• 70..75 cm über Asphalt\n• Ungestörte Fresnel-Zone\n• Liegt weit über Dosen/Getränken\n• Keine Wasser-Resonanzdämpfung!",
            color='#93c5fd', fontsize=7.0, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#082f49', edgecolor='#0284c7', lw=0.8), zorder=12)

    # Untere Dimensionsleiste & Status
    ax.plot([-100, 138], [-44, -44], color='#334155', linewidth=0.8, linestyle='--', zorder=2)
    ax.text(-62, -46.5, "MOTORRAD-CHASSIS & BORDELEKTRONIK", color=TEXT_MUTED, fontsize=7.5, ha='center', zorder=12)
    ax.text(-4, -46.5, "MAGNETISCHE ABRISS-SCHNITTSTELLE", color=CYAN_HIGHLIGHT, fontsize=7.5, ha='center', zorder=12)
    ax.text(76, -46.5, "KOFFER-INTERN: ZERO-DRILL & 100% WARTUNGSFREI", color='#38bdf8', fontsize=7.5, ha='center', zorder=12)

    # Achsen-Ausblendung
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
        spine.set_linewidth(1.0)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "saddlebag_magsafe_wiring_cad.png")
    plt.savefig(output_path, dpi=220, facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print(f"Generated: {output_path}")


if __name__ == '__main__':
    generate_saddlebag_wiring_diagram()
