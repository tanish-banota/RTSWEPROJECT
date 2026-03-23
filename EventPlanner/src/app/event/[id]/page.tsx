"use client";

import { useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { mockEvents, Event } from "@/lib/mockData";

export default function EventDetail() {
  const router = useRouter();
  const params = useParams();

  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const id = params.id as string;

    // Simulate API fetch
    setTimeout(() => {
      const foundEvent = mockEvents.find((e) => e.id === id) || null;
      setEvent(foundEvent);
      setLoading(false);
    }, 300);
  }, [params.id]);

  // Loading state
  if (loading) {
    return <p className="p-6">Loading event...</p>;
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
      <p className="text-gray-600 mb-2">{event.club}</p>
      <p className="mb-2">
        {new Date(event.date).toLocaleString()}
      </p>
      <p className="mb-4">{event.location}</p>

    </div>
  );
}
