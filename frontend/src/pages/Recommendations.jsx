import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Sparkles, History } from 'lucide-react'
import ActionRecommender from '../components/ActionRecommender.jsx'
import { Query, PageTitle, EventSelect, ErrorBox } from '../components/ui.jsx'
import { getEvents, recommend, getAudit } from '../api/client.js'

export default function Recommendations() {
  const [id, setId] = useState('')
  const ev = useQuery({ queryKey: ['events'], queryFn: getEvents })
  const rec = useMutation({ mutationFn: recommend })
  const audit = useQuery({ queryKey: ['audit'], queryFn: getAudit, refetchInterval: 5000 })

  return (
    <>
      <PageTitle>Recommendations</PageTitle>

      <Query q={ev}>{e => (
        <div className="flex flex-wrap gap-3 mb-6">
          <EventSelect events={e} value={id} onChange={setId} />
          <button className="btn shrink-0" disabled={!id || rec.isPending} onClick={() => rec.mutate(id)}>
            <Sparkles size={14} />
            {rec.isPending ? 'Optimizing…' : 'Get Recommendations'}
          </button>
        </div>
      )}</Query>

      {rec.isError && <ErrorBox error={rec.error} />}
      {rec.data && <ActionRecommender key={rec.data.event_id} eventId={rec.data.event_id} plans={rec.data.plans} />}

      <h2 className="section-title mt-10 mb-3 flex items-center gap-2"><History size={12} /> Audit trail</h2>
      <Query q={audit}>{a => a.length ? (
        <div className="card text-xs space-y-2 max-h-64 overflow-y-auto">
          {a.map((r, i) => (
            <div key={i} className="flex items-center gap-3 py-1.5 border-b border-ink-600/40 last:border-none">
              <span className="text-slate-500 font-mono text-[10px]">{r.timestamp}</span>
              <span className="w-1 h-1 rounded-full bg-slate-600" />
              <span className="text-slate-300">{r.user_action}</span>
              <span className="text-slate-500">·</span>
              <span className="text-slate-400">{r.entity} {r.entity_id}</span>
            </div>
          ))}
        </div>
      ) : <div className="text-xs text-slate-500">No actions logged yet.</div>}</Query>
    </>
  )
}