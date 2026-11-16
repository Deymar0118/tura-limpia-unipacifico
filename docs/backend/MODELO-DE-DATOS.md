# Modelo de datos – Tura Limpia

## 1. Descripción general

Tura Limpia utiliza PostgreSQL como sistema de gestión de bases de datos y SQLAlchemy como ORM para representar las entidades y administrar las operaciones de persistencia.

El modelo de datos está diseñado para organizar la información relacionada con los usuarios, sus perfiles, los roles, los trabajadores, las cuadrillas, los vehículos y la planificación y ejecución de las rutas de recolección de residuos sólidos.

## 2. Organización de las entidades

Las entidades del sistema se agrupan de acuerdo con su responsabilidad funcional.

### 2.1. Usuarios y control de acceso

| Entidad | Responsabilidad |
|---|---|
| `Rol` | Define los roles disponibles en el sistema. |
| `Perfil` | Relaciona a un usuario con un rol y conserva información del periodo de asignación. |
| `Usuario` | Almacena las credenciales y los datos generales de acceso. |
| `UsuarioPerfil` | Representa la relación entre usuarios y perfiles, según la estructura de asociación definida en el modelo. |

Los roles identificados para el sistema son ciudadano, trabajador, gerente y administrador.

La separación entre usuario y perfil permite que una misma cuenta tenga un historial de asignaciones de roles.

### 2.2. Personal operativo

| Entidad | Responsabilidad |
|---|---|
| `Trabajador` | Almacena información correspondiente al personal operativo. |
| `Conductor` | Representa la información específica de los conductores. |
| `Cuadrilla` | Agrupa al personal que participa en las actividades de recolección. |
| `TrabajadorCuadrilla` | Relaciona trabajadores con cuadrillas. |

Esta organización permite representar tanto la información individual del personal como su participación en los equipos de trabajo.

### 2.3. Organización territorial y rutas

| Entidad | Responsabilidad |
|---|---|
| `Barrio` | Representa los barrios del distrito. |
| `Macroruta` | Agrupa sectores o recorridos de mayor cobertura. |
| `Microruta` | Representa recorridos específicos dentro de la organización territorial. |
| `ParadaRuta` | Define puntos de parada asociados a los recorridos. |

Estas entidades permiten organizar territorialmente la prestación del servicio de recolección.

### 2.4. Vehículos y programación

| Entidad | Responsabilidad |
|---|---|
| `Vehiculo` | Almacena información de los vehículos utilizados en la operación. |
| `DiaSemana` | Define los días de la semana utilizados en la programación. |
| `Turno` | Representa los turnos de trabajo. |
| `ProgramacionRuta` | Organiza la programación de las rutas. |
| `Asignacion` | Representa las asignaciones operativas correspondientes. |

### 2.5. Ejecución y seguimiento

| Entidad | Responsabilidad |
|---|---|
| `EjecucionRuta` | Registra la ejecución de una ruta programada. |
| `CuadrillaEjecucion` | Relaciona las cuadrillas con una ejecución de ruta. |
| `EjecucionParada` | Registra información de las paradas realizadas. |
| `UbicacionGPS` | Almacena registros de ubicación para el seguimiento. |
| `Novedad` | Registra situaciones o eventos presentados durante la operación. |

## 3. Relación entre usuario, perfil y rol

La gestión de identidad se organiza mediante tres conceptos principales:

- **Usuario:** representa la cuenta de una persona dentro del sistema.
- **Perfil:** representa la asignación de un rol a un usuario durante un periodo.
- **Rol:** determina el tipo de acceso y las responsabilidades asociadas al perfil.

El usuario puede tener varios perfiles históricos. Cada cambio de rol debe conservar la asignación anterior y registrar una nueva.

Los perfiles utilizan información temporal, como la fecha de inicio y la fecha de finalización, además de su estado.

Este enfoque permite consultar los roles que ha tenido una persona sin perder el historial de sus asignaciones.

## 4. Incorporación del superadministrador

Como parte de las mejoras de seguridad, se incorporó el campo `es_superadministrador` a la entidad `Usuario`.

### 4.1. Nuevo atributo

| Campo | Tipo | Valor predeterminado | Descripción |
|---|---|---|---|
| `es_superadministrador` | Boolean | `false` | Identifica si la cuenta corresponde al superadministrador del sistema. |

La cuenta designada como superadministrador es **Administrador Principal**, correspondiente al usuario `admin` y al correo `admin@turalimpia.com`.

Esta cuenta conserva su rol de administrador, pero cuenta con una distinción adicional que permite aplicar reglas especiales de protección.

### 4.2. Restricción de unicidad

Se incorporó el índice único parcial:

`uq_usuarios_superadministrador`

Este índice se aplica a los registros cuyo campo `es_superadministrador` tiene el valor `true`.

Su finalidad es impedir que existan dos usuarios marcados simultáneamente como superadministradores.

## 5. Migración de la base de datos

La incorporación del superadministrador se realizó mediante una migración de Alembic.

Archivo:

`backend/alembic/versions/2fa5b594e1b7_agregar_superadministrador.py`

La migración realiza las siguientes operaciones:

1. Agrega la columna `es_superadministrador` a la tabla `usuarios`.
2. Establece `false` como valor predeterminado.
3. Crea el índice único parcial para garantizar que solo exista un superadministrador.
4. Define las operaciones inversas para permitir revertir la migración.

La migración fue ejecutada correctamente mediante:

```powershell
alembic upgrade head
```

## 6. Consideraciones para la evolución del modelo

El modelo de datos debe conservar la separación entre cuentas, perfiles y roles para mantener un historial consistente de los permisos asignados.

Cualquier funcionalidad futura de eliminación de usuarios, administración de privilegios o transferencia de la condición de superadministrador deberá respetar las restricciones de integridad y las reglas de seguridad del sistema.

Los detalles de autorización y protección de las cuentas administrativas se encuentran en `SEGURIDAD-Y-AUTORIZACION.md`.