import 'package:flutter/material.dart';
import 'services/assistnow_service.dart';
import 'services/ble_bridge_service.dart';
import 'services/firmware_service.dart';
import 'services/identity_service.dart';
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
  final FirmwareService _firmwareService = FirmwareService();
  final IdentityService _identityService = IdentityService();

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
    _firmwareService.dispose();
    _identityService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      CockpitScreen(
        ble: _bleService,
        assistNow: _assistNowService,
        proxy: _proxyService,
        identity: _identityService,
        onNavigateToIdentity: () => setState(() => _currentIndex = 1),
      ),
      IdentityScreen(identity: _identityService, ble: _bleService),
      ProxyScreen(proxy: _proxyService),
      FirmwareScreen(firmware: _firmwareService, ble: _bleService),
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
            icon: Icon(Icons.badge_outlined),
            selectedIcon: Icon(Icons.badge, color: Color(0xFF00F2FE)),
            label: 'Identität',
          ),
          NavigationDestination(
            icon: Icon(Icons.cell_tower),
            selectedIcon: Icon(Icons.cell_tower, color: Color(0xFF00F2FE)),
            label: 'Mobilfunk-Proxy',
          ),
          NavigationDestination(
            icon: Icon(Icons.memory),
            selectedIcon: Icon(Icons.memory, color: Color(0xFF00F2FE)),
            label: 'Firmware-OTA',
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
  final IdentityService identity;
  final VoidCallback? onNavigateToIdentity;

  const CockpitScreen({
    super.key,
    required this.ble,
    required this.assistNow,
    required this.proxy,
    required this.identity,
    this.onNavigateToIdentity,
  });

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: Listenable.merge([ble, assistNow, proxy, identity]),
      builder: (context, _) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 0. Active Crew & Machine Summary Card
              Card(
                color: const Color(0xFF0E1422),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                  side: BorderSide(
                    color: const Color(0xFF00F2FE).withValues(alpha: 0.35),
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: Row(
                    children: [
                      const Text('🪪', style: TextStyle(fontSize: 24)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${identity.bikeName} · ${identity.riderName} (${identity.pacingProfileLabel})',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              identity.isPillionPresent
                                  ? 'Duo-Modus: Sozius (${identity.pillionName}) an Bord · Announce Aktiv'
                                  : 'Solo-Fahrt: Nur Fahrer im Schwarm announced',
                              style: TextStyle(
                                fontSize: 11,
                                color: identity.isPillionPresent ? const Color(0xFF00E676) : Colors.white70,
                              ),
                            ),
                          ],
                        ),
                      ),
                      if (onNavigateToIdentity != null)
                        TextButton.icon(
                          style: TextButton.styleFrom(
                            foregroundColor: const Color(0xFF00F2FE),
                            padding: const EdgeInsets.symmetric(horizontal: 8),
                          ),
                          onPressed: onNavigateToIdentity,
                          icon: const Icon(Icons.edit, size: 14),
                          label: const Text('Profil', style: TextStyle(fontSize: 12)),
                        ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 12),

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

              if (ble.hwLostMask != 0) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.redAccent.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.redAccent),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.warning, color: Colors.redAccent, size: 24),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Hardware-Verlust / Anomalie erkannt!',
                              style: TextStyle(fontWeight: FontWeight.bold, color: Colors.redAccent, fontSize: 13),
                            ),
                            Text(
                              'NVS-Baseline Abweichung (Maske: 0x${ble.hwLostMask.toRadixString(16).toUpperCase()}). Ein Modul antwortet nicht.',
                              style: const TextStyle(fontSize: 11, color: Colors.white70),
                            ),
                          ],
                        ),
                      ),
                      TextButton(
                        onPressed: () => ble.sendControlCommand([0x41, 0x03]),
                        child: const Text('Re-Scan', style: TextStyle(color: Color(0xFF00F2FE), fontSize: 11)),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // Live Telemetry Grid (6 Metrics)
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                childAspectRatio: 1.4,
                children: [
                  _metricTile(
                    title: 'Bordnetz (KL30)',
                    value: '${ble.batteryVoltage.toStringAsFixed(1)} V',
                    icon: Icons.battery_charging_full,
                    color: ble.batteryVoltage > 12.2 ? const Color(0xFF00E676) : Colors.orangeAccent,
                    subtext: ble.ignitionOn ? 'KL15: ${ble.ignitionVoltage.toStringAsFixed(1)} V' : 'Standby (Zdg AUS)',
                  ),
                  _metricTile(
                    title: 'Schräglage (IMU)',
                    value: '${ble.leanAngle.abs().toStringAsFixed(1)}°',
                    icon: Icons.screen_rotation,
                    color: const Color(0xFF00F2FE),
                    subtext: ble.leanAngle == 0 ? 'Aufrecht' : (ble.leanAngle < 0 ? 'Linksneigung' : 'Rechtsneigung'),
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
                    title: 'GNSS Fix (SAM-M10Q)',
                    value: ble.gnss3dFix ? '3D FIX' : 'SUCHE...',
                    icon: Icons.satellite_alt,
                    color: ble.gnss3dFix ? const Color(0xFF00E676) : Colors.orangeAccent,
                    subtext: 'Front-Node PCBA 05',
                  ),
                  _metricTile(
                    title: 'Keyfob / Remote',
                    value: '${ble.remoteBatPct} %',
                    icon: Icons.vpn_key,
                    color: ble.remoteBatPct > 20 ? const Color(0xFF00E676) : Colors.orangeAccent,
                    subtext: 'Smart-Beacon NVS',
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
// 1b. Fahrzeug- & Besatzungs-Identität (SSOT & Schwarm-Profil)
// ---------------------------------------------------------------------------
class IdentityScreen extends StatefulWidget {
  final IdentityService identity;
  final BleBridgeService ble;

  const IdentityScreen({
    super.key,
    required this.identity,
    required this.ble,
  });

  @override
  State<IdentityScreen> createState() => _IdentityScreenState();
}

class _IdentityScreenState extends State<IdentityScreen> {
  late TextEditingController _bikeNameCtrl;
  late TextEditingController _riderNameCtrl;
  late TextEditingController _pillionNameCtrl;
  String _pacingProfile = 'fast_duo';
  int _doubtTimerSec = 15;

  @override
  void initState() {
    super.initState();
    _bikeNameCtrl = TextEditingController(text: widget.identity.bikeName);
    _riderNameCtrl = TextEditingController(text: widget.identity.riderName);
    _pillionNameCtrl = TextEditingController(text: widget.identity.pillionName);
    _pacingProfile = widget.identity.pacingProfile;
    _doubtTimerSec = widget.identity.doubtTimerSec;
  }

  @override
  void dispose() {
    _bikeNameCtrl.dispose();
    _riderNameCtrl.dispose();
    _pillionNameCtrl.dispose();
    super.dispose();
  }

  void _saveAll() {
    widget.identity.save(
      bikeName: _bikeNameCtrl.text,
      pacingProfile: _pacingProfile,
      doubtTimerSec: _doubtTimerSec,
      riderName: _riderNameCtrl.text,
      pillionName: _pillionNameCtrl.text,
      ble: widget.ble,
    );
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        backgroundColor: const Color(0xFF131B2E),
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: Color(0xFF00E676)),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                widget.ble.isConnected
                    ? 'Identität auf Zentralbox gesichert & synchron!'
                    : 'Identität lokal gesichert (Wird bei BLE-Connect synchronisiert)',
                style: const TextStyle(color: Colors.white, fontSize: 13),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: Listenable.merge([widget.identity, widget.ble]),
      builder: (context, _) {
        final isDuo = widget.identity.isPillionPresent;
        final bleOnline = widget.ble.isConnected;

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Card with Node ID & Status
              Card(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: const Border(
                      left: BorderSide(color: Color(0xFF00F2FE), width: 4),
                    ),
                  ),
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Row(
                            children: [
                              Text('🪪', style: TextStyle(fontSize: 22)),
                              SizedBox(width: 8),
                              Text(
                                'Fahrzeug & Besatzung',
                                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: const Color(0xFF00F2FE).withValues(alpha: 0.3)),
                            ),
                            child: Text(
                              'Node: ${widget.identity.nodeIdHex}',
                              style: const TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF00F2FE),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'Hardware-gebundene Identitäten der Zentralbox (SSOT) für LoRa-Discovery, Relativ-Radar & TTS-Ansagen.',
                        style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
                      ),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          Icon(
                            bleOnline ? Icons.cloud_done : Icons.storage,
                            size: 14,
                            color: bleOnline ? const Color(0xFF00E676) : Colors.orangeAccent,
                          ),
                          const SizedBox(width: 6),
                          Text(
                            bleOnline ? 'Zentralbox NVS synchron (Live BLE)' : 'Lokaler Cache aktiv (Zentralbox Standby)',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: bleOnline ? const Color(0xFF00E676) : Colors.orangeAccent,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 1. Fahrzeug-Identität (Bike Entity)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Row(
                            children: [
                              Icon(Icons.two_wheeler, color: Color(0xFFFF6B00)),
                              SizedBox(width: 8),
                              Text(
                                'Motorrad / Fahrzeug-Identität',
                                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                              ),
                            ],
                          ),
                          Text(
                            'UID: ${widget.identity.bikeUid}',
                            style: TextStyle(fontFamily: 'monospace', fontSize: 10, color: Colors.white.withValues(alpha: 0.5)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 14),
                      TextField(
                        controller: _bikeNameCtrl,
                        decoration: InputDecoration(
                          labelText: 'Fahrzeug-Name / Bike-Alias',
                          hintText: 'z. B. Harley Road Glide ST CVO oder BMW R1250GS',
                          labelStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 13),
                          filled: true,
                          fillColor: Colors.black.withValues(alpha: 0.25),
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                          prefixIcon: const Icon(Icons.edit, size: 18),
                        ),
                        onChanged: (val) => widget.identity.save(bikeName: val, ble: widget.ble),
                      ),
                      const SizedBox(height: 12),
                      DropdownButtonFormField<String>(
                        initialValue: _pacingProfile,
                        decoration: InputDecoration(
                          labelText: 'Fahrstil & Gruppen-Dynamik (Doubt-Timer)',
                          labelStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 13),
                          filled: true,
                          fillColor: Colors.black.withValues(alpha: 0.25),
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                          prefixIcon: const Icon(Icons.timer_outlined, size: 18),
                        ),
                        dropdownColor: const Color(0xFF131B2E),
                        items: const [
                          DropdownMenuItem(value: 'fast_duo', child: Text('🏁 Duo / Flotte Truppe (Doubt-Timer: 15s)')),
                          DropdownMenuItem(value: 'dynamic_tour', child: Text('🏍️ Dynamische Tour (Doubt-Timer: 25s)')),
                          DropdownMenuItem(value: 'group_standard', child: Text('👥 Standard / Gemischte Gruppe (Doubt-Timer: 35s)')),
                          DropdownMenuItem(value: 'cruising_large_group', child: Text('☕ Gemütlich / Große Kolonne (Doubt-Timer: 50s)')),
                          DropdownMenuItem(value: 'custom', child: Text('⚙️ Benutzerdefiniert (10–90s)')),
                        ],
                        onChanged: (val) {
                          if (val != null) {
                            setState(() => _pacingProfile = val);
                            widget.identity.save(pacingProfile: val, ble: widget.ble);
                          }
                        },
                      ),
                      if (_pacingProfile == 'custom') ...[
                        const SizedBox(height: 10),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.black.withValues(alpha: 0.25),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: const Color(0xFF00F2FE).withValues(alpha: 0.2)),
                          ),
                          child: Row(
                            children: [
                              const Text('Doubt-Timer:', style: TextStyle(fontSize: 12, color: Colors.white70)),
                              const SizedBox(width: 8),
                              Text(
                                '${_doubtTimerSec}s',
                                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF00F2FE)),
                              ),
                              Expanded(
                                child: Slider(
                                  value: _doubtTimerSec.toDouble().clamp(10.0, 90.0),
                                  min: 10,
                                  max: 90,
                                  divisions: 16,
                                  activeColor: const Color(0xFF00F2FE),
                                  onChanged: (val) {
                                    final sec = val.round();
                                    setState(() => _doubtTimerSec = sec);
                                    widget.identity.save(doubtTimerSec: sec, ble: widget.ble);
                                  },
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 2. Besatzung: Fahrer & Sozius Slots
              Row(
                children: [
                  // Fahrer Slot Card
                  Expanded(
                    child: Card(
                      color: const Color(0xFF0A84FF).withValues(alpha: 0.08),
                      child: Padding(
                        padding: const EdgeInsets.all(14),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                const Row(
                                  children: [
                                    Icon(Icons.person, color: Color(0xFF00F2FE), size: 18),
                                    SizedBox(width: 6),
                                    Text('Fahrer', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF00E676).withValues(alpha: 0.15),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: const Text('🟢 Aktiv', style: TextStyle(color: Color(0xFF00E676), fontSize: 10, fontWeight: FontWeight.bold)),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            TextField(
                              controller: _riderNameCtrl,
                              decoration: InputDecoration(
                                labelText: 'Fahrer-Rufzeichen',
                                hintText: 'z. B. Michael',
                                labelStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
                                filled: true,
                                fillColor: Colors.black.withValues(alpha: 0.3),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                isDense: true,
                              ),
                              onChanged: (val) => widget.identity.save(riderName: val, ble: widget.ble),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              'Rolle: ROLE_RIDER (0x01)',
                              style: TextStyle(fontSize: 10, color: Colors.white.withValues(alpha: 0.5)),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                  const SizedBox(width: 12),

                  // Sozius Slot Card
                  Expanded(
                    child: Card(
                      color: isDuo
                          ? const Color(0xFFFF9F0A).withValues(alpha: 0.08)
                          : Colors.white.withValues(alpha: 0.02),
                      child: Padding(
                        padding: const EdgeInsets.all(14),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                const Row(
                                  children: [
                                    Icon(Icons.group, color: Color(0xFFFF9F0A), size: 18),
                                    SizedBox(width: 6),
                                    Text('Sozius', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: isDuo
                                        ? const Color(0xFF00E676).withValues(alpha: 0.15)
                                        : Colors.white.withValues(alpha: 0.06),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Text(
                                    isDuo ? '🟢 An Bord' : '⚪ Solo',
                                    style: TextStyle(
                                      color: isDuo ? const Color(0xFF00E676) : Colors.grey,
                                      fontSize: 10,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 10),
                            TextField(
                              controller: _pillionNameCtrl,
                              decoration: InputDecoration(
                                labelText: 'Sozius-Rufzeichen',
                                hintText: 'z. B. Sarah',
                                labelStyle: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
                                filled: true,
                                fillColor: Colors.black.withValues(alpha: 0.3),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                isDense: true,
                              ),
                              onChanged: (val) => widget.identity.save(pillionName: val, ble: widget.ble),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              isDuo ? 'Rolle: ROLE_PILLION (0x02)' : 'Nicht im Schwarm announced',
                              style: TextStyle(fontSize: 10, color: Colors.white.withValues(alpha: 0.5)),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              // Sozius An Bord Toggle
              Card(
                child: SwitchListTile(
                  title: const Text('Sozius fährt heute mit (An Bord)', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                  subtitle: Text(
                    isDuo
                        ? 'Duo-Modus aktiv: Sozius wird im LoRa-Schwarm announced & Audio-Share aktiv.'
                        : 'Solo-Modus: Gespeichertes Sozius-Profil wird strikt NICHT announced.',
                    style: TextStyle(fontSize: 11, color: Colors.white.withValues(alpha: 0.6)),
                  ),
                  value: isDuo,
                  activeThumbColor: const Color(0xFFFF9F0A),
                  onChanged: (val) => widget.identity.save(isPillionPresent: val, ble: widget.ble),
                ),
              ),

              const SizedBox(height: 16),

              // 3. LoRa-Schwarm Announce Vorschau (Was das Bike tatsächlich ins Netz funkt)
              Card(
                color: const Color(0xFF0E1422),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                  side: BorderSide(color: const Color(0xFF00E676).withValues(alpha: 0.4), style: BorderStyle.solid),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            '📡 Aktives LoRa Kanal 1 Schwarm-Discovery-Beacon:',
                            style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 0.5),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: const Color(0xFF00E676).withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: const Text('ETSI 18ms', style: TextStyle(color: Color(0xFF00E676), fontSize: 10, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        widget.identity.swarmPreviewText,
                        style: const TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF00E676),
                          fontFamily: 'monospace',
                        ),
                      ),
                      const SizedBox(height: 14),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                            foregroundColor: const Color(0xFF00F2FE),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                          onPressed: _saveAll,
                          icon: const Icon(Icons.save, size: 18),
                          label: const Text('Auf Zentralbox sichern & synchronisieren'),
                        ),
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

// ---------------------------------------------------------------------------
// 4. Firmware & OTA Hub Screen (ESP32-S3, OMM Intercom, Front-Node)
// ---------------------------------------------------------------------------
class FirmwareScreen extends StatefulWidget {
  final FirmwareService firmware;
  final BleBridgeService ble;

  const FirmwareScreen({
    super.key,
    required this.firmware,
    required this.ble,
  });

  @override
  State<FirmwareScreen> createState() => _FirmwareScreenState();
}

class _FirmwareScreenState extends State<FirmwareScreen> {
  final TextEditingController _serverUrlCtrl = TextEditingController();
  final ScrollController _logScrollCtrl = ScrollController();
  bool _isOfflineCached = false;
  int _cachedSizeBytes = 0;

  @override
  void initState() {
    super.initState();
    _loadServerUrl();
    _checkCacheStatus();
  }

  Future<void> _loadServerUrl() async {
    final url = await widget.firmware.getFirmwareServerUrl();
    _serverUrlCtrl.text = url;
  }

  Future<void> _checkCacheStatus() async {
    final cached = await widget.firmware.isFirmwareCached(widget.firmware.selectedTarget);
    final size = await widget.firmware.getCachedFileSize(widget.firmware.selectedTarget);
    if (mounted) {
      setState(() {
        _isOfflineCached = cached;
        _cachedSizeBytes = size;
      });
    }
  }

  @override
  void dispose() {
    _serverUrlCtrl.dispose();
    _logScrollCtrl.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_logScrollCtrl.hasClients) {
        _logScrollCtrl.animateTo(
          _logScrollCtrl.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: Listenable.merge([widget.firmware, widget.ble]),
      builder: (context, _) {
        _scrollToBottom();
        final fw = widget.firmware;
        final ble = widget.ble;
        final target = fw.selectedTarget;
        final isFlashing = fw.isFlashing;

        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Banner
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(Icons.memory, color: Color(0xFF00F2FE), size: 28),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Smart Firmware & OTA Hub',
                              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              'Direktes High-Speed Flashen via Bluetooth Low Energy ohne Browser-Timeouts.',
                              style: TextStyle(color: Colors.white.withValues(alpha: 0.65), fontSize: 11),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // BLE Warning Banner if disconnected
              if (!ble.isConnected) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.orangeAccent.withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.orangeAccent.withValues(alpha: 0.4)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.bluetooth_searching, color: Colors.orangeAccent, size: 20),
                      const SizedBox(width: 10),
                      const Expanded(
                        child: Text(
                          'Motorrad nicht über BLE verbunden. Bitte zuerst im Tab "Cockpit" mit der Central Box verbinden.',
                          style: TextStyle(fontSize: 11, color: Colors.white70),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // 1. Target Selector
              const Text('1. Zielknoten auswählen', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
              const SizedBox(height: 8),
              ...FirmwareTarget.values.map((t) {
                final isSelected = t == target;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(12),
                    onTap: isFlashing
                        ? null
                        : () {
                            fw.selectTarget(t);
                            _checkCacheStatus();
                          },
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? const Color(0xFF00F2FE).withValues(alpha: 0.12)
                            : const Color(0xFF131B2E).withValues(alpha: 0.6),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: isSelected ? const Color(0xFF00F2FE) : Colors.white12,
                          width: isSelected ? 1.5 : 1.0,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            t == FirmwareTarget.ommIntercom
                                ? Icons.headset_mic
                                : (t == FirmwareTarget.frontNode
                                    ? Icons.speed
                                    : (t == FirmwareTarget.radarSubMcu ? Icons.radar : Icons.memory)),
                            color: isSelected ? const Color(0xFF00F2FE) : Colors.grey,
                            size: 24,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      t.title,
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 13,
                                        color: isSelected ? Colors.white : Colors.white70,
                                      ),
                                    ),
                                    Text(
                                      t.defaultVersion,
                                      style: TextStyle(
                                        fontSize: 11,
                                        fontWeight: FontWeight.bold,
                                        color: isSelected ? const Color(0xFF00E676) : Colors.grey,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  t.subtitle,
                                  style: TextStyle(fontSize: 10, color: Colors.white.withValues(alpha: 0.5)),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              }),

              const SizedBox(height: 16),

              // 2. Binary Source & Offline Caching Card
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('2. Firmware-Binärdatei & Offline-Cache', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.04),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          children: [
                            Icon(
                              fw.customBinaryFile != null
                                  ? Icons.insert_drive_file
                                  : (_isOfflineCached ? Icons.check_circle : Icons.cloud_download),
                              color: fw.customBinaryFile != null
                                  ? const Color(0xFFFF6B00)
                                  : (_isOfflineCached ? const Color(0xFF00E676) : Colors.grey),
                              size: 20,
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    fw.customBinaryFile != null
                                        ? 'Manuelle Datei: ${fw.customBinaryFile!.path.split('/').last}'
                                        : (_isOfflineCached
                                            ? 'Offline im App-Speicher bereit (${(_cachedSizeBytes / 1024).toStringAsFixed(1)} kB)'
                                            : 'Nicht im Offline-Speicher (Server-Download erforderlich)'),
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                                  ),
                                  Text(
                                    fw.customBinaryFile != null
                                        ? fw.customBinaryFile!.path
                                        : 'Datei: ${target.filename}',
                                    style: TextStyle(fontSize: 10, color: Colors.white.withValues(alpha: 0.5)),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ],
                              ),
                            ),
                            if (fw.customBinaryFile != null)
                              IconButton(
                                icon: const Icon(Icons.close, size: 16, color: Colors.redAccent),
                                onPressed: () {
                                  fw.clearCustomBinary();
                                  _checkCacheStatus();
                                },
                              ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF00E676).withValues(alpha: 0.15),
                                foregroundColor: const Color(0xFF00E676),
                                padding: const EdgeInsets.symmetric(vertical: 10),
                              ),
                              onPressed: (isFlashing || fw.isDownloading)
                                  ? null
                                  : () async {
                                      final ok = await fw.downloadForOfflineUse(target);
                                      if (ok) _checkCacheStatus();
                                    },
                              icon: fw.isDownloading
                                  ? const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2))
                                  : const Icon(Icons.download_for_offline, size: 18),
                              label: const Text('Offline cachen (Garage)', style: TextStyle(fontSize: 11)),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF00F2FE).withValues(alpha: 0.15),
                                foregroundColor: const Color(0xFF00F2FE),
                                padding: const EdgeInsets.symmetric(vertical: 10),
                              ),
                              onPressed: isFlashing
                                  ? null
                                  : () async {
                                      await fw.pickCustomBinary();
                                      _checkCacheStatus();
                                    },
                              icon: const Icon(Icons.folder_open, size: 18),
                              label: const Text('Eigene .bin wählen', style: TextStyle(fontSize: 11)),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 3. Flash Execution Card
              Card(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(
                    color: isFlashing ? const Color(0xFF00F2FE) : Colors.white12,
                    width: isFlashing ? 1.5 : 1.0,
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('3. Flash- & OTA-Transfer', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                            decoration: BoxDecoration(
                              color: (isFlashing ? const Color(0xFF00F2FE) : (fw.status == OtaStatus.success ? const Color(0xFF00E676) : Colors.grey)).withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Text(
                              fw.status.name.toUpperCase(),
                              style: TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                color: isFlashing ? const Color(0xFF00F2FE) : (fw.status == OtaStatus.success ? const Color(0xFF00E676) : Colors.grey),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Text(
                        fw.statusMessage,
                        style: TextStyle(
                          fontSize: 12,
                          color: fw.status == OtaStatus.failed ? Colors.redAccent : Colors.white70,
                        ),
                      ),
                      const SizedBox(height: 12),
                      if (isFlashing || fw.progress > 0) ...[
                        LinearProgressIndicator(
                          value: fw.progress > 0 ? fw.progress : null,
                          backgroundColor: Colors.white12,
                          color: const Color(0xFF00F2FE),
                          minHeight: 8,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              '${(fw.progress * 100).toStringAsFixed(0)} % abgeschlossen',
                              style: const TextStyle(fontSize: 11, color: Colors.grey),
                            ),
                            if (fw.speedText.isNotEmpty)
                              Text(
                                fw.speedText,
                                style: const TextStyle(fontSize: 11, color: Color(0xFF00E676), fontWeight: FontWeight.bold),
                              ),
                          ],
                        ),
                        const SizedBox(height: 12),
                      ],
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: ble.isConnected
                              ? const Color(0xFF00F2FE)
                              : Colors.grey.withValues(alpha: 0.3),
                          foregroundColor: Colors.black,
                          minimumSize: const Size.fromHeight(46),
                        ),
                        onPressed: (!ble.isConnected || isFlashing)
                            ? null
                            : () => fw.startFlash(ble: ble),
                        icon: isFlashing
                            ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black))
                            : const Icon(Icons.flash_on),
                        label: Text(
                          isFlashing
                              ? 'Flashe ${target.filename}...'
                              : '⚡ Firmware auf Motorrad flashen (OTA)',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 4. Live Diagnostic Log Console
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Row(
                            children: [
                              Icon(Icons.terminal, size: 16, color: Color(0xFF00F2FE)),
                              SizedBox(width: 8),
                              Text('OTA Live-Diagnoselog', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            ],
                          ),
                          TextButton(
                            onPressed: () => fw.clearLogs(),
                            child: const Text('Leeren', style: TextStyle(fontSize: 11, color: Colors.grey)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Container(
                        height: 140,
                        width: double.infinity,
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: const Color(0xFF080C14),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: Colors.white10),
                        ),
                        child: fw.logEntries.isEmpty
                            ? const Text('Keine Protokolle vorhanden.', style: TextStyle(color: Colors.grey, fontSize: 11))
                            : ListView.builder(
                                controller: _logScrollCtrl,
                                itemCount: fw.logEntries.length,
                                itemBuilder: (context, i) {
                                  final line = fw.logEntries[i];
                                  final isErr = line.contains('FEHLER') || line.contains('Abbruch');
                                  final isOk = line.contains('✓') || line.contains('🎉');
                                  return Padding(
                                    padding: const EdgeInsets.only(bottom: 2),
                                    child: Text(
                                      line,
                                      style: TextStyle(
                                        fontFamily: 'monospace',
                                        fontSize: 10,
                                        color: isErr
                                            ? Colors.redAccent
                                            : (isOk ? const Color(0xFF00E676) : Colors.white70),
                                      ),
                                    ),
                                  );
                                },
                              ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 5. Server URL Configuration Tile
              Card(
                child: ExpansionTile(
                  title: const Text('Update-Server Einstellungen', style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
                  leading: const Icon(Icons.settings, size: 20, color: Colors.grey),
                  childrenPadding: const EdgeInsets.all(16),
                  children: [
                    TextField(
                      controller: _serverUrlCtrl,
                      decoration: InputDecoration(
                        labelText: 'Firmware Server Basis-URL',
                        prefixIcon: const Icon(Icons.dns, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                      ),
                      onSubmitted: (val) => fw.setFirmwareServerUrl(val),
                    ),
                    const SizedBox(height: 10),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(minimumSize: const Size.fromHeight(38)),
                      onPressed: () => fw.setFirmwareServerUrl(_serverUrlCtrl.text),
                      child: const Text('URL speichern', style: TextStyle(fontSize: 12)),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
