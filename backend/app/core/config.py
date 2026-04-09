import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = os.getenv("GDP_PROJECT_NAME", "cloud-native-game-discovery-platform")

    DB_HOST = os.getenv("GDP_DB_HOST", "localhost")
    DB_PORT = int(os.getenv("GDP_DB_PORT", "5432"))
    DB_NAME = os.getenv("GDP_DB_NAME", "gamedb")
    DB_USER = os.getenv("GDP_DB_USER", "gameuser")
    DB_PASSWORD = os.getenv("GDP_DB_PASSWORD", "gamepass")

    GCP_PROJECT_ID = os.getenv("GDP_GCP_PROJECT_ID", "")
    GCP_LOCATION = os.getenv("GDP_GCP_LOCATION", "us-central1")
    EMBEDDING_MODEL = os.getenv("GDP_EMBEDDING_MODEL", "gemini-embedding-001")

    QUERY_CACHE_FILE = os.getenv("GDP_QUERY_CACHE_FILE", "query_cache.json")
    LOG_LEVEL = os.getenv("GDP_LOG_LEVEL", "INFO")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
