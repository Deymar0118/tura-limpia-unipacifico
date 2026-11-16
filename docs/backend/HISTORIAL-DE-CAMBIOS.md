# Historial de cambios – Tura Limpia

## 1. Objetivo

Registrar los principales cambios realizados en el proyecto Tura Limpia, desde la implementación de la HU-01 (Gestión de usuarios) hasta la incorporación del superadministrador y las reglas de protección de las cuentas administrativas.

## 2. HU-01 – Gestión de usuarios

Se desarrolló la integración del módulo de administración de usuarios entre el frontend y el backend.

### Cambios realizados

- Integración del formulario de creación de usuarios con la API.
- Integración del listado de usuarios con paginación.
- Implementación de la consulta individual de usuarios.
- Integración de la actualización de datos personales.
- Implementación de la asignación de perfiles y roles.
- Adaptación de las respuestas del backend al formato utilizado por React.
- Normalización de los perfiles para identificar el perfil vigente.
- Integración de la activación y desactivación de cuentas.

### Endpoints integrados

| Método | Endpoint | Funcionalidad |
|---|---|---|
| GET | `/administracion/` | Acceso al módulo administrativo. |
| GET | `/administracion/roles` | Consulta de roles. |
| POST | `/administracion/usuarios` | Registro de usuarios. |
| GET | `/administracion/usuarios` | Listado de usuarios. |
| GET | `/administracion/usuarios/{id_usuario}` | Consulta individual. |
| PUT | `/administracion/usuarios/{id_usuario}` | Actualización de usuarios. |
| POST | `/administracion/usuarios/{id_usuario}/perfiles` | Asignación de perfiles. |

## 3. Integración de autenticación y navegación

Se realizaron ajustes en el frontend para conectar el inicio de sesión con la información devuelta por el backend.

### Cambios realizados

- Integración del servicio de autenticación.
- Obtención y almacenamiento local de la sesión del usuario.
- Redirección según el rol después del inicio de sesión.
- Implementación de rutas protegidas mediante `AdminRoute`.
- Restricción de acceso al panel administrativo para usuarios que no tengan rol administrador.
- Incorporación de la página provisional de construcción para los módulos que todavía no están disponibles.

### Archivos principales

- `frontend/src/App.jsx`
- `frontend/src/modules/auth/pages/AuthPage.jsx`
- `frontend/src/modules/construction/pages/ConstructionPage.jsx`

## 4. Mejoras en la interfaz de administración

Se realizaron ajustes en la presentación y funcionamiento del módulo administrativo.

### Cambios realizados

- Adaptación de la tabla de usuarios a la información recibida desde la API.
- Ajustes en el formulario de creación y edición.
- Integración de la consulta de roles disponibles.
- Manejo de errores y notificaciones de las operaciones.
- Ajustes de visualización de la tabla para mantener accesibles las acciones de edición y activación o desactivación.

### Archivos principales

- `frontend/src/modules/admin/pages/UsersManagementPage.jsx`
- `frontend/src/modules/admin/components/UserFormModal.jsx`
- `frontend/src/modules/admin/components/UserTable.css`
- `frontend/src/modules/admin/services/usuarioService.js`

## 5. Protección del superadministrador

Se identificó la necesidad de proteger la cuenta principal del sistema para evitar que las operaciones administrativas pudieran dejar a Tura Limpia sin una cuenta de control.

Se designó como superadministrador a la cuenta **Administrador Principal**.

### Cambios realizados en el modelo

Se incorporó el atributo:

`es_superadministrador`

Este campo permite diferenciar la cuenta principal de los demás usuarios administradores.

También se agregó el índice único parcial:

`uq_usuarios_superadministrador`

Su finalidad es impedir que existan múltiples cuentas identificadas como superadministrador.

### Migración

Se creó la migración:

`2fa5b594e1b7_agregar_superadministrador.py`

La migración agrega el nuevo campo a la tabla `usuarios` y establece la restricción de unicidad.

La migración fue aplicada correctamente mediante Alembic.

## 6. Protección de las cuentas administrativas

Se modificaron los servicios y repositorios de administración para incorporar validaciones adicionales.

### Cambios en el servicio

Archivo:

`backend/src/services/administracion_service.py`

Se incorporaron validaciones para:

- Identificar al superadministrador.
- Obtener los perfiles activos de un usuario.
- Determinar si un usuario es administrador activo.
- Impedir la desactivación del superadministrador.
- Impedir el cambio de rol del superadministrador.
- Evitar que una operación deje al sistema sin administradores activos.

### Cambios en el repositorio

Archivo:

`backend/src/repository/administracion_repository.py`

Se incorporaron operaciones para:

- Obtener el usuario antes de actualizarlo utilizando bloqueo de fila.
- Consultar y bloquear los administradores activos.
- Contar los administradores activos.

Estas operaciones sirven de apoyo a las validaciones de seguridad realizadas por los servicios.

## 7. Validaciones técnicas realizadas

Durante el desarrollo se realizaron las siguientes comprobaciones:

- Compilación de los archivos modificados del servicio y repositorio.
- Aplicación de la migración de Alembic.
- Configuración de la cuenta Administrador Principal como superadministrador.
- Inicio del servidor FastAPI sin errores de arranque.
- Verificación del funcionamiento de la autenticación y navegación del frontend durante la integración.

Estas comprobaciones no equivalen a una suite completa de pruebas automatizadas.

## 8. Estado y trabajo pendiente

Al cierre de estos cambios, las siguientes actividades quedan identificadas para validación o desarrollo posterior:

- Pruebas funcionales específicas de las restricciones del superadministrador.
- Pruebas de protección del último administrador activo.
- Pruebas de solicitudes concurrentes sobre cuentas administrativas.
- Validación de permisos para cada rol del sistema.
- Implementación de protecciones específicas si en el futuro se agrega eliminación de usuarios.
- Continuación de los módulos funcionales correspondientes a los demás roles.

## 9. Resumen

Los cambios realizados permitieron avanzar desde una interfaz de administración conectada al backend hasta un módulo de gestión de usuarios con control de acceso y protecciones para las cuentas administrativas.

La incorporación del superadministrador y de las validaciones del último administrador activo fortalece la continuidad de la administración del sistema y establece una base para seguir desarrollando los demás módulos de Tura Limpia.