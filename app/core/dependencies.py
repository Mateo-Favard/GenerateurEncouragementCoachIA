from fastapi import Request

from app.services.llm.base import LLMProvider
from app.services.tts.base import TTSProvider


def get_llm(request: Request) -> LLMProvider:
    return request.app.state.llm_provider


def get_tts(request: Request) -> TTSProvider:
    return request.app.state.tts_provider
