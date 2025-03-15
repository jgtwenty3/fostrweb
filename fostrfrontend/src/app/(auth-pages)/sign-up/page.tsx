"use client"

import React, { useState } from 'react'
import { Input } from '../Components/Input'
import Link from 'next/link'
import { createShelter, signUp } from '@/app/lib/api/api'

export default function SignUpPage() {
  const [step, setStep] = useState(1)
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [role, setRole] = useState("")

  const [shelterName, setShelterName] = useState("")
  const [shelterEmail, setShelterEmail] = useState("")
  const [shelterPhone, setShelterPhone] = useState("")
  const [shelterStreetAddress, setShelterStreetAddress] = useState("")
  const [shelterCity, setShelterCity] = useState("")
  const [shelterState, setShelterState] = useState("")
  const [shelterZipcode, setShelterZipcode] = useState("")
  const [shelterAbout, setShelterAbout] = useState("")

  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
  
    try {
      if (step === 1 && role === "owner") {
        setStep(2);
        setLoading(false);
        return;
      }
  
      console.log("Signing up user:", { firstName, lastName, email, password, role });
  
      // Sign up the user
      const userResponse = await signUp({ first_name: firstName, last_name: lastName, email, password, role });
  
      console.log("User signed up successfully:", userResponse);

      
  
      // Create shelter if role is owner
      if (role === "owner") {
        console.log("Creating shelter:", { shelterName, shelterEmail, shelterPhone });
        const shelterResponse = await createShelter({
          name: shelterName,
          email: shelterEmail,
          phone: shelterPhone,
          streetAddress: shelterStreetAddress,
          city: shelterCity,
          state: shelterState,
          zipcode: shelterZipcode,
          about: shelterAbout,
        });
        console.log("Shelter created successfully:", shelterResponse);
      }
  
      // Handle success (Redirect, show success message, etc.)
    } catch (err: any) {
      console.error("Error during sign-up:", err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="flex justify-center items-center min-h-screen">
      <form
        className="flex flex-col w-full max-w-sm px-4 py-6 rounded-lg shadow-lg sm:flex-1 border-2 border-darkBlue"
        onSubmit={handleSubmit}
      >
        <h1 className="text-2xl font-medium text-darkBlue text-center uppercase">Sign up</h1>
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

        {step === 1 && (
          <div className="flex flex-col gap-2 mt-4 text-fostrBlue">
            <label htmlFor="first_name" className="text-darkBlue text-left font-semibold">First Name</label>
            <Input
              name="first_name"
              type="text"
              placeholder="Wilbert"
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="last_name" className="text-darkBlue text-left font-semibold">Last Name</label>
            <Input
              name="last_name"
              type="text"
              placeholder="Wilbert"
              required
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="email" className="text-darkBlue text-left font-semibold">Email</label>
            <Input
              name="email"
              type="email"
              placeholder="you@example.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="role" className="text-darkBlue text-left font-semibold">Role</label>
            <select
              name="role"
              required
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="mb-2 px-2 py-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-fostrBlue"
            >
              <option value="" disabled>Select your role</option>
              <option value="owner">Owner</option>
              <option value="user">User</option>
            </select>
            <label htmlFor="password" className="text-darkBlue text-left font-semibold">Password</label>
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
              {loading ? "Next" : "Next"}
            </button>
          </div>
        )}

        {step === 2 && role === "owner" && (
          <div className="flex flex-col gap-2 mt-4 text-fostrBlue">
            <label htmlFor="shelterName" className="text-darkBlue text-left font-semibold">Shelter Name</label>
            <Input
              name="shelterName"
              type="text"
              placeholder="Happy Paws Shelter"
              required
              value={shelterName}
              onChange={(e) => setShelterName(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterEmail" className="text-darkBlue text-left font-semibold">Shelter Email</label>
            <Input
              name="shelterEmail"
              type="email"
              placeholder="shelter@example.com"
              required
              value={shelterEmail}
              onChange={(e) => setShelterEmail(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterPhone" className="text-darkBlue text-left font-semibold">Shelter Phone</label>
            <Input
              name="shelterPhone"
              type="text"
              placeholder="(555) 555-5555"
              value={shelterPhone}
              onChange={(e) => setShelterPhone(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterStreetAddress" className="text-darkBlue text-left font-semibold">Street Address</label>
            <Input
              name="shelterStreetAddress"
              type="text"
              placeholder="1234 Shelter St"
              required
              value={shelterStreetAddress}
              onChange={(e) => setShelterStreetAddress(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterCity" className="text-darkBlue text-left font-semibold">City</label>
            <Input
              name="shelterCity"
              type="text"
              placeholder="City"
              required
              value={shelterCity}
              onChange={(e) => setShelterCity(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterState" className="text-darkBlue text-left font-semibold">State</label>
            <Input
              name="shelterState"
              type="text"
              placeholder="State"
              required
              value={shelterState}
              onChange={(e) => setShelterState(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterZipcode" className="text-darkBlue text-left font-semibold">Zipcode</label>
            <Input
              name="shelterZipcode"
              type="text"
              placeholder="12345"
              required
              value={shelterZipcode}
              onChange={(e) => setShelterZipcode(e.target.value)}
              className="mb-2"
            />
            <label htmlFor="shelterAbout" className="text-darkBlue text-left font-semibold">About</label>
            <textarea
              name="shelterAbout"
              placeholder="About the shelter"
              value={shelterAbout}
              onChange={(e) => setShelterAbout(e.target.value)}
              className="mb-2 px-2 py-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-fostrBlue"
            />
            <button
              type="submit"
              className="bg-fostrBlue hover:bg-blue-700 text-white px-4 py-2 uppercase mt-4"
              disabled={loading}
            >
              {loading ? "Signing Up..." : "Sign Up"}
            </button>
          </div>
        )}
      </form>
    </div>
  )
}
