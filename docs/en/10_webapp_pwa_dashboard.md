# 10 - WebApp PWA & Dashboard Operation

This document specifies the architecture of the standalone **Progressive Web App (PWA) Dashboard**, the Web Bluetooth (WebBLE) communication layer, local **IndexedDB offline storage**, the control interface for the **Universal Front Node** (1-click CarPlay hard reboot, wind noise VU meter, Auto-Café countdown), and the **advanced GPX export engine** (Navi Shaping Points & Video Telemetry).

---

## 1. Architecture & Offline Capability

The dashboard is a fully self-contained Progressive Web App (PWA) built with standard HTML5, modern vanilla CSS3 (Glassmorphism theme), and modular ES6 JavaScript. The application communicates directly with the ESP32-S3 via the Web Bluetooth API (WebBLE)—completely free of cloud dependencies:

- **Local Offline Storage (IndexedDB):** GPX rides can be downloaded via BLE directly from the internal MicroSD card and stored persistently in the browser's `omb_tours_db`.
- **Service Worker Caching:** Employs a cache-first strategy for smooth offline operation on iOS and Android.

### 1.1 Platform Compatibility

| Platform | Recommended Browser | Connection Details |
| :--- | :--- | :--- |
| **Android / PC / Mac / Linux** | **Google Chrome, MS Edge, Opera** | **Native:** Direct Web Bluetooth support under HTTPS or `http://localhost`. |
| **Apple iOS / iPadOS** (iPhone, iPad) | **[Bluefy – Web BLE Browser](https://apps.apple.com/app/bluefy-web-ble-browser/id1492822055)** | **Required:** Apple restricts WebBLE in WebKit/Safari. Bluefy provides a standard-compliant bridge using Apple CoreBluetooth. |

---

## 2. Dashboard Navigation & Functional Tabs

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OPENMOTORBRIDGE PWA DASHBOARD NAVIGATION                        │
├─────────────────┬─────────────────┬──────────────────┬────────────────┬────────────────┤
│ 📊 Cockpit &    │ 🎧 Audio &      │ 🧩 Cartridges &  │ 🗺️ Tours &     │ ⚙️ Hardware &   │
│    Power        │    Ducking      │    DLE           │    WebDAV      │    Reserve     │
└─────────────────┴─────────────────┴──────────────────┴────────────────┴────────────────┘
```

### 2.1 Tab 1: Cockpit & Power (`#tab-cockpit`)
* **Vehicle Dynamics & Lean Angle:** Real-time animated motorcycle attitude indicator (15-state EKF with Bosch BMI270).
* **Universal Front Node Dashboard Card:**
  * **Link Status:** Live 2.4 GHz ESP-NOW wireless status badge.
  * **Subsystem Tiles:**
    1. **📱 Wireless CarPlay / AA (Ottocast):** Live voltage & current (`5.00 V · 380 mA`), operating status (`ACTIVE`, `REBOOT`, `STANDBY`).
    2. **⚡ Handlebar PTT (Zero-Latency):** Status indicator (`< 1.8 ms Latency`) with glowing pulse animation when keying.
    3. **🎙️ Cockpit Noise (Knowles MEMS):** Real-time sound pressure level in $\text{dB(A)}$ and dynamic AGC helmet boost (`+0.0 dB` to `+6.0 dB Boost`).
  * **Wind Noise VU Meter:** Color-coded level bar ($35\,\text{dB(A)}$ idle to $115\,\text{dB(A)}$ highway).
  * **Interactive Controls:**
    * **`⚡ CarPlay 1-Click Hard Reboot (2.5s)`:** Triggers a hardware power cycle on the TI TPS2051B switch (2.5s VBUS cutoff with countdown animation).
    * **`🔘 Test Handlebar PTT`:** Simulates mechanical button presses with tactile feedback.
    * **`Auto-Café Mode (60s)` Toggle:** Automatically cuts VBUS after ignition OFF to release smartphone Wi-Fi for café/hotel networks.

### 2.2 Tab 2: Audio & Ducking (`#tab-audio`)
* **Mode Selector:** Standard Mode (Mesh Bridge), Single Rider Mode, Cruise Mode.
* **Sliders:** Input sensitivity for Port 1 (Sena) and Port 2 (Cardo), Ducking depth, and Transparency volume.

### 2.3 Tab 3: Cartridges & DLE (`#tab-cartridges`)
* **Live Slot Status:** Visual display of active cartridges in Slot 1 and Slot 2 with 1-Wire UIDs.
* **Cartridge Onboarding Wizard:** 3-step interactive pairing guide.

### 2.4 Tab 4: Tours & WebDAV (`#tab-tours`)
* **Tour History:** Tabular list of all recorded GPX rides with dates, distances, and peak lean angles.
* **GPX Export Engine:** Download rides in 4 optimized formats (Moto-Navi Shaping, Video-Sync, Clean Track, Raw EKF).

### 2.5 Tab 5: Hardware & Reserve (`#tab-hardware`)
* **Front Node Diagnostics:** Hardware specifications (ESP32-C3, LMR36015, USB2512B, TPS2051B, Knowles MEMS) and OTA firmware check.
