import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: "ABRISK | AMR Decision Intelligence",
  description: "Structure-informed antibiotic risk stratification and mechanism intelligence for clinicians and researchers.",
  keywords: ["AMR", "antimicrobial resistance", "antibiotic", "clinical decision support", "CARD"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`} suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen flex flex-col`} suppressHydrationWarning>
        <Navigation />

        <main className="flex-1">
          {children}
        </main>

        <Footer />
      </body>
    </html>
  );
}
