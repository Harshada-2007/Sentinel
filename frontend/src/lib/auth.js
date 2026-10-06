export const USERS = [
  { email: 'admin@sentinel.dev',  password: 'admin123',  name: 'Admin User',  role: 'admin' },
  { email: 'ops@sentinel.dev',    password: 'ops123',    name: 'Ops User',    role: 'operator' },
  { email: 'viewer@sentinel.dev', password: 'viewer123', name: 'Viewer User', role: 'viewer' },
]

const KEY = 'sentinel.session'

export function login(email, password) {
  const u = USERS.find(x => x.email.toLowerCase() === email.trim().toLowerCase() && x.password === password)
  if (!u) return { error: 'Invalid email or password' }
  const session = { email: u.email, name: u.name, role: u.role, at: Date.now() }
  localStorage.setItem(KEY, JSON.stringify(session))
  return { session }
}

export function logout() {
  localStorage.removeItem(KEY)
}

export function getSession() {
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? JSON.parse(raw) : null
  } catch { return null }
}