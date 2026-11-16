
import { clearSession } from '../../app/session'

const API_BASE_URL = (
  import.meta.env.VITE_API_URL || 'http://localhost:8000'
).replace(/\/+$/, '')

const TOKENS_KEY = 'turalimpia.tokens'

export class ApiError extends Error {
  constructor(status, detail) {
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join('. ')
      : typeof detail === 'string'
        ? detail
        : 'Error de comunicación con el servidor'

    super(message)

    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

export function setAuthTokens({ access_token }) {
  localStorage.setItem(
    TOKENS_KEY,
    JSON.stringify({ access_token }),
  )
}

export function clearAuthTokens() {
  localStorage.removeItem(TOKENS_KEY)
}

export function getAccessToken() {
  const raw = localStorage.getItem(TOKENS_KEY)

  if (!raw) return null

  try {
    return JSON.parse(raw).access_token || null
  } catch {
    return null
  }
}

export async function apiClient(
  ruta,
  { metodo = 'GET', body, query } = {},
) {
  const url = new URL(`${API_BASE_URL}${ruta}`)

  if (query) {
    Object.entries(query).forEach(([clave, valor]) => {
      if (valor !== undefined && valor !== null && valor !== '') {
        url.searchParams.set(clave, valor)
      }
    })
  }

  const headers = {
    Accept: 'application/json',
  }

  const token = getAccessToken()

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const config = {
    method: metodo,
    headers,
  }

  if (body !== undefined) {
    if (body instanceof FormData) {
      config.body = body
    } else {
      headers['Content-Type'] = 'application/json'
      config.body = JSON.stringify(body)
    }
  }

  let response

  try {
    response = await fetch(url.toString(), config)
  } catch {
    throw new ApiError(
      0,
      'No se pudo conectar con el servidor. Comprueba que FastAPI esté activo.',
    )
  }

  const contentType = response.headers.get('content-type') || ''

  let data = null

  if (contentType.includes('application/json')) {
    try {
      data = await response.json()
    } catch {
      data = null
    }
  }

  if (!response.ok) {
    const rutasPublicas = [
      '/auth/login',
      '/auth/register',
    ]

    if (
      response.status === 401 &&
      token &&
      !rutasPublicas.includes(ruta)
    ) {
      clearAuthTokens()
      clearSession()

      if (window.location.pathname !== '/login') {
        window.location.assign('/login')
      }
    }

    throw new ApiError(
      response.status,
      data?.detail ?? data?.mensaje ?? 'Solicitud fallida',
    )
  }

  return data
}
