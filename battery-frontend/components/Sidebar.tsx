"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Sidebar nav - shared shell used by every screen.
 * Uses real Next.js routes (not just tab-switching state) so that
 * "View Details" buttons on the Alerts screen can deep-link straight
 * to /predictions?vehicle=EV001 and land on the right vehicle.
 */
const NAV_ITEMS = [
  { label: "Fleet Overview", href: "/" },
  { label: "Alerts", href: "/alerts" },
  { label: "Predictions", href: "/predictions" }, // Member B builds the screen
  { label: "Simulation", href: "/simulation" },   // Member C builds the screen
  { label: "Reports", href: "/reports" },         // Member C builds the screen
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 shrink-0 bg-card border-r border-gray-800 flex flex-col">
      <div className="px-6 py-6 border-b border-gray-800">
        <h1 className="text-sm font-semibold text-gray-100 leading-tight">
          Battery Digital Twin
        </h1>
        <p className="text-xs text-gray-500 mt-1">Intelligence Platform</p>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          // Treat exact match for "/" and prefix match for everything else
          const isActive =
            item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block px-3 py-2 rounded-md text-sm transition-colors ${
                isActive
                  ? "bg-accent/15 text-accent font-medium"
                  : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="px-6 py-4 border-t border-gray-800 text-xs text-gray-600">
        ET AI Hackathon 2026
      </div>
    </aside>
  );
}
