import { Navigate, Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import ContractorDashboard from './pages/ContractorDashboard'
import TrainerDashboard from './pages/TrainerDashboard'
import AdminDashboard from './pages/AdminDashboard'
import { getUser, isAuthed } from './services/auth'

function ProtectedRoute({ children, role }) {
  const user = getUser()
  if (!isAuthed() || !user) return <Navigate to="/login" replace />
  if (role && user.role !== role) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/contractor" element={<ProtectedRoute role="contractor"><ContractorDashboard /></ProtectedRoute>} />
        <Route path="/trainer" element={<ProtectedRoute role="trainer"><TrainerDashboard /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>} />
      </Routes>
    </div>
  )
}
