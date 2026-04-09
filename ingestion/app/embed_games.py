from app.clients.vertex_embedding_client import VertexEmbeddingClient
from app.core.config import settings
from app.loaders.postgres_loader import (
    init_db,
    init_vector_schema,
    list_games_missing_embeddings,
    update_game_embedding,
)
import time

def run_embedding_backfill(limit: int = 50) -> None:
    print("Initializing database schema...")
    init_db()

    client = VertexEmbeddingClient()

    print("Getting first embedding to detect vector dimension...")
    test_vector = client.embed_text("test embedding dimension")
    vector_dimension = len(test_vector)
    print(f"Detected embedding dimension: {vector_dimension}")

    init_vector_schema(vector_dimension)

    games = list_games_missing_embeddings(limit=limit)
    print(f"Found {len(games)} games missing embeddings.")

    for game in games:
        try:
            time.sleep(0.5)
            embedding = client.embed_text(game["document_text"])
            update_game_embedding(
                game_id=game["id"],
                embedding=embedding,
                embedding_model=settings.EMBEDDING_MODEL,
            )
            print(f"Embedded game: {game['title']}")
        except Exception as exc:
            print(f"Failed embedding game id={game['id']} title={game['title']}: {exc}")

    print("Embedding backfill complete.")


if __name__ == "__main__":
    run_embedding_backfill(limit=5)
