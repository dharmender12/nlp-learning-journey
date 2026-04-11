import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { setAuth } from '../services/auth'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/login', { email, password })
      setAuth(data.access_token, data.user)
      if (data.user.role === 'contractor') navigate('/contractor')
      else if (data.user.role === 'trainer') navigate('/trainer')
      else navigate('/admin')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen grid place-items-center bg-gradient-to-br from-teal-50 to-orange-50 px-4">
      <form onSubmit={submit} className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold">Welcome back</h1>
        <input className="w-full border rounded p-3" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input className="w-full border rounded p-3" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="w-full bg-brand text-white rounded p-3">Login</button>
        <p className="text-sm text-slate-600">No account? <Link className="text-brand underline" to="/register">Register</Link></p>
      </form>
    </div>
  )
}
