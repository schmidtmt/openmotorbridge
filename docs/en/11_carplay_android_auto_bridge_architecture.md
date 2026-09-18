# 11 - Smart-Managed CarPlay & Android Auto Bridge Architecture (PCBA 05)

## 1. System Overview & Problem Statement

Modern motorcycles—especially **Harley-Davidson models equipped with the Boom! Box GTS and the 2024+ Skyline OS**—feature large-format touchscreen displays with smartphone integration capabilities. In practice, however, riders encounter severe proprietary barriers:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROPRIETARY OEM INFOTAINMENT BARRIER                           │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [Rider Smartphone]                                    [Harley Skyline OS / Boom! Box]
  • Android Auto: Completely blocked or defective    ──► USB port blocks connection
  • Apple CarPlay: Requires OEM headset handshake    ──► "No headset connected"
                   (WHIM module costs $450 extra!)        (CarPlay stays greyed out & inactive)
  • External Dongles: Flap loose in fairing cavity,  ──► Crashes in summer heat (>65°C),
                      parasitic drain, no WHIM-byp.      dropped connections, cable clutter
```

### The OpenMotorBridge Solution: Modular Two-Stage Architecture

OpenMotorBridge resolves these issues through a strictly modular **two-stage architecture** that scales seamlessly from a minimalist naked bike to a fully equipped touring machine:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│            OPENMOTORBRIDGE MODULAR TWO-STAGE ARCHITECTURE                              │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [STAGE 1: BASE SYSTEM (PCBA 01 CENTRAL BOX UNDER THE SEAT)]
  • Operates on ANY motorcycle (Naked Bike, Enduro, Supersport, Classic, Cruiser)
  • Single-Point-of-Contact: Smartphone, helmet, and external GPS pair EXCLUSIVELY with OMB!
  • Music streaming, smartphone navigation (Google Maps, Kurviger, Calimoto) & voice calls
  • External GPS (Garmin Zūmo XT/XT2, TomTom): Receives turn-by-turn audio prompts & live traffic
  • Central Audio DSP: Raised-Cosine Ducking (-12 dB Navi, -18 dB Radar), wind filter, sidetone
  • Full Intercom Matrix (Sena/Cardo pannier pods), eCall crash emergency & rear radar

                                │ Optionally expandable via
                                │ ESP-NOW wireless link (< 0.9 ms latency)
                                ▼

  [STAGE 2: UNIVERSAL COCKPIT & FRONT HUB (PCBA 05 IN FAIRING / COCKPIT AREA)]
  • UNIVERSAL FUNCTIONS FOR ANY MOTORCYCLE (Naked, Enduro, Tourer, Cruiser):
    - Hardwired Handlebar PTT (Optocoupler GPIO 0, < 1.8 ms): Only 30–50 cm harness along handlebars!
      Completely eliminates fragile, fatigue-prone signal wiring across the steering head bearing.
    - Knowles I2S MEMS Wind Noise Microphone: Measures dynamic ram-air pressure directly at the windscreen
      (physically impossible under the seat) for automatic helmet volume tracking (AGC).
    - Cockpit USB Charging Hub: 20W USB-PD Fast Charging on handlebars & dedicated accessory port.
    - Action-Cam BLE Shutter Bridge: Controls GoPro / Insta360 in direct line-of-sight (< 0.5 m).
  
  • MODULAR INFOTAINMENT & DISPLAY EXTENSION (For bikes with touchscreen & aftermarket TFTs):
    - For Harley Skyline OS / Boom! Box GTS, Honda Goldwing, or aftermarket displays (Chigee/Carpuride)
    - Converts wired CarPlay into wireless Apple CarPlay & wireless Android Auto
    - USB Media Proxy for native Harley display (track display & controls without forcing CarPlay)
    - USB CDC-NCM Ethernet Tethering: Provides the built-in factory navigation with live traffic data
    - 100% without routing new signal or video cables through the steering head!
```

---

## 2. Architectural Decision: Why No Onboard Linux SOM on PCBA 05? (Evaluation & Discarded Alternatives)

During early design phases, an extensive evaluation examined whether a soldered-down Linux System-on-Module (SOM) should be placed directly onto the PCBA 05 board. For fanless continuous duty inside the sealed cavity of a motorcycle front fairing (temperature rating per ISO 16750-2 of **-40 °C to +85 °C**), standard single-board computers (such as Raspberry Pi 4/5) were ruled out immediately due to excessive power dissipation (> 5 W) and thermal throttling.

### System-on-Module (SOM) Evaluation Matrix – All Integrated Linux Approaches Discarded

| Criterion | Allwinner V3s | Allwinner T113-S3 | NXP i.MX6ULL | Raspberry Pi CM4 | **OpenMotorBridge Hybrid (Option C)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Architecture Status**| *Discarded* | *Discarded* | *Discarded* | *Discarded* | **Selected & Implemented** |
| **CPU / Controller** | 1x Cortex-A7 @ 1.2 GHz | 2x Cortex-A7 @ 1.2 GHz | 1x Cortex-A7 @ 792 MHz | 4x Cortex-A72 @ 1.5 GHz | **ESP32-S3 Dual-Core @ 240 MHz + COTS Dongle** |
| **Operating System** | Linux Kernel / Rootfs | Linux Kernel / Rootfs | Linux Kernel / Rootfs | Linux Kernel / Rootfs | **100% Linux-Free (FreeRTOS / Bare-Metal)** |
| **Cold Boot Time** | 15–20 s | 15–20 s | 18–25 s | > 25 s | **< 300 ms Instant-On (Firmware)** |
| **RAM (Integrated)** | 64 MB DDR2 SIP | 128 MB DDR3 SIP | External (128–512 MB) | External (1–8 GB) | 512 kB SRAM + 8 MB PSRAM (ESP32-S3) |
| **Video Decoding** | 1080p @ 60 H.264 | 1080p @ 60 H.264/H.265 | 720p @ 30 (Software) | 4K @ 60 | In dedicated offboard automotive COTS stick |
| **Video Encoding (AA)**| No Hardware Enc. | **No Hardware Enc.** | No Hardware Enc. | H.264 HW Encoder | In COTS stick (Dedicated ASIC/DSP) |
| **Power Consumption** | ~0.8 W | ~1.1 W (Streaming) | ~1.0 W | > 4.5 W | **~0.4 W PCBA 05 (Dongle 0.0 W when idle/radio)**|
| **Enclosure Temp (65°C)**| 72 °C | 76 °C | 74 °C | > 95 °C (Throttles) | **Cool (Dongle thermally isolated via pigtail)**|
| **Filesystem Risk** | Ext4 Corruption | Ext4 Corruption | Ext4 Corruption | Ext4 Corruption | **Zero Risk (No eMMC, Flash read-only/FAT)** |

### Why an Onboard Linux SOM Was Discarded Technologically & Practically:

1. **The Critical Hardware Limitation (Missing H.264 Hardware Encoder):**
   * Low-cost automotive SoCs like the Allwinner T113-S3 feature a VPU for hardware **decoding** of H.264/H.265 up to 1080p60, but possess **no fast H.264 hardware encoder**.
   * When Android Auto and the motorcycle display (e.g. Harley 12.3" panel at $1920 \times 720$ or 6.5" panel at $800 \times 480$) negotiate differing resolutions or frame rates, video frames must be dynamically scaled and re-encoded.
   * Weak dual-core Cortex-A7 cores collapse under software encoding: latency surges past $> 150\,\text{ms}$, video stutters, and touchscreen responsiveness becomes intolerably sluggish.
2. **Cold Boot & Startup Time (< 300 ms Instant-On Required):**
   * A Linux kernel with U-Boot, device trees, systemd, and network daemons requires **15 to 25 seconds** minimum before rendering the first frame.
   * OpenMotorBridge requires absolute **instant-on readiness**: the moment the rider hits ignition, the ESP32-S3 boots in **under 300 milliseconds**.
3. **Filesystem Resilience on Abrupt Ignition Cut:**
   * Motorcycles are frequently powered down via the kill switch or key switch without warning. An active, writing Linux filesystem (Ext4 journaling on eMMC or SD card) inevitably suffers corruption over time.
   * The ESP32-S3 utilizes LittleFS in NOR flash with wear leveling, rendering it totally immune to sudden power cuts.
4. **Thermal Decoupling Inside the Fairing:**
   * In a sealed fairing above a hot engine block, summer temperatures build up to +75 °C to +85 °C. A soldered Linux SoC on PCBA 05 would push the PCB beyond thermal limits.
5. **Zero Maintenance Across Apple/Google Protocol Shifts:**
   * When Google or Apple alter their handshake or crypto protocols, an onboard Linux SOM would necessitate reflashing the motorcycle's internal electronics.
   * With our modular approach, the rider updates the $40 COTS adapter in 2 minutes via smartphone app, leaving OpenMotorBridge hardware untouched and stable.

### The Final Hardware Design on PCBA 05 (Universal Front Node)
* **Controller:** ESP32-S3-WROOM-1U Dual-Core Xtensa LX7 @ 240 MHz with Vector DSP (wind noise filtering) and external U.FL antenna connector.
* **USB Hub:** Microchip USB2514B Automotive USB 2.0 High-Speed 480 Mbps 4-Port Hub.
* **Port 1 (Handlebar):** High-speed data + 20W Automotive USB-PD Fast Charging (Southchip SC8102, 9V/2.2A & QC 3.0) for phone mounts (QuadLock/SP Connect).
* **Port 2 (Fairing Pigtail):** Switched VBUS via TI TPS2051B load switch. Connects via a $25\dots 30\,\text{cm}$ shielded harness to the CP2AA dongle attached to the fairing bracket (3M Dual-Lock).
* **Port 3 (Glove Box):** Dedicated USB feed to the glove box—remains **100% free for MP3/FLAC USB thumb drives and official OEM infotainment software updates**.
* **Port 4 (Cockpit Accessories):** High-speed data for dashcam storage, Chigee display, or Garmin Zūmo navigation.
* **CAN-Bus Subsystem:** TI TCAN334G with hardware listen-only pin (`S`) and **solid-state auto-sensing $120\,\Omega$ relay (`CPC1017N`)**, which stays open if boot impedance is $< 100\,\Omega$ to prevent bus collapse.
* **12V Cockpit Channels:** Directional blind-spot mirror warning LEDs (`J9`, Radar BSD), 12V Qi wireless phone power (`J10`), and optional high-side smart switch for auxiliary driving lights (`J11`).
* **Diagnostics & Acoustics:** Knowles SPH0645 I2S MEMS wind noise microphone + WS2812B RGB status indicator with light pipe through the enclosure lid.

---

## 3. Architectural Dilemma: Linux Black-Box vs Embedded RTOS vs Modular Dongle

In automotive practice, there is justifiable skepticism against placing an opaque "Linux black-box" inside permanently mounted vehicle nodes:
- **Drawbacks of Embedded Linux:** 15–25 second boot times, filesystem corruption on abrupt power cuts, continuous maintenance overhead for CVE kernel security patches, and incompatibility risks across major smartphone OS releases.
- **Why FPGAs Are Unviable:** Apple CarPlay and Android Auto are not mere hardware video pipelines (like HDMI or LVDS), but full OSI Layer 4–7 networking and cryptographic software stacks (WPA3 Wi-Fi Direct, TLS 1.3, Bonjour/mDNS, hundreds of Google Protobuf RPCs). Synthesizing this in VHDL/Verilog is commercially unviable and ultimately requires soft-core processors running an OS.

### Comparison of the Three Approaches

| Criterion | Option A: Hardwired Linux SOM on PCBA 05 | Option B: Pure MCU / FreeRTOS (ESP32-S3 / Crossover) | Option C: OpenMotorBridge Smart-Managed Dongle (Recommended) |
| :--- | :--- | :--- | :--- |
| **Linux Black-Box on PCB?** | **Yes** (Kernel, Rootfs, Maintenance) | **No** (100% Bare-Metal Firmware) | **No** (OMB remains 100% Linux-Free) |
| **Cold Boot / Startup Time** | 15–20 seconds | **< 300 milliseconds** | **< 300 milliseconds (OMB Instant-On)** |
| **iPhone Wireless CarPlay** | Yes | **Yes** (Slim RTSP/CarPlay Bridge Stack) | **Yes** (Native via USB or Crossover MCU) |
| **Android Auto ➔ CarPlay** | Yes (via NAL Passthrough) | Extremely limited (no H.264 scaling) | **Yes** (Via dedicated offboard COTS stick) |
| **Maintenance on OS Updates**| Reflash motorcycle hardware | Firmware reflash required | **Simple 2-minute app update on COTS stick** |
| **RF Coexistence (2.4G vs 5G)**| Critical near-field coupling | Good | **Optimal (> 30 dB isolation via 30 cm pigtail)**|
| **Glove Box USB Availability**| Free | Free | **100% free for MP3 thumb drives & updates** |
| **Standby Parasitic Current** | Complex sleep power gating | **0.0 µA** (Deep Sleep) | **True 0.0 µA** (TPS2051B disconnects VBUS) |

### The Recommended Hybrid Reference Architecture: Smart-Managed Front Node

#### 1. Baseline Conditions on Harley-Davidson (Skyline OS & Boom! Box GTS)
* **Apple CarPlay is strictly WIRED from the factory:** The rider must plug the phone into the glove box USB harness on every ride.
* **Android Auto is COMPLETELY ABSENT:** Harley does not license native Android Auto.
* **Crucial Dongle Distinction (CP2AA vs Pure AA Dongles):**
  A standard wireless Android Auto adapter (such as *Motorola MA1*) **does not function at all** on a Harley because it relies on a native vehicle-side Android Auto host. On a Harley, the adapter must be an active **protocol transcoder (CP2AA: CarPlay-to-Android-Auto)** (e.g. *Ottocast U2-X Pro* or *Carlinkit 4.0*), which presents itself as an Apple CarPlay device to the bike while serving wireless Android Auto to the phone!

#### 2. Added Value: Fully Automated, Headless Management by OpenMotorBridge

Normally, 2-in-1 adapters are cumbersome because riders must manually toggle modes or wait for interactive UI prompts. OpenMotorBridge eliminates this friction completely:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             OPENMOTORBRIDGE HEADLESS DONGLE MANAGEMENT (PCBA 05)                       │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [1. RIDER IDENTIFICATION ON IGNITION ON (< 200 ms via BLE / PWA Profile)]
  ├──► Case A: Rider phone identified as Android
  │    • OMB powers up the TPS2051B load switch (5.0 V VBUS)
  │    • OMB commands the dongle headlessly ──► Direct boot into CP2AA transcoding mode
  │    • Zero dialog prompts ("iPhone or Android?") on the Harley touchscreen!
  │    • Harley launches wireless Android Auto seamlessly over the CarPlay video stream.
  │
  ├──► Case B: Rider phone identified as iPhone
  │    • Option 1: Dongle is booted by OMB in pure wireless CarPlay pass-through
  │      (converts wired Skyline OS CarPlay into wireless CarPlay!).
  │    • Option 2 (Phone on charge cable): OMB keeps the dongle port DE-ENERGIZED.
  │
  └──► Case C: No paired smartphone / Quick local ride / FM Radio operation
       • OMB keeps the dongle USB port COMPLETELY POWERED OFF (0.0 mA).
       • No heat dissipation in the fairing, zero RF pollution, zero boot overhead!
```

---

## 4. Protocol Bridging: Android Auto to Apple CarPlay Emulation

Because recent Harley-Davidson motorcycles exclusively support **Apple CarPlay**, Android users are left in the cold. OpenMotorBridge implements universal protocol bridging:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROTOCOL BRIDGING SEQUENCE DIAGRAM                              │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [Android Smartphone]         [PCBA 05 & CP2AA Dongle]        [Harley Skyline OS]
           │                                   │                                │
           │ 1. Wireless Android Auto Auth     │                                │
           ├──────────────────────────────────►│                                │
           │    (Wi-Fi 5 GHz TLS Handshake)    │                                │
           │                                   │ 2. Apple MFi USB iAP2 Init     │
           │                                   ├───────────────────────────────►│
           │                                   │    (Simulates Apple iPhone)    │
           │                                   │                                │
           │                                   │ 3. WHIM Headset Presence Auth  │
           │                                   ├───────────────────────────────►│
           │                                   │    "Headset Connected: OK"     │
           │                                   │◄───────────────────────────────┤
           │                                   │    Harley activates CarPlay    │
           │                                   │                                │
           │ 4. Video Stream (H.264 720p @60)  │                                │
           ├──────────────────────────────────►│ 5. NAL Repackaging (Zero-Copy) │
           │                                   ├───────────────────────────────►│
           │                                   │    CarPlay Video Surface Frame │
           │                                   │                                │
           │ 6. Audio Stream (Opus / PCM)      │ 7. I2S Audio Ducking Engine    │
           ├──────────────────────────────────►│    (-18 dB on Radar Warning)   │
           │                                   ├───────────────────────────────►│
           │                                   │    PCM 48 kHz Stereo Output    │
           │                                   │                                │
           │                                   │ 8. Handlebar PTT Key Pressed   │
           │ 9. Google Assistant Invocation    │◄───────────────────────────────┤
           │◄──────────────────────────────────┤    Injected as HID Key Event   │
```

### Video Pipeline & Latency Optimization
* **Zero-Copy H.264 NAL Passthrough:** Android Auto emits video frames as standard H.264 Annex-B NAL units. The dedicated bridge ASIC in the COTS adapter does not transcode the underlying video, but packages the NAL units directly into the RTP/AVP container format mandated by Apple CarPlay.
* **Latency Budget:**
  * Wi-Fi transmission phone ➔ dongle: **12 ms**
  * NAL repackaging & socket buffer: **3 ms**
  * USB High-Speed transfer dongle ➔ Skyline OS: **4 ms**
  * Display composition & rendering on bike: **16 ms**
  * **Total Glass-to-Glass Latency: 35 ms** (Silky smooth at 60 fps, zero perceived touch delay).

### 4.1 Community Discoveries & Future Roadmap: Native Android Auto in Skyline OS
> [!NOTE]
> **Roadmap & Reality Check: What About Dormant Android Auto Code in Skyline OS?**
> * **Community Discoveries:** In the firmware files of Skyline OS (2024+ model years), complete Android Auto libraries (`libaao.so`, `libandroidauto.so`, Protobuf RPCs) were identified. In bench environments with direct eMMC hardware access, Android Auto was successfully booted on test clusters.
> * **Production Barrier:** In real-world motorcycles, Harley's cybersecurity architecture (Secure Boot with dm-verity signature enforcement and UDS Service 0x27 Seed-Key protection on CAN ID 0x7E2) currently prevents 1-click OBD enablement. Neither *Diag4Bike* nor *TechnoResearch Centurion* currently offer native activation.
> * **Periodic Reality Check:** We actively track firmware updates and tuning community discoveries to assess viable enablement paths.
> * **Future-Proof Migration:** Should Harley officially unlock native Android Auto or a clean UDS exploit emerge, the Front Node (PCBA 05) will switch via firmware update to lightweight *Direct Wireless Pass-Through* (< 2% CPU load, < 15 ms latency). Until then, our integrated CP2AA bridge remains the only thermally resilient and road-proven solution on the market.

---

## 5. WHIM Headset Bypass & Helmet Audio Routing

### The Harley WHIM Dilemma
Harley-Davidson disables Apple CarPlay unless a physical 7-pin corded headset or the $450 **Wireless Headset Interface Module (WHIM)** is detected. Standard Bluetooth headsets (Sena, Cardo) can pair to the head unit, but fail to trigger CarPlay or get demoted to poor-quality mono audio (A2DP stream blocked).

### OpenMotorBridge Virtual WHIM Generator
1. **USB iAP2 Feature Descriptor:** The bridge registers on the USB bus as a certified Apple MFi accessory with an active voice endpoint (`VoiceOverAudio` feature bit `0x04` asserted).
2. **100% Wireless HD Audio Helmet Routing:**
   - The rider and pillion helmets pair **strictly via wireless Bluetooth HD Audio** (LE Audio LC3 or Bluetooth Classic HFP 1.8 Wideband Speech) with OpenMotorBridge. There is **zero wired tether** to the helmet!
   - The cartridge pods (Pod 1 / Pod 2) serve exclusively as vehicle-side audio interfaces (e.g. for legacy Boom! Box GTS harnesses), never for the rider's headset.
   - The ESP32-S3 Audio DSP handles wind noise suppression, AGC, and Raised-Cosine Ducking (-18 dB on radar alerts), forwarding the pristine digital voice channel via USB Audio Class (UAC) straight into the head unit.
3. **Seamless Voice Assistants:** When the rider presses the handlebar voice button or speaks *"Hey Siri"* / *"Hey Google"*, the bridge opens the microphone channel directly to the smartphone. The motorcycle accepts the audio stream without WHIM warnings.

### 5.3 Native OEM Display & USB Media Proxy (Operation Without CarPlay / Android Auto)
No rider is forced to run Apple CarPlay or Android Auto. Those who prefer the clean factory media menus designed by Harley-Davidson benefit from the **USB Media Proxy Architecture** of the Front Node:

1. **How It Works:**
   * The Front Node enumerates on the glove box USB port (`J4`) as a certified Apple MFi / USB Audio Class peripheral.
   * The smartphone streams audio (Spotify, Apple Music) via Bluetooth directly to the OpenMotorBridge Central Box.
   * OpenMotorBridge extracts ID3 metadata (title, artist, album, track duration) and forwards it via ESP-NOW to the Front Node, which passes it over USB to Skyline OS.
2. **What the Rider Sees on the Display:**
   * The 12.3" Skyline OS (or 6.5" Boom! Box) screen opens its native media player: full track title, artist name, album art tags, and progress bar rendered in Harley's factory aesthetic.
3. **Hybrid Audio Routing (Two Selectable Profiles):**
   * **Profile 1: "Helmet Priority" (Default with headset):**
     Audio is **not** routed through the motorcycle's audio stage, but travels straight from phone into the Hi-Fi DSP of OpenMotorBridge and via LDAC / aptX-HD into the helmet.
     *Advantages:* Eliminates the secondary Bluetooth hop ($< 20\,\text{ms}$ vs $> 300\,\text{ms}$ latency), avoids WHIM constraints, and maintains full Raised-Cosine Ducking ($-18\,\text{dB}$ on radar alerts, $-12\,\text{dB}$ on intercom).
   * **Profile 2: "Fairing Speakers" (Cruising with external audio):**
     The Front Node injects digital audio via USB (48 kHz / 16-bit stereo) into Skyline OS, broadcasting music through the fairing-mounted Rockford Fosgate speakers.

---

## 6. Handlebar Controls & Source-Aware CAN Handlebar Gating

Through the Universal Front Node (PCBA 05), the motorcycle's handlebar switches interface directly with smartphone navigation and media functions:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CONTROL MATRIX: HANDLEBAR CONTROLS & ACTIONS                    │
└────────────────────────────────────────────────────────────────────────────────────────┘

  Handlebar Control                   Signal Path                  Action on Display
  ─────────────────────────────────────────────────────────────────────────────────────
  Left Joystick Short Press           CAN-Bus / Front Node         Previous Track
  Right Joystick Short Press          CAN-Bus / Front Node         Next Track
  Joystick Center Click / Mute        CAN-Bus / Front Node         Play / Pause Toggle
  Voice Button Short Press            CAN-Bus / Front Node         Siri / Google Assistant
  Voice Button Long Press (> 2.0 s)   Front Node GPIO              OpenMotorBridge PTT
  Radar Alert (Garmin Varia)          Rear Pod CAN Telegram        Audio Ducking -18 dB
  eCall Crash Detected (> 6.5 g)      Main Box LoRa SOS            Full-Screen SOS Emergency Overlay
```

### 6.1 Collision Protection: Preventing Ghost Streaming During Radio or Thumb Drive Playback
Naive CAN sniffing on `0x290` (handlebar joystick) causes severe operational conflict:
*If the rider is listening to FM radio or an MP3 thumb drive and presses "Next Track", an unmanaged bridge would simultaneously wake up Spotify on the phone, blaring unwanted audio into the helmet.*

OpenMotorBridge prevents this through **Source-Aware CAN Handlebar Gating**:

```
                         ┌──────────────────────────────────────────────┐
                         │       HARLEY-DAVIDSON CAN-BUS (0x290)        │
                         │   Handlebar Joystick [NEXT / PREV / CLICK]   │
                         └──────────────────────┬───────────────────────┘
                                                │
                                                ▼
                                 ┌──────────────────────────────┐
                                 │   OPENMOTORBRIDGE CAN-GATE   │
                                 │   (Source verification gate) │
                                 └──────────────┬───────────────┘
                                                │
                  ┌─────────────────────────────┴─────────────────────────────┐
                  │                                                           │
                  ▼                                                           ▼
   [CONDITION 1: Harley Audio Source]                          [CONDITION 2: Front Node USB Hub]
Infotainment reports on CAN (0x388):                          Microchip USB2514B Port 3 Status:
• FM/AM Radio Tuner       ➔ BLOCK                             • MP3 Drive plugged & active
• DAB+ / SiriusXM         ➔ BLOCK                               ➔ BLOCK (Harley is reading drive)
• Local USB Stick (MP3)   ➔ BLOCK                             • No Drive / Charging Phone Only
• Bluetooth Audio         ➔ ALLOW                               ➔ ALLOW
• CarPlay / Android Auto  ➔ ALLOW
• OMB Virtual USB Proxy   ➔ ALLOW
                  │                                                           │
                  └─────────────────────────────┬─────────────────────────────┘
                                                │
                                                ▼
                                 ┌──────────────────────────────┐
                                 │  Is OMB the active source?   │
                                 └──────┬────────────────┬──────┘
                                     NO │                │ YES
                                        ▼                ▼
                                 [DISCARD EVENT]      [DISPATCH AVRCP]
                                 Harley manages       Smartphone skips
                                 own radio/stick      to next track!
```

1. **CAN Source Filtering (`audio_source_active` on `0x388`):** Handlebar rocker events are only dispatched to the smartphone when Bluetooth, CarPlay, Android Auto, or the OMB proxy is selected as the primary source.
2. **USB Hub Status (`USB2514B` Port 3 Sensing):** Senses on a hardware level whether a mass storage device is mounted in the glove box.
3. **AVRCP Playback-State Lock:** Prevents accidental music playback when the smartphone media app is in a `STOPPED` state.
4. **PWA Configuration:** In Tab 5, riders can select between `AUTOMATIC (Source-Gated)` (default), `ALWAYS ACTIVE` (for naked bikes), and `DISABLED`.

---

## 7. Live Traffic & Data Bridge for Factory Navigation

Harley-Davidson's factory navigation system (Skyline OS / Boom! Box GTS) relies on map and traffic telemetry from **HERE Technologies / TomTom**. To render real-time traffic jams, construction zones, and dynamic re-routing, the internal navigation engine requires an internet uplink.

### The Conventional Hurdle
Normally, Harley expects riders to manually enable their smartphone's *Personal Wi-Fi Hotspot* before every journey. Under iOS, inactive personal hotspots fall asleep after minutes—causing the factory navigation to drop traffic telemetry. Furthermore, the phone overheats in the pocket.

### The OpenMotorBridge Solution: Intelligent Cockpit Wi-Fi AP Gateway

OpenMotorBridge solves this via the Front Node's dual-mode SoftAP (PCBA 05, ESP32-S3 on Channel 1) with **differentiated no-gateway DHCP routing (RFC 3442)**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             INTELLIGENT COCKPIT WI-FI AP ROUTING GATEWAY (PCBA 05)                     │
└────────────────────────────────────────────────────────────────────────────────────────┘

  1. DYNAMIC, PRIVACY-COMPLIANT SSID GENERATION:
     • Format: "OMB-[Model]-[3-Digit ID]" (e.g. "OMB-Skyline-742" or "OMB-HD-318")
     • Model Identifier: 100% passively derived from CAN bus fingerprint (zero invasive UDS frames!)
     • 3-Digit ID: Deterministically derived from silicon eFuse MAC (100–999) ➔ No VIN broadcast!
     • Customizable: Freely editable in PWA (Tab 5) and stored persistently in NVS flash.

  2. STATIC IP MAPPING (192.168.4.0/24 & AP Isolation DISABLED):
     • 192.168.4.1:  Front Node (Gateway & PWA Server)
     • 192.168.4.10: Rider Smartphone (DHCP Option 3 OMITTED / 0.0.0.0)
     • 192.168.4.11: Pillion Smartphone (DHCP Option 3 OMITTED / 0.0.0.0)
     • 192.168.4.20: Harley Skyline OS (DHCP Option 3 DYNAMICALLY points to active uplink)

  3. DIFFERENTIATED NO-GATEWAY DHCP (RFC 3442):
     • Smartphone retains full 4G/5G mobile data connectivity (no "No Internet" drops).
     • PWA Dashboard operates at high speed and low latency over Wi-Fi.

  4. DYNAMIC UPLINK ROUTING FOR SKYLINE OS:
     • In Tab 5, rider selects: [X] Rider Phone   [ ] Pillion Phone   [ ] Offline.
     • Skyline OS receives the chosen phone's IP as its default gateway (Option 3).
     • HERE traffic feeds stream transparently through the selected smartphone.

  5. FUNCTIONAL DIVISION: USB vs WI-FI:
     • USB Port (J4 / USB2514B): Pure automotive media & projection bus (CarPlay/AA, MP3 drives).
       Prevents "Unsupported USB Device" warnings in the restrictive Harley kernel.
     • Wi-Fi AP: Dedicated IP & telemetry bus using Harley's native, official Wi-Fi menu.
```

### Turn-by-Turn Voice Prompt Ducking for Factory GPS
* Voice prompts from the factory GPS (*"In 300 meters, turn right"*) travel over the Front Node's digital audio return channel to the OMB Audio DSP.
* The DSP executes automated Raised-Cosine Ducking ($-12\,\text{dB}$) against helmet music, smoothly blends in the navigation prompt, and gently restores music volume.

### 7.1 Architecture Analysis: PWA vs Native Companion App & Tailscale Coexistence

When architecting mobile data bridges for motorcycle cockpits, mobile operating systems (iOS & Android) introduce distinct challenges. The following principles govern OpenMotorBridge:

#### 1. Why the Progressive Web App (PWA) Is Superior
* **Independence & Zero Operating Costs:** Native iOS apps require the paid *Apple Developer Program* ($99/year subscription) and restrictive review processes for every minor firmware update.
* **Store-Free Deployment:** The OpenMotorBridge PWA is served directly from the Front Node's internal NOR flash via HTTP. It operates instantly in any browser (iPhone, Android, tablet) without installation or external approval.

#### 2. The "Single-VPN" Dilemma (Tailscale & Smart-Home Coexistence)
* Modern mobile OSs (iOS `NEPacketTunnelProvider` and Android `VpnService`) enforce a strict system policy: **only one active VPN tunnel at any time**.
* Many riders continuously run **Tailscale** or WireGuard on their smartphones (e.g. for Home Assistant, garage door automation, or security cameras).
* If OpenMotorBridge were to establish an L3 WireGuard tunnel between Front Node and phone, the mobile OS would immediately kill the rider's existing Tailscale link.

#### 3. Future Companion App: Layer-5 SOCKS5/Stream Relay (`bar.f0o.omb`)
If a native OpenMotorBridge companion app is deployed in the future (reserved Android Application ID `bar.f0o.omb` in the Google Play Console), it resolves routing without VPN interference:
* **Layer 5 Instead of Layer 3:** Rather than handling raw IP packets (L3, which requires root privileges or VPN adapters), the Front Node terminates TCP connections (Port 80/443) locally and streams opaque TLS byte streams over unprivileged standard sockets (`connect()`) to the companion app.
* **Zero VPN Slots Consumed:** Because the app opens standard POSIX sockets over the cellular network, Tailscale remains 100% active and undisturbed.
* **Store-Compliant Background Link:** Leverages `UIBackgroundModes = bluetooth-central` (iOS) or a lean Foreground Service with a persistent sticky notification (Android `bar.f0o.omb`) to keep the uplink active as long as bike ignition is ON.
* **Zero Cellular Subscription (Zero-Cost Principle):** In alignment with OpenMotorBridge core principles, the system avoids recurring cellular SIM fees by relying on the decentralized 868 MHz LoRa mesh (PCBA 04 & PCBA 07 Keyfob) for off-grid messaging and anti-theft tracking (documented in `.context/IDEAS_BACKLOG.md`).

---

## 8. Thermal Management, Cranking Protection & Hard Reboot (Automotive Grade)

### 1. Engine Cranking Protection (ISO 7637-2 Pulse 4)
During starter motor engagement, motorcycle battery voltages routinely sag to **5.8 V to 6.5 V**. The onboard buck-boost regulator (TI TPS63070) on PCBA 05 maintains the 5.0 V VBUS supply for the USB2514B hub, ESP32-S3, and attached peripherals at **5.00 V ± 1%**, ensuring navigation projections **never reboot** when starting the engine.

### 2. Fairing Thermal Protection & Physical Isolation (Up to +85 °C Ambient)
Inside a sealed fairing above a hot engine block, temperatures surge during summer stops. OpenMotorBridge protects sensitive electronics through a three-stage thermal architecture:
* **Minimal Self-Heating on PCBA 05:** The ESP32-S3 draws only ~0.4 W at 240 MHz. Even at 65 °C fairing temperatures, silicon junction temperatures stay far below the 105 °C rating (AEC-Q100 Grade 2).
* **Physically Isolated CP2AA Dongle:** The dongle is not soldered onto the PCB, but decoupled via the shielded 25–30 cm pigtail cable and mounted using 3M Dual-Lock in a ventilated fairing pocket.
* **Automated TPS2051B Thermal Gating:** Using the onboard temperature sensor (SHTC3 / LM75), firmware actively tracks thermal headroom. If fairing temperatures exceed 75 °C or if no phone is connected, the ESP32-S3 de-energizes the dongle's VBUS via the TI TPS2051B switch (0.0 W dissipation), preventing thermal breakdown.

### 3. One-Click Hard Reboot via PWA & Handlebar Switch
If a smartphone or CarPlay protocol handshake freezes, riders can force-reboot the dongle via the PWA (Tab 1 Cockpit & Tab 5 Hardware) or by holding the handlebar PTT switch for 3 seconds:
* The ESP32-S3 pulls the enable line of the **TI TPS2051B high-side switch** low for **2,500 ms**.
* Dongle VBUS (Port 2) is completely cut (0.0 V with active discharge).
* Clean re-enumeration of the USB handshake completes in under 4 seconds.

---

## 9. Summary & Comparison

| Feature | Standard Loose Dongle (Carlinkit / Ottocast) | OpenMotorBridge PCBA 05 Bridge |
| :--- | :--- | :--- |
| **Mounting Location** | Loose inside glove box (cable clutter) | **Fully integrated inside front fairing (PCBA 05)** |
| **Harley WHIM Constraint** | CarPlay blocked without expensive OEM module | **Fully emulated (Virtual WHIM & MFi bypass)** |
| **Android Auto** | Not supported on modern Harley models | **Fully supported via Android-Auto-to-CarPlay Bridge** |
| **Helmet Audio** | Requires dongle mic or degrades to mono | **Direct digital connection with Sena/Cardo via I2S** |
| **Radar Ducking** | No connection to rear radar sensors | **Automated Raised-Cosine Ducking (-18 dB)** |
| **Summer Heat (>65°C)** | Crashes after 20–40 minutes | **Thermally isolated (30 cm pigtail) & TPS2051B gating up to 85 °C** |
