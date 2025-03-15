const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function signUp(userData: {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  role?: string;
}) {
  try {
    const res = await fetch(`${API_BASE_URL}/sign-up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(userData),
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "Signup failed");
    }

    return res.json();
  } catch (error) {
    console.error("Signup error:", error);
    throw error;
  }
}

export async function login(credentials: { email: string; password: string }) {
  try {
    const res = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Ensure cookies are included
      body: JSON.stringify(credentials),
    });

    // Log response headers to check if Set-Cookie is present
    console.log('Login Response Headers:', res.headers);

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "Login failed");
    }

    const data = await res.json();
    console.log('Login Response Body:', data); // Log response body for user data

    return data; // Includes user data with role
  } catch (error) {
    console.error("Login error:", error);
    throw error;
  }
}



export async function logout() {
  try {
    const res = await fetch(`${API_BASE_URL}/logout`, {
      method: "DELETE",
      credentials: "include",
    });

    if (!res.ok) throw new Error("Failed to log out");

    return null; // Returning `null` for consistency
  } catch (error) {
    console.error("Logout failed:", error);
    return null;
  }
}

export async function checkSession() {
  try {
    const res = await fetch(`${API_BASE_URL}/check_session`, {
      method: "GET",
      credentials: "include", // Ensure cookies are sent with the request
    });

    console.log('Check Session Request Headers:', res.headers);  // Log request headers

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "Session check failed");
    }

    return res.json();  // Returns user data if session is valid
  } catch (error) {
    console.error("Session check error:", error);
    throw error;
  }
}



export async function createShelter(shelterData:{
  name:string,
  email:string,
  phone:string,
  streetAddress: string,
  city:string,
  state:string,
  zipcode:string,
  about?:string;
}){
  try{
    const res = await fetch(`${API_BASE_URL}/shelters`,{
      method:"POST",
      headers:{"Content-Type": "application/json"},
      credentials:"include",
      body:JSON.stringify(shelterData)
    });
    if (!res.ok){
      const errorData = await res.json();
      throw new Error(errorData.error||"shetler creation failed")
    }
    return res.json()
  } catch(error){
    console.error("Shelter creation error", error);
    throw error;
  }
}

