import { useState } from 'react'
import api from '../services/api'

const tiers = [
  { key: 'free', price: '₹0', text: 'Only applicant count' },
  { key: 'standard', price: '₹199', text: 'See all applicants' },
  { key: 'premium', price: '₹249', text: 'AI shortlist (2x required)' },
]

export default function TierUpgradeModal({ onClose, onUpdated }) {
  const [loading, setLoading] = useState(false)

  const choose = async (tier) => {
    setLoading(true)
    try {
      const { data } = await api.post('/users/subscription', { tier })
      onUpdated(data)
      onClose()
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center p-4">
      <div className="bg-white rounded-xl p-6 w-full max-w-2xl">
        <h3 className="text-lg font-semibold mb-4">Upgrade Subscription</h3>
        <div className="grid md:grid-cols-3 gap-3">
          {tiers.map((tier) => (
            <button key={tier.key} onClick={() => choose(tier.key)} className="text-left border rounded-lg p-4 hover:border-brand">
              <p className="font-semibold capitalize">{tier.key}</p>
              <p className="text-2xl font-bold my-2">{tier.price}</p>
              <p className="text-sm text-slate-600">{tier.text}</p>
            </button>
          ))}
        </div>
        <div className="mt-4 text-right">
          <button onClick={onClose} className="px-3 py-2 border rounded" disabled={loading}>Close</button>
        </div>
      </div>
    </div>
  )
}
