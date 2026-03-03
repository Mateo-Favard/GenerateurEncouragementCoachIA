from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "COACH_"}

    # LLM
    llm_model_path: str = "models/llm/Qwen3-4B-Q4_K_M.gguf"
    llm_n_ctx: int = 4096
    llm_n_threads: int = 4
    llm_max_tokens: int = 2048
    llm_temperature: float = 0.7

    # TTS
    tts_model_path: str = "models/tts/fr_FR-siwis-medium.onnx"
    tts_sample_rate: int = 22050
    tts_speaker_id: int = 0

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # Thread pool
    max_workers: int = 4

    # Temp files
    temp_dir: Path = Path("/tmp/audiocoach")


settings = Settings()
