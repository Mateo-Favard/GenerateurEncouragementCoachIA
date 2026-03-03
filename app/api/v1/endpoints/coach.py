import asyncio
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.dependencies import get_llm, get_tts
from app.core.exceptions import CoachError, LLMError, TTSError
from app.models.requests import CoachingRequest
from app.services.llm.base import LLMProvider
from app.services.tts.base import TTSProvider
from app.workflow.graph import build_coaching_graph

logger = logging.getLogger(__name__)

router = APIRouter()

_executor = ThreadPoolExecutor(max_workers=settings.max_workers)


def _cleanup_file(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
        logger.debug("Cleaned up temp file: %s", path)
    except OSError as e:
        logger.warning("Failed to cleanup %s: %s", path, e)


@router.post(
    "/coach",
    response_class=FileResponse,
    responses={
        200: {"content": {"audio/wav": {}}, "description": "Audio WAV du coaching"},
        422: {"description": "Validation error"},
        502: {"description": "LLM or TTS failure"},
    },
)
async def generate_coaching(
    request: CoachingRequest,
    background_tasks: BackgroundTasks,
    llm: LLMProvider = Depends(get_llm),
    tts: TTSProvider = Depends(get_tts),
) -> FileResponse:
    request_id = uuid.uuid4().hex[:8]
    logger.info(
        "[%s] Coaching request | theme=%s exercises=%d",
        request_id,
        request.theme,
        len(request.exercises),
    )

    temp_dir = settings.temp_dir
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_path = temp_dir / f"coaching_{request_id}.wav"

    graph = build_coaching_graph(llm, tts, max_tokens=settings.llm_max_tokens)

    initial_state = {
        "exercises": request.exercises,
        "theme": request.theme,
        "duration_hint": request.duration_hint,
        "audio_path": output_path,
    }

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(_executor, graph.invoke, initial_state)

    if result.get("error"):
        error_msg = result["error"]
        logger.error("[%s] Workflow failed: %s", request_id, error_msg)
        if "LLM" in error_msg:
            raise LLMError(error_msg)
        elif "TTS" in error_msg:
            raise TTSError(error_msg)
        else:
            raise CoachError(error_msg)

    logger.info(
        "[%s] Coaching generated | audio_duration=%.1fs text_len=%d",
        request_id,
        result.get("audio_duration_seconds", 0),
        len(result.get("coaching_text", "")),
    )

    background_tasks.add_task(_cleanup_file, output_path)

    return FileResponse(
        path=str(output_path),
        media_type="audio/wav",
        filename=f"coaching_{request.theme}_{request_id}.wav",
    )
