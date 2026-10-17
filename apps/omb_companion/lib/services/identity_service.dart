import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'ble_bridge_service.dart';

class IdentityService extends ChangeNotifier {
  static const String prefBikeName = 'omb_bike_name';
  static const String prefBikeClass = 'omb_bike_class';
  static const String prefRiderName = 'omb_rider_name';
  static const String prefPillionName = 'omb_pillion_name';
  static const String prefPillionPresent = 'omb_pillion_present';

  String _bikeName = 'Harley Street Glide 117';
  String _bikeClass = 'cruiser';
  String _riderName = 'Michael';
  String _pillionName = 'Sarah';
  bool _isPillionPresent = false;

  final String nodeIdHex = '0x4A';
  final String bikeUid = '0x014F2A9012008C';

  String get bikeName => _bikeName;
  String get bikeClass => _bikeClass;
  String get riderName => _riderName;
  String get pillionName => _pillionName;
  bool get isPillionPresent => _isPillionPresent;

  String get swarmPreviewText {
    if (_isPillionPresent) {
      return '[$nodeIdHex] "$_riderName" & "$_pillionName" @ $_bikeName · Duo (Fahrer + Sozius aktiv)';
    } else {
      return '[$nodeIdHex] "$_riderName" @ $_bikeName · Solo (Nur Fahrer aktiv)';
    }
  }

  IdentityService() {
    load();
  }

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _bikeName = prefs.getString(prefBikeName) ?? 'Harley Street Glide 117';
    _bikeClass = prefs.getString(prefBikeClass) ?? 'cruiser';
    _riderName = prefs.getString(prefRiderName) ?? 'Michael';
    _pillionName = prefs.getString(prefPillionName) ?? 'Sarah';
    _isPillionPresent = prefs.getBool(prefPillionPresent) ?? false;
    notifyListeners();
  }

  Future<void> save({
    String? bikeName,
    String? bikeClass,
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
