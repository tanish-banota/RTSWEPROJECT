"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabaseClient";
import { useAuth } from "@/context/AuthContext";
import EventCard from "@/components/EventCard";

export default function FavoritesPage() {
  const { user } = useAuth();
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchFavorites = async () => {
      setLoading(true);
      // Fetch user_favorites and join with events table[cite: 3, 11]
      const { data, error } = await supabase
        .from("user_favorites")
        .select(`
          event_id,
          events (*)
        `)
        .eq("user_id", user.id);

      if (data) {
        // Extract the nested event objects[cite: 11]
        setEvents(data.map(fav => fav.events));
      }
      setLoading(false);
    };

    fetchFavorites();
  }, [user]);

  if (loading) return <p className="p-6">Loading favorites...</p>;
  if (events.length === 0) return <p className="p-6 text-center">No favorites yet! Go find some events. ❤️</p>;

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Your Favorite Events</h1>
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}