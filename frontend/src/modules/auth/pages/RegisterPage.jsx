import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthLayout from '../components/AuthLayout'
import { registrarUsuario, obtenerMensajeAuth } from '../services/authService'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    nombre: '',
    email: '',
    password: '',
    confirm: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

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
      await registrarUsuario({
        nombre: form.nombre.trim(),
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
      title="Crea tu"
      accent="cuenta."
      description="Regístrate para consultar rutas y horarios de recolección en el Distrito de Buenaventura."
      footer={<>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></>}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="auth-field">
          <label htmlFor="nombre">Nombre completo</label>
          <input
            id="nombre"
            name="nombre"
            type="text"
            className="auth-input"
            placeholder="Tu nombre"
            value={form.nombre}
            onChange={handleChange}
            disabled={loading}
            required
          />
        </div>

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
            placeholder="Mínimo 8 caracteres"
            value={form.password}
            onChange={handleChange}
            minLength={8}
            disabled={loading}
            required
          />
        </div>

        <div className="auth-field">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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
          {loading ? 'Creando cuenta…' : 'Crear cuenta'}
        </button>
      </form>
    </AuthLayout>
  )
}
