import json
import os
import threading
from typing import Dict, List

from app.core.config import settings


class QueryCacheService:
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.cache_file = settings.QUERY_CACHE_FILE

    def _load_cache(self) -> Dict[str, List[float]]:
        if not os.path.exists(self.cache_file):
            return {}

        try:
            with open(self.cache_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                return {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_cache(self, cache: Dict[str, List[float]]) -> None:
        with open(self.cache_file, "w", encoding="utf-8") as file:
            json.dump(cache, file)

    def get(self, query: str) -> List[float] | None:
        with self._lock:
            cache = self._load_cache()
            value = cache.get(query)
            if isinstance(value, list):
                return value
            return None

    def set(self, query: str, embedding: List[float]) -> None:
        with self._lock:
            cache = self._load_cache()
            cache[query] = embedding
            self._save_cache(cache)
