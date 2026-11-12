import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.core.config import get_settings
from src.core.database import crear_tablas, get_db

logger = logging.getLogger("turalimpia.main")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja los eventos de inicio (startup) y cierre (shutdown) del servidor."""
    logger.info("Iniciando TuraLimpia API...")
    try:
        if settings.es_produccion:
            logger.info("Validando credenciales de entorno de producción...")
            settings.validar_produccion()

        logger.info("Inicializando esquema de tablas en PostgreSQL...")
        await crear_tablas()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error crítico en el arranque del servidor: {e}", exc_info=True)
        raise e

    yield
    logger.info("Apagando servidor TuraLimpia API...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API REST para el Sistema de Gestión y Optimización de la Recolección "
        "y Transporte de Residuos Sólidos en Buenaventura (TuraLimpia)."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración de políticas de origen cruzado (CORS) para el Frontend en React
origins = [o.strip() for o in settings.allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Inyecta cabeceras de seguridad HTTP a todas las respuestas del servidor."""
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    if settings.es_produccion:
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )

    return response


@app.get("/", tags=["Root"])
async def root():
    """Ruta raíz de confirmación de estado de la API."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "status": "active",
    }


@app.get("/healthcheck", tags=["Health"])
async def healthcheck(db: AsyncSession = Depends(get_db)):
    """Evalúa la conectividad en tiempo real con la base de datos PostgreSQL."""
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "app": settings.app_name,
            "version": settings.app_version,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión con PostgreSQL: {str(e)}",
        )