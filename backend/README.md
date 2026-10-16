# Backend - Tura Limpia

API del proyecto construida con FastAPI y PostgreSQL.

## Requisitos previos

- Python 3.10 a 3.12 (versiones más recientes como 3.13/3.14 pueden dar problemas con algunas dependencias, ver sección de problemas comunes)
- PostgreSQL instalado localmente. Si no lo tienes, descárgalo de https://www.postgresql.org/download/ y sigue el instalador (deja las opciones por defecto, solo anota la contraseña que pongas para el usuario `postgres`)
- Git

## Estructura del proyecto

```text
backend/
├── alembic/                  # Control de versiones y migraciones de la BD
│   └── versions/
├── assets/                   # Recursos estáticos y diagramas
├── tests/                    # Pruebas unitarias e integración
│   ├── api/
│   └── services/
├── src/                      # Código fuente ejecutable de la aplicación
│   ├── main.py               # Punto de entrada de FastAPI y Middlewares
│   ├── core/                 # Configuración (config.py), conexión a BD (database.py) y errores
│   ├── models/               # Modelos ORM de SQLAlchemy (User, Ruta, Vehiculo, etc.)
│   ├── repository/           # Consultas y acceso a la base de datos (CRUDs)
│   ├── routers/              # Endpoints REST (FastAPI Routers)
│   ├── schemas/              # Modelos de validación y DTOs con Pydantic
│   ├── security/             # Autenticación, hashing (Bcrypt) y tokens JWT
│   └── services/             # Lógica y reglas de negocio
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Reglas de exclusión de Git (venv, .env, __pycache__)
├── alembic.ini               # Configuración global de Alembic
├── Procfile                  # Configuración de despliegue PaaS (Render / Heroku)
├── requirements.txt          # Dependencias del proyecto
└── seed_admin.py             # Script de inicialización del usuario Administrador principal
```


## Como ejecutarlo localmente

Clonar el proyecto

```
git clone https://github.com/Deymar0118/tura-limpia-unipacifico.git
```

Ir a la carpeta del backend

```
cd tura-limpia-unipacifico/backend
```

Crear y activar el entorno virtual

```
python -m venv venv
venv\Scripts\activate
```

Instalar las dependencias

```
pip install -r requirements.txt
```

Crear una base de datos local en PostgreSQL llamada `tura_limpia` (usando pgAdmin, que se instala junto con PostgreSQL: clic derecho en Databases > Create > Database)

Copiar el archivo de variables de entorno y poner tu propia contraseña de PostgreSQL

```
copy .env.example .env
```

Levantar el servidor

```
uvicorn src.main:app --reload
```

## Endpoints

- API: http://127.0.0.1:8000/
- Prueba de conexión a la base de datos: http://127.0.0.1:8000/test-db
- Documentación de la API: http://127.0.0.1:8000/docs

## Problemas comunes

**Error `ModuleNotFoundError: No module named 'psycopg'`**

Ocurre con versiones nuevas de Python (3.13/3.14) donde `psycopg2-binary` no instala correctamente. Solución:

```
pip install "psycopg[binary]"
```

**El servidor no arranca / error de conexión a la base de datos**

Verifica que:
- PostgreSQL esté corriendo (en Windows: buscar "Servicios", confirmar que el servicio `postgresql-x64-...` diga "En ejecución")
- La contraseña en tu archivo `.env` sea exactamente la misma que configuraste al instalar PostgreSQL
- La base de datos `turalimpia` exista (verificar en pgAdmin)