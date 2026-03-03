#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MODELS_DIR="$PROJECT_DIR/models"

echo "=== AudioCoach KeepFit - Model Download ==="

# LLM: Qwen3 4B Q4_K_M
LLM_DIR="$MODELS_DIR/llm"
LLM_FILE="$LLM_DIR/Qwen3-4B-Q4_K_M.gguf"
LLM_URL="https://huggingface.co/Qwen/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q4_K_M.gguf"

mkdir -p "$LLM_DIR"
if [ -f "$LLM_FILE" ]; then
    echo "[LLM] Already downloaded: $LLM_FILE"
else
    echo "[LLM] Downloading Qwen 3.5 4B Q4_K_M..."
    curl -L --progress-bar -o "$LLM_FILE" "$LLM_URL"
    echo "[LLM] Done: $LLM_FILE"
fi

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
echo "LLM: $LLM_FILE ($(du -h "$LLM_FILE" | cut -f1))"
echo "TTS: $TTS_ONNX ($(du -h "$TTS_ONNX" | cut -f1))"
