import { createContext, useContext, useEffect, useState } from 'react'
import { login as doLogin, logout as doLogout, getSession } from '../lib/auth.js'

const AuthCtx = createContext(null)

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setSession(getSession())
    setLoading(false)
  }, [])

  const signIn = async (email, password) => {
    const { session, error } = doLogin(email, password)
    if (error) return { error: { message: error } }
    setSession(session)
    return { session }
  }

  const signOut = async () => {
    doLogout()
    setSession(null)
  }

  return (
    <AuthCtx.Provider value={{ session, user: session, loading, signIn, signOut }}>
      {children}
    </AuthCtx.Provider>
  )
}

export const useAuth = () => useContext(AuthCtx)