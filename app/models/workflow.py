from pathlib import Path
from typing import TypedDict


class CoachingWorkflowState(TypedDict, total=False):
    # Inputs
    exercises: list[str]
    theme: str
    duration_hint: str

    # After generate_text
    coaching_text: str
    tokens_used: int

    # After synthesize_audio
    audio_path: Path
    audio_duration_seconds: float
    sample_rate: int

    # Error tracking
    error: str | None
