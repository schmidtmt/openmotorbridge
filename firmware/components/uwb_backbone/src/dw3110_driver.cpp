#include "dw3110_driver.h"
#include <string.h>
#include <stdlib.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

static const char *TAG = "DW3110_DRV";

struct dw3110_driver_s {
    dw3110_config_t config;
    spi_device_handle_t spi_dev;
    bool hardware_present;
    bool rx_active;
    uint32_t dev_id;
    
    dw3110_rx_callback_t rx_cb;
    dw3110_tx_done_callback_t tx_cb;
    void *user_ctx;
    
    SemaphoreHandle_t isr_sem;
    uint64_t last_tx_ts;
    uint64_t last_rx_ts;
};

// -----------------------------------------------------------------------------
// SPI Low-Level Helpers
// -----------------------------------------------------------------------------
static esp_err_t dw3110_spi_read(dw3110_driver_t *drv, uint16_t reg_addr, uint8_t *buffer, size_t len) {
    if (!drv->hardware_present || !drv->spi_dev) {
        return ESP_ERR_INVALID_STATE;
    }

    uint8_t tx_hdr[2];
    tx_hdr[0] = (uint8_t)((reg_addr & 0x3F) | 0x00); // Read bit = 0 in header
    tx_hdr[1] = (uint8_t)((reg_addr >> 6) & 0xFF);

    spi_transaction_t t = {};
    t.length = (2 + len) * 8;
    t.rxlength = len * 8;
    t.flags = 0;

    uint8_t *tx_buf = (uint8_t *)malloc(2 + len);
    uint8_t *rx_buf = (uint8_t *)malloc(2 + len);
    if (!tx_buf || !rx_buf) {
        free(tx_buf);
        free(rx_buf);
        return ESP_ERR_NO_MEM;
    }

    tx_buf[0] = tx_hdr[0];
    tx_buf[1] = tx_hdr[1];
    memset(tx_buf + 2, 0, len);

    t.tx_buffer = tx_buf;
    t.rx_buffer = rx_buf;

    esp_err_t err = spi_device_transmit(drv->spi_dev, &t);
    if (err == ESP_OK) {
        memcpy(buffer, rx_buf + 2, len);
    }

    free(tx_buf);
    free(rx_buf);
    return err;
}

static esp_err_t dw3110_spi_write(dw3110_driver_t *drv, uint16_t reg_addr, const uint8_t *buffer, size_t len) {
    if (!drv->hardware_present || !drv->spi_dev) {
        return ESP_ERR_INVALID_STATE;
    }

    uint8_t *tx_buf = (uint8_t *)malloc(2 + len);
    if (!tx_buf) return ESP_ERR_NO_MEM;

    tx_buf[0] = (uint8_t)((reg_addr & 0x3F) | 0x80); // Write bit = 1
    tx_buf[1] = (uint8_t)((reg_addr >> 6) & 0xFF);
    memcpy(tx_buf + 2, buffer, len);

    spi_transaction_t t = {};
    t.length = (2 + len) * 8;
    t.tx_buffer = tx_buf;

    esp_err_t err = spi_device_transmit(drv->spi_dev, &t);
    free(tx_buf);
    return err;
}

static uint32_t dw3110_spi_read32(dw3110_driver_t *drv, uint16_t reg_addr) {
    uint32_t val = 0;
    if (dw3110_spi_read(drv, reg_addr, (uint8_t *)&val, 4) == ESP_OK) {
        return val;
    }
    return 0;
}

static void dw3110_spi_write32(dw3110_driver_t *drv, uint16_t reg_addr, uint32_t val) {
    dw3110_spi_write(drv, reg_addr, (const uint8_t *)&val, 4);
}

// -----------------------------------------------------------------------------
// GPIO ISR Handler
// -----------------------------------------------------------------------------
static void IRAM_ATTR dw3110_gpio_isr(void *arg) {
    dw3110_driver_t *drv = (dw3110_driver_t *)arg;
    if (drv && drv->isr_sem) {
        BaseType_t high_task_wakeup = pdFALSE;
        xSemaphoreGiveFromISR(drv->isr_sem, &high_task_wakeup);
        portYIELD_FROM_ISR(high_task_wakeup);
    }
}

// -----------------------------------------------------------------------------
// Public Driver API Implementation
// -----------------------------------------------------------------------------
esp_err_t dw3110_init(const dw3110_config_t *config, dw3110_driver_t **driver_out) {
    if (!config || !driver_out) {
        return ESP_ERR_INVALID_ARG;
    }

    dw3110_driver_t *drv = (dw3110_driver_t *)calloc(1, sizeof(dw3110_driver_t));
    if (!drv) {
        return ESP_ERR_NO_MEM;
    }

    drv->config = *config;
    drv->isr_sem = xSemaphoreCreateBinary();

    ESP_LOGI(TAG, "Initializing Qorvo DW3110 UWB Transceiver (IEEE 802.15.4z, Ch.5 @ 6.489 GHz)...");

    // 1. Hardware Reset Pin konfigurieren & Puls ausgeben
    if (drv->config.pin_rst != GPIO_NUM_NC) {
        gpio_config_t rst_conf = {};
        rst_conf.pin_bit_mask = (1ULL << drv->config.pin_rst);
        rst_conf.mode = GPIO_MODE_OUTPUT;
        rst_conf.pull_up_en = GPIO_PULLUP_DISABLE;
        rst_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
        gpio_config(&rst_conf);

        gpio_set_level(drv->config.pin_rst, 0); // Assert RST
        vTaskDelay(pdMS_TO_TICKS(5));
        gpio_set_level(drv->config.pin_rst, 1); // Release RST
        vTaskDelay(pdMS_TO_TICKS(10));
    }

    // 2. SPI Device am Host initialisieren
    spi_device_interface_config_t dev_cfg = {};
    dev_cfg.clock_speed_hz = 16 * 1000 * 1000; // 16 MHz Initial SPI Speed
    dev_cfg.mode = 0;                          // SPI Mode 0 (CPOL=0, CPHA=0)
    dev_cfg.spics_io_num = drv->config.pin_cs;
    dev_cfg.queue_size = 4;

    esp_err_t ret = spi_bus_add_device(drv->config.spi_host, &dev_cfg, &drv->spi_dev);
    if (ret != ESP_OK) {
        ESP_LOGW(TAG, "spi_bus_add_device failed (%s). Checking mock operation.", esp_err_to_name(ret));
    }

    // 3. Device-ID auslesen zur HW-Verifikation
    drv->hardware_present = false;
    if (drv->spi_dev) {
        drv->hardware_present = true;
        drv->dev_id = dw3110_spi_read32(drv, DW3110_REG_DEV_ID);
        if ((drv->dev_id & 0xFFFF0000) != (DW3110_DEV_ID_DECA << 16)) {
            ESP_LOGW(TAG, "DW3110 Hardware not detected on SPI bus (Read DEV_ID: 0x%08lX).", (unsigned long)drv->dev_id);
            ESP_LOGW(TAG, "Activating seamless loopback / simulation mock mode for development.");
            drv->hardware_present = false;
            drv->dev_id = 0xDECA0302; // Mock DW3110 ID
        } else {
            ESP_LOGI(TAG, "DW3110 silicon detected! DEV_ID = 0x%08lX (Revision: 0x%02X)",
                     (unsigned long)drv->dev_id, (uint8_t)(drv->dev_id & 0xFF));
        }
    } else {
        ESP_LOGI(TAG, "Running in software emulation mock mode.");
        drv->dev_id = 0xDECA0302;
    }

    // 4. DW3110 HF- & System-Register konfigurieren
    if (drv->hardware_present) {
        // Soft-Reset & Clock-Lock
        dw3110_spi_write32(drv, DW3110_REG_SYS_CTRL, DW3110_SYS_CTRL_TRXOFF);

        // Kanal 5 @ 6.489 GHz konfigurieren
        dw3110_spi_write32(drv, DW3110_REG_CHAN_CTRL, DW3110_CHAN_5_SELECT);

        // BPRF Modus, 6.8 Mbps Datarate, 64 Symbol Präambel für minimale Latenz (< 0.2 ms)
        uint32_t tx_fctrl = DW3110_TX_FCTRL_TXBR_6M8 | DW3110_TX_FCTRL_TR_64 | DW3110_TX_FCTRL_TXPSR_64;
        dw3110_spi_write32(drv, DW3110_REG_TX_FCTRL, tx_fctrl);

        // PAN-ID und Kurzadresse setzen
        uint32_t panadr = ((uint32_t)drv->config.pan_id << 16) | (uint32_t)drv->config.short_addr;
        dw3110_spi_write32(drv, DW3110_REG_PANADR, panadr);

        // Frame Filtering & Auto-ACK aktivieren
        uint32_t sys_cfg = DW3110_SYS_CFG_FFEN | DW3110_SYS_CFG_FFBC | DW3110_SYS_CFG_PHR_6M8 | DW3110_SYS_CFG_FAST_AACK;
        dw3110_spi_write32(drv, DW3110_REG_SYS_CFG, sys_cfg);

        // Interrupts für TXFRS und RXFCG aktivieren
        uint32_t sys_enable = DW3110_SYS_ENABLE_TXFRS | DW3110_SYS_ENABLE_RXFCG | DW3110_SYS_ENABLE_RXFCE;
        dw3110_spi_write32(drv, DW3110_REG_SYS_ENABLE_LO, sys_enable);
    }

    // 5. GPIO IRQ Interrupt-Handler registrieren
    if (drv->config.pin_irq != GPIO_NUM_NC && drv->hardware_present) {
        gpio_config_t irq_conf = {};
        irq_conf.pin_bit_mask = (1ULL << drv->config.pin_irq);
        irq_conf.mode = GPIO_MODE_INPUT;
        irq_conf.pull_up_en = GPIO_PULLUP_DISABLE;
        irq_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;
        irq_conf.intr_type = GPIO_INTR_POSEDGE;
        gpio_config(&irq_conf);

        gpio_isr_handler_add(drv->config.pin_irq, dw3110_gpio_isr, drv);
    }

    *driver_out = drv;
    ESP_LOGI(TAG, "DW3110 Driver ready (PAN: 0x%04X, Addr: 0x%04X, Mode: %s)",
             drv->config.pan_id, drv->config.short_addr,
             drv->hardware_present ? "PHYSICAL_SILICON" : "SIMULATION_LOOPBACK");
    return ESP_OK;
}

bool dw3110_is_hardware_present(dw3110_driver_t *driver) {
    return driver ? driver->hardware_present : false;
}

uint32_t dw3110_read_dev_id(dw3110_driver_t *driver) {
    return driver ? driver->dev_id : 0;
}

void dw3110_set_callbacks(dw3110_driver_t *driver,
                          dw3110_rx_callback_t rx_cb,
                          dw3110_tx_done_callback_t tx_cb,
                          void *user_ctx) {
    if (driver) {
        driver->rx_cb = rx_cb;
        driver->tx_cb = tx_cb;
        driver->user_ctx = user_ctx;
    }
}

esp_err_t dw3110_transmit(dw3110_driver_t *driver, const uint8_t *data, size_t len, bool wait_for_response) {
    if (!driver || !data || len == 0 || len > UWB_BACKBONE_MAX_FRAME_SIZE) {
        return ESP_ERR_INVALID_ARG;
    }

    driver->last_tx_ts = esp_timer_get_time();

    if (driver->hardware_present) {
        // Daten in TX_BUFFER schreiben
        dw3110_spi_write(driver, DW3110_REG_TX_BUFFER, data, len);

        // Frame-Länge aktualisieren (+2 Bytes für DW3110 Auto-FCS CRC)
        uint32_t tx_fctrl = DW3110_TX_FCTRL_TXBR_6M8 | DW3110_TX_FCTRL_TR_64 | DW3110_TX_FCTRL_TXPSR_64 | ((len + 2) & 0x3FF);
        dw3110_spi_write32(driver, DW3110_REG_TX_FCTRL, tx_fctrl);

        // Sende-Trigger
        uint32_t ctrl = DW3110_SYS_CTRL_TXSTRT;
        if (wait_for_response) {
            ctrl |= DW3110_SYS_CTRL_WAIT4RESP | DW3110_SYS_CTRL_RXENAB;
        }
        dw3110_spi_write32(driver, DW3110_REG_SYS_CTRL, ctrl);
    } else {
        // Simulation Mode: Sofortiges Callback auslösen
        if (driver->tx_cb) {
            driver->tx_cb(true, driver->last_tx_ts, driver->user_ctx);
        }
    }

    return ESP_OK;
}

esp_err_t dw3110_start_rx(dw3110_driver_t *driver) {
    if (!driver) return ESP_ERR_INVALID_ARG;

    driver->rx_active = true;
    if (driver->hardware_present) {
        dw3110_spi_write32(driver, DW3110_REG_SYS_CTRL, DW3110_SYS_CTRL_RXENAB);
    }
    return ESP_OK;
}

esp_err_t dw3110_sleep(dw3110_driver_t *driver) {
    if (!driver) return ESP_ERR_INVALID_ARG;

    driver->rx_active = false;
    if (driver->hardware_present) {
        dw3110_spi_write32(driver, DW3110_REG_SYS_CTRL, DW3110_SYS_CTRL_TRXOFF);
    }
    return ESP_OK;
}

void dw3110_isr_handler(dw3110_driver_t *driver) {
    if (!driver) return;
    dw3110_process_events(driver);
}

void dw3110_process_events(dw3110_driver_t *driver) {
    if (!driver || !driver->hardware_present) return;

    // Status-Register lesen
    uint32_t status = dw3110_spi_read32(driver, DW3110_REG_SYS_STATUS_LO);

    // TX Frame Sent
    if (status & DW3110_SYS_STATUS_TXFRS) {
        // Status löschen
        dw3110_spi_write32(driver, DW3110_REG_SYS_STATUS_LO, DW3110_SYS_STATUS_TXFRS);
        uint32_t tx_time_raw = dw3110_spi_read32(driver, DW3110_REG_TX_TIME);
        driver->last_tx_ts = (uint64_t)tx_time_raw;

        if (driver->tx_cb) {
            driver->tx_cb(true, driver->last_tx_ts, driver->user_ctx);
        }
    }

    // RX Frame Check Good (Paket fehlerfrei empfangen)
    if (status & DW3110_SYS_STATUS_RXFCG) {
        // Empfangslänge aus RX_FINFO lesen
        uint32_t rx_finfo = dw3110_spi_read32(driver, DW3110_REG_RX_FINFO);
        size_t rx_len = rx_finfo & DW3110_RX_FINFO_LEN_MASK;

        if (rx_len > 2 && rx_len <= UWB_BACKBONE_MAX_FRAME_SIZE + 2) {
            uint8_t rx_buf[UWB_BACKBONE_MAX_FRAME_SIZE + 4];
            dw3110_spi_read(driver, DW3110_REG_RX_BUFFER, rx_buf, rx_len - 2); // -2 da CRC abgeschnitten wird

            uint32_t rx_time_raw = dw3110_spi_read32(driver, DW3110_REG_RX_TIME);
            driver->last_rx_ts = (uint64_t)rx_time_raw;

            // Geschätzter RSSI-Wert
            int8_t rssi = -75;

            // Status löschen & Receiver wieder scharf schalten
            dw3110_spi_write32(driver, DW3110_REG_SYS_STATUS_LO, DW3110_SYS_STATUS_RXFCG);
            dw3110_spi_write32(driver, DW3110_REG_SYS_CTRL, DW3110_SYS_CTRL_RXENAB);

            if (driver->rx_cb) {
                driver->rx_cb(rx_buf, rx_len - 2, rssi, driver->last_rx_ts, driver->user_ctx);
            }
        }
    }

    // RX Error / Timeout behandeln
    if (status & (DW3110_SYS_STATUS_RXFCE | DW3110_SYS_STATUS_RXRFTO)) {
        dw3110_spi_write32(driver, DW3110_REG_SYS_STATUS_LO, DW3110_SYS_STATUS_RXFCE | DW3110_SYS_STATUS_RXRFTO);
        dw3110_spi_write32(driver, DW3110_REG_SYS_CTRL, DW3110_SYS_CTRL_RXENAB);
    }
}

uint16_t dw3110_compute_twr_distance_cm(uint64_t poll_tx, uint64_t poll_rx,
                                        uint64_t resp_tx, uint64_t resp_rx) {
    if (resp_rx <= poll_tx || resp_tx <= poll_rx) {
        return 0;
    }

    uint64_t round1 = resp_rx - poll_tx;
    uint64_t reply1 = resp_tx - poll_rx;

    if (round1 <= reply1) {
        return 0;
    }

    int64_t tof_units = (int64_t)(round1 - reply1) / 2;
    float tof_ps = (float)tof_units * DW3110_TIME_UNITS_PS;
    float distance_mm = tof_ps * SPEED_OF_LIGHT_MM_PER_PS;
    int32_t distance_cm = (int32_t)(distance_mm / 10.0f);

    if (distance_cm < 0) return 0;
    if (distance_cm > 10000) return 10000;
    return (uint16_t)distance_cm;
}

void dw3110_deinit(dw3110_driver_t *driver) {
    if (!driver) return;

    if (driver->config.pin_irq != GPIO_NUM_NC && driver->hardware_present) {
        gpio_isr_handler_remove(driver->config.pin_irq);
    }

    if (driver->spi_dev) {
        spi_bus_remove_device(driver->spi_dev);
    }

    if (driver->isr_sem) {
        vSemaphoreDelete(driver->isr_sem);
    }

    free(driver);
}
