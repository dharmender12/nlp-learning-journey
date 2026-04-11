import { useState } from 'react'
import api from '../services/api'

export default function CreateContractModal({ onClose, onCreated }) {
  const [form, setForm] = useState({ company_name: '', title: '', description: '' })
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data } = await api.post('/contracts', form)
      onCreated(data)
      onClose()
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center p-4">
      <form onSubmit={submit} className="bg-white rounded-xl p-6 w-full max-w-lg space-y-3">
        <h3 className="text-lg font-semibold">Create Contract</h3>
        <input className="w-full border rounded p-2" placeholder="Company" required value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} />
        <input className="w-full border rounded p-2" placeholder="Title" required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
        <textarea className="w-full border rounded p-2" rows="4" placeholder="Description" required value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <div className="flex justify-end gap-2">
          <button type="button" className="px-3 py-2 border rounded" onClick={onClose}>Cancel</button>
          <button className="px-3 py-2 bg-brand text-white rounded" disabled={loading}>{loading ? 'Creating...' : 'Create'}</button>
        </div>
      </form>
    </div>
  )
}
