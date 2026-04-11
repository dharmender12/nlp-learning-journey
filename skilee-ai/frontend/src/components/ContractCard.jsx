export default function ContractCard({ contract, action }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <h3 className="text-lg font-semibold">{contract.title}</h3>
      <p className="text-sm text-slate-500 mt-1">{contract.company_name}</p>
      <p className="mt-2 text-slate-700">{contract.description}</p>
      <div className="mt-3 flex gap-2 text-xs">
        <span className="bg-teal-100 text-teal-700 px-2 py-1 rounded">{contract.subject}</span>
        <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded">Need: {contract.required_trainers}</span>
      </div>
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
