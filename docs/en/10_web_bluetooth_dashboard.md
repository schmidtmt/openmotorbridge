# 10 - Web Bluetooth Dashboard & PWA Frontend

This document specifies the progressive web app (PWA) architecture, Web Bluetooth (WebBLE) communication pipeline, local **IndexedDB offline storage**, and the **extended GPX export engine** (navigation shaping points & actioncam video telemetry).

---

## 1. Architecture & Offline Capabilities
The dashboard is a self-contained Progressive Web App (PWA) built with modern HTML5, CSS3, and ES6 JavaScript. The application communicates directly with the ESP32-S3 host MCU via Web Bluetooth API (WebBLE) – without cloud requirements or mandatory external servers.
- **Local Offline Storage (IndexedDB):** Recorded GPX tour tracks can be transferred via BLE and persisted locally within the browser's `omb_tours_db`.
- **Service Worker Caching:** Full offline installation support across iOS and Android utilizing cache-first strategies.

---

## 2. Telemetry & Control Capabilities
- **Real-Time Telemetry:** Live monitoring of motorcycle electrical voltage (KL15/KL30), UPS battery health (BQ24075), and handlebar remote CR2032 state (BLE Service 0x180F).
- **Audio Matrix Controller:** Dynamic mode selection (Standard, Single Rider, Cruise Mode) with interactive gain sliders and ducking threshold configuration.
- **Cartridge Profile Manager:** Automatic 1-Wire DS2401 detection, profile rendering, and ground-truth mesh channel re-sync.
- **Cartridge Onboarding Wizard:** Step-by-step guidance for pristine RF isolation (disabling classic Bluetooth, resetting pairings, pure mesh operation).
- **WS2812B RGB Status LED Widget:** Live reflection of physical enclosure LED states.

---

## 3. Extended GPX Export & Navigation Formatting

The integrated GPX Export Engine transforms recorded 10 Hz raw dead-reckoning tracks into 4 specialized export formats:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       OMB GPX EXPORT ENGINE PROFILES                        │
├───────────────────┬───────────────────────────────┬─────────────────────────┤
│ Export Profile    │ Target Navigation Systems     │ Key Features            │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **1. Moto-Navi**  │ Garmin Zūmo XT/XT2, BMW CRN,  │ • Road-Snapping (OSM)   │
│    **(Shaping)**  │ Kurviger, Calimoto, TomTom    │ • Strategic Via-Points  │
│                   │                               │ • Garmin `<gpxx:>` Ext  │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **2. Video-Sync** │ Telemetry Overlay, VIRB Edit, │ • 10 Hz 1-PPS Timecode  │
│    **(HiFi EKF)** │ Dashware, Insta360, GoPro     │ • Lean angle (deg)      │
│                   │                               │ • Video highlight tags  │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **3. Clean Track**│ Google Earth, Komoot, Relive, │ • Douglas-Peucker RDP   │
│    **(Visual)**   │ Strava, Apple/Google Maps     │ • Compact file size     │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ **4. Raw EKF**    │ Engineering, MATLAB, Analysis │ • Raw IMU & CAN sensor  │
│    **(Diagnose)** │                               │   telemetry streams     │
└───────────────────┴───────────────────────────────┴─────────────────────────┘
```

1. **Garmin / BMW Shaping Points (`<rtept>` & `<gpxx:RoutePointExtension>`):**
   * Prevents motorcycle navigators from recalibrating routes by injecting silent shaping points along mountain passes and scenic curves.
2. **Actioncam Timecode Sync (`<omb:action_event>`):**
   * Embeds handlebar remote clicks as frame-accurate highlight cut marks.

---

## 4. Smart Firmware & OEM Adapter Update-Hub

The dashboard integrates a unified update hub for all system firmware and OEM intercom modules:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 SMART FIRMWARE & OEM ADAPTER UPDATE-HUB                     │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 📡 OMM Rear Pod 3 In-System Flasher  │ 🎴 Sena / Cardo Mesh 3.0 Assistant   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • 1-Click High-Speed UART Push       │ • 1. Auto-Pairing Pulse (TLP222A 5s) │
│ • 460,800 Baud SLIP Loader           │ • 2. Deep-Link to OEM Mobile App     │
│ • Automated MD5 Hash Verification    │ • 3. JSON Profile-Merge & Gain-Sync  │
│ • Zero Motorcycle Disassembly        │ • No Manual Button Acrobatics        │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

1. **OMM In-System Firmware Push:**
   * Streams `omm_rear.bin` directly over the 6-pin UART interface to the ESP32-C3 coprocessor with animated real-time progress ($< 6\,\text{s}$).
2. **Sena & Cardo Smart Adapter Assistant:**
   * **Step 1:** Automatically triggers the cartridge's TLP222A optocoupler with a 5-second pulse to enter Bluetooth pairing mode.
   * **Step 2:** Deep-links directly to the official Sena or Cardo mobile app for wireless vendor firmware updates.
   * **Step 3:** Merges updated vendor JSON profiles (e.g. `sena_apex_v3.json`) with customized audio ducking and gain presets.

