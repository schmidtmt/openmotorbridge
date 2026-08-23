#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2s_std.h"
#include "esp_log.h"
#include <math.h>

static const char *TAG = "AUDIO_DSP";

#define SAMPLE_RATE     48000
#define BUFFER_SAMPLES  128
#define DUCKING_ATTACK  0.05f   // Schnelles Absenken
#define DUCKING_RELEASE 0.002f  // Sanftes Zurückblenden

enum OperationMode {
    MODE_STANDARD = 0,
    MODE_SINGLE_RIDER = 1,
    MODE_CRUISE = 2
};

static OperationMode current_mode = MODE_STANDARD;
static float ducking_factor = 1.0f;

void audio_set_operation_mode(OperationMode mode) {
    current_mode = mode;
    ESP_LOGI(TAG, "Audio operating mode switched to: %d", mode);
}

void task_audio_dsp(void *pvParameters) {
    ESP_LOGI(TAG, "Audio DSP Task started on Core 1 (Realtime Priority).");

    int16_t in_p1[BUFFER_SAMPLES];
    int16_t in_p2[BUFFER_SAMPLES];
    int16_t out_mix[BUFFER_SAMPLES];

    while (true) {
        // Dummy Audio-Frame Processing / Raised-Cosine Ducking Engine
        bool nav_active = false; // Wird vom Bluetooth Audio Sink gemeldet

        if (nav_active) {
            // Ducking aktiv: Musik & Intercom dämpfen
            if (ducking_factor > 0.25f) {
                ducking_factor -= DUCKING_ATTACK;
                if (ducking_factor < 0.25f) ducking_factor = 0.25f;
            }
        } else {
            // Ducking lösen: Sanft zurück auf 1.0f
            if (ducking_factor < 1.0f) {
                ducking_factor += DUCKING_RELEASE;
                if (ducking_factor > 1.0f) ducking_factor = 1.0f;
            }
        }

        // Routing-Entscheidungen je nach Modus
        for (int i = 0; i < BUFFER_SAMPLES; i++) {
            if (current_mode == MODE_SINGLE_RIDER) {
                // Port 2 stummschalten
                out_mix[i] = (int16_t)(in_p1[i] * ducking_factor);
            } else if (current_mode == MODE_CRUISE) {
                // Intercom gedämpft, Fokus auf Lautsprecher
                out_mix[i] = (int16_t)((in_p1[i] + in_p2[i]) * 0.5f * ducking_factor);
            } else {
                // Standard: Beide Ports symmetrisch gemischt
                out_mix[i] = (int16_t)((in_p1[i] + in_p2[i]) * ducking_factor);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(5)); // DMA Buffer Tick
    }
}