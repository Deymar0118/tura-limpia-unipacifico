# Arquitectura del sistema – Tura Limpia

## 1. Descripción general

Tura Limpia utiliza una arquitectura cliente-servidor en la que el frontend se encarga de la interacción con los usuarios, el backend procesa las solicitudes y aplica las reglas de negocio, y PostgreSQL almacena la información del sistema.

La solución está construida con las siguientes tecnologías:

| Componente | Tecnología |
|---|---|
| Frontend | React 19 |
| Herramienta de desarrollo frontend | Vite |
| Navegación | React Router |
| Backend | Python y FastAPI |
| ORM | SQLAlchemy |
| Base de datos | PostgreSQL |
| Migraciones | Alembic |
| Autenticación | JWT |

## 2. Estructura general

El proyecto está dividido en dos módulos principales:

- `frontend/`: contiene la aplicación web y sus componentes visuales.
- `backend/`: contiene la API, las reglas de negocio, el acceso a datos y las migraciones de la base de datos.

La estructura general es:

```text
tura-limpia-unipacifico/
│
├── backend/
│   ├── alembic/
│   │   └── versions/
│   └── src/
│       ├── models/
│       ├── repository/
│       ├── routers/
│       ├── schemas/
│       ├── services/
│       └── main.py
│
├── frontend/
│   └── src/
│       ├── app/
│       ├── modules/
│       │   ├── admin/
│       │   ├── auth/
│       │   └── construction/
│       ├── shared/
│       └── App.jsx
│
└── docs/
```

## 3. Arquitectura del backend

El backend está desarrollado con FastAPI y utiliza una separación por responsabilidades para organizar el procesamiento de las solicitudes.

### 3.1. Routers

Ubicación:

`backend/src/routers/`

Los routers definen los endpoints de la API, reciben las solicitudes HTTP y conectan las operaciones con los servicios correspondientes.

En el módulo de administración se encuentra:

`administracion.py`

Este router expone las operaciones relacionadas con la gestión de usuarios, consulta de roles, actualización de información y asignación de perfiles.

### 3.2. Schemas

Ubicación:

`backend/src/schemas/`

Los schemas definen la estructura de los datos que recibe y devuelve la API.

Se utilizan para:

- Validar los datos de entrada.
- Definir los campos obligatorios y opcionales.
- Establecer los tipos de datos.
- Estandarizar las respuestas de los endpoints.

Entre los esquemas utilizados en la gestión de usuarios se encuentran los de creación, actualización, asignación de perfiles y listado de usuarios.

### 3.3. Services

Ubicación:

`backend/src/services/`

La capa de servicios contiene la lógica de negocio.

Se encarga de procesar las operaciones solicitadas por los routers, aplicar las validaciones correspondientes y coordinar las operaciones de persistencia mediante los repositorios.

En el módulo de administración, `administracion_service.py` contiene la lógica para registrar, consultar, actualizar y gestionar los perfiles de los usuarios, además de las protecciones relacionadas con los administradores y el superadministrador.

### 3.4. Repository

Ubicación:

`backend/src/repository/`

La capa de repositorios centraliza las operaciones de acceso a datos.

Se comunica con PostgreSQL mediante SQLAlchemy y permite separar las consultas y operaciones de persistencia de la lógica de negocio.

El archivo `administracion_repository.py` contiene las consultas relacionadas con los usuarios, perfiles y administradores activos.

### 3.5. Models

Ubicación:

`backend/src/models/`

Los modelos representan las entidades almacenadas en la base de datos y definen sus columnas, relaciones y restricciones.

Se utilizan mediante SQLAlchemy para interactuar con las tablas de PostgreSQL.

### 3.6. Migraciones

Ubicación:

`backend/alembic/versions/`

Alembic administra los cambios en la estructura de la base de datos.

Las migraciones permiten incorporar nuevas columnas, índices y restricciones sin tener que reconstruir manualmente toda la base de datos.

## 4. Arquitectura del frontend

El frontend está desarrollado con React y utiliza React Router para administrar la navegación entre las diferentes páginas.

La organización se realiza mediante módulos funcionales.

### 4.1. Módulo de autenticación

Ubicación:

`frontend/src/modules/auth/`

Contiene las funcionalidades de inicio de sesión y la comunicación con los endpoints de autenticación.

El servicio de autenticación obtiene el token de acceso y consulta la información del usuario autenticado.

### 4.2. Módulo de administración

Ubicación:

`frontend/src/modules/admin/`

Contiene la interfaz para gestionar los usuarios del sistema.

Incluye:

- Página principal de administración.
- Tabla de usuarios.
- Formulario de creación y edición.
- Servicio de comunicación con los endpoints administrativos.

### 4.3. Módulo de construcción

Ubicación:

`frontend/src/modules/construction/`

Contiene una página provisional para los perfiles cuyos módulos funcionales todavía no están disponibles.

Permite mostrar el nombre del usuario y su rol, e informa que las funcionalidades correspondientes se encuentran en construcción.

### 4.4. Componentes compartidos

Ubicación:

`frontend/src/shared/`

Contiene elementos reutilizables por diferentes módulos. Entre ellos se encuentra el cliente de API, responsable de centralizar las solicitudes HTTP al backend.

## 5. Comunicación entre componentes

El flujo general de comunicación es:

1. El usuario interactúa con la interfaz React.
2. El frontend realiza una solicitud HTTP al backend.
3. FastAPI recibe la solicitud mediante el router correspondiente.
4. Los schemas validan la estructura de los datos.
5. El servicio ejecuta las reglas de negocio.
6. El repositorio realiza las operaciones necesarias en PostgreSQL.
7. El backend devuelve una respuesta HTTP.
8. El frontend procesa la respuesta y actualiza la interfaz.

## 6. Autenticación y autorización

La autenticación se realiza mediante tokens JWT.

El frontend conserva el token de acceso y lo utiliza para enviar solicitudes a los endpoints protegidos.

El backend valida el acceso y determina si el usuario tiene los permisos necesarios para ejecutar cada operación.

La autorización no depende únicamente de las restricciones de navegación del frontend: las operaciones protegidas también se validan en la API.

## 7. Ejecución en entorno local

### Backend

Desde la carpeta `backend`, con el entorno virtual activado:

```powershell
uvicorn src.main:app --reload
```

La API queda disponible en:

`http://localhost:8000`

La documentación interactiva se encuentra en:

`http://localhost:8000/docs`

### Frontend

Desde la carpeta `frontend`:

```powershell
npm run dev
```

La aplicación se ejecuta mediante el servidor de desarrollo de Vite.

## 8. Consideraciones de arquitectura

La separación entre routers, schemas, servicios, repositorios y modelos facilita el mantenimiento y la evolución del sistema.

Esta organización permite incorporar nuevos módulos funcionales sin concentrar toda la lógica en un único componente y facilita la implementación de reglas de negocio y controles de acceso desde el backend.