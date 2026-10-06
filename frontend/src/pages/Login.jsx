import { useState } from 'react'
import { Link, useNavigate, useLocation, Navigate } from 'react-router-dom'
import { ShieldCheck, Mail, Lock, Loader2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext.jsx'

const DEMO_HINT = { email: 'admin@sentinel.dev', password: 'admin123' }

export default function Login() {
  const { signIn, user } = useAuth()
  const nav = useNavigate()
  const loc = useLocation()
  const from = loc.state?.from?.pathname || '/dashboard'

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')

  if (user) return <Navigate to={from} replace />

  const submit = async (e) => {
    e.preventDefault()
    setErr('')
    setBusy(true)
    const { error } = await signIn(email, password)
    setBusy(false)
    if (error) return setErr(error.message)
    nav(from, { replace: true })
  }

  const fillDemo = () => {
    setEmail(DEMO_HINT.email)
    setPassword(DEMO_HINT.password)
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-ink-900">
      <div className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <span className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-glow mb-3">
            <ShieldCheck className="text-white" size={22} />
          </span>
          <h1 className="text-white text-xl font-semibold tracking-tight">Sign in to Sentinel</h1>
          <p className="text-xs text-slate-500 mt-1">AI Supply Chain Control Tower</p>
        </div>

        <form onSubmit={submit} className="card space-y-4">
          <label className="block">
            <span className="text-xs text-slate-400 mb-1.5 block">Email</span>
            <div className="relative">
              <Mail size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input type="email" required autoFocus className="input pl-9"
                value={email} onChange={e => setEmail(e.target.value)} placeholder="you@company.com" />
            </div>
          </label>

          <label className="block">
            <span className="text-xs text-slate-400 mb-1.5 block">Password</span>
            <div className="relative">
              <Lock size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input type="password" required className="input pl-9"
                value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" />
            </div>
          </label>

          {err && <div className="text-xs text-red-400 bg-red-500/10 border border-red-500/30 rounded-lg p-2">{err}</div>}

          <button className="btn w-full" disabled={busy}>
            {busy ? <><Loader2 size={14} className="animate-spin" /> Signing in…</> : 'Sign in'}
          </button>

          <button type="button" onClick={fillDemo}
            className="w-full text-[11px] text-slate-500 hover:text-slate-300 transition-colors">
            Use demo credentials (admin@sentinel.dev / admin123)
          </button>
        </form>

        <div className="text-center text-xs text-slate-500 mt-6">
          <Link to="/" className="hover:text-slate-300">← Back to home</Link>
        </div>
      </div>
    </div>
  )
}