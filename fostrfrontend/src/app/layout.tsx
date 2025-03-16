import type { Metadata } from "next";
import { ThemeProvider } from "next-themes";

import "./globals.css"; // Make sure globals.css includes the font definitions
import { AuthProvider } from "./Context/AuthContext";

export const metadata: Metadata = {
  title: "FOSTR",
  description: "Manage your shelter or rescue or find a way to help out by fostering, volunteering, or transporting",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
         {children}
        </AuthProvider>
         
       
      </body>
    </html>
  );
}
