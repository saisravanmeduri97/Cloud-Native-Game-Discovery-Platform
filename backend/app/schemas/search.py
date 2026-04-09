from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language game discovery query")
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    id: int
    title: str
    description: str | None = None
    release_date: str | None = None
    rating: float | None = None
    rating_count: int | None = None
    review_summary: str | None = None
    cover_image_url: str | None = None
    website_url: str | None = None
    similarity_score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
