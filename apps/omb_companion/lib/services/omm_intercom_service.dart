import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'ble_bridge_service.dart';

class OmmIntercomService extends ChangeNotifier {
  static const String prefOmm446Mode = 'omb_omm446_mode';
  static const String prefOmm446Channel = 'omb_omm446_channel';
  static const String prefOmm446Ctcss = 'omb_omm446_ctcss';
  static const String prefOmm446ColorCode = 'omb_omm446_color_code';
  static const String prefOmm446Squelch = 'omb_omm446_squelch';
  static const String prefOmm446Power = 'omb_omm446_power';
  static const String prefOmm24MeshMode = 'omb_omm24_mesh_mode';
  static const String prefOmm24Channel = 'omb_omm24_channel';
  static const String prefOmm24Volume = 'omb_omm24_volume';

  // 16 PMR446 Standard Channels
  static const List<double> pmrFrequencies = [
    446.00625, // Ch 1
    446.01875, // Ch 2
    446.03125, // Ch 3
    446.04375, // Ch 4
    446.05625, // Ch 5
    446.06875, // Ch 6
    446.08125, // Ch 7
    446.09375, // Ch 8 (Mountain / Emergency / Motorcycle)
    446.10625, // Ch 9
    446.11875, // Ch 10
    446.13125, // Ch 11
    446.14375, // Ch 12
    446.15625, // Ch 13
    446.16875, // Ch 14
    446.18125, // Ch 15
    446.19375, // Ch 16
  ];

  // 38 Standard CTCSS Subtones (Index 0 = Off)
  static const List<double> ctcssTones = [
    0.0,
    67.0, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8,
    97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3, 131.8,
    136.5, 141.3, 146.2, 151.4, 156.7, 162.2, 167.9, 173.8, 179.9, 186.2,
    192.8, 203.5, 210.7, 218.1, 225.7, 233.6, 241.8, 250.3,
  ];

  // OMM 446 State
  String _omm446Mode = 'analog'; // 'analog' (PMR446) or 'dmr' (DMR Tier I)
  int _omm446Channel = 8; // Default Ch 8 (Bergrettung / Wanderkanal)
  int _omm446Ctcss = 16; // Default Subtone 16 (114.8 Hz)
  int _omm446ColorCode = 1; // 1..16
  int _omm446Squelch = 3; // 1..8
  String _omm446Power = 'high'; // 'high' (0.5W Bike) or 'low' (0.2W Helmet)
  bool _isPttActive = false;

  // OMM 2.4 GHz State
  String _omm24MeshMode = 'open'; // 'open' (Open Convoy) or 'private' (AES-128)
  int _omm24Channel = 1; // 1..16
  int _omm24Volume = 80; // 0..100%
  int _omm24PeersCount = 4;

  String get omm446Mode => _omm446Mode;
  int get omm446Channel => _omm446Channel;
  int get omm446Ctcss => _omm446Ctcss;
  int get omm446ColorCode => _omm446ColorCode;
  int get omm446Squelch => _omm446Squelch;
  String get omm446Power => _omm446Power;
  bool get isPttActive => _isPttActive;

  String get omm24MeshMode => _omm24MeshMode;
  int get omm24Channel => _omm24Channel;
  int get omm24Volume => _omm24Volume;
  int get omm24PeersCount => _omm24PeersCount;

  double get currentFrequency =>
      (_omm446Channel >= 1 && _omm446Channel <= 16)
          ? pmrFrequencies[_omm446Channel - 1]
          : 446.09375;

  String get currentCtcssLabel {
    if (_omm446Ctcss <= 0 || _omm446Ctcss >= ctcssTones.length) {
      return '00: Off (Carrier Squelch)';
    }
    return '$_omm446Ctcss (${ctcssTones[_omm446Ctcss].toStringAsFixed(1)} Hz)';
  }

  String get channelDescription {
    if (_omm446Channel == 8) {
      return 'Kanal 8: Bergrettung / Notruf / Wanderkanal';
    }
    return 'PMR446 Kanal $_omm446Channel';
  }

  OmmIntercomService() {
    load();
  }

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _omm446Mode = prefs.getString(prefOmm446Mode) ?? 'analog';
    _omm446Channel = prefs.getInt(prefOmm446Channel) ?? 8;
    _omm446Ctcss = prefs.getInt(prefOmm446Ctcss) ?? 16;
    _omm446ColorCode = prefs.getInt(prefOmm446ColorCode) ?? 1;
    _omm446Squelch = prefs.getInt(prefOmm446Squelch) ?? 3;
    _omm446Power = prefs.getString(prefOmm446Power) ?? 'high';

    _omm24MeshMode = prefs.getString(prefOmm24MeshMode) ?? 'open';
    _omm24Channel = prefs.getInt(prefOmm24Channel) ?? 1;
    _omm24Volume = prefs.getInt(prefOmm24Volume) ?? 80;
    notifyListeners();
  }

  Future<void> setOmm446Mode(String mode, {BleBridgeService? ble}) async {
    _omm446Mode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(prefOmm446Mode, mode);
    _syncToBle(ble);
  }

  Future<void> setOmm446Channel(int ch, {BleBridgeService? ble}) async {
    if (ch < 1) ch = 1;
    if (ch > 16) ch = 16;
    _omm446Channel = ch;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm446Channel, ch);
    _syncToBle(ble);
  }

  Future<void> setOmm446Ctcss(int ctcss, {BleBridgeService? ble}) async {
    if (ctcss < 0) ctcss = 0;
    if (ctcss > 38) ctcss = 38;
    _omm446Ctcss = ctcss;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm446Ctcss, ctcss);
    _syncToBle(ble);
  }

  Future<void> setOmm446ColorCode(int cc, {BleBridgeService? ble}) async {
    if (cc < 1) cc = 1;
    if (cc > 16) cc = 16;
    _omm446ColorCode = cc;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm446ColorCode, cc);
    _syncToBle(ble);
  }

  Future<void> setOmm446Squelch(int sq, {BleBridgeService? ble}) async {
    if (sq < 1) sq = 1;
    if (sq > 8) sq = 8;
    _omm446Squelch = sq;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm446Squelch, sq);
    _syncToBle(ble);
  }

  Future<void> setOmm446Power(String pwr, {BleBridgeService? ble}) async {
    _omm446Power = pwr;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(prefOmm446Power, pwr);
    _syncToBle(ble);
  }

  void setPtt(bool active, {BleBridgeService? ble}) {
    _isPttActive = active;
    notifyListeners();
    if (ble != null && ble.isConnected) {
      // Opcode 0x44: Direct PTT transmit state
      ble.sendControlCommand([0x44, active ? 0x01 : 0x00]);
    }
  }

  Future<void> setOmm24MeshMode(String mode, {BleBridgeService? ble}) async {
    _omm24MeshMode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(prefOmm24MeshMode, mode);
    _syncToBle(ble);
  }

  Future<void> setOmm24Channel(int ch, {BleBridgeService? ble}) async {
    if (ch < 1) ch = 1;
    if (ch > 16) ch = 16;
    _omm24Channel = ch;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm24Channel, ch);
    _syncToBle(ble);
  }

  Future<void> setOmm24Volume(int vol, {BleBridgeService? ble}) async {
    if (vol < 0) vol = 0;
    if (vol > 100) vol = 100;
    _omm24Volume = vol;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(prefOmm24Volume, vol);
    _syncToBle(ble);
  }

  void setOmm24PeersCount(int count) {
    if (count < 0) count = 0;
    _omm24PeersCount = count;
    notifyListeners();
  }

  void _syncToBle(BleBridgeService? ble) {
    if (ble == null || !ble.isConnected) return;
    try {
      final jsonPayload = jsonEncode({
        'omm446_mode': _omm446Mode,
        'omm446_ch': _omm446Channel,
        'omm446_freq': currentFrequency,
        'omm446_ctcss': _omm446Ctcss,
        'omm446_color_code': _omm446ColorCode,
        'omm446_sq': _omm446Squelch,
        'omm446_power': _omm446Power,
        'omm24_mode': _omm24MeshMode,
        'omm24_ch': _omm24Channel,
        'omm24_vol': _omm24Volume,
      });
      final bytes = utf8.encode(jsonPayload);
      final len = bytes.length;
      final packet = <int>[
        0x43, // Opcode 0x43: OMM Radio & Mesh Hub Sync
        (len >> 8) & 0xFF,
        len & 0xFF,
        ...bytes,
      ];
      ble.sendControlCommand(packet);
    } catch (e) {
      debugPrint('Failed to sync OMM config over BLE: $e');
    }
  }
}
