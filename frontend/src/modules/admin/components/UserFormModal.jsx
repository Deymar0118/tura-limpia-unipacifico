import { useState, useEffect } from 'react'
import {
  registrarUsuarioAdmin,
  actualizarUsuario,
  obtenerRoles
} from '../services/usuarioService'
import './UserFormModal.css'

export default function UserFormModal({ isOpen, onClose, onUserCreated, userToEdit = null }) {
  const [roles, setRoles] = useState([])
  const [cargando, setCargando] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const isEditing = Boolean(userToEdit)

  const [formData, setFormData] = useState(() => {
    if (userToEdit) {
      return {
        nombres: userToEdit.nombres || '',
        apellidos: userToEdit.apellidos || '',
        nombre_usuario: userToEdit.nombre_usuario || '',
        correo: userToEdit.correo || '',
        password: '',
        telefono: userToEdit.telefono || '',
        documento: userToEdit.perfil?.documento || '',
        rol_id: userToEdit.perfil?.rol?.id ? String(userToEdit.perfil.rol.id) : '',
        fecha_inicio: userToEdit.perfil?.fecha_inicio || new Date().toISOString().split('T')[0]
      }
    }
    return {
      nombres: '',
      apellidos: '',
      nombre_usuario: '',
      correo: '',
      password: '',
      telefono: '',
      documento: '',
      rol_id: '',
      fecha_inicio: new Date().toISOString().split('T')[0]
    }
  })

  useEffect(() => {
    if (!isOpen) return
    let cancelado = false

    obtenerRoles().then((data) => {
      if (!cancelado && data) {
        setRoles(data)
        setFormData((prev) => {
          if (!prev.rol_id && data[0]?.id) {
            return { ...prev, rol_id: String(data[0].id) }
          }
          return prev
        })
      }
    })

    return () => {
      cancelado = true
    }
  }, [isOpen])

  if (!isOpen) return null

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
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
    if (!isEditing && (!formData.password || formData.password.length < 8)) {
      setErrorMsg('La contraseña temporal debe tener al menos 8 caracteres.')
      return
    }
    if (!formData.documento.trim()) {
      setErrorMsg('El documento de identidad (cédula) es obligatorio.')
      return
    }
    if (!formData.rol_id) {
      setErrorMsg('Debe seleccionar un rol para el perfil.')
      return
    }

    const payload = {
      nombres: formData.nombres.trim(),
      apellidos: formData.apellidos.trim(),
      nombre_usuario: formData.nombre_usuario.trim(),
      correo: formData.correo.trim(),
      telefono: formData.telefono.trim(),
      perfil: {
        documento: formData.documento.trim(),
        rol_id: Number(formData.rol_id),
        fecha_inicio: formData.fecha_inicio,
        estado: true
      }
    }

    if (formData.password) {
      payload.password = formData.password
    }

    try {
      setCargando(true)
      let res
      if (isEditing) {
        res = await actualizarUsuario(userToEdit.id, payload)
      } else {
        res = await registrarUsuarioAdmin(payload)
      }

      if (res.success || res.id) {
        onUserCreated(res.data || res, isEditing)
        onClose()
      } else {
        setErrorMsg(res.message || 'No se pudo procesar la operación.')
      }
    } catch (err) {
      setErrorMsg(err.detail || err.message || 'Error al comunicarse con el servidor.')
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
              {isEditing ? 'Editar Funcionario y Rol' : 'Registrar Nuevo Funcionario'}
            </h2>
            <p className="modal-subtitle">
              {isEditing
                ? 'Modificar permisos, rol asignado o información del perfil'
                : 'Asignar credenciales y perfil laboral en Tura Limpia'}
            </p>
          </div>
          <button
            type="button"
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Cerrar modal"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          {errorMsg && <div className="modal-alert modal-alert--error">{errorMsg}</div>}

          <h3 className="form-section-title">Datos Personales y Acceso</h3>

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
                placeholder="crodriguez"
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
                placeholder="carlos@turalimpia.com"
                value={formData.correo}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="password">
                {isEditing ? 'Nueva contraseña (Opcional)' : 'Contraseña temporal *'}
              </label>
              <input
                id="password"
                type="password"
                name="password"
                className="form-input"
                placeholder={isEditing ? 'Dejar en blanco para mantener actual' : 'Mínimo 8 caracteres'}
                value={formData.password}
                onChange={handleChange}
                required={!isEditing}
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

          <h3 className="form-section-title">Perfil Laboral y Asignación de Rol</h3>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label" htmlFor="documento">
                Documento de identidad (Cédula) <span className="required">*</span>
              </label>
              <input
                id="documento"
                type="text"
                name="documento"
                className="form-input"
                placeholder="1114859632"
                value={formData.documento}
                onChange={handleChange}
                required
              />
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
                {roles.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.nombre}
                  </option>
                ))}
              </select>
            </div>
          </div>

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
              {cargando ? 'Guardando...' : isEditing ? 'Guardar Cambios' : 'Crear Usuario'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
