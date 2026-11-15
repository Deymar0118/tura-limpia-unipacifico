from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.repository.usuario_repository import UsuarioRepository
from src.schemas.auth import LoginRequest, TokenPayload, TokenResponse, UsuarioActualResponse
from src.security.auth_depends import obtener_usuario_actual
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UsuarioRepository(db))


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autentica con correo o nombre de usuario y contraseña (RF-06) y retorna el token de acceso.",
    responses={
        401: {"description": "Credenciales inválidas"},
        403: {"description": "Usuario inactivo o sin rol activo"},
    },
)
async def login(datos: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(datos)


@router.get(
    "/me",
    response_model=UsuarioActualResponse,
    summary="Usuario autenticado",
    description="Retorna los datos y el rol del dueño del token para asignar permisos en la vista (RF-06).",
    responses={401: {"description": "Token inválido o expirado"}},
)
async def me(
    usuario: TokenPayload = Depends(obtener_usuario_actual),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.obtener_usuario_actual(usuario.sub)
