import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Truck, Boxes, AlertTriangle, GitBranch, FlaskConical, Lightbulb, ShieldCheck } from 'lucide-react'

const links = [
   { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/suppliers', label: 'Suppliers', icon: Truck },
  { to: '/inventory', label: 'Inventory', icon: Boxes },
  { to: '/disruptions', label: 'Disruptions', icon: AlertTriangle },
  { to: '/impact', label: 'Impact Analysis', icon: GitBranch },
  { to: '/simulator', label: 'Simulator', icon: FlaskConical },
  { to: '/recommendations', label: 'Recommendations', icon: Lightbulb },
]

export default function Sidebar({ open = false, onNavigate = () => {} }) {
  return (
    <aside className={`fixed inset-y-0 left-0 z-40 w-64 shrink-0 bg-ink-800/95 backdrop-blur border-r border-ink-600 h-screen p-4 flex flex-col transition-transform duration-200 md:sticky md:top-0 md:w-60 md:translate-x-0 md:bg-ink-800/80 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
      <div className="flex items-center gap-2.5 mb-8 px-2 py-3">
        <span className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-glow">
          <ShieldCheck className="text-white" size={18} />
        </span>
        <div className="leading-tight">
          <div className="text-white font-semibold tracking-tight">Sentinel</div>
          <div className="text-[10px] text-slate-500 uppercase tracking-widest">Control Tower</div>
        </div>
      </div>

      <nav className="space-y-1 overflow-y-auto flex-1">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            onClick={onNavigate}
            className={({ isActive }) =>
              `group relative flex items-center gap-2.5 px-3 py-2 rounded-xl text-sm transition-all duration-150 ${
                isActive
                  ? 'bg-accent/15 text-white border border-accent/30 shadow-glow'
                  : 'text-slate-400 hover:bg-ink-700/70 hover:text-slate-200 border border-transparent'
              }`
            }
          >
            <Icon size={16} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto pt-4 text-[10px] text-slate-600 px-2">
        v1.0 · AI Supply Chain
      </div>
    </aside>
  )
}