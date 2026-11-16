import './UserTable.css'

export default function UserTable({
  usuarios,
  cargando,
  pagination,
  onPageChange,
  onToggleStatus,
  onEditUser
}) {
  const getRoleBadgeClass = (rolNombre) => {
    const rol = (rolNombre || '').toLowerCase()
    if (rol.includes('admin')) return 'badge-role--admin'
    if (rol.includes('operat') || rol.includes('trabajador')) return 'badge-role--operativo'
    return 'badge-role--default'
  }

  return (
    <div className="table-responsive-wrapper">
      <table className="user-table">
        <thead>
          <tr>
            <th>Funcionario</th>
            <th>Contacto</th>
            <th>Documento</th>
            <th>Rol Asignado</th>
            <th>Estado Cuenta</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {cargando ? (
            <tr>
              <td colSpan="6" style={{ textAlign: 'center', padding: '36px' }}>
                Cargando funcionarios...
              </td>
            </tr>
          ) : usuarios.length === 0 ? (
            <tr>
              <td colSpan="6">
                <div className="table-empty-state">
                  <div className="table-empty-title">No se encontraron usuarios</div>
                  <p>Intenta cambiar los términos de búsqueda o filtros.</p>
                </div>
              </td>
            </tr>
          ) : (
            usuarios.map((usuario) => {
              const rolNombre = usuario.perfil?.rol?.nombre || 'Sin Rol'
              const doc = usuario.perfil?.documento || 'No registrado'
              const esActivo = usuario.activo

              return (
                <tr key={usuario.id}>
                  <td>
                    <div className="user-cell-name">
                      <span className="user-full-name">
                        {usuario.nombres} {usuario.apellidos}
                      </span>
                      <span className="user-username">@{usuario.nombre_usuario}</span>
                    </div>
                  </td>
                  <td>
                    <div className="user-cell-contact">
                      <span className="user-email">{usuario.correo}</span>
                      {usuario.telefono && (
                        <span className="user-phone">{usuario.telefono}</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <span style={{ fontWeight: 600, color: '#334155' }}>{doc}</span>
                  </td>
                  <td>
                    <span className={`badge-role ${getRoleBadgeClass(rolNombre)}`}>
                      {rolNombre}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`badge-status ${
                        esActivo ? 'badge-status--active' : 'badge-status--inactive'
                      }`}
                    >
                      <span className="badge-status-dot" />
                      {esActivo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td>
                    <div className="table-actions-cell">
                      <button
                        type="button"
                        className="btn-edit-user"
                        onClick={() => onEditUser?.(usuario)}
                        title="Modificar datos o cambiar rol del usuario"
                      >
                        Editar
                      </button>
                      <button
                        type="button"
                        className="btn-toggle-status"
                        onClick={() => onToggleStatus(usuario.id, esActivo)}
                        title={esActivo ? 'Desactivar acceso' : 'Activar acceso'}
                      >
                        {esActivo ? 'Desactivar' : 'Activar'}
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>

      {pagination && pagination.total > 0 && (
        <div className="pagination-wrapper">
          <span>
            Página {pagination.page} de {pagination.total_pages} ({pagination.total} usuarios en total)
          </span>
          <div className="pagination-controls">
            <button
              type="button"
              className="pagination-btn"
              disabled={pagination.page <= 1}
              onClick={() => onPageChange(pagination.page - 1)}
            >
              Anterior
            </button>
            <button
              type="button"
              className="pagination-btn"
              disabled={pagination.page >= pagination.total_pages}
              onClick={() => onPageChange(pagination.page + 1)}
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
