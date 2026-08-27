#!/usr/bin/env python3
import sys
import pcbnew

def clean_pcb(pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    tracks = list(board.GetTracks())
    for t in tracks:
        board.Remove(t)
    pcbnew.SaveBoard(pcb_path, board)
    print(f"Cleaned {pcb_path}: removed {len(tracks)} tracks/vias.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        clean_pcb(sys.argv[1])
    else:
        print("Usage: clean_pcb_tracks.py <path_to_pcb>")
