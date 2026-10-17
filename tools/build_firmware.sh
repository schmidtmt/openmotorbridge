#!/usr/bin/env bash
# ==============================================================================
# OpenMotorBridge - Unified Firmware Build & Flash Tool
# ==============================================================================
# Automatically manages toolchain paths (CMake.app, Python 3.14, Ninja, ESP-IDF).
#
# Usage:
#   ./tools/build_firmware.sh [TARGET] [ACTION/ARGS...]
#
# Targets:
#   main_controller (default) | main
#   front_node                | front
#   smart_cartridge           | cartridge
#   radar_submcu              | radar
#   omm_module                | omm
#   omm446_module             | omm446
#   all                       (Builds all 6 ESP-IDF targets sequentially)
#
# Actions:
#   build (default) | flash | monitor | menuconfig | fullclean | size
#
# Examples:
#   ./tools/build_firmware.sh
#   ./tools/build_firmware.sh front_node
#   ./tools/build_firmware.sh main_controller flash -p /dev/cu.usbmodem1101
#   ./tools/build_firmware.sh all
# ==============================================================================

set -e

# Resolve script directory even when invoked through a symlink
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
    DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FIRMWARE_DIR="$REPO_ROOT/firmware"

# Load ESP-IDF environment
ENV_SCRIPT="$SCRIPT_DIR/esp_env.sh"
if [ ! -f "$ENV_SCRIPT" ]; then
    echo "❌ Missing environment script: $ENV_SCRIPT" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$ENV_SCRIPT"

TARGET="${1:-main_controller}"
shift 2>/dev/null || true
IDF_ARGS=("$@")
if [ ${#IDF_ARGS[@]} -eq 0 ]; then
    IDF_ARGS=("build")
fi

# Normalize target aliases
case "$TARGET" in
    main|main_controller)
        TARGET_DIR="$FIRMWARE_DIR/main_controller"
        TARGET_NAME="Main Controller (ESP32-S3)"
        ;;
    front|front_node)
        TARGET_DIR="$FIRMWARE_DIR/front_node"
        TARGET_NAME="Front Node (ESP32-S3)"
        ;;
    cartridge|smart_cartridge)
        TARGET_DIR="$FIRMWARE_DIR/smart_cartridge"
        TARGET_NAME="Smart Cartridge (ESP32-C6)"
        ;;
    radar|radar_submcu)
        TARGET_DIR="$FIRMWARE_DIR/radar_submcu"
        TARGET_NAME="Radar Sub-MCU (ESP32-C6)"
        ;;
    omm|omm_module)
        TARGET_DIR="$FIRMWARE_DIR/omm_module"
        TARGET_NAME="OMM 2.4 GHz Intercom (ESP32-C6)"
        ;;
    omm446|omm446_module)
        TARGET_DIR="$FIRMWARE_DIR/omm446_module"
        TARGET_NAME="OMM 446 MHz Transceiver (ESP32-C6)"
        ;;
    all)
        echo "========================================================================"
        echo "🏍️  OpenMotorBridge - Building ALL Firmware Targets"
        echo "========================================================================"
        TARGETS=(main_controller front_node smart_cartridge radar_submcu omm_module omm446_module)
        FAILED=0
        for t in "${TARGETS[@]}"; do
            echo ""
            echo "▶ Building Target: $t ..."
            if ! "$0" "$t" "${IDF_ARGS[@]}"; then
                echo "❌ Failed building target: $t"
                FAILED=$((FAILED + 1))
            fi
        done
        echo ""
        if [ $FAILED -eq 0 ]; then
            echo "🎉 All firmware targets built successfully!"
            exit 0
        else
            echo "❌ $FAILED target(s) failed to build."
            exit 1
        fi
        ;;
    *)
        echo "❌ Unknown target: $TARGET" >&2
        echo "Supported targets: main_controller, front_node, smart_cartridge, radar_submcu, omm_module, omm446_module, all" >&2
        exit 1
        ;;
esac

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory does not exist: $TARGET_DIR" >&2
    exit 1
fi

echo "------------------------------------------------------------------------"
echo "🛠️  Building Target: $TARGET_NAME"
echo "📁  Directory:       $TARGET_DIR"
echo "⚡  Command:         idf.py ${IDF_ARGS[*]}"
echo "------------------------------------------------------------------------"

cd "$TARGET_DIR"
idf.py "${IDF_ARGS[@]}"

echo ""
echo "✓ Success: $TARGET_NAME [idf.py ${IDF_ARGS[*]}] complete."
