import { riskBg } from './ui.jsx'

export default function RiskHeatmap({ suppliers }) {
  const tiers = [1, 2, 3]
  return (
    <div className="space-y-4">
      {tiers.map(t => (
        <div key={t}>
          <div className="flex items-center gap-2 mb-2">
            <span className="section-title">Tier {t}</span>
            <span className="text-[10px] text-slate-500">
              {suppliers.filter(s => s.tier === t).length} suppliers
            </span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {suppliers
              .filter(s => s.tier === t)
              .sort((a, b) => b.risk_score - a.risk_score)
              .map(s => (
                <div
                  key={s.supplier_id}
                  title={`${s.name} — ${(s.risk_score * 100).toFixed(0)}%`}
                  className={`w-8 h-8 rounded-lg ${riskBg(s.risk_score)} flex items-center justify-center text-[10px] font-medium text-white/95 ring-1 ring-white/5 hover:ring-white/40 hover:scale-110 transition-transform cursor-pointer`}
                  style={{ opacity: 0.35 + s.risk_score * 0.65 }}
                >
                  {Math.round(s.risk_score * 100)}
                </div>
              ))}
          </div>
        </div>
      ))}
      <div className="flex gap-4 text-[11px] text-slate-400 pt-1">
        <span className="flex items-center gap-1.5"><i className="w-2.5 h-2.5 bg-green-500 rounded-sm" /> low</span>
        <span className="flex items-center gap-1.5"><i className="w-2.5 h-2.5 bg-amber-500 rounded-sm" /> warning</span>
        <span className="flex items-center gap-1.5"><i className="w-2.5 h-2.5 bg-red-500 rounded-sm" /> critical</span>
      </div>
    </div>
  )
}