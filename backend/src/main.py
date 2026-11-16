
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
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""

    logger.info("Iniciando TuraLimpia API...")

    if settings.entorno == "produccion":
        if settings.debug:
            raise RuntimeError(
                "DEBUG no puede estar habilitado en producción."
            )

    yield

    logger.info("Cerrando TuraLimpia API...")


app = FastAPI(
    title="TuraLimpia API",
    description=(
        "API REST para el sistema de Gestión y Optimización "
        "de la Recolección y Transporte de Residuos Sólidos "
        "en Buenaventura. Proyecto Tura Limpia."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Encabezados de seguridad
@app.middleware("http")
async def security_headers(
    request: Request,
    call_next,
) -> Response:
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


# Routers
app.include_router(auth.router)
app.include_router(administracion.router)


# Endpoint raíz
@app.get(
    "/",
    tags=["Root"],
    summary="Estado general de la API",
)
async def root():
    return {
        "mensaje": "Bienvenido a TuraLimpia API",
        "version": "1.0.0",
        "documentacion": "/docs",
    }


# Healthcheck
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
            "app": "TuraLimpia API",
            "version": "1.0.0",
        }

    except Exception:
        logger.exception("Error en el healthcheck")

        raise HTTPException(
            status_code=503,
            detail="La base de datos no está disponible.",
        )
