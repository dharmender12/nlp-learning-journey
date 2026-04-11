import { useEffect, useState } from 'react'
import api from '../services/api'
import ContractCard from '../components/ContractCard'
import ApplyModal from '../components/ApplyModal'
import CVUploader from '../components/CVUploader'

export default function TrainerDashboard() {
  const [contracts, setContracts] = useState([])
  const [applications, setApplications] = useState([])
  const [applyFor, setApplyFor] = useState(null)
  const [reuploadId, setReuploadId] = useState(null)
  const [skills, setSkills] = useState('')
  const [years, setYears] = useState(0)

  const loadContracts = async () => {
    const { data } = await api.get('/contracts')
    setContracts(data)
  }

  const loadMyApplications = async () => {
    const { data } = await api.get('/applications/me')
    setApplications(data)
  }

  useEffect(() => {
    loadContracts()
    loadMyApplications()
  }, [])

  const reupload = async (file) => {
    if (!reuploadId || !file) return
    const form = new FormData()
    form.append('skills', skills)
    form.append('years_experience', String(years))
    form.append('cv', file)
    await api.put(`/applications/${reuploadId}/cv`, form)
    setReuploadId(null)
    setSkills('')
    setYears(0)
    loadMyApplications()
  }

  return (
    <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Trainer Dashboard</h1>
        <p className="text-slate-600">Browse contracts and apply with AI-scored CV.</p>
      </div>

      <section className="grid md:grid-cols-2 gap-4">
        {contracts.map((contract) => (
          <ContractCard
            key={contract.id}
            contract={contract}
            action={<button className="bg-brand text-white px-3 py-2 rounded" onClick={() => setApplyFor(contract.id)}>Apply</button>}
          />
        ))}
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">My Applications</h2>
        <div className="grid gap-3">
          {applications.map((app) => (
            <div key={app.id} className="bg-white border rounded-lg p-4 flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="font-medium">Application #{app.id} | Contract #{app.contract_id}</p>
                <p className="text-sm text-slate-600">Score: {app.relevance_score} | {app.skills}</p>
              </div>
              <button className="px-3 py-2 rounded bg-slate-900 text-white" onClick={() => setReuploadId(app.id)}>
                Reupload CV
              </button>
            </div>
          ))}
          {applications.length === 0 && <p className="text-slate-500">No applications yet.</p>}
        </div>
      </section>

      {reuploadId && (
        <section className="bg-white border rounded-xl p-4 space-y-3">
          <h3 className="font-semibold">Reupload CV for Application #{reuploadId}</h3>
          <input className="w-full border rounded p-2" placeholder="Updated skills" value={skills} onChange={(e) => setSkills(e.target.value)} />
          <input className="w-full border rounded p-2" type="number" min="0" placeholder="Years of experience" value={years} onChange={(e) => setYears(e.target.value)} />
          <CVUploader onFile={reupload} />
        </section>
      )}

      {applyFor && <ApplyModal contractId={applyFor} onClose={() => { setApplyFor(null); loadMyApplications() }} />}
    </main>
  )
}
