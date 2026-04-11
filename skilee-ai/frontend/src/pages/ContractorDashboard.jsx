import { useEffect, useState } from 'react'
import api from '../services/api'
import ContractCard from '../components/ContractCard'
import CreateContractModal from '../components/CreateContractModal'
import TierUpgradeModal from '../components/TierUpgradeModal'
import ApplicationTable from '../components/ApplicationTable'

export default function ContractorDashboard() {
  const [contracts, setContracts] = useState([])
  const [subscription, setSubscription] = useState({ tier: 'free' })
  const [showCreate, setShowCreate] = useState(false)
  const [showUpgrade, setShowUpgrade] = useState(false)
  const [selectedContract, setSelectedContract] = useState(null)
  const [appData, setAppData] = useState(null)

  const loadContracts = async () => {
    const { data } = await api.get('/contracts')
    setContracts(data)
  }

  const loadSubscription = async () => {
    const { data } = await api.get('/users/me/subscription')
    setSubscription(data)
  }

  useEffect(() => {
    loadContracts()
    loadSubscription()
  }, [])

  const viewApplicants = async (contractId) => {
    const { data } = await api.get(`/contracts/${contractId}/applications`)
    setSelectedContract(contractId)
    setAppData(data)
  }

  return (
    <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <div className="bg-white border rounded-xl p-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Contractor Dashboard</h1>
          <p className="text-slate-600">Current tier: <span className="capitalize font-semibold">{subscription.tier}</span></p>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setShowUpgrade(true)} className="bg-accent text-white px-4 py-2 rounded">Upgrade Tier</button>
          <button onClick={() => setShowCreate(true)} className="bg-brand text-white px-4 py-2 rounded">Create Contract</button>
        </div>
      </div>

      <section className="grid md:grid-cols-2 gap-4">
        {contracts.map((contract) => (
          <ContractCard
            key={contract.id}
            contract={contract}
            action={<button className="bg-slate-900 text-white px-3 py-2 rounded" onClick={() => viewApplicants(contract.id)}>View Applicants</button>}
          />
        ))}
      </section>

      {selectedContract && appData && (
        <section className="space-y-3">
          <h2 className="text-xl font-semibold">Applications for Contract #{selectedContract}</h2>
          <p className="text-slate-600">Applicants: {appData.applicant_count} | Tier view: {appData.tier}</p>
          {appData.tier === 'free' ? (
            <p className="bg-yellow-50 border border-yellow-200 rounded p-3 text-yellow-800">Upgrade to Standard or Premium to view candidates.</p>
          ) : (
            <ApplicationTable data={appData.applicants} />
          )}
        </section>
      )}

      {showCreate && <CreateContractModal onClose={() => setShowCreate(false)} onCreated={loadContracts} />}
      {showUpgrade && <TierUpgradeModal onClose={() => setShowUpgrade(false)} onUpdated={setSubscription} />}
    </main>
  )
}
