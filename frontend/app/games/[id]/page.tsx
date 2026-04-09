import Link from "next/link";

import { getGameById } from "../../lib/api";

type PageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function GameDetailPage({ params }: PageProps) {
  const { id } = await params;
  const game = await getGameById(id);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-6xl px-6 py-10">
        <Link
          href="/"
          className="inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 transition hover:border-sky-400 hover:text-white"
        >
          ← Back to search
        </Link>

        <div className="mt-8 grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
            <div className="h-80 w-full overflow-hidden bg-slate-900">
              {game.cover_image_url ? (
                <img
                  src={game.cover_image_url}
                  alt={game.title}
                  className="h-full w-full object-cover"
                />
              ) : (
                <div className="flex h-full items-center justify-center text-slate-500">
                  No image available
                </div>
              )}
            </div>

            <div className="p-6">
              <div className="flex flex-wrap items-center gap-3">
                <span className="rounded-full bg-sky-500/15 px-3 py-1 text-sm text-sky-300">
                  {game.source_name.toUpperCase()}
                </span>

                {game.release_date && (
                  <span className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">
                    Released: {game.release_date}
                  </span>
                )}

                {typeof game.rating === "number" && (
                  <span className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">
                    Rating: {game.rating}
                  </span>
                )}
              </div>

              <h1 className="mt-4 text-4xl font-bold">{game.title}</h1>

              <p className="mt-5 whitespace-pre-line text-base leading-7 text-slate-300">
                {game.description || "No description available."}
              </p>

              {game.website_url && (
                <a
                  href={game.website_url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-6 inline-flex rounded-2xl bg-sky-500 px-5 py-3 font-semibold text-white transition hover:bg-sky-400"
                >
                  Visit Official Website
                </a>
              )}
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Review Summary</h2>
              <p className="mt-3 text-sm leading-6 text-slate-300">
                {game.review_summary || "No review summary available."}
              </p>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Genres</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                {game.genres.length > 0 ? (
                  game.genres.map((genre) => (
                    <span
                      key={genre}
                      className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300"
                    >
                      {genre}
                    </span>
                  ))
                ) : (
                  <p className="text-sm text-slate-400">No genres available.</p>
                )}
              </div>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Platforms</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                {game.platforms.length > 0 ? (
                  game.platforms.map((platform) => (
                    <span
                      key={platform}
                      className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300"
                    >
                      {platform}
                    </span>
                  ))
                ) : (
                  <p className="text-sm text-slate-400">No platforms available.</p>
                )}
              </div>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
              <h2 className="text-lg font-semibold">Tags</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                {game.tags.length > 0 ? (
                  game.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300"
                    >
                      {tag}
                    </span>
                  ))
                ) : (
                  <p className="text-sm text-slate-400">No tags available.</p>
                )}
              </div>
            </div>
          </aside>
        </div>
      </section>
    </main>
  );
}
