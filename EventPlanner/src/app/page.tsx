import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black-50 px-6">
      
      {/* HERO SECTION */}
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4">
          Discover Campus Events Effortlessly
        </h1>

        <p className="text-gray-600 text-lg mb-8">
          Find club meetings, networking events, and social gatherings — all in one place.
        </p>

        {/* CTA BUTTONS */}
        <div className="flex gap-4 justify-center">
          <Link
            href="/feed"
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg"
          >
            Explore Events
          </Link>

          <Link
            href="/login"
            className="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-100"
          >
            Login
          </Link>
        </div>
      </div>

      {/* FEATURE SECTION */}
      <div className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl">
        
        <div className="p-4 bg-black rounded-lg shadow">
          <h3 className="font-semibold mb-2">📅 Stay Updated</h3>
          <p className="text-sm text-gray-600">
            Never miss a meeting — we gather events from multiple sources.
          </p>
        </div>

        <div className="p-4 bg-black rounded-lg shadow">
          <h3 className="font-semibold mb-2">💬 Connect</h3>
          <p className="text-sm text-gray-600">
            RSVP and chat with others attending the same events.
          </p>
        </div>

      </div>
    </div>
  );
}