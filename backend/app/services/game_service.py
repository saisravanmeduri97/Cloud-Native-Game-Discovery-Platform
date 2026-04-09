from sqlalchemy import text
from sqlalchemy.orm import Session


def semantic_search_games(db: Session, query_embedding: list[float], limit: int = 5) -> list[dict]:
    vector_literal = "[" + ",".join(str(x) for x in query_embedding) + "]"

    query = text(
        """
        SELECT
            id,
            title,
            description,
            release_date::text AS release_date,
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

    rows = db.execute(
        query,
        {"embedding": vector_literal, "limit": limit},
    ).mappings().all()

    return [dict(row) for row in rows]


def get_game_by_id(db: Session, game_id: int) -> dict | None:
    game_query = text(
        """
        SELECT
            id,
            source_name,
            source_game_id,
            slug,
            title,
            description,
            release_date::text AS release_date,
            rating,
            rating_count,
            review_summary,
            cover_image_url,
            website_url
        FROM games
        WHERE id = :game_id;
        """
    )

    row = db.execute(game_query, {"game_id": game_id}).mappings().first()
    if not row:
        return None

    result = dict(row)

    genre_query = text(
        """
        SELECT ge.name
        FROM genres ge
        JOIN game_genres gg ON ge.id = gg.genre_id
        WHERE gg.game_id = :game_id
        ORDER BY ge.name;
        """
    )

    platform_query = text(
        """
        SELECT p.name
        FROM platforms p
        JOIN game_platforms gp ON p.id = gp.platform_id
        WHERE gp.game_id = :game_id
        ORDER BY p.name;
        """
    )

    tag_query = text(
        """
        SELECT t.name
        FROM tags t
        JOIN game_tags gt ON t.id = gt.tag_id
        WHERE gt.game_id = :game_id
        ORDER BY t.name;
        """
    )

    result["genres"] = [r[0] for r in db.execute(genre_query, {"game_id": game_id}).all()]
    result["platforms"] = [r[0] for r in db.execute(platform_query, {"game_id": game_id}).all()]
    result["tags"] = [r[0] for r in db.execute(tag_query, {"game_id": game_id}).all()]

    return result
