const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type SearchResult = {
  id: number;
  title: string;
  description?: string | null;
  release_date?: string | null;
  rating?: number | null;
  rating_count?: number | null;
  review_summary?: string | null;
  cover_image_url?: string | null;
  website_url?: string | null;
  similarity_score: number;
};

export type SearchResponse = {
  results: SearchResult[];
};

export type GameDetail = {
  id: number;
  source_name: string;
  source_game_id: string;
  slug?: string | null;
  title: string;
  description?: string | null;
  release_date?: string | null;
  rating?: number | null;
  rating_count?: number | null;
  review_summary?: string | null;
  cover_image_url?: string | null;
  website_url?: string | null;
  genres: string[];
  platforms: string[];
  tags: string[];
};

export async function searchGames(
  query: string,
  limit = 6
): Promise<SearchResult[]> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      limit,
    }),
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Search failed: ${text}`);
  }

  const data: SearchResponse = await response.json();
  return data.results;
}

export async function getGameById(gameId: string): Promise<GameDetail> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Game detail fetch failed: ${text}`);
  }

  return response.json();
}
