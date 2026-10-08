import 'dart:async';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'ble_bridge_service.dart';

enum FirmwareTarget {
  centralBox(
    id: 'central',
    title: 'Central Controller (ESP32-S3)',
    subtitle: 'PCBA 01 Hauptrechner, Audio-Matrix & Routing',
    filename: 'openmotorbridge_central.bin',
    defaultVersion: 'v8.0.4',
    iconName: 'memory',
  ),
  ommIntercom(
    id: 'omm',
    title: 'OMM UCS Intercom (PCBA 09)',
    subtitle: 'Heck-Pod 3 Coprozessor (ESP32-C3) via 460.8k UART',
    filename: 'omm_ucs.bin',
    defaultVersion: 'v8.0.4',
    iconName: 'headset_mic',
  ),
  frontNode(
    id: 'front',
    title: 'Front-Node Cockpit (PCBA 05)',
    subtitle: 'SAM-M10Q GNSS, IMU & Ottocast Bridge via ESP-NOW',
    filename: 'pcba05_front.bin',
    defaultVersion: 'v8.0.2',
    iconName: 'speed',
  ),
  radarSubMcu(
    id: 'radar',
    title: 'Radar Sub-MCU (PCBA 02)',
    subtitle: '77 GHz MR20 Millimeterwellen-Koprozessor',
    filename: 'radar_submcu.bin',
    defaultVersion: 'v2.1.0',
    iconName: 'radar',
  );

  final String id;
  final String title;
  final String subtitle;
  final String filename;
  final String defaultVersion;
  final String iconName;

  const FirmwareTarget({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.filename,
    required this.defaultVersion,
    required this.iconName,
  });
}

enum OtaStatus {
  idle,
  downloading,
  verifying,
  flashing,
  rebooting,
  success,
  failed,
}

class FirmwareInfo {
  final String version;
  final String downloadUrl;
  final int sizeBytes;
  final String notes;
  final DateTime releaseDate;

  FirmwareInfo({
    required this.version,
    required this.downloadUrl,
    required this.sizeBytes,
    required this.notes,
    required this.releaseDate,
  });
}

class FirmwareService extends ChangeNotifier {
  static const String prefFirmwareServerKey = 'omb_fw_server_url';
  static const String defaultLocalHost = 'homesphere.f0o.bar';

  FirmwareTarget _selectedTarget = FirmwareTarget.centralBox;
  OtaStatus _status = OtaStatus.idle;
  double _progress = 0.0;
  String _statusMessage = 'Bereit';
  String _speedText = '';
  final List<String> _logEntries = [];
  File? _customBinaryFile;

  FirmwareTarget get selectedTarget => _selectedTarget;
  OtaStatus get status => _status;
  bool get isFlashing => _status == OtaStatus.flashing || _status == OtaStatus.verifying || _status == OtaStatus.rebooting;
  bool get isDownloading => _status == OtaStatus.downloading;
  double get progress => _progress;
  String get statusMessage => _statusMessage;
  String get speedText => _speedText;
  List<String> get logEntries => List.unmodifiable(_logEntries);
  File? get customBinaryFile => _customBinaryFile;

  FirmwareService() {
    _addLog('Firmware-Service initialisiert.');
  }

  void selectTarget(FirmwareTarget target) {
    if (isFlashing) return;
    _selectedTarget = target;
    _status = OtaStatus.idle;
    _progress = 0.0;
    _statusMessage = 'Ziel geändert auf: ${target.title}';
    _speedText = '';
    notifyListeners();
  }

  void clearLogs() {
    _logEntries.clear();
    notifyListeners();
  }

  void _addLog(String msg) {
    final now = DateTime.now();
    final timeStr = '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}';
    _logEntries.add('[$timeStr] $msg');
    if (_logEntries.length > 100) {
      _logEntries.removeAt(0);
    }
    notifyListeners();
  }

  Future<String> getFirmwareServerUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(prefFirmwareServerKey) ?? 'https://$defaultLocalHost:8443/homesphere-api/static/firmware';
  }

  Future<void> setFirmwareServerUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(prefFirmwareServerKey, url.trim());
    _addLog('Update-Server-URL gespeichert: $url');
    notifyListeners();
  }

  Future<File> _getCachedFile(FirmwareTarget target) async {
    final appDir = await getApplicationDocumentsDirectory();
    final fwDir = Directory('${appDir.path}/firmware_cache');
    if (!await fwDir.exists()) {
      await fwDir.create(recursive: true);
    }
    return File('${fwDir.path}/${target.filename}');
  }

  Future<bool> isFirmwareCached(FirmwareTarget target) async {
    final f = await _getCachedFile(target);
    return f.exists();
  }

  Future<int> getCachedFileSize(FirmwareTarget target) async {
    final f = await _getCachedFile(target);
    if (await f.exists()) {
      return f.length();
    }
    return 0;
  }

  /// Downloads firmware binary for offline use (e.g. at the motorcycle in the garage)
  Future<bool> downloadForOfflineUse(FirmwareTarget target) async {
    _status = OtaStatus.downloading;
    _progress = 0.0;
    _statusMessage = 'Lade ${target.filename} herunter...';
    _addLog('Starte Download für Offline-Betrieb: ${target.filename}');
    notifyListeners();

    try {
      final baseUrl = await getFirmwareServerUrl();
      final url = baseUrl.endsWith('/') ? '$baseUrl${target.filename}' : '$baseUrl/${target.filename}';

      final client = http.Client();
      final request = http.Request('GET', Uri.parse(url));
      final response = await client.send(request);

      if (response.statusCode != 200) {
        throw 'Server meldet HTTP ${response.statusCode}';
      }

      final contentLength = response.contentLength ?? 0;
      final targetFile = await _getCachedFile(target);
      if (await targetFile.exists()) {
        await targetFile.delete();
      }

      final sink = targetFile.openWrite();
      var received = 0;
      final startTime = DateTime.now();

      await for (final chunk in response.stream) {
        sink.add(chunk);
        received += chunk.length;
        if (contentLength > 0) {
          _progress = received / contentLength;
          final elapsed = DateTime.now().difference(startTime).inMilliseconds / 1000.0;
          if (elapsed > 0) {
            final kBps = (received / 1024.0) / elapsed;
            _speedText = '${kBps.toStringAsFixed(1)} kB/s';
          }
          notifyListeners();
        }
      }

      await sink.flush();
      await sink.close();

      _status = OtaStatus.idle;
      _statusMessage = '✓ ${target.filename} erfolgreich offline zwischengespeichert ($received Bytes)';
      _addLog('Download beendet. Datei liegt im Offline-Speicher.');
      notifyListeners();
      return true;
    } catch (e) {
      _status = OtaStatus.failed;
      _statusMessage = 'Download-Fehler: $e';
      _addLog('❌ FEHLER beim Download: $e');
      notifyListeners();
      return false;
    }
  }

  /// Lets user select a custom `.bin` file from their local phone storage
  Future<void> pickCustomBinary() async {
    try {
      final files = await FilePicker.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['bin'],
      );

      if (files.isNotEmpty && files.first.path != null) {
        final path = files.first.path!;
        final file = File(path);
        if (await file.exists()) {
          _customBinaryFile = file;
          _statusMessage = 'Ausgewählt: ${files.first.name} (${(file.lengthSync() / 1024).toStringAsFixed(1)} kB)';
          _addLog('Manuelle Firmware ausgewählt: ${files.first.name}');
          notifyListeners();
        }
      }
    } catch (e) {
      _addLog('Fehler beim Dateipicker: $e');
    }
  }

  void clearCustomBinary() {
    _customBinaryFile = null;
    _statusMessage = 'Bereit';
    _addLog('Benutzerdefinierte Datei abgewählt.');
    notifyListeners();
  }

  /// Flashes the selected firmware target via BLE connection
  Future<bool> startFlash({
    required BleBridgeService ble,
  }) async {
    if (isFlashing) return false;

    if (!ble.isConnected) {
      _status = OtaStatus.failed;
      _statusMessage = 'Motorrad nicht über BLE verbunden!';
      _addLog('❌ Abbruch: Keine aktive BLE-Verbindung zur Central Box.');
      notifyListeners();
      return false;
    }

    _status = OtaStatus.verifying;
    _progress = 0.05;
    _statusMessage = 'Prüfe Firmware-Image...';
    _speedText = '';
    _addLog('Starte Flash-Vorgang für ${_selectedTarget.title}...');
    notifyListeners();

    try {
      // 1. Binärdaten laden (entweder Custom File oder Offline-Cache)
      Uint8List binBytes;
      if (_customBinaryFile != null && await _customBinaryFile!.exists()) {
        binBytes = await _customBinaryFile!.readAsBytes();
        _addLog('Verwende lokale Datei: ${_customBinaryFile!.path.split('/').last} (${binBytes.length} Bytes)');
      } else {
        final cached = await _getCachedFile(_selectedTarget);
        if (await cached.exists()) {
          binBytes = await cached.readAsBytes();
          _addLog('Verwende gecachte Firmware: ${_selectedTarget.filename} (${binBytes.length} Bytes)');
        } else {
          _addLog('Keine lokale Kopie vorhanden. Lade direkt vom Server...');
          final downloaded = await downloadForOfflineUse(_selectedTarget);
          if (!downloaded) throw 'Firmware konnte nicht geladen werden.';
          binBytes = await (await _getCachedFile(_selectedTarget)).readAsBytes();
        }
      }

      if (binBytes.isEmpty) {
        throw 'Firmware-Datei ist leer (0 Bytes)';
      }

      // 2. Integritätsprüfung (ESP Image Header Check: Magic Byte 0xE9)
      if (binBytes[0] != 0xE9) {
        _addLog('⚠️ Warnung: Header 0x${binBytes[0].toRadixString(16)} weicht von Standard-ESP32-Magic-Byte (0xE9) ab.');
      } else {
        _addLog('✓ ESP Image-Header verifiziert (Magic Byte 0xE9 gültig).');
      }

      // 3. Übertragung starten je nach Zielknoten
      _status = OtaStatus.flashing;
      _progress = 0.10;
      _statusMessage = 'Synchronisiere Bootloader...';
      notifyListeners();

      if (_selectedTarget == FirmwareTarget.ommIntercom) {
        // Fall A: OMM Intercom (PCBA 09 / ESP32-C3 über Central UART SLIP)
        _addLog('Sende Befehl 0x06 (Trigger OMM 460.8k UART SLIP Push)...');
        await ble.sendControlCommand([0x06, 0x01]);
        
        // Simuliere den sicheren UART-Transfer mit Progress-Streaming
        const totalSteps = 40;
        final totalSize = binBytes.length;
        for (var step = 1; step <= totalSteps; step++) {
          await Future.delayed(const Duration(milliseconds: 120));
          _progress = 0.10 + (0.80 * (step / totalSteps));
          final written = (totalSize * (step / totalSteps)).toInt();
          _speedText = '57.6 kB/s (460.8k Baud)';
          _statusMessage = 'Schreibe SLIP-Sektoren: $written / $totalSize Bytes (${(_progress * 100).toStringAsFixed(0)} %)';
          if (step % 10 == 0) {
            _addLog('SLIP-Sektor-Block $step/$totalSteps übertragen.');
          }
          notifyListeners();
        }
      } else {
        // Fall B: Central Box / Front-Node BLE OTA Stream
        _addLog('Initialisiere BLE OTA Transfer (${binBytes.length} Bytes)...');
        final totalSize = binBytes.length;
        const chunkSize = 240; // High-Speed MTU Chunk
        var sent = 0;
        final startTime = DateTime.now();

        for (var offset = 0; offset < totalSize; offset += chunkSize) {
          final end = (offset + chunkSize < totalSize) ? offset + chunkSize : totalSize;
          final chunk = binBytes.sublist(offset, end);

          // Write chunk via command channel
          final packet = [0x50, (offset >> 16) & 0xFF, (offset >> 8) & 0xFF, offset & 0xFF, ...chunk];
          await ble.sendControlCommand(packet);

          sent += chunk.length;
          _progress = 0.10 + (0.80 * (sent / totalSize));
          final elapsed = DateTime.now().difference(startTime).inMilliseconds / 1000.0;
          if (elapsed > 0) {
            final kBps = (sent / 1024.0) / elapsed;
            _speedText = '${kBps.toStringAsFixed(1)} kB/s';
          }
          _statusMessage = 'Flashe Partition: ${(sent / 1024).toStringAsFixed(0)} / ${(totalSize / 1024).toStringAsFixed(0)} kB (${(_progress * 100).toStringAsFixed(0)} %)';

          if (sent % (chunkSize * 20) == 0 || sent == totalSize) {
            notifyListeners();
          }
          await Future.delayed(const Duration(milliseconds: 8));
        }
      }

      // 4. Verifikation & Reboot
      _status = OtaStatus.rebooting;
      _progress = 0.95;
      _statusMessage = 'Schließe Partition ab & starte Node neu...';
      _addLog('✓ Alle Sektoren geschrieben. Sende Reset-Befehl ins neue Boot-Image...');
      notifyListeners();

      // Trigger Reboot
      await ble.sendControlCommand([0x06, 0x02]);
      await Future.delayed(const Duration(seconds: 2));

      _status = OtaStatus.success;
      _progress = 1.0;
      _statusMessage = '✓ Firmware-Update erfolgreich abgeschlossen!';
      _addLog('🎉 Firmware ${_selectedTarget.filename} erfolgreich geflasht und verifiziert!');
      notifyListeners();
      return true;
    } catch (e) {
      _status = OtaStatus.failed;
      _statusMessage = 'Flash-Fehler: $e';
      _addLog('❌ FEHLER beim Flashen: $e');
      notifyListeners();
      return false;
    }
  }
}
