from typing import Any, Dict, List

from bs4 import BeautifulSoup


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def clean_html(text: str) -> str:
    if not text:
        return ""

    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)
    return clean_text


def _extract_names(items: Any, key: str = "name") -> List[str]:
    if not items or not isinstance(items, list):
        return []

    results: List[str] = []

    for item in items:
        if not item or not isinstance(item, dict):
            continue

        value = item.get(key)
        if value:
            results.append(str(value).strip())

    return results


def _extract_platform_names(platforms: Any) -> List[str]:
    if not platforms or not isinstance(platforms, list):
        return []

    results: List[str] = []

    for item in platforms:
        if not item or not isinstance(item, dict):
            continue

        platform = item.get("platform")
        if not platform or not isinstance(platform, dict):
            continue

        name = platform.get("name")
        if name:
            results.append(str(name).strip())

    return results


def build_game_document(game: Dict[str, Any]) -> str:
    title = _safe_str(game.get("title")) or "N/A"
    genres = ", ".join(game.get("genres", [])) or "N/A"
    platforms = ", ".join(game.get("platforms", [])) or "N/A"
    tags = ", ".join(game.get("tags", [])) or "N/A"
    release_date = _safe_str(game.get("release_date")) or "N/A"
    rating = game.get("rating")
    description = _safe_str(game.get("description")) or "N/A"
    review_summary = _safe_str(game.get("review_summary")) or "N/A"

    return (
        f"Title: {title}\n"
        f"Genres: {genres}\n"
        f"Platforms: {platforms}\n"
        f"Tags: {tags}\n"
        f"Release Date: {release_date}\n"
        f"Rating: {rating if rating is not None else 'N/A'}\n"
        f"Description: {description}\n"
        f"Review Summary: {review_summary}"
    )


def map_rawg_game(raw: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    raw = raw or {}
    details = details or {}

    raw_description = details.get("description_raw")
    description = clean_html(raw_description)

    rating = raw.get("rating")
    rating_count = raw.get("ratings_count")

    mapped: Dict[str, Any] = {
        "source_name": "rawg",
        "source_game_id": _safe_str(raw.get("id")),
        "slug": _safe_str(raw.get("slug")),
        "title": _safe_str(raw.get("name")) or "Unknown Title",
        "description": description[:2000] if description else "",
        "release_date": raw.get("released"),
        "rating": rating,
        "rating_count": rating_count,
        "review_summary": (
            f"Rated {rating} based on {rating_count} ratings."
            if rating is not None and rating_count is not None
            else ""
        ),
        "cover_image_url": _safe_str(raw.get("background_image")),
        "website_url": _safe_str(details.get("website")),
        "genres": _extract_names(details.get("genres")),
        "tags": _extract_names(details.get("tags")),
        "platforms": _extract_platform_names(details.get("platforms")),
    }

    mapped["document_text"] = build_game_document(mapped)
    return mapped
