import Link from "next/link";

export default function Navbar() {
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