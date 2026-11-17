import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  obtenerUsuarios,
  obtenerRoles,
  toggleEstadoUsuario
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

  // Filtros y paginación
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [pagination, setPagination] = useState({ page: 1, limit: 10, total: 0, total_pages: 1 })

  const [recargarTrigger, setRecargarTrigger] = useState(0)

  useEffect(() => {
    let cancelado = false
    async function fetchUsuarios() {
      setCargando(true)
      try {
        const res = await obtenerUsuarios({
          page: currentPage,
          limit: 10,
          q: searchTerm,
          rol_id: selectedRole
        })
        if (!cancelado && res.data) {
          setUsuarios(res.data)
          if (res.pagination) setPagination(res.pagination)
        }
      } catch (err) {
        console.error('Error al cargar usuarios:', err)
      } finally {
        if (!cancelado) setCargando(false)
      }
    }

    fetchUsuarios()
    return () => {
      cancelado = true
    }
  }, [currentPage, searchTerm, selectedRole, recargarTrigger])

  useEffect(() => {
    let cancelado = false
    obtenerRoles().then((data) => {
      if (!cancelado) setRoles(data || [])
    })
    return () => {
      cancelado = true
    }
  }, [])

  const handleOpenCreate = () => {
    setUserToEdit(null)
    setIsModalOpen(true)
  }

  const handleOpenEdit = (usuario) => {
    setUserToEdit(usuario)
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setUserToEdit(null)
  }

  const handleUserSaved = (usuario, isEditing) => {
    const rolNombre = usuario.perfil?.rol?.nombre || 'Rol asignado'
    setToastMsg(
      isEditing
        ? `Usuario ${usuario.nombres} actualizado correctamente (Rol: ${rolNombre}).`
        : `Funcionario ${usuario.nombres} ${usuario.apellidos} registrado con éxito.`
    )
    setRecargarTrigger((prev) => prev + 1)
    setTimeout(() => setToastMsg(''), 4000)
  }

  const handleToggleStatus = async (id, estadoActual) => {
    try {
      await toggleEstadoUsuario(id, estadoActual)
      setRecargarTrigger((prev) => prev + 1)
      setToastMsg(`Estado del funcionario actualizado correctamente.`)
      setTimeout(() => setToastMsg(''), 3000)
    } catch (err) {
      console.error('Error al actualizar estado:', err)
    }
  }

  return (
    <div className="admin-page-container">
      <header className="admin-header">
        <div>
          <span className="admin-header-badge">Panel Administrativo</span>
          <h1 className="admin-header-title">Gestión de Usuarios</h1>
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
          <div className="admin-toast-message">
            <span>{toastMsg}</span>
            <button
              type="button"
              onClick={() => setToastMsg('')}
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#065f46' }}
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
              placeholder="Buscar por nombre, correo o documento..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value)
                setCurrentPage(1)
              }}
            />
          </div>

          <select
            className="admin-role-select"
            value={selectedRole}
            onChange={(e) => {
              setSelectedRole(e.target.value)
              setCurrentPage(1)
            }}
          >
            <option value="">Todos los roles</option>
            {roles.map((r) => (
              <option key={r.id} value={r.id}>
                {r.nombre}
              </option>
            ))}
          </select>
        </div>

        <UserTable
          usuarios={usuarios}
          cargando={cargando}
          pagination={pagination}
          onPageChange={(nuevaPagina) => setCurrentPage(nuevaPagina)}
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
