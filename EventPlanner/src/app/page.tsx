import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 py-14 px-6 text-slate-950">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-12">
        <div className="rounded-[2rem] border border-slate-200 bg-white/95 p-10 shadow-[0_40px_120px_-40px_rgba(15,23,42,0.35)] backdrop-blur-xl">
          <div className="max-w-3xl text-center mx-auto">
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.28em] text-sky-600">
              Campus events, simplified
            </p>
            <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl">
              Discover campus events effortlessly.
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
              Find club meetings, networking events, and social gatherings — all in one place.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link
                href="/feed"
                className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-sky-600 to-indigo-600 px-8 py-4 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-700 hover:to-indigo-700"
              >
                Explore Events
              </Link>
              <Link
                href="/login"
                className="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-8 py-4 text-sm font-semibold text-slate-900 transition hover:bg-slate-100"
              >
                Login
              </Link>
            </div>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="rounded-[1.5rem] border border-slate-200 bg-slate-950 p-7 shadow-lg shadow-slate-900/10">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-sky-600 text-white shadow-sm">
              📅
            </div>
            <h3 className="text-xl font-semibold text-white">Stay Updated</h3>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              Never miss a meeting — we gather events from multiple sources and keep your calendar in sync.
            </p>
          </div>

          <div className="rounded-[1.5rem] border border-slate-200 bg-slate-950 p-7 shadow-lg shadow-slate-900/10">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-indigo-600 text-white shadow-sm">
              💬
            </div>
            <h3 className="text-xl font-semibold text-white">Connect</h3>
            <p className="mt-3 text-sm leading-7 text-slate-300">
              RSVP and connect with others attending the same events, all from your feed.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
