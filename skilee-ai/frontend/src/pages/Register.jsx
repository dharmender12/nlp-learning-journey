import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { setAuth } from '../services/auth'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '', role: 'trainer' })
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/register', form)
      setAuth(data.access_token, data.user)
      if (data.user.role === 'contractor') navigate('/contractor')
      else if (data.user.role === 'trainer') navigate('/trainer')
      else navigate('/admin')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen grid place-items-center bg-gradient-to-br from-orange-50 to-teal-50 px-4">
      <form onSubmit={submit} className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold">Create account</h1>
        <input className="w-full border rounded p-3" type="email" placeholder="Email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
        <input className="w-full border rounded p-3" type="password" placeholder="Password" required minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        <select className="w-full border rounded p-3" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="trainer">Trainer</option>
          <option value="contractor">Contractor</option>
          <option value="admin">Admin</option>
        </select>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="w-full bg-brand text-white rounded p-3">Register</button>
        <p className="text-sm text-slate-600">Already have account? <Link className="text-brand underline" to="/login">Login</Link></p>
      </form>
    </div>
  )
}
