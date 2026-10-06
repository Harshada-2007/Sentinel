import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, X } from 'lucide-react'
import AlertCard from '../components/AlertCard.jsx'
import { Query, PageTitle } from '../components/ui.jsx'
import { getEvents, createEvent, getSuppliers } from '../api/client.js'

const TYPES = ['port_strike', 'factory_fire', 'weather', 'customs_delay', 'labor_dispute', 'raw_material_shortage', 'geopolitical', 'logistics_failure']

function Modal({ onClose }) {
  const qc = useQueryClient()
  const sups = useQuery({ queryKey: ['suppliers'], queryFn: getSuppliers })
  const [f, setF] = useState({ event_type: TYPES[0], affected_supplier_id: '', severity: 0.6, predicted_delay_days: 4, description: '' })
  const m = useMutation({ mutationFn: createEvent, onSuccess: () => { qc.invalidateQueries(); onClose() } })
  const set = (k, v) => setF({ ...f, [k]: v })
  const sup = sups.data?.find(s => s.supplier_id === f.affected_supplier_id)

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-30 p-4" onClick={onClose}>
      <div className="card w-full max-w-md space-y-4 animate-fade-in" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between">
          <h2 className="text-white font-semibold">Create disruption event</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white"><X size={16} /></button>
        </div>
        <select className="input" value={f.event_type} onChange={e => set('event_type', e.target.value)}>
          {TYPES.map(t => <option key={t}>{t}</option>)}
        </select>
        <select className="input" value={f.affected_supplier_id} onChange={e => set('affected_supplier_id', e.target.value)}>
          <option value="">Select supplier…</option>
          {sups.data?.map(s => <option key={s.supplier_id} value={s.supplier_id}>{s.supplier_id} · {s.name} ({s.location})</option>)}
        </select>
        <label className="text-xs text-slate-400 block">
          Severity: <span className="text-white font-medium">{f.severity}</span>
          <input type="range" min="0.05" max="0.99" step="0.01" className="w-full mt-1 accent-accent" value={f.severity} onChange={e => set('severity', +e.target.value)} />
        </label>
        <label className="text-xs text-slate-400 block">
          Predicted delay (days)
          <input type="number" min="1" className="input mt-1" value={f.predicted_delay_days} onChange={e => set('predicted_delay_days', +e.target.value)} />
        </label>
        <textarea className="input" placeholder="Description" rows={3} value={f.description} onChange={e => set('description', e.target.value)} />
        {m.isError && <div className="text-red-400 text-xs">{m.error.message}</div>}
        <div className="flex justify-end gap-2 pt-2">
          <button className="btn-ghost" onClick={onClose}>Cancel</button>
          <button className="btn" disabled={!sup || !f.description || m.isPending} onClick={() => m.mutate({ ...f, affected_region: sup.location })}>
            Create
          </button>
        </div>
      </div>
    </div>
  )
}

export default function Disruptions() {
  const [open, setOpen] = useState(false)
  const q = useQuery({ queryKey: ['events'], queryFn: getEvents, refetchInterval: 30000 })
  return (
    <>
      <PageTitle right={<button className="btn" onClick={() => setOpen(true)}><Plus size={14} /> Create Event</button>}>
        Disruptions
      </PageTitle>
      <Query q={q}>{e => (
        <div className="grid lg:grid-cols-2 gap-3">
          {e.map(ev => <AlertCard key={ev.event_id} event={ev} />)}
        </div>
      )}</Query>
      {open && <Modal onClose={() => setOpen(false)} />}
    </>
  )
}