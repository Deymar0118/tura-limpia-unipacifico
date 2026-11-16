# Seguridad y autorización – Tura Limpia

## 1. Objetivo

Documentar los mecanismos de autenticación, autorización y protección de cuentas implementados en Tura Limpia, especialmente los relacionados con la gestión de usuarios y las cuentas administrativas.

## 2. Autenticación

El sistema utiliza autenticación mediante tokens JWT.

El proceso general es:

1. El usuario ingresa sus credenciales en el formulario de inicio de sesión.
2. El frontend envía la solicitud al backend.
3. El backend valida las credenciales.
4. Si la autenticación es correcta, se obtiene un token de acceso.
5. El frontend utiliza el token para realizar solicitudes a los endpoints protegidos.
6. El backend valida la identidad y los permisos antes de ejecutar las operaciones.

La autenticación permite identificar al usuario que realiza una solicitud, mientras que la autorización determina qué operaciones puede ejecutar.

## 3. Autorización en el backend

Las operaciones administrativas están protegidas mediante dependencias de autorización.

En el módulo de administración se utiliza `requiere_admin_db` para restringir el acceso a usuarios con permisos administrativos.

Además, se actualizó la validación de roles para consultar el rol vigente del usuario en la base de datos, evitando depender exclusivamente de la información del rol que pudiera estar almacenada en un JWT anterior.

Esto es importante cuando un usuario cambia de rol o su cuenta es desactivada: las autorizaciones deben reflejar el estado actual registrado en la base de datos.

## 4. Protección de la interfaz

El frontend utiliza rutas protegidas para controlar la navegación.

En `frontend/src/App.jsx` se implementó `AdminRoute`, que verifica la sesión y el rol del usuario antes de permitir el acceso al módulo administrativo.

El comportamiento es:

- Sin sesión válida: redirección al inicio de sesión.
- Usuario administrador: acceso al módulo de administración.
- Usuario con otro rol: redirección a la página de construcción.

Este mecanismo mejora la experiencia de navegación, pero no reemplaza la autorización del backend. La API mantiene la responsabilidad de validar los permisos de cada operación.

## 5. Protección del superadministrador

### 5.1. Identificación

Se designó como superadministrador a la cuenta denominada **Administrador Principal**.

Datos de identificación utilizados durante su configuración:

- Nombre de usuario: `admin`.
- Correo: `admin@turalimpia.com`.
- Rol: administrador.
- Campo de identificación: `es_superadministrador = true`.

La cuenta se mantiene como administrador y se distingue mediante un atributo adicional en la tabla `usuarios`.

### 5.2. Restricciones implementadas

Se incorporaron validaciones en la capa de servicios para impedir las siguientes operaciones sobre el superadministrador:

- Desactivar su cuenta.
- Cambiar su rol.

Estas restricciones se aplican desde los servicios de administración, antes de ejecutar los cambios correspondientes.

La cuenta puede conservar sus datos personales, pero las operaciones protegidas no deben permitir que pierda su condición de superadministrador ni sus capacidades administrativas.

### 5.3. Unicidad

La base de datos cuenta con el índice único parcial:

`uq_usuarios_superadministrador`

Este índice impide que más de un registro tenga `es_superadministrador = true`.

## 6. Protección del último administrador activo

Se incorporó una validación para impedir que el sistema pierda su último administrador activo.

Antes de realizar operaciones que puedan afectar la disponibilidad de una cuenta administrativa, el servicio consulta los administradores activos y verifica si la operación dejaría al sistema sin ningún administrador.

Las operaciones contempladas incluyen:

- Desactivar un administrador.
- Cambiar el rol de un administrador a uno que no tenga privilegios administrativos.

Si la operación afectaría al último administrador activo, el backend debe rechazarla.

Para apoyar estas validaciones, el repositorio incorpora consultas que permiten:

- Obtener y bloquear el usuario que se va a actualizar.
- Consultar y bloquear los administradores activos.
- Contar los administradores activos.

Se utilizan bloqueos de filas mediante SQLAlchemy para reducir conflictos durante las operaciones de actualización.

**Nota:** la protección frente a solicitudes concurrentes requiere pruebas específicas en PostgreSQL. Los bloqueos implementados no deben considerarse una garantía absoluta de serialización hasta validar los escenarios concurrentes y, si es necesario, reforzar el mecanismo de bloqueo.

## 7. Validaciones en la capa de servicios

La lógica de protección se concentra en:

`backend/src/services/administracion_service.py`

Entre las funciones auxiliares incorporadas se encuentran:

- `_es_superadministrador`: identifica si un usuario tiene la condición de superadministrador.
- `_obtener_perfiles_activos`: obtiene los perfiles activos de un usuario.
- `_es_administrador_activo`: determina si el usuario cuenta actualmente con un perfil administrador activo.
- `_proteger_ultimo_administrador`: valida que una operación no deje al sistema sin administradores activos.

También se utilizan operaciones del repositorio para obtener y bloquear los registros involucrados en las actualizaciones.

## 8. Consideraciones sobre eliminación y privilegios

En el router de administración revisado durante esta implementación no se encontró un endpoint de eliminación de usuarios.

Por lo tanto, no se considera implementada una protección de eliminación del superadministrador a través de un endpoint de borrado.

Si en el futuro se incorpora esa funcionalidad, deberá incluir validaciones específicas para impedir la eliminación del superadministrador y evitar que el sistema quede sin administradores activos.

De igual manera, cualquier funcionalidad futura que permita modificar privilegios o transferir la condición de superadministrador deberá aplicar controles equivalentes desde el backend y respetar la restricción de unicidad de la base de datos.

## 9. Validaciones realizadas

Durante la implementación se realizaron las siguientes comprobaciones:

- Compilación del servicio de administración mediante `python -m compileall`.
- Compilación del repositorio de administración.
- Inicio del servidor FastAPI sin errores de arranque.
- Ejecución de la migración de Alembic.
- Configuración de la cuenta Administrador Principal como superadministrador.

Estas comprobaciones verifican la sintaxis, el arranque y la aplicación de la migración, pero no sustituyen las pruebas funcionales de todos los escenarios de autorización.

## 10. Pruebas pendientes

Antes de considerar completa la validación de seguridad, deben probarse los siguientes escenarios:

1. Intentar desactivar al superadministrador.
2. Intentar cambiar el rol del superadministrador.
3. Intentar desactivar al último administrador activo.
4. Intentar quitar el rol administrador al último administrador activo.
5. Verificar que otro administrador pueda gestionar usuarios ordinarios.
6. Verificar que un usuario sin permisos administrativos reciba una respuesta de acceso denegado.
7. Verificar el comportamiento ante solicitudes concurrentes que intenten modificar administradores.
8. Comprobar que los cambios de rol y estado se reflejen inmediatamente en las autorizaciones del backend.

## 11. Principio de seguridad

Las reglas de seguridad deben aplicarse en el backend y mantenerse consistentes con las restricciones de la base de datos.

El frontend puede ocultar o restringir opciones de navegación, pero ninguna operación sensible debe depender únicamente de controles visuales o validaciones del cliente.