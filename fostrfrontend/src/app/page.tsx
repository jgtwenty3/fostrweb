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
          <a href ="/sign-in">
            <button className="bg-fostrBlue hover:bg-darkBlue text-white px-4 py-2 uppercase rounded-full">Sign In</button>
          </a>
          <a href ="/sign-up">
            <button className="bg-fostrBlue hover:bg-darkBlue text-white px-4 py-2 uppercase rounded-full ">Sign Up</button>
          </a>
         
        </div>

        {/* Mobile menu (Hamburger) */}
        <div className="md:hidden flex items-center space-x-2">
          <button className="text-darkBlue text-4xl">☰</button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex flex-col flex-1 bg-background p-2">
        <h1 className="text-9xl font-bold text-foreground uppercase">Fostr</h1>
        
      </main>

      {/* Footer */}
      <footer className="bg-darkBlue text-white p-4 text-center">
        <p>&copy; 2025 Fostr. All rights reserved.</p>
      </footer>
    </div>
  );
}
