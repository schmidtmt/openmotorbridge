# 06 - Telemetry Blackbox, SDIO Ringbuffer & WebDAV Sync

This document specifies the storage and telemetry subsystem of OpenMotorBridge v8.0: the 4-bit high-speed SDIO bus, the GDPR/BGH-compliant rolling ringbuffer with cryptographic signatures, the automated TLS-secured WebDAV cloud upload, and the **low-power USB Mass Storage Class (MSC) mode** for direct PC access.

---

## 1. High-Speed SDIO Storage Interface (4-Bit @ 40 MHz)

* **Interface:** Native 4-bit SDIO bus operating at 40 MHz connected to ESP32-S3 (GPIOs 40–45).
* **Throughput:** Continuous write speeds $> 12\,\text{MB/s}$ (enabling uninterrupted 10 Hz GPX, IMU, and audio telemetry logging).
* **Filesystem:** FAT32 with dynamic sector buffering (32 kB cluster size).
* **Failsafe:** The integrated BQ24075 UPS buffer guarantees clean unmounting and closing of FAT file allocation tables during abrupt power losses.

---

## 2. Rolling Ringbuffer & Court Admissibility (BGH VI ZR 233/17 & GDPR)

To comply with European data privacy regulations (GDPR Art. 5 & 25) and German Federal Court of Justice rulings (BGH VI ZR 233/17) regarding unprompted surveillance in road traffic:

```
┌─────────────────────────────────────────────────────────────┐
│          GDPR-COMPLIANT ROLLING RINGBUFFER ARCHITECTURE      │
├─────────────────────────────────────────────────────────────┤
│ • Continuous rolling buffer directory: /tracks/             │
│ • Auto-Purge Threshold: Free space < 200 MB                 │
│ • Oldest unprotected track segments overwritten in 50MB blk │
│ • Manual highlight protection via handlebar switch (*.fav)  │
│ • Crash sensor trigger: Impact > 4G locks last 15 min.      │
└─────────────────────────────────────────────────────────────┘
```

1. **Rolling Ringbuffer:** Normal riding data is recorded in 15-minute segments and cyclically overwritten.
2. **Crash Freeze:** If the Bosch BMI270 IMU detects a severe deceleration impact ($> 4{,}0\,\text{g}$) or an engine cutoff accompanied by high tilt, the last 15 minutes plus subsequent rundown data are permanently write-protected.
3. **Cryptographic Integrity (ECDSA SHA-256):** Every recorded segment is signed using a hardware key stored in the ESP32 eFuse/ATECC608A to provide tamper-proof evidence for accident reconstruction.

---

## 3. Automatic WebDAV / Nextcloud Upload in Home Wi-Fi

```
MOTORCYCLE ENTERS GARAGE (IGNITION OFF)
┌─────────────────────────────────────────────────────────────┐
│ 1. KL15 drops -> UPS rundown timer initiates (Graceful Run) │
│ 2. ESP32-S3 scans for configured Home Wi-Fi SSIDs for 60 s  │
│ 3. Wi-Fi connects via WPA2/WPA3 Personal / Enterprise       │
│ 4. TLS 1.3 Client connects to Nextcloud / ownCloud / NAS    │
│ 5. Automated upload of new *.gpx tracks and logs (1.8 MB/s) │
│ 6. Sync complete confirmation -> Filesystem unmount -> Sleep│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Minimal USB Mass Storage Class (MSC) Mode

Connecting the Central Box to a PC, Mac, or tablet via USB-C while the motorcycle ignition is OFF activates the **Minimal USB MSC Mode**:

```
┌─────────────────────────────────────────────────────────────┐
│             MINIMAL USB MASS STORAGE CLASS MODE             │
├─────────────────────────────────────────────────────────────┤
│ • VBUS detection (5V on native USB-C port)                  │
│ • Main power relays & audio DSP (ES8388) remain UNPOWERED   │
│ • Wireless modules (LoRa, Mesh, Bluetooth) remain DISABLED  │
│ • Current draw from USB port: < 80 mA (Zero battery drain)  │
│ • MicroSD card mounts instantly as standard flash drive     │
└─────────────────────────────────────────────────────────────┘
```

* **No Tools Required:** The MicroSD card stays safely sealed inside the IP67 enclosure. The computer immediately detects the drive `OPENMOTOR`.
* **Instant Access:** Rides can be opened directly in Google Earth, BaseCamp, GPXSee, or Kurviger.
