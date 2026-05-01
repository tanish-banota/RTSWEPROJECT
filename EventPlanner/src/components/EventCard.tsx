"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { supabase } from "@/lib/supabaseClient";

type Event = {
  id: string;
  title: string;
  club_name: string;
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
  const router = useRouter();

  const [isFavorited, setIsFavorited] = useState(false);

  const handleDelete = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!confirm("Are you sure you want to delete this event?")) return;

    const { error } = await supabase
      .from("events")
      .delete()
      .eq("id", event.id); // Delete by event ID[cite: 3]

    if (error) {
      alert("Error deleting event: " + error.message);
    } else {
      window.location.reload(); // Refresh the feed to show it's gone[cite: 11]
    }
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    router.push(`/admin/edit-event/${event.id}`); // Direct to edit page[cite: 15]
  };

  const [isLoading, setIsLoading] = useState(false);
  const [isRSVPed, setIsRSVPed] = useState(false);

  useEffect(() => {
    if (!user) return;
    
    // Check if this event is already favorited by the user
    const checkFavorite = async () => {
      const { data } = await supabase
        .from("user_favorites")
        .select("id")
        .eq("user_id", user.id)
        .eq("event_id", event.id)
        .single();
      
      if (data) setIsFavorited(true);
    };

    checkFavorite();
  }, [user, event.id]);

  const toggleFavorite = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) return alert("Please log in to favorite events");

    if (isFavorited) {
      // Remove favorite
      await supabase
        .from("user_favorites")
        .delete()
        .eq("user_id", user.id)
        .eq("event_id", event.id);
      setIsFavorited(false);
    } else {
      // Add favorite
      await supabase
        .from("user_favorites")
        .insert([{ user_id: user.id, event_id: event.id }]);
      setIsFavorited(true);
    }
  };

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
    <div className="border p-4 rounded mb-4 shadow-sm relative group">
      {/* Favorite Button */}
      <button 
        onClick={toggleFavorite}
        className="absolute bottom-4 right-4 z-50 text-2xl"
      >
        {isFavorited ? "❤️" : "🤍"}
      </button>
      {user?.is_admin && (
        <div className="absolute top-4 right-4 flex gap-2 z-50">
          <button onClick={handleEdit} className="p-2 bg-white border rounded shadow-md hover:bg-gray-100">
            ✏️
          </button>
          <button onClick={handleDelete} className="p-2 bg-white border border-red-100 rounded shadow-md text-red-500 hover:bg-red-50">
            🗑️
          </button>
        </div>
      )}
      
      {/* CLICKABLE CONTENT */}
      <Link href={`/event/${event.id}`}>
        <div className="cursor-pointer hover:bg-gray-50 p-2 rounded">
          <h2 className="text-xl font-bold">{event.title}</h2>
          <p className="text-sm text-gray-600">{event.club_name}</p>
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