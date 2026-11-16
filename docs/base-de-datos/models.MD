# Documentación técnica de modelos de datos – Tura Limpia

## 1. Objetivo

Documentar los modelos implementados en el backend de Tura Limpia mediante SQLAlchemy. Se describen las tablas representadas, sus atributos, claves primarias, claves foráneas, restricciones y relaciones ORM.

Esta documentación se basa en el código compartido. Los nombres y restricciones corresponden a lo declarado en esos modelos.

## 2. Tecnologías y convenciones

- **Python:** lenguaje de implementación.
- **SQLAlchemy ORM:** mapeo entre clases Python y tablas de PostgreSQL.
- **PostgreSQL:** motor de base de datos.
- **UUID:** identificador utilizado en varias entidades.
- **`Mapped` y `mapped_column`:** definición tipada de atributos y columnas.
- **`relationship`:** definición de relaciones ORM.
- **`ForeignKey`:** referencia entre tablas.

Convenciones:

- `PK`: clave primaria.
- `FK`: clave foránea.
- `nullable=False`: campo obligatorio.
- `nullable=True`: campo opcional.
- `unique=True`: valor único.
- `index=True`: columna indexada.
- `server_default`: valor predeterminado asignado por la base de datos.
- `ondelete`: comportamiento de la clave foránea al eliminar el registro referenciado.

## 3. Organización de archivos

```text
models/
├── __init__.py
├── ejecucion.py
├── novedad.py
├── personal.py
├── programacion.py
├── ruta.py
├── territorio.py
├── usuario.py
└── vehiculo.py
```

El archivo `__init__.py` importa y expone los modelos y la tabla de asociación para facilitar su importación desde otros módulos.

## 4. Descripción de los modelos

### 4.1. `usuario.py` – Usuarios, roles y perfiles

#### `Rol` — tabla `roles`

Representa los roles disponibles en el sistema.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_rol` | Integer | PK, índice | Identificador del rol. |
| `nombre_rol` | String(50) | Obligatorio, único | Nombre del rol. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del rol. |

**Relación:** un rol puede estar asociado a varios perfiles.

#### `Perfil` — tabla `perfiles`

Representa un perfil asociado a un rol.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_perfil` | UUID | PK, generado por defecto | Identificador del perfil. |
| `id_rol` | Integer | FK a `roles.id_rol`, obligatorio, índice | Rol asociado. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del perfil. |

**Relaciones:** pertenece a un `Rol` y puede asociarse con varios registros de `UsuarioPerfil`.

#### `UsuarioPerfil` — tabla `usuario_perfil`

Tabla intermedia que relaciona usuarios y perfiles, conservando la vigencia de la asociación.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_usuario` | UUID | PK compuesta, FK a `usuarios.id_usuario` | Usuario asociado. |
| `id_perfil` | UUID | PK compuesta, FK a `perfiles.id_perfil` | Perfil asociado. |
| `fecha_inicio` | Date | Obligatorio | Inicio de la asociación. |
| `fecha_fin` | Date | Opcional | Fin de la asociación. |

**Relaciones:** conecta `Usuario` con `Perfil`. La clave primaria está compuesta por ambos identificadores.

#### `Usuario` — tabla `usuarios`

Almacena la información de identificación, contacto y acceso de los usuarios.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_usuario` | UUID | PK, generado por defecto | Identificador del usuario. |
| `id_barrio` | Integer | FK a `barrios.id_barrio`, opcional, índice | Barrio asociado. |
| `nombres` | String(100) | Obligatorio | Nombres. |
| `apellidos` | String(100) | Obligatorio | Apellidos. |
| `nombre_completo` | String(200) | Opcional | Nombre completo. |
| `nombre_usuario` | String(50) | Obligatorio, único, índice | Nombre de usuario. |
| `correo` | String(100) | Obligatorio, único, índice | Correo electrónico. |
| `password_hash` | String(255) | Obligatorio | Hash de la contraseña. |
| `telefono` | String(20) | Opcional | Teléfono. |
| `documento` | String(30) | Opcional, único, índice | Número de documento. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado de la cuenta. |
| `fecha_registro` | DateTime con zona horaria | Obligatorio, default `now()` | Fecha y hora de registro. |

**Relaciones:**

- Puede estar asociado a un `Barrio`.
- Puede tener asociaciones con perfiles mediante `UsuarioPerfil`.
- Puede tener un perfil de `Trabajador`.
- Puede registrar varias `Novedad`.

### 4.2. `personal.py` – Personal y cuadrillas

#### `Trabajador` — tabla `trabajadores`

Representa a una persona registrada como trabajador.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_trabajador` | UUID | PK, generado por defecto | Identificador del trabajador. |
| `id_usuario` | UUID | FK a `usuarios.id_usuario`, obligatorio, único, índice | Cuenta asociada. |
| `cargo` | String(50) | Obligatorio | Cargo del trabajador. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del trabajador. |

**Relaciones:** pertenece a un `Usuario`, puede tener un registro `Conductor` y se vincula con cuadrillas mediante `TrabajadorCuadrilla`.

#### `Conductor` — tabla `conductores`

Almacena los datos específicos de licencia de los trabajadores que conducen vehículos.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_conductor` | UUID | PK, generado por defecto | Identificador del conductor. |
| `id_trabajador` | UUID | FK a `trabajadores.id_trabajador`, obligatorio, único, índice | Trabajador relacionado. |
| `categoria_licencia` | String(20) | Obligatorio | Categoría de la licencia. |
| `num_licencia` | String(50) | Obligatorio, único | Número de licencia. |
| `vencimiento_licencia` | Date | Obligatorio | Vencimiento de la licencia. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del conductor. |

**Relaciones:** pertenece a un `Trabajador` y puede estar relacionado con varias `ProgramacionRuta`.

#### `Cuadrilla` — tabla `cuadrillas`

Representa un grupo de personal operativo.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_cuadrilla` | UUID | PK, generado por defecto | Identificador de la cuadrilla. |
| `nombre_cuadrilla` | String(100) | Obligatorio | Nombre de la cuadrilla. |
| `num_integrantes` | Integer | Obligatorio, default `1` | Número de integrantes. |
| `tipo_cuadrilla` | String(50) | Obligatorio | Tipo de cuadrilla. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado de la cuadrilla. |

**Relaciones:** puede asociarse con varias programaciones y con trabajadores mediante `TrabajadorCuadrilla`.

#### `TrabajadorCuadrilla` — tabla `trabajador_cuadrilla`

Tabla intermedia que registra la vinculación de trabajadores a cuadrillas y su periodo de vigencia.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_trabajador` | UUID | PK compuesta, FK a `trabajadores.id_trabajador` | Trabajador asociado. |
| `id_cuadrilla` | UUID | PK compuesta, FK a `cuadrillas.id_cuadrilla` | Cuadrilla asociada. |
| `fecha_inicio` | Date | Obligatorio | Inicio de la vinculación. |
| `fecha_fin` | Date | Opcional | Fin de la vinculación. |

La clave primaria está compuesta por `id_trabajador` e `id_cuadrilla`.

### 4.3. `territorio.py` – División territorial

#### `Barrio` — tabla `barrios`

Representa los barrios registrados para organizar la cobertura territorial del servicio.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_barrio` | Integer | PK, índice | Identificador del barrio. |
| `nombre_barrio` | String(100) | Obligatorio, índice | Nombre del barrio. |
| `comuna` | String(50) | Opcional | Comuna. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del barrio. |

**Relaciones:** puede estar asociado a varios usuarios y a varias `ParadaRuta`.

### 4.4. `ruta.py` – Estructura de rutas

#### `Macroruta` — tabla `macrorutas`

Representa una ruta general que agrupa microrutas.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_macroruta` | Integer | PK, índice | Identificador de la macroruta. |
| `nombre_macroruta` | String(100) | Obligatorio | Nombre. |
| `descripcion` | Text | Opcional | Descripción. |
| `tipo_servicio` | String(50) | Obligatorio | Tipo de servicio. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado. |

**Relaciones:** contiene varias `Microruta` y puede tener varias `ProgramacionRuta`.

#### `Microruta` — tabla `microrutas`

Representa un recorrido específico perteneciente a una macroruta.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_microruta` | Integer | PK, índice | Identificador de la microruta. |
| `id_macroruta` | Integer | FK a `macrorutas.id_macroruta`, obligatorio, índice | Macroruta relacionada. |
| `nombre_microruta` | String(100) | Obligatorio | Nombre. |
| `trazado` | Text | Opcional | Trazado del recorrido. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado. |

**Relaciones:** pertenece a una `Macroruta` y contiene varias `ParadaRuta`.

#### `ParadaRuta` — tabla `paradas_ruta`

Define los puntos de parada de una microruta y el barrio correspondiente.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_parada` | Integer | PK, índice | Identificador de la parada. |
| `id_microruta` | Integer | FK a `microrutas.id_microruta`, obligatorio, índice | Microruta relacionada. |
| `id_barrio` | Integer | FK a `barrios.id_barrio`, obligatorio, índice | Barrio asociado. |
| `orden_visita` | Integer | Obligatorio | Orden de visita. |
| `hora_estimada_llegada` | Time | Opcional | Hora estimada de llegada. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado de la parada. |

**Relaciones:** pertenece a una `Microruta` y se relaciona con un `Barrio`.

### 4.5. `vehiculo.py` – Flota vehicular

#### `Vehiculo` — tabla `vehiculos`

Almacena la información de los vehículos que pueden ser asignados a la operación.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_vehiculo` | UUID | PK, generado por defecto | Identificador del vehículo. |
| `tipo` | String(50) | Obligatorio | Tipo de vehículo. |
| `placa` | String(20) | Obligatorio, único, índice | Placa. |
| `num_interno` | String(20) | Obligatorio, único | Número interno. |
| `marca` | String(50) | Opcional | Marca. |
| `modelo` | String(50) | Opcional | Modelo. |
| `capacidad_ton` | Float | Opcional | Capacidad en toneladas. |
| `fecha_adquisicion` | Date | Opcional | Fecha de adquisición. |
| `estado_operativo` | String(30) | Obligatorio, default `operativo` | Estado operativo. |

**Relaciones:** puede tener varias `Asignacion` y varias `EjecucionRuta`.

### 4.6. `programacion.py` – Programación y asignaciones

#### Tabla de asociación `programacion_dia`

Relaciona programaciones de ruta con días de la semana.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_programacion` | UUID | PK compuesta, FK a `programaciones_ruta.id_programacion` | Programación relacionada. |
| `id_dia` | Integer | PK compuesta, FK a `dias_semana.id_dia` | Día asociado. |

#### `DiaSemana` — tabla `dias_semana`

Catálogo de días de la semana.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_dia` | Integer | PK, índice | Identificador del día. |
| `nombre_dia` | String(20) | Obligatorio, único | Nombre del día. |

#### `Turno` — tabla `turnos`

Define los turnos y sus horarios.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_turno` | Integer | PK, índice | Identificador del turno. |
| `nombre_turno` | String(50) | Obligatorio, único | Nombre del turno. |
| `hora_inicio` | Time | Obligatorio | Hora de inicio. |
| `hora_fin` | Time | Obligatorio | Hora de finalización. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado del turno. |

**Relaciones:** puede estar relacionado con varias `Asignacion`.

#### `ProgramacionRuta` — tabla `programaciones_ruta`

Define la programación de una macroruta, su cuadrilla, conductor y vigencia.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_programacion` | UUID | PK, generado por defecto | Identificador de la programación. |
| `id_macroruta` | Integer | FK a `macrorutas.id_macroruta`, obligatorio, índice | Macroruta programada. |
| `id_cuadrilla` | UUID | FK a `cuadrillas.id_cuadrilla`, obligatorio, índice | Cuadrilla asignada. |
| `id_conductor` | UUID | FK a `conductores.id_conductor`, obligatorio, índice | Conductor asignado. |
| `vigencia_desde` | Date | Obligatorio | Inicio de vigencia. |
| `vigencia_hasta` | Date | Opcional | Fin de vigencia. |
| `estado` | String(20) | Obligatorio, default `activo` | Estado de la programación. |

**Relaciones:** pertenece a una `Macroruta`, una `Cuadrilla` y un `Conductor`; se asocia con varios `DiaSemana` mediante `programacion_dia` y puede tener varias `Asignacion`.

#### `Asignacion` — tabla `asignaciones`

Registra la asignación de un vehículo a una programación y un turno para una fecha.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_asignacion` | UUID | PK, generado por defecto | Identificador de la asignación. |
| `id_programacion` | UUID | FK a `programaciones_ruta.id_programacion`, obligatorio, índice | Programación relacionada. |
| `id_vehiculo` | UUID | FK a `vehiculos.id_vehiculo`, obligatorio, índice | Vehículo asignado. |
| `id_turno` | Integer | FK a `turnos.id_turno`, obligatorio, índice | Turno asignado. |
| `fecha` | Date | Obligatorio, índice | Fecha de la asignación. |
| `estado` | String(20) | Obligatorio, default `programada` | Estado de la asignación. |

**Relaciones:** pertenece a una `ProgramacionRuta`, un `Vehiculo` y un `Turno`; puede tener varias `EjecucionRuta`.

### 4.7. `ejecucion.py` – Ejecución operativa y seguimiento GPS

#### `EjecucionRuta` — tabla `ejecuciones_ruta`

Representa la ejecución real de una asignación.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_ejecucion` | UUID | PK, generado por defecto | Identificador de la ejecución. |
| `id_asignacion` | UUID | FK a `asignaciones.id_asignacion`, obligatorio, índice | Asignación ejecutada. |
| `id_vehiculo` | UUID | FK a `vehiculos.id_vehiculo`, obligatorio, índice | Vehículo utilizado. |
| `fecha_hora_inicio` | DateTime con zona horaria | Obligatorio | Inicio de la ejecución. |
| `fecha_hora_fin` | DateTime con zona horaria | Opcional | Fin de la ejecución. |
| `duracion_real` | String(50) | Opcional | Duración real registrada. |
| `observaciones` | Text | Opcional | Observaciones. |
| `estado` | String(20) | Obligatorio, default `en_proceso` | Estado de la ejecución. |

**Relaciones:** pertenece a una `Asignacion` y un `Vehiculo`; puede tener varias `UbicacionGPS` y varias `Novedad`.

#### `CuadrillaEjecucion` — tabla `cuadrilla_ejecucion`

Tabla intermedia que registra las cuadrillas participantes en una ejecución y sus horarios.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_cuadrilla` | UUID | PK compuesta, FK a `cuadrillas.id_cuadrilla` | Cuadrilla participante. |
| `id_ejecucion` | UUID | PK compuesta, FK a `ejecuciones_ruta.id_ejecucion` | Ejecución relacionada. |
| `hora_inicio` | Time | Opcional | Inicio de participación. |
| `hora_fin` | Time | Opcional | Fin de participación. |

#### `EjecucionParada` — tabla `ejecucion_parada`

Tabla intermedia que registra la información real de las paradas realizadas durante una ejecución.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_ejecucion` | UUID | PK compuesta, FK a `ejecuciones_ruta.id_ejecucion` | Ejecución relacionada. |
| `id_parada` | Integer | PK compuesta, FK a `paradas_ruta.id_parada` | Parada realizada. |
| `hora_llegada_real` | Time | Opcional | Hora real de llegada. |
| `observacion` | Text | Opcional | Observación de la parada. |

#### `UbicacionGPS` — tabla `ubicaciones_gps`

Almacena registros de ubicación geográfica asociados a una ejecución.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_ubicacion` | Integer | PK, índice | Identificador de la ubicación. |
| `id_ejecucion` | UUID | FK a `ejecuciones_ruta.id_ejecucion`, obligatorio, índice | Ejecución relacionada. |
| `fecha_hora` | DateTime con zona horaria | Obligatorio, default `now()`, índice | Fecha y hora del registro. |
| `latitud` | Numeric(10, 8) | Obligatorio | Latitud. |
| `longitud` | Numeric(11, 8) | Obligatorio | Longitud. |
| `coordenadas` | String(100) | Opcional | Representación textual de coordenadas. |
| `velocidad` | Float | Opcional | Velocidad registrada. |

**Relación:** cada ubicación pertenece a una `EjecucionRuta`.

### 4.8. `novedad.py` – Registro de novedades

#### `Novedad` — tabla `novedades`

Registra situaciones que afectan el desarrollo de una ejecución de ruta.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_novedad` | UUID | PK, generado por defecto | Identificador de la novedad. |
| `id_ejecucion` | UUID | FK a `ejecuciones_ruta.id_ejecucion`, obligatorio, índice | Ejecución afectada. |
| `id_usuario` | UUID | FK a `usuarios.id_usuario`, opcional, índice | Usuario que registra la novedad. |
| `tipo_novedad` | String(50) | Obligatorio | Tipo de novedad. |
| `descripcion` | Text | Obligatorio | Descripción. |
| `fecha_hora` | DateTime con zona horaria | Obligatorio, default `now()` | Fecha y hora del registro. |
| `direccion_ref` | String(200) | Opcional | Dirección o referencia del lugar. |
| `estado` | String(20) | Obligatorio, default `reportada` | Estado de la novedad. |

**Relaciones:** pertenece a una `EjecucionRuta` y puede estar asociada a un `Usuario`.

## 5. Resumen de modelos y tablas

| Archivo | Clases y tablas |
|---|---|
| `usuario.py` | `Rol` (`roles`), `Perfil` (`perfiles`), `UsuarioPerfil` (`usuario_perfil`), `Usuario` (`usuarios`). |
| `personal.py` | `Trabajador` (`trabajadores`), `Conductor` (`conductores`), `Cuadrilla` (`cuadrillas`), `TrabajadorCuadrilla` (`trabajador_cuadrilla`). |
| `territorio.py` | `Barrio` (`barrios`). |
| `ruta.py` | `Macroruta` (`macrorutas`), `Microruta` (`microrutas`), `ParadaRuta` (`paradas_ruta`). |
| `vehiculo.py` | `Vehiculo` (`vehiculos`). |
| `programacion.py` | `DiaSemana` (`dias_semana`), `Turno` (`turnos`), `ProgramacionRuta` (`programaciones_ruta`), `Asignacion` (`asignaciones`) y `programacion_dia`. |
| `ejecucion.py` | `EjecucionRuta` (`ejecuciones_ruta`), `CuadrillaEjecucion` (`cuadrilla_ejecucion`), `EjecucionParada` (`ejecucion_parada`), `UbicacionGPS` (`ubicaciones_gps`). |
| `novedad.py` | `Novedad` (`novedades`). |

El código compartido define **22 clases de modelo y 1 tabla de asociación** (`programacion_dia`).

## 6. Relaciones principales entre módulos

- **Usuarios y perfiles:** `Usuario` se asocia con `Perfil` mediante `UsuarioPerfil`; `Perfil` pertenece a `Rol`.
- **Usuarios y personal:** `Trabajador` referencia a `Usuario`; `Conductor` referencia a `Trabajador`.
- **Personal y cuadrillas:** `Trabajador` y `Cuadrilla` se vinculan mediante `TrabajadorCuadrilla`.
- **Territorio y rutas:** `Macroruta` agrupa `Microruta`; cada microruta contiene paradas (`ParadaRuta`) y cada parada referencia un barrio.
- **Programación:** `ProgramacionRuta` relaciona una macroruta, una cuadrilla y un conductor; también se vincula con días mediante `programacion_dia`.
- **Asignaciones:** `Asignacion` relaciona una programación con un vehículo y un turno para una fecha.
- **Ejecución:** `EjecucionRuta` registra la ejecución de una asignación y el vehículo utilizado.
- **Seguimiento:** `UbicacionGPS` registra posiciones asociadas a una ejecución.
- **Novedades:** `Novedad` se asocia con una ejecución y, opcionalmente, con el usuario que la registra.
- **Participación y paradas:** `CuadrillaEjecucion` y `EjecucionParada` registran información complementaria de una ejecución.

## 7. Comportamiento de eliminación

En las claves foráneas se declaran los siguientes comportamientos:

- **`CASCADE`:** permite propagar la eliminación a registros dependientes, según la relación configurada.
- **`RESTRICT`:** impide eliminar un registro que continúa siendo referenciado.
- **`SET NULL`:** establece el valor de la clave foránea en `NULL` cuando se elimina el registro referenciado.

Estos comportamientos corresponden a las opciones `ondelete` declaradas en las claves foráneas. Las opciones `cascade` de `relationship` son configuraciones adicionales del ORM y deben considerarse junto con las reglas de la base de datos.

## 8. Consideraciones

1. Esta documentación describe los campos y relaciones declarados en los modelos compartidos. No confirma por sí sola que las tablas ya estén creadas en PostgreSQL; eso se verifica mediante las migraciones.
2. Las reglas de negocio que no estén expresadas como restricciones en los modelos deben validarse en las capas correspondientes del backend, como servicios y esquemas.
3. Los valores predeterminados indicados corresponden a los declarados mediante `server_default`.
4. Los modelos deben mantenerse sincronizados con el modelo relacional y las migraciones de Alembic.
5. La documentación debe actualizarse cuando se agreguen, eliminen o modifiquen modelos, campos o relaciones.

## 9. Resultado

Se documentaron los modelos SQLAlchemy compartidos para Tura Limpia, organizados en las áreas de usuarios, personal, territorio, rutas, vehículos, programación, ejecución y novedades. El documento identifica las tablas, atributos, restricciones y relaciones principales, y sirve como referencia para el desarrollo de esquemas, repositorios, servicios, endpoints y migraciones de la base de datos.