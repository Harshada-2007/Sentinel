import { AlertTriangle } from 'lucide-react'

export default function AlertCard({ event }) {
  const tone =
    event.severity >= 0.6  ? { border: 'border-red-500/40',    text: 'text-red-400',    chip: 'bg-red-500/15 text-red-300 border-red-500/30' } :
    event.severity >= 0.35 ? { border: 'border-amber-500/40',  text: 'text-amber-400',  chip: 'bg-amber-500/15 text-amber-300 border-amber-500/30' } :
                             { border: 'border-green-500/40',  text: 'text-green-400',  chip: 'bg-green-500/15 text-green-300 border-green-500/30' }

  return (
    <div className={`card card-hover border ${tone.border} flex gap-3`}>
      <span className={`w-9 h-9 rounded-xl bg-ink-700 border ${tone.border} flex items-center justify-center shrink-0`}>
        <AlertTriangle size={16} className={tone.text} />
      </span>
      <div className="min-w-0 flex-1">
        <div className="flex items-center justify-between gap-3">
          <div className="text-sm text-white capitalize truncate">
            {event.event_type.replace(/_/g, ' ')} <span className="text-slate-500">·</span> {event.affected_region}
          </div>
          <span className={`pill ${tone.chip} shrink-0`}>sev {event.severity}</span>
        </div>
        <div className="text-xs text-slate-400 truncate mt-0.5">{event.description}</div>
        <div className="text-[11px] text-slate-500 mt-1.5 flex items-center gap-2">
          <span>{event.event_id}</span>
          <span className="w-1 h-1 rounded-full bg-slate-600" />
          <span>{event.detected_date}</span>
          <span className="w-1 h-1 rounded-full bg-slate-600" />
          <span>~{event.predicted_delay_days}d delay</span>
        </div>
      </div>
    </div>
  )
}