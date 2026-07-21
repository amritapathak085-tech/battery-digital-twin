import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "Battery Digital Twin Intelligence Platform",
  description: "AI-powered EV fleet battery health, prediction, simulation & business impact",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-background text-gray-200 min-h-screen">
        <div className="flex min-h-screen">
          <Sidebar />
          {/* Main content area - each screen renders here via app/page.tsx */}
          <main className="flex-1 overflow-y-auto p-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
