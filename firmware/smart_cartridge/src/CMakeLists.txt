idf_component_register(
    SRCS
        "main.cpp"
        "cartridge_mechatronics.cpp"
        "cartridge_audio_codec.cpp"
        "cartridge_ble_client.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        esp_timer
        driver
        esp_driver_gpio
        esp_driver_i2c
        esp_driver_i2s
        esp_driver_uart
        nvs_flash
        app_update
        mbedtls
        bt
        uwb_backbone
    WHOLE_ARCHIVE
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-missing-field-initializers -Wno-error=cpp)
