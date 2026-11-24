idf_component_register(
    SRCS
        "main.cpp"
        "keyfob_ble.cpp"
        "sx1262_lora.cpp"
        "buzzer_driver.cpp"
        "ws2812b_led.cpp"
        "power_manager.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        esp_timer
        driver
        esp_driver_gpio
        esp_driver_spi
        esp_driver_ledc
        nvs_flash
        esp_adc
        bt
        esp_pm
    WHOLE_ARCHIVE
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-missing-field-initializers -Wno-error=cpp)

