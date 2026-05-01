"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabaseClient";
import { useAuth } from "@/context/AuthContext";

export default function AddEventPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    club: "",
    date: "",
    location: "",
    description: "",
    tags: "",
  });

  // Security check: Redirect if not an admin[cite: 1]
  if (!user?.is_admin) {
    return <p className="p-6">Access Denied.</p>;
  }

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);

  const { error } = await supabase.from("events").insert([
    {
      title: formData.title,
      club_name: formData.club, // Map 'club' state to 'club_name' column[cite: 13]
      start_time: formData.date,
      location: formData.location,
      description: formData.description,
      tags: formData.tags.split(",").map((t) => t.trim()),
    },
  ]);

  if (error) {
    alert(error.message);
  } else {
    router.push("/feed");
  }
  setLoading(false);
};

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-6">Add New Event</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          placeholder="Event Title"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
        <input
          placeholder="Club Name"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, club: e.target.value })}
          required
        />
        <input
          type="datetime-local"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          required
        />
        <input
          placeholder="Location"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          required
        />
        <textarea
          placeholder="Description"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
        <input
          placeholder="Tags (comma separated)"
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Saving..." : "Create Event"}
        </button>
      </form>
    </div>
  );
}