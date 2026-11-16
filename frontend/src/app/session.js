import { clearQueryCache, setQueryCacheScope } from '../shared/api/queryCache'

const SESSION_KEY = 'turalimpia.session'

export const ROLES = Object.freeze({
  ADMIN: 'admin',
  GERENTE: 'gerente',
  TRABAJADOR: 'trabajador',
  CIUDADANO: 'ciudadano',
})

export const ETIQUETA_ROL = Object.freeze({
  admin: 'Administrador',
  gerente: 'Gerente',
  trabajador: 'Trabajador',
  ciudadano: 'Ciudadano',
})

export const getSession = () => {
  const raw = localStorage.getItem(SESSION_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export function saveSession(sesion, { actualizarCache = true } = {}) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(sesion))

  if (actualizarCache) {
    setQueryCacheScope(sesion?.email || 'anon')
  }
}

export function updateSession(cambios) {
  const actual = getSession() || {}
  saveSession({ ...actual, ...cambios }, { actualizarCache: false })
}

export const setSession = (session) => {
  if (session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
  } else {
    localStorage.removeItem(SESSION_KEY)
  }
  return session
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY)
  clearQueryCache()
  setQueryCacheScope('anon')
}

export function getRol() {
  return getSession()?.rol || null
}

export function getUsuario() {
  const sesion = getSession()
  return sesion ? { nombre: sesion.nombre, email: sesion.email, rol: sesion.rol } : null
}

if (typeof localStorage !== 'undefined') {
  setQueryCacheScope(getSession()?.email || 'anon')
}