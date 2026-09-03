#include "ota_service_manager.h"
#include "esp_log.h"
#include "esp_system.h"

static const char* TAG = "OTA_MGR";

OtaServiceManager& OtaServiceManager::instance() {
    static OtaServiceManager inst;
    return inst;
}

OtaServiceManager::OtaServiceManager()
    : m_updating(false)
    , m_ota_handle(0)
    , m_update_partition(nullptr)
    , m_received_bytes(0)
    , m_total_bytes(0)
{
}

bool OtaServiceManager::init() {
    const esp_partition_t* running = esp_ota_get_running_partition();
    if (running) {
        ESP_LOGI(TAG, "Current running partition: '%s' at offset 0x%08lX (type %d, subtype %d)",
                 running->label, running->address, running->type, running->subtype);
    }
    confirm_running_partition();
    return true;
}

void OtaServiceManager::confirm_running_partition() {
    esp_ota_img_states_t ota_state;
    const esp_partition_t* running = esp_ota_get_running_partition();

    if (esp_ota_get_state_partition(running, &ota_state) == ESP_OK) {
        if (ota_state == ESP_OTA_IMG_PENDING_VERIFY) {
            ESP_LOGW(TAG, "First boot after OTA! Confirming app health to cancel rollback window...");
            esp_ota_mark_app_valid_cancel_rollback();
            ESP_LOGI(TAG, "New firmware partition marked VALID & ACTIVE.");
        }
    }
}

bool OtaServiceManager::begin_update(size_t image_size) {
    if (m_updating) {
        ESP_LOGW(TAG, "OTA already in progress, aborting previous session.");
        abort_update();
    }

    const esp_partition_t* running = esp_ota_get_running_partition();
    m_update_partition = esp_ota_get_next_update_partition(NULL);

    if (!m_update_partition) {
        ESP_LOGE(TAG, "No valid target OTA partition found!");
        return false;
    }

    ESP_LOGI(TAG, "Beginning OTA update to partition '%s' at 0x%08lX (Expected size: %zu bytes)",
             m_update_partition->label, m_update_partition->address, image_size);

    esp_err_t err = esp_ota_begin(m_update_partition, image_size, &m_ota_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_begin failed: %s", esp_err_to_name(err));
        return false;
    }

    m_updating = true;
    m_received_bytes = 0;
    m_total_bytes = image_size;
    return true;
}

bool OtaServiceManager::write_chunk(const uint8_t* data, size_t len) {
    if (!m_updating || !data || len == 0) return false;

    esp_err_t err = esp_ota_write(m_ota_handle, data, len);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_write failed at offset %zu: %s", m_received_bytes, esp_err_to_name(err));
        abort_update();
        return false;
    }

    m_received_bytes += len;
    return true;
}

bool OtaServiceManager::finalize_and_reboot() {
    if (!m_updating) return false;

    esp_err_t err = esp_ota_end(m_ota_handle);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_end failed: %s", esp_err_to_name(err));
        m_updating = false;
        return false;
    }

    err = esp_ota_set_boot_partition(m_update_partition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "esp_ota_set_boot_partition failed: %s", esp_err_to_name(err));
        m_updating = false;
        return false;
    }

    ESP_LOGI(TAG, "OTA update SUCCESS! Transferred %zu bytes. Next boot target: '%s'. Restarting MCU...",
             m_received_bytes, m_update_partition->label);

    m_updating = false;
    esp_restart();
    return true;
}

void OtaServiceManager::abort_update() {
    if (m_updating) {
        esp_ota_abort(m_ota_handle);
        m_updating = false;
        m_received_bytes = 0;
        m_total_bytes = 0;
        ESP_LOGW(TAG, "OTA session aborted. Existing firmware retained intact.");
    }
}

bool OtaServiceManager::is_updating() const {
    return m_updating;
}

size_t OtaServiceManager::get_received_bytes() const {
    return m_received_bytes;
}

size_t OtaServiceManager::get_total_bytes() const {
    return m_total_bytes;
}
