from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.llm.base import LLMProvider, LLMResponse
from app.services.tts.base import TTSProvider, TTSResult


class MockLLMProvider(LLMProvider):
    def __init__(self):
        self._loaded = False

    def load(self) -> None:
        self._loaded = True

    def generate(self, prompt: str, max_tokens: int = 2048) -> LLMResponse:
        return LLMResponse(
            text="Allez moussaillons! On commence par 20 jumping jacks. Courage!",
            tokens_used=42,
        )

    def unload(self) -> None:
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded


class MockTTSProvider(TTSProvider):
    def __init__(self):
        self._loaded = False

    def load(self) -> None:
        self._loaded = True

    def synthesize(self, text: str, output_path: Path) -> TTSResult:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Write a minimal valid WAV file
        import wave

        samples = np.zeros(22050, dtype=np.int16)  # 1 second of silence
        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            wf.writeframes(samples.tobytes())

        return TTSResult(
            audio_path=output_path,
            duration_seconds=1.0,
            sample_rate=22050,
        )

    def unload(self) -> None:
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded


@pytest.fixture
def mock_llm():
    provider = MockLLMProvider()
    provider.load()
    return provider


@pytest.fixture
def mock_tts():
    provider = MockTTSProvider()
    provider.load()
    return provider


@pytest.fixture
async def client(mock_llm, mock_tts):
    app.state.llm_provider = mock_llm
    app.state.tts_provider = mock_tts
    app.state.llm_loaded = True
    app.state.tts_loaded = True

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
