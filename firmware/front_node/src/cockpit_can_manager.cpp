#include "cockpit_can_manager.h"
#include "front_node_config.h"
#include "cockpit_switches_manager.h"
#include "esp_log.h"

static const char* TAG = "COCKPIT_CAN";

CockpitCanManager& CockpitCanManager::instance() {
    static CockpitCanManager inst;
    return inst;
}

CockpitCanManager::CockpitCanManager()
    : m_installed(false)
    , m_bus_ok(false)
    , m_state(CAN_STATE_AUTO_SENSING)
    , m_auto_sense_timer_ms(0)
    , m_rx_count(0)
    , m_baud_rate_kbps(250)
{
}

bool CockpitCanManager::init(uint32_t baud_rate_kbps) {
    m_baud_rate_kbps = baud_rate_kbps;
    m_state = CAN_STATE_AUTO_SENSING;
    m_auto_sense_timer_ms = 0;
    m_rx_count = 0;

    // Start in LISTEN-ONLY mode during auto-sensing: prevents error frames or bus-off if J2 is open
    twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(
        PIN_CAN_TX,
        PIN_CAN_RX,
        TWAI_MODE_LISTEN_ONLY
    );
    g_config.rx_queue_len = 32;
    g_config.tx_queue_len = 16;

    twai_timing_config_t t_config;
    if (baud_rate_kbps == 500) {
        t_config = TWAI_TIMING_CONFIG_500KBITS();
    } else {
        t_config = TWAI_TIMING_CONFIG_250KBITS(); // Default Harley HD-LAN
    }

    twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

    esp_err_t err = twai_driver_install(&g_config, &t_config, &f_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "twai_driver_install failed: %s", esp_err_to_name(err));
        m_state = CAN_STATE_DEACTIVATED;
        return false;
    }

    err = twai_start();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "twai_start failed: %s", esp_err_to_name(err));
        m_state = CAN_STATE_DEACTIVATED;
        return false;
    }

    m_installed = true;
    m_bus_ok = true;

    // Initially keep termination open and transceiver silent until bus presence is confirmed
    CockpitSwitchesManager::instance().set_can_termination(false);
    CockpitSwitchesManager::instance().set_can_silent(false);

    ESP_LOGI(TAG, "Cockpit CAN driver initialized in LISTEN-ONLY Auto-Sensing mode (%lu kbps, TX=GPIO%d, RX=GPIO%d)",
             baud_rate_kbps, PIN_CAN_TX, PIN_CAN_RX);
    return true;
}

void CockpitCanManager::update(uint32_t delta_ms) {
    if (m_state == CAN_STATE_AUTO_SENSING) {
        m_auto_sense_timer_ms += delta_ms;
        if (m_auto_sense_timer_ms >= 2500) {
            // Timeout reached without receiving any CAN frames -> J2 is unconnected
            m_state = CAN_STATE_DEACTIVATED;
            CockpitSwitchesManager::instance().set_can_termination(false); // Open 120R termination relay
            CockpitSwitchesManager::instance().set_can_silent(true);       // Set TCAN334G into ultra-low-power Silent mode
            if (m_installed) {
                twai_stop();
            }
            m_bus_ok = false;
            ESP_LOGI(TAG, "Cockpit CAN Auto-Sense: No bus detected at J2 after 2.5s. Port DEACTIVATED (Termination OPEN, Transceiver Silent). Remote CAN via Central Box active.");
        }
    }
}

bool CockpitCanManager::receive_message(CanMessage* msg, TickType_t wait_ticks) {
    if (!m_installed || !msg || m_state == CAN_STATE_DEACTIVATED) return false;

    twai_message_t twai_msg;
    esp_err_t res = twai_receive(&twai_msg, wait_ticks);
    if (res != ESP_OK) {
        return false;
    }

    // First frame received during auto-sensing: Lock into CONNECTED state!
    if (m_state == CAN_STATE_AUTO_SENSING) {
        m_state = CAN_STATE_CONNECTED;
        CockpitSwitchesManager::instance().set_can_termination(true); // Close 120R CPC1017N relay
        CockpitSwitchesManager::instance().set_can_silent(false);     // Normal mode
        ESP_LOGI(TAG, "✨ Cockpit CAN Auto-Sense: Valid CAN frame detected at J2! Port LOCKED as ACTIVE (120R Termination CLOSED).");
    }

    m_rx_count++;
    msg->id = twai_msg.identifier;
    msg->dlc = twai_msg.data_length_code;
    msg->is_extended = (twai_msg.flags & TWAI_MSG_FLAG_EXTD) != 0;
    for (int i = 0; i < twai_msg.data_length_code && i < 8; ++i) {
        msg->data[i] = twai_msg.data[i];
    }
    return true;
}

bool CockpitCanManager::transmit_message(const CanMessage& msg) {
    if (!m_installed || m_state != CAN_STATE_CONNECTED) return false;

    twai_message_t twai_msg = {};
    twai_msg.identifier = msg.id;
    twai_msg.data_length_code = msg.dlc;
    twai_msg.flags = msg.is_extended ? TWAI_MSG_FLAG_EXTD : 0;
    for (int i = 0; i < msg.dlc && i < 8; ++i) {
        twai_msg.data[i] = msg.data[i];
    }

    esp_err_t res = twai_transmit(&twai_msg, pdMS_TO_TICKS(20));
    return (res == ESP_OK);
}

bool CockpitCanManager::is_bus_healthy() const {
    if (!m_installed || m_state == CAN_STATE_DEACTIVATED) return false;
    twai_status_info_t status;
    twai_get_status_info(&status);
    return (status.state == TWAI_STATE_RUNNING);
}
