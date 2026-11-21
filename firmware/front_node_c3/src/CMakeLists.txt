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
        esp_timer
        freertos
        ringbuf
)

