idf_component_register(
    SRCS
        "main.cpp"
        "usb_headunit_device.cpp"
        "interchip_uart_link.cpp"
        "i2s_audio_bridge.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        driver
        esp_driver_gpio
        esp_driver_uart
        esp_driver_i2s
        esp_timer
        freertos
        ringbuf
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-missing-field-initializers -Wno-error=cpp)

