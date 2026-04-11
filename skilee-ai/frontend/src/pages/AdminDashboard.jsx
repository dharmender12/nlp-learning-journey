import { useEffect, useState } from 'react'
import api from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('/users/admin/stats').then(({ data }) => setStats(data))
  }, [])

  if (!stats) {
    return <main className="max-w-5xl mx-auto px-4 py-6">Loading admin analytics...</main>
  }

  const bars = [
    { name: 'Users', value: stats.total_users },
    { name: 'Contracts', value: stats.total_contracts },
    { name: 'Applications', value: stats.total_applications },
  ]

  const revenue = [
    { name: 'Revenue', value: stats.revenue_inr },
    { name: 'Remaining', value: Math.max(1, 5000 - stats.revenue_inr) },
  ]

  return (
    <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      <div className="grid md:grid-cols-4 gap-4">
        <StatCard title="Total Users" value={stats.total_users} />
        <StatCard title="Total Contracts" value={stats.total_contracts} />
        <StatCard title="Total Applications" value={stats.total_applications} />
        <StatCard title="Revenue (INR)" value={`₹${stats.revenue_inr}`} />
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white border rounded-xl p-4 h-72">
          <h3 className="font-semibold mb-2">Platform Activity</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={bars}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0f766e" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white border rounded-xl p-4 h-72">
          <h3 className="font-semibold mb-2">Revenue Snapshot</h3>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={revenue} dataKey="value" innerRadius={50} outerRadius={80}>
                <Cell fill="#ea580c" />
                <Cell fill="#f1f5f9" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </main>
  )
}

function StatCard({ title, value }) {
  return (
    <div className="bg-white border rounded-xl p-4">
      <p className="text-sm text-slate-500">{title}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  )
}
