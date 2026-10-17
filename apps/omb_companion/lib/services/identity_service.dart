import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'ble_bridge_service.dart';

class IdentityService extends ChangeNotifier {
  static const String prefBikeName = 'omb_bike_name';
  static const String prefBikeClass = 'omb_bike_class';
  static const String prefPacingProfile = 'omb_pacing_profile';
  static const String prefDoubtTimerSec = 'omb_doubt_timer_sec';
  static const String prefRiderName = 'omb_rider_name';
  static const String prefPillionName = 'omb_pillion_name';
  static const String prefPillionPresent = 'omb_pillion_present';

  String _bikeName = 'Harley Road Glide ST CVO';
  String _bikeClass = 'cruiser';
  String _pacingProfile = 'fast_duo'; // fast_duo, dynamic_tour, group_standard, cruising_large_group, custom
  int _doubtTimerSec = 15;
  String _riderName = 'Michael';
  String _pillionName = 'Sarah';
  bool _isPillionPresent = false;

  final String nodeIdHex = '0x4A';
  final String bikeUid = '0x014F2A9012008C';

  String get bikeName => _bikeName;
  String get bikeClass => _bikeClass;
  String get pacingProfile => _pacingProfile;
  int get doubtTimerSec => _doubtTimerSec;
  String get riderName => _riderName;
  String get pillionName => _pillionName;
  bool get isPillionPresent => _isPillionPresent;

  String get pacingProfileLabel {
    switch (_pacingProfile) {
      case 'fast_duo':
        return 'Duo Flott (15s)';
      case 'dynamic_tour':
        return 'Dynamische Tour (25s)';
      case 'group_standard':
        return 'Standard Gruppe (35s)';
      case 'cruising_large_group':
        return 'Gemütlich / Kolonne (50s)';
      case 'custom':
        return 'Custom (${_doubtTimerSec}s)';
      default:
        return '$_doubtTimerSec s';
    }
  }

  String get swarmPreviewText {
    final mode = _isPillionPresent ? 'Duo' : 'Solo';
    final crew = _isPillionPresent ? '"$_riderName" & "$_pillionName"' : '"$_riderName"';
    return '[$nodeIdHex] $crew @ $_bikeName · $mode · Pacing: $pacingProfileLabel';
  }

  IdentityService() {
    load();
  }

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _bikeName = prefs.getString(prefBikeName) ?? 'Harley Road Glide ST CVO';
    _bikeClass = prefs.getString(prefBikeClass) ?? 'cruiser';
    _pacingProfile = prefs.getString(prefPacingProfile) ?? 'fast_duo';
    _doubtTimerSec = prefs.getInt(prefDoubtTimerSec) ?? 15;
    _riderName = prefs.getString(prefRiderName) ?? 'Michael';
    _pillionName = prefs.getString(prefPillionName) ?? 'Sarah';
    _isPillionPresent = prefs.getBool(prefPillionPresent) ?? false;
    notifyListeners();
  }

  Future<void> save({
    String? bikeName,
    String? bikeClass,
    String? pacingProfile,
    int? doubtTimerSec,
    String? riderName,
    String? pillionName,
    bool? isPillionPresent,
    BleBridgeService? ble,
  }) async {
    final prefs = await SharedPreferences.getInstance();

    if (bikeName != null) {
      _bikeName = bikeName.trim().isEmpty ? 'Motorrad' : bikeName.trim();
      await prefs.setString(prefBikeName, _bikeName);
    }
    if (bikeClass != null) {
      _bikeClass = bikeClass;
      await prefs.setString(prefBikeClass, _bikeClass);
    }
    if (pacingProfile != null) {
      _pacingProfile = pacingProfile;
      await prefs.setString(prefPacingProfile, _pacingProfile);
      
      // Auto-assign doubt timer preset if not custom
      if (_pacingProfile == 'fast_duo') {
        _doubtTimerSec = 15;
      } else if (_pacingProfile == 'dynamic_tour') {
        _doubtTimerSec = 25;
      } else if (_pacingProfile == 'group_standard') {
        _doubtTimerSec = 35;
      } else if (_pacingProfile == 'cruising_large_group') {
        _doubtTimerSec = 50;
      }
      await prefs.setInt(prefDoubtTimerSec, _doubtTimerSec);
    }
    if (doubtTimerSec != null) {
      _doubtTimerSec = doubtTimerSec;
      await prefs.setInt(prefDoubtTimerSec, _doubtTimerSec);
    }
    if (riderName != null) {
      _riderName = riderName.trim().isEmpty ? 'Fahrer' : riderName.trim();
      await prefs.setString(prefRiderName, _riderName);
    }
    if (pillionName != null) {
      _pillionName = pillionName.trim().isEmpty ? 'Sozius' : pillionName.trim();
      await prefs.setString(prefPillionName, _pillionName);
    }
    if (isPillionPresent != null) {
      _isPillionPresent = isPillionPresent;
      await prefs.setBool(prefPillionPresent, _isPillionPresent);
    }

    notifyListeners();

    // Sync to Central Box via BLE if connected
    if (ble != null && ble.isConnected) {
      await syncToCentralBox(ble);
    }
  }

  Future<void> togglePillionPresence({BleBridgeService? ble}) async {
    await save(isPillionPresent: !_isPillionPresent, ble: ble);
  }

  /// Sends identity frame over BLE GATT Control Characteristic (Opcode 0x42: IDENT_SYNC)
  Future<bool> syncToCentralBox(BleBridgeService ble) async {
    if (!ble.isConnected) return false;

    try {
      final payload = {
        'bike_name': _bikeName,
        'bike_class': _bikeClass,
        'pacing_profile': _pacingProfile,
        'doubt_timer_sec': _doubtTimerSec,
        'rider_name': _riderName,
        'pillion_name': _pillionName,
        'pillion_present': _isPillionPresent,
      };
      final jsonBytes = utf8.encode(jsonEncode(payload));

      // Packet: [0x42, length_high, length_low, ...jsonBytes]
      final packet = <int>[
        0x42,
        (jsonBytes.length >> 8) & 0xFF,
        jsonBytes.length & 0xFF,
        ...jsonBytes,
      ];

      return await ble.sendControlCommand(packet);
    } catch (e) {
      debugPrint('Identity sync error: $e');
      return false;
    }
  }
}
