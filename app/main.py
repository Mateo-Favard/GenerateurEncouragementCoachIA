import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.core.config import settings
from app.core.exceptions import CoachError, coach_error_handler
from app.core.logging import setup_logging
from app.services.llm.llamacpp_provider import LlamaCppProvider
from app.services.tts.piper_provider import PiperProvider

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load models
    logger.info("Starting AudioCoach KeepFit...")

    llm = LlamaCppProvider(
        model_path=settings.llm_model_path,
        n_ctx=settings.llm_n_ctx,
        n_threads=settings.llm_n_threads,
        temperature=settings.llm_temperature,
    )
    tts = PiperProvider(
        model_path=settings.tts_model_path,
        sample_rate=settings.tts_sample_rate,
        speaker_id=settings.tts_speaker_id,
    )

    llm.load()
    app.state.llm_provider = llm
    app.state.llm_loaded = True

    tts.load()
    app.state.tts_provider = tts
    app.state.tts_loaded = True

    logger.info("All models loaded, ready to serve")

    yield

    # Shutdown: unload models
    logger.info("Shutting down AudioCoach KeepFit...")
    llm.unload()
    tts.unload()


app = FastAPI(
    title="AudioCoach KeepFit",
    description="API de generation audio de coaching sportif",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_exception_handler(CoachError, coach_error_handler)
app.include_router(api_router)
