#!/usr/bin/env bash
# ==============================================================================
# OpenMotorBridge - ESP-IDF Environment Setup Script (macOS / Linux)
# ==============================================================================
# Usage:
#   source tools/esp_env.sh
#   . tools/esp_env.sh
# ==============================================================================

# Ensure macOS Application and Framework tool paths are prioritized
# 1. CMake.app
if [ -d "/Applications/CMake.app/Contents/bin" ]; then
    export PATH="/Applications/CMake.app/Contents/bin:$PATH"
fi

# 2. Ninja and standard UNIX tools
if [ -d "/usr/local/bin" ]; then
    export PATH="/usr/local/bin:$PATH"
fi

# 3. Python 3.14 framework (matches ~/.espressif/python_env/idf5.5_py3.14_env)
if [ -d "/Library/Frameworks/Python.framework/Versions/3.14/bin" ]; then
    export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"
fi

# 4. Locate ESP-IDF export.sh
IDF_EXPORT=""
if [ -f "$HOME/esp-idf/export.sh" ]; then
    IDF_EXPORT="$HOME/esp-idf/export.sh"
elif [ -n "$IDF_PATH" ] && [ -f "$IDF_PATH/export.sh" ]; then
    IDF_EXPORT="$IDF_PATH/export.sh"
elif [ -f "$HOME/esp/esp-idf/export.sh" ]; then
    IDF_EXPORT="$HOME/esp/esp-idf/export.sh"
else
    # Find any matching export.sh in ~/esp*
    for candidate in "$HOME"/esp*/export.sh "$HOME"/esp/esp-idf*/export.sh; do
        if [ -f "$candidate" ]; then
            IDF_EXPORT="$candidate"
            break
        fi
    done
fi

if [ -z "$IDF_EXPORT" ] || [ ! -f "$IDF_EXPORT" ]; then
    echo "❌ Error: Could not locate ESP-IDF export.sh in $HOME/esp-idf or ~/esp/." >&2
    echo "   Please install ESP-IDF or set IDF_PATH." >&2
    return 1 2>/dev/null || exit 1
fi

# Source ESP-IDF environment cleanly
# shellcheck disable=SC1090
. "$IDF_EXPORT" > /dev/null 2>&1

echo "✓ OpenMotorBridge ESP-IDF Environment Loaded."
echo "  - CMake:  $(which cmake 2>/dev/null || echo 'not found')"
echo "  - Ninja:  $(which ninja 2>/dev/null || echo 'not found')"
echo "  - Python: $(which python3 2>/dev/null || echo 'not found') ($(${IDF_PYTHON_ENV_PATH:-python3} --version 2>/dev/null || python3 --version))"
echo "  - IDF:    ${IDF_PATH:-$HOME/esp-idf} ($(idf.py --version 2>/dev/null || echo 'active'))"
