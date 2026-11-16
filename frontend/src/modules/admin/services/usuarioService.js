
import { apiClient } from '../../../shared/api/apiClient'

// --------------------------------------------------
// Adaptadores: backend FastAPI -> formato del frontend
// --------------------------------------------------

function normalizarRol(rol) {
  if (!rol) return null

  return {
    ...rol,
    id: rol.id_rol ?? rol.id,
    nombre: rol.nombre_rol ?? rol.nombre,
  }
}

function normalizarPerfil(perfil) {
  if (!perfil) return null

  return {
    ...perfil,
    id: perfil.id_perfil ?? perfil.id,
    documento: perfil.documento ?? null,
    fecha_inicio: perfil.fecha_inicio,
    estado: perfil.estado,
    rol: normalizarRol(perfil.rol),
  }
}

// Identificar si un perfil está activo
function perfilEstaActivo(perfil) {
  return (
    perfil.estado === true ||
    perfil.estado === 1 ||
    perfil.estado === 'activo' ||
    perfil.estado === 'true'
  )
}

// Seleccionar el perfil más reciente
function seleccionarPerfilVigente(perfiles) {
  if (!perfiles.length) return null

  const perfilesActivos = perfiles.filter(perfilEstaActivo)

  const candidatos = perfilesActivos.length
    ? perfilesActivos
    : perfiles

  return [...candidatos].sort((a, b) => {
    const fechaA = new Date(a.fecha_inicio || 0).getTime()
    const fechaB = new Date(b.fecha_inicio || 0).getTime()

    return fechaB - fechaA
  })[0]
}

function normalizarUsuario(usuario) {
  if (!usuario) return null

  const perfilesOriginales = Array.isArray(usuario.perfiles)
    ? usuario.perfiles
    : usuario.perfil
      ? [usuario.perfil]
      : []

  const perfiles = perfilesOriginales.map(normalizarPerfil)

  const perfilActual = seleccionarPerfilVigente(perfiles)

  const activo =
    typeof usuario.activo === 'boolean'
      ? usuario.activo
      : usuario.estado === 'activo'

  return {
    ...usuario,
    id: usuario.id_usuario ?? usuario.id,
    activo,
    estado: usuario.estado ?? (activo ? 'activo' : 'inactivo'),
    perfil: perfilActual,
    perfiles,
  }
}

function normalizarPaginacion(paginacion = {}) {
  return {
    page: paginacion.pagina ?? 1,
    limit: paginacion.por_pagina ?? 10,
    total: paginacion.total_registros ?? 0,
    total_pages: paginacion.total_paginas ?? 0,
  }
}

// --------------------------------------------------
// Usuarios
// --------------------------------------------------

export async function obtenerUsuarios({
  page = 1,
  limit = 10,
} = {}) {
  const respuesta = await apiClient('/administracion/usuarios', {
    query: {
      pagina: page,
      por_pagina: limit,
    },
  })

  return {
    success: respuesta.success ?? true,
    data: (respuesta.data || []).map(normalizarUsuario),
    pagination: normalizarPaginacion(respuesta.paginacion),
  }
}

// --------------------------------------------------
// Roles
// --------------------------------------------------

export async function obtenerRoles() {
  const respuesta = await apiClient('/administracion/roles', {
    query: {
      solo_activos: true,
    },
  })

  const roles = Array.isArray(respuesta)
    ? respuesta
    : respuesta.data || []

  return roles.map(normalizarRol)
}

// --------------------------------------------------
// Crear usuario
// --------------------------------------------------

export async function registrarUsuarioAdmin(datos) {
  const respuesta = await apiClient('/administracion/usuarios', {
    metodo: 'POST',
    body: datos,
  })

  return {
    ...respuesta,
    data: normalizarUsuario(respuesta.data),
  }
}

// --------------------------------------------------
// Actualizar información del usuario
// --------------------------------------------------

export async function actualizarUsuario(id, datos) {
  const payload = {}

  const camposPermitidos = [
    'nombres',
    'apellidos',
    'nombre_usuario',
    'correo',
    'telefono',
    'documento',
    'id_barrio',
  ]

  camposPermitidos.forEach((campo) => {
    if (datos[campo] !== undefined) {
      payload[campo] = datos[campo]
    }
  })

  if (datos.estado !== undefined) {
    payload.estado = datos.estado
  } else if (typeof datos.activo === 'boolean') {
    payload.estado = datos.activo ? 'activo' : 'inactivo'
  }

  const respuesta = await apiClient(
    `/administracion/usuarios/${id}`,
    {
      metodo: 'PUT',
      body: payload,
    },
  )

  return normalizarUsuario(respuesta)
}

// --------------------------------------------------
// Asignar un nuevo perfil o cambiar el rol
// --------------------------------------------------

export async function asignarPerfilUsuario(id, datos) {
  const payload = {
    id_rol: Number(datos.id_rol ?? datos.rol_id),
    fecha_inicio: datos.fecha_inicio,
  }

  if (datos.cargo?.trim()) {
    payload.cargo = datos.cargo.trim()
  }

  const respuesta = await apiClient(
    `/administracion/usuarios/${id}/perfiles`,
    {
      metodo: 'POST',
      body: payload,
    },
  )

  return normalizarUsuario(respuesta)
}

// --------------------------------------------------
// Activar / desactivar usuario
// --------------------------------------------------

export async function toggleEstadoUsuario(id, estadoActual) {
  return actualizarUsuario(id, {
    estado: estadoActual ? 'inactivo' : 'activo',
  })
}
