# 09 - Firmware Architecture (C++ / FreeRTOS / ESP-IDF v5.x)

## 1. Dual-Core Task Distribution

```mermaid
graph TD
    subgraph Core0 ["Core 0: Communication & I/O Engine"]
        T1["task_ble_server (WebBLE Dashboard)"]
        T2["task_ble_client (Handlebar Remote 0x180F)"]
        T3["task_cartridge_mgr (Dual 1-Wire & Profiles)"]
        T4["task_sdio_logger (4-Bit FAT32 GPX Logger)"]
        T5["task_power_supervisor (ADC KL15/KL30/UPS)"]
        T6["task_webdav_sync (TLS 1.3 Upload on Ignition OFF)"]
        T7["task_gnss_bridge (UART 460.8k to Pod 3)"]
    end

    subgraph Core1 ["Core 1: Real-Time Audio DSP (Deterministic)"]
        A1["I2S DMA Rx (ES8388 Codec ADC)"] --> A2["Raised-Cosine Ducking & Gain Engine"]
        A2 --> A3["I2S DMA Tx (ES8388 Codec DAC)"]
    end
```

## 2. Deterministic FreeRTOS Priorities
- `task_audio_dsp` (Priority 24, Core 1): Dedicated real-time processing.
- `task_gnss_bridge` (Priority 18, Core 0): Fast UART ring buffer drain.
- `task_power_supervisor` (Priority 15, Core 0): 100 ms ADC telemetry sampling.
- `task_sdio_logger` (Priority 10, Core 0): Block writes to SDIO card.
- `task_ble_server` & `task_ble_client` (Priority 8, Core 0): NimBLE event pump.
