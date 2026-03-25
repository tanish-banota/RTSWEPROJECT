"use client";

import { useState } from "react";
import { mockEvents } from "../../lib/mockData";

export default function FeedPage() {
  const [search, setSearch] = useState("");
 const [rsvped, setRsvped] = useState<string[]>(() => {
  if (typeof window === "undefined") return [];
  const saved = localStorage.getItem("rsvpedEvents");
  return saved ? JSON.parse(saved) : [];
});

  const filtered = mockEvents.filter(
    (event) =>
      event.title.toLowerCase().includes(search.toLowerCase()) ||
      event.club.toLowerCase().includes(search.toLowerCase())
  );

 function handleRSVP(id: string) {
  if (!rsvped.includes(id)) {
    const updated = [...rsvped, id];
    setRsvped(updated);
    localStorage.setItem("rsvpedEvents", JSON.stringify(updated));
  }
}

  return (
    <div style={{ maxWidth: "700px", margin: "0 auto", padding: "32px 16px", fontFamily: "sans-serif" }}>
      
      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "4px" }}>
          🎓 Campus Event Feed
        </h1>
        <p style={{ color: "#666" }}>Discover and RSVP to clubs and events at your school</p>
      </div>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="🔍 Search events or clubs..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "100%",
          padding: "12px 16px",
          borderRadius: "10px",
          border: "1px solid #ddd",
          fontSize: "1rem",
          marginBottom: "24px",
          boxSizing: "border-box",
        }}
      />

      {/* Stats Bar */}
      <div style={{ display: "flex", gap: "16px", marginBottom: "24px" }}>
        <div style={{ background: "#EEF2FF", borderRadius: "8px", padding: "12px 20px", flex: 1, textAlign: "center" }}>
          <p style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#4F46E5" }}>{mockEvents.length}</p>
          <p style={{ fontSize: "0.8rem", color: "#666" }}>Total Events</p>
        </div>
        <div style={{ background: "#F0FDF4", borderRadius: "8px", padding: "12px 20px", flex: 1, textAlign: "center" }}>
          <p style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#16A34A" }}>{rsvped.length}</p>
          <p style={{ fontSize: "0.8rem", color: "#666" }}>RSVPs Made</p>
        </div>
        <div style={{ background: "#FFF7ED", borderRadius: "8px", padding: "12px 20px", flex: 1, textAlign: "center" }}>
          <p style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#EA580C" }}>{filtered.length}</p>
          <p style={{ fontSize: "0.8rem", color: "#666" }}>Showing</p>
        </div>
      </div>

      {/* Empty State */}
      {filtered.length === 0 ? (
        <div style={{ textAlign: "center", padding: "48px", color: "#999" }}>
          <p style={{ fontSize: "2rem" }}>🔎</p>
          <p style={{ fontSize: "1.1rem" }}>No events found for "{search}"</p>
        </div>
      ) : (
        filtered.map((event) => {
          const joined = rsvped.includes(event.id);
          return (
            <div
              key={event.id}
              style={{
                border: joined ? "2px solid #16A34A" : "1px solid #e5e7eb",
                borderRadius: "12px",
                padding: "20px",
                marginBottom: "16px",
                background: joined ? "#F0FDF4" : "white",
                boxShadow: "0 1px 4px rgba(0,0,0,0.06)",
                transition: "all 0.2s",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <h2 style={{ fontSize: "1.2rem", fontWeight: "bold", marginBottom: "6px" }}>
                    {event.title}
                  </h2>
                  <p style={{ color: "#555", marginBottom: "4px" }}>🏛️ {event.club}</p>
                  <p style={{ color: "#555", marginBottom: "4px" }}>📍 {event.location}</p>
                  <p style={{ color: "#555" }}>📅 {new Date(event.date).toLocaleString()}</p>
                </div>
                <button
                  onClick={() => handleRSVP(event.id)}
                  style={{
                    padding: "10px 20px",
                    borderRadius: "8px",
                    border: "none",
                    background: joined ? "#16A34A" : "#4F46E5",
                    color: "white",
                    fontWeight: "bold",
                    cursor: joined ? "default" : "pointer",
                    fontSize: "0.9rem",
                    whiteSpace: "nowrap",
                  }}
                >
                  {joined ? "Joined ✅" : "RSVP →"}
                </button>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}