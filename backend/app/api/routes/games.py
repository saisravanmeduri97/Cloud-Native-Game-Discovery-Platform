import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.game import GameDetailResponse
from app.services.game_service import get_game_by_id


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    logger.info(
        "Received game detail request",
        extra={
            "extra_data": {
                "event": "game_detail_request_received",
                "game_id": game_id,
            }
        },
    )

    result = get_game_by_id(db, game_id)
    if not result:
        logger.warning(
            "Game not found",
            extra={
                "extra_data": {
                    "event": "game_detail_not_found",
                    "game_id": game_id,
                }
            },
        )
        raise HTTPException(status_code=404, detail="Game not found")

    logger.info(
        "Game detail request completed",
        extra={
            "extra_data": {
                "event": "game_detail_request_completed",
                "game_id": game_id,
                "title": result["title"],
            }
        },
    )
    return result
