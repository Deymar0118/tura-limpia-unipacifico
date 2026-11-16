
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.repository.usuario_repository import UsuarioRepository
from src.schemas.auth import (
    LoginRequest,
    RegistroRequest,
    RegistroResponse,
    TokenPayload,
    TokenResponse,
    UsuarioActualResponse,
)
from src.security.auth_depends import obtener_usuario_actual
from src.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AuthService:
    """Construye el servicio de autenticación."""

    return AuthService(UsuarioRepository(db))


@router.post(
    "/register",
    response_model=RegistroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar ciudadano",
    description=(
        "Registra una nueva cuenta ciudadana. "
        "El rol ciudadano se asigna automáticamente. "
        "No requiere registro para consultar los vehículos."
    ),
    responses={
        409: {"description": "Correo o usuario ya registrado."},
        422: {"description": "Datos de registro inválidos."},
    },
)
async def registrar(
    datos: RegistroRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Registra un nuevo ciudadano."""

    return await auth_service.registrar(datos)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description=(
        "Autentica un usuario mediante correo electrónico "
        "o nombre de usuario y contraseña. Retorna un JWT de acceso."
    ),
    responses={
        401: {"description": "Credenciales inválidas."},
        403: {"description": "Usuario inactivo o sin rol activo."},
    },
)
async def login(
    datos: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Autentica al usuario y genera su token."""

    return await auth_service.login(datos)


@router.get(
    "/me",
    response_model=UsuarioActualResponse,
    summary="Consultar usuario autenticado",
    description=(
        "Retorna los datos del usuario asociado al JWT "
        "enviado en la cabecera Authorization."
    ),
    responses={
        401: {"description": "Token inválido o expirado."},
    },
)
async def me(
    usuario: TokenPayload = Depends(obtener_usuario_actual),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Obtiene los datos del usuario autenticado."""

    return await auth_service.obtener_usuario_actual(usuario.sub)
