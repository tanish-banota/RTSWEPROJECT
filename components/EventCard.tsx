"use client";

import { Event } from "../lib/mockData";

export default function EventCard({ event }: { event: Event }) {
  return (
    <div className="border rounded-lg p-4 mb-4 shadow-sm">
      <h2 className="text-xl font-semibold mb-2">🎉 {event.title}</h2>
      <p className="mb-1">🏛️ {event.club}</p>
      <p className="mb-1">📅 {new Date(event.date).toLocaleString()}</p>
      <p className="mb-3">📍 {event.location}</p>
    </div>
  );
}