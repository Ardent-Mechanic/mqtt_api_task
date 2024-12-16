from fastapi import APIRouter

from core.config import settings

from .metric import router as metric_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    metric_router,
    prefix=settings.api.v1.metric,
)

