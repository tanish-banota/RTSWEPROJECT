"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { supabase } from "@/lib/supabaseClient";

type Event = {
  id: string;
  title: string;
  club: string;
  date: string;
  location: string;
  description: string;
  tags?: string[];
};

type EventCardProps = {
  event: Event;
};

export default function EventCard({ event }: EventCardProps) {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isRSVPed, setIsRSVPed] = useState(false);

  useEffect(() => {
    if (!user) {
      setIsRSVPed(false);
      return;
    }

    const fetchRSVPStatus = async () => {
      const { data, error } = await supabase
        .from("profiles")
        .select("rsvpd_events")
        .eq("id", user.id)
        .single();

      if (!error && data?.rsvpd_events?.includes(event.id)) {
        setIsRSVPed(true);
      } else {
        setIsRSVPed(false);
      }
    };

    fetchRSVPStatus();
  }, [event.id, user]);

  const handleRSVP = async () => {
    if (!user) {
      return;
    }

    try {
      setIsLoading(true);

      const { data: profile, error: fetchError } = await supabase
        .from("profiles")
        .select("rsvpd_events")
        .eq("id", user.id)
        .single();

      const existingEvents = profile?.rsvpd_events ?? [];
      const updatedEvents = Array.from(new Set([...existingEvents, event.id]));

      const { error: upsertError } = await supabase
        .from("profiles")
        .upsert(
          {
            id: user.id,
            rsvpd_events: updatedEvents,
          },
          { onConflict: "id" }
        );

      if (upsertError) {
        throw upsertError;
      }

      setIsRSVPed(true);
    } catch (err) {
      console.error("Failed to RSVP", err);
      // You could show a user-friendly error message here
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
          <p className="text-sm text-gray-600">{event.club}</p>
          <p className="text-sm text-gray-600">{new Date(event.date).toLocaleString()}</p>
          <p className="text-sm text-gray-600">{event.location}</p>
          
          {/* TAGS */}
          {event.tags && event.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-2">
              {event.tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </Link>

      {/* ACTION BUTTONS */}
      {user ? (
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
      ) : (
        <p className="mt-3 text-sm text-gray-500">Login to RSVP</p>
      )}
    </div>
  );
}