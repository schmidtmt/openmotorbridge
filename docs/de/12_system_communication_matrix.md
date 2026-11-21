# OpenMotorBridge System Communication Matrix (SSOT)

> **Dokumenten-ID:** `OMB-COMM-SSOT-2026-V10`  
> **Version:** `10.0` | **Datum:** `2026-11-19`  
> **Status:** `Verbindliche Systemvorgabe (Architectural Ground Truth)`  
> **SSOT-Quelldatei:** [`data/system_communication_matrix.json`](../../data/system_communication_matrix.json)  

Lückenlose Definition sämtlicher logischer und physischer Kommunikationsbeziehungen zwischen allen Knoten, Controllern, Peripheriegeräten, OEM-Adaptern, Helmen und dem Smartphone im OpenMotorBridge Gesamtsystem.

---

## 1. System-Knoten, Controller & Endgeräte (Nodes)

| Node-Key | Platinen-ID / Typ | Bezeichnung | Controller / Hardware | Primäre System-Rolle |
| :--- | :--- | :--- | :--- | :--- |
| `NODE_CENTRAL_BOX` | **PCBA 01** | Zentralbox Coordinator (Main Box) | `ESP32-S31-WROOM-1U (U2) + QCC3084 (U9)` | Alleiniger USB-Master (USB2517I Hub U8), zentraler Audio-DSP & einziges CAN-Gateway im Fahrzeug |
| `NODE_FRONT_CHIP1` | **PCBA 05 - Chip 1** | Frontnode Backbone-Client | `ESP32-S31-WROOM-1U (U1)` | Sensor-Aggregation, Fahrtwind-Mikrofon, Daumentaster, Backbone-Uplink zur Zentralbox |
| `NODE_FRONT_CHIP2` | **PCBA 05 - Chip 2** | Frontnode Infotainment-Client | `ESP32-C3FH4 (U10)` | USB-Client für Infotainment (SkylineOS / Nachrüst-AA), WHIM Headset-Emulation, Bord-Lautsprecher UAC |
| `NODE_SKYLINE_OS` | **OEM Infotainment** | Harley-Davidson Boom! Box GTS / SkylineOS | `Harley OEM Touchscreen Headunit` | USB-Master für Infotainment, Display, Bord-Lautsprecher und kabelgebundenes Apple CarPlay |
| `NODE_AFTERMARKET_AA` | **Aftermarket Display** | Nachrüst-Android Auto / CarPlay Display an J4 | `Carpuride / Chigee / COTS Display` | Alternativer USB-Master an Stecker J4 (exklusiv zu SkylineOS via Hardware-Mux) |
| `NODE_POD_L` | **PCBA 03 - Bay 1** | Universal Smart Cartridge Bay 1 (Koffer Links) | `ESP32-C6-MINI-1U (U1) + ES8388 Codec (U2) + CH554E (U7)` | USB-Client an Zentralbox Strang 2, Audio DAC/ADC & Mechatronik-Steuerung für Cartridge/Gateway Bucht 1 |
| `NODE_POD_R` | **PCBA 03 - Bay 2** | Universal Smart Cartridge Bay 2 (Koffer Rechts) | `ESP32-C6-MINI-1U (U1) + ES8388 Codec (U2) + CH554E (U7)` | USB-Client an Zentralbox Strang 3, Audio DAC/ADC & Mechatronik-Steuerung für Cartridge/Gateway Bucht 2 |
| `NODE_OEM_ADAPTER_L` | **Cartridge Slot 1** | OEM Intercom Adapter Bay 1 (Sena / Cardo / Midland) | `Proprietärer OEM Intercom Chip` | Analoges Audio-In/Out + Hardware-PTT + Mechatronik-Taster ACT1..4 via J4 |
| `NODE_OEM_ADAPTER_R` | **Cartridge Slot 2** | OEM Intercom Adapter Bay 2 (Sena / Cardo / Midland) | `Proprietärer OEM Intercom Chip` | Analoges Audio-In/Out + Hardware-PTT + Mechatronik-Taster ACT1..4 via J4 |
| `NODE_OMM_MODULE_L` | **PCBA 09/10 Slot 1** | OpenMotorMesh Modul Bay 1 (2.4G / PMR446 DMR) | `ESP32-C6-MINI-1U + PICO-V3-02` | Nativer digitaler USB Audio-Pfad + digitale PTT/Mesh Steuerung via CH554E Host an J4 |
| `NODE_OMM_MODULE_R` | **PCBA 09/10 Slot 2** | OpenMotorMesh Modul Bay 2 (2.4G / PMR446 DMR) | `ESP32-C6-MINI-1U + PICO-V3-02` | Nativer digitaler USB Audio-Pfad + digitale PTT/Mesh Steuerung via CH554E Host an J4 |
| `NODE_RADAR` | **PCBA 08** | Heck-Radar 2.0 & 5.9 GHz V2X Sub-MCU | `ESP32-C5-WROOM-1U (U1) + MR20 77GHz Radar` | USB-Client an Zentralbox Strang 4, 20 Hz Radar Target Stream, C-ITS V2X, 36x RGB Matrix |
| `NODE_HELMET_DRIVER` | **Helm 1** | Fahrer-Helm (Headset Lautsprecher & Mikrofon) | `Bluetooth 5.4 Dual-A2DP / Auracast / HFP Headset am Qualcomm QCC3084 (PCBA 01)` | Drahtlose Sprachaufnahme & Audiowiedergabe Fahrer via Bluetooth 5.4 direkt an Zentralbox |
| `NODE_HELMET_PILLION` | **Helm 2** | Sozius-Helm (Headset Lautsprecher & Mikrofon) | `Bluetooth 5.4 Dual-A2DP / Auracast / HFP Headset am Qualcomm QCC3084 (PCBA 01)` | Drahtlose Sprachaufnahme & Audiowiedergabe Sozius via Bluetooth 5.4 direkt an Zentralbox (inkl. privater Kabinen-Flüster-Funktion) |
| `NODE_EXT_MESH_GROUP` | **Externe Gruppe** | Externe Motorrad-Gruppe / Mesh- & Funk-Teilnehmer | `Sena Mesh 2.0 / Cardo DMC / OMM 2.4 GHz TDMA / PMR446 DMR` | Externe Kommunikationspartner auf der Straße (bis zu 31 Mesh-Nodes + analoge/digitale Funkgeräte) |
| `NODE_SMARTPHONE` | **Smartphone** | Fahrer-Smartphone (iOS / Android) | `Apple iOS / Google Android` | Musikquelle, Navigations-Engine, Telefonie, Cloud-Sync & OMB App-Interface |
| `NODE_NAVI_DEVICE` | **Externes Navi** | Externes Motorrad-Navi an J10 (Garmin Zūmo / TomTom) | `Garmin Zūmo XT/XT2 / TomTom Rider` | Empfängt reine 12V Stromversorgung von J10 (Audio per Bluetooth direkt an Zentralbox) |
| `NODE_VEHICLE_CAN` | **Fahrzeugnetz** | Motorrad-Fahrzeug CAN-Bus | `Fahrzeug-ECU / BCM (Harley HD-LAN / Standard CAN)` | Einzige physische CAN-Anbindung im Gesamtsystem (ausschließlich an Zentralbox PCBA 01) |
| `NODE_ACTION_CAM` | **EXT_CAM** | Action-Cam / Dashcam | `GoPro / Insta360 / DJI (COTS)` | Drahtlose Helmkamera oder Fairing-Cam fuer Videoaufzeichnung, automatisches Event-Tagging und manuelle Hilight-Bookmarks |

---

## 2. Physische Bus-Topologie & Übertragungsmedien (Buses)

| Bus-Identifier | Beschreibung, physischer Pfad & Isolation |
| :--- | :--- |
| `BUS_USB_BACKBONE_CH1` | Geschirmter 4-Draht USB 2.0 High-Speed Backbone (Zentralbox Host -> Frontnode Chip 1 Client, Molex J6.3/4 -> J1) |
| `BUS_USB_BACKBONE_CH2` | Geschirmter 4-Draht USB 2.0 High-Speed Backbone (Zentralbox Host -> Pod Links Client, Molex J6.7/8) |
| `BUS_USB_BACKBONE_CH3` | Geschirmter 4-Draht USB 2.0 High-Speed Backbone (Zentralbox Host -> Pod Rechts Client, Molex J6.11/12) |
| `BUS_USB_BACKBONE_CH4` | Geschirmter 4-Draht USB 2.0 High-Speed Backbone (Zentralbox Host -> Heck-Radar Client, Molex J6.15/16) |
| `BUS_FRONT_INTER_CHIP` | Lokaler Inter-Chip Bus auf PCBA 05 (Chip 1 <-> Chip 2: I2S Digital Audio + UART Flasher + SPI/GPIO Control) |
| `BUS_FRONT_INFOTAINMENT_MUX` | High-Speed USB 2.0 Mux (TS3USB221 auf PCBA 05: Chip 2 Client -> Pos A SkylineOS / Pos B Nachrüst-AA J4) |
| `BUS_POD_J4_HYBRID_L` | 8-poliger Hybrid-Schnittstellenstecker J4 an Pod Links (TS5A23157: Analog Audio/PTT vs. Digital CH554E USB Host / OMM) |
| `BUS_POD_J4_HYBRID_R` | 8-poliger Hybrid-Schnittstellenstecker J4 an Pod Rechts (TS5A23157: Analog Audio/PTT vs. Digital CH554E USB Host / OMM) |
| `BUS_RF_INTERCOM_L` | Drahtlose Funk-/Mesh-Verbindung Bay 1 (Sena Mesh 2.0 / Cardo DMC / OMM 2.4G Mesh / PMR446 DMR von Bucht 1 zu externen Gruppen-Teilnehmern) |
| `BUS_RF_INTERCOM_R` | Drahtlose Funk-/Mesh-Verbindung Bay 2 (Sena Mesh 2.0 / Cardo DMC / OMM 2.4G Mesh / PMR446 DMR von Bucht 2 zu externen Gruppen-Teilnehmern) |
| `BUS_BLUETOOTH_CENTRAL` | Drahtlose Bluetooth 5.4 Verbindung (Zentralbox QCC3084 <-> Smartphone, Fahrer-Helm & Sozius-Helm: Dual-A2DP, LE Audio Auracast, HFP 1.8 Wideband Voice, BLE Telemetrie) |
| `BUS_WIFI_BT_DONGLE` | Drahtlose 5 GHz Wi-Fi + BT Verbindung (Onboard CP2AA-Dongle an Frontnode <-> Smartphone: Wireless CarPlay / AA) |
| `BUS_VEHICLE_CAN` | Zweiadriger verdrillter Automotive CAN-Bus (Motorrad-Kabelbaum <-> Zentralbox U6 TCAN334G) |
| `BUS_POWER_NAVI_J10` | 2-polige abgesicherte +12V_PROT Stromleitung (Frontnode J10 -> Garmin/TomTom Cradle) |
| `BUS_BLE_ACTIONCAM` | Drahtlose Bluetooth Low Energy 5.0 Funkverbindung (Zentralbox ANT3 / Frontnode <-> Actioncam: GATT Shutter Control, Hilight-Tags, Telemetrie) |
| `BUS_A2DP_POD_MESH` | Drahtlose Classic Bluetooth A2DP Audio-Verbindung (Zentralbox U13 ESP32-PICO-V3-02 ANT4 -> OEM-Adapter Sena/Cardo im Koffer-Pod: Stereo A2DP Musikstream fuer natives Mesh-Music-Sharing) |
| `BUS_FRONT_I2S` | 4-Draht synchroner I2S Digital-Audiobus auf PCBA 05 (U1 ESP32-S31 <-> U10 ESP32-C3FH4): C3_I2S_BCLK, C3_I2S_WS, C3_I2S_SDO, C3_I2S_SDI fuer latenzfreie Audioübertragung zu den Bordlautsprechern und Mikrofon-Rückkanal |

---

## 3. Schiene 1: Frontnode <-> Zentralbox (USB-Backbone Strang 1)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_01_FRONT_TELEM_10HZ** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Telemetry Stream* | `USB_PKT_FRONT_TELEMETRY (0x04)` | 10 Hz | • GNSS_PVT (Lat, Lon, Alt, Speed, Heading, Satellites, Fix)<br>• Knowles_Wind_SPL_dBA<br>• TMP117_Ambient_Temp<br>• OPT3001_Ambient_Lux<br>• BMP390_Baro_Pa<br>• Status_Flags | Konsolidierte Sensordaten für Navigation, eCall, Eiswarnung, Tag/Nacht-Umschaltung und AGC-Helmlautstärke | ✅ Implementiert |
| **COMM_02_KNOWLES_RAW_AUDIO** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*USB Audio Class 2.0 (UAC2 In / Isochronous)* | `UAC2 Audio Endpoint (16 kHz / 48 kHz 24-bit PCM)` | Kontinuierlicher Audio-Stream | • Raw_Acoustic_Mic_PCM | Einspeisung des Fahrtwindmikrofons in den zentralen Audio-DSP für spektrale Windgeräusch- und Staudruckanalyse | ⚠️ Teilweise / Entwurf |
| **COMM_03_HANDLEBAR_GESTURES** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*USB HID Interrupt Endpoint* | `USB_PKT_GESTURE_EVENT (0x03)` | Event-basiert (< 1 ms Latenz) | • Button_ID (PTT, Cam, Media)<br>• Event_Type (Down, Up, Short, Double, Long, Hold)<br>• Duration_ms | Verzögerungsfreie Weitergabe von Daumentaster-Befehlen (Funk-PTT, Kamera-Bookmark, Sprachassistent, Warnung) | ✅ Implementiert |
| **COMM_04_FRONT_HEARTBEAT** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC* | `USB_PKT_NODE_HEARTBEAT (0x02)` | 1 Hz | • Uptime_sec<br>• VBUS_mV<br>• Die_Temp_C<br>• USB_Port_ID<br>• Link_Quality | Link-Überwachung, Port-Topologieverifikation und Spannungsüberwachung am Front-Knoten | ✅ Implementiert |
| **COMM_05_REMOTE_SD_READ_REQ** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*USB Mass Storage (MSC) / Remote File Protocol* | `USB_PKT_REMOTE_FILE_REQ` | On-Demand | • File_Handle_or_Path<br>• Block_Offset<br>• Byte_Count | Frontnode liest HUD-Grafiken, Offline-Karten-Tiles oder Update-Blobs von der SD-Karte der Zentralbox | ✅ Implementiert |
| **COMM_06_REMOTE_SD_READ_RESP** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB Mass Storage (MSC) / Remote File Protocol* | `USB_PKT_REMOTE_FILE_RESP` | On-Demand (Antwort auf REQ) | • File_Handle<br>• Block_Offset<br>• Payload_Bytes<br>• CRC32<br>• Status | Liefert angeforderte SD-Karten-Datenblöcke von der Zentralbox an den Frontnode | ✅ Implementiert |
| **COMM_07_MIRROR_BSD_TRIGGER** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Event* | `USB_PKT_BSD_TRIGGER (0x07)` | Event-basiert / bis zu 20 Hz | • Left_Active<br>• Left_Threat_Level (0..2)<br>• Right_Active<br>• Right_Threat_Level (0..2) | Direkte Ansteuerung der Totwinkel-Warn-LEDs in den Spiegeln (Gate Q1 DMN63D8 -> J2/J3) | ✅ Implementiert |
| **COMM_08_COCKPIT_HUD_UPDATE** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Stream* | `USB_PKT_COCKPIT_HUD_STATE (0x08)` | 10 Hz | • Left_Threat_Level<br>• Right_Threat_Level<br>• Closest_Rear_Dist_dm<br>• GLOSA_V2X_Active<br>• Recommended_Speed_kph<br>• Navi_Maneuver_Icon | Aktualisierung der Dual-OLED-Displays in den Lautsprecherecken des Cockpits (J11/J9) | ✅ Implementiert |
| **COMM_09_POWER_CONFIG_SYNC** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Command* | `USB_CMD_CONFIG (0x11)` | Event-basiert | • Sub_Command (0x01: KL15 Sync, 0x02: Aux Light Q2 Mode, 0x03: Sleep Mode) | Synchronisiert Zündungszustand, schaltet Adventure-Zusatzscheinwerfer (Q2 TPS1H100) und steuert Standby | ✅ Implementiert |
| **COMM_10_DONGLE_HARD_RESET** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Command* | `USB_CMD_POWER_CYCLE (0x10)` | On-Demand bei Fehler | • Target_Port (0: CP2AA Dongle U4, 1: Hub U2)<br>• Off_Duration_ms (2500 ms) | 2.5 s Kaltstart-Reset des CarPlay/AA-Dongles via TPS2051B bei Verbindungsabbruch oder Hänger | ✅ Implementiert |
| **COMM_11_WIFI_UPLOAD_TRIGGER** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC Command* | `USB_CMD_WIFI_UPLOAD_START` | On-Demand (bei Heim-WLAN) | • SSID<br>• Auth_Token<br>• Target_Folder<br>• Upload_Bitmask | Aktiviert High-Speed Wi-Fi 6E (U9 ESP32-E22) zum automatischen Cloud-Sync / WebDAV-Upload bei Zündung AUS | ⚠️ Teilweise / Entwurf |
| **COMM_12_DFU_FIRMWARE_PUSH** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB-CDC DFU Protocol* | `USB_PKT_FW_UPDATE_PUSH (0x50)` | Blockweise während Update | • Target_Chip (1: Front Chip 1, 2: Front Chip 2)<br>• Block_Index<br>• Total_Blocks<br>• Chunk_Payload_96B | Zero-Disassembly Firmware-Update von Chip 1 und Durchreichen an Chip 2 | implemented (Chip 1) / missing (Chip 2 Forwarding) |
| **COMM_13_BIKE_SPEAKER_AUDIO_DOWN** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*USB Audio Class 2.0 (UAC2 Out / Isochronous)* | `USB_PKT_AUDIO_STREAM_DOWN (0x24)` | 48 kHz Stereo 16-bit PCM | • Master_Mix_Audio (Musik, Navi, Radio) | Streamt den fertigen Audio-Master-Mix zur Ausgabe über die Motorrad-Lautsprecher von SkylineOS an den Frontnode | ❌ **FEHLT (Offen)** |
| **COMM_54_CAM_HUD_STATUS_FORWARD** | `CENTRAL_BOX` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1`<br>*OpenMotorBridge USB 2.0 Backbone* | `USB_PKT_CAM_STATUS (0x22)` | 1 Hz / On Change | • Cam_Connected (bool)<br>• Cam_Recording (bool -> Blinkender REC Indikator)<br>• Cam_Battery_Pct (uint8)<br>• Hilight_Tags_Count (uint16) | Visualisiert den Aufnahmestatus der Helmkamera (REC-Icon, rot blinkend bei Aufnahme, Batteriebalken) auf den Cockpit-OLEDs J9/J11 | ✅ Implementiert |
| **COMM_55_CAM_GNSS_1PPS_SYNC** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*OpenMotorBridge USB 2.0 Backbone* | `USB_PKT_GNSS_TIME_MARK (0x23)` | 1 Hz (1-PPS Hardware Trigger) | • UTC_Time_Nanoseconds (u-blox SAM-M10Q 1-PPS)<br>• TOW_TimeOfWeek_ms<br>• PPS_Valid_Flag<br>• SDIO_Blackbox_Sector_Index | Framegenaue (< 15 ns Jitter) Koppelung von Sensordaten (Schraeglage, G-Kraefte, Radar-Targets) mit dem Videomaterial der Actioncam via GPX-Videomarker | ✅ Implementiert |
| **COMM_56_FRONT_MEDIA_AUDIO_UP** | `FRONT_CHIP1` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1`<br>*OpenMotorBridge Low-Latency Audio Protocol* | `USB_PKT_AUDIO_MEDIA_UP (0x26) [UsbAudioMediaUpPkt]` | 100 Hz Frames (10 ms Intervall) | • source_id (0x01 = CP2AA Dongle, 0x02 = USB Stick)<br>• media_l[28] & media_r[28] (Stereo Navigation / Musik von CarPlay/Android Auto)<br>• sample_pairs & frame_seq | Einspeisung von Navigations-Sprachansagen und Medien-Audio von CarPlay / Android Auto am Frontnode in den zentralen DSP der Zentralbox | ⚠️ Teilweise / Entwurf |

---

## 4. Frontnode Inter-Chip Brücke (Chip 1 <-> Chip 2 auf PCBA 05)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_14_INTERCHIP_I2S_AUDIO** | `FRONT_CHIP1` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_FRONT_INTER_CHIP`<br>*I2S Digital Audio Bus (BCLK, WS, DOUT)* | `48 kHz 16-bit Stereo PCM` | Kontinuierlicher Audio-Stream | • Master_Mix_Audio | Verlustfreie Übergabe des Lautsprecher-Audiosignals von Chip 1 an Chip 2 | ✅ Implementiert |
| **COMM_15_INTERCHIP_UART_FLASH** | `FRONT_CHIP1` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_FRONT_INTER_CHIP`<br>*UART ROM Bootloader (esp-serial-flasher) + GPIO EN/BOOT* | `SLIP-Framed Espressif Bootloader Packets` | On-Demand während Update (921.600 Baud) | • Flash_Write_Block<br>• Sync<br>• Mem_Begin<br>• Mem_Data | Chip 1 flasht Chip 2 vollautomatisch über UART, gesteuert von der Zentralbox | ✅ Implementiert |
| **COMM_16_INTERCHIP_MEDIA_CONTROLS** | `FRONT_CHIP1` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_FRONT_INTER_CHIP`<br>*UART / SPI Control Channel* | `MEDIA_CTRL_EVENT` | Event-basiert | • Opcode (Next_Track, Prev_Track, Play_Pause, Vol_Up, Vol_Down, Voice_Trigger) | Leitet Lenkertaster-Eingaben für Musik und Sprachassistent an Chip 2 weiter | ✅ Implementiert |
| **COMM_17_INTERCHIP_MUX_CONTROL** | `FRONT_CHIP1` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_FRONT_INTER_CHIP`<br>*Hardware GPIO + Quittung via UART* | `GPIO Level (0 = SkylineOS, 1 = J4 Nachrüst-AA)` | Bei Modus-Umschaltung | • Mux_Select_State<br>• Dongle_Power_Enable | Schaltet den TS3USB221 USB-Mux zwischen OEM-Display und Nachrüst-AA an J4 um | ✅ Implementiert |
| **COMM_18_INTERCHIP_INFOTAINMENT_STATUS** | `FRONT_CHIP2` $\rightarrow$<br>`FRONT_CHIP1` | `BUS_FRONT_INTER_CHIP`<br>*UART Status Telemetrie* | `INFOTAINMENT_STATUS_REPORT` | 1 Hz / Event-basiert | • CarPlay_Active (bool)<br>• AndroidAuto_Active (bool)<br>• Headset_Emulation_State<br>• Mux_Feedback<br>• Fault_Flags | Rückmeldung des aktuellen Infotainment-Betriebszustands an Chip 1 zur Weiterleitung an die Zentralbox | ✅ Implementiert |
| **COMM_58_FRONT_INTERCHIP_I2S_AUDIO** | `FRONT_CHIP1` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_FRONT_I2S`<br>*Bidirektionaler I2S Stereo PCM Audiobus (Hardware-I2S)* | `48 kHz 16/24-Bit Stereo PCM Stream (C3_I2S_SDO: S31->C3 Lautsprecher; C3_I2S_SDI: C3->S31 Mic/Siri)` | Kontinuierlicher I2S Stream (Double-Buffered DMA, < 2.5 ms Latenz) | • Audio-Playback Stream (Zentralbox/Intercom/Navi -> C3 UAC Out an Boom! Box Bordlautsprecher)<br>• Mikrofon-/Sprach-Rückkanal (Siri / Harley Voice Handshake an Zentralbox-DSP) | Latenzfreie, verlustfreie digitale Audio-Verbindung zwischen Front-Node Haupt-MCU (S31) und Infotainment-Client (C3) für Wiedergabe über die Bordlautsprecher der Harley | ✅ Implementiert |

---

## 5. Schiene 2: Frontnode <-> Infotainment (SkylineOS & Nachrüst-AA)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_19_UAC_SPEAKER_STREAM** | `FRONT_CHIP2` $\rightarrow$<br>`SKYLINE_OS` | `BUS_FRONT_INFOTAINMENT_MUX`<br>*USB Audio Class (UAC Out)* | `Standard USB Audio Streaming Interface` | 48 kHz Stereo PCM | • Speaker_Sound_Output | Wiedergabe von OpenMotorBridge Audio über die werksseitigen Motorrad-Lautsprecher der Harley | ✅ Implementiert |
| **COMM_20_WHIM_HEADSET_BYPASS** | `FRONT_CHIP2` $\rightarrow$<br>`SKYLINE_OS` | `BUS_FRONT_INFOTAINMENT_MUX`<br>*USB UAC + HID Headset Emulation / Apple Accessory Handshake* | `Headset Feature Descriptor & State Machine` | Beim Start & Dauerverbindung | • Headset_Present_Flag<br>• Mic_Active_State | Gaukelt SkylineOS ein verbundenes OEM-Headset vor, um kabelgebundenes Apple CarPlay sofort freizuschalten | ✅ Implementiert |
| **COMM_21_HID_MEDIA_CONTROLS** | `FRONT_CHIP2` $\rightarrow$<br>`SKYLINE_OS` | `BUS_FRONT_INFOTAINMENT_MUX`<br>*USB HID Consumer Control Endpoint* | `HID Consumer Control Report` | Event-basiert | • Play_Pause<br>• Scan_Next<br>• Scan_Previous<br>• Volume_Increment<br>• Volume_Decrement | Steuerung des Musik-Playbacks auf dem Werks-Display über die OpenMotorBridge Daumentaster am Lenker | ✅ Implementiert |
| **COMM_22_CDC_NCM_TRAFFIC_TETHER** | `FRONT_CHIP2` $\rightarrow$<br>`SKYLINE_OS` | `BUS_FRONT_INFOTAINMENT_MUX`<br>*USB CDC-NCM Ethernet Emulation* | `Ethernet Frames / IP Traffic` | Kontinuierlich bei aktiver Navigation | • Live_Traffic_Data_Packets | Versorgt das Harley Werks-Navigationssystem über Smartphone-Tethering automatisch mit Live-Staudaten | ⚠️ Teilweise / Entwurf |
| **COMM_23_AFTERMARKET_AA_DATAPATH** | `FRONT_CHIP2` $\rightarrow$<br>`AFTERMARKET_AA` | `BUS_FRONT_INFOTAINMENT_MUX`<br>*Nativer USB 2.0 High-Speed Pfad via Stecker J4* | `CarPlay / Android Auto Video/Audio Framing` | Vollständige USB-Verbindung | • H.264/H.265_Video_Frames<br>• Touch_Events<br>• UAC_Audio | Direkte Anbindung von Nachrüst-Displays (Carpuride/Chigee) oder COTS-Sticks an Stecker J4 (Pos B des Mux) | ❌ **FEHLT (Offen)** |
| **COMM_24_NAVI_POWER_FEED** | `FRONT_CHIP1` $\rightarrow$<br>`NAVI_DEVICE` | `BUS_POWER_NAVI_J10`<br>*Reine galvanische Stromversorgung (Keine Daten)* | `DC Power (+12V_PROT / GND)` | Dauerhaft bei KL15 | • 12V_DC_Supply_max_2A | Reine abgesicherte Stromversorgung für Garmin Zūmo XT/XT2 oder Smartphone-Cradle. Audio läuft rein via Bluetooth! | ✅ Implementiert |

---

## 6. Pod-Cartridges <-> Zentralbox (USB-Backbone Strang 2 & 3)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_25_POD_L_AUDIO_DOWN** | `CENTRAL_BOX` $\rightarrow$<br>`POD_L` | `BUS_USB_BACKBONE_CH2`<br>*OpenMotorBridge Low-Latency Multi-Channel Audio Protocol* | `USB_PKT_AUDIO_STREAM_DOWN (0x24) [UsbAudioStreamDownPkt]` | 100 Hz Frames (10 ms Intervall) | • driver_voice_bytes & pillion_voice_bytes (Getrennte Fahrer- & Sozius-Sprachkanäle, komprimiert Opus 24k / Vocoder)<br>• music_down_bytes (Stereo-Musikstream Downlink)<br>• compressed_payload[100] (Gemeinsamer komprimierter Audio-Frame)<br>• flags (USB_AUDIO_FLAG_PTT_ACTIVE, USB_AUDIO_FLAG_TARGET_FUNK, USB_AUDIO_FLAG_PILLION_WHISPER, Ducking -18 dB)<br>• voice_gain_db & music_gain_db (DSP Pegelvorgaben) | Deterministische Übertragung getrennter Sprachkanäle (Fahrer/Sozius) und Downlink-Musik an Cartridge Bay 1 (Koffer Links) zur Einspeisung in Mesh/Funk-Gateway | ✅ Implementiert |
| **COMM_26_POD_L_AUDIO_UP** | `POD_L` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH2`<br>*OpenMotorBridge Low-Latency Audio Protocol* | `USB_PKT_AUDIO_STREAM_UP (0x25) [UsbAudioStreamUpPkt]` | 100 Hz Frames (10 ms Intervall) | • voice_funk_count & voice_mesh_count (Anzahl aktiver Funk- und Mesh-Sprachstreams)<br>• music_mesh_pairs (Musik-Sharing Samples/Bytes)<br>• compressed_payload[100] (Multi-Stream Payload: Opus HD 24k Mesh Voice, Codec2/AMBE+2 Funk Voice, Opus Music Sharing)<br>• status_flags (Bit 0: Intercom aktiv, Bit 1: PTT gedrückt, Bit 2: OMM digital)<br>• sample_count & frame_seq | Überträgt empfangene Mesh- und Funk-Sprachstreams sowie empfangenes Mesh-Music-Sharing vom Gateway in Bay 1 (Koffer Links) digital an die Zentralbox zur räumlichen Verteilung und Mischung | ✅ Implementiert |
| **COMM_27_POD_L_ANNOUNCE** | `POD_L` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH2`<br>*USB-CDC Handshake* | `USB_DESC_POD_ANNOUNCE (0x20)` | Beim Booten / Einstecken | • Hardware_Klasse (Sena/Cardo/OMM)<br>• OMM_DETECT_State<br>• Bay_Strap_ID (Bay 1 Links)<br>• Chip_UID<br>• VCC_mV | Deterministische Erkennung der Cartridge und Zuweisung als Koffer-Bucht 1 (Links) ohne USB-ID-Kollision | ✅ Implementiert |
| **COMM_28_POD_L_CONTROL_CMD** | `CENTRAL_BOX` $\rightarrow$<br>`POD_L` | `BUS_USB_BACKBONE_CH2`<br>*USB-CDC Command* | `USB_CMD_POD_CONTROL (0x21)` | Event-basiert | • Opcode (ACT1_POWER, ACT2_MESH, ACT3_VOL_UP, ACT4_VOL_DOWN, PTT_FIRE)<br>• Pulse_Duration_ms | Zentralbox triggert Mechatronik-Taster am Adapter oder schaltet den Funk-PTT-Kanal | ✅ Implementiert |
| **COMM_29_POD_L_CONTROL_ACK** | `POD_L` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH2`<br>*USB-CDC Response* | `USB_PKT_POD_ACK (0x22)` | Antwort auf CMD | • Token<br>• Opcode<br>• Result_Code<br>• Local_Switches_Bitmask<br>• Execution_us | Quittierung der Mechatronik-Ausführung und Meldung des Status lokaler Taster an der Cartridge | ✅ Implementiert |
| **COMM_30_POD_R_AUDIO_DOWN** | `CENTRAL_BOX` $\rightarrow$<br>`POD_R` | `BUS_USB_BACKBONE_CH3`<br>*OpenMotorBridge Low-Latency Multi-Channel Audio Protocol* | `USB_PKT_AUDIO_STREAM_DOWN (0x24) [UsbAudioStreamDownPkt]` | 100 Hz Frames (10 ms Intervall) | • driver_voice_bytes & pillion_voice_bytes (Getrennte Fahrer- & Sozius-Sprachkanäle, komprimiert Opus 24k / Vocoder)<br>• music_down_bytes (Stereo-Musikstream Downlink)<br>• compressed_payload[100] (Gemeinsamer komprimierter Audio-Frame)<br>• flags (USB_AUDIO_FLAG_PTT_ACTIVE, USB_AUDIO_FLAG_TARGET_FUNK, USB_AUDIO_FLAG_PILLION_WHISPER, Ducking -18 dB)<br>• voice_gain_db & music_gain_db (DSP Pegelvorgaben) | Deterministische Übertragung getrennter Sprachkanäle (Fahrer/Sozius) und Downlink-Musik an Cartridge Bay 2 (Koffer Rechts) zur Einspeisung in Mesh/Funk-Gateway | ✅ Implementiert |
| **COMM_31_POD_R_AUDIO_UP** | `POD_R` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH3`<br>*OpenMotorBridge Low-Latency Audio Protocol* | `USB_PKT_AUDIO_STREAM_UP (0x25) [UsbAudioStreamUpPkt]` | 100 Hz Frames (10 ms Intervall) | • voice_funk_count & voice_mesh_count (Anzahl aktiver Funk- und Mesh-Sprachstreams)<br>• music_mesh_pairs (Musik-Sharing Samples/Bytes)<br>• compressed_payload[100] (Multi-Stream Payload: Opus HD 24k Mesh Voice, Codec2/AMBE+2 Funk Voice, Opus Music Sharing)<br>• status_flags (Bit 0: Intercom aktiv, Bit 1: PTT gedrückt, Bit 2: OMM digital)<br>• sample_count & frame_seq | Überträgt empfangene Mesh- und Funk-Sprachstreams sowie empfangenes Mesh-Music-Sharing vom Gateway in Bay 2 (Koffer Rechts) digital an die Zentralbox zur räumlichen Verteilung und Mischung | ✅ Implementiert |
| **COMM_32_POD_R_ANNOUNCE_CONTROL** | `POD_R` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH3`<br>*USB-CDC* | `USB_DESC_POD_ANNOUNCE / CMD / ACK` | Event-basiert | • Identisch zu Bay 1 mit Bay_Strap_ID = Bay 2 Rechts | Deterministische Erkennung und Steuerung der Cartridge in Bay 2 (Koffer Rechts) | ✅ Implementiert |

---

## 7. Pod-Cartridge <-> OEM-Adapter & OMM-Module (Stecker J4)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_33_OEM_ADAPTER_AUDIO_IN** | `POD_L` $\rightarrow$<br>`OEM_ADAPTER_L` | `BUS_POD_J4_HYBRID_L`<br>*Analog Audio Stereo (Pin 4: AUDIO_IN_L, Pin 5: AUDIO_IN_R)* | `Analoge Wechselspannung (Line-Level 1 Vrms)` | Kontinuierlich | • Analog_Master_Mix | Wandlung des USB-Audiosignals im ES8388 DAC und Übergabe an den OEM Intercom-Adapter | ✅ Implementiert |
| **COMM_34_OEM_ADAPTER_MIC_OUT** | `OEM_ADAPTER_L` $\rightarrow$<br>`POD_L` | `BUS_POD_J4_HYBRID_L`<br>*Analog Audio Mono (Pin 7: VOICE_OUT)* | `Analoge Wechselspannung (Mic-Level)` | Kontinuierlich | • Analog_Mic_Signal | Übergabe der Helm-Stimme vom OEM-Adapter an den ES8388 ADC der Cartridge | ✅ Implementiert |
| **COMM_35_OEM_ADAPTER_PTT_HARDWARE** | `POD_L` $\rightarrow$<br>`OEM_ADAPTER_L` | `BUS_POD_J4_HYBRID_L`<br>*Open-Drain Schaltsignal (Pin 8: PTT_BTN)* | `Low-Active Pegel (GND)` | Event-basiert bei PTT-Druck | • PTT_Assert_to_GND | Simuliert den mechanischen PTT-Taster am OEM-Adapter, gesteuert über die Lenkertaster | ✅ Implementiert |
| **COMM_36_OEM_ADAPTER_MECHATRONIC** | `POD_L` $\rightarrow$<br>`OEM_ADAPTER_L` | `BUS_POD_J4_HYBRID_L`<br>*Open-Drain FET Pulsschalter (ACT1..4)* | `Tastimpulse (100..500 ms)` | Event-basiert | • Power_Toggle<br>• Mesh_Toggle<br>• Volume_Up<br>• Volume_Down | Automatisiertes Ein-/Ausschalten und Modus-Umschalten des eingesteckten OEM-Adapters | ✅ Implementiert |
| **COMM_37_OMM_DIGITAL_I2S_PATH** | `POD_L` $\rightarrow$<br>`OMM_MODULE_L` | `BUS_POD_J4_HYBRID_L`<br>*USB 2.0 Full-Speed Host (CH554E U7) via TS5A23157 (U4) mit 3.0 Mbps UART Bridge zum ESP32-C6 (U1)* | `USB Multi-Stream Frames mit komprimierten Opus- & Vocoder-Payloads (5 bidirektionale Streams)` | 10-20 ms Frame-Takt bei aktivem Mesh-/Funk-Betrieb (Netto ~180 kbps für alle 5 Streams) | • Stream 1 Up: Voice-Mesh (Opus 24k Wideband, ~24 kbps)<br>• Stream 2 Up: Voice-Funk (446 MHz PMR/DMR via AMBE+2 / Codec2 / Opus Voice, 1.2-6 kbps)<br>• Stream 3 Up: Audio-Mesh (Opus Stereo Music-Sharing, 48-64 kbps)<br>• Stream 4 Down: Voice-Mic-TX (Getrennt: driver_bytes & pillion_bytes mit Private Cabin Whisper Mute)<br>• Stream 5 Down: Audio-Master-Mix (CarPlay/Navigation/Radar zu OMM/Helm, Opus Stereo, 48-64 kbps)<br>• Embedded Flags: PTT_ACTIVE, TARGET_FUNK, PILLION_WHISPER, Squelch/Carrier & RSSI | Verlustfreie volldigitale 3.0 Mbps USB-Host-Audiobrücke. Überträgt getrennte komprimierte Audioströme (Opus 24k & DMR/Codec2 Vocoder; max. 5 Streams, da 2 zeitgleiche Musikeinspeisungen ins selbe Gehör sinnlos sind) mit 'Private Cabin Whisper' (Sozius spricht per Taster rein privat in den Fahrerhelm mit -12 dB Mesh-Ducking) zur individuellen DSP-Mischung, 3D Spatial Panning und autonomem -18 dB Musik-Ducking in der Zentralbox. | ✅ Implementiert |

---

## 8. Koffer-Gateways (Bay 1 & Bay 2) <-> Externe Gruppen-Teilnehmer (Drahtloses Mesh & Funk)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_59_EXT_MESH_BAY1** | `OMM_MODULE_L` $\rightarrow$<br>`EXT_MESH_GROUP` | `BUS_RF_INTERCOM_L`<br>*OMM 2.4 GHz TDMA Mesh / Sena Mesh 2.0 / Cardo DMC / PMR446 DMR* | `Drahtlose RF Mesh- & Funk-Frames` | TDMA Frame-Takt (10-20 ms) / Funk-Träger | • Mesh_Voice_Packets (bis zu 31 Teilnehmer)<br>• Funk_Voice (PMR446 / DMR)<br>• PTT_Handshake & Squelch<br>• Music_Sharing_Frames | Drahtlose Gruppenkommunikation über das Gateway in Koffer-Bucht 1 (Links) zu externen Tourteilnehmern auf der Straße | ✅ Implementiert |
| **COMM_60_EXT_MESH_BAY2** | `OMM_MODULE_R` $\rightarrow$<br>`EXT_MESH_GROUP` | `BUS_RF_INTERCOM_R`<br>*OMM 2.4 GHz TDMA Mesh / Sena Mesh 2.0 / Cardo DMC / PMR446 DMR* | `Drahtlose RF Mesh- & Funk-Frames` | TDMA Frame-Takt (10-20 ms) / Funk-Träger | • Mesh_Voice_Packets (bis zu 31 Teilnehmer)<br>• Funk_Voice (PMR446 / DMR)<br>• PTT_Handshake & Squelch<br>• Music_Sharing_Frames | Drahtlose Gruppenkommunikation über das Gateway in Koffer-Bucht 2 (Rechts) zu externen Tourteilnehmern auf der Straße (z.B. Paralleler Sena/Cardo Bridge-Betrieb) | ✅ Implementiert |

---

## 9. Zentralbox <-> Heck-Radar 2.0 & V2X (USB-Backbone Strang 4)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_41_RADAR_TARGETS_20HZ** | `RADAR` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH4`<br>*USB-CDC Stream* | `USB_PKT_RADAR_TARGETS (0x30)` | 20 Hz | • Target_Count<br>• Array of Targets (Target_ID, Distance_dm, Relative_Speed_cm_s, Azimuth_deg_10, TTC_cs, Threat_Level, URGENT_Flag) | Voroptimierte 77GHz Radar-Objektliste für Blind Spot Detection (BSD), Kollisionswarnung und Notbremsanzeige | ✅ Implementiert |
| **COMM_42_RADAR_V2X_EVENTS** | `RADAR` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_USB_BACKBONE_CH4`<br>*USB-CDC Event Stream* | `USB_PKT_V2X_CITS_EVENT (0x32)` | Asynchron bei V2X-Empfang (5.9 GHz) | • V2X_Message_Type (CAM, DENM, SPATEM)<br>• Event_Code (Notbremsung Voraus, Einsatzfahrzeug, Ampelphase)<br>• Distance_m<br>• Recommended_Speed | C-ITS Fahrzeug-zu-Fahrzeug und Infrastruktur-Gefahrenmeldungen über 5.9 GHz 802.11p OCB | ✅ Implementiert |
| **COMM_43_RADAR_LED_CMD** | `CENTRAL_BOX` $\rightarrow$<br>`RADAR` | `BUS_USB_BACKBONE_CH4`<br>*USB-CDC Command* | `USB_PKT_RADAR_LED_CMD (0x31)` | Event-basiert | • Macro_ID (Warnblinken, Bremslicht-Pulsen, Notfall-Strobe)<br>• Brightness<br>• Left_BSD_Marker<br>• Right_BSD_Marker | Zentralbox steuert die 36x WS2812B RGB Heck-Matrix für adaptive Rückwarnmuster | ✅ Implementiert |
| **COMM_44_RADAR_DFU_PUSH** | `CENTRAL_BOX` $\rightarrow$<br>`RADAR` | `BUS_USB_BACKBONE_CH4`<br>*USB-CDC DFU* | `USB_PKT_FW_UPDATE_PUSH (0x50)` | Blockweise während Update | • Chunk_Payload_96B<br>• Block_Index | Zero-Disassembly Firmware-Update der ESP32-C5 Sub-MCU im Heck-Gehäuse über den USB-Backbone | ✅ Implementiert |

---

## 10. Zentralbox <-> Smartphone & Helm-Headsets (Bluetooth 5.4 Dual-A2DP, LE Audio & HFP)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_38_HELMET_DRIVER_AUDIO** | `CENTRAL_BOX` $\rightarrow$<br>`HELMET_DRIVER` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth 5.4 Dual-A2DP / LE Audio Auracast (aptX Adaptive / AAC / LC3)* | `Stereo Media Audio Stream (< 15 ms Latenz)` | Kontinuierlich | • Master_Audio_Mix (Spatial Panning: Funk 70/30 L/R, Mesh Center, Ducked Music -18 dB, Navi -12 dB, Radar-Alerts -18 dB) | Drahtlose Stereo-Audiowiedergabe für den Fahrer-Helm mit individueller DSP-Mischung über den Qualcomm QCC3084 SoC | ✅ Implementiert |
| **COMM_39_HELMET_DRIVER_MIC** | `HELMET_DRIVER` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth HFP 1.8 (mSBC Wideband Speech) / LE Audio LC3* | `Sprach-Audio Stream (16 kHz / 32 kHz)` | Kontinuierlich bei aktiver Sprachübertragung / VAD | • Fahrer_Helmmikrofon_Signal<br>• VAD_State | Drahtlose Sprachaufnahme vom Fahrer-Helmmikrofon direkt an den Qualcomm QCC3084 / ESP32-S31 DSP zur Fahrtwindkompensation, VOX und Weiterleitung an Mesh/Funk | ✅ Implementiert |
| **COMM_40_HELMET_PILLION_AUDIO** | `CENTRAL_BOX` $\rightarrow$<br>`HELMET_PILLION` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth 5.4 Dual-A2DP / LE Audio Auracast (aptX Adaptive / AAC / LC3)* | `Stereo Media Audio Stream (< 15 ms Latenz)` | Kontinuierlich | • Sozius_Audio_Mix (Fahrer-Stimme, Mesh-Gruppe, Musik ungeduckt/geduckt, exklusiver privater Flüster-Rückkanal) | Drahtlose individuelle Stereo-Audiowiedergabe für den Sozius-Helm über den Qualcomm QCC3084 SoC | ✅ Implementiert |
| **COMM_40B_HELMET_PILLION_MIC** | `HELMET_PILLION` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth HFP 1.8 (mSBC Wideband Speech) / LE Audio LC3* | `Sprach-Audio Stream + Flüstertaster-Event` | Kontinuierlich bei aktiver Sprachübertragung | • Sozius_Helmmikrofon_Signal<br>• Pillion_Whisper_Button_State<br>• VAD_State | Drahtlose Sprachaufnahme vom Sozius-Helmmikrofon an den DSP; bei aktivem 'Private Cabin Whisper' lokales Routing nur an Fahrer-Ohr (-12 dB Mesh-Ducking) mit vollständiger Mesh-Stummschaltung | ✅ Implementiert |
| **COMM_45_SMARTPHONE_A2DP_MUSIC** | `SMARTPHONE` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth A2DP Sink (Qualcomm QCC3084)* | `aptX Adaptive / AAC / SBC Audio Stream` | Kontinuierlicher Audio-Stream | • Stereo_Media_Audio | Drahtloses Musik-Streaming vom Smartphone in die Zentralbox zur zentralen DSP-Mischung | ✅ Implementiert |
| **COMM_46_SMARTPHONE_HFP_TELEPHONY** | `SMARTPHONE` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth HFP 1.8 Wideband Voice (mSBC / CVSD)* | `Bidirektionales Sprach-Audio` | Bei aktivem Anruf | • Caller_Voice_In<br>• Driver_Mic_Voice_Out | Freisprech-Telefonie mit DSP-Windgeräuschfilterung und automatischer Intercom-Stummschaltung | ✅ Implementiert |
| **COMM_47_SMARTPHONE_BLE_GATT** | `SMARTPHONE` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLUETOOTH_CENTRAL`<br>*Bluetooth Low Energy (BLE 5.0 GATT)* | `Custom OpenMotorBridge GATT Service` | Event-basiert / 1 Hz Telemetrie | • App_Config_Parameters<br>• eCall_Trigger_Ack<br>• Live_Status_Notifications | OpenMotorBridge Smartphone-App für System-Setup, Profilwahl und Diagnose | ✅ Implementiert |

---

## 11. Smartphone <-> Frontnode Dongle (Wireless CarPlay / Android Auto)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_48_SMARTPHONE_WIRELESS_CP_AA** | `SMARTPHONE` $\rightarrow$<br>`FRONT_CHIP2` | `BUS_WIFI_BT_DONGLE`<br>*5 GHz Wi-Fi Direct (802.11ac) + Bluetooth 5.0 Handshake* | `Wireless Apple CarPlay & Wireless Android Auto Tunnel` | Dauerhaft während Fahrt | • H.264_Screen_Video<br>• Multi_Touch_Events<br>• UAC_Navigation_Audio | Kabellose Spiegelung von Smartphone-Apps (Google Maps, Waze, Kurviger, Calimoto) auf das Motorrad-Display | implemented (via COTS Dongle) |

---

## 12. Zentralbox <-> Motorrad CAN-Bus (Einziger CAN-Knoten im Bike)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_49_VEHICLE_CAN_TELEMETRY_IN** | `VEHICLE_CAN` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_VEHICLE_CAN`<br>*Automotive CAN 2.0B / CAN-FD (500 kbps, TCAN334G U6)* | `Harley-Davidson HD-LAN / Standard OBD-II Frames` | 10..50 Hz kontinuierlich | • Fahrzeuggeschwindigkeit<br>• Motordrehzahl<br>• Ganganzeige<br>• Blinkerschalter<br>• Bremsschalter<br>• Kupplung<br>• Tankstand | Fahrzeugzustands-Erfassung für automatische Audio-Dämpfung, Bremslicht-Verstärkung und Fahrten-Logging | ✅ Implementiert |
| **COMM_50_VEHICLE_CAN_SAFETY_ISOLATION** | `CENTRAL_BOX` $\rightarrow$<br>`VEHICLE_CAN` | `BUS_VEHICLE_CAN`<br>*Hardware Listen-Only Mode (Pin S auf TCAN334G auf HIGH)* | `Null-Senden (Reiner Empfangsmodus)` | Dauerhaft aktiv | • Keine TX-Daten auf dem Fahrzeugbus! | Garantiert absolute Störungsfreiheit des Motorrad-Bordnetzes. Das OMB-System kann den Fahrzeug-CAN niemals stören oder blockieren. | ✅ Implementiert |

---

## 13. Zentralbox / Frontnode <-> Action-Cam & Dashcam (BLE & Synchronisation)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_51_CAM_BLE_CONTROL** | `CENTRAL_BOX` $\rightarrow$<br>`ACTION_CAM` | `BUS_BLE_ACTIONCAM`<br>*BLE GATT Client (GoPro 0xFEA6 / Insta360 0xBE80 / DJI 0xFFF0)* | `GATT Write (Shutter / Mode / Wake / Sleep)` | Event-basiert (v > 10 km/h, Tankstopp 10min, Lenkertaster) | • Shutter_Command (Start_Record, Stop_Record)<br>• Camera_Mode (Video, Photo, Timelapse)<br>• Power_State (Sleep, Wakeup, Keepalive)<br>• Fuel_Stop_Hold (10-min grace period on KL15 OFF) | Drahtlose Steuerung von Helmkamera oder Lenker-Actioncam: Automatischer Aufnahmestart bei Fahrtbeginn (> 10 km/h), Shutter-Toggle per Lenkertaster und 10-Minuten-Nachlauf bei Tankstopps | ✅ Implementiert |
| **COMM_52_CAM_BLE_HILIGHT_TAG** | `CENTRAL_BOX` $\rightarrow$<br>`ACTION_CAM` | `BUS_BLE_ACTIONCAM`<br>*BLE GATT Write (GATT [0x01, 0x18] HiLight Tag)* | `GATT Write (HiLight Bookmark)` | Event-basiert (Lenkertaster, Radar TTC < 2.5s, ESS < -0.60g) | • Bookmark_Tag_ID (Sequenznummer)<br>• Trigger_Reason (MANUAL_PTT, AUTO_RADAR_TTC, AUTO_ESS_BRAKE, ECALL)<br>• Timestamp_ms (Relative Videozeit) | Setzt Bookmark-Marker direkt in den laufenden Videostream der Actioncam bei Gefahrensituationen (Heckradar-Kollisionsgefahr, Notbremsung) oder manuellem Klick am Lenkertaster | ✅ Implementiert |
| **COMM_53_CAM_BLE_STATUS_FEEDBACK** | `ACTION_CAM` $\rightarrow$<br>`CENTRAL_BOX` | `BUS_BLE_ACTIONCAM`<br>*BLE GATT Notifications* | `GATT Notify (Camera Status)` | 1 Hz / Event-basiert | • Recording_State (True / False)<br>• Battery_Percentage (0-100%)<br>• Remaining_Minutes (Restaufnahmezeit auf SD)<br>• Cam_Brand (GoPro, Insta360, DJI)<br>• Error_State (SD Full, Overheating, None) | Uebermittelt den Aufnahmestatus und Batteriestand der Actioncam an die Zentralbox fuer HUD-Visualisierung und Systemueberwachung | ✅ Implementiert |

---

## 14. Zentralbox (U13 A2DP) <-> OEM-Adapter (Drahtloses Mesh-Music-Sharing)

| ID | Von $\rightarrow$ Nach | Bus & Protokoll | Paket / Typ | Rate | Nutzdaten / Payload | Zweck & Funktion | Firmware-Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **COMM_57_POD_A2DP_MUSIC_SHARE** | `CENTRAL_BOX` $\rightarrow$<br>`OEM_ADAPTER_L` | `BUS_A2DP_POD_MESH`<br>*Classic Bluetooth 5.0 A2DP Source (SBC / AAC)* | `A2DP Stereo Media Audio Stream` | Dauerhafter Audio-Stream bei aktivem Music-Sharing | • Stereo_Media_Audio_Stream (vom Smartphone/DSP)<br>• AVRCP_Playback_State<br>• Track_Metadata | Drahtlose Einspeisung des Stereo-Musikstreams von der Zentralbox (ANT4 Suedseite) in den OEM-Adapter im Koffer-Pod zur Weiterverteilung in das Gruppen-Mesh via herstellereigenes Music-Sharing | ⚠️ Teilweise / Entwurf |

---

## 15. Konsolidierte Firmware-Lücken-Matrix & Entwicklungs-Roadmap

Insgesamt wurden **61 Kommunikationsbeziehungen** erfasst.
Davon sind **7 Kanäle** noch offen oder nur teilweise implementiert:

| Kanal-ID | Betroffene Knoten | Bus | Fehlende Funktionalität / Aufgabenstellung | Dringlichkeit |
| :--- | :--- | :--- | :--- | :---: |
| **COMM_02_KNOWLES_RAW_AUDIO** | `FRONT_CHIP1` $\rightarrow$ `CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1` | Einspeisung des Fahrtwindmikrofons in den zentralen Audio-DSP für spektrale Windgeräusch- und Staudruckanalyse | 🔴 Hoch (Core) |
| **COMM_11_WIFI_UPLOAD_TRIGGER** | `CENTRAL_BOX` $\rightarrow$ `FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1` | Aktiviert High-Speed Wi-Fi 6E (U9 ESP32-E22) zum automatischen Cloud-Sync / WebDAV-Upload bei Zündung AUS | 🟡 Mittel |
| **COMM_13_BIKE_SPEAKER_AUDIO_DOWN** | `CENTRAL_BOX` $\rightarrow$ `FRONT_CHIP1` | `BUS_USB_BACKBONE_CH1` | Streamt den fertigen Audio-Master-Mix zur Ausgabe über die Motorrad-Lautsprecher von SkylineOS an den Frontnode | 🔴 Hoch (Core) |
| **COMM_22_CDC_NCM_TRAFFIC_TETHER** | `FRONT_CHIP2` $\rightarrow$ `SKYLINE_OS` | `BUS_FRONT_INFOTAINMENT_MUX` | Versorgt das Harley Werks-Navigationssystem über Smartphone-Tethering automatisch mit Live-Staudaten | 🟡 Mittel |
| **COMM_23_AFTERMARKET_AA_DATAPATH** | `FRONT_CHIP2` $\rightarrow$ `AFTERMARKET_AA` | `BUS_FRONT_INFOTAINMENT_MUX` | Direkte Anbindung von Nachrüst-Displays (Carpuride/Chigee) oder COTS-Sticks an Stecker J4 (Pos B des Mux) | 🟡 Mittel |
| **COMM_56_FRONT_MEDIA_AUDIO_UP** | `FRONT_CHIP1` $\rightarrow$ `CENTRAL_BOX` | `BUS_USB_BACKBONE_CH1` | Einspeisung von Navigations-Sprachansagen und Medien-Audio von CarPlay / Android Auto am Frontnode in den zentralen DSP der Zentralbox | 🔴 Hoch (Core) |
| **COMM_57_POD_A2DP_MUSIC_SHARE** | `CENTRAL_BOX` $\rightarrow$ `OEM_ADAPTER_L` | `BUS_A2DP_POD_MESH` | Drahtlose Einspeisung des Stereo-Musikstreams von der Zentralbox (ANT4 Suedseite) in den OEM-Adapter im Koffer-Pod zur Weiterverteilung in das Gruppen-Mesh via herstellereigenes Music-Sharing | 🟡 Mittel |

---
*Automatisch generiert durch `tools/generate_comm_docs.py` aus `data/system_communication_matrix.json`.*
