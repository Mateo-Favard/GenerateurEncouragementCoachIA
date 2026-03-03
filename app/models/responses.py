from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"


class ReadyResponse(BaseModel):
    status: str
    llm_loaded: bool
    tts_loaded: bool


class ErrorResponse(BaseModel):
    error: str


class CoachingMetadata(BaseModel):
    theme: str
    exercises: list[str]
    text_length: int
    audio_duration_seconds: float
