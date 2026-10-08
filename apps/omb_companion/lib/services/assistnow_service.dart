import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class AssistNowService extends ChangeNotifier {
  // Free public or configured u-blox AssistNow token
  static const String defaultToken = 'p1rQkK2J0USx_11x8pPzWw'; // Evaluation token
  bool _isFetching = false;
  DateTime? _lastInjection;
  int _lastPacketSizeBytes = 0;
  String _status = 'Bereit';

  bool get isFetching => _isFetching;
  DateTime? get lastInjection => _lastInjection;
  int get lastPacketSizeBytes => _lastPacketSizeBytes;
  String get status => _status;

  /// Fetches the AssistNow Online MGA packet (~3-8 kB) via cellular connection
  Future<Uint8List?> fetchMGAData({
    String token = defaultToken,
    double? approxLat,
    double? approxLon,
  }) async {
    _isFetching = true;
    _status = 'Lade u-blox AssistNow Online Daten...';
    notifyListeners();

    try {
      final queryParams = <String, String>{
        'token': token,
        'gnss': 'gps,gal,glo,bds',
        'datatype': 'eph,alm,aux,pos',
      };

      if (approxLat != null && approxLon != null) {
        queryParams['lat'] = approxLat.toStringAsFixed(4);
        queryParams['lon'] = approxLon.toStringAsFixed(4);
        queryParams['pacc'] = '100000'; // 100 km accuracy
      }

      final uri = Uri.https('online-live1.services.u-blox.com', '/GetOnlineData.ashx', queryParams);
      final response = await http.get(uri).timeout(const Duration(seconds: 8));

      if (response.statusCode == 200 && response.bodyBytes.isNotEmpty) {
        _lastPacketSizeBytes = response.bodyBytes.length;
        _lastInjection = DateTime.now();
        _status = 'Erfolgreich geladen ($_lastPacketSizeBytes Bytes)';
        notifyListeners();
        return response.bodyBytes;
      } else {
        _status = 'AssistNow Fehler: HTTP ${response.statusCode}';
      }
    } catch (e) {
      _status = 'AssistNow Verbindungsfehler: $e';
    } finally {
      _isFetching = false;
      notifyListeners();
    }
    return null;
  }
}
