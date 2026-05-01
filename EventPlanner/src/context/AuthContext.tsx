"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { supabase } from "@/lib/supabaseClient";
import type { Session } from "@supabase/supabase-js";

let authSessionPromise: Promise<Session | null> | null = null;

async function getSessionOnce(): Promise<Session | null> {
  if (authSessionPromise) {
    return authSessionPromise;
  }

  authSessionPromise = supabase.auth.getSession().then(({ data: { session }, error }) => {
    if (error) {
      authSessionPromise = null;
      throw error;
    }
    return session;
  });

  return authSessionPromise;
}

type User = {
  id: string;
  email: string;
  is_admin: boolean;
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  error: string | null;
  loginWithPassword: (email: string, password: string) => Promise<void>;
  signUpWithPassword: (email: string, password: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

function userFromSession(session: Session | null, isAdmin: boolean = false): User | null {
  if (!session?.user) return null;
  return {
    id: session.user.id,
    email: session.user.email ?? "",
    is_admin: isAdmin,
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    const loadSession = async () => {
      try {
        const session = await getSessionOnce();
        if (!active) return;

        if (session?.user) {
          // Fetch the admin flag from the profiles table
          const { data } = await supabase
            .from("profiles")
            .select("is_admin")
            .eq("id", session.user.id)
            .single();
          
          setUser(userFromSession(session, !!data?.is_admin));
        } else {
          setUser(null);
        }
      } catch (err) {
        if (!active) return;
        setError((err as Error)?.message ?? "Failed to load session");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadSession();

    const { data } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        if (!active) return;
        setUser(userFromSession(session));
      }
    );

    return () => {
      active = false;
      data?.subscription.unsubscribe();
    };
  }, []);

  const loginWithPassword = async (email: string, password: string) => {
    setError(null);
    setLoading(true);

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      throw error;
    }

    setUser(userFromSession(data.session));
    setLoading(false);
  };

  const signUpWithPassword = async (email: string, password: string) => {
    setError(null);
    setLoading(true);

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      throw error;
    }

    setUser(userFromSession(data.session));
    setLoading(false);
  };

  const loginWithGoogle = async () => {
    setError(null);
    setLoading(true);

    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/feed`,
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      throw error;
    }

    setLoading(false);
  };

  const logout = async () => {
    setError(null);
    setLoading(true);
    await supabase.auth.signOut();
    setUser(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        loginWithPassword,
        signUpWithPassword,
        loginWithGoogle,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("AuthContext missing");
  return context;
}