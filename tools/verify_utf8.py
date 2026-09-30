#!/usr/bin/env python3
"""
tools/verify_utf8.py - UTF-8 Integrity & Multibyte Sanitizer for OpenMotorBridge

Ensures all text files in the repository contain 100% valid UTF-8 sequences.
Can automatically sanitize fragile 3-byte/4-byte box-drawing characters into
standard 1-byte ASCII (+, -, |, *) to prevent mid-byte slicing errors in tools.
"""

import sys
import os
import argparse
import subprocess

TEXT_EXTENSIONS = (
    '.md', '.py', '.scad', '.json', '.h', '.cpp', '.c',
    '.txt', '.sh', '.yaml', '.yml', '.html', '.css', '.js'
)

BOX_TO_ASCII = {
    '-': '-', '=': '=', '|': '|', '|': '|', '-': '-', '-': '-', '|': '|', '|': '|',
    '-': '-', '-': '-', '|': '|', '|': '|', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '=': '=', '|': '|', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+', '+': '+',
    '+': '+', '+': '+', '+': '+', 'v': 'v', '^': '^', '>': '>', '<': '<', 'o': 'o',
    '#': '#', '#': '#', '*': '*', '-': '-', '--': '--', '"': '"', '"': '"', '"': '"',
    '...': '...', '->': '->'
}

def get_staged_files():
    try:
        out = subprocess.check_output(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')
        return [f.strip() for f in out.splitlines() if f.strip().endswith(TEXT_EXTENSIONS)]
    except Exception:
        return []

def get_all_repo_files():
    result = []
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root or '.system_generated' in root:
            continue
        for f in files:
            if f.endswith(TEXT_EXTENSIONS):
                result.append(os.path.normpath(os.path.join(root, f)))
    return sorted(result)

def check_file(path, fix=False, sanitize=False):
    if not os.path.exists(path):
        return True, 0

    with open(path, 'rb') as f:
        raw = f.read()

    # 1. UTF-8 Validation
    is_valid = True
    err_msg = ""
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        is_valid = False
        err_msg = f"Invalid UTF-8 at byte {e.start} ({e.reason})"

    if not is_valid:
        if fix:
            print(f"[FIXING] {path}: {err_msg}")
            # Replace invalid byte sequences cleanly
            repaired = raw.decode('utf-8', errors='replace')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(repaired)
            return True, 1
        else:
            print(f"[FAIL] {path}: {err_msg}")
            return False, 0

    # 2. Optional ASCII Sanitization of fragile box characters
    if sanitize:
        modified = text
        changes = 0
        for char, repl in BOX_TO_ASCII.items():
            if char in modified:
                changes += modified.count(char)
                modified = modified.replace(char, repl)
        if changes > 0:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(modified)
            print(f"[SANITIZED] {path}: replaced {changes} box/symbol characters with 1-byte ASCII")
            return True, changes

    return True, 0

def main():
    parser = argparse.ArgumentParser(description="UTF-8 Integrity & Multibyte Sanitizer")
    parser.add_argument('--staged', action='store_true', help="Check only git staged files")
    parser.add_argument('--fix', action='store_true', help="Automatically repair invalid UTF-8 bytes")
    parser.add_argument('--sanitize', action='store_true', help="Convert fragile box-drawing/symbols to 1-byte ASCII")
    parser.add_argument('files', nargs='*', help="Specific files to check")

    args = parser.parse_args()

    if args.files:
        files = args.files
    elif args.staged:
        files = get_staged_files()
        if not files:
            print("[INFO] No staged text files to verify.")
            sys.exit(0)
    else:
        files = get_all_repo_files()

    print(f"Scanning {len(files)} files for UTF-8 integrity...")
    all_ok = True
    total_issues = 0

    for path in files:
        ok, count = check_file(path, fix=args.fix, sanitize=args.sanitize)
        if not ok:
            all_ok = False
            total_issues += 1

    if all_ok:
        print(f"[SUCCESS] All {len(files)} files are 100% valid UTF-8!")
        sys.exit(0)
    else:
        print(f"[ERROR] Found {total_issues} files with invalid UTF-8 encoding.")
        sys.exit(1)

if __name__ == '__main__':
    main()
