#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

// =============================================================================
// OpenMotorBridge - Universal Group Split Fallback Engine (docs/de/09_firmware_architecture.md)
// Multi-Tier Fallback: Sena/Cardo -> OMM 2.4G (+20dBm) -> LoRa 868 -> PMR446
// =============================================================================

typedef enum {
    GROUP_LIFECYCLE_STANDBY = 0,         // Einzelfahrer / Nicht in Gruppe
    GROUP_LIFECYCLE_MICRO_CLUSTER,       // Tier 1: Privates Heim-Cluster (z. B. 2 Bikes)
    GROUP_LIFECYCLE_PRE_MERGE,           // Am Treffpunkt (Stillstand, Discovery aktiv)
    GROUP_LIFECYCLE_MACRO_ACTIVE,        // Normalbetrieb in Großgruppe (Dual-Layer)
    GROUP_LIFECYCLE_DOUBT_SPLIT,         // Doubt-Timer aktiv (15..30s Kursabweichung)
    GROUP_LIFECYCLE_RESCUE_ESCALATION,   // Verbindungsabbruch: Stufen 1 bis 3
    GROUP_LIFECYCLE_GROUP_PAUSED,        // Kaffeepause (Stillstand < 30m, NVS-Persistenz)
    GROUP_LIFECYCLE_GROUP_LEFT           // Endgültig verlassen / Disperse
} GroupLifecycleState_t;

typedef enum {
    RESCUE_LEVEL_NONE = 0,               // Line-of-Sight Verbindung aktiv
    RESCUE_LEVEL_1_OMM_2G4 = 1,          // > 15s Verlust: OMM 2.4 GHz +20 dBm Hopping
    RESCUE_LEVEL_2_LORA_868 = 2,         // > 45s Verlust: SX1262 LoRa Telemetrie & Bearing
    RESCUE_LEVEL_3_PMR_ANALOG = 3        // > 120s Verlust: PMR446 Analog-TTS Broadcast
} GroupRescueLevel_t;

typedef struct {
    GroupLifecycleState_t lifecycle_state;
    GroupRescueLevel_t    rescue_level;
    uint32_t              connected_members_count;
    uint32_t              time_since_last_contact_ms;
    float                 lead_distance_km;
    float                 lead_bearing_deg;
    char                  lead_guidance_text[64];
    bool                  hfp_call_active;      // Smartphone Anruf aktiv (Mic Mute & PTT Lock)
    bool                  doubt_timer_active;
} GroupStatus_t;

/**
 * @brief Initialisiert die Group Split Fallback & Rescue Engine
 */
esp_err_t group_split_rescue_engine_init(void);

/**
 * @brief Periodischer Update-Tick (z.B. alle 100 ms) mit aktuellen Fahr- und GNSS-Daten
 */
void group_split_update(float speed_kmh, double lat, double lon, float heading_deg);

/**
 * @brief Aktualisiert den Intercom Link-Status (True = Sena/Cardo Intercom empfängt Frames)
 */
void group_split_report_intercom_contact(bool is_contact_ok);

/**
 * @brief Meldet Anrufstatus vom Qualcomm QCC3084 HFP Profil (Mute & PTT-Lock)
 */
void group_split_set_hfp_call_state(bool is_call_active);

/**
 * @brief Speichert den aktuellen Gruppen-Zustand für Kaffeepausen im NVS (vor Tiefschlaf)
 */
esp_err_t group_split_persist_to_nvs(void);

/**
 * @brief Stellt den Gruppen-Zustand nach Zündungs-Kaltstart aus dem NVS wieder her (< 50 ms)
 */
esp_err_t group_split_restore_from_nvs(void);

/**
 * @brief Gibt den aktuellen Gesamtstatus der Group-Engine zurück
 */
GroupStatus_t group_split_get_status(void);

#ifdef __cplusplus
}
#endif
