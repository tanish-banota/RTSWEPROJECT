import Link from "next/link";

export default function Home() {
  return (
    <div className="p-6">
      <h1 className="text-2x1 font-bold">Club Finder</h1>

      <Link href="/login" className="text-blue-500 underline">
        Go to Login
      </Link>

      <Link href="/feed" className="text-blue-500 underline">
        Go to Feed
      </Link>
    </div>
  );
}
