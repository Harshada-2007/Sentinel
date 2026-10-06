import { useQuery } from '@tanstack/react-query'
import { Truck, IndianRupee, PackageX, Activity } from 'lucide-react'
import KpiCard from '../components/KpiCard.jsx'
import AlertCard from '../components/AlertCard.jsx'
import RiskHeatmap from '../components/RiskHeatmap.jsx'
import { Query, PageTitle, inr } from '../components/ui.jsx'
import { getKpis, getEvents, getSuppliers, recommend } from '../api/client.js'

function TopActions({ events }) {
  const top = [...events].sort((a, b) => b.severity - a.severity)[0]
  const q = useQuery({ queryKey: ['recommend', top?.event_id], queryFn: () => recommend(top.event_id), enabled: !!top })
  if (!top) return <div className="text-slate-400 text-sm">No events.</div>
  return (
    <div>
      <div className="text-xs text-slate-400 mb-3">
        For highest-severity event <span className="text-white font-mono">{top.event_id}</span>
      </div>
      <Query q={q}>{d => d.plans.length ? (
        <ol className="space-y-2.5">
          {d.plans.slice(0, 3).map(p => (
            <li key={p.rank} className="bg-ink-700/60 border border-ink-600 rounded-xl p-3 text-sm flex items-start gap-3 hover:border-accent/40 transition-colors">
              <span className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 text-white text-xs font-semibold flex items-center justify-center shrink-0">#{p.rank}</span>
              <div className="min-w-0">
                <div className="text-white font-medium truncate">{p.label}</div>
                <div className="text-xs text-slate-400 mt-0.5">
                  {inr(p.estimated_cost)} · stockout <span className="text-green-400">↓{(p.expected_stockout_reduction * 100).toFixed(0)}%</span>
                </div>
              </div>
            </li>
          ))}
        </ol>
      ) : <div className="text-slate-400 text-sm">No feasible plans.</div>}</Query>
    </div>
  )
}

export default function Dashboard() {
  const kpis = useQuery({ queryKey: ['kpis'], queryFn: getKpis, refetchInterval: 30000 })
  const events = useQuery({ queryKey: ['events'], queryFn: getEvents, refetchInterval: 30000 })
  const sups = useQuery({ queryKey: ['suppliers'], queryFn: getSuppliers })

  return (
    <>
      <PageTitle>Dashboard</PageTitle>

      <Query q={kpis}>{k => (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <KpiCard label="Suppliers at risk"    value={k.suppliers_at_risk}   tone="critical" icon={Truck} />
          <KpiCard label="Rupee exposure"       value={inr(k.dollar_exposure)} tone="warning"  icon={IndianRupee} />
          <KpiCard label="Stockouts predicted"  value={k.stockouts_predicted}  tone="critical" icon={PackageX} />
          <KpiCard label="Active events"        value={k.active_events}        tone="warning"  icon={Activity} />
        </div>
      )}</Query>

      <div className="grid lg:grid-cols-2 gap-6">
        <section>
          <div className="flex items-center justify-between mb-3">
            <h2 className="section-title">Live disruption alerts</h2>
            <span className="text-[10px] text-slate-500">refreshes every 30s</span>
          </div>
          <Query q={events}>{e => (
            <div className="space-y-3 max-h-[480px] overflow-y-auto pr-1">
              {e.slice(0, 15).map(ev => <AlertCard key={ev.event_id} event={ev} />)}
            </div>
          )}</Query>
        </section>

        <div className="space-y-6">
          <section className="card">
            <h2 className="section-title mb-4">Risk heatmap · supplier × tier</h2>
            <Query q={sups}>{s => <RiskHeatmap suppliers={s} />}</Query>
          </section>
          <section className="card">
            <h2 className="section-title mb-4">Top 3 recommended actions</h2>
            <Query q={events}>{e => <TopActions events={e} />}</Query>
          </section>
        </div>
      </div>
    </>
  )
}