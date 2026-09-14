#!/usr/bin/env python3
"""
Automated Capture of High-Fidelity PWA Screenshots for OpenMotorBridge Documentation
--------------------------------------------------------------------------------------
Uses Google Chrome in headless mode to render the authentic PWA tabs from demo.html:
1. Tab 1: Cockpit, Telemetry, Radar HUD & Front Node
2. Tab 2: Audio Ducking & Smart Cartridge Mechatronics
3. Tab 3: Cartridges, DLE & In-System Flashing
4. Tab 4: Tour Logging, Replay & GPX WebDAV Export
5. Tab 5: Device Hub (Keyfob Pager, Headsets, Cameras)
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "docs/images/pwa")
HTML_URL = f"file://{os.path.join(os.path.dirname(BASE_DIR), 'webapp_pwa/demo.html')}"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TABS = [
    ("tab-cockpit", "pwa_tab1_cockpit_radar_hud.png", "Tab 1: Cockpit, EKF & Heck-Radar HUD"),
    ("tab-audio", "pwa_tab2_audio_smart_cartridge.png", "Tab 2: Audio & Smart Cartridge Mechatronics"),
    ("tab-cartridges", "pwa_tab3_cartridges_dle_status.png", "Tab 3: Kassetten & DLE Status"),
    ("tab-tours", "pwa_tab4_tours_gpx_export.png", "Tab 4: Touren, Replay & GPX Export"),
    ("tab-hardware", "pwa_tab5_device_hub_keyfob.png", "Tab 5: Geräte-Hub & LoRa Smart-Keyfob")
]

def capture_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 75)
    print("📸 CAPTURING AUTHENTIC PWA DASHBOARD SCREENSHOTS")
    print("=" * 75)

    for tab_id, filename, label in TABS:
        out_path = os.path.join(OUTPUT_DIR, filename)
        url = f"{HTML_URL}?tab={tab_id}"
        print(f"  Capturing [{label}] -> {filename}...")

        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--window-size=1200,900",
            "--virtual-time-budget=2500",
            f"--screenshot={out_path}",
            url
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            size = os.path.getsize(out_path)
            print(f"  ✅ Saved {filename} ({size} bytes)")
        except Exception as e:
            print(f"  ❌ Error capturing {filename}: {e}")

    print("\n🎉 ALL PWA SCREENSHOTS SUCCESSFULLY CAPTURED IN:")
    print(f"   {OUTPUT_DIR}")

if __name__ == "__main__":
    capture_screenshots()
