"use client";

import { useState, useEffect } from "react";
import EventCard from "@/components/EventCard";
import { mockEvents, Event } from "@/lib/mockData";

export default function FeedPage() {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    // Simulate fetching data
    setTimeout(() => {
      setEvents(mockEvents);
    }, 500); // optional delay to simulate network
  }, []);

  if (!events) return <p>Loading...</p>;
  if (events.length === 0) return <p>No events found</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Event Feed</h1>
      {events.map((e) => (
        <EventCard key={e.id} event={e} />
      ))}
    </div>
  );
}
// working with mockdata for now, will replace with backend data fetching in the future