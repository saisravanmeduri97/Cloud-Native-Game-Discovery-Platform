import logging

from fastapi import APIRouter


logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    logger.info(
        "Health check requested",
        extra={"extra_data": {"event": "health_check"}}
    )
    return {"status": "ok"}


@router.get("/ready")
def readiness():
    logger.info(
        "Readiness check requested",
        extra={"extra_data": {"event": "readiness_check"}}
    )
    return {"status": "ready"}
