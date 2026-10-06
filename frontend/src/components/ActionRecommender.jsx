import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { CheckCircle2, HelpCircle, TrendingDown, ShieldCheck, IndianRupee } from 'lucide-react'
import ExplanationPanel from './ExplanationPanel.jsx'
import { acceptPlan } from '../api/client.js'
import { inr } from './ui.jsx'

const LEVERS = { 1: 'Backup supplier', 2: 'Transfer inventory', 3: 'Reorder timing', 4: 'Prioritize orders', 5: 'Pricing/promo' }

export default function ActionRecommender({ eventId, plans }) {
  const [open, setOpen] = useState(null)
  const accept = useMutation({ mutationFn: rank => acceptPlan(eventId, rank) })

  if (!plans.length) return <div className="text-slate-400 text-sm">No feasible plans for this event.</div>

  return (
    <div className="space-y-4">
      {plans.map(p => (
        <div key={p.rank} className="card card-hover">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <div className="flex items-center gap-2.5">
                <span className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-sm font-semibold flex items-center justify-center shadow-glow">
                  #{p.rank}
                </span>
                <span className="text-white font-medium">{p.label}</span>
              </div>
              <div className="flex flex-wrap gap-1.5 mt-3">
                {p.levers_used.map(l => (
                  <span key={l} className="pill bg-ink-700 text-slate-300 border-ink-600">
                    L{l} · {LEVERS[l]}
                  </span>
                ))}
              </div>
              <p className="text-xs text-slate-400 mt-3 leading-relaxed">{p.description}</p>
            </div>

            <div className="text-right text-sm shrink-0 space-y-1.5 w-40">
              <div className="flex items-center justify-end gap-1.5 text-slate-400">
                <IndianRupee size={12} /><b className="text-white font-medium">{inr(p.estimated_cost)}</b>
              </div>
              <div className="flex items-center justify-end gap-1.5 text-slate-400">
                <TrendingDown size={12} className="text-green-400" />
                <b className="text-green-400 font-medium">{(p.expected_stockout_reduction * 100).toFixed(0)}%</b>
                <span className="text-[10px]">less stockouts</span>
              </div>
              <div className="flex items-center justify-end gap-1.5 text-slate-400">
                <ShieldCheck size={12} className="text-green-400" />
                <b className="text-green-400 font-medium">+{(p.sla_impact * 100).toFixed(1)}</b>
                <span className="text-[10px]">SLA pts</span>
              </div>
            </div>
          </div>

          <div className="flex gap-2 mt-4 pt-4 border-t border-ink-600/60">
            <button className="btn-ghost" onClick={() => setOpen(open === p.rank ? null : p.rank)}>
              <HelpCircle size={14} /> Why this action?
            </button>
            <button className="btn" disabled={accept.isPending || accept.data?.plan?.rank === p.rank} onClick={() => accept.mutate(p.rank)}>
              <CheckCircle2 size={14} />
              {accept.variables === p.rank && accept.isSuccess ? 'Accepted · logged' : 'Accept'}
            </button>
          </div>

          {accept.isError && accept.variables === p.rank && (
            <div className="text-red-400 text-xs mt-2">Failed to log: {accept.error.message}</div>
          )}
          {open === p.rank && <ExplanationPanel eventId={eventId} rank={p.rank} />}
        </div>
      ))}
    </div>
  )
}