#include "cockpit_can_manager.h"
#include "front_node_config.h"
#include "esp_log.h"

static const char* TAG = "COCKPIT_CAN";

CockpitCanManager& CockpitCanManager::instance() {
    static CockpitCanManager inst;
    return inst;
}

CockpitCanManager::CockpitCanManager()
    : m_installed(false)
    , m_bus_ok(false)
{
}

bool CockpitCanManager::init(uint32_t baud_rate_kbps) {
    twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(
        PIN_CAN_TX,
        PIN_CAN_RX,
        TWAI_MODE_NORMAL
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
        return false;
    }

    err = twai_start();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "twai_start failed: %s", esp_err_to_name(err));
        return false;
    }

    m_installed = true;
    m_bus_ok = true;
    ESP_LOGI(TAG, "Cockpit CAN driver started successfully (%lu kbps, TX=GPIO5, RX=GPIO4)", baud_rate_kbps);
    return true;
}

bool CockpitCanManager::receive_message(CanMessage* msg, TickType_t wait_ticks) {
    if (!m_installed || !msg) return false;

    twai_message_t twai_msg;
    esp_err_t res = twai_receive(&twai_msg, wait_ticks);
    if (res != ESP_OK) {
        return false;
    }

    msg->id = twai_msg.identifier;
    msg->dlc = twai_msg.data_length_code;
    msg->is_extended = (twai_msg.flags & TWAI_MSG_FLAG_EXTD) != 0;
    for (int i = 0; i < twai_msg.data_length_code && i < 8; ++i) {
        msg->data[i] = twai_msg.data[i];
    }
    return true;
}

bool CockpitCanManager::transmit_message(const CanMessage& msg) {
    if (!m_installed) return false;

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
    if (!m_installed) return false;
    twai_status_info_t status;
    twai_get_status_info(&status);
    return (status.state == TWAI_STATE_RUNNING);
}
