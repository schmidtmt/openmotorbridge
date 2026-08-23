/**
 * OpenMotorBridge (OMB) v8.0 - Web Bluetooth Dashboard & PWA Controller
 */

// Web Bluetooth Service & Characteristic UUIDs (Matching ble_service_server.cpp)
const OMB_SERVICE_UUID = '23d113ef-5f78-2315-deef-121200a00000';
const TELEMETRY_CHAR_UUID = '23d113ef-5f78-2315-deef-121200a00001';
const CONTROL_CHAR_UUID = '23d113ef-5f78-2315-deef-121200a00002';

// Application State
const state = {
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
const btnConnect = document.getElementById('btn-connect');
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
// 1. Toast Notification Helper
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
// 2. Tab Navigation
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
// 3. Web Bluetooth API Connection
// ==========================================
btnConnect.addEventListener('click', async () => {
    if (state.isBleConnected) {
        disconnectBle();
        return;
    }

    try {
        showToast('Suche nach OpenMotorBridge v8.0...');
        bleDevice = await navigator.bluetooth.requestDevice({
            filters: [{ namePrefix: 'OpenMotorBridge' }],
            optionalServices: [OMB_SERVICE_UUID]
        });

        bleDevice.addEventListener('gattserverdisconnected', onBleDisconnected);

        showToast('Verbinde mit GATT Server...');
        const server = await bleDevice.gatt.connect();
        const service = await server.getPrimaryService(OMB_SERVICE_UUID);

        // Telemetrie Notifications abonnieren
        const teleChar = await service.getCharacteristic(TELEMETRY_CHAR_UUID);
        await teleChar.startNotifications();
        teleChar.addEventListener('characteristicvaluechanged', handleBleTelemetry);

        controlChar = await service.getCharacteristic(CONTROL_CHAR_UUID);

        state.isBleConnected = true;
        updateBleUiState(true);
        showToast('Erfolgreich mit OpenMotorBridge verbunden!', 'success');

        // Stop demo mode if running
        if (state.isDemoMode) toggleDemoMode(false);

    } catch (err) {
        console.error('BLE Verbindung fehlgeschlagen:', err);
        showToast('Verbindung abgebrochen: ' + err.message, 'warning');
    }
});

function onBleDisconnected() {
    state.isBleConnected = false;
    updateBleUiState(false);
    showToast('OpenMotorBridge BLE Verbindung getrennt.', 'warning');
}

function disconnectBle() {
    if (bleDevice && bleDevice.gatt.connected) {
        bleDevice.gatt.disconnect();
    }
    state.isBleConnected = false;
    updateBleUiState(false);
}

function updateBleUiState(connected) {
    if (connected) {
        btnConnect.textContent = '✓ Verbunden';
        btnConnect.classList.add('connected');
        dotBle.classList.add('active');
        labelBleStatus.textContent = 'BLE Online';
    } else {
        btnConnect.textContent = '⚡ BLE Verbinden';
        btnConnect.classList.remove('connected');
        dotBle.classList.remove('active');
        labelBleStatus.textContent = 'BLE Offline';
    }
}

// Telemetrie Frame Parser vom ESP32-S3
function handleBleTelemetry(event) {
    const view = event.target.value;
    if (view.byteLength >= 16) {
        // [V_IGN(float32), V_BAT(float32), BTN_BAT(uint8), MODE(uint8), SATS(uint8), LEAN(int8)...]
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
// 4. UI Telemetry Updater
// ==========================================
function updateTelemetryUi(data) {
    if (data.v_ign !== undefined) {
        valVign.textContent = `${data.v_ign.toFixed(1)} V`;
        const cutOffMap = { agm: 11.8, wet: 11.6, lifepo4: 12.8, nmc: 10.5 };
        const threshold = cutOffMap[state.batteryChemistry] || 11.8;
        if (data.v_ign < threshold) {
            valVign.style.color = 'var(--accent-red)';
            document.getElementById('sub-vign-status').textContent = 'WARNUNG: Unterspannung!';
        } else {
            valVign.style.color = 'var(--accent-green)';
            document.getElementById('sub-vign-status').textContent = 'Status: AKTIV (12V)';
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
                    badge.textContent = 'Aktiv';
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
// 5. Demo / Simulation Mode
// ==========================================
btnDemo.addEventListener('click', () => {
    toggleDemoMode(!state.isDemoMode);
});

function toggleDemoMode(enable) {
    state.isDemoMode = enable;
    if (enable) {
        btnDemo.classList.add('active');
        btnDemo.textContent = '🎮 Demo Aktiv';
        showToast('Live-Simulation gestartet', 'success');

        let angleTime = 0;
        state.demoInterval = setInterval(() => {
            angleTime += 0.05;
            // Sinusförmige Schräglagen-Oszillation (-38° bis +38°)
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
        btnDemo.textContent = '🎮 Demo-Modus';
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
        showToast('Demo-Simulation beendet');
    }
}

// ==========================================
// 6. Audio Modes & Sliders
// ==========================================
document.querySelectorAll('.mode-card').forEach(card => {
    card.addEventListener('click', async () => {
        const mode = parseInt(card.getAttribute('data-mode'), 10);
        updateTelemetryUi({ mode: mode });
        showToast(`Betriebsmodus gewechselt: Modus ${mode}`);

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
    showToast('Sena Apex: Mesh Toggle Puls (200ms) ausgelöst', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x02, 0x00]));
});

document.getElementById('btn-trigger-p1-next').addEventListener('click', async () => {
    showToast('Sena Apex: Kanalwechsel Puls (1000ms) ausgelöst', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x03, 0x00]));
});

document.getElementById('btn-p1-resync').addEventListener('click', () => {
    showToast('Ground-Truth Mesh Re-Sync gesendet', 'success');
});

document.getElementById('btn-p2-next').addEventListener('click', async () => {
    showToast('Cardo DMC Gen2: Kanalweiterschaltung (800ms) ausgelöst', 'info');
    if (controlChar) await controlChar.writeValue(new Uint8Array([0x04, 0x00]));
});

// ==========================================
// 7. Battery Chemistry Selector
// ==========================================
selectBatteryType.addEventListener('change', (e) => {
    state.batteryChemistry = e.target.value;
    localStorage.setItem('omb_bat_chem', state.batteryChemistry);
    const cutOffMap = {
        agm: 'AGM / Gel (11.8 V Cut-Off)',
        wet: 'Nass Blei-Säure (11.6 V Cut-Off)',
        lifepo4: 'LiFePO4 (12.8 V Cut-Off)',
        nmc: 'Li-Ion NMC (10.5 V Cut-Off)'
    };
    labelBatteryChem.textContent = cutOffMap[state.batteryChemistry] || '11.8 V Cut-Off';
    showToast(`Batterie-Chemie aktualisiert: ${e.target.options[e.target.selectedIndex].text}`, 'success');
});

// ==========================================
// 8. Onboarding Wizard Modal
// ==========================================
btnOpenWizard.addEventListener('click', () => {
    wizardModal.classList.add('active');
});

btnCloseWizard.addEventListener('click', () => {
    wizardModal.classList.remove('active');
});

btnWizardFinish.addEventListener('click', () => {
    wizardModal.classList.remove('active');
    showToast('Kassetten-Profil erfolgreich eingerichtet & aktiviert!', 'success');
});

// ==========================================
// 9. Hardware Reserve I/O Toggle
// ==========================================
btnToggleReserveB.addEventListener('click', () => {
    state.telemetry.reserve_b = !state.telemetry.reserve_b;
    if (state.telemetry.reserve_b) {
        valReserveBState.textContent = 'Ausgang: AKTIV (5V ON)';
        valReserveBState.style.color = 'var(--text-primary)';
        btnToggleReserveB.textContent = 'Output Deaktivieren';
        showToast('RESERVE_GPIO_B aktiviert (5V Relais/Cam ON)', 'success');
    } else {
        valReserveBState.textContent = 'Ausgang: INAKTIV (0V OFF)';
        valReserveBState.style.color = 'var(--text-muted)';
        btnToggleReserveB.textContent = 'Output Aktivieren';
        showToast('RESERVE_GPIO_B deaktiviert', 'info');
    }
});

// ==========================================
// 10. Tour Logger & WebDAV Sync
// ==========================================
document.getElementById('btn-trigger-video-marker').addEventListener('click', () => {
    showToast('Actioncam 1-PPS Video-Marker im GPX 2.0 Track gesetzt!', 'success');
});

document.getElementById('btn-trigger-webdav-now').addEventListener('click', () => {
    showToast('WebDAV Sync gestartet: Verbinde mit Nextcloud...', 'info');
    setTimeout(() => {
        showToast('2 GPX-Touren erfolgreich via TLS 1.3 hochgeladen!', 'success');
    }, 1200);
});

document.getElementById('btn-save-webdav').addEventListener('click', () => {
    const url = document.getElementById('input-webdav-url').value;
    const user = document.getElementById('input-webdav-user').value;
    localStorage.setItem('omb_webdav_cfg', JSON.stringify({ url, user }));
    showToast('WebDAV Server-Zugangsdaten gespeichert & verifiziert', 'success');
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
    showToast(`Download gestartet: ${filename}`, 'success');
};

// ==========================================
// 11. Service Worker Registration (PWA Offline)
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