import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "sonner";
import Navigation from "@/components/layout/Navigation";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "CoreFlow | Foco Flutuante",
  description: "Plataforma de produtividade baseada em ciclos de energia.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="dark">
      <body className={`${inter.variable} font-sans antialiased min-h-screen text-zinc-100 bg-[#0a0a0a] selection:bg-indigo-500/30`}>
        <div className="relative flex min-h-screen w-full">
          <Navigation />
          <main className="flex-1 sm:pl-20 pb-20 sm:pb-0 min-h-screen overflow-x-hidden">
            {children}
          </main>
        </div>
        <Toaster theme="dark" position="bottom-center" />
      </body>
    </html>
  );
}
