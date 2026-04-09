import json
from typing import Any, List, Dict

from sqlalchemy import create_engine, text

from app.core.config import settings


# ------------------------------------------------------
# DB ENGINE
# ------------------------------------------------------

engine = create_engine(settings.database_url, future=True)


# ------------------------------------------------------
# DB INIT (TABLES + VECTOR SUPPORT)
# ------------------------------------------------------

def init_db() -> None:
    statements = [
        # Raw payload storage
        """
        CREATE TABLE IF NOT EXISTS raw_games (
            id SERIAL PRIMARY KEY,
            source_name VARCHAR(50) NOT NULL,
            source_game_id VARCHAR(100) NOT NULL,
            payload_json JSONB NOT NULL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_name, source_game_id)
        );
        """,

        # Main game table (no embedding dimension yet)
        """
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            source_name VARCHAR(50) NOT NULL,
            source_game_id VARCHAR(100) NOT NULL,
            slug VARCHAR(255),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            release_date DATE NULL,
            rating FLOAT NULL,
            rating_count INTEGER NULL,
            review_summary TEXT,
            cover_image_url TEXT,
            website_url TEXT,
            document_text TEXT,
            embedding vector,
            embedding_model VARCHAR(100),
            embedding_updated_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_name, source_game_id)
        );
        """,

        # Lookup tables
        """
        CREATE TABLE IF NOT EXISTS genres (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS platforms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tags (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        );
        """,

        # Mapping tables
        """
        CREATE TABLE IF NOT EXISTS game_genres (
            game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
            genre_id INTEGER REFERENCES genres(id) ON DELETE CASCADE,
            PRIMARY KEY (game_id, genre_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS game_platforms (
            game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
            platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE,
            PRIMARY KEY (game_id, platform_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS game_tags (
            game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
            tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (game_id, tag_id)
        );
        """,
    ]

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

        for stmt in statements:
            conn.execute(text(stmt))


# ------------------------------------------------------
# VECTOR SCHEMA FIX (IMPORTANT FIX)
# ------------------------------------------------------

def init_vector_schema(vector_dimension: int) -> None:
    statements = [
        "CREATE EXTENSION IF NOT EXISTS vector;",

        # Create embedding column safely
        f"""
        ALTER TABLE games
        ADD COLUMN IF NOT EXISTS embedding vector({vector_dimension});
        """,

        """
        ALTER TABLE games
        ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(100);
        """,

        """
        ALTER TABLE games
        ADD COLUMN IF NOT EXISTS embedding_updated_at TIMESTAMP;
        """
    ]

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


# ------------------------------------------------------
# RAW DATA STORAGE
# ------------------------------------------------------

def upsert_raw_game(source_name: str, source_game_id: str, payload: dict) -> None:
    query = text(
        """
        INSERT INTO raw_games (source_name, source_game_id, payload_json)
        VALUES (:source_name, :source_game_id, CAST(:payload_json AS JSONB))
        ON CONFLICT (source_name, source_game_id)
        DO UPDATE SET
            payload_json = EXCLUDED.payload_json,
            fetched_at = CURRENT_TIMESTAMP;
        """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "source_name": source_name,
                "source_game_id": source_game_id,
                "payload_json": json.dumps(payload),
            },
        )


# ------------------------------------------------------
# MAIN GAME UPSERT
# ------------------------------------------------------

def upsert_game(game: dict) -> int:
    query = text(
        """
        INSERT INTO games (
            source_name, source_game_id, slug, title, description,
            release_date, rating, rating_count, review_summary,
            cover_image_url, website_url, document_text
        )
        VALUES (
            :source_name, :source_game_id, :slug, :title, :description,
            :release_date, :rating, :rating_count, :review_summary,
            :cover_image_url, :website_url, :document_text
        )
        ON CONFLICT (source_name, source_game_id)
        DO UPDATE SET
            slug = EXCLUDED.slug,
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            release_date = EXCLUDED.release_date,
            rating = EXCLUDED.rating,
            rating_count = EXCLUDED.rating_count,
            review_summary = EXCLUDED.review_summary,
            cover_image_url = EXCLUDED.cover_image_url,
            website_url = EXCLUDED.website_url,
            document_text = EXCLUDED.document_text,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id;
        """
    )

    with engine.begin() as conn:
        result = conn.execute(query, game)
        return result.scalar_one()


# ------------------------------------------------------
# LOOKUP HELPERS
# ------------------------------------------------------

def get_or_create_lookup_id(table_name: str, value: str) -> int:
    select_query = text(f"SELECT id FROM {table_name} WHERE name = :value;")

    insert_query = text(
        f"""
        INSERT INTO {table_name} (name)
        VALUES (:value)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id;
        """
    )

    with engine.begin() as conn:
        result = conn.execute(select_query, {"value": value}).fetchone()
        if result:
            return result[0]

        result = conn.execute(insert_query, {"value": value})
        return result.scalar_one()


def replace_game_mappings(
    game_id: int,
    relation_table: str,
    foreign_key: str,
    values: List[str],
    lookup_table: str,
) -> None:
    delete_query = text(f"DELETE FROM {relation_table} WHERE game_id = :game_id;")

    with engine.begin() as conn:
        conn.execute(delete_query, {"game_id": game_id})

    for value in values:
        lookup_id = get_or_create_lookup_id(lookup_table, value)

        insert_query = text(
            f"""
            INSERT INTO {relation_table} (game_id, {foreign_key})
            VALUES (:game_id, :lookup_id)
            ON CONFLICT DO NOTHING;
            """
        )

        with engine.begin() as conn:
            conn.execute(
                insert_query,
                {"game_id": game_id, "lookup_id": lookup_id},
            )


# ------------------------------------------------------
# EMBEDDING FUNCTIONS
# ------------------------------------------------------

def list_games_missing_embeddings(limit: int = 100) -> List[Dict[str, Any]]:
    query = text(
        """
        SELECT id, title, document_text
        FROM games
        WHERE document_text IS NOT NULL
          AND TRIM(document_text) <> ''
          AND (embedding IS NULL OR embedding_updated_at IS NULL)
        ORDER BY id
        LIMIT :limit;
        """
    )

    with engine.begin() as conn:
        rows = conn.execute(query, {"limit": limit}).mappings().all()
        return [dict(row) for row in rows]


def update_game_embedding(
    game_id: int,
    embedding: List[float],
    embedding_model: str,
) -> None:
    vector_literal = "[" + ",".join(str(x) for x in embedding) + "]"

    query = text(
        """
        UPDATE games
        SET embedding = CAST(:embedding AS vector),
            embedding_model = :embedding_model,
            embedding_updated_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :game_id;
        """
    )

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "game_id": game_id,
                "embedding": vector_literal,
                "embedding_model": embedding_model,
            },
        )


# ------------------------------------------------------
# SEMANTIC SEARCH
# ------------------------------------------------------

def semantic_search_games(
    query_embedding: List[float],
    limit: int = 5,
) -> List[Dict[str, Any]]:
    vector_literal = "[" + ",".join(str(x) for x in query_embedding) + "]"

    query = text(
        """
        SELECT
            id,
            title,
            description,
            release_date,
            rating,
            rating_count,
            review_summary,
            cover_image_url,
            website_url,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity_score
        FROM games
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit;
        """
    )

    with engine.begin() as conn:
        rows = conn.execute(
            query,
            {"embedding": vector_literal, "limit": limit},
        ).mappings().all()

        return [dict(row) for row in rows]
