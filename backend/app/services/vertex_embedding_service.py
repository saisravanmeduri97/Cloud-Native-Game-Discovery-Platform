import logging

from vertexai import init
from vertexai.language_models import TextEmbeddingModel

from app.core.config import settings
from app.services.query_cache_service import QueryCacheService


logger = logging.getLogger(__name__)


class VertexEmbeddingService:
    def __init__(self) -> None:
        if not settings.GCP_PROJECT_ID:
            raise ValueError("GDP_GCP_PROJECT_ID is not set.")

        init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
        self.model = TextEmbeddingModel.from_pretrained(settings.EMBEDDING_MODEL)
        self.cache_service = QueryCacheService()

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text.")

        normalized_text = text.strip()

        cached_embedding = self.cache_service.get(normalized_text)
        if cached_embedding is not None:
            logger.info(
                "Embedding cache hit",
                extra={
                    "extra_data": {
                        "event": "embedding_cache_hit",
                        "query_length": len(normalized_text),
                        "embedding_model": settings.EMBEDDING_MODEL,
                    }
                },
            )
            return cached_embedding

        logger.info(
            "Embedding cache miss; calling Vertex AI",
            extra={
                "extra_data": {
                    "event": "embedding_cache_miss",
                    "query_length": len(normalized_text),
                    "embedding_model": settings.EMBEDDING_MODEL,
                }
            },
        )

        embeddings = self.model.get_embeddings([normalized_text])
        embedding_values = embeddings[0].values

        self.cache_service.set(normalized_text, embedding_values)

        logger.info(
            "Stored query embedding in cache",
            extra={
                "extra_data": {
                    "event": "embedding_cache_store",
                    "query_length": len(normalized_text),
                    "embedding_dimension": len(embedding_values),
                    "embedding_model": settings.EMBEDDING_MODEL,
                }
            },
        )

        return embedding_values
