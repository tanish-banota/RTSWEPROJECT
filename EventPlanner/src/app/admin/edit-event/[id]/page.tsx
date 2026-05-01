"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { supabase } from "@/lib/supabaseClient";
import { useAuth } from "@/context/AuthContext";

export default function EditEventPage() {
  const router = useRouter();
  const { id } = useParams();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: "",
    club: "",
    date: "",
    location: "",
    description: "",
    tags: "",
  });

  // Security: Admin check
  useEffect(() => {
    if (!user?.is_admin) return;

    const fetchEvent = async () => {
      const { data, error } = await supabase
        .from("events")
        .select("*")
        .eq("id", id)
        .single(); // Get the specific event[cite: 12]

      if (data) {
        setFormData({
            ...data,
            club: data.club_name,
            date: data.start_time || "", // Load from 'start_time' column[cite: 8, 12]
            tags: data.tags ? data.tags.join(", ") : "",
        });
        }
      setLoading(false);
    };

    fetchEvent();
  }, [id, user]);

  if (!user?.is_admin) return <p className="p-6">Access Denied.</p>;
  if (loading) return <p className="p-6">Loading event data...</p>;

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const { error } = await supabase
        .from("events")
        .update({
            title: formData.title,
            club_name: formData.club,
            start_time: formData.date, // Save state 'date' back to 'start_time'[cite: 8]
            location: formData.location,
            description: formData.description,
            tags: formData.tags.split(",").map((t) => t.trim()),
        })
        .eq("id", id);

    if (error) {
      alert(error.message);
    } else {
      router.push("/feed"); // Return to discovery feed[cite: 11]
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-6">Edit Event</h1>
      <form onSubmit={handleUpdate} className="space-y-4">
        <label className="block text-sm font-medium text-gray-700">Title</label>
        <input
          value={formData.title}
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
        
        <label className="block text-sm font-medium text-gray-700">Club</label>
        <input
          value={formData.club}
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, club: e.target.value })}
          required
        />

        <label className="block text-sm font-medium text-gray-700">Date & Time</label>
        <input
          type="datetime-local"
          value={formData.date ? new Date(formData.date).toISOString().slice(0, 16) : ""}
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, date: e.target.value })}
          required
        />

        <label className="block text-sm font-medium text-gray-700">Location</label>
        <input
          value={formData.location}
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          required
        />

        <label className="block text-sm font-medium text-gray-700">Description</label>
        <textarea
          value={formData.description}
          className="w-full p-2 border rounded h-32"
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />

        <label className="block text-sm font-medium text-gray-700">Tags (comma separated)</label>
        <input
          value={formData.tags}
          className="w-full p-2 border rounded"
          onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
        />

        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => router.back()}
            className="w-1/2 border border-gray-300 py-2 rounded hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="w-1/2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Saving..." : "Update Event"}
          </button>
        </div>
      </form>
    </div>
  );
}