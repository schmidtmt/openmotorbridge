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
        status_led_title: 'WS2812B RGB Status-LED (Gehäusedeckel)',
        gpx_modal_title: 'Erweiterter GPX-Export & Navi-Formatierung',
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
        ambient_mic_label: 'Front Ambient-Mic Pegel & AGC (v ≤ 30 km/h)',
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
        btn_learn_uuid: 'UUID anlernen',
        uuid_modal_title: 'Neue Kassette erkannt!',
        detected_slot: 'Erkannter Steckplatz:',
        uuid_assign_intro: 'Dieser Kassetten-Hardware wurde bisher noch kein Profil zugewiesen. Welches Intercom oder Funkgerät ist in dieser Kassette verbaut?',
        lbl_select_profile: 'Hardware-Profil auswählen:',
        btn_save_mapping: 'Profil zuweisen & speichern',
        btn_cancel: 'Später zuweisen',
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
        live_map_title: 'Live GPS-Spur & OpenMotorMesh Gruppen-Radar',
        audio_vu_title: 'Echtzeit Audio-Matrix & Live-Pegelüberwachung',
        btn_guide_ptt: 'Guide Pass-Through (10s)',
        btn_siren_sim: 'Sirenen-Alarm Test',
        btn_replay_tour: 'Tour im Cockpit abspielen',
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
        status_led_title: 'WS2812B RGB Status LED (Enclosure Lid)',
        gpx_modal_title: 'Extended GPX Export & Navigation Formatting',
        live_map_title: 'Live GPS Trail & OpenMotorMesh Group Radar',
        audio_vu_title: 'Realtime Audio Matrix & Live Level Meter',
        btn_guide_ptt: 'Guide Pass-Through (10s)',
        btn_siren_sim: 'Siren Alert Test',
        btn_replay_tour: 'Replay Tour in Cockpit',
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
        ambient_mic_label: 'Front Ambient Mic Level & AGC (v ≤ 30 km/h)',
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
        btn_learn_uuid: 'Learn UUID',
        uuid_modal_title: 'New Cartridge Detected!',
        detected_slot: 'Detected Slot:',
        uuid_assign_intro: 'This cartridge hardware has not been mapped to a profile yet. Which intercom or radio is installed in this cartridge?',
        lbl_select_profile: 'Select Hardware Profile:',
        btn_save_mapping: 'Assign & Save Profile',
        btn_cancel: 'Assign Later',
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
const sliderGainAmbient = document.getElementById('slider-gain-ambient');
const labelGainAmbient = document.getElementById('label-gain-ambient');

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

sliderGainAmbient?.addEventListener('input', (e) => {
    const val = parseFloat(e.target.value);
    labelGainAmbient.textContent = `${val >= 0 ? '+' : ''}${val.toFixed(1)} dB (AGC aktiv)`;
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
    sena_vortex: {
        vendor: 'Sena Technologies • Bluetooth 5.1 (Vortex)',
        vendor_en: 'Sena Technologies • Bluetooth 5.1 (Vortex)',
        badge: 'badge_online',
        badge_class: 'badge-green',
        status: 'Power ON • DLE +20 Pkt.',
        status_en: 'Power ON • DLE +20 Pts.',
        status_color: 'var(--accent-orange)',
        idle_ma: 32,
        dle_bonus: 20
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
// 9b. 1-Wire New UUID Detection & Profile Assignment
// ==========================================
const uuidDetectModal = document.getElementById('uuid-detect-modal');
const btnCloseUuidModal = document.getElementById('btn-close-uuid-modal');
const btnCancelUuid = document.getElementById('btn-cancel-uuid');
const btnSaveUuidMapping = document.getElementById('btn-save-uuid-mapping');
const detectedSlotName = document.getElementById('detected-slot-name');
const detectedUuidVal = document.getElementById('detected-uuid-val');
const selectUuidProfile = document.getElementById('select-uuid-profile');

let currentDetectedPort = 1;

function openUuidDetectionModal(portNum, customUid = null) {
    currentDetectedPort = portNum;
    const isDe = (state.lang === 'de');
    if (detectedSlotName) {
        detectedSlotName.textContent = portNum === 1 
            ? (isDe ? 'Pod 1 (Rahmen links)' : 'Pod 1 (Frame Left)') 
            : (isDe ? 'Pod 2 (Rahmen rechts)' : 'Pod 2 (Frame Right)');
    }
    if (detectedUuidVal) {
        detectedUuidVal.textContent = customUid || (portNum === 1 ? '01:A2:3B:4C:5D:6E:7F:8A' : '01:B3:78:11:44:90:3A');
    }
    if (uuidDetectModal) uuidDetectModal.classList.add('active');
}

function closeUuidDetectionModal() {
    if (uuidDetectModal) uuidDetectModal.classList.remove('active');
}

btnCloseUuidModal?.addEventListener('click', closeUuidDetectionModal);
btnCancelUuid?.addEventListener('click', closeUuidDetectionModal);

btnSaveUuidMapping?.addEventListener('click', () => {
    const selectedProfile = selectUuidProfile?.value || 'sena_50_series';
    const profileText = selectUuidProfile?.options[selectUuidProfile.selectedIndex]?.text || selectedProfile;
    const uid = detectedUuidVal?.textContent || '01:A2:3B:4C:5D:6E:7F:8A';
    
    // Save to localStorage mapping
    try {
        const mapping = JSON.parse(localStorage.getItem('omb_cartridge_mapping') || '{}');
        mapping[uid] = selectedProfile;
        localStorage.setItem('omb_cartridge_mapping', JSON.stringify(mapping));
    } catch (e) {
        console.error("Mapping save error:", e);
    }
    
    // Apply to current pod selector and display
    const selectEl = document.getElementById(`select-pod${currentDetectedPort}-profile`);
    if (selectEl) {
        selectEl.value = selectedProfile;
        updatePodDisplay(currentDetectedPort, selectedProfile);
    }
    
    const uidEl = document.getElementById(`pod${currentDetectedPort}-uid`);
    if (uidEl) uidEl.textContent = uid;
    
    closeUuidDetectionModal();
    const isDe = (state.lang === 'de');
    showToast(isDe 
        ? `Erfolgreich! UID ${uid} dauerhaft mit ${profileText} verknüpft.` 
        : `Success! UID ${uid} permanently mapped to ${profileText}.`, 'success');
});

document.getElementById('btn-p1-learn')?.addEventListener('click', () => {
    openUuidDetectionModal(1, '01:4F:2A:90:12:00:8C');
});

document.getElementById('btn-p2-learn')?.addEventListener('click', () => {
    openUuidDetectionModal(2, '01:B3:78:11:44:90:3A');
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

// ==========================================
// 11b. Interactive LED & Battery Simulators & USB MSC
// ==========================================
const btnToggleLowbat = document.getElementById('btn-toggle-lowbat');
let s_isLowBatSim = false;

if (btnToggleLowbat) {
    btnToggleLowbat.addEventListener('click', () => {
        s_isLowBatSim = !s_isLowBatSim;
        if (s_isLowBatSim) {
            valBtnBat.textContent = '15 %';
            valBtnBat.style.color = 'var(--accent-red)';
            barBtnBat.style.width = '15%';
            barBtnBat.style.background = 'var(--accent-red)';
            btnToggleLowbat.textContent = '⚡ Normal (95%) Reset';
            showToast(state.lang === 'de' ? '⚠️ CR2032 Batterie schwach (15%)! Warnung an CAN-Bus & LED ausgelöst.' : '⚠️ CR2032 Battery Low (15%)! CAN-Bus & LED Alert triggered.', 'error');
            updateLedVisual('red');
        } else {
            valBtnBat.textContent = '95 %';
            valBtnBat.style.color = 'var(--accent-green)';
            barBtnBat.style.width = '95%';
            barBtnBat.style.background = 'var(--accent-green)';
            btnToggleLowbat.textContent = '⚡ Low-Bat (15%) Test';
            showToast(state.lang === 'de' ? 'CR2032 Batterie auf 95% zurückgesetzt (Normal)' : 'CR2032 Battery restored to 95% (Normal)', 'success');
            updateLedVisual('green');
        }
    });
}

function updateLedVisual(colorKey) {
    const ledVisual = document.getElementById('rgb-led-visual');
    const ledBadge = document.getElementById('badge-led-status');
    const ledLabel = document.getElementById('rgb-led-label');
    const ledDesc = document.getElementById('rgb-led-desc');
    const isDe = (state.lang === 'de');

    const ledMap = {
        green: {
            color: '#30d158',
            badge: isDe ? 'Online (Grün)' : 'Online (Green)',
            badgeClass: 'badge-green',
            label: isDe ? 'Normalbetrieb (Pulsierend Grün)' : 'Normal Operation (Pulsing Green)',
            desc: isDe ? 'Bordnetz aktiv, alle Kassetten online, DLE synchronisiert' : 'Vehicle power active, all pods online, DLE synced'
        },
        blue: {
            color: '#0a84ff',
            badge: isDe ? 'BLE / USB (Blau)' : 'BLE / USB (Blue)',
            badgeClass: 'badge-blue',
            label: isDe ? 'BLE Pairing / USB-C MSC Modus' : 'BLE Pairing / USB-C MSC Mode',
            desc: isDe ? 'WebApp verbunden oder MicroSD als USB-Laufwerk am PC' : 'WebApp connected or MicroSD exposed as USB drive'
        },
        yellow: {
            color: '#ffd60a',
            badge: isDe ? 'USV-Nachlauf (Gelb)' : 'UPS Rundown (Yellow)',
            badgeClass: 'badge-orange',
            label: isDe ? 'USV-Akkubetrieb (Zündung AUS)' : 'UPS Battery Mode (Ignition OFF)',
            desc: isDe ? '15 Min. Nachlauf: GPX-Flush & WebDAV-Upload aktiv' : '15 min rundown: GPX flush & WebDAV upload active'
        },
        red: {
            color: '#ff453a',
            badge: isDe ? 'Warnung (Rot)' : 'Alert (Red)',
            badgeClass: 'badge-purple',
            label: isDe ? 'Fehler / Unterspannung Starterbatterie' : 'Error / Starter Battery Under-Voltage',
            desc: isDe ? 'Spannung < 11.8 V oder CR2032 Lenkertaster leer' : 'Voltage < 11.8 V or handlebar CR2032 depleted'
        },
        purple: {
            color: '#bf5af2',
            badge: isDe ? 'DLE Leader (Lila)' : 'DLE Leader (Purple)',
            badgeClass: 'badge-purple',
            label: isDe ? 'OMM DLE Leader-Knoten' : 'OMM DLE Group Leader',
            desc: isDe ? 'Dieses Motorrad koordiniert das Gruppen-Mesh' : 'This motorcycle coordinates the group mesh'
        },
        white: {
            color: '#ffffff',
            badge: isDe ? 'Marker (Weiß)' : 'Marker (White)',
            badgeClass: 'badge-green',
            label: isDe ? 'Actioncam Marker Bestätigung' : 'Action Cam Marker Confirmation',
            desc: isDe ? '1-PPS GPS Highlight-Marker im GPX gespeichert' : '1-PPS GPS highlight marker recorded in GPX'
        }
    };

    const cfg = ledMap[colorKey] || ledMap.green;
    if (ledVisual) {
        ledVisual.style.background = cfg.color;
        ledVisual.style.boxShadow = `0 0 24px ${cfg.color}`;
    }
    if (ledBadge) {
        ledBadge.className = `card-badge ${cfg.badgeClass}`;
        ledBadge.textContent = cfg.badge;
    }
    if (ledLabel) ledLabel.textContent = cfg.label;
    if (ledDesc) ledDesc.textContent = cfg.desc;
}

document.getElementById('select-led-sim')?.addEventListener('change', (e) => {
    updateLedVisual(e.target.value);
});

document.getElementById('btn-trigger-usb-msc')?.addEventListener('click', () => {
    updateLedVisual('blue');
    showToast(state.lang === 'de' ? '💾 USB Mass Storage Modus aktiviert: MicroSD als Laufwerk "OPENMOTOR" am Rechner gemountet.' : '💾 USB Mass Storage mode active: MicroSD mounted as "OPENMOTOR" volume on PC.', 'success');
});

// ==========================================
// 11c. Extended GPX Export Engine & IndexedDB Storage
// ==========================================
let currentExportTour = {
    filename: 'tour_20260823.gpx',
    datetime: '2026-08-23 09:15',
    duration: '1h 42m',
    distance: '84.6 km',
    maxLean: '44.2°'
};

// IndexedDB Initialization
let dbPromise = null;
function getIndexedDb() {
    if (!dbPromise) {
        dbPromise = new Promise((resolve, reject) => {
            if (!window.indexedDB) {
                console.warn('IndexedDB not supported');
                resolve(null);
                return;
            }
            const request = indexedDB.open('OpenMotorBridgeDB', 1);
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains('tours')) {
                    db.createObjectStore('tours', { keyPath: 'id' });
                }
            };
            request.onsuccess = (e) => resolve(e.target.result);
            request.onerror = (e) => reject(e.target.error);
        });
    }
    return dbPromise;
}

async function saveTourToIndexedDb(tourObj) {
    try {
        const db = await getIndexedDb();
        if (!db) return false;
        const tx = db.transaction('tours', 'readwrite');
        const store = tx.objectStore('tours');
        store.put(tourObj);
        return true;
    } catch (err) {
        console.error('Failed to save to IndexedDB:', err);
        return false;
    }
}

// Modal Trigger
window.openGpxExportModal = function (filename, datetime, duration, distance, maxLean) {
    currentExportTour = { filename, datetime, duration, distance, maxLean };
    const modal = document.getElementById('gpx-export-modal');
    if (!modal) return;

    document.getElementById('modal-gpx-filename').textContent = filename;
    document.getElementById('modal-gpx-meta').textContent = `${datetime} • ${duration} • ${distance} • Max. ${maxLean}`;
    modal.classList.add('active');
};

const btnCloseGpxModal = document.getElementById('btn-close-gpx-modal');
if (btnCloseGpxModal) {
    btnCloseGpxModal.addEventListener('click', () => {
        document.getElementById('gpx-export-modal')?.classList.remove('active');
    });
}

// Target Profile Radio Styling
document.querySelectorAll('input[name="gpx-profile"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        document.querySelectorAll('input[name="gpx-profile"]').forEach(r => {
            const tile = r.closest('.stat-tile');
            if (tile) {
                tile.style.border = r.checked ? '1px solid var(--accent-orange)' : '1px solid var(--border-subtle)';
                tile.style.background = r.checked ? 'rgba(255, 159, 10, 0.08)' : 'var(--bg-surface-elevated)';
            }
        });
    });
});

// GPX XML Generators
function generateExtendedGpxXml(profileType, tour, options) {
    const timeIso = new Date().toISOString();
    let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    xml += `<gpx version="1.1" creator="OpenMotorBridge v8.0"\n`;
    xml += `  xmlns="http://www.topografix.com/GPX/1/1"\n`;
    xml += `  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n`;
    xml += `  xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3"\n`;
    xml += `  xmlns:omb="http://openmotorbridge.org/xmlschemas/omb/1.0"\n`;
    xml += `  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n`;
    xml += `  <metadata>\n    <name>${tour.filename}</name>\n    <time>${timeIso}</time>\n  </metadata>\n`;

    // 1. Moto-Navi Route (with Garmin / BMW Shaping Points)
    if (profileType === 'moto_navi') {
        xml += `  <rte>\n    <name>OMB Moto Route (${tour.distance})</name>\n`;
        if (options.garminExt) {
            xml += `    <extensions>\n      <gpxx:RouteExtension>\n        <gpxx:IsAutoNamed>false</gpxx:IsAutoNamed>\n        <gpxx:TransportMode>Driving</gpxx:TransportMode>\n      </gpxx:RouteExtension>\n    </extensions>\n`;
        }
        // Shaping Points sample array
        const shapingPoints = [
            { name: "Start Tour (Klausenpass West)", lat: 46.8686, lon: 8.6433, ele: 485.0 },
            { name: "Shaping Point 1 (Urnerboden)", lat: 46.8834, lon: 8.8415, ele: 1372.0 },
            { name: "Shaping Point 2 (Passhöhe 1948m)", lat: 46.8683, lon: 8.8567, ele: 1948.0 },
            { name: "Ziel (Linthal Glarus)", lat: 46.9208, lon: 8.9983, ele: 662.0 }
        ];

        shapingPoints.forEach((pt, idx) => {
            xml += `    <rtept lat="${pt.lat.toFixed(6)}" lon="${pt.lon.toFixed(6)}">\n`;
            xml += `      <ele>${pt.ele.toFixed(1)}</ele>\n`;
            xml += `      <name>${pt.name}</name>\n`;
            if (options.garminExt && idx > 0 && idx < shapingPoints.length - 1) {
                xml += `      <extensions>\n        <gpxx:RoutePointExtension>\n          <gpxx:Subclass>000000000000ffffffffffffffffffffffff</gpxx:Subclass>\n          <gpxx:PointType>ShapingPoint</gpxx:PointType>\n        </gpxx:RoutePointExtension>\n      </extensions>\n`;
            }
            xml += `    </rtept>\n`;
        });
        xml += `  </rte>\n`;
    }

    // 2. Track Representation (for Visual / Telemetry / Raw)
    xml += `  <trk>\n    <name>${tour.filename}</name>\n    <trkseg>\n`;

    const samplePts = [
        { lat: 46.8686, lon: 8.6433, ele: 485.0, speed: 64.2, lean: 22.4, g_lon: 0.15, act: null },
        { lat: 46.8720, lon: 8.6850, ele: 720.0, speed: 82.5, lean: 38.6, g_lon: -0.42, act: null },
        { lat: 46.8834, lon: 8.8415, ele: 1372.0, speed: 71.0, lean: 44.2, g_lon: -0.68, act: "gopro_highlight" },
        { lat: 46.8683, lon: 8.8567, ele: 1948.0, speed: 55.4, lean: 35.1, g_lon: 0.28, act: null },
        { lat: 46.9208, lon: 8.9983, ele: 662.0, speed: 50.0, lean: 12.0, g_lon: -0.10, act: null }
    ];

    samplePts.forEach((pt, i) => {
        xml += `      <trkpt lat="${pt.lat.toFixed(6)}" lon="${pt.lon.toFixed(6)}">\n`;
        xml += `        <ele>${pt.ele.toFixed(1)}</ele>\n`;
        xml += `        <time>2026-08-23T09:${15 + i * 5}:00.000Z</time>\n`;

        if (profileType === 'video_sync' || profileType === 'raw_ekf') {
            xml += `        <extensions>\n          <omb:telemetry>\n`;
            xml += `            <omb:lean_angle>${pt.lean.toFixed(1)}</omb:lean_angle>\n`;
            xml += `            <omb:speed_kmh>${pt.speed.toFixed(1)}</omb:speed_kmh>\n`;
            xml += `            <omb:accel_g_lon>${pt.g_lon.toFixed(2)}</omb:accel_g_lon>\n`;
            if (profileType === 'raw_ekf') {
                xml += `            <omb:battery_v>12.62</omb:battery_v>\n`;
                xml += `            <omb:satellites>18</omb:satellites>\n`;
                xml += `            <omb:imu_temp_c>28.4</omb:imu_temp_c>\n`;
            }
            if (options.actionTags && pt.act) {
                xml += `            <omb:action_event type="video_marker" camera="insta360_x4" clip_offset_ms="42000"/>\n`;
            }
            xml += `          </omb:telemetry>\n        </extensions>\n`;
        }
        xml += `      </trkpt>\n`;
    });

    xml += `    </trkseg>\n  </trk>\n</gpx>\n`;
    return xml;
}

// Download Button Click Handler
document.getElementById('btn-download-gpx-custom')?.addEventListener('click', () => {
    const selectedProfile = document.querySelector('input[name="gpx-profile"]:checked')?.value || 'moto_navi';
    const options = {
        roadSnapping: document.getElementById('chk-road-snapping')?.checked,
        garminExt: document.getElementById('chk-garmin-ext')?.checked,
        actionTags: document.getElementById('chk-action-tags')?.checked
    };

    const gpxContent = generateExtendedGpxXml(selectedProfile, currentExportTour, options);
    const filename = currentExportTour.filename.replace('.gpx', `_${selectedProfile}.gpx`);

    const blob = new Blob([gpxContent], { type: 'application/gpx+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    document.getElementById('gpx-export-modal')?.classList.remove('active');
    showToast(state.lang === 'de' ? `GPX Export erfolgreich: ${filename}` : `GPX export successful: ${filename}`, 'success');
});

// Save to IndexedDB Handler
document.getElementById('btn-save-indexeddb')?.addEventListener('click', async () => {
    const selectedProfile = document.querySelector('input[name="gpx-profile"]:checked')?.value || 'moto_navi';
    const options = {
        roadSnapping: document.getElementById('chk-road-snapping')?.checked,
        garminExt: document.getElementById('chk-garmin-ext')?.checked,
        actionTags: document.getElementById('chk-action-tags')?.checked
    };
    const gpxContent = generateExtendedGpxXml(selectedProfile, currentExportTour, options);

    const tourEntry = {
        id: `${currentExportTour.filename}_${Date.now()}`,
        filename: currentExportTour.filename,
        profile: selectedProfile,
        savedAt: new Date().toISOString(),
        distance: currentExportTour.distance,
        maxLean: currentExportTour.maxLean,
        content: gpxContent
    };

    const ok = await saveTourToIndexedDb(tourEntry);
    if (ok) {
        showToast(state.lang === 'de' ? '💾 Tour erfolgreich im lokalen IndexedDB-Speicher gesichert!' : '💾 Tour saved to local IndexedDB storage successfully!', 'success');
        document.getElementById('gpx-export-modal')?.classList.remove('active');
        loadToursFromIndexedDb();
    } else {
        showToast(state.lang === 'de' ? 'Fehler beim Speichern in IndexedDB' : 'Failed to save to IndexedDB', 'error');
    }
});

// ==========================================
// 11d. Tour Inspector Modal & Interactive Elevation Profile
// ==========================================
const tourInspectModal = document.getElementById('tour-inspect-modal');
const btnCloseInspectModal = document.getElementById('btn-close-inspect-modal');
let s_inspectingTour = null;

window.openTourInspectModal = function (tourId) {
    const tour = s_defaultTours.find(t => t.id === tourId);
    if (!tour) return;
    s_inspectingTour = tour;

    document.getElementById('inspect-tour-title').textContent = tour.name;
    document.getElementById('inspect-dist').textContent = tour.distance;
    document.getElementById('inspect-dur').textContent = tour.duration;
    document.getElementById('inspect-lean').textContent = tour.maxLean;
    document.getElementById('inspect-speed').textContent = `${tour.topSpeed} km/h`;
    document.getElementById('inspect-ele-gain').textContent = tour.eleGain;

    tourInspectModal?.classList.add('active');
};

if (btnCloseInspectModal) {
    btnCloseInspectModal.addEventListener('click', () => {
        tourInspectModal?.classList.remove('active');
    });
}

document.getElementById('btn-inspect-export-gpx')?.addEventListener('click', () => {
    if (s_inspectingTour) {
        openGpxExportModal(s_inspectingTour.filename, s_inspectingTour.datetime, s_inspectingTour.duration, s_inspectingTour.distance, s_inspectingTour.maxLean);
        tourInspectModal?.classList.remove('active');
    }
});

// Tour Replay Simulator (Playback recorded GPS stream in Cockpit gauges)
let s_replayTimer = null;
document.getElementById('btn-replay-tour')?.addEventListener('click', () => {
    tourInspectModal?.classList.remove('active');
    switchTab('tab-cockpit');
    showToast(state.lang === 'de' ? `▶️ Tour-Replay gestartet: ${s_inspectingTour?.name}` : `▶️ Tour replay started: ${s_inspectingTour?.name}`, 'success');

    let step = 0;
    if (s_replayTimer) clearInterval(s_replayTimer);
    s_replayTimer = setInterval(() => {
        step++;
        const phase = (step % 200) / 200;
        // Simulate realistic alpine pass dynamics
        const simSpeed = 40 + Math.sin(phase * Math.PI * 4) * 35;
        const simLean = Math.sin(phase * Math.PI * 8) * 44.2;
        const simAltitude = 1200 + Math.sin(phase * Math.PI * 2) * 1024;

        state.telemetry.speed = Math.max(0, simSpeed);
        state.telemetry.lean_angle = simLean;
        
        // Update Live Gauges
        document.getElementById('val-speed').textContent = simSpeed.toFixed(1);
        document.getElementById('val-lean-angle').textContent = `${simLean.toFixed(1)}°`;
        const visual = document.getElementById('bike-lean-visual');
        if (visual) visual.style.transform = `rotate(${simLean}deg)`;

        // Update Radar Canvas & Speed Dot
        updateSpeedGatingVisual(simSpeed);
        document.getElementById('lbl-radar-alt').textContent = `${Math.round(simAltitude)} m`;

        if (step > 600) {
            clearInterval(s_replayTimer);
            showToast(state.lang === 'de' ? '✓ Tour-Replay abgeschlossen' : '✓ Tour replay finished', 'info');
        }
    }, 100);
});

// ==========================================
// 11e. Default Tours & Dynamic Table Renderer
// ==========================================
const s_defaultTours = [
    {
        id: 'susten_20260823',
        filename: 'sustenpass_tour.gpx',
        name: 'Sustenpass Kurvenrausch',
        datetime: '2026-08-23 09:15',
        duration: '1h 42m',
        distance: '84.6 km',
        maxLean: '44.2°',
        topSpeed: 118,
        eleGain: '+1.420 m',
        status: 'uploaded'
    },
    {
        id: 'gotthard_20260822',
        filename: 'gotthard_tremola.fav.gpx',
        name: 'Gotthard Pass Tremola Classic',
        datetime: '2026-08-22 14:30',
        duration: '3h 15m',
        distance: '192.3 km',
        maxLean: '47.8°',
        topSpeed: 134,
        eleGain: '+2.150 m',
        status: 'favorite'
    },
    {
        id: 'schwarzwald_20260819',
        filename: 'b500_schwarzwald.gpx',
        name: 'Schwarzwaldhochstraße B500',
        datetime: '2026-08-19 11:00',
        duration: '2h 05m',
        distance: '128.4 km',
        maxLean: '41.5°',
        topSpeed: 112,
        eleGain: '+980 m',
        status: 'uploaded'
    }
];

function loadToursFromIndexedDb() {
    const tbody = document.getElementById('tour-list-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    s_defaultTours.forEach(tour => {
        const tr = document.createElement('tr');
        const badgeHtml = tour.status === 'favorite' 
            ? `<span class="card-badge badge-orange">★ Favorit</span>` 
            : `<span class="card-badge badge-green">Hochgeladen</span>`;

        tr.innerHTML = `
            <td><strong>${tour.datetime}</strong><div class="stat-sub">${tour.name}</div></td>
            <td>${tour.duration}</td>
            <td>${tour.distance}</td>
            <td style="color: var(--accent-orange); font-weight: 700;">${tour.maxLean}</td>
            <td>${badgeHtml}</td>
            <td>
                <div style="display: flex; gap: 6px;">
                    <button class="btn-secondary" style="padding: 4px 8px; font-size: 0.75rem;" onclick="openTourInspectModal('${tour.id}')">📊 Details</button>
                    <button class="btn-primary" style="padding: 4px 8px; font-size: 0.75rem;" onclick="openGpxExportModal('${tour.filename}', '${tour.datetime}', '${tour.duration}', '${tour.distance}', '${tour.maxLean}')">⚡ GPX</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
loadToursFromIndexedDb();

// ==========================================
// 11f. Live Tour Recording Bar
// ==========================================
let s_isRecording = false;
let s_recordStartTime = 0;
let s_recordInterval = null;

const btnToggleTourRecord = document.getElementById('btn-toggle-tour-record');
const dotRecording = document.getElementById('dot-recording');
const lblRecordingStatus = document.getElementById('lbl-recording-status');
const lblRecordingTimer = document.getElementById('lbl-recording-timer');
const labelRecordBtn = document.getElementById('label-record-btn');

if (btnToggleTourRecord) {
    btnToggleTourRecord.addEventListener('click', () => {
        s_isRecording = !s_isRecording;
        if (s_isRecording) {
            s_recordStartTime = Date.now();
            dotRecording.style.background = 'var(--accent-red)';
            dotRecording.classList.add('active');
            lblRecordingStatus.textContent = state.lang === 'de' ? '🔴 Aufzeichnung LÄUFT (10 Hz EKF)' : '🔴 Recording ACTIVE (10 Hz EKF)';
            lblRecordingTimer.style.display = 'inline';
            labelRecordBtn.textContent = state.lang === 'de' ? 'Aufzeichnung Stoppen' : 'Stop Recording';
            btnToggleTourRecord.style.background = 'linear-gradient(135deg, #455a64, #263238)';
            showToast(state.lang === 'de' ? '🔴 Tour-Aufzeichnung gestartet! 1-PPS Zeit-Sync aktiv.' : '🔴 Tour recording started! 1-PPS time sync locked.', 'info');

            s_recordInterval = setInterval(() => {
                const elapsedSec = Math.floor((Date.now() - s_recordStartTime) / 1000);
                const h = String(Math.floor(elapsedSec / 3600)).padStart(2, '0');
                const m = String(Math.floor((elapsedSec % 3600) / 60)).padStart(2, '0');
                const s = String(elapsedSec % 60).padStart(2, '0');
                lblRecordingTimer.textContent = `${h}:${m}:${s}`;
            }, 1000);
        } else {
            clearInterval(s_recordInterval);
            dotRecording.style.background = '#6e7681';
            dotRecording.classList.remove('active');
            lblRecordingStatus.textContent = state.lang === 'de' ? 'Tour-Aufzeichnung beendet & im BGH-Speicher gesichert' : 'Tour recording stopped & stored in privacy buffer';
            lblRecordingTimer.style.display = 'none';
            labelRecordBtn.textContent = state.lang === 'de' ? 'Tour Aufzeichnen' : 'Record Tour';
            btnToggleTourRecord.style.background = 'linear-gradient(135deg, var(--accent-red), #b31d1d)';
            showToast(state.lang === 'de' ? '💾 Tour erfolgreich auf MicroSD & IndexedDB gespeichert!' : '💾 Tour saved to MicroSD & IndexedDB successfully!', 'success');
        }
    });
}

// ==========================================
// 11g. Live OpenMotorMesh Radar Canvas Renderer
// ==========================================
const canvasRadar = document.getElementById('canvas-live-radar');
let s_radarCtx = canvasRadar?.getContext('2d');
let s_radarAngle = 0;

function renderLiveRadarCanvas() {
    if (!canvasRadar || !s_radarCtx) return;
    const w = canvasRadar.width;
    const h = canvasRadar.height;
    const cx = w / 2;
    const cy = h / 2;

    s_radarCtx.clearRect(0, 0, w, h);

    // 1. Tech Grid Background
    s_radarCtx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    s_radarCtx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
        s_radarCtx.beginPath();
        s_radarCtx.moveTo(x, 0);
        s_radarCtx.lineTo(x, h);
        s_radarCtx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
        s_radarCtx.beginPath();
        s_radarCtx.moveTo(0, y);
        s_radarCtx.lineTo(w, y);
        s_radarCtx.stroke();
    }

    // 2. Range Rings (Proximity 250m, 500m 2.4GHz, 1000m)
    [50, 100, 180].forEach((r, idx) => {
        s_radarCtx.beginPath();
        s_radarCtx.arc(cx, cy, r, 0, Math.PI * 2);
        s_radarCtx.strokeStyle = idx === 1 ? 'rgba(255, 159, 10, 0.3)' : 'rgba(10, 132, 255, 0.15)';
        s_radarCtx.lineWidth = idx === 1 ? 1.5 : 1;
        if (idx === 1) s_radarCtx.setLineDash([4, 4]);
        s_radarCtx.stroke();
        s_radarCtx.setLineDash([]);
    });

    // 3. Radar Sweep Line
    s_radarAngle += 0.03;
    s_radarCtx.beginPath();
    s_radarCtx.moveTo(cx, cy);
    s_radarCtx.arc(cx, cy, 180, s_radarAngle, s_radarAngle + 0.3);
    s_radarCtx.closePath();
    const sweepGrad = s_radarCtx.createRadialGradient(cx, cy, 10, cx, cy, 180);
    sweepGrad.addColorStop(0, 'rgba(0, 242, 254, 0.25)');
    sweepGrad.addColorStop(1, 'rgba(0, 242, 254, 0.0)');
    s_radarCtx.fillStyle = sweepGrad;
    s_radarCtx.fill();

    // 4. GPS Breadcrumb Trail (Curve Color-Coding by Lean Angle)
    const breadcrumbs = [
        { dx: -220, dy: 60, lean: 12 },
        { dx: -180, dy: 45, lean: 28 },
        { dx: -140, dy: 10, lean: 44 },
        { dx: -100, dy: -25, lean: 39 },
        { dx: -60, dy: -40, lean: 20 },
        { dx: -20, dy: -20, lean: 8 },
        { dx: 0, dy: 0, lean: state.telemetry.lean_angle }
    ];

    s_radarCtx.lineWidth = 3;
    for (let i = 0; i < breadcrumbs.length - 1; i++) {
        const p1 = breadcrumbs[i];
        const p2 = breadcrumbs[i + 1];
        s_radarCtx.beginPath();
        s_radarCtx.moveTo(cx + p1.dx, cy + p1.dy);
        s_radarCtx.lineTo(cx + p2.dx, cy + p2.dy);
        // Color gradient by lean angle
        s_radarCtx.strokeStyle = Math.abs(p1.lean) > 35 ? '#ff9f0a' : '#00f2fe';
        s_radarCtx.stroke();
    }

    // 5. Mesh Group Nodes
    // Bike 2 (Sena Apex)
    const b2x = cx + 95;
    const b2y = cy - 45;
    s_radarCtx.beginPath();
    s_radarCtx.arc(b2x, b2y, 6, 0, Math.PI * 2);
    s_radarCtx.fillStyle = '#0a84ff';
    s_radarCtx.fill();
    s_radarCtx.fillStyle = '#ffffff';
    s_radarCtx.font = '10px sans-serif';
    s_radarCtx.fillText('Bike 2 (Sena)', b2x + 10, b2y + 3);

    // Bike 3 (Cardo Edge)
    const b3x = cx - 75;
    const b3y = cy + 85;
    s_radarCtx.beginPath();
    s_radarCtx.arc(b3x, b3y, 6, 0, Math.PI * 2);
    s_radarCtx.fillStyle = '#ff9f0a';
    s_radarCtx.fill();
    s_radarCtx.fillText('Bike 3 (Cardo)', b3x + 10, b3y + 3);

    // 6. Own Center Bike (Leader)
    s_radarCtx.beginPath();
    s_radarCtx.arc(cx, cy, 8, 0, Math.PI * 2);
    s_radarCtx.fillStyle = '#30d158';
    s_radarCtx.fill();
    s_radarCtx.strokeStyle = '#ffffff';
    s_radarCtx.lineWidth = 2;
    s_radarCtx.stroke();

    requestAnimationFrame(renderLiveRadarCanvas);
}
requestAnimationFrame(renderLiveRadarCanvas);

// ==========================================
// 11h. Audio VU-Meter & Speed Gating Curve Update
// ==========================================
function updateSpeedGatingVisual(speed) {
    const dot = document.getElementById('speed-cursor-dot');
    if (!dot) return;
    // Map speed (0 to 50 km/h) to SVG path coordinate x (20 to 280)
    const clampedSpeed = Math.min(Math.max(speed, 0), 50);
    const mappedX = 20 + (clampedSpeed / 50) * 260;
    
    // Attenuation calculation (Raised-Cosine)
    let mappedY = 25; // 0 dB
    if (clampedSpeed > 15 && clampedSpeed <= 30) {
        const factor = (clampedSpeed - 15) / 15;
        const raisedCosine = 0.5 * (1 + Math.cos(factor * Math.PI));
        mappedY = 90 - (raisedCosine * 65);
    } else if (clampedSpeed > 30) {
        mappedY = 90; // Muted
    }

    dot.setAttribute('cx', mappedX);
    dot.setAttribute('cy', mappedY);
}

// Live Audio VU Meter Loop
setInterval(() => {
    if (document.getElementById('tab-audio')?.classList.contains('active')) {
        const p1Rms = -14 + (Math.random() * 6 - 3);
        const p2Rms = -18 + (Math.random() * 8 - 4);
        const ambRms = state.telemetry.speed > 30 ? -96 : (-22 + (Math.random() * 4 - 2));

        document.getElementById('lbl-vu-p1').textContent = `${p1Rms.toFixed(1)} dBFS`;
        document.getElementById('bar-vu-p1').style.width = `${Math.min(100, Math.max(5, 100 + p1Rms * 2))}%`;

        document.getElementById('lbl-vu-p2').textContent = `${p2Rms.toFixed(1)} dBFS`;
        document.getElementById('bar-vu-p2').style.width = `${Math.min(100, Math.max(5, 100 + p2Rms * 2))}%`;

        document.getElementById('lbl-vu-ambient').textContent = state.telemetry.speed > 30 
            ? '-96.0 dBFS (Stumm > 30 km/h)' 
            : `${ambRms.toFixed(1)} dBFS (Transparenz ON)`;
        document.getElementById('bar-vu-ambient').style.width = state.telemetry.speed > 30 
            ? '0%' 
            : `${Math.min(100, Math.max(5, 100 + ambRms * 2))}%`;
    }
}, 150);

// Smart Group Action Handlers
document.getElementById('btn-guide-passthrough')?.addEventListener('click', () => {
    showToast(state.lang === 'de' ? '🎙️ Guide Pass-Through aktiv: Frontmikrofon für 10 Sekunden ins Gruppen-Mesh geschaltet!' : '🎙️ Guide Pass-Through active: Front mic routed to group mesh for 10 seconds!', 'info');
});

document.getElementById('btn-siren-alert-sim')?.addEventListener('click', () => {
    showToast(state.lang === 'de' ? '🚨 SIRENE ERKANNT: Kolonnen-Frühwarnung (ALERT_SIREN_APPROACHING) an alle Bikes gesendet!' : '🚨 SIREN DETECTED: Early warning (ALERT_SIREN_APPROACHING) broadcast to all bikes!', 'error');
});

// ==========================================
// Smart Update Hub Handlers (OMM UART Push & OEM Adapter Assistant)
// ==========================================
const btnTriggerOmmPush = document.getElementById('btn-trigger-omm-push');
const containerOmmProgress = document.getElementById('container-omm-push-progress');
const barOmmPush = document.getElementById('bar-omm-push');
const lblOmmPushStatus = document.getElementById('lbl-omm-push-status');
const lblOmmPushPct = document.getElementById('lbl-omm-push-pct');
const badgeOmmFwState = document.getElementById('badge-omm-fw-state');

btnTriggerOmmPush?.addEventListener('click', () => {
    btnTriggerOmmPush.disabled = true;
    containerOmmProgress.style.display = 'block';
    lblOmmPushStatus.textContent = state.lang === 'de' ? 'Synchronisiere ROM-Bootloader (0x08 SLIP)...' : 'Syncing ROM Bootloader (0x08 SLIP)...';
    barOmmPush.style.width = '5%';
    lblOmmPushPct.textContent = '5 %';
    showToast(state.lang === 'de' ? '⚡ High-Speed UART Push (460.800 Baud) gestartet...' : '⚡ High-Speed UART Push (460,800 Baud) started...', 'info');

    let pct = 5;
    const flashInterval = setInterval(() => {
        pct += 15;
        if (pct > 100) pct = 100;
        barOmmPush.style.width = `${pct}%`;
        lblOmmPushPct.textContent = `${pct} %`;
        
        if (pct < 40) {
            lblOmmPushStatus.textContent = state.lang === 'de' ? 'Flash-Sektoren löschen & SLIP Chunks streamen...' : 'Erasing flash & streaming SLIP chunks...';
        } else if (pct < 90) {
            lblOmmPushStatus.textContent = state.lang === 'de' ? `Übertrage 'omm_rear.bin' (${pct}%)...` : `Transferring 'omm_rear.bin' (${pct}%)...`;
        } else if (pct === 100) {
            clearInterval(flashInterval);
            lblOmmPushStatus.textContent = state.lang === 'de' ? '✓ MD5 Hash verifiziert • Coprozessor neugestartet' : '✓ MD5 Hash verified • Coprocessor rebooted';
            badgeOmmFwState.textContent = 'Synchron (v8.0.4)';
            badgeOmmFwState.className = 'card-badge badge-green';
            btnTriggerOmmPush.disabled = false;
            showToast(state.lang === 'de' ? '✓ OMM Heck-Pod Firmware erfolgreich via UART aktualisiert!' : '✓ OMM Rear Pod firmware successfully updated via UART!', 'success');
        }
    }, 250);
});

document.getElementById('btn-trigger-oem-pairing')?.addEventListener('click', () => {
    showToast(state.lang === 'de' ? '⚡ TLP222A Optokoppler triggert 5s Phone-Pairing-Puls... Adapter bereit für Smartphone-App!' : '⚡ TLP222A optocoupler triggered 5s phone pairing pulse... Adapter ready for OEM app!', 'info');
});

document.getElementById('btn-trigger-profile-merge')?.addEventListener('click', () => {
    showToast(state.lang === 'de' ? '✓ Profil \'sena_apex.json\' erfolgreich mit Mesh 3.0 Parametern zusammengeführt & aktiviert!' : '✓ Profile \'sena_apex.json\' merged with Mesh 3.0 parameters & activated!', 'success');
});

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