
import {
  apiClient,
  clearAuthTokens,
  setAuthTokens,
} from '../../../shared/api/apiClient'
import { clearSession, setSession } from '../../../app/session'

// Registro público: crea la cuenta, pero no inicia sesión automáticamente.
export async function registrarUsuario({
  nombres,
  apellidos,
  nombreUsuario,
  correo,
  telefono,
  contrasena,
}) {
  return apiClient('/auth/register', {
    metodo: 'POST',
    body: {
      nombres,
      apellidos,
      nombre_usuario: nombreUsuario,
      correo,
      telefono: telefono || null,
      password: contrasena,
    },
  })
}

// Inicio de sesión: obtiene el JWT y consulta los datos del usuario.
export async function iniciarSesion({ identificador, password }) {
  clearAuthTokens()
  clearSession()

  const tokens = await apiClient('/auth/login', {
    metodo: 'POST',
    body: {
      email: identificador,
      password,
    },
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

// El backend todavía no tiene endpoint de logout.
// La sesión se cierra eliminando el token local.
export async function cerrarSesion() {
  clearAuthTokens()
  clearSession()
}

export function obtenerMensajeAuth(error) {
  if (Array.isArray(error?.detail)) {
    return error.detail
      .map((item) => item.msg)
      .join('. ')
  }

  if (typeof error?.detail === 'string') {
    return error.detail
  }

  return error?.message || 'No se pudo completar la operación.'
}
