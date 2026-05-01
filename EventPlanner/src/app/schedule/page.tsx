"use client";

import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function ScheduleRootPage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  if (loading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-600">Loading schedule...</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Your Schedule</h1>
      <p className="mb-6 text-gray-600">
        Choose a view to see the events you have RSVP'd for.
      </p>

      <div className="grid gap-4 sm:grid-cols-2">
        <Link
          href="/schedule/week"
          className="rounded-3xl border border-gray-200 bg-white p-6 text-center shadow-sm transition hover:border-blue-300 hover:shadow-md"
        >
          <h2 className="text-xl font-semibold mb-2">Weekly Schedule</h2>
          <p className="text-sm text-gray-600">See RSVP'd events for the current week.</p>
        </Link>

        <Link
          href="/schedule/month"
          className="rounded-3xl border border-gray-200 bg-white p-6 text-center shadow-sm transition hover:border-blue-300 hover:shadow-md"
        >
          <h2 className="text-xl font-semibold mb-2">Monthly Schedule</h2>
          <p className="text-sm text-gray-600">See RSVP'd events for the current month.</p>
        </Link>
      </div>
    </div>
  );
}
