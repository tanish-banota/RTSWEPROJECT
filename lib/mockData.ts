export type Event = {
  id: string;
  title: string;
  date: string;
  club: string;
  location: string;
};

export const mockEvents: Event[] = [
  { id: "1", title: "Chess Club Meetup", date: "2026-03-21T18:00:00Z", club: "Chess Club", location: "Room 101" },
  { id: "2", title: "Hackathon Kickoff", date: "2026-03-22T10:00:00Z", club: "Coding Club", location: "Auditorium" },
  { id: "3", title: "Art Workshop", date: "2026-03-23T14:00:00Z", club: "Art Club", location: "Studio 5" },
  { id: "4", title: "Soccer Tryouts", date: "2026-03-25T15:00:00Z", club: "Soccer Club", location: "Main Field" },
  { id: "5", title: "Photography Walk", date: "2026-03-26T11:00:00Z", club: "Photography Club", location: "Campus Garden" },
  { id: "6", title: "Debate Practice", date: "2026-03-27T17:00:00Z", club: "Debate Club", location: "Room 204" },
];