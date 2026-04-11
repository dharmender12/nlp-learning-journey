import { useState } from 'react'
import api from '../services/api'
import CVUploader from './CVUploader'

export default function ApplyModal({ contractId, onClose }) {
  const [coverLetter, setCoverLetter] = useState('')
  const [skills, setSkills] = useState('')
  const [years, setYears] = useState(0)
  const [cv, setCv] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    if (!cv) return

    const form = new FormData()
    form.append('cover_letter', coverLetter)
    form.append('skills', skills)
    form.append('years_experience', String(years))
    form.append('cv', cv)

    setLoading(true)
    try {
      await api.post(`/contracts/${contractId}/apply`, form)
      onClose()
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center p-4">
      <form onSubmit={submit} className="bg-white rounded-xl p-6 w-full max-w-lg space-y-3">
        <h3 className="text-lg font-semibold">Apply to Contract</h3>
        <textarea className="w-full border rounded p-2" rows="3" placeholder="Cover letter" value={coverLetter} onChange={(e) => setCoverLetter(e.target.value)} />
        <input className="w-full border rounded p-2" placeholder="Skills (comma separated)" value={skills} onChange={(e) => setSkills(e.target.value)} />
        <input className="w-full border rounded p-2" type="number" min="0" placeholder="Years of experience" value={years} onChange={(e) => setYears(e.target.value)} />
        <CVUploader onFile={setCv} />
        {cv && <p className="text-xs text-slate-500">Selected: {cv.name}</p>}
        <div className="flex justify-end gap-2">
          <button type="button" className="px-3 py-2 border rounded" onClick={onClose}>Cancel</button>
          <button className="px-3 py-2 bg-brand text-white rounded" disabled={loading || !cv}>{loading ? 'Submitting...' : 'Submit'}</button>
        </div>
      </form>
    </div>
  )
}
