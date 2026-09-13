#pragma once

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include "esp_ota_ops.h"

class OtaServiceManager {
public:
    static OtaServiceManager& instance();

    bool init();
    void confirm_running_partition();

    bool begin_update(size_t image_size);
    bool write_chunk(const uint8_t* data, size_t len);
    bool finalize_and_reboot();
    void abort_update();

    bool is_updating() const;
    size_t get_received_bytes() const;
    size_t get_total_bytes() const;

    // --- Automated Self-Health & Rollback Validation (Phase 2) ---
    bool is_health_check_pending() const;
    bool is_health_check_passed() const;
    uint32_t get_health_check_remaining_sec() const;
    void update_health_check(uint32_t delta_ms);
    void record_can_activity();
    void record_espnow_activity();

private:
    OtaServiceManager();

    bool m_updating;
    esp_ota_handle_t m_ota_handle;
    const esp_partition_t* m_update_partition;
    size_t m_received_bytes;
    size_t m_total_bytes;

    // Self-Health evaluation state
    bool m_health_pending;
    bool m_health_passed;
    uint32_t m_health_timer_ms;
    uint32_t m_can_frames_seen;
    uint32_t m_espnow_pings_seen;
};
