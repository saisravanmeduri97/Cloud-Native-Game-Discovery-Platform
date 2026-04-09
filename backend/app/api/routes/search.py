import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import SearchRequest, SearchResponse
from app.services.game_service import semantic_search_games
from app.services.vertex_embedding_service import VertexEmbeddingService


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search_games(payload: SearchRequest, db: Session = Depends(get_db)):
    logger.info(
        "Received search request",
        extra={
            "extra_data": {
                "event": "search_request_received",
                "query": payload.query,
                "limit": payload.limit,
            }
        },
    )

    try:
        embedding_service = VertexEmbeddingService()
        query_embedding = embedding_service.embed_text(payload.query)
        results = semantic_search_games(db, query_embedding, payload.limit)

        logger.info(
            "Search request completed successfully",
            extra={
                "extra_data": {
                    "event": "search_request_completed",
                    "query": payload.query,
                    "limit": payload.limit,
                    "result_count": len(results),
                }
            },
        )

        return {"results": results}

    except Exception as exc:
        logger.exception(
            "Search request failed",
            extra={
                "extra_data": {
                    "event": "search_request_failed",
                    "query": payload.query,
                    "limit": payload.limit,
                }
            },
        )
        raise HTTPException(status_code=500, detail=f"Search failed: {exc}")
