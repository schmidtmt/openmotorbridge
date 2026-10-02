#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"
#include "openmotormesh.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    OMM_MESH_DISCONNECTED = 0,
    OMM_MESH_OPEN_GROUP   = 1,
    OMM_MESH_PRIVATE_GROUP = 2,
    OMM_MESH_ROAMING_RESCUE = 3
} OmmMeshState_t;

typedef void (*omm_audio_rx_cb_t)(const int16_t *audio_data, size_t samples, uint8_t sender_id);

esp_err_t omm_transceiver_init(omm_audio_rx_cb_t rx_callback);
esp_err_t omm_transceiver_send_audio(const int16_t *samples, size_t count);
void omm_transceiver_set_ptt(bool ptt_active);
bool omm_transceiver_is_ptt(void);
void omm_transceiver_set_mesh_mode(OmmMeshState_t mode);
OmmMeshState_t omm_transceiver_get_mesh_mode(void);
uint8_t omm_transceiver_get_active_peers(void);

#ifdef __cplusplus
}
#endif
