import { Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Layout from './components/Layout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Suppliers from './pages/Suppliers.jsx'
import Inventory from './pages/Inventory.jsx'
import Disruptions from './pages/Disruptions.jsx'
import ImpactAnalysis from './pages/ImpactAnalysis.jsx'
import Simulator from './pages/Simulator.jsx'
import Recommendations from './pages/Recommendations.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/suppliers" element={<Suppliers />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/disruptions" element={<Disruptions />} />
        <Route path="/impact" element={<ImpactAnalysis />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}