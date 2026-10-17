#include "cartridge_ble_client.h"
#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "uwb_backbone_types.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "host/ble_gap.h"
#include "host/ble_gatt.h"

static const char *TAG = "CARTRIDGE_BLE";

static CartridgeBleClient* s_client_inst = nullptr;

static void ble_client_host_task(void *param) {
    ESP_LOGI(TAG, "Cartridge NimBLE Central Host Task running.");
    nimble_port_run();
    nimble_port_freertos_deinit();
}

static void on_ble_sync(void) {
    ESP_LOGI(TAG, "✓ Cartridge NimBLE Central Host synced.");
    if (s_client_inst) {
        s_client_inst->trigger_connect();
    }
}

static void on_ble_reset(int reason) {
    ESP_LOGE(TAG, "Cartridge NimBLE Reset (reason=%d)", reason);
}

static int on_gatt_write_cb(uint16_t conn_handle, const struct ble_gatt_error *error,
                            struct ble_gatt_attr *attr, void *arg) {
    if (error->status == 0) {
        ESP_LOGD(TAG, "✓ GATT write successful (Handle: 0x%04X)", attr ? attr->handle : 0);
    } else {
        ESP_LOGW(TAG, "⚠️ GATT write failed: status=%d", error->status);
    }
    return 0;
}

static int on_disc_chr_cb(uint16_t conn_handle, const struct ble_gatt_error *error,
                          const struct ble_gatt_chr *chr, void *arg) {
    auto *client = static_cast<CartridgeBleClient*>(arg);
    if (!client) return 0;

    if (error->status == 0 && chr != nullptr) {
        uint16_t uuid16 = ble_uuid_u16(&chr->uuid.u);
        ESP_LOGI(TAG, "Discovered Characteristic: UUID 0x%04X, Val Handle 0x%04X, Props=0x%02X",
                 uuid16, chr->val_handle, chr->properties);
        if (client->get_config().flavor == BLE_FLAVOR_SENA_RC_GATT) {
            if (uuid16 == 0xFFE1 || (chr->properties & (BLE_GATT_CHR_PROP_WRITE | BLE_GATT_CHR_PROP_WRITE_NO_RSP))) {
                client->set_char_handle(chr->val_handle);
                ESP_LOGI(TAG, "✓ Bound Sena RC GATT Write Characteristic Handle: 0x%04X", chr->val_handle);
            }
        } else {
            if (chr->properties & (BLE_GATT_CHR_PROP_WRITE | BLE_GATT_CHR_PROP_WRITE_NO_RSP)) {
                client->set_char_handle(chr->val_handle);
                ESP_LOGI(TAG, "✓ Bound Intercom Write Characteristic Handle: 0x%04X", chr->val_handle);
            }
        }
    } else if (error->status == BLE_HS_EDONE) {
        ESP_LOGI(TAG, "Characteristic discovery complete.");
    }
    return 0;
}

static int on_disc_svc_cb(uint16_t conn_handle, const struct ble_gatt_error *error,
                          const struct ble_gatt_svc *service, void *arg) {
    auto *client = static_cast<CartridgeBleClient*>(arg);
    if (!client) return 0;

    if (error->status == 0 && service != nullptr) {
        uint16_t uuid16 = ble_uuid_u16(&service->uuid.u);
        ESP_LOGI(TAG, "Discovered GATT Service: 0x%04X (Handles %u..%u)",
                 uuid16, service->start_handle, service->end_handle);

        uint16_t target_uuid = client->get_config().service_uuid;
        if (target_uuid == 0 || uuid16 == target_uuid) {
            ESP_LOGI(TAG, "Target Service 0x%04X matched -> Discovering characteristics...", uuid16);
            ble_gattc_disc_all_chrs(conn_handle, service->start_handle, service->end_handle,
                                    on_disc_chr_cb, arg);
        }
    }
    return 0;
}

static int gap_event_cb(struct ble_gap_event *event, void *arg) {
    auto *client = static_cast<CartridgeBleClient*>(arg);
    if (!client) return 0;

    switch (event->type) {
        case BLE_GAP_EVENT_DISC: {
            struct ble_hs_adv_fields fields;
            int rc = ble_hs_adv_parse_fields(&fields, event->disc.data, event->disc.length_data);
            if (rc != 0) return 0;

            const char *prefix = client->get_config().device_prefix;
            bool match = false;

            if (fields.name != nullptr && fields.name_len > 0) {
                char dev_name[33] = {0};
                size_t cpy_len = fields.name_len < 32 ? fields.name_len : 32;
                memcpy(dev_name, fields.name, cpy_len);
                if (prefix != nullptr && strlen(prefix) > 0 && strstr(dev_name, prefix) != nullptr) {
                    match = true;
                    ESP_LOGI(TAG, "Found target intercom by name '%s'", dev_name);
                }
            }

            // Also check 16-bit Service UUID
            if (!match && fields.uuids16 != nullptr) {
                uint16_t target_uuid = client->get_config().service_uuid;
                for (int i = 0; i < fields.num_uuids16; i++) {
                    if (ble_uuid_u16(&fields.uuids16[i].u) == target_uuid) {
                        match = true;
                        ESP_LOGI(TAG, "Found target intercom by Service UUID 0x%04X", target_uuid);
                        break;
                    }
                }
            }

            if (match) {
                ble_gap_disc_cancel();
                struct ble_gap_conn_params conn_params = {
                    .scan_itvl = 0x0010,
                    .scan_window = 0x0010,
                    .itvl_min = 0x0006, // 7.5 ms fast latency
                    .itvl_max = 0x0010, // 20 ms
                    .latency = 0,
                    .supervision_timeout = 200, // 2000 ms
                    .min_ce_len = 0,
                    .max_ce_len = 0
                };
                ESP_LOGI(TAG, "Connecting to target intercom address...");
                ble_gap_connect(BLE_OWN_ADDR_PUBLIC, &event->disc.addr, 10000, &conn_params, gap_event_cb, arg);
            }
            break;
        }

        case BLE_GAP_EVENT_CONNECT: {
            if (event->connect.status == 0) {
                ESP_LOGI(TAG, "✓ Docked Intercom CONNECTED via BLE (Conn Handle %u)", event->connect.conn_handle);
                client->on_connected(event->connect.conn_handle);
                ble_gattc_disc_all_svcs(event->connect.conn_handle, on_disc_svc_cb, arg);
            } else {
                ESP_LOGW(TAG, "⚠️ Connection attempt failed (status=%d)", event->connect.status);
                client->on_disconnected();
            }
            break;
        }

        case BLE_GAP_EVENT_DISCONNECT: {
            ESP_LOGW(TAG, "⚠️ Docked Intercom DISCONNECTED (reason=%d) -> Engaging Mechatronic fallback!",
                     event->disconnect.reason);
            client->on_disconnected();
            break;
        }

        case BLE_GAP_EVENT_DISC_COMPLETE: {
            client->on_scan_complete();
            break;
        }

        default:
            break;
    }
    return 0;
}

CartridgeBleClient& CartridgeBleClient::instance() {
    static CartridgeBleClient s_instance;
    return s_instance;
}

CartridgeBleClient::CartridgeBleClient()
    : m_initialized(false),
      m_connected(false),
      m_connecting(false),
      m_last_connect_attempt_ms(0),
      m_conn_handle(0),
      m_char_handle(0) {
    memset(&m_config, 0, sizeof(m_config));
    s_client_inst = this;
}

esp_err_t CartridgeBleClient::init() {
    if (m_initialized) return ESP_OK;

    ESP_LOGI(TAG, "Initializing Cartridge Dedicated BLE Central (ESP32-C6 BT 5.3)...");

    int rc = nimble_port_init();
    if (rc != 0) {
        ESP_LOGE(TAG, "Failed to initialize NimBLE port (%d)", rc);
        return ESP_FAIL;
    }

    ble_hs_cfg.sync_cb = on_ble_sync;
    ble_hs_cfg.reset_cb = on_ble_reset;

    nimble_port_freertos_init(ble_client_host_task);

    m_initialized = true;
    m_connected = false;
    m_connecting = false;
    ESP_LOGI(TAG, "✓ Cartridge BLE Central initialized.");
    return ESP_OK;
}

esp_err_t CartridgeBleClient::configure(const CartridgeBleConfig_t &config) {
    memcpy(&m_config, &config, sizeof(CartridgeBleConfig_t));
    ESP_LOGI(TAG, "Configured BLE profile: Flavor=%s, Prefix='%s', UUID=0x%04X, Supported=%s",
             get_ble_flavor_name(m_config.flavor),
             m_config.device_prefix,
             m_config.service_uuid,
             m_config.supported ? "YES" : "NO");

    if (!m_config.supported || m_config.flavor == BLE_FLAVOR_NONE) {
        disconnect();
    } else {
        trigger_connect();
    }
    return ESP_OK;
}

void CartridgeBleClient::trigger_connect() {
    if (!m_config.supported || m_config.flavor == BLE_FLAVOR_NONE) return;
    if (m_connected || m_connecting) return;

    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
    m_last_connect_attempt_ms = now_ms;

    ESP_LOGI(TAG, "Initiating BLE background scan/connect for target '%s' (Flavor: %s)...",
             m_config.device_prefix, get_ble_flavor_name(m_config.flavor));

    struct ble_gap_disc_params disc_params = {
        .itvl = 0x0020,
        .window = 0x0020,
        .filter_policy = 0,
        .limited = 0,
        .passive = 0,
        .filter_duplicates = 1
    };

    m_connecting = true;
    int rc = ble_gap_disc(BLE_OWN_ADDR_PUBLIC, 10000, &disc_params, gap_event_cb, this);
    if (rc != 0) {
        ESP_LOGW(TAG, "ble_gap_disc failed (rc=%d)", rc);
        m_connecting = false;
    }
}

void CartridgeBleClient::disconnect() {
    if (m_connected && m_conn_handle != 0) {
        ESP_LOGI(TAG, "Disconnecting BLE link from intercom.");
        ble_gap_terminate(m_conn_handle, BLE_ERR_REM_USER_CONN_TERM);
        m_connected = false;
        m_connecting = false;
        m_conn_handle = 0;
        m_char_handle = 0;
    }
}

esp_err_t CartridgeBleClient::write_gatt_data(uint16_t handle, const uint8_t *data, uint16_t len) {
    if (!m_connected || handle == 0) {
        return ESP_ERR_INVALID_STATE;
    }
    int rc = ble_gattc_write_flat(m_conn_handle, handle, data, len, on_gatt_write_cb, this);
    if (rc != 0) {
        ESP_LOGW(TAG, "ble_gattc_write_flat failed: rc=%d", rc);
        return ESP_FAIL;
    }
    return ESP_OK;
}

esp_err_t CartridgeBleClient::send_command(uint8_t opcode) {
    if (!m_config.supported || m_config.flavor == BLE_FLAVOR_NONE) {
        return ESP_ERR_NOT_SUPPORTED;
    }

    if (!m_connected) {
        ESP_LOGW(TAG, "BLE link is NOT connected -> Falling back to Mechatronics.");
        return ESP_ERR_INVALID_STATE;
    }

    switch (m_config.flavor) {
        case BLE_FLAVOR_OMM_NATIVE:
            return send_omm_native(opcode);

        case BLE_FLAVOR_SENA_RC_GATT:
            return send_sena_rc_gatt(opcode);

        case BLE_FLAVOR_CARDO_BLE_V2:
            return send_cardo_ble_v2(opcode);

        case BLE_FLAVOR_HID_CONSUMER:
            return send_hid_consumer(opcode);

        default:
            return ESP_ERR_NOT_SUPPORTED;
    }
}

esp_err_t CartridgeBleClient::send_omm_native(uint8_t opcode) {
    uint8_t val = 0;
    switch (opcode) {
        case CARTRIDGE_OPCODE_VOLUME_UP:     val = 1; break;
        case CARTRIDGE_OPCODE_VOLUME_DOWN:   val = 0; break;
        case CARTRIDGE_OPCODE_MESH_TOGGLE:   val = 1; break;
        case CARTRIDGE_OPCODE_OPEN_GROUP_SW: val = 2; break;
        case CARTRIDGE_OPCODE_CHANNEL_NEXT:  val = 1; break;
        case CARTRIDGE_OPCODE_CHANNEL_PREV:  val = 0; break;
        default:
            return ESP_ERR_NOT_SUPPORTED;
    }
    ESP_LOGI(TAG, "OMM Native BLE TX: Opcode 0x%02X -> Handle 0x%04X", opcode, m_char_handle);
    return write_gatt_data(m_char_handle, &val, 1);
}

esp_err_t CartridgeBleClient::send_sena_rc_gatt(uint8_t opcode) {
    uint8_t frame[5] = { 0xAA, 0x55, 0x00, 0x00, 0x00 };

    switch (opcode) {
        case CARTRIDGE_OPCODE_VOLUME_UP:
            frame[2] = 0x03; frame[3] = 0x01; // Vol +
            break;
        case CARTRIDGE_OPCODE_VOLUME_DOWN:
            frame[2] = 0x03; frame[3] = 0x02; // Vol -
            break;
        case CARTRIDGE_OPCODE_MESH_TOGGLE:
            frame[2] = 0x05; frame[3] = 0x01; // Mesh Toggle
            break;
        case CARTRIDGE_OPCODE_OPEN_GROUP_SW:
            frame[2] = 0x06; frame[3] = 0x01; // Group Mesh Toggle
            break;
        case CARTRIDGE_OPCODE_CHANNEL_NEXT:
            frame[2] = 0x07; frame[3] = 0x01; // Channel Next
            break;
        case CARTRIDGE_OPCODE_CHANNEL_PREV:
            frame[2] = 0x07; frame[3] = 0x02; // Channel Prev
            break;
        default:
            return ESP_ERR_NOT_SUPPORTED;
    }

    frame[4] = frame[2] ^ frame[3]; // Checksum
    ESP_LOGI(TAG, "Sena RC GATT TX: [%02X %02X %02X %02X %02X] -> Handle 0x%04X (< 5 ms)",
             frame[0], frame[1], frame[2], frame[3], frame[4], m_char_handle);
    return write_gatt_data(m_char_handle, frame, sizeof(frame));
}

esp_err_t CartridgeBleClient::send_cardo_ble_v2(uint8_t opcode) {
    uint8_t cmd_payload[2] = { 0x00, 0x00 };
    switch (opcode) {
        case CARTRIDGE_OPCODE_VOLUME_UP:     cmd_payload[0] = 0x03; break;
        case CARTRIDGE_OPCODE_VOLUME_DOWN:   cmd_payload[0] = 0x04; break;
        case CARTRIDGE_OPCODE_MESH_TOGGLE:   cmd_payload[0] = 0x05; break; // DMC Mute toggle
        case CARTRIDGE_OPCODE_OPEN_GROUP_SW: cmd_payload[0] = 0x07; break; // Private chat
        default:
            return ESP_ERR_NOT_SUPPORTED;
    }

    ESP_LOGI(TAG, "Cardo BLE v2 TX: Command 0x%02X -> Handle 0x%04X (< 5 ms)", cmd_payload[0], m_char_handle);
    return write_gatt_data(m_char_handle, cmd_payload, 1);
}

esp_err_t CartridgeBleClient::send_hid_consumer(uint8_t opcode) {
    uint16_t usage_id = 0;
    switch (opcode) {
        case CARTRIDGE_OPCODE_VOLUME_UP:   usage_id = 0x00E9; break;
        case CARTRIDGE_OPCODE_VOLUME_DOWN: usage_id = 0x00EA; break;
        case CARTRIDGE_OPCODE_MESH_TOGGLE: usage_id = 0x00CD; break; // Play/Pause
        default:
            return ESP_ERR_NOT_SUPPORTED;
    }

    uint8_t hid_buf[2] = { (uint8_t)(usage_id & 0xFF), (uint8_t)((usage_id >> 8) & 0xFF) };
    ESP_LOGI(TAG, "HID Consumer TX: Usage 0x%04X -> Handle 0x%04X", usage_id, m_char_handle);
    return write_gatt_data(m_char_handle, hid_buf, sizeof(hid_buf));
}

void CartridgeBleClient::update() {
    // Supervision / auto-reconnect watchdog every 5 seconds if disconnected
    if (m_config.supported && m_config.flavor != BLE_FLAVOR_NONE && !m_connected && !m_connecting) {
        uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000ULL);
        if (now_ms - m_last_connect_attempt_ms > 5000) {
            trigger_connect();
        }
    }
}
