import Image from "next/image";

export default function LandingPage() {
  return (
    <div className="relative min-h-screen">
      {/* Navbar */}
      <nav className="flex justify-between items-center w-full bg-background text-foreground border-b-2 border-darkBlue">
        {/* Logo */}
        <div className="px-2 py-1">
          <Image src ="images/fostr.svg" alt = "logo" width={75} height={75}/>
        </div>
        
        {/* Navigation Buttons */}
        <div className="hidden md:flex space-x-6 p-5">
          <button className="bg-fostrBlue hover:bg-darkBlue text-white px-4 py-2 uppercase">Sign In</button>
          <button className="bg-fostrBlue hover:bg-darkBlue text-white px-4 py-2 uppercase ">Sign Up</button>
        </div>

        {/* Mobile menu (Hamburger) */}
        <div className="md:hidden flex items-center space-x-2">
          <button className="text-white">☰</button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex justify-center items-center flex-1 bg-background p-4">
        <h1 className="text-8xl font-bold text-center text-foreground">Welcome to Fostr</h1>
        <div>

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-fostrBlue text-white p-4 text-center">
        <p>&copy; 2025 MyCompany. All rights reserved.</p>
      </footer>
    </div>
  );
}
