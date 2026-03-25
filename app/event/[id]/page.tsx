import { mockEvents } from "@/lib/mockData";

export default function EventDetail({ params }: { params: { id: string } }) {
  const event = mockEvents.find(e => e.id == Number(params.id));

  if (!event) return <p>Event not found</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl">{event.title}</h1>
      <p>{event.club}</p>
      <p>{event.description}</p>
      <p>{new Date(event.date).toLocaleString()}</p>
    </div>
  );
}