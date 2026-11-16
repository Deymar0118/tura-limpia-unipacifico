
import { useState, useEffect } from 'react'
import {
  registrarUsuarioAdmin,
  actualizarUsuario,
  asignarPerfilUsuario,
  obtenerRoles,
} from '../services/usuarioService'
import './UserFormModal.css'

function obtenerFechaActual() {
  const fecha = new Date()
  const anio = fecha.getFullYear()
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')

  return `${anio}-${mes}-${dia}`
}

function obtenerRolActual(usuario) {
  return usuario?.perfil?.rol?.id
    ? String(usuario.perfil.rol.id)
    : ''
}

function formatearError(error) {
  const detalle = error?.detail

  if (Array.isArray(detalle)) {
    return detalle
      .map((item) => {
        if (typeof item === 'string') return item
        if (item?.msg) {
          const campo = Array.isArray(item.loc)
            ? item.loc.filter((parte) => parte !== 'body').join('. ')
            : ''

          return campo ? `${campo}: ${item.msg}` : item.msg
        }

        return JSON.stringify(item)
      })
      .join('\n')
  }

  if (typeof detalle === 'string') {
    return detalle
  }

  if (detalle && typeof detalle === 'object') {
    return (
      detalle.message ||
      detalle.mensaje ||
      JSON.stringify(detalle)
    )
  }

  return error?.message || 'Error al comunicarse con el servidor.'
}

export default function UserFormModal({
  isOpen,
  onClose,
  onUserCreated,
  userToEdit = null,
}) {
  const [roles, setRoles] = useState([])
  const [cargando, setCargando] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const isEditing = Boolean(userToEdit)

  const [formData, setFormData] = useState({
    nombres: '',
    apellidos: '',
    nombre_usuario: '',
    correo: '',
    password: '',
    telefono: '',
    documento: '',
    rol_id: '',
    fecha_inicio: obtenerFechaActual(),
    cargo: '',
  })

  useEffect(() => {
    if (!isOpen) return

    let cancelado = false

    async function inicializarFormulario() {
      setErrorMsg('')

      setFormData({
        nombres: userToEdit?.nombres || '',
        apellidos: userToEdit?.apellidos || '',
        nombre_usuario: userToEdit?.nombre_usuario || '',
        correo: userToEdit?.correo || '',
        password: '',
        telefono: userToEdit?.telefono || '',
        documento: userToEdit?.perfil?.documento || '',
        rol_id: obtenerRolActual(userToEdit),
        fecha_inicio:
          userToEdit?.perfil?.fecha_inicio || obtenerFechaActual(),
        cargo: userToEdit?.perfil?.cargo || '',
      })

      try {
        const data = await obtenerRoles()

        if (cancelado) return

        setRoles(data)

        setFormData((prev) => ({
          ...prev,
          rol_id: prev.rol_id || (
            data[0]?.id ? String(data[0].id) : ''
          ),
        }))
      } catch (error) {
        if (!cancelado) {
          setErrorMsg(formatearError(error))
        }
      }
    }

    inicializarFormulario()

    return () => {
      cancelado = true
    }
  }, [isOpen, userToEdit])

  if (!isOpen) return null

  const handleChange = (e) => {
    const { name, value } = e.target

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrorMsg('')

    if (!formData.nombres.trim() || !formData.apellidos.trim()) {
      setErrorMsg('Nombres y apellidos son obligatorios.')
      return
    }

    if (!formData.nombre_usuario.trim()) {
      setErrorMsg('El nombre de usuario es obligatorio.')
      return
    }

    if (!formData.correo.trim()) {
      setErrorMsg('El correo electrónico es obligatorio.')
      return
    }

    if (!isEditing && formData.password.length < 8) {
      setErrorMsg('La contraseña debe tener al menos 8 caracteres.')
      return
    }

    if (!isEditing && !formData.documento.trim()) {
      setErrorMsg('El documento de identidad es obligatorio.')
      return
    }

    if (!formData.rol_id) {
      setErrorMsg('Debe seleccionar un rol.')
      return
    }

    if (!formData.fecha_inicio) {
      setErrorMsg('La fecha de inicio es obligatoria.')
      return
    }

    const datosPersonales = {
      nombres: formData.nombres.trim(),
      apellidos: formData.apellidos.trim(),
      nombre_usuario: formData.nombre_usuario.trim(),
      correo: formData.correo.trim(),
    }

    if (formData.telefono.trim()) {
      datosPersonales.telefono = formData.telefono.trim()
    }

    const rolSeleccionado = roles.find(
      (rol) => String(rol.id) === String(formData.rol_id),
    )

    const esTrabajador = (
      rolSeleccionado?.nombre || ''
    ).toLowerCase().includes('trabajador')

    try {
      setCargando(true)

      let resultado

      if (!isEditing) {
        const payload = {
          ...datosPersonales,
          password: formData.password,
          perfil: {
            documento: formData.documento.trim(),
            rol_id: Number(formData.rol_id),
            fecha_inicio: formData.fecha_inicio,
            estado: true,
          },
        }

        if (esTrabajador && formData.cargo.trim()) {
          payload.perfil.cargo = formData.cargo.trim()
        }

        const respuesta = await registrarUsuarioAdmin(payload)
        resultado = respuesta.data
      } else {
        const idUsuario = userToEdit.id

        if (!idUsuario) {
          throw new Error('No se encontró el identificador del usuario.')
        }

        resultado = await actualizarUsuario(
          idUsuario,
          datosPersonales,
        )

        const rolActual = obtenerRolActual(userToEdit)

        if (rolActual !== String(formData.rol_id)) {
          const datosPerfil = {
            id_rol: Number(formData.rol_id),
            fecha_inicio: formData.fecha_inicio,
          }

          if (esTrabajador && formData.cargo.trim()) {
            datosPerfil.cargo = formData.cargo.trim()
          }

          resultado = await asignarPerfilUsuario(
            idUsuario,
            datosPerfil,
          )
        }
      }

      if (resultado) {
        onUserCreated?.(resultado, isEditing)
        onClose()
      } else {
        setErrorMsg('El servidor no devolvió los datos esperados.')
      }
    } catch (error) {
      console.error('Error al guardar usuario:', error)
      setErrorMsg(formatearError(error))
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal-container">
        <div className="modal-header">
          <div>
            <h2 className="modal-title">
              {isEditing
                ? 'Editar Funcionario y Rol'
                : 'Registrar Nuevo Funcionario'}
            </h2>

            <p className="modal-subtitle">
              {isEditing
                ? 'Modificar información o asignar un nuevo rol'
                : 'Asignar credenciales y perfil laboral en Tura Limpia'}
            </p>
          </div>

          <button
            type="button"
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Cerrar modal"
            disabled={cargando}
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {errorMsg && (
            <div
              className="modal-alert modal-alert--error"
              role="alert"
              style={{ whiteSpace: 'pre-line' }}
            >
              {errorMsg}
            </div>
          )}

          <h3 className="form-section-title">
            Datos Personales y Acceso
          </h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="nombres">
                Nombres <span className="required">*</span>
              </label>

              <input
                id="nombres"
                type="text"
                name="nombres"
                className="form-input"
                placeholder="Ej. Carlos Andrés"
                value={formData.nombres}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="apellidos">
                Apellidos <span className="required">*</span>
              </label>

              <input
                id="apellidos"
                type="text"
                name="apellidos"
                className="form-input"
                placeholder="Ej. Rodríguez Murillo"
                value={formData.apellidos}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="nombre_usuario">
                Nombre de usuario <span className="required">*</span>
              </label>

              <input
                id="nombre_usuario"
                type="text"
                name="nombre_usuario"
                className="form-input"
                value={formData.nombre_usuario}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="correo">
                Correo institucional <span className="required">*</span>
              </label>

              <input
                id="correo"
                type="email"
                name="correo"
                className="form-input"
                value={formData.correo}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="password">
                {isEditing
                  ? 'Nueva contraseña (No disponible)'
                  : 'Contraseña temporal *'}
              </label>

              <input
                id="password"
                type="password"
                name="password"
                className="form-input"
                value={formData.password}
                onChange={handleChange}
                required={!isEditing}
                disabled={isEditing}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="telefono">
                Teléfono de contacto
              </label>

              <input
                id="telefono"
                type="tel"
                name="telefono"
                className="form-input"
                placeholder="315..."
                value={formData.telefono}
                onChange={handleChange}
              />
            </div>
          </div>

          <hr className="form-section-divider" />

          <h3 className="form-section-title">
            Perfil Laboral y Asignación de Rol
          </h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="documento">
                Documento de identidad (Cédula)
                {!isEditing && <span className="required"> *</span>}
              </label>

              <input
                id="documento"
                type="text"
                name="documento"
                className="form-input"
                value={formData.documento}
                onChange={handleChange}
                required={!isEditing}
                disabled={isEditing && !formData.documento}
              />

              {isEditing && !formData.documento && (
                <small>
                  El listado no proporciona el documento. No se modificará.
                </small>
              )}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="rol_id">
                Rol del sistema <span className="required">*</span>
              </label>

              <select
                id="rol_id"
                name="rol_id"
                className="form-select"
                value={formData.rol_id}
                onChange={handleChange}
                required
              >
                <option value="">Seleccionar rol</option>

                {roles.map((rol) => (
                  <option key={rol.id} value={rol.id}>
                    {rol.nombre}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="fecha_inicio">
                Fecha de inicio de funciones
              </label>

              <input
                id="fecha_inicio"
                type="date"
                name="fecha_inicio"
                className="form-input"
                value={formData.fecha_inicio}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="cargo">
                Cargo (si corresponde)
              </label>

              <input
                id="cargo"
                type="text"
                name="cargo"
                className="form-input"
                placeholder="Ej. Operario de recolección"
                value={formData.cargo}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="modal-actions">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={cargando}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="btn-submit"
              disabled={cargando}
            >
              {cargando
                ? 'Guardando...'
                : isEditing
                  ? 'Guardar Cambios'
                  : 'Crear Usuario'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
