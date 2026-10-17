# OpenMotorBridge - PCBA 07 Smart Keyfob & Silent Pager Firmware
# Target: Nordic Semiconductor nRF52840 (ARM Cortex-M4F @ 64 MHz)
# Toolchain: Zephyr RTOS / Nordic nRF Connect SDK (NCS) / CMake

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(openmotorbridge_smart_keyfob VERSION 1.0.0 LANGUAGES C CXX ASM)

target_sources(app PRIVATE
    src/main.cpp
    src/keyfob_ble.cpp
    src/sx1262_lora.cpp
    src/drv2605l_haptics.cpp
    src/buzzer_driver.cpp
    src/ws2812b_led.cpp
    src/power_manager.cpp
)

target_include_directories(app PRIVATE src)

# Compiler flags for ultra-low-power optimization and modern C++17
target_compile_features(app PRIVATE cxx_std_17)
target_compile_options(app PRIVATE
    -Wall
    -Wextra
    -Os
    -ffunction-sections
    -fdata-sections
)
