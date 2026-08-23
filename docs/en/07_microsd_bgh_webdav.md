# 07 - MicroSD Storage, BGH Compliant Ring Buffer & WebDAV Auto-Sync

## 1. High-Speed 4-Bit SDIO Interface
Track logs are recorded directly to an automotive grade MicroSD card (FAT32) using the native 4-bit SDIO hardware bus of the ESP32-S3:
- **Bus Speed:** 40 MHz clock with 4 data lines (DAT0..DAT3).
- **Format:** GPX 2.0 with custom OpenMotorBridge XML telemetry extensions (`<omb:telemetry>` for lean angle, speed, voltage, satellite lock).

## 2. BGH VI ZR 233/17 & GDPR Ring Buffer Compliance
To comply with legal data protection requirements and precedent German dashcam rulings:
- Logs are stored in rolling 15-minute segments (`/tracks/tour_YYYYMMDD_HHMMSS.gpx`).
- When free storage drops below **200 MB**, the oldest unprotected track files are automatically purged.
- **Permanent Preservation:** Key moments can be flagged by pressing the handlebar remote button or via 1-PPS action cam trigger. Flagged tracks are renamed to `*.fav.gpx` and protected from automated deletion.

## 3. Post-Ride WebDAV Auto-Sync (TLS 1.3)
When vehicle ignition is turned off (`KL15 = OFF`), the central box enters its graceful shutdown buffer:
1. Flushes and finalizes the active GPX file.
2. Scans for known home Wi-Fi SSIDs (e.g. garage network).
3. Connects via **TLS 1.3** and uploads pending GPX tracks to a configured WebDAV server (Nextcloud, Synology NAS, QNAP).
4. Powers down into ULP sleep mode upon successful sync.
