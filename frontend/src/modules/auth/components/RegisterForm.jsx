
import { useState, useMemo } from 'react'
import './AuthForms.css'

const REGLAS_CONTRASENA = [
  {
    id: 'longitud',
    test: (v) => v.length >= 8,
    texto: 'Al menos 8 caracteres',
  },
  {
    id: 'maximo',
    test: (v) => new TextEncoder().encode(v).length <= 72,
    texto: 'Máximo 72 bytes',
  },
]

function RegisterForm({ onSubmit, isSubmitting = false }) {
  const [nombres, setNombres] = useState('')
  const [apellidos, setApellidos] = useState('')
  const [nombreUsuario, setNombreUsuario] = useState('')
  const [correo, setCorreo] = useState('')
  const [telefono, setTelefono] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [confirmacion, setConfirmacion] = useState('')
  const [errorConfirmacion, setErrorConfirmacion] = useState('')
  const [mostrarReglas, setMostrarReglas] = useState(false)

  const validacion = useMemo(
    () =>
      REGLAS_CONTRASENA.map((regla) => ({
        ...regla,
        cumplida: regla.test(contrasena),
      })),
    [contrasena],
  )

  const contrasenaValida = validacion.every((regla) => regla.cumplida)

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!contrasenaValida) return

    if (contrasena !== confirmacion) {
      setErrorConfirmacion('Las contraseñas no coinciden.')
      return
    }

    setErrorConfirmacion('')

    onSubmit?.({
      nombres,
      apellidos,
      nombreUsuario,
      correo,
      telefono,
      contrasena,
    })
  }

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <label className="auth-form__field">
        <span className="auth-form__label">Nombres</span>
        <input
          className="auth-form__input"
          type="text"
          name="nombres"
          placeholder="Tus nombres"
          autoComplete="given-name"
          value={nombres}
          onChange={(e) => setNombres(e.target.value)}
          minLength={2}
          maxLength={100}
          required
        />
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Apellidos</span>
        <input
          className="auth-form__input"
          type="text"
          name="apellidos"
          placeholder="Tus apellidos"
          autoComplete="family-name"
          value={apellidos}
          onChange={(e) => setApellidos(e.target.value)}
          minLength={2}
          maxLength={100}
          required
        />
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Nombre de usuario</span>
        <input
          className="auth-form__input"
          type="text"
          name="nombreUsuario"
          placeholder="Ej. juanperez"
          autoComplete="username"
          value={nombreUsuario}
          onChange={(e) => setNombreUsuario(e.target.value)}
          minLength={3}
          maxLength={50}
          required
        />
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Correo electrónico</span>
        <input
          className="auth-form__input"
          type="email"
          name="correo"
          placeholder="nombre@ejemplo.com"
          autoComplete="email"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
        />
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Teléfono (opcional)</span>
        <input
          className="auth-form__input"
          type="tel"
          name="telefono"
          placeholder="Número de contacto"
          autoComplete="tel"
          value={telefono}
          onChange={(e) => setTelefono(e.target.value)}
          maxLength={20}
        />
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Contraseña</span>
        <input
          className="auth-form__input"
          type="password"
          name="contrasena"
          placeholder="Crea una contraseña segura"
          autoComplete="new-password"
          value={contrasena}
          onChange={(e) => {
            setContrasena(e.target.value)
            setMostrarReglas(true)
          }}
          minLength={8}
          required
        />

        {mostrarReglas && (
          <ul className="auth-form__rules" aria-label="Requisitos de contraseña">
            {validacion.map((regla) => (
              <li
                key={regla.id}
                className={
                  regla.cumplida
                    ? 'auth-form__rule is-met'
                    : 'auth-form__rule'
                }
              >
                <span className="auth-form__rule-icon" aria-hidden="true">
                  {regla.cumplida ? '✓' : '○'}
                </span>
                {regla.texto}
              </li>
            ))}
          </ul>
        )}
      </label>

      <label className="auth-form__field">
        <span className="auth-form__label">Confirmar contraseña</span>
        <input
          className="auth-form__input"
          type="password"
          name="confirmacion"
          placeholder="Repite tu contraseña"
          autoComplete="new-password"
          value={confirmacion}
          onChange={(e) => {
            setConfirmacion(e.target.value)
            setErrorConfirmacion('')
          }}
          required
        />

        {errorConfirmacion && (
          <span className="auth-form__error" role="alert">
            {errorConfirmacion}
          </span>
        )}
      </label>

      <button
        type="submit"
        className="auth-form__submit"
        disabled={isSubmitting || !contrasenaValida}
      >
        {isSubmitting ? 'Creando cuenta...' : 'Registrar cuenta'}
      </button>
    </form>
  )
}

export default RegisterForm
