# 07 - MicroSD Storage, BGH Ring Buffer, WebDAV Sync & USB MSC

This document specifies the high-speed 4-bit SDIO memory bus, the GDPR/BGH-compliant ring buffer, automated WebDAV synchronization, and the **minimal USB Mass Storage Class (MSC) mode** for direct PC/Mac file transfer.

---

## 1. Storage Interface & High-Speed SDIO

* **Interface:** Native 4-bit SDIO bus @ 40 MHz attached to ESP32-S3 (GPIOs 40–45).
* **Throughput:** Sustained sequential write throughput $> 12\,\text{MB/s}$ (guarantees drop-free 10 Hz GPX, IMU, and telemetry logging).
* **Filesystem:** FAT32 with dynamic sector buffering (32 kB cluster size).

---

## 2. Ring Buffer & BGH Compliance (BGH VI ZR 233/17 / GDPR)

* **Rolling Buffer:** Tour tracks are saved as a circular buffer inside the `/tracks/` directory.
* **Auto-Purge Threshold:** When free storage falls below $200\,\text{MB}$, the firmware automatically purges the oldest unprotected GPX logs in 50 MB chunks.
* **Highlight Write-Protection:** Manually flagged video highlights or tours marked as favorites in the WebApp (`*.fav.gpx`) are permanently write-protected against automatic purging.

---

## 3. WebDAV Sync in Home Wi-Fi

* **Automatic Network Scan:** Upon ignition shutoff (KL15 $< 11.8\,\text{V}$), the system scans for known home Wi-Fi SSIDs during the 15-minute UPS rundown.
* **TLS 1.3 Upload:** If a configured network is found, the integrated WebDAV client uploads newly recorded GPX tracks encrypted via TLS 1.3 to Nextcloud, ownCloud, or Synology NAS (transfer speed $\approx 1.8\,\text{MB/s}$).
* **Clean Rundown:** Once synchronization concludes, the filesystem is cleanly unmounted and the unit transitions to deep sleep.

---

## 4. USB Mass Storage Class (MSC) & Minimal Boot Mode

When the main box is connected to a PC, Mac, or tablet via its native USB-C port while motorcycle ignition (KL15) is off, the ESP32-S3 launches into **Minimal USB MSC Mode**:

```
┌─────────────────────────────────────────────────────────────┐
│             MINIMAL USB MASS STORAGE CLASS MODE             │
├─────────────────────────────────────────────────────────────┤
│ • VBUS Detection (5V active on native USB-C port)           │
│ • Main Power Gates & Audio DSP (ES8388) remain ISOLATED     │
│ • Radio transceivers (LoRa, Mesh, BLE) remain SHUT DOWN     │
│ • Current Draw from USB Port: < 80 mA (Zero battery drain)  │
│ • MicroSD card is mounted and presented as USB Flash Drive  │
└─────────────────────────────────────────────────────────────┘
```

### Key Advantages in Practice:
1. **No Tools / No Card Removal:** The MicroSD card stays safely sealed inside the IP67 housing. The host PC immediately mounts the volume as `OPENMOTOR`.
2. **Direct Access:** Track logs in `/tracks/` can be opened directly in Google Earth, BaseCamp, or Kurviger, and profile JSON files in `/profiles/` can be configured on the desktop.
3. **Vehicle Battery Protection:** Only the USB stack and SDIO controller are powered; all vehicle electronics and high-power stages remain completely powered off.
