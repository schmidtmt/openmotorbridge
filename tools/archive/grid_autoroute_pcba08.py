#!/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
"""
tools/grid_autoroute_pcba08.py
==============================
Grid-based autorouter for PCBA 08 SPI and Power nets:
- Routes UWB_RF orthogonally
- Uses an obstacle-aware A* pathfinder to route:
  * VCC_3V3
  * UWB_SCK
  * UWB_MOSI
  * UWB_MISO
  * UWB_CS
  * UWB_IRQ
  * UWB_RST
- Ensures strict DRC clearance >= 0.18 mm
"""

import os
import sys
import heapq
import math
import subprocess
import pcbnew

PCB_PATH = "hardware/kicad_radar_submcu/openmotorbridge_radar_submcu.kicad_pcb"
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

def to_nm(mm):
    return int(round(mm * 1e6))

def to_mm(nm):
    return float(nm) / 1e6

class GridRouter:
    def __init__(self, board, x_min=42.0, x_max=158.0, y_min=67.0, y_max=133.0, step=0.25):
        self.board = board
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.step = step
        
        self.nx = int(math.ceil((x_max - x_min) / step)) + 1
        self.ny = int(math.ceil((y_max - y_min) / step)) + 1
        
        # 2 layers: 0: F.Cu, 1: B.Cu
        # obstacle grid: True = blocked
        self.blocked = [
            [False] * (self.nx * self.ny),  # F.Cu
            [False] * (self.nx * self.ny)   # B.Cu
        ]
        
    def to_grid(self, x, y):
        gx = int(round((x - self.x_min) / self.step))
        gy = int(round((y - self.y_min) / self.step))
        return gx, gy

    def to_world(self, gx, gy):
        x = self.x_min + gx * self.step
        y = self.y_min + gy * self.step
        return x, y

    def in_bounds(self, gx, gy):
        return 0 <= gx < self.nx and 0 <= gy < self.ny

    def block_circle(self, layer_idx, cx, cy, radius_mm):
        cgx, cgy = self.to_grid(cx, cy)
        gr = int(math.ceil(radius_mm / self.step))
        for dgx in range(-gr, gr + 1):
            for dgy in range(-gr, gr + 1):
                gx, gy = cgx + dgx, cgy + dgy
                if self.in_bounds(gx, gy):
                    wx, wy = self.to_world(gx, gy)
                    if (wx - cx)**2 + (wy - cy)**2 <= radius_mm**2:
                        self.blocked[layer_idx][gy * self.nx + gx] = True

    def block_segment(self, layer_idx, x1, y1, x2, y2, radius_mm):
        # Sample along segment
        length = math.hypot(x2 - x1, y2 - y1)
        steps = max(1, int(math.ceil(length / (self.step * 0.5))))
        for s in range(steps + 1):
            t = float(s) / steps
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            self.block_circle(layer_idx, x, y, radius_mm)

    def load_obstacles(self, exclude_nets=set()):
        # 1. Inner cutout: (69.5, 74.5) to (130.5, 125.5)
        # Block both layers in cutout
        for gx in range(self.nx):
            for gy in range(self.ny):
                wx, wy = self.to_world(gx, gy)
                # Outer border margin: 0.3mm from edge
                if wx < 42.8 or wx > 157.2 or wy < 67.8 or wy > 132.2:
                    self.blocked[0][gy * self.nx + gx] = True
                    self.blocked[1][gy * self.nx + gx] = True
                # Inner cutout with margin
                if (69.2 <= wx <= 130.8) and (74.2 <= wy <= 125.8):
                    self.blocked[0][gy * self.nx + gx] = True
                    self.blocked[1][gy * self.nx + gx] = True

        # 2. Existing tracks and vias
        clearance = 0.28  # 0.18 mm clearance + 0.10 mm half-width
        for t in self.board.GetTracks():
            if t.GetNetname() in exclude_nets:
                continue
            s, e = t.GetStart(), t.GetEnd()
            sx, sy = to_mm(s.x), to_mm(s.y)
            ex, ey = to_mm(e.x), to_mm(e.y)
            w = to_mm(t.GetWidth())
            r = (w / 2.0) + clearance
            if isinstance(t, pcbnew.PCB_VIA):
                # Vias block both layers
                self.block_circle(0, sx, sy, r)
                self.block_circle(1, sx, sy, r)
            else:
                layer_idx = 0 if t.GetLayer() == pcbnew.F_Cu else 1
                self.block_segment(layer_idx, sx, sy, ex, ey, r)

        # 3. Pads of components
        for p in self.board.GetPads():
            if p.GetNetname() in exclude_nets:
                continue
            pos = p.GetPosition()
            px, py = to_mm(pos.x), to_mm(pos.y)
            # Size of pad
            sz = p.GetSize()
            max_r = (max(to_mm(sz.x), to_mm(sz.y)) / 2.0) + clearance
            layers = p.GetLayerSet()
            if layers.Contains(pcbnew.F_Cu):
                self.block_circle(0, px, py, max_r)
            if layers.Contains(pcbnew.B_Cu):
                self.block_circle(1, px, py, max_r)

    def find_path(self, start_xyz, target_xyz, max_iterations=500000):
        # start_xyz = (x, y, layer_idx)
        sgx, sgy = self.to_grid(start_xyz[0], start_xyz[1])
        tgx, tgy = self.to_grid(target_xyz[0], target_xyz[1])
        s_layer = start_xyz[2]
        t_layer = target_xyz[2]

        start_state = (sgx, sgy, s_layer)
        target_state = (tgx, tgy, t_layer)

        # Priority queue for A*
        pq = []
        heapq.heappush(pq, (0.0, 0.0, start_state))
        came_from = {}
        cost_so_far = {start_state: 0.0}

        def heuristic(a):
            ax, ay = self.to_world(a[0], a[1])
            tx, ty = self.to_world(tgx, tgy)
            dist = math.hypot(tx - ax, ty - ay)
            layer_cost = 5.0 if a[2] != t_layer else 0.0
            return dist + layer_cost

        # 8 directions on same layer
        dirs = [
            (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
            (1, 1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (-1, -1, 1.414)
        ]

        iterations = 0
        while pq:
            iterations += 1
            if iterations > max_iterations:
                print(f"Pathfinding exceeded {max_iterations} iterations!")
                return None

            _, current_cost, current = heapq.heappop(pq)
            cgx, cgy, clay = current

            # Check target (reach target grid cell on target layer)
            if current == target_state or (cgx == tgx and cgy == tgy and clay == t_layer):
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            # 1. Neighbor planar moves
            for dx, dy, step_cost in dirs:
                ngx, ngy = cgx + dx, cgy + dy
                if self.in_bounds(ngx, ngy):
                    # Check if blocked (target cell is allowed to be blocked by pad)
                    if (ngx, ngy, clay) != target_state and self.blocked[clay][ngy * self.nx + ngx]:
                        continue
                    nxt = (ngx, ngy, clay)
                    new_cost = current_cost + step_cost * self.step
                    if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                        cost_so_far[nxt] = new_cost
                        priority = new_cost + heuristic(nxt)
                        came_from[nxt] = current
                        heapq.heappush(pq, (priority, new_cost, nxt))

            # 2. Via move (switch layer)
            other_layer = 1 - clay
            # Via costs 15.0 and requires both layers free at this point
            if (cgx, cgy, other_layer) != target_state and not self.blocked[other_layer][cgy * self.nx + cgx]:
                nxt = (cgx, cgy, other_layer)
                new_cost = current_cost + 15.0
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    priority = new_cost + heuristic(nxt)
                    came_from[nxt] = current
                    heapq.heappush(pq, (priority, new_cost, nxt))

        return None

def simplify_path(router, grid_path):
    if not grid_path or len(grid_path) < 2:
        return []
    
    # Break into segments by layer and collinearity
    segments = []
    
    cur_start = grid_path[0]
    cur_dir = None
    
    for i in range(1, len(grid_path)):
        p_prev = grid_path[i - 1]
        p_cur = grid_path[i]
        
        # Check layer transition (via)
        if p_cur[2] != p_prev[2]:
            # Close previous segment
            sx, sy = router.to_world(cur_start[0], cur_start[1])
            ex, ey = router.to_world(p_prev[0], p_prev[1])
            if (sx, sy) != (ex, ey):
                segments.append(('track', cur_start[2], (sx, sy), (ex, ey)))
            # Add via
            vx, vy = router.to_world(p_prev[0], p_prev[1])
            segments.append(('via', vx, vy))
            cur_start = p_cur
            cur_dir = None
            continue
            
        dx = p_cur[0] - p_prev[0]
        dy = p_cur[1] - p_prev[1]
        step_dir = (dx, dy)
        
        if cur_dir is None:
            cur_dir = step_dir
        elif cur_dir != step_dir:
            # Direction change
            sx, sy = router.to_world(cur_start[0], cur_start[1])
            ex, ey = router.to_world(p_prev[0], p_prev[1])
            segments.append(('track', cur_start[2], (sx, sy), (ex, ey)))
            cur_start = p_prev
            cur_dir = step_dir
            
    # Final segment
    sx, sy = router.to_world(cur_start[0], cur_start[1])
    ex, ey = router.to_world(grid_path[-1][0], grid_path[-1][1])
    if (sx, sy) != (ex, ey):
        segments.append(('track', cur_start[2], (sx, sy), (ex, ey)))
        
    return segments

def main():
    board = pcbnew.LoadBoard(PCB_PATH)
    print("Autorouting PCBA 08...")

    # 1. Clean old test tracks for these nets
    cleanup_nets = ["UWB_RF", "UWB_SCK", "UWB_MOSI", "UWB_MISO", "UWB_CS", "UWB_IRQ", "UWB_RST"]
    to_remove = [t for t in board.GetTracks() if t.GetNetname() in cleanup_nets]
    for t in to_remove:
        board.Remove(t)
    print(f"✓ Removed {len(to_remove)} existing/temporary tracks.")

    # 2. Add orthogonal RF track: (145.25, 98.35) -> (145.25, 96.50) -> (152.00, 96.50)
    net_rf = board.FindNet("UWB_RF")
    t1 = pcbnew.PCB_TRACK(board)
    t1.SetNet(net_rf); t1.SetLayer(pcbnew.B_Cu); t1.SetWidth(to_nm(0.35))
    t1.SetStart(pcbnew.VECTOR2I(to_nm(145.25), to_nm(98.35)))
    t1.SetEnd(pcbnew.VECTOR2I(to_nm(145.25), to_nm(96.50)))
    board.Add(t1)

    t2 = pcbnew.PCB_TRACK(board)
    t2.SetNet(net_rf); t2.SetLayer(pcbnew.B_Cu); t2.SetWidth(to_nm(0.35))
    t2.SetStart(pcbnew.VECTOR2I(to_nm(145.25), to_nm(96.50)))
    t2.SetEnd(pcbnew.VECTOR2I(to_nm(152.00), to_nm(96.50)))
    board.Add(t2)
    print("✓ Added orthogonal RF track.")

    # 3. Setup router
    router = GridRouter(board, step=0.30)
    print("Building obstacle grid...")
    router.load_obstacles(exclude_nets=set(cleanup_nets))
    print(f"✓ Obstacle grid built: {router.nx} x {router.ny} cells.")

    # 4. Route nets
    nets_to_route = [
        ("UWB_SCK",  (47.25, 106.00, 1), (144.75, 101.25, 1)),
        ("UWB_MOSI", (47.25, 104.50, 1), (143.55, 100.55, 1)),
        ("UWB_MISO", (47.25, 103.00, 1), (144.25, 101.25, 1)),
        ("UWB_CS",   (47.25, 100.00, 1), (143.55, 100.05, 1)),
        ("UWB_IRQ",  (47.25,  98.50, 1), (144.25,  98.35, 1)),
        ("UWB_RST",  (64.75, 101.50, 1), (143.55,  99.05, 1)),
        ("VCC_3V3",  (151.00, 87.35, 1), (144.75,  98.35, 1)),
    ]

    for net_name, start_xyz, target_xyz in nets_to_route:
        net = board.FindNet(net_name)
        print(f"Routing {net_name} from {start_xyz[:2]} to {target_xyz[:2]}...")
        path = router.find_path(start_xyz, target_xyz)
        if not path:
            print(f"❌ FAILED to route {net_name}!")
            continue

        segs = simplify_path(router, path)
        print(f"  ✓ Found path with {len(segs)} segments.")
        
        # Add to board
        for item in segs:
            if item[0] == 'track':
                _, layer_idx, (sx, sy), (ex, ey) = item
                layer = pcbnew.F_Cu if layer_idx == 0 else pcbnew.B_Cu
                tr = pcbnew.PCB_TRACK(board)
                tr.SetNet(net)
                tr.SetLayer(layer)
                tr.SetWidth(to_nm(0.18))
                tr.SetStart(pcbnew.VECTOR2I(to_nm(sx), to_nm(sy)))
                tr.SetEnd(pcbnew.VECTOR2I(to_nm(ex), to_nm(ey)))
                board.Add(tr)
                # Mark as obstacle for subsequent nets
                router.block_segment(layer_idx, sx, sy, ex, ey, 0.28)
            elif item[0] == 'via':
                _, vx, vy = item
                via = pcbnew.PCB_VIA(board)
                via.SetNet(net)
                via.SetPosition(pcbnew.VECTOR2I(to_nm(vx), to_nm(vy)))
                via.SetDrill(to_nm(0.25))
                via.SetWidth(to_nm(0.50))
                via.SetViaType(pcbnew.VIATYPE_THROUGH)
                board.Add(via)
                router.block_circle(0, vx, vy, 0.45)
                router.block_circle(1, vx, vy, 0.45)

    # Connect exact pad endpoints
    for net_name, start_xyz, target_xyz in nets_to_route:
        net = board.FindNet(net_name)
        # Check start pad connection
        sx, sy, sl = start_xyz
        layer = pcbnew.F_Cu if sl == 0 else pcbnew.B_Cu
        sgx, sgy = router.to_grid(sx, sy)
        swx, swy = router.to_world(sgx, sgy)
        if (swx, swy) != (sx, sy):
            tr = pcbnew.PCB_TRACK(board)
            tr.SetNet(net); tr.SetLayer(layer); tr.SetWidth(to_nm(0.18))
            tr.SetStart(pcbnew.VECTOR2I(to_nm(sx), to_nm(sy)))
            tr.SetEnd(pcbnew.VECTOR2I(to_nm(swx), to_nm(swy)))
            board.Add(tr)

        # Check target pad connection
        tx, ty, tl = target_xyz
        layer = pcbnew.F_Cu if tl == 0 else pcbnew.B_Cu
        tgx, tgy = router.to_grid(tx, ty)
        twx, twy = router.to_world(tgx, tgy)
        if (twx, twy) != (tx, ty):
            tr = pcbnew.PCB_TRACK(board)
            tr.SetNet(net); tr.SetLayer(layer); tr.SetWidth(to_nm(0.18))
            tr.SetStart(pcbnew.VECTOR2I(to_nm(twx), to_nm(twy)))
            tr.SetEnd(pcbnew.VECTOR2I(to_nm(tx), to_nm(ty)))
            board.Add(tr)

    # Refill zones
    for zone in board.Zones():
        zone.SetNeedRefill(True)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    print("✓ Refilled all zones.")

    board.Save(PCB_PATH)
    print(f"✓ Saved updated {PCB_PATH}")

if __name__ == "__main__":
    main()
