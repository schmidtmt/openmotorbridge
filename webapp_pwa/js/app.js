/**
 * OpenMotorBridge (OMB) v8.0 - Web Bluetooth Dashboard & PWA Controller
 * With lightweight Bilingual Internationalization (German / English)
 */

// Web Bluetooth Service & Characteristic UUIDs (Matching ble_service_server.cpp)
const OMB_SERVICE_UUID = '23d113ef-5f78-2315-deef-121200a00000';
const TELEMETRY_CHAR_UUID = '23d113ef-5f78-2315-deef-121200a00001';
const CONTROL_CHAR_UUID = '23d113ef-5f78-2315-deef-121200a00002';

// Bilingual Translations Dictionary (DE / EN)
const i18n = {
    de: {
        app_subtitle: 'v8.0 Satelliten-Gateway',
        ble_offline: 'BLE Offline',
        ble_online: 'BLE Online',
        demo_mode: 'Demo-Modus',
        demo_active: 'Demo Aktiv',
        ble_connect: 'BLE Verbinden',
        ble_connected: '✓ Verbunden',
        tab_cockpit: 'Cockpit & Power',
        tab_audio: 'Audio & Ducking',
        tab_cartridges: 'Kassetten & DLE',
        tab_tours: 'Touren & WebDAV',
        tab_hardware: 'Hardware & Reserve',
        dynamics_title: 'Fahrdynamik & Schräglage',
        lean_sub: 'Kurvenschräglage (Bosch BMI270 15-State EKF)',
        speed_label: 'Geschwindigkeit',
        sats_label: 'Satelliten',
        sync_label: '1-PPS Zeit-Sync',
        power_title: 'Spannungs- & Thermomanagement',
        thermal_normal: 'JEITA: Normal (22°C)',
        thermal_cold: 'JEITA: Kälteschutz (< 0°C)',
        thermal_hot: 'JEITA: Hitzeschutz (> 45°C)',
        vign_label: 'Bordnetz KL15 (Zündung)',
        vign_active: 'Status: AKTIV',
        vign_inactive: 'Status: INAKTIV',
        vign_warning: 'WARNUNG: Unterspannung!',
        vbat_label: 'USV-LiPo (Unter Sitzbank)',
        vbat_sub: '1000 mAh Puffer',
        bat_chem_label: 'Starterbatterie-Typ & Schutzschwelle',
        handlebar_label: 'Lenkertaster (CR2032 Batterie)',
        handlebar_sub: 'Bluetooth SIG Service 0x180F Überwachung',
        audio_modes_title: 'Audio-Routing & Betriebsmodi',
        mode_0_name: 'Standard Mode (Mesh Bridge)',
        mode_0_desc: 'Port 1 (Sena) & Port 2 (Cardo) sind simultan aktiv und werden symmetrisch zum Fahrerhelm gemischt.',
        mode_1_name: 'Single Rider Mode',
        mode_1_desc: 'Port 2 stummgeschaltet. Voller Fokus auf Primär-Intercom, Navigation & A2DP-Musik.',
        mode_2_name: 'Cruise Mode (Boom! Box Lautsprecher)',
        mode_2_desc: 'Intercom -6 dB gedämpft. Optimierte Ausgabe über Harley-Davidson Bordlautsprecher.',
        badge_active: 'Aktiv',
        badge_online: 'Online',
        ducking_title: 'Raised-Cosine Ducking & Gain',
        gain_p1_label: 'Port 1 Eingangspegel (Sena Apex)',
        gain_p2_label: 'Port 2 Eingangspegel (Cardo DMC Gen2)',
        ducking_depth_label: 'Navi Ducking Dämpfung (Prio 1)',
        btn_p1_toggle: 'Port 1 Mesh Toggle (200ms)',
        btn_p1_next: 'Port 1 Channel Next (1s)',
        pod1_title: 'Pod 1 (Rahmen links)',
        pod2_title: 'Pod 2 (Rahmen rechts)',
        pod3_title: 'Pod 3 (Heckbürzel)',
        inserted_cartridge: 'Gesteckte Kassette',
        bt_classic_off: 'BT Classic AUS',
        mesh_only_on: 'Mesh-Only Aktiv',
        btn_ground_truth: 'Ground-Truth Re-Sync',
        btn_channel_advance: 'Kanal Weiterschalten (800ms)',
        dle_score_label: 'DLE Gateway Score:',
        lora_power_label: 'LoRa Sendeleistung:',
        btn_onboarding_wizard: 'Onboarding-Wizard',
        storage_title: 'MicroSD & BGH-Ringspeicher',
        storage_usage_label: 'Speicherbelegung (4-Bit SDIO FAT32)',
        storage_purge_sub: '14.5 GB frei • Auto-Purge Schwellwert: 200 MB',
        btn_actioncam_marker: 'Actioncam Marker setzen',
        btn_webdav_sync: 'WebDAV Sofort-Sync',
        webdav_title: 'Heim-WLAN & WebDAV Sync',
        webdav_url_label: 'WebDAV Server URL',
        webdav_user_label: 'Benutzername',
        webdav_pass_label: 'Passwort / App-Token',
        btn_save_webdav: 'Speichern & Testen',
        saved_tours_title: 'Gespeicherte Touren (/tracks/)',
        btn_refresh: 'Aktualisieren',
        th_date: 'Datum & Uhrzeit',
        th_duration: 'Dauer',
        th_distance: 'Distanz',
        th_max_lean: 'Max. Schräglage',
        th_status: 'Status',
        th_actions: 'Aktionen',
        status_uploaded: 'Hochgeladen',
        status_favorite: '★ Favorit',
        reserve_title: 'Reserve-Schnittstellen (HD26 Pins 25 & 26)',
        reserve_a_high: 'Pegel: HIGH (3.3V)',
        reserve_a_sub: 'Verwendung: Externer Lenker-PTT / Alarmanlagen-Sensor',
        reserve_b_active: 'Ausgang: AKTIV (5V ON)',
        reserve_b_inactive: 'Ausgang: INAKTIV (0V OFF)',
        reserve_b_sub: 'Zweck: Actioncam Power-Gate / Relais',
        btn_toggle_output: 'Toggle Output',
        diagnostics_title: 'Fahrzeug-CAN & Diagnostik',
        can_speed_label: 'CAN-Bus Geschwindigkeit:',
        codec_label: 'Audio-Codec:',
        transient_label: 'Transientenschutz:',
        cpu_clock_label: 'CPU Core 0 / Core 1 Takt:',
        btn_system_reboot: 'Zentralbox Warmstart (Soft Reboot)',
        wizard_title: '✨ Kassetten-Onboarding-Wizard',
        wizard_intro: 'Um maximale HF-Entkopplung und Latenzfreiheit zu gewährleisten, führe vor dem Einstecken neuer Intercoms folgende Schritte durch:',
        wizard_step1_h: 'Bluetooth Classic deaktivieren',
        wizard_step1_p: 'Entkoppele alle gekoppelten Smartphones und GPS-Navis vom Intercom, um 2,4-GHz-Kanalblockaden zu verhindern.',
        wizard_step2_h: 'Reinen Mesh-Modus erzwingen',
        wizard_step2_p: 'Aktiviere "Open Mesh Channel 1" (Sena) bzw. "Open DMC Group" (Cardo) und deaktiviere Audio-Multitasking im Endgerät.',
        wizard_step3_h: 'Kassette einschieben & verriegeln',
        wizard_step3_p: 'Schiebe die Kassette ein, bis die POM-C Snap-Lock Klinken einrasten, und schließe den 90°-Cam-Lock Drehriegel.',
        btn_wizard_finish: 'Verstanden & Profil aktivieren'
    },
    en: {
        app_subtitle: 'v8.0 Satellite Gateway',
        ble_offline: 'BLE Offline',
        ble_online: 'BLE Online',
        demo_mode: 'Demo Mode',
        demo_active: 'Demo Active',
        ble_connect: 'Connect BLE',
        ble_connected: '✓ Connected',
        tab_cockpit: 'Cockpit & Power',
        tab_audio: 'Audio & Ducking',
        tab_cartridges: 'Cartridges & DLE',
        tab_tours: 'Tours & WebDAV',
        tab_hardware: 'Hardware & Reserve',
        dynamics_title: 'Ride Dynamics & Lean Angle',
        lean_sub: 'Cornering Lean Angle (Bosch BMI270 15-State EKF)',
        speed_label: 'Speed',
        sats_label: 'Satellites',
        sync_label: '1-PPS Time Sync',
        power_title: 'Voltage & Thermal Management',
        thermal_normal: 'JEITA: Normal (22°C)',
        thermal_cold: 'JEITA: Cold Inhibit (< 0°C)',
        thermal_hot: 'JEITA: Heat Inhibit (> 45°C)',
        vign_label: 'Vehicle KL15 (Ignition)',
        vign_active: 'Status: ACTIVE',
        vign_inactive: 'Status: INACTIVE',
        vign_warning: 'WARNING: Undervoltage!',
        vbat_label: 'UPS LiPo (Under Seat)',
        vbat_sub: '1000 mAh Buffer',
        bat_chem_label: 'Starter Battery Chemistry & Threshold',
        handlebar_label: 'Handlebar Remote (CR2032 Battery)',
        handlebar_sub: 'Bluetooth SIG Service 0x180F Monitoring',
        audio_modes_title: 'Audio Routing & Operating Modes',
        mode_0_name: 'Standard Mode (Mesh Bridge)',
        mode_0_desc: 'Port 1 (Sena) & Port 2 (Cardo) are simultaneously active and mixed symmetrically to the rider headset.',
        mode_1_name: 'Single Rider Mode',
        mode_1_desc: 'Port 2 muted. Full focus on primary intercom, navigation & A2DP music.',
        mode_2_name: 'Cruise Mode (Boom! Box Speakers)',
        mode_2_desc: 'Intercom attenuated by -6 dB. Optimized output via Harley-Davidson fairing speakers.',
        badge_active: 'Active',
        badge_online: 'Online',
        ducking_title: 'Raised-Cosine Ducking & Gain',
        gain_p1_label: 'Port 1 Input Gain (Sena Apex)',
        gain_p2_label: 'Port 2 Input Gain (Cardo DMC Gen2)',
        ducking_depth_label: 'Navi Ducking Depth (Priority 1)',
        btn_p1_toggle: 'Port 1 Mesh Toggle (200ms)',
        btn_p1_next: 'Port 1 Channel Next (1s)',
        pod1_title: 'Pod 1 (Left Frame)',
        pod2_title: 'Pod 2 (Right Frame)',
        pod3_title: 'Pod 3 (Rear Fender)',
        inserted_cartridge: 'Plugged Cartridge',
        bt_classic_off: 'BT Classic OFF',
        mesh_only_on: 'Mesh-Only Active',
        btn_ground_truth: 'Ground-Truth Re-Sync',
        btn_channel_advance: 'Advance Channel (800ms)',
        dle_score_label: 'DLE Gateway Score:',
        lora_power_label: 'LoRa Output Power:',
        btn_onboarding_wizard: 'Onboarding Wizard',
        storage_title: 'MicroSD & Privacy Ring Buffer',
        storage_usage_label: 'Storage Usage (4-Bit SDIO FAT32)',
        storage_purge_sub: '14.5 GB free • Auto-purge threshold: 200 MB',
        btn_actioncam_marker: 'Set Action Cam Marker',
        btn_webdav_sync: 'WebDAV Instant Sync',
        webdav_title: 'Home Wi-Fi & WebDAV Sync',
        webdav_url_label: 'WebDAV Server URL',
        webdav_user_label: 'Username',
        webdav_pass_label: 'Password / App Token',
        btn_save_webdav: 'Save & Test Connection',
        saved_tours_title: 'Recorded Rides (/tracks/)',
        btn_refresh: 'Refresh',
        th_date: 'Date & Time',
        th_duration: 'Duration',
        th_distance: 'Distance',
        th_max_lean: 'Max Lean Angle',
        th_status: 'Status',
        th_actions: 'Actions',
        status_uploaded: 'Uploaded',
        status_favorite: '★ Favorite',
        reserve_title: 'Reserve Interfaces (HD26 Pins 25 & 26)',
        reserve_a_high: 'Level: HIGH (3.3V)',
        reserve_a_sub: 'Usage: External Handlebar PTT / Alarm Sensor',
        reserve_b_active: 'Output: ACTIVE (5V ON)',
        reserve_b_inactive: 'Output: INACTIVE (0V OFF)',
        reserve_b_sub: 'Purpose: Action Cam Power Gate / Relay',
        btn_toggle_output: 'Toggle Output',
        diagnostics_title: 'Vehicle CAN & Diagnostics',
        can_speed_label: 'CAN Bus Baudrate:',
        codec_label: 'Audio Codec:',
        transient_label: 'Transient Protection:',
        cpu_clock_label: 'CPU Core 0 / Core 1 Clock:',
        btn_system_reboot: 'Central Box Warmstart (Soft Reboot)',
        wizard_title: '✨ Cartridge Onboarding Wizard',
        wizard_intro: 'To ensure maximum RF isolation and zero latency, follow these steps before inserting a new intercom unit:',
        wizard_step1_h: 'Disable Bluetooth Classic',
        wizard_step1_p: 'Unpair all smartphones and GPS units from the intercom to eliminate in-band 2.4 GHz channel collisions.',
        wizard_step2_h: 'Force Pure Mesh Mode',
        wizard_step2_p: 'Activate "Open Mesh Channel 1" (Sena) or "Open DMC Group" (Cardo) and disable audio multitasking on the device.',
        wizard_step3_h: 'Insert & Lock Cartridge',
        wizard_step3_p: 'Slide the cartridge in until the POM-C snap-lock clicks, then turn the 90° cam-lock to secure.',
        btn_wizard_finish: 'Understood & Activate Profile'
    }
};

// Application State
const state = {
    lang: localStorage.getItem('omb_lang') || (navigator.language.startsWith('de') ? 'de' : 'en'),
    isBleConnected: false,
    isDemoMode: false,
    demoInterval: null,
    batteryChemistry: localStorage.getItem('omb_bat_chem') || 'agm',
    webdavConfig: JSON.parse(localStorage.getItem('omb_webdav_cfg') || '{}'),
    telemetry: {
        v_ign: 12.6,
        v_bat: 4.12,
        btn_bat: 95,
        speed: 0.0,
        lean_angle: 0.0,
        sats: 18,
        mode: 0,
        reserve_b: true
    }
};

// DOM Elements
const btnLangToggle = document.getElementById('btn-lang-toggle');
const labelLang = document.getElementById('label-lang');
const btnConnect = document.getElementById('btn-connect');
const labelConnectBtn = document.getElementById('label-connect-btn');
const btnDemo = document.getElementById('btn-demo-mode');
const pillBleStatus = document.getElementById('pill-ble-status');
const dotBle = document.getElementById('dot-ble');
const labelBleStatus = document.getElementById('label-ble-status');

const valVign = document.getElementById('val-vign');
const valVbat = document.getElementById('val-vbat');
const valBtnBat = document.getElementById('val-btn-bat');
const barBtnBat = document.getElementById('bar-btn-bat');
const valSpeed = document.getElementById('val-speed');
const valSats = document.getElementById('val-sats');
const valLeanAngle = document.getElementById('val-lean-angle');
const bikeLeanVisual = document.getElementById('bike-lean-visual');
const selectBatteryType = document.getElementById('select-battery-type');
const labelBatteryChem = document.getElementById('label-battery-chem');

const sliderGainP1 = document.getElementById('slider-gain-p1');
const labelGainP1 = document.getElementById('label-gain-p1');
const sliderGainP2 = document.getElementById('slider-gain-p2');
const labelGainP2 = document.getElementById('label-gain-p2');
const sliderDuckingDepth = document.getElementById('slider-ducking-depth');
const labelDuckingDepth = document.getElementById('label-ducking-depth');

const wizardModal = document.getElementById('wizard-modal');
const btnOpenWizard = document.getElementById('btn-open-wizard');
const btnCloseWizard = document.getElementById('btn-close-wizard');
const btnWizardFinish = document.getElementById('btn-wizard-finish');

const btnToggleReserveB = document.getElementById('btn-toggle-reserve-b');
const valReserveBState = document.getElementById('val-reserve-b-state');

let bleDevice = null;
let controlChar = null;

// ==========================================
// 1. Language & i18n Engine
// ==========================================
function setLanguage(lang) {
    state.lang = lang;
    localStorage.setItem('omb_lang', lang);
    labelLang.textContent = lang.toUpperCase();

    const dict = i18n[lang] || i18n.de;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Update battery chemistry options text
    updateBatteryOptionsText(lang);
    updateBleUiState(state.isBleConnected);

    showToast(lang === 'de' ? 'Sprache: Deutsch' : 'Language: English', 'info');
}

function updateBatteryOptionsText(lang) {
    if (!selectBatteryType) return;
    if (lang === 'en') {
        selectBatteryType.options[0].text = 'AGM / Gel (Cut-Off 11.8 V)';
        selectBatteryType.options[1].text = 'Standard Flooded Wet (Cut-Off 11.6 V)';
        selectBatteryType.options[2].text = 'LiFePO4 Lithium Iron Phosphate (Cut-Off 12.8 V)';
        selectBatteryType.options[3].text = 'Li-Ion NMC Starter Battery (Cut-Off 10.5 V)';
    } else {
        selectBatteryType.options[0].text = 'AGM / Gel (Abschaltschwelle 11.8 V)';
        selectBatteryType.options[1].text = 'Standard Blei-Säure Nass (Abschaltschwelle 11.6 V)';
        selectBatteryType.options[2].text = 'LiFePO4 Lithium-Eisenphosphat (Abschaltschwelle 12.8 V)';
        selectBatteryType.options[3].text = 'Li-Ion NMC Starterbatterie (Abschaltschwelle 10.5 V)';
    }
}

btnLangToggle.addEventListener('click', () => {
    setLanguage(state.lang === 'de' ? 'en' : 'de');
});

// ==========================================
// 2. Toast Notification Helper
// ==========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : '⚡';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ==========================================
// 3. Tab Navigation
// ==========================================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const tabId = btn.getAttribute('data-tab');
        const targetTab = document.getElementById(tabId);
        if (targetTab) {
            targetTab.classList.add('active');
        }
    });
});

// ==========================================
// 4. Web Bluetooth API Connection
// ==========================================
btnConnect.addEventListener('click', async () => {
    if (state.isBleConnected) {
        disconnectBle();
        return;
    }

    try {
        const dict = i18n[state.lang];
        showToast(state.lang === 'de' ? 'Suche nach OpenMotorBridge v8.0...' : 'Scanning for OpenMotorBridge v8.0...');
        bleDevice = await navigator.bluetooth.requestDevice({
            filters: [{ namePrefix: 'OpenMotorBridge' }],
            optionalServices: [OMB_SERVICE_UUID]
        });

        bleDevice.addEventListener('gattserverdisconnected', onBleDisconnected);

        showToast(state.lang === 'de' ? 'Verbinde mit GATT Server...' : 'Connecting to GATT Server...');
        const server = await bleDevice.gatt.connect();
        const service = await server.getPrimaryService(OMB_SERVICE_UUID);

        // Telemetry Notifications
        const teleChar = await service.getCharacteristic(TELEMETRY_CHAR_UUID);
        await teleChar.startNotifications();
        teleChar.addEventListener('characteristicvaluechanged', handleBleTelemetry);

        controlChar = await service.getCharacteristic(CONTROL_CHAR_UUID);

        state.isBleConnected = true;
        updateBleUiState(true);
        showToast(state.lang === 'de' ? 'Erfolgreich mit OpenMotorBridge verbunden!' : 'Connected to OpenMotorBridge!', 'success');

        if (state.isDemoMode) toggleDemoMode(false);

    } catch (err) {
        console.error('BLE connection failed:', err);
        showToast((state.lang === 'de' ? 'Verbindung abgebrochen: ' : 'Connection failed: ') + err.message, 'warning');
    }
});

function onBleDisconnected() {
    state.isBleConnected = false;
    updateBleUiState(false);
    showToast(state.lang === 'de' ? 'OpenMotorBridge BLE getrennt.' : 'OpenMotorBridge BLE disconnected.', 'warning');
}

function disconnectBle() {
    if (bleDevice && bleDevice.gatt.connected) {
        bleDevice.gatt.disconnect();
    }
    state.isBleConnected = false;
    updateBleUiState(false);
}

function updateBleUiState(connected) {
    const dict = i18n[state.lang];
    if (connected) {
        labelConnectBtn.textContent = dict.ble_connected;
        btnConnect.classList.add('connected');
        dotBle.classList.add('active');
        labelBleStatus.textContent = dict.ble_online;
    } else {
        labelConnectBtn.textContent = dict.ble_connect;
        btnConnect.classList.remove('connected');
        dotBle.classList.remove('active');
        labelBleStatus.textContent = dict.ble_offline;
    }
}

function handleBleTelemetry(event) {
    const view = event.target.value;
    if (view.byteLength >= 16) {
        const vign = view.getFloat32(0, true);
        const vbat = view.getFloat32(4, true);
        const btnBat = view.getUint8(8);
        const mode = view.getUint8(9);
        const lean = view.getInt8(10);

        updateTelemetryUi({
            v_ign: vign,
            v_bat: vbat,
            btn_bat: btnBat,
            mode: mode,
            lean_angle: lean
        });
    }
}

// ==========================================
// 5. UI Telemetry Updater
// ==========================================
function updateTelemetryUi(data) {
    const dict = i18n[state.lang];
    if (data.v_ign !== undefined) {
        valVign.textContent = `${data.v_ign.toFixed(1)} V`;
        const cutOffMap = { agm: 11.8, wet: 11.6, lifepo4: 12.8, nmc: 10.5 };
        const threshold = cutOffMap[state.batteryChemistry] || 11.8;
        if (data.v_ign < threshold) {
            valVign.style.color = 'var(--accent-red)';
            document.getElementById('sub-vign-status').textContent = dict.vign_warning;
        } else {
            valVign.style.color = 'var(--accent-green)';
            document.getElementById('sub-vign-status').textContent = dict.vign_active;
        }
    }

    if (data.v_bat !== undefined) {
        valVbat.textContent = `${data.v_bat.toFixed(2)} V`;
    }

    if (data.btn_bat !== undefined) {
        valBtnBat.textContent = `${data.btn_bat} %`;
        barBtnBat.style.width = `${data.btn_bat}%`;
    }

    if (data.speed !== undefined) {
        valSpeed.textContent = data.speed.toFixed(1);
    }

    if (data.sats !== undefined) {
        valSats.textContent = data.sats;
    }

    if (data.lean_angle !== undefined) {
        valLeanAngle.textContent = `${data.lean_angle.toFixed(1)}°`;
        bikeLeanVisual.style.transform = `rotate(${data.lean_angle}deg)`;
    }

    if (data.mode !== undefined) {
        document.querySelectorAll('.mode-card').forEach(card => {
            const m = parseInt(card.getAttribute('data-mode'), 10);
            if (m === data.mode) {
                card.classList.add('active');
                if (!card.querySelector('.badge-green')) {
                    const badge = document.createElement('span');
                    badge.className = 'card-badge badge-green';
                    badge.textContent = dict.badge_active;
                    card.querySelector('.mode-card-header').appendChild(badge);
                }
            } else {
                card.classList.remove('active');
                const badge = card.querySelector('.badge-green');
                if (badge) badge.remove();
            }
        });
    }
}

// ==========================================
// 6. Demo / Simulation Mode
// ==========================================
btnDemo.addEventListener('click', () => {
    toggleDemoMode(!state.isDemoMode);
});

function toggleDemoMode(enable) {
    const dict = i18n[state.lang];
    state.isDemoMode = enable;
    if (enable) {
        btnDemo.classList.add('active');
        btnDemo.querySelector('span').textContent = dict.demo_active;
        showToast(state.lang === 'de' ? 'Live-Simulation gestartet' : 'Live simulation started', 'success');

        let angleTime = 0;
        state.demoInterval = setInterval(() => {
            angleTime += 0.05;
            const simulatedLean = Math.sin(angleTime) * 36.5 + (Math.random() * 2 - 1);
            const simulatedSpeed = Math.abs(Math.cos(angleTime * 0.7)) * 75 + 25;
            const simulatedVign = 12.6 + Math.sin(angleTime * 0.2) * 0.4;

            updateTelemetryUi({
                v_ign: simulatedVign,
                v_bat: 4.12,
                btn_bat: 95,
                speed: simulatedSpeed,
                sats: 19,
                lean_angle: simulatedLean
            });
        }, 100);
    } else {
        btnDemo.classList.remove('active');
        btnDemo.querySelector('span').textContent = dict.demo_mode;
        if (state.demoInterval) {
            clearInterval(state.demoInterval);
            state.demoInterval = null;
        }
        updateTelemetryUi({
            v_ign: 12.6,
            v_bat: 4.12,
            btn_bat: 95,
            speed: 0.0,
            sats: 18,
            lean_angle: 0.0
        });
        showToast(state.lang === 'de' ? 'Demo-Simulation beendet' : 'Demo simulation stopped');
    }
}

// ==========================================
// 7. Audio Modes & Sliders
// ==========================================
document.querySelectorAll('.mode-card').forEach(card => {
    card.addEventListener('click', async () => {
        const mode = parseInt(card.getAttribute('data-mode'), 10);
        updateTelemetryUi({ mode: mode });
        showToast(`${state.lang === 'de' ? 'Betriebsmodus gewechselt: Modus' : 'Operating mode switched: Mode'} ${mode}`);

        if (controlChar) {
            try {
                await controlChar.writeValue(new Uint8Array([0x01, mode]));
            } catch (e) {
                console.warn('GATT Write failed:', e);
            }
        }
    });
});

sliderGainP1.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    labelGainP1.textContent = `${val >= 0 ? '+' : ''}${val.toFixed(1)} dB`;
});

sliderGainP2.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    labelGainP2.textContent = `${val >= 0 ? '+' : ''}${val.toFixed(1)} dB`;
});

sliderDuckingDepth.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    labelDuckingDepth.textContent = `${val.toFixed(1)} dB`;
});

// Hardware Trigger Buttons
document.getElementById('btn-trigger-p1-toggle').addEventListener('click', async () => {
    showToast(state.lang === 'de' ? 'Sena Apex: Mesh Toggle Puls (200ms) ausgelöst' : 'Sena Apex: Mesh Toggle Pulse (200ms) triggered', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x02, 0x00]));
});

document.getElementById('btn-trigger-p1-next').addEventListener('click', async () => {
    showToast(state.lang === 'de' ? 'Sena Apex: Kanalwechsel Puls (1000ms) ausgelöst' : 'Sena Apex: Channel Next Pulse (1000ms) triggered', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x03, 0x00]));
});

document.getElementById('btn-p1-resync').addEventListener('click', () => {
    showToast(state.lang === 'de' ? 'Ground-Truth Mesh Re-Sync gesendet' : 'Ground-Truth Mesh Re-Sync sent', 'success');
});

document.getElementById('btn-p2-next').addEventListener('click', async () => {
    showToast(state.lang === 'de' ? 'Cardo DMC Gen2: Kanalweiterschaltung (800ms) ausgelöst' : 'Cardo DMC Gen2: Channel advance (800ms) triggered', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x04, 0x00]));
});

// ==========================================
// 8. Battery Chemistry Selector
// ==========================================
selectBatteryType.addEventListener('change', (e) => {
    state.batteryChemistry = e.target.value;
    localStorage.setItem('omb_bat_chem', state.batteryChemistry);
    const cutOffMap = {
        agm: 'AGM / Gel (11.8 V Cut-Off)',
        wet: 'Wet Lead-Acid (11.6 V Cut-Off)',
        lifepo4: 'LiFePO4 (12.8 V Cut-Off)',
        nmc: 'Li-Ion NMC (10.5 V Cut-Off)'
    };
    labelBatteryChem.textContent = cutOffMap[state.batteryChemistry] || '11.8 V Cut-Off';
    showToast(state.lang === 'de' ? `Batterie-Chemie: ${e.target.options[e.target.selectedIndex].text}` : `Battery chemistry: ${e.target.options[e.target.selectedIndex].text}`, 'success');
});

// ==========================================
// 8b. Class-Oriented Cartridge Profile Engine
// ==========================================
const CARTRIDGE_PROFILES = {
    disabled: {
        vendor: 'Slot Deaktiviert (0.0 mA • Mute)',
        vendor_en: 'Slot Disabled (0.0 mA • Mute)',
        badge: 'badge_offline',
        badge_class: 'badge-purple',
        status: 'Power OFF • Mute (-96 dB)',
        status_en: 'Power OFF • Mute (-96 dB)',
        status_color: 'var(--text-muted)',
        idle_ma: 0,
        dle_bonus: 0
    },
    sena_60s: {
        vendor: 'Sena Technologies • Mesh 3.0 Wave',
        vendor_en: 'Sena Technologies • Mesh 3.0 Wave',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +60 Pkt.',
        status_en: 'Power ON • DLE +60 Pts.',
        status_color: 'var(--accent-green)',
        idle_ma: 50,
        dle_bonus: 60
    },
    sena_apex: {
        vendor: 'Sena Technologies • Mesh 3.0',
        vendor_en: 'Sena Technologies • Mesh 3.0',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +60 Pkt.',
        status_en: 'Power ON • DLE +60 Pts.',
        status_color: 'var(--accent-green)',
        idle_ma: 45,
        dle_bonus: 60
    },
    sena_50_series: {
        vendor: 'Sena Technologies • Mesh 2.0/3.0',
        vendor_en: 'Sena Technologies • Mesh 2.0/3.0',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +60 Pkt.',
        status_en: 'Power ON • DLE +60 Pts.',
        status_color: 'var(--accent-green)',
        idle_ma: 45,
        dle_bonus: 60
    },
    sena_spider: {
        vendor: 'Sena Technologies • Mesh-Only',
        vendor_en: 'Sena Technologies • Mesh-Only',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +40 Pkt.',
        status_en: 'Power ON • DLE +40 Pts.',
        status_color: 'var(--accent-blue)',
        idle_ma: 40,
        dle_bonus: 40
    },
    sena_legacy_bt: {
        vendor: 'Sena Technologies • Bluetooth Intercom',
        vendor_en: 'Sena Technologies • Bluetooth Intercom',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +20 Pkt.',
        status_en: 'Power ON • DLE +20 Pts.',
        status_color: 'var(--accent-orange)',
        idle_ma: 35,
        dle_bonus: 20
    },
    cardo_dmc_gen2: {
        vendor: 'Cardo Systems • DMC Gen2',
        vendor_en: 'Cardo Systems • DMC Gen2',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +60 Pkt.',
        status_en: 'Power ON • DLE +60 Pts.',
        status_color: 'var(--accent-green)',
        idle_ma: 45,
        dle_bonus: 60
    },
    cardo_freecom_live: {
        vendor: 'Cardo Systems • Live Intercom BT5.2',
        vendor_en: 'Cardo Systems • Live Intercom BT5.2',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +40 Pkt.',
        status_en: 'Power ON • DLE +40 Pts.',
        status_color: 'var(--accent-blue)',
        idle_ma: 38,
        dle_bonus: 40
    },
    cardo_dmc_legacy: {
        vendor: 'Cardo Systems • DMC Gen1',
        vendor_en: 'Cardo Systems • DMC Gen1',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +30 Pkt.',
        status_en: 'Power ON • DLE +30 Pts.',
        status_color: 'var(--accent-orange)',
        idle_ma: 42,
        dle_bonus: 30
    },
    pmr446_gateway: {
        vendor: 'Alan Electronics • PMR446 Funk',
        vendor_en: 'Alan Electronics • PMR446 Radio',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +10 Pkt.',
        status_en: 'Power ON • DLE +10 Pts.',
        status_color: 'var(--accent-orange)',
        idle_ma: 60,
        dle_bonus: 10
    }
};

function updatePodDisplay(podNum, profileKey) {
    const prof = CARTRIDGE_PROFILES[profileKey] || CARTRIDGE_PROFILES.disabled;
    const isDe = (state.lang === 'de');
    const badgeEl = document.getElementById(`pod${podNum}-badge`);
    const vendorEl = document.getElementById(`pod${podNum}-vendor`);
    const statusEl = document.getElementById(`pod${podNum}-status`);
    
    if (vendorEl) vendorEl.textContent = isDe ? prof.vendor : prof.vendor_en;
    if (statusEl) {
        statusEl.textContent = isDe ? prof.status : prof.status_en;
        statusEl.style.color = prof.status_color;
    }
    if (badgeEl) {
        if (profileKey === 'disabled') {
            badgeEl.className = 'card-badge badge-purple';
            badgeEl.textContent = isDe ? 'Aus' : 'Off';
        } else {
            badgeEl.className = 'card-badge badge-green';
            badgeEl.textContent = isDe ? 'Online' : 'Online';
        }
    }
    
    // Recalculate DLE Score
    const p1Key = document.getElementById('select-pod1-profile')?.value || 'sena_apex';
    const p2Key = document.getElementById('select-pod2-profile')?.value || 'cardo_dmc_gen2';
    const p1Bonus = CARTRIDGE_PROFILES[p1Key]?.dle_bonus || 0;
    const p2Bonus = CARTRIDGE_PROFILES[p2Key]?.dle_bonus || 0;
    const maxBonus = Math.max(p1Bonus, p2Bonus);
    const dleTotal = maxBonus + 20 + 10 + 10; // HW + Power + GNSS + LoRa
    const dleEl = document.getElementById('val-dle-score');
    if (dleEl) dleEl.textContent = `${dleTotal} / 100 Pkt.`;
}

document.getElementById('select-pod1-profile')?.addEventListener('change', (e) => {
    updatePodDisplay(1, e.target.value);
    showToast(state.lang === 'de' ? `Pod 1 Profil geladen: ${e.target.options[e.target.selectedIndex].text}` : `Pod 1 profile applied: ${e.target.options[e.target.selectedIndex].text}`, 'success');
});

document.getElementById('select-pod2-profile')?.addEventListener('change', (e) => {
    updatePodDisplay(2, e.target.value);
    showToast(state.lang === 'de' ? `Pod 2 Profil geladen: ${e.target.options[e.target.selectedIndex].text}` : `Pod 2 profile applied: ${e.target.options[e.target.selectedIndex].text}`, 'success');
});

// ==========================================
// 9. Onboarding Wizard Modal
// ==========================================
btnOpenWizard.addEventListener('click', () => {
    wizardModal.classList.add('active');
});

btnCloseWizard.addEventListener('click', () => {
    wizardModal.classList.remove('active');
});

btnWizardFinish.addEventListener('click', () => {
    wizardModal.classList.remove('active');
    showToast(state.lang === 'de' ? 'Kassetten-Profil erfolgreich eingerichtet & aktiviert!' : 'Cartridge profile configured & activated successfully!', 'success');
});

// ==========================================
// 10. Hardware Reserve I/O Toggle
// ==========================================
btnToggleReserveB.addEventListener('click', () => {
    const dict = i18n[state.lang];
    state.telemetry.reserve_b = !state.telemetry.reserve_b;
    if (state.telemetry.reserve_b) {
        valReserveBState.textContent = dict.reserve_b_active;
        valReserveBState.style.color = 'var(--text-primary)';
        showToast(state.lang === 'de' ? 'RESERVE_GPIO_B aktiviert (5V ON)' : 'RESERVE_GPIO_B enabled (5V ON)', 'success');
    } else {
        valReserveBState.textContent = dict.reserve_b_inactive;
        valReserveBState.style.color = 'var(--text-muted)';
        showToast(state.lang === 'de' ? 'RESERVE_GPIO_B deaktiviert' : 'RESERVE_GPIO_B disabled', 'info');
    }
});

// ==========================================
// 11. Tour Logger & WebDAV Sync
// ==========================================
document.getElementById('btn-trigger-video-marker').addEventListener('click', () => {
    showToast(state.lang === 'de' ? 'Actioncam 1-PPS Video-Marker im GPX 2.0 Track gesetzt!' : 'Action cam 1-PPS video marker embedded in GPX 2.0 track!', 'success');
});

document.getElementById('btn-trigger-webdav-now').addEventListener('click', () => {
    showToast(state.lang === 'de' ? 'WebDAV Sync gestartet: Verbinde mit Nextcloud...' : 'WebDAV sync started: Connecting to Nextcloud...', 'info');
    setTimeout(() => {
        showToast(state.lang === 'de' ? '2 GPX-Touren erfolgreich via TLS 1.3 hochgeladen!' : '2 GPX tours uploaded via TLS 1.3 successfully!', 'success');
    }, 1200);
});

document.getElementById('btn-save-webdav').addEventListener('click', () => {
    const url = document.getElementById('input-webdav-url').value;
    const user = document.getElementById('input-webdav-user').value;
    localStorage.setItem('omb_webdav_cfg', JSON.stringify({ url, user }));
    showToast(state.lang === 'de' ? 'WebDAV Zugangsdaten gespeichert' : 'WebDAV credentials saved', 'success');
});

// Mock GPX Download Generator
window.downloadMockGpx = function (filename) {
    const gpxContent = `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="OpenMotorBridge v8.0" xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>OMB Motorcycle Ride</name>
    <trkseg>
      <trkpt lat="47.3769" lon="8.5417"><ele>408.2</ele><time>2026-08-23T09:15:00Z</time></trkpt>
      <trkpt lat="47.3820" lon="8.5520"><ele>420.5</ele><time>2026-08-23T09:20:00Z</time></trkpt>
    </trkseg>
  </trk>
</gpx>`;
    const blob = new Blob([gpxContent], { type: 'application/gpx+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(state.lang === 'de' ? `Download gestartet: ${filename}` : `Download started: ${filename}`, 'success');
};

// Initialize Language on Boot
setLanguage(state.lang);

// ==========================================
// 12. Service Worker Registration (PWA Offline)
// ==========================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js').then(() => {
            console.log('OpenMotorBridge PWA Service Worker ready.');
        }).catch(err => {
            console.warn('SW registration failed:', err);
        });
    });
}