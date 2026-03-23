"use client";

import { useState, useEffect } from "react";
import EventCard from "@/components/EventCard";
import { mockEvents, Event } from "@/lib/mockData";

export default function FeedPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setEvents(mockEvents);
      setLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  // LOADING STATE
  if (loading) {
    return <p className="p-6">Loading events...</p>;
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
// working with mockdata for now, will replace with backend data fetching in the future