-- ==============================================================================
-- OpenMotorMesh (OMM) - Wireshark Protocol Dissector
-- Dual-PHY 2.4 GHz IEEE 802.15.4 / SC-FDMA & 868 MHz Semtech SX1262 LoRa
-- ==============================================================================

local omm_proto = Proto("omm", "OpenMotorMesh Protocol (OMM)")

-- Field Definitions
local f_type       = ProtoField.uint8("omm.type", "Packet Type", base.HEX, {
    [0x01] = "DLE Beacon (Leader Election)",
    [0x02] = "Audio Stream (Opus SILK / Codec2 RTP)",
    [0x03] = "Group Radar Telemetry",
    [0xFF] = "Emergency / Siren Early Warning"
})
local f_version    = ProtoField.uint8("omm.version", "Protocol Version", base.DEC)
local f_seq        = ProtoField.uint16("omm.seq", "Sequence Number", base.DEC)
local f_node_uid   = ProtoField.uint64("omm.node_uid", "Origin Node UID (DS2401)", base.HEX)
local f_cluster_id = ProtoField.uint32("omm.cluster_id", "Cluster Group ID", base.HEX)
local f_dle_score  = ProtoField.uint8("omm.dle_score", "DLE Leader Score (0..100)", base.DEC)
local f_cap_mask   = ProtoField.uint8("omm.capabilities", "Capabilities Bitmask", base.HEX)
local f_tx_power   = ProtoField.int8("omm.tx_power", "TX Power (dBm)", base.DEC)

-- Capability Bits
local f_cap_mesh   = ProtoField.bool("omm.cap.dual_mesh", "Dual-Mesh Bridge Active", 8, nil, 0x01)
local f_cap_lora   = ProtoField.bool("omm.cap.lora_hp", "LoRa High-Power Active", 8, nil, 0x02)
local f_cap_gnss   = ProtoField.bool("omm.cap.gnss_1pps", "GNSS 1-PPS Locked", 8, nil, 0x04)
local f_cap_can    = ProtoField.bool("omm.cap.can_bus", "CAN-Bus Telemetry", 8, nil, 0x08)
local f_cap_mic    = ProtoField.bool("omm.cap.env_mic", "Front Ambient-Mic Active (+5 Pts)", 8, nil, 0x10)
local f_cap_ups    = ProtoField.bool("omm.cap.ups_bat", "USV LiPo Buffer Active", 8, nil, 0x20)

-- Radar Fields
local f_lat        = ProtoField.int32("omm.radar.lat", "Latitude (deg * 1e7)", base.DEC)
local f_lon        = ProtoField.int32("omm.radar.lon", "Longitude (deg * 1e7)", base.DEC)
local f_alt        = ProtoField.int16("omm.radar.alt", "Altitude (m AMSL)", base.DEC)
local f_speed      = ProtoField.uint8("omm.radar.speed", "Speed (km/h)", base.DEC)
local f_heading    = ProtoField.uint8("omm.radar.heading", "Heading (deg / 2)", base.DEC)
local f_lean       = ProtoField.int8("omm.radar.lean", "Lean Angle (deg)", base.DEC)
local f_status     = ProtoField.uint8("omm.radar.status", "Status Flags", base.HEX)

-- Emergency Fields
local f_alert_sub  = ProtoField.uint8("omm.alert.subtype", "Alert Subtype", base.HEX, {
    [0x01] = "Siren Early Warning (ALERT_SIREN_APPROACHING)",
    [0x02] = "Automatic Crash Detection (eCall)"
})
local f_alert_dur  = ProtoField.uint16("omm.alert.duration", "Alert Duration (ms)", base.DEC)
local f_crc8       = ProtoField.uint8("omm.crc8", "CRC-8/AUTOSAR", base.HEX)

omm_proto.fields = {
    f_type, f_version, f_seq, f_node_uid, f_cluster_id, f_dle_score, f_cap_mask, f_tx_power,
    f_cap_mesh, f_cap_lora, f_cap_gnss, f_cap_can, f_cap_mic, f_cap_ups,
    f_lat, f_lon, f_alt, f_speed, f_heading, f_lean, f_status,
    f_alert_sub, f_alert_dur, f_crc8
}

function omm_proto.dissector(buffer, pinfo, tree)
    local length = buffer:len()
    if length < 2 then return end

    pinfo.cols.protocol = "OpenMotorMesh"
    local pkt_type = buffer(0, 1):uint()
    local subtree = tree:add(omm_proto, buffer(), "OpenMotorMesh Frame")

    subtree:add(f_type, buffer(0, 1))

    if pkt_type == 0x01 then -- DLE Beacon
        pinfo.cols.info = "OMM DLE Beacon (Leader Election & Sync)"
        if length >= 19 then
            subtree:add(f_version, buffer(1, 1))
            subtree:add(f_node_uid, buffer(2, 8))
            subtree:add(f_dle_score, buffer(10, 1))
            
            local cap_tree = subtree:add(f_cap_mask, buffer(11, 1))
            cap_tree:add(f_cap_mesh, buffer(11, 1))
            cap_tree:add(f_cap_lora, buffer(11, 1))
            cap_tree:add(f_cap_gnss, buffer(11, 1))
            cap_tree:add(f_cap_can, buffer(11, 1))
            cap_tree:add(f_cap_mic, buffer(11, 1))
            cap_tree:add(f_cap_ups, buffer(11, 1))

            subtree:add(f_tx_power, buffer(12, 1))
            subtree:add(f_cluster_id, buffer(13, 4))
            subtree:add(f_seq, buffer(17, 2))
        end

    elseif pkt_type == 0x03 then -- Group Radar
        pinfo.cols.info = "OMM Group Radar Telemetry (10 Hz)"
        if length >= 16 then
            subtree:add(f_lat, buffer(2, 4))
            subtree:add(f_lon, buffer(6, 4))
            subtree:add(f_alt, buffer(10, 2))
            subtree:add(f_speed, buffer(12, 1))
            subtree:add(f_heading, buffer(13, 1))
            subtree:add(f_lean, buffer(14, 1))
            subtree:add(f_status, buffer(15, 1))
        end

    elseif pkt_type == 0xFF then -- Emergency Alert
        pinfo.cols.info = "🚨 OMM EMERGENCY ALERT: SIREN / CRASH WARNING"
        if length >= 18 then
            subtree:add(f_alert_sub, buffer(1, 1))
            subtree:add(f_node_uid, buffer(2, 8))
            subtree:add(f_lat, buffer(10, 4))
            subtree:add(f_lon, buffer(14, 4))
            subtree:add(f_alert_dur, buffer(18, 2))
        end
    end
end

-- Register dissector for custom EtherType & UDP Ports
local udp_table = DissectorTable.get("udp.port")
udp_table:add(8088, omm_proto)

local wtap_encap_table = DissectorTable.get("wtap_encap")
print("OpenMotorMesh (OMM) Wireshark Dissector loaded successfully.")
