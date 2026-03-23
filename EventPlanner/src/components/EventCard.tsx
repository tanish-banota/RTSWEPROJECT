"use client";

import Link from "next/link";
import { useState } from "react";

type Event = {
  id: string;
  title: string;
  club: string;
  date: string;
  location: string;
};

type EventCardProps = {
  event: Event;
};

export default function EventCard({ event }: EventCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [isRSVPed, setIsRSVPed] = useState(false);

  const handleRSVP = async () => {
    try {
      setIsLoading(true);

      await fetch(`/rsvp/${event.id}`, { method: "POST" });

      setIsRSVPed(true);
    } catch (err) {
      console.error("Failed to RSVP");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="border p-4 rounded mb-4 shadow-sm">
      
      {/* CLICKABLE CONTENT */}
      <Link href={`/event/${event.id}`}>
        <div className="cursor-pointer hover:bg-gray-50 p-2 rounded">
          <h2 className="text-xl font-bold">{event.title}</h2>
          <p>{event.club}</p>
          <p>{new Date(event.date).toLocaleString()}</p>
          <p>{event.location}</p>
        </div>
      </Link>

      {/* ACTION BUTTONS */}
      <button
        className={`mt-3 px-4 py-2 rounded text-white ${
          isRSVPed
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-600"
        }`}
        onClick={handleRSVP}
        disabled={isLoading || isRSVPed}
      >
        {isLoading ? "RSVPing..." : isRSVPed ? "RSVPed" : "RSVP"}
      </button>
    </div>
  );
}