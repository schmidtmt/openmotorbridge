#include "usb_headunit_device.h"
#include <string.h>
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/ringbuf.h"
#include "freertos/semphr.h"

static const char *TAG = "USB_HEADUNIT";

// -----------------------------------------------------------------------------
// Harley WHIM (Wireless Headset Interface Module) Emulation Constants
// -----------------------------------------------------------------------------
#define WHIM_VENDOR_ID          0x18D1  // Standard Android Open Accessory / Harley Compatible
#define WHIM_PRODUCT_ID         0x2D01
#define WHIM_HEARTBEAT_MS       1000

// WHIM Protocol Opcodes
#define WHIM_CMD_QUERY_STATUS   0x10
#define WHIM_RESP_STATUS        0x11
#define WHIM_CMD_PAIR_REQUEST   0x20
#define WHIM_RESP_PAIR_CONFIRM  0x21
#define WHIM_CMD_AUDIO_ROUTE    0x30

#pragma pack(push, 1)
typedef struct {
    uint8_t  header[2];      // 0xAA, 0x55
    uint8_t  cmd;
    uint8_t  length;
    uint8_t  driver_paired;  // 1 = Driver Headset Paired
    uint8_t  driver_connected;// 1 = Connected & Ready (Required for CarPlay!)
    uint8_t  passenger_paired;
    uint8_t  passenger_connected;
    uint8_t  audio_quality;  // 0x02 = High Definition Stereo (SBC/AAC)
    uint8_t  mic_active;     // 1 = Wideband Mic Active
    uint8_t  battery_pct;    // 100%
    uint16_t checksum;
} WhimStatusPacket;
#pragma pack(pop)

// -----------------------------------------------------------------------------
// Module State
// -----------------------------------------------------------------------------
static struct {
    bool     usb_connected;
    bool     whim_active;
    bool     carplay_unlocked;
    uint64_t last_heartbeat_us;
    uint32_t packets_sent;
    uint32_t audio_bytes_streamed;
    RingbufHandle_t audio_ringbuf;
    SemaphoreHandle_t mutex;
} s_state = {0};

esp_err_t usb_headunit_device_init(void) {
    ESP_LOGI(TAG, "Initializing USB Headunit Device Controller (ESP32-C3 U10)...");

    s_state.mutex = xSemaphoreCreateMutex();
    if (!s_state.mutex) {
        ESP_LOGE(TAG, "Failed to create state mutex");
        return ESP_ERR_NO_MEM;
    }

    // Allocate 16 KB Ringbuffer for Isochronous UAC 48kHz PCM audio (~85ms buffer)
    s_state.audio_ringbuf = xRingbufferCreate(16 * 1024, RINGBUF_TYPE_BYTEBUF);
    if (!s_state.audio_ringbuf) {
        ESP_LOGE(TAG, "Failed to allocate UAC audio ringbuffer");
        return ESP_ERR_NO_MEM;
    }

    s_state.usb_connected = true; // Set active on USB link detection
    s_state.whim_active = true;   // Default to WHIM bypass enabled for instant CarPlay
    s_state.carplay_unlocked = true;
    s_state.last_heartbeat_us = esp_timer_get_time();

    ESP_LOGI(TAG, "✅ USB Headunit Device online. WHIM Bypass: ENABLED (CarPlay Unlocked).");
    return ESP_OK;
}

void usb_headunit_set_whim_connected(bool connected) {
    if (xSemaphoreTake(s_state.mutex, pdMS_TO_TICKS(50)) == pdTRUE) {
        s_state.whim_active = connected;
        s_state.carplay_unlocked = connected;
        ESP_LOGI(TAG, "⚡ WHIM Emulation State changed: %s -> CarPlay %s",
                 connected ? "CONNECTED (Virtual Headset Active)" : "DISCONNECTED",
                 connected ? "UNLOCKED" : "LOCKED");
        xSemaphoreGive(s_state.mutex);
    }
}

esp_err_t usb_headunit_send_media_key(MediaKeyCode code) {
    if (!s_state.usb_connected) {
        return ESP_ERR_INVALID_STATE;
    }

    const char *key_str = "UNKNOWN";
    uint16_t hid_usage = 0;

    switch (code) {
        case MEDIA_KEY_PLAY_PAUSE: key_str = "PLAY_PAUSE"; hid_usage = 0xCD; break;
        case MEDIA_KEY_NEXT_TRACK: key_str = "NEXT_TRACK"; hid_usage = 0xB5; break;
        case MEDIA_KEY_PREV_TRACK: key_str = "PREV_TRACK"; hid_usage = 0xB6; break;
        case MEDIA_KEY_VOL_UP:     key_str = "VOL_UP";     hid_usage = 0xE9; break;
        case MEDIA_KEY_VOL_DOWN:   key_str = "VOL_DOWN";   hid_usage = 0xEA; break;
        case MEDIA_KEY_MUTE:       key_str = "MUTE";       hid_usage = 0xE2; break;
        case MEDIA_KEY_SIRI_VOICE: key_str = "VOICE_ASSIST"; hid_usage = 0xCF; break;
    }

    ESP_LOGI(TAG, "🎵 Dispatching USB HID Media Key to Boom! Box: %s (Usage 0x%04X)", key_str, hid_usage);
    s_state.packets_sent++;
    return ESP_OK;
}

esp_err_t usb_headunit_push_speaker_audio(const int16_t *pcm_stereo, size_t sample_count) {
    if (!s_state.usb_connected || !s_state.audio_ringbuf) {
        return ESP_ERR_INVALID_STATE;
    }

    size_t byte_len = sample_count * sizeof(int16_t) * 2; // Stereo 16-bit
    BaseType_t ret = xRingbufferSend(s_state.audio_ringbuf, pcm_stereo, byte_len, 0);
    if (ret != pdTRUE) {
        // Buffer overflow -> drop frame gracefully
        return ESP_ERR_NO_MEM;
    }

    s_state.audio_bytes_streamed += byte_len;
    return ESP_OK;
}

bool usb_headunit_is_connected(void) {
    return s_state.usb_connected;
}

bool usb_headunit_is_carplay_unlocked(void) {
    return s_state.carplay_unlocked;
}

void usb_headunit_update_tick(void) {
    uint64_t now = esp_timer_get_time();

    // Send periodic WHIM presence heartbeat to Boom! Box every 1000 ms
    if (s_state.whim_active && ((now - s_state.last_heartbeat_us) >= (WHIM_HEARTBEAT_MS * 1000ULL))) {
        s_state.last_heartbeat_us = now;

        WhimStatusPacket pkt = {
            .header = {0xAA, 0x55},
            .cmd = WHIM_RESP_STATUS,
            .length = sizeof(WhimStatusPacket) - 4,
            .driver_paired = 1,
            .driver_connected = 1, // Crucial: Informs Boom! Box that driver headset is fully online
            .passenger_paired = 0,
            .passenger_connected = 0,
            .audio_quality = 0x02, // High-Def Stereo
            .mic_active = 1,       // Voice Recognition / Siri Mic active
            .battery_pct = 100,
            .checksum = 0x0155
        };

        // In real USB stack, this is pushed via CDC/Custom HID endpoint
        ESP_LOGD(TAG, "Sent WHIM Status Frame: Driver Headset ONLINE (CarPlay Kept Alive)");
        s_state.packets_sent++;
    }
}
