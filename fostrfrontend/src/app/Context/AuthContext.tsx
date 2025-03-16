"use client"
import React, { createContext, useState, useEffect, ReactNode } from "react";
import { useRouter } from 'next/navigation'


interface AuthContextType {
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
  } | null;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthContextType['user']>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch(`${API_URL}/check_session`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include", // Ensure cookies are included if needed
        });


        const data = await response.json();
        

        // Map session data to match your context structure
        setUser({
          id: data.id, // Use the 'id' from the session data
          name: `${data.first_name} ${data.last_name}`, // Combine first and last name
          email: data.email, // Use the 'email' from the session data
          role: data.role, // Use the 'role' from the session data
        });
      } catch (error) {
        console.error("Session check error:", error);
        setUser(null);
      } finally {
        setLoading(false);
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
