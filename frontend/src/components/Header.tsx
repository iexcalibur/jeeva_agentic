'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sparkles } from 'lucide-react';

export default function Header() {
  const pathname = usePathname();
  const isHome = pathname === '/';

  const isActive = (href: string) => {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  };

  return (
    <header className="w-full fixed top-0 left-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          
          <Link 
            href="/" 
            className={`flex items-center gap-3 font-bold text-xl tracking-tight transition-all duration-200 rounded-lg px-3 py-2 ${
              isHome
                ? 'text-white'
                : 'text-white hover:opacity-80'
            }`}
          >
            <div className={`w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 ring-1 ring-white/10 transition-all ${
              isHome ? 'ring-2 ring-indigo-500/50' : ''
            }`}>
              <Sparkles size={18} className="text-white" />
            </div>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
              Jeeva Agentic
            </span>
          </Link>

          {isHome && (
            <nav className="hidden md:flex items-center gap-2">
              <Link
                href="/chat"
                className={`group flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 border border-transparent ${
                  isActive('/chat')
                    ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20 shadow-[0_0_15px_-3px_rgba(99,102,241,0.2)]'
                    : 'text-slate-500 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                <Sparkles size={18} className={isActive('/chat') ? 'text-indigo-400' : 'text-slate-500 group-hover:text-slate-300'} />
                <span className="font-medium text-sm">Chat</span>
              </Link>
            </nav>
          )}

          {!isHome && <div className="hidden md:block w-[120px]"></div>}
        </div>
      </div>
    </header>
  );
}
