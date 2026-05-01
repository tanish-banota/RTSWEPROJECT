"use client";

import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getEvents, Event } from "@/lib/api";

export default function EventDetail() {
  const router = useRouter();
  const params = useParams();

  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const id = params.id as string;

    const fetchEvent = async () => {
      try {
        setLoading(true);
        setError(null);
        const events = await getEvents();
        const foundEvent = events.find((e) => e.id === id) || null;
        setEvent(foundEvent);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch event");
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [params.id]);

  // Loading state
  if (loading) {
    return <p className="p-6">Loading event...</p>;
  }

  // Error state
  if (error) {
    return <p className="p-6 text-red-500">Error: {error}</p>;
  }

  // Not found state
  if (!event) {
    return <p className="p-6 text-red-500">Event not found</p>;
  }

  // Normal UI
  return (
    <div className="p-6 max-w-xl mx-auto">
      <button
        onClick={() => router.back()}
        className="mb-4 text-blue-500"
      >
        ← Back
      </button>

      <h1 className="text-2xl font-bold mb-2">{event.title}</h1>
      <p className="text-white-600 mb-2">{event.club}</p>
      <p className="text-white-600 mb-2">
        {new Date(event.date).toLocaleString()}
      </p>
      <p className="text-white-600 mb-4">{event.location}</p>
      <p className="text-white-700 leading-relaxed">{event.description}</p>
    </div>
  );
}
