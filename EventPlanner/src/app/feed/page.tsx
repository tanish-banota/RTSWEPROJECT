"use client";

import { useState, useEffect } from "react";
import EventCard from "@/components/EventCard";
import { getEvents, Event } from "@/lib/api";

export default function FeedPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getEvents();
        setEvents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch events");
        console.error("Error fetching events:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  // LOADING STATE
  if (loading) {
    return <p className="p-6">Loading events...</p>;
  }

  // ERROR STATE
  if (error) {
    return <p className="p-6 text-red-500">Error: {error}</p>;
  }

  // EMPTY STATE
  if (events.length === 0) {
    return <p className="p-6">No events found</p>;
  }

  // NORMAL UI
  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl mb-4 font-bold">Event Feed</h1>

      {events.map((e) => (
        <EventCard key={e.id} event={e} />
      ))}
    </div>
  );
}