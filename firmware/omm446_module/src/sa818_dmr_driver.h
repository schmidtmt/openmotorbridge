#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "omm446_config.h"

typedef enum {
    SA818_MODE_ANALOG_FM = 0,  // Standard PMR446 Analog FM (12.5 kHz)
    SA818_MODE_DIGITAL_DMR = 1 // Digital DMR Tier I Direct Mode (DMO TDMA)
} Sa818RadioMode_t;

typedef enum {
    SA818_PWR_LOW_0_2W = 0,    // 0.2W ERP (Helmet / SAR-Safe Mode)
    SA818_PWR_HIGH_0_5W = 1    // 0.5W ERP (Bike / Pod Mode, Max PMR446 legal limit)
} Sa818PowerLevel_t;

typedef struct {
    Sa818RadioMode_t mode;
    uint8_t channel;           // 1 .. 16
    double tx_freq_mhz;
    double rx_freq_mhz;
    uint8_t ctcss_index;       // 0 = Off, 1..38 for Analog FM
    uint8_t dmr_color_code;    // 1 .. 16 for Digital DMR Tier I
    uint8_t dmr_slot;          // 1 or 2
    uint8_t squelch_level;     // 1 .. 8 (Default: 3)
    uint8_t volume_level;      // 1 .. 8 (Default: 6)
    Sa818PowerLevel_t power;
    bool is_transmitting;      // PTT active state
    bool is_receiving;         // Carrier / Squelch open
    int8_t last_rssi_dbm;      // S-Meter telemetry
} Sa818State_t;

// Squelch state change callback signature
typedef void (*sa818_squelch_cb_t)(bool carrier_active, void *user_ctx);

class Sa818DmrDriver {
public:
    static Sa818DmrDriver& getInstance() {
        static Sa818DmrDriver instance;
        return instance;
    }

    esp_err_t init();
    esp_err_t connectHandshake();

    // Mode & Channel Selection
    esp_err_t setRadioMode(Sa818RadioMode_t mode);
    esp_err_t setChannel(uint8_t channel); // 1 .. 16
    esp_err_t nextChannel();
    esp_err_t prevChannel();

    // CTCSS / Color Code configuration
    esp_err_t setCtcss(uint8_t ctcss_index);
    esp_err_t setDmrColorCode(uint8_t color_code);

    // Audio & Filter
    esp_err_t setVolume(uint8_t volume_1_to_8);
    esp_err_t setSquelch(uint8_t sq_level_1_to_8);
    esp_err_t setAudioFilters(bool pre_emphasis, bool high_pass, bool low_pass);

    // Sende-Tastung (Hardware PTT) & Power Select
    esp_err_t setPtt(bool active);
    esp_err_t setPowerLevel(Sa818PowerLevel_t level);

    // Telemetrie
    const Sa818State_t& getState() const { return m_state; }
    int8_t pollRssi();

    // Callback-Registrierung für schnellen Squelch-Interrupt
    void registerSquelchCallback(sa818_squelch_cb_t cb, void *user_ctx);

    // ISR-interne Benachrichtigung
    void handleSquelchIsr(bool carrier_active);

private:
    Sa818DmrDriver();
    ~Sa818DmrDriver() = default;

    esp_err_t sendCommand(const char *cmd, char *response_buf, size_t max_len, uint32_t timeout_ms = 500);
    esp_err_t applyChannelConfig();

    Sa818State_t m_state;
    sa818_squelch_cb_t m_squelch_cb;
    void *m_squelch_user_ctx;
    uint32_t m_ptt_start_tick;
    bool m_initialized;
};
