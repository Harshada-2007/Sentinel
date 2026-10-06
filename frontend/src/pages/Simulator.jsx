import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Play } from 'lucide-react'
import SimulatorPanel from '../components/SimulatorPanel.jsx'
import { Query, PageTitle, EventSelect, ErrorBox } from '../components/ui.jsx'
import { getEvents, runSimulation } from '../api/client.js'

const LEVERS = [
  { id: 1, name: 'Switch to backup supplier', key: 'qty_fraction', min: 0, max: 1, step: 0.05, def: 0.6 },
  { id: 2, name: 'Transfer inventory', key: 'qty_fraction', min: 0, max: 1, step: 0.05, def: 0.4 },
  { id: 3, name: 'Change reorder timing', key: 'qty_fraction', min: 0, max: 1, step: 0.05, def: 0.3 },
  { id: 4, name: 'Prioritize critical orders', key: 'deprioritize_fraction', min: 0, max: 1, step: 0.05, def: 0.5 },
  { id: 5, name: 'Pricing / promotion', key: 'demand_reduction_fraction', min: 0, max: 0.6, step: 0.05, def: 0.2 },
]

export default function Simulator() {
  const [id, setId] = useState('')
  const [on, setOn] = useState({})
  const [val, setVal] = useState(Object.fromEntries(LEVERS.map(l => [l.id, l.def])))
  const ev = useQuery({ queryKey: ['events'], queryFn: getEvents })
  const sim = useMutation({ mutationFn: runSimulation })
  const run = () => sim.mutate({
    event_id: id,
    actions: LEVERS.filter(l => on[l.id]).map(l => ({ lever: l.id, params: { [l.key]: val[l.id] } })),
  })

  return (
    <>
      <PageTitle>Simulator</PageTitle>
      <Query q={ev}>{e => <div className="mb-4"><EventSelect events={e} value={id} onChange={setId} /></div>}</Query>

      <div className="card space-y-4 mb-6">
        <div className="section-title">Configure interventions</div>
        {LEVERS.map(l => (
          <div key={l.id} className="flex items-center gap-4 text-sm py-1">
            <label className="flex items-center gap-2.5 w-64 cursor-pointer">
              <input type="checkbox" className="accent-accent" checked={!!on[l.id]} onChange={e => setOn({ ...on, [l.id]: e.target.checked })} />
              <span className="pill bg-ink-700 text-slate-300 border-ink-600">L{l.id}</span>
              <span className="text-slate-300">{l.name}</span>
            </label>
            <input
              type="range" min={l.min} max={l.max} step={l.step} value={val[l.id]} disabled={!on[l.id]}
              className="flex-1 accent-accent disabled:opacity-40"
              onChange={e => setVal({ ...val, [l.id]: +e.target.value })}
            />
            <span className="w-12 text-right text-slate-400 tabular-nums">{val[l.id]}</span>
          </div>
        ))}
        <button className="btn mt-2" disabled={!id || sim.isPending} onClick={run}>
          <Play size={13} /> {sim.isPending ? 'Running…' : 'Run Simulation'}
        </button>
      </div>

      {sim.isError && <ErrorBox error={sim.error} />}
      {sim.data && <SimulatorPanel result={sim.data} />}
    </>
  )
}