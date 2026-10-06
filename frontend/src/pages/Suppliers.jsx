import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import SupplierTable from '../components/SupplierTable.jsx'
import { Query, PageTitle, tierColor } from '../components/ui.jsx'
import { getSuppliers, getSupplierRisk } from '../api/client.js'

function Drawer({ supplier, onClose }) {
  const q = useQuery({ queryKey: ['risk', supplier.supplier_id], queryFn: () => getSupplierRisk(supplier.supplier_id) })
  return (
    <div className="fixed right-0 top-0 h-full w-full max-w-md bg-ink-800 border-l border-ink-600 p-6 overflow-y-auto z-20">
      <button className="float-right" onClick={onClose}><X /></button>
      <h2 className="text-white font-semibold">{supplier.name}</h2>
      <div className="text-xs text-slate-400 mb-4">{supplier.supplier_id} · {supplier.location} · Tier {supplier.tier}</div>
      <Query q={q}>{r => (<>
        <div className={`text-4xl font-semibold ${tierColor(r.risk_tier)}`}>{(r.delay_probability * 100).toFixed(0)}%</div>
        <div className="text-xs text-slate-400 mb-3">probability of delay &gt; 2 days</div>
        <p className="text-sm mb-4">{r.explanation}</p>
        <div className="text-xs text-slate-400 mb-1">Feature importance</div>
        <div className="h-48"><ResponsiveContainer><BarChart data={r.top_factors} layout="vertical" margin={{ left: 40 }}>
          <XAxis type="number" stroke="#64748b" fontSize={11} /><YAxis type="category" dataKey="factor" stroke="#64748b" fontSize={11} width={120} />
          <Tooltip contentStyle={{ background: '#111827', border: '1px solid #263047' }} /><Bar dataKey="importance" fill="#3b82f6" /></BarChart></ResponsiveContainer></div>
      </>)}</Query>
    </div>
  )
}
export default function Suppliers() {
  const [sel, setSel] = useState(null)
  const q = useQuery({ queryKey: ['suppliers'], queryFn: getSuppliers })
  return (<><PageTitle>Suppliers</PageTitle><Query q={q}>{s => <SupplierTable suppliers={s} onSelect={setSel} />}</Query>{sel && <Drawer supplier={sel} onClose={() => setSel(null)} />}</>)
}
