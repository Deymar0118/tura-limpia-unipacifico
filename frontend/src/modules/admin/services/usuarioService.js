import { apiClient } from '../../../shared/api/apiClient'

// datos de prueba
let usuariosMock = [
  {
    id: 1,
    nombres: 'Deymar Andres',
    apellidos: 'Ampudia Rivas',
    nombre_usuario: 'dampudia',
    correo: 'deymar.ampudia@turalimpia.com',
    telefono: '3157894561',
    activo: true,
    perfil: {
      id: 101,
      documento: '1114859632',
      fecha_inicio: '2026-02-01',
      estado: true,
      rol: { id: 1, nombre: 'Administrador' }
    }
  },
  {
    id: 2,
    nombres: 'Santiago Andres',
    apellidos: 'Guarnizo Patiño',
    nombre_usuario: 'spatiño',
    correo: 'saltiago.patiño@turalimpia.com',
    telefono: '3184561234',
    activo: true,
    perfil: {
      id: 102,
      documento: '1115896321',
      fecha_inicio: '2026-02-15',
      estado: true,
      rol: { id: 2, nombre: 'Operativo' }
    }
  },
  {
    id: 3,
    nombres: 'Jhon Jairo',
    apellidos: 'Cuero Angulo',
    nombre_usuario: 'jcuero',
    correo: 'jhon.cuero@turalimpia.com',
    telefono: '3129876543',
    activo: false,
    perfil: {
      id: 103,
      documento: '1116741258',
      fecha_inicio: '2026-03-01',
      estado: false,
      rol: { id: 2, nombre: 'Operativo' }
    }
  }
]

const rolesMock = [
  { id: 1, nombre: 'Administrador', descripcion: 'Acceso total y configuración del sistema' },
  { id: 2, nombre: 'Operativo', descripcion: 'Coordinación y despacho de rutas y flota' },
  { id: 3, nombre: 'Consulta', descripcion: 'Visualización general de tableros e informes' }
]

/**
 * consulta de usuarios
 */
export async function obtenerUsuarios({ page = 1, limit = 10, q = '', rol_id = '' } = {}) {
  try {
    const query = { page, limit }
    if (q) query.q = q
    if (rol_id) query.rol_id = rol_id

    const respuesta = await apiClient('/administracion/usuarios', {
      metodo: 'GET',
      query
    })
    return respuesta
  } catch {
    let filtrados = [...usuariosMock]
    if (q) {
      const term = q.toLowerCase()
      filtrados = filtrados.filter(
        (u) =>
          u.nombres.toLowerCase().includes(term) ||
          u.apellidos.toLowerCase().includes(term) ||
          u.correo.toLowerCase().includes(term) ||
          u.nombre_usuario.toLowerCase().includes(term) ||
          u.perfil.documento.includes(term)
      )
    }
    if (rol_id) {
      filtrados = filtrados.filter((u) => u.perfil.rol.id === Number(rol_id))
    }

    return {
      success: true,
      message: 'Usuarios consultados correctamente (Modo simulación)',
      data: filtrados,
      pagination: {
        page: Number(page),
        limit: Number(limit),
        total: filtrados.length,
        total_pages: Math.ceil(filtrados.length / limit) || 1
      }
    }
  }
}

export async function obtenerRoles() {
  try {
    const respuesta = await apiClient('/administracion/roles', { metodo: 'GET' })
    return respuesta.data || respuesta
  } catch {
    return rolesMock
  }
}

/**
 * Registra un nuevo usuario
 */
export async function registrarUsuarioAdmin(datos) {
  try {
    const respuesta = await apiClient('/administracion/usuarios', {
      metodo: 'POST',
      body: datos
    })
    return respuesta
  } catch (error) {
    if (error?.status === 0 || !error?.status) {
      const rolEncontrado = rolesMock.find((r) => r.id === Number(datos.perfil.rol_id)) || {
        id: datos.perfil.rol_id,
        nombre: 'Operativo'
      }

      const nuevoUsuario = {
        id: usuariosMock.length + 1,
        nombres: datos.nombres,
        apellidos: datos.apellidos,
        nombre_usuario: datos.nombre_usuario,
        correo: datos.correo,
        telefono: datos.telefono || '',
        activo: true,
        perfil: {
          id: 100 + usuariosMock.length + 1,
          documento: datos.perfil.documento,
          fecha_inicio: datos.perfil.fecha_inicio,
          estado: datos.perfil.estado !== undefined ? datos.perfil.estado : true,
          rol: rolEncontrado
        }
      }
      usuariosMock.unshift(nuevoUsuario)

      return {
        success: true,
        message: 'Usuario registrado correctamente (Modo simulación)',
        data: nuevoUsuario
      }
    }
    throw error
  }
}

/**
 * Actualiza los datos o el rol
 */
export async function actualizarUsuario(id, datos) {
  try {
    const respuesta = await apiClient(`/administracion/usuarios/${id}`, {
      metodo: 'PUT',
      body: datos
    })
    return respuesta
  } catch (error) {
    if (error?.status === 0 || !error?.status) {
      usuariosMock = usuariosMock.map((u) => {
        if (u.id === id) {
          const rolEncontrado =
            rolesMock.find((r) => r.id === Number(datos.perfil?.rol_id)) || u.perfil?.rol

          return {
            ...u,
            nombres: datos.nombres ?? u.nombres,
            apellidos: datos.apellidos ?? u.apellidos,
            nombre_usuario: datos.nombre_usuario ?? u.nombre_usuario,
            correo: datos.correo ?? u.correo,
            telefono: datos.telefono ?? u.telefono,
            activo: datos.activo !== undefined ? datos.activo : u.activo,
            perfil: {
              ...u.perfil,
              documento: datos.perfil?.documento ?? u.perfil?.documento,
              fecha_inicio: datos.perfil?.fecha_inicio ?? u.perfil?.fecha_inicio,
              estado: datos.perfil?.estado !== undefined ? datos.perfil.estado : u.perfil?.estado,
              rol: rolEncontrado
            }
          }
        }
        return u
      })

      const usuarioActualizado = usuariosMock.find((u) => u.id === id)
      return {
        success: true,
        message: 'Usuario y rol actualizados correctamente (Modo simulación)',
        data: usuarioActualizado
      }
    }
    throw error
  }
}

export async function toggleEstadoUsuario(id, estadoActual) {
  try {
    return await apiClient(`/administracion/usuarios/${id}`, {
      metodo: 'PUT',
      body: { activo: !estadoActual }
    })
  } catch {
    usuariosMock = usuariosMock.map((u) => (u.id === id ? { ...u, activo: !estadoActual } : u))
    return { success: true, message: 'Estado actualizado' }
  }
}
