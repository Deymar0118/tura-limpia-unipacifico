
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  obtenerUsuarios,
  obtenerRoles,
  toggleEstadoUsuario,
} from '../services/usuarioService'
import UserTable from '../components/UserTable'
import UserFormModal from '../components/UserFormModal'
import './UsersManagementPage.css'

export default function UsersManagementPage() {
  const [usuarios, setUsuarios] = useState([])
  const [roles, setRoles] = useState([])
  const [cargando, setCargando] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [userToEdit, setUserToEdit] = useState(null)
  const [toastMsg, setToastMsg] = useState('')
  const [toastError, setToastError] = useState(false)

  // Filtros y paginación
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState('')
  const [currentPage, setCurrentPage] = useState(1)

  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    total_pages: 0,
  })

  const [recargarTrigger, setRecargarTrigger] = useState(0)

  // Mostrar notificaciones
  const mostrarMensaje = (mensaje, esError = false) => {
    setToastMsg(mensaje)
    setToastError(esError)
  }

  // Cargar usuarios desde FastAPI
  useEffect(() => {
    let cancelado = false

    async function fetchUsuarios() {
      setCargando(true)

      try {
        const respuesta = await obtenerUsuarios({
          page: currentPage,
          limit: 10,
        })

        if (cancelado) return

        setUsuarios(respuesta.data || [])

        setPagination(
          respuesta.pagination || {
            page: 1,
            limit: 10,
            total: 0,
            total_pages: 0,
          },
        )

        setToastMsg('')
      } catch (error) {
        if (!cancelado) {
          console.error('Error al cargar usuarios:', error)

          mostrarMensaje(
            error.message || 'No se pudieron cargar los usuarios.',
            true,
          )
        }
      } finally {
        if (!cancelado) {
          setCargando(false)
        }
      }
    }

    fetchUsuarios()

    return () => {
      cancelado = true
    }
  }, [currentPage, recargarTrigger])

  // Cargar roles desde FastAPI
  useEffect(() => {
    let cancelado = false

    async function fetchRoles() {
      try {
        const data = await obtenerRoles()

        if (!cancelado) {
          setRoles(data || [])
        }
      } catch (error) {
        if (!cancelado) {
          mostrarMensaje(
            error.message || 'No se pudieron cargar los roles.',
            true,
          )
        }
      }
    }

    fetchRoles()

    return () => {
      cancelado = true
    }
  }, [])

  // Aplicar filtros sobre la página cargada
  const usuariosFiltrados = usuarios.filter((usuario) => {
    const termino = searchTerm.trim().toLowerCase()

    const coincideBusqueda =
      !termino ||
      [
        usuario.nombres,
        usuario.apellidos,
        usuario.nombre_completo,
        usuario.nombre_usuario,
        usuario.correo,
        usuario.perfil?.documento,
      ]
        .filter(Boolean)
        .some((valor) => valor.toLowerCase().includes(termino))

    const rolId = usuario.perfil?.rol?.id

    const coincideRol =
      !selectedRole || String(rolId) === String(selectedRole)

    return coincideBusqueda && coincideRol
  })

  // Abrir formulario de creación
  const handleOpenCreate = () => {
    setUserToEdit(null)
    setIsModalOpen(true)
  }

  // Abrir formulario de edición
  const handleOpenEdit = (usuario) => {
    setUserToEdit(usuario)
    setIsModalOpen(true)
  }

  // Cerrar formulario
  const handleCloseModal = () => {
    setIsModalOpen(false)
    setUserToEdit(null)
  }

  // Actualizar después de crear o editar
  const handleUserSaved = (usuario, isEditing) => {
    const rolNombre =
      usuario.perfil?.rol?.nombre || 'Rol asignado'

    mostrarMensaje(
      isEditing
        ? `Usuario ${usuario.nombres} actualizado correctamente (Rol: ${rolNombre}).`
        : `Funcionario ${usuario.nombres} ${usuario.apellidos} registrado con éxito.`,
    )

    setRecargarTrigger((prev) => prev + 1)
  }

  // Activar o desactivar una cuenta
  const handleToggleStatus = async (id, estadoActual) => {
    try {
      await toggleEstadoUsuario(id, estadoActual)

      mostrarMensaje(
        `Cuenta ${estadoActual ? 'desactivada' : 'activada'} correctamente.`,
      )

      setRecargarTrigger((prev) => prev + 1)
    } catch (error) {
      console.error('Error al actualizar estado:', error)

      mostrarMensaje(
        error.message || 'No se pudo actualizar el estado del usuario.',
        true,
      )
    }
  }

  return (
    <div className="admin-page-container">
      <header className="admin-header">
        <div>
          <span className="admin-header-badge">
            Panel Administrativo
          </span>

          <h1 className="admin-header-title">
            Gestión de Usuarios
          </h1>
        </div>

        <div className="admin-header-actions">
          <Link to="/dashboard" className="btn-back-link">
            ← Volver al Dashboard
          </Link>

          <button
            type="button"
            className="btn-primary-action"
            onClick={handleOpenCreate}
          >
            <span>+</span> Nuevo Usuario
          </button>
        </div>
      </header>

      <main className="admin-content-card">
        {toastMsg && (
          <div
            className={`admin-toast-message ${
              toastError ? 'admin-toast-message--error' : ''
            }`}
            role="status"
          >
            <span>{toastMsg}</span>

            <button
              type="button"
              onClick={() => setToastMsg('')}
              aria-label="Cerrar notificación"
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                color: toastError ? '#991b1b' : '#065f46',
              }}
            >
              &times;
            </button>
          </div>
        )}

        <div className="admin-filters-bar">
          <div className="search-input-wrapper">
            <input
              type="text"
              className="admin-search-input"
              placeholder="Buscar en esta página..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <select
            className="admin-role-select"
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
          >
            <option value="">Todos los roles</option>

            {roles.map((rol) => (
              <option key={rol.id} value={rol.id}>
                {rol.nombre}
              </option>
            ))}
          </select>
        </div>

        <UserTable
          usuarios={usuariosFiltrados}
          cargando={cargando}
          pagination={pagination}
          onPageChange={(nuevaPagina) => {
            setCurrentPage(nuevaPagina)
            setSearchTerm('')
            setSelectedRole('')
          }}
          onToggleStatus={handleToggleStatus}
          onEditUser={handleOpenEdit}
        />
      </main>

      {isModalOpen && (
        <UserFormModal
          key={userToEdit ? `edit-${userToEdit.id}` : 'create'}
          isOpen={isModalOpen}
          userToEdit={userToEdit}
          onClose={handleCloseModal}
          onUserCreated={handleUserSaved}
        />
      )}
    </div>
  )
}
