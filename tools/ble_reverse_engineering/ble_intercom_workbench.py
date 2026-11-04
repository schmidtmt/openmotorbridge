#!/usr/bin/env python3
"""
OpenMotorBridge - BLE Intercom Reverse-Engineering & Protocol Workbench
=======================================================================
Target Devices:
  - Cardo Packtalk Edge / Pro / Neo (Cardo Connect App)
  - Sena Spider X Slim / ST1 / RT1 / 50S / 60S (Sena Motorcycles App)

Capabilities:
  1. `scan`          - Live BLE scanner (via Bleak/CoreBluetooth) with Manufacturer
                       Data & Service UUID decoding for Cardo & Sena headsets.
  2. `dump-gatt`     - Connects to headset, enumerates full GATT tree (Services,
                       Characteristics, Descriptors, Properties) & reads all state
                       values into a JSON snapshot.
  3. `diff`          - Compares two GATT snapshots (Before vs. After changing a
                       setting in the Cardo/Sena smartphone app) and pinpoints the
                       exact Characteristic UUID and byte/bit offsets that changed.
  4. `monitor`       - Live interactive GATT Notification/Indication sniffer +
                       labeled session recorder + live hex command injector.
                       Automatically computes byte-diffs against previous frames
                       and detects checksum algorithms (XOR, Sum8, 2's Complement,
                       CRC-8, CRC-16/CCITT).
  5. `parse-capture` - Pure-Python binary parser for:
                         * Android `btsnoop_hci.log` (RFC 1761)
                         * Apple Xcode `PacketLogger` (`.pklg`)
                         * Wireshark `.pcap` & `.pcapng` (HCI H4 / L2CAP / ATT)
                       Extracts all ATT Write Requests (0x12), Write Commands (0x52),
                       Notifications (0x1B), Indications (0x1D), and Read Responses (0x0B).
  6. `export-header` - Converts labeled & verified BLE commands from a session JSON
                       directly into a C/C++ header (`generated_intercom_ble_cmds.h`)
                       for `firmware/smart_cartridge/src/cartridge_ble_client.cpp`.
"""

from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import json
import os
import struct
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Known Vendor Signatures & UUID Hints (Cardo & Sena)
# ---------------------------------------------------------------------------
KNOWN_VENDORS = {
    "CARDO": {
        "name_keywords": ["CARDO", "PACKTALK", "PT-EDGE", "PT_EDGE", "FREECOM", "SPIRIT"],
        "service_hints": {
            "0000fe59": "Nordic DFU / Cardo BLE Service",
            "0000180f": "Battery Service",
            "0000180a": "Device Information",
        },
    },
    "SENA": {
        "name_keywords": ["SENA", "SPIDER", "50S", "50R", "60S", "30K", "SF", "RC3", "RC4"],
        "service_hints": {
            "0000ffe0": "Sena Remote / Command GATT Service (0xFFE0)",
            "0000ffe1": "Sena Remote / Command GATT Characteristic (0xFFE1)",
            "0000180f": "Battery Service",
            "0000180a": "Device Information",
        },
    },
}

ATT_OPCODES = {
    0x01: "ERROR_RSP",
    0x02: "MTU_REQ",
    0x03: "MTU_RSP",
    0x04: "FIND_INFO_REQ",
    0x05: "FIND_INFO_RSP",
    0x08: "READ_BY_TYPE_REQ",
    0x09: "READ_BY_TYPE_RSP",
    0x0A: "READ_REQ",
    0x0B: "READ_RSP",
    0x10: "READ_BY_GRP_TYPE_REQ",
    0x11: "READ_BY_GRP_TYPE_RSP",
    0x12: "WRITE_REQ",
    0x13: "WRITE_RSP",
    0x1B: "HANDLE_VALUE_NTF",
    0x1D: "HANDLE_VALUE_IND",
    0x1E: "HANDLE_VALUE_CFM",
    0x52: "WRITE_CMD",
}

# ---------------------------------------------------------------------------
# Standardized OpenMotorBridge OEM Action Catalog for `learn-profile` Wizard
# ---------------------------------------------------------------------------
OEM_LEARNING_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "CARTRIDGE_OPCODE_MESH_TOGGLE",
        "opcode": 0x05,
        "capability_flag": "can_mesh_toggle",
        "title": "Mesh Intercom EIN / AUS (Mesh Toggle / DMC Mute)",
        "instruction": "Drücke JETZT in der App oder am Headset 'Mesh Intercom Ein/Aus' (bzw. DMC Mute).",
    },
    {
        "id": "CARTRIDGE_OPCODE_OPEN_GROUP_SW",
        "opcode": 0x06,
        "capability_flag": "can_group_toggle",
        "title": "Open Mesh <-> Group Mesh / Private Chat umschalten",
        "instruction": "Schalte JETZT zwischen 'Open Mesh' und 'Group Mesh' (bzw. Private Chat) um.",
    },
    {
        "id": "OEM_ACTION_CHANNEL_SET_1",
        "opcode": 0x11,
        "capability_flag": "can_channel_select",
        "channel_num": 1,
        "title": "Open Mesh Kanal 1 wählen",
        "instruction": "Stelle in der App JETZT auf 'Kanal 1' (Referenzpunkt 1 für Kanal-Formel).",
    },
    {
        "id": "OEM_ACTION_CHANNEL_SET_2",
        "opcode": 0x12,
        "capability_flag": "can_channel_select",
        "channel_num": 2,
        "title": "Open Mesh Kanal 2 wählen",
        "instruction": "Stelle in der App JETZT auf 'Kanal 2' (Referenzpunkt 2 für Kanal-Formel).",
    },
    {
        "id": "OEM_ACTION_CHANNEL_SET_3",
        "opcode": 0x13,
        "capability_flag": "can_channel_select",
        "channel_num": 3,
        "title": "Open Mesh Kanal 3 wählen",
        "instruction": "Stelle in der App JETZT auf 'Kanal 3' (Referenzpunkt 3 zur Verifikation von Kanal 1..9).",
    },
    {
        "id": "CARTRIDGE_OPCODE_CHANNEL_NEXT",
        "opcode": 0x07,
        "capability_flag": "can_channel_select",
        "title": "Kanal + (Nächster Kanal)",
        "instruction": "Betätige JETZT 'Kanal +' (falls als Direktbefehl vorhanden, sonst 's' für Skip).",
    },
    {
        "id": "CARTRIDGE_OPCODE_CHANNEL_PREV",
        "opcode": 0x08,
        "capability_flag": "can_channel_select",
        "title": "Kanal - (Vorheriger Kanal)",
        "instruction": "Betätige JETZT 'Kanal -' (falls als Direktbefehl vorhanden, sonst 's' für Skip).",
    },
    {
        "id": "CARTRIDGE_OPCODE_VOLUME_UP",
        "opcode": 0x03,
        "capability_flag": "can_volume",
        "title": "Lautstärke + (Volume Up)",
        "instruction": "Erhöhe JETZT die Lautstärke um 1 Stufe ('Volume +').",
    },
    {
        "id": "CARTRIDGE_OPCODE_VOLUME_DOWN",
        "opcode": 0x04,
        "capability_flag": "can_volume",
        "title": "Lautstärke - (Volume Down)",
        "instruction": "Verringere JETZT die Lautstärke um 1 Stufe ('Volume -').",
    },
    {
        "id": "OEM_ACTION_MIC_MUTE_ON",
        "opcode": 0x20,
        "capability_flag": "can_mic_mute",
        "title": "Mikrofon Stumm EIN (Mic Mute On)",
        "instruction": "Schalte JETZT das Mikrofon STUMM ('Mic Mute EIN').",
    },
    {
        "id": "OEM_ACTION_MIC_MUTE_OFF",
        "opcode": 0x21,
        "capability_flag": "can_mic_mute",
        "title": "Mikrofon Stumm AUS (Mic Mute Off)",
        "instruction": "Hebe JETZT die Mikrofon-Stummschaltung wieder auf ('Mic Mute AUS').",
    },
    {
        "id": "OEM_ACTION_AUDIO_MIX_HIGH",
        "opcode": 0x22,
        "capability_flag": "can_telemetry",
        "title": "Audio-Overlay / Multitasking-Empfindlichkeit ändern",
        "instruction": "Ändere JETZT die Audio-Mix / Audio-Overlay-Empfindlichkeit in der App.",
    },
    {
        "id": "OEM_ACTION_VOX_TOGGLE",
        "opcode": 0x24,
        "capability_flag": "can_telemetry",
        "title": "VOX Sprachaktivierung / Sidetone EIN/AUS",
        "instruction": "Schalte JETZT 'VOX' oder 'Sidetone' in der App um.",
    },
    {
        "id": "CARTRIDGE_OPCODE_POWER_OFF",
        "opcode": 0x02,
        "capability_flag": "can_power_off",
        "title": "Power-Off / Standby per BLE",
        "instruction": "Falls die App ein Ausschalten/Standby per BLE erlaubt, JETZT auslösen (sonst 's').",
    },
]


# ---------------------------------------------------------------------------
# Checksum & Frame Structure Analyzer
# ---------------------------------------------------------------------------
def crc8_standard(data: bytes, poly: int = 0x07, init: int = 0x00) -> int:
    crc = init
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


def crc16_ccitt(data: bytes, poly: int = 0x1021, init: int = 0xFFFF) -> int:
    crc = init
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def analyze_frame_checksum(raw: bytes) -> List[str]:
    """
    Tests common intercom BLE protocol checksums on the trailing byte(s) of `raw`.
    Checks full payload (excluding last byte) as well as payload skipping 1- or 2-byte sync headers.
    """
    hits: List[str] = []
    if len(raw) < 3:
        return hits

    last_byte = raw[-1]
    body_all = raw[:-1]

    for start_idx, label_prefix in [(0, "all[0..-2]"), (1, "body[1..-2]"), (2, "body[2..-2]")]:
        if len(body_all) <= start_idx:
            continue
        sub = body_all[start_idx:]

        # 1. XOR Checksum
        xor_val = 0
        for b in sub:
            xor_val ^= b
        if xor_val == last_byte:
            hits.append(f"XOR({label_prefix}) == 0x{last_byte:02X}")

        # 2. 8-bit Modulo-256 Sum
        sum_val = sum(sub) & 0xFF
        if sum_val == last_byte:
            hits.append(f"SUM8({label_prefix}) == 0x{last_byte:02X}")

        # 3. Two's Complement of Sum ((-sum) & 0xFF)
        twos_val = (-sum(sub)) & 0xFF
        if twos_val == last_byte:
            hits.append(f"TWOS_COMP({label_prefix}) == 0x{last_byte:02X}")

        # 4. Ones' Complement (~sum & 0xFF)
        ones_val = (~sum(sub)) & 0xFF
        if ones_val == last_byte:
            hits.append(f"ONES_COMP({label_prefix}) == 0x{last_byte:02X}")

        # 5. CRC-8 (poly 0x07 and 0x31)
        if crc8_standard(sub, 0x07, 0x00) == last_byte:
            hits.append(f"CRC8_07({label_prefix}) == 0x{last_byte:02X}")
        if crc8_standard(sub, 0x31, 0x00) == last_byte:
            hits.append(f"CRC8_31({label_prefix}) == 0x{last_byte:02X}")

    # 6. Check 16-bit CRC-CCITT (Big-Endian and Little-Endian in last 2 bytes)
    if len(raw) >= 4:
        body16 = raw[:-2]
        last16_be = (raw[-2] << 8) | raw[-1]
        last16_le = (raw[-1] << 8) | raw[-2]
        for init_val in (0xFFFF, 0x0000):
            c16 = crc16_ccitt(body16, 0x1021, init_val)
            if c16 == last16_be:
                hits.append(f"CRC16_CCITT_BE(init=0x{init_val:04X}) == 0x{last16_be:04X}")
            if c16 == last16_le:
                hits.append(f"CRC16_CCITT_LE(init=0x{init_val:04X}) == 0x{last16_le:04X}")

    return hits


def analyze_frame_structure(raw: bytes, prev_raw: Optional[bytes] = None) -> Dict[str, Any]:
    """
    Inspects a BLE GATT payload for length fields, printable ASCII strings,
    checksum matches, and byte-level diffs against a previous payload on the same handle.
    """
    hex_spaced = " ".join(f"{b:02X}" for b in raw)
    ascii_repr = "".join(chr(b) if 32 <= b < 127 else "." for b in raw)
    checksums = analyze_frame_checksum(raw)

    length_hints: List[str] = []
    n = len(raw)
    for idx in range(min(4, n)):
        val = raw[idx]
        if val == n and n > 2:
            length_hints.append(f"byte[{idx}]=0x{val:02X} == total_len({n})")
        elif val == n - idx - 1 and (n - idx - 1) > 1:
            length_hints.append(f"byte[{idx}]=0x{val:02X} == remaining_len({n - idx - 1})")
        elif val == n - idx - 2 and (n - idx - 2) > 1:
            length_hints.append(f"byte[{idx}]=0x{val:02X} == payload_len_excl_crc({n - idx - 2})")

    changed_bytes: List[Dict[str, Any]] = []
    if prev_raw is not None:
        max_len = max(len(raw), len(prev_raw))
        for i in range(max_len):
            b_old = prev_raw[i] if i < len(prev_raw) else None
            b_new = raw[i] if i < len(raw) else None
            if b_old != b_new:
                changed_bytes.append({
                    "offset": i,
                    "old_hex": f"0x{b_old:02X}" if b_old is not None else "None",
                    "new_hex": f"0x{b_new:02X}" if b_new is not None else "None",
                    "old_dec": b_old,
                    "new_dec": b_new,
                })

    return {
        "length": n,
        "hex": hex_spaced,
        "ascii": ascii_repr,
        "checksum_candidates": checksums,
        "length_field_hints": length_hints,
        "diff_vs_previous": changed_bytes,
    }


def format_diff_line(raw: bytes, prev_raw: Optional[bytes]) -> str:
    """Formats hex string with [XX] brackets around bytes that changed compared to prev_raw."""
    if prev_raw is None:
        return " ".join(f"{b:02X}" for b in raw)
    parts: List[str] = []
    for i, b in enumerate(raw):
        if i >= len(prev_raw) or prev_raw[i] != b:
            parts.append(f"[{b:02X}]")
        else:
            parts.append(f" {b:02X} ")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Pure-Python Binary Capture Parser (BTSnoop / PacketLogger .pklg / PCAP / PCAPNG)
# ---------------------------------------------------------------------------
@dataclass
class CapturedAttEvent:
    index: int
    timestamp_iso: str
    rel_time_s: float
    direction: str          # "TX (App->Headset)" | "RX (Headset->App)" | "UNKNOWN"
    att_opcode: int
    att_opcode_name: str
    att_handle: int
    payload_hex: str
    payload_bytes: bytes = field(repr=False)
    label: str = ""
    uuid_hint: str = ""
    analysis: Dict[str, Any] = field(default_factory=dict)


def _extract_att_from_hci_acl(acl_bytes: bytes, direction: str, idx: int, ts_sec: float, t0: float,
                              prev_by_handle: Dict[int, bytes]) -> Optional[CapturedAttEvent]:
    """
    Parses an HCI ACL packet:
      [Handle+Flags: 2B LE] [ACL Total Len: 2B LE] [L2CAP Len: 2B LE] [L2CAP CID: 2B LE] [ATT PDU...]
    """
    if len(acl_bytes) < 9:
        return None
    handle_flags, acl_len, l2cap_len, l2cap_cid = struct.unpack_from("<HHHH", acl_bytes, 0)
    pb_flag = (handle_flags >> 12) & 0x03
    # Only start of L2CAP PDU (pb_flag in (0x00, 0x02)) on ATT fixed channel CID 0x0004
    if l2cap_cid != 0x0004 or pb_flag == 0x01:
        return None

    att_pdu = acl_bytes[8:8 + l2cap_len]
    if len(att_pdu) < 3:
        return None

    opcode = att_pdu[0]
    # Focus on data-carrying ATT opcodes: Write Req (0x12), Write Cmd (0x52),
    # Handle Value Notification (0x1B), Handle Value Indication (0x1D), Read Rsp (0x0B)
    if opcode in (0x12, 0x52, 0x1B, 0x1D):
        if len(att_pdu) < 3:
            return None
        att_handle = struct.unpack_from("<H", att_pdu, 1)[0]
        value = att_pdu[3:]
    elif opcode == 0x0B:
        att_handle = 0x0000
        value = att_pdu[1:]
    else:
        return None

    prev_val = prev_by_handle.get(att_handle)
    analysis = analyze_frame_structure(value, prev_val)
    prev_by_handle[att_handle] = value

    ts_iso = dt.datetime.fromtimestamp(ts_sec, tz=dt.timezone.utc).isoformat()
    return CapturedAttEvent(
        index=idx,
        timestamp_iso=ts_iso,
        rel_time_s=round(ts_sec - t0, 6),
        direction=direction,
        att_opcode=opcode,
        att_opcode_name=ATT_OPCODES.get(opcode, f"0x{opcode:02X}"),
        att_handle=att_handle,
        payload_hex=" ".join(f"{b:02X}" for b in value),
        payload_bytes=value,
        analysis=analysis,
    )


def parse_btsnoop_file(data: bytes) -> List[CapturedAttEvent]:
    """Parses Android `btsnoop_hci.log` (RFC 1761) binary data."""
    if len(data) < 16 or data[:8] != b"btsnoop\x00":
        raise ValueError("Not a valid btsnoop_hci.log file (missing 'btsnoop\\0' magic header).")
    version, datalink = struct.unpack_from(">II", data, 8)
    offset = 16
    events: List[CapturedAttEvent] = []
    prev_by_handle: Dict[int, bytes] = {}
    t0: Optional[float] = None
    pkt_idx = 0

    # BTSnoop epoch offset (microseconds between 0000-01-01 and 1970-01-01)
    BTSNOOP_EPOCH_DELTA_US = 0x00DCDDB30F2F8000

    while offset + 24 <= len(data):
        orig_len, incl_len, flags, drops, ts_us = struct.unpack_from(">IIIIQ", data, offset)
        offset += 24
        pkt = data[offset:offset + incl_len]
        offset += incl_len
        pkt_idx += 1

        ts_sec = max(0.0, (ts_us - BTSNOOP_EPOCH_DELTA_US) / 1_000_000.0)
        if t0 is None:
            t0 = ts_sec

        # Direction bit 0 of flags: 0 = Host->Controller (TX), 1 = Controller->Host (RX)
        is_rx = bool(flags & 0x01)
        direction = "RX (Headset->App)" if is_rx else "TX (App->Headset)"

        # Datalink 1002 = HCI UART (H4) where pkt[0] is packet type (0x02 = ACL Data)
        # Datalink 1001 = Unencapsulated HCI where flags bit 1 indicates Command/Event vs ACL
        acl_payload: Optional[bytes] = None
        if datalink == 1002 and len(pkt) > 1 and pkt[0] == 0x02:
            acl_payload = pkt[1:]
        elif datalink == 1001 and not (flags & 0x02):
            acl_payload = pkt
        elif len(pkt) > 1 and pkt[0] == 0x02:
            acl_payload = pkt[1:]

        if acl_payload:
            ev = _extract_att_from_hci_acl(acl_payload, direction, pkt_idx, ts_sec, t0, prev_by_handle)
            if ev:
                events.append(ev)

    return events


def parse_apple_pklg_file(data: bytes) -> List[CapturedAttEvent]:
    """Parses macOS / iOS Xcode PacketLogger (`.pklg`) binary capture files."""
    offset = 0
    events: List[CapturedAttEvent] = []
    prev_by_handle: Dict[int, bytes] = {}
    t0: Optional[float] = None
    pkt_idx = 0

    while offset + 13 <= len(data):
        # PacketLogger record: [len: 4B BE] [ts_sec: 4B BE] [ts_usec: 4B BE] [type: 1B] [payload...]
        rec_len, ts_s, ts_us, pkt_type = struct.unpack_from(">IIIB", data, offset)
        if rec_len < 9 or offset + 4 + rec_len > len(data):
            break
        payload = data[offset + 13:offset + 4 + rec_len]
        offset += 4 + rec_len
        pkt_idx += 1

        ts_sec = float(ts_s) + float(ts_us) / 1_000_000.0
        if t0 is None:
            t0 = ts_sec

        # PacketLogger type: 0x02 = ACL TX (Host->Controller), 0x03 = ACL RX (Controller->Host)
        if pkt_type in (0x02, 0x03):
            direction = "TX (App->Headset)" if pkt_type == 0x02 else "RX (Headset->App)"
            ev = _extract_att_from_hci_acl(payload, direction, pkt_idx, ts_sec, t0, prev_by_handle)
            if ev:
                events.append(ev)

    return events


def parse_pcap_file(data: bytes) -> List[CapturedAttEvent]:
    """Parses classic libpcap (`.pcap`) files with Bluetooth HCI H4 / Linux Cooked / ACL link types."""
    magic = struct.unpack_from("<I", data, 0)[0]
    endian = "<" if magic in (0xA1B2C3D4, 0xA1B23C4D) else ">"
    _, _, _, _, _, network = struct.unpack_from(endian + "IHHiIII", data, 0)
    offset = 24
    events: List[CapturedAttEvent] = []
    prev_by_handle: Dict[int, bytes] = {}
    t0: Optional[float] = None
    pkt_idx = 0

    while offset + 16 <= len(data):
        ts_s, ts_us, incl_len, orig_len = struct.unpack_from(endian + "IIII", data, offset)
        offset += 16
        pkt = data[offset:offset + incl_len]
        offset += incl_len
        pkt_idx += 1

        ts_sec = float(ts_s) + float(ts_us) / 1_000_000.0
        if t0 is None:
            t0 = ts_sec

        acl_payload: Optional[bytes] = None
        direction = "UNKNOWN"
        # LINKTYPE_BLUETOOTH_HCI_H4_WITH_PHDR (201): 4B direction header + 1B H4 type
        if network == 201 and len(pkt) > 5 and pkt[4] == 0x02:
            is_rx = struct.unpack_from(">I", pkt, 0)[0] != 0
            direction = "RX (Headset->App)" if is_rx else "TX (App->Headset)"
            acl_payload = pkt[5:]
        # LINKTYPE_BLUETOOTH_HCI_H4 (187): 1B H4 type
        elif network == 187 and len(pkt) > 1 and pkt[0] == 0x02:
            acl_payload = pkt[1:]
        elif len(pkt) > 1 and pkt[0] == 0x02:
            acl_payload = pkt[1:]

        if acl_payload:
            ev = _extract_att_from_hci_acl(acl_payload, direction, pkt_idx, ts_sec, t0, prev_by_handle)
            if ev:
                events.append(ev)

    return events


def parse_capture_auto(file_path: Path) -> List[CapturedAttEvent]:
    """Auto-detects and parses BTSnoop, Apple PacketLogger (.pklg), or PCAP files."""
    data = file_path.read_bytes()
    if data[:8] == b"btsnoop\x00":
        return parse_btsnoop_file(data)
    if len(data) >= 4 and struct.unpack_from("<I", data, 0)[0] in (0xA1B2C3D4, 0xD4C3B2A1, 0xA1B23C4D, 0x4D3CB2A1):
        return parse_pcap_file(data)
    # Default to Apple PacketLogger (.pklg)
    return parse_apple_pklg_file(data)


# ---------------------------------------------------------------------------
# Differential GATT Snapshot Analyzer (Before vs. After App Setting Change)
# ---------------------------------------------------------------------------
def diff_gatt_snapshots(snap_before: Dict[str, Any], snap_after: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Compares two GATT characteristic state dumps (`dump-gatt` JSON files)
    and returns a list of characteristics whose values changed.
    """
    chars_before = {
        c["uuid"] + f"@{c.get('handle', 0)}": c
        for s in snap_before.get("services", [])
        for c in s.get("characteristics", [])
    }
    chars_after = {
        c["uuid"] + f"@{c.get('handle', 0)}": c
        for s in snap_after.get("services", [])
        for c in s.get("characteristics", [])
    }

    diffs: List[Dict[str, Any]] = []
    for key, c_after in chars_after.items():
        c_before = chars_before.get(key)
        if not c_before:
            continue
        hex_before = c_before.get("read_hex")
        hex_after = c_after.get("read_hex")
        if hex_before != hex_after and (hex_before is not None or hex_after is not None):
            b_old = bytes.fromhex(hex_before.replace(" ", "")) if hex_before else b""
            b_new = bytes.fromhex(hex_after.replace(" ", "")) if hex_after else b""
            analysis = analyze_frame_structure(b_new, b_old)
            diffs.append({
                "characteristic_uuid": c_after["uuid"],
                "handle": c_after.get("handle"),
                "description": c_after.get("description", ""),
                "old_hex": hex_before,
                "new_hex": hex_after,
                "diff_visual": format_diff_line(b_new, b_old),
                "changed_bytes": analysis["diff_vs_previous"],
                "checksum_candidates": analysis["checksum_candidates"],
            })
    return diffs


# ---------------------------------------------------------------------------
# C/C++ Firmware Header Generator for `PCBA 03` (`cartridge_ble_client.cpp`)
# ---------------------------------------------------------------------------
def generate_cpp_header(session_data: Dict[str, Any], output_path: Path) -> str:
    """
    Generates a ready-to-include C/C++ header (`generated_intercom_ble_cmds.h`)
    containing verified BLE GATT command byte arrays for Cardo Packtalk Edge
    and Sena Spider X Slim.
    """
    device_name = session_data.get("device_name", "UNKNOWN_INTERCOM")
    vendor = session_data.get("vendor", "GENERIC").upper()
    commands = session_data.get("commands", [])

    lines = [
        "// ============================================================================",
        "// AUTO-GENERATED BY tools/ble_reverse_engineering/ble_intercom_workbench.py",
        f"// Source Device : {device_name} ({vendor})",
        f"// Generated At  : {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "// Target        : firmware/smart_cartridge/src/cartridge_ble_client.cpp",
        "// ============================================================================",
        "#pragma once",
        "",
        "#include <stdint.h>",
        "#include <stddef.h>",
        "",
        "typedef struct {",
        "    const char*    action_name;",
        "    uint16_t       att_handle;",
        "    const char*    char_uuid;",
        "    const uint8_t* payload;",
        "    size_t         payload_len;",
        "    bool           write_without_response;",
        "} IntercomCapturedBleCmd_t;",
        "",
    ]

    struct_entries: List[str] = []
    for idx, cmd in enumerate(commands):
        label = cmd.get("label") or f"CMD_{idx:02d}"
        safe_sym = "".join(ch if ch.isalnum() else "_" for ch in label.upper()).strip("_")
        raw_bytes = bytes.fromhex(cmd["payload_hex"].replace(" ", ""))
        byte_Initializer = ", ".join(f"0x{b:02X}" for b in raw_bytes)
        handle = int(cmd.get("att_handle", 0))
        uuid_str = cmd.get("char_uuid", "00000000-0000-0000-0000-000000000000")
        no_rsp = "true" if cmd.get("att_opcode_name") == "WRITE_CMD" else "false"

        arr_name = f"k_{vendor.lower()}_{safe_sym.lower()}_bytes_{idx}"
        lines.append(f"// Action: {label} | Handle: 0x{handle:04X} | Raw: {cmd['payload_hex']}")
        lines.append(f"static const uint8_t {arr_name}[{len(raw_bytes)}] = {{ {byte_Initializer} }};")
        lines.append("")
        struct_entries.append(
            f'    {{ "{label}", 0x{handle:04X}, "{uuid_str}", {arr_name}, sizeof({arr_name}), {no_rsp} }}'
        )

    lines.append(f"static const IntercomCapturedBleCmd_t k_{vendor.lower()}_captured_commands[] = {{")
    lines.append(",\n".join(struct_entries))
    lines.append("};")
    lines.append("")
    lines.append(
        f"static const size_t k_{vendor.lower()}_captured_commands_count = "
        f"sizeof(k_{vendor.lower()}_captured_commands) / sizeof(k_{vendor.lower()}_captured_commands[0]);"
    )
    lines.append("")

    content = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return content


def synthesize_channel_rule(
    ch1_hex: Optional[str], ch2_hex: Optional[str], ch3_hex: Optional[str]
) -> Optional[Dict[str, Any]]:
    """
    Given captured frames for Channel 1, Channel 2, and optionally Channel 3,
    automatically discovers:
      - which byte index encodes the channel number (1-based `ch` or 0-based `ch - 1`),
      - which checksum formula updates the trailing byte,
      - and synthesizes the exact byte payloads for all 9 Mesh Channels (1..9)!
    """
    if not ch1_hex or not ch2_hex:
        return None
    b1 = bytes.fromhex(ch1_hex.replace(" ", ""))
    b2 = bytes.fromhex(ch2_hex.replace(" ", ""))
    b3 = bytes.fromhex(ch3_hex.replace(" ", "")) if ch3_hex else None
    if len(b1) != len(b2) or len(b1) < 2:
        return None
    if b3 is not None and len(b3) != len(b1):
        b3 = None

    ch_offset: Optional[int] = None
    zero_based = False
    for i in range(len(b1)):
        if b2[i] - b1[i] == 1 and (b3 is None or b3[i] - b2[i] == 1):
            if b1[i] in (0, 1):
                ch_offset = i
                zero_based = b1[i] == 0
                break

    if ch_offset is None:
        return None

    crc_cands = analyze_frame_checksum(b1)
    crc_rule = crc_cands[0].split("==")[0].strip() if crc_cands else "NONE"

    synthesized_channels: Dict[str, str] = {}
    for ch in range(1, 10):
        frame = bytearray(b1)
        frame[ch_offset] = (ch - 1) if zero_based else ch
        # Recompute trailing 1-byte checksum if detected
        if len(frame) >= 3 and crc_rule != "NONE":
            start_idx = 2 if "body[2..-2]" in crc_rule else (1 if "body[1..-2]" in crc_rule else 0)
            sub = bytes(frame[start_idx:-1])
            if crc_rule.startswith("XOR("):
                x = 0
                for v in sub:
                    x ^= v
                frame[-1] = x
            elif crc_rule.startswith("SUM8("):
                frame[-1] = sum(sub) & 0xFF
            elif crc_rule.startswith("TWOS_COMP("):
                frame[-1] = (-sum(sub)) & 0xFF
            elif crc_rule.startswith("CRC8_07("):
                frame[-1] = crc8_standard(sub, 0x07, 0x00)
            elif crc_rule.startswith("CRC8_31("):
                frame[-1] = crc8_standard(sub, 0x31, 0x00)
        synthesized_channels[f"CHANNEL_{ch}"] = " ".join(f"{b:02X}" for b in frame)

    return {
        "channel_byte_offset": ch_offset,
        "encoding": "0-based (ch-1)" if zero_based else "1-based (ch)",
        "checksum_rule": crc_rule,
        "synthesized_channels_1_to_9": synthesized_channels,
    }


def export_complete_oem_profile(
    profile_doc: Dict[str, Any], json_path: Path, header_path: Path
) -> Tuple[Path, Path]:
    """
    Writes both the structured OEM Adapter Profile JSON and a complete C/C++
    profile header (`CartridgeBleConfig_t` + opcode dispatch table) for `PCBA 03`.
    """
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(profile_doc, indent=2, ensure_ascii=False), encoding="utf-8")

    commands_for_header = []
    for item in profile_doc.get("learned_actions", []):
        if item.get("status") == "LEARNED" and item.get("payload_hex"):
            commands_for_header.append({
                "label": item["id"],
                "att_handle": item.get("att_handle", 0),
                "char_uuid": item.get("char_uuid", ""),
                "payload_hex": item["payload_hex"],
                "att_opcode_name": item.get("att_opcode_name", "WRITE_CMD"),
            })

    ch_rule = profile_doc.get("channel_synthesis")
    if ch_rule and "synthesized_channels_1_to_9" in ch_rule:
        ch_handle = profile_doc.get("primary_write_handle", 0)
        ch_uuid = profile_doc.get("primary_write_uuid", "")
        for ch_name, ch_hex in ch_rule["synthesized_channels_1_to_9"].items():
            commands_for_header.append({
                "label": f"SYNTH_{ch_name}",
                "att_handle": ch_handle,
                "char_uuid": ch_uuid,
                "payload_hex": ch_hex,
                "att_opcode_name": "WRITE_CMD",
            })

    generate_cpp_header(
        {
            "device_name": profile_doc.get("device_name", "OEM_INTERCOM"),
            "vendor": profile_doc.get("vendor", "OEM"),
            "commands": commands_for_header,
        },
        header_path,
    )
    return json_path, header_path


# ---------------------------------------------------------------------------
# Live macOS / Bleak Commands (Scan, GATT Dump, Interactive Monitor & Replay)
# ---------------------------------------------------------------------------
def _require_bleak():
    try:
        import bleak  # noqa: F401
        return bleak
    except ImportError:
        print(
            "\n[!] Das Python-Paket 'bleak' (macOS CoreBluetooth BLE Backend) ist noch nicht installiert.\n"
            "    Installiere es mit:\n"
            "      pip install bleak\n",
            file=sys.stderr,
        )
        sys.exit(1)


def classify_intercom_vendor(name: str, service_uuids: List[str]) -> str:
    upper_name = (name or "").upper()
    for vendor, meta in KNOWN_VENDORS.items():
        if any(kw in upper_name for kw in meta["name_keywords"]):
            return vendor
        for u in service_uuids:
            u_short = u.lower()[:8]
            if u_short in meta["service_hints"]:
                return vendor
    return ""


async def cmd_scan(args: argparse.Namespace) -> None:
    bleak = _require_bleak()
    from bleak import BleakScanner

    print(f"[*] Scanne {args.timeout:.1f}s nach BLE-Geräten (Filter: '{args.filter or 'ALLE'}')...")
    devices = await BleakScanner.discover(timeout=args.timeout, return_adv=True)

    rows = []
    for addr, (dev, adv) in devices.items():
        name = dev.name or adv.local_name or "<Unbenannt>"
        uuids = list(adv.service_uuids or [])
        vendor = classify_intercom_vendor(name, uuids)
        if args.filter:
            f_up = args.filter.upper()
            if f_up not in name.upper() and f_up not in vendor and f_up not in addr.upper():
                continue
        mfg_hex = {
            f"0x{comp_id:04X}": " ".join(f"{b:02X}" for b in payload)
            for comp_id, payload in (adv.manufacturer_data or {}).items()
        }
        rows.append((adv.rssi or -999, vendor, name, dev.address, uuids, mfg_hex))

    rows.sort(key=lambda r: (r[1] == "", -r[0]))
    print("-" * 100)
    print(f"{'RSSI':>6} | {'VENDOR':<8} | {'NAME':<28} | {'ADDRESS / UUID (macOS)':<36} | {'SERVICES / MFG DATA'}")
    print("-" * 100)
    for rssi, vendor, name, addr, uuids, mfg_hex in rows:
        tag = f"★ {vendor}" if vendor else ""
        info = f"UUIDs={uuids} Mfg={mfg_hex}" if (uuids or mfg_hex) else "-"
        print(f"{rssi:>4}dBm | {tag:<8} | {name[:28]:<28} | {addr:<36} | {info}")
    print("-" * 100)


async def _resolve_target_device(target: str, timeout: float = 6.0):
    from bleak import BleakScanner

    devices = await BleakScanner.discover(timeout=timeout, return_adv=True)
    target_up = target.upper()
    for addr, (dev, adv) in devices.items():
        name = dev.name or adv.local_name or ""
        if target_up == addr.upper() or target_up in name.upper():
            return dev, (name or addr)
    raise RuntimeError(f"BLE-Gerät '{target}' nicht gefunden. Bitte zuerst `scan` ausführen.")


async def cmd_dump_gatt(args: argparse.Namespace) -> None:
    _require_bleak()
    from bleak import BleakClient

    dev, dev_name = await _resolve_target_device(args.device)
    print(f"[*] Verbinde mit '{dev_name}' ({dev.address})...")

    snapshot: Dict[str, Any] = {
        "device_name": dev_name,
        "address": dev.address,
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "label": args.label or "",
        "services": [],
    }

    async with BleakClient(dev) as client:
        print(f"[+] Verbunden! Lese kompletten GATT-Baum...")
        for svc in client.services:
            svc_entry: Dict[str, Any] = {
                "uuid": svc.uuid,
                "handle": svc.handle,
                "description": svc.description,
                "characteristics": [],
            }
            print(f"\n[Service] {svc.uuid} (Handle 0x{svc.handle:04X}) - {svc.description}")
            for char in svc.characteristics:
                props = list(char.properties)
                read_hex: Optional[str] = None
                read_ascii: Optional[str] = None
                if "read" in props:
                    try:
                        val = bytes(await client.read_gatt_char(char))
                        read_hex = " ".join(f"{b:02X}" for b in val)
                        read_ascii = "".join(chr(b) if 32 <= b < 127 else "." for b in val)
                    except Exception as exc:
                        read_hex = f"<read_err: {exc}>"

                print(
                    f"  ├─ [Char] {char.uuid} (Handle 0x{char.handle:04X}) "
                    f"Props={props} Val={read_hex or '-'}"
                )
                svc_entry["characteristics"].append({
                    "uuid": char.uuid,
                    "handle": char.handle,
                    "description": char.description,
                    "properties": props,
                    "read_hex": read_hex,
                    "read_ascii": read_ascii,
                    "descriptors": [{"uuid": d.uuid, "handle": d.handle} for d in char.descriptors],
                })
            snapshot["services"].append(svc_entry)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[✓] GATT-Snapshot gespeichert unter: {out_path}")


async def _capture_single_state(target: str, label: str, listen_sec: float = 1.5) -> Dict[str, Any]:
    """
    Connects briefly to the headset, reads all readable GATT characteristics AND
    collects any immediate status Notifications emitted upon connection (for `listen_sec`),
    then disconnects cleanly so the Smartphone App can reconnect immediately.
    """
    from bleak import BleakClient

    dev, dev_name = await _resolve_target_device(target)
    snap: Dict[str, Any] = {
        "device_name": dev_name,
        "address": dev.address,
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "label": label,
        "services": [],
    }
    latest_notify_by_handle: Dict[int, bytes] = {}

    async with BleakClient(dev) as client:
        for svc in client.services:
            for char in svc.characteristics:
                if "notify" in char.properties or "indicate" in char.properties:
                    def _make_cb(h: int):
                        def _cb(_s, data: bytearray):
                            latest_notify_by_handle[h] = bytes(data)
                        return _cb
                    try:
                        await client.start_notify(char, _make_cb(char.handle))
                    except Exception:
                        pass

        await asyncio.sleep(listen_sec)

        for svc in client.services:
            svc_entry: Dict[str, Any] = {
                "uuid": svc.uuid,
                "handle": svc.handle,
                "description": svc.description,
                "characteristics": [],
            }
            for char in svc.characteristics:
                props = list(char.properties)
                val_bytes: Optional[bytes] = None
                if "read" in props:
                    try:
                        val_bytes = bytes(await client.read_gatt_char(char))
                    except Exception:
                        val_bytes = None
                if val_bytes is None and char.handle in latest_notify_by_handle:
                    val_bytes = latest_notify_by_handle[char.handle]

                read_hex = " ".join(f"{b:02X}" for b in val_bytes) if val_bytes is not None else None
                read_ascii = (
                    "".join(chr(b) if 32 <= b < 127 else "." for b in val_bytes)
                    if val_bytes is not None
                    else None
                )
                svc_entry["characteristics"].append({
                    "uuid": char.uuid,
                    "handle": char.handle,
                    "description": char.description,
                    "properties": props,
                    "read_hex": read_hex,
                    "read_ascii": read_ascii,
                })
            snap["services"].append(svc_entry)

    return snap


async def cmd_step_diff(args: argparse.Namespace) -> None:
    """
    Guided interactive Step-by-Step Recorder for headsets that only allow one
    active BLE Central connection at a time (Smartphone App OR Mac):
      1. Captures a baseline GATT + Initial-Notify snapshot and disconnects.
      2. User changes ONE setting in Cardo Connect / Sena Motorcycles App.
      3. Reconnects, captures the new state, diffs all characteristics against
         the previous step, and records the exact changed bytes & UUIDs.
    """
    _require_bleak()
    loop = asyncio.get_running_loop()

    print("\n" + "=" * 90)
    print(" GEFÜHRTER SCHRITT-FÜR-SCHRITT APP-SETTING RECORDER (`step-diff`)")
    print(" Ideal, wenn das Headset nur EINE gleichzeitige BLE-Verbindung (App ODER Mac) erlaubt:")
    print("   1. Stelle in der Smartphone-App den Ausgangszustand ein & trenne/schließe kurz die App.")
    print("   2. Drücke hier ENTER -> Mac liest den kompletten GATT-Status aus & gibt das Headset sofort frei.")
    print("   3. Ändere in der App genau EINE Einstellung (z. B. 'Mesh Kanal 1 -> 2'), trenne die App")
    print("      und gib hier den Namen der Änderung ein -> Sofortiger Byte-Diff!")
    print("=" * 90)

    print("\n[Schritt 0] Bitte App kurz trennen/schließen und ENTER drücken für Baseline-Snapshot...")
    await loop.run_in_executor(None, sys.stdin.readline)

    print(f"[*] Lese Baseline-Snapshot von '{args.device}'...")
    prev_snap = await _capture_single_state(args.device, "BASELINE", args.listen_sec)
    print(f"[✓] Baseline erfasst ({prev_snap['device_name']}) & BLE-Verbindung wieder freigegeben!")

    steps_log: List[Dict[str, Any]] = []
    step_num = 1

    while True:
        print(
            f"\n[Schritt {step_num}] Ändere jetzt EINE Einstellung in der App, trenne die App kurz\n"
            f"            und tippe die Bezeichnung ein (oder 'q' zum Beenden): ",
            end="",
            flush=True,
        )
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        label = line.strip()
        if not label or label.lower() in ("q", "quit", "exit"):
            break

        print(f"[*] Lese neuen Zustand nach '{label}'...")
        new_snap = await _capture_single_state(args.device, label, args.listen_sec)
        diffs = diff_gatt_snapshots(prev_snap, new_snap)

        if not diffs:
            print(f"  [!] Keine Änderung in lesbaren/notify GATT-Characteristics erkannt.")
        else:
            for d in diffs:
                print(
                    f"  [★ TREFFER] '{label}' -> UUID {d['characteristic_uuid']} (Handle 0x{(d['handle'] or 0):04X})\n"
                    f"     Vorher : {d['old_hex']}\n"
                    f"     Nachher: {d['new_hex']}\n"
                    f"     Diff   : {d['diff_visual']}"
                )
        steps_log.append({
            "step": step_num,
            "label": label,
            "captured_at": new_snap["captured_at"],
            "diffs": diffs,
        })
        prev_snap = new_snap
        step_num += 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "device_name": prev_snap["device_name"],
                "steps": steps_log,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\n[✓] {len(steps_log)} Änderungs-Schritte gespeichert in: {out_path}")


async def cmd_learn_profile(args: argparse.Namespace) -> None:
    """
    Guided OEM Adapter Profile Wizard (`learn-profile`).
    Walks step-by-step through all 14 standard OpenMotorBridge intercom actions,
    prompts "JETZT drücken!", captures GATT Notifications & Read-Diffs,
    synthesizes the Channel 1..9 formula, and outputs both the JSON OEM profile
    and the C/C++ firmware header for `PCBA 03`.
    """
    _require_bleak()
    loop = asyncio.get_running_loop()

    print("\n" + "=" * 95)
    print(" 🧙‍♂️ OPENMOTORBRIDGE OEM-ADAPTER PROFIL-ASSISTENT (`learn-profile`)")
    print("=" * 95)
    print(" Dieser Assistent führt dich Schritt für Schritt durch alle 14 Intercom-Kommandos,")
    print(" sagt dir jeweils 'JETZT drücken / umstellen!', zeichnet die BLE-Änderung automatisch auf,")
    print(" berechnet Prüfsummen + die Formel für Kanal 1..9 und erzeugt am Ende ein fertiges")
    print(" Geräte-Profil (JSON + C/C++ Firmware-Header) für neue OEM-Adapter!")
    print("-" * 95)
    print(" Steuerung bei jedem Schritt:")
    print("   [ENTER]  -> Aktion wurde ausgeführt, Zustand JETZT aufzeichnen & auswerten")
    print("   s        -> Diesen Befehl überspringen (falls vom Gerät nicht unterstützt)")
    print("   r        -> Vorherigen Schritt wiederholen")
    print("   q        -> Assistent vorzeitig beenden & bisheriges Profil speichern")
    print("=" * 95)

    print("\n[Initialisierung] Bitte Headset einschalten (App kurz trennen, falls exklusiv) & ENTER drücken...")
    await loop.run_in_executor(None, sys.stdin.readline)

    print(f"[*] Verbinde mit '{args.device}' für Baseline-Scan...")
    prev_snap = await _capture_single_state(args.device, "BASELINE", args.listen_sec)
    dev_name = prev_snap["device_name"]
    vendor = classify_intercom_vendor(dev_name, []) or "OEM"
    slug = "".join(c.lower() if c.isalnum() else "_" for c in dev_name).strip("_") or "intercom"
    print(f"[✓] Verbunden & Baseline erfasst: '{dev_name}' (Vendor: {vendor})")

    learned_actions: List[Dict[str, Any]] = []
    capabilities: Dict[str, bool] = {
        "can_power_boot": False,
        "can_power_off": False,
        "can_mesh_toggle": False,
        "can_group_toggle": False,
        "can_volume": False,
        "can_channel_select": False,
        "can_mic_mute": False,
        "can_telemetry": False,
        "can_le_audio_lc3": False,
    }
    primary_write_handle = 0
    primary_write_uuid = ""

    idx = 0
    total = len(OEM_LEARNING_CATALOG)
    while idx < total:
        item = OEM_LEARNING_CATALOG[idx]
        print(f"\n┌─────────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"│ Schritt [{idx + 1:>2}/{total}]: {item['title']:<70} │")
        print(f"│ Opcode        : {item['id']} (0x{item['opcode']:02X}){'':<46} │")
        print(f"└─────────────────────────────────────────────────────────────────────────────────────────┘")
        print(f" 👉 {item['instruction']}")
        print("    [ENTER = Aufzeichnen | 's' = Überspringen | 'r' = Zurück | 'q' = Fertig]: ", end="", flush=True)

        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        choice = line.strip().lower()

        if choice in ("q", "quit", "exit"):
            break
        if choice == "r" and idx > 0:
            idx -= 1
            if learned_actions:
                learned_actions.pop()
            continue
        if choice == "s":
            print(f"    ⏭️  Übersprungen: {item['id']}")
            learned_actions.append({
                "id": item["id"],
                "opcode": item["opcode"],
                "title": item["title"],
                "status": "SKIPPED",
            })
            idx += 1
            continue

        print(f"    ⏳ Zeichne BLE-Zustand für '{item['id']}' auf ({args.listen_sec:.1f}s)...")
        new_snap = await _capture_single_state(args.device, item["id"], args.listen_sec)
        diffs = diff_gatt_snapshots(prev_snap, new_snap)

        if diffs:
            best = diffs[0]
            capabilities[item["capability_flag"]] = True
            primary_write_handle = best.get("handle") or primary_write_handle
            primary_write_uuid = best["characteristic_uuid"] or primary_write_uuid
            print(
                f"    ✅ ERKANNT auf UUID {best['characteristic_uuid']} (Handle 0x{(best.get('handle') or 0):04X}):\n"
                f"       Payload : {best['new_hex']}\n"
                f"       Diff    : {best['diff_visual']}"
            )
            if best["checksum_candidates"]:
                print(f"       CRC     : {', '.join(best['checksum_candidates'])}")
            learned_actions.append({
                "id": item["id"],
                "opcode": item["opcode"],
                "title": item["title"],
                "status": "LEARNED",
                "att_handle": best.get("handle") or 0,
                "char_uuid": best["characteristic_uuid"],
                "payload_hex": best["new_hex"],
                "old_hex": best["old_hex"],
                "changed_bytes": best["changed_bytes"],
                "checksum_candidates": best["checksum_candidates"],
                "att_opcode_name": "WRITE_CMD",
            })
            prev_snap = new_snap
            idx += 1
        else:
            print("    ⚠️  Keine Änderung erkannt! Möchtest du diesen Schritt wiederholen ('r') oder überspringen ('s')? [r/s]: ", end="", flush=True)
            retry_line = await loop.run_in_executor(None, sys.stdin.readline)
            if retry_line and retry_line.strip().lower() == "s":
                learned_actions.append({
                    "id": item["id"],
                    "opcode": item["opcode"],
                    "title": item["title"],
                    "status": "NO_CHANGE_DETECTED",
                })
                idx += 1

    # Check if we can automatically synthesize Channels 1..9 from Ch1, Ch2, Ch3
    by_id = {a["id"]: a.get("payload_hex") for a in learned_actions if a.get("status") == "LEARNED"}
    ch_rule = synthesize_channel_rule(
        by_id.get("OEM_ACTION_CHANNEL_SET_1"),
        by_id.get("OEM_ACTION_CHANNEL_SET_2"),
        by_id.get("OEM_ACTION_CHANNEL_SET_3"),
    )
    if ch_rule:
        print("\n✨ [KANAL-FORMEL AUTOMATISCH SYNTHETISIERT (Kanal 1..9)]:")
        print(f"   Kanal-Byte Offset : Byte[{ch_rule['channel_byte_offset']}] ({ch_rule['encoding']})")
        print(f"   Prüfsummen-Formel : {ch_rule['checksum_rule']}")

    profile_doc = {
        "device_name": dev_name,
        "vendor": vendor,
        "slug": slug,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "primary_write_handle": primary_write_handle,
        "primary_write_uuid": primary_write_uuid,
        "capabilities": capabilities,
        "learned_actions": learned_actions,
        "channel_synthesis": ch_rule,
    }

    json_out = Path(args.output_json or f"captures/profiles/{slug}_oem_profile.json")
    hdr_out = Path(args.output_header or f"firmware/smart_cartridge/src/oem_profile_{slug}.h")
    export_complete_oem_profile(profile_doc, json_out, hdr_out)

    print("\n" + "=" * 95)
    print(f" 🎉 OEM-GERÄTEPROFIL FÜR '{dev_name}' ERFOLGREICH ERSTELLT!")
    print(f"    1. JSON-Adapter-Profil : {json_out}")
    print(f"    2. C/C++ Firmware-Code : {hdr_out}")
    print("=" * 95)


async def cmd_monitor(args: argparse.Namespace) -> None:
    """
    Interactive live GATT Notification monitor & command injector.
    Subscribes to all Notify/Indicate characteristics on the Cardo/Sena headset,
    logs every incoming packet with automatic byte-diffing & checksum detection,
    and lets the user type labels or inject raw hex commands in real time.
    """
    _require_bleak()
    from bleak import BleakClient

    dev, dev_name = await _resolve_target_device(args.device)
    vendor = classify_intercom_vendor(dev_name, []) or "INTERCOM"
    print(f"[*] Verbinde mit '{dev_name}' ({dev.address}) [Vendor: {vendor}]...")

    prev_by_handle: Dict[int, bytes] = {}
    recorded_events: List[Dict[str, Any]] = []
    current_label = "INITIAL_CONNECT"
    t0 = dt.datetime.now(dt.timezone.utc).timestamp()

    async with BleakClient(dev) as client:
        char_map: Dict[str, Any] = {}
        notify_count = 0

        def make_notify_cb(c_obj):
            def _cb(_sender, data: bytearray):
                nonlocal current_label
                raw = bytes(data)
                now = dt.datetime.now(dt.timezone.utc)
                rel_s = round(now.timestamp() - t0, 3)
                prev = prev_by_handle.get(c_obj.handle)
                analysis = analyze_frame_structure(raw, prev)
                diff_str = format_diff_line(raw, prev)
                prev_by_handle[c_obj.handle] = raw

                crc_info = f" | CRC: {', '.join(analysis['checksum_candidates'])}" if analysis["checksum_candidates"] else ""
                print(
                    f"\n🔔 [{rel_s:>7.3f}s] [NOTIFY 0x{c_obj.handle:04X} | {c_obj.uuid[:8]}] "
                    f"Label='{current_label}'\n"
                    f"   Hex : {diff_str}  (ASCII: '{analysis['ascii']}'){crc_info}"
                )
                recorded_events.append({
                    "timestamp_iso": now.isoformat(),
                    "rel_time_s": rel_s,
                    "direction": "RX (Headset->App)",
                    "att_opcode_name": "HANDLE_VALUE_NTF",
                    "att_handle": c_obj.handle,
                    "char_uuid": c_obj.uuid,
                    "payload_hex": analysis["hex"],
                    "label": current_label,
                    "analysis": analysis,
                })
            return _cb

        for svc in client.services:
            for char in svc.characteristics:
                char_map[f"0x{char.handle:04x}"] = char
                char_map[str(char.handle)] = char
                char_map[char.uuid.lower()] = char
                char_map[char.uuid.lower()[:8]] = char
                if "notify" in char.properties or "indicate" in char.properties:
                    try:
                        await client.start_notify(char, make_notify_cb(char))
                        notify_count += 1
                        print(f"  [✓] Subscribed Notify: Handle 0x{char.handle:04X} ({char.uuid})")
                    except Exception as exc:
                        print(f"  [!] Notify fehlgeschlagen auf 0x{char.handle:04X}: {exc}")

        print("\n" + "=" * 88)
        print(f" LIVE BLE INTERCOM MONITOR AKTIV ({notify_count} Notify-Kanäle abonniert)")
        print(" Interaktive Befehle (einfach eintippen + Enter):")
        print("   label <Text>               -> Setzt das aktuelle Action-Label (z. B. 'label Mesh Kanal 2')")
        print("   write <Handle/UUID> <Hex>  -> Sendet GATT Write Request (z. B. 'write 0xffe1 AA 55 05 01 04')")
        print("   wcmd  <Handle/UUID> <Hex>  -> Sendet GATT Write Without Response")
        print("   read  <Handle/UUID>        -> Liest aktuellen Wert einer Characteristic")
        print("   quit                       -> Speichert Session-JSON & beendet Monitor")
        print("=" * 88 + "\n")

        loop = asyncio.get_running_loop()
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            cmd_line = line.strip()
            if not cmd_line:
                continue
            if cmd_line.lower() in ("q", "quit", "exit"):
                break

            parts = cmd_line.split(maxsplit=2)
            verb = parts[0].lower()

            if verb == "label" and len(parts) >= 2:
                current_label = cmd_line[5:].strip()
                print(f"[*] Aktuelles Action-Label gesetzt auf: '{current_label}'")

            elif verb in ("write", "wcmd") and len(parts) == 3:
                target_key = parts[1].lower()
                c_obj = char_map.get(target_key)
                if not c_obj:
                    print(f"[!] Unbekanntes Handle/UUID '{parts[1]}'")
                    continue
                raw = bytes.fromhex(parts[2].replace(" ", ""))
                resp = verb == "write"
                try:
                    await client.write_gatt_char(c_obj, raw, response=resp)
                    now = dt.datetime.now(dt.timezone.utc)
                    rel_s = round(now.timestamp() - t0, 3)
                    analysis = analyze_frame_structure(raw, prev_by_handle.get(c_obj.handle))
                    prev_by_handle[c_obj.handle] = raw
                    print(
                        f"📤 [{rel_s:>7.3f}s] [TX {'WRITE_REQ' if resp else 'WRITE_CMD'} -> 0x{c_obj.handle:04X}] "
                        f"Label='{current_label}' | Hex: {analysis['hex']}"
                    )
                    recorded_events.append({
                        "timestamp_iso": now.isoformat(),
                        "rel_time_s": rel_s,
                        "direction": "TX (App->Headset)",
                        "att_opcode_name": "WRITE_REQ" if resp else "WRITE_CMD",
                        "att_handle": c_obj.handle,
                        "char_uuid": c_obj.uuid,
                        "payload_hex": analysis["hex"],
                        "label": current_label,
                        "analysis": analysis,
                    })
                except Exception as exc:
                    print(f"[!] Write-Fehler: {exc}")

            elif verb == "read" and len(parts) >= 2:
                c_obj = char_map.get(parts[1].lower())
                if not c_obj:
                    print(f"[!] Unbekanntes Handle/UUID '{parts[1]}'")
                    continue
                try:
                    raw = bytes(await client.read_gatt_char(c_obj))
                    print(f"📥 [READ 0x{c_obj.handle:04X}] Hex: {' '.join(f'{b:02X}' for b in raw)}")
                except Exception as exc:
                    print(f"[!] Read-Fehler: {exc}")
            else:
                # Any freeform text sets the label directly for fast workflow!
                current_label = cmd_line
                print(f"[*] Action-Label aktualisiert: '{current_label}'")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    session_doc = {
        "device_name": dev_name,
        "vendor": vendor,
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "commands": recorded_events,
    }
    out_path.write_text(json.dumps(session_doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[✓] {len(recorded_events)} BLE-Events gespeichert in: {out_path}")


# ---------------------------------------------------------------------------
# Offline CLI Commands (`diff`, `parse-capture`, `export-header`)
# ---------------------------------------------------------------------------
def cmd_diff(args: argparse.Namespace) -> None:
    snap_a = json.loads(Path(args.before).read_text(encoding="utf-8"))
    snap_b = json.loads(Path(args.after).read_text(encoding="utf-8"))
    diffs = diff_gatt_snapshots(snap_a, snap_b)

    print("=" * 90)
    print(f" GATT SNAPSHOT DIFF: '{args.before}'  -->  '{args.after}'")
    print("=" * 90)
    if not diffs:
        print("Keine Unterschiede in den lesbaren GATT-Characteristics gefunden.")
        return

    for d in diffs:
        print(f"\n[★ GEÄNDERT] Characteristic {d['characteristic_uuid']} (Handle 0x{(d['handle'] or 0):04X})")
        print(f"  Vorher : {d['old_hex']}")
        print(f"  Nachher: {d['new_hex']}")
        print(f"  Diff   : {d['diff_visual']}")
        for cb in d["changed_bytes"]:
            print(f"    -> Byte[{cb['offset']}]: {cb['old_hex']} ({cb['old_dec']}) => {cb['new_hex']} ({cb['new_dec']})")
        if d["checksum_candidates"]:
            print(f"  Prüfsummen-Treffer: {', '.join(d['checksum_candidates'])}")

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(diffs, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n[✓] Diff-Report gespeichert unter: {out}")


def cmd_parse_capture(args: argparse.Namespace) -> None:
    cap_path = Path(args.capture_file)
    events = parse_capture_auto(cap_path)

    if args.writes_only:
        events = [e for e in events if e.att_opcode in (0x12, 0x52)]

    print("=" * 105)
    print(f" EXTRAHIERTE BLE ATT/GATT PAKETE AUS: {cap_path.name} ({len(events)} Pakete)")
    print("=" * 105)
    print(f"{'#':>5} | {'REL_TIME':>9} | {'DIRECTION':<18} | {'OPCODE':<16} | {'HANDLE':<6} | {'PAYLOAD (HEX & CHECKSUM)'}")
    print("-" * 105)

    serializable_cmds: List[Dict[str, Any]] = []
    for ev in events:
        crc_note = f"  [{', '.join(ev.analysis['checksum_candidates'])}]" if ev.analysis["checksum_candidates"] else ""
        print(
            f"{ev.index:>5} | {ev.rel_time_s:>8.3f}s | {ev.direction:<18} | "
            f"{ev.att_opcode_name:<16} | 0x{ev.att_handle:04X} | {ev.payload_hex}{crc_note}"
        )
        d = asdict(ev)
        d.pop("payload_bytes", None)
        serializable_cmds.append(d)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc = {
            "device_name": args.device_name or cap_path.stem,
            "vendor": args.vendor or "CARDO_OR_SENA",
            "source_capture": str(cap_path),
            "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "commands": serializable_cmds,
        }
        out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n[✓] Analysierte Session als JSON exportiert: {out_path}")


def cmd_export_header(args: argparse.Namespace) -> None:
    session_data = json.loads(Path(args.session_json).read_text(encoding="utf-8"))
    out_path = Path(args.output)
    generate_cpp_header(session_data, out_path)
    print(f"[✓] C/C++ Firmware-Header erfolgreich generiert: {out_path}")


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ble_intercom_workbench.py",
        description="OpenMotorBridge BLE Reverse-Engineering Workbench (Cardo Packtalk Edge & Sena Spider X Slim)",
    )
    sub = p.add_subparsers(dest="subcommand", required=True)

    # 1. scan
    p_scan = sub.add_parser("scan", help="Scanne nach BLE-Geräten (Cardo / Sena / Spider / Packtalk)")
    p_scan.add_argument("--timeout", type=float, default=6.0, help="Scan-Dauer in Sekunden (Default: 6.0)")
    p_scan.add_argument("--filter", type=str, default="", help="Optionaler Namens-/Vendor-Filter (z.B. CARDO oder SENA)")

    # 2. dump-gatt
    p_dump = sub.add_parser("dump-gatt", help="Liest kompletten GATT-Baum & alle lesbaren Werte in eine JSON-Datei")
    p_dump.add_argument("--device", "-d", required=True, help="Gerätename (z.B. 'Packtalk' oder 'Spider') oder BLE-Adresse")
    p_dump.add_argument("--label", "-l", default="", help="Beschreibung des aktuellen Zustands (z.B. 'Mesh_Ch1_VOX_On')")
    p_dump.add_argument("--output", "-o", required=True, help="Ausgabe-JSON-Pfad")

    # 3. diff
    p_diff = sub.add_parser("diff", help="Vergleicht zwei GATT-Snapshots (Vorher vs. Nachher nach App-Änderung)")
    p_diff.add_argument("before", help="Pfad zum GATT-Snapshot VOR der Änderung")
    p_diff.add_argument("after", help="Pfad zum GATT-Snapshot NACH der Änderung")
    p_diff.add_argument("--output", "-o", default="", help="Optionaler Pfad für JSON-Diff-Report")

    # 4. monitor
    p_mon = sub.add_parser("monitor", help="Interaktiver Live-GATT-Sniffer (Notifications) & Hex-Befehls-Injektor")
    p_mon.add_argument("--device", "-d", required=True, help="Gerätename oder BLE-Adresse")
    p_mon.add_argument("--output", "-o", default="captures/live_session.json", help="Pfad für aufgezeichnete Session-JSON")

    # 4b. step-diff
    p_sdiff = sub.add_parser(
        "step-diff",
        help="Freier Schritt-für-Schritt Recorder für beliebige App-Einstellungen",
    )
    p_sdiff.add_argument("--device", "-d", required=True, help="Gerätename (z.B. 'Packtalk' oder 'Spider') oder Adresse")
    p_sdiff.add_argument("--listen-sec", type=float, default=1.5, help="Wartezeit auf Status-Notifications pro Schritt (s)")
    p_sdiff.add_argument("--output", "-o", default="captures/step_diff_session.json", help="Ausgabe-JSON-Pfad")

    # 4c. learn-profile
    p_learn = sub.add_parser(
        "learn-profile",
        help="Interaktiver 14-Schritte Assistent ('Jetzt drücken!'): Lernt alle Befehle & erzeugt ein fertiges OEM-Profil",
    )
    p_learn.add_argument("--device", "-d", required=True, help="Gerätename (z.B. 'Spider' oder 'Packtalk') oder BLE-Adresse")
    p_learn.add_argument("--listen-sec", type=float, default=1.8, help="Aufzeichnungsdauer pro Schritt in Sekunden")
    p_learn.add_argument("--output-json", default="", help="Optionaler Pfad für das JSON-Profil")
    p_learn.add_argument("--output-header", default="", help="Optionaler Pfad für den generierten C/C++ Header")

    # 5. parse-capture
    p_cap = sub.add_parser(
        "parse-capture",
        help="Analysiert Android btsnoop_hci.log, Apple PacketLogger (.pklg) oder Wireshark (.pcap)",
    )
    p_cap.add_argument("capture_file", help="Pfad zur .log / .pklg / .pcap Datei")
    p_cap.add_argument("--writes-only", action="store_true", help="Zeige nur GATT Write-Befehle (App -> Headset)")
    p_cap.add_argument("--vendor", default="CARDO_OR_SENA", help="Vendor-Tag (CARDO oder SENA)")
    p_cap.add_argument("--device-name", default="", help="Gerätename für den Export")
    p_cap.add_argument("--output", "-o", default="", help="Speichere extrahierte Befehle als Session-JSON")

    # 6. export-header
    p_hdr = sub.add_parser(
        "export-header",
        help="Generiert C/C++ Header (generated_intercom_ble_cmds.h) aus einer aufgezeichneten Session-JSON",
    )
    p_hdr.add_argument("session_json", help="Pfad zur Session-JSON")
    p_hdr.add_argument(
        "--output",
        "-o",
        default="firmware/smart_cartridge/src/generated_intercom_ble_cmds.h",
        help="Zielpfad für die generierte .h Datei",
    )

    return p


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.subcommand == "scan":
        asyncio.run(cmd_scan(args))
    elif args.subcommand == "dump-gatt":
        asyncio.run(cmd_dump_gatt(args))
    elif args.subcommand == "monitor":
        asyncio.run(cmd_monitor(args))
    elif args.subcommand == "step-diff":
        asyncio.run(cmd_step_diff(args))
    elif args.subcommand == "learn-profile":
        asyncio.run(cmd_learn_profile(args))
    elif args.subcommand == "diff":
        cmd_diff(args)
    elif args.subcommand == "parse-capture":
        cmd_parse_capture(args)
    elif args.subcommand == "export-header":
        cmd_export_header(args)


if __name__ == "__main__":
    main()
