import {
  apiClient,
  clearAuthTokens,
  setAuthTokens,
} from '../../../shared/api/apiClient'
import { clearSession, setSession } from '../../../app/session'

async function autenticar(ruta, body) {
  const tokens = await apiClient(ruta, {
    metodo: 'POST',
    body,
  })

  setAuthTokens(tokens)

  try {
    const usuario = await apiClient('/auth/me')
    setSession(usuario)
    return { tokens, usuario }
  } catch (error) {
    clearAuthTokens()
    clearSession()
    throw error
  }
}

export function iniciarSesion({ email, password }) {
  return autenticar('/auth/login', {
    email,
    password,
  })
}

export function registrarUsuario({ nombre, email, password }) {
  return autenticar('/auth/registro', {
    nombre,
    email,
    password,
  })
}

export async function cerrarSesion() {
  try {
    await apiClient('/auth/logout', { metodo: 'POST' })
  } catch {
    // Si la llamada falla o el backend no está disponible, aseguramos la limpieza local
  } finally {
    clearAuthTokens()
    clearSession()
  }
}

export function obtenerMensajeAuth(error) {
  if (Array.isArray(error?.detail)) {
    return error.detail.map((item) => item.msg).join('. ')
  }

  return error?.detail || error?.message || 'No se pudo completar la operación'
}
