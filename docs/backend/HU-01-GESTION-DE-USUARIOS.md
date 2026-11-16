# HU-01 – Gestión de usuarios

## 1. Descripción general

La HU-01 implementa el módulo de gestión de usuarios del sistema Tura Limpia. Su objetivo es permitir que los usuarios con permisos de administrador puedan registrar, consultar, actualizar y gestionar los perfiles y roles de los usuarios del sistema.

La funcionalidad integra el frontend desarrollado en React con el backend desarrollado en FastAPI y la base de datos PostgreSQL.

## 2. Funcionalidades implementadas

### 2.1. Registro de usuarios

Se implementó el registro de usuarios desde el módulo de administración.

El formulario permite ingresar:

- Nombres.
- Apellidos.
- Nombre de usuario.
- Correo electrónico.
- Contraseña.
- Documento.
- Rol inicial.
- Fecha de inicio del perfil.
- Cargo, cuando corresponda.

El registro se realiza mediante:

`POST /administracion/usuarios`

El backend valida la información recibida y crea el usuario junto con su perfil inicial.

### 2.2. Consulta y listado de usuarios

Se implementó una vista de administración que permite consultar los usuarios registrados.

Endpoint:

`GET /administracion/usuarios`

Parámetros de paginación:

- `pagina`: número de página.
- `por_pagina`: cantidad de registros por página.

La respuesta incluye los usuarios y los datos de paginación, como el total de registros y el total de páginas.

En el frontend se implementó la presentación de la información y el filtrado local de los registros cargados para facilitar su consulta.

### 2.3. Consulta individual

Se implementó la consulta de un usuario específico mediante:

`GET /administracion/usuarios/{id_usuario}`

Esta operación permite recuperar la información del usuario y sus perfiles asociados.

### 2.4. Actualización de usuarios

Se implementó la actualización de los datos personales del usuario mediante:

`PUT /administracion/usuarios/{id_usuario}`

Permite actualizar los campos contemplados por el esquema de administración, entre ellos:

- Nombres y apellidos.
- Nombre de usuario.
- Correo electrónico.
- Teléfono.
- Documento.
- Barrio.
- Estado de la cuenta.

El estado de la cuenta se maneja mediante los valores `activo` e `inactivo`.

### 2.5. Gestión de perfiles y roles

Se implementó la asignación de perfiles a los usuarios mediante:

`POST /administracion/usuarios/{id_usuario}/perfiles`

La operación permite asignar un rol y registrar la fecha de inicio del nuevo perfil, además del cargo cuando corresponda.

El cambio de rol se maneja mediante la creación de un nuevo perfil, conservando el historial de perfiles del usuario en lugar de reemplazar directamente el registro anterior.

Los roles utilizados en el sistema son:

- Ciudadano.
- Trabajador.
- Gerente.
- Administrador.

Los identificadores actuales de estos roles son:

| Rol | ID |
|---|---:|
| Ciudadano | 5 |
| Trabajador | 6 |
| Gerente | 7 |
| Administrador | 8 |

### 2.6. Activación y desactivación

Se integró la gestión del estado de las cuentas desde la tabla de usuarios.

La operación utiliza el endpoint de actualización y permite activar o desactivar una cuenta según las reglas de seguridad implementadas en el backend.

## 3. Integración frontend y backend

El módulo frontend se encuentra organizado dentro de:

`frontend/src/modules/admin/`

Componentes y archivos principales:

- `pages/UsersManagementPage.jsx`: página principal de administración de usuarios.
- `components/UserFormModal.jsx`: formulario de creación y edición.
- `components/UserTable.css`: estilos de la tabla.
- `services/usuarioService.js`: comunicación con los endpoints de administración.

El servicio de usuarios adapta las respuestas del backend al formato utilizado por los componentes de React. También normaliza los perfiles y roles para identificar el perfil vigente del usuario.

## 4. Control de acceso

Las operaciones de administración están protegidas en el backend mediante dependencias de autorización.

El frontend también controla el acceso a las rutas administrativas. Los usuarios con rol administrador pueden acceder al módulo de gestión; los demás perfiles son dirigidos a la página de construcción mientras se implementan sus respectivos módulos.

La protección del frontend es complementaria. La autorización real de las operaciones se valida en el backend.

## 5. Criterios de seguridad

La gestión de usuarios incorpora las siguientes consideraciones:

- Validación de los datos recibidos por el backend.
- Restricción de las operaciones administrativas a usuarios autorizados.
- Validación de los estados de las cuentas.
- Conservación del historial de perfiles al cambiar de rol.
- Protección del último administrador activo.
- Protección especial de la cuenta designada como superadministrador.

Los detalles de estas últimas protecciones se documentan en `SEGURIDAD-Y-AUTORIZACION.md`.

## 6. Estado de implementación

La integración del módulo de gestión de usuarios con el backend se encuentra implementada.

Se realizaron pruebas de funcionamiento de la interfaz, autenticación, navegación y arranque del backend. Las pruebas específicas de todos los escenarios de seguridad, concurrencia y autorización deben mantenerse como parte de la validación pendiente antes de considerar el módulo listo para producción.