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

private:
    OtaServiceManager();

    bool m_updating;
    esp_ota_handle_t m_ota_handle;
    const esp_partition_t* m_update_partition;
    size_t m_received_bytes;
    size_t m_total_bytes;
};
