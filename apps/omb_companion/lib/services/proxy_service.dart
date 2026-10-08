import 'dart:async';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class ProxyStatus {
  final bool isRunning;
  final bool boundToCellular;
  final int bytesRx;
  final int bytesTx;
  final int activeConnections;
  final int port;

  ProxyStatus({
    required this.isRunning,
    required this.boundToCellular,
    required this.bytesRx,
    required this.bytesTx,
    required this.activeConnections,
    required this.port,
  });

  factory ProxyStatus.idle([int port = 8080]) => ProxyStatus(
        isRunning: false,
        boundToCellular: false,
        bytesRx: 0,
        bytesTx: 0,
        activeConnections: 0,
        port: port,
      );
}

class ProxyService extends ChangeNotifier {
  static const MethodChannel _channel = MethodChannel('bar.f0o.omb/proxy');

  ProxyStatus _status = ProxyStatus.idle();
  Timer? _pollTimer;
  int _port = 8080;

  ProxyStatus get status => _status;
  bool get isRunning => _status.isRunning;
  bool get isBoundToCellular => _status.boundToCellular;
  int get port => _port;

  ProxyService() {
    _startPolling();
  }

  @override
  void dispose() {
    _pollTimer?.cancel();
    super.dispose();
  }

  void _startPolling() {
    _pollTimer?.cancel();
    _pollTimer = Timer.periodic(const Duration(seconds: 2), (_) => refreshStatus());
    refreshStatus();
  }

  Future<void> refreshStatus() async {
    if (!Platform.isAndroid) return;
    try {
      final res = await _channel.invokeMethod<Map<dynamic, dynamic>>('getProxyStatus');
      if (res != null) {
        _status = ProxyStatus(
          isRunning: res['running'] as bool? ?? false,
          boundToCellular: res['boundToCellular'] as bool? ?? false,
          bytesRx: (res['bytesRx'] as num? ?? 0).toInt(),
          bytesTx: (res['bytesTx'] as num? ?? 0).toInt(),
          activeConnections: (res['activeConnections'] as num? ?? 0).toInt(),
          port: _port,
        );
        notifyListeners();
      }
    } catch (_) {}
  }

  Future<bool> startProxy([int? customPort]) async {
    if (!Platform.isAndroid) {
      // iOS / desktop stub
      _status = ProxyStatus(
        isRunning: true,
        boundToCellular: true,
        bytesRx: 1024,
        bytesTx: 2048,
        activeConnections: 1,
        port: customPort ?? _port,
      );
      notifyListeners();
      return true;
    }

    if (customPort != null) _port = customPort;
    try {
      final success = await _channel.invokeMethod<bool>('startProxy', {'port': _port}) ?? false;
      await Future.delayed(const Duration(milliseconds: 300));
      await refreshStatus();
      return success;
    } catch (e) {
      debugPrint('Error starting proxy: $e');
      return false;
    }
  }

  Future<bool> stopProxy() async {
    if (!Platform.isAndroid) {
      _status = ProxyStatus.idle(_port);
      notifyListeners();
      return true;
    }

    try {
      final success = await _channel.invokeMethod<bool>('stopProxy') ?? false;
      await Future.delayed(const Duration(milliseconds: 300));
      await refreshStatus();
      return success;
    } catch (e) {
      debugPrint('Error stopping proxy: $e');
      return false;
    }
  }

  String formatBytes(int bytes) {
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(2)} MB';
  }
}
