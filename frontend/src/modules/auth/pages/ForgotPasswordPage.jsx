import { useState } from 'react'
import { Link } from 'react-router-dom'
import { solicitarRecuperacion, obtenerMensajeAuth } from '../services/authService'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await solicitarRecuperacion({ email: email.trim() })
      setSent(true)
    } catch (err) {
      setError(obtenerMensajeAuth(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      title="Recupera tu"
      accent="acceso."
      description="Escribe el correo de tu cuenta y te enviaremos un enlace para crear una nueva contraseña."
      footer={<>¿Ya la recordaste? <Link to="/login">Inicia sesión</Link></>}
    >
      {sent ? (
        <p className="auth-success" role="status">
          Si existe una cuenta con <strong>{email.trim()}</strong>, te enviamos
          un enlace para restablecer tu contraseña. Revisa también la carpeta
          de spam.
        </p>
      ) : (
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label htmlFor="email">Correo electrónico</label>
            <input
              id="email"
              name="email"
              type="email"
              className="auth-input"
              placeholder="tucorreo@ejemplo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              required
            />
          </div>

          {error && <p className="auth-error" role="alert">{error}</p>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? 'Enviando…' : 'Enviar enlace'}
          </button>
        </form>
      )}
    </div>
  )
}
