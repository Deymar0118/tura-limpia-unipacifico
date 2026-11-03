import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import AuthLayout from '../components/AuthLayout'
import { restablecerContrasena, obtenerMensajeAuth } from '../services/authService'

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [form, setForm] = useState({ password: '', confirm: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (form.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.')
      return
    }

    if (form.password !== form.confirm) {
      setError('Las contraseñas no coinciden.')
      return
    }

    setLoading(true)

    try {
      await restablecerContrasena({ token, password: form.password })
      setDone(true)
    } catch (err) {
      setError(obtenerMensajeAuth(err))
    } finally {
      setLoading(false)
    }
  }

  const renderContent = () => {
    if (!token) {
      return (
        <div className="auth-form">
          <p className="auth-error" role="alert">
            Este enlace no es válido o está incompleto.
          </p>
          <Link className="auth-link" to="/recuperar-contrasena">
            Solicitar un nuevo enlace
          </Link>
        </div>
      )
    }

    if (done) {
      return (
        <div className="auth-form">
          <p className="auth-success" role="status">
            Tu contraseña se actualizó correctamente.
          </p>
          <Link className="auth-btn" to="/login">
            Ir a iniciar sesión
          </Link>
        </div>
      )
    }

    return (
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-field">
          <div className="auth-field__row">
            <label htmlFor="password">Nueva contraseña</label>
            <button
              type="button"
              onClick={() => setShowPassword((prev) => !prev)}
              className="auth-toggle-btn"
            >
              {showPassword ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
          <input
            id="password"
            name="password"
            type={showPassword ? 'text' : 'password'}
            className="auth-input"
            placeholder="Mínimo 8 caracteres"
            value={form.password}
            onChange={handleChange}
            minLength={8}
            disabled={loading}
            required
          />
        </div>

        <div className="auth-field">
          <div className="auth-field__row">
            <label htmlFor="confirm">Confirmar contraseña</label>
            <button
              type="button"
              onClick={() => setShowConfirm((prev) => !prev)}
              className="auth-toggle-btn"
            >
              {showConfirm ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
          <input
            id="confirm"
            name="confirm"
            type={showConfirm ? 'text' : 'password'}
            className="auth-input"
            placeholder="Repite tu contraseña"
            value={form.confirm}
            onChange={handleChange}
            disabled={loading}
            required
          />
        </div>

        {error && <p className="auth-error" role="alert">{error}</p>}

        <button type="submit" className="auth-btn" disabled={loading}>
          {loading ? 'Guardando…' : 'Guardar contraseña'}
        </button>
      </form>
    )
  }

  return (
    <AuthLayout
      title="Crea una nueva"
      accent="contraseña."
      description="Elige una contraseña segura que no uses en otros sitios."
      footer={<>¿Necesitas ayuda? <Link to="/login">Volver al inicio de sesión</Link></>}
    >
      {renderContent()}
    </AuthLayout>
  )
}
