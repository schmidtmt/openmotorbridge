idf_component_register(
    SRCS
        "main.cpp"
        "sa818_dmr_driver.cpp"
        "es8388_codec.cpp"
        "keypad_indicator.cpp"
        "omm446_ble_service.cpp"
        "power_supervisor.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        nvs_flash
        driver
        esp_driver_gpio
        esp_driver_i2c
        esp_driver_i2s
        esp_driver_uart
        esp_adc
        esp_pm
        freertos
        log
        bt
        esp_timer
    WHOLE_ARCHIVE
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-missing-field-initializers -Wno-error=cpp)
