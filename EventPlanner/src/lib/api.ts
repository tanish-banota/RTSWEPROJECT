// lib/api.ts
export type Event = {
  id: string;
  title: string;
  date: string;
  club_name: string;
  location: string;
  description: string;
  tags?: string[];
};

export const getEvents = async (): Promise<Event[]> => {
  const res = await fetch("http://localhost:5000/events");
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
};
// fetching data from backend 