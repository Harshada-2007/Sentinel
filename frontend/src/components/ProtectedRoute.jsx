import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  const loc = useLocation()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-6 h-6 rounded-full border-2 border-slate-600 border-t-accent animate-spin" />
      </div>
    )
  }
  if (!user) return <Navigate to="/login" state={{ from: loc }} replace />
  return children
}