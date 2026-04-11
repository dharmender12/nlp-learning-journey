import { Link, useNavigate } from 'react-router-dom'
import { clearAuth, getUser } from '../services/auth'

export default function Navbar() {
  const navigate = useNavigate()
  const user = getUser()

  const onLogout = () => {
    clearAuth()
    navigate('/login')
  }

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-brand">Skilee-AI</Link>
        <div className="flex items-center gap-3">
          {user && <span className="text-sm text-slate-600">{user.email} ({user.role})</span>}
          {user && (
            <button className="bg-slate-900 text-white px-3 py-2 rounded" onClick={onLogout}>
              Logout
            </button>
          )}
        </div>
      </div>
    </header>
  )
}
