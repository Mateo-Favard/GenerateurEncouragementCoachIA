from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TTSResult:
    audio_path: Path
    duration_seconds: float
    sample_rate: int


class TTSProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        """Load the TTS model."""

    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> TTSResult:
        """Synthesize text to a WAV file. Synchronous (CPU-bound)."""

    @abstractmethod
    def unload(self) -> None:
        """Release model resources."""

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Whether the model is ready."""
