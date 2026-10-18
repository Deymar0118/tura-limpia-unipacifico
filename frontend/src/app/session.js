// Gestión del estado de sesión y autenticación
const SESSION_KEY = 'turalimpia.session'

export const getSession = () => {
  const raw = localStorage.getItem(SESSION_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export const setSession = (session) => {
  if (session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
  } else {
    localStorage.removeItem(SESSION_KEY)
  }
  return session
}

export const clearSession = () => {
  localStorage.removeItem(SESSION_KEY)
}
