import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthLayout from '../components/AuthLayout'
import { iniciarSesion, obtenerMensajeAuth } from '../services/authService'

export default function LoginPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await iniciarSesion({
        email: form.email.trim(),
        password: form.password,
      })
      navigate('/')
    } catch (err) {
      setError(obtenerMensajeAuth(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Bienvenido de"
      accent="nuevo."
      description="Ingresa para consultar rutas, flota e incidencias del servicio de aseo en Buenaventura."
      footer={<>¿No tienes cuenta? <Link to="/registro">Regístrate</Link></>}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-field">
          <label htmlFor="email">Correo electrónico</label>
          <input
            id="email"
            name="email"
            type="email"
            className="auth-input"
            placeholder="tucorreo@ejemplo.com"
            value={form.email}
            onChange={handleChange}
            disabled={loading}
            required
          />
        </div>

        <div className="auth-field">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <label htmlFor="password">Contraseña</label>
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
            placeholder="Tu contraseña"
            value={form.password}
            onChange={handleChange}
            disabled={loading}
            required
          />
        </div>
                <Link className="auth-link" to="/recuperar-contrasena">
                  ¿Olvidaste tu contraseña?
                </Link>

        {error && <p className="auth-error" role="alert">{error}</p>}

        <button type="submit" className="auth-btn" disabled={loading}>
          {loading ? 'Ingresando…' : 'Iniciar sesión'}
        </button>
      </form>
    </AuthLayout>
  )
}
