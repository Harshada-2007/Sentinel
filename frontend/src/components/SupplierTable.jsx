import { useState } from 'react'
import { ArrowUpDown } from 'lucide-react'
import { riskBg, tierColor } from './ui.jsx'

const cols = [
  ['supplier_id', 'ID'], ['name', 'Name'], ['tier', 'Tier'], ['location', 'Location'],
  ['lead_time_days', 'Lead (d)'], ['reliability_score', 'Reliability'], ['risk_score', 'Delay risk'],
]

export default function SupplierTable({ suppliers, onSelect }) {
  const [sort, setSort] = useState({ key: 'risk_score', dir: -1 })
  const rows = [...suppliers].sort((a, b) => (a[sort.key] > b[sort.key] ? 1 : -1) * sort.dir)

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px] text-sm">
          <thead className="bg-ink-700/60 text-slate-400 text-[11px] uppercase tracking-wider">
            <tr>
              {cols.map(([k, l]) => (
                <th key={k} className="text-left px-4 py-3 cursor-pointer select-none" onClick={() => setSort({ key: k, dir: sort.key === k ? -sort.dir : -1 })}>
                  <span className="inline-flex items-center gap-1.5 hover:text-slate-200">
                    {l}<ArrowUpDown size={11} className="opacity-60" />
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(s => (
              <tr key={s.supplier_id} onClick={() => onSelect(s)}
                  className="border-t border-ink-600 hover:bg-ink-700/50 cursor-pointer transition-colors">
                <td className="px-4 py-3 font-mono text-xs text-slate-400">{s.supplier_id}</td>
                <td className="px-4 py-3 text-white">{s.name}</td>
                <td className="px-4 py-3"><span className="pill bg-ink-700 text-slate-300 border-ink-600">T{s.tier}</span></td>
                <td className="px-4 py-3 text-slate-300">{s.location}</td>
                <td className="px-4 py-3 text-slate-300">{s.lead_time_days}</td>
                <td className="px-4 py-3 text-slate-300">{s.reliability_score}</td>
                <td className="px-4 py-3 w-56">
                  <div className="flex items-center gap-3">
                    <div className="h-1.5 flex-1 bg-ink-600 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${riskBg(s.risk_score)}`} style={{ width: `${s.risk_score * 100}%` }} />
                    </div>
                    <span className={`text-xs font-medium tabular-nums ${tierColor(s.risk_tier)}`}>
                      {(s.risk_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}