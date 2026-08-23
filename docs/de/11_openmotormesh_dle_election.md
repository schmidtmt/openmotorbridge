# 11 - OpenMotorMesh (OMM) - Protokoll-Stack, DLE & Cross-Domain Audio

OpenMotorMesh (OMM) ist ein hierarchisches, latenzoptimiertes Mesh-Routing-Protokoll, das speziell fuer hochdynamische Fahrzeugverbaende im Ad-hoc-Betrieb (868 MHz LoRa & 2.4 GHz IEEE 802.15.4) entwickelt wurde. Es verbindet proprietaere Audio-Inseln (Sena Mesh, Cardo DMC) mit einem offenen, IP-faehigen Daten- und Voice-Backbone.

## 1. Layer 2: Schlanker MAC-Layer (3GPP LTE-Anlehnung)
Um Kollisionen bei schnellen Gruppenfahrten ohne feste Basisstation zu vermeiden, nutzt OMM einen abgeleiteten Mini-Cellular TDMA/CSMA-Hybrid-Frame (100 ms Superframe-Dauer):
- **Beacon Slot (10 ms):** DLE Leader Sync & Clock Normal
- **Control Slot (10 ms):** Join/Leave & Routing Requests
- **Voice Slots (TDMA, 4x 15 ms = 60 ms):** Stream 1 (Master Voice), Stream 2 (Relay Voice)
- **CSMA Slots (20 ms):** Ad-hoc Daten, GPS Telemetrie, Alerting

### Frame-Header Definition (Layer 2 Frame - 5 Bytes)
- `VER` (2 Bit): Protokollversion (01 = v8.0)
- `PRIO` (2 Bit): 00 Notfall/SOS, 01 Echtzeit-Sprache (RTP), 10 Telemetrie, 11 Hintergrund-Sync
- `FRAME_TYPE` (4 Bit): Beacon (0x1), Route Request (0x2), Route Reply (0x3), Voice Data (0x4), Telemetrie (0x5), ACK (0x6)
- `NETWORK_ID` (16 Bit PAN ID), `SOURCE_NODE_ID` (16 Bit), `DESTINATION_NODE_ID` (16 Bit), `SEQUENCE_NUM` (8 Bit)

## 2. Layer 3: Stateless IPv6 & 6LoWPAN
- **Adressierung:** Link-lokale IPv6-Adresse (fe80::/64) abgeleitet von der 64-Bit Chip-UID (DS2401).
- **6LoWPAN Kompression (RFC 6282):** Reduziert den 40-Byte IPv6-Header auf bis zu 2 bis 4 Bytes (LOWPAN_IPHC).
- **Routing:** Ad-hoc On-Demand Distance Vector (AODV-R) basierend auf LQI, RSSI und DLE-Score.

## 3. Layer 4 & Audio: RTP & Opus Voice Streaming
- **Voice-Codec:** Opus Audio mit SILK-Modus (12 kbps VBR, 20 ms Frame-Groesse).
- **RTP-Kompression:** Reduziert auf 3 Bytes Header (Sequence 16-Bit + Timestamp 8-Bit Delta).
- **Adaptiver Jitter-Buffer:** Dynamische Latenzanpassung im DSP (30 bis 80 ms).

## 4. Dynamic Leader Election (DLE) Algorithmus
Score_DLE = S_HW + S_PWR + S_GNSS + S_LORA + S_UPTIME

| Parameter | Bedingung | Punkte |
| :--- | :--- | :--- |
| **S_HW (Hardware Tier)** | Sena Apex (Mesh 3.0) ODER Cardo Edge (DMC Gen2) gesteckt | +60 Pkt. |
| | Sena Legacy / Cardo DMC Gen1 gesteckt | +30 Pkt. |
| **S_PWR (Stromversorgung)** | Zuendung aktiv (KL15 > 12.5 V) | +20 Pkt. |
| | Pufferbetrieb (USV-Akku > 3.8 V) | +5 Pkt. |
| **S_GNSS (Positionsstabilitaet)** | 3D Fix mit PDOP < 1.5 | +10 Pkt. |
| **S_LORA (Link-Qualitaet)** | Durchschnittlicher Nachbar-RSSI > -85 dBm | +10 Pkt. |
| **S_UPTIME (Hysterese-Schutz)** | Bereits aktiver Leader (verhindert Flattern) | +15 Pkt. |
