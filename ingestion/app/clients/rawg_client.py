import requests
from typing import Dict, Any

from app.core.config import settings


class RawgClient:
    BASE_URL = "https://api.rawg.io/api"

    def __init__(self) -> None:
        if not settings.RAWG_API_KEY:
            raise ValueError("GDP_RAWG_API_KEY is not set in environment variables.")

    # ------------------------------------------------------
    # FETCH LIST OF GAMES
    # ------------------------------------------------------

    def fetch_games(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/games"

        params = {
            "key": settings.RAWG_API_KEY,
            "page": page,
            "page_size": page_size,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Failed to fetch games from RAWG: {exc}") from exc

    # ------------------------------------------------------
    # FETCH GAME DETAILS (IMPORTANT UPGRADE)
    # ------------------------------------------------------

    def fetch_game_details(self, game_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/games/{game_id}"

        params = {
            "key": settings.RAWG_API_KEY,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                f"Failed to fetch game details for id={game_id}: {exc}"
            ) from exc
