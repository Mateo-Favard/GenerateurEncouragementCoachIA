import logging
import subprocess
import wave
from pathlib import Path

from app.services.tts.base import TTSProvider, TTSResult

logger = logging.getLogger(__name__)


class PiperProvider(TTSProvider):
    def __init__(
        self,
        model_path: str,
        sample_rate: int = 22050,
        speaker_id: int = 0,
    ):
        self._model_path = model_path
        self._sample_rate = sample_rate
        self._speaker_id = speaker_id
        self._loaded = False

    def load(self) -> None:
        logger.info("Checking Piper binary availability...")
        result = subprocess.run(
            ["piper", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Piper binary not found or broken: {result.stderr}")

        model_path = Path(self._model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"TTS model not found: {self._model_path}")

        self._loaded = True
        logger.info("TTS ready | model=%s", self._model_path)

    def synthesize(self, text: str, output_path: Path) -> TTSResult:
        if not self._loaded:
            raise RuntimeError("TTS not loaded")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Synthesizing audio | text_len=%d output=%s", len(text), output_path)

        cmd = [
            "piper",
            "--model", self._model_path,
            "--output_file", str(output_path),
            "--speaker", str(self._speaker_id),
        ]

        result = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Piper synthesis failed: {result.stderr}")

        if not output_path.exists():
            raise RuntimeError("Piper produced no output file")

        duration = self._get_wav_duration(output_path)
        logger.info("Audio synthesized | duration=%.1fs path=%s", duration, output_path)

        return TTSResult(
            audio_path=output_path,
            duration_seconds=duration,
            sample_rate=self._sample_rate,
        )

    def _get_wav_duration(self, path: Path) -> float:
        with wave.open(str(path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            self._sample_rate = rate
            return frames / rate

    def unload(self) -> None:
        self._loaded = False
        logger.info("TTS unloaded")

    @property
    def is_loaded(self) -> bool:
        return self._loaded
