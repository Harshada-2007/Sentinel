import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import InventoryTable from '../components/InventoryTable.jsx'
import { Query, PageTitle } from '../components/ui.jsx'
import { getHeatmap, getWarehouses, getDemandForecast } from '../api/client.js'

function Forecast({ pid }) {
  const q = useQuery({ queryKey: ['forecast', pid], queryFn: () => getDemandForecast(pid) })
  return (
    <div className="card mt-6 animate-fade-in">
      <div className="flex items-center justify-between mb-4">
        <h2 className="section-title">14-day demand forecast</h2>
        <span className="pill bg-ink-700 text-slate-300 border-ink-600 font-mono">{pid}</span>
      </div>
      <Query q={q}>{d => (
        <div className="h-72">
          <ResponsiveContainer>
            <LineChart data={d.forecast}>
              <defs>
                <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="100%" stopColor="#8b5cf6" />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="#1c2331" vertical={false} />
              <XAxis dataKey="date" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: '#0f1420', border: '1px solid #222a3d', borderRadius: 12 }} />
              <Line type="monotone" dataKey="predicted_quantity" stroke="url(#lineGrad)" dot={false} strokeWidth={2.5} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}</Query>
    </div>
  )
}

export default function Inventory() {
  const [pid, setPid] = useState(null)
  const h = useQuery({ queryKey: ['heatmap'], queryFn: getHeatmap })
  const w = useQuery({ queryKey: ['warehouses'], queryFn: getWarehouses })
  return (
    <>
      <PageTitle>Inventory</PageTitle>
      <p className="text-xs text-slate-400 mb-4">
        Cells show quantity on hand; redder = higher predicted 7-day stockout probability. Click a cell for the demand forecast.
      </p>
      <Query q={h}>{rows => <Query q={w}>{wh => <InventoryTable rows={rows} warehouses={wh} onSelect={setPid} selected={pid} />}</Query>}</Query>
      {pid && <Forecast pid={pid} />}
    </>
  )
}