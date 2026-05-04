# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

AudioCoach KeepFit - FastAPI API that generates French audio coaching for sport exercises. User sends exercises + a theme (pirate, chevalier...), Qwen3.5-0.8B generates motivational text, Piper synthesizes it to WAV audio.

## Commands

Everything runs in Docker. Never use local Python.

```bash
make download-models   # Download LLM (~812MB) + TTS (~60MB) from HuggingFace
make up                # docker compose up --build (starts API on :8000)
make down              # Stop containers
make test              # Run pytest in Docker (uses mock providers, no models needed)
make lint              # Ruff check via Docker
make logs              # docker compose logs -f
```

Single test: `docker compose --profile test run --rm test python -m pytest tests/test_api/test_coach.py::test_coach_returns_wav -v`

Swagger UI: http://localhost:8000/docs

## Architecture

```
POST /api/v1/coach {exercises, theme}
  → LangGraph graph (2 nodes):
    [generate_text] → Qwen3.5-0.8B via llama-cpp-python → coaching text
    [synthesize_audio] → Piper CLI subprocess → WAV file
  → FileResponse (download) → BackgroundTasks cleanup temp file
```

### Provider pattern

`LLMProvider` and `TTSProvider` are abstract base classes (`app/services/*/base.py`). Implementations are `LlamaCppProvider` and `PiperProvider`. Tests use `MockLLMProvider` / `MockTTSProvider` from `tests/conftest.py`.

### Concurrency model

LLM and TTS are synchronous CPU-bound calls. They run via `asyncio.run_in_executor(ThreadPoolExecutor)` to avoid blocking the event loop. Single Uvicorn worker (LLM uses ~812MB RAM).

### Lifespan

Models load at startup in `app/main.py` lifespan context. Providers are stored in `app.state` and injected via `Depends()` from `app/core/dependencies.py`.

### Prompt engineering

`app/services/llm/prompts.py` — system prompt enforces natural spoken French (no markdown, no lists, no stage directions). `LlamaCppProvider._clean_output()` post-processes to strip `<think>` blocks, XML tags, markdown artifacts, and bracketed annotations.

## Key conventions

- Config via pydantic-settings, all env vars prefixed `COACH_` (`app/core/config.py`)
- Dockerfile separates llama-cpp-python compilation in its own layer (long build, cached independently)
- Models are git-ignored, mounted as read-only Docker volume (`./models:/app/models:ro`)
- Generated WAV files are temp files in `/tmp/audiocoach`, cleaned after response
- ChatML prompt format for Qwen3: `<|im_start|>role\ncontent<|im_end|>`
