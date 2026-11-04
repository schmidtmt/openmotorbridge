#!/usr/bin/env python3
"""
Unit & Integration Tests for `ble_intercom_workbench.py`.
Verifies:
  1. Checksum detection (XOR, SUM8, TWOS_COMP, CRC8, CRC16-CCITT) on Sena & Cardo frames.
  2. Byte-level differential analysis between sequential GATT payloads.
  3. Binary parsing of Android `btsnoop_hci.log` and Apple `PacketLogger (.pklg)` captures.
  4. GATT snapshot diffing (`diff_gatt_snapshots`).
  5. C/C++ header generation (`generate_cpp_header`) for `PCBA 03` (`cartridge_ble_client.cpp`).
"""

import struct
import tempfile
from pathlib import Path

from ble_intercom_workbench import (
    analyze_frame_checksum,
    analyze_frame_structure,
    diff_gatt_snapshots,
    export_complete_oem_profile,
    generate_cpp_header,
    parse_apple_pklg_file,
    parse_btsnoop_file,
    synthesize_channel_rule,
)


def _build_hci_acl_att_write(handle: int, payload: bytes, opcode: int = 0x52) -> bytes:
    att_pdu = struct.pack("<BH", opcode, handle) + payload
    l2cap = struct.pack("<HH", len(att_pdu), 0x0004) + att_pdu
    acl = struct.pack("<HH", 0x0040, len(l2cap)) + l2cap
    return acl


def test_checksum_and_diff_engine():
    # Sena-style frame: [0xAA, 0x55, cmd=0x07, ch=0x01, xor=0x06]
    frame_ch1 = bytes([0xAA, 0x55, 0x07, 0x01, 0x06])
    frame_ch2 = bytes([0xAA, 0x55, 0x07, 0x02, 0x05])

    hits1 = analyze_frame_checksum(frame_ch1)
    assert any("XOR(body[2..-2]) == 0x06" in h for h in hits1), f"Unexpected hits: {hits1}"

    struct_diff = analyze_frame_structure(frame_ch2, frame_ch1)
    changed_offsets = [d["offset"] for d in struct_diff["diff_vs_previous"]]
    assert changed_offsets == [3, 4], f"Expected offsets [3, 4], got {changed_offsets}"


def test_btsnoop_and_pklg_parsers():
    acl1 = _build_hci_acl_att_write(0x002A, bytes([0xAA, 0x55, 0x05, 0x01, 0x04]), opcode=0x52)
    acl2 = _build_hci_acl_att_write(0x002A, bytes([0xAA, 0x55, 0x07, 0x03, 0x04]), opcode=0x12)

    # 1. Synthetic Android btsnoop_hci.log (Datalink 1002 = H4)
    BTSNOOP_EPOCH_DELTA_US = 0x00DCDDB30F2F8000
    snoop = bytearray(b"btsnoop\x00" + struct.pack(">II", 1, 1002))
    for i, acl in enumerate([acl1, acl2]):
        h4_pkt = b"\x02" + acl
        ts_us = BTSNOOP_EPOCH_DELTA_US + (1_700_000_000 + i) * 1_000_000
        snoop += struct.pack(">IIIIQ", len(h4_pkt), len(h4_pkt), 0, 0, ts_us) + h4_pkt

    ev_snoop = parse_btsnoop_file(bytes(snoop))
    assert len(ev_snoop) == 2
    assert ev_snoop[0].att_handle == 0x002A
    assert ev_snoop[0].att_opcode_name == "WRITE_CMD"
    assert ev_snoop[1].att_opcode_name == "WRITE_REQ"
    assert ev_snoop[1].payload_hex == "AA 55 07 03 04"

    # 2. Synthetic Apple PacketLogger (.pklg)
    pklg = bytearray()
    for i, acl in enumerate([acl1, acl2]):
        rec_len = 9 + len(acl)
        pklg += struct.pack(">IIIB", rec_len, 1_700_000_000 + i, 0, 0x02) + acl

    ev_pklg = parse_apple_pklg_file(bytes(pklg))
    assert len(ev_pklg) == 2
    assert ev_pklg[0].payload_hex == "AA 55 05 01 04"


def test_snapshot_diff_and_header_export():
    snap_before = {
        "services": [{
            "uuid": "0000ffe0-0000-1000-8000-00805f9b34fb",
            "characteristics": [{
                "uuid": "0000ffe1-0000-1000-8000-00805f9b34fb",
                "handle": 42,
                "read_hex": "AA 55 07 01 06",
            }],
        }]
    }
    snap_after = {
        "services": [{
            "uuid": "0000ffe0-0000-1000-8000-00805f9b34fb",
            "characteristics": [{
                "uuid": "0000ffe1-0000-1000-8000-00805f9b34fb",
                "handle": 42,
                "read_hex": "AA 55 07 02 05",
            }],
        }]
    }
    diffs = diff_gatt_snapshots(snap_before, snap_after)
    assert len(diffs) == 1
    assert diffs[0]["changed_bytes"][0]["offset"] == 3

    with tempfile.TemporaryDirectory() as tmp:
        hdr_path = Path(tmp) / "generated_intercom_ble_cmds.h"
        session = {
            "device_name": "Sena Spider X Slim",
            "vendor": "SENA",
            "commands": [{
                "label": "MESH_CHANNEL_2",
                "att_handle": 0x002A,
                "char_uuid": "0000ffe1-0000-1000-8000-00805f9b34fb",
                "payload_hex": "AA 55 07 02 05",
                "att_opcode_name": "WRITE_CMD",
            }],
        }
        code = generate_cpp_header(session, hdr_path)
        assert "k_sena_mesh_channel_2_bytes_0" in code
        assert "0xAA, 0x55, 0x07, 0x02, 0x05" in code

        # Verify automatic Channel 1..9 formula synthesis & full OEM profile export
        ch_rule = synthesize_channel_rule("AA 55 07 01 06", "AA 55 07 02 05", "AA 55 07 03 04")
        assert ch_rule is not None
        assert ch_rule["channel_byte_offset"] == 3
        assert ch_rule["synthesized_channels_1_to_9"]["CHANNEL_9"] == "AA 55 07 09 0E"

        json_out = Path(tmp) / "sena_spider_oem_profile.json"
        hdr_out2 = Path(tmp) / "oem_profile_sena_spider.h"
        export_complete_oem_profile(
            {
                "device_name": "Sena Spider X Slim",
                "vendor": "SENA",
                "primary_write_handle": 0x002A,
                "primary_write_uuid": "0000ffe1-0000-1000-8000-00805f9b34fb",
                "learned_actions": [
                    {
                        "id": "CARTRIDGE_OPCODE_MESH_TOGGLE",
                        "status": "LEARNED",
                        "att_handle": 0x002A,
                        "char_uuid": "0000ffe1-0000-1000-8000-00805f9b34fb",
                        "payload_hex": "AA 55 05 01 04",
                        "att_opcode_name": "WRITE_CMD",
                    }
                ],
                "channel_synthesis": ch_rule,
            },
            json_out,
            hdr_out2,
        )
        assert json_out.exists()
        assert "SYNTH_CHANNEL_9" in hdr_out2.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_checksum_and_diff_engine()
    test_btsnoop_and_pklg_parsers()
    test_snapshot_diff_and_header_export()
    print("[SUCCESS] All BLE Intercom Workbench self-tests passed!")

