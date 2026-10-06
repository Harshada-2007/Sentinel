export default function KpiCard({ label, value, tone = 'ok', icon: Icon }) {
  const c =
    tone === 'critical' ? 'text-red-400' :
    tone === 'warning'  ? 'text-amber-400' :
                          'text-green-400'
  const ring =
    tone === 'critical' ? 'from-red-500/20 to-red-500/0 border-red-500/30' :
    tone === 'warning'  ? 'from-amber-500/20 to-amber-500/0 border-amber-500/30' :
                          'from-green-500/20 to-green-500/0 border-green-500/30'

  return (
    <div className="card card-hover">
      <div className="flex items-start justify-between">
        <div className="text-slate-400 text-[11px] uppercase tracking-[0.12em]">{label}</div>
        {Icon && (
          <span className={`w-9 h-9 rounded-xl bg-gradient-to-br ${ring} border flex items-center justify-center ${c}`}>
            <Icon size={16} />
          </span>
        )}
      </div>
      <div className={`text-3xl font-semibold mt-3 tracking-tight ${c}`}>{value}</div>
      <div className="mt-3 h-1 rounded-full bg-ink-700 overflow-hidden">
        <div className={`h-full ${c.replace('text-', 'bg-')} opacity-70`} style={{ width: '62%' }} />
      </div>
    </div>
  )
}