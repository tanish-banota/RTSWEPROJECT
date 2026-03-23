import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Login Page</h1>

      <Link href="/feed" className="text-blue-500 underline">
        Go to Feed →
      </Link>
    </div>
  );
}