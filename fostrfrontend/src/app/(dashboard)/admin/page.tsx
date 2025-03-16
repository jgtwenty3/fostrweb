"use client"
import React, { useEffect, useState } from 'react';
import { checkSession } from '@/app/lib/api/api';  // Assuming the checkSession function is imported

type Props = {}

interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role?: string;
}

export default function AdminDashBoard({}: Props) {
  const [user, setUser] = useState<User | null>(null);
  // const [loading, setLoading] = useState<boolean>(true);
  // const [error, setError] = useState<string | null>(null);

  // const verifySession = async () => {
  //   try {
  //     const sessionData = await checkSession();  // Call your checkSession function
  //     setUser(sessionData); 
  //     console.log(sessionData)// Set the user data on successful session check
  //   } catch (err) {
  //     setError('You are not logged in or session expired');
  //     console.error('Session check error:', err);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  // useEffect(() => {
  //   verifySession();  // Check session when the component mounts
  // }, []);

  // if (loading) {
  //   return <div>Loading...</div>;
  // }

  // if (error) {
  //   return <div>{error}</div>;
  // }

  return (
    <div>
      <h1>Welcome to the Admin Dashboard</h1>
      <p>Hello, {user?.first_name} {user?.last_name}</p>
      <p>Email: {user?.email}</p>
      {user?.role && <p>Role: {user.role}</p>}
    </div>
  );
}
