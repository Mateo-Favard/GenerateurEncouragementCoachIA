from fastapi import APIRouter

from app.api.v1.endpoints import coach, health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router, tags=["health"])
router.include_router(coach.router, tags=["coach"])
