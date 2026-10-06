import { useQuery } from '@tanstack/react-query'
import { explain } from '../api/client.js'
import { Query } from './ui.jsx'

export default function ExplanationPanel({ eventId, rank }) {
  const q = useQuery({ queryKey: ['explain', eventId, rank], queryFn: () => explain(eventId, rank) })
  return (
    <div className="mt-3 p-3.5 rounded-xl bg-ink-700/60 border border-ink-600 text-sm leading-relaxed text-slate-300 animate-fade-in">
      <Query q={q}>{d => d.explanation}</Query>
    </div>
  )
}