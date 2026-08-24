#!/usr/bin/env bash
# ==============================================================================
# OpenMotorBridge - Unified Simulation Suite Runner (with auto-managed venv)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

echo "🏍️  OpenMotorBridge Simulation Suite"
echo "────────────────────────────────────────────────────────────────────────"

# Check if Python virtual environment exists, if not create and install dependencies
if [ ! -f "${VENV_DIR}/bin/python" ]; then
    echo "⚙️  Creating Python virtual environment in ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    echo "📦 Installing required dependencies (numpy, scipy, matplotlib)..."
    "${VENV_DIR}/bin/pip" install --upgrade pip --quiet
    "${VENV_DIR}/bin/pip" install -r "${ROOT_DIR}/requirements.txt" --quiet
    echo "✓ Virtual environment ready."
fi

# Execute testbench with venv Python
"${VENV_DIR}/bin/python" "${SCRIPT_DIR}/run_all_simulations.py" "$@"
