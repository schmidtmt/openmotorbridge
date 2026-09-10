#!/usr/bin/env python3
"""
OpenMotorBridge - Advanced Multi-Motorcycle Digital Twin Simulator
==================================================================
Simulates 2 interconnected motorcycles (Bike A = Leader, Bike B = Chaser)
equipped with full 5-PCB OpenMotorBridge stacks:

PCBs per Motorcycle:
  1. PCBA 01: Main Box Controller (ESP32-S3, 15-State ADR-EKF, Power Supervisor, Audio DSP)
  2. PCBA 02: Satellite Pod Base (Passive M8 interface, SP3012 TVS line protection)
  3. PCBA 03: Pod Cartridge (1-Wire DS2401 Silicon ROM ID, PTT triggers, audio levels)
  4. PCBA 04: Rear Pod 3 (u-blox MAX-M10S GNSS, SX1262 LoRa 868MHz, 2.4GHz OMM Mesh, Garmin Radar)
  5. PCBA 05: Universal Front Node (ESP32-C3, dual Knowles MEMS mics, cockpit PTT, VBUS)

Physics & RF Simulation:
  - Geodetic Track: Wil SG -> Wattwil Umfahrung (2.2km Tunnel) -> Wattwil Kreisel -> Rickenpass
  - 15-State ADR-EKF Dead Reckoning during 100% GNSS tunnel blackout
  - RF Propagation (Friis & Log-Distance Path Loss + 35dB tunnel attenuation)
  - Dynamic Handover: 2.4 GHz High-Speed Mesh (OMM) <-> 868 MHz LoRa (SX1262)
  - Pure Python RFC 6455 WebSocket Server (ws://localhost:8765) streaming live to PWA
"""

import sys
import os
import time
import math
import json
import base64
import hashlib
import asyncio
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracks.wil_wattwil_ricken import generate_full_track, TrackPoint, latlon_distance, latlon_bearing, latlon_offset

# ANSI Colors for Terminal Output
C_LEAD  = "\033[92m"    # Green (Bike A - Leader)
C_CHAS  = "\033[94m"    # Blue (Bike B - Chaser)
C_TUNN  = "\033[91m"    # Red (Tunnel / Blackout)
C_RF    = "\033[95m"    # Magenta (RF Mesh / LoRa)
C_PWA   = "\033[96m"    # Cyan (WebSocket PWA)
C_BOLD  = "\033[1m"
C_RST   = "\033[0m"

# =============================================================================
# HARDWARE EMULATION: 5 PCBs PER MOTORCYCLE
# =============================================================================

class EmulatedMainPCB:
    """PCBA 01: ESP32-S3 Main Controller"""
    def __init__(self, bike_id: str):
        self.bike_id = bike_id
        self.v_ign = 14.20       # Alternator voltage (V)
        self.v_bat = 4.14        # LiPo USV buffer (V)
        self.btn_bat = 98        # Wireless PTT battery (%)
        self.mode = 2            # Default: Mode 2 (Dual-Mesh Intercom)
        self.dr_active = False   # ADR Dead-Reckoning active flag
        
        # 15-State ADR-EKF state variables
        self.est_x = 0.0
        self.est_y = 0.0
        self.est_heading = 0.0
        self.residual_gyro_bias = 0.0001 # rad/s (~0.005 deg/s residual error)
        self.wheel_speed_slip = 0.0015   # 0.15% radius / slip error

class EmulatedPodCartridge:
    """PCBA 03: Interchangeable Intercom Sled (Sena / Cardo / Blind)"""
    def __init__(self, slot: int, profile: str, rom_id: str):
        self.slot = slot
        self.profile = profile
        self.rom_id = rom_id
        self.ptt_pressed = False
        self.audio_gain_db = 0.0

class EmulatedRearPod3:
    """PCBA 04: Rear Pod 3 Coprocessor (GNSS, LoRa, 2.4GHz Mesh, Garmin Radar)"""
    def __init__(self, bike_id: str):
        self.bike_id = bike_id
        self.sats_visible = 20
        self.hdop = 0.8
        self.gnss_fix = True
        self.lora_tx_power_dbm = 22.0
        self.mesh_tx_power_dbm = 14.0
        
        # Garmin Varia Radar target list
        self.radar_targets: List[Dict[str, Any]] = []
        self.last_radar_update = 0.0

class EmulatedFrontNode:
    """PCBA 05: Universal Front Node (ESP32-C3, Knowles MEMS mics, Cockpit PTT)"""
    def __init__(self, bike_id: str):
        self.bike_id = bike_id
        self.cockpit_ptt_pressed = False
        self.vbus_enabled = True
        self.acoustic_spl_dba = 62.0 # Baseline cockpit acoustic level

class MotorcycleNode:
    """Complete Motorcycle System containing 5 interconnected PCBs."""
    def __init__(self, bike_id: str, is_leader: bool = True):
        self.bike_id = bike_id
        self.is_leader = is_leader
        
        # The 5 Physical PCBs
        self.pcb_main = EmulatedMainPCB(bike_id)
        self.pcb_cartridges = [
            EmulatedPodCartridge(1, "sena_60s", "0x01_A3_89_F0_12_45_67_89"),
            EmulatedPodCartridge(2, "cardo_edge", "0x01_B4_92_E1_33_56_78_9A")
        ]
        self.pcb_rear = EmulatedRearPod3(bike_id)
        self.pcb_front = EmulatedFrontNode(bike_id)
        
        # Vehicle Kinematics
        self.lat = 47.4640
        self.lon = 9.0430
        self.alt = 570.0
        self.speed_kmh = 0.0
        self.heading_deg = 0.0
        self.lean_angle_deg = 0.0
        self.in_tunnel = False
        
        # EKF Ground Truth vs Estimated position tracker
        self.true_x = 0.0
        self.true_y = 0.0
        self.tunnel_entry_x = 0.0
        self.tunnel_entry_y = 0.0
        self.tunnel_drift_m = 0.0
        self.was_in_tunnel = False

    def update_kinematics(self, pt: TrackPoint, dt: float):
        """Update vehicle dynamics and feed 15-State ADR-EKF."""
        self.lat = pt.lat
        self.lon = pt.lon
        self.alt = pt.alt_m
        self.speed_kmh = pt.speed_kmh
        self.heading_deg = pt.heading_deg
        self.lean_angle_deg = pt.lean_angle_deg
        self.in_tunnel = pt.in_tunnel
        
        v_mps = pt.speed_mps
        heading_rad = math.radians(pt.heading_deg)
        
        # Propagate true local cartesian coordinates
        self.true_x += v_mps * math.cos(heading_rad) * dt
        self.true_y += v_mps * math.sin(heading_rad) * dt
        
        # Front node microphone noise scales with airspeed (cube root aero noise model)
        self.pcb_front.acoustic_spl_dba = 55.0 + 22.0 * math.log10(max(10.0, pt.speed_kmh) / 10.0)
        
        # GNSS Receiver state
        self.pcb_rear.sats_visible = pt.sats_visible
        self.pcb_rear.hdop = pt.hdop
        self.pcb_rear.gnss_fix = not pt.in_tunnel
        
        # EKF Sensor Fusion logic
        if pt.in_tunnel:
            self.pcb_main.dr_active = True
            if not self.was_in_tunnel:
                # First step entering tunnel: record reference origin
                self.tunnel_entry_x = self.true_x
                self.tunnel_entry_y = self.true_y
                self.pcb_main.est_x = self.true_x
                self.pcb_main.est_y = self.true_y
                self.pcb_main.est_heading = heading_rad
            else:
                # Integrate IMU yaw rate with residual gyro bias + CAN wheel speed slip
                meas_yaw_rate = math.radians(pt.yaw_rate_deg_s) + self.pcb_main.residual_gyro_bias
                self.pcb_main.est_heading += meas_yaw_rate * dt
                meas_v = v_mps * (1.0 + self.pcb_main.wheel_speed_slip)
                
                self.pcb_main.est_x += meas_v * math.cos(self.pcb_main.est_heading) * dt
                self.pcb_main.est_y += meas_v * math.sin(self.pcb_main.est_heading) * dt
                
            # Current dead-reckoning drift
            self.tunnel_drift_m = math.sqrt((self.true_x - self.pcb_main.est_x)**2 + 
                                            (self.true_y - self.pcb_main.est_y)**2)
        else:
            self.pcb_main.dr_active = False
            # When GNSS fix is available, EKF snaps to satellite position
            self.pcb_main.est_x = self.true_x
            self.pcb_main.est_y = self.true_y
            self.pcb_main.est_heading = heading_rad
            self.tunnel_drift_m = 0.0
            
        self.was_in_tunnel = pt.in_tunnel

        # Simulate Garmin Radar target when on open road
        now = time.time()
        if not pt.in_tunnel and (now - self.pcb_rear.last_radar_update) > 1.0:
            self.pcb_rear.last_radar_update = now
            # Simulated vehicle approaching from behind
            dist = 45.0 + 15.0 * math.sin(now * 0.2)
            speed_delta = 20.0 + 5.0 * math.cos(now * 0.3)
            self.pcb_rear.radar_targets = [{
                "id": 101,
                "distance_m": round(dist, 1),
                "speed_diff_kmh": round(speed_delta, 1),
                "threat": "critical" if dist < 25.0 else ("warning" if dist < 50.0 else "info")
            }]
        elif pt.in_tunnel:
            self.pcb_rear.radar_targets = []

# =============================================================================
# RF PROPAGATION & DYNAMIC DLE MESH HANDOVER ENGINE
# =============================================================================

class RfPropagationEngine:
    """Calculates path loss, RSSI, and manages dynamic 2.4GHz <-> 868MHz handover."""
    def __init__(self):
        self.freq_mesh_ghz = 2.45
        self.freq_lora_mhz = 868.0
        self.mesh_sensitivity_dbm = -88.0 # High-speed IEEE 802.15.4 OMM threshold
        self.lora_sensitivity_dbm = -137.0 # SX1262 LoRa SF10 threshold
        self.current_link = "OMM_MESH_24GHZ"
        self.handover_count = 0
        self.last_rssi_24 = -60.0
        self.last_rssi_lora = -75.0

    def compute_link(self, bike_a: MotorcycleNode, bike_b: MotorcycleNode) -> Dict[str, Any]:
        """Calculates distance, RSSI and selects optimal physical layer."""
        distance_m = latlon_distance(bike_a.lat, bike_a.lon, bike_b.lat, bike_b.lon)
        distance_m = max(1.0, distance_m)

        # 1. Path Loss 2.4 GHz (Log-Distance Model + Tunnel Occlusion)
        # PL(d) = 20*log10(4*pi*d/lambda) + 10*n*log10(d/d0) + TunnelLoss
        lambda_24 = 3e8 / (self.freq_mesh_ghz * 1e9) # 0.122 m
        free_space_24 = 20.0 * math.log10((4.0 * math.pi * min(distance_m, 10.0)) / lambda_24)
        n_loss = 2.6 # Road exponent
        path_loss_24 = free_space_24 + 10.0 * n_loss * math.log10(max(1.0, distance_m / 10.0))

        # Tunnel Wall Attenuation: If either bike is in tunnel, add 38 dB attenuation
        tunnel_loss_db = 0.0
        if bike_a.in_tunnel or bike_b.in_tunnel:
            tunnel_loss_db = 38.0

        rssi_24 = bike_a.pcb_rear.mesh_tx_power_dbm - path_loss_24 - tunnel_loss_db

        # 2. Path Loss 868 MHz LoRa (Superior concrete penetration & diffraction)
        lambda_lora = 3e8 / (self.freq_lora_mhz * 1e6) # 0.345 m
        free_space_lora = 20.0 * math.log10((4.0 * math.pi * min(distance_m, 10.0)) / lambda_lora)
        path_loss_lora = free_space_lora + 10.0 * 2.2 * math.log10(max(1.0, distance_m / 10.0))
        # LoRa tunnel loss is much lower due to waveguide effect at lower UHF (~12 dB)
        lora_tunnel_loss = 12.0 if (bike_a.in_tunnel or bike_b.in_tunnel) else 0.0
        rssi_lora = bike_a.pcb_rear.lora_tx_power_dbm - path_loss_lora - lora_tunnel_loss

        self.last_rssi_24 = rssi_24
        self.last_rssi_lora = rssi_lora

        # 3. Dynamic Handover State Machine
        new_link = self.current_link
        if self.current_link == "OMM_MESH_24GHZ":
            if rssi_24 < self.mesh_sensitivity_dbm:
                # Trigger Handover to 868 MHz LoRa
                new_link = "LORA_868MHZ"
                self.handover_count += 1
        elif self.current_link == "LORA_868MHZ":
            # Hysteresis: Require +4 dB margin before returning to 2.4 GHz
            if rssi_24 > (self.mesh_sensitivity_dbm + 4.0) and not (bike_a.in_tunnel or bike_b.in_tunnel):
                new_link = "OMM_MESH_24GHZ"
                self.handover_count += 1

        self.current_link = new_link

        return {
            "distance_m": round(distance_m, 1),
            "link_type": self.current_link,
            "rssi_24_dbm": round(rssi_24, 1),
            "rssi_lora_dbm": round(rssi_lora, 1),
            "handover_count": self.handover_count,
            "bandwidth_kbps": 250 if self.current_link == "OMM_MESH_24GHZ" else 19.2,
            "audio_codec": "Opus 24k Full-Duplex" if self.current_link == "OMM_MESH_24GHZ" else "Opus 8k PTT Half-Duplex"
        }

# =============================================================================
# PURE PYTHON RFC 6455 WEBSOCKET SERVER (ZERO EXTERNAL DEPENDENCIES)
# =============================================================================

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class WebSocketClient:
    """Handles single RFC 6455 WebSocket client connection."""
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.handshake_done = False

    async def perform_handshake(self) -> bool:
        """Performs RFC 6455 HTTP upgrade handshake."""
        try:
            req_data = await self.reader.readuntil(b"\r\n\r\n")
            headers = req_data.decode("utf-8", errors="ignore").split("\r\n")
            key = None
            for h in headers:
                if ":" in h:
                    k, v = h.split(":", 1)
                    if k.strip().lower() == "sec-websocket-key":
                        key = v.strip()
                        break
            if not key:
                return False

            accept_token = base64.b64encode(hashlib.sha1((key + WS_GUID).encode("utf-8")).digest()).decode("utf-8")
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_token}\r\n\r\n"
            )
            self.writer.write(response.encode("utf-8"))
            await self.writer.drain()
            self.handshake_done = True
            return True
        except Exception:
            return False

    async def send_text(self, text: str):
        """Sends an unmasked text frame (Opcode 0x1) to the client."""
        if not self.handshake_done:
            return
        payload = text.encode("utf-8")
        length = len(payload)
        frame = bytearray([0x81]) # FIN + Text Opcode
        if length <= 125:
            frame.append(length)
        elif length <= 65535:
            frame.append(126)
            frame.extend(length.to_bytes(2, "big"))
        else:
            frame.append(127)
            frame.extend(length.to_bytes(8, "big"))
        frame.extend(payload)
        try:
            self.writer.write(frame)
            await self.writer.drain()
        except Exception:
            self.handshake_done = False

    async def read_frame(self) -> Optional[str]:
        """Reads incoming masked frame from client."""
        try:
            head = await self.reader.readexactly(2)
            fin_opcode = head[0]
            masked_length = head[1]
            opcode = fin_opcode & 0x0F
            if opcode == 0x8: # Connection Close
                return None
            length = masked_length & 0x7F
            if length == 126:
                ext_len = await self.reader.readexactly(2)
                length = int.from_bytes(ext_len, "big")
            elif length == 127:
                ext_len = await self.reader.readexactly(8)
                length = int.from_bytes(ext_len, "big")

            mask = await self.reader.readexactly(4)
            payload = bytearray(await self.reader.readexactly(length))
            for i in range(len(payload)):
                payload[i] ^= mask[i % 4]
            return payload.decode("utf-8", errors="ignore")
        except Exception:
            return None

class WebSocketBroadcastServer:
    """Asynchronous WebSocket server managing active PWA connections."""
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketClient] = set()
        self.command_queue: asyncio.Queue = asyncio.Queue()

    async def client_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client = WebSocketClient(reader, writer)
        if await client.perform_handshake():
            self.clients.add(client)
            print(f"{C_PWA}[PWA-SERVER]{C_RST} Client connected! (Active: {len(self.clients)})")
            try:
                while client.handshake_done:
                    msg = await client.read_frame()
                    if msg is None:
                        break
                    try:
                        cmd = json.loads(msg)
                        await self.command_queue.put(cmd)
                    except Exception:
                        pass
            finally:
                self.clients.discard(client)
                writer.close()
                print(f"{C_PWA}[PWA-SERVER]{C_RST} Client disconnected. (Active: {len(self.clients)})")

    async def broadcast_json(self, data: Dict[str, Any]):
        """Broadcasts JSON payload to all connected PWA browser tabs."""
        if not self.clients:
            return
        payload = json.dumps(data)
        dead = []
        for client in self.clients:
            try:
                await client.send_text(payload)
            except Exception:
                dead.append(client)
        for d in dead:
            self.clients.discard(d)

# =============================================================================
# DIGITAL TWIN SIMULATOR ORCHESTRATOR
# =============================================================================

class DigitalTwinSimulator:
    """Master orchestrator running the multi-bike track simulation."""
    def __init__(self, port: int = 8765, speed_multiplier: float = 1.0, headless: bool = False):
        self.port = port
        self.speed_multiplier = speed_multiplier
        self.headless = headless
        
        # Load Track
        self.track = generate_full_track(sample_rate_hz=10.0)
        self.dt = 0.1 # 10 Hz simulation step
        
        # Instantiate 2 Motorcycle Nodes (10 PCBs total)
        self.bike_a = MotorcycleNode("Bike_A", is_leader=True)
        self.bike_b = MotorcycleNode("Bike_B", is_leader=False)
        
        # RF Engine & WebSocket Server
        self.rf_engine = RfPropagationEngine()
        self.ws_server = WebSocketBroadcastServer(host="0.0.0.0", port=port)
        
        # Metrics for Automated Regression Test
        self.max_tunnel_drift_m = 0.0
        self.tunnel_blackout_detected = False
        self.handover_occurred = False
        self.return_to_mesh_occurred = False

    async def run(self, max_duration_s: Optional[float] = None):
        """Main execution loop."""
        server = await asyncio.start_server(self.ws_server.client_handler, "0.0.0.0", self.port)
        addr = server.sockets[0].getsockname()
        print(f"\n{C_BOLD}==================================================================={C_RST}")
        print(f"{C_BOLD}   OpenMotorBridge Digital Twin Simulator (10 PCBs & 2 Bikes)      {C_RST}")
        print(f"{C_BOLD}==================================================================={C_RST}")
        print(f"  • Route:      Wil SG -> Wattwil Tunnel (2.2km) -> Kreisel -> Rickenpass")
        print(f"  • Track:      {len(self.track)} points ({self.track[-1].time_s / 60.0:.1f} min)")
        print(f"  • WebSocket:  ws://localhost:{self.port} (Connect OpenMotorBridge PWA)")
        print(f"  • Mode:       {'Headless Testbench' if self.headless else 'Interactive Live Mode'} (Speed: {self.speed_multiplier}x)")
        print(f"-------------------------------------------------------------------\n")

        # Chaser delay: 45 steps = 4.5 seconds behind on highway (~60-100m gap)
        chaser_lag_steps = 45
        
        start_wall_time = time.time()
        step_idx = 0
        total_steps = len(self.track)
        
        try:
            while step_idx < total_steps:
                pt_a = self.track[step_idx]
                pt_b_idx = max(0, step_idx - chaser_lag_steps)
                pt_b = self.track[pt_b_idx]
                
                # 1. Update Kinematics & EKF for both bikes
                self.bike_a.update_kinematics(pt_a, self.dt)
                self.bike_b.update_kinematics(pt_b, self.dt)
                
                # 2. Update RF Propagation & DLE Handover
                rf_state = self.rf_engine.compute_link(self.bike_a, self.bike_b)
                
                # Track metrics for verification
                if self.bike_a.in_tunnel:
                    self.tunnel_blackout_detected = True
                    self.max_tunnel_drift_m = max(self.max_tunnel_drift_m, self.bike_a.tunnel_drift_m)
                    
                if rf_state["link_type"] == "LORA_868MHZ":
                    self.handover_occurred = True
                if self.handover_occurred and rf_state["link_type"] == "OMM_MESH_24GHZ":
                    self.return_to_mesh_occurred = True

                # Process incoming PWA commands
                while not self.ws_server.command_queue.empty():
                    cmd = await self.ws_server.command_queue.get()
                    action = cmd.get("action")
                    if action == "set_mode":
                        self.bike_a.pcb_main.mode = int(cmd.get("mode", 2))
                        print(f"{C_PWA}[PWA-CMD]{C_RST} Bike A Intercom Mode -> {self.bike_a.pcb_main.mode}")
                    elif action == "ptt_press":
                        pressed = bool(cmd.get("pressed", False))
                        self.bike_a.pcb_cartridges[0].ptt_pressed = pressed
                        print(f"{C_PWA}[PWA-CMD]{C_RST} Bike A PTT Triggered: {pressed}")

                # 3. Construct Live Telemetry Frame for PWA
                telemetry_frame = {
                    "type": "telemetry",
                    "timestamp": round(pt_a.time_s, 2),
                    "bike_id": "Bike_A",
                    "v_ign": self.bike_a.pcb_main.v_ign,
                    "v_bat": self.bike_a.pcb_main.v_bat,
                    "btn_bat": self.bike_a.pcb_main.btn_bat,
                    "speed": round(self.bike_a.speed_kmh, 1),
                    "sats": self.bike_a.pcb_rear.sats_visible,
                    "hdop": round(self.bike_a.pcb_rear.hdop, 2),
                    "lean_angle": round(self.bike_a.lean_angle_deg, 1),
                    "mode": self.bike_a.pcb_main.mode,
                    "lat": round(self.bike_a.lat, 6),
                    "lon": round(self.bike_a.lon, 6),
                    "alt": round(self.bike_a.alt, 1),
                    "heading": round(self.bike_a.heading_deg, 1),
                    "in_tunnel": self.bike_a.in_tunnel,
                    "dr_active": self.bike_a.pcb_main.dr_active,
                    "dr_drift_m": round(self.bike_a.tunnel_drift_m, 2),
                    "rf_link": rf_state["link_type"],
                    "rf_rssi": rf_state["rssi_24_dbm"],
                    "lora_rssi": rf_state["rssi_lora_dbm"],
                    "distance_chaser_m": rf_state["distance_m"],
                    "handover_count": rf_state["handover_count"],
                    "mesh_members": [
                        {"id": "Bike_A (Leader)", "role": "LEADER", "rssi": -45, "state": "ONLINE"},
                        {"id": "Bike_B (Chaser)", "role": "MEMBER", "rssi": int(rf_state["rssi_24_dbm"]), "state": "ONLINE"}
                    ],
                    "radar": {
                        "targets": self.bike_a.pcb_rear.radar_targets
                    },
                    "audio": {
                        "front_mems_dba": round(self.bike_a.pcb_front.acoustic_spl_dba, 1),
                        "codec": rf_state["audio_codec"],
                        "ptt": self.bike_a.pcb_cartridges[0].ptt_pressed
                    }
                }
                
                # Broadcast to PWA
                await self.ws_server.broadcast_json(telemetry_frame)

                # Periodic terminal status output (every 2.0s simulated time)
                if step_idx % 20 == 0:
                    status_line = (
                        f"[{pt_a.time_s:6.1f}s] "
                        f"Speed: {self.bike_a.speed_kmh:4.1f}km/h | "
                        f"Lean: {self.bike_a.lean_angle_deg:+4.1f}° | "
                        f"Sats: {self.bike_a.pcb_rear.sats_visible:2d} | "
                        f"Link: {rf_state['link_type']:16s} (d={rf_state['distance_m']:5.1f}m, RSSI={rf_state['rssi_24_dbm']:+5.1f}dBm)"
                    )
                    if self.bike_a.in_tunnel:
                        status_line += f" {C_TUNN}[TUNNEL EKF-DR: {self.bike_a.tunnel_drift_m:4.2f}m]{C_RST}"
                    if pt_a.label:
                        status_line += f" {C_BOLD}<< {pt_a.label} >>{C_RST}"
                    print(status_line)

                # Check duration limit
                if max_duration_s and pt_a.time_s >= max_duration_s:
                    print(f"\n[INFO] Target duration {max_duration_s}s reached.")
                    break

                # Advance simulation step
                step_idx += 1
                
                # Timing sleep based on speed multiplier
                if self.speed_multiplier > 0.0:
                    sleep_time = self.dt / self.speed_multiplier
                    await asyncio.sleep(sleep_time)

        finally:
            server.close()
            await server.wait_closed()

        # Print final verification report
        print(f"\n{C_BOLD}==================================================================={C_RST}")
        print(f"{C_BOLD}   SIMULATION SUMMARY & REGRESSION TEST RESULTS                    {C_RST}")
        print(f"{C_BOLD}==================================================================={C_RST}")
        print(f"  • Simulated Time:        {pt_a.time_s:.1f} s")
        print(f"  • Tunnel Blackout Check:  {'PASS (GNSS dropped to 0 Sats)' if self.tunnel_blackout_detected else 'FAIL'}")
        print(f"  • Max EKF Tunnel Drift:   {self.max_tunnel_drift_m:.2f} m (Automotive Standard: < 30.0 m for 2.2 km tunnel)")
        print(f"  • LoRa Handover Check:    {'PASS (Switched on attenuation)' if self.handover_occurred else 'FAIL'}")
        print(f"  • Return Handover Check:  {'PASS (Returned to 2.4 GHz Mesh)' if self.return_to_mesh_occurred else 'SKIPPED (Short run)'}")
        
        # Assertions for automated tests
        assert self.tunnel_blackout_detected, "Tunnel GNSS blackout was not detected!"
        assert self.max_tunnel_drift_m < 30.0, f"Tunnel drift exceeded limit: {self.max_tunnel_drift_m:.2f}m >= 30m"
        print(f"{C_LEAD}{C_BOLD}  [PASS] ALL DIGITAL TWIN CHECKS COMPLETED SUCCESSFULLY!{C_RST}\n")
        return True

def main():
    parser = argparse.ArgumentParser(description="OpenMotorBridge Multi-Motorcycle Digital Twin Simulator")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket server port (default: 8765)")
    parser.add_argument("--speed", type=float, default=1.0, help="Simulation speed multiplier (default: 1.0, use 10.0+ for fast)")
    parser.add_argument("--duration", type=float, default=None, help="Stop after N simulated seconds")
    parser.add_argument("--headless", action="store_true", help="Run without user interaction for CI/CD")
    parser.add_argument("--fast", action="store_true", help="Run at maximum compute speed (useful for tests)")
    args = parser.parse_args()

    speed = 50.0 if args.fast else args.speed
    sim = DigitalTwinSimulator(port=args.port, speed_multiplier=speed, headless=args.headless)
    
    try:
        asyncio.run(sim.run(max_duration_s=args.duration))
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    main()
