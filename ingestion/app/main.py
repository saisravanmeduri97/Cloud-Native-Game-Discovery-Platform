import time
import traceback

from app.clients.rawg_client import RawgClient
from app.core.config import settings
from app.loaders.postgres_loader import (
    init_db,
    replace_game_mappings,
    upsert_game,
    upsert_raw_game,
)
from app.mappers.game_mapper import map_rawg_game


def run_ingestion(page: int = 1) -> None:
    print("Initializing database tables...")
    init_db()

    client = RawgClient()
    print(f"Fetching RAWG data page={page}, page_size={settings.INGEST_PAGE_SIZE}...")

    response = client.fetch_games(page=page, page_size=settings.INGEST_PAGE_SIZE)
    results = response.get("results", [])

    print(f"Fetched {len(results)} games.")

    for raw_game in results:
        try:
            game_id = raw_game.get("id")
            details = client.fetch_game_details(str(game_id))
            mapped = map_rawg_game(raw_game, details)

            upsert_raw_game(
                source_name=mapped["source_name"],
                source_game_id=mapped["source_game_id"],
                payload=raw_game,
            )

            db_game_id = upsert_game(mapped)

            replace_game_mappings(
                db_game_id,
                "game_genres",
                "genre_id",
                mapped["genres"],
                "genres",
            )
            replace_game_mappings(
                db_game_id,
                "game_platforms",
                "platform_id",
                mapped["platforms"],
                "platforms",
            )
            replace_game_mappings(
                db_game_id,
                "game_tags",
                "tag_id",
                mapped["tags"],
                "tags",
            )

            print(f"Upserted game: {mapped['title']}")
            time.sleep(0.2)

        except Exception as exc:
            print(f"Failed processing record id={raw_game.get('id')}: {exc}")
            traceback.print_exc()

    print("Ingestion completed.")


if __name__ == "__main__":
    run_ingestion(page=1)
