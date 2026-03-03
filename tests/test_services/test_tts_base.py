import tempfile
from pathlib import Path

from tests.conftest import MockTTSProvider


def test_mock_tts_lifecycle():
    tts = MockTTSProvider()
    assert not tts.is_loaded

    tts.load()
    assert tts.is_loaded

    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "test.wav"
        result = tts.synthesize("Bonjour!", output)
        assert result.audio_path.exists()
        assert result.duration_seconds > 0
        assert result.sample_rate == 22050

    tts.unload()
    assert not tts.is_loaded
