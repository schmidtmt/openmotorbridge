import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

enum BleState { disconnected, scanning, connecting, connected }

class BleBridgeService extends ChangeNotifier {
  static const String prefLastDeviceId = 'omb_last_ble_device_id';

  // Official OpenMotorBridge GATT UUIDs (firmware/main_controller/src/ble_service_server.cpp)
  static final Guid serviceUuid = Guid('23d113ef-5f78-2315-deef-121200a00000');
  static final Guid telemetryCharUuid = Guid('23d113ef-5f78-2315-deef-121200a00001');
  static final Guid controlCharUuid = Guid('23d113ef-5f78-2315-deef-121200a00002');
  static final Guid gpsAssistCharUuid = Guid('23d113ef-5f78-2315-deef-121200a00004');

  // Legacy fallback UUIDs
  static final Guid serviceUuidFallback = Guid('00000001-omb0-4000-8000-00805f9b34fb');
  static final Guid telemetryCharUuidFallback = Guid('00000002-omb0-4000-8000-00805f9b34fb');
  static final Guid controlCharUuidFallback = Guid('00000003-omb0-4000-8000-00805f9b34fb');
  static final Guid gpsAssistCharUuidFallback = Guid('00000004-omb0-4000-8000-00805f9b34fb');

  BleState _state = BleState.disconnected;
  BluetoothDevice? _connectedDevice;
  List<ScanResult> _scanResults = [];
  StreamSubscription? _scanSub;
  StreamSubscription? _connSub;
  String _statusText = 'Nicht verbunden';

  // Live Telemetry Cache (SystemTelemetry_t)
  double _leanAngle = 0.0;
  double _batteryVoltage = 12.6;
  double _ignitionVoltage = 0.0;
  bool _ignitionOn = false;
  int _radarAlertLevel = 0; // 0=Clear, 1=Approaching, 2=Critical
  int _remoteBatPct = 100;
  bool _gnss3dFix = false;
  int _hwLostMask = 0;

  BleState get state => _state;
  bool get isConnected => _state == BleState.connected;
  String get statusText => _statusText;
  List<ScanResult> get scanResults => _scanResults;
  BluetoothDevice? get connectedDevice => _connectedDevice;

  double get leanAngle => _leanAngle;
  double get batteryVoltage => _batteryVoltage;
  double get ignitionVoltage => _ignitionVoltage;
  bool get ignitionOn => _ignitionOn;
  int get radarAlertLevel => _radarAlertLevel;
  int get remoteBatPct => _remoteBatPct;
  bool get gnss3dFix => _gnss3dFix;
  int get hwLostMask => _hwLostMask;

  BleBridgeService() {
    _initAutoConnect();
  }

  @override
  void dispose() {
    _scanSub?.cancel();
    _connSub?.cancel();
    super.dispose();
  }

  Future<void> _initAutoConnect() async {
    final prefs = await SharedPreferences.getInstance();
    final lastId = prefs.getString(prefLastDeviceId);
    if (lastId != null && lastId.isNotEmpty) {
      startScan(autoConnectId: lastId);
    }
  }

  Future<void> startScan({String? autoConnectId}) async {
    if (_state == BleState.scanning || _state == BleState.connecting) return;

    _state = BleState.scanning;
    _statusText = 'Suche nach OpenMotorBridge Geräten...';
    _scanResults.clear();
    notifyListeners();

    _scanSub?.cancel();
    _scanSub = FlutterBluePlus.scanResults.listen((results) {
      _scanResults = results.where((r) {
        final name = r.device.platformName.toUpperCase();
        return name.contains('OMB') ||
            name.contains('MOTORBRIDGE') ||
            r.advertisementData.serviceUuids.contains(serviceUuid) ||
            r.advertisementData.serviceUuids.contains(serviceUuidFallback);
      }).toList();
      notifyListeners();

      if (autoConnectId != null) {
        for (final r in results) {
          if (r.device.remoteId.str == autoConnectId) {
            connectToDevice(r.device);
            break;
          }
        }
      }
    });

    try {
      await FlutterBluePlus.startScan(timeout: const Duration(seconds: 10));
      await FlutterBluePlus.isScanning.where((s) => !s).first;
    } catch (e) {
      _statusText = 'Scan-Fehler: $e';
    } finally {
      if (_state == BleState.scanning) {
        _state = BleState.disconnected;
        _statusText = _scanResults.isEmpty ? 'Kein Gerät in Reichweite' : 'Geräte gefunden';
        notifyListeners();
      }
    }
  }

  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
    _state = BleState.disconnected;
    notifyListeners();
  }

  Future<void> connectToDevice(BluetoothDevice device) async {
    await stopScan();
    _state = BleState.connecting;
    _statusText = 'Verbinde mit ${device.platformName.isEmpty ? device.remoteId.str : device.platformName}...';
    notifyListeners();

    try {
      await device.connect(license: License.nonprofit, autoConnect: true, timeout: const Duration(seconds: 15));
      _connectedDevice = device;
      _state = BleState.connected;
      _statusText = 'Verbunden mit ${device.platformName}';

      // Save ID for auto-reconnect
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(prefLastDeviceId, device.remoteId.str);

      // Listen to disconnect
      _connSub?.cancel();
      _connSub = device.connectionState.listen((conn) {
        if (conn == BluetoothConnectionState.disconnected) {
          _state = BleState.disconnected;
          _statusText = 'Verbindung getrennt';
          notifyListeners();
        }
      });

      // Discover services & setup telemetry
      await _setupTelemetry(device);
      notifyListeners();
    } catch (e) {
      _state = BleState.disconnected;
      _statusText = 'Verbindung fehlgeschlagen: $e';
      notifyListeners();
    }
  }

  Future<void> disconnect() async {
    _connSub?.cancel();
    await _connectedDevice?.disconnect();
    _connectedDevice = null;
    _state = BleState.disconnected;
    _statusText = 'Getrennt';

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(prefLastDeviceId);
    notifyListeners();
  }

  Future<void> _setupTelemetry(BluetoothDevice device) async {
    final services = await device.discoverServices();
    for (final s in services) {
      for (final c in s.characteristics) {
        if ((c.uuid == telemetryCharUuid || c.uuid == telemetryCharUuidFallback) &&
            c.properties.notify) {
          await c.setNotifyValue(true);
          c.onValueReceived.listen((bytes) {
            _parseTelemetry(bytes);
          });
        }
      }
    }
  }

  void _parseTelemetry(List<int> bytes) {
    if (bytes.length >= 22) {
      // Official packed SystemTelemetry_t from firmware (22 bytes)
      final byteData = ByteData.sublistView(Uint8List.fromList(bytes));
      _ignitionVoltage = byteData.getFloat32(0, Endian.little);
      _batteryVoltage = byteData.getFloat32(4, Endian.little);
      _remoteBatPct = bytes[8];
      // bytes[9] = operation_mode
      // bytes[10] = port1_active, bytes[11] = port2_active
      _gnss3dFix = bytes[12] != 0;
      _leanAngle = bytes[13].toSigned(8).toDouble();
      _hwLostMask = byteData.getUint16(20, Endian.little);
      _ignitionOn = _ignitionVoltage > 5.0;
      _radarAlertLevel = (_hwLostMask != 0) ? 2 : 0;
      notifyListeners();
      return;
    }

    if (bytes.length >= 8) {
      // Legacy / compact telemetry frame
      final flags = bytes[1];
      _ignitionOn = (flags & 0x01) != 0;
      _radarAlertLevel = (flags >> 1) & 0x03;

      final vMv = bytes[2] | (bytes[3] << 8);
      _batteryVoltage = vMv / 1000.0;
      _ignitionVoltage = _ignitionOn ? 14.2 : 0.0;

      final angleRaw = (bytes[4] | (bytes[5] << 8)).toSigned(16);
      _leanAngle = angleRaw / 10.0;

      notifyListeners();
    }
  }

  /// Sends a generic GATT control opcode to the Central Controller
  Future<bool> sendControlCommand(List<int> cmd) async {
    if (_connectedDevice == null || !isConnected) return false;
    try {
      final services = await _connectedDevice!.discoverServices();
      for (final s in services) {
        for (final c in s.characteristics) {
          if (c.uuid == controlCharUuid || c.uuid == controlCharUuidFallback) {
            await c.write(cmd, withoutResponse: false);
            return true;
          }
        }
      }
    } catch (e) {
      debugPrint('Control command write error: $e');
    }
    return false;
  }

  /// Injects u-blox AssistNow binary ephemeris frames into Front Node
  Future<bool> injectAssistNowData(Uint8List ubxBytes) async {
    if (_connectedDevice == null || !isConnected) return false;
    try {
      final services = await _connectedDevice!.discoverServices();
      for (final s in services) {
        for (final c in s.characteristics) {
          if (c.uuid == gpsAssistCharUuid || c.uuid == gpsAssistCharUuidFallback) {
            // Write in 240-byte MTU chunks
            const chunkSize = 240;
            for (var i = 0; i < ubxBytes.length; i += chunkSize) {
              final end = (i + chunkSize < ubxBytes.length) ? i + chunkSize : ubxBytes.length;
              await c.write(ubxBytes.sublist(i, end), withoutResponse: false);
            }
            return true;
          }
        }
      }
    } catch (e) {
      debugPrint('AssistNow write error: $e');
    }
    return false;
  }
}
