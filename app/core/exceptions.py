import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class CoachError(Exception):
    """Base exception for AudioCoach."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class LLMError(CoachError):
    """LLM generation failed."""

    def __init__(self, message: str = "Text generation failed"):
        super().__init__(message, status_code=502)


class TTSError(CoachError):
    """TTS synthesis failed."""

    def __init__(self, message: str = "Audio synthesis failed"):
        super().__init__(message, status_code=502)


class ModelNotLoadedError(CoachError):
    """Model not loaded yet."""

    def __init__(self, message: str = "Model not loaded"):
        super().__init__(message, status_code=503)


async def coach_error_handler(request: Request, exc: CoachError) -> JSONResponse:
    logger.error("CoachError: %s (status=%d)", exc.message, exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )
