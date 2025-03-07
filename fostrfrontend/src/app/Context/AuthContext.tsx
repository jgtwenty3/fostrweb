"use client"
import React, { createContext, useState, useEffect, ReactNode } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL; // Accessing the API URL

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch(`${API_URL}/check_session`, {
          method: "GET",
          credentials: "include", // Ensure cookies are sent with the request
        });

        if (!response.ok) {
          throw new Error("Unauthorized");
        }

        const data = await response.json();
        setUser(data); // Set the user if logged in
      } catch (error) {
        setUser(null); // If an error occurs, the user is not logged in
      } finally {
        setLoading(false); // Loading is complete
      }
    };

    checkSession();
  }, [API_URL]);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
