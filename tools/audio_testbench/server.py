#!/usr/bin/env python3
"""
=============================================================================
OpenMotorBridge - Live Audio DSP Testbench Server
=============================================================================
Lightweight local test server for real-time acoustic & DSP testing:
- Runs on http://localhost:8088
- Zero external dependencies (uses standard Python library)
- Automatically opens default web browser
- Serves Web Audio DSP Studio with full microphone & media access

Usage:
  python3 tools/audio_testbench/server.py [--port 8088]
=============================================================================
"""

import os
import sys
import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

class TestbenchRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable aggressive caching for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Concise logging
        if "200" not in args[1]:
            super().log_message(format, *args)

def main():
    parser = argparse.ArgumentParser(description="OpenMotorBridge Live Audio DSP Testbench Server")
    parser.add_argument("--port", type=int, default=8088, help="Port to bind server (default: 8088)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open web browser")
    args = parser.parse_args()

    testbench_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(testbench_dir)

    server_address = ('127.0.0.1', args.port)
    httpd = HTTPServer(server_address, TestbenchRequestHandler)

    url = f"http://localhost:{args.port}"
    print("=" * 76)
    print("      🎧 OPENMOTORBRIDGE LIVE AUDIO DSP STUDIO & REALTIME TESTBENCH       ")
    print("=" * 76)
    print(f"✓ Serving testbench from: {testbench_dir}")
    print(f"✓ Running at:             {url}")
    print("\nFeatures available:")
    print("  • Real-Time Headset & Microphone Ingestion")
    print("  • 15ms Attack / 800ms Release Raised-Cosine Ducking (audio_dsp_pipeline.cpp)")
    print("  • 0-160 km/h Motorcycle Speedometer with Ambient Transparency & Wind Gate")
    print("  • 1-Wire Hot-Swap Profiles (Sena 60S, Cardo Pro, OMM LoRa Radio, Mute)")
    print("  • Integrated Riding-Synthwave Player & Custom MP3 Drag-and-Drop")
    print("  • Live Spectrum Visualizer & Triple VU-Meters")
    print("\nPress Ctrl+C to stop server.")
    print("=" * 76)

    if not args.no_browser:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping OpenMotorBridge Live Audio Testbench. Goodbye!")
        httpd.server_close()
        sys.exit(0)

if __name__ == '__main__':
    main()
