from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    tokens_used: int


class LLMProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        """Load the model into memory."""

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 2048) -> LLMResponse:
        """Generate text from prompt. Synchronous (CPU-bound)."""

    @abstractmethod
    def unload(self) -> None:
        """Release model resources."""

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Whether the model is ready."""
