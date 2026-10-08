import 'package:flutter/material.dart';
import 'services/assistnow_service.dart';
import 'services/ble_bridge_service.dart';
import 'services/proxy_service.dart';
import 'services/update_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const OmbCompanionApp());
}

class OmbCompanionApp extends StatelessWidget {
  const OmbCompanionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OpenMotorBridge Companion',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0B0F19),
        primaryColor: const Color(0xFF00F2FE),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00F2FE),
          secondary: Color(0xFFFF6B00),
          surface: Color(0xFF131B2E),
        ),
        cardTheme: CardThemeData(
          color: const Color(0xFF131B2E).withValues(alpha: 0.85),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(color: Colors.white.withValues(alpha: 0.08)),
          ),
        ),
        useMaterial3: true,
      ),
      home: const MainNavigationScreen(),
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final UpdateService _updateService = UpdateService();
  final ProxyService _proxyService = ProxyService();
  final BleBridgeService _bleService = BleBridgeService();
  final AssistNowService _assistNowService = AssistNowService();

  @override
  void initState() {
    super.initState();
    // Auto-check for updates silently on app startup
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _updateService.checkForUpdate();
    });
  }

  @override
  void dispose() {
    _proxyService.dispose();
    _bleService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      CockpitScreen(ble: _bleService, assistNow: _assistNowService, proxy: _proxyService),
      ProxyScreen(proxy: _proxyService),
      UpdateScreen(updater: _updateService),
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B0F19).withValues(alpha: 0.9),
        elevation: 0,
        title: Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.asset(
                'assets/images/logo.jpg',
                width: 32,
                height: 32,
                fit: BoxFit.cover,
                errorBuilder: (_, _, _) => const Icon(Icons.two_wheeler, color: Color(0xFF00F2FE), size: 24),
              ),
            ),
            const SizedBox(width: 12),
            const Text(
              'OpenMotorBridge',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, letterSpacing: 0.5),
            ),
          ],
        ),
        actions: [
          // Live BLE status chip
          ListenableBuilder(
            listenable: _bleService,
            builder: (context, _) {
              final connected = _bleService.isConnected;
              return Container(
                margin: const EdgeInsets.only(right: 16),
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                decoration: BoxDecoration(
                  color: (connected ? const Color(0xFF00E676) : Colors.orangeAccent).withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: (connected ? const Color(0xFF00E676) : Colors.orangeAccent).withValues(alpha: 0.4),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      connected ? Icons.bluetooth_connected : Icons.bluetooth_searching,
                      size: 14,
                      color: connected ? const Color(0xFF00E676) : Colors.orangeAccent,
                    ),
                    const SizedBox(width: 6),
                    Text(
                      connected ? 'ONLINE' : 'SCAN',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: connected ? const Color(0xFF00E676) : Colors.orangeAccent,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
      body: screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        backgroundColor: const Color(0xFF0E1422),
        indicatorColor: const Color(0xFF00F2FE).withValues(alpha: 0.2),
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.speed),
            selectedIcon: Icon(Icons.speed, color: Color(0xFF00F2FE)),
            label: 'Cockpit',
          ),
          NavigationDestination(
            icon: Icon(Icons.cell_tower),
            selectedIcon: Icon(Icons.cell_tower, color: Color(0xFF00F2FE)),
            label: 'Mobilfunk-Proxy',
          ),
          NavigationDestination(
            icon: Icon(Icons.system_update_alt),
            selectedIcon: Icon(Icons.system_update_alt, color: Color(0xFF00F2FE)),
            label: 'Self-Update',
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// 1. Cockpit & Telemetry Screen
// ---------------------------------------------------------------------------
class CockpitScreen extends StatelessWidget {
  final BleBridgeService ble;
  final AssistNowService assistNow;
  final ProxyService proxy;

  const CockpitScreen({
    super.key,
    required this.ble,
    required this.assistNow,
    required this.proxy,
  });

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: Listenable.merge([ble, assistNow, proxy]),
      builder: (context, _) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Connection Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Motorrad-Verbindung (BLE)',
                            style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                          ),
                          if (ble.state == BleState.scanning)
                            const SizedBox(
                              width: 16,
                              height: 16,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        ble.statusText,
                        style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 13),
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                              foregroundColor: const Color(0xFF00F2FE),
                            ),
                            onPressed: () {
                              if (ble.isConnected) {
                                ble.disconnect();
                              } else {
                                ble.startScan();
                              }
                            },
                            icon: Icon(ble.isConnected ? Icons.link_off : Icons.search),
                            label: Text(ble.isConnected ? 'Trennen' : 'Scan starten'),
                          ),
                        ],
                      ),
                      if (ble.scanResults.isNotEmpty && !ble.isConnected) ...[
                        const Divider(height: 24),
                        const Text('Gefundene Geräte:', style: TextStyle(fontSize: 12, color: Colors.grey)),
                        const SizedBox(height: 6),
                        ...ble.scanResults.map((r) => ListTile(
                              dense: true,
                              contentPadding: EdgeInsets.zero,
                              leading: const Icon(Icons.bluetooth, color: Color(0xFF00F2FE)),
                              title: Text(r.device.platformName.isEmpty ? 'OMB-CENTRAL' : r.device.platformName),
                              subtitle: Text(r.device.remoteId.str, style: const TextStyle(fontSize: 11)),
                              trailing: ElevatedButton(
                                onPressed: () => ble.connectToDevice(r.device),
                                child: const Text('Verbinden'),
                              ),
                            )),
                      ],
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // Live Telemetry Grid
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                childAspectRatio: 1.4,
                children: [
                  _metricTile(
                    title: 'Bordnetz / Batterie',
                    value: '${ble.batteryVoltage.toStringAsFixed(1)} V',
                    icon: Icons.battery_charging_full,
                    color: ble.batteryVoltage > 12.2 ? const Color(0xFF00E676) : Colors.orangeAccent,
                    subtext: ble.ignitionOn ? 'Zündung EIN (KL15)' : 'Standby',
                  ),
                  _metricTile(
                    title: 'Schräglage (IMU)',
                    value: '${ble.leanAngle.abs().toStringAsFixed(1)}°',
                    icon: Icons.screen_rotation,
                    color: const Color(0xFF00F2FE),
                    subtext: ble.leanAngle < 0 ? 'Linksneigung' : 'Rechtsneigung',
                  ),
                  _metricTile(
                    title: 'Radar 2.0 (77 GHz)',
                    value: ble.radarAlertLevel == 0
                        ? 'FREI'
                        : (ble.radarAlertLevel == 1 ? 'ANNÄHERUNG' : 'WARNUNG!'),
                    icon: Icons.radar,
                    color: ble.radarAlertLevel == 0
                        ? const Color(0xFF00E676)
                        : (ble.radarAlertLevel == 1 ? Colors.orangeAccent : Colors.redAccent),
                    subtext: 'Heck-Transceiver',
                  ),
                  _metricTile(
                    title: 'Mobilfunk-Proxy',
                    value: proxy.isRunning ? 'AKTIV' : 'STANDBY',
                    icon: Icons.cell_tower,
                    color: proxy.isRunning ? const Color(0xFF00F2FE) : Colors.grey,
                    subtext: 'Port ${proxy.port} (Cellular)',
                  ),
                ],
              ),

              const SizedBox(height: 16),

              // A-GPS Instant Fix Injection Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.gps_fixed, color: Color(0xFF00F2FE)),
                          const SizedBox(width: 8),
                          const Text(
                            'u-blox AssistNow A-GPS Instant-Fix',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Lädt u-blox MGA-Ephemeriden (~3-8 kB) über Mobilfunk und speist sie via BLE in den SAM-M10Q GNSS-Chip ein. TTFF sinkt von ~30s auf < 1.5s!',
                        style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'Status: ${assistNow.status}',
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 12),
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                          foregroundColor: const Color(0xFF00F2FE),
                        ),
                        onPressed: assistNow.isFetching
                            ? null
                            : () async {
                                final data = await assistNow.fetchMGAData();
                                if (data != null && ble.isConnected) {
                                  await ble.injectAssistNowData(data);
                                }
                              },
                        icon: assistNow.isFetching
                            ? const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2))
                            : const Icon(Icons.bolt),
                        label: const Text('Jetzt MGA-Daten laden & injizieren'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _metricTile({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
    required String subtext,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(title, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                Icon(icon, size: 16, color: color),
              ],
            ),
            Text(value, style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold, color: color)),
            Text(subtext, style: TextStyle(fontSize: 10, color: Colors.white.withValues(alpha: 0.5))),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// 2. Mobilfunk-Proxy Screen (Layer-5 SOCKS5/HTTP without VPN conflict)
// ---------------------------------------------------------------------------
class ProxyScreen extends StatelessWidget {
  final ProxyService proxy;

  const ProxyScreen({super.key, required this.proxy});

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: proxy,
      builder: (context, _) {
        final isRunning = proxy.isRunning;
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Main Control Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              Icon(
                                Icons.cell_tower,
                                color: isRunning ? const Color(0xFF00F2FE) : Colors.grey,
                                size: 28,
                              ),
                              const SizedBox(width: 12),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'Mobilfunk-Proxy (SOCKS5/HTTP)',
                                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                  ),
                                  Text(
                                    isRunning ? 'Aktiv auf 127.0.0.1:${proxy.port}' : 'Gestoppt',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: isRunning ? const Color(0xFF00E676) : Colors.grey,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          Switch(
                            value: isRunning,
                            activeThumbColor: const Color(0xFF00F2FE),
                            onChanged: (val) {
                              if (val) {
                                proxy.startProxy();
                              } else {
                                proxy.stopProxy();
                              }
                            },
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      // Architectural Badge: Tailscale / Zero VPN Conflict
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF00E676).withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: const Color(0xFF00E676).withValues(alpha: 0.3)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.verified_user, color: Color(0xFF00E676), size: 20),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                'Kein VpnService-Slot belegt: Parallel laufende VPNs (Tailscale / Homesphere / WireGuard) bleiben 100% aktiv!',
                                style: TextStyle(color: Colors.white.withValues(alpha: 0.9), fontSize: 11),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFF00F2FE).withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.wifi_off, color: Color(0xFF00F2FE), size: 20),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                'Bypasst das 5 GHz WLAN von Wireless CarPlay / Android Auto und routet Datenpakete der Zentralbox direkt über 4G/5G Mobilfunk.',
                                style: TextStyle(color: Colors.white.withValues(alpha: 0.8), fontSize: 11),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // Traffic Statistics Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Verkehrs- & Routing-Statistik', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _statItem(
                            label: 'Empfangen (RX)',
                            value: proxy.formatBytes(proxy.status.bytesRx),
                            icon: Icons.arrow_downward,
                            color: const Color(0xFF00E676),
                          ),
                          _statItem(
                            label: 'Gesendet (TX)',
                            value: proxy.formatBytes(proxy.status.bytesTx),
                            icon: Icons.arrow_upward,
                            color: const Color(0xFF00F2FE),
                          ),
                          _statItem(
                            label: 'Verbindungen',
                            value: '${proxy.status.activeConnections}',
                            icon: Icons.sync_alt,
                            color: const Color(0xFFFF6B00),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _statItem({required String label, required String value, required IconData icon, required Color color}) {
    return Column(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(height: 6),
        Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color)),
        const SizedBox(height: 2),
        Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// 3. In-App Self-Update Screen (GitHub Releases & Local Server)
// ---------------------------------------------------------------------------
class UpdateScreen extends StatefulWidget {
  final UpdateService updater;

  const UpdateScreen({super.key, required this.updater});

  @override
  State<UpdateScreen> createState() => _UpdateScreenState();
}

class _UpdateScreenState extends State<UpdateScreen> {
  final TextEditingController _urlCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCustomUrl();
  }

  Future<void> _loadCustomUrl() async {
    final url = await widget.updater.getCustomServerUrl();
    _urlCtrl.text = url;
  }

  @override
  void dispose() {
    _urlCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: widget.updater,
      builder: (context, _) {
        final info = widget.updater.availableUpdate;
        final isDownloading = widget.updater.isDownloading;

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Version Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.asset(
                          'assets/images/logo.jpg',
                          width: 48,
                          height: 48,
                          fit: BoxFit.cover,
                          errorBuilder: (_, _, _) => const Icon(Icons.install_mobile, color: Color(0xFF00F2FE), size: 32),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('Installierte App-Version', style: TextStyle(color: Colors.grey, fontSize: 12)),
                          Text(
                            'v${widget.updater.currentVersion}',
                            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            widget.updater.statusMessage,
                            style: TextStyle(
                              fontSize: 11,
                              color: info?.isNewer == true ? const Color(0xFF00E676) : Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // Available Update Banner
              if (info != null && info.isNewer) ...[
                Card(
                  color: const Color(0xFF00E676).withValues(alpha: 0.12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                    side: const BorderSide(color: Color(0xFF00E676)),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.new_releases, color: Color(0xFF00E676)),
                            const SizedBox(width: 8),
                            Text(
                              'Neues Update verfügbar: v${info.version}',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF00E676)),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(info.releaseNotes, style: const TextStyle(fontSize: 12, color: Colors.white70)),
                        const SizedBox(height: 16),
                        if (isDownloading) ...[
                          LinearProgressIndicator(
                            value: widget.updater.downloadProgress > 0 ? widget.updater.downloadProgress : null,
                            color: const Color(0xFF00E676),
                            backgroundColor: Colors.white12,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            '${(widget.updater.downloadProgress * 100).toStringAsFixed(0)} % heruntergeladen',
                            style: const TextStyle(fontSize: 11, color: Colors.grey),
                          ),
                        ] else ...[
                          ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0xFF00E676),
                              foregroundColor: Colors.black,
                              minimumSize: const Size.fromHeight(44),
                            ),
                            onPressed: () => widget.updater.downloadAndInstall(info.downloadUrl),
                            icon: const Icon(Icons.download),
                            label: const Text('Herunterladen & Jetzt Installieren', style: TextStyle(fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // Server Settings Card (Custom Local Server vs. GitHub)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Update-Quelle konfigurieren', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      const SizedBox(height: 8),
                      Text(
                        'Standardmäßig prüft die App automatisch die GitHub Releases von openmotorbridge. Du kannst hier auch die URL deines lokalen Homeservers (z. B. http://192.168.1.100:8080/app.apk oder .json) hinterlegen.',
                        style: TextStyle(color: Colors.white.withValues(alpha: 0.65), fontSize: 11),
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        controller: _urlCtrl,
                        decoration: InputDecoration(
                          hintText: 'Leer lassen für GitHub Releases oder Server-URL eingeben',
                          hintStyle: const TextStyle(fontSize: 11, color: Colors.grey),
                          labelText: 'Lokaler Server URL (Optional)',
                          prefixIcon: const Icon(Icons.dns, size: 20),
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                          isDense: true,
                        ),
                        onChanged: (val) => widget.updater.setCustomServerUrl(val),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                          foregroundColor: const Color(0xFF00F2FE),
                          minimumSize: const Size.fromHeight(42),
                        ),
                        onPressed: widget.updater.isChecking ? null : () => widget.updater.checkForUpdate(),
                        icon: widget.updater.isChecking
                            ? const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2))
                            : const Icon(Icons.refresh),
                        label: const Text('Jetzt nach Updates suchen'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
