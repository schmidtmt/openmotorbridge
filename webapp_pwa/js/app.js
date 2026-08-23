// Web Bluetooth Service & Characteristic UUIDs
const OMB_SERVICE_UUID = '0000a000-1212-efde-1523-785fef13d123';
const TELEMETRY_CHAR_UUID = '0000a001-1212-efde-1523-785fef13d123';
const CONTROL_CHAR_UUID = '0000a002-1212-efde-1523-785fef13d123';

let bleDevice = null;
let controlChar = null;

const btnConnect = document.getElementById('btn-connect');
const valVign = document.getElementById('val-vign');
const valVbat = document.getElementById('val-vbat');
const valBtnBat = document.getElementById('val-btn-bat');

// BLE Verbindungsaufbau
btnConnect.addEventListener('click', async () => {
    try {
        bleDevice = await navigator.bluetooth.requestDevice({
            filters: [{ namePrefix: 'OpenMotorBridge' }],
            optionalServices: [OMB_SERVICE_UUID]
        });

        const server = await bleDevice.gatt.connect();
        const service = await server.getPrimaryService(OMB_SERVICE_UUID);

        // Telemetrie Notifications abonnieren
        const teleChar = await service.getCharacteristic(TELEMETRY_CHAR_UUID);
        await teleChar.startNotifications();
        teleChar.addEventListener('characteristicvaluechanged', handleTelemetry);

        controlChar = await service.getCharacteristic(CONTROL_CHAR_UUID);
        btnConnect.textContent = 'Verbunden';
        btnConnect.style.backgroundColor = '#00e676';
    } catch (err) {
        console.error('BLE Verbindung fehlgeschlagen:', err);
    }
});

// Telemetrie-Daten parsen
function handleTelemetry(event) {
    const view = event.target.value;
    // Beispielhafter Frame-Aufbau: [VIGN_MSB, VIGN_LSB, VBAT_MSB, VBAT_LSB, BTN_BAT]
    const vign = (view.getUint16(0, true) / 100).toFixed(1);
    const vbat = (view.getUint16(2, true) / 100).toFixed(2);
    const btnBat = view.getUint8(4);

    valVign.textContent = `${vign} V`;
    valVbat.textContent = `${vbat} V`;
    valBtnBat.textContent = `${btnBat} %`;
}

// Betriebsmodus-Umschaltung
document.querySelectorAll('.mode-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');

        const mode = parseInt(e.target.getAttribute('data-mode'), 10);
        if (controlChar) {
            const payload = new Uint8Array([0x01, mode]); // Command 0x01 = Set Mode
            await controlChar.writeValue(payload);
        }
    });
});

// PWA Service Worker Registrierung
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./service-worker.js');
    });
}