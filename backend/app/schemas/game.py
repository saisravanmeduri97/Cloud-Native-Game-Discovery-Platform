from pydantic import BaseModel


class GameDetailResponse(BaseModel):
    id: int
    source_name: str
    source_game_id: str
    slug: str | None = None
    title: str
    description: str | None = None
    release_date: str | None = None
    rating: float | None = None
    rating_count: int | None = None
    review_summary: str | None = None
    cover_image_url: str | None = None
    website_url: str | None = None
    genres: list[str]
    platforms: list[str]
    tags: list[str]
