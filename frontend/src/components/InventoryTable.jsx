import { riskBg } from './ui.jsx'

export default function InventoryTable({ rows, warehouses, onSelect, selected }) {
  const products = [...new Map(rows.map(r => [r.product_id, r.name])).entries()]
  const cell = Object.fromEntries(rows.map(r => [`${r.product_id}|${r.warehouse_id}`, r]))

  return (
    <div className="card overflow-auto p-0 max-h-[560px]">
      <table className="text-xs w-full min-w-max border-separate border-spacing-0">
        <thead className="sticky top-0 z-10 bg-ink-800/95 backdrop-blur text-slate-400">
          <tr>
            <th className="text-left px-3 py-3 border-b border-ink-600">Product</th>
            {warehouses.map(w => (
              <th key={w.warehouse_id} className="px-3 py-3 border-b border-ink-600 font-medium">{w.name}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {products.map(([pid, name]) => (
            <tr key={pid} className={selected === pid ? 'bg-accent/10' : ''}>
              <td className={`px-3 py-2 whitespace-nowrap border-b border-ink-600/60 ${selected === pid ? 'text-white' : 'text-slate-300'}`}>
                <span className="font-mono text-[10px] text-slate-500 mr-1">{pid}</span> {name}
              </td>
              {warehouses.map(w => {
                const c = cell[`${pid}|${w.warehouse_id}`]
                return (
                  <td key={w.warehouse_id} className="px-1.5 py-1.5 border-b border-ink-600/60">
                    {c ? (
                      <button
                        onClick={() => onSelect(pid)}
                        title={`${c.days_of_cover}d cover · ${(c.stockout_probability * 100).toFixed(0)}% stockout`}
                        className={`w-full rounded-md py-1.5 text-white text-[11px] font-medium hover:ring-2 hover:ring-white/40 transition-all ${riskBg(c.stockout_probability)}`}
                        style={{ opacity: 0.45 + c.stockout_probability * 0.55 }}
                      >
                        {c.quantity_on_hand}
                      </button>
                    ) : (
                      <span className="text-slate-600 text-center block">–</span>
                    )}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}