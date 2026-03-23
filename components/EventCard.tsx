"use client";

type Event = {
  id: string;
  title: string;
  date: string;
  club: string;
  location: string;
};

interface EventCardProps {
  event: Event;
}

export default function EventCard({ event }: EventCardProps) {
  return (
    <div className="border p-4 rounded mb-4">
      <h2 className="text-xl font-bold">{event.title}</h2>
      <p>{event.club}</p>
      <p>{new Date(event.date).toLocaleString()}</p>
      <p>{event.location}</p>
     <button
  className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
  onClick={() =>
    fetch(`/rsvp/${event.id}`, { method: "POST" })
      .then(() => alert("RSVP sent!"))//replace the alert with UI state updates (like disabling the button after RSVP)
      .catch(() => alert("Failed to RSVP"))
  }
>
  RSVP
</button>
    </div>
  );
}