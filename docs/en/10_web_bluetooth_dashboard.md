# 10 - Web Bluetooth Dashboard & PWA Frontend

## 1. Zero-Cloud Philosophy & Architecture
The configuration and monitoring dashboard is built as an autonomous Progressive Web App (PWA) using HTML5, Vanilla ES6 JavaScript, and modern CSS3 Glassmorphism:
- **No App Store / No Cloud Account:** Operates directly in Chrome, Edge, and WebBLE-capable browsers on iOS (Bluefy) and Android.
- **Offline Operation:** Service Worker caches all assets for complete offline availability.

## 2. Web Bluetooth GATT Service Profile

| UUID | Name | Permissions | Description |
| :--- | :--- | :---: | :--- |
| `23d113ef-5f78-2315-deef-121200a00000` | **OMB Primary Service** | - | Main GATT Service |
| `23d113ef-5f78-2315-deef-121200a00001` | **Telemetry Characteristic** | Notify | 10 Hz Telemetry Frame (Voltage, Lean Angle, GPS, Batteries) |
| `23d113ef-5f78-2315-deef-121200a00002` | **Control Characteristic** | Write | Audio mode switch, Gain settings, Trigger pulses |

## 3. UI Features
- **Live Cockpit:** Real-time lean angle horizon indicator (BMI270 EKF), speed, satellite count, and 1-PPS lock.
- **Power & Thermal:** KL15/KL30 voltage, 5 starter battery chemistry selector, LiPo UPS state, and JEITA thermal status (< 0°C / > 45°C).
- **Audio Matrix & Ducking:** Mode selection with live dB meters and gain sliders.
- **Cartridge Manager & Wizard:** Cartridge identification, DLE leader score breakdown, and onboarding wizard.
- **Tour Manager:** SDIO storage gauge with BGH purge status and WebDAV configuration.
- **Reserve I/O:** Controls for Pins 25 & 26.
- **Built-in Demo Simulation:** Complete sensor physics simulation for instant testing without hardware.
