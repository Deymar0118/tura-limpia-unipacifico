from fastapi import APIRouter, Query, Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_service import AuthService

from src.repository import (
    UsuarioRepository,
    RolRepository,
    TokenRevocadoRepository,
    PerfilRepository,
)

from src.core.database import get_db
from src.security import (
    obtener_usuario_actual,
    requiere_rol,
    limiter,
)
from src.schemas import (

    LoginRequest,
    RegistroRequest,
    RefreshRequest,
    LogoutRequest,
    CambioPasswordRequest,
    AsignarRolRequest,
    TokenResponse,
    TokenPayload,
    UsuarioResponse,
    RolEnum,
)

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    usuario_repo = UsuarioRepository(db)
    rol_repo = RolRepository(db)
    perfil_repo = PerfilRepository(db)
    token_revocado_repo = TokenRevocadoRepository(db)

    return AuthService(
        usuario_repository=usuario_repo,
        rol_repository=rol_repo,
        perfil_repository=perfil_repo,
        token_revocado_repository=token_revocado_repo
    )

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/registro",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una cuenta con rol CIUDADANO por defecto y retorna los tokens de acceso.",
    responses={
        201: {"description": "Usuario creado exitosamente"},
        400: {"description": "Email ya registrado o datos invalidos"},
        429: {"description": "Limite de solicitudes excedido (3/min)"},
    },
)
@limiter.limit("3/minute")
async def registrar_usuario(request: Request, datos: RegistroRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.registrar_usuario(datos)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesion",
    description="Autentica al usuario con email y password, retorna access y refresh token.",
    responses={
        200: {"description": "Login exitoso"},
        401: {"description": "Credenciales invalidas"},
        429: {"description": "Limite de solicitudes excedido (5/min)"},
    },
)
@limiter.limit("5/minute")
async def login(request: Request, datos: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(datos)

