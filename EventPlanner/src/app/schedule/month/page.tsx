"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import { useAuth } from "@/context/AuthContext";
import { supabase } from "@/lib/supabaseClient";

type EventRecord = {
  id: string;
  title: string;
  start_time?: string;
  date?: string;
  description?: string;
  location?: string;
};

type CalendarEvent = {
  id: string;
  title: string;
  start: string;
  extendedProps: {
    location: string | undefined;
    description: string | undefined;
  };
};

function getMonthRange(date: Date) {
  const start = new Date(date.getFullYear(), date.getMonth(), 1);
  start.setHours(0, 0, 0, 0);

  const end = new Date(date.getFullYear(), date.getMonth() + 1, 0);
  end.setHours(23, 59, 59, 999);

  return { start, end };
}

export default function MonthlySchedulePage() {
  const router = useRouter();
  const calendarRef = useRef<any>(null);
  const [calendarApi, setCalendarApi] = useState<any>(null);
  const { user, loading } = useAuth();
  const [rsvpdIds, setRsvpdIds] = useState<string[]>([]);
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [range, setRange] = useState(getMonthRange(new Date()));
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const handleCalendarNav = (action: "prev" | "next" | "today") => {
    const api = calendarApi || calendarRef.current?.getApi();
    if (!api) return;
    if (action === "prev") api.prev();
    if (action === "next") api.next();
    if (action === "today") api.today();
  };

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  useEffect(() => {
    if (!user) return;

    const fetchProfile = async () => {
      try {
        setLoadingData(true);
        setError(null);

        const { data, error } = await supabase
          .from("profiles")
          .select("rsvpd_events")
          .eq("id", user.id)
          .single();

        if (error) {
          const noRow =
            error.code === "PGRST116" ||
            error.message?.includes("Results contain 0 rows");

          if (noRow) {
            setRsvpdIds([]);
            return;
          }

          setError(error.message);
          setRsvpdIds([]);
          return;
        }

        setRsvpdIds(data?.rsvpd_events ?? []);
      } catch (err) {
        setError((err as Error).message ?? "Failed to load profile");
        setRsvpdIds([]);
      } finally {
        setLoadingData(false);
      }
    };

    fetchProfile();
  }, [user]);

  useEffect(() => {
    if (!user) {
      setEvents([]);
      setLoadingData(false);
      return;
    }

    const normalizedIds = Array.isArray(rsvpdIds)
      ? rsvpdIds
      : rsvpdIds
      ? [String(rsvpdIds)]
      : [];

    if (normalizedIds.length === 0) {
      setEvents([]);
      setLoadingData(false);
      return;
    }

    const fetchEvents = async () => {
      try {
        setLoadingData(true);
        setError(null);

        const { data, error } = await supabase
          .from("events")
          .select("id,title,start_time,date,description,location")
          .in("id", normalizedIds);

        if (error) {
          setError(error.message);
          setEvents([]);
          return;
        }

        const mapped = (data ?? [])
          .map((event: EventRecord) => {
            const startValue = event.start_time ?? event.date;
            if (!startValue) return null;

            const startDate = new Date(startValue);
            if (Number.isNaN(startDate.getTime())) return null;
            if (startDate < range.start || startDate > range.end) return null;

            return {
              id: event.id,
              title: event.title,
              start: startDate.toISOString(),
              extendedProps: {
                location: event.location,
                description: event.description,
              },
            };
          })
          .filter((event): event is CalendarEvent => event !== null);

        setEvents(mapped);
      } catch (err) {
        setError((err as Error).message ?? "Failed to load events");
        setEvents([]);
      } finally {
        setLoadingData(false);
      }
    };

    fetchEvents();
  }, [user, rsvpdIds, range]);

  const calendarEvents = useMemo(() => events, [events]);

  const monthLabel = useMemo(() => {
    return new Intl.DateTimeFormat("en-US", {
      month: "long",
      year: "numeric",
    }).format(range.start);
  }, [range.start]);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-3">Monthly Schedule</h1>
      <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Viewing</p>
          <h2 className="text-2xl font-semibold text-slate-900">{monthLabel}</h2>
        </div>
        <p className="text-gray-600">Only RSVP'd events are shown for the selected month.</p>
      </div>

      {error && (
        <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {loadingData && (
        <p className="mb-4 text-gray-600">Loading events...</p>
      )}
      <>
        <div className="mb-4 flex flex-wrap items-center gap-2">
          <button
            type="button"
            className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50"
            onClick={() => handleCalendarNav("prev")}
          >
              Previous
            </button>
            <button
              type="button"
              className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50"
              onClick={() => handleCalendarNav("today")}
            >
              Today
            </button>
            <button
              type="button"
              className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50"
              onClick={() => handleCalendarNav("next")}
            >
              Next
            </button>
          </div>
          <FullCalendar
            ref={calendarRef}
            plugins={[dayGridPlugin, interactionPlugin]}
            initialView="dayGridMonth"
            events={calendarEvents}
            eventDisplay="block"
            dayMaxEventRows={3}
            headerToolbar={false}
            height="auto"
            datesSet={(arg) => {
              if (calendarApi !== arg.view.calendar) {
                setCalendarApi(arg.view.calendar);
              }

              const monthStart = arg.view.currentStart ?? arg.start;
              const monthEnd = arg.view.currentEnd ?? arg.end;

              if (
                monthStart.valueOf() !== range.start.valueOf() ||
                monthEnd.valueOf() !== range.end.valueOf()
              ) {
                setRange({ start: monthStart, end: monthEnd });
              }
            }}
            eventContent={(arg) => (
              <div className="max-w-full rounded-xl bg-white px-2 py-1 text-left text-sm shadow-sm text-slate-900 whitespace-normal break-words">
                <strong className="block text-[0.78rem] leading-tight">
                  {arg.event.title}
                </strong>
                {arg.event.extendedProps.location && (
                  <div className="mt-1 text-[0.68rem] text-slate-600 break-words">
                    {arg.event.extendedProps.location}
                  </div>
                )}
              </div>
            )}
          />
        </>
    </div>
  );
}
