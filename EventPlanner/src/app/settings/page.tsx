"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function SettingsPage() {
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
        <p className="text-gray-600">Loading user information...</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Settings</h1>
      <div className="rounded-3xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-3">User information</h2>
        <div className="grid gap-4 text-sm text-gray-700">
          <div>
            <p className="font-medium text-gray-900">Email</p>
            <p>{user.email}</p>
          </div>
          <div>
            <p className="font-medium text-gray-900">User ID</p>
            <p>{user.id}</p>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <button
          type="button"
          onClick={() => router.push("/feed")}
          className="rounded-full bg-blue-600 px-5 py-2 text-white hover:bg-blue-700"
        >
          Back to feed
        </button>
      </div>
    </div>
  );
}
