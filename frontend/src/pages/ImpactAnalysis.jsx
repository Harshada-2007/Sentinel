import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import ImpactPanel from '../components/ImpactPanel.jsx'
import { Query, PageTitle, EventSelect } from '../components/ui.jsx'
import { getEvents, getImpact } from '../api/client.js'

export default function ImpactAnalysis() {
  const [id, setId] = useState('')
  const ev = useQuery({ queryKey: ['events'], queryFn: getEvents })
  const imp = useQuery({ queryKey: ['impact', id], queryFn: () => getImpact(id), enabled: !!id })
  return (
    <>
      <PageTitle>Impact Analysis</PageTitle>
      <Query q={ev}>{e => <div className="mb-6"><EventSelect events={e} value={id} onChange={setId} /></div>}</Query>
      {id && <Query q={imp}>{d => <ImpactPanel impact={d} />}</Query>}
    </>
  )
}