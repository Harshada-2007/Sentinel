export const Loading = ({ text = 'Loading…' }) => (
  <div className="flex items-center gap-2 text-slate-400 text-sm p-4">
    <span className="w-3 h-3 rounded-full border-2 border-slate-600 border-t-accent animate-spin" />
    {text}
  </div>
)

export const ErrorBox = ({ error }) => (
  <div className="text-red-300 text-sm p-4 bg-red-500/10 border border-red-500/30 rounded-xl animate-fade-in">
    <div className="font-medium text-red-200">Something went wrong</div>
    <div className="text-xs text-red-300/80 mt-1">
      {error?.message || 'Unknown error'}. Is the backend running on port 8000?
    </div>
  </div>
)

export const Query = ({ q, children }) =>
  q.isLoading ? <Loading /> : q.isError ? <ErrorBox error={q.error} /> : children(q.data)

export const tierColor = t =>
  t === 'critical' ? 'text-red-400' : t === 'warning' ? 'text-amber-400' : 'text-green-400'

export const riskBg = p =>
  p >= 0.66 ? 'bg-red-500' : p >= 0.35 ? 'bg-amber-500' : 'bg-green-500'

export const inr = n =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(Number(n || 0))

export const PageTitle = ({ children, right }) => (
  <div className="flex items-center justify-between mb-6">
    <h1 className="text-2xl font-semibold text-white tracking-tight">{children}</h1>
    {right}
  </div>
)

export const EventSelect = ({ events, value, onChange }) => (
  <select className="input max-w-md" value={value || ''} onChange={e => onChange(e.target.value)}>
    <option value="">Select an event…</option>
    {events.map(e => (
      <option key={e.event_id} value={e.event_id}>
        {e.event_id} · {e.event_type.replace(/_/g, ' ')} · {e.affected_region} · sev {e.severity}
      </option>
    ))}
  </select>
)