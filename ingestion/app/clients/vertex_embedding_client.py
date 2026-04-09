from vertexai import init
from vertexai.language_models import TextEmbeddingModel

from app.core.config import settings


class VertexEmbeddingClient:
    def __init__(self) -> None:
        if not settings.GCP_PROJECT_ID:
            raise ValueError("GDP_GCP_PROJECT_ID is not set.")
        if not settings.GCP_LOCATION:
            raise ValueError("GDP_GCP_LOCATION is not set.")

        init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
        self.model = TextEmbeddingModel.from_pretrained(settings.EMBEDDING_MODEL)

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text.")

        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values
