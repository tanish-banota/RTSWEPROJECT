"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useAuth } from "@/context/AuthContext";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (pathname === "/" || pathname === "/login") {
    return null;
  }

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  return (
    <div className="flex justify-between items-center p-4 border-b bg-white shadow-sm z-10">
      <div className="flex items-center gap-6">
        <Link href={user ? "/feed" : "/"} className="font-bold text-lg">
          Event Finder
        </Link>
        {user?.is_admin && (
          <Link 
            href="/admin/add-event" 
            className="bg-green-600 text-white px-3 py-1 rounded-md text-sm hover:bg-green-700"
          >
            + Add Event
          </Link>
        )}
        {user && (
          <>
            <Link href="/favorites" className="text-sm text-gray-700 hover:text-blue-600">
               Favorites
            </Link>
            <Link href="/schedule/week" className="text-sm text-gray-700 hover:text-blue-600">
              Weekly
            </Link>
            <Link href="/schedule/month" className="text-sm text-gray-700 hover:text-blue-600">
              Monthly
            </Link>
          </>
        )}
      </div>

      {user ? (
        <div className="relative" ref={menuRef}>
          <button
            type="button"
            onClick={() => setOpen((prev) => !prev)}
            className="flex items-center gap-2 rounded-full border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-blue-500 text-white shadow-sm">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="h-5 w-5"
              >
                <path d="M12 12c2.7 0 4.9-2.2 4.9-4.9S14.7 2.2 12 2.2 7.2 4.4 7.2 7.1 9.3 12 12 12zm0 2.2c-3.2 0-9.6 1.6-9.6 4.9v1.6h19.2v-1.6c0-3.3-6.4-4.9-9.6-4.9z" />
              </svg>
            </span>
            <span>{user.email?.split("@")[0]}</span>
          </button>

          {open && (
            <div className="absolute right-0 mt-2 w-44 rounded-xl border border-gray-200 bg-white p-2 shadow-lg">
              <button
                type="button"
                onClick={() => {
                  router.push("/settings");
                  setOpen(false);
                }}
                className="w-full rounded-lg px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100"
              >
                Settings
              </button>
              <button
                type="button"
                onClick={handleLogout}
                className="mt-1 w-full rounded-lg px-3 py-2 text-left text-sm text-red-600 hover:bg-red-50"
              >
                Log out
              </button>
            </div>
          )}
        </div>
      ) : (
        <Link href="/login" className="text-sm text-blue-600 hover:text-blue-800">
          Login
        </Link>
      )}
    </div>
  );
}