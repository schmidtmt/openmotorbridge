idf_component_register(
    SRCS
        "main.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        esp_timer
        driver
        esp_driver_gpio
        esp_driver_uart
        nvs_flash
        uwb_backbone
    WHOLE_ARCHIVE
)

target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-missing-field-initializers -Wno-error=cpp)
