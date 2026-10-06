import { inr } from './ui.jsx'

const Stat = ({ value, label, tone }) => (
  <div className="text-center">
    <div className={`text-2xl font-semibold tracking-tight ${tone || 'text-white'}`}>{value}</div>
    <div className="text-[10px] text-slate-500 uppercase tracking-wider mt-0.5">{label}</div>
  </div>
)

const Col = ({ title, o, tone, badge }) => (
  <div className={`card border ${tone}`}>
    <div className="flex items-center justify-between mb-4">
      <div className="text-sm text-white font-medium">{title}</div>
      {badge && <span className={`pill ${badge}`}>{badge.text}</span>}
    </div>
    <div className="grid grid-cols-3 gap-2">
      <Stat value={`${o.stockout_risk_pct}%`} label="Stockout risk" tone={o.stockout_risk_pct > 15 ? 'text-red-400' : 'text-green-400'} />
      <Stat value={`${o.sla_pct}%`}         label="SLA"           tone={o.sla_pct < 90 ? 'text-amber-400' : 'text-green-400'} />
      <Stat value={inr(o.total_cost)}       label="Cost" />
    </div>
    <ul className="mt-4 space-y-1.5 text-xs text-slate-400">
      {o.details.map((d, i) => (
        <li key={i} className="flex gap-2"><span className="text-slate-600">•</span><span>{d.description}</span></li>
      ))}
    </ul>
  </div>
)

export default function SimulatorPanel({ result }) {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <Col title="Do nothing"    o={result.do_nothing}   tone="border-red-500/40 bg-gradient-to-br from-red-500/[0.04] to-transparent"
           badge={{ text: 'baseline', className: 'bg-ink-700 text-slate-400 border-ink-600' }} />
      <Col title="With your actions" o={result.with_actions} tone="border-green-500/40 bg-gradient-to-br from-green-500/[0.04] to-transparent"
           badge={{ text: 'improved', className: 'bg-green-500/15 text-green-300 border-green-500/30' }} />
    </div>
  )
}