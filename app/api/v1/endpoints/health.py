from fastapi import APIRouter, Request

from app.models.responses import HealthResponse, ReadyResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/ready", response_model=ReadyResponse)
async def ready(request: Request) -> ReadyResponse:
    llm_loaded = getattr(request.app.state, "llm_loaded", False)
    tts_loaded = getattr(request.app.state, "tts_loaded", False)
    status = "ready" if (llm_loaded and tts_loaded) else "loading"
    return ReadyResponse(status=status, llm_loaded=llm_loaded, tts_loaded=tts_loaded)
