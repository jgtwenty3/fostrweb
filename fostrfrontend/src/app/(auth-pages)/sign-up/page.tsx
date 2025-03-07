"use client"

import React, { useState } from 'react'
import { Input } from '../Components/Input'
import Link from 'next/link'

export default function SignUpPage() {
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [phone, setPhone] = useState("")
  const [role, setRole] = useState("")

  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    // Replace with your actual sign-up logic
    try {
      // Example sign-up logic (replace with your backend request)
      console.log("Signing up with:", email, password)
      // On successful sign-up, redirect or handle success
    } catch (err) {
      setError("Invalid credentials. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex justify-center items-center min-h-screen">
      <form
        className="flex flex-col w-full max-w-sm px-4 py-6 rounded-lg shadow-lg sm:flex-1 sm:items-center border-2 border-darkBlue"
        onSubmit={handleSubmit}
      >
        <h1 className="text-2xl font-medium text-darkBlue text-center">Sign up</h1>
        <p className="text-sm text-darkBlue text-center">
          Already have an account?{' '}
          <Link className="text-fostrBlue font-medium underline" href="/sign-in">
            Sign in
          </Link>
        </p>
        {error && (
          <div className="text-red-500 text-sm text-center mt-2">
            {error}
          </div>
        )}
        <div className="flex flex-col gap-2 mt-4 text-fostrBlue">
        <label htmlFor="email" className="text-darkBlue text-left">First Name</label>
          <Input
            name="first_name"
            type="first_name"
            placeholder="Wilbert"
            required
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="mb-2"
          />
          <label htmlFor="email" className="text-darkBlue text-left">Last Name</label>
          <Input
            name="last_name"
            type="last_name"
            placeholder="Wilbert"
            required
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className="mb-2"
          />
          <label htmlFor="email" className="text-darkBlue text-left">Email</label>
          <Input
            name="email"
            type="email"
            placeholder="you@example.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mb-2"
          />
          <label htmlFor="role" className="text-darkBlue text-left">Role</label>
          <Input
            name="role"
            type="role"
            placeholder="admin"
            required
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="mb-2"
          />
          <label htmlFor="password" className="text-darkBlue text-left">Password</label>
          <Input
            type="password"
            name="password"
            placeholder="Your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mb-2"
          />
          <button
            type="submit"
            className="bg-fostrBlue hover:bg-blue-700 text-white px-4 py-2 uppercase mt-4"
            disabled={loading}
          >
            {loading ? "Signing Up..." : "Sign Up"}
          </button>
        </div>
      </form>
    </div>
  )
}
