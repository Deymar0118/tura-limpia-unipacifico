import uuid
from fastapi import HTTPException, status
from src.models import Usuario
from src.repository.usuario_repository import ESTADO_ACTIVO, UsuarioRepository
from src.schemas.auth import LoginRequest, RolEnum, TokenResponse, UsuarioActualResponse
from src.security.password import verificar_password
from src.security.tokens import crear_access_token


class AuthService:
    """Lógica de negocio del inicio de sesión (RF-06)."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    async def login(self, datos: LoginRequest) -> TokenResponse:
        usuario = await self.usuario_repository.buscar_por_correo_o_usuario(datos.identificador.strip())
        if not usuario or not verificar_password(datos.password, usuario.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
        if usuario.estado != ESTADO_ACTIVO:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuario inactivo")

        rol = await self._obtener_rol(usuario.id_usuario)
        return TokenResponse(access_token=crear_access_token(str(usuario.id_usuario), rol.value))

    async def obtener_usuario_actual(self, id_usuario: str) -> UsuarioActualResponse:
        usuario = await self._buscar_usuario_activo(id_usuario)
        rol = await self._obtener_rol(usuario.id_usuario)
        return UsuarioActualResponse(
            id=str(usuario.id_usuario),
            nombre=usuario.nombre_completo or f"{usuario.nombres} {usuario.apellidos}",
            email=usuario.correo,
            rol=rol,
        )

    async def _buscar_usuario_activo(self, id_usuario: str) -> Usuario:
        try:
            usuario = await self.usuario_repository.buscar_por_id(uuid.UUID(id_usuario))
        except ValueError:
            usuario = None
        if not usuario or usuario.estado != ESTADO_ACTIVO:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return usuario

    async def _obtener_rol(self, id_usuario: uuid.UUID) -> RolEnum:
        """Obtiene el rol vigente y verifica que sea uno de los roles de RF-01."""
        nombre_rol = await self.usuario_repository.obtener_rol_activo(id_usuario)
        try:
            return RolEnum(nombre_rol)
        except ValueError:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuario sin rol activo")
