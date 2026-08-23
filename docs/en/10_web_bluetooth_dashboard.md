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
