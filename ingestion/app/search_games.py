import json
import os
from typing import Any, Dict, List

from app.clients.vertex_embedding_client import VertexEmbeddingClient
from app.loaders.postgres_loader import semantic_search_games


CACHE_FILE = "query_cache.json"


def load_cache() -> Dict[str, List[float]]:
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache: Dict[str, List[float]]) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file)


def get_query_embedding(query: str) -> List[float]:
    cache = load_cache()

    if query in cache:
        print("Using cached embedding.")
        return cache[query]

    print("Generating embedding from Vertex AI...")
    client = VertexEmbeddingClient()
    embedding = client.embed_text(query)

    cache[query] = embedding
    save_cache(cache)

    return embedding


def print_results(query: str, results: List[Dict[str, Any]]) -> None:
    print(f"\nQuery: {query}\n")

    if not results:
        print("No matching games found.")
        return

    for idx, row in enumerate(results, start=1):
        print(f"{idx}. {row['title']} | score={row['similarity_score']:.4f}")
        print(f"   Rating: {row.get('rating')} ({row.get('rating_count')} ratings)")
        print(f"   Release Date: {row.get('release_date')}")
        print(f"   Review Summary: {row.get('review_summary')}")
        print(f"   Cover Image: {row.get('cover_image_url')}")
        print()


def run_semantic_search(query: str, limit: int = 5) -> None:
    try:
        embedding = get_query_embedding(query)
        results = semantic_search_games(embedding, limit=limit)
        print_results(query, results)
    except Exception as exc:
        print(f"Semantic search failed: {exc}")
        raise


if __name__ == "__main__":
    run_semantic_search("dark fantasy open world action rpg", limit=5)
