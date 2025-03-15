"use client"
import React, { createContext, useState, useEffect, ReactNode } from 'react';

// Define user type
interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role?: string;
}

// Define context type
interface SessionContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  checkSession: () => void;
}

// Create context
const SessionContext = createContext<SessionContextType | undefined>(undefined);

type SessionProviderProps = {
  children: ReactNode;
};

export const SessionProvider = ({ children }: SessionProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check session function
  const checkSession = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/check_session`, {
        method: "GET",
        credentials: "include",  // Ensure cookies are sent with the request
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Session check failed");
      }

      const userData = await res.json();
      setUser(userData); // Set user data
    } catch (error) {
      console.error("Session check error:", error);
      setError("You are not logged in.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkSession(); // Check session when the app mounts
  }, []);

  return (
    <SessionContext.Provider value={{ user, loading, error, checkSession }}>
      {children}
    </SessionContext.Provider>
  );
};

// Custom hook to access session data
export const useSession = (): SessionContextType => {
  const context = React.useContext(SessionContext);
  if (!context) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
};
