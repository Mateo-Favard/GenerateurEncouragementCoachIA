from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "COACH_"}

    # LLM (OpenRouter)
    openrouter_api_key: str
    openrouter_model: str = "minimax/minimax-m2.5"
    llm_max_tokens: int = 512
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
