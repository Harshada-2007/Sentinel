import { inr } from './ui.jsx'

const Node = ({ label, sub, tone = 'bg-ink-700/70 border-ink-600' }) => (
  <div className={`${tone} border rounded-xl px-3.5 py-2.5 text-xs min-w-[110px]`}>
    <div className="text-white font-medium">{label}</div>
    {sub && <div className="text-slate-400 truncate mt-0.5">{sub}</div>}
  </div>
)

const Arrow = () => <span className="text-slate-600 self-center select-none">→</span>

export default function ImpactPanel({ impact }) {
  const c = impact.cascade
  return (
    <div className="space-y-4">
      <div className="card border-red-500/40 bg-gradient-to-br from-red-500/[0.06] to-transparent">
        <div className="text-2xl font-semibold text-red-400 tracking-tight">
          {impact.affected_orders_count.toLocaleString()} orders affected
        </div>
        <div className="text-sm text-red-300/80 mt-1">{inr(impact.revenue_at_risk)} revenue at risk</div>
        <div className="text-[11px] text-slate-400 mt-2">
          {c.event.event_type.replace(/_/g, ' ')} · severity {c.event.severity} · {c.event.predicted_delay_days}-day predicted delay
        </div>
      </div>

      <div className="card">
        <div className="section-title mb-3">Cascade · Event → Supplier → Products → Warehouses → Orders → ₹</div>
        <div className="flex flex-wrap items-stretch gap-2">
          <Node label={c.event.event_id} sub={c.event.event_type} tone="bg-red-500/20 border-red-500/30" /><Arrow />
          <Node label={c.supplier?.name || '—'} sub={c.supplier?.location} tone="bg-amber-500/20 border-amber-500/30" /><Arrow />
          <Node label={`${c.products.length} products`} sub={c.products.slice(0, 4).join(', ')} /><Arrow />
          <Node label={`${c.warehouses.length} warehouses`} sub={c.warehouses.join(', ')} /><Arrow />
          <Node label={`${c.orders_count} orders`} /><Arrow />
          <Node label={inr(impact.revenue_at_risk)} tone="bg-red-500/20 border-red-500/30" />
        </div>
      </div>

      <div className="card overflow-x-auto p-0">
        <table className="w-full text-sm">
          <thead className="bg-ink-700/60 text-slate-400 text-[11px] uppercase tracking-wider">
            <tr>
              <th className="text-left px-4 py-3">Product</th>
              <th className="px-4 py-3 text-right">Orders</th>
              <th className="px-4 py-3 text-right">Value at risk</th>
            </tr>
          </thead>
          <tbody>
            {impact.affected_products.map(p => (
              <tr key={p.product_id} className="border-t border-ink-600 hover:bg-ink-700/40">
                <td className="px-4 py-3"><span className="text-slate-400 font-mono text-xs">{p.product_id}</span> · {p.name}</td>
                <td className="px-4 py-3 text-right tabular-nums">{p.orders_affected}</td>
                <td className="px-4 py-3 text-right text-red-400 font-medium tabular-nums">{inr(p.value_at_risk)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}