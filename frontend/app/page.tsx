"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

import { SearchResult, searchGames } from "./lib/api";

const samplePrompts = [
  "dark fantasy open world action rpg",
  "relaxing indie exploration game",
  "fast paced multiplayer shooter",
  "story rich sci-fi game with choices",
];

function formatScore(score: number): string {
  return (score * 100).toFixed(1) + "%";
}

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(event: FormEvent) {
    event.preventDefault();

    const trimmedQuery = query.trim();
    if (!trimmedQuery) {
      setError("Please enter a game discovery query.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSearched(false);

      const data = await searchGames(trimmedQuery, 8);
      setResults(data);
      setSearched(true);
    } catch (err) {
      setResults([]);
      setSearched(true);
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handlePromptClick(prompt: string) {
    setQuery(prompt);
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-10">
        <div className="mb-10">
          <div className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-1 text-sm text-slate-300">
            Cloud Native Game Discovery Platform
          </div>

          <h1 className="mt-6 max-w-4xl text-4xl font-bold leading-tight md:text-6xl">
            AI-powered game discovery with semantic search
          </h1>

          <p className="mt-4 max-w-3xl text-base text-slate-300 md:text-lg">
            Describe the kind of game you want in natural language, and the
            platform will return the closest semantic matches using embeddings,
            pgvector, and FastAPI.
          </p>
        </div>

        <form
          onSubmit={handleSearch}
          className="rounded-3xl border border-white/10 bg-white/5 p-4 shadow-2xl backdrop-blur"
        >
          <div className="flex flex-col gap-3 md:flex-row">
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Try: dark fantasy open world action rpg"
              className="flex-1 rounded-2xl border border-white/10 bg-slate-900 px-5 py-4 text-base text-white outline-none ring-0 placeholder:text-slate-400 focus:border-sky-400"
            />
            <button
              type="submit"
              disabled={loading}
              className="rounded-2xl bg-sky-500 px-6 py-4 font-semibold text-white transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Searching..." : "Discover Games"}
            </button>
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            {samplePrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => handlePromptClick(prompt)}
                className="rounded-full border border-white/10 bg-slate-900 px-3 py-2 text-sm text-slate-300 transition hover:border-sky-400 hover:text-white"
              >
                {prompt}
              </button>
            ))}
          </div>
        </form>

        {error && (
          <div className="mt-6 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
            {error}
          </div>
        )}

        {!loading && !searched && (
          <section className="mt-10 grid gap-4 md:grid-cols-3">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Natural language search</h2>
              <p className="mt-2 text-sm text-slate-300">
                Search with intent, not exact keywords. Ask for mood, genre,
                pace, style, or gameplay feel.
              </p>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">AI retrieval</h2>
              <p className="mt-2 text-sm text-slate-300">
                Results are ranked using semantic similarity over embedded game
                documents stored in PostgreSQL with pgvector.
              </p>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Cloud-native design</h2>
              <p className="mt-2 text-sm text-slate-300">
                Built for a production-minded deployment model with FastAPI,
                GKE, Terraform, observability, and structured logging.
              </p>
            </div>
          </section>
        )}

        {searched && !loading && results.length === 0 && !error && (
          <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-8 text-slate-300">
            No matches found for that query. Try changing the genre, mood, or
            gameplay style.
          </div>
        )}

        {results.length > 0 && (
          <section className="mt-10">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-2xl font-semibold">Results</h2>
              <p className="text-sm text-slate-400">
                {results.length} game{results.length === 1 ? "" : "s"} found
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {results.map((game) => (
                <Link
                  key={game.id}
                  href={`/games/${game.id}`}
                  className="group overflow-hidden rounded-3xl border border-white/10 bg-white/5 transition hover:border-sky-400/60 hover:bg-white/10"
                >
                  <div className="relative h-52 w-full overflow-hidden bg-slate-900">
                    {game.cover_image_url ? (
                      <img
                        src={game.cover_image_url}
                        alt={game.title}
                        className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full items-center justify-center text-slate-500">
                        No image available
                      </div>
                    )}
                  </div>

                  <div className="p-5">
                    <div className="mb-3 flex items-start justify-between gap-3">
                      <h3 className="text-lg font-semibold text-white">
                        {game.title}
                      </h3>
                      <span className="rounded-full bg-sky-500/15 px-3 py-1 text-xs font-medium text-sky-300">
                        {formatScore(game.similarity_score)}
                      </span>
                    </div>

                    <p className="line-clamp-4 text-sm text-slate-300">
                      {game.description || game.review_summary || "No summary available."}
                    </p>

                    <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-400">
                      {game.release_date && (
                        <span className="rounded-full border border-white/10 px-2 py-1">
                          {game.release_date}
                        </span>
                      )}
                      {typeof game.rating === "number" && (
                        <span className="rounded-full border border-white/10 px-2 py-1">
                          Rating: {game.rating}
                        </span>
                      )}
                      {typeof game.rating_count === "number" && (
                        <span className="rounded-full border border-white/10 px-2 py-1">
                          {game.rating_count} ratings
                        </span>
                      )}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}
      </section>
    </main>
  );
}
