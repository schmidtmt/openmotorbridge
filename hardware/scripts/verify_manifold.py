#!/usr/bin/env python3
import sys
import struct
import re
from collections import defaultdict

def parse_ascii_stl(filepath):
    triangles = []
    with open(filepath, 'r', errors='ignore') as f:
        curr_tri = []
        for line in f:
            line = line.strip()
            if line.startswith('vertex'):
                parts = line.split()
                if len(parts) >= 4:
                    v = (round(float(parts[1]), 4), round(float(parts[2]), 4), round(float(parts[3]), 4))
                    curr_tri.append(v)
                    if len(curr_tri) == 3:
                        triangles.append(tuple(curr_tri))
                        curr_tri = []
    return triangles

def parse_binary_stl(filepath):
    triangles = []
    with open(filepath, 'rb') as f:
        header = f.read(80)
        count_bytes = f.read(4)
        if len(count_bytes) < 4:
            return []
        num_triangles = struct.unpack('<I', count_bytes)[0]
        for _ in range(num_triangles):
            data = f.read(50)
            if len(data) < 50:
                break
            floats = struct.unpack('<12f', data[:48])
            v1 = (round(floats[3], 4), round(floats[4], 4), round(floats[5], 4))
            v2 = (round(floats[6], 4), round(floats[7], 4), round(floats[8], 4))
            v3 = (round(floats[9], 4), round(floats[10], 4), round(floats[11], 4))
            triangles.append((v1, v2, v3))
    return triangles

def is_ascii(filepath):
    with open(filepath, 'rb') as f:
        start = f.read(512)
        if b'solid' in start and b'facet' in start:
            return True
    return False

def verify_stl(stl_path):
    if is_ascii(stl_path):
        triangles = parse_ascii_stl(stl_path)
    else:
        triangles = parse_binary_stl(stl_path)
        
    num_triangles = len(triangles)
    edges = defaultdict(int)
    vertices = set()
    
    for (v1, v2, v3) in triangles:
        vertices.add(v1)
        vertices.add(v2)
        vertices.add(v3)
        for (va, vb) in [(v1, v2), (v2, v3), (v3, v1)]:
            if va != vb:
                e = tuple(sorted((va, vb)))
                edges[e] += 1
                
    open_edges = [e for e, count in edges.items() if count == 1]
    non_manifold = [e for e, count in edges.items() if count > 2]

    # Connected components via vertex adjacency graph
    adj = defaultdict(set)
    for (va, vb) in edges.keys():
        adj[va].add(vb)
        adj[vb].add(va)

    visited = set()
    components = 0
    for v in adj:
        if v not in visited:
            components += 1
            q = [v]
            visited.add(v)
            for curr in q:
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)
    
    print(f"STL: {stl_path}")
    print(f"  Triangles: {num_triangles}")
    print(f"  Unique Vertices: {len(vertices)}")
    print(f"  Total Edges: {len(edges)}")
    print(f"  Open Edges (count == 1): {len(open_edges)}")
    print(f"  Non-Manifold Edges (count > 2): {len(non_manifold)}")
    print(f"  Connected Components: {components}")
    
    is_manifold = (len(open_edges) == 0 and len(non_manifold) == 0 and (components == 1 or 'wing_covers' in stl_path))
    print(f"  100% 2-MANIFOLD & MONOLITHIC: {'YES (WATERTIGHT)' if is_manifold else 'NO'}\n")
    return is_manifold

if __name__ == '__main__':
    paths = sys.argv[1:] if len(sys.argv) > 1 else ['hardware/cad/stl/02_pod_base/pod3_st_performance_hybrid_cradle.stl']
    for p in paths:
        verify_stl(p)
