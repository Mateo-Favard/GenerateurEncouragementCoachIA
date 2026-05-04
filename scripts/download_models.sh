#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MODELS_DIR="$PROJECT_DIR/models"

echo "=== AudioCoach KeepFit - Model Download ==="

# TTS: Piper FR siwis-medium
TTS_DIR="$MODELS_DIR/tts"
TTS_ONNX="$TTS_DIR/fr_FR-siwis-medium.onnx"
TTS_JSON="$TTS_DIR/fr_FR-siwis-medium.onnx.json"
TTS_BASE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium"

mkdir -p "$TTS_DIR"
if [ -f "$TTS_ONNX" ]; then
    echo "[TTS] Already downloaded: $TTS_ONNX"
else
    echo "[TTS] Downloading Piper FR siwis-medium..."
    curl -L --progress-bar -o "$TTS_ONNX" "$TTS_BASE_URL/fr_FR-siwis-medium.onnx"
    curl -L --progress-bar -o "$TTS_JSON" "$TTS_BASE_URL/fr_FR-siwis-medium.onnx.json"
    echo "[TTS] Done: $TTS_ONNX"
fi

echo ""
echo "=== All models downloaded ==="
echo "TTS: $TTS_ONNX ($(du -h "$TTS_ONNX" | cut -f1))"
