"use client"
import Link from 'next/link'
import React, { useContext, useEffect, useState } from 'react'
import { Input } from '../Components/Input'
import { login } from '@/app/lib/api/api'
import { useRouter } from 'next/navigation'
import { AuthContext } from '@/app/Context/AuthContext'

export default function SignInPage() {
  const { user, loading: userLoading } = useContext(AuthContext);
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    if (user) {
      // Redirect based on the user's role
      if (user.role === 'User') {
        router.push("/UserFeed");
      } else if (user.role === 'Owner') {
        router.push("/admin");
      }
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const loggedInUser = await login({ email, password });

      console.log("User logged in:", loggedInUser);
      router.push("/admin"); // Change to the route you want after login
    } catch (err) {
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Check if user data is available and loading is done
  if (userLoading) {
    return <div>Loading...</div>; // You can return a loading state while waiting for user data
  }

  console.log(user);

  return (
    <div className="flex justify-center items-center min-h-screen">
      <form
        className="flex flex-col w-full max-w-sm px-4 py-6 rounded-lg shadow-lg sm:flex-1 border-2 border-darkBlue"
        onSubmit={handleSubmit}
      >
        <h1 className="text-2xl font-medium text-darkBlue text-center uppercase ">Sign in</h1>
        <p className="text-sm text-darkBlue text-center">
          Don't have an account?{' '}
          <Link className="text-fostrBlue font-medium underline" href="/sign-up">
            Sign up
          </Link>
        </p>
        {error && (
          <div className="text-red-500 text-sm text-center mt-2">
            {error}
          </div>
        )}
        
        <div className="flex flex-col gap-4 mt-8 text-fostrBlue">
        <label htmlFor="email" className="text-darkBlue font-semibold">Email </label>
          <Input
            name="email"
            type="email"
            placeholder="you@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className=''
          />
          <div className="flex justify-between items-center">
            <label htmlFor="password" className="text-darkBlue font-semibold">Password </label>
          </div>
          <Input
            type="password"
            name="password"
            placeholder="Your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Link
              className="text-xs underline text-fostrBlue ml-2"
              href="/forgot-password"
            >
              Forgot Password?
            </Link>
          <button
            type="submit"
            className="bg-fostrBlue hover:bg-blue-700 text-white px-4 py-2 uppercase mt-4 rounded-full"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </div>
      </form>
    </div>
  )
}
