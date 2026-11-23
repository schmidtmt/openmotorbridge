# 11 - Smartphone Integration, Charging Architecture & Navigation Ergonomics

This document specifies the authoritative interface between rider smartphone and OpenMotorBridge (OMB), the glovebox fast-charging infrastructure, the navigation architecture with factory headunits, and the ergonomic realities across different vehicle platforms (BMW GS vs. Harley-Davidson Touring).

---

## 1. System Overview: Deliberate Removal of Apple CarPlay & Android Auto

Earlier conceptual stages envisioned mirroring Apple CarPlay and Android Auto to factory motorcycle screens (such as the Harley Boom! Box GTS or Skyline OS) via third-party USB dongles and emulated MFi headsets. Following comprehensive real-world track and touring tests, this approach was **deliberately and completely removed**:

1. **Thermal Shutdown Protection in Enclosed Compartments:**
   * A smartphone charging inductively inside a sealed fairing glovebox while simultaneously running a 5 GHz Wi-Fi Direct H.264/H.265 video-streaming stack reaches temperatures in excess of $65\,^\circ\text{C}$ within 15–20 minutes in summer ambient conditions.
   * This inevitably triggers **thermal shutdown of the smartphone** mid-ride.
2. **Proprietary Instability & Update Breakage:**
   * Video mirroring via dongles and reverse-engineered headset handshakes is notoriously fragile, prone to frame stutter and buffering latency, and frequently invalidated by OEM firmware updates.
3. **Wiring Harness Slimming & EMC Protection:**
   * Eliminating the glovebox USB hub (`PCBA 05B`) completely removes sensitive high-speed USB differential pairs from the cockpit harness. The glovebox is fed by a **pure 2-wire DC line** -- zero EMC noise pickup, zero bus collisions.

**Guiding Principle:** OpenMotorBridge focuses strictly on where it excels: **zero-latency audio authority (3× QCC3086), true HFP 1.8 telephony with full-duplex helmet microphone return, deterministic DSP ducking, and stable 30W automotive fast-charging.**

---

## 2. Real Smartphone Interconnect (Qualcomm QCC3086 `U9`)

All smartphone interaction is handled natively by the dedicated Bluetooth 5.4 audio transceiver **Qualcomm QCC3086 (`U9`)** and the system DSP **ESP32-S31 (`U2`)**:

```
+----------------------------------------------------------------------------------------+
|                      SMARTPHONE ⟷ OPENMOTORBRIDGE INTERFACES                           |
+----------------------------------------------------------------------------------------+
  [Rider Smartphone (in glovebox or handlebar mount)]
        │
        ├─► [Bluetooth A2DP Sink] ──────► Qualcomm QCC3086 (U9) ──► I2S ──► ESP32-S31 DSP
        │   (Hi-Fi Music Spotify/Apple)                             (Raised-Cosine Ducking)
        │
        ◄─► [Bluetooth HFP 1.8] ────────► Qualcomm QCC3086 (U9) ◄─► I2S ◄─► ESP32-S31 DSP
        │   (Full-Duplex Telephony)       (mSBC / LC3 Speech)       ▲   (Helmet Mic Return)
        │                                                           │
        │                                                Rider Helmet (U13 QCC3086)
        │                                                Pillion Helmet (U14 QCC3086)
        │
        ◄─► [Bluetooth AVRCP 1.6] ──────► QCC3086 UART ◄── CAN-Bus ◄── Factory Handlebar Keys
        │   (Play/Pause, Next/Prev, Vol)                            (Harley LHCM / BMW Wheel)
        │
        ◄─► [BLE GATT Telemetry] ───────► ESP32-S31 (U2) Onboard Ceramic (ANT3)
            (Lean angle, TPMS, eCall, Setup, Turn-by-Turn Navigation via COMM_48)
```

### 2.1 Hi-Fi Music Streaming (A2DP Sink)
* **Codecs:** aptX Adaptive, aptX Lossless, LC3, AAC, SBC.
* **DSP Ducking:** The ESP32-S31 mixer smoothly ducks music by **-12 dB** during navigation prompts and immediately by **-18 dB** during radar and emergency collision alerts.

### 2.2 Full-Duplex Telephony (HFP 1.8 Voice Return Channel)
* **The Problem with Legacy Receivers:** Pure A2DP sinks cannot send voice back to the phone, forcing riders to pull over, take off gloves, and retrieve the phone.
* **The QCC3086 Solution:**
  * Full **Hands-Free Profile (HFP 1.8)** support with `mSBC` and `LC3` wideband speech codecs.
  * **Uplink (Voice Return):** The rider helmet microphone (received via `U13`) is filtered digitally by the DSP (wind noise suppression) and piped back to the smartphone with **< 20 ms latency**.
  * Calls can be conducted at highway speeds with crystal-clear voice fidelity.

### 2.3 Media & Call Control via Factory Handlebar Switches
* **CAN-Bus Integration (100% Listen-Only):**
  * Central Box reads factory handlebar switch frames via the automotive CAN transceiver `TCAN334G` (`U6`):
    * **Harley-Davidson:** Left Hand Control Module (LHCM) and Right Hand Control Module (RHCM).
    * **BMW Motorrad:** Multi-Controller (Wonderwheel) on the left handlebar perch.
* **Command Mapping:**
  * **Music:** Volume (`Vol+`/`Vol-`), Track Next/Prev, Play/Pause ➔ ESP32-S31 translates into **AVRCP 1.6** commands to `U9`.
  * **Telephony:** Incoming call in helmet ➔ Pressing factory switch answers (`ATA`). Long press declines/ends (`AT+CHUP`).
  * **Custom Bikes:** Front Node (`PCBA 05`) provides discrete switch inputs (`BTN_L`, `BTN_R`, PTT).

---

## 3. Glovebox Charging Infrastructure (Genuine 30W Fast Charger)

The fairing glovebox (e.g. right media compartment on Harley Touring) is engineered as a **pure high-performance charging bay**:

### 3.1 Electrical Feed & Fast-Charging Regulator
* **Pure 2-Wire DC Feed:** Protected DC supply from Front Node `J7` / Central Box.
* **Automotive Buck-Boost Controller:** Southchip `SC8721` / `SW3526` delivering up to **30–36 W total power**.
* **Authentic Fast Charging:** Supports **USB Power Delivery 3.0 (PD)** and **QuickCharge 4.0** with 5V / 9V / 12V negotiation. Not a sluggish standard 5V charger!

### 3.2 Magnetic Qi Charging Puck (Qi2 / MagSafe Compatible)
* **Inductive Output:** Negotiates 9V/12V PD and delivers the **standardized 15W inductive fast-charging limit** to the phone.
* **DC Input Consumption:** At ~70% inductive transfer efficiency, the puck draws approximately 20–22 W on the DC feed.
* **Mechanical Hold:** An integrated N52 magnet ring securely locks the smartphone in position even over severe bumps.
* **Thermal Equilibrium:** Because the phone does not run intensive video streaming, battery temperatures remain safe ($< 42\,^\circ\text{C}$).

### 3.3 Secondary USB-C PD Fast-Charge Port
* In addition to the Qi puck, a standard **USB-C PD port (up to 30W)** is available for wired charging of companion devices (tablets, action cams, powerbanks).

---

## 4. Navigation Architecture & Factory Headunits

Modern motorcycle headunits are closed ecosystems. OpenMotorBridge handles navigation across three validated pathways:

```
+----------------------------------------------------------------------------------------+
|                          THREE WAYS TO NAVIGATE WITH OMB                               |
+----------------------------------------------------------------------------------------+

  1. FACTORY HEADUNIT NAVIGATION (Harley Boom! Box / SkylineOS or BMW ConnectedRide TFT)
     [Harley / BMW GPS] ────────(Bluetooth Audio)────► Front Node (PCBA 05 FSC-BT802)
                                                                 │
                                                       (Digital Audio Bus)
                                                                 ▼
     [Rider & Pillion Helmets] ◄── (DSP Ducking -12 dB) ◄── Central Box ESP32-S31 DSP

  2. SMARTPHONE AUDIO NAVIGATION (Kurviger, Calimoto, Google Maps)
     [Smartphone in Pocket/Glovebox] ──(BT A2DP/HFP)──► QCC3086 (U9) ──► ESP32-S31 DSP ──► Helmets

  3. NATIVE OMB COCKPIT DISPLAY (Custom & Naked Bikes)
     [Smartphone App] ──────────(BLE GATT COMM_48)───► ESP32-S31 ──► Cockpit OLED/TFT Display
     (Turn-by-Turn arrows, remaining meters, street name, speed limit)
```

### 4.1 Factory Headunits (Harley SkylineOS / Boom! Box GTS / BMW TFT)
* Factory headunits do not permit external map injection or third-party turn arrows without CarPlay.
* **The OMB Solution:** When the rider uses the bike's built-in navigation on the big display, the **FSC-BT802 transceiver** on Front Node (`PCBA 05`) captures spoken navigation prompts digitally over Bluetooth.
* Central Box DSP ducks background music by -12 dB and plays navigation instructions into both helmets in studio quality.

### 4.2 Smartphone Audio Navigation (Kurviger / Calimoto)
* Many riders prefer winding-road routing apps like Kurviger or Calimoto.
* The phone computes route in the glovebox; turn-by-turn spoken guidance streams via QCC3086 (`U9`). The rider navigates **100% by audio** without glancing down at a screen.

### 4.3 BLE Turn-by-Turn Navigation (`COMM_48`)
* Designed for bikes with the **native OMB Cockpit Display** (custom builds, naked bikes, or auxiliary handlebar displays).
* Smartphone apps broadcast lightweight BLE GATT packets containing maneuver icons, distance in meters, street names, and speed limits directly into the rider's field of view.

---

## 5. Ergonomic & Display Reality: GS/GSA vs. Harley Road Glide

In practice, a fundamental cockpit ergonomics difference exists between adventure bikes and touring baggers:

| Characteristic | BMW GS / GSA & Adventure Bikes | Harley-Davidson Touring (Road Glide / Street Glide) |
| :--- | :--- | :--- |
| **Smartphone Mount Location** | Handlebar / windshield bar (QuadLock / SP Connect) | Tucked away in sealed glovebox on Qi puck |
| **Phone Screen Visibility** | **Directly in rider's line of sight** | **Invisible (inside closed compartment)** |
| **In-Ride App Usage** | The **OMB Companion App** (live lean angle, TPMS, radar halo) or Kurviger map is continuously visible. | **OMB app CANNOT be mirrored to Harley screen** (deliberate removal of Android Auto / CarPlay). |
| **Navigation Practice** | Visual map on handlebar phone or BMW Navigator | **Visual navigation via factory Harley map on 12.3"/6.5" screen**; smartphone provides audio tour prompts, music, and telephony to helmet. |
| **Power Feed (`J4`)** | Flexible feed to handlebar mount | Pure 2-wire DC feed to 30W Qi puck in glovebox |

### The Real-World Touring Balance on Road Glide
We state this factually without embellishment:
* Android Auto would theoretically have allowed projecting our companion app onto the Harley screen.
* Because Android Auto and CarPlay were **deliberately removed due to dongle unreliability, connection drops, and severe glovebox overheating, the OMB app is not visible on the Harley display while riding.**
* The Road Glide rider operates with clear, stress-free roles:
  1. **Big Fairing Screen:** Displays Harley factory maps, tachometer, and vehicle telemetry.
  2. **Helmets:** Zero-latency audio guidance (prompts, Spotify music, full-duplex phone calls, group intercom, radar pings).
  3. **Glovebox:** Phone charges coolly and securely attached to the magnetic Qi puck.
