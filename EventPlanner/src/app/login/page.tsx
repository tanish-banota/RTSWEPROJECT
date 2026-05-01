"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const {
    loginWithPassword,
    signUpWithPassword,
    loginWithGoogle,
    loading,
    error,
  } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async () => {
    setMessage(null);

    try {
      if (mode === "login") {
        await loginWithPassword(email, password);
      } else {
        await signUpWithPassword(email, password);
      }
      router.push("/feed");
    } catch (err) {
      setMessage("Please check your email and password and try again.");
    }
  };

  const handleGoogleLogin = async () => {
    setMessage(null);
    try {
      await loginWithGoogle();
    } catch (err) {
      setMessage("Google login failed. Please try again.");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-8">
      <div className="w-full max-w-md rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold mb-4">
          {mode === "login" ? "Login" : "Create Account"}
        </h1>

        <label className="block mb-3">
          <span className="text-sm text-gray-600">Email</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="mt-1 w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </label>

        <label className="block mb-4">
          <span className="text-sm text-gray-600">Password</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="mt-1 w-full rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </label>

        {(message || error) && (
          <p className="mb-3 text-sm text-red-600">{message || error}</p>
        )}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="mb-3 w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading
            ? "Working..."
            : mode === "login"
            ? "Login"
            : "Create account"}
        </button>

        <button
          onClick={handleGoogleLogin}
          type="button"
          className="mb-4 w-full rounded border border-gray-300 bg-white px-4 py-2 text-gray-700 hover:bg-gray-100"
        >
          Continue with Google
        </button>

        <div className="text-center text-sm text-gray-600">
          {mode === "login" ? (
            <>
              New here?{' '}
              <button
                type="button"
                onClick={() => setMode("register")}
                className="text-blue-600 hover:underline"
              >
                Create an account
              </button>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => setMode("login")}
                className="text-blue-600 hover:underline"
              >
                Login
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}