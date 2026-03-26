"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();
  
  // Hide navbar on home page
  if (pathname === "/") {
    return null;
  }

  return (
    <div className="flex justify-between items-center p-4 border-b">
      <Link href="/" className="font-bold text-lg">
        Event Finder
      </Link>

      <Link href="/login" className="text-sm">
        Login
      </Link>
    </div>
  );
}