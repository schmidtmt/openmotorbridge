import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:open_filex/open_filex.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UpdateInfo {
  final String version;
  final String downloadUrl;
  final String releaseNotes;
  final bool isNewer;

  UpdateInfo({
    required this.version,
    required this.downloadUrl,
    required this.releaseNotes,
    required this.isNewer,
  });
}

class UpdateService extends ChangeNotifier {
  static const String prefCustomUrlKey = 'omb_update_custom_url';
  static const String defaultGithubRepo = 'schmidtmt/openmotorbridge';
  static const MethodChannel _channel = MethodChannel('bar.f0o.omb/updater');

  bool _isChecking = false;
  bool _isDownloading = false;
  double _downloadProgress = 0.0;
  String _statusMessage = '';
  UpdateInfo? _availableUpdate;
  String _currentVersion = '1.0.0';

  bool get isChecking => _isChecking;
  bool get isDownloading => _isDownloading;
  double get downloadProgress => _downloadProgress;
  String get statusMessage => _statusMessage;
  UpdateInfo? get availableUpdate => _availableUpdate;
  String get currentVersion => _currentVersion;

  UpdateService() {
    _initVersion();
  }

  Future<void> _initVersion() async {
    try {
      final info = await PackageInfo.fromPlatform();
      _currentVersion = info.version;
      notifyListeners();
    } catch (_) {}
  }

  Future<String> getCustomServerUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(prefCustomUrlKey) ?? '';
  }

  Future<void> setCustomServerUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(prefCustomUrlKey, url.trim());
    notifyListeners();
  }

  /// Checks for an update either from a custom server URL or GitHub Releases
  Future<UpdateInfo?> checkForUpdate() async {
    _isChecking = true;
    _statusMessage = 'Prüfe auf Updates...';
    notifyListeners();

    try {
      final customUrl = await getCustomServerUrl();

      if (customUrl.isNotEmpty) {
        // Mode A: Custom Local Server (JSON metadata or direct APK)
        _availableUpdate = await _checkCustomServer(customUrl);
      } else {
        // Mode B: GitHub Releases API
        _availableUpdate = await _checkGithubReleases();
      }

      _statusMessage = _availableUpdate != null && _availableUpdate!.isNewer
          ? 'Neues Update v${_availableUpdate!.version} verfügbar!'
          : 'App ist auf dem neuesten Stand (v$_currentVersion)';
    } catch (e) {
      _statusMessage = 'Update-Prüfung fehlgeschlagen: $e';
      _availableUpdate = null;
    } finally {
      _isChecking = false;
      notifyListeners();
    }

    return _availableUpdate;
  }

  Future<UpdateInfo?> _checkGithubReleases() async {
    final url = Uri.parse('https://api.github.com/repos/$defaultGithubRepo/releases/latest');
    final response = await http.get(url, headers: {'Accept': 'application/vnd.github.v3+json'});

    if (response.statusCode != 200) {
      throw 'GitHub API Fehler: ${response.statusCode}';
    }

    final data = json.decode(response.body);
    final tagName = (data['tag_name'] as String? ?? '').replaceFirst('v', '');
    final notes = data['body'] as String? ?? 'Keine Release Notes vorhanden.';

    String? apkDownloadUrl;
    final assets = data['assets'] as List<dynamic>? ?? [];
    for (final asset in assets) {
      final name = asset['name'] as String? ?? '';
      if (name.endsWith('.apk')) {
        apkDownloadUrl = asset['browser_download_url'] as String?;
        break;
      }
    }

    if (apkDownloadUrl == null) {
      throw 'Keine .apk Datei im neuesten GitHub Release gefunden.';
    }

    final isNewer = _isVersionNewer(tagName, _currentVersion);
    return UpdateInfo(
      version: tagName,
      downloadUrl: apkDownloadUrl,
      releaseNotes: notes,
      isNewer: isNewer,
    );
  }

  Future<UpdateInfo?> _checkCustomServer(String serverUrl) async {
    // If user provided a direct URL to a JSON metadata file:
    // { "version": "1.0.2", "url": "http://.../app-release.apk", "notes": "..." }
    if (serverUrl.endsWith('.json')) {
      final response = await http.get(Uri.parse(serverUrl));
      if (response.statusCode != 200) throw 'Server meldet HTTP ${response.statusCode}';
      final data = json.decode(response.body);
      final remoteVer = (data['version'] as String? ?? '').replaceFirst('v', '');
      final apkUrl = data['url'] as String? ?? '';
      final notes = data['notes'] as String? ?? '';
      return UpdateInfo(
        version: remoteVer,
        downloadUrl: apkUrl,
        releaseNotes: notes,
        isNewer: _isVersionNewer(remoteVer, _currentVersion),
      );
    } else {
      // Direct APK URL
      return UpdateInfo(
        version: 'neu',
        downloadUrl: serverUrl,
        releaseNotes: 'Direkter Download vom lokalen Server.',
        isNewer: true,
      );
    }
  }

  /// Downloads the APK with progress and prompts installation
  Future<bool> downloadAndInstall(String downloadUrl) async {
    _isDownloading = true;
    _downloadProgress = 0.0;
    _statusMessage = 'Lade Update herunter...';
    notifyListeners();

    try {
      final client = http.Client();
      final request = http.Request('GET', Uri.parse(downloadUrl));
      final response = await client.send(request);

      if (response.statusCode != 200) {
        throw 'Download fehlgeschlagen (HTTP ${response.statusCode})';
      }

      final contentLength = response.contentLength ?? 0;
      final tempDir = await getTemporaryDirectory();
      final filePath = '${tempDir.path}/openmotorbridge-update.apk';
      final file = File(filePath);
      if (await file.exists()) {
        await file.delete();
      }

      final sink = file.openWrite();
      var received = 0;

      await for (final chunk in response.stream) {
        sink.add(chunk);
        received += chunk.length;
        if (contentLength > 0) {
          _downloadProgress = received / contentLength;
          notifyListeners();
        }
      }

      await sink.flush();
      await sink.close();

      _statusMessage = 'Starte Installation...';
      _downloadProgress = 1.0;
      notifyListeners();

      // Trigger Installation via Native Android Channel (fallback to OpenFilex)
      if (Platform.isAndroid) {
        try {
          await _channel.invokeMethod('installApk', {'filePath': filePath});
          return true;
        } catch (_) {
          final res = await OpenFilex.open(filePath, type: 'application/vnd.android.package-archive');
          return res.type == ResultType.done;
        }
      } else {
        final res = await OpenFilex.open(filePath);
        return res.type == ResultType.done;
      }
    } catch (e) {
      _statusMessage = 'Download/Installationsfehler: $e';
      return false;
    } finally {
      _isDownloading = false;
      notifyListeners();
    }
  }

  bool _isVersionNewer(String remote, String current) {
    if (remote.isEmpty) return false;
    try {
      final rParts = remote.split('.').map((e) => int.tryParse(e) ?? 0).toList();
      final cParts = current.split('.').map((e) => int.tryParse(e) ?? 0).toList();
      for (var i = 0; i < 3; i++) {
        final r = i < rParts.length ? rParts[i] : 0;
        final c = i < cParts.length ? cParts[i] : 0;
        if (r > c) return true;
        if (r < c) return false;
      }
      return false;
    } catch (_) {
      return remote != current;
    }
  }
}
