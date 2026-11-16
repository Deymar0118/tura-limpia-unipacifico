
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.database import get_db
from src.routers import administracion, auth


settings = get_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("turalimpia.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""

    logger.info("Iniciando TuraLimpia API...")

    if settings.es_produccion:
        settings.validar_produccion()

        if settings.debug:
            raise RuntimeError(
                "DEBUG no puede estar habilitado en producción."
            )

    yield

    logger.info("Cerrando TuraLimpia API...")


app = FastAPI(
    title=settings.app_name,
    description=(
        "API REST para el Sistema de Gestión y Optimización de la "
        "Recolección y Transporte de Residuos Sólidos en Buenaventura."
    ),
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS: permite los dominios configurados en ALLOWED_ORIGINS.
origins = [
    origin.strip()
    for origin in settings.allowed_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_headers(
    request: Request,
    call_next,
) -> Response:
    """Agrega encabezados de seguridad HTTP."""

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    if settings.es_produccion:
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )

    return response


# Routers
app.include_router(auth.router)
app.include_router(administracion.router)


@app.get("/", tags=["Root"], summary="Estado general de la API")
async def root():
    return {
        "mensaje": "Bienvenido a TuraLimpia API",
        "version": settings.app_version,
        "documentacion": "/docs",
        "status": "active",
    }


@app.get(
    "/healthcheck",
    tags=["Health"],
    summary="Verificar estado de la API",
    description="Comprueba la conectividad con PostgreSQL.",
)
async def healthcheck(
    db: AsyncSession = Depends(get_db),
):
    try:
        await db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
            "app": settings.app_name,
            "version": settings.app_version,
        }

    except Exception:
        logger.exception("Error en el healthcheck")

        raise HTTPException(
            status_code=503,
            detail="La base de datos no está disponible.",
        )
