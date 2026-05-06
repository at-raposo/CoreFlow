"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Swords, FileText } from "lucide-react";
import clsx from "clsx";

export default function Navigation() {
  const pathname = usePathname();

  const navItems = [
    { name: "QG", path: "/qg", icon: Home },
    { name: "Editais", path: "/editais", icon: FileText },
    { name: "Trincheira", path: "/trincheira", icon: Swords },
  ];

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden sm:flex flex-col items-center py-8 w-20 fixed inset-y-0 left-0 bg-[#121212] border-r border-white/5 z-50">
        <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-black text-xl mb-12 shadow-[0_0_15px_rgba(99,102,241,0.2)]">
          CF
        </div>
        
        <nav className="flex flex-col gap-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.path || (pathname === '/' && item.path === '/qg');
            
            return (
              <Link 
                key={item.path} 
                href={item.path}
                className={clsx(
                  "relative group p-3 rounded-2xl flex items-center justify-center transition-all duration-300",
                  isActive ? "bg-[#1E1E1E] text-white shadow-inner border border-white/5" : "text-zinc-500 hover:text-zinc-300 hover:bg-white/5"
                )}
                title={item.name}
              >
                {isActive && (
                  <span className="absolute -left-1 w-1 h-8 bg-indigo-500 rounded-r-full" />
                )}
                <Icon className="w-6 h-6" />
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Mobile Bottom Bar */}
      <nav className="sm:hidden fixed bottom-0 inset-x-0 bg-[#121212]/90 backdrop-blur-xl border-t border-white/5 z-50 pb-safe">
        <div className="flex items-center justify-around p-3">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.path || (pathname === '/' && item.path === '/qg');
            
            return (
              <Link 
                key={item.path} 
                href={item.path}
                className={clsx(
                  "flex flex-col items-center gap-1 transition-all duration-300",
                  isActive ? "text-white" : "text-zinc-500 hover:text-zinc-400"
                )}
              >
                <div className={clsx(
                  "p-2 rounded-xl transition-all duration-300",
                  isActive ? "bg-[#1E1E1E] border border-white/5 shadow-inner" : "bg-transparent"
                )}>
                  <Icon className="w-6 h-6" />
                </div>
                <span className="text-[10px] font-medium tracking-wide">{item.name}</span>
              </Link>
            )
          })}
        </div>
      </nav>
    </>
  );
}
