import { useQuery } from '@tanstack/react-query'
import { Outlet } from 'react-router-dom'
import { Bell, LogOut, Menu, Search } from 'lucide-react'
import { useState } from 'react'
import Sidebar from './Sidebar.jsx'
import { useAuth } from '../context/AuthContext.jsx'
import { getKpis } from '../api/client.js'

export default function Layout() {
  const { data } = useQuery({ queryKey: ['kpis'], queryFn: getKpis, refetchInterval: 30000 })
  const { user, signOut } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex min-h-screen">
      <Sidebar open={sidebarOpen} onNavigate={() => setSidebarOpen(false)} />
      {sidebarOpen && (
        <button
          type="button"
          aria-label="Close navigation menu"
          className="fixed inset-0 z-30 bg-black/60 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      <div className="flex-1 min-w-0 flex flex-col">
        <header className="min-h-16 sticky top-0 z-20 border-b border-ink-600 flex items-center justify-between gap-3 px-3 sm:px-5 lg:px-6 py-2 bg-ink-800/70 backdrop-blur-md">
          <div className="flex min-w-0 items-center gap-3">
            <button
              type="button"
              aria-label="Open navigation menu"
              aria-expanded={sidebarOpen}
              className="btn-ghost !px-2 !py-2 md:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu size={18} />
            </button>
            <div className="flex min-w-0 items-center gap-2 text-sm text-slate-300">
              <span className="font-medium text-white whitespace-nowrap">AI Supply Chain</span>
              <span className="hidden sm:inline text-slate-500 whitespace-nowrap">Control Tower</span>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2 sm:gap-3">
            <div className="hidden md:flex items-center gap-2 bg-ink-700/70 border border-ink-600 rounded-xl px-3 py-1.5 w-72">
              <Search size={14} className="text-slate-500" />
              <input placeholder="Search suppliers, orders…" className="bg-transparent outline-none text-sm w-full placeholder:text-slate-500" />
            </div>

            <span className="pill bg-red-500/15 text-red-400 border-red-500/30">
              <Bell size={12} /> Live {data ? `· ${data.active_events}` : ''}
            </span>

            <div className="flex items-center gap-2 sm:pl-3 sm:border-l border-ink-600">
              <div className="text-right leading-tight hidden sm:block">
                <div className="text-xs text-white">{user?.name}</div>
                <div className="text-[10px] text-slate-500 capitalize">{user?.role}</div>
              </div>
              <span className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xs font-semibold">
                {user?.name?.[0] ?? '?'}
              </span>
              <button onClick={signOut} className="btn-ghost !px-2 !py-1.5" title="Sign out">
                <LogOut size={14} />
              </button>
            </div>
          </div>
        </header>

        <main className="p-3 sm:p-4 lg:p-6 flex-1 min-w-0"><Outlet /></main>
      </div>
    </div>
  )
}